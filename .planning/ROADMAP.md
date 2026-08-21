# Roadmap: GG-SAD — Normative Clarification & Governance Transition (Milestone 1)

## Overview

This milestone completes the GG-SAD transition design's 13-step sequence (steps 6–13,
following steps 1–5 already committed: design approval, bootstrap plan, GSD Core 1.10.0
pin, AGENTS.md/CLAUDE.md replacement, GSD onboarding). It clarifies the normative
specification without changing implementation behavior, gates that clarification behind
two independent hard checkpoints (explicit repository-owner approval, then a structurally
independent Claude Code review), retires or relocates the legacy development-governance
corpus that still frames GG-SAD as governing this repository's own development, corrects
quality-tool ownership boundaries, audits the retained `src/ggsad/` implementation against
the *clarified* contract (not prior completion evidence), remediates only evidenced gaps,
and closes with a clean full verification baseline captured as evidence.

**Structure mode:** Horizontal Layers — a sequential governance/audit process with hard
approval gates, not iterative user-facing feature slices. Each phase is a layer the next
phase depends on; none are independently shippable vertical slices.

**Execution settings (from config.json):** sequential, non-parallel execution
(`parallelization: false`); manual/interactive phase advancement with explicit
confirmation at each gate (`mode: interactive`, `auto_advance: false`); no autonomous
execution. Phases 2 (Owner Approval) and 3 (Independent Review) are hard gates — they
MUST NOT be bundled with any other phase's work and MUST NOT be skipped or merged.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED) — none in this milestone

- [x] **Phase 1: Normative Clarification** - Produce a proposed diff to the normative spec that clarifies scope without changing implementation behavior (completed 2026-08-19)
- [x] **Phase 2: Owner Approval** - Repository owner reviews and explicitly approves (or requests changes to) the exact Phase 1 diff — hard gate (completed 2026-08-19)
- [x] **Phase 3: Independent Review** - Structurally independent Claude Code review evaluates the owner-approved diff; blocking findings resolved — hard gate (completed 2026-08-20)
- [x] **Phase 4: Legacy Governance Retirement** - Classify and disposition every legacy development-governance artifact; retire/relocate without silent deletion (completed 2026-08-20)
- [x] **Phase 5: Quality-Tool Ownership Boundaries** - Scope product quality tooling correctly and standardize commands/type-checker across retained docs (completed 2026-08-21)
- [x] **Phase 6: Implementation Conformance Audit** - Audit `src/ggsad/` against the clarified contract and produce an evidenced gap list
- [x] **Phase 7: Gap Remediation** - Implement only evidenced conformance gaps, each with test coverage
- [ ] **Phase 8: Full Verification** - Run the complete verification baseline clean and record evidence

## Phase Details

### Phase 1: Normative Clarification

**Goal**: Produce a proposed diff to `docs/method/GG-SAD_normative_method_specification.md`
that clarifies SPEC authority/applicability, the canonical artifact model, the state
transition-table contract, deterministic tailoring, portable Pair Review evidence fields,
a technology-neutral minimal automation contract, and document quality — all without
changing implementation behavior. No file under `src/ggsad/` is touched in this phase.
**Depends on**: Nothing (first phase)
**Requirements**: NORM-01, NORM-02, NORM-03, NORM-04, NORM-05, NORM-06, NORM-07, NORM-08
**Success Criteria** (what must be TRUE):

  1. A proposed diff exists that separates the SPEC's own authority/applicability, method semantics, reference-implementation requirements, and optional integration guidance into distinct sections (NORM-01)
  2. The diff defines a canonical artifact model distinguishing mandatory information from mandatory files, with `state.yaml` mandatory only when persistent state is used (NORM-02)
  3. The diff replaces the state narrative with an explicit transition-table contract covering canonical phases/statuses, legal combinations, gate evaluation per action, and cancellation/supersession/reopening/terminal behavior (NORM-03)
  4. The diff makes tailoring deterministic (self-approval under `lean` stays subordinate to non-delegable human approval), defines portable Pair Review evidence fields, and defines a technology-neutral minimal automation contract (NORM-04, NORM-05, NORM-06)
  5. The diff repairs document quality: Sections 6–13 renumbered, the German-spec reference removed, tool-local citations removed, examples clearly labeled (NORM-07)
  6. No file under `src/ggsad/` is modified as part of producing this diff (NORM-08)

**Plans**: 3/3 plans executed
Plans:

- [x] 01-01-PLAN.md — Phase 1 pre-execution baseline (F-01) + Section 1.1 document category map (NORM-01) + Section 4.3 canonical artifact model (NORM-02)
- [x] 01-02-PLAN.md — Section 8 transition-table contract + Section 20 fix (NORM-03) + Section 5.4 non-delegable approval (NORM-04) + Section 14.5 portable Pair Review evidence fields (NORM-05)
- [x] 01-03-PLAN.md — Section 22 minimal automation contract (NORM-06) + Sections 6/7/9-13 renumbering + Section 14.2 tool-citation cleanup (NORM-07) + baseline-anchored phase-closing NORM-08 verification

### Phase 2: Owner Approval

**Goal**: The repository owner reviews the exact proposed normative diff from Phase 1 and
records explicit approval, or specific requested changes, before the diff is treated as
final. This is a hard gate — it cannot complete without the owner's explicit recorded
approval of the diff exactly as it will be merged, and it MUST NOT be bundled with any
other phase's work.
**Depends on**: Phase 1
**Requirements**: APPR-01, APPR-02
**Success Criteria** (what must be TRUE):

  1. The repository owner has reviewed the exact diff produced in Phase 1 (APPR-01)
  2. The owner has recorded explicit approval, or specific requested changes, before the diff is treated as final (APPR-01)
  3. If changes were requested, the diff was revised and re-submitted for owner approval, and that re-approval was obtained, before this phase closes (APPR-02)
  4. This phase does not close until an explicit recorded owner approval exists for the diff exactly as it will be merged

**Plans**: 0/1 plans executed

Plans:

- [x] 02-01-PLAN.md — Apply SF-01–SF-08 corrections, verify the corrected exact diff, and obtain explicit owner approval

### Phase 3: Independent Review

**Goal**: A structurally independent Claude Code review — explicitly not a fresh context
or subagent of whoever authored the Phase 1 diff — evaluates the owner-approved diff and
returns findings with stable IDs, severity, and exact references. All blocking findings
are resolved or explicitly dispositioned by the owner before this phase closes. This is a
hard gate — independence must be structurally real, not a fresh-context relabeling of the
same Requestor, and this phase MUST NOT be bundled with any other phase's work.
**Depends on**: Phase 2
**Requirements**: REVIEW-01, REVIEW-02, REVIEW-03
**Success Criteria** (what must be TRUE):

  1. An independent Claude Code review — structurally distinct from the Phase 1 diff's author, not a fresh context or subagent of that Requestor — evaluates the owner-approved diff (REVIEW-01)
  2. Review findings are returned with stable IDs, severity, and exact references, per the Pair Review model's evidence requirements (REVIEW-02)
  3. All blocking findings are resolved (fixed) or explicitly dispositioned by the owner before the diff is treated as final and merged (REVIEW-03)

**Plans**: 0/1 plans executed

Plans:

- [x] 03-01-PLAN.md — Resolve PR-01–PR-03, obtain exact-diff owner approval, and complete independent Claude follow-up review

### Phase 4: Legacy Governance Retirement

**Goal**: Classify every legacy development-governance artifact catalogued in
`.planning/intel/context.md` as retained, retired, archived, or rewritten; explicitly
disposition the two near-duplicate architecture docs and the two competing roadmap docs;
move retired/archived artifacts outside the active GSD-governed workflow without silent
deletion.
**Depends on**: Phase 3
**Requirements**: RETIRE-01, RETIRE-02, RETIRE-03, RETIRE-04, RETIRE-05
**Success Criteria** (what must be TRUE):

  1. Every legacy artifact identified in `.planning/intel/context.md` (`docs/constitution.md`, `docs/project-brief.md`, `docs/architecture.md`, `docs/architecture-reference.md`, `docs/roadmap.md`, `docs/implementation-roadmap.md`, `docs/adr/ADR-0001`–`0008`, `docs/workflow-reference.md`, `CLAUDE_CODE_PROJECT_START.md`, the German normative spec, `specs/CHG-001-reference-repository-bootstrap/` state and evidence) is classified as retained, retired, archived, or rewritten (RETIRE-01)
  2. `docs/architecture.md` vs. `docs/architecture-reference.md` receives an explicit disposition — one canonical, merged, or both retired — rather than remaining an unresolved duplicate pair (RETIRE-02)
  3. `docs/implementation-roadmap.md` vs. `docs/roadmap.md` receives an explicit disposition, preserving `docs/roadmap.md`'s live delivery-status content for the historical record (RETIRE-03)
  4. Retired or archived artifacts are moved outside the active GSD-governed workflow (not silently deleted) and are no longer read as active development governance by any agent instruction file (RETIRE-04)
  5. `specs/CHG-*` state and evidence are explicitly marked historical — not promoted, referenced, or restated as current governance or proof of conformance anywhere in the retained document set (RETIRE-05)

**Plans**: 0/1 plans executed

Plans:

- [x] 04-01-PLAN.md — Decouple CHG-001 tests, archive 28 legacy files with a 29-entry manifest, rewrite README, and verify retirement scope

### Phase 5: Quality-Tool Ownership Boundaries

**Goal**: Explicitly scope product quality tooling (ruff, ty, pytest/coverage) to product
code, tests, and owned scripts; explicitly exclude installer-owned GSD runtime files;
standardize on `uv sync --locked` and `ty` strict mode across every retained governing
document.
**Depends on**: Phase 4
**Requirements**: TOOL-01, TOOL-02, TOOL-03, TOOL-04
**Success Criteria** (what must be TRUE):

  1. Product quality-tool scope (ruff, ty, pytest/coverage) is explicitly configured to include product code, tests, and owned scripts (TOOL-01)
  2. Product quality-tool scope explicitly excludes installer-owned GSD runtime files (`.claude/gsd-core/`, `.claude/hooks/`, etc.) as development tooling, not Python product source (TOOL-02)
  3. `uv sync --locked` (not bare `uv sync`) is the sole documented baseline command across every retained governing document (TOOL-03)
  4. `ty` strict mode (not `mypy`) is the sole documented type-checker across every retained governing document, closing the tooling-drift concern logged in `.planning/codebase/CONCERNS.md` (TOOL-04)

**Plans**: 1 plan

Plans:

- [x] 05-01-PLAN.md — Align quality-tool ownership configuration, synchronize active baseline commands, and verify TOOL-01 through TOOL-04

### Phase 6: Implementation Conformance Audit

**Goal**: Audit every component of `src/ggsad/` against the *clarified* normative contract
from Phase 1 — not against prior GG-SAD/CHG-001 completion evidence — re-evaluate every
item already catalogued in `.planning/codebase/CONCERNS.md` for continued relevance, and
produce a written list of evidenced conformance gaps (or state explicitly that none
exist).
**Depends on**: Phase 5
**Requirements**: AUDIT-01, AUDIT-02, AUDIT-03
**Success Criteria** (what must be TRUE):

  1. Every component of the retained implementation (`src/ggsad/application/`, `src/ggsad/engine/`, `src/ggsad/validators/`, `src/ggsad/models/`, `src/ggsad/resources/`, `src/ggsad/cli.py`) is evaluated against the clarified normative contract from Phase 1 — not against prior GG-SAD/CHG-001 completion evidence (AUDIT-01)
  2. Each item already catalogued in `.planning/codebase/CONCERNS.md` (tech debt, known limitations, fragile areas, security considerations, test-coverage gaps) is re-evaluated for continued relevance and severity under the clarified contract (AUDIT-02)
  3. A written list of evidenced conformance gaps exists, each with an exact file/requirement reference, or an explicit statement that none exist (AUDIT-03)

**Plans**: TBD

### Phase 7: Gap Remediation

**Goal**: Implement only the conformance gaps evidenced in Phase 6, each with
corresponding test coverage. If Phase 6 finds zero gaps, this phase's scope is to record
that explicitly and close without code changes.
**Depends on**: Phase 6
**Requirements**: GAP-01, GAP-02
**Success Criteria** (what must be TRUE):

  1. Only conformance gaps evidenced by Phase 6's AUDIT-03 list are implemented — no speculative, unrelated, or "clean up while I'm here" changes (GAP-01)
  2. Each implemented gap fix has corresponding automated test coverage (GAP-02)
  3. If Phase 6 found zero gaps, that is explicitly recorded and this phase closes without code changes

**Plans**: TBD

### Phase 8: Full Verification

**Goal**: Run the complete verification baseline (`uv sync --locked`,
`uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check src tests`, `uv run pytest`,
`uv build`) clean, capture its output as evidence, and record GSD verification results for
this milestone.
**Depends on**: Phase 7
**Requirements**: VERIFY-01, VERIFY-02
**Success Criteria** (what must be TRUE):

  1. `uv sync --locked` runs clean (VERIFY-01)
  2. `uv run ruff format --check .`, `uv run ruff check .`, and `uv run ty check src tests` all run clean (VERIFY-01)
  3. `uv run pytest` and `uv build` both run clean (VERIFY-01)
  4. The full command output is captured as evidence, and GSD verification results for this milestone are recorded per GSD's own evidence conventions — not a GG-SAD `evidence.md` (VERIFY-02)

**Plans**: TBD

## Progress

**Execution Order:**
Phases execute strictly in order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Phases 2 and 3 are hard
gates and are never merged with adjacent phases. Manual, interactive advancement only —
no autonomous or parallel execution.

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Normative Clarification | 3/3 | Complete    | 2026-08-19 |
| 2. Owner Approval | 1/1 | Complete    | 2026-08-19 |
| 3. Independent Review | 1/1 | Complete    | 2026-08-20 |
| 4. Legacy Governance Retirement | 1/1 | Complete    | 2026-08-20 |
| 5. Quality-Tool Ownership Boundaries | 1/1 | Complete    | 2026-08-21 |
| 6. Implementation Conformance Audit | 1/1 | Complete | 2026-08-21 |
| 7. Gap Remediation | 1/1 | Complete | 2026-08-21 |
| 8. Full Verification | 0/TBD | Not started | - |
