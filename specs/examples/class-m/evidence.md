# Verification Evidence: CHG-000 — Example: Add a --quiet Flag to ggsad validate

## Metadata

- Change ID: CHG-000
- Phase: verify
- Status: Draft
- Evidence Owner: human:project-owner
- Requestor: human:project-owner
- Reviewer: Not applicable
- Created: 2026-08-03
- Last Updated: 2026-08-03
- Specification: `spec.md`
- Plan: `plan.md`
- State: `state.yaml`
- Review Record: Not applicable

## 1. Evidence Principles

- Evidence demonstrates completion; it does not replace the specification.
- Results MUST identify whether a check was executed, passed, failed, skipped, unavailable, or not
  applicable.
- Durable reports SHOULD be referenced rather than copied in full.
- Evidence MUST NOT contain secrets or unnecessary sensitive data.
- A status MUST NOT be based solely on assertion.

**This file documents an illustrative example (R-018), not an implemented change. Every
check below is honestly reported as Not Run, per the constitution's rule that unexecuted
checks must never be reported as passed.**

## 2. Verification Environment

Not applicable — no implementation was performed for this illustrative example.

## 3. Requirement Coverage

| Requirement | Acceptance Example / Condition | Verification Method | Evidence | Result |
|---|---|---|---|---|
| R-001 | E-001, E-002 | CLI acceptance test | Not applicable | Not Run |

## 4. Acceptance Example Coverage

| Example | Covers | Evidence | Result | Notes |
|---|---|---|---|---|
| E-001 | R-001 | Not applicable | Not Run | Illustrative example only |
| E-002 | R-001 | Not applicable | Not Run | Illustrative example only |

## 5. Quality Gates

| Gate | Command or Method | Result | Evidence | Notes |
|---|---|---|---|---|
| Environment / Dependency Sync | `uv sync` | Not Run | Not applicable | Illustrative example |
| Formatting | `uv run ruff format --check .` | Not Run | Not applicable | Illustrative example |
| Linting | `uv run ruff check .` | Not Run | Not applicable | Illustrative example |
| Type Checking | `uv run ty check` | Not Run | Not applicable | Illustrative example |
| Unit Tests | `uv run pytest` | Not Run | Not applicable | Illustrative example |
| Build / Packaging | `uv build` | Not Run | Not applicable | Illustrative example |

## 6. Detailed Test Results

None: no code was written for this illustrative example.

## 7. Negative, Failure, Boundary, and Recovery Evidence

| Scenario | Requirement / Example | Evidence | Result |
|---|---|---|---|
| None | Not applicable | Not applicable | Not Run |

## 8. Traceability Summary

```text
Goal
|-- Requirement R-001
    |-- Acceptance Example E-001, E-002
        |-- (not executed -- illustrative example)
```

## 9. Pair Review

- Required: No
- Review ID: Not applicable
- Requestor: human:project-owner
- Reviewer: Not applicable
- Reviewer Type: Not applicable
- Review Scope: Not applicable
- Review Target: Not applicable
- Result: Not Required
- Review Evidence: Not applicable

### Findings

None.

### Blocking-Finding Summary

- Open Blocking Findings: 0
- Resolution Evidence: Not applicable
- Re-verification Required: No
- Re-verification Result: Not applicable

## 10. Approval Evidence

| Approval | Required | Approver | Status | Evidence |
|---|---|---|---|---|
| Specification | No | Not Required | Not Required | Not applicable |

## 11. Deviations

None.

## 12. Known Limitations

- This is a fixture example (R-018), not an implemented change: no code, no tests, no gate results.

## 13. Wait and Failure Evidence

### Wait Events

None.

### Failure Events

None.

## 14. Final Gate Evaluation

### Definition of Fail

- Triggered: No
- Criteria: Not applicable
- Evidence: Not applicable
- Result: Not applicable

### Definition of Wait

- Triggered: No
- Criteria: Not applicable
- Evidence: Not applicable
- Result: Not applicable

### Current Definition of Done

- Satisfied: No
- Criteria: Not applicable — never implemented
- Evidence: Not applicable
- Result: Not satisfied (by design; this is a fixture)

### Next Definition of Ready

- Satisfied: Not Applicable
- Criteria: Not applicable
- Evidence: Not applicable
- Result: Not applicable

## 15. Final Result

- Final Status: Pending
- Recommended Transition: None — this example is never transitioned
- Transition Evidence: Not applicable
- Remaining Actions: None — this is a static fixture, not an active change
- Evidence Owner Statement: This file documents an illustrative Class M example required by
  R-018/E-013. No implementation, tests, or gate checks were executed; every result above is
  honestly reported as Not Run or Not Applicable rather than asserted as passing.

## 16. Evidence History

| Date | Actor | Revision | Summary |
|---|---|---|---|
| 2026-08-03 | human:project-owner | 1 | Initial evidence record for the illustrative example |
