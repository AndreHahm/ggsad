"""Warnings and pending items of the status report that need a hand-built change."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path

from project_helpers import ADA, make_change, req, settle, write

from ggsad.core.gate_model import BaselineEntry, CommandSpec, ExitMap, Gate
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.issues import Issue
from ggsad.core.loader import LoadedChange, load_change
from ggsad.core.operations import make_runner, run_action
from ggsad.core.project import load_settings
from ggsad.core.settings import Settings
from ggsad.core.state import Approval, Question, State, Wait
from ggsad.core.status import (
    _approval_warnings,
    _baseline_warnings,
    _history_warnings,
    _is_before,
    build_status,
    collect_warnings,
    pending_items,
)

NOW = "2026-11-03T12:00:00Z"


def loaded_change(root: Path) -> tuple[Settings, LoadedChange]:
    make_change(root)
    settle(root)
    run_action(root, "c-1", req("approve", ADA, target="all"))
    settings, _ = load_settings(root)
    assert settings is not None
    return settings, load_change(root, settings, "c-1", GitAnchorStore(root))


def with_state(loaded: LoadedChange, state: State, **context: object) -> LoadedChange:
    return replace(loaded, state=state, context=replace(loaded.context, **context))


def codes(warnings: Sequence[Issue]) -> list[str]:
    return [w.code for w in warnings]


def test_a_moment_that_is_not_a_time_is_never_overdue() -> None:
    assert _is_before("2026-11-01T00:00:00Z", NOW) is True
    assert _is_before("soon", NOW) is False
    assert _is_before(None, NOW) is False
    assert _is_before("2026-11-01", NOW) is True


def test_a_baseline_entry_past_its_review_date_is_reported() -> None:
    gate = Gate("t", "done", "check", baseline=(BaselineEntry("F1", "r", "2026-10-01"),))
    fresh = Gate("u", "done", "check", baseline=(BaselineEntry("F2", "r", "2027-01-01"),))
    assert codes(_baseline_warnings([gate, fresh], NOW)) == ["baseline-review-overdue"]


def test_a_stale_sign_off_and_a_lapsing_override_are_reported(root: Path) -> None:
    _, loaded = loaded_change(root)
    old = "sha256:" + "0" * 64
    state = State(
        state="active",
        approvals=(
            Approval("gate", "human:ada", "A1", "A0", gate="legal", definitions_hash=old),
            Approval("override", "human:ada", "A1", "A0", gate="flaky", attempts=2, used=1,
                     definitions_hash=old),
            Approval("override", "human:ada", "A1", "A0", gate="spent", attempts=1, used=1,
                     definitions_hash=old),
        ),
    )  # fmt: skip
    found = codes(_approval_warnings(with_state(loaded, state)))
    assert found == ["sign-off-stale", "override-lapses"]


def test_a_human_close_without_an_agent_report_is_reported(root: Path) -> None:
    _, loaded = loaded_change(root)
    bodies = (*loaded.bodies, {"action": "close", "actor": "human:ada"})
    warnings = _history_warnings(replace(loaded, bodies=bodies))
    assert "no-agent-report" in codes(warnings)
    reported = {"action": "close", "actor": "human:ada", "agent_report": {}}
    quiet = _history_warnings(replace(loaded, bodies=(*loaded.bodies, reported)))
    assert "no-agent-report" not in codes(quiet)


def test_an_external_wait_whose_program_exists_is_ready_to_resume(root: Path) -> None:
    settings, loaded = loaded_change(root)
    gate = Gate("lint", "done", "check", command=CommandSpec(("@interpreter",), ExitMap()))
    wait = Wait("external", "cannot run", "human:ada", "gate lint can be evaluated")
    ctx = replace(loaded.context, gates=(gate,))
    changed = replace(loaded, state=State(state="waiting", wait=wait), context=ctx)
    runner = make_runner(root, settings, changed)
    assert "ready-to-resume" in codes(collect_warnings([], changed, settings, runner, NOW))


def test_an_answer_by_someone_who_may_not_resume_is_reported(root: Path) -> None:
    settings, loaded = loaded_change(root)
    question = Question("Q1", "Which?", "human:bo", "agent:builder", answer="A", answerer="agent:x")
    wait = Wait("question", "waiting", "human:bo", "Q1 answered", None, "Q1")
    state = State(state="waiting", questions=(question,), wait=wait)
    changed = with_state(loaded, state)
    runner = make_runner(root, settings, changed)
    assert "ready-to-resume" in codes(collect_warnings([], changed, settings, runner, NOW))
    allowed = replace(question, answerer="human:bo")
    again = with_state(loaded, replace(state, questions=(allowed,)))
    assert "ready-to-resume" not in codes(collect_warnings([], again, settings, runner, NOW))


def test_a_missing_document_and_the_interpreter_are_reported(root: Path) -> None:
    settings, loaded = loaded_change(root)
    runner = make_runner(root, settings, loaded)
    found = collect_warnings(["docs/roadmap.md"], loaded, settings, runner, NOW)
    assert "document-missing" in codes(found)


def test_a_missing_author_is_a_fallback(root: Path) -> None:
    settings, loaded = loaded_change(root)
    bare = replace(loaded, definition={"owner": "human:ada"})
    runner = make_runner(root, settings, bare)
    found = collect_warnings([], bare, settings, runner, NOW)
    assert codes(found).count("fallback-role") == 2


def test_pending_sign_offs_and_soft_failures_name_who_must_act(root: Path) -> None:
    _, loaded = loaded_change(root)
    gates = (
        Gate("legal", "done", "sign-off"),
        Gate("flaky", "fail", "command", "soft"),
    )
    state = State(state="active")
    changed = with_state(loaded, state, gates=gates)
    items = pending_items(changed, {"flaky": "satisfied"})
    assert [(p.kind, p.id) for p in items] == [("sign-off", "legal"), ("soft-failure", "flaky")]
    assert pending_items(replace(changed, state=None), {}) == ()


def test_a_closed_change_shows_its_reason_and_the_changes_that_follow(root: Path) -> None:
    settings, loaded = loaded_change(root)
    write(root, "specs/c-2/change.yaml", "follows: c-1\n")
    state = State(state="closed", outcome="cancelled", reason="not needed", replaced_by="c-3")
    closed = replace(loaded, state=state)
    shown = build_status(root, settings, closed, make_runner(root, settings, closed), NOW)
    assert shown.closed == {"reason": "not needed", "replaced_by": "c-3", "followed_by": ["c-2"]}
    assert shown.headline == "all fine"
