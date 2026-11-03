"""The evaluation of one gate by kind: commands, sign-offs, review reports, retry limits.

Section 24.2 decides what a command that cannot run means for each kind of gate.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ggsad.core.baseline import compare
from ggsad.core.gate_model import (
    DEFAULT_RETRY_LIMIT,
    LEVEL_ORDER,
    NOT_EVALUABLE,
    NOT_SATISFIED,
    SATISFIED,
    CommandSpec,
    Facts,
    Gate,
    Outcome,
    Runner,
    RunOutcome,
)

if TYPE_CHECKING:
    from ggsad.core.state import Approval, State


def _with_program(run: RunOutcome, outcome: Outcome) -> Outcome:
    """Name the program that ran when the token `@interpreter` stood for it (Section 24.10)."""
    if not run.ran:
        return outcome
    detail = f"ran {run.ran}" + (f"; {outcome.detail}" if outcome.detail else "")
    return Outcome(outcome.result, detail)


def _cannot_start(group: str, run: RunOutcome) -> Outcome:
    cause = run.cause or "the command cannot start"
    if group == "done" and not run.program_missing:
        return Outcome(NOT_SATISFIED, cause)
    return Outcome(NOT_EVALUABLE, cause)


def map_run(group: str, spec: CommandSpec | None, run: RunOutcome) -> Outcome:
    """Map a run to a result (Section 24.2)."""
    if run.kind == "cannot-start":
        return _cannot_start(group, run)
    if run.kind == "timeout":
        return Outcome(
            NOT_EVALUABLE, f"the command exceeded its time limit: {run.cause}".rstrip(": ")
        )
    if run.status is None or spec is None:
        return Outcome(NOT_EVALUABLE, run.cause or "the command ended without an exit status")
    result = spec.exit_map.result_for(run.status)
    note = "" if result != NOT_EVALUABLE else f"exit status {run.status} is not mapped"
    return Outcome(result, run.cause or note)


def run_command(
    group: str, spec: CommandSpec | None, runner: Runner
) -> tuple[Outcome, RunOutcome | None]:
    """Run a command and map the run. A missing or incomplete command cannot be evaluated."""
    if spec is None:
        return Outcome(NOT_EVALUABLE, "the gate has no complete command"), None
    run = runner(spec.command, spec.time_limit)
    return _with_program(run, map_run(group, spec, run)), run


def command_outcome(gate: Gate, runner: Runner) -> Outcome:
    """A command gate; a baseline can turn a `not_satisfied` exit into `satisfied` (24.6)."""
    outcome, run = run_command(gate.group, gate.command, runner)
    if run is None or gate.baseline is None:
        return outcome
    if run.kind != "exit" or outcome.result != NOT_SATISFIED:
        return outcome
    ids = [entry.id for entry in gate.baseline]
    return _with_program(run, compare(ids, gate.extract, run))


def retry_outcome(gate: Gate, facts: Facts) -> Outcome:
    """A retry limit is active when the recorded `not_satisfied` count reaches the limit."""
    count = facts.not_satisfied_counts.get(gate.retry_gate or "", 0)
    limit = gate.limit if gate.limit is not None else DEFAULT_RETRY_LIMIT
    note = f"{gate.retry_gate} had {count} not_satisfied results, limit {limit}"
    return Outcome(SATISFIED if count >= limit else NOT_SATISFIED, note)


def _approval_of(state: State, target: str, gate_id: str | None = None) -> Approval | None:
    for approval in reversed(state.approvals):
        if approval.target == target and (gate_id is None or approval.gate == gate_id):
            return approval
    return None


def sign_off_outcome(
    state: State, gate_id: str, minimum_level: str | None, facts: Facts
) -> Outcome:
    """A sign-off gate is satisfied by a current sign-off at the required level (Section 24.3)."""
    approval = _approval_of(state, "gate", gate_id)
    if approval is None:
        return Outcome(NOT_SATISFIED, "no sign-off is recorded")
    bound = approval.definitions_hash
    if bound is not None and facts.definitions_hash not in (None, bound):
        return Outcome(NOT_SATISFIED, "the sign-off is stale: the gate definitions changed")
    if LEVEL_ORDER.get(approval.assurance, 0) < LEVEL_ORDER.get(minimum_level or "A0", 0):
        return Outcome(NOT_SATISFIED, f"the sign-off needs the level {minimum_level}")
    return Outcome(SATISFIED)


def review_outcome(state: State, gate: Gate, facts: Facts) -> Outcome:
    """A review gate needs a complete report that the decision owner approved (Section 23.3)."""
    gaps = facts.review_gaps.get(gate.id)
    if gaps is None:
        return Outcome(NOT_SATISFIED, "no review report was checked")
    if gaps:
        return Outcome(NOT_SATISFIED, "missing: " + "; ".join(gaps))
    approval = _approval_of(state, "review")
    if approval is None:
        return Outcome(NOT_SATISFIED, "the review result is not approved")
    if facts.review_hash is None:
        return Outcome(NOT_EVALUABLE, "the content hash of review.md was not provided")
    if approval.content_hash != facts.review_hash:
        return Outcome(NOT_SATISFIED, "review.md changed after the approval of the review result")
    return Outcome(SATISFIED)
