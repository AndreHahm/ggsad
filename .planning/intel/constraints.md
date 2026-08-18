# Constraints

Two sources in this ingest set were classified `type: SPEC`, each with a manifest precedence
override (lower integer = higher precedence):

- `docs/method/GG-SAD_normative_method_specification.md` — precedence **0** (highest in this
  ingest set) — "the leading document" per the second SPEC's own owner-confirmed decisions.
- `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md` —
  precedence **1** — an approved transition design; explicitly does not itself amend the
  normative specification, delete existing governance, install GSD, or change the Python
  implementation; it designs a transition sequence for later governed changes to execute.

Both are `Status: Approved` / `Normative Baseline` as stated in their own documents. Where they
overlap, the design document (precedence 1) governs the transition process; the normative method
specification (precedence 0) governs GG-SAD method semantics and remains superior in the
document hierarchy it itself defines. No direct content contradiction was found between the two
SPECs — the design document explicitly subordinates itself to the normative specification.

---

## Document Hierarchy (Binding Order of Precedence)

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: In case of conflict inside a GG-SAD-governed project, precedence is: (1)
  `docs/constitution.md`, (2) existing accepted ADRs under `docs/adr/`, (3)
  `docs/project-brief.md`, (4) `docs/architecture.md`, (5) approved scoped decision records that
  do not replace an ADR, (6) approved change specification `spec.md`, (7) approved implementation
  plan `plan.md`, (8) local task list `tasks.md`, (9) implementation and tests, (10) evidence,
  supplementary notes, and temporary work artifacts. "A change MUST NOT silently override a
  higher-ranking document." This is the GG-SAD *product's own* internal document hierarchy
  (i.e., a rule the GG-SAD method itself defines for projects that adopt GG-SAD as their
  governing method) — it is distinct from, and must not be confused with, the separate question
  of which method governs *this* repository's own development (resolved in the "Development
  Method Transition" entry below).

## Phase Model and Gate Evaluation Order

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: Standard phases: `INTAKE → SPECIFY → PLAN → BUILD → VERIFY → RELEASE → CLOSED`, with
  permitted shortened flows (Patch, Standard, Release, Exploration). Standard statuses: `draft,
  ready, active, waiting, failed, done, cancelled, superseded`. Gate evaluation order MUST always
  be: (1) Definition of Fail, (2) Definition of Wait, (3) current-phase Definition of Done, (4)
  next-phase Definition of Ready. "A satisfied DoD does not override a satisfied DoF or DoW."
  State changes occur only through explicit transition actions (`start, complete, wait, resume,
  fail, cancel, supersede, reopen`), never arbitrary status mutation.

## Definition of Ready / Done / Wait / Fail (method-level summary)

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: Sections 9–12 define minimum DoR criteria per phase (Ready-to-Spec/Plan/Build/
  Verify/Release), minimum DoD criteria per phase (Spec/Plan/Build/Verify/Release-Done), DoW
  categories (`WAIT_USER_INPUT`, `WAIT_DECISION`, `WAIT_DEPENDENCY`, `WAIT_PROCESS`,
  `WAIT_APPROVAL`, `WAIT_EXTERNAL_SYSTEM`) with mandatory wait-record fields, and DoF categories
  (critical technical error, data loss/corruption, security breach, unauthorized breaking change,
  constitution/ADR violation, scope violation, budget/retry-limit exceeded, unrecoverable state,
  unsatisfiable acceptance conditions) with mandatory fail-rule fields. Expanded, project-facing
  versions of these four gates also exist as separate DOC-classified sources (see `context.md`,
  "Project-Wide Gate Definitions").

## Pair Review Model

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: Requestor and Reviewer MUST be distinct participant identities within the same review
  cycle (Human–Human, Human–Agent, Agent–Human, Agent–Agent, or Human/Agent with an external
  review service). Pair Review is optional by default; activation and depth are resolved from
  compliance profile, scope, class, risk, and policy. The Reviewer MUST NOT silently modify the
  Requestor's governed work product; findings MUST return to the Requestor for disposition.
  Unresolved blocking findings MUST block the applicable gate. Pair Review MUST NOT replace a
  required human approval. A fresh context or subagent of the same participant does not satisfy
  independence.

## Evidence Model

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: Evidence MUST demonstrate traceably whether requirements, gates, and quality criteria
  are satisfied (test results, build output, static analysis, security scans, review approvals,
  logs, screenshots, measurements, deployment/release records, commit/PR references). A minimal
  evidence template with a Requirement Coverage table, Quality Gates checklist, Deviations, and
  Final Status is defined.

## Agent Execution Algorithm and Prohibitions

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: A 12-step per-phase algorithm (load context → determine phase/status/goal/scope →
  evaluate DoF → DoW → DoD → preserve evidence → evaluate next DoR → start only if ready →
  perform changes only within approved scope → verify compliance after each change → enter
  controlled wait on conflict/uncertainty/missing approval → final drift/evidence check before
  completion). Explicit prohibitions: an agent MUST NOT invent goals/requirements/approvals,
  interpret missing information as consent, silently modify higher-ranking documents, implement
  unapproved breaking changes, bypass wait states through speculation, mark a flow done with
  missing evidence, conceal errors, or work beyond approved scope.

## Compliance Profiles and Workflow Tailoring

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: Every GG-SAD-governed project selects one active compliance profile (`lean`,
  `standard`, `governed`, `regulated`, or a documented custom profile inheriting from one of
  these). Effective workflow resolution order: invariant core → compliance profile → project
  configuration → change-class requirements → local strengthening in the change spec →
  integration mappings. "A lower layer MUST NOT silently weaken a higher layer." Size classes:
  Class S (Patch, inline spec), Class M (Change, mandatory `spec.md`), Class L (Initiative,
  decomposed into multiple change specs).

## Combination Contracts and GG-SAD Memory Model

- source: docs/method/GG-SAD_normative_method_specification.md
- type: protocol
- content: Every external integration (e.g. GSD, OpenSpec, Spec Kit, BMAD, Hermes, Kiro — named
  as non-normative examples) requires a mapping contract defining ownership, mapped GG-SAD
  phases/artifacts, authoritative source per mapped fact, permissions, gate/approval interaction,
  state synchronization, and failure/rollback/uninstall behavior. GG-SAD MAY provide a project
  memory (Decision, Learning, Failure, Definition, External Source record types); memory MUST NOT
  replace governing documents, and architecture decisions MUST remain ADRs (a memory decision
  MUST NOT be used to avoid the ADR process).

---

## Development-Method Transition: GSD Core Is the Sole Development Method

- source: docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md
- type: protocol
- content: Owner-confirmed governing decision #3: "GSD Core is the sole development method for
  this minimal-automation prototype." Decision #4: "GG-SAD is the product being implemented; it
  does not govern development of this prototype." Use official GSD Core **1.10.0** (pinned, not
  `latest`); the repository's prior 1.9.1 installation is updated in place via the official
  installer's supported update path, then onboarded (no `.planning/` existed before this
  transition). Non-goal: "Using GG-SAD and GSD simultaneously as development methods." This
  directly supersedes the GG-SAD-governs-this-repo's-own-development framing found throughout
  the DOC-classified corpus (constitution.md, project-brief.md, architecture.md, roadmap.md,
  ADR-0001–0008, CHG-001 spec.md, implementation-guide.md, implementation-roadmap.md,
  workflow-reference.md) — see the auto-resolved entry in `INGEST-CONFLICTS.md`.

## Existing Repository Treatment (Retain vs. Retire/Rewrite)

- source: docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md
- type: protocol
- content: Retain initially: `src/ggsad/`, `tests/`, packaging and Python quality configuration,
  the English normative specification, and product schemas/templates/examples required by the
  clarified contract. Retire, archive outside the active workflow, or rewrite: the German
  normative specification; the root development constitution and agent rules that impose GG-SAD
  workflow; `CLAUDE_CODE_PROJECT_START.md` (retired); `CLAUDE.md` (replaced); `AGENTS.md`
  (rewritten); `specs/CHG-*` development state and evidence; roadmap, ADRs, architecture, and
  implementation plans "whose conclusions assumed the prior GG-SAD/GSD combination model."
  Retain-versus-rewrite rule: "Existing code is retained only when it conforms to the clarified
  product contract and passes verification. Prior GG-SAD completion evidence is historical
  context, not proof of conformance."

## Quality and Verification Baseline

- source: docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md
- type: nfr
- content: `uv sync --locked`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty
  check`, `uv run pytest`, `uv build`. Installer-owned GSD runtime files must not be treated as
  Python product source; quality-tool scope must explicitly include product code, tests, and
  owned scripts while excluding third-party generated tooling. (Matches the baseline independently
  stated in `docs/constitution.md` §11 and `docs/definitions/definition-of-done.md`, except those
  DOC-classified sources use `uv sync` without `--locked`.)

## Normative Specification Correction Scope (planned amendment content)

- source: docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md
- type: protocol
- content: A future governed amendment to the leading SPEC must: (1) establish the SPEC's own
  authority/applicability and separate method semantics from reference-implementation
  requirements from optional integration guidance; (2) define a canonical artifact model
  distinguishing mandatory information from mandatory files (`state.yaml` when persistent state
  is used; `plan.md`/`tasks.md`/`evidence.md`/`review.md` remain conditional); (3) replace the
  state narrative with an explicit transition-table contract (canonical phases/statuses, legal
  combinations, gate evaluation per action, cancellation/supersession/reopening/terminal
  behavior); (4) make tailoring deterministic (self-approval under `lean` stays subordinate to
  non-delegable human approval); (5) define portable Pair Review evidence (participant, role,
  reviewed revision, action, timestamp, result, findings, disposition); (6) define a
  technology-neutral minimal automation contract (init, create goal-bound change, validate,
  evaluate/execute one controlled transition, reject invalid operations without partial mutation,
  emit human- and machine-readable results, record history); (7) repair document quality
  (renumber Sections 6–13, remove the German spec, remove tool-local citations, label examples
  clearly).

## Transition Sequence and Explicit Non-Goals

- source: docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md
- type: protocol
- content: 13-step ordered transition sequence: (1) approve design; (2) create a bootstrap
  implementation plan; (3) update installer-managed GSD to pinned 1.10.0; (4) replace/suspend
  `AGENTS.md`/`CLAUDE.md`/`CLAUDE_CODE_PROJECT_START.md`; (5) onboard the repository into GSD;
  (6) use GSD to plan/prepare the normative amendment without changing implementation behavior;
  (7) obtain owner approval for the exact normative diff; (8) obtain independent Claude Code
  review and resolve blocking findings; (9) use GSD to retire/relocate remaining conflicting
  development-governance artifacts; (10) configure quality tools to separate owned source from
  installer-owned tooling; (11) audit retained implementation against the clarified contract;
  (12) implement only identified conformance gaps through GSD; (13) run the complete verification
  baseline and record GSD verification results. Explicit non-goals for this transition: building
  profile resolution, a full gate engine, memory, MCP, a web UI, CI integration, or multi-agent
  orchestration; preserving prior roadmap ordering or change-closure claims; using GG-SAD and GSD
  simultaneously as development methods; rewriting passing implementation code solely for a clean
  history.
