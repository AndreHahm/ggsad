# Fix register: what changed in the specification and why

This register lists the nine changes made to the specification to fix the eleven findings of the first independent review. A change is a repair when the text had one consistent reading, and my choice when more than one reading was possible; for a choice the other readings are named, so that the owner can pick another one. A choice is a proposal: it becomes the decision of the owner only through the owner approval of the exact new text. The approval packet is printed from this register.

## The nine changes

| Change | Title | Findings | Kind | Status | Sections | Examples |
|---|---|---|---|---|---|---|
| FG-01 | A pause request on a change that has already hit a hard failure | RV-A-002, RV-X-001 | repair | drafted | 8.3 | AE-295 |
| FG-02 | Re-opening a closed change when its new work would have to wait | RV-A-001, RV-X-002 | my choice | pending | - | - |
| FG-03 | Starting a change when a check cannot be run | RV-C-001, RV-A-003 | repair | pending | - | - |
| FG-04 | Cancelling or replacing a change when a check cannot be run | RV-A-003 | my choice | pending | - | - |
| FG-05 | Which rule decides when a ready condition is not met | RV-D-001 | repair | pending | - | - |
| FG-06 | Recording a question in the full profile | RV-B-001 | repair | pending | - | - |
| FG-07 | What happens when a retry limit is reached | RV-B-005 | my choice | pending | - | - |
| FG-08 | Deciding whether a file is text or binary before hashing it | RV-E-001 | my choice | pending | - | - |
| FG-09 | The guard check for continuous integration | RV-X-003 | my choice | pending | - | - |

## Change details

### FG-01 — A pause request on a change that has already hit a hard failure

- What changed: If a change is asked to pause while a hard failure is active, it now ends as failed and the answer is success, as the failure rule already says; before, the table also said that the pause request is refused.
- Why: Two rules gave different answers for the same request.
- My choice: none: the failure rule and the `resume` row already say what happens, so the text has one consistent reading.
- Before: "Reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure."
- After: "Reject without any partial mutation of persisted state when the precondition is not satisfied. When DoF finds a fail condition of the severity `hard` active, close the change as failed in the same state mutation and answer `success` (Section 24.7)."
- Notes: Section 8.3 only: the Rejection Behavior cell of the `wait` row of the transition table. Stale statements found by the sweep: the `wait` row of the table of results stays true (the action never answers blocked), and the `resume` row stays true (it already followed Section 24.7). The example AE-295 is placed after AE-241 and cited in the last See sentence of Section 8.3.

### FG-02 — Re-opening a closed change when its new work would have to wait

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

### FG-03 — Starting a change when a check cannot be run

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

### FG-04 — Cancelling or replacing a change when a check cannot be run

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

### FG-05 — Which rule decides when a ready condition is not met

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

### FG-06 — Recording a question in the full profile

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

### FG-07 — What happens when a retry limit is reached

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

### FG-08 — Deciding whether a file is text or binary before hashing it

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

### FG-09 — The guard check for continuous integration

- What changed: pending
- Why: pending
- My choice: pending
- Before: pending
- After: pending
- Notes: pending

## Normative lines removed or reworded

None.

## Findings whose quoted sentence an edit touched

None.

## Findings not touched

- RV-A-004 (MINOR): open information; no edit
- RV-B-002 (MINOR): open information; no edit
- RV-B-003 (MINOR): open information; no edit
- RV-B-004 (MINOR): open information; no edit
- RV-C-002 (MINOR): open information; no edit
- RV-C-003 (INFO): open information; no edit
- RV-D-002 (MINOR): open information; no edit
- RV-D-003 (INFO): open information; no edit
- RV-E-002 (MINOR): open information; no edit
- RV-E-003 (MINOR): open information; no edit
- RV-X-004 (MINOR): open information; no edit
- RV-X-005 (MINOR): open information; no edit
- RV-X-006 (INFO): open information; no edit
- RV-X-007 (INFO): open information; no edit

## Header

The header of the specification (the Version line and the Revision line) is unchanged by this round.
