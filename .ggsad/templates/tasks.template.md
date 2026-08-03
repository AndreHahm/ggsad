# Implementation Checklist: <Change ID> — <Change Title>

## Metadata

- Change ID: <CHG-NNN>
- Status: Draft | Active | Done | Superseded
- Phase: build
- Owner: <participant-id>
- Last Updated: <YYYY-MM-DD>
- Specification: `spec.md`
- Plan: `plan.md`

## Usage Rules

- This checklist is an execution aid, not the source of truth for requirements or architecture.
- Every task MUST map to an approved requirement, plan step, risk control, or evidence need.
- Tasks MUST NOT silently expand scope.
- Completion boxes MUST reflect actual completion.
- Blocked tasks MUST identify a wait or failure condition.
- Remove tasks that no longer apply only with a recorded reason.

## Task Status Legend

- `[ ]` Not started
- `[-]` In progress
- `[x]` Complete
- `[!]` Blocked
- `[~]` Not applicable or superseded with rationale

## 1. Preparation

- [ ] **T-001 — Confirm active change state**
  - Maps To: <state or gate>
  - Files: `state.yaml`
  - Evidence: <reference>
  - Notes:

- [ ] **T-002 — Review governing artifacts**
  - Maps To: Constitution, ADRs, Project Brief, Architecture, Specification
  - Files: <paths>
  - Evidence: <reference>
  - Notes:

## 2. Implementation

- [ ] **T-010 — <Actionable Task Title>**
  - Maps To: R-001, E-001, Plan Step 1
  - Files: <paths>
  - Preconditions: <conditions>
  - Expected Result: <observable result>
  - Verification: <test or check>
  - Evidence: <reference>
  - Owner: <participant-id>
  - Notes:

- [ ] **T-011 — <Actionable Task Title>**
  - Maps To: <requirement or plan step>
  - Files: <paths>
  - Preconditions:
  - Expected Result:
  - Verification:
  - Evidence:
  - Owner:
  - Notes:

## 3. Tests and Verification

- [ ] **T-020 — Add or update unit tests**
  - Maps To: <requirements and examples>
  - Files: <test paths>
  - Verification: <command>
  - Evidence:

- [ ] **T-021 — Add or update integration or acceptance tests**
  - Maps To: <requirements and examples>
  - Files:
  - Verification:
  - Evidence:

- [ ] **T-022 — Run required quality gates**
  - Commands:
    ```bash
    <format-command>
    <lint-command>
    <type-check-command>
    <test-command>
    <build-command>
    ```
  - Evidence:

- [ ] **T-023 — Verify negative, failure, boundary, and recovery behavior**
  - Maps To:
  - Evidence:

## 4. Documentation and Artifacts

- [ ] **T-030 — Update implementation documentation**
  - Files:
  - Maps To:

- [ ] **T-031 — Update architecture or ADR references if approved**
  - Files:
  - Approval Reference:

- [ ] **T-032 — Update evidence**
  - File: `evidence.md`
  - Maps To:

## 5. Pair Review

- [ ] **T-040 — Prepare stable review target**
  - Requestor:
  - Reviewer:
  - Commit or Worktree:
  - Scope:

- [ ] **T-041 — Conduct Pair Review**
  - Review ID:
  - Evidence:

- [ ] **T-042 — Resolve and re-verify blocking findings**
  - Finding IDs:
  - Evidence:

## 6. Closure Preparation

- [ ] **T-050 — Perform specification-to-implementation consistency check**
  - Evidence:

- [ ] **T-051 — Confirm no unapproved scope or deviations**
  - Evidence:

- [ ] **T-052 — Confirm required documentation is current**
  - Evidence:

- [ ] **T-053 — Evaluate DoF, DoW, DoD, and next DoR**
  - Evidence:

## Blocked Tasks

| Task | Status | Reason | Waiting For | Safe State | Resume Condition |
|---|---|---|---|---|---|
| <task-id> | waiting | <reason> | <owner-or-source> | <state> | <condition> |

## Superseded or Not-Applicable Tasks

| Task | Status | Rationale | Approved By / Reference |
|---|---|---|---|
| <task-id> | superseded | not_applicable | <rationale> | <reference> |

## Completion Summary

- Completed Tasks:
- Remaining Tasks:
- Blocked Tasks:
- Deviations:
- Next Permitted Action:
