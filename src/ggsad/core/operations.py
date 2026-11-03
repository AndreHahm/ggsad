"""Running one state-changing operation end to end (Implementation Contract, Sections 22.2, 22.3).

`run_action` reads the project and the change, hands them to the engine, appends the entries the
engine decided on, and returns the result envelope. A refusal writes nothing. It never raises for
the content of a file, a history, or a failed write.

Interpretations fixed here (listed in the pull request):
- a project file that is missing or unreadable answers `error`; one that is present and unusable
  (schema version, shape) answers `rejected`;
- a history that cannot be trusted (inconsistent, truncated, rewritten, no anchor) answers
  `rejected` with the code of the finding; a history that cannot be read, a lock, a write, and a
  state conflict answer `error`;
- when the second entry of a chained action cannot be written after the first was, the answer is
  `error` with `changed` true, because the first entry is already part of the history.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Final

from ggsad.core.anchor import adopt_anchor
from ggsad.core.engine import apply
from ggsad.core.errors import StateError
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.issues import Issue
from ggsad.core.loader import LoadedChange, load_change
from ggsad.core.project import load_settings
from ggsad.core.runner import CommandRunner
from ggsad.core.settings import Settings
from ggsad.core.values import text_list

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from ggsad.core.anchor import AnchorStore
    from ggsad.core.engine_types import ActionResult, Request

ERROR_CODES: Final = frozenset(
    {
        "config-missing", "config-unreadable", "definition-unreadable", "state-read-failed",
        "state-write-failed", "lock-unavailable", "state-conflict", "anchor-write-failed",
        "anchor-lagging", "anchor-invalid", "agent-report-invalid",
    }
)  # fmt: skip
RESULTS: Final = ("success", "rejected", "blocked", "error")
EXIT_CODES: Final = {"success": 0, "rejected": 1, "blocked": 1, "error": 2}


@dataclass(frozen=True)
class Envelope:
    """The result envelope of every operation (Section 22.2)."""

    operation: str
    result: str
    changed: bool
    state: Mapping[str, object] | None = None
    issues: tuple[Issue, ...] = ()
    data: Mapping[str, object] = field(default_factory=dict)

    @property
    def exit_code(self) -> int:
        """0 for success, 1 for rejected or blocked, 2 for error."""
        return EXIT_CODES[self.result]

    def problems(self) -> list[str]:
        """Why the envelope is invalid, empty when it follows Section 22.2."""
        found: list[str] = []
        if self.result not in RESULTS:
            found.append(f"{self.result!r} is not a result")
        if self.result == "rejected" and self.changed:
            found.append("a rejected result cannot have changed true")
        if self.result == "blocked" and not self.changed:
            found.append("a blocked result must have changed true")
        if self.result != "success" and not self.issues:
            found.append("a result other than success needs an issue")
        return found

    def to_json(self) -> dict[str, object]:
        """The envelope as a JSON object; omitted fields follow Section 22.2."""
        out: dict[str, object] = {
            "operation": self.operation,
            "result": self.result,
            "changed": self.changed,
        }
        if self.state is not None:
            out["state"] = dict(self.state)
        if self.issues:
            out["issues"] = [
                {"code": i.code, "message": i.message, **({"path": i.path} if i.path else {})}
                for i in self.issues
            ]
        if self.data:
            out["data"] = dict(self.data)
        return out


def now_utc() -> str:
    """The time of an entry: the system clock in UTC, to the second."""
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def failure(operation: str, issues: tuple[Issue, ...]) -> Envelope:
    """The envelope of a refusal: `error` for a file that cannot be read, else `rejected`."""
    kind = "error" if any(i.code in ERROR_CODES for i in issues) else "rejected"
    return Envelope(operation, kind, False, issues=issues)


def error_issue(error: StateError) -> Issue:
    """The issue of a failed read, check, or write."""
    return Issue(error.code, error.message)


def open_project(root: Path) -> tuple[Settings | None, tuple[Issue, ...]]:
    """The settings of the project, or the issues that stop the operation."""
    return load_settings(root)


def make_runner(root: Path, settings: Settings, loaded: LoadedChange) -> CommandRunner:
    """The runner of the change: its `required_tools` and the interpreter of the settings."""
    tools = text_list(loaded.definition.get("required_tools")) if loaded.definition else None
    return CommandRunner(root, tools or (), settings.interpreter)


def _append(
    loaded: LoadedChange, bodies: tuple[dict[str, object], ...]
) -> tuple[Issue | None, int]:
    """Append the bodies in order. Returns the issue of the first write that failed and how many
    entries this call recorded. `anchor-lagging` means the entry was recorded."""
    recorded = 0
    for offset, body in enumerate(bodies):
        try:
            loaded.store.append(body, read_version=loaded.read_version + offset)
        except StateError as error:
            if error.code == "anchor-lagging":
                recorded += 1
            return error_issue(error), recorded
        recorded += 1
    return None, recorded


def run_action(
    root: Path, change_id: str, request: Request, anchors: AnchorStore | None = None
) -> Envelope:
    """Run one action of the transition table against the change on disk."""
    settings, issues = open_project(root)
    if settings is None:
        return failure(request.action, issues)
    store = anchors if anchors is not None else GitAnchorStore(root)
    loaded = load_change(root, settings, change_id, store, request.action)
    if loaded.problems:
        return failure(request.action, loaded.problems)
    if loaded.history_error is not None:
        return failure(request.action, (error_issue(loaded.history_error),))
    runner = make_runner(root, settings, loaded)
    done = apply(loaded.state, request, loaded.context, loaded.facts, runner)
    if not done.bodies:
        return Envelope(
            request.action, done.result, False, done.state.to_json(), done.issues, done.data
        )
    if request.action == "adopt":
        refusal = _anchor_first(loaded, store)
        if refusal is not None:
            return refusal
    return _record(loaded, done)


def _anchor_first(loaded: LoadedChange, anchors: AnchorStore) -> Envelope | None:
    """Create the anchor of the history as it is, before the entry of `adopt` is appended."""
    document = loaded.store.read()
    entries = document.entries if document is not None else ()
    try:
        adopt_anchor(anchors, loaded.change_id, entries)
    except StateError as error:
        return failure("adopt", (error_issue(error),))
    return None


def _record(loaded: LoadedChange, done: ActionResult) -> Envelope:
    issue, recorded = _append(loaded, tuple(done.bodies))
    if issue is not None:
        return Envelope(done.operation, "error", recorded > 0, issues=(issue,))
    return Envelope(done.operation, done.result, True, done.state.to_json(), done.issues, done.data)
