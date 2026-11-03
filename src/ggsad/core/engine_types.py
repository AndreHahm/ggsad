"""Types of the engine: actors, requests, the context, steps, and results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Final

from ggsad.core.gate_eval import Evaluation, Facts, Gate, Runner, evaluate
from ggsad.core.issues import Issue
from ggsad.core.state import State

if TYPE_CHECKING:
    from collections.abc import Mapping

HUMAN_PREFIX: Final = "human:"


@dataclass(frozen=True)
class Actor:
    """The participant who performs an action (Section 24.3)."""

    identity: str
    assurance: str = "A0"
    account: str | None = None

    @property
    def is_human(self) -> bool:
        """True for a `human:` identity."""
        return self.identity.startswith(HUMAN_PREFIX)


@dataclass(frozen=True)
class Request:
    """One requested action with the inputs any action may carry."""

    action: str
    actor: Actor
    at: str
    note: str | None = None
    reason: str | None = None
    target: str | None = None
    gate: str | None = None
    question: str | None = None
    text: str | None = None
    owner: str | None = None
    options: tuple[str, ...] | None = None
    answer: str | None = None
    resume_when: str | None = None
    expires: str | None = None
    and_resume: bool = False
    about_spec: bool = False
    replaced_by: str | None = None
    documents: tuple[str, ...] = ()
    attempts: int | None = None
    content_hash: str | None = None
    files: Mapping[str, str] | None = None
    agent_report: Mapping[str, object] | None = None
    repaired: Mapping[str, object] | None = None


@dataclass(frozen=True)
class Context:
    """The roles and gates of the change, as the caller read them."""

    change_id: str = ""
    gates: tuple[Gate, ...] = ()
    change_owner: str = ""
    author: str = ""
    owner: str = ""
    requestors: frozenset[str] = frozenset()
    approved_humans: frozenset[str] | None = None
    agent_may_close: bool = False
    approver: str = ""
    compliance_profile: str = "lean"
    team_mode: str = "team"
    deputies: frozenset[str] = frozenset()
    unavailable_approvers: frozenset[str] = frozenset()
    minimum_levels: Mapping[str, str] = field(default_factory=dict)

    def is_approved_human(self, identity: str | None) -> bool:
        """True for a `human:` identity that the list of approved humans allows."""
        if identity is None or not identity.startswith(HUMAN_PREFIX):
            return False
        return self.approved_humans is None or identity in self.approved_humans


@dataclass(frozen=True)
class ActionResult:
    """What one action did. `bodies` are the entry bodies to append, in order."""

    operation: str
    result: str
    issues: tuple[Issue, ...]
    state: State
    bodies: tuple[dict[str, object], ...] = ()
    data: Mapping[str, object] = field(default_factory=dict)

    @property
    def changed(self) -> bool:
        """True when something must be recorded (Section 22.2)."""
        return bool(self.bodies)

    @property
    def codes(self) -> tuple[str, ...]:
        """The issue codes, which makes assertions short."""
        return tuple(issue.code for issue in self.issues)


class Rejected(Exception):  # noqa: N818 - a control-flow signal, not an error
    """The request is invalid or a precondition is not met: nothing is written."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.issue = Issue(code, message)


@dataclass
class Step:
    """What a handler decided: the new state and what to record."""

    state: State
    result: str = "success"
    issues: tuple[Issue, ...] = ()
    evaluation: Evaluation | None = None
    files: Mapping[str, str] | None = None
    data: dict[str, object] = field(default_factory=dict)
    action: str | None = None
    chained: Step | None = None
    note: str | None = None


@dataclass(frozen=True)
class Call:
    """Everything a handler may read."""

    request: Request
    state: State
    context: Context
    facts: Facts
    runner: Runner

    def need(self, value: str | None, code: str, message: str) -> str:
        """A required, non-blank text input, or reject."""
        if value is None or not value.strip():
            raise Rejected(code, message)
        return value

    def evaluate(self) -> Evaluation:
        """Evaluate the gates for the requested action."""
        return evaluate(
            self.request.action, self.context.gates, self.state, self.facts, self.runner
        )
