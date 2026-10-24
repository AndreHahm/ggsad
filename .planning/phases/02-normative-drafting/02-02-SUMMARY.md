---
phase: 02-normative-drafting
plan: 02
subsystem: normative-spec
tags: [gate-results, frozen-gates, baselines, hard-soft-failure, result-blocked, bash-check]
status: complete

requires:
  - phase: 02-normative-drafting
    provides: "Plan 01: method profiles (5.6), the core profile (23), conventions K1 to K6, check script, AE-01 to AE-59"
provides:
  - "Check script options --ids (check C1) and the acceptance example structure check R2 (warning only)"
  - "Section 24 Protections Shared by Both Profiles: intro with term table and the single value-comparison rule, map row 24"
  - "Section 24.2 Three-Valued Gate Results, 24.1 Frozen Gate Definitions, 24.6 Known-Failure Baselines, 24.7 Hard and Soft Failure"
  - "Result blocked: sections 22.1 to 22.3 rewritten, per-action tables for full (8.3) and core (23.4), cells of complete and resume in 8.3"
  - "Pointer sentences at 3.3, 8.4, 8.5, 10.7, 11.1, 12, 12.1, 12.2, 15, 16.1, 16.4, 19, 20"
  - "Acceptance examples AE-60 to AE-124"
affects: [02-03 trust and integrity, 02-04 state and versioning, 02-05 full revision and resolution, Phase 3 owner approval]

actuals:
  tokens: 14000
  tasks: 3
  commits: 6

tech-stack:
  added: []
  patterns: ["rule once in section 24, one pointer sentence at each existing site", "rule paragraph ends 'See AE-nn.'", "per-action result tables as bold-captioned tables without new headings"]

key-files:
  created: []
  modified:
    - docs/method/GG-SAD_normative_method_specification.md
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh

key-decisions:
  - "No owner decision was made. Judgment calls are listed under Drafting choices for the Phase 3 packet."

patterns-established:
  - "Quick check before every specification commit; each commit stages the specification only; C1 run with the ids done so far."

requirements-completed: [SPEC-01, SPEC-02, SPEC-03, SPEC-07, SPEC-08]  # drafted as proposed text; SPEC-13 stays open: it is checked in every plan and closes with the phase.

duration: "about 30 minutes"
completed: 2026-10-24
---

# Phase 2 Plan 02: Gates and Results Summary

**Proposed text for SPEC-02, SPEC-01, SPEC-07, SPEC-08 and SPEC-03: a three-valued gate result with a check-command gate and exit map, gate definitions frozen by the content hash of the parsed definition, known-failure baselines, hard and soft failure with a bounded override, and the fourth result `blocked` with a rejected-versus-blocked table for each method profile, backed by 65 acceptance examples and a check script that now verifies commit subjects against requirement ids.**

## Accomplishments

- Check script: `--ids LIST` runs C1 (each listed id is named by a commit since the base that touches the specification; every such commit starts `docs(02-NN): SPEC-nn` and names only known ids; the single header subject of plan 05 is accepted and counts toward no id; SPEC-13 needs no commit). R2 warns on duplicate acceptance example ids and on blocks without Covers, Given, When or Then.
- Section 24 and 24.2: the three results `satisfied`, `not_satisfied`, `not_evaluable`; the causes of `not_evaluable`; the decision order (hard failure, then a gate that cannot be evaluated, then soft failure, then wait gate, then unmet done gate); retry counting over `not_satisfied` only; the check-command gate with command as argument list and exit map; `not_applicable` kept as a different marker.
- Section 24.1: gate definitions fixed at approval, compared by the content hash of the parsed definition before every state-changing operation, with `cancel`, `supersede` and the re-approval (recorded as an amendment) exempt.
- Section 24.6: baseline on a check-command gate only, satisfied when every failure is on it, otherwise `not_satisfied` naming up to three new failures in code point order plus the count, unreadable failures `not_evaluable`.
- Section 24.7: severity `hard` or `soft` on every fail condition; hard closes as failed without human action; soft pauses for a human who closes as failed or records an override (reason, integer N of at least 1, bound to the approved hash, lapses when used up or on amendment, no default N).
- Sections 22.1 to 22.3: four results with the `changed` value of each, a non-empty `issues` field for every result other than `success`, the `state` field per method profile, an operation to record a human decision; 8.3 cells of `complete` and `resume` read `blocked` for gate evaluations and `rejected` for preconditions; captioned per-action tables in 8.3 (`full`) and 23.4 (`core`).

## Task Commits

1. Task 1 (tracer), script: `docs(02-02): extend normative diff check script (C1, R2)`
2. Task 1 (tracer), SPEC-02: `docs(02-02): SPEC-02 define three-valued gate results in section 24`
3. Task 2, SPEC-01: `docs(02-02): SPEC-01 freeze gate definitions at approval in section 24.1`
4. Task 2, SPEC-07: `docs(02-02): SPEC-07 define known-failure baselines in section 24.6`
5. Task 3, SPEC-08: `docs(02-02): SPEC-08 distinguish hard and soft failure in section 24.7`
6. Task 3, SPEC-03: `docs(02-02): SPEC-03 add result blocked and rejected versus blocked per action`

The summary and planning-state commits follow. The tracer passed its own commands (`--ids SPEC-02` printed `FAIL C1` before the SPEC-02 commit and `RESULT: PASS` after), and the plan has no human checkpoint, so no stop was made at the tracer gate.

## Verification

- `bash -n` exits 0; `shellcheck` exits 0 (run, no findings).
- C1 seeded on a throwaway clone outside the repository, each run with the script copy: a spec-touching subject without `SPEC-nn` fails; `SPEC-19` fails as an unknown id; the header subject alone passes for `SPEC-12` and does not count toward `SPEC-02`; a subject naming two ids counts toward both; `SPEC-13` in the list needs no commit; a commit that does not touch the specification is ignored; `--ids SPEC-19`, `--ids spec-01`, `--ids SPEC-01,` and `--ids` with no value exit 2.
- R2 seeded on copies: a missing Then line, a duplicate id and a missing Covers line each print `WARN R2` and the run still ends `RESULT: PASS`.
- Quick run after each specification commit: `RESULT: PASS`. Final run: B1 E1 E2 E3 S1 S2 N1 X1 R5 R6 R2 C1 all `PASS`; warnings: `WARN X1` (the word "prototypes" in existing text of section 5.1) and two `WARN R8` on the heading and map row "Protections Shared by Both Profiles" (the heading text is fixed by the plan and contains the word without a qualifier). `bash CHK | grep -c '^WARN R2'` is 0.
- `--ids SPEC-02,SPEC-01,SPEC-07,SPEC-08,SPEC-03` prints `RESULT: PASS`; the five specification commits are in the order SPEC-02, SPEC-01, SPEC-07, SPEC-08, SPEC-03, one each.
- Additions only: the commits for SPEC-02, SPEC-01, SPEC-07 and SPEC-08 each have 0 removed lines. The SPEC-03 commit removes four lines (the two 8.3 cells and the two 22.2 paragraphs it rewrites).
- `grep -n '^### 24\.'` lists 24.1, 24.2, 24.6, 24.7 in that order; the map row for section 24 occurs once and R5 holds.
- Section checks: `--section 24.2` names `not_evaluable`, `MUST NOT count toward`, `not_applicable`, `exit`, `WAIT_EXTERNAL_SYSTEM`; `--section 24.1` names `Section 25.2`, `cancel`, `supersede`, `amendment`, `rejected`; `--section 24.6` names `baseline`, `not_evaluable`, `three`; `--section 24.7` names `hard`, `soft`, `override`, `lapses`, `severity`; `--section 22.2` has 9 lines with `blocked`, `--section 22.3` has 1; 8.3 and 23.4 each contain the caption `Rejected and Blocked Results per Action` once.
- Example coverage: 1 block covers Section 24, 14 cover 24.2, 12 cover 24.1, 10 cover 24.6, 14 cover 24.7, 6 cover 22.2, 4 cover 8.3, 4 new blocks cover 23.4 for the results. AE-01 to AE-124 are all defined once and all cited; there is no gap.
- Pointers: each of 3.3, 8.4, 8.5, 10.7, 11.1, 12, 12.1, 12.2, 15, 16.1, 16.4, 19 and 20 outputs a reference to the section 24 rule it points to.
- `git diff --name-only origin/main...HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; the changed paths are the specification and `.planning/` only.
- `git status --short` was empty after every script run; the script writes only inside a directory it removes on exit.
- Python baseline: not run (no Python changed).

## Deviations from Plan

**1. [Process] An example id gap was repaired by rewriting local history.**
- **Found during:** Task 3 verification.
- **Issue:** After a renumbering inside the SPEC-01 text, AE-86 was never defined, which broke the rule of consecutive example ids (convention K3). An example that was missing anyway (an approval of a different target while the gate definitions differ) was written as AE-86.
- **Fix:** The addition was squashed into the SPEC-01 commit with an autosquash rebase of the four local commits above the SPEC-02 commit, and the SPEC-01 message was reworded to "AE-75 to AE-86". Nothing had been pushed; the tree after the rebase is identical to the tree before it apart from AE-86 and its citation. Each requirement still has exactly one specification commit.

**2. [Rule 2 - Missing critical functionality] Existing normative cells were rewritten as the plan directs, with one effect to note.**
- The 8.3 cell of `complete` no longer lists DoF among the causes of rejection: an active hard fail condition closes the change as failed, and a soft fail condition or a gate that cannot be evaluated is a wait (24.7, 24.2). The 22.2 `issues` and `state` sentences were extended, not weakened.

Otherwise the plan was executed as written.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. DC-03, DC-04, DC-05, DC-19, DC-23, DC-24 and DC-25 are research register ids; DC-40 onward are new in this plan (DC-28 to DC-39 are in plan 01).

- **DC-03:** "Cancellation" in 24.1 includes `supersede`; the re-approval itself is exempt; a read-only report answers `rejected` with `changed` false and says the gates are not enforced.
- **DC-04:** `not_applicable` stays the marker for a gate not evaluated by design; `not_evaluable` is a separate result and is never recorded as `not_applicable`.
- **DC-05:** `blocked` is generalized to "valid operation, evaluation recorded, transition did not occur", answered only by `close` and `resume` (`core`) and `complete` and `resume` (`full`); every other action answers `rejected`.
- **DC-19:** An override gives an integer N of at least 1; the specification states no default; no number, zero, a negative number or a non-integer is rejected.
- **DC-23:** The check-command gate is defined in 24.2: command as an argument list, an exit map, an unmapped exit status is `not_evaluable`.
- **DC-24:** The `state` field of the envelope holds phase and status for `full`, state and outcome for `core`.
- **DC-25:** Section 22.1 gains "record a human decision"; it is inserted before the last list item so that no existing list line is rewritten. `migrate` is left to plan 04.
- **DC-40 (new):** The result names are `satisfied`, `not_satisfied`, `not_evaluable`, exact lowercase. They describe whether the condition of the gate holds; a done gate is met, and a fail or wait gate is active, when the result is `satisfied`.
- **DC-41 (new):** The section 24 intro holds the single comparison rule: identifiers, path patterns, paths and text values compare as Unicode code point sequences without normalization (defined in 25.1); a rule MAY state otherwise, and none of 24.1, 24.2, 24.6 and 24.7 does.
- **DC-42 (new):** The identity of the frozen definitions is the content hash (25.2) of the parsed gate definitions: comments, layout, mapping key order and quoting do not change it; the order of list elements does.
- **DC-43 (new):** The stable issue codes `gates-changed` (a state-changing or read-only operation while the hashes differ) and `start-blocked` (a `start` stopped by a gate) are named in the text.
- **DC-44 (new):** Under 24.1 every state-changing operation except `cancel`, `supersede` and the approval that replaces the approved hash is rejected, including `approve` of another target, `fail`, `adopt`, `ask` and `answer`. The re-approval is recorded as an amendment that names both hashes and needs a human at the level 24.3 sets.
- **DC-45 (new):** A check-command gate MUST declare a command and an exit map; there is no default map. The map lists exit statuses (non-negative integers) for `satisfied`, `not_satisfied` and, optionally, `not_evaluable`; a status may appear once. A time limit and an extraction rule are optional. In `full` it is a condition of a Flow Gates list that names a command.
- **DC-46 (new):** Output never changes the result the exit map decides, except for the baseline comparison of 24.6; empty output never makes a gate `satisfied`.
- **DC-47 (new):** A retry limit counts `not_satisfied` results over the whole life of the change and is never reset; the limit is a non-negative integer reached when count is at least limit (a limit of 0 is reached at once); a `not_evaluable` result between two `not_satisfied` results neither adds nor resets.
- **DC-48 (new):** `start` is rejected, creating no wait, when a gate cannot be evaluated or a fail or wait gate would decide; `resume` replaces the earlier wait record with a record of kind `external`; read-only actions report and create no wait.
- **DC-49 (new):** An action that closes the change as failed because of a hard failure answers `success`.
- **DC-50 (new):** Baseline entries form a set (a repeated identifier counts once); the record names up to three new failures in ascending code point order plus the count; a baseline entry that did not fail is noted, not a failure; an empty baseline is valid; a baseline on a gate that is not a check-command gate is invalid.
- **DC-51 (new):** A retry limit is a soft fail condition; a retry limit that declares `hard` is invalid. Severity values are exact lowercase.
- **DC-52 (new):** An override names the soft fail condition it covers; an attempt is an evaluation by `close` (`core`) or `complete` (`full`) made while the override is in force, except an evaluation that ends in the wait for a gate that cannot be evaluated; the N-th attempt is allowed and the next evaluation pauses again.
- **DC-53 (new):** In `full`, the wait caused by a soft failure is category `WAIT_DECISION` with the resume condition "a human has recorded an override"; the `fail` action of 8.3 is the other disposition.
- **DC-54 (new):** Per-action results: in `core`, `resume` is rejected while the resume condition of the wait record is not satisfied and blocked while a gate keeps the change waiting; in `full`, `resume` is blocked when the resume-phase DoR is not satisfied or a DoW condition is still active; `start` with an unmet gate is rejected (`start-blocked`) in both; `reopen` is never blocked; a `complete` that preserves the phase with status `done` answers `success`.
- **DC-55 (new):** The 8.3 cell of `complete` is rewritten so that DoF is no longer a cause of rejection (see Deviations); the 12.2 template gains a `Severity` line, the 16.4 template gains a line for gates that could not be evaluated, and section 20 gains the condition "no soft failure awaits a human disposition".
- **DC-56 (new):** In `full`, `start` of a phase with an unevaluable gate follows the `core` reading (rejected, no wait); only `complete` and `resume` create the `external` wait.
- **DC-57 (new):** The section 24 intro term table defines the base revision in `core` as the revision recorded when `start` succeeds and in `full` as the revision recorded when the change starts (24.5); "human" points to 24.3 in both. A `---` separator precedes the heading of section 24, as it does between other sections.
- **DC-58 (new):** Acceptance example ids AE-60 to AE-124 are consecutive but not in document order (the SPEC-01 examples sit above 24.2 and carry AE-75 to AE-86; the per-action results examples sit in 22.2, 8.3 and 23.4).

## Hand-off sites

- Forward references that must resolve by the end of plan 04: sections 24.3, 24.4, 24.5, 24.8, 24.9, 24.10 and 25.1 (all cited from sections 23 and 24), and 25.2 (cited by 24.1). Plan 03 must define: the assurance level required for the approval of gates and for a human disposition (24.3), the base revision and the scope measurement (24.5), and the interpreter (24.10). Plan 04 must define in 25.1 the code point comparison without normalization that the section 24 intro cites, and in 25.2 the content hash applied to a parsed definition.
- Exit codes: the work items speak of the approved result envelope and exit codes, but no requirement of the set owns exit codes and none were added; hand-off to the engine phases (research open question OQ-7, resolved by hand-off).
- Plan 05: the realization table in the section 24 intro; rule-unit examples for the `full` parts added here (the `full` examples AE-71, AE-97, AE-121 to AE-124 exist; the 24.1 and 24.6 `full` realizations rest on the generic wording of the Flow Gates and have no `full`-specific example); section 5.3 layers.
- Engine phases (unchanged by this phase): the issue codes `gates-changed` and `start-blocked`, the result `blocked` in the result envelope, the exit map of the check-command gate.

## Known Stubs

None.

## Threat Flags

None. The threat register entries were handled in the text: the exempt set of 24.1 names `cancel`, `supersede` and the re-approval (T-02-06, AE-77, AE-78, AE-81); `not_evaluable` is never a failure and never counted, with a limit-boundary example (T-02-07, AE-62 to AE-64); the baseline is frozen under 24.1 and the override is bounded, bound to the approved hash and lapses on amendment (T-02-08, AE-96, AE-102, AE-103).

## Unverified

- Whether each rule faithfully states the protection the prototype exercised, whether the `full` readings are the right ones (they are argued, not tested), and whether the examples cover normal and failure behavior at the right risk level can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4).
- Cross references to sections 24.3, 24.4, 24.5, 24.8, 24.9, 24.10, 25.1 and 25.2 do not resolve yet, by design.
- The text is draft; nothing here is approved or reviewed.

## Self-Check: PASSED

- The summary exists next to the plan; the script and the specification contain `--ids`, `### 24.1 Frozen Gate Definitions`, `### 24.2 Three-Valued Gate Results`, `### 24.6 Known-Failure Baselines`, `### 24.7 Hard and Soft Failure` and map row 24.
- The six plan 02 commit subjects above are present in the log after the base.
