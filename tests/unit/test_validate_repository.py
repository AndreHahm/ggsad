"""Unit tests for repository-level validation aggregation (R-005 through R-009)."""

from __future__ import annotations

from pathlib import Path

from ggsad.application.create_change import build_change_manifest
from ggsad.application.initialize_project import initialize_project
from ggsad.application.manifest_writer import write_manifest
from ggsad.application.validate_repository import (
    _validate_declared_mappings,
    discover_change_directories,
    validate_change,
    validate_project_config,
    validate_repository,
)
from ggsad.models.config import IntegrationDeclaration, ProjectConfig
from ggsad.models.validation import IssueCategory
from ggsad.validators.yaml_loader import dump_yaml_bytes, load_yaml_file


def _init(tmp_path: Path) -> Path:
    initialize_project(tmp_path)
    return tmp_path


def _new_change(target: Path, change_id: str = "CHG-002", slug: str = "example-change") -> Path:
    manifest = build_change_manifest(
        target, change_id=change_id, slug=slug, title="Example", goal="Ship it"
    )
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


def _declare_mapping(target: Path, mapping: str) -> None:
    """Declare one `gsd` integration with an arbitrary (possibly malicious)
    mapping path, via the YAML round-trip API rather than string
    substitution -- the path values under test contain backslashes that
    Python `repr()`/naive string formatting would encode incorrectly for
    YAML's single-quote (no-escaping) scalar style."""
    config_path = target / ".ggsad" / "config.yaml"
    data = load_yaml_file(config_path)
    data["project"]["operating_mode"] = "combination"
    data["integrations"] = [{"id": "gsd", "mode": "companion", "mapping": mapping}]
    config_path.write_bytes(dump_yaml_bytes(data))


def test_prf004_schema_rejects_windows_drive_absolute_mapping_path(tmp_path: Path) -> None:
    """PRF-004: a drive-absolute path must fail schema validation, not be
    silently accepted and later resolved outside the repository."""
    target = _init(tmp_path)
    _declare_mapping(target, "C:\\outside.yaml")

    issues = validate_project_config(target)

    assert issues
    assert all(issue.category is IssueCategory.SCHEMA_VIOLATION for issue in issues)


def test_prf004_schema_rejects_unc_mapping_path(tmp_path: Path) -> None:
    target = _init(tmp_path)
    _declare_mapping(target, "\\\\server\\share\\mapping.yaml")

    issues = validate_project_config(target)

    assert issues
    assert all(issue.category is IssueCategory.SCHEMA_VIOLATION for issue in issues)


def test_prf004_schema_rejects_backslash_traversal_mapping_path(tmp_path: Path) -> None:
    target = _init(tmp_path)
    _declare_mapping(target, "..\\outside.yaml")

    issues = validate_project_config(target)

    assert issues
    assert all(issue.category is IssueCategory.SCHEMA_VIOLATION for issue in issues)


def test_prf004_declared_mapping_escaping_target_is_rejected_as_path_safety(
    tmp_path: Path,
) -> None:
    """Defense in depth (PRF-004): `_validate_declared_mappings` verifies path
    containment explicitly rather than trusting the schema pattern alone --
    `Path`'s `/` operator silently discards the left-hand side if the
    right-hand side turns out to be absolute. Constructed directly against an
    in-memory `ProjectConfig`, bypassing the schema layer, to prove the
    code-level guard rejects an escaping path independently."""
    target = _init(tmp_path)
    data = load_yaml_file(target / ".ggsad" / "config.yaml")
    config = ProjectConfig.model_validate(data)
    escaping_config = config.model_copy(
        update={
            "integrations": [
                IntegrationDeclaration(id="gsd", mode="companion", mapping="../../outside.yaml")
            ]
        }
    )

    issues = _validate_declared_mappings(target, escaping_config)

    assert len(issues) == 1
    assert issues[0].category is IssueCategory.PATH_SAFETY


def test_prf005_schema_rejects_unsupported_config_schema_version(tmp_path: Path) -> None:
    """PRF-005: only schema_version '0.1' is currently supported."""
    target = _init(tmp_path)
    config_path = target / ".ggsad" / "config.yaml"
    data = load_yaml_file(config_path)
    data["schema_version"] = "99.9"
    config_path.write_bytes(dump_yaml_bytes(data))

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


def test_missing_conditional_plan_is_allowed_when_state_does_not_reference_it(
    tmp_path: Path,
) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    (change_dir / "plan.md").unlink()
    state_path = change_dir / "state.yaml"
    state = load_yaml_file(state_path)
    state["artifacts"]["plan"] = None
    state_path.write_bytes(dump_yaml_bytes(state))

    issues = validate_change(target, change_dir)

    assert not any(issue.field == "plan.md" for issue in issues)


def test_missing_state_declared_artifact_is_reported(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    (change_dir / "evidence.md").unlink()

    issues = validate_change(target, change_dir)

    assert any(
        issue.category is IssueCategory.MISSING_ARTIFACT and issue.field == "artifacts/evidence"
        for issue in issues
    )


def test_state_declared_artifact_must_stay_within_change_directory(tmp_path: Path) -> None:
    target = _init(tmp_path)
    change_dir = _new_change(target)
    state_path = change_dir / "state.yaml"
    state = load_yaml_file(state_path)
    state["artifacts"]["spec"] = "../../outside.md"
    state_path.write_bytes(dump_yaml_bytes(state))

    issues = validate_change(target, change_dir)

    assert any(
        issue.category is IssueCategory.PATH_SAFETY and issue.field == "artifacts/spec"
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

    assert any(issue.field == "artifacts/evidence" for issue in issues)


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
