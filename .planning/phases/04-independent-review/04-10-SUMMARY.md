---
phase: 04-independent-review
plan: 10
subsystem: independent-review-fix-round-3
tags: [independent-review, fix-round, owner-decision, normative-specification, check-script, round-3]
status: complete

requires: ["04-09"]
provides:
  - "Fix round check script with the profile of round 3 (decision questions, register skeleton, stage edits with FE3 to FE7) and the replay of round 2"
  - "Specification with the three fixes of the BLOCKING findings of round 2, each the way the owner chose, with the examples AE-306 to AE-308"
  - "Register of round 3 with the options offered, the owner's choice, before and after, and the sweep of stale statements"
affects: [04-11 (diff identity, approval packet and approval of the exact new text), 04-12, 04-13]

actuals:
  tokens: 20500
  tasks: 3
  commits: 6

tech-stack:
  added: []
  patterns: ["profile variables with round 2 as the default", "replay of an earlier round in a throwaway clone", "owner choice tied to the offered options by a check"]

key-files:
  created:
    - .planning/reviews/2026-10-27-normative-spec-fix-round-3-register.md
  modified:
    - .planning/phases/04-independent-review/04-check-fix-round.sh
    - docs/method/GG-SAD_normative_method_specification.md

key-decisions:
  - "OD-1 (RR-B-001): Accept an equivalent. OD-2 (RR-X-001): Repository files only. OD-3 (RR-X-002): Soft failures only. Recorded as the owner gave them; they become final only through the owner's approval of the exact text in plan 04-11."

requirements-completed: []  # REVIEW-02 stays open: the fixes void the approval of the text; REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close only.

duration: "not measured; the plan spanned an implementation session, an owner checkpoint run by the orchestrator and a continuation session"
completed: 2026-10-27
---

# Phase 4 Plan 10: Fix Round 3 Summary

PHASE NOT COMPLETE. The three BLOCKING findings of the review of round 2 (RR-B-001, RR-X-001, RR-X-002) are fixed in the specification the way the repository owner chose, and the changes are recorded in a register. The fixes void the approval of the text of round 2, so the new text must be approved (plan 04-11), reviewed again (plan 04-12) and the new findings dispositioned (plan 04-13). The nine other findings of round 2 are untouched and still open information. Phase 4 stays open and nothing is ticked.

## Accomplishments

- The fix round script has the profile of round 3: `--round 3`, `--print-decision-questions`, `--print-register-skeleton`, the stage `edits` with the checks FE3 to FE7, and the replay of round 2 (`--replay-round-2`, checks R2-1 to R2-8). Round 2 is the default and behaves as before.
- RR-B-001, Section 22.4: the first verification of `guard` now requires an anchor or an equivalent mechanism (Section 24.4), and the sentence on the stable issue codes says that `anchor-missing` is reported when the history has neither. New example AE-306.
- RR-X-001, Sections 24.5 and 24.10: only ignore files inside the repository count; creating or changing one is a changed path that needs an allowed path; ignore settings kept elsewhere are not applied. New example AE-307; AE-150 and AE-162 corrected (the ignore file is inside the repository and in place at the base revision).
- RR-X-002, Sections 8.3 and 24.7: `fail` in the `full` profile is allowed only while a soft failure awaits disposition; with only a hard failure active it is rejected with `changed` false. Section 24.7 names `fail` as a second exception next to `start`. New example AE-308; AE-243 corrected.
- The register records, per change, the options that were offered, the choice as relayed, a before and an after fragment, and the sweep of stale statements. The Requestor did not assess any finding.

## Task Commits

1. Task 1 (tracer): `bc40aa5` docs(04-10): add the round 3 profile and the replay of round 2 to the fix round check script (tracer)
2. Task 2: owner checkpoint run by the orchestrator, no commit
3. Task 3: `ee6bab0` docs(04-10): fix-round guard history verification
4. Task 3: `9f7e030` docs(04-10): fix-round scope measurement and ignore settings
5. Task 3: `4e3e62f` docs(04-10): fix-round fail action precondition
6. Task 3: `71c591d` docs(04-10): add the fix register of round 3
7. Task 3: this summary, committed as `docs(04-10): summary`.

## Owner decisions

- Statement of channel as the orchestrator gave it: the answers were given by the repository owner through the interactive question tool (AskUserQuestion) in the orchestrating session, one question at a time, and are relayed by the orchestrator.
- OD-1 (Guard anchor, RR-B-001): `Accept an equivalent`; reason: none given.
- OD-2 (Ignore settings, RR-X-001): `Repository files only`; reason: none given.
- OD-3 (Fail action, RR-X-002): `Soft failures only`; reason: none given.
- These choices carry no name and no date. They become final only through the approval of the exact text in plan 04-11, which carries a name and a date typed by the owner.

## Verification

- Pre-flight of task 1 (before the script change): `CHK --round 2 --stage dispositioned`, `FIX --stage approval-recorded`, `FIX --stage approval-pending`, `FIX --stage edits --complete`, `CHK2 --final` and `FIX --replay-round-1 --with-current-scripts` each ended `RESULT: PASS`; after the change the same commands and `FIX --replay-round-2 --with-current-scripts` ended `RESULT: PASS`.
- Precondition of task 3: the blob of the specification was 93f8278f1b0427444016cdbfa4b0e4ff9d16d369, the register did not exist, and `FIX --replay-round-2 --with-current-scripts` ended `RESULT: PASS`.
- After the last commit:
  - `bash FIX --round 3 --stage edits --complete` ends `RESULT: PASS`, exit 0, with `PASS FE3`, `PASS FE4`, `PASS FE5`, `PASS FE6` and `PASS FE7`.
  - `bash CHK2 --final` ends `RESULT: PASS`.
  - `bash FIX --replay-round-2 --with-current-scripts` ends `RESULT: PASS` and holds `PASS R2-1` to `PASS R2-8`.
  - `bash FIX --replay-round-1 --with-current-scripts` ends `RESULT: PASS` and holds `PASS FR5`.
- The blob of the specification is now a81d9c89651f326605db08708ea4c079809a2825; its first eight lines (the header) are identical to those of the text of round 2. The highest example id is AE-308, as the register ends its run. Each of the three specification commits lists only the specification; the register commit lists only the register.
- The register holds three `### FG-1` entries, three rows with the status drafted, three Owner decision bullets equal to the labels above, three Channel bullets equal to the fixed sentence, no fill marker, and none of the banned path or temporary-file words. `git diff --name-only origin/main...HEAD` lists the specification and paths under .planning/ only; nothing under src, .ggsad, specs, tests, AGENTS.md or CLAUDE.md. No requirement is ticked. `git worktree list` shows one entry and `git status --short` is empty.

## Sweep results (short)

- FG-10: Section 24.4, AE-142, the `new` and `adopt` rows and AE-303 to AE-305 stay true; Section 22.4 updated in three places.
- FG-11: Sections 24.5 (two paragraphs) and 24.10 (one phrase) updated; AE-150 and AE-162 corrected; AE-149, AE-152 and the temporary-file sentences stay true.
- FG-12: both `fail` cells of Section 8.3 and one passage of Section 24.7 updated; AE-243 corrected; Sections 8.4, 23.4, 24.2 and AE-98 to AE-101 stay true.

## Deviations from Plan

**1. [Rule 1 - Bug] Check R2-6 of the round-2 replay (task 1).** The executor of task 1 changed R2-6 from `--stage brief`, which cannot pass at a commit that holds the captured reports, to `--round 2 --print-brief` equal to the round-2 brief character for character. It also reworded the error message of `--with-current-scripts`. Both were done in task 1 and are in `bc40aa5`; the replay of round 2 passes.

**2. [Rule 2 - Consistency] One sentence of Section 24.7 beyond the two cells.** For OD-3 the plan names the Precondition cell and the rejected cell of the `fail` row. The sweep found that the paragraph on hard failure (an action that finds a hard failure closes the change as failed) would again read as applying to a refused `fail`, so one sentence names `fail` as a second exception and `start` is described as an exception instead of the exception. The register lists the removed line with its reason.

**3. [Reading] One point of OD-2 shown to the owner.** The option says ignore settings kept elsewhere are not applied. The exclude file in the metadata directory of version control is not an ordinary file of the working tree and cannot appear as a changed path, so the text counts it among the settings kept elsewhere; this follows from the reason the option gives. It is marked in the Notes of FG-11 as a point for the owner to confirm in the approval. No other point was left open by a chosen option.

## Known Stubs

None.

## Unverified

- The Python baseline (uv, ruff, ty, pytest) was not run: only .planning/ and the specification changed.
- The owner's answers reached this executor through the orchestrator's message and cannot be independently checked from the repository; the register states the channel, and FE7 proves that the recorded choice is one of the options offered, not who answered.
- The checks prove structure, minimality and consistency with the register, not that any text is right. Which findings are correct is not assessed here.
- The nine undispositioned findings (RR-A-001, RR-A-002, RR-A-003, RR-B-002, RR-B-003, RR-X-003, RR-X-004, RR-X-005, RR-X-006) are untouched and still open information.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-11 (diff identity again, approval packet, approval of the exact new text). From the first specification commit of this plan, the live checks that pin the text of round 2 fail by design; `bash FIX --replay-round-2` keeps the evidence of round 2 checkable.

## Self-Check: PASSED

- Files exist: the fix round script, the specification, the register and this summary.
- Commits `bc40aa5`, `ee6bab0`, `9f7e030`, `4e3e62f` and `71c591d` exist on gsd/v1.1-executable-core.
- `bash FIX --round 3 --stage edits --complete` ends `RESULT: PASS`; the replays of rounds 1 and 2 end `RESULT: PASS`.
