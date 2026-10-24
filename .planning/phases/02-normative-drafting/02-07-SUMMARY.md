---
phase: 02-normative-drafting
plan: 07
subsystem: normative-spec
tags: [gap-closure, review-findings, state-document, write-protection, evidence-commands, schema-versions, identifiers, assurance-levels]
status: complete
gap_closure: true

requires:
  - phase: 02-normative-drafting
    provides: "Plan 06: the core gate model, evaluation by group, AE-1 to AE-281, check script with R9 and J1, the register DC-01 to DC-122"
provides:
  - "Write protection of the state document: the in-progress file state.json.tmp and the lock object state.json.lock, both exempt from the scope measurement, a lock held across compare and replace for every appending operation"
  - "The after record gains reason; the action of an entry is the name of an operation from a closed set; the history-dependent rule list reads Sections 24.1 to 24.5, 24.7, and 24.8"
  - "The parsed value of the full gate definitions has a fourth member requirements (id, evidence_commands); the change specification template gets a heading Evidence Commands per requirement"
  - "Version check order for a state document (latest recorded version first); the identifier syntax of a change; contract operations name the right transition table; the required level is recorded in each approval and is never lowered for a change that already used a higher one; the interpreter that ran is named in gate_detail"
  - "AE-282 to AE-289 (8 examples; the specification now holds AE-1 to AE-289)"
affects: [Plan 08, Phase 3 owner approval, Phase 4 independent review]

actuals:
  tokens: 6200
  tasks: 3
  commits: 5

tech-stack:
  added: []
  patterns: ["finding ids live in commit subjects, plans, this summary and the register, never in the specification", "a leftover implementation artifact has a fixed name, is exempt from the scope measurement and is never state"]

key-files:
  created: []
  modified:
    - docs/method/GG-SAD_normative_method_specification.md

key-decisions:
  - "No owner decision was made. The conservative readings are listed under Drafting choices (DC-123 to DC-133) for the Phase 3 packet."

patterns-established:
  - "Each fix is a numbered drafting choice with an acceptance example whose id is cited by a rule line (See AE-nnn)."

requirements-completed: []  # the specification is proposed text; nothing here is approved or reviewed.

duration: "one session, not timed"
completed: 2026-10-25
---

# Phase 2 Plan 07: Review Findings, Part 2 (state document, trust, evidence commands, identifiers) Summary

**Closes CR-02, CR-03, WR-12, WR-14 to WR-17, WR-22 to WR-24, WR-27 and five info items of the advisory review in the proposed text: a crash leaves only two fixed-name files that the scope check ignores, the write lock is a separate lock object that covers every appending operation, the evidence commands of a `full` change are part of the hashed gate definitions, and the required level of an approval is recorded and cannot be lowered by a configuration change. The specification holds AE-1 to AE-289 and `--final` prints RESULT: PASS.**

## Accomplishments

- Write protection (CR-02, WR-14): 25.1 names the in-progress file `state.json.tmp` and the lock object `state.json.lock`, both in the change directory; 24.5 exempts exactly these two names in both method profiles and measures every other name (`state.json.bak` is measured). The lock is an exclusive lock on `state.json.lock` that the system releases when its holder ends, so the file existing is not a held lock; it is taken before the comparison, also for a change without a state document, and held across compare and replace. It covers the creation and every operation that appends an entry (the table actions, `approve`, `ask`, `answer`, `adopt`, `migrate`). AE-282, AE-283.
- Body fields (WR-15, WR-16, WR-17): the list of history-dependent rules reads "Sections 24.1 to 24.5, 24.7, and 24.8" in 4.3, 25.1 and AE-195; the `after` record gains `reason` (null unless the outcome or status is `failed`; the `fail` reason, or for a hard failure a text naming the failing gates and their detail), and 23.2 points to it; `action` is the name of the operation from a closed set (`new`, `approve`, `ask`, `answer`, `adopt`, `migrate`, or an action of the transition table of the method profile). AE-284, AE-285.
- Evidence commands in the frozen set (CR-03): the parsed value of the `full` gate definitions has four members; `requirements` is the list, in written order, of objects `id` (the heading text before the em dash) and `evidence_commands` (the list items under `#### Evidence Commands`, marker removed, white-space runs collapsed). The 16.1 template, the 16.1 closing sentences, 24.9, 16.4 and the `full` cell of the realization table follow. AE-286 mirrors AE-169 for `full`.
- Schema versions (WR-12, WR-27, IN-05): 25.3 makes the comparison with the latest recorded version first for a state document and checks only a matching document against the supported versions; AE-211 states a held step; AE-198 uses two files that each hold the byte 00; ", a timestamp" is gone from 25.2.
- Contract and identifiers (WR-22, WR-23): 22.1 and 22.3 name the transition table of the method profile (Section 8.3 or Section 23.4) and 22.1 gains three bullets (record a question, adopt a history, report on a change); 4.3 holds the identifier syntax, reserved names and case-fold uniqueness, applied to `id`, Change ID, `follows` and `replaced_by`; 23.1, 23.4 and 16.1 point to it. AE-287, AE-288.
- Trust (WR-24, IN-04, IN-10): 24.3 records `required_level` in each approval and keeps the required level of an approval kind at or above the highest one the history records, and states that the configuration is a repository file that the specification does not protect; 24.10 states that the interpreter is not frozen and that `gate_detail` names the program the token stood for; 25.1 `approvals` gains the field; AE-161 is worded as a recommendation; item 4 of the statement ends "so that the statement names the history that the action extends". AE-289; AE-159 reworded.
- Info items: IN-03 (AE-154 states the cause of a missing base revision), IN-07 (4.3 "In a `full` change, ..."), IN-04, IN-05, IN-10 as above.

No `Covers:` line of an F1 unit changed (F1 still reports 41 units and 11 realization rows).

## Task Commits

1. Task 1 (tracer): `fe75577` docs(02-07): SPEC-15 SPEC-06 fix CR-02 WR-14 WR-15 WR-16 WR-17 IN-03 IN-07 state document write protection and body fields (AE-282 to AE-285)
2. Task 2 (1): `94290c9` docs(02-07): SPEC-10 SPEC-01 SPEC-14 fix CR-03 requirements in the frozen definitions of full (AE-286)
3. Task 2 (2): `dcd3426` docs(02-07): SPEC-18 SPEC-15 fix WR-12 WR-27 IN-05 schema version check order and content hash examples
4. Task 2 (3): `7060749` docs(02-07): SPEC-03 SPEC-15 fix WR-22 WR-23 contract operations and change identifiers (AE-287, AE-288)
5. Task 3: `f59f2f8` docs(02-07): SPEC-04 SPEC-11 fix WR-24 IN-04 IN-10 recorded required level and interpreter (AE-289)

This summary and the planning-state update are committed separately after it. The plan has no human checkpoint, so no stop was made at the tracer gate; the tracer's verify (`--final` with R9 and R2) was re-run and passed before the next task started.

## Verification

- `bash CHK --final` printed RESULT: PASS after every spec commit. The final run printed `PASS R9` (N = 289), `PASS J1` (2 json blocks), `PASS R2` (289 blocks), `PASS F1` (41 units) and the A1 facts: result blob `0b6eb5c510cd512ecdc9e0d6096d8a5af436eeec` (working file and HEAD equal), SHA-256 `755780d2ba6920330e28082277ccff3c9e269fb0eb4db00809fc5ac7ec4d89f1`, 4602 lines. Warnings only: `WARN X1` (the word "prototype" in existing text) and two `WARN R8` on the heading and map row "Protections Shared by Both Profiles". The quick run (`bash CHK`) printed RESULT: PASS.
- Section greps after the last commit: `--section 24.5` and `--section 25.1` each contain `state.json.tmp` and `state.json.lock`; `--section 25.1 | grep -c 'every operation that records an evaluation'` is 0 and the section contains "appends an entry" and `reason`; `grep -c 'Sections 24.1, 24.3, 24.4, and 24.8'` is 0 and `grep -c 'Sections 24.1 to 24.5, 24.7, and 24.8'` is 3; `--section 4.3 | grep -c 'In a `full` change, `plan.md`'` is 1 and the section contains `[A-Za-z0-9][A-Za-z0-9._-]*`; `--section 24 | grep -c 'an object with three members'` is 0, with "four members" and `requirements`; `--section 16.1 | grep -c '^#### Evidence Commands'` is 1; `--section 24.9 | grep -c 'Evidence cell of the requirement coverage table'` is 0; `--section 16.4 | grep -c 'Evidence Commands'` is 1; `--section 25.3 | grep -c 'is made first'` is 2; `--section 25.2 | grep -c 'a timestamp'` is 0; `grep -c 'each hold the byte 00'` is 1; `--section 22.1` and `--section 22.3` have 0 "Section 8 Transition Table"; `--section 24.3 | grep -c 'names the history that the action extends'` is 1, `grep -c 'position in the history at which the action will be recorded'` is 0, the section contains `required_level` and "highest required level"; `--section 24.10 | grep -c gate_detail` is 2; `grep -c 'follows this recommendation'` is 1.
- Example counts: `grep -c '^\*\*AE-'` printed 285 after commit 1, 286 after commit 2, 288 after commit 4 and 289 after the last; AE-289 is the highest id (the blocks are not in document order, DC-39).
- `git log --format=%s origin/main..HEAD | grep -c '^docs(02-07): '` printed 5 before this summary; `git diff --name-only origin/main...HEAD` lists the specification and paths under `.planning/` only; limited to `src .ggsad specs tests AGENTS.md CLAUDE.md` it prints nothing; `git status --short` was empty after every commit. A grep of the specification for the forms CR-, WR-, IN-, DC- followed by digits found nothing (X1 also passes). Python baseline: not run (no Python changed).

## Deviations from Plan

**1. [Rule 1 - Consistency] AE-170 reworded.** Once the evidence commands stand under the heading Evidence Commands, the Given of AE-170 ("only a screenshot in the Evidence cell") no longer said why the evidence is incomplete. It now reads "has no item under its heading Evidence Commands and only a screenshot in the Evidence cell of its requirement coverage table". The `Covers:` line is unchanged. The plan lists AE-169 and AE-257 as unaffected and does not name AE-170.
- **Commit:** `94290c9`

**2. [Plan reading] AE-286 has two cases.** Besides the replaced command (rejected with `gates-changed`) it shows that a change of white space inside an item is no difference, because the text of an item is hashed with white-space runs collapsed.

**3. [Plan reading] AE-211 and AE-289 Given/Then.** AE-211 states a held step from 1.0 to 1.1 and expects `schema-version-mismatch` and not `migration-required`; AE-289 uses the approval of the specification as its kind.

**4. [Plan reading] Pointer sentences.** The 24.1 text, the 4.3 rule on conditional files and the 22.1 list needed no further edits beyond the rows; the new rules end "See AE-nnn." (R2).

Otherwise the plan was executed as written.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. They continue the register `02-DRAFTING-CHOICES.md` (DC-01 to DC-107) and the list of the summary of plan 06 (DC-108 to DC-122), which this plan does not edit.

- **DC-123 (CR-02, 24.5, 25.1):** The exemption is two fixed names, `state.json.tmp` and `state.json.lock`, in the change directory, in both method profiles. Any other name, including `state.json.bak`, is measured. A leftover is never state, is ignored, and MAY be removed. The alternative of keeping the artifacts outside the working tree was not taken because it conflicts with the same-directory rename. AE-282.
- **DC-124 (WR-14, 25.1):** The lock is a separate lock object held across compare and replace, taken also when no state document exists; it is a lock that the system releases when its holder ends, so a leftover file is not a held lock and cannot block writers. It covers the creation and every operation that appends an entry. A reader does not take it. AE-283.
- **DC-125 (CR-03, 24 intro, 16.1, 16.4, 24.9):** The fourth member is `requirements` with `id` and `evidence_commands`; the home of a command is a list item under `#### Evidence Commands` of the requirement; the hashed value of a command is the text of its item (marker removed, white-space runs collapsed). The form of the text is not fixed beyond "argument list, exit map, optional time limit", so two spellings of the same command are two values. The Evidence column of 16.4 now points at the commands and records what they produced. AE-286.
- **DC-126 (WR-12, 25.3):** For a state document the comparison with the latest recorded version is made first; a lowered version that is migratable is still `schema-version-mismatch`. AE-211.
- **DC-127 (WR-15, 4.3, 25.1):** The history-dependent list is extended (24.2 retry counts, 24.5 base revision, 24.7 overrides and attempts) and no inline-record fallback is defined; an inline-record `full` change does not get these rules enforced and the report must not claim them. AE-195.
- **DC-128 (WR-16, 25.1, 23.2):** `reason` is in the `after` record of both method profiles (`status` for `full`); for a hard failure it is generated from the failing gates and their detail.
- **DC-129 (WR-17, 25.1):** `action` is the operation name from a closed set shared by both method profiles. AE-285.
- **DC-130 (WR-24, 24.3, 24.10, 25.1):** The record carries `required_level` for the approval kinds only (approval of the specification, approval and re-approval of gate definitions, sign-off, override); the ratchet applies to these kinds. The levels A0, A1, A2 and the statement are unchanged (O-3). The interpreter is not frozen; `gate_detail` names the program that the token stood for. AE-289, AE-159.
- **DC-131 (IN-03, IN-04, IN-05, IN-07, IN-10, WR-27):** AE-154 states a state taken over from an older document; AE-161 is worded as a recommendation; ", a timestamp" is deleted; 4.3 limits the conditional-files sentence to `full`; the statement clause names the history the action extends; AE-198 uses files that each hold the byte 00.
- **DC-132 (WR-22, 22.1, 22.3):** The three bullets are added before the last; the report bullet is worded as the read-only actions `check`, `review`, and `guard` without a section pointer, because `full` has no table row for them either. AE-287.
- **DC-133 (WR-23, 4.3, 23.1, 23.4, 16.1):** The identifier syntax is `[A-Za-z0-9][A-Za-z0-9._-]*` (whole identifier), no trailing `.`, no reserved device name (ASCII case-folded), unique after ASCII case folding, for `id`, Change ID, `follows` and `replaced_by`. Reserved names followed by an extension (such as `nul.txt`) and non-ASCII case folding are not addressed. AE-288.

Hand-off list for plan 08 (D-11), the new names that the register and the identity note must carry: `state.json.tmp`, `state.json.lock`, the heading `Evidence Commands`, the members `requirements`, `evidence_commands` and `id` of the full gate definitions, the fields `reason` and `required_level`, the identifier syntax of 4.3, the closed set of `action` names.

## Findings closed

| Finding | Disposition | Commit | Example | Choice |
|---|---|---|---|---|
| CR-02 | FIXED | `fe75577` | AE-282 | DC-123 |
| WR-14 | FIXED | `fe75577` | AE-283 | DC-124 |
| WR-15 | FIXED | `fe75577` | AE-195 | DC-127 |
| WR-16 | FIXED | `fe75577` | AE-284 | DC-128 |
| WR-17 | FIXED | `fe75577` | AE-285 | DC-129 |
| IN-03 | FIXED | `fe75577` | AE-154 | DC-131 |
| IN-07 | FIXED | `fe75577` | - | DC-131 |
| CR-03 | FIXED | `94290c9` | AE-286 | DC-125 |
| WR-12 | FIXED | `dcd3426` | AE-211 | DC-126 |
| WR-27 | FIXED | `dcd3426` | AE-198 | DC-131 |
| IN-05 | FIXED | `dcd3426` | - | DC-131 |
| WR-22 | FIXED | `7060749` | AE-287 | DC-132 |
| WR-23 | FIXED | `7060749` | AE-288 | DC-133 |
| WR-24 | FIXED-CONSERVATIVE | `f59f2f8` | AE-289, AE-159 | DC-130 |
| IN-04 | FIXED | `f59f2f8` | AE-161 | DC-131 |
| IN-10 | FIXED | `f59f2f8` | - | DC-131 |

That is 11 findings (CR-02, CR-03, WR-12, WR-14 to WR-17, WR-22 to WR-24, WR-27) and 5 info items (IN-03, IN-04, IN-05, IN-07, IN-10). The remaining findings and info items belong to plan 08.

## Residual of WR-24

A participant who can change the project configuration can lower a minimum level for a change whose history records no earlier approval of that kind, and for the kinds of action that record no `required_level` (an answer, `cancel`, `supersede`, `fail`, `adopt`). The specification says so (24.3) and does not close it; closing it would need the assurance-relevant configuration keys inside the hashed gate definitions or outside the working tree, which is an owner decision (open question OQ-13 of the register). Likewise the interpreter named by the configuration can be changed without a difference of the gate definitions; only the record shows which program ran.

## Known Stubs

None.

## Threat Flags

None beyond the register of the plan. T-02-26: exactly two exempt names, another name is measured (AE-282). T-02-27: `requirements` is a member of the hashed value and AE-286 mirrors AE-169. T-02-28: the recorded required level and the per-change ratchet are in the text, with the residual stated above. T-02-29: a held lock and not the existence of the file (AE-283). T-02-33: syntax, reserved names and case-fold uniqueness (AE-288).

## Unverified

- The lock semantics (an exclusive lock that the system releases when its holder ends) were not exercised on any file system; the text is a requirement and no implementation exists for it in this phase.
- No implementation was changed or run; the Python baseline was not run.
- Whether the ratchet of DC-130 for the approval kinds only, the text-valued evidence command of DC-125, and the identifier syntax of DC-133 are the right choices can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4).
- The register `02-DRAFTING-CHOICES.md` and the diff identity note `.planning/reviews/2026-10-24-normative-spec-diff-identity.md` were not edited by this plan; the identity note names a stale blob and will change again in plan 08.
- The text is draft; nothing here is approved or reviewed.

## Self-Check: PASSED

- The five commits `fe75577`, `94290c9`, `dcd3426`, `7060749` and `f59f2f8` are present in the log after `origin/main`, and all five start `docs(02-07): SPEC-`.
- The specification contains `**AE-282` to `**AE-289`, the strings `state.json.tmp`, `state.json.lock`, `#### Evidence Commands` and `required_level`.
