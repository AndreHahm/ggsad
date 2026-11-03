"""Build the example projects in `examples/` with the real `ggsad` command line.

Each example is created in a scratch Git repository by running `ggsad init`, `new`, `approve`,
`start`, `close`, and `ask`, with a fixed clock and fixed identities. Git commit hashes (recorded
at `start`) differ from run to run, so a rebuild changes the history files. The record files are
copied to `examples/<name>/` (no `.git` folder).

Run from the repository root:

    uv run python scripts/build_examples.py

A test (`tests/unit/core/test_examples.py`) copies each example, makes it a Git repository again,
and checks it with `ggsad doctor`, so the examples cannot drift from the tool.
"""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import NoReturn

from ggsad.core.cli import main

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
START = datetime(2026, 1, 12, 9, 0, tzinfo=UTC)


@dataclass(frozen=True)
class Example:
    """One example project: who works in it, and what the two changes are."""

    name: str
    profile: str
    team_mode: str
    owner: str
    approver: str
    humans: tuple[tuple[str, str], ...]
    problem: str
    outcome: str


@dataclass(frozen=True)
class Change:
    """A change definition in the example."""

    identifier: str
    problem: str
    sentence: str
    folder: str
    example: str


EXAMPLE_LIST = (
    Example(
        "lean-startup",
        "lean",
        "team",
        "human:ada",
        "human:ada",
        (("human:ada", "ada-gh"),),
        "Small teams lose customers because password resets need a support ticket.",
        "A user resets a password without help from the team.",
    ),
    Example(
        "solo-developer",
        "standard",
        "solo",
        "human:sam",
        "human:sam",
        (("human:sam", "sam-gh"),),
        "One developer keeps a notes app and wants exports without hand-made copies.",
        "A user exports all notes in one step.",
    ),
    Example(
        "governed-enterprise",
        "governed",
        "team",
        "human:ada",
        "human:grace",
        (("human:ada", "ada-gh"), ("human:grace", "grace-gh")),
        "Support staff cannot see who changed a customer record, which audits require.",
        "Every change of a customer record shows who made it and when.",
    ),
)


OPEN_CHANGES = {
    "lean-startup": Change(
        "reset-mail-text",
        "The reset mail is hard to understand.",
        "The reset mail tells the user in one sentence what to do next.",
        "mail",
        "reset_mail",
    ),
    "solo-developer": Change(
        "export-formats",
        "Some people want the export as a spreadsheet, not as text.",
        "A user can choose a spreadsheet file for the export.",
        "formats",
        "export_formats",
    ),
    "governed-enterprise": Change(
        "audit-filter",
        "The list of changes of a record is too long to read.",
        "A person can filter the list of changes by date.",
        "filter",
        "audit_filter",
    ),
}
FINISHED_CHANGES = {
    "lean-startup": ("reset-password", "reset", "reset_password"),
    "solo-developer": ("export-notes", "export", "export_notes"),
    "governed-enterprise": ("audit-trail", "audit", "audit_trail"),
}


def changes_of(example: Example) -> tuple[Change, Change]:
    """The finished change and the open change of an example."""
    identifier, folder, module = FINISHED_CHANGES[example.name]
    finished = Change(identifier, example.problem, example.outcome, folder, module)
    return finished, OPEN_CHANGES[example.name]


class Scratch:
    """A scratch repository with a fixed clock; it runs `ggsad` in the process."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.step = 0

    def clock(self) -> str:
        self.step += 1
        return (START + timedelta(minutes=5 * self.step)).strftime("%Y-%m-%dT%H:%M:%SZ")

    def git(self, *args: str) -> None:
        subprocess.run(  # noqa: S603  # nosec B603
            ["git", "-c", "commit.gpgsign=false", *args],  # noqa: S607  # nosec B607
            cwd=self.root,
            check=True,
            capture_output=True,
        )

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def ggsad(self, *argv: str) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main([*argv, "--root", str(self.root)], clock=self.clock)
        if code != 0:
            stop(f"ggsad {' '.join(argv)} failed ({code}):\n{out.getvalue()}")

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def stop(message: str) -> NoReturn:
    raise SystemExit(message)


def quote(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def definition(example: Example, change: Change) -> str:
    """The full `change.yaml`: one requirement with an example and an evidence command."""
    done = change.sentence
    return (
        'schema_version: "1.0"\n'
        f"id: {quote(change.identifier)}\n"
        "method_profile: core\n"
        f"compliance_profile: {quote(example.profile)}\n"
        f"author: {quote(example.owner)}\n"
        f"owner: {quote(example.owner)}\n"
        f"approver: {quote(example.approver)}\n"
        "goal:\n"
        f"  problem: {quote(change.problem)}\n"
        f"  done_when: [{quote(done)}]\n"
        "  non_goals: []\n"
        "scope:\n"
        f'  allow: ["src/{change.folder}/"]\n'
        "required_tools: [git]\n"
        "requirements:\n"
        "  - id: R1\n"
        f"    text: {quote(done)}\n"
        '    examples: ["Given a person who needs it, when they ask, then it happens"]\n'
        f"    done_when: [{quote(done)}]\n"
        "    evidence:\n"
        '      - command: ["git", "ls-files", "--error-unmatch",'
        f' "src/{change.folder}/{change.example}.py"]\n'
        "        exit_map: {satisfied: [0], not_satisfied: [1]}\n"
        "gates:\n"
        "  fail: []\n"
        "  wait: []\n"
        "  done: []\n"
    )


def configure(scratch: Scratch, example: Example) -> None:
    """Set the approved humans, and for the governed profile a deputy and minimum levels."""
    path = scratch.root / ".ggsad" / "config.yaml"
    text = path.read_text(encoding="utf-8")
    humans = "".join(
        f'    - {{identity: "{who}", account: {account}}}\n' for who, account in example.humans
    )
    text = text.replace(
        "  # Add the humans who may approve, with their accounts, to turn the list on:\n"
        "  # approved_humans:\n"
        f'  #   - {{identity: "{example.owner}", account: your-account}}\n',
        f"  approved_humans:\n{humans}",
    )
    if "approved_humans:\n    -" not in text:
        stop("config template changed: approved_humans block not found")
    if example.profile == "governed":
        text = text.replace(
            "minimum_levels: {}", "minimum_levels: {spec_approval: A1, gate_approval: A1}"
        )
    path.write_text(text, encoding="utf-8", newline="\n")


def project_documents(scratch: Scratch, example: Example) -> None:
    """Short, real text for the brief and the constitution, and stubs for the other documents."""
    name = example.name
    scratch.write(
        "docs/project-brief.md",
        f"# Project brief: {name}\n\nCompliance profile: {example.profile}\n\n"
        f"## Problem\n\n{example.problem}\n\n## Outcomes\n\n{example.outcome}\n\n"
        "## Scope and non-goals\n\nThis is a demonstration project; it holds no real product.\n\n"
        "## Constraints\n\nEvery change goes through the method.\n\n## Method\n\n"
        f"Method profile: core\nOperating mode: {example.team_mode}\n"
        "Integrated methods and tools: none\n",
    )
    scratch.write(
        "docs/constitution.md",
        "# Constitution\n\nNo change may break these rules.\n\n"
        "## Quality\n\nEvery requirement has a check that a command can run.\n\n"
        "## Approvals\n\nA human approves the specification before work starts.\n",
    )
    if example.profile in {"standard", "governed"}:
        scratch.write(
            "docs/architecture.md",
            "# Architecture\n\nOne small program; each change adds a folder under `src/`.\n",
        )
        scratch.write(
            "docs/roadmap.md",
            "# Roadmap\n\nNow: the two changes in `specs/`. Next: nothing planned.\n",
        )


def run_change(scratch: Scratch, example: Example, change: Change, *, finish: bool) -> None:
    """Create, approve, and start a change; then close it, or leave it with an open question."""
    chg = change.identifier
    human = ["--actor", example.approver, "--assurance", "A1", "--account"]
    account = dict(example.humans)[example.approver]
    scratch.ggsad(
        "new",
        chg,
        "--actor",
        "agent:assistant",
        "--problem",
        change.problem,
        "--done-when",
        change.sentence,
    )
    scratch.write(f"specs/{chg}/change.yaml", definition(example, change))
    scratch.write(
        f"specs/{chg}/spec.md",
        f"# Specification: {chg}\n\nProblem: {change.problem}\n\n"
        f"Requirement R1: {change.sentence}\n\nConflicts with higher documents: none\n",
    )
    scratch.commit(f"Define {chg}")
    scratch.ggsad("approve", chg, "all", *human, account, "--yes")
    if not finish:
        ask_question(scratch, chg)
        return
    scratch.ggsad("start", chg, "--actor", "agent:assistant")
    scratch.write(
        f"src/{change.folder}/{change.example}.py",
        f'"""{change.sentence}"""\n\n\ndef run() -> str:\n    return "{change.identifier}"\n',
    )
    scratch.commit(f"Implement {chg}")
    scratch.ggsad("close", chg, *human, account)


def ask_question(scratch: Scratch, chg: str) -> None:
    """The open change waits for a human answer before the work starts."""
    scratch.ggsad(
        "ask",
        chg,
        "--actor",
        "agent:assistant",
        "--text",
        "Which of the two ways of doing this do you prefer?",
    )


def build(example: Example, target: Path) -> None:
    """Build one example in a scratch repository and copy the record files to `target`."""
    with tempfile.TemporaryDirectory() as folder:
        scratch = Scratch(Path(folder))
        scratch.git("init", "-q")
        scratch.git("config", "user.name", "Example Author")
        scratch.git("config", "user.email", "author@example.com")
        scratch.ggsad(
            "init",
            "--profile",
            example.profile,
            "--project-id",
            example.name,
            "--owner",
            example.owner,
            "--team-mode",
            example.team_mode,
        )
        shutil.rmtree(scratch.root / "specs" / "example")
        configure(scratch, example)
        project_documents(scratch, example)
        scratch.commit("Set up the project")
        finished, open_change = changes_of(example)
        run_change(scratch, example, finished, finish=True)
        run_change(scratch, example, open_change, finish=False)
        scratch.commit("Record the open question")
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(scratch.root, target, ignore=shutil.ignore_patterns(".git", "*.lock"))


def clean(target: Path) -> None:
    """Remove the files `git` would not keep: nothing but cache folders."""
    for cache in target.rglob("__pycache__"):
        shutil.rmtree(cache)


def run() -> int:
    for example in EXAMPLE_LIST:
        target = EXAMPLES / example.name
        build(example, target)
        clean(target)
        sys.stdout.write(f"built {target}\n")
    return 0


if __name__ == "__main__":
    sys.exit(run())
