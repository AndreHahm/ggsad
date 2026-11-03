"""The real runner of check commands (Sections 24.2 and 24.10).

A command is an argument list that is run directly: no shell reads it, so a pipe, a redirection, or
a variable in an argument is an ordinary character. The first element is a program of the
`required_tools` list, or the token `@interpreter`, which stands for the interpreter that the
project settings name (or for the Python that runs this tool when they name none). The runner never
searches the project for an interpreter.

`CommandRunner` is the `Runner` that the engine is handed. It reports what happened; the engine
decides what it means.
"""

from __future__ import annotations

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


def _cap(data: bytes | None) -> str:
    return (data or b"")[:MAX_OUTPUT].decode("utf-8", "replace")


@dataclass(frozen=True)
class CommandRunner:
    """Runs the check commands of one change from the root of the repository."""

    root: Path
    required_tools: Collection[str] | None = None
    interpreter: str | None = None

    def interpreter_program(self) -> str:
        """The program that the token stands for."""
        return self.interpreter or sys.executable

    def interpreter_warning(self) -> str | None:
        """A warning when the interpreter lives inside the repository (Section 24.10)."""
        found = shutil.which(self.interpreter_program())
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
        found = shutil.which(program)
        if found is None:
            return RunOutcome(
                "cannot-start",
                cause=f"the approved program {program!r} is missing",
                program_missing=True,
                ran=ran,
            )
        return self._run([found, *command[1:]], time_limit, ran)

    def _run(self, argv: list[str], time_limit: int | None, ran: str) -> RunOutcome:
        try:
            # Argument list, no shell; the program was checked against required_tools above.
            done = subprocess.run(  # noqa: S603  # nosec B603
                argv, capture_output=True, check=False, cwd=self.root, timeout=time_limit
            )
        except subprocess.TimeoutExpired:
            return RunOutcome("timeout", cause=f"stopped after {time_limit} seconds", ran=ran)
        except OSError as error:
            return RunOutcome("cannot-start", cause=f"cannot start {argv[0]!r}: {error}", ran=ran)
        if done.returncode < 0:
            cause = f"ended by signal {-done.returncode}"
            return RunOutcome("no-status", cause=cause, ran=ran)
        return RunOutcome(
            "exit",
            status=done.returncode,
            stdout=_cap(done.stdout),
            stderr=_cap(done.stderr),
            ran=ran,
        )
