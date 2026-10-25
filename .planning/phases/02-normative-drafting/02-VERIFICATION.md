---
phase: 02-normative-drafting
verified: 2026-10-25T00:00:00Z
status: passed
score: 9/9 roadmap success criteria verified (SPEC-01 to SPEC-18 all specified in the text)
behavior_unverified: 0
overrides_applied: 1
overrides:
  - item: "All four human_verification items below (owner questions OQ-8 to OQ-15, exempt set of 24.1, header number and heading, independent review of the unproven items)"
    accepted_by: "repository owner, 2026-10-25, in reply to the question how to close Phase 2"
    reason: "These items are owned by Phase 3 (owner approval of the exact diff) and Phase 4 (independent review by Devin CLI). They stay open there and are not decided by closing Phase 2."
re_verification: false
gaps: []
deferred: []
human_verification:
  - test: "Owner decides owner questions OQ-8 to OQ-15 (register 02-DRAFTING-CHOICES.md, section 'Owner questions OQ-8 to OQ-15') and may overrule any conservative drafting choice DC-01 to DC-141"
    expected: "Each question gets an explicit owner answer, or the owner accepts the conservative reading in the text; recorded in the Phase 3 approval record"
    why_human: "Judgment calls the drafter was told to resolve conservatively and flag (CONTEXT D-10, D-15); only the repository owner can confirm them. Expected to stay open until Phase 3."
  - test: "Owner confirms the exempt set of Section 24.1 (cancel, supersede and the re-approval itself) against roadmap criterion 1, which says 'every operation except cancellation'"
    expected: "Owner accepts the wider exempt set, or asks for supersede and re-approval to be handled differently"
    why_human: "The text is wider than the criterion's wording (register: 'The exempt set of 24.1', DC-03, DC-44). It is needed for the move rule of Section 5.6 and for re-approval to be possible at all, but it is a semantic choice."
  - test: "Owner decides on the header number (Version 1.4, Revision 2026-10-25) and the qualified-term heading 'Protections Shared by Both Profiles' (check warning R8)"
    expected: "Number and heading kept, or changed at approval"
    why_human: "CONTEXT D-12 leaves the number to the owner; the R8 warning is a style heuristic, not a defect."
  - test: "Phase 4 independent reviewer examines the 'Unproven items' list of the register (SPEC-14 full realizations, SPEC-16 beyond the no-weakening check, SPEC-17, SPEC-18, anchor 'or equivalent' clause, A1 verifier, retry-limit-as-soft-failure, path pattern syntax, evaluation by group, and the others)"
    expected: "Independent findings with stable IDs; blocking findings fixed or dispositioned by the owner"
    why_human: "AGENTS.md requires owner approval and independent review by a non-Requestor for any change to the normative specification. Neither is part of Phase 2. The 02-REVIEW.md review was an advisory same-product review and is not independent."
---

# Phase 2: Normative Drafting Verification Report

**Phase Goal:** Produce a proposed diff to `docs/method/GG-SAD_normative_method_specification.md` that specifies the protections the prototype exercised and the two profiles, as proposed text only. No file under `src/ggsad/` is touched in this phase.
**Verified:** 2026-10-25
**Status:** human_needed (no gaps; only the owner and reviewer decisions that Phases 3 and 4 own)
**Re-verification:** No, initial verification
**Branch:** `gsd/v1.1-executable-core`, HEAD `6fe35ba`, 76 commits on `origin/main` (`d3e81a5`)

## Method

I did not rely on the plan summaries. I re-ran the phase check script with `--final`, recomputed the diff identity, diffed the branch against `origin/main` for scope, and read the specification text for every requirement (Sections 4.3, 5.3 to 5.6, 8, 22, 23, 24, 25). I also ran independent greps for the self-containment rules and recomputed the two hash examples. The deliverable is specification text, so "behavior" here means the rule text and its acceptance examples. The examples cannot be executed until the engine phases (5 to 8).

## Diff Identity

| Fact | Expected | Observed |
|---|---|---|
| Base blob (`origin/main`) | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` | same (check B1) |
| Result blob | `ed758c46d5ac901359ab2c0df8e437ef89fed0f1` | same, working file and HEAD (`git hash-object`) |
| SHA-256 | `45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3` | same (`sha256sum`) |
| Lines / diffstat | 4649; 3268 insertions, 41 deletions | same (check A1) |
| Working tree | clean | `git status --short` empty before and after my runs |

## Check Script (`02-check-normative-diff.sh --final`)

Run from the repository root. Result: `RESULT: PASS`. Passed: B1, E1, E2, E3, S1, S2, N1, X1, R5, R6, R2 (294 example blocks), R9 (AE-1 to AE-294, no gap, no repeat), J1 (2 JSON blocks parse), R3, R1, R7, C1, R4, F1 (41 `full` rule units, 11 protection rows), W1, D1 (44 of 44 review findings with exactly one disposition each, no CR or WR left RECORDED). Warnings only: X1 (the word "prototype" at line 345, which is base text in the `lean` row of Section 5.1) and two R8 lines (the heading and map row "Protections Shared by Both Profiles").

I did not take the script as proof. I confirmed its claims independently:

- All 294 defined example ids are unique, and every defined id is cited by a rule line (zero referenced-but-undefined, zero defined-but-uncited).
- AE-183 (`{"count":2,"name":"café"}`) and AE-184 (`{}`) hash to the stated values (`sha256sum` on the exact canonical bytes).
- The 35 lines removed from the base are the expected ones: the old header, the `state.yaml` references, the profile table that was renamed to compliance profiles, the old `reopen` and result-envelope wording, and YAML metadata examples. No base normative protection was dropped silently. Section 5.1's four profile rows are byte-identical to the base.

## Scope and Self-Containment (SPEC-13, D-09, D-11, D-15)

| Check | Evidence | Status |
|---|---|---|
| Nothing under `src/ggsad/` changed | `git diff origin/main HEAD -- src` empty; `git log origin/main..HEAD -- src` has 0 commits | VERIFIED |
| Only `docs/method/` and `.planning/` touched | `git diff --name-status origin/main HEAD` lists the specification plus 30 paths under `.planning/` (27 added, 3 modified); `git log --name-only` over all 76 commits shows no other path, so there is no touch-and-revert either | VERIFIED |
| `docs/decisions/`, `.ggsad/`, `specs/`, `tests/`, `AGENTS.md`, `CLAUDE.md` untouched | diff is empty for these | VERIFIED |
| No prototype ids (P-nn), no decision/requirement/finding ids (O-n, SPEC-nn, DC-nn, OQ-nn, CR/WR/IN-nn, D-nn, CHG-n), no commit hashes, no local paths, no `.planning` references in the specification | independent grep returns nothing; the only 64-hex tokens are the two example hashes of AE-183 and AE-184 | VERIFIED |
| No "prototype" reference added | the one hit (line 345) is base text; the diff's added lines contain none | VERIFIED |

## Goal Achievement: Observable Truths (ROADMAP success criteria)

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Gate definitions are fixed at approval; a later edit blocks every operation except cancellation until re-approved; three-valued results; unevaluable is never a failure and never counts toward a retry limit (SPEC-01, SPEC-02) | VERIFIED | 24.1 (lines 3099 to 3115): hash of parsed definitions compared before every state-changing operation, mismatch gives `rejected`, `changed` false, `gates-changed`; `cancel`, `supersede` and the re-approval are exempt; AE-75 to AE-86. 24.2 (3213 to 3261): `satisfied`, `not_satisfied`, `not_evaluable`; "MUST NOT be recorded as `not_satisfied`, MUST NOT make a fail gate active, MUST NOT count toward any retry limit"; retry-limit count rule at 3247; AE-61 to AE-74, AE-280. See the human note on the exempt set. |
| 2 | Normative fourth result `blocked` in 22.2; `rejected` means nothing written, never `changed` (SPEC-03) | VERIFIED | 22.2 (2171 to 2182): four exact-lowercase results, `blocked` is `changed: true`, `rejected` with `changed` true and `blocked` with `changed` false are invalid, only `close`/`resume` (core) and `complete`/`resume` (full) answer `blocked`. Per-action tables at 8.3 (898 to 911) and 23.4 (2467 to 2484). AE-111 to AE-120, AE-259. |
| 3 | Assurance levels A0 to A2 and the signed-approval statement are normative; verifiers optional; an agent able to use a human's credentials can act as that human (SPEC-04) | VERIFIED | 24.3 (3383 to 3430): levels and statement "normative. The verifiers are not"; statement fields (operation, change, version = history position, identity, details incl. content hash) built by the implementation; fail-closed; explicit sentence "An agent that is able to use a human's credentials can act as that human, and this holds at every level" (3430). AE-125 to AE-136, AE-289. |
| 4 | History consistency vs completeness with anchor requirement for high assurance; scope, how measured, isolation (SPEC-05, SPEC-06) | VERIFIED | 24.4 (3536 to 3567): consistency defined, "Consistency is not completeness", anchor required where configuration requires A2, truncated vs rewritten detection, anchor limit stated (AE-145). 24.5 (3657 to 3675): measured against the base revision incl. staged/unstaged/untracked-not-ignored, outside scope is a hard failure, ignored files invisible, change MUST run isolated and unrelated uncommitted work is not excluded. AE-137 to AE-157, AE-278, AE-282, AE-294. |
| 5 | Known-failure baselines; hard/soft failure with a bounded, recorded override (SPEC-07, SPEC-08) | VERIFIED | 24.6 (3773 to 3785): all on baseline gives `satisfied`, a new failure gives `not_satisfied` and is named (max three, code point order), unreadable gives `not_evaluable`; baseline frozen with the gates. 24.7 (3867 to 3884): hard closes as failed without human action; soft waits for `fail` or an override (reason required, N is an integer of at least 1, no default, bound to the approved hash, lapses when attempts are used up or the gates are amended). AE-87 to AE-110, AE-279. |
| 6 | Open questions as state with structured answers blocking approval and closure; evidence executable and tied to a requirement; interpreter explicit and opt-in with trust consequence (SPEC-09, SPEC-10, SPEC-11) | VERIFIED | 24.8 (4006 to 4028): fields incl. `options`; unanswered question rejects spec approval (`open-questions`) and blocks closure; acceptance only by recorded answer. 24.9 (4126 to 4142): no requirements means no complete evidence; each requirement needs a bound evidence command. 24.10 (4208 to 4218): no shell, `@interpreter` opt-in, no discovery, and "Code in a location that version control is told to ignore is invisible to the scope check". AE-158 to AE-182. |
| 7 | Both profiles specified; applicability and movement between them; `full` revised to carry the protections, marked specified-but-not-implemented, an acceptance example per `full` rule (SPEC-12, SPEC-14) | VERIFIED | 5.6 (550 to 579): `core`/`full` as a second axis, exactly one of each per change, applicability table, move by new change plus `supersede`, `full` "specified but not implemented" (571). Section 23 specifies `core` (documents, 4 states, 3 outcomes, gates, 11-row transition table, wait records, evaluation order, 4 base gates). Section 24 intro (2973 to 2991): realization table, 11 rows, `core` and `full` columns. `full` sections 6 to 10 and 8 carry "This section specifies the `full` method profile". F1: 41 rule units each with a `Covers:` example (I read samples for 4.1, 6.1 to 6.3, 7.1 flows, 9.4/10.4, 11.2, 12.2; each has a normal and a failure/boundary case in Given/When/Then). |
| 8 | State is JSON (`state.json`) with canonical hashing form; six-layer resolution with `core` implementing four; `reopen` for `full` only; `schema_version` with explicit recorded migration (SPEC-15 to SPEC-18) | VERIFIED | 25.1 (4266 to 4319): `state.json`, entry fields `n/prev/body/hash`, canonical form (sorted code-point keys, no whitespace, integers only, defined escapes), atomic write, lock; 25.2 content hash; 4.3 (293 to 319) updated to `state.json`; the only `state.yaml` left is the migration source in 25.3 (4553, AE-214). 5.3 (373 to 394): six layers, `core` implements layers 1, 2, 3, 5, no weakening, layers never renumbered; AE-218 to AE-228, AE-290. Reopen: 8.3 row (896) "`full` only", 8.4 (1024), 23.4 (2463) "The method profile `core` has no `reopen` action", AE-48, AE-217, AE-246. 25.3 (4529 to 4553): `schema_version` format and ordering, `migrate` is the only way, never silent, recorded per step, unknown version refused (`migration-required`, `schema-version-unsupported`, `schema-version-mismatch`); AE-203 to AE-214. |
| 9 | No file under `src/ggsad/` modified (SPEC-13) | VERIFIED | See Scope table: empty diff, 0 commits touching `src`, S1 and S2 pass. |

**Score:** 9/9 truths verified. 0 present-but-behavior-unverified. The acceptance examples are not executed; the engine phases will do that (ENG, TRUST, INTEG, WORK, VERIFY).

## Requirements Coverage

| Requirement | Where specified | Examples | Status |
|---|---|---|---|
| SPEC-01 | 24.1 | AE-75 to AE-86 | SATISFIED |
| SPEC-02 | 24.2, 8.5, 23.6 | AE-61 to AE-74, AE-280 | SATISFIED |
| SPEC-03 | 22.2, 22.3, 8.3, 23.4 | AE-111 to AE-120, AE-259 | SATISFIED |
| SPEC-04 | 24.3, 5.4 | AE-125 to AE-136, AE-289, AE-292, AE-293 | SATISFIED |
| SPEC-05 | 24.4 | AE-137 to AE-146, AE-278 | SATISFIED |
| SPEC-06 | 24.5 | AE-147 to AE-157, AE-253, AE-282, AE-294 | SATISFIED |
| SPEC-07 | 24.6 | AE-87 to AE-96, AE-254 | SATISFIED |
| SPEC-08 | 24.7 | AE-97 to AE-110, AE-255, AE-279 | SATISFIED |
| SPEC-09 | 24.8, 23.4 `ask`/`answer` | AE-171 to AE-182, AE-256 | SATISFIED |
| SPEC-10 | 24.9, 23.7 | AE-163 to AE-170, AE-257, AE-286 | SATISFIED |
| SPEC-11 | 24.10 | AE-158 to AE-162, AE-258 | SATISFIED |
| SPEC-12 | 5.6, 23, applicability table | AE-01 to AE-08, AE-09 to AE-59, AE-291 | SATISFIED in text; see bookkeeping note |
| SPEC-13 | n/a (diff scope) | n/a | SATISFIED |
| SPEC-14 | Section 24 realization table, `full` sections with markers, 41 rule-unit examples | AE-229 to AE-269 and others | SATISFIED |
| SPEC-15 | 25.1, 25.2, 4.3 | AE-183 to AE-202 | SATISFIED |
| SPEC-16 | 5.3 | AE-218 to AE-228, AE-290 | SATISFIED |
| SPEC-17 | 8.3, 8.4, 23.4 | AE-48, AE-217, AE-246 | SATISFIED |
| SPEC-18 | 25.3, 22.2 | AE-203 to AE-214 | SATISFIED |

No orphaned requirement: every SPEC id (01 to 18) is claimed in the roadmap and has text. APPR-01, REVIEW-01 and REVIEW-02 belong to Phases 3 and 4 and are correctly untouched.

## Decision Conformance (O-1 to O-11, D-01 to D-15)

| Decision | Status | Evidence |
|---|---|---|
| O-1 both profiles kept | VERIFIED | 5.6, 23, 24 |
| O-2 profile resolution and gate engine back in scope | VERIFIED | 5.3 specified; CI scope is Phase 7 |
| O-3 levels and statement normative, verifiers optional | VERIFIED | 24.3 |
| O-4 state moves to JSON | VERIFIED | 25.1; `state.yaml` survives only as migration source |
| O-5 `blocked` normative | VERIFIED | 22.2 |
| O-6 `reopen` in `full`, not in `core` | VERIFIED | 8.3, 8.4, 23.4 |
| O-7 `schema_version`, refuse unknown, explicit recorded migration | VERIFIED | 25.3 |
| O-8 `full` specified, not built, marked | VERIFIED | 5.6 (571), 24 (2973) |
| O-9 protections are invariants of both profiles | VERIFIED | 24 intro and realization table |
| O-10 `core` implements four layers | VERIFIED | 5.3 |
| O-11 CI verify-only | NOT IN THIS PHASE | Implementation (WORK-04), not a SPEC requirement |
| D-01/D-02 edit file on branch, identity by blob and SHA-256 | VERIFIED | Identity table; note `.planning/reviews/2026-10-24-normative-spec-diff-identity.md` |
| D-03 one commit group per requirement, ids in subjects | VERIFIED | check C1 passes over 36 specification commits |
| D-04 to D-07 method vs compliance profiles, six layers, fixed method profile, move by supersede | VERIFIED | 5.1 unchanged, 5.2, 5.3, 5.6 |
| D-09 lean read-only check script | VERIFIED | script present, read-only (temp dir only), `--final` passes |
| D-10 conservative readings listed for Phase 3 | VERIFIED | register DC-01 to DC-141, OQ-1 to OQ-15 |
| D-11 ripple files not touched, hand-off list recorded | VERIFIED | diff scope; register "Hand-off list" |
| D-12 header Version 1.4 and Revision line | VERIFIED | lines 3 to 5 (R4 passes) |
| D-13/D-14 examples inline, ids AE-nn, one set per rule unit (about 40) | VERIFIED | 41 units, 294 examples |
| D-15 specification cites no development artifacts | VERIFIED | independent grep |

## Anti-Patterns

Debt-marker scan on the specification and the phase notes: no `TBD`, `FIXME`, `XXX` (check R3 passes, no unfinished-text markers outside code fences). No placeholders. No tabs, no CRLF, UTF-8 without BOM (E1 to E3). No blocker.

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| specification | 61, 2950 | "Both Profiles" without a qualifier (check R8) | Info | Style under D-05; heading and map row. Owner can leave it. |
| `.planning/REQUIREMENTS.md` | 36, 129 | SPEC-12 still `[ ]` / `Pending` while all other SPEC ids are `[x]` / `Complete` | Warning (bookkeeping) | The text satisfies SPEC-12. The 02-01 and 02-05 summaries deliberately left it open "for the phase verification". The file was not edited here (instruction), so the orchestrator should tick SPEC-12 and set the traceability row to Complete when it closes the phase. |

## Spot Checks of Internal Consistency (adversarial)

I looked for contradictions between the new sections and the amended old ones. None found in these places:

- 22.2, 8.3, 23.4 and 24.7 agree on which actions answer `blocked` and that a hard-failure close answers `success`.
- 23.6, 24.2 and 8.5 agree on the evaluation order and on group evaluation with early stop (AE-280).
- 23.7 base gates and 5.3's weakening check use the same identifiers; `gate-weakened` is the same code in 5.3 and in AE-219 to AE-228.
- 24.4 anchor creation at `new` (position 1) agrees with 23.4 `new` and with `adopt` (AE-278).
- 24.5 exempt names (`state.json.tmp`, `state.json.lock`) agree with 25.1's write protocol.
- 25.3's version-mismatch check order agrees with 22.2's issue-code list.
- The 44 review findings (3 critical, 27 warnings, 14 info) each have one row in the register (D1); the critical ones are visibly addressed in the text: CR-01 (`review` gate kind rejected, 23.3, AE-272), CR-02 (crash artifacts exempt from the scope check and the write protocol in 25.1, AE-282/283), CR-03 (requirements and evidence commands in the frozen `full` set, 24 intro, AE-286).

## Human Verification Required

These are not defects. They are the decisions the phase deliberately left to Phases 3 and 4.

### 1. Owner questions OQ-8 to OQ-15 and conservative drafting choices

**Test:** Owner reads the register sections "Owner questions OQ-8 to OQ-15", "Dispositions of the open questions OQ-1 to OQ-7", and the DC tables (DC-01 to DC-141) and answers or accepts each.
**Expected:** Explicit answers recorded in the Phase 3 approval record.
**Why human:** CONTEXT D-10 and D-15 tell the drafter to take the most conservative reading and flag it. Open by design. The eight questions are: restore a `review` gate kind (CR-01), combination mode for `core` (WR-18), stricter compliance profile than the project's (WR-19), agent self-approval under `lean` (WR-20), assurance floor for the 5.4 decisions (WR-21), protection of assurance-relevant configuration beyond the ratchet (WR-24), a question staying open before the specify Definition of Done (WR-25), an opt-out for the allowed path list in `full` (WR-26).

### 2. Exempt set of Section 24.1

**Test:** Owner confirms that `supersede` and the re-approval itself are exempt from the gates-changed comparison, in addition to `cancel`.
**Expected:** Accepted, or a different rule requested.
**Why human:** Roadmap criterion 1 words it as "every operation except cancellation". The text exempts three operations. The register records why (the move rule needs `supersede`, and re-approval cannot work otherwise).

### 3. Header number and heading wording

**Test:** Owner keeps or changes Version 1.4 and the heading "Protections Shared by Both Profiles".
**Why human:** Owner preference (D-12, D-05).

### 4. Independent review (Phase 4) of the unproven items

**Test:** The non-Requestor reviewer evaluates the register's "Unproven items" list.
**Why human:** Required by `AGENTS.md`. The advisory review in `02-REVIEW.md` was by the Requestor's own side and does not count as independent.

## Gaps Summary

No gaps. All nine roadmap success criteria and all eighteen SPEC requirements are specified in the text with rules and acceptance examples. The artifact matches the recorded identity (blob `ed758c46...`, SHA-256 `45ba09d9...`), the check script passes with `--final`, nothing outside `docs/method/` and `.planning/` changed, `src/ggsad/` is untouched in all 76 commits, and the specification cites no prototype ids, decision ids, commit hashes or local paths.

Open items are the owner and reviewer decisions of Phases 3 and 4, plus one bookkeeping step for the orchestrator: mark SPEC-12 Complete in `.planning/REQUIREMENTS.md` (checkbox at line 36, traceability row at line 129).

Any edit to the specification after this report voids the identity values above and requires re-running `02-check-normative-diff.sh --final` and re-recording the identity note.

---

_Verified: 2026-10-25_
_Verifier: Claude (gsd-verifier)_
