# <Change ID> — <Change Title>

## Metadata

- Change ID: <CHG-NNN>
- Slug: <change-slug>
- Class: S | M | L
- Phase: specify
- Status: draft | ready | active | waiting | done | failed | cancelled | superseded
- Flow Profile: <patch | standard | release | custom>
- Compliance Profile: lean | standard | governed | regulated | <custom>
- Requestor: <participant-id>
- Decision Owner: <name-or-role>
- Created: <YYYY-MM-DD>
- Last Updated: <YYYY-MM-DD>
- Related Roadmap Item: <reference-or-none>
- Parent Initiative: <change-id-or-none>

## Goal

### Desired Outcome

<Describe the target state and expected benefit.>

### Problem Being Solved

<Describe the current problem, deficiency, need, or opportunity.>

### Success Signals

- <measurable or verifiable signal>
- <measurable or verifiable signal>

### Non-Goals

- <explicitly excluded outcome>
- <explicitly excluded outcome>

## Context

<Describe the relevant current state, history, constraints, and affected users or systems.>

## Scope

### Included

- <included behavior, component, artifact, or boundary>

### Excluded

- <excluded behavior, component, artifact, or boundary>

## Stakeholders and Participants

| Role | Participant | Responsibility |
|---|---|---|
| Requestor | <participant-id> | Creates or changes the governed work product |
| Reviewer | <participant-id-or-pending> | Independently evaluates the work product |
| Approver | <participant-id-or-not-required> | Provides required approval |
| Informed | <participant-or-group> | Receives status or outcome |

## Requirements

### R-001 — <Requirement Title>

<Write one unambiguous, verifiable requirement.>

- Priority: Must | Should | May
- Source: <source-or-rationale>
- Related ADRs: <references-or-none>
- Verification Method: <test, review, analysis, inspection, measurement>

### R-002 — <Requirement Title>

<Repeat as required.>

## Acceptance Examples

Every behavioral requirement MUST have at least one concrete acceptance example, unless a
justified alternative verifiable condition is documented.

### E-001 — <Example Title>

- Covers: R-001
- Type: normal | negative | failure | boundary | recovery | permission

Given <initial state>
When <action or event>
Then <observable result>
And <additional result>

### E-002 — <Example Title>

- Covers: R-001, R-002
- Type: <type>

Given <initial state>
When <action or event>
Then <observable result>

## Alternative Verifiable Conditions

Use only when an acceptance example would not improve clarity.

| Requirement | Condition | Why an Example Is Not Applicable |
|---|---|---|
| <requirement-id> | <verifiable condition> | <rationale> |

## Constraints

### Project and Constitutional Constraints

- <constraint>

### Architecture and ADR Constraints

- <constraint or reference>

### Technology Constraints

- <constraint>

### Security, Privacy, and Compliance Constraints

- <constraint>

### Compatibility and Migration Constraints

- <constraint>

### Resource and Budget Constraints

- <constraint>

## Affected Areas

- Components:
- Interfaces:
- Data:
- Configuration:
- Documentation:
- Operations:
- Users:
- External Integrations:

## Risks

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| <risk> | low | medium | high | low | medium | high | <mitigation> | <owner> |

## Dependencies and Prerequisites

| Dependency | Type | Owner | Required Condition | Status |
|---|---|---|---|---|
| <dependency> | technical | decision | approval | external | <owner> | <condition> | open |

## Breaking-Change Assessment

- Breaking Change: Yes | No | Unknown
- Affected Consumers: <consumers-or-none>
- Migration Required: Yes | No | Unknown
- Approval Required: Yes | No
- Reference: <ADR, plan, or decision>

## Flow Gates

### Additional Ready Conditions

- <local condition or None>

### Additional Done Conditions

- <local condition or None>

### Additional Wait Conditions

- <trigger, owner, and resume condition or None>

### Additional Fail Conditions

- <trigger, response, and final status or None>

Local gates may strengthen project definitions but MUST NOT silently weaken them.

## Verification Plan

| Requirement / Example | Verification Method | Expected Evidence | Owner |
|---|---|---|---|
| R-001 / E-001 | <method> | <evidence> | <owner> |

## Pair Review

- Required: Yes | No | Conditional
- Activation Basis: <profile, risk, class, artifact, or policy>
- Requestor: <participant-id>
- Reviewer: <distinct-participant-id-or-pending>
- Review Scope: <artifacts and criteria>
- Separate `review.md`: Optional | Conditional | Mandatory
- Separate Human Approval: Yes | No | Conditional

## Approval

- Specification Approval Required: Yes | No
- Approver: <participant-id-or-pending>
- Approval Status: Pending | Approved | Rejected | Not Required
- Approval Evidence: <reference-or-none>

## Open Questions

| ID | Question | Owner | Blocking | Resolution Condition |
|---|---|---|---|---|
| Q-001 | <question> | <owner> | Yes | No | <condition> |

Use `None` when no open questions remain.

## Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Architecture: `docs/architecture.md`
- ADRs: <references>
- Plan: `plan.md`
- Tasks: `tasks.md`
- Evidence: `evidence.md`
- State: `state.yaml`
- Companion Execution Context: <reference-or-none>

## Change History

| Date | Actor | Status | Summary |
|---|---|---|---|
| <YYYY-MM-DD> | <actor> | Draft | Initial draft |
