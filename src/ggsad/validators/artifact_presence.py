"""Required Class M artifact presence check (R-008, E-008)."""

from __future__ import annotations

from pathlib import Path

from ggsad.models.validation import IssueCategory, ValidationIssue

REQUIRED_CLASS_M_ARTIFACTS: tuple[str, ...] = (
    "state.yaml",
    "spec.md",
    "plan.md",
    "tasks.md",
    "evidence.md",
)


def validate_required_artifacts(change_dir: Path) -> list[ValidationIssue]:
    """Report each required Class M artifact missing from `change_dir`, explicitly."""
    issues: list[ValidationIssue] = []

    for name in REQUIRED_CLASS_M_ARTIFACTS:
        path = change_dir / name
        if not path.exists():
            issues.append(
                ValidationIssue(
                    category=IssueCategory.MISSING_ARTIFACT,
                    file=str(change_dir),
                    field=name,
                    reason=f"Required Class M artifact {name!r} is missing.",
                    remediation=f"Create {path}.",
                )
            )

    return issues
