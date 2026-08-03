"""Unit tests for the typed ProjectConfig model."""

from __future__ import annotations

from ggsad.models.config import ProjectConfig

_VALID: dict = {
    "schema_version": "0.1",
    "project": {
        "id": "sample",
        "operating_mode": "stand-alone",
        "compliance_profile": "standard",
    },
    "method": {"name": "Goal-Gated Spec-Anchored Development", "version": "1.2"},
    "workflow": {"default_change_class": "M", "enabled_phases": ["specify", "plan"]},
    "pair_review": {
        "default_requirement": "optional",
        "distinct_requestor_and_reviewer": True,
        "required_for": [],
        "human_approval_required_for": [],
    },
    "integrations": [],
    "memory": {"enabled": False},
}


def test_parses_valid_config() -> None:
    config = ProjectConfig.model_validate(_VALID)

    assert config.project.compliance_profile == "standard"
    assert config.workflow.default_change_class == "M"
    assert config.integrations == []


def test_unmodeled_optional_sections_are_preserved_not_dropped() -> None:
    data = {**_VALID, "budgets": {"max_retry_count": 3}}

    config = ProjectConfig.model_validate(data)

    assert config.model_dump()["budgets"] == {"max_retry_count": 3}
