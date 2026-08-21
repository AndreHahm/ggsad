"""Unit tests for unconditional Class M artifact presence (R-008, E-008)."""

from __future__ import annotations

from pathlib import Path

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


def test_missing_conditional_plan_is_allowed(tmp_path: Path) -> None:
    change_dir = tmp_path / "CHG-002-example"
    _touch_all_except(change_dir, missing="plan.md")

    issues = validate_required_artifacts(change_dir)

    assert issues == []


def test_every_missing_artifact_is_reported(tmp_path: Path) -> None:
    change_dir = tmp_path / "CHG-002-example"
    change_dir.mkdir(parents=True)  # nothing created

    issues = validate_required_artifacts(change_dir)

    assert {issue.field for issue in issues} == {"state.yaml", "spec.md"}
