"""The real runner of check commands (Sections 24.2 and 24.10).

A command is an argument list that is run directly: no shell reads it, so a pipe, a redirection, or
a variable in an argument is an ordinary character. The first element is a program of the
`required_tools` list, or the token `@interpreter`, which stands for the interpreter that the
project settings name (or for the Python that runs this tool when they name none). The runner never
searches the project for an interpreter.

`CommandRunner` is the `Runner` that the engine is handed. It reports what happened; the engine
decides what it means. A relative program path is resolved from the repository root, the directory
the command runs in.
"""

from __future__ import annotations

import os
import shutil
import subprocess  # nosec B404 - the runner must start the programs of the gates
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Final

from ggsad.core.gate_model import RunOutcome

if TYPE_CHECKING:
    from collections.abc import Collection

INTERPRETER_MARK: Final = "@interpreter"
MAX_OUTPUT: Final = 1_000_000
DEFAULT_TIME_LIMIT: Final = 1800


def _cap(data: bytes | None) -> tuple[str, bool]:
    """The decoded output, cut at the cap, and whether anything was cut."""
    raw = data or b""
    return raw[:MAX_OUTPUT].decode("utf-8", "replace"), len(raw) > MAX_OUTPUT


@dataclass(frozen=True)
class CommandRunner:
    """Runs the check commands of one change from the root of the repository."""

    root: Path
    required_tools: Collection[str] | None = None
    interpreter: str | None = None
    default_time_limit: int = DEFAULT_TIME_LIMIT

    def interpreter_program(self) -> str:
        """The program that the token stands for."""
        return self.interpreter or sys.executable

    def _lookup(self, program: str) -> str | None:
        """The executable file for a program name, from the root for a relative path."""
        if os.sep in program or "/" in program:
            return shutil.which(
                program if Path(program).is_absolute() else str(self.root / program)
            )
        return shutil.which(program)

    def _exists_unexecutable(self, program: str) -> bool:
        """True when a file of that name exists but is not an executable program."""
        if os.sep in program or "/" in program:
            return (self.root / program).is_file()
        folders = os.environ.get("PATH", "").split(os.pathsep)
        return any((Path(folder) / program).is_file() for folder in folders if folder)

    def interpreter_warning(self) -> str | None:
        """A warning when the interpreter lives inside the repository (Section 24.10)."""
        found = self._lookup(self.interpreter_program())
        if found is None:
            return None
        if Path(found).resolve().is_relative_to(self.root.resolve()):
            return f"the interpreter {found} lives inside the repository"
        return None

    def __call__(self, command: tuple[str, ...], time_limit: int | None) -> RunOutcome:
        """Run a command and report the exit status, a timeout, or why it could not start."""
        program, ran = command[0], ""
        if program == INTERPRETER_MARK:
            program = self.interpreter_program()
            ran = program
        elif self.required_tools is None or program not in self.required_tools:
            return RunOutcome(
                "cannot-start", cause=f"the program {program!r} is not on the list required_tools"
            )
        found = self._lookup(program)
        if found is None:
            return self._not_found(program, ran)
        return self._run([found, *command[1:]], time_limit or self.default_time_limit, ran)

    def _not_found(self, program: str, ran: str) -> RunOutcome:
        if self._exists_unexecutable(program):
            cause = f"the program {program!r} exists but is not executable"
            return RunOutcome("cannot-start", cause=cause, ran=ran)
        cause = f"the approved program {program!r} is missing"
        return RunOutcome("cannot-start", cause=cause, program_missing=True, ran=ran)

    def _run(self, argv: list[str], time_limit: int, ran: str) -> RunOutcome:
        try:
            # Argument list, no shell; the program was checked against required_tools above.
            done = subprocess.run(  # noqa: S603  # nosec B603  # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-audit.dangerous-subprocess-use-audit
                argv, capture_output=True, check=False, cwd=self.root, timeout=time_limit
            )
        except subprocess.TimeoutExpired:
            return RunOutcome("timeout", cause=f"stopped after {time_limit} seconds", ran=ran)
        except OSError as error:
            return RunOutcome("cannot-start", cause=f"cannot start {argv[0]!r}: {error}", ran=ran)
        if done.returncode < 0:
            cause = f"ended by signal {-done.returncode}"
            return RunOutcome("no-status", cause=cause, ran=ran)
        out, out_cut = _cap(done.stdout)
        err, err_cut = _cap(done.stderr)
        return RunOutcome(
            "exit",
            status=done.returncode,
            stdout=out,
            stderr=err,
            ran=ran,
            truncated=out_cut or err_cut,
        )
