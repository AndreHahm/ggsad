# GG-SAD — Normative Method Specification

**Version:** 1.3
**Status:** Normative Baseline  
**Revision:** 2026-08-21 — Clarified transition, phase-gate, release-approval, Pair Review evidence, and implementation-alignment contracts.
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
| 23. The `core` Profile | Method Semantics |

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
- evidence appropriate to the selected compliance profile,
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

GG-SAD defines the following default compliance profiles:

| Compliance Profile | Intended Use | Minimum Characteristics |
|---|---|---|
| `lean` | Pre-PMF MVPs, prototypes, solo development, fast iteration | Minimal artifacts, automated checks where available, self-approval permitted unless a critical rule applies |
| `standard` | Typical product and team development | Separate specification for normal changes, defined quality gates, recorded evidence, peer review where practical |
| `governed` | Enterprise or high-impact delivery | Strong traceability, explicit approvals, security and architecture review, controlled release evidence |
| `regulated` | Regulated, safety-critical, or externally audited work | Segregation of duties, immutable or retained evidence, formal approvals, compliance mappings, audit-ready history |

Projects MAY define additional compliance profiles. Custom compliance profiles MUST inherit from a default compliance profile or explicitly document every invariant and deviation.

### 5.2 Tailoring Dimensions

A compliance profile MAY tailor:

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

A compliance profile of lower compliance MAY reduce optional controls. It MUST NOT disable the invariant core defined in Section 3.7.

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

### 5.6 Method Profiles

GG-SAD defines two **method profiles**, `core` and `full`. A method profile fixes the model by which a change is carried out: its documents, states, gates, and actions.

Method profiles are a second axis beside the compliance profiles of Section 5.1. They do not replace, rename, or alter the compliance profiles, and a compliance profile does not select a method profile.

- `core` is the simplified model with four states, three outcomes, and one set of gate lists per change. It is specified in Section 23.
- `full` is the model with phases, Definition of Ready and Definition of Done pairs, size classes, and the document hierarchy. It is specified by Sections 4 to 22 together with the protections of Section 24.

Every change has exactly one method profile and exactly one compliance profile. Both are resolved in the order defined in Section 5.3.

A change MUST record its method profile when the change is created. Project configuration MAY name a default method profile, which applies to every change that selects none. A project that names a default SHOULD record it in the project brief (Section 16.5). A request to create a change that selects no method profile, in a project whose configuration names no default, MUST be rejected, and no change is created. See AE-01, AE-02, AE-03.

The identifiers `core` and `full` are exact lowercase strings. Any other value, including a different letter case or surrounding whitespace, is not a method profile and MUST be rejected. See AE-04.

The method profile of a change is fixed for the life of the change. An operation MUST NOT alter the method profile of an existing change, and the recorded value MUST NOT be edited. See AE-05.

To move work from one method profile to the other, a new change MUST be created in the other method profile, and the existing change MUST be superseded by the new change with the `supersede` action. No in-place switch is defined, and the states of `core` are not mapped onto the phases and statuses of `full`. A change that is already closed MUST NOT be superseded. See AE-06, AE-07.

The method profile `full` is specified but not implemented: the reference implementation does not implement `full` and MUST reject the creation of a change that selects it. This marking describes the implementation only; it does not suspend or weaken any rule of `full`. See AE-08.

The following table states which of Sections 1 to 22 apply to which method profile. A section that the table does not name as `full` only applies to both method profiles. A `core` change MUST NOT be required to satisfy a rule of a section that applies to `full` only. Sections 23 to 25 state their own applicability. See AE-39, AE-50, AE-59.

| Sections | Applies To |
|---|---|
| 4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 11.1, 16.1 to 16.4, and the diagram of Section 21 | `full` only |
| 11.2 and 12.2 | Both method profiles, except that the safe current state and the next action of a wait state in 11.2 and the final status code of a fail rule in 12.2 apply to `full` only. Sections 23.5 and 23.2 give the `core` equivalents. |
| Every other section of Sections 1 to 22 | Both method profiles |

**AE-01 — Select the `core` method profile at creation**

- Covers: Section 5.6

Given a project whose configuration names no default method profile  
When a change is created that selects the method profile `core`  
Then the change is created with the recorded method profile `core`, and Section 23 governs it

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

**AE-04 — Reject a method profile identifier that is not exact**

- Covers: Section 5.6

Given a project whose configuration names no default method profile  
When a change is created that selects the method profile `Core`  
Then the creation is rejected, because only the exact lowercase identifiers `core` and `full` are method profiles, and no change is created

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

**AE-08 — Reject a change that selects the unimplemented method profile**

- Covers: Section 5.6

Given the reference implementation  
When a change is created that selects the method profile `full`  
Then the creation is rejected, and no change is created

## 6. Size Classes

This section specifies the `full` method profile (Section 5.6).

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
| `start` | A non-closed phase with status `ready` | Starting the phase is authorized. | DoF → DoW; current-phase DoR was established by `ready`, and current-phase DoD and next-phase DoR are not applicable. | Same phase with status `active`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |
| `complete` | A non-closed phase with status `draft`, `active`, or `done` | From `draft`, the current phase's DoR is satisfied; from `active`, the current phase's DoD is satisfied; from `done`, the next phase's DoR is re-evaluated. | From `draft`: DoF → DoW → current-phase DoR. From `active`: DoF → DoW → current-phase DoD → next-phase DoR. From `done`: DoF → DoW → next-phase DoR; current-phase DoR and DoD are already established. | From `draft`, the same phase with status `ready`. From `active`, satisfied current-phase DoD first produces the current phase with status `done`; satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. From `done`, satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. Completion of the final phase produces `closed`/`done`. | Reject without any partial mutation of persisted state when the applicable precondition, DoF, DoW, current-phase DoR, or current-phase DoD is not satisfied. Unsatisfied next-phase DoR is not a rejection after current-phase DoD succeeds or during re-evaluation from `done`; it preserves the current phase with status `done`. |
| `wait` | Any non-closed phase/status | A DoW condition is active. | DoF → DoW; current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | Same phase with status `waiting`. | Reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure. |
| `resume` | A non-closed phase with status `waiting` | The recorded resume condition is satisfied and the recorded or explicitly required resume phase is non-closed. | DoF → DoW → DoR for the recorded non-closed resume phase or explicitly required earlier non-closed phase; current-phase DoD and next-phase DoR are not applicable. | Recorded non-closed resume phase, or an explicitly required earlier non-closed phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied; remain `waiting` when a DoW condition is still active; fail when DoF determines failure. |
| `fail` | Any non-closed phase/status | A DoF condition is active. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `cancel` | Any non-closed phase/status | An authorized cancellation decision exists. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `cancelled`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `reopen` | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF for the new corrective scope → DoW for the new corrective scope → DoR for the recorded resume phase or explicitly stated earlier phase; the prior terminal outcome's DoF and DoW, closed-phase DoD, and next-phase DoR are not applicable. | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied; wait when the new corrective scope's DoW determines a pause; fail when the new corrective scope's DoF determines failure. |

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

This section specifies the `full` method profile (Section 5.6).

DoR determines whether a phase may begin.

### 9.1 Ready-to-Intake

At minimum:

- a request, problem, opportunity, or goal has been captured,
- the requestor or intake owner is identifiable,
- enough context exists to classify or route the work,
- no active DoF condition requires immediate failure handling.

### 9.2 Ready-to-Explore

At minimum:

- the question, opportunity, or uncertainty to explore is described,
- the expected decision or learning outcome is identified,
- exploration boundaries and relevant constraints are known,
- an owner for the exploration is identified.

### 9.3 Ready-to-Decide

At minimum:

- the decision to be made is stated,
- relevant exploration evidence and viable options are available,
- material tradeoffs, risks, and constraints are visible,
- the authorized decision owner is identified.

### 9.4 Ready-to-Spec

At minimum:

- the goal or problem is described,
- the expected benefit is understandable,
- the requestor or decision owner is identified,
- known constraints are available,
- affected system areas are roughly known,
- no obvious conflict with the constitution exists.

### 9.5 Ready-to-Plan

At minimum:

- goal, scope, and non-goals are defined,
- requirements and acceptance conditions are understandable,
- relevant architecture and ADR constraints have been reviewed,
- open questions have been answered or explicitly accepted,
- no unresolved contradictions exist.

### 9.6 Ready-to-Build

At minimum:

- the specification is approved,
- the technical approach is sufficiently clear,
- critical risks have been assessed,
- required dependencies are available,
- test and verification criteria are defined,
- no blocking decision is pending.

### 9.7 Ready-to-Verify

At minimum:

- the planned implementation is complete or testable,
- relevant tests exist,
- build and analysis tools are available,
- known deviations are documented.

### 9.8 Ready-to-Release

At minimum:

- build and required tests have succeeded,
- security and quality gates are satisfied,
- migration and rollback are clarified,
- known limitations are documented,
- required approvals are available.

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

### 10.2 Explore-Done

At minimum:

- the stated question or uncertainty has been investigated within the approved boundaries,
- relevant observations, evidence, and limitations are recorded,
- viable options or a justified conclusion are available for decision,
- no production implementation has begun merely because exploration completed.

### 10.3 Decide-Done

At minimum:

- the authorized decision owner has recorded the selected option or disposition,
- the decision rationale and material tradeoffs are documented,
- consequences, constraints, and required follow-up are identified,
- any resulting specification work has an explicit goal-bound handoff.

### 10.4 Spec-Done

At minimum:

- goal, benefit, and success signals are described,
- scope and non-goals are defined,
- requirements are unambiguous and verifiable,
- each behavioral requirement has at least one concrete acceptance example, or a justified alternative verifiable acceptance condition exists,
- constraints are documented,
- open questions are closed or explicitly accepted,
- ADR conflicts are resolved or returned to the requestor,
- the specification is approved.

### 10.5 Plan-Done

At minimum:

- the technical approach is described,
- affected components are identified,
- architecture, data, API, and operational impacts are assessed,
- the test strategy is defined,
- migration and rollback needs are clarified,
- risks and decisions are documented,
- implementation is decomposed appropriately.

### 10.6 Build-Done

At minimum:

- all approved changes are implemented,
- no unintended scope has been introduced,
- tests have been added or updated,
- local quality gates have succeeded,
- required documentation is updated,
- deviations from the specification are explained and approved.

### 10.7 Verify-Done

At minimum:

- all acceptance conditions have been verified,
- required automated tests have succeeded,
- relevant negative and failure cases have been checked,
- regression tests have succeeded,
- evidence is complete,
- remaining limitations are documented.

### 10.8 Release-Done

At minimum:

- deployment or publication has succeeded,
- smoke tests have succeeded,
- version and release notes are documented,
- monitoring shows no critical problems,
- rollback is possible or explicitly not required,
- required release approval has been recorded by an authorized human decision owner,
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

Lean and low-risk Class S flows MAY omit Pair Review. Governed or regulated compliance profiles SHOULD require it for relevant high-impact changes.

### 14.2 Participants and Identity

A participant may be a human, AI agent, coding agent, review agent, or external review service. Requestor and Reviewer MUST have distinct participant identities for the same review cycle.

Examples (illustrative, non-normative):

- Requestor: Human; Reviewer: Human
- Requestor: Human; Reviewer: AI Agent (any vendor or product, for example Codex or Devin)
- Requestor: AI Agent (for example Claude Code); Reviewer: AI Agent from a distinct vendor or product (for example Codex or Devin)
- Requestor: AI Agent (any vendor or product, for example Claude Code); Reviewer: Human
- Requestor: AI Agent (any vendor or product, for example Claude Code); Reviewer: External Review Service

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

## Method Profile

`core | full`

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

The diagram above shows the `full` flow (Section 5.6). The flow of `core` is given by the transition table of Section 23.4.

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

---

## 23. The `core` Profile

This section specifies the `core` method profile (Section 5.6). The protections of Section 24 and the state definitions of Section 25 apply to a `core` change as those sections state. Sections 1 to 22 apply to a `core` change as Section 5.6 states.

### 23.1 Change Definition and Documents

A `core` change consists of three documents in its change directory (Section 4.3):

```text
specs/<change-id>/
├── change.yaml
├── spec.md
└── state.json
```

- `change.yaml` is the change definition, a human-owned YAML document.
- `spec.md` is the specification of the change. A human writes it, and the `approve` action approves it (Section 23.4). Section 3.9 applies to its requirements.
- `state.json` is the state document. The implementation owns it, and Section 25.1 defines it.

The change definition MUST contain these fields:

- `id`: the identifier of the change, unique among the changes of the project;
- `method_profile`: the method profile of the change, which is `core` (Section 5.6);
- `compliance_profile`: the compliance profile of the change (Section 5.1);
- `author` and `owner`: the participant that wrote the change and the participant responsible for it;
- `goal`: with `problem`, `done_when`, and `non_goals`, as Section 3.1 requires;
- `scope`: with `allow`, the list of path patterns the change MAY touch (Section 24.5);
- `requirements`: the requirements of the change, each with text, examples, and evidence commands (Section 24.9);
- `gates`: with the three lists `fail`, `wait`, and `done` (Section 23.3).

The change definition MAY contain `follows`, the identifier of one earlier change that this change continues. The change named in `follows` MUST exist and MUST be in the state `closed`. The field is a reference only: it never changes the state or the outcome of the named change. See AE-09, AE-11, AE-12.

A `core` change has no size class (Section 6), no phase (Section 7), no Definition of Ready or Definition of Done per phase (Sections 9 and 10), and no ranking of change documents (Section 4.1). The invariant core of Section 3.7 applies to it: the goal is `goal`, the specification anchor is `spec.md`, gate evaluation is Section 23.6, evidence is the requirement evidence of Section 24.9, controlled wait and fail behavior are Sections 23.5 and 24.7, and the traceable final status is the outcome of Section 23.2. See AE-59.

A human MUST NOT edit the state document by hand. An implementation MUST detect a state document that does not match the recorded history of the change and MUST NOT act on it (Section 24.4). See AE-10.

**AE-09 — Accept a complete change definition**

- Covers: Section 23.1

Given a change definition with the fields `id`, `method_profile` set to `core`, `compliance_profile`, `author`, `owner`, `goal`, `scope`, `requirements`, and `gates`  
When the `new` action receives it  
Then the change exists with the documents `change.yaml`, `spec.md`, and `state.json`

**AE-10 — Refuse a state document edited by hand**

- Covers: Section 23.1

Given a `core` change whose `state.json` was edited by hand after the last recorded action  
When any action that changes state is requested  
Then the implementation detects that the state document does not match the recorded history and refuses to act

**AE-11 — Follow a closed change**

- Covers: Section 23.1

Given a `core` change A that is closed with the outcome `failed`  
When a new change B is created with `follows` naming change A  
Then change B is created, and change A keeps its state `closed` and its outcome `failed`

**AE-12 — Reject following a change that has not ended**

- Covers: Section 23.1

Given a `core` change A in the state `active`  
When a new change B is created with `follows` naming change A  
Then the creation is rejected, because change A is not closed, and no change B exists

**AE-59 — A `core` change has no size class**

- Covers: Section 23.1

Given a `core` change whose scope would be a Class L initiative under Section 6  
When the change is created  
Then Section 6 does not apply, the change is one `core` change, and no decomposition into several changes is required

### 23.2 States and Outcomes

A `core` change is always in exactly one of four states:

- `open`: the change exists and has not started;
- `active`: the change has started and work is in progress;
- `waiting`: the change is paused by a wait record (Section 23.5);
- `closed`: the change has ended.

A `closed` change has exactly one of three outcomes:

- `done`: the change was completed successfully by the `close` action;
- `failed`: the change ended unsuccessfully, because a hard fail condition was active or because a human disposed of a soft fail condition with the `fail` action (Section 24.7);
- `cancelled`: the change was ended by the `cancel` or `supersede` action.

The state document records the state in the field `state` and the outcome in the field `outcome` (Section 25.1). An outcome exists only when the state is `closed`; in every other state the outcome is `null`. An outcome of `failed` MUST carry a reason text. The final status codes of Section 12.2 apply to `full` only. See AE-14, AE-39, AE-41.

When a change is created, its record MUST show the state `open`, the outcome `null`, no approval, no question, no wait record, and no base revision. See AE-13.

A `closed` change is final: no action changes its state or its outcome. Follow-up work is a new change that names the closed change in `follows` (Section 23.1). See AE-15.

**AE-13 — Initial record of a new change**

- Covers: Section 23.2

Given a valid change definition  
When the change is created  
Then the record shows the state `open`, the outcome `null`, no approval, no question, no wait record, and no base revision

**AE-14 — The outcome exists only when closed**

- Covers: Section 23.2

Given an `active` change whose outcome is `null`  
When the `close` action succeeds  
Then the state is `closed` and the outcome is `done`, and no change in any other state has an outcome

**AE-15 — A closed change is final**

- Covers: Section 23.2

Given a `core` change that is `closed` with the outcome `cancelled`  
When the `start` action is requested for it  
Then the request is rejected, and the state and the outcome do not change

### 23.3 Gates

The field `gates` of a `core` change holds three lists:

- `fail`: fail gates, each stating a condition under which the change has failed;
- `wait`: wait gates, each stating a condition under which the change pauses: while the condition is active, the change does not start, resume, or close;
- `done`: done gates, each stating a condition that MUST be satisfied before the change closes with the outcome `done`.

There is no ready gate. Readiness to start is a precondition of the `start` action (Section 23.4).

Every gate has an `id` that is unique within the change, including the base gates of Section 23.7. A fail gate and a wait gate are predicate gates: each evaluates a condition to one of the three results of Section 24.2. A fail gate has a `severity`, which is `hard` or `soft` (Section 24.7), and a fail gate without a severity is invalid. A done gate has exactly one kind: `check`, a command evaluated as Section 24.2 defines; `review`, satisfied by a recorded review result from a participant other than the participant that requested the reviewed work (Section 3.10); or `sign-off`, satisfied by an approval of that gate recorded by a human (Section 24.3). A change definition with a duplicate gate identifier, a gate without a kind, a gate with more than one kind, or a fail gate without a severity MUST be rejected. See AE-16, AE-17, AE-18.

**AE-16 — Reject a duplicate gate identifier**

- Covers: Section 23.3

Given a change definition with two gates that both have the `id` `tests-pass`  
When the `new` action receives it  
Then the definition is rejected, and no change is created

**AE-17 — Reject a fail gate without a severity**

- Covers: Section 23.3

Given a change definition whose fail gate `no-secrets` has no `severity`  
When the `new` action receives it  
Then the definition is rejected, because a fail gate without a severity is invalid

**AE-18 — Reject a done gate with two kinds**

- Covers: Section 23.3

Given a change definition whose done gate `release-ok` is both a `check` and a `sign-off`  
When the `new` action receives it  
Then the definition is rejected, because a done gate has exactly one kind

### 23.4 Actions and Transition Table

A `core` change changes state only through the actions of the table below. An action requested from a state that the table does not list under Legal From MUST be rejected (Section 22.3). If a precondition of a row is not met, the transition of that row does not occur.

| Action | Legal From | Precondition | Resulting State |
|---|---|---|---|
| `new` | No change with the given identifier exists | The change definition is valid under Sections 23.1 and 23.3, its method profile is selected under Section 5.6, its identifier is unique, and `follows`, when present, names a closed change. | The state `open` with the outcome `null` and the initial record of Section 23.2. See AE-19, AE-20. |
| `approve` | Any state except `closed` | The approval has one target. For `spec`, no question is unanswered (Section 24.8). For `gates`, the gate definitions are valid under Section 23.3. For `all`, both conditions hold. For `override`, a soft fail condition awaits disposition (Section 24.7), and the approval gives a reason and at least one further attempt. For a named gate, the gate is a `sign-off` done gate of the change. Section 24.1 governs the re-approval of changed gate definitions. | The state and the outcome do not change, and the approval is recorded. See AE-21, AE-22, AE-23, AE-24. |
| `start` | `open` | The gate definitions are approved and unchanged since approval (Section 24.1), the specification is approved when the compliance profile or the project configuration requires it, the revision from which the change starts can be recorded (Section 24.5), and the evaluation of Section 23.6 finds no fail gate and no wait gate active. | The state `active`, with the base revision recorded. See AE-25, AE-26. |
| `wait` | `active` | A reason, an owner, and a resume condition are given. | The state `waiting`, with a wait record of kind `manual`, or of kind `question` when the action gives a question (Section 23.5). See AE-27, AE-28, AE-29. |
| `ask` | `open`, `active` | The question has a text and an owner, which defaults to the owner of the change. A structured question has at least two distinct options. | The state does not change, and an unanswered question with the next identifier is recorded (Section 24.8). See AE-30, AE-31. |
| `answer` | Any state except `closed` | The question exists and is unanswered. The answer comes from the owner of the question. A structured question receives one of its options, and a free-text question receives a text. | The state does not change, and the question is recorded as answered. An answer does not resume a waiting change. See AE-32, AE-33, AE-34. |
| `resume` | `waiting` | The resume condition of the wait record is satisfied (Section 23.5). | The state `active`, when the evaluation of Section 23.6 finds no gate that decides otherwise. Otherwise the change remains `waiting`, or becomes `closed` with the outcome `failed`, as Section 23.6 decides. See AE-35, AE-36. |
| `close` | `active` | The evaluation of Section 23.6 finds no fail gate and no wait gate active, and every done gate is satisfied. | The state `closed` with the outcome `done`. When the evaluation finds otherwise, the change does not close: it remains `active` when a wait gate is active or a done gate is not satisfied, becomes `waiting` when Section 23.6 requires a wait, and becomes `closed` with the outcome `failed` when a hard fail condition is active. See AE-37, AE-38. |
| `fail` | `waiting`, with a wait record of kind `fail-gate` | A soft fail condition awaits disposition (Section 24.7), and a reason text is given. | The state `closed` with the outcome `failed` and the reason recorded. See AE-39, AE-40, AE-41. |
| `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active. See AE-42, AE-43. |
| `supersede` | Any state except `closed` | The preconditions of `cancel` hold, and `replaced_by` names a different change that exists. | As `cancel`, with `replaced_by` recorded in the closed change. See AE-44, AE-45. |
| `adopt` | Any state | The history of the change has no anchor (Section 24.4). | The state and the outcome do not change, and the anchor is created from the history as it is. See AE-46, AE-47. |

The actions `approve`, `fail`, `cancel`, `supersede`, and `adopt` MUST be performed by a human participant, An `answer` to a question whose owner is a human MUST also be given by a human (Section 24.3). See AE-24.

The actions `check`, `review`, and `guard` are read-only. They report on a change, they never change its state or its history, and they are legal from every state. They are not rows of the table. See AE-49.

The method profile `core` has no `reopen` action. A change in the state `closed` is final, and follow-up work is a new change that names the closed change in `follows` (Section 23.1). See AE-48.

**AE-19 — Create a change**

- Covers: Section 23.4 (`new`)

Given a valid change definition whose identifier `c-1` is not used  
When the `new` action receives it  
Then the change `c-1` exists in the state `open` with the outcome `null`

**AE-20 — Reject a duplicate change identifier**

- Covers: Section 23.4 (`new`)

Given an existing change `c-1`  
When the `new` action receives a valid change definition with the `id` `c-1`  
Then the action is rejected, and the existing change `c-1` does not change

**AE-21 — Approve the specification and the gates together**

- Covers: Section 23.4 (`approve`)

Given an `open` change with valid gate definitions and no unanswered question  
When a human approves the target `all`  
Then the approvals of the specification and of the gates are recorded, and the state remains `open`

**AE-22 — Reject the approval of a specification with an unanswered question**

- Covers: Section 23.4 (`approve`)

Given an `open` change with the unanswered question Q1  
When a human approves the target `spec`  
Then the action is rejected, no approval is recorded, and Q1 remains unanswered

**AE-23 — Reject an override when no soft fail condition awaits disposition**

- Covers: Section 23.4 (`approve`)

Given an `active` change with no soft fail condition awaiting disposition  
When a human approves the target `override` with a reason and two further attempts  
Then the action is rejected, and no override is recorded

**AE-24 — Reject the approval of a sign-off gate by an agent**

- Covers: Section 23.4 (`approve`)

Given an `active` change with the `sign-off` done gate `legal-ok`  
When an AI agent requests the approval of the gate `legal-ok`  
Then the action is rejected, because an approval MUST be performed by a human, and the gate remains unsatisfied

**AE-25 — Start a change**

- Covers: Section 23.4 (`start`)

Given an `open` change with approved and unchanged gate definitions, an approved specification, and no fail gate or wait gate active  
When the `start` action is requested  
Then the state is `active`, and the base revision is recorded

**AE-26 — Reject the start of a change whose gates are not approved**

- Covers: Section 23.4 (`start`)

Given an `open` change whose gate definitions are not approved  
When the `start` action is requested  
Then the action is rejected, and the change remains `open` with no base revision

**AE-27 — Wait for a person outside the change**

- Covers: Section 23.4 (`wait`)

Given an `active` change  
When the `wait` action gives the reason `vendor reply needed`, the owner `vendor`, and the resume condition `vendor reply recorded`  
Then the state is `waiting`, and the wait record has the kind `manual`

**AE-28 — Reject a wait from a change that has not started**

- Covers: Section 23.4 (`wait`)

Given an `open` change  
When the `wait` action gives a reason, an owner, and a resume condition  
Then the action is rejected, and the change remains `open` with no wait record

**AE-29 — Wait for the answer to a question**

- Covers: Section 23.4 (`wait`)

Given an `active` change with the unanswered question Q1  
When the `wait` action names Q1, the owner of Q1, and the resume condition `Q1 answered`  
Then the state is `waiting`, and the wait record has the kind `question` and names Q1

**AE-30 — Ask a structured question**

- Covers: Section 23.4 (`ask`)

Given an `active` change  
When the `ask` action records a question with the options `keep` and `drop`  
Then an unanswered question Q1 is recorded, and the state remains `active`

**AE-31 — Reject a structured question with one option**

- Covers: Section 23.4 (`ask`)

Given an `active` change  
When the `ask` action records a structured question with the single option `keep`  
Then the action is rejected, because a structured question has at least two distinct options, and no question is recorded

**AE-32 — Answer a structured question**

- Covers: Section 23.4 (`answer`)

Given an `active` change with the unanswered structured question Q1 whose options are `keep` and `drop` and whose owner is a human  
When that human answers Q1 with `keep`  
Then Q1 is recorded as answered with `keep`, and the state remains `active`

**AE-33 — Reject an answer that is not an option**

- Covers: Section 23.4 (`answer`)

Given the unanswered structured question Q1 whose options are `keep` and `drop`  
When Q1 is answered with `merge`  
Then the action is rejected, and Q1 remains unanswered

**AE-34 — Reject a second answer**

- Covers: Section 23.4 (`answer`)

Given the question Q1 that is already answered with `keep`  
When Q1 is answered again with `drop`  
Then the action is rejected, and Q1 keeps the answer `keep`

**AE-35 — Resume after the awaited question is answered**

- Covers: Section 23.4 (`resume`)

Given a `waiting` change with a wait record of kind `question` for Q1, and Q1 is now answered, and no gate decides otherwise  
When the `resume` action is requested  
Then the state is `active`

**AE-36 — Stay waiting while the resume condition is not satisfied**

- Covers: Section 23.4 (`resume`)

Given a `waiting` change with a wait record of kind `question` for Q1, and Q1 is unanswered  
When the `resume` action is requested  
Then the change remains `waiting`

**AE-37 — Close a completed change**

- Covers: Section 23.4 (`close`)

Given an `active` change with every done gate satisfied and no fail gate or wait gate active  
When the `close` action is requested  
Then the state is `closed` and the outcome is `done`

**AE-38 — Do not close with an unsatisfied done gate**

- Covers: Section 23.4 (`close`)

Given an `active` change with one done gate that is not satisfied  
When the `close` action is requested  
Then the change does not close, remains `active`, and has the outcome `null`

**AE-39 — Fail a change that awaits disposition of a soft fail**

- Covers: Section 23.4 (`fail`)

Given a `waiting` change with a wait record of kind `fail-gate` for a soft fail condition  
When a human performs the `fail` action with the reason `retry limit reached`  
Then the state is `closed`, the outcome is `failed`, and the reason `retry limit reached` is recorded

**AE-40 — Reject fail when no soft fail condition awaits disposition**

- Covers: Section 23.4 (`fail`)

Given an `active` change with no soft fail condition awaiting disposition  
When a human performs the `fail` action with a reason  
Then the action is rejected, and the change remains `active`

**AE-41 — Reject fail without a reason**

- Covers: Section 23.4 (`fail`)

Given a `waiting` change with a wait record of kind `fail-gate` for a soft fail condition  
When a human performs the `fail` action with no reason  
Then the action is rejected, and the change remains `waiting`

**AE-42 — Cancel a waiting change**

- Covers: Section 23.4 (`cancel`)

Given a `waiting` change  
When a human performs the `cancel` action  
Then the state is `closed` and the outcome is `cancelled`, although a wait was active

**AE-43 — Cancel with a hard fail condition active**

- Covers: Section 23.4 (`cancel`)

Given an `active` change with a hard fail condition active  
When a human performs the `cancel` action  
Then the state is `closed` and the outcome is `failed`, not `cancelled`

**AE-44 — Supersede a change**

- Covers: Section 23.4 (`supersede`)

Given an `active` change A and an existing change B  
When a human performs the `supersede` action on change A with `replaced_by` naming change B  
Then change A is `closed` with the outcome `cancelled` and `replaced_by` naming change B

**AE-45 — Reject supersede without a replacement**

- Covers: Section 23.4 (`supersede`)

Given an `active` change A  
When a human performs the `supersede` action on change A and gives no `replaced_by`  
Then the action is rejected, and change A remains `active`

**AE-46 — Adopt an unanchored history**

- Covers: Section 23.4 (`adopt`)

Given a change whose history has no anchor  
When a human performs the `adopt` action  
Then the anchor is created from the history as it is, and the state and the outcome do not change

**AE-47 — Reject adopt when an anchor exists**

- Covers: Section 23.4 (`adopt`)

Given a change whose history already has an anchor  
When a human performs the `adopt` action  
Then the action is rejected, and the existing anchor is not replaced

**AE-48 — A closed change cannot be reopened**

- Covers: Section 23.4

Given a `core` change that is `closed` with the outcome `done`  
When a `reopen` action is requested for it  
Then the request is rejected, because `core` has no `reopen` action, and follow-up work is a new change that names this change in `follows`

**AE-49 — A read-only action changes nothing**

- Covers: Section 23.4

Given a `closed` change  
When the `check` action is requested for it  
Then the action reports on the change, and the state, the outcome, and the history do not change

### 23.5 Wait Records

A `core` change has at most one wait record, and the wait record exists exactly while the state is `waiting`. A wait record contains:

- `kind`: one of `question`, `manual`, `fail-gate`, and `external`;
- `reason`: why the change waits;
- `owner`: the participant or source expected to act;
- `resume_when`: the condition under which the `resume` action is legal;
- `expires`: OPTIONAL, an instant after which the wait is overdue;
- `question`: the identifier of the awaited question, present when the kind is `question`.

The kind of a wait record depends on how it came to exist:

- `question`: the `wait` action gave a question (Section 24.8);
- `manual`: the `wait` action gave no question;
- `fail-gate`: the evaluation of Section 23.6 found a soft fail condition (Section 24.7);
- `external`: the evaluation of Section 23.6 found a gate that could not be evaluated (Section 24.2).

The resume condition is satisfied as follows. For the kind `question`, the awaited question is answered. For the kind `fail-gate`, a human has recorded an override for the soft fail condition. For the kind `external`, the gate can be evaluated. For the kind `manual`, the owner of the wait states in the `resume` action that the condition holds.

A `core` wait record has no safe current state and no next action. Those two items of Section 11.2 apply to `full` only. An overdue wait remains a wait until the change leaves the state `waiting`.

Each kind corresponds to one wait category of Section 11.1:

| Wait Kind | Wait Category |
|---|---|
| `question` | `WAIT_USER_INPUT` |
| `manual` | `WAIT_PROCESS` |
| `fail-gate` | `WAIT_DECISION` |
| `external` | `WAIT_EXTERNAL_SYSTEM` |

The categories `WAIT_DEPENDENCY` and `WAIT_APPROVAL` have no kind of their own in `core`. See AE-50, AE-51, AE-52.

**AE-50 — A wait record needs no safe state and no next action**

- Covers: Section 23.5

Given an `active` change  
When the `wait` action gives the reason `vendor reply needed`, the owner `vendor`, and the resume condition `vendor reply recorded`, and gives no safe state and no next action  
Then the wait record is valid

**AE-51 — Reject a wait without an owner**

- Covers: Section 23.5

Given an `active` change  
When the `wait` action gives a reason and a resume condition but no owner  
Then the action is rejected, and the change remains `active` with no wait record

**AE-52 — A wait kind corresponds to a wait category**

- Covers: Section 23.5

Given a `waiting` change whose wait record has the kind `fail-gate`  
When the wait record is reported in the wait categories of Section 11.1  
Then the category is `WAIT_DECISION`

### 23.6 Evaluation Order

The gates of a `core` change MUST be evaluated in this order, and the evaluation MUST stop as soon as a gate decides the requested action:

1. A fail gate with the severity `hard` that is active decides: the change becomes `closed` with the outcome `failed`.
2. A gate whose condition could not be evaluated decides: the change becomes `waiting` with a wait record of kind `external` (Section 24.2). A condition that could not be evaluated is never a failure.
3. A fail gate with the severity `soft` that is active decides: the change becomes `waiting` with a wait record of kind `fail-gate` until a human disposes of it (Section 24.7).
4. A wait gate that is active decides: the change does not start, resume, or close.
5. For the `close` action only, a done gate that is not satisfied decides: the change does not close.

If no gate decides, the requested action takes effect. The actions `close` and `resume` apply steps 1 to 4, and `close` also applies step 5. The action `start` requires that none of the steps 1 to 4 would decide. Sections 24.2 and 24.7 refine steps 2 and 3. A satisfied done gate does not override a fail gate or a wait gate that is active. A gate that does not apply to the requested action is not evaluated and, when gate results are recorded, is recorded as `not_applicable`. See AE-53, AE-54, AE-55.

**AE-53 — A hard fail decides before the done gates**

- Covers: Section 23.6

Given an `active` change with every done gate satisfied and a fail gate with the severity `hard` active  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed`, not `done`

**AE-54 — A condition that cannot be evaluated is a wait, not a failure**

- Covers: Section 23.6

Given an `active` change with a `check` done gate whose command cannot start because its program is missing  
When the `close` action is requested  
Then the change is `waiting` with a wait record of kind `external`, and no failure is recorded

**AE-55 — A satisfied done gate does not override an active wait gate**

- Covers: Section 23.6

Given an `active` change with every done gate satisfied and a wait gate active  
When the `close` action is requested  
Then the change does not close and remains `active`

### 23.7 Base Gates

Every `core` change has four base gates in addition to the gates in its change definition:

- the scope violation gate, a fail gate with the severity `hard`, which is active when a path changed since the base revision lies outside `scope.allow` (Section 24.5);
- the unanswered question gate, a wait gate, which is active while any question is unanswered (Section 24.8);
- the stale specification approval gate, a wait gate, which is active while `spec.md` differs from the version that was approved (Section 24.3);
- the incomplete evidence gate, a done gate, which is not satisfied until the evidence of every requirement is complete (Section 24.9).

The base gates belong to the `core` method profile. They apply to every `core` change without being listed in its change definition, they MUST NOT be removed, and a lower layer of Section 5.3 MUST NOT weaken or alter them. See AE-56, AE-57, AE-58.

**AE-56 — The scope violation gate applies without being listed**

- Covers: Section 23.7

Given an `active` change whose definition lists no gates and whose `scope.allow` is `lib/**`, and a file under `docs/` changed since the base revision  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed`, because the scope violation gate is a hard fail gate

**AE-57 — A changed specification makes its approval stale**

- Covers: Section 23.7

Given an `active` change whose `spec.md` was approved and then edited  
When the `close` action is requested  
Then the change does not close, because the stale specification approval gate is active, and it can close after a human approves `spec` again

**AE-58 — Incomplete evidence prevents closure**

- Covers: Section 23.7

Given an `active` change with a requirement that has no evidence command  
When the `close` action is requested  
Then the change does not close, because the incomplete evidence gate is not satisfied
