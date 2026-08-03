"""Repository-level validation aggregation (R-005 through R-009, R-015).

`validate_repository()` composes:

- project configuration validation: schema (R-005) and compliance profile
  identity (E-006, `validators/compliance_profile.py`);
- every mapping file declared by the config's `integrations` list: schema
  (R-006) and companion authority (R-017, `validators/mapping_authority.py`);
- per-change validation: required Class M artifacts (R-008, E-008,
  `validators/artifact_presence.py`), `state.yaml` schema (R-007), and
  unresolved placeholders in `spec.md`/`plan.md` (R-009) -- deliberately
  scoped to those two files to mirror R-011's transition-precondition
  wording exactly, not the whole change directory (a freshly-`init`ed
  project's `docs/` are expected to still contain placeholders; see
  `initialize_project.py`).

Returns a flat `list[ValidationIssue]`; the CLI layer decides presentation
(text/JSON) and exit code.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from ggsad.models.config import ProjectConfig
from ggsad.models.mapping import IntegrationMapping
from ggsad.models.validation import IssueCategory, ValidationIssue
from ggsad.validators.artifact_presence import validate_required_artifacts
from ggsad.validators.compliance_profile import validate_compliance_profile
from ggsad.validators.mapping_authority import validate_mapping_authority
from ggsad.validators.placeholder_detector import validate_no_unresolved_placeholders
from ggsad.validators.schema_validator import load_schema, validate_against_schema
from ggsad.validators.yaml_loader import YamlLoadError, load_yaml_file

_CHANGE_DIR_PATTERN = re.compile(r"^CHG-\d{3,}-[a-z0-9]+(?:-[a-z0-9]+)*$")
_PLACEHOLDER_CHECKED_ARTIFACTS: tuple[str, ...] = ("spec.md", "plan.md")


def _load_and_schema_validate(
    path: Path, schema_path: Path
) -> tuple[Any | None, list[ValidationIssue]]:
    """Load and schema-validate a governed YAML file.

    Returns `(None, issues)` if the file or its schema is missing, or the
    file isn't parseable; returns `(data, issues)` otherwise, where `issues`
    is the (possibly empty) list of schema violations.
    """
    if not path.exists():
        return None, [
            ValidationIssue(
                category=IssueCategory.MISSING_ARTIFACT,
                file=str(path),
                reason="Required file is missing.",
            )
        ]

    try:
        data = load_yaml_file(path)
    except YamlLoadError as exc:
        return None, [
            ValidationIssue(category=IssueCategory.YAML_SYNTAX, file=str(path), reason=str(exc))
        ]

    if not schema_path.exists():
        return data, [
            ValidationIssue(
                category=IssueCategory.MISSING_ARTIFACT,
                file=str(schema_path),
                reason="Schema file is missing; cannot validate.",
            )
        ]

    schema = load_schema(schema_path)
    issues = validate_against_schema(data=data, schema=schema, file_label=str(path))
    return data, issues


def validate_project_config(target: Path) -> list[ValidationIssue]:
    """Validate `.ggsad/config.yaml`: schema (R-005), profile (E-006), mappings (R-006/R-017)."""
    config_path = target / ".ggsad" / "config.yaml"
    schema_path = target / ".ggsad" / "schemas" / "config.schema.json"
    data, issues = _load_and_schema_validate(config_path, schema_path)
    if data is None or issues:
        return issues

    config = ProjectConfig.model_validate(data)
    issues += validate_compliance_profile(config, target, file_label=str(config_path))
    issues += _validate_declared_mappings(target, config)
    return issues


def _validate_declared_mappings(target: Path, config: ProjectConfig) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    mapping_schema_path = target / ".ggsad" / "schemas" / "mappings.schema.json"

    for integration in config.integrations:
        # `config.schema.json`'s relativePath pattern already forbids absolute,
        # UNC, and traversal paths, but containment is verified explicitly here
        # as defense in depth rather than relying on the regex alone -- Path's
        # `/` operator silently discards `target` if the right-hand side turns
        # out to be an absolute path (e.g. `C:\outside.yaml` on Windows).
        mapping_path = (target / integration.mapping).resolve()
        if not mapping_path.is_relative_to(target):
            issues.append(
                ValidationIssue(
                    category=IssueCategory.PATH_SAFETY,
                    file=integration.mapping,
                    reason=f"Mapping path resolves outside the repository: {mapping_path}",
                    remediation="Use a path within the repository for 'integrations[].mapping'.",
                )
            )
            continue
        data, mapping_issues = _load_and_schema_validate(mapping_path, mapping_schema_path)
        issues += mapping_issues
        if data is None or mapping_issues:
            continue
        mapping = IntegrationMapping.model_validate(data)
        issues += validate_mapping_authority(mapping, file_label=str(mapping_path))

    return issues


def validate_change(target: Path, change_dir: Path) -> list[ValidationIssue]:
    """Validate one change: artifacts (R-008), state schema (R-007), placeholders (R-009)."""
    issues: list[ValidationIssue] = []
    issues += validate_required_artifacts(change_dir)

    state_path = change_dir / "state.yaml"
    if state_path.exists():
        schema_path = target / ".ggsad" / "schemas" / "state.schema.json"
        _, state_issues = _load_and_schema_validate(state_path, schema_path)
        issues += state_issues

    for name in _PLACEHOLDER_CHECKED_ARTIFACTS:
        artifact_path = change_dir / name
        if artifact_path.exists():
            issues += validate_no_unresolved_placeholders(artifact_path)

    return issues


def discover_change_directories(target: Path) -> list[Path]:
    """Find real change directories directly under `target/specs/`.

    Matches `CHG-<digits>-<slug>` only, so `specs/examples/`, which lives
    one level deeper, is never picked up here (R-018: an example must not
    be treated as active project state).
    """
    specs_dir = target / "specs"
    if not specs_dir.is_dir():
        return []
    return sorted(
        p for p in specs_dir.iterdir() if p.is_dir() and _CHANGE_DIR_PATTERN.match(p.name)
    )


def validate_repository(target: Path, *, change_id: str | None = None) -> list[ValidationIssue]:
    """Validate governed GG-SAD artifacts under `target`.

    Always validates project configuration and its declared mappings. If
    `change_id` is given, validates only that change; otherwise validates
    every change directory discovered under `specs/`.
    """
    target = target.resolve()
    issues = validate_project_config(target)

    if change_id is not None:
        change_dirs = [p for p in (target / "specs").glob(f"{change_id}-*") if p.is_dir()]
        if not change_dirs:
            issues.append(
                ValidationIssue(
                    category=IssueCategory.MISSING_ARTIFACT,
                    file=str(target / "specs"),
                    reason=f"No change directory found for change ID {change_id!r}.",
                )
            )
    else:
        change_dirs = discover_change_directories(target)

    for change_dir in change_dirs:
        issues += validate_change(target, change_dir)

    return issues
