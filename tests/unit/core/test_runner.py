"""The real command runner: AE-065 (no shell), AE-066 (the interpreter token), required_tools."""

from __future__ import annotations

import sys
from pathlib import Path

from engine_helpers import (
    active,
    check_gate,
    context,
    definition,
    do,
    evidence_requirement,
    req,
)

from ggsad.core.baseline import compare
from ggsad.core.checks import run_command
from ggsad.core.gate_model import CommandSpec, ExitMap, ExtractRule, RunOutcome
from ggsad.core.runner import CommandRunner

PY = sys.executable
OK = ExitMap(frozenset({0}), frozenset({1}))


def runner(tmp_path: Path, tools: set[str] | None = None, interpreter: str | None = None):
    return CommandRunner(tmp_path, tools, interpreter)


def test_ae065_shell_syntax_is_an_ordinary_character(tmp_path: Path) -> None:
    code = "import sys; print(sys.argv[1])"
    run = runner(tmp_path)(("@interpreter", "-c", code, "a; echo done > x.txt"), None)
    assert run.kind == "exit" and run.status == 0
    assert run.stdout.strip() == "a; echo done > x.txt"
    assert not (tmp_path / "x.txt").exists()


def test_ae066_the_token_stands_for_the_configured_interpreter_and_the_record_names_it(
    tmp_path: Path,
) -> None:
    run = runner(tmp_path, interpreter=PY)(("@interpreter", "-c", "pass"), None)
    assert run.status == 0 and run.ran == PY
    spec = CommandSpec(("@interpreter", "-c", "pass"), OK)
    outcome, _ = run_command("done", spec, runner(tmp_path, interpreter=PY))
    assert outcome.result == "satisfied" and PY in outcome.detail


def test_without_a_configured_interpreter_the_token_is_the_python_that_runs_the_tool(
    tmp_path: Path,
) -> None:
    run = runner(tmp_path)(("@interpreter", "-c", "pass"), None)
    assert run.status == 0 and run.ran == PY


def test_a_configured_interpreter_that_is_missing_is_a_missing_approved_program(
    tmp_path: Path,
) -> None:
    run = runner(tmp_path, interpreter="no-such-interpreter-xyz")(("@interpreter", "x"), None)
    assert run.kind == "cannot-start" and run.program_missing
    assert run.ran == "no-such-interpreter-xyz"


def test_a_program_that_is_not_on_required_tools_cannot_start_and_is_not_missing(
    tmp_path: Path,
) -> None:
    for tools in (None, {"other"}):
        run = runner(tmp_path, tools)(("git", "--version"), None)
        assert run.kind == "cannot-start" and not run.program_missing
        assert "required_tools" in run.cause


def test_an_approved_program_that_is_missing_is_reported_as_missing(tmp_path: Path) -> None:
    run = runner(tmp_path, {"no-such-tool-xyz"})(("no-such-tool-xyz",), None)
    assert run.kind == "cannot-start" and run.program_missing


def test_an_approved_program_runs_and_its_output_is_kept(tmp_path: Path) -> None:
    run = runner(tmp_path, {"git"})(("git", "--version"), None)
    assert run.kind == "exit" and run.status == 0 and "git version" in run.stdout


def test_the_exit_status_stdout_and_stderr_are_reported(tmp_path: Path) -> None:
    code = "import sys; print('FAILED a'); print('oops', file=sys.stderr); sys.exit(3)"
    run = runner(tmp_path)(("@interpreter", "-c", code), None)
    assert (run.kind, run.status) == ("exit", 3)
    assert "FAILED a" in run.stdout and "oops" in run.stderr


def test_a_command_over_its_time_limit_is_stopped_and_reported(tmp_path: Path) -> None:
    run = runner(tmp_path)(("@interpreter", "-c", "import time; time.sleep(30)"), 1)
    assert run.kind == "timeout"


def test_the_command_runs_from_the_root_of_the_repository(tmp_path: Path) -> None:
    run = runner(tmp_path)(("@interpreter", "-c", "import os; print(os.getcwd())"), None)
    assert Path(run.stdout.strip()).resolve() == tmp_path.resolve()


def test_a_program_that_exists_but_cannot_start_is_not_satisfied_for_a_done_gate(
    tmp_path: Path,
) -> None:
    broken = tmp_path / "broken.exe"
    broken.write_bytes(b"not a program")
    broken.chmod(0o755)
    spec = CommandSpec((str(broken),), OK)
    outcome, run = run_command("done", spec, runner(tmp_path, {str(broken)}))
    assert run is not None and run.kind == "cannot-start" and not run.program_missing
    assert outcome.result == "not_satisfied"
    fail_outcome, _ = run_command("fail", spec, runner(tmp_path, {str(broken)}))
    assert fail_outcome.result == "not_evaluable"


def test_the_interpreter_inside_the_repository_is_warned_about(tmp_path: Path) -> None:
    inside = CommandRunner(Path(PY).resolve().parent, None, None)
    assert inside.interpreter_warning() is not None
    assert runner(tmp_path).interpreter_warning() is None
    assert runner(tmp_path, interpreter="no-such-interpreter-xyz").interpreter_warning() is None


def test_the_engine_closes_a_change_with_the_real_runner(tmp_path: Path) -> None:
    gates = definition(done=[check_gate("tests-pass", "@interpreter")])
    gates["done"][0]["command"] = ["@interpreter", "-c", "pass"]
    requirement = evidence_requirement("@interpreter")
    requirement["evidence"][0]["command"] = ["@interpreter", "-c", "pass"]
    ctx = context(gates, requirements=[requirement])
    result = do(active(), req("close"), ctx, run=runner(tmp_path))
    assert result.state.outcome == "done"
    assert "ran " in str(result.bodies[0]["gate_detail"])


def test_output_over_the_cap_is_marked_truncated_and_a_baseline_cannot_pass_on_it(
    tmp_path: Path,
) -> None:
    code = "print('FAILED old'); print('x' * 1_100_000); print('FAILED new')"
    run = runner(tmp_path)(("@interpreter", "-c", code), None)
    assert run.truncated and "FAILED old" in run.stdout and "FAILED new" not in run.stdout
    rule = ExtractRule(r"^FAILED (\S+)")
    assert compare(["old"], rule, run).result == "not_evaluable"
    seen = RunOutcome("exit", status=1, stdout="FAILED new", truncated=True)
    assert compare(["old"], rule, seen).result == "not_satisfied"  # a new failure is certain


def test_a_program_that_exists_but_is_not_executable_is_not_a_missing_program(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / "approved-tool").write_text("not a program", encoding="utf-8")
    (tmp_path / "approved-tool").chmod(0o644)
    monkeypatch.setenv("PATH", str(tmp_path))
    run = runner(tmp_path, {"approved-tool"})(("approved-tool",), None)
    assert run.kind == "cannot-start" and not run.program_missing
    assert "not executable" in run.cause


def test_a_relative_program_path_is_resolved_from_the_repository_root(
    tmp_path: Path, monkeypatch, tmp_path_factory
) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    script = scripts / "check.cmd" if sys.platform == "win32" else scripts / "check"
    script.write_text("exit 0\n" if sys.platform == "win32" else "#!/bin/sh\nexit 0\n")
    script.chmod(0o755)
    monkeypatch.chdir(tmp_path_factory.mktemp("elsewhere"))
    run = runner(tmp_path, {"scripts/check"})(("scripts/check",), None)
    assert run.kind == "exit" and run.status == 0


def test_a_command_without_a_time_limit_gets_the_default_limit(tmp_path: Path) -> None:
    bounded = CommandRunner(tmp_path, default_time_limit=1)
    run = bounded(("@interpreter", "-c", "import time; time.sleep(30)"), None)
    assert run.kind == "timeout"
    assert CommandRunner(tmp_path).default_time_limit == 1800
