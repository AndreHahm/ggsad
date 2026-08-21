"""Unit tests for the ggsad CLI entry point."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ggsad import __version__
from ggsad.application.initialize_project import build_asset_manifest
from ggsad.cli import app

runner = CliRunner()


def _last_envelope(output: str) -> dict[str, object]:
    line = next(line for line in reversed(output.splitlines()) if line.startswith("Result: "))
    return json.loads(line.removeprefix("Result: "))


def test_help_exits_zero_and_lists_usage() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage" in result.output


def test_version_flag_prints_version_and_exits_zero() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_bare_invocation_exits_zero() -> None:
    result = runner.invoke(app, [])

    assert result.exit_code == 0


def test_init_second_run_reports_unchanged_files(tmp_path: Path) -> None:
    runner.invoke(app, ["init", str(tmp_path)])

    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code == 0
    assert "unchanged:" in result.output
    assert _last_envelope(result.output) == {
        "changed": False,
        "data": {"message": f"GG-SAD project initialized at {tmp_path.resolve()}"},
        "operation": "initialize",
        "result": "success",
    }


def test_new_without_goal_returns_rejected_envelope(tmp_path: Path) -> None:
    runner.invoke(app, ["init", str(tmp_path)])

    result = runner.invoke(app, ["new", "CHG-002", "example-change", "--target", str(tmp_path)])

    assert result.exit_code == 1
    envelope = _last_envelope(result.output)
    assert envelope["operation"] == "create_change"
    assert envelope["result"] == "rejected"
    assert envelope["changed"] is False


def test_init_conflict_output_also_lists_unchanged_files(tmp_path: Path) -> None:
    manifest = build_asset_manifest(tmp_path)
    config_path = tmp_path / ".ggsad" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_bytes(manifest[config_path])  # matches -> unchanged
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "constitution.md").write_bytes(b"conflicting content\n")  # -> conflict

    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code != 0
    assert "conflict:" in result.output
    assert "unchanged:" in result.output


def test_new_second_run_on_same_change_id_is_rejected_deterministically(tmp_path: Path) -> None:
    """Unlike `init`, `new` is not idempotent, and this must not depend on
    timing: `state.yaml`'s creation timestamp has second precision, so two
    `new` calls within the same second would render byte-identical content
    -- relying on byte comparison here would make rejection racy. The
    change directory's mere existence is checked instead, deterministically."""
    runner.invoke(app, ["init", str(tmp_path)])
    runner.invoke(
        app, ["new", "CHG-002", "example-change", "--goal", "Ship it", "--target", str(tmp_path)]
    )
    original_state = (tmp_path / "specs" / "CHG-002-example-change" / "state.yaml").read_bytes()

    result = runner.invoke(
        app, ["new", "CHG-002", "example-change", "--goal", "Ship it", "--target", str(tmp_path)]
    )

    assert result.exit_code != 0
    assert "already exists" in result.output
    assert (
        tmp_path / "specs" / "CHG-002-example-change" / "state.yaml"
    ).read_bytes() == original_state


def test_new_rejects_existing_change_directory_and_writes_nothing(tmp_path: Path) -> None:
    runner.invoke(app, ["init", str(tmp_path)])
    change_dir = tmp_path / "specs" / "CHG-002-example-change"
    change_dir.mkdir(parents=True)
    (change_dir / "spec.md").write_bytes(b"pre-existing, unrelated content\n")

    result = runner.invoke(
        app, ["new", "CHG-002", "example-change", "--goal", "Ship it", "--target", str(tmp_path)]
    )

    assert result.exit_code != 0
    assert "already exists" in result.output
    assert not (change_dir / "state.yaml").exists()
    assert (change_dir / "spec.md").read_bytes() == b"pre-existing, unrelated content\n"
