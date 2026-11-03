"""The `init` operation: files, no overwriting, profile differences, and a working result."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

import pytest
from project_helpers import git, write

from ggsad.core.cli import main
from ggsad.core.init_project import InitOptions, init_project
from ggsad.core.operations import Envelope
from ggsad.core.project import BRIEF_PATH, CONFIG_PATH, brief_profile, load_settings

AT = "2026-11-03T10:00:00Z"


def listed(done: Envelope, key: str) -> list[str]:
    return cast("list[str]", done.data[key])


DEFAULT = InitOptions("lean", "demo", "human:ada")


def options(**fields: Any) -> InitOptions:
    return replace(DEFAULT, **fields)


@pytest.fixture
def folder(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    return tmp_path


def test_init_creates_the_configuration_the_brief_and_the_templates(folder: Path) -> None:
    done = init_project(folder, options())
    assert done.result == "success" and done.changed and done.problems() == []
    created = set(listed(done, "created"))
    assert {CONFIG_PATH, BRIEF_PATH, "docs/constitution.md"} <= created
    assert ".ggsad/templates/change.yaml" in created and "specs/example/change.yaml" in created
    assert "docs/architecture.md" not in created
    settings, issues = load_settings(folder)
    assert settings is not None and issues == ()
    assert brief_profile(folder) == "lean"


def test_a_stricter_profile_creates_the_four_documents(folder: Path) -> None:
    done = init_project(folder, options(profile="standard"))
    created = set(listed(done, "created"))
    assert {"docs/architecture.md", "docs/roadmap.md"} <= created


def test_init_never_overwrites_a_file(folder: Path) -> None:
    write(folder, "docs/constitution.md", "my rules\n")
    done = init_project(folder, options())
    assert "docs/constitution.md" in listed(done, "skipped")
    assert (folder / "docs/constitution.md").read_text() == "my rules\n"


def test_a_second_init_changes_nothing(folder: Path) -> None:
    init_project(folder, options())
    again = init_project(folder, options())
    assert again.result == "success" and not again.changed
    assert listed(again, "created") == []


def test_a_profile_that_differs_from_the_configuration_writes_nothing(folder: Path) -> None:
    init_project(folder, options())
    done = init_project(folder, options(profile="governed"))
    assert done.result == "rejected" and [i.code for i in done.issues] == ["profile-mismatch"]
    assert not done.changed and not (folder / "docs/roadmap.md").exists()


def test_a_brief_that_differs_from_the_configuration_is_reported(folder: Path) -> None:
    write(folder, BRIEF_PATH, "Compliance profile: governed\n")
    done = init_project(folder, options())
    assert done.result == "rejected" and "profile-mismatch" in [i.code for i in done.issues]
    assert not (folder / CONFIG_PATH).exists()


@pytest.mark.parametrize(
    ("fields", "code"),
    [
        ({"profile": "nope"}, "profile-invalid"),
        ({"team_mode": "crowd"}, "team-mode-invalid"),
        ({"project_id": " "}, "project-id-missing"),
        ({"owner": "ada"}, "owner-invalid"),
        ({"requestors": ("builder",)}, "requestor-invalid"),
    ],
)
def test_bad_options_write_nothing(folder: Path, fields: dict[str, Any], code: str) -> None:
    done = init_project(folder, options(**fields))
    assert done.result == "rejected" and code in [i.code for i in done.issues]
    assert not (folder / ".ggsad").exists()


def test_a_failed_write_leaves_nothing_behind(folder: Path) -> None:
    (folder / "specs").write_text("a file where a folder must go", encoding="utf-8")
    done = init_project(folder, options())
    assert done.result == "error" and not done.changed
    assert not (folder / CONFIG_PATH).exists()


def test_the_cli_sets_up_a_project_that_works(
    folder: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    def run(*argv: str) -> int:
        return main([*argv, "--root", str(folder)], clock=lambda: AT)

    assert run("init", "--profile", "lean", "--owner", "human:ada") == 0
    assert "init: success" in capsys.readouterr().out
    assert run("new", "example", "--actor", "agent:assistant") == 0
    capsys.readouterr()
    assert run("check", "example", "--json") == 0
    report = json.loads(capsys.readouterr().out)["data"]["report"]
    assert report["state"] == "open"
    assert run("init", "--profile", "governed") == 1


def test_the_cli_uses_the_folder_name_and_the_git_user(
    folder: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GGSAD_ACTOR", raising=False)
    git(folder, "config", "user.name", "bo")
    assert main(["init", "--profile", "lean", "--root", str(folder)], clock=lambda: AT) == 0
    settings, _ = load_settings(folder)
    assert settings is not None
    assert settings.project_id == folder.name and settings.owner == "human:bo"
