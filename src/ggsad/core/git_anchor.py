"""The default anchor store: one Git ref per change, inside the repository of the project.

An anchor is a small JSON blob. The ref `refs/ggsad/anchors/<change-id>` points at the blob, so the
anchor is outside the working tree and is not part of the history of any change. It protects
against accident and against an actor who can write the history and not the repository metadata.
It does not protect against an actor who can write both (Section 24.4).
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Final

from ggsad.core.errors import StateError
from ggsad.core.git_scope import GitError, run_git
from ggsad.core.history import Anchor
from ggsad.core.identifiers import check_identifier
from ggsad.core.values import as_int, as_mapping

if TYPE_CHECKING:
    from pathlib import Path

REF_PREFIX: Final = "refs/ggsad/anchors/"
PROBE_REF: Final = "refs/ggsad/probe"
_NOT_FOUND: Final = (0, 1)


class GitAnchorStore:
    """Anchors as Git refs that point at JSON blobs."""

    def __init__(self, repo: Path) -> None:
        self._repo = repo

    def _ref(self, change_id: str) -> str:
        if check_identifier(change_id):
            raise StateError("anchor-invalid", f"{change_id!r} is not a change identifier")
        return f"{REF_PREFIX}{change_id}"

    def read(self, change_id: str) -> Anchor | None:
        """The stored anchor, None when absent. A damaged blob is an error, never 'no anchor'."""
        ref = self._ref(change_id)
        try:
            found = run_git(self._repo, "rev-parse", "--verify", "--quiet", ref, ok=(0, 1))
            if not found.strip():
                return None
            text = run_git(self._repo, "cat-file", "blob", found.decode().strip()).decode("utf-8")
            data = as_mapping(json.loads(text))
        except (GitError, ValueError) as error:
            raise StateError("anchor-invalid", f"the anchor cannot be read: {error}") from error
        position = as_int(data.get("position")) if data is not None else None
        digest = data.get("hash") if data is not None else None
        if position is None or position < 1 or not isinstance(digest, str):
            raise StateError("anchor-invalid", "the anchor does not hold a position and a hash")
        return Anchor(position, digest)

    def prepare(self, change_id: str) -> None:
        """Check that a ref can be written now, without leaving a trace."""
        self._ref(change_id)
        try:
            blob = run_git(self._repo, "hash-object", "-w", "--stdin", stdin=b"{}").decode().strip()
            run_git(self._repo, "update-ref", PROBE_REF, blob)
            run_git(self._repo, "update-ref", "-d", PROBE_REF)
        except GitError as error:
            message = f"the anchor location is not writable: {error}"
            raise StateError("anchor-write-failed", message) from error

    def write(self, change_id: str, anchor: Anchor) -> None:
        """Point the ref at a new blob. Git replaces a ref in one step."""
        ref = self._ref(change_id)
        text = json.dumps({"position": anchor.position, "hash": anchor.hash}, indent=2) + "\n"
        try:
            blob = (
                run_git(self._repo, "hash-object", "-w", "--stdin", stdin=text.encode("utf-8"))
                .decode()
                .strip()
            )
            run_git(self._repo, "update-ref", ref, blob)
        except GitError as error:
            raise StateError(
                "anchor-write-failed", f"the anchor cannot be written: {error}"
            ) from error
