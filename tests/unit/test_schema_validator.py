"""Unit tests for generic JSON Schema validation."""

from __future__ import annotations

from ggsad.models.validation import IssueCategory
from ggsad.validators.schema_validator import validate_against_schema

_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["name"],
    "properties": {
        "name": {"type": "string"},
        "count": {"type": "integer", "minimum": 0},
    },
}


def test_valid_data_produces_no_issues() -> None:
    issues = validate_against_schema(
        data={"name": "ok", "count": 3}, schema=_SCHEMA, file_label="fixture.yaml"
    )

    assert issues == []


def test_missing_required_field_is_reported() -> None:
    issues = validate_against_schema(data={"count": 3}, schema=_SCHEMA, file_label="fixture.yaml")

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.SCHEMA_VIOLATION
    assert issues[0].file == "fixture.yaml"
    assert "name" in issues[0].reason


def test_multiple_violations_are_all_reported() -> None:
    issues = validate_against_schema(
        data={"count": -1, "extra": True}, schema=_SCHEMA, file_label="fixture.yaml"
    )

    # missing 'name', 'count' below minimum, and disallowed 'extra' property
    assert len(issues) == 3


def test_field_locator_uses_json_pointer_style_path() -> None:
    schema = {
        "type": "object",
        "properties": {"nested": {"type": "object", "required": ["value"]}},
    }
    issues = validate_against_schema(data={"nested": {}}, schema=schema, file_label="fixture.yaml")

    assert issues[0].field == "nested"
