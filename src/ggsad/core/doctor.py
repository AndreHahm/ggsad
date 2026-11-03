"""The `doctor` operation: a read-only health check of the whole project.

It checks the project setup, the tools and the environment, and every change that has a history,
and it names the command that fixes each problem. It writes nothing, runs no gate command, and
fixes nothing itself. The result is `success` when nothing is wrong and `rejected` otherwise;
warnings never change the result.

Interpretations fixed here (listed in the pull request):
- a change without a state document is not checked: it has not been created yet;
- a closed change is checked for its history and its anchor only, because later work in the
  repository can no longer violate its scope;
- a missing Git user name is a warning, because `--actor` or `GGSAD_ACTOR` can name the actor.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.git_scope import GitError, run_git
from ggsad.core.issues import Issue
from ggsad.core.loader import existing_ids, load_change
from ggsad.core.operations import Envelope
from ggsad.core.project import (
    BRIEF_PATH,
    brief_profile,
    load_settings,
    missing_documents,
    profile_issue,
)
from ggsad.core.reports import run_read_only
from ggsad.core.runner import CommandRunner
from ggsad.core.state_store import STATE_FILE
from ggsad.core.values import text_list

if TYPE_CHECKING:
    from pathlib import Path

    from ggsad.core.anchor import AnchorStore
    from ggsad.core.settings import Settings

PROBLEM: Final = "problem"
WARNING: Final = "warning"
HISTORY_CODES: Final = frozenset(
    {
        "history-inconsistent",
        "anchor-missing",
        "schema-version-mismatch",
        "schema-version-unsupported",
    }
)
FIXES: Final = {
    "git-unavailable": "install Git and run `git init` in the project folder",
    "config-missing": "run `ggsad init --profile <profile>`",
    "profile-mismatch": f"make the line 'Compliance profile:' in {BRIEF_PATH} equal the profile in "
    ".ggsad/config.yaml",
    "brief-profile-missing": f"add the line 'Compliance profile: <profile>' to {BRIEF_PATH}",
    "document-missing": "create it; a template is in .ggsad/templates/",
    "interpreter-missing": "install the interpreter or change `interpreter` in .ggsad/config.yaml",
    "interpreter-in-repository": "use an interpreter outside the repository",
    "actor-unknown": "set GGSAD_ACTOR, run `git config user.name`, or pass --actor",
    "tool-missing": "install the program or remove it from required_tools of the change",
    "anchor-missing": "a human runs `ggsad adopt {id}`",
    "migration-required": "run `ggsad migrate {id}`; the old state.yaml stays as it is",
    "history-inconsistent": "the Owner runs `ggsad repair {id} --show`, then `ggsad repair {id} "
    "--reason <why>`",
    "gates-changed": "a human approves them again with `ggsad approve {id} gates`, or cancels "
    "the change",
    "approval-stale": "a human approves the changed document again: `ggsad approve {id} spec` "
    "or `ggsad approve {id} documents`",
    "scope-violation": "undo the changes outside the allowed paths, or amend the gates",
    "hard-failure-active": "see `ggsad check {id}`",
    "schema-version-unsupported": "use a version of ggsad that supports this file",
    "schema-version-mismatch": "restore the file from version control; do not edit schema_version",
    "definition-missing": "restore specs/{id}/change.yaml from version control",
}


@dataclass(frozen=True)
class Finding:
    """One thing the doctor found, with the way to fix it."""

    severity: str
    category: str
    code: str
    message: str
    fix: str

    def to_json(self) -> dict[str, str]:
        """The finding as a JSON object."""
        return {
            "severity": self.severity,
            "category": self.category,
            "code": self.code,
            "message": self.message,
            "fix": self.fix,
        }


def _finding(severity: str, category: str, code: str, message: str, change_id: str = "") -> Finding:
    fix = FIXES.get(code, "see the message").format(id=change_id)
    return Finding(severity, category, code, message, fix)


# ------------------------------------------------------------------ setup


def _setup(root: Path) -> tuple[Settings | None, list[Finding]]:
    found: list[Finding] = []
    try:
        run_git(root, "rev-parse", "--git-dir")
    except GitError as error:
        found.append(
            _finding(PROBLEM, "setup", "git-unavailable", f"Git cannot be used here: {error}")
        )
    settings, issues = load_settings(root)
    found.extend(_finding(PROBLEM, "setup", i.code, i.message) for i in issues)
    if settings is None:
        return None, found
    found.extend(_documents(root, settings))
    return settings, found


def _documents(root: Path, settings: Settings) -> list[Finding]:
    found: list[Finding] = []
    mismatch = profile_issue(root, settings)
    if mismatch is not None:
        found.append(_finding(PROBLEM, "setup", mismatch.code, mismatch.message))
    if (root / BRIEF_PATH).is_file() and brief_profile(root) is None:
        message = f"{BRIEF_PATH} does not state the compliance profile"
        found.append(_finding(WARNING, "setup", "brief-profile-missing", message))
    found.extend(
        _finding(PROBLEM, "setup", "document-missing", f"the required document {path} is missing")
        for path in missing_documents(root, settings.compliance_profile)
    )
    return found


# ------------------------------------------------------------ environment


def _actor_known(root: Path) -> bool:
    if os.environ.get("GGSAD_ACTOR"):
        return True
    try:
        return bool(run_git(root, "config", "user.name", ok=(0, 1)).strip())
    except GitError:
        return False


def _environment(root: Path, settings: Settings) -> list[Finding]:
    runner = CommandRunner(root, (), settings.interpreter)
    found: list[Finding] = []
    if not runner.program_exists(runner.interpreter_program()):
        message = f"the interpreter {runner.interpreter_program()!r} cannot be found"
        found.append(_finding(PROBLEM, "environment", "interpreter-missing", message))
    inside = runner.interpreter_warning()
    if inside is not None:
        found.append(_finding(WARNING, "environment", "interpreter-in-repository", inside))
    if not _actor_known(root):
        message = "no actor is set: GGSAD_ACTOR is empty and Git has no user.name"
        found.append(_finding(WARNING, "environment", "actor-unknown", message))
    return found


def _tools(root: Path, settings: Settings, change_id: str, tools: list[str]) -> list[Finding]:
    runner = CommandRunner(root, tools, settings.interpreter)
    return [
        _finding(
            WARNING,
            f"change {change_id}",
            "tool-missing",
            f"the program {tool!r} is missing",
            change_id,
        )
        for tool in tools
        if not runner.program_exists(tool)
    ]


# ---------------------------------------------------------------- changes


def _kept(code: str, *, closed: bool) -> bool:
    return not closed or code in HISTORY_CODES


def _guard_findings(
    root: Path, change_id: str, anchors: AnchorStore, now: str, *, closed: bool
) -> list[Finding]:
    guard = run_read_only(root, change_id, "guard", now, anchors)
    return [
        _finding(PROBLEM, f"change {change_id}", i.code, i.message, change_id)
        for i in guard.issues
        if _kept(i.code, closed=closed)
    ]


def _change(
    root: Path, settings: Settings, change_id: str, anchors: AnchorStore, now: str
) -> list[Finding]:
    loaded = load_change(root, settings, change_id, anchors)
    if loaded.problems:
        category = f"change {change_id}"
        return [_finding(PROBLEM, category, i.code, i.message, change_id) for i in loaded.problems]
    closed = loaded.state is not None and loaded.state.closed
    found = _guard_findings(root, change_id, anchors, now, closed=closed)
    if closed:
        return found
    tools = text_list((loaded.definition or {}).get("required_tools")) or []
    return found + _tools(root, settings, change_id, tools)


def _changes(root: Path, settings: Settings, anchors: AnchorStore, now: str) -> list[Finding]:
    found: list[Finding] = []
    for change_id in existing_ids(root):
        folder = root / "specs" / change_id
        if (folder / STATE_FILE).is_file() or (folder / "state.yaml").is_file():
            found.extend(_change(root, settings, change_id, anchors, now))
    return found


# ------------------------------------------------------------------ doctor


def run_doctor(root: Path, now: str, anchors: AnchorStore | None = None) -> Envelope:
    """Check the project, the environment, and every change. Read-only."""
    settings, findings = _setup(root)
    if settings is not None:
        findings.extend(_environment(root, settings))
        findings.extend(_changes(root, settings, anchors or GitAnchorStore(root), now))
    problems = [f for f in findings if f.severity == PROBLEM]
    data = {"findings": [f.to_json() for f in findings], "problems": len(problems)}
    if not problems:
        return Envelope("doctor", "success", False, data=data)
    issues = tuple(Issue(f.code, f"{f.category}: {f.message}") for f in problems)
    return Envelope("doctor", "rejected", False, issues=issues, data=data)
