---
phase: 04-independent-review
plan: 20
subsystem: independent-review-capture
tags: [independent-review, devin-cli, review-note, findings-table, consent-trail, round-5]
status: complete

requires: ["04-19"]
provides:
  - "Review check script with the round profile 5 (names and defaults only; the machinery of rounds 3 and 4 reused)"
  - "Brief of round 5, printed by the script from the round-1 brief"
  - "Review note of round 5 in reported form: six verbatim reports (RG-A, RG-B, RG-C, RG-D, RG-E, RG-X), the script-derived findings table, reviewer version and model, the consent trail, status lines, blocking count and one check warning row"
  - "Diff identity note sentence pointing at the review note of round 5, limited to the scope stated in that note"
affects: [04-21 owner dispositions]

requirements-completed: []  # REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close, when the dispositions of plan 04-21 support it.

actuals:
  tokens: 24000
  tasks: 3
  commits: 6

completed: 2026-10-29
---

# Phase 4 Plan 20: Round-5 Reviewer Runs and Capture Summary

PHASE NOT COMPLETE. Phase 4 stays in progress; no requirement is ticked.

Six separate Devin CLI sessions (model swe-2-medium, version 3000.4.25) each returned a report on the owner-approved text of fix round 5; the six reports are quoted verbatim in the review note of round 5 by the script printer, the findings table is derived by the script, and the check stage reported passes with 22 findings of which 1 is BLOCKING. The reports are usable.

## Accomplishments

- The note holds the six reports, the findings table with an empty Disposition column, the reviewer version and model, the consent trail rows, the status lines `Independent review: reported` and `Owner dispositions: pending`, `Blocking findings: 1`, and one `Check warning` row (RP6, see Scope). All six passes of the brief's table ran, so the note holds no scope sentence.
- The Requestor did not write, edit, filter, merge, summarise or re-rate any finding and did not assess whether any finding is correct.
- The diff identity note sentence now names the review note of round 5 and says the review is limited to the scope stated in that note; it was the only change to that file.
- One pass (RG-X) was run twice, because the first output failed the format check RP5 (a SUMMARY line over 200 characters); the first output was not used, and the report quoted in the note is that of the second run.

## Task Commits

1. Task 1 (tracer): `eb9531c` (round profile 5, machinery of round 4 reused; the script), `b206c33` (brief of round 5).
2. Task 2: consent checkpoint, no commit.
3. Task 3: `11ff3e3` (note in pending form), `1de57ad` (the reports and the findings table), `a106323` (identity note sentence), and this summary, committed as `docs(04-20): summary`.

## Consent trail

- Statement of channel: the answers were given by the repository owner through the interactive question tool in the orchestrating session and relayed verbatim to the executors; no default or auto-advance was applied.
- Passes chosen by the owner: all six (RG-A, RG-B, RG-C, RG-D, RG-E, RG-X). The owner's answers to the six part questions, verbatim, in table order: RG-A `Read it`; RG-B `Read it`; RG-C `Read it`; RG-D `Read it`; RG-E `Read it`; RG-X `Read it`. The recommendation shown with the questions for RG-A, RG-D and RG-E was Skip it; the owner chose Read it for each. The six questions were asked in two tool calls of three.
- Server question and answer: May I switch off four of your Devin add-on servers (GitKraken, Notion, Codacy and Linear) while the review runs, and switch them back on afterwards? Answer: `Switch off, then back on`. The orchestrating session switched the four off and verified it with `devin mcp list` (mcp-linear and pycharm stayed enabled); after the run phase it switched the four back on, and `devin mcp list` then showed none disabled.
- Run-set consent question, as the script prints it: May I send the test run and the six review passes RG-A, RG-B, RG-C, RG-D, RG-E and RG-X (run set 196dfab7a957, model swe-2-medium) to Devin now? Sending cannot be undone, and no run is repeated without asking you again.
- Owner's answer, verbatim: `Consent`
- Run set: 196dfab7a957. Model: swe-2-medium.
- The plain residue of `sed` and `awk` (they can start other programs and write files anywhere the account may write; the checks see only the repository, the inputs, the decoy and the output folder) and the other limits were told to the owner before the consent question.
- Second consent, for the repeat of RG-X: the owner was told which run, the kind of problem (format, check RP5), the usable reports, that a repeat may return different findings, and that the findings of the unusable output would not be recorded. A first three-option question (Keep this report / Run once more / Stop) was answered `Run once more`; it was not the wording of the plan, so the plan's question was asked: May I run RG-X once more, because its output was unusable for reason its SUMMARY line exceeded the 200-character limit (format, check RP5)? Sending cannot be undone, and a usable report is never replaced. Options `Run once more` and `Stop`; answer `Run once more`. Pass RG-X therefore ran twice; the first output failed RP5 and was not used; the second run may return different findings from the first.

## Result

| Pass | Findings | BLOCKING | MAJOR | MINOR | INFO |
|---|---|---|---|---|---|
| RG-A | 6 | 1 | 0 | 4 | 1 |
| RG-B | 4 | 0 | 0 | 3 | 1 |
| RG-C | 2 | 0 | 1 | 1 | 0 |
| RG-D | 1 | 0 | 0 | 1 | 0 |
| RG-E | 4 | 0 | 0 | 2 | 2 |
| RG-X | 5 | 0 | 1 | 4 | 0 |

- Totals (from `bash CHK --round 5 --print-counts`, re-derived at the end of the task): total=22 blocking=1 major=2 minor=15 info=4.
- BLOCKING finding id: RG-A-001 (Section 4.3, line 303). The reviewer's summary: "The reserved-name check compares the whole identifier, so `nul.txt` or `con.x` passes the rule yet is still a reserved device name on Windows."
- Reviewer: Devin CLI version 3000.4.25, model swe-2-medium. Each report's identity statement is the reviewer's own.
- No assessment of any finding is made here. Plan 04-21 asks the owner to disposition each BLOCKING finding.

## Scope of the review

Passes run: RG-A RG-B RG-C RG-D RG-E RG-X
Passes not run: none
Lines printed by `bash CHK --round 5 --print-pass-scope` for the run set:
- `Run set passes: RG-A RG-B RG-C RG-D RG-E RG-X`
- `Read only by the cross-check pass RG-X: none`
Changed places read by no pass of the run set: none

All six passes of the brief's table ran, so every section has a pass of its own and the whole text was also read by the cross-check pass. By the printed counts the passes RG-A (lines 1-1126), RG-D (lines 3153-4003) and RG-E (lines 4004-4898) hold no changed line between the text of round 4 and the approved text (stage reported: `WARN RS1` for each, not counted). The pass RG-B holds 12 hunks and 86 added lines, RG-C 3 hunks and 10 added lines, and RG-X 15 hunks and 96 added lines. Places that did not change since round 4 were last read by the passes of round 4 that covered them; how closely is not stated here.

Check warning (row of the note): `WARN RP6 RG-A: the quote of reference 8 occurs in SPEC but not between the lines 908-908`. The quote of that reference occurs in the text, but not between the lines the reviewer named.

Commands the reviewer may run: ls, cat, head, tail, wc, grep, diff, sha256sum, certutil -hashfile, Get-FileHash, Compare-Object, sed, awk (thirteen read-only commands; the same configuration was used for the test run and for every pass).

## Verification

Each of the following was run once, one at a time in the foreground, after the identity commit:

- `bash 04-check-fix-round.sh --replay-round-3 --with-current-scripts` last lines: `PASS R3-8 ...` then `RESULT: PASS`.
- `--replay-round-2 --with-current-scripts` last lines: `PASS R2-8 ...` then `RESULT: PASS`.
- `--replay-round-1 --with-current-scripts` last lines: `PASS FR5 ...` then `RESULT: PASS`.
- `--replay-round-4 --with-current-scripts` last lines: `PASS R4-8 ...` then `RESULT: PASS`.
- `bash 02-check-normative-diff.sh --final` ends `RESULT: PASS`.
- `bash 04-check-independent-review.sh --round 5 --stage reported` ends `RESULT: PASS`; the checks RP1 to RP9 for each of the six quoted reports, F1 (22 findings) and F2 (blocking count 1) are PASS; its warnings are the three RS1 lines and the RP6 line named above.
- Earlier in the task: `bash 04-check-fix-round.sh --round 5 --stage approval-pending` and `--stage approval-recorded` ended `RESULT: PASS` after the identity change.
- Each report passed `--verify-out` and `--report-file` before the next pass was started.
- Containment after each run: `git status --short` empty; the specification blob equal to the result blob of the approval record; the diff to `origin/main` lists only the specification and paths under `.planning/`; `--verify-snapshot` of the inputs passed; the output directory held exactly the one report file; the decoy token was absent from the report and the captured output; the decoy directory and the configuration directory were unchanged.
- Comparison of each quoted block with the held report after the normalisation (CR bytes deleted, each tab replaced by four spaces): identical for the six reports.
- `git status --short` was empty after the checks and before this summary.
- The Python baseline was not run because only `.planning/` changed.

## What Devin loaded in the inputs directory

One global rule was listed and its file is empty. Three user skills were listed. Two servers that the command line cannot switch off (mcp-linear and pycharm) stayed enabled during the runs; the four servers named in the consent were off. No always-on context was found beyond that residue. The configuration of Devin outside the minimal reviewer configuration was not edited.

## Observations (from the runs only; observations, not proofs)

- After each run the repository, the specification blob and the inputs were unchanged and the output directory held only the report file; the decoy token did not appear in any report or captured output. This does not prove the configuration is honoured.
- The reports were produced by the call form of plan 04-08. The reliability of the call across sessions is not shown.

## Deviations from Plan

**1. [Method] Question wording.** The six part questions were asked in two tool calls of three, not one call per part. At the owner's standing request recommendation sentences were appended to the part, server, consent and repeat questions; they are not recorded as part of the questions.

**2. [Method] Repeat question.** A three-option question preceded the plan's own `Run again` question; one of its options (Keep this report) would have required relaxing check RP5, which the plan does not provide. The plan's question was then asked and answered as recorded above.

**3. [Method] Continuation prompts.** A first continuation prompt lacked the owner's original task-2 answers; that executor halted before running anything; a second prompt carried them.

**4. [Method] End-of-task checks.** The end-of-task replays were interrupted once when the system ran short of memory and background shells were reaped; they were re-run one at a time in the foreground by the executor that wrote this summary.

**5. [Method] Run scripts.** The runs were started from short helper scripts outside the repository, not from the committed tree.

Setup and run details that the plan keeps out of committed files were told to the owner in the conversation.

## Unverified

- The identity of the reviewer is its own statement in each report.
- The owner's answers reached the executors through the orchestrator's messages; the repository cannot show who answered.
- The reports are the reviewer's; none is assessed here. That the passes read their ranges as closely as the brief asks is not shown, and thoroughness over the length of the text cannot be shown.
- What the reviewer opened beyond its directory is only its self-report; the repository cannot prevent reads outside the working directory if the tool ignores the configuration. That the configuration is honoured is not proven.
- The reviewer ran with containment checks that cannot see everything `sed` and `awk` could do: `awk` can start other programs and write files and `sed` can run commands and write files, so that a reviewer that disobeyed the brief could in principle run other programs and write files anywhere the Windows account may write; no check of this plan sees that outside the repository, the inputs, the decoy and the output directory (the brief's instruction to modify nothing is an instruction, not a barrier). The owner was told this before the consent question.

## Phase-close facts

- REVIEW-01 and REVIEW-02 are not ticked and Phase 4 is not marked complete.
- Plan 04-21 asks the owner to disposition each BLOCKING finding (RG-A-001).
- REVIEW-01 is supported only by the stated scope.

Dispatch: sequential executors on the main working tree (workflow.use_worktrees is false)

## Self-Check

Passed: the reported stage, the replays of rounds 4, 3, 2 and 1 with the current scripts, `CHK2 --final`, the six block comparisons, the containment checks after each run, and an empty working tree before this summary.

REENABLE-SERVERS: yes
