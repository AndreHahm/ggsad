# ADR-0007: Use One Agent with Phase-Specific Workflows Initially

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

The reference implementation needs agent-assisted intake, specification, planning, build,
verification, review preparation, and closure support.

Introducing multiple specialized agents or an orchestration system before the engine, permissions,
gates, and evidence model are stable would add complexity, token cost, coordination risk, and
ambiguous responsibility.

The architecture and implementation guide recommend one agent with multiple phase workflows for
the initial release. fileciteturn1file5

## Decision Drivers

- Minimal viable implementation
- Clear accountability
- Lower orchestration complexity
- Easier permission and context control
- Reduced token and maintenance overhead
- Ability to validate workflow semantics before scaling roles

## Considered Options

### Option 1 — One Primary Agent with Phase Workflows

Use one implementation runtime, initially Claude Code, with explicit phase-specific instructions
and permissions.

**Advantages**

- Simple operational model
- Clear Requestor identity
- Easier context and permission boundaries
- Lower maintenance cost
- Supports incremental workflow design

**Disadvantages**

- Context may still become large
- One runtime is a concentration point
- Independent review still requires another participant

### Option 2 — Specialized Multi-Agent Team

Create separate specification, architecture, implementation, testing, and review agents.

**Advantages**

- Strong specialization
- Potential parallelism
- Clear conceptual roles

**Disadvantages**

- Higher orchestration and token overhead
- Complex handoffs and state synchronization
- Increased risk of conflicting artifacts
- Premature before permissions and gates are operational

### Option 3 — Autonomous Agent Orchestrator

Build or adopt an orchestration system immediately.

**Advantages**

- Automated delegation
- Potential scalability
- Rich workflow automation

**Disadvantages**

- Significant out-of-scope platform work
- Security and control risk
- Would define the method through tooling prematurely
- Contradicts the bootstrap non-goals

## Decision

> The initial reference implementation will use one primary implementation agent with
> phase-specific workflows and permissions.

Independent Pair Review will use a distinct human, agent, or external service when required. A
second context or subagent under the same participant identity does not automatically qualify as
independent review.

## Consequences

### Positive

- Simpler bootstrap and debugging
- Clear ownership of implementation work
- Easier enforcement of phase-specific scope
- Faster validation of GG-SAD semantics
- Avoids premature orchestration platform work

### Negative

- Limited parallelism
- The primary agent may accumulate context
- Manual handoff to an independent reviewer is required

### Neutral or Operational

- GSD may use fresh contexts for execution support
- Fresh contexts do not change participant identity
- Additional agent roles require later evidence and ADRs

## Constraints and Guardrails

- Every workflow must define objective, inputs, readable files, writable files, prohibited
  actions, stop conditions, and output contract.
- The primary implementation agent is the Requestor unless explicitly reassigned.
- Reviewer identity must be distinct.
- Agents may not self-approve human-bound actions.
- Subagents require a genuine context, permission, or specialization boundary.

## Implementation Notes

- Define `/ggsad.intake`, `/ggsad.specify`, `/ggsad.plan`, `/ggsad.build`,
  `/ggsad.verify`, and `/ggsad.close` later.
- Use `AGENTS.md` for general rules and `CLAUDE.md` for Claude-specific constraints.
- Keep review-only execution separate from implementation.

## Verification

The decision is considered implemented when:

- Claude Code can execute CHG-001 under phase-scoped instructions;
- writable and prohibited paths are explicit;
- required Pair Review uses a distinct participant;
- no multi-agent orchestrator is required;
- subagent output is validated by the primary Requestor.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Context degradation | medium | Use GSD and fresh contexts |
| Self-review confusion | high | Enforce distinct participant identity |
| Excessive agent permissions | high | Define phase-specific scopes |
| Primary-agent bottleneck | medium | Add roles only after observed need |

## Rollback or Reversal

A future ADR may introduce specialized agents or orchestration after the core engine, permission
model, identity model, and workflow contracts are validated. Migration must preserve audit history
and review independence.

## Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Architecture: `docs/architecture.md`
- Roadmap: `docs/roadmap.md`
- Agent Rules: `AGENTS.md`
- Claude Rules: `CLAUDE.md`
- Related Change: `specs/CHG-001-reference-repository-bootstrap/`

## Decision History

| Date | Status | Actor | Summary |
|---|---|---|---|
| 2026-08-02 | Proposed | human:project-owner | Initial proposal |
