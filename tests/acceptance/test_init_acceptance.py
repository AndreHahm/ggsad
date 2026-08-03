"""CLI-level acceptance tests for `ggsad init`: E-001 and E-002."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ggsad.cli import app

runner = CliRunner()


def test_e001_initialize_a_clean_repository(tmp_path: Path) -> None:
    """E-001: an empty writable target directory is initialized successfully,
    and the approved GG-SAD directories and baseline files are created."""
    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / ".ggsad" / "config.yaml").exists()
    assert (tmp_path / ".ggsad" / "schemas" / "config.schema.json").exists()
    assert (tmp_path / ".ggsad" / "templates" / "spec.template.md").exists()
    assert (tmp_path / "docs" / "constitution.md").exists()
    assert "created:" in result.output


def test_e002_reject_unsafe_reinitialization(tmp_path: Path) -> None:
    """E-002: a target directory with an existing, modified `docs/constitution.md`
    causes `init` to fail with an actionable conflict message, leaves that file
    byte-for-byte unchanged, and removes no unrelated file."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    modified_content = b"# My modified constitution\n\nDo not overwrite this.\n"
    (docs_dir / "constitution.md").write_bytes(modified_content)
    sentinel = tmp_path / "unrelated-user-file.txt"
    sentinel.write_text("keep me\n", encoding="utf-8")

    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code != 0
    assert "conflict" in result.output.lower()
    assert (docs_dir / "constitution.md").read_bytes() == modified_content
    assert sentinel.exists()
    assert sentinel.read_text(encoding="utf-8") == "keep me\n"
    assert not (tmp_path / ".ggsad").exists()
