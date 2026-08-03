# ADR-0005: Use Explicit State Transition Actions

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

GG-SAD defines phases, statuses, gates, wait behavior, fail behavior, evidence requirements, and
history. Direct edits to `state.yaml` could bypass gate evaluation, approval boundaries, and
transition legality.

The engine therefore needs a controlled mechanism for state changes.

## Decision Drivers

- Prevention of invalid state mutation
- Mandatory gate evaluation
- Explainable failures
- Atomic updates
- Complete transition history
- Agent safety
- Reproducible workflow behavior

## Considered Options

### Option 1 — Explicit Transition Actions

Expose actions such as `start`, `complete`, `wait`, `resume`, `fail`, `cancel`, `supersede`, and
`reopen`.

**Advantages**

- Encodes legal transitions
- Allows gate checks before mutation
- Produces consistent history
- Supports clear CLI and API contracts
- Prevents arbitrary status edits

**Disadvantages**

- More implementation work than direct file editing
- Requires migration when transition semantics evolve
- Exceptional transitions need explicit design

### Option 2 — Direct State File Editing

Allow humans and agents to update phase and status manually.

**Advantages**

- Minimal implementation
- Maximum flexibility

**Disadvantages**

- Easy gate bypass
- Weak auditability
- Inconsistent history
- High risk of invalid or contradictory state

### Option 3 — Event-Sourced State Only

Store only events and derive current state.

**Advantages**

- Complete audit trail
- Strong reconstruction capability
- Natural history model

**Disadvantages**

- Higher initial complexity
- More difficult manual inspection
- Premature for the first vertical slice

## Decision

> The project will expose explicit validated transition actions rather than permitting arbitrary
> workflow-state mutation.

The initial bootstrap will support a controlled `draft → ready` transition. Additional actions
will be added incrementally.

## Consequences

### Positive

- State changes become predictable and auditable
- Agents cannot bypass gates by editing status fields
- Invalid transitions produce actionable errors
- History can be generated consistently

### Negative

- Transition logic becomes a critical component
- Recovery and migration paths require careful design
- Users cannot freely edit governed state

### Neutral or Operational

- Manual edits may still occur during development but are not a valid production workflow
- State history is stored with the change

## Constraints and Guardrails

- Transition writes must be atomic.
- Invalid transitions must not change files.
- Gate evaluation order must remain DoF → DoW → DoD → DoR.
- Human-bound approvals cannot be synthesized by the engine or an agent.
- Reopen and supersede actions require explicit policy.

## Implementation Notes

- Model phase and status separately.
- Validate current state and requested action.
- Evaluate applicable criteria.
- Write the new state atomically.
- Append a history event with actor, time, previous state, new state, and reason.

## Verification

The decision is considered implemented when:

- valid `draft → ready` transitions succeed;
- invalid transitions are rejected;
- rejected transitions leave files unchanged;
- accepted transitions append history;
- direct state mutation is not exposed as a supported CLI action.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Transition bugs corrupt state | high | Property-based tests and atomic writes |
| Missing exceptional path | medium | Add actions through governed changes |
| Actor identity is weak | medium | Record explicit actor metadata and improve later |
| Gate logic becomes tangled | high | Keep transition and gate components separate |

## Rollback or Reversal

A future ADR may adopt event sourcing or another state model. Migration must preserve current
state, history, wait/failure metadata, and transition semantics.

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
