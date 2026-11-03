"""The model of the gates of the `core` profile: types, constants, and parsing.

Gates are parsed from a validated definition into typed values. Evaluation is in `gate_eval`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final, Literal

from ggsad.core.gates import DEFAULT_RETRY_LIMIT
from ggsad.core.values import as_int, as_list, as_mapping, as_text, text_list

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

SATISFIED: Final = "satisfied"
NOT_SATISFIED: Final = "not_satisfied"
NOT_EVALUABLE: Final = "not_evaluable"
NOT_APPLICABLE: Final = "not_applicable"
LEVEL_ORDER: Final = {"A0": 0, "A1": 1, "A2": 2}
# Which groups of gates an action evaluates (Section 23.6).
GROUPS_FOR: Final[dict[str, tuple[str, ...]]] = {
    "close": ("fail", "wait", "done"),
    "resume": ("fail", "wait"),
    "start": ("fail", "wait"),
    "cancel": ("fail",),
    "supersede": ("fail",),
}
ALL_GROUPS: Final = ("fail", "wait", "done")


@dataclass(frozen=True)
class ExitMap:
    """The exit statuses that mean each result of a check command (Section 24.2)."""

    satisfied: frozenset[int] = frozenset()
    not_satisfied: frozenset[int] = frozenset()
    not_evaluable: frozenset[int] = frozenset()

    def result_for(self, status: int) -> str:
        """The result of an exit status; a status that is not mapped is not evaluable."""
        if status in self.satisfied:
            return SATISFIED
        if status in self.not_satisfied:
            return NOT_SATISFIED
        return NOT_EVALUABLE


@dataclass(frozen=True)
class CommandSpec:
    """A check command: argument list, exit map, and an optional time limit in seconds."""

    command: tuple[str, ...]
    exit_map: ExitMap
    time_limit: int | None = None


@dataclass(frozen=True)
class ExtractRule:
    """How failure identifiers are found in the output of a command (Section 24.6)."""

    pattern: str
    stream: str = "stdout"


@dataclass(frozen=True)
class BaselineEntry:
    """A known failure that the change is not required to fix."""

    id: str
    reason: str = ""
    review_by: str = ""


@dataclass(frozen=True)
class EvidenceCommand:
    """An evidence command bound to a requirement (Section 24.9)."""

    spec: CommandSpec


@dataclass(frozen=True)
class Requirement:
    """A requirement with its evidence commands, or a human check with a sign-off gate."""

    id: str
    commands: tuple[EvidenceCommand, ...] = ()
    human_gate: str | None = None


@dataclass(frozen=True)
class Gate:
    """One gate. `kind` is the done-gate kind or the member of a condition of a fail/wait gate."""

    id: str
    group: str
    kind: str
    severity: str | None = None
    command: CommandSpec | None = None
    retry_gate: str | None = None
    limit: int | None = None
    predicate: str | None = None
    minimum_level: str | None = None
    baseline: tuple[BaselineEntry, ...] | None = None
    extract: ExtractRule | None = None
    requirements: tuple[Requirement, ...] = ()


@dataclass(frozen=True)
class RunOutcome:
    """What a runner reports about one command. The engine decides what it means."""

    kind: Literal["exit", "timeout", "cannot-start", "no-status"]
    status: int | None = None
    cause: str = ""
    program_missing: bool = False
    stdout: str = ""
    stderr: str = ""
    ran: str = ""
    truncated: bool = False


type Runner = Callable[[tuple[str, ...], int | None], RunOutcome]


@dataclass(frozen=True)
class Check:
    """A result handed in by the caller for a check that needs files or version control."""

    result: str
    detail: str = ""


@dataclass(frozen=True)
class Facts:
    """What the caller observed. A fact that is not handed in is `not_evaluable`."""

    scope: Check | None = None
    stale_spec_approval: Check | None = None
    review_gaps: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    review_hash: str | None = None
    not_satisfied_counts: Mapping[str, int] = field(default_factory=dict)
    definitions_hash: str | None = None
    spec_hash: str | None = None
    documents: Mapping[str, str] = field(default_factory=dict)
    gates_approved: bool = False
    spec_approval_ok: bool = True
    revision: str | None = None
    unclean_paths: tuple[str, ...] = ()
    target_issues: Mapping[str, tuple[tuple[str, str], ...]] = field(default_factory=dict)
    open_changes: frozenset[str] = frozenset()
    has_anchor: bool = False
    history_damaged: bool = False


@dataclass(frozen=True)
class Outcome:
    """The result and detail of one gate evaluation."""

    result: str
    detail: str = ""


@dataclass(frozen=True)
class Decision:
    """What the results decide (Section 24.2): fail, external, soft, wait, done, or none."""

    kind: str = "none"  # none, fail, external, soft, wait, or done
    gate_ids: tuple[str, ...] = ()
    detail: str = ""


@dataclass(frozen=True)
class Evaluation:
    """The recorded results of one evaluation and what they decide."""

    results: Mapping[str, str]
    details: Mapping[str, str]
    decision: Decision
    covered: tuple[str, ...] = ()


# --------------------------------------------------------------------------- parsing


def parse_gates(
    gates: object,
    default_retry_limit: int = DEFAULT_RETRY_LIMIT,
    requirements: object = None,
) -> tuple[Gate, ...]:
    """Turn a valid `gates` definition into gates, with the base gates and implicit retry limits.

    The definition is assumed to have passed `validate_for_gate_approval`; a malformed entry is
    skipped rather than raising.
    """
    mapping = as_mapping(gates) or {}
    evidence = Gate(
        "incomplete-evidence", "done", "evidence", requirements=parse_requirements(requirements)
    )
    parsed: list[Gate] = [g for g in _BASE_GATES if g.id != "incomplete-evidence"] + [evidence]
    for group in ALL_GROUPS:
        for item in as_list(mapping.get(group)) or []:
            gate = _parse_gate(group, as_mapping(item))
            if gate is not None:
                parsed.append(gate)
    return (*parsed, *_implicit_retry_gates(parsed, default_retry_limit))


_BASE_GATES: Final = (
    Gate("scope-violation", "fail", "predicate", "hard", predicate="scope-violation"),
    Gate("unanswered-question", "wait", "predicate", predicate="unanswered-question"),
    Gate("stale-spec-approval", "wait", "predicate", predicate="stale-spec-approval"),
)


def _implicit_retry_gates(gates: Sequence[Gate], default: int) -> list[Gate]:
    covered = {g.retry_gate for g in gates if g.kind == "retry_limit"}
    return [
        Gate(f"{g.id}#retry-limit", "fail", "retry_limit", "soft", retry_gate=g.id, limit=default)
        for g in gates
        if g.group == "done" and g.kind == "check" and g.id not in covered
    ]


def _parse_gate(group: str, item: Mapping[str, object] | None) -> Gate | None:
    gate_id = as_text(item.get("id")) if item is not None else None
    if item is None or gate_id is None or group not in ALL_GROUPS:
        return None
    if group == "done":
        kind = as_text(item.get("kind")) or ""
        return Gate(
            gate_id,
            "done",
            kind,
            command=_parse_command(item) if kind == "check" else None,
            minimum_level=as_text(item.get("minimum_level")),
            baseline=_parse_baseline(item.get("baseline")),
            extract=_parse_extract(item.get("extract")),
        )
    return _parse_condition(group, gate_id, item)


def _parse_condition(group: str, gate_id: str, item: Mapping[str, object]) -> Gate | None:
    cond = as_mapping(item.get("condition"))
    if cond is None:
        return None
    severity = as_text(item.get("severity")) if group == "fail" else None
    if "predicate" in cond:
        return Gate(gate_id, group, "predicate", severity, predicate=as_text(cond["predicate"]))
    spec = as_mapping(cond.get("retry_limit"))
    if spec is not None:
        return Gate(
            gate_id,
            group,
            "retry_limit",
            "soft",
            retry_gate=as_text(spec.get("gate")),
            limit=as_int(spec.get("limit")),
        )
    return Gate(gate_id, group, "command", severity, command=_parse_command(cond))


def _parse_command(holder: Mapping[str, object]) -> CommandSpec | None:
    command = text_list(holder.get("command"))
    exit_map = as_mapping(holder.get("exit_map"))
    if not command or exit_map is None:
        return None
    limit = as_int(holder.get("time_limit"))
    return CommandSpec(command=tuple(command), exit_map=_parse_exit_map(exit_map), time_limit=limit)


def _statuses(value: object) -> frozenset[int]:
    return frozenset(n for n in (as_int(s) for s in as_list(value) or []) if n is not None)


def _parse_exit_map(exit_map: Mapping[str, object]) -> ExitMap:
    return ExitMap(
        _statuses(exit_map.get(SATISFIED)),
        _statuses(exit_map.get(NOT_SATISFIED)),
        _statuses(exit_map.get(NOT_EVALUABLE)),
    )


def _parse_baseline(value: object) -> tuple[BaselineEntry, ...] | None:
    if value is None:
        return None
    entries = []
    for item in as_list(value) or []:
        entry = as_mapping(item) or {}
        identifier = as_text(entry.get("id"))
        if identifier is not None:
            entries.append(BaselineEntry(identifier, as_text(entry.get("reason")) or ""))
    return tuple(entries)


def _parse_extract(value: object) -> ExtractRule | None:
    rule = as_mapping(value)
    pattern = as_text(rule.get("pattern")) if rule else None
    if rule is None or pattern is None:
        return None
    return ExtractRule(pattern, as_text(rule.get("stream")) or "stdout")


def _evidence_commands(value: object) -> tuple[EvidenceCommand, ...]:
    specs = (_parse_command(as_mapping(entry) or {}) for entry in as_list(value) or [])
    return tuple(EvidenceCommand(spec) for spec in specs if spec is not None)


def _parse_requirement(item: object) -> Requirement | None:
    requirement = as_mapping(item)
    identifier = as_text(requirement.get("id")) if requirement else None
    if requirement is None or identifier is None:
        return None
    human = as_mapping(requirement.get("human_check")) or {}
    commands = _evidence_commands(requirement.get("evidence"))
    return Requirement(identifier, commands, as_text(human.get("gate")))


def parse_requirements(value: object) -> tuple[Requirement, ...]:
    """Turn the `requirements` of a change definition into requirements (Section 24.9)."""
    parsed = (_parse_requirement(item) for item in as_list(value) or [])
    return tuple(r for r in parsed if r is not None)
