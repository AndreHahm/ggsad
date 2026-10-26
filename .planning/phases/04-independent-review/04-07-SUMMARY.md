---
phase: 04-independent-review
plan: 07
subsystem: independent-review-fix-round-approval
tags: [independent-review, fix-round, owner-approval, approval-packet, approval-record, check-script]
status: complete

requires: ["04-06"]
provides:
  - "Diff identity note updated in place with the pins of the final text of the fix round (blob 93f8278f1b0427444016cdbfa4b0e4ff9d16d369, 4770 lines)"
  - "Check script extended with the stages approval-pending (AP1 to AP5) and approval-recorded (AR1 to AR5) and the printers --print-delta, --print-approval-questions, --print-approval-packet and --print-approval-record-skeleton"
  - "Approval packet of the fix round, printed from the live text and the register"
  - "Owner approval record of the fix round, outcome approved"
affects: [04-08, 04-09]

actuals:
  tokens: 25000
  tasks: 3
  commits: 7

tech-stack:
  added: []
  patterns: ["packet and record created only from script printers; the check requires byte equality with the printed form", "questions printed by one function, compared with the recorded questions character for character", "outcome derived by rule and checked"]

key-files:
  created:
    - .planning/reviews/2026-10-26-normative-spec-fix-round-approval-packet.md
    - .planning/reviews/2026-10-26-normative-spec-fix-round-approval-record.md
    - .planning/phases/04-independent-review/04-07-SUMMARY.md
  modified:
    - .planning/reviews/2026-10-24-normative-spec-diff-identity.md
    - .planning/phases/04-independent-review/04-check-fix-round.sh

key-decisions:
  - "Outcome of the approval round: approved. The owner approved the exact text with fingerprint 93f8278f1b04 (4770 lines) and asked for no change, so all five Requestor picks stand."

requirements-completed: []  # APPR-01 is re-obtained for the new text but the tick is decided by the orchestrator at phase close only; REVIEW-01 and REVIEW-02 stay open.

duration: "not measured; the plan spanned an implementation session and an owner checkpoint run by the orchestrator"
completed: 2026-10-26
---

# Phase 4 Plan 07: Owner Approval of the Fix Round Summary

PHASE NOT COMPLETE. The repository owner approved the exact new text of the specification, so the approval record of the fix round exists and pins the text for the limited independent review of plan 04-08. Phase 4 stays open: the independent review of this text has not taken place, and REVIEW-01, REVIEW-02 and APPR-01 are not ticked by this plan.

## Outcome

- Owner approval: approved. The check `bash FIX --stage approval-recorded` prints PASS for AR1 to AR5 and `RESULT: PASS`.
- The approval is of the text with blob `93f8278f1b0427444016cdbfa4b0e4ff9d16d369`, SHA-256 `6c0e86dd39e74242566755db6702972d893a83cc4827d9fc7e4805f89db85d91`, 4770 lines, 1 file changed, 3393 insertions and 45 deletions against the base, 46 commits touching the file. The previously approved text (blob `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`) stays as history.
- The five changes marked `my choice` in the register (FG-02, FG-04, FG-07, FG-08, FG-09: re-opening a closed change whose new work would have to wait; cancelling or replacing a change when a check cannot be run; what happens when a retry limit is reached; deciding whether a file is text or binary before hashing it; the guard check for continuous integration) were approved as drafted. The owner requested no change.
- The four other changes (FG-01, FG-03, FG-05, FG-06) are repairs where the text had one consistent reading.

## The owner's answers

- Statement of channel as the orchestrator gave it: the answers were given by the repository owner through the interactive question tool in this session and relayed by the orchestrating session.
- Q01 (Approval), question as asked, equal to the printed question: "Do you approve the new text exactly as it now stands (fingerprint 93f8278f1b04, 4770 lines), or do you want changes?" Answer: `Approve exact text`.
- Q02 (Changes): not asked, because the text was approved.
- Q03 (Name): `AndreHahm`. Q04 (Date): `2026-10-26`. Both were picks from candidates that the owner explicitly asked to be offered, and the record says so in one sentence in the row Owner reply.

## Accomplishments

- The diff identity note holds the pins of the final text (rows Result blob, Reviewed SHA-256, Line count, Diffstat and Check results); the one sentence on approval and review now says that owner approval of this text is recorded in the owner approval record of the fix round and that the independent review of this text has not taken place.
- The check script has the stages approval-pending and approval-recorded and four printers. The packet is the printed output (nine changes in plain words, before and after, the pins, the exact delta, the four questions); the record was created from the printed skeleton and filled with the owner's words only.
- The packet status line is now `recorded in the owner approval record`; nothing else in the packet changed. Checks AP2 and AP5 accept this form once a record exists.

## Task Commits

1. Task 1 (tracer): `11d7669` docs(04-07): record the diff identity of the text of the fix round
2. Task 1 (tracer): `cac5cab` docs(04-07): add the approval stages and printers to the fix round check script (tracer)
3. Task 1 (tracer): `78ca8d2` docs(04-07): add the owner approval packet of the fix round
4. Task 2: owner checkpoint run by the orchestrator, no commit
5. Task 3: `4af5eb1` docs(04-07): record the owner approval of the fix round
6. Task 3: `4155dd1` docs(04-07): mark the fix round packet as recorded
7. Task 3: `d7aba79` docs(04-07): point the diff identity note at the approval record of the fix round
8. Task 3: this summary, committed as `docs(04-07): summary`.

## Verification

- `bash FIX --stage approval-recorded` ends `RESULT: PASS` (exit 0) with AR1 to AR5 passing; `bash FIX --stage approval-pending` ends `RESULT: PASS` with the packet in its recorded form; `bash CHK2 --final` ends `RESULT: PASS`; `bash FIX --replay-round-1 --with-current-scripts` ends `RESULT: PASS`. The pending-stage run and the final diff check were run before the record was filled, and all four checks were run again after the three commits of task 3.
- `git hash-object docs/method/GG-SAD_normative_method_specification.md` prints `93f8278f1b0427444016cdbfa4b0e4ff9d16d369`, equal to the Result blob row of the record and of the identity note. The specification, the register and the round-1 evidence are not edited by this plan.
- The record holds no fill marker (count 0), four question blocks and four answers, and exactly one `- Owner approval: approved` line. The record commit lists only the record, the packet commit lists only the packet and changes one line, the identity commit lists only the identity note and changes one line.
- Seeded runs against copies of the finished record, each printing the named id and exiting 1: Q01 answered `Maybe` (AR4); the outcome `changes requested` next to Q01 `Approve exact text` (AR4); one word of a question changed (AR3); one digit of a pin changed (AR2); the date 2026-02-30 (AR5, together with AR2, since the replacement changed every occurrence of the date); a fill marker left in the Q03 answer (AR1, together with AR5). The unchanged record ends `RESULT: PASS`. The seeded cases of the tracer (task 1) were run in that task and are not repeated here beyond this subset.
- `git diff --name-only origin/main...HEAD` lists the specification and paths under `.planning/` only; the diff for `src .ggsad specs tests AGENTS.md CLAUDE.md` is empty; `grep -c '^- \[x\] \*\*REVIEW-0' .planning/REQUIREMENTS.md` prints 0.

## Deviations from Plan

**1. [Observation] `.planning/REQUIREMENTS.md` appears in `git diff --name-only origin/main...HEAD`.** The acceptance text expects that command to print nothing for that file. The file differs from the base branch because of edits made by earlier phases; none of the commits of this plan touches it (each commit lists the files named above). Nothing was changed to alter the output.

**2. [Channel] Name and date are picks from candidates.** The plan forbids suggesting a name or a date. The owner explicitly asked the orchestrator to offer candidates and picked one for each; the record says so in one sentence.

**3. [Tracer gate] No separate tracer checkpoint.** Auto mode was not active; execution continued from the tracer commit to the owner checkpoint as the orchestrator directed.

## Known Stubs

None.

## Unverified

- The owner's answers reached this executor through the orchestrator's message and cannot be independently checked from the repository. The record states the channel, and the checks prove completeness, consistency and the tie to the pinned text, not who answered. Name and date were picks from candidates, so they are not independent evidence of identity.
- The owner's reading of the nine changes and of the exact delta cannot be shown; the record proves that the answer concerns the text with the recorded fingerprint.
- The independent review of this text has not taken place; nothing here asserts its result.
- Whether the tick of APPR-01 from round 1 stands for this text is not decided here; it rests, for this text, on the record, and the orchestrator alone decides at phase close.

## Next step

Plan 04-08: the round profile of the review check script, the consent of the owner, and the limited independent review (header and Sections 1 to 8, Sections 9 to 22, and the whole text read across sections; Sections 23, 24 and 25 are read only by the pass over the whole text) of the text pinned by the approval record. Any edit of the specification before the review voids the approval.

## Self-Check: PASSED

- Files exist: the diff identity note, the check script, the packet, the record and this summary.
- Commits `11d7669`, `cac5cab`, `78ca8d2`, `4af5eb1`, `4155dd1` and `d7aba79` exist on gsd/v1.1-executable-core.
- `bash FIX --stage approval-recorded` ends `RESULT: PASS`; the specification blob is unchanged.
