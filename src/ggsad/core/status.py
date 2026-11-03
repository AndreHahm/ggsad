"""The status report of a change (Section 23.8). It reads, it writes nothing, it runs nothing.

The report starts with one line for the owner: `needs you`, `waiting on others`, or `all fine`.
Then come the state, the recorded gate results, who must act for every pending item, and the
warnings. No warning blocks anything.

Interpretations fixed here (listed in the pull request):
- the gate results shown are the ones the history recorded last; the report does not run commands;
- a pending item needs the owner when its actor is a `human:` identity, and others otherwise;
- a wait of the kind `external` is `ready to resume` when the program of its gate can be found;
- a fallback is reported for the Approver (none named or not on the list), and for a missing
  Author or Change owner.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Final

from ggsad.core.engine_actions import wait_gate
from ggsad.core.gate_eval import SATISFIED, override_in_force
from ggsad.core.guards import approved_hash
from ggsad.core.issues import Issue
from ggsad.core.loader import DEFINITION_FILE, change_path, existing_ids
from ggsad.core.project import missing_documents, read_yaml_file
from ggsad.core.state import State
from ggsad.core.values import as_mapping

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from ggsad.core.gate_model import Gate
    from ggsad.core.loader import LoadedChange
    from ggsad.core.runner import CommandRunner
    from ggsad.core.settings import Settings
    from ggsad.core.state import Approval, Wait

NEEDS_YOU: Final = "needs you"
WAITING: Final = "waiting on others"
ALL_FINE: Final = "all fine"
HUMAN: Final = "human:"


@dataclass(frozen=True)
class Pending:
    """One item that someone must act on."""

    kind: str
    id: str
    actor: str
    detail: str

    def to_json(self) -> dict[str, str]:
        """The item as a JSON object."""
        return {"kind": self.kind, "id": self.id, "actor": self.actor, "detail": self.detail}


@dataclass(frozen=True)
class StatusReport:
    """What the status report shows."""

    headline: str
    state: str
    outcome: str | None
    gate_results: Mapping[str, str]
    pending: tuple[Pending, ...]
    warnings: tuple[Issue, ...]
    gates_enforced: bool
    closed: Mapping[str, object]

    def to_json(self) -> dict[str, object]:
        """The report as a JSON object."""
        return {
            "headline": self.headline,
            "state": self.state,
            "outcome": self.outcome,
            "gate_results": dict(self.gate_results),
            "pending": [p.to_json() for p in self.pending],
            "warnings": [{"code": w.code, "message": w.message} for w in self.warnings],
            "gates_enforced": self.gates_enforced,
            "closed": dict(self.closed),
        }


def _moment(text: str | None) -> datetime | None:
    if text is None:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _is_before(earlier: str | None, now: str) -> bool:
    a, b = _moment(earlier), _moment(now)
    return a is not None and b is not None and a < b


def latest_results(bodies: Sequence[Mapping[str, object]]) -> dict[str, str]:
    """The gate results of the latest entry that recorded any."""
    for body in reversed(bodies):
        results = as_mapping(body.get("gate_results"))
        if results:
            return {str(k): str(v) for k, v in results.items()}
    return {}


def _approver_pending(loaded: LoadedChange, state: State) -> list[Pending]:
    approver = loaded.context.approver
    items: list[Pending] = []
    targets = {a.target for a in state.approvals}
    if (
        state.state == "open"
        and loaded.facts.definitions_hash is not None
        and not loaded.facts.gates_approved
    ):
        items.append(Pending("approval", "gates", approver, "the gate definitions await approval"))
    if state.state == "open" and not loaded.facts.spec_approval_ok and "spec" not in targets:
        items.append(Pending("approval", "spec", approver, "the specification awaits approval"))
    return items


def _sign_offs(loaded: LoadedChange, state: State) -> list[Pending]:
    if state.state != "active":
        return []
    signed = {a.gate for a in state.approvals if a.target == "gate"}
    return [
        Pending("sign-off", g.id, loaded.context.approver, f"the sign-off {g.id!r} is due")
        for g in loaded.context.gates
        if g.group == "done" and g.kind == "sign-off" and g.id not in signed
    ]


def _questions(state: State) -> list[Pending]:
    return [Pending("question", q.id, q.owner, q.text) for q in state.unanswered]


def _wait(state: State) -> list[Pending]:
    wait = state.wait
    if wait is None:
        return []
    return [Pending("wait", wait.kind, wait.owner, wait.reason)]


def _soft_failures(loaded: LoadedChange, state: State, results: Mapping[str, str]) -> list[Pending]:
    owner = loaded.context.change_owner or loaded.context.owner
    return [
        Pending("soft-failure", g.id, owner, f"the soft failure {g.id!r} awaits a disposition")
        for g in loaded.context.gates
        if g.group == "fail"
        and g.severity == "soft"
        and results.get(g.id) == SATISFIED
        and override_in_force(state, g.id, loaded.facts) is None
        and state.state != "closed"
    ]


def pending_items(loaded: LoadedChange, results: Mapping[str, str]) -> tuple[Pending, ...]:
    """Everything that waits for someone, in a fixed order."""
    state = loaded.state
    if state is None or state.closed:
        return ()
    return (
        *_approver_pending(loaded, state),
        *_sign_offs(loaded, state),
        *_questions(state),
        *_wait(state),
        *_soft_failures(loaded, state, results),
    )


def headline(pending: Sequence[Pending]) -> str:
    """The one line for the owner."""
    if any(p.actor.startswith(HUMAN) for p in pending):
        return NEEDS_YOU
    return WAITING if pending else ALL_FINE


# ---------------------------------------------------------------- warnings


def _warn(code: str, message: str) -> Issue:
    return Issue(code, message)


def _wait_warnings(loaded: LoadedChange, runner: CommandRunner, now: str) -> list[Issue]:
    state = loaded.state
    wait = state.wait if state is not None else None
    if state is None or wait is None:
        return []
    found: list[Issue] = []
    if _is_before(wait.expires, now):
        found.append(_warn("wait-overdue", f"the wait is overdue; {wait.owner} must act"))
    found.extend(_external_ready(loaded, wait, runner))
    found.extend(_answered_by_other(loaded, state))
    return found


def _external_ready(loaded: LoadedChange, wait: Wait, runner: CommandRunner) -> list[Issue]:
    if wait.kind != "external":
        return []
    gate = next((g for g in loaded.context.gates if g.id == wait_gate(wait)), None)
    if gate is None or gate.command is None:
        return []
    if not runner.program_exists(gate.command.command[0]):
        return []
    return [_warn("ready-to-resume", "the cause may be gone, ready to resume")]


def _may_resume(loaded: LoadedChange, wait: Wait, answerer: str) -> bool:
    return loaded.context.is_approved_human(answerer) or answerer == wait.owner


def _answered_by_other(loaded: LoadedChange, state: State) -> list[Issue]:
    wait = state.wait
    if wait is None or wait.kind != "question":
        return []
    question = state.question(wait.question or "")
    if question is None or not question.answered:
        return []
    if _may_resume(loaded, wait, question.answerer or ""):
        return []
    message = f"ready to resume; {wait.owner} or an approved human can resume"
    return [_warn("ready-to-resume", message)]


def _role_warnings(loaded: LoadedChange, settings: Settings) -> list[Issue]:
    definition = loaded.definition or {}
    found: list[Issue] = []
    if definition.get("approver") != loaded.context.approver:
        found.append(_warn("fallback-role", "no Approver is named; the Owner is the Approver"))
    found.extend(
        _warn("fallback-role", f"the change names no {role}; a fallback is used")
        for role in ("author", "owner")
        if not definition.get(role)
    )
    return found + _settings_warnings(settings)


def _settings_warnings(settings: Settings) -> list[Issue]:
    found: list[Issue] = []
    if settings.approved_humans is None:
        found.append(_warn("no-approved-list", "no list of approved humans is set"))
    if settings.team_mode == "solo":
        found.append(_warn("solo-mode", "team_mode is solo"))
    if not settings.deputies:
        found.append(_warn("no-deputy", "no deputy exists"))
    return found


def _approval_warning(approval: Approval, now_hash: str | None) -> Issue | None:
    if approval.definitions_hash in (None, now_hash):
        return None
    if approval.target == "gate":
        return _warn("sign-off-stale", f"the sign-off of {approval.gate} is stale")
    if approval.target == "override" and approval.used < (approval.attempts or 0):
        return _warn("override-lapses", f"the override of {approval.gate} would lapse")
    return None


def _approval_warnings(loaded: LoadedChange) -> list[Issue]:
    if loaded.state is None:
        return []
    now_hash = loaded.facts.definitions_hash
    found = [_approval_warning(a, now_hash) for a in loaded.state.approvals]
    return [w for w in found if w is not None]


def _baseline_warnings(gates: Sequence[Gate], now: str) -> list[Issue]:
    today = now[:10]
    return [
        _warn(
            "baseline-review-overdue",
            f"the baseline entry {e.id!r} of {g.id} is past {e.review_by}",
        )
        for g in gates
        for e in g.baseline or ()
        if e.review_by and e.review_by < today
    ]


def _human_close_without_report(bodies: Sequence[Mapping[str, object]]) -> bool:
    closes = [b for b in bodies if b.get("action") == "close"]
    if not closes:
        return False
    return str(closes[-1].get("actor", "")).startswith(HUMAN) and "agent_report" not in closes[-1]


def _history_warnings(loaded: LoadedChange) -> list[Issue]:
    found: list[Issue] = []
    if not loaded.facts.has_anchor:
        found.append(
            _warn("no-anchor", "no anchor is set; the history protects against accident only")
        )
    scope = loaded.facts.scope
    if scope is not None and scope.result == SATISFIED:
        found.append(_warn("scope-violation", scope.detail))
    if _human_close_without_report(loaded.bodies):
        found.append(_warn("no-agent-report", "a human closed the change without an agent report"))
    return found


def collect_warnings(
    root_missing: Sequence[str],
    loaded: LoadedChange,
    settings: Settings,
    runner: CommandRunner,
    now: str,
) -> tuple[Issue, ...]:
    """All warnings that apply (Section 23.8)."""
    found = [
        _warn("document-missing", f"the required document {p} is missing") for p in root_missing
    ]
    found += _wait_warnings(loaded, runner, now)
    found += _role_warnings(loaded, settings)
    found += _approval_warnings(loaded)
    found += _baseline_warnings(loaded.context.gates, now)
    found += _history_warnings(loaded)
    interpreter = runner.interpreter_warning()
    if interpreter is not None:
        found.append(_warn("interpreter-in-repository", interpreter))
    return tuple(found)


def followers(root: Path, change_id: str, names: Sequence[str]) -> list[str]:
    """The changes whose `follows` names this change."""
    found: list[str] = []
    for name in names:
        value, issue = read_yaml_file(change_path(root, name) / DEFINITION_FILE, "definition")
        mapping = as_mapping(value)
        if issue is None and mapping is not None and mapping.get("follows") == change_id:
            found.append(name)
    return found


def build_status(
    root: Path,
    settings: Settings,
    loaded: LoadedChange,
    runner: CommandRunner,
    now: str,
) -> StatusReport:
    """The status report of a loaded change."""
    state = loaded.state or State()
    results = latest_results(loaded.bodies)
    pending = pending_items(loaded, results)
    missing = missing_documents(root, settings.compliance_profile)
    approved = approved_hash(state)
    closed: dict[str, object] = {}
    if state.closed:
        closed = {
            "reason": state.reason,
            "replaced_by": state.replaced_by,
            "followed_by": followers(root, loaded.change_id, existing_ids(root)),
        }
    return StatusReport(
        headline(pending),
        state.state,
        state.outcome,
        results,
        pending,
        collect_warnings(missing, loaded, settings, runner, now),
        approved is None or approved == loaded.facts.definitions_hash,
        closed,
    )
