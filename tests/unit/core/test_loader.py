"""Reading one change from disk and building the facts of the engine."""

from __future__ import annotations

import json
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.git_scope import head_revision
from ggsad.core.loader import LoadedChange, anchor_required, existing_ids, load_change
from ggsad.core.project import (
    BRIEF_PATH,
    CONFIG_PATH,
    CONSTITUTION_PATH,
    definitions_hash,
    load_settings,
)
from ggsad.core.settings import Settings
from ggsad.core.state import State
from ggsad.core.state_store import StateStore

CONFIG = """\
schema_version: "1.0"
project: {id: demo, compliance_profile: lean}
roles: {owner: "human:ada"}
"""
SENTENCE = "Users can reset a password"
CHANGE_YAML = """\
schema_version: "1.0"
id: c-1
method_profile: core
compliance_profile: lean
author: "human:ada"
owner: "human:ada"
goal:
  problem: Resets are manual
  done_when: ["Users can reset a password"]
  non_goals: []
scope:
  allow: ["lib/**"]
requirements:
  - id: R1
    text: A user can reset a password
    examples: ["Given a user, when they reset, then a mail is sent"]
    done_when: ["Users can reset a password"]
    evidence:
      - command: [run-tests]
        exit_map: {satisfied: [0], not_satisfied: [1]}
gates: {fail: [], wait: [], done: []}
"""


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def write(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def body(state: State) -> dict[str, Any]:
    return {
        "action": "new",
        "actor": "agent:builder",
        "account": None,
        "assurance": "A0",
        "at": "2026-11-03T10:00:00Z",
        "result": "success",
        "gate_results": None,
        "gate_detail": None,
        "files": None,
        "note": None,
        "after": state.to_json(),
    }


@pytest.fixture
def root(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    write(tmp_path, CONFIG_PATH, CONFIG)
    write(tmp_path, CONSTITUTION_PATH, "rules\n")
    write(tmp_path, "specs/c-1/change.yaml", CHANGE_YAML)
    write(tmp_path, "specs/c-1/spec.md", "# Spec\nConflicts with higher documents: none\n")
    write(tmp_path, "lib/a.py", "x\n")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


@pytest.fixture
def settings(root: Path) -> Settings:
    found, issues = load_settings(root)
    assert found is not None, issues
    return found


def load(root: Path, settings: Settings, action: str | None = None) -> LoadedChange:
    return load_change(root, settings, "c-1", GitAnchorStore(root), action)


def start(root: Path, state: State) -> None:
    store = StateStore(root / "specs/c-1", anchors=GitAnchorStore(root), change_id="c-1")
    store.append(body(state), read_version=0)


def test_a_change_without_a_history_is_new(root: Path, settings: Settings) -> None:
    loaded = load(root, settings)
    assert loaded.state is None and loaded.read_version == 0
    assert loaded.problems == () and loaded.history_error is None
    assert loaded.facts.has_anchor is False


def test_the_facts_hold_the_hashes_and_the_fingerprint(root: Path, settings: Settings) -> None:
    loaded = load(root, settings)
    assert loaded.definition is not None
    assert loaded.facts.definitions_hash == definitions_hash(loaded.definition)
    assert loaded.facts.spec_hash is not None
    assert list(loaded.facts.documents) == [CONSTITUTION_PATH]
    assert loaded.facts.gates_approved is False


def test_a_valid_definition_passes_new_and_the_gate_approval(
    root: Path, settings: Settings
) -> None:
    loaded = load(root, settings)
    assert loaded.facts.target_issues["new"] == ()
    assert loaded.facts.target_issues["approve:gates"] == ()
    assert loaded.facts.target_issues["approve:spec"] == ()


def test_a_spec_without_the_conflict_line_cannot_be_approved(
    root: Path, settings: Settings
) -> None:
    write(root, "specs/c-1/spec.md", "# Spec\n")
    codes = [c for c, _ in load(root, settings).facts.target_issues["approve:spec"]]
    assert codes == ["conflict-line-missing"]


def test_a_missing_review_cannot_be_approved(root: Path, settings: Settings) -> None:
    codes = [c for c, _ in load(root, settings).facts.target_issues["approve:review"]]
    assert codes == ["review-missing"]


def test_a_missing_definition_is_a_problem(root: Path, settings: Settings) -> None:
    (root / "specs/c-1/change.yaml").unlink()
    loaded = load(root, settings)
    assert loaded.definition is None
    assert [p.code for p in loaded.problems] == ["definition-missing"]


def test_a_definition_with_an_unusable_version_is_refused(root: Path, settings: Settings) -> None:
    write(root, "specs/c-1/change.yaml", CHANGE_YAML.replace('"1.0"', '"9.9"', 1))
    loaded = load(root, settings)
    assert [p.code for p in loaded.problems] == ["schema-version-unsupported"]


def test_an_identifier_that_is_a_path_reads_nothing(root: Path, settings: Settings) -> None:
    loaded = load_change(root, settings, "../x", GitAnchorStore(root))
    assert [p.code for p in loaded.problems] == ["id-invalid"]
    assert loaded.state is None


def test_the_state_and_the_counts_come_from_the_history(root: Path, settings: Settings) -> None:
    start(root, State())
    loaded = load(root, settings)
    assert loaded.state is not None and loaded.state.state == "open"
    assert loaded.read_version == 1
    assert loaded.facts.has_anchor is True


def test_a_damaged_history_is_reported_and_marked(root: Path, settings: Settings) -> None:
    start(root, State())
    path = root / "specs/c-1/state.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["entries"][0]["body"]["actor"] = "agent:other"
    path.write_text(json.dumps(document), encoding="utf-8")
    loaded = load(root, settings)
    assert loaded.history_error is not None
    assert loaded.facts.history_damaged is True
    assert loaded.state is None


def test_the_revision_and_unclean_work_are_asked_only_for_start(
    root: Path, settings: Settings
) -> None:
    write(root, "lib/b.py", "uncommitted\n")
    assert load(root, settings).facts.revision is None
    started = load(root, settings, "start")
    assert started.facts.revision == head_revision(root)
    assert started.facts.unclean_paths == ("lib/b.py",)


def test_the_scope_is_measured_once_the_change_has_a_base_revision(
    root: Path, settings: Settings
) -> None:
    assert load(root, settings).facts.scope is None
    start(root, State(state="active", base_revision=head_revision(root)))
    write(root, "docs/other.md", "outside\n")
    scope = load(root, settings).facts.scope
    assert scope is not None and scope.result == "satisfied"
    assert "docs/other.md" in scope.detail


def test_the_spec_must_be_approved_before_the_start_unless_the_profile_is_lean(
    root: Path, settings: Settings
) -> None:
    assert load(root, settings).facts.spec_approval_ok is True
    standard = replace(settings, compliance_profile="standard")
    assert load(root, standard).facts.spec_approval_ok is False
    levelled = replace(settings, minimum_levels={"spec_approval": "A0"})
    assert load(root, levelled).facts.spec_approval_ok is False


def test_open_changes_are_listed_for_supersede_only(root: Path, settings: Settings) -> None:
    write(root, "specs/c-2/change.yaml", CHANGE_YAML.replace("id: c-1", "id: c-2"))
    store = StateStore(root / "specs/c-2", change_id="c-2")
    store.append(body(State()), read_version=0)
    assert load(root, settings).facts.open_changes == frozenset()
    assert load(root, settings, "supersede").facts.open_changes == {"c-2"}
    assert existing_ids(root) == ["c-1", "c-2"]


def test_a_profile_that_differs_from_the_brief_stops_new(root: Path, settings: Settings) -> None:
    write(root, BRIEF_PATH, "Compliance profile: governed\n")
    codes = [c for c, _ in load(root, settings).facts.target_issues["new"]]
    assert "profile-mismatch" in codes


def test_an_anchor_is_required_when_a_level_is_a2(settings: Settings) -> None:
    assert anchor_required(settings) is False
    assert anchor_required(replace(settings, minimum_levels={"sign_off": "A2"})) is True
