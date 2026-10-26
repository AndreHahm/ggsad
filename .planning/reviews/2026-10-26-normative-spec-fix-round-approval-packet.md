# Owner approval packet, fix round: proposed normative method specification

- Owner approval: pending

## What you are asked

On 2026-10-25 the owner approved the text of the specification. The independent reviewer then reported its findings, and the owner asked for eleven of them to be fixed. The text has been changed in nine places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.

## The nine changes

| # | What changed | Why | Whose reading |
|---|---|---|---|
| 1 | If a change is asked to pause while a hard failure is active, it now ends as failed and the answer is success, as the failure rule already says; before, the table also said that the pause request is refused. | Two rules gave different answers for the same request. | repair: the text had one consistent reading |
| 2 | Re-opening a closed change is now refused when its new work would have to wait (for example for an answer still owed), and the change stays closed. | The table said the re-open waits and also said it can never be blocked, so its result was undefined. | my choice: you can change it |
| 3 | Starting a change when a check cannot be run (for example because its tool is missing) is refused and nothing is written; every place that speaks of this now says so. | One place already said it, while the others left it open or said that the change would wait. | repair: the text had one consistent reading |
| 4 | When a check cannot be run, cancelling or replacing a change still goes ahead and the check is recorded as could not be evaluated, while pausing, failing or re-opening is refused with the code gate-not-evaluable. | The old rule said that the change waits, which these actions cannot do. | my choice: you can change it |
| 5 | One paragraph now says which decision rule applies when a ready condition of the full profile is not met, so that every outcome in the transition table follows from the rules. | The rules listed fail, wait and done conditions but not ready conditions, so a reader could not tell how they rank. | repair: the text had one consistent reading |
| 6 | The text now says that recording a question is the action ask in both profiles and that it is not a row of the transition table. | One part said that ask exists for the full profile, while the transition table and the section on questions did not mention it. | repair: the text had one consistent reading |
| 7 | The definition of failure now says openly that reaching a retry limit pauses the change for a human, who ends it as failed or records a bounded exception. | The original rule said that exceeding a retry limit ends the flow, and the specification had softened this without saying so. | my choice: you can change it |
| 8 | A file is text exactly when its bytes are valid UTF-8 and contain no zero byte, and this is now a MUST instead of a recommendation. | With only a recommendation, two tools could compute different hashes for the same file. | my choice: you can change it |
| 9 | A new short section defines guard, a read-only check that a CI pipeline can run: it checks the history, the approved gates, the approvals, the scope and hard failures, never runs a command of the project, and proves the record, not the outcome. | The decision on verify-only CI had no text in the specification, and guard was named but never defined. | my choice: you can change it |

## Before and after

### Change 1 of 9: A pause request on a change that has already hit a hard failure

- Findings: RV-A-002, RV-X-001
- My choice: none: the failure rule and the `resume` row already say what happens, so the text has one consistent reading.
- Before: "Reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure."
- After: "Reject without any partial mutation of persisted state when the precondition is not satisfied. When DoF finds a fail condition of the severity `hard` active, close the change as failed in the same state mutation and answer `success` (Section 24.7)."

### Change 2 of 9: Re-opening a closed change when its new work would have to wait

- Findings: RV-A-001, RV-X-002
- My choice: I chose to refuse the re-open, as starting a change is refused when a wait applies, because it changes the least; the other ways are to let the re-open succeed and then wait, or to record it and answer blocked (the largest edit). This is a proposal; the owner can pick another way.
- Before: "Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied; wait when the new corrective scope's DoW determines a pause; fail when the new corrective scope's DoF determines failure."
- After: "Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied or a DoW condition of the new corrective scope is active; fail when the new corrective scope's DoF determines failure."

### Change 3 of 9: Starting a change when a check cannot be run

- Findings: RV-C-001, RV-A-003
- My choice: none: the rule for deciding already says that the start is refused, and the other places are brought into line.
- Before: "and the evaluation of Section 23.6 finds no fail gate and no wait gate active."
- After: "and none of the steps 1 to 4 of Section 23.6 would decide, so that a fail gate that is active, a gate that cannot be evaluated, or a wait gate that is active prevents the start."

### Change 4 of 9: Cancelling or replacing a change when a check cannot be run

- Findings: RV-A-003
- My choice: I chose that a cancellation is never held up by a broken check, and I named the refusal code; the other ways are to refuse all five actions (simplest, but a broken check could stop a cancellation) or to let all five answer blocked and wait (the largest edit). This is a proposal; the owner can pick another way.
- Before: none (new text)
- After: "`cancel` and `supersede` take effect, because an authorized cancellation is not held up by a check that cannot run and a gate that cannot be evaluated is never a failure, and the result `not_evaluable` of the gate and its cause are recorded in the entry of the action."

### Change 5 of 9: Which rule decides when a ready condition is not met

- Findings: RV-D-001
- My choice: none: the transition table already states the outcomes, and the paragraph writes down how the rules rank them.
- Before: none (new text)
- After: "The Definition of Ready of the current phase, for `complete` from `draft`, and the Definition of Ready of the resume phase, for `resume` and `reopen`, rank with rule 5 for the action concerned"

### Change 6 of 9: Recording a question in the full profile

- Findings: RV-B-001
- My choice: none: the lists of contract operations and of entry actions already name ask for both profiles.
- Before: "In `full`, a question is recorded in the state file, or in the inline record where no state file is persisted (Section 4.3), and the answer is recorded as a human decision (Section 22.1)."
- After: "In `full`, the operation that records a question is the action `ask`, which is not a transition: its entry has the action name `ask` (Section 25.1), it leaves the phase and the status unchanged, and it is legal for a change that is not in the `closed` phase."

### Change 7 of 9: What happens when a retry limit is reached

- Findings: RV-B-005
- My choice: I kept the softer rule that the first approval accepted and only stated it openly; the other ways are to let each project choose hard or soft, or to go back to always ending as failed (both change examples). This is a proposal; the owner can pick another way.
- Before: none (new text)
- After: "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition, and the human closes the change as failed or records an override (Section 24.7)."

### Change 8 of 9: Deciding whether a file is text or binary before hashing it

- Findings: RV-E-001
- My choice: I made the recommended rule binding; the other way is to let each tool decide and to record text or binary with every stored hash (a much larger edit). This is a proposal; the owner can pick the other way.
- Before: "an implementation SHOULD classify a file as text only when its bytes are valid UTF-8 and hold no zero byte"
- After: "A file is text exactly when its bytes are valid UTF-8 and hold no zero byte, and every other file is binary. An implementation MUST classify a file in this way."

### Change 9 of 9: The guard check for continuous integration

- Findings: RV-X-003
- My choice: I wrote the smallest definition; inside it I also chose (1) the names of six problem codes, (2) that a missing state file makes guard answer rejected, (3) that guard can run in any state, (4) that an anchor is required only where approvals need the strongest level; the other way is to leave CI out of the specification. This is a proposal; the owner can change any of these.
- Before: none (new text)
- After: "The action `guard` MUST NOT execute any command that the change or the project defines, that is the commands of gates, the evidence commands, and the interpreter that the project names (Sections 24.9 and 24.10), and an implementation MUST NOT execute one on its behalf."

## The text under approval

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `93f8278f1b0427444016cdbfa4b0e4ff9d16d369` |
| Reviewed SHA-256 | `6c0e86dd39e74242566755db6702972d893a83cc4827d9fc7e4805f89db85d91` |
| Line count | `4770` |
| Diffstat | `1 file changed, 3393 insertions(+), 45 deletions(-)` |
| Commits touching the file | `46` |
| Previously approved blob and SHA-256 | `ed758c46d5ac901359ab2c0df8e437ef89fed0f1` and `45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3` |
| Register file | `.planning/reviews/2026-10-26-normative-spec-fix-round-register.md` |
| Register blob | `362290846b8c0dd7be0938aede4dcaae4c5bd632` |

## The exact change

The change from the text approved in round 1 has 22 hunks, adds 136 lines and removes 15 lines.

```
@@ -886,30 +886,34 @@ Then the status `done` is legal as the local completion signal of the phase, and
 
 | Action | Legal From (Phase/Status) | Precondition | Gate Order | Resulting Phase/Status | Rejection Behavior |
 |---|---|---|---|---|---|
-| `start` | A non-closed phase with status `ready` | Starting the phase is authorized. | DoF → DoW; current-phase DoR was established by `ready`, and current-phase DoD and next-phase DoR are not applicable. | Same phase with status `active`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |
+| `start` | A non-closed phase with status `ready` | Starting the phase is authorized. | DoF → DoW; current-phase DoR was established by `ready`, and current-phase DoD and next-phase DoR are not applicable. | Same phase with status `active`. | Reject without any partial mutation of persisted state when the precondition is not satisfied or an applicable gate would decide against the start: a Definition of Fail condition that is active (a hard failure included), a Definition of Wait condition that is active, or a gate that cannot be evaluated (Section 24.2). |
 | `complete` | A non-closed phase with status `draft`, `active`, or `done` | The phase and status are a legal source, and the evaluation is requested: from `draft`, of the current phase's DoR; from `active`, of the current phase's DoD; from `done`, of the next phase's DoR. | From `draft`: DoF → DoW → current-phase DoR. From `active`: DoF → DoW → current-phase DoD → next-phase DoR. From `done`: DoF → DoW → next-phase DoR; current-phase DoR and DoD are already established. | From `draft`, the same phase with status `ready`. From `active`, satisfied current-phase DoD first produces the current phase with status `done`; satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. From `done`, satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. Completion of the final phase produces `closed`/`done`. | Reject without any partial mutation of persisted state when the phase and status are not a legal source. When DoW, current-phase DoR, or current-phase DoD does not allow the transition, record the evaluation in the history and answer `blocked` (Section 22.2); an active fail condition of the severity `hard` closes the change as failed, and a soft fail condition or a gate that cannot be evaluated puts the change in a wait (Sections 24.7 and 24.2). Unsatisfied next-phase DoR is not a rejection after current-phase DoD succeeds or during re-evaluation from `done`; it preserves the current phase with status `done`. |
-| `wait` | Any non-closed phase/status | A DoW condition is active. | DoF → DoW; current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | Same phase with status `waiting`. | Reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure. |
+| `wait` | Any non-closed phase/status | A DoW condition is active. | DoF → DoW; current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | Same phase with status `waiting`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When DoF finds a fail condition of the severity `hard` active, close the change as failed in the same state mutation and answer `success` (Section 24.7). |
 | `resume` | A non-closed phase with status `waiting` | The recorded resume condition is satisfied and the recorded or explicitly required resume phase is non-closed. | DoF → DoW → DoR for the recorded non-closed resume phase or explicitly required earlier non-closed phase; current-phase DoD and next-phase DoR are not applicable. | Recorded non-closed resume phase, or an explicitly required earlier non-closed phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When the resume-phase DoR is not satisfied or a DoW condition is still active, record the evaluation in the history, remain `waiting`, and answer `blocked` (Section 22.2). Fail when DoF determines failure (Section 24.7). |
 | `fail` | Any non-closed phase/status | A DoF condition is active. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
 | `cancel` | Any non-closed phase/status | An authorized cancellation decision exists. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `cancelled`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
 | `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
-| `reopen` (`full` only) | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF for the new corrective scope → DoW for the new corrective scope → DoR for the recorded resume phase or explicitly stated earlier phase; the prior terminal outcome's DoF and DoW, closed-phase DoD, and next-phase DoR are not applicable. | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied; wait when the new corrective scope's DoW determines a pause; fail when the new corrective scope's DoF determines failure. |
+| `reopen` (`full` only) | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF for the new corrective scope → DoW for the new corrective scope → DoR for the recorded resume phase or explicitly stated earlier phase; the prior terminal outcome's DoF and DoW, closed-phase DoD, and next-phase DoR are not applicable. | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied or a DoW condition of the new corrective scope is active; fail when the new corrective scope's DoF determines failure. |
 
 **Rejected and Blocked Results per Action (`full`)**
 
 | Action | Answers `rejected` (nothing is written, `changed` is `false`) | Answers `blocked` (the evaluation is recorded, `changed` is `true`) |
 |---|---|---|
-| `start` | The phase does not have the status `ready`, the start is not authorized, or an applicable gate does not allow the start (issue code `start-blocked`). | Never. |
+| `start` | The phase does not have the status `ready`, the start is not authorized, or an applicable gate does not allow the start or cannot be evaluated (issue code `start-blocked`). | Never. |
 | `complete` | The phase and status are not a legal source. | DoW, current-phase DoR, or current-phase DoD does not allow the transition, including a wait that a soft fail condition or a gate that cannot be evaluated causes. |
 | `wait` | The change is closed, or no DoW condition is active. | Never. |
 | `resume` | The status is not `waiting`, the resume condition is not satisfied, or the resume phase is closed. | The resume-phase DoR is not satisfied, or a DoW condition is still active, so that the change remains `waiting`. |
 | `fail` | The change is closed, or no DoF condition is active. | Never. |
 | `cancel` | The change is closed, or no authorized cancellation decision exists. | Never. |
 | `supersede` | The change is closed, or no later change is authorized to replace this change. | Never. |
-| `reopen` | The change is not in the `closed` phase, the corrective follow-up work is not authorized with a reason and a new goal-bound scope, or the resume-phase DoR is not satisfied. | Never. |
+| `reopen` | The change is not in the `closed` phase, the corrective follow-up work is not authorized with a reason and a new goal-bound scope, the resume-phase DoR is not satisfied, or a Definition of Wait condition of the new corrective scope is active. | Never. |
 
 An action whose evaluation closes the change as failed answers `success` (Section 24.7). An action answers `blocked` only where this table lists a case, and a `complete` that preserves the current phase with the status `done` because the next-phase DoR is not satisfied answers `success`. See AE-121, AE-122, AE-123, AE-124.
 
+Section 24.2 states what `wait`, `fail`, `cancel`, `supersede`, and `reopen` of the `full` profile answer when a gate that applies to them cannot be evaluated.
+
+The contract operations `approve`, `ask`, `answer`, `adopt`, and `migrate` (Sections 22.1, 24.3, 24.4, 24.8, and 25.3) are not rows of this table: they leave the phase and the status unchanged, and each is recorded under its own action name (Section 25.1).
+
 **AE-121 — Complete is blocked when the Definition of Done is not satisfied**
 
 - Covers: Section 8.3
@@ -942,7 +946,7 @@ Given a `full` change whose phase has the status `ready` and a Definition of Wai
 When the `start` action is requested  
 Then the result is `rejected` with `changed` false and the issue code `start-blocked`, and the status remains `ready`
 
-See AE-239, AE-240, AE-241, AE-242, AE-243, AE-244, AE-245, AE-246.
+See AE-239, AE-240, AE-241, AE-242, AE-243, AE-244, AE-245, AE-246, AE-295, AE-296, AE-297, AE-298.
 
 **AE-239 — Start a ready phase**
 
@@ -952,6 +956,14 @@ Given a `full` change in the build phase with the status `ready`, an authorizati
 When the `start` action is requested for each change  
 Then the first change has the status `active` in the same phase, and the request for the second change is rejected with `changed` false, because `draft` is not a legal source of `start`
 
+**AE-297 — Start is rejected when a gate cannot be evaluated**
+
+- Covers: Section 8.3 (`start`)
+
+Given a `full` change whose phase has the status `ready`, an authorization to start, and a Definition of Wait condition that cannot be evaluated because version control is unavailable  
+When the `start` action is requested  
+Then the result is `rejected` with `changed` false and the issue code `start-blocked`, the status remains `ready`, and no wait state is created
+
 **AE-240 — Complete a phase, with and without the next Definition of Ready**
 
 - Covers: Section 8.3 (`complete`)
@@ -968,6 +980,14 @@ Given a `full` change in the plan phase with the status `active` and an active D
 When the `wait` action is requested for each change  
 Then the first change has the status `waiting` in the same phase, and the request for the second change is rejected with `changed` false
 
+**AE-295 — A wait request on a change with a hard failure closes the change as failed**
+
+- Covers: Section 8.3 (`wait`)
+
+Given a `full` change in the plan phase with the status `active`, an active Definition of Wait condition, and an active Definition of Fail condition of the severity `hard`  
+When the `wait` action is requested  
+Then the change is in the `closed` phase with the status `failed`, the result is `success`, and no wait state is recorded
+
 **AE-242 — Resume when the resume condition holds**
 
 - Covers: Section 8.3 (`resume`)
@@ -992,6 +1012,14 @@ Given a `full` change in the build phase with the status `waiting` because of an
 When the `cancel` action is requested for each change  
 Then the first change is in the `closed` phase with the status `cancelled`, and the second change is in the `closed` phase with the status `failed`, because the Definition of Fail has first priority
 
+**AE-298 — Cancel proceeds when a gate cannot be evaluated**
+
+- Covers: Section 8.3 (`cancel`)
+
+Given a `full` change in the build phase with the status `active`, an authorized cancellation decision, and a Definition of Fail condition that cannot be evaluated because its program is missing  
+When the `cancel` action is requested  
+Then the change is in the `closed` phase with the status `cancelled`, and the result `not_evaluable` of the condition is recorded with its cause
+
 **AE-245 — Supersede needs a later change**
 
 - Covers: Section 8.3 (`supersede`)
@@ -1008,6 +1036,14 @@ Given a `full` change in the `closed` phase with the status `done` whose resume
 When the `reopen` action is requested for each change, with a reason and a new goal-bound scope  
 Then the first change returns to the build phase with the status `active`, and the request for the second change is rejected with `changed` false, because that change is not in the `closed` phase
 
+**AE-296 — Reopen of a `full` change is rejected when the new corrective scope would have to wait**
+
+- Covers: Section 8.3 (`reopen`)
+
+Given a `full` change in the `closed` phase with the status `done` whose resume phase recorded at closure is the build phase, and a Definition of Wait condition of the new corrective scope that is active  
+When the `reopen` action is requested with a reason and a new goal-bound scope  
+Then the result is `rejected` with `changed` false, and the change stays in the `closed` phase
+
 ### 8.4 Cancellation, Supersession, Reopening, and Terminal Behavior
 
 `cancel` moves any non-closed phase/status to the `closed` phase with status `cancelled` when an authorized cancellation decision exists. `supersede` moves any non-closed phase/status to the `closed` phase with status `superseded` when a later change replaces this change's goal.
@@ -1015,7 +1051,8 @@ Then the first change returns to the build phase with the status `active`, and t
 For `cancel` and `supersede`, an active DoW condition does not prevent the authorized terminal
 action. DoW and the current- and next-phase readiness and completion gates are not applicable to
 these actions. DoF retains first priority; when DoF determines that the change has failed, the
-resulting terminal status is `failed` rather than `cancelled` or `superseded`.
+resulting terminal status is `failed` rather than `cancelled` or `superseded`. A gate that cannot be evaluated
+determines no failure, so that the action takes effect (Section 24.2).
 
 The comparison of the gate definitions with the approved ones (Section 24.1) does not stop `cancel` or `supersede`.
 
@@ -1057,7 +1094,7 @@ A satisfied DoD does not override a satisfied DoF or DoW.
 
 This order defines evaluation precedence. A gate that is not applicable to the requested action or current state is skipped and, when gate evidence is recorded, MUST be recorded as `not_applicable`. Evaluation MUST stop as soon as a gate determines the requested action's outcome.
 
-A gate evaluation has one of three results: `satisfied`, `not_satisfied`, or `not_evaluable`. A gate that cannot be evaluated is neither failed nor `not_applicable`: the change waits, and a known hard failure is decided before it. Section 24.2 specifies these results and refines this order. It also states that the gates are evaluated by group, that a group is evaluated whole, and that the evaluation stops after the first group that decides.
+A gate evaluation has one of three results: `satisfied`, `not_satisfied`, or `not_evaluable`. A gate that cannot be evaluated is neither failed nor `not_applicable`: the change waits, except that the action `start` is rejected instead of waiting, `cancel` and `supersede` proceed, and `wait`, `fail`, and `reopen` of the `full` profile are rejected (Section 24.2), and a known hard failure is decided before it. Section 24.2 specifies these results and refines this order. It also states that the gates are evaluated by group, that a group is evaluated whole, and that the evaluation stops after the first group that decides.
 
 See AE-248.
 
@@ -1437,6 +1474,8 @@ DoF describes conditions under which the flow MUST terminate unsuccessfully.
 
 The obligation to terminate applies to a fail condition of the severity `hard`. A fail condition of the severity `soft` pauses the flow for a human disposition (Section 24.7).
 
+A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition, and the human closes the change as failed or records an override (Section 24.7).
+
 ### 12.1 Typical Fail Categories
 
 - critical technical error,
@@ -2155,7 +2194,7 @@ A GG-SAD automation contract MUST support these technology-neutral operations:
 - migrate a schema-governed file to a newer schema version, as an explicit operation whose steps are recorded (Section 25.3);
 - record a question of a change (Section 24.8);
 - adopt the history of a change (Section 24.4);
-- report on a change, as the read-only actions `check`, `review`, and `guard` do;
+- report on a change, as the read-only actions `check`, `review`, and `guard` (Section 22.4) do;
 - evaluate and execute one controlled state transition under the transition table of the method profile of the change (Section 8.3 or Section 23.4). See AE-287.
 
 **AE-287 — Asking a question is an operation of the contract**
@@ -2243,6 +2282,48 @@ A valid operation whose evaluation says that the requested transition does not o
 
 For every operation, an implementation MUST emit both an actionable human-readable message and the structured result envelope. It MUST record transition history and relevant evidence under the transition table of the method profile of the change (Section 8.3 or Section 23.4) and Section 15 Evidence Model.
 
+### 22.4 The `guard` Action
+
+The action `guard` is the verify-only action. It is defined for both method profiles. It is read-only: it never changes the state or the history of a change, it is legal from every state and phase, and it is not a row of the table of Section 8.3 or of Section 23.4.
+
+The action performs five verifications and reports the result of each:
+
+1. The history is consistent (Section 24.4) and, where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor.
+2. The gate definitions equal the approved ones (Section 24.1).
+3. Every approval is current for the content it names and has the level that the configuration or the gate requires (Section 24.3).
+4. The scope, measured against the base revision, holds (Section 24.5).
+5. No fail condition of the severity `hard` is active (Section 24.7). This is decided from the results that the history records and from the measurement of the scope, and not by running a command.
+
+The action `guard` MUST NOT execute any command that the change or the project defines, that is the commands of gates, the evidence commands, and the interpreter that the project names (Sections 24.9 and 24.10), and an implementation MUST NOT execute one on its behalf.
+
+The result is `success` with `changed` false when all five verifications hold. Otherwise the result is `rejected` with `changed` false and at least one issue that names each verification that failed, with these stable issue codes: `history-inconsistent` and `anchor-missing` for the first verification, `gates-changed` (Section 24.1) for the second, `approval-stale` for the third, `scope-violation` for the fourth, and `hard-failure-active` for the fifth. A verification that needs a state document that the change does not have is reported as not enforced, and it makes the result `rejected` (Sections 24.1 and 25.1).
+
+Because the action runs nothing, it proves the record and not the outcome: it cannot confirm that the checks of the change pass, and running them stays a separate task. A pipeline that runs `guard` on a change is the verify-only integration of the method, and enforcement is by the caller, which acts on the result. See AE-303, AE-304, AE-305.
+
+**AE-303 — A guard on a sound change succeeds and starts no program**
+
+- Covers: Section 22.4
+
+Given an `active` `core` change whose approved gate definitions are unchanged, with a consistent history, a scope that holds, no hard failure recorded, and a `check` gate whose program is missing  
+When the `guard` action is requested  
+Then the result is `success` with `changed` false, and no program is started
+
+**AE-304 — A guard rejects a change whose gate definitions were edited**
+
+- Covers: Section 22.4
+
+Given an `active` `core` change whose gate definitions were edited after their approval and have not been approved again  
+When the `guard` action is requested  
+Then the result is `rejected` with `changed` false and the issue code `gates-changed`, and the history is unchanged
+
+**AE-305 — A guard on an inline record reports that the verifications are not enforced**
+
+- Covers: Section 22.4
+
+Given a `full` change in the build phase with the status `active` whose record is kept inline, without a state document  
+When the `guard` action is requested  
+Then the result is `rejected` with `changed` false, and an issue states that the verifications that need a state document are not enforced
+
 ---
 
 ## 23. The `core` Profile
@@ -2445,20 +2526,20 @@ A `core` change changes state only through the actions of the table below. An ac
 |---|---|---|---|
 | `new` | No change with the given identifier exists | The change definition is valid under Sections 23.1 and 23.3, its method profile is selected under Section 5.6, its identifier follows the syntax of Section 4.3 and is unique, and `follows`, when present, names a closed change. | The state `open` with the outcome `null` and the initial record of Section 23.2, and the anchor at position 1 where an anchor is kept or required (Section 24.4). See AE-19, AE-20, AE-278. |
 | `approve` | Any state except `closed` | The approval has one target. For `spec`, no question is unanswered (Section 24.8). For `gates`, the gate definitions are valid under Section 23.3. For `all`, both conditions hold. For `override`, a soft fail condition awaits disposition (Section 24.7), and the approval gives a reason and at least one further attempt. For a named gate, the gate is a `sign-off` done gate of the change. Section 24.1 governs the re-approval of changed gate definitions. | The state and the outcome do not change, and the approval is recorded. See AE-21, AE-22, AE-23, AE-24. |
-| `start` | `open` | The gate definitions are approved and unchanged since approval (Section 24.1), the specification is approved when the compliance profile or the project configuration requires it, the revision from which the change starts can be recorded (Section 24.5), and the evaluation of Section 23.6 finds no fail gate and no wait gate active. | The state `active`, with the base revision recorded. See AE-25, AE-26. |
+| `start` | `open` | The gate definitions are approved and unchanged since approval (Section 24.1), the specification is approved when the compliance profile or the project configuration requires it, the revision from which the change starts can be recorded (Section 24.5), and none of the steps 1 to 4 of Section 23.6 would decide, so that a fail gate that is active, a gate that cannot be evaluated, or a wait gate that is active prevents the start. | The state `active`, with the base revision recorded. See AE-25, AE-26. |
 | `wait` | `active` | A reason, an owner, and a resume condition are given, or an unanswered question is named. A named question exists and is unanswered, and the action never creates a question. When a question is named, the owner of the wait is the owner of the question and a different owner is rejected, and the reason and the resume condition default to awaiting the answer to the question (Section 24.8). | The state `waiting`, with a wait record of kind `manual`, or of kind `question` when the action names a question (Section 23.5). See AE-27, AE-28, AE-29, AE-275. |
 | `ask` | `open`, `active`, `waiting` | The question has a text and an owner, which defaults to the owner of the change. A structured question has at least two distinct options. | The state does not change, and an unanswered question with the next identifier is recorded (Section 24.8). In the state `waiting`, the wait record does not change, and the change cannot resume until the question is answered (Section 23.7). See AE-30, AE-31, AE-274. |
 | `answer` | Any state except `closed` | The question exists and is unanswered. The answer comes from the owner of the question. A structured question receives one of its options, and a free-text question receives a text. | The state does not change, and the question is recorded as answered. An answer does not resume a waiting change. See AE-32, AE-33, AE-34. |
 | `resume` | `waiting` | The resume condition of the wait record is satisfied (Section 23.5). | The state `active`, when the evaluation of Section 23.6 finds no gate that decides otherwise. Otherwise the change remains `waiting`, or becomes `closed` with the outcome `failed`, as Section 23.6 decides. See AE-35, AE-36. |
 | `close` | `active` | The evaluation of Section 23.6 finds no fail gate and no wait gate active, and every done gate is satisfied. | The state `closed` with the outcome `done`. When the evaluation finds otherwise, the change does not close: it remains `active` when a wait gate is active or a done gate is not satisfied, becomes `waiting` when Section 23.6 requires a wait, and becomes `closed` with the outcome `failed` when a hard fail condition is active. See AE-37, AE-38. |
 | `fail` | `waiting`, with a wait record of kind `fail-gate` | A soft fail condition awaits disposition (Section 24.7), and a reason text is given. | The state `closed` with the outcome `failed` and the reason recorded. See AE-39, AE-40, AE-41. |
-| `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active. See AE-42, AE-43. |
+| `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). A gate that cannot be evaluated determines no failure and does not prevent it (Section 24.2). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active. See AE-42, AE-43. |
 | `supersede` | Any state except `closed` | The preconditions of `cancel` hold, and `replaced_by` names a different change that exists. | As `cancel`, with `replaced_by` recorded in the closed change. See AE-44, AE-45. |
 | `adopt` | Any state | The history of the change has no anchor (Section 24.4). | The state and the outcome do not change, and the anchor is created from the history as it is. See AE-46, AE-47. |
 
 The actions `approve`, `fail`, `cancel`, `supersede`, and `adopt` MUST be performed by a human participant. An `answer` to a question whose owner is a human MUST also be given by a human (Section 24.3). See AE-24.
 
-The actions `check`, `review`, and `guard` are read-only. They report on a change, they never change its state or its history, and they are legal from every state. They are not rows of the table. See AE-49.
+The actions `check`, `review`, and `guard` (Section 22.4) are read-only. They report on a change, they never change its state or its history, and they are legal from every state. They are not rows of the table. See AE-49.
 
 The method profile `core` has no `reopen` action. A change in the state `closed` is final, and follow-up work is a new change that names the closed change in `follows` (Section 23.1). See AE-48.
 
@@ -2483,6 +2564,8 @@ A `follows` field is a reference and not a state transition: it never changes th
 
 A `close` or a `resume` whose evaluation finds a fail gate of the severity `hard` active answers `success` with the state `closed` and the outcome `failed` (Section 24.7). An action answers `blocked` only where this table lists a case. See AE-117, AE-118, AE-119, AE-120.
 
+Section 24.2 states what `cancel` and `supersede` answer when a gate that applies to them cannot be evaluated: they take effect, and the result `not_evaluable` is recorded. See AE-299.
+
 **AE-117 — Start with an unmet gate is rejected**
 
 - Covers: Section 23.4
@@ -2731,6 +2814,14 @@ Given an `active` change with a hard fail condition active
 When a human performs the `cancel` action  
 Then the state is `closed` and the outcome is `failed`, not `cancelled`
 
+**AE-299 — Cancel proceeds when a fail gate cannot be evaluated**
+
+- Covers: Section 23.4 (`cancel`)
+
+Given an `active` `core` change with a fail gate of the severity `hard` whose command cannot start because its program is missing  
+When a human performs the `cancel` action  
+Then the state is `closed` and the outcome is `cancelled`, the result of the fail gate is `not_evaluable`, and no failure is recorded
+
 **AE-44 — Supersede a change**
 
 - Covers: Section 23.4 (`supersede`)
@@ -2983,7 +3074,7 @@ Every protection of Sections 24.1 to 24.10, and the result `blocked` of Section
 | Scope and isolation | 24.5 | `scope.allow` of the change definition, and the base revision recorded when `start` succeeds | The allowed path list in the Scope of the change specification (Section 16.1), and the base revision recorded when the first phase begins |
 | Known-failure baselines | 24.6 | A baseline on a `check` done gate | A baseline on a verification condition that names a check command (Section 10.7) |
 | Hard and soft failure | 24.7 | The severity of a fail gate; a soft failure puts the change in a wait of kind `fail-gate` | The severity of a fail rule (Section 12.2); a soft failure puts the change in the status `waiting` with the category `WAIT_DECISION` |
-| Open questions as state | 24.8 | The actions `ask` and `answer` and the base gate `unanswered-question` | The question is recorded in the state file, and a Definition of Wait condition is active while it is unanswered |
+| Open questions as state | 24.8 | The actions `ask` and `answer` and the base gate `unanswered-question` | The action `ask` records the question in the state file, and a Definition of Wait condition is active while it is unanswered |
 | Executable evidence | 24.9 | The base gate `incomplete-evidence` | Verify-Done (Section 10.7) and the completion criteria (Section 20) |
 | Gate-command interpreter | 24.10 | The commands of `check` gates and the evidence commands | The commands of the Flow Gates and the evidence commands |
 | The result `blocked` | 22.2 | The actions `close` and `resume` (Section 23.4) | The actions `complete` and `resume` (Section 8.3) |
@@ -3240,8 +3331,12 @@ An action that evaluates gates decides from the results in this order, and the f
 4. A wait gate that is active: the change does not advance.
 5. For an action that completes a change or a phase, a done gate that is `not_satisfied`: the change does not complete.
 
+In `full`, the Definitions of Ready (Section 8.5) take part in the evaluation, and the rules rank their results as follows. A condition of the Definition of Fail is a fail gate, which rules 1 and 3 rank by its severity. A condition of the Definition of Wait is a wait gate, which rule 4 ranks. A condition of the Definition of Done is a done gate, which rule 5 ranks. The Definition of Ready of the current phase, for `complete` from `draft`, and the Definition of Ready of the resume phase, for `resume` and `reopen`, rank with rule 5 for the action concerned: when one is not satisfied, the transition does not occur and the action answers as Section 8.3 states. The Definition of Ready of the next phase decides nothing: when it is not satisfied, the current phase is completed and not advanced, and the action answers `success` (Section 8.3). See AE-300.
+
 A known hard failure therefore outranks a gate that cannot be evaluated. This order refines Section 8.5 and Section 23.6. The `start` action requires that none of the rules 1 to 4 would decide: when one would, `start` is rejected and no wait is created, and a hard failure included, because `start` never closes a change (Section 24.7). When the action is `resume`, the wait record created by rule 2 replaces the earlier record, whose resume condition was met. An action that only reports on a change reports the result and creates no wait. See AE-69, AE-71, AE-72, AE-74.
 
+Rule 2 does not make the other actions that evaluate gates and never answer `blocked` wait, because a wait is a recorded change that they cannot answer (Section 22.2). In `full`, these actions are `wait`, `fail`, `cancel`, `supersede`, and `reopen`; in `core`, they are `cancel` and `supersede`, which look for an active hard failure. When no hard failure is active and a gate that applies to one of them cannot be evaluated, `cancel` and `supersede` take effect, because an authorized cancellation is not held up by a check that cannot run and a gate that cannot be evaluated is never a failure, and the result `not_evaluable` of the gate and its cause are recorded in the entry of the action. The actions `wait`, `fail`, and `reopen` are rejected with `changed` false, nothing is written, no wait is created, and the stable issue code is `gate-not-evaluable`. See AE-298, AE-299.
+
 The gates are evaluated by group. The order of the groups is the order of Section 23.6 in `core`, that is the fail gates, the wait gates, and the done gates, and the order of Section 8.5 in `full`, that is the Definition of Fail, the Definition of Wait, the Definition of Ready of the current phase, the Definition of Done, and the Definition of Ready of the next phase. A group is evaluated whole: every gate of the group that applies to the action is evaluated, even when an earlier gate of the same group already decides. After a group, the evaluation stops if the results of the groups evaluated so far decide the action under the rules 1 to 5, so that a gate of a later group is not evaluated: its command is not run, and no result is recorded for it. The rules rank the results of the gates that were evaluated, so that a gate which is not evaluated cannot outrank a gate which is. In `core`, a wait gate that is active therefore decides before a done gate that cannot be evaluated, the change does not become `waiting` for that done gate, and the `close` action answers `blocked`. A wait gate that cannot be evaluated is `not_evaluable`, and it creates a wait record of kind `external` before any done gate is evaluated. See AE-280.
 
 A retry limit is a fail condition that becomes active when the number of `not_satisfied` results recorded for a named gate reaches a limit. The count is the number of `not_satisfied` results of that gate in the history over the whole life of the change, a non-negative integer. The limit is a non-negative integer, and it is reached when the count is greater than or equal to the limit: with a limit of three, the third `not_satisfied` result reaches it and the second does not. A `satisfied` result, a `not_evaluable` result, and a `not_applicable` record are not counted, and a `not_evaluable` result between two `not_satisfied` results neither adds to the count nor resets it. A retry limit that is not a non-negative integer is invalid and MUST be rejected when the gate definitions are approved. See AE-63, AE-64, AE-70.
@@ -3380,6 +3475,14 @@ Given an `open` `core` change with a wait gate whose condition cannot be evaluat
 When the `start` action is requested  
 Then the action is rejected, the change remains `open`, and no wait record is created
 
+**AE-300 — Full: a Definition of Ready of the current phase that is not satisfied blocks the completion**
+
+- Covers: Section 24.2 (full)
+
+Given a `full` change in the build phase with the status `draft` whose Definition of Ready of the current phase is not satisfied  
+When the `complete` action is requested  
+Then the result is `blocked` with `changed` true, the evaluation is recorded in the history, and the status stays `draft`
+
 ### 24.3 Assurance Levels and Signed Approval
 
 Every action on a change is performed under an identity that the participant claims. This section defines three assurance levels, which state how well a claim was checked; the statement that a signed approval signs; the actions that only a human may perform; and the limit of what any level proves.
@@ -3877,6 +3980,8 @@ A soft failure pauses the change for a human. When an action that evaluates gate
 
 The `fail` action is valid only while a soft failure awaits disposition. See AE-99, AE-100, AE-101.
 
+When a retry limit is reached, the change waits as it does for a soft failure, and the human closes the change as failed or records an override. Nothing ends the change automatically.
+
 An override is recorded by a human as an approval with the target `override` (Section 23.4). It MUST name the soft fail condition that it applies to, MUST give a reason, and MUST give a number N of further attempts. N MUST be an integer greater than or equal to 1. This specification defines no default for N: a request that gives no number, a number below 1, or a number that is not an integer MUST be rejected, and so MUST a request that gives no reason. An override is valid only for a fail condition of the severity `soft` that awaits disposition. An override for any other fail condition MUST be rejected. See AE-104, AE-105, AE-106, AE-107, AE-109.
 
 An attempt is one evaluation by the action that completes the change (in `core`, `close`; in `full`, `complete`) that is made while the override is in force. An evaluation that ends in the wait of Section 24.2 for a gate that cannot be evaluated is not an attempt. While the override is in force, the soft failure that it covers does not pause the change. The N-th attempt is allowed, and the evaluation after it pauses the change again, as a soft failure does. See AE-102.
@@ -4015,7 +4120,7 @@ An open question is part of the state of the change and is recorded in its histo
 - `answer`: absent while the question is unanswered;
 - `answerer`: the participant that gave the answer.
 
-In `core`, the `ask` action records a question without pausing the change, and the `wait` action that names an unanswered question pauses the change with a wait record of kind `question`; the `wait` action never creates a question (Sections 23.4 and 23.5). In `full`, a question is recorded in the state file, or in the inline record where no state file is persisted (Section 4.3), and the answer is recorded as a human decision (Section 22.1). A wait that a question causes has the category `WAIT_USER_INPUT` (Section 11.1).
+In `core`, the `ask` action records a question without pausing the change, and the `wait` action that names an unanswered question pauses the change with a wait record of kind `question`; the `wait` action never creates a question (Sections 23.4 and 23.5). In `full`, the operation that records a question is the action `ask`, which is not a transition: its entry has the action name `ask` (Section 25.1), it leaves the phase and the status unchanged, and it is legal for a change that is not in the `closed` phase. The question is recorded in the state file, or in the inline record where no state file is persisted (Section 4.3), and the answer is recorded as a human decision (Section 22.1). See AE-301. A wait that a question causes has the category `WAIT_USER_INPUT` (Section 11.1).
 
 Two options are distinct when they differ as sequences of code points (Section 24). A structured question with fewer than two distinct options MUST be rejected, and so MUST a structured question whose list repeats an option. Question identifiers are compared in the same way, so that `Q1` and `q1` are different identifiers. See AE-177, AE-181.
 
@@ -4123,6 +4228,14 @@ Given a `full` change in the specify phase with the status `active` and the unan
 When the `complete` action is requested  
 Then the result is `blocked` with `changed` true, the issues name Q1, and the phase and status do not change
 
+**AE-301 — Full: asking a question is the action ask and changes neither the phase nor the status**
+
+- Covers: Section 24.8 (full)
+
+Given a `full` change in the build phase with the status `active`  
+When a participant records a question with a text and the owner of the change  
+Then the entry has the action `ask`, the phase and the status are unchanged, and the question is unanswered
+
 ### 24.9 Executable Evidence
 
 The evidence for a requirement is executable and is bound to that requirement. An evidence command is a check command as Section 24.2 defines it: an argument list, an exit map, and OPTIONALLY a time limit. It is run as Section 24.10 states. A requirement lists the evidence commands that are bound to it: in `core`, in the field `requirements` of the change definition (Section 23.1); in `full`, in the change specification, under the heading Evidence Commands of the requirement (Section 16.1).
@@ -4470,7 +4583,7 @@ The content hash of a text file is the hash string of the bytes of the file afte
 
 The content hash of a binary file is the hash string of the bytes of the file, exactly. See AE-198.
 
-Whether a file is text or binary is decided by the implementation. The decision MUST depend only on the bytes of the file, so that the same bytes are always classified in the same way, and an implementation SHOULD classify a file as text only when its bytes are valid UTF-8 and hold no zero byte. The hash string does not state which kind was applied. A content hash is therefore comparable only with a content hash that an implementation computed with the same decision, and a content hash that differs from the recorded one is a difference. See AE-198.
+A file is text exactly when its bytes are valid UTF-8 and hold no zero byte, and every other file is binary. An implementation MUST classify a file in this way. Valid UTF-8 is a sequence of bytes that encodes Unicode scalar values in the shortest form, with no surrogate code point and no value above U+10FFFF. The decision depends on the bytes only, so that every conforming implementation computes the same content hash for the same bytes. The hash string does not state which kind was applied, and a content hash that one implementation computed can be compared with one that another implementation computed. A content hash that differs from the recorded one is a difference. See AE-198, AE-302.
 
 The content hash of a parsed definition, such as the gate definitions of a change (Section 24.1), is the hash string of the canonical bytes of the parsed value (Section 25.1) and not of the text of the file. A YAML document is read as YAML 1.2 with its core schema, and an alias is replaced by the value it refers to. Comments, layout, the order of the keys of a mapping, and the quoting of a scalar that reads as the same value therefore have no effect, and the order of the elements of a sequence has an effect. A parsed value that is outside the domain of Section 25.1 has no content hash: this holds for a floating-point number, a mapping key that is not a string, a mapping that repeats a key, and a scalar that the core schema reads as a type that the domain does not hold. An operation that needs the content hash of such a definition MUST be rejected, and its issue states which value is outside the domain. See AE-199, AE-200.
 
@@ -4494,6 +4607,14 @@ Given two files that each hold the byte 00 and differ only in that the first hol
 When the content hash of each file is computed  
 Then the content hashes of the two files differ, the file whose bytes are not valid UTF-8 is hashed on its exact bytes, and the same bytes give the same content hash each time
 
+**AE-302 — The kind of a file is decided by its bytes**
+
+- Covers: Section 25.2
+
+Given three files with the line ending carriage return and line feed, of which the first holds text that is valid UTF-8, the second holds the byte 00, and the third holds bytes that are not valid UTF-8, and for each of them a variant with the line ending line feed alone  
+When the content hash of each of the six files is computed  
+Then the first file has the same content hash as its variant, because it is text, and the second and the third file each have a content hash that differs from the content hash of their variant, because they are binary and are hashed byte for byte
+
 **AE-199 — Layout and comments do not change the hash of a parsed definition, and a list order does**
 
 - Covers: Section 25.2
```

## Questions

### Q01 — Approval

- Question: Do you approve the new text exactly as it now stands (fingerprint 93f8278f1b04, 4770 lines), or do you want changes?
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

If you approve, the text goes to an independent review by a reviewer that is not the Requestor. That review is limited: it has one pass over the header and Sections 1 to 8, one pass over Sections 9 to 22 and one pass over the whole text read across sections. Sections 23, 24 and 25 have no pass of their own and are read only by the pass over the whole text. Any later edit of the specification voids the approval.

If you request changes, nothing is approved, the text is edited for them, the packet is printed again and you are asked again.

The tick of the requirement for owner approval from the first round is not changed by any plan and rests, for this text, on the record that follows this packet.

This packet is evidence only. It does not change the reviewed file.
