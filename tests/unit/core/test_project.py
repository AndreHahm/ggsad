"""Reading the project from disk: settings, fingerprint, hashes, documents, profile check."""

from __future__ import annotations

from pathlib import Path

import pytest

from ggsad.core.project import (
    ADR_DIRECTORY,
    BRIEF_PATH,
    CONFIG_PATH,
    CONSTITUTION_PATH,
    brief_profile,
    conflict_line_issues,
    definitions_hash,
    document_fingerprint,
    load_settings,
    missing_documents,
    profile_issue,
    read_yaml_file,
)

CONFIG = """\
schema_version: "1.0"
project: {id: demo, compliance_profile: lean}
roles: {owner: "human:ada"}
"""


def write(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_settings_are_read_from_the_config_file(tmp_path: Path) -> None:
    write(tmp_path, CONFIG_PATH, CONFIG)
    settings, issues = load_settings(tmp_path)
    assert issues == () and settings is not None
    assert settings.project_id == "demo"


def test_a_missing_config_file_is_an_issue_not_an_exception(tmp_path: Path) -> None:
    settings, issues = load_settings(tmp_path)
    assert settings is None
    assert [i.code for i in issues] == ["config-missing"]


def test_a_config_that_is_not_yaml_is_an_issue(tmp_path: Path) -> None:
    write(tmp_path, CONFIG_PATH, "a: [unclosed")
    settings, issues = load_settings(tmp_path)
    assert settings is None
    assert [i.code for i in issues] == ["config-invalid"]


def test_an_unusable_schema_version_is_refused(tmp_path: Path) -> None:
    write(tmp_path, CONFIG_PATH, CONFIG.replace('"1.0"', '"2.0"'))
    settings, issues = load_settings(tmp_path)
    assert settings is None
    assert "schema-version-unsupported" in [i.code for i in issues]


def test_a_file_that_is_not_text_is_unreadable(tmp_path: Path) -> None:
    (tmp_path / "x.yaml").write_bytes(b"\xff\xfe\x00")
    value, issue = read_yaml_file(tmp_path / "x.yaml", "config")
    assert value is None and issue is not None and issue.code == "config-unreadable"


def test_the_gate_hash_ignores_comments_and_key_order() -> None:
    first = definitions_hash({"gates": {"done": [], "fail": []}, "goal": "a"})
    second = definitions_hash({"goal": "b", "gates": {"fail": [], "done": []}})
    assert first == second


def test_the_gate_hash_changes_with_a_gate_the_scope_or_an_evidence_command() -> None:
    base = {"gates": {"done": []}, "scope": {"allow": ["a/"]}, "requirements": []}
    reference = definitions_hash(base)
    assert definitions_hash({**base, "gates": {"done": [{"id": "x"}]}}) != reference
    assert definitions_hash({**base, "scope": {"allow": ["b/"]}}) != reference
    with_evidence = {**base, "requirements": [{"id": "r1", "evidence": [{"command": ["t"]}]}]}
    assert definitions_hash(with_evidence) != reference


def test_the_gate_hash_ignores_the_goal_text() -> None:
    one = {"gates": {}, "requirements": [{"id": "r1", "text": "a", "evidence": None}]}
    two = {"gates": {}, "requirements": [{"id": "r1", "text": "b", "evidence": None}]}
    assert definitions_hash(one) == definitions_hash(two)


def test_no_gates_means_no_hash() -> None:
    assert definitions_hash({"goal": "x"}) is None


def test_the_fingerprint_holds_the_documents_that_exist(tmp_path: Path) -> None:
    write(tmp_path, CONSTITUTION_PATH, "rules\n")
    write(tmp_path, f"{ADR_DIRECTORY}/ADR-2-b.md", "b\n")
    write(tmp_path, f"{ADR_DIRECTORY}/ADR-1-a.md", "a\n")
    write(tmp_path, f"{ADR_DIRECTORY}/notes.txt", "ignored\n")
    fingerprint = document_fingerprint(tmp_path)
    assert list(fingerprint) == [
        CONSTITUTION_PATH,
        f"{ADR_DIRECTORY}/ADR-1-a.md",
        f"{ADR_DIRECTORY}/ADR-2-b.md",
    ]


def test_an_edit_changes_the_fingerprint_and_line_endings_do_not(tmp_path: Path) -> None:
    write(tmp_path, CONSTITUTION_PATH, "rules\n")
    before = document_fingerprint(tmp_path)
    (tmp_path / CONSTITUTION_PATH).write_bytes(b"rules\r\n")
    assert document_fingerprint(tmp_path) == before
    write(tmp_path, CONSTITUTION_PATH, "other rules\n")
    assert document_fingerprint(tmp_path) != before


def test_required_documents_depend_on_the_profile(tmp_path: Path) -> None:
    write(tmp_path, BRIEF_PATH, "x")
    assert missing_documents(tmp_path, "lean") == [CONSTITUTION_PATH]
    assert len(missing_documents(tmp_path, "standard")) == 3
    assert missing_documents(tmp_path, "unknown") == []


@pytest.mark.parametrize(
    ("text", "codes"),
    [
        (None, ["spec-missing"]),
        ("# Spec\n", ["conflict-line-missing"]),
        ("Conflicts with higher documents:\n", ["conflict-line-missing"]),
        ("Conflicts with higher documents: none\n", []),
        ("x\nConflicts with higher documents: ADR-1, architecture\ny\n", []),
    ],
)
def test_the_conflict_line_is_required(text: str | None, codes: list[str]) -> None:
    assert [code for code, _ in conflict_line_issues(text)] == codes


def test_a_brief_and_a_config_with_different_profiles_are_reported(tmp_path: Path) -> None:
    write(tmp_path, CONFIG_PATH, CONFIG)
    settings, _ = load_settings(tmp_path)
    assert settings is not None
    assert profile_issue(tmp_path, settings) is None
    write(tmp_path, BRIEF_PATH, "Compliance profile: lean\n")
    assert brief_profile(tmp_path) == "lean"
    assert profile_issue(tmp_path, settings) is None
    write(tmp_path, BRIEF_PATH, "Compliance profile: governed\n")
    issue = profile_issue(tmp_path, settings)
    assert issue is not None and issue.code == "profile-mismatch"
