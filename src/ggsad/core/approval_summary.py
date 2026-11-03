"""The approval summary (Section 24.1, AE-319): what a human sees before an approval is recorded.

It is read-only. The lines come in this order: what a re-approval would invalidate (overrides that
would lapse, sign-offs that would become stale), what changed since the last approval, the fail
gates with their severity, the retry limits, the rules the implementation enforces and those that
are conduct only (Section 19.1), the team mode, and whether an anchor is set.

Interpretations fixed here (listed in the pull request):
- what changed is shown from the hashes and the document fingerprint that the history records;
  the earlier text of the gate definitions is not kept, so a diff of gates is not shown.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ggsad.core.guards import approved_hash, recorded_documents

if TYPE_CHECKING:
    from ggsad.core.gate_model import Gate
    from ggsad.core.loader import LoadedChange
    from ggsad.core.settings import Settings
    from ggsad.core.state import Approval, State

ENFORCED: Final = (
    "the scope",
    "the gates",
    "the human-only actions",
    "the frozen gate definitions",
    "the history",
    "the open questions",
    "the executable evidence",
)
CONDUCT: Final = (
    "inventing goals, requirements, or approvals",
    "taking missing information as consent",
    "silently changing higher-ranking documents",
    "breaking changes without approval",
    "bypassing wait states through speculation",
    "marking a flow done when evidence is missing",
    "concealing errors",
    "working beyond the approved scope",
)
SHORT: Final = 12


def _short(digest: str | None) -> str:
    return (digest or "none")[:SHORT]


def _lapse_line(approval: Approval) -> str | None:
    left = (approval.attempts or 0) - approval.used
    if approval.target == "override" and left > 0:
        return (
            f"the override of {approval.gate} lapses with {left} attempt(s) left; "
            "the change would pause again"
        )
    if approval.target == "gate":
        return f"the sign-off of {approval.gate} becomes stale"
    return None


def _invalidated(loaded: LoadedChange, state: State) -> list[str]:
    """Overrides that would lapse and sign-offs that would become stale by a re-approval."""
    now = loaded.facts.definitions_hash
    old = approved_hash(state)
    if old is None or old == now:
        return []
    stale = [a for a in state.approvals if a.definitions_hash not in (None, now)]
    lines = [_lapse_line(a) for a in stale]
    return [line for line in lines if line is not None]


def _gate_part(loaded: LoadedChange, state: State) -> list[str]:
    old, now = approved_hash(state), loaded.facts.definitions_hash
    if old is None or old == now:
        return []
    return [f"the gate definitions (approved {_short(old)}, now {_short(now)})"]


def _spec_part(loaded: LoadedChange, state: State) -> list[str]:
    spec = [a for a in state.approvals if a.target == "spec"]
    current = loaded.facts.spec_hash
    return ["spec.md"] if spec and current is not None and spec[-1].content_hash != current else []


def _document_part(loaded: LoadedChange, state: State) -> list[str]:
    recorded = recorded_documents(state)
    if recorded is None:
        return []
    current = dict(loaded.facts.documents)
    return sorted(p for p in {*recorded, *current} if recorded.get(p) != current.get(p))


def _changed_parts(loaded: LoadedChange, state: State) -> list[str]:
    return _gate_part(loaded, state) + _spec_part(loaded, state) + _document_part(loaded, state)


def _changes(loaded: LoadedChange, state: State) -> str:
    if not state.approvals:
        return "changed since the last approval: first approval"
    parts = _changed_parts(loaded, state)
    return "changed since the last approval: " + (", ".join(parts) if parts else "nothing")


def _fail_gates(gates: tuple[Gate, ...], settings: Settings) -> list[str]:
    lines: list[str] = []
    for gate in gates:
        if gate.group != "fail":
            continue
        softer = gate.severity == "soft" and settings.fail_severity == "hard"
        flag = f" (softer than the default {settings.fail_severity})" if softer else ""
        lines.append(f"fail gate {gate.id}: {gate.severity}{flag}")
    return lines


def _retry_limits(gates: tuple[Gate, ...], settings: Settings) -> list[str]:
    lines = [f"retry limit of {g.retry_gate}: {g.limit}" for g in gates if g.kind == "retry_limit"]
    return [*lines, f"default retry limit: {settings.retry_limit}"]


def build_summary(loaded: LoadedChange, settings: Settings) -> list[str]:
    """The lines of the approval summary for the change as it is now."""
    state = loaded.state
    if state is None:
        return []
    lines = _invalidated(loaded, state)
    lines.append(_changes(loaded, state))
    lines.extend(_fail_gates(loaded.context.gates, settings))
    lines.extend(_retry_limits(loaded.context.gates, settings))
    lines.append("the implementation enforces: " + ", ".join(ENFORCED))
    lines.append("conduct only: " + ", ".join(CONDUCT))
    lines.append(f"team_mode: {settings.team_mode}")
    lines.append(f"anchor: {'set' if loaded.facts.has_anchor else 'not set'}")
    return lines
