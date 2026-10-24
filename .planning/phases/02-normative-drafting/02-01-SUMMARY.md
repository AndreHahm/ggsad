---
phase: 02-normative-drafting
plan: 01
subsystem: normative-spec
tags: [method-profiles, core-profile, applicability, bash-check]
status: complete

requires: []
provides:
  - "Read-only quick check script 02-check-normative-diff.sh (B1 E1 E2 E3 S1 S2 N1 X1 R5 R6 R8, --section)"
  - "Specification section 5.6 Method Profiles with the applicability table"
  - "Specification section 23 The core Profile (23.1 to 23.7) and section map row 23"
  - "Full markers at 4.1, 6 to 10 and the section 21 diagram; Method Profile heading in the 16.5 template; qualified compliance profile terms"
  - "Acceptance examples AE-01 to AE-59"
affects: [02-02 gates and results, 02-03 trust and integrity, 02-04 state and versioning, 02-05 full revision and resolution, Phase 3 owner approval]

actuals:
  tokens: 12700
  tasks: 3
  commits: 4

tech-stack:
  added: []
  patterns: ["one rule, then its AE blocks, rule ends 'See AE-nn.'", "forward references to sections 24 and 25 resolved by plan 04"]

key-files:
  created:
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh
  modified:
    - docs/method/GG-SAD_normative_method_specification.md

key-decisions:
  - "No owner decision was made. Judgment calls are listed under Drafting choices for the Phase 3 packet."

patterns-established:
  - "Quick check before every specification commit; each commit stages the specification only."

requirements-completed: []  # SPEC-12 and SPEC-13 stay open until phase close: plan 05 adds rule-unit examples for the full part, and SPEC-13 is checked in every plan.

duration: "about 20 minutes"
completed: 2026-10-24
---

# Phase 2 Plan 01: Method Profiles and the core Profile Summary

A read-only quick check script plus the proposed text for SPEC-12: method profiles `core` and `full` as a second axis beside the compliance profiles (section 5.6), the `core` model (section 23), an applicability table over sections 1 to 22, full markers, and qualified profile terms, with 59 acceptance examples.

## Accomplishments

- Check script with eleven checks and a `--section` reader; green on the untouched base and on each commit, and proven against one seeded defect per check.
- Section 5.6: vocabulary, selection at creation with an optional project default, exact lowercase identifiers, fixed for the life of the change, move by a new change plus `supersede`, `full` specified but not implemented, applicability table.
- Section 23: change definition and documents (23.1), four states and three outcomes with the initial record (23.2), gates (23.3), twelve-action transition table without `reopen` (23.4), wait records with the kind-to-category table (23.5), evaluation order (23.6), four base gates (23.7).
- Full marker sentence at the head of 4.1, 6, 7, 8, 9 and 10; caption under the section 21 diagram; `## Method Profile` after `## Compliance Profile` in the 16.5 template.
- Bare "profile" qualified as "compliance profile" at seven existing sites; the four rows of the 5.1 table are byte-identical.

## Task Commits

1. Task 1 (tracer), script: `docs(02-01): add normative diff check script`
2. Task 1 (tracer), 5.6: `docs(02-01): SPEC-12 define method profiles in section 5.6`
3. Task 2: `docs(02-01): SPEC-12 specify the core profile in section 23`
4. Task 3: `docs(02-01): SPEC-12 add applicability table, profile markers and qualified terms`

The summary and planning-state commits follow. The tracer passed its own commands (quick run `RESULT: PASS`), so no stop was made at the tracer gate.

## Verification

- `bash -n` exits 0; `shellcheck` exits 0 (run, no findings).
- Base run before the 5.6 edit: `RESULT: PASS`, eleven lines; two consecutive base runs print identical output.
- Seeded defects, each on a copy of the specification or through `--paths-from`, exit 1 with the expected `FAIL`:
  - E1 (byte order mark), E2 (carriage return, missing final line feed, trailing blank line), E3 (tab, three trailing spaces, one trailing space);
  - N1 (`SHALL`; `MUST not`, with a lowercase `must` printed as an uncounted `WARN N1`);
  - X1 (hash-like token, a P-nn identifier, a drive-letter path);
  - R5 (missing map row, heading without map row, odd number of fences);
  - R6 (retitled `8.3` heading);
  - B1 (`--base-blob` of a different blob);
  - S1 (path under `src/ggsad/`), S2 (path under `tests/`).
- Script inputs and exits: a NUL-delimited list holding the single path `.planning/x` + newline + `src/y` passes (newline-splitting would have flagged `src/y`); an empty list passes; a list without a final NUL is read; an unknown `--base`, an unreadable `--file` and an unknown `--section` exit 2; a failing git listing (base without a merge base) exits 2.
- `git status --short` was identical before and after every script run; the script writes only inside a directory it removes on exit.
- After each specification commit the quick run printed `RESULT: PASS`. Final quick run: B1 E1 E2 E3 S1 S2 N1 X1 R5 R6 R8 all `PASS`, `RESULT: PASS`.
- `bash CHK --section 5.6` contains `supersede`, `specified but not implemented`, `second axis`, `fixed`, `Applies To`, `4.1`, `5.5`, `8.1 to 8.5`, `11.2`, `12.2`; eight AE blocks carry `- Covers: Section 5.6`.
- Section 23: seven `### 23.n` headings, one map row; each of the twelve actions has at least two `- Covers: Section 23.4 (`<action>`)` blocks; 51 AE blocks in section 23; `--section 23.2` names open, active, waiting, closed, done, failed, cancelled; `--section 23.7` cites Section 5.3. The Task 2 commit has no removed lines.
- Every defined AE (59) is cited by a rule and every cited AE is defined, with no duplicate definition.
- Task 3: sections 4.1, 6, 7, 8, 9 and 10 each print `specifies the `full` method profile`; `## Method Profile` occurs once; no removed line mentions a 5.1 compliance row (`lean` row byte-identical); `WARN R8` count is 0.
- `git diff --name-only origin/main...HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; `git diff --name-only origin/main...HEAD` lists the specification and `.planning/` paths only.
- Three commits with subject `docs(02-01): SPEC-12 ` touch the specification; each stages only the specification.
- Python baseline: not run (no Python changed).

## Deviations from Plan

**1. [Plan sequencing] The no-size-class example was added with section 23, not with the applicability commit.**
- **Found during:** Task 2.
- **Issue:** The 23.1 rule that a `core` change has no size class must end "See AE-nn." in its own commit, so the example (AE-59) was written in the Task 2 commit instead of the Task 3 commit. The applicability table in Task 3 cites it.
- **Files modified:** `docs/method/GG-SAD_normative_method_specification.md`
- **Commit:** `docs(02-01): SPEC-12 specify the core profile in section 23`

Otherwise the plan was executed as written. The one warning left in the quick run is `WARN X1` on the word "prototypes" in existing text of section 5.1; it is not new and the plan does not change that sentence.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. Ids DC-01 to DC-27 are the research register; DC-28 onward are new in this plan.

- **DC-01:** No renumbering. Section 5.6 and section 23 are added; map row 23 is `| 23. The `core` Profile | Method Semantics |`, added in the commit that creates the heading.
- **DC-02:** `supersede` in `core` closes the change as `cancelled` with a required `replaced_by` naming a different existing change.
- **DC-09:** The `core` wait record is its own (`kind`, `reason`, `owner`, `resume_when`, optional `expires`, optional `question`) with no safe state and no next action; a table maps `question`, `manual`, `fail-gate`, `external` to `WAIT_USER_INPUT`, `WAIT_PROCESS`, `WAIT_DECISION`, `WAIT_EXTERNAL_SYSTEM`. `WAIT_DEPENDENCY` and `WAIT_APPROVAL` have no kind of their own.
- **DC-12:** The base gates of `core` are the scope violation fail gate (hard), the unanswered question wait gate, the stale specification approval wait gate (active while `spec.md` differs from the approved version) and the incomplete evidence done gate; present on every change, not removable, not alterable by a lower layer.
- **DC-22:** Marker sentence "This section specifies the `full` method profile (Section 5.6)." at the head of 4.1, 6, 7, 8, 9, 10, a caption under the section 21 diagram, and the statement in 5.6.
- **DC-24:** `core` records `state` and `outcome` in `state.json` (section 25.1 will define it); the section 22.2 wording for both profiles is left to plan 02.
- **DC-26:** The method profile is chosen per change at creation; project configuration MAY name a default; a project that names one SHOULD record it in the project brief, whose 16.5 template gains `## Method Profile` with the values `core | full`.
- **DC-27:** Default applicability is both method profiles unless a section is listed as `full` only. Full-only: 4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 11.1, 16.1 to 16.4, the section 21 diagram. Sections 23 to 25 state their own applicability.
- **DC-28 (new):** The mixed sections 11.2 and 12.2 apply to both method profiles except the safe current state and next action of a wait state (11.2) and the final status code of a fail rule (12.2), which are `full` only; sections 23.5 and 23.2 give the `core` equivalents. Plan 05 gives the `full` part of each a rule-unit example.
- **DC-29 (new):** Creation with no method profile and no project default is rejected; `core` and `full` are exact lowercase identifiers and any other value (other case, whitespace) is rejected.
- **DC-30 (new):** The reference implementation does not implement `full` and MUST reject the creation of a change that selects it; the marking does not weaken any `full` rule.
- **DC-31 (new):** File names and field names of a `core` change: directory `specs/<change-id>/` with `change.yaml`, `spec.md`, `state.json`; fields `id`, `method_profile`, `compliance_profile`, `author`, `owner`, `goal` (`problem`, `done_when`, `non_goals`), `scope.allow`, `requirements`, `gates` (`fail`, `wait`, `done`) and optional `follows`. For `full` the method profile is recorded with the mandatory information of the change (section 4.3); the 16.1 template is not changed.
- **DC-32 (new):** `follows` MUST name an existing change that is `closed` with any outcome; the field is a reference and never changes the named change.
- **DC-33 (new):** Gate semantics in `core`: fail and wait gates are predicate gates; an active wait gate blocks start, resume and close without creating a wait record; done gate kinds are `check`, `review` (a recorded result from a participant other than the requestor) and `sign-off` (a human approval of that gate); gate identifiers are unique including base gates.
- **DC-34 (new):** Transition table readings: `approve` and `answer` are legal from every state except `closed`; `ask` from `open` and `active`; `fail` only from `waiting` with a `fail-gate` wait record, with a reason; `cancel` and `supersede` from every state except `closed`; `adopt` from any state and only while the history has no anchor; `wait` needs a reason, an owner and a resume condition and creates kind `manual`, or kind `question` when it gives a question. `check`, `review` and `guard` are read-only, legal from every state, and their report content is not specified.
- **DC-35 (new):** Evaluation order in 23.6: active hard fail, then a gate that could not be evaluated (wait of kind `external`), then active soft fail (wait of kind `fail-gate`), then active wait gate, then, for `close` only, an unsatisfied done gate. `start` requires that none of these would decide. A gate that does not apply to the action is recorded as `not_applicable`.
- **DC-36 (new):** An action requested from a state outside its Legal From cell MUST be rejected under section 22.3; for an unmet precondition the table says only that the transition does not occur. Whether an unmet precondition answers `rejected` or `blocked` is left to plan 02.
- **DC-37 (new):** Resume conditions by kind: `question` is satisfied when the question is answered; `fail-gate` when a human has recorded an override; `external` when the gate can be evaluated again; `manual` when the owner of the wait states in `resume` that the condition holds. An overdue wait stays a wait until the change leaves `waiting`.
- **DC-38 (new):** Seven bare "profile" sites became "compliance profile" (3.7 selected profile, 5.1 intro, 5.1 table header only, 5.1 custom profiles sentence, 5.2 first line, 5.2 lower-compliance sentence reworded to "A compliance profile of lower compliance", 14.1). "the `lean` profile" mentions, "enabled practice profiles" and the heading "5.3 Profile Resolution" are left as they are.
- **DC-39 (new):** Acceptance example ids are not in document order: AE-59 sits in 23.1 after AE-12.

## Hand-off sites

- Forward references that must resolve by the end of plan 04: sections 24.1, 24.2, 24.3, 24.4, 24.5, 24.7, 24.8, 24.9 and 25.1 (all cited from section 23), and section 24 as a whole from section 5.6.
- Plan 02: result `blocked` versus `rejected` per action in section 23.4 and in section 22; the `core` row for `reopen` absence is already stated; 24.2 defines the check command gate and the three-valued result used by 23.3 and 23.6.
- Plan 04: `state.yaml` to `state.json` in section 4.3, the JSON blocks of 8.1 and 11.2, section 25.1 for the `state` and `outcome` fields and the wait record fields named in 23.5.
- Plan 05: section 5.3 layers (the base gates of 23.7 are cited as a layer-2 input), rule-unit examples for the `full` part of 11.2 and 12.2, header Version 1.4.
- Engine phases (unchanged by this phase): version "1.3" pinned in `.ggsad/config.yaml`, `src/ggsad/application/initialize_project.py` and `tests/unit/test_initialize_project.py`; schema constants "0.1"; `flow.profile` in `specs/examples/class-m/state.yaml`.

## Known Stubs

None.

## Unverified

- Whether each `core` rule faithfully states the protection the prototype exercised, whether the `full` markers and the mixed-section row are the right reading, and whether the examples cover normal and failure behavior at the right risk level can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4).
- Cross references to sections 24 and 25 do not resolve yet by design (forward references); the reference check comes with plan 04.
- The text is draft; nothing here is approved or reviewed.

## Self-Check: PASSED

- Script and summary exist; the specification contains `### 5.6 Method Profiles`, `## 23. The `core` Profile` and map row 23.
- The four plan 01 commit subjects above are present in the log after `origin/main`.
