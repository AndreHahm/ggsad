"""Class M change creation (R-003, R-004, R-008, R-012).

`build_change_manifest` renders the five required artifacts for a new
change under `specs/<change-id>-<slug>/`: `state.yaml` is constructed
through the typed `ChangeState` model from Slice 2 (so it's correct by
construction against `state.schema.json`, not hand-formatted YAML), and
`spec.md`/`plan.md`/`tasks.md`/`evidence.md` are copied verbatim from their
packaged templates, placeholders unresolved -- the same pattern
`initialize_project.py` uses for the project-level docs.

Only Class M is implemented in CHG-001 (R2 in the roadmap; S and L are not
in scope). Change ID and slug are validated by strict regex before any path
is resolved, which by construction rules out the traversal characters
(`/`, `..`) that R-004 and R-012 care about; `resolve_change_directory`
still verifies containment as defense in depth rather than relying on the
regex alone.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from ggsad.models.state import (
    ArtifactPaths,
    ChangeIdentity,
    ChangeState,
    FailureState,
    FlowState,
    GoalSummary,
    HistoryEvent,
    PairReviewState,
    WaitState,
    dump_change_state,
)
from ggsad.resources import resource_root
from ggsad.validators.yaml_loader import dump_yaml_bytes

CHANGE_ID_PATTERN = re.compile(r"^CHG-\d{3,}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SUPPORTED_CHANGE_CLASS = "M"

_ARTIFACT_TEMPLATES: dict[str, str] = {
    "spec.template.md": "spec.md",
    "plan.template.md": "plan.md",
    "tasks.template.md": "tasks.md",
    "evidence.template.md": "evidence.md",
}


class ChangeCreationError(ValueError):
    """Base for `ggsad new` rejections (R-004 validation, R-012 containment/conflict)."""


class InvalidChangeIdentifierError(ChangeCreationError):
    """Raised when a change ID, slug, or class fails R-004 validation."""


class ChangeAlreadyExistsError(ChangeCreationError):
    """Raised when the target change directory already exists.

    Deliberately checked by directory existence, not byte-for-byte content
    comparison: `state.yaml`'s history timestamp has second precision, so
    two `new` invocations within the same second render byte-identical
    output -- relying on that for "already exists" detection would make a
    governance-critical rejection non-deterministic. A change's state is
    also expected to evolve after creation (transitions, approvals), so
    even a byte-identical re-render should never be treated as a safe
    no-op the way `init`'s idempotency is.
    """


def validate_change_id(change_id: str) -> None:
    """Reject a change ID that doesn't match `CHG-<three-or-more-digits>`."""
    if not CHANGE_ID_PATTERN.match(change_id):
        msg = (
            f"Invalid change ID {change_id!r}: must match 'CHG-' followed by "
            "three or more digits, e.g. 'CHG-002'."
        )
        raise InvalidChangeIdentifierError(msg)


def validate_slug(slug: str) -> None:
    """Reject a slug that isn't lowercase alphanumeric segments joined by single hyphens."""
    if not SLUG_PATTERN.match(slug):
        msg = (
            f"Invalid slug {slug!r}: must be lowercase alphanumeric segments "
            "separated by single hyphens, e.g. 'example-change'."
        )
        raise InvalidChangeIdentifierError(msg)


def resolve_change_directory(target: Path, change_id: str, slug: str) -> Path:
    """Resolve `specs/<change_id>-<slug>/` under `target`, verifying containment."""
    specs_root = (target / "specs").resolve()
    change_dir = (specs_root / f"{change_id}-{slug}").resolve()

    if change_dir.parent != specs_root:
        # Defense in depth: validate_change_id/validate_slug already forbid
        # the characters that would make this reachable, but containment is
        # verified rather than assumed from the regexes alone.
        msg = f"Resolved change path {change_dir} escapes {specs_root}."
        raise InvalidChangeIdentifierError(msg)

    return change_dir


def _render_state_yaml(*, change_id: str, slug: str, title: str, change_class: str) -> bytes:
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    state = ChangeState(
        schema_version="0.1",
        change=ChangeIdentity(id=change_id, slug=slug, title=title, change_class=change_class),
        flow=FlowState(profile="standard", phase="specify", status="draft"),
        goal=GoalSummary(summary=f"<Describe the desired outcome for {change_id}.>"),
        artifacts=ArtifactPaths(
            spec="spec.md", plan="plan.md", tasks="tasks.md", evidence="evidence.md"
        ),
        pair_review=PairReviewState(required=True, status="pending"),
        wait=WaitState(),
        failure=FailureState(),
        history=[HistoryEvent(timestamp=now, event="change-created", actor="cli-user")],
    )
    return dump_yaml_bytes(dump_change_state(state))


def build_change_manifest(
    target: Path,
    *,
    change_id: str,
    slug: str,
    title: str,
    change_class: str = SUPPORTED_CHANGE_CLASS,
) -> dict[Path, bytes]:
    """Build the manifest for a new Class M change: absolute path -> desired content.

    Raises:
        InvalidChangeIdentifierError: if `change_id`, `slug`, or `change_class`
            fail validation.
        ChangeAlreadyExistsError: if the target change directory already exists.
    """
    validate_change_id(change_id)
    validate_slug(slug)
    if change_class != SUPPORTED_CHANGE_CLASS:
        msg = f"Unsupported change class {change_class!r}: CHG-001 only implements Class M."
        raise InvalidChangeIdentifierError(msg)

    change_dir = resolve_change_directory(target, change_id, slug)

    if change_dir.exists():
        msg = (
            f"Change directory {change_dir} already exists. `ggsad new` creates a change "
            "once; use a different change ID, or edit the existing change's artifacts directly."
        )
        raise ChangeAlreadyExistsError(msg)

    manifest: dict[Path, bytes] = {
        change_dir / "state.yaml": _render_state_yaml(
            change_id=change_id, slug=slug, title=title, change_class=change_class
        )
    }

    resources = resource_root()
    for entry in (resources / "templates").iterdir():
        if entry.is_file():
            artifact_name = _ARTIFACT_TEMPLATES.get(entry.name)
            if artifact_name is not None:
                manifest[change_dir / artifact_name] = entry.read_bytes()

    return manifest
