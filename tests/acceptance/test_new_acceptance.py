"""CLI-level acceptance tests for `ggsad new`: E-003 and E-004."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ggsad.application.initialize_project import initialize_project
from ggsad.cli import app
from ggsad.models.state import ChangeState
from ggsad.validators.yaml_loader import load_yaml_file

runner = CliRunner()


def test_e003_create_a_valid_class_m_change(tmp_path: Path) -> None:
    """E-003: given a valid initialized project, `ggsad new` creates
    `specs/CHG-002-example-change/` with all five required artifacts, and
    `state.yaml` identifies Class M, phase `specify`, status `draft`."""
    initialize_project(tmp_path)

    result = runner.invoke(app, ["new", "CHG-002", "example-change", "--target", str(tmp_path)])

    assert result.exit_code == 0

    change_dir = tmp_path / "specs" / "CHG-002-example-change"
    assert change_dir.is_relative_to(tmp_path)
    for name in ("state.yaml", "spec.md", "plan.md", "tasks.md", "evidence.md"):
        assert (change_dir / name).exists(), name

    state = ChangeState.model_validate(load_yaml_file(change_dir / "state.yaml"))
    assert state.change.change_class == "M"
    assert state.flow.phase == "specify"
    assert state.flow.status == "draft"


def test_e004_reject_an_invalid_change_identifier(tmp_path: Path) -> None:
    """E-004: an invalid change ID fails with a non-zero exit code, the
    message identifies the invalid identifier, and no files are created
    outside or inside the intended change directory."""
    initialize_project(tmp_path)

    result = runner.invoke(app, ["new", "change/../../002", "example", "--target", str(tmp_path)])

    assert result.exit_code != 0
    assert "change/../../002" in result.output
    assert not (tmp_path / "specs").exists()
    # Nothing escaped upward out of the target either.
    assert not (tmp_path.parent / "002").exists()
    assert not (tmp_path.parent / "escape").exists()
