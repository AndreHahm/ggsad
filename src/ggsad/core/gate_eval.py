"""Gate evaluation of the `core` profile (Sections 23.6, 23.7, 24.2, and 24.7).

The engine is pure: commands are run by a runner that the caller hands in, and the results of the
checks that need files or version control (scope, stale specification approval, evidence, review
reports) are handed in as `Facts`. Nothing here reads a clock, a file, or a process.

Interpretations fixed here (listed in the pull request):
- a retry limit is checked against the `not_satisfied` results already in the history, before the
  done gates run, so the limit is reached when the count is greater than or equal to it;
- the implicit retry limit of a done `check` gate is evaluated under the key `<gate>#retry-limit`;
- a base-gate result that the caller does not hand in is `not_evaluable`, never a pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final, Literal

from ggsad.core.gates import DEFAULT_RETRY_LIMIT
from ggsad.core.values import as_int, as_list, as_mapping, as_text, text_list

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

    from ggsad.core.state import Approval, State

SATISFIED: Final = "satisfied"
NOT_SATISFIED: Final = "not_satisfied"
NOT_EVALUABLE: Final = "not_evaluable"
NOT_APPLICABLE: Final = "not_applicable"
LEVEL_ORDER: Final = {"A0": 0, "A1": 1, "A2": 2}
# Which groups of gates an action evaluates (Section 23.6).
GROUPS_FOR: Final[dict[str, tuple[str, ...]]] = {
    "close": ("fail", "wait", "done"),
    "resume": ("fail", "wait"),
    "start": ("fail", "wait"),
    "cancel": ("fail",),
    "supersede": ("fail",),
}
ALL_GROUPS: Final = ("fail", "wait", "done")


@dataclass(frozen=True)
class ExitMap:
    """The exit statuses that mean each result of a check command (Section 24.2)."""

    satisfied: frozenset[int] = frozenset()
    not_satisfied: frozenset[int] = frozenset()
    not_evaluable: frozenset[int] = frozenset()

    def result_for(self, status: int) -> str:
        """The result of an exit status; a status that is not mapped is not evaluable."""
        if status in self.satisfied:
            return SATISFIED
        if status in self.not_satisfied:
            return NOT_SATISFIED
        return NOT_EVALUABLE


@dataclass(frozen=True)
class CommandSpec:
    """A check command: argument list, exit map, and an optional time limit in seconds."""

    command: tuple[str, ...]
    exit_map: ExitMap
    time_limit: int | None = None


@dataclass(frozen=True)
class Gate:
    """One gate. `kind` is the done-gate kind or the member of a condition of a fail/wait gate."""

    id: str
    group: str
    kind: str
    severity: str | None = None
    command: CommandSpec | None = None
    retry_gate: str | None = None
    limit: int | None = None
    predicate: str | None = None
    minimum_level: str | None = None


@dataclass(frozen=True)
class RunOutcome:
    """What a runner reports about one command. The engine decides what it means."""

    kind: Literal["exit", "timeout", "cannot-start", "no-status"]
    status: int | None = None
    cause: str = ""
    program_missing: bool = False


type Runner = Callable[[tuple[str, ...], int | None], RunOutcome]


@dataclass(frozen=True)
class Check:
    """A result handed in by the caller for a check that needs files or version control."""

    result: str
    detail: str = ""


@dataclass(frozen=True)
class Facts:
    """What the caller observed. A fact that is not handed in is `not_evaluable`."""

    scope: Check | None = None
    stale_spec_approval: Check | None = None
    evidence: Check | None = None
    review_gaps: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    not_satisfied_counts: Mapping[str, int] = field(default_factory=dict)
    definitions_hash: str | None = None
    gates_approved: bool = False
    spec_approval_ok: bool = True
    revision: str | None = None
    unclean_paths: tuple[str, ...] = ()
    target_issues: Mapping[str, tuple[tuple[str, str], ...]] = field(default_factory=dict)
    open_changes: frozenset[str] = frozenset()
    has_anchor: bool = False
    history_damaged: bool = False


@dataclass(frozen=True)
class Outcome:
    """The result and detail of one gate evaluation."""

    result: str
    detail: str = ""


@dataclass(frozen=True)
class Decision:
    """What the results decide (Section 24.2): fail, external, soft, wait, done, or none."""

    kind: str = "none"  # none, fail, external, soft, wait, or done
    gate_ids: tuple[str, ...] = ()
    detail: str = ""


@dataclass(frozen=True)
class Evaluation:
    """The recorded results of one evaluation and what they decide."""

    results: Mapping[str, str]
    details: Mapping[str, str]
    decision: Decision
    covered: tuple[str, ...] = ()


# --------------------------------------------------------------------------- parsing


def parse_gates(gates: object, default_retry_limit: int = DEFAULT_RETRY_LIMIT) -> tuple[Gate, ...]:
    """Turn a valid `gates` definition into gates, with the base gates and implicit retry limits.

    The definition is assumed to have passed `validate_for_gate_approval`; a malformed entry is
    skipped rather than raising.
    """
    mapping = as_mapping(gates) or {}
    parsed: list[Gate] = list(_BASE_GATES)
    for group in ALL_GROUPS:
        for item in as_list(mapping.get(group)) or []:
            gate = _parse_gate(group, as_mapping(item))
            if gate is not None:
                parsed.append(gate)
    return (*parsed, *_implicit_retry_gates(parsed, default_retry_limit))


_BASE_GATES: Final = (
    Gate("scope-violation", "fail", "predicate", "hard", predicate="scope-violation"),
    Gate("unanswered-question", "wait", "predicate", predicate="unanswered-question"),
    Gate("stale-spec-approval", "wait", "predicate", predicate="stale-spec-approval"),
    Gate("incomplete-evidence", "done", "evidence"),
)


def _implicit_retry_gates(gates: Sequence[Gate], default: int) -> list[Gate]:
    covered = {g.retry_gate for g in gates if g.kind == "retry_limit"}
    return [
        Gate(f"{g.id}#retry-limit", "fail", "retry_limit", "soft", retry_gate=g.id, limit=default)
        for g in gates
        if g.group == "done" and g.kind == "check" and g.id not in covered
    ]


def _parse_gate(group: str, item: Mapping[str, object] | None) -> Gate | None:
    gate_id = as_text(item.get("id")) if item is not None else None
    if item is None or gate_id is None or group not in ALL_GROUPS:
        return None
    if group == "done":
        kind = as_text(item.get("kind")) or ""
        return Gate(
            gate_id,
            "done",
            kind,
            command=_parse_command(item) if kind == "check" else None,
            minimum_level=as_text(item.get("minimum_level")),
        )
    return _parse_condition(group, gate_id, item)


def _parse_condition(group: str, gate_id: str, item: Mapping[str, object]) -> Gate | None:
    cond = as_mapping(item.get("condition"))
    if cond is None:
        return None
    severity = as_text(item.get("severity")) if group == "fail" else None
    if "predicate" in cond:
        return Gate(gate_id, group, "predicate", severity, predicate=as_text(cond["predicate"]))
    spec = as_mapping(cond.get("retry_limit"))
    if spec is not None:
        return Gate(
            gate_id,
            group,
            "retry_limit",
            "soft",
            retry_gate=as_text(spec.get("gate")),
            limit=as_int(spec.get("limit")),
        )
    return Gate(gate_id, group, "command", severity, command=_parse_command(cond))


def _parse_command(holder: Mapping[str, object]) -> CommandSpec | None:
    command = text_list(holder.get("command"))
    exit_map = as_mapping(holder.get("exit_map"))
    if not command or exit_map is None:
        return None
    limit = as_int(holder.get("time_limit"))
    return CommandSpec(command=tuple(command), exit_map=_parse_exit_map(exit_map), time_limit=limit)


def _statuses(value: object) -> frozenset[int]:
    return frozenset(n for n in (as_int(s) for s in as_list(value) or []) if n is not None)


def _parse_exit_map(exit_map: Mapping[str, object]) -> ExitMap:
    return ExitMap(
        _statuses(exit_map.get(SATISFIED)),
        _statuses(exit_map.get(NOT_SATISFIED)),
        _statuses(exit_map.get(NOT_EVALUABLE)),
    )


# ------------------------------------------------------------------- one gate


def _cannot_start(gate: Gate, outcome: RunOutcome) -> Outcome:
    cause = outcome.cause or "the command cannot start"
    if gate.group == "done" and not outcome.program_missing:
        return Outcome(NOT_SATISFIED, cause)
    return Outcome(NOT_EVALUABLE, cause)


def _run_outcome(gate: Gate, outcome: RunOutcome) -> Outcome:
    """Map a run to a result (Section 24.2)."""
    spec = gate.command
    if outcome.kind == "cannot-start":
        return _cannot_start(gate, outcome)
    if outcome.kind == "timeout":
        return Outcome(
            NOT_EVALUABLE, f"the command exceeded its time limit: {outcome.cause}".rstrip(": ")
        )
    if outcome.status is None or spec is None:
        return Outcome(NOT_EVALUABLE, outcome.cause or "the command ended without an exit status")
    result = spec.exit_map.result_for(outcome.status)
    note = "" if result != NOT_EVALUABLE else f"exit status {outcome.status} is not mapped"
    return Outcome(result, outcome.cause or note)


def _approved(state: State, gate: Gate) -> Approval | None:
    for approval in reversed(state.approvals):
        if approval.target == "gate" and approval.gate == gate.id:
            return approval
    return None


def _sign_off(state: State, gate: Gate) -> Outcome:
    approval = _approved(state, gate)
    if approval is None:
        return Outcome(NOT_SATISFIED, "no sign-off is recorded")
    needed = LEVEL_ORDER.get(gate.minimum_level or "A0", 0)
    if LEVEL_ORDER.get(approval.assurance, 0) < needed:
        return Outcome(NOT_SATISFIED, f"the sign-off needs the level {gate.minimum_level}")
    return Outcome(SATISFIED)


def _predicate(gate: Gate, state: State, facts: Facts) -> Outcome:
    if gate.predicate == "unanswered-question":
        open_ids = [q.id for q in state.unanswered]
        if open_ids:
            return Outcome(SATISFIED, f"unanswered: {', '.join(open_ids)}")
        return Outcome(NOT_SATISFIED)
    check = facts.scope if gate.predicate == "scope-violation" else facts.stale_spec_approval
    return _from_check(check, gate.predicate or gate.id)


def _from_check(check: Check | None, name: str) -> Outcome:
    if check is None:
        return Outcome(NOT_EVALUABLE, f"the result of {name} was not provided")
    return Outcome(check.result, check.detail)


def _retry(gate: Gate, facts: Facts) -> Outcome:
    count = facts.not_satisfied_counts.get(gate.retry_gate or "", 0)
    limit = gate.limit if gate.limit is not None else DEFAULT_RETRY_LIMIT
    note = f"{gate.retry_gate} had {count} not_satisfied results, limit {limit}"
    return Outcome(SATISFIED if count >= limit else NOT_SATISFIED, note)


@dataclass(frozen=True)
class _Env:
    state: State
    facts: Facts
    runner: Runner


def _evaluate_gate(gate: Gate, env: _Env) -> Outcome:
    if gate.kind == "retry_limit":
        return _retry(gate, env.facts)
    if gate.kind == "predicate":
        return _predicate(gate, env.state, env.facts)
    if gate.kind == "evidence":
        return _from_check(env.facts.evidence, "the evidence")
    if gate.kind == "sign-off":
        return _sign_off(env.state, gate)
    if gate.kind == "review":
        return _review(gate, env.facts)
    return _command(gate, env)


def _review(gate: Gate, facts: Facts) -> Outcome:
    gaps = facts.review_gaps.get(gate.id)
    if gaps is None:
        return Outcome(NOT_SATISFIED, "no review report was checked")
    if gaps:
        return Outcome(NOT_SATISFIED, "missing: " + "; ".join(gaps))
    return Outcome(SATISFIED)


def _command(gate: Gate, env: _Env) -> Outcome:
    if gate.command is None:
        return Outcome(NOT_EVALUABLE, "the gate has no complete command")
    outcome = env.runner(gate.command.command, gate.command.time_limit)
    return _run_outcome(gate, outcome)


# ----------------------------------------------------------------- decision


def override_in_force(state: State, gate_id: str, facts: Facts) -> Approval | None:
    """The latest override of a soft fail gate that still has attempts and is not lapsed."""
    for approval in reversed(state.approvals):
        if approval.target != "override" or approval.gate != gate_id:
            continue
        same = approval.definitions_hash in (None, facts.definitions_hash)
        if same and approval.used < (approval.attempts or 0):
            return approval
        return None
    return None


def _ids(done: Sequence[tuple[Gate, Outcome]], group: str, *results: str) -> list[str]:
    return [g.id for g, o in done if g.group == group and o.result in results]


def _active_fail(done: Sequence[tuple[Gate, Outcome]], severity: str) -> list[str]:
    return [
        g.id
        for g, o in done
        if g.group == "fail" and o.result == SATISFIED and g.severity == severity
    ]


def _rules(
    done: Sequence[tuple[Gate, Outcome]], covered: Sequence[str]
) -> tuple[tuple[str, list[str]], ...]:
    unknown = [g.id for g, o in done if o.result == NOT_EVALUABLE]
    soft = [i for i in _active_fail(done, "soft") if i not in covered]
    return (
        ("fail", _active_fail(done, "hard")),
        ("external", unknown[:1]),
        ("soft", soft[:1]),
        ("wait", _ids(done, "wait", SATISFIED)),
        ("done", _ids(done, "done", NOT_SATISFIED, NOT_EVALUABLE)),
    )


def _decide(
    done: Sequence[tuple[Gate, Outcome]], state: State, facts: Facts
) -> tuple[Decision, tuple[str, ...]]:
    """Apply the five rules of Section 24.2 to the results so far."""
    detail = {g.id: o.detail for g, o in done}
    soft = _active_fail(done, "soft")
    covered = tuple(i for i in soft if override_in_force(state, i, facts) is not None)
    for kind, ids in _rules(done, covered):
        if ids:
            return Decision(kind, tuple(ids), _join(ids, detail)), covered
    return Decision(), covered


def _join(ids: Sequence[str], detail: Mapping[str, str]) -> str:
    return "; ".join(f"{i}: {detail[i]}" if detail.get(i) else i for i in ids)


def evaluate(
    action: str,
    gates: Sequence[Gate],
    state: State,
    facts: Facts,
    runner: Runner,
) -> Evaluation:
    """Evaluate the gates of an action by group, stopping at the first group that decides."""
    applies = GROUPS_FOR.get(action, ())
    env = _Env(state, facts, runner)
    results: dict[str, str] = {}
    details: dict[str, str] = {}
    done: list[tuple[Gate, Outcome]] = []
    decision, covered = Decision(), ()
    for group in ALL_GROUPS:
        members = [g for g in gates if g.group == group]
        if group not in applies:
            results.update({g.id: NOT_APPLICABLE for g in members})
        elif decision.kind == "none":
            _run_group(members, env, done, results, details)
            decision, covered = _decide(done, state, facts)
    return Evaluation(results, details, decision, covered)


def _run_group(
    members: Sequence[Gate],
    env: _Env,
    done: list[tuple[Gate, Outcome]],
    results: dict[str, str],
    details: dict[str, str],
) -> None:
    for gate in members:
        outcome = _evaluate_gate(gate, env)
        done.append((gate, outcome))
        results[gate.id] = outcome.result
        if outcome.detail:
            details[gate.id] = outcome.detail


def probe(
    gate_id: str, gates: Sequence[Gate], state: State, facts: Facts, runner: Runner
) -> Outcome:
    """Evaluate one gate on its own, to see whether it can be evaluated again."""
    gate = next((g for g in gates if g.id == gate_id), None)
    if gate is None:
        return Outcome(NOT_EVALUABLE, f"the gate {gate_id!r} is not known")
    return _evaluate_gate(gate, _Env(state, facts, runner))


def count_not_satisfied(bodies: Sequence[Mapping[str, object]]) -> dict[str, int]:
    """Count the `not_satisfied` results per gate over the whole history (Section 24.2)."""
    counts: dict[str, int] = {}
    for body in bodies:
        results = as_mapping(body.get("gate_results")) or {}
        for gate_id, result in results.items():
            if result == NOT_SATISFIED:
                counts[gate_id] = counts.get(gate_id, 0) + 1
    return counts
