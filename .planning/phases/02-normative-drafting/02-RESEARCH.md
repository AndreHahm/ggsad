# Phase 2: Normative Drafting - Research

**Researched:** 2026-10-24
**Domain:** Amending one normative Markdown specification (a spec impact map, not a technology survey)
**Confidence:** HIGH for spec line facts and prototype facts (every cited file was read this session); MEDIUM for placement and ordering advice (judgment); LOW for the content of SPEC-14, SPEC-16, SPEC-17 and SPEC-18 (the prototype gives little or no evidence for them)

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** The proposed text is written by editing `docs/method/GG-SAD_normative_method_specification.md` directly on the milestone branch (`gsd/v1.1-executable-core`). The diff is that file on the branch versus `origin/main`; no separate patch file is the artifact. `main` stays untouched until a pull request is merged. — **Reversibility:** reversible — a draft on a branch can be rewritten or reset before approval.
- **D-02:** The exact diff is identified for Phase 3 approval and Phase 4 review by git blob ids and SHA-256 recorded at the end of Phase 2 (the base blob on `origin/main` and the result blob), as Phase 1 did for the decision record. Commit hashes or ranges are not used as the identity, because a rebase merge rewrites them. Any later edit to the file invalidates the recorded values and requires recording new ones.
- **D-03:** Commits on the spec file are one per requirement (SPEC-01 to SPEC-18); closely related requirements may share a commit when separating them would leave an inconsistent text. Each commit subject names its requirement ids so a review finding maps to a commit.
- **D-04:** The new method profiles `core` and `full` (O-1) and the existing compliance profiles of section 5.1 (`lean`, `standard`, `governed`, `regulated`) are separate axes. A project/change selects a method profile and a compliance profile; both are resolved in the section 5.3 order. The compliance profiles are kept unchanged. — **Reversibility:** costly — every later phase and the engine design cite this structure.
- **D-05:** The specification uses qualified terms, "method profile" for `core`/`full` and "compliance profile" for `lean` to `regulated`, wherever a bare "profile" would be ambiguous. The owner's O-1 wording ("profiles") is kept; no renaming (a rename would need a new dated owner decision in the record).
- **D-06:** In the six-layer resolution order of section 5.3 (SPEC-16, O-10), layer 2 "selected profile" means the pair method profile plus compliance profile, resolved together. The count stays six layers, and `core` implements layers 1, 2, 3 and 5 (invariant core, selected profile, project configuration, the change's own gates), exactly as O-10 decides. No seventh layer.
- **D-07:** A change's method profile is fixed when the change is created. To move between `core` and `full`, create a new change in the other profile and supersede the old one with the existing `supersede` action; no in-place switch and no mapping of the four `core` states onto the `full` phases is specified. — **Reversibility:** costly — an in-place switch could be added later only by a new dated owner decision plus a state mapping.
- **D-08:** Phase 2 is planned as five theme plans, one wave each (all edit the same file, so they run in sequence): (1) profile vocabulary (SPEC-12); (2) gates and results (SPEC-01, 02, 03, 07, 08); (3) trust and integrity (SPEC-04, 05, 06, 09, 10, 11); (4) state and versioning (SPEC-15, 17, 18); (5) full-profile revision and resolution (SPEC-14, 16). SPEC-13 is a check in every plan, not a plan. SPEC-16, unproven by the prototype beyond a base-gate no-weakening check, is planned with its own acceptance examples in the last plan.
- **D-09:** Phase 2 includes a lean read-only check script, in the style of Phase 1's `01-check-decision-record.sh`. Its checks include: every SPEC id has a commit naming it; nothing under `src/ggsad/` changed; only `docs/method/` and `.planning/` are touched; normative-term and cross-reference sanity; LF endings and UTF-8 without BOM. The exact check list is the planner's choice.
- **D-10:** When the drafter meets an ambiguity that O-1 to O-11 do not settle, it drafts the most conservative reading, lists it in a per-plan "Drafting choices" list, and continues. Those lists are carried into the Phase 3 approval packet so the owner can overrule each choice at approval. The drafter does not stop execution for these and does not leave them as open questions in the normative text.
- **D-11:** Phase 2 touches only the specification text. Examples and templates written inside the specification are updated for `state.json` (SPEC-15). `specs/examples/class-m/state.yaml`, `.ggsad/templates/`, `.ggsad/schemas/state.schema.json` and the archived CHG-001 state are not changed in this phase, because the current implementation and tests validate them; they go on a hand-off list recorded for the engine phases (5 to 8).
- **D-12:** The specification's header is drafted as Version 1.4 with a new Revision line describing the change. The packet for Phase 3 states the number so the owner can change it at approval. — **Reversibility:** reversible — one header line.
- **D-13:** Acceptance examples for the `full` rules (SPEC-14) are written inline under each rule in Given/When/Then form, each with an id (for example AE-nn) that the rule cites, covering normal and failure/boundary behavior as section 3.9 requires, so rule, example and verification evidence stay traceable.

### Claude's Discretion

- The order of requirement commits inside a plan, the exact checks of the lean script, the numbering and placement of new subsections and acceptance example ids, and the exact wording of rules, provided they follow D-01 to D-13, the section 2 normative terms and the Phase 1 record.

### Deferred Ideas (OUT OF SCOPE)

- Conversion of `specs/examples/`, `.ggsad/templates/`, `.ggsad/schemas/state.schema.json` and the archived CHG-001 state to JSON — engine phases (hand-off list above).
- An in-place `core` to `full` switch with a state mapping — would need a new dated owner decision (D-07).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SPEC-01 to SPEC-18 | The 18 normative-drafting requirements of `.planning/REQUIREMENTS.md` | Part 1 gives one impact block per id; Part 4 gives plan order and dependencies |
</phase_requirements>

## Project Constraints (from CLAUDE.md and AGENTS.md)

- Follow `AGENTS.md` and the active GSD Core 1.10.0 workflow under `.planning/`; GSD is the sole development method; do not create or advance GG-SAD change state to govern this repository's development.
- The specification is the leading source for method semantics and may not be redefined by development artifacts. Changes to it need explicit repository-owner approval and independent review by a reviewer that is not the Requestor (Claude Code is the Requestor; Devin CLI is the reviewer; a fresh context or subagent of the Requestor is not independent). Phase 2 only drafts; it neither approves nor reviews.
- Legacy files under `specs/CHG-*`, prior GG-SAD evidence and historical roadmaps are not governance.
- Preserve unrelated changes; no destructive Git operations; no secrets; report checks not run. The `uv`/`ruff`/`ty`/`pytest` baseline applies to Python changes; Phase 2 changes no Python, so the baseline is not run and the plan must say so.
- Project memory: evidence notes are self-contained, with no links to transcripts or failed runs.

## Summary

Phase 2 edits one file, `docs/method/GG-SAD_normative_method_specification.md`. The working copy is byte-identical to the base: `git hash-object` returns `da29d6f3bdef2e88fdd85a762939017d7d7034fa`, equal to `git rev-parse origin/main:docs/method/GG-SAD_normative_method_specification.md`; 1422 lines, UTF-8, LF only, no BOM, one final LF, no tabs [VERIFIED: bash probe this session]. The file is the `full` model today (nine phases, eight statuses, DoR/DoD pairs, size classes, ten-rank hierarchy). The amendment must add a second model (`core`), eleven profile-neutral protections, a JSON state definition and versioning, and revise `full`, while keeping every existing section number stable (the decision record, requirements and roadmap cite sections 4.3, 5.3, 8, 22.2 by number).

The central planning facts: (1) the prototype source, not only MAPPING.md, carries the facts a drafter needs (statement format, canonical form, anchor semantics, baseline rule, scope measurement); this document digests them so drafters need not open the prototype. (2) Nothing in the specification today can hold the `core` model, so SPEC-12 is the largest single drafting task and every later requirement hangs on it. (3) Twenty places in the current text contradict a decision or need a judgment call (Part 2, T1 to T20, with 27 candidate Drafting choices); the biggest are the gate-fails-means-reject rule of 8.3 against `blocked`, the "explicitly accepted" escape hatch for open questions, the "MUST NOT silently weaken" wording, and the scope of "each `full` rule has an acceptance example". (4) D-08's plan order is workable but has forward references from Plan 2 to Plan 3 and from Plan 3 to Plan 4; Part 4 gives a numbering ledger and an intra-plan order that contain this. (5) Five items are unproven or only argued: SPEC-14, SPEC-16, SPEC-17, SPEC-18 and the "or an equivalent" clause of SPEC-05.

**Primary recommendation:** Keep sections 1 to 22 numbered as they are; add 5.6 (method profiles), 23 (the `core` profile), 24 (protections shared by both profiles, one home per protection) and 25 (state document, canonical form, schema versions); amend 5.3 in place for SPEC-16; reserve all new section numbers in Plan 1 so later plans can forward-reference them; and give every new rule inline `AE-nn` examples.

## Citation legend

Every tag below was opened with Read or a bash probe this session. Discrete values are quoted verbatim beside the claim.

- `S:Lnn` = specification at blob da29d6f, line nn. `S:§x` = section x.
- Prototype source (outside this repo; digest here, never cited in the spec): `E` engine.py, `A` evaluate.py, `K` store.py, `C` canon.py, `G` signing.py, `V` env.py, `M` model.py, `PF` profiles.py, all under `C:/Dev/Repos/ggsad-core-proto/src/gscore/`; `MAP §n`/`MAP P-nn`/`MAP A-nn` = MAPPING.md; `MP` = MILESTONE-PROPOSAL.md. P-nn and A-nn are source pointers for the planner only: the spec text must not contain them.
- `D-nn` = CONTEXT decision; `O-n` = owner decision record. `DC-nn` = candidate Drafting choice (register in Part 2). `OQ-n` = open question (Part 6).
- `[ASSUMED]` marks my own judgment where no source settles it; all of them are collected in the Assumptions Log.

## Architectural Responsibility Map (where each capability lives in the diff)

| Capability | Primary home | Secondary | Rationale |
|---|---|---|---|
| Method profile vocabulary, selection, immutability, move rule, applicability, status marker | new §5.6 (after §5.5, before L363 `## 6.`) | §1.1 map, §16.5 template | Sits beside §5.1 compliance profiles and §5.3 resolution, so the two axes (D-04) are co-located |
| `core` model: documents, states, outcomes, actions, transition table, wait kinds, base gates | new §23 (after L1422) | §21 caption | No existing section can hold a second model; appending avoids renumbering |
| Protections SPEC-01, 02, 04 to 11 (profile-neutral) | new §24.1 to §24.10, one home each | pointers in §3.3, 8.4, 8.5, 10.4, 10.7, 12, 15, 20 | §3.5 one fact one home; the §24 intro carries a "realization in each profile" table |
| Result `blocked`, rejected-vs-blocked per action | §22.2, §22.3 in place; per-action table in §23 (core) and a new unnumbered table after the §8.3 table (full) | §8.3 rejection cells | O-5 names §22.2 and the transition table |
| State document, canonical form, content hash, `schema_version`, migration | new §25 | §4.3 L266/L278, §8.1 L487-493, §11.2 L750-758 | SPEC-15 and SPEC-18 need one home; §4.3 only names the file |
| Resolution order (SPEC-16) | §5.3 in place (L322-333) | §3.8 L137, §4.2 L256, §5.2 L320, §23 | Section already exists; renumbering forbidden |
| `reopen` per profile (SPEC-17) | §8.3 row L514 and §8.4 L516-527 | §23 states its absence | Existing text is unconditional |
| Header, Revision | L3, L5 | — | D-12 |

## Standard Stack and Package Legitimacy Audit

No external packages are installed in this phase: the output is Markdown plus one bash check script using git, awk, grep, iconv, od, sha256sum (all present, see Environment Availability). Package Legitimacy Audit: none required. No ecosystem registry, Context7 or web lookup was used or needed; the task statement ruled out web research.

## Architecture Patterns

### Shape of the diff

```
origin/main blob da29d6f (full model only, 1.3)
  Plan 1  SPEC-12  -> §5.6 + §23 skeleton + §1.1 rows 23/24/25 + qualified terms (D-05)
  Plan 2  02,01,07,08,03 -> §24.2,.1,.6,.7 ; §22.2/22.3 ; per-action tables
  Plan 3  04,05,06,11,10,09 -> §24.3,.4,.5,.10,.9,.8 ; §15, §10.4, §9.5 edits
  Plan 4  15,18,17 -> §25 ; §4.3 ; §8.1/§11.2 JSON ; §8.3/§8.4 reopen per profile
  Plan 5  16,14 (+ header last) -> §5.3 ; full realizations + AE examples ; L3/L5
  result blob -> record base blob, result blob, SHA-256 (D-02) -> Phase 3 packet
```

### Pattern 1: one home, many pointers (§3.5)

Write each protection once in §24 in profile-neutral words ("the change definition", "the history"), with a table in the §24 intro mapping those words to `core` artifacts (change definition YAML, `state.json`, base commit) and to `full` artifacts (the change specification incl. Flow Gates, §16.1 L1033-1049; the state file or inline record, §4.3 L278). Existing sections get one-sentence pointers, not copies. This keeps SPEC-14 ("full carries the protections") a mapping task instead of eleven rewrites.

### Pattern 2: rule, then examples, then cross-reference

For each rule: the rule paragraph (section 2 terms), then `AE-nn` blocks in the style of the §16.1 template (L1019-1027): use a bold line `**AE-07 — <Title>**` rather than the template's `###` heading, so examples add no headings (the heading and map checks R1, R5, R6 stay simple; DC-10), `- Covers: <section>`, then `Given`/`When`/`Then` lines each ending in two spaces except the last (the L1025-1026 style). The rule cites its AE ids ("See AE-07, AE-08"). The 3.9 minimum is one normal and one failure or boundary example where risk warrants (L151).

### Anti-Patterns to Avoid

- Renumbering or retitling existing headings: breaks citations from the decision record (sections 4.3, 5.3, 8, 22), REQUIREMENTS (22.2, 5.3), and the 1.1 map.
- Copying a protection into each full section (duplicates, drift).
- Writing prototype names into normative text: `gscore`, `P-nn`, `A-nn`, `CHG-nn`, `change.yaml` as a prototype artifact reference, `spike`, `hotfix`, a commit hash, a local path, a URL.
- Leaving a placeholder in an intermediate commit unmarked: allowed on the branch, but the final blob must have none (check R3).

## Don't Hand-Roll

| Problem | Don't build | Use instead | Why |
|---|---|---|---|
| Cross-reference and heading checks | A Markdown parser | grep/awk over `^#{2,4} ` headings and `Sections? N` references | Baseline headings are regular: 22 top-level numbers 1..22 contiguous, 22 map rows L38-59, 46 fences, tables with consistent column counts (all probed on the base) |
| Diff identity | Commit ranges | `git hash-object` + `sha256sum` of the file (D-02) | A rebase merge rewrites commit ids |
| Check script structure | A new CLI style | Phase 1's `01-check-decision-record.sh` (options, `PASS ID msg` / `FAIL ID msg`, `RESULT:` line, exit 0/1/2, `--ref`, `--scope-base`, trap-removed temp dir) | Same reviewers, same conventions [VERIFIED: `.planning/phases/01-decision-record/01-check-decision-record.sh:1-20,118-120,358-363`] |

## Part 1. Per-requirement impact map

Format per block: **Obliges** (what the text must say) / **Facts** (state as facts in the spec; sources are pointers) / **Edit sites** (existing section + line at blob da29d6f, insertion point, proposed new heading) / **Ripples** (other things that must change with it) / **Needs first**. Line numbers refer to the base blob; they shift as earlier commits land, so cite headings when placing edits.

### SPEC-01 — Frozen gate definitions (Plan 2)

- **Obliges:** A change's gate definitions are fixed when the change is approved. Any later difference between the current definitions and the approved ones blocks every operation except cancellation until a human re-approves.
- **Facts:** The identity of the fixed set is a content hash of the parsed definition, so comments and formatting do not invalidate approval [M:119-121]. Every state-changing action first compares the hash with the approved one; on mismatch it writes nothing and answers `rejected` with the issue text "change.yaml differs from the approved version; a human must re-approve gates (amend)" [E:115-122]. `cancel` performs no such check [E:738-759]. Re-approval after an edit is recorded as `amend`, not `approve` [E:444-453]. The read-only `check` answers `rejected` with `changed: false` [E:800-803]. `guard` reports `not-enforced` rather than closing the change when gates differ [E:868-870]. Purpose: an agent could otherwise rewrite the gates that judge it (src MAP P-01, A-01; tested).
- **Edit sites:** new §24.1 "Frozen Gate Definitions"; one-sentence pointer at the end of §3.3 (after L99); §8.4 paragraph L520-523 (add that the frozen-gate block does not stop `cancel` or `supersede`); §16.1 "Flow Gates" L1033-1049 (state that these are the change's gate definitions in `full`); §23 core table.
- **Ripples:** §22 result: a blocked-by-frozen operation is `rejected` (precondition), see SPEC-03; SPEC-04 (who re-approves); SPEC-08 (an override lapses when gates are amended); SPEC-14 realization row.
- **Needs first:** SPEC-12 vocabulary. Forward references: SPEC-04 (human approval), §25.2 content hash (SPEC-15).
- **Traps:** the exempt set must contain the re-approval itself or the change deadlocks; "cancellation" must cover `supersede` (DC-03, D-07 depends on it). The prototype does not check `fail`, `adopt`, `ask`/`answer` while `open`, or `review` [E:721-735,762-780,609-645,818-852]; the requirement text ("every operation except cancellation") is stricter, so follow the requirement and record DC-03.

### SPEC-02 — Three-valued gate results (Plan 2)

- **Obliges:** Gate results are satisfied, not satisfied, could not be evaluated. A gate that cannot be evaluated is never a failure and never counts toward a retry limit. The text must also say what happens to the change in that case.
- **Facts:** Prototype result values `true`, `false`, `error`, `skipped` [A:65]. Environment problems are `error`, never `false`: the command cannot start (missing executable, timeout) [V:23-28,161-167]; the exit code is mapped to neither pass nor fail ("exit N is not mapped to pass or fail") [A:134]; the failing output says a module is missing ("No module named") [A:26-29,126-129]; git is unavailable; no base commit once the change has started [A:175-189]; any exception during evaluation [A:101-106]. Retry counting counts only results equal to "false": `n = sum(1 for e in self.h.entries if e["body"].get("gate_results", {}).get(gid) == "false")` [A:210-212]. Decision order when evaluating: a known hard fail wins; then an unevaluable gate puts the change in a wait of kind `external`; then a soft fail pauses for a human; then an active wait gate blocks; then an unmet done gate blocks; otherwise done [E:215-235]. `skipped` means commands were deliberately not run for this action [A:121-122]. Real case: antivirus TLS interception broke dependency sync, which a naive gate reports as a failed check (src MAP P-02, observed).
- **Edit sites:** new §24.2; §8.5 L529-541 (add the third value and the refinement "a known hard failure beats an unevaluable gate"; reconcile with `not_applicable` at L541, DC-04); §12.1 L785 ("exceeding hard budget, cost, or retry limits": add that unevaluable results do not count); §11.1 L735 (`WAIT_EXTERNAL_SYSTEM` is the full-profile category for an unevaluable gate, DC-09); §16.4 "Final Gate Evaluation" L1160-1165 (the Yes/No lines gain a "could not be evaluated" value); §19 L1321-1323 steps 3 to 5 (pointer only).
- **Ripples:** this block must define the check-command gate (a gate whose condition is a command with a pass/fail exit map): no other SPEC item owns it, and SPEC-07, SPEC-10, SPEC-11 all rely on it (DC-23 in the register). §22 `issues` content.
- **Needs first:** SPEC-12.
- **Traps:** `skipped` vs `not_applicable` vs "could not be evaluated" are three different things (DC-04).

### SPEC-03 — Result `blocked` (Plan 2, last in the plan)

- **Obliges:** Four results: `success`, `rejected`, `error`, `blocked`. `blocked` is a recorded evaluation that did not close the change, always `changed: true`; `rejected` means nothing was written and is never `changed`. The transition tables must say per action which of the two applies (O-5).
- **Facts:** `RESULTS = ("success", "rejected", "blocked", "error")`. The envelope constructor refuses `rejected` with `changed` true ("a rejected result never changes state; use 'blocked' if it was recorded") and `blocked` with `changed` false ("a blocked result is recorded in the history, so it changes state"); `issues` is present whenever the result is not `success` [E:35-74]. Only `close` and `resume` can answer `blocked`: when the gates say no after evaluation, the attempt is appended to history and the answer is `blocked` (a change may also move to `waiting` in the same write) [E:660-716]. `start` with unmet gates answers `rejected` even though its issue code is `start-blocked` [E:573-576]. A `close` whose hard fail triggers answers `success` with the change closed as `failed` [E:705-709]. The purpose: retries can be counted only if blocked attempts are recorded (src MAP A-03).
- **Edit sites:** §22.2 L1412 (result list; "never partial" kept), L1414 (`issues` also for `blocked`; the `state` field wording is per profile, see DC-24); §22.3 L1420 and L1422 (invalid operations stay `rejected` or `error` with `changed` false; a valid operation whose evaluation says no is `blocked`; history records blocked attempts); §8.3 rejection cells L507-514 and a new unnumbered table "Rejected and Blocked Results per Action" between the table (ends L514) and `### 8.4` (L516); the same table for `core` inside §23.
- **Ripples:** SPEC-17 (the `reopen` row), SPEC-08 and SPEC-09 (what blocks), SPEC-01 (rejected).
- **Needs first:** SPEC-12 (the core table exists), SPEC-02 (what "gates say no" means).
- **Traps:** DC-05 (the requirement says "did not close the change"; in `full` most actions never close, so the definition must be generalized); no SPEC item covers exit codes although WORK-01 says "approved result envelope and exit codes" and §22 is technology-neutral (OQ-7).

### SPEC-04 — Assurance levels and signed approval (Plan 3, first in the plan)

- **Obliges:** Assurance levels A0 to A2 and the signed-approval statement (operation, change, position in the change's history, signer, exact content approved) are normative; verifiers (SSH signature, platform review) are optional; an agent able to use a human's credentials can act as that human.
- **Facts:** Order A0 < A1 < A2 [M:14-15: `Assurance = Literal["A0", "A1", "A2"]`, `LEVELS: dict[str, int] = {"A0": 0, "A1": 1, "A2": 2}`]. A0: "No credential check exists, so every claim is worth exactly A0" [V:187-194]. A1: the mapped platform account's latest review on the change's pull request is an approval of the checked-out commit and the approved files have no uncommitted changes; anything else, including any failure to ask the platform, is A0 [V:222-276]; it cannot tell the human from an agent holding the human's login, and a platform does not let a pull request's author approve it, so it cannot serve a solo developer (MAP P-04). A2: a valid signature over exactly the engine-built statement by a key listed for that identity in a signers file kept outside the repository [V:279-318,349-354]. Verification fails closed: an unverified claim is A0 and the action is rejected when the level is below the required one [E:139-158]. The required level is the higher of the gate's minimum and the profile's minimum [E:152; A:159-161]. The statement: a format-identifying header line, then `operation`, `change`, `version` (the number of history entries, i.e. position in history), `identity`, then every detail field sorted by name with its value JSON-encoded so no value can inject a line; the engine builds the statement so what is signed cannot drift from what is verified [G:16-17,24-36]. A private key without a passphrase lets anything that can read it sign as the human; the signer refuses it unless told otherwise [G:39-65]. Human-only actions: approvals, sign-offs, overrides, answers by a human owner, `cancel`, `fail`, `adopt` (MAP row 5.4); a human identity is marked `human:` [V:170-177].
- **Edit sites:** new §24.3 "Assurance Levels and Signed Approval"; §5.4 L335-344 (add that "a human" is evidenced at a level, and that A0 is self-declared and does not by itself satisfy a decision that needs a verified human; the `lean` self-approval allowance L296, L344 stays); §3.10 L170 and §14.2 L869 (pointer only).
- **Ripples:** SPEC-01, 08, 09 name "human" actions; the statement needs the content-hash definition of §25 (DC-16); §16.4 L1146 evidence-record fields are unchanged.
- **Needs first:** SPEC-12. Forward from Plan 2 to this block (use the ledger).
- **Traps:** D-04 keeps §5.1 unchanged, so no assurance floor can be assigned per compliance profile (prototype: `lean` A0, `standard` A1 [PF:30-36]); see DC-11, OQ-1. The statement header and the signature namespace are implementation details: specify a format identifier and version, not the prototype's literals.

### SPEC-05 — History consistency and completeness (Plan 3)

- **Obliges:** Distinguish consistency (the recorded history is internally unbroken) from completeness (no records are missing, notably at the tail); require an external anchor, or an equivalent, to detect truncation where a profile demands high assurance.
- **Facts:** History is an append-only list; each entry has `n`, `prev`, `body`, `hash`; the entry hash is the SHA-256 of the canonical form of `{"prev": prev, "body": body}`; the first entry's `prev` is `"sha256:" + "0" * 64` [K:18,41-42,147-152]. Verification: `n` consecutive from 1, each `prev` equals the previous hash, each recomputed hash equals the stored one, at least one entry [K:110-123]. The current state is the last entry's `after` snapshot, so no mutable field exists to edit by hand [K:1-5,125-127]. A chain alone cannot see truncation: the prototype has a test named `test_KNOWN_LIMITATION_tail_truncation_is_not_detected` (MAP P-05). The anchor keeps the latest `(n, hash)` outside the working tree, written only after the append succeeded; a history shorter than the anchor means "truncated or rolled back", an entry `n` whose hash differs means "rewritten", history with no anchor is refused until a human explicitly adopts it, and an existing anchor cannot be replaced [K:45-88; E:762-780].
- **Edit sites:** new §24.4; §15 L922-924 (pointer); §25 holds the canonical form it depends on.
- **Ripples:** SPEC-04 (adopt is a human action at a level); SPEC-15 (canonical form).
- **Needs first:** SPEC-12; forward to SPEC-15 (Plan 4): reserve §25 in Plan 1.
- **Traps:** "a profile demands high assurance" has no definition: draft it as "the applicable configuration requires approvals at A2" without touching §5.1 (DC-11); the anchor is only as strong as its location (the spec must say an actor able to write both the history and the anchor can rewrite both); "or an equivalent" is evidenced by nothing in the prototype (LOW).

### SPEC-06 — Scope and isolation (Plan 3)

- **Obliges:** Define a change's scope, how it is measured (against the commit the change started from), that work outside it is a hard failure, and that a change runs isolated from unrelated uncommitted work.
- **Facts:** Scope is a list of path patterns the change may touch. The start action records the base commit and refuses to start if it cannot be recorded [E:564-570]. Paths changed since the base are the tracked differences against the base (committed, staged and unstaged) plus untracked files not ignored by git [V:75-78]; any such path matching no allowed pattern is a scope violation, a hard failure, reported as "outside scope: [...]" [A:175-189]. The change's own record files are exempt because tampering with them is caught by the frozen-gate hash, the approval hash and the chain [A:182-185]. Before the change has started there is no base: the result is not evaluated; after it has started with no base recorded: an error [A:177-180]. Git-ignored files are invisible to this measurement (MAP A-11). Unrelated uncommitted work counts as an out-of-scope edit, so a change runs in a clean separate checkout; a survey of 18 repositories found 15 with uncommitted work that would have hard-failed a change started in them (MAP P-06, A-07).
- **Edit sites:** new §24.5; §12.1 L784 ("action outside the approved scope": pointer); §10.6 L693 and §19 L1327 (pointers); §16.1 "Scope" L1003-1011 (in `full` scope is prose today: it needs a machine-checkable path list, DC-21); §6.1 L376.
- **Ripples:** SPEC-01 (scope is part of the frozen definition), SPEC-02 (unmeasurable scope is "could not be evaluated"), SPEC-11 (ignored files).
- **Needs first:** SPEC-12.
- **Traps:** the requirement says "commit"; word it as the revision the change started from so the text is not tied to one VCS (`[ASSUMED]`, DC-21); a hard failure here is the one case where the change closes as failed with no human action (SPEC-08).

### SPEC-07 — Known-failure baselines (Plan 2)

- **Obliges:** A verification gate may carry a recorded baseline of already-failing tests: the gate passes when every failure is on the baseline, fails and names any new failure, and is not evaluable when the failures cannot be read.
- **Facts:** The baseline is a list of failing test ids on the gate; it is valid only on a command gate [M:62-64,73-74]. Evaluation: pass exit code means satisfied; failing exit code with a baseline: take the failing ids from the command's output; none found: "exit N but no FAILED lines were found to compare" is an error, not a guess; any id not on the baseline: not satisfied, naming up to three new ids and a count ("N new failure(s): ..."); otherwise satisfied, noting baseline entries that did not fail ("N known failure(s), none new") [A:130-131,136-147]. A real repository had 33 failing tests before any change (MAP P-07, observed).
- **Edit sites:** new §24.6; §10.7 L699-708 (L706 "regression tests have succeeded": pointer); §15 (pointer in the evidence list L926-937).
- **Ripples:** the baseline is part of the gate definition and so frozen by SPEC-01 (editing it needs human re-approval, otherwise it would hide regressions); SPEC-02 (unreadable output is "could not be evaluated").
- **Needs first:** SPEC-02 (the check gate and tri-state), SPEC-01.
- **Traps:** the prototype identifies failures with one test runner's summary lines; write "a stable failure identifier that the gate declares how to extract" (technology-neutral, DC-23); entries on the baseline that now pass are not a failure.

### SPEC-08 — Hard and soft failure (Plan 2)

- **Obliges:** Hard failure: the change closes as failed without human action. Soft failure: the change pauses for a human disposition, either close as failed or a recorded override that grants a bounded number of further attempts and lapses when the gates are amended.
- **Facts:** Each fail condition carries severity `hard` or `soft`; a fail condition without severity is invalid [M:50-52,96-98]. A known hard fail closes the change as `failed` on the next evaluating action (`close`, `resume`, `guard`) [E:215-218,705-709,675-678,873-879]; `cancel` of a change whose hard fail is active ends as `failed`, not `cancelled` (already §8.4 L520-523). A soft fail puts the change in `waiting` with wait kind `fail-gate` [E:222-226,712-713]. Dispositions: the human `fail` action closes it as failed and is valid only while a soft fail awaits disposition [E:721-735]; an override approval for that gate, valid only for a soft fail condition, needs a reason and at least one attempt, binds to the exact frozen gate hash, and counts later `close` attempts, so it lapses when attempts are used up and dies on any gate amendment because the hash no longer matches [E:202-208,520-532]. The default grant is `DEFAULT_OVERRIDE_ATTEMPTS = 2` [E:199]; that is an implementation default, not a rule. That auto-failing a retry limit would be wrong is reasoning, not observation (MAP P-08).
- **Edit sites:** new §24.7; §12 intro L775 ("MUST terminate unsuccessfully": add the soft kind); §12.1 L785 (retry limits are the typical soft case, DC-19); §12.2 L789-797 and template L799-817 (a fail rule gains a severity); §8.3 `fail` row L511 and §8.4 (full: hard closes by `fail` without human action, soft needs a human); §11.1 L731 (`WAIT_DECISION` is the full-profile category for a soft-fail pause, DC-09); §20 L1352 (no soft failure awaiting disposition).
- **Ripples:** SPEC-01 (override lapse), SPEC-02 (unevaluable is not a fail), SPEC-04 (human disposition at a verified level).
- **Needs first:** SPEC-02, SPEC-01; forward to SPEC-04.
- **Traps:** do not copy the default "2" into the spec (DC-19); in `full` the "attempt" being counted has to be named (`complete` is the analogue of `close`, DC-05).

### SPEC-09 — Open questions as state (Plan 3)

- **Obliges:** Open questions are change state; structured answers (a choice among declared options) are supported; specification approval and closure are blocked while any question is unanswered.
- **Facts:** A question has an id (`Q1`, `Q2`, ...), text, owner (default: the change owner), asker, answer, answerer, options (none for a free-text question; otherwise at least two distinct options, else rejected "a structured question needs two or more distinct options"), and an optional note [E:238-247]. `ask` records a question without pausing, in `open` or `active` [E:609-628]; `wait` with a question creates one and pauses [E:583-606]. Only the question's owner may answer; a human owner's answer needs a verified human; a structured question accepts only one of its options; a free-text question needs text; an answered question cannot be answered again [E:257-280]. An unanswered question blocks spec approval (rejected, code `open-questions`: "answer ['Q1'] before approving the spec") [E:456-460] and, as a base wait condition, blocks `close` [PF:10; E:227-229]. Observed: trial specs carried an unresolved question as prose that nothing could see (MAP P-09).
- **Edit sites:** new §24.8; §9.4 L576-585 and §9.5 L587-595 (L594 "open questions have been answered or explicitly accepted"); §10.4 L663-674 (L672 "open questions are closed or explicitly accepted"); §16.1 "Open Questions" L1062-1064 (a view, not the authority, once state holds questions, DC-08); §20 L1352-1359 (add: no question unanswered); §11.3 L760-769 (pointer, the agent "formulate[s] one minimal, decidable question").
- **Ripples:** SPEC-04 (human owner answers), SPEC-03 (blocked at close, rejected at approval), SPEC-14.
- **Needs first:** SPEC-12; SPEC-02 for the blocking outcome.
- **Traps:** the "explicitly accepted" wording at L594 and L672 is an escape hatch the requirement removes; resolve by making acceptance an answer (DC-08).

### SPEC-10 — Executable evidence tied to a requirement (Plan 3)

- **Obliges:** Evidence is executable and tied to a requirement; a change with no requirements has no complete evidence.
- **Facts:** A requirement has text, examples and evidence commands [M:33-36]. Evidence is complete only if the change declares at least one requirement ("no requirements declared" is false), every requirement has at least one evidence command ("no evidence for [...]"), and, when the commands are run at closure, each passes; an evidence command that cannot be run makes the gate not evaluable [A:224-240]. This is a base done condition in the prototype's `lean` and `standard` profiles (not in its `spike` and `hotfix`) [PF:12,33,36,45,52]. Observed: the first trial's evidence list was decorative until a gate ran it (MAP P-10).
- **Edit sites:** new §24.9; §15 L922-968 (permitted evidence L926-937 includes non-executable items such as screenshots; template L939-966 shows `tests/...` paths, not commands; L968 "evidence MAY be documented directly in `spec.md`"); §16.4 L1128-1131 (the "Evidence" column); §10.7 L699-708 (L707 "evidence is complete"); §20 L1355; §3.4 L101-103 (pointer); §16.1 L1013-1017 and L1051-1053.
- **Ripples:** SPEC-02, SPEC-07, SPEC-11 (the commands run through the declared interpreter).
- **Needs first:** SPEC-02, SPEC-07. Draft after SPEC-11.
- **Traps:** the existing permitted-evidence list conflicts with "evidence is executable": resolve as DC-18 (a requirement's evidence is complete only with an executable check bound to it; other records supplement).

### SPEC-11 — Explicit, opt-in interpreter (Plan 3)

- **Obliges:** The interpreter that runs gate commands is explicit and opt-in; state the trust consequence: code in git-ignored locations is invisible to the scope check.
- **Facts:** Gate commands run as an argument list with no shell, so no injection and no `&&` [V:142-167]. A designated token as the first element stands for the project's configured interpreter only if the configuration sets one; it is never discovered, because a virtual environment is git-ignored and what sits behind the token decides whether every gate passes; absent configuration it means the interpreter running the engine [V:111-124,139,155-156]. `check` warns when the interpreter lives inside the repository [E:790-793; V:387-391]. Tested (MAP P-12, A-11).
- **Edit sites:** new §24.10; pointers at §12 (L784 area) and §15 (L926-937). The prototype's executable allowlist is not a SPEC item: do not add it.
- **Ripples:** SPEC-06 (ignored files), SPEC-10.
- **Needs first:** SPEC-02 (the check gate), SPEC-06.

### SPEC-12 — Method profiles `core` and `full` (Plan 1)

- **Obliges:** Specify both profiles (O-1), state which requirements apply to which and how a change moves between them; fixed at creation, moved by a new change plus `supersede` (D-07); qualified terms (D-05); specified-but-not-implemented marking for `full` (O-8).
- **Facts for the `core` model (all copied as facts):** four states `open`, `active`, `waiting`, `closed` and three outcomes `done`, `failed`, `cancelled`; an outcome exists only when `closed` (MAP §1 row 8.1-8.2). New change state: `open` with `outcome` null, no approvals, no questions, no wait, no base commit [K:29-38]. Actions: `new`, `approve` (targets: spec, gates, all, override, a human gate), `start`, `wait`, `ask`, `answer`, `resume`, `close`, `fail`, `cancel`, `adopt`; read-only `check`, `review`, `guard` (MAP row 8.3). `start` needs state `open`, frozen gates, spec approved if the profile requires it, a base commit, and no active wait or fail condition [E:557-580]; it moves to `active`. `wait` needs `active` and a reason and owner [E:583-606]. `resume` needs `waiting` [E:648-687]. `close` needs `active` and every done gate satisfied with no active fail or wait [E:690-718]. `cancel` is available to a human on any non-closed change; waits do not block it; an active hard fail turns it into `failed` [E:738-759]. A change may follow only an ended change (`follows`) [E:377-383]. `supersede` is `cancel` with `replaced_by` (MAP row 8.3). Evaluation order: fail, then wait, then done, with the refinements of SPEC-02 and SPEC-08 (MAP row 8.5). Wait record: kind (`question`, `manual`, `fail-gate`, `external`), reason, owner, resume condition, optional expiry, optional question id; no `safe_state` and no `next_action` (MAP row 11; E:287-289, 599-602). Gates per change are three lists `fail`, `wait`, `done`; "Ready" is folded into the `start` preconditions (MAP row 3.3). Fail and wait gates are predicates; fail gates carry severity; done gates are checks, reviews or human sign-offs; exactly one kind per gate; ids unique [M:50-102]. Change definition (human-owned YAML, frozen): id, follows, compliance profile, author, owner, goal (problem, done_when, non_goals), scope.allow, requirements, gates [M:108-121]. Engine-owned `state.json` (SPEC-15). No size classes, phases, DoR/DoD pairs or document hierarchy (MAP §1 rows 4, 6, 7, 9, 10).
- **Edit sites:** new §5.6 "Method Profiles" (after the last paragraph of §5.5, L361): vocabulary, selection per change recorded at creation with an optional project default, immutability, the move rule, the applicability table, the status marker. New §23 "The `core` Profile" (after L1422): documents, states and outcomes, actions and transition table (no `reopen`, SPEC-17), result-per-action table (SPEC-03), wait kinds, base gate set (DC-12), layers implemented (SPEC-16). §1.1 map L36-59: append rows 23, 24, 25 (categories: Method Semantics for 23 and 24, Reference-Implementation Requirements for 25, DC-01). Qualify bare "profile": L124, L292, L294, L301 (three times), L305, L320, L865 (inventory in Part 3). §16.5 L1210-1216 (add a method profile line, DC-26). §4.1/§4.2 and §6 to §10: a one-line "`full` profile" marker each. §21 L1363-1395: caption that the diagram is the `full` flow (DC-22).
- **Ripples:** every later block depends on this vocabulary; SPEC-14 completes the marker and the applicability table.
- **Needs first:** nothing. It is first.
- **Traps:** the applicability table must say something for every existing section; the default rule "applies to both unless marked `full` only" is the conservative reading (DC-27), with the `full`-only list: §4.1 and the document hierarchy, §5.5, §6, §7, §8.1 to §8.5 as written, §9, §10, §11.1 category list, §16.1 to §16.4 file layout and templates. Everything else applies to both. `[ASSUMED]` list; owner can overrule at Phase 3.

### SPEC-13 — No change under `src/ggsad/` (check in every plan)

- **Obliges:** Nothing in `src/ggsad/` changes. This is a check, not a drafting block (D-08).
- **Facts:** The engine pins method version `"1.3"` at `src/ggsad/application/initialize_project.py:82`, the test at `tests/unit/test_initialize_project.py:61`, and `.ggsad/config.yaml:10`: Version 1.4 (D-12) will mismatch these; none may be touched now (SPEC-13, D-11). Add all three to the hand-off list [VERIFIED: grep this session].
- **Check:** script check S1/S2 (Part 5).

### SPEC-14 — Revise `full` (Plan 5)

- **Obliges:** `full` carries the protections of SPEC-01 to SPEC-11 as invariants (O-9); is marked specified-but-not-implemented (O-8); each `full` rule has an acceptance example (D-13).
- **Facts:** The prototype never ran phases, DoR/DoD, size classes, ADRs or releases (MAP §5); every `full` realization is therefore argued, not tested (LOW). The proposal's mitigation for an unbuilt `full`: keep it small, mark it clearly, give each rule an acceptance example (O-8 consequences; MP risks).
- **Edit sites:** the §24 intro realization table (a "Realization in `full`" column per protection); §8.3 rows L507-514 and the new per-action table (SPEC-03); §8.5; §9.4 to §9.6; §10.4, §10.7; §12; §15; §20; §16.1 L1033-1049; AE examples under each full rule: §5.5, §7.1, §8.2, §8.3 (one per action), §8.4, §8.5, each DoR/DoD pair of §9 and §10.
- **Needs first:** all of SPEC-01 to SPEC-11, SPEC-15, SPEC-16, SPEC-17.
- **Traps:** (a) scope of "each `full` rule" (OQ-3): per bullet is 200+ examples, per rule unit is roughly 40; recommend per unit (one transition-table action, one numbered rule subsection, one DoR/DoD pair) and ask the owner; (b) full realization of frozen gates (DC-06), scope (DC-21) and state (DC-07) are judgment calls the prototype cannot support; (c) the marker wording (DC-22): "specified but not implemented" must not imply the text is untested-normative-free; it states the reference implementation refuses `full` (ENG-06).

### SPEC-15 — `state.json` and canonical form (Plan 4)

- **Obliges:** State is a JSON document (`state.json`) with a defined canonical form for hashing; examples and templates inside the specification are updated (D-11).
- **Facts:** Canonical form: object keys sorted, separators `,` and `:` with no whitespace, non-ASCII not escaped, UTF-8 bytes; hash string is `sha256:` plus the lowercase hex digest [C:13-18]: `json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`. File shape `{"entries": [ {n, prev, body, hash}, ... ]}` written pretty-printed (the file is not the hashed form), replaced atomically through a temporary file, guarded by a lock and by an expected-version check (compare-and-swap) so concurrent writers fail instead of interleaving [K:129-160]. Entry `body` fields: `verb`, `actor`, `assurance`, `at`, `result`, `gate_results`, `gate_detail`, `files`, `note`, `after` [E:179-186]; `after` fields: `state`, `outcome`, `approvals`, `questions`, `wait`, `base_commit`, `replaced_by` [K:29-38]. Human-owned definitions stay YAML (O-4).
- **Edit sites:** §4.3 tree L266 (`state.yaml` becomes `state.json`) and L278 (the sentence); §8.1 YAML block L487-493 and §11.2 template L750-758 (convert to JSON blocks, keep the key spellings as they are; the two blocks already disagree: `owner` at L491 vs `waiting_for` at L753); new §25.1 "State Document and Canonical Form" and §25.2 "Content Hash"; §4.3 also needs the `core` layout (change definition, `spec.md`, `state.json`, reviews) beside the `full` layout (DC-07); `.ggsad/config.yaml` mention at L290 stays YAML.
- **Ripples:** SPEC-05 (chain), SPEC-04 (exact content hash), SPEC-18 (`schema_version`), the decision record says the rename touches "sections 4.3, 8 and 22" but the literal `state.yaml` occurs only at L266 and L278 (Part 3 inventory).
- **Needs first:** SPEC-12. Forward-referenced from Plan 2 and 3.
- **Traps:** DC-14 (floats, ordering rule, string-escape rules: restrict values to strings, integers, booleans, null, arrays and objects; state the key ordering as code point order); DC-16 (file content hash for text vs binary has no SPEC owner, INTEG-02 needs one; OQ-7).

### SPEC-16 — Six-layer profile resolution (Plan 5, unproven)

- **Obliges:** Resolution follows the six-layer order of §5.3; a lower layer must not weaken a higher one; `core` implements four of six.
- **Facts:** The only prototype evidence is a no-weakening check of a change's gates against the profile's base gates: a base gate missing, a base predicate gate "altered" (kind, predicate or severity differs), or a base human gate with a lower required assurance than the base [PF:57-74]. It is applied at creation and again before gates are approved, answering `rejected` with issue `profile-violation` [E:295-306,409-411,444-447]. Nothing else about resolution exists (MAP §1 row 5.3: "NOT BUILT"; O-2: "no evidence for profile resolution").
- **Edit sites:** §5.3 L322-333 in place: L327 "selected compliance profile" becomes "selected method profile and compliance profile, resolved together" (D-06); L333 "A lower layer MUST NOT silently weaken a higher layer" (DC-13); add the `core` layer set (1, 2, 3, 5) and that layers 4 and 6 are not applicable to `core` and are specified for `full` and combination use (O-10); add what weakening means (remove a gate, alter its condition, lower its severity, lower a required assurance level) and AE examples; §3.8 L137; §4.2 L254-256; §5.2 L320.
- **Needs first:** SPEC-12, SPEC-01, SPEC-04, SPEC-08 (severity).
- **Traps:** the "profile's base gates" does not exist in §5.1 (D-04 keeps it unchanged): define the base gate set per method profile (DC-12). The §5.3 rule "silently" vs §4.2 "without an approved exception" (OQ-2). Examples are mandatory: normal (project configuration tightens, change adds a gate), failure (change deletes a base gate), boundary (hard to soft; assurance A1 to A0; same gate id with changed condition), order (a lower layer cannot loosen a higher one even if listed later).

### SPEC-17 — `reopen` for `full` only (Plan 4)

- **Obliges:** `reopen` is specified for `full` and absent from `core`; the transition table states this per profile (O-6).
- **Facts:** `core` has no `reopen`; a closed change is followed by a new change that names it (`follows`), and a follow-up can only follow a change that has ended [E:377-383; MAP §1 row 8.3].
- **Edit sites:** §8.3 row L514 (mark "`full` only" in the first column or the legal-from cell); §8.4 heading L516 (keep) and paragraph L525; L527 "no further phase advancement is legal except through `reopen`" (qualify: in `full`; in `core` a closed change is final); §23 states absence and the `follows` rule; the new per-action table (SPEC-03) has no `reopen` row for `core`.
- **Needs first:** SPEC-12 (the `core` table exists), SPEC-03.
- **Traps:** proved only by absence. A sentence is needed that `follows` is a reference, not a state transition, so no `core` change ever leaves `closed`.

### SPEC-18 — `schema_version` and migration (Plan 4, unproven)

- **Obliges:** Every artifact carries `schema_version`; an unknown version is refused; migration is an explicit, recorded command, never silent.
- **Facts:** Today the three schemas pin a constant: `.ggsad/schemas/config.schema.json:20`, `mappings.schema.json:19`, `state.schema.json:22` each read `"const": "0.1"`; `.ggsad/config.yaml:1` is `schema_version: "0.1"`; there is no migration path (O-7). The prototype's `state.json` has no `schema_version` field [K:147-154]: nothing in it proves SPEC-18 (decision-driven, O-7). Migrating the prototype's recorded results from `rejected` to `blocked` and renaming `state.yaml` to `state.json` are both migrations (O-7, O-4 consequences).
- **Edit sites:** new §25.3 "Schema Versions and Migration"; §22.1 L1401-1406 (add `migrate` as a contract operation, DC-25); §22.2 (refusal of an unknown version is `rejected`, nothing written).
- **Needs first:** SPEC-15 (where `state.json` carries the version), SPEC-03.
- **Traps:** "every artifact" needs a boundary: machine-readable files that have a schema (config, mappings, state, change definition); Markdown documents are out (DC-15). The history is append-only and hash-chained, so migration appends a record naming source version, target version and the source content hash, and never rewrites entries in place (DC-15). Where `schema_version` sits relative to the hashed content is a design choice: if it is outside the chain, a downgrade is not tamper-evident.

## Part 2. Conflicts, traps and the Drafting-choice register

### Conflicts between current text and decisions or evidence

| # | Where (base blob) | Conflict | Smallest consistent resolution (candidate) |
|---|---|---|---|
| T1 | §7 L406-416, §8.1 L474-483 vs O-1 | Nine phases and eight statuses vs four states and three outcomes | Keep §7 to §10 as `full` (marked); add §23 for `core`; field names in `core` are `state` and `outcome`, in `full` `phase` and `status` (L495 "`closed` ... never a status value" applies to `full` only). DC-01, DC-24 |
| T2 | §22.2 L1414 | "The `state` field contains the resulting phase and status" collides with `core`'s own `state` and `outcome` | Word per profile: `full`: phase and status; `core`: state and outcome. DC-24 |
| T3 | §5.3 L324-333 vs O-10 | Six layers vs four implemented; layer 4 (change-class) needs size classes that `core` lacks | Keep six; `core` resolves 1, 2, 3, 5; 4 and 6 are "not applicable to `core`", never renumbered (D-06). DC-12 |
| T4 | §5.3 L333 vs SPEC-16; §4.2 L256; §3.8 L137 | "MUST NOT silently weaken" (explicit weakening arguably allowed); §4.2 allows weakening "without an approved exception"; SPEC-16 says a lower layer must not weaken | Draft the rule as absolute (drop "silently") and reconcile §4.2 by limiting its exception to `full` local specifications vs project-wide definitions, outside the layer rule. DC-13, OQ-2 |
| T5 | §8.3 L507-514 rejection cells vs O-5 | An unsatisfied gate today means "Reject without any partial mutation"; `blocked` means a recorded evaluation | Precondition failures stay `rejected`; for completion-type actions a gate evaluation that says no is `blocked` and recorded. Core: `close`, `resume`; `full`: `complete`, `resume`. Others `rejected`. DC-05 |
| T6 | §22.3 L1420 | "invalid operation ... `changed` MUST be `false`" and "`rejected` or `error`" | State that a valid operation whose gates say no is not invalid: `blocked`, `changed` true. Add to §22.3 |
| T7 | §8.3 L514, §8.4 L525, L527 | `reopen` is unconditional; L527 "no further phase advancement is legal except through `reopen`" | Qualify by profile (SPEC-17) |
| T8 | §4.3 L266, L278 and O-4 consequences | The record says the rename touches "sections 4.3, 8 and 22"; the literal `state.yaml` occurs only at L266 and L278; §8 has only an unnamed YAML block (L487-493) and §22 none | Rename L266, L278; convert L487-493 and L750-758 to JSON; add one sentence in §22 only if needed for `state` field wording |
| T9 | §9.5 L594, §10.4 L672, §16.1 L1062-1064 vs SPEC-09 | "answered or explicitly accepted" is an exemption the requirement forbids | Acceptance becomes a recorded answer (for example a structured option "accepted"); the §16.1 section is a view. DC-08 |
| T10 | §12 L775, L785 vs SPEC-08, SPEC-02 | "MUST terminate" and "retry limits" vs a soft pause and unevaluable results not counted | Split DoF into hard (terminates) and soft (pauses for a human); retry limits are soft; unevaluable results never count |
| T11 | §15 L926-937, L968, §20 L1355 vs SPEC-10 | Non-executable evidence is permitted | Complete evidence for a requirement needs an executable check bound to it; other records supplement. DC-18 |
| T12 | §11.1 L728-735, §11.2 L739-746 vs `core` waits | `WAIT_*` categories and mandatory `safe state` and `next action` vs kinds `question`, `manual`, `fail-gate`, `external` with no safe state or next action | `core` defines its own wait record; safe state and next action are `full` only; table maps kinds to categories (`external` to `WAIT_EXTERNAL_SYSTEM`, `fail-gate` to `WAIT_DECISION`, `question` to `WAIT_USER_INPUT`, `manual` to `WAIT_PROCESS`). DC-09 `[ASSUMED]` mapping |
| T13 | §3.9 L144 vs D-13 | MUST give every behavioral requirement an example; D-13 speaks only of `full` rules | Give every new rule (both profiles) AE examples. DC-10 |
| T14 | §8.5 L541 vs SPEC-02 | `not_applicable` is a recorded gate value; tri-state adds none | Tri-state is the outcome of evaluating; `not_applicable` stays the marker for a gate intentionally not evaluated (the prototype's `skipped`). DC-04 |
| T15 | §12.2 L816 `FAILED_POLICY_VIOLATION` vs one `failed` outcome in `core` (MAP §4 item 3) | Final-status codes in the fail-rule template | Codes are `full` only; `core` records the reason text with outcome `failed` |
| T16 | §4.3 L278 vs the protections | State file mandatory only if the project persists state; Class S may live inline in an issue (§6.1 L369-371) | `core`: `state.json` always. `full`: keep the allowance and state that mechanical enforcement of SPEC-01, 04, 05, 09 needs `state.json`. DC-07, OQ-4 |
| T17 | D-07 vs `core` outcomes | D-07 says supersede with "the existing `supersede` action", but `core` has three outcomes without `superseded` | `core` keeps `supersede` as an action that closes with outcome `cancelled` and a required `replaced_by`. DC-02, OQ-6 |
| T18 | §5.1 L294-299 vs SPEC-16 base gates | No base gates per compliance profile exist, and D-04 keeps §5.1 unchanged | Base gates are defined per method profile in §23; compliance strengthening arrives via project configuration (layer 3). DC-12, OQ-1 |
| T19 | WORK-01 vs §22 | "approved result envelope and exit codes": no SPEC item or text defines exit codes | Note as an unowned gap; either add a short exit-code statement in the SPEC-03 commit or hand it to Phase 7 explicitly. OQ-7 |
| T20 | INTEG-02 vs SPEC set | Text vs binary content hashing has no SPEC item | Define "content hash" in §25.2 with the SPEC-15 commit (DC-16) |

### Drafting-choice register (candidates for the Phase 3 packet, D-10)

| ID | Choice (most conservative reading) | Block |
|---|---|---|
| DC-01 | Do not renumber; add §5.6, §23, §24, §25; append §1.1 rows 23 (Method Semantics), 24 (Method Semantics), 25 (Reference-Implementation Requirements) | all |
| DC-02 | `core` `supersede` closes as `cancelled` with required `replaced_by` | SPEC-12, 17 |
| DC-03 | "Cancellation" in SPEC-01 includes `supersede`; the re-approval itself is exempt; read-only reports answer `rejected` with `changed` false | SPEC-01 |
| DC-04 | `skipped` is recorded as `not_applicable`; "could not be evaluated" is a separate outcome | SPEC-02 |
| DC-05 | `blocked` generalized: an evaluation was recorded and the requested transition did not occur; completion-type actions only | SPEC-03 |
| DC-06 | `full` frozen set: the change specification including Flow Gates, plus the project-wide definitions in effect recorded by content hash at approval | SPEC-14 |
| DC-07 | `core`: `state.json` mandatory; `full` keeps the optional-state allowance of §4.3 | SPEC-15, 14 |
| DC-08 | Open-question acceptance is an answer; §16.1 Open Questions is a view | SPEC-09 |
| DC-09 | `core` wait record is its own; kind-to-category mapping table; safe state and next action `full` only | SPEC-12 |
| DC-10 | AE examples for every new rule in both profiles; unit = one rule paragraph, one transition-table action, one DoR/DoD pair; ids unique and cited, not necessarily in document order | SPEC-14 |
| DC-11 | No assurance floor per compliance profile; "high assurance" = configuration requires approvals at A2 | SPEC-04, 05 |
| DC-12 | Base gate set per method profile (`core`: scope hard failure, open questions wait, spec approval stale wait, evidence complete done) | SPEC-16 |
| DC-13 | Weakening is absolute; "silently" dropped; §4.2 exception limited to `full` | SPEC-16 |
| DC-14 | Canonical form restricted to string, integer, boolean, null, array, object; key order by code point; UTF-8; no ASCII escaping; `sha256:` prefix | SPEC-15 |
| DC-15 | "Artifact" = machine-readable schema-governed file; migration appends a record, never rewrites | SPEC-18 |
| DC-16 | Content hash defined in §25.2: text normalizes line endings, binary is byte-exact; classification rule left to the implementation unless the owner rules (OQ-7) | SPEC-15 |
| DC-17 | The spec text cites no O-n, P-nn, SPEC-nn, A-nn ids; the Revision line names no requirement ids | all |
| DC-18 | Executable check bound to each behavioral requirement; other records supplement | SPEC-10 |
| DC-19 | Override grants a recorded number of attempts N >= 1; no default value in the spec | SPEC-08 |
| DC-20 | Header Version and Revision edited in the last commit of Plan 5 | D-12 |
| DC-21 | `full` scope gets a machine-checkable path list; scope measured against "the revision the change started from" | SPEC-06, 14 |
| DC-22 | Marker sentence at the head of §4.1, §6, §7, §8, §9, §10 and in §5.6 and §21 caption | SPEC-12, 14 |
| DC-23 | The check-command gate (exit map, unmapped exit is "could not be evaluated", failure ids extracted as the gate declares) is defined in §24.2 | SPEC-02, 07 |
| DC-24 | `core`: `state` and `outcome`; `full`: `phase` and `status`; §22.2 `state` field worded per profile | SPEC-03, 12 |
| DC-25 | §22.1 gains "record a human decision" and "migrate" operations | SPEC-03, 18 |
| DC-26 | Method profile chosen per change at creation; project configuration may name a default; §16.5 project brief gains one line | SPEC-12 |
| DC-27 | Default applicability: both profiles unless marked `full` only | SPEC-12 |

## Part 3. Spec conventions the drafter must follow

**Normative terms (§2, L63-69):** only `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`, in bold at definition and plain capitals in rules. The base also uses uppercase `OPTIONAL` (L166) and capitalised `Recommended` (L908, L910); do not add `SHALL`, `REQUIRED`, `RECOMMENDED`. Lowercase modals occur three times in the base (L547 "may begin", L869 "may be a human", L1414 "may appear"): descriptive only.

**Headings:** `## N. Title` for sections, `### N.M Title` for subsections; four levels are used unnumbered (`#### Patch Flow` L440, `#### constitution.md` L208). Section cross-references are written "Section 8.3", "Sections 9 and 10" (L32, 274, 320, 337-342, 359, 495, 643, 920, 1350, 1406, 1414, 1422); no Markdown anchors or links exist (verified: no `](#`, no `](http`). Template subsection titles use backticks (`### 16.1 \`spec.md\``). Existing rule ids: `F-01` (inside a template fence, L802) and `R1`/`E1` (inside the §16.1 template). The base has no inline rule ids of its own: new ids (`AE-nn`) are an addition.

**Tables:** pipe tables with a `|---|---|` separator row and Title Case headers (L36-59, L294-299, L505-514, L946-949, L1146-1153); all tables in the base have constant column counts (verified by awk). Long cells are tolerated (L507-514 exceed 800 characters).

**Examples:** the template style is L1019-1027: `### E1 — <Title>` (a heading), `- Covers: R1`, then three lines `Given ...  ` / `When ...  ` / `Then ...` with two trailing spaces on the first two. Two trailing spaces are the only trailing whitespace in the base (L4, L804, L815, L1025, L1026): do not strip them and do not add other trailing whitespace.

**Header (L1-6):** `# GG-SAD — Normative Method Specification` / `**Version:** 1.3` / `**Status:** Normative Baseline  ` (two trailing spaces) / `**Revision:** 2026-08-21 — <one sentence>.` / `**Target audience:** ...`. New values (D-12): Version 1.4; Revision `YYYY-MM-DD — <one sentence naming the amendment>.` (ISO date, spaced em dash, sentence ending in a period); keep Status unchanged unless the owner rules otherwise.

**§1.1 map (L36-59):** a bijection today: 22 numbered `##` headings (1 to 22, contiguous) and 22 rows `| N. Title | Category |`. Adding §23 to §25 requires three rows and the title text must match the heading. Category vocabulary: `Authority & Applicability`, `Method Semantics`, `Project Governance`, `Reference-Implementation Requirements`, `Optional Integration Guidance`.

**§21 Quick Reference (L1363-1395):** a text diagram of the `full` flow and the precedence chain. It lists no profile and no protection; it needs a one-line caption naming the `full` profile (DC-22) and nothing else. §20 (L1348-1359) lists closure conditions and should gain the new conditions (no unanswered question, no soft failure awaiting disposition, executable evidence complete).

**Character set:** UTF-8 with non-ASCII punctuation (em dash, arrows, box-drawing); LF only; one final LF; no BOM; no tabs [VERIFIED: probes]. The base has no hash-like token, URL, drive path, `O-n`, `P-n`, `SPEC-nn`, `gscore` or `MAPPING` string; the word "prototypes" occurs once (L296).

### Occurrence inventory at blob da29d6f

- `state.yaml`: L266 (the §4.3 tree), L278 (the optional-state sentence). `.ggsad/config.yaml` L290 stays. YAML fences: L487 (status metadata) and L750 (wait template); no other `yaml` fence.
- `reopen`: L514 (table row), L516 (heading "Reopening"), L525, L527.
- `lean`: L296 (profile row), L337, L344, L865 ("Lean and low-risk Class S flows"), L1212 (the value list). Never a synonym for `core`.
- Bare "profile" that D-05 must qualify: L124 "selected profile", L292 "default profiles", L294 table header "Profile", L301 "additional profiles ... Custom profiles ... default profile", L305 "A profile MAY tailor", L320 "A lower-compliance profile", L322 heading "5.3 Profile Resolution" (keep the heading, qualify in the body), L865 "Governed or regulated profiles". Already qualified: L113, L137, L166, L231, L288, L290, L327, L337, L858, L1210, L1312, L1319. A third sense exists at L315: "enabled practice profiles" (undefined elsewhere): leave and do not touch.
- `profile` in the existing implementation's state example: `specs/examples/class-m/state.yaml:10` `profile: standard` under `flow:` means the compliance profile (hand-off item; do not change now).

## Part 4. Plan decomposition check against D-08

| Plan | Requirements | Verdict | Notes |
|---|---|---|---|
| 1 | SPEC-12 | OK, but it is the largest single task | Must create §5.6, the §23 `core` model and table, §1.1 rows 23 to 25, term qualification, and reserve §24 and §25 so later plans can forward-reference. The applicability table (SPEC-12) names protections that do not exist yet |
| 2 | SPEC-01, 02, 03, 07, 08 | OK with an internal order | Order: 02, 01, 07, 08, 03. SPEC-02 defines the check gate; 01 needs the content hash (§25, later); 08 needs "human" (SPEC-04, Plan 3); 03 last because it depends on what blocks |
| 3 | SPEC-04, 05, 06, 09, 10, 11 | OK with an internal order | Order: 04, 05, 06, 11, 10, 09. SPEC-04 defines "human" that Plan 2 already cites; SPEC-05 needs §25 (Plan 4); 10 needs 11 |
| 4 | SPEC-15, 17, 18 | OK | Order 15, 18, 17. SPEC-17 edits the tables created in Plan 1 and the per-action table of Plan 2 |
| 5 | SPEC-14, 16 | OK, with 16 before 14 | SPEC-14 must be last (it depends on all); the header commit (DC-20) is the final spec commit |

**Forward references:** Plan 2 cites assurance levels and content hash; Plan 3 cites the canonical form. Resolve with a numbering ledger written in Plan 1 (section number to requirement, kept in the plan, not in the spec). Intermediate commits may hold forward references and, if needed, placeholder headings; the check script validates reference resolution and placeholders only at phase end (`--final`), never per commit.

**One commit per requirement (D-03):** SPEC-12 is the one block whose completion depends on later text (the applicability table). Either finish the table in Plan 1 with references to reserved numbers (preferred), or add a second SPEC-12 commit in Plan 5; both satisfy D-03 if the subject names SPEC-12.

**File overlap:** all five plans edit the one file; plans run in sequence (D-08), no conflict. Plan 2 and 4 both touch §8.3 and §22; the order above prevents rework. Rebase risk: if origin/main gains a spec edit before Phase 3, the base blob changes and D-02 values must be re-recorded (check B1).

**Not draftable from CONTEXT.md alone:** every block needs the prototype facts above. This document is the digest; plans should cite its fact lines so a drafter need not open the prototype repository. Needing prototype source beyond MAPPING: SPEC-04 (statement fields), SPEC-05 (anchor semantics), SPEC-06 (scope measurement), SPEC-07 (baseline rule), SPEC-11, SPEC-12 (core model), SPEC-15 (canonical form).

**Unproven or only argued (call out in each plan's Drafting choices list):** SPEC-14 (all realizations), SPEC-16 (beyond a no-weakening check), SPEC-17 (absence only), SPEC-18 (decision-driven, no prototype evidence), SPEC-05 "or an equivalent", SPEC-04 A1 (platform review: "not tested directly", MAP P-04), SPEC-08's rule that a retry limit is soft (reasoning, MAP P-08).

**SPEC-13:** a check in each plan (script S1, S2 with `--scope-base origin/main`), not a commit; the script treats SPEC-13 as satisfied by those checks (see C1).

**Hand-off list additions (record in the Phase 2 summary, D-11):** `.ggsad/config.yaml:10`, `src/ggsad/application/initialize_project.py:82` and `tests/unit/test_initialize_project.py:61` pin method version "1.3"; schema constants `"0.1"` at `.ggsad/schemas/config.schema.json:20`, `mappings.schema.json:19`, `state.schema.json:22`; `flow.profile` in `specs/examples/class-m/state.yaml:10`. These add to the D-11 list (`specs/examples/class-m/state.yaml`, `.ggsad/templates/`, `state.schema.json`, archived CHG-001 state).

## Common Pitfalls

### Pitfall 1: Deadlock in the frozen-gate rule
**What goes wrong:** "Every operation except cancellation is blocked" also blocks the re-approval that is supposed to unblock it. **Avoid:** name the re-approval as exempt (DC-03). **Warning sign:** an AE example with no step that lets a human re-approve.

### Pitfall 2: Prototype vocabulary leaks into the text
**What goes wrong:** `change.yaml`-as-prototype, `gscore`, `P-nn`, `spike`, `hotfix`, `CHG-nn` ids, a hash or a path appear in normative prose. **Avoid:** check X1 on the whole file (the base is clean). **Warning sign:** any added line matching those tokens.

### Pitfall 3: A rule without an example
**What goes wrong:** §3.9 L144 makes an example mandatory; a rule lands without one. **Avoid:** check R2 (every rule paragraph in §23 to §25 cites an AE; every AE is cited and has Given/When/Then).

### Pitfall 4: Dangling or broken references after appending sections
**What goes wrong:** "Section 24.7" cited but absent; §1.1 map misses a new row. **Avoid:** checks R1 and the map bijection; reserve numbers in Plan 1.

### Pitfall 5: Silent rewrite of existing numbered headings
**What goes wrong:** a renamed heading breaks external citations. **Avoid:** check R6 (every base heading text present, in order).

### Pitfall 6: Two homes for one fact
**What goes wrong:** gate freezing described in §3.3, §8.3 and §24.1 differently. **Avoid:** write once in §24, pointers elsewhere (Pattern 1).

### Pitfall 7: Overclaiming trust
**What goes wrong:** text implies an A2 signature proves a human is present. **Avoid:** SPEC-04 must state, in normative text, that an agent able to use a human's credentials can act as that human; the same limit applies to the anchor location (SPEC-05) and to platform review (A1).

### Pitfall 8: Unevaluable result counted as a failure
**What goes wrong:** a retry-limit rule or a soft-fail rule treats "could not be evaluated" as failed. **Avoid:** every rule that counts failures says "satisfied-not" results only; add an AE where a missing tool does not consume an attempt.

## Code Examples

No code is shipped. The one executable artifact is the check script; its output contract, copied from Phase 1 [VERIFIED: `01-check-decision-record.sh:17-18`]:

```
PASS ID message
FAIL ID message
RESULT: PASS            (exit 0)
RESULT: FAIL N          (exit 1; exit 2 on usage error or unreadable file)
```

## State of the Art

| Old approach | Current approach | When changed | Impact |
|---|---|---|---|
| One model (nine phases) | Two method profiles | O-1, 2026-10-23 | §23 and §5.6 added |
| Three results | Four (`blocked`) | O-5 | §22.2, §22.3, per-action tables |
| `state.yaml` | `state.json` with canonical form | O-4 | §4.3, §8.1, §11.2, §25 |
| Version 1.3 | Version 1.4 | D-12 | Header; hand-off for the pinned `"1.3"` |

**Deprecated/outdated:** none retired; `reopen` becomes `full` only.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The applicability default (both unless `full` only) and the `full`-only list | SPEC-12, DC-27 | Owner may want core to drop Pair Review (§3.10, §14) or keep §4.1; the matrix is rewritten |
| A2 | Kind-to-category mapping of waits (T12) | DC-09 | Wrong category names in a table |
| A3 | `blocked` generalized to `full` (DC-05) | SPEC-03 | `full` table cells rewritten |
| A4 | Placement as new sections 5.6, 23, 24, 25 and the §1.1 categories | DC-01 | Reordering of the diff; no content loss |
| A5 | Per-rule-unit granularity of AE examples (about 40) | SPEC-14, OQ-3 | If per bullet, sizing grows five-fold |
| A6 | "High assurance" means a required A2 | SPEC-05, DC-11 | Anchor requirement attaches to a different trigger |
| A7 | VCS-neutral wording ("the revision the change started from") | SPEC-06, DC-21 | Reviewer asks for git-specific wording |
| A8 | Canonical-form restrictions (no floats; key order by code point) | SPEC-15, DC-14 | Hash mismatch across implementations |
| A9 | Per-method-profile base gate set | SPEC-16, DC-12 | Compliance profiles later need their own base gates (§5.1 change) |
| A10 | No `O-n` or requirement ids in the spec text | DC-17 | Reviewer wants traceability to the decision record inside the spec |

## Open Questions

1. **OQ-1 Assurance floors and base gates per compliance profile.** Known: D-04 keeps §5.1 unchanged; the prototype set `lean` to A0 and `standard` to A1 and gave each its own base gates. Unclear: whether compliance profiles gain a floor or base gates. Recommendation: owner decides at Phase 3; the draft assigns none.
2. **OQ-2 May an approved exception weaken a higher layer?** §5.3 says "silently", §4.2 says "without an approved exception", SPEC-16 says "must not". Recommendation: owner rules; the draft is absolute.
3. **OQ-3 Granularity of "each `full` rule has an acceptance example".** Per bullet (200+) or per rule unit (about 40). Recommendation: owner confirms the unit before Plan 5.
4. **OQ-4 `state.json` for `full`.** Mandatory (breaks inline Class S, §6.1 L369-371) or optional (the protections then cannot be enforced mechanically for those changes)?
5. **OQ-5 Cite the decision record in the spec?** O-n ids are not prototype ids, but self-containment suggests no. The draft cites none.
6. **OQ-6 `core` `supersede`:** outcome `cancelled` with `replaced_by`, or a fourth outcome `superseded`?
7. **OQ-7 Items no SPEC id owns:** exit codes (WORK-01) and the text-versus-binary classification rule for content hashing (INTEG-02). Add to a SPEC commit now, or hand to the engine phases explicitly?

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| git | check script, blob ids | ✓ | 2.56.0.windows.2 | — |
| bash | check script | ✓ | 5.3.15 (cygwin) | — |
| GNU awk, grep, sed | check script | ✓ | 5.4.1, 3.0, 4.9 | — |
| iconv, od, sha256sum | UTF-8, BOM, LF, D-02 hash | ✓ | libiconv 1.19; coreutils 8.32 | — |
| shellcheck | lint of the script (Phase 1 used a SC2016 disable) | ✓ | present | skip, report as not run |
| origin/main ref | base blob | ✓ | `d3e81a5` is its tip | — |

**Missing dependencies:** none. The `uv` baseline is not needed (no Python change); the plan must record it as not run.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | One read-only bash script, `.planning/phases/02-normative-drafting/02-check-normative-diff.sh`, in the style of Phase 1's script |
| Config file | none; options `--ref`, `--base REF` (default `origin/main`), `--base-blob ID` (default `da29d6f3bdef2e88fdd85a762939017d7d7034fa`), `--final`, `--version 1.4` |
| Quick run command | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh` |
| Full suite command | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --final` |

### Phase Requirements to Test Map

| Check | Behavior | Per-commit | `--final` | Mechanical? |
|---|---|---|---|---|
| B1 | `git rev-parse origin/main:PATH` still equals the base blob; else FAIL "base moved, re-record D-02" | yes | yes | yes |
| E1, E2, E3 | UTF-8 without BOM; LF only, one final LF, no trailing blank line; no tab; trailing whitespace only as exactly two spaces after text | yes | yes | yes |
| S1 | SPEC-13: no path under `src/` changed since the base (committed, staged, unstaged, untracked) | yes | yes | yes |
| S2 | Only `docs/method/GG-SAD_normative_method_specification.md` under `docs/method/` and paths under `.planning/` changed; nothing else (D-09) | yes | yes | yes |
| C1 | Every id in SPEC-01..12, 14..18 appears in the subject of at least one commit in `BASE..HEAD` that touches the spec; every spec-touching commit names at least one SPEC id (a range such as `SPEC-01..SPEC-18` may be expanded); SPEC-13 is covered by S1, S2 | no (needs all commits) | yes | yes |
| N1 | Added lines: no `SHALL`, `REQUIRED`, `RECOMMENDED`; WARN on lowercase `must`, `should`, `shall`; FAIL on malformed forms (`MUST not`, `NOT MUST`) | yes | yes | yes (heuristic) |
| X1 | Whole file, absolute (the base is clean): no `\bP-[0-9]+`, `\bA-[0-9]+`, `\bO-[0-9]+` (if DC-17 holds), `SPEC-[0-9]+`, `CHG-[0-9]+`, hex token of 7 to 40 characters containing a digit, `https?://`, drive-letter or home path, `gscore`, `ggsad-core-proto`, `MAPPING`, `MILESTONE-PROPOSAL`, `BACKLOG`; WARN on the word `prototype` | yes | yes | yes |
| R1 | Every `Section N` / `Sections N and M` / `Section N.M` reference resolves to a numbered heading; no duplicate heading numbers; top-level numbers contiguous from 1; subsection numbers contiguous within each section | no (forward refs) | yes | yes |
| R2 | `AE-nn` ids defined once, each defined AE is cited by a rule, each cited AE exists, each AE block has Given, When and Then lines; every new subsection in §23 to §25 cites at least one AE | no | yes | yes |
| R3 | No `TBD`, `TODO`, `FIXME`, `XXX`, `to be defined` outside fenced blocks (template `<...>` placeholders inside fences are legitimate) | no | yes | yes |
| R4 | `**Version:** 1.4` and a Revision line matching `^\*\*Revision:\*\* [0-9]{4}-[0-9]{2}-[0-9]{2} — .+\.$` | no | yes | yes |
| R5 | §1.1 map bijection: the set of `## N. Title` headings equals the set of map rows (title text equal); fences balanced (even count); table column counts constant per table | yes | yes | yes |
| R6 | Every heading present in the base is still present, unchanged and in order (renumber and retitle guard) | yes | yes | yes |
| R7 | `state.yaml` appears in no §4.3 tree line; the only permitted occurrence in the file is in the migration rule of §25.3 (WARN with line numbers); each `reopen` occurrence in §8 is within a line or paragraph that names `full` (WARN) | no | yes | partly |
| R8 | WARN list: added lines containing `profile` not preceded by `method `, `compliance `, `custom `, `default `, `selected `, `active `, for the D-05 review | yes | yes | heuristic |
| A1 | Print, read-only: base blob, result blob (`git hash-object FILE`), SHA-256 (`sha256sum`), line count, diffstat, commit list: the D-02 record for the Phase 3 packet | n/a | yes | yes |

### Sampling Rate

- **Per task commit:** the quick command (B1, E*, S*, N1, X1, R5, R6, R8).
- **Per plan (wave) merge:** quick command plus C1 for the requirements of that plan (`--ids` option, planner's choice).
- **Phase gate:** `--final` green, then A1 recorded, before the Phase 3 packet is written. Any later edit to the file voids A1.

### Wave 0 Gaps

- [ ] `.planning/phases/02-normative-drafting/02-check-normative-diff.sh` does not exist: write it first (before any spec edit, so every later commit is checked).
- [ ] Verify each check against the untouched base blob before relying on it (probes already pass on the base for E1 to E3, R5, R6, X1, fences and tables).
- [ ] Decide how a commit subject names a range of ids (C1).

### What only a human or the Phase 4 reviewer can judge

- Whether each rule faithfully states the protection the prototype exercised (facts digest above is the oracle, not the check).
- Whether a rule is self-contained, unambiguous and testable; whether examples cover normal and failure or boundary behavior at the right risk level.
- The correctness of every Drafting choice (DC-01 to DC-27) and of the `full` realizations, which no test can exercise (SPEC-14).
- Consistency between `core` and `full` tables, and absence of contradictions the script cannot see (for example the §5.3 versus §4.2 exception wording).
- That the text neither implies nor hides the trust limits (SPEC-04, SPEC-05, SPEC-11).
- Independence of review (Phase 4: Devin CLI, not the Requestor).

## Security Domain

Phase 2 changes documentation only: no code, no authentication, no secrets. ASVS categories do not apply to the deliverable. The content being specified is itself a threat model; the text must capture these patterns and their limits:

| Pattern | STRIDE | Mitigation the text must state |
|---------|--------|--------------------------------|
| Agent edits the gates that judge it | Tampering | Frozen definitions, re-approval (SPEC-01) |
| Agent acts as a human | Spoofing | Assurance levels, signed statement, plain admission of the credential limit (SPEC-04) |
| Replayed signature | Spoofing, Repudiation | Statement binds operation, change, history position, content (SPEC-04) |
| History truncated or rewritten | Tampering | Chain plus external anchor (SPEC-05) |
| Work outside scope or in ignored files | Elevation of privilege | Scope hard failure, isolation, interpreter explicit (SPEC-06, 11) |
| Baseline hides a new failure | Tampering | Baseline is frozen and human-approved (SPEC-07, 01) |
| Environment fault read as pass or fail | Denial of service, Repudiation | Three-valued results (SPEC-02) |

## Sources

### Primary (HIGH confidence; all read this session)
- `docs/method/GG-SAD_normative_method_specification.md` (blob da29d6f, lines 1-1422) and bash probes for line endings, encoding, tables, fences, map bijection.
- `.planning/phases/02-normative-drafting/02-CONTEXT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/config.json`.
- `docs/decisions/2026-10-23-executable-core-decisions.md` (O-1 to O-11), `AGENTS.md`, `CLAUDE.md`.
- `.planning/phases/01-decision-record/01-check-decision-record.sh` (check script model).
- Prototype: `MAPPING.md`, `MILESTONE-PROPOSAL.md`, and `src/gscore/` `engine.py`, `evaluate.py`, `store.py`, `canon.py`, `signing.py`, `env.py`, `model.py`, `profiles.py`.
- `.ggsad/config.yaml`, `.ggsad/schemas/*.schema.json` (grep), `specs/examples/class-m/state.yaml`, `src/ggsad/application/initialize_project.py` and `tests/unit/test_initialize_project.py` (grep for `"1.3"`).

### Secondary / Tertiary
- None. No web research was used (ruled out by the task).

## Metadata

**Confidence breakdown:**
- Standard stack: n/a (no packages).
- Architecture (placement, ordering): MEDIUM, judgment backed by the line facts above.
- Spec line facts and prototype facts: HIGH, read this session with quoted values.
- SPEC-14, 16, 17, 18 content: LOW, unproven by the prototype.
- Pitfalls: HIGH for traps tied to line numbers; MEDIUM for DC resolutions.

**Research date:** 2026-10-24
**Valid until:** the next edit to the specification on `origin/main` or to the decision record (re-run `git rev-parse origin/main:docs/method/GG-SAD_normative_method_specification.md` against `da29d6f3bdef2e88fdd85a762939017d7d7034fa`); line numbers shift as Phase 2 commits land.
