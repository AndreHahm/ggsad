# GG-SAD — Normative Method Specification

**Version:** 1.3
**Status:** Normative Baseline  
**Revision:** 2026-08-19 — Clarified authority, artifact, transition, tailoring, Pair Review evidence, and minimal automation contracts.
**Target audience:** AI agents, workflow engines, automation systems, and technical project owners

---

## 1. Purpose

**Goal-Gated Spec-Anchored Development (GG-SAD)** is a lightweight, goal-oriented development method for specification-driven software development.

GG-SAD defines:

- a binding document hierarchy,
- a phase-based development flow,
- explicit entry, completion, waiting, and failure conditions,
- minimal artifacts per change,
- rules for deviations, decisions, and evidence,
- controlled use of AI agents.

GG-SAD does not require epics, sprints, story points, role models, or ceremonies. The primary unit of work is a **goal-bound change**.

GG-SAD MUST be usable in two operating modes:

- **stand-alone mode**, where GG-SAD provides the governing method and execution flow;
- **combination mode**, where GG-SAD governs goals, gates, evidence, state, and precedence while another method, framework, tool, or agent platform supplies planning, execution, review, context engineering, or automation capabilities.

### 1.1 Document Scope and Category Map

This specification is the leading GG-SAD semantic and product baseline. The precedence list in Section 4, Document Hierarchy, governs artifacts inside a GG-SAD-managed project; it does not rank this specification itself, which remains superior to every document ordered by that list.

A GG-SAD implementation MAY be developed using another development method. That development method MAY govern implementation work, but it MUST NOT redefine the GG-SAD product semantics established by this specification.

| Section | Category |
|---|---|
| 1. Purpose | Authority & Applicability |
| 2. Normative Terms | Method Semantics |
| 3. Core Principles | Method Semantics |
| 4. Document Hierarchy | Project Governance |
| 5. Workflow and Compliance Tailoring | Project Governance |
| 6. Size Classes | Method Semantics |
| 7. Phase Model | Method Semantics |
| 8. State Model | Method Semantics |
| 9. Definition of Ready | Method Semantics |
| 10. Definition of Done | Method Semantics |
| 11. Definition of Wait | Method Semantics |
| 12. Definition of Fail | Method Semantics |
| 13. Conflict and Decision Rules | Method Semantics |
| 14. Pair Review Model | Method Semantics |
| 15. Evidence Model | Method Semantics |
| 16. Minimum Templates | Reference-Implementation Requirements |
| 17. Combination Contracts | Optional Integration Guidance |
| 18. GG-SAD Memory Model | Optional Integration Guidance |
| 19. Agent Execution Algorithm | Reference-Implementation Requirements |
| 20. Completion Criteria for a Change | Method Semantics |
| 21. Quick Reference | Method Semantics |
| 22. Minimal Automation Contract | Reference-Implementation Requirements |

---

## 2. Normative Terms

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted normatively.

- **MUST / MUST NOT:** mandatory requirement.
- **SHOULD / SHOULD NOT:** strong recommendation; deviations require justification.
- **MAY:** optional capability or approach.

---

## 3. Core Principles

### 3.1 Goal First

Every change MUST have an explicit goal.

The goal MUST describe:

- which problem is being solved,
- which desired state is to be achieved,
- how achievement of the goal will be recognized,
- which outcomes are explicitly outside the change.

### 3.2 Spec Anchoring

The specification is the binding anchor of a change.

Code, tests, plans, and evidence MUST conform to the approved specification. The specification does not replace architecture decisions or project-wide rules.

### 3.3 Gate-Controlled Flow

Every phase transition MUST be controlled by defined gates:

- **Definition of Ready (DoR):** May the next phase begin?
- **Definition of Done (DoD):** Has the current phase been completed successfully?
- **Definition of Wait (DoW):** Must the flow pause in a controlled manner?
- **Definition of Fail (DoF):** Must the flow terminate unsuccessfully?

### 3.4 Evidence over Assertion

A status MUST NOT be set solely by assertion. Verifiable evidence MUST exist for relevant completion criteria.

### 3.5 One Fact, One Home

Each piece of information SHOULD have exactly one authoritative location.

Duplication across documents SHOULD be avoided. References are preferable to copies.

### 3.6 Risk-Based Scaling

Artifacts and process steps MUST be scaled according to risk, uncertainty, impact, and the selected compliance profile, not only according to estimated effort.

### 3.7 Tailorable but Invariant Core

GG-SAD workflows MUST be tailorable. Tailoring MAY change enabled phases, required artifacts, review depth, approval rules, evidence depth, permissions, and automation.

Tailoring MUST NOT remove the invariant core:

- an explicit goal,
- a specification anchor appropriate to the change size,
- gate evaluation,
- evidence appropriate to the selected profile,
- controlled wait and fail behavior,
- traceable final status.

### 3.8 Stand-Alone and Combination Use

GG-SAD MUST remain independent from a specific planning framework, coding agent, IDE, issue tracker, or delivery platform.

In combination mode:

- GG-SAD owns governance semantics, state, gates, precedence, and closure;
- the integrated method or tool MAY own subordinate planning or execution artifacts;
- mapped external artifacts MUST identify their GG-SAD role;
- external workflows MUST NOT bypass GG-SAD gates or weaken the active compliance profile;
- conflicts MUST be resolved according to the GG-SAD document hierarchy.

---

### 3.9 Example-Driven Specification

Every behavioral requirement MUST include at least one concrete acceptance example.

An acceptance example SHOULD identify:

- the relevant initial state,
- the triggering action or event,
- the expected observable result,
- relevant negative, failure, or boundary behavior according to risk.

Given/When/Then MAY be used, but GG-SAD does not require a specific example notation. A requirement MAY omit an example only when an example would not improve clarity. The specification MUST then define an alternative verifiable acceptance condition and explain why an example is not applicable.

Acceptance examples MUST be traceable to requirements and verification evidence.

### 3.10 Pair Review

GG-SAD supports **Pair Review** as a controlled collaboration model between two distinct participants:

- the **Requestor** creates or changes a governed work product;
- the **Reviewer** independently reviews, verifies, tests, validates, or otherwise evaluates that work product and returns traceable findings to the Requestor.

The Requestor and Reviewer MUST be different participants within the same review cycle. Supported combinations include Human–Human, Human–Agent, Agent–Human, Agent–Agent, and Human or Agent with an external review service.

Pair Review is OPTIONAL by default. Its use and required depth MUST be resolved from the active compliance profile, project scope, change class, risk, impact, and project-specific policy. A project MAY require Pair Review for selected phases, artifact types, or risk categories.

The Reviewer MUST NOT silently modify the Requestor's governed work product as part of the review. Findings MUST be returned to the Requestor for disposition. A separate explicitly assigned change action MAY authorize the Reviewer to become a Requestor for a later correction cycle.

Pair Review MUST NOT replace a required human approval. Where segregation of duties applies, the project MAY require Requestor, Reviewer, and Approver to be three distinct participants.

## 4. Document Hierarchy

### 4.1 Binding Order of Precedence

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

### 4.2 Project-Wide Documents

```text
docs/
├── constitution.md
├── project-brief.md
├── architecture.md
├── roadmap.md
├── definitions/
│   ├── definition-of-ready.md
│   ├── definition-of-done.md
│   ├── definition-of-wait.md
│   └── definition-of-fail.md
└── adr/
    └── ADR-<number>-<title>.md
```

#### `constitution.md`

Contains non-negotiable project-wide rules, especially:

- quality principles,
- security principles,
- architecture principles,
- approval rules,
- prohibited actions and dependencies,
- rules for breaking changes,
- resource and budget limits,
- minimum requirements for tests and evidence.

#### `project-brief.md`

Describes the stable product and project context:

- problem and opportunity,
- target users and stakeholders,
- intended outcomes and success signals,
- project type and lifecycle context,
- scope boundaries and non-goals,
- business, delivery, budget, and time constraints,
- selected compliance profile,
- external methods, frameworks, tools, or agents used in combination mode.

The project brief MUST NOT contain architecture decisions that belong in ADRs.

#### `architecture.md`

Describes the current structural state of the system:

- system context,
- components and responsibilities,
- module and integration boundaries,
- data flows,
- deployment and operational structure,
- known technical constraints,
- references to relevant ADRs.

#### `roadmap.md`

Describes the intended direction of development. The roadmap SHOULD remain concise and MAY use the sections `Now`, `Next`, `Later`, and `Open`.

The roadmap is not a sprint or epic backlog.

#### `docs/definitions/`

Contains the project-wide standard gates. Local specifications MAY strengthen these rules, but MUST NOT weaken them without an approved exception.

#### `docs/adr/`

Contains durable architecture decisions. Existing accepted ADRs take precedence over new requirements and plans.

### 4.3 Change-Specific Documents

```text
specs/<change-id>/
├── state.yaml
├── spec.md
├── plan.md
├── tasks.md
├── evidence.md
└── review.md
```

`spec.md` remains the mandatory file for normal (Class M and Class L) changes as defined in Section 6.

Every change carries mandatory information regardless of file layout: the goal, specification anchor, gate outcome, evidence, wait or fail behavior when applicable, and final status.

`state.yaml` is a mandatory file only when the project uses persistent, machine-readable workflow state to track phase, status, gates, and history. When state is not persisted that way, the same mandatory information MAY instead be recorded inline in `spec.md` or `evidence.md`.

`plan.md`, `tasks.md`, `evidence.md`, and `review.md` remain conditional files. They are required only when the change's size, risk, evidence needs, or review-depth needs call for them.

Inline storage of any of this information is permitted only when its authoritative location and required fields are unambiguous.

---

## 5. Workflow and Compliance Tailoring

### 5.1 Compliance Profiles

Every project MUST select one active compliance profile in `.ggsad/config.yaml` and record it in `docs/project-brief.md`.

GG-SAD defines the following default profiles:

| Profile | Intended Use | Minimum Characteristics |
|---|---|---|
| `lean` | Pre-PMF MVPs, prototypes, solo development, fast iteration | Minimal artifacts, automated checks where available, self-approval permitted unless a critical rule applies |
| `standard` | Typical product and team development | Separate specification for normal changes, defined quality gates, recorded evidence, peer review where practical |
| `governed` | Enterprise or high-impact delivery | Strong traceability, explicit approvals, security and architecture review, controlled release evidence |
| `regulated` | Regulated, safety-critical, or externally audited work | Segregation of duties, immutable or retained evidence, formal approvals, compliance mappings, audit-ready history |

Projects MAY define additional profiles. Custom profiles MUST inherit from a default profile or explicitly document every invariant and deviation.

### 5.2 Tailoring Dimensions

A profile MAY tailor:

- enabled and skippable phases,
- required artifacts by change class,
- mandatory document sections,
- criterion severity,
- automatic, review, and approval checks,
- evidence retention and provenance,
- human approval requirements,
- Pair Review activation, reviewer independence, review scope, and finding severity rules,
- enabled practice profiles and combination recipes,
- agent permissions and autonomy,
- release, rollback, and monitoring requirements,
- integration mappings to external methods and tools.

A lower-compliance profile MAY reduce optional controls. It MUST NOT disable the invariant core defined in Section 3.7.

### 5.3 Profile Resolution

The effective workflow MUST be resolved in this order:

1. GG-SAD invariant core,
2. selected compliance profile,
3. project-specific configuration,
4. change-class requirements,
5. local strengthening in the change specification,
6. integration mappings for external frameworks and tools.

A lower layer MUST NOT silently weaken a higher layer.

### 5.4 Non-Delegable Human Approval

Regardless of the active compliance profile or the `lean` profile's self-approval allowance in Section 5.1, the following decisions MUST always be made by a human and MUST NOT be satisfied by agent self-approval:

- approval of a breaking change under Section 13;
- resolution of an ADR conflict requiring a decision under Section 13;
- any decision that would trigger a Definition of Fail condition under Section 12 if left unresolved;
- release approvals required by Ready-to-Release and Release-Done under Sections 9 and 10.

Self-approval under the `lean` profile is permitted only for decisions outside this non-delegable set.

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

## 6. Size Classes

### 6.1 Class S — Patch

Suitable for small, clearly bounded changes with a known solution and low risk.

Minimum artifact:

- inline specification in an issue, change request, or commit context.

Minimum content:

- goal,
- scope,
- acceptance conditions,
- verification.

### 6.2 Class M — Change

Suitable for self-contained functional or technical changes.

Mandatory artifact:

- `spec.md`

Optional artifacts:

- `plan.md`
- `tasks.md`
- `evidence.md`

### 6.3 Class L — Initiative

Suitable for multiple independent or interdependent changes.

An initiative MUST be decomposed into multiple change specifications. A short roadmap or dependency overview MAY be used. An epic is not required.

---

## 7. Phase Model

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

#### Standard Flow

```text
specify → plan → build → verify → closed
```

#### Release Flow

```text
specify → plan → build → verify → release → closed
```

#### Exploration Flow

```text
explore → decide → specify
```

Exploration MUST NOT silently transition into production implementation.

---

## 8. State Model

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

```yaml
phase: build
status: waiting
reason: user-approval-required
owner: requestor
resume_when: approval-recorded
```

`closed` is the terminal phase defined in Section 7; it is never a status value. When a change is in the `closed` phase, its terminal outcome is recorded in `status` as `done`, `failed`, `cancelled`, or `superseded`.

### 8.2 Legal Phase/Status Combinations

The statuses `draft`, `ready`, `active`, and `waiting` are legal at any non-closed phase. The status `done` is legal at any phase as that phase's local completion signal, gating advancement on the next phase's Definition of Ready. It represents the change's successful terminal outcome only when it occurs with the `closed` phase.

The statuses `failed`, `cancelled`, and `superseded` are legal only with the `closed` phase. An action producing any of these outcomes MUST finalize the change into the `closed` phase in the same state mutation.

### 8.3 Transition Table

| Action | Legal From (Phase/Status) | Precondition | Gate Order | Resulting Phase/Status | Rejection Behavior |
|---|---|---|---|---|---|
| `start` | A non-closed phase with status `ready` | Starting the phase is authorized. | DoF → DoW → current-phase DoD → next-phase DoR | Same phase with status `active`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |
| `complete` | A non-closed phase with status `draft` or `active` | From `draft`, the current phase's DoR is satisfied; from `active`, the current phase's DoD is satisfied. | From `draft`: DoF → DoW → current-phase DoR. From `active`: DoF → DoW → current-phase DoD → next-phase DoR. | From `draft`, the same phase with status `ready`; from `active`, the current phase with status `done`, after which satisfied next-phase DoR may produce the next phase with status `ready`. Completion of the final phase produces `closed`/`done`. | Reject without any partial mutation of persisted state when the applicable precondition or gate is not satisfied. |
| `wait` | Any non-closed phase/status | A DoW condition is active. | DoF → DoW → current-phase DoD → next-phase DoR | Same phase with status `waiting`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |
| `resume` | A non-closed phase with status `waiting` | The recorded resume condition is satisfied. | DoF → DoW → current-phase DoD → next-phase DoR | Recorded resume phase, or an explicitly required earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |
| `fail` | Any non-closed phase/status | A DoF condition is active. | DoF → DoW → current-phase DoD → next-phase DoR | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |
| `cancel` | Any non-closed phase/status | An authorized cancellation decision exists. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `cancelled`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `reopen` | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF → DoW → current-phase DoD → next-phase DoR | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |

### 8.4 Cancellation, Supersession, Reopening, and Terminal Behavior

`cancel` moves any non-closed phase/status to the `closed` phase with status `cancelled` when an authorized cancellation decision exists. `supersede` moves any non-closed phase/status to the `closed` phase with status `superseded` when a later change replaces this change's goal.

For `cancel` and `supersede`, an active DoW condition does not prevent the authorized terminal
action. DoW and the current- and next-phase readiness and completion gates are not applicable to
these actions. DoF retains first priority; when DoF determines that the change has failed, the
resulting terminal status is `failed` rather than `cancelled` or `superseded`.

`reopen` moves a change from the `closed` phase back to the resume phase recorded at closure, or to an explicitly stated earlier phase, for corrective follow-up work. The action MUST record its reason and the new goal-bound scope in history.

Once a change is in the `closed` phase, no further phase advancement is legal except through `reopen`.

### 8.5 Evaluation Priority

The following order MUST be applied during every gate evaluation:

1. DoF
2. DoW
3. DoR for the current phase
4. DoD for the current phase
5. DoR for the next phase

A satisfied DoD does not override a satisfied DoF or DoW.

This order defines evaluation precedence. A gate that is not applicable to the requested action or current state is skipped and, when gate evidence is recorded, MUST be recorded as `not_applicable`. Evaluation MUST stop as soon as a gate determines the requested action's outcome.

---

## 9. Definition of Ready

DoR determines whether a phase may begin.

### 9.1 Ready-to-Spec

At minimum:

- the goal or problem is described,
- the expected benefit is understandable,
- the requestor or decision owner is identified,
- known constraints are available,
- affected system areas are roughly known,
- no obvious conflict with the constitution exists.

### 9.2 Ready-to-Plan

At minimum:

- goal, scope, and non-goals are defined,
- requirements and acceptance conditions are understandable,
- relevant architecture and ADR constraints have been reviewed,
- open questions have been answered or explicitly accepted,
- no unresolved contradictions exist.

### 9.3 Ready-to-Build

At minimum:

- the specification is approved,
- the technical approach is sufficiently clear,
- critical risks have been assessed,
- required dependencies are available,
- test and verification criteria are defined,
- no blocking decision is pending.

### 9.4 Ready-to-Verify

At minimum:

- the planned implementation is complete or testable,
- relevant tests exist,
- build and analysis tools are available,
- known deviations are documented.

### 9.5 Ready-to-Release

At minimum:

- build and required tests have succeeded,
- security and quality gates are satisfied,
- migration and rollback are clarified,
- known limitations are documented,
- required approvals are available.

---

## 10. Definition of Done

DoD determines whether a phase has been completed successfully.

### 10.1 Spec-Done

At minimum:

- goal, benefit, and success signals are described,
- scope and non-goals are defined,
- requirements are unambiguous and verifiable,
- each behavioral requirement has at least one concrete acceptance example, or a justified alternative verifiable acceptance condition exists,
- constraints are documented,
- open questions are closed or explicitly accepted,
- ADR conflicts are resolved or returned to the requestor,
- the specification is approved.

### 10.2 Plan-Done

At minimum:

- the technical approach is described,
- affected components are identified,
- architecture, data, API, and operational impacts are assessed,
- the test strategy is defined,
- migration and rollback needs are clarified,
- risks and decisions are documented,
- implementation is decomposed appropriately.

### 10.3 Build-Done

At minimum:

- all approved changes are implemented,
- no unintended scope has been introduced,
- tests have been added or updated,
- local quality gates have succeeded,
- required documentation is updated,
- deviations from the specification are explained and approved.

### 10.4 Verify-Done

At minimum:

- all acceptance conditions have been verified,
- required automated tests have succeeded,
- relevant negative and failure cases have been checked,
- regression tests have succeeded,
- evidence is complete,
- remaining limitations are documented.

### 10.5 Release-Done

At minimum:

- deployment or publication has succeeded,
- smoke tests have succeeded,
- version and release notes are documented,
- monitoring shows no critical problems,
- rollback is possible or explicitly not required,
- roadmap and status are updated.

---

## 11. Definition of Wait

DoW describes conditions under which the flow MUST pause in a controlled manner without being considered failed.

### 11.1 Typical Wait Categories

- `WAIT_USER_INPUT`
- `WAIT_DECISION`
- `WAIT_DEPENDENCY`
- `WAIT_PROCESS`
- `WAIT_APPROVAL`
- `WAIT_EXTERNAL_SYSTEM`

### 11.2 Mandatory Content of a Wait State

Every wait state MUST include:

- reason,
- outstanding information or decision,
- responsible person or source,
- resume condition,
- safe current state,
- next action after resumption.

Template:

```yaml
status: waiting
reason: architecture-decision-required
waiting_for: requestor
resume_when: ADR-approved
safe_state: no-uncommitted-destructive-change
resume_at: planning
next_action: update-plan
```

### 11.3 AI Agent Behavior in a Wait State

An AI agent MUST:

- stop all risky or scope-changing actions,
- preserve the current state,
- state the missing decision precisely,
- formulate one minimal, decidable question,
- never interpret an assumption as approval,
- resume at the defined point once the resume condition is satisfied.

---

## 12. Definition of Fail

DoF describes conditions under which the flow MUST terminate unsuccessfully.

### 12.1 Typical Fail Categories

- critical technical error,
- data loss or repository corruption,
- critical security breach,
- unauthorized breaking change,
- violation of the constitution or an ADR,
- action outside the approved scope,
- exceeding hard budget, cost, or retry limits,
- unrecoverable build or migration state,
- permanently unsatisfiable acceptance conditions.

### 12.2 Mandatory Content of a Fail Rule

Every fail rule MUST include:

- trigger,
- required response,
- permitted preservation actions,
- final status,
- required documentation.

Template:

```markdown
### F-01 — Unauthorized Breaking Change

**Trigger**  
A breaking change is required but has not been approved.

**Required response**

- Stop implementation.
- Revert or isolate unapproved changes.
- Preserve existing evidence.
- Document the conflict in the specification.
- Mark the flow as failed.

**Final status**  
`FAILED_POLICY_VIOLATION`
```

---

## 13. Conflict and Decision Rules

### 13.1 ADR Conflicts

Existing accepted ADRs take precedence.

When a requirement conflicts with an ADR, the agent MUST:

1. document the conflict in the requirement or specification,
2. stop planning or implementation,
3. return the requirement to the requestor,
4. request a decision,
5. communicate and reference the decision.

An existing ADR MUST only be changed or replaced through an explicitly approved change flow.

### 13.2 Specification Drift

When implementation or tests deviate from the specification, one of the following actions MUST occur:

- adjust the implementation,
- change and reapprove the specification before continuing,
- document the deviation as an accepted exception,
- stop the flow if the deviation is not permitted.

### 13.3 Breaking Changes

Breaking changes MUST be explicitly marked, assessed, and approved. Without approval, the corresponding DoF rule applies.

---

## 14. Pair Review Model

### 14.1 Activation

Pair Review MAY be enabled or required by:

- the active compliance profile,
- project scope and organizational policy,
- change class,
- risk or criticality,
- affected artifact type,
- local strengthening in the change specification.

Lean and low-risk Class S flows MAY omit Pair Review. Governed or regulated profiles SHOULD require it for relevant high-impact changes.

### 14.2 Participants and Identity

A participant may be a human, AI agent, coding agent, review agent, or external review service. Requestor and Reviewer MUST have distinct participant identities for the same review cycle.

Examples (illustrative, non-normative):

- Requestor: Human; Reviewer: Human
- Requestor: Human; Reviewer: AI Agent (any vendor or product)
- Requestor: AI Agent; Reviewer: AI Agent from a distinct vendor or product
- Requestor: AI Agent (any vendor or product); Reviewer: Human
- Requestor: AI Agent (any vendor or product); Reviewer: External Review Service

Separate sessions of the same participant identity do not satisfy the independence rule unless the project explicitly defines and justifies them as independently controlled participants.

### 14.3 Review Cycle

A Pair Review cycle MUST:

1. identify the Requestor and Reviewer,
2. define the review scope and criteria,
3. preserve a stable reviewable work product,
4. record findings with severity and status,
5. return findings to the Requestor,
6. record the Requestor's disposition and changes,
7. verify resolved blocking findings when required,
8. preserve the final review result as evidence.

### 14.4 Findings

A finding SHOULD include:

- stable finding ID,
- review-cycle ID,
- Requestor and Reviewer identities,
- category,
- severity,
- affected artifact and reference,
- summary and details,
- required or recommended action,
- status and disposition rationale.

Recommended severities are `informational`, `minor`, `major`, `blocking`, and `critical`.

Recommended statuses are `open`, `accepted`, `rejected`, `resolved`, `verified`, and `withdrawn`.

Unresolved blocking findings MUST block the applicable completion or transition gate unless they are formally dispositioned by an authorized decision owner.

### 14.5 Review Artifacts

Pair Review evidence MAY be recorded inline in `evidence.md`. A separate `review.md` is conditional and SHOULD be required only when review complexity, retention, auditability, or compliance justifies it.

Review findings are not requirements and do not override higher-ranking artifacts. A finding that requires a requirement or architecture change MUST trigger the appropriate specification or ADR workflow.

Regardless of whether it is stored inline in `evidence.md` or separately in `review.md`, a portable Pair Review evidence record MUST capture exactly these eight fields: participant; role (`Requestor` or `Reviewer`); reviewed revision (the exact artifact revision reviewed); action (the review action taken); timestamp; result; findings (a reference to or summary of the findings); and disposition. This evidence-record field set is distinct from, and complements, the per-finding fields in Section 14.4.

## 15. Evidence Model

Evidence MUST demonstrate traceably whether requirements, gates, and quality criteria have been satisfied.

Permitted evidence includes:

- test results,
- build output,
- static analysis,
- security scans,
- review approvals,
- logs,
- screenshots,
- measurements,
- deployment or release records,
- references to commits and pull requests.

Minimal evidence template:

```markdown
# Verification Evidence

## Requirement Coverage

| Requirement | Evidence | Result |
|---|---|---|
| R1 | `tests/...` | Pass |
| R2 | `tests/...` | Pass |

## Quality Gates

- Build: Pass
- Unit tests: Pass
- Integration tests: Pass
- Static analysis: Pass
- Security checks: Pass

## Deviations

None.

## Final Status

Done.
```

For small changes, evidence MAY be documented directly in `spec.md`.

---

## 16. Minimum Templates

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

## Requirements

### R1 — <Title>

<verifiable requirement>

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
- Requestor:
- Reviewer:
- Result:

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

## Final Status

<status>
```

### 16.5 `project-brief.md`

```markdown
# Project Brief

## Problem and Opportunity

<problem, need, or opportunity>

## Target Users and Stakeholders

- <user or stakeholder>

## Desired Outcomes and Success Signals

- <verifiable outcome>

## Project Type and Lifecycle Context

- Greenfield | Brownfield | Migration | Modernization | Re-engineering

## Scope and Non-Goals

### Included

- <included>

### Excluded

- <excluded>

## Constraints

- Time:
- Budget:
- Technology:
- Delivery:

## Compliance Profile

`lean | standard | governed | regulated | <custom>`

## Operating Mode

`stand-alone | combination`

## Integrated Methods and Tools

- <method, framework, tool, agent, or None>
```

### 16.6 `architecture.md`

```markdown
# Architecture

## System Context

<system and external actors>

## Components

| Component | Responsibility | Dependencies |
|---|---|---|

## Boundaries and Constraints

- <boundary or constraint>

## Data Flows

- <important data flow>

## Deployment and Operations

- <operating model>

## Known Limitations

- <limitation>

## Related ADRs

- <ADR reference>
```

### 16.7 `roadmap.md`

```markdown
# Roadmap

## Now

- <active goal>

## Next

- <next goal>

## Later

- <later goal>

## Open

- <unresolved direction or option>
```

---


## 17. Combination Contracts

Each external integration MUST define a mapping contract containing:

- integration name and version,
- purpose and owned capabilities,
- mapped GG-SAD phases and artifacts,
- authoritative source for each mapped fact,
- allowed read and write scopes,
- gate and approval interaction,
- state synchronization rules,
- failure, rollback, and uninstall behavior.

GG-SAD MAY be combined with methods such as GSD, OpenSpec, Spec Kit, or BMAD and with tools such as Hermes or Kiro. These names are examples, not normative dependencies.

## 18. GG-SAD Memory Model

GG-SAD MAY provide a project memory. Until a reference implementation exists, memory is an optional capability and MUST NOT replace governing documents.

The memory MUST support at least these record types:

- **Decision** — scoped product, process, implementation, or operational decisions that are not architecture decisions;
- **Learning** — reusable knowledge derived from delivery or operation;
- **Failure** — failed approaches, incidents, causes, mitigations, and prevention guidance;
- **Definition** — glossary terms, domain language, abbreviations, and canonical meanings;
- **External Source** — referenced external information with provenance, retrieval date, relevance, and trust metadata.

Architecture decisions MUST remain ADRs. A memory decision MUST NOT be used to avoid the ADR process.

Memory records MUST include stable IDs, scope, provenance, status, timestamps, and links to related artifacts. Retrieval MUST respect project permissions and the active compliance profile.

## 19. Agent Execution Algorithm

An AI agent MUST use the following process for every active phase:

```text
1. Load the project brief, project-wide rules, relevant ADRs, architecture, active compliance profile, integration mappings, and applicable memory records.
2. Determine the current phase, status, goal, and scope.
3. Evaluate DoF.
4. Evaluate DoW.
5. Evaluate DoD for the current phase.
6. If DoD is satisfied, preserve the evidence.
7. Evaluate DoR for the next phase.
8. Start the next phase only if its DoR is satisfied.
9. Perform changes exclusively within the approved scope.
10. After every relevant change, verify specification, architecture, and policy compliance.
11. On conflict, uncertainty, or missing approval, enter a controlled wait state.
12. Before completion, perform a final drift and evidence check.
```

### 19.1 Agent Prohibitions

An AI agent MUST NOT:

- invent goals, requirements, or approvals,
- interpret missing information as consent,
- silently modify higher-ranking documents,
- implement breaking changes without approval,
- bypass wait states through speculation,
- mark a flow as done when evidence is missing,
- conceal errors or reinterpret them as successful deviations,
- work beyond the approved scope.

---

## 20. Completion Criteria for a Change

A change transitions into the `closed` phase with the terminal status `done`, representing successful completion, only when all of the following conditions are satisfied. The `closed` phase MAY also be reached with a different terminal status under the rules in Section 8; those outcomes are not gated by this list.

- no DoF condition is active,
- no DoW condition is active,
- all required DoD criteria are satisfied,
- requirement and acceptance-example coverage is evidenced,
- required Pair Review cycles are complete and blocking findings are resolved or formally dispositioned,
- specification, implementation, tests, and documentation are consistent,
- relevant roadmap, architecture, or ADR references have been updated,
- the final status is documented traceably.

---

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

Leading source of truth:

```text
Constitution
→ ADRs
→ Project Brief
→ Architecture
→ Scoped Decisions
→ Change Spec
→ Plan
→ Tasks
→ Code and Tests
→ Evidence
```

GG-SAD does not optimize for maximum documentation volume. It optimizes for **clear goals, controlled transitions, and verifiable outcomes**.

## 22. Minimal Automation Contract

### 22.1 Contract Operations

A GG-SAD automation contract MUST support these technology-neutral operations:

- initialize a stand-alone GG-SAD project;
- create a goal-bound change;
- validate governing configuration, artifacts, references, and state;
- evaluate and execute one controlled state transition under the Section 8 Transition Table.

The contract specifies observable behavior and compatibility requirements only. It does not prescribe a programming language, module structure, or vendor-specific agent interface.

### 22.2 Minimal Result Envelope

Every contract operation MUST return a result envelope containing three fields present in every response regardless of outcome: `operation`, identifying which contract operation ran; `result`, whose value is one of `success`, `rejected`, or `error` and is never partial; and `changed`, indicating whether persistent state changed.

The `state` field contains the resulting phase and status and is included when applicable to the operation; it is omitted when the operation produces no phase/status result. As defined in Section 8, the phase may be `closed`, while the status carries the terminal outcome. The `issues` field contains stable codes plus human-readable messages and is included whenever `result` is `rejected` or `error` and omitted whenever `result` is `success`. The `data` field is always optional operation-specific output and is present only when relevant to the operation.

A goal summary, specification anchor, gate outcome, evidence references, and timestamp are not universally required envelope fields. They MAY appear inside `data` when relevant to a specific operation.

### 22.3 Rejection and Output Requirements

An invalid operation MUST be rejected without any partial mutation of persisted state. Its `result` MUST be `rejected` or `error`, and `changed` MUST be `false`.

For every operation, an implementation MUST emit both an actionable human-readable message and the structured result envelope. It MUST record transition history and relevant evidence under the Section 8 Transition Table and Section 15 Evidence Model.
