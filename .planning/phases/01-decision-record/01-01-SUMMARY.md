---
phase: 01-decision-record
plan: 01
subsystem: governance-docs
tags: [decision-record, owner-decisions, bash-check]
status: complete

requires: []
provides:
  - "Decision record docs/decisions/2026-10-23-executable-core-decisions.md with O-1 to O-11, all Proposed wording"
  - "Read-only check script 01-check-decision-record.sh (E1 E2 H1 F1 F2 D1 S1 X1 X2 G1)"
affects: [01-02 owner confirmation, 01-03 delivery, milestone v1.1 Phases 2 to 8]

actuals:
  tokens: 7100
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns: ["field-bullet decision entries", "mechanical decisive-phrase check per Chosen sentence"]

key-files:
  created:
    - docs/decisions/2026-10-23-executable-core-decisions.md
    - .planning/phases/01-decision-record/01-check-decision-record.sh
  modified: []

key-decisions:
  - "No decision was made in this plan; O-1 to O-11 are recorded as the owner's decisions of 2026-10-23, in Proposed wording until the owner confirms in plan 01-02."

patterns-established:
  - "Rationale only where the proposal records the owner's reason (O-6); ten entries read 'rationale not recorded'."

requirements-completed: []  # DEC-01 stays open: entries are Proposed wording; the orchestrator ticks it at phase close.

duration: "about 50 minutes including the tracer gate"
completed: 2026-10-24
---

# Phase 1 Plan 01: Decision Record Summary

One self-contained record of the owner's eleven Executable Core decisions (O-4 with its explicit departure from the proposal's YAML recommendation), checked by a small read-only bash script that fails on a changed id, field, status, hash or scope.

## Accomplishments

- Frame (status block with `Owner confirmation: pending`, rules for using the record, Requestor notes) and entries O-1 to O-11 in ascending order, each with the seven fields; O-4 also carries `Departs from the proposal`.
- Every Chosen is one sentence containing the decisive phrases of the decided text; eleven phrase checks pass.
- Rationale appears only for O-6 (the decided text's own reason: `reopen` is phase-based); the other ten entries read `rationale not recorded`.
- Check script: encoding (E1, E2), ids and order (H1), fields (F1, F2), O-4 departure (D1), status by stage (S1), hash tokens (X1), self-containment (X2), scope against a base (G1).

## Task Commits

1. Task 1 (tracer): `20123ea` docs(01-01): record frame, O-4 entry and first checks (owner approved the tracer gate)
2. Task 2: `aae52c8` docs(01-01): add entries O-1 to O-3 and O-5 to O-11
3. Task 3: `99f5d40` docs(01-01): add self-containment and scope checks

## Verification

- `bash 01-check-decision-record.sh --scope-base origin/main` and the same with `--ref HEAD`: RESULT PASS, ten PASS lines.
- Negative runs failed as intended: stage confirmed (FAIL S1), a removed O-5 heading (FAIL H1), a stray `1a2b3c4` (FAIL X1), a second prototype mention, path, address, link, prototype name, finding id and bare requirement id (FAIL X2; the qualified `v1.1 SPEC-14` passes), an extra top-level file (FAIL G1), an edited requirement line citing O-5 (FAIL G1; file restored with `git checkout -- .planning/REQUIREMENTS.md`).
- `git status --short` was identical before and after every script run.
- `git diff --name-only origin/main...HEAD` lists only paths under docs/decisions/ and .planning/.

## Deviations from Plan

None - plan executed as written. The `.gsd/` sentinel was excluded by the owner in `.git/info/exclude`, so G1 needed no special case and the script was not changed for it.

## Known Stubs

None.

## Unverified

- Fidelity of each restatement to the proposal was checked by me against the proposal text at commit 058d6c0 and the earlier drafts, plus the mechanical phrase checks; the owner has not yet reviewed the committed wording (plan 01-02).

## Self-Check: PASSED

- Record and script exist; commits 20123ea, aae52c8 and 99f5d40 exist on gsd/phase-1-decision-record.
