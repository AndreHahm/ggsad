"""The typed `after` record: AE-014, AE-082 (outcome only when closed, reason when failed)."""

from __future__ import annotations

import contextlib
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ggsad.core.state import Approval, Question, State, StateRecordError, Wait


def record(**override: Any) -> dict[str, Any]:
    data = State().to_json()
    data.update(override)
    return data


def test_ae014_new_state_is_open_with_null_outcome() -> None:
    state = State()
    assert (state.state, state.outcome, state.wait, state.base_revision) == (
        "open",
        None,
        None,
        None,
    )
    assert state.approvals == () and state.questions == ()


def test_round_trip_keeps_every_field() -> None:
    state = State(
        state="waiting",
        approvals=(
            Approval("override", "human:ada", "A1", "A1", gate="flaky", reason="r", attempts=2),
        ),
        questions=(Question("Q1", "keep?", "human:ada", "agent:x", options=("keep", "drop")),),
        wait=Wait("question", "awaiting Q1", "human:ada", "Q1 answered", question="Q1"),
        base_revision="abc",
    )
    assert State.from_json(state.to_json()) == state


def test_ae082_failed_outcome_needs_a_reason() -> None:
    with pytest.raises(StateRecordError):
        State.from_json(record(state="closed", outcome="failed"))
    ok = State.from_json(record(state="closed", outcome="failed", reason="retry limit reached"))
    assert ok.reason == "retry limit reached"


@pytest.mark.parametrize(
    "bad",
    [
        {"state": "closed"},  # closed without outcome
        {"outcome": "done"},  # outcome while open
        {"state": "waiting"},  # waiting without wait record
        {"reason": "x"},  # reason without failed
        {"state": "paused"},
        {"extra": 1},
        {"approvals": "none"},
        {"questions": [{"id": "Q1"}]},
        {"schema_version": None},
    ],
)
def test_invalid_records_are_refused(bad: dict[str, Any]) -> None:
    with pytest.raises(StateRecordError):
        State.from_json(record(**bad))


def test_missing_field_is_refused() -> None:
    data = record()
    del data["wait"]
    with pytest.raises(StateRecordError):
        State.from_json(data)


def test_question_helpers() -> None:
    q1 = Question("Q1", "t", "human:ada", "agent:x")
    q2 = Question("Q2", "t", "human:ada", "agent:x", answer="yes", answerer="human:ada")
    state = State(questions=(q1, q2))
    assert state.unanswered == (q1,)
    assert state.question("Q2") == q2
    assert state.question("q2") is None


@given(
    st.recursive(
        st.none() | st.booleans() | st.integers() | st.text(),
        lambda c: st.lists(c) | st.dictionaries(st.text(), c),
        max_leaves=8,
    )
)
def test_from_json_never_raises_anything_but_state_record_error(value: object) -> None:
    with contextlib.suppress(StateRecordError):
        State.from_json(value)
