# Owner approval packet, fix round 3: proposed normative method specification

- Owner approval: recorded in the owner approval record

## What you are asked

On 2026-10-26 the owner approved the text of the specification. The independent reviewer then looked at it a second time; the owner asked for the three findings that the reviewer rated BLOCKING, its strongest rating, to be fixed, and chose how. The text has been changed in three places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.

## The three changes

| # | What changed | Why | Whose reading |
|---|---|---|---|
| 1 | The guard check now passes a history that has an anchor or an equivalent mechanism, as the history rules already allow. It reports a missing anchor only when the history has neither. | The guard asked for an anchor in so many words, so a change that correctly used an equivalent mechanism would have failed it. | your decision: Accept an equivalent |
| 2 | The scope check now counts only ignore files that lie inside the repository. They are ordinary files, so creating or changing one is a changed path that needs an allowed path, and ignore settings kept elsewhere are not applied. | Ignore settings kept outside the measured files could hide any out-of-scope work, because changing them left no changed path to count. | your decision: Repository files only |
| 3 | In the full profile, the fail action is now allowed only while a soft failure waits for a human. With only a hard failure active it is refused, and the change keeps its state. | One table said that fail is allowed whenever a failure condition is active, while the section on hard and soft failure said it is for a soft failure only. | your decision: Soft failures only |

## Before and after

### Change 1 of 3: How the guard check treats an equivalent to the history anchor

- Findings: RR-B-001
- Options offered: Accept an equivalent | Anchor only, said openly
- Your decision: Accept an equivalent; reason: none given
- Before: "where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor."
- After: "where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor or an equivalent mechanism (Section 24.4)."

### Change 2 of 3: How the scope check treats ignore settings

- Findings: RR-X-001
- Options offered: Repository files only | Detect any change | Measure every file | Say it openly
- Your decision: Repository files only; reason: none given
- Before: "A file that version control is told to ignore is invisible to the measurement."
- After: "Only ignore files inside the repository count. An ignore file is an ordinary file of the working tree, such as a `.gitignore` file, so that creating or changing one is a changed path, and it is a scope violation when no pattern of the allowed path list matches it."

### Change 3 of 3: When the fail action is allowed in the full profile

- Findings: RR-X-002
- Options offered: Soft failures only | Any active failure
- Your decision: Soft failures only; reason: none given
- Before: "A DoF condition is active."
- After: "A soft failure awaits disposition: the status is `waiting` with a wait state of the category `WAIT_DECISION` for a DoF condition of the severity `soft` that is active (Section 24.7)."

## The text under approval

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `a81d9c89651f326605db08708ea4c079809a2825` |
| Reviewed SHA-256 | `d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc` |
| Line count | `4794` |
| Diffstat | `1 file changed, 3419 insertions(+), 47 deletions(-)` |
| Commits touching the file | `49` |
| Previously approved blob and SHA-256 | `93f8278f1b0427444016cdbfa4b0e4ff9d16d369` and `6c0e86dd39e74242566755db6702972d893a83cc4827d9fc7e4805f89db85d91` |
| Register file | `.planning/reviews/2026-10-27-normative-spec-fix-round-3-register.md` |
| Register blob | `8c006d67ef5fa6de13a943aa9c821def6721f992` |

## The exact change

The change from the text approved in round 2 has 13 hunks, adds 39 lines and removes 15 lines.

```
@@ -890,7 +890,7 @@ Then the status `done` is legal as the local completion signal of the phase, and
 | `complete` | A non-closed phase with status `draft`, `active`, or `done` | The phase and status are a legal source, and the evaluation is requested: from `draft`, of the current phase's DoR; from `active`, of the current phase's DoD; from `done`, of the next phase's DoR. | From `draft`: DoF → DoW → current-phase DoR. From `active`: DoF → DoW → current-phase DoD → next-phase DoR. From `done`: DoF → DoW → next-phase DoR; current-phase DoR and DoD are already established. | From `draft`, the same phase with status `ready`. From `active`, satisfied current-phase DoD first produces the current phase with status `done`; satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. From `done`, satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. Completion of the final phase produces `closed`/`done`. | Reject without any partial mutation of persisted state when the phase and status are not a legal source. When DoW, current-phase DoR, or current-phase DoD does not allow the transition, record the evaluation in the history and answer `blocked` (Section 22.2); an active fail condition of the severity `hard` closes the change as failed, and a soft fail condition or a gate that cannot be evaluated puts the change in a wait (Sections 24.7 and 24.2). Unsatisfied next-phase DoR is not a rejection after current-phase DoD succeeds or during re-evaluation from `done`; it preserves the current phase with status `done`. |
 | `wait` | Any non-closed phase/status | A DoW condition is active. | DoF → DoW; current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | Same phase with status `waiting`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When DoF finds a fail condition of the severity `hard` active, close the change as failed in the same state mutation and answer `success` (Section 24.7). |
 | `resume` | A non-closed phase with status `waiting` | The recorded resume condition is satisfied and the recorded or explicitly required resume phase is non-closed. | DoF → DoW → DoR for the recorded non-closed resume phase or explicitly required earlier non-closed phase; current-phase DoD and next-phase DoR are not applicable. | Recorded non-closed resume phase, or an explicitly required earlier non-closed phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When the resume-phase DoR is not satisfied or a DoW condition is still active, record the evaluation in the history, remain `waiting`, and answer `blocked` (Section 22.2). Fail when DoF determines failure (Section 24.7). |
-| `fail` | Any non-closed phase/status | A DoF condition is active. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
+| `fail` | Any non-closed phase/status | A soft failure awaits disposition: the status is `waiting` with a wait state of the category `WAIT_DECISION` for a DoF condition of the severity `soft` that is active (Section 24.7). | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
 | `cancel` | Any non-closed phase/status | An authorized cancellation decision exists. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `cancelled`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
 | `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
 | `reopen` (`full` only) | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF for the new corrective scope → DoW for the new corrective scope → DoR for the recorded resume phase or explicitly stated earlier phase; the prior terminal outcome's DoF and DoW, closed-phase DoD, and next-phase DoR are not applicable. | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied or a DoW condition of the new corrective scope is active; fail when the new corrective scope's DoF determines failure. |
@@ -903,7 +903,7 @@ Then the status `done` is legal as the local completion signal of the phase, and
 | `complete` | The phase and status are not a legal source. | DoW, current-phase DoR, or current-phase DoD does not allow the transition, including a wait that a soft fail condition or a gate that cannot be evaluated causes. |
 | `wait` | The change is closed, or no DoW condition is active. | Never. |
 | `resume` | The status is not `waiting`, the resume condition is not satisfied, or the resume phase is closed. | The resume-phase DoR is not satisfied, or a DoW condition is still active, so that the change remains `waiting`. |
-| `fail` | The change is closed, or no DoF condition is active. | Never. |
+| `fail` | The change is closed, or no soft failure awaits disposition, so that an active DoF condition of the severity `hard` alone does not allow the action. | Never. |
 | `cancel` | The change is closed, or no authorized cancellation decision exists. | Never. |
 | `supersede` | The change is closed, or no later change is authorized to replace this change. | Never. |
 | `reopen` | The change is not in the `closed` phase, the corrective follow-up work is not authorized with a reason and a new goal-bound scope, the resume-phase DoR is not satisfied, or a Definition of Wait condition of the new corrective scope is active. | Never. |
@@ -946,7 +946,7 @@ Given a `full` change whose phase has the status `ready` and a Definition of Wai
 When the `start` action is requested  
 Then the result is `rejected` with `changed` false and the issue code `start-blocked`, and the status remains `ready`
 
-See AE-239, AE-240, AE-241, AE-242, AE-243, AE-244, AE-245, AE-246, AE-295, AE-296, AE-297, AE-298.
+See AE-239, AE-240, AE-241, AE-242, AE-243, AE-244, AE-245, AE-246, AE-295, AE-296, AE-297, AE-298, AE-308.
 
 **AE-239 — Start a ready phase**
 
@@ -996,14 +996,22 @@ Given a `full` change with the status `waiting` in the build phase whose resume
 When the `resume` action is requested for each change  
 Then the first change returns to the build phase with the status `active`, and the request for the second change is rejected with `changed` false, so that it remains `waiting`
 
-**AE-243 — Fail only while a Definition of Fail condition is active**
+**AE-243 — Fail only while a soft failure awaits disposition**
 
 - Covers: Section 8.3 (`fail`)
 
-Given a `full` change in the verify phase with an active Definition of Fail condition, and a second `full` change in the verify phase with no such condition  
+Given a `full` change in the verify phase with the status `waiting` because of an active Definition of Fail condition of the severity `soft`, and a second `full` change in the verify phase with no soft failure that awaits disposition  
 When the `fail` action is requested for each change  
 Then the first change is in the `closed` phase with the status `failed`, and the request for the second change is rejected with `changed` false
 
+**AE-308 — Fail is refused when only a hard failure is active**
+
+- Covers: Section 8.3 (`fail`)
+
+Given a `full` change in the verify phase with the status `active` and an active Definition of Fail condition of the severity `hard`, and no soft failure that awaits disposition  
+When the `fail` action is requested  
+Then the result is `rejected` with `changed` false, and the change keeps its phase and its status
+
 **AE-244 — Cancel is not prevented by a wait, and a failure has priority**
 
 - Covers: Section 8.3 (`cancel`)
@@ -2288,7 +2296,7 @@ The action `guard` is the verify-only action. It is defined for both method prof
 
 The action performs five verifications and reports the result of each:
 
-1. The history is consistent (Section 24.4) and, where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor.
+1. The history is consistent (Section 24.4) and, where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor or an equivalent mechanism (Section 24.4).
 2. The gate definitions equal the approved ones (Section 24.1).
 3. Every approval is current for the content it names and has the level that the configuration or the gate requires (Section 24.3).
 4. The scope, measured against the base revision, holds (Section 24.5).
@@ -2296,9 +2304,9 @@ The action performs five verifications and reports the result of each:
 
 The action `guard` MUST NOT execute any command that the change or the project defines, that is the commands of gates, the evidence commands, and the interpreter that the project names (Sections 24.9 and 24.10), and an implementation MUST NOT execute one on its behalf.
 
-The result is `success` with `changed` false when all five verifications hold. Otherwise the result is `rejected` with `changed` false and at least one issue that names each verification that failed, with these stable issue codes: `history-inconsistent` and `anchor-missing` for the first verification, `gates-changed` (Section 24.1) for the second, `approval-stale` for the third, `scope-violation` for the fourth, and `hard-failure-active` for the fifth. A verification that needs a state document that the change does not have is reported as not enforced, and it makes the result `rejected` (Sections 24.1 and 25.1).
+The result is `success` with `changed` false when all five verifications hold. Otherwise the result is `rejected` with `changed` false and at least one issue that names each verification that failed, with these stable issue codes: `history-inconsistent` and `anchor-missing` for the first verification (`anchor-missing` is reported when the history has neither an anchor nor an equivalent mechanism, Section 24.4), `gates-changed` (Section 24.1) for the second, `approval-stale` for the third, `scope-violation` for the fourth, and `hard-failure-active` for the fifth. A verification that needs a state document that the change does not have is reported as not enforced, and it makes the result `rejected` (Sections 24.1 and 25.1).
 
-Because the action runs nothing, it proves the record and not the outcome: it cannot confirm that the checks of the change pass, and running them stays a separate task. A pipeline that runs `guard` on a change is the verify-only integration of the method, and enforcement is by the caller, which acts on the result. See AE-303, AE-304, AE-305.
+Because the action runs nothing, it proves the record and not the outcome: it cannot confirm that the checks of the change pass, and running them stays a separate task. A pipeline that runs `guard` on a change is the verify-only integration of the method, and enforcement is by the caller, which acts on the result. See AE-303, AE-304, AE-305, AE-306.
 
 **AE-303 — A guard on a sound change succeeds and starts no program**
 
@@ -2324,6 +2332,14 @@ Given a `full` change in the build phase with the status `active` whose record i
 When the `guard` action is requested  
 Then the result is `rejected` with `changed` false, and an issue states that the verifications that need a state document are not enforced
 
+**AE-306 — A guard accepts an equivalent mechanism in place of an anchor**
+
+- Covers: Section 22.4
+
+Given a project whose configuration requires approvals at the level A2, and a change with a consistent history, no anchor, and an independent append-only record outside the working tree that holds the latest position and hash and is written only after each successful append  
+When the `guard` action is requested  
+Then the first verification holds, the issue code `anchor-missing` is not reported, and the result is `success` with `changed` false when the other four verifications hold
+
 ---
 
 ## 23. The `core` Profile
@@ -3765,7 +3781,7 @@ A path is written relative to the root of the repository, with the character `/`
 
 The base revision is the revision from which the change started. It is recorded when the change starts: in `core`, when the `start` action succeeds (Section 23.4); in `full`, when the first phase of the change begins. A change MUST NOT start when its base revision cannot be recorded: the start is rejected, and nothing is written. See AE-153.
 
-The paths changed since the base revision are the paths whose content differs from the base revision according to version control, whether the difference is committed, staged, or unstaged, and the files that version control does not track and has not been told to ignore. A path changed since the base revision that no pattern of the allowed path list matches is a scope violation. A scope violation is a hard failure (Section 24.7): the change is closed as failed without human action, and the record names the paths outside the scope. See AE-147, AE-148, AE-149.
+The paths changed since the base revision are the paths whose content differs from the base revision according to version control, whether the difference is committed, staged, or unstaged, and the files that version control does not track and that no ignore file inside the repository tells it to ignore. A path changed since the base revision that no pattern of the allowed path list matches is a scope violation. A scope violation is a hard failure (Section 24.7): the change is closed as failed without human action, and the record names the paths outside the scope. See AE-147, AE-148, AE-149.
 
 The record files of the change itself are exempt from the measurement. In `core` they are the change definition, the specification, and the state document (Section 23.1). In `full` they are the specification and the state file or inline record of the change (Sections 16.1 and 4.3). Other means detect their alteration: the hash of the gate definitions (Section 24.1), the approval of the specification (Section 24.3), and the chain of the history (Section 24.4). In both method profiles, exactly two further names in the change directory are exempt: the in-progress file `state.json.tmp` and the lock object `state.json.lock` that the writer of the state document uses (Section 25.1), so that a file left behind by an interrupted write is never a scope violation. Every other file in the change directory is measured, including a file with a similar name such as `state.json.bak`. See AE-155, AE-282.
 
@@ -3773,7 +3789,7 @@ In `core`, before the change has started there is no base revision, and the scop
 
 An allowed path list that is present and empty allows no path: every path changed since the base revision is a scope violation. When no path has changed, the change is in scope, whatever the list holds. See AE-151.
 
-A file that version control is told to ignore is invisible to the measurement. A change can create or alter an ignored file without a scope violation, so the allowed path list does not limit what happens in ignored locations. The consequence for the code that gate commands run is stated in Section 24.10. See AE-150.
+A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement. A change can create or alter such an ignored file without a scope violation, so the allowed path list does not limit what happens in ignored locations. Only ignore files inside the repository count. An ignore file is an ordinary file of the working tree, such as a `.gitignore` file, so that creating or changing one is a changed path, and it is a scope violation when no pattern of the allowed path list matches it. An ignore setting kept anywhere else, such as the exclude file in the metadata directory of version control or an excludes file of the user, is not applied: a file that only such a setting hides is counted like any other file that version control does not track. The consequence for the code that gate commands run is stated in Section 24.10. See AE-150, AE-307.
 
 Work that is uncommitted when the change starts and that does not belong to the change is a changed path like any other. The measurement counts it, and it is a scope violation when no pattern matches it. A change therefore MUST run isolated: in a working copy that is separate from other work and whose content at the start equals the base revision, apart from the record files of the change. An implementation SHOULD warn when it finds other uncommitted work at the start, and it MUST NOT exclude that work from the measurement. See AE-152.
 
@@ -3805,10 +3821,18 @@ Then `tools/run.sh` is a changed path outside the scope, and the change is close
 
 - Covers: Section 24.5
 
-Given an `active` `core` change whose `scope.allow` is `lib/**`, a directory `.cache/` that version control is told to ignore, and a new file `.cache/tool.py` created by the change  
+Given an `active` `core` change whose `scope.allow` is `lib/**`, a directory `.cache/` that an ignore file inside the repository, in place at the base revision, tells version control to ignore, and a new file `.cache/tool.py` created by the change  
 When the `close` action evaluates the gates  
 Then `.cache/tool.py` is not seen by the measurement, and no scope violation is found
 
+**AE-307 — An ignore setting kept outside the repository is not applied, and an ignore file inside it is a changed path**
+
+- Covers: Section 24.5
+
+Given an `active` `core` change whose `scope.allow` is `lib/**`, an excludes file of the user that lists `tools/`, and the new files `tools/run.sh` and `.gitignore`, where `.gitignore` is an ignore file inside the repository that lists `build/`  
+When the `close` action evaluates the gates  
+Then the excludes file of the user is not applied, `tools/run.sh` is counted, `.gitignore` is a changed path, both paths are outside the scope, and the change is closed as failed
+
 **AE-151 — An empty allowed path list allows no path**
 
 - Covers: Section 24.5
@@ -3971,14 +3995,14 @@ Then the result is `rejected` with the issue code `gates-changed`, and the basel
 
 Every fail condition has a severity, which is `hard` or `soft`, written in exact lowercase. A fail condition without a severity, or with any other value, is invalid and MUST be rejected when the gate definitions are approved. In `core`, the severity is the field `severity` of a fail gate (Section 23.3). In `full`, every fail rule states its severity (Section 12.2). A retry limit (Section 24.2) is a fail condition of the severity `soft`, and a retry limit that declares the severity `hard` is invalid and MUST be rejected. See AE-97, AE-108, AE-110.
 
-A hard failure ends the change as failed without any human action. When an action that evaluates gates finds a fail condition of the severity `hard` active, the action MUST close the change as failed in the same state mutation: in `core`, the state `closed` with the outcome `failed`; in `full`, the `closed` phase with the status `failed`. This decision comes before every other decision of Section 24.2, and the action that makes it answers `success`. An active hard failure also turns `cancel` and `supersede` into a close as failed (Sections 8.4 and 23.4). The action `start` is the exception: it never closes a change. When a fail gate of the severity `hard` is active, `start` is rejected with `changed` false and the issue code `start-blocked` (Section 24.2), and the change keeps its state. The failure is decided by `cancel`, by `supersede`, or by the first action that completes or resumes the change. See AE-98, AE-279.
+A hard failure ends the change as failed without any human action. When an action that evaluates gates finds a fail condition of the severity `hard` active, the action MUST close the change as failed in the same state mutation: in `core`, the state `closed` with the outcome `failed`; in `full`, the `closed` phase with the status `failed`. This decision comes before every other decision of Section 24.2, and the action that makes it answers `success`. An active hard failure also turns `cancel` and `supersede` into a close as failed (Sections 8.4 and 23.4). The action `start` is an exception: it never closes a change. When a fail gate of the severity `hard` is active, `start` is rejected with `changed` false and the issue code `start-blocked` (Section 24.2), and the change keeps its state. The action `fail` is a second exception: it is valid only while a soft failure awaits disposition, so that with only a fail condition of the severity `hard` active it is rejected with `changed` false (Sections 8.3 and 23.4), and the change keeps its state. The failure is decided by `cancel`, by `supersede`, or by the first action that completes or resumes the change. See AE-98, AE-279.
 
 A soft failure pauses the change for a human. When an action that evaluates gates finds a fail condition of the severity `soft` active and no hard failure, the action MUST NOT close the change. The change waits: in `core`, in the state `waiting` with a wait record of kind `fail-gate` (Section 23.5); in `full`, with the status `waiting` and a wait state of the category `WAIT_DECISION` (Section 11.1), whose resume condition is that a human has recorded an override. The wait ends by a human disposition (Section 24.3), which is one of two:
 
 - the human closes the change as failed with the `fail` action and a reason (Sections 8.3 and 23.4);
 - the human records an override of the soft failure.
 
-The `fail` action is valid only while a soft failure awaits disposition. See AE-99, AE-100, AE-101.
+The `fail` action is valid only while a soft failure awaits disposition. See AE-99, AE-100, AE-101, AE-308.
 
 When a retry limit is reached, the change waits as it does for a soft failure, and the human closes the change as failed or records an override. Nothing ends the change automatically.
 
@@ -4328,7 +4352,7 @@ The interpreter that the project configuration names is not part of the gate def
 
 An implementation SHOULD warn when the interpreter that the token stands for lives inside the repository of the project. See AE-161.
 
-Code in a location that version control is told to ignore is invisible to the scope check (Section 24.5). When a command runs code from such a location, including an interpreter or a library that is installed there, a change can alter that code, and so the result of the gate, without a scope violation. The scope check therefore does not show that the code behind a gate is unchanged, and the result of a gate is worth only as much as the protection of the code that its command runs. See AE-162.
+Code in a location that an ignore file inside the repository tells version control to ignore is invisible to the scope check (Section 24.5). When a command runs code from such a location, including an interpreter or a library that is installed there, a change can alter that code, and so the result of the gate, without a scope violation. The scope check therefore does not show that the code behind a gate is unchanged, and the result of a gate is worth only as much as the protection of the code that its command runs. See AE-162.
 
 **AE-158 — Shell syntax has no effect**
 
@@ -4366,7 +4390,7 @@ Then the configured interpreter is used, and an implementation that follows this
 
 - Covers: Section 24.10
 
-Given a check-command gate whose command runs the script `.cache/gate.script`, a location that version control is told to ignore, and a change whose `scope.allow` is `lib/**` that edits the script so that it always ends with the exit status that the exit map maps to `satisfied`  
+Given a check-command gate whose command runs the script `.cache/gate.script`, a location that an ignore file inside the repository, in place at the base revision, tells version control to ignore, and a change whose `scope.allow` is `lib/**` that edits the script so that it always ends with the exit status that the exit map maps to `satisfied`  
 When the gate is evaluated  
 Then the gate is `satisfied`, and the scope check finds no violation, because the edited script is invisible to it
 
```

## Questions

### Q01 — Approval

- Question: Do you approve the new text exactly as it now stands (fingerprint a81d9c89651f, 4794 lines), or do you want changes?
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
