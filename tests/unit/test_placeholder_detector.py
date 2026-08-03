"""Unit tests for unresolved-placeholder detection (R-009)."""

from __future__ import annotations

from pathlib import Path

from ggsad.models.validation import IssueCategory
from ggsad.validators.placeholder_detector import (
    find_unresolved_placeholders,
    validate_no_unresolved_placeholders,
)


def test_finds_bare_placeholder_in_prose() -> None:
    assert find_unresolved_placeholders("- Project: <project-name>") == ["<project-name>"]


def test_finds_multiple_distinct_placeholders() -> None:
    text = "- Created: <YYYY-MM-DD>\n- Approver: <name-or-role>\n"
    assert find_unresolved_placeholders(text) == ["<YYYY-MM-DD>", "<name-or-role>"]


def test_ignores_placeholders_inside_fenced_code_blocks() -> None:
    text = "Real prose.\n```bash\nggsad new <CHANGE_ID> <SLUG>\n```\nMore prose.\n"
    assert find_unresolved_placeholders(text) == []


def test_ignores_placeholders_inside_inline_code_spans() -> None:
    text = "Creates a change under `specs/<change-id>-<slug>/`."
    assert find_unresolved_placeholders(text) == []


def test_bare_placeholder_outside_code_is_still_found_alongside_inline_code() -> None:
    text = "See `specs/<change-id>-<slug>/`. Approver: <name-or-role>."
    assert find_unresolved_placeholders(text) == ["<name-or-role>"]


def test_ordinary_prose_with_no_angle_brackets_is_clean() -> None:
    text = "This is a normal sentence with no placeholders at all."
    assert find_unresolved_placeholders(text) == []


def test_validate_no_unresolved_placeholders_on_clean_file(tmp_path: Path) -> None:
    path = tmp_path / "clean.md"
    path.write_text("Nothing to see here.\n", encoding="utf-8")

    assert validate_no_unresolved_placeholders(path) == []


def test_validate_no_unresolved_placeholders_reports_issue(tmp_path: Path) -> None:
    path = tmp_path / "dirty.md"
    path.write_text("- Approver: <name-or-role>\n", encoding="utf-8")

    issues = validate_no_unresolved_placeholders(path)

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.UNRESOLVED_PLACEHOLDER
    assert "<name-or-role>" in issues[0].reason
