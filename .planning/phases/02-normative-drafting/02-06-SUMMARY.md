---
phase: 02-normative-drafting
plan: 06
subsystem: normative-spec
tags: [gap-closure, review-findings, core-gates, evaluation-order, wait-records, anchor, applicability, bash-check]
status: complete
gap_closure: true

requires:
  - phase: 02-normative-drafting
    provides: "Plan 05: the six-layer resolution, the realization table, 41 full rule examples, Version 1.4, the check script with --final, the register DC-01 to DC-107"
provides:
  - "Check script: R9 (the AE ids are exactly AE-1 to AE-N, no gap, no repeat, fails in every mode) and J1 (every json fence parses, python3 -I, else python, else node, else a warning)"
  - "Applicability fixes in 5.6, 11.2, 12.1, 19, 20 and the template of 11.2 (core is not asked to run steps it lacks)"
  - "The core gate model: done-gate kinds check and sign-off, one form of condition for a fail or wait gate, ask from waiting, wait names an existing question, stale approval only after a first approval, wait records made by evaluation, the anchor of a new change"
  - "Evaluation by group with early stop, start never closes a change, complete has a legal source as its only precondition, the value domain of gate_results"
  - "AE-270 to AE-281 (12 examples; the specification now holds AE-1 to AE-281)"
affects: [Plan 07, Plan 08, Phase 3 owner approval, Phase 4 independent review]

actuals:
  tokens: 7500
  tasks: 3
  commits: 5

tech-stack:
  added: []
  patterns: ["finding ids live in commit subjects, plans, this summary and the register, never in the specification", "a group of gates is evaluated whole and the evaluation stops after the first group that decides"]

key-files:
  created: []
  modified:
    - docs/method/GG-SAD_normative_method_specification.md
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh

key-decisions:
  - "No owner decision was made. The conservative readings are listed under Drafting choices (DC-108 to DC-122) for the Phase 3 packet."

patterns-established:
  - "Each fix is a numbered drafting choice with an acceptance example whose id is cited by a rule line (See AE-nnn)."

requirements-completed: []  # the specification is proposed text; nothing here is approved or reviewed.

duration: "one session, not timed"
completed: 2026-10-24
---

# Phase 2 Plan 06: Review Findings, Part 1 (applicability, core gates, evaluation order) Summary

**Closes CR-01, WR-01 to WR-11, WR-13 and four info items of the advisory review in the proposed text: the unrealizable `review` gate kind is removed, a `core` fail or wait gate has exactly one form of condition, gates are evaluated by group with an early stop, `start` never closes a change, and the check script now guards the AE numbering (R9) and the JSON blocks (J1). The specification holds AE-1 to AE-281 and `--final` prints RESULT: PASS.**

## Accomplishments

- Check script: R9 fails when the ids of the lines `**AE-nn — ` outside fences are not exactly AE-1 to AE-N (it prints N, here 281). J1 parses every `json` fence with `python3 -I`, else `python`, else `node`; with none it prints `WARN J1 no JSON parser, blocks not parsed`, which is not counted. The usage comment names both.
- Applicability (WR-03, WR-04, WR-05, IN-06, IN-09): 11.1 leaves the `full`-only row of 5.6; the row for 11.2 and 12.2 also exempts `core` from the required response, the permitted preservation actions and the required documentation of a fail rule; sections 19 and 20 each gain a paragraph "For a `core` change" that maps the steps and the completion conditions to 23.6, 23.7 and the `close` action; 12.1 reads "exceeding a hard budget or cost limit"; the template of 11.2 uses `owner`, adds `outstanding` and `"resume_at": "plan"`, and a sentence lists the six fields.
- Gate model (CR-01, WR-06): the done-gate kinds are `check` and `sign-off`; "A done gate of the kind `review` is invalid" and is rejected; the pointer to Section 3.10 is gone. A fail or wait gate has no kind and a `condition` that holds exactly one of `command` (with `exit_map`, optional `time_limit`), `retry_limit` (with `gate` and `limit`) or `predicate`; 24.2 evaluates a command condition as a check command without a baseline; 23.7 gives each base gate its predicate and says the 5.3 check of the base identifiers comes first.
- Actions and records (WR-08, WR-09, WR-10, IN-13): `ask` is legal from `open`, `active`, `waiting`; `wait` names an existing unanswered question and never creates one, takes its owner and defaults its reason and resume condition; the stale approval gate is active only after a first approval and only while the hash differs from the last approved one; the evaluation-made records of kind `fail-gate` and `external` have a stated owner, `resume_when` and `reason`.
- Anchor (WR-11): the first append of `new` creates the anchor at position 1 where one is kept or required; `adopt` serves a history that has entries and no anchor.
- Evaluation and results (WR-01, WR-02, WR-07, WR-13, IN-03): `start` never closes a change (rejected, `changed` false, `start-blocked`); the precondition of `complete` is a legal source plus a requested evaluation; 24.2 evaluates by group, a group whole, and "a gate of a later group is not evaluated" once an earlier group decides, with one pointer sentence each in 8.5 and 23.6; `gate_results` holds the three results or the marker `not_applicable`; AE-102 states the unsatisfied done gate.
- Examples AE-270 to AE-281, each cited by a rule line; AE-222, AE-223 and AE-102 reworded. No `Covers:` line of an F1 unit changed (F1 still reports 41 units).

## Task Commits

1. Task 1, script: `04a7ccf` docs(02-06): extend normative diff check script (R9, J1)
2. Task 1, spec: `d88ab49` docs(02-06): SPEC-12 fix WR-03 WR-04 WR-05 IN-06 IN-09 applicability of sections 11 to 20 (AE-270, AE-271)
3. Task 2 (1): `7228ae1` docs(02-06): SPEC-12 SPEC-09 SPEC-04 fix CR-01 WR-06 WR-08 WR-09 WR-10 IN-13 core gates, actions and wait records (AE-272 to AE-277)
4. Task 2 (2): `2f00f44` docs(02-06): SPEC-05 fix WR-11 anchor of a new change (AE-278)
5. Task 3: `5f92395` docs(02-06): SPEC-02 SPEC-03 SPEC-08 SPEC-15 fix WR-01 WR-02 WR-07 WR-13 IN-03 evaluation order and results (AE-279 to AE-281)

This summary and the planning-state update are committed separately after it. The plan has no human checkpoint, so no stop was made at the tracer gate; the tracer commands (R9 and J1 seeded runs, section greps, `--final`) passed before the applicability commit.

## Verification

- `bash -n` exits 0; `shellcheck` exits 0 with no finding.
- Seeded defects on throwaway copies of the specification outside the repository (`--file`; the copies were deleted): renumbering AE-100 to AE-1000 printed `FAIL R9 AE-100 is missing (the ids stop at AE-1000, 269 blocks)` and the run exited 1; deleting the closing brace of the first json fence printed `FAIL J1 the json block at line 809 does not parse`; the untouched file printed `PASS R9 the ids AE-1 to AE-269 ...` and `PASS J1 2 json block(s) parse` (at that time).
- Section greps after the last commit: `--section 5.6 | grep -c '11\.1'` is 0 and `grep -c 'permitted preservation actions'` is 1; sections 19 and 20 each contain "For a `core` change" once; `--section 12.1 | grep -c 'retry limits'` is 0; `--section 11.2` has 0 `waiting_for` and 1 `"resume_at": "plan"`; `--section 23.3` has 0 "Section 3.10", 1 "A done gate of the kind `review` is invalid", and contains `retry_limit`, `predicate`, `exit_map`, `scope-violation`; `--section 23.4` has 1 row `| `ask` | `open`, `active`, `waiting` |` and 1 "is not `open`, `active`, or `waiting`"; `grep -c 'gave a question\|gives a question'` of the specification is 0; `--section 23.7` contains "approved at least once"; `--section 24.4` contains "position 1"; `--section 24.7` contains `start-blocked`; `--section 24.2` contains "a gate of a later group is not evaluated"; `--section 8.3 | grep -c 'applicable precondition is not satisfied'` is 0; `--section 25.1` contains "marker `not_applicable`".
- Example counts: `grep -c '^\*\*AE-'` printed 271 after the first spec commit, 277 after the third and 278 after the fourth, as the plan states, and 281 after the last; the id AE-281 is the highest (the blocks are not in document order, DC-39).
- `bash CHK --final` printed RESULT: PASS after every spec commit; the final run printed `PASS R9` (N = 281), `PASS J1`, `PASS R2` (281 blocks), `PASS F1` (41 units) and the A1 facts: result blob `1112418e2235ef96511714af75a618963f46612d` (working file and HEAD equal), SHA-256 `6e2700ecdea03ad24376e5e70d501932b9804979aeed3cc25171e7886e88ef36`. Warnings only: `WARN X1` (the word "prototypes" in existing text) and two `WARN R8` on the heading and map row "Protections Shared by Both Profiles".
- `bash CHK --ids SPEC-02,SPEC-03,SPEC-04,SPEC-05,SPEC-08,SPEC-09,SPEC-12,SPEC-15` printed `PASS C1` and RESULT: PASS.
- `git diff --name-only origin/main...HEAD` lists the specification and paths under `.planning/` only; limited to `src .ggsad specs tests AGENTS.md CLAUDE.md` it prints nothing; `git status --short` was empty after every commit.
- A grep of the specification for the forms CR-, WR-, IN-, DC- followed by digits found nothing (X1 also passes). Python baseline: not run (no Python changed).

## Deviations from Plan

**1. [Rule 1 - Bug] AE-224 named a done gate without a kind.**
- **Found during:** Task 2.
- **Issue:** Once a done gate has to have exactly one kind, the done gate `review-ok` of AE-224 (a strengthening listed before a weakening) would itself be invalid, which muddles the reason for the rejection.
- **Fix:** "the done gate `review-ok` of the kind `sign-off`" (one phrase; the plan lists AE-222, AE-223 and AE-102 as reworded and does not name AE-224).
- **Commit:** `7228ae1`

**2. [Plan reading] `gate_detail` values stay text.** The plan row says the values of `gate_results` and `gate_detail` are the three results or the marker. A cause or a failure name is text, not a result, so the domain is stated for `gate_results` only and `gate_detail` is limited to gates that have a value in `gate_results` (DC-121).

**3. [Plan reading] `retry_limit` is a condition of a fail gate only,** because 24.2 and 24.7 define a retry limit as a fail condition of the severity `soft` (DC-112).

**4. [Plan reading] Pointer sentences, not rewrites.** The sentences "stop as soon as a gate decides" in 8.5 and 23.6 stay; each section gains one sentence that points to the group rule of 24.2. 24.2 also gains one clause in the sentence on `start` (a hard failure included, because `start` never closes a change).

**5. [Plan reading] Commit order.** The anchor text (WR-11) was drafted with the first group of edits and held back from the third commit so that the example counts 277 and 278 match the plan; the tree after the fourth commit is the same as drafted.

Otherwise the plan was executed as written.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. They continue the register `02-DRAFTING-CHOICES.md` (DC-01 to DC-107), which this plan does not edit.

- **DC-108 (WR-03, 5.6):** 11.1 is removed from the `full`-only row and falls under "every other section", so it applies to both method profiles. AE-52 stays.
- **DC-109 (WR-04, 19, 20):** The two sections stay in "both". Each gains a paragraph for a `core` change. For section 20 the fail, wait, soft failure, question, done criteria and evidence conditions are mapped to gates; the conditions about the requirement coverage table, Pair Review, document consistency and references are said to be met through the requirements and gates of the change, with no document of the `full` method profile required. This last mapping is the broadest reading and is for the owner to confirm. Example AE-270.
- **DC-110 (WR-05, 5.6, 23.3):** `core` is exempt from the required response, the permitted preservation actions and the required documentation of 12.2; a `core` fail gate holds `id`, `severity`, `condition`; the response is fixed by 24.7. AE-271.
- **DC-111 (CR-01, 23.3):** The kind `review` is dropped, not realized. A review before closure is a `sign-off` gate or a `check` gate; the records of 14.5 are evidence that no gate evaluates; the read-only action `review` is unchanged. The other option in the finding (a `review-result` action with a recorded reviewer, revision and result) would add an operation to 22.1 and a field to 25.1 and is left to the owner: the register of Phase 3 should list it as an open question. AE-272.
- **DC-112 (WR-06, 23.3, 23.7, 24.2):** A fail or wait gate has no kind and one `condition` with exactly one of the members `command` (plus `exit_map`, optional `time_limit`), `retry_limit` (a mapping with `gate`, a `check` done gate, and `limit`; fail gate only) or `predicate` (`scope-violation` on a fail gate; `unanswered-question`, `stale-spec-approval` on a wait gate). None, two, another member, or a predicate not listed for the kind is rejected at `new`; values (a bad limit, a missing exit map) are rejected at the approval of the gate definitions, as before. A command condition is evaluated as a check command and carries no baseline (24.6). The base gates are fixed in 23.7 and are not subject to the kind and form rules; the 5.3 check of the base identifiers comes first. AE-273; AE-222 and AE-223 state their conditions in these forms.
- **DC-113 (WR-08, 23.4):** `ask` is legal from `open`, `active` and `waiting`; a question asked while waiting leaves the wait record unchanged and blocks `resume` through the unanswered question gate. AE-274.
- **DC-114 (WR-09, 23.4, 23.5, 24.8):** `wait` names an existing unanswered question and never creates one; the wait owner is the question's owner and another owner is rejected; reason and resume condition default to awaiting the answer; an answered or unknown question is rejected. AE-29 stays valid. AE-275.
- **DC-115 (WR-10, 23.7, 24.3):** The stale approval gate is active only if the specification was approved at least once and its hash differs from the last approved hash; a never-approved specification does not stop `start`. AE-276.
- **DC-116 (WR-11, 23.4, 24.4):** The entry of `new` creates the anchor at position 1 where one is kept or required; this is not a replacement. `adopt` serves a history with entries and no anchor. AE-278; AE-140 stays.
- **DC-117 (IN-13, 23.5):** For a record made by evaluation, `owner` is the owner of the change, `resume_when` is `a human recorded an override of <id>` (`fail-gate`) or `gate <id> can be evaluated` (`external`), and `reason` names the gate and the cause. Who may `resume` such a record is not restated. AE-277.
- **DC-118 (WR-01, 24.7, 24.2):** `start` never closes a change; with a hard fail gate active it is rejected (`changed` false, `start-blocked`) and the failure is decided by `cancel`, `supersede` or the first completing or resuming action. AE-279.
- **DC-119 (WR-02, 8.3):** The precondition of `complete` is a legal source plus the requested evaluation of the DoR (from `draft`), the DoD (from `active`) or the next DoR (from `done`); the rejection cell and the result table reject only a source that is not legal; evaluation outcomes stay `blocked`. AE-121 and AE-122 stay.
- **DC-120 (WR-07, 24.2, 8.5, 23.6):** The intent is "stop by group": the groups are the fail, wait and done gates (`core`) and DoF, DoW, DoR, DoD, next DoR (`full`, order of 8.5); a group is evaluated whole; a gate of a later group is not evaluated (no command run, no result); the rules 1 to 5 rank the results of the gates that were evaluated. Consequence: in `core` an active wait gate decides before an unevaluable done gate (`blocked`, no wait record), and an unevaluable wait gate gives an `external` wait. The other option (evaluate every gate first, then rank) would run commands of gates that cannot matter. AE-248, AE-55 and AE-69 stay true; a known hard failure keeps rank 1. AE-280.
- **DC-121 (WR-13, 24.2, 25.1):** `gate_results` values are the three results in exact lowercase or the marker `not_applicable`; `gate_detail` is text for a gate that has a value in `gate_results`; the rejection rule of 24.2 applies to a record of a result. AE-61 stays. AE-281.
- **DC-122 (IN-03, IN-06, IN-09):** AE-102 states "a done gate that stays unsatisfied"; 12.1 lists only a hard budget or cost limit among the fail categories (the retry limit stays a soft condition in the next paragraph); the 11.2 template uses `owner`, adds `outstanding`, and sets `resume_at` to `plan`, with a sentence that lists the six fields and says `resume_at` holds a phase identifier of Section 7. AE-268 names the fields.

## Findings closed

| Finding | Disposition | Commit | Example | Choice |
|---|---|---|---|---|
| WR-03 | FIXED | `d88ab49` | AE-52 | DC-108 |
| WR-04 | FIXED | `d88ab49` | AE-270 | DC-109 |
| WR-05 | FIXED | `d88ab49` | AE-271 | DC-110 |
| CR-01 | FIXED-CONSERVATIVE | `7228ae1` | AE-272 | DC-111 |
| WR-06 | FIXED-CONSERVATIVE | `7228ae1` | AE-273 (AE-222, AE-223) | DC-112 |
| WR-08 | FIXED | `7228ae1` | AE-274 | DC-113 |
| WR-09 | FIXED | `7228ae1` | AE-275 | DC-114 |
| WR-10 | FIXED | `7228ae1` | AE-276 | DC-115 |
| WR-11 | FIXED | `2f00f44` | AE-278 | DC-116 |
| WR-01 | FIXED | `5f92395` | AE-279 | DC-118 |
| WR-02 | FIXED | `5f92395` | AE-121, AE-122 | DC-119 |
| WR-07 | FIXED-CONSERVATIVE | `5f92395` | AE-280 | DC-120 |
| WR-13 | FIXED | `5f92395` | AE-281 | DC-121 |
| IN-13 | FIXED | `7228ae1` | AE-277 | DC-117 |
| IN-06 | FIXED | `d88ab49` | - | DC-122 |
| IN-09 | FIXED | `d88ab49` | AE-268 | DC-122 |
| IN-03 | FIXED | `5f92395` | AE-102 | DC-122 |

That is 13 findings (CR-01, WR-01 to WR-11, WR-13) and 4 info items (IN-03, IN-06, IN-09, IN-13). CR-02, CR-03, WR-12, WR-14 onward and the other info items belong to plans 07 and 08.

## Known Stubs

None.

## Threat Flags

None beyond the register of the plan. T-02-22: rank 1 stays first, examples exist for the stop and the no-stop case (AE-280, AE-69, AE-248), and `--final` passed after each commit. T-02-23: reviews move to the human `sign-off` gate or a `check` gate, and the open question is recorded under DC-111. T-02-24: both new checks were proven with seeded defects, and J1 degrades to a warning, never to a pass. T-02-25: no finding, choice or decision id is in the specification.

## Unverified

- The J1 fallbacks to `python` and `node`, and the warning when no parser exists, were not exercised; only the `python3 -I` path ran, on this machine.
- Whether the group reading of 24.2 (DC-120), the omission of the kind `review` instead of a recording mechanism (DC-111), the fail-gate-only `retry_limit` (DC-112) and the broad mapping of section 20 (DC-109) are the right choices can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4).
- The register `02-DRAFTING-CHOICES.md` and the diff identity note `.planning/reviews/2026-10-24-normative-spec-diff-identity.md` were not edited by this plan. The identity note still names the blob `78ac13fd...` of plan 05, which is stale: the text is now blob `1112418e...` and will change again in plans 07 and 08.
- The text is draft; nothing here is approved or reviewed.

## Self-Check: PASSED

- The five commits `04a7ccf`, `d88ab49`, `7228ae1`, `2f00f44` and `5f92395` are present in the log after `origin/main`, and four of them start `docs(02-06): SPEC-`.
- The specification contains `**AE-270` to `**AE-281` and the phrase "A done gate of the kind `review` is invalid"; the check script contains R9 and J1.
