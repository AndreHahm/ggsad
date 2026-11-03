"""The status report and the read-only actions (AE-071 to AE-073, AE-318, Section 23.8)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from project_helpers import ADA, FULL, git, make_change, req, settle, write

from ggsad.core.operations import Envelope, run_action
from ggsad.core.reports import run_read_only
from ggsad.core.status import ALL_FINE, NEEDS_YOU, WAITING, Pending, headline

NOW = "2026-11-03T12:00:00Z"
HEAD = """# Review

Participant: agent:devin
Role: Reviewer
Reviewed revision: 5327a59
Action: review round
Timestamp: 2026-11-03T10:00:00Z
Result: findings reported
Findings: 1
Disposition: F-1 fix

## Findings

| Finding | Severity | Decision | Reason | Status |
|---|---|---|---|---|
| F-1 | minor | fix | wrong guard | verified |
"""


def active_change(root: Path) -> None:
    make_change(root)
    settle(root)
    assert run_action(root, "c-1", req("approve", ADA, target="all")).result == "success"
    assert run_action(root, "c-1", req("start")).result == "success"


def read(root: Path, action: str) -> Envelope:
    return run_read_only(root, "c-1", action, NOW)


def report(done: Envelope) -> dict[str, Any]:
    return cast("dict[str, Any]", done.data["report"])


def warning_codes(done: Envelope) -> list[str]:
    return [w["code"] for w in report(done)["warnings"]]


def test_the_report_starts_with_one_line_and_writes_nothing(root: Path) -> None:
    active_change(root)
    run_action(root, "c-1", req("ask", text="Which mail text?"))
    run_action(root, "c-1", req("wait", question="Q1", expires="2026-11-01T00:00:00Z"))
    before = (root / "specs/c-1/state.json").read_bytes()
    done = read(root, "check")
    assert done.result == "success" and not done.changed
    shown = report(done)
    assert shown["headline"] == NEEDS_YOU
    assert shown["pending"][0]["actor"] == "human:ada"
    assert "wait-overdue" in warning_codes(done)
    assert (root / "specs/c-1/state.json").read_bytes() == before


def test_a_new_change_needs_the_approver(root: Path) -> None:
    make_change(root)
    shown = report(read(root, "check"))
    assert shown["headline"] == NEEDS_YOU
    assert [p["id"] for p in shown["pending"]] == ["gates"]


def test_an_active_change_with_nothing_due_is_all_fine(root: Path) -> None:
    active_change(root)
    shown = report(read(root, "check"))
    assert shown["headline"] == ALL_FINE and shown["state"] == "active"
    assert shown["gates_enforced"] is True


def test_the_headline_rule() -> None:
    human = Pending("question", "Q1", "human:ada", "x")
    agent = Pending("wait", "external", "agent:builder", "x")
    assert headline([]) == ALL_FINE
    assert headline([agent]) == WAITING
    assert headline([agent, human]) == NEEDS_YOU


def test_the_warnings_name_fallbacks_and_the_missing_deputy(root: Path) -> None:
    active_change(root)
    codes = warning_codes(read(root, "check"))
    assert "fallback-role" in codes and "no-deputy" in codes
    assert "no-approved-list" not in codes and "no-anchor" not in codes


def test_a_missing_anchor_is_a_warning(root: Path) -> None:
    active_change(root)
    git(root, "update-ref", "-d", "refs/ggsad/anchors/c-1")
    assert "no-anchor" in warning_codes(read(root, "check"))


def test_edited_gates_are_rejected_and_the_report_says_they_are_not_enforced(root: Path) -> None:
    active_change(root)
    write(root, "specs/c-1/change.yaml", FULL.replace("lib/**", "src/**"))
    done = read(root, "check")
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["gates-changed"]
    assert report(done)["gates_enforced"] is False


def test_a_change_without_a_history_is_not_reportable(root: Path) -> None:
    write(root, "specs/c-1/change.yaml", FULL)
    done = read(root, "check")
    assert done.result == "rejected" and [i.code for i in done.issues] == ["change-missing"]


def test_ae071_a_guard_on_a_sound_change_succeeds(root: Path) -> None:
    active_change(root)
    done = read(root, "guard")
    assert done.result == "success" and not done.changed, done.issues


def test_ae072_a_guard_rejects_edited_gates(root: Path) -> None:
    active_change(root)
    write(root, "specs/c-1/change.yaml", FULL.replace("lib/**", "src/**"))
    done = read(root, "guard")
    assert done.result == "rejected" and "gates-changed" in [i.code for i in done.issues]


def test_a_guard_rejects_a_spec_edited_after_its_approval(root: Path) -> None:
    active_change(root)
    write(root, "specs/c-1/spec.md", "# changed\nConflicts with higher documents: none\n")
    assert "approval-stale" in [i.code for i in read(root, "guard").issues]


def test_a_guard_rejects_an_edited_higher_document(root: Path) -> None:
    active_change(root)
    write(root, "docs/constitution.md", "new rules\n")
    assert "approval-stale" in [i.code for i in read(root, "guard").issues]


def test_a_guard_reports_a_scope_violation(root: Path) -> None:
    active_change(root)
    write(root, "docs/other.md", "outside\n")
    assert "scope-violation" in [i.code for i in read(root, "guard").issues]


def test_a_guard_reports_a_rewritten_history_as_inconsistent(root: Path) -> None:
    active_change(root)
    path = root / "specs/c-1/state.json"
    path.write_text(path.read_text().replace("agent:builder", "agent:other"), encoding="utf-8")
    done = read(root, "guard")
    assert done.result == "rejected" and [i.code for i in done.issues] == ["history-inconsistent"]


def test_a_guard_without_a_state_document_is_not_enforced(root: Path) -> None:
    write(root, "specs/c-1/change.yaml", FULL)
    done = read(root, "guard")
    assert done.result == "rejected" and "not enforced" in done.issues[0].message


def test_check_scope_holds_then_is_violated(root: Path) -> None:
    make_change(root)
    assert read(root, "check-scope").data["scope"] == "not started"
    settle(root)
    run_action(root, "c-1", req("approve", ADA, target="all"))
    run_action(root, "c-1", req("start"))
    assert read(root, "check-scope").data["scope"] == "holds"
    write(root, "docs/other.md", "outside\n")
    done = read(root, "check-scope")
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["scope-violation"]


def test_review_needs_a_complete_report(root: Path) -> None:
    make_change(root)
    missing = read(root, "review")
    assert missing.result == "rejected" and missing.data["review_exists"] is False
    write(root, "specs/c-1/review.md", HEAD)
    assert read(root, "review").result == "success"
    write(root, "specs/c-1/review.md", HEAD.replace("| verified |", "| open |"))
    assert [i.code for i in read(root, "review").issues] == ["review-incomplete"]


def test_a_missing_project_is_an_error(tmp_path: Path) -> None:
    done = run_read_only(tmp_path, "c-1", "check", NOW)
    assert done.result == "error" and done.exit_code == 2


def test_an_unreadable_review_is_an_error_not_a_traceback(root: Path) -> None:
    make_change(root)
    (root / "specs/c-1/review.md").write_bytes(b"\xff\xfe\x00bad")
    done = read(root, "review")
    assert done.result == "error" and done.exit_code == 2
    assert [i.code for i in done.issues] == ["review-unreadable"]


def test_a_review_approval_is_bound_to_the_hash_of_review_md(root: Path) -> None:
    active_change(root)
    write(root, "specs/c-1/review.md", HEAD)
    done = run_action(root, "c-1", req("approve", ADA, target="review"))
    assert done.result == "success", done.issues
    assert run_read_only(root, "c-1", "guard", NOW).result == "success"
    write(root, "specs/c-1/review.md", HEAD + "\nNote after the table.\n")
    assert "approval-stale" in [i.code for i in read(root, "guard").issues]


def test_approve_all_applies_the_checks_of_the_spec_and_of_the_gates(root: Path) -> None:
    make_change(root)
    settle(root)
    write(root, "specs/c-1/spec.md", "# Spec without the conflict line\n")
    done = run_action(root, "c-1", req("approve", ADA, target="all"))
    assert done.result == "rejected" and [i.code for i in done.issues] == ["conflict-line-missing"]
    write(root, "specs/c-1/spec.md", "Conflicts with higher documents: none\n")
    write(
        root,
        "specs/c-1/change.yaml",
        FULL.replace('scope:\n  allow: ["lib/**"]\n', 'scope:\n  allow: ["/bad"]\n'),
    )
    again = run_action(root, "c-1", req("approve", ADA, target="all"))
    assert again.result == "rejected" and "scope-pattern-invalid" in [i.code for i in again.issues]
