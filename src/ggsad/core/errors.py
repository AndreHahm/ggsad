"""Errors that stop an operation with the result `error` (Implementation Contract, Section 22.2).

An `error` writes nothing and leaves `changed` false. The code is stable; the message is for
humans.
"""

from __future__ import annotations


class StateError(Exception):
    """The operation could not be carried out, so nothing was written."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
