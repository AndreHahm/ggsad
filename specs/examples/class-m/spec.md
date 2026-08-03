# CHG-000 — Example: Add a --quiet Flag to ggsad validate

## Metadata

- Change ID: CHG-000
- Slug: example-quiet-validate-flag
- Class: M
- Phase: specify
- Status: draft
- Flow Profile: standard
- Compliance Profile: standard
- Requestor: human:project-owner
- Decision Owner: human:project-owner
- Created: 2026-08-03
- Last Updated: 2026-08-03
- Related Roadmap Item: None
- Parent Initiative: None

> This is the repository's required complete Class M example (R-018). It is a fictional,
> illustrative change and is not active project state — see `state.yaml`'s `flow.status`
> (`draft`) and this file's own Status field above.

## Goal

### Desired Outcome

`ggsad validate` supports a `--quiet` flag. When set, it suppresses the per-issue
listing and prints only a single final summary line, so scripts that only care about
the exit code are not forced to parse or discard per-issue text output.

### Problem Being Solved

CI scripts and pre-commit hooks that call `ggsad validate` only to gate on its exit
code currently have to redirect its full per-issue output themselves. A built-in
`--quiet` flag makes that intent explicit and avoids relying on shell redirection.

### Success Signals

- `ggsad validate --quiet` exits non-zero on any validation issue, with no per-issue lines printed.
- `ggsad validate --quiet` exits zero silently when the repository is valid.

### Non-Goals

- Changing the default (non-quiet) output format.
- Adding a `--quiet` flag to `ggsad init` or `ggsad new`.

## Context

`ggsad validate`'s text output (Slice 5, CHG-001) prints one line per `ValidationIssue`
plus a final count line. That is the right default for interactive use, but is
unnecessarily verbose for a CI gate that only checks the exit code.

## Scope

### Included

- A `--quiet` boolean option on `ggsad validate`.
- Suppression of per-issue lines when `--quiet` is set; the final summary line remains.

### Excluded

- Any change to `--format json` output (already machine-readable).
- A corresponding flag on other commands.

## Stakeholders and Participants

| Role | Participant | Responsibility |
|---|---|---|
| Requestor | human:project-owner | Defines this example change |
| Reviewer | agent:codex | Would independently review, if this were a real change |
| Approver | human:project-owner | Would provide approval, if this were a real change |
| Informed | CI script maintainers | Consumers of the new flag |

## Requirements

### R-001 — Add a `--quiet` Option to `ggsad validate`

The CLI MUST accept a `--quiet` boolean flag on `ggsad validate`. When set, per-issue
output lines MUST be suppressed; the final summary line and the exit code MUST be
unaffected.

- Priority: Must
- Source: reduce CI script boilerplate
- Related ADRs: None
- Verification Method: CLI acceptance test

## Acceptance Examples

### E-001 — Quiet Mode Suppresses Per-Issue Output on Failure

- Covers: R-001
- Type: normal

Given a repository with at least one validation issue
When the user runs `ggsad validate --quiet`
Then the command exits non-zero
And no per-issue lines are printed
And the final summary line is still printed

### E-002 — Quiet Mode Is Silent on Success

- Covers: R-001
- Type: normal

Given a repository with no validation issues
When the user runs `ggsad validate --quiet`
Then the command exits zero
And no output is printed

## Alternative Verifiable Conditions

None.

## Constraints

### Project and Constitutional Constraints

- Must not weaken `ggsad validate`'s existing exit-code contract.

### Architecture and ADR Constraints

- None beyond the existing CLI layer (architecture.md Section 5.12).

### Technology Constraints

- Typer boolean option, consistent with existing `ggsad` flags.

### Security, Privacy, and Compliance Constraints

- None; no new data is read or written.

### Compatibility and Migration Constraints

- Additive flag; default behavior is unchanged.

### Resource and Budget Constraints

- None.

## Affected Areas

- Components: CLI
- Interfaces: `ggsad validate`
- Data: None
- Configuration: None
- Documentation: CLI help text
- Operations: None
- Users: CI script authors
- External Integrations: None

## Risks

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| `--quiet` accidentally also suppresses the exit code | high | low | dedicated acceptance test asserting exit code is unaffected | Requestor |

## Dependencies and Prerequisites

| Dependency | Type | Owner | Required Condition | Status |
|---|---|---|---|---|
| `ggsad validate` (Slice 5) | technical | Requestor | Already implemented | satisfied |

## Breaking-Change Assessment

- Breaking Change: No
- Affected Consumers: None
- Migration Required: No
- Approval Required: No
- Reference: Additive CLI flag

## Flow Gates

### Additional Ready Conditions

None beyond project defaults.

### Additional Done Conditions

None beyond project defaults.

### Additional Wait Conditions

None.

### Additional Fail Conditions

None.

## Verification Plan

| Requirement / Example | Verification Method | Expected Evidence | Owner |
|---|---|---|---|
| R-001 / E-001, E-002 | CLI acceptance test | test reference and command result | Requestor |

## Pair Review

- Required: No
- Activation Basis: Not applicable — illustrative example, not an active change
- Requestor: human:project-owner
- Reviewer: Not applicable
- Review Scope: Not applicable
- Separate `review.md`: Optional
- Separate Human Approval: No

## Approval

- Specification Approval Required: No
- Approver: Not Required
- Approval Status: Not Required
- Approval Evidence: None — illustrative example only

## Open Questions

None.

## Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Architecture: `docs/architecture.md`
- ADRs: None
- Plan: `plan.md`
- Tasks: `tasks.md`
- Evidence: `evidence.md`
- State: `state.yaml`
- Companion Execution Context: None

## Change History

| Date | Actor | Status | Summary |
|---|---|---|---|
| 2026-08-03 | human:project-owner | Draft | Initial draft of the illustrative example |
