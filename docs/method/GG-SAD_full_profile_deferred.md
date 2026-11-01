# GG-SAD — Full Method Profile (Deferred)

**Status:** Deferred, not normative. This document keeps the text of the `full` method profile that the normative specification (`GG-SAD_normative_method_specification.md`) no longer contains. It is specified, not implemented, and no rule of it binds a project until a later revision of the normative specification adopts it. Section numbers and the numbers of acceptance examples (`AE-…`) are those of the normative specification version 1.4; the acceptance examples of the normative specification have been renumbered, so an `AE-` number in this document does not name an example there. A reference to a section that this document does not contain names the normative specification (`GG-SAD_normative_method_specification.md`), the Implementation Contract, or the Signing Extension as before.

---

### 4.1 Binding Order of Precedence

This section specifies the `full` method profile (Section 5.6).

In case of conflict, the following priority applies:

1. `docs/constitution.md`
2. existing accepted ADRs under `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. approved scoped decision records, where they do not replace an ADR
6. approved change specification `spec.md`
7. approved implementation plan `plan.md`
8. local task list `tasks.md`
9. implementation and tests
10. evidence, supplementary notes, and temporary work artifacts

A change MUST NOT silently override a higher-ranking document.

See AE-229.

**AE-229 — A higher-ranking document wins over a lower one**

- Covers: Section 4.1

Given a `full` change whose approved `spec.md` requires a library that an accepted ADR under `docs/adr/` prohibits, and a `plan.md` whose scope differs from the approved `spec.md`  
When the plan of the change is prepared  
Then the ADR takes precedence over the specification, the conflict is documented and returned to the requestor, and the approved `spec.md` takes precedence over the `plan.md`, so that the change does not silently override either higher-ranking document


### 5.5 Phase Omission

A phase MAY be omitted only when the resolved workflow explicitly permits that omission and a participant authorized by the applicable approval rules approves it. An agent MUST NOT infer permission to omit a phase from silence, missing artifacts, project size, or apparent lack of relevance.

The omission record MUST identify:

- the omitted phase;
- the authorizing workflow rule;
- the approver;
- the rationale;
- the approval timestamp;
- the replacement evidence.

Selecting a named flow from Section 7.1 is one authorized flow-selection decision, not a separate omission decision for each phase the flow omits. One compact omission record MUST cover all phases omitted by the selected flow. The named flow supplies the authorizing workflow rule and omitted-phase list; the record MUST still identify the approver, rationale, approval timestamp, and replacement evidence. For a Class S change, this record MAY be stored inline with the minimal specification defined in Section 6.1.

Replacement evidence MUST cover the outcomes and gates that each omitted phase would normally establish or explain why each outcome or gate is not applicable. Omitting a phase MUST NOT remove an invariant-core obligation or bypass the Definition of Ready for the next phase.

See AE-230.

**AE-230 — A phase is omitted only with a record**

- Covers: Section 5.5

Given a `full` change on the Patch Flow with one compact omission record that names the flow, the approver, the rationale, the approval timestamp, and the replacement evidence for every phase the flow omits, and a second `full` change on which an agent omits the verify phase because the change is small, with no record  
When both changes are checked  
Then the first change is accepted with its one record, and the omission of the second change is rejected, because permission to omit a phase is not inferred from project size or from silence


## 6. Size Classes

This section specifies the `full` method profile (Section 5.6).

### 6.1 Class S — Patch

Suitable for small, clearly bounded changes with a known solution and low risk.

Minimum artifact:

- inline specification in an issue, change request, or commit context.

Minimum content:

- goal,
- scope, including the allowed path list (Section 24.5),
- acceptance conditions,
- verification.

The scope of a change is stated and measured as Section 24.5 states.

See AE-231.

**AE-231 — A Class S change meets its minimum content**

- Covers: Section 6.1

Given a Class S change with an inline specification that states the goal, the scope with its allowed path list, the acceptance conditions, and the verification, and a second Class S change whose inline specification states no verification  
When each inline specification is checked against the minimum content of Class S  
Then the first meets the minimum content, and the second does not, and the missing verification is reported

### 6.2 Class M — Change

Suitable for self-contained functional or technical changes.

Mandatory artifact:

- `spec.md`

Optional artifacts:

- `plan.md`
- `tasks.md`
- `evidence.md`

See AE-232.

**AE-232 — A Class M change needs `spec.md` and no other file**

- Covers: Section 6.2

Given a Class M change that has `spec.md` and no `plan.md`, `tasks.md`, or `evidence.md`, and a second Class M change that has no `spec.md`  
When the mandatory artifact of each change is checked  
Then the first change is valid, because the other three artifacts are optional, and the second lacks its mandatory artifact `spec.md`

### 6.3 Class L — Initiative

Suitable for multiple independent or interdependent changes.

An initiative MUST be decomposed into multiple change specifications. A short roadmap or dependency overview MAY be used. An epic is not required.

See AE-233.

**AE-233 — A Class L initiative is decomposed**

- Covers: Section 6.3

Given an initiative that is decomposed into three change specifications with a short dependency overview and no epic, and a second initiative that is recorded as one single change specification  
When the decomposition of each initiative is checked  
Then the first initiative is accepted, because an epic is not required, and the second is not accepted, because an initiative MUST be decomposed into multiple change specifications

---

## 7. Phase Model

This section specifies the `full` method profile (Section 5.6).

The canonical phase identifiers are lowercase and limited to:

```text
intake
explore
decide
specify
plan
build
verify
release
closed
```

The standard delivery flow is:

```text
intake
  ↓
specify
  ↓
plan
  ↓
build
  ↓
verify
  ↓
release
  ↓
closed
```

Not every change MUST pass through every phase.

### 7.1 Permitted Shortened Flows

#### Patch Flow

```text
specify → build → verify → closed
```

See AE-234.

**AE-234 — Patch Flow skips the plan and the release phase**

- Covers: Section 7.1 (Patch Flow)

Given a `full` change that follows the Patch Flow, in the specify phase with the status `done` and with the Definition of Ready of the build phase satisfied  
When the `complete` action is requested, and later the same change in the verify phase is moved to the release phase  
Then the first request advances the change to the build phase, and the move to the release phase is not permitted, because the Patch Flow is specify, build, verify, and closed

#### Standard Flow

```text
specify → plan → build → verify → closed
```

See AE-235.

**AE-235 — Standard Flow includes the plan phase**

- Covers: Section 7.1 (Standard Flow)

Given a `full` change that follows the Standard Flow, in the specify phase with the status `done` and with the Definition of Ready of the plan phase satisfied  
When the `complete` action is requested, and later a move of the change from the specify phase directly to the build phase is requested  
Then the first request advances the change to the plan phase, and the direct move to the build phase is not permitted, because the Standard Flow is specify, plan, build, verify, and closed

#### Release Flow

```text
specify → plan → build → verify → release → closed
```

See AE-236.

**AE-236 — Release Flow ends with the release phase**

- Covers: Section 7.1 (Release Flow)

Given a `full` change that follows the Release Flow, in the verify phase with the status `done` and with the Definition of Ready of the release phase satisfied  
When the `complete` action is requested, and later a close of the change directly from the verify phase is requested  
Then the first request advances the change to the release phase, and the direct close is not permitted, because the Release Flow is specify, plan, build, verify, release, and closed

#### Exploration Flow

```text
explore → decide → specify
```

Exploration MUST NOT silently transition into production implementation.

See AE-237.

**AE-237 — Exploration does not become production implementation**

- Covers: Section 7.1 (Exploration Flow)

Given a `full` change that follows the Exploration Flow, in the decide phase with the status `done` and with the Definition of Ready of the specify phase satisfied  
When the `complete` action is requested, and later a move of an exploration change from the decide phase to the build phase is requested  
Then the first request advances the change to the specify phase, and the move to the build phase is not permitted, because exploration does not transition into production implementation

---

## 8. State Model

This section specifies the `full` method profile (Section 5.6).

Every phase has a status.

### 8.1 Canonical Statuses

```text
draft
ready
active
waiting
failed
done
cancelled
superseded
```

Recommended metadata format:

```json
{
  "phase": "build",
  "status": "waiting",
  "reason": "user-approval-required",
  "owner": "requestor",
  "resume_when": "approval-recorded"
}
```

In the state document, `phase` and `status` are fields of the `after` record of an entry, and the other fields are held in its field `wait` (Section 25.1).

`closed` is the terminal phase defined in Section 7; it is never a status value. When a change is in the `closed` phase, its terminal outcome is recorded in `status` as `done`, `failed`, `cancelled`, or `superseded`.

### 8.2 Legal Phase/Status Combinations

The statuses `draft`, `ready`, `active`, and `waiting` are legal at any non-closed phase. The status `done` is legal at any phase as that phase's local completion signal, gating advancement on the next phase's Definition of Ready. It represents the change's successful terminal outcome only when it occurs with the `closed` phase.

The statuses `failed`, `cancelled`, and `superseded` are legal only with the `closed` phase. An action producing any of these outcomes MUST finalize the change into the `closed` phase in the same state mutation.

See AE-238.

**AE-238 — Legal combinations of phase and status**

- Covers: Section 8.2

Given a `full` change in the build phase  
When the status `done` is recorded for the build phase, and then the status `failed` is requested for the build phase without the `closed` phase  
Then the status `done` is legal as the local completion signal of the phase, and the status `failed` is not legal with a phase that is not `closed`, because an action that produces `failed` finalizes the change into the `closed` phase in the same state mutation

### 8.3 Transition Table

| Action | Legal From (Phase/Status) | Precondition | Gate Order | Resulting Phase/Status | Rejection Behavior |
|---|---|---|---|---|---|
| `start` | A non-closed phase with status `ready` | Starting the phase is authorized. | DoF → DoW; current-phase DoR was established by `ready`, and current-phase DoD and next-phase DoR are not applicable. | Same phase with status `active`. | Reject without any partial mutation of persisted state when the precondition is not satisfied or an applicable gate would decide against the start: a Definition of Fail condition that is active (a hard failure included), a Definition of Wait condition that is active, or a gate that cannot be evaluated (Section 24.2). |
| `complete` | A non-closed phase with status `draft`, `active`, or `done` | The phase and status are a legal source, and the evaluation is requested: from `draft`, of the current phase's DoR; from `active`, of the current phase's DoD; from `done`, of the next phase's DoR. | From `draft`: DoF → DoW → current-phase DoR. From `active`: DoF → DoW → current-phase DoD → next-phase DoR. From `done`: DoF → DoW → next-phase DoR; current-phase DoR and DoD are already established. | From `draft`, the same phase with status `ready`. From `active`, satisfied current-phase DoD first produces the current phase with status `done`; satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. From `done`, satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. Completion of the final phase produces `closed`/`done`. | Reject without any partial mutation of persisted state when the phase and status are not a legal source. When DoW, current-phase DoR, or current-phase DoD does not allow the transition, record the evaluation in the history and answer `blocked` (Section 22.2); an active fail condition of the severity `hard` closes the change as failed, and a soft fail condition or a gate that cannot be evaluated puts the change in a wait (Sections 24.7 and 24.2). Unsatisfied next-phase DoR is not a rejection after current-phase DoD succeeds or during re-evaluation from `done`; it preserves the current phase with status `done`. |
| `wait` | Any non-closed phase/status | A DoW condition is active. | DoF → DoW; current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | Same phase with status `waiting`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When DoF finds a fail condition of the severity `hard` active, close the change as failed in the same state mutation and answer `success` (Section 24.7). |
| `resume` | A non-closed phase with status `waiting` | The recorded resume condition is satisfied and the recorded or explicitly required resume phase is non-closed. | DoF → DoW → DoR for the recorded non-closed resume phase or explicitly required earlier non-closed phase; current-phase DoD and next-phase DoR are not applicable. | Recorded non-closed resume phase, or an explicitly required earlier non-closed phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When the resume-phase DoR is not satisfied or a DoW condition is still active, record the evaluation in the history, remain `waiting`, and answer `blocked` (Section 22.2). Fail when DoF determines failure (Section 24.7). |
| `fail` | Any non-closed phase/status | A soft failure awaits disposition: the status is `waiting` with a wait state of the category `WAIT_DECISION` for a DoF condition of the severity `soft` that is active (Section 24.7). | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `cancel` | Any non-closed phase/status | An authorized cancellation decision exists. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `cancelled`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied or the gate definitions differ from the approved ones (issue code `gates-changed`, Section 24.1). |
| `reopen` (`full` only) | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF for the new corrective scope → DoW for the new corrective scope → DoR for the recorded resume phase or explicitly stated earlier phase; the prior terminal outcome's DoF and DoW, closed-phase DoD, and next-phase DoR are not applicable. | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied or a DoW condition of the new corrective scope is active; fail when the new corrective scope's DoF determines failure. |

**Rejected and Blocked Results per Action (`full`)**

| Action | Answers `rejected` (nothing is written, `changed` is `false`) | Answers `blocked` (the evaluation is recorded, `changed` is `true`) |
|---|---|---|
| `start` | The phase does not have the status `ready`, the start is not authorized, or an applicable gate does not allow the start or cannot be evaluated (issue code `start-blocked`). | Never. |
| `complete` | The phase and status are not a legal source. | DoW, current-phase DoR, or current-phase DoD does not allow the transition, including a wait that a soft fail condition or a gate that cannot be evaluated causes. |
| `wait` | The change is closed, or no DoW condition is active. | Never. |
| `resume` | The status is not `waiting`, the resume condition is not satisfied, or the resume phase is closed. | The resume-phase DoR is not satisfied, or a DoW condition is still active, so that the change remains `waiting`. |
| `fail` | The change is closed, or no soft failure awaits disposition, so that an active DoF condition of the severity `hard` alone does not allow the action. | Never. |
| `cancel` | The change is closed, or no authorized cancellation decision exists. | Never. |
| `supersede` | The change is closed, no later change is authorized to replace this change, or the gate definitions differ from the approved ones (issue code `gates-changed`, Section 24.1). | Never. |
| `reopen` | The change is not in the `closed` phase, the corrective follow-up work is not authorized with a reason and a new goal-bound scope, the resume-phase DoR is not satisfied, or a Definition of Wait condition of the new corrective scope is active. | Never. |

An action whose evaluation closes the change as failed answers `success` (Section 24.7). An action answers `blocked` only where this table lists a case, and a `complete` that preserves the current phase with the status `done` because the next-phase DoR is not satisfied answers `success`. See AE-121, AE-122, AE-123, AE-124.

Section 24.2 states what `wait`, `fail`, `cancel`, `supersede`, and `reopen` of the `full` profile answer when a gate that applies to them cannot be evaluated.

The contract operations `approve`, `ask`, `answer`, `adopt`, and `migrate` (Sections 22.1, 24.3, 24.4, 24.8, and 25.3) are not rows of this table: they leave the phase and the status unchanged, and each is recorded under its own action name (Section 25.1).

**AE-121 — Complete is blocked when the Definition of Done is not satisfied**

- Covers: Section 8.3

Given a `full` change in the build phase with the status `active` whose Definition of Done is not satisfied  
When the `complete` action is requested  
Then the result is `blocked` with `changed` true, the issues name the unsatisfied criteria, the evaluation is recorded in the history, and the phase and status do not change

**AE-122 — Complete from a status that is not a legal source is rejected**

- Covers: Section 8.3

Given a `full` change in the build phase with the status `waiting`  
When the `complete` action is requested  
Then the result is `rejected` with `changed` false, and nothing is written to the history

**AE-123 — Resume is blocked when the resume-phase Definition of Ready is not satisfied**

- Covers: Section 8.3

Given a `full` change with the status `waiting`, whose resume condition is satisfied and whose resume-phase Definition of Ready is not satisfied  
When the `resume` action is requested  
Then the result is `blocked` with `changed` true, the evaluation is recorded in the history, and the change remains `waiting`

**AE-124 — Start with an unmet gate is rejected**

- Covers: Section 8.3

Given a `full` change whose phase has the status `ready` and a Definition of Wait condition that is active  
When the `start` action is requested  
Then the result is `rejected` with `changed` false and the issue code `start-blocked`, and the status remains `ready`

See AE-239, AE-240, AE-241, AE-242, AE-243, AE-244, AE-245, AE-246, AE-295, AE-296, AE-297, AE-298, AE-308, AE-310.

**AE-239 — Start a ready phase**

- Covers: Section 8.3 (`start`)

Given a `full` change in the build phase with the status `ready`, an authorization to start, and no Definition of Fail or Definition of Wait condition active, and a second `full` change in the build phase with the status `draft`  
When the `start` action is requested for each change  
Then the first change has the status `active` in the same phase, and the request for the second change is rejected with `changed` false, because `draft` is not a legal source of `start`

**AE-297 — Start is rejected when a gate cannot be evaluated**

- Covers: Section 8.3 (`start`)

Given a `full` change whose phase has the status `ready`, an authorization to start, and a Definition of Wait condition that cannot be evaluated because version control is unavailable  
When the `start` action is requested  
Then the result is `rejected` with `changed` false and the issue code `start-blocked`, the status remains `ready`, and no wait state is created

**AE-240 — Complete a phase, with and without the next Definition of Ready**

- Covers: Section 8.3 (`complete`)

Given a `full` change in the build phase with the status `active`, whose Definition of Done is satisfied and whose next-phase Definition of Ready is satisfied, and a second such change whose next-phase Definition of Ready is not satisfied  
When the `complete` action is requested for each change  
Then the first change advances to the verify phase with the status `ready`, and the second change stays in the build phase with the status `done` and the result `success`

**AE-241 — Wait only while a Definition of Wait condition is active**

- Covers: Section 8.3 (`wait`)

Given a `full` change in the plan phase with the status `active` and an active Definition of Wait condition, and a second `full` change in the plan phase with the status `active` and no such condition  
When the `wait` action is requested for each change  
Then the first change has the status `waiting` in the same phase, and the request for the second change is rejected with `changed` false

**AE-295 — A wait request on a change with a hard failure closes the change as failed**

- Covers: Section 8.3 (`wait`)

Given a `full` change in the plan phase with the status `active`, an active Definition of Wait condition, and an active Definition of Fail condition of the severity `hard`  
When the `wait` action is requested  
Then the change is in the `closed` phase with the status `failed`, the result is `success`, and no wait state is recorded

**AE-242 — Resume when the resume condition holds**

- Covers: Section 8.3 (`resume`)

Given a `full` change with the status `waiting` in the build phase whose resume condition is satisfied and whose resume-phase Definition of Ready is satisfied, and a second waiting change whose resume condition is not satisfied  
When the `resume` action is requested for each change  
Then the first change returns to the build phase with the status `active`, and the request for the second change is rejected with `changed` false, so that it remains `waiting`

**AE-243 — Fail only while a soft failure awaits disposition**

- Covers: Section 8.3 (`fail`)

Given a `full` change in the verify phase with the status `waiting` because of an active Definition of Fail condition of the severity `soft`, and a second `full` change in the verify phase with no soft failure that awaits disposition  
When the `fail` action is requested for each change  
Then the first change is in the `closed` phase with the status `failed`, and the request for the second change is rejected with `changed` false

**AE-308 — Fail is refused when only a hard failure is active**

- Covers: Section 8.3 (`fail`)

Given a `full` change in the verify phase with the status `active` and an active Definition of Fail condition of the severity `hard`, and no soft failure that awaits disposition  
When the `fail` action is requested  
Then the result is `rejected` with `changed` false, and the change keeps its phase and its status

**AE-244 — Cancel is not prevented by a wait, and a failure has priority**

- Covers: Section 8.3 (`cancel`)

Given a `full` change in the build phase with the status `waiting` because of an active Definition of Wait condition and an authorized cancellation decision, and a second such change that also has an active Definition of Fail condition  
When the `cancel` action is requested for each change  
Then the first change is in the `closed` phase with the status `cancelled`, and the second change is in the `closed` phase with the status `failed`, because the Definition of Fail has first priority

**AE-298 — Cancel proceeds when a gate cannot be evaluated**

- Covers: Section 8.3 (`cancel`)

Given a `full` change in the build phase with the status `active`, an authorized cancellation decision, and a Definition of Fail condition that cannot be evaluated because its program is missing  
When the `cancel` action is requested  
Then the change is in the `closed` phase with the status `cancelled`, and the result `not_evaluable` of the condition is recorded with its cause

**AE-310 — A full change rejects wait, fail, and reopen when a gate cannot be evaluated**

- Covers: Section 8.3 (full: `wait`, `fail`, and `reopen`)

Given three `full` changes with no active Definition of Fail condition of the severity `hard` and, in each, a Definition of Fail condition that applies to the action and cannot be evaluated because its program is missing: a change in the plan phase with the status `active` and an active Definition of Wait condition, a change in the verify phase with the status `waiting` because of an active Definition of Fail condition of the severity `soft`, and a change in the `closed` phase with the status `done` whose resume phase recorded at closure is the build phase, with a reason and a new goal-bound scope authorized, a satisfied resume-phase Definition of Ready, and no active Definition of Wait condition of the new corrective scope  
When the `wait` action is requested for the first change, the `fail` action for the second, and the `reopen` action for the third  
Then each result is `rejected` with `changed` false and the issue code `gate-not-evaluable`, nothing is written to the history, no wait state is created, and each change keeps its phase and its status

**AE-245 — Supersede needs a later change**

- Covers: Section 8.3 (`supersede`)

Given a `full` change in the plan phase and a later change that is authorized to replace it, and a second `full` change for which no later change is authorized  
When the `supersede` action is requested for each change  
Then the first change is in the `closed` phase with the status `superseded`, and the request for the second change is rejected with `changed` false

**AE-246 — Reopen a closed `full` change only from the `closed` phase**

- Covers: Section 8.3 (`reopen`)

Given a `full` change in the `closed` phase with the status `done` whose resume phase recorded at closure is the build phase, and a second `full` change in the build phase with the status `active`  
When the `reopen` action is requested for each change, with a reason and a new goal-bound scope  
Then the first change returns to the build phase with the status `active`, and the request for the second change is rejected with `changed` false, because that change is not in the `closed` phase

**AE-296 — Reopen of a `full` change is rejected when the new corrective scope would have to wait**

- Covers: Section 8.3 (`reopen`)

Given a `full` change in the `closed` phase with the status `done` whose resume phase recorded at closure is the build phase, and a Definition of Wait condition of the new corrective scope that is active  
When the `reopen` action is requested with a reason and a new goal-bound scope  
Then the result is `rejected` with `changed` false, and the change stays in the `closed` phase

### 8.4 Cancellation, Supersession, Reopening, and Terminal Behavior

`cancel` moves any non-closed phase/status to the `closed` phase with status `cancelled` when an authorized cancellation decision exists. `supersede` moves any non-closed phase/status to the `closed` phase with status `superseded` when a later change replaces this change's goal.

For `cancel` and `supersede`, an active DoW condition does not prevent the authorized terminal
action. DoW and the current- and next-phase readiness and completion gates are not applicable to
these actions. DoF retains first priority; when DoF determines that the change has failed, the
resulting terminal status is `failed` rather than `cancelled` or `superseded`. A gate that cannot be evaluated
determines no failure, so that the action takes effect (Section 24.2).

The comparison of the gate definitions with the approved ones (Section 24.1) does not stop `cancel`. It does stop `supersede`: while the gate definitions differ from the approved ones, `supersede` is rejected with the issue code `gates-changed`, and it can go ahead only after a human has approved the gate definitions again.

A fail condition of the severity `hard` closes the change as failed without human action, and a fail condition of the severity `soft` waits for a human, who either closes the change with `fail` or records an override (Section 24.7).

In the `full` method profile, `reopen` moves a change from the `closed` phase back to the resume phase recorded at closure, or to an explicitly stated earlier phase, for corrective follow-up work. The action MUST record its reason and the new goal-bound scope in history. The method profile `core` has no `reopen` action (Section 23.4). See AE-217.

In the `full` method profile, once a change is in the `closed` phase, no further phase advancement is legal except through `reopen`. A `closed` `core` change is final.

See AE-247.

**AE-217 — Reopen a closed `full` change**

- Covers: Section 8.4

Given a `full` change in the `closed` phase with the status `done`, whose resume phase recorded at closure is the build phase  
When the `reopen` action is requested with a reason and a new goal-bound scope, and the Definition of Ready of the build phase is satisfied  
Then the change is in the build phase with the status `active`, and the reason and the new scope are recorded in the history

**AE-247 — A wait does not prevent cancellation and a closed change does not advance**

- Covers: Section 8.4

Given a `full` change in the plan phase with the status `waiting` for an active Definition of Wait condition and an authorized cancellation decision, and a `full` change in the `closed` phase with the status `done`  
When the `cancel` action is requested for the first change, and the `complete` action is requested for the second  
Then the first change is in the `closed` phase with the status `cancelled`, because an active Definition of Wait condition does not prevent an authorized cancellation, and the request for the second change is rejected, because no phase advancement is legal in the `closed` phase except through `reopen`

### 8.5 Evaluation Priority

The following order MUST be applied during every gate evaluation:

1. DoF
2. DoW
3. DoR for the current phase
4. DoD for the current phase
5. DoR for the next phase

A satisfied DoD does not override a satisfied DoF or DoW.

This order defines evaluation precedence. A gate that is not applicable to the requested action or current state is skipped and, when gate evidence is recorded, MUST be recorded as `not_applicable`. Evaluation MUST stop as soon as a gate determines the requested action's outcome.

A gate evaluation has one of three results: `satisfied`, `not_satisfied`, or `not_evaluable`. A gate that cannot be evaluated is neither failed nor `not_applicable`: the change waits, except that the action `start` is rejected instead of waiting, `cancel` and `supersede` proceed, and `wait`, `fail`, and `reopen` of the `full` profile are rejected (Section 24.2), and a known hard failure is decided before it. Section 24.2 specifies these results and refines this order. It also states that the gates are evaluated by group, that a group is evaluated whole, and that the evaluation stops after the first group that decides.

See AE-248.

**AE-248 — The Definition of Fail is evaluated before the Definition of Wait and the Definition of Done**

- Covers: Section 8.5

Given a `full` change in the build phase with the status `active`, a satisfied Definition of Done, and an active Definition of Wait condition, and a second such change that also has an active Definition of Fail condition of the severity `hard`  
When the `complete` action is requested for each change  
Then the first request answers `blocked`, because the Definition of Wait decides before the Definition of Done and the later gates are not evaluated, and the second change is closed as failed, because the Definition of Fail decides first

---

## 9. Definition of Ready

This section specifies the `full` method profile (Section 5.6).

DoR determines whether a phase may begin.

### 9.1 Ready-to-Intake

At minimum:

- a request, problem, opportunity, or goal has been captured,
- the requestor or intake owner is identifiable,
- enough context exists to classify or route the work,
- no active DoF condition requires immediate failure handling.

See AE-260.

### 9.2 Ready-to-Explore

At minimum:

- the question, opportunity, or uncertainty to explore is described,
- the expected decision or learning outcome is identified,
- exploration boundaries and relevant constraints are known,
- an owner for the exploration is identified.

See AE-261.

### 9.3 Ready-to-Decide

At minimum:

- the decision to be made is stated,
- relevant exploration evidence and viable options are available,
- material tradeoffs, risks, and constraints are visible,
- the authorized decision owner is identified.

See AE-262.

### 9.4 Ready-to-Spec

At minimum:

- the goal or problem is described,
- the expected benefit is understandable,
- the requestor or decision owner is identified,
- known constraints are available,
- affected system areas are roughly known,
- no obvious conflict with the constitution exists.

A question about the goal or the problem that is still open is recorded as an open question of the change (Section 24.8). Ready-to-Spec is a statement about the criteria above alone. While the recorded question is unanswered, the `complete` action answers `blocked` (Section 24.8), and the Definition of Done of the specify phase is not satisfied.

See AE-263.

### 9.5 Ready-to-Plan

At minimum:

- goal, scope, and non-goals are defined,
- requirements and acceptance conditions are understandable,
- relevant architecture and ADR constraints have been reviewed,
- all open questions have been answered (Section 24.8),
- no unresolved contradictions exist.

See AE-264.

### 9.6 Ready-to-Build

At minimum:

- the specification is approved,
- the technical approach is sufficiently clear,
- critical risks have been assessed,
- required dependencies are available,
- test and verification criteria are defined,
- the allowed path list is stated (Section 24.5),
- no blocking decision is pending.

See AE-265.

### 9.7 Ready-to-Verify

At minimum:

- the planned implementation is complete or testable,
- relevant tests exist,
- build and analysis tools are available,
- known deviations are documented.

See AE-266.

### 9.8 Ready-to-Release

At minimum:

- build and required tests have succeeded,
- security and quality gates are satisfied,
- migration and rollback are clarified,
- known limitations are documented,
- required approvals are available.

See AE-267.

---

## 10. Definition of Done

This section specifies the `full` method profile (Section 5.6).

DoD determines whether a phase has been completed successfully.

### 10.1 Intake-Done

At minimum:

- the request is recorded and goal-bound,
- its class, risk, and applicable workflow are resolved sufficiently for routing,
- the next phase and responsible owner are identified,
- rejected, duplicate, or out-of-scope requests are dispositioned traceably.

A rejected, duplicate, or out-of-scope disposition ends the change through the `cancel` action
defined in Section 8.3, rather than satisfying this Definition of Done for forward advancement.

See AE-260.

**AE-260 — Intake is ready and done, and a duplicate ends by cancellation**

- Covers: Sections 9.1 and 10.1

Given a request that is captured with an identifiable requestor and enough context to route it, and a second request that is recorded as a duplicate of an existing change  
When the Definition of Ready and the Definition of Done of the intake phase are evaluated for each request  
Then the first request satisfies both, and its next phase and responsible owner are identified, and the duplicate is dispositioned through the `cancel` action and does not satisfy the Definition of Done for forward advancement

### 10.2 Explore-Done

At minimum:

- the stated question or uncertainty has been investigated within the approved boundaries,
- relevant observations, evidence, and limitations are recorded,
- viable options or a justified conclusion are available for decision,
- no production implementation has begun merely because exploration completed.

See AE-261.

**AE-261 — Exploration stays within its boundaries**

- Covers: Sections 9.2 and 10.2

Given an exploration whose question, expected learning outcome, boundaries, and owner are stated, and a second exploration during which production code was already written  
When the Definition of Ready and the Definition of Done of the explore phase are evaluated for each exploration  
Then the first exploration is ready and, once its observations and options are recorded, done, and the second does not satisfy the Definition of Done, because production implementation has begun

### 10.3 Decide-Done

At minimum:

- the authorized decision owner has recorded the selected option or disposition,
- the decision rationale and material tradeoffs are documented,
- consequences, constraints, and required follow-up are identified,
- any resulting specification work has an explicit goal-bound handoff.

See AE-262.

**AE-262 — A decision is recorded by its authorized owner**

- Covers: Sections 9.3 and 10.3

Given a decision whose statement, options, tradeoffs, and authorized decision owner are known, and a second decision whose selected option was recorded by a participant who is not the authorized decision owner  
When the Definition of Ready and the Definition of Done of the decide phase are evaluated for each decision  
Then the first decision is ready and, once the owner records the option, the rationale, and the consequences, done, and the second does not satisfy the Definition of Done, because the authorized decision owner has not recorded the selected option

### 10.4 Spec-Done

At minimum:

- goal, benefit, and success signals are described,
- scope and non-goals are defined,
- requirements are unambiguous and verifiable,
- each behavioral requirement has at least one concrete acceptance example, or a justified alternative verifiable acceptance condition exists,
- constraints are documented,
- all open questions have been answered (Section 24.8),
- ADR conflicts are resolved or returned to the requestor,
- the specification is approved.

See AE-263.

**AE-263 — A specification is done only with its questions answered and approved**

- Covers: Sections 9.4 and 10.4

Given a specification whose goal, benefit, requestor, and constraints are known and that conflicts with no rule of the constitution, and a second specification with one unanswered question  
When the Definition of Ready and the Definition of Done of the specify phase are evaluated for each specification, and the `complete` action is requested for the second  
Then the criteria of Ready-to-Spec are met for both, and for the second the `complete` action answers `blocked` and the Definition of Done is not satisfied, because every open question has to be answered (Section 24.8) and the specification has to be approved

### 10.5 Plan-Done

At minimum:

- the technical approach is described,
- affected components are identified,
- architecture, data, API, and operational impacts are assessed,
- the test strategy is defined,
- migration and rollback needs are clarified,
- risks and decisions are documented,
- implementation is decomposed appropriately.

See AE-264.

**AE-264 — Planning needs answered questions and a test strategy**

- Covers: Sections 9.5 and 10.5

Given a specification with defined goal, scope, and non-goals whose open questions are all answered, a second specification with one unanswered question, and a plan that describes no test strategy  
When the Definition of Ready of the plan phase is evaluated for the two specifications, and the Definition of Done of the plan phase is evaluated for the plan  
Then the first specification is ready, the second is not ready, because a question is unanswered, and the plan does not satisfy the Definition of Done, because the test strategy is not defined

### 10.6 Build-Done

At minimum:

- all approved changes are implemented,
- no unintended scope has been introduced,
- tests have been added or updated,
- local quality gates have succeeded,
- required documentation is updated,
- deviations from the specification are explained and approved.

Whether unintended scope has been introduced is measured as Section 24.5 states.

See AE-265.

**AE-265 — A build is done only within its scope**

- Covers: Sections 9.6 and 10.6

Given an approved specification with a clear technical approach, assessed risks, available dependencies, and defined test criteria, a stated allowed path list, and a build in which a path outside that list changed  
When the Definition of Ready and the Definition of Done of the build phase are evaluated  
Then the specification is ready to build, and the build does not satisfy the Definition of Done, because unintended scope has been introduced, which is a hard failure (Section 24.5)

### 10.7 Verify-Done

At minimum:

- all acceptance conditions have been verified,
- required automated tests have succeeded,
- relevant negative and failure cases have been checked,
- regression tests have succeeded,
- evidence is complete,
- remaining limitations are documented.

A verification gate MAY carry a baseline of known failures (Section 24.6).

Evidence is complete as Section 24.9 defines it.

See AE-266.

**AE-266 — Verification needs complete executable evidence**

- Covers: Sections 9.7 and 10.7

Given an implementation that is testable, with existing tests and available build tools, and a verification in which one requirement has no evidence command  
When the Definition of Ready and the Definition of Done of the verify phase are evaluated, and `complete` is requested  
Then the implementation is ready to verify, and the verification does not satisfy the Definition of Done, because the evidence is not complete (Section 24.9), so that `complete` answers `blocked`

### 10.8 Release-Done

At minimum:

- deployment or publication has succeeded,
- smoke tests have succeeded,
- version and release notes are documented,
- monitoring shows no critical problems,
- rollback is possible or explicitly not required,
- required release approval has been recorded by an authorized human decision owner,
- roadmap and status are updated.

See AE-267.

**AE-267 — A release is done only with a human release approval**

- Covers: Sections 9.8 and 10.8

Given a release whose build and tests succeeded, whose migration and rollback are clarified, and whose approvals are available, and a second release whose approval was recorded by the identity `agent:releaser`  
When the Definition of Ready and the Definition of Done of the release phase are evaluated for each release  
Then the first release is ready, and the second does not satisfy the Definition of Done, because the required release approval has to be recorded by an authorized human decision owner (Sections 5.4 and 24.3)

---


### 16.1 `spec.md`

```markdown
# Change: <Title>

## Metadata

- Change ID: <id>
- Class: S | M | L
- Phase: specify
- Status: draft
- Requestor: <name-or-role>

## Goal

<Desired target state and benefit>

## Success Signals

- <measurable or verifiable signal>

## Non-Goals

- <explicitly excluded outcome>

## Context

<relevant current state>

## Scope

### Included

- <included item>

### Excluded

- <excluded item>

### Allowed Paths

- <path pattern>

## Requirements

### R1 — <Title>

<verifiable requirement>

#### Evidence Commands

- <argument list and exit map>

## Acceptance Examples

### E1 — <Title>

- Covers: R1

Given <initial state>  
When <action>  
Then <result>

## Constraints

- <project-wide or local constraint>

## Flow Gates

### Additional Ready Conditions

- <optional>

### Additional Done Conditions

- <optional>

### Additional Wait Conditions

- <optional>

### Additional Fail Conditions

- <optional>

## Verification

- <evidence or test>

## Pair Review

- Required: yes | no
- Requestor: <participant-id>
- Reviewer: <distinct-participant-id>
- Scope: <artifacts and criteria>

## Open Questions

- None.
```

The conditions listed under Flow Gates, together with the scope, are the gate definitions of the change and are fixed when the change is approved (Section 24.1).

The Change ID follows the syntax of the identifier of a change in Section 4.3.

The list under the heading Allowed Paths of the Scope is the allowed path list of the change. It holds path patterns that can be checked by machine, and Section 24.5 states how they are written and measured. The Included and Excluded lists describe the scope in words and are not measured. See AE-311.

The list under the heading Evidence Commands of a requirement holds the evidence commands that are bound to it as Section 24.9 states. Each list item states the argument list, the exit map, and optionally the time limit of one command. The requirement identifiers and these lists are fixed with the gate definitions (Section 24.1), and a requirement without a list item has no evidence command.

The section Open Questions of the change specification is a view of the questions that are recorded as state (Section 24.8).

**AE-311 — Full: a change specification states its gate conditions, its allowed paths, and its evidence commands under fixed headings**

- Covers: Section 16.1

Given a `full` change specification whose Additional Done Conditions list holds the one item `run-tests --suite unit`, whose Additional Ready Conditions, Additional Wait Conditions, and Additional Fail Conditions lists hold only the marker `<optional>`, whose Allowed Paths list holds `lib/**` and whose Excluded list holds the item `the build scripts`, and whose requirement R1 holds the item `run-tests --suite unit` with the exit map `0` to `satisfied` under the heading Evidence Commands  
When the gate definitions of the change are read from the specification  
Then the Done conditions are the one condition `run-tests --suite unit`, the other three lists are empty because the marker `<optional>` is not a condition, the allowed path list is `lib/**`, the Excluded list is not measured, and the evidence commands of R1 are the one item under its heading

### 16.2 `plan.md`

```markdown
# Implementation Plan: <Title>

## Technical Approach

<selected approach>

## Affected Components

- <component>

## Architecture Impact

- <impact or None>

## Data and API Impact

- <impact or None>

## Test Strategy

- <test level and coverage>

## Migration and Rollback

- <strategy or Not required>

## Risks

- <risk and mitigation>

## Decisions

- <decision with reference>

## Implementation Sequence

1. <step>
2. <step>
```

### 16.3 `tasks.md`

```markdown
# Implementation Checklist

- [ ] <actionable step>
- [ ] Add or update tests.
- [ ] Run quality gates.
- [ ] Update documentation.
- [ ] Perform a spec-to-code consistency check.
- [ ] Capture evidence.
```

### 16.4 `evidence.md`

```markdown
# Verification Evidence

## Requirement Coverage

| Requirement | Evidence | Result |
|---|---|---|

## Quality Gates

- Build:
- Tests:
- Static analysis:
- Security:

## Pair Review

- Review ID:
- Required: Yes | No
- Result:

| Participant | Role | Reviewed Revision | Action | Timestamp | Result | Findings | Disposition |
|---|---|---|---|---|---|---|---|
| <participant-id> | Requestor | <exact-revision> | <action> | <timestamp> | <result> | <reference-or-summary> | <disposition> |
| <distinct-participant-id> | Reviewer | <exact-revision> | <action> | <timestamp> | <result> | <reference-or-summary> | <disposition> |

### Findings

| ID | Severity | Summary | Status |
|---|---|---|---|

## Deviations

- None.

## Final Gate Evaluation

- DoF triggered: No
- DoW triggered: No
- DoD satisfied: Yes | No
- Next DoR satisfied: Yes | No | Not applicable
- Gates that could not be evaluated: None | <gate and cause>

## Final Status

<status>
```

A gate that could not be evaluated is not recorded as Yes or No in the Final Gate Evaluation. It is listed by name with its cause (Section 24.2). See AE-312.

The Evidence column of the requirement coverage table points at the evidence commands that stand under the heading Evidence Commands of the requirement in the change specification (Sections 16.1 and 24.9) and records what they produced. Other records MAY be added to it. See AE-312.

**AE-312 — Full: the evidence lists a gate that could not be evaluated, and the coverage table names the evidence commands**

- Covers: Section 16.4

Given a `full` change in the verify phase whose Definition of Done holds the condition `run-tests --suite unit`, which could not be evaluated because its program is missing, and whose requirement R1 has the evidence command `check-docs --strict` under its heading Evidence Commands, which ran  
When the evidence of the change is written  
Then the line Gates that could not be evaluated of the Final Gate Evaluation names `run-tests --suite unit` with the cause that its program is missing, the condition is not recorded as Yes or No, and the Evidence cell of R1 in the requirement coverage table points at the evidence command `check-docs --strict` and records what it produced



## 21. Quick Reference

```text
Goal
  ↓
Definition of Ready
  ↓
Active Phase
  ├── Definition of Fail → FAILED
  ├── Definition of Wait → WAITING
  └── Definition of Done → DONE
                              ↓
                    Next Definition of Ready
                              ↓
                         Next Phase
```

The diagram above shows the `full` flow (Section 5.6). The flow of `core` is given by the transition table of Section 23.4 of the normative specification.

---

## Appendix A. Acceptance Examples of the `full` Method Profile

These examples were removed from the normative specification with the `full` method profile. Their numbers are those of version 1.4 and are not numbers of the normative specification.

**AE-227 — The approved exception applies to one `full` change only**

- Covers: Section 5.3

Given a project-wide definition of done under `docs/definitions/` with a regression-test criterion, and a `full` change whose local specification states that this criterion does not apply, together with an exception approved by `human:ada` at the level that the approval of gate definitions requires  
When the change is checked before approval, and a second `full` change without an exception is checked as well  
Then the first change is accepted without the criterion and the exception is recorded, and the second change is rejected with the issue code `gate-weakened` and `changed` false, as weakening the project-wide definition

**AE-02 — Use the default method profile**

- Covers: Section 5.6

Given a project whose configuration names the default method profile `core`  
When a change is created that selects no method profile  
Then the change is created with the recorded method profile `core`

**AE-03 — Reject creation with no method profile and no default**

- Covers: Section 5.6

Given a project whose configuration names no default method profile  
When a change is created that selects no method profile  
Then the creation is rejected, and no change is created

**AE-05 — Reject an in-place switch of the method profile**

- Covers: Section 5.6

Given an active change whose recorded method profile is `core`  
When an operation sets the method profile of that change to `full`  
Then the operation is rejected, and the recorded method profile remains `core`

**AE-06 — Move to the other method profile by a new change and supersede**

- Covers: Section 5.6

Given an active change A whose method profile is `full`  
When a new change B is created with the method profile `core` and change A is superseded by change B  
Then change B is a `core` change in the state `open`, change A is closed as replaced by change B, and no state of change A is mapped onto a state of change B

**AE-07 — Reject a second supersede of a closed change**

- Covers: Section 5.6

Given a change A that is closed because change B superseded it  
When another change C is created and the `supersede` action of change A by change C is requested  
Then the request is rejected, because change A is closed, and change A remains replaced by change B

**AE-268 — Full: a wait state names a safe current state and a next action**

- Covers: Section 11.2

Given a `full` change with the status `active` and an active Definition of Wait condition, and a request to wait that gives the fields `reason`, `outstanding`, `owner`, and `resume_when`, with the fields `safe_state` and `next_action` in one request and without them in the other  
When the `wait` action is requested twice, once with and once without the safe current state and the next action  
Then the request that gives all six fields is recorded as a wait state, and the request that gives no safe current state and no next action is rejected with `changed` false, because every wait state of a `full` change includes them

**AE-269 — Full: a fail rule names its final status**

- Covers: Section 12.2

Given a `full` fail rule that states a trigger, a required response, permitted preservation actions, the final status `FAILED_POLICY_VIOLATION`, the required documentation, and the severity `hard`, and a second fail rule that states no final status  
When the two rules are validated, and the first rule becomes active on a `full` change  
Then the first rule is valid, and its final status code `FAILED_POLICY_VIOLATION` is recorded when the change is closed as failed, and the second rule is invalid, because every fail rule of a `full` change includes a final status

**AE-59 — A `core` change has no size class**

- Covers: Section 23.1

Given a `core` change whose scope would be a Class L initiative under Section 6  
When the change is created  
Then Section 6 does not apply, the change is one `core` change, and no decomposition into several changes is required

**AE-249 — Full: changed Flow Gates or project-wide definitions are rejected**

- Covers: Section 24.1 (full)

Given a `full` change whose Flow Gates, allowed path list, and the project-wide definitions under `docs/definitions/` were approved, with nothing changed since  
When `complete` is requested, then a condition is added under Additional Done Conditions and `complete` is requested again, then the condition is removed, a file under `docs/definitions/` is edited, and `complete` is requested a third time  
Then the first request is evaluated, and the second and third requests are rejected with the issue code `gates-changed` and `changed` false, because the content hash of the parsed gate definitions differs from the approved hash

**AE-250 — Full: a condition that cannot be evaluated is a wait**

- Covers: Section 24.2 (full)

Given a `full` change in the verify phase whose Definition of Done holds a check-command condition whose program does not exist, and a second change whose condition runs and exits with a status that the exit map assigns to `satisfied`  
When `complete` is requested for each change  
Then the first condition is `not_evaluable`, the result is `blocked`, the change is `waiting` with the category `WAIT_EXTERNAL_SYSTEM`, and no failure is recorded, and the second condition is `satisfied`

**AE-251 — Full: the approval of the specification needs a human**

- Covers: Section 24.3 (full)

Given a `full` change whose specification awaits approval, the identity `agent:builder`, and the identity `human:ada` with a claim at the level that the project configuration requires  
When each identity approves the specification  
Then the approval by `agent:builder` is rejected, because an approval is performed by a human, and the approval by `human:ada` is recorded in the state file with the identity, the level, and the content hash of the specification

**AE-252 — Full: the history is checked where a state file exists**

- Covers: Section 24.4 (full)

Given a `full` change whose state file has an entry that was altered after it was recorded, and a second `full` change that keeps its record inline in `spec.md`  
When an operation that reads the history is requested for each change  
Then the first operation is refused, because the history is not consistent, and for the second change the rules that read or write the history are not enforced mechanically and the implementation does not report them as enforced

**AE-253 — Full: the allowed path list is measured**

- Covers: Section 24.5 (full)

Given a `full` change that has started and whose Scope lists the allowed path `src/billing/**`, and a second started `full` change whose specification states no allowed path list  
When a file under `docs/` is found changed since the base revision of the first change, and the scope of the second change is measured  
Then the first change has a scope violation, which is a hard failure naming the path, and the scope of the second change is `not_evaluable`, which is neither `satisfied` nor a violation

**AE-294 — Full: the scope is evaluated from the first approval of the gate definitions**

- Covers: Section 24.5 (full)

Given a `full` change whose specification states no allowed path list, with a complete specification otherwise, and whose gate definitions are not yet approved  
When the scope is measured before the approval, the gate definitions are approved, and the scope is measured again and the Definition of Ready of the build phase is evaluated  
Then the record shows `not_applicable` before the approval and `not_evaluable` after it, and the change is not ready to build, because the allowed path list is not stated

**AE-254 — Full: a verification condition carries a baseline**

- Covers: Section 24.6 (full)

Given a `full` change whose Verify-Done condition names a check command with a baseline of two known failing tests  
When the command fails exactly those two tests in one run, and those two and a third test in another run  
Then the first run is `satisfied`, and the second run is `not_satisfied` and names the third test as a new failure

**AE-255 — Full: hard and soft fail rules differ**

- Covers: Section 24.7 (full)

Given a `full` change with a fail rule of the severity `hard` that becomes active, and a second `full` change with a fail rule of the severity `soft` that becomes active  
When `complete` is requested for each change  
Then the first change is closed with the status `failed` without human action, and the second change is `waiting` with the category `WAIT_DECISION` until a human closes it with `fail` or records an override

**AE-256 — Full: an unanswered question keeps a wait condition active**

- Covers: Section 24.8 (full)

Given a `full` change with an unanswered question Q1 in its state file whose owner is `human:ada`  
When `complete` is requested, then `human:ada` answers Q1, and `complete` is requested again  
Then the first request answers `blocked`, because a Definition of Wait condition is active while Q1 is unanswered, the answer is recorded as a human decision, and after it the condition is no longer active

**AE-257 — Full: Verify-Done needs executable evidence for every requirement**

- Covers: Section 24.9 (full)

Given a `full` change in the verify phase with two requirements and an evidence command bound to the first requirement only  
When `complete` is requested, then an evidence command is added for the second requirement, the gate definitions are approved again, both commands are `satisfied`, and `complete` is requested again  
Then the first request answers `blocked`, because the evidence is not complete, and the second request is not blocked by the evidence

**AE-286 — Full: a replaced evidence command needs a new approval**

- Covers: Section 24.9 (full)

Given a `full` change whose gate definitions were approved with the item `run-tests --suite unit` and the exit map `0` to `satisfied` under the heading Evidence Commands of the requirement R1, and a second approved `full` change with the same kind of item  
When in the first change the item is replaced by a command that always ends with the exit status that its exit map maps to `satisfied`, in the second change only the white space inside the item is changed, and `complete` is requested for each  
Then the request for the first change is rejected with the issue code `gates-changed` and `changed` false, and the replaced command has no effect until a human approves the gate definitions again, and the request for the second change is evaluated, because a run of white space does not change the parsed value

**AE-258 — Full: a Flow Gates command runs without a shell**

- Covers: Section 24.10 (full)

Given a `full` change with a Flow Gates condition whose command is the argument list `@interpreter` and `checks/run.py` in a project whose configuration names an interpreter, and a second condition whose command is the single element `make test && make lint`  
When both conditions are evaluated  
Then the first command runs with the configured interpreter and no shell, and the second is run as one program name without a shell, which does not exist, so that the condition is `not_evaluable`

**AE-259 — Full: only complete and resume answer blocked**

- Covers: Section 22.2 (full)

Given a `full` change in the build phase with the status `active` whose Definition of Done is not satisfied, and a `full` change in the plan phase with the status `ready` and an active Definition of Wait condition  
When the `complete` action is requested for the first change, and the `start` action is requested for the second  
Then the first result is `blocked` with `changed` true and the evaluation is recorded, and the second result is `rejected` with `changed` false, because in `full` only `complete` and `resume` answer `blocked`

**AE-71 — A gate that cannot be evaluated puts a `full` change in a wait**

- Covers: Section 24.2

Given a `full` change in the build phase with the status `active`, whose Definition of Done includes a check-command gate that cannot be evaluated because version control is unavailable  
When the `complete` action is requested  
Then the change has the status `waiting` in the build phase with a wait state of the category `WAIT_EXTERNAL_SYSTEM`, and no failure is recorded

**AE-300 — Full: a Definition of Ready of the current phase that is not satisfied blocks the completion**

- Covers: Section 24.2 (full)

Given a `full` change in the build phase with the status `draft` whose Definition of Ready of the current phase is not satisfied  
When the `complete` action is requested  
Then the result is `blocked` with `changed` true, the evaluation is recorded in the history, and the status stays `draft`

**AE-182 — An unanswered question blocks a `full` change**

- Covers: Section 24.8

Given a `full` change in the specify phase with the status `active` and the unanswered question Q1 in its state file  
When the `complete` action is requested  
Then the result is `blocked` with `changed` true, the issues name Q1, and the phase and status do not change

**AE-301 — Full: asking a question is the action ask and changes neither the phase nor the status**

- Covers: Section 24.8 (full)

Given a `full` change in the build phase with the status `active`  
When a participant records a question with a text and the owner of the change  
Then the entry has the action `ask`, the phase and the status are unchanged, and the question is unanswered

**AE-170 — A `full` change needs an executable check for Verify-Done**

- Covers: Section 24.9

Given a `full` change in the verify phase with the status `active`, whose requirement R1 has no item under its heading Evidence Commands and only a screenshot in the Evidence cell of its requirement coverage table  
When the `complete` action evaluates the Definition of Done of the phase  
Then the criterion that evidence is complete is not satisfied, and the phase is not completed
