"""Integration tests for packaged GG-SAD method assets.

Verifies that schemas, templates, and the GSD mapping are readable through
the packaged resource loader at runtime, independent of this repository's
own top-level ``.ggsad/`` directory.
"""

from __future__ import annotations

import json

from ruamel.yaml import YAML

from ggsad.resources import resource_root

yaml = YAML(typ="safe")

EXPECTED_SCHEMAS = {
    "config.schema.json",
    "mappings.schema.json",
    "state.schema.json",
}

EXPECTED_TEMPLATES = {
    "adr.template.md",
    "architecture.template.md",
    "constitution.template.md",
    "definition.template.md",
    "evidence.template.md",
    "plan.template.md",
    "project-brief.template.md",
    "roadmap.template.md",
    "spec.template.md",
    "tasks.template.md",
}


def test_packaged_schemas_are_present_and_valid_json() -> None:
    schemas_dir = resource_root() / "schemas"
    names = {entry.name for entry in schemas_dir.iterdir()}

    assert names >= EXPECTED_SCHEMAS

    for name in EXPECTED_SCHEMAS:
        content = (schemas_dir / name).read_text(encoding="utf-8")
        schema = json.loads(content)
        assert "$schema" in schema
        assert "$id" in schema


def test_packaged_templates_are_present() -> None:
    templates_dir = resource_root() / "templates"
    names = {entry.name for entry in templates_dir.iterdir()}

    assert names >= EXPECTED_TEMPLATES


def test_packaged_gsd_mapping_is_valid_yaml_with_required_keys() -> None:
    mapping_path = resource_root() / "mappings" / "gsd.yaml"
    content = mapping_path.read_text(encoding="utf-8")
    mapping = yaml.load(content)

    assert mapping["integration"]["id"] == "gsd"
    assert mapping["permissions"]["may_approve"] is False
    assert mapping["permissions"]["may_transition_ggsad_state_directly"] is False
    assert mapping["permissions"]["may_close_ggsad_change"] is False
