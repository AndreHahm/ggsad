"""The doctor: a read-only health check of the project, the environment, and every change."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from project_helpers import ADA, CONFIG, FIELDS, FULL, git, make_change, req, settle, write

from ggsad.core.cli import main
from ggsad.core.doctor import run_doctor
from ggsad.core.new_change import create_change
from ggsad.core.operations import Envelope, run_action

NOW = "2026-11-03T12:00:00Z"
STRICT = CONFIG + "minimum_levels: {sign_off: A2}\n"


def findings(done: Envelope) -> list[dict[str, str]]:
    return cast("list[dict[str, str]]", done.data["findings"])


def problems(done: Envelope) -> list[tuple[str, str]]:
    return [(f["code"], f["fix"]) for f in findings(done) if f["severity"] == "problem"]


def codes(done: Envelope, severity: str = "problem") -> list[str]:
    return [f["code"] for f in findings(done) if f["severity"] == severity]


def test_a_healthy_project_passes(root: Path) -> None:
    make_change(root)
    done = run_doctor(root, NOW)
    assert done.result == "success" and not done.changed and done.data["problems"] == 0, problems(
        done
    )


def test_a_folder_without_a_project_says_how_to_start(tmp_path: Path) -> None:
    done = run_doctor(tmp_path, NOW)
    assert done.result == "rejected" and not done.changed
    assert ("config-missing", "run `ggsad init --profile <profile>`") in problems(done)
    assert "git-unavailable" in codes(done)


def test_a_brief_that_differs_from_the_config_is_a_problem(root: Path) -> None:
    write(root, "docs/project-brief.md", "Compliance profile: governed\n")
    assert "profile-mismatch" in codes(run_doctor(root, NOW))


def test_a_brief_without_a_profile_line_is_a_warning(root: Path) -> None:
    write(root, "docs/project-brief.md", "# Brief\n")
    done = run_doctor(root, NOW)
    assert done.result == "success" and "brief-profile-missing" in codes(done, "warning")


def test_missing_required_documents_are_problems(root: Path) -> None:
    write(root, ".ggsad/config.yaml", CONFIG.replace("lean", "standard"))
    write(root, "docs/project-brief.md", "Compliance profile: standard\n")
    missing = [
        f["message"] for f in findings(run_doctor(root, NOW)) if f["code"] == "document-missing"
    ]
    assert any("architecture.md" in m for m in missing) and any("roadmap.md" in m for m in missing)


def test_a_missing_interpreter_is_a_problem(root: Path) -> None:
    write(root, ".ggsad/config.yaml", CONFIG + "interpreter: no-such-interpreter-xyz\n")
    assert "interpreter-missing" in codes(run_doctor(root, NOW))


def test_no_actor_is_a_warning(root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GGSAD_ACTOR", raising=False)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(root / "none"))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(root / "none"))
    done = run_doctor(root, NOW)
    assert done.result == "success" and "actor-unknown" in codes(done, "warning")


def test_a_missing_tool_of_a_change_is_a_warning(root: Path) -> None:
    write(root, "specs/c-1/change.yaml", FULL + 'required_tools: ["no-such-tool-xyz"]\n')
    assert create_change(root, "c-1", req("new"), FIELDS).result == "success"
    done = run_doctor(root, NOW)
    assert done.result == "success" and "tool-missing" in codes(done, "warning")


def test_a_history_without_an_anchor_names_the_adopt_command(root: Path) -> None:
    write(root, ".ggsad/config.yaml", STRICT)
    create_change(root, "c-1", req("new"), FIELDS)
    git(root, "update-ref", "-d", "refs/ggsad/anchors/c-1")
    done = run_doctor(root, NOW)
    assert ("anchor-missing", "a human runs `ggsad adopt c-1`") in problems(done)


def test_edited_gates_name_the_reapproval(root: Path) -> None:
    make_change(root)
    settle(root)
    run_action(root, "c-1", req("approve", ADA, target="all"))
    write(root, "specs/c-1/change.yaml", FULL.replace("lib/**", "src/**"))
    fixes = dict(problems(run_doctor(root, NOW)))
    assert "ggsad approve c-1 gates" in fixes["gates-changed"]


def test_a_damaged_history_names_the_repair_command(root: Path) -> None:
    make_change(root)
    run_action(root, "c-1", req("ask", text="One?"))
    path = root / "specs/c-1/state.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["entries"] = document["entries"][:1]
    path.write_text(json.dumps(document), encoding="utf-8")
    fixes = dict(problems(run_doctor(root, NOW)))
    assert "ggsad repair c-1 --show" in fixes["history-inconsistent"]


def test_a_closed_change_is_not_blamed_for_later_work(root: Path) -> None:
    make_change(root)
    assert run_action(root, "c-1", req("cancel", ADA, reason="not needed")).result == "success"
    write(root, "docs/other.md", "later work\n")
    assert run_doctor(root, NOW).result == "success"


def test_a_folder_without_a_history_is_not_checked(root: Path) -> None:
    write(root, "specs/draft/change.yaml", "anything\n")
    assert run_doctor(root, NOW).result == "success"


def test_a_change_with_an_unusable_definition_is_a_problem(root: Path) -> None:
    make_change(root)
    (root / "specs/c-1/change.yaml").unlink()
    assert "definition-missing" in codes(run_doctor(root, NOW))


def test_the_command_prints_each_problem_with_its_fix(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["doctor", "--root", str(tmp_path)], clock=lambda: NOW) == 1
    out = capsys.readouterr().out
    assert "[problem] setup: config-missing" in out and "fix: run `ggsad init" in out


def test_the_command_json_carries_the_findings(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["doctor", "--json", "--root", str(root)], clock=lambda: NOW) == 0
    envelope: dict[str, Any] = json.loads(capsys.readouterr().out)
    assert envelope["operation"] == "doctor" and envelope["data"]["problems"] == 0
