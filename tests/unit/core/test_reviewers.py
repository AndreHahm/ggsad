"""A Reviewer from the vendor of the Requestor is declined (Section 14.2, AE-322)."""

from __future__ import annotations

from typing import Any

import pytest
from test_review_report import report

from ggsad.core.reviewers import vendor_issues
from ggsad.core.settings import Requestor, Reviewer

REQUESTORS = (Requestor("agent:builder", "Anthropic", "m1"),)
REVIEWERS = (
    Reviewer("agent:devin", "Cognition", "m2"),
    Reviewer("agent:twin", " anthropic ", "m3"),
    Reviewer("agent:backup", "Google", "m4", fallback=True),
)


def started(actor: str = "agent:builder", action: str = "new") -> dict[str, Any]:
    return {"action": action, "actor": actor}


def codes(who: str, bodies: tuple[dict[str, Any], ...] = (started(),)) -> list[str]:
    return [c for c, _ in vendor_issues(report(who=who), REQUESTORS, REVIEWERS, bodies)]


def test_ae322_a_reviewer_of_another_vendor_is_accepted() -> None:
    assert codes("agent:devin") == []
    assert codes("agent:backup") == []


def test_ae322_a_reviewer_of_the_vendor_of_the_requestor_is_declined() -> None:
    assert codes("agent:twin") == ["reviewer-same-vendor"]


def test_the_requestor_is_the_agent_that_started_the_change() -> None:
    other = (started("agent:other"), started())
    assert codes("agent:twin", other) == []


def test_the_first_new_or_start_entry_counts_and_humans_are_skipped() -> None:
    bodies = (started("human:ada", "approve"), started("agent:builder", "start"))
    assert codes("agent:twin", bodies) == ["reviewer-same-vendor"]


@pytest.mark.parametrize(
    "bodies",
    [(), (started("human:ada", "new"),), (started("agent:unlisted"),), (started(action="close"),)],
)
def test_without_a_known_requestor_nothing_is_declined(bodies: tuple[dict[str, Any], ...]) -> None:
    assert codes("agent:twin", bodies) == []


def test_an_unlisted_reviewer_or_a_missing_vendor_is_not_declined() -> None:
    assert codes("agent:stranger") == []
    nameless = (Reviewer("agent:twin"),)
    assert vendor_issues(report(who="agent:twin"), REQUESTORS, nameless, (started(),)) == []


def test_a_text_that_is_not_a_report_or_is_missing_has_no_vendor_issue() -> None:
    assert vendor_issues(None, REQUESTORS, REVIEWERS, (started(),)) == []
    assert vendor_issues("nothing", REQUESTORS, REVIEWERS, (started(),)) == []


def test_a_reviewer_with_the_identity_of_the_requestor_is_declined_whatever_the_vendors() -> None:
    same = (Requestor("agent:solo", "A"),)
    listed = (Reviewer("agent:solo", "B"),)
    found = vendor_issues(report(who="agent:solo"), same, listed, (started("agent:solo"),))
    assert [c for c, _ in found] == ["reviewer-is-requestor"]
    bare = vendor_issues(report(who="agent:solo"), (), (), (started("agent:solo"),))
    assert [c for c, _ in bare] == ["reviewer-is-requestor"]
