"""JSON Schema (Draft 2020-12) validation for governed GG-SAD artifacts.

This is the generic structural check (R-005, R-006, R-007). Semantic,
business-level checks that a JSON Schema cannot express -- such as the
companion authority rule in R-006/R-017 -- live in their own validators
(see `mapping_authority.py`) and are composed with this one by their
callers, not folded into it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from ggsad.models.validation import IssueCategory, ValidationIssue


def load_schema(schema_path: Path) -> dict[str, Any]:
    """Load a JSON Schema document from disk."""
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_against_schema(
    *,
    data: Any,  # noqa: ANN401 -- parsed YAML/JSON is dynamically typed until schema-checked
    schema: dict[str, Any],
    file_label: str,
) -> list[ValidationIssue]:
    """Validate `data` against `schema`.

    Returns every violation found (empty list if `data` is valid), each as
    a normalized :class:`ValidationIssue`.
    """
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))

    return [
        ValidationIssue(
            category=IssueCategory.SCHEMA_VIOLATION,
            file=file_label,
            field="/".join(str(segment) for segment in error.path) or None,
            reason=error.message,
        )
        for error in errors
    ]
