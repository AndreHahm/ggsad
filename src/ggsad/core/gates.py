"""Gate definitions of a change (Sections 5.3, 23.3, 23.7, 24.2, 24.6, and 24.7).

The checks run in two stages. The creation stage (`approval=False`) checks the structure that
Section 23.3 requires when a change is created. The approval stage (`approval=True`) adds the
checks that Sections 24.1, 24.2, 24.5, 24.6, and 24.7 require when the gate definitions are
approved: complete commands and exit maps, retry limits, and baselines.

Field names that the specification leaves open are fixed here and documented in the pull request:
`gates.not_applicable` (how a definition states that a base gate does not apply), the layout of an
exit map (`satisfied`, `not_satisfied`, `not_evaluable`), and the baseline entry fields.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import TYPE_CHECKING, Final

from ggsad.core.values import as_int, as_list, as_mapping, as_text, text_list

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ggsad.core.issues import ReportBuilder

LIST_NAMES: Final = ("fail", "wait", "done")
SEVERITIES: Final = frozenset({"hard", "soft"})
DONE_KINDS: Final = frozenset({"check", "sign-off", "review"})
ASSURANCE_LEVELS: Final = frozenset({"A0", "A1", "A2"})
EXIT_RESULTS: Final = ("satisfied", "not_satisfied", "not_evaluable")
CONDITION_MEMBERS: Final = ("command", "retry_limit", "predicate")
FAIL_PREDICATES: Final = frozenset({"scope-violation"})
WAIT_PREDICATES: Final = frozenset({"unanswered-question", "stale-spec-approval"})
DEFAULT_RETRY_LIMIT: Final = 3


def _is_member(value: object, allowed: frozenset[str]) -> bool:
    """True when the value is a string in the set; a list or mapping never raises."""
    return isinstance(value, str) and value in allowed


@dataclass(frozen=True)
class BaseGate:
    """A base gate of Section 23.7, as the definition may not redefine it."""

    list_name: str
    severity: str | None
    predicate: str | None


BASE_GATES: Final[dict[str, BaseGate]] = {
    "scope-violation": BaseGate("fail", "hard", "scope-violation"),
    "unanswered-question": BaseGate("wait", None, "unanswered-question"),
    "stale-spec-approval": BaseGate("wait", None, "stale-spec-approval"),
    "incomplete-evidence": BaseGate("done", None, None),
}


@dataclass(frozen=True)
class GateIndex:
    """What later checks need to know about the gates of a definition."""

    done_check_ids: frozenset[str] = frozenset()
    sign_off_ids: frozenset[str] = frozenset()


@dataclass
class _Context:
    rb: ReportBuilder
    approval: bool
    default_retry_limit: int
    seen: dict[str, str] = field(default_factory=dict)
    done_check_ids: set[str] = field(default_factory=set)
    sign_off_ids: set[str] = field(default_factory=set)
    retry_refs: list[tuple[str, str]] = field(default_factory=list)


def check_gates(
    value: object,
    rb: ReportBuilder,
    *,
    approval: bool,
    default_retry_limit: int = DEFAULT_RETRY_LIMIT,
) -> GateIndex:
    """Check the `gates` field and return the index of its done gates."""
    ctx = _Context(rb, approval, default_retry_limit)
    gates = as_mapping(value)
    if gates is None:
        rb.error("field-type-invalid", "gates must be a mapping", "gates")
        return GateIndex()
    for key in sorted(set(gates) - {*LIST_NAMES, "not_applicable"}):
        rb.error("field-unknown", f"unknown field {key!r} in gates", f"gates.{key}")
    if "not_applicable" in gates:
        _check_not_applicable(gates["not_applicable"], ctx)
    for list_name in LIST_NAMES:
        _check_list(list_name, gates.get(list_name), ctx)
    _check_retry_refs(ctx)
    return GateIndex(frozenset(ctx.done_check_ids), frozenset(ctx.sign_off_ids))


def _check_not_applicable(value: object, ctx: _Context) -> None:
    ids = text_list(value)
    if ids is None:
        ctx.rb.error(
            "field-type-invalid",
            "gates.not_applicable must be a list of gate identifiers",
            "gates.not_applicable",
        )
        return
    for gate_id in ids:
        if gate_id in BASE_GATES:
            ctx.rb.error(
                "gate-weakened",
                f"base gate {gate_id!r} is removed: a change cannot state that it does not apply",
                "gates.not_applicable",
            )
        else:
            ctx.rb.error(
                "gate-unknown",
                f"gates.not_applicable names {gate_id!r}, which is not a base gate",
                "gates.not_applicable",
            )


def _check_list(list_name: str, value: object, ctx: _Context) -> None:
    if value is None:
        ctx.rb.error("field-missing", f"gates.{list_name} is required", f"gates.{list_name}")
        return
    items = as_list(value)
    if items is None:
        ctx.rb.error(
            "field-type-invalid", f"gates.{list_name} must be a list", f"gates.{list_name}"
        )
        return
    for index, item in enumerate(items):
        _check_entry(list_name, f"gates.{list_name}[{index}]", item, ctx)


def _check_entry(list_name: str, path: str, item: object, ctx: _Context) -> None:
    gate = as_mapping(item)
    gate_id = as_text(gate.get("id")) if gate is not None else None
    if gate is None or gate_id is None:
        ctx.rb.error("gate-invalid", "a gate must be a mapping with a non-empty id", path)
        return
    if gate_id in BASE_GATES:
        _check_base_collision(gate_id, list_name, gate, path, ctx)
        return
    if gate_id in ctx.seen:
        ctx.rb.error(
            "gate-id-duplicate",
            f"gate identifier {gate_id!r} is already used at {ctx.seen[gate_id]}",
            path,
        )
        return
    ctx.seen[gate_id] = path
    if list_name == "fail":
        _check_fail_gate(gate, path, ctx)
    elif list_name == "wait":
        _check_wait_gate(gate, path, ctx)
    else:
        _check_done_gate(gate_id, gate, path, ctx)


def _check_base_collision(
    gate_id: str, list_name: str, gate: Mapping[str, object], path: str, ctx: _Context
) -> None:
    """A gate with the identifier of a base gate redefines it (Sections 5.3 and 23.7)."""
    base = BASE_GATES[gate_id]
    condition = as_mapping(gate.get("condition"))
    same_list = list_name == base.list_name
    same_condition = (
        base.predicate is not None
        and condition is not None
        and dict(condition) == {"predicate": base.predicate}
    )
    severity = gate.get("severity")
    if same_list and same_condition and severity == base.severity:
        ctx.rb.error(
            "gate-id-duplicate",
            f"gate identifier {gate_id!r} is the identifier of a base gate and is listed again",
            path,
        )
        return
    manner = "severity lowered" if same_list and same_condition else "altered"
    ctx.rb.error("gate-weakened", f"base gate {gate_id!r} is {manner}", path)


def _check_keys(
    gate: Mapping[str, object], allowed: frozenset[str], path: str, ctx: _Context
) -> None:
    for key in sorted(set(gate) - allowed):
        ctx.rb.error("gate-invalid", f"unknown member {key!r} in a gate", f"{path}.{key}")


def _check_fail_gate(gate: Mapping[str, object], path: str, ctx: _Context) -> None:
    _check_keys(gate, frozenset({"id", "description", "severity", "condition"}), path, ctx)
    severity = gate.get("severity")
    if not _is_member(severity, SEVERITIES):
        ctx.rb.error(
            "severity-invalid",
            "a fail gate needs the severity 'hard' or 'soft' in exact lowercase",
            f"{path}.severity",
        )
    member = _check_condition(gate.get("condition"), "fail", f"{path}.condition", ctx)
    if member == "retry_limit" and severity == "hard":
        ctx.rb.error(
            "severity-invalid",
            "a retry limit is a soft fail condition and cannot declare the severity 'hard'",
            f"{path}.severity",
        )


def _check_wait_gate(gate: Mapping[str, object], path: str, ctx: _Context) -> None:
    _check_keys(gate, frozenset({"id", "description", "condition"}), path, ctx)
    _check_condition(gate.get("condition"), "wait", f"{path}.condition", ctx)


def _check_done_gate(gate_id: str, gate: Mapping[str, object], path: str, ctx: _Context) -> None:
    kind = gate.get("kind")
    if not _is_member(kind, DONE_KINDS) or not isinstance(kind, str):
        ctx.rb.error(
            "done-gate-kind-invalid",
            "a done gate has exactly one kind: 'check', 'sign-off', or 'review'",
            f"{path}.kind",
        )
        return
    common = {"id", "description", "kind"}
    if kind == "check":
        ctx.done_check_ids.add(gate_id)
        _check_keys(
            gate,
            frozenset(common | {"command", "exit_map", "time_limit", "baseline", "extract"}),
            path,
            ctx,
        )
        check_command_fields(gate, path, ctx.rb, required=ctx.approval)
        if "extract" in gate:
            _check_extract(gate["extract"], f"{path}.extract", ctx)
    elif kind == "sign-off":
        ctx.sign_off_ids.add(gate_id)
        _check_keys(gate, frozenset(common | {"minimum_level", "baseline"}), path, ctx)
        if "minimum_level" in gate:
            _check_minimum_level(gate["minimum_level"], f"{path}.minimum_level", ctx)
    else:
        _check_keys(gate, frozenset(common | {"baseline"}), path, ctx)
    if ctx.approval:
        _check_baseline(gate, kind, path, ctx)


def _pattern_groups(pattern: str) -> int:
    """The number of capture groups of a pattern, or -1 when it is not a regular expression."""
    try:
        return re.compile(pattern).groups
    except re.error:
        return -1


def _check_extract(value: object, path: str, ctx: _Context) -> None:
    """An extraction rule: a pattern with one capture group and the stream to read (24.6)."""
    rule = as_mapping(value)
    pattern = as_text(rule.get("pattern")) if rule else None
    if rule is None or set(rule) - {"pattern", "stream"} or pattern is None:
        ctx.rb.error("extract-invalid", "extract holds a pattern and optionally a stream", path)
        return
    if rule.get("stream", "stdout") not in ("stdout", "stderr", "both"):
        ctx.rb.error("extract-invalid", "the stream is stdout, stderr, or both", f"{path}.stream")
    if _pattern_groups(pattern) != 1:
        ctx.rb.error(
            "extract-invalid",
            "the pattern is a regular expression with exactly one capture group",
            f"{path}.pattern",
        )


def _check_minimum_level(value: object, path: str, ctx: _Context) -> None:
    if not _is_member(value, ASSURANCE_LEVELS):
        ctx.rb.error("level-invalid", "a minimum level is 'A0', 'A1', or 'A2'", path)


def _condition_member(cond: Mapping[str, object]) -> str | None:
    """The one member that a well-formed condition holds, or None."""
    members = [name for name in CONDITION_MEMBERS if name in cond]
    extras = set(cond) - {*CONDITION_MEMBERS, "exit_map", "time_limit"}
    command_only = {"exit_map", "time_limit"} & set(cond)
    if len(members) != 1 or extras or (command_only and members != ["command"]):
        return None
    return members[0]


def _check_condition(value: object, gate_kind: str, path: str, ctx: _Context) -> str | None:
    """Check the condition of a fail or wait gate and return the member it holds."""
    cond = as_mapping(value)
    member = _condition_member(cond) if cond is not None else None
    if cond is None or member is None:
        ctx.rb.error(
            "condition-invalid",
            "a condition is a mapping that holds exactly one of command, retry_limit, and "
            "predicate (command may add exit_map and time_limit)",
            path,
        )
        return None
    if member == "command":
        check_command_fields(cond, path, ctx.rb, required=ctx.approval)
    elif member == "retry_limit":
        _check_retry_limit(cond["retry_limit"], gate_kind, f"{path}.retry_limit", ctx)
    else:
        _check_predicate(cond["predicate"], gate_kind, f"{path}.predicate", ctx)
    return member


def _check_predicate(value: object, gate_kind: str, path: str, ctx: _Context) -> None:
    allowed = FAIL_PREDICATES if gate_kind == "fail" else WAIT_PREDICATES
    if not _is_member(value, allowed):
        ctx.rb.error(
            "condition-invalid",
            f"a {gate_kind} gate may name only the predicates {sorted(allowed)}",
            path,
        )


def check_command_fields(
    holder: Mapping[str, object], path: str, rb: ReportBuilder, *, required: bool
) -> None:
    """Check command, exit_map, and time_limit of a check command (Section 24.2)."""
    _check_command(holder, path, rb, required=required)
    if "exit_map" in holder:
        _check_exit_map(holder["exit_map"], f"{path}.exit_map", rb)
    elif required and "command" in holder:
        rb.error("exit-map-invalid", "a check command needs an exit map", f"{path}.exit_map")
    if "time_limit" in holder:
        seconds = as_int(holder["time_limit"])
        if seconds is None or seconds < 1:
            rb.error(
                "time-limit-invalid", "a time limit is a positive integer", f"{path}.time_limit"
            )


def _check_command(
    holder: Mapping[str, object], path: str, rb: ReportBuilder, *, required: bool
) -> None:
    if "command" not in holder:
        if required:
            rb.error("command-missing", "a check command needs a command", f"{path}.command")
    elif not text_list(holder["command"]):
        rb.error(
            "command-invalid",
            "a command is a non-empty argument list of non-empty strings",
            f"{path}.command",
        )


def _check_exit_map(value: object, path: str, rb: ReportBuilder) -> None:
    exit_map = as_mapping(value)
    if exit_map is None:
        rb.error("exit-map-invalid", "an exit map must be a mapping", path)
        return
    for key in sorted(set(exit_map) - set(EXIT_RESULTS)):
        rb.error("exit-map-invalid", f"unknown result {key!r} in an exit map", path)
    seen: set[int] = set()
    for result in EXIT_RESULTS:
        _check_exit_statuses(result, exit_map, seen, path, rb)


def _check_exit_statuses(
    result: str, exit_map: Mapping[str, object], seen: set[int], path: str, rb: ReportBuilder
) -> None:
    statuses = as_list(exit_map.get(result))
    if statuses is None:
        if result != "not_evaluable":
            rb.error("exit-map-invalid", f"an exit map needs the list {result!r}", path)
        return
    for status in statuses:
        number = as_int(status)
        if number is None or number < 0 or number in seen:
            rb.error(
                "exit-map-invalid",
                f"exit status {status!r} must be a non-negative integer that appears once",
                path,
            )
        else:
            seen.add(number)


def _check_retry_limit(value: object, gate_kind: str, path: str, ctx: _Context) -> None:
    spec = as_mapping(value)
    if gate_kind != "fail" or spec is None or set(spec) != {"gate", "limit"}:
        ctx.rb.error(
            "condition-invalid",
            "a retry limit belongs to a fail gate and holds exactly gate and limit",
            path,
        )
        return
    target = as_text(spec["gate"])
    if target is None:
        ctx.rb.error("retry-limit-gate-invalid", "a retry limit names a done gate", path)
    else:
        ctx.retry_refs.append((target, path))
    if ctx.approval:
        _check_retry_value(spec["limit"], f"{path}.limit", ctx)


def _check_retry_value(value: object, path: str, ctx: _Context) -> None:
    limit = as_int(value)
    if limit is None or limit < 0:
        ctx.rb.error("retry-limit-invalid", "a retry limit is a non-negative integer", path)
    elif limit > ctx.default_retry_limit:
        ctx.rb.error(
            "retry-limit-invalid",
            f"a retry limit may be lower than the default {ctx.default_retry_limit} "
            "and never higher",
            path,
        )


def _check_retry_refs(ctx: _Context) -> None:
    for target, path in ctx.retry_refs:
        if target not in ctx.done_check_ids:
            ctx.rb.error(
                "retry-limit-gate-invalid",
                f"{target!r} is not a done gate of the kind 'check' of this change",
                path,
            )


def _check_baseline(gate: Mapping[str, object], kind: str, path: str, ctx: _Context) -> None:
    """A baseline is valid only on a check-command gate, with a reason and a review date."""
    if "baseline" not in gate:
        return
    where = f"{path}.baseline"
    entries = as_list(gate["baseline"])
    if kind != "check" or entries is None:
        ctx.rb.error(
            "baseline-invalid", "a baseline is a list on a done gate of the kind 'check'", where
        )
        return
    for index, entry in enumerate(entries):
        _check_baseline_entry(entry, f"{where}[{index}]", ctx)


def _check_baseline_entry(entry: object, path: str, ctx: _Context) -> None:
    fields = as_mapping(entry)
    if fields is None or set(fields) != {"id", "reason", "review_by"}:
        ctx.rb.error(
            "baseline-invalid",
            "a baseline entry holds exactly id, reason, and review_by",
            path,
        )
        return
    if as_text(fields["id"]) is None or as_text(fields["reason"]) is None:
        ctx.rb.error("baseline-invalid", "a baseline entry needs an id and a reason", path)
    if not _is_iso_date(fields["review_by"]):
        ctx.rb.error(
            "baseline-invalid", "review_by is a date written YYYY-MM-DD", f"{path}.review_by"
        )


def _is_iso_date(value: object) -> bool:
    if isinstance(value, date):
        return True
    text = as_text(value)
    if text is None:
        return False
    try:
        date.fromisoformat(text)
    except ValueError:
        return False
    return True
