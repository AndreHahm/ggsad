"""The handlers of the actions of Section 23.4. Each raises `Rejected` or returns a `Step`."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Final

from ggsad.core.engine_types import Call, Rejected, Step
from ggsad.core.gate_eval import NOT_EVALUABLE, Decision, Evaluation, override_in_force, probe
from ggsad.core.guards import approved_hash, recorded_documents, required_level
from ggsad.core.issues import Issue
from ggsad.core.state import Approval, Question, State, Wait

if TYPE_CHECKING:
    from collections.abc import Callable

APPROVE_TARGETS: Final = frozenset(
    {"spec", "gates", "review", "documents", "all", "override", "gate"}
)
OVERRIDE_PREFIX: Final = "a human recorded an override of "
MIN_OPTIONS: Final = 2
HANDLERS: dict[str, Callable[[Call], Step]] = {}


def handler(name: str) -> Callable[[Callable[[Call], Step]], Callable[[Call], Step]]:
    """Register a handler under the name of its action."""

    def register(function: Callable[[Call], Step]) -> Callable[[Call], Step]:
        HANDLERS[name] = function
        return function

    return register


# ------------------------------------------------------------------ helpers


def _closed(state: State, outcome: str, reason: str | None = None) -> State:
    return state.with_(state="closed", outcome=outcome, wait=None, reason=reason)


def _failed_by(decision: Decision) -> str:
    return f"a hard fail condition is active: {decision.detail}"


def _blocked(ev: Evaluation, code: str, state: State) -> Step:
    message = f"{ev.decision.detail}" if ev.decision.detail else code
    return Step(state, "blocked", (Issue(code, message),), evaluation=ev)


def wait_gate(wait: Wait) -> str:
    """The identifier of the gate that a wait of the kind `fail-gate` or `external` names."""
    text = wait.resume_when
    if text.startswith(OVERRIDE_PREFIX):
        return text[len(OVERRIDE_PREFIX) :]
    if text.startswith("gate ") and text.endswith(" can be evaluated"):
        return text[len("gate ") : -len(" can be evaluated")]
    return ""


def _wait_from(call: Call, decision: Decision) -> Wait:
    """The wait record that an evaluation creates (Section 23.5)."""
    gate_id = decision.gate_ids[0]
    owner = call.context.change_owner
    if decision.kind == "external":
        reason = f"gate {gate_id} cannot be evaluated: {decision.detail}"
        return Wait("external", reason, owner, f"gate {gate_id} can be evaluated")
    reason = f"soft fail condition {gate_id} is active: {decision.detail}"
    return Wait("fail-gate", reason, owner, f"{OVERRIDE_PREFIX}{gate_id}")


def _with_wait(call: Call, ev: Evaluation, state: State) -> Step:
    """Wait after an evaluation that found a gate that cannot be evaluated or a soft failure."""
    wait = _wait_from(call, ev.decision)
    code = "gate-not-evaluable" if ev.decision.kind == "external" else "soft-failure"
    return _blocked(ev, code, state.with_(state="waiting", wait=wait))


def _bump_attempts(call: Call, ev: Evaluation) -> State:
    """Count one attempt on every override in force, whether or not its condition is active now."""
    state = call.state
    if ev.decision.kind in ("fail", "external"):
        return state
    forced = [override_in_force(state, g, call.facts) for g in _override_gates(state)]
    used_up = {id(a) for a in forced if a is not None}
    approvals = tuple(
        replace(a, used=a.used + 1) if id(a) in used_up else a for a in state.approvals
    )
    return state.with_(approvals=approvals)


def _override_gates(state: State) -> list[str]:
    return list(dict.fromkeys(a.gate or "" for a in state.approvals if a.target == "override"))


def _owner_or_default(call: Call, about_spec: bool) -> str:
    request, context = call.request, call.context
    owner = request.owner or (context.author if about_spec else context.change_owner)
    if not context.is_approved_human(owner):
        raise Rejected("owner-not-approved", f"{owner!r} is not an approved human")
    return owner


# ---------------------------------------------------------------------- new


@handler("new")
def _new(_call: Call) -> Step:
    return Step(State())


# ------------------------------------------------------------------ approve


def _check_approve(call: Call) -> str:
    request, state = call.request, call.state
    target = request.target
    if target not in APPROVE_TARGETS or target is None:
        raise Rejected("approve-target-invalid", f"{target!r} is not a target of an approval")
    for code, message in call.facts.target_issues.get(f"approve:{target}", ()):
        raise Rejected(code, message)
    if target in ("spec", "all"):
        _no_open_questions(state)
    if target in ("gates", "all") and call.facts.definitions_hash is None:
        raise Rejected("gates-missing", "the change definition has no gate definitions to approve")
    return target


@handler("approve")
def _approve(call: Call) -> Step:
    target, state = _check_approve(call), call.state
    if target == "gate":
        return _sign_off_step(call)
    if target == "override":
        approvals = (_override_approval(call),)
    else:
        names = ("spec", "gates") if target == "all" else (target,)
        approvals = tuple(_approval(call, name) for name in names)
    questions = _stale_sign_off_questions(call) if approvals[-1].target == "amendment" else ()
    return Step(
        state.with_(
            approvals=(*state.approvals, *approvals), questions=(*state.questions, *questions)
        )
    )


def _no_open_questions(state: State) -> None:
    if state.unanswered:
        ids = ", ".join(q.id for q in state.unanswered)
        raise Rejected("open-questions", f"these questions are unanswered: {ids}")


def _approval(call: Call, target: str) -> Approval:
    """The approval record of a target, bound to the content it approves (Section 24.3)."""
    request, facts = call.request, call.facts
    base = Approval(
        target=target,
        actor=request.actor.identity,
        assurance=request.actor.assurance,
        required_level=required_level(call),
        content_hash=request.content_hash,
    )
    if target == "spec":
        return replace(
            base,
            content_hash=facts.spec_hash or request.content_hash,
            documents=tuple(sorted(facts.documents.items())),
        )
    if target == "documents":
        return _documents_approval(call, base)
    if target == "gates":
        return _gates_approval(call, base)
    return base


def _documents_approval(call: Call, base: Approval) -> Approval:
    recorded = recorded_documents(call.state)
    current = dict(call.facts.documents)
    if recorded is not None and recorded == current:
        raise Rejected("documents-unchanged", "the higher-ranking documents did not change")
    return replace(base, documents=tuple(sorted(current.items())))


def _gates_approval(call: Call, base: Approval) -> Approval:
    """The first approval of the gate definitions, or the amendment that replaces the hash."""
    new = call.facts.definitions_hash
    old = approved_hash(call.state)
    if old is None or old == new:
        return replace(base, content_hash=new, definitions_hash=new)
    return replace(
        base,
        target="amendment",
        content_hash=new,
        definitions_hash=new,
        replaced_hash=old,
        summary=call.request.text,
    )


def _stale_text(gate_id: str) -> str:
    return f"The gate definitions changed. Please sign off {gate_id} again."


def _stale_signers(call: Call) -> list[Approval]:
    """The sign-offs that are bound to the replaced hash, for gates that still exist."""
    old = approved_hash(call.state)
    gates = {g.id for g in call.context.gates if g.kind == "sign-off"}
    signed = {a.gate: a for a in call.state.approvals if a.target == "gate" and a.gate in gates}
    return [a for a in signed.values() if a.definitions_hash == old]


def _stale_sign_off_questions(call: Call) -> tuple[Question, ...]:
    """One question per sign-off that the amendment makes stale (Section 24.3)."""
    first = len(call.state.questions) + 1
    asker = call.request.actor.identity
    return tuple(
        Question(f"Q{first + i}", _stale_text(a.gate or ""), a.actor, asker)
        for i, a in enumerate(_stale_signers(call))
    )


def _sign_off_step(call: Call) -> Step:
    """A sign-off; it answers the question that a stale sign-off left, in the same entry."""
    state = call.state
    approval = _gate_approval(call)
    text = _stale_text(approval.gate or "")
    questions = tuple(
        replace(q, answer="signed off", answerer=approval.actor)
        if not q.answered and q.text == text
        else q
        for q in state.questions
    )
    return Step(state.with_(approvals=(*state.approvals, approval), questions=questions))


def _gate_approval(call: Call) -> Approval:
    name = call.request.gate
    gate = next((g for g in call.context.gates if g.id == name), None)
    if gate is None or gate.group != "done" or gate.kind != "sign-off":
        raise Rejected("gate-not-sign-off", f"{name!r} is not a sign-off done gate of the change")
    base = _approval(call, "gate")
    return replace(base, gate=name, definitions_hash=call.facts.definitions_hash)


def _override_approval(call: Call) -> Approval:
    request, wait = call.request, call.state.wait
    waiting_for = wait_gate(wait) if wait is not None and wait.kind == "fail-gate" else None
    if waiting_for is None or request.gate != waiting_for:
        raise Rejected(
            "override-invalid",
            "an override applies only to a soft fail condition that awaits disposition",
        )
    reason = call.need(request.reason, "reason-missing", "an override needs a reason")
    attempts = request.attempts
    if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1:
        raise Rejected(
            "attempts-invalid", "an override gives a whole number of attempts, at least 1"
        )
    base = replace(_approval(call, "override"), definitions_hash=call.facts.definitions_hash)
    return replace(base, gate=waiting_for, reason=reason, attempts=attempts)


# -------------------------------------------------------------------- start


@handler("start")
def _start(call: Call) -> Step:
    facts = call.facts
    if not facts.gates_approved:
        raise Rejected(
            "gates-not-approved", "the gate definitions are not approved or have changed"
        )
    if not facts.spec_approval_ok:
        raise Rejected("spec-not-approved", "the specification must be approved before the start")
    if facts.revision is None:
        raise Rejected("base-revision-unavailable", "the revision to start from cannot be recorded")
    if facts.unclean_paths:
        paths = ", ".join(facts.unclean_paths)
        raise Rejected(
            "working-copy-unclean", f"uncommitted work outside the record files: {paths}"
        )
    ev = call.evaluate()
    if ev.decision.kind != "none":
        raise Rejected("start-blocked", ev.decision.detail or ev.decision.kind)
    return Step(call.state.with_(state="active", base_revision=facts.revision), evaluation=ev)


# --------------------------------------------------------------- wait / ask


@handler("wait")
def _wait(call: Call) -> Step:
    request = call.request
    wait = _question_wait(call) if request.question else _manual_wait(call)
    return Step(call.state.with_(state="waiting", wait=wait))


def _question_wait(call: Call) -> Wait:
    request = call.request
    question = call.state.question(request.question or "")
    if question is None or question.answered:
        raise Rejected("question-invalid", "the question does not exist or is answered")
    if request.owner is not None and request.owner != question.owner:
        raise Rejected("owner-mismatch", "the owner of the wait is the owner of the question")
    return Wait(
        "question",
        request.reason or f"awaiting the answer to {question.id}",
        question.owner,
        request.resume_when or f"{question.id} answered",
        request.expires,
        question.id,
    )


def _manual_wait(call: Call) -> Wait:
    request = call.request
    reason = call.need(request.reason, "reason-missing", "a wait needs a reason")
    resume = call.need(request.resume_when, "resume-condition-missing", "a wait needs a condition")
    owner = request.owner
    if not call.context.is_approved_human(owner) or owner is None:
        raise Rejected("owner-not-approved", "the owner of a wait is an approved human")
    return Wait("manual", reason, owner, resume, request.expires)


def _options(options: tuple[str, ...] | None) -> tuple[str, ...] | None:
    if options is None:
        return None
    if (
        len(set(options)) != len(options)
        or len(options) < MIN_OPTIONS
        or not all(o.strip() for o in options)
    ):
        raise Rejected("options-invalid", "a structured question has at least two distinct options")
    return options


@handler("ask")
def _ask(call: Call) -> Step:
    request, state = call.request, call.state
    text = call.need(request.text, "text-missing", "a question needs a text")
    options = _options(request.options)
    owner = _owner_or_default(call, request.about_spec)
    number = len(state.questions) + 1
    question = Question(f"Q{number}", text, owner, request.actor.identity, options)
    return Step(state.with_(questions=(*state.questions, question)))


@handler("conflict")
def _conflict(call: Call) -> Step:
    request, state = call.request, call.state
    text = call.need(request.text, "text-missing", "a conflict needs a text")
    documents = request.documents
    if len(set(documents)) < MIN_OPTIONS:
        raise Rejected("documents-missing", "a conflict names two documents")
    owner = _owner_or_default(call, "spec.md" in documents)
    asked = f"{text} ({' / '.join(documents)})"
    question = Question(f"Q{len(state.questions) + 1}", asked, owner, request.actor.identity)
    wait = Wait("question", f"conflict between {' and '.join(documents)}", owner,
                f"{question.id} answered", None, question.id)  # fmt: skip
    return Step(state.with_(state="waiting", questions=(*state.questions, question), wait=wait))


# ------------------------------------------------------------------- answer


@handler("answer")
def _answer(call: Call) -> Step:
    request, state = call.request, call.state
    question = state.question(request.question or "")
    if question is None or question.answered:
        raise Rejected("question-invalid", "the question does not exist or is already answered")
    if request.actor.identity != question.owner:
        raise Rejected("answer-not-owner", "only the owner of a question answers it")
    answer = _valid_answer(question, request.answer)
    done = replace(question, answer=answer, answerer=request.actor.identity)
    questions = tuple(done if q.id == question.id else q for q in state.questions)
    step = Step(state.with_(questions=questions))
    if request.and_resume:
        step.chained = _chained_resume(call, step.state)
    return step


def _valid_answer(question: Question, answer: str | None) -> str:
    if question.options is not None:
        if answer not in question.options:
            raise Rejected("answer-invalid", "the answer is not one of the options")
        return answer
    if answer is None or not answer.strip():
        raise Rejected("answer-invalid", "the answer to a free-text question is not empty")
    return answer


def _may_resume(call: Call, wait: Wait) -> bool:
    """The answerer resumes when approved or when the owner of the wait (Section 24.3)."""
    actor = call.request.actor.identity
    return call.context.is_approved_human(actor) or actor == wait.owner


def _chained_resume(call: Call, state: State) -> Step | None:
    """Answer and resume as one step, when the answerer may resume and the change waits for it."""
    wait = state.wait
    if (
        wait is None
        or wait.kind != "question"
        or wait.question != call.request.question
        or not _may_resume(call, wait)
    ):
        return None
    chained = replace(call, state=state, request=replace(call.request, action="resume"))
    try:
        step = _resume(chained)
    except Rejected:
        return None
    step.action = "resume"
    return step


# ------------------------------------------------------------------- resume


def _resume_allowed(call: Call, wait: Wait) -> None:
    state = call.state
    if wait.kind == "question":
        question = state.question(wait.question or "")
        if question is None or not question.answered:
            raise Rejected("resume-condition-unmet", "the awaited question is not answered")
    elif wait.kind == "fail-gate":
        if override_in_force(state, wait_gate(wait), call.facts) is None:
            raise Rejected("resume-condition-unmet", "no override of the soft failure is in force")
    elif wait.kind == "manual":
        call.need(call.request.note, "note-missing", "a manual wait needs a note of one sentence")
    else:
        _check_evaluable(call, wait)


def _check_evaluable(call: Call, wait: Wait) -> None:
    """A wait of the kind `external` ends when the gate can be evaluated again."""
    outcome = probe(wait_gate(wait), call.context.gates, call.state, call.facts, call.runner)
    if outcome.result == NOT_EVALUABLE:
        raise Rejected("resume-condition-unmet", f"still cannot be evaluated: {outcome.detail}")


@handler("resume")
def _resume(call: Call) -> Step:
    wait = call.state.wait
    if wait is None:
        raise Rejected("state-illegal", "the change is not waiting")
    _resume_allowed(call, wait)
    ev = call.evaluate()
    kind = ev.decision.kind
    state = call.state
    if kind == "none":
        return Step(state.with_(state="active", wait=None), evaluation=ev)
    if kind == "fail":
        return Step(_closed(state, "failed", _failed_by(ev.decision)), evaluation=ev)
    if kind == "wait":
        return _blocked(ev, "wait-gate-active", state)
    if (
        kind == "external"
        and wait.kind == "external"
        and ev.decision.gate_ids[0] == wait_gate(wait)
    ):
        raise Rejected("resume-condition-unmet", f"still cannot be evaluated: {ev.decision.detail}")
    return _with_wait(call, ev, state)


# -------------------------------------------------------------------- close


@handler("close")
def _close(call: Call) -> Step:
    agent = not call.request.actor.is_human
    if agent and call.request.agent_report is None:
        raise Rejected("agent-report-missing", "an agent closes a change with an agent report")
    ev = call.evaluate()
    if ev.decision.kind == "none" and agent and not call.context.agent_may_close:
        raise Rejected("human-close-required", "a human closes a change as done")
    return _close_decided(call, ev)


def _close_decided(call: Call, ev: Evaluation) -> Step:
    kind = ev.decision.kind
    after = _bump_attempts(call, ev)
    if kind == "none":
        return Step(_closed(after, "done"), evaluation=ev)
    if kind == "fail":
        return Step(_closed(call.state, "failed", _failed_by(ev.decision)), evaluation=ev)
    if kind in ("external", "soft"):
        return _with_wait(call, ev, after)
    code = "wait-gate-active" if kind == "wait" else "done-gate-unsatisfied"
    return _blocked(ev, code, after)


# --------------------------------------------------------- fail / cancel / supersede


@handler("fail")
def _fail(call: Call) -> Step:
    wait = call.state.wait
    if wait is None or wait.kind != "fail-gate":
        raise Rejected("state-illegal", "no soft failure awaits disposition")
    reason = call.need(call.request.reason, "reason-missing", "failing a change needs a reason")
    return Step(_closed(call.state, "failed", reason))


def _end(call: Call, replaced_by: str | None = None) -> Step:
    state, request = call.state, call.request
    ev = call.evaluate()
    if ev.decision.kind == "fail":
        closed = _closed(state, "failed", _failed_by(ev.decision))
    elif state.wait is not None and state.wait.kind == "fail-gate":
        reason = (
            request.reason or f"soft fail condition {wait_gate(state.wait)} awaited disposition"
        )
        closed = _closed(state, "failed", reason)
    else:
        closed = _closed(state, "cancelled")
    return Step(closed.with_(replaced_by=replaced_by), evaluation=ev)


@handler("cancel")
def _cancel(call: Call) -> Step:
    return _end(call)


@handler("supersede")
def _supersede(call: Call) -> Step:
    request, context = call.request, call.context
    target = request.replaced_by
    if target is None or target == context.change_id or target not in call.facts.open_changes:
        raise Rejected(
            "replaced-by-invalid", "replaced_by names a different change that exists and is open"
        )
    call.need(request.reason, "reason-missing", "superseding a change records a reason")
    return _end(call, target)


# ----------------------------------------------------- adopt / owners / repair


@handler("adopt")
def _adopt(call: Call) -> Step:
    if call.facts.has_anchor:
        raise Rejected("anchor-exists", "the history has an anchor already")
    return Step(call.state)


@handler("handover")
def _handover(call: Call) -> Step:
    request, context = call.request, call.context
    if request.actor.identity not in (context.owner, context.change_owner):
        raise Rejected("not-owner", "only the Owner or the Change owner hands a change over")
    new_owner = _owner_or_default_strict(call)
    call.need(request.reason, "reason-missing", "a handover gives a reason")
    note = f"new Change owner {new_owner}: {request.reason}"
    return Step(call.state, data={"owner": new_owner}, note=note)


def _owner_or_default_strict(call: Call) -> str:
    owner = call.request.owner
    if owner is None or not call.context.is_approved_human(owner):
        raise Rejected("owner-not-approved", f"{owner!r} is not an approved human")
    return owner


@handler("reassign")
def _reassign(call: Call) -> Step:
    request, context, state = call.request, call.context, call.state
    if request.actor.identity not in (context.owner, context.change_owner):
        raise Rejected("not-owner", "only the Owner or the Change owner reassigns")
    new_owner = _owner_or_default_strict(call)
    call.need(request.reason, "reason-missing", "a reassignment gives a reason")
    if request.question is not None:
        question = state.question(request.question)
        if question is None:
            raise Rejected("question-invalid", "the question does not exist")
        moved = replace(question, owner=new_owner)
        return Step(
            state.with_(questions=tuple(moved if q.id == moved.id else q for q in state.questions))
        )
    if request.target == "wait" and state.wait is not None:
        return Step(state.with_(wait=replace(state.wait, owner=new_owner)))
    raise Rejected("reassign-target-missing", "name the question or the wait to reassign")


@handler("repair")
def _repair(call: Call) -> Step:
    if not call.facts.history_damaged:
        raise Rejected("history-consistent", "the history is consistent and complete")
    if call.request.actor.identity != call.context.owner:
        raise Rejected("not-owner", "only the Owner of the project repairs a history")
    call.need(call.request.reason, "reason-missing", "a repair gives a written reason")
    return Step(call.state)
