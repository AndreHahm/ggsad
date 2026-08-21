"""Unit tests for the typed ChangeState model."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import ValidationError

from ggsad.models.state import ChangeState

_VALID: dict[str, Any] = {
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


@pytest.mark.parametrize("status", ["failed", "cancelled", "superseded"])
def test_terminal_status_requires_closed_phase(status: str) -> None:
    data = {**_VALID, "flow": {**_VALID["flow"], "status": status}}

    with pytest.raises(ValidationError, match="closed phase"):
        ChangeState.model_validate(data)


@pytest.mark.parametrize("status", ["draft", "ready", "active", "waiting"])
def test_closed_phase_rejects_nonterminal_status(status: str) -> None:
    data = {**_VALID, "flow": {**_VALID["flow"], "phase": "closed", "status": status}}

    with pytest.raises(ValidationError, match="terminal status"):
        ChangeState.model_validate(data)


def test_removed_design_phase_is_rejected() -> None:
    data = {**_VALID, "flow": {**_VALID["flow"], "phase": "design"}}

    with pytest.raises(ValidationError, match="phase"):
        ChangeState.model_validate(data)


def test_closed_phase_is_rejected_as_resume_target() -> None:
    data = {**_VALID, "wait": {**_VALID["wait"], "resume_phase": "closed"}}

    with pytest.raises(ValidationError, match="resume_phase"):
        ChangeState.model_validate(data)
