"""The protections: frozen gates, higher documents, identity, levels, roles.

AE-033, AE-035, AE-037, AE-040, AE-041, AE-042, AE-313, AE-319, AE-320, AE-326.
"""

from __future__ import annotations

from dataclasses import replace

from engine_helpers import (
    ADA,
    AGENT,
    CLEAR,
    active,
    check_gate,
    context,
    definition,
    do,
    req,
    runner,
)

from ggsad.core.engine_types import Actor
from ggsad.core.gate_eval import Check, RunOutcome
from ggsad.core.state import Approval, Question, State, Wait

H1 = "sha256:" + "1" * 64
H2 = "sha256:" + "2" * 64
S1 = "sha256:" + "a" * 64
S2 = "sha256:" + "b" * 64
DOC = {"docs/architecture.md": "sha256:" + "c" * 64}
APPROVED = Approval("gates", "human:ada", "A0", "A0", content_hash=H1, definitions_hash=H1)
LEGAL = definition(done=[{"id": "legal-ok", "kind": "sign-off"}])


def with_hash(value: str | None, **kw: object):
    return replace(CLEAR, definitions_hash=value, **kw)


# ----------------------------------------------------------- frozen gates (24.1)


def test_ae035_a_changed_gate_definition_stops_the_action_and_writes_nothing() -> None:
    state = active(approvals=(APPROVED,))
    result = do(state, req("close"), facts=with_hash(H2))
    assert result.result == "rejected" and result.codes == ("gates-changed",)
    assert not result.changed and result.state == state
    assert do(state, req("close"), facts=with_hash(H1)).state.outcome == "done"


def test_nothing_is_fixed_before_the_first_approval() -> None:
    assert do(active(), req("close"), facts=with_hash(H2)).state.outcome == "done"


def test_cancel_and_supersede_are_exempt_from_the_comparison() -> None:
    state = active(approvals=(APPROVED,))
    changed = replace(with_hash(H2), open_changes=frozenset({"C-2"}))
    assert do(state, req("cancel"), facts=changed).state.outcome == "cancelled"
    done = do(state, req("supersede", replaced_by="C-2", reason="r"), facts=changed)
    assert done.state.replaced_by == "C-2"


def test_other_approvals_are_stopped_while_the_gates_differ() -> None:
    state = active(approvals=(APPROVED,))
    assert do(state, req("approve", target="spec"), facts=with_hash(H2)).codes == ("gates-changed",)


def test_ae037_gate_definitions_that_are_absent_cannot_be_approved() -> None:
    result = do(State(), req("approve", target="gates"), facts=with_hash(None))
    assert result.codes == ("gates-missing",)


def test_the_first_approval_records_the_hash_and_a_reapproval_is_an_amendment() -> None:
    first = do(State(), req("approve", target="gates"), facts=with_hash(H1)).state
    assert first.approvals[-1].target == "gates" and first.approvals[-1].content_hash == H1
    amended = do(
        first, req("approve", target="gates", text="severity softened"), facts=with_hash(H2)
    )
    last = amended.state.approvals[-1]
    assert (last.target, last.replaced_hash, last.content_hash) == ("amendment", H1, H2)
    assert last.summary == "severity softened"
    running = amended.state.with_(state="active", base_revision="r1")
    assert do(running, req("close"), facts=with_hash(H2)).state.outcome == "done"


def test_ae319_an_override_bound_to_the_earlier_hash_lapses_after_the_amendment() -> None:
    cond = {"retry_limit": {"gate": "tests-pass", "limit": 3}}
    gates = definition(fail=[{"id": "tries", "severity": "soft", "condition": cond}],
                       done=[check_gate()])  # fmt: skip
    ctx = context(gates)
    facts = replace(with_hash(H1), not_satisfied_counts={"tests-pass": 3})
    wait = Wait("fail-gate", "r", "human:ada", "a human recorded an override of tries")
    paused = State(state="waiting", base_revision="r1", wait=wait, approvals=(APPROVED,))
    granted = do(paused, req("approve", target="override", gate="tries", reason="r", attempts=2),
                 ctx, facts).state  # fmt: skip
    assert granted.approvals[-1].definitions_hash == H1
    resumed = do(granted, req("resume"), ctx, facts).state
    assert resumed.state == "active"
    amended = do(resumed, req("approve", target="gates"), ctx, replace(facts, definitions_hash=H2))
    after = replace(facts, definitions_hash=H2)
    result = do(amended.state, req("close"), ctx, after)
    assert result.state.wait is not None and result.state.wait.kind == "fail-gate"


def test_a_stale_sign_off_leaves_a_question_that_the_next_sign_off_answers() -> None:
    ctx = context(LEGAL)
    first = do(active(approvals=(APPROVED,)), req("approve", target="gate", gate="legal-ok"),
               ctx, with_hash(H1)).state  # fmt: skip
    assert do(first, req("close"), ctx, with_hash(H1)).state.outcome == "done"
    amended = do(first, req("approve", target="gates"), ctx, with_hash(H2)).state
    question = amended.unanswered[0]
    assert question.owner == "human:ada" and "legal-ok" in question.text
    blocked = do(amended, req("close"), ctx, with_hash(H2))
    assert blocked.result == "blocked"
    signed = do(amended, req("approve", target="gate", gate="legal-ok"), ctx, with_hash(H2)).state
    assert signed.unanswered == () and signed.questions[0].answer == "signed off"
    assert do(signed, req("close"), ctx, with_hash(H2)).state.outcome == "done"


# --------------------------------------------------- higher documents (Section 4)


def spec_approved(documents: dict[str, str]) -> State:
    approval = Approval("spec", "human:ada", "A0", "A0", content_hash=S1,
                        documents=tuple(sorted(documents.items())))  # fmt: skip
    return active(approvals=(approval,))


def test_ae313_an_edit_of_a_higher_document_stops_the_change_until_approved() -> None:
    state = spec_approved(DOC)
    edited = replace(CLEAR, documents={"docs/architecture.md": "sha256:" + "d" * 64}, spec_hash=S1)
    result = do(state, req("close"), facts=edited)
    assert result.codes == ("higher-documents-changed",)
    assert "docs/architecture.md" in result.issues[0].message and not result.changed
    approved = do(state, req("approve", target="documents"), facts=edited).state
    assert approved.approvals[-1].target == "documents"
    assert do(approved, req("close"), facts=edited).state.outcome == "done"


def test_higher_documents_that_appear_or_vanish_count_as_changed() -> None:
    state = spec_approved(DOC)
    gone = replace(CLEAR, documents={}, spec_hash=S1)
    assert do(state, req("close"), facts=gone).codes == ("higher-documents-changed",)
    extra = replace(CLEAR, documents={**DOC, "docs/adr/ADR-1.md": S2}, spec_hash=S1)
    assert do(state, req("close"), facts=extra).codes == ("higher-documents-changed",)


def test_cancel_is_exempt_and_unchanged_documents_cannot_be_approved() -> None:
    state = spec_approved(DOC)
    edited = replace(CLEAR, documents={}, spec_hash=S1)
    assert do(state, req("cancel"), facts=edited).state.outcome == "cancelled"
    same = replace(CLEAR, documents=DOC, spec_hash=S1)
    assert do(state, req("approve", target="documents"), facts=same).codes == (
        "documents-unchanged",
    )
    assert do(state, req("close"), facts=same).state.outcome == "done"


def test_the_spec_approval_records_the_fingerprint_and_the_spec_hash() -> None:
    facts = replace(CLEAR, documents=DOC, spec_hash=S1)
    approval = do(State(), req("approve", target="spec"), facts=facts).state.approvals[-1]
    assert dict(approval.documents) == DOC and approval.content_hash == S1


def test_ae033_a_changed_spec_makes_its_approval_stale_until_approved_again() -> None:
    state = spec_approved({})
    edited = replace(CLEAR, spec_hash=S2)
    blocked = do(state, req("close"), facts=edited)
    assert blocked.result == "blocked" and "spec.md changed" in blocked.issues[0].message
    again = do(state, req("approve", target="spec"), facts=edited).state
    assert do(again, req("close"), facts=edited).state.outcome == "done"
    never = replace(CLEAR, spec_hash=S2)  # never approved: not stale
    assert do(active(), req("close"), facts=never).state.outcome == "done"


# ------------------------------------------------------ identity and levels (24.3)


def test_ae040_a_non_human_identity_cannot_cancel() -> None:
    assert do(active(), req("cancel", Actor("agent:builder"))).codes == ("human-required",)
    assert do(active(), req("cancel", Actor("builder"))).codes == ("human-required",)


def test_ae320_a_human_that_is_not_on_the_list_is_rejected() -> None:
    ctx = context(approved_humans=frozenset({"human:ada", "human:bo"}))
    eve = Actor("human:eve")
    assert do(State(), req("approve", eve, target="spec"), ctx).codes == ("human-not-approved",)
    assert do(State(), req("approve", ADA, target="spec"), ctx).result == "success"
    assert do(active(), req("cancel", eve), ctx).codes == ("human-not-approved",)


def test_the_resume_after_an_answer_is_allowed_for_the_owner_of_the_wait() -> None:
    q = Question("Q1", "t", "human:bo", "agent:codex")
    wait = Wait("question", "r", "human:bo", "Q1 answered", None, "Q1")
    waiting = State(state="waiting", questions=(q,), wait=wait)
    ctx = context(approved_humans=frozenset({"human:ada"}), change_owner="human:bo")
    bo = Actor("human:bo")
    result = do(waiting, req("answer", bo, question="Q1", answer="yes", and_resume=True), ctx)
    assert result.codes == ("human-not-approved",)
    listed = context(approved_humans=frozenset({"human:ada", "human:bo"}), change_owner="human:bo")
    both = do(waiting, req("answer", bo, question="Q1", answer="yes", and_resume=True), listed)
    assert both.state.state == "active"


def test_ae041_an_unsigned_claim_is_a_claim_at_a0_and_is_accepted_by_default() -> None:
    result = do(State(), req("approve", Actor("human:ada"), target="spec"))
    assert result.state.approvals[0].assurance == "A0"
    assert result.state.approvals[0].required_level == "A0"


def test_a_required_level_above_the_claim_is_rejected_and_recorded_when_met() -> None:
    ctx = context(minimum_levels={"spec_approval": "A1"})
    low = do(State(), req("approve", Actor("human:ada", "A0"), target="spec"), ctx)
    assert low.codes == ("assurance-too-low",) and not low.changed
    ok = do(State(), req("approve", Actor("human:ada", "A1"), target="spec"), ctx)
    assert ok.state.approvals[0].required_level == "A1"


def test_ae042_a_lowered_minimum_does_not_lower_the_level_the_history_used() -> None:
    first = Approval("spec", "human:ada", "A2", "A2", content_hash=S1)
    state = State(approvals=(first,))
    ctx = context(minimum_levels={"spec_approval": "A0"})
    result = do(state, req("approve", Actor("human:ada", "A0"), target="spec"), ctx)
    assert result.codes == ("assurance-too-low",)
    assert do(state, req("approve", Actor("human:ada", "A2"), target="spec"), ctx).changed


def test_the_higher_of_the_gate_minimum_and_the_settings_applies_to_a_sign_off() -> None:
    gates = definition(done=[{"id": "legal-ok", "kind": "sign-off", "minimum_level": "A1"}])
    ctx = context(gates, minimum_levels={"sign_off": "A2"})
    one = req("approve", Actor("human:ada", "A1"), target="gate", gate="legal-ok")
    assert do(active(), one, ctx).codes == ("assurance-too-low",)
    two = req("approve", Actor("human:ada", "A2"), target="gate", gate="legal-ok")
    assert do(active(), two, ctx).state.approvals[0].required_level == "A2"


def test_levels_apply_to_answers_and_cancel_too() -> None:
    ctx = context(minimum_levels={"cancel": "A1", "answer": "A1"})
    assert do(active(), req("cancel", Actor("human:ada", "A0")), ctx).codes == (
        "assurance-too-low",
    )
    assert do(active(), req("cancel", Actor("human:ada", "A1")), ctx).state.outcome == "cancelled"


# ----------------------------------------------------------------------- roles


def test_ae326_the_same_person_as_author_and_approver_depends_on_profile_and_mode() -> None:
    cases = [
        ("lean", "team", True),
        ("lean", "solo", True),
        ("standard", "team", False),
        ("standard", "solo", True),
        ("governed", "team", False),
        ("governed", "solo", True),
        ("regulated", "team", False),
        ("regulated", "solo", False),
    ]
    for profile, mode, allowed in cases:
        ctx = context(compliance_profile=profile, team_mode=mode)
        result = do(State(), req("approve", target="spec"), ctx)
        assert (result.result == "success") is allowed, (profile, mode)
        if not allowed:
            assert result.codes == ("roles-not-separate",)


def test_only_the_approver_approves_and_a_deputy_stands_in_when_recorded_unavailable() -> None:
    ctx = context(author="human:cy", approver="human:bo", owner="human:ada",
                  deputies=frozenset({"human:dee"}))  # fmt: skip
    assert do(State(), req("approve", ADA, target="spec"), ctx).codes == ("not-approver",)
    assert do(State(), req("approve", Actor("human:bo"), target="spec"), ctx).changed
    away = replace(ctx, unavailable_approvers=frozenset({"human:bo"}))
    dee = Actor("human:dee")
    assert do(State(), req("approve", dee, target="spec"), away).changed
    assert do(State(), req("approve", dee, target="spec"), ctx).codes == ("not-approver",)


def test_the_owner_and_deputies_may_give_the_reapproval_of_the_gates() -> None:
    ctx = context(author="human:cy", approver="human:bo", owner="human:ada",
                  deputies=frozenset({"human:dee"}))  # fmt: skip
    state = State(approvals=(APPROVED,))
    for who in ("human:ada", "human:dee", "human:bo"):
        result = do(state, req("approve", Actor(who), target="gates"), ctx, with_hash(H2))
        assert result.state.approvals[-1].target == "amendment", who
    other = do(state, req("approve", Actor("human:zed"), target="gates"), ctx, with_hash(H2))
    assert other.codes == ("not-approver",)


def test_a_hard_failure_and_a_missing_program_still_work_with_guards_in_place() -> None:
    facts = replace(CLEAR, scope=Check("satisfied", "docs/a.md"))
    assert do(active(), req("close"), facts=facts).state.outcome == "failed"
    gates = definition(done=[check_gate("docs-built", "mk")])
    run = runner({"mk": RunOutcome("cannot-start", program_missing=True)})
    assert do(active(), req("close"), context(gates), run=run).state.wait is not None
    assert do(State(), req("start", AGENT)).result == "success"
