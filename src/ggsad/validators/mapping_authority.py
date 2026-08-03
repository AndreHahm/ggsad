"""Companion mapping authority checks (R-006, R-017).

A JSON Schema can confirm that `permissions.may_approve` etc. are booleans,
but not that they are `false` -- that a companion integration (e.g. GSD) may
never approve, directly transition, or close GG-SAD work is a GG-SAD
business invariant, not a structural constraint. This module checks it.
"""

from __future__ import annotations

from ggsad.models.mapping import IntegrationMapping
from ggsad.models.validation import IssueCategory, ValidationIssue

_FORBIDDEN_PERMISSIONS: tuple[tuple[str, str], ...] = (
    ("may_approve", "approve GG-SAD work"),
    ("may_transition_ggsad_state_directly", "directly transition GG-SAD state"),
    ("may_close_ggsad_change", "close a GG-SAD change"),
)


def validate_mapping_authority(
    mapping: IntegrationMapping, *, file_label: str
) -> list[ValidationIssue]:
    """Verify a companion mapping does not grant forbidden GG-SAD authority.

    Returns one :class:`ValidationIssue` per violated permission (empty list
    if the mapping is compliant).
    """
    issues: list[ValidationIssue] = []
    permissions = mapping.permissions

    for field_name, capability in _FORBIDDEN_PERMISSIONS:
        if getattr(permissions, field_name):
            issues.append(
                ValidationIssue(
                    category=IssueCategory.MAPPING_AUTHORITY,
                    file=file_label,
                    field=f"permissions/{field_name}",
                    reason=(
                        f"The companion '{mapping.integration.id}' may not {capability}; "
                        f"'{field_name}' must be false."
                    ),
                    remediation=f"Set permissions.{field_name}: false.",
                )
            )

    return issues
