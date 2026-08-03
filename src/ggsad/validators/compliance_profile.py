"""Compliance-profile identity check (R-005, E-006).

`config.schema.json`'s `compliance_profile` field only constrains the
*shape* of the string (`^[a-z][a-z0-9_-]*$`); it can't know whether the
profile actually exists. CHG-001 explicitly excludes the full profile
resolver (R4 in the roadmap) and doesn't ship default profile file content
(`.ggsad/profiles/` is deliberately empty -- see `initialize_project.py`),
so this check is intentionally minimal: a profile is accepted if it is one
of the four named throughout the project's own docs, or if a corresponding
custom profile file exists under `.ggsad/profiles/`.
"""

from __future__ import annotations

from pathlib import Path

from ggsad.models.config import ProjectConfig
from ggsad.models.validation import IssueCategory, ValidationIssue

KNOWN_BUILTIN_PROFILES = frozenset({"lean", "standard", "governed", "regulated"})


def validate_compliance_profile(
    config: ProjectConfig, target: Path, *, file_label: str
) -> list[ValidationIssue]:
    """Reject a compliance profile that is neither built-in nor a known custom profile file."""
    profile = config.project.compliance_profile
    if profile in KNOWN_BUILTIN_PROFILES:
        return []

    custom_profile_path = target / ".ggsad" / "profiles" / f"{profile}.yaml"
    if custom_profile_path.exists():
        return []

    return [
        ValidationIssue(
            category=IssueCategory.UNKNOWN_PROFILE,
            file=file_label,
            field="project/compliance_profile",
            reason=(
                f"Unknown compliance profile {profile!r}: not one of the built-in profiles "
                f"({', '.join(sorted(KNOWN_BUILTIN_PROFILES))}), and no custom profile file "
                f"found at {custom_profile_path}."
            ),
            remediation=(
                f"Use a built-in profile, or add {custom_profile_path} as an approved "
                "custom profile."
            ),
        )
    ]
