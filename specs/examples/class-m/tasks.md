# Implementation Checklist: CHG-000 — Example: Add a --quiet Flag to ggsad validate

## Metadata

- Change ID: CHG-000
- Status: Draft
- Phase: build
- Owner: human:project-owner
- Last Updated: 2026-08-03
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

- [~] **T-001 — Confirm active change state**
  - Maps To: `state.yaml` remains `specify/draft`
  - Files: `state.yaml`
  - Evidence: This is an illustrative example (R-018); it is never actually built.
  - Notes: Not applicable — see `spec.md`'s disclaimer banner.

## 2. Implementation

- [~] **T-010 — Add the `--quiet` option to `validate_command`**
  - Maps To: R-001, E-001, E-002, Plan Step 1
  - Files: `src/ggsad/cli.py`
  - Preconditions: None
  - Expected Result: `ggsad validate --quiet` suppresses per-issue lines, keeps the exit code.
  - Verification: Not applicable — illustrative example, never executed.
  - Evidence: Not applicable — illustrative example, never executed.
  - Owner: human:project-owner
  - Notes: Demonstrates the artifact relationship required by R-018; not real work.

## 3. Tests and Verification

- [~] **T-020 — Add acceptance tests for `--quiet`**
  - Maps To: E-001, E-002
  - Files: Not applicable — illustrative example
  - Verification: Not applicable
  - Evidence: Not applicable

## 4. Documentation and Artifacts

- [~] **T-030 — Update `ggsad validate --help` text**
  - Files: `src/ggsad/cli.py`
  - Maps To: R-001

## 5. Pair Review

- [~] **T-040 — Pair Review**
  - Requestor: human:project-owner
  - Reviewer: Not applicable — Pair Review is not required for this illustrative example
  - Scope: Not applicable

## 6. Closure Preparation

- [~] **T-050 — Evaluate DoF, DoW, DoD, and next DoR**
  - Evidence: Not applicable — this example is never closed as a real change

## Blocked Tasks

None.

## Superseded or Not-Applicable Tasks

| Task | Status | Rationale | Approved By / Reference |
|---|---|---|---|
| T-001, T-010, T-020, T-030, T-040, T-050 | not_applicable | Illustrative example (R-018); never executed as real work | human:project-owner |

## Completion Summary

- Completed Tasks: 0
- Remaining Tasks: 0 (all marked not-applicable; see above)
- Blocked Tasks: 0
- Deviations: None
- Next Permitted Action: Not applicable — this is a static example, not an active change
