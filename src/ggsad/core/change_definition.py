"""Validation of the change definition `change.yaml` (Sections 3.11, 5.6, 23.1, and 24.9).

Two entry points mirror the two moments at which the specification checks a definition:

- `validate_for_new` is the check of the `new` action: the definition is valid under Sections
  23.1 and 23.3, its profiles fit the project, and its identifier and `follows` are sound.
- `validate_for_gate_approval` repeats those checks and adds the ones that Sections 24.1 to 24.9
  require when the gate definitions are approved.

Both take the parsed YAML document, never a file, and return a `Report`. Nothing is written.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final

from ggsad.core.gates import DEFAULT_RETRY_LIMIT, GateIndex, check_command_fields, check_gates
from ggsad.core.identifiers import ascii_lower, check_identifier
from ggsad.core.issues import Report, ReportBuilder
from ggsad.core.values import as_list, as_mapping, as_text, text_list

if TYPE_CHECKING:
    from collections.abc import Collection, Mapping

SUPPORTED_SCHEMA_VERSIONS: Final = ("1.0",)
METHOD_PROFILE: Final = "core"
HUMAN_PREFIX: Final = "human:"
_VERSION: Final = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
_REQUIRED: Final = (
    "schema_version",
    "id",
    "method_profile",
    "compliance_profile",
    "author",
    "owner",
    "goal",
    "requirements",
)
_OPTIONAL: Final = ("scope", "gates", "follows", "approver", "required_tools", "agent_may_close")
_REQUIREMENT_KEYS: Final = frozenset(
    {"id", "text", "examples", "done_when", "evidence", "human_check"}
)


@dataclass(frozen=True)
class ProjectContext:
    """What a definition is judged against: the project, not the definition itself."""

    compliance_profile: str
    existing_ids: Collection[str] = ()
    closed_ids: Collection[str] = ()
    approved_humans: Collection[str] | None = None
    default_retry_limit: int = DEFAULT_RETRY_LIMIT


def validate_for_new(definition: object, context: ProjectContext) -> Report:
    """Check a change definition for the `new` action (Sections 23.1 and 23.3)."""
    return _validate(definition, context, approval=False)


def validate_for_gate_approval(definition: object, context: ProjectContext) -> Report:
    """Check a change definition before its gate definitions are approved (Section 24.1)."""
    return _validate(definition, context, approval=True)


def _validate(definition: object, context: ProjectContext, *, approval: bool) -> Report:
    rb = ReportBuilder()
    root = as_mapping(definition)
    if root is None:
        rb.error("definition-invalid", "a change definition is a mapping", "")
        return rb.build()
    if not _check_schema_version(root, rb):
        return rb.build()
    _check_fields(root, rb)
    _check_id(root, context, rb, approval=approval)
    _check_profiles(root, context, rb)
    _check_roles(root, context, rb)
    _check_follows(root, context, rb)
    _check_body(root, context, rb, approval=approval)
    _check_options(root, rb)
    return rb.build()


def _check_body(
    root: Mapping[str, object], context: ProjectContext, rb: ReportBuilder, *, approval: bool
) -> None:
    """Goal, gates, scope, and requirements. A field that is present is never skipped."""
    sentences = _check_goal(root["goal"], rb) if "goal" in root else None
    index = _check_gates_and_scope(root, rb, context, approval=approval)
    requirements = _Requirements(sentences, index, rb, approval)
    covered = requirements.check(root["requirements"]) if "requirements" in root else set()
    if approval and sentences is not None:
        _check_coverage(sentences, covered, rb)


def _check_schema_version(root: Mapping[str, object], rb: ReportBuilder) -> bool:
    """Section 25.3 of the Implementation Contract: refuse an unusable version, write nothing."""
    version = root.get("schema_version")
    if isinstance(version, str) and version in SUPPORTED_SCHEMA_VERSIONS:
        return True
    shown = f"{version!r}" if _VERSION.fullmatch(str(version)) is None else version
    rb.error(
        "schema-version-unsupported",
        f"schema_version {shown} is not supported; supported: {list(SUPPORTED_SCHEMA_VERSIONS)}",
        "schema_version",
    )
    return False


def _check_fields(root: Mapping[str, object], rb: ReportBuilder) -> None:
    for name in _REQUIRED:
        if name not in root:
            rb.error("field-missing", f"field {name!r} is required", name)
    for name in sorted(set(root) - {*_REQUIRED, *_OPTIONAL}):
        rb.error("field-unknown", f"unknown field {name!r}", name)


def _check_id(
    root: Mapping[str, object], context: ProjectContext, rb: ReportBuilder, *, approval: bool
) -> None:
    if "id" not in root:
        return
    identifier = root["id"]
    if not isinstance(identifier, str):
        rb.error("id-invalid", "the identifier must be a string", "id")
        return
    existing: Collection[str] = context.existing_ids
    if approval:
        # The change already exists; only the other changes can collide with it.
        existing = [e for e in existing if ascii_lower(e) != ascii_lower(identifier)]
    for issue in check_identifier(identifier, existing=existing):
        rb.error(issue.code, issue.message, issue.path)


def _check_profiles(root: Mapping[str, object], context: ProjectContext, rb: ReportBuilder) -> None:
    method = root.get("method_profile")
    if "method_profile" in root and method != METHOD_PROFILE:
        rb.error(
            "method-profile-invalid",
            f"method_profile must be exactly {METHOD_PROFILE!r}, not {method!r}",
            "method_profile",
        )
    profile = root.get("compliance_profile")
    if "compliance_profile" in root and profile != context.compliance_profile:
        rb.error(
            "compliance-profile-mismatch",
            f"compliance_profile {profile!r} differs from the project's "
            f"{context.compliance_profile!r}",
            "compliance_profile",
        )


def _check_roles(root: Mapping[str, object], context: ProjectContext, rb: ReportBuilder) -> None:
    """Section 3.11: author, owner, and approver are humans; the first two must be approved."""
    for name in ("author", "owner"):
        if name in root:
            _check_person(name, root[name], context.approved_humans, rb)
    _check_approver(root, context.approved_humans, rb)


def _check_person(
    name: str, value: object, approved: Collection[str] | None, rb: ReportBuilder
) -> None:
    if not isinstance(value, str) or not value.startswith(HUMAN_PREFIX):
        rb.error("role-not-human", f"{name} must be a human identity (human:<name>)", name)
    elif approved is not None and value not in approved:
        rb.error("human-not-approved", f"{value!r} is not an approved human", name)


def _check_approver(
    root: Mapping[str, object], approved: Collection[str] | None, rb: ReportBuilder
) -> None:
    if "approver" not in root:
        rb.warn("approver-fallback", "no approver is named; the Change owner approves", "approver")
        return
    approver = root["approver"]
    if not isinstance(approver, str) or not approver.startswith(HUMAN_PREFIX):
        rb.error("role-not-human", "approver must be a human identity (human:<name>)", "approver")
    elif approved is not None and approver not in approved:
        rb.warn(
            "approver-fallback",
            f"{approver!r} is not an approved human; the Change owner approves",
            "approver",
        )


def _check_follows(root: Mapping[str, object], context: ProjectContext, rb: ReportBuilder) -> None:
    if "follows" not in root:
        return
    follows = root["follows"]
    if not isinstance(follows, str) or check_identifier(follows):
        rb.error("follows-invalid", "follows must be a valid change identifier", "follows")
    elif follows not in context.closed_ids:
        rb.error(
            "follows-invalid",
            f"follows names {follows!r}, which does not exist or is not closed",
            "follows",
        )


def _check_goal(value: object, rb: ReportBuilder) -> list[str] | None:
    """Check the goal (Section 3.1) and return its done_when sentences, None when unreadable."""
    goal = as_mapping(value)
    if goal is None:
        rb.error("field-type-invalid", "goal must be a mapping", "goal")
        return None
    _check_goal_members(goal, rb)
    return _goal_sentences(goal, rb)


def _check_goal_members(goal: Mapping[str, object], rb: ReportBuilder) -> None:
    for name in ("problem", "done_when", "non_goals"):
        if name not in goal:
            rb.error("field-missing", f"goal.{name} is required", f"goal.{name}")
    for name in sorted(set(goal) - {"problem", "done_when", "non_goals"}):
        rb.error("field-unknown", f"unknown field {name!r} in goal", f"goal.{name}")
    if "problem" in goal and as_text(goal["problem"]) is None:
        rb.error("field-type-invalid", "goal.problem must be a non-empty text", "goal.problem")
    if "non_goals" in goal and as_list(goal["non_goals"]) is None:
        rb.error("field-type-invalid", "goal.non_goals must be a list", "goal.non_goals")


def _goal_sentences(goal: Mapping[str, object], rb: ReportBuilder) -> list[str] | None:
    if "done_when" not in goal:
        return None
    sentences = text_list(goal["done_when"])
    if not sentences:
        rb.error(
            "field-type-invalid",
            "goal.done_when is a non-empty list of sentences",
            "goal.done_when",
        )
        return None
    return sentences


def _check_gates_and_scope(
    root: Mapping[str, object], rb: ReportBuilder, context: ProjectContext, *, approval: bool
) -> GateIndex:
    index = GateIndex()
    if "gates" in root:
        index = check_gates(
            root["gates"], rb, approval=approval, default_retry_limit=context.default_retry_limit
        )
    elif approval:
        rb.error("gates-absent", "the gate definitions cannot be approved without gates", "gates")
    if "scope" in root:
        _check_scope(root["scope"], rb, approval=approval)
    elif approval:
        rb.error("scope-absent", "the allowed path list is required for approval", "scope")
    return index


def _scope_allow(value: object) -> list[object] | None:
    scope = as_mapping(value)
    if scope is None or set(scope) != {"allow"}:
        return None
    return as_list(scope["allow"])


def _check_scope(value: object, rb: ReportBuilder, *, approval: bool) -> None:
    allow = _scope_allow(value)
    if allow is None:
        rb.error("field-type-invalid", "scope holds exactly the list allow", "scope")
        return
    if not approval:
        return
    for index, pattern in enumerate(allow):
        if not _pattern_ok(pattern):
            rb.error(
                "scope-pattern-invalid",
                f"path pattern {pattern!r} is empty, begins with '/', or has a '..' segment",
                f"scope.allow[{index}]",
            )


def _pattern_ok(pattern: object) -> bool:
    return (
        isinstance(pattern, str)
        and pattern != ""
        and not pattern.startswith("/")
        and ".." not in pattern.split("/")
    )


@dataclass
class _Requirements:
    """State shared by the checks of the requirements of one definition."""

    sentences: list[str] | None
    index: GateIndex
    rb: ReportBuilder
    approval: bool
    seen: set[str] = field(default_factory=set)
    covered: set[str] = field(default_factory=set)

    def check(self, value: object) -> set[str]:
        """Check the requirements and return the done_when sentences with evidence behind them."""
        items = as_list(value)
        if items is None:
            self.rb.error("field-type-invalid", "requirements must be a list", "requirements")
            return self.covered
        for position, item in enumerate(items):
            path = f"requirements[{position}]"
            requirement = as_mapping(item)
            if requirement is None:
                self.rb.error("requirement-invalid", "a requirement is a mapping", path)
            elif self._check_one(requirement, path):
                self.covered.update(text_list(requirement.get("done_when", [])) or [])
        return self.covered

    def _check_one(self, requirement: Mapping[str, object], path: str) -> bool:
        """Check one requirement. True when it has an evidence command or a human check."""
        for key in sorted(set(requirement) - _REQUIREMENT_KEYS):
            self.rb.error(
                "requirement-invalid", f"unknown member {key!r} in a requirement", f"{path}.{key}"
            )
        self._check_identity(requirement, path)
        self._check_sentences(requirement.get("done_when", []), f"{path}.done_when")
        commands = self._check_evidence(requirement.get("evidence", []), f"{path}.evidence")
        human = "human_check" in requirement and self._check_human_check(
            requirement["human_check"], f"{path}.human_check"
        )
        return commands > 0 or human

    def _check_identity(self, requirement: Mapping[str, object], path: str) -> None:
        identifier = as_text(requirement.get("id"))
        if identifier is None or as_text(requirement.get("text")) is None:
            self.rb.error("requirement-invalid", "a requirement needs an id and a text", path)
        elif identifier in self.seen:
            self.rb.error(
                "requirement-id-duplicate", f"requirement id {identifier!r} is repeated", path
            )
        else:
            self.seen.add(identifier)

    def _check_sentences(self, value: object, path: str) -> None:
        listed = text_list(value)
        if listed is None:
            self.rb.error("requirement-invalid", "done_when is a list of sentences", path)
            return
        for sentence in listed:
            if self.sentences is not None and sentence not in self.sentences:
                self.rb.error(
                    "done-when-unknown",
                    f"{sentence!r} is not a done_when sentence of the goal",
                    path,
                )

    def _check_evidence(self, value: object, path: str) -> int:
        """Check the evidence commands and return how many are well formed."""
        items = as_list(value)
        if items is None:
            self.rb.error("requirement-invalid", "evidence is a list of commands", path)
            return 0
        well_formed = 0
        for position, item in enumerate(items):
            command = as_mapping(item)
            if command is None or "command" not in command:
                self.rb.error("requirement-invalid", "an evidence entry holds a command", path)
                continue
            check_command_fields(command, f"{path}[{position}]", self.rb, required=self.approval)
            well_formed += 1
        return well_formed

    def _check_human_check(self, value: object, path: str) -> bool:
        """A human check names a reason and a sign-off gate (Section 24.9)."""
        check = as_mapping(value)
        if (
            check is None
            or set(check) != {"reason", "gate"}
            or any(as_text(part) is None for part in check.values())
        ):
            self.rb.error("human-check-invalid", "a human check holds a reason and a gate", path)
            return False
        if self.approval and check["gate"] not in self.index.sign_off_ids:
            self.rb.error(
                "human-check-invalid",
                f"{check['gate']!r} is not a done gate of the kind 'sign-off'",
                f"{path}.gate",
            )
            return False
        return True


def _check_coverage(sentences: list[str], covered: set[str], rb: ReportBuilder) -> None:
    """Section 23.1: every done_when sentence is covered by a requirement with evidence."""
    missing = [sentence for sentence in sentences if sentence not in covered]
    if missing:
        rb.error(
            "done-when-uncovered",
            "no requirement with an evidence command or a human check covers: "
            + "; ".join(repr(sentence) for sentence in missing),
            "goal.done_when",
        )


def _check_options(root: Mapping[str, object], rb: ReportBuilder) -> None:
    if "required_tools" in root and text_list(root["required_tools"]) is None:
        rb.error(
            "field-type-invalid",
            "required_tools is a list of program names",
            "required_tools",
        )
    if "agent_may_close" in root and not isinstance(root["agent_may_close"], bool):
        rb.error("field-type-invalid", "agent_may_close is true or false", "agent_may_close")
