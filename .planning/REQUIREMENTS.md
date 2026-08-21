# Requirements: GG-SAD — Normative Clarification & Governance Transition (Milestone 1)

**Defined:** 2026-08-18
**Core Value:** The normative specification is the single leading authority; the retained implementation must be proven to conform to the *clarified* contract through audit and verification evidence, not assumed from prior completion claims.

## v1 Requirements

Eight categories, one per roadmap phase, in strict execution order. Phases 2 and 3
(owner approval, independent review) are hard gates — they MUST NOT be bundled with
other work.

### Normative Clarification (NORM)

Scope of the amendment is fixed by the approved transition design's "Normative
Specification Correction Scope" — clarification only, no implementation-behavior change.

- [x] **NORM-01**: A proposed diff to `docs/method/GG-SAD_normative_method_specification.md` separates the SPEC's own authority/applicability, method semantics, reference-implementation requirements, and optional integration guidance into distinct sections
- [x] **NORM-02**: The proposed diff defines a canonical artifact model distinguishing mandatory information from mandatory files (`state.yaml` when persistent state is used; `plan.md`/`tasks.md`/`evidence.md`/`review.md` remain conditional)
- [x] **NORM-03**: The proposed diff replaces the state narrative with an explicit transition-table contract (canonical phases/statuses, legal combinations, gate evaluation per action, cancellation/supersession/reopening/terminal behavior)
- [x] **NORM-04**: The proposed diff makes tailoring deterministic — self-approval under the `lean` profile stays subordinate to non-delegable human approval
- [x] **NORM-05**: The proposed diff defines portable Pair Review evidence fields (participant, role, reviewed revision, action, timestamp, result, findings, disposition)
- [x] **NORM-06**: The proposed diff defines a technology-neutral minimal automation contract (init, create goal-bound change, validate, evaluate/execute one controlled transition, reject invalid operations without partial mutation, emit human- and machine-readable results, record history)
- [x] **NORM-07**: The proposed diff repairs document quality — renumbers Sections 6–13, removes the German-spec reference, removes tool-local citations, labels examples clearly
- [x] **NORM-08**: No implementation file under `src/ggsad/` is modified by this phase

### Owner Approval (APPR)

- [x] **APPR-01**: The repository owner reviews the exact proposed normative diff (NORM-01–07) and records explicit approval, or specific requested changes, before the diff is treated as final
- [x] **APPR-02**: If the owner requests changes, the diff is revised and re-submitted for approval before proceeding to REVIEW

### Independent Review (REVIEW)

- [x] **REVIEW-01**: An independent Claude Code review — not a fresh context or subagent of the Requestor who authored the diff — evaluates the owner-approved normative diff
- [x] **REVIEW-02**: Review findings are returned with stable IDs, severity, and exact references, per the Pair Review model's evidence requirements
- [x] **REVIEW-03**: All blocking findings are resolved (fixed or explicitly dispositioned by the owner) before the diff is treated as final and merged

### Legacy Governance Retirement (RETIRE)

Scope is the full DOC-classified corpus catalogued in `.planning/intel/context.md` that
currently frames GG-SAD as governing this repository's own development.

- [x] **RETIRE-01**: Every legacy development-governance artifact identified in `.planning/intel/context.md` (`docs/constitution.md`, `docs/project-brief.md`, `docs/architecture.md`, `docs/architecture-reference.md`, `docs/roadmap.md`, `docs/implementation-roadmap.md`, `docs/adr/ADR-0001`–`0008`, `docs/workflow-reference.md`, `CLAUDE_CODE_PROJECT_START.md`, `docs/method/GG-SAD_normative_method_specification_DE.md`, `specs/CHG-001-reference-repository-bootstrap/` state and evidence) is classified as retained, retired, archived, or rewritten
- [x] **RETIRE-02**: The two near-duplicate architecture documents (`docs/architecture.md` vs. `docs/architecture-reference.md`) receive an explicit disposition (one canonical, merged, or both retired) rather than being left as an unresolved duplicate pair
- [x] **RETIRE-03**: The two competing "GG-SAD Implementation Roadmap" documents (`docs/implementation-roadmap.md` vs. `docs/roadmap.md`) receive an explicit disposition, preserving `docs/roadmap.md`'s live delivery-status content for the historical record
- [x] **RETIRE-04**: Retired or archived artifacts are moved outside the active GSD-governed workflow (not silently deleted) and are no longer read as active development governance by any agent instruction file
- [x] **RETIRE-05**: `specs/CHG-*` state and evidence are explicitly marked historical — not promoted, referenced, or restated as current governance or proof of conformance anywhere in the retained document set

### Quality-Tool Ownership Boundaries (TOOL)

- [x] **TOOL-01**: Product quality-tool scope (ruff, ty, pytest/coverage) is explicitly configured to include product code, tests, and owned scripts
- [x] **TOOL-02**: Product quality-tool scope explicitly excludes installer-owned GSD runtime files (`.claude/gsd-core/`, `.claude/hooks/`, etc.) — they are development tooling, not Python product source
- [x] **TOOL-03**: The documented baseline command is `uv sync --locked` (not bare `uv sync`), reconciling the discrepancy between `AGENTS.md`/the transition SPEC and the legacy `docs/constitution.md` §11 / `docs/definitions/definition-of-done.md` wording
- [x] **TOOL-04**: The `ty` strict-mode baseline (not `mypy`) is the sole documented type-checker across all retained governing documents, closing the tooling-drift concern already logged in `.planning/codebase/CONCERNS.md`

### Implementation Conformance Audit (AUDIT)

- [x] **AUDIT-01**: Every component of the retained implementation (`src/ggsad/application/`, `src/ggsad/engine/`, `src/ggsad/validators/`, `src/ggsad/models/`, `src/ggsad/resources/`, `src/ggsad/cli.py`) is evaluated against the *clarified* normative contract from NORM-01–07 — not against prior GG-SAD/CHG-001 completion evidence
- [x] **AUDIT-02**: The audit explicitly re-evaluates each item already catalogued in `.planning/codebase/CONCERNS.md` (tech debt, known limitations, fragile areas, security considerations, test-coverage gaps) for continued relevance and severity under the clarified contract
- [x] **AUDIT-03**: The audit produces a written list of evidenced conformance gaps — each with an exact file/requirement reference — or an explicit statement that none exist

### Gap Remediation (GAP)

- [x] **GAP-01**: Only conformance gaps evidenced by AUDIT-03 are implemented; no speculative, unrelated, or "clean up while I'm here" changes are made
- [x] **GAP-02**: Each implemented gap fix has corresponding automated test coverage

### Full Verification (VERIFY)

- [ ] **VERIFY-01**: The complete verification baseline runs clean and its output is captured as evidence: `uv sync --locked`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check src tests`, `uv run pytest`, `uv build`
- [ ] **VERIFY-02**: GSD verification results for this milestone are recorded per GSD's own evidence conventions (not a GG-SAD `evidence.md`)

## v2 Requirements (Deferred, Explicit Non-Goals for This Milestone)

Per the approved transition design's own non-goal list — potential future milestone
scope, not tracked further here:

### Deferred Capability

- **DEFER-01**: Profile resolution (inheritance, effective-workflow reporting)
- **DEFER-02**: A full gate engine (DoR/DoD/DoW/DoF automated evaluation beyond the current `specify/draft`→`specify/ready` transition)
- **DEFER-03**: GG-SAD project memory (Decision/Learning/Failure/Definition/External Source records)
- **DEFER-04**: MCP integration
- **DEFER-05**: A web UI
- **DEFER-06**: CI integration
- **DEFER-07**: Multi-agent orchestration

## Out of Scope

| Feature / Action | Reason |
|---|---|
| Building profile resolution, a full gate engine, memory, MCP, a web UI, CI integration, or multi-agent orchestration | Explicit non-goal of the approved transition design |
| Preserving prior roadmap ordering or `specs/CHG-*` change-closure claims | `specs/CHG-*` and legacy roadmap/status docs are not active development governance |
| Using GG-SAD and GSD simultaneously as development methods for this repository | GSD Core 1.10.0 is the sole development method (explicit non-goal) |
| Rewriting passing implementation code solely for a clean history | Explicit non-goal of the approved transition design |
| Treating prior GG-SAD/CHG-001 completion evidence as proof of current conformance | Retain-versus-rewrite rule: historical context only, not proof |
| Modifying product or normative files during `.planning/` initialization | Explicit instruction for this bootstrap step |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| NORM-01 … NORM-08 | Phase 1 | Pending |
| APPR-01, APPR-02 | Phase 2 | Complete |
| REVIEW-01 … REVIEW-03 | Phase 3 | Complete |
| RETIRE-01 … RETIRE-05 | Phase 4 | Complete |
| TOOL-01 … TOOL-04 | Phase 5 | Complete |
| AUDIT-01 … AUDIT-03 | Phase 6 | Pending |
| GAP-01, GAP-02 | Phase 7 | Pending |
| VERIFY-01, VERIFY-02 | Phase 8 | Pending |

**Coverage:**

- v1 requirements: 29 total (NORM 8, APPR 2, REVIEW 3, RETIRE 5, TOOL 4, AUDIT 3, GAP 2, VERIFY 2)
- Mapped to phases: 29
- Unmapped: 0 ✓

---
*Requirements defined: 2026-08-18*
*Last updated: 2026-08-18 — corrected Coverage count (29 total, was misstated as 33; the requirement-ID list and phase mappings above were already accurate)*
