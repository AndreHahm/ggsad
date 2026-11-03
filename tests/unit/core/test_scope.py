"""Path patterns and the allowed path list: AE-046, AE-047, AE-050, AE-051."""

from __future__ import annotations

import pytest

from ggsad.core.scope import is_record_file, matches, paths_outside, pattern_valid


@pytest.mark.parametrize(
    ("pattern", "path", "expected"),
    [
        ("lib/**", "lib/net/client.py", True),  # AE-046
        ("lib/**", "lib", True),
        ("lib/**", "docs/guide.md", False),  # AE-047
        ("src/app.py", "src/app.py", True),
        ("src/app.py", "src/App.py", False),
        ("docs/", "docs/a/b.md", True),
        ("docs/", "docs/", False),
        ("docs/", "docsx/a", False),
        ("*.md", "readme.md", True),
        ("*.md", "docs/readme.md", False),
        ("**/*.py", "a/b/c.py", True),
        ("**/*.py", "c.py", True),
        ("a/**/z", "a/z", True),
        ("a/**/z", "a/b/c/z", True),
        ("a/**/z", "a/b/c/y", False),
        ("lib/?.py", "lib/?.py", True),
        ("lib/?.py", "lib/a.py", False),
        ("café", "café", False),  # nothing is normalized (AE-034)
    ],
)
def test_matching(pattern: str, path: str, expected: bool) -> None:
    assert matches(pattern, path) is expected


@pytest.mark.parametrize("pattern", ["", "/abs", "a/../b", "..", 3, None])
def test_invalid_patterns(pattern: object) -> None:
    assert not pattern_valid(pattern)
    assert not matches(str(pattern), "a")


def test_ae050_record_files_are_exempt_and_other_files_are_measured() -> None:
    changed = ["specs/c-1/spec.md", "specs/c-1/state.json", "specs/c-1/notes.md", "lib/a.py"]
    assert paths_outside(["lib/**"], changed, "specs/c-1") == ["specs/c-1/notes.md"]


def test_ae051_interrupted_write_files_are_exempt_and_backups_are_not() -> None:
    exempt = ["specs/c-1/state.json.tmp", "specs/c-1/state.json.lock", "specs/c-1/review.md"]
    assert paths_outside(["lib/**"], exempt, "specs/c-1") == []
    assert paths_outside(["lib/**"], ["specs/c-3/state.json.bak"], "specs/c-3") == [
        "specs/c-3/state.json.bak"
    ]
    assert not is_record_file("other/spec.md", "specs/c-1")
    assert is_record_file("specs/c-1/change.yaml", "specs/c-1/")


def test_an_empty_allowed_list_allows_nothing_and_no_change_is_in_scope() -> None:
    assert paths_outside([], ["a.py"], "specs/c") == ["a.py"]
    assert paths_outside([], [], "specs/c") == []


def test_outside_paths_are_in_code_point_order() -> None:
    assert paths_outside(["x"], ["b", "B", "a"], "specs/c") == ["B", "a", "b"]


@pytest.mark.parametrize(
    ("pattern", "path", "expected"),
    [
        ("src/*/", "src/core/file.py", True),
        ("src/*/", "src/a", False),
        ("src/*/", "src/", False),
        ("src/*/", "lib/core/file.py", False),
        ("a/**/", "a/b/c.py", True),
        ("a/**/", "a/c.py", True),
        ("a/**/", "a", False),
        ("a/**/", "x/b/c.py", False),
    ],
)
def test_wildcards_in_a_trailing_directory_pattern(pattern: str, path: str, expected: bool) -> None:
    assert matches(pattern, path) is expected
