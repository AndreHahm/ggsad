"""Scope measurement against real Git repositories: AE-046 to AE-051, working-copy-unclean."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import ggsad.core.git_scope as module
from ggsad.core.git_scope import (
    GitError,
    changed_paths,
    head_revision,
    measure_scope,
    unclean_paths,
)

CHANGE = "specs/c-1"


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def write(repo: Path, name: str, text: str = "x\n") -> None:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    write(tmp_path, "lib/a.py")
    write(tmp_path, ".gitignore", ".cache/\n")
    write(tmp_path, f"{CHANGE}/spec.md")
    write(tmp_path, f"{CHANGE}/change.yaml")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "base")
    return tmp_path


def test_ae046_a_changed_path_inside_the_scope_is_in_scope(repo: Path) -> None:
    base = head_revision(repo)
    write(repo, "lib/net/client.py")
    assert measure_scope(repo, base, ["lib/**"], CHANGE).result == "not_satisfied"


def test_ae047_a_committed_path_outside_the_scope_is_a_violation(repo: Path) -> None:
    base = head_revision(repo)
    write(repo, "docs/guide.md")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "docs")
    check = measure_scope(repo, base, ["lib/**"], CHANGE)
    assert check.result == "satisfied" and "docs/guide.md" in check.detail


def test_staged_unstaged_and_deleted_paths_are_changed(repo: Path) -> None:
    base = head_revision(repo)
    write(repo, "lib/a.py", "changed\n")
    write(repo, "staged.txt")
    git(repo, "add", "staged.txt")
    (repo / CHANGE / "change.yaml").unlink()
    assert changed_paths(repo, base) == ["lib/a.py", "specs/c-1/change.yaml", "staged.txt"]


def test_ae048_a_file_hidden_by_an_ignore_file_of_the_base_revision_is_invisible(
    repo: Path,
) -> None:
    base = head_revision(repo)
    write(repo, ".cache/tool.py")
    assert changed_paths(repo, base) == []
    assert measure_scope(repo, base, ["lib/**"], CHANGE).result == "not_satisfied"


def test_ae049_outside_ignore_settings_do_not_hide_and_a_new_ignore_file_is_a_path(
    repo: Path,
) -> None:
    base = head_revision(repo)
    info = repo / ".git" / "info"
    info.mkdir(exist_ok=True)
    (info / "exclude").write_text("tools/\n", encoding="utf-8")
    write(repo, "tools/run.sh")
    write(repo, "sub/.gitignore", "build/\n")
    write(repo, "build/out.o")
    paths = changed_paths(repo, base)
    assert "tools/run.sh" in paths and "sub/.gitignore" in paths and "build/out.o" in paths
    assert measure_scope(repo, base, ["lib/**"], CHANGE).result == "satisfied"


def test_a_created_ignore_file_hides_nothing(repo: Path) -> None:
    base = head_revision(repo)
    write(repo, "sub/.gitignore", "build/\n")
    write(repo, "sub/build/out.o")
    assert "sub/build/out.o" in changed_paths(repo, base)


def test_ae050_record_files_are_not_measured_but_other_files_in_the_directory_are(
    repo: Path,
) -> None:
    base = head_revision(repo)
    write(repo, f"{CHANGE}/spec.md", "edited\n")
    write(repo, f"{CHANGE}/state.json")
    write(repo, f"{CHANGE}/notes.md")
    check = measure_scope(repo, base, ["lib/**"], CHANGE)
    assert check.detail == "paths outside the scope: specs/c-1/notes.md"


def test_ae051_interrupted_write_leftovers_are_exempt_and_a_backup_is_not(repo: Path) -> None:
    base = head_revision(repo)
    write(repo, f"{CHANGE}/state.json.tmp")
    write(repo, f"{CHANGE}/state.json.lock")
    assert measure_scope(repo, base, ["lib/**"], CHANGE).result == "not_satisfied"
    write(repo, f"{CHANGE}/state.json.bak")
    assert measure_scope(repo, base, ["lib/**"], CHANGE).result == "satisfied"


def test_a_scope_that_cannot_be_measured_is_not_evaluable(repo: Path, tmp_path_factory) -> None:
    base = head_revision(repo)
    assert measure_scope(repo, None, ["lib/**"], CHANGE).result == "not_evaluable"
    assert measure_scope(repo, base, None, CHANGE).result == "not_evaluable"
    elsewhere = tmp_path_factory.mktemp("notarepo")
    bad = measure_scope(elsewhere, base, ["lib/**"], CHANGE)
    assert bad.result == "not_evaluable" and "unavailable" in bad.detail
    assert measure_scope(repo, "0" * 40, ["lib/**"], CHANGE).result == "not_evaluable"


def test_an_empty_allowed_list_allows_nothing(repo: Path) -> None:
    base = head_revision(repo)
    assert measure_scope(repo, base, [], CHANGE).result == "not_satisfied"
    write(repo, "lib/a.py", "changed\n")
    assert measure_scope(repo, base, [], CHANGE).result == "satisfied"


def test_head_revision_outside_a_repository_raises(tmp_path: Path) -> None:
    with pytest.raises(GitError):
        head_revision(tmp_path)


def test_unclean_paths_ignore_the_record_files(repo: Path) -> None:
    assert unclean_paths(repo, CHANGE) == []
    write(repo, f"{CHANGE}/spec.md", "edited\n")
    write(repo, f"{CHANGE}/state.json")
    assert unclean_paths(repo, CHANGE) == []
    write(repo, "lib/a.py", "dirty\n")
    write(repo, "new.txt")
    assert unclean_paths(repo, CHANGE) == ["lib/a.py", "new.txt"]


def test_a_revision_that_could_be_read_as_an_option_is_refused(repo: Path) -> None:
    for bad in ("--output=x", "-p", "HEAD~1", "main", ""):
        check = measure_scope(repo, bad, ["lib/**"], CHANGE)
        assert check.result == "not_evaluable" and "not a revision" in check.detail
    assert not (repo / "x").exists()


def test_the_ignore_set_is_computed_once_for_many_untracked_files(repo: Path, monkeypatch) -> None:
    calls = []
    original = module._hidden_at_base

    def counting(*args):
        calls.append(1)
        return original(*args)

    monkeypatch.setattr(module, "_hidden_at_base", counting)
    base = head_revision(repo)
    for index in range(20):
        write(repo, f"lib/new{index}.py")
    assert len(changed_paths(repo, base)) == 20
    assert len(calls) == 1


def test_a_git_call_that_does_not_finish_is_not_evaluable(repo: Path, monkeypatch) -> None:
    base = head_revision(repo)

    def hang(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="git", timeout=1)

    monkeypatch.setattr(module.subprocess, "run", hang)
    check = measure_scope(repo, base, ["lib/**"], CHANGE)
    assert check.result == "not_evaluable" and "did not finish" in check.detail


def test_repository_state_variables_of_the_caller_are_not_inherited(
    repo: Path, tmp_path_factory, monkeypatch
) -> None:
    base = head_revision(repo)
    other = tmp_path_factory.mktemp("other")
    git(other, "init", "-q")
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(other))
    monkeypatch.setenv("GIT_INDEX_FILE", str(other / ".git" / "index"))
    write(repo, "lib/new.py")
    assert changed_paths(repo, base) == ["lib/new.py"]
    assert head_revision(repo) == base
