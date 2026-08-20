# ADR-0008: Defer Memory, MCP, Web UI, and Multi-Agent Orchestration

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

The long-term GG-SAD architecture may include governed project memory, MCP exposure, a web UI,
IDE integration, repository automation, and multi-agent orchestration.

However, the initial objective is to prove the method through a manually usable repository and a
small CLI that can initialize, create, validate, and transition a change safely.

Implementing these platform capabilities during the bootstrap would increase scope, architecture,
security, operational, and maintenance complexity before real pilots validate the need.

## Decision Drivers

- Smallest coherent vertical slice
- Manual validation before automation
- Reduced security and maintenance risk
- Prevention of premature platform design
- Clear focus on core state, validation, and transition semantics
- Ability to learn from pilots before selecting backends and protocols

## Considered Options

### Option 1 — Defer All Four Capability Areas

Exclude project memory implementation, MCP server, web UI, and multi-agent orchestration from
CHG-001 and early core milestones.

**Advantages**

- Maintains focus
- Reduces security surface
- Avoids premature data and protocol decisions
- Speeds core validation
- Preserves architectural flexibility

**Disadvantages**

- Less automation and user convenience initially
- Memory and tool integrations arrive later
- Some manual workflows remain

### Option 2 — Implement File-Based Memory Immediately

Add the memory taxonomy and local storage during CHG-001.

**Advantages**

- Early context reuse
- Dogfoods future memory model

**Disadvantages**

- Expands schema and governance scope
- Risks confusing memory with governing truth
- Not required for initial CLI value

### Option 3 — Add MCP Early

Expose GG-SAD through an MCP server.

**Advantages**

- Broad agent integration potential
- Standardized tool interface

**Disadvantages**

- Security and permission complexity
- Protocol coupling before stable engine APIs
- Additional operational surface

### Option 4 — Build a Web UI or Orchestrator Early

Create a richer user experience or autonomous multi-agent execution platform.

**Advantages**

- More visible product experience
- Potential automation and parallelism

**Disadvantages**

- Highest complexity and maintenance cost
- Distracts from method validation
- Introduces identity, authorization, deployment, and observability requirements

## Decision

> The project will defer project memory implementation, MCP exposure, web UI, and multi-agent
> orchestration until the core repository, state, validation, transition, profile, gate, evidence,
> and review capabilities have been validated through real pilots.

The architecture may define extension points, but CHG-001 must not implement these capabilities.

## Consequences

### Positive

- The bootstrap remains small and testable
- Security and operational surface stay limited
- Core method semantics can stabilize first
- Future implementation choices remain open
- Maintenance cost stays proportional to demonstrated value

### Negative

- Users initially rely on files and CLI workflows
- Agent integration remains less automated
- Project memory benefits are delayed

### Neutral or Operational

- Memory taxonomy may remain documented
- MCP and UI remain roadmap candidates
- No deferred capability is considered abandoned

## Constraints and Guardrails

- No database-backed state or memory in CHG-001.
- No semantic vector index in CHG-001.
- No MCP server or tool endpoint in CHG-001.
- No web application or dashboard in CHG-001.
- No autonomous agent delegation or orchestration in CHG-001.
- Discoveries must be recorded in the roadmap or a future change proposal, not implemented
  opportunistically.

## Implementation Notes

- Keep extension boundaries in the architecture.
- Use portable files for current configuration and state.
- Add future capabilities only through dedicated GG-SAD changes and ADRs.
- Require permission, failure, rollback, and maintenance models before admission.

## Verification

The decision is considered implemented when:

- CHG-001 contains none of the deferred capabilities;
- the first CLI slice works without a database, web service, MCP, or orchestrator;
- roadmap entries preserve future direction;
- adding a deferred capability requires a separate approved change.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Deferred scope creeps into bootstrap | high | Enforce CHG-001 non-goals |
| Future extension becomes difficult | medium | Preserve narrow extension points |
| Manual workflows slow pilots | medium | Automate only repeated proven needs |
| Deferred items are forgotten | low | Keep explicit roadmap entries |

## Rollback or Reversal

Each deferred capability may be admitted through a dedicated ADR and governed change after
evidence demonstrates repeated need, ownership, permission boundaries, failure behavior, rollback,
and justified maintenance cost.

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
