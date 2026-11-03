"""Measuring the scope of a change with Git (Section 24.5).

The engine is pure; this module is the adapter that asks Git. It starts `git` with an argument
list and no shell. Every function that cannot get an answer from Git raises `GitError`, and
`measure_scope` turns that into the result `not_evaluable`, never into a pass or a violation.

The paths changed since the base revision are the paths whose content differs from the base
revision (committed, staged, or unstaged) and the untracked files that no ignore file hides. An
ignore file counts only when it is inside the repository and was in place at the base revision.
An exclude file in the metadata directory or an excludes file of the user is never applied.
"""

from __future__ import annotations

import re
import subprocess  # nosec B404 - the adapter must start git; see _git
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Final

from ggsad.core.gate_eval import NOT_EVALUABLE, NOT_SATISFIED, SATISFIED, Check
from ggsad.core.scope import is_record_file, paths_outside

if TYPE_CHECKING:
    from collections.abc import Sequence

IGNORE_FILE: Final = ".gitignore"
_REVISION: Final = re.compile(r"[0-9a-f]{7,64}")


class GitError(Exception):
    """Git is unavailable or could not answer."""


class NotARevisionError(GitError):
    """The text is not a commit hash, so it is never handed to Git."""

    def __init__(self, text: str) -> None:
        super().__init__(f"{text!r} is not a revision")


def _git(repo: Path, *args: str, stdin: bytes | None = None, ok: Sequence[int] = (0,)) -> bytes:
    command = ["git", "-C", str(repo), *args]
    try:
        # Fixed argument list, no shell; revisions are validated hashes (see _check_revision).
        done = subprocess.run(  # noqa: S603  # nosec B603  # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-audit.dangerous-subprocess-use-audit
            command,
            input=stdin,
            capture_output=True,
            check=False,
        )
    except OSError as error:
        raise GitError(str(error)) from error
    if done.returncode not in ok:
        message = done.stderr.decode("utf-8", "replace").strip()
        raise GitError(message or f"git {args[0]} ended with status {done.returncode}")
    return done.stdout


def _split(output: bytes) -> list[str]:
    return [item.decode("utf-8", "surrogateescape") for item in output.split(b"\0") if item]


def head_revision(repo: Path) -> str:
    """The revision the working copy is on: the revision a change would start from."""
    return _git(repo, "rev-parse", "--verify", "HEAD").decode().strip()


def _ignore_files_at(repo: Path, base: str) -> list[str]:
    listed = _split(_git(repo, "ls-tree", "-r", "--name-only", "-z", base))
    return [p for p in listed if p.rsplit("/", 1)[-1] == IGNORE_FILE]


def _hidden_at_base(repo: Path, base: str, paths: Sequence[str]) -> set[str]:
    """The paths that the ignore files of the base revision hide."""
    files = _ignore_files_at(repo, base)
    if not files or not paths:
        return set()
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        _git(root, "init", "-q", "--template=")
        for name in files:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(_git(repo, "show", f"{base}:{name}"))
        stdin = b"\0".join(p.encode("utf-8", "surrogateescape") for p in paths) + b"\0"
        empty = root / ".git" / "empty-excludes"
        empty.write_bytes(b"")
        exclude = f"core.excludesFile={empty}"
        args = ("-c", exclude, "check-ignore", "--no-index", "-z", "--stdin")
        out = _git(root, *args, stdin=stdin, ok=(0, 1))
        return set(_split(out))


def _check_revision(base: str) -> None:
    """A revision is a commit hash or HEAD, so it can never be read by Git as an option."""
    if base != "HEAD" and not _REVISION.fullmatch(base):
        raise NotARevisionError(base)


def changed_paths(repo: Path, base: str) -> list[str]:
    """The paths changed since the base revision, in code point order."""
    _check_revision(base)
    tracked = _split(
        _git(repo, "diff", "--name-only", "--no-renames", "--no-ext-diff", "-z", base, "--")
    )
    untracked = _split(_git(repo, "ls-files", "--others", "-z"))
    hidden = _hidden_at_base(repo, base, untracked)
    visible = [p for p in untracked if p not in hidden]
    return sorted({*tracked, *visible})


def unclean_paths(repo: Path, change_dir: str) -> list[str]:
    """Uncommitted work other than the record files of the change (Section 24.5)."""
    paths = changed_paths(repo, "HEAD")
    return [p for p in paths if not is_record_file(p, change_dir)]


def measure_scope(
    repo: Path, base: str | None, allow: Sequence[str] | None, change_dir: str
) -> Check:
    """The result of the scope violation gate for an active change (Section 24.5)."""
    if base is None:
        return Check(NOT_EVALUABLE, "no base revision was recorded")
    if allow is None:
        return Check(NOT_EVALUABLE, "the change definition has no allowed path list")
    try:
        changed = changed_paths(repo, base)
    except GitError as error:
        return Check(NOT_EVALUABLE, f"version control is unavailable: {error}")
    outside = paths_outside(allow, changed, change_dir)
    if outside:
        return Check(SATISFIED, "paths outside the scope: " + ", ".join(outside))
    return Check(NOT_SATISFIED)
