"""Change identifiers (Section 4.3): syntax, reserved names, and uniqueness.

Identifiers name a directory, so they must not hold a path separator, must not be a reserved
device name, and must stay unique on a file system that ignores letter case.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

from ggsad.core.issues import Issue

if TYPE_CHECKING:
    from collections.abc import Collection

_SYNTAX: Final = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_RESERVED: Final = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{n}" for n in range(1, 10)}
    | {f"lpt{n}" for n in range(1, 10)}
)


def ascii_lower(text: str) -> str:
    """Fold the ASCII upper case letters to lower case and leave every other code point alone."""
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in text)


def check_identifier(
    identifier: str,
    *,
    existing: Collection[str] = (),
    path: str = "id",
) -> list[Issue]:
    """Check an identifier against Section 4.3 and return the issues, empty when it is valid.

    The checks run in order and stop at the first failure, so one identifier yields one issue.
    """
    if _SYNTAX.fullmatch(identifier) is None or identifier.endswith("."):
        return [
            Issue(
                "id-invalid",
                f"identifier {identifier!r} must match [A-Za-z0-9][A-Za-z0-9._-]* "
                "and must not end with '.'",
                path,
            )
        ]
    if ascii_lower(identifier.split(".", 1)[0]) in _RESERVED:
        return [Issue("id-reserved", f"identifier {identifier!r} uses a reserved name", path)]
    folded = ascii_lower(identifier)
    if any(ascii_lower(other) == folded for other in existing):
        return [
            Issue(
                "id-not-unique",
                f"identifier {identifier!r} is not unique once letter case is ignored",
                path,
            )
        ]
    return []
