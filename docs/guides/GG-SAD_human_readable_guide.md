# GG-SAD Explained Clearly

## A Lightweight Development Method with Clear Goals and Safe Transitions

**GG-SAD** stands for **Goal-Gated Spec-Anchored Development**.

The basic idea is simple:

> A change starts with a clear goal, is guided by an understandable specification, and may move to the next phase only when defined conditions are satisfied.

The method is deliberately lightweight. It requires neither epics nor full sprints, story points, role ceremonies, or a large agent apparatus.

---

## Why GG-SAD?

Many spec-driven development frameworks offer valuable ideas. In practice, however, they often create too many documents, too many process steps, or workflows that are too rigid.

GG-SAD focuses on what matters:

- **What are we trying to achieve?**
- **What exactly should change?**
- **When may we begin?**
- **When are we truly done?**
- **When must we wait?**
- **When must we stop?**
- **What evidence shows that the result is correct?**

This keeps the process controlled without making it cumbersome.

GG-SAD can be used **stand-alone** or as a **governance layer around another method or tool**. For example, a team may use GSD for context-safe execution, OpenSpec for lightweight specifications, Spec Kit for configurable workflows, BMAD for product and architecture guidance, or Kiro and Hermes as execution environments while GG-SAD retains control of gates, state, evidence, and closure.

---

## The Four Building Blocks

GG-SAD rests on four building blocks.

### 1. Goal

Every change has a clear goal.

A good goal does not merely describe a task such as *“change the login code.”* It describes the desired state:

> User accounts should be protected automatically after repeated failed login attempts.

It also includes success signals:

- A locked account rejects further login attempts.
- A successful login resets the failure counter.
- Existing clients remain compatible.

The goal supports decision-making. When several solutions are possible, the preferred one is the option that best achieves the goal while respecting architecture, rules, and scope.

### 2. Specification

The specification describes **what** should be achieved.

It typically contains:

- goal and benefit,
- scope and exclusions,
- requirements,
- concrete examples,
- technical or organizational constraints,
- verification criteria,
- open questions.

It should be clear enough for a person or an AI agent to work from. It should not prescribe every implementation detail in advance.

### 3. Gates

Gates control when the workflow may continue.

GG-SAD uses four kinds:

| Gate | Question |
|---|---|
| **Definition of Ready** | May the next phase begin? |
| **Definition of Done** | Has the current phase been completed? |
| **Definition of Wait** | Must we pause in a controlled way? |
| **Definition of Fail** | Must we terminate the flow? |

### 4. Evidence

Evidence is the verifiable proof that a requirement has been satisfied.

Examples include:

- passing tests,
- build output,
- security scans,
- review approvals,
- deployment records,
- measurements,
- references to commits or pull requests.

Without evidence, *“done”* is only an assertion.

---

## Project-Wide Documents

GG-SAD uses a small number of clearly separated documents.

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
```

### `constitution.md`

The constitution contains the non-negotiable rules of the project.

These may include:

- security principles,
- quality requirements,
- permitted or prohibited technologies,
- rules for breaking changes,
- minimum testing requirements,
- budget or resource limits,
- boundaries for autonomous agents.

The constitution changes rarely.

### `project-brief.md`

The project brief explains what the project is, why it exists, who it serves, and which operating conditions apply.

It normally records:

- the problem and opportunity,
- users and stakeholders,
- desired outcomes and success signals,
- project type such as greenfield, brownfield, migration, modernization, or re-engineering,
- scope and non-goals,
- delivery, budget, and time constraints,
- the selected compliance profile,
- whether GG-SAD runs alone or with other methods and tools.

### `architecture.md`

This document shows how the system is structured today.

It answers questions such as:

- Which components exist?
- Who is responsible for what?
- Which dependencies exist?
- How does data flow through the system?
- Where are the technical boundaries?
- How is the system operated and deployed?

`architecture.md` provides the current overall picture. Individual architecture decisions belong in ADRs.

### `roadmap.md`

The roadmap describes the direction of development without turning it into a complete project-management system.

A simple format is sufficient:

```markdown
## Now

- Authentication Hardening

## Next

- Session Management

## Later

- External Identity Providers

## Open

- Multi-region Deployment
```

In many cases, this roadmap replaces the need for an epic model.

### ADRs

Architecture Decision Records document important, durable decisions.

Examples:

- Why was PostgreSQL selected?
- Why does communication remain synchronous?
- Why is a particular dependency prohibited?

A new requirement must not silently override an existing ADR. When a conflict appears, the flow stops and a decision is requested.

---

## Tailoring GG-SAD to the Project

GG-SAD does not require a startup MVP and a regulated enterprise platform to use the same workflow.

A project selects a compliance profile:

| Profile | Typical Context | What Changes |
|---|---|---|
| **Lean** | Pre-PMF MVP, prototype, solo developer, fast iteration | Short inline specs, few artifacts, mostly automated checks, limited approvals |
| **Standard** | Normal product development | Separate specs for normal changes, defined quality gates, practical peer review |
| **Governed** | Enterprise or high-impact systems | Strong traceability, architecture and security reviews, explicit approvals |
| **Regulated** | Audited, safety-critical, or regulated systems | Segregation of duties, retained evidence, formal approvals, compliance mappings |

The core remains the same in every profile: a goal, a specification anchor, gates, suitable evidence, controlled waiting and failure, and a traceable result.

## Stand-Alone and Combined Operation

In stand-alone mode, GG-SAD supplies the complete governing flow.

In combination mode, another framework or tool may supply detailed planning, implementation, context management, testing, or agent execution. GG-SAD still decides:

- which facts are authoritative,
- whether a phase may start or finish,
- when work must wait or fail,
- which evidence is required,
- whether a change may close.

Every combination needs a small mapping contract so that external artifacts and commands have a clear GG-SAD role.

## Documents for Each Change

For a normal change, the following structure is often enough:

```text
specs/042-user-lockout/
├── spec.md
├── plan.md
└── evidence.md
```

An optional task list may be added:

```text
tasks.md
```

### `spec.md`

The specification is the central document of the change.

### `plan.md`

The plan describes the technical approach. It is needed only when the solution is not obvious or relevant risks exist.

### `tasks.md`

The task list is an execution aid. It is not a sprint backlog and is not the leading source of truth.

### `evidence.md`

This file collects the evidence showing that requirements and quality gates have been satisfied.

For small changes, the plan, tasks, and evidence may be included directly in `spec.md`.

---

## The Typical Flow

A complete workflow looks like this:

```text
INTAKE
  ↓
SPECIFY
  ↓
PLAN
  ↓
BUILD
  ↓
VERIFY
  ↓
RELEASE
  ↓
CLOSED
```

Not every change needs every phase.

### Small Change

```text
SPECIFY → BUILD → VERIFY → CLOSED
```

### Normal Change

```text
SPECIFY → PLAN → BUILD → VERIFY → CLOSED
```

### Release-Relevant Change

```text
SPECIFY → PLAN → BUILD → VERIFY → RELEASE → CLOSED
```

### Exploration

```text
EXPLORE → DECIDE → SPECIFY
```

Important: exploration must not quietly turn into production implementation.

---

## Definition of Ready

The **Definition of Ready** answers:

> Do we have enough clarity and approval to start the next phase?

### Ready-to-Spec

Specification work can begin when:

- the goal or problem is understandable,
- the expected benefit is known,
- a contact or decision owner is identified,
- important constraints are known,
- there is no obvious conflict with project rules.

### Ready-to-Plan

Planning can begin when:

- scope and non-goals are clear,
- requirements are understandable,
- acceptance conditions exist,
- relevant ADRs have been reviewed,
- open questions are resolved or consciously accepted.

### Ready-to-Build

Implementation can begin when:

- the specification is approved,
- the technical approach is sufficiently clear,
- risks have been assessed,
- dependencies are available,
- tests and verification criteria are defined.

### Ready-to-Release

A release can begin when:

- build and tests have succeeded,
- security and quality gates have passed,
- migration and rollback are clarified,
- required approvals are available.

---

## Definition of Done

The **Definition of Done** answers:

> How do we know that a phase is truly complete?

### Spec-Done

A specification is complete when:

- goal and benefit are clearly described,
- scope and exclusions are defined,
- requirements are verifiable,
- examples or acceptance conditions exist,
- open questions are resolved or explicitly accepted,
- ADR conflicts are clarified,
- the specification is approved.

### Plan-Done

A plan is complete when:

- the technical approach is described,
- affected components are known,
- architecture, data, and API impacts are assessed,
- test strategy and rollback are clarified,
- risks and decisions are documented.

### Build-Done

Implementation is complete when:

- all approved changes are implemented,
- no unintended scope has been added,
- tests have been added,
- local quality gates have passed,
- documentation has been updated,
- no unexplained deviation from the specification remains.

### Verify-Done

Verification is complete when:

- all acceptance conditions have been tested,
- automated tests have passed,
- failure and negative cases have been checked,
- regression tests have succeeded,
- evidence is complete.

### Release-Done

A release is complete when:

- deployment or publication has succeeded,
- smoke tests have passed,
- the version and release notes are documented,
- no critical operational problem is visible,
- roadmap and status have been updated.

---

## Definition of Wait

The **Definition of Wait** is one of GG-SAD's particular strengths.

It separates two situations that are often confused:

- *We cannot continue right now.*
- *The change has failed.*

A wait state is not a failure. It means that a specific prerequisite is missing.

Typical reasons include:

- a user response is missing,
- an architecture decision is pending,
- a review or approval is missing,
- an external system is unavailable,
- another process must finish first,
- a breaking change requires approval.

A useful wait entry looks like this:

```yaml
status: waiting
reason: architecture-decision-required
waiting_for: requestor
resume_when: ADR-approved
safe_state: no-destructive-change
next_action: update-plan
```

In this state, an AI agent must stop, preserve the safe state, and ask a precise question. It must not replace missing information with its own assumptions.

---

## Definition of Fail

The **Definition of Fail** describes hard termination conditions.

Typical examples include:

- critical data loss,
- repository corruption,
- severe security breach,
- unauthorized breaking change,
- violation of the constitution or an ADR,
- work outside the approved scope,
- exceeding a hard budget limit,
- an unrecoverable migration,
- permanently unsatisfiable acceptance conditions.

A fail rule should always define:

1. What triggers it?
2. Which actions must stop immediately?
3. Which preservation actions are still permitted?
4. Which final status applies?
5. What must be documented?

This tells an autonomous agent exactly when it must stop improvising.

---

## Gate Evaluation Order

GG-SAD always evaluates gates in this order:

1. **DoF** — Must we terminate?
2. **DoW** — Must we wait?
3. **DoD** — Is the current phase complete?
4. **DoR** — May the next phase begin?

This order prevents unsafe shortcuts.

Example:

The specification may be complete, while the next phase still cannot start because architecture approval is missing.

```text
Spec-Done = satisfied
Ready-to-Plan = not satisfied
Result = waiting
```

---

## What Happens When an ADR Conflicts?

Suppose a new requirement calls for a change that conflicts with an existing ADR.

Then:

1. The conflict is documented in the specification.
2. Planning or implementation stops.
3. The requirement is returned to the requestor.
4. A decision is requested.
5. The flow continues only after that decision.

The ADR is not changed incidentally. Changing it requires its own approved decision flow.

---

## How Much Documentation Does a Change Need?

GG-SAD uses three size classes.

### S — Patch

For small, clear changes.

Usually requires only:

- goal,
- scope,
- acceptance conditions,
- verification.

This can be written directly in an issue.

### M — Change

For normal, self-contained changes.

Requires:

- `spec.md`

Depending on risk, it may also need:

- `plan.md`
- `tasks.md`
- `evidence.md`

### L — Initiative

For larger efforts containing multiple independent changes.

The initiative is decomposed into multiple change specifications. A short roadmap or dependency overview is sufficient. An epic is optional, not mandatory.

---

## Minimal Specification Example

```markdown
# Change: User Lockout

## Goal

Protect accounts after repeated failed login attempts.

## Success Signals

- The account is locked after five failed attempts.
- A successful login resets the failure counter.
- Existing clients remain compatible.

## Non-Goals

- Administrator interface for unlocking accounts.
- Email notifications.
- IP-based rate limiting.

## Requirements

### R1 — Failed Attempts

The system counts consecutive failed login attempts per account.

### R2 — Lockout

The account is locked after five failed attempts.

## Acceptance Example

Given an active account with four failed attempts  
When another incorrect password is entered  
Then the account is locked  
And authentication is rejected

## Constraints

- Existing authentication ADRs take precedence.
- No new external dependency.
- The existing API format remains compatible.

## Verification

- Unit tests for R1 and R2.
- Integration test for the fifth failed attempt.
- Existing authentication tests remain successful.
```

---

## Evidence Instead of Additional Status Reports

GG-SAD avoids separate completion, review, and status documents when they provide no additional value.

A compact evidence document is often sufficient:

```markdown
# Verification Evidence

| Requirement | Evidence | Result |
|---|---|---|
| R1 | `AccountLockoutTests.cs` | Pass |
| R2 | `AuthenticationIntegrationTests.cs` | Pass |

## Quality Gates

- Build: Pass
- Unit tests: Pass
- Integration tests: Pass
- Static analysis: Pass
- Security checks: Pass

## Deviations

None.
```

---

## Future GG-SAD Memory

A later GG-SAD implementation will include a project memory for reusable information that does not belong in the governing documents.

Planned record types are:

- **Decisions** that are not architecture decisions,
- **Learnings** from implementation and operation,
- **Failures** and failed approaches,
- **Definitions and glossary terms**,
- **External sources** with provenance and trust information.

Architecture decisions remain ADRs. Memory must never become a hidden way to override the constitution, project brief, architecture, specification, or evidence.

## GG-SAD and AI Agents

GG-SAD is particularly suitable for AI agents because it establishes clear boundaries.

At any time, an agent can answer:

- Which goal am I pursuing?
- Which phase am I in?
- What may I change?
- Which rules take precedence?
- When am I done?
- When must I wait?
- When must I stop?
- Which evidence is still missing?

An agent must not:

- invent requirements,
- assume missing approvals,
- silently override ADRs,
- implement breaking changes without approval,
- work outside the scope,
- ignore missing evidence,
- bypass wait states through speculation.

---

## Example-Driven Specification and Pair Review

### Concrete examples as the standard

GG-SAD uses Example-Driven Specification as a standard practice. Every behavioral requirement includes at least one concrete acceptance example or a justified alternative acceptance condition. The notation remains flexible: Given/When/Then, tables, API examples, and state transitions are all valid.

Examples connect requirements, implementation, tests, and evidence. Higher-risk work also covers negative, failure, and boundary cases.

### Pair Review

Pair Review separates creation from evaluation:

```text
Requestor creates or changes a work product
→ Reviewer reviews, tests, verifies, or validates it
→ Reviewer returns findings
→ Requestor decides and corrects
→ Reviewer rechecks blocking findings
```

Requestor and Reviewer must be distinct participants. Supported combinations include:

- Human → Human
- Human → Agent
- Agent → Human
- Agent → Agent
- Human or Agent → external review service

Pair Review is not universally mandatory. The compliance profile, project scope, change class, risk, and project policy determine whether and how deeply it is used. Lean or small low-risk changes may omit it; governed and regulated flows may require it for relevant work.

The Reviewer does not silently modify the reviewed work product. Findings are returned to the Requestor. Pair Review does not replace required human approval.

## The Most Important Rule

GG-SAD is not document-driven. It is goal-driven.

The leading chain is:

```text
Goal
→ Spec
→ Gates
→ Implementation
→ Verification
→ Evidence
```

At project level:

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

Tasks are tools. The specification is the anchor. The goal provides direction. The gates control the path. Evidence shows whether the outcome is correct.

---

## Summary

GG-SAD provides a middle path between informal development and heavyweight SDD frameworks.

It is:

- lightweight and compliance-tailorable,
- goal-oriented,
- risk-based,
- specification-guided,
- suitable for agents,
- verifiable,
- usable without mandatory epics or sprints,
- usable stand-alone or with other methods and tools.

The core can be expressed in one sentence:

> A change may begin, continue, or be completed only when its goal, specification, gates, and evidence verifiably permit it.
