# ADR-0006: Use GSD as the Initial Execution Companion

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

The GG-SAD implementation is a substantial, multi-phase greenfield effort. Long-running coding
sessions risk context degradation, implementation drift, and loss of planning state.

GG-SAD itself governs goals, specifications, gates, state, evidence, approvals, and closure. It
does not yet provide a mature execution and context-engineering runtime.

GSD provides a Discuss → Plan → Execute → Verify workflow and persistent `.planning/` execution
context, making it a suitable initial companion. The comparison baseline identifies GSD as
particularly strong for context-heavy implementation work. fileciteturn1file1

## Decision Drivers

- Strong context engineering for long-running implementation
- Phase-oriented planning and verification
- Compatibility with Claude Code
- Support for fresh-context execution
- Ability to remain subordinate to GG-SAD governance
- Lower overlap with GG-SAD governance than broader process frameworks

## Considered Options

### Option 1 — GSD as Execution Companion

Use GSD for context engineering, subordinate planning, execution, and verification support.

**Advantages**

- Reduces context rot
- Provides practical execution workflow
- Fits solo and small-team agentic development
- Can be mapped beneath GG-SAD

**Disadvantages**

- Creates a second artifact tree under `.planning/`
- Requires explicit source-of-truth rules
- GSD completion does not equal GG-SAD closure

### Option 2 — OpenSpec

Use OpenSpec for repository-based specifications and execution support.

**Advantages**

- Lightweight
- Broad agent support
- Good for small and brownfield changes

**Disadvantages**

- Strong overlap with GG-SAD specification artifacts
- Higher risk of duplicate authoritative specs
- Less specialized context engineering

### Option 3 — Spec Kit

Use Spec Kit as the primary implementation framework.

**Advantages**

- Rich extensibility
- Strong enterprise and multi-agent support

**Disadvantages**

- Larger process footprint
- Risk of GG-SAD becoming an adapter to another workflow platform
- More artifact and configuration overhead

### Option 4 — BMAD

Use BMAD for end-to-end planning and execution.

**Advantages**

- Strong product, architecture, and review guidance
- Comprehensive role model

**Disadvantages**

- High token and process overhead
- Too heavyweight for the initial implementation
- Greater role and artifact overlap

### Option 5 — GG-SAD Stand-Alone Only

Implement without any companion method.

**Advantages**

- No integration complexity
- No duplicate artifact tree

**Disadvantages**

- Higher context-management risk
- More manual planning burden
- Slower initial implementation

## Decision

> The project will use GSD Core as the initial subordinate execution and context-engineering
> companion for Claude Code.

GG-SAD remains authoritative for governance, requirements, architecture, state, gates, evidence,
approvals, and closure.

## Consequences

### Positive

- Better continuity across long implementation sessions
- Clear Discuss, Plan, Execute, and Verify loop
- Earlier dogfooding of GG-SAD combination mode
- Practical support for vertical implementation slices

### Negative

- `.planning/` may duplicate information
- Mapping contracts and review discipline are required
- Contributors must understand two layers

### Neutral or Operational

- GSD is installed project-locally for Claude Code
- GSD artifacts are derived and non-authoritative
- `/gsd-ship` does not close a GG-SAD change

## Constraints and Guardrails

- GSD may not approve or transition GG-SAD state directly.
- GSD may not modify accepted ADRs or approved specifications silently.
- `.planning/` must remain below GG-SAD artifacts in precedence.
- Mapping conflicts produce `waiting`.
- Removing GSD must preserve stand-alone GG-SAD operation.
- Auto-advance and autonomous shipping remain disabled initially.

## Implementation Notes

- Install with the approved project-local GSD installer.
- Maintain `.ggsad/mappings/gsd.yaml`.
- Initialize GSD only after governing artifacts exist.
- Review generated `.planning/` files for scope expansion and duplicate truth.

## Verification

The decision is considered implemented when:

- GSD is initialized project-locally;
- `.planning/` artifacts are labeled subordinate;
- CHG-001 remains the only initial implementation scope;
- GSD cannot approve, transition, or close GG-SAD work;
- the repository still works without GSD.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Duplicate sources of truth | high | Enforce mapping and precedence |
| Scope expansion by generated plans | high | Review all GSD artifacts |
| Tool dependency | medium | Preserve stand-alone mode |
| GSD ship mistaken for closure | high | Require GG-SAD gate and evidence evaluation |
| Version drift | medium | Pin or record project-approved GSD version |

## Rollback or Reversal

GSD can be removed by deleting its local runtime files and `.planning/` execution state after
preserving required references. GG-SAD artifacts and state must remain intact. Another companion
may be introduced through a new ADR and mapping contract.

## Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Architecture: `docs/architecture.md`
- Roadmap: `docs/roadmap.md`
- Mapping: `.ggsad/mappings/gsd.yaml`
- Related Change: `specs/CHG-001-reference-repository-bootstrap/`

## Decision History

| Date | Status | Actor | Summary |
|---|---|---|---|
| 2026-08-02 | Proposed | human:project-owner | Initial proposal |
