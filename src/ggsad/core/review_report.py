"""The review report `review.md` (Sections 14.2, 14.5, and 23.3).

Layout: the heading `# Review`, the eight `Field: value` lines of the evidence record (and the
optional line `Reviewer switch`), the heading `## Findings`, and a table with the columns
Finding, Severity, Decision, Reason, Status. Text after the table is not read.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import takewhile
from typing import Final

HEADING: Final = "# Review"
FINDINGS_HEADING: Final = "## Findings"
FIELDS: Final = (
    "Participant", "Role", "Reviewed revision", "Action", "Timestamp", "Result", "Findings",
    "Disposition",
)  # fmt: skip
OPTIONAL_FIELDS: Final = ("Reviewer switch",)
COLUMNS: Final = ("Finding", "Severity", "Decision", "Reason", "Status")
SEVERITIES: Final = ("informational", "minor", "major", "blocking", "critical")
DECISIONS: Final = ("fix", "defer", "reject")
STATUSES: Final = ("verified", "open", "accepted", "deferred")
SETTLED: Final = ("verified", "accepted", "deferred")
SERIOUS: Final = ("blocking", "critical")
MIN_TABLE_LINES: Final = 2


@dataclass(frozen=True)
class Finding:
    """One row of the findings table."""

    id: str
    severity: str
    decision: str
    reason: str
    status: str


@dataclass(frozen=True)
class ReviewReport:
    """A review report that follows the layout."""

    record: dict[str, str]
    findings: tuple[Finding, ...]


class LayoutError(ValueError):
    """The text is not a review report."""


def _bad(where: str, message: str) -> LayoutError:
    return LayoutError(message if where == "layout" else f"{where}: {message}")


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _read_field(line: str, record: dict[str, str]) -> None:
    name, separator, value = line.partition(":")
    if not separator or name not in (*FIELDS, *OPTIONAL_FIELDS) or name in record:
        raise _bad("layout", f"unexpected line before the findings: {line!r}")
    record[name] = value.strip()


def _read_record(lines: list[str], start: int) -> tuple[dict[str, str], int]:
    record: dict[str, str] = {}
    index = start
    while index < len(lines) and lines[index].strip() != FINDINGS_HEADING:
        if lines[index].strip():
            _read_field(lines[index].strip(), record)
        index += 1
    missing = [name for name in FIELDS if not record.get(name)]
    if missing:
        raise _bad("layout", "missing fields: " + ", ".join(missing))
    return record, index


def _read_row(line: str) -> Finding:
    cells = _cells(line)
    if len(cells) != len(COLUMNS):
        raise _bad("layout", f"a finding row has {len(COLUMNS)} columns: {line!r}")
    finding = Finding(*cells)
    if not finding.id:
        raise _bad("layout", "a finding needs an identifier")
    if finding.severity not in SEVERITIES:
        raise _bad(
            "layout", f"{finding.id}: severity {finding.severity!r} is not one of {SEVERITIES}"
        )
    if finding.decision and finding.decision not in DECISIONS:
        raise _bad(
            "layout", f"{finding.id}: decision {finding.decision!r} is not one of {DECISIONS}"
        )
    if finding.status not in STATUSES:
        raise _bad("layout", f"{finding.id}: status {finding.status!r} is not one of {STATUSES}")
    return finding


def _check_table_head(rows: list[str]) -> None:
    if len(rows) < MIN_TABLE_LINES or _cells(rows[0]) != list(COLUMNS):
        raise _bad("layout", "the findings table needs the columns " + ", ".join(COLUMNS))
    if set("".join(_cells(rows[1]))) - set("-: "):
        raise _bad("layout", "the findings table needs a separator row")


def _read_table(lines: list[str], start: int) -> tuple[Finding, ...]:
    rows = [line for line in lines[start:] if line.strip()]
    _check_table_head(rows)
    body = list(takewhile(lambda line: line.strip().startswith("|"), rows[MIN_TABLE_LINES:]))
    findings = tuple(_read_row(line) for line in body)
    if len({f.id for f in findings}) != len(findings):
        raise _bad("layout", "a finding identifier is repeated")
    return findings


def parse_review(text: str) -> ReviewReport:
    """Read a review report, or raise LayoutError."""
    lines = text.splitlines()
    body = [i for i, line in enumerate(lines) if line.strip()]
    if not body or lines[body[0]].strip() != HEADING:
        raise _bad("layout", f"the report starts with the heading {HEADING!r}")
    record, index = _read_record(lines, body[0] + 1)
    if index >= len(lines):
        raise _bad("layout", f"the heading {FINDINGS_HEADING!r} is missing")
    return ReviewReport(record, _read_table(lines, index + 1))


def _reviewer_problem(report: ReviewReport) -> str | None:
    if report.record["Role"] != "Reviewer":
        return "the report does not name a Reviewer"
    if report.record["Participant"].startswith("human:"):
        return "the Reviewer is a human"
    return None


def _reviewer_issues(report: ReviewReport) -> list[tuple[str, str]]:
    problem = _reviewer_problem(report)
    if problem is None:
        return []
    code = "reviewer-not-agent" if "human" in problem else "review-layout-invalid"
    return [(code, problem)]


def approval_issues(text: str | None) -> list[tuple[str, str]]:
    """Why the review result cannot be approved (Section 23.4, target `review`)."""
    if text is None:
        return [("review-missing", "review.md does not exist")]
    try:
        report = parse_review(text)
    except LayoutError as error:
        return [("review-layout-invalid", str(error))]
    issues = _reviewer_issues(report)
    undecided = [f.id for f in report.findings if f.severity in SERIOUS and not f.decision]
    if undecided and not issues:
        issues = [
            ("review-undecided", "no decision of the decision owner: " + ", ".join(undecided))
        ]
    return issues


def completion_gaps(text: str | None) -> tuple[str, ...]:
    """What is missing for a done gate of the kind `review` (Section 23.3)."""
    issues = approval_issues(text)
    if issues:
        return tuple(message for _code, message in issues)
    report = parse_review(text or "")
    open_fixes = [f.id for f in report.findings if f.decision == "fix" and f.status not in SETTLED]
    if open_fixes:
        return ("findings marked fix are not verified or dispositioned: " + ", ".join(open_fixes),)
    return ()
