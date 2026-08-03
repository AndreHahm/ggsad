# Verification Evidence: <Change ID> — <Change Title>

## Metadata

- Change ID: <CHG-NNN>
- Phase: verify
- Status: Draft | Active | Complete | Superseded
- Evidence Owner: <participant-id>
- Requestor: <participant-id>
- Reviewer: <distinct-participant-id-or-pending>
- Created: <YYYY-MM-DD>
- Last Updated: <YYYY-MM-DD>
- Specification: `spec.md`
- Plan: `plan.md`
- State: `state.yaml`
- Review Record: <path-or-inline>

## 1. Evidence Principles

- Evidence demonstrates completion; it does not replace the specification.
- Results MUST identify whether a check was executed, passed, failed, skipped, unavailable, or not
  applicable.
- Durable reports SHOULD be referenced rather than copied in full.
- Evidence MUST NOT contain secrets or unnecessary sensitive data.
- A status MUST NOT be based solely on assertion.

## 2. Verification Environment

| Item | Value |
|---|---|
| Repository Revision | <commit-or-worktree-reference> |
| Branch / Worktree | <reference> |
| Operating System | <value> |
| Runtime | <value> |
| Toolchain | <value> |
| Configuration / Profile | <value> |
| Date and Time | <ISO-8601> |

## 3. Requirement Coverage

| Requirement | Acceptance Example / Condition | Verification Method | Evidence | Result |
|---|---|---|---|---|
| R-001 | E-001 | <test or review> | `<reference>` | Pass | Fail | Partial | Not Run |

## 4. Acceptance Example Coverage

| Example | Covers | Evidence | Result | Notes |
|---|---|---|---|---|
| E-001 | R-001 | `<reference>` | Pass | Fail | <notes> |

## 5. Quality Gates

| Gate | Command or Method | Result | Evidence | Notes |
|---|---|---|---|---|
| Environment / Dependency Sync | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Formatting | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Linting | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Type Checking | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Unit Tests | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Integration Tests | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Acceptance Tests | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Build / Packaging | `<command>` | Pass | Fail | Not Run | `<reference>` | |
| Security | `<command-or-review>` | Pass | Fail | Not Run | `<reference>` | |
| Compatibility | `<command-or-review>` | Pass | Fail | Not Run | `<reference>` | |
| Documentation | `<check>` | Pass | Fail | Not Run | `<reference>` | |

## 6. Detailed Test Results

### 6.1 <Test or Check Name>

- Command:
  ```bash
  <command>
  ```
- Result: Pass | Fail | Not Run | Not Applicable
- Exit Code: <code-or-none>
- Report: `<path-or-URL-reference>`
- Summary: <concise result>
- Limitations: <limitations-or-none>

## 7. Negative, Failure, Boundary, and Recovery Evidence

| Scenario | Requirement / Example | Evidence | Result |
|---|---|---|---|
| <scenario> | <reference> | <evidence> | Pass | Fail | Not Run |

## 8. Traceability Summary

```text
Goal
└── Requirement R-001
    └── Acceptance Example E-001
        └── Test or Review <reference>
            └── Evidence <reference>
```

<Repeat or provide a table when useful.>

## 9. Pair Review

- Required: Yes | No | Conditional
- Review ID: <PR-NNN-or-none>
- Requestor: <participant-id>
- Reviewer: <distinct-participant-id>
- Reviewer Type: Human | Agent | External Review Service
- Review Scope: <artifacts and criteria>
- Review Target: <commit, worktree, or artifact version>
- Result: Pending | Pass | Pass with Findings | Fail | Not Required
- Review Evidence: <reference>

### Findings

| ID | Category | Severity | Artifact / Reference | Summary | Status | Disposition |
|---|---|---|---|---|---|---|
| PRF-001 | <category> | informational | minor | major | blocking | critical | <reference> | <summary> | open | resolved | verified | <disposition> |

### Blocking-Finding Summary

- Open Blocking Findings: <number>
- Resolution Evidence: <reference-or-none>
- Re-verification Required: Yes | No
- Re-verification Result: <result-or-none>

## 10. Approval Evidence

| Approval | Required | Approver | Status | Evidence |
|---|---|---|---|---|
| Specification | Yes | No | <participant> | Approved | Rejected | Pending | Not Required | <reference> |
| Architecture / ADR | Yes | No | <participant> | <status> | <reference> |
| Breaking Change | Yes | No | <participant> | <status> | <reference> |
| Release | Yes | No | <participant> | <status> | <reference> |

## 11. Deviations

| ID | Specification or Plan Reference | Deviation | Impact | Status | Approval / Decision |
|---|---|---|---|---|---|
| DEV-001 | <reference> | <deviation> | <impact> | open | accepted | rejected | resolved | <reference> |

Use `None` when no deviations exist.

## 12. Known Limitations

- <limitation or None>

## 13. Wait and Failure Evidence

### Wait Events

| Timestamp | Category | Reason | Waiting For | Resume Condition | Resolution |
|---|---|---|---|---|---|
| <timestamp> | WAIT_<CATEGORY> | <reason> | <owner> | <condition> | <resolution> |

### Failure Events

| Timestamp | Category | Trigger | Response | Final Status | Evidence |
|---|---|---|---|---|---|
| <timestamp> | FAILED_<CATEGORY> | <trigger> | <response> | <status> | <reference> |

Use `None` when no wait or failure events occurred.

## 14. Final Gate Evaluation

Evaluate in this order.

### Definition of Fail

- Triggered: Yes | No
- Criteria:
- Evidence:
- Result:

### Definition of Wait

- Triggered: Yes | No
- Criteria:
- Evidence:
- Result:

### Current Definition of Done

- Satisfied: Yes | No
- Criteria:
- Evidence:
- Result:

### Next Definition of Ready

- Satisfied: Yes | No | Not Applicable
- Criteria:
- Evidence:
- Result:

## 15. Final Result

- Final Status: Pending | Done | Waiting | Failed | Cancelled | Superseded
- Recommended Transition: <action-or-none>
- Transition Evidence: <reference-or-none>
- Remaining Actions: <actions-or-none>
- Evidence Owner Statement: <concise factual statement>

## 16. Evidence History

| Date | Actor | Revision | Summary |
|---|---|---|---|
| <YYYY-MM-DD> | <actor> | <revision> | Initial evidence record |
