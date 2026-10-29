---
phase: 04-independent-review
plan: 22
subsystem: independent-review-fix-round-6
tags: [independent-review, owner-disposition, disposition-addendum, fix-round, specification-edit, round-6]
status: complete

requires: ["04-21"]
provides:
  - "Profile 6 of the fix round check script, the shared disposition addendum code and the replay of round 5"
  - "Disposition addendum of round 5 with the owner's dispositions of RG-C-001, RG-X-001 and RG-X-004"
  - "Specification edits for RG-A-001 and RG-X-004 (FG-23), RG-C-001 (FG-24) and RG-X-001 (FG-25)"
  - "Fix register of round 6"
affects: [04-23 approval of the exact new text, 04-24 review of round 6, 04-25 dispositions of round 6]

actuals:
  tokens: 8000   # chars/4 over the files changed by task 3 only (addendum, specification, register, this summary); the script changed by task 1 is not counted
  tasks: 3
  commits: 8

tech-stack:
  added: []
  patterns: ["one addendum code path shared by profiles 5 and 6 through profile variables", "replay of an earlier round in a throwaway clone", "register entries tied to the text by the check script"]

key-files:
  created:
    - .planning/reviews/2026-10-29-normative-spec-review-disposition-addendum-round-5.md
    - .planning/reviews/2026-10-29-normative-spec-fix-round-6-register.md
  modified:
    - .planning/phases/04-independent-review/04-check-fix-round.sh
    - docs/method/GG-SAD_normative_method_specification.md

key-decisions:
  - "RG-A-001 and RG-X-004 are fixed as a repair: the reserved-name test applies to the part of the identifier before the first dot (FG-23)."
  - "RG-C-001: the owner chose Not closed; a supersede action refuses a replacement that is closed (FG-24)."
  - "RG-X-001: the owner chose Say it openly; one sentence and one example state that spec.md is protected only after it was approved (FG-25)."

requirements-completed: []  # REVIEW-01 and REVIEW-02 are not ticked; Phase 4 is open.

duration: "not measured; the plan spanned two implementation sessions and an owner checkpoint run by the orchestrator"
completed: 2026-10-29
---

# Phase 4 Plan 22: Fix Round 6 Summary

PHASE NOT COMPLETE. The fix round script has a profile for round 6, a checked disposition addendum and a replay of round 5. The owner dispositioned RG-C-001, RG-X-001 and RG-X-004 as fix and chose how the first two are fixed. The specification now carries the fixes for RG-A-001, RG-X-004, RG-C-001 and RG-X-001, with three new examples (AE-321 to AE-323) and a register. The text of round 5 is no longer the live text, so it must be approved again (plan 04-23), reviewed again (plan 04-24) and the new findings dispositioned (plan 04-25).

## Accomplishments

- Task 1 (tracer): profile 6 of the fix round check script, the profile variables of the addendum code, the static table of changes FG-23 to FG-25, the decisions OD-10 and OD-11, the register skeleton of round 6 and the replay of round 5 (checks R5-1 to R5-8). Commits `a1b2aad` and `eb6ec0c`.
- Task 2: owner checkpoint, run by the orchestrator; no commit.
- Task 3: the addendum, three specification commits, the register and this summary.
- The 18 findings of round 5 without a disposition (14 MINOR, 4 INFO) are untouched and are listed in the register under `Findings not touched`. The Requestor assessed no finding.

## Task Commits

1. Task 1: `a1b2aad` docs(04-22): add the round 6 profile to the fix round check script (tracer)
2. Task 1: `eb6ec0c` docs(04-22): add the replay of round 5 to the fix round check script
3. Task 3: `8a4acf0` docs(04-22): record the owner dispositions of the further findings of round 5
4. Task 3: `02612b8` docs(04-22): fix-round reserved names before the first dot
5. Task 3: `e53bb61` docs(04-22): fix-round replacement named by a supersede action
6. Task 3: `531da84` docs(04-22): fix-round protection of the specification file
7. Task 3: `373fe5c` docs(04-22): add the fix register of round 6
8. Task 3: this summary, committed as `docs(04-22): summary`.

## Owner dispositions and decisions

Channel (statement as the orchestrator gave it): the answers were given by the repository owner through the interactive question tool in the orchestrating session and relayed verbatim. The pick of which three findings to ask about reached the plan only through the orchestrating session; each of the three was asked.

Findings asked (question as recorded, which is the question printed by `bash CHK --round 5 --print-disposition-skeleton --finding ID`; disposition and reason as the owner gave them):

- RG-C-001. Question: `Finding RG-C-001 (MAJOR). The reviewer says: The supersede precondition accepts a closed change as replaced_by, so a change can be superseded into a dead end. What should happen to it: fix, accept, defer or reject?` Disposition: Fix. Owner reason: none given.
- RG-X-001. Question: `Finding RG-X-001 (MAJOR). The reviewer says: A `core` change whose project never requires spec approval can have `spec.md` silently rewritten at any time; the stale gate never activates and nothing detects the drift. What should happen to it: fix, accept, defer or reject?` Disposition: Fix. Owner reason: none given.
- RG-X-004. Question: `Finding RG-X-004 (MINOR). The reviewer says: The identifier rule bans reserved base names only; `con.x` or `nul.tmp` remain legal identifiers even though they are still unusable directory names on some file systems. What should happen to it: fix, accept, defer or reject?` Disposition: Fix. Owner reason: none given.
- RG-A-001 was already Fix on record (reason none given) and was fixed as a repair; it was not asked again.

Design decisions (label as the owner gave it; reason none given for both):

- OD-10 Replacement (RG-C-001). Question: `The supersede action only requires that the replacement is a different change that exists, and the text does not say whether that change may already be closed. Which replacement should be allowed?` Answer: Not closed.
- OD-11 Spec drift (RG-X-001). Question: `The text protects the specification file (spec.md) of a core change against later edits only after it was approved once, and a project does not always require that approval. How should this be fixed?` Answer: Say it openly.

Name and date as the owner gave them:

- Name: AndreHahm. Date: 2026-10-29.
- Provenance: the owner's free-text replies to the name and date questions came back only as the option label `Type it under Other`; the questions were not sent a third time. The owner was asked whether candidates were wanted and answered `Yes, offer candidates`. The name was picked from the candidates AndreHahm and Andre Hahm, and the date from the candidates 2026-10-29 and 2026-10-30. The addendum states this in its Owner reply row.

The response about the neutral fact and the quoted sentences: this executor received the owner answers and the channel statement through the orchestrator's message. That message did not repeat the full statement of the response about the neutral fact on RG-X-004 and about the quoted sentences near the edit sites, nor the derived list; it did state that with the label Say it openly only one sentence is added in Section 23.7 and no sentence quoted by a finding without a disposition is reworded. The orchestrator states, after this executor returned: before the dispositions the owner was told in the conversation that RG-X-004 quotes the same sentence as RG-A-001 and that the fix of RG-A-001 edits that sentence whatever is answered for RG-X-004. Before the design questions the owner was told which sections each option of OD-10 and OD-11 edits and that only `Always approve it` rewords the `start` precondition quoted by RG-X-003. The full derived list of quoted sentences near the edit sites (for example the two RG-A-002 sentences in Section 4.3) was not read out to the owner.

These choices carry no name and no date of their own and become final only through the owner approval of the exact new text in plan 04-23.

The orchestrator appended a trailing recommendation sentence (`(My recommendation: ...)`) to the questions at the owner's standing request. It is not part of the recorded questions, which are the printed ones. This deviates from the rule that no option is recommended.

## The fixes

- FG-23, repair (RG-A-001 and RG-X-004), Section 4.3: the sentence on reserved names now says that the part of the identifier before its first dot, which is the whole identifier when it holds no dot, must not be one of the reserved names, compared after case folding; `See AE-321.` is appended; the example AE-321 shows `nul.txt` and `COM3.log` rejected and `nul-1` and `console.txt` accepted. The assumption A-5 was checked: the reviewer's second wording (forbid a dot after a reserved word) and the first reject the same identifiers (`nul.txt`, `COM3.log`, `con.x`, `nul.tmp` rejected; `nul-1`, `console.txt`, `a.nul`, `com10.x` accepted). The list of reserved names is not widened.
- FG-24, owner decision Not closed (RG-C-001), Section 23.4: the precondition of the `supersede` row says that `replaced_by` names a different change that exists and is not `closed`, the table of results lists a closed replacement among the grounds for rejection, the See list gains AE-322, and the example AE-322 is added.
- FG-25, owner decision Say it openly (RG-X-001), Section 23.7: one new paragraph with one sentence says that `spec.md` is protected against later edits only after it was approved and that otherwise `change.yaml` is the only machine-checkable anchor; the example AE-323 is added after AE-276. No existing sentence was reworded, so the stop question `Quoted sentences` did not arise; FE3 confirms that the quoted sentences of the 18 findings without a disposition are still in the text.
- The specification has 4924 lines (round 5: 4898) and the blob `2acdd0b38174b6fd8e8e3df9952063c74071c22a` (round 5: `3c0f689e2464b3a9fc8fcce5c1fc7ef55e06bfd1`). The first eight lines are unchanged. The highest example id is AE-323.

## Verification

- Before the first specification commit, `bash CHK --round 5 --stage dispositioned` ended `RESULT: PASS` (`PASS D8 closure: not closable (fix pending)`) and `bash FIX --round 6 --stage edits --complete` was not yet runnable (no register).
- Addendum: `bash FIX --round 6 --stage dispositions` ended `RESULT: PASS` with `PASS DA1` to `PASS DA5`. The addendum holds no fill marker; its questions equal the printed ones.
- After the register commit: `bash FIX --round 6 --stage edits --complete` ended `RESULT: PASS` with `PASS DA1` to `PASS DA5` and `PASS FE3` to `PASS FE7` (FE3: the header and the 18 undispositioned findings are untouched, only the specification and .planning/ changed, no tab, every changed line lies in a listed section; FE5: its 3 drafted entries are consistent with the text; FE6: the Phase 2 check with --final ends `RESULT: PASS`; FE7: the 3 drafted entries). `bash FIX --round 6 --stage dispositions` ended `RESULT: PASS`. `bash CHK2 --final` ended `RESULT: PASS`.
- Replays, run one at a time with the current scripts: `bash FIX --replay-round-5 --with-current-scripts` printed `PASS R5-1` to `PASS R5-8` and ended `RESULT: PASS`; `--replay-round-4` printed `PASS R4-8` and ended `RESULT: PASS`; `--replay-round-3` printed `PASS R3-8` and ended `RESULT: PASS`. After each, `git worktree list` printed one line and `git status --short` was empty. The orchestrator ran `--replay-round-2` and `--replay-round-1` afterwards, one at a time, with the current scripts: `PASS R2-7` and `PASS R2-8` and `RESULT: PASS`; `PASS FR4` and `PASS FR5` and `RESULT: PASS`; the tree was clean and `git worktree list` printed one line.
- Live checks that fail by design from the first specification commit, because they pin the text of round 5; each stays checkable through `FIX --replay-round-5`: `FIX --round 5 --stage edits` (ended `RESULT: FAIL 3` after the change), `FIX --round 5 --stage approval-pending`, `FIX --round 5 --stage approval-recorded`, and `CHK --round 5` in the stages pins (ended `RESULT: FAIL 6`), brief, reported and dispositioned. The stage `FIX --round 5 --stage dispositions` ended `RESULT: PASS` after the change, as the plan states.
- Task 1 evidence (the pre-flight and after-change baselines of the script work and the fixture proofs) was produced by the earlier executor and is not restated here; this executor re-ran only the checks listed above.

Sweep for stale statements (details in the Notes of each register entry): Section 4.3 (AE-288, the pattern, the final dot, uniqueness, `follows` and `replaced_by`), Section 16.1 and Sections 23.1 and 23.4 (references to the syntax of Section 4.3) stay true; the examples AE-44, AE-45, AE-78, AE-309, AE-06, AE-07 and AE-245 and Section 25.1 stay true for the supersede fix; Section 23.7 (the stale gate bullet, AE-57, AE-276), the `start` row and AE-25 and AE-26 of Section 23.4 and Section 24.3 stay true for the spec drift fix.

Dispatch: sequential executors on the main working tree (workflow.use_worktrees is false)

The Python baseline was not run because only .planning/ and the specification changed.

## Deviations from Plan

**1. [Placement] The example AE-322 is placed after AE-45, not after AE-309.** The plan says after AE-309, but AE-309 stands in Section 24.1 (Frozen Gate Definitions) while the other `supersede` examples (AE-44, AE-45) stand in Section 23.4, which is the section the new example covers. The register lists Section 23.4 only. No rule changes with the placement.

**2. [Channel] A recommendation was appended to the owner questions.** See the section on the owner dispositions.

**3. [Channel] Name and date were picks from candidates the owner asked for.** The plan forbids suggesting a name or a date; the owner's free-text replies came back as an option label, and the owner then asked for candidates. The addendum says so.

**4. [Method] The replays of rounds 2 and 1 were not run by this executor.** The replays of rounds 5, 4 and 3 and the other checks above ended `RESULT: PASS`. The replay of round 2 was killed by the system for low memory in the executor's run. The orchestrator then ran both replays one at a time, and both ended `RESULT: PASS` (see Verification).

**5. [Method] Hunk-wise staging.** The three edits of the specification were made in one working tree and staged hunk by hunk so that each change has its own commit listing exactly the specification.

## Known Stubs

None.

## Unverified

- The owner's answers reached this executor through the orchestrator's message and cannot be independently checked from the repository. The checks prove structure, minimality and consistency with the register, not that any text is right; which findings are correct is not assessed.
- The full derived list of quoted sentences near the edit sites was not read out to the owner (see above); the neutral fact on RG-X-004 and the sections each option edits were.
- Whether the choices are right: they become final only through the owner approval of plan 04-23.
- The findings without a disposition (14 MINOR, 4 INFO of round 5, as the script derives) are untouched and remain open information. REVIEW-01 and REVIEW-02 are supported only by the stated scope of the later review.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-23. From the first specification commit of this plan the live checks that pin the text of round 5 fail by design; the replay of round 5 keeps them checkable. PHASE NOT COMPLETE; REVIEW-01 and REVIEW-02 are not ticked.

## Self-Check: PASSED

- Files exist: the addendum, the register, the specification, this summary.
- Commits `a1b2aad`, `eb6ec0c`, `8a4acf0`, `02612b8`, `e53bb61`, `531da84` and `373fe5c` exist on gsd/v1.1-executable-core.
