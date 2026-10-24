---
phase: 02-normative-drafting
reviewed: 2026-10-24T00:00:00Z
depth: standard
files_reviewed: 1
files_reviewed_list:
  - docs/method/GG-SAD_normative_method_specification.md
findings:
  critical: 3
  warning: 27
  info: 14
  total: 44
status: issues_found
---

# Phase 2: Code Review Report

**Reviewed:** 2026-10-24
**Depth:** standard
**Files Reviewed:** 1
**Status:** issues_found

## Summary

Scope: `git diff origin/main` of `docs/method/GG-SAD_normative_method_specification.md` (header, 3.x, 4.x, 5.3 to 5.6, 8.x to 12, 15, 16.1, 19 to 22, new sections 23 to 25). The advisory same-product review is for the Requestor's own use. It does not replace the Phase 3 owner approval or the Phase 4 independent review.

Mechanical checks that were run, with no defect found:
- All 269 acceptance-example ids (AE-01 to AE-269) are defined exactly once, and every `AE-n` reference resolves.
- All cross-references of the form `Section N.N` point to existing headings.
- Both JSON blocks (lines 809 and 1345) parse.
- The hash strings in AE-183 and AE-184 recompute correctly (SHA-256 of `{"count":2,"name":"café"}` and of `{}`).

The substantive defects are semantic and are concentrated in three areas:
- **Section 23, `core`.** The `review` gate kind cannot be satisfied (CR-01). The gate shape is under-specified (WR-06). Several `core` rules conflict with the "Applies To" table of 5.6 (WR-03, WR-04, WR-05).
- **Section 25.1 versus 24.5.** A crash artifact turns into an irreversible hard failure (CR-02). The write-lock rule is weak (WR-14).
- **Section 24.1 for `full`.** The hashed value for `full` omits what 24.1 and 24.9 say is frozen (CR-03).

Items already recorded in `02-DRAFTING-CHOICES.md` as deferred are not repeated. These are the unnamed configuration keys, the text-versus-binary hashing rule, and the unproven items.

## Critical Issues

### CR-01: The `review` done-gate kind has no defined way to be satisfied or evaluated

**File:** `docs/method/GG-SAD_normative_method_specification.md:2299`, `:2346`, `:2084-2086`
**Issue:** 23.3 defines a done gate of kind `review` as "satisfied by a recorded review result from a participant other than the participant that requested the reviewed work". No operation or action records a review result.
- The 23.4 transition table has no such row.
- The `review` action is declared read-only: "they never change its state or its history" (2346).
- The contract operations of 22.1 list only "record a human decision (an approval, a sign-off, an override, or an answer)".
- Section 24.2 requires every gate to evaluate to `satisfied`, `not_satisfied`, or `not_evaluable`, but gives no evaluation method for a `review` gate.
- The history `body` (25.1) has no field for a review result, reviewer identity, or reviewed revision. The eight-field Pair Review record of 14.5 lives in `evidence.md` or `review.md`, which are not machine-evaluated. `review.md` is also scope-measured (4.3, 24.5).

A `core` change with a `review` gate (for example the `review-ok` gate in AE-224) can therefore never reach `close`, or the result depends on an unspecified out-of-band file. This is a normative gate kind that is unrealizable as written.

**Fix:** Either add a recording mechanism or drop the kind.
- Add a `core` action row, for example `review-result`, legal from `active`.
  - It carries the reviewer identity, the reviewed revision or content hash, a result, and a disposition.
  - It is recorded in the history (`body.files` plus `note`).
  - The `review` gate is `satisfied` when the latest recorded result for the gate has result `approved`, a reviewer different from `author`, and a content hash equal to the current hash.
- Then add that operation to 22.1 and add acceptance examples (satisfied, same-participant rejected, stale revision).
- Alternatively, remove `review` from the 23.3 kinds and let `sign-off` carry reviews.

### CR-02: A leftover temporary or lock file in the change directory becomes an irreversible hard scope failure

**File:** `docs/method/GG-SAD_normative_method_specification.md:4099`, `:4101`, `:3466-3468` (also AE-193 and AE-194, `:4183-4197`)
**Issue:** 25.1 mandates atomic replacement through "a temporary file in the same directory". It says a leftover temporary file "is not state: an implementation MUST ignore it and MAY remove it". The write lock (4101) is taken on "the place where the document will be created", which may also leave an artifact.

24.5 exempts only three record files (`change.yaml`, `spec.md`, `state.json`) from the scope measurement. It states: "Every other file in the change directory is measured." It also counts "files that version control does not track and has not been told to ignore". After an interrupted write (the very scenario of AE-193 and AE-194), a stray `specs/<id>/state.json.tmp` is an untracked, unexempted path outside `scope.allow`. The next `close` or `resume` then finds the hard `scope-violation` and closes the change as `failed` without human action (24.7). A closed change is final (23.2). A crash therefore permanently fails the change, and the rule "ignore it" in 25.1 does not stop that.

**Fix:** Pick one of these and add an acceptance example.
- Add a rule in 24.5 that exempts the implementation-owned temporary and lock artifacts of 25.1. They would need a reserved, specified name or suffix in the change directory, for example a `.tmp` or `.lock` suffix on the state document name.
- Or require the temporary and lock artifacts to live outside the working tree, next to the anchor. This conflicts with the "same directory" rename-atomicity requirement, so the exemption is probably simpler.

### CR-03: The parsed value of `full` gate definitions omits the requirement evidence commands that 24.1 and 24.9 say are frozen

**File:** `docs/method/GG-SAD_normative_method_specification.md:2840` against `:2948`, `:3927`, `:3913`, `:2912-2914` (AE-257), `:1723`, `:1835`
**Issue:** 2840 defines the hashed value of `full` gate definitions as "an object with three members": `flow_gates`, `scope`, `definitions`. Three other places contradict it.
- 2948 and 3927 say "The requirement identifiers and the evidence commands that are bound to them are also fixed with the gate definitions ... A difference between them and the approved ones is a difference of the gate definitions".
- AE-257 relies on this: "an evidence command is added for the second requirement, the gate definitions are approved again".
- 3913 puts the full evidence commands "in the change specification (16.1), where the Evidence cell of the requirement coverage table (16.4) names them". 16.1 has no field for evidence commands. 16.4 is `evidence.md`, a conditional file that is a record of results and is produced after approval.

Taken literally, the hashed object has no member for requirements or evidence commands. A participant can therefore swap an evidence command for `true` in a `full` change without producing `gates-changed`. That is exactly the bypass AE-169 forbids for `core`, and there is no `full` counterpart to AE-169. The purpose stated in 24.1 ("no participant can change the gates that judge a change without a human approving the change again") is defeated for `full`.

**Fix:**
- Extend the 2840 object with a fourth member, for example `requirements`.
  - It is a list of `{id, evidence_commands}` parsed from a defined, machine-readable place in `spec.md`.
  - Add the matching home in the 16.1 template, for example a per-requirement `Evidence command` list.
  - Do not use the `evidence.md` Evidence cell.
- Update 3913 and 1835 accordingly, and add a `full` acceptance example equivalent to AE-169.

## Warnings

### WR-01: `start` with an active hard failure is "rejected" in 23.4, 24.2, and 8.3, but "closes the change as failed" in 24.7

**File:** `docs/method/GG-SAD_normative_method_specification.md:3664` against `:3076`, `:2358`, `:856`, `:2734`, `:2333`
**Issue:** 24.7 says that when "an action that evaluates gates finds a fail condition of the severity `hard` active, the action MUST close the change as failed in the same state mutation. This decision comes before every other decision of Section 24.2". `start` evaluates gates. 24.2 (3076), 23.6 (2734), and both Rejected/Blocked tables (856, 2358) say `start` "requires that none of the rules 1 to 4 would decide: when one would, `start` is rejected and no wait is created". Rule 1 is the hard fail. For `start` with an active hard fail gate, the two rules give opposite results: a failed closure with `success`, or `rejected` with the change unchanged. No acceptance example covers it (AE-117, AE-124, and AE-74 cover wait gates and unevaluable gates only).
**Fix:** Add an explicit carve-out to 24.7, or to the `start` row. For example: "`start` never closes a change; an active hard fail gate makes `start` `rejected` with `start-blocked`, and the failure is decided at the first action that completes the change." Alternatively, make `start` the single action that turns a hard failure into a close. Add an example either way.

### WR-02: The 8.3 `complete` row says unsatisfied DoR/DoD is both a rejection and `blocked`

**File:** `docs/method/GG-SAD_normative_method_specification.md:844`, `:857`, `:873` (AE-121)
**Issue:** The Precondition cell of `complete` reads: "From `draft`, the current phase's DoR is satisfied; from `active`, the current phase's DoD is satisfied". The Rejection Behavior cell begins: "Reject ... when the applicable precondition is not satisfied". The same cell continues: "When DoW, current-phase DoR, or current-phase DoD does not allow the transition, ... answer `blocked`". The result table (857) repeats the overlap. A reader cannot tell whether an unsatisfied DoD is a precondition failure (`rejected`, `changed` false) or an evaluation (`blocked`, `changed` true). AE-121 chooses `blocked`. The base text (origin/main) said "Reject ... when ... DoW, current-phase DoR, or current-phase DoD is not satisfied", and the phase's edit left the Precondition cell untouched.
**Fix:** Reword the Precondition cell to "From `draft`, the evaluation of the current phase's DoR is requested; from `active`, ..." and limit "precondition" in the Rejection cell to the legal-source and authorization checks.

### WR-03: 11.1 is marked `full` only in 5.6, but `core` and the shared sections use its wait categories

**File:** `docs/method/GG-SAD_normative_method_specification.md:539` against `:2689-2698`, `:2716-2722` (AE-52), `:3803`, `:1328-1330`
**Issue:** The applicability table lists "11.1" under `full` only, and says a `core` change MUST NOT be required to satisfy a rule of a `full`-only section. 23.5 maps every `core` wait kind to "a wait category of Section 11.1". AE-52 requires `core` to "report in the wait categories of Section 11.1". 24.8 assigns `WAIT_USER_INPUT` (a 11.1 category) to a wait caused by a question in both profiles. 11.1 itself holds the two new sentences about gates that cannot be evaluated (24.2) and soft failures (24.7), which are shared protections.
**Fix:** Move 11.1 to the "Both method profiles" row of the 5.6 table.

### WR-04: Sections 19 and 20 are "Both" per 5.6 but are written in `full` terms that `core` does not have

**File:** `docs/method/GG-SAD_normative_method_specification.md:541` against `:1985-2004`, `:2023-2035`, `:2200`
**Issue:** Per the 5.6 table, 19 and 20 apply to both profiles ("Every other section of Sections 1 to 22"). 23.1 (2200) says a `core` change has "no phase, no Definition of Ready or Definition of Done per phase". Section 19 tells every agent to "Evaluate DoD for the current phase", "Evaluate DoR for the next phase", and "Start the next phase only if its DoR is satisfied". Section 20 defines completion as a transition "into the `closed` phase with the terminal status `done`" with "all required DoD criteria". `core` has the state `closed` and the outcome `done`, and it closes only through the `close` action of 23.4. As written, a `core` agent is required to run steps that do not exist for it.
**Fix:** Either add 19 and 20 to the `full` only list and give `core` equivalents (23.6 is the `core` algorithm), or add `core` wording in each ("for `core`: the states and outcomes of 23.2, the gates of 23.6").

### WR-05: 12.2 is "Both" but the `core` fail gate has none of its mandatory content

**File:** `docs/method/GG-SAD_normative_method_specification.md:541`, `:1410-1418` against `:2291-2299`
**Issue:** The 5.6 table exempts only "the final status code of a fail rule" from 12.2 for `core`. The remaining mandatory content of a fail rule (trigger, required response, permitted preservation actions, required documentation) therefore applies to `core`. A `core` fail gate (23.3) has an `id`, a `severity`, and an unspecified condition, with no response, preservation, or documentation field. Either every `core` fail gate is non-conformant, or the table is wrong.
**Fix:** State in the 5.6 table which 12.2 items `core` is exempt from (response, preservation actions, documentation as well), or add those fields to the `core` fail-gate definition.

### WR-06: The `core` fail and wait gates are said to have no kind but also need one, and their condition has no representation

**File:** `docs/method/GG-SAD_normative_method_specification.md:2299`, `:3082`, `:2294` (and AE-74, `:3196-3202`; AE-94, `:3636-3642`)
**Issue:** 23.3 gives a `kind` to done gates only (`check`, `review`, `sign-off`). The sentence that ends the paragraph rejects "a gate without a kind, a gate with more than one kind" for every gate. As written, a valid fail or wait gate (which has no kind) must be rejected.

5.3 (378, 384) and AE-222 compare "kind" and "condition" of base fail and wait gates. 24.2 (3082) says a check-command gate "in `core` ... is a done gate of the kind `check`". Yet AE-74 and 23.6 step 2 give a wait gate "whose condition cannot be evaluated". AE-94 rejects a baseline "on a wait gate" because it is "not a check-command gate". No text says how the condition of a `core` fail or wait gate is written (command, retry limit, predicate name). Nothing therefore defines when such a gate is `not_evaluable`, nor what "alters the condition" means for the weakening check. DC-33 records the gates as "predicate gates" without a representation.
**Fix:** Define the representation: at minimum, "a fail or wait gate has a `condition` that is one of `command` (a check-command gate), `retry_limit` (with `gate` and `limit`), or a named built-in predicate". Restrict the "without a kind" rule to done gates.

### WR-07: "Stop as soon as a gate decides" conflicts with ranking an unevaluable gate above an active wait gate

**File:** `docs/method/GG-SAD_normative_method_specification.md:2726-2734`, `:3068-3076`, `:1012`, `:1022-1024` (AE-248), `:2756-2758` (AE-55)
**Issue:** 23.6 and 8.5 order the decisions fail, wait, ready, done and require evaluation to "stop as soon as a gate decides". 24.2 and 23.6 rank "a gate that is `not_evaluable`" (which may be a done gate or an evidence command) above "a wait gate that is active". In `core`, an `active` change has an active wait gate and an unevaluable `check` done gate. If evaluation stops at the wait gate (by gate type), the change stays `active` and `close` answers `blocked`. If it evaluates every gate first, the change becomes `waiting` with a wait record of kind `external`. AE-248 states that "the later gates are not evaluated". The result therefore depends on an implementation's evaluation order, which 5.3 forbids ("The result ... MUST NOT depend on the order"). No acceptance example covers the combination.
**Fix:** Say whether commands of lower-ranked gate types are run when a higher-ranked decision exists. If the intent is "stop by gate type", make the `not_evaluable` rule apply only to gates evaluated up to the deciding gate. If the intent is "rank by outcome", say that all applicable gates are evaluated first. Add an acceptance example.

### WR-08: A `core` agent in a wait state cannot record the question that 11.3 requires

**File:** `docs/method/GG-SAD_normative_method_specification.md:1380` against `:2335`
**Issue:** 11.3 (applies to both profiles) says the question that the agent formulates in a wait state "is recorded as an open question of the change (Section 24.8)". In `core`, `ask` is legal only from `open` and `active` (2335). A change that entered `waiting` by evaluation (kinds `external` or `fail-gate`) cannot take an `ask`. The `wait` action that carries a question is legal only from `active`. The agent in a wait has no action that records its question.
**Fix:** Allow `ask` from `waiting` (the question gate then keeps the change from resuming until answered, which is consistent with 23.7), or state that 11.3's recording sentence applies to `full` only.

### WR-09: The `wait` action "gives" a question in 23.5 and 24.8 but "names" an existing one in AE-29

**File:** `docs/method/GG-SAD_normative_method_specification.md:2334`, `:2680`, `:3803` against `:2483-2489` (AE-29)
**Issue:** 24.8 says "the `wait` action that gives a question records it and pauses the change". 23.5 says the `question` kind exists because "the `wait` action gave a question". AE-29 has the `wait` action name an existing unanswered question, "Q1". Which is it? The rule does not say what happens in each case. Open points:
- Does `wait` create a new question when given text?
- Does `wait` naming an already answered question get rejected?
- Does a `wait` naming a question owned by another participant keep that owner as the wait `owner`?
**Fix:** Pick one: `wait` takes a question identifier (existing, unanswered, required to be rejected otherwise), or `wait` takes question text and records it as the next `Q<n>`. Update 23.4, 23.5, 24.8, and AE-29 consistently, and add the rejection example for an answered question.

### WR-10: The stale-specification-approval gate is undefined when the specification was never approved

**File:** `docs/method/GG-SAD_normative_method_specification.md:2766`, `:2333`, `:3222`
**Issue:** The base gate `stale-spec-approval` is "active while `spec.md` differs from the version that was approved". If no version was ever approved, there is no "version that was approved". 23.4 `start` says the specification must be approved only "when the compliance profile or the project configuration requires it". If the gate is read as "active whenever the current hash differs from the approved hash (none)", every `lean` change that does not require approval can neither start nor close. If it is read as inactive, the text has to say so. AE-57 covers only approve-then-edit.
**Fix:** State "The gate is active only if the specification was approved at least once and the current content hash differs from the last approved content hash." Add an acceptance example for an unapproved specification in a project that does not require approval.

### WR-11: Creation of the anchor for a new change is unspecified, so under A2 every new change appears to need `adopt` first

**File:** `docs/method/GG-SAD_normative_method_specification.md:3362`, `:3374`, `:2342` (and AE-140, `:3402-3408`)
**Issue:** Where configuration requires A2 approvals, the history "MUST have an anchor ... and an implementation MUST NOT act on a change whose history has none until a human adopts the history". `adopt` is the only anchor-creating action. The text also says the anchor "is advanced" after every append and "is only advanced" (3372). Nothing says that `new` creates the anchor with the first entry. A literal reading is that every new change in an A2 project is unusable until a human performs `adopt`. A reader could equally assume that `new` creates the anchor, but then it does not say who performs it or that it is exempt from "MUST NOT replace".
**Fix:** State that the first successful append of a new change creates the anchor (position 1), and that `adopt` is for histories that had no anchor (legacy or migrated). Add an acceptance example for `new` followed by `start` in an A2 project.

### WR-12: `schema-version-mismatch` and `migration-required` or `schema-version-unsupported` can both apply to the same state document

**File:** `docs/method/GG-SAD_normative_method_specification.md:4287-4299`, `:2107`, `:4369-4375` (AE-211)
**Issue:** 25.3 first checks the `schema_version` of the file (a migratable version gets `migration-required`, anything else unusable gets `schema-version-unsupported`). 4299 then adds `schema-version-mismatch` for a state document whose version differs from the last recorded version. AE-211's input (document edited down to `"1.0"`, last entry records `"1.1"`) is, for an implementation that holds a `1.0` to `1.1` step, a migratable version, so the first check yields `migration-required`. AE-211 expects `schema-version-mismatch`. Without a stated order of the checks, AE-211 and the bullet list contradict each other. The 4299 purpose ("detects a document whose version was lowered by hand in order to run a migration again") is exactly the case where the first check would pass the document to a migration.
**Fix:** State the order: "For a state document, the consistency check against the last recorded version is made first; only a document that matches it is checked against the supported versions."

### WR-13: `not_applicable` must be recorded in `gate_results`, but 24.2 says any non-result name must be rejected

**File:** `docs/method/GG-SAD_normative_method_specification.md:3054`, `:3090` against `:4062`, `:1012`, `:2734`, `:3470`, `:3152-3154` (AE-68), `:3562-3564` (AE-157)
**Issue:** 24.2: "A name in another letter case, or any other name, is not a result and MUST be rejected" (AE-61). 24.2 also says "`not_applicable` is not a result". 8.5, 23.6, 24.5, AE-68, and AE-157 all require a gate that does not apply to be "recorded as `not_applicable`". 25.1 defines `gate_results` as "an object from the identifier of each gate that the action evaluated to the result recorded for it (Section 24.2)", which allows only the three results. A validator that enforces 25.1 and AE-61 rejects the mandated `not_applicable` entries. The wording leaves unclear which field holds the marker.
**Fix:** In 25.1, state the value domain of `gate_results` and `gate_detail`: "`satisfied`, `not_satisfied`, `not_evaluable`, or the marker `not_applicable`". Scope the AE-61 rule to "a record of a result".

### WR-14: The write protection of 25.1 covers only evaluations, and it locks a file that the same write replaces

**File:** `docs/method/GG-SAD_normative_method_specification.md:4101`, `:4099`
**Issue:** There are two problems.
- **Scope.** The lock-and-compare rule "applies to the creation of a change and to every operation that records an evaluation". `approve`, `ask`, `answer`, `wait`, `cancel`, `adopt`, and `migrate` also append entries. Two concurrent `ask` calls that both read version 6 are not covered, and one entry is lost. AE-191 and AE-192 cover only creation and `close`/`complete`.
- **Mechanism.** The lock is "an exclusive lock on the state document", while the write replaces that same path (rename) in a single step. A lock held on the old file does not exclude a process that opens the new file after the rename. A lock on "the place where the document will be created" for a document that does not exist yet has nothing to lock.

**Fix:** Apply the protection to every operation that appends an entry. Specify a separate lock object (a lock file or directory with a reserved name, ignored by the scope measurement, see CR-02) held across compare-and-replace.

### WR-15: The list of history-dependent rules that need a state document omits rules that read or write the history

**File:** `docs/method/GG-SAD_normative_method_specification.md:305`, `:4051`, `:2831` against `:3078`, `:3673`, `:3464`
**Issue:** 4.3 and 25.1 enforce "Sections 24.1, 24.3, 24.4, and 24.8" mechanically only when a state document exists, and an implementation "MUST NOT report any of them as enforced" otherwise. The criterion is "rules ... that read or write the history". Other rules clearly read or write the history:
- The retry-limit count in 24.2 is "the number of `not_satisfied` results of that gate in the history".
- An override and its attempt count in 24.7 are recorded in the history and bound to the approved hash.
- The base revision in 24.5 is recorded in the state.

The retry limit and override of an inline-record `full` change therefore cannot be computed, but the text neither lists them nor says what happens.
**Fix:** Extend the list to 24.2 (retry limits), 24.5 (base revision), and 24.7 (overrides and attempts), or define a `full` inline-record fallback. Update the AE-195 report accordingly.

### WR-16: A `failed` outcome "MUST carry a reason text", but the state record has no field for it, and a hard failure has no actor text

**File:** `docs/method/GG-SAD_normative_method_specification.md:2259` against `:4065`, `:4070-4079`
**Issue:** 23.2: "An outcome of `failed` MUST carry a reason text." The `after` record of 25.1 has `state`, `outcome`, `approvals`, `questions`, `wait`, `base_revision`, `replaced_by`, `schema_version`, and no reason field. The only text field is `note` ("the text that the actor gave, or `null`"). A hard-failure closure by `close`, `resume`, `cancel`, or `supersede` has no actor-supplied reason, so `note` is `null`, and the paths "outside the scope" named in AE-148 have no defined home other than `gate_detail`. The "MUST carry" rule cannot be checked from the state record.
**Fix:** Add `reason` to the `core` `after` record (null unless the outcome is `failed`), set from the `fail` reason, or generated from the failing gate identifiers and details for a hard failure.

### WR-17: The `action` names of the 25.1 body are undefined for the `full` operations that have no table row

**File:** `docs/method/GG-SAD_normative_method_specification.md:4057` against the 8.3 table (`:841-850`) and `:2084`
**Issue:** `body.action` is "an action of the transition table of the method profile (Section 23.4 or Section 8.3) or `migrate`". The 8.3 table has no `new`, `approve`, `ask`, `answer`, or `adopt`. Yet `full` changes are created, approved, answered, and adopted (22.1, 24.3, 24.4, and 24.8 apply to `full`), and each must write an entry. There is no valid `action` value for them. Entry 1 of every `full` state document is therefore unnameable.
**Fix:** Define `action` as "the name of the operation", with a closed list shared by both profiles (`new`, `approve`, `ask`, `answer`, `adopt`, `migrate`, plus the table actions of the profile).

### WR-18: 5.3 and AE-226 say layer 6 does not apply to `core`, while 3.8, 17, and 25.3 apply integration mappings to every change

**File:** `docs/method/GG-SAD_normative_method_specification.md:382` against `:135-147`, `:1952-1965`, `:4281`, `:541`
**Issue:** 382 states "the integration mappings of layer 6 are not part of the resolution of a `core` change", but in the same paragraph "Both layers are specified for the `full` method profile and for combination use (Sections 3.8 and 17), and in both the rule that a lower layer MUST NOT weaken a higher layer applies." Sections 3.8 and 17 apply to both profiles. 25.3 lists "the integration mappings" as a schema-governed file and describes migrating it "inside a change", with no `full` restriction. A `core` change in combination mode has integration mappings and an integration mapping contract (17). The text says both that they are out of the `core` resolution and that the no-weakening rule applies to them.
**Fix:** Decide the intent. If `core` supports combination mode, layer 6 applies and AE-226 changes. Otherwise state that a `core` change cannot be used in combination mode, and limit 17 and the 25.3 integration-mapping rules to `full`.

### WR-19: Is the compliance profile selected per project or per change?

**File:** `docs/method/GG-SAD_normative_method_specification.md:329`, `:523`, `:2191`
**Issue:** 5.1: "Every project MUST select one active compliance profile in `.ggsad/config.yaml`". 5.6 and AE-132/AE-226 treat the compliance profile as a property of each change ("Every change has exactly one ... compliance profile", `compliance_profile` is a required field of `change.yaml`). Nothing says that the change's value MUST equal the project's, nor that it MAY differ. If it may differ, a change definition (layer 5) can select `lean` in a `regulated` project, which weakens the project selection in layer 2 and 3. If it may not, the field is redundant and unchecked.
**Fix:** Add a rule: "`compliance_profile` of a change MUST equal the active compliance profile of the project, or name a profile at least as strict; otherwise `new` is rejected", and an example.

### WR-20: 24.3 and 23.4 require a human for "every approval", while 5.1 and 5.4 keep `lean` self-approval, including agent self-approval

**File:** `docs/method/GG-SAD_normative_method_specification.md:335`, `:476-485` against `:2344`, `:3220`, `:2860-2866` (AE-251)
**Issue:** 5.1 gives `lean` "self-approval permitted unless a critical rule applies". 5.4 says that "agent self-approval" may not satisfy the four non-delegable decisions and that `lean` self-approval "is permitted only for decisions outside this non-delegable set". The new last paragraph of 5.4 adds that "the self-approval allowance ... is unchanged". But 24.3 states "These actions MUST be performed by a human: every approval, ..." and 23.4 says `approve` "MUST be performed by a human participant", for both profiles including `full`. For a `lean` change, "self-approval by an agent" outside the set is allowed by 5.4 and forbidden by 24.3. The "unchanged" sentence is false as written.
**Fix:** Either restrict the "every approval" sentence in 24.3 and 23.4 to "every approval that 5.4 does not allow to be self-approved under `lean`", or narrow the `lean` allowance in 5.1 and 5.4 to a human self-approval.

### WR-21: "A verified human" in 5.4 is undefined and conflicts with 24.3 and AE-130/AE-132

**File:** `docs/method/GG-SAD_normative_method_specification.md:485` against `:3216-3220`, `:3291-3313`
**Issue:** 5.4 says an A0 claim "does not by itself satisfy a decision that needs a verified human". 24.3 defines no "verified human": only the `human:` prefix is required, no level proves a human is present (3249), and a compliance profile sets no minimum level (3218). AE-130 and AE-132 record an A0 approval by `human:ada` as valid in a `regulated` change. A non-delegable decision of 5.4 under a project with no configured minimum is therefore either satisfied by A0 (AE-132) or not (5.4). No acceptance example covers 5.4.
**Fix:** Replace "a verified human" with a testable condition: "a claim whose verified level is at least the level required under Section 24.3 for that kind of action". Add an example for a non-delegable decision at A0 with no configured minimum.

### WR-22: 22.1 and 22.3 point to the Section 8 transition table only

**File:** `docs/method/GG-SAD_normative_method_specification.md:2086`, `:2163` against `:2161`, `:2327`
**Issue:** Section 22 applies to both profiles. The last contract operation is "evaluate and execute one controlled state transition under the Section 8 Transition Table". The last paragraph of 22.3 requires an implementation to "record transition history and relevant evidence under the Section 8 Transition Table and Section 15 Evidence Model". The `core` transition table is in 23.4 (2161 does cite both). The 22.1 operations list also does not name the operations `core` needs and the evidence list assumes (`ask`, `answer`, `adopt`, `check`, `review`, `guard`).
**Fix:** Say "under the transition table of the method profile (Section 8.3 or Section 23.4)" in both places and extend the 22.1 list, or state that `record a human decision` covers `ask`, `answer`, and `adopt`.

### WR-23: The change identifier is used as a directory name and in references, with no syntax rule

**File:** `docs/method/GG-SAD_normative_method_specification.md:2189`, `:289-299`, `:307-314`, `:2341`
**Issue:** `id` is "unique among the changes of the project" and names the directory `specs/<change-id>/`. It is also the value of `follows` and `replaced_by`. The text compares identifiers as code point sequences without normalization (24). There is no grammar for `id`.
- A value such as `../x`, `a/b`, or an absolute path escapes or nests the change directory.
- Two ids that differ only in case, or in Unicode normalization (AE-60), map to one directory on case-insensitive or normalizing file systems, so "unique" is not "distinct directory".
- Reserved device names on Windows are valid code point sequences.

The drafting choices register notes that scope patterns were hardened against `..`, but the same hardening is missing for the `id`, which is also a path.
**Fix:** Add a rule: "`id` MUST match `[a-z0-9][a-z0-9._-]*`, contain no path separator, and be unique after case folding. A violating definition is rejected." Add a rejection example.

### WR-24: The minimum assurance levels and the interpreter live in a repository file, outside every integrity protection

**File:** `docs/method/GG-SAD_normative_method_specification.md:329`, `:3212`, `:3218`, `:3997` (and `:3999`)
**Issue:** 24.3 deliberately keeps the signers file "outside the repository ... so that a participant who can change the repository cannot add a key for itself". The required assurance level, however, is the maximum of the gate minimum and "the minimum that the project configuration sets" (3218). That configuration is `.ggsad/config.yaml` (329), inside the repository. The frozen gate definitions (24.1) do not include it, the history does not record the level that was required, and the scope check covers it only if a change's allowed path list does not already admit `.ggsad/`. A participant that can edit the repository can lower the minimum from A2 to A0, approve at A0, and restore the file. The same applies to the interpreter that the token `@interpreter` stands for (3997). The interpreter decides "whether every gate passes", and 24.10 only advises a warning.
**Fix:** Record the required level and the verified level in each approval entry and have the implementation reject a lower configured minimum than the highest required level already used in the history. Alternatively, hash the assurance-relevant configuration keys into the approved hash or keep them outside the working tree like the signers file.

### WR-25: AE-263 and 9.4 let a specification with an open question be "ready", but 24.8 and 8.5 make an open question block every `complete` in `full`

**File:** `docs/method/GG-SAD_normative_method_specification.md:1078`, `:1217-1219` (AE-263) against `:3809`, `:1002-1010`, `:844`
**Issue:** 9.4 says a still-open question about the goal "is recorded as an open question" and does not make Ready-to-Spec depend on it. AE-263 says the second specification (one unanswered question) is "ready as well". 24.8 says that in `full` an unanswered question makes a Definition of Wait condition active, so "`complete` and `resume` answer `blocked`". Per 8.5, DoW is evaluated before DoR, and `complete` from `draft` (the action that moves the specify phase to `ready`) is evaluated "DoF → DoW → current-phase DoR". The `complete` that establishes the "ready" status is therefore blocked while the question is open, and the specification cannot be both ready and have an unanswered question.
**Fix:** Either exclude questions raised in the specify phase from the DoW condition until the DoD of that phase, or reword AE-263 and 9.4 so that "ready" is a statement about the DoR criteria alone and say that `complete` still answers `blocked`.

### WR-26: A `full` change need not state an allowed path list, but without one it can never complete

**File:** `docs/method/GG-SAD_normative_method_specification.md:626`, `:3460`, `:3470` (AE-253, `:2876-2882`; AE-231, `:630-636`)
**Issue:** 24.5: "a change specification that states no allowed path list has a scope that cannot be measured", and after the start such a scope is `not_evaluable`. 24.2 turns `not_evaluable` into a wait at the next `complete`. Class S minimum content (6.1) is goal, scope, acceptance conditions, and verification, and AE-231 treats that as sufficient. A scope stated in words only (Included/Excluded) meets 6.1 and the 16.1 template, but never produces `satisfied`, so the change waits at every `complete` and cannot finish. Only a human `cancel`, `supersede`, or `fail` ends it.
**Fix:** Require the allowed path list in the minimum content of 6.1 and in the Ready-to-Build criteria (9.6), or state that an unmeasurable scope in `full` is `not_applicable` for changes that explicitly opt out with an approved record.

### WR-27: AE-198 does not establish that the example files are binary

**File:** `docs/method/GG-SAD_normative_method_specification.md:4243-4245` (and `:4223`)
**Issue:** AE-198 says "two binary files that differ only in that the first holds the bytes 0D 0A where the second holds the byte 0A" and expects different content hashes. 25.2 leaves the text-versus-binary decision to the implementation ("SHOULD classify a file as text only when its bytes are valid UTF-8 and hold no zero byte"). If the files contain only valid UTF-8 and no zero byte, a conforming implementation classifies them as text, normalizes CRLF, and produces equal hashes. The expected result fails for such content. The example does not say that the files hold a zero byte or invalid UTF-8.
**Fix:** State the content, for example "two files that each hold the byte 00 and differ only in 0D 0A versus 0A", so that every classification rule yields binary.

## Info

### IN-01: 5.3 lists lowering an assurance level as a weakening, then accepts it as "no effect"

**File:** `docs/method/GG-SAD_normative_method_specification.md:378`, `:380`, `:384`, `:410-416` (AE-221)
**Issue:** 378 defines a weakening to include "lowers the assurance level that the gate or the action requires" and forbids it. 380 and AE-221 then accept such a statement ("accepted and has no effect"), and the rejection check of 384 lists only kind, condition, and severity. It is not clear whether the "MUST NOT" is met by rejection or by neutralization.
**Fix:** Say in 378 that a lower assurance statement is neutralized (not rejected), or add it to the rejected cases of 384.

### IN-02: Behavioral rules without any acceptance example (3.9)

**File:** `docs/method/GG-SAD_normative_method_specification.md:485`, `:4295`, `:4082`, `:2675`, `:3247`
**Issue:** 3.9 requires at least one example per behavioral requirement. These changed rules have none:
- The A0 paragraph of 5.4 (485).
- `migrate` refusing a file that already has the target version, and a failing step answering `error` with the earlier steps discarded (4295).
- The duplicate-key rule for the state document (4082; AE-188 covers only layout).
- The `expires` field and overdue wait of 23.5 (2675, 2687).
- The SHOULD-refuse-an-unprotected-key rule of 24.3 (3247; AE-134 illustrates the risk only).

**Fix:** Add one example each, or the alternative acceptance condition 3.9 asks for, with the reason.

### IN-03: Two examples have preconditions that cannot occur or are incomplete

**File:** `docs/method/GG-SAD_normative_method_specification.md:3534-3540` (AE-154), `:3719-3725` (AE-102)
**Issue:** AE-154 starts from an `active` `core` change "whose record holds no base revision". `start` never succeeds without recording one (2333, 3464), and the state cannot be hand-edited, so the setup is unreachable. AE-102 requests `close` three times with an override of two attempts, and says the first two evaluations are "not paused". Nothing in the Given makes the first two `close` calls not close the change, so an unmet done gate is implied but not stated.
**Fix:** For AE-154, state the cause (for example a migrated legacy state) or move it to `full`. For AE-102, add "and a done gate that stays unsatisfied".

### IN-04: An example asserts a SHOULD as a certain outcome

**File:** `docs/method/GG-SAD_normative_method_specification.md:3999`, `:4027-4033` (AE-161)
**Issue:** 3999 says an implementation "SHOULD warn" when the interpreter lives inside the repository. AE-161 says "the implementation warns" as the Then. A SHOULD with accepted deviations is tested as a MUST.
**Fix:** Change 3999 to MUST, or word the example as "an implementation that follows this recommendation warns".

### IN-05: 25.2 mentions a "timestamp" for a YAML 1.2 core schema that has no timestamp type

**File:** `docs/method/GG-SAD_normative_method_specification.md:4225`
**Issue:** The text lists "a timestamp" among the values outside the domain, but a YAML 1.2 core-schema parser reads an unquoted date as a string, so the case never arises. The list implies a type resolution that the stated schema does not perform. The registered deferral on the text/binary rule (DC register) covers the classification only.
**Fix:** Delete "a timestamp" or say "a scalar that a parser reads as a timestamp (which the core schema does not)".

### IN-06: 12.1 lists "retry limits" among the conditions that terminate the flow, while a retry limit is soft

**File:** `docs/method/GG-SAD_normative_method_specification.md:1398`, `:1404`, `:1386-1388`
**Issue:** The typical fail categories (obligation to terminate) include "exceeding hard budget, cost, or retry limits". 1404 says a retry limit is a soft fail condition that pauses the flow, and 1388 limits the obligation to terminate to hard conditions.
**Fix:** Reword the category to "exceeding a hard budget or cost limit" and note retry limits as soft.

### IN-07: The `core` document tree differs between 4.3 and 23.1

**File:** `docs/method/GG-SAD_normative_method_specification.md:309-314` against `:2175-2180`, `:317-319`
**Issue:** The 4.3 tree for a `core` change lists `review.md`. 23.1 says "a `core` change consists of three documents ... (Section 4.3)" and shows a three-file tree. 4.3 explains that `review.md` is conditional, but the sentence at 319 ("`plan.md`, `tasks.md`, `evidence.md`, and `review.md` remain conditional files") follows the `core` tree and reads as if `core` may also have `plan.md`, `tasks.md`, and `evidence.md`. Those files are measured by the scope check if present.
**Fix:** Say in 319 that the sentence is about `full`, and mark `review.md` in both `core` trees consistently.

### IN-08: The 4.2 exception is recorded in a document that is conditional and produced late

**File:** `docs/method/GG-SAD_normative_method_specification.md:281`, `:319`, `:458-464` (AE-227)
**Issue:** The approved exception to a project-wide definition is "recorded in the Deviations of the evidence of the change (Section 16.4)". The 5.3 check runs "when the change is created, and again before the gate definitions of the change are approved", and AE-227 checks before approval. `evidence.md` is a conditional file normally written during verify. At the time of the check it may not exist.
**Fix:** Name an earlier home (a section in `spec.md` that is part of the hashed gate definitions) and keep the Deviations entry as the later record.

### IN-09: The wait-state JSON templates have inconsistent field names and a non-canonical phase id

**File:** `docs/method/GG-SAD_normative_method_specification.md:1345-1355`, `:1334-1341`, `:809-817`, `:4080`, `:1365` (AE-268)
**Issue:** 11.2 lists six mandatory items, including "outstanding information or decision", but the template has no field for it (`waiting_for` holds the responsible party). The 8.1 template names the responsible party `owner`. 25.1 says the `wait` object holds "the wait content of Section 11.2 and the other metadata of Section 8.1", so the same party is `owner` or `waiting_for`. The template's `"resume_at": "planning"` is not one of the canonical phase ids of Section 7 (`plan`). AE-268 treats all six items as mandatory.
**Fix:** Align the field names (`owner` throughout, add `outstanding`), and use `"resume_at": "plan"`.

### IN-10: The 24.3 statement rationale is off by one

**File:** `docs/method/GG-SAD_normative_method_specification.md:3229`, `:3287-3289` (AE-129)
**Issue:** The `version` field is "the number of entries that the history of the change holds when the statement is built ..., so that the statement names the position in the history at which the action will be recorded". With N entries, the action is recorded at position N+1. AE-129 and the optimistic lock in 25.1 both use N. The explanatory clause is wrong, and an implementer who follows the clause instead of the definition produces signatures that other verifiers reject.
**Fix:** Replace the clause with "so that the statement names the history that the action extends".

### IN-11: The relation of `docs/definitions/` to `core` is not stated

**File:** `docs/method/GG-SAD_normative_method_specification.md:277-281`, `:541`, `:2200`
**Issue:** 4.2 applies to both profiles and says local specifications MUST NOT weaken the project-wide standard gates. A `core` change has no DoR or DoD (2200). The text does not say whether the project-wide definition files bind a `core` change, and 281 says "a `core` change has no such exception", which implies they do.
**Fix:** State whether `docs/definitions/` is in force for `core`, and if so how.

### IN-12: The `gate-weakened` issue code is defined for `core` only

**File:** `docs/method/GG-SAD_normative_method_specification.md:384`, `:458-464` (AE-227)
**Issue:** The result and issue code are specified for `core`. For `full`, 384 says only that an entry that weakens "is a weakening", and AE-227 says "rejected as weakening".
**Fix:** Name the code `gate-weakened` and the result `rejected` for `full` as well.

### IN-13: The content of an evaluator-created wait record is not specified

**File:** `docs/method/GG-SAD_normative_method_specification.md:2669-2685`, `:2334`
**Issue:** A wait record "contains" `kind`, `reason`, `owner`, `resume_when`. The `wait` action requires owner, reason, and resume condition from the caller. Records of kind `fail-gate` and `external` are created by the evaluation, and the text does not say what `owner` and `resume_when` hold for them, or who may `resume` them.
**Fix:** Give the values, for example `owner` is the change owner, `resume_when` is "override recorded" or "gate `<id>` can be evaluated", and `reason` names the gate and cause.

### IN-14: 24.9 removes evidence-depth tailoring that 3.7 and 5.2 allow

**File:** `docs/method/GG-SAD_normative_method_specification.md:124`, `:342-359`, `:3913-3925`, `:3969-3975` (AE-168)
**Issue:** 3.7 lets tailoring change "evidence depth" and keeps "evidence appropriate to the selected compliance profile" as invariant. 5.2 lets a compliance profile tailor evidence retention and provenance. 24.9 requires, for both profiles and every compliance profile, an executable command for every requirement, and says a requirement whose only evidence is a review or a screenshot "has no evidence command". Requirements that cannot be run (visual or process requirements) can never reach complete evidence, even under `lean`.
**Fix:** State in 3.7 that executable evidence is part of the invariant core, and say how a non-executable requirement is dispositioned, for example an approved alternative acceptance condition.

---

_Reviewed: 2026-10-24_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
