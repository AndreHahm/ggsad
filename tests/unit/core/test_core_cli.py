"""The command line: commands, output, exit codes, and who acts."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from project_helpers import ADA, git, make_change, req, settle, write

from ggsad.core.cli import (
    build_parser,
    build_request,
    find_root,
    main,
    resolve_actor,
)
from ggsad.core.engine_types import Actor
from ggsad.core.operations import run_action

AT = "2026-11-03T10:00:00Z"
NEW = ["new", "c-1", "--problem", "Resets are manual", "--done-when", "Users can reset"]


def run(root: Path, *argv: str, actor: str = "agent:builder") -> int:
    return main([*argv, "--root", str(root), "--actor", actor], clock=lambda: AT)


def approved(root: Path) -> None:
    make_change(root)
    settle(root)
    run_action(root, "c-1", req("approve", ADA, target="all"))


def test_new_creates_the_change_and_exits_with_zero(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(root, *NEW) == 0
    out = capsys.readouterr().out
    assert "new: success (recorded)" in out and "acting as: agent:builder" in out
    assert (root / "specs/c-1/change.yaml").is_file()


def test_json_prints_the_envelope(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(root, *NEW, "--json") == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["operation"] == "new" and envelope["changed"] is True
    assert envelope["state"]["state"] == "open"


def test_a_rejection_exits_with_one_and_names_the_issue(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert run(root, *NEW, actor="agent:stranger") == 1
    assert "requestor-not-approved" in capsys.readouterr().out


def test_an_error_exits_with_two(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run(tmp_path, *NEW) == 2
    assert "config-missing" in capsys.readouterr().out


def test_approve_takes_the_target_and_the_assurance(root: Path) -> None:
    make_change(root)
    settle(root)
    assert run(root, "approve", "c-1", "all", "--yes", actor="human:ada") == 0
    assert run(root, "start", "c-1") == 0


def test_check_prints_the_line_for_the_owner_first(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    approved(root)
    run(root, "start", "c-1")
    capsys.readouterr()
    assert run(root, "ask", "c-1", "--text", "Which text?", "--option", "a", "--option", "b") == 0
    assert run(root, "wait", "c-1", "--question", "Q1") == 0
    capsys.readouterr()
    assert run(root, "check", "c-1") == 0
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "needs you"
    assert "state: waiting" in lines
    assert any("human:ada must act" in line for line in lines)


def test_check_json_carries_the_report(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    approved(root)
    assert run(root, "check", "c-1", "--json") == 0
    report = json.loads(capsys.readouterr().out)["data"]["report"]
    assert report["state"] == "open" and "headline" in report


def test_guard_and_check_scope_are_commands(root: Path) -> None:
    approved(root)
    run(root, "start", "c-1")
    assert run(root, "guard", "c-1") == 0
    assert run(root, "check-scope", "c-1") == 0
    write(root, "docs/other.md", "outside\n")
    assert run(root, "check-scope", "c-1") == 1


def test_an_unreadable_agent_report_is_an_error(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    approved(root)
    assert run(root, "close", "c-1", "--agent-report", str(root / "missing.json")) == 2
    assert "agent-report-invalid" in capsys.readouterr().out
    (root / "list.json").write_text("[1]", encoding="utf-8")
    assert run(root, "close", "c-1", "--agent-report", str(root / "list.json")) == 2


def test_a_missing_required_option_is_a_usage_error(root: Path) -> None:
    with pytest.raises(SystemExit) as caught:
        main(["init", "--root", str(root)], clock=lambda: AT)
    assert caught.value.code == 2


def test_the_request_carries_every_option() -> None:
    args = build_parser().parse_args(
        ["conflict", "c-1", "--text", "t", "--document", "a.md", "--document", "b.md"]
    )
    request = build_request("conflict", args, Actor("agent:x"), AT)
    assert request.documents == ("a.md", "b.md") and request.text == "t"
    answer = build_parser().parse_args(
        ["answer", "c-1", "--question", "Q1", "--answer", "yes", "--and-resume"]
    )
    built = build_request("answer", answer, Actor("human:ada"), AT)
    assert built.and_resume and built.question == "Q1" and built.answer == "yes"
    override = build_parser().parse_args(["approve", "c-1", "override", "--attempts", "2"])
    assert build_request("approve", override, Actor("human:ada"), AT).attempts == 2


def test_the_actor_is_the_option_then_the_variable_then_git(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GGSAD_ACTOR", raising=False)
    git(root, "config", "user.name", "ada")
    assert resolve_actor(None, root, "A0").identity == "human:ada"
    monkeypatch.setenv("GGSAD_ACTOR", "agent:env")
    assert resolve_actor(None, root, "A0").identity == "agent:env"
    assert resolve_actor("agent:option", root, "A1").identity == "agent:option"


def test_the_account_is_read_independently_of_the_claimed_identity(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GGSAD_ACCOUNT", raising=False)
    assert resolve_actor("human:ada", root, "A1") == Actor("human:ada", "A1", None)
    git(root, "config", "github.user", "real-user")
    assert resolve_actor("human:ada", root, "A1").account == "real-user"
    monkeypatch.setenv("GGSAD_ACCOUNT", "env-user")
    assert resolve_actor("human:ada", root, "A1").account == "env-user"
    assert resolve_actor("human:ada", root, "A1", "option-user").account == "option-user"


def test_the_recorded_account_is_the_one_given_not_the_one_on_the_list(root: Path) -> None:
    approved(root)
    assert run(root, "start", "c-1", "--account", "someone-else") == 0
    entries = json.loads((root / "specs/c-1/state.json").read_text(encoding="utf-8"))["entries"]
    assert entries[-1]["body"]["account"] == "someone-else"
    assert run(root, "check", "c-1") == 0


def test_without_any_identity_the_actor_is_unknown(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GGSAD_ACTOR", raising=False)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(tmp_path / "none"))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(tmp_path / "none"))
    assert resolve_actor(None, tmp_path, "A0").identity == "human:unknown"


def test_the_root_is_found_upwards(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    deep = root / "a" / "b"
    deep.mkdir(parents=True)
    monkeypatch.chdir(deep)
    assert find_root(None) == root.resolve()
    assert find_root(str(root)) == root.resolve()


def test_the_root_is_the_current_folder_when_no_project_is_found(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    assert find_root(None) == tmp_path.resolve()


def test_init_without_a_root_uses_the_current_folder_even_inside_a_project(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    inner = root / "sub"
    inner.mkdir()
    monkeypatch.chdir(inner)
    assert main(["init", "--profile", "lean", "--owner", "human:ada"], clock=lambda: AT) == 0
    assert (inner / ".ggsad/config.yaml").is_file()
