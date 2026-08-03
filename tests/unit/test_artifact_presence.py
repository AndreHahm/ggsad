"""Unit tests for the required Class M artifact presence check (R-008, E-008)."""

from __future__ import annotations

from pathlib import Path

from ggsad.models.validation import IssueCategory
from ggsad.validators.artifact_presence import (
    REQUIRED_CLASS_M_ARTIFACTS,
    validate_required_artifacts,
)


def _touch_all_except(change_dir: Path, missing: str) -> None:
    change_dir.mkdir(parents=True)
    for name in REQUIRED_CLASS_M_ARTIFACTS:
        if name != missing:
            (change_dir / name).write_text("x", encoding="utf-8")


def test_complete_change_has_no_issues(tmp_path: Path) -> None:
    change_dir = tmp_path / "CHG-002-example"
    _touch_all_except(change_dir, missing="")

    assert validate_required_artifacts(change_dir) == []


def test_missing_plan_is_reported_explicitly(tmp_path: Path) -> None:
    """E-008: a missing plan.md is identified by change and file name."""
    change_dir = tmp_path / "CHG-002-example"
    _touch_all_except(change_dir, missing="plan.md")

    issues = validate_required_artifacts(change_dir)

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.MISSING_ARTIFACT
    assert issues[0].field == "plan.md"
    assert str(change_dir) in issues[0].file


def test_every_missing_artifact_is_reported(tmp_path: Path) -> None:
    change_dir = tmp_path / "CHG-002-example"
    change_dir.mkdir(parents=True)  # nothing created

    issues = validate_required_artifacts(change_dir)

    assert {issue.field for issue in issues} == set(REQUIRED_CLASS_M_ARTIFACTS)
