# Fix register: what changed in the specification and why

This register lists the nine changes made to the specification to fix the eleven findings of the first independent review. A change is a repair when the text had one consistent reading, and my choice when more than one reading was possible; for a choice the other readings are named, so that the owner can pick another one. A choice is a proposal: it becomes the decision of the owner only through the owner approval of the exact new text. The approval packet is printed from this register.

## The nine changes

| Change | Title | Findings | Kind | Status | Sections | Examples |
|---|---|---|---|---|---|---|
| FG-01 | A pause request on a change that has already hit a hard failure | RV-A-002, RV-X-001 | repair | drafted | 8.3 | AE-295 |
| FG-02 | Re-opening a closed change when its new work would have to wait | RV-A-001, RV-X-002 | my choice | drafted | 8.3 | AE-296 |
| FG-03 | Starting a change when a check cannot be run | RV-C-001, RV-A-003 | repair | drafted | 8.3, 8.5, 23.4 | AE-297 |
| FG-04 | Cancelling or replacing a change when a check cannot be run | RV-A-003 | my choice | drafted | 8.3, 8.4, 8.5, 23.4, 24.2 | AE-298, AE-299 |
| FG-05 | Which rule decides when a ready condition is not met | RV-D-001 | repair | drafted | 24.2 | AE-300 |
| FG-06 | Recording a question in the full profile | RV-B-001 | repair | drafted | 8.3, 24, 24.8 | AE-301 |
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

- What changed: Re-opening a closed change is now refused when its new work would have to wait (for example for an answer still owed), and the change stays closed.
- Why: The table said the re-open waits and also said it can never be blocked, so its result was undefined.
- My choice: I chose to refuse the re-open, as starting a change is refused when a wait applies, because it changes the least; the other ways are to let the re-open succeed and then wait, or to record it and answer blocked (the largest edit). This is a proposal; the owner can pick another way.
- Before: "Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied; wait when the new corrective scope's DoW determines a pause; fail when the new corrective scope's DoF determines failure."
- After: "Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied or a DoW condition of the new corrective scope is active; fail when the new corrective scope's DoF determines failure."
- Notes: Section 8.3 only: the Rejection Behavior cell of the `reopen` row of the transition table, and the rejected cell of the `reopen` row of the table of results, which now names a Definition of Wait condition of the new corrective scope. Stale statements found by the sweep: the blocked cell of the `reopen` row (`Never.`) stays true, the sentence of Section 22.2 on the actions that can answer blocked stays true, the realization row for the result blocked stays true, and the examples AE-217, AE-246 and AE-259 stay true. The example AE-296 is placed after AE-246 and cited in the last See sentence of Section 8.3.

### FG-03 — Starting a change when a check cannot be run

- What changed: Starting a change when a check cannot be run (for example because its tool is missing) is refused and nothing is written; every place that speaks of this now says so.
- Why: One place already said it, while the others left it open or said that the change would wait.
- My choice: none: the rule for deciding already says that the start is refused, and the other places are brought into line.
- Before: "and the evaluation of Section 23.6 finds no fail gate and no wait gate active."
- After: "and none of the steps 1 to 4 of Section 23.6 would decide, so that a fail gate that is active, a gate that cannot be evaluated, or a wait gate that is active prevents the start."
- Notes: Section 23.4: the Precondition cell of the `start` row (the `close` row has similar words and stays true as it is). Section 8.3: the Rejection Behavior cell of the `start` row and the rejected cell of its row of the table of results. Section 8.5: the sentence on a gate that cannot be evaluated. Stale statements found by the sweep: Section 24.2 stays true, the rejected cell of the `start` row of the table of results of Section 23.4 stays true, and the examples AE-74, AE-117 and AE-124 stay true. The example AE-297 is placed after AE-239 and cited in the last See sentence of Section 8.3.

### FG-04 — Cancelling or replacing a change when a check cannot be run

- What changed: When a check cannot be run, cancelling or replacing a change still goes ahead and the check is recorded as could not be evaluated, while pausing, failing or re-opening is refused with the code gate-not-evaluable.
- Why: The old rule said that the change waits, which these actions cannot do.
- My choice: I chose that a cancellation is never held up by a broken check, and I named the refusal code; the other ways are to refuse all five actions (simplest, but a broken check could stop a cancellation) or to let all five answer blocked and wait (the largest edit). This is a proposal; the owner can pick another way.
- Before: none (new text)
- After: "`cancel` and `supersede` take effect, because an authorized cancellation is not held up by a check that cannot run and a gate that cannot be evaluated is never a failure, and the result `not_evaluable` of the gate and its cause are recorded in the entry of the action."
- Notes: Section 24.2: one new paragraph after the paragraph on a known hard failure (rule 2 and that paragraph are not edited). Sections 8.3 and 23.4: one pointer sentence each. Section 8.4: one sentence added to the paragraph on cancel and supersede. Section 23.4: the Precondition cell of the `cancel` row. Section 8.5: the sentence that FG-03 changed now also names the actions that proceed and are rejected. The name of the refusal code is my own. Stale statements found by the sweep: the sentence of Section 8.5 on a gate that cannot be evaluated updated; rule 2 of Section 24.2 stays true (its words are unchanged and the new paragraph names the actions it does not apply to); the sentence of Section 22.2 stays true; the blocked cells of both tables of results stay true; the realization rows for the three-valued results and for the result blocked stay true; the examples AE-111 to AE-116 and AE-154 stay true. The example AE-298 is placed after AE-244 and cited in the last See sentence of Section 8.3; AE-299 is placed after AE-43 and cited in the new sentence of Section 23.4.

### FG-05 — Which rule decides when a ready condition is not met

- What changed: One paragraph now says which decision rule applies when a ready condition of the full profile is not met, so that every outcome in the transition table follows from the rules.
- Why: The rules listed fail, wait and done conditions but not ready conditions, so a reader could not tell how they rank.
- My choice: none: the transition table already states the outcomes, and the paragraph writes down how the rules rank them.
- Before: none (new text)
- After: "The Definition of Ready of the current phase, for `complete` from `draft`, and the Definition of Ready of the resume phase, for `resume` and `reopen`, rank with rule 5 for the action concerned"
- Notes: Section 24.2 only: one new paragraph between the five rules and the paragraph on a known hard failure; the five rules and that paragraph are not edited. Stale statements found by the sweep: the rules 1 to 5 stay true, the transition table of Section 8.3 stays true, and the example AE-240 stays true. The example AE-300 is placed after AE-74 and cited at the end of the new paragraph.

### FG-06 — Recording a question in the full profile

- What changed: The text now says that recording a question is the action ask in both profiles and that it is not a row of the transition table.
- Why: One part said that ask exists for the full profile, while the transition table and the section on questions did not mention it.
- My choice: none: the lists of contract operations and of entry actions already name ask for both profiles.
- Before: "In `full`, a question is recorded in the state file, or in the inline record where no state file is persisted (Section 4.3), and the answer is recorded as a human decision (Section 22.1)."
- After: "In `full`, the operation that records a question is the action `ask`, which is not a transition: its entry has the action name `ask` (Section 25.1), it leaves the phase and the status unchanged, and it is legal for a change that is not in the `closed` phase."
- Notes: Section 24.8: the sentence for the full profile (the sentence for core is not edited). Section 8.3: one sentence after the pointer sentences below the table of results; no row ask is added. Section 24: the full cell of the realization row Open questions as state, which now names the action ask. Stale statements found by the sweep: the example AE-287 stays true, Section 22.1 stays true, Section 25.1 stays true because it already names ask in the closed set of entry actions, and the ask row of Section 23.4 stays true. The example AE-301 is placed after AE-182 and cited in the sentence of Section 24.8.

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
