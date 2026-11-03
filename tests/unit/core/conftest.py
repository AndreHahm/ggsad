"""Fixtures shared by the tests of the core."""

from __future__ import annotations

from pathlib import Path

import pytest
from project_helpers import CONFIG, git, write


@pytest.fixture
def root(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    write(tmp_path, ".ggsad/config.yaml", CONFIG)
    write(tmp_path, "docs/constitution.md", "rules\n")
    write(tmp_path, "docs/project-brief.md", "Compliance profile: lean\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path
