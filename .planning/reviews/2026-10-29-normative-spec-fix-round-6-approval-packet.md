# Owner approval packet, fix round 6: proposed normative method specification

- Owner approval: recorded in the owner approval record

## What you are asked

On 2026-10-28 the owner approved the text of the specification. The independent reviewer then looked at it a fifth time; the owner asked for the finding that the reviewer rated BLOCKING, its strongest rating, to be fixed, and answered the related findings that the disposition addendum records, each with the word the owner gave (RG-C-001: fix, RG-X-001: fix, RG-X-004: fix). Where a change is of the kind owner decision the owner chose how. Where a change is of the kind repair the finding itself names the fix. The text has been changed in three places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.

## The changes

| # | What changed | Why | Whose reading |
|---|---|---|---|
| 1 | The rule on reserved device names now tests the part of the identifier before its first dot, so that `nul.txt` and `COM3.log` are rejected like `nul`. A new example shows both the rejected and the accepted identifiers. | The reviewer says the old test compared the whole identifier, and the owner dispositioned both findings fix. | no decision asked: the finding names the fix |
| 2 | A supersede action now refuses a replacement that is already closed. The condition of the action and the list of rejections say so, and a new example shows the refusal. | The reviewer says a change could be superseded into a dead end, and the owner dispositioned the finding fix and chose the way. | your decision: Not closed |
| 3 | The section on the base gates now says openly that the specification file is protected against later edits only after it was approved, and that before that only the change definition file is a machine-checkable anchor. A new example shows an edit that is not reported. | The reviewer says an edit of an unapproved specification file goes unnoticed, and the owner dispositioned the finding fix and chose the way. | your decision: Say it openly |

## Before and after

### Change 1 of 3: A reserved device name that is followed by an extension

- Findings: RG-A-001, RG-X-004
- Your decision: none asked; the finding leaves no design choice
- Before: "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."
- After: "The part of the identifier before its first dot, which is the whole identifier when it holds no dot, MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."

### Change 2 of 3: Which change a supersede action may name as its replacement

- Findings: RG-C-001
- Options offered: Not closed | Not closed, or done
- Your decision: Not closed; reason: none given
- Before: "and `replaced_by` names a different change that exists."
- After: "and `replaced_by` names a different change that exists and is not `closed`."

### Change 3 of 3: A specification file that nothing protects when its approval is never required

- Findings: RG-X-001
- Options offered: Record its hash | Always approve it | Say it openly
- Your decision: Say it openly; reason: none given
- Before: none (new text)
- After: "before its first approval, an edit of `spec.md` is not reported as a difference from an approved version, and `change.yaml` is the only machine-checkable anchor of the change. See AE-323."

## The text under approval

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `2acdd0b38174b6fd8e8e3df9952063c74071c22a` |
| Reviewed SHA-256 | `177bc9836133127936c19af9c4f60d076c327bd1743b67e1a875c89c5afb669e` |
| Line count | `4924` |
| Diffstat | `1 file changed, 3552 insertions(+), 50 deletions(-)` |
| Commits touching the file | `62` |
| Previously approved blob and SHA-256 | `3c0f689e2464b3a9fc8fcce5c1fc7ef55e06bfd1` and `09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704` |
| Register file | `.planning/reviews/2026-10-29-normative-spec-fix-round-6-register.md` |
| Register blob | `a45389641f3ec3e2e8e7bf671509e322f6d93490` |
| Disposition addendum file | `.planning/reviews/2026-10-29-normative-spec-review-disposition-addendum-round-5.md` |
| Disposition addendum blob | `1df2a0469d155b4197eb9e091c470d74f520e8b9` |

## The exact change

The change from the text approved in round 5 has 7 hunks, adds 29 lines and removes 3 lines.

```
@@ -300,7 +300,7 @@ specs/<change-id>/
 
 `spec.md` remains the mandatory file for normal (Class M and Class L) changes as defined in Section 6.
 
-The identifier of a change, which is the `id` of a `core` change definition (Section 23.1) and the Change ID of a `full` change specification (Section 16.1), names the directory `specs/<change-id>/` of the change. The whole identifier MUST match `[A-Za-z0-9][A-Za-z0-9._-]*`, so that it holds no path separator. It MUST NOT end with the character `.`. It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case. Two identifiers that are equal after that folding name the same directory on a file system that ignores letter case, so an identifier MUST also be unique among the changes of the project after the folding: an identifier that differs from the identifier of an existing change only in the case of ASCII letters is not unique. The same syntax applies to the values of `follows` and `replaced_by`, which name a change by its identifier. A definition with an identifier that does not follow these rules is rejected, and nothing is written. See AE-288.
+The identifier of a change, which is the `id` of a `core` change definition (Section 23.1) and the Change ID of a `full` change specification (Section 16.1), names the directory `specs/<change-id>/` of the change. The whole identifier MUST match `[A-Za-z0-9][A-Za-z0-9._-]*`, so that it holds no path separator. It MUST NOT end with the character `.`. The part of the identifier before its first dot, which is the whole identifier when it holds no dot, MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case. Two identifiers that are equal after that folding name the same directory on a file system that ignores letter case, so an identifier MUST also be unique among the changes of the project after the folding: an identifier that differs from the identifier of an existing change only in the case of ASCII letters is not unique. The same syntax applies to the values of `follows` and `replaced_by`, which name a change by its identifier. A definition with an identifier that does not follow these rules is rejected, and nothing is written. See AE-288. See AE-321.
 
 Every change carries mandatory information regardless of file layout: the goal, specification anchor, gate outcome, evidence, wait or fail behavior when applicable, and final status.
 
@@ -330,6 +330,14 @@ Given a project that holds the change `Task-7`, and five change definitions whos
 When the `new` action receives each definition  
 Then the first four are rejected and nothing is written, because `../x` and `a/b` hold a path separator, `task-7` differs from `Task-7` only in letter case, and `nul` is a reserved name, and the definition with the identifier `c-1` is accepted
 
+**AE-321 — A reserved name before the first dot is rejected**
+
+- Covers: Section 4.3
+
+Given a project and four change definitions whose identifiers are `nul.txt`, `COM3.log`, `nul-1`, and `console.txt`  
+When the `new` action receives each definition  
+Then the first two are rejected and nothing is written for them, because the part before the first dot, `nul` and `COM3` (which is `com3` after the folding), is a reserved name, and the definitions with the identifiers `nul-1` and `console.txt` are accepted, because the part before the first dot, `nul-1` and `console`, is not a reserved name
+
 ---
 
 ## 5. Workflow and Compliance Tailoring
@@ -2646,7 +2654,7 @@ A `core` change changes state only through the actions of the table below. An ac
 | `close` | `active` | The evaluation of Section 23.6 finds no fail gate and no wait gate active, and every done gate is satisfied. | The state `closed` with the outcome `done`. When the evaluation finds otherwise, the change does not close: it remains `active` when a wait gate is active or a done gate is not satisfied, becomes `waiting` when Section 23.6 requires a wait, and becomes `closed` with the outcome `failed` when a hard fail condition is active. See AE-37, AE-38. |
 | `fail` | `waiting`, with a wait record of kind `fail-gate` | A soft fail condition awaits disposition (Section 24.7), and a reason text is given. | The state `closed` with the outcome `failed` and the reason recorded. See AE-39, AE-40, AE-41. |
 | `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). A gate that cannot be evaluated determines no failure and does not prevent it (Section 24.2). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active. See AE-42, AE-43. |
-| `supersede` | Any state except `closed` | The preconditions of `cancel` hold, except that differing gate definitions prevent the action (Section 24.1), and `replaced_by` names a different change that exists. | As `cancel`, with `replaced_by` recorded in the closed change. See AE-44, AE-45, AE-309. |
+| `supersede` | Any state except `closed` | The preconditions of `cancel` hold, except that differing gate definitions prevent the action (Section 24.1), and `replaced_by` names a different change that exists and is not `closed`. | As `cancel`, with `replaced_by` recorded in the closed change. See AE-44, AE-45, AE-309, AE-322. |
 | `adopt` | Any state | The history of the change has no anchor (Section 24.4). | The state and the outcome do not change, and the anchor is created from the history as it is. See AE-46, AE-47. |
 
 The actions `approve`, `fail`, `cancel`, `supersede`, and `adopt` MUST be performed by a human participant. An `answer` to a question whose owner is a human MUST also be given by a human (Section 24.3). See AE-24.
@@ -2671,7 +2679,7 @@ A `follows` field is a reference and not a state transition: it never changes th
 | `close` | The state is not `active`. | The evaluation of Section 23.6 finds a wait gate active, a done gate not satisfied, a soft failure, or a gate that cannot be evaluated, so that the change does not close. |
 | `fail` | The state is not `waiting` with a wait record of kind `fail-gate`, or no reason is given. | Never. |
 | `cancel` | The state is `closed`. | Never. |
-| `supersede` | The state is `closed`, or `replaced_by` is missing, names the change itself, or names a change that does not exist, or the gate definitions differ from the approved ones (issue code `gates-changed`, Section 24.1). | Never. |
+| `supersede` | The state is `closed`, or `replaced_by` is missing, names the change itself, or names a change that does not exist, or names a change that is `closed`, or the gate definitions differ from the approved ones (issue code `gates-changed`, Section 24.1). | Never. |
 | `adopt` | The history already has an anchor. | Never. |
 
 A `close` or a `resume` whose evaluation finds a fail gate of the severity `hard` active answers `success` with the state `closed` and the outcome `failed` (Section 24.7). An action answers `blocked` only where this table lists a case. See AE-117, AE-118, AE-119, AE-120.
@@ -2950,6 +2958,14 @@ Given an `active` change A
 When a human performs the `supersede` action on change A and gives no `replaced_by`  
 Then the action is rejected, and change A remains `active`
 
+**AE-322 — Reject supersede with a closed replacement**
+
+- Covers: Section 23.4 (`supersede`)
+
+Given an `active` change A and a `closed` change B  
+When a human performs the `supersede` action on change A with `replaced_by` naming change B  
+Then the result is `rejected` with `changed` false, change A is not closed, and nothing is written to the history
+
 **AE-46 — Adopt an unanchored history**
 
 - Covers: Section 23.4 (`adopt`)
@@ -3116,6 +3132,8 @@ The base gates have the identifiers `scope-violation`, `unanswered-question`, `s
 
 The predicate of a base gate has the identifier of the gate as its name, and the rules of Section 23.3 about the kind and the condition of a gate govern the gates of the change definition and not the base gates. The check of Section 5.3 on the identifiers of the base gates is made before the other checks of Sections 23.1 and 23.3, so that a gate with the identifier of a base gate is rejected as Section 5.3 states, whatever its condition. A specification that was never approved has no approved version from which it can differ, so that the stale specification approval gate is not active for it and does not stop the `start` action. See AE-276.
 
+The specification file `spec.md` of a `core` change is protected against later edits only after it was approved: before its first approval, an edit of `spec.md` is not reported as a difference from an approved version, and `change.yaml` is the only machine-checkable anchor of the change. See AE-323.
+
 **AE-56 — The scope violation gate applies without being listed**
 
 - Covers: Section 23.7
@@ -3148,6 +3166,14 @@ Given an `open` `core` change in a project whose configuration does not require
 When the `start` action is requested, and later a human approves `spec`, `spec.md` is edited, and the `close` action is requested
 Then the `start` action succeeds, because the stale specification approval gate is not active, and the `close` action does not close the change, because the gate is active after the edit
 
+**AE-323 — An edit of a specification that was never approved is not reported**
+
+- Covers: Section 23.7
+
+Given an `active` `core` change in a project whose configuration does not require the approval of the specification, whose `spec.md` was never approved and was edited after the change started, and whose other gates are satisfied  
+When the `close` action is requested  
+Then the change closes, because the stale specification approval gate is not active and the edit of `spec.md` is not reported as a difference from an approved version
+
 ---
 
 ## 24. Protections Shared by Both Profiles
```

## Questions

### Q01 — Approval

- Question: Do you approve the new text exactly as it now stands (fingerprint 2acdd0b38174, 4924 lines), or do you want changes?
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
