---
phase: 04-independent-review
plan: 18
subsystem: independent-review-fix-round-5
tags: [independent-review, fix-round, owner-disposition, owner-decision, normative-specification, check-script, round-5]
status: complete

requires: ["04-17"]
provides:
  - "Fix round check script with the profile of round 5 (decision questions OD-6 to OD-9, register skeleton with a derived number of changes, stage edits with the addendum checks DA1 to DA5 and FE3 to FE7, stage dispositions, addendum printer) and the replay of round 4"
  - "Disposition addendum of round 4: the owner's dispositions of seven further findings, all fix"
  - "Specification with the seven fixes the owner chose: ten new acceptance examples (AE-311 to AE-320) and three wording repairs"
  - "Register of round 5 with the options offered, the owner's choices, before and after, and the sweep of stale statements"
affects: [04-19 (diff identity again, approval stages and packet of profile 5, approval of the exact new text), 04-20, 04-21]

actuals:
  tokens: 27000
  tasks: 3
  commits: 13

tech-stack:
  added: []
  patterns: ["profile variables with round 2 as the default", "replay of an earlier round in a throwaway clone", "disposition addendum that supplements an immutable record", "owner choice tied to the offered options by a check", "derived number of changes from the dispositions on record"]

key-files:
  created:
    - .planning/reviews/2026-10-28-normative-spec-review-disposition-addendum-round-4.md
    - .planning/reviews/2026-10-28-normative-spec-fix-round-5-register.md
  modified:
    - .planning/phases/04-independent-review/04-check-fix-round.sh
    - docs/method/GG-SAD_normative_method_specification.md

key-decisions:
  - "Dispositions: RF-B-004, RF-X-002, RF-X-003, RF-X-004 (MAJOR) and, answered at the owner's choice, RF-C-001, RF-C-002, RF-B-001 (MINOR) all Fix, reason none given."
  - "OD-6 (RF-X-001 and RF-B-004), OD-7 (RF-X-002), OD-8 (RF-X-003), OD-9 (RF-X-004): Add examples, reason none given. They become final only through the owner's approval of the exact text in plan 04-19."

requirements-completed: []  # REVIEW-02 stays open: the fixes void the approval of the text; REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close only.

duration: "not measured; the plan spanned an implementation session (task 1), an owner checkpoint run by the orchestrator and a continuation session (task 3)"
completed: 2026-10-28
---

# Phase 4 Plan 18: Fix Round 5 Summary

PHASE NOT COMPLETE. The BLOCKING finding of the review of round 4 (RF-X-001) and six further findings that the repository owner dispositioned fix (RF-B-004, RF-X-002, RF-X-003, RF-X-004, RF-C-001, RF-C-002, RF-B-001; seven findings in the addendum, eight in all) are fixed in the specification the way the owner chose, and the changes are recorded in a register. The fixes void the approval of the text of round 4, so the new text must be approved (plan 04-19), reviewed again (plan 04-20) and the new findings dispositioned (plan 04-21). The 26 other findings of round 4 are untouched and still open information (MAJOR 6, MINOR 17, INFO 3). Phase 4 stays open and nothing is ticked.

## Accomplishments

- The fix round script has the profile of round 5: `--round 5`, `--print-decision-questions` (OD-6 to OD-9, two one-sentence options each), `--print-register-skeleton` (the number of changes is derived from the dispositions in the record and the addendum), `--print-addendum-skeleton` with `--findings`, the stage `dispositions` (checks DA1 to DA5, which never read the live specification), the stage `edits` with the addendum checks first and FE3 to FE7, and the replay of round 4 (`--replay-round-4`, checks R4-1 to R4-8). Round 2 is the default; profiles 3 and 4 behave as before.
- The disposition addendum of round 4 records the owner's answers for seven findings with the question as the review check script prints it. The record and the note of round 4 are not edited.
- FG-16 (RF-X-001, RF-B-004), Sections 16.1 and 16.4: two new examples, AE-311 (the gate conditions, the allowed paths and the evidence commands of a change specification) and AE-312 (the evidence lists a gate that could not be evaluated and the coverage table names the evidence commands), each cited by a See sentence. Sections 16.2 and 16.3 hold only a template and no rule sentence and got none.
- FG-17 (RF-X-002), Sections 13.1 to 13.3: AE-313 (conflict with an accepted ADR), AE-314 (deviation from the specification) and AE-315 (breaking change without approval).
- FG-18 (RF-X-003), Sections 14.3 to 14.5: AE-316 (review cycle), AE-317 (blocking finding blocks until dispositioned) and AE-318 (review finding is not a requirement, eight-field evidence record).
- FG-19 (RF-X-004), Section 19.1: AE-319, one example that shows all eight prohibitions together.
- FG-20 (RF-C-001), Section 23.6: the first sentence now says the evaluation stops once the results of a group decide the requested action (Section 24.2). Repair; no example.
- FG-21 (RF-C-002), Section 23.3: one sentence added to the bullet on `retry_limit` (the identifier named by `gate` MUST be that of a `check` done gate of the same change, a definition naming none is rejected) and AE-320 (placed after AE-273). The sentence that the finding quotes is not reworded. Repair.
- FG-22 (RF-B-001), Section 12: the clause that cites the earlier text of the method is removed from the sentence on a retry limit and nothing else. Repair.
- The register records, per change, the options that were offered, the choice as relayed (or the statement that none was open), a before and an after fragment, and the sweep of stale statements. The Requestor did not assess any finding.

## Task Commits

1. Task 1, part A (tracer): `71f0d1d` docs(04-18): add the round 5 profile to the fix round check script (tracer)
2. Task 1, part B: `6dad03c` docs(04-18): add the disposition addendum of round 4 to the fix round check script
3. Task 1, part C: `88bd7ff` docs(04-18): add the replay of round 4 to the fix round check script
4. Task 2: owner checkpoint run by the orchestrator, no commit
5. Task 3: `f3ec822` docs(04-18): record the owner dispositions of the related findings of round 4
6. Task 3: `dcae330` docs(04-18): fix-round acceptance examples for the minimum templates
7. Task 3: `b672c30` docs(04-18): fix-round acceptance examples for the ADR conflict rules
8. Task 3: `35dd076` docs(04-18): fix-round acceptance examples for the review cycle
9. Task 3: `d286cd1` docs(04-18): fix-round acceptance examples for the agent prohibitions
10. Task 3: `60a3fec` docs(04-18): fix-round stop rule of the core evaluation
11. Task 3: `429c7f6` docs(04-18): fix-round check gate named by a retry limit
12. Task 3: `12a59b4` docs(04-18): fix-round clause that cites the earlier text
13. Task 3: `0f68dfa` docs(04-18): add the fix register of round 5
14. Task 3: this summary, committed as `docs(04-18): summary`.

## Owner dispositions and decisions

- Statement of channel as the orchestrator gave it: the answers were given by the repository owner through the interactive question tool (AskUserQuestion) in the orchestrating session and relayed verbatim by the orchestrator. Before the questions the orchestrator explained, in plain words and marked as its own explanation, that the reviewer returned 34 findings with one BLOCKING (RF-X-001, already Fix), that RF-B-004, RF-X-002, RF-X-003 and RF-X-004 are about rules without worked examples, what Fix, Accept, Defer and Reject lead to, that nothing is sent anywhere or edited by the questions, and that the other findings need no answer.
- Dispositions, one question per finding, the question text being the printed text of `bash CHK --round 4 --print-disposition-skeleton --finding ID` (they are in the addendum word for word):
  - RF-B-004 (MAJOR): `Fix`; reason: none given.
  - RF-X-002 (MAJOR): `Fix`; reason: none given.
  - RF-X-003 (MAJOR): `Fix`; reason: none given.
  - RF-X-004 (MAJOR): `Fix`; reason: none given.
  - RF-C-001 (MINOR): offered neutrally with the question `Do you want to answer this finding now?`; the owner answered `Answer it now`; then `Fix`; reason: none given.
  - RF-C-002 (MINOR): the same offer; `Answer it now`; then `Fix`; reason: none given.
  - RF-B-001 (MINOR): the same offer; `Answer it now`; then `Fix`; reason: none given. Before it was asked, the orchestrator told the owner as a fact that the clause was added in round 4 because the owner chose `Soft, said openly` for the retry limit.
  - No other finding was asked about.
- Design decisions, each asked alone, the option labels as `bash FIX --round 5 --print-decision-questions` prints them:
  - OD-6 Templates (RF-X-001 and RF-B-004): `Add examples`; reason: none given.
  - OD-7 ADR rules (RF-X-002): `Add examples`; reason: none given.
  - OD-8 Review rules (RF-X-003): `Add examples`; reason: none given.
  - OD-9 Agent bans (RF-X-004): `Add examples`; reason: none given.
  - No `Say none needed`, no `owner wishes`.
- Name: `AndreHahm`. Date: `2026-10-28`. Both were picks from candidates that the owner asked the orchestrator to offer: the free-text replies came back twice each only as the option label `Type it under Other`, the question was not sent a third time, the owner was asked through the tool whether candidates should be offered and answered `Offer candidates` for both. The name candidates were `AndreHahm` and `Andre Hahm`; the date candidates were 2026-10-28 and 2026-10-29. The addendum states this in its Owner reply row. The date is not earlier than the Owner disposition date of the record of round 4 (2026-10-28).
- Statement of the response about the quoted sentences near the edit sites, as the orchestrator gave it: before each design decision was asked, the owner was told as facts (OD-6) that the sentence in Section 16.1 at line 1830 says the Flow Gates conditions plus the scope are the gate definitions fixed at approval, and (OD-7, OD-8, OD-9) that no other open finding quotes a sentence in Section 13, in Sections 14.3 to 14.5 or in Sections 19 and 19.1. Before OD-6 the owner was also told that SPEC-14 says each `full` rule has an acceptance example like the `core` rules have, that `Say none needed` would change only the specification text and leave the requirement text as it is, and that the design choices carry neither name nor date and become final through the owner's approval of the exact text in plan 04-19. The longer list of quoted sentences near the edit sites (RF-A-003 line 577, RF-X-005 line 573, RF-B-005, RF-B-006, and the own quotes of RF-C-001 and RF-C-002) was not read out to the owner (see Deviations).
- These choices carry no name and no date of their own. They become final only through the approval of the exact text in plan 04-19, which carries a name and a date typed by the owner.
- At the owner's standing request the orchestrator appended the sentence `(My recommendation: X.)` to owner questions (process reasons only on the disposition questions, a full recommendation on the design questions). That sentence is not part of the recorded questions in the addendum or the register, and it deviates from the plan's rule that no option is recommended; the recommendation is the orchestrator's judgment of process and never the reviewer's verdict.

## Verification

- Task 1, re-checked in this session: `bash -n FIX` and `shellcheck FIX` exit 0, no carriage return in the script, `--round 5 --print-decision-questions` prints four blocks `OD-6` to `OD-9` and eight option lines, and `--round 5 --print-addendum-skeleton` prints a block for each of the four default findings. The earlier executor reported that the round-4 stages (`CHK --round 4 --stage dispositioned`, `FIX --round 4 --stage approval-recorded`, `approval-pending` and `edits --complete`) ended `RESULT: PASS` before the change, that the printers of profiles 2 to 4 were byte-identical before and after, that the good register and addendum fixtures passed, that the seeded failures printed the named ids (seven for the register stage, ten for the addendum stage, R4-1 for the replay) and that the usage cases exit 2; those fixture runs were not repeated here. The number of rows of the note of round 4 with an empty Disposition cell, held as a constant by the script, is 33 (34 findings, one with a disposition); the stage derives 26 after the addendum.
- Precondition of task 3: `git status --short` was empty, the blob of the specification was fca228479a34e228785f4c0b100da3c6745ada0a, the addendum and the register did not exist, and `bash FIX --round 4 --stage edits --complete` ended `RESULT: PASS`.
- After the last specification and register commit (all commands run on the committed state):
  - `bash FIX --round 5 --stage dispositions` ends `RESULT: PASS` with `PASS DA1` to `PASS DA5` (seven blocks).
  - `bash FIX --round 5 --stage edits --complete` ends `RESULT: PASS`, exit 0, with `PASS DA1` to `PASS DA5` and `PASS FE3` (the header and the 26 undispositioned findings are untouched, every changed line lies in a listed section), `PASS FE4`, `PASS FE5` (seven drafted entries), `PASS FE6` (the Phase 2 check) and `PASS FE7`.
  - `bash CHK2 --final` ends `RESULT: PASS`.
  - `bash FIX --replay-round-4 --with-current-scripts` ends `RESULT: PASS` and holds `PASS R4-1` to `PASS R4-8`.
  - `bash FIX --replay-round-3 --with-current-scripts` ends `RESULT: PASS` and holds `PASS R3-1` to `PASS R3-8`.
  - `bash FIX --replay-round-2 --with-current-scripts` ends `RESULT: PASS` and holds `PASS R2-1` to `PASS R2-8`.
  - `bash FIX --replay-round-1 --with-current-scripts` ends `RESULT: PASS` and holds `PASS FR1` to `PASS FR5`.
  - `git worktree list` prints one line and `git status --short` was empty before this summary was written.
- The blob of the specification is now 3c0f689e2464b3a9fc8fcce5c1fc7ef55e06bfd1 (4898 lines); its first eight lines (the header) are identical to those of the text of round 4. The highest example id is AE-320, as the register ends its run. Each of the seven specification commits lists only the specification; the addendum commit lists only the addendum; the register commit lists only the register. The addendum and the register hold no fill marker and none of the banned path or temporary-file words.
- `git diff --name-only a43ee82 HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; no requirement is ticked (`grep -c '^- \[x\] \*\*REVIEW-0' .planning/REQUIREMENTS.md` prints 0).

## Sweep results (short)

- FG-16: Sections 16.1 and 16.4 gain a See sentence and an example each. The quoted sentences of Section 16.1 (the gate definitions sentence and the sentence on the requirement identifiers and evidence command lists), the template of Sections 16.2 and 16.3, Section 5.6, and Sections 24.1, 24.2 and 24.9 stay true.
- FG-17: Sections 13.1, 13.2 and 13.3 gain a See sentence and an example each; Sections 12.1, 12.2, 19, 19.1 and 20 stay true.
- FG-18: Sections 14.3, 14.4 and 14.5 gain a See sentence and an example each; Section 14.2, Section 20 and the Pair Review parts of Sections 16.1 and 16.4 stay true.
- FG-19: Section 19.1 gains a See sentence and an example; Section 19 (the algorithm steps and AE-270), Section 13.3 and Section 20 stay true.
- FG-20: Section 23.6 first sentence only; the group sentence of Section 23.6, the steps 1 to 5, AE-53 to AE-55 and the paragraph on groups of Section 24.2 stay true. Section 8.5 (full profile) has the sentence "Evaluation MUST stop as soon as a gate determines the requested action's outcome"; it is not named by the finding and is not edited.
- FG-21: Section 23.3 gains one sentence in the bullet on `retry_limit` and AE-320; the other sentences of Section 23.3, AE-273, Section 24.2 (retry limit), Section 12 and Section 12.1 stay true.
- FG-22: one clause removed in Section 12; the sentence before it, the rest of the same sentence (word for word), and Section 12.1 stay true; no other passage holds the words of the removed clause.

## Dispatch

Dispatch: sequential executors on the main working tree (workflow.use_worktrees is false).

The Python baseline (uv, ruff, ty, pytest) was not run, because only .planning/ and the specification changed.

## Deviations from Plan

**1. [Process] Optional offers and their disposition questions were batched.** The plan asks one question at a time. The orchestrator put the three offers (`Do you want to answer this finding now?` for RF-C-001, RF-C-002 and RF-B-001) in one tool call as three questions, and the three disposition questions of the optional findings in one tool call as three questions. No question text or option changed.

**2. [Channel] Name and date are picks from candidates.** The plan forbids suggesting a name or taking a date from the session; the free-text replies came back twice each only as the option label, the owner asked for candidates and picked `AndreHahm` and `2026-10-28` in the tool. The addendum says so in its Owner reply row, in the wording used for such a pick in the record of round 4.

**3. [Process] Recommendation sentences in the owner questions.** See the last bullet of the section on owner dispositions and decisions.

**4. [Process] The quoted sentences near the edit sites were told only in part.** The plan (step 4 of the checkpoint) asks that the quoted sentences near the edit sites be told to the owner as facts before each decision, with finding id, section, line and a plain phrase. The orchestrator told only the facts listed in the section on owner dispositions and decisions; the longer list (RF-A-003 line 577, RF-X-005 line 573, RF-B-005, RF-B-006, and the own quotes of RF-C-001 and RF-C-002) was not read out. No edit rewords a quoted sentence of a finding without a disposition (FE3 passes), so the stop question was never needed and the register names no touched sentence.

**5. [Rule 1 - Bug] `CHK --round 4 --stage reported` no longer passes.** Step (2) of task 3 says to run it before filling the Check results row and that it still passes at this state. It ends `RESULT: FAIL` with the checks T1 (the status line of the note now reads that the owner dispositions are recorded) and F1 (the Findings table now holds the Disposition cell of RF-X-001), which is the state plan 04-17 left on purpose; the stage `dispositioned` is the one that fits. It ended `RESULT: PASS` before the addendum was written, and the Check results row of the addendum says exactly that (the stage dispositioned check, before this addendum was written). The row is free text and no check compares it to a fixed sentence.

**6. [Rule 1 - Bug] FE3 in profile 5 does not look up one quoted sentence by letter case.** (Task 1.) The quote of RF-C-002 in the note starts in lower case ("the member `gate` ...") while the text has "The member `gate` ..."; it is the only one of the 33 quotes that is not a substring of the text. In profile 5 FE3 does not look up a quoted sentence that the text does not hold; rounds 3 and 4 are unchanged. The difference is letter case only. Since RF-C-002 has a disposition fix, its quote is exempt anyway.

**7. [Process] Commit split of task 1.** The checks DA1 to DA5 and the addendum printer are in the first commit because the stage `edits` runs them first; the second commit holds the stage `dispositions` and its usage text; the third the replay.

**8. [Reading] No MUST, MUST NOT or SHOULD in Sections 16.1 to 16.4.** The plan's rule for the label `Add examples` speaks of subsections that hold a rule written with MUST, MUST NOT or SHOULD. The four subsections hold none of these words; I read as rules the prose sentences that state what the template requires (the gate definitions, the allowed path list, the evidence command lists, the listing of a gate that could not be evaluated, the Evidence column). Sections 16.2 and 16.3 hold only a template and no such sentence and got no example. The owner sees the two examples in the approval packet of plan 04-19.

**9. [Reading] Choices inside the label `Add examples`.** AE-314 shows two of the four actions of Section 13.2 (reapproval of the specification, stop of the flow); AE-315 refers to the fail rule template F-01 of Section 12.2 as the corresponding rule of Section 13.3; AE-319 shows all eight prohibitions in one scenario; AE-317 uses the completion of a change as the gate that a blocking finding blocks. The examples for Sections 13 and 14 and the example for Section 19.1 are written without the prefix Full because those sections apply to both method profiles.

**10. [Reading] The repair of FG-21 adds a sentence.** The finding quotes the sentence "The member `gate` is the identifier of a done gate of the kind `check` ...". The repair adds a new sentence at the end of the bullet and leaves the quoted sentence as it is. Likewise FG-20 rewrites the sentence its finding quotes (exempt, as the finding has the disposition fix).

## Known Stubs

None.

## Unverified

- The owner's answers reached this executor through the orchestrator's message and cannot be independently checked from the repository; the addendum and the register state the channel, and DA3 and FE7 prove that the recorded words are among those offered, not who answered.
- The checks prove structure, minimality and consistency with the register, not that any text is right. Which findings are correct is not assessed here.
- The 26 findings without a disposition (RF-A-001, RF-A-002, RF-A-003, RF-A-004, RF-A-005, RF-A-006, RF-B-002, RF-B-003, RF-B-005, RF-B-006, RF-D-001, RF-D-002, RF-D-003, RF-D-004, RF-E-001, RF-E-002, RF-E-003, RF-E-004, RF-X-005, RF-X-006, RF-X-007, RF-X-008, RF-X-009, RF-X-010, RF-X-011, RF-X-012) are untouched and still open information.
- RF-B-006 (INFO, no disposition) names the passage of Section 12 as the place where the change from the earlier text is disclosed; after FG-22 that passage no longer cites the earlier text. The finding is not touched and not assessed here.
- The new examples and the sentences are drafts that the owner approves or does not approve in plan 04-19; the wording choices of deviations 8 and 9 are the executor's reading of the label `Add examples`.
- The requirement SPEC-14 is not edited; the label `Say none needed` was not chosen, so the question of narrowing it does not arise in this plan. RF-X-005 (MINOR, no disposition) asks the same about Sections 11.3, 12.1, 15, 17 and 18, which this round does not touch.
- Note for plan 04-19: the approval printers and the stages `approval-pending` and `approval-recorded` exit 2 in `--round 5` until that plan adds them.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-19 (diff identity again, approval stages and packet of profile 5, approval of the exact new text). From the first specification commit of this plan, the live checks that pin the text of round 4 fail by design; `bash FIX --replay-round-4` keeps the evidence of round 4 checkable.

## Self-Check: PASSED

- Files exist: the fix round script, the addendum, the specification, the register and this summary.
- Commits `71f0d1d`, `6dad03c`, `88bd7ff`, `f3ec822`, `dcae330`, `b672c30`, `35dd076`, `d286cd1`, `60a3fec`, `429c7f6`, `12a59b4` and `0f68dfa` exist on gsd/v1.1-executable-core.
- `bash FIX --round 5 --stage edits --complete` and `bash FIX --round 5 --stage dispositions` end `RESULT: PASS`; `bash CHK2 --final` and the replays of rounds 4, 3, 2 and 1 end `RESULT: PASS`.
