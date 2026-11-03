"""Executable evidence and baselines: AE-052, AE-061 to AE-064, AE-321."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from engine_helpers import (
    CLEAR,
    active,
    check_gate,
    context,
    definition,
    do,
    evidence_requirement,
    gate_detail,
    gate_results,
    req,
    runner,
)

from ggsad.core.baseline import compare, extract_failures
from ggsad.core.gate_model import ExtractRule, RunOutcome
from ggsad.core.state import Approval

FAIL = RunOutcome("exit", status=1)
NO_PROGRAM = RunOutcome(
    "cannot-start", cause="the approved program is missing", program_missing=True
)
NOT_LISTED = RunOutcome("cannot-start", cause="not on required_tools")


def two(first: str = "check-1", second: str = "check-2") -> list[dict[str, Any]]:
    return [evidence_requirement(first, "R1"), evidence_requirement(second, "R2")]


def test_ae061_complete_evidence_when_both_commands_are_satisfied() -> None:
    result = do(active(), req("close"), context(requirements=two()))
    assert result.state.outcome == "done"
    assert gate_results(result)["incomplete-evidence"] == "satisfied"


def test_ae062_a_requirement_without_an_evidence_command_is_named() -> None:
    bare = {"id": "R2", "text": "t", "done_when": [], "evidence": []}
    result = do(active(), req("close"), context(requirements=[evidence_requirement(), bare]))
    assert result.result == "blocked"
    assert "R2 has no evidence command" in gate_detail(result)["incomplete-evidence"]


def test_a_change_without_requirements_has_no_complete_evidence() -> None:
    result = do(active(), req("close"), context(requirements=[]))
    assert result.result == "blocked"
    assert "no requirements are declared" in gate_detail(result)["incomplete-evidence"]


def test_ae063_a_failing_evidence_command_leaves_the_evidence_incomplete() -> None:
    result = do(active(), req("close"), context(requirements=two()), run=runner({"check-2": FAIL}))
    assert result.result == "blocked" and result.state.state == "active"
    assert "R2 evidence 1 is not_satisfied" in gate_detail(result)["incomplete-evidence"]


def test_an_evidence_command_that_cannot_be_evaluated_makes_the_change_wait_not_fail() -> None:
    result = do(active(), req("close"), context(), run=runner({"evidence-check": NO_PROGRAM}))
    wait = result.state.wait
    assert wait is not None and wait.kind == "external"
    assert "incomplete-evidence" in wait.reason and result.state.outcome is None


def test_an_evidence_command_that_cannot_start_otherwise_is_not_satisfied() -> None:
    result = do(active(), req("close"), context(), run=runner({"evidence-check": NOT_LISTED}))
    assert result.result == "blocked" and result.state.wait is None
    assert gate_results(result)["incomplete-evidence"] == "not_satisfied"


def test_ae321_a_human_check_is_closed_by_a_sign_off_and_recorded() -> None:
    check = {"reason": "no command can judge readability", "gate": "page-ok"}
    human = {"id": "R1", "text": "t", "done_when": [], "human_check": check}
    gates = definition(done=[{"id": "page-ok", "kind": "sign-off"}])
    ctx = context(gates, requirements=[human])
    assert do(active(), req("close"), ctx).result == "blocked"
    signed = active(approvals=(Approval("gate", "human:ada", "A1", "A0", gate="page-ok"),))
    result = do(signed, req("close"), ctx)
    assert result.state.outcome == "done"
    assert "human-checked: R1" in gate_detail(result)["incomplete-evidence"]


def test_a_stale_sign_off_does_not_close_a_human_check() -> None:
    human = {"id": "R1", "text": "t", "done_when": [],
             "human_check": {"reason": "r", "gate": "page-ok"}}  # fmt: skip
    gates = definition(done=[{"id": "page-ok", "kind": "sign-off"}])
    old = Approval(
        "gate", "human:ada", "A1", "A0", gate="page-ok", definitions_hash="sha256:" + "1" * 64
    )
    facts = replace(CLEAR, definitions_hash="sha256:" + "2" * 64)
    result = do(active(approvals=(old,)), req("close"), context(gates, requirements=[human]), facts)
    assert result.result == "blocked"


# ------------------------------------------------------------------- baselines


def baseline_gate(ids: list[str]) -> dict[str, Any]:
    gate = check_gate()
    gate["extract"] = {"pattern": r"^FAILED (\S+)", "stream": "stdout"}
    gate["baseline"] = [{"id": i, "reason": "known", "review_by": "2026-12-01"} for i in ids]
    return gate


def output(*lines: str) -> RunOutcome:
    return RunOutcome("exit", status=1, stdout="\n".join(lines))


def test_ae052_a_new_failure_is_named() -> None:
    gates = definition(done=[baseline_gate(["t1"])])
    run = runner({"pytest": output("FAILED t1", "FAILED t9")})
    result = do(active(), req("close"), context(gates), run=run)
    assert result.result == "blocked"
    detail = gate_detail(result)["tests-pass"]
    assert "1 new failures: t9" in detail and "0 baseline entries did not fail" in detail


def test_failures_that_are_all_on_the_baseline_are_satisfied_and_unused_entries_are_counted() -> (
    None
):
    gates = definition(done=[baseline_gate(["t1", "t2", "t3"])])
    run = runner({"pytest": output("FAILED t1", "FAILED t1", "noise")})
    result = do(active(), req("close"), context(gates), run=run)
    assert result.state.outcome == "done"
    assert "2 baseline entries did not fail" in gate_detail(result)["tests-pass"]


def test_the_exit_status_satisfied_is_satisfied_whatever_the_output() -> None:
    gates = definition(done=[baseline_gate([])])
    run = runner({"pytest": RunOutcome("exit", status=0, stdout="FAILED t9")})
    assert do(active(), req("close"), context(gates), run=run).state.outcome == "done"


def test_an_empty_baseline_makes_every_failure_new() -> None:
    gates = definition(done=[baseline_gate([])])
    result = do(active(), req("close"), context(gates), run=runner({"pytest": output("FAILED a")}))
    assert result.result == "blocked" and "1 new failures: a" in gate_detail(result)["tests-pass"]


def test_failures_that_cannot_be_extracted_make_the_gate_not_evaluable() -> None:
    gates = definition(done=[baseline_gate(["t1"])])
    result = do(active(), req("close"), context(gates), run=runner({"pytest": output("nothing")}))
    assert result.state.wait is not None and result.state.wait.kind == "external"
    assert gate_results(result)["tests-pass"] == "not_evaluable"


def test_a_gate_with_a_baseline_but_no_rule_cannot_compare() -> None:
    gate = baseline_gate(["t1"])
    del gate["extract"]
    result = do(active(), req("close"), context(definition(done=[gate])),
                run=runner({"pytest": output("FAILED t1")}))  # fmt: skip
    assert gate_results(result)["tests-pass"] == "not_evaluable"


def test_a_baseline_does_not_change_a_cannot_start() -> None:
    gates = definition(done=[baseline_gate(["t1"])])
    result = do(active(), req("close"), context(gates), run=runner({"pytest": NOT_LISTED}))
    assert gate_results(result)["tests-pass"] == "not_satisfied"


def test_the_new_failures_are_named_in_code_point_order_up_to_three() -> None:
    run = output("FAILED b", "FAILED B", "FAILED a", "FAILED c")
    result = compare([], ExtractRule(r"^FAILED (\S+)"), run)
    assert result.detail.startswith("4 new failures: B, a, b;")


def test_extraction_streams_and_bad_rules() -> None:
    run = RunOutcome("exit", status=1, stdout="FAILED out", stderr="FAILED err")
    assert extract_failures(ExtractRule(r"FAILED (\w+)", "stdout"), run) == {"out"}
    assert extract_failures(ExtractRule(r"FAILED (\w+)", "stderr"), run) == {"err"}
    assert extract_failures(ExtractRule(r"FAILED (\w+)", "both"), run) == {"out", "err"}
    assert extract_failures(ExtractRule(r"FAILED (\w+)", "other"), run) is None
    assert extract_failures(ExtractRule(r"FAILED \w+", "stdout"), run) is None  # no group
    assert extract_failures(ExtractRule(r"(", "stdout"), run) is None  # not a regex
    assert compare(["x"], None, run).result == "not_evaluable"
