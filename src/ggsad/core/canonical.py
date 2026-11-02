"""The canonical form and the hash string (Implementation Contract, Section 25.1).

Everything that is hashed in GG-SAD is hashed over its canonical form, never over the text of a
file, so layout and key order have no effect. The values of the domain are strings, integers,
booleans, `null`, arrays, and objects whose keys are strings.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping
from typing import Final, cast

MAX_INTEGER: Final = 2**53 - 1
_FIRST_PRINTABLE: Final = 0x20
HASH_PREFIX: Final = "sha256:"
ZERO_HASH: Final = HASH_PREFIX + "0" * 64
HASH_PATTERN: Final = re.compile(r"sha256:[0-9a-f]{64}")
_SURROGATE: Final = re.compile("[" + chr(0xD800) + "-" + chr(0xDFFF) + "]")
_ESCAPES: Final = {
    '"': '\\"',
    "\\": "\\\\",
    "\b": "\\b",
    "\t": "\\t",
    "\n": "\\n",
    "\f": "\\f",
    "\r": "\\r",
}


class DomainError(ValueError):
    """A value is outside the domain, so it can be neither written nor hashed."""

    def __init__(self, path: str, reason: str) -> None:
        super().__init__(f"{path or '<root>'}: {reason}")
        self.path = path
        self.reason = reason


def canonical_text(value: object) -> str:
    """Return the canonical form of the value, or raise DomainError."""
    return _canonical(value, "")


def canonical_bytes(value: object) -> bytes:
    """The UTF-8 encoding of the canonical form, without a byte order mark or a final newline."""
    return canonical_text(value).encode("utf-8")


def hash_bytes(data: bytes) -> str:
    """The hash string of some bytes: `sha256:` and 64 lowercase hexadecimal digits."""
    return HASH_PREFIX + hashlib.sha256(data).hexdigest()


def hash_value(value: object) -> str:
    """The hash string of a value, which is the hash string of its canonical bytes."""
    return hash_bytes(canonical_bytes(value))


def is_hash_string(value: object) -> bool:
    """True for a hash string written exactly as Section 25.1 requires (lowercase digits)."""
    return isinstance(value, str) and HASH_PATTERN.fullmatch(value) is not None


def _canonical(value: object, path: str) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return _integer(value, path)
    if isinstance(value, str):
        return _string(value, path)
    return _composite(value, path)


def _composite(value: object, path: str) -> str:
    if isinstance(value, list):
        items = [_canonical(item, f"{path}[{index}]") for index, item in enumerate(value)]
        return "[" + ",".join(items) + "]"
    if isinstance(value, Mapping):
        return _object(cast("Mapping[object, object]", value), path)
    raise DomainError(path, f"a {type(value).__name__} is not in the domain")


def _integer(value: int, path: str) -> str:
    if abs(value) > MAX_INTEGER:
        raise DomainError(path, "an integer must not exceed 2**53 - 1 in magnitude")
    return str(value)


def _string(value: str, path: str) -> str:
    if _SURROGATE.search(value):
        raise DomainError(path, "a string must not hold a surrogate code point")
    return '"' + "".join(_escape(char) for char in value) + '"'


def _escape(char: str) -> str:
    if char in _ESCAPES:
        return _ESCAPES[char]
    if ord(char) < _FIRST_PRINTABLE:
        return f"\\u{ord(char):04x}"
    return char


def _object(value: Mapping[object, object], path: str) -> str:
    for key in value:
        if not isinstance(key, str):
            raise DomainError(path, "an object key must be a string")
    # Python orders strings by code point, which is the order that Section 25.1 requires.
    members = [
        f"{_string(str(key), path)}:{_canonical(value[key], f'{path}.{key}')}"
        for key in sorted(str(key) for key in value)
    ]
    return "{" + ",".join(members) + "}"
