"""The anchor of a history (Section 24.4): where it is kept, how it advances, and `adopt`.

An anchor records the position and hash of the latest entry at a location outside the working
tree. It is written only after the append of that entry succeeded, it is only ever advanced along
the same chain, and `adopt` creates one for a history that has none.
"""

from __future__ import annotations

import json
import os
from typing import TYPE_CHECKING, Protocol

from ggsad.core.errors import StateError
from ggsad.core.history import Anchor, verify_chain
from ggsad.core.identifiers import check_identifier
from ggsad.core.values import as_int, as_mapping

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from ggsad.core.history import Entry


class AnchorStore(Protocol):
    """Where anchors are kept: outside the working tree of the project."""

    def read(self, change_id: str) -> Anchor | None:
        """The anchor of a change, or None when it has none."""
        ...

    def write(self, change_id: str, anchor: Anchor) -> None:
        """Store the anchor of a change. Callers use `advance_anchor` or `adopt_anchor`."""
        ...

    def prepare(self, change_id: str) -> None:
        """Raise StateError unless an anchor can be written now, so a write can be refused early."""
        ...


class FileAnchorStore:
    """Anchors as small JSON files in a directory outside the project."""

    def __init__(self, root: Path) -> None:
        self._root = root

    def _path(self, change_id: str) -> Path:
        if check_identifier(change_id):
            raise StateError("anchor-invalid", f"{change_id!r} is not a change identifier")
        return self._root / f"{change_id}.anchor.json"

    def read(self, change_id: str) -> Anchor | None:
        """The stored anchor, None when absent. A damaged file is an error, never 'no anchor'."""
        path = self._path(change_id)
        if not path.exists():
            return None
        try:
            data = as_mapping(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError) as error:
            raise StateError(
                "anchor-invalid", f"the anchor file cannot be read: {error}"
            ) from error
        position = as_int(data.get("position")) if data is not None else None
        digest = data.get("hash") if data is not None else None
        if position is None or position < 1 or not isinstance(digest, str):
            raise StateError(
                "anchor-invalid", "the anchor file does not hold a position and a hash"
            )
        return Anchor(position, digest)

    def prepare(self, change_id: str) -> None:
        """Check that the anchor location exists and is writable, without leaving a trace."""
        probe = self._path(change_id).with_suffix(".probe")
        try:
            self._root.mkdir(parents=True, exist_ok=True)
            probe.write_bytes(b"")
            probe.unlink()
        except OSError as error:
            message = f"the anchor location is not writable: {error}"
            raise StateError("anchor-write-failed", message) from error

    def write(self, change_id: str, anchor: Anchor) -> None:
        """Replace the anchor file atomically."""
        path = self._path(change_id)
        temporary = path.with_suffix(".tmp")
        text = json.dumps({"position": anchor.position, "hash": anchor.hash}, indent=2) + "\n"
        try:
            self._root.mkdir(parents=True, exist_ok=True)
            with temporary.open("w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            temporary.replace(path)
        except OSError as error:
            raise StateError(
                "anchor-write-failed", f"the anchor cannot be written: {error}"
            ) from error


def advance_anchor(store: AnchorStore, change_id: str, entries: Sequence[Entry]) -> Anchor:
    """Move the anchor to the latest entry, after a successful append.

    An existing anchor is only advanced along the same chain: it is never replaced and never set
    to an earlier position or a different hash.
    """
    current = store.read(change_id)
    if current is not None and not _same_chain(entries, current):
        raise StateError(
            "anchor-conflict",
            "the anchor does not belong to this history, and an anchor is never replaced",
        )
    latest = entries[-1]
    anchor = Anchor(latest.n, latest.hash)
    store.write(change_id, anchor)
    return anchor


def adopt_anchor(store: AnchorStore, change_id: str, entries: Sequence[Entry]) -> Anchor:
    """Create the anchor of a history that has none, at its latest entry (the `adopt` action).

    Adoption is rejected when an anchor exists and when the history is not consistent. A human who
    adopts takes responsibility for the completeness of the history at that moment.
    """
    if store.read(change_id) is not None:
        raise StateError("adopt-rejected", "the history already has an anchor")
    problems = verify_chain(entries)
    if problems:
        raise StateError("adopt-rejected", f"the history is not consistent: {problems[0].message}")
    latest = entries[-1]
    anchor = Anchor(latest.n, latest.hash)
    store.write(change_id, anchor)
    return anchor


def _same_chain(entries: Sequence[Entry], current: Anchor) -> bool:
    return len(entries) >= current.position and entries[current.position - 1].hash == current.hash
