"""Unit tests for the companion mapping authority check (R-006, R-017)."""

from __future__ import annotations

from ggsad.models.mapping import IntegrationMapping
from ggsad.validators.mapping_authority import validate_mapping_authority

_BASE: dict = {
    "integration": {"id": "gsd", "mode": "companion"},
    "ownership": {"governance": "ggsad"},
    "sources_of_truth": {"project_context": "docs/project-brief.md"},
    "permissions": {
        "may_modify_approved_specification": False,
        "may_modify_accepted_adr": False,
        "may_transition_ggsad_state_directly": False,
        "may_approve": False,
        "may_close_ggsad_change": False,
    },
    "mappings": [
        {
            "external_artifact": ".planning/STATE.md",
            "ggsad_role": "execution-state",
            "authoritative": False,
        }
    ],
    "failure": {
        "on_mapping_conflict": "wait",
        "on_sync_error": "wait",
        "uninstall_preserves_ggsad_artifacts": True,
    },
}


def test_compliant_mapping_has_no_authority_issues() -> None:
    mapping = IntegrationMapping.model_validate(_BASE)

    issues = validate_mapping_authority(mapping, file_label="gsd.yaml")

    assert issues == []


def test_may_approve_true_is_rejected() -> None:
    data = {**_BASE, "permissions": {**_BASE["permissions"], "may_approve": True}}
    mapping = IntegrationMapping.model_validate(data)

    issues = validate_mapping_authority(mapping, file_label="gsd.yaml")

    assert len(issues) == 1
    assert "approve" in issues[0].reason
    assert issues[0].field == "permissions/may_approve"


def test_all_three_forbidden_permissions_are_each_reported() -> None:
    data = {
        **_BASE,
        "permissions": {
            **_BASE["permissions"],
            "may_approve": True,
            "may_transition_ggsad_state_directly": True,
            "may_close_ggsad_change": True,
        },
    }
    mapping = IntegrationMapping.model_validate(data)

    issues = validate_mapping_authority(mapping, file_label="gsd.yaml")

    assert len(issues) == 3
