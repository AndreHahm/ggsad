"""Integration tests: validate this repository's own governed artifacts.

This is the permanent regression coverage for what was, during CHG-001
Slice 2 development, an ad hoc one-off script: confirming
`.ggsad/config.yaml`, `.ggsad/mappings/gsd.yaml`, and CHG-001's own
`state.yaml` stay schema-valid, model-parseable, and (for the mapping)
authority-compliant as the repository evolves.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ggsad.models.config import ProjectConfig
from ggsad.models.mapping import IntegrationMapping
from ggsad.models.state import ChangeState
from ggsad.validators.mapping_authority import validate_mapping_authority
from ggsad.validators.schema_validator import load_schema, validate_against_schema
from ggsad.validators.yaml_loader import YamlLoadError, load_yaml_file, load_yaml_text

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_project_config_is_schema_and_model_valid() -> None:
    path = REPO_ROOT / ".ggsad" / "config.yaml"
    schema = load_schema(REPO_ROOT / ".ggsad" / "schemas" / "config.schema.json")
    data = load_yaml_file(path)

    issues = validate_against_schema(data=data, schema=schema, file_label=str(path))
    assert issues == []

    config = ProjectConfig.model_validate(data)
    assert config.project.id == "ggsad-reference-implementation"


def test_gsd_mapping_is_schema_valid_model_valid_and_authority_compliant() -> None:
    path = REPO_ROOT / ".ggsad" / "mappings" / "gsd.yaml"
    schema = load_schema(REPO_ROOT / ".ggsad" / "schemas" / "mappings.schema.json")
    data = load_yaml_file(path)

    issues = validate_against_schema(data=data, schema=schema, file_label=str(path))
    assert issues == []

    mapping = IntegrationMapping.model_validate(data)
    authority_issues = validate_mapping_authority(mapping, file_label=str(path))
    assert authority_issues == []


def test_chg_001_state_is_schema_and_model_valid() -> None:
    path = REPO_ROOT / "specs" / "CHG-001-reference-repository-bootstrap" / "state.yaml"
    schema = load_schema(REPO_ROOT / ".ggsad" / "schemas" / "state.schema.json")
    data = load_yaml_file(path)

    issues = validate_against_schema(data=data, schema=schema, file_label=str(path))
    assert issues == []

    state = ChangeState.model_validate(data)
    assert state.change.id == "CHG-001"
    assert state.flow.phase == "specify"
    # Was "draft" through Slices 1-6; CHG-001 reached specify/ready in Slice 7 once
    # evidence.md existed and its own draft->ready transition preconditions held.
    assert state.flow.status == "ready"
    assert len(state.history) >= 1


def test_e005_invalid_project_yaml_is_rejected_with_actionable_location() -> None:
    """E-005: invalid YAML in `.ggsad/config.yaml` is rejected without a stack trace,
    identifying the file and the parse location."""
    broken = "project:\n  id: [unterminated\n"

    with pytest.raises(YamlLoadError) as excinfo:
        load_yaml_text(broken, source=".ggsad/config.yaml")

    assert str(Path(".ggsad/config.yaml")) in str(excinfo.value)
    assert excinfo.value.line is not None


def test_e007_mapping_granting_approval_authority_is_rejected() -> None:
    """E-007: a mapping that sets `may_approve: true` fails validation with an
    explanation that the companion may not approve GG-SAD work."""
    schema = load_schema(REPO_ROOT / ".ggsad" / "schemas" / "mappings.schema.json")
    data = load_yaml_file(REPO_ROOT / ".ggsad" / "mappings" / "gsd.yaml")
    mutated = {**data, "permissions": {**data["permissions"], "may_approve": True}}

    # Structurally still schema-valid: the schema only constrains the type.
    assert validate_against_schema(data=mutated, schema=schema, file_label="gsd.yaml") == []

    mapping = IntegrationMapping.model_validate(mutated)
    issues = validate_mapping_authority(mapping, file_label="gsd.yaml")

    assert len(issues) == 1
    assert "approve" in issues[0].reason
