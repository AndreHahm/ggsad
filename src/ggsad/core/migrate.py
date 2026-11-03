"""The `migrate` operation: convert a state document to a supported version (Section 25.3).

Today the chain has one step: a YAML state document `state.yaml` becomes `state.json`, whose first
entry is a `migrate` entry (AE-103). The operation is explicit, never part of another one. It
needs the change definition to exist, because it never guesses content. It does not change or
delete the old file, and once `state.json` exists the old file is not read.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ggsad.core.content_hash import path_content_hash
from ggsad.core.errors import StateError
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.identifiers import check_identifier
from ggsad.core.issues import Issue
from ggsad.core.legacy_state import LEGACY_FILE, LEGACY_VERSION, LegacyStateError, convert
from ggsad.core.loader import DEFINITION_FILE, anchor_required, change_path
from ggsad.core.operations import Envelope, error_issue, failure, open_project
from ggsad.core.project import read_yaml_file
from ggsad.core.state import SCHEMA_VERSION
from ggsad.core.state_store import StateStore

if TYPE_CHECKING:
    from pathlib import Path

    from ggsad.core.anchor import AnchorStore
    from ggsad.core.engine_types import Request

STATE_FILE: Final = "state.json"


def _refused(*issues: Issue) -> Envelope:
    return Envelope("migrate", "rejected", False, issues=issues)


def _target_issue(target: str | None) -> Issue | None:
    if target is None or target == SCHEMA_VERSION:
        return None
    return Issue(
        "schema-version-unsupported",
        f"the target version {target!r} is not supported; the supported version is "
        f"{SCHEMA_VERSION!r}",
    )


def _body(
    request: Request, source_hash: str, converted_note: str, after: object
) -> dict[str, object]:
    actor = request.actor
    return {
        "action": "migrate",
        "actor": actor.identity,
        "account": actor.account,
        "assurance": actor.assurance,
        "at": request.at,
        "result": "success",
        "gate_results": None,
        "gate_detail": None,
        "files": None,
        "note": converted_note,
        "after": after,
        "source_version": LEGACY_VERSION,
        "target_version": SCHEMA_VERSION,
        "source_hash": source_hash,
    }


def _convert_file(path: Path, request: Request, store: StateStore) -> Envelope:
    try:
        converted = convert((path / LEGACY_FILE).read_text(encoding="utf-8"))
    except LegacyStateError as error:
        return _refused(error.issue)
    except (OSError, UnicodeDecodeError) as error:
        return failure("migrate", (Issue("state-read-failed", f"{LEGACY_FILE}: {error}"),))
    note = request.note or converted.note
    source_hash = path_content_hash(path / LEGACY_FILE)
    after = converted.state.to_json()
    try:
        store.append(_body(request, source_hash, note, after), read_version=0)
    except StateError as error:
        recorded = error.code == "anchor-lagging"
        return Envelope("migrate", "error", recorded, issues=(error_issue(error),))
    data = {"source_version": LEGACY_VERSION, "target_version": SCHEMA_VERSION}
    return Envelope("migrate", "success", True, after, data=data | {"source_hash": source_hash})


def _precheck(path: Path, change_id: str, target: str | None) -> Issue | None:
    """The reason that nothing is to be migrated, or None when the old file can be converted."""
    unsupported = _target_issue(target)
    if unsupported is not None:
        return unsupported
    if (path / STATE_FILE).exists():
        message = f"the state document already has the version {SCHEMA_VERSION!r}"
        return Issue("migration-not-needed", message)
    if not (path / LEGACY_FILE).exists():
        return Issue("nothing-to-migrate", f"{change_id} has no {LEGACY_FILE}")
    return read_yaml_file(path / DEFINITION_FILE, "definition")[1]


def migrate_change(
    root: Path,
    change_id: str,
    request: Request,
    anchors: AnchorStore | None = None,
    target: str | None = None,
) -> Envelope:
    """Convert the state document of a change; write nothing unless it succeeds."""
    settings, issues = open_project(root)
    if settings is None:
        return failure("migrate", issues)
    invalid = check_identifier(change_id)
    if invalid:
        return failure("migrate", tuple(invalid))
    path = change_path(root, change_id)
    refusal = _precheck(path, change_id, target)
    if refusal is not None:
        return _refused(refusal)
    store = StateStore(
        path,
        anchors=anchors if anchors is not None else GitAnchorStore(root),
        require_anchor=anchor_required(settings),
        change_id=change_id,
    )
    return _convert_file(path, request, store)
