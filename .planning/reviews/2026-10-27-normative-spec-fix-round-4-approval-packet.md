# Owner approval packet, fix round 4: proposed normative method specification

- Owner approval: pending

## What you are asked

On 2026-10-27 the owner approved the text of the specification. The independent reviewer then looked at it a third time; the owner asked for the three findings that the reviewer rated BLOCKING, its strongest rating, to be fixed. For two of them the owner chose how; for the third the finding itself names the fix. The text has been changed in three places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.

## The three changes

| # | What changed | Why | Whose reading |
|---|---|---|---|
| 1 | After the gate definitions of a change were edited, only `cancel` still goes ahead. The `supersede` action is now refused with the issue code `gates-changed` until a human approves the edited gate definitions again, and the tables and examples say so. | Edited gate definitions are meant to block every operation except cancellation, but the text also let `supersede` go ahead. | your decision: Cancel only |
| 2 | The section on the Definition of Fail now says plainly that its duty to end the flow does not cover a retry limit. Reaching one pauses the flow for a human, and the earlier text of this method ended the flow there. No rule about retry limits changed. | The earlier text made exceeding a retry limit a case where the flow must end, and this text pauses it instead without saying so. | your decision: Soft, said openly |
| 3 | A new example shows that a `wait`, a `fail` and a `reopen` on a full change are each rejected, with nothing written and no wait created, when a gate that applies cannot be evaluated. The issue code is `gate-not-evaluable`. | The rule that rejects these three actions had no example, although the rules for the core actions have one. | no decision asked: the finding names the fix |

## Before and after

### Change 1 of 3: How the gate comparison treats the supersede action

- Findings: RT-A-001
- Options offered: Cancel only | Supersede too, said openly
- Your decision: Cancel only; reason: none given
- Before: "Three operations are exempt from the comparison and MUST NOT be stopped by it: `cancel`, `supersede`, and the approval of the gate definitions that replaces the approved hash."
- After: "Two operations are exempt from the comparison and MUST NOT be stopped by it: `cancel` and the approval of the gate definitions that replaces the approved hash."

### Change 2 of 3: What happens when a retry limit is reached

- Findings: RT-B-001
- Options offered: Soft, said openly | Hard or soft | Hard only
- Your decision: Soft, said openly; reason: none given
- Before: none (new text)
- After: "The obligation to terminate of this section does not cover a retry limit: reaching one pauses the flow for a human disposition and does not end it by itself, as the earlier text of this method did."

### Change 3 of 3: An example for a wait, a fail or a reopen that cannot be evaluated

- Findings: RT-D-001
- Your decision: none asked; the finding leaves no design choice
- Before: none (new text)
- After: "Then each result is `rejected` with `changed` false and the issue code `gate-not-evaluable`, nothing is written to the history, no wait state is created, and each change keeps its phase and its status"

## The text under approval

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `fca228479a34e228785f4c0b100da3c6745ada0a` |
| Reviewed SHA-256 | `5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1` |
| Line count | `4812` |
| Diffstat | `1 file changed, 3439 insertions(+), 49 deletions(-)` |
| Commits touching the file | `52` |
| Previously approved blob and SHA-256 | `a81d9c89651f326605db08708ea4c079809a2825` and `d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc` |
| Register file | `.planning/reviews/2026-10-27-normative-spec-fix-round-4-register.md` |
| Register blob | `38514e9478af40ae6d20d3f31ae93d87d34e14b0` |

## The exact change

The change from the text approved in round 3 has 11 hunks, adds 28 lines and removes 10 lines.

```
@@ -892,7 +892,7 @@ Then the status `done` is legal as the local completion signal of the phase, and
 | `resume` | A non-closed phase with status `waiting` | The recorded resume condition is satisfied and the recorded or explicitly required resume phase is non-closed. | DoF → DoW → DoR for the recorded non-closed resume phase or explicitly required earlier non-closed phase; current-phase DoD and next-phase DoR are not applicable. | Recorded non-closed resume phase, or an explicitly required earlier non-closed phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When the resume-phase DoR is not satisfied or a DoW condition is still active, record the evaluation in the history, remain `waiting`, and answer `blocked` (Section 22.2). Fail when DoF determines failure (Section 24.7). |
 | `fail` | Any non-closed phase/status | A soft failure awaits disposition: the status is `waiting` with a wait state of the category `WAIT_DECISION` for a DoF condition of the severity `soft` that is active (Section 24.7). | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
 | `cancel` | Any non-closed phase/status | An authorized cancellation decision exists. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `cancelled`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
-| `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
+| `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied or the gate definitions differ from the approved ones (issue code `gates-changed`, Section 24.1). |
 | `reopen` (`full` only) | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF for the new corrective scope → DoW for the new corrective scope → DoR for the recorded resume phase or explicitly stated earlier phase; the prior terminal outcome's DoF and DoW, closed-phase DoD, and next-phase DoR are not applicable. | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied or a DoW condition of the new corrective scope is active; fail when the new corrective scope's DoF determines failure. |
 
 **Rejected and Blocked Results per Action (`full`)**
@@ -905,7 +905,7 @@ Then the status `done` is legal as the local completion signal of the phase, and
 | `resume` | The status is not `waiting`, the resume condition is not satisfied, or the resume phase is closed. | The resume-phase DoR is not satisfied, or a DoW condition is still active, so that the change remains `waiting`. |
 | `fail` | The change is closed, or no soft failure awaits disposition, so that an active DoF condition of the severity `hard` alone does not allow the action. | Never. |
 | `cancel` | The change is closed, or no authorized cancellation decision exists. | Never. |
-| `supersede` | The change is closed, or no later change is authorized to replace this change. | Never. |
+| `supersede` | The change is closed, no later change is authorized to replace this change, or the gate definitions differ from the approved ones (issue code `gates-changed`, Section 24.1). | Never. |
 | `reopen` | The change is not in the `closed` phase, the corrective follow-up work is not authorized with a reason and a new goal-bound scope, the resume-phase DoR is not satisfied, or a Definition of Wait condition of the new corrective scope is active. | Never. |
 
 An action whose evaluation closes the change as failed answers `success` (Section 24.7). An action answers `blocked` only where this table lists a case, and a `complete` that preserves the current phase with the status `done` because the next-phase DoR is not satisfied answers `success`. See AE-121, AE-122, AE-123, AE-124.
@@ -946,7 +946,7 @@ Given a `full` change whose phase has the status `ready` and a Definition of Wai
 When the `start` action is requested  
 Then the result is `rejected` with `changed` false and the issue code `start-blocked`, and the status remains `ready`
 
-See AE-239, AE-240, AE-241, AE-242, AE-243, AE-244, AE-245, AE-246, AE-295, AE-296, AE-297, AE-298, AE-308.
+See AE-239, AE-240, AE-241, AE-242, AE-243, AE-244, AE-245, AE-246, AE-295, AE-296, AE-297, AE-298, AE-308, AE-310.
 
 **AE-239 — Start a ready phase**
 
@@ -1028,6 +1028,14 @@ Given a `full` change in the build phase with the status `active`, an authorized
 When the `cancel` action is requested  
 Then the change is in the `closed` phase with the status `cancelled`, and the result `not_evaluable` of the condition is recorded with its cause
 
+**AE-310 — A full change rejects wait, fail, and reopen when a gate cannot be evaluated**
+
+- Covers: Section 8.3 (full: `wait`, `fail`, and `reopen`)
+
+Given three `full` changes with no active Definition of Fail condition of the severity `hard` and, in each, a Definition of Fail condition that applies to the action and cannot be evaluated because its program is missing: a change in the plan phase with the status `active` and an active Definition of Wait condition, a change in the verify phase with the status `waiting` because of an active Definition of Fail condition of the severity `soft`, and a change in the `closed` phase with the status `done` whose resume phase recorded at closure is the build phase, with a reason and a new goal-bound scope authorized, a satisfied resume-phase Definition of Ready, and no active Definition of Wait condition of the new corrective scope  
+When the `wait` action is requested for the first change, the `fail` action for the second, and the `reopen` action for the third  
+Then each result is `rejected` with `changed` false and the issue code `gate-not-evaluable`, nothing is written to the history, no wait state is created, and each change keeps its phase and its status
+
 **AE-245 — Supersede needs a later change**
 
 - Covers: Section 8.3 (`supersede`)
@@ -1062,7 +1070,7 @@ these actions. DoF retains first priority; when DoF determines that the change h
 resulting terminal status is `failed` rather than `cancelled` or `superseded`. A gate that cannot be evaluated
 determines no failure, so that the action takes effect (Section 24.2).
 
-The comparison of the gate definitions with the approved ones (Section 24.1) does not stop `cancel` or `supersede`.
+The comparison of the gate definitions with the approved ones (Section 24.1) does not stop `cancel`. It does stop `supersede`: while the gate definitions differ from the approved ones, `supersede` is rejected with the issue code `gates-changed`, and it can go ahead only after a human has approved the gate definitions again.
 
 A fail condition of the severity `hard` closes the change as failed without human action, and a fail condition of the severity `soft` waits for a human, who either closes the change with `fail` or records an override (Section 24.7).
 
@@ -1484,6 +1492,8 @@ The obligation to terminate applies to a fail condition of the severity `hard`.
 
 A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition, and the human closes the change as failed or records an override (Section 24.7).
 
+The obligation to terminate of this section does not cover a retry limit: reaching one pauses the flow for a human disposition and does not end it by itself, as the earlier text of this method did.
+
 ### 12.1 Typical Fail Categories
 
 - critical technical error,
@@ -2550,7 +2560,7 @@ A `core` change changes state only through the actions of the table below. An ac
 | `close` | `active` | The evaluation of Section 23.6 finds no fail gate and no wait gate active, and every done gate is satisfied. | The state `closed` with the outcome `done`. When the evaluation finds otherwise, the change does not close: it remains `active` when a wait gate is active or a done gate is not satisfied, becomes `waiting` when Section 23.6 requires a wait, and becomes `closed` with the outcome `failed` when a hard fail condition is active. See AE-37, AE-38. |
 | `fail` | `waiting`, with a wait record of kind `fail-gate` | A soft fail condition awaits disposition (Section 24.7), and a reason text is given. | The state `closed` with the outcome `failed` and the reason recorded. See AE-39, AE-40, AE-41. |
 | `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). A gate that cannot be evaluated determines no failure and does not prevent it (Section 24.2). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active. See AE-42, AE-43. |
-| `supersede` | Any state except `closed` | The preconditions of `cancel` hold, and `replaced_by` names a different change that exists. | As `cancel`, with `replaced_by` recorded in the closed change. See AE-44, AE-45. |
+| `supersede` | Any state except `closed` | The preconditions of `cancel` hold, except that differing gate definitions prevent the action (Section 24.1), and `replaced_by` names a different change that exists. | As `cancel`, with `replaced_by` recorded in the closed change. See AE-44, AE-45, AE-309. |
 | `adopt` | Any state | The history of the change has no anchor (Section 24.4). | The state and the outcome do not change, and the anchor is created from the history as it is. See AE-46, AE-47. |
 
 The actions `approve`, `fail`, `cancel`, `supersede`, and `adopt` MUST be performed by a human participant. An `answer` to a question whose owner is a human MUST also be given by a human (Section 24.3). See AE-24.
@@ -2575,7 +2585,7 @@ A `follows` field is a reference and not a state transition: it never changes th
 | `close` | The state is not `active`. | The evaluation of Section 23.6 finds a wait gate active, a done gate not satisfied, a soft failure, or a gate that cannot be evaluated, so that the change does not close. |
 | `fail` | The state is not `waiting` with a wait record of kind `fail-gate`, or no reason is given. | Never. |
 | `cancel` | The state is `closed`. | Never. |
-| `supersede` | The state is `closed`, or `replaced_by` is missing, names the change itself, or names a change that does not exist. | Never. |
+| `supersede` | The state is `closed`, or `replaced_by` is missing, names the change itself, or names a change that does not exist, or the gate definitions differ from the approved ones (issue code `gates-changed`, Section 24.1). | Never. |
 | `adopt` | The history already has an anchor. | Never. |
 
 A `close` or a `resume` whose evaluation finds a fail gate of the severity `hard` active answers `success` with the state `closed` and the outcome `failed` (Section 24.7). An action answers `blocked` only where this table lists a case. See AE-117, AE-118, AE-119, AE-120.
@@ -3211,7 +3221,7 @@ The identity of the fixed definitions is the content hash (Section 25.2) of the
 
 Every state-changing operation MUST first compute the hash of the current gate definitions and compare it with the approved hash. When the two differ, the operation MUST write nothing, and its result MUST be `rejected` with `changed` false (Section 22.2) and the stable issue code `gates-changed`, whose message states that the gate definitions differ from the approved ones and that a human has to approve them again. See AE-75, AE-76, AE-86.
 
-Three operations are exempt from the comparison and MUST NOT be stopped by it: `cancel`, `supersede`, and the approval of the gate definitions that replaces the approved hash. The exemption of `cancel` and `supersede` ensures that a change whose definitions were altered can always be ended. The approval that replaces the approved hash is the re-approval; without the exemption, no change could leave this state. See AE-77, AE-78, AE-81.
+Two operations are exempt from the comparison and MUST NOT be stopped by it: `cancel` and the approval of the gate definitions that replaces the approved hash. The exemption of `cancel` ensures that a change whose definitions were altered can always be ended. The action `supersede` is not exempt: while the hashes differ, it is rejected with `changed` false and the issue code `gates-changed`, and it can go ahead only after a human has approved the gate definitions again. The approval that replaces the approved hash is the re-approval; without its exemption, no change could leave this state. See AE-77, AE-78, AE-309, AE-81.
 
 The re-approval MUST be performed by a human at the assurance level that Section 24.3 requires for the approval of gates. It is recorded in the history as an amendment, not as an approval, and the record names the approved hash that it replaces and the new approved hash. After the re-approval the new hash is the approved hash, and an override of a soft failure that is bound to the earlier hash lapses (Section 24.7). See AE-81, AE-85.
 
@@ -3245,14 +3255,22 @@ Given a `core` change whose gate definitions differ from the approved ones
 When a human performs the `cancel` action  
 Then the state is `closed` and the outcome is `cancelled`
 
-**AE-78 — Supersede is not stopped by differing gate definitions**
+**AE-78 — Supersede goes ahead once the gate definitions are approved again**
 
 - Covers: Section 24.1
 
-Given a `core` change A whose gate definitions differ from the approved ones, and an existing change B  
+Given a `core` change A whose gate definitions differed from the approved ones and were approved again by a human, and an existing change B  
 When a human performs the `supersede` action on change A with `replaced_by` naming change B  
 Then change A is `closed` with the outcome `cancelled` and `replaced_by` naming change B
 
+**AE-309 — Supersede is rejected while the gate definitions differ**
+
+- Covers: Section 24.1
+
+Given a `core` change A whose gate definitions differ from the approved ones, and an existing change B  
+When a human performs the `supersede` action on change A with `replaced_by` naming change B  
+Then the result is `rejected` with `changed` false and the issue code `gates-changed`, change A is not closed, and nothing is written to the history
+
 **AE-79 — A formatting-only edit does not differ**
 
 - Covers: Section 24.1
@@ -3351,7 +3369,7 @@ In `full`, the Definitions of Ready (Section 8.5) take part in the evaluation, a
 
 A known hard failure therefore outranks a gate that cannot be evaluated. This order refines Section 8.5 and Section 23.6. The `start` action requires that none of the rules 1 to 4 would decide: when one would, `start` is rejected and no wait is created, and a hard failure included, because `start` never closes a change (Section 24.7). When the action is `resume`, the wait record created by rule 2 replaces the earlier record, whose resume condition was met. An action that only reports on a change reports the result and creates no wait. See AE-69, AE-71, AE-72, AE-74.
 
-Rule 2 does not make the other actions that evaluate gates and never answer `blocked` wait, because a wait is a recorded change that they cannot answer (Section 22.2). In `full`, these actions are `wait`, `fail`, `cancel`, `supersede`, and `reopen`; in `core`, they are `cancel` and `supersede`, which look for an active hard failure. When no hard failure is active and a gate that applies to one of them cannot be evaluated, `cancel` and `supersede` take effect, because an authorized cancellation is not held up by a check that cannot run and a gate that cannot be evaluated is never a failure, and the result `not_evaluable` of the gate and its cause are recorded in the entry of the action. The actions `wait`, `fail`, and `reopen` are rejected with `changed` false, nothing is written, no wait is created, and the stable issue code is `gate-not-evaluable`. See AE-298, AE-299.
+Rule 2 does not make the other actions that evaluate gates and never answer `blocked` wait, because a wait is a recorded change that they cannot answer (Section 22.2). In `full`, these actions are `wait`, `fail`, `cancel`, `supersede`, and `reopen`; in `core`, they are `cancel` and `supersede`, which look for an active hard failure. When no hard failure is active and a gate that applies to one of them cannot be evaluated, `cancel` and `supersede` take effect, because an authorized cancellation is not held up by a check that cannot run and a gate that cannot be evaluated is never a failure, and the result `not_evaluable` of the gate and its cause are recorded in the entry of the action. The actions `wait`, `fail`, and `reopen` are rejected with `changed` false, nothing is written, no wait is created, and the stable issue code is `gate-not-evaluable`. See AE-298, AE-299, AE-310.
 
 The gates are evaluated by group. The order of the groups is the order of Section 23.6 in `core`, that is the fail gates, the wait gates, and the done gates, and the order of Section 8.5 in `full`, that is the Definition of Fail, the Definition of Wait, the Definition of Ready of the current phase, the Definition of Done, and the Definition of Ready of the next phase. A group is evaluated whole: every gate of the group that applies to the action is evaluated, even when an earlier gate of the same group already decides. After a group, the evaluation stops if the results of the groups evaluated so far decide the action under the rules 1 to 5, so that a gate of a later group is not evaluated: its command is not run, and no result is recorded for it. The rules rank the results of the gates that were evaluated, so that a gate which is not evaluated cannot outrank a gate which is. In `core`, a wait gate that is active therefore decides before a done gate that cannot be evaluated, the change does not become `waiting` for that done gate, and the `close` action answers `blocked`. A wait gate that cannot be evaluated is `not_evaluable`, and it creates a wait record of kind `external` before any done gate is evaluated. See AE-280.
 
```

## Questions

### Q01 — Approval

- Question: Do you approve the new text exactly as it now stands (fingerprint fca228479a34, 4812 lines), or do you want changes?
- Options:
  - Approve exact text: The text is approved as it stands and goes to the limited independent review that the packet describes.
  - Request changes: Nothing is approved; you say what to change.
- Answer: (unanswered)

### Q02 — Changes

- Question: What would you like changed? Say it in your own words.
- Answer: (unanswered)

### Q03 — Name

- Question: Under which name should this approval be recorded?
- Answer: (unanswered)

### Q04 — Date

- Question: Which date should be recorded? Use the form YYYY-MM-DD.
- Answer: (unanswered)

## What follows

If you approve, the text goes to an independent review by a reviewer that is not the Requestor. Before anything is sent, you decide which parts of the text that review reads, with the figures of what changed where, and you consent to the exact run. Any later edit of the specification voids the approval.

If you request changes, nothing is approved, the text is edited for them, the packet is printed again and you are asked again.

The tick of the requirement for owner approval from the first round is not changed by any plan and rests, for this text, on the record that follows this packet.

This packet is evidence only. It does not change the reviewed file.
