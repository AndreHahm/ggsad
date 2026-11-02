"""Change identifiers (Section 4.3), including AE-001."""

from __future__ import annotations

import pytest

from ggsad.core.identifiers import ascii_lower, check_identifier


def codes(identifier: str, existing: tuple[str, ...] = ()) -> list[str]:
    return [issue.code for issue in check_identifier(identifier, existing=existing)]


def test_ae_001_identifier_that_can_leave_the_directory_or_collide_is_rejected() -> None:
    existing = ("Task-7",)

    assert codes("../x", existing) == ["id-invalid"]
    assert codes("a/b", existing) == ["id-invalid"]
    assert codes("task-7", existing) == ["id-not-unique"]
    assert codes("nul", existing) == ["id-reserved"]
    assert codes("c-1", existing) == []


@pytest.mark.parametrize("identifier", ["", ".x", "-x", "a b", "a.", "name\n", "café"])
def test_syntax_rejects(identifier: str) -> None:
    assert codes(identifier) == ["id-invalid"]


@pytest.mark.parametrize("identifier", ["con", "CON", "Prn.txt", "aux.v2", "com1", "LPT9.log"])
def test_reserved_names_are_rejected_by_the_part_before_the_first_dot(identifier: str) -> None:
    assert codes(identifier) == ["id-reserved"]


@pytest.mark.parametrize("identifier", ["com0", "com10", "console", "nul-1", "x.nul"])
def test_names_that_only_look_reserved_are_accepted(identifier: str) -> None:
    assert codes(identifier) == []


def test_uniqueness_folds_ascii_case_only() -> None:
    assert codes("ABC", ("abc",)) == ["id-not-unique"]
    assert codes("abc", ("abc",)) == ["id-not-unique"]
    assert codes("abc", ("abd",)) == []


def test_ascii_lower_leaves_other_code_points_alone() -> None:
    assert ascii_lower("AbC-É") == "abc-É"
