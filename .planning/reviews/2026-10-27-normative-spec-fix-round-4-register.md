# Fix register, round 4: what changed in the specification and why

This register lists the three changes made to the specification to fix the three BLOCKING findings of the third independent review that the owner dispositioned fix. For two of them the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For the third the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.

## The three changes

| Change | Title | Findings | Kind | Status | Sections | Examples |
|---|---|---|---|---|---|---|
| FG-13 | How the gate comparison treats the supersede action | RT-A-001 | owner decision | drafted | 8.3, 8.4, 23.4, 24.1 | AE-309 |
| FG-14 | What happens when a retry limit is reached | RT-B-001 | owner decision | drafted | 12 | - |
| FG-15 | An example for a wait, a fail or a reopen that cannot be evaluated | RT-D-001 | repair | drafted | 8.3, 24.2 | AE-310 |

## Change details

### FG-13 — How the gate comparison treats the supersede action

- What changed: After the gate definitions of a change were edited, only `cancel` still goes ahead. The `supersede` action is now refused with the issue code `gates-changed` until a human approves the edited gate definitions again, and the tables and examples say so.
- Why: Edited gate definitions are meant to block every operation except cancellation, but the text also let `supersede` go ahead.
- Options: Cancel only | Supersede too, said openly
- Owner decision: Cancel only
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: "Three operations are exempt from the comparison and MUST NOT be stopped by it: `cancel`, `supersede`, and the approval of the gate definitions that replaces the approved hash."
- After: "Two operations are exempt from the comparison and MUST NOT be stopped by it: `cancel` and the approval of the gate definitions that replaces the approved hash."
- Notes: Section 24.1: the paragraph on the exempt operations (two operations are exempt, a sentence says that `supersede` is not exempt and is rejected with `gates-changed` until a human approves the gate definitions again, and the See sentence cites AE-309). Section 8.4: the sentence on the comparison of the gate definitions. Section 8.3: the Rejection Behavior cell of the `supersede` row of the transition table and the rejected cell of the `supersede` row of the table of results. Section 23.4: the Precondition cell of the `supersede` row (the preconditions of `cancel` hold, except that differing gate definitions prevent the action), the rejected cell of the `supersede` row of the table of results, and the See sentence of the `supersede` row. The `cancel` rows are not edited. The example AE-78 is corrected, because it showed `supersede` going ahead while the definitions differ: it now shows `supersede` going ahead once a human has approved the gate definitions again. The example AE-309 is placed after AE-78 and cited in Section 24.1 and in the `supersede` row of Section 23.4. No requirement is edited. Stale statements found by the sweep:
  - Section 24.1, the sentence that all state-changing operations compare the gate hash first: stays true; it is the rule that now also covers `supersede`.
  - Section 24.1, the paragraph on the re-approval and the paragraph on read-only operations: stay true.
  - Section 8.3, the `wait` row of the transition table and the example on a wait request, and the cell of the table of results for `reopen`: stay true; they do not speak of the comparison of the gate definitions.
  - Section 8.4, the paragraph that says an active DoW condition does not prevent `cancel` and `supersede`, and the sentence on a gate that cannot be evaluated: stay true.
  - Section 23.4, the `cancel` row and the example AE-77: stay true.
  - Section 24.2 (the paragraph on the actions that never answer `blocked`) and Section 24.7 (the sentences that an active hard failure turns `cancel` and `supersede` into a close as failed): stay true; they speak of the case in which the gate definitions equal the approved ones.
  - Section 22.4, the lists of human actions in Section 24.3 and in the quick reference, and the examples AE-44 and AE-45: stay true.

### FG-14 — What happens when a retry limit is reached

- What changed: The section on the Definition of Fail now says plainly that its duty to end the flow does not cover a retry limit. Reaching one pauses the flow for a human, and the earlier text of this method ended the flow there. No rule about retry limits changed.
- Why: The earlier text made exceeding a retry limit a case where the flow must end, and this text pauses it instead without saying so.
- Options: Soft, said openly | Hard or soft | Hard only
- Owner decision: Soft, said openly
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: none (new text)
- After: "The obligation to terminate of this section does not cover a retry limit: reaching one pauses the flow for a human disposition and does not end it by itself, as the earlier text of this method did."
- Notes: Section 12 only: one paragraph is added after the paragraph that says a retry limit is a soft fail condition. The sentences of Sections 12 and 12.1 that say a retry limit is a soft fail condition are not edited, and no example is added; the existing example AE-101 already shows the chosen behaviour (a retry limit pauses the change and does not fail it). Point for the owner to confirm in the approval: the specification has no name for the text that it replaced, so the added sentence says `the earlier text of this method`, which follows the wording of the option. Stale statements found by the sweep:
  - Section 12.1, the sentence that a retry limit is a soft fail condition: stays true.
  - Section 23.3, the member `retry_limit` and the soft fail gate in the example: stay true.
  - Section 24.2, the paragraph that defines a retry limit, and Section 24.7, the paragraph on a retry limit that is reached and the sentence that a retry limit has the severity `soft`: stay true.
  - the examples AE-101 and AE-108: stay true.
  - Section 20, the criteria for a completed change: stays true; it does not speak of retry limits.

### FG-15 — An example for a wait, a fail or a reopen that cannot be evaluated

- What changed: A new example shows that a `wait`, a `fail` and a `reopen` on a full change are each rejected, with nothing written and no wait created, when a gate that applies cannot be evaluated. The issue code is `gate-not-evaluable`.
- Why: The rule that rejects these three actions had no example, although the rules for the core actions have one.
- Options: none: no design choice was open, because the finding names the fix itself.
- Owner decision: none: no design choice was open, because the finding names the fix itself.
- Owner reason: none: no design choice was open, because the finding names the fix itself.
- Channel: none: no design choice was open, because the finding names the fix itself.
- Before: none (new text)
- After: "Then each result is `rejected` with `changed` false and the issue code `gate-not-evaluable`, nothing is written to the history, no wait state is created, and each change keeps its phase and its status"
- Notes: No design choice was open: the finding names the fix itself, and the behaviour is fixed by the rule that it quotes. The example AE-310 is placed after AE-298 in Section 8.3 and cited in the list of examples at the end of the tables of Section 8.3 and in the See sentence of the paragraph on the other actions that evaluate gates in Section 24.2. Each of the three Givens leaves the gate that cannot be evaluated as the only reason for the rejection: the precondition of the action is met and no hard failure is active, as in the neighbouring examples for `start` and `cancel`. Stale statements found by the sweep:
  - Section 8.3, the sentence that points to Section 24.2 for what `wait`, `fail`, `cancel`, `supersede`, and `reopen` answer when a gate cannot be evaluated: stays true.
  - Section 24.2, the sentence that rejects `wait`, `fail`, and `reopen` with the issue code `gate-not-evaluable`: stays true; the example shows it.
  - the examples AE-297 to AE-299: stay true.

## Normative lines removed or reworded

- Three operations are exempt from the comparison and MUST NOT :: the owner chose that only `cancel` still goes ahead; the paragraph now names two exempt operations, and the line keeps its MUST NOT for them

## Findings whose quoted sentence an edit touched

None.

## Findings not touched

- RT-A-002 (MAJOR): open information; no edit
- RT-A-003 (MINOR): open information; no edit
- RT-A-004 (INFO): open information; no edit
- RT-B-002 (MINOR): open information; no edit
- RT-B-003 (MINOR): open information; no edit
- RT-B-004 (MINOR): open information; no edit
- RT-C-001 (MAJOR): open information; no edit
- RT-C-002 (MAJOR): open information; no edit
- RT-C-003 (MINOR): open information; no edit
- RT-D-002 (MINOR): open information; no edit
- RT-D-003 (INFO): open information; no edit
- RT-E-001 (MINOR): open information; no edit
- RT-E-002 (MINOR): open information; no edit
- RT-E-003 (INFO): open information; no edit
- RT-X-001 (MAJOR): open information; no edit
- RT-X-002 (MAJOR): open information; no edit
- RT-X-003 (MAJOR): open information; no edit
- RT-X-004 (MAJOR): open information; no edit
- RT-X-005 (MINOR): open information; no edit
- RT-X-006 (MINOR): open information; no edit

## Header

The header of the specification (the Version line and the Revision line) is unchanged by this round.
