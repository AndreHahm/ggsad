# GG-SAD Implementation Guide

## 1. Purpose

This document defines the recommended implementation approach for **Goal-Gated Spec-Anchored Development (GG-SAD)**.

GG-SAD is implemented as a lightweight, tool-independent method first and as an automation framework second. The implementation must preserve the following principles:

- Goals drive the work.
- Specifications anchor the implementation.
- Behavioral requirements use concrete acceptance examples by default.
- Pair Review separates creation from independent evaluation when enabled by compliance, scope, class, risk, or policy.
- Architecture and ADRs constrain solutions.
- Gates control phase transitions.
- Evidence demonstrates completion.
- Waiting and failure are explicit states.
- Documentation grows only when risk, complexity, or compliance justifies it.
- GG-SAD works stand-alone and with companion methods, frameworks, tools, and agents.
- Workflow profiles make lean MVP and solo flows as valid as governed and regulated flows.
- Project memory preserves reusable Decisions, Learnings, Failures, Definitions, and External Sources without replacing ADRs or governing documents.

The implementation must avoid mandatory epics, full sprint mechanics, large agent swarms, excessive hooks, and document proliferation.

---

## 2. Implementation Strategy

GG-SAD should be introduced in eight stages:

1. Establish the normative method core and project brief.
2. Define compliance profiles and tailoring rules.
3. Pilot stand-alone and combination-mode workflows on real changes.
4. Implement validation, profile resolution, mapping, and state management.
5. Add phase-specific agent workflows.
6. Add repository and CI integrations.
7. Add optional companion-method and external-tool adapters.
8. Add governed project memory.

Automation must follow observed needs. It must not define the method prematurely.

---

## 3. Repository Structure

```text
project/
├── .ggsad/
│   ├── config.yaml
│   ├── schemas/
│   │   ├── config.schema.json
│   │   └── change-state.schema.json
│   └── templates/
│       ├── constitution.md
│       ├── project-brief.md
│       ├── architecture.md
│       ├── roadmap.md
│       ├── adr.md
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── evidence.md
│       └── review.md        # conditional
├── docs/
│   ├── constitution.md
│   ├── project-brief.md
│   ├── architecture.md
│   ├── roadmap.md
│   ├── definitions/
│   │   ├── definition-of-ready.md
│   │   ├── definition-of-done.md
│   │   ├── definition-of-wait.md
│   │   └── definition-of-fail.md
│   ├── adr/
│   └── memory/
│       ├── decisions/
│       ├── learnings/
│       ├── failures/
│       ├── definitions/
│       └── external-sources/
├── specs/
│   └── CHG-001-example/
│       ├── state.yaml
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── evidence.md
│       └── review.md        # conditional
├── src/
├── tests/
└── tools/
    └── ggsad/
```

The `.ggsad/` directory contains method configuration, schemas, and templates. The `docs/` directory contains project-wide governing documents. The `specs/` directory contains change-specific artifacts.

---

## 4. Document Hierarchy

The following precedence order applies:

1. `docs/constitution.md`
2. Accepted ADRs in `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. Approved scoped Decisions that do not replace ADRs
6. Approved change specification
7. Approved change plan
8. Task checklist
9. Implementation and tests
10. Evidence and reports

A lower-level artifact must not silently override a higher-level artifact.

When a conflict is detected:

- stop the affected flow,
- record the conflict in the change specification,
- return the requirement or decision to the responsible requestor,
- create or update an ADR when architecture policy must change,
- resume only after the conflict is resolved.

---

## 5. Project-Wide Documents

### 5.1 Constitution

The constitution contains stable, non-negotiable project rules:

- quality principles,
- security rules,
- testing expectations,
- approval requirements,
- prohibited dependencies,
- breaking-change policy,
- documentation policy,
- agent permissions,
- budget and resource limits.

### 5.2 Project Brief

`docs/project-brief.md` defines the durable product and project context:

- problem and opportunity,
- users and stakeholders,
- outcomes and success signals,
- project type and lifecycle context,
- scope and non-goals,
- constraints,
- active compliance profile,
- stand-alone or combination mode,
- integrated methods and tools.

### 5.3 Architecture

`docs/architecture.md` describes the current system architecture:

- system context,
- components and responsibilities,
- module boundaries,
- dependency direction,
- data flows,
- external integrations,
- deployment topology,
- technical constraints,
- known architectural limitations.

It describes the current structure, not the history of decisions. Individual decisions belong in ADRs.

### 5.4 Roadmap

`docs/roadmap.md` describes intended development direction without introducing mandatory epic or sprint structures.

Recommended sections:

- Now
- Next
- Later
- Open Decisions
- Deferred
- Completed

Each roadmap item should identify a goal, status, dependency, and optional linked change specifications.

---

## 6. Workflow Tailoring and Compliance Profiles

The effective workflow is resolved from:

```text
Invariant Core
→ Compliance Profile
→ Project Overrides
→ Change Class
→ Local Strengthening
→ Companion Mapping
```

Default profiles:

- `lean`: MVPs, prototypes, solo work, fast iteration;
- `standard`: ordinary product development;
- `governed`: enterprise and high-impact work;
- `regulated`: audited, safety-critical, or regulated work.

Recommended configuration:

```yaml
project:
  operating_mode: combination
  compliance_profile: lean

workflow:
  profile: patch
  skippable_phases:
    - plan
    - release

integrations:
  - id: openspec
    version: "1.x"
    mapping: .ggsad/mappings/openspec.yaml

memory:
  enabled: false
```

Profiles may tailor artifacts, phase requirements, checks, approvals, evidence retention, agent autonomy, and release controls. They may not remove the invariant core.

## 7. Change Classes

GG-SAD uses three change classes.

### Class S — Small Change

Use when the solution is known, risk is low, and only a few files are affected.

Required artifacts:

- `spec.md` or an issue-level inline specification,
- verification evidence.

Optional:

- `plan.md`,
- `tasks.md`.

### Class M — Standard Change

Use for a distinct behavior change with moderate risk or multiple implementation steps.

Required artifacts:

- `state.yaml`,
- `spec.md`,
- `plan.md`,
- `evidence.md`.

Optional:

- `tasks.md`.

### Class L — Large or High-Risk Change

Use for architecture changes, breaking changes, migrations, security-sensitive work, or cross-component changes.

Required artifacts:

- `state.yaml`,
- `spec.md`,
- `plan.md`,
- `tasks.md`,
- `evidence.md`,
- ADR updates when architecture decisions change.

Large changes should be decomposed into multiple Class M changes whenever possible.

---

## 8. State Model

### 7.1 Phases

```text
intake
specify
plan
build
verify
release
closed
```

A project may omit `plan` or `release` when the selected flow profile allows it.

### 7.2 Status Values

```text
draft
ready
active
waiting
done
failed
cancelled
superseded
```

Phase and status are stored separately.

Example:

```yaml
flow:
  phase: build
  status: waiting
```

### 7.3 Transition Actions

The engine should expose actions rather than arbitrary status edits:

```text
start
complete
wait
resume
fail
cancel
supersede
reopen
```

Each action must validate the current state and applicable gates before changing state.

---

## 9. Gate Model

Each active phase evaluates gates in this order:

1. Definition of Fail
2. Definition of Wait
3. Definition of Done for the current phase
4. Definition of Ready for the next phase

### 8.1 Definition of Ready

DoR answers: **May the next phase start?**

Examples:

- Ready-to-Spec
- Ready-to-Plan
- Ready-to-Build
- Ready-to-Verify
- Ready-to-Release

### 8.2 Definition of Done

DoD answers: **Has the current phase completed successfully?**

Examples:

- Spec-Done
- Plan-Done
- Build-Done
- Verify-Done
- Release-Done

### 8.3 Definition of Wait

DoW answers: **Must the flow pause without failing?**

Typical reasons:

- user input required,
- approval pending,
- external dependency unavailable,
- another process still running,
- architecture decision pending,
- rate or budget window temporarily exhausted.

A wait state must record:

- reason,
- owner,
- safe state,
- resume condition,
- resume phase,
- next action after resume.

### 8.4 Definition of Fail

DoF answers: **Must the flow terminate unsuccessfully?**

Typical triggers:

- critical data loss,
- repository corruption,
- non-recoverable deployment failure,
- critical security violation,
- unauthorized breaking change,
- forbidden dependency,
- exceeded hard budget,
- maximum retry limit reached,
- unresolved contradiction after the allowed clarification cycles.

DoF criteria must define:

- trigger,
- mandatory response,
- allowed preservation or rollback actions,
- terminal failure status.

---

## 10. Gate Criterion Format

Each criterion should have a stable identifier and machine-readable metadata.

Example:

```markdown
### R2B-03 — Blocking decisions resolved

No blocking architecture or product decision may remain open.

- Type: state
- Evidence: state.yaml
- Severity: blocking
- Check mode: automatic
```

Supported check modes:

- `automatic`
- `review`
- `approval`

Suggested result values:

- `pass`
- `fail`
- `wait`
- `not_applicable`
- `not_evaluated`

Human approvals must never be generated by an agent acting as the approver.

---

## 11. Change State File

Each Class M or L change should contain `state.yaml`.

```yaml
schema_version: "1.0"

change:
  id: CHG-001
  title: Account lockout
  class: M

flow:
  profile: standard
  phase: specify
  status: active

goal:
  summary: Protect accounts against repeated login attempts.

artifacts:
  spec: spec.md
  plan: null
  tasks: null
  evidence: null

gates:
  current:
    definition: spec-done
    result: pending
  next:
    definition: ready-to-plan
    result: not_evaluated

wait:
  reason: null
  owner: null
  resume_condition: null
  resume_phase: null

failure:
  reason: null
  category: null

history:
  - timestamp: 2026-08-02T00:00:00Z
    event: change-created
    actor: human
```

The state file is the machine-readable workflow state. It is not the authoritative source for requirements, architecture, or evidence content.

---

## 12. Minimal Templates

### 12.1 Project Brief

```markdown
# Project Brief

## Problem and Opportunity
## Target Users and Stakeholders
## Desired Outcomes and Success Signals
## Project Type and Lifecycle Context
## Scope and Non-Goals
## Constraints
## Compliance Profile
## Operating Mode
## Integrated Methods and Tools
```

### 12.2 Change Specification

```markdown
# <Change ID> — <Title>

## Goal

### Desired Outcome

### Success Signals

### Non-Goals

## Context

## Scope

### Included

### Excluded

## Requirements

### R-001 — <Requirement Title>

## Examples

### E-001 — <Example Title>

## Constraints

## Verification

| Requirement | Verification Method |
|---|---|
| R-001 | Automated test |

## Open Questions

## Local Flow Gates

None.
```

### 12.3 Implementation Plan

```markdown
# Implementation Plan

## Approach

## Affected Components

## Architecture Impact

None.

## Data and API Impact

None.

## Test Strategy

## Risks

## Rollback

Not required.

## Decisions

None.
```

### 12.4 Task Checklist

```markdown
# Implementation Checklist

- [ ] Implement the approved behavior.
- [ ] Add or update tests.
- [ ] Run quality gates.
- [ ] Update required documentation.
- [ ] Capture verification evidence.
```

### 12.5 Evidence

```markdown
# Verification Evidence

## Requirement Evidence

| Requirement | Evidence | Result |
|---|---|---|
| R-001 | Test reference | Pass |

## Quality Gates

| Gate | Result | Evidence |
|---|---|---|
| Build | Pass | Command output |
| Tests | Pass | Test report |

## Deviations

None.

## Final Result

Pending.
```

---

## 13. CLI Scope

The first automation component should be a small CLI.

Recommended commands:

```text
ggsad init
ggsad profile
ggsad map
ggsad new
ggsad status
ggsad validate
ggsad evaluate
ggsad transition
ggsad resume
ggsad close
ggsad memory
```

### `ggsad init`

Creates method configuration, schemas, templates, project-wide documents, and directories.

### `ggsad new`

Creates a change directory, `state.yaml`, and the minimum artifacts for the selected class and flow profile.

### `ggsad validate`

Checks:

- repository structure,
- schema validity,
- required headings,
- requirement identifiers,
- artifact references,
- status values,
- document hierarchy violations,
- gate weakening,
- evidence completeness.

### `ggsad evaluate`

Evaluates DoF, DoW, current DoD, and next DoR and returns an explainable result.

### `ggsad transition`

Executes only valid state transitions and appends a history record.

### `ggsad close`

Confirms final evidence, unresolved waits, deviations, and required project-document updates before closing the change.

---

## 14. Agent Workflows

The first version should use one agent with phase-specific commands rather than multiple specialized agents.

Recommended commands:

```text
/ggsad.intake
/ggsad.specify
/ggsad.plan
/ggsad.build
/ggsad.verify
/ggsad.close
/ggsad.status
/ggsad.resume
```

Each workflow must define:

- objective,
- required inputs,
- readable artifacts,
- writable artifacts,
- prohibited actions,
- gate evaluation responsibilities,
- wait behavior,
- failure behavior,
- expected output contract.

### Permission Example

```yaml
permissions:
  specify:
    write:
      - "specs/{change_id}/spec.md"
      - "specs/{change_id}/state.yaml"
    deny:
      - "src/**"
      - "tests/**"

  plan:
    write:
      - "specs/{change_id}/plan.md"
      - "specs/{change_id}/tasks.md"
      - "specs/{change_id}/state.yaml"

  build:
    write:
      - "src/**"
      - "tests/**"
      - "specs/{change_id}/evidence.md"
      - "specs/{change_id}/state.yaml"

  verify:
    write:
      - "specs/{change_id}/evidence.md"
      - "specs/{change_id}/state.yaml"
```

Agents must not silently change approved specifications, plans, architecture, or ADRs during implementation.

---


## 15. Pair Review Implementation

Pair Review is a profile-resolved capability rather than a universally mandatory phase.

The resolver should consider:

- active compliance profile,
- project scope,
- change class,
- risk and criticality,
- affected artifact type,
- local specification rules.

Supported participant combinations include Human–Human, Human–Agent, Agent–Human, Agent–Agent, and external review services. Requestor and Reviewer identities must differ for a review cycle.

Recommended state model:

```yaml
pair_review:
  required: false
  status: not_required | pending | active | findings_open | resolved | verified
  requestor:
    id: human:andi
    type: human
  reviewer:
    id: agent:claude-code
    type: agent
  review_id: PR-001
  scope: []
  open_blocking_findings: 0
```

Recommended finding model:

```yaml
id: PRF-001
review_id: PR-001
category: testing
severity: blocking
status: open
artifact: tests/authentication_tests.py
reference: R-004
summary: Missing negative test
required_action: Add and evidence the expired-token case.
```

Reviewers should receive read and execution permissions required for review, verification, test, and validation. They should not receive write permission to governed work products unless a separate correction action assigns them as Requestor for a new cycle.

Pair Review evidence may remain inside `evidence.md`; `review.md` is conditional for complex, governed, regulated, or retained reviews.

## 16. Practice Profiles and Combination Recipes

The implementation should provide a registry for practices that refine phases, gates, templates, and evidence without changing GG-SAD semantics.

Planned packages:

- Testing Strategy Profiles: Property-Based, Mutation, Risk-Based, and Exploratory Testing;
- Architecture Practice Profiles: Feature-Sliced Design, Service-Layer Architecture, and Event-Driven Architecture;
- Security Practice Profile: Threat Modeling;
- Discovery and Product Practice Profiles: Design Thinking and Jobs to Be Done;
- Combination Recipes for validated project contexts.

Dual-Track Development and delivery models such as Trunk-Based Development, GitFlow, and Continuous Delivery remain open topics until their state, governance, and integration consequences are resolved.

## 17. Companion-Method Integration

A mapping contract should include:

```yaml
integration:
  id: gsd
  version: "1.x"
  mode: companion

ownership:
  governance: ggsad
  execution_plans: gsd
  state: ggsad
  closure: ggsad

mappings:
  - external: phase-plan
    ggsad_role: plan
  - external: verification-summary
    ggsad_role: evidence

permissions:
  may_transition_state: false
  may_approve: false

failure:
  on_sync_error: wait
  uninstall_preserves_artifacts: true
```

Initial documented mappings should cover GSD, OpenSpec, Spec Kit, BMAD, Hermes, and Kiro. The integration layer must be optional; deleting all mappings must leave a functional stand-alone GG-SAD workflow.

## 18. Project Memory

The memory subsystem should expose a backend-neutral API for:

- Decisions that are not ADRs,
- Learnings,
- Failures,
- Definitions and glossary entries,
- External Sources.

Every record should contain:

```yaml
id: MEM-DEC-0001
type: decision
scope: project
status: active
summary: Use feature flags for staged rollout.
provenance:
  actor: human
  source: specs/CHG-014/evidence.md
created_at: 2026-08-02T08:00:00Z
supersedes: null
related:
  - CHG-014
```

The implementation must classify architecture decisions and redirect them to the ADR workflow. Memory retrieval must apply permissions, compliance profile, provenance, trust, retention, and redaction rules.

Recommended initial implementation:

- file-based Markdown/YAML records for transparency and Git portability;
- a backend interface for later SQLite, vector, or external memory adapters;
- lexical and metadata search before semantic retrieval;
- optional semantic index as a rebuildable derivative;
- export and migration as mandatory capabilities;
- no hidden model-generated memory without provenance and review policy.

## 19. CI Integration

CI integration should be added only after manual pilot validation.

Recommended checks:

- valid change ID,
- valid state schema,
- approved specification exists,
- implementation phase was ready,
- requirement references exist,
- tests and quality gates pass,
- evidence is complete,
- no unresolved wait remains,
- no unapproved architecture or breaking change is present.

Example output:

```text
GG-SAD Validation

PASS  Document hierarchy
PASS  Change state schema
PASS  Specification structure
PASS  Requirement references
FAIL  Evidence completeness

R-004 has no verification evidence.
```

Git conventions may be provided as optional profiles but must not be mandatory method requirements.

---

## 20. Technology Recommendation

Recommended implementation stack:

- Markdown for method and project documentation,
- YAML for configuration and state,
- JSON Schema for structural validation,
- Python for the CLI and rule engine,
- Typer for CLI commands,
- Pydantic for models,
- PyYAML or ruamel.yaml for YAML handling,
- pytest for tests,
- optional Jinja2 for template rendering.

Suggested package structure:

```text
src/ggsad/
├── cli.py
├── config.py
├── models/
│   ├── change.py
│   ├── gate.py
│   └── state.py
├── engine/
│   ├── evaluator.py
│   ├── transitions.py
│   ├── hierarchy.py
│   └── evidence.py
├── validators/
│   ├── schema.py
│   ├── markdown.py
│   ├── references.py
│   └── gates.py
├── templates/
└── adapters/
```

---

## 21. Anti-Overhead Rules

The implementation must enforce these principles:

1. No artifact without a clear consumer.
2. No new document when a section is sufficient.
3. No task checklist when execution is obvious.
4. No separate plan without relevant uncertainty, risk, or coordination need.
5. No duplicate evidence; references are preferred.
6. No new agent role without a real permission or context boundary.
7. No hook when an explicit CLI validation is sufficient.
8. No tool-specific dependency in the method core.
9. Local gates may strengthen global gates but may not silently weaken them.
10. Every new component must justify its maintenance and workflow cost.

---

## 22. Minimum Viable Implementation

The first productive version should contain:

- one normative method specification,
- one human-readable guide,
- project-wide constitution, project brief, architecture, and roadmap templates,
- default compliance profiles and a deterministic resolver,
- stand-alone and companion mapping contracts,
- four gate-definition templates,
- change specification, plan, task, and evidence templates,
- one `state.yaml` schema,
- one configuration schema,
- one Python validator and transition engine,
- six core phase-specific agent workflows,
- one example change for each change class,
- lean MVP and solo-developer examples,
- one governed or regulated example,
- a backend-neutral memory model and file-based reference backend.

The first version should not contain:

- sub-agent orchestration,
- a web application,
- a database,
- a mandatory MCP server,
- mandatory hooks,
- sprint or epic management,
- automatic issue synchronization,
- an unrestricted custom workflow language that can bypass GG-SAD invariants.

---

## 23. Acceptance Criteria for the Implementation

The GG-SAD implementation is ready for pilot use when:

- a project can be initialized from templates including `project-brief.md`,
- lean, standard, governed, and regulated profiles resolve deterministically,
- GG-SAD works stand-alone and with validated companion mappings,
- Class S, M, and L changes can be created,
- valid and invalid transitions are distinguished,
- DoR, DoD, DoW, and DoF can be evaluated,
- wait and fail states produce different outcomes,
- agents are limited by phase-specific permissions,
- evidence can be mapped to requirements and acceptance examples,
- Pair Review can be omitted or required through deterministic tailoring,
- Human–Human and mixed human/agent Pair Review combinations are supported,
- distinct Requestor and Reviewer identities are validated,
- the validator detects missing artifacts and hierarchy conflicts,
- the method can be used without GitHub, Jira, Linear, or a specific AI agent,
- one real project completes at least three pilot changes successfully,
- a Pre-PMF MVP and a solo fast-iteration pilot meet defined overhead targets,
- a regulated profile retains audit-ready evidence,
- memory records preserve provenance and cannot replace ADRs or governing documents.
