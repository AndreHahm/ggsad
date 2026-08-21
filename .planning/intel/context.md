# Context

Topic-keyed notes from every source classified `type: DOC` in this ingest set (29 sources).
Every entry lists its `source:` for provenance. Where a topic is superseded or subordinated by a
higher-precedence SPEC (see `constraints.md`), that status is noted explicitly; the original
content is still summarized here for traceability, not discarded.

---

## GSD Bootstrap Transition — Implementation Plan and Review Findings

- source: docs/superpowers/plans/2026-08-18-gsd-bootstrap-transition.md
- source: docs/superpowers/plans/2026-08-18-gsd-bootstrap-transition-findings.md
- source: docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design-findings.md

The plan (Requestor: Codex) sequences five tasks to execute the transition design: (1) capture a
pre-transition baseline (branch state, GSD version 1.9.1, product checks — 150 tests passing;
`ty check` explicitly excluded from the "green baseline" assertion because installer-owned
`.claude/scripts` produce 31 diagnostics, to be recorded as a future GSD work item); (2) update
installer-owned GSD Core to pinned 1.10.0 via `npx @opengsd/gsd-core@1.10.0 --claude --local`
after verifying npm package metadata; (3) replace `AGENTS.md` and `CLAUDE.md` with concise
authority-contract text and delete `CLAUDE_CODE_PROJECT_START.md`; (4) onboard the retained
repository into GSD via `/gsd-onboard`, requiring the generated roadmap's first milestone to
follow a specific 7-step order (clarify normative spec → owner approval + independent review →
retire legacy governance → correct quality-tool ownership → audit implementation → implement only
evidenced gaps → run full verification) and rejecting any roadmap that adds profile resolution, a
gate engine, memory, MCP, web UI, CI integration, or multi-agent orchestration; (5) close the
bootstrap and hand control to GSD, verifying a clean, separately-committed history and running
`/gsd-progress --next`.

Global plan constraints: do not modify the normative spec or `src/ggsad/`/`tests/`/product
schemas/templates/examples during this bootstrap; do not manually edit installer-owned files;
pin GSD Core exactly to 1.10.0; stop on any unresolved installer migration, destructive
replacement, or manifest conflict.

Two independent-review cycles by Claude Code (as Reviewer, Codex as Requestor) preceded and
followed the plan:
- Review of the design document (commit `800a004`) found two blocking gaps (F-02: `CLAUDE.md`
  and `CLAUDE_CODE_PROJECT_START.md` not named in the retirement/rewrite scope; F-03: bootstrap
  authorization claim lacked an evidence trail) plus five non-blocking findings; all were
  dispositioned by the repository owner on 2026-08-18 (see the disposition table in
  `constraints.md`'s source SPEC).
- Review of the resulting plan (commit `f070237`) found full conformance to the approved design
  with **no blocking findings** and three non-blocking gaps (PF-01: Task 5's diff check omitted
  `.ggsad/` and `specs/examples/`; PF-02: no explicit single-commit rollback step for the
  onboarding task; PF-03: npm package identity asserted but not independently verifiable from
  repo state alone — informational only). PF-01 and PF-02 were incorporated into the plan (visible
  in the plan text read above — Task 5 Step 2 already diffs `.ggsad` and `specs/examples`, and
  Task 4 Step 7/Step 3-of-Task-5 already implement a targeted single-commit revert).

This transition work is itself the mechanism that produced the current repository state (this
ingest run), i.e. `.planning/` now exists because Task 4 of this plan executed.

## Legacy GG-SAD Architecture Decision Records (ADR-0001–0008)

- source: docs/adr/ADR-0001-use-python-for-reference-engine.md
- source: docs/adr/ADR-0002-use-markdown-for-governing-documents.md
- source: docs/adr/ADR-0003-use-yaml-for-configuration-and-state.md
- source: docs/adr/ADR-0004-separate-method-core-from-integrations.md
- source: docs/adr/ADR-0005-use-explicit-state-transition-actions.md
- source: docs/adr/ADR-0006-use-gsd-as-initial-execution-companion.md
- source: docs/adr/ADR-0007-use-one-agent-with-phase-workflows.md
- source: docs/adr/ADR-0008-defer-memory-mcp-web-ui-and-orchestration.md

All eight carry `Status: Proposed` (never accepted), `Related Change: CHG-001`, dated
2026-08-02, manifest-classified `type: DOC` (see `decisions.md`). Candidate technical direction
recorded, each with full Decision Drivers / Considered Options / Consequences / Risk tables in
source:

- **ADR-0001**: Python 3.12+ for the GG-SAD reference engine and CLI (vs. .NET/C#, Rust).
- **ADR-0002**: Markdown as the normative format for governing/change documents; YAML/JSON for
  structured state (vs. YAML/JSON-only, vs. database/proprietary docs platform).
- **ADR-0003**: YAML for GG-SAD configuration, profiles, mappings, and change state, with JSON
  Schema for structural contracts and safe/explicit YAML loading (vs. JSON-only, vs. TOML).
- **ADR-0004**: Separate the stable Method Core/Engine from Method Services, Agent Workflows, and
  optional Integration Adapters, with dependencies flowing strictly inward (vs. building directly
  around GSD/Claude Code, vs. a plugin-first framework).
- **ADR-0005**: Expose explicit validated transition actions (`start, complete, wait, resume,
  fail, cancel, supersede, reopen`) rather than direct `state.yaml` editing; initial bootstrap
  supports only `draft → ready` (vs. direct file editing, vs. event-sourced state only).
- **ADR-0006**: Use GSD Core as the initial subordinate execution/context-engineering companion
  for Claude Code, with GG-SAD remaining authoritative for governance/state/gates/evidence/
  approvals/closure (vs. OpenSpec, Spec Kit, BMAD, or GG-SAD stand-alone only). Constraints
  include "GSD may not approve or transition GG-SAD state directly" and "`/gsd-ship` does not
  close a GG-SAD change." **This ADR's premise (GG-SAD governs, GSD is subordinate) is the
  framing explicitly reversed by the higher-precedence transition SPEC** — see
  `INGEST-CONFLICTS.md`.
- **ADR-0007**: One primary implementation agent with phase-specific workflows and permissions
  for the initial reference implementation, rather than a specialized multi-agent team or an
  autonomous orchestrator; independent Pair Review still requires a distinct participant.
- **ADR-0008**: Defer project memory, MCP exposure, web UI, and multi-agent orchestration from
  CHG-001 and early core milestones until validated by real pilots.

## GG-SAD Human-Readable Guides (English and German)

- source: docs/guides/GG-SAD_human_readable_guide.md
- source: docs/guides/GG-SAD_human_readable_guide_DE.md

Plain-language explanatory guides (not normative) describing GG-SAD as built on four blocks
(Goal, Specification, Gates, Evidence), the DoR/DoD/DoW/DoF gate model in evaluation order
(DoF → DoW → DoD → DoR), the three change size classes (S/M/L), compliance profiles
(lean/standard/governed/regulated), stand-alone vs. combination operating modes, Example-Driven
Specification, and the Pair Review model. The German guide (`GG-SAD_human_readable_guide_DE.md`)
is a full translation of the English guide (`GG-SAD_human_readable_guide.md`) with equivalent
content; both are guides, not the normative specification itself, so they are not directly
subject to the transition SPEC's "remove the German normative specification" directive (which
targets `GG-SAD_normative_method_specification_DE.md` specifically — see next entry).

## GG-SAD Normative Method Specification (German) — targeted for removal

- source: docs/method/GG-SAD_normative_method_specification_DE.md

Full German-language translation of the normative method specification (same structure and
content as `docs/method/GG-SAD_normative_method_specification.md`, covering purpose, normative
terms, core principles, document hierarchy, workflow/compliance tailoring, size classes, phase
model, state model, DoR/DoD/DoW/DoF, conflict rules, Pair Review model, evidence model, minimum
templates, combination contracts, memory model, and agent execution algorithm). Owner-confirmed
governing decision #7 in the transition design SPEC states: "The German normative specification
is removed until the English baseline stabilizes." This document is therefore flagged for
removal per the higher-precedence SPEC (see `constraints.md` and `INGEST-CONFLICTS.md`); it is
retained here only as a historical record of its content at ingest time.

## GG-SAD Reference Implementation Architecture (two competing documents)

- source: docs/architecture.md
- source: docs/architecture-reference.md

Two separate files describe essentially the same five-layer reference architecture (Layer 5
Integrations/Companion Methods → Layer 4 Agent Workflows → Layer 3 Method Services → Layer 2
Method Engine → Layer 1 Method Core), the same dependency-direction rule (dependencies flow
inward, Method Core has zero tool/vendor dependencies), the same main execution flow (load
governing docs → resolve profile → validate → Gate Engine [DoF→DoW→DoD→DoR] → Transition Engine
→ State Manager), and overlapping component responsibilities (State Manager, Transition Engine,
Gate Engine, Document Validator, Evidence Mapper, Pair Review Service, Memory Service, CLI, Agent
Workflow Adapter, Integration Adapters) and a Python/uv/Typer/Pydantic/ruamel.yaml/JSON
Schema/pytest/Hypothesis/Ruff/ty technology baseline. `docs/architecture.md` ("GG-SAD Reference
Implementation Architecture") carries explicit metadata (Status: Initial Baseline, Architecture
Version 0.1, Method Baseline GG-SAD 1.2, Last Updated 2026-08-02) and slightly more detail (13
architectural decisions requiring ADRs, explicit Repository Structure tree, explicit Actor
table). `docs/architecture-reference.md` ("GG-SAD Reference Architecture") has no metadata block
and organizes practice/testing profile packages slightly differently. These are near-duplicate
variants of the same project document — flagged in `INGEST-CONFLICTS.md`. Both describe candidate
product architecture for the GG-SAD reference engine, which the transition SPEC also flags as
historical material whose conclusions assumed the prior GG-SAD/GSD combination model.

## GG-SAD Project Constitution

- source: docs/constitution.md

Version 0.2 (Last Updated 2026-08-03), `Status: Active`. Defines a document-precedence order
identical in structure to the normative SPEC's (constitution → accepted ADRs → project-brief →
architecture → scoped decisions → change spec → plan → tasks → implementation/tests → evidence/
GSD `.planning/` artifacts), an invariant GG-SAD core, goal/scope control rules, gate-controlled
flow (DoF→DoW→DoD→DoR), evidence/traceability rules, a Pair Review section matching the SPEC,
Human Approval Boundaries (constitutional changes, ADR changes, scope changes, breaking changes,
control-weakening, destructive actions, deviations, stable releases all require explicit human
approval), Engineering Quality baseline (`uv sync`, `ruff format --check`, `ruff check`, `ty
check`, `pytest`, `uv build` — note: without `--locked`, differing from the transition SPEC's
`uv sync --locked`), Testing Rules, Security/Repository Safety rules, Tool/Integration
Independence, a dedicated **"GSD Companion Rules"** section (§15) stating GSD is "the initial
execution companion," `.planning/` is "subordinate," and "GSD MUST NOT approve specifications or
transitions" — **this framing is the one the higher-precedence transition SPEC explicitly
reverses** (see `INGEST-CONFLICTS.md`) — Documentation Rules, Anti-Overhead Rules, Change/Release
Discipline, and a formal Amendment Process.

## Project-Wide Gate Definitions (Definition of Done / Fail / Ready / Wait)

- source: docs/definitions/definition-of-done.md
- source: docs/definitions/definition-of-fail.md
- source: docs/definitions/definition-of-ready.md
- source: docs/definitions/definition-of-wait.md

Detailed, project-facing elaborations of the four gates summarized at method level in
`docs/method/GG-SAD_normative_method_specification.md` §9–12 (see `constraints.md`). Definition
of Done covers per-phase completion criteria for Intake, Explore/Decide, Specification, Plan,
Design/Architecture, Build, Verify, Pair Review, Release Readiness, Release, and Closure, plus a
Python quality baseline identical to the constitution's (`uv sync` without `--locked`). Definition
of Fail defines 13 failure categories (e.g. `FAILED_POLICY_VIOLATION`, `FAILED_SECURITY`,
`FAILED_DATA_LOSS`, `FAILED_UNAUTHORIZED_BREAKING_CHANGE`), general fail triggers, required
failure-rule fields, immediate agent behavior on DoF, the recoverable-error-vs-failure
distinction, mandatory failure scenarios (constitutional/ADR violation, security incident, data
loss, unrecoverable migration, fabricated evidence), and restart-after-failure rules. Definition
of Ready defines per-phase readiness criteria (Intake through Close) and Class/Profile tailoring
notes (Class S may use inline spec; Class L requires stronger readiness). Definition of Wait
defines nine wait categories, required wait-record fields (with a fuller YAML template than the
method-level SPEC), agent behavior in wait, safe-state requirements, resume rules, and the
"wait is not failure" distinction.

## GG-SAD Implementation Guide and Implementation Roadmap

- source: docs/implementation-guide.md
- source: docs/implementation-roadmap.md

The Implementation Guide is a detailed recommended-approach document: an 8-stage implementation
strategy (method core/project brief → compliance profiles → pilots → validation/state engine →
agent workflows → CI → companion adapters → memory), a full recommended repository structure
(`.ggsad/`, `docs/`, `specs/`, `src/`, `tests/`, `tools/ggsad/`), document hierarchy, project-wide
document responsibilities, workflow tailoring (`Invariant Core → Compliance Profile → Project
Overrides → Change Class → Local Strengthening → Companion Mapping`), three change classes (S/M/L
with differing required artifacts), state model (7 phases, 8 status values, 8 transition
actions), gate model detail, a `state.yaml` example, minimal templates for every artifact type, a
CLI command surface (`ggsad init/profile/map/new/status/validate/evaluate/transition/resume/
close/memory`), agent-workflow permission examples, Pair Review implementation detail (including
a recommended `pair_review:`/finding YAML model), Practice Profiles and Combination Recipes
(Testing Strategy, Architecture Practice, Security Practice, Discovery/Product Practice
profiles), companion-method integration mapping-contract format, project memory record format,
CI integration guidance, technology recommendation, 21 anti-overhead rules, a Minimum Viable
Implementation content list, and 23 acceptance criteria for pilot readiness.

The Implementation Roadmap (`docs/implementation-roadmap.md`, distinct file from
`docs/roadmap.md` below, both titled "GG-SAD Implementation Roadmap") lays out Phase 0 (Method
Baseline) through Phase 10 (GG-SAD Project Memory), Open Topics (Dual-Track Development, Delivery
Models), Deferred-by-Default items, and Suggested Release Milestones v0.1 through v1.0 with
explicit Definition of Ready/Done for v1.0. **This document and `docs/roadmap.md` describe
overlapping but structurally different roadmap content under the same title** — flagged in
`INGEST-CONFLICTS.md`.

## Project Brief

- source: docs/project-brief.md

`Status: active`, Last Updated 2026-08-02. Describes the GG-SAD Reference Implementation project:
problem/opportunity (fragmented governance across chat sessions and tool-specific workflows for
AI-assisted development), target users/stakeholders table, desired outcomes/success signals,
project type (greenfield, single-repository, pre-alpha), scope/non-goals, constraints
(Python/Markdown/YAML/JSON Schema/Git-portable, CLI-first, Python 3.12+), **Compliance Profile:
standard**, **GG-SAD Operating Mode: combination** ("GG-SAD is the governing method for this
repository. It owns goals, specification authority, state, gates, precedence, approvals, evidence
requirements, and closure.") — **this framing is the one the higher-precedence transition SPEC
explicitly reverses** (see `INGEST-CONFLICTS.md`) — an Integrated Methods/Tools table (GSD Core,
Claude Code, Codex/Human Reviewer, Git, GitHub Actions), Enabled Practices, Pair Review Policy,
Product/Delivery Assumptions, a Key Risks table, and Open Decisions (including the `ty`
strict-mode adoption noted as superseding `mypy`, dated 2026-08-03).

## Roadmap (project status document)

- source: docs/roadmap.md

`Status: Active`, Method Baseline GG-SAD 1.2, Last Updated 2026-08-04. Distinct in structure from
`docs/implementation-roadmap.md` (uses `Now`/`Next`/`Later`/`Open` horizons with R0–R14 items
rather than Phase 0–10). Contains **live status entries** not present in the Implementation
Roadmap: R0 (Repository Bootstrap) marked "**Complete**" as of 2026-08-04, citing
`CHG-001-reference-repository-bootstrap` reaching Build-Done and Verify-Done with a completed
Pair Review (`agent:codex`) and zero open blocking findings; R1 (Reference Repository and Manual
Flow) marked "**Partially delivered**" with an explicit accounting of what CHG-001 did and did
not cover; R2 (Initial Vertical CLI Slice) marked "**Delivered**" with a noted pre-existing scope
gap (`ggsad status` was never in CHG-001's approved scope). R3–R8 ("Next") and R9–R14 ("Later")
remain undelivered roadmap items (State/Transition Engine, Profile Resolver, Document Validator,
Gate Engine, Evidence/Traceability, Pair Review Engine, Agent Workflows, CI Integration,
Companion Methods, Optional Integrations, Project Memory, Stable 1.0). This document is the
authoritative record of what the legacy GG-SAD-governed CHG-001 change actually delivered,
independent of whether its governance framing remains active going forward.

## CHG-001 — Reference Repository Bootstrap (legacy change spec)

- source: specs/CHG-001-reference-repository-bootstrap/spec.md

Class M change, `Phase: specify`, `Status: ready` (per the document's own Metadata block — see
also Finding F-06 in the design-review findings, noting this phase value never advanced past
`specify` in `state.yaml` despite Build/Verify-Done evidence and a full Pair Review cycle
recorded elsewhere, which the transition design cites as a concrete instance of the ambiguous
state narrative it sets out to fix). Requestor: human:project-owner; Implementation Requestor:
agent:claude-code; Reviewer: agent:codex; Approver: human:project-owner. Goal: initialize a
GG-SAD project, create a Class M change, validate config/state, perform one controlled
`draft → ready` transition, and produce actionable errors — "the smallest useful vertical slice
of GG-SAD automation." Explicit non-goals: full gate engine, automatic evidence evaluation, CI
integration, project memory, MCP, web UI, issue-tracker sync, multi-agent orchestration, release
automation, database-backed state, semantic index, 1.0 compatibility guarantees. Contains 20
formal requirements (R-001–R-020) and 15 acceptance examples (E-001–E-015) — see `requirements.md`
for why these are not extracted as REQ- entries. Architecture/ADR Constraints section records
that ADR-0001–0008 were dispositioned (2026-08-02, human:project-owner) as "non-blocking drafts
for CHG-001" — their individual `Status: Proposed` was left unchanged; this only removed them as
a Ready-to-Build blocker for CHG-001 specifically. Change History shows the spec was approved
2026-08-02 and transitioned to `ready` 2026-08-03, with a noted `ty` (Astral) strict-mode
adoption decision recorded the same day (PRF-003 disposition, also reflected in
`docs/project-brief.md`'s Open Decisions and `docs/constitution.md` v0.2).

## Standard Product, Development, and Open Source Workflow

- source: docs/workflow-reference.md

`WORKFLOW.md`, GG-SAD v1.2 baseline. A 22-phase integrated lifecycle reference spanning product
discovery (Ideation → Discovery → Opportunity Validation → Product Strategy → Product Definition),
OSS Foundation/Governance, the GG-SAD development workflow (Intake → Explore/Decide → Specify →
Plan → Design & Architecture → Build → Verify), Release (Release Readiness → Release & Publication
→ Adoption & Enablement), and Operation/Evolution/Retirement (Operate & Support → Measure & Learn
→ Maintain & Evolve → Deprecate → Retire → Archive). Cross-cutting sections cover Example-Driven
Specification, Pair Review, OSS community/contribution/security/license/governance management,
standard phase-gate questions (DoF/DoW/DoD/DoR), tailoring guidance by profile tier, common
shortened flows, and minimum lifecycle artifacts per level (project, change, OSS). This is a
general-purpose reference workflow document, not scoped specifically to this repository's own
development process, though it assumes the same GG-SAD gate/evidence/Pair-Review model documented
elsewhere in this ingest set.

## Example Placeholder Files

- source: specs/examples/class-s/.gitkeep
- source: specs/examples/class-l/.gitkeep

Both files exist and are empty (confirmed at read time). They preserve otherwise-empty
`specs/examples/class-s/` and `specs/examples/class-l/` directories in Git — placeholders for the
Class S and Class L example changes that `docs/implementation-roadmap.md` (Phase 1 / Phase 2) and
`docs/roadmap.md` (R1) describe as not-yet-delivered roadmap items. No content to extract.
