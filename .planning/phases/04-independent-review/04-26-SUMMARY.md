---
phase: 04-independent-review
plan: 26
subsystem: independent-review-fix-round-7
tags: [independent-review, owner-decision, fix-round, specification-edit, round-7]
status: complete

requires: ["04-25"]
provides:
  - "Profile 7 of the fix round check script (no addendum) and the replay of round 6"
  - "Specification edits for RH-C-001 (FG-26), RH-X-001 (FG-27) and RH-X-002 (FG-28)"
  - "Fix register of round 7"
affects: [04-27 approval of the exact new text, 04-28 review of round 7, 04-29 dispositions of round 7]

actuals:
  tokens: 9000   # chars/4 over the files changed by task 3 only (specification, register, this summary); the script changed by task 1 is not counted
  tasks: 3
  commits: 8

tech-stack:
  added: []
  patterns: ["a profile without an addendum reuses the derived changes of profiles 5 and 6", "replay of an earlier round in a throwaway clone", "register entries tied to the text by the check script"]

key-files:
  created:
    - .planning/reviews/2026-10-30-normative-spec-fix-round-7-register.md
  modified:
    - .planning/phases/04-independent-review/04-check-fix-round.sh
    - docs/method/GG-SAD_normative_method_specification.md

key-decisions:
  - "RH-C-001: the owner chose Close as failed; a cancel or supersede of a core change that waits on a soft failure closes it as failed, with the person's reason or else an automatic text; the full profile is not changed (FG-26)."
  - "RH-X-001: fixed as a repair; the first entry of a full change that the new action created is new, and a converted YAML state document starts with a migrate entry (FG-27)."
  - "RH-X-002: the owner chose Base revision only; only the ignore files as they were at the base revision hide a path (FG-28)."

requirements-completed: []  # REVIEW-01 and REVIEW-02 are not ticked; Phase 4 is open.

duration: "not measured; the plan spanned three executor sessions and an owner checkpoint run by the orchestrator"
completed: 2026-10-30
---

# Phase 4 Plan 26: Fix Round 7 Summary

PHASE NOT COMPLETE. The fix round script has a profile for round 7 and a replay of round 6. The owner chose how RH-C-001 and RH-X-002 are fixed, and RH-X-001 is fixed as a repair. The specification now carries the three fixes, with three new examples (AE-324 to AE-326), and a register records them. The text of round 6 is no longer the live text, so it must be approved again (plan 04-27), reviewed again (plan 04-28) and the new findings dispositioned (plan 04-29). The nine findings of round 6 without a disposition are untouched.

## Accomplishments

- Task 1 (tracer): profile 7 of the fix round check script (constants of the files of round 7, the static table of the changes FG-26 to FG-28, the decisions OD-12 and OD-13, the register skeleton, the mapping of FE7), no addendum code reached, and the replay of round 6 (checks R6-1 to R6-8). Commits `1974a72` and `bf020ed`.
- Task 2: owner checkpoint, run by the orchestrator; no commit.
- Task 3: three specification commits, one follow-up specification commit, the register and this summary.
- The nine findings of round 6 without a disposition (3 MAJOR, 3 MINOR, 3 INFO) are listed in the register under `Findings not touched`. The Requestor assessed no finding.

## Task Commits

1. Task 1: `1974a72` docs(04-26): add the round 7 profile to the fix round check script (tracer)
2. Task 1: `bf020ed` docs(04-26): add the replay of round 6 to the fix round check script
3. Task 3: `46a93ef` docs(04-26): fix-round cancel and supersede of a change that waits on a soft failure
4. Task 3: `f8c57a3` docs(04-26): fix-round first entry of a converted change
5. Task 3: `d1c9163` docs(04-26): fix-round revision of an ignore file in the scope rule
6. Task 3: `0abdab5` docs(04-26): fix-round example of a converted change keeps state.yaml in Section 25.3
7. Task 3: `69ed5f8` docs(04-26): add the fix register of round 7
8. Task 3: this summary, committed as `docs(04-26): summary`.

## Owner decisions

Channel (statement as the orchestrator gave it): the answers were given by the repository owner through the interactive question tool in this session (orchestrating session).

Response about the sections and the quoted sentences, as the orchestrator gave it: before each decision was asked, the owner was told the sections it edits and the quoted sentences of undispositioned findings near the edit sites (OD-12: RH-C-004 Section 23.4 line 2658; RH-X-003 Section 23.4 line 2673 and Section 24.1 line 3336; RH-C-003 Section 23.4 line 2674; OD-13: none). RH-X-001 was explained as a neutral fact before OD-12 (the reviewer's two wordings describe the same behaviour). The owner did not answer `owner wishes`, so FG-27 stays a repair with no question.

- OD-12 Soft failure (RH-C-001): label `Close as failed`; reason: none given.
  - Follow-up 1 (reason text of a failed outcome that a cancel or supersede causes), asked because the label leaves the point open: `Person's reason, else automatic`. The person's reason is used when given; otherwise an automatic text names the soft failure that was awaiting a decision.
  - Follow-up 2 (the full profile): `Only core changes`. The full rows (Sections 8.3 and 8.4 and the full statements of Section 24.7) stay, and the text says openly that core and full differ here, in the paragraph of Section 24.7 that covers both. Reason of both follow-ups: none given.
- OD-13 Ignore file (RH-X-002): label `Base revision only`; reason: none given.
- These choices carry no name and no date. They become final only through the owner approval of the exact new text in plan 04-27, which carries a name and a date typed by the owner.
- RH-X-001 (FG-27): a repair; no question was asked. The check on the two cases of the new example (flagged assumption A-4) found that the two wordings of the reviewer describe the same behaviour.

## What was changed

- FG-26 (Sections 23.2, 23.4, 24.7 and 25.1; example AE-324 after AE-43; AE-42 corrected to name a wait of kind `manual`).
- FG-27 (Section 25.1; example AE-325 after AE-285; Section 25.3 not edited).
- FG-28 (Section 24.5; example AE-326 after AE-307).
- The sweep for stale statements is listed per change, as nested bullets, in the Notes of the register. No quoted sentence of a finding without a disposition was reworded, and the register names none under the touched sentences.

## Verification

Task 1, before the change (stage level): `CHK --round 6 --stage dispositioned` ended `PASS D8 closure: not closable (fix pending)` and `RESULT: PASS`; `FIX --round 6 --stage dispositions`, `--stage approval-recorded`, `--stage approval-pending` and `--stage edits --complete` each ended `RESULT: PASS` (last PASS lines DA5, AR5, AP5 and FE7). After the change the same five commands printed byte-identical output, and the printers of rounds 2 to 6 printed byte-identical output.

Task 1, fixtures: a good register fixture ended `RESULT: PASS` with no DA line; the eight seeded failures printed FE5, FE5, FE7, FE5, FE5, FE3, FE5 and FE5; six usage cases and five replay-combination cases exited 2; a copy of the round-6 approval record with a foreign blob printed `FAIL R6-1`. The remaining matches of `grep -n '"$ROUND" -eq 6'` are all of the kind that selects a value that differs between profiles 6 and 7, at lines 562, 565, 585, 668, 994, 1119 and 1239 of the script.

Task 3, end of task, one at a time in the foreground, after the last commit:

- `FIX --round 7 --stage edits --complete`: PASS FE3, FE4, FE5, FE6, FE7, none for DA1 to DA5, `RESULT: PASS`, exit 0.
- `FIX --round 6 --stage dispositions`: `RESULT: PASS`.
- `CHK2 --final`: `RESULT: PASS`.
- `FIX --replay-round-6 --with-current-scripts`: `PASS R6-1` to `PASS R6-8`, `RESULT: PASS`.
- `FIX --replay-round-5 --with-current-scripts`: `PASS R5-8`, `RESULT: PASS`.
- `FIX --replay-round-4 --with-current-scripts`: `PASS R4-8`, `RESULT: PASS`.
- `FIX --replay-round-3 --with-current-scripts`: `PASS R3-8`, `RESULT: PASS`.
- `FIX --replay-round-2 --with-current-scripts`: `PASS R2-8`, `RESULT: PASS`.
- `FIX --replay-round-1 --with-current-scripts`: `PASS FR5`, `RESULT: PASS`.

The new text: blob `bfc0df6f96756c0c162d694067fd363e272d36b7`, SHA-256 `044fa076078f0f3794a216bdc96d7d54b0fc632404edbad31e2457fc0e9cc821`, 4950 lines (the text of round 6 was blob `2acdd0b38174b6fd8e8e3df9952063c74071c22a`, 4924 lines). The header (the first eight lines) is unchanged. The highest example id is AE-326; AE-324, AE-325 and AE-326 each occur at least twice. `git diff --name-only origin/main...HEAD` lists the specification and paths under `.planning/` only; nothing under src, .ggsad, specs, tests, AGENTS.md or CLAUDE.md changed. REVIEW-01 and REVIEW-02 are not ticked.

Live checks that fail by design from the first specification commit, because they pin the text of round 6: `FIX --round 6 --stage edits`, `--stage approval-pending` and `--stage approval-recorded`, and `CHK --round 6` in the stages pins, brief, reported and dispositioned (observed: `FIX --round 6 --stage approval-recorded` ends `RESULT: FAIL 3`, and `CHK --round 6 --stage pins` ends `RESULT: FAIL 6`). `FIX --replay-round-6 --with-current-scripts` keeps all of them checkable at the commit that holds the text of round 6, and the replays of rounds 1 to 5 keep the earlier rounds checkable. `FIX --round 6 --stage dispositions`, `FIX --round 7 --stage edits` and `CHK2 --final` do not pin the text of round 6 and stay valid.

Dispatch: sequential executors on the main working tree (workflow.use_worktrees is false)

The Python baseline was not run, because only `.planning/` and the specification changed.

## Deviations from Plan

1. [Rule 3 - Blocking] The constant `BRIEF6_PATH` is defined in the commit of the replay (part B) and not in the commit of the profile (part A), because it is used only by the replay and shellcheck reports an unused constant otherwise. Both commits are shellcheck-clean.
2. [Rule 2 - Missing critical] Under `--round 7` the addendum option is ignored and the addendum is read only when ADD_RND is greater than 0, so that a stray option cannot be read as an addendum.
3. [Rule 3 - Blocking] The example AE-325 does not name the file `state.yaml`, as the plan wrote it, because the drafting check allows that name only in Section 25.3. The example says a YAML state document. The fix is the separate commit `0abdab5`.
4. [Plan stop rule] The plan's wording for `Close as failed` left the reason text and the full profile open. The executor stopped at a checkpoint, as the plan requires, and the owner answered both points (see Owner decisions).
5. The recommendation sentence that the orchestrator may append to a question at the owner's standing request is not part of the recorded questions, which are the printed ones; this is a deviation from the rule that no option is recommended. The orchestrator's message to this executor does not say whether it appended one for OD-12, OD-13 or the two follow-up questions.

## Notes for plan 04-27

The approval code of the fix round script has the call `eargs=(--addendum "$ADDENDUM")` under `ROUND -ge 5` (in the code that runs the stage edits from the approval stage). Under `--round 7` the addendum is empty, and an empty value of `--addendum` exits 2. Plan 04-27 must make that argument conditional on ADD_RND being greater than 0. The stages approval-pending and approval-recorded and the approval printers exit 2 under `--round 7` until plan 04-27.

## Unverified

- The owner's answers reached this executor through the orchestrator's messages and cannot be independently checked from the repository. The checks prove structure, minimality and consistency with the register, not that any text is right. Which findings are correct is not assessed.
- The nine findings of round 6 without a disposition are untouched and are still open information (ids and counts are derived by the script: RH-A-001, RH-A-002, RH-B-001, RH-B-002, RH-B-003, RH-C-002, RH-C-003, RH-C-004, RH-X-003).
- The claim in the text of Section 24.7 that a `full` change that waits for a decision on a soft failure ends with the status `cancelled` or `superseded` restates the existing rule of Section 8.4 as read by the executor; no check proves it.
- REVIEW-01 and REVIEW-02 are supported only by the stated scope of the later review.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-27 (the approval of the exact new text). From the first specification commit of this plan the live checks that pin the text of round 6 fail by design, and the replay of round 6 keeps them checkable.
