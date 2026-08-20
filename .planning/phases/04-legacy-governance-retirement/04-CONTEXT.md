# Phase 4 Context — Legacy Governance Retirement

## Status

Design approved by the repository owner on 2026-08-20. This artifact defines the boundary for Phase 4 planning and execution.

## Goal

Remove superseded GG-SAD repository-development governance from the active documentation and specification surfaces without silently deleting history. Preserve the English normative specification as the leading product authority and GSD Core 1.10.0 as this repository's sole development method.

## Selected Approach

Use a repository-local historical archive at:

```text
archive/legacy-ggsad-governance/
```

Files are moved while preserving their original relative paths beneath the archive root. A single `MANIFEST.md` records every disposition. Archived material is historical context only and has no current governing authority or evidentiary force.

Rejected approaches:

- Git-history-only deletion, because it makes discovery and classification unnecessarily difficult.
- Leaving files in their active paths with historical banners, because they remain plausible competing authorities.
- Merging or rewriting legacy architecture and roadmap documents in this phase, because that would create new architecture or roadmap scope rather than retire superseded governance.

## Archive Inventory

### Superseded repository governance

| Original path | Classification | Required archive treatment |
|---|---|---|
| `docs/constitution.md` | Superseded repository governance | Archive; no current authority |
| `docs/project-brief.md` | Superseded repository governance | Archive; combination-mode and subordinate-GSD framing is historical |
| `docs/adr/ADR-0001-use-python-for-reference-engine.md` | Proposed legacy ADR | Archive with original Proposed status preserved |
| `docs/adr/ADR-0002-use-markdown-for-governing-documents.md` | Proposed legacy ADR | Archive with original Proposed status preserved |
| `docs/adr/ADR-0003-use-yaml-for-configuration-and-state.md` | Proposed legacy ADR | Archive with original Proposed status preserved |
| `docs/adr/ADR-0004-separate-method-core-from-integrations.md` | Proposed legacy ADR | Archive with original Proposed status preserved |
| `docs/adr/ADR-0005-use-explicit-state-transition-actions.md` | Proposed legacy ADR | Archive with original Proposed status preserved |
| `docs/adr/ADR-0006-use-gsd-as-initial-execution-companion.md` | Proposed legacy ADR with superseded development-method premise | Archive; explicitly identify the reversed premise |
| `docs/adr/ADR-0007-use-one-agent-with-phase-workflows.md` | Proposed legacy ADR | Archive with original Proposed status preserved |
| `docs/adr/ADR-0008-defer-memory-mcp-web-ui-and-orchestration.md` | Proposed legacy ADR | Archive with original Proposed status preserved |
| `specs/CHG-001-reference-repository-bootstrap/spec.md` | Historical GG-SAD change evidence | Archive; not current governance or conformance proof |
| `specs/CHG-001-reference-repository-bootstrap/plan.md` | Historical GG-SAD change evidence | Archive; not current governance or conformance proof |
| `specs/CHG-001-reference-repository-bootstrap/tasks.md` | Historical GG-SAD change evidence | Archive; not current governance or conformance proof |
| `specs/CHG-001-reference-repository-bootstrap/evidence.md` | Historical GG-SAD change evidence | Archive; not current governance or conformance proof |
| `specs/CHG-001-reference-repository-bootstrap/state.yaml` | Historical GG-SAD change state | Archive; its incomplete phase progression is preserved, not repaired |
| `CLAUDE_CODE_PROJECT_START.md` | Previously retired startup governance | Record as already absent; do not recreate |

### Duplicate architecture documents

| Original path | Classification | Required archive treatment |
|---|---|---|
| `docs/architecture.md` | Superseded architecture candidate | Archive without selecting it as canonical |
| `docs/architecture-reference.md` | Superseded architecture candidate | Archive without merging it |

Both architecture documents are retired. Phase 4 creates no replacement architecture document. Phase 6 audits the implementation directly against the clarified normative specification; a future approved phase may create current architecture documentation if evidence shows it is needed.

### Competing roadmap documents

| Original path | Classification | Required archive treatment |
|---|---|---|
| `docs/implementation-roadmap.md` | Superseded aspirational roadmap | Archive intact |
| `docs/roadmap.md` | Historical delivery-status record | Archive intact and preserve its status claims as history only |

`.planning/ROADMAP.md` is the active development roadmap. Historical delivery claims in `docs/roadmap.md` are not current governance or proof of conformance.

### Stale and derived method documents

| Original path | Classification | Required archive treatment |
|---|---|---|
| `docs/method/GG-SAD_normative_method_specification_DE.md` | Unmaintained normative translation | Archive until the English baseline stabilizes and a separate translation change is approved |
| `docs/workflow-reference.md` | Superseded GG-SAD 1.2 workflow reference | Archive; its 22-phase lifecycle is not the canonical phase model |
| `docs/implementation-guide.md` | Superseded implementation guidance | Archive; do not update in place |
| `docs/definitions/definition-of-ready.md` | Derived gate elaboration | Archive; the English normative specification remains authoritative |
| `docs/definitions/definition-of-done.md` | Derived gate elaboration | Archive; includes stale development-tool wording |
| `docs/definitions/definition-of-wait.md` | Derived gate elaboration | Archive |
| `docs/definitions/definition-of-fail.md` | Derived gate elaboration | Archive |
| `docs/guides/GG-SAD_human_readable_guide.md` | Derived explanatory guide | Archive; may be recreated from a stable English normative baseline |
| `docs/guides/GG-SAD_human_readable_guide_DE.md` | Derived translated guide | Archive; may be recreated through separately approved translation work |

## Archive Manifest Contract

`archive/legacy-ggsad-governance/MANIFEST.md` must:

- identify the archive as non-authoritative historical material;
- name the English normative specification as the leading product authority;
- name `.planning/` and GSD Core 1.10.0 as the active repository-development method and state;
- record original path, archived path, classification, rationale, original status where relevant, and current authority for every inventoried artifact;
- distinguish the historical delivery record from the aspirational roadmap;
- state that both architecture documents were retired without replacement;
- state that ADR-0001 through ADR-0008 were Proposed, not accepted;
- state that CHG-001 artifacts are historical and are not conformance proof;
- record `CLAUDE_CODE_PROJECT_START.md` as already retired and absent at Phase 4 start;
- avoid changing the contents of moved historical files.

## Active README Contract

Update `README.md` so an active reader sees only the current model:

- the English normative specification is the leading source for GG-SAD product semantics;
- GSD Core 1.10.0 is this repository's sole development method;
- `.planning/` owns current development requirements, roadmap, state, plans, and verification;
- legacy GG-SAD change state, constitution, project brief, architecture, ADRs, and roadmaps are not active repository governance;
- the archive manifest is linked only for historical context;
- current product usage and CLI documentation are preserved where accurate;
- references that instruct contributors or agents to read archived governance are removed;
- claims that GSD is subordinate to GG-SAD for this repository's development are removed;
- CHG-001 is not presented as the current project status or as conformance proof;
- the repository tree reflects the active normative document, GSD planning, archive, implementation, and tests.

The existing Document Hierarchy and Project Status and Initial Scope sections require replacement, not isolated reference deletion. Their replacements must point readers to `AGENTS.md` for repository authority rules and `.planning/` for current development requirements, roadmap, state, plans, and verification. The overview, repository tree, compliance/contributing guidance, and every other repeated occurrence of the legacy hierarchy or CHG-001-as-current framing must be aligned in the same rewrite.

This phase does not turn README into a second normative specification. It references authoritative sources instead of duplicating their rules.

## Test-Fixture Decoupling

`tests/integration/test_governed_artifact_validation.py` currently reads CHG-001's historical `state.yaml` from its active `specs/` path in two tests. Phase 4 must remove that dependency.

Create a dedicated minimal valid state fixture under `tests/fixtures/governed_artifacts/`. The fixture must be written as test data against the current state schema, not copied or described as CHG-001 evidence. Update the module docstring, the two tests, and their names/comments so they validate:

- a representative state fixture is schema-valid and model-parseable;
- an unsupported state schema version is rejected.

The tests must not read from `archive/` and must not cite CHG-001 as current repository evidence.

## Explicitly Retained Active Artifacts

- `docs/method/GG-SAD_normative_method_specification.md` — leading product authority.
- `AGENTS.md` and `CLAUDE.md` — current agent instructions.
- `.planning/` — GSD development state and evidence.
- `.ggsad/`, `src/ggsad/`, product schemas, product templates, product mappings, and examples — retained for later quality-boundary and conformance phases.
- `README.md` — retained but rewritten to the current authority and development-method model.
- `THIRD_PARTY_NOTICES.md`, packaging metadata, and license files.

References to standard GG-SAD paths inside the normative specification, product templates, mappings, or examples describe product behavior for GG-SAD-managed consumer projects. They are not declarations that this repository uses those artifacts for development governance and are not changed in Phase 4.

Installer-owned `.claude/gsd-core/`, hooks, and skill references are not modified.

## Scope Boundaries

Phase 4 may change only:

- archive moves and `archive/legacy-ggsad-governance/MANIFEST.md`;
- `README.md`;
- the dedicated state test fixture;
- `tests/integration/test_governed_artifact_validation.py`;
- Phase 4 `.planning/` artifacts.

Phase 4 must not change:

- the English normative specification;
- product implementation under `src/ggsad/`;
- `.ggsad/` schemas, templates, profiles, or mappings;
- installer-owned GSD files;
- unrelated tests or documentation;
- historical file contents while moving them.

## Verification Contract

Completion evidence must prove:

1. all 29 inventoried dispositions are represented: 28 archived files plus the already-absent `CLAUDE_CODE_PROJECT_START.md`;
2. every archived file retains byte-identical content at its archive destination;
3. no archived file remains at its original active path;
4. `README.md`, `AGENTS.md`, and `CLAUDE.md` contain no active dependency on superseded governance or the subordinate-GSD development model;
5. CHG-001 is not used by active tests as conformance evidence;
6. the English normative specification, `src/ggsad/`, `.ggsad/`, and unrelated tests are unchanged;
7. archive manifest entries resolve to existing destinations, except the explicitly absent startup file;
8. Ruff formatting and linting, pytest, packaging, and applicable GSD consistency checks are executed;
9. `ty` results are reported honestly, with installer-owned diagnostics kept distinct from product diagnostics.

## Completion Boundary

Phase 4 closes only after its archive manifest, active-reference cleanup, fixture decoupling, and verification evidence are complete. Phase 5 quality-tool ownership work does not start automatically.
