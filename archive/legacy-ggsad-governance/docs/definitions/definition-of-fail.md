# Definition of Fail

## Purpose

The Definition of Fail (DoF) identifies conditions under which a flow must terminate
unsuccessfully.

DoF has the highest gate-evaluation priority. When a DoF trigger is active, completion or
readiness criteria cannot override it.

## Typical Failure Categories

- `FAILED_POLICY_VIOLATION`
- `FAILED_SECURITY`
- `FAILED_DATA_LOSS`
- `FAILED_REPOSITORY_CORRUPTION`
- `FAILED_UNAUTHORIZED_BREAKING_CHANGE`
- `FAILED_SCOPE_VIOLATION`
- `FAILED_UNRECOVERABLE_STATE`
- `FAILED_BUDGET_LIMIT`
- `FAILED_RETRY_LIMIT`
- `FAILED_UNSATISFIABLE_REQUIREMENT`
- `FAILED_DEPENDENCY`
- `FAILED_APPROVAL_DENIED`
- `FAILED_INTEGRITY`

## General Fail Triggers

A flow MUST fail when:

- a critical security violation occurs;
- data loss or repository corruption occurs and cannot be safely recovered;
- an unauthorized breaking change is introduced or required;
- the constitution or an accepted ADR is knowingly violated;
- work proceeds outside the approved scope after the violation is detected;
- a destructive action is performed without required authorization;
- the goal is permanently unachievable within approved constraints;
- an implementation, build, migration, deployment, or release state is unrecoverable;
- a hard cost, budget, time, or retry limit is exceeded;
- required acceptance conditions are permanently unsatisfiable;
- evidence is fabricated, concealed, or materially misrepresented;
- required independent review or approval is deliberately bypassed;
- state or history integrity cannot be trusted;
- an integration bypasses GG-SAD gates and the safe state cannot be restored.

## Required Failure Rule

Every failure rule MUST define:

- trigger;
- category;
- mandatory response;
- actions that must stop;
- permitted preservation, isolation, rollback, or recovery actions;
- final status;
- required evidence and documentation;
- escalation owner.

Example:

```markdown
### F-01 — Unauthorized Breaking Change

**Trigger**

A breaking change is required or implemented without the required approval.

**Mandatory response**

- Stop affected implementation and release work.
- Isolate or revert the unauthorized change when safe.
- Preserve evidence and the current repository state.
- Record the conflict in the change specification.
- Notify the Requestor and human decision owner.

**Permitted actions**

- Read-only diagnosis.
- Creation of a recovery or decision package.
- Safe rollback explicitly allowed by policy.

**Final status**

`FAILED_UNAUTHORIZED_BREAKING_CHANGE`
```

## Immediate Agent Behavior

When a DoF trigger is detected, an agent MUST:

1. stop affected work;
2. avoid further mutation except approved preservation or recovery actions;
3. protect repository, data, credentials, and evidence;
4. identify the exact trigger and affected artifacts;
5. record the failure category and current safe state;
6. disclose commands already executed and their results;
7. notify the Requestor and escalation owner;
8. avoid presenting partial success as completion;
9. avoid retry loops that may increase damage;
10. require a new authorized recovery or replacement change before resuming failed work.

## Recoverable Error Versus Failure

Not every command error is a DoF event.

A recoverable error may remain in the active phase when:

- no policy or integrity violation occurred;
- state remains safe;
- retry is bounded and justified;
- the error can be corrected within approved scope;
- evidence remains trustworthy.

A condition should become `waiting` rather than `failed` when a temporary dependency, decision,
approval, process, or external system is missing and safe resumption remains possible.

## Mandatory Failure Scenarios

### Constitutional or ADR Violation

- Stop affected work.
- Document the exact conflict.
- Preserve evidence.
- Do not alter the higher-precedence artifact to justify the implementation.
- Mark failure if the violation was executed and cannot be safely reverted within policy.

### Critical Security Incident

- Stop affected operations.
- Isolate affected artifacts or environments where authorized.
- Do not expose secrets in logs or reports.
- Preserve forensic evidence.
- Escalate to the human security owner.
- Use `FAILED_SECURITY`.

### Data Loss or Repository Corruption

- Stop writes.
- Preserve the current state.
- Avoid destructive cleanup.
- Use approved backup or recovery procedures only.
- Record affected data and commands.
- Use `FAILED_DATA_LOSS` or `FAILED_REPOSITORY_CORRUPTION`.

### Unrecoverable Migration or Release

- Stop rollout or publication.
- Execute only approved rollback or withdrawal actions.
- Preserve release and monitoring evidence.
- Notify operational and decision owners.
- Use `FAILED_UNRECOVERABLE_STATE`.

### Fabricated Evidence or Approval

- Stop closure and release.
- Mark affected evidence as untrusted.
- preserve the audit trail;
- require independent investigation and correction;
- use `FAILED_INTEGRITY`.

## Failure Evidence

The failure record MUST include:

- change and phase;
- trigger and category;
- detection timestamp and actor;
- commands or events leading to failure;
- affected artifacts and environments;
- current safe state;
- preservation, isolation, rollback, or recovery actions;
- known impact;
- unresolved risks;
- escalation owner;
- final status.

## Restart After Failure

A failed flow MUST NOT be silently resumed.

Continuation requires one of:

- a separately authorized recovery change;
- a new change that supersedes the failed change;
- an explicit reopen action permitted by policy, with documented rationale and approval.

The original failure history and evidence MUST remain preserved.

Local DoF rules may add stricter triggers but MUST NOT downgrade a mandatory failure into success
or an unsafe wait.
