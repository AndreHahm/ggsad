"""Adopting a history that has no anchor (Section 24.4, AE-044, AE-045)."""

from __future__ import annotations

from pathlib import Path

import pytest
from project_helpers import ADA, CONFIG, FIELDS, git, req, write

from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.new_change import create_change
from ggsad.core.operations import run_action
from ggsad.core.reports import run_read_only

STRICT = CONFIG + "minimum_levels: {sign_off: A2}\n"
NOW = "2026-11-03T12:00:00Z"


@pytest.fixture
def unanchored(root: Path) -> Path:
    write(root, ".ggsad/config.yaml", STRICT)
    assert create_change(root, "c-1", req("new"), FIELDS).result == "success"
    git(root, "update-ref", "-d", "refs/ggsad/anchors/c-1")
    return root


def test_a_history_without_an_anchor_stops_every_action(unanchored: Path) -> None:
    done = run_action(unanchored, "c-1", req("approve", ADA, target="spec"))
    assert done.result == "rejected" and [i.code for i in done.issues] == ["anchor-missing"]
    guard = run_read_only(unanchored, "c-1", "guard", NOW)
    assert [i.code for i in guard.issues] == ["anchor-missing"]


def test_ae044_a_human_adopts_the_history_and_work_goes_on(unanchored: Path) -> None:
    done = run_action(unanchored, "c-1", req("adopt", ADA))
    assert done.result == "success" and done.changed, done.issues
    anchor = GitAnchorStore(unanchored).read("c-1")
    assert anchor is not None and anchor.position == 2
    assert run_action(unanchored, "c-1", req("approve", ADA, target="spec")).result == "success"


def test_an_agent_cannot_adopt(unanchored: Path) -> None:
    done = run_action(unanchored, "c-1", req("adopt"))
    assert done.result == "rejected" and [i.code for i in done.issues] == ["human-required"]
    assert GitAnchorStore(unanchored).read("c-1") is None


def test_ae045_adoption_is_rejected_when_an_anchor_exists(root: Path) -> None:
    create_change(root, "c-1", req("new"), FIELDS)
    done = run_action(root, "c-1", req("adopt", ADA))
    assert done.result == "rejected" and [i.code for i in done.issues] == ["anchor-exists"]


def test_adoption_is_rejected_when_the_history_is_not_consistent(unanchored: Path) -> None:
    path = unanchored / "specs/c-1/state.json"
    path.write_text(path.read_text().replace("agent:builder", "agent:other"), encoding="utf-8")
    done = run_action(unanchored, "c-1", req("adopt", ADA))
    assert done.result == "rejected" and not done.changed
    assert GitAnchorStore(unanchored).read("c-1") is None
