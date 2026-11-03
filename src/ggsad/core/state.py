"""The state of a `core` change: the `after` record of Section 25.1, as typed values.

The record holds the whole state after an action. `State.from_json` reads it back strictly: an
unknown field, a missing field, or a value of the wrong type is refused with `StateRecordError`.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Final

from ggsad.core.issues import Issue
from ggsad.core.values import as_int, as_list, as_mapping, as_text

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

SCHEMA_VERSION: Final = "1.0"
STATES: Final = ("open", "active", "waiting", "closed")
OUTCOMES: Final = ("done", "failed", "cancelled")
WAIT_KINDS: Final = ("question", "manual", "fail-gate", "external")
ASSURANCE: Final = ("A0", "A1", "A2")


class StateRecordError(ValueError):
    """An `after` record is not valid, so it must not be used."""

    def __init__(self, message: str, path: str = "") -> None:
        super().__init__(f"{path}: {message}" if path else message)
        self.issue = Issue("state-record-invalid", message, path)


def _fail(path: str, expected: str) -> StateRecordError:
    return StateRecordError(f"must be {expected}", path)


@dataclass(frozen=True)
class Question:
    """A question that is part of the state (Section 24.8)."""

    id: str
    text: str
    owner: str
    asker: str
    options: tuple[str, ...] | None = None
    answer: str | None = None
    answerer: str | None = None

    @property
    def answered(self) -> bool:
        """True once an answer is recorded."""
        return self.answer is not None


@dataclass(frozen=True)
class Wait:
    """A wait record (Section 23.5)."""

    kind: str
    reason: str
    owner: str
    resume_when: str
    expires: str | None = None
    question: str | None = None


@dataclass(frozen=True)
class Approval:
    """One recorded approval (Sections 24.1, 24.3, 24.7).

    `gate` names the gate of a sign-off or the soft fail gate of an override. `attempts` and
    `used` are the further attempts that an override grants and the attempts already made.
    """

    target: str
    actor: str
    assurance: str
    required_level: str
    content_hash: str | None = None
    gate: str | None = None
    reason: str | None = None
    attempts: int | None = None
    used: int = 0
    definitions_hash: str | None = None


@dataclass(frozen=True)
class State:
    """The whole state of a change after an action."""

    state: str = "open"
    outcome: str | None = None
    approvals: tuple[Approval, ...] = ()
    questions: tuple[Question, ...] = ()
    wait: Wait | None = None
    base_revision: str | None = None
    replaced_by: str | None = None
    reason: str | None = None
    schema_version: str = SCHEMA_VERSION

    def with_(self, **changes: object) -> State:
        """A copy with some fields replaced."""
        return replace(self, **changes)  # type: ignore[arg-type]

    @property
    def closed(self) -> bool:
        """True when the change has ended."""
        return self.state == "closed"

    def question(self, question_id: str) -> Question | None:
        """The question with that identifier, or None."""
        return next((q for q in self.questions if q.id == question_id), None)

    @property
    def unanswered(self) -> tuple[Question, ...]:
        """The questions that have no answer."""
        return tuple(q for q in self.questions if not q.answered)

    def to_json(self) -> dict[str, object]:
        """The `after` record as a JSON-able object with every field present."""
        return {
            "state": self.state,
            "outcome": self.outcome,
            "approvals": [_approval_json(a) for a in self.approvals],
            "questions": [_question_json(q) for q in self.questions],
            "wait": None if self.wait is None else _wait_json(self.wait),
            "base_revision": self.base_revision,
            "replaced_by": self.replaced_by,
            "reason": self.reason,
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_json(cls, value: object) -> State:
        """Read an `after` record strictly, or raise StateRecordError."""
        record = _exact(value, _STATE_KEYS, "after")
        state = _choice(record["state"], STATES, "after.state")
        outcome = _optional_choice(record["outcome"], OUTCOMES, "after.outcome")
        wait = None if record["wait"] is None else _read_wait(record["wait"])
        result = cls(
            state=state,
            outcome=outcome,
            approvals=tuple(_read_list(record["approvals"], _read_approval, "after.approvals")),
            questions=tuple(_read_list(record["questions"], _read_question, "after.questions")),
            wait=wait,
            base_revision=_optional_text(record["base_revision"], "after.base_revision"),
            replaced_by=_optional_text(record["replaced_by"], "after.replaced_by"),
            reason=_optional_text(record["reason"], "after.reason"),
            schema_version=_text(record["schema_version"], "after.schema_version"),
        )
        _check_consistent(result)
        return result


def _check_consistent(state: State) -> None:
    if (state.outcome is not None) != (state.state == "closed"):
        raise _fail("after.outcome", "set exactly when the state is closed")
    if (state.wait is not None) != (state.state == "waiting"):
        raise _fail("after.wait", "set exactly when the state is waiting")
    if state.reason is not None and state.outcome != "failed":
        raise _fail("after.reason", "null unless the outcome is failed")
    if state.outcome == "failed" and state.reason is None:
        raise _fail("after.reason", "a text when the outcome is failed")


# ---------------------------------------------------------------- reading helpers

_STATE_KEYS: Final = frozenset(
    {
        "state", "outcome", "approvals", "questions", "wait", "base_revision", "replaced_by",
        "reason", "schema_version",
    }
)  # fmt: skip
_QUESTION_KEYS: Final = frozenset({"id", "text", "owner", "asker", "options", "answer", "answerer"})
_WAIT_KEYS: Final = frozenset({"kind", "reason", "owner", "resume_when", "expires", "question"})
_APPROVAL_KEYS: Final = frozenset(
    {
        "target", "actor", "assurance", "required_level", "content_hash", "gate", "reason",
        "attempts", "used", "definitions_hash",
    }
)  # fmt: skip


def _exact(value: object, keys: frozenset[str], path: str) -> Mapping[str, object]:
    mapping = as_mapping(value)
    if mapping is None:
        raise _fail(path, "an object")
    missing = sorted(keys - set(mapping))
    unknown = sorted(set(mapping) - keys)
    if missing or unknown:
        raise _fail(path, f"exactly the known fields (missing {missing}, unknown {unknown})")
    return mapping


def _text(value: object, path: str) -> str:
    text = as_text(value)
    if text is None:
        raise _fail(path, "a non-empty text")
    return text


def _optional_text(value: object, path: str) -> str | None:
    return None if value is None else _text(value, path)


def _choice(value: object, allowed: tuple[str, ...], path: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise _fail(path, f"one of {', '.join(allowed)}")
    return value


def _optional_choice(value: object, allowed: tuple[str, ...], path: str) -> str | None:
    return None if value is None else _choice(value, allowed, path)


def _read_list[T](value: object, reader: Callable[[object], T], path: str) -> list[T]:
    items = as_list(value)
    if items is None:
        raise _fail(path, "a list")
    return [reader(item) for item in items]


def _read_options(value: object, path: str) -> tuple[str, ...] | None:
    if value is None:
        return None
    items = as_list(value)
    if items is None:
        raise _fail(path, "null or a list of texts")
    return tuple(_text(item, path) for item in items)


def _read_question(value: object) -> Question:
    record = _exact(value, _QUESTION_KEYS, "after.questions[]")
    return Question(
        id=_text(record["id"], "question.id"),
        text=_text(record["text"], "question.text"),
        owner=_text(record["owner"], "question.owner"),
        asker=_text(record["asker"], "question.asker"),
        options=_read_options(record["options"], "question.options"),
        answer=_optional_text(record["answer"], "question.answer"),
        answerer=_optional_text(record["answerer"], "question.answerer"),
    )


def _read_wait(value: object) -> Wait:
    record = _exact(value, _WAIT_KEYS, "after.wait")
    return Wait(
        kind=_choice(record["kind"], WAIT_KINDS, "wait.kind"),
        reason=_text(record["reason"], "wait.reason"),
        owner=_text(record["owner"], "wait.owner"),
        resume_when=_text(record["resume_when"], "wait.resume_when"),
        expires=_optional_text(record["expires"], "wait.expires"),
        question=_optional_text(record["question"], "wait.question"),
    )


def _read_approval(value: object) -> Approval:
    record = _exact(value, _APPROVAL_KEYS, "after.approvals[]")
    attempts = None if record["attempts"] is None else as_int(record["attempts"])
    used = as_int(record["used"])
    if used is None or used < 0 or (record["attempts"] is not None and attempts is None):
        raise _fail("approval.attempts/used", "whole numbers")
    return Approval(
        target=_text(record["target"], "approval.target"),
        actor=_text(record["actor"], "approval.actor"),
        assurance=_choice(record["assurance"], ASSURANCE, "approval.assurance"),
        required_level=_choice(record["required_level"], ASSURANCE, "approval.required_level"),
        content_hash=_optional_text(record["content_hash"], "approval.content_hash"),
        gate=_optional_text(record["gate"], "approval.gate"),
        reason=_optional_text(record["reason"], "approval.reason"),
        attempts=attempts,
        used=used,
        definitions_hash=_optional_text(record["definitions_hash"], "approval.definitions_hash"),
    )


def _approval_json(a: Approval) -> dict[str, object]:
    return {
        "target": a.target,
        "actor": a.actor,
        "assurance": a.assurance,
        "required_level": a.required_level,
        "content_hash": a.content_hash,
        "gate": a.gate,
        "reason": a.reason,
        "attempts": a.attempts,
        "used": a.used,
        "definitions_hash": a.definitions_hash,
    }


def _question_json(q: Question) -> dict[str, object]:
    return {
        "id": q.id,
        "text": q.text,
        "owner": q.owner,
        "asker": q.asker,
        "options": None if q.options is None else list(q.options),
        "answer": q.answer,
        "answerer": q.answerer,
    }


def _wait_json(w: Wait) -> dict[str, object]:
    return {
        "kind": w.kind,
        "reason": w.reason,
        "owner": w.owner,
        "resume_when": w.resume_when,
        "expires": w.expires,
        "question": w.question,
    }
