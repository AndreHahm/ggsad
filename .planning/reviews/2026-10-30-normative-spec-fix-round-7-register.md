# Fix register, round 7: what changed in the specification and why

This register lists the three changes made to the specification to fix the three BLOCKING findings of the sixth independent review that the owner dispositioned fix. For a change of the kind owner decision the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For a change of the kind repair the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.

## The changes

| Change | Title | Findings | Kind | Status | Sections | Examples |
|---|---|---|---|---|---|---|
| FG-26 | How cancel and supersede end a change that waits for a decision on a soft failure | RH-C-001 | owner decision | drafted | 23.2, 23.4, 24.7, 25.1 | AE-324 |
| FG-27 | The first entry of a change that was converted from a YAML state document | RH-X-001 | repair | drafted | 25.1 | AE-325 |
| FG-28 | Which revision of an ignore file the scope measurement applies | RH-X-002 | owner decision | drafted | 24.5 | AE-326 |

## Change details

### FG-26 — How cancel and supersede end a change that waits for a decision on a soft failure

- What changed: A cancel or supersede of a core change that waits for a decision on a soft failure now closes it as failed, not as cancelled. The person's reason is used when given, otherwise an automatic text names the soft failure. The full profile is not changed, and the text says that the two differ.
- Why: The reviewer says the text let a cancel end such a wait as cancelled, against the rule that the wait ends only by fail or override. The owner dispositioned the finding fix and chose the way.
- Options: Close as failed | Allow cancelled
- Owner decision: Close as failed
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: "The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active."
- After: "or the outcome `failed` when a hard fail condition is active or when the change awaits the disposition of a soft fail condition, that is, when it is `waiting` with a wait record of kind `fail-gate` (Section 24.7)."
- Notes: Sections 23.2, 23.4, 24.7 and 25.1. The `cancel` row of Section 23.4 gains the close as failed for a change that is `waiting` with a wait record of kind `fail-gate`, an optional reason text of the actor, and the reason text of the outcome; the `supersede` row keeps the words As `cancel`. The definitions of `failed` and `cancelled` in Section 23.2, the sentences of Section 24.7 on the close by `cancel` and `supersede` and on the two dispositions of a soft failure, and the member `reason` of Section 25.1 are brought in step, and one paragraph is added to Section 24.7 that also says that the full profile differs. The example AE-324 is placed after AE-43. The example AE-42 is corrected so that its wait has the kind `manual`, because with the kind `fail-gate` its outcome is now `failed`. Owner follow-up answer on the reason text (relayed through the interactive question tool, reason none given), chosen label "Person's reason, else automatic": the person's reason is used when given; otherwise an automatic text names the soft failure that was awaiting a decision. Owner follow-up answer on the full profile (same channel, reason none given), chosen label "Only core changes": the full rows of Sections 8.3 and 8.4 and the full statements of Section 24.7 stay, and the text says openly that core and full differ here, in the paragraph of Section 24.7 that covers both.
  - Section 23.2, the sentence that an outcome of `failed` MUST carry a reason text: stays true; the member `reason` of Section 25.1 now names the third source of that text.
  - Section 23.4, the row `supersede` (As `cancel`), the tables of results (`cancel` is rejected only when the state is `closed`) and the sentence that the actions are performed by a human: stay true.
  - Section 23.4, the examples AE-43, AE-44, AE-299 and AE-322: stay true; the changes of AE-44 and AE-322 are `active`, and the wait of AE-299 is not a wait on a soft failure.
  - Section 23.5 and Section 23.6 step 3, the kind `fail-gate` and the sentence that a soft failure waits until a human disposes of it: stay true.
  - Section 24.1, the examples AE-77 and AE-78: stay true; the change of each is not described as waiting on a soft failure.
  - Section 24.2, the rule that `cancel` and `supersede` take effect when a gate cannot be evaluated, and AE-310: stay true.
  - Section 24.7, the examples AE-99 to AE-101 and AE-308, the sentence on a retry limit and the sentences on an override: stay true.
  - Section 8.3, Section 8.4 and the examples AE-244, AE-247 and AE-298 of the full profile: not edited, as the owner answered.
  - Section 12 and Section 12.1, the sentences that the human closes the change as failed or records an override: stay true; one of them is the quoted sentence of a finding without a disposition and is not edited.
  - Section 24.3 and the list of the actions that need a human: stay true.

### FG-27 — The first entry of a change that was converted from a YAML state document

- What changed: The text now says that the first entry of a full change that the new action created is new, and that a state document converted from an older YAML document starts with a migrate entry. A new example shows both.
- Why: The reviewer says two sections gave different first entries for a converted full change, and the owner dispositioned the finding fix.
- Options: none: no design choice was open, because the finding names the fix itself.
- Owner decision: none: no design choice was open, because the finding names the fix itself.
- Owner reason: none: no design choice was open, because the finding names the fix itself.
- Channel: none: no design choice was open, because the finding names the fix itself.
- Before: "The first entry of a `full` change is `new`"
- After: "The first entry of a `full` change that the `new` action created is `new` (the first entry of a state document that was converted from a YAML state document is the `migrate` entry of Section 25.3)"
- Notes: Section 25.1 only: one sentence of the paragraph on the body fields is rewritten, AE-325 is appended to the See list at the end of that paragraph, and the example AE-325 is placed after AE-285. Section 25.3 is not edited. No design choice was open, because the finding names the fix itself; its two wordings, which qualify the sentence of Section 25.1 or carve out the converted document of Section 25.3, describe the same behaviour on the two cases of AE-325, and the first was drafted because the required action names it first.
  - Section 25.3, the sentence that the first entry of the new state document is a `migrate` entry with `n` 1, and the example AE-214: stay true and are not edited.
  - Section 25.1, the examples AE-189, AE-281 and AE-285: stay true; AE-285 speaks of a new `full` change.
  - Section 24.4, the sentence on the `prev` of the first entry, and the example AE-278 (a new change creates its anchor with its first entry): stay true.
  - Section 25.3, the other sentences on the migration of the state document: stay true.

### FG-28 — Which revision of an ignore file the scope measurement applies

- What changed: Only the ignore files as they were at the base revision now hide a path, so an ignore file that a change creates or alters hides nothing. A new example shows a change that alters the ignore file and then works in the path it now lists.
- Why: The reviewer says the text did not fix which version of an ignore file counts, and the owner chose that only the version at the base revision counts.
- Options: Base revision only | Forbid editing it
- Owner decision: Base revision only
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: "A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement."
- After: "Only ignore files inside the repository count, and only as they were at the base revision: an ignore file that the change creates or alters hides nothing, so a path that only the created or altered ignore file hides is measured like any other path."
- Notes: Section 24.5 only: the sentence on the paths changed since the base revision and the sentence that a file hidden by an ignore file is invisible say that only the ignore file as it was at the base revision hides a path, the See list at the end of that paragraph gains AE-326, and the example AE-326 is placed after AE-307.
  - Section 24.5, the example AE-150 (it already says that the ignore file is in place at the base revision) and the example AE-149: stay true.
  - Section 24.5, the example AE-307: stays true; its ignore file is a new file and the excludes file of the user is not applied.
  - Section 24.5, the sentence that an ignore file is an ordinary file of the working tree and that creating or changing one is a changed path: stays true.
  - Section 24.10, the paragraph on code in a location that an ignore file hides and the example AE-162 (it already says in place at the base revision): stay true.
  - the other uses of the word ignore concern other things (letter case of file systems, the temporary file of the state document) and stay true.

## Normative lines removed or reworded

- A hard failure ends the change as failed without any human a :: The sentence of Section 24.7 on the close as failed by `cancel` and `supersede` also names the change that awaits the disposition of a soft failure.
- A field that does not apply to an action is present with the :: The sentence of Section 25.1 on the first entry of a `full` change is qualified for the change that the `new` action created.

## Findings whose quoted sentence an edit touched

None.

## Findings not touched

- RH-A-001 (MINOR): open information; no edit
- RH-A-002 (INFO): open information; no edit
- RH-B-001 (MAJOR): open information; no edit
- RH-B-002 (MINOR): open information; no edit
- RH-B-003 (INFO): open information; no edit
- RH-C-002 (MAJOR): open information; no edit
- RH-C-003 (MINOR): open information; no edit
- RH-C-004 (INFO): open information; no edit
- RH-X-003 (MAJOR): open information; no edit

## Header

The header of the specification (the Version line and the Revision line) is unchanged by this round.
