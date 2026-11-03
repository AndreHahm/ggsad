"""The review report layout and the review gate: AE-011, AE-316, AE-322."""

from __future__ import annotations

import contextlib
from dataclasses import replace

import pytest
from engine_helpers import CLEAR, active, context, definition, do, req
from hypothesis import given
from hypothesis import strategies as st

from ggsad.core.review_report import (
    LayoutError,
    approval_issues,
    completion_gaps,
    parse_review,
)
from ggsad.core.state import Approval

H1 = "sha256:" + "1" * 64
HEAD = """# Review

Participant: {who}
Role: {role}
Reviewed revision: 5327a59
Action: review round
Timestamp: 2026-11-03T10:00:00Z
Result: findings reported
Findings: 2
Disposition: F-1 fix, F-2 defer
"""
TABLE = """
## Findings

| Finding | Severity | Decision | Reason | Status |
|---|---|---|---|---|
{rows}

Severities: informational, minor, major, blocking, critical.
"""


def report(rows: str = "| F-1 | blocking | fix | wrong guard | verified |",
           who: str = "agent:devin", role: str = "Reviewer") -> str:  # fmt: skip
    return HEAD.format(who=who, role=role) + TABLE.format(rows=rows)


def test_a_report_in_the_layout_is_read() -> None:
    parsed = parse_review(
        report("| F-1 | blocking | fix | r | verified |\n| F-2 | minor |  |  | open |")
    )
    assert parsed.record["Participant"] == "agent:devin"
    assert [(f.id, f.severity, f.decision, f.status) for f in parsed.findings] == [
        ("F-1", "blocking", "fix", "verified"),
        ("F-2", "minor", "", "open"),
    ]
    assert completion_gaps(report()) == () and approval_issues(report()) == []


def test_the_optional_reviewer_switch_line_is_allowed() -> None:
    text = report().replace(
        "Disposition: F-1 fix, F-2 defer", "Disposition: x\nReviewer switch: none"
    )
    assert parse_review(text).record["Reviewer switch"] == "none"


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "# Not a review\n",
        report().replace("# Review", "Review"),
        report().replace("Timestamp: 2026-11-03T10:00:00Z\n", ""),
        report().replace("Role: Reviewer", "Role: Reviewer\nRole: Reviewer"),
        report().replace("Action: review round", "Colour: red"),
        report().replace("## Findings", "## Results"),
        report().replace("| Finding | Severity", "| Id | Severity"),
        report().replace("|---|---|---|---|---|", "| a | b |"),
        report("| F-1 | huge | fix | r | verified |"),
        report("| F-1 | blocking | maybe | r | verified |"),
        report("| F-1 | blocking | fix | r | done |"),
        report("| F-1 | blocking | fix | r |"),
        report("| F-1 | blocking | fix | r | verified |\n| F-1 | minor | fix | r | open |"),
        report("|  | blocking | fix | r | verified |"),
    ],
)
def test_text_that_does_not_follow_the_layout_is_not_a_review_report(bad: str) -> None:
    with pytest.raises(LayoutError):
        parse_review(bad)
    assert approval_issues(bad)[0][0] == "review-layout-invalid"
    assert completion_gaps(bad)


def test_ae322_a_review_by_a_human_is_not_a_review_report() -> None:
    issues = approval_issues(report(who="human:ada"))
    assert issues[0][0] == "reviewer-not-agent"
    assert completion_gaps(report(who="human:ada"))
    assert approval_issues(report(role="Requestor"))[0][0] == "review-layout-invalid"


def test_ae316_a_blocking_finding_without_a_decision_is_named() -> None:
    text = report(
        "| F-1 | blocking | | | open |\n| F-2 | critical | | | open |\n| F-3 | minor | | | open |"
    )
    code, message = approval_issues(text)[0]
    assert code == "review-undecided" and "F-1, F-2" in message and "F-3" not in message


def test_ae011_a_fix_finding_must_be_verified_or_dispositioned() -> None:
    assert completion_gaps(report("| F-1 | blocking | fix | r | open |"))[0].startswith(
        "findings marked fix"
    )
    for status in ("verified", "accepted", "deferred"):
        assert completion_gaps(report(f"| F-1 | blocking | fix | r | {status} |")) == ()
    assert completion_gaps(report("| F-1 | minor | defer | r | open |")) == ()


def test_a_missing_file_is_reported() -> None:
    assert approval_issues(None) == [("review-missing", "review.md does not exist")]
    assert completion_gaps(None) == ("review.md does not exist",)


@given(st.text(max_size=300))
def test_parse_review_only_raises_layout_error(text: str) -> None:
    with contextlib.suppress(LayoutError):
        parse_review(text)
    assert isinstance(completion_gaps(text), tuple)


def test_ae322_the_engine_declines_the_approval_of_a_review_by_a_human() -> None:
    bad = report(who="human:ada")
    facts = replace(CLEAR, target_issues={"approve:review": tuple(approval_issues(bad))})
    result = do(active(), req("approve", target="review", content_hash=H1), facts=facts)
    assert result.codes == ("reviewer-not-agent",) and not result.changed
    good = replace(CLEAR, target_issues={"approve:review": tuple(approval_issues(report()))})
    approved = do(active(), req("approve", target="review", content_hash=H1), facts=good)
    assert approved.state.approvals[-1].target == "review"
    assert approved.state.approvals[-1].content_hash == H1


def test_the_review_gate_is_satisfied_end_to_end_from_the_parsed_report() -> None:
    gates = definition(done=[{"id": "code-review", "kind": "review"}])
    text = report()
    facts = replace(CLEAR, review_gaps={"code-review": completion_gaps(text)}, review_hash=H1)
    approval = Approval("review", "human:ada", "A0", "A0", content_hash=H1)
    result = do(active(approvals=(approval,)), req("close"), context(gates), facts)
    assert result.state.outcome == "done"
    open_fix = replace(
        facts,
        review_gaps={"code-review": completion_gaps(report("| F-1 | blocking | fix | r | open |"))},
    )
    assert (
        do(active(approvals=(approval,)), req("close"), context(gates), open_fix).result
        == "blocked"
    )
