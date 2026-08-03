"""Normalized validation issue model shared by all GG-SAD validators.

Every validator in this package (YAML loading, JSON Schema checking, mapping
authority, and later the document and repository validators) reports its
findings as :class:`ValidationIssue` so CLI output stays consistent and
actionable, per CHG-001 R-015.
"""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class IssueCategory(StrEnum):
    """Category of a validation issue, used for grouping and remediation hints."""

    YAML_SYNTAX = "yaml_syntax"
    SCHEMA_VIOLATION = "schema_violation"
    MAPPING_AUTHORITY = "mapping_authority"
    MISSING_ARTIFACT = "missing_artifact"
    UNRESOLVED_PLACEHOLDER = "unresolved_placeholder"
    UNKNOWN_PROFILE = "unknown_profile"
    UNSUPPORTED_TRANSITION = "unsupported_transition"


class ValidationIssue(BaseModel):
    """A single actionable validation finding.

    Fields required by CHG-001 R-015: a category, the affected file, a
    concise reason, and (where determinable) a field locator and a
    remediation hint.
    """

    model_config = ConfigDict(frozen=True)

    category: IssueCategory
    file: str
    reason: str
    field: str | None = None
    remediation: str | None = None

    def __str__(self) -> str:
        location = f" ({self.field})" if self.field else ""
        hint = f" -- {self.remediation}" if self.remediation else ""
        return f"[{self.category.value}] {self.file}{location}: {self.reason}{hint}"
