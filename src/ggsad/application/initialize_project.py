"""Project initialization (R-001, R-002, R-012).

Generates the approved CHG-001 asset manifest -- `.ggsad/config.yaml`
(rendered with sensible schema-valid defaults), the packaged schemas and
templates, and the four project-level governing documents that map 1:1 to a
packaged template (constitution, project-brief, architecture, roadmap) --
and writes it with conservative idempotency (plan.md Sec 4.1):

- a target file that doesn't exist yet is created;
- a target file that exists with byte-identical content is left unchanged;
- a target file that exists with different content is a conflict.

If any conflict is found, nothing is written: the whole manifest is
preflighted before any file is touched, so a failed `init` never leaves a
partial or unexpected mutation (R-012).

Deliberately excluded from this manifest: `docs/adr/` (ADRs are authored
per-decision, not templated at init time) and `docs/definitions/` (four
distinct DoR/DoD/DoW/DoF documents from one generic template, with no
described CHG-001 command to disambiguate them). Both are structural
locations in `architecture.md`'s diagram, not artifacts with a concrete
acceptance example requiring them at init time.
"""

from __future__ import annotations

import re
from io import StringIO
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from ggsad.application.manifest_writer import (
    PreflightResult,
    WriteResult,
    preflight,
    write_manifest,
)
from ggsad.resources import resource_root

# `InitResult` is `WriteResult` under the name this module's public API has
# used since Slice 3 -- the write semantics are identical and shared with
# `create_change.py` via `manifest_writer.write_manifest`.
InitResult = WriteResult

__all__ = [
    "InitResult",
    "PreflightResult",
    "build_asset_manifest",
    "initialize_project",
    "preflight",
    "slugify_project_id",
]

_SLUG_INVALID = re.compile(r"[^a-z0-9]+")

_DOC_TEMPLATES: dict[str, str] = {
    "constitution.template.md": "constitution.md",
    "project-brief.template.md": "project-brief.md",
    "architecture.template.md": "architecture.md",
    "roadmap.template.md": "roadmap.md",
}


def slugify_project_id(name: str) -> str:
    """Derive a schema-valid `project.id` from a directory name."""
    slug = _SLUG_INVALID.sub("-", name.lower()).strip("-")
    return slug or "ggsad-project"


def _default_config_yaml(project_id: str) -> bytes:
    config: dict[str, Any] = {
        "schema_version": "0.1",
        "project": {
            "id": project_id,
            "operating_mode": "stand-alone",
            "compliance_profile": "standard",
        },
        "method": {
            "name": "Goal-Gated Spec-Anchored Development",
            "version": "1.3",
        },
        "workflow": {
            "default_change_class": "M",
            "enabled_phases": [
                "intake",
                "specify",
                "plan",
                "build",
                "verify",
                "release",
                "closed",
            ],
        },
        "pair_review": {
            "default_requirement": "optional",
            "distinct_requestor_and_reviewer": True,
            "required_for": [],
            "human_approval_required_for": [],
        },
        "integrations": [],
        "memory": {"enabled": False},
    }

    dumper = YAML(typ="safe")
    dumper.default_flow_style = False
    buffer = StringIO()
    dumper.dump(config, buffer)
    return buffer.getvalue().encode("utf-8")


def build_asset_manifest(target: Path) -> dict[Path, bytes]:
    """Build the approved CHG-001 init manifest: absolute path -> desired content."""
    target = target.resolve()
    manifest: dict[Path, bytes] = {}

    project_id = slugify_project_id(target.name)
    manifest[target / ".ggsad" / "config.yaml"] = _default_config_yaml(project_id)

    resources = resource_root()

    for entry in (resources / "schemas").iterdir():
        if entry.is_file():
            manifest[target / ".ggsad" / "schemas" / entry.name] = entry.read_bytes()

    for entry in (resources / "templates").iterdir():
        if entry.is_file():
            manifest[target / ".ggsad" / "templates" / entry.name] = entry.read_bytes()
            doc_name = _DOC_TEMPLATES.get(entry.name)
            if doc_name is not None:
                manifest[target / "docs" / doc_name] = entry.read_bytes()

    return manifest


def initialize_project(target: Path) -> InitResult:
    """Initialize (or safely re-run against) a GG-SAD project at `target`.

    Nothing is written if any conflict is found (R-012): the manifest is
    fully preflighted first. See `manifest_writer.write_manifest` for the
    shared preflight-then-write logic used by both `init` and `new`.
    """
    manifest = build_asset_manifest(target)
    return write_manifest(manifest)
