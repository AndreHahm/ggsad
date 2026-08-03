"""Unit tests for the package version marker."""

from __future__ import annotations

import re

from ggsad import __version__


def test_version_is_a_dotted_semver_like_string() -> None:
    assert re.match(r"^\d+\.\d+\.\d+$", __version__)
