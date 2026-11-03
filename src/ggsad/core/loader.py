"""Reading one change from disk: its files, its history, and the facts the engine takes as input.

The loader reads and asks Git; it never writes and never raises for the content of a file or a
history. What it cannot use becomes an issue (`problems`) or a `StateError` (`history_error`), and
the operation layer turns those into a result. Slow questions to Git (the revision, uncommitted
work) are asked only for the action that needs them.

Interpretations fixed here (listed in the pull request):
- the specification must be approved before the start in every profile except `lean`, and in
  `lean` when the settings set a minimum level for `spec_approval`;
- an anchor is required when any minimum level in the settings is `A2`;
- a change is open for `supersede` when its history exists and does not end in `closed`.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Final

from ggsad.core.anchor import AnchorStore
from ggsad.core.change_definition import (
    SUPPORTED_SCHEMA_VERSIONS,
    ProjectContext,
    validate_for_gate_approval,
    validate_for_new,
)
from ggsad.core.content_hash import file_content_hash
from ggsad.core.errors import StateError
from ggsad.core.gate_eval import NOT_EVALUABLE, Check, Facts, Gate, count_not_satisfied
from ggsad.core.git_scope import GitError, head_revision, measure_scope, unclean_paths
from ggsad.core.guards import approved_hash
from ggsad.core.identifiers import check_identifier
from ggsad.core.issues import Issue
from ggsad.core.project import (
    conflict_line_issues,
    definitions_hash,
    document_fingerprint,
    profile_issue,
    read_yaml_file,
)
from ggsad.core.review_report import approval_issues, completion_gaps
from ggsad.core.settings import Settings, build_context, gates_for
from ggsad.core.state import State, StateRecordError
from ggsad.core.state_store import StateStore
from ggsad.core.values import as_list, as_mapping

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

    from ggsad.core.engine_types import Context

SPECS: Final = "specs"
DEFINITION_FILE: Final = "change.yaml"
SPEC_FILE: Final = "spec.md"
REVIEW_FILE: Final = "review.md"
Problem = tuple[str, str]


@dataclass(frozen=True)
class LoadedChange:
    """Everything an operation needs to know about one change."""

    change_id: str
    change_dir: str
    definition: Mapping[str, object] | None
    state: State | None
    bodies: tuple[Mapping[str, object], ...]
    context: Context
    facts: Facts
    store: StateStore
    problems: tuple[Issue, ...] = ()
    history_error: StateError | None = None

    @property
    def read_version(self) -> int:
        """The number of entries that were read, for the conflict check of the store."""
        return len(self.bodies)


def existing_ids(root: Path) -> list[str]:
    """The identifiers of the changes the project already has."""
    specs = root / SPECS
    if not specs.is_dir():
        return []
    return sorted(item.name for item in specs.iterdir() if item.is_dir())


def change_path(root: Path, change_id: str) -> Path:
    """The directory of a change. The identifier must have passed `check_identifier`."""
    return root / SPECS / change_id


def read_text(path: Path) -> str | None:
    """The text of a file, None when it does not exist or is not text."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _read_state(store: StateStore) -> tuple[State | None, tuple[Mapping[str, object], ...]]:
    """The state and the entry bodies. Raises StateError for a history that cannot be used."""
    document = store.read()
    if document is None:
        return None, ()
    store.verify(document)
    try:
        after = document.entries[-1].body["after"] if document.entries else None
        state = State.from_json(after)
    except (StateRecordError, KeyError) as error:
        raise StateError(
            "state-record-invalid", f"the recorded state is not valid: {error}"
        ) from error
    return state, tuple(entry.body for entry in document.entries)


def _definition(path: Path) -> tuple[Mapping[str, object] | None, tuple[Issue, ...]]:
    value, issue = read_yaml_file(path / DEFINITION_FILE, "definition")
    if issue is not None:
        return None, (issue,)
    mapping = as_mapping(value)
    if mapping is None:
        return None, (Issue("definition-invalid", "a change definition is a mapping"),)
    if mapping.get("schema_version") not in SUPPORTED_SCHEMA_VERSIONS:
        message = (
            f"schema_version {mapping.get('schema_version')!r} of the definition is not supported"
        )
        return None, (Issue("schema-version-unsupported", message),)
    return mapping, ()


def anchor_required(settings: Settings) -> bool:
    """True when the configuration requires approvals at the level A2 (Section 24.4)."""
    return "A2" in settings.minimum_levels.values()


def spec_approval_required(settings: Settings) -> bool:
    """True when the specification must be approved before the start (Section 23.4)."""
    return settings.compliance_profile != "lean" or "spec_approval" in settings.minimum_levels


def _has_anchor(anchors: AnchorStore, change_id: str) -> bool:
    try:
        return anchors.read(change_id) is not None
    except StateError:
        return False


def _target_issues(
    root: Path,
    settings: Settings,
    definition: Mapping[str, object] | None,
    spec_text: str | None,
    review_text: str | None,
) -> dict[str, tuple[Problem, ...]]:
    found: dict[str, tuple[Problem, ...]] = {
        "approve:review": tuple(approval_issues(review_text)),
        "approve:spec": tuple(conflict_line_issues(spec_text)),
    }
    if definition is not None:
        context = ProjectContext(
            settings.compliance_profile,
            existing_ids(root),
            approved_humans=settings.approved_identities,
            default_retry_limit=settings.retry_limit,
        )
        report = validate_for_gate_approval(definition, context)
        found["approve:gates"] = tuple((i.code, i.message) for i in report.issues)
    return found


def _review_gaps(gates: tuple[Gate, ...], review_text: str | None) -> dict[str, tuple[str, ...]]:
    ids = [g.id for g in gates if g.kind == "review" and g.group == "done"]
    return {gate_id: completion_gaps(review_text) for gate_id in ids}


def _scope(
    root: Path, definition: Mapping[str, object] | None, state: State | None, change_dir: str
) -> Check | None:
    if state is None or state.base_revision is None:
        return None
    scope = as_mapping(definition.get("scope")) if definition is not None else None
    allow = as_list(scope.get("allow")) if scope is not None else None
    patterns = [p for p in allow if isinstance(p, str)] if allow is not None else None
    return measure_scope(root, state.base_revision, patterns, change_dir)


def _start_facts(root: Path, change_dir: str) -> tuple[str | None, tuple[str, ...]]:
    try:
        return head_revision(root), tuple(unclean_paths(root, change_dir))
    except GitError:
        return None, ()


def _spec_approved(settings: Settings, state: State | None) -> bool:
    if not spec_approval_required(settings):
        return True
    return state is not None and any(a.target == "spec" for a in state.approvals)


def _open_ids(root: Path, own: str) -> frozenset[str]:
    found: set[str] = set()
    for name in existing_ids(root):
        if name == own:
            continue
        try:
            state, _ = _read_state(StateStore(change_path(root, name)))
        except StateError:
            continue
        if state is not None and state.state != "closed":
            found.add(name)
    return frozenset(found)


@dataclass(frozen=True)
class _Files:
    """What was read for one change, before the facts are built."""

    definition: Mapping[str, object] | None
    problems: tuple[Issue, ...]
    state: State | None
    bodies: tuple[Mapping[str, object], ...]
    error: StateError | None
    spec_text: str | None
    review_text: str | None


def _read_files(path: Path, store: StateStore, change_id: str) -> _Files:
    invalid = check_identifier(change_id)
    if invalid:
        return _Files(None, tuple(invalid), None, (), None, None, None)
    definition, problems = _definition(path)
    state: State | None = None
    bodies: tuple[Mapping[str, object], ...] = ()
    error: StateError | None = None
    try:
        state, bodies = _read_state(store)
    except StateError as caught:
        error = caught
    spec, review = read_text(path / SPEC_FILE), read_text(path / REVIEW_FILE)
    return _Files(definition, problems, state, bodies, error, spec, review)


def _text_hash(text: str | None) -> str | None:
    return file_content_hash(text.encode("utf-8")) if text is not None else None


def _build_facts(
    root: Path, settings: Settings, change_id: str, files: _Files, gates: tuple[Gate, ...]
) -> Facts:
    change_dir = f"{SPECS}/{change_id}"
    definition, state = files.definition, files.state
    current = state if state is not None else State()
    hash_now = definitions_hash(definition) if definition is not None else None
    approved = approved_hash(current)
    issues = _target_issues(root, settings, definition, files.spec_text, files.review_text)
    issues["new"] = _new_issues(root, settings, definition, change_id)
    stale = None if files.spec_text is not None else Check(NOT_EVALUABLE, "spec.md is missing")
    return Facts(
        scope=_scope(root, definition, state, change_dir),
        stale_spec_approval=stale,
        review_gaps=_review_gaps(gates, files.review_text),
        review_hash=_text_hash(files.review_text),
        not_satisfied_counts=count_not_satisfied(files.bodies),
        definitions_hash=hash_now,
        spec_hash=_text_hash(files.spec_text),
        documents=document_fingerprint(root),
        gates_approved=approved is not None and approved == hash_now,
        spec_approval_ok=_spec_approved(settings, state),
        target_issues=issues,
        history_damaged=files.error is not None,
    )


def load_change(
    root: Path,
    settings: Settings,
    change_id: str,
    anchors: AnchorStore,
    action: str | None = None,
) -> LoadedChange:
    """Read a change. `action` lets the loader ask Git only what that action needs."""
    path = change_path(root, change_id)
    store = StateStore(
        path, anchors=anchors, require_anchor=anchor_required(settings), change_id=change_id
    )
    files = _read_files(path, store, change_id)
    definition = files.definition
    gates = gates_for(settings, definition) if definition is not None else ()
    context = build_context(settings, definition or {}, gates, change_id)
    facts = _build_facts(root, settings, change_id, files, gates)
    extra: dict[str, object] = {"has_anchor": _has_anchor(anchors, change_id)}
    if action == "start":
        extra["revision"], extra["unclean_paths"] = _start_facts(root, f"{SPECS}/{change_id}")
    if action == "supersede":
        extra["open_changes"] = _open_ids(root, change_id)
    return LoadedChange(
        change_id,
        f"{SPECS}/{change_id}",
        definition,
        files.state,
        files.bodies,
        context,
        replace(facts, **extra),
        store,
        files.problems,
        files.error,
    )


def _new_issues(
    root: Path, settings: Settings, definition: Mapping[str, object] | None, change_id: str
) -> tuple[Problem, ...]:
    found: list[Problem] = []
    mismatch = profile_issue(root, settings)
    if mismatch is not None:
        found.append((mismatch.code, mismatch.message))
    if definition is not None:
        others = [name for name in existing_ids(root) if name != change_id]
        context = ProjectContext(
            settings.compliance_profile,
            others,
            approved_humans=settings.approved_identities,
            default_retry_limit=settings.retry_limit,
        )
        found.extend((i.code, i.message) for i in validate_for_new(definition, context).issues)
    return tuple(found)
