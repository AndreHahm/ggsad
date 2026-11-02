"""Narrowing helpers for parsed YAML values.

A change definition is a parsed YAML document, so every value starts as `object`. These helpers
narrow a value to the shape a rule expects without raising.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast


def as_mapping(value: object) -> Mapping[str, object] | None:
    """Return the value as a mapping with string keys, or None."""
    if isinstance(value, Mapping) and all(isinstance(key, str) for key in value):
        return cast("Mapping[str, object]", value)
    return None


def as_list(value: object) -> list[object] | None:
    """Return the value as a list, or None. Strings are not lists."""
    if isinstance(value, list):
        return cast("list[object]", value)
    return None


def as_text(value: object) -> str | None:
    """Return the value as a non-empty string, or None."""
    if isinstance(value, str) and value.strip():
        return value
    return None


def as_int(value: object) -> int | None:
    """Return the value as an integer, or None. A boolean is not an integer."""
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    return None


def text_list(value: object) -> list[str] | None:
    """Return the value as a list of non-empty strings, or None."""
    items = as_list(value)
    if items is None:
        return None
    texts = [as_text(item) for item in items]
    if any(text is None for text in texts):
        return None
    return [text for text in texts if text is not None]
