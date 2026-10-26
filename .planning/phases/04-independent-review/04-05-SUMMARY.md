---
phase: 04-independent-review
plan: 05
subsystem: independent-review-fix-round
tags: [independent-review, fix-round, check-script, replay, owner-direction]
status: complete

requires: ["04-04"]
provides:
  - "Check script of the fix round with the stage state (ST1, fact line ST2) and the replay of the three round-1 checks (FR1 to FR5)"
  - "Phase 2 drafting check whose C1 also accepts the commit subjects of the fix round"
  - "Record of the deviation by owner direction: the decision checkpoint was removed from this plan"
affects: [04-06, 04-07, 04-08, 04-09]

actuals:
  tokens: 12000
  tasks: 3
  commits: 4

tech-stack:
  added: []
  patterns: ["throwaway local clone outside the repository for replaying earlier evidence", "one added family of accepted commit subjects instead of loosening a check"]

key-files:
  created:
    - .planning/phases/04-independent-review/04-check-fix-round.sh
    - .planning/phases/04-independent-review/04-05-SUMMARY.md
  modified:
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh

key-decisions:
  - "The fix round runs without a decision checkpoint, by owner direction (see Deviation by owner direction); no decision record exists."

requirements-completed: []  # plan 04-05 carries REVIEW-02, which stays open; REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close only.

duration: "not measured; tasks 1 and 2 and task 3 were run by separate executors"
completed: 2026-10-26
---

# Phase 4 Plan 05: Fix Round Mechanism Summary

PHASE NOT COMPLETE. This plan opened the fix round that follows the independent review of the proposed normative method specification: it built the check script of the round (the state of the text and the replay of the round-1 checks at the commit that holds the round-1 text) and made the Phase 2 drafting check accept the commit subjects of the fix round. It edits no specification text, creates no decision record and asked the owner nothing. The specification still holds the text of round 1 (blob ed758c46d5ac901359ab2c0df8e437ef89fed0f1, 4649 lines), so every round-1 live check still passes.

## Accomplishments

- The check script `04-check-fix-round.sh` has the stage state (ST1: the approval record and the disposition record of round 1 pin the same blob, SHA-256 and line count; ST2: a fact line that says whether the specification equals the text of round 1) and `--replay-round-1`. The replay finds the newest commit reachable from HEAD at which the specification holds the round-1 blob, makes a throwaway local clone of the repository outside the repository, checks that commit out detached and runs there the drafting check with `--final` (FR2), the owner approval check in stage recorded (FR3) and the review check in stage dispositioned (FR4). With `--with-current-scripts` the current versions of the three scripts are run there too (FR5), which shows that a later extension of a script still validates the round-1 evidence. This is what keeps round 1 checkable after the first specification commit of plan 04-06, from which the live checks that pin the round-1 text fail by design.
- The Phase 2 drafting check accepts, in C1, one more family of commit subjects: `docs(04-NN): fix-round <text>`. The family names no requirement id and counts toward none, like the two header subjects. No other check, pattern or message of that script changed.
- One defect found by the seeded runs of task 2 was fixed in the script of the round (commit 6ee27ba).

## Task Commits

1. Task 1 (tracer): `10197f2` docs(04-05): add the fix round check script with the state, replay and decisions stages (tracer)
2. Task 2, part A: `8837727` docs(04-05): accept fix-round commit subjects in the drafting check (C1)
3. Task 2, part B: `6ee27ba` docs(04-05): fix the fix round check script after the seeded runs
4. Task 3: this summary, committed as `docs(04-05): summary` (the state files follow in their own commit).

## Deviation by owner direction

Tasks 3 and 4 of this plan as first written (a checkpoint with five design questions D-1 to D-5, and a decision record with a check stage that validates it) were not carried out. The repository owner, shown that checkpoint through the orchestrating session, said that it was too complex and chose, through the interactive question tool:

- scope: all eleven findings as dispositioned (six BLOCKING, five MAJOR);
- mode: the option labelled `You review a diff` (the Requestor picks the smallest, most consistent fix for each problem and shows the owner the actual before-and-after text with a one-line plain explanation each; the owner approves it once or says what to change);
- re-review: Devin looks again with a smaller run set than the first review. The owner fixed its size later, when plan 04-08 was sized: a test run, the pass RR-A (the header and Sections 1 to 8), the pass RR-B (Sections 9 to 22) and the cross-check pass RR-X (the whole text, read across sections). The passes RR-C (Section 23), RR-D (Section 24 up to the end of 24.5) and RR-E (Sections 24.6 to 24.10 and Section 25) are not run, although their ranges hold changed lines, so Sections 23 to 25 are read only by RR-X. Adding any of them is the owner's call, made through a revision of plan 04-08;
- overall: a lighter round.

The earlier plans 04-06 to 04-11 were replaced by 04-06 to 04-09. No decision file exists. The five points that were to be decided are drafted in plan 04-06 as the Requestor's picks, marked `my choice` in the register, shown to the owner in plan 04-07 as before-and-after text, and changeable there. A pick is a proposal, never a decision.

Channel, as the orchestrator relayed it: the owner's choices were given in the orchestrating session through the interactive question tool and reached this executor in the orchestrator's message. The repository cannot show who answered.

## Parts of the script left unused

The script holds parts that this plan no longer uses and that no later plan calls:

- the stage decisions (`--stage decisions`) and its checks FD1 to FD8;
- the options `--decisions`, `--print-decision-questions` and `--print-decisions-skeleton`;
- the helper `decision_data` with the fixed decision texts;
- the default path of the decision record.

They are not deleted: the script passed its seeded runs with them in place, nothing depends on them, and removing them would be one more change to a proven script with no benefit. They run only when called; the default stage and the replay never touch them. `bash FIX --stage decisions` exits 2 because no decision record exists, by design (observed: the message is that the record cannot be read, exit 2).

## Verification

Baseline of the round-1 chain, run for task 3 (last lines):

- `bash 04-check-fix-round.sh --stage state` ends `RESULT: PASS`; ST1 passes (blob, SHA-256 and 4649 lines pinned identically by both records) and the output holds `STATE: the specification equals the text of round 1 (all round-1 live checks apply)`.
- `bash 04-check-fix-round.sh --replay-round-1 --with-current-scripts` ends `RESULT: PASS` with PASS FR1, FR2, FR3, FR4 and FR5.
- `bash 02-check-normative-diff.sh --final`, `bash 03-check-owner-approval.sh --stage recorded` and `bash 04-check-independent-review.sh --stage dispositioned` each end `RESULT: PASS`.
- `bash -n` and `shellcheck` on `04-check-fix-round.sh` and on `02-check-normative-diff.sh` exit 0.
- `git worktree list | wc -l` prints 1.
- `git hash-object docs/method/GG-SAD_normative_method_specification.md` prints `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`, the round-1 blob; the specification is untouched.
- The C1 extension changed only the C1 block and its usage comment: `git diff 8837727~1 8837727 --stat` lists the one file, `.planning/phases/02-normative-drafting/02-check-normative-diff.sh`, with 6 insertions and 2 deletions.
- No decision file exists: `.planning/reviews/2026-10-26-normative-spec-fix-round-decisions.md` is absent.
- The per-case results of the seeded runs of tasks 1 and 2 were reported in the handovers of those tasks and are not restated here.

## Deviations from Plan

None beyond the deviation by owner direction above. Task 3 was run as revised; tasks 1 and 2 were already executed and were not repeated.

## Known Stubs

None.

## Unverified

- The owner's direction, including the later choice of the smaller run set of the re-review, reached this plan through the orchestrator's message and cannot be checked from the repository.
- The replay proves the round-1 evidence against the commit it finds, not against a later text.
- The checks prove structure and consistency, not that any text is right.
- Whether the lighter round satisfies the hard gate of Phase 4 for the owner is for the owner to judge at the approval of plan 04-07 and the dispositions of plan 04-09; nothing here decides it.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-06. From the first specification commit of that plan, the live round-1 checks that pin the round-1 text (the Phase 3 check in stage recorded and the Phase 4 check in the stages that use the round-1 defaults) fail by design; `bash 04-check-fix-round.sh --replay-round-1` keeps round 1 checkable, and the Phase 2 check with `--final` stays valid for the fix-round commits through the accepted subject family.

## Self-Check: PASSED

- Files exist: `04-check-fix-round.sh`, `02-check-normative-diff.sh` and this summary.
- Commits `10197f2`, `8837727` and `6ee27ba` exist on gsd/v1.1-executable-core.
- The baseline lines above ended `RESULT: PASS`; the specification blob is unchanged; no decision file exists.
