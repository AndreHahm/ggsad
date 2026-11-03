"""The `repair` operation: the way out of a history that cannot be trusted (Section 24.4).

A history that is not consistent, or that is truncated or rewritten, stops every action. The
Owner of the project repairs it with a written reason. The implementation first shows exactly
which entries are missing or wrong (`show_only`). It then keeps the damaged `state.json` at a
location outside the change directory, replaces the history by its longest consistent prefix,
appends a `repaired` entry, and sets the anchor to that entry. The repair records the loss; it
never hides it.

Interpretations fixed here (listed in the pull request):
- the damaged file is kept as `.ggsad/repairs/<change-id>.<time>.state.json`;
- when the anchor is ahead of the history, the entries lost are counted from the anchor;
- a history with no consistent entry at all cannot be repaired (`repair-impossible`);
- the new anchor is set when an anchor existed or the settings require one.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from ggsad.core.engine import apply
from ggsad.core.errors import StateError
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.history import Anchor, Entry, check_anchor, verify_chain
from ggsad.core.issues import Issue
from ggsad.core.loader import LoadedChange, anchor_required, load_change
from ggsad.core.operations import Envelope, error_issue, failure, make_runner, open_project
from ggsad.core.state import State, StateRecordError
from ggsad.core.state_store import StateDocument, StateStore, parse_state_document

if TYPE_CHECKING:
    from pathlib import Path

    from ggsad.core.anchor import AnchorStore
    from ggsad.core.engine_types import Request

REPAIRS_DIRECTORY = ".ggsad/repairs"


@dataclass(frozen=True)
class Damage:
    """What is wrong with a history and what can be kept."""

    prefix: tuple[Entry, ...]
    lost: int
    messages: tuple[str, ...]
    old_anchor: Anchor | None


def _entries(text: str | None) -> tuple[tuple[Entry, ...], str | None]:
    if text is None:
        return (), "the state document does not exist or cannot be read"
    try:
        return parse_state_document(text).entries, None
    except StateError as error:
        return (), error.message


def _anchor_damage(entries: tuple[Entry, ...], anchor: Anchor | None) -> Damage | None:
    problems = check_anchor(entries, anchor) if anchor is not None else []
    if anchor is None or not problems:
        return None
    keep = entries if problems[0].code == "history-truncated" else entries[: anchor.position - 1]
    lost = max(anchor.position - len(keep), len(entries) - len(keep))
    return Damage(keep, lost, tuple(p.message for p in problems), anchor)


def diagnose(text: str | None, anchor: Anchor | None) -> Damage | None:
    """What is damaged in the state document, or None when nothing is."""
    entries, unreadable = _entries(text)
    if unreadable is not None:
        return Damage((), anchor.position if anchor else 0, (unreadable,), anchor)
    problems = verify_chain(entries)
    if not problems:
        return _anchor_damage(entries, anchor)
    first = next(i for i, e in enumerate(entries) if verify_chain(entries[: i + 1]))
    keep = entries[:first]
    lost = max(len(entries), anchor.position if anchor else 0) - len(keep)
    return Damage(keep, lost, tuple(p.message for p in problems), anchor)


def _describe(damage: Damage) -> dict[str, object]:
    return {
        "damage": list(damage.messages),
        "entries_kept": len(damage.prefix),
        "entries_lost": damage.lost,
        "old_anchor": _anchor_json(damage.old_anchor),
    }


def _anchor_json(anchor: Anchor | None) -> dict[str, object] | None:
    return None if anchor is None else {"position": anchor.position, "hash": anchor.hash}


def _read_text(store: StateStore) -> str | None:
    try:
        return store.state_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _salvaged(loaded: LoadedChange, damage: Damage) -> tuple[LoadedChange, Issue | None]:
    if not damage.prefix:
        return loaded, Issue("repair-impossible", "no consistent entry is left to keep")
    try:
        state = State.from_json(damage.prefix[-1].body["after"])
    except (StateRecordError, KeyError) as error:
        return loaded, Issue(
            "repair-impossible", f"the last consistent state is not valid: {error}"
        )
    bodies = tuple(entry.body for entry in damage.prefix)
    return replace(loaded, state=state, bodies=bodies), None


def _keep_damaged_file(root: Path, store: StateStore, change_id: str, at: str) -> str:
    stamp = at.replace(":", "-")
    target = root / REPAIRS_DIRECTORY / f"{change_id}.{stamp}.state.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as handle:
        handle.write(store.state_path.read_bytes())
    return target.relative_to(root).as_posix()


def _write_repair(
    root: Path, loaded: LoadedChange, damage: Damage, body: dict[str, object], anchors: AnchorStore
) -> Entry:
    """Replace the history by its prefix, append the `repaired` entry, and set the anchor."""
    store = loaded.store
    version = loaded.state.schema_version if loaded.state is not None else "1.0"
    prefix = StateDocument(version, damage.prefix)
    plain = StateStore(store.state_path.parent, change_id=loaded.change_id)
    plain.state_path.parent.mkdir(parents=True, exist_ok=True)
    plain.state_path.write_text(prefix.to_text(), encoding="utf-8", newline="\n")
    entry = plain.append(body, read_version=len(damage.prefix))
    if damage.old_anchor is not None or anchor_required_for(root):
        anchors.write(loaded.change_id, Anchor(entry.n, entry.hash))
    return entry


def anchor_required_for(root: Path) -> bool:
    """True when the settings of the project require an anchor."""
    settings, _ = open_project(root)
    return settings is not None and anchor_required(settings)


def repair_change(
    root: Path,
    change_id: str,
    request: Request,
    anchors: AnchorStore | None = None,
    *,
    show_only: bool = False,
) -> Envelope:
    """Show or carry out the repair of the history of a change."""
    settings, issues = open_project(root)
    if settings is None:
        return failure("repair", issues)
    store = anchors if anchors is not None else GitAnchorStore(root)
    loaded = load_change(root, settings, change_id, store, "repair")
    if loaded.problems:
        return failure("repair", loaded.problems)
    if loaded.history_error is None:
        runner = make_runner(root, settings, loaded)
        done = apply(loaded.state, request, loaded.context, loaded.facts, runner)
        state = done.state.to_json() if loaded.state is not None else None
        return Envelope("repair", done.result, False, state, done.issues)
    return _repair_damaged(root, loaded, request, store, show_only=show_only)


def _repair_damaged(
    root: Path, loaded: LoadedChange, request: Request, anchors: AnchorStore, *, show_only: bool
) -> Envelope:
    try:
        anchor = anchors.read(loaded.change_id)
    except StateError as error:
        return failure("repair", (error_issue(error),))
    damage = diagnose(_read_text(loaded.store), anchor)
    if damage is None:
        return failure(
            "repair", (error_issue(loaded.history_error),) if loaded.history_error else ()
        )
    if show_only:
        return Envelope("repair", "success", False, data=_describe(damage))
    salvaged, problem = _salvaged(loaded, damage)
    if problem is not None:
        return failure("repair", (problem,))
    return _carry_out(root, salvaged, damage, request, anchors)


def _carry_out(
    root: Path, loaded: LoadedChange, damage: Damage, request: Request, anchors: AnchorStore
) -> Envelope:
    settings, _ = open_project(root)
    if settings is None or loaded.state is None:
        return failure("repair", (Issue("config-missing", "the project has no settings"),))
    repaired = {**_describe(damage), "reason": request.reason, "damaged_file": None}
    trial = apply(
        loaded.state,
        replace(request, repaired=repaired),
        loaded.context,
        loaded.facts,
        make_runner(root, settings, loaded),
    )
    if not trial.bodies:
        return Envelope("repair", trial.result, False, trial.state.to_json(), trial.issues)
    try:
        kept = _keep_damaged_file(root, loaded.store, loaded.change_id, request.at)
        body = {**trial.bodies[0], "repaired": {**repaired, "damaged_file": kept}}
        entry = _write_repair(root, loaded, damage, body, anchors)
    except (OSError, StateError) as error:
        issue = (
            error_issue(error)
            if isinstance(error, StateError)
            else Issue("state-write-failed", str(error))
        )
        return failure("repair", (issue,))
    data = {**_describe(damage), "damaged_file": kept, "entry": entry.n}
    return Envelope("repair", "success", True, trial.state.to_json(), data=data)
