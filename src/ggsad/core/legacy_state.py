"""Read the old YAML state document (schema 0.1) as a state of this method (Section 25.3, AE-103).

Only what maps clearly is taken over. A status without a clear match is refused by name, so that a
person decides and nothing is guessed. The old history events cannot become entries (the new chain
starts at the `migrate` entry), so they are kept as one text, which becomes the note of that entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from ggsad.core.canonical import DomainError
from ggsad.core.content_hash import yaml_value
from ggsad.core.issues import Issue
from ggsad.core.state import State
from ggsad.core.values import as_list, as_mapping, as_text

if TYPE_CHECKING:
    from collections.abc import Mapping

LEGACY_FILE: Final = "state.yaml"
LEGACY_VERSION: Final = "0.1"
OPEN_STATUSES: Final = ("draft", "ready")
OUTCOME_OF_STATUS: Final = {"done": "done", "cancelled": "cancelled", "failed": "failed"}


class LegacyStateError(ValueError):
    """The old state document cannot be taken over; `issue` says why."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.issue = Issue(code, message)


@dataclass(frozen=True)
class Converted:
    """The state taken over from an old document, and the text of its old history."""

    state: State
    note: str


def convert(text: str) -> Converted:
    """The state and the history note of an old document, or raise LegacyStateError."""
    document = _document(text)
    status = _status(document)
    return Converted(_state(status, document), _history_note(document))


def _error(code: str, message: str) -> LegacyStateError:
    return LegacyStateError(code, message)


def _invalid(what: str, detail: str) -> LegacyStateError:
    return _error(
        "legacy-state-invalid", f"{LEGACY_FILE} {what}" + (f": {detail}" if detail else "")
    )


def _unreadable(error: Exception) -> LegacyStateError:
    return _invalid("cannot be read", str(error))


def _not_a_mapping() -> LegacyStateError:
    return _invalid("must hold a mapping", "")


def _no_status() -> LegacyStateError:
    return _invalid("needs flow.status as a text", "")


def _wrong_version(version: object) -> LegacyStateError:
    text = f"{LEGACY_FILE} has schema_version {version!r}; only {LEGACY_VERSION!r} is converted"
    return _error("schema-version-unsupported", text)


def _unmapped(status: str) -> LegacyStateError:
    text = (
        f"the status {status!r} has no clear match; finish or cancel the change first, "
        "or write its state by hand"
    )
    return _error("legacy-status-unmapped", text)


def _no_reason() -> LegacyStateError:
    text = "the change failed, but failure.reason is empty; the new state needs a reason"
    return _error("legacy-failure-reason-missing", text)


def _document(text: str) -> Mapping[str, object]:
    try:
        value = yaml_value(text)
    except DomainError as error:
        raise _unreadable(error) from error
    document = as_mapping(value)
    if document is None:
        raise _not_a_mapping()
    version = document.get("schema_version")
    if version != LEGACY_VERSION:
        raise _wrong_version(version)
    return document


def _status(document: Mapping[str, object]) -> str:
    flow = as_mapping(document.get("flow"))
    status = as_text(flow.get("status")) if flow is not None else None
    if status is None:
        raise _no_status()
    return status


def _state(status: str, document: Mapping[str, object]) -> State:
    if status in OPEN_STATUSES:
        return State()
    outcome = OUTCOME_OF_STATUS.get(status)
    if outcome is None:
        raise _unmapped(status)
    reason = _failure_reason(document) if outcome == "failed" else None
    return State(state="closed", outcome=outcome, reason=reason)


def _failure_reason(document: Mapping[str, object]) -> str:
    failure = as_mapping(document.get("failure"))
    reason = as_text(failure.get("reason")) if failure is not None else None
    if reason is None:
        raise _no_reason()
    return reason


def _history_note(document: Mapping[str, object]) -> str:
    events = as_list(document.get("history")) or []
    lines = [_event_line(event) for event in events]
    return f"converted from {LEGACY_FILE}; old history: " + (
        "; ".join(line for line in lines if line) or "none"
    )


def _event_line(event: object) -> str:
    item = as_mapping(event)
    if item is None:
        return ""
    parts = [as_text(item.get(name)) for name in ("timestamp", "event", "actor", "reason")]
    return " ".join(part for part in parts if part)
