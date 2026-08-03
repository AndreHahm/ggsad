"""Unresolved template placeholder detection (R-009, plan.md Sec 4.4).

Detects only the approved angle-bracket forms used by the packaged
templates (`<placeholder>`, `<placeholder-or-value>`, `<YYYY-MM-DD>`, and
similar tokens), and ignores angle-bracket syntax inside fenced code blocks
and inline code spans, where it usually represents example CLI syntax or
pattern illustration (e.g. `` `specs/<change-id>-<slug>/` ``) rather than
unresolved document content. Confirmed against the packaged templates: every
genuine placeholder appears bare in prose (e.g. `- Project: <project-name>`),
never backtick-wrapped, so stripping inline code spans doesn't risk missing
a real one.
"""

from __future__ import annotations

import re
from pathlib import Path

from ggsad.models.validation import IssueCategory, ValidationIssue

_PLACEHOLDER_PATTERN = re.compile(r"<[A-Za-z][A-Za-z0-9_-]*>")
_FENCED_CODE_BLOCK_PATTERN = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE_SPAN_PATTERN = re.compile(r"`[^`\n]+`")


def find_unresolved_placeholders(text: str) -> list[str]:
    """Return unresolved `<placeholder>`-style tokens found outside code fences/spans."""
    prose_only = _FENCED_CODE_BLOCK_PATTERN.sub("", text)
    prose_only = _INLINE_CODE_SPAN_PATTERN.sub("", prose_only)
    return _PLACEHOLDER_PATTERN.findall(prose_only)


def validate_no_unresolved_placeholders(path: Path) -> list[ValidationIssue]:
    """Reject `path` if it still contains unresolved template placeholders."""
    text = path.read_text(encoding="utf-8")
    placeholders = find_unresolved_placeholders(text)
    if not placeholders:
        return []

    unique = sorted(set(placeholders))
    return [
        ValidationIssue(
            category=IssueCategory.UNRESOLVED_PLACEHOLDER,
            file=str(path),
            reason=f"Unresolved template placeholder(s) found: {', '.join(unique)}.",
            remediation="Replace each placeholder with real content.",
        )
    ]
