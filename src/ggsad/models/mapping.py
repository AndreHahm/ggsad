"""Typed view of `.ggsad/mappings/*.yaml` (companion integration mappings).

Mirrors the required shape of `.ggsad/schemas/mappings.schema.json`. The
`permissions` block is fully typed (not `extra="allow"`) because
`mapping_authority.py` inspects it directly to enforce R-006/R-017 — GSD or
any companion may never gain approval, direct-transition, or closure
authority over GG-SAD state.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class IntegrationBlock(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    id: str
    mode: str
    version: str | None = None
    description: str | None = None


class MappingPermissions(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    may_modify_approved_specification: bool
    may_modify_accepted_adr: bool
    may_transition_ggsad_state_directly: bool
    may_approve: bool
    may_close_ggsad_change: bool
    may_write_paths: list[str] | None = None
    may_read_paths: list[str] | None = None
    deny_paths: list[str] | None = None


class MappingEntry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    external_artifact: str
    ggsad_role: str
    authoritative: bool
    external_command: str | None = None
    ggsad_phase: str | None = None
    ggsad_artifact: str | None = None
    synchronization: str = "none"
    notes: str | None = None


class MappingFailurePolicy(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    on_mapping_conflict: str
    on_sync_error: str
    uninstall_preserves_ggsad_artifacts: bool
    recovery_instructions: str | None = None


class IntegrationMapping(BaseModel):
    """Typed view of a `.ggsad/mappings/*.yaml` file, e.g. `gsd.yaml`."""

    model_config = ConfigDict(frozen=True, extra="allow")

    integration: IntegrationBlock
    ownership: dict[str, str]
    sources_of_truth: dict[str, str]
    permissions: MappingPermissions
    failure: MappingFailurePolicy
    schema_version: str | None = None
    mappings: list[MappingEntry] = Field(default_factory=list)
