"""The read-only actions `check`, `review`, `guard`, and `check-scope` (Sections 22.4 and 23.8).

They never write, never record a failure, and start no program. Each answers with the same
envelope as the other operations, with `changed` false.

Interpretations fixed here (listed in the pull request):
- `check` answers `rejected` with `gates-changed` while the gate definitions differ from the
  approved ones, and still carries the report with `gates_enforced` false;
- `review` answers `success` when the report of `review.md` could be approved and is complete, and
  otherwise `rejected` with the codes of what is missing;
- `guard` reports a scope that cannot be measured as `scope-violation` with that message, because
  it cannot confirm that the scope holds;
- `check-scope` answers `success` with `data.scope` set to `not_evaluable` where the scope cannot
  be measured, and `success` with `data.scope` set to `not started` before the start.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ggsad.core.errors import StateError
from ggsad.core.gate_eval import LEVEL_ORDER, NOT_EVALUABLE, SATISFIED
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.guards import approved_hash, recorded_documents
from ggsad.core.issues import Issue
from ggsad.core.loader import LoadedChange, load_change
from ggsad.core.operations import Envelope, error_issue, failure, make_runner, open_project
from ggsad.core.review_report import approval_issues, completion_gaps
from ggsad.core.status import build_status, latest_results

if TYPE_CHECKING:
    from pathlib import Path

    from ggsad.core.anchor import AnchorStore
    from ggsad.core.gate_model import Facts
    from ggsad.core.settings import Settings
    from ggsad.core.state import Approval, State

READ_ONLY: Final = ("check", "review", "guard", "check-scope")
HISTORY_CODES: Final = frozenset({"anchor-missing"})


def run_read_only(
    root: Path, change_id: str, action: str, now: str, anchors: AnchorStore | None = None
) -> Envelope:
    """Run one read-only action against the change on disk."""
    settings, issues = open_project(root)
    if settings is None:
        return failure(action, issues)
    loaded = load_change(root, settings, change_id, anchors or GitAnchorStore(root), action)
    refusal = _refusal(action, loaded)
    if refusal is not None:
        return refusal
    if action == "guard":
        return _guard(loaded)
    if action == "check-scope":
        return _check_scope(loaded)
    if action == "review":
        return _review(root, loaded)
    return _check(root, settings, loaded, now)


def _refusal(action: str, loaded: LoadedChange) -> Envelope | None:
    """The envelope when the change cannot be read at all. `guard` judges a bad history itself."""
    if loaded.problems:
        return failure(action, loaded.problems)
    if action == "guard":
        return None
    if loaded.history_error is not None:
        return failure(action, (error_issue(loaded.history_error),))
    if loaded.state is None:
        return failure(action, (Issue("change-missing", "the change has no history yet"),))
    return None


# ------------------------------------------------------------------- check


def _check(root: Path, settings: Settings, loaded: LoadedChange, now: str) -> Envelope:
    runner = make_runner(root, settings, loaded)
    report = build_status(root, settings, loaded, runner, now)
    state = loaded.state.to_json() if loaded.state is not None else None
    data = {"report": report.to_json()}
    if not report.gates_enforced:
        text = "the gate definitions differ from the approved ones; the gates are not enforced"
        return Envelope("check", "rejected", False, state, (Issue("gates-changed", text),), data)
    return Envelope("check", "success", False, state, data=data)


# ------------------------------------------------------------------ review


def _read_review(path: Path) -> tuple[str | None, Issue | None]:
    try:
        return (path.read_text(encoding="utf-8") if path.is_file() else None), None
    except (OSError, UnicodeDecodeError) as error:
        return None, Issue("review-unreadable", f"review.md cannot be read: {error}")


def _review(root: Path, loaded: LoadedChange) -> Envelope:
    path = root / loaded.change_dir / "review.md"
    text, unreadable = _read_review(path)
    if unreadable is not None:
        return Envelope("review", "error", False, issues=(unreadable,))
    problems = approval_issues(text) or [("review-incomplete", g) for g in completion_gaps(text)]
    state = loaded.state.to_json() if loaded.state is not None else None
    data = {"review_exists": text is not None, "gaps": [message for _, message in problems]}
    if problems:
        issues = tuple(Issue(code, message) for code, message in problems)
        return Envelope("review", "rejected", False, state, issues, data)
    return Envelope("review", "success", False, state, data=data)


# ------------------------------------------------------------- check-scope


def _check_scope(loaded: LoadedChange) -> Envelope:
    scope = loaded.facts.scope
    state = loaded.state.to_json() if loaded.state is not None else None
    if scope is None:
        return Envelope("check-scope", "success", False, state, data={"scope": "not started"})
    if scope.result == NOT_EVALUABLE:
        data = {"scope": NOT_EVALUABLE, "detail": scope.detail}
        return Envelope("check-scope", "success", False, state, data=data)
    if scope.result == SATISFIED:
        issue = Issue("scope-violation", scope.detail)
        return Envelope("check-scope", "rejected", False, state, (issue,), {"scope": "violated"})
    return Envelope("check-scope", "success", False, state, data={"scope": "holds"})


# ------------------------------------------------------------------- guard


def _history_issue(error: StateError) -> Issue:
    code = error.code
    if code in HISTORY_CODES:
        return Issue(code, error.message)
    if code in ("state-read-failed", "lock-unavailable", "anchor-invalid"):
        return error_issue(error)
    return Issue("history-inconsistent", error.message)


def _level_issues(state: State) -> list[Issue]:
    return [
        _stale(f"the {a.target} approval is below its required level")
        for a in state.approvals
        if LEVEL_ORDER.get(a.assurance, 0) < LEVEL_ORDER.get(a.required_level, 0)
    ]


def _latest(state: State, target: str) -> Approval | None:
    found = [a for a in state.approvals if a.target == target]
    return found[-1] if found else None


def _content_issues(state: State, facts: Facts) -> list[Issue]:
    found: list[Issue] = []
    spec, review = _latest(state, "spec"), _latest(state, "review")
    if spec and facts.spec_hash is not None and spec.content_hash != facts.spec_hash:
        found.append(_stale("spec.md changed after its approval"))
    if review and review.content_hash != facts.review_hash:
        found.append(_stale("review.md changed after the approval of the review result"))
    recorded = recorded_documents(state)
    if recorded is not None and recorded != dict(facts.documents):
        found.append(_stale("the higher-ranking documents changed after their approval"))
    return found


def _approval_issues(loaded: LoadedChange) -> list[Issue]:
    if loaded.state is None:
        return []
    return _level_issues(loaded.state) + _content_issues(loaded.state, loaded.facts)


def _stale(message: str) -> Issue:
    return Issue("approval-stale", message)


def _hard_failures(loaded: LoadedChange) -> list[Issue]:
    state = loaded.state
    if state is None or state.closed:
        return []
    results = latest_results(loaded.bodies)
    return [
        Issue("hard-failure-active", f"the hard fail gate {g.id!r} is active")
        for g in loaded.context.gates
        if g.group == "fail" and g.severity == "hard" and results.get(g.id) == SATISFIED
    ]


def _scope_issues(loaded: LoadedChange) -> list[Issue]:
    scope = loaded.facts.scope
    if scope is None or scope.result not in (SATISFIED, NOT_EVALUABLE):
        return []
    text = (
        scope.detail
        if scope.result == SATISFIED
        else f"the scope cannot be measured: {scope.detail}"
    )
    return [Issue("scope-violation", text)]


def _guard(loaded: LoadedChange) -> Envelope:
    if loaded.history_error is not None:
        return failure("guard", (_history_issue(loaded.history_error),))
    state = loaded.state
    if state is None:
        text = "the change has no state document; the verifications are not enforced"
        return Envelope("guard", "rejected", False, issues=(Issue("history-inconsistent", text),))
    found: list[Issue] = []
    approved = approved_hash(state)
    if approved is not None and approved != loaded.facts.definitions_hash:
        found.append(Issue("gates-changed", "the gate definitions differ from the approved ones"))
    found += _approval_issues(loaded)
    found += _scope_issues(loaded)
    found += _hard_failures(loaded)
    if found:
        return Envelope("guard", "rejected", False, state.to_json(), tuple(found))
    return Envelope("guard", "success", False, state.to_json())
