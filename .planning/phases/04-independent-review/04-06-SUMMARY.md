---
phase: 04-independent-review
plan: 06
subsystem: independent-review-fix-round
tags: [independent-review, fix-round, normative-specification, register, check-script]
status: complete

requires: ["04-05"]
provides:
  - "The specification with the fixes FG-01 to FG-09 for the eleven findings that the owner dispositioned as fix (examples AE-295 to AE-305, new Section 22.4)"
  - "The fix register: a short plain-language account of the nine changes, with before and after text, for the approval packet of plan 04-07"
  - "The stage edits of the fix round check script (checks FE1 to FE6, --complete, the register skeleton printer)"
affects: [04-07, 04-08, 04-09]

actuals:
  tokens: 17400
  tasks: 3
  commits: 16

tech-stack:
  added: []
  patterns: ["one commit per fix group that holds the specification edit and its register entry", "a check that fails when an old statement is left behind, when text outside the listed sections is touched, or when a MUST, SHOULD or MAY line is removed without a stated reason"]

key-files:
  created:
    - .planning/reviews/2026-10-26-normative-spec-fix-round-register.md
    - .planning/phases/04-independent-review/04-06-SUMMARY.md
  modified:
    - docs/method/GG-SAD_normative_method_specification.md
    - .planning/phases/04-independent-review/04-check-fix-round.sh

key-decisions:
  - "Five of the nine changes (FG-02, FG-04, FG-07, FG-08, FG-09) are the Requestor's picks between readings. They are proposals and not decisions of the owner; they become the owner's only through the approval of plan 04-07."

requirements-completed: []  # plan 04-06 carries REVIEW-02, which stays open; REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close only.

duration: "not measured"
completed: 2026-10-26
---

# Phase 4 Plan 06: Fix Round Drafting Summary

PHASE NOT COMPLETE. The text is not final and not approved. This plan drafted the fixes for the eleven findings of the first independent review that the owner dispositioned as fix, in the nine groups FG-01 to FG-09, wrote the short register of the changes, and guarded the edits with the stage edits of the fix round check script. The first specification commit of this plan voided the round-1 approval, by design. The specification is frozen for plan 04-07: it must not change before the diff identity is recorded there. Nothing was asked of the owner, nothing was sent anywhere, and no pick is presented as a decision of the owner.

## Accomplishments

- All nine groups are drafted as the smallest edits that make the text consistent, one commit per group with the subject family `docs(04-06): fix-round ...`, each commit holding the specification edit and the register entry together. The whole delta from the round-1 text is 136 insertions and 15 deletions in one file; the specification now has 4770 lines.
- The register (`2026-10-26-normative-spec-fix-round-register.md`) has one table of the nine changes and one entry per change with What changed, Why, My choice, Before, After and Notes. It says in plain words that a choice is a proposal. What the owner reads in plan 04-07 is what is recorded there.
- The stage edits of `04-check-fix-round.sh` has six checks: FE1 the old statement is gone and the new facts are present in the named places, and the examples exist with their tags; FE2 the statements that stay true are unchanged (the sentence of Section 22.2 on the actions that can answer blocked, the blocked cell of every row of both tables of results, the realization row of the result blocked, the examples AE-259 and AE-287); FE3 minimality (header, the quoted sentences of the 14 findings that were not dispositioned, only the specification and `.planning/` changed, no tab in an added line, every changed line inside a section that the register lists); FE4 every removed line with MUST, SHOULD or MAY is listed in the register with a reason; FE5 the register (layout, fields, quoted fragments, sections, examples, encoding, self-containment; with `--complete` all nine groups and the eleven findings); FE6 the Phase 2 check with `--final` on the specification under test.

## The nine changes

| Change | Kind | Findings | Sections edited | Examples |
|---|---|---|---|---|
| FG-01 A pause request on a change that has already hit a hard failure | repair | RV-A-002, RV-X-001 | 8.3 | AE-295 |
| FG-02 Re-opening a closed change when its new work would have to wait | my choice | RV-A-001, RV-X-002 | 8.3 | AE-296 |
| FG-03 Starting a change when a check cannot be run | repair | RV-C-001, RV-A-003 | 8.3, 8.5, 23.4 | AE-297 |
| FG-04 Cancelling or replacing a change when a check cannot be run | my choice | RV-A-003 | 8.3, 8.4, 8.5, 23.4, 24.2 | AE-298, AE-299 |
| FG-05 Which rule decides when a ready condition is not met | repair | RV-D-001 | 24.2 | AE-300 |
| FG-06 Recording a question in the full profile | repair | RV-B-001 | 8.3, 24, 24.8 | AE-301 |
| FG-07 What happens when a retry limit is reached | my choice | RV-B-005 | 12, 24.7 | none |
| FG-08 Deciding whether a file is text or binary before hashing it | my choice | RV-E-001 | 25.2 | AE-302 |
| FG-09 The guard check for continuous integration | my choice | RV-X-003 | 22.1, 22.4, 23.4 | AE-303, AE-304, AE-305 |

The four repairs (FG-01, FG-03, FG-05, FG-06) make the passages agree on the one reading that the existing text has. The five picks are proposals: FG-02 a reopen whose new scope would have to wait is rejected, like start; FG-04 with a gate that cannot be evaluated cancel and supersede proceed and the result `not_evaluable` is recorded, while wait, fail and reopen are rejected with the issue code `gate-not-evaluable` (the code name is the Requestor's); FG-07 a retry limit stays a soft failure condition and Sections 12 and 24.7 say openly that reaching it pauses the flow for a human, who closes the change as failed or records an override; FG-08 the text-or-binary rule for content hashes is a MUST; FG-09 `guard` is defined minimally as the verify-only action, with four details that are the Requestor's own readings (the six issue codes, a missing state document makes the result `rejected` as not enforced, `guard` is legal from every state and phase, an anchor is demanded only where approvals at the level A2 are required). For each pick the register names the other readings in plain words. The owner can change any pick at the approval of plan 04-07.

## Task Commits

Task 1 (tracer, FG-01):

1. `a872056` docs(04-06): add the edits stage to the fix round check script (tracer)
2. `3247b09` docs(04-06): fix-round wait closes the change as failed on a hard failure (FG-01)

Task 2 (FG-02 to FG-06):

3. `6650e6d` docs(04-06): add the FE1 checks of FG-02 to FG-06 to the fix round check script
4. `b5d785f` docs(04-06): fix-round reopen is rejected when its new scope would have to wait (FG-02)
5. `729f40f` docs(04-06): fix-round start with a gate that cannot be evaluated (FG-03)
6. `8502827` docs(04-06): fix-round actions that never answer blocked and a gate that cannot be evaluated (FG-04)
7. `71d8107` docs(04-06): fix-round Definitions of Ready in the decision rules (FG-05)
8. `b0d3aeb` docs(04-06): fix-round the question-recording operation of the full profile (FG-06)
9. `9b1b050` docs(04-06): allow nested sweep bullets under Notes in the fix round check script
10. `f348c08` docs(04-06): list the sweep results of FG-04 one per line in the fix register

Task 3 (FG-07 to FG-09, read-through, close):

11. `4cd8753` docs(04-06): add the FE1 checks of FG-07 to FG-09 to the fix round check script
12. `55ae1ca` docs(04-06): fix-round retry limit is a soft failure condition, stated openly (FG-07)
13. `d86a968` docs(04-06): fix-round classification of text and binary files for the content hash (FG-08)
14. `443e5b1` docs(04-06): fix-round the action guard and verify-only integration (FG-09)
15. `d9d3313` docs(04-06): fix-round repair after the read-through of the delta
16. this summary, committed as `docs(04-06): summary` (the state files follow in their own commit).

## Verification

- `bash 04-check-fix-round.sh --stage edits --complete` ends `RESULT: PASS` with PASS FE1 (nine groups), FE2, FE3, FE4, FE5 and FE6.
- `bash 02-check-normative-diff.sh --final` ends `RESULT: PASS`, and FE6 re-runs it after every specification commit.
- `bash 04-check-fix-round.sh --replay-round-1 --with-current-scripts` ends `RESULT: PASS` with PASS FR1, FR2, FR3, FR4 and FR5: the round-1 evidence stays checkable at the commit that holds the round-1 text.
- `bash -n` and `shellcheck` on `04-check-fix-round.sh` exit 0; the script has LF line endings only and no tab.
- Order of invalidation, observed after the first specification commit: `bash 04-check-fix-round.sh --stage state` prints the second STATE line (the specification differs from the text of round 1) and ends `RESULT: PASS`; `bash 03-check-owner-approval.sh --stage recorded` exits 1 with FAIL R1 (the file differs from the pinned text), H1 and C1. This is the expected result: the round-1 approval is void until plan 04-07 obtains a new one.
- Seeded failures of task 1, each printing the named id and exiting 1: the round-1 text as the specification under test (FE1); the sentence of Section 22.2 changed (FE2); one header line changed (FE3); the quoted sentence of an undispositioned finding changed (FE3); one MUST paragraph of Section 24.7 deleted (FE4); the After fragment of the register altered (FE5); the words `Section 8.3` put into What changed (FE5); the id AE-295 defined twice (FE6).
- Seeded failures of task 2 and task 3: the round-1 text as the specification under test prints FAIL FE1 for six groups after task 2 and for nine groups at the close; a register with one group pending prints FAIL FE5 with `--complete` and ends `RESULT: PASS` without it; a register whose FG-09 My choice lacks the marker `(4)` prints FAIL FE5; one word of Section 5.6 changed prints FAIL FE3.
- Whole-delta facts: `git diff --shortstat` from the round-1 text shows 1 file changed, 136 insertions and 15 deletions; the example ids run from AE-1 to AE-305 without gap or repeat; no line of the examples AE-259 and AE-287 or of the `close` row of Section 23.4 changed; the specification has 10 commits of this plan and 46 commits since `origin/main`; `git diff --name-only origin/main...HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; `REVIEW-01` and `REVIEW-02` are not ticked.
- The Python baseline of AGENTS.md (uv, ruff, ty, pytest, build) was not run: this plan changes no Python source, test or build input.

## Read-through of the delta

The whole delta was read once, hunk by hunk (28 hunks), with the sections each hunk cites and with the questions: does the new text contradict a sentence it cites or sits next to, does an example still follow from its rule, is a term used before its definition, is a section reference right. One imprecision was found and repaired in `d9d3313`: the first sentence of the new paragraph of Section 24.2 spoke of all actions that never answer blocked, which seemed to include `start`, whose rejection is stated in the paragraph before it; it now speaks of the other actions that evaluate gates. No other contradiction was found. The repair is noted in the entry FG-04. No choice that belongs to the owner was needed.

## Deviations from Plan

**1. [Rule 3 - Blocking] Nested bullets under Notes.** The acceptance criterion for FG-04 counts lines that hold `updated` or `stays true` (at least three), while the register layout of the plan gives each bullet one line. The register check now ignores nested bullets after a Notes bullet, and the sweep results of the groups FG-04, FG-07, FG-08 and FG-09 are one nested bullet each. Commits `9b1b050` (script) and `f348c08` (register). The layout of the printed skeleton did not change.

**2. [Rule 1 - Placement] Check of the changed lines.** FE3 places every changed non-blank line of the specification by the nearest numbered heading at or above it, instead of only the first line of each hunk. This is stricter, and it keeps a blank line next to a new heading from being placed in the section above.

**3. [Rule 1 - Example citation] AE-301 is cited in Section 24.8, not in the front list of Section 24.** The list `See AE-249 ... AE-286.` in front of Section 24.1 is the quoted sentence of an undispositioned finding (RV-D-002), and extending it would have touched that sentence. AE-301 is placed after AE-182 and cited in the sentence of Section 24.8 that the group edits. The other new examples are placed next to the examples of the same action or rule and cited in a `See` sentence of their section, or in the new sentence or paragraph.

**4. [Rule 1 - Register] One bullet for the two removed sentences of FG-08.** FE4 works on removed lines, and the two sentences were one line of the text. The register lists that line once under the heading of normative lines removed or reworded, with one reason that covers both sentences.

**5. Tracer gate.** The plan is autonomous and the configuration has no automatic advance; the orchestrator directed the whole plan in one run, so no human-verify checkpoint was returned after the tracer. The tracer's verification was run end to end after its two commits (the stage edits, the Phase 2 check, the state stage, the replay and the expected failure of the round-1 approval check), and the other groups followed.

## Known Stubs

None. The register fields are all filled; no pending marker is left in the register.

## Threat Flags

None. The new normative surface (the action `guard` and the issue code `gate-not-evaluable`) is the surface that the plan's threat model names (T-04-53) and is guarded by FE1.

## Unverified

- The five picks are the Requestor's proposals and not decisions of the owner; they become the owner's only through the approval of plan 04-07, where each can be changed.
- The checks prove structure and consistency (old statements gone, new facts present, nothing outside the listed sections touched, no weakened MUST, SHOULD or MAY line without a reason), not that a reading is right.
- The Phase 2 check does not run the examples.
- The read-through of the delta is the Requestor's own and is not independent review; a new independent review follows in plan 04-08.
- The repairs make the text consistent with the existing text; whether the owner would have chosen the same reading is exactly what the approval of plan 04-07 is for.

## Next step

Plan 04-07: record the diff identity of the new text, print the approval packet from the register, and obtain one approval of the exact new text from the owner. The specification must not change before the diff identity is recorded there; any further edit requires the checks of this plan to be re-run and the register to be updated first. The text of round 1 stays checkable with `bash 04-check-fix-round.sh --replay-round-1`.

## Self-Check: PASSED

- Files exist: the specification, the register, `04-check-fix-round.sh` and this summary.
- Commits `a872056`, `3247b09`, `6650e6d`, `b5d785f`, `729f40f`, `8502827`, `71d8107`, `b0d3aeb`, `9b1b050`, `f348c08`, `4cd8753`, `55ae1ca`, `d86a968`, `443e5b1` and `d9d3313` exist on gsd/v1.1-executable-core.
- The closing checks above ended `RESULT: PASS`; the working tree was clean before this summary.
