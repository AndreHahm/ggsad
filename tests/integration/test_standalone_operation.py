"""Stand-alone operation verification (R-016).

Confirms the core Python modules under `src/ggsad/` don't import GSD,
Claude Code, GitHub, an IDE, CI, or an issue-tracker SDK, and that a full
init -> new -> validate workflow succeeds against a stand-alone
(`operating_mode: stand-alone`, no integrations) project.
"""

from __future__ import annotations

import ast
import tomllib
from pathlib import Path

from typer.testing import CliRunner

from ggsad.application.create_change import build_change_manifest
from ggsad.application.manifest_writer import write_manifest
from ggsad.cli import app
from ggsad.validators.yaml_loader import load_yaml_file

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "ggsad"

_FORBIDDEN_IMPORT_SUBSTRINGS = (
    "gsd",
    "claude",
    "github",
    "gitlab",
    "jira",
    "linear",
)

runner = CliRunner()


def _imported_module_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_no_source_module_imports_a_forbidden_integration_sdk() -> None:
    offending: list[str] = []
    for path in SRC_ROOT.rglob("*.py"):
        for name in _imported_module_names(path):
            lowered = name.lower()
            if any(forbidden in lowered for forbidden in _FORBIDDEN_IMPORT_SUBSTRINGS):
                offending.append(f"{path.relative_to(REPO_ROOT)}: import {name}")

    assert offending == []


def test_declared_dependencies_contain_no_forbidden_integration_package() -> None:
    """Checks only the actual declared dependency lists, not the whole file --
    pyproject.toml legitimately mentions '.claude'/'.github' as ruff
    `extend-exclude` paths, which is unrelated to runtime dependencies."""
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    declared = list(pyproject["project"]["dependencies"])
    declared += pyproject["dependency-groups"]["dev"]

    for package in declared:
        lowered = package.lower()
        for forbidden in _FORBIDDEN_IMPORT_SUBSTRINGS:
            assert forbidden not in lowered, f"{package!r} looks like a forbidden dependency"


def test_full_workflow_succeeds_stand_alone_with_no_integrations(tmp_path: Path) -> None:
    """E-012 (partial -- transition lands in Slice 6): init and validate succeed
    with zero active integrations, and change creation succeeds too, confirming
    R-016 end to end. `validate` is checked right after `init` (not after `new`):
    a freshly created change's spec.md/plan.md are raw, unfilled templates by
    design (R-009 correctly flags that separately -- see test_validate_repository.py),
    which is orthogonal to whether the stand-alone workflow itself works."""
    init_result = runner.invoke(app, ["init", str(tmp_path)])
    assert init_result.exit_code == 0

    config = load_yaml_file(tmp_path / ".ggsad" / "config.yaml")
    assert config["project"]["operating_mode"] == "stand-alone"
    assert config["integrations"] == []

    validate_result = runner.invoke(app, ["validate", str(tmp_path)])
    assert validate_result.exit_code == 0

    manifest = build_change_manifest(
        tmp_path, change_id="CHG-002", slug="example-change", title="Example"
    )
    write_result = write_manifest(manifest)
    assert write_result.ok
