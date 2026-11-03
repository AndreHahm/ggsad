"""Repairing a damaged history (Section 24.4, AE-317)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from project_helpers import ADA, CONFIG, FIELDS, req, write

from ggsad.core.errors import StateError
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.history import Entry
from ggsad.core.new_change import create_change
from ggsad.core.operations import run_action
from ggsad.core.repair import REPAIRS_DIRECTORY, repair_change
from ggsad.core.reports import run_read_only
from ggsad.core.state_store import LOCK_FILE, StateStore, _exclusive_lock

STRICT = CONFIG + "minimum_levels: {sign_off: A2}\n"
STATE = "specs/c-1/state.json"
NOW = "2026-11-03T12:00:00Z"


def history(root: Path, entries: int) -> None:
    """A change with `entries` entries: the `new` entry and then questions."""
    write(root, ".ggsad/config.yaml", STRICT)
    assert create_change(root, "c-1", req("new"), FIELDS).result == "success"
    for number in range(entries - 1):
        done = run_action(root, "c-1", req("ask", text=f"Question {number}?"))
        assert done.result == "success", done.issues


def cut(root: Path, keep: int) -> None:
    path = root / STATE
    document = json.loads(path.read_text(encoding="utf-8"))
    document["entries"] = document["entries"][:keep]
    path.write_text(json.dumps(document), encoding="utf-8")


def repair(root: Path, *, show: bool = False, actor=ADA, reason: str = "disk fault"):
    request = req("repair", actor, reason=reason)
    return repair_change(root, "c-1", request, show_only=show)


@pytest.fixture
def truncated(root: Path) -> Path:
    """AE-317: an anchor at position 8 and a history of 5 consistent entries."""
    history(root, 8)
    cut(root, 5)
    return root


def test_a_truncated_history_stops_every_action_and_the_guard_says_so(truncated: Path) -> None:
    done = run_action(truncated, "c-1", req("ask", text="More?"))
    assert done.result == "rejected" and not done.changed
    assert "truncated" in done.issues[0].message
    guard = run_read_only(truncated, "c-1", "guard", NOW)
    assert "truncated" in guard.issues[0].message


def test_show_lists_the_damage_and_writes_nothing(truncated: Path) -> None:
    before = (truncated / STATE).read_bytes()
    done = repair(truncated, show=True)
    assert done.result == "success" and not done.changed
    assert done.data["entries_lost"] == 3 and done.data["entries_kept"] == 5
    assert (truncated / STATE).read_bytes() == before
    assert not (truncated / REPAIRS_DIRECTORY).exists()


def test_ae317_a_repair_records_what_was_lost_and_keeps_the_damaged_file(
    truncated: Path,
) -> None:
    damaged = (truncated / STATE).read_text(encoding="utf-8")
    done = repair(truncated)
    assert done.result == "success" and done.changed, done.issues
    assert done.data["entries_lost"] == 3 and done.data["entry"] == 6
    kept = truncated / str(done.data["damaged_file"])
    assert kept.read_text(encoding="utf-8") == damaged
    assert kept.parent == truncated / REPAIRS_DIRECTORY
    entries = json.loads((truncated / STATE).read_text(encoding="utf-8"))["entries"]
    assert len(entries) == 6 and entries[-1]["body"]["action"] == "repair"
    repaired = entries[-1]["body"]["repaired"]
    assert repaired["entries_lost"] == 3 and repaired["old_anchor"]["position"] == 8
    assert (
        repaired["reason"] == "disk fault" and repaired["damaged_file"] == done.data["damaged_file"]
    )
    anchor = GitAnchorStore(truncated).read("c-1")
    assert anchor is not None and anchor.position == 6 and anchor.hash == entries[-1]["hash"]


def test_work_goes_on_after_a_repair(truncated: Path) -> None:
    repair(truncated)
    assert run_action(truncated, "c-1", req("ask", text="Again?")).result == "success"
    assert run_read_only(truncated, "c-1", "guard", NOW).result == "success"


def test_a_rewritten_entry_keeps_the_entries_before_it(root: Path) -> None:
    history(root, 4)
    path = root / STATE
    document = json.loads(path.read_text(encoding="utf-8"))
    document["entries"][2]["body"]["note"] = "edited"
    path.write_text(json.dumps(document), encoding="utf-8")
    shown = repair(root, show=True)
    assert shown.data["entries_kept"] == 2 and shown.data["entries_lost"] == 2
    assert repair(root).result == "success"


def test_an_unreadable_state_document_cannot_be_repaired(root: Path) -> None:
    history(root, 3)
    (root / STATE).write_text("{not json", encoding="utf-8")
    done = repair(root)
    assert done.result == "rejected" and [i.code for i in done.issues] == ["repair-impossible"]


def test_a_consistent_history_is_not_repaired(root: Path) -> None:
    history(root, 3)
    done = repair(root)
    assert done.result == "rejected" and [i.code for i in done.issues] == ["history-consistent"]
    assert not done.changed


def test_an_agent_cannot_repair_and_a_reason_is_required(truncated: Path) -> None:
    refused = repair(truncated, actor=req("x").actor)
    assert refused.result == "rejected" and [i.code for i in refused.issues] == ["human-required"]
    silent = repair(truncated, reason=" ")
    assert silent.result == "rejected" and [i.code for i in silent.issues] == ["reason-missing"]
    assert not (truncated / REPAIRS_DIRECTORY).exists()
    assert len(json.loads((truncated / STATE).read_text())["entries"]) == 5


def test_a_repair_cannot_take_the_lock_and_writes_nothing(truncated: Path) -> None:
    before = (truncated / STATE).read_bytes()
    with _exclusive_lock(truncated / "specs/c-1" / LOCK_FILE):
        done = repair(truncated)
    assert done.result == "error" and [i.code for i in done.issues] == ["lock-unavailable"]
    assert not done.changed and (truncated / STATE).read_bytes() == before
    assert not list((truncated / REPAIRS_DIRECTORY).glob("*"))


def test_a_repair_stops_when_the_document_changed_after_it_was_examined(truncated: Path) -> None:
    store = StateStore(truncated / "specs/c-1", change_id="c-1")
    kept: list[Entry] = []
    with pytest.raises(StateError) as caught:
        store.replace_history(kept, "1.0", {}, expected_text="not the current text")
    assert caught.value.code == "state-conflict"
