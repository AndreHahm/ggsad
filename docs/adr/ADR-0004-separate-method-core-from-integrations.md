# ADR-0004: Separate the Method Core from Integrations

## Metadata

- Status: Proposed
- Date: 2026-08-02
- Decision Owners: Project Maintainer
- Requestor: human:project-owner
- Reviewer: pending
- Approver: pending
- Related Change: CHG-001
- Supersedes: None
- Superseded By: None

## Context

GG-SAD must operate stand-alone and in combination with methods, tools, coding agents, IDEs, CI
systems, issue trackers, and repository platforms.

If external integrations are allowed to define core semantics, GG-SAD would become coupled to a
vendor or execution environment and could no longer provide stable governance.

## Decision Drivers

- Tool and vendor independence
- Stand-alone operation
- Stable normative semantics
- Optional companion-method support
- Testability and maintainability
- Clear dependency direction
- Safe removal or replacement of integrations

## Considered Options

### Option 1 — Layered Core with Optional Adapters

Keep Method Core, Engine, Services, Agent Workflows, and Integrations in separate dependency
layers.

**Advantages**

- Preserves method independence
- Enables optional integrations
- Supports independent testing
- Makes ownership boundaries explicit
- Allows adapters to evolve without redefining semantics

**Disadvantages**

- Requires mapping contracts and adapter interfaces
- Introduces architectural boundaries that must be maintained
- Some duplicated translation code may exist

### Option 2 — Build Directly Around GSD or Claude Code

Use the initial execution environment as the architectural center.

**Advantages**

- Faster initial integration
- Less adapter design
- Immediate use of tool-specific features

**Disadvantages**

- Vendor and runtime coupling
- Reduced portability
- External workflow may override GG-SAD semantics
- Stand-alone operation becomes difficult

### Option 3 — Plugin-First Framework

Design a broad plugin system before the core engine.

**Advantages**

- Maximum extensibility from the beginning
- Unified integration model

**Disadvantages**

- Premature complexity
- Core semantics may remain unstable
- High maintenance cost before validated demand

## Decision

> The project will separate the stable GG-SAD Method Core and Engine from Method Services, Agent
> Workflows, and optional Integration Adapters.

Dependencies must flow inward:

```text
Integrations → Agent Workflows → Method Services → Method Engine → Method Core
```

## Consequences

### Positive

- GG-SAD remains portable and tool-independent
- Stand-alone operation is preserved
- Integrations can be added or removed safely
- Core semantics can be versioned separately
- Testing boundaries become clearer

### Negative

- Integration mappings and interfaces require explicit design
- Some external tools may need translation layers
- Adapter maintenance remains an ongoing cost

### Neutral or Operational

- The first GSD integration is contractual and procedural
- Deep synchronization is deferred until demonstrated need exists

## Constraints and Guardrails

- Method Core must not import agent, repository-host, IDE, or CI SDKs.
- Integrations must not transition state or approve work directly.
- Removing integrations must preserve GG-SAD artifacts.
- Mapping conflicts must produce wait or fail outcomes, not silent reconciliation.
- Memory and integration data must not override governing documents.

## Implementation Notes

- Organize code into core, engine, services, workflows, and adapters.
- Define `.ggsad/mappings/` contracts.
- Add integration admission criteria to the roadmap.
- Keep adapter tests separate from core tests.

## Verification

The decision is considered implemented when:

- core modules run without GSD, Claude Code, GitHub, or CI dependencies;
- stand-alone initialization and validation work;
- GSD can be removed without deleting GG-SAD artifacts;
- integration permissions and ownership are explicit.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Layer leakage | high | Enforce imports and architecture tests |
| Adapter duplication | medium | Define narrow common interfaces |
| Premature abstraction | medium | Add extension points only after pilots |
| Integration bypass | high | Validate mapping permissions and transitions |

## Rollback or Reversal

This decision may be superseded only by an ADR that preserves stand-alone governance semantics and
provides a migration plan for integrations and core contracts.

## Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Architecture: `docs/architecture.md`
- Roadmap: `docs/roadmap.md`
- Related Change: `specs/CHG-001-reference-repository-bootstrap/`

## Decision History

| Date | Status | Actor | Summary |
|---|---|---|---|
| 2026-08-02 | Proposed | human:project-owner | Initial proposal |
