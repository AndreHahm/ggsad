"""Unit tests for the typed ChangeState model."""

from __future__ import annotations

from ggsad.models.state import ChangeState

_VALID: dict = {
    "schema_version": "0.1",
    "change": {"id": "CHG-999", "slug": "example", "title": "Example", "class": "M"},
    "flow": {"profile": "standard", "phase": "specify", "status": "draft"},
    "goal": {"summary": "Do the thing."},
    "artifacts": {
        "spec": "spec.md",
        "plan": "plan.md",
        "tasks": "tasks.md",
        "evidence": "evidence.md",
    },
    "pair_review": {"required": True, "status": "pending", "requestor": None, "reviewer": None},
    "wait": {
        "reason": None,
        "category": None,
        "owner": None,
        "resume_condition": None,
        "safe_state": None,
        "resume_phase": None,
        "next_action": None,
    },
    "failure": {"reason": None, "category": None},
    "history": [{"timestamp": "2026-08-02T00:00:00Z", "event": "change-created", "actor": "human"}],
}


def test_parses_valid_state_and_aliases_class_field() -> None:
    state = ChangeState.model_validate(_VALID)

    assert state.change.change_class == "M"
    assert state.flow.status == "draft"
    assert len(state.history) == 1
    assert state.history[0].event == "change-created"


def test_gates_block_is_preserved_untyped_when_present() -> None:
    data = {**_VALID, "gates": {"current": {"definition": "DoD", "result": "pending"}}}

    state = ChangeState.model_validate(data)

    assert state.gates == {"current": {"definition": "DoD", "result": "pending"}}
