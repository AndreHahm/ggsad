"""The command line of GG-SAD: one command per action (Implementation Contract, Section 22).

`ggsad <action> <change-id> [options]`. The message is readable text; `--json` prints the result
envelope instead. The exit code is 0 for `success`, 1 for `rejected` or `blocked`, and 2 for
`error` (or for a command line that cannot be read).

Who acts: `--actor`, else the variable `GGSAD_ACTOR`, else `human:<git user.name>`. The assurance
level is declared with `--assurance` (default A0); this tool cannot verify it. The time of an
entry is the system clock in UTC.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from ggsad.core.approval_summary import build_summary
from ggsad.core.doctor import run_doctor
from ggsad.core.engine_types import Actor, Request
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.git_scope import GitError, run_git
from ggsad.core.identifiers import check_identifier
from ggsad.core.init_project import InitOptions, init_project
from ggsad.core.issues import Issue
from ggsad.core.loader import load_change
from ggsad.core.new_change import NewFields, create_change
from ggsad.core.operations import Envelope, failure, now_utc, run_action
from ggsad.core.project import CONFIG_PATH, load_settings
from ggsad.core.render import render_json, render_text
from ggsad.core.repair import repair_change
from ggsad.core.reports import READ_ONLY, run_read_only
from ggsad.core.settings import PROFILES, TEAM_MODES

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import TextIO

    from ggsad.core.settings import Settings

ACTOR_VARIABLE: Final = "GGSAD_ACTOR"
ACCOUNT_VARIABLE: Final = "GGSAD_ACCOUNT"
TEXT: Final = {"type": str}
FLAGS: Final[dict[str, dict[str, Any]]] = {
    "note": {**TEXT, "help": "a short note recorded with the entry"},
    "reason": {**TEXT, "help": "the reason that is recorded"},
    "text": {**TEXT, "help": "the text of a question, a conflict, or an approval summary"},
    "owner": {**TEXT, "help": "the identity that owns the item, for example human:ada"},
    "question": {**TEXT, "help": "the identifier of a question, for example Q1"},
    "gate": {**TEXT, "help": "the identifier of a gate"},
    "answer": {**TEXT, "help": "the answer to a question"},
    "resume_when": {**TEXT, "help": "the condition that ends a wait"},
    "expires": {**TEXT, "help": "when a wait is overdue, as a UTC time"},
    "replaced_by": {**TEXT, "help": "the open change that replaces this one"},
    "target": {**TEXT, "help": "what to reassign: wait"},
    "attempts": {"type": int, "help": "the further attempts an override grants"},
    "option": {**TEXT, "action": "append", "help": "an option of a structured question"},
    "document": {**TEXT, "action": "append", "help": "a document that conflicts, twice"},
    "and_resume": {"action": "store_true", "help": "resume the change with the answer"},
    "about_spec": {"action": "store_true", "help": "the question is about spec.md"},
    "yes": {"action": "store_true", "help": "record the approval without asking after the summary"},
    "show": {"action": "store_true", "help": "only show what is damaged; write nothing"},
    "agent_report": {**TEXT, "help": "a JSON file with the report of the agent that closes"},
}
ACTIONS: Final[dict[str, tuple[str, ...]]] = {
    "start": ("note",),
    "approve": ("gate", "reason", "attempts", "text", "note", "yes"),
    "wait": ("question", "reason", "owner", "resume_when", "expires", "note"),
    "ask": ("text", "option", "owner", "about_spec"),
    "answer": ("question", "answer", "and_resume", "note"),
    "resume": ("note", "question"),
    "close": ("note", "agent_report"),
    "fail": ("reason", "note"),
    "cancel": ("reason",),
    "supersede": ("replaced_by", "reason"),
    "conflict": ("text", "document", "owner"),
    "handover": ("owner", "reason"),
    "reassign": ("owner", "reason", "question", "target"),
    "adopt": ("note",),
    "repair": ("reason", "show", "note"),
}
HELP: Final = {
    "new": "create a change from a template and record it",
    "approve": "record an approval; the target is spec, gates, review, documents, all, gate, "
    "or override",
    "start": "start an open change",
    "wait": "pause an active change",
    "ask": "record a question",
    "answer": "answer a question",
    "resume": "resume a waiting change",
    "close": "evaluate the done gates and close the change",
    "fail": "close a waiting change as failed",
    "cancel": "cancel a change",
    "supersede": "cancel a change that another change replaces",
    "conflict": "record a conflict between two documents",
    "handover": "hand a change over to a new Change owner",
    "reassign": "reassign the owner of a question or a wait",
    "adopt": "create the anchor of a history that has none",
    "repair": "replace a damaged history by its consistent part (the Owner, with a reason)",
    "check": "report on a change: the status report",
    "review": "check review.md",
    "guard": "verify the record of a change without running any command",
    "check-scope": "report paths changed outside the allowed list",
}


def change_identifier(text: str) -> str:
    """An argparse type: the identifier of a change, checked where the command line is read."""
    problems = check_identifier(text)
    if problems:
        raise argparse.ArgumentTypeError(problems[0].message)
    return text


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("change_id", type=change_identifier, help="the identifier of the change")
    parser.add_argument("--root", help="the project root (default: the nearest project upwards)")
    parser.add_argument("--json", action="store_true", help="print the result envelope as JSON")
    parser.add_argument("--actor", help="who acts, for example human:ada or agent:builder")
    parser.add_argument("--assurance", choices=("A0", "A1", "A2"), default="A0")
    parser.add_argument(
        "--account", help="the real account of the hosting service (default: Git github.user)"
    )


def _add_flag(parser: argparse.ArgumentParser, name: str) -> None:
    spec = dict(FLAGS[name])
    parser.add_argument("--" + name.replace("_", "-"), dest=name, **spec)


def build_parser() -> argparse.ArgumentParser:
    """The parser of every command."""
    parser = argparse.ArgumentParser(
        prog="ggsad", description="Goal-Gated Spec-Anchored Development"
    )
    commands = parser.add_subparsers(dest="command", required=True, metavar="<command>")
    new = commands.add_parser("new", help=HELP["new"])
    _common(new)
    new.add_argument("--problem", help="the problem (not needed if change.yaml exists)")
    new.add_argument("--done-when", dest="done_when", action="append",
                     help="a sentence that says when the change is done, repeatable")  # fmt: skip
    new.add_argument("--owner", help="the Change owner (default: the Owner of the project)")
    new.add_argument("--author", help="the Author (default: the actor if human, else the Owner)")
    for action, names in ACTIONS.items():
        sub = commands.add_parser(action, help=HELP[action])
        _common(sub)
        if action == "approve":
            sub.add_argument("approve_target", metavar="target", help="what is approved")
        for name in names:
            _add_flag(sub, name)
    for action in READ_ONLY:
        _common(commands.add_parser(action, help=HELP[action]))
    _add_init(commands)
    doctor = commands.add_parser("doctor", help="check the project, the tools, and every change")
    doctor.add_argument("--root", help="the project folder (default: the nearest project upwards)")
    doctor.add_argument("--json", action="store_true", help="print the result envelope as JSON")
    return parser


def _add_init(commands: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    init = commands.add_parser("init", help="set up a project: config, brief, templates, example")
    init.add_argument("--root", help="the project folder (default: the current folder)")
    init.add_argument("--json", action="store_true", help="print the result envelope as JSON")
    init.add_argument("--profile", required=True, choices=PROFILES, help="the compliance profile")
    init.add_argument("--project-id", dest="project_id", help="default: the folder name")
    init.add_argument("--owner", help="the Owner, for example human:ada (default: the Git user)")
    init.add_argument("--requestor", action="append", help="an agent that may request changes")
    init.add_argument("--team-mode", dest="team_mode", choices=TEAM_MODES, default="team")


def find_root(given: str | None) -> Path:
    """The project root: the given folder, else the nearest folder upwards with a config file."""
    if given:
        return Path(given).resolve()
    here = Path.cwd().resolve()
    for folder in (here, *here.parents):
        if (folder / CONFIG_PATH).is_file():
            return folder
    return here


def _git_name(root: Path) -> str | None:
    try:
        name = run_git(root, "config", "user.name", ok=(0, 1)).decode("utf-8").strip()
    except GitError:
        return None
    return name or None


def _git_value(root: Path, key: str) -> str | None:
    try:
        value = run_git(root, "config", key, ok=(0, 1)).decode("utf-8").strip()
    except GitError:
        return None
    return value or None


def resolve_account(given: str | None, root: Path) -> str | None:
    """The real account: the option, else the variable, else `github.user` of Git (Section 24.3).

    It is never taken from the list of approved humans: that list says which account is expected,
    and the history must make a difference between the two visible.
    """
    return given or os.environ.get(ACCOUNT_VARIABLE) or _git_value(root, "github.user")


def resolve_actor(
    given: str | None, root: Path, assurance: str, account: str | None = None
) -> Actor:
    """Who acts: the option, else the variable, else the Git user (Section 24.3)."""
    identity = given or os.environ.get(ACTOR_VARIABLE)
    if not identity:
        name = _git_name(root)
        identity = f"human:{name}" if name else "human:unknown"
    return Actor(identity, assurance, resolve_account(account, root))


def _read_report(path: str | None) -> dict[str, object] | None:
    if path is None:
        return None
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        message = "the agent report must be a JSON object"
        raise TypeError(message)
    return value


def build_request(action: str, args: argparse.Namespace, actor: Actor, at: str) -> Request:
    """The request of an action from the parsed command line."""
    options = tuple(args.option) if getattr(args, "option", None) else None
    documents = tuple(getattr(args, "document", None) or ())
    return Request(
        action,
        actor,
        at,
        note=getattr(args, "note", None),
        reason=getattr(args, "reason", None),
        target=getattr(args, "approve_target", None) or getattr(args, "target", None),
        gate=getattr(args, "gate", None),
        question=getattr(args, "question", None),
        text=getattr(args, "text", None),
        owner=getattr(args, "owner", None),
        options=options,
        answer=getattr(args, "answer", None),
        resume_when=getattr(args, "resume_when", None),
        expires=getattr(args, "expires", None),
        and_resume=bool(getattr(args, "and_resume", False)),
        about_spec=bool(getattr(args, "about_spec", False)),
        replaced_by=getattr(args, "replaced_by", None),
        documents=documents,
        attempts=getattr(args, "attempts", None),
        agent_report=_read_report(getattr(args, "agent_report", None)),
    )


def _init(args: argparse.Namespace, root: Path) -> Envelope:
    name = _git_name(root)
    options = InitOptions(
        args.profile,
        args.project_id or root.name,
        args.owner or (f"human:{name}" if name else "human:unknown"),
        tuple(args.requestor or ("agent:assistant",)),
        args.team_mode,
    )
    return init_project(root, options)


def _new_fields(args: argparse.Namespace, actor: Actor, settings: Settings | None) -> NewFields:
    owner = args.owner or (settings.owner if settings else "")
    author = args.author or (actor.identity if actor.is_human else owner)
    return NewFields(args.problem or "", args.done_when or (), owner, author)


def _confirm_approval(
    args: argparse.Namespace, root: Path, settings: Settings | None, stdin: TextIO
) -> Envelope | None:
    """Show the approval summary; return a refusal unless the human confirms (Section 24.1)."""
    if settings is None:
        return None
    anchors = GitAnchorStore(root)
    loaded = load_change(root, settings, args.change_id, anchors, "approve")
    if loaded.problems or loaded.history_error is not None or loaded.state is None:
        return None
    lines = ["approval summary:", *build_summary(loaded, settings)]
    sys.stderr.write("\n".join(lines) + "\n")
    if args.yes or (stdin.isatty() and _asked(stdin)):
        return None
    text = "the approval was not confirmed after the summary; run again and answer y, or pass --yes"
    return failure("approve", (Issue("approval-not-confirmed", text),))


def _asked(stdin: TextIO) -> bool:
    sys.stderr.write("record this approval? [y/N] ")
    sys.stderr.flush()
    return stdin.readline().strip().lower() in ("y", "yes")


def _change(
    args: argparse.Namespace, root: Path, clock: Callable[[], str], stdin: TextIO
) -> tuple[Envelope, str]:
    settings, _ = load_settings(root)
    actor = resolve_actor(args.actor, root, args.assurance, args.account)
    try:
        request = build_request(args.command, args, actor, clock())
    except (OSError, ValueError, TypeError) as error:
        issue = Issue("agent-report-invalid", f"the agent report cannot be read: {error}")
        return failure(args.command, (issue,)), actor.identity
    if args.command == "approve" and actor.is_human:
        refusal = _confirm_approval(args, root, settings, stdin)
        if refusal is not None:
            return refusal, actor.identity
    if args.command == "new":
        fields = _new_fields(args, actor, settings)
        return create_change(root, args.change_id, request, fields), actor.identity
    if args.command == "repair":
        done = repair_change(root, args.change_id, request, show_only=args.show)
        return done, actor.identity
    return run_action(root, args.change_id, request), actor.identity


def execute(
    args: argparse.Namespace, root: Path, clock: Callable[[], str], stdin: TextIO
) -> tuple[Envelope, str | None]:
    """Run the command. Returns the envelope and the identity that acted, if any."""
    if args.command == "init":
        return _init(args, root), None
    if args.command == "doctor":
        return run_doctor(root, clock()), None
    if args.command in READ_ONLY:
        return run_read_only(root, args.change_id, args.command, clock()), None
    return _change(args, root, clock, stdin)


def main(
    argv: Sequence[str] | None = None,
    *,
    clock: Callable[[], str] = now_utc,
    stdin: TextIO | None = None,
) -> int:
    """Run the command line and return the exit code."""
    args = build_parser().parse_args(argv)
    root = Path(args.root or ".").resolve() if args.command == "init" else find_root(args.root)
    envelope, actor = execute(args, root, clock, stdin or sys.stdin)
    sys.stdout.write((render_json(envelope) if args.json else render_text(envelope, actor)) + "\n")
    return envelope.exit_code


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
