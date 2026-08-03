"""Unit tests for project initialization (R-001, R-002, R-012)."""

from __future__ import annotations

from pathlib import Path

from ggsad.application.initialize_project import (
    build_asset_manifest,
    initialize_project,
    preflight,
    slugify_project_id,
)
from ggsad.models.config import ProjectConfig
from ggsad.validators.schema_validator import load_schema, validate_against_schema
from ggsad.validators.yaml_loader import load_yaml_text

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_slugify_project_id_lowercases_and_hyphenates() -> None:
    assert slugify_project_id("My Cool Project") == "my-cool-project"


def test_slugify_project_id_strips_leading_trailing_invalid_chars() -> None:
    assert slugify_project_id("--Foo_Bar--") == "foo-bar"


def test_slugify_project_id_falls_back_when_nothing_valid_remains() -> None:
    assert slugify_project_id("___") == "ggsad-project"


def test_manifest_contains_expected_file_counts(tmp_path: Path) -> None:
    manifest = build_asset_manifest(tmp_path)

    ggsad_config = [p for p in manifest if p == (tmp_path / ".ggsad" / "config.yaml")]
    schemas = [p for p in manifest if p.parent == tmp_path / ".ggsad" / "schemas"]
    templates = [p for p in manifest if p.parent == tmp_path / ".ggsad" / "templates"]
    docs = [p for p in manifest if p.parent == tmp_path / "docs"]

    assert len(ggsad_config) == 1
    assert len(schemas) == 3
    assert len(templates) == 10
    assert {p.name for p in docs} == {
        "constitution.md",
        "project-brief.md",
        "architecture.md",
        "roadmap.md",
    }


def test_generated_config_yaml_is_schema_valid(tmp_path: Path) -> None:
    manifest = build_asset_manifest(tmp_path)
    content = manifest[tmp_path / ".ggsad" / "config.yaml"].decode("utf-8")

    data = load_yaml_text(content)
    schema = load_schema(REPO_ROOT / ".ggsad" / "schemas" / "config.schema.json")

    assert validate_against_schema(data=data, schema=schema, file_label="config.yaml") == []

    config = ProjectConfig.model_validate(data)
    assert config.project.operating_mode == "stand-alone"
    assert config.integrations == []


def test_generated_config_yaml_uses_slugified_target_dirname(tmp_path: Path) -> None:
    project_dir = tmp_path / "My Project"
    project_dir.mkdir()

    manifest = build_asset_manifest(project_dir)
    data = load_yaml_text(manifest[project_dir / ".ggsad" / "config.yaml"].decode("utf-8"))

    assert data["project"]["id"] == "my-project"


def test_preflight_on_empty_directory_marks_everything_to_create(tmp_path: Path) -> None:
    manifest = build_asset_manifest(tmp_path)

    result = preflight(manifest)

    assert set(result.to_create) == set(manifest)
    assert result.unchanged == ()
    assert result.conflicts == ()


def test_preflight_detects_identical_existing_file_as_unchanged(tmp_path: Path) -> None:
    manifest = build_asset_manifest(tmp_path)
    config_path = tmp_path / ".ggsad" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_bytes(manifest[config_path])

    result = preflight(manifest)

    assert config_path in result.unchanged
    assert config_path not in result.to_create
    assert result.conflicts == ()


def test_preflight_detects_modified_existing_file_as_conflict(tmp_path: Path) -> None:
    manifest = build_asset_manifest(tmp_path)
    config_path = tmp_path / ".ggsad" / "config.yaml"
    config_path.parent.mkdir(parents=True)
    config_path.write_bytes(b"schema_version: modified-by-someone-else\n")

    result = preflight(manifest)

    assert config_path in result.conflicts


def test_initialize_project_on_empty_directory_creates_everything(tmp_path: Path) -> None:
    result = initialize_project(tmp_path)

    assert result.ok
    assert result.conflicts == ()
    assert len(result.created) > 0
    for path in result.created:
        assert path.exists()


def test_initialize_project_is_idempotent_on_second_run(tmp_path: Path) -> None:
    first = initialize_project(tmp_path)
    second = initialize_project(tmp_path)

    assert first.ok
    assert second.ok
    assert second.created == ()
    assert set(second.unchanged) == set(first.created)


def test_initialize_project_rejects_conflicting_docs_and_writes_nothing_else(
    tmp_path: Path,
) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    modified = b"# Not the template content\n"
    (docs_dir / "constitution.md").write_bytes(modified)

    result = initialize_project(tmp_path)

    assert not result.ok
    assert (tmp_path / "docs" / "constitution.md") in result.conflicts
    assert (docs_dir / "constitution.md").read_bytes() == modified

    # R-012: a conflict anywhere must prevent every other write, not just the
    # conflicting file.
    assert not (tmp_path / ".ggsad" / "config.yaml").exists()
    assert not (tmp_path / ".ggsad" / "schemas").exists()
