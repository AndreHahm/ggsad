"""Property-based tests for the transition engine (R-004, R-012, R-013, T-066).

ID/slug format-safety and path-containment properties already have dedicated
coverage in `tests/unit/test_create_change.py` (Hypothesis over arbitrary
digit counts, parameterized unsafe slugs). This file covers the two
properties specific to the transition engine: across every schema-valid
`(phase, status)` combination, only `specify/draft` may transition, and
every rejection -- for any reason -- leaves `state.yaml` byte-for-byte
unchanged.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

from ggsad.application.create_change import build_change_manifest
from ggsad.application.initialize_project import initialize_project
from ggsad.application.manifest_writer import write_manifest
from ggsad.engine.transitions import (
    SUPPORTED_SOURCE_PHASE,
    SUPPORTED_SOURCE_STATUS,
    perform_transition,
)
from ggsad.validators.yaml_loader import dump_yaml_bytes, load_yaml_file

_PHASES = (
    "intake",
    "explore",
    "decide",
    "specify",
    "plan",
    "build",
    "verify",
    "release",
    "closed",
)
_STATUSES = (
    "draft",
    "ready",
    "active",
    "waiting",
    "done",
    "failed",
    "cancelled",
    "superseded",
)


def _set_source_state(state_path: Path, phase: str, status: str) -> None:
    """Overwrite a change's phase/status, keeping the file schema-valid.

    `waiting`/`failed` statuses conditionally require non-null wait/failure
    fields per state.schema.json; filled in here so the only thing under
    test is the phase/status combination itself, not an incidental schema
    violation.
    """
    data = load_yaml_file(state_path)
    data["flow"]["phase"] = phase
    data["flow"]["status"] = status
    if status == "waiting":
        data["wait"].update(
            reason="property-test wait",
            category="WAIT_DEPENDENCY",
            resume_condition="dependency resolved",
            safe_state="draft",
            resume_phase="specify",
            next_action="wait",
        )
    if status == "failed":
        data["failure"].update(reason="property-test failure", category="FAILED_TEST")
    state_path.write_bytes(dump_yaml_bytes(data))


@given(phase=st.sampled_from(_PHASES), status=st.sampled_from(_STATUSES))
@settings(max_examples=len(_PHASES) * len(_STATUSES), deadline=None)
def test_only_specify_draft_transitions_all_others_preserve_bytes(phase: str, status: str) -> None:
    with tempfile.TemporaryDirectory() as raw_dir:
        target = Path(raw_dir)
        initialize_project(target)
        manifest = build_change_manifest(
            target, change_id="CHG-002", slug="example-change", title="Example", goal="Ship it"
        )
        write_manifest(manifest)
        change_dir = target / "specs" / "CHG-002-example-change"
        (change_dir / "spec.md").write_text("# Spec\n\nFilled in.\n", encoding="utf-8")
        (change_dir / "plan.md").write_text("# Plan\n\nFilled in.\n", encoding="utf-8")

        _set_source_state(change_dir / "state.yaml", phase, status)
        original_bytes = (change_dir / "state.yaml").read_bytes()

        result = perform_transition(target, "CHG-002", actor="property-test")

        is_supported_source = phase == SUPPORTED_SOURCE_PHASE and status == SUPPORTED_SOURCE_STATUS
        assert result.ok == is_supported_source

        current_bytes = (change_dir / "state.yaml").read_bytes()
        if is_supported_source:
            assert current_bytes != original_bytes  # a successful transition does write
        else:
            assert current_bytes == original_bytes  # R-012: rejection preserves bytes exactly
