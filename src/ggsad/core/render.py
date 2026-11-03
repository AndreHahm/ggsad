"""The readable message of an envelope (Implementation Contract, Section 22.3).

Every operation emits a readable message and the structured envelope; the command line prints the
message by default and the envelope as JSON with `--json`. A status report starts with the one
line for the owner.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from ggsad.core.operations import Envelope


def render_json(envelope: Envelope) -> str:
    """The envelope as JSON text."""
    return json.dumps(envelope.to_json(), indent=2, ensure_ascii=False)


def _report_lines(report: dict[str, Any]) -> list[str]:
    lines = [str(report["headline"])]
    state = str(report["state"])
    outcome = report.get("outcome")
    lines.append(f"state: {state}" + (f" ({outcome})" if outcome else ""))
    results = report.get("gate_results")
    if results:
        lines.append("gates: " + ", ".join(f"{gate}={result}" for gate, result in results.items()))
    if report.get("gates_enforced") is False:
        lines.append(
            "the gates are not enforced: the gate definitions differ from the approved ones"
        )
    lines.extend(_closed_lines(report.get("closed") or {}))
    lines.extend(_list_lines("pending", report.get("pending") or [], _pending_text))
    lines.extend(_list_lines("warnings", report.get("warnings") or [], _warning_text))
    return lines


def _closed_lines(closed: dict[str, Any]) -> list[str]:
    lines = [f"reason: {closed['reason']}"] if closed.get("reason") else []
    if closed.get("replaced_by"):
        lines.append(f"replaced by: {closed['replaced_by']}")
    followers = closed.get("followed_by")
    if followers:
        lines.append("followed by: " + ", ".join(str(name) for name in followers))
    return lines


def _pending_text(item: dict[str, Any]) -> str:
    return f"{item['actor']} must act: {item['kind']} {item['id']}: {item['detail']}"


def _warning_text(item: dict[str, Any]) -> str:
    return f"{item['code']}: {item['message']}"


def _list_lines(
    title: str, items: list[dict[str, Any]], text: Callable[[dict[str, Any]], str]
) -> list[str]:
    if not items:
        return []
    return [f"{title}:", *(f"  - {text(item)}" for item in items)]


def render_text(envelope: Envelope, actor: str | None = None) -> str:
    """The readable message: the report for `check`, otherwise the result and the issues."""
    report = envelope.data.get("report")
    lines: list[str] = []
    if isinstance(report, dict):
        lines.extend(_report_lines(cast("dict[str, Any]", report)))
        lines.append("")
    changed = "recorded" if envelope.changed else "nothing written"
    lines.append(f"{envelope.operation}: {envelope.result} ({changed})")
    if actor:
        lines.append(f"acting as: {actor}")
    lines.extend(f"  {issue.code}: {issue.message}" for issue in envelope.issues)
    if envelope.state is not None and not isinstance(report, dict):
        lines.append(f"state: {envelope.state.get('state')}")
    lines.extend(_data_lines(envelope.data))
    return "\n".join(lines)


def _data_lines(data: Mapping[str, object]) -> list[str]:
    return [f"{key}: {value}" for key, value in data.items() if key != "report"]
