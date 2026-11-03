"""Migration of a YAML state document to `state.json` (Section 25.3, AE-084, AE-098, AE-103)."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest
from project_helpers import ADA, FULL, git, req, write

from ggsad.core.canonical import ZERO_HASH
from ggsad.core.cli import main
from ggsad.core.content_hash import path_content_hash
from ggsad.core.doctor import run_doctor
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.history import verify_chain
from ggsad.core.migrate import migrate_change
from ggsad.core.operations import Envelope, run_action
from ggsad.core.state import State
from ggsad.core.state_store import StateStore

if TYPE_CHECKING:
    from ggsad.core.anchor import AnchorStore

OLD = """\
schema_version: "0.1"
change:
  id: CHG-001
  slug: reset
  title: Reset a password
  class: M
flow:
  profile: standard
  phase: {phase}
  status: {status}
goal:
  summary: Users can reset a password.
wait:
  reason: null
failure:
  reason: {failure}
  category: null
history:
  - timestamp: "2026-08-02T00:00:00Z"
    event: change-created
    actor: human
  - timestamp: "2026-08-02T12:00:00Z"
    event: adr-disposition-recorded
    actor: human:project-owner
    reason: ADR-0001 recorded
"""


def old_change(root: Path, status: str = "draft", failure: str = "null") -> Path:
    """A change directory with a definition and an old `state.yaml`, committed."""
    write(root, "specs/c-1/change.yaml", FULL)
    write(root, "specs/c-1/state.yaml", OLD.format(phase="specify", status=status, failure=failure))
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "old change")
    return root / "specs" / "c-1"


def migrate(root: Path, anchors: AnchorStore | None = None, target: str | None = None) -> Envelope:
    return migrate_change(root, "c-1", req("migrate", ADA), anchors, target)


def test_ae103_the_yaml_state_becomes_state_json_with_a_migrate_entry(root: Path) -> None:
    folder = old_change(root)
    before = (folder / "state.yaml").read_bytes()
    done = migrate(root)
    assert done.result == "success" and done.changed, done.issues
    document = StateStore(folder).read()
    assert document is not None and verify_chain(document.entries) == []
    first = document.entries[0]
    assert (first.n, first.prev, first.body["action"]) == (1, ZERO_HASH, "migrate")
    assert first.body["source_hash"] == path_content_hash(folder / "state.yaml")
    assert (first.body["source_version"], first.body["target_version"]) == ("0.1", "1.0")
    assert (folder / "state.yaml").read_bytes() == before
    assert State.from_json(first.body["after"]).state == "open"


def test_ae084_the_old_history_is_kept_as_a_note_of_the_first_entry(root: Path) -> None:
    folder = old_change(root)
    migrate(root)
    document = StateStore(folder).read()
    assert document is not None
    note = document.entries[0].body["note"]
    assert isinstance(note, str)
    assert "change-created" in note and "adr-disposition-recorded" in note
    assert "2026-08-02T00:00:00Z" in note


def test_the_anchor_follows_the_migrated_history(root: Path) -> None:
    old_change(root)
    assert migrate(root, anchors=GitAnchorStore(root)).result == "success"
    anchor = GitAnchorStore(root).read("c-1")
    assert anchor is not None and anchor.position == 1


@pytest.mark.parametrize(
    ("status", "state", "outcome"),
    [("draft", "open", None), ("ready", "open", None), ("done", "closed", "done"),
     ("cancelled", "closed", "cancelled")],
)  # fmt: skip
def test_clear_statuses_are_taken_over(root: Path, status: str, state: str, outcome: str) -> None:
    folder = old_change(root, status)
    assert migrate(root).result == "success"
    document = StateStore(folder).read()
    assert document is not None
    taken = State.from_json(document.entries[0].body["after"])
    assert (taken.state, taken.outcome) == (state, outcome)


def test_a_failed_change_keeps_its_reason(root: Path) -> None:
    folder = old_change(root, "failed", failure='"the test never passed"')
    assert migrate(root).result == "success"
    document = StateStore(folder).read()
    assert document is not None
    taken = State.from_json(document.entries[0].body["after"])
    assert (taken.state, taken.outcome, taken.reason) == (
        "closed",
        "failed",
        "the test never passed",
    )


def test_a_failed_change_without_a_reason_is_refused(root: Path) -> None:
    folder = old_change(root, "failed")
    done = migrate(root)
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["legacy-failure-reason-missing"]
    assert not (folder / "state.json").exists()


@pytest.mark.parametrize("status", ["active", "waiting", "superseded", "paused"])
def test_a_status_without_a_clear_match_is_refused_by_name(root: Path, status: str) -> None:
    folder = old_change(root, status)
    done = migrate(root)
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["legacy-status-unmapped"]
    assert status in done.issues[0].message
    assert not (folder / "state.json").exists()


def test_a_missing_definition_is_not_guessed(root: Path) -> None:
    folder = old_change(root)
    (folder / "change.yaml").unlink()
    done = migrate(root)
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["definition-missing"]
    assert not (folder / "state.json").exists()


@pytest.mark.parametrize(
    "text",
    ["- not a mapping\n", 'schema_version: "0.1"\nflow: 3\n', "key: [unclosed\n"],
)
def test_an_unreadable_old_file_is_refused(root: Path, text: str) -> None:
    folder = old_change(root)
    write(root, "specs/c-1/state.yaml", text)
    done = migrate(root)
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["legacy-state-invalid"]
    assert not (folder / "state.json").exists()


def test_another_old_version_is_unsupported(root: Path) -> None:
    folder = old_change(root)
    text = (folder / "state.yaml").read_text(encoding="utf-8").replace('"0.1"', '"0.2"', 1)
    write(root, "specs/c-1/state.yaml", text)
    done = migrate(root)
    assert [i.code for i in done.issues] == ["schema-version-unsupported"]
    assert done.result == "rejected" and not done.changed


def test_an_old_state_stops_every_other_action_until_it_is_migrated(root: Path) -> None:
    old_change(root)
    done = run_action(root, "c-1", req("start"))
    assert done.result == "rejected" and "migration-required" in [i.code for i in done.issues]
    assert migrate(root).result == "success"
    again = run_action(root, "c-1", req("start"))
    assert "migration-required" not in [i.code for i in again.issues]


def test_a_current_state_document_is_not_migrated(root: Path) -> None:
    old_change(root)
    assert migrate(root).result == "success"
    done = migrate(root)
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["migration-not-needed"]


def test_state_json_wins_over_an_old_file(root: Path) -> None:
    folder = old_change(root)
    assert migrate(root).result == "success"
    before = (folder / "state.json").read_text(encoding="utf-8")
    assert migrate(root).result == "rejected"
    assert (folder / "state.json").read_text(encoding="utf-8") == before


def test_a_target_version_must_be_supported(root: Path) -> None:
    folder = old_change(root)
    done = migrate(root, target="2.0")
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["schema-version-unsupported"]
    assert not (folder / "state.json").exists()
    assert migrate(root, target="1.0").result == "success"


def test_a_change_without_any_state_has_nothing_to_migrate(root: Path) -> None:
    write(root, "specs/c-1/change.yaml", FULL)
    done = migrate(root)
    assert done.result == "rejected" and not done.changed
    assert [i.code for i in done.issues] == ["nothing-to-migrate"]


def test_the_command_migrates_a_change(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    folder = old_change(root)
    code = main(["migrate", "c-1", "--root", str(root), "--actor", "human:ada"])
    assert code == 0, capsys.readouterr().out
    assert (folder / "state.json").exists()
    assert main(["migrate", "c-1", "--root", str(root), "--actor", "human:ada"]) == 1


def test_the_doctor_names_the_migrate_command(root: Path) -> None:
    old_change(root)
    done = run_doctor(root, "2026-11-03T12:00:00Z")
    findings = cast("list[dict[str, str]]", done.data["findings"])
    found = [(f["code"], f["fix"]) for f in findings if f["severity"] == "problem"]
    assert (
        "migration-required",
        "run `ggsad migrate c-1`; the old state.yaml stays as it is",
    ) in found
