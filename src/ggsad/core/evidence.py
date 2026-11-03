"""Executable evidence (Section 24.9): the incomplete evidence gate, judged at closure.

The evidence of a change is complete only when it declares a requirement, every requirement has an
evidence command or a human check, and every evidence command ends `satisfied` in this evaluation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ggsad.core.checks import run_command, sign_off_outcome
from ggsad.core.gate_model import NOT_EVALUABLE, NOT_SATISFIED, SATISFIED, Outcome

if TYPE_CHECKING:
    from ggsad.core.gate_model import Facts, Gate, Requirement, Runner
    from ggsad.core.state import State


def _check_requirement(
    requirement: Requirement, state: State, facts: Facts, runner: Runner
) -> tuple[list[str], list[str]]:
    """The gaps (not complete) and the unknowns (cannot be evaluated) of one requirement."""
    gaps: list[str] = []
    unknown: list[str] = []
    for number, command in enumerate(requirement.commands, start=1):
        outcome, _run = run_command("done", command.spec, runner)
        label = f"{requirement.id} evidence {number}"
        if outcome.result == NOT_EVALUABLE:
            unknown.append(f"{label}: {outcome.detail}")
        elif outcome.result != SATISFIED:
            gaps.append(
                f"{label} is {outcome.result}" + (f" ({outcome.detail})" if outcome.detail else "")
            )
    if requirement.human_gate is not None:
        signed = sign_off_outcome(state, requirement.human_gate, None, facts)
        if signed.result != SATISFIED:
            gaps.append(f"{requirement.id} human check: {signed.detail}")
    elif not requirement.commands:
        gaps.append(f"{requirement.id} has no evidence command and no human check")
    return gaps, unknown


def evaluate_evidence(gate: Gate, state: State, facts: Facts, runner: Runner) -> Outcome:
    """The result of the incomplete evidence gate."""
    if not gate.requirements:
        return Outcome(NOT_SATISFIED, "no requirements are declared")
    gaps: list[str] = []
    unknown: list[str] = []
    for requirement in gate.requirements:
        more_gaps, more_unknown = _check_requirement(requirement, state, facts, runner)
        gaps += more_gaps
        unknown += more_unknown
    if unknown:
        return Outcome(NOT_EVALUABLE, "; ".join(unknown))
    if gaps:
        return Outcome(NOT_SATISFIED, "; ".join(gaps))
    checked = [r.id for r in gate.requirements if r.human_gate is not None]
    note = f"human-checked: {', '.join(checked)}" if checked else ""
    return Outcome(SATISFIED, note)
