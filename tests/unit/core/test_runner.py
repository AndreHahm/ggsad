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

from ggsad.core.checks import run_command
from ggsad.core.gate_model import CommandSpec, ExitMap
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
