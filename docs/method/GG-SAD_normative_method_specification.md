# GG-SAD — Normative Method Specification

**Version:** 2.0 (draft)
**Status:** Draft, pending owner approval and independent review  
**Revision:** 2026-10-31 — Restructured around the `core` method profile. The `full` method profile, the automation contract, the state document with its hashing and schema versions, and the signature verification moved to their own documents (Section 1.1). Pair Review is bounded to one round and one re-check (Section 14.3). The acceptance examples were reduced from 326 to a representative set and renumbered in order.  
**Revision:** 2026-11-02 — Applied the owner decisions of the requirements interview (`docs/requirements/`): combination mode and layer 5 moved to "future"; approved-human list; `review` gate; follow-up change; `repair`, `conflict`, `check-scope`; status report (Section 23.8); human close; default retry limit; baseline reasons; required tools. New examples are numbered from AE-313.  
**Target audience:** AI agents, workflow engines, automation systems, and technical project owners

---

## 1. Purpose

**Goal-Gated Spec-Anchored Development (GG-SAD)** is a lightweight, goal-oriented development method for specification-driven software development.

GG-SAD defines:

- a small set of binding project documents,
- a goal-bound change with one specification and a short state model,
- explicit done, wait, and fail gates,
- minimal artifacts per change,
- rules for deviations, decisions, and evidence,
- controlled use of AI agents.

GG-SAD does not require epics, sprints, story points, role models, or ceremonies. The primary unit of work is a **goal-bound change**.

GG-SAD MUST be usable in **stand-alone mode**, where GG-SAD provides the governing method and execution flow, and it MUST NOT depend on a specific agent, IDE, or framework.

**Combination mode**, where GG-SAD governs goals, gates, evidence, state, and precedence while another method, framework, tool, or agent platform supplies planning, execution, review, context engineering, or automation capabilities, is described in Sections 3.8 and 17 but is a future capability. It is described and not built. An implementation MUST refuse to start when the project configuration asks for combination mode, and its message MUST say that combination mode is not supported.

### 1.1 Document Scope and Moved Sections

This specification is the leading GG-SAD semantic and product baseline. The precedence list in Section 4, Document Hierarchy, governs artifacts inside a GG-SAD-managed project; it does not rank this specification itself, which remains superior to every document ordered by that list.

A GG-SAD implementation MAY be developed using another development method. That development method MAY govern implementation work, but it MUST NOT redefine the GG-SAD product semantics established by this specification.

This specification contains the `core` method. Three further documents in `docs/method/` hold what it does not contain. Section numbers are stable: a section number that this document does not contain names a section of one of them.

| Document | Sections | Status |
|---|---|---|
| `GG-SAD_implementation_contract.md` | 22 (automation contract) and 25 (state document, content hash, schema versions) | Normative for the reference implementation only |
| `GG-SAD_signing_extension.md` | 24.3 as extended (assurance levels A1 and A2, signed approval) | Optional extension |
| `GG-SAD_full_profile_deferred.md` | 4.1, 5.5, 6 to 10, 16.1 to 16.4, the flow diagram of old Section 21, and the examples of the `full` method profile | Deferred, not normative |

A reference in this document to a section of one of these documents names that document. A bare reference to Section 22 or 25, or to a subsection of them, names `GG-SAD_implementation_contract.md`. An `AE-nnn` reference names the document that defines the example: `AE-001` to `AE-066` are in this document, `AE-067` to `AE-103` in `GG-SAD_implementation_contract.md`, and `AE-104` to `AE-109` in `GG-SAD_signing_extension.md`. The examples that follow the 2026-11-02 decisions are numbered `AE-313` onward and are in this document unless a section of another document says otherwise.

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

Every change MUST be controlled by defined gates:

- **Definition of Done (DoD):** Has the change been completed successfully?
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

GG-SAD workflows MUST be tailorable. Tailoring MAY change required artifacts, review depth, approval rules, evidence depth, permissions, and automation.

Tailoring MUST NOT remove the invariant core:

- an explicit goal,
- a specification anchor,
- gate evaluation,
- evidence appropriate to the selected compliance profile,
- controlled wait and fail behavior,
- traceable final status.

### 3.8 Stand-Alone and Combination Use

GG-SAD MUST remain independent from a specific planning framework, coding agent, IDE, issue tracker, or delivery platform.

Combination mode is a future capability (Section 1). When it is built, these rules will apply to it:

- GG-SAD owns governance semantics, state, gates, precedence, and closure;
- the integrated method or tool MAY own subordinate planning or execution artifacts;
- mapped external artifacts MUST identify their GG-SAD role;
- external workflows MUST NOT bypass GG-SAD gates or weaken the active compliance profile;
- conflicts MUST be resolved according to the GG-SAD document hierarchy.

An integration mapping for an external framework or tool will be a fifth layer of the resolution in Section 5.3. That layer is not active today (Section 5.3).

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

Pair Review is OPTIONAL by default. Its use and required depth MUST be resolved from the active compliance profile, project scope, risk, impact, and project-specific policy. A project MAY require Pair Review for selected phases, artifact types, or risk categories.

The Reviewer MUST NOT silently modify the Requestor's governed work product as part of the review. Findings MUST be returned to the Requestor for disposition. A separate explicitly assigned change action MAY authorize the Reviewer to become a Requestor for a later correction cycle.

Where a rule of this specification requires a human participant, the claim of being a human is evidenced at an assurance level (Section 24.3).

Pair Review MUST NOT replace a required human approval. Where segregation of duties applies, the project MAY require Requestor, Reviewer, and Approver to be three distinct participants.

## 4. Document Hierarchy

In case of conflict between project documents, the following priority applies:

1. `docs/constitution.md`
2. existing accepted ADRs under `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. the approved change specification `spec.md`
6. implementation and tests
7. evidence, supplementary notes, and temporary work artifacts

A change MUST NOT silently override a higher-ranking document.

When a requirement of a change is set aside because it contradicts a higher-ranking document, the implementation or the agent MUST tell the owner openly, in this form: `requirement <id> was not applied, because it needs an approved change in <higher-ranking document>`. The message is recorded in the history of the change.

Two guards make an override of a higher-ranking document visible:

1. **Fingerprint of the higher documents.** When the specification of a change is approved, the implementation records the content hash (Section 25.2) of each document that ranks above the specification (items 1 to 4 above). While any of these hashes differs from the recorded one, every state-changing operation except `cancel` and the approval of the edit MUST be rejected with the issue code `higher-documents-changed`, whose message names the documents. A human approves the edit with the approval target `documents`, which replaces the recorded hashes and is recorded as an amendment.
2. **Conflict line.** `spec.md` carries the line `Conflicts with higher documents: none` or `Conflicts with higher documents: <list>`. A human confirms the line when approving the specification. The implementation checks only that the line exists: the approval of a specification without the line MUST be rejected with the issue code `conflict-line-missing`. It does not judge whether the line is true.

See AE-313.

**AE-313 — An edit of a higher-ranking document stops the change until a human approves it**

Given an `active` `core` change whose specification was approved, and `docs/architecture.md` edited afterwards  
When the `close` action is requested  
Then the result is `rejected` with `changed` false and the issue code `higher-documents-changed` that names `docs/architecture.md`, and the change can continue after a human approves the target `documents`

### 4.2 Project-Wide Documents

```text
docs/
├── constitution.md     non-negotiable rules: quality, security, architecture, approvals,
│                       prohibited actions, breaking-change rules, limits, minimum evidence
├── project-brief.md    stable context: problem, users, outcomes, scope and non-goals,
│                       constraints, compliance profile, integrated methods
├── architecture.md     current structure: components, boundaries, data flows, deployment,
│                       known constraints, related ADRs
├── roadmap.md          intended direction (Now, Next, Later, Open); not a backlog
├── definitions/        project-wide standard gates
└── adr/                durable architecture decisions, ADR-<number>-<title>.md
```

The project brief MUST NOT contain architecture decisions that belong in ADRs. It MUST record the compliance profile, the method profile, the operating mode, and the integrated methods and tools. Templates for these documents are in `.ggsad/templates/`.

The files under `docs/definitions/` contain the project-wide standard gates. Local specifications MAY strengthen these rules, but MUST NOT weaken them (Section 5.3). A `core` change has no exception to this rule.

Existing accepted ADRs take precedence over new requirements and plans.

The documents that a project MUST have depend on its compliance profile (Section 5.1):

| Compliance profile | Required documents | Optional documents |
|---|---|---|
| `lean` | `docs/project-brief.md`, `docs/constitution.md` | `docs/architecture.md`, `docs/roadmap.md`, `docs/definitions/`, `docs/adr/` |
| `standard`, `governed`, `regulated` | `docs/project-brief.md`, `docs/constitution.md`, `docs/architecture.md`, `docs/roadmap.md` | `docs/definitions/`, `docs/adr/` |

When the specification or the gate definitions of a change are approved and a required document is missing, the implementation MUST warn and MUST NOT block the approval. Each fact has one home (Section 3.5): a document names a fact of another document by reference.

### 4.3 Change-Specific Documents

A change keeps its documents in this layout:

```text
specs/<change-id>/
├── change.yaml
├── spec.md
├── state.json
└── review.md
```

`change.yaml`, `spec.md`, and `state.json` are the three documents of a change (Section 23.1). `review.md` is conditional. It is the single place where the result of a Pair Review is kept (Section 14.5) and the file that a done gate of the kind `review` reads (Section 23.3). It is not a document of the change, and the scope check of Section 24.5 does not measure it. Other review files are not documents of the change, and the scope check measures them like any other file that is not a record file.

The identifier of a change, which is the `id` of the change definition (Section 23.1), names the directory `specs/<change-id>/` of the change. The whole identifier MUST match `[A-Za-z0-9][A-Za-z0-9._-]*`, so that it holds no path separator. It MUST NOT end with the character `.`. The part of the identifier before its first dot, which is the whole identifier when it holds no dot, MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case. Two identifiers that are equal after that folding name the same directory on a file system that ignores letter case, so an identifier MUST also be unique among the changes of the project after the folding: an identifier that differs from the identifier of an existing change only in the case of ASCII letters is not unique. The same syntax applies to the values of `follows` and `replaced_by`, which name a change by its identifier. A definition with an identifier that does not follow these rules is rejected, and nothing is written. See AE-001.

Every change carries mandatory information regardless of file layout: the goal, specification anchor, gate outcome, evidence, wait or fail behavior when applicable, and final status.

`state.json` is the state document of the change (Section 25.1). A change always has one.

**AE-001 — An identifier that can leave the change directory or collide is rejected**

Given a project that holds the change `Task-7`, and five change definitions whose identifiers are `../x`, `a/b`, `task-7`, `nul`, and `c-1`  
When the `new` action receives each definition  
Then the first four are rejected and nothing is written, because `../x` and `a/b` hold a path separator, `task-7` differs from `Task-7` only in letter case, and `nul` is a reserved name, and the definition with the identifier `c-1` is accepted

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

The core rules of this specification are the same for all four profiles. The profiles differ only in these respects:

| Compliance profile | What it changes in the rules of this specification |
|---|---|
| `lean` | A human who requested the work MAY approve it (Section 5.4). Pair Review MAY be omitted (Section 14.1). Fewer project documents are required (Section 4.2). |
| `standard` | Pair Review is applied where practical. The four project documents of Section 4.2 are required. |
| `governed` | As `standard`, and Pair Review SHOULD be required for relevant high-impact changes (Section 14.1). |
| `regulated` | As `governed`, and the project SHOULD require three distinct participants for Requestor, Reviewer, and Approver (Section 3.10). |

A compliance profile reaches an assurance level only through a gate or the project configuration (Section 24.3).

The profile in `.ggsad/config.yaml` and the profile in `docs/project-brief.md` MUST be equal. An implementation MUST report a difference, and it MUST NOT create a change while they differ. An implementation MUST offer an `init` operation that takes the profile once and creates the configuration, the brief, and the template documents that the profile requires (Section 4.2); it MUST NOT overwrite an existing file (Section 22.1).

Projects MAY define additional compliance profiles. Custom compliance profiles MUST inherit from a default compliance profile or explicitly document every invariant and deviation.

### 5.2 Tailoring Dimensions

A compliance profile MAY tailor:

- required artifacts,
- mandatory document sections,
- criterion severity,
- automatic, review, and approval checks,
- evidence retention and provenance,
- human approval requirements,
- Pair Review activation, reviewer independence, review scope, and finding severity rules,
- enabled practice profiles,
- agent permissions and autonomy,
- release, rollback, and monitoring requirements.

A compliance profile of lower compliance MAY reduce optional controls. It MUST NOT disable the invariant core defined in Section 3.7.

A compliance profile is resolved together with the method profile as the second layer of Section 5.3, and a lower layer MUST NOT weaken it.

### 5.3 Profile Resolution

The effective workflow MUST be resolved in this order:

1. GG-SAD invariant core,
2. selected method profile and compliance profile, resolved together,
3. project-specific configuration,
4. local strengthening in the change definition.

A lower layer MUST NOT weaken a higher layer.

Layer 2 is one layer that holds two things. The method profile (Section 5.6) and the compliance profile (Section 5.1) of a change are resolved together, and neither ranks above the other. Four layers are active. A fifth layer, integration mappings for external frameworks and tools, is a future capability that moves with combination mode (Sections 3.8 and 17). Until it is built, no layer is added and no integration mapping affects the resolution.

A lower layer weakens a higher layer when it does any of these things to a gate that the higher layer defines: it removes the gate, that is, it states that the gate does not apply or it leaves the gate out of a definition that replaces the gates of the higher layer; it alters the condition of the gate, including its kind and every other declaration that Section 24.1 fixes; it lowers its severity (Section 24.7); or it lowers the assurance level that the gate or the action requires (Section 24.3), where a lower statement of an assurance level is neutralized and is not rejected (see below). A lower layer strengthens a higher layer when it adds a gate with an identifier of its own, or when the project configuration raises a required assurance level. Strengthening is permitted at every layer. A lower layer MUST NOT strengthen by redefining a gate of a higher layer: it adds a gate of its own instead. The result of the resolution MUST NOT depend on the order in which layers or their entries are listed, and an entry that is listed later never overrides an entry of a higher layer. See AE-002, AE-004.

The required assurance level of an action is the higher of the levels that the layers state (Section 24.3). A lower layer that states a lower level than a higher layer requires for the same kind of action therefore does not lower it: the statement is neutralized, that is, it is accepted, it has no effect, and it is not a cause of rejection. See AE-003.

A `core` change implements layers 1 to 4. Layer 1 is the invariant core of Section 3.7 with the protections of Section 24. Layer 2 supplies the base gates of Section 23.7 together with the rules of the compliance profile. Layer 3 is the project configuration, for example the minimum assurance levels of Section 24.3. Layer 4 is the gates and the scope of the change definition (Section 23.1). A `core` change does not use integration mappings: its gates are the base gates of Section 23.7 and the gates of its change definition. The combination mode of Sections 3.8 and 17 is a future capability, and the reference implementation does not build it. When the fifth layer is built, it MUST NOT weaken a higher layer, and no external workflow bypasses a gate (Section 3.8). The layers are never renumbered.

An implementation MUST check that a change does not weaken a higher layer when the change is created, and again before the gate definitions of the change are approved (Section 24.1), because a definition can be edited after the change is created. For a `core` change the check compares the change definition with the base gates of Section 23.7. A change definition that states that a base gate does not apply, or that lists a gate with the identifier of a base gate, redefines that base gate. It MUST be rejected with the result `rejected` and `changed` false (Section 22.2), and nothing is written. The stable issue code is `gate-weakened` when the definition states that the base gate does not apply, or when the listed gate differs from the base gate in its kind, its condition, or its severity. The message names the gate and the manner of the weakening: removed, altered, or severity lowered. A listed gate that does not differ from the base gate is rejected as a duplicate identifier (Section 23.3). See AE-002, AE-005.

**AE-002 — Reject a definition that removes a base gate**

Given a `core` change definition that states that the base gate `incomplete-evidence` does not apply to the change  
When the `new` action receives it  
Then the definition is rejected with the issue code `gate-weakened`, the message names `incomplete-evidence` as removed, `changed` is false, and no change is created

**AE-003 — A lower level in a lower layer does not lower the required level**

Given a project configuration that sets the minimum level A2 for the sign-off of gates, and a `core` change definition whose `sign-off` done gate `legal-ok` states the minimum level A1  
When `human:ada` signs off `legal-ok` with a claim at A1  
Then the sign-off is rejected, because the required level remains A2, and the change definition itself was accepted, because the lower statement is neutralized: it is accepted, it has no effect, and it is not rejected

**AE-004 — A strengthening does not offset a later weakening**

Given a `core` change definition that lists the done gate `review-ok` of the kind `sign-off` first and, listed after it, a fail gate `scope-violation` with the severity `soft`  
When the `new` action receives it  
Then the whole definition is rejected with the issue code `gate-weakened`, because an entry listed later does not override a higher layer and an added gate does not make up for a weakened one, and no change is created

**AE-005 — Check again before the gate definitions are approved**

Given a `core` change created from a valid definition, and `change.yaml` edited afterwards so that it lists a fail gate `scope-violation` with the severity `soft`  
When `human:ada` approves the target `gates`  
Then the approval is rejected with the issue code `gate-weakened`, `changed` is false, and no approval is recorded

### 5.4 Non-Delegable Human Approval

Regardless of the active compliance profile or the `lean` profile's self-approval allowance in Section 5.1, the following decisions MUST always be made by a human and MUST NOT be satisfied by agent self-approval:

- approval of a breaking change under Section 13;
- resolution of an ADR conflict requiring a decision under Section 13;
- any decision that would trigger a Definition of Fail condition under Section 12 if left unresolved.

Self-approval under the `lean` profile is permitted only for decisions outside this non-delegable set.

A decision that a human makes is evidenced at an assurance level (Section 24.3). A claim satisfies a decision of the set above only if its verified level is at least the level that Section 24.3 requires for the action that records the decision, which is A0 when neither a gate nor the project configuration states a minimum. A claim at the level A0 is self-declared, and it satisfies such a decision only where the required level is A0.

Self-approval under the `lean` compliance profile means that the human who requested the work may approve it. It never means that a participant that is not a human approves it, because every approval is performed by a human (Sections 23.4 and 24.3). See AE-006.

**AE-006 — Self-approval under `lean` is by a human only**

Given a `core` change with the compliance profile `lean`, a decision outside the non-delegable set, the identity `human:ada` who requested the work, and the identity `agent:builder`  
When each identity approves the target `spec`  
Then the approval by `human:ada` is recorded, although she requested the work, and the approval by `agent:builder` is rejected, because a participant that is not a human cannot approve

### 5.6 Method Profiles

GG-SAD defines one **method profile**, `core`. A method profile fixes the model by which a change is carried out: its documents, states, gates, and actions. `core` is the model with four states, three outcomes, and one set of gate lists per change. It is specified in Section 23.

The method profile is a second axis beside the compliance profiles of Section 5.1. It does not replace, rename, or alter the compliance profiles, and a compliance profile does not select a method profile.

A second model, `full`, with phases, size classes, and Definition of Ready and Definition of Done pairs, is kept in `GG-SAD_full_profile_deferred.md`. It is not a method profile of this specification: the reference implementation MUST reject the creation of a change that selects it. See AE-007.

Every change has exactly one method profile and exactly one compliance profile. Both are resolved in the order defined in Section 5.3.

The compliance profile of a change MUST equal the active compliance profile of the project (Section 5.1) at the time the change is created. A request to create a change whose compliance profile differs from it is rejected, and no change is created. See AE-008.

A change MUST record its method profile, `core`, when the change is created. The identifier `core` is an exact lowercase string. Any other value, including a different letter case or surrounding whitespace, and including `full`, is not a method profile of this specification and MUST be rejected. See AE-007.

The method profile of a change is fixed for the life of the change. The recorded value MUST NOT be edited.

**AE-007 — Reject a change that selects the deferred model**

Given a change definition whose `method_profile` is `full`
When a change is created from it
Then the creation is rejected, and no change is created

**AE-008 — The compliance profile of a change equals the project's**

Given a project whose active compliance profile is `regulated`  
When a change is created with the compliance profile `regulated`, and another change is created with the compliance profile `lean`  
Then the first change is created, and the second creation is rejected and no change is created, because the compliance profile of the second change differs from the active compliance profile of the project

## 11. Definition of Wait

DoW describes conditions under which the flow MUST pause in a controlled manner without being considered failed.

### 11.1 Typical Wait Reasons

Typical reasons to wait are missing user input, a pending decision, a dependency, a running process, a pending approval, and an external system that cannot be reached. The kinds of wait record in Section 23.5 classify them: a gate that cannot be evaluated (Section 24.2) causes a wait of kind `external`, and a soft failure that awaits a human disposition (Section 24.7) causes a wait of kind `fail-gate`.

### 11.2 Mandatory Content of a Wait State

Every wait state MUST include:

- reason,
- outstanding information or decision,
- responsible person or source,
- resume condition.

The fields are `reason`, `outstanding` (the outstanding information or decision), `owner` (the responsible person or source), and `resume_when`. Section 23.5 defines the wait record, and the state document records it in the field `wait` (Section 25.1).

An overdue wait (Section 23.5) is shown as a warning in every status report and names the owner who must act (Section 23.8). Nothing happens automatically.

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

A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition, and the human closes the change as failed or records an override (Section 24.7).

The obligation to terminate of this section does not cover a retry limit: reaching one pauses the flow for a human disposition and does not end it by itself.

### 12.1 Typical Fail Categories

Typical fail conditions are a critical technical or security error, data loss or repository corruption, an unauthorized breaking change, a violation of the constitution or an ADR, an action outside the approved scope, exceeding a hard budget limit, an unrecoverable build or migration state, and permanently unsatisfiable acceptance conditions.

A gate that cannot be evaluated is not a failure and does not count toward a retry limit (Section 24.2). A retry limit is a soft fail condition (Section 24.7). The approved scope is the allowed path list of Section 24.5: a path that changed since the base revision and lies outside it is a hard failure.

### 12.2 Mandatory Content of a Fail Rule

Every fail rule MUST state its trigger and its severity, `hard` or `soft` (Section 24.7). Section 23.3 states what a fail gate holds, and Section 24.7 fixes the response to an active fail condition.

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

An existing ADR MUST only be changed or replaced through an explicitly approved change flow. See AE-009.

An implementation MUST offer the `conflict` action (Section 23.4) for steps 1 to 4: the agent names the two documents that disagree and gives a text, and the implementation records an unanswered question for the owner of the change, puts the change into the state `waiting` with a wait record of kind `question`, and names the two documents in the question. The change cannot close while the question is unanswered (Section 24.8). An agent that does not use the action is still bound by the steps above; the action makes the stop visible and does not replace the duty. See AE-314.

**AE-314 — The conflict action stops the change and names both documents**

Given an `active` change whose requirement R2 conflicts with the accepted ADR `ADR-004`  
When the agent requests the `conflict` action with the documents `spec.md` and `docs/adr/ADR-004.md` and the text `R2 conflicts with ADR-004`  
Then the change is `waiting` with a wait record of kind `question`, the question Q1 names both documents, and a `close` request answers `blocked` while Q1 is unanswered

**AE-009 — An agent stops on a conflict with an accepted ADR and returns the requirement**

Given an `active` change whose requirement R2 states that jobs are kept in a message queue, and an accepted ADR that fixes a database table as the place where jobs are kept  
When the agent finds that R2 conflicts with the ADR  
Then the agent documents the conflict in the requirement or the specification, stops planning or implementation, returns R2 to the requestor, and requests a decision, it communicates and references the decision once it is made, and the ADR is neither changed nor replaced except through an explicitly approved change flow

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
- risk or criticality,
- affected artifact type,
- local strengthening in the change specification.

The `lean` compliance profile MAY omit Pair Review. Governed or regulated compliance profiles SHOULD require it for relevant high-impact changes.

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

A Pair Review cycle is bounded. It consists of one review round and at most one re-check. A cycle MUST:

1. identify the Requestor and Reviewer,
2. define the review scope and criteria,
3. preserve a stable reviewable work product,
4. record findings with severity and status,
5. return findings to the Requestor,
6. record the disposition of each finding,
7. preserve the final review result as evidence.

In the **review round**, the Reviewer reports every finding that the scope and criteria cover. The decision owner is the person who owns the repository of the project, or the person that the review scope names as the decision owner; neither the Requestor nor the Reviewer is the decision owner of its own work. The decision owner then marks each finding `fix`, `defer`, or `reject`, with a reason. The Requestor applies the findings marked `fix`.

In the **re-check**, the Reviewer checks only the findings marked `fix` and reports each as `verified` or `open`. The re-check MUST NOT raise a finding about text that the review round covered. It MAY raise a finding about a defect that a fix itself introduced.

The cycle ends with the re-check, or with the review round when no finding is marked `fix`. A finding that is `open` after the re-check is dispositioned by the decision owner as `accepted` or `deferred`; it does not start another review round. A further review of the same work product requires a new review cycle that the decision owner approves explicitly. The decision owner MAY overrule the bound of this section by an explicit instruction that orders further review rounds or re-checks, and the history of the change MUST record the instruction.

See AE-010.

**AE-010 — A Pair Review cycle has one review round and at most one re-check**

Given a change with a required Pair Review whose Requestor is the participant `agent-a` and whose Reviewer is the distinct participant `reviewer-b`, the review scope `spec.md` with the criterion that every requirement is verifiable, the reviewed work product fixed as the exact revision `r12`, and a review round in which the Reviewer reports the findings `F-1` and `F-2`, where the decision owner marks `F-1` as `fix` and `F-2` as `defer`
When the Requestor applies the fix for `F-1`, and the Reviewer then performs the re-check, and the Reviewer also wishes to raise a new finding about text that the review round covered
Then the re-check checks `F-1` only and reports it as `verified` or `open`, the new finding is not accepted into the cycle, `F-2` stays deferred, the cycle ends with the re-check, and the final review result is preserved as evidence

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

Unresolved blocking findings MUST block the applicable completion or transition gate unless they are formally dispositioned by an authorized decision owner. See AE-011.

**AE-011 — An unresolved blocking finding blocks the gate until it is formally dispositioned**

Given two changes with a Pair Review whose finding `F-1` has the severity `blocking`, where `F-1` has the status `open` in the first change, and `F-1` has the status `accepted` in the second change with a disposition rationale that an authorized decision owner recorded  
When the completion of each change is requested  
Then the unresolved blocking finding blocks the completion of the first change, and the finding of the second change does not block it, because an authorized decision owner formally dispositioned it

### 14.5 Review Artifacts

The result of a Pair Review is kept in one place: `review.md` in the change directory, and the history of the change records the content hash of `review.md` (Section 25.2) when the decision owner approves the review result with the approval target `review` (Section 23.4). `review.md` is conditional: a change without a required Pair Review has none.

`review.md` has a fixed layout so that a done gate of the kind `review` (Section 23.3) can read it. It holds the eight-field evidence record below and, for each finding, a row with these columns: finding ID, severity, decision of the decision owner (`fix`, `defer`, or `reject`), reason, and status (`verified`, `open`, `accepted`, or `deferred`). A `review.md` that does not follow this layout is not a review report.

Review findings are not requirements and do not override higher-ranking artifacts. A finding that requires a requirement or architecture change MUST trigger the appropriate specification or ADR workflow.

Regardless of where it is stored, a portable Pair Review evidence record MUST capture exactly these eight fields: participant; role (`Requestor` or `Reviewer`); reviewed revision (the exact artifact revision reviewed); action (the review action taken); timestamp; result; findings (a reference to or summary of the findings); and disposition. This evidence-record field set is distinct from, and complements, the per-finding fields in Section 14.4.

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

In a `core` change the evidence is the evidence commands of the requirements and the results that the history of the change records for them (Section 24.9).

---

## 16. Minimum Templates

The form of `spec.md` and `change.yaml` of a `core` change is Section 23.1. The templates of `project-brief.md`, `architecture.md`, and `roadmap.md` are the files `.ggsad/templates/project-brief.template.md`, `architecture.template.md`, and `roadmap.template.md`. The templates of `plan.md`, `tasks.md`, `evidence.md`, and the `full` form of `spec.md` (former Sections 16.1 to 16.4) are in `GG-SAD_full_profile_deferred.md`.

## 17. Combination Contracts

This section describes a future capability (Section 1). It is described and not built, and an implementation refuses to start in combination mode (Section 1).

Each external integration will have to define a mapping contract containing:

- integration name and version,
- purpose and owned capabilities,
- mapped GG-SAD artifacts and states,
- authoritative source for each mapped fact,
- allowed read and write scopes,
- gate and approval interaction,
- state synchronization rules,
- failure, rollback, and uninstall behavior.

GG-SAD MAY be combined with methods such as GSD, OpenSpec, Spec Kit, or BMAD and with tools such as Hermes or Kiro. These names are examples, not normative dependencies.

An integration mapping will be layer 5 of the resolution of Section 5.3, which is not active today. It MUST NOT weaken a higher layer, and it adds no gate to a `core` change.

## 18. GG-SAD Memory Model

GG-SAD MAY provide a project memory. Until a reference implementation exists, memory is an optional capability and MUST NOT replace governing documents.

The memory MUST support at least these record types:

- **Decision** — scoped product, process, implementation, or operational decisions that are not architecture decisions;
- **Learning** — reusable knowledge derived from delivery or operation;
- **Failure** — failed approaches, incidents, causes, mitigations, and prevention guidance;
- **Definition** — glossary terms, domain language, abbreviations, and canonical meanings;
- **External Source** — referenced external information with provenance, retrieval date, relevance, and trust metadata.

Architecture decisions MUST remain ADRs. A memory decision MUST NOT be used to avoid the ADR process. When a memory record and an accepted ADR disagree, the ADR governs and the memory record MUST be marked `outdated`.

Each record type has a small template with these fields: date, title, one sentence, and a link to the source. A record MAY carry more fields (below); these four are the minimum.

Memory records MUST include stable IDs, scope, provenance, status, timestamps, and links to related artifacts. Retrieval MUST respect project permissions and the active compliance profile.

## 19. Agent Execution Algorithm

An AI agent MUST use the following process for every active change:

```text
1. Load the project brief, project-wide rules, relevant ADRs, architecture, active compliance profile, and applicable memory records.
2. Determine the state, goal, and scope of the change.
3. Evaluate the fail gates, then the wait gates, then the done gates (Section 23.6).
4. If the change may close, preserve the evidence and close it.
5. Perform changes exclusively within the approved scope.
6. After every relevant change, verify specification, architecture, and policy compliance.
7. On conflict, uncertainty, or missing approval, enter a controlled wait state.
8. Before closing, perform a final drift and evidence check.
```

In step 3, a gate that cannot be evaluated is neither failed nor satisfied: the change waits, as Section 24.2 states.

In step 5, the approved scope is the allowed path list, and it is measured as Section 24.5 states. The preservation of the evidence in step 4 is Section 24.9, and the change ends through the `close` action of Section 23.4. See AE-012.

**AE-012 — An agent closes through the gates of Section 23.6**

- Covers: Sections 19 and 20

Given an `active` change whose done gates are all satisfied and for which no fail gate and no wait gate is active
When an agent follows the execution algorithm of Section 19 and the completion criteria of Section 20
Then the agent evaluates the gates of Section 23.6, and the change ends through the `close` action in the state `closed` with the outcome `done`

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

Most of these prohibitions are conduct and not checks. The implementation enforces only these: the scope (Section 24.5), the gates (Sections 23.6 and 24.2), the human-only actions (Section 24.3), the frozen gate definitions (Section 24.1), the history (Section 24.4), the open questions (Section 24.8), and the executable evidence (Section 24.9). The approval summary (Section 24.1) lists which rules the implementation enforces and which are conduct only, so that the owner knows what the approval relies on.

When an agent closes a change, it MUST hand in an agent report with the closing request: the errors it saw, the decisions it returned to the owner, and the exceptions it recorded. The history records the report. A closing request from an agent without it MUST be rejected with the issue code `agent-report-missing`. When a human closes a change, the report is optional, and the status report shows `no agent report` where there is none (Section 23.8).

---

## 20. Completion Criteria for a Change

A change is closed with the outcome `done`, representing successful completion, only when all of the following conditions are satisfied. A change MAY also end with the outcome `failed` or `cancelled` under Section 23.2; those outcomes are not gated by this list.

- no fail condition is active,
- no wait condition is active,
- no soft failure awaits a human disposition (Section 24.7),
- no open question is unanswered (Section 24.8),
- all done gates are satisfied,
- the executable evidence of every requirement is complete (Section 24.9),
- required Pair Review cycles are complete and blocking findings are resolved or formally dispositioned, which a done gate of the kind `review` checks (Section 23.3),
- a human performs the closing, unless the change definition declares `agent_may_close` (Section 23.1),
- the final outcome is documented traceably.

Each of these conditions has a counterpart in Section 23. An active fail condition is a fail gate that decides, an active wait condition is a wait gate that decides or a gate that cannot be evaluated, and a soft failure that awaits a human disposition is a fail gate of the severity `soft` (Section 23.6). An unanswered question is the unanswered question gate, and the executable evidence is the incomplete evidence gate (Section 23.7). The final outcome is the outcome of the change (Section 23.2). The change is completed by the `close` action of Section 23.4, which ends it in the state `closed` with the outcome `done`. See AE-012.

---

## 21. Quick Reference

```text
Goal
  ↓
open ──start──> active ──close──> closed (done)
                  │  ↑
               wait│  │resume
                  ↓  │
                waiting
Any state before closed: fail, cancel, supersede ──> closed (failed | cancelled)
```

The gates decide the transitions: a fail gate ends the change, a wait gate pauses it, and the done gates allow it to close (Section 23.6).

Leading source of truth:

```text
Constitution
→ ADRs
→ Project Brief
→ Architecture
→ Change Spec
→ Code and Tests
→ Evidence
```

GG-SAD does not optimize for maximum documentation volume. It optimizes for **clear goals, controlled transitions, and verifiable outcomes**.

## 23. The `core` Profile

This section specifies the `core` method profile (Section 5.6). The protections of Section 24 and the state definitions of Section 25 apply to a `core` change as those sections state. Sections 1 to 22 apply to a `core` change.

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
- `id`: the identifier of the change, which follows the syntax of Section 4.3 and is unique among the changes of the project;
- `method_profile`: the method profile of the change, which is `core` (Section 5.6);
- `compliance_profile`: the compliance profile of the change (Section 5.1), which Section 5.6 requires to equal the active compliance profile of the project;
- `author` and `owner`: the participant that wrote the change and the participant responsible for it;
- `goal`: with `problem`, `done_when`, and `non_goals`, as Section 3.1 requires;
- `scope`: with `allow`, the list of path patterns the change MAY touch (Section 24.5);
- `requirements`: the requirements of the change, each with text, examples, the `done_when` sentences it covers, and evidence commands (Section 24.9);
- `gates`: with the three lists `fail`, `wait`, and `done` (Section 23.3).

The change definition MAY contain `required_tools`, the approved list of programs that its commands need (Section 24.2), and `agent_may_close`, which is `true` when an agent MAY close the change as `done` (Section 23.4). Both are part of the gate definitions and are fixed with them (Section 24.1). A change definition without `agent_may_close` means that only a human closes the change as `done`.

Each sentence of `done_when` MUST be covered by at least one requirement, and each requirement MUST list the `done_when` sentences that it covers. The approval of the gate definitions MUST be rejected with the issue code `done-when-uncovered`, whose message names the sentences, while a `done_when` sentence is not covered by a requirement that has at least one evidence command or a human check (Section 24.9). The check is structural: the implementation cannot judge whether the command proves the sentence, and the human who approves reviews that. See AE-315.

**AE-315 — A done-when sentence without an evidence command refuses the approval**

Given a change whose `done_when` holds the sentences S1 and S2, where S1 is covered by the requirement R1 with one evidence command and S2 is covered by no requirement  
When a human approves the target `gates`  
Then the approval is rejected with the issue code `done-when-uncovered` that names S2, and no approved hash is recorded

The change definition MAY contain `follows`, the identifier of one earlier change that this change continues, which follows the syntax of Section 4.3. The change named in `follows` MUST exist and MUST be in the state `closed`. The field is a reference only: it never changes the state or the outcome of the named change. A **follow-up** is a new change that an implementation creates with `follows` set to a closed change and with the goal and the scope pre-filled from the closed change. It is an ordinary change in every other respect: it has its own identifier, its own approval, and its own history.

The invariant core of Section 3.7 applies to a `core` change: the goal is `goal`, the specification anchor is `spec.md`, gate evaluation is Section 23.6, evidence is the requirement evidence of Section 24.9, controlled wait and fail behavior are Sections 23.5 and 24.7, and the traceable final status is the outcome of Section 23.2.

A human MUST NOT edit the state document by hand. An implementation MUST detect a state document that does not match the recorded history of the change and MUST NOT act on it (Section 24.4). See AE-013.

**AE-013 — Refuse a state document edited by hand**

Given a `core` change whose `state.json` was edited by hand after the last recorded action  
When any action that changes state is requested  
Then the implementation detects that the state document does not match the recorded history and refuses to act

### 23.2 States and Outcomes

A `core` change is always in exactly one of four states:

- `open`: the change exists and has not started;
- `active`: the change has started and work is in progress;
- `waiting`: the change is paused by a wait record (Section 23.5);
- `closed`: the change has ended.

A `closed` change has exactly one of three outcomes:

- `done`: the change was completed successfully by the `close` action;
- `failed`: the change ended unsuccessfully, because a hard fail condition was active or because a human disposed of a soft fail condition with the `fail` action, or with the `cancel` or `supersede` action while the change awaited that disposition (Section 24.7);
- `cancelled`: the change was ended by the `cancel` or `supersede` action, when no hard fail condition was active and the change did not await the disposition of a soft fail condition (Section 23.4).

The state document records the state in the field `state` and the outcome in the field `outcome` (Section 25.1). An outcome exists only when the state is `closed`; in every other state the outcome is `null`. An outcome of `failed` MUST carry a reason text, which the state document records in the field `reason` of the `after` record (Section 25.1). See AE-014, AE-026, AE-082.

When a change is created, its record MUST show the state `open`, the outcome `null`, no approval, no question, no wait record, and no base revision.

A `closed` change is final: no action changes its state or its outcome. Follow-up work is a new change that names the closed change in `follows` (Section 23.1). See AE-015.

**AE-014 — The outcome exists only when closed**

Given an `active` change whose outcome is `null`  
When the `close` action succeeds  
Then the state is `closed` and the outcome is `done`, and no change in any other state has an outcome

**AE-015 — A closed change is final**

Given a `core` change that is `closed` with the outcome `cancelled`  
When the `start` action is requested for it  
Then the request is rejected, and the state and the outcome do not change

### 23.3 Gates

The field `gates` of a `core` change holds three lists:

- `fail`: fail gates, each stating a condition under which the change has failed;
- `wait`: wait gates, each stating a condition under which the change pauses: while the condition is active, the change does not start, resume, or close;
- `done`: done gates, each stating a condition that MUST be satisfied before the change closes with the outcome `done`.

There is no ready gate. Readiness to start is a precondition of the `start` action (Section 23.4).

A fail gate and a wait gate have no kind. Each has a `condition`, a mapping that holds exactly one of the members `command`, `retry_limit`, and `predicate`:

- `command`: the argument list of a check command (Section 24.2). The condition also holds the member `exit_map`, and it MAY hold the member `time_limit`. The gate is active when the command ends with an exit status that the exit map maps to `satisfied`.
- `retry_limit`: a mapping with the members `gate` and `limit`, for a fail gate only. The member `gate` is the identifier of a done gate of the kind `check`, and the member `limit` is the limit of Section 24.2. The gate is active when the retry limit is reached. The identifier named by `gate` MUST be the identifier of a done gate of the kind `check` of the same change, and a definition whose retry limit names none is rejected.
- `predicate`: the name of a built-in predicate. A fail gate MAY name `scope-violation`, and a wait gate MAY name `unanswered-question` or `stale-spec-approval`. Section 23.7 defines them.

A condition that holds none of these members, that holds two or more of them, that holds another member, or that names a predicate which is not listed for the kind of the gate MUST be rejected. The rules about the kind of a gate apply to done gates only.

A `core` fail gate holds an `id`, a `severity`, and a condition. It states no required response, no permitted preservation actions, and no documentation: the response to an active fail gate is fixed by Section 24.7, a closure as failed for the severity `hard` and a wait for a human disposition for the severity `soft`, and the preservation of the history and the evidence is the work of Sections 24.4 and 24.9.

Every gate has an `id` that is unique within the change, including the base gates of Section 23.7. A fail gate has a `severity`, which is `hard` or `soft` (Section 24.7), and a fail gate without a severity is invalid. A done gate has exactly one kind: `check`, a command evaluated as Section 24.2 defines; `sign-off`, satisfied by an approval of that gate recorded by a human (Section 24.3); or `review`, satisfied by a complete review report. A done gate of the kind `review` is satisfied only when all of these hold: `review.md` exists in the change directory and follows the layout of Section 14.5; the history records its content hash; every finding of the severity `blocking` or `critical` has a decision of the decision owner; and every finding marked `fix` is `verified`, or is `open` and dispositioned `accepted` or `deferred`. The gate is not satisfied otherwise, and the record names what is missing. The gate reads the file at the closure and checks its content hash against the one that the approval with the target `review` recorded; a `review.md` edited after that approval does not satisfy the gate until the decision owner approves it again. The read-only action `review` (Section 23.4) is not a kind of gate. A change definition with a duplicate gate identifier, a done gate without a kind, a done gate with more than one kind, a done gate of another kind, or a fail gate without a severity MUST be rejected. See AE-016, AE-316.

**AE-016 — A done gate of an unknown kind is rejected**

Given a change definition with the done gate `code-review` of the kind `peer`, and a second change definition with the done gates `tests-pass` of the kind `check`, `legal-ok` of the kind `sign-off`, and `code-review` of the kind `review`
When the `new` action receives each of them
Then the first definition is rejected, because a done gate of the kind `peer` is not a kind of this specification, and no change is created, and the second definition is accepted

**AE-316 — A review gate needs a complete review report**

Given an `active` change with the done gate `code-review` of the kind `review`, and a `review.md` in which the finding `F-1` of the severity `blocking` has no decision of the decision owner  
When the `close` action is requested  
Then the gate is not satisfied, the record names `F-1` as missing a decision, and the change does not close

### 23.4 Actions and Transition Table

A `core` change changes state only through the actions of the table below. An action requested from a state that the table does not list under Legal From MUST be rejected (Section 22.3). If a precondition of a row is not met, the transition of that row does not occur.

| Action | Legal From | Precondition | Resulting State |
|---|---|---|---|
| `new` | No change with the given identifier exists | The change definition is valid under Sections 23.1 and 23.3, its method profile is selected under Section 5.6, its identifier follows the syntax of Section 4.3 and is unique, and `follows`, when present, names a closed change. | The state `open` with the outcome `null` and the initial record of Section 23.2, and the anchor at position 1 where an anchor is kept or required (Section 24.4). |
| `approve` | Any state except `closed` | The approval has one target. For `spec`, no question is unanswered (Section 24.8) and `spec.md` carries the conflict line (Section 4). For `gates`, the gate definitions are valid under Section 23.3 and every `done_when` sentence is covered (Section 23.1). For `review`, `review.md` follows the layout of Section 14.5 and every finding of the severity `blocking` or `critical` has a decision of the decision owner; the approval records the content hash of `review.md`. For `documents`, the recorded hashes of the higher-ranking documents differ from the current ones (Section 4). For `all`, the conditions of `spec` and `gates` hold. For `override`, a soft fail condition awaits disposition (Section 24.7), and the approval gives a reason and at least one further attempt. For a named gate, the gate is a `sign-off` done gate of the change. Section 24.1 governs the re-approval of changed gate definitions. | The state and the outcome do not change, and the approval is recorded. See AE-018, AE-019, AE-020. |
| `start` | `open` | The gate definitions are approved and unchanged since approval (Section 24.1), the specification is approved when the compliance profile or the project configuration requires it, the revision from which the change starts can be recorded (Section 24.5), the working copy holds no uncommitted work other than the record files of the change (Section 24.5), and none of the steps 1 to 4 of Section 23.6 would decide, so that a fail gate that is active, a gate that cannot be evaluated, or a wait gate that is active prevents the start. | The state `active`, with the base revision recorded. See AE-021. |
| `wait` | `active` | A reason, an owner, and a resume condition are given, or an unanswered question is named. A named question exists and is unanswered, and the action never creates a question. When a question is named, the owner of the wait is the owner of the question and a different owner is rejected, and the reason and the resume condition default to awaiting the answer to the question (Section 24.8). | The state `waiting`, with a wait record of kind `manual`, or of kind `question` when the action names a question (Section 23.5). See AE-022. |
| `ask` | `open`, `active`, `waiting` | The question has a text and an owner, which defaults to the owner of the change. A structured question has at least two distinct options. | The state does not change, and an unanswered question with the next identifier is recorded (Section 24.8). In the state `waiting`, the wait record does not change, and the change cannot resume until the question is answered (Section 23.7). |
| `answer` | Any state except `closed` | The question exists and is unanswered. The answer comes from the owner of the question. A structured question receives one of its options, and a free-text question receives a text. | The state does not change, and the question is recorded as answered. An answer does not resume a waiting change by itself. The request MAY carry `and_resume`: when the answerer is allowed to resume (Section 24.3) and the change waits for this question, the answer and the `resume` are one step, and both are recorded. Otherwise the status report says `ready to resume` and names who can resume (Section 23.8). See AE-023. |
| `resume` | `waiting` | The resume condition of the wait record is satisfied (Section 23.5). For a wait record of kind `manual`, the request carries a note of one sentence that says what happened, and the history records it; a request without the note is rejected. | The state `active`, when the evaluation of Section 23.6 finds no gate that decides otherwise. Otherwise the change remains `waiting`, or becomes `closed` with the outcome `failed`, as Section 23.6 decides. |
| `close` | `active` | The evaluation of Section 23.6 finds no fail gate and no wait gate active, and every done gate is satisfied. A closing that would end in `done` is performed by a human, unless the change definition declares `agent_may_close` (Section 23.1). A closing by an agent carries the agent report (Section 19.1). | The state `closed` with the outcome `done`. When the evaluation finds otherwise, the change does not close: it remains `active` when a wait gate is active or a done gate is not satisfied, becomes `waiting` when Section 23.6 requires a wait, and becomes `closed` with the outcome `failed` when a hard fail condition is active. See AE-024, AE-025. |
| `fail` | `waiting`, with a wait record of kind `fail-gate` | A soft fail condition awaits disposition (Section 24.7), and a reason text is given. | The state `closed` with the outcome `failed` and the reason recorded. See AE-026. |
| `cancel` | Any state except `closed` | An active wait does not prevent the action, and differing gate definitions do not prevent it (Section 24.1). A gate that cannot be evaluated determines no failure and does not prevent it (Section 24.2). | The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active or when the change awaits the disposition of a soft fail condition, that is, when it is `waiting` with a wait record of kind `fail-gate` (Section 24.7). The actor MAY give a reason text with the action. When the outcome is `failed` because of a soft fail condition, the reason text of the outcome is the reason that the actor gave or, when the actor gave none, a text that names that soft fail condition (Section 25.1). See AE-027. |
| `supersede` | Any state except `closed` | The preconditions of `cancel` hold, including that differing gate definitions do not prevent the action (Section 24.1), and `replaced_by` names a different change that exists and is not `closed`. The action is performed by a human and records a reason. | As `cancel`, with `replaced_by` recorded in the closed change. |
| `adopt` | Any state | The history of the change has no anchor (Section 24.4). | The state and the outcome do not change, and the anchor is created from the history as it is. See AE-028. |
| `conflict` | `active` | Two documents are named and a text is given (Section 13.1). The owner of the question is the owner of the change. | The state `waiting`, with a wait record of kind `question`, and an unanswered question that names the two documents. See AE-314. |
| `repair` | Any state | The history is not consistent, or is truncated or rewritten (Section 24.4). The actor is the owner of the project and gives a written reason. | The state and the outcome do not change as a result of the repair itself, and the history continues with a `repaired` entry (Section 24.4). See AE-317. |

The actions `approve`, `fail`, `cancel`, `supersede`, `adopt`, and `repair` MUST be performed by a human participant. An `answer` to a question whose owner is a human MUST also be given by a human (Section 24.3). See AE-020.

The actions `check`, `review`, `guard`, and `check-scope` (Section 22.4) are read-only. The action `check-scope` reports at any time, without changing anything, whether the paths changed since the base revision lie inside the allowed path list (Section 24.5), so that an agent or a hook finds a scope violation early. The status report shows the same early warning (Section 23.8), and the failure is still decided by the action that evaluates the gates. They report on a change, they never change its state or its history, and they are legal from every state. They are not rows of the table.

The method profile `core` has no `reopen` action. A change in the state `closed` is final, and follow-up work is a new change that names the closed change in `follows` (Section 23.1).

A `follows` field is a reference and not a state transition: it never changes the state or the outcome of the change that it names, so that no `core` change leaves the state `closed`. A new change whose `follows` names a change that has not ended, because that change is `open`, `active`, or `waiting`, or that names a change that does not exist, is rejected, and nothing is written.

**Rejected and Blocked Results per Action (`core`)**

| Action | Answers `rejected` (nothing is written, `changed` is `false`) | Answers `blocked` (the evaluation is recorded, `changed` is `true`) |
|---|---|---|
| `new` | The change definition is invalid, the identifier does not follow the syntax of Section 4.3 or is not unique, `follows` does not name a closed change, or no method profile is selected. | Never. |
| `approve` | The target is invalid or its preconditions are not met, the approver is not a human where Section 24.3 requires one, or the gate definitions differ from the approved ones and the target is not the gate definitions (Section 24.1). | Never. |
| `start` | The state is not `open`, or a precondition is not met, including a fail gate, a wait gate, or a gate that cannot be evaluated that would decide against the start (issue code `start-blocked`), or uncommitted work other than the record files of the change (issue code `working-copy-unclean`, whose message lists the paths). | Never. |
| `wait` | The state is not `active`; or the reason, the owner, or the resume condition is missing and no question is named; or the named question does not exist, is already answered, or has another owner than the owner given. | Never. |
| `ask` | The state is not `open`, `active`, or `waiting`, or the question is not valid. | Never. |
| `answer` | The state is `closed`, the question does not exist or is already answered, or the answer is not valid or not given by the owner of the question. | Never. |
| `resume` | The state is not `waiting`, or the resume condition of the wait record is not satisfied, or the wait record is of kind `manual` and the request carries no note. | The evaluation of Section 23.6 finds a gate that keeps the change waiting. |
| `close` | The state is not `active`; or an agent requests a closing that would end in `done` and the change definition does not declare `agent_may_close` (issue code `human-close-required`); or an agent requests the closing without the agent report (issue code `agent-report-missing`). | The evaluation of Section 23.6 finds a wait gate active, a done gate not satisfied, a soft failure, or a gate that cannot be evaluated, so that the change does not close. |
| `fail` | The state is not `waiting` with a wait record of kind `fail-gate`, or no reason is given. | Never. |
| `cancel` | The state is `closed`. | Never. |
| `supersede` | The state is `closed`, or `replaced_by` is missing, names the change itself, or names a change that does not exist, or names a change that is `closed`. | Never. |
| `adopt` | The history already has an anchor. | Never. |
| `conflict` | The state is not `active`, or fewer than two documents or no text is given. | Never. |
| `repair` | The history is consistent and complete, or the actor is not the owner of the project, or no reason is given. | Never. |

A `close` or a `resume` whose evaluation finds a fail gate of the severity `hard` active answers `success` with the state `closed` and the outcome `failed` (Section 24.7). An action answers `blocked` only where this table lists a case. See AE-017.

Section 24.2 states what `cancel` and `supersede` answer when a gate that applies to them cannot be evaluated: they take effect, and the result `not_evaluable` is recorded.

**AE-017 — A close that triggers a hard failure answers success**

Given an `active` `core` change with a fail gate of the severity `hard` that is active  
When the `close` action is requested  
Then the result is `success`, the state is `closed`, and the outcome is `failed`

**AE-018 — Approve the specification and the gates together**

- Covers: Section 23.4 (`approve`)

Given an `open` change with valid gate definitions and no unanswered question  
When a human approves the target `all`  
Then the approvals of the specification and of the gates are recorded, and the state remains `open`

**AE-019 — Reject the approval of a specification with an unanswered question**

- Covers: Section 23.4 (`approve`)

Given an `open` change with the unanswered question Q1  
When a human approves the target `spec`  
Then the action is rejected, no approval is recorded, and Q1 remains unanswered

**AE-020 — Reject the approval of a sign-off gate by an agent**

- Covers: Section 23.4 (`approve`)

Given an `active` change with the `sign-off` done gate `legal-ok`  
When an AI agent requests the approval of the gate `legal-ok`  
Then the action is rejected, because an approval MUST be performed by a human, and the gate remains unsatisfied

**AE-021 — Reject the start of a change whose gates are not approved**

- Covers: Section 23.4 (`start`)

Given an `open` change whose gate definitions are not approved  
When the `start` action is requested  
Then the action is rejected, and the change remains `open` with no base revision

**AE-022 — Wait for the answer to a question**

- Covers: Section 23.4 (`wait`)

Given an `active` change with the unanswered question Q1  
When the `wait` action names Q1, the owner of Q1, and the resume condition `Q1 answered`  
Then the state is `waiting`, and the wait record has the kind `question` and names Q1

**AE-023 — Answer a structured question**

- Covers: Section 23.4 (`answer`)

Given an `active` change with the unanswered structured question Q1 whose options are `keep` and `drop` and whose owner is a human  
When that human answers Q1 with `keep`  
Then Q1 is recorded as answered with `keep`, and the state remains `active`

**AE-024 — Close a completed change**

- Covers: Section 23.4 (`close`)

Given an `active` change with every done gate satisfied and no fail gate or wait gate active  
When the `close` action is requested  
Then the state is `closed` and the outcome is `done`

**AE-025 — Do not close with an unsatisfied done gate**

- Covers: Section 23.4 (`close`)

Given an `active` change with one done gate that is not satisfied  
When the `close` action is requested  
Then the change does not close, remains `active`, and has the outcome `null`

**AE-026 — Fail a change that awaits disposition of a soft fail**

- Covers: Section 23.4 (`fail`)

Given a `waiting` change with a wait record of kind `fail-gate` for a soft fail condition  
When a human performs the `fail` action with the reason `retry limit reached`  
Then the state is `closed`, the outcome is `failed`, and the reason `retry limit reached` is recorded

**AE-027 — Cancel with a hard fail condition active**

- Covers: Section 23.4 (`cancel`)

Given an `active` change with a hard fail condition active  
When a human performs the `cancel` action  
Then the state is `closed` and the outcome is `failed`, not `cancelled`

**AE-028 — Adopt an unanchored history**

- Covers: Section 23.4 (`adopt`)

Given a change whose history has no anchor  
When a human performs the `adopt` action  
Then the anchor is created from the history as it is, and the state and the outcome do not change

### 23.5 Wait Records

A `core` change has at most one wait record, and the wait record exists exactly while the state is `waiting`. A wait record contains:

- `kind`: one of `question`, `manual`, `fail-gate`, and `external`;
- `reason`: why the change waits;
- `owner`: the participant or source expected to act;
- `resume_when`: the condition under which the `resume` action is legal;
- `expires`: OPTIONAL, an instant after which the wait is overdue;
- `question`: the identifier of the awaited question, present when the kind is `question`.

The kind of a wait record depends on how it came to exist:

- `question`: the `wait` action named an unanswered question (Section 24.8);
- `manual`: the `wait` action named no question;
- `fail-gate`: the evaluation of Section 23.6 found a soft fail condition (Section 24.7);
- `external`: the evaluation of Section 23.6 found a gate that could not be evaluated (Section 24.2).

A wait record that the evaluation creates has these values. The `owner` is the owner of the change. For the kind `fail-gate`, `resume_when` is the text `a human recorded an override of <id>`, where `<id>` is the identifier of the fail gate. For the kind `external`, `resume_when` is the text `gate <id> can be evaluated`, where `<id>` is the identifier of the gate that could not be evaluated. The `reason` names the gate and the cause. See AE-029.

The resume condition is satisfied as follows. For the kind `question`, the awaited question is answered. For the kind `fail-gate`, a human has recorded an override for the soft fail condition. For the kind `external`, the gate can be evaluated. For the kind `manual`, the owner of the wait states in the `resume` action that the condition holds, with the one-sentence note of Section 23.4.

A wait of the kind `external` ends when the cause is gone. The status report re-tests the missing approved program and shows `the cause may be gone, ready to resume` when it exists, and the `resume` action itself checks that the gate can be evaluated and is rejected with a clear message when it still cannot. Nothing resumes by itself (Section 23.8).

An overdue wait remains a wait until the change leaves the state `waiting`. It is shown as a warning in every status report, and the warning names the owner of the wait (Section 23.8).

**AE-029 — A wait record that the evaluation creates names its owner, gate, and resume condition**

Given two `active` `core` changes owned by `human:ada`, the first with a soft fail gate `flaky` that is active and the second with a `check` done gate `docs-built` whose approved program (listed in `required_tools`) is missing
When the `close` action is requested for each change
Then the first change is `waiting` with a wait record of kind `fail-gate`, the owner `human:ada`, the resume condition `a human recorded an override of flaky`, and a reason that names `flaky`, and the second change is `waiting` with a wait record of kind `external`, the owner `human:ada`, the resume condition `gate docs-built can be evaluated`, and a reason that names `docs-built` and the missing program

### 23.6 Evaluation Order

The gates of a `core` change MUST be evaluated in this order, and the evaluation MUST stop once the results of a group decide the requested action (Section 24.2):

1. A fail gate with the severity `hard` that is active decides: the change becomes `closed` with the outcome `failed`.
2. A gate whose condition could not be evaluated decides: the change becomes `waiting` with a wait record of kind `external` (Section 24.2). A condition that could not be evaluated is never a failure.
3. A fail gate with the severity `soft` that is active decides: the change becomes `waiting` with a wait record of kind `fail-gate` until a human disposes of it (Section 24.7).
4. A wait gate that is active decides: the change does not start, resume, or close.
5. For the `close` action only, a done gate that is not satisfied decides: the change does not close.

If no gate decides, the requested action takes effect. The actions `close` and `resume` apply steps 1 to 4, and `close` also applies step 5. The action `start` requires that none of the steps 1 to 4 would decide. Sections 24.2 and 24.7 refine steps 2 and 3. Section 24.2 also states that the gates are evaluated by group, that a group is evaluated whole, and that the evaluation stops after the first group that decides. A satisfied done gate does not override a fail gate or a wait gate that is active. A gate that does not apply to the requested action is not evaluated and, when gate results are recorded, is recorded as `not_applicable`. See AE-030, AE-031.

**AE-030 — A hard fail decides before the done gates**

Given an `active` change with every done gate satisfied and a fail gate with the severity `hard` active  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed`, not `done`

**AE-031 — A condition that cannot be evaluated is a wait, not a failure**

Given an `active` change with a `check` done gate whose command cannot start because its approved program (listed in `required_tools`) is missing  
When the `close` action is requested  
Then the change is `waiting` with a wait record of kind `external`, and no failure is recorded

### 23.7 Base Gates

Every `core` change has four base gates in addition to the gates in its change definition:

- the scope violation gate, a fail gate with the severity `hard` and the condition `predicate` `scope-violation`, which is active when a path changed since the base revision lies outside `scope.allow` (Section 24.5);
- the unanswered question gate, a wait gate with the condition `predicate` `unanswered-question`, which is active while any question is unanswered (Section 24.8);
- the stale specification approval gate, a wait gate with the condition `predicate` `stale-spec-approval`, which is active only if `spec.md` was approved at least once and its content hash differs from the content hash that was approved last (Section 24.3);
- the incomplete evidence gate, a done gate, which is not satisfied until the evidence of every requirement is complete (Section 24.9).

The base gates belong to the `core` method profile. They apply to every `core` change without being listed in its change definition, they MUST NOT be removed, and a lower layer of Section 5.3 MUST NOT weaken or alter them. See AE-032, AE-033.

The base gates have the identifiers `scope-violation`, `unanswered-question`, `stale-spec-approval`, and `incomplete-evidence`. A change definition that redefines one of them, or that states that one does not apply, is rejected as Section 5.3 states, at the creation of the change and again before the approval of its gate definitions. See AE-002, AE-005.

The predicate of a base gate has the identifier of the gate as its name, and the rules of Section 23.3 about the kind and the condition of a gate govern the gates of the change definition and not the base gates. The check of Section 5.3 on the identifiers of the base gates is made before the other checks of Sections 23.1 and 23.3, so that a gate with the identifier of a base gate is rejected as Section 5.3 states, whatever its condition. A specification that was never approved has no approved version from which it can differ, so that the stale specification approval gate is not active for it and does not stop the `start` action.

The specification file `spec.md` of a `core` change is protected against later edits only after it was approved: before its first approval, an edit of `spec.md` is not reported as a difference from an approved version, and `change.yaml` is the only machine-checkable anchor of the change.

**AE-032 — The scope violation gate applies without being listed**

Given an `active` change whose definition lists no gates and whose `scope.allow` is `lib/**`, and a file under `docs/` changed since the base revision  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed`, because the scope violation gate is a hard fail gate

**AE-033 — A changed specification makes its approval stale**

Given an `active` change whose `spec.md` was approved and then edited  
When the `close` action is requested  
Then the change does not close, because the stale specification approval gate is active, and it can close after a human approves `spec` again

### 23.8 Status Report

The read-only actions of Section 22.4 (`check`, `review`, `guard`, and `check-scope`) report on a change. The report writes nothing and records no failure. It starts with one line for the owner, which is one of `needs you`, `waiting on others`, or `all fine`, followed by the facts below. `needs you` is shown when a decision, an approval, a sign-off, or a disposition of the owner or of an approved human is due.

The report MUST show:

- the state, the outcome, and the results of the gates;
- who must act, for every pending item (a question, a wait, a soft failure, an approval);
- for a change that is `closed`: the reason of a cancellation and the changes that follow it (`follows`) or replace it (`replaced_by`);
- that the gates are not enforced, when the gate definitions differ from the approved ones (Section 24.1).

The report MUST show these warnings where they apply, and no warning blocks anything:

- an overdue wait, naming the owner (Section 23.5);
- a wait of the kind `external` whose cause may be gone: `ready to resume` (Section 23.5), and a wait whose question was answered by someone who may not resume: `ready to resume`, naming who can resume (Section 23.4);
- no anchor is set, so that the history protects against accident and partial tampering only (Section 24.4);
- no list of approved humans is set (Section 24.3);
- a sign-off that is stale because the gate definitions changed since the sign-off (Section 24.3);
- a path outside the allowed path list that has changed already (Section 23.4, `check-scope`);
- a baseline entry whose review date has passed (Section 24.6);
- a required project document that is missing (Section 4.2);
- an override that would lapse (Section 24.1);
- no agent report, where a human closed the change (Section 19.1).

The `guard` action keeps the five verifications and the issue codes of Section 22.4. See AE-318.

**AE-318 — The report starts with one line for the owner**

Given an `active` `core` change that waits for the answer of the owner `human:ada` to the question Q1, whose wait is overdue  
When the `check` action is requested  
Then the report starts with `needs you`, names `human:ada` as the owner who must act, shows the overdue wait as a warning, and writes nothing

---

## 24. Protections

This section specifies the protections of a `core` change. Each rule is written once in this section, and the other sections point to it.

The protections use these terms:

- **Change definition:** `change.yaml` (Section 23.1).
- **History:** `state.json` (Section 25.1).
- **Base revision:** the revision recorded when the `start` action succeeds (Section 23.4).
- **Human:** a participant that is a human person (Section 24.3).

Identifiers, path patterns, paths, and text values are compared as sequences of Unicode code points, without normalization (Section 25.1). Result names are exact lowercase strings. A rule of this section that compares values compares them in this way unless the rule states otherwise. See AE-034.

**AE-034 — Compare identifiers as code point sequences**

Given a change definition with two gate identifiers that look the same, the first written `café` with the single code point U+00E9 and the second written `cafe` followed by the code point U+0301
When the change definition is validated
Then the two identifiers are different, because values are compared as sequences of code points without normalization, and the definition is not rejected for a duplicate identifier

Every protection of Sections 24.1 to 24.10, and the result `blocked` of Section 22.2, is an invariant of the method. The table states how each is realized in a `core` change.

| Protection | Section | Realization |
|---|---|---|
| Frozen gate definitions | 24.1 | The three gate lists, the scope, and the requirement evidence commands of the change definition |
| Three-valued gate results | 24.2 | Every fail, wait, and done gate; a gate that cannot be evaluated puts the change in a wait of kind `external` |
| Identity and human-only actions | 24.3 | The approvals, sign-offs, overrides, answers, and the actions `fail`, `cancel`, `supersede`, `adopt`, and `repair` of Section 23.4, and the list of approved humans |
| History consistency and completeness | 24.4 | `state.json` |
| Scope and isolation | 24.5 | `scope.allow` of the change definition, and the base revision recorded when `start` succeeds |
| Known-failure baselines | 24.6 | A baseline on a `check` done gate |
| Hard and soft failure | 24.7 | The severity of a fail gate; a soft failure puts the change in a wait of kind `fail-gate` |
| Open questions as state | 24.8 | The actions `ask` and `answer` and the base gate `unanswered-question` |
| Executable evidence | 24.9 | The base gate `incomplete-evidence` |
| Gate-command interpreter | 24.10 | The commands of `check` gates and the evidence commands |
| The result `blocked` | 22.2 | The actions `close` and `resume` (Section 23.4) |

### 24.1 Frozen Gate Definitions

The gate definitions of a change are fixed when the change is approved. They are the gates of the change definition, that is, its three gate lists (Section 23.3), together with everything those gates declare (conditions, severities, retry limits, commands, exit maps, time limits, extraction rules, and baselines), the list `required_tools` and the declaration `agent_may_close` (Section 23.1), and the scope of the change (Section 24.5). The purpose is that no participant can change the gates that judge a change without a human approving the change again. Before the first approval of the gate definitions nothing is fixed, and this section stops no operation.

The identity of the fixed definitions is the content hash (Section 25.2) of the parsed gate definitions, computed over the parsed values and not over the text of the file. A comment, the layout, the order of keys in a mapping, and the quoting of a value that parses to the same value therefore do not change the identity. The order of the elements of a list does change it, because that order is part of the parsed value. The hash computed at the approval is the approved hash and is recorded in the history. See AE-036.

Every state-changing operation MUST first compute the hash of the current gate definitions and compare it with the approved hash. When the two differ, the operation MUST write nothing, and its result MUST be `rejected` with `changed` false (Section 22.2) and the stable issue code `gates-changed`, whose message states that the gate definitions differ from the approved ones and that a human has to approve them again. See AE-035.

Three operations are exempt from the comparison and MUST NOT be stopped by it: `cancel`, `supersede`, and the approval of the gate definitions that replaces the approved hash. The exemption of `cancel` and `supersede` ensures that a change whose definitions were altered can always be ended, and `supersede` behaves exactly like `cancel`: it is performed by a human and records a reason. The approval that replaces the approved hash is the re-approval; without its exemption, no change could leave this state.

The re-approval MUST be performed by a human at the assurance level that Section 24.3 requires for the approval of gates. The human is the owner of the project or an approved deputy (Section 24.3). It is recorded in the history as an amendment, not as an approval, and the record names the approved hash that it replaces and the new approved hash, and holds a short before and after of the changed gates and of the changed lines of the specification. After the re-approval the new hash is the approved hash, and an override of a soft failure that is bound to the earlier hash lapses (Section 24.7).

**Approval summary.** Before an approval is recorded, the implementation shows the human a summary, and the approval is recorded only after the human has seen it. The summary shows: what changed since the last approval, or `first approval` when there is none; for every fail gate its severity `hard` or `soft`, flagging a gate whose severity is softer than the default severity of fail gates (Section 24.7); the retry limits and the default retry limit (Section 24.7); which rules the implementation enforces and which are conduct only (Section 19.1); whether an anchor is set (Section 24.4); and, for a re-approval, any override that would lapse with the number of attempts that are left, and any sign-off that would become stale. See AE-319.

**AE-319 — A re-approval says first that an override lapses**

Given an `active` `core` change with an override of the soft failure of `tests-pass` with one attempt left, and gate definitions that were edited after the approval  
When `human:ada` starts the re-approval of the target `gates`  
Then the summary says that the override lapses with one attempt left and that the change would pause again, and the re-approval is recorded only after `human:ada` has seen it

A read-only operation does not write. While the hashes differ, it answers `rejected` with `changed` false and the issue code `gates-changed`, and it states in its report that the gates are not enforced. It never closes the change and never records a failure.

The approval of gate definitions MUST be rejected when the change definition has no gate definitions at all (no `gates` field). A definition that holds empty lists of additional gates is valid and is fixed as it is: an empty list is a definition, and a gate added to it later is a difference. See AE-037.

The requirement identifiers and the evidence commands that are bound to them are also fixed with the gate definitions (Section 24.9). See AE-064.

**AE-035 — Reject an operation when the gate definitions differ**

Given a `core` change whose gate definitions were approved, and the severity of the fail gate `no-secrets` was edited from `hard` to `soft` after the approval  
When the `close` action is requested  
Then the result is `rejected` with `changed` false and the issue code `gates-changed`, and nothing is written to the history

**AE-036 — A reordered gate list differs**

Given a `core` change whose approved done gates are `lint` followed by `tests-pass`, and the two gates were swapped after the approval  
When the `close` action is requested  
Then the hashes differ, because the order of a list is part of the parsed value, and the result is `rejected` with the issue code `gates-changed`

**AE-037 — Reject the approval of absent gate definitions**

Given a `core` change whose change definition has no `gates` field  
When a human approves the gate definitions  
Then the approval is rejected, and no approved hash is recorded

### 24.2 Three-Valued Gate Results

Every evaluation of a gate ends in exactly one of three results:

- `satisfied`: the evaluation established that the condition of the gate holds;
- `not_satisfied`: the evaluation established that the condition of the gate does not hold;
- `not_evaluable`: the evaluation could not establish either, because the gate could not be evaluated.

A done gate is met when its result is `satisfied`. A fail gate and a wait gate are active when their result is `satisfied`, that is, when the condition they describe holds. Every result is recorded in the history together with the gate it belongs to. A record of a result whose name is in another letter case, or is any other name than the three results, is not a result and MUST be rejected. The marker `not_applicable` is not a result, and it is the one other value that a record of an evaluation holds in place of a result (Section 25.1). See AE-075.

A gate cannot be evaluated when any of these holds. Without the list `required_tools`, no program is approved, so a command that cannot start is `not_satisfied`. A command that cannot start for a reason other than the missing approved program of the first item, including a program that is not on the list `required_tools` of the change (Section 23.1), is not a case of `not_evaluable`: its result is `not_satisfied`, and the record names the cause.

- the command of the gate cannot start because a program that the list `required_tools` approves is missing;
- the command exceeds the time limit that the gate declares and is stopped;
- the command ends without an exit status, or with an exit status that the exit map of the gate does not map;
- the command reports that a module, tool, or dependency it needs is missing, either through an exit status that the exit map maps to `not_evaluable` or through output that the gate declares for that purpose;
- version control is unavailable to a gate that needs it;
- the gate needs the base revision and the change has started without one (Section 24.5);
- any other exception occurs during the evaluation.

A gate that is `not_evaluable` is not a failure. Its result MUST NOT be recorded as `not_satisfied`, it MUST NOT make a fail gate active, and it MUST NOT count toward any retry limit. The record of the result MUST name the gate and the cause. See AE-038.

An action that evaluates gates decides from the results in this order, and the first rule that applies decides:

1. A fail gate with the severity `hard` that is active: the change fails (Section 24.7).
2. A gate that is `not_evaluable`: the change waits. The change is `waiting` with a wait record of kind `external` (Section 23.5).
3. A fail gate with the severity `soft` that is active: the change waits for a human disposition (Section 24.7).
4. A wait gate that is active: the change does not advance.
5. For an action that completes a change, a done gate that is `not_satisfied`: the change does not complete.

A known hard failure therefore outranks a gate that cannot be evaluated. This order refines Section 23.6. The `start` action requires that none of the rules 1 to 4 would decide: when one would, `start` is rejected and no wait is created, and a hard failure included, because `start` never closes a change (Section 24.7). When the action is `resume`, the wait record created by rule 2 replaces the earlier record, whose resume condition was met. An action that only reports on a change reports the result and creates no wait. See AE-039.

Rule 2 does not make the other actions that evaluate gates and never answer `blocked` wait, because a wait is a recorded change that they cannot answer (Section 22.2). These actions are `cancel` and `supersede`, which look for an active hard failure. When no hard failure is active and a gate that applies to one of them cannot be evaluated, `cancel` and `supersede` take effect, because an authorized cancellation is not held up by a check that cannot run and a gate that cannot be evaluated is never a failure, and the result `not_evaluable` of the gate and its cause are recorded in the entry of the action.

The gates are evaluated by group. The order of the groups is the order of Section 23.6, that is the fail gates, the wait gates, and the done gates. A group is evaluated whole: every gate of the group that applies to the action is evaluated, even when an earlier gate of the same group already decides. After a group, the evaluation stops if the results of the groups evaluated so far decide the action under the rules 1 to 5, so that a gate of a later group is not evaluated: its command is not run, and no result is recorded for it. The rules rank the results of the gates that were evaluated, so that a gate which is not evaluated cannot outrank a gate which is. A wait gate that is active therefore decides before a done gate that cannot be evaluated, the change does not become `waiting` for that done gate, and the `close` action answers `blocked`. A wait gate that cannot be evaluated is `not_evaluable`, and it creates a wait record of kind `external` before any done gate is evaluated.

A retry limit is a fail condition that becomes active when the number of `not_satisfied` results recorded for a named gate reaches a limit. The count is the number of `not_satisfied` results of that gate in the history over the whole life of the change, a non-negative integer. The limit is a non-negative integer, and it is reached when the count is greater than or equal to the limit: with a limit of three, the third `not_satisfied` result reaches it and the second does not. A `satisfied` result, a `not_evaluable` result, and a `not_applicable` record are not counted, and a `not_evaluable` result between two `not_satisfied` results neither adds to the count nor resets it. A retry limit that is not a non-negative integer is invalid and MUST be rejected when the gate definitions are approved.

Every evaluation records its own result. When the cause of a `not_evaluable` result is removed and the gate is evaluated again, the new result is recorded and the earlier record remains in the history unchanged.

A check-command gate is a gate whose condition is the outcome of a command. It is a done gate of the kind `check` (Section 23.3). The definition of a check-command gate declares:

- the command as an argument list, in which the program and each argument are separate elements and no shell interprets them;
- the exit map: the exit statuses, which are non-negative integers, that mean `satisfied`; the exit statuses that mean `not_satisfied`; and OPTIONALLY the exit statuses that mean `not_evaluable`. An exit status appears at most once in the map;
- OPTIONALLY, a time limit and the rule by which failure identifiers are extracted from the output (Section 24.6).

A definition of a check-command gate without a command or without an exit map is invalid and MUST be rejected when the gate definitions are approved. An exit status that the exit map does not map is `not_evaluable`. Except for the baseline comparison of Section 24.6, the output of a command does not change the result that the exit map decides. Empty output never makes a gate `satisfied`: only an exit status that the exit map maps to `satisfied` does. This specification names no programming language, test runner, or output format. Section 24.10 governs the interpreter that runs the command.

A `command` condition of a fail gate or a wait gate (Section 23.3) is evaluated as a check command: its command and its exit map are defined and evaluated as above, and a condition without an exit map is invalid and MUST be rejected when the gate definitions are approved. Such a gate is not a check-command gate in the sense of Section 24.6, so that it carries no baseline.

`not_applicable` is not a result. It is the marker that Section 23.6 prescribes for a gate that is not evaluated by design, because it does not apply to the requested action or because the commands of gates were deliberately not run for the action. A `not_applicable` record is not a failure, does not count toward a retry limit, and is not `not_evaluable`: a gate that applies to the action and could not be evaluated is `not_evaluable`.

**AE-038 — A missing program is not a failure and consumes no attempt**

Given the `check` done gate `tests-pass`, a soft fail gate that is active when `tests-pass` has three `not_satisfied` results, and a history with two `not_satisfied` results of `tests-pass`  
When the `close` action is requested and the approved program of the command of `tests-pass` is missing  
Then the result of `tests-pass` is `not_evaluable`, the count remains two, the fail gate is not active, and the change is `waiting` with a wait record of kind `external`

**AE-039 — A hard failure is decided before a gate that cannot be evaluated**

Given an `active` `core` change with a fail gate of the severity `hard` that is active and a `check` done gate whose command cannot start because its approved program is missing  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed`, and no wait record is created

### 24.3 Identity and Human-Only Actions

Every action on a change is performed under an identity that the participant claims. A claim has an assurance level, which states how well the claim was checked. This specification fixes one level, `A0`, self-declared: no check of the claim exists. Every claim is worth exactly A0 unless a verifier establishes a higher level. The Signing Extension (`GG-SAD_signing_extension.md`) defines the higher levels `A1` and `A2` and their verifiers, and an implementation MAY verify them. An implementation that verifies none treats every claim as A0.

Verification MUST fail closed. A claim whose level cannot be established is A0, whatever the reason. An action whose required level is higher than the verified level of its claim MUST be rejected, with `changed` false (Section 22.2). A claim that carries no signature and no review is not malformed: it is a claim at A0, and it is rejected only where the required level is higher. See AE-041.

The required level of an action is the higher of two minimums: the minimum that the gate states, when the action serves a gate (a sign-off gate, or the fail condition of an override), and the minimum that the project configuration sets for the kind of action. The kinds of action are the approval of the specification, the approval and the re-approval of gate definitions, the approval of the review result, the approval of changed higher-ranking documents, the sign-off of a gate, an override, an answer, `cancel` and `supersede`, `fail`, `adopt`, and `repair`. A minimum that is not stated is A0. This specification assigns no minimum to a compliance profile (Section 5.1): a compliance profile reaches a level only through a gate or through the project configuration.

For the kinds of action that an approval record covers, which are the approval of the specification, the approval and the re-approval of gate definitions, the approval of the review result, the approval of changed higher-ranking documents, the sign-off of a gate, and an override, the required level is never below the highest required level that the history of the change records in `required_level` for that kind of action. A project configuration that is lowered after an approval at a higher level therefore does not lower the level that the next action of that kind in the same change requires. The project configuration is a file of the repository, and this specification does not protect it: a participant that can change the configuration can lower a minimum for a change whose history records no earlier approval of that kind. See AE-042.

These actions MUST be performed by a human: every approval, the sign-off of a gate, an override, an answer to a question whose owner is a human, `cancel`, `supersede`, `fail`, and `adopt`. The identity of a human is written with the prefix `human:`. An identity without that prefix is not a human, and an action that requires a human MUST be rejected when the identity that performs it does not carry the prefix. The prefix is part of the claim: at A0 it is self-declared, and at A1 or A2 it is as well verified as the claim is. See AE-040, AE-108.

**Approved humans.** The project configuration holds the list of approved humans: the owner of the project and the named deputies, each with the identity written with the prefix `human:` and the account of the hosting service (a GitHub user) that belongs to it. When the list is absent, every identity with the prefix `human:` is accepted as before, and the status report warns that no list is set (Section 23.8). When the list is present, an action that requires a human MUST be rejected, with the issue code `human-not-approved`, when the identity is not on the list. Only the owner of the project changes the list. A deputy MAY give the re-approval of gate definitions (Section 24.1) and any other human-only action, but MAY NOT change the list. The history records, with every human-only action, the typed identity and the real account that the implementation reads from version control or from the hosting service, so that a difference between them is visible afterwards. The list is a file of the repository and this specification does not protect it, in the same way as the project configuration above. The Signing Extension remains optional. See AE-320.

**Resuming.** The identity that answered a question may resume the change when it is on the list of approved humans or when it is the owner of the wait record; otherwise the status report says `ready to resume` and names who can resume (Section 23.8).

**Stale sign-off.** When a re-approval of the gate definitions makes the sign-off of a gate stale, because the sign-off is bound to the earlier hash, the re-approval entry records an unanswered question that asks for the new sign-off. The owner of the question is the human who gave the earlier sign-off. The next sign-off of that gate answers the question in the same entry. The status report shows the stale sign-off (Section 23.8), and the change cannot close while the gate is not satisfied.

**AE-320 — A human name that is not on the list is rejected**

Given a project whose list of approved humans holds `human:ada` and `human:bo`, and an `open` `core` change  
When the participant `human:eve` approves the target `spec`  
Then the approval is rejected with the issue code `human-not-approved`, and the approval of `human:ada` is recorded together with her typed identity and her real account

An approval binds the exact content that is approved, and that content is identified by its content hash (Section 25.2). For the approval of the specification, the approved content is the specification of the change. For the approval of gate definitions, it is the gate definitions (Section 24.1). For the sign-off of a gate and for an override, it is the gate definitions together with the identifier of the gate or of the fail condition. The history records, for every action, the identity and the verified level, and for an approval also the content hash that was approved and the `required_level`, which is the required level that applied when the approval was accepted. The approval of the specification is stale only if the specification was approved at least once and the content hash of the current specification differs from the content hash that was approved last, and the stale specification approval gate of Section 23.7 is active in that case and in no other. See AE-104, AE-105.

No level proves that a human is present. At A0, any participant can write any identity, and an agent that is able to use a human's credentials can act as that human at every level (see the Signing Extension).

**AE-040 — Reject a human-only action under an identity that is not marked as human**

Given an `active` `core` change  
When the participant `agent:builder` performs the `cancel` action  
Then the action is rejected, because the identity does not carry the prefix `human:`, and the change remains `active`

**AE-041 — An unsigned claim is A0, not malformed**

Given an `open` `core` change in a project whose configuration sets no minimum level for approvals  
When the participant `human:ada` approves the target `spec` with no signature and no review  
Then the approval is not rejected as malformed, and it is recorded with the verified level A0

**AE-042 — A lowered minimum does not lower the level that the history already used**

Given an `open` `core` change in a project whose configuration sets the minimum level A2 for the approval of the specification, and the approval of the target `spec` by `human:ada` at A2, which is recorded with the `required_level` A2, and then a change of the configuration that lowers the minimum to A0 and a change of the specification that makes the approval stale  
When `human:ada` approves the target `spec` again with a claim at A0  
Then the approval is rejected with `changed` false, because the required level is not below A2, which the history of the change already records for the approval of the specification, and no approval is recorded

### 24.4 History Consistency and Completeness

The history of a change is an append-only list of entries, and the state of the change is read from it (Section 25.1). Every entry has four fields:

- `n`: the position of the entry, which starts at 1;
- `prev`: the hash of the entry before it. For the first entry, `prev` is the prefix `sha256:` followed by 64 digits 0;
- `body`: the content that the entry records, including the result of the action and the state of the change after it;
- `hash`: the hash of the entry, which is the hash of the canonical form (Section 25.1) of an object that holds `prev` and `body`. It is written as the prefix `sha256:` followed by the 64 lowercase hexadecimal digits of the SHA-256 digest.

The state of the change is the state that the last entry records. The state document has no other field that holds the state, so that there is no field to edit by hand in order to change it.

A history is consistent when it has at least one entry, the positions run from 1 without a gap, the `prev` of each entry equals the `hash` of the entry before it, and the stored `hash` of each entry equals the hash that is computed again from its `prev` and `body`. A history without an entry is not consistent. An implementation MUST verify the consistency of the history before it acts on a change, and MUST NOT act on a history that is not consistent.

Consistency is not completeness. Consistency says that the entries which are present form an unbroken chain. It does not say that no entry is missing: a history from which the last entries were removed is still consistent, because nothing in a chain refers forward to the entries after it. Completeness says that no entry is missing, in particular none at the end of the history, and a chain alone cannot establish it.

An anchor records the position and the hash of the latest entry of a history. It is kept at a location that is outside the working tree of the project and is not part of the history, and it is written only after the append of that entry has succeeded. After every successful append the anchor is advanced to the new latest entry. Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor or an equivalent mechanism, and an implementation MUST NOT act on a change whose history has none until a human adopts the history. An equivalent mechanism gives the verifier a record of the latest position and hash that is independent of the history, is written only after the append has succeeded, supports the three checks below, and cannot be replaced. Where no configuration requires approvals at the level A2, an implementation MAY keep an anchor. See AE-044.

The first successful append of a change, which is the entry of the `new` action, creates the anchor at position 1 where an anchor is kept or required. This creation is not a replacement, and it needs no `adopt` action. The `adopt` action serves a history that has entries and no anchor, for example a history that was written before an anchor was kept. An implementation therefore acts on a new change in a project that requires approvals at the level A2 without an `adopt` action first.

With an anchor, the verifier compares the history with it:

- a history with fewer entries than the position of the anchor is truncated, or it was rolled back to an earlier state;
- a history whose entry at the position of the anchor has a hash that differs from the hash of the anchor was rewritten;
- otherwise the history agrees with the anchor. Entries after the position of the anchor are the entries appended since the anchor was last advanced.

An implementation MUST NOT act on a history that is truncated or rewritten, and its message MUST say which of the two it found. See AE-043.

An existing anchor MUST NOT be replaced. It is only advanced, after a successful append, to the position and the hash of a later entry of the same chain. No action sets an anchor to an earlier position or to a different hash, except the `repair` action, which does so openly: it records the old anchor in the `repaired` entry before it sets the new one.

The `adopt` action creates the anchor from the history as it is, at the position and the hash of its latest entry (Section 23.4). It MUST be performed by a human at the level that Section 24.3 requires for `adopt`, and it is rejected when an anchor exists and when the history is not consistent. A human who adopts a history takes responsibility for its completeness at that moment: adoption cannot show whether entries were lost before it. See AE-044, AE-045.

**Repair.** A history that is not consistent, or that is truncated or rewritten, stops every action (above). The `repair` action (Section 23.4) is the way out. It is performed by the owner of the project with a written reason, also when an anchor exists. The implementation first shows exactly which entries are missing or wrong. It then keeps the damaged `state.json` unchanged at a location outside the change directory, which it names in the entry, replaces the history by its longest consistent prefix, and appends a `repaired` entry that records the damage found, the number of entries lost, the old anchor (position and hash), and the reason. The new anchor is set at the `repaired` entry where an anchor is kept or required. The repair never hides the loss: it records it. Adoption of an unanchored history remains the `adopt` action. See AE-317.

**AE-317 — A repair records what was lost and keeps the damaged file**

Given a `core` change with an anchor at position 8 and a history of 5 consistent entries, because the last three entries were lost  
When the owner `human:ada` performs the `repair` action with the reason `disk fault` after the implementation showed the missing entries  
Then the history continues with a `repaired` entry at position 6 that records the 3 lost entries, the old anchor at position 8, and the reason, the damaged file is kept outside the change directory, and the new anchor holds the position and the hash of the `repaired` entry

An anchor is only as strong as the location that holds it. An actor that can write both the history and the anchor can rewrite both, and every check of this section then passes. The anchor protects against an actor that can write the history and cannot write the anchor, and against accident. It does not protect against an actor that can write both. The anchor stays optional where no configuration requires approvals at the level A2. The approval summary (Section 24.1) and the status report (Section 23.8) say plainly when no anchor is set, so that the owner knows the protection is weak.

**AE-043 — A rewritten entry is detected through the anchor**

Given an anchor at position 5 with the hash of entry 5, and a history in which the body of entry 5 was edited and the hashes of entry 5 were computed again, so that the chain is consistent  
When any action on the change is requested  
Then the hash of entry 5 differs from the hash of the anchor, the history is found rewritten, and the implementation does not act

**AE-044 — A history without an anchor is refused until a human adopts it**

Given a project whose configuration requires approvals at the level A2, and a consistent history with no anchor  
When any action other than `adopt` is requested, and later a human performs `adopt` at the level A2  
Then the first request is refused, and after the `adopt` action the anchor holds the position and the hash of the latest entry and the actions are accepted

**AE-045 — Reject the adoption of an inconsistent history**

Given a history whose entry 2 was edited without a change of its stored hash, and no anchor  
When a human performs the `adopt` action  
Then the action is rejected, and no anchor is created

### 24.5 Scope and Isolation

The scope of a change is a list of path patterns, the allowed path list. A change MAY touch a path only when at least one pattern of the list matches it. The allowed path list is the field `scope.allow` of the change definition (Section 23.1). The allowed path list is part of the gate definitions and is fixed with them (Section 24.1).

A path is written relative to the root of the repository, with the character `/` as the separator. A pattern is written in the same way and is compared with a path as Section 24 states, so that letter case matters and nothing is normalized. A pattern without a wildcard names one path, and a pattern that ends with `/` names every path below that directory. In a pattern, `*` matches any sequence of characters other than `/` inside one path segment, and a segment that is exactly `**` matches any number of path segments, including none. No other wildcard exists. A pattern that is empty, that begins with `/`, or that has a path segment `..` is invalid and MUST be rejected when the gate definitions are approved.

The base revision is the revision from which the change started. It is recorded when the `start` action succeeds (Section 23.4). A change MUST NOT start when its base revision cannot be recorded: the start is rejected, and nothing is written.

The paths changed since the base revision are the paths whose content differs from the base revision according to version control, whether the difference is committed, staged, or unstaged, and the files that version control does not track and that no ignore file inside the repository, as it was at the base revision, tells it to ignore. A path changed since the base revision that no pattern of the allowed path list matches is a scope violation. A scope violation is a hard failure (Section 24.7): the change is closed as failed without human action, and the record names the paths outside the scope. See AE-046, AE-047.

The record files of the change itself are exempt from the measurement. They are the change definition, the specification, and the state document (Section 23.1). Other means detect their alteration: the hash of the gate definitions (Section 24.1), the approval of the specification (Section 24.3), and the chain of the history (Section 24.4). Exactly three further names in the change directory are exempt: the in-progress file `state.json.tmp` and the lock object `state.json.lock` that the writer of the state document uses (Section 25.1), so that a file left behind by an interrupted write is never a scope violation, and the review report `review.md` (Section 14.5), whose content hash the history records. Every other file in the change directory is measured, including a file with a similar name such as `state.json.bak`. See AE-050, AE-051.

Before the change has started there is no base revision, and the scope is not evaluated: the record shows `not_applicable` (Section 24.2). After the change has started, a scope that cannot be measured is `not_evaluable` (Section 24.2). That is the case when version control is unavailable, when no base revision was recorded, and when the allowed path list is absent. It is never recorded as `satisfied`, and it is never recorded as a scope violation.

An allowed path list that is present and empty allows no path: every path changed since the base revision is a scope violation. When no path has changed, the change is in scope, whatever the list holds.

A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement, when that ignore file was in place at the base revision and, as it was then, tells version control to ignore the file. A change can create or alter such an ignored file without a scope violation, so the allowed path list does not limit what happens in ignored locations. Only ignore files inside the repository count, and only as they were at the base revision: an ignore file that the change creates or alters hides nothing, so a path that only the created or altered ignore file hides is measured like any other path. An ignore file is an ordinary file of the working tree, such as a `.gitignore` file, so that creating or changing one is a changed path, and it is a scope violation when no pattern of the allowed path list matches it. An ignore setting kept anywhere else, such as the exclude file in the metadata directory of version control or an excludes file of the user, is not applied: a file that only such a setting hides is counted like any other file that version control does not track. The consequence for the code that gate commands run is stated in Section 24.10. See AE-048, AE-049.

Work that is uncommitted when the change starts and that does not belong to the change is a changed path like any other. The measurement counts it, and it is a scope violation when no pattern matches it. A change therefore MUST run isolated: in a working copy that is separate from other work and whose content at the start equals the base revision, apart from the record files of the change. The `start` action therefore MUST be rejected when the working copy holds uncommitted work other than the record files of the change, with the issue code `working-copy-unclean`, whose message lists the paths (Section 23.4). An implementation MUST NOT exclude such work from the measurement, and no list of paths that are known before the start exists. Ignored files stay invisible to the measurement, as above, and that gap is accepted.

**AE-046 — A changed path that a pattern matches is in scope**

Given an `active` `core` change whose `scope.allow` is `lib/**`  
When the file `lib/net/client.py` is changed and the `close` action evaluates the gates  
Then the path is in scope, and the scope violation gate is not active

**AE-047 — A path outside the scope is a hard failure**

Given an `active` `core` change whose `scope.allow` is `lib/**`, and the file `docs/guide.md` is committed after the base revision  
When the `close` action is requested  
Then the state is `closed` and the outcome is `failed` without human action, and the record names `docs/guide.md` as outside the scope

**AE-048 — An ignored file is invisible**

Given an `active` `core` change whose `scope.allow` is `lib/**`, a directory `.cache/` that an ignore file inside the repository, in place at the base revision, tells version control to ignore, and a new file `.cache/tool.py` created by the change  
When the `close` action evaluates the gates  
Then `.cache/tool.py` is not seen by the measurement, and no scope violation is found

**AE-049 — An ignore setting kept outside the repository is not applied, and an ignore file inside it is a changed path**

Given an `active` `core` change whose `scope.allow` is `lib/**`, an excludes file of the user that lists `tools/`, and the new files `tools/run.sh` and `.gitignore`, where `.gitignore` is an ignore file inside the repository that lists `build/`  
When the `close` action evaluates the gates  
Then the excludes file of the user is not applied, `tools/run.sh` is counted, `.gitignore` is a changed path, both paths are outside the scope, and the change is closed as failed

**AE-050 — The record files of the change are exempt**

Given an `active` `core` change `c-1` whose `scope.allow` is `lib/**`, and the files `specs/c-1/spec.md` and `specs/c-1/state.json` changed since the base revision, and the new file `specs/c-1/notes.md`  
When the `close` action evaluates the gates  
Then `spec.md` and `state.json` are not measured, and `specs/c-1/notes.md` is a changed path outside the scope

**AE-051 — Files left by an interrupted write are exempt and any other name is measured**

Given an `active` `core` change `c-1` whose `scope.allow` is `lib/**`, and in its directory the untracked files `state.json.tmp` and `state.json.lock` left behind by an interrupted write, and an `active` `core` change `c-3` with the same `scope.allow` and the untracked file `specs/c-3/state.json.bak`
When the `close` action evaluates the gates of `c-1` and `c-3`
Then no scope violation is found for `c-1`, because the two names are exempt, and `specs/c-3/state.json.bak` is a changed path outside the scope of `c-3`, so that `c-3` is closed as failed

### 24.6 Known-Failure Baselines

A check-command gate (Section 24.2) MAY carry a baseline: the list of failure identifiers that were already failing before the change started and that the change is not required to fix. A baseline is valid only on a check-command gate. A baseline on any other gate is invalid and MUST be rejected when the gate definitions are approved. The baseline is part of the gate definition and is fixed with it (Section 24.1): changing it requires a new approval by a human, so that a baseline cannot be used to hide a new failure. See AE-053.

Each entry of a baseline carries a written reason and a review date (`review_by`). An entry without a reason or without a review date is invalid and MUST be rejected when the gate definitions are approved. Past its review date an entry still applies, and the status report shows a warning that names the owner of the change (Section 23.8); nothing blocks. The comparison below uses the failure identifiers of the entries.

A failure identifier is a string that identifies one failure in a way that is stable across runs, for example the identifier of a failing test. The gate declares how failure identifiers are extracted from the output of its command (Section 24.2). Failure identifiers are compared as Section 24 states. The extracted identifiers form a set: an identifier that appears more than once counts once.

When the command of a gate with a baseline ends with an exit status that the exit map maps to `satisfied`, the result is `satisfied`. When it ends with an exit status that the exit map maps to `not_satisfied`, the implementation extracts the failure identifiers from the output and compares them with the baseline:

- when every extracted failure is on the baseline, the result is `satisfied`. This includes the case where the extracted failures are exactly the failures of the baseline;
- when at least one extracted failure is not on the baseline, the result is `not_satisfied`. The record names up to three of the new failures, in ascending order of their code points, and the number of new failures;
- when no failure identifier can be extracted, or when the output cannot be read, the result is `not_evaluable`, because the failures cannot be compared.

An empty baseline is valid. With an empty baseline every extracted failure is a new failure, and the result is `satisfied` only when no failure occurred. A baseline entry that did not fail in the evaluation is not a failure and does not change the result. The record notes the number of such entries. See AE-052.

**AE-052 — A new failure is named**

Given a check-command gate whose baseline lists the failure `t1`, and whose command ends with an exit status that the exit map maps to `not_satisfied`  
When the output of the command names the failures `t1` and `t9`  
Then the result is `not_satisfied`, and the record names `t9` and states that there is one new failure

**AE-053 — A changed baseline needs a new approval**

Given a `core` change whose gate definitions were approved with a baseline that lists the failure `t1`, and the entry `t9` was added to the baseline after the approval  
When the `close` action is requested  
Then the result is `rejected` with the issue code `gates-changed`, and the baseline with `t9` has no effect until a human approves the gate definitions again

### 24.7 Hard and Soft Failure

Every fail condition has a severity, which is `hard` or `soft`, written in exact lowercase. A fail condition without a severity, or with any other value, is invalid and MUST be rejected when the gate definitions are approved. The severity is the field `severity` of a fail gate (Section 23.3). A retry limit (Section 24.2) is a fail condition of the severity `soft`, and a retry limit that declares the severity `hard` is invalid and MUST be rejected. See AE-054.

A hard failure ends the change as failed without any human action. When an action that evaluates gates finds a fail condition of the severity `hard` active, the action MUST close the change as failed in the same state mutation: the state `closed` with the outcome `failed`. This decision comes before every other decision of Section 24.2, and the action that makes it answers `success`. An active hard failure also turns `cancel` and `supersede` into a close as failed (Section 23.4), and so does a change that awaits the disposition of a soft failure (see the next paragraphs). The action `start` is an exception: it never closes a change. When a fail gate of the severity `hard` is active, `start` is rejected with `changed` false and the issue code `start-blocked` (Section 24.2), and the change keeps its state. The action `fail` is a second exception: it is valid only while a soft failure awaits disposition, so that with only a fail condition of the severity `hard` active it is rejected with `changed` false (Section 23.4), and the change keeps its state. The failure is decided by `cancel`, by `supersede`, or by the first action that completes or resumes the change. See AE-055.

A soft failure pauses the change for a human. When an action that evaluates gates finds a fail condition of the severity `soft` active and no hard failure, the action MUST NOT close the change. The change waits, in the state `waiting` with a wait record of kind `fail-gate` (Section 23.5). The wait ends by a human disposition (Section 24.3), which is one of two:

- the human closes the change as failed, with the `fail` action and a reason or with the `cancel` or `supersede` action (Section 23.4);
- the human records an override of the soft failure.

The `fail` action is valid only while a soft failure awaits disposition. See AE-056.

A `cancel` or `supersede` of a change that is `waiting` with a wait record of kind `fail-gate` therefore closes the change as failed and not as cancelled, in the same way as an active hard failure does. The reason text of the outcome is the reason that the actor gave with the action or, when the actor gave none, a text that names the soft fail condition that awaited disposition (Section 25.1).

When a retry limit is reached, the change waits as it does for a soft failure, and the human closes the change as failed or records an override. Nothing ends the change automatically.

The default number of tries is 3. It applies to every done gate of the kind `check` that has no retry limit of its own, as an implicit retry limit of the severity `soft`. The project configuration MAY set a lower default, and a retry limit in a change definition MAY be lower than the default. A retry limit or a default above 3 is invalid and MUST be rejected when the gate definitions are approved: authors may lower the number of tries and never raise it. The default severity of fail gates is `hard`. The project configuration MAY set it, and the approval summary flags a fail gate whose severity is softer than the default (Section 24.1).

An override is recorded by a human as an approval with the target `override` (Section 23.4). It MUST name the soft fail condition that it applies to, MUST give a reason, and MUST give a number N of further attempts. N MUST be an integer greater than or equal to 1. This specification defines no default for N: a request that gives no number, a number below 1, or a number that is not an integer MUST be rejected, and so MUST a request that gives no reason. An override is valid only for a fail condition of the severity `soft` that awaits disposition. An override for any other fail condition MUST be rejected.

An attempt is one evaluation by the `close` action that is made while the override is in force. An evaluation that ends in the wait of Section 24.2 for a gate that cannot be evaluated is not an attempt. While the override is in force, the soft failure that it covers does not pause the change. The N-th attempt is allowed, and the evaluation after it pauses the change again, as a soft failure does. See AE-057.

An override is bound to the approved hash of the gate definitions (Section 24.1). It lapses when its N attempts are used up and when the gate definitions are amended. A lapsed override has no effect, and a soft failure that is still active pauses the change again.

**AE-054 — Reject a fail rule without a severity**

Given a `core` change whose fail gate `no-secrets` states no severity
When the gate definitions are approved
Then the approval is rejected, because every fail condition has a severity, and no approved hash is recorded

**AE-055 — A hard failure closes the change as failed without human action**

Given an `active` `core` change with a fail gate of the severity `hard` that is active  
When the `close` action is requested  
Then the result is `success`, the state is `closed`, the outcome is `failed`, and no human action was needed

**AE-056 — A soft failure pauses the change**

Given an `active` `core` change with a fail gate of the severity `soft` that is active and no hard failure  
When the `close` action is requested  
Then the change does not close, and it is `waiting` with a wait record of kind `fail-gate`

**AE-057 — An override allows exactly the granted attempts**

Given an `active` `core` change with an active soft failure, a done gate that stays unsatisfied, and an override of that soft failure with two further attempts  
When the `close` action is requested three times and none of the evaluations ends in a wait for a gate that cannot be evaluated  
Then the first two evaluations are not paused by the soft failure, and the third evaluation pauses the change again with a wait record of kind `fail-gate`

### 24.8 Open Questions as State

An open question is part of the state of the change and is recorded in its history. It is not prose in a document. A question has these fields:

- `id`: the letter `Q` followed by a decimal number that starts at 1, assigned by the implementation in the order of creation;
- `text`: the text of the question;
- `owner`: the participant that answers the question, which is the owner of the change unless the question names another;
- `asker`: the participant that asked the question;
- `options`: absent for a free-text question, and otherwise a list of at least two distinct options, which is the list of a structured question;
- `answer`: absent while the question is unanswered;
- `answerer`: the participant that gave the answer.

The `ask` action records a question without pausing the change, and the `wait` action that names an unanswered question pauses the change with a wait record of kind `question`; the `wait` action never creates a question (Sections 23.4 and 23.5). The answer is recorded as a human decision (Section 22.1).

Two options are distinct when they differ as sequences of code points (Section 24). A structured question with fewer than two distinct options MUST be rejected, and so MUST a structured question whose list repeats an option. Question identifiers are compared in the same way, so that `Q1` and `q1` are different identifiers.

Only the owner of a question answers it. An answer from another participant MUST be rejected. When the owner is a human, the answer MUST be given by a human, at the level that Section 24.3 requires for an answer. The answer to a structured question MUST be exactly one of its options, and any other value MUST be rejected. The answer to a free-text question MUST be rejected when it is empty or consists only of spaces, tabs, and line breaks. A question that is already answered MUST NOT be answered again: a second answer MUST be rejected, and the first answer stays. An answer does not resume a waiting change. See AE-060.

An unanswered question blocks two things. The approval of the specification MUST be rejected with the issue code `open-questions`, whose message names the unanswered questions, and no approval is recorded. The closure of the change is blocked: the unanswered question gate of Section 23.7 is a wait gate that is active, and the `close` action answers `blocked`. See AE-058, AE-059.

An open question is not accepted by silence, by omission, or by a statement outside the history. A participant who wants to proceed without resolving a question records an answer to it, given by the owner of the question; the answer can be an option such as `accept` of a structured question. The acceptance of an open question is therefore an answer, and a statement of acceptance that is not recorded as an answer leaves the question unanswered.

A section Open Questions in `spec.md`, where it exists, is a view of the questions that are recorded as state. Where the view and the recorded state differ, the recorded state governs.

**AE-058 — An unanswered question blocks the approval of the specification**

Given an `open` `core` change with the unanswered question Q1  
When a human approves the target `spec`  
Then the result is `rejected` with the issue code `open-questions` that names Q1, and no approval is recorded

**AE-059 — An unanswered question blocks closure**

Given an `active` `core` change with every done gate satisfied and the unanswered question Q1  
When the `close` action is requested  
Then the result is `blocked` with `changed` true, the issues name the unanswered question gate, and the change remains `active`

**AE-060 — A structured answer is recorded**

Given an `active` `core` change with the unanswered structured question Q1 whose options are `keep` and `drop` and whose owner is `human:ada`  
When `human:ada` answers Q1 with `drop`  
Then Q1 is recorded as answered with `drop` and with the answerer `human:ada`, and the state of the change does not change

### 24.9 Executable Evidence

The evidence for a requirement is executable and is bound to that requirement. An evidence command is a check command as Section 24.2 defines it: an argument list, an exit map, and OPTIONALLY a time limit. It is run as Section 24.10 states. A requirement lists the evidence commands that are bound to it in the field `requirements` of the change definition (Section 23.1).

The evidence of a change is complete only when all of these hold:

- the change declares at least one requirement;
- every requirement has at least one evidence command that is bound to it, or a human check as described below;
- when the evidence commands are run at closure, each of them has the result `satisfied`.

A requirement that cannot be checked by a machine MAY declare a **human check** instead of evidence commands: a written reason why no command can check it, and the identifier of a done gate of the kind `sign-off` that covers it. The evidence of such a requirement is complete when that gate is satisfied, and the record shows the requirement as `human-checked`. The reason is part of the gate definitions (Section 24.1). For changes to documents, an implementation SHOULD offer ready-made standard checks, for example a link check and a format check. They support the human who verifies a documentation change before the sign-off, and they do not replace the sign-off. See AE-321.

**AE-321 — A requirement that no command can check is closed by a sign-off with a reason**

Given an `active` change with the requirement R1 `the new page reads well`, which declares a human check with the reason `no command can judge readability` and the sign-off gate `page-ok`  
When `human:ada` signs off `page-ok` and the `close` action is requested with every other done gate satisfied  
Then the evidence of R1 is complete, the record shows R1 as `human-checked`, and the change closes

Closure is the evaluation that decides whether the change completes: the `close` action (Section 23.4). The incomplete evidence gate (Section 23.7) is satisfied only when the evidence is complete. See AE-061.

A change with no requirements has no complete evidence: its evidence is not complete, and the record states that no requirements are declared. A requirement without an evidence command and without a human check makes the evidence not complete, and the record names the requirement. An evidence command with the result `not_satisfied` makes the evidence not complete. An evidence command that cannot run has the result `not_evaluable` (Section 24.2): that is not a failure, it does not count toward a retry limit, the change waits as Section 24.2 states, and the evidence is not complete until the command has run and is `satisfied`. See AE-062, AE-063.

The other records that Section 15 names, for example reviews, logs, screenshots, measurements, and references to commits, MAY be kept. They supplement the executable check and never replace it. A requirement whose only evidence is such a record has no evidence command, and its evidence is not complete.

The requirement identifiers and the evidence commands that are bound to them are fixed with the gate definitions (Section 24.1), because the incomplete evidence gate judges the change by them. A difference between them and the approved ones is a difference of the gate definitions. See AE-064.

**AE-061 — Complete evidence**

Given an `active` `core` change with the requirements R1 and R2, each with one evidence command  
When the `close` action runs both evidence commands and both have the result `satisfied`  
Then the evidence is complete, and the incomplete evidence gate is satisfied

**AE-062 — A requirement without an evidence command is not evidenced**

Given an `active` `core` change with the requirements R1 and R2, where R1 has an evidence command and R2 has none  
When the `close` action is requested  
Then the evidence is not complete, and the record names R2

**AE-063 — A failing evidence command leaves the evidence incomplete**

Given an `active` `core` change with the requirement R1 whose evidence command ends with an exit status that the exit map maps to `not_satisfied`  
When the `close` action is requested  
Then the evidence is not complete, and the change does not close

**AE-064 — A changed evidence command needs a new approval**

Given a `core` change whose gate definitions were approved with the evidence command of R1, and the command of R1 was replaced after the approval by a command that always ends with the exit status that the exit map maps to `satisfied`  
When the `close` action is requested  
Then the result is `rejected` with the issue code `gates-changed`, and the replaced command has no effect until a human approves the gate definitions again

### 24.10 Gate-Command Interpreter

The commands of check-command gates (Section 24.2) and the evidence commands of requirements (Section 24.9) are run directly, as argument lists. No shell runs them, so the syntax of a shell has no effect: a pipe, a conjunction, a redirection, the expansion of a variable or of a pattern, and a command substitution are ordinary characters of an argument. See AE-065.

The interpreter is the program that runs the code a command points at, for example the runtime of a programming language. It is explicit and opt-in. A command MAY use the designated token `@interpreter` as the first element of its argument list. The token stands for the interpreter that the project configuration names if the configuration names one, and only for that interpreter. An implementation MUST NOT discover an interpreter: it MUST NOT search the project for a virtual environment, a tool directory, or any other candidate, because what stands behind the token decides whether every gate passes. When the configuration names no interpreter, the token stands for the interpreter that runs the implementation itself. A first element other than the token is a program that is run as it is. See AE-066.

The interpreter that the project configuration names is not part of the gate definitions and is not frozen (Section 24.1), so a change of the configuration changes which program runs without a difference of the gate definitions. The record shows which program ran: the `gate_detail` of the result of a command whose first element is the token `@interpreter` names the program that the token stood for in that evaluation (Section 25.1). See AE-066.

An implementation SHOULD warn when the interpreter that the token stands for lives inside the repository of the project.

Because no shell runs a command, a check that needs a pipe or a redirection is wrapped in a script of the project, and the command runs the script. For example, the command `@interpreter`, `scripts/run_tests.py` runs the script `scripts/run_tests.py`, and the script runs the tests and writes their output to a file with its own code. The guide of the implementation SHOULD give a ready-made example of such a wrapper script. A script that a command runs is code of the project: when it lies in a location that the scope check does not see (below), a change can alter it unnoticed.

Code in a location that an ignore file inside the repository tells version control to ignore is invisible to the scope check (Section 24.5). When a command runs code from such a location, including an interpreter or a library that is installed there, a change can alter that code, and so the result of the gate, without a scope violation. The scope check therefore does not show that the code behind a gate is unchanged, and the result of a gate is worth only as much as the protection of the code that its command runs.

**AE-065 — Shell syntax has no effect**

Given a check-command gate whose command is the argument list `run-tests`, `--label`, `a; echo done`  
When the gate is evaluated  
Then the program `run-tests` is run with the two arguments `--label` and `a; echo done`, and no second command `echo` is run

**AE-066 — The designated token stands for the configured interpreter**

Given a project configuration that names the interpreter `rt-stable`, and a check-command gate whose command is `@interpreter`, `check.script`  
When the gate is evaluated  
Then the program `rt-stable` is run with the argument `check.script`, and the `gate_detail` of the result names `rt-stable`

---
