"""Unit tests for repository-level validation aggregation (R-005 through R-009)."""

from __future__ import annotations

from pathlib import Path

from ggsad.application.create_change import build_change_manifest
from ggsad.application.initialize_project import initialize_project
from ggsad.application.manifest_writer import write_manifest
from ggsad.application.validate_repository import (
    discover_change_directories,
    validate_change,
    validate_project_config,
    validate_repository,
)
from ggsad.models.validation import IssueCategory


def _init(tmp_path: Path) -> Path:
    initialize_project(tmp_path)
    return tmp_path


def _new_change(target: Path, change_id: str = "CHG-002", slug: str = "example-change") -> Path:
    manifest = build_change_manifest(target, change_id=change_id, slug=slug, title="Example")
    write_manifest(manifest)
    return target / "specs" / f"{change_id}-{slug}"


# --- project config validation -----------------------------------------------------


def test_freshly_initialized_project_config_has_no_issues(tmp_path: Path) -> None:
    target = _init(tmp_path)

    assert validate_project_config(target) == []


def test_missing_config_is_reported(tmp_path: Path) -> None:
    issues = validate_project_config(tmp_path)  # never initialized

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.MISSING_ARTIFACT


def test_invalid_yaml_config_is_reported_as_yaml_syntax(tmp_path: Path) -> None:
    target = _init(tmp_path)
    config_path = target / ".ggsad" / "config.yaml"
    config_path.write_text("project: [unterminated\n", encoding="utf-8")

    issues = validate_project_config(target)

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.YAML_SYNTAX


def test_schema_invalid_config_is_reported_as_schema_violation(tmp_path: Path) -> None:
    target = _init(tmp_path)
    config_path = target / ".ggsad" / "config.yaml"
    config_path.write_text("schema_version: '0.1'\n", encoding="utf-8")  # missing required keys

    issues = validate_project_config(target)

    assert issues
    assert all(issue.category is IssueCategory.SCHEMA_VIOLATION for issue in issues)


def test_e006_unknown_compliance_profile_fails_validation(tmp_path: Path) -> None:
    target = _init(tmp_path)
    config_path = target / ".ggsad" / "config.yaml"
    content = config_path.read_text(encoding="utf-8")
    config_path.write_text(content.replace("standard", "not-a-real-profile"), encoding="utf-8")

    issues = validate_project_config(target)

    assert any(issue.category is IssueCategory.UNKNOWN_PROFILE for issue in issues)


def test_missing_config_schema_file_is_reported(tmp_path: Path) -> None:
    target = _init(tmp_path)
    (target / ".ggsad" / "schemas" / "config.schema.json").unlink()

    issues = validate_project_config(target)

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.MISSING_ARTIFACT
    assert "config.schema.json" in issues[0].file


def test_declared_mapping_with_schema_violation_skips_authority_check(tmp_path: Path) -> None:
    """A structurally invalid mapping is reported once (schema violation) and
    the authority check (which needs a valid, typed mapping) is skipped rather
    than raising on malformed data."""
    target = _init(tmp_path)
    config_path = target / ".ggsad" / "config.yaml"
    content = config_path.read_text(encoding="utf-8")
    content = content.replace("operating_mode: stand-alone", "operating_mode: combination")
    content = content.replace(
        "integrations: []",
        "integrations:\n- id: gsd\n  mode: companion\n  mapping: .ggsad/mappings/gsd.yaml\n",
    )
    config_path.write_text(content, encoding="utf-8")
    mapping_path = target / ".ggsad" / "mappings" / "gsd.yaml"
    mapping_path.parent.mkdir(parents=True)
    mapping_path.write_text("integration:\n  id: gsd\n", encoding="utf-8")  # missing required keys

    issues = validate_project_config(target)

    assert issues
    assert all(issue.category is IssueCategory.SCHEMA_VIOLATION for issue in issues)


# --- change discovery and per-change validation -------------------------------------


def test_discover_change_directories_finds_real_changes_only(tmp_path: Path) -> None:
    target = _init(tmp_path)
    _new_change(target, "CHG-002", "example-change")
    _new_change(target, "CHG-003", "another-change")
    # Simulate the packaged example living alongside real changes.
    (target / "specs" / "examples" / "class-m").mkdir(parents=True)

    found = discover_change_directories(target)

    assert {p.name for p in found} == {"CHG-002-example-change", "CHG-003-another-change"}


def _fill_in_spec_and_plan(change_dir: Path) -> None:
    """Overwrite spec.md/plan.md with placeholder-free content.

    `ggsad new` copies the raw templates verbatim (by design -- the user
    fills them in), so they legitimately still contain unresolved
    placeholders right after creation. Tests that want to isolate a
    *different* concern use this to get a "filled in" change first.
    """
    (change_dir / "spec.md").write_text("# Example Spec\n\nNo placeholders here.\n", "utf-8")
    (change_dir / "plan.md").write_text("# Example Plan\n\nNo placeholders here.\n", "utf-8")


def test_freshly_created_change_still_has_unresolved_placeholders(tmp_path: Path) -> None:
    """A raw `ggsad new` change hasn't been filled in yet, so R-009 correctly
    flags it -- this is the intended, not-yet-ready state, matching R-011's
    "no unresolved placeholders" transition precondition."""
    target = _init(tmp_path)
    change_dir = _new_change(target)

    issues = validate_change(target, change_dir)

    assert any(issue.category is IssueCategory.UNRESOLVED_PLACEHOLDER for issue in issues)


def test_validate_change_on_filled_in_change_has_no_issues(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    _fill_in_spec_and_plan(change_dir)

    assert validate_change(target, change_dir) == []


def test_e008_missing_plan_is_reported(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    (change_dir / "plan.md").unlink()

    issues = validate_change(target, change_dir)

    assert any(
        issue.category is IssueCategory.MISSING_ARTIFACT and issue.field == "plan.md"
        for issue in issues
    )


def test_unresolved_placeholder_in_spec_is_reported(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    _fill_in_spec_and_plan(change_dir)
    (change_dir / "spec.md").write_text("- Approver: <name-or-role>\n", encoding="utf-8")

    issues = validate_change(target, change_dir)

    assert any(issue.category is IssueCategory.UNRESOLVED_PLACEHOLDER for issue in issues)


def test_placeholder_check_does_not_apply_to_tasks_or_evidence(tmp_path: Path) -> None:
    """Deliberately scoped to spec.md/plan.md only, mirroring R-011's exact wording."""
    target = _init(tmp_path)
    change_dir = _new_change(target)
    _fill_in_spec_and_plan(change_dir)
    (change_dir / "tasks.md").write_text("- Owner: <name-or-role>\n", encoding="utf-8")

    issues = validate_change(target, change_dir)

    assert not any(issue.category is IssueCategory.UNRESOLVED_PLACEHOLDER for issue in issues)


# --- top-level orchestration ---------------------------------------------------------


def test_validate_repository_with_no_changes_reports_only_config_issues(tmp_path: Path) -> None:
    target = _init(tmp_path)

    assert validate_repository(target) == []


def test_validate_repository_scans_all_changes_by_default(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    (change_dir / "evidence.md").unlink()
    _new_change(target, "CHG-003", "another-change")

    issues = validate_repository(target)

    assert any(issue.field == "evidence.md" for issue in issues)


def test_validate_repository_with_change_filter_scopes_to_that_change(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target, "CHG-002", "example-change")
    (change_dir / "evidence.md").unlink()
    _new_change(target, "CHG-003", "another-change")  # untouched, would also be flagged if scanned

    issues = validate_repository(target, change_id="CHG-002")

    assert any("CHG-002" in issue.file for issue in issues)
    assert not any("CHG-003" in issue.file for issue in issues)


def test_validate_repository_reports_missing_change_id(tmp_path: Path) -> None:
    target = _init(tmp_path)

    issues = validate_repository(target, change_id="CHG-999")

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.MISSING_ARTIFACT
    assert "CHG-999" in issues[0].reason
