"""The history of a change: entries, the hash chain, and the anchor (Sections 24.4 and 25.1).

The history is an append-only list of entries. Every entry holds the hash of the entry before it
and its own hash, so an edit of an entry breaks the chain. A chain cannot show that entries were
cut off at the end, so an anchor outside the project records the latest position and hash.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Final

from ggsad.core.canonical import ZERO_HASH, DomainError, hash_value, is_hash_string
from ggsad.core.issues import Issue, Report
from ggsad.core.values import as_mapping, as_text

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

ACTIONS: Final = frozenset(
    {
        "new", "approve", "start", "wait", "ask", "answer", "resume", "close", "fail", "cancel",
        "supersede", "adopt", "conflict", "handover", "reassign", "repair", "migrate",
    }
)  # fmt: skip
BODY_FIELDS: Final = (
    "action", "actor", "account", "assurance", "at", "result", "gate_results", "gate_detail",
    "files", "note", "after",
)  # fmt: skip
# Fields that only some actions add (Section 25.1): (required, optional).
ACTION_FIELDS: Final[dict[str, tuple[frozenset[str], frozenset[str]]]] = {
    "close": (frozenset(), frozenset({"agent_report"})),
    "repair": (frozenset({"repaired"}), frozenset()),
    "migrate": (frozenset({"source_version", "target_version", "source_hash"}), frozenset()),
}
ASSURANCE_LEVELS: Final = frozenset({"A0", "A1", "A2"})
RESULTS: Final = frozenset({"success", "blocked"})
GATE_RESULT_VALUES: Final = frozenset(
    {"satisfied", "not_satisfied", "not_evaluable", "not_applicable"}
)
_INSTANT: Final = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


class EntryInvalidError(ValueError):
    """An entry body is not valid, so it must not be written."""

    def __init__(self, issues: Sequence[Issue]) -> None:
        super().__init__("; ".join(f"{issue.code}: {issue.message}" for issue in issues))
        self.issues = tuple(issues)


@dataclass(frozen=True)
class Entry:
    """One entry of the history: position, previous hash, body, and its own hash."""

    n: int
    prev: str
    body: Mapping[str, object]
    hash: str

    def to_json(self) -> dict[str, object]:
        """The entry as the object that the state document stores."""
        return {"n": self.n, "prev": self.prev, "body": dict(self.body), "hash": self.hash}


@dataclass(frozen=True)
class Anchor:
    """The position and hash of the latest entry, kept outside the project (Section 24.4)."""

    position: int
    hash: str


def entry_hash(prev: str, body: Mapping[str, object]) -> str:
    """The hash of an entry: the hash string of the object that holds `prev` and `body`."""
    return hash_value({"prev": prev, "body": dict(body)})


def make_entry(n: int, prev: str, body: Mapping[str, object]) -> Entry:
    """Build an entry, or raise EntryInvalidError or DomainError. Nothing is written."""
    issues = validate_body(body)
    if issues:
        raise EntryInvalidError(issues)
    return Entry(n, prev, dict(body), entry_hash(prev, body))


# ------------------------------------------------------------------ body validation


def validate_body(body: Mapping[str, object]) -> list[Issue]:
    """Check an entry body against Section 25.1: exactly its fields, with valid values."""
    action = body.get("action")
    issues: list[Issue] = []
    if not isinstance(action, str) or action not in ACTIONS:
        issues.append(Issue("entry-action-unknown", f"{action!r} is not an action name", "action"))
    fields = ACTION_FIELDS.get(action) if isinstance(action, str) else None
    required, optional = fields if fields else (frozenset(), frozenset())
    issues += _check_field_set(body, required, optional)
    issues += _check_values(body)
    return issues


def _check_field_set(
    body: Mapping[str, object], required: frozenset[str], optional: frozenset[str]
) -> list[Issue]:
    issues = [
        Issue("entry-field-missing", f"the body needs the field {name!r}", name)
        for name in (*BODY_FIELDS, *sorted(required))
        if name not in body
    ]
    allowed = {*BODY_FIELDS, *required, *optional}
    issues += [
        Issue("entry-field-unknown", f"the body has no field {name!r}", name)
        for name in sorted(set(body) - allowed)
    ]
    return issues


def _check_values(body: Mapping[str, object]) -> list[Issue]:
    checks: list[tuple[str, bool, str]] = [
        ("actor", as_text(body.get("actor")) is not None, "a non-empty identity"),
        ("account", _none_or_text(body.get("account")), "null or a non-empty account"),
        ("assurance", _in(body.get("assurance"), ASSURANCE_LEVELS), "A0, A1, or A2"),
        ("at", _is_instant(body.get("at")), "an instant written YYYY-MM-DDThh:mm:ssZ"),
        ("result", _in(body.get("result"), RESULTS), "'success' or 'blocked'"),
        ("note", _none_or_text(body.get("note")), "null or a text"),
        ("after", isinstance(body.get("after"), dict), "an object"),
    ]
    issues = [
        Issue("entry-field-invalid", f"{name} must be {expected}", name)
        for name, valid, expected in checks
        if name in body and not valid
    ]
    return issues + _check_gate_fields(body) + _check_files(body)


def _in(value: object, allowed: frozenset[str]) -> bool:
    return isinstance(value, str) and value in allowed


def _none_or_text(value: object) -> bool:
    return value is None or as_text(value) is not None


def _is_instant(value: object) -> bool:
    if not isinstance(value, str) or _INSTANT.fullmatch(value) is None:
        return False
    try:
        datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def _check_gate_fields(body: Mapping[str, object]) -> list[Issue]:
    results = body.get("gate_results")
    issues: list[Issue] = []
    if results is not None and not _results_ok(results):
        issues.append(
            Issue(
                "entry-field-invalid",
                "gate_results maps gate ids to satisfied, not_satisfied, not_evaluable, "
                "or not_applicable, written in exact lowercase",
                "gate_results",
            )
        )
    detail = body.get("gate_detail")
    if detail is not None and not _detail_ok(detail, results):
        issues.append(
            Issue(
                "entry-field-invalid",
                "gate_detail maps gates that have a result to texts",
                "gate_detail",
            )
        )
    return issues


def _results_ok(results: object) -> bool:
    mapping = as_mapping(results)
    return mapping is not None and all(_in(v, GATE_RESULT_VALUES) for v in mapping.values())


def _detail_ok(detail: object, results: object) -> bool:
    detail_map = as_mapping(detail)
    result_map = as_mapping(results)
    if detail_map is None or result_map is None:
        return False
    return all(key in result_map and isinstance(text, str) for key, text in detail_map.items())


def _check_files(body: Mapping[str, object]) -> list[Issue]:
    files = body.get("files")
    if "files" not in body or files is None:
        return []
    mapping = as_mapping(files)
    if mapping is None or not all(is_hash_string(value) for value in mapping.values()):
        return [Issue("entry-field-invalid", "files maps paths to content hashes", "files")]
    return []


# ------------------------------------------------------------------ chain and anchor


def verify_chain(entries: Sequence[Entry]) -> list[Issue]:
    """Section 24.4: a history is consistent when its entries form an unbroken, correct chain."""
    if not entries:
        return [Issue("history-inconsistent", "the history has no entry")]
    issues: list[Issue] = []
    for index, entry in enumerate(entries):
        previous = entries[index - 1].hash if index else ZERO_HASH
        problem = _entry_problem(entry, index + 1, previous)
        if problem is not None:
            issues.append(Issue("history-inconsistent", problem, f"entries[{index}]"))
    return issues


def _entry_problem(entry: Entry, expected_n: int, previous: str) -> str | None:
    if entry.n != expected_n:
        return f"entry {expected_n} has the position {entry.n}"
    if entry.prev != previous:
        return f"entry {entry.n} does not follow the hash of the entry before it"
    try:
        computed = entry_hash(entry.prev, entry.body)
    except DomainError as error:
        return f"entry {entry.n} holds a value outside the domain: {error}"
    if entry.hash != computed:
        return f"entry {entry.n} does not match its hash"
    return None


def check_anchor(entries: Sequence[Entry], anchor: Anchor) -> list[Issue]:
    """Compare a consistent history with the anchor: truncated, rewritten, or in agreement."""
    if len(entries) < anchor.position:
        return [
            Issue(
                "history-truncated",
                f"the history holds {len(entries)} entries and the anchor is at "
                f"position {anchor.position}: it was truncated or rolled back",
            )
        ]
    if entries[anchor.position - 1].hash != anchor.hash:
        return [
            Issue(
                "history-rewritten",
                f"entry {anchor.position} differs from the hash in the anchor: "
                "the history was rewritten",
            )
        ]
    return []


def verify_history(
    entries: Sequence[Entry], anchor: Anchor | None, *, require_anchor: bool = False
) -> Report:
    """Verify the consistency of a history and, where there is one, its agreement with the anchor.

    An implementation must not act on a history that this reports as anything but ok.
    """
    chain = verify_chain(entries)
    if chain:
        return Report(tuple(chain))
    if anchor is not None:
        return Report(tuple(check_anchor(entries, anchor)))
    if require_anchor:
        message = "the history has no anchor; a human has to adopt it (Section 24.4)"
        return Report((Issue("anchor-missing", message),))
    return Report()
