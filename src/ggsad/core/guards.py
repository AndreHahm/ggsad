"""The protections that stop an action before its handler runs (Sections 4, 24.1, and 24.3).

Each check raises `Rejected` with a stable issue code, and nothing is written.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ggsad.core.engine_types import Call, Rejected
from ggsad.core.gate_eval import LEVEL_ORDER

if TYPE_CHECKING:
    from ggsad.core.state import State

KIND_OF_TARGET: Final = {
    "spec": "spec_approval",
    "gates": "gate_approval",
    "amendment": "gate_approval",
    "review": "review_approval",
    "documents": "documents_approval",
    "gate": "sign_off",
    "override": "override",
}
KIND_OF_ACTION: Final = {
    "answer": "answer",
    "cancel": "cancel",
    "supersede": "cancel",
    "fail": "fail",
    "adopt": "adopt",
    "repair": "repair",
}
SAME_PERSON_ALLOWED: Final = {
    "lean": ("team", "solo"),
    "standard": ("solo",),
    "governed": ("solo",),
    "regulated": (),
}
FROZEN_EXEMPT: Final = frozenset({"cancel", "supersede"})
HUMAN_ONLY: Final = frozenset(
    {"approve", "fail", "cancel", "supersede", "adopt", "repair", "handover", "reassign", "answer"}
)


def approved_hash(state: State) -> str | None:
    """The approved hash of the gate definitions: the latest approval or amendment of them."""
    for approval in reversed(state.approvals):
        if approval.target in ("gates", "amendment"):
            return approval.content_hash
    return None


def recorded_documents(state: State) -> dict[str, str] | None:
    """The fingerprint of the higher documents recorded last, or None before any approval."""
    for approval in reversed(state.approvals):
        if approval.target in ("spec", "documents"):
            return dict(approval.documents)
    return None


def check_guards(call: Call) -> None:
    """Run every protection that applies to the requested action."""
    _check_listed(call)
    _check_frozen_gates(call)
    _check_higher_documents(call)
    _check_assurance(call)
    if call.request.action == "approve":
        _check_approver(call)


def _check_listed(call: Call) -> None:
    actor, listed = call.request.actor, call.context.approved_humans
    required = call.request.action in HUMAN_ONLY and actor.is_human
    if required and listed is not None and actor.identity not in listed:
        raise Rejected("human-not-approved", f"{actor.identity} is not an approved human")


def _is_replacement(call: Call) -> bool:
    """True for the approval of the gate definitions that replaces the approved hash."""
    request = call.request
    return request.action == "approve" and request.target in ("gates", "all")


def _check_frozen_gates(call: Call) -> None:
    action = call.request.action
    approved = approved_hash(call.state)
    if approved is None or action in FROZEN_EXEMPT or _is_replacement(call):
        return
    if call.facts.definitions_hash != approved:
        raise Rejected(
            "gates-changed",
            "the gate definitions differ from the approved ones; a human has to approve them again",
        )


def _check_higher_documents(call: Call) -> None:
    request = call.request
    recorded = recorded_documents(call.state)
    if recorded is None or request.action == "cancel":
        return
    if request.action == "approve" and request.target == "documents":
        return
    current = dict(call.facts.documents)
    changed = sorted(p for p in {*recorded, *current} if recorded.get(p) != current.get(p))
    if changed:
        raise Rejected(
            "higher-documents-changed",
            "these higher-ranking documents changed: " + ", ".join(changed),
        )


def _history_level(state: State, kind: str) -> int:
    levels = [
        LEVEL_ORDER.get(a.required_level, 0)
        for a in state.approvals
        if KIND_OF_TARGET.get(a.target) == kind
    ]
    return max(levels, default=0)


def _kinds(call: Call) -> tuple[str, ...]:
    request = call.request
    if request.action == "approve":
        if request.target == "all":
            return ("spec_approval", "gate_approval")
        kind = KIND_OF_TARGET.get(request.target or "")
        return (kind,) if kind else ()
    kind = KIND_OF_ACTION.get(request.action)
    return (kind,) if kind else ()


def _gate_minimum(call: Call) -> int:
    request = call.request
    if request.action != "approve" or request.target != "gate":
        return 0
    gate = next((g for g in call.context.gates if g.id == request.gate), None)
    return LEVEL_ORDER.get(gate.minimum_level or "A0", 0) if gate else 0


def required_level(call: Call) -> str:
    """The required level: the highest of the settings, the gate, and the history (Section 24.3)."""
    levels = [_gate_minimum(call)]
    for kind in _kinds(call):
        levels.append(LEVEL_ORDER.get(call.context.minimum_levels.get(kind, "A0"), 0))
        levels.append(_history_level(call.state, kind))
    top = max(levels)
    return next(name for name, rank in LEVEL_ORDER.items() if rank == top)


def _check_assurance(call: Call) -> None:
    if not _kinds(call):
        return
    needed = required_level(call)
    verified = call.request.actor.assurance
    if LEVEL_ORDER.get(verified, 0) < LEVEL_ORDER[needed]:
        raise Rejected(
            "assurance-too-low", f"the action needs the level {needed}; the claim is at {verified}"
        )


def approvers(call: Call) -> set[str]:
    """Who may give an approval (Section 3.11): the Approver, a deputy for an absent Approver."""
    context = call.context
    approver = context.approver or context.change_owner
    allowed = {approver}
    if approver in context.unavailable_approvers:
        allowed |= context.deputies
    if _is_replacement(call):
        allowed |= {context.owner, *context.deputies}
    return allowed


def _check_approver(call: Call) -> None:
    request, context = call.request, call.context
    if request.target == "review":
        return
    actor = request.actor.identity
    if actor not in approvers(call):
        raise Rejected("not-approver", f"{actor} is not the Approver of this change")
    allowed = SAME_PERSON_ALLOWED.get(context.compliance_profile, ())
    if actor == context.author and context.team_mode not in allowed:
        raise Rejected(
            "roles-not-separate",
            "the Author cannot also approve under "
            f"{context.compliance_profile} in {context.team_mode} mode",
        )
