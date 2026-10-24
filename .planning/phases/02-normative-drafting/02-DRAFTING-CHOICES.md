# Phase 2 drafting choices register

Input for the Phase 3 packet. This register consolidates every drafting choice of plans 01 to 05 for the proposed text of `docs/method/GG-SAD_normative_method_specification.md`. Each entry states the reading that the drafter took where the owner decisions leave room, so that the owner can overrule it. Nothing in this register is an owner decision, an approval, or a review result. The method version in the header of the text is 1.4 (see "Version note").

The ids DC-01 to DC-27 come from the research register. The ids DC-28 onward were assigned while drafting: DC-28 to DC-39 in plan 01, DC-40 to DC-58 in plan 02, DC-59 to DC-79 in plan 03, DC-80 to DC-95 in plan 04, and DC-96 to DC-107 in plan 05.

## Drafting choices DC-01 to DC-27 (research register)

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-01 | all | 1.1 | No renumbering. Sections 5.6, 23, 24, and 25 are added; map rows 23 and 24 are in the category Method Semantics and row 25 in Reference-Implementation Requirements. |
| DC-02 | SPEC-12, SPEC-17 | 23.4 | In `core`, `supersede` closes the change as `cancelled` with a required `replaced_by` that names a different existing change. |
| DC-03 | SPEC-01 | 24.1 | "Cancellation" includes `supersede`. The re-approval itself is exempt. A read-only report answers `rejected` with `changed` false and says that the gates are not enforced. |
| DC-04 | SPEC-02 | 24.2 | `not_applicable` stays the marker for a gate that is not evaluated by design. `not_evaluable` is a separate result and is never recorded as `not_applicable`. |
| DC-05 | SPEC-03 | 22.2 | `blocked` means: valid operation, evaluation recorded, transition did not occur. Only `close` and `resume` (`core`) and `complete` and `resume` (`full`) answer it. |
| DC-06 | SPEC-14 | 24 intro | The frozen set of a `full` change is the change specification with its Flow Gates, its allowed path list, and the project-wide definitions in effect at the approval, identified by content hash (completed by DC-101). |
| DC-07 | SPEC-15, SPEC-14 | 4.3, 25.1 | `core` keeps `state.json` always. `full` keeps the optional-state allowance of 4.3; the rules that read or write the history are enforced mechanically only for a change that has a state document, and an implementation does not report them as enforced for an inline record. |
| DC-08 | SPEC-09 | 24.8, 9.5, 10.4 | Acceptance of an open question is an answer. The Open Questions section of 16.1 is a view; the recorded state governs. |
| DC-09 | SPEC-12 | 23.5 | The `core` wait record is its own (kind, reason, owner, resume condition, optional expiry, optional question), with no safe state and no next action. A table maps the four kinds to wait categories. |
| DC-10 | SPEC-14 | examples | Examples for the rules of both profiles; ids unique and cited, consecutive, not necessarily in document order. Plan 05 adds one example per rule unit (DC-104). |
| DC-11 | SPEC-04, SPEC-05 | 24.3, 24.4 | No assurance floor is assigned per compliance profile. "High assurance" means that the applicable configuration requires approvals at A2. |
| DC-12 | SPEC-16 | 23.7, 5.3 | The base gate set belongs to the method profile: for `core`, the scope violation gate (fail, hard), the unanswered question gate (wait), the stale specification approval gate (wait), and the incomplete evidence gate (done). Present on every change, not removable, not alterable by a lower layer. Identifiers added by DC-96. |
| DC-13 | SPEC-16 | 5.3, 4.2 | Weakening is absolute. The word "silently" is dropped from the rule. The exception of 4.2 is limited to the local specification of a `full` change (DC-98). |
| DC-14 | SPEC-15 | 25.1 | Canonical form restricted to strings, integers, booleans, null, arrays, and objects with string keys; keys in code point order; no whitespace; UTF-8 without BOM and final line feed; no ASCII escaping; `sha256:` prefix with 64 lowercase digits. No floating point. |
| DC-15 | SPEC-18 | 25.3 | An artifact is a machine-readable, schema-governed file (project configuration, integration mappings, change definition, state document). Markdown is out. A migration appends and never rewrites. |
| DC-16 | SPEC-15 | 25.2 | Text files normalize line endings, binary files are byte-exact; the classification rule is left to the implementation with a SHOULD default (valid UTF-8 and no zero byte). |
| DC-17 | all | text | The specification cites no decision, requirement, prototype, or finding id; check X1 passes. The Revision line names no requirement id. |
| DC-18 | SPEC-10 | 24.9 | An executable check bound to each requirement is required for complete evidence; the records of 15 supplement it. |
| DC-19 | SPEC-08 | 24.7 | An override gives an integer N of at least 1; the text states no default; any other value is rejected. |
| DC-20 | header | header | Version and Revision are edited in the last commit that touches the text, with a subject that names no requirement id (see "Commit structure"). |
| DC-21 | SPEC-06, SPEC-14 | 24.5, 16.1 | A `full` change gets a machine-checkable allowed path list in the Scope of the change specification (DC-102). Scope is measured against "the revision the change started from". |
| DC-22 | SPEC-12, SPEC-14 | 4.1, 6 to 10, 21 | The marker sentence "This section specifies the `full` method profile (Section 5.6)." heads 4.1, 6, 7, 8, 9, and 10, with a caption under the diagram of 21 and the statement in 5.6. |
| DC-23 | SPEC-02, SPEC-07 | 24.2 | The check-command gate is defined in 24.2: command as an argument list, an exit map, an unmapped exit status is `not_evaluable`. |
| DC-24 | SPEC-03, SPEC-12 | 22.2, 23.2 | `core` records `state` and `outcome`; `full` records `phase` and `status`; the `state` field of the envelope is worded per method profile. |
| DC-25 | SPEC-03, SPEC-18 | 22.1 | Section 22.1 gains "record a human decision" and `migrate`, each inserted before the last list item so that no existing list line is rewritten. |
| DC-26 | SPEC-12 | 5.6, 16.5 | The method profile is chosen per change at creation; project configuration MAY name a default; the project brief template gains `## Method Profile` with the values `core | full`. |
| DC-27 | SPEC-12 | 5.6 | Default applicability: both method profiles unless a section is listed as `full` only (4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 11.1, 16.1 to 16.4, the diagram of 21). Sections 23 to 25 state their own applicability. |

## Drafting choices DC-28 to DC-95 (plans 01 to 04)

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-28 | SPEC-12 | 5.6 | The mixed sections 11.2 and 12.2 apply to both method profiles except the safe current state and next action of a wait state (11.2) and the final status code of a fail rule (12.2), which are `full` only. |
| DC-29 | SPEC-12 | 5.6 | Creation with no method profile and no project default is rejected; `core` and `full` are exact lowercase identifiers and any other value is rejected. |
| DC-30 | SPEC-12 | 5.6 | The reference implementation does not implement `full` and MUST reject the creation of a change that selects it; the marking does not weaken any `full` rule. |
| DC-31 | SPEC-12 | 23.1 | Directory `specs/<change-id>/` with `change.yaml`, `spec.md`, `state.json`; fields `id`, `method_profile`, `compliance_profile`, `author`, `owner`, `goal`, `scope.allow`, `requirements`, `gates`, optional `follows`. |
| DC-32 | SPEC-12 | 23.1 | `follows` MUST name an existing change that is `closed`; the field is a reference and never changes the named change. |
| DC-33 | SPEC-12 | 23.3 | Fail and wait gates are predicate gates; an active wait gate blocks start, resume, and close without creating a wait record; done gate kinds are `check`, `review`, `sign-off`; gate identifiers are unique including base gates. |
| DC-34 | SPEC-12 | 23.4 | Transition table readings: `approve` and `answer` from every state except `closed`; `ask` from `open` and `active`; `fail` only from `waiting` with a `fail-gate` record; `adopt` from any state while the history has no anchor; read-only actions `check`, `review`, `guard`. |
| DC-35 | SPEC-12 | 23.6 | Evaluation order: active hard fail, a gate that could not be evaluated, active soft fail, active wait gate, then for `close` only an unsatisfied done gate. |
| DC-36 | SPEC-12 | 23.4 | An action from a state outside its Legal From cell is rejected; the choice between `rejected` and `blocked` for an unmet precondition is settled in 22.2 and the per-action tables. |
| DC-37 | SPEC-12 | 23.5 | Resume conditions by kind: `question` when answered; `fail-gate` when a human recorded an override; `external` when the gate can be evaluated again; `manual` when the owner of the wait states that the condition holds. An overdue wait stays a wait. |
| DC-38 | SPEC-12 | 3.7, 5.1, 5.2, 14.1 | Seven bare uses of "profile" became "compliance profile"; the four rows of the 5.1 table are byte-identical; "the `lean` profile" mentions and the heading of 5.3 are left as they are. |
| DC-39 | SPEC-12 | examples | Example ids are not in document order (AE-59 sits in 23.1). |
| DC-40 | SPEC-02 | 24.2 | Result names `satisfied`, `not_satisfied`, `not_evaluable` (exact lowercase); a done gate is met, and a fail or wait gate is active, when the result is `satisfied`. |
| DC-41 | SPEC-02 | 24 intro | Identifiers, path patterns, paths, and text values compare as sequences of Unicode code points without normalization; a rule MAY state otherwise. |
| DC-42 | SPEC-01 | 24.1 | The identity of the frozen definitions is the content hash of the parsed gate definitions; comments, layout, key order, and quoting do not change it; list order does. |
| DC-43 | SPEC-01 | 24.1 | The stable issue codes `gates-changed` and `start-blocked` are named in the text. |
| DC-44 | SPEC-01 | 24.1 | Every state-changing operation except `cancel`, `supersede`, and the approval that replaces the approved hash is rejected while the hashes differ (including `approve` of another target, `fail`, `adopt`, `ask`, `answer`). The re-approval is an amendment naming both hashes. |
| DC-45 | SPEC-02 | 24.2 | A check-command gate declares a command (argument list) and an exit map; there is no default map; a time limit and an extraction rule are optional. |
| DC-46 | SPEC-02 | 24.2 | Output never changes the result the exit map decides, except for the baseline comparison of 24.6; empty output never makes a gate `satisfied`. |
| DC-47 | SPEC-02 | 24.2 | A retry limit counts `not_satisfied` over the whole life of the change, never reset; reached when count is at least limit; a limit of 0 is reached at once; `not_evaluable` neither adds nor resets. |
| DC-48 | SPEC-02 | 24.2, 23.4 | `start` is rejected, creating no wait, when a gate cannot be evaluated or a fail or wait gate would decide; `resume` replaces the earlier wait record with a record of kind `external`; read-only actions create no wait. |
| DC-49 | SPEC-08 | 24.7 | An action that closes the change as failed because of a hard failure answers `success`. |
| DC-50 | SPEC-07 | 24.6 | Baseline entries form a set; the record names up to three new failures in ascending code point order plus the count; an empty baseline is valid; a baseline on a gate that is not a check-command gate is invalid. |
| DC-51 | SPEC-08 | 24.7 | A retry limit is a soft fail condition; a retry limit that declares `hard` is invalid. Severity values are exact lowercase. |
| DC-52 | SPEC-08 | 24.7 | An override names the soft fail condition it covers; an attempt is an evaluation by `close` or `complete` made while the override is in force; the N-th attempt is allowed and the next evaluation pauses again. |
| DC-53 | SPEC-08 | 24.7 | In `full`, the wait caused by a soft failure is category `WAIT_DECISION` with the resume condition "a human has recorded an override"; `fail` is the other disposition. |
| DC-54 | SPEC-03 | 8.3, 23.4 | Per-action results: `resume` is rejected while the resume condition is not satisfied and blocked while a gate keeps the change waiting; `start` with an unmet gate is rejected in both profiles; `reopen` is never blocked; a `complete` that preserves the phase with status `done` answers `success`. |
| DC-55 | SPEC-08, SPEC-03 | 12.2, 16.4, 20 | The 12.2 template gains a `Severity` line, the 16.4 template a line for gates that could not be evaluated, and section 20 the condition "no soft failure awaits a human disposition". The 8.3 cell of `complete` no longer lists DoF among the causes of rejection. |
| DC-56 | SPEC-03 | 8.3 | In `full`, `start` of a phase with an unevaluable gate follows the `core` reading (rejected, no wait); only `complete` and `resume` create the `external` wait. |
| DC-57 | SPEC-02, SPEC-12 | 24 intro | The term table defines the base revision in `core` as the revision recorded when `start` succeeds and in `full` as the revision recorded when the change starts; a `---` separator precedes the heading of section 24. |
| DC-58 | SPEC-02 | examples | Example ids AE-60 to AE-124 are consecutive but not in document order. |
| DC-59 | SPEC-04 | 24.3 | Level names are the exact strings `A0`, `A1`, `A2`. A1 is a platform review of the checked-out revision; the specification names no platform. |
| DC-60 | SPEC-04 | 24.3 | The required level of an action is the higher of the gate minimum and the project configuration minimum for the kind of action; an unstated minimum is A0. |
| DC-61 | SPEC-04 | 24.3 | Human-only actions are every approval, sign-off, override, an answer to a question with a human owner, `cancel`, `supersede`, `fail`, `adopt` (`supersede` is added to the list the plan named, because 23.4 already requires a human). The identity of a human carries the prefix `human:`. |
| DC-62 | SPEC-04 | 24.3 | The statement is built by the implementation: a first line with a format identifier and version, then operation, change, version (history position), identity, and details sorted by name; values JSON-encoded; the signed bytes are the UTF-8 lines ended by line feeds. |
| DC-63 | SPEC-04 | 24.3 | An approval binds the content hash of the specification, of the gate definitions, or of the gate definitions plus the gate or fail condition identifier. The specification approval is stale while the current hash differs. |
| DC-64 | SPEC-04 | 24.3 | An implementation that creates signatures SHOULD refuse an unprotected private key unless a human allows it; a participant who can write the signers file can list its own key (stated plainly). |
| DC-65 | SPEC-05 | 24.4 | An anchor or an equivalent is required only where the configuration requires approvals at A2; an equivalent is defined by properties; the anchor is kept outside the working tree and outside the history. |
| DC-66 | SPEC-05 | 24.4 | `adopt` is rejected when the history is not consistent, in addition to the 23.4 precondition that no anchor exists, and needs a human at the level 24.3 requires. |
| DC-67 | SPEC-05 | 24.4 | Entry fields `n`, `prev`, `body`, `hash`; the first `prev` is `sha256:` plus 64 zero digits; the entry hash is over the canonical form of `prev` and `body`; a history without an entry is not consistent. |
| DC-68 | SPEC-06 | 24.5 | In `full` the allowed path list is a list of path patterns stated in the Scope of the change specification; a change that states none has a scope that cannot be measured (`not_evaluable`). |
| DC-69 | SPEC-06 | 24.5 | Path patterns: relative to the repository root with `/`; no wildcard names one path; a trailing `/` names a tree; `*` stays inside one segment; a segment `**` matches any number of segments; an empty pattern, a leading `/`, or a segment `..` is invalid. Drafted conservatively; flagged as F1. |
| DC-70 | SPEC-06 | 24.5 | In `full` the base revision is recorded when the first phase of the change begins. |
| DC-71 | SPEC-06 | 24.5 | The exempt record files are the change definition, the specification, and the state document in `core`, and the specification and the state file or inline record in `full`; every other file in the change directory is measured. |
| DC-72 | SPEC-06 | 24.5 | Before start the scope gate is recorded `not_applicable`; after start a scope that cannot be measured is `not_evaluable`, never `satisfied` and never a violation. |
| DC-73 | SPEC-06 | 24.5 | A change MUST run isolated; an implementation SHOULD warn when it finds other uncommitted work at start and MUST NOT exclude such work from the measurement. |
| DC-74 | SPEC-11 | 24.10 | The designated token is the literal `@interpreter`; the interpreter is never discovered; with no configuration it is the implementation's own interpreter; a warning is advised when it lives inside the repository. |
| DC-75 | SPEC-10 | 24.9 | An evidence command is a check command of 24.2; closure is `close` in `core` and the evaluation of Verify-Done and the completion criteria in `full`. |
| DC-76 | SPEC-10 | 24.9, 24.1 | The requirement identifiers and the evidence commands are fixed with the gate definitions. |
| DC-77 | SPEC-09 | 24.8 | A question id is `Q` plus a decimal number from 1 assigned by the implementation; structured options are pairwise distinct; an empty free-text answer is rejected; an answer does not resume a waiting change. |
| DC-78 | SPEC-09 | 24.8 | In `full` a question is recorded in the state file or inline record; an unanswered question makes a Definition of Wait condition active, so `complete` and `resume` answer `blocked`. |
| DC-79 | SPEC-09 | 24.8 | The issue code `open-questions` is named in the text. |
| DC-80 | SPEC-12, SPEC-15 | 4.3 | The `core` layout of 4.3 shows `change.yaml`, `spec.md`, `state.json`, and a conditional `review.md`; review files are measured by the scope check like any other non-record file. |
| DC-81 | SPEC-15 | 25.1 | All ten body fields are always present and a field that does not apply is `null`; `at` is a UTC string `YYYY-MM-DDThh:mm:ssZ`; `result` is `success` or `blocked`; a rejected or failed action writes no entry. |
| DC-82 | SPEC-15 | 25.1 | The `after` record is the whole state and holds `schema_version`; the field is `base_revision`; in `full` it holds `phase` and `status` in place of `state` and `outcome`. |
| DC-83 | SPEC-15 | 25.1 | Integers are decimal, without fraction or exponent, with a magnitude not above 2 to the power 53 minus 1; a string holds no surrogate code point; a value outside the domain ends with `error` and writes nothing. |
| DC-84 | SPEC-15 | 25.1 | The expected version is the number of entries read; the writer locks, compares under the lock, and on a difference answers `error` with `state-conflict`; atomic replacement through a temporary file in the same directory. |
| DC-85 | SPEC-15 | 25.2 | A parsed YAML definition is read as YAML 1.2 with the core schema, aliases expanded; a float, a timestamp, a non-string key, a repeated key, or an integer above the bound has no content hash. |
| DC-86 | SPEC-15 | 25.2 | The content hash of a file set is the hash of the canonical form of an object from path to file hash; the hash of gate definitions together with a gate identifier uses the members `definitions` and `gate`. |
| DC-87 | SPEC-18 | 25.3 | The version is a string of two integers joined by a dot, compared one integer at a time; a number is not a version. |
| DC-88 | SPEC-18 | 25.3 | Three stable issue codes: `migration-required`, `schema-version-unsupported`, `schema-version-mismatch`; every operation that uses the file is refused, read-only ones included; only `migrate` accepts a migratable version. |
| DC-89 | SPEC-18 | 25.3 | `migrate` applies steps in ascending order, one entry per step, all or nothing; it is a contract operation, legal from every state, and changes neither state nor outcome. |
| DC-90 | SPEC-18 | 25.3 | The migration entry adds `source_version`, `target_version`, and `source_hash`. |
| DC-91 | SPEC-18 | 25.3 | The document version must equal `after.schema_version` of the last entry; a difference makes the history not consistent and is refused with `schema-version-mismatch`. |
| DC-92 | SPEC-18 | 25.3 | A project-level artifact is migrated inside a change that is not `closed`; a migration of a change definition that alters the parsed gate definitions needs a new human approval. |
| DC-93 | SPEC-18 | 25.3 | An old `state.yaml` is converted by `migrate` to `state.json` whose first entry is a `migrate` entry; the old file is not changed, deleted, or read afterwards; the hash chain restarts at that entry (an anchor makes the restart detectable). |
| DC-94 | SPEC-17 | 8.3, 8.4 | `reopen` is marked `full` only; in `core` a closed change is final; `follows` is a reference and a new change naming a change that is not closed is rejected. |
| DC-95 | SPEC-15 | 25.1 | The text carries two real SHA-256 test vectors (AE-183, AE-184); they are not development identifiers. |

## Drafting choices DC-96 to DC-107 (plan 05)

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-96 | SPEC-16 | 5.3, 23.7 | The four base gates of `core` have the identifiers `scope-violation`, `unanswered-question`, `stale-spec-approval`, and `incomplete-evidence`. A change definition that redefines one of them or states that it does not apply is rejected at creation and again before the approval of the gate definitions; the stable issue code is `gate-weakened` when the listed gate differs in kind, condition, or severity or the gate is stated not to apply, and a listed gate that does not differ is rejected as a duplicate identifier (23.3). |
| DC-97 | SPEC-16 | 5.3 | Weakening is: remove a gate (state that it does not apply, or leave it out of a definition that replaces the gates of the higher layer), alter its condition (including kind and every declaration 24.1 fixes), lower its severity, lower the assurance level it requires. Strengthening is adding a gate with an identifier of its own or raising a level in the project configuration. A lower layer that states a lower assurance level than a higher layer requires does not lower it (the higher level is required, 24.3); the statement is accepted and has no effect, consistent with the example of 24.3 on the gate minimum. The result does not depend on the order of listing. |
| DC-98 | SPEC-16 | 4.2, 5.3 | The approved exception of 4.2 exists only for the local specification of a `full` change that departs from a project-wide definition. A human approves it at the level 24.3 sets for the approval of gate definitions; it applies to that change only; it is recorded in the Deviations of the evidence (16.4); it never reaches the invariant core, the protections of section 24, or the base gates; a `core` change has none. It is a recorded human decision and not a weakening by a lower layer. The existing 4.2 sentence is not rewritten; a paragraph is added after it. For the owner to overrule (research OQ-2). |
| DC-99 | SPEC-16 | 5.3, 3.8 | A `core` change implements layers 1, 2, 3, and 5. Layer 4 (change-class requirements, the size classes of 6) and layer 6 (integration mappings, 3.8 and 17) are not applicable to `core` and are specified for `full` and combination use. No seventh layer; layers are never renumbered. |
| DC-100 | SPEC-16 | 5.3 | For a `full` change the no-weakening check compares the Flow Gates with the project-wide definitions of 4.2; an entry that removes or relaxes a condition is a weakening unless the approved exception covers it. |
| DC-101 | SPEC-14 | 24 intro | The definitions fixed in `full` are the Flow Gates, the allowed path list, and the project-wide definitions under `docs/definitions/` in effect at the approval. The parsed value is an object with `flow_gates` (lists `ready`, `done`, `wait`, `fail` of condition texts in written order; the text of a condition is the list item without its marker, white space runs replaced by one space; the marker `<optional>` is not a condition; a heading without items gives an empty list), `scope` (the allowed path list), and `definitions` (the content hash of the file set under `docs/definitions/`). A change of a project-wide definition after the approval makes the gate definitions differ from the approved ones. This completes the item that plan 04 handed over. |
| DC-102 | SPEC-14 | 16.1 | The 16.1 template gains the heading `### Allowed Paths` with the line `- <path pattern>` in the Scope, and one paragraph says that this list is the allowed path list and that Included and Excluded describe the scope in words and are not measured. |
| DC-103 | SPEC-14 | 24 intro | The realization table has 11 rows (24.1 to 24.10 and the result `blocked`) with the columns Protection, Section, In `core`, In `full`. The `full` cells are argued from the generic wording of the `full` flow (Flow Gates, DoR, DoD, DoW, DoF, wait categories, state file or inline record) and have no prototype evidence. |
| DC-104 | SPEC-14 | examples | The rule unit is as in the owner's granularity rule: 30 rule units (4.1, 5.5, 6.1 to 6.3, the four flows of 7.1, 8.2, the eight actions of 8.3, 8.4, 8.5, the eight pairs 9.k with 10.k, and the `full`-only parts of 11.2 and 12.2) plus the 11 realizations, 41 units. Each unit has one example block that shows a normal and a failure or boundary case. Unit 8.4 has two blocks, because the example of `reopen` already existed. The examples AE-218 to AE-228 belong to 5.3 and AE-229 to AE-269 to the 41 units. The pair examples sit after each Definition of Done and are cited from both 9.k and 10.k. |
| DC-105 | SPEC-16 | 23.4 | A stray comma before "An `answer`" in the paragraph after the 23.4 table (text of plan 02) became a full stop. This is the only edit of an existing line outside 5.3 in this plan; it changes no rule. |
| DC-106 | header | header | Version 1.4 (owner's number from the planning record; the packet states it so the owner can change it). The Revision line is dated 2026-10-24, the day of drafting, followed by an em dash and one sentence that names the amendment (method profiles, shared protections, JSON state, schema versions) and no id. |
| DC-107 | SPEC-14 | 24 intro | The 11 realization examples sit after the realization table in the section 24 intro, not at the end of each subsection 24.k, and are cited from one paragraph there. |

## Dispositions of the open questions OQ-1 to OQ-7

| ID | Question | Disposition in the draft |
|---|---|---|
| OQ-1 | Assurance floors and base gates per compliance profile | The draft assigns none (DC-11). Base gates belong to the method profile (DC-12, DC-96). The example of 24.3 shows that a compliance profile alone sets no minimum level. |
| OQ-2 | May an approved exception weaken a higher layer | The draft is absolute (DC-13, DC-97). The one exception left is the exception of 4.2, limited to the local specification of a `full` change (DC-98). |
| OQ-3 | Granularity of "each `full` rule has an acceptance example" | Settled by the owner's granularity rule: the rule unit; 41 units here (DC-104). |
| OQ-4 | `state.json` for `full` | Drafting choice DC-07: always for `core`; `full` keeps the optional-state allowance, with mechanical enforcement only where a state document exists. |
| OQ-5 | Cite the decision record in the text | The text cites none; check X1 passes (DC-17). |
| OQ-6 | `core` `supersede` | Closes as `cancelled` with `replaced_by` (DC-02). |
| OQ-7 | Items no requirement owns: exit codes and the text-versus-binary rule | Exit codes: no requirement owns them and none were added; handed to the engine phases with the list of stable issue codes. The text-versus-binary rule: 25.2 states the constraint (depends on the bytes only) and a SHOULD default; the concrete rule goes to the engine phases. |

## Flagged edge and prohibition items

Probe items 50 equal 43 authored (tagged in plans 01 to 05) plus 7 flagged. The seven flagged items are listed for the owner. No text, example, or check was written for them.

| Flag | Item | Requirement | Note |
|---|---|---|---|
| F1 | E18 encoding | 06 (scope) | Path case and normalization are platform dependent. The text compares paths as code point sequences without normalization and letter case matters (24, 24.5); on a file system that folds case or normalizes names, a changed path can match differently. The path pattern syntax (DC-69) is drafted, not exercised. |
| F2 | E36 precision | 12 (profiles) | The profile identifiers carry no quantity beyond counts, so no precision rule applies. |
| F3 | E42 adjacency | 14 (`full` revision) | Recorded as flagged in the accounting of plan 05; no rule or example was authored for it. |
| F4 | E44 ordering | 14 (`full` revision) | No defensible document criterion for an order of the rule units; the examples are not ordered by any criterion except the document order of their rules. |
| F5 | E45 | 15 | Unclassified probe item, flagged. |
| F6 | E46 | 16 | Unclassified probe item, flagged. |
| F7 | E47 | 17 | Unclassified probe item, flagged. |

Prohibitions: six are kept after the precision pass, all authored descriptor-less in plan 01, and none is flagged. Scope-pattern injection and path traversal are canon from the secure-phase review and were not minted here; a pattern with an empty text, a leading `/`, or a segment `..` is invalid (DC-69).

## Unproven items

These rest on reasoning or on a single decision and no prototype or test exercised them. The independent review should look at each.

- SPEC-14, the `full` realizations: every row of the realization table and the 41 examples (DC-101, DC-103, DC-104). Specified, not implemented.
- SPEC-16, beyond the prototype's no-weakening check: the `full` side of the check (DC-100), the layer set of `core` (DC-99), and the exception of 4.2 (DC-98).
- SPEC-17: proved by absence only (a `core` change has no `reopen`).
- SPEC-18: decision-driven, no prototype evidence; the YAML-to-JSON conversion rule and the migration of a project-level artifact inside a change.
- The "or an equivalent" clause of the anchor rule in 24.4 (nothing exercised an equivalent mechanism).
- The A1 verifier of 24.3 (platform review is not tested directly and cannot serve a participant who works alone).
- The rule that a retry limit is a soft fail condition (reasoning).
- The path pattern syntax (F1 above).

## Version note

The header of the proposed text reads `Version: 1.4` and a Revision line dated 2026-10-24 (DC-106). The number is a drafting value so that it can be changed in one line. Version 1.3 stays pinned in three places that this phase does not touch (see the hand-off list).

## Hand-off list (engine phases 5 to 8)

Files and values that this phase does not change and that the engine phases must align with the proposed text once the text is in force:

- `specs/examples/class-m/state.yaml` (the example state; its `flow.profile` at line 10 is the compliance profile), `.ggsad/templates/*.template.md`, `.ggsad/schemas/state.schema.json`, and the archived CHG-001 state.
- The pinned method version "1.3" in `.ggsad/config.yaml` (line 10), `src/ggsad/application/initialize_project.py` (line 82), and `tests/unit/test_initialize_project.py` (line 61).
- The schema constants "0.1" in `.ggsad/schemas/config.schema.json` (line 20), `.ggsad/schemas/mappings.schema.json` (line 19), and `.ggsad/schemas/state.schema.json` (line 22). The text fixes the form of `schema_version` and the checks, not the version values; the version of the first JSON state document and the first migration step are engine choices.
- Exit codes (no requirement owns them): the mapping of the four results and of the stable issue codes (`gates-changed`, `start-blocked`, `open-questions`, `state-conflict`, `migration-required`, `schema-version-unsupported`, `schema-version-mismatch`, `gate-weakened`) to exit codes.
- The concrete text-versus-binary rule for content hashing (25.2 states the constraint and a SHOULD default only).
- Configuration keys that the text does not name: the minimum assurance levels, the interpreter, the platform account mapping, the signers file location, the anchor location, and the default method profile. Also the spelling of the statement format identifier, the signature scheme, and the storage of the anchor.
- The reference implementation refuses a change that selects `full`; the realizations in the table of the section 24 intro stay specified but not implemented.

## Commit structure

- Each requirement has its own commit or commits whose subject begins `docs(02-NN): SPEC-nn`. Several requirements have more than one commit because the parts are independent or because a part would otherwise have broken an additions-only check: SPEC-12 has three (5.6; section 23; applicability and markers), SPEC-14 has three (realization table; examples for sections 4 to 8 and the realizations; examples for the definitions of ready, done, wait, and fail), SPEC-18 has two (section 25.3; the `schema_version` field of the change definition). SPEC-15 has one: the reference-fix commit that plan 04 allowed for was not needed, because the reference check found nothing dangling.
- The header commit `docs(02-05): header Version 1.4 and revision line (D-12)` is the last commit that touches the text. It implements the version decision, so its subject names no requirement id; the check C1 accepts exactly that subject and counts it toward no id.
- SPEC-13 (nothing under `src/ggsad/` changes) has no commit: it is met by the checks S1 and S2 and by an empty diff under `src/ggsad/`, deliberately.
- Plan 02 rewrote local history once, before any push, to repair a gap in the example ids; the tree is the same as before the rewrite apart from that one example, and each requirement still has one commit.

## The mixed row of 11.2 and 12.2

The applicability table of 5.6 treats 11.2 and 12.2 as mixed: both method profiles, except the safe current state and next action of a wait state (11.2) and the final status code of a fail rule (12.2), which are `full` only (DC-28). Plan 05 gives each `full`-only part its own example (AE-268, AE-269).

## The exempt set of 24.1

The set of operations that the comparison of gate definitions does not stop is wider than the phrase "every operation except cancellation" in the success criterion: it holds `cancel`, `supersede` (which the move rule of 5.6 needs), and the re-approval of the gate definitions. The owner can overrule this (DC-03, DC-44).

## Verification record

The Python baseline is not run (no Python changed in this phase). The shell checks are the read-only script of this phase, run with `--final`; its output is quoted in the summary of plan 05 and in the identity note.
