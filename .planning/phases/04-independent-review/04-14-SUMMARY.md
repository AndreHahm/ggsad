---
phase: 04-independent-review
plan: 14
subsystem: independent-review-fix-round-4
tags: [independent-review, fix-round, owner-decision, normative-specification, check-script, round-4]
status: complete

requires: ["04-13"]
provides:
  - "Fix round check script with the profile of round 4 (decision questions, register skeleton, stage edits with FE3 to FE7 including the kind repair) and the replay of round 3"
  - "Specification with the three fixes of the BLOCKING findings of round 3: two the way the owner chose, one by the example the finding asks for, with the examples AE-309 and AE-310"
  - "Register of round 4 with the options offered, the owner's choices, before and after, and the sweep of stale statements"
affects: [04-15 (diff identity, approval stages and packet of profile 4, approval of the exact new text), 04-16, 04-17]

actuals:
  tokens: 30000
  tasks: 3
  commits: 8

tech-stack:
  added: []
  patterns: ["profile variables with round 2 as the default", "replay of an earlier round in a throwaway clone", "owner choice tied to the offered options by a check", "kind repair: an entry with no design choice, tied to one fixed sentence by a check"]

key-files:
  created:
    - .planning/reviews/2026-10-27-normative-spec-fix-round-4-register.md
  modified:
    - .planning/phases/04-independent-review/04-check-fix-round.sh
    - docs/method/GG-SAD_normative_method_specification.md

key-decisions:
  - "OD-4 (RT-A-001): Cancel only. OD-5 (RT-B-001): Soft, said openly. Recorded as the owner gave them; they become final only through the owner's approval of the exact text in plan 04-15."
  - "RT-D-001 (FG-15) left no design choice: the finding names the fix itself, an example."

requirements-completed: []  # REVIEW-02 stays open: the fixes void the approval of the text; REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close only.

duration: "not measured; the plan spanned an implementation session (task 1), an owner checkpoint run by the orchestrator and a continuation session (task 3)"
completed: 2026-10-28
---

# Phase 4 Plan 14: Fix Round 4 Summary

PHASE NOT COMPLETE. The three BLOCKING findings of the review of round 3 (RT-A-001, RT-B-001, RT-D-001) are fixed in the specification, two the way the repository owner chose and one by the example the finding asks for, and the changes are recorded in a register. The fixes void the approval of the text of round 3, so the new text must be approved (plan 04-15), reviewed again (plan 04-16) and the new findings dispositioned (plan 04-17). The 20 other findings of round 3 are untouched and still open information. Phase 4 stays open and nothing is ticked.

## Accomplishments

- The fix round script has the profile of round 4: `--round 4`, `--print-decision-questions`, `--print-register-skeleton`, the stage `edits` with the checks FE3 to FE7, the kind `repair` (FE5 compares the Kind cell with the kind the data function gives; FE7 requires the four bullets Options, Owner decision, Owner reason and Channel of such an entry to equal one fixed sentence), and the replay of round 3 (`--replay-round-3`, checks R3-1 to R3-8). Round 2 is the default and profile 3 behaves as before.
- FG-13 (RT-A-001), Sections 8.3, 8.4, 23.4 and 24.1: only `cancel` is exempt from the comparison of the gate definitions; `supersede` is rejected with `changed` false and the issue code `gates-changed` until a human approves the gate definitions again. The `supersede` cells of the two tables of Section 8.3 and of Section 23.4 (precondition, rejected cell, See sentence) and the sentence of Section 8.4 say so. New example AE-309 (placed after AE-78); AE-78 corrected to show `supersede` going ahead once the gate definitions are approved again. No requirement is edited.
- FG-14 (RT-B-001), Section 12: one added paragraph says plainly that the obligation to terminate of that section does not cover a retry limit, that reaching one pauses the flow for a human disposition, and that the earlier text of this method ended the flow there. The sentences that a retry limit is soft are not edited; no example is added (AE-101 already shows the behaviour).
- FG-15 (RT-D-001), Sections 8.3 and 24.2: one new example, AE-310 (placed after AE-298), shows that `wait`, `fail` and `reopen` of a `full` change are each rejected with `changed` false, nothing written, no wait created and the issue code `gate-not-evaluable` when a gate that applies cannot be evaluated; the example is cited in the list of examples of Section 8.3 and in the See sentence of Section 24.2.
- The register records, per change, the options that were offered, the choice as relayed (or the statement that none was open), a before and an after fragment, and the sweep of stale statements. The Requestor did not assess any finding.

## Task Commits

1. Task 1, profile half (tracer): `9a5d8e7` docs(04-14): add the round 4 profile to the fix round check script (tracer)
2. Task 1, replay half: `95323ca` docs(04-14): add the replay of round 3 to the fix round check script
3. Task 2: owner checkpoint run by the orchestrator, no commit
4. Task 3: `83f70ea` docs(04-14): fix-round exemption of supersede from the gate comparison
5. Task 3: `ff36416` docs(04-14): fix-round retry limit that is reached
6. Task 3: `9b55101` docs(04-14): fix-round acceptance example for an action that cannot be evaluated
7. Task 3: `be7c183` docs(04-14): add the fix register of round 4
8. Task 3: this summary, committed as `docs(04-14): summary`.

## Owner decisions

- Statement of channel as the orchestrator gave it: the answers were given by the repository owner through the interactive question tool in the orchestrating session, and are relayed by the orchestrator.
- OD-4 (Supersede, RT-A-001): `Cancel only`; reason: none given.
- OD-5 (Retry limit, RT-B-001): `Soft, said openly`; reason: none given.
- RT-D-001 left no design choice, so nothing was asked about it: the reviewer's own required action is to add an acceptance example covering the rejection of `wait`, `fail` and `reopen` with the issue code `gate-not-evaluable`; the requirement SPEC-14 asks that each `full` rule has an acceptance example of the kind the `core` rules have; the recorded consequences of decision O-8 name giving each rule an acceptance example as the mitigation for a specified-but-unbuilt `full`; and the behaviour to show is fixed by the rule in Section 24.2 that the finding quotes. The owner sees the example in the approval packet of plan 04-15 and may ask for changes there (assumption A-3).
- Statement of the response: before each decision was asked, the owner was told the quoted sentences near the edit sites for that decision (finding ids with section and line). For OD-4 these were the rows for `Cancel only` (Sections 8.3, 8.4, 23.4 and 24.1: RT-X-004 at 24.1 line 3212, RT-A-004 at 8.3 line 909, RT-X-002 at 8.3 line 891 and lines 987-989, and, only if Section 24.7 were stale, RT-X-002 at line 3998 and RT-X-001 at line 4000) and for `Supersede too, said openly` (Sections 8.4 and 24.1: RT-X-004 at 24.1 line 3212), together with the fact that the requirement words cancellation only and that neither label edits requirements. For OD-5 these were the rows for `Soft, said openly` (Section 12, nothing reworded, RT-B-002 at line 1485 in the same section) and for `Hard or soft` and `Hard only` (Sections 12, 12.1, 24.2, 24.7, and 23.3 and 20 only if the sweep found them: RT-B-002 at 12 line 1485 and 12.1 line 1501 would be reworded and stay without a disposition; RT-B-003, RT-X-001, RT-X-002 and, if reached, RT-C-001, RT-C-002, RT-C-003 and RT-B-004 in the same sections). Neither chosen label rewords a quoted sentence of an undispositioned finding.
- These choices carry no name and no date. They become final only through the approval of the exact text in plan 04-15, which carries a name and a date typed by the owner.

## Verification

- Pre-flight of task 1 (before the script change): `CHK --round 3 --stage dispositioned`, `FIX --round 3 --stage approval-recorded`, `FIX --round 3 --stage approval-pending` and `FIX --round 3 --stage edits --complete` each ended `RESULT: PASS`; after the change the same stages and the replays below ended `RESULT: PASS`. The outputs of the three profile 3 printers were byte-identical before and after. On a good fixture the profile 4 stage `edits` ended `RESULT: PASS`; the seeded failures FE5 (the Kind cell of FG-15 read `owner decision`) and FE7 (one word of the FG-15 Channel bullet) exited 1; `--round 5`, `--round 4 --stage state`, `--round 4 --stage approval-pending` and `--round 4 --stage decisions` exited 2; a copy of the round-3 approval record with a foreign blob printed `FAIL R3-1`.
- Precondition of task 3: the blob of the specification was a81d9c89651f326605db08708ea4c079809a2825, the register did not exist, and `FIX --round 3 --stage edits --complete` ended `RESULT: PASS`.
- After the last specification and register commit:
  - `bash FIX --round 4 --stage edits --complete` ends `RESULT: PASS`, exit 0, with `PASS FE3`, `PASS FE4`, `PASS FE5`, `PASS FE6` and `PASS FE7`.
  - `bash CHK2 --final` ends `RESULT: PASS`.
  - `bash FIX --replay-round-3 --with-current-scripts` ends `RESULT: PASS` and holds `PASS R3-1` to `PASS R3-8`.
  - `bash FIX --replay-round-2 --with-current-scripts` ends `RESULT: PASS` and holds `PASS R2-1` to `PASS R2-8`.
  - `bash FIX --replay-round-1 --with-current-scripts` ends `RESULT: PASS`.
- The blob of the specification is now fca228479a34e228785f4c0b100da3c6745ada0a; its first eight lines (the header) are identical to those of the text of round 3. The highest example id is AE-310, as the register ends its run. Each of the three specification commits lists only the specification; the register commit lists only the register.
- The register holds three `### FG-1` entries, three rows with the status drafted, three Owner decision bullets (two equal to the labels above, one equal to the fixed no-choice sentence), two Channel bullets equal to the fixed sentence, no fill marker, no banned path or temporary-file word, and no line `- RT-B-002 :: ` (no quoted sentence of an undispositioned finding was reworded). No requirement is ticked.

## Sweep results (short)

- FG-13: Sections 8.3, 8.4, 23.4 and 24.1 updated (the `supersede` cells of the tables, the sentence of Section 8.4, the paragraph on the exempt operations); AE-78 corrected and AE-309 added. The sentence of Section 24.1 on the comparison of every operation (RT-X-004), the `wait` row and the `reopen` cell of Section 8.3 (RT-X-002, RT-A-004), the `cancel` rows, AE-77, Section 24.2, Section 24.7 and AE-44 and AE-45 stay true. Section 24.7 was not stale.
- FG-14: Section 12 updated by one paragraph; Section 12.1, Section 23.3, Sections 24.2 and 24.7 (retry limit), AE-101 and AE-108 and Section 20 stay true.
- FG-15: Sections 8.3 and 24.2 gain the citation of AE-310 and one example; the sentences that point to Section 24.2 and the issue code `gate-not-evaluable` and the examples AE-297 to AE-299 stay true.

## Dispatch

Dispatch: sequential executors on the main working tree (workflow.use_worktrees is false).

## Deviations from Plan

**1. [Process] Recommendations printed in the owner questions.** At the owner's request (asked twice, and "always show which option you recommend"), the orchestrator printed "My recommendation: ..." in the text of each question (OD-4: `Cancel only`; OD-5: `Soft, said openly`) and gave reasons. The labels and descriptions were printed exactly as the script prints them. The recommendation was the orchestrator's judgment, not the reviewer's verdict, and the owner chose. The plan says that no option is marked as recommended; this is recorded here so that the owner and the later approval can weigh the choices accordingly. The channel sentence of the Channel bullet stays the fixed sentence the script requires.

**2. [Reading] Two points shown to the owner for confirmation.** (a) The specification has no name for the text that Section 12 replaced, so the added sentence says `the earlier text of this method`, following the wording of the option; this is marked in the Notes of FG-14. (b) For `Cancel only` the example AE-78 was made false and is corrected to show `supersede` going ahead once the gate definitions are approved again, which follows from the option (`supersede` is refused until a human approves the edited checks again); AE-309 shows the refusal.

**3. [Rule 3 - Blocking] Example title and Covers line of AE-310.** The Phase 2 check (rule R7) wants every line that names `reopen` in Section 8 to name `full`; the title of AE-310 therefore says `A full change` and the Covers line says `full`. No other change was needed.

**4. [Process] Commit splitting.** The three fixes share one file and were written together so that the register and the checks could be run once; the specification was then committed in three steps (one per finding) from intermediate states of the same file, and the three commits together equal the checked working file byte for byte.

## Known Stubs

None.

## Unverified

- The Python baseline (uv, ruff, ty, pytest) was not run: only .planning/ and the specification changed.
- The owner's answers reached this executor through the orchestrator's message and cannot be independently checked from the repository; the register states the channel, and FE7 proves that the recorded choice is one of the options offered, not who answered.
- The checks prove structure, minimality and consistency with the register, not that any text is right. Which findings are correct is not assessed here.
- The 20 undispositioned findings (RT-A-002, RT-A-003, RT-A-004, RT-B-002, RT-B-003, RT-B-004, RT-C-001, RT-C-002, RT-C-003, RT-D-002, RT-D-003, RT-E-001, RT-E-002, RT-E-003, RT-X-001, RT-X-002, RT-X-003, RT-X-004, RT-X-005, RT-X-006) are untouched and still open information.
- Note for plan 04-15: the round-4 packet printer still carries round-3 wording ("second time", "your decision: <label>"); plan 04-15 must edit it and add the reading of a `repair` entry.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-15 (diff identity again, approval stages and packet of profile 4, approval of the exact new text). From the first specification commit of this plan, the live checks that pin the text of round 3 fail by design; `bash FIX --replay-round-3` keeps the evidence of round 3 checkable.

## Self-Check: PASSED

- Files exist: the fix round script, the specification, the register and this summary.
- Commits `9a5d8e7`, `95323ca`, `83f70ea`, `ff36416`, `9b55101` and `be7c183` exist on gsd/v1.1-executable-core.
- `bash FIX --round 4 --stage edits --complete` ends `RESULT: PASS`; the replays of rounds 1, 2 and 3 end `RESULT: PASS`.
