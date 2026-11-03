"""Running operations end to end on a real project: new, approve, start, and refusals."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from project_helpers import ADA, CONFIG, FIELDS, FULL, make_change, req, settle, write

from ggsad.core.definition_update import DefinitionUpdateError, set_owner
from ggsad.core.engine_types import Actor
from ggsad.core.errors import StateError
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.issues import Issue
from ggsad.core.loader import load_change
from ggsad.core.new_change import NewFields, create_change
from ggsad.core.operations import Envelope, now_utc, run_action
from ggsad.core.project import load_settings
from ggsad.core.state_store import StateStore


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


def test_new_refuses_a_change_folder_that_leads_outside_the_project(
    root: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    outside = tmp_path_factory.mktemp("outside")
    (root / "specs").mkdir()
    try:
        (root / "specs" / "c-1").symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("links cannot be created here")
    done = create_change(root, "c-1", req("new"), FIELDS)
    assert done.result == "rejected" and codes(done) == ["path-outside-project"]
    assert list(outside.iterdir()) == []


def test_new_keeps_non_bmp_characters_in_the_generated_files(root: Path) -> None:
    fields = NewFields("Fix \U0001f600", ["Users see \U0001f600"], "human:ada", "human:ada")
    done = create_change(root, "c-1", req("new"), fields)
    assert done.result == "success", done.issues
    assert "\U0001f600" in (root / "specs/c-1/change.yaml").read_text(encoding="utf-8")


def test_new_keeps_its_files_when_the_entry_was_recorded_but_the_anchor_lagged(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def refuse(self: GitAnchorStore, change_id: str, anchor: object) -> None:
        raise StateError("anchor-write-failed", "no space")

    monkeypatch.setattr(GitAnchorStore, "write", refuse)
    done = create_change(root, "c-1", req("new"), FIELDS)
    assert done.result == "error" and done.changed and codes(done) == ["anchor-lagging"]
    assert (root / "specs/c-1/change.yaml").is_file() and (root / "specs/c-1/state.json").is_file()


def test_a_state_conflict_does_not_claim_that_this_call_recorded_anything(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    make_change(root)
    real = StateStore.append

    def competing(self: StateStore, body: dict[str, object], *, read_version: int) -> object:
        real(self, {**body, "note": "other writer"}, read_version=read_version)
        raise StateError("state-conflict", "another writer changed the change")

    monkeypatch.setattr(StateStore, "append", competing)
    done = run_action(root, "c-1", req("ask", text="Q?"))
    assert done.result == "error" and codes(done) == ["state-conflict"]
    assert not done.changed and done.problems() == []


def test_the_clock_gives_a_utc_time_to_the_second() -> None:
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", now_utc())


@pytest.mark.parametrize("change_id", ["a/b", "..", "x/../y"])
def test_new_refuses_an_identifier_that_is_a_path(root: Path, change_id: str) -> None:
    done = create_change(root, change_id, req("new"), FIELDS)
    assert done.result == "rejected" and not (root / "specs").exists()


ADA_LINE = '    - {identity: "human:ada", account: ada-gh}\n'
CY_LINE = '    - {identity: "human:cy", account: cy-gh}\n'
WITH_CY = CONFIG.replace(ADA_LINE, ADA_LINE + CY_LINE)


def test_ae325_a_handover_updates_the_owner_in_the_definition(root: Path) -> None:
    write(root, ".ggsad/config.yaml", WITH_CY)
    make_change(root)
    before = (root / "specs/c-1/change.yaml").read_text(encoding="utf-8")
    assert "# Paths this change may touch" in before
    done = run_action(root, "c-1", req("handover", ADA, owner="human:cy", reason="Bo left"))
    assert done.result == "success", done.issues
    after = (root / "specs/c-1/change.yaml").read_text(encoding="utf-8")
    assert 'owner: "human:cy"' in after or "owner: human:cy" in after
    assert "# Paths this change may touch" in after
    settings, _ = load_settings(root)
    assert settings is not None
    loaded = load_change(root, settings, "c-1", GitAnchorStore(root))
    assert loaded.context.change_owner == "human:cy"


def test_a_handover_does_not_make_the_gates_look_changed(root: Path) -> None:
    write(root, ".ggsad/config.yaml", WITH_CY)
    make_change(root)
    settle(root)
    run_action(root, "c-1", req("approve", ADA, target="all"))
    run_action(root, "c-1", req("handover", ADA, owner="human:cy", reason="Bo left"))
    assert run_action(root, "c-1", req("start")).result == "success"


def test_a_document_that_cannot_be_read_is_an_error_not_a_traceback(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    make_change(root)

    def unreadable(path: Path) -> str:
        raise PermissionError(path.name)

    monkeypatch.setattr("ggsad.core.project.path_content_hash", unreadable)
    done = run_action(root, "c-1", req("ask", text="Q?"))
    assert done.result == "error" and codes(done) == ["document-unreadable"] and not done.changed


def test_a_handover_whose_definition_cannot_be_updated_says_so(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write(root, ".ggsad/config.yaml", WITH_CY)
    make_change(root)

    def refuse(path: Path, owner: str) -> None:
        raise DefinitionUpdateError(path.name + owner)

    monkeypatch.setattr("ggsad.core.operations.set_owner", refuse)
    done = run_action(root, "c-1", req("handover", ADA, owner="human:cy", reason="Bo left"))
    assert done.result == "error" and done.changed
    assert codes(done) == ["definition-update-failed"] and "human:cy" in done.issues[0].message


def test_set_owner_refuses_a_file_that_is_not_a_mapping(tmp_path: Path) -> None:
    path = tmp_path / "change.yaml"
    path.write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(DefinitionUpdateError):
        set_owner(path, "human:cy")
    path.write_text("a: [unclosed\n", encoding="utf-8")
    with pytest.raises(DefinitionUpdateError):
        set_owner(path, "human:cy")


FOLLOW_UP = FULL.replace("id: c-1", "id: c-2") + "follows: c-0\n"


def closed_change(root: Path) -> None:
    write(root, "specs/c-0/change.yaml", FULL.replace("id: c-1", "id: c-0"))
    assert create_change(root, "c-0", req("new"), FIELDS).result == "success"
    assert run_action(root, "c-0", req("cancel", ADA, reason="done with it")).result == "success"


def test_a_follow_up_of_a_closed_change_can_be_created_and_approved(root: Path) -> None:
    closed_change(root)
    write(root, "specs/c-2/change.yaml", FOLLOW_UP)
    done = create_change(root, "c-2", req("new"), FIELDS)
    assert done.result == "success", done.issues
    approved = run_action(root, "c-2", req("approve", ADA, target="gates"))
    assert approved.result == "success", approved.issues


def test_a_follow_up_of_a_change_that_is_not_closed_is_rejected(root: Path) -> None:
    write(root, "specs/c-0/change.yaml", FULL.replace("id: c-1", "id: c-0"))
    create_change(root, "c-0", req("new"), FIELDS)
    write(root, "specs/c-2/change.yaml", FOLLOW_UP)
    done = create_change(root, "c-2", req("new"), FIELDS)
    assert done.result == "rejected" and "follows-invalid" in codes(done)
