"""Typed view of `specs/<change-id>/state.yaml` (GG-SAD change state).

Mirrors the required shape of `.ggsad/schemas/state.schema.json`. `history`
is fully typed as a list of :class:`HistoryEvent`, since R-014 (append
transition history) needs typed construction, not just passthrough. The
optional `gates` block is left untyped (`dict[str, Any] | None`): the
criterion/gate engine is explicitly out of CHG-001 scope (ADR-0008), so
there is no current consumer for a fully modeled `GateState`.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ChangeIdentity(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow", populate_by_name=True)

    id: str
    slug: str
    title: str
    change_class: str = Field(alias="class")


class FlowState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    profile: str
    phase: str
    status: str
    owner: str | None = None


class GoalSummary(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    summary: str
    success_signals: list[str] | None = None
    non_goals: list[str] | None = None


class ArtifactPaths(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    spec: str | None = None
    plan: str | None = None
    tasks: str | None = None
    evidence: str | None = None
    review: str | None = None


class PairReviewParticipant(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    id: str
    type: str


class PairReviewState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    required: bool
    status: str
    requestor: PairReviewParticipant | None = None
    reviewer: PairReviewParticipant | None = None
    review_id: str | None = None
    scope: list[str] | None = None
    open_blocking_findings: int | None = None


class WaitState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    reason: str | None = None
    category: str | None = None
    owner: str | None = None
    resume_condition: str | None = None
    safe_state: str | None = None
    resume_phase: str | None = None
    next_action: str | None = None
    created_at: str | None = None


class FailureState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    reason: str | None = None
    category: str | None = None
    required_response: str | None = None
    safe_state: str | None = None
    evidence: list[str] | None = None


class HistoryEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    timestamp: str
    event: str
    actor: str
    action: str | None = None
    previous_phase: str | None = None
    previous_status: str | None = None
    new_phase: str | None = None
    new_status: str | None = None
    reason: str | None = None
    evidence: list[str] | None = None


class ChangeState(BaseModel):
    """Typed view of a change's `state.yaml`."""

    model_config = ConfigDict(frozen=True, extra="allow")

    schema_version: str
    change: ChangeIdentity
    flow: FlowState
    goal: GoalSummary
    artifacts: ArtifactPaths
    pair_review: PairReviewState
    wait: WaitState
    failure: FailureState
    history: list[HistoryEvent] = Field(default_factory=list)
    gates: dict[str, Any] | None = None


def dump_change_state(state: ChangeState) -> dict[str, Any]:
    """Serialize `state` to a `state.schema.json`-conformant dict.

    `model_dump()` alone isn't enough: most optional fields in the schema
    (e.g. `failure.evidence`, `history[].action`) are typed without `null`
    in their union, so an unset field must be *omitted*, not dumped as
    `null`. But a few blocks are the opposite -- `wait`, `failure.reason`/
    `failure.category`, and `pair_review.requestor`/`reviewer` are
    *required keys* that must stay present even when their value is null
    (see the CHG-001 `state.yaml` convention this mirrors). `exclude_none`
    handles the first case; the required-nullable keys are restored after.

    Shared by `create_change.py` (new state.yaml) and `engine/transitions.py`
    (state.yaml after a transition) -- both serialize a `ChangeState` back
    to disk and need the same schema-conformance handling.
    """
    data = state.model_dump(by_alias=True, exclude_none=True)

    wait = data.setdefault("wait", {})
    for key in (
        "reason",
        "category",
        "owner",
        "resume_condition",
        "safe_state",
        "resume_phase",
        "next_action",
    ):
        wait.setdefault(key, None)

    failure = data.setdefault("failure", {})
    for key in ("reason", "category"):
        failure.setdefault(key, None)

    pair_review = data.setdefault("pair_review", {})
    for key in ("requestor", "reviewer"):
        pair_review.setdefault(key, None)

    return data
