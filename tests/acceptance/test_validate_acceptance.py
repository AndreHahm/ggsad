"""CLI-level acceptance tests for `ggsad validate`: E-005, E-006, E-008, E-013."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ggsad.application.create_change import build_change_manifest
from ggsad.application.initialize_project import initialize_project
from ggsad.application.manifest_writer import write_manifest
from ggsad.application.validate_repository import discover_change_directories, validate_change
from ggsad.cli import app

runner = CliRunner()
REPO_ROOT = Path(__file__).resolve().parents[2]


def test_validate_on_freshly_initialized_project_passes(tmp_path: Path) -> None:
    initialize_project(tmp_path)

    result = runner.invoke(app, ["validate", str(tmp_path)])

    assert result.exit_code == 0
    assert "OK" in result.output


def test_e005_invalid_config_yaml_fails_with_actionable_message(tmp_path: Path) -> None:
    initialize_project(tmp_path)
    (tmp_path / ".ggsad" / "config.yaml").write_text("project: [unterminated\n", encoding="utf-8")

    result = runner.invoke(app, ["validate", str(tmp_path)])

    assert result.exit_code != 0
    assert "config.yaml" in result.output
    assert "Traceback" not in result.output


def test_e006_unknown_compliance_profile_fails(tmp_path: Path) -> None:
    initialize_project(tmp_path)
    config_path = tmp_path / ".ggsad" / "config.yaml"
    config_path.write_text(
        config_path.read_text(encoding="utf-8").replace("standard", "not-a-real-profile"),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(tmp_path)])

    assert result.exit_code != 0
    assert "not-a-real-profile" in result.output


def test_e008_missing_plan_is_identified_by_change_and_file(tmp_path: Path) -> None:
    initialize_project(tmp_path)
    manifest = build_change_manifest(
        tmp_path, change_id="CHG-002", slug="example-change", title="Example", goal="Ship it"
    )
    write_manifest(manifest)
    change_dir = tmp_path / "specs" / "CHG-002-example-change"
    (change_dir / "plan.md").unlink()

    result = runner.invoke(app, ["validate", str(tmp_path)])

    assert result.exit_code != 0
    assert "CHG-002-example-change" in result.output
    assert "plan.md" in result.output


def test_e013_the_complete_class_m_example_passes_validation() -> None:
    """E-013: the repository's Class M example passes all structural and schema
    checks, and is clearly marked as an example rather than active project state."""
    # Marked as an example, not active state: `specs/examples/class-m/` lives one
    # level deeper than real changes, so `--change CHG-000` finds no match, and it
    # is never picked up by the default (no --change) scan either.
    result = runner.invoke(app, ["validate", str(REPO_ROOT), "--change", "CHG-000"])
    assert result.exit_code != 0  # confirms CHG-000 is not an active change directory

    example_dir = REPO_ROOT / "specs" / "examples" / "class-m"
    assert example_dir not in discover_change_directories(REPO_ROOT)

    # The example itself is validated directly -- this is the actual R-018/E-013 check.
    issues = validate_change(REPO_ROOT, example_dir)
    assert issues == []


def test_json_format_produces_parseable_structured_issues(tmp_path: Path) -> None:
    initialize_project(tmp_path)
    config_path = tmp_path / ".ggsad" / "config.yaml"
    config_path.write_text(
        config_path.read_text(encoding="utf-8").replace("standard", "not-a-real-profile"),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(tmp_path), "--format", "json"])

    assert result.exit_code != 0
    payload = json.loads(result.output)
    assert payload["operation"] == "validate"
    assert payload["result"] == "rejected"
    assert payload["changed"] is False
    assert payload["issues"][0]["code"] == "unknown_profile"


def test_invalid_format_value_is_rejected(tmp_path: Path) -> None:
    initialize_project(tmp_path)

    result = runner.invoke(app, ["validate", str(tmp_path), "--format", "xml"])

    assert result.exit_code != 0
    assert "xml" in result.output


def test_change_filter_scopes_output_to_that_change(tmp_path: Path) -> None:
    initialize_project(tmp_path)
    for change_id, slug in (("CHG-002", "example-change"), ("CHG-003", "another-change")):
        manifest = build_change_manifest(
            tmp_path, change_id=change_id, slug=slug, title="Example", goal="Ship it"
        )
        write_manifest(manifest)
    change_002 = tmp_path / "specs" / "CHG-002-example-change"
    # ggsad new copies the raw templates verbatim -- fill CHG-002 in so this
    # test isolates the --change filter, not the (expected) placeholder finding.
    (change_002 / "spec.md").write_text("# Spec\n\nFilled in.\n", encoding="utf-8")
    (change_002 / "plan.md").write_text("# Plan\n\nFilled in.\n", encoding="utf-8")
    (tmp_path / "specs" / "CHG-003-another-change" / "evidence.md").unlink()

    result = runner.invoke(app, ["validate", str(tmp_path), "--change", "CHG-002"])

    assert result.exit_code == 0
    assert "CHG-003" not in result.output
