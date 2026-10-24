---
phase: 02-normative-drafting
plan: 03
subsystem: normative-spec
tags: [assurance-levels, signed-approval, history-anchor, scope, interpreter, executable-evidence, open-questions, bash-check]
status: complete

requires:
  - phase: 02-normative-drafting
    provides: "Plans 01 and 02: method profiles, the core profile (23), section 24 intro and 24.1, 24.2, 24.6, 24.7, conventions K1 to K6, the check script with --ids, AE-01 to AE-124"
provides:
  - "Check script: R3 (unfinished-text markers, warning only) and R2 citations (a defined example no rule line cites, a cited example that is not defined, a subsection of sections 23 to 25 that cites none; warning only); --section compares heading numbers as text"
  - "Section 24.3 Assurance Levels and Signed Approval, 24.4 History Consistency and Completeness, 24.5 Scope and Isolation, 24.10 Gate-Command Interpreter, 24.9 Executable Evidence, 24.8 Open Questions as State"
  - "Pointer sentences at 3.4, 3.10, 5.4, 6.1, 9.4, 10.6, 10.7, 11.3, 12.1, 14.2, 15 (four), 16.1 (two), 16.4, 19 and 20 (two bullets); the acceptance-exemption bullets of 9.5 and 10.4 replaced"
  - "Section 24 now holds 24.1 to 24.10 in numeric order"
  - "Acceptance examples AE-125 to AE-182"
affects: [02-04 state and versioning, 02-05 full revision and resolution, Phase 3 owner approval, engine phases]

actuals:
  tokens: 13300
  tasks: 3
  commits: 7

tech-stack:
  added: []
  patterns: ["rule once in section 24, one pointer sentence at each existing site", "rule paragraph ends 'See AE-nn.'", "illustrative statement in a text fence with placeholders instead of literal hashes"]

key-files:
  created: []
  modified:
    - docs/method/GG-SAD_normative_method_specification.md
    - .planning/phases/02-normative-drafting/02-check-normative-diff.sh

key-decisions:
  - "No owner decision was made. Judgment calls are listed under Drafting choices for the Phase 3 packet."

patterns-established:
  - "Quick check before every specification commit; each commit stages the specification only; C1 run with the ids done so far."

requirements-completed: [SPEC-04, SPEC-05, SPEC-06, SPEC-09, SPEC-10, SPEC-11]  # drafted as proposed text; SPEC-13 stays open: it is checked in every plan and closes with the phase.

duration: "about 1 hour"
completed: 2026-10-24
---

# Phase 2 Plan 03: Trust and Integrity Summary

**Proposed text for SPEC-04, SPEC-05, SPEC-06, SPEC-11, SPEC-10 and SPEC-09: assurance levels A0 to A2 with a fail-closed signed-approval statement and a plain credential limit, history consistency separated from completeness with an anchor rule and its stated limit, scope measured against the base revision with isolation, an explicit opt-in gate-command interpreter, executable evidence bound to each requirement, and open questions as change state, backed by 58 acceptance examples and a check script that now flags unfinished text and uncited examples.**

## Accomplishments

- Check script: R3 warns on TODO, FIXME, TBD, XXX, the word placeholder, "to be defined" and runs of question marks outside code fences. R2 now also warns when a defined example is cited by no rule line, when a cited example is not defined, and when a subsection of sections 23 to 25 cites no example. `--section` compared heading numbers as numbers, so `--section 24.10` printed 24.1 and `--section 3.10` printed 3.1; it now compares them as text.
- Section 24.3: levels `A0` (self-declared), `A1` (platform review of the checked-out revision, no uncommitted change in the approved files) and `A2` (valid signature over exactly the statement the implementation builds, by a key listed for the identity in a signers file kept outside the repository); verifiers are optional; verification fails closed; the required level is the higher of the gate minimum and the configured minimum, and a compliance profile sets none; human-only actions with the `human:` identity prefix; the approval binds the content hash of Section 25.2; the statement layout (format identifier and version, operation, change, version as history position, identity, details sorted by name, values JSON-encoded); key handling; and the sentence that an agent able to use a human's credentials can act as that human, with its consequence at each level.
- Section 24.4: entry fields and the entry hash over the canonical form of Section 25.1; consistency (unbroken chain, at least one entry) separated from completeness; an anchor or an equivalent where the configuration requires approvals at A2; truncated and rewritten findings; no anchor means refused until a human adopts; an anchor is only advanced, never replaced; the stated limit that an actor who can write both can rewrite both.
- Section 24.5: the allowed path list, path pattern rules, the base revision recorded at start (start refused when it cannot be recorded), the measured set (tracked differences incl. staged and unstaged, plus untracked unignored files), an outside path is a hard failure, the change's own record files are exempt, not evaluated before start and `not_evaluable` after start without a base, ignored files invisible, an empty allowed list allows no path while an empty changed set is in scope, and isolation.
- Section 24.10: commands run as argument lists without a shell; the designated first token `@interpreter` stands for the configured interpreter only, never a discovered one, and for the implementation's own interpreter when none is configured; a warning when the interpreter lives inside the repository; the trust consequence that code in ignored locations is invisible to the scope check.
- Section 24.9: evidence is complete only with at least one requirement, an evidence command for each requirement, and each command `satisfied` at closure; a command that cannot run is `not_evaluable`; other records supplement and never replace the check; the permitted-evidence list and the `spec.md` sentence of 15 are qualified; criterion added to 20.
- Section 24.8: question fields, `ask` and `wait` in `core`, distinct options, only the owner answers, a human owner needs a human, empty free text and a repeated answer rejected, an unanswered question rejects specification approval (`open-questions`) and blocks closure; acceptance becomes an answer in 9.5 and 10.4; the Open Questions section of 16.1 is a view; criterion added to 20.

## Task Commits

1. Task 1 (tracer), script: `docs(02-03): extend normative diff check script (R3, R2 citations)`
2. Task 1 (tracer), SPEC-04: `docs(02-03): SPEC-04 define assurance levels and signed approval in section 24.3`
3. Task 2, SPEC-05: `docs(02-03): SPEC-05 separate history consistency from completeness in section 24.4`
4. Task 2, SPEC-06: `docs(02-03): SPEC-06 define scope measurement and isolation in section 24.5`
5. Task 2, SPEC-11: `docs(02-03): SPEC-11 make the gate-command interpreter explicit and opt-in in section 24.10`
6. Task 3, SPEC-10: `docs(02-03): SPEC-10 require executable evidence tied to a requirement in section 24.9`
7. Task 3, SPEC-09: `docs(02-03): SPEC-09 record open questions as change state in section 24.8`

The summary and planning-state commits follow. The tracer passed its own commands (`--ids SPEC-04` printed `FAIL C1` before the SPEC-04 commit and `RESULT: PASS` after), and the plan has no human checkpoint, so no stop was made at the tracer gate.

## Verification

- `bash -n` exits 0; `shellcheck` exits 0 (run, no findings).
- Seeded defects on copies of the specification outside the repository (`--file`): a defined example no rule line cites prints `WARN R2 ... is defined but no rule line cites it`; a cited example that is not defined prints `WARN R2 ... is cited but not defined`; a new `### 24.9` subsection without a citation prints `WARN R2 section 24.9 cites no acceptance example`; a `TODO` line and a "to be defined" line outside a fence print `WARN R3`, while a `TODO` inside a fence does not. Every seeded run still ended `RESULT: PASS`, because these checks are warnings in quick mode.
- Two consecutive quick runs print identical output; `git status --short` showed only the intended modification after script runs.
- `--ids` before each specification commit printed `FAIL C1` for the id being drafted (the expected red); after each commit it printed `RESULT: PASS` with the ids done so far. The final run `--ids SPEC-04,SPEC-05,SPEC-06,SPEC-11,SPEC-10,SPEC-09` printed `RESULT: PASS`.
- Final quick run: B1 E1 E2 E3 S1 S2 N1 X1 R5 R6 R2 R3 all `PASS`; warnings: `WARN X1` (the word "prototypes" in existing text of section 5.1) and two `WARN R8` on the heading and map row "Protections Shared by Both Profiles" (fixed text from plan 02). `bash CHK | grep -c '^WARN R[23]'` is 0. The R2 line reports 182 example blocks, all cited, all with a unique id.
- `grep -n '^### 24\.'` lists 24.1 to 24.10 in numeric order; the map row for section 24 occurs once and R5 holds.
- Section checks: `--section 24.3` contains `can act as that human`, `fail closed`, `signers`, `outside the repository`, `format identifier`, `A0`, `A1`, `A2`, `Section 25.2`; `--section 24.4` contains `consistency`, `completeness`, `anchor`, `truncat`, `adopt`, `Section 25.1`; `--section 24.5` contains `hard failure`, `untracked`, `ignored`, `isolated`; `--section 24.10` contains `opt-in`, `shell`, `invisible to the scope check`; `--section 24.8` contains `open-questions`, `structured`, `options`, `blocked`, `answer`; `--section 24.9` contains `executable`, `bound to`, `not complete`, `no requirements`; `--section 20` contains `unanswered` and `executable`.
- `--section 9.5` and `--section 10.4` each contain 0 lines with `explicitly accepted`.
- Pointers: each of 5.4, 3.10 and 14.2 outputs a `Section 24.3` reference; each of 15, 12.1, 10.6, 19 and 6.1 outputs a reference to 24.4, 24.5 or 24.10; each of 3.4, 10.7, 16.1 and 16.4 outputs `Section 24.9`; each of 9.4, 11.3 and 16.1 outputs `Section 24.8`.
- Example coverage: 12 blocks cover 24.3, 10 cover 24.4, 11 cover 24.5, 5 cover 24.10, 8 cover 24.9 and 12 cover 24.8. AE-125 to AE-182 are defined once, consecutive, and all cited.
- Additions only: the commits for SPEC-04, SPEC-05, SPEC-06, SPEC-11 and SPEC-10 remove no line. The SPEC-09 commit removes exactly the two acceptance-exemption bullets of 9.5 and 10.4 that the plan replaces.
- `git diff --name-only origin/main...HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; changed paths are the specification and `.planning/` only.
- Python baseline: not run (no Python changed).

## Deviations from Plan

**1. [Rule 1 - Bug] The `--section` reader compared heading numbers numerically.**
- **Found during:** Task 1 while checking the pointer sites.
- **Issue:** `--section 3.10` printed 3.1 and `--section 24.10` would have printed 24.1, which would make the acceptance checks of this plan read the wrong section.
- **Fix:** the comparison is done as text. Verified with 24.1, 24.10, 3.1, 3.10 and 5.
- **Files modified:** `.planning/phases/02-normative-drafting/02-check-normative-diff.sh`
- **Commit:** `docs(02-03): extend normative diff check script (R3, R2 citations)`

**2. [Rule 2 - Missing critical functionality] The evidence commands are fixed with the gate definitions.**
- **Found during:** Task 3, SPEC-10.
- **Issue:** The gate definitions of 24.1 list the gates, their declarations and the scope. The incomplete evidence gate judges the change by the requirements and their evidence commands, which 24.1 does not list. A participant could replace a command with one that always succeeds after the approval and no rule would stop it.
- **Fix:** 24.9 states that the requirement identifiers and the evidence commands are fixed with the gate definitions, and a one-paragraph pointer was added to 24.1 as its own paragraph (no existing line was rewritten). An example (AE-169) shows the `gates-changed` rejection.
- **Commit:** `docs(02-03): SPEC-10 require executable evidence tied to a requirement in section 24.9`

**3. [Plan reading] The SPEC-09 commit is not additions only.** The plan directs replacing the two acceptance-exemption bullets in the same position; the only removed lines are those two bullets.

Otherwise the plan was executed as written.

## Drafting choices

For the Phase 3 packet; the owner can overrule each one. DC-08, DC-10, DC-11, DC-17, DC-18 and DC-21 are research register ids; DC-59 onward are new in this plan (DC-28 to DC-39 are in plan 01, DC-40 to DC-58 in plan 02).

- **DC-08:** Acceptance of an open question is an answer. The bullets of 9.5 and 10.4 now read "all open questions have been answered (Section 24.8)"; statements of acceptance outside the history leave the question unanswered; the Open Questions section of 16.1 is a view and the recorded state governs.
- **DC-10:** Examples were written for each rule paragraph of 24.3 to 24.10 (normal and failure or boundary behavior each); AE-125 to AE-182 are consecutive and cited but not in document order.
- **DC-11:** No assurance floor is assigned per compliance profile. A minimum level comes only from a gate or from the project configuration; "high assurance" in the anchor rule means that the applicable configuration requires approvals at A2.
- **DC-17:** The text cites no decision, requirement, prototype or finding id; check X1 passes. The statement example uses placeholders, not literal hashes.
- **DC-18:** Complete evidence needs an executable check bound to each requirement; the records of Section 15 supplement it. The permitted-evidence list and the `spec.md` sentence of 15 are qualified by added paragraphs, not rewritten.
- **DC-21:** Scope is measured against "the revision the change started from" and the measured set is described by version-control facts (tracked differences, committed, staged or unstaged, plus untracked files that are not ignored), not by one system.
- **DC-59 (new):** The level names are the exact strings `A0`, `A1`, `A2`. A1 is defined by a platform review (latest review of the account the project configuration maps to the identity approves the checked-out revision, and no approved file has an uncommitted change); the specification names no platform.
- **DC-60 (new):** The required level of an action is the higher of the gate minimum and the project configuration minimum for the kind of action; an unstated minimum is A0. The kinds are: approval of the specification, approval and re-approval of gate definitions, sign-off, override, answer, `cancel` and `supersede`, `fail`, `adopt`.
- **DC-61 (new):** The human-only actions are every approval, sign-off, override, an answer to a question with a human owner, `cancel`, `supersede`, `fail`, `adopt` (`supersede` is added to the list the plan named, because 23.4 already requires a human). The identity of a human carries the exact prefix `human:`; without it a human-only action is rejected.
- **DC-62 (new):** The statement is built by the implementation. It holds a first line with the format identifier and version (spelling not fixed), then operation, change, version (the number of history entries when built, which names the history position), identity, and the details sorted by name in code point order. Every value after the first line is JSON-encoded as 25.1 encodes it. The signed bytes are the UTF-8 lines, each ended by a line feed. A statement with an unsupported identifier or version is not verified.
- **DC-63 (new):** An approval binds the content hash (25.2) of the specification, of the gate definitions, or of the gate definitions plus the gate or fail condition identifier. The specification approval is stale while the current hash differs.
- **DC-64 (new):** An implementation that creates signatures SHOULD refuse an unprotected private key unless a human allows it; a participant who can write the signers file can list its own key (stated).
- **DC-65 (new):** An anchor or an equivalent is required only where the configuration requires approvals at A2, and MAY be kept otherwise. An equivalent is defined by properties (independent record of the latest position and hash, written only after a successful append, supports the three checks, cannot be replaced). The anchor is kept outside the working tree and outside the history and is advanced after every successful append.
- **DC-66 (new):** `adopt` is rejected when the history is not consistent, in addition to the 23.4 precondition that no anchor exists, and requires a human at the level 24.3 requires for `adopt`.
- **DC-67 (new):** History entry fields are `n`, `prev`, `body`, `hash`; the first `prev` is `sha256:` followed by 64 zero digits; the entry hash is over the canonical form of an object holding `prev` and `body`; the state of the change is the state the last entry records. A history without an entry is not consistent.
- **DC-68 (new):** In `full` the allowed path list is a list of path patterns stated in the Scope of the change specification; a `full` change that states none has a scope that cannot be measured (`not_evaluable`). The 16.1 template is not changed here.
- **DC-69 (new):** Path patterns are relative to the repository root with `/`; a pattern without a wildcard names one path, a trailing `/` names a directory tree, `*` stays inside one segment, a segment `**` matches any number of segments; an empty pattern, a leading `/` or a segment `..` is invalid and rejected at approval. Drafted conservatively; flagged for the rule-unit review of plan 05 (F1).
- **DC-70 (new):** In `full` the base revision is recorded when the first phase of the change begins.
- **DC-71 (new):** The exempt record files are the change definition, the specification and the state document in `core`, and the specification and the state file or inline record in `full`; every other file in the change directory is measured.
- **DC-72 (new):** Before start the scope gate is recorded `not_applicable`; after start a scope that cannot be measured (version control unavailable, no base revision, or no allowed path list) is `not_evaluable`, never `satisfied` and never a violation.
- **DC-73 (new):** A change MUST run isolated; an implementation SHOULD warn when it finds other uncommitted work at start and MUST NOT exclude such work from the measurement.
- **DC-74 (new):** The designated token is the literal `@interpreter`; the interpreter is never discovered; with no configuration it is the implementation's own interpreter; an implementation SHOULD warn when the interpreter lives inside the repository.
- **DC-75 (new):** An evidence command is a check command of 24.2 (argument list and exit map). Closure is `close` in `core`, and the evaluation of Verify-Done (10.7) and of the completion criteria (20) in `full`.
- **DC-76 (new):** The requirement identifiers and the evidence commands are fixed with the gate definitions (see Deviations, item 2).
- **DC-77 (new):** A question id is `Q` plus a decimal number from 1 assigned by the implementation; options of a structured question are pairwise distinct (a repeated option is rejected); a free-text answer that is empty or only spaces, tabs and line breaks is rejected; an answer does not resume a waiting change; question ids compare as code point sequences.
- **DC-78 (new):** In `full` a question is recorded in the state file, or in the inline record where none is persisted, and the answer is recorded as a human decision (22.1); an unanswered question makes a Definition of Wait condition active, so `complete` and `resume` answer `blocked`.
- **DC-79 (new):** The issue code `open-questions` is named in the text. The codes `gates-changed` and `start-blocked` from plan 02 are reused unchanged.

## Hand-off sites

- Forward references that must resolve by the end of plan 04: Section 25.1 (the JSON value encoding used by the statement, the entry fields and hash, the `state`, `outcome`, question and wait fields, the code point comparison cited by the section 24 intro) and Section 25.2 (the content hash applied to a parsed definition and to a specification document, cited by 24.1 and 24.3).
- Plan 05: the realization table in the section 24 intro for 24.3 to 24.10; the `full` parts of 24.5 (allowed path list in the Scope of 16.1, base revision at the first phase) and 24.8 have the examples AE-170 and AE-182 only for evidence and questions, none for scope; the path pattern rule (F1); section 5.3 layers (the base gates of 23.7 are cited from 24.3, 24.5, 24.8 and 24.9).
- Engine phases (unchanged by this phase): configuration keys for the minimum levels, the interpreter, the platform account mapping, the signers file location and the anchor location are not named by the specification; the spelling of the statement format identifier, the signature scheme, and the storage of the anchor are implementation choices; the issue code `open-questions`.

## Known Stubs

None.

## Threat Flags

None. The threat register entries were handled in the text: the credential limit is stated plainly with the fail-closed rule, a statement that binds operation, change, history position and content, and the replay example (T-02-10, AE-129, AE-134, AE-136); the anchor rules carry the stated limit and a truncation example (T-02-11, AE-139, AE-145); ignored locations are stated invisible and the interpreter is opt-in and never discovered (T-02-12, AE-150, AE-160, AE-162); the exemption wording is replaced by a recorded answer, checked on 9.5 and 10.4 (T-02-13, AE-180).

## Unverified

- Whether each rule faithfully states the protection the prototype exercised, whether the `full` readings are the right ones (they are argued, not tested), and whether the examples cover normal and failure behavior at the right risk level can only be judged by the owner (Phase 3) and the independent reviewer (Phase 4).
- Unproven items: the A1 platform-review verifier (not tested directly; it cannot serve a participant who works alone); the "or an equivalent" clause of the anchor rule (nothing exercised an equivalent mechanism); the path pattern syntax (drafted, not exercised); the `full` realizations of scope, evidence and questions.
- Cross references to Sections 25.1 and 25.2 do not resolve yet, by design.
- The text is draft; nothing here is approved or reviewed.

## Self-Check: PASSED

- The summary exists next to the plan; the specification contains the six headings `### 24.3 Assurance Levels and Signed Approval`, `### 24.4 History Consistency and Completeness`, `### 24.5 Scope and Isolation`, `### 24.8 Open Questions as State`, `### 24.9 Executable Evidence` and `### 24.10 Gate-Command Interpreter`, each once; the script contains the R3 check.
- The seven plan 03 commit subjects above are present in the log after `origin/main`, and six of them start `docs(02-03): SPEC-`.
