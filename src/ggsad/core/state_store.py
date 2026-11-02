"""The state document `state.json` and its safe writing (Implementation Contract, Section 25.1).

The document holds the history of a change. A write goes to a temporary file that is flushed and
then replaces the document in one step, under an exclusive lock, and only if no other writer
changed the document since this writer read it.
"""

from __future__ import annotations

import json
import os
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from ggsad.core.anchor import AnchorStore, advance_anchor
from ggsad.core.canonical import ZERO_HASH, DomainError
from ggsad.core.change_definition import SUPPORTED_SCHEMA_VERSIONS
from ggsad.core.errors import StateError
from ggsad.core.history import Entry, make_entry, verify_history
from ggsad.core.values import as_int, as_list, as_mapping

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping
    from pathlib import Path
    from typing import IO

if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

STATE_FILE: Final = "state.json"
TEMPORARY_FILE: Final = "state.json.tmp"
LOCK_FILE: Final = "state.json.lock"


@dataclass(frozen=True)
class StateDocument:
    """The parsed state document: a schema version and the entries of the history."""

    schema_version: str
    entries: tuple[Entry, ...]

    def to_text(self) -> str:
        """The JSON text to write. Its layout is free; hashes never depend on it."""
        document = {
            "schema_version": self.schema_version,
            "entries": [entry.to_json() for entry in self.entries],
        }
        return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def parse_state_document(text: str) -> StateDocument:
    """Parse the text of a state document. Raises StateError when it is not a valid document."""
    data = _load(text)
    entries = as_list(data.get("entries")) if data is not None else None
    if data is None or set(data) != {"schema_version", "entries"} or entries is None:
        raise StateError(
            "state-document-invalid", "a state document holds schema_version and entries"
        )
    version = data["schema_version"]
    if not isinstance(version, str):
        raise StateError("schema-version-unsupported", "schema_version must be a string")
    return StateDocument(version, tuple(_parse_entry(item, i) for i, item in enumerate(entries)))


def _load(text: str) -> Mapping[str, object] | None:
    try:
        return as_mapping(
            json.loads(
                text,
                object_pairs_hook=_no_repeated_keys,
                parse_float=_reject_number,
                parse_constant=_reject_number,
            )
        )
    except (ValueError, DomainError) as error:
        message = f"the state document is not valid: {error}"
        raise StateError("state-document-invalid", message) from error


class _RepeatedKeyError(ValueError):
    def __init__(self, key: str) -> None:
        super().__init__(f"the key {key!r} is repeated")


def _no_repeated_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _RepeatedKeyError(key)
        result[key] = value
    return result


def _reject_number(text: str) -> object:
    raise DomainError("", f"{text} is a number outside the domain")


def _parse_entry(item: object, index: int) -> Entry:
    fields = as_mapping(item)
    if fields is None or set(fields) != {"n", "prev", "body", "hash"}:
        raise StateError(
            "state-document-invalid", f"entry {index + 1} holds exactly n, prev, body, and hash"
        )
    number, body = as_int(fields["n"]), as_mapping(fields["body"])
    if number is None or body is None:
        raise StateError("state-document-invalid", f"entry {index + 1} has an invalid n or body")
    prev, digest = fields["prev"], fields["hash"]
    if not isinstance(prev, str) or not isinstance(digest, str):
        raise StateError("state-document-invalid", f"entry {index + 1} has an invalid hash")
    return Entry(number, prev, body, digest)


class StateStore:
    """The state document of one change, with locked, atomic, conflict-checked appends."""

    def __init__(
        self,
        change_dir: Path,
        *,
        anchors: AnchorStore | None = None,
        require_anchor: bool = False,
        change_id: str | None = None,
    ) -> None:
        if require_anchor and anchors is None:
            raise StateError(
                "anchor-required", "a required anchor needs an anchor store; none was given"
            )
        self._dir = change_dir
        self._anchors = anchors
        self._require_anchor = require_anchor
        self._change_id = change_id or change_dir.name

    @property
    def state_path(self) -> Path:
        """The state document."""
        return self._dir / STATE_FILE

    def read(self) -> StateDocument | None:
        """The state document, or None when the change has none. A leftover .tmp file is ignored."""
        try:
            text = self.state_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except (OSError, UnicodeDecodeError) as error:
            raise StateError(
                "state-read-failed", f"the state document cannot be read: {error}"
            ) from error
        document = parse_state_document(text)
        _check_schema_version(document)
        return document

    def verify(self, document: StateDocument) -> None:
        """Raise StateError unless the history is consistent and agrees with its anchor."""
        anchor = self._anchors.read(self._change_id) if self._anchors is not None else None
        report = verify_history(document.entries, anchor, require_anchor=self._require_anchor)
        if not report.ok:
            issue = report.issues[0]
            raise StateError(issue.code, issue.message)

    def append(self, body: Mapping[str, object], *, read_version: int) -> Entry:
        """Append one entry. `read_version` is the number of entries the writer read (0 if none).

        Raises StateError (result `error`) on a conflict, a lock that cannot be taken, a damaged
        history, or a failed write; nothing is written in those cases.
        """
        self._dir.mkdir(parents=True, exist_ok=True)
        with _exclusive_lock(self._dir / LOCK_FILE):
            document = self.read()
            current = len(document.entries) if document is not None else 0
            if current != read_version:
                raise StateError(
                    "state-conflict",
                    f"another writer changed the change (read {read_version} entries, found "
                    f"{current}); read it again and repeat the operation",
                )
            if document is not None:
                self.verify(document)
            entry = self._build_entry(document, body)
            if self._anchors is not None:
                # Refuse before writing: after the replacement the entry cannot be taken back.
                self._anchors.prepare(self._change_id)
            entries = (*(document.entries if document else ()), entry)
            version = document.schema_version if document else SUPPORTED_SCHEMA_VERSIONS[-1]
            self._replace(StateDocument(version, entries))
            self._advance_anchor(entries)
        return entry

    def _build_entry(self, document: StateDocument | None, body: Mapping[str, object]) -> Entry:
        previous = document.entries[-1].hash if document is not None else ZERO_HASH
        number = len(document.entries) + 1 if document is not None else 1
        return make_entry(number, previous, body)

    def _replace(self, document: StateDocument) -> None:
        temporary = self._dir / TEMPORARY_FILE
        try:
            with temporary.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(document.to_text())
                handle.flush()
                os.fsync(handle.fileno())
            temporary.replace(self.state_path)
        except OSError as error:
            raise StateError(
                "state-write-failed", f"the state document cannot be written: {error}"
            ) from error

    def _advance_anchor(self, entries: tuple[Entry, ...]) -> None:
        """After a successful append: create the anchor with the first entry, then advance it."""
        if self._anchors is None:
            return
        try:
            if len(entries) == 1 or self._anchors.read(self._change_id) is not None:
                advance_anchor(self._anchors, self._change_id, entries)
        except StateError as error:
            raise StateError(
                "anchor-lagging",
                f"entry {entries[-1].n} was recorded, but the anchor was not advanced "
                f"({error.message}); repeat the advance or adopt the history",
            ) from error


def _check_schema_version(document: StateDocument) -> None:
    if document.schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise StateError(
            "schema-version-unsupported",
            f"schema_version {document.schema_version!r} is not supported",
        )
    if document.entries:
        after = as_mapping(document.entries[-1].body.get("after"))
        if after is None or after.get("schema_version") != document.schema_version:
            raise StateError(
                "schema-version-mismatch",
                "schema_version differs from the version recorded in the last entry",
            )


@contextmanager
def _exclusive_lock(path: Path) -> Iterator[None]:
    """An exclusive lock that the system releases when the process ends.

    A lock file that is left behind is not a held lock. A writer that cannot take the lock does
    not write.
    """
    try:
        handle = path.open("a+b")
    except OSError as error:
        raise StateError(
            "lock-unavailable", f"the lock object cannot be opened: {error}"
        ) from error
    try:
        _lock(handle)
        try:
            yield
        finally:
            _unlock(handle)
    finally:
        handle.close()


def _lock(handle: IO[bytes]) -> None:
    try:
        if sys.platform == "win32":
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as error:
        raise StateError("lock-unavailable", "another writer holds the lock") from error


def _unlock(handle: IO[bytes]) -> None:
    if sys.platform == "win32":
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
