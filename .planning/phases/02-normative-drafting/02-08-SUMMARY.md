---
phase: 02-normative-drafting
plan: 08
subsystem: normative-spec
tags: [gap-closure, review-findings, resolution-layers, compliance-profile, approval, open-questions, allowed-path-list, register, diff-identity, bash-check]
status: complete
gap_closure: true

requires:
  - phase: 02-normative-drafting
    provides: "Plan 07: write protection of the state document, evidence commands in the frozen definitions of full, AE-1 to AE-289, the register DC-01 to DC-107 with the lists of plans 06 and 07 in their summaries"
provides:
  - "Check script: D1 (with --final and --register FILE; exactly one disposition row per review finding, no CR or WR row RECORDED, no other id) and a second id-less header subject accepted by C1"
  - "5.3: layer 6 gives a core change no gate; combination mode is specified for full; a lower assurance statement is neutralized, not rejected; a weakening in a full change is rejected with gate-weakened. 17 points to 5.3"
  - "5.6 and 23.1: the compliance profile of a change must equal the project's active one at creation"
  - "5.4: lean self-approval means the requesting human; a claim satisfies a decision at the level 24.3 requires"
  - "9.4, 6.1, 9.6, 24.5: Ready-to-Spec is about its criteria, complete answers blocked while a question is open; the allowed path list is stated and is a Ready-to-Build criterion; in full the scope is evaluated from the first approval of the gate definitions"
  - "AE-290 to AE-294 (5 examples; the specification now holds AE-1 to AE-294)"
  - "Header Revision line dated 2026-10-25; register DC-108 to DC-141, the 44-row disposition table, OQ-8 to OQ-15; the diff identity of the final text"
affects: [Phase 3 owner approval, Phase 4 independent review]

actuals:
  tokens: 22600
  tasks: 4
  commits: 7

tech-stack:
  added: []
  patterns: ["finding ids live in commit subjects, plans, summaries and the register, never in the specification", "a disposition table in the register is machine-checked (D1) so that no finding is dropped"]

key-files:
  created: []
  modified:
    - docs/method/GG-SAD_normative_method_specification.md
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh
    - .planning/phases/02-normative-drafting/02-DRAFTING-CHOICES.md
    - .planning/reviews/2026-10-24-normative-spec-diff-identity.md

key-decisions:
  - "No owner decision was made. The conservative readings are listed under Drafting choices (DC-134 to DC-141) and as owner questions OQ-8 to OQ-15 for the Phase 3 packet."

patterns-established:
  - "Each fix is a numbered drafting choice with an acceptance example whose id is cited by a rule line (See AE-nnn)."

requirements-completed: []  # the specification is proposed text; nothing here is approved or reviewed.

duration: "one session, not timed"
completed: 2026-10-25
---

# Phase 2 Plan 08: Review Findings, Part 3 and the Close of the Phase Artifacts Summary

**Closes WR-18 to WR-21, WR-25, WR-26 and the info items IN-01, IN-02 (A0 paragraph), IN-12 in the proposed text, and finishes the phase artifacts: the check script now guards the disposition table (D1), the header Revision line is dated, the register holds DC-108 to DC-141 with a disposition for each of the 44 findings and the owner questions OQ-8 to OQ-15, and the diff identity note names the final blob. The specification holds AE-1 to AE-294 and `--final` prints RESULT: PASS.**

## Accomplishments

- Check script (tracer): D1 runs only with `--final`; `--register FILE` names the register (default: the register of this phase). Under the heading "Dispositions of the review findings" each of CR-01..CR-03, WR-01..WR-27, IN-01..IN-14 must have exactly one row whose first two cells are the id and one of FIXED, FIXED-CONSERVATIVE, DEFERRED-TO-OWNER, RECORDED; a CR or WR row valued RECORDED fails, and so does a row for any other id. C1 accepts the second id-less header subject `docs(02-08): header revision line after the review fixes (D-12)` in addition to the first, and counts neither toward an id. The usage comment names both.
- Resolution layers and compliance profile (WR-18, WR-19, IN-01, IN-12): 5.3 says that layer 6 gives a `core` change no gate because a `core` change does not use integration mappings, that the combination mode of 3.8 and 17 is specified for `full` and combination use and is not built, and that where layer 6 applies no weakening and no bypass of a gate is allowed; 17 gains a pointer sentence; the six layers keep their numbers and 25.3 is unchanged. 5.6 requires that the compliance profile of a change MUST equal the active compliance profile of the project at creation, and 23.1 points to it. The lower assurance statement is "neutralized" (accepted, no effect, not a cause of rejection), and a weakening in a `full` change is `rejected`, `changed` false, `gate-weakened`. AE-290, AE-291; AE-221 and AE-227 reworded.
- Approval (WR-20, WR-21, IN-02): self-approval under the `lean` compliance profile means the human who requested the work; the sentence "a verified human" is replaced by "a claim satisfies a decision of the set only if its verified level is at least the level that 24.3 requires for the action that records the decision (A0 when no gate or configuration states a minimum)". AE-292, AE-293 (the A0 paragraph of 5.4).
- Open questions and the allowed path list (WR-25, WR-26): 9.4 says Ready-to-Spec is a statement about its criteria alone and that `complete` answers `blocked` while the recorded question is unanswered; AE-263 says so. 6.1 puts the allowed path list in the minimum content of Class S, 9.6 gains the criterion "the allowed path list is stated (Section 24.5)", and 24.5 evaluates the scope in `full` from the first approval of the gate definitions (`not_applicable` before). AE-294; AE-231 and AE-265 mention the list.
- Header (D-12): the Revision line reads 2026-10-25 (the output of `date +%F`), an em dash and one sentence that names the amendment and the alignment of the gate model, evaluation order, approval rules and identifier rules; no id, no mention of a review. The Version stays 1.4 and the Status line keeps its two trailing spaces.
- Register: intro updated; table DC-108 to DC-141; "Changed by DC-nnn." appended to 23 earlier rows (the 15 rows the plan names and DC-55, DC-63, DC-68, DC-72, DC-91, DC-97, DC-99, DC-102); "Dispositions of the review findings" (44 rows), "Recorded findings", "Owner questions OQ-8 to OQ-15"; Unproven items, Version note, hand-off list, Commit structure and Verification record extended.
- Identity note updated in place with the values below.

No `Covers:` line of an F1 unit changed (F1 still reports 41 units and 11 realization rows). The four rows of the table of 5.1 are byte-identical to the base (4 rows, 0 changed lines).

## Task Commits

1. Task 1 (tracer), script: `53ac426` docs(02-08): extend normative diff check script (D1, second header subject)
2. Task 1, spec: `1c8d6b2` docs(02-08): SPEC-16 SPEC-12 fix WR-18 WR-19 IN-01 IN-12 resolution layers, compliance profile and weakening wording
3. Task 2 (1): `fbe1278` docs(02-08): SPEC-04 fix WR-20 WR-21 IN-02 approval by a human and the A0 claim
4. Task 2 (2): `81e98e7` docs(02-08): SPEC-09 SPEC-06 fix WR-25 WR-26 open questions and the allowed path list of full
5. Task 3 (1), header: `1726d14` docs(02-08): header revision line after the review fixes (D-12)
6. Task 3 (2), register: `972c235` docs(02-08): record drafting choices and dispositions of the review findings
7. Task 4, identity note: `a82400c` docs(02-08): record the diff identity of the proposed specification

This summary and the planning-state update are committed separately after it. The plan has no human checkpoint, so no stop was made at the tracer gate; the tracer's verify (`--final` with C1, R9 and the failing lines) was re-run and passed before the next task started.

## Verification

- `bash -n` and `shellcheck` on the check script exit 0 with no finding.
- Seeded D1 runs on throwaway register copies outside the repository (a generated 44-row table with the columns Finding, Disposition, Where, Evidence, DC): the intact copy printed `PASS D1`; a removed row (WR-10), the value `OPEN` (WR-05), a CR row valued `RECORDED` (CR-02), an extra id (WR-28) and a repeated id (IN-01) each printed `FAIL D1` with a message naming the row. Seeded C1 runs in a throwaway clone (never pushed): a one-line specification commit with the subject `docs(02-08): header revision wording` printed `FAIL C1`, and the same commit renamed to the accepted subject printed `PASS C1`. The copies and the clone are outside the repository and hold no path in any committed text.
- Before the register existed, `--final` printed `FAIL D1` as its only FAIL after each specification commit and after the header commit; after the register commit it printed RESULT: PASS.
- Greps after the last specification commit: `--section 5.1` has 4 rows of the compliance profiles and `git diff -U0 origin/main...HEAD` has 0 changed lines of them; `--section 5.3` has 6 numbered layers and contains "layer 6"; `--section 17 | grep -c 'Section 5.3'` is 1 (at least 1 required); `--section 5.6 | grep -c 'MUST equal the active compliance profile'` is 1; `--section 5.4 | grep -c 'a verified human'` is 0 and the section contains "at least the level"; `--section 6.1` and `--section 9.6` contain "allowed path list"; `--section 24.5` contains "first approval of the gate definitions"; `--section 9.4` contains `blocked`; `grep -c 'CR-[0-9]\|WR-[0-9]\|IN-[0-9]\|DC-[0-9]'` of the specification is 0; the Revision line has 0 occurrences of "review".
- Example counts: `grep -c '^\*\*AE-'` printed 289 at the start, 291 after commit 2, 293 after commit 3 and 294 after commit 4; AE-294 is the highest id.
- `git log -1 --format=%s -- docs/method/GG-SAD_normative_method_specification.md` is `docs(02-08): header revision line after the review fixes (D-12)`; the three other specification subjects of this plan start `docs(02-08): SPEC-`.
- `bash CHK` (quick run) prints RESULT: PASS; `bash CHK --final` prints RESULT: PASS (see the register facts below). Register: 44 rows `| CR-`, `| WR-` or `| IN-` (30 FIXED, 10 FIXED-CONSERVATIVE, 4 RECORDED, 0 DEFERRED-TO-OWNER); it contains DC-141, OQ-15, CR-01, WR-26 and IN-14; the register and the identity note hold no `Decided (`, `owner-confirmed` or `Owner reply`.
- `git diff --name-only origin/main...HEAD` lists the specification and paths under `.planning/` only; limited to `src .ggsad specs tests AGENTS.md CLAUDE.md` it prints nothing. `git status --short` was empty after every commit.
- Python baseline: not run (no Python changed).

Final facts printed by `--final` (A1): base blob `da29d6f3bdef2e88fdd85a762939017d7d7034fa`; result blob `ed758c46d5ac901359ab2c0df8e437ef89fed0f1` (working file and HEAD equal); SHA-256 `45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3`; 4649 lines; 1 file changed, 3268 insertions(+), 41 deletions(-); 36 commits touch the specification since `origin/main`. Passes: B1, E1, E2, E3, S1, S2, N1, X1, R5, R6, R2 (294 blocks), R9 (N = 294), J1 (2 blocks), R3, R1, R7, C1, R4, F1 (41 units), W1, D1. Warnings only: `WARN X1` (the word "prototype" in existing text at line 345) and two `WARN R8` on the heading and map row "Protections Shared by Both Profiles". The same values are in the identity note, and the blob, the SHA-256 and the line count were re-read from the file after the identity note commit and are unchanged by this summary (the summary and the state update touch no specification line).

## Deviations from Plan

**1. [Rule 1 - Consistency] AE-231 and AE-265 reworded.** Once the allowed path list is part of the minimum content of Class S (6.1) and a Ready-to-Build criterion (9.6), the Given of AE-231 ("states the goal, the scope, ...") and of AE-265 ("a build in which a path outside the allowed path list changed") no longer said that a list is stated. AE-231 now reads "the scope with its allowed path list" and AE-265 "a stated allowed path list"; neither `Covers:` line changed. The plan names AE-253 as staying and does not name these two.
- **Commit:** `81e98e7`

**2. [Plan reading] 24.5 first sentence "In `core`".** The rule that the scope is `not_applicable` before the start is now prefixed "In `core`", because in `full` the scope is evaluated from the first approval of the gate definitions (WR-26). The core wording and AE-154 and AE-157 are otherwise unchanged.
- **Commit:** `81e98e7`

**3. [Plan reading] Additional "Changed by" rows.** Besides the 15 earlier rows the plan lists, eight more rows now end with "Changed by DC-nnn." because a later choice changes them (DC-55, DC-63, DC-68, DC-72, DC-91, DC-97, DC-99, DC-102).
- **Commit:** `972c235`

**4. [Plan reading] IN-08, IN-11, IN-14 cite DC-140.** The plan assigns no DC to these three recorded items; DC-140 covers all recorded items, with the reasons in the section "Recorded findings".
- **Commit:** `972c235`

Otherwise the plan was executed as written.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. They continue the register `02-DRAFTING-CHOICES.md`, which now holds DC-01 to DC-141.

- **DC-134 (WR-18, 5.3, 17):** A `core` change does not use integration mappings; layer 6 gives it no gate. Combination mode is specified for `full` and combination use; neither is built. Where layer 6 applies it does not weaken a higher layer and no workflow bypasses a gate. 25.3 unchanged; six layers kept. AE-290. Open: OQ-9.
- **DC-135 (WR-19, 5.6, 23.1):** The compliance profile of a change MUST equal the project's active one at creation, else `new` is rejected; "or a stricter one" is not taken. AE-291. Open: OQ-10.
- **DC-136 (WR-20, 5.4):** `lean` self-approval means the requesting human; never a participant that is not a human. AE-292. Open: OQ-11.
- **DC-137 (WR-21, 5.4):** A claim satisfies a decision of the non-delegable set at the level 24.3 requires (A0 when none is stated). No floor is assigned. AE-293. Open: OQ-12.
- **DC-138 (WR-25, 9.4, AE-263):** Ready-to-Spec concerns its criteria alone; `complete` answers `blocked` while the recorded question is unanswered, and the Definition of Done is not satisfied. Open: OQ-14.
- **DC-139 (WR-26, 6.1, 9.6, 24.5):** The allowed path list is required for Class S minimum content and for Ready-to-Build; in `full` the scope is evaluated from the first approval of the gate definitions. AE-294. Open: OQ-15.
- **DC-140 (IN-01, IN-02, IN-08, IN-11, IN-12, IN-14):** Neutralized lower assurance statement; `gate-weakened` for `full`; AE-293 for the A0 paragraph; four other rules without an example and three items recorded without a text change.
- **DC-141 (header):** Revision line dated by `date +%F`, naming the amendment and the alignment of four rule groups; a second id-less header subject, accepted by C1.

## Findings closed

| Finding | Disposition | Example | Choice |
|---|---|---|---|
| WR-18 | FIXED-CONSERVATIVE | AE-290 | DC-134 |
| WR-19 | FIXED-CONSERVATIVE | AE-291 | DC-135 |
| IN-01 | FIXED | AE-221 | DC-140 |
| IN-12 | FIXED | AE-227 | DC-140 |
| WR-20 | FIXED-CONSERVATIVE | AE-292 | DC-136 |
| WR-21 | FIXED-CONSERVATIVE | AE-293 | DC-137 |
| WR-25 | FIXED-CONSERVATIVE | AE-263 | DC-138 |
| WR-26 | FIXED-CONSERVATIVE | AE-294 | DC-139 |
| IN-02 | RECORDED | AE-293 (A0 paragraph) | DC-140 |

The register holds all 44 dispositions: 30 FIXED, 10 FIXED-CONSERVATIVE, 0 DEFERRED-TO-OWNER, 4 RECORDED (IN-02, IN-08, IN-11, IN-14). No CR or WR finding is RECORDED.

## Owner questions

- **OQ-8 (CR-01):** restore a `review` gate kind with a recording action.
- **OQ-9 (WR-18):** may a `core` change use combination mode.
- **OQ-10 (WR-19):** may a change name a stricter compliance profile.
- **OQ-11 (WR-20):** may an agent self-approve under `lean`.
- **OQ-12 (WR-21):** an assurance floor for the decisions of 5.4.
- **OQ-13 (WR-24):** protect the assurance-relevant configuration beyond the ratchet.
- **OQ-14 (WR-25):** may a question stay open through the phases before the Definition of Done of the specify phase.
- **OQ-15 (WR-26):** an approved opt-out instead of a required allowed path list.

## Known Stubs

None.

## Threat Flags

None beyond the register of the plan. T-02-30: the identity values were taken after the last specification edit and re-read after the identity note commit. T-02-31: every approval is by a human (AE-292), the reading is left as OQ-11. T-02-32: D1 checks all 44 ids, with seeded failures proven, and no CR or WR row is RECORDED.

## Unverified

- The seeded D1 and C1 runs exercised the generated tables and a clone on this machine only; the check script was not run under another shell or another awk.
- No implementation was changed or run; the Python baseline was not run.
- Whether the conservative readings of this plan (DC-134 to DC-139) and the earlier ones in the register are the right choices can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4). The register does not claim that any of them is approved.
- The throwaway clone and register copies of the seeded runs are in the session scratch directory outside the repository; removing them was not permitted in this session.
- The text is draft; nothing here is approved or reviewed.

## Self-Check: PASSED

- The seven commits `53ac426`, `1c8d6b2`, `fbe1278`, `81e98e7`, `1726d14`, `972c235` and `a82400c` are present in the log after `origin/main`, and subjects of the three spec fix commits start `docs(02-08): SPEC-`.
- The specification contains `**AE-290` to `**AE-294`; the register contains `## Dispositions of the review findings`, DC-141 and OQ-15; the identity note contains the SHA-256 value; the check script contains D1.
