"""The text of the files that `init` creates (Sections 4.2, 5.1, and 14.5).

Every text is plain Markdown or YAML for a person to edit. None of it is read back as a rule: the
brief states its profile on one line, and the review template follows the layout of `review.md`.
"""

from __future__ import annotations

from typing import Final

from ggsad.core.settings import SCHEMA_VERSION

BRIEF_TEMPLATE: Final = """\
# Project brief

Compliance profile: {profile}

## Problem

What problem does the project solve, and for whom?

## Outcomes

What is true when the project works?

## Scope and non-goals

What is in, and what is explicitly out?

## Constraints

Technical, legal, and organizational limits.

## Method

Method profile: core
Operating mode: {team_mode}
Integrated methods and tools: none
"""
CONSTITUTION_TEMPLATE: Final = """\
# Constitution

The rules that no change may break. A change never overrides this document silently.

## Quality

## Security

## Architecture

## Approvals

## Prohibited actions

## Minimum evidence
"""
ARCHITECTURE_TEMPLATE: Final = """\
# Architecture

The current structure: components, boundaries, data flows, deployment, known constraints, and the
decisions (ADRs) that explain them. Put durable decisions in `docs/adr/`, not here.
"""
ROADMAP_TEMPLATE: Final = """\
# Roadmap

The intended direction. This is not a backlog.

## Now

## Next

## Later

## Open
"""
REVIEW_TEMPLATE: Final = """\
# Review

Participant: agent:<name>
Role: Reviewer
Reviewed revision: <commit>
Action: review round
Timestamp: <UTC time>
Result: findings reported
Findings: 0
Disposition: none

## Findings

| Finding | Severity | Decision | Reason | Status |
|---|---|---|---|---|

Severities: informational, minor, major, blocking, critical.
"""
SPEC_TEMPLATE: Final = """\
# Specification: <change-id>

Problem: <what is wrong or missing>

Conflicts with higher documents: none
"""
EXAMPLE_PROBLEM: Final = "Users cannot reset their password without help"
EXAMPLE_DONE_WHEN: Final = ("A user can reset their own password",)


def config_text(
    project_id: str, profile: str, team_mode: str, owner: str, requestors: tuple[str, ...]
) -> str:
    """The text of `.ggsad/config.yaml`."""
    listed = "".join(f"    - {{identity: {_quote(name)}}}\n" for name in requestors)
    return (
        f'schema_version: "{SCHEMA_VERSION}"\n'
        "project:\n"
        f"  id: {_quote(project_id)}\n"
        f"  compliance_profile: {_quote(profile)}\n"
        f"  team_mode: {_quote(team_mode)}\n"
        "roles:\n"
        f"  owner: {_quote(owner)}\n"
        "  # Add the humans who may approve, with their accounts, to turn the list on:\n"
        "  # approved_humans:\n"
        f"  #   - {{identity: {_quote(owner)}, account: your-account}}\n"
        "  requestors:\n"
        f"{listed}"
        "defaults:\n"
        "  retry_limit: 3\n"
        "  fail_severity: hard\n"
        "minimum_levels: {}\n"
    )


def _quote(text: str) -> str:
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
