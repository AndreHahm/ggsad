"""Unit tests for the typed IntegrationMapping model."""

from __future__ import annotations

from typing import Any

from ggsad.models.mapping import IntegrationMapping

_VALID: dict[str, Any] = {
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


def test_parses_valid_mapping() -> None:
    mapping = IntegrationMapping.model_validate(_VALID)

    assert mapping.integration.id == "gsd"
    assert mapping.permissions.may_approve is False
    assert mapping.mappings[0].external_artifact == ".planning/STATE.md"


def test_mapping_entry_synchronization_defaults_to_none() -> None:
    mapping = IntegrationMapping.model_validate(_VALID)

    assert mapping.mappings[0].synchronization == "none"
