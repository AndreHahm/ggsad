"""Shared helpers of the engine tests."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, cast

from ggsad.core.canonical import ZERO_HASH
from ggsad.core.engine import apply
from ggsad.core.engine_types import ActionResult, Actor, Context, Request
from ggsad.core.gate_eval import Check, Facts, RunOutcome, parse_gates
from ggsad.core.history import make_entry
from ggsad.core.state import State

ADA = Actor("human:ada", "A1")
AGENT = Actor("agent:codex")
NOW = "2026-11-03T10:00:00Z"
CLEAR = Facts(
    scope=Check("not_satisfied"),
    stale_spec_approval=Check("not_satisfied"),
    evidence=Check("satisfied"),
    gates_approved=True,
    revision="r1",
)


def check_gate(gate_id: str = "tests-pass", program: str = "pytest") -> dict[str, Any]:
    return {
        "id": gate_id,
        "kind": "check",
        "command": [program],
        "exit_map": {"satisfied": [0], "not_satisfied": [1], "not_evaluable": [9]},
    }


def definition(fail: list[Any] | None = None, wait: list[Any] | None = None,
               done: list[Any] | None = None) -> dict[str, Any]:  # fmt: skip
    return {"fail": fail or [], "wait": wait or [], "done": done or []}


def context(gates: dict[str, Any] | None = None, **kw: Any) -> Context:
    base = Context(
        change_id="C-1",
        gates=parse_gates(gates or definition()),
        change_owner="human:ada",
        author="human:ada",
        owner="human:ada",
        requestors=frozenset({"agent:codex"}),
    )
    return replace(base, **kw)


def cmd_gate(gate_id: str, severity: str, program: str) -> dict[str, Any]:
    """A fail gate that is active when the program exits with 1."""
    exit_map = {"satisfied": [1], "not_satisfied": [0]}
    return {"id": gate_id, "severity": severity,
            "condition": {"command": [program], "exit_map": exit_map}}  # fmt: skip


def runner(results: dict[str, RunOutcome] | None = None):
    table = results or {}

    def run(command: tuple[str, ...], limit: int | None) -> RunOutcome:
        return table.get(command[0], RunOutcome("exit", status=0))

    return run


def req(action: str, actor: Actor = ADA, **kw: Any) -> Request:
    return Request(action, actor, NOW, **kw)


def active(**kw: Any) -> State:
    return State(state="active", base_revision="r1", **kw)


def do(state: State | None, request: Request, ctx: Context | None = None,
       facts: Facts = CLEAR, run: Any = None) -> ActionResult:  # fmt: skip
    result = apply(state, request, ctx or context(), facts, run or runner())
    assert_consistent(result)
    return result


def gate_results(result: ActionResult) -> dict[str, str]:
    return cast("dict[str, str]", result.bodies[0]["gate_results"])


def gate_detail(result: ActionResult) -> dict[str, str]:
    return cast("dict[str, str]", result.bodies[0]["gate_detail"])


def assert_consistent(result: ActionResult) -> None:
    """Section 22.2 and 25.1: the envelope rules, and every body is a valid entry."""
    assert result.result in {"success", "rejected", "blocked", "error"}
    if result.result == "rejected":
        assert not result.changed
        assert result.issues
    if result.result == "blocked":
        assert result.changed
        assert result.issues
    if result.result == "success":
        assert not result.issues
    for index, body in enumerate(result.bodies, start=1):
        make_entry(index, ZERO_HASH, body)
    if result.bodies:
        assert State.from_json(result.bodies[-1]["after"]) == result.state
