"""Unit tests for the compliance-profile identity check (E-006)."""

from __future__ import annotations

from pathlib import Path

from ggsad.models.config import ProjectConfig
from ggsad.models.validation import IssueCategory
from ggsad.validators.compliance_profile import validate_compliance_profile

_BASE: dict = {
    "schema_version": "0.1",
    "project": {
        "id": "sample",
        "operating_mode": "stand-alone",
        "compliance_profile": "standard",
    },
    "method": {"name": "Goal-Gated Spec-Anchored Development", "version": "1.2"},
    "workflow": {"default_change_class": "M", "enabled_phases": ["specify"]},
    "pair_review": {
        "default_requirement": "optional",
        "distinct_requestor_and_reviewer": True,
        "required_for": [],
        "human_approval_required_for": [],
    },
    "integrations": [],
    "memory": {"enabled": False},
}


def _config_with_profile(profile: str) -> ProjectConfig:
    data = {**_BASE, "project": {**_BASE["project"], "compliance_profile": profile}}
    return ProjectConfig.model_validate(data)


def test_each_builtin_profile_is_accepted(tmp_path: Path) -> None:
    for profile in ("lean", "standard", "governed", "regulated"):
        config = _config_with_profile(profile)
        issues = validate_compliance_profile(config, tmp_path, file_label="config.yaml")
        assert issues == [], profile


def test_unknown_profile_with_no_custom_file_is_rejected(tmp_path: Path) -> None:
    config = _config_with_profile("made-up-profile")

    issues = validate_compliance_profile(config, tmp_path, file_label="config.yaml")

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.UNKNOWN_PROFILE
    assert "made-up-profile" in issues[0].reason


def test_unknown_profile_with_matching_custom_file_is_accepted(tmp_path: Path) -> None:
    profiles_dir = tmp_path / ".ggsad" / "profiles"
    profiles_dir.mkdir(parents=True)
    (profiles_dir / "custom-team-profile.yaml").write_text("{}\n", encoding="utf-8")
    config = _config_with_profile("custom-team-profile")

    issues = validate_compliance_profile(config, tmp_path, file_label="config.yaml")

    assert issues == []
