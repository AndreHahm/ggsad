"""Unit tests for the normalized ValidationIssue model."""

from __future__ import annotations

import pytest

from ggsad.models.validation import IssueCategory, ValidationIssue


def test_str_includes_category_file_and_reason() -> None:
    issue = ValidationIssue(
        category=IssueCategory.SCHEMA_VIOLATION,
        file="config.yaml",
        reason="'project' is a required property",
    )

    text = str(issue)

    assert "schema_violation" in text
    assert "config.yaml" in text
    assert "'project' is a required property" in text


def test_str_includes_field_and_remediation_when_present() -> None:
    issue = ValidationIssue(
        category=IssueCategory.MAPPING_AUTHORITY,
        file="gsd.yaml",
        field="permissions/may_approve",
        reason="companion may not approve GG-SAD work",
        remediation="Set permissions.may_approve: false.",
    )

    text = str(issue)

    assert "(permissions/may_approve)" in text
    assert "-- Set permissions.may_approve: false." in text


def test_issue_is_frozen() -> None:
    issue = ValidationIssue(category=IssueCategory.SCHEMA_VIOLATION, file="x.yaml", reason="bad")

    with pytest.raises(Exception, match=r"frozen|Instance is frozen|immutable"):
        setattr(issue, "reason", "changed")  # noqa: B010 -- deliberately dynamic to avoid static rejection
