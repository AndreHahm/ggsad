"""Controlled `draft -> ready` transition (R-010, R-011, R-012, R-013, R-014).

The only transition CHG-001 implements -- not a general status editor
(R-010, ADR-0005). `perform_transition` evaluates every R-011 precondition
before writing anything, and writes only through `state_writer.
atomic_replace_state`, so a rejected transition never mutates `state.yaml`
(R-012) and a successful one is never partially written (R-013).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ggsad.application.create_change import validate_change_id
from ggsad.application.validate_repository import validate_change, validate_project_config
from ggsad.engine.state_writer import atomic_replace_state
from ggsad.models.state import ChangeState, HistoryEvent, dump_change_state
from ggsad.models.validation import IssueCategory, ValidationIssue
from ggsad.validators.yaml_loader import dump_yaml_bytes, load_yaml_file

SUPPORTED_SOURCE_PHASE = "specify"
SUPPORTED_SOURCE_STATUS = "draft"
SUPPORTED_TARGET_STATUS = "ready"


def _transition_evidence(target: Path, change_dir: Path) -> list[str]:
    """Capture immutable digests of artifacts evaluated for draft-to-ready."""
    paths = [
        target / ".ggsad" / "config.yaml",
        change_dir / "state.yaml",
        change_dir / "spec.md",
        change_dir / "plan.md",
    ]
    return [
        f"sha256:{path.relative_to(target).as_posix()}:{hashlib.sha256(path.read_bytes()).hexdigest()}"
        for path in paths
        if path.is_file()
    ]


def find_change_directory(target: Path, change_id: str) -> Path | None:
    """Locate the single `specs/<change_id>-*/` directory for `change_id`, if any."""
    specs_dir = target / "specs"
    if not specs_dir.is_dir():
        return None
    matches = [p for p in specs_dir.glob(f"{change_id}-*") if p.is_dir()]
    return matches[0] if matches else None


def _validate_source_state(state: ChangeState, *, file_label: str) -> list[ValidationIssue]:
    if state.flow.phase == SUPPORTED_SOURCE_PHASE and state.flow.status == SUPPORTED_SOURCE_STATUS:
        return []
    return [
        ValidationIssue(
            category=IssueCategory.UNSUPPORTED_TRANSITION,
            file=file_label,
            field="flow",
            reason=(
                f"Unsupported source state for this transition: "
                f"phase={state.flow.phase!r}, status={state.flow.status!r}. CHG-001 only "
                f"supports {SUPPORTED_SOURCE_PHASE}/{SUPPORTED_SOURCE_STATUS} -> "
                f"{SUPPORTED_SOURCE_PHASE}/{SUPPORTED_TARGET_STATUS}."
            ),
        )
    ]


def _validate_no_active_wait_or_failure(
    state: ChangeState, *, file_label: str
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if state.wait.reason is not None:
        issues.append(
            ValidationIssue(
                category=IssueCategory.UNSUPPORTED_TRANSITION,
                file=file_label,
                field="wait/reason",
                reason=f"An active wait condition is recorded: {state.wait.reason!r}.",
                remediation="Resolve the wait condition before transitioning.",
            )
        )
    if state.failure.reason is not None:
        issues.append(
            ValidationIssue(
                category=IssueCategory.UNSUPPORTED_TRANSITION,
                file=file_label,
                field="failure/reason",
                reason=f"An active failure condition is recorded: {state.failure.reason!r}.",
                remediation="Resolve the failure condition before transitioning.",
            )
        )
    return issues


def evaluate_transition_preconditions(target: Path, change_dir: Path) -> list[ValidationIssue]:
    """Evaluate every R-011 precondition for the draft -> ready transition.

    Reuses the same config/mapping/artifact/state-schema/placeholder checks
    that power `ggsad validate` (R-005 through R-009) -- these directly cover
    R-011's first five bullets ("the project configuration is valid",
    "referenced mappings are valid", "the change state is valid", "required
    Class M artifacts exist", "the specification/plan has no unresolved
    placeholders"). The remaining two bullets ("no active wait or failure",
    "the current state is exactly the supported source state") are
    transition-specific and checked here.
    """
    issues = validate_project_config(target)
    issues += validate_change(target, change_dir)
    if issues:
        # state.yaml may not be schema-valid or even parseable at this
        # point; the transition-specific checks below need a constructible
        # ChangeState, so they can't run safely until the above is clean.
        return issues

    state_path = change_dir / "state.yaml"
    state = ChangeState.model_validate(load_yaml_file(state_path))
    issues += _validate_source_state(state, file_label=str(state_path))
    issues += _validate_no_active_wait_or_failure(state, file_label=str(state_path))
    return issues


@dataclass(frozen=True, slots=True)
class TransitionResult:
    """Outcome of a `perform_transition` call."""

    ok: bool
    issues: tuple[ValidationIssue, ...]
    new_status: str | None = None

    @property
    def rejected(self) -> bool:
        return not self.ok


def perform_transition(target: Path, change_id: str, *, actor: str) -> TransitionResult:
    """Transition `change_id` from specify/draft to specify/ready.

    Nothing is written unless every R-011 precondition holds. The write
    itself goes through `state_writer.atomic_replace_state` (R-013):
    serialize to a temp file in the same directory, re-validate it, then
    atomically replace `state.yaml`.
    """
    target = target.resolve()
    validate_change_id(change_id)  # defense in depth; matches R-004's format for any change ID

    change_dir = find_change_directory(target, change_id)
    if change_dir is None:
        issue = ValidationIssue(
            category=IssueCategory.MISSING_ARTIFACT,
            file=str(target / "specs"),
            reason=f"No change directory found for change ID {change_id!r}.",
        )
        return TransitionResult(ok=False, issues=(issue,))

    issues = evaluate_transition_preconditions(target, change_dir)
    if issues:
        return TransitionResult(ok=False, issues=tuple(issues))

    state_path = change_dir / "state.yaml"
    state = ChangeState.model_validate(load_yaml_file(state_path))

    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    history_event = HistoryEvent(
        timestamp=now,
        event="draft-to-ready",
        actor=actor,
        action="complete",
        previous_phase=state.flow.phase,
        previous_status=state.flow.status,
        new_phase=state.flow.phase,
        new_status=SUPPORTED_TARGET_STATUS,
        reason="draft-to-ready transition (R-010)",
        evidence=_transition_evidence(target, change_dir),
    )
    new_state = state.model_copy(
        update={
            "flow": state.flow.model_copy(update={"status": SUPPORTED_TARGET_STATUS}),
            "history": [*state.history, history_event],
        }
    )

    schema_path = target / ".ggsad" / "schemas" / "state.schema.json"
    new_bytes = dump_yaml_bytes(dump_change_state(new_state))
    atomic_replace_state(state_path, new_bytes, schema_path)

    return TransitionResult(ok=True, issues=(), new_status=SUPPORTED_TARGET_STATUS)
