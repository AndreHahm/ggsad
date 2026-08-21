"""Unit tests for the controlled draft-to-ready transition (R-010 through R-014)."""

from __future__ import annotations

from pathlib import Path

from ggsad.application.create_change import build_change_manifest
from ggsad.application.initialize_project import initialize_project
from ggsad.application.manifest_writer import write_manifest
from ggsad.engine.transitions import (
    find_change_directory,
    perform_transition,
)
from ggsad.models.validation import IssueCategory
from ggsad.validators.yaml_loader import dump_yaml_bytes, load_yaml_file


def _init(tmp_path: Path) -> Path:
    initialize_project(tmp_path)
    return tmp_path


def _new_change(target: Path, change_id: str = "CHG-002", slug: str = "example-change") -> Path:
    manifest = build_change_manifest(
        target, change_id=change_id, slug=slug, title="Example", goal="Ship it"
    )
    write_manifest(manifest)
    return target / "specs" / f"{change_id}-{slug}"


def _fill_in_spec_and_plan(change_dir: Path) -> None:
    (change_dir / "spec.md").write_text("# Spec\n\nFilled in.\n", encoding="utf-8")
    (change_dir / "plan.md").write_text("# Plan\n\nFilled in.\n", encoding="utf-8")


# --- find_change_directory -----------------------------------------------------------


def test_find_change_directory_locates_existing_change(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)

    assert find_change_directory(target, "CHG-002") == change_dir


def test_find_change_directory_returns_none_when_missing(tmp_path: Path) -> None:
    target = _init(tmp_path)

    assert find_change_directory(target, "CHG-999") is None


# --- rejection: unfilled templates (R-011) --------------------------------------------


def test_transition_rejects_unfilled_change_and_preserves_state(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    original = (change_dir / "state.yaml").read_bytes()

    result = perform_transition(target, "CHG-002", actor="human:test")

    assert not result.ok
    assert any(issue.category is IssueCategory.UNRESOLVED_PLACEHOLDER for issue in result.issues)
    assert (change_dir / "state.yaml").read_bytes() == original


def test_transition_rejects_missing_change_id(tmp_path: Path) -> None:
    target = _init(tmp_path)

    result = perform_transition(target, "CHG-999", actor="human:test")

    assert not result.ok
    assert result.issues[0].category is IssueCategory.MISSING_ARTIFACT


# --- E-010: valid transition ----------------------------------------------------------


def test_e010_valid_transition_succeeds_and_appends_history(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    _fill_in_spec_and_plan(change_dir)

    result = perform_transition(target, "CHG-002", actor="human:test")

    assert result.ok
    assert result.new_status == "ready"

    data = load_yaml_file(change_dir / "state.yaml")
    assert data["flow"]["phase"] == "specify"
    assert data["flow"]["status"] == "ready"
    assert len(data["history"]) == 2
    event = data["history"][-1]
    assert event["event"] == "draft-to-ready"
    assert event["actor"] == "human:test"
    assert event["action"] == "complete"
    assert event["previous_phase"] == "specify"
    assert event["previous_status"] == "draft"
    assert event["new_phase"] == "specify"
    assert event["new_status"] == "ready"
    assert event["reason"]


# --- E-011: unsupported source state ---------------------------------------------------


def test_e011_reject_unsupported_transition_and_preserve_state(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    _fill_in_spec_and_plan(change_dir)

    first = perform_transition(target, "CHG-002", actor="human:test")
    assert first.ok
    ready_bytes = (change_dir / "state.yaml").read_bytes()

    second = perform_transition(target, "CHG-002", actor="human:test")

    assert not second.ok
    assert any(issue.category is IssueCategory.UNSUPPORTED_TRANSITION for issue in second.issues)
    assert any("unsupported" in issue.reason.lower() for issue in second.issues)
    assert (change_dir / "state.yaml").read_bytes() == ready_bytes  # unchanged


# --- active wait/failure blocks the transition ------------------------------------------


def test_active_wait_blocks_transition(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    _fill_in_spec_and_plan(change_dir)
    state_path = change_dir / "state.yaml"
    data = load_yaml_file(state_path)
    data["wait"]["reason"] = "blocked on approval"
    data["wait"]["category"] = "WAIT_APPROVAL"
    state_path.write_bytes(dump_yaml_bytes(data))

    result = perform_transition(target, "CHG-002", actor="human:test")

    assert not result.ok
    assert any("wait" in (issue.field or "") for issue in result.issues)


def test_active_failure_blocks_transition(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    _fill_in_spec_and_plan(change_dir)
    state_path = change_dir / "state.yaml"
    data = load_yaml_file(state_path)
    data["failure"]["reason"] = "build broke"
    data["failure"]["category"] = "FAILED_TEST"
    state_path.write_bytes(dump_yaml_bytes(data))

    result = perform_transition(target, "CHG-002", actor="human:test")

    assert not result.ok
    assert any("failure" in (issue.field or "") for issue in result.issues)
