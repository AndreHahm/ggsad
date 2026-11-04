"""The vendor rule for the Reviewer (Section 14.2): the same vendor as the Requestor is declined.

The Requestor of a change is the agent that started it: the actor of the first `new` or `start`
entry that is not a human. Its vendor, and the vendor of the Reviewer named in `review.md`, come
from the settings. When either is not known, nothing is declined, because nothing can be compared.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ggsad.core.review_report import LayoutError, parse_review

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from ggsad.core.settings import Requestor, Reviewer

STARTING_ACTIONS: Final = ("new", "start")
HUMAN_PREFIX: Final = "human:"


def _requestor_identity(bodies: Sequence[Mapping[str, object]]) -> str | None:
    for body in bodies:
        actor = body.get("actor")
        starts = body.get("action") in STARTING_ACTIONS
        if starts and isinstance(actor, str) and not actor.startswith(HUMAN_PREFIX):
            return actor
    return None


def _vendor(identity: str | None, listed: Sequence[Requestor | Reviewer]) -> str | None:
    for entry in listed:
        if entry.identity == identity and entry.vendor is not None:
            return entry.vendor.strip().casefold()
    return None


def vendor_issues(
    text: str | None,
    requestors: Sequence[Requestor],
    reviewers: Sequence[Reviewer],
    bodies: Sequence[Mapping[str, object]],
) -> list[tuple[str, str]]:
    """`reviewer-same-vendor` when the Reviewer of the report has the vendor of the Requestor."""
    if text is None:
        return []
    try:
        reviewer = parse_review(text).record["Participant"]
    except LayoutError:
        return []
    requestor = _requestor_identity(bodies)
    vendor = _vendor(reviewer, reviewers)
    if vendor is None or vendor != _vendor(requestor, requestors):
        return []
    message = f"the Reviewer {reviewer} has the same vendor as the Requestor {requestor}"
    return [("reviewer-same-vendor", message)]
