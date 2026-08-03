"""Unit tests for atomic state replacement (R-012, R-013)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ggsad.engine.state_writer import StateWriteError, atomic_replace_state

REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_SCHEMA = REPO_ROOT / ".ggsad" / "schemas" / "state.schema.json"

_VALID_STATE_YAML = b"""\
schema_version: '0.1'
change:
  id: CHG-002
  slug: example
  title: Example
  class: M
flow:
  profile: standard
  phase: specify
  status: ready
goal:
  summary: Example
artifacts:
  spec: spec.md
  plan: plan.md
  tasks: tasks.md
  evidence: evidence.md
pair_review:
  required: true
  status: pending
  requestor: null
  reviewer: null
wait:
  reason: null
  category: null
  owner: null
  resume_condition: null
  safe_state: null
  resume_phase: null
  next_action: null
failure:
  reason: null
  category: null
history:
- timestamp: '2026-08-03T00:00:00Z'
  event: change-created
  actor: cli-user
"""


def test_atomic_replace_state_writes_valid_content(tmp_path: Path) -> None:
    state_path = tmp_path / "state.yaml"
    state_path.write_bytes(b"schema_version: '0.1'\n")  # old content

    atomic_replace_state(state_path, _VALID_STATE_YAML, STATE_SCHEMA)

    assert state_path.read_bytes() == _VALID_STATE_YAML


def test_atomic_replace_state_leaves_no_temp_file_behind(tmp_path: Path) -> None:
    state_path = tmp_path / "state.yaml"
    state_path.write_bytes(_VALID_STATE_YAML)

    atomic_replace_state(state_path, _VALID_STATE_YAML, STATE_SCHEMA)

    remaining = list(tmp_path.iterdir())
    assert remaining == [state_path]


def test_atomic_replace_state_rejects_invalid_content_and_preserves_original(
    tmp_path: Path,
) -> None:
    state_path = tmp_path / "state.yaml"
    state_path.write_bytes(_VALID_STATE_YAML)

    invalid = b"schema_version: '0.1'\n"  # missing every other required key

    with pytest.raises(StateWriteError):
        atomic_replace_state(state_path, invalid, STATE_SCHEMA)

    assert state_path.read_bytes() == _VALID_STATE_YAML  # untouched
    assert list(tmp_path.iterdir()) == [state_path]  # temp file cleaned up
