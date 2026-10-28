# Owner approval packet, fix round 5: proposed normative method specification

- Owner approval: pending

## What you are asked

On 2026-10-28 the owner approved the text of the specification. The independent reviewer then looked at it a fourth time; the owner asked for the finding that the reviewer rated BLOCKING, its strongest rating, to be fixed, and answered the related findings that the disposition addendum records, each with the word the owner gave (RF-B-001: fix, RF-B-004: fix, RF-C-001: fix, RF-C-002: fix, RF-X-002: fix, RF-X-003: fix, RF-X-004: fix). Where a change is of the kind owner decision the owner chose how. Where a change is of the kind repair the finding itself names the fix. The text has been changed in seven places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.

## The changes

| # | What changed | Why | Whose reading |
|---|---|---|---|
| 1 | Two new examples show the rules of the minimum templates: how a change specification states its gate conditions, allowed paths and evidence commands, and how the evidence lists a gate that could not be evaluated. The plan and tasks templates hold no rule sentence and got none. | The owner dispositioned the finding fix and chose to add examples for the rules of these templates, which had none. | your decision: Add examples |
| 2 | Three new examples show the rules on a conflict with an accepted ADR, on a deviation of the implementation or the tests from the specification, and on breaking changes. Each rule now points to its example. | The owner dispositioned the finding fix and chose to add examples for these rules, which had none. | your decision: Add examples |
| 3 | Three new examples show the rules on a review cycle that returns a blocking finding, on a blocking finding that blocks a gate until it is dispositioned, and on the evidence record of a review. Each rule now points to its example. | The owner dispositioned the finding fix and chose to add examples for these rules, which had none. | your decision: Add examples |
| 4 | One new example shows the prohibitions on an AI agent together: an agent that meets a gap does not invent, assume or speculate, does not hide an error, and does not work beyond the approved scope. The list now points to it. | The owner dispositioned the finding fix and chose to add an example for these prohibitions, which had none. | your decision: Add examples |
| 5 | The first sentence of the evaluation order now says that the evaluation stops once the results of a group decide the requested action, which is what the later sentences on groups already said. | The reviewer says the two stop rules of the section read differently, and the owner dispositioned the finding fix. | no decision asked: the finding names the fix |
| 6 | The section on conditions now says that the identifier named by a retry limit must be the identifier of a check done gate of the same change, and that a definition naming none is rejected. A new example shows the rejection. | The reviewer says no rule required the named gate to exist in the same change, and the owner dispositioned the finding fix. | no decision asked: the finding names the fix |
| 7 | The clause that cited the earlier text of the method was removed from the sentence on a retry limit. The rest of the sentence is unchanged. | The reviewer says the clause cites a document outside the specification, and the owner dispositioned the finding fix. | no decision asked: the finding names the fix |

## Before and after

### Change 1 of 7: Rules of the full-only templates that have no acceptance example

- Findings: RF-X-001, RF-B-004
- Options offered: Add examples | Say none needed
- Your decision: Add examples; reason: none given
- Before: none (new text)
- After: "the other three lists are empty because the marker `<optional>` is not a condition, the allowed path list is `lib/**`"

### Change 2 of 7: Rules on ADR conflicts, drift and breaking changes that have no acceptance example

- Findings: RF-X-002
- Options offered: Add examples | Say none needed
- Your decision: Add examples; reason: none given
- Before: none (new text)
- After: "stops planning or implementation, returns R2 to the requestor, and requests a decision"

### Change 3 of 7: Rules on the review cycle and its artifacts that have no acceptance example

- Findings: RF-X-003
- Options offered: Add examples | Say none needed
- Your decision: Add examples; reason: none given
- Before: none (new text)
- After: "the finding is returned to the Requestor, the disposition of the Requestor and the changes made are recorded"

### Change 4 of 7: Prohibitions on an AI agent that have no acceptance example

- Findings: RF-X-004
- Options offered: Add examples | Say none needed
- Your decision: Add examples; reason: none given
- Before: none (new text)
- After: "does not read the missing answer as consent, does not silently modify the approved specification"

### Change 5 of 7: How the evaluation of a core change stops

- Findings: RF-C-001
- Your decision: none asked; the finding leaves no design choice
- Before: "and the evaluation MUST stop as soon as a gate decides the requested action:"
- After: "and the evaluation MUST stop once the results of a group decide the requested action (Section 24.2):"

### Change 6 of 7: A retry limit that names a check gate which does not exist

- Findings: RF-C-002
- Your decision: none asked; the finding leaves no design choice
- Before: none (new text)
- After: "The identifier named by `gate` MUST be the identifier of a done gate of the kind `check` of the same change, and a definition whose retry limit names none is rejected."

### Change 7 of 7: A sentence that cites the earlier text of the method

- Findings: RF-B-001
- Your decision: none asked; the finding leaves no design choice
- Before: "does not end it by itself, as the earlier text of this method did."
- After: "does not end it by itself."

## The text under approval

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `3c0f689e2464b3a9fc8fcce5c1fc7ef55e06bfd1` |
| Reviewed SHA-256 | `09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704` |
| Line count | `4898` |
| Diffstat | `1 file changed, 3529 insertions(+), 53 deletions(-)` |
| Commits touching the file | `59` |
| Previously approved blob and SHA-256 | `fca228479a34e228785f4c0b100da3c6745ada0a` and `5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1` |
| Register file | `.planning/reviews/2026-10-28-normative-spec-fix-round-5-register.md` |
| Register blob | `fbae15eec645ff447818d87c19e25f28b013ccfe` |
| Disposition addendum file | `.planning/reviews/2026-10-28-normative-spec-review-disposition-addendum-round-4.md` |
| Disposition addendum blob | `26bbd45378694e7971253a4a89e90ac239adb69b` |

## The exact change

The change from the text approved in round 4 has 12 hunks, adds 96 lines and removes 10 lines.

````
@@ -1492,7 +1492,7 @@ The obligation to terminate applies to a fail condition of the severity `hard`.
 
 A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition, and the human closes the change as failed or records an override (Section 24.7).
 
-The obligation to terminate of this section does not cover a retry limit: reaching one pauses the flow for a human disposition and does not end it by itself, as the earlier text of this method did.
+The obligation to terminate of this section does not cover a retry limit: reaching one pauses the flow for a human disposition and does not end it by itself.
 
 ### 12.1 Typical Fail Categories
 
@@ -1575,7 +1575,15 @@ When a requirement conflicts with an ADR, the agent MUST:
 4. request a decision,
 5. communicate and reference the decision.
 
-An existing ADR MUST only be changed or replaced through an explicitly approved change flow.
+An existing ADR MUST only be changed or replaced through an explicitly approved change flow. See AE-313.
+
+**AE-313 — An agent stops on a conflict with an accepted ADR and returns the requirement**
+
+- Covers: Section 13.1
+
+Given an `active` change whose requirement R2 states that jobs are kept in a message queue, and an accepted ADR that fixes a database table as the place where jobs are kept  
+When the agent finds that R2 conflicts with the ADR  
+Then the agent documents the conflict in the requirement or the specification, stops planning or implementation, returns R2 to the requestor, and requests a decision, it communicates and references the decision once it is made, and the ADR is neither changed nor replaced except through an explicitly approved change flow
 
 ### 13.2 Specification Drift
 
@@ -1586,9 +1594,27 @@ When implementation or tests deviate from the specification, one of the followin
 - document the deviation as an accepted exception,
 - stop the flow if the deviation is not permitted.
 
+See AE-314.
+
+**AE-314 — A deviation from the specification leads to one of the actions of Section 13.2**
+
+- Covers: Section 13.2
+
+Given two `active` changes whose tests deviate from the approved specification, where a human decides in the first change that the specification is to change, and the deviation in the second change is not permitted  
+When the deviation is found in each change  
+Then the specification of the first change is changed and reapproved before the work continues, and the flow of the second change is stopped, and neither change continues with the deviation left as it is
+
 ### 13.3 Breaking Changes
 
-Breaking changes MUST be explicitly marked, assessed, and approved. Without approval, the corresponding DoF rule applies.
+Breaking changes MUST be explicitly marked, assessed, and approved. Without approval, the corresponding DoF rule applies. See AE-315.
+
+**AE-315 — A breaking change without approval triggers the corresponding fail rule**
+
+- Covers: Section 13.3
+
+Given two changes that each remove a field that clients of an interface use, where the first change marks the removal as a breaking change, assesses it, and has it approved, and the second change marks and assesses it and has no approval, and a fail rule whose trigger is that a breaking change is required but has not been approved (the template F-01 of Section 12.2)  
+When each change implements the removal  
+Then the fail rule does not apply to the first change, and it applies to the second change, which is stopped and closed as failed
 
 ---
 
@@ -1636,6 +1662,16 @@ A Pair Review cycle MUST:
 7. verify resolved blocking findings when required,
 8. preserve the final review result as evidence.
 
+See AE-316.
+
+**AE-316 — A Pair Review cycle returns a blocking finding to the Requestor and records the disposition**
+
+- Covers: Section 14.3
+
+Given a change with a required Pair Review whose Requestor is the participant `agent-a` and whose Reviewer is the distinct participant `reviewer-b`, the review scope `spec.md` with the criterion that every requirement is verifiable, the reviewed work product fixed as the exact revision `r12`, a rule of the project that resolved blocking findings are verified, and one finding of the severity `blocking` that the Reviewer records with the status `open`  
+When the review cycle runs  
+Then the finding is returned to the Requestor, the disposition of the Requestor and the changes made are recorded, the Reviewer verifies that the blocking finding is resolved, and the final review result is preserved as evidence
+
 ### 14.4 Findings
 
 A finding SHOULD include:
@@ -1654,7 +1690,15 @@ Recommended severities are `informational`, `minor`, `major`, `blocking`, and `c
 
 Recommended statuses are `open`, `accepted`, `rejected`, `resolved`, `verified`, and `withdrawn`.
 
-Unresolved blocking findings MUST block the applicable completion or transition gate unless they are formally dispositioned by an authorized decision owner.
+Unresolved blocking findings MUST block the applicable completion or transition gate unless they are formally dispositioned by an authorized decision owner. See AE-317.
+
+**AE-317 — An unresolved blocking finding blocks the gate until it is formally dispositioned**
+
+- Covers: Section 14.4
+
+Given two changes with a Pair Review whose finding `F-1` has the severity `blocking`, where `F-1` has the status `open` in the first change, and `F-1` has the status `accepted` in the second change with a disposition rationale that an authorized decision owner recorded  
+When the completion of each change is requested  
+Then the unresolved blocking finding blocks the completion of the first change, and the finding of the second change does not block it, because an authorized decision owner formally dispositioned it
 
 ### 14.5 Review Artifacts
 
@@ -1662,7 +1706,15 @@ Pair Review evidence MAY be recorded inline in `evidence.md`. A separate `review
 
 Review findings are not requirements and do not override higher-ranking artifacts. A finding that requires a requirement or architecture change MUST trigger the appropriate specification or ADR workflow.
 
-Regardless of whether it is stored inline in `evidence.md` or separately in `review.md`, a portable Pair Review evidence record MUST capture exactly these eight fields: participant; role (`Requestor` or `Reviewer`); reviewed revision (the exact artifact revision reviewed); action (the review action taken); timestamp; result; findings (a reference to or summary of the findings); and disposition. This evidence-record field set is distinct from, and complements, the per-finding fields in Section 14.4.
+Regardless of whether it is stored inline in `evidence.md` or separately in `review.md`, a portable Pair Review evidence record MUST capture exactly these eight fields: participant; role (`Requestor` or `Reviewer`); reviewed revision (the exact artifact revision reviewed); action (the review action taken); timestamp; result; findings (a reference to or summary of the findings); and disposition. This evidence-record field set is distinct from, and complements, the per-finding fields in Section 14.4. See AE-318.
+
+**AE-318 — A review finding does not override a requirement, and the evidence record holds eight fields**
+
+- Covers: Section 14.5
+
+Given a Pair Review recorded inline in `evidence.md`, in which the finding of the Reviewer says that requirement R3 of the approved specification is to change  
+When the Requestor handles the finding  
+Then requirement R3 is not changed by the finding, the specification workflow is triggered to change it, and the evidence record of the review holds exactly the eight fields participant, role, reviewed revision, action, timestamp, result, findings, and disposition
 
 ## 15. Evidence Model
 
@@ -1831,12 +1883,20 @@ The conditions listed under Flow Gates, together with the scope, are the gate de
 
 The Change ID follows the syntax of the identifier of a change in Section 4.3.
 
-The list under the heading Allowed Paths of the Scope is the allowed path list of the change. It holds path patterns that can be checked by machine, and Section 24.5 states how they are written and measured. The Included and Excluded lists describe the scope in words and are not measured.
+The list under the heading Allowed Paths of the Scope is the allowed path list of the change. It holds path patterns that can be checked by machine, and Section 24.5 states how they are written and measured. The Included and Excluded lists describe the scope in words and are not measured. See AE-311.
 
 The list under the heading Evidence Commands of a requirement holds the evidence commands that are bound to it as Section 24.9 states. Each list item states the argument list, the exit map, and optionally the time limit of one command. The requirement identifiers and these lists are fixed with the gate definitions (Section 24.1), and a requirement without a list item has no evidence command.
 
 The section Open Questions of the change specification is a view of the questions that are recorded as state (Section 24.8).
 
+**AE-311 — Full: a change specification states its gate conditions, its allowed paths, and its evidence commands under fixed headings**
+
+- Covers: Section 16.1
+
+Given a `full` change specification whose Additional Done Conditions list holds the one item `run-tests --suite unit`, whose Additional Ready Conditions, Additional Wait Conditions, and Additional Fail Conditions lists hold only the marker `<optional>`, whose Allowed Paths list holds `lib/**` and whose Excluded list holds the item `the build scripts`, and whose requirement R1 holds the item `run-tests --suite unit` with the exit map `0` to `satisfied` under the heading Evidence Commands  
+When the gate definitions of the change are read from the specification  
+Then the Done conditions are the one condition `run-tests --suite unit`, the other three lists are empty because the marker `<optional>` is not a condition, the allowed path list is `lib/**`, the Excluded list is not measured, and the evidence commands of R1 are the one item under its heading
+
 ### 16.2 `plan.md`
 
 ```markdown
@@ -1943,9 +2003,17 @@ The section Open Questions of the change specification is a view of the question
 <status>
 ```
 
-A gate that could not be evaluated is not recorded as Yes or No in the Final Gate Evaluation. It is listed by name with its cause (Section 24.2).
+A gate that could not be evaluated is not recorded as Yes or No in the Final Gate Evaluation. It is listed by name with its cause (Section 24.2). See AE-312.
+
+The Evidence column of the requirement coverage table points at the evidence commands that stand under the heading Evidence Commands of the requirement in the change specification (Sections 16.1 and 24.9) and records what they produced. Other records MAY be added to it. See AE-312.
+
+**AE-312 — Full: the evidence lists a gate that could not be evaluated, and the coverage table names the evidence commands**
+
+- Covers: Section 16.4
 
-The Evidence column of the requirement coverage table points at the evidence commands that stand under the heading Evidence Commands of the requirement in the change specification (Sections 16.1 and 24.9) and records what they produced. Other records MAY be added to it.
+Given a `full` change in the verify phase whose Definition of Done holds the condition `run-tests --suite unit`, which could not be evaluated because its program is missing, and whose requirement R1 has the evidence command `check-docs --strict` under its heading Evidence Commands, which ran  
+When the evidence of the change is written  
+Then the line Gates that could not be evaluated of the Final Gate Evaluation names `run-tests --suite unit` with the cause that its program is missing, the condition is not recorded as Yes or No, and the Evidence cell of R1 in the requirement coverage table points at the evidence command `check-docs --strict` and records what it produced
 
 ### 16.5 `project-brief.md`
 
@@ -2141,6 +2209,16 @@ An AI agent MUST NOT:
 - conceal errors or reinterpret them as successful deviations,
 - work beyond the approved scope.
 
+See AE-319.
+
+**AE-319 — An agent that meets a gap does not fill it by invention, silence, or speculation**
+
+- Covers: Section 19.1
+
+Given an `active` change with the approved scope `lib/**`, a requirement R2 whose approval is missing, an open question whether an export format is wanted that nobody has answered, the planned removal of a field that clients of an interface use, which no one approved, an implementation of R2 that fails its evidence command with an error, and a needed edit of the approved specification of the change and of the file `docs/guide.md`  
+When the agent works on the change  
+Then the agent does not invent the approval of R2 or a requirement for the export format, does not read the missing answer as consent, does not silently modify the approved specification, does not implement the removal of the field, does not bypass the wait through speculation, does not mark the flow as done while the evidence of R2 is missing, records the error as an error and not as a successful deviation, and does not edit `docs/guide.md`, which lies outside the approved scope
+
 ---
 
 ## 20. Completion Criteria for a Change
@@ -2487,7 +2565,7 @@ There is no ready gate. Readiness to start is a precondition of the `start` acti
 A fail gate and a wait gate have no kind. Each has a `condition`, a mapping that holds exactly one of the members `command`, `retry_limit`, and `predicate`:
 
 - `command`: the argument list of a check command (Section 24.2). The condition also holds the member `exit_map`, and it MAY hold the member `time_limit`. The gate is active when the command ends with an exit status that the exit map maps to `satisfied`.
-- `retry_limit`: a mapping with the members `gate` and `limit`, for a fail gate only. The member `gate` is the identifier of a done gate of the kind `check`, and the member `limit` is the limit of Section 24.2. The gate is active when the retry limit is reached.
+- `retry_limit`: a mapping with the members `gate` and `limit`, for a fail gate only. The member `gate` is the identifier of a done gate of the kind `check`, and the member `limit` is the limit of Section 24.2. The gate is active when the retry limit is reached. The identifier named by `gate` MUST be the identifier of a done gate of the kind `check` of the same change, and a definition whose retry limit names none is rejected. See AE-320.
 - `predicate`: the name of a built-in predicate. A fail gate MAY name `scope-violation`, and a wait gate MAY name `unanswered-question` or `stale-spec-approval`. Section 23.7 defines them.
 
 A condition that holds none of these members, that holds two or more of them, that holds another member, or that names a predicate which is not listed for the kind of the gate MUST be rejected. The rules about the kind of a gate apply to done gates only. See AE-273.
@@ -2520,6 +2598,14 @@ Given a change definition with the hard fail gate `no-secrets` whose condition i
 When the `new` action receives each of them
 Then the first definition is accepted, and the second and the third are rejected, because a condition has exactly one form, and no change is created for them
 
+**AE-320 — A retry limit names a check done gate of the same change**
+
+- Covers: Section 23.3
+
+Given a change definition with the `check` done gate `tests-pass` and the soft fail gate `flaky` whose condition is a `retry_limit` for `tests-pass`, a second definition with the same done gate and a soft fail gate whose `retry_limit` names `tests-pas`, an identifier that no gate of the change carries, and a third definition whose `retry_limit` names the `sign-off` done gate `legal-ok`  
+When the `new` action receives each of them  
+Then the first definition is accepted, and the second and the third are rejected, because the identifier named by `gate` is not that of a done gate of the kind `check` of the same change, and no change is created for them
+
 **AE-16 — Reject a duplicate gate identifier**
 
 - Covers: Section 23.3
@@ -2981,7 +3067,7 @@ Then the category is `WAIT_DECISION`
 
 ### 23.6 Evaluation Order
 
-The gates of a `core` change MUST be evaluated in this order, and the evaluation MUST stop as soon as a gate decides the requested action:
+The gates of a `core` change MUST be evaluated in this order, and the evaluation MUST stop once the results of a group decide the requested action (Section 24.2):
 
 1. A fail gate with the severity `hard` that is active decides: the change becomes `closed` with the outcome `failed`.
 2. A gate whose condition could not be evaluated decides: the change becomes `waiting` with a wait record of kind `external` (Section 24.2). A condition that could not be evaluated is never a failure.
````

## Questions

### Q01 — Approval

- Question: Do you approve the new text exactly as it now stands (fingerprint 3c0f689e2464, 4898 lines), or do you want changes?
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
