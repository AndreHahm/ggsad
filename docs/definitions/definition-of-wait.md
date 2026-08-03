# Definition of Wait

## Purpose

The Definition of Wait (DoW) identifies conditions under which work must pause safely without
being considered failed.

A wait state means that a specific prerequisite, decision, input, approval, dependency, or
external condition is missing but the change remains potentially achievable.

## Typical Wait Categories

- `WAIT_USER_INPUT`
- `WAIT_DECISION`
- `WAIT_DEPENDENCY`
- `WAIT_PROCESS`
- `WAIT_APPROVAL`
- `WAIT_REVIEW`
- `WAIT_EXTERNAL_SYSTEM`
- `WAIT_BUDGET_WINDOW`
- `WAIT_RATE_LIMIT`

## Wait Triggers

A phase MUST enter `waiting` when, for example:

- required user information is missing;
- a product, architecture, security, legal, operational, or compliance decision is pending;
- specification or plan approval is required but not recorded;
- a required dependency, environment, tool, permission, or credential is temporarily unavailable;
- an external system or process must complete first;
- a review is required but no independent Reviewer is available;
- blocking review findings require Requestor action;
- a potential ADR or constitutional conflict requires a decision;
- an implementation discovery requires specification revision and reapproval;
- a temporary rate, cost, or capacity boundary prevents safe continuation;
- the next phase is not ready even though the current phase is done.

## Required Wait Record

Every wait state MUST record:

```yaml
status: waiting
reason: architecture-decision-required
category: WAIT_DECISION
waiting_for: human:project-owner
resume_when: ADR-approved
safe_state: no-uncommitted-destructive-change
resume_phase: plan
next_action: update-plan-and-reevaluate-gates
created_at: 2026-08-02T00:00:00Z
```

Required fields are:

- reason;
- category;
- responsible person, role, process, or external source;
- precise resume condition;
- safe current state;
- phase or point at which work resumes;
- next action after resumption;
- timestamp and actor.

## Agent Behavior in Wait

An agent in a wait state MUST:

- stop risky, destructive, scope-changing, and approval-dependent actions;
- preserve the working state and relevant evidence;
- state exactly what is missing;
- identify the responsible owner or source;
- formulate one minimal, decidable request where human input is needed;
- avoid treating assumptions, silence, or model output as approval;
- avoid unrelated work unless separately governed;
- resume only after the recorded condition is satisfied;
- reevaluate DoF, DoW, DoD, and DoR after resumption.

An agent MAY:

- perform explicitly allowed read-only analysis;
- prepare decision options or diagnostics;
- preserve logs and evidence;
- improve non-governed notes when this cannot affect the decision or scope.

## Safe-State Requirements

Before entering wait:

- no destructive or half-applied operation may remain active;
- temporary files and generated output must be identified;
- the working tree state must be understood;
- rollback or recovery information must be preserved where relevant;
- secrets and sensitive output must remain protected;
- review targets should remain stable when waiting for findings.

## Resume Rules

A wait state may resume only when:

- the exact recorded condition is satisfied;
- required evidence or approval is available;
- the responsible actor is identifiable;
- the safe state remains valid or is restored;
- new information has been incorporated into the correct authoritative artifact;
- applicable gates are reevaluated.

If the missing condition materially changes goal, scope, architecture, risk, or requirements, the
flow MUST return to the appropriate earlier phase rather than continuing from the old plan.

## Wait Is Not Failure

A wait MUST NOT be converted to failure merely because work cannot continue immediately.

A wait becomes failure only when a Definition of Fail trigger applies, such as:

- the prerequisite is permanently unavailable;
- the goal is no longer achievable within approved constraints;
- a deadline or hard budget boundary is exceeded;
- required approval is explicitly denied;
- safe recovery is no longer possible.

## Wait Completion Evidence

Evidence should record:

- wait category and reason;
- entry timestamp;
- preserved safe state;
- requested decision or dependency;
- resolution;
- resume timestamp and actor;
- post-resume gate evaluation.

Local DoW rules may add triggers and metadata but MUST NOT permit unsafe continuation.
