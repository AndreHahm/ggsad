"""The engine: transition table, evaluation order, failure, waits (Sections 23.2 to 24.8).

Test names carry the AE number of the example they cover.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from engine_helpers import (
    ADA,
    AGENT,
    CLEAR,
    NOW,
    active,
    assert_consistent,
    check_gate,
    cmd_gate,
    context,
    definition,
    do,
    gate_detail,
    gate_results,
    req,
    runner,
)
from hypothesis import given
from hypothesis import strategies as st

from ggsad.core.engine import apply
from ggsad.core.engine_types import Actor, Request
from ggsad.core.gate_eval import (
    Check,
    RunOutcome,
    count_not_satisfied,
    parse_gates,
)
from ggsad.core.state import Approval, Question, State, Wait

# ------------------------------------------------------------ states and outcomes


def test_ae014_close_sets_outcome_done_only_when_closed() -> None:
    result = do(active(), req("close"))
    assert (result.state.state, result.state.outcome) == ("closed", "done")
    assert do(None, req("new", AGENT)).state.outcome is None


def test_ae015_closed_change_is_final() -> None:
    closed = State(state="closed", outcome="cancelled")
    result = do(closed, req("start", AGENT))
    assert result.result == "rejected" and result.state == closed and not result.changed
    assert result.codes == ("state-illegal",)


def test_new_creates_open_state_and_rejects_a_second_new() -> None:
    created = do(None, req("new", AGENT))
    assert created.result == "success" and created.state == State()
    assert do(State(), req("new", AGENT)).codes == ("change-exists",)
    assert do(None, req("close", AGENT)).codes == ("change-missing",)


def test_new_rejected_with_caller_issues() -> None:
    facts = replace(
        CLEAR, target_issues={"new": (("follows-open", "follows names an open change"),)}
    )
    assert do(None, req("new", AGENT), facts=facts).codes == ("follows-open",)


# ------------------------------------------------------------------ approvals


def test_ae018_approve_all_records_spec_and_gates_and_keeps_state() -> None:
    facts = replace(CLEAR, definitions_hash="sha256:" + "a" * 64)
    result = do(
        State(), req("approve", target="all", content_hash="sha256:" + "b" * 64), facts=facts
    )
    assert [a.target for a in result.state.approvals] == ["spec", "gates"]
    assert result.state.state == "open"


def test_ae019_unanswered_question_blocks_spec_approval() -> None:
    state = State(questions=(Question("Q1", "t", "human:ada", "agent:codex"),))
    result = do(state, req("approve", target="spec"))
    assert result.codes == ("open-questions",) and "Q1" in result.issues[0].message
    assert result.state.approvals == ()


def test_ae020_agent_cannot_approve_a_sign_off_gate() -> None:
    gates = definition(done=[{"id": "legal-ok", "kind": "sign-off"}])
    result = do(active(), req("approve", AGENT, target="gate", gate="legal-ok"), context(gates))
    assert result.codes == ("human-required",)


def test_sign_off_by_a_human_satisfies_the_gate() -> None:
    gates = definition(done=[{"id": "legal-ok", "kind": "sign-off"}])
    ctx = context(gates)
    assert do(active(), req("close"), ctx).result == "blocked"
    signed = do(active(), req("approve", target="gate", gate="legal-ok"), ctx).state
    assert do(signed, req("close"), ctx).state.outcome == "done"
    assert do(active(), req("approve", target="gate", gate="nope"), ctx).codes == (
        "gate-not-sign-off",
    )


def test_approve_unknown_target_is_rejected() -> None:
    assert do(State(), req("approve", target="everything")).codes == ("approve-target-invalid",)


def test_ae021_start_needs_approved_gates() -> None:
    facts = replace(CLEAR, gates_approved=False)
    result = do(State(), req("start", AGENT), facts=facts)
    assert result.result == "rejected" and result.state.state == "open"
    assert result.state.base_revision is None


def test_start_records_the_base_revision_and_evaluates_only_fail_and_wait_groups() -> None:
    gates = definition(done=[check_gate()])
    result = do(State(), req("start", AGENT), context(gates))
    assert result.state.state == "active" and result.state.base_revision == "r1"
    results = gate_results(result)
    assert results["tests-pass"] == "not_applicable"  # AE-075
    assert results["scope-violation"] == "not_applicable"  # not evaluated before the start


def test_start_rejections() -> None:
    no_rev = replace(CLEAR, revision=None)
    assert do(State(), req("start", AGENT), facts=no_rev).codes == ("base-revision-unavailable",)
    dirty = replace(CLEAR, unclean_paths=("a.py", "b.py"))
    result = do(State(), req("start", AGENT), facts=dirty)
    assert result.codes == ("working-copy-unclean",) and "a.py, b.py" in result.issues[0].message
    assert do(State(), req("start", ADA)).codes == ("requestor-not-approved",)
    assert do(State(), req("start", Actor("agent:other"))).codes == ("requestor-not-approved",)


def test_start_is_blocked_by_hard_failure_wait_gate_or_unevaluable_gate() -> None:
    hard_gate = definition(fail=[cmd_gate("no-secrets", "hard", "scan")])
    run = runner({"scan": RunOutcome("exit", status=1)})
    assert do(State(), req("start", AGENT), context(hard_gate), run=run).codes == ("start-blocked",)
    question = State(questions=(Question("Q1", "t", "human:ada", "agent:codex"),))
    assert do(question, req("start", AGENT)).codes == ("start-blocked",)
    nostart = runner({"scan": RunOutcome("cannot-start", cause="no scan")})
    unknown = do(State(), req("start", AGENT), context(hard_gate), run=nostart)
    assert unknown.codes == ("start-blocked",)
    assert do(State(), req("start", AGENT), facts=replace(CLEAR, scope=None)).result == "success"


# ------------------------------------------------------------- wait, ask, answer


def test_ae022_wait_for_a_question() -> None:
    state = active(questions=(Question("Q1", "keep?", "human:ada", "agent:codex"),))
    result = do(state, req("wait", AGENT, question="Q1", owner="human:ada"))
    wait = result.state.wait
    assert result.state.state == "waiting" and wait is not None
    assert (wait.kind, wait.question, wait.resume_when) == ("question", "Q1", "Q1 answered")


def test_wait_rejections() -> None:
    q = Question("Q1", "t", "human:ada", "agent:codex")
    assert do(
        active(questions=(q,)), req("wait", AGENT, question="Q1", owner="human:bo")
    ).codes == ("owner-mismatch",)
    assert do(active(), req("wait", AGENT, question="Q9")).codes == ("question-invalid",)
    assert do(active(), req("wait", AGENT, reason="r", resume_when="x", owner="agent:x")).codes == (
        "owner-not-approved",
    )
    assert do(active(), req("wait", AGENT, owner="human:ada", resume_when="x")).codes == (
        "reason-missing",
    )
    assert do(State(), req("wait", AGENT, question="Q1")).codes == ("state-illegal",)


def test_manual_wait_and_resume_needs_a_note() -> None:
    waited = do(active(), req("wait", AGENT, reason="legal", owner="human:ada", resume_when="ok"))
    assert waited.state.wait is not None and waited.state.wait.kind == "manual"
    assert do(waited.state, req("resume", ADA)).codes == ("note-missing",)
    resumed = do(waited.state, req("resume", ADA, note="Legal said yes."))
    assert resumed.state.state == "active" and resumed.state.wait is None


def test_ask_assigns_next_identifier_and_default_owner() -> None:
    first = do(active(), req("ask", AGENT, text="Which?", options=("a", "b")))
    second = do(first.state, req("ask", AGENT, text="Why?", about_spec=True))
    assert [q.id for q in second.state.questions] == ["Q1", "Q2"]
    assert second.state.questions[0].owner == "human:ada"
    assert do(active(), req("ask", AGENT, text="x", options=("a", "a"))).codes == (
        "options-invalid",
    )
    assert do(active(), req("ask", AGENT, text="x", options=("a",))).codes == ("options-invalid",)
    assert do(active(), req("ask", AGENT, text="x", owner="agent:x")).codes == (
        "owner-not-approved",
    )
    assert do(active(), req("ask", AGENT, text=" ")).codes == ("text-missing",)


def test_ae023_and_ae060_answer_a_structured_question() -> None:
    q = Question("Q1", "t", "human:ada", "agent:codex", options=("keep", "drop"))
    result = do(active(questions=(q,)), req("answer", question="Q1", answer="drop"))
    answered = result.state.questions[0]
    assert (answered.answer, answered.answerer) == ("drop", "human:ada")
    assert result.state.state == "active"


def test_answer_rejections() -> None:
    q = Question("Q1", "t", "human:ada", "agent:codex", options=("keep", "drop"))
    state = active(questions=(q,))
    assert do(state, req("answer", question="Q1", answer="maybe")).codes == ("answer-invalid",)
    assert do(state, req("answer", Actor("human:bo"), question="Q1", answer="keep")).codes == (
        "answer-not-owner",
    )
    assert do(state, req("answer", AGENT, question="Q1", answer="keep")).codes == (
        "human-required",
    )
    free = active(questions=(Question("Q1", "t", "human:ada", "agent:codex"),))
    assert do(free, req("answer", question="Q1", answer=" \t")).codes == ("answer-invalid",)
    done = do(free, req("answer", question="Q1", answer="yes")).state
    assert do(done, req("answer", question="Q1", answer="again")).codes == ("question-invalid",)


def test_an_answer_does_not_resume_unless_asked() -> None:
    q = Question("Q1", "t", "human:ada", "agent:codex")
    waiting = State(state="waiting", questions=(q,),
                    wait=Wait("question", "r", "human:ada", "Q1 answered", None, "Q1"))  # fmt: skip
    plain = do(waiting, req("answer", question="Q1", answer="yes"))
    assert plain.state.state == "waiting" and len(plain.bodies) == 1
    both = do(waiting, req("answer", question="Q1", answer="yes", and_resume=True))
    assert both.state.state == "active" and [b["action"] for b in both.bodies] == [
        "answer",
        "resume",
    ]


def test_ae314_conflict_stops_the_change_and_names_both_documents() -> None:
    result = do(active(), req("conflict", AGENT, text="R2 conflicts with ADR-004",
                              documents=("spec.md", "docs/adr/ADR-004.md")))  # fmt: skip
    state = result.state
    assert state.state == "waiting" and state.wait is not None and state.wait.kind == "question"
    assert "spec.md" in state.questions[0].text and "ADR-004" in state.questions[0].text
    assert do(state.with_(state="active", wait=None), req("close")).result == "blocked"
    assert do(active(), req("conflict", AGENT, text="x", documents=("spec.md",))).codes == (
        "documents-missing",
    )


# --------------------------------------------------------- close and evaluation


def test_ae024_close_completed_change() -> None:
    gates = definition(done=[check_gate()])
    assert do(active(), req("close"), context(gates)).state.outcome == "done"


def test_ae025_unsatisfied_done_gate_keeps_the_change_active() -> None:
    gates = definition(done=[check_gate()])
    run = runner({"pytest": RunOutcome("exit", status=1)})
    result = do(active(), req("close"), context(gates), run=run)
    assert result.result == "blocked" and result.changed
    assert (result.state.state, result.state.outcome) == ("active", None)


def test_ae017_a_hard_failure_closes_as_failed_with_success() -> None:
    gates = definition(fail=[cmd_gate("no-secrets", "hard", "scan")])
    run = runner({"scan": RunOutcome("exit", status=1)})
    result = do(active(), req("close"), context(gates), run=run)
    assert result.result == "success"
    assert (result.state.state, result.state.outcome) == ("closed", "failed")
    assert "no-secrets" in (result.state.reason or "")


def test_ae030_a_hard_failure_decides_before_satisfied_done_gates() -> None:
    gates = definition(done=[check_gate()])
    facts = replace(CLEAR, scope=Check("satisfied", "docs/guide.md"))
    result = do(active(), req("close"), context(gates), facts)
    assert result.state.outcome == "failed"
    results = gate_results(result)
    assert "tests-pass" not in results  # a later group is not evaluated


def test_ae031_a_missing_program_makes_the_change_wait_not_fail() -> None:
    gates = definition(done=[check_gate("docs-built", "mk")])
    run = runner({"mk": RunOutcome("cannot-start", cause="program mk is missing",
                                   program_missing=True)})  # fmt: skip
    result = do(active(), req("close"), context(gates), run=run)
    wait = result.state.wait
    assert result.result == "blocked" and result.state.state == "waiting"
    assert wait is not None and wait.kind == "external"
    assert result.state.outcome is None


def test_ae029_waits_that_the_evaluation_creates() -> None:
    soft = definition(fail=[cmd_gate("flaky", "soft", "flaky")])
    first = do(
        active(), req("close"), context(soft), run=runner({"flaky": RunOutcome("exit", status=1)})
    )
    wait = first.state.wait
    assert wait is not None and wait.kind == "fail-gate" and wait.owner == "human:ada"
    assert wait.resume_when == "a human recorded an override of flaky" and "flaky" in wait.reason
    docs = definition(done=[check_gate("docs-built", "mk")])
    run = runner(
        {"mk": RunOutcome("cannot-start", cause="missing program mk", program_missing=True)}
    )
    second = do(active(), req("close"), context(docs), run=run).state.wait
    assert second is not None and second.kind == "external"
    assert second.resume_when == "gate docs-built can be evaluated"
    assert "docs-built" in second.reason and "mk" in second.reason


def test_ae032_scope_violation_gate_applies_without_being_listed() -> None:
    facts = replace(CLEAR, scope=Check("satisfied", "paths outside the scope: docs/a.md"))
    result = do(active(), req("close"), facts=facts)
    assert (result.state.state, result.state.outcome) == ("closed", "failed")
    assert "docs/a.md" in (result.state.reason or "")  # AE-082


def test_ae033_stale_specification_approval_blocks_until_approved_again() -> None:
    stale = replace(CLEAR, stale_spec_approval=Check("satisfied", "spec.md changed"))
    result = do(active(), req("close"), facts=stale)
    assert result.result == "blocked" and result.state.state == "active"
    assert do(active(), req("close"), facts=CLEAR).state.outcome == "done"


def test_ae327_unstartable_fail_gate_waits_but_unstartable_done_gate_fails() -> None:
    fail = definition(fail=[cmd_gate("no-secrets", "hard", "scan")])
    nostart = RunOutcome("cannot-start", cause="no such program")
    first = do(active(), req("close"), context(fail), run=runner({"scan": nostart}))
    assert first.state.state == "waiting" and first.state.wait is not None
    assert first.state.wait.kind == "external"
    done = definition(done=[check_gate("lint", "lintx")])
    second = do(active(), req("close"), context(done), run=runner({"lintx": nostart}))
    assert second.result == "blocked" and second.state.state == "active"
    assert gate_results(second)["lint"] == "not_satisfied"
    assert "no such program" in gate_detail(second)["lint"]


def test_timeout_unmapped_status_and_no_status_are_not_evaluable() -> None:
    gates = definition(done=[check_gate()])
    for outcome in (
        RunOutcome("timeout"),
        RunOutcome("exit", status=77),
        RunOutcome("exit", status=9),
        RunOutcome("no-status"),
    ):
        result = do(active(), req("close"), context(gates), run=runner({"pytest": outcome}))
        assert gate_results(result)["tests-pass"] == "not_evaluable"
        assert result.state.wait is not None and result.state.wait.kind == "external"


def test_ae039_a_hard_failure_is_decided_before_an_unevaluable_gate() -> None:
    gates = definition(done=[check_gate("docs-built", "mk")])
    facts = replace(CLEAR, scope=Check("satisfied", "docs/x"))
    run = runner({"mk": RunOutcome("cannot-start", program_missing=True)})
    result = do(active(), req("close"), context(gates), facts, run)
    assert result.state.outcome == "failed" and result.state.wait is None


def test_a_wait_gate_decides_before_a_done_gate_that_cannot_be_evaluated() -> None:
    gates = definition(done=[check_gate("docs-built", "mk")])
    state = active(questions=(Question("Q1", "t", "human:ada", "agent:codex"),))
    run = runner({"mk": RunOutcome("cannot-start", program_missing=True)})
    result = do(state, req("close"), context(gates), run=run)  # AE-059
    assert result.result == "blocked" and result.state.state == "active"
    assert "unanswered-question" in result.issues[0].message or "Q1" in result.issues[0].message
    assert "docs-built" not in gate_results(result)


def test_a_wait_gate_that_cannot_be_evaluated_waits_before_the_done_gates() -> None:
    gates = definition(wait=[{"id": "ready", "condition": {"command": ["probe"],
                       "exit_map": {"satisfied": [0], "not_satisfied": [1]}}}])  # fmt: skip
    run = runner({"probe": RunOutcome("cannot-start", cause="no probe")})
    result = do(active(), req("close"), context(gates), run=run)
    assert result.state.wait is not None and result.state.wait.kind == "external"


def test_ae068_ae069_blocked_is_recorded_and_rejected_writes_nothing() -> None:
    blocked = do(active(), req("close"), context(definition(done=[check_gate()])),
                 run=runner({"pytest": RunOutcome("exit", status=1)}))  # fmt: skip
    assert blocked.result == "blocked" and blocked.changed
    rejected = do(State(), req("close"))
    assert rejected.result == "rejected" and rejected.bodies == ()


def test_close_by_an_agent_needs_a_report_and_permission() -> None:
    assert do(active(), req("close", AGENT)).codes == ("agent-report-missing",)
    report = {"errors": [], "decisions": [], "exceptions": []}
    assert do(active(), req("close", AGENT, agent_report=report)).codes == ("human-close-required",)
    allowed = do(active(), req("close", AGENT, agent_report=report), context(agent_may_close=True))
    assert allowed.state.outcome == "done" and allowed.bodies[0]["agent_report"] == report
    assert do(active(), req("close", Actor("agent:other"), agent_report=report)).codes == (
        "requestor-not-approved",
    )


def test_missing_base_gate_result_is_not_evaluable_never_a_pass() -> None:
    result = do(active(), req("close"), facts=replace(CLEAR, evidence=None))
    assert result.state.wait is not None and result.state.wait.kind == "external"
    assert (
        do(active(), req("close"), facts=replace(CLEAR, evidence=Check("not_satisfied"))).result
        == "blocked"
    )


def test_review_gate_needs_a_complete_report() -> None:
    gates = definition(done=[{"id": "code-review", "kind": "review"}])
    facts = replace(CLEAR, review_gaps={"code-review": ("F-1 has no decision",)})
    result = do(active(), req("close"), context(gates), facts)  # AE-316
    assert result.result == "blocked" and "F-1" in result.issues[0].message
    ok = replace(CLEAR, review_gaps={"code-review": ()})
    assert do(active(), req("close"), context(gates), ok).state.outcome == "done"


# ------------------------------------------------------- failure, retry, override


def soft_gate() -> dict[str, Any]:
    cond = {"retry_limit": {"gate": "tests-pass", "limit": 3}}
    return {"id": "tries", "severity": "soft", "condition": cond}


def test_ae055_ae056_hard_closes_failed_soft_pauses() -> None:
    gates = definition(fail=[cmd_gate("soft-one", "soft", "s")])
    run = runner({"s": RunOutcome("exit", status=1)})
    result = do(active(), req("close"), context(gates), run=run)
    assert result.state.state == "waiting" and result.state.wait is not None
    assert result.state.wait.kind == "fail-gate" and result.state.outcome is None


def test_ae038_a_missing_program_consumes_no_attempt() -> None:
    gates = definition(fail=[soft_gate()], done=[check_gate()])
    bodies = [{"gate_results": {"tests-pass": "not_satisfied"}}] * 2
    counts = count_not_satisfied(bodies)
    facts = replace(CLEAR, not_satisfied_counts=counts)
    run = runner({"pytest": RunOutcome("cannot-start", program_missing=True)})
    result = do(active(), req("close"), context(gates), facts, run)
    assert counts == {"tests-pass": 2}
    assert gate_results(result)["tests-pass"] == "not_evaluable"
    assert gate_results(result)["tries"] == "not_satisfied"
    assert result.state.wait is not None and result.state.wait.kind == "external"


def test_retry_limit_is_reached_when_the_count_equals_the_limit() -> None:
    gates = definition(fail=[soft_gate()], done=[check_gate()])
    two = replace(CLEAR, not_satisfied_counts={"tests-pass": 2})
    three = replace(CLEAR, not_satisfied_counts={"tests-pass": 3})
    assert do(active(), req("close"), context(gates), two).state.outcome == "done"
    paused = do(active(), req("close"), context(gates), three)
    assert paused.state.wait is not None and paused.state.wait.kind == "fail-gate"


def test_a_done_check_gate_has_an_implicit_retry_limit_of_three() -> None:
    gates = definition(done=[check_gate()])
    three = replace(CLEAR, not_satisfied_counts={"tests-pass": 3})
    result = do(active(), req("close"), context(gates), three)
    assert result.state.wait is not None and result.state.wait.kind == "fail-gate"
    assert gate_results(result)["tests-pass#retry-limit"] == "satisfied"
    lower = do(
        active(),
        req("close"),
        context(
            gates,
        ),
        replace(CLEAR, not_satisfied_counts={"tests-pass": 2}),
    )
    assert lower.state.outcome == "done"


def paused_state() -> State:
    wait = Wait("fail-gate", "r", "human:ada", "a human recorded an override of flaky")
    return State(state="waiting", base_revision="r1", wait=wait)


def test_ae026_fail_closes_a_change_that_awaits_disposition() -> None:
    result = do(paused_state(), req("fail", reason="retry limit reached"))
    assert (result.state.state, result.state.outcome) == ("closed", "failed")
    assert result.state.reason == "retry limit reached"
    assert do(paused_state(), req("fail")).codes == ("reason-missing",)
    assert do(active(), req("fail", reason="x")).codes == ("state-illegal",)
    manual = State(state="waiting", wait=Wait("manual", "r", "human:ada", "x"))
    assert do(manual, req("fail", reason="x")).codes == ("state-illegal",)


def test_ae027_cancel_with_a_hard_failure_is_failed() -> None:
    facts = replace(CLEAR, scope=Check("satisfied", "docs/a.md"))
    result = do(active(), req("cancel"), facts=facts)
    assert (result.state.state, result.state.outcome) == ("closed", "failed")
    assert do(active(), req("cancel")).state.outcome == "cancelled"
    assert do(active(), req("cancel", AGENT)).codes == ("human-required",)


def test_cancel_of_a_change_awaiting_a_soft_failure_is_failed_with_a_reason() -> None:
    named = do(paused_state(), req("cancel"))
    assert named.state.outcome == "failed" and "flaky" in (named.state.reason or "")
    given = do(paused_state(), req("cancel", reason="enough"))
    assert given.state.reason == "enough"


def test_cancel_takes_effect_when_a_gate_cannot_be_evaluated() -> None:
    result = do(active(), req("cancel"), facts=replace(CLEAR, scope=None))
    assert result.state.outcome == "cancelled"
    assert gate_results(result)["scope-violation"] == "not_evaluable"
    assert gate_results(result)["incomplete-evidence"] == "not_applicable"


def test_supersede_records_replaced_by() -> None:
    facts = replace(CLEAR, open_changes=frozenset({"C-2"}))
    done = do(active(), req("supersede", replaced_by="C-2", reason="merged"), facts=facts)
    assert done.state.outcome == "cancelled" and done.state.replaced_by == "C-2"
    for target in (None, "C-1", "C-9"):
        bad = do(active(), req("supersede", replaced_by=target, reason="r"), facts=facts)
        assert bad.codes == ("replaced-by-invalid",)
    assert do(active(), req("supersede", replaced_by="C-2"), facts=facts).codes == (
        "reason-missing",
    )


def test_ae057_an_override_allows_exactly_the_granted_attempts() -> None:
    gates = definition(fail=[soft_gate()], done=[check_gate()])
    ctx = context(gates)
    run = runner({"pytest": RunOutcome("exit", status=1)})
    facts = replace(
        CLEAR, not_satisfied_counts={"tests-pass": 3}, definitions_hash="sha256:" + "c" * 64
    )
    paused = do(active(), req("close"), ctx, facts, run).state
    assert paused.wait is not None and paused.wait.resume_when.endswith("override of tries")
    assert do(paused, req("resume"), ctx, facts, run).codes == ("resume-condition-unmet",)
    approve = req("approve", target="override", gate="tries", reason="flaky CI", attempts=2)
    granted = do(paused, approve, ctx, facts, run).state
    state = do(granted, req("resume"), ctx, facts, run).state
    assert state.state == "active"  # the override is in force
    results = []
    for _ in range(3):
        outcome = do(state, req("close"), ctx, facts, run)
        results.append((outcome.result, outcome.state.state))
        state = outcome.state
        if outcome.state.state == "waiting":
            break
    assert results == [("blocked", "active"), ("blocked", "active"), ("blocked", "waiting")]
    assert state.wait is not None and state.wait.kind == "fail-gate"


def test_override_is_validated() -> None:
    wrong = req("approve", target="override", gate="tries", reason="r", attempts=1)
    assert do(active(), wrong).codes == ("override-invalid",)
    for attempts in (None, 0, -1, True):
        bad = req("approve", target="override", gate="flaky", reason="r", attempts=attempts)
        assert do(paused_state(), bad).codes == ("attempts-invalid",)
    no_reason = req("approve", target="override", gate="flaky", attempts=1)
    assert do(paused_state(), no_reason).codes == ("reason-missing",)
    other = req("approve", target="override", gate="other", reason="r", attempts=1)
    assert do(paused_state(), other).codes == ("override-invalid",)


def test_a_lapsed_override_has_no_effect() -> None:
    gates = definition(fail=[soft_gate()], done=[check_gate()])
    facts = replace(
        CLEAR, not_satisfied_counts={"tests-pass": 3}, definitions_hash="sha256:" + "d" * 64
    )
    override = Approval("override", "human:ada", "A1", "A0", gate="tries", attempts=2,
                        definitions_hash="sha256:" + "e" * 64)  # fmt: skip
    result = do(active(approvals=(override,)), req("close"), context(gates), facts)
    assert result.state.wait is not None and result.state.wait.kind == "fail-gate"


# --------------------------------------------------------------- resume details


def test_resume_of_an_external_wait_is_rejected_while_the_gate_still_cannot_run() -> None:
    gates = definition(done=[check_gate("docs-built", "mk")])
    run = runner({"mk": RunOutcome("cannot-start", program_missing=True)})
    waiting = do(active(), req("close"), context(gates), run=run).state
    assert do(waiting, req("resume"), context(gates), run=run).codes == ("resume-condition-unmet",)
    fixed = do(waiting, req("resume"), context(gates), run=runner())
    assert fixed.state.state == "active"


def test_resume_with_a_hard_failure_closes_as_failed_and_with_a_wait_gate_is_blocked() -> None:
    waiting = State(state="waiting", wait=Wait("manual", "r", "human:ada", "x"))
    hard = replace(CLEAR, scope=Check("satisfied", "docs/a"))
    result = do(waiting, req("resume", note="done"), facts=hard)
    assert result.result == "success" and result.state.outcome == "failed"
    stale = replace(CLEAR, stale_spec_approval=Check("satisfied"))
    blocked = do(waiting, req("resume", note="done"), facts=stale)
    assert blocked.result == "blocked" and blocked.state.wait == waiting.wait


# ----------------------------------------------------- adopt, owners, repair


def test_ae028_adopt_creates_no_change_of_state() -> None:
    result = do(active(), req("adopt"))
    assert result.state == active() and result.changed
    assert do(active(), req("adopt"), facts=replace(CLEAR, has_anchor=True)).codes == (
        "anchor-exists",
    )
    closed = State(state="closed", outcome="done")
    assert do(closed, req("adopt")).result == "success"


def test_ae325_handover_names_the_new_owner() -> None:
    ctx = context(change_owner="human:bo")
    result = do(active(), req("handover", owner="human:cy", reason="Bo left"), ctx)
    assert result.data == {"owner": "human:cy"} and result.state == active()
    assert do(
        active(), req("handover", Actor("human:zed"), owner="human:cy", reason="r"), ctx
    ).codes == ("not-owner",)
    assert do(active(), req("handover", owner="agent:x", reason="r"), ctx).codes == (
        "owner-not-approved",
    )
    assert do(active(), req("handover", owner="human:cy"), ctx).codes == ("reason-missing",)


def test_reassign_moves_a_question_or_a_wait() -> None:
    q = Question("Q1", "t", "human:bo", "agent:codex")
    state = active(questions=(q,))
    moved = do(state, req("reassign", question="Q1", owner="human:cy", reason="away"))
    assert moved.state.questions[0].owner == "human:cy"
    waiting = State(state="waiting", wait=Wait("manual", "r", "human:bo", "x"))
    reassigned = do(waiting, req("reassign", target="wait", owner="human:cy", reason="r"))
    assert reassigned.state.wait is not None and reassigned.state.wait.owner == "human:cy"
    assert do(state, req("reassign", question="Q9", owner="human:cy", reason="r")).codes == (
        "question-invalid",
    )
    assert do(state, req("reassign", owner="human:cy", reason="r")).codes == (
        "reassign-target-missing",
    )


def test_repair_needs_damage_the_owner_and_a_reason() -> None:
    damaged = replace(CLEAR, history_damaged=True)
    ok = do(active(), req("repair", reason="disk fault", repaired={"lost": 3}), facts=damaged)
    assert ok.bodies[0]["repaired"] == {"lost": 3}
    assert do(active(), req("repair", reason="r")).codes == ("history-consistent",)
    other = req("repair", Actor("human:bo"), reason="r")
    assert do(active(), other, facts=damaged).codes == ("not-owner",)
    assert do(active(), req("repair"), facts=damaged).codes == ("reason-missing",)


def test_unknown_action_is_rejected() -> None:
    assert do(active(), req("reopen")).codes == ("action-unknown",)


# --------------------------------------------------- properties: never raises


ACTIONS = (
    "new", "approve", "start", "wait", "ask", "answer", "resume", "close", "fail", "cancel",
    "supersede", "adopt", "conflict", "handover", "reassign", "repair", "nope",
)  # fmt: skip


@given(
    head=st.tuples(
        st.sampled_from(ACTIONS),
        st.sampled_from(["human:ada", "human:bo", "agent:codex", "agent:other", ""]),
        st.sampled_from(["open", "active", "waiting", "closed", None]),
    ),
    text=st.none() | st.text(max_size=6),
    number=st.none() | st.integers(-2, 4),
    flag=st.booleans(),
)
def test_apply_never_raises_and_keeps_the_envelope_rules(
    head: tuple[str, str, str | None], text: str | None, number: int | None, flag: bool
) -> None:
    action, who, state = head
    q = Question("Q1", "t", "human:ada", "agent:codex", options=("a", "b"))
    wait = Wait("question", "r", "human:ada", "Q1 answered", None, "Q1")
    current = None
    if state is not None:
        outcome = "cancelled" if state == "closed" else None
        current = State(
            state=state, outcome=outcome, questions=(q,), wait=wait if state == "waiting" else None
        )
    request = Request(
        action, Actor(who), NOW, reason=text, target=text, gate=text, question=text, text=text,
        owner=text, options=(text, text) if text else None, answer=text, resume_when=text,
        and_resume=flag, about_spec=flag, replaced_by=text, documents=(text or "", "b"),
        attempts=number, note=text,
    )  # fmt: skip
    result = apply(current, request, context(definition(done=[check_gate()])), CLEAR, runner())
    assert_consistent(result)


def test_parse_gates_adds_base_gates_and_skips_malformed_entries() -> None:
    gates = parse_gates({"fail": ["x", {"id": 1}, {"id": "a", "condition": 3}],
                         "wait": [{"id": "w", "condition": {"command": ["p"]}}],
                         "done": [{"id": "d", "kind": "check"}], "bogus": []})  # fmt: skip
    ids = [g.id for g in gates]
    assert ids[:4] == ["scope-violation", "unanswered-question", "stale-spec-approval",
                       "incomplete-evidence"]  # fmt: skip
    assert "w" in ids and "d" in ids and "a" not in ids
    assert parse_gates(None)[0].id == "scope-violation"


def test_a_gate_without_a_complete_command_cannot_be_evaluated() -> None:
    gates = definition(done=[{"id": "d", "kind": "check"}])
    result = do(active(), req("close"), context(gates))
    assert result.state.wait is not None and result.state.wait.kind == "external"


def test_sign_off_minimum_level() -> None:
    gates = definition(done=[{"id": "s", "kind": "sign-off", "minimum_level": "A2"}])
    ctx = context(gates)
    low = do(active(), req("approve", target="gate", gate="s"), ctx).state
    assert do(low, req("close"), ctx).result == "blocked"
    high = do(
        active(), req("approve", Actor("human:ada", "A2"), target="gate", gate="s"), ctx
    ).state
    assert do(high, req("close"), ctx).state.outcome == "done"


def test_a_blocked_chained_resume_keeps_its_issues() -> None:
    qs = (
        Question("Q1", "t", "human:ada", "agent:codex"),
        Question("Q2", "t", "human:ada", "agent:codex"),
    )
    wait = Wait("question", "r", "human:ada", "Q1 answered", None, "Q1")
    waiting = State(state="waiting", questions=qs, wait=wait)
    result = do(waiting, req("answer", question="Q1", answer="yes", and_resume=True))
    assert result.result == "blocked" and result.codes == ("wait-gate-active",)
    assert [b["action"] for b in result.bodies] == ["answer", "resume"]


def test_handover_records_the_new_owner_in_the_body() -> None:
    result = do(active(), req("handover", owner="human:cy", reason="Bo left"))
    note = str(result.bodies[0]["note"])
    assert "human:cy" in note and "Bo left" in note


def test_override_attempts_are_used_even_when_the_condition_is_inactive() -> None:
    gates = definition(fail=[cmd_gate("flaky", "soft", "flaky")])
    override = Approval("override", "human:ada", "A1", "A0", gate="flaky", attempts=2)
    state = active(approvals=(override,))
    quiet = runner({"flaky": RunOutcome("exit", status=0)})  # condition not active
    first = do(state, req("close"), context(gates), run=quiet)
    assert first.state.outcome == "done"
    again = do(
        active(approvals=(replace(override, used=1),)), req("close"), context(gates), run=quiet
    )
    assert again.state.approvals[0].used == 2


def test_equal_duplicate_overrides_do_not_double_the_attempts() -> None:
    gates = definition(fail=[cmd_gate("flaky", "soft", "flaky")])
    override = Approval("override", "human:ada", "A1", "A0", gate="flaky", attempts=2)
    state = active(approvals=(override, replace(override)))
    loud = runner({"flaky": RunOutcome("exit", status=1)})
    after = do(state, req("close"), context(gates), run=loud).state
    assert [a.used for a in after.approvals] == [0, 1]


def test_and_resume_applies_only_to_the_question_the_change_waits_for() -> None:
    q1 = Question("Q1", "t", "human:ada", "agent:codex")
    q2 = Question("Q2", "t", "human:ada", "agent:codex", answer="yes", answerer="human:ada")
    wait = Wait("question", "r", "human:ada", "Q2 answered", None, "Q2")
    waiting = State(state="waiting", questions=(q1, q2), wait=wait)
    result = do(waiting, req("answer", question="Q1", answer="yes", and_resume=True))
    assert result.state.state == "waiting" and result.state.wait == wait
    assert [b["action"] for b in result.bodies] == ["answer"]
