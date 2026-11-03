"""The `new` operation: write `change.yaml` and a `spec.md` stub from a template, then record it.

A file that already exists is kept and used, so a change definition written by hand works too.
When the action is not accepted, the files this call created are removed again, so a refusal
leaves nothing behind (Section 22.3).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Final

from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.identifiers import check_identifier
from ggsad.core.issues import Issue
from ggsad.core.loader import DEFINITION_FILE, SPEC_FILE, change_path
from ggsad.core.operations import Envelope, failure, open_project, run_action

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

    from ggsad.core.anchor import AnchorStore
    from ggsad.core.engine_types import Request

CONFLICT_STUB: Final = "Conflicts with higher documents: none"


@dataclass(frozen=True)
class NewFields:
    """What the template needs besides the identifier and the profile."""

    problem: str
    done_when: Sequence[str]
    owner: str
    author: str


def definition_text(change_id: str, profile: str, fields: NewFields) -> str:
    """The text of a new `change.yaml`. Strings are written as JSON, which YAML reads as is."""
    quote = json.dumps
    done = ", ".join(quote(sentence) for sentence in fields.done_when)
    return (
        'schema_version: "1.0"\n'
        f"id: {quote(change_id)}\n"
        "method_profile: core\n"
        f"compliance_profile: {quote(profile)}\n"
        f"author: {quote(fields.author)}\n"
        f"owner: {quote(fields.owner)}\n"
        "goal:\n"
        f"  problem: {quote(fields.problem)}\n"
        f"  done_when: [{done}]\n"
        "  non_goals: []\n"
        '# Paths this change may touch, for example: allow: ["src/"]\n'
        "scope:\n"
        "  allow: []\n"
        "# One requirement per sentence; add examples and evidence commands before approval.\n"
        "requirements:\n"
        f"{_requirements(fields.done_when)}"
        "gates:\n"
        "  fail: []\n"
        "  wait: []\n"
        "  done: []\n"
    )


def _requirements(sentences: Sequence[str]) -> str:
    quote = json.dumps
    return "".join(
        f"  - id: R{number}\n"
        f"    text: {quote(sentence)}\n"
        '    examples: ["Given ..., when ..., then ..."]\n'
        f"    done_when: [{quote(sentence)}]\n"
        for number, sentence in enumerate(sentences, start=1)
    )


def spec_text(change_id: str, fields: NewFields) -> str:
    """The text of a new `spec.md`: it carries the conflict line a human confirms (Section 4.1)."""
    return f"# Specification: {change_id}\n\nProblem: {fields.problem}\n\n{CONFLICT_STUB}\n"


def _inside(root: Path, directory: Path) -> bool:
    """True when the folder of a change, links resolved, lies below `specs` of the project."""
    return directory.resolve().is_relative_to((root / "specs").resolve())


def _write_new(path: Path, text: str, created: list[Path]) -> None:
    if path.exists():
        return
    path.write_text(text, encoding="utf-8", newline="\n")
    created.append(path)


def _undo(created: list[Path], directory: Path, *, made_directory: bool) -> None:
    for path in created:
        path.unlink(missing_ok=True)
    if made_directory and directory.exists() and not any(directory.iterdir()):
        directory.rmdir()
        if not any(directory.parent.iterdir()):
            directory.parent.rmdir()


def create_change(
    root: Path,
    change_id: str,
    request: Request,
    fields: NewFields,
    anchors: AnchorStore | None = None,
) -> Envelope:
    """Create a change from the template and record the action `new`."""
    settings, issues = open_project(root)
    if settings is None:
        return failure("new", issues)
    invalid = check_identifier(change_id)
    if invalid:
        return failure("new", tuple(invalid))
    directory = change_path(root, change_id)
    if not _inside(root, directory):
        text = f"the folder of {change_id!r} leads outside the project"
        return failure("new", (Issue("path-outside-project", text),))
    if (directory / "state.json").exists():
        return run_action(root, change_id, request, anchors)
    made_directory = not directory.exists()
    created: list[Path] = []
    try:
        directory.mkdir(parents=True, exist_ok=True)
        text = definition_text(change_id, settings.compliance_profile, fields)
        _write_new(directory / DEFINITION_FILE, text, created)
        _write_new(directory / SPEC_FILE, spec_text(change_id, fields), created)
        done = run_action(root, change_id, request, anchors or GitAnchorStore(root))
    except OSError as error:
        _undo(created, directory, made_directory=made_directory)
        return failure(
            "new", (Issue("state-write-failed", f"the files cannot be written: {error}"),)
        )
    if done.result != "success":
        _undo(created, directory, made_directory=made_directory)
    return done
