"""Path patterns and the allowed path list of a change (Section 24.5).

A pattern without a wildcard names one path. A pattern that ends with `/` names every path below
that directory. In a pattern, `*` matches any characters inside one path segment, and a segment
that is exactly `**` matches any number of segments, including none. Letter case matters and
nothing is normalized.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

# The record files of the change are exempt, and so are exactly three further names (Section 24.5).
RECORD_FILES: Final = ("change.yaml", "spec.md", "state.json")
EXEMPT_FILES: Final = ("state.json.tmp", "state.json.lock", "review.md")


def pattern_valid(pattern: object) -> bool:
    """A pattern is invalid when empty, when it begins with `/`, or when a segment is `..`."""
    if not isinstance(pattern, str) or not pattern or pattern.startswith("/"):
        return False
    return ".." not in pattern.split("/")


@lru_cache(maxsize=512)
def _segment(pattern: str) -> re.Pattern[str]:
    return re.compile("[^/]*".join(re.escape(part) for part in pattern.split("*")) + r"\Z")


def _match_segments(pattern: Sequence[str], path: Sequence[str]) -> bool:
    if not pattern:
        return not path
    head, rest = pattern[0], pattern[1:]
    if head == "**":
        return any(_match_segments(rest, path[skip:]) for skip in range(len(path) + 1))
    if not path:
        return False
    return _segment(head).match(path[0]) is not None and _match_segments(rest, path[1:])


def matches(pattern: str, path: str) -> bool:
    """True when the pattern matches the path (both written relative to the repository root)."""
    if not pattern_valid(pattern):
        return False
    segments = path.split("/")
    if pattern.endswith("/"):
        # Every path below the directory: at least one more, non-empty segment must follow.
        return "" not in segments and _match_segments(
            [*pattern[:-1].split("/"), "*", "**"], segments
        )
    return _match_segments(pattern.split("/"), segments)


def is_record_file(path: str, change_dir: str) -> bool:
    """True for the record files of the change and the three exempt names in its directory."""
    prefix = change_dir.rstrip("/") + "/"
    if not path.startswith(prefix):
        return False
    return path[len(prefix) :] in (*RECORD_FILES, *EXEMPT_FILES)


def paths_outside(allow: Sequence[str], changed: Iterable[str], change_dir: str) -> list[str]:
    """The measured paths that no pattern of the allowed list matches, in code point order."""
    outside = {
        path
        for path in changed
        if not is_record_file(path, change_dir) and not any(matches(p, path) for p in allow)
    }
    return sorted(outside)
