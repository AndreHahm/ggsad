"""Running operations end to end on a real project: new, approve, start, and refusals."""

from __future__ import annotations

import json
from pathlib import Path

from project_helpers import ADA, FIELDS, FULL, make_change, req, settle, write

from ggsad.core.engine_types import Actor
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.issues import Issue
from ggsad.core.new_change import create_change
from ggsad.core.operations import Envelope, run_action


def codes(envelope: Envelope) -> list[str]:
    return [i.code for i in envelope.issues]


def test_new_writes_the_files_and_the_first_entry(root: Path) -> None:
    done = make_change(root)
    assert done.result == "success" and done.changed and done.problems() == []
    assert (root / "specs/c-1/change.yaml").is_file()
    assert "Conflicts with higher documents: none" in (root / "specs/c-1/spec.md").read_text()
    assert GitAnchorStore(root).read("c-1") is not None
    assert done.state is not None and done.state["state"] == "open"


def test_a_rejected_new_leaves_no_file_behind(root: Path) -> None:
    done = create_change(root, "c-1", req("new", Actor("agent:stranger")), FIELDS)
    assert done.result == "rejected" and not done.changed
    assert codes(done) == ["requestor-not-approved"]
    assert not (root / "specs").exists()


def test_new_with_a_bad_identifier_writes_nothing(root: Path) -> None:
    done = create_change(root, "../x", req("new"), FIELDS)
    assert done.result == "rejected" and codes(done) == ["id-invalid"]
    assert not (root / "specs").exists()


def test_new_twice_is_rejected_and_keeps_the_first(root: Path) -> None:
    make_change(root)
    again = make_change(root)
    assert again.result == "rejected" and codes(again) == ["change-exists"]
    assert (root / "specs/c-1/state.json").is_file()


def test_new_in_a_project_without_a_config_is_an_error(tmp_path: Path) -> None:
    done = create_change(tmp_path, "c-1", req("new"), FIELDS)
    assert done.result == "error" and codes(done) == ["config-missing"]
    assert not done.changed and done.exit_code == 2


def test_a_hand_written_definition_is_kept(root: Path) -> None:
    write(root, "specs/c-1/change.yaml", FULL)
    assert make_change(root).result == "success"
    assert "run-tests" in (root / "specs/c-1/change.yaml").read_text()


def test_the_walk_from_new_to_start(root: Path) -> None:
    make_change(root)
    settle(root)
    assert run_action(root, "c-1", req("approve", ADA, target="all")).result == "success"
    started = run_action(root, "c-1", req("start"))
    assert started.result == "success", started.issues
    assert started.state is not None and started.state["state"] == "active"
    document = json.loads((root / "specs/c-1/state.json").read_text())
    actions = [e["body"]["action"] for e in document["entries"]]
    assert actions == ["new", "approve", "start"]


def test_an_edit_of_the_gates_after_the_approval_stops_every_action(root: Path) -> None:
    make_change(root)
    settle(root)
    run_action(root, "c-1", req("approve", ADA, target="all"))
    write(root, "specs/c-1/change.yaml", FULL.replace("lib/**", "src/**"))
    done = run_action(root, "c-1", req("start"))
    assert done.result == "rejected" and "gates-changed" in codes(done)
    assert not done.changed


def test_a_rejected_action_writes_nothing(root: Path) -> None:
    make_change(root)
    before = (root / "specs/c-1/state.json").read_text()
    done = run_action(root, "c-1", req("close"))
    assert done.result == "rejected" and not done.changed
    assert (root / "specs/c-1/state.json").read_text() == before


def test_a_tampered_history_is_refused(root: Path) -> None:
    make_change(root)
    path = root / "specs/c-1/state.json"
    document = json.loads(path.read_text())
    document["entries"][0]["body"]["actor"] = "agent:other"
    path.write_text(json.dumps(document))
    done = run_action(root, "c-1", req("approve", ADA, target="spec"))
    assert done.result == "rejected" and not done.changed
    assert done.issues


def test_an_action_on_a_change_that_does_not_exist_is_rejected(root: Path) -> None:
    done = run_action(root, "nope", req("start"))
    assert done.result == "rejected" and "definition-missing" in codes(done)


def test_the_envelope_rules() -> None:
    issue = (Issue("x", "m"),)
    assert Envelope("a", "success", True).problems() == []
    assert Envelope("a", "rejected", True, issues=issue).problems()
    assert Envelope("a", "blocked", False, issues=issue).problems()
    assert Envelope("a", "rejected", False).problems()
    assert Envelope("a", "odd", False, issues=issue).problems()
    assert Envelope("a", "blocked", True, issues=issue).exit_code == 1


def test_json_omits_what_does_not_apply() -> None:
    plain = Envelope("a", "success", False).to_json()
    assert plain == {"operation": "a", "result": "success", "changed": False}
    shown = Envelope("a", "error", False, issues=(Issue("c", "m", "p"),), data={"k": 1}).to_json()
    assert shown["issues"] == [{"code": "c", "message": "m", "path": "p"}]
    assert shown["data"] == {"k": 1}
