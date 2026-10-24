---
phase: 02-normative-drafting
plan: 05
subsystem: normative-spec
tags: [profile-resolution, no-weakening, full-profile, realization-table, acceptance-examples, version-header, diff-identity, bash-check]
status: complete

requires:
  - phase: 02-normative-drafting
    provides: "Plans 01 to 04: method profiles (5.6), the core profile (23), protections (24.1 to 24.10), state and versioning (25), conventions K1 to K6, the check script with --ids, AE-01 to AE-217"
provides:
  - "Check script: --final (R1, R2, R3, R7 become failures; C1 for SPEC-01 to SPEC-12 and SPEC-14 to SPEC-18; R4, F1, W1, A1) and --version"
  - "Section 5.3 rewritten in place: six layers, layer 2 as the method profile and compliance profile resolved together, the definition of weakening, the layer set of core, the creation-time and pre-approval check with the issue code gate-weakened; pointers at 3.8, 4.2, 5.2 and 23.7"
  - "Realization table of the 11 protections in the section 24 intro, the frozen set and the parsed value of the Flow Gates of a full change, an Allowed Paths line in the 16.1 template Scope"
  - "41 full rule units with an acceptance example (AE-229 to AE-269) and 11 examples for 5.3 (AE-218 to AE-228)"
  - "Header Version 1.4 and a Revision line"
  - "02-DRAFTING-CHOICES.md (DC-01 to DC-107, OQ-1 to OQ-7, flagged items F1 to F7, unproven items, hand-off list) and the diff identity note"
affects: [Phase 3 owner approval, Phase 4 independent review, engine phases]

actuals:
  tokens: 21000
  tasks: 3
  commits: 8

tech-stack:
  added: []
  patterns: ["rule paragraph ends 'See AE-nn.'", "a pointer paragraph before the example blocks of a rule unit; example blocks of a unit directly after it", "rule-unit table in a script (F1) so that a missing example fails the final run"]

key-files:
  created:
    - .planning/phases/02-normative-drafting/02-DRAFTING-CHOICES.md
    - .planning/reviews/2026-10-24-normative-spec-diff-identity.md
  modified:
    - docs/method/GG-SAD_normative_method_specification.md
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh

key-decisions:
  - "No owner decision was made. Judgment calls are listed under Drafting choices for the Phase 3 packet."

patterns-established:
  - "Quick check before every specification commit; each commit stages the specification only; --final closes the phase."

requirements-completed: [SPEC-16, SPEC-14, SPEC-13]  # drafted as proposed text; nothing here is approved or reviewed.

duration: "about 25 minutes"
completed: 2026-10-24
---

# Phase 2 Plan 05: Full-Profile Revision and Resolution Summary

**Proposed text for SPEC-16 and SPEC-14, the version header, the consolidated register and the diff identity: a six-layer resolution in which a lower layer never weakens a higher one (weakening defined, a creation-time and pre-approval check with the code `gate-weakened`), a realization table that shows each of the 11 protections in `core` and in `full`, 41 acceptance examples for the `full` rule units, Version 1.4, and a `--final` run of the check script that passes.**

## Accomplishments

- Check script: `--final` turns R1, R2, R3, and R7 into failures, runs C1 for SPEC-01 to SPEC-12 and SPEC-14 to SPEC-18, and adds R4 (header `Version: 1.4` and a Revision line with an ISO date, an em dash and a closing period), F1 (an example for each of the 41 `full` rule units, printing the count, and a realization row for each of the 11 protections), W1 (no status wording in the specification or the notes, no Owner reply row in the identity note) and A1 (base blob, result blob, SHA-256, line count, diffstat, commit list; no verdict). `--version` sets the expected version. Quick mode is unchanged.
- SPEC-16 (5.3): the six items keep their order; item 2 reads "selected method profile and compliance profile, resolved together"; the word "silently" is gone. New paragraphs: layer 2 is one layer; weakening is removing a gate, altering its condition (kind and every declaration of 24.1), lowering its severity, or lowering the assurance level it requires; strengthening is adding a gate with its own identifier or raising a level in the project configuration; a lower level in a lower layer has no effect because the higher level is required; the result does not depend on listing order; a `core` change implements layers 1, 2, 3, and 5, with layers 4 and 6 specified for `full` and combination use; the check at creation and again before the approval of the gate definitions, rejecting with `gate-weakened`. The exception of 4.2 is limited to the local specification of a `full` change. Pointers at 3.8, 4.2, 5.2, and 23.7; the base gates of `core` now carry identifiers. 11 examples (AE-218 to AE-228): normal, removal, hard to soft, A2 to A1, same identifier with a changed condition, a duplicate restatement, order, the pre-approval check, the layer set, and the exception.
- SPEC-14, commit 1: the caption `**Realization of the Protections in the Two Method Profiles**` and an 11-row table (24.1 to 24.10 and the result `blocked`) with the columns Protection, Section, In `core`, In `full`; the statement that every protection is an invariant of both method profiles; the frozen set of a `full` change and the parsed value of its Flow Gates (this completes the item that plan 04 handed over); an Allowed Paths heading and bullet in the 16.1 template Scope with one sentence.
- SPEC-14, commit 2: examples for 4.1, 5.5, 6.1, 6.2, 6.3, the four flows of 7.1, 8.2, each of the eight actions of 8.3, 8.4, 8.5, and the 11 realizations (AE-229 to AE-259).
- SPEC-14, commit 3: eight pair examples for 9.k with 10.k, and one each for the `full` only parts of 11.2 and 12.2 (AE-260 to AE-269).
- Header: Version 1.4 and the Revision line `2026-10-24 — Added the method profiles ...`; the Status line keeps its two trailing spaces.
- `02-DRAFTING-CHOICES.md`: DC-01 to DC-107 with block, section and reading taken, OQ-1 to OQ-7, the flagged items F1 to F7, the unproven items, the version note, the hand-off list, the commit structure, the mixed row of 11.2 and 12.2, and the exempt set of 24.1.
- Diff identity note `.planning/reviews/2026-10-24-normative-spec-diff-identity.md`: base blob, result blob, SHA-256, line count, diffstat, the `--final` result, the Python baseline as not run, the review command, and the statement that approval and review have not taken place.

## Task Commits

1. Task 1 (tracer), script: `docs(02-05): extend normative diff check script (final, R4, F1, W1, A1)`
2. Task 1 (tracer), SPEC-16: `docs(02-05): SPEC-16 specify six-layer resolution with no weakening`
3. Task 2, SPEC-14 (1): `docs(02-05): SPEC-14 add the full realization of the protections`
4. Task 2, SPEC-14 (2): `docs(02-05): SPEC-14 add acceptance examples for full rules, sections 4 to 8 and realizations`
5. Task 2, SPEC-14 (3): `docs(02-05): SPEC-14 add acceptance examples for definitions of ready, done, wait and fail`
6. Task 3, header: `docs(02-05): header Version 1.4 and revision line (D-12)`
7. Task 3, register: `docs(02-05): record drafting choices register`
8. Task 3, identity: `docs(02-05): record the diff identity of the proposed specification`

The summary and planning-state commits follow. SPEC-13 has no commit by design (S1, S2, and an empty diff under `src/ggsad/`). The tracer passed its own commands (`--ids SPEC-16` printed `FAIL C1` before the SPEC-16 commit and `RESULT: PASS` after; `--final` then printed exactly `FAIL C1`, `FAIL R4`, `FAIL F1`), and the plan has no human checkpoint, so no stop was made at the tracer gate.

## Verification

- `bash -n` exits 0; `shellcheck` (0.11.0) exits 0 with no finding.
- Seeded defects on copies of the specification outside the repository (`--file`): a Revision line without a closing period printed `FAIL R4`, and a good header printed `PASS R4`; a line `Decided (x)` printed `FAIL W1`; a removed `Covers: Section 8.3 (`wait`)` line printed `FAIL F1` naming it; a removed `Covers: Section 8.4` line (the unit needs two) printed `FAIL F1`; a removed realization row for the result `blocked` and a renumbered row `24.55` each printed `FAIL F1`; `--version 1.x` exits 2.
- Tracer gate: before the SPEC-16 commit `--ids SPEC-16` printed `FAIL C1` and `bash CHK --final` printed `FAIL C1` (SPEC-14), `FAIL R4`, `FAIL F1` and no other FAIL; after the SPEC-14 commits it printed `PASS F1` with 41 units and its only FAIL was R4; after the header commit it printed `RESULT: PASS`.
- Final quick run: B1 E1 E2 E3 S1 S2 N1 X1 R5 R6 R2 R3 R1 R7 all `PASS`, `RESULT: PASS`; warnings: `WARN X1` (the word "prototypes" in existing text of 5.1) and two `WARN R8` on the heading and map row "Protections Shared by Both Profiles" (fixed text from plan 02). R2 reports 269 example blocks, all cited, all with a unique id.
- `bash CHK --final` exits 0 with `RESULT: PASS` (C1, R1 to R7, F1, W1, S1, S2 and the others); A1 facts: base blob `da29d6f3bdef2e88fdd85a762939017d7d7034fa`, result blob `78ac13fd58513317f58991167db10f7a1566f24c` (working file and HEAD equal), SHA-256 `dca08253ffba2f25716919f9ceb975f6075a72571a7f9a42cbeb10c1adaa5e10`, 4399 lines, 3017 insertions and 40 deletions. The note holds the same three values; they were checked against `git hash-object`, `git rev-parse HEAD:<file>` and `sha256sum` after the note was committed.
- Section checks: `--section 5.3` contains `method profile and compliance profile`, `resolved together`, `Section 23.7`, `combination`, 6 numbered items, and `grep -c 'silently weaken'` of the file is 0; 11 example blocks cover Section 5.3; `--section 4.2` contains `full`; `--section 24` contains the caption once and 11 data rows; `--section 16.1` mentions the allowed paths. The F1 check lists all 41 Covers lines.
- Additions only: each of the three SPEC-14 commits has 0 removed lines (`git show --format= HEAD~n -- <file> | grep -c '^-[^-]'` printed 0 for n = 0, 1, 2 at the time of the third commit); `git log --format=%s origin/main..HEAD -- <file> | grep -c '^docs(02-05): SPEC-14 '` is 3. `git log -1 --format=%s -- <file>` is the header subject.
- `git diff --name-only origin/main...HEAD` lists the specification and paths under `.planning/` only; restricted to `src .ggsad specs tests AGENTS.md CLAUDE.md` it prints nothing; `git status --short` was empty after every commit.
- Python baseline: not run (no Python changed).

## Deviations from Plan

**1. [Rule 1 - Bug] A stray comma in the 23.4 paragraph.**
- **Found during:** Task 1.
- **Issue:** Plan 04 listed the comma before "An `answer`" in the paragraph after the 23.4 table as a typo for plan 05.
- **Fix:** replaced by a full stop, in the SPEC-16 commit (the only edit of an existing line outside 5.3; it changes no rule; DC-105).
- **Commit:** `docs(02-05): SPEC-16 specify six-layer resolution with no weakening`

**2. [Rule 2 - Missing critical functionality] The base gates of `core` had no identifiers.**
- **Found during:** Task 1.
- **Issue:** The no-weakening check compares gates by identifier, and 23.7 named the four base gates only in words, so a "same identifier with a changed condition" case could not be stated.
- **Fix:** 23.7 names `scope-violation`, `unanswered-question`, `stale-spec-approval`, `incomplete-evidence` in an added paragraph, and 5.3 states the issue code `gate-weakened` (DC-96).
- **Commit:** `docs(02-05): SPEC-16 specify six-layer resolution with no weakening`

**3. [Plan reading] The 4.2 sentence was not rewritten.** The plan says to qualify it; an added paragraph after it limits the exception to a `full` local specification (DC-98). 5.3 replaces the two lines the plan names (item 2 and the weakening sentence).

**4. [Plan reading] A lower assurance level in a lower layer is accepted and has no effect, not rejected,** because the example of 24.3 on the gate minimum (a gate may state A1 under a configured A2) is existing text, and 24.3 makes the higher level the required one (DC-97).

**5. [Plan reading] The 16.1 "line" for allowed paths is a heading with one bullet plus one explanatory sentence** (DC-102).

**6. [Plan reading] The unit 8.4 needs two examples in check F1,** because an example with `Covers: Section 8.4` (the `reopen` example of plan 04) already existed; without the count the check would pass without a new example.

**7. [Plan reading] No stop at the tracer gate.** Auto mode is off, but the orchestrator ran this plan as one autonomous sequence without a human checkpoint; the tracer commands passed.

Otherwise the plan was executed as written. The context rule (a progress note after commit 2 of SPEC-14) was not needed.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. The full list DC-01 to DC-107 is in `02-DRAFTING-CHOICES.md`. DC-06, DC-12, DC-13, DC-20, DC-21 are research ids completed here; DC-96 onward are new in this plan (DC-28 to DC-39 are in plan 01, DC-40 to DC-58 in plan 02, DC-59 to DC-79 in plan 03, DC-80 to DC-95 in plan 04).

- **DC-96 (new):** The four base gates have the identifiers `scope-violation`, `unanswered-question`, `stale-spec-approval`, `incomplete-evidence`. A change definition that redefines one or states it does not apply is rejected at creation and before the approval of gate definitions; `gate-weakened` when it differs in kind, condition, or severity, a duplicate identifier (23.3) when it does not differ.
- **DC-97 (new):** Weakening means remove, alter the condition (including kind and every declaration of 24.1), lower the severity, or lower the required assurance level. Strengthening is a gate with its own identifier or a raised level in the project configuration. A lower level in a lower layer is accepted and has no effect. The result does not depend on listing order.
- **DC-98 (new):** The exception of 4.2 exists only for the local specification of a `full` change; a human approves it at the level of the approval of gate definitions, it applies to that change only and is recorded in the Deviations of the evidence, and it never reaches the invariant core, the protections of section 24, or the base gates. A `core` change has none. The existing 4.2 sentence stays; a paragraph is added.
- **DC-99 (new):** A `core` change implements layers 1, 2, 3, and 5; layers 4 (size classes) and 6 (integration mappings) are not applicable to `core` and are specified for `full` and combination use; no seventh layer.
- **DC-100 (new):** For a `full` change the no-weakening check compares the Flow Gates with the project-wide definitions of 4.2.
- **DC-101 (new):** The frozen set of a `full` change is the Flow Gates, the allowed path list, and the project-wide definitions under `docs/definitions/` in effect at the approval; the parsed value is an object with `flow_gates` (lists `ready`, `done`, `wait`, `fail` of condition texts), `scope`, and `definitions` (the content hash of the file set).
- **DC-102 (new):** The 16.1 template Scope gains `### Allowed Paths` with `- <path pattern>`; Included and Excluded stay descriptive and are not measured.
- **DC-103 (new):** The `full` cells of the realization table are argued from the generic wording of the `full` flow; they have no prototype evidence.
- **DC-104 (new):** The unit of the examples is the rule unit: 30 units plus 11 realizations = 41; each unit has one block that shows a normal and a failure or boundary case; 8.4 has two blocks; AE-218 to AE-269 are consecutive.
- **DC-105 (new):** The stray comma of the 23.4 paragraph is a full stop (deviation 1).
- **DC-106 (new):** Version 1.4; the Revision line is dated by `date +%F` (2026-10-24), names the amendment in one sentence, and holds no id.
- **DC-107 (new):** The 11 realization examples sit after the realization table in the section 24 intro, cited from one paragraph there.

## Hand-off list (D-11)

The full list is in `02-DRAFTING-CHOICES.md`. In short: the example state `specs/examples/class-m/state.yaml`, `.ggsad/templates/`, the three schema constants "0.1", the archived CHG-001 state; the pinned method version "1.3" in `.ggsad/config.yaml`, `src/ggsad/application/initialize_project.py`, and `tests/unit/test_initialize_project.py` (now stale against Version 1.4); exit codes and the mapping of the stable issue codes (now also `gate-weakened`); the text-versus-binary rule; the configuration keys the text does not name.

## Known Stubs

None.

## Threat Flags

None. The threat register entries were handled: the no-weakening rule is absolute with the qualifier dropped, weakening is defined, and failure, boundary, order and pre-approval examples exist (T-02-18, AE-219 to AE-225); the identity note records the blob ids and SHA-256 after the last edit to the text and they were re-checked after the note was committed (T-02-19); the untested `full` realizations are marked specified but not implemented and listed as unproven in the register (T-02-20); the checks forbid status wording, no checkpoint was made, and nothing was pushed (T-02-21).

## Unverified

- Whether the `full` realizations and the 41 examples are the right reading of a model that the prototype never ran, whether the no-weakening check suits the engine, and whether the examples cover normal and failure behavior at the right risk level can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4).
- Unproven items, as the register lists them: SPEC-14 realizations, SPEC-16 beyond the base-gate check, SPEC-17 (absence), SPEC-18, the equivalent-anchor clause, the platform-review verifier, the soft retry limit, and the path pattern syntax.
- The text is draft; nothing here is approved or reviewed. Any later edit to the specification voids the identity note.
- SPEC-12 is still marked pending in the requirements file: plan 01 left it open until plan 05 added the `full` rule-unit examples, which now exist; closing it is for the phase verification.

## Self-Check: PASSED

- The summary exists next to the plan; the specification contains `**Version:** 1.4`, the caption `**Realization of the Protections in the Two Method Profiles**` once, and `### 5.3 Profile Resolution`; the register contains DC-01, DC-27, DC-28, DC-107, OQ-7, F7, SPEC-13, the header commit and supersede; the identity note exists.
- The eight plan 05 commit subjects above are present in the log after `origin/main`, and four of them start `docs(02-05): SPEC-`.
