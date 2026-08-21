# GG-SAD — Normative Clarification & Governance Transition (Milestone 1)

## What This Is

GG-SAD (Goal-Gated Spec-Anchored Development) is a lightweight, goal-oriented,
specification-driven development method, with this repository serving as both its
normative method specification's home and its Python reference implementation
(`src/ggsad/`, Typer CLI: `init`/`new`/`validate`/`transition`). As of this milestone,
the repository is developed under **GSD Core 1.10.0** as its sole development method —
GG-SAD is the product being implemented here, it does not govern the development of
this repository.

## Core Value

`docs/method/GG-SAD_normative_method_specification.md` (English) is the single leading
authority for GG-SAD method semantics and reference-implementation behavior. The
retained Python implementation must be proven to conform to the *clarified* contract
through explicit audit and verification evidence — not assumed to conform because prior
GG-SAD/CHG-001 completion evidence claims it does.

## Requirements

### Validated

- ✓ GSD Core 1.10.0 pinned as the sole development method for this repository — transition steps 1–5 (design approval, bootstrap plan, GSD pin, AGENTS.md/CLAUDE.md replacement, GSD onboarding), evidenced by commits `800a004`…`8642fbb`

### Active

See `.planning/REQUIREMENTS.md` for the full v1 requirement set (NORM, APPR, REVIEW,
RETIRE, TOOL, AUDIT, GAP, VERIFY categories — one per roadmap phase).

- [ ] Clarify the normative specification without changing implementation behavior
- [ ] Obtain explicit repository-owner approval of the exact normative diff
- [ ] Obtain independent Claude Code review and resolve blocking findings
- [ ] Classify and retire/relocate remaining conflicting legacy development-governance artifacts
- [ ] Correct quality-tool ownership boundaries (product code vs. installer-owned GSD tooling)
- [ ] Audit the retained implementation against the clarified normative contract
- [ ] Implement only evidenced conformance gaps
- [ ] Run the complete verification baseline and record GSD verification results

### Out of Scope

- Profile resolution — explicit non-goal of the approved transition design
- A full gate engine — explicit non-goal
- GG-SAD project memory — explicit non-goal
- MCP integration — explicit non-goal
- A web UI — explicit non-goal
- CI integration — explicit non-goal
- Multi-agent orchestration — explicit non-goal
- Preserving prior roadmap ordering or change-closure claims — `specs/CHG-*` and legacy roadmap/status docs are not active development governance
- Using GG-SAD and GSD simultaneously as development methods for this repository — GSD Core is the sole development method (non-goal, explicit)
- Rewriting passing implementation code solely for a clean history — explicit non-goal
- Promoting historical `specs/CHG-*` state or prior GG-SAD completion evidence as proof of current conformance — historical context only, per the retain-versus-rewrite rule

## Context

- **Governing documents for this ingest (binding precedence):** `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md` (precedence 1, governs the transition process) and `docs/method/GG-SAD_normative_method_specification.md` (precedence 0, governs GG-SAD method semantics and remains superior in the hierarchy it itself defines). No content contradiction exists between them — the design document explicitly subordinates itself to the normative specification.
- **Derived context available:** `.planning/codebase/` (ARCHITECTURE.md, STACK.md, STRUCTURE.md, CONVENTIONS.md, INTEGRATIONS.md, TESTING.md, CONCERNS.md — codebase map dated 2026-08-18) and `.planning/intel/` (SYNTHESIS.md, constraints.md, context.md, decisions.md, requirements.md, `INGEST-CONFLICTS.md` — doc-ingest synthesis of 31 classified documents, 0 blockers / 2 warnings / 3 auto-resolved info). Both are derived/reference context, not governance documents themselves.
- **Existing implementation:** `src/ggsad/` (Python 3.13, Typer CLI, Pydantic v2 models, JSON Schema validators, ruamel.yaml-based state engine) delivers `init`/`new`/`validate`/`transition` per the CHG-001 change (evidenced complete 2026-08-04). Per the retain-versus-rewrite rule, this is retained *pending* audit against the clarified contract in this milestone — prior completion evidence is historical context, not proof of conformance.
- **Known concerns already catalogued** (`.planning/codebase/CONCERNS.md`): a resolved-but-notable type-checker substitution (mypy→ty) that required amending multiple documents; two previously-found and fixed security/validation gaps (path traversal in schema-declared paths, unenforced schema-version pinning); several intentional scope gaps (phase-transition engine limited to `specify/draft`→`specify/ready`, no profile content, single GSD mapping only, limited Pair Review coverage) documented as future roadmap work, not defects of this milestone's scope.
- **Two pairs of unresolved near-duplicate legacy documents** (from `INGEST-CONFLICTS.md`, relevant to the retirement/classification phase): `docs/architecture.md` vs. `docs/architecture-reference.md` (competing reference-architecture docs); `docs/implementation-roadmap.md` vs. `docs/roadmap.md` (competing "GG-SAD Implementation Roadmap" docs, the latter carrying live delivery-status content). Neither pair declares one canonical over the other — the retirement/classification phase must produce an explicit disposition for each.
- **Quality/verification baseline commands:** `uv sync --locked`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check src tests`, `uv run pytest`, `uv build` (per `AGENTS.md` and the transition SPEC; supersedes the bare `uv sync` and `mypy` framing still present in some DOC-classified legacy sources).

## Constraints

- **Method:** GSD Core 1.10.0 (pinned) is the sole development method for this repository. GG-SAD MUST NOT be used to govern this repository's own development.
- **Normative spec changes:** Require explicit repository-owner approval of the exact diff, plus independent Claude Code review. A fresh context or subagent of the Requestor does not satisfy independence.
- **Product/normative files:** Not modified by this initialization — `.planning/` artifacts only, per explicit instruction.
- **Evidence:** Prior GG-SAD/CHG-001 completion evidence and `specs/CHG-*` state are historical context, not proof of current conformance. Retained code is retained only when it conforms to the clarified product contract and passes verification.
- **Scope:** No profile resolution, gate engine, memory, MCP, web UI, CI integration, or multi-agent orchestration in this milestone (see Out of Scope).
- **Tech stack (baseline, unchanged by this milestone):** Python 3.13, `uv`, Typer 0.27, Pydantic 2.13 (frozen models), `ruamel.yaml`, JSON Schema (Draft 2020-12), pytest 9.1 / pytest-cov / Hypothesis, Ruff 0.16, `ty` 0.0.65 (strict).
- **Execution mode:** Manual phase advancement with explicit confirmation at each gate; sequential (non-parallel, non-autonomous) execution; model tier inherited from the active session rather than pinned.
- **Commit discipline for this bootstrap:** `.planning/` artifacts are not committed during initialization. Per the approved plan, they land in a single Task 4 onboarding commit after external (independent) verification.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| GSD Core 1.10.0 pinned as sole development method | Owner-confirmed governing decision in the approved transition design | ✓ Good — committed (steps 1–5) |
| Eight fine-grained phases with owner approval and independent review as separate hard gates | Selected during onboarding from the owner-approved bootstrap plan and its hard approval/independent-review boundaries; approval/review must not be bundled with other work — each is an independent checkpoint | — Pending |
| Horizontal Layers project structure mode | Sequential governance/audit process with hard gates, not iterative user-facing feature slices | — Pending |
| Manual phase advancement, sequential execution, no autonomous/parallel implementation | Minimal-automation prototype; explicit confirmation required at each gate | — Pending |
| Research only when a phase has a genuine unresolved external fact (not blanket upfront research) | Most phases are internal governance/audit work already grounded in derived intel and codebase context | — Pending |
| Model tier inherited from configured session rather than hard-pinned | User preference | — Pending |
| `.planning/` artifacts tracked in Git, but not committed during this initialization | Approved plan requires a single Task 4 onboarding commit after external verification | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-08-18 after initialization*
