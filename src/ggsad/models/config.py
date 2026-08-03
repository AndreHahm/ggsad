"""Typed view of `.ggsad/config.yaml` (GG-SAD project configuration).

Mirrors the required shape of `.ggsad/schemas/config.schema.json`. JSON
Schema remains the authoritative structural contract (R-005); these models
are a typed convenience layer for code that needs to work with already
schema-valid configuration, not a replacement validator. Optional schema
sections without a current consumer (`permissions`, `evidence`, `retention`,
`budgets`) are intentionally left untyped via `extra="allow"` rather than
speculatively modeled, to avoid the two representations drifting apart.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProjectSection(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    id: str
    operating_mode: str
    compliance_profile: str
    name: str | None = None
    repository_type: str | None = None
    delivery_context: str | None = None


class MethodSection(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    name: str
    version: str


class WorkflowSection(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    default_change_class: str
    enabled_phases: list[str]
    default_flow_profile: str | None = None
    skippable_phases: list[str] | None = None
    profiles_path: str | None = None
    templates_path: str | None = None
    schemas_path: str | None = None


class PairReviewPolicy(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    default_requirement: str
    distinct_requestor_and_reviewer: bool
    required_for: list[str]
    human_approval_required_for: list[str]
    human_human_allowed: bool | None = None
    allowed_participant_types: list[str] | None = None
    separate_review_document: str | None = None
    blocking_finding_rule: str | None = None


class IntegrationDeclaration(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    id: str
    mode: str
    mapping: str
    version: str | None = None
    enabled: bool = True


class MemorySection(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    enabled: bool
    backend: str | None = None
    path: str | None = None
    record_types: list[str] | None = None


class ProjectConfig(BaseModel):
    """Typed view of `.ggsad/config.yaml`."""

    model_config = ConfigDict(frozen=True, extra="allow")

    schema_version: str
    project: ProjectSection
    method: MethodSection
    workflow: WorkflowSection
    pair_review: PairReviewPolicy
    memory: MemorySection
    integrations: list[IntegrationDeclaration] = Field(default_factory=list)
