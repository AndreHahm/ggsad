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
| 24. Protections Shared by Both Profiles | Method Semantics |
| 25. State, Hashing, and Schema Versions | Reference-Implementation Requirements |

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

The gate definitions of a change are fixed when the change is approved (Section 24.1).

### 3.4 Evidence over Assertion

A status MUST NOT be set solely by assertion. Verifiable evidence MUST exist for relevant completion criteria.

The evidence for a requirement is executable and is bound to that requirement (Section 24.9).

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

An integration mapping for an external framework or tool is the sixth layer of the resolution in Section 5.3, and it MUST NOT weaken a higher layer.

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

Where a rule of this specification requires a human participant, the claim of being a human is evidenced at an assurance level (Section 24.3).

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

The approved exception exists only for the local specification of a `full` change that departs from a project-wide definition under `docs/definitions/`. A human MUST approve it at the assurance level that Section 24.3 sets for the approval of gate definitions, it applies to that change only, and it is recorded in the Deviations of the evidence of the change (Section 16.4). It is a recorded decision of a human and not a weakening by a lower layer in the sense of Section 5.3, and it never reaches the invariant core, the protections of Section 24, or the base gates of Section 23.7. A `core` change has no such exception. See AE-227, AE-228.

#### `docs/adr/`

Contains durable architecture decisions. Existing accepted ADRs take precedence over new requirements and plans.

### 4.3 Change-Specific Documents

A `full` change keeps its documents in this layout:

```text
specs/<change-id>/
├── state.json
├── spec.md
├── plan.md
├── tasks.md
├── evidence.md
└── review.md
```

`spec.md` remains the mandatory file for normal (Class M and Class L) changes as defined in Section 6.

Every change carries mandatory information regardless of file layout: the goal, specification anchor, gate outcome, evidence, wait or fail behavior when applicable, and final status.

`state.json` is the state document of the change (Section 25.1), and it is a mandatory file only when the project uses persistent, machine-readable workflow state to track phase, status, gates, and history. When state is not persisted that way, the same mandatory information MAY instead be recorded inline in `spec.md` or `evidence.md`. The rules of Sections 24.1, 24.3, 24.4, and 24.8 that read or write the history are enforced mechanically only for a change that has a state document.

A `core` change (Section 23.1) always has a state document, and it keeps its documents in this layout:

```text
specs/<change-id>/
├── change.yaml
├── spec.md
├── state.json
└── review.md
```

`change.yaml`, `spec.md`, and `state.json` are the three documents of a `core` change. `review.md` and other review files are conditional, they are not documents of the change, and the scope check of Section 24.5 measures them like any other file that is not a record file.

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

A compliance profile is resolved together with the method profile as the second layer of Section 5.3, and a lower layer MUST NOT weaken it.

### 5.3 Profile Resolution

The effective workflow MUST be resolved in this order:

1. GG-SAD invariant core,
2. selected method profile and compliance profile, resolved together,
3. project-specific configuration,
4. change-class requirements,
5. local strengthening in the change specification,
6. integration mappings for external frameworks and tools.

A lower layer MUST NOT weaken a higher layer.

Layer 2 is one layer that holds two things. The method profile (Section 5.6) and the compliance profile (Section 5.1) of a change are resolved together, and neither ranks above the other. The number of layers is six, and no layer is added.

A lower layer weakens a higher layer when it does any of these things to a gate that the higher layer defines: it removes the gate, that is, it states that the gate does not apply or it leaves the gate out of a definition that replaces the gates of the higher layer; it alters the condition of the gate, including its kind and every other declaration that Section 24.1 fixes; it lowers its severity (Section 24.7); or it lowers the assurance level that the gate or the action requires (Section 24.3). A lower layer strengthens a higher layer when it adds a gate with an identifier of its own, or when the project configuration raises a required assurance level. Strengthening is permitted at every layer. A lower layer MUST NOT strengthen by redefining a gate of a higher layer: it adds a gate of its own instead. The result of the resolution MUST NOT depend on the order in which layers or their entries are listed, and an entry that is listed later never overrides an entry of a higher layer. See AE-218, AE-219, AE-220, AE-222, AE-224.

The required assurance level of an action is the higher of the levels that the layers state (Section 24.3). A lower layer that states a lower level than a higher layer requires for the same kind of action therefore does not lower it: the statement is accepted and has no effect. See AE-221.

A `core` change implements layers 1, 2, 3, and 5. Layer 1 is the invariant core of Section 3.7 with the protections of Section 24. Layer 2 supplies the base gates of Section 23.7 together with the rules of the compliance profile. Layer 3 is the project configuration, for example the minimum assurance levels of Section 24.3. Layer 5 is the gates and the scope of the change definition (Section 23.1). Layers 4 and 6 are not applicable to a `core` change: the change-class requirements of layer 4 are the size classes of Section 6, which a `core` change does not have, and the integration mappings of layer 6 are not part of the resolution of a `core` change. Both layers are specified for the `full` method profile and for combination use (Sections 3.8 and 17), and in both the rule that a lower layer MUST NOT weaken a higher layer applies. The layers are never renumbered. See AE-226.

An implementation MUST check that a change does not weaken a higher layer when the change is created, and again before the gate definitions of the change are approved (Section 24.1), because a definition can be edited after the change is created. For a `core` change the check compares the change definition with the base gates of Section 23.7. A change definition that states that a base gate does not apply, or that lists a gate with the identifier of a base gate, redefines that base gate. It MUST be rejected with the result `rejected` and `changed` false (Section 22.2), and nothing is written. The stable issue code is `gate-weakened` when the definition states that the base gate does not apply, or when the listed gate differs from the base gate in its kind, its condition, or its severity. The message names the gate and the manner of the weakening: removed, altered, or severity lowered. A listed gate that does not differ from the base gate is rejected as a duplicate identifier (Section 23.3). For a `full` change the check compares the Flow Gates of the change specification with the project-wide definitions (Section 4.2), and an entry that removes or relaxes a condition of a project-wide definition is a weakening unless the approved exception of Section 4.2 covers it. See AE-219, AE-220, AE-222, AE-223, AE-225, AE-227, AE-228.

**AE-218 — Project configuration tightens and the change adds a gate**

- Covers: Section 5.3

Given a project configuration that sets the minimum level A2 for the sign-off of gates, and a `core` change definition that adds the done gate `release-ok` of the kind `sign-off`  
When the change is created  
Then the change is created, the four base gates and `release-ok` all apply, and the sign-off of `release-ok` needs a claim at A2

**AE-219 — Reject a definition that removes a base gate**

- Covers: Section 5.3

Given a `core` change definition that states that the base gate `incomplete-evidence` does not apply to the change  
When the `new` action receives it  
Then the definition is rejected with the issue code `gate-weakened`, the message names `incomplete-evidence` as removed, `changed` is false, and no change is created

**AE-220 — Reject a base gate whose severity is lowered from hard to soft**

- Covers: Section 5.3

Given a `core` change definition that lists a fail gate with the identifier `scope-violation` and the severity `soft`  
When the `new` action receives it  
Then the definition is rejected with the issue code `gate-weakened`, the message names `scope-violation` with its severity lowered, and no change is created

**AE-221 — A lower level in a lower layer does not lower the required level**

- Covers: Section 5.3

Given a project configuration that sets the minimum level A2 for the sign-off of gates, and a `core` change definition whose `sign-off` done gate `legal-ok` states the minimum level A1  
When `human:ada` signs off `legal-ok` with a claim at A1  
Then the sign-off is rejected, because the required level remains A2, and the change definition itself was accepted, because the lower statement has no effect

**AE-222 — Reject the identifier of a base gate with a changed condition**

- Covers: Section 5.3

Given a `core` change definition that lists a wait gate with the identifier `stale-spec-approval` whose condition is active only before the first `start`  
When the `new` action receives it  
Then the definition is rejected with the issue code `gate-weakened`, the message names `stale-spec-approval` as altered, and no change is created

**AE-223 — A restatement that does not differ is a duplicate identifier**

- Covers: Section 5.3

Given a `core` change definition that lists a wait gate with the identifier `unanswered-question`, the same kind, the same condition, and no difference from the base gate  
When the `new` action receives it  
Then the definition is rejected as a duplicate identifier (Section 23.3), and the issue code is not `gate-weakened`, because nothing is weakened

**AE-224 — A strengthening does not offset a later weakening**

- Covers: Section 5.3

Given a `core` change definition that lists the done gate `review-ok` first and, listed after it, a fail gate `scope-violation` with the severity `soft`  
When the `new` action receives it  
Then the whole definition is rejected with the issue code `gate-weakened`, because an entry listed later does not override a higher layer and an added gate does not make up for a weakened one, and no change is created

**AE-225 — Check again before the gate definitions are approved**

- Covers: Section 5.3

Given a `core` change created from a valid definition, and `change.yaml` edited afterwards so that it lists a fail gate `scope-violation` with the severity `soft`  
When `human:ada` approves the target `gates`  
Then the approval is rejected with the issue code `gate-weakened`, `changed` is false, and no approval is recorded

**AE-226 — A `core` change resolves four of the six layers**

- Covers: Section 5.3

Given a `core` change with the compliance profile `standard`, in a project whose configuration sets the minimum level A1 for answers, and whose change definition adds its own gates  
When the effective workflow of the change is resolved  
Then layer 1 (the invariant core), layer 2 (the base gates and the compliance profile together), layer 3 (the project configuration), and layer 5 (the gates of the change definition) contribute, layers 4 and 6 are not applicable, and the six layers keep their numbers

**AE-227 — The approved exception applies to one `full` change only**

- Covers: Section 5.3

Given a project-wide definition of done under `docs/definitions/` with a regression-test criterion, and a `full` change whose local specification states that this criterion does not apply, together with an exception approved by `human:ada` at the level that the approval of gate definitions requires  
When the change is checked before approval, and a second `full` change without an exception is checked as well  
Then the first change is accepted without the criterion and the exception is recorded, and the second change is rejected as weakening the project-wide definition

**AE-228 — The exception never reaches a base gate**

- Covers: Section 5.3

Given a `core` change definition that states that the base gate `incomplete-evidence` does not apply, together with a record of an exception approved by `human:ada`  
When the `new` action receives it  
Then the definition is rejected with the issue code `gate-weakened`, because a `core` change has no exception and a base gate is never covered by one

### 5.4 Non-Delegable Human Approval

Regardless of the active compliance profile or the `lean` profile's self-approval allowance in Section 5.1, the following decisions MUST always be made by a human and MUST NOT be satisfied by agent self-approval:

- approval of a breaking change under Section 13;
- resolution of an ADR conflict requiring a decision under Section 13;
- any decision that would trigger a Definition of Fail condition under Section 12 if left unresolved;
- release approvals required by Ready-to-Release and Release-Done under Sections 9 and 10.

Self-approval under the `lean` profile is permitted only for decisions outside this non-delegable set.

A decision that a human makes is evidenced at an assurance level (Section 24.3). A claim at the level A0 is self-declared, and it does not by itself satisfy a decision that needs a verified human. The self-approval allowance of the `lean` compliance profile that is stated above is unchanged.

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

The scope of a change is stated and measured as Section 24.5 states.

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

### 8.3 Transition Table

| Action | Legal From (Phase/Status) | Precondition | Gate Order | Resulting Phase/Status | Rejection Behavior |
|---|---|---|---|---|---|
| `start` | A non-closed phase with status `ready` | Starting the phase is authorized. | DoF → DoW; current-phase DoR was established by `ready`, and current-phase DoD and next-phase DoR are not applicable. | Same phase with status `active`. | Reject without any partial mutation of persisted state when the precondition or an applicable gate is not satisfied. |
| `complete` | A non-closed phase with status `draft`, `active`, or `done` | From `draft`, the current phase's DoR is satisfied; from `active`, the current phase's DoD is satisfied; from `done`, the next phase's DoR is re-evaluated. | From `draft`: DoF → DoW → current-phase DoR. From `active`: DoF → DoW → current-phase DoD → next-phase DoR. From `done`: DoF → DoW → next-phase DoR; current-phase DoR and DoD are already established. | From `draft`, the same phase with status `ready`. From `active`, satisfied current-phase DoD first produces the current phase with status `done`; satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. From `done`, satisfied next-phase DoR advances to the next phase with status `ready`, while unsatisfied next-phase DoR preserves the current phase with status `done`. Completion of the final phase produces `closed`/`done`. | Reject without any partial mutation of persisted state when the applicable precondition is not satisfied. When DoW, current-phase DoR, or current-phase DoD does not allow the transition, record the evaluation in the history and answer `blocked` (Section 22.2); an active fail condition of the severity `hard` closes the change as failed, and a soft fail condition or a gate that cannot be evaluated puts the change in a wait (Sections 24.7 and 24.2). Unsatisfied next-phase DoR is not a rejection after current-phase DoD succeeds or during re-evaluation from `done`; it preserves the current phase with status `done`. |
| `wait` | Any non-closed phase/status | A DoW condition is active. | DoF → DoW; current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | Same phase with status `waiting`. | Reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure. |
| `resume` | A non-closed phase with status `waiting` | The recorded resume condition is satisfied and the recorded or explicitly required resume phase is non-closed. | DoF → DoW → DoR for the recorded non-closed resume phase or explicitly required earlier non-closed phase; current-phase DoD and next-phase DoR are not applicable. | Recorded non-closed resume phase, or an explicitly required earlier non-closed phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. When the resume-phase DoR is not satisfied or a DoW condition is still active, record the evaluation in the history, remain `waiting`, and answer `blocked` (Section 22.2). Fail when DoF determines failure (Section 24.7). |
| `fail` | Any non-closed phase/status | A DoF condition is active. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `cancel` | Any non-closed phase/status | An authorized cancellation decision exists. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `cancelled`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `supersede` | Any non-closed phase/status | A later goal-bound change is authorized to replace this change. | DoF; DoW, current-phase DoR, current-phase DoD, and next-phase DoR are not applicable. | `closed` phase with status `superseded`, unless DoF determines `failed`. | Reject without any partial mutation of persisted state when the precondition is not satisfied. |
| `reopen` (`full` only) | The `closed` phase with a terminal status | Corrective follow-up work is authorized with a reason and a new goal-bound scope. | DoF for the new corrective scope → DoW for the new corrective scope → DoR for the recorded resume phase or explicitly stated earlier phase; the prior terminal outcome's DoF and DoW, closed-phase DoD, and next-phase DoR are not applicable. | The resume phase recorded at closure, or an explicitly stated earlier phase, with status `active`. | Reject without any partial mutation of persisted state when the precondition or resume-phase DoR is not satisfied; wait when the new corrective scope's DoW determines a pause; fail when the new corrective scope's DoF determines failure. |

**Rejected and Blocked Results per Action (`full`)**

| Action | Answers `rejected` (nothing is written, `changed` is `false`) | Answers `blocked` (the evaluation is recorded, `changed` is `true`) |
|---|---|---|
| `start` | The phase does not have the status `ready`, the start is not authorized, or an applicable gate does not allow the start (issue code `start-blocked`). | Never. |
| `complete` | The phase and status are not a legal source, or the applicable precondition is not satisfied. | DoW, current-phase DoR, or current-phase DoD does not allow the transition, including a wait that a soft fail condition or a gate that cannot be evaluated causes. |
| `wait` | The change is closed, or no DoW condition is active. | Never. |
| `resume` | The status is not `waiting`, the resume condition is not satisfied, or the resume phase is closed. | The resume-phase DoR is not satisfied, or a DoW condition is still active, so that the change remains `waiting`. |
| `fail` | The change is closed, or no DoF condition is active. | Never. |
| `cancel` | The change is closed, or no authorized cancellation decision exists. | Never. |
| `supersede` | The change is closed, or no later change is authorized to replace this change. | Never. |
| `reopen` | The change is not in the `closed` phase, the corrective follow-up work is not authorized with a reason and a new goal-bound scope, or the resume-phase DoR is not satisfied. | Never. |

An action whose evaluation closes the change as failed answers `success` (Section 24.7). An action answers `blocked` only where this table lists a case, and a `complete` that preserves the current phase with the status `done` because the next-phase DoR is not satisfied answers `success`. See AE-121, AE-122, AE-123, AE-124.

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

### 8.4 Cancellation, Supersession, Reopening, and Terminal Behavior

`cancel` moves any non-closed phase/status to the `closed` phase with status `cancelled` when an authorized cancellation decision exists. `supersede` moves any non-closed phase/status to the `closed` phase with status `superseded` when a later change replaces this change's goal.

For `cancel` and `supersede`, an active DoW condition does not prevent the authorized terminal
action. DoW and the current- and next-phase readiness and completion gates are not applicable to
these actions. DoF retains first priority; when DoF determines that the change has failed, the
resulting terminal status is `failed` rather than `cancelled` or `superseded`.

The comparison of the gate definitions with the approved ones (Section 24.1) does not stop `cancel` or `supersede`.

A fail condition of the severity `hard` closes the change as failed without human action, and a fail condition of the severity `soft` waits for a human, who either closes the change with `fail` or records an override (Section 24.7).

In the `full` method profile, `reopen` moves a change from the `closed` phase back to the resume phase recorded at closure, or to an explicitly stated earlier phase, for corrective follow-up work. The action MUST record its reason and the new goal-bound scope in history. The method profile `core` has no `reopen` action (Section 23.4). See AE-217.

In the `full` method profile, once a change is in the `closed` phase, no further phase advancement is legal except through `reopen`. A `closed` `core` change is final.

**AE-217 — Reopen a closed `full` change**

- Covers: Section 8.4

Given a `full` change in the `closed` phase with the status `done`, whose resume phase recorded at closure is the build phase  
When the `reopen` action is requested with a reason and a new goal-bound scope, and the Definition of Ready of the build phase is satisfied  
Then the change is in the build phase with the status `active`, and the reason and the new scope are recorded in the history

### 8.5 Evaluation Priority

The following order MUST be applied during every gate evaluation:

1. DoF
2. DoW
3. DoR for the current phase
4. DoD for the current phase
5. DoR for the next phase

A satisfied DoD does not override a satisfied DoF or DoW.

This order defines evaluation precedence. A gate that is not applicable to the requested action or current state is skipped and, when gate evidence is recorded, MUST be recorded as `not_applicable`. Evaluation MUST stop as soon as a gate determines the requested action's outcome.

A gate evaluation has one of three results: `satisfied`, `not_satisfied`, or `not_evaluable`. A gate that cannot be evaluated is neither failed nor `not_applicable`: the change waits, and a known hard failure is decided before it. Section 24.2 specifies these results and refines this order.

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

A question about the goal or the problem that is still open is recorded as an open question of the change (Section 24.8).

### 9.5 Ready-to-Plan

At minimum:

- goal, scope, and non-goals are defined,
- requirements and acceptance conditions are understandable,
- relevant architecture and ADR constraints have been reviewed,
- all open questions have been answered (Section 24.8),
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
- all open questions have been answered (Section 24.8),
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

Whether unintended scope has been introduced is measured as Section 24.5 states.

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

`WAIT_EXTERNAL_SYSTEM` is the category of the wait that a gate causes when it cannot be evaluated (Section 24.2).

`WAIT_DECISION` is the category of the wait that a soft failure causes while it awaits a human disposition (Section 24.7).

### 11.2 Mandatory Content of a Wait State

Every wait state MUST include:

- reason,
- outstanding information or decision,
- responsible person or source,
- resume condition,
- safe current state,
- next action after resumption.

Template:

```json
{
  "status": "waiting",
  "reason": "architecture-decision-required",
  "waiting_for": "requestor",
  "resume_when": "ADR-approved",
  "safe_state": "no-uncommitted-destructive-change",
  "resume_at": "planning",
  "next_action": "update-plan"
}
```

In the state document, `status` is a field of the `after` record of an entry, and the other fields of this content are the value of its field `wait` (Section 25.1).

### 11.3 AI Agent Behavior in a Wait State

An AI agent MUST:

- stop all risky or scope-changing actions,
- preserve the current state,
- state the missing decision precisely,
- formulate one minimal, decidable question,
- never interpret an assumption as approval,
- resume at the defined point once the resume condition is satisfied.

The question that the agent formulates is recorded as an open question of the change (Section 24.8).

---

## 12. Definition of Fail

DoF describes conditions under which the flow MUST terminate unsuccessfully.

The obligation to terminate applies to a fail condition of the severity `hard`. A fail condition of the severity `soft` pauses the flow for a human disposition (Section 24.7).

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

A gate that cannot be evaluated is not a failure and does not count toward a retry limit (Section 24.2).

A retry limit is a soft fail condition (Section 24.7).

The approved scope is the allowed path list of Section 24.5. A path that changed since the base revision and that lies outside the allowed path list is a hard failure.

The interpreter that runs the commands of gates is explicit and opt-in (Section 24.10).

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

**Severity**  
`hard`
```

Every fail rule also states its severity, `hard` or `soft` (Section 24.7).

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

Whether a participant is a human is a claim that is evidenced at an assurance level (Section 24.3).

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

Where evidence is recorded in the history of a change, the consistency and the completeness of that history are verified as Section 24.4 states.

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

A check-command gate whose evidence is a test run MAY carry a baseline of known failures (Section 24.6).

The commands that produce evidence are run as Section 24.10 states.

The evidence of a requirement is complete only with an executable check that is bound to that requirement (Section 24.9). The records that the list above names supplement that check and do not replace it.

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

The executable check of Section 24.9 is still required when the evidence is documented in `spec.md`.

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

The conditions listed under Flow Gates, together with the scope, are the gate definitions of the change and are fixed when the change is approved (Section 24.1).

The evidence commands of a requirement of the change specification are bound to it as Section 24.9 states.

The section Open Questions of the change specification is a view of the questions that are recorded as state (Section 24.8).

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

A gate that could not be evaluated is not recorded as Yes or No in the Final Gate Evaluation. It is listed by name with its cause (Section 24.2).

The Evidence column of the requirement coverage table names the executable check that is bound to the requirement (Section 24.9). Other records MAY be added to it.

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

In steps 3 to 5, a gate that cannot be evaluated is neither failed nor satisfied: the change waits, as Section 24.2 states.

In step 9, the approved scope is the allowed path list, and it is measured as Section 24.5 states.

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
- no soft failure awaits a human disposition (Section 24.7),
- no open question is unanswered (Section 24.8),
- all required DoD criteria are satisfied,
- the executable evidence of every requirement is complete (Section 24.9),
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
- record a human decision (an approval, a sign-off, an override, or an answer) in the history of a change;
- migrate a schema-governed file to a newer schema version, as an explicit operation whose steps are recorded (Section 25.3);
- evaluate and execute one controlled state transition under the Section 8 Transition Table.

The contract specifies observable behavior and compatibility requirements only. It does not prescribe a programming language, module structure, or vendor-specific agent interface.

### 22.2 Minimal Result Envelope

Every contract operation MUST return a result envelope containing three fields present in every response regardless of outcome: `operation`, identifying which contract operation ran; `result`, whose value is one of `success`, `rejected`, `blocked`, or `error` and is never partial; and `changed`, indicating whether persistent state changed.

The four results are exact lowercase names with these meanings:

- `success`: the operation took effect;
- `rejected`: the operation was invalid, or a precondition of the operation was not met; nothing was written, and `changed` is `false`;
- `blocked`: the operation was valid, its evaluation was recorded in the history, and the requested transition did not occur; `changed` is `true`;
- `error`: the operation could not be carried out; nothing was written, and `changed` is `false`.

A `rejected` result with `changed` true and a `blocked` result with `changed` false are invalid. Only the actions that complete a change or a phase and the action `resume` can answer `blocked`: `close` and `resume` of a `core` change (Section 23.4), and `complete` and `resume` of a `full` change (Section 8.3). Every other action answers `rejected` when it does not take effect. An action whose evaluation closes the change as failed answers `success` (Section 24.7). See AE-111, AE-112, AE-113, AE-116.

The `state` field contains the resulting state of the change and is included when applicable to the operation; it is omitted when the operation produces no state result. For a `full` change it contains the phase and status. As defined in Section 8, the phase may be `closed`, while the status carries the terminal outcome. For a `core` change it contains the state and the outcome (Section 23.2). The `issues` field contains stable codes plus human-readable messages. It is included whenever `result` is `rejected`, `blocked`, or `error`, and it then contains at least one issue; it is omitted whenever `result` is `success`. A result other than `success` without an issue is invalid. The `data` field is always optional operation-specific output and is present only when relevant to the operation. See AE-114, AE-115.

A goal summary, specification anchor, gate outcome, evidence references, and timestamp are not universally required envelope fields. They MAY appear inside `data` when relevant to a specific operation.

An operation that uses a schema-governed file whose `schema_version` the implementation cannot use is refused with the result `rejected`, `changed` false, and nothing written. The stable issue code is `migration-required` when the version is older and can be migrated, `schema-version-unsupported` for every other unusable value, and `schema-version-mismatch` when the version of a state document differs from the latest recorded one (Section 25.3). See AE-204, AE-205, AE-206, AE-211.

**AE-111 — A blocked result is recorded and changes state**

- Covers: Section 22.2

Given an `active` `core` change with a done gate that is not satisfied  
When the `close` action is requested  
Then the result is `blocked` with `changed` true, the issues name the unsatisfied gate, the evaluation is recorded in the history, and the state remains `active`

**AE-112 — A rejected result writes nothing**

- Covers: Section 22.2

Given an `open` `core` change  
When the `close` action is requested  
Then the result is `rejected` with `changed` false, the issues state that the change is not `active`, and nothing is written to the history

**AE-113 — Reject an envelope whose changed value contradicts its result**

- Covers: Section 22.2

Given an envelope with the result `rejected` and `changed` true, and an envelope with the result `blocked` and `changed` false  
When the two envelopes are validated  
Then both are invalid

**AE-114 — Reject an envelope with no issue**

- Covers: Section 22.2

Given an envelope with the result `blocked` and an empty `issues` field  
When the envelope is validated  
Then the envelope is invalid, because every result other than `success` has at least one issue

**AE-115 — The state field is worded per method profile**

- Covers: Section 22.2

Given a closed `core` change with the outcome `done` and a `full` change in the build phase with the status `done`  
When the `state` field of the envelope of each change is read  
Then the `state` field of the `core` change contains the state `closed` and the outcome `done`, and the `state` field of the `full` change contains the phase `build` and the status `done`

**AE-116 — Reject a result name that is not exact lowercase**

- Covers: Section 22.2

Given an envelope with the result `Blocked`  
When the envelope is validated  
Then the envelope is invalid, because the results are the exact lowercase names `success`, `rejected`, `blocked`, and `error`

### 22.3 Rejection and Output Requirements

An invalid operation MUST be rejected without any partial mutation of persisted state. Its `result` MUST be `rejected` or `error`, and `changed` MUST be `false`.

A valid operation whose evaluation says that the requested transition does not occur is not an invalid operation. When the evaluation is recorded in the history, its result is `blocked` and `changed` is `true`; recording it is what makes the attempts countable under Section 24.2. An operation that is invalid, or whose precondition is not met, stays `rejected` or `error` with `changed` false. Sections 8.3 and 23.4 state per action which result applies. See AE-111, AE-112.

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

- `schema_version`: the version of the schema of the change definition (Section 25.3);
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

Given a change definition with the fields `schema_version` set to a supported version, `id`, `method_profile` set to `core`, `compliance_profile`, `author`, `owner`, `goal`, `scope`, `requirements`, and `gates`  
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

The actions `approve`, `fail`, `cancel`, `supersede`, and `adopt` MUST be performed by a human participant. An `answer` to a question whose owner is a human MUST also be given by a human (Section 24.3). See AE-24.

The actions `check`, `review`, and `guard` are read-only. They report on a change, they never change its state or its history, and they are legal from every state. They are not rows of the table. See AE-49.

The method profile `core` has no `reopen` action. A change in the state `closed` is final, and follow-up work is a new change that names the closed change in `follows` (Section 23.1). See AE-48.

A `follows` field is a reference and not a state transition: it never changes the state or the outcome of the change that it names, so that no `core` change leaves the state `closed`. A new change whose `follows` names a change that has not ended, because that change is `open`, `active`, or `waiting`, or that names a change that does not exist, is rejected, and nothing is written. See AE-11, AE-12, AE-215, AE-216.

**Rejected and Blocked Results per Action (`core`)**

| Action | Answers `rejected` (nothing is written, `changed` is `false`) | Answers `blocked` (the evaluation is recorded, `changed` is `true`) |
|---|---|---|
| `new` | The change definition is invalid, the identifier is not unique, `follows` does not name a closed change, or no method profile is selected. | Never. |
| `approve` | The target is invalid or its preconditions are not met, the approver is not a human where Section 24.3 requires one, or the gate definitions differ from the approved ones and the target is not the gate definitions (Section 24.1). | Never. |
| `start` | The state is not `open`, or a precondition is not met, including a fail gate, a wait gate, or a gate that cannot be evaluated that would decide against the start (issue code `start-blocked`). | Never. |
| `wait` | The state is not `active`, or the reason, the owner, or the resume condition is missing. | Never. |
| `ask` | The state is not `open` or `active`, or the question is not valid. | Never. |
| `answer` | The state is `closed`, the question does not exist or is already answered, or the answer is not valid or not given by the owner of the question. | Never. |
| `resume` | The state is not `waiting`, or the resume condition of the wait record is not satisfied. | The evaluation of Section 23.6 finds a gate that keeps the change waiting. |
| `close` | The state is not `active`. | The evaluation of Section 23.6 finds a wait gate active, a done gate not satisfied, a soft failure, or a gate that cannot be evaluated, so that the change does not close. |
| `fail` | The state is not `waiting` with a wait record of kind `fail-gate`, or no reason is given. | Never. |
| `cancel` | The state is `closed`. | Never. |
| `supersede` | The state is `closed`, or `replaced_by` is missing, names the change itself, or names a change that does not exist. | Never. |
| `adopt` | The history already has an anchor. | Never. |

A `close` or a `resume` whose evaluation finds a fail gate of the severity `hard` active answers `success` with the state `closed` and the outcome `failed` (Section 24.7). An action answers `blocked` only where this table lists a case. See AE-117, AE-118, AE-119, AE-120.

**AE-117 — Start with an unmet gate is rejected**

- Covers: Section 23.4

Given an `open` `core` change with a wait gate that is active  
When the `start` action is requested  
Then the result is `rejected` with `changed` false and the issue code `start-blocked`, and the change remains `open`

**AE-118 — Resume is rejected while the resume condition is not satisfied**

- Covers: Section 23.4

Given a `waiting` `core` change with a wait record of kind `question` for Q1, and Q1 is unanswered  
When the `resume` action is requested  
Then the result is `rejected` with `changed` false, and nothing is written to the history

**AE-119 — Resume is blocked while a wait gate is still active**

- Covers: Section 23.4

Given a `waiting` `core` change whose awaited question is answered and whose wait gate `vendor-reply` is still active  
When the `resume` action is requested  
Then the result is `blocked` with `changed` true, the issues name `vendor-reply`, the evaluation is recorded in the history, and the change remains `waiting`

**AE-120 — A close that triggers a hard failure answers success**

- Covers: Section 23.4

Given an `active` `core` change with a fail gate of the severity `hard` that is active  
When the `close` action is requested  
Then the result is `success`, the state is `closed`, and the outcome is `failed`

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

**AE-215 — Following a closed change leaves it closed**

- Covers: Section 23.4

Given a `core` change A that is `closed` with the outcome `cancelled`  
When a new change B names A in `follows`, and B is started and closed  
Then A keeps its state `closed` and its outcome `cancelled`, and no entry is added to the history of A by the creation or by the later actions of B

**AE-216 — Following a change that is waiting or does not exist is rejected**

- Covers: Section 23.4

Given a `core` change A in the state `waiting`, and no change with the identifier `c-9`  
When a new change B names A in `follows`, and another new change names `c-9` in `follows`  
Then both creations are rejected, nothing is written, and no change B exists

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

The base gates have the identifiers `scope-violation`, `unanswered-question`, `stale-spec-approval`, and `incomplete-evidence`. A change definition that redefines one of them, or that states that one does not apply, is rejected as Section 5.3 states, at the creation of the change and again before the approval of its gate definitions. See AE-219, AE-225.

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

---

## 24. Protections Shared by Both Profiles

This section specifies protections that apply to both method profiles (Section 5.6). Every protection in Sections 24.1 to 24.10 applies to a `core` change and to a `full` change. Each rule is written once in this section, and the other sections point to it.

The protections use terms that name different artifacts in the two method profiles:

| Term in This Section | In `core` | In `full` |
|---|---|---|
| Change definition | `change.yaml` (Section 23.1) | The change specification, including its Flow Gates (Section 16.1) |
| History | `state.json` (Section 25.1) | The state file, or the inline record where no state file is persisted (Section 4.3) |
| Base revision | The revision recorded when the `start` action succeeds (Section 23.4) | The revision recorded when the change starts (Section 24.5) |
| Human | A participant that is a human person (Section 24.3) | A participant that is a human person (Sections 5.4 and 24.3) |

Identifiers, path patterns, paths, and text values are compared as sequences of Unicode code points, without normalization (Section 25.1). Result names are exact lowercase strings. A rule of this section that compares values compares them in this way unless the rule states otherwise. See AE-60.

**AE-60 — Compare identifiers as code point sequences**

- Covers: Section 24

Given a change definition with two gate identifiers that look the same, the first written `café` with the single code point U+00E9 and the second written `cafe` followed by the code point U+0301  
When the change definition is validated  
Then the two identifiers are different, because values are compared as sequences of code points without normalization, and the definition is not rejected for a duplicate identifier

### 24.1 Frozen Gate Definitions

The gate definitions of a change are fixed when the change is approved. They are the gates of the change definition, that is, the three gate lists of a `core` change (Section 23.3) or the Flow Gates of a `full` change (Section 16.1), together with everything those gates declare (conditions, severities, retry limits, commands, exit maps, time limits, extraction rules, and baselines) and the scope of the change (Section 24.5). The purpose is that no participant can change the gates that judge a change without a human approving the change again. Before the first approval of the gate definitions nothing is fixed, and this section stops no operation.

The identity of the fixed definitions is the content hash (Section 25.2) of the parsed gate definitions, computed over the parsed values and not over the text of the file. A comment, the layout, the order of keys in a mapping, and the quoting of a value that parses to the same value therefore do not change the identity. The order of the elements of a list does change it, because that order is part of the parsed value. The hash computed at the approval is the approved hash and is recorded in the history. See AE-79, AE-80.

Every state-changing operation MUST first compute the hash of the current gate definitions and compare it with the approved hash. When the two differ, the operation MUST write nothing, and its result MUST be `rejected` with `changed` false (Section 22.2) and the stable issue code `gates-changed`, whose message states that the gate definitions differ from the approved ones and that a human has to approve them again. See AE-75, AE-76, AE-86.

Three operations are exempt from the comparison and MUST NOT be stopped by it: `cancel`, `supersede`, and the approval of the gate definitions that replaces the approved hash. The exemption of `cancel` and `supersede` ensures that a change whose definitions were altered can always be ended. The approval that replaces the approved hash is the re-approval; without the exemption, no change could leave this state. See AE-77, AE-78, AE-81.

The re-approval MUST be performed by a human at the assurance level that Section 24.3 requires for the approval of gates. It is recorded in the history as an amendment, not as an approval, and the record names the approved hash that it replaces and the new approved hash. After the re-approval the new hash is the approved hash, and an override of a soft failure that is bound to the earlier hash lapses (Section 24.7). See AE-81, AE-85.

A read-only operation does not write. While the hashes differ, it answers `rejected` with `changed` false and the issue code `gates-changed`, and it states in its report that the gates are not enforced. It never closes the change and never records a failure. See AE-82.

The approval of gate definitions MUST be rejected when the change definition has no gate definitions at all (in `core`, no `gates` field; in `full`, no Flow Gates). A definition that holds empty lists of additional gates is valid and is fixed as it is: an empty list is a definition, and a gate added to it later is a difference. See AE-83, AE-84.

The requirement identifiers and the evidence commands that are bound to them are also fixed with the gate definitions (Section 24.9). See AE-169.

**AE-75 — An unchanged fixed set passes the comparison**

- Covers: Section 24.1

Given a `core` change whose gate definitions were approved and have not changed since  
When the `close` action is requested  
Then the hash of the current gate definitions equals the approved hash, and the action goes on to evaluate the gates under Section 23.6

**AE-76 — Reject an operation when the gate definitions differ**

- Covers: Section 24.1

Given a `core` change whose gate definitions were approved, and the severity of the fail gate `no-secrets` was edited from `hard` to `soft` after the approval  
When the `close` action is requested  
Then the result is `rejected` with `changed` false and the issue code `gates-changed`, and nothing is written to the history

**AE-77 — Cancel is not stopped by differing gate definitions**

- Covers: Section 24.1

Given a `core` change whose gate definitions differ from the approved ones  
When a human performs the `cancel` action  
Then the state is `closed` and the outcome is `cancelled`

**AE-78 — Supersede is not stopped by differing gate definitions**

- Covers: Section 24.1

Given a `core` change A whose gate definitions differ from the approved ones, and an existing change B  
When a human performs the `supersede` action on change A with `replaced_by` naming change B  
Then change A is `closed` with the outcome `cancelled` and `replaced_by` naming change B

**AE-79 — A formatting-only edit does not differ**

- Covers: Section 24.1

Given a `core` change whose gate definitions were approved, and a comment was added and the indentation of `change.yaml` was changed after the approval, so that the parsed gate definitions are the same  
When the `close` action is requested  
Then the hashes are equal, and the action is not rejected for differing gate definitions

**AE-80 — A reordered gate list differs**

- Covers: Section 24.1

Given a `core` change whose approved done gates are `lint` followed by `tests-pass`, and the two gates were swapped after the approval  
When the `close` action is requested  
Then the hashes differ, because the order of a list is part of the parsed value, and the result is `rejected` with the issue code `gates-changed`

**AE-81 — Record the re-approval as an amendment**

- Covers: Section 24.1

Given a `core` change whose gate definitions differ from the approved ones  
When a human approves the gate definitions again  
Then the history records an amendment that names the earlier approved hash and the new approved hash, the new hash is the approved hash, and a following `close` action is evaluated under Section 23.6

**AE-82 — A read-only report states that the gates are not enforced**

- Covers: Section 24.1

Given a `core` change whose gate definitions differ from the approved ones  
When the `check` action is requested  
Then the result is `rejected` with `changed` false and the issue code `gates-changed`, the report states that the gates are not enforced, and the history does not change

**AE-83 — Reject the approval of absent gate definitions**

- Covers: Section 24.1

Given a `core` change whose change definition has no `gates` field  
When a human approves the gate definitions  
Then the approval is rejected, and no approved hash is recorded

**AE-84 — Accept empty lists of additional gates**

- Covers: Section 24.1

Given a `core` change whose `gates` field holds the empty lists `fail`, `wait`, and `done`  
When a human approves the gate definitions  
Then the approval is recorded with the hash of these definitions, and a gate added to a list later makes the hashes differ

**AE-85 — Reject a re-approval by a participant that is not a human**

- Covers: Section 24.1

Given a `core` change whose gate definitions differ from the approved ones  
When an AI agent approves the gate definitions again  
Then the approval is rejected, the approved hash does not change, and the change remains stopped by the comparison

**AE-86 — Reject another approval while the gate definitions differ**

- Covers: Section 24.1

Given a `core` change whose gate definitions differ from the approved ones  
When a human approves the target `spec`  
Then the result is `rejected` with `changed` false and the issue code `gates-changed`, and no approval is recorded

### 24.2 Three-Valued Gate Results

Every evaluation of a gate ends in exactly one of three results:

- `satisfied`: the evaluation established that the condition of the gate holds;
- `not_satisfied`: the evaluation established that the condition of the gate does not hold;
- `not_evaluable`: the evaluation could not establish either, because the gate could not be evaluated.

A done gate is met when its result is `satisfied`. A fail gate and a wait gate are active when their result is `satisfied`, that is, when the condition they describe holds. Every result is recorded in the history together with the gate it belongs to. A name in another letter case, or any other name, is not a result and MUST be rejected. See AE-61.

A gate cannot be evaluated when any of these holds:

- the command of the gate cannot start, for example because its program is missing;
- the command exceeds the time limit that the gate declares and is stopped;
- the command ends without an exit status, or with an exit status that the exit map of the gate does not map;
- the command reports that a module, tool, or dependency it needs is missing, either through an exit status that the exit map maps to `not_evaluable` or through output that the gate declares for that purpose;
- version control is unavailable to a gate that needs it;
- the gate needs the base revision and the change has started without one (Section 24.5);
- any other exception occurs during the evaluation.

A gate that is `not_evaluable` is not a failure. Its result MUST NOT be recorded as `not_satisfied`, it MUST NOT make a fail gate active, and it MUST NOT count toward any retry limit. The record of the result MUST name the gate and the cause. See AE-62.

An action that evaluates gates decides from the results in this order, and the first rule that applies decides:

1. A fail gate with the severity `hard` that is active: the change fails (Section 24.7).
2. A gate that is `not_evaluable`: the change waits. In `core`, the change is `waiting` with a wait record of kind `external` (Section 23.5). In `full`, the change has the status `waiting` and a wait state of the category `WAIT_EXTERNAL_SYSTEM` (Section 11.1), whose resume condition is that the gate can be evaluated and whose next action after resumption is the evaluation of the gate again.
3. A fail gate with the severity `soft` that is active: the change waits for a human disposition (Section 24.7).
4. A wait gate that is active: the change does not advance.
5. For an action that completes a change or a phase, a done gate that is `not_satisfied`: the change does not complete.

A known hard failure therefore outranks a gate that cannot be evaluated. This order refines Section 8.5 and Section 23.6. The `start` action requires that none of the rules 1 to 4 would decide: when one would, `start` is rejected and no wait is created. When the action is `resume`, the wait record created by rule 2 replaces the earlier record, whose resume condition was met. An action that only reports on a change reports the result and creates no wait. See AE-69, AE-71, AE-72, AE-74.

A retry limit is a fail condition that becomes active when the number of `not_satisfied` results recorded for a named gate reaches a limit. The count is the number of `not_satisfied` results of that gate in the history over the whole life of the change, a non-negative integer. The limit is a non-negative integer, and it is reached when the count is greater than or equal to the limit: with a limit of three, the third `not_satisfied` result reaches it and the second does not. A `satisfied` result, a `not_evaluable` result, and a `not_applicable` record are not counted, and a `not_evaluable` result between two `not_satisfied` results neither adds to the count nor resets it. A retry limit that is not a non-negative integer is invalid and MUST be rejected when the gate definitions are approved. See AE-63, AE-64, AE-70.

Every evaluation records its own result. When the cause of a `not_evaluable` result is removed and the gate is evaluated again, the new result is recorded and the earlier record remains in the history unchanged. See AE-67.

A check-command gate is a gate whose condition is the outcome of a command. In `core`, it is a done gate of the kind `check` (Section 23.3). In `full`, it is a condition of a Flow Gates list (Section 16.1) that names a command. The definition of a check-command gate declares:

- the command as an argument list, in which the program and each argument are separate elements and no shell interprets them;
- the exit map: the exit statuses, which are non-negative integers, that mean `satisfied`; the exit statuses that mean `not_satisfied`; and OPTIONALLY the exit statuses that mean `not_evaluable`. An exit status appears at most once in the map;
- OPTIONALLY, a time limit and the rule by which failure identifiers are extracted from the output (Section 24.6).

A definition of a check-command gate without a command or without an exit map is invalid and MUST be rejected when the gate definitions are approved. An exit status that the exit map does not map is `not_evaluable`. Except for the baseline comparison of Section 24.6, the output of a command does not change the result that the exit map decides. Empty output never makes a gate `satisfied`: only an exit status that the exit map maps to `satisfied` does. This specification names no programming language, test runner, or output format. Section 24.10 governs the interpreter that runs the command. See AE-65, AE-66, AE-73.

`not_applicable` is not a result. It is the marker that Sections 8.5 and 23.6 prescribe for a gate that is not evaluated by design, because it does not apply to the requested action or because the commands of gates were deliberately not run for the action. A `not_applicable` record is not a failure, does not count toward a retry limit, and is not `not_evaluable`: a gate that applies to the action and could not be evaluated is `not_evaluable`. See AE-68.

**AE-61 — Reject a result name that is not exact lowercase**

- Covers: Section 24.2

Given the evaluation of the gate `tests-pass`  
When a record names the result `Satisfied`  
Then the record is rejected and nothing is recorded, because the only results are the exact lowercase names `satisfied`, `not_satisfied`, and `not_evaluable`

**AE-62 — A missing program is not a failure and consumes no attempt**

- Covers: Section 24.2

Given the `check` done gate `tests-pass`, a soft fail gate that is active when `tests-pass` has three `not_satisfied` results, and a history with two `not_satisfied` results of `tests-pass`  
When the `close` action is requested and the program of the command of `tests-pass` is missing  
Then the result of `tests-pass` is `not_evaluable`, the count remains two, the fail gate is not active, and the change is `waiting` with a wait record of kind `external`

**AE-63 — The limit-th not_satisfied result reaches the limit**

- Covers: Section 24.2

Given a retry limit of three for `tests-pass` and a history with two `not_satisfied` results and, between them, one `not_evaluable` result  
When the next evaluation of `tests-pass` is `not_satisfied`  
Then the count is three, the limit is reached, and the fail condition is active

**AE-64 — The result before the limit does not reach it**

- Covers: Section 24.2

Given a retry limit of three for `tests-pass` and a history with one `not_satisfied` result and one later `not_evaluable` result  
When the next evaluation of `tests-pass` is `not_satisfied`  
Then the count is two, because the `not_evaluable` result is not counted, the limit is not reached, and the fail condition is not active

**AE-65 — An unmapped exit status is not evaluable**

- Covers: Section 24.2

Given a check-command gate whose exit map maps the exit status 0 to `satisfied` and the exit status 1 to `not_satisfied`  
When its command ends with the exit status 2  
Then the result is `not_evaluable`, not `not_satisfied`, and the output of the command does not change it

**AE-66 — Empty output never makes a gate satisfied**

- Covers: Section 24.2

Given a check-command gate whose exit map maps the exit status 0 to `satisfied` and the exit status 1 to `not_satisfied`  
When its command ends with the exit status 1 and writes no output, and a second evaluation ends with the exit status 2 and writes no output  
Then the first result is `not_satisfied` and the second result is `not_evaluable`, and neither is `satisfied`

**AE-67 — A re-evaluation keeps the earlier record**

- Covers: Section 24.2

Given a history with a `not_evaluable` result of `tests-pass`, recorded because its program was missing  
When the program is installed and `tests-pass` is evaluated again with the result `satisfied`  
Then the new result is recorded, and the earlier `not_evaluable` record remains in the history unchanged

**AE-68 — A gate that does not apply differs from a gate that cannot be evaluated**

- Covers: Section 24.2

Given the `check` done gate `docs-built`, which does not apply to the `start` action and applies to the `close` action, and whose command cannot start  
When the `start` action is evaluated and later the `close` action is evaluated  
Then `docs-built` is recorded as `not_applicable` for `start` and as `not_evaluable` for `close`, and only the second puts the change in a wait

**AE-69 — A hard failure is decided before a gate that cannot be evaluated**

- Covers: Section 24.2

Given an `active` `core` change with a fail gate of the severity `hard` that is active and a `check` done gate whose command cannot start  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed`, and no wait record is created

**AE-70 — Reject a retry limit that is not a non-negative integer**

- Covers: Section 24.2

Given gate definitions with a retry limit of -1 for one gate and a retry limit of 2.5 for another  
When the gate definitions are approved  
Then the approval is rejected for both limits, and no approval is recorded

**AE-71 — A gate that cannot be evaluated puts a `full` change in a wait**

- Covers: Section 24.2

Given a `full` change in the build phase with the status `active`, whose Definition of Done includes a check-command gate that cannot be evaluated because version control is unavailable  
When the `complete` action is requested  
Then the change has the status `waiting` in the build phase with a wait state of the category `WAIT_EXTERNAL_SYSTEM`, and no failure is recorded

**AE-72 — A report on a change creates no wait**

- Covers: Section 24.2

Given an `active` `core` change with a `check` done gate that is `not_evaluable`  
When the `check` action is requested  
Then the report names the gate and the cause, no wait record is created, and the state remains `active`

**AE-73 — Reject a check-command gate without an exit map**

- Covers: Section 24.2

Given a change definition with a `check` done gate that declares a command and no exit map  
When the gate definitions are approved  
Then the approval is rejected, because a check-command gate without an exit map is invalid, and no approval is recorded

**AE-74 — Start is rejected, not put in a wait, when a gate cannot be evaluated**

- Covers: Section 24.2

Given an `open` `core` change with a wait gate whose condition cannot be evaluated  
When the `start` action is requested  
Then the action is rejected, the change remains `open`, and no wait record is created

### 24.3 Assurance Levels and Signed Approval

Every action on a change is performed under an identity that the participant claims. This section defines three assurance levels, which state how well a claim was checked; the statement that a signed approval signs; the actions that only a human may perform; and the limit of what any level proves.

There are three assurance levels. In order from the lowest to the highest they are `A0`, `A1`, and `A2`, and these exact strings are their names:

- `A0`, self-declared: no check of the claim exists. Every claim is worth exactly A0 unless a verifier establishes a higher level;
- `A1`, platform review: the latest review by the platform account that the project configuration maps to the claimed identity is an approval of the revision that is checked out, and none of the files that are approved has an uncommitted change. The review is recorded by the platform that hosts the project, on the review object of the change, for example a pull request;
- `A2`, signature: the claim carries a valid signature over exactly the statement that the implementation builds for the action, made with a key that is listed for the claimed identity in a signers file. The signers file is kept outside the repository of the project, so that a participant who can change the repository cannot add a key for itself.

The levels, their order, and the statement defined below are normative. The verifiers are not: an implementation MAY verify `A1`, `A2`, or both. An implementation that verifies neither treats every claim as A0. An implementation that verifies A2 MUST verify it over the statement defined below and over no other statement.

Verification MUST fail closed. A claim whose level cannot be established is A0, whatever the reason: no verifier exists, the platform does not answer, the signers file cannot be read, the signature is not valid, the key is not listed for the identity, or the statement that was signed differs from the statement that the implementation builds. An action whose required level is higher than the verified level of its claim MUST be rejected, with `changed` false (Section 22.2). A claim that carries no signature and no review is not malformed: it is a claim at A0, and it is rejected only where the required level is higher. See AE-125, AE-127, AE-129, AE-130.

The required level of an action is the higher of two minimums: the minimum that the gate states, when the action serves a gate (a sign-off gate, or the fail condition of an override), and the minimum that the project configuration sets for the kind of action. The kinds of action are the approval of the specification, the approval and the re-approval of gate definitions, the sign-off of a gate, an override, an answer, `cancel` and `supersede`, `fail`, and `adopt`. A minimum that is not stated is A0. This specification assigns no minimum to a compliance profile (Section 5.1): a compliance profile reaches a level only through a gate or through the project configuration. See AE-131, AE-132.

These actions MUST be performed by a human: every approval, the sign-off of a gate, an override, an answer to a question whose owner is a human, `cancel`, `supersede`, `fail`, and `adopt`. The identity of a human is written with the prefix `human:`. An identity without that prefix is not a human, and an action that requires a human MUST be rejected when the identity that performs it does not carry the prefix. The prefix is part of the claim: at A0 it is self-declared, and at A1 or A2 it is as well verified as the claim is. See AE-128, AE-133.

An approval binds the exact content that is approved, and that content is identified by its content hash (Section 25.2). For the approval of the specification, the approved content is the specification of the change. For the approval of gate definitions, it is the gate definitions (Section 24.1). For the sign-off of a gate and for an override, it is the gate definitions together with the identifier of the gate or of the fail condition. The history records, for every action, the identity and the verified level, and for an approval also the content hash that was approved. The approval of the specification is stale while the content hash of the current specification differs from the content hash that was approved, and the stale specification approval gate of Section 23.7 is active in that case. See AE-125, AE-126, AE-136.

The statement of a signed approval is built by the implementation from the action that it is about to perform. A statement that the participant supplies is not accepted, so that what is signed cannot differ from what is verified. The statement is text in lines, each ended by a line feed, and the bytes that are signed are its UTF-8 encoding. It contains, in this order:

1. a first line that holds the format identifier and the format version of the statement;
2. the operation, which is the name of the action;
3. the change, which is the identifier of the change;
4. the version, which is the number of entries that the history of the change holds when the statement is built (Section 24.4), so that the statement names the position in the history at which the action will be recorded;
5. the identity of the signer;
6. the details of the action, one line for each detail field, in ascending order of the field names compared as Section 24 states. The details of an approval include its target and the content hash of the content that is approved.

Each line after the first has the form `name: value`, and each value is encoded as JSON, in the way that Section 25.1 encodes a value, so that no value can contain a line feed and no value can inject a line of its own. A statement with a format identifier or a format version that the verifier does not support is not verified. The specification fixes that the format identifier and the format version are part of the statement, and it does not fix their spelling. An illustration, not normative:

```text
<format identifier> <format version>
operation: "approve"
change: "c-1"
version: 4
identity: "human:ada"
content_hash: "sha256:<64 hexadecimal digits>"
target: "spec"
```

A signature made for a statement is valid only for that statement. A signature made at another position of the history, for another change, for another operation, or over other content is not valid for the statement that the implementation builds now. See AE-129, AE-136.

A private key that is not protected by a passphrase, or by an equivalent protection, lets every process and every participant that can read the key sign as its holder. An implementation that creates signatures SHOULD refuse such a key unless a human explicitly allows its use. The signers file lists public keys only, and a participant that can write the signers file can list its own key for any identity. See AE-134.

No level proves that a human is present. An agent that is able to use a human's credentials can act as that human, and this holds at every level. At A0, any participant can write any identity. At A1, the platform sees the account and not the participant that operates it, so an agent that holds the login of the account can approve as the account holder; and a platform commonly does not let the author of a review object approve it, so A1 does not serve a participant who works alone. At A2, an agent that can read an unprotected private key, or that can use a key which a running process holds, can sign as the signer. The levels raise the cost of a false claim, and they do not exclude it. See AE-134, AE-135.

**AE-125 — Reject an A0 claim where A2 is required**

- Covers: Section 24.3

Given an `open` `core` change in a project whose configuration sets the minimum level A2 for the approval of the specification  
When a participant that claims the identity `human:ada` approves the target `spec` and carries no signature  
Then the verified level is A0, which is below the required level A2, the approval is rejected with `changed` false, and no approval is recorded

**AE-126 — Accept a valid signature at A2**

- Covers: Section 24.3

Given the same change and configuration, and a signers file outside the repository that lists a key for `human:ada`  
When the approval of the target `spec` carries a valid signature by that key over the statement that the implementation builds  
Then the approval is recorded with the verified level A2 and with the content hash of the specification that was approved

**AE-127 — A forged signature fails closed**

- Covers: Section 24.3

Given the same change and configuration, and a signers file that lists a key for `human:ada`  
When the approval of the target `spec` carries a signature made with a key that is not listed for `human:ada`  
Then the claim is A0, the approval is rejected, and no approval is recorded

**AE-128 — Reject a human-only action under an identity that is not marked as human**

- Covers: Section 24.3

Given an `active` `core` change  
When the participant `agent:builder` performs the `cancel` action  
Then the action is rejected, because the identity does not carry the prefix `human:`, and the change remains `active`

**AE-129 — A signature replayed at another history position fails**

- Covers: Section 24.3

Given a signature that is valid for an approval of `spec` whose statement names the version 4, and a `core` change whose history now holds five entries, in a project whose configuration sets the minimum level A2  
When the approval is presented again with that signature  
Then the statement that the implementation builds names the version 5, the signature is not valid for it, the claim is A0, and the approval is rejected

**AE-130 — An unsigned claim is A0, not malformed**

- Covers: Section 24.3

Given an `open` `core` change in a project whose configuration sets no minimum level for approvals  
When the participant `human:ada` approves the target `spec` with no signature and no review  
Then the approval is not rejected as malformed, and it is recorded with the verified level A0

**AE-131 — The required level is the higher of the gate minimum and the configured minimum**

- Covers: Section 24.3

Given a `sign-off` done gate `legal-ok` that states the minimum level A1, and a project configuration that sets the minimum level A2 for the sign-off of gates  
When `human:ada` signs off `legal-ok` with a claim at A1, and later with a claim at A2  
Then the first sign-off is rejected, because the required level is A2, and the second sign-off is recorded

**AE-132 — A compliance profile alone sets no minimum level**

- Covers: Section 24.3

Given a change whose compliance profile is `regulated`, whose gates state no minimum level, and whose project configuration sets none  
When `human:ada` approves the target `spec` with a claim at A0  
Then the approval is recorded, because the required level is A0

**AE-133 — A1 requires that the approved files have no uncommitted change**

- Covers: Section 24.3

Given a project whose configuration sets the minimum level A1 for the approval of the specification, a platform account mapped to `human:ada` whose latest review approves the checked-out revision, and an uncommitted change in the specification of the change  
When `human:ada` approves the target `spec`  
Then the claim is A0, because an approved file has an uncommitted change, and the approval is rejected

**AE-134 — An agent with a human's key can sign as that human**

- Covers: Section 24.3

Given a private key of `human:ada` without a passphrase that an AI agent can read, a signers file that lists the matching key for `human:ada`, and a configuration that sets the minimum level A2  
When the AI agent signs an approval of the target `spec` as `human:ada`  
Then the approval is valid and is recorded at A2, and this specification offers no detection of it, because an agent that is able to use a human's credentials can act as that human

**AE-135 — A1 does not tell the account holder from an agent**

- Covers: Section 24.3

Given an AI agent that holds the login of the platform account mapped to `human:ada`, and a review by that account that approves the checked-out revision  
When the agent claims the identity `human:ada` for an approval  
Then the claim is verified at A1, and the verification does not show that the participant is not an agent

**AE-136 — A signature over other content fails**

- Covers: Section 24.3

Given a signature by a listed key over the statement for an approval of `spec` that names the content hash of an earlier version of the specification, and a specification that was edited since  
When the approval is presented with that signature  
Then the statement that the implementation builds names the content hash of the current specification, the signature is not valid for it, and the claim is A0

### 24.4 History Consistency and Completeness

The history of a change is an append-only list of entries, and the state of the change is read from it (Section 25.1). Every entry has four fields:

- `n`: the position of the entry, which starts at 1;
- `prev`: the hash of the entry before it. For the first entry, `prev` is the prefix `sha256:` followed by 64 digits 0;
- `body`: the content that the entry records, including the result of the action and the state of the change after it;
- `hash`: the hash of the entry, which is the hash of the canonical form (Section 25.1) of an object that holds `prev` and `body`. It is written as the prefix `sha256:` followed by the 64 lowercase hexadecimal digits of the SHA-256 digest.

The state of the change is the state that the last entry records. The state document has no other field that holds the state, so that there is no field to edit by hand in order to change it.

A history is consistent when it has at least one entry, the positions run from 1 without a gap, the `prev` of each entry equals the `hash` of the entry before it, and the stored `hash` of each entry equals the hash that is computed again from its `prev` and `body`. A history without an entry is not consistent. An implementation MUST verify the consistency of the history before it acts on a change, and MUST NOT act on a history that is not consistent. See AE-137, AE-141, AE-143.

Consistency is not completeness. Consistency says that the entries which are present form an unbroken chain. It does not say that no entry is missing: a history from which the last entries were removed is still consistent, because nothing in a chain refers forward to the entries after it. Completeness says that no entry is missing, in particular none at the end of the history, and a chain alone cannot establish it. See AE-139.

An anchor records the position and the hash of the latest entry of a history. It is kept at a location that is outside the working tree of the project and is not part of the history, and it is written only after the append of that entry has succeeded. After every successful append the anchor is advanced to the new latest entry. Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor or an equivalent mechanism, and an implementation MUST NOT act on a change whose history has none until a human adopts the history. An equivalent mechanism gives the verifier a record of the latest position and hash that is independent of the history, is written only after the append has succeeded, supports the three checks below, and cannot be replaced. Where no configuration requires approvals at the level A2, an implementation MAY keep an anchor. See AE-140, AE-142.

With an anchor, the verifier compares the history with it:

- a history with fewer entries than the position of the anchor is truncated, or it was rolled back to an earlier state;
- a history whose entry at the position of the anchor has a hash that differs from the hash of the anchor was rewritten;
- otherwise the history agrees with the anchor. Entries after the position of the anchor are the entries appended since the anchor was last advanced.

An implementation MUST NOT act on a history that is truncated or rewritten, and its message MUST say which of the two it found. See AE-138, AE-139.

An existing anchor MUST NOT be replaced. It is only advanced, after a successful append, to the position and the hash of a later entry of the same chain. No action sets an anchor to an earlier position or to a different hash. See AE-144.

The `adopt` action creates the anchor from the history as it is, at the position and the hash of its latest entry (Section 23.4). It MUST be performed by a human at the level that Section 24.3 requires for `adopt`, and it is rejected when an anchor exists and when the history is not consistent. A human who adopts a history takes responsibility for its completeness at that moment: adoption cannot show whether entries were lost before it. See AE-140, AE-146.

An anchor is only as strong as the location that holds it. An actor that can write both the history and the anchor can rewrite both, and every check of this section then passes. The anchor protects against an actor that can write the history and cannot write the anchor, and against accident. It does not protect against an actor that can write both. See AE-145.

**AE-137 — Accept a consistent history that agrees with its anchor**

- Covers: Section 24.4

Given a history of four entries with positions 1 to 4, each `prev` equal to the hash of the entry before it, each stored hash equal to the hash computed again, and an anchor at position 4 with the hash of entry 4  
When any action on the change is requested  
Then the history is consistent and agrees with the anchor, and the implementation acts on the change

**AE-138 — A rewritten entry is detected through the anchor**

- Covers: Section 24.4

Given an anchor at position 5 with the hash of entry 5, and a history in which the body of entry 5 was edited and the hashes of entry 5 were computed again, so that the chain is consistent  
When any action on the change is requested  
Then the hash of entry 5 differs from the hash of the anchor, the history is found rewritten, and the implementation does not act

**AE-139 — A truncated history is consistent and is detected through the anchor**

- Covers: Section 24.4

Given an anchor at position 5, and a history from which entries 4 and 5 were removed, so that three entries remain  
When any action on the change is requested  
Then the chain of three entries is consistent, the history has fewer entries than the position of the anchor, it is found truncated or rolled back, and the implementation does not act

**AE-140 — A history without an anchor is refused until a human adopts it**

- Covers: Section 24.4

Given a project whose configuration requires approvals at the level A2, and a consistent history with no anchor  
When any action other than `adopt` is requested, and later a human performs `adopt` at the level A2  
Then the first request is refused, and after the `adopt` action the anchor holds the position and the hash of the latest entry and the actions are accepted

**AE-141 — A history without an entry is not consistent**

- Covers: Section 24.4

Given a state document whose history has no entry  
When any action on the change is requested  
Then the history is not consistent, and the implementation does not act

**AE-142 — An equivalent mechanism meets the requirement for an anchor**

- Covers: Section 24.4

Given a project whose configuration requires approvals at the level A2, and no anchor, but an independent append-only record outside the working tree that holds the latest position and hash and is written only after each successful append  
When the history is verified, once intact and once with its last entry removed  
Then the requirement for an anchor is met, the intact history agrees with the record, and the shortened history is found truncated

**AE-143 — An edited entry that keeps its stored hash breaks the chain**

- Covers: Section 24.4

Given a history of three entries in which the body of entry 2 was edited and its stored hash was not changed  
When the history is verified  
Then the hash computed again for entry 2 differs from its stored hash, the history is not consistent, and the implementation does not act

**AE-144 — An existing anchor is not replaced**

- Covers: Section 24.4

Given an anchor at position 5  
When an operation sets the anchor to position 3, or to a different hash at position 5  
Then the operation is rejected, and the anchor does not change

**AE-145 — An actor that can write both history and anchor can rewrite both**

- Covers: Section 24.4

Given an actor that can write the history and the anchor, that rewrote entries 3 to 5, computed their hashes again, and set the anchor to the new latest entry  
When the history is verified  
Then the history is consistent and agrees with the anchor, and no check of this section detects the rewrite

**AE-146 — Reject the adoption of an inconsistent history**

- Covers: Section 24.4

Given a history whose entry 2 was edited without a change of its stored hash, and no anchor  
When a human performs the `adopt` action  
Then the action is rejected, and no anchor is created

### 24.5 Scope and Isolation

The scope of a change is a list of path patterns, the allowed path list. A change MAY touch a path only when at least one pattern of the list matches it. In `core`, the allowed path list is the field `scope.allow` of the change definition (Section 23.1). In `full`, it is the list of path patterns that the Scope of the change specification states (Section 16.1), and a change specification that states no allowed path list has a scope that cannot be measured. The allowed path list is part of the gate definitions and is fixed with them (Section 24.1).

A path is written relative to the root of the repository, with the character `/` as the separator. A pattern is written in the same way and is compared with a path as Section 24 states, so that letter case matters and nothing is normalized. A pattern without a wildcard names one path, and a pattern that ends with `/` names every path below that directory. In a pattern, `*` matches any sequence of characters other than `/` inside one path segment, and a segment that is exactly `**` matches any number of path segments, including none. No other wildcard exists. A pattern that is empty, that begins with `/`, or that has a path segment `..` is invalid and MUST be rejected when the gate definitions are approved. See AE-156.

The base revision is the revision from which the change started. It is recorded when the change starts: in `core`, when the `start` action succeeds (Section 23.4); in `full`, when the first phase of the change begins. A change MUST NOT start when its base revision cannot be recorded: the start is rejected, and nothing is written. See AE-153.

The paths changed since the base revision are the paths whose content differs from the base revision according to version control, whether the difference is committed, staged, or unstaged, and the files that version control does not track and has not been told to ignore. A path changed since the base revision that no pattern of the allowed path list matches is a scope violation. A scope violation is a hard failure (Section 24.7): the change is closed as failed without human action, and the record names the paths outside the scope. See AE-147, AE-148, AE-149.

The record files of the change itself are exempt from the measurement. In `core` they are the change definition, the specification, and the state document (Section 23.1). In `full` they are the specification and the state file or inline record of the change (Sections 16.1 and 4.3). Other means detect their alteration: the hash of the gate definitions (Section 24.1), the approval of the specification (Section 24.3), and the chain of the history (Section 24.4). Every other file in the change directory is measured. See AE-155.

Before the change has started there is no base revision, and the scope is not evaluated: the record shows `not_applicable` (Section 24.2). After the change has started, a scope that cannot be measured is `not_evaluable` (Section 24.2). That is the case when version control is unavailable, when no base revision was recorded, and when the allowed path list is absent. It is never recorded as `satisfied`, and it is never recorded as a scope violation. See AE-154, AE-157.

An allowed path list that is present and empty allows no path: every path changed since the base revision is a scope violation. When no path has changed, the change is in scope, whatever the list holds. See AE-151.

A file that version control is told to ignore is invisible to the measurement. A change can create or alter an ignored file without a scope violation, so the allowed path list does not limit what happens in ignored locations. The consequence for the code that gate commands run is stated in Section 24.10. See AE-150.

Work that is uncommitted when the change starts and that does not belong to the change is a changed path like any other. The measurement counts it, and it is a scope violation when no pattern matches it. A change therefore MUST run isolated: in a working copy that is separate from other work and whose content at the start equals the base revision, apart from the record files of the change. An implementation SHOULD warn when it finds other uncommitted work at the start, and it MUST NOT exclude that work from the measurement. See AE-152.

**AE-147 — A changed path that a pattern matches is in scope**

- Covers: Section 24.5

Given an `active` `core` change whose `scope.allow` is `lib/**`  
When the file `lib/net/client.py` is changed and the `close` action evaluates the gates  
Then the path is in scope, and the scope violation gate is not active

**AE-148 — A path outside the scope is a hard failure**

- Covers: Section 24.5

Given an `active` `core` change whose `scope.allow` is `lib/**`, and the file `docs/guide.md` is committed after the base revision  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed` without human action, and the record names `docs/guide.md` as outside the scope

**AE-149 — An untracked file that is not ignored is counted**

- Covers: Section 24.5

Given an `active` `core` change whose `scope.allow` is `lib/**`, and the new file `tools/run.sh` that version control does not track and has not been told to ignore  
When the `close` action evaluates the gates  
Then `tools/run.sh` is a changed path outside the scope, and the change is closed as failed

**AE-150 — An ignored file is invisible**

- Covers: Section 24.5

Given an `active` `core` change whose `scope.allow` is `lib/**`, a directory `.cache/` that version control is told to ignore, and a new file `.cache/tool.py` created by the change  
When the `close` action evaluates the gates  
Then `.cache/tool.py` is not seen by the measurement, and no scope violation is found

**AE-151 — An empty allowed path list allows no path**

- Covers: Section 24.5

Given two `active` `core` changes whose `scope.allow` is an empty list, and the file `lib/a.py` changed since the base revision in the first change and no path changed in the second  
When the `close` action evaluates the gates of each change  
Then the first change has a scope violation and is closed as failed, and the second change is in scope

**AE-152 — Unrelated uncommitted work counts as an outside edit**

- Covers: Section 24.5

Given a working copy in which the file `notes/todo.txt` has an uncommitted edit that does not belong to the change, and a change whose `scope.allow` is `lib/**` that starts in that working copy  
When the `close` action evaluates the gates  
Then `notes/todo.txt` is a changed path outside the scope, and the change is closed as failed, which is why the change runs in an isolated working copy

**AE-153 — Refuse the start when the base revision cannot be recorded**

- Covers: Section 24.5

Given an `open` `core` change, and version control that does not provide a revision to record  
When the `start` action is requested  
Then the action is rejected, nothing is written, the change remains `open`, and no base revision is recorded

**AE-154 — A scope that cannot be measured is not evaluable after the start**

- Covers: Section 24.5

Given an `active` `core` change whose record holds no base revision, in a project where version control is available  
When the `close` action evaluates the gates  
Then the result of the scope gate is `not_evaluable`, no scope violation is recorded, and the change waits with a wait record of kind `external`

**AE-155 — The record files of the change are exempt**

- Covers: Section 24.5

Given an `active` `core` change `c-1` whose `scope.allow` is `lib/**`, and the files `specs/c-1/spec.md` and `specs/c-1/state.json` changed since the base revision, and the new file `specs/c-1/notes.md`  
When the `close` action evaluates the gates  
Then `spec.md` and `state.json` are not measured, and `specs/c-1/notes.md` is a changed path outside the scope

**AE-156 — A wildcard does not cross a path separator, and an invalid pattern is rejected**

- Covers: Section 24.5

Given a change definition whose `scope.allow` is `lib/*.py`, and a second change definition whose `scope.allow` is `../lib/**`  
When the file `lib/sub/a.py` is changed in the first change, and the gate definitions of the second change are approved  
Then `lib/sub/a.py` is outside the scope of the first change, because `*` does not match `/`, and the approval of the second change is rejected, because the pattern has a segment `..`

**AE-157 — The scope is not evaluated before the change has started**

- Covers: Section 24.5

Given an `open` `core` change with no base revision  
When the `start` action is requested and succeeds  
Then the scope gate is recorded as `not_applicable` for that evaluation, and the start is not stopped by it

### 24.6 Known-Failure Baselines

A check-command gate (Section 24.2) MAY carry a baseline: the list of failure identifiers that were already failing before the change started and that the change is not required to fix. A baseline is valid only on a check-command gate. A baseline on any other gate is invalid and MUST be rejected when the gate definitions are approved. The baseline is part of the gate definition and is fixed with it (Section 24.1): changing it requires a new approval by a human, so that a baseline cannot be used to hide a new failure. See AE-94, AE-96.

A failure identifier is a string that identifies one failure in a way that is stable across runs, for example the identifier of a failing test. The gate declares how failure identifiers are extracted from the output of its command (Section 24.2). Failure identifiers are compared as Section 24 states. The extracted identifiers form a set: an identifier that appears more than once counts once. See AE-93.

When the command of a gate with a baseline ends with an exit status that the exit map maps to `satisfied`, the result is `satisfied`. When it ends with an exit status that the exit map maps to `not_satisfied`, the implementation extracts the failure identifiers from the output and compares them with the baseline:

- when every extracted failure is on the baseline, the result is `satisfied`. This includes the case where the extracted failures are exactly the failures of the baseline;
- when at least one extracted failure is not on the baseline, the result is `not_satisfied`. The record names up to three of the new failures, in ascending order of their code points, and the number of new failures;
- when no failure identifier can be extracted, or when the output cannot be read, the result is `not_evaluable`, because the failures cannot be compared.

An empty baseline is valid. With an empty baseline every extracted failure is a new failure, and the result is `satisfied` only when no failure occurred. A baseline entry that did not fail in the evaluation is not a failure and does not change the result. The record notes the number of such entries. See AE-87, AE-88, AE-89, AE-90, AE-91, AE-92, AE-95.

**AE-87 — All failures are on the baseline**

- Covers: Section 24.6

Given a check-command gate whose baseline lists the failures `t1` and `t2`, and whose command ends with an exit status that the exit map maps to `not_satisfied`  
When the output of the command names the failures `t1` and `t2`  
Then the result is `satisfied`

**AE-88 — A new failure is named**

- Covers: Section 24.6

Given a check-command gate whose baseline lists the failure `t1`, and whose command ends with an exit status that the exit map maps to `not_satisfied`  
When the output of the command names the failures `t1` and `t9`  
Then the result is `not_satisfied`, and the record names `t9` and states that there is one new failure

**AE-89 — Unreadable failures are not evaluable**

- Covers: Section 24.6

Given a check-command gate whose baseline lists the failure `t1`, and whose command ends with an exit status that the exit map maps to `not_satisfied`  
When the output of the command contains no failure identifier that can be extracted  
Then the result is `not_evaluable`, not `satisfied` and not `not_satisfied`

**AE-90 — Equal sets satisfy the gate**

- Covers: Section 24.6

Given a check-command gate whose baseline lists the failures `t1`, `t2`, and `t3`, and whose command ends with an exit status that the exit map maps to `not_satisfied`  
When the output of the command names exactly `t3`, `t1`, and `t2`  
Then the result is `satisfied`, because the extracted failures and the baseline are the same set

**AE-91 — An empty baseline passes only without a failure**

- Covers: Section 24.6

Given a check-command gate whose baseline is empty  
When one evaluation ends with an exit status that the exit map maps to `satisfied`, and a second evaluation ends with an exit status that the exit map maps to `not_satisfied` and names the failure `t1`  
Then the first result is `satisfied`, and the second result is `not_satisfied` with one new failure `t1`

**AE-92 — Name at most three new failures in code point order**

- Covers: Section 24.6

Given a check-command gate with an empty baseline, whose command ends with an exit status that the exit map maps to `not_satisfied`  
When the output of the command names the failures `t5`, `t2`, `t4`, `t1`, and `t3`  
Then the result is `not_satisfied`, and the record names `t1`, `t2`, and `t3` in that order and states that there are five new failures

**AE-93 — Failure identifiers are compared as code point sequences**

- Covers: Section 24.6

Given a check-command gate whose baseline lists the failure `café` written with the single code point U+00E9  
When the output of a failing command names the failure `café` written as `cafe` followed by the code point U+0301  
Then the identifiers are different, the failure is a new failure, and the result is `not_satisfied`

**AE-94 — Reject a baseline on a gate that is not a check-command gate**

- Covers: Section 24.6

Given a change definition with a baseline on a wait gate  
When the gate definitions are approved  
Then the approval is rejected, because a baseline is valid only on a check-command gate

**AE-95 — A baseline entry that no longer fails is noted**

- Covers: Section 24.6

Given a check-command gate whose baseline lists the failures `t1` and `t2`, and whose command ends with an exit status that the exit map maps to `not_satisfied`  
When the output of the command names only `t1`  
Then the result is `satisfied`, and the record notes that one baseline entry did not fail

**AE-96 — A changed baseline needs a new approval**

- Covers: Section 24.6

Given a `core` change whose gate definitions were approved with a baseline that lists the failure `t1`, and the entry `t9` was added to the baseline after the approval  
When the `close` action is requested  
Then the result is `rejected` with the issue code `gates-changed`, and the baseline with `t9` has no effect until a human approves the gate definitions again

### 24.7 Hard and Soft Failure

Every fail condition has a severity, which is `hard` or `soft`, written in exact lowercase. A fail condition without a severity, or with any other value, is invalid and MUST be rejected when the gate definitions are approved. In `core`, the severity is the field `severity` of a fail gate (Section 23.3). In `full`, every fail rule states its severity (Section 12.2). A retry limit (Section 24.2) is a fail condition of the severity `soft`, and a retry limit that declares the severity `hard` is invalid and MUST be rejected. See AE-97, AE-108, AE-110.

A hard failure ends the change as failed without any human action. When an action that evaluates gates finds a fail condition of the severity `hard` active, the action MUST close the change as failed in the same state mutation: in `core`, the state `closed` with the outcome `failed`; in `full`, the `closed` phase with the status `failed`. This decision comes before every other decision of Section 24.2, and the action that makes it answers `success`. An active hard failure also turns `cancel` and `supersede` into a close as failed (Sections 8.4 and 23.4). See AE-98.

A soft failure pauses the change for a human. When an action that evaluates gates finds a fail condition of the severity `soft` active and no hard failure, the action MUST NOT close the change. The change waits: in `core`, in the state `waiting` with a wait record of kind `fail-gate` (Section 23.5); in `full`, with the status `waiting` and a wait state of the category `WAIT_DECISION` (Section 11.1), whose resume condition is that a human has recorded an override. The wait ends by a human disposition (Section 24.3), which is one of two:

- the human closes the change as failed with the `fail` action and a reason (Sections 8.3 and 23.4);
- the human records an override of the soft failure.

The `fail` action is valid only while a soft failure awaits disposition. See AE-99, AE-100, AE-101.

An override is recorded by a human as an approval with the target `override` (Section 23.4). It MUST name the soft fail condition that it applies to, MUST give a reason, and MUST give a number N of further attempts. N MUST be an integer greater than or equal to 1. This specification defines no default for N: a request that gives no number, a number below 1, or a number that is not an integer MUST be rejected, and so MUST a request that gives no reason. An override is valid only for a fail condition of the severity `soft` that awaits disposition. An override for any other fail condition MUST be rejected. See AE-104, AE-105, AE-106, AE-107, AE-109.

An attempt is one evaluation by the action that completes the change (in `core`, `close`; in `full`, `complete`) that is made while the override is in force. An evaluation that ends in the wait of Section 24.2 for a gate that cannot be evaluated is not an attempt. While the override is in force, the soft failure that it covers does not pause the change. The N-th attempt is allowed, and the evaluation after it pauses the change again, as a soft failure does. See AE-102.

An override is bound to the approved hash of the gate definitions (Section 24.1). It lapses when its N attempts are used up and when the gate definitions are amended. A lapsed override has no effect, and a soft failure that is still active pauses the change again. See AE-103.

**AE-97 — Reject a fail rule without a severity**

- Covers: Section 24.7

Given a `full` change whose fail rule `F-02` states no severity  
When the gate definitions are approved  
Then the approval is rejected, because every fail condition has a severity, and no approved hash is recorded

**AE-98 — A hard failure closes the change as failed without human action**

- Covers: Section 24.7

Given an `active` `core` change with a fail gate of the severity `hard` that is active  
When the `close` action is requested  
Then the result is `success`, the state is `closed`, the outcome is `failed`, and no human action was needed

**AE-99 — A soft failure pauses the change**

- Covers: Section 24.7

Given an `active` `core` change with a fail gate of the severity `soft` that is active and no hard failure  
When the `close` action is requested  
Then the change does not close, and it is `waiting` with a wait record of kind `fail-gate`

**AE-100 — A human closes a paused change as failed**

- Covers: Section 24.7

Given a `waiting` `core` change with a wait record of kind `fail-gate`  
When a human performs the `fail` action with the reason `retry limit reached`  
Then the state is `closed` and the outcome is `failed`

**AE-101 — A retry limit pauses the change and does not fail it**

- Covers: Section 24.7

Given a retry limit of three for `tests-pass`, a history with three `not_satisfied` results of `tests-pass`, and an `active` `core` change  
When the `close` action is requested  
Then the change is `waiting` with a wait record of kind `fail-gate`, and it is not `closed`

**AE-102 — An override allows exactly the granted attempts**

- Covers: Section 24.7

Given an `active` `core` change with an active soft failure and an override of that soft failure with two further attempts  
When the `close` action is requested three times and none of the evaluations ends in a wait for a gate that cannot be evaluated  
Then the first two evaluations are not paused by the soft failure, and the third evaluation pauses the change again with a wait record of kind `fail-gate`

**AE-103 — An override lapses when the gate definitions are amended**

- Covers: Section 24.7

Given a `core` change with an override that has one attempt left, and a human amended the gate definitions by approving them again  
When the `close` action is requested and the soft failure is still active  
Then the override has no effect, and the change is `waiting` with a wait record of kind `fail-gate`

**AE-104 — Reject an override without a reason**

- Covers: Section 24.7

Given a `waiting` `core` change with a wait record of kind `fail-gate`  
When a human approves the target `override` with two further attempts and no reason  
Then the approval is rejected, and no override is recorded

**AE-105 — Reject an override with zero attempts**

- Covers: Section 24.7

Given a `waiting` `core` change with a wait record of kind `fail-gate`  
When a human approves the target `override` with a reason and zero further attempts  
Then the approval is rejected, because the number of attempts is at least 1, and no override is recorded

**AE-106 — Reject an override with a number that is not an integer**

- Covers: Section 24.7

Given a `waiting` `core` change with a wait record of kind `fail-gate`  
When a human approves the target `override` with a reason and 2.5 further attempts  
Then the approval is rejected, and no override is recorded

**AE-107 — Reject an override for a hard failure**

- Covers: Section 24.7

Given an `active` `core` change with a fail gate of the severity `hard` that is active  
When a human approves the target `override` for that fail gate with a reason and two further attempts  
Then the approval is rejected, because an override is valid only for a soft failure, and the next evaluating action closes the change as failed

**AE-108 — Reject a retry limit with the severity hard**

- Covers: Section 24.7

Given gate definitions with a retry limit of three for `tests-pass` and the severity `hard`  
When the gate definitions are approved  
Then the approval is rejected, because a retry limit has the severity `soft`

**AE-109 — Reject an override that gives no number of attempts**

- Covers: Section 24.7

Given a `waiting` `core` change with a wait record of kind `fail-gate`  
When a human approves the target `override` with a reason and no number of attempts  
Then the approval is rejected, because no default number exists, and no override is recorded

**AE-110 — Reject a severity that is not exact lowercase**

- Covers: Section 24.7

Given a change definition whose fail gate `no-secrets` has the severity `Hard`  
When the gate definitions are approved  
Then the approval is rejected, because only the exact lowercase values `hard` and `soft` are severities

### 24.8 Open Questions as State

An open question is part of the state of the change and is recorded in its history. It is not prose in a document. A question has these fields:

- `id`: the letter `Q` followed by a decimal number that starts at 1, assigned by the implementation in the order of creation;
- `text`: the text of the question;
- `owner`: the participant that answers the question, which is the owner of the change unless the question names another;
- `asker`: the participant that asked the question;
- `options`: absent for a free-text question, and otherwise a list of at least two distinct options, which is the list of a structured question;
- `answer`: absent while the question is unanswered;
- `answerer`: the participant that gave the answer.

In `core`, the `ask` action records a question without pausing the change, and the `wait` action that gives a question records it and pauses the change with a wait record of kind `question` (Sections 23.4 and 23.5). In `full`, a question is recorded in the state file, or in the inline record where no state file is persisted (Section 4.3), and the answer is recorded as a human decision (Section 22.1). A wait that a question causes has the category `WAIT_USER_INPUT` (Section 11.1).

Two options are distinct when they differ as sequences of code points (Section 24). A structured question with fewer than two distinct options MUST be rejected, and so MUST a structured question whose list repeats an option. Question identifiers are compared in the same way, so that `Q1` and `q1` are different identifiers. See AE-177, AE-181.

Only the owner of a question answers it. An answer from another participant MUST be rejected. When the owner is a human, the answer MUST be given by a human, at the level that Section 24.3 requires for an answer. The answer to a structured question MUST be exactly one of its options, and any other value MUST be rejected. The answer to a free-text question MUST be rejected when it is empty or consists only of spaces, tabs, and line breaks. A question that is already answered MUST NOT be answered again: a second answer MUST be rejected, and the first answer stays. An answer does not resume a waiting change. See AE-173, AE-174, AE-175, AE-176, AE-178, AE-179, AE-181.

An unanswered question blocks two things. The approval of the specification MUST be rejected with the issue code `open-questions`, whose message names the unanswered questions, and no approval is recorded. The closure of the change is blocked: in `core`, the unanswered question gate of Section 23.7 is a wait gate that is active, and the `close` action answers `blocked`; in `full`, a Definition of Wait condition is active (Section 11), and the actions `complete` and `resume` answer `blocked` (Section 8.3). See AE-171, AE-172, AE-182.

An open question is not accepted by silence, by omission, or by a statement outside the history. A participant who wants to proceed without resolving a question records an answer to it, given by the owner of the question; the answer can be an option such as `accept` of a structured question. The acceptance of an open question is therefore an answer, and a statement of acceptance that is not recorded as an answer leaves the question unanswered. See AE-180.

The section Open Questions of the change specification (Section 16.1) is a view of the questions that are recorded as state. Where the view and the recorded state differ, the recorded state governs.

**AE-171 — An unanswered question blocks the approval of the specification**

- Covers: Section 24.8

Given an `open` `core` change with the unanswered question Q1  
When a human approves the target `spec`  
Then the result is `rejected` with the issue code `open-questions` that names Q1, and no approval is recorded

**AE-172 — An unanswered question blocks closure**

- Covers: Section 24.8

Given an `active` `core` change with every done gate satisfied and the unanswered question Q1  
When the `close` action is requested  
Then the result is `blocked` with `changed` true, the issues name the unanswered question gate, and the change remains `active`

**AE-173 — A structured answer is recorded**

- Covers: Section 24.8

Given an `active` `core` change with the unanswered structured question Q1 whose options are `keep` and `drop` and whose owner is `human:ada`  
When `human:ada` answers Q1 with `drop`  
Then Q1 is recorded as answered with `drop` and with the answerer `human:ada`, and the state of the change does not change

**AE-174 — Reject an answer that is not one of the options**

- Covers: Section 24.8

Given the unanswered structured question Q1 whose options are `keep` and `drop`  
When its owner answers Q1 with `Keep`  
Then the answer is rejected, because only the exact option `keep` or `drop` is an answer, and Q1 remains unanswered

**AE-175 — Reject an empty free-text answer**

- Covers: Section 24.8

Given the unanswered free-text question Q2  
When its owner answers Q2 with an empty text, and later with a text of three spaces  
Then both answers are rejected, and Q2 remains unanswered

**AE-176 — Reject a repeated answer**

- Covers: Section 24.8

Given the question Q1 that is answered with `keep`  
When its owner answers Q1 with `keep` again, and later with `drop`  
Then both answers are rejected, and Q1 keeps the answer `keep`

**AE-177 — Options are distinct as code point sequences**

- Covers: Section 24.8

Given two structured questions, the first with the options `keep` and `keep`, and the second with the option `café` written with the single code point U+00E9 and the option `café` written as `cafe` followed by the code point U+0301  
When the `ask` action records each of them  
Then the first question is rejected, because it has only one distinct option, and the second question is recorded, because its two options are distinct

**AE-178 — Only the owner answers**

- Covers: Section 24.8

Given an unanswered question Q1 whose owner is `human:bo`  
When `human:ada` answers Q1  
Then the answer is rejected, because `human:ada` is not the owner, and Q1 remains unanswered

**AE-179 — A human owner needs a human answer**

- Covers: Section 24.8

Given an unanswered question Q1 whose owner is `human:ada`  
When the participant `agent:builder` answers Q1 in the name of the owner  
Then the answer is rejected, because the owner is a human and the answerer is not, and Q1 remains unanswered

**AE-180 — Acceptance is an answer**

- Covers: Section 24.8

Given an `open` `core` change with the unanswered structured question Q1 whose options are `accept` and `resolve`, and a note in the specification that says Q1 is accepted  
When a human approves the target `spec`, and later the owner of Q1 answers Q1 with `accept` and a human approves the target `spec` again  
Then the first approval is rejected with the issue code `open-questions`, and the second approval is recorded

**AE-181 — Question identifiers are compared as code point sequences**

- Covers: Section 24.8

Given an unanswered question Q1  
When its owner answers the question `q1`  
Then the answer is rejected, because no question with the identifier `q1` exists, and Q1 remains unanswered

**AE-182 — An unanswered question blocks a `full` change**

- Covers: Section 24.8

Given a `full` change in the specify phase with the status `active` and the unanswered question Q1 in its state file  
When the `complete` action is requested  
Then the result is `blocked` with `changed` true, the issues name Q1, and the phase and status do not change

### 24.9 Executable Evidence

The evidence for a requirement is executable and is bound to that requirement. An evidence command is a check command as Section 24.2 defines it: an argument list, an exit map, and OPTIONALLY a time limit. It is run as Section 24.10 states. A requirement lists the evidence commands that are bound to it: in `core`, in the field `requirements` of the change definition (Section 23.1); in `full`, in the change specification (Section 16.1), where the Evidence cell of the requirement coverage table (Section 16.4) names them.

The evidence of a change is complete only when all of these hold:

- the change declares at least one requirement;
- every requirement has at least one evidence command that is bound to it;
- when the evidence commands are run at closure, each of them has the result `satisfied`.

Closure is the evaluation that decides whether the change completes: in `core`, the `close` action (Section 23.4); in `full`, the evaluation of Verify-Done (Section 10.7) and of the completion criteria (Section 20). In `core`, the incomplete evidence gate (Section 23.7) is satisfied only when the evidence is complete. See AE-163.

A change with no requirements has no complete evidence: its evidence is not complete, and the record states that no requirements are declared. A requirement without an evidence command makes the evidence not complete, and the record names the requirement. An evidence command with the result `not_satisfied` makes the evidence not complete. An evidence command that cannot run has the result `not_evaluable` (Section 24.2): that is not a failure, it does not count toward a retry limit, the change waits as Section 24.2 states, and the evidence is not complete until the command has run and is `satisfied`. See AE-164, AE-165, AE-166, AE-167.

The other records that Section 15 names, for example reviews, logs, screenshots, measurements, and references to commits, MAY be kept. They supplement the executable check and never replace it. A requirement whose only evidence is such a record has no evidence command, and its evidence is not complete. See AE-168, AE-170.

The requirement identifiers and the evidence commands that are bound to them are fixed with the gate definitions (Section 24.1), because the incomplete evidence gate judges the change by them. A difference between them and the approved ones is a difference of the gate definitions. See AE-169.

**AE-163 — Complete evidence**

- Covers: Section 24.9

Given an `active` `core` change with the requirements R1 and R2, each with one evidence command  
When the `close` action runs both evidence commands and both have the result `satisfied`  
Then the evidence is complete, and the incomplete evidence gate is satisfied

**AE-164 — A change with no requirements has no complete evidence**

- Covers: Section 24.9

Given an `active` `core` change whose definition declares no requirement  
When the `close` action is requested  
Then the evidence is not complete, the record states that no requirements are declared, the incomplete evidence gate is not satisfied, and the result is `blocked`

**AE-165 — A requirement without an evidence command is not evidenced**

- Covers: Section 24.9

Given an `active` `core` change with the requirements R1 and R2, where R1 has an evidence command and R2 has none  
When the `close` action is requested  
Then the evidence is not complete, and the record names R2

**AE-166 — A command that cannot run is not evaluable**

- Covers: Section 24.9

Given an `active` `core` change with the requirement R1 whose evidence command names a program that is missing  
When the `close` action is requested  
Then the result of the command is `not_evaluable`, no failure is recorded, nothing is counted toward a retry limit, the change waits with a wait record of kind `external`, and the evidence is not complete

**AE-167 — A failing evidence command leaves the evidence incomplete**

- Covers: Section 24.9

Given an `active` `core` change with the requirement R1 whose evidence command ends with an exit status that the exit map maps to `not_satisfied`  
When the `close` action is requested  
Then the evidence is not complete, and the change does not close

**AE-168 — Other records supplement the executable check**

- Covers: Section 24.9

Given an `active` `core` change with the requirement R1 whose only evidence is a screenshot and a review approval  
When the `close` action is requested, and later an evidence command that is `satisfied` is bound to R1 and the action is requested again  
Then the evidence is not complete at the first request, and complete at the second, where the screenshot and the review approval remain as supplements

**AE-169 — A changed evidence command needs a new approval**

- Covers: Section 24.9

Given a `core` change whose gate definitions were approved with the evidence command of R1, and the command of R1 was replaced after the approval by a command that always ends with the exit status that the exit map maps to `satisfied`  
When the `close` action is requested  
Then the result is `rejected` with the issue code `gates-changed`, and the replaced command has no effect until a human approves the gate definitions again

**AE-170 — A `full` change needs an executable check for Verify-Done**

- Covers: Section 24.9

Given a `full` change in the verify phase with the status `active`, whose requirement R1 has only a screenshot in the Evidence cell of its requirement coverage table  
When the `complete` action evaluates the Definition of Done of the phase  
Then the criterion that evidence is complete is not satisfied, and the phase is not completed

### 24.10 Gate-Command Interpreter

The commands of check-command gates (Section 24.2) and the evidence commands of requirements (Section 24.9) are run directly, as argument lists. No shell runs them, so the syntax of a shell has no effect: a pipe, a conjunction, a redirection, the expansion of a variable or of a pattern, and a command substitution are ordinary characters of an argument. See AE-158.

The interpreter is the program that runs the code a command points at, for example the runtime of a programming language. It is explicit and opt-in. A command MAY use the designated token `@interpreter` as the first element of its argument list. The token stands for the interpreter that the project configuration names if the configuration names one, and only for that interpreter. An implementation MUST NOT discover an interpreter: it MUST NOT search the project for a virtual environment, a tool directory, or any other candidate, because what stands behind the token decides whether every gate passes. When the configuration names no interpreter, the token stands for the interpreter that runs the implementation itself. A first element other than the token is a program that is run as it is. See AE-159, AE-160.

An implementation SHOULD warn when the interpreter that the token stands for lives inside the repository of the project. See AE-161.

Code in a location that version control is told to ignore is invisible to the scope check (Section 24.5). When a command runs code from such a location, including an interpreter or a library that is installed there, a change can alter that code, and so the result of the gate, without a scope violation. The scope check therefore does not show that the code behind a gate is unchanged, and the result of a gate is worth only as much as the protection of the code that its command runs. See AE-162.

**AE-158 — Shell syntax has no effect**

- Covers: Section 24.10

Given a check-command gate whose command is the argument list `run-tests`, `--label`, `a; echo done`  
When the gate is evaluated  
Then the program `run-tests` is run with the two arguments `--label` and `a; echo done`, and no second command `echo` is run

**AE-159 — The designated token stands for the configured interpreter**

- Covers: Section 24.10

Given a project configuration that names the interpreter `rt-stable`, and a check-command gate whose command is `@interpreter`, `check.script`  
When the gate is evaluated  
Then the program `rt-stable` is run with the argument `check.script`

**AE-160 — Without configuration the token stands for the interpreter of the implementation**

- Covers: Section 24.10

Given a project configuration that names no interpreter, a directory inside the repository that holds an interpreter, and a check-command gate whose command is `@interpreter`, `check.script`  
When the gate is evaluated  
Then the interpreter that runs the implementation itself is used, and the interpreter in the repository is not discovered and not used

**AE-161 — Warn when the interpreter lives inside the repository**

- Covers: Section 24.10

Given a project configuration that names an interpreter located in a directory inside the repository  
When a gate whose command starts with `@interpreter` is evaluated  
Then the configured interpreter is used, and the implementation warns that it lives inside the repository

**AE-162 — Code in an ignored location is invisible to the scope check**

- Covers: Section 24.10

Given a check-command gate whose command runs the script `.cache/gate.script`, a location that version control is told to ignore, and a change whose `scope.allow` is `lib/**` that edits the script so that it always ends with the exit status that the exit map maps to `satisfied`  
When the gate is evaluated  
Then the gate is `satisfied`, and the scope check finds no violation, because the edited script is invisible to it

---

## 25. State, Hashing, and Schema Versions

This section defines the state document, the canonical form and the content hash that the protections of Section 24 rely on, and the versions of the schema-governed files. It applies to both method profiles (Section 5.6). The history, the entry hash, and the approvals that Section 24 describes are stored and hashed as this section states.

### 25.1 State Document and Canonical Form

The state document of a change is the JSON file `state.json` in the change directory (Section 4.3). It holds the history of the change (Section 24.4). The implementation owns it, and a human MUST NOT edit it by hand (Section 23.1). The definitions that humans own, such as the change definition and the project configuration, stay YAML documents. In `core`, every change has a state document. In `full`, the state document is kept where the project persists workflow state (Section 4.3). The rules of Sections 24.1, 24.3, 24.4, and 24.8 that read or write the history are enforced mechanically only for a change that has a state document, and an implementation MUST NOT report any of them as enforced for a change whose record is kept inline. See AE-195.

The state document is a JSON object with two fields. `schema_version` holds the version of the schema of the document, and Section 25.3 defines its form and the checks on it. `entries` holds the history: a list of entries in ascending order of `n`, each with the four fields `n`, `prev`, `body`, and `hash` that Section 24.4 defines.

The `body` of an entry holds exactly these fields:

- `action`: the name of the action that the entry records, which is an action of the transition table of the method profile (Section 23.4 or Section 8.3) or `migrate` (Section 25.3);
- `actor`: the identity of the participant that performed the action (Section 24.3);
- `assurance`: the verified assurance level of the claim of the actor, which is `A0`, `A1`, or `A2` (Section 24.3);
- `at`: the instant at which the entry was written, as a string in UTC that is written `YYYY-MM-DDThh:mm:ssZ`;
- `result`: the result of the action, which is `success` or `blocked` (Section 22.2), because an action that is `rejected` or ends in `error` writes no entry;
- `gate_results`: an object from the identifier of each gate that the action evaluated to the result recorded for it (Section 24.2), or `null` when the action evaluated no gate;
- `gate_detail`: an object from the identifier of a gate to the text that the evaluation recorded for it, or `null` when the evaluation recorded none;
- `files`: an object from a path to the content hash of the file (Section 25.2), for the files that the action approved, evaluated, or recorded, or `null` when it concerns no file;
- `note`: the text that the actor gave, or `null`;
- `after`: the record of the state of the change after the action.

A field that does not apply to an action is present with the value `null`. The body holds no other field, except that an action MAY be defined to add fields for itself, and Section 25.3 defines such fields for `migrate`. See AE-189.

The `after` record holds the whole state of the change after the action, and not only what the action changed, so that the state of the change is the `after` record of the last entry (Section 24.4). In `core`, it holds these fields:

- `state` and `outcome` (Section 23.2);
- `approvals`: the approvals recorded so far, in the order of their recording, each naming its target, the identity, the verified assurance level, and the content hash that was approved (Section 24.3), and for a sign-off, an override, and a re-approval also the fields that Sections 24.1 and 24.7 call for;
- `questions`: the questions recorded so far, with the fields of Section 24.8;
- `wait`: the wait record (Section 23.5), or `null`;
- `base_revision`: the base revision (Section 24.5), or `null` before it is recorded;
- `replaced_by`: the identifier given to `supersede`, or `null`;
- `schema_version`: the version of the schema of the document after the action (Section 25.3).

In `full`, the `after` record holds `phase` and `status` (Section 8.1) in place of `state` and `outcome`. Its field `wait` holds the wait content of Section 11.2 and the other metadata of Section 8.1, or `null`, and its other fields are those of `core`. See AE-190.

The file is a JSON text in UTF-8. Its layout, that is, indentation and line breaks, is free, and a writer SHOULD pretty-print it so that a human can read it. The file is not the hashed form: a hash is computed over the canonical form defined below and never over the text of the file, so the layout has no effect on a hash. A JSON object that holds the same key twice is not a valid state document. See AE-188.

The values of a state document, and every value that is hashed, belong to a small domain: strings, integers, booleans, `null`, arrays, and objects whose keys are strings. A string is a sequence of Unicode code points that holds no surrogate code point. An integer is a whole number written in decimal digits, without a fraction or an exponent, and its magnitude does not exceed 2 to the power 53, minus 1, so that implementations that store numbers as double-precision values agree. A floating-point number is not in the domain. An implementation that is about to write or hash a value outside the domain MUST stop with the result `error` and MUST write nothing. See AE-187.

The canonical form of a value is the text built by these rules:

- no whitespace is written outside a string, the elements of an array and the members of an object are separated by `,`, and a key is separated from its value by `:`;
- the members of an object are written in ascending order of their keys, compared as sequences of Unicode code points as defined below, and an object does not hold the same key twice;
- a string is enclosed in `"`; the code point `"` is written `\"` and the code point `\` is written `\\`; the code points U+0008, U+0009, U+000A, U+000C, and U+000D are written `\b`, `\t`, `\n`, `\f`, and `\r`; every other code point below U+0020 is written `\u` followed by four lowercase hexadecimal digits; every other code point is written as itself, so that no code point is written as an escape because it is outside ASCII, and the code points U+007F and `/` are written as themselves;
- an integer is written in decimal digits, with a leading `-` when it is negative, without a leading `+`, without a leading zero, and the integer zero is written `0`; the other values are written `true`, `false`, and `null`.

The canonical bytes of a value are the UTF-8 encoding of its canonical form, without a byte order mark and without a final line feed. See AE-183, AE-184, AE-186.

Strings are compared as sequences of Unicode code points: the first code point at which two strings differ decides the order by its numeric value, and a string that is a prefix of a longer string comes first. Letter case matters, and nothing is normalized. The comparison is not a comparison by UTF-16 code units, which orders some characters above U+FFFF differently. Every comparison of identifiers, paths, and values that Section 24 makes is made in this way. See AE-185.

A hash is written as a hash string: the prefix `sha256:` followed by the 64 lowercase hexadecimal digits of the SHA-256 digest of some bytes. The hash string of a value is the hash string of its canonical bytes. The hash of an entry is the hash string of the object that holds `prev` and `body` (Section 24.4), and the `prev` of the first entry is the prefix `sha256:` followed by 64 digits 0. A hash string is compared as a string, so that a hash written with an uppercase digit differs from the same hash written with lowercase digits. See AE-184, AE-196.

An implementation MUST write the state document with an atomic replacement. It writes the whole new document to a temporary file in the same directory, flushes it to storage when the system allows, and then replaces the state document with the temporary file in a single step of the file system. Until that step, the state document is the previous one. An interruption at any moment, such as a crash, a power loss, or a failed write, therefore leaves the previous state document intact, and a temporary file that is left behind is not state: an implementation MUST ignore it and MAY remove it. When the file system cannot replace a file in a single step, the implementation MUST NOT write, and its result is `error`. The creation of the first state document of a change is a replacement in the same way: an interrupted creation leaves no state document. See AE-193, AE-194.

An implementation MUST also protect a write against a second writer. The writer names the version it read, which is the number of entries of the state document at that time, and zero for a change that has no state document yet. It takes an exclusive lock on the state document of the change, or, when the change has none yet, on the place where the document will be created, and keeps the lock until its replacement has finished. Under the lock it compares the number of entries that the document holds now with the version it read. When the two differ, the operation MUST write nothing and its result MUST be `error` with the stable issue code `state-conflict`, whose message states that another writer changed the change and that the operation can be repeated after reading it again. A writer that cannot take the lock MUST NOT write, and its result is `error`. This applies to the creation of a change and to every operation that records an evaluation, in `core` and in `full`. See AE-191, AE-192.

**AE-183 — The canonical form sorts the keys, drops whitespace, and keeps non-ASCII characters**

- Covers: Section 25.1

Given an object with the member `name`, whose value is `café` written with the single code point U+00E9, and the member `count`, whose value is the integer 2, listed in that order  
When its canonical form is built and hashed  
Then the canonical text is `{"count":2,"name":"café"}`, the code point U+00E9 is written as itself and encoded in UTF-8 as the two bytes C3 and A9, and the hash string is `sha256:29775eba68050199f13058db83b4c14ba4b6a6a26666d6373a3cc47481bf6471`

**AE-184 — The hash string of the empty object**

- Covers: Section 25.1

Given the empty object  
When its canonical form is built and hashed  
Then the canonical text is `{}`, and the hash string is `sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`, which is the prefix `sha256:` and 64 lowercase hexadecimal digits

**AE-185 — Keys are ordered by code point and not by UTF-16 code unit**

- Covers: Section 25.1

Given an object with two members whose keys are the single code points U+1F600 and U+FF5E, listed with U+1F600 first  
When its canonical form is built  
Then the member with the key U+FF5E is written first, because U+FF5E is the lower code point, although an order by UTF-16 code units would place U+1F600 first

**AE-186 — Only the code points that JSON requires are escaped**

- Covers: Section 25.1

Given a string value that holds a line feed, the code point U+0001, a quotation mark, a backslash, a solidus, and the code point U+007F  
When its canonical form is built  
Then the line feed is written `\n`, U+0001 is written `\u0001`, the quotation mark is written `\"`, the backslash is written `\\`, and the solidus and U+007F are written as themselves

**AE-187 — A value outside the domain is neither written nor hashed**

- Covers: Section 25.1

Given an entry body in which one value is the floating-point number 1.5  
When the implementation is about to write the entry  
Then the operation ends with the result `error`, and nothing is written

**AE-188 — The layout of the file does not change a hash**

- Covers: Section 25.1

Given a state document of three entries, and the same document written again with other indentation and other line breaks but with the same values  
When the history is verified  
Then both documents give the same entry hashes, and both histories are consistent

**AE-189 — Every body field is present and a field that does not apply is null**

- Covers: Section 25.1

Given an `ask` action that evaluates no gate, concerns no file, and gives no note  
When the entry is written  
Then the body holds the ten fields `action`, `actor`, `assurance`, `at`, `result`, `gate_results`, `gate_detail`, `files`, `note`, and `after`, and `gate_results`, `gate_detail`, `files`, and `note` are `null`

**AE-190 — The record after an action is worded per method profile**

- Covers: Section 25.1

Given a closed `core` change with the outcome `done` and a `full` change in the build phase with the status `done`  
When the `after` record of the last entry of each change is read  
Then the `after` record of the `core` change holds `state` set to `closed` and `outcome` set to `done`, the `after` record of the `full` change holds `phase` set to `build` and `status` set to `done`, and neither record holds the fields of the other

**AE-191 — The second of two writers with the same version fails when a change is created**

- Covers: Section 25.1

Given a `core` project and a `full` project, and in each of them two writers that both read that no state document of the change `c-1` exists, and the first writer of the project has created the state document  
When the second writer of the project tries to create it with the version zero  
Then the second writer writes nothing, its result is `error` with the issue code `state-conflict`, and the state document is the one that the first writer created

**AE-192 — The second of two writers with the same version fails when an evaluation is recorded**

- Covers: Section 25.1

Given an `active` `core` change and a `full` change in the build phase with the status `active`, each with a state document of six entries, and for each change two writers that both read the version 6  
When both writers request the action that completes the change (`close` or `complete`) and the first writer records its evaluation as entry 7  
Then the second writer writes nothing, its result is `error` with the issue code `state-conflict`, and the state document holds seven entries

**AE-193 — An interrupted creation leaves no state document**

- Covers: Section 25.1

Given a new `core` change and a new `full` change whose state documents are being created, and the process stops after the temporary file is written and before the replacement  
When the project is read again  
Then neither change has a state document, the temporary file is ignored, and the creation can be repeated

**AE-194 — An interrupted write of an evaluation leaves the previous state intact**

- Covers: Section 25.1

Given an `active` `core` change and a `full` change in the build phase with the status `active`, each with a state document of six entries, and the process stops while the entry 7 that records an evaluation is being written  
When each state document is read again  
Then each document is the previous one of six entries, it is consistent, and no part of the entry 7 is in it

**AE-195 — A change whose record is inline is not reported as enforced**

- Covers: Section 25.1

Given a `full` change of Class S whose record is kept inline in an issue, in a project that persists no workflow state  
When the implementation reports which protections are enforced for it  
Then the report does not list Sections 24.1, 24.3, 24.4, and 24.8 as enforced, because the change has no state document

**AE-196 — A hash is compared as a string**

- Covers: Section 25.1

Given an entry whose stored `hash` is the correct hash written with an uppercase hexadecimal digit  
When the consistency of the history is verified  
Then the stored hash differs from the hash that is computed again, and the history is not consistent

### 25.2 Content Hash

The content hash is the hash string (Section 25.1) that identifies some content. An approval binds the content hash of what it approves (Section 24.3), and the identity of fixed gate definitions is a content hash (Section 24.1). This section defines the content hash of the content that those sections name.

The content hash of a text file is the hash string of the bytes of the file after its line endings are normalized: every pair of a carriage return followed by a line feed, and every carriage return that is not followed by a line feed, is replaced by a line feed. Nothing else is changed. A file with the same text and different line endings therefore has the same content hash. See AE-197.

The content hash of a binary file is the hash string of the bytes of the file, exactly. See AE-198.

Whether a file is text or binary is decided by the implementation. The decision MUST depend only on the bytes of the file, so that the same bytes are always classified in the same way, and an implementation SHOULD classify a file as text only when its bytes are valid UTF-8 and hold no zero byte. The hash string does not state which kind was applied. A content hash is therefore comparable only with a content hash that an implementation computed with the same decision, and a content hash that differs from the recorded one is a difference. See AE-198.

The content hash of a parsed definition, such as the gate definitions of a change (Section 24.1), is the hash string of the canonical bytes of the parsed value (Section 25.1) and not of the text of the file. A YAML document is read as YAML 1.2 with its core schema, and an alias is replaced by the value it refers to. Comments, layout, the order of the keys of a mapping, and the quoting of a scalar that reads as the same value therefore have no effect, and the order of the elements of a sequence has an effect. A parsed value that is outside the domain of Section 25.1 has no content hash: this holds for a floating-point number, a timestamp, a mapping key that is not a string, a mapping that repeats a key, and a scalar that the core schema reads as a type that the domain does not hold. An operation that needs the content hash of such a definition MUST be rejected, and its issue states which value is outside the domain. See AE-199, AE-200.

The content hash of a set of files is the hash string of the canonical bytes of an object that maps the path of each file to its content hash. A path is written relative to the root of the repository, with `/` as the separator (Section 24.5). The order in which the files are listed has no effect. See AE-201.

The content hash of the gate definitions together with the identifier of a gate, which binds the sign-off of a gate and an override (Section 24.3), is the hash string of the canonical bytes of an object with the member `definitions`, which holds the content hash of the gate definitions, and the member `gate`, which holds the identifier. See AE-202.

**AE-197 — Text with different line endings has one content hash**

- Covers: Section 25.2

Given two text files that hold the same two lines, the first with the line ending carriage return and line feed and the second with the line ending line feed alone  
When the content hash of each file is computed  
Then the two content hashes are equal

**AE-198 — A binary file is hashed byte for byte**

- Covers: Section 25.2

Given two binary files that differ only in that the first holds the bytes 0D 0A where the second holds the byte 0A, and a file whose bytes are not valid UTF-8  
When the content hash of each file is computed  
Then the content hashes of the two files differ, the file whose bytes are not valid UTF-8 is hashed on its exact bytes, and the same bytes give the same content hash each time

**AE-199 — Layout and comments do not change the hash of a parsed definition, and a list order does**

- Covers: Section 25.2

Given a gate definition file, a copy with an added comment, other indentation, the keys of a mapping in another order, and a quoted scalar that reads as the same string, and a third copy in which the order of two elements of a list is exchanged  
When the content hash of each file is computed as a parsed definition  
Then the first copy has the same content hash as the original, and the third copy has a different content hash

**AE-200 — A definition with a value outside the domain has no content hash**

- Covers: Section 25.2

Given a gate definition in which a retry limit is written as the floating-point number 1.5, and the same definition in which the value is the quoted string `1.5`  
When the approval of the gate definitions is requested for each  
Then the first approval is rejected and its issue names the value outside the domain, and the second definition has a content hash

**AE-201 — The order of the files has no effect on the hash of a set**

- Covers: Section 25.2

Given a set of the two files `lib/a.py` and `docs/b.md`, listed in the first order and then in the reverse order  
When the content hash of the set is computed  
Then both orders give the same content hash, which is the hash string of the canonical bytes of the object that maps `docs/b.md` and `lib/a.py` to their content hashes

**AE-202 — The identifier of the gate is part of the hash of a sign-off**

- Covers: Section 25.2

Given the same gate definitions and two gate identifiers, `review-ok` and `release-ok`  
When the content hash of the gate definitions together with each identifier is computed  
Then the two content hashes differ, because the member `gate` of the hashed object differs

### 25.3 Schema Versions and Migration

Every machine-readable file that a schema governs carries the top-level field `schema_version`. These files are the project configuration (`.ggsad/config.yaml`), the integration mappings, the change definition (Section 23.1), and the state document (Section 25.1). A Markdown document, such as the specification of a change or the change specification of a `full` change, has no schema and no schema version.

The value of `schema_version` is a string of two non-negative integers that are written in decimal digits and joined by one dot, such as `0.1`. Neither integer has a sign or a leading zero, except that the integer zero is written `0`. Two versions are compared one integer at a time, from left to right, by the numeric value of each integer, so that `0.9` is older than `0.10` and `0.10` is older than `1.0`. A value that is not a string, for example the number 0.1 that a YAML file holds when the value is not quoted, is not a version.

An implementation supports one or more versions of each kind of file: it reads and writes a file of a supported version as it is. It MAY also hold migration steps, and each step converts a file from one version to the next higher version. A version is migratable when it is not supported, when it is lower than the highest supported version, and when a chain of steps leads from it to a supported version. See AE-208.

Before an implementation uses a governed file for an operation, it MUST check the `schema_version` of the file:

- a version that equals a supported version is accepted;
- a migratable version is refused until the file is migrated explicitly: the operation answers `rejected` with the stable issue code `migration-required`;
- every other value is refused with the result `rejected` and the stable issue code `schema-version-unsupported`: a version that is newer than every supported version, a version that is unknown, a missing field, the value `null`, an empty string, a value that is not a string, and a string that is not a version.

A refusal writes nothing and leaves `changed` false (Section 22.2). It applies to every operation that uses the file, including a read-only operation and the validation of the file, and it applies to the state document of a change in the same way as to the other files. The one exception is the `migrate` operation, which accepts a migratable version. An implementation MUST NOT guess the content of a file of a version that it does not support, and MUST NOT write such a file. See AE-203, AE-204, AE-205, AE-206, AE-207.

The `migrate` operation (Section 22.1) is the only way to change the version of a file. It is explicit and it is never carried out silently as a part of another operation. It takes the file and optionally a target version, which is a supported version that is higher than the version of the file and which is the highest supported version when it is not given. It applies the steps of the chain one at a time in ascending order of version, so that no step is skipped and no step is applied twice, and it records each step. When a step cannot be applied, the operation writes nothing and answers `error`; the steps that were applied before it are not kept. A file that already has the target version, or a higher one, is not migrated, and the operation answers `rejected`. See AE-209.

A migration of the state document appends one entry to the history for each step. The body of the entry has the action `migrate` and the result `success`, and in addition to the fields of Section 25.1 it holds `source_version`, the version before the step, `target_version`, the version after the step, and `source_hash`, the source content hash, which is the content hash (Section 25.2) of the state document before the step, taken as a parsed value for a state document written in JSON and as a text file for a state document written in YAML. The `after` record of the entry holds the target version in `schema_version`, and the field `schema_version` of the state document is set to the version after the last step. The entries that the history already holds are kept as they are: a migration appends to the history and MUST NOT rewrite an entry, and the `n`, `prev`, `body`, and `hash` of every earlier entry are unchanged. See AE-209, AE-210.

The version of the state document MUST equal the latest recorded version, which is the `schema_version` of the `after` record of the last entry. A state document whose version differs from it, whether lower or higher, is not consistent in the sense of Section 24.4. An implementation MUST NOT act on it, and its result is `rejected` with the stable issue code `schema-version-mismatch`. This detects a state document whose version was lowered by hand in order to run a migration again, or to make a refusal disappear. See AE-211.

A project-level artifact, that is, the project configuration or the integration mappings, is migrated inside a change: the `migrate` operation names a change that is not `closed`, and the migration is recorded in the history of that change, in an entry whose `files` field maps the path of the artifact to its content hash after the step, and whose `source_hash` is its content hash before the step. The change definition and the state document of a change are migrated as part of that change. A migration that changes the parsed gate definitions of a change makes them differ from the approved ones, and Section 24.1 then requires that a human approves them again. The `migrate` operation does not change the state or the outcome of a change. Applied to the state document or the change definition of a change, it is therefore legal from every state of that change, and it is not a row of a transition table. See AE-212, AE-213.

A state document that an earlier version of this method wrote as a YAML document named `state.yaml` is migrated by the `migrate` operation, which converts it to `state.json` as a step of the chain. The first entry of the new state document is a `migrate` entry with `n` 1 and the `prev` of Section 25.1, whose `source_hash` is the content hash of the old file as a text file and whose `after` record holds the state that was taken over from the old document. The operation neither changes nor deletes the old file, and once `state.json` exists the old file is not read. The chain of hashes starts at that entry: the earlier history is not covered by it, and an anchor that exists for the change makes a history that was restarted in this way detectable (Section 24.4). See AE-214.

**AE-203 — A version that equals a supported version is accepted**

- Covers: Section 25.3

Given an implementation that supports the version `0.1`, and a project configuration with `schema_version` set to `"0.1"`  
When an operation reads the project configuration  
Then the version is accepted, and the operation goes on

**AE-204 — An older migratable version is refused until it is migrated**

- Covers: Section 25.3

Given an implementation that supports only the version `1.0` and holds a step from `0.1` to `1.0`, and a change definition with `schema_version` set to `"0.1"`  
When the `validate` operation is requested for the change  
Then the result is `rejected` with `changed` false and the issue code `migration-required`, nothing is written, and after an explicit `migrate` the same operation accepts the change definition

**AE-205 — A newer version is refused**

- Covers: Section 25.3

Given an implementation that supports only the version `1.0`, and a state document with `schema_version` set to `"1.1"`  
When any operation, including a read-only one, uses the state document  
Then the result is `rejected` with `changed` false and the issue code `schema-version-unsupported`, and nothing is written

**AE-206 — A missing, null, or empty version is refused**

- Covers: Section 25.3

Given three project configurations, the first without the field `schema_version`, the second with `schema_version` set to `null`, and the third with `schema_version` set to the empty string  
When an operation reads each of them  
Then each read is refused with the result `rejected` and the issue code `schema-version-unsupported`, and nothing is written

**AE-207 — A value that is not a version string is refused**

- Covers: Section 25.3

Given a project configuration with the unquoted value 0.1, which the YAML file holds as a number, a second one with the string `"01.1"`, and a third with the string `"1.0.0"`  
When an operation reads each of them  
Then each read is refused with the result `rejected` and the issue code `schema-version-unsupported`, because none of the values is a string of two integers without a leading zero joined by one dot

**AE-208 — Versions are compared one integer at a time**

- Covers: Section 25.3

Given an implementation that supports only the version `0.10` and holds a step from `0.9` to `0.10`, and two change definitions with the versions `"0.9"` and `"0.100"`  
When an operation reads each of them  
Then the version `0.9` is migratable and is refused with the issue code `migration-required`, and the version `0.100` is newer than the supported version and is refused with the issue code `schema-version-unsupported`

**AE-209 — A migration applies its steps in ascending order and records each**

- Covers: Section 25.3

Given an implementation that supports only the version `2.0` and holds the steps `1.0` to `1.1` and `1.1` to `2.0`, and a state document of six entries with `schema_version` set to `"1.0"`  
When the `migrate` operation is requested for the state document without a target version  
Then the step from `1.0` to `1.1` is applied and recorded as entry 7, the step from `1.1` to `2.0` is applied and recorded as entry 8, each entry names its source version, its target version, and its source content hash, and the version of the state document is `"2.0"`

**AE-210 — A migration appends and does not rewrite an entry**

- Covers: Section 25.3

Given a state document of six entries that is consistent, and a migration of it to a newer version  
When the history is read again after the migration  
Then the entries 1 to 6 have the same `prev`, `body`, and `hash` as before, the entries 7 and later are the migration entries, and the history is consistent

**AE-211 — A lowered version of the state document is detected**

- Covers: Section 25.3

Given a state document whose last entry records the version `"1.1"`, and a hand edit that sets the field `schema_version` of the document to `"1.0"`  
When any operation is requested for the change  
Then the result is `rejected` with the issue code `schema-version-mismatch`, nothing is written, and the implementation does not act on the change

**AE-212 — A project-level artifact is migrated inside a change and recorded in it**

- Covers: Section 25.3

Given a migratable project configuration, an `active` change `c-1`, and a `closed` change `c-0`  
When the `migrate` operation for the project configuration names `c-1`, and then another `migrate` operation names `c-0`, and then a third names no change  
Then the first migration succeeds and the history of `c-1` gets an entry whose `files` field maps the path of the project configuration to its content hash after the step and whose `source_hash` is its content hash before the step, and the second and the third operation are rejected and write nothing

**AE-213 — A migration that changes the gate definitions needs a new approval**

- Covers: Section 25.3

Given an `active` `core` change whose gate definitions were approved, and a change definition whose migration changes its parsed gate definitions  
When the change definition is migrated and then the `close` action is requested  
Then the migration is recorded, and the `close` action is rejected with the issue code `gates-changed` until a human approves the gate definitions again

**AE-214 — A YAML state document is converted by an explicit migration**

- Covers: Section 25.3

Given a change directory with a YAML state document named `state.yaml` and no `state.json`  
When the `migrate` operation is requested for the change  
Then `state.json` is created with a first entry that is a `migrate` entry with `n` 1 and the `prev` of the first entry, whose `source_hash` is the content hash of the old file as a text file, the old file is neither changed nor deleted, and later operations read only `state.json`
