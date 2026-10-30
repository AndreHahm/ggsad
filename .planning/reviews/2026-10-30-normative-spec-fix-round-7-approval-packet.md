# Owner approval packet, fix round 7: proposed normative method specification

- Owner approval: recorded in the owner approval record

## What you are asked

On 2026-10-29 the owner approved the text of the specification. The independent reviewer then looked at it a sixth time; the owner asked for the three findings that the reviewer rated BLOCKING, its strongest rating, to be fixed. Where a change is of the kind owner decision the owner chose how. Where a change is of the kind repair the finding itself names the fix. The text has been changed in three places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.

## The changes

| # | What changed | Why | Whose reading |
|---|---|---|---|
| 1 | A cancel or supersede of a core change that waits for a decision on a soft failure now closes it as failed, not as cancelled. The person's reason is used when given, otherwise an automatic text names the soft failure. The full profile is not changed, and the text says that the two differ. | The reviewer says the text let a cancel end such a wait as cancelled, against the rule that the wait ends only by fail or override. The owner dispositioned the finding fix and chose the way. | your decision: Close as failed |
| 2 | The text now says that the first entry of a full change that the new action created is new, and that a state document converted from an older YAML document starts with a migrate entry. A new example shows both. | The reviewer says two sections gave different first entries for a converted full change, and the owner dispositioned the finding fix. | no decision asked: the finding names the fix |
| 3 | Only the ignore files as they were at the base revision now hide a path, so an ignore file that a change creates or alters hides nothing. A new example shows a change that alters the ignore file and then works in the path it now lists. | The reviewer says the text did not fix which version of an ignore file counts, and the owner chose that only the version at the base revision counts. | your decision: Base revision only |

## Before and after

### Change 1 of 3: How cancel and supersede end a change that waits for a decision on a soft failure

- Findings: RH-C-001
- Options offered: Close as failed | Allow cancelled
- Your decision: Close as failed; reason: none given
- Before: "The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active."
- After: "or the outcome `failed` when a hard fail condition is active or when the change awaits the disposition of a soft fail condition, that is, when it is `waiting` with a wait record of kind `fail-gate` (Section 24.7)."

### Change 2 of 3: The first entry of a change that was converted from a YAML state document

- Findings: RH-X-001
- Your decision: none asked; the finding leaves no design choice
- Before: "The first entry of a `full` change is `new`"
- After: "The first entry of a `full` change that the `new` action created is `new` (the first entry of a state document that was converted from a YAML state document is the `migrate` entry of Section 25.3)"

### Change 3 of 3: Which revision of an ignore file the scope measurement applies

- Findings: RH-X-002
- Options offered: Base revision only | Forbid editing it
- Your decision: Base revision only; reason: none given
- Before: "A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement."
- After: "Only ignore files inside the repository count, and only as they were at the base revision: an ignore file that the change creates or alters hides nothing, so a path that only the created or altered ignore file hides is measured like any other path."

## The text under approval

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `bfc0df6f96756c0c162d694067fd363e272d36b7` |
| Reviewed SHA-256 | `044fa076078f0f3794a216bdc96d7d54b0fc632404edbad31e2457fc0e9cc821` |
| Line count | `4950` |
| Diffstat | `1 file changed, 3578 insertions(+), 50 deletions(-)` |
| Commits touching the file | `66` |
| Previously approved blob and SHA-256 | `2acdd0b38174b6fd8e8e3df9952063c74071c22a` and `177bc9836133127936c19af9c4f60d076c327bd1743b67e1a875c89c5afb669e` |
| Register file | `.planning/reviews/2026-10-30-normative-spec-fix-round-7-register.md` |
| Register blob | `6171c29a19b40bffe483d93325a469c6e44798c7` |

## The exact change

The change from the text approved in round 6 has 11 hunks, adds 36 lines and removes 10 lines.

```
@@ -2527,8 +2527,8 @@ A `core` change is always in exactly one of four states:
 A `closed` change has exactly one of three outcomes:
 
 - `done`: the change was completed successfully by the `close` action;
-- `failed`: the change ended unsuccessfully, because a hard fail condition was active or because a human disposed of a soft fail condition with the `fail` action (Section 24.7);
-- `cancelled`: the change was ended by the `cancel` or `supersede` action.
+- `failed`: the change ended unsuccessfully, because a hard fail condition was active or because a human disposed of a soft fail condition with the `fail` action, or with the `cancel` or `supersede` action while the change awaited that disposition (Section 24.7);
+- `cancelled`: the change was ended by the `cancel` or `supersede` action, when no hard fail condition was active and the change did not await the disposition of a soft fail condition (Section 23.4).
 
 The state document records the state in the field `state` and the outcome in the field `outcome` (Section 25.1). An outcome exists only when the state is `closed`; in every other state the outcome is `null`. An outcome of `failed` MUST carry a reason text, which the state document records in the field `reason` of the `after` record (Section 25.1). The final status codes of Section 12.2 apply to `full` only. See AE-14, AE-39, AE-41, AE-284.
 
@@ -2653,7 +2653,7 @@ A `core` change changes state only through the actions of the table below. An ac
 | `resume` | `waiting` | The resume condition of the wait record is satisfied (Section 23.5). | The state `active`, when the evaluation of Section 23.6 finds no gate that decides otherwise. Otherwise the change remains `waiting`, or becomes `closed` with the outcome `failed`, as Section 23.6 decides. See AE-35, AE-36. |
 | `close` | `active` | The evaluation of Section 23.6 finds no fail gate and no wait gate active, and every done gate is satisfied. | The state `closed` with the outcome `done`. When the evaluation finds otherwise, the change does not close: it remains `active` when a wait gate is active or a done gate is not satisfied, becomes `waiting` when Section 23.6 requires a wait, and becomes `closed` with the outcome `failed` when a hard fail condition is active. See AE-37, AE-38. |
 | `fail` | `waiting`, with a wait record of kind `fail-gate` | A soft fail condition awaits disposition (Section 24.7), and a reason text is given. | The state `closed` with the outcome `failed` and the reason recorded. See AE-39, AE-40, AE-41. |
-| `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). A gate that cannot be evaluated determines no failure and does not prevent it (Section 24.2). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active. See AE-42, AE-43. |
+| `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). A gate that cannot be evaluated determines no failure and does not prevent it (Section 24.2). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active or when the change awaits the disposition of a soft fail condition, that is, when it is `waiting` with a wait record of kind `fail-gate` (Section 24.7). The actor MAY give a reason text with the action. When the outcome is `failed` because of a soft fail condition, the reason text of the outcome is the reason that the actor gave or, when the actor gave none, a text that names that soft fail condition (Section 25.1). See AE-42, AE-43, AE-324. |
 | `supersede` | Any state except `closed` | The preconditions of `cancel` hold, except that differing gate definitions prevent the action (Section 24.1), and `replaced_by` names a different change that exists and is not `closed`. | As `cancel`, with `replaced_by` recorded in the closed change. See AE-44, AE-45, AE-309, AE-322. |
 | `adopt` | Any state | The history of the change has no anchor (Section 24.4). | The state and the outcome do not change, and the anchor is created from the history as it is. See AE-46, AE-47. |
 
@@ -2922,7 +2922,7 @@ Then the action is rejected, and the change remains `waiting`
 
 - Covers: Section 23.4 (`cancel`)
 
-Given a `waiting` change  
+Given a `waiting` change with a wait record of kind `manual`  
 When a human performs the `cancel` action  
 Then the state is `closed` and the outcome is `cancelled`, although a wait was active
 
@@ -2934,6 +2934,14 @@ Given an `active` change with a hard fail condition active
 When a human performs the `cancel` action  
 Then the state is `closed` and the outcome is `failed`, not `cancelled`
 
+**AE-324 — Cancel and supersede close a change that waits on a soft failure as failed**
+
+- Covers: Section 23.4 (`cancel` and `supersede`)
+
+Given a `waiting` `core` change A and a second such change C, each with a wait record of kind `fail-gate` for a fail gate of the severity `soft`, and an existing change B that is not `closed`  
+When a human performs the `cancel` action on change A with the reason `no longer needed`, and the `supersede` action on change C with `replaced_by` naming change B and no reason  
+Then change A is `closed` with the outcome `failed` and the reason `no longer needed`, not `cancelled`, and change C is `closed` with the outcome `failed`, `replaced_by` naming change B, and a reason text that names the soft fail condition that awaited disposition
+
 **AE-299 — Cancel proceeds when a fail gate cannot be evaluated**
 
 - Covers: Section 23.4 (`cancel`)
@@ -3911,7 +3919,7 @@ A path is written relative to the root of the repository, with the character `/`
 
 The base revision is the revision from which the change started. It is recorded when the change starts: in `core`, when the `start` action succeeds (Section 23.4); in `full`, when the first phase of the change begins. A change MUST NOT start when its base revision cannot be recorded: the start is rejected, and nothing is written. See AE-153.
 
-The paths changed since the base revision are the paths whose content differs from the base revision according to version control, whether the difference is committed, staged, or unstaged, and the files that version control does not track and that no ignore file inside the repository tells it to ignore. A path changed since the base revision that no pattern of the allowed path list matches is a scope violation. A scope violation is a hard failure (Section 24.7): the change is closed as failed without human action, and the record names the paths outside the scope. See AE-147, AE-148, AE-149.
+The paths changed since the base revision are the paths whose content differs from the base revision according to version control, whether the difference is committed, staged, or unstaged, and the files that version control does not track and that no ignore file inside the repository, as it was at the base revision, tells it to ignore. A path changed since the base revision that no pattern of the allowed path list matches is a scope violation. A scope violation is a hard failure (Section 24.7): the change is closed as failed without human action, and the record names the paths outside the scope. See AE-147, AE-148, AE-149.
 
 The record files of the change itself are exempt from the measurement. In `core` they are the change definition, the specification, and the state document (Section 23.1). In `full` they are the specification and the state file or inline record of the change (Sections 16.1 and 4.3). Other means detect their alteration: the hash of the gate definitions (Section 24.1), the approval of the specification (Section 24.3), and the chain of the history (Section 24.4). In both method profiles, exactly two further names in the change directory are exempt: the in-progress file `state.json.tmp` and the lock object `state.json.lock` that the writer of the state document uses (Section 25.1), so that a file left behind by an interrupted write is never a scope violation. Every other file in the change directory is measured, including a file with a similar name such as `state.json.bak`. See AE-155, AE-282.
 
@@ -3919,7 +3927,7 @@ In `core`, before the change has started there is no base revision, and the scop
 
 An allowed path list that is present and empty allows no path: every path changed since the base revision is a scope violation. When no path has changed, the change is in scope, whatever the list holds. See AE-151.
 
-A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement. A change can create or alter such an ignored file without a scope violation, so the allowed path list does not limit what happens in ignored locations. Only ignore files inside the repository count. An ignore file is an ordinary file of the working tree, such as a `.gitignore` file, so that creating or changing one is a changed path, and it is a scope violation when no pattern of the allowed path list matches it. An ignore setting kept anywhere else, such as the exclude file in the metadata directory of version control or an excludes file of the user, is not applied: a file that only such a setting hides is counted like any other file that version control does not track. The consequence for the code that gate commands run is stated in Section 24.10. See AE-150, AE-307.
+A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement, when that ignore file was in place at the base revision and, as it was then, tells version control to ignore the file. A change can create or alter such an ignored file without a scope violation, so the allowed path list does not limit what happens in ignored locations. Only ignore files inside the repository count, and only as they were at the base revision: an ignore file that the change creates or alters hides nothing, so a path that only the created or altered ignore file hides is measured like any other path. An ignore file is an ordinary file of the working tree, such as a `.gitignore` file, so that creating or changing one is a changed path, and it is a scope violation when no pattern of the allowed path list matches it. An ignore setting kept anywhere else, such as the exclude file in the metadata directory of version control or an excludes file of the user, is not applied: a file that only such a setting hides is counted like any other file that version control does not track. The consequence for the code that gate commands run is stated in Section 24.10. See AE-150, AE-307, AE-326.
 
 Work that is uncommitted when the change starts and that does not belong to the change is a changed path like any other. The measurement counts it, and it is a scope violation when no pattern matches it. A change therefore MUST run isolated: in a working copy that is separate from other work and whose content at the start equals the base revision, apart from the record files of the change. An implementation SHOULD warn when it finds other uncommitted work at the start, and it MUST NOT exclude that work from the measurement. See AE-152.
 
@@ -3963,6 +3971,14 @@ Given an `active` `core` change whose `scope.allow` is `lib/**`, an excludes fil
 When the `close` action evaluates the gates  
 Then the excludes file of the user is not applied, `tools/run.sh` is counted, `.gitignore` is a changed path, both paths are outside the scope, and the change is closed as failed
 
+**AE-326 — An ignore file that the change alters hides nothing**
+
+- Covers: Section 24.5
+
+Given an `active` `core` change whose `scope.allow` is `.gitignore` and `lib/**`, an ignore file `.gitignore` inside the repository that was in place at the base revision and does not list `build/`, and a change that alters `.gitignore` so that it lists `build/` and then creates the file `build/out.bin`  
+When the `close` action evaluates the gates  
+Then `build/out.bin` is counted, because the ignore file as it was at the base revision does not hide it, it is a changed path outside the scope, and the change is closed as failed
+
 **AE-151 — An empty allowed path list allows no path**
 
 - Covers: Section 24.5
@@ -4125,15 +4141,17 @@ Then the result is `rejected` with the issue code `gates-changed`, and the basel
 
 Every fail condition has a severity, which is `hard` or `soft`, written in exact lowercase. A fail condition without a severity, or with any other value, is invalid and MUST be rejected when the gate definitions are approved. In `core`, the severity is the field `severity` of a fail gate (Section 23.3). In `full`, every fail rule states its severity (Section 12.2). A retry limit (Section 24.2) is a fail condition of the severity `soft`, and a retry limit that declares the severity `hard` is invalid and MUST be rejected. See AE-97, AE-108, AE-110.
 
-A hard failure ends the change as failed without any human action. When an action that evaluates gates finds a fail condition of the severity `hard` active, the action MUST close the change as failed in the same state mutation: in `core`, the state `closed` with the outcome `failed`; in `full`, the `closed` phase with the status `failed`. This decision comes before every other decision of Section 24.2, and the action that makes it answers `success`. An active hard failure also turns `cancel` and `supersede` into a close as failed (Sections 8.4 and 23.4). The action `start` is an exception: it never closes a change. When a fail gate of the severity `hard` is active, `start` is rejected with `changed` false and the issue code `start-blocked` (Section 24.2), and the change keeps its state. The action `fail` is a second exception: it is valid only while a soft failure awaits disposition, so that with only a fail condition of the severity `hard` active it is rejected with `changed` false (Sections 8.3 and 23.4), and the change keeps its state. The failure is decided by `cancel`, by `supersede`, or by the first action that completes or resumes the change. See AE-98, AE-279.
+A hard failure ends the change as failed without any human action. When an action that evaluates gates finds a fail condition of the severity `hard` active, the action MUST close the change as failed in the same state mutation: in `core`, the state `closed` with the outcome `failed`; in `full`, the `closed` phase with the status `failed`. This decision comes before every other decision of Section 24.2, and the action that makes it answers `success`. An active hard failure also turns `cancel` and `supersede` into a close as failed (Sections 8.4 and 23.4), and in `core` so does a change that awaits the disposition of a soft failure (see the next paragraphs). The action `start` is an exception: it never closes a change. When a fail gate of the severity `hard` is active, `start` is rejected with `changed` false and the issue code `start-blocked` (Section 24.2), and the change keeps its state. The action `fail` is a second exception: it is valid only while a soft failure awaits disposition, so that with only a fail condition of the severity `hard` active it is rejected with `changed` false (Sections 8.3 and 23.4), and the change keeps its state. The failure is decided by `cancel`, by `supersede`, or by the first action that completes or resumes the change. See AE-98, AE-279.
 
 A soft failure pauses the change for a human. When an action that evaluates gates finds a fail condition of the severity `soft` active and no hard failure, the action MUST NOT close the change. The change waits: in `core`, in the state `waiting` with a wait record of kind `fail-gate` (Section 23.5); in `full`, with the status `waiting` and a wait state of the category `WAIT_DECISION` (Section 11.1), whose resume condition is that a human has recorded an override. The wait ends by a human disposition (Section 24.3), which is one of two:
 
-- the human closes the change as failed with the `fail` action and a reason (Sections 8.3 and 23.4);
+- the human closes the change as failed, with the `fail` action and a reason (Sections 8.3 and 23.4) or, in `core`, with the `cancel` or `supersede` action (Section 23.4);
 - the human records an override of the soft failure.
 
 The `fail` action is valid only while a soft failure awaits disposition. See AE-99, AE-100, AE-101, AE-308.
 
+In `core`, a `cancel` or `supersede` of a change that is `waiting` with a wait record of kind `fail-gate` therefore closes the change as failed and not as cancelled, in the same way as an active hard failure does. The reason text of the outcome is the reason that the actor gave with the action or, when the actor gave none, a text that names the soft fail condition that awaited disposition (Section 25.1). In `full`, `cancel` and `supersede` do not do this: a `full` change that waits for a decision on a soft failure ends with the status `cancelled` or `superseded` (Section 8.4), so the two method profiles differ here. See AE-324.
+
 When a retry limit is reached, the change waits as it does for a soft failure, and the human closes the change as failed or records an override. Nothing ends the change automatically.
 
 An override is recorded by a human as an approval with the target `override` (Section 23.4). It MUST name the soft fail condition that it applies to, MUST give a reason, and MUST give a number N of further attempts. N MUST be an integer greater than or equal to 1. This specification defines no default for N: a request that gives no number, a number below 1, or a number that is not an integer MUST be rejected, and so MUST a request that gives no reason. An override is valid only for a fail condition of the severity `soft` that awaits disposition. An override for any other fail condition MUST be rejected. See AE-104, AE-105, AE-106, AE-107, AE-109.
@@ -4549,7 +4567,7 @@ The `body` of an entry holds exactly these fields:
 - `note`: the text that the actor gave, or `null`;
 - `after`: the record of the state of the change after the action.
 
-A field that does not apply to an action is present with the value `null`. The body holds no other field, except that an action MAY be defined to add fields for itself, and Section 25.3 defines such fields for `migrate`. The first entry of a `full` change is `new`, the entry of an approval is `approve`, and an entry with a name outside the closed set of `action` is not valid. See AE-189, AE-281, AE-285.
+A field that does not apply to an action is present with the value `null`. The body holds no other field, except that an action MAY be defined to add fields for itself, and Section 25.3 defines such fields for `migrate`. The first entry of a `full` change that the `new` action created is `new` (the first entry of a state document that was converted from a YAML state document is the `migrate` entry of Section 25.3), the entry of an approval is `approve`, and an entry with a name outside the closed set of `action` is not valid. See AE-189, AE-281, AE-285, AE-325.
 
 The `after` record holds the whole state of the change after the action, and not only what the action changed, so that the state of the change is the `after` record of the last entry (Section 24.4). In `core`, it holds these fields:
 
@@ -4559,7 +4577,7 @@ The `after` record holds the whole state of the change after the action, and not
 - `wait`: the wait record (Section 23.5), or `null`;
 - `base_revision`: the base revision (Section 24.5), or `null` before it is recorded;
 - `replaced_by`: the identifier given to `supersede`, or `null`;
-- `reason`: `null` unless the outcome is `failed`; when the `fail` action ended the change, the reason text that the actor gave; when a hard fail condition ended the change, a text that names each failing gate and the detail that the evaluation recorded for it, such as the paths outside the scope (Section 24.5);
+- `reason`: `null` unless the outcome is `failed`; when the `fail` action ended the change, the reason text that the actor gave; when a hard fail condition ended the change, a text that names each failing gate and the detail that the evaluation recorded for it, such as the paths outside the scope (Section 24.5); when `cancel` or `supersede` ended a change that awaited the disposition of a soft fail condition, the reason text that the actor gave or, when the actor gave none, a text that names that soft fail condition (Section 23.4);
 - `schema_version`: the version of the schema of the document after the action (Section 25.3).
 
 In `full`, the `after` record holds `phase` and `status` (Section 8.1) in place of `state` and `outcome`. Its field `wait` holds the wait content of Section 11.2 and the other metadata of Section 8.1, or `null`, its field `reason` is `null` unless the status is `failed`, and its other fields are those of `core`. See AE-190, AE-284.
@@ -4697,6 +4715,14 @@ Given a new `full` change that is created and then approved, and an entry whose
 When the entries are written and the entry with that name is validated  
 Then the first entry of the `full` change has the `action` `new`, the entry of the approval has the `action` `approve`, and the entry whose `action` is not in the closed set is not valid
 
+**AE-325 — The first entry of a converted state document is a migrate entry**
+
+- Covers: Section 25.1
+
+Given a `full` change that the `new` action created, and a `full` change whose state document was converted from a YAML state document  
+When the first entry of the state document of each change is read  
+Then the first entry of the first change has the `action` `new`, and the first entry of the second change is the `migrate` entry with `n` 1 (Section 25.3)
+
 **AE-193 — An interrupted creation leaves no state document**
 
 - Covers: Section 25.1
```

## Questions

### Q01 — Approval

- Question: Do you approve the new text exactly as it now stands (fingerprint bfc0df6f9675, 4950 lines), or do you want changes?
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
