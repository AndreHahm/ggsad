"""CLI-level acceptance tests for `ggsad transition`: E-009, E-010, E-011."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ggsad.application.create_change import build_change_manifest
from ggsad.application.initialize_project import initialize_project
from ggsad.application.manifest_writer import write_manifest
from ggsad.cli import app
from ggsad.validators.yaml_loader import load_yaml_file

runner = CliRunner()


def _new_change(target: Path, change_id: str = "CHG-002", slug: str = "example-change") -> Path:
    manifest = build_change_manifest(
        target, change_id=change_id, slug=slug, title="Example", goal="Ship it"
    )
    write_manifest(manifest)
    return target / "specs" / f"{change_id}-{slug}"


def test_e009_unresolved_placeholder_rejects_transition_and_preserves_state(
    tmp_path: Path,
) -> None:
    """E-009: a Class M spec.md with an unresolved placeholder rejects the
    draft -> ready transition, state.yaml stays unchanged, and the output
    identifies the placeholder and file."""
    initialize_project(tmp_path)
    change_dir = _new_change(tmp_path)
    original_state = (change_dir / "state.yaml").read_bytes()

    result = runner.invoke(app, ["transition", "CHG-002", "ready", "--target", str(tmp_path)])

    assert result.exit_code != 0
    assert "placeholder" in result.output.lower()
    assert "spec.md" in result.output
    assert (change_dir / "state.yaml").read_bytes() == original_state


def test_e010_valid_transition_succeeds(tmp_path: Path) -> None:
    """E-010: a valid, fully-satisfied change transitions to ready, state.yaml
    is updated, and a history event is appended."""
    initialize_project(tmp_path)
    change_dir = _new_change(tmp_path)
    (change_dir / "spec.md").write_text("# Spec\n\nFilled in.\n", encoding="utf-8")
    (change_dir / "plan.md").write_text("# Plan\n\nFilled in.\n", encoding="utf-8")

    result = runner.invoke(
        app,
        ["transition", "CHG-002", "ready", "--actor", "human:test", "--target", str(tmp_path)],
    )

    assert result.exit_code == 0
    assert "ready" in result.output

    data = load_yaml_file(change_dir / "state.yaml")
    assert data["flow"]["status"] == "ready"
    assert data["flow"]["phase"] == "specify"
    assert data["history"][-1]["actor"] == "human:test"


def test_e011_reject_unsupported_transition(tmp_path: Path) -> None:
    """E-011: transitioning an already-ready change is rejected, the original
    state file remains unchanged, and the output states the source state is
    unsupported."""
    initialize_project(tmp_path)
    change_dir = _new_change(tmp_path)
    (change_dir / "spec.md").write_text("# Spec\n\nFilled in.\n", encoding="utf-8")
    (change_dir / "plan.md").write_text("# Plan\n\nFilled in.\n", encoding="utf-8")

    first = runner.invoke(app, ["transition", "CHG-002", "ready", "--target", str(tmp_path)])
    assert first.exit_code == 0
    ready_bytes = (change_dir / "state.yaml").read_bytes()

    second = runner.invoke(app, ["transition", "CHG-002", "ready", "--target", str(tmp_path)])

    assert second.exit_code != 0
    assert "unsupported" in second.output.lower()
    assert (change_dir / "state.yaml").read_bytes() == ready_bytes


def test_transition_rejects_a_target_status_other_than_ready(tmp_path: Path) -> None:
    """R-010: not a general status editor -- only 'ready' is accepted at all."""
    initialize_project(tmp_path)
    _new_change(tmp_path)

    result = runner.invoke(app, ["transition", "CHG-002", "done", "--target", str(tmp_path)])

    assert result.exit_code != 0
    assert "done" in result.output


def test_transition_missing_change_id_is_rejected(tmp_path: Path) -> None:
    initialize_project(tmp_path)

    result = runner.invoke(app, ["transition", "CHG-999", "ready", "--target", str(tmp_path)])

    assert result.exit_code != 0
    assert "CHG-999" in result.output
