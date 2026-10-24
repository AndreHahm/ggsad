---
phase: 02-normative-drafting
plan: 04
subsystem: normative-spec
tags: [state-json, canonical-form, content-hash, schema-version, migration, reopen, bash-check]
status: complete

requires:
  - phase: 02-normative-drafting
    provides: "Plans 01 to 03: method profiles, the core profile (23), section 24 (24.1 to 24.10), conventions K1 to K6, the check script with --ids, AE-01 to AE-182"
provides:
  - "Check script: R7 (the old state file name outside the migration rule of 25.3; a reopen in section 8 outside a unit that names the full profile) and R1 (section references resolve; heading numbers unique and contiguous); both warning only"
  - "Section 25 with map row 25: 25.1 State Document and Canonical Form, 25.2 Content Hash, 25.3 Schema Versions and Migration"
  - "Section 4.3 names state.json and shows the core layout beside the full layout; the blocks of 8.1 and 11.2 are JSON with unchanged key spellings"
  - "migrate in 22.1, the refusal of an unusable schema version in 22.2, schema_version among the fields of the change definition in 23.1"
  - "reopen marked full only in 8.3, 8.4 and the closed-change sentence; the core absence, the final-closed rule and the follows rule in 23.4"
  - "Acceptance examples AE-183 to AE-217"
affects: [02-05 full revision and resolution, Phase 3 owner approval, engine phases]

actuals:
  tokens: 11600
  tasks: 3
  commits: 6

tech-stack:
  added: []
  patterns: ["rule paragraph ends 'See AE-nn.'", "test vectors computed with an independent tool before they were written into the text", "additions-only commit for the migration rules; edits of existing lines only where the plan says replace"]

key-files:
  created: []
  modified:
    - docs/method/GG-SAD_normative_method_specification.md
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh

key-decisions:
  - "No owner decision was made. Judgment calls are listed under Drafting choices for the Phase 3 packet."

patterns-established:
  - "Quick check before every specification commit; each commit stages the specification only; C1 run with the ids done so far."

requirements-completed: [SPEC-15, SPEC-18, SPEC-17]  # drafted as proposed text; SPEC-13 stays open: it is checked in every plan and closes with the phase.

duration: "about 1 hour"
completed: 2026-10-24
---

# Phase 2 Plan 04: State and Versioning Summary

**Proposed text for SPEC-15, SPEC-18 and SPEC-17: a JSON state document with a defined canonical form (keys by code point, UTF-8, no ASCII escaping, a closed value domain), a `sha256:` hash string, a content hash for text, binary, parsed definitions and file sets, atomic replacement under a lock with an expected-version check, a `schema_version` rule with explicit recorded migration and downgrade detection, and `reopen` limited to the `full` method profile, backed by 35 acceptance examples and a check script that now resolves section references and watches the old state file name.**

## Accomplishments

- Check script: R7 warns on `state.yaml` anywhere outside Section 25.3 (a tree line of Section 4.3 gets its own message) and on a `reopen` in Section 8 that is not in a line, a paragraph, or a directly preceding bold caption line that names `full`. R1 resolves every `Section N`, `Sections N and M` and `Section N.M` reference (a list continues after a comma, "and", "or" or "to"), flags duplicate heading numbers, requires top-level numbers contiguous from 1 and subsection numbers contiguous within each section. Run on the untouched base (`--ref origin/main`) R1 prints PASS. Both are warnings in quick mode.
- Section 25.1: the state document `state.json` (fields `schema_version` and `entries`), the ten body fields (`action`, `actor`, `assurance`, `at`, `result`, `gate_results`, `gate_detail`, `files`, `note`, `after`), the `after` record per method profile, the file as a pretty-printed form that is not the hashed form, the value domain (strings, integers, booleans, null, arrays, objects; no floating point; integers up to 2 to the power 53 minus 1), the canonical form (no whitespace, keys in code point order, escapes only where JSON requires them, UTF-8 without BOM and final line feed), the code point comparison that Section 24 cites, the hash string and the first `prev`, atomic replacement through a temporary file, and a lock with an expected-version check whose conflict answers `error` with `state-conflict`. The rule applies to creation and to recorded evaluations in `core` and `full`. 14 examples including two verified test vectors.
- Section 25.2: the content hash of a text file (CR LF and lone CR become LF), of a binary file (byte-exact), the implementation's text-or-binary decision (a function of the bytes only, with a SHOULD default), of a parsed definition (YAML 1.2 core schema, canonical bytes of the parsed value, values outside the domain have no hash and the approval is rejected), of a file set, and of the gate definitions together with a gate identifier. 6 examples.
- Section 25.3: the version form (two integers joined by a dot, compared one integer at a time), the governed files, the check before use with three stable issue codes, the explicit `migrate` operation (ascending steps, each recorded, all or nothing), the migration entry that appends and never rewrites, the downgrade rule (document version equals the latest recorded one), migration of a project-level artifact inside a change, and conversion of an old YAML state document. 12 examples.
- Pointers: 22.1 (list item `migrate`, inserted before the last item), 22.2 (one paragraph with the three issue codes), 23.1 (bullet `schema_version` and the example AE-09), 4.3 (tree, sentence, core layout), 8.1 and 11.2 (JSON blocks and one pointer sentence each), 8.3, 8.4 and 23.4 for `reopen` and `follows`.
- Every forward reference of plans 01 to 03 to Sections 25.1 and 25.2 now resolves; R1 reports no unresolved reference in the whole text.

## Task Commits

1. Task 1 (tracer), script: `docs(02-04): extend normative diff check script (R7)`
2. Task 1 (tracer), SPEC-15: `docs(02-04): SPEC-15 specify state.json and its canonical form in section 25`
3. Task 2, SPEC-18: `docs(02-04): SPEC-18 require schema_version and explicit recorded migration in section 25.3`
4. Task 2, SPEC-18 (alignment): `docs(02-04): SPEC-18 add schema_version to the change definition fields`
5. Task 3, SPEC-17: `docs(02-04): SPEC-17 specify reopen for full only`
6. Task 3, script: `docs(02-04): extend normative diff check script (R1)`

The summary and planning-state commits follow. The tracer passed its own commands (`--ids SPEC-15` printed `FAIL C1` before the SPEC-15 commit and `RESULT: PASS` after), and the plan has no human checkpoint, so no stop was made at the tracer gate. No commit `docs(02-04): SPEC-15 resolve section references` was needed: R1 found nothing dangling.

## Verification

- `bash -n` exits 0; `shellcheck` exits 0 (run, no findings).
- Seeded defects on copies of the specification outside the repository (`--file`): the untouched current text of Section 4.3 and the unqualified `reopen` lines printed `WARN R7`; after they were qualified on a copy, R7 passed; a new line `reopen again` inside a Section 8 example paragraph printed `WARN R7`. For R1, an appended line citing Section 99, Sections 24.1, 24.2 and 26.4, and Section 25.9 to 25.3 printed three `WARN R1 ... does not resolve`; a heading renumbered 24.5 printed the duplicate, the dangling references and the missing 24.4; a second heading `## 24.` printed the duplicate and the missing top-level number 22. The first two seeded runs ended `RESULT: PASS`, because these checks are warnings in quick mode; the run with the renamed top-level heading also printed `FAIL R5` and `FAIL R6` (the map row and the base heading are gone), as it should.
- `--ids` before each specification commit printed `FAIL C1` for the id being drafted; after each commit it printed `RESULT: PASS`. The final run `--ids SPEC-04,SPEC-05,SPEC-06,SPEC-11,SPEC-10,SPEC-09,SPEC-15,SPEC-18,SPEC-17` printed `RESULT: PASS`, and so did `--ids SPEC-15,SPEC-18,SPEC-17`.
- Final quick run: B1 E1 E2 E3 S1 S2 N1 X1 R5 R6 R2 R3 R1 R7 all `PASS`; warnings: `WARN X1` (the word "prototypes" in existing text of section 5.1) and two `WARN R8` on the heading and map row "Protections Shared by Both Profiles" (fixed text from plan 02). `bash CHK | grep -c '^WARN R[17]'` is 0. R2 reports 217 example blocks, all cited, all with a unique id.
- JSON: the fences of 8.1 and 11.2 each parse with `json.loads` and keep their key spellings. `bash CHK --section 4.3` has 0 lines with the old state file name and 4 with `state.json`.
- Test vectors: the hash strings of `{}` and of `{"count":2,"name":"café"}` in AE-184 and AE-183 were computed with `sha256sum` and agree with an independent Python computation of the canonical form; the escape example AE-186 was checked the same way.
- Section checks: `--section 25.1` contains `sha256:`, `code point`, `UTF-8`, `compare`, `atomic`; `--section 25.2` contains `line ending` and `byte`; `--section 25.3` contains `schema_version`, `migrate`, `ascending`, `source content hash`, `rejected`, `MUST NOT rewrite`; `--section 22.1` contains `migrate`; `--section 22.2` mentions the three codes; `--section 8.3` has a line with "`full` only"; `--section 23.4` contains `follows`, `reopen`, `final`. The map row for section 25 occurs once.
- Example coverage: 14 blocks cover 25.1, 6 cover 25.2, 12 cover 25.3, 2 cover `follows` in 23.4 plus the existing AE-11, AE-12, AE-48, 1 covers `reopen` in 8.4. AE-183 to AE-217 are consecutive, defined once, and all cited.
- Additions only: the SPEC-15 commit removes only the lines the plan replaces (the old tree line, the optional-state sentence, and the two YAML fences); the SPEC-18 commit that adds 25.3 removes no line (`git show --format= HEAD -- docs/method/GG-SAD_normative_method_specification.md | grep -c '^-[^-]'` printed 0 right after it); the alignment commit changes one line (AE-09) and adds one bullet; the SPEC-17 commit rewrites the three lines the plan names.
- `grep -n '^### 2[345]\.'` lists 23.1 to 23.7, 24.1 to 24.10 and 25.1 to 25.3 in numeric order, contiguous.
- `git diff --name-only origin/main...HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; changed paths are the specification and `.planning/` only.
- Python baseline: not run (no Python changed).

## Deviations from Plan

**1. [Rule 2 - Missing critical functionality] `schema_version` was not a field of the change definition.**
- **Found during:** Task 2.
- **Issue:** The plan makes the change definition schema-governed, but the field list of 23.1 (MUST contain) and the example AE-09 did not name `schema_version`, so a definition that follows 23.1 would have been refused by 25.3.
- **Fix:** a bullet in the list of 23.1 and the same field in AE-09, in their own commit after the additions-only SPEC-18 commit, so that the additions-only acceptance check holds for the commit that adds 25.3.
- **Commit:** `docs(02-04): SPEC-18 add schema_version to the change definition fields`

**2. [Rule 2 - Missing critical functionality] The `after` record also holds `schema_version`.**
- **Found during:** Task 2.
- **Issue:** The plan lists the `after` fields without a version, but the downgrade rule needs a version recorded in the hash chain; a version only in the top-level field would not be tamper-evident.
- **Fix:** `after.schema_version` in both method profiles (25.1) and the rule in 25.3 that the document version equals it (DC-82, DC-93).
- **Commit:** the SPEC-15 and SPEC-18 commits.

**3. [Plan reading] R7 is stricter than the plan text.** The plan names a tree line of 4.3; R7 warns on the old state file name anywhere outside 25.3, which is how the plan words the allowance in task 2. The `reopen` rule accepts a bold caption line directly before a table, because the results table of 8.3 names the `full` profile only in its caption.

**4. [Plan reading] The core absence statement of 23.4 already existed from plan 01.** Task 3 added the missing pieces (the `follows` reference rule and the rejected cases) as a separate paragraph and did not rewrite the existing line.

Otherwise the plan was executed as written.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. DC-07, DC-14, DC-15, DC-16, DC-25 and OQ-4, OQ-6, OQ-7 are research ids; DC-80 onward are new in this plan (DC-28 to DC-39 are in plan 01, DC-40 to DC-58 in plan 02, DC-59 to DC-79 in plan 03).

- **DC-07:** `core` keeps `state.json` always. `full` keeps the optional-state allowance of 4.3, and the text states that the rules of 24.1, 24.3, 24.4 and 24.8 that read or write the history are enforced mechanically only for a change that has a state document; an implementation MUST NOT report them as enforced for an inline record (OQ-4, resolved this way).
- **DC-14:** The canonical form is restricted to strings, integers, booleans, null, arrays and objects with string keys; keys in code point order (not UTF-16 order); separators `,` and `:` without whitespace; UTF-8 without BOM and final line feed; no ASCII escaping; the `sha256:` prefix with 64 lowercase digits. Floating-point numbers are outside the domain.
- **DC-15:** "Artifact" means a machine-readable, schema-governed file: the project configuration, the integration mappings, the change definition, the state document. Markdown is out. A migration appends and never rewrites.
- **DC-16:** The content hash is defined in 25.2: text normalizes line endings, binary is byte-exact; the classification rule is left to the implementation, with the constraint that it depends only on the bytes and a SHOULD default (valid UTF-8 and no zero byte). The concrete rule is handed to the engine phases (OQ-7).
- **DC-25:** Section 22.1 gains `migrate`, inserted before the last list item so that no existing list line is rewritten (the item for recording a human decision came from plan 02).
- **OQ-6:** unchanged from plan 01: `core` `supersede` closes as `cancelled` with `replaced_by`; this plan only keeps `follows` as a reference.
- **OQ-7:** exit codes and the concrete text-versus-binary rule are not specified here (see Hand-off).
- **DC-80 (new):** The core layout of 4.3 shows `change.yaml`, `spec.md`, `state.json` and a conditional `review.md`; review files are not documents of the change and are measured by the scope check like any other non-record file.
- **DC-81 (new):** All ten body fields are always present and a field that does not apply is `null`; `at` is a UTC string written `YYYY-MM-DDThh:mm:ssZ`; `result` is `success` or `blocked` (a rejected or failed action writes no entry); `gate_results` and `gate_detail` are objects keyed by gate identifier; `files` is an object from a path to a content hash; an action may add its own body fields (only `migrate` does).
- **DC-82 (new):** The `after` record is the whole state, not a delta, and holds `schema_version` (deviation 2). The field is `base_revision` (24.5 wording), not the prototype's name. In `full` it holds `phase` and `status` in place of `state` and `outcome`, and `wait` holds the content of 11.2 and the other metadata of 8.1.
- **DC-83 (new):** Integers are decimal, without fraction or exponent, with a magnitude not above 2 to the power 53 minus 1; a string holds no surrogate code point; writing or hashing a value outside the domain ends with `error` and writes nothing.
- **DC-84 (new):** The expected version is the number of entries read (zero when the change has no state document). The writer takes an exclusive lock, compares under the lock, and on a difference answers `error` with the stable code `state-conflict` (an invalid or precondition-failing operation would be `rejected`; a lost race is an operation that could not be carried out). A lock that cannot be taken is `error`. Atomic replacement through a temporary file in the same directory; a leftover temporary file is ignored; a file system that cannot replace in one step means no write.
- **DC-85 (new):** A parsed YAML definition is read as YAML 1.2 with the core schema, aliases expanded. A float, a timestamp, a non-string key, a repeated key or an integer above the bound has no content hash and an operation that needs it is rejected. The parsed value of the Flow Gates of a `full` change is not defined here (see Hand-off).
- **DC-86 (new):** The content hash of a file set is the hash of the canonical form of an object from path to file hash (paths relative to the repository root with `/`). The hash of gate definitions together with a gate identifier is the hash of the canonical form of an object with the members `definitions` and `gate` (this completes the forward reference of 24.3).
- **DC-87 (new):** The version is a string of two integers joined by a dot, without sign or leading zero (except `0`), compared one integer at a time; a number is not a version. An implementation supports one or more versions; a version is migratable when it is unsupported, lower than the highest supported version, and a chain of steps leads to a supported one.
- **DC-88 (new):** Three stable issue codes: `migration-required` (older, migratable), `schema-version-unsupported` (newer, unknown, absent, null, empty, not a string, not a version), `schema-version-mismatch` (document version differs from the latest recorded one). Every operation that uses the file is refused, read-only ones and validation included; only `migrate` accepts a migratable version.
- **DC-89 (new):** `migrate` applies the steps in ascending order, one entry per step, all or nothing in one atomic write (a failing step answers `error`, a target not above the current version or not supported is `rejected`). It is a contract operation and not a row of a transition table; for the state document and the change definition of a change it is legal from every state (it changes neither state nor outcome); any participant may perform it and the actor and the assurance level are recorded like for any action.
- **DC-90 (new):** The migration entry adds the body fields `source_version`, `target_version` and `source_hash`. `source_hash` is the content hash of the state document before the step, as a parsed value for a JSON document and as a text file for a YAML document.
- **DC-91 (new):** The document version must equal `after.schema_version` of the last entry; a difference, lower or higher, makes the history not consistent in the sense of 24.4 and is refused with `schema-version-mismatch`.
- **DC-92 (new):** A project-level artifact is migrated inside a change that is not `closed` (a closed change is final); the entry's `files` maps the artifact path to its content hash after the step and `source_hash` is the hash before it. A migration of a change definition that alters the parsed gate definitions needs a new human approval (24.1).
- **DC-93 (new):** An old `state.yaml` is converted by `migrate` to `state.json` whose first entry is a `migrate` entry (`n` 1, the zero `prev`); the old file is not changed, deleted or read afterwards. The hash chain restarts at that entry, and the text says plainly that an anchor makes such a restart detectable. This is the only mention of the old file name outside history, as the R7 allowance.
- **DC-94 (new):** `reopen` is marked `full` only in the first cell of the 8.3 row; the results table keeps its row, because its caption names `full`; the sentences of 8.4 begin "In the `full` method profile"; a closed `core` change is final; `follows` is a reference and a new change naming a change that is `open`, `active`, `waiting` or unknown is rejected.
- **DC-95 (new):** The text carries two real SHA-256 test vectors (AE-183, AE-184). They are not development identifiers; check X1 passes. Plan 03 used placeholders for an illustrative statement; test vectors are the one place where a literal digest helps independent implementations.

## Hand-off list (D-11)

Files and values that this phase does not change and that the engine phases (5 to 8) must align with the proposed text once it is approved:

- `specs/examples/class-m/state.yaml` (the YAML example state; `flow.profile` at line 10 is the compliance profile), `.ggsad/templates/`, `.ggsad/schemas/state.schema.json`, and the archived CHG-001 state.
- The pinned method version "1.3" in `.ggsad/config.yaml` (line 10), `src/ggsad/application/initialize_project.py` (line 82) and `tests/unit/test_initialize_project.py` (line 61).
- The schema constants `"0.1"` at `.ggsad/schemas/config.schema.json:20`, `.ggsad/schemas/mappings.schema.json:19` and `.ggsad/schemas/state.schema.json:22`. The text fixes the form of `schema_version` and the checks, and it does not fix the version values. The schema version of the first JSON state document, and the first migration step (from the YAML state), are engine choices.
- Exit codes (WORK-01): no requirement owns them and none were added (research OQ-7, resolved by hand-off). Open for the engine phases: the mapping of the four results and the stable issue codes (`gates-changed`, `start-blocked`, `open-questions`, `state-conflict`, `migration-required`, `schema-version-unsupported`, `schema-version-mismatch`) to exit codes.
- The concrete text-versus-binary rule for content hashing (INTEG-02, research OQ-7): 25.2 states the constraint and a SHOULD default only.
- For plan 05: the parsed value of the Flow Gates of a `full` change (Markdown) for the content hash of 24.1 is not defined; the `full` realization table of the section 24 intro; the stray comma before "An `answer`" in the paragraph after the 23.4 table (plan 02 text) should be a full stop.

## Known Stubs

None.

## Threat Flags

None. The threat register entries were handled in the text: one total ordering and one value domain with worked canonical-form examples and parse-checked JSON blocks (T-02-14, AE-183 to AE-187); the document version must equal the latest recorded version and a migration appends and never rewrites (T-02-15, AE-210, AE-211); an expected-version check and atomic replacement with examples for both cases in both method profiles (T-02-16, AE-191 to AE-194); the absence of `reopen` in `core` is stated, rejected in an example, and `follows` is a reference only (T-02-17, AE-48, AE-215, AE-216).

## Unverified

- Whether the `full` readings are right (the `full` realization of state is argued, not tested), whether the lock and expected-version rule fits every file system, whether the version form and the three issue codes suit the engine, and whether the examples cover normal and failure behavior at the right risk level can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4).
- Unproven items, as the research marks them: SPEC-18 (no prototype evidence, decision-driven), SPEC-17 (proved by absence only), the YAML-to-JSON conversion rule, and the migration of a project-level artifact inside a change.
- The test vectors were computed with `sha256sum` and Python on this machine; no conformance test suite was run (no Python changed).
- The text is draft; nothing here is approved or reviewed.

## Self-Check: PASSED

- The summary exists next to the plan; the specification contains the headings `## 25. State, Hashing, and Schema Versions`, `### 25.1 State Document and Canonical Form`, `### 25.2 Content Hash` and `### 25.3 Schema Versions and Migration`, each once; the script contains the R1 and R7 checks.
- The six plan 04 commit subjects above are present in the log after `origin/main`, and four of them start `docs(02-04): SPEC-`.
