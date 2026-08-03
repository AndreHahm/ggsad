# Implementation Plan: CHG-000 — Example: Add a --quiet Flag to ggsad validate

## Metadata

- Change ID: CHG-000
- Status: Draft
- Phase: plan
- Requestor: human:project-owner
- Planner: human:project-owner
- Approver: Not Required
- Created: 2026-08-03
- Last Updated: 2026-08-03
- Specification: `spec.md`
- State: `state.yaml`

## 1. Purpose

This plan describes how R-001 (a `--quiet` flag on `ggsad validate`) would be implemented.
It is an illustrative example (R-018) and is subordinate to the approved specification,
accepted ADRs, architecture, project brief, and constitution, like any real plan would be.

## 2. Planning Preconditions

- [x] Specification is approved where required (not required for this illustrative example).
- [x] Relevant project documents and ADRs were reviewed.
- [x] Blocking questions are resolved or explicitly accepted (none exist).
- [x] Required dependencies and permissions are identified.
- [x] Ready-to-Plan criteria are satisfied.

## 3. Technical Approach

Add a `quiet: bool = typer.Option(False, "--quiet", ...)` parameter to the existing
`validate_command` in `src/ggsad/cli.py`. When `quiet` is `True`, skip the per-issue
`typer.echo(str(issue))` loop but still compute and print the final summary line, and
still `raise typer.Exit(code=1)` when issues exist. No change to `validate_repository()`
itself — this is purely an output-formatting change in the CLI layer.

## 4. Alternatives Considered

### Option 1 — CLI-layer flag (selected)

- Summary: Add `--quiet` to the existing `validate_command`, gating only the per-issue echo loop.
- Advantages: Minimal, isolated change; no impact on `validate_repository()`'s return contract.
- Disadvantages: None identified.
- Reason Not Selected: Not applicable — selected.

### Option 2 — New `--format quiet` value

- Summary: Treat "quiet" as a third `--format` value alongside `text` and `json`.
- Advantages: Reuses the existing `--format` option instead of adding a new flag.
- Disadvantages: Conflates "output format" with "verbosity"; `--format json --quiet` would
  be a more natural combination than a single `--format quiet-json`.
- Reason Not Selected: Verbosity and format are orthogonal; keeping them as separate flags
  composes better.

## 5. Affected Components and Artifacts

| Component or Artifact | Planned Change | Requirement | Owner |
|---|---|---|---|
| `src/ggsad/cli.py` | Add `--quiet` option to `validate_command` | R-001 | Requestor |

## 6. Architecture Impact

- Impact: None
- ADR Required: No
- Architecture Document Update Required: No
- Dependency Direction Changes: None
- Boundary Changes: None
- Related ADRs: None

No architectural impact: this is an additive CLI-layer flag with no change to the engine,
validators, or models.

## 7. Data and State Impact

- Data Model Changes: None
- State Model Changes: None
- Configuration Changes: None
- Schema Changes: None
- Persistence Changes: None
- Retention or Migration Impact: None

## 8. Interface and Compatibility Impact

- CLI: New `--quiet` option on `ggsad validate`
- API: Not applicable
- Events: Not applicable
- File Formats: Unchanged
- Public Interfaces: `ggsad validate` gains one additive option
- Backward Compatibility: Fully backward compatible; default behavior unchanged
- Deprecation: None
- Versioning: Pre-alpha CLI, no separate versioning required

## 9. Security, Privacy, and Compliance Impact

- Threats: None new
- Trust Boundaries: Unchanged
- Permissions: Unchanged
- Secrets: None
- Data Classification: Not applicable
- Privacy: Not applicable
- Compliance: Not applicable
- Required Review or Approval: None beyond standard CLI review

## 10. Operational Impact

- Deployment: None
- Packaging: None
- Monitoring: None
- Logging: Fewer log lines in quiet mode, by design
- Metrics: None
- Alerting: None
- Support: Document `--quiet` in `ggsad validate --help`
- Backup and Recovery: Not applicable
- Rollback: Revert the commit

## 11. Test and Verification Strategy

| Requirement / Example | Test Level | Test or Check | Evidence |
|---|---|---|---|
| R-001 / E-001, E-002 | acceptance | `CliRunner` invocation with `--quiet` | test report |

### Required Test Types

- Unit: Not required beyond the acceptance tests below
- Integration: Not required
- Acceptance: E-001, E-002
- Regression: Existing non-quiet `validate` tests must keep passing
- Property-Based: Not applicable
- Security: Not applicable
- Performance: Not applicable
- Compatibility: Not applicable
- Manual Review: Not required

## 12. Evidence Strategy

If this were a real change, results would be recorded in `evidence.md`, referencing the
`pytest` run rather than duplicating its output.

Expected evidence:

- `pytest` output for the two new acceptance tests
- `ggsad validate --help` output showing the documented flag

## 13. Pair Review Plan

- Required: No
- Requestor: human:project-owner
- Reviewer: Not applicable
- Review Scope: Not applicable
- Review Criteria: Not applicable
- Stable Review Target: Not applicable
- Blocking-Finding Rule: Not applicable
- Re-verification Required: No

## 14. Migration and Rollback

### Migration

Not required.

### Rollback

Revert the commit that added the `--quiet` option.

### Irreversible Actions

None.

## 15. Dependencies and Permissions

| Dependency or Permission | Owner | Required Before | Failure Behavior |
|---|---|---|---|
| `ggsad validate` (Slice 5) | Requestor | Build | wait |

## 16. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation | Detection |
|---|---|---|---|---|
| `--quiet` accidentally suppresses the exit code | high | low | dedicated acceptance test | acceptance test |

## 17. Implementation Sequence

1. Add the `--quiet` option and gate the per-issue echo loop on it.
2. Add E-001 and E-002 acceptance tests.
3. Update `ggsad validate --help` text and note the flag in evidence.

Each step produces a reviewable and recoverable state.

## 18. Task Decomposition

- Task Artifact Required: Yes
- Rationale: `tasks.md` is a required Class M artifact for CHG-001-generated changes
  (Q-005), so it is included here too, kept small since this is a single-file change.

## 19. Wait and Fail Handling

### Expected Wait Conditions

| Condition | Owner / Source | Safe State | Resume Condition | Next Action |
|---|---|---|---|---|
| None expected | Not applicable | Not applicable | Not applicable | Not applicable |

### Expected Fail Conditions

| Trigger | Required Response | Preservation Action | Final Status |
|---|---|---|---|
| None expected | Not applicable | Not applicable | Not applicable |

## 20. Delivery and Commit Strategy

- Branch or Worktree: Not applicable — illustrative example only
- Commit Boundaries: Not applicable
- Generated Files: Not applicable
- Review Target: Not applicable
- Merge or Release Policy: Not applicable; this example is never merged as a real change

## 21. Plan Validation

Before approval, confirm:

- [x] Every planned change maps to a requirement or approved technical necessity.
- [x] No accepted ADR is contradicted.
- [x] No excluded scope was introduced.
- [x] Verification and evidence work are included.
- [x] Migration, rollback, wait, and fail behavior are clear.
- [x] Required approvals and Pair Review are identified (none required for this example).
- [x] The implementation sequence is safe and reviewable.

## 22. Decisions and References

| Decision | Type | Reference |
|---|---|---|
| CLI-layer flag over `--format quiet` | scoped decision | Section 4, Option 1 |

## 23. Approval

- Approval Required: No
- Approver: Not Required
- Status: Not Required
- Evidence: None — illustrative example only

## 24. Plan History

| Date | Actor | Status | Summary |
|---|---|---|---|
| 2026-08-03 | human:project-owner | Draft | Initial illustrative plan |
