"""Gate evaluation of the `core` profile (Sections 23.6, 23.7, 24.2, and 24.7).

The engine is pure: commands are run by a runner that the caller hands in, and the results of the
checks that need files or version control (scope, stale specification approval, review reports)
are handed in as `Facts`. Nothing here reads a clock, a file, or a process.

Interpretations fixed here (listed in the pull requests):
- a retry limit is checked against the `not_satisfied` results already in the history, before the
  done gates run, so the limit is reached when the count is greater than or equal to it;
- the implicit retry limit of a done `check` gate is evaluated under the key `<gate>#retry-limit`;
- a base-gate result that the caller does not hand in is `not_evaluable`, never a pass.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ggsad.core.checks import command_outcome, retry_outcome, review_outcome, sign_off_outcome
from ggsad.core.evidence import evaluate_evidence
from ggsad.core.gate_model import (
    ALL_GROUPS,
    GROUPS_FOR,
    LEVEL_ORDER,
    NOT_APPLICABLE,
    NOT_EVALUABLE,
    NOT_SATISFIED,
    SATISFIED,
    Check,
    CommandSpec,
    Decision,
    Evaluation,
    ExitMap,
    Facts,
    Gate,
    Outcome,
    Requirement,
    Runner,
    RunOutcome,
    parse_gates,
)
from ggsad.core.values import as_mapping

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from ggsad.core.state import Approval, State

__all__ = [
    "ALL_GROUPS", "GROUPS_FOR", "LEVEL_ORDER", "NOT_APPLICABLE", "NOT_EVALUABLE", "NOT_SATISFIED",
    "SATISFIED", "Check", "CommandSpec", "Decision", "Evaluation", "ExitMap", "Facts", "Gate",
    "Outcome", "Requirement", "RunOutcome", "Runner", "count_not_satisfied", "evaluate",
    "override_in_force", "parse_gates", "probe",
]  # fmt: skip


def _predicate(gate: Gate, state: State, facts: Facts) -> Outcome:
    if gate.predicate == "unanswered-question":
        open_ids = [q.id for q in state.unanswered]
        if open_ids:
            return Outcome(SATISFIED, f"unanswered: {', '.join(open_ids)}")
        return Outcome(NOT_SATISFIED)
    if gate.predicate == "scope-violation":
        if state.state == "open":
            return Outcome(NOT_APPLICABLE, "the change has not started")
        return _from_check(facts.scope, "scope-violation")
    return _stale_spec(state, facts)


def _stale_spec(state: State, facts: Facts) -> Outcome:
    """Active only if the specification was approved and its hash differs from the approved one."""
    if facts.spec_hash is None:
        return _from_check(facts.stale_spec_approval, "stale-spec-approval")
    approved = [a for a in state.approvals if a.target == "spec"]
    if not approved or approved[-1].content_hash == facts.spec_hash:
        return Outcome(NOT_SATISFIED)
    return Outcome(SATISFIED, "spec.md changed after its approval")


def _from_check(check: Check | None, name: str) -> Outcome:
    if check is None:
        return Outcome(NOT_EVALUABLE, f"the result of {name} was not provided")
    return Outcome(check.result, check.detail)


@dataclass(frozen=True)
class _Env:
    state: State
    facts: Facts
    runner: Runner


def _evaluate_gate(gate: Gate, env: _Env) -> Outcome:
    if gate.kind == "retry_limit":
        return retry_outcome(gate, env.facts)
    if gate.kind == "predicate":
        return _predicate(gate, env.state, env.facts)
    if gate.kind == "evidence":
        return evaluate_evidence(gate, env.state, env.facts, env.runner)
    if gate.kind == "sign-off":
        return sign_off_outcome(env.state, gate.id, gate.minimum_level, env.facts)
    if gate.kind == "review":
        return review_outcome(env.state, gate, env.facts)
    return command_outcome(gate, env.runner)


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
