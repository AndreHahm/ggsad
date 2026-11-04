"""The project settings of the `core` profile: `.ggsad/config.yaml`, schema version 1.0.

The file is read as parsed YAML. `read_settings` checks it and returns typed `Settings`; it writes
nothing and never raises for a bad file. Reading the file from disk, and `init`, come with the CLI.

Layout (Sections 3.11, 5.1, 24.1, 24.3, 24.7):

    schema_version: "1.0"
    project: {id, compliance_profile, team_mode}
    roles: {owner, approved_humans, deputies, unavailable_approvers, requestors, reviewers}
    defaults: {retry_limit, fail_severity}
    minimum_levels: {<kind of action>: A0|A1|A2}
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final

from ggsad.core.engine_types import Context
from ggsad.core.gate_model import parse_gates
from ggsad.core.issues import Report, ReportBuilder
from ggsad.core.values import as_int, as_list, as_mapping, as_text, text_list

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ggsad.core.gate_eval import Gate

SCHEMA_VERSION: Final = "1.0"
PROFILES: Final = ("lean", "standard", "governed", "regulated")
TEAM_MODES: Final = ("solo", "team")
SEVERITIES: Final = ("hard", "soft")
LEVELS: Final = ("A0", "A1", "A2")
MAX_RETRY_LIMIT: Final = 3
KINDS: Final = (
    "spec_approval", "gate_approval", "review_approval", "documents_approval", "sign_off",
    "override", "answer", "cancel", "fail", "adopt", "repair",
)  # fmt: skip
_TOP: Final = frozenset(
    {"schema_version", "project", "roles", "defaults", "minimum_levels", "interpreter"}
)
_PROJECT: Final = frozenset({"id", "compliance_profile", "team_mode"})
_ROLES: Final = frozenset(
    {"owner", "approved_humans", "deputies", "unavailable_approvers", "requestors", "reviewers"}
)
_DEFAULTS: Final = frozenset({"retry_limit", "fail_severity"})
_REQUESTOR: Final = frozenset({"identity", "vendor", "model"})
_REVIEWER: Final = frozenset({"identity", "vendor", "model", "fallback"})
_HUMAN: Final = "human:"
_AGENT: Final = "agent:"


@dataclass(frozen=True)
class ApprovedHuman:
    """An approved human: the typed identity and the account of the hosting service."""

    identity: str
    account: str


@dataclass(frozen=True)
class Requestor:
    """An agent that may act as Requestor, with its vendor and model."""

    identity: str
    vendor: str | None = None
    model: str | None = None


@dataclass(frozen=True)
class Reviewer:
    """An agent or review service that may act as Reviewer, with its vendor and model.

    `fallback` marks the fallback Reviewer, which comes from a third vendor (Section 14.2).
    """

    identity: str
    vendor: str | None = None
    model: str | None = None
    fallback: bool = False


@dataclass(frozen=True)
class Settings:
    """The checked project settings."""

    project_id: str
    compliance_profile: str
    team_mode: str = "team"
    owner: str = ""
    approved_humans: tuple[ApprovedHuman, ...] | None = None
    deputies: tuple[str, ...] = ()
    unavailable_approvers: tuple[str, ...] = ()
    requestors: tuple[Requestor, ...] = ()
    reviewers: tuple[Reviewer, ...] = ()
    retry_limit: int = MAX_RETRY_LIMIT
    fail_severity: str = "hard"
    minimum_levels: Mapping[str, str] = field(default_factory=dict)
    interpreter: str | None = None

    @property
    def approved_identities(self) -> frozenset[str] | None:
        """The identities on the list of approved humans, or None when no list is set."""
        if self.approved_humans is None:
            return None
        return frozenset(h.identity for h in self.approved_humans)


@dataclass(frozen=True)
class _Roles:
    owner: str
    approved_humans: tuple[ApprovedHuman, ...] | None
    deputies: tuple[str, ...]
    unavailable_approvers: tuple[str, ...]
    requestors: tuple[Requestor, ...]
    reviewers: tuple[Reviewer, ...] = ()


def _check_header(root: Mapping[str, object], rb: ReportBuilder) -> None:
    _check_unknown(root, _TOP, "", rb)
    if root.get("schema_version") != SCHEMA_VERSION:
        rb.error(
            "schema-version-unsupported",
            f"schema_version must be {SCHEMA_VERSION!r}",
            "schema_version",
        )
    if "interpreter" in root and as_text(root["interpreter"]) is None:
        rb.error("field-type-invalid", "interpreter must be the name of a program", "interpreter")


def read_settings(value: object) -> tuple[Settings | None, Report]:
    """Check parsed settings. The settings are None when the report holds errors."""
    rb = ReportBuilder()
    root = as_mapping(value)
    if root is None:
        rb.error("field-type-invalid", "the settings must be a mapping")
        return None, rb.build()
    _check_header(root, rb)
    project = _read_project(root.get("project"), rb)
    roles = _read_roles(root.get("roles"), rb)
    defaults = _read_defaults(root.get("defaults"), rb)
    levels = _read_levels(root.get("minimum_levels"), rb)
    if project is None or roles is None or defaults is None or levels is None:
        return None, rb.build()
    settings = Settings(
        project_id=project[0],
        compliance_profile=project[1],
        team_mode=project[2],
        minimum_levels=levels,
        interpreter=as_text(root.get("interpreter")) if "interpreter" in root else None,
        retry_limit=defaults[0],
        fail_severity=defaults[1],
        owner=roles.owner,
        approved_humans=roles.approved_humans,
        deputies=roles.deputies,
        unavailable_approvers=roles.unavailable_approvers,
        requestors=roles.requestors,
        reviewers=roles.reviewers,
    )
    _check_consistency(settings, rb)
    report = rb.build()
    return (settings if report.ok else None), report


def _check_unknown(
    mapping: Mapping[str, object], allowed: frozenset[str], where: str, rb: ReportBuilder
) -> None:
    for key in sorted(set(mapping) - allowed):
        path = f"{where}.{key}" if where else key
        rb.error("field-unknown", f"unknown field {key!r}", path)


def _section(value: object, name: str, rb: ReportBuilder) -> Mapping[str, object] | None:
    if value is None:
        return {}
    mapping = as_mapping(value)
    if mapping is None:
        rb.error("field-type-invalid", f"{name} must be a mapping", name)
    return mapping


def _choice(value: object, allowed: tuple[str, ...], path: str, rb: ReportBuilder) -> str | None:
    if isinstance(value, str) and value in allowed:
        return value
    rb.error("field-value-invalid", f"{path} must be one of {', '.join(allowed)}", path)
    return None


def _read_project(value: object, rb: ReportBuilder) -> tuple[str, str, str] | None:
    project = _section(value, "project", rb)
    if project is None:
        return None
    _check_unknown(project, _PROJECT, "project", rb)
    project_id = as_text(project.get("id"))
    if project_id is None:
        rb.error("field-missing", "project.id is required", "project.id")
    profile = _choice(project.get("compliance_profile"), PROFILES, "project.compliance_profile", rb)
    mode = _choice(project.get("team_mode", "team"), TEAM_MODES, "project.team_mode", rb)
    if project_id is None or profile is None or mode is None:
        return None
    return project_id, profile, mode


def _human(value: object, path: str, rb: ReportBuilder) -> str | None:
    text = as_text(value)
    if text is None or not text.startswith(_HUMAN) or text == _HUMAN:
        rb.error("identity-invalid", f"{path} must be an identity written human:<name>", path)
        return None
    return text


def _read_roles(value: object, rb: ReportBuilder) -> _Roles | None:
    roles = _section(value, "roles", rb)
    if roles is None:
        return None
    _check_unknown(roles, _ROLES, "roles", rb)
    owner = _human(roles.get("owner"), "roles.owner", rb)
    humans = _read_humans(roles.get("approved_humans"), rb)
    deputies = _read_humans_list(roles.get("deputies"), "roles.deputies", rb)
    away = _read_humans_list(roles.get("unavailable_approvers"), "roles.unavailable_approvers", rb)
    requestors = _read_requestors(roles.get("requestors"), rb)
    reviewers = _read_reviewers(roles.get("reviewers"), rb)
    if owner is None or deputies is None or away is None:
        return None
    if requestors is None or reviewers is None:
        return None
    return _Roles(owner, humans, deputies, away, requestors, reviewers)


def _read_humans(value: object, rb: ReportBuilder) -> tuple[ApprovedHuman, ...] | None:
    if value is None:
        return None
    items = as_list(value)
    if items is None:
        rb.error(
            "field-type-invalid", "roles.approved_humans must be a list", "roles.approved_humans"
        )
        return None
    read = [_read_human(item, f"roles.approved_humans[{i}]", rb) for i, item in enumerate(items)]
    return tuple(h for h in read if h is not None)


def _read_human(item: object, path: str, rb: ReportBuilder) -> ApprovedHuman | None:
    entry = as_mapping(item) or {}
    identity = _human(entry.get("identity"), f"{path}.identity", rb)
    account = as_text(entry.get("account"))
    if account is None:
        rb.error("field-missing", f"{path}.account is required", f"{path}.account")
    if identity is None or account is None:
        return None
    return ApprovedHuman(identity, account)


def _read_humans_list(value: object, path: str, rb: ReportBuilder) -> tuple[str, ...] | None:
    if value is None:
        return ()
    names = text_list(value)
    if names is None:
        rb.error("field-type-invalid", f"{path} must be a list of identities", path)
        return None
    checked = [_human(name, path, rb) for name in names]
    return tuple(name for name in checked if name is not None)


def _read_requestors(value: object, rb: ReportBuilder) -> tuple[Requestor, ...] | None:
    if value is None:
        return ()
    items = as_list(value)
    if items is None:
        rb.error("field-type-invalid", "roles.requestors must be a list", "roles.requestors")
        return None
    found: list[Requestor] = []
    for index, item in enumerate(items):
        entry = as_mapping(item) or {}
        path = f"roles.requestors[{index}]"
        _check_unknown(entry, _REQUESTOR, path, rb)
        identity = as_text(entry.get("identity"))
        if identity is None or not identity.startswith(_AGENT):
            rb.error("identity-invalid", f"{path}.identity must be written agent:<name>", path)
            continue
        found.append(Requestor(identity, as_text(entry.get("vendor")), as_text(entry.get("model"))))
    return tuple(found)


def _read_reviewer(item: object, path: str, rb: ReportBuilder) -> Reviewer | None:
    entry = as_mapping(item) or {}
    _check_unknown(entry, _REVIEWER, path, rb)
    identity = as_text(entry.get("identity"))
    if identity is None or not identity.startswith(_AGENT):
        rb.error("identity-invalid", f"{path}.identity must be written agent:<name>", path)
        return None
    fallback = entry.get("fallback", False)
    if not isinstance(fallback, bool):
        rb.error("field-type-invalid", f"{path}.fallback must be true or false", path)
        return None
    vendor, model = as_text(entry.get("vendor")), as_text(entry.get("model"))
    return Reviewer(identity, vendor, model, fallback)


def _read_reviewers(value: object, rb: ReportBuilder) -> tuple[Reviewer, ...] | None:
    if value is None:
        return ()
    items = as_list(value)
    if items is None:
        rb.error("field-type-invalid", "roles.reviewers must be a list", "roles.reviewers")
        return None
    found = [_read_reviewer(item, f"roles.reviewers[{i}]", rb) for i, item in enumerate(items)]
    return tuple(r for r in found if r is not None)


def _read_defaults(value: object, rb: ReportBuilder) -> tuple[int, str] | None:
    defaults = _section(value, "defaults", rb)
    if defaults is None:
        return None
    _check_unknown(defaults, _DEFAULTS, "defaults", rb)
    limit = as_int(defaults.get("retry_limit", MAX_RETRY_LIMIT))
    if limit is None or not 0 <= limit <= MAX_RETRY_LIMIT:
        rb.error(
            "retry-limit-invalid",
            f"defaults.retry_limit is a whole number from 0 to {MAX_RETRY_LIMIT}",
            "defaults.retry_limit",
        )
    severity = _choice(
        defaults.get("fail_severity", "hard"), SEVERITIES, "defaults.fail_severity", rb
    )
    if limit is None or severity is None:
        return None
    return limit, severity


def _read_levels(value: object, rb: ReportBuilder) -> dict[str, str] | None:
    levels = _section(value, "minimum_levels", rb)
    if levels is None:
        return None
    _check_unknown(levels, frozenset(KINDS), "minimum_levels", rb)
    found: dict[str, str] = {}
    for kind in KINDS:
        if kind in levels:
            level = _choice(levels[kind], LEVELS, f"minimum_levels.{kind}", rb)
            if level is not None:
                found[kind] = level
    return found


def _check_consistency(settings: Settings, rb: ReportBuilder) -> None:
    listed = settings.approved_identities
    if listed is not None and settings.owner not in listed:
        rb.error(
            "owner-not-approved", "the Owner must be on the list of approved humans", "roles.owner"
        )
    for name in (*settings.deputies, *settings.unavailable_approvers):
        if listed is not None and name not in listed:
            rb.error("human-not-approved", f"{name} is not on the list of approved humans", "roles")
    if settings.compliance_profile == "regulated" and not settings.deputies:
        rb.error(
            "deputy-required", "the profile regulated needs at least one deputy", "roles.deputies"
        )


def gates_for(settings: Settings, definition: Mapping[str, object]) -> tuple[Gate, ...]:
    """The gates of a change: its own, the base gates, the implicit retry limits, the evidence."""
    return parse_gates(
        definition.get("gates"), settings.retry_limit, definition.get("requirements")
    )


def build_context(
    settings: Settings, definition: Mapping[str, object], gates: tuple[Gate, ...], change_id: str
) -> Context:
    """The context of one change: the settings plus the roles its change definition names."""
    owner = as_text(definition.get("owner")) or settings.owner
    author = as_text(definition.get("author")) or ""
    named = as_text(definition.get("approver"))
    listed = settings.approved_identities
    approver = named if named and (listed is None or named in listed) else owner
    return Context(
        change_id=change_id,
        gates=gates,
        change_owner=owner,
        author=author,
        owner=settings.owner,
        requestors=frozenset(r.identity for r in settings.requestors),
        approved_humans=settings.approved_identities,
        agent_may_close=definition.get("agent_may_close") is True,
        approver=approver,
        compliance_profile=settings.compliance_profile,
        team_mode=settings.team_mode,
        deputies=frozenset(settings.deputies),
        unavailable_approvers=frozenset(settings.unavailable_approvers),
        minimum_levels=dict(settings.minimum_levels),
    )
