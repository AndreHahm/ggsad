# Definition of <Ready | Done | Wait | Fail>

## Metadata

- Definition ID: <stable-id>
- Type: DoR | DoD | DoW | DoF
- Scope: Project | Phase | Change Class | Profile | Local Change
- Applies To: <phase, transition, artifact, or condition>
- Status: Draft | Active | Superseded
- Version: <version>
- Owner: <name-or-role>
- Last Updated: <YYYY-MM-DD>
- Supersedes: <reference-or-none>

## Purpose

<Explain the question answered by this definition and why it exists.>

Examples:

- DoR: May the next phase begin?
- DoD: Has the current phase completed successfully?
- DoW: Must the flow pause safely?
- DoF: Must the flow terminate unsuccessfully?

## Evaluation Priority

GG-SAD evaluates gates in this order:

1. Definition of Fail;
2. Definition of Wait;
3. current-phase Definition of Done;
4. next-phase Definition of Ready.

<Explain this definition's position and interaction with the other gate types.>

## Applicability

This definition applies when:

- <condition>
- <condition>

This definition does not apply when:

- <condition>

## Criteria

### <Criterion ID> — <Criterion Title>

<Clear, verifiable criterion statement.>

- Severity: informational | minor | major | blocking | critical
- Check Mode: automatic | review | approval
- Evidence: <expected evidence>
- Owner: <responsible role>
- Result Values: pass | fail | wait | not_applicable | not_evaluated

### <Criterion ID> — <Criterion Title>

<Repeat as required.>

## Evaluation Rules

- <rule>
- <rule>
- <rule>

For `not_applicable`, record:

- rationale;
- actor;
- authority;
- evidence or reference.

## Evidence Requirements

| Criterion | Required Evidence | Source | Retention |
|---|---|---|---|
| <criterion-id> | <evidence> | <path-or-system> | <policy> |

## Result

### Pass Condition

<Define when this gate passes.>

### Blocking Condition

<Define what blocks the transition or completion.>

### Not-Applicable Condition

<Define when the definition or criterion may be marked not applicable.>

## Wait-Specific Fields

Complete this section only for DoW definitions.

### Wait Category

`WAIT_<CATEGORY>`

### Trigger

<Describe the condition that requires a controlled pause.>

### Required Wait Record

```yaml
status: waiting
reason: <reason>
category: WAIT_<CATEGORY>
waiting_for: <person-role-process-or-source>
resume_when: <precise-condition>
safe_state: <preserved-safe-state>
resume_phase: <phase>
next_action: <action>
created_at: <ISO-8601 timestamp>
```

### Permitted Actions While Waiting

- <read-only or preservation action>

### Prohibited Actions While Waiting

- <risky, destructive, scope-changing, or approval-dependent action>

### Resume Rules

- <rule>
- <rule>

## Fail-Specific Fields

Complete this section only for DoF definitions.

### Failure Category

`FAILED_<CATEGORY>`

### Trigger

<Describe the hard failure condition.>

### Mandatory Response

- <action that must stop>
- <preservation or isolation action>
- <escalation action>

### Permitted Preservation or Recovery Actions

- <permitted action>

### Final Status

`FAILED_<CATEGORY>`

### Required Failure Evidence

- <evidence>
- <evidence>

### Restart or Supersession Rule

<Define whether recovery requires a new change, superseding change, or approved reopen action.>

## Agent Behavior

An agent evaluating this definition MUST:

- <required behavior>
- <required behavior>

An agent MUST NOT:

- <prohibited behavior>
- <prohibited behavior>

## Local Strengthening

Local specifications MAY strengthen this definition by:

- <allowed strengthening>

Local specifications MUST NOT:

- silently weaken blocking criteria;
- bypass required approval;
- convert a mandatory failure into success or unsafe waiting;
- remove required evidence.

## Examples

### Passing Example

Given <initial state>
When <evaluation occurs>
Then <expected result>

### Blocking Example

Given <initial state>
When <evaluation occurs>
Then <expected blocking result>

### Wait or Fail Example

Given <initial state>
When <trigger occurs>
Then <wait-or-fail result>

## Related Artifacts

- Constitution: `docs/constitution.md`
- Architecture: `docs/architecture.md`
- Project Brief: `docs/project-brief.md`
- Related ADRs: <references>
- Related Profile: <reference>
- Related Change: <reference-or-none>

## Definition History

| Date | Version | Status | Actor | Summary |
|---|---|---|---|---|
| <YYYY-MM-DD> | <version> | Draft | <actor> | Initial draft |
