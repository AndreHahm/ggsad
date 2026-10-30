---
phase: 04-independent-review
plan: 27
subsystem: independent-review-fix-round-7-approval
tags: [independent-review, owner-approval, normative-specification, check-script, round-7]
status: complete

requires: ["04-26"]
provides:
  - "Diff identity note updated in place with the pins of the text of fix round 7 (bfc0df6f96756c0c162d694067fd363e272d36b7, 4950 lines) and a pointer to the approval record"
  - "Profile 7 of the approval stages and printers of the fix round check script, with every read of the disposition addendum guarded by ADD_RND greater than 0"
  - "Approval packet of round 7, printed by the script, and the owner approval record of round 7 (outcome approved)"
affects: [04-28 (preparation of the independent review of the approved text), 04-29]

actuals:
  tokens: 8900
  tasks: 3
  commits: 7

tech-stack:
  added: []
  patterns: ["profile variables with round 2 as the default", "addendum reads guarded by a profile variable, not by the round number", "packet printed from the live text and the register, equal byte for byte", "record rebuilt from pins and printed questions"]

key-files:
  created:
    - .planning/reviews/2026-10-30-normative-spec-fix-round-7-approval-packet.md
    - .planning/reviews/2026-10-30-normative-spec-fix-round-7-approval-record.md
  modified:
    - .planning/reviews/2026-10-24-normative-spec-diff-identity.md
    - .planning/phases/04-independent-review/04-check-fix-round.sh

key-decisions:
  - "The owner approved the exact text of fix round 7 (fingerprint bfc0df6f9675, 4950 lines), which makes the fixes of plan 04-26 (the close as failed for cancel and supersede of a core change that waits on a soft failure, FG-26; the repair of the first entry of a converted full change, FG-27; the base-revision-only reading of an ignore file, FG-28) final as part of that text."

requirements-completed: []  # No plan ticks a requirement here. REVIEW-02 stays open and the tick of APPR-01 from the first round is not changed by any plan; the orchestrator alone decides at phase close.

duration: "not measured; the plan spanned an implementation session (task 1), an owner checkpoint run by the orchestrator and a continuation session (task 3)"
completed: 2026-10-30
---

# Phase 4 Plan 27: Approval of the Text of Fix Round 7 Summary

PHASE NOT COMPLETE. The repository owner approved the exact new text of the specification (blob `bfc0df6f96756c0c162d694067fd363e272d36b7`, 4950 lines) and the approval is on record with the exact pins. The independent review of this text has not started; plan 04-28 asks the owner which parts it reads and whether the exact run may be sent. Phase 4 stays open and no requirement is ticked by this plan.

## Outcome

Approved. Record: `.planning/reviews/2026-10-30-normative-spec-fix-round-7-approval-record.md`. Key lines of the record:

- `Owner approval: approved`
- `Owner reply date: 2026-10-30`
- `Reply given by`: AndreHahm
- `Owner reply`: given by the repository owner through the interactive question tool and relayed by the orchestrating session; the name and the date were picks from candidates that the owner asked for and were not typed.

## Owner answers (as relayed)

- Statement of channel as the orchestrating session gave it: the answers were given by the repository owner through the interactive question tool in this session (the orchestrating session).
- Q01 (Approval), question text as the script prints it (the asked text also carried a short summary of the three changes and a recommendation sentence, which are not recorded): "Do you approve the new text exactly as it now stands (fingerprint bfc0df6f9675, 4950 lines), or do you want changes?" Answer: `Approve exact text`.
- Q02 (Changes): not asked, because the text was approved. Recorded as `None. (not asked, because the text was approved)`.
- Q03 (Name): the typed reply came back twice only as the option label `Type it under Other`; the owner then answered `Yes, offer candidates` when asked whether candidates were wanted and picked `AndreHahm` from the candidates `AndreHahm` and `Andre Hahm`. The name is a pick from candidates the owner asked for; it was not typed.
- Q04 (Date): the same sequence. The owner picked `2026-10-30` from the candidates `2026-10-30` and `2026-10-31`. A pick from candidates the owner asked for; not typed. It is not earlier than 2026-10-30, the Owner disposition date of the disposition record of round 6.
- The choices of plan 04-26 and the repair were kept: the owner requested no change (Q01 was `Approve exact text`).

## Accomplishments

- IDN: the diff identity note was updated in place with the pins of the final text (task 1), then pointed at the approval record of round 7 with the statement that the independent review of this text has not taken place (task 3).
- FIX: profile 7 of the stages `approval-pending` and `approval-recorded` and of the four printers (`--print-delta`, `--print-approval-questions`, `--print-approval-packet`, `--print-approval-record-skeleton`). The reads of the addendum in `ap_facts`, `ap_pin_rows`, the addendum argument of the call of the stage edits in AP4 (the item flagged in the summary of plan 04-26) and the lower bound of the date in AR5 are guarded by ADD_RND greater than 0; the paragraph `What you are asked` leaves out the list of answers on further findings when there is no addendum. The stages state, decisions and dispositions exit 2 under `--round 7`. Round 2 stays the default and profiles 3 to 6 behave as before. No `"$ROUND" -eq [56]` match remains in the approval section; the one remaining `-ge 5` there selects the paragraph function that profiles 5, 6 and 7 share.
- APK7: printed by the script from the live text and the register; its status line changed once, from pending to recorded in the owner approval record.
- ARC7: created from the printed skeleton and filled with the owner's answers; pins the text, the previously approved text of round 6, the register and the packet.

## Task Commits

1. Task 1: `912d3e1` docs(04-27): record the diff identity of the text of fix round 7
2. Task 1: `e87fc95` docs(04-27): add profile 7 of the approval stages and printers to the fix round check script (tracer)
3. Task 1: `cdacca4` docs(04-27): add the owner approval packet of fix round 7
4. Task 2: owner checkpoint run by the orchestrator, no commit
5. Task 3: `9d40ea6` docs(04-27): record the owner approval of fix round 7
6. Task 3: `21a5d35` docs(04-27): mark the fix round 7 packet as recorded
7. Task 3: `c3c13aa` docs(04-27): point the diff identity note at the approval record of round 7
8. Task 3: this summary, committed as `docs(04-27): summary`.

## Verification

- Task 1 (tracer): `bash FIX --round 7 --stage approval-pending` ended `RESULT: PASS` with PASS lines for AP1 to AP5. Seeded cases against copies, each printing the named id and exiting 1: identity copy with one digit changed, `FAIL AP1`; packet copy with one delta character changed, `FAIL AP2`; register copy with one word of a Why changed, `FAIL AP2`; register copy with the Options bullet of the repair entry FG-27 changed, `FAIL AP4`; Q01 `Maybe`, `FAIL AR4`; outcome approved next to `Request changes`, `FAIL AR4`; one character of a Question changed, `FAIL AR3`; one digit of a pin changed, `FAIL AR2`; a date earlier than 2026-10-30, `FAIL AR5`; the date 2026-02-30, `FAIL AR5`; an unfilled marker, `FAIL AR1`. Good record fixtures for both outcomes ended `RESULT: PASS`. `--round 7 --stage state`, `--stage dispositions` and `--stage decisions` exit 2. The printers of the earlier profiles (approval questions of rounds 3 to 6, decision questions and register skeletons of rounds 4 to 7, packet, record skeleton and delta of round 6) printed the same bytes and exit codes before and after the script change (45 saved files compared equal). The hunk count of `--print-delta` (11) equals that of `git diff --unified=3` between the round-6 blob and the working blob. `bash -n` and `shellcheck` on the script exit 0.
- Pre-record state (task 3 precondition): `git status --short` was empty, the blob of the specification was `bfc0df6f96756c0c162d694067fd363e272d36b7` and equal to the Result blob row of the identity note, the record did not exist, and `bash FIX --round 7 --stage approval-pending` ended `RESULT: PASS`. `bash CHK2 --final` ended `RESULT: PASS` before the record was filled, as the Check results row says.
- After the three task-3 commits, run on the committed state, one at a time in the foreground:
  - `bash FIX --round 7 --stage approval-recorded` ends `RESULT: PASS` (AR1 to AR5), exit 0.
  - `bash FIX --round 7 --stage approval-pending` ends `RESULT: PASS` (AP2 and AP5 accept the recorded status line once the record exists).
  - `bash FIX --round 6 --stage dispositions` ends `RESULT: PASS`.
  - `bash CHK2 --final` ends `RESULT: PASS`.
  - `bash FIX --replay-round-6 --with-current-scripts` ends `PASS R6-8` and `RESULT: PASS`; `--replay-round-5` ends `PASS R5-8` and `RESULT: PASS`; `--replay-round-4` ends `PASS R4-8` and `RESULT: PASS`; `--replay-round-3` ends `PASS R3-8` and `RESULT: PASS`; `--replay-round-2` ends `PASS R2-8` and `RESULT: PASS`; `--replay-round-1` ends `PASS FR5` and `RESULT: PASS`. The same replays also ended `RESULT: PASS` at the end of task 1.
- The seeded cases were not repeated against the final record of task 3; they were run in task 1 against fixtures built from the printed skeleton.
- `git hash-object` of the specification is `bfc0df6f96756c0c162d694067fd363e272d36b7`, equal to the Result blob row of the record, and unchanged by this plan. The record holds no fill marker (`grep -c FILL` prints 0), four question blocks and four answers, and one outcome line.
- `git diff --name-only origin/main...HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; `grep -c '^- \[x\] \*\*REVIEW-0' .planning/REQUIREMENTS.md` prints 0; `git worktree list` prints one line; `git status --short` was empty before this summary was written.
- The record commit lists exactly the record; the packet commit lists exactly the packet and changes one line; the identity commits list exactly the identity note.

## Dispatch

Dispatch: sequential executors on the main working tree (workflow.use_worktrees is false)

The Python baseline (uv, ruff, ty, pytest) was not run, because only .planning/ changed.

## Deviations from Plan

**1. [Process] Recommendation sentence in the owner question.** At the owner's standing request the orchestrator appended `(My recommendation: ...)` to the text of the questions, and the text of Q01 also carried a short summary of the three changes. These are not part of the recorded questions, so check AR3 holds; the plan says that no option is recommended. This is stated here so that the approval can be weighed accordingly.

**2. [Channel] Name and date are picks from candidates.** The plan asks for the name and the date as separate free-text questions and forbids suggesting either. The free-text replies came back twice only as the option label, the owner asked for candidates and picked `AndreHahm` and `2026-10-30` in the tool. The record states the picks in its Owner reply row.

**3. [Tooling] Packet written by redirect.** Task 1 wrote the packet file by redirecting the output of `--print-approval-packet` instead of copying it through the Write tool. The bytes are the script's own, and AP2 confirms byte equality (commit `cdacca4`).

**4. [Process] Stray python process.** Task 1 started one `python3` heredoc command by mistake; it hung and was not killed, as the standing rules say. It touched no file, and the edit was redone with the Edit tool. A stray process may still exist.

## Known Stubs

None.

## Unverified

- The owner's answers reached this executor through the orchestrator's message and cannot be independently checked from the repository. The record states the channel; the checks prove completeness, consistency and the tie to the pinned text, not who answered.
- The name and the date were picks from candidates that the orchestrator offered at the owner's request; the owner's own typed reply never reached the record.
- The checks prove structure and consistency, not that the text is right. The text has not been independently reviewed.
- The reason fields of the two owner decisions in the register read `none given`.
- Requirement honesty: APPR-01 was ticked for the first text. The tick is not changed by any plan; it rests, for this text, on the new record. The orchestrator alone decides at phase close whether it stands. REVIEW-01 and REVIEW-02 are not ticked; they are supported only by the stated scope of the later review.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-28: the owner decides which parts of the approved text the independent review reads and consents to the exact run. Nothing is sent before that.
