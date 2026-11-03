"""The engine of the `core` profile: the transition table of Section 23.4 as pure logic.

`apply` takes the state, a request, the context (roles and gates), the facts the caller observed,
and a runner for check commands. It returns an `ActionResult`: the result (Section 22.2), the
issues, the state after, and the entry bodies to append. It reads no clock and no file and starts
no process; the store appends the bodies. The handlers live in `engine_actions`.
"""

from __future__ import annotations

from typing import Final

from ggsad.core.engine_actions import HANDLERS
from ggsad.core.engine_types import (
    ActionResult,
    Call,
    Context,
    Rejected,
    Request,
    Step,
)
from ggsad.core.gate_eval import Facts, Runner
from ggsad.core.state import State

HUMAN_ONLY: Final = frozenset(
    {"approve", "fail", "cancel", "supersede", "adopt", "repair", "handover", "reassign", "answer"}
)
REQUESTOR_ACTIONS: Final = frozenset({"new", "start", "ask", "wait", "conflict", "resume", "close"})
HUMAN_MAY: Final = frozenset({"resume", "close"})
ANY_STATE: Final = frozenset({"open", "active", "waiting"})
LEGAL_FROM: Final[dict[str, frozenset[str]]] = {
    "approve": ANY_STATE,
    "start": frozenset({"open"}),
    "wait": frozenset({"active"}),
    "ask": ANY_STATE,
    "answer": ANY_STATE,
    "resume": frozenset({"waiting"}),
    "close": frozenset({"active"}),
    "fail": frozenset({"waiting"}),
    "cancel": ANY_STATE,
    "supersede": ANY_STATE,
    "adopt": ANY_STATE | {"closed"},
    "conflict": frozenset({"active"}),
    "handover": ANY_STATE,
    "reassign": ANY_STATE,
    "repair": ANY_STATE | {"closed"},
}


def apply(
    state: State | None, request: Request, context: Context, facts: Facts, runner: Runner
) -> ActionResult:
    """Apply one action. A bad request answers `rejected`; it never raises."""
    current = state if state is not None else State()
    call = Call(request, current, context, facts, runner)
    try:
        _check_access(call, is_new=state is None)
        step = HANDLERS[request.action](call)
    except Rejected as rejection:
        return ActionResult(request.action, "rejected", (rejection.issue,), current)
    return _finish(call, step)


def _check_access(call: Call, *, is_new: bool) -> None:
    request = call.request
    if request.action not in HANDLERS:
        raise Rejected("action-unknown", f"{request.action!r} is not an action of this method")
    if (request.action == "new") != is_new:
        if is_new:
            raise Rejected("change-missing", "the change does not exist")
        raise Rejected("change-exists", "the change exists already")
    if not is_new and call.state.state not in LEGAL_FROM[request.action]:
        raise Rejected(
            "state-illegal",
            f"the action {request.action!r} is not legal from the state {call.state.state!r}",
        )
    _check_actor(call)
    for code, message in call.facts.target_issues.get(request.action, ()):
        raise Rejected(code, message)


def _check_actor(call: Call) -> None:
    action, actor = call.request.action, call.request.actor
    if action in HUMAN_ONLY and not actor.is_human:
        raise Rejected("human-required", f"the action {action!r} must be performed by a human")
    if action not in REQUESTOR_ACTIONS:
        return
    if actor.is_human and action not in HUMAN_MAY:
        raise Rejected("requestor-not-approved", "there is no human Requestor in version 1")
    if not actor.is_human and actor.identity not in call.context.requestors:
        raise Rejected("requestor-not-approved", f"{actor.identity} is not a listed Requestor")


def _finish(call: Call, step: Step) -> ActionResult:
    bodies = [_body(call, step)]
    state, result = step.state, step.result
    if step.chained is not None:
        bodies.append(_body(call, step.chained))
        state, result = step.chained.state, step.chained.result
    return ActionResult(
        call.request.action, result, step.issues, state, tuple(bodies), dict(step.data)
    )


def _body(call: Call, step: Step) -> dict[str, object]:
    request, evaluation = call.request, step.evaluation
    files = step.files or request.files
    body: dict[str, object] = {
        "action": step.action or request.action,
        "actor": request.actor.identity,
        "account": request.actor.account,
        "assurance": request.actor.assurance,
        "at": request.at,
        "result": step.result,
        "gate_results": dict(evaluation.results) if evaluation else None,
        "gate_detail": (dict(evaluation.details) or None) if evaluation else None,
        "files": dict(files) if files else None,
        "note": request.note if request.note is not None else request.reason,
        "after": step.state.to_json(),
    }
    body.update(_extra_fields(request))
    return body


def _extra_fields(request: Request) -> dict[str, object]:
    if request.action == "close" and request.agent_report is not None:
        return {"agent_report": dict(request.agent_report)}
    if request.action == "repair":
        return {"repaired": dict(request.repaired or {})}
    return {}
