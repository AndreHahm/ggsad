# GG-SAD Reference Architecture

## 1. Architectural Goal

The GG-SAD reference architecture separates the stable method from automation and external integrations. This prevents tool-specific behavior from becoming part of the method itself.

```text
┌──────────────────────────────────────────────┐
│ Layer 5 — Integrations and Companion Methods │
│ GSD, OpenSpec, Spec Kit, BMAD, IDE, CI, MCP  │
├──────────────────────────────────────────────┤
│ Layer 4 — Agent Workflows                    │
│ intake, specify, plan, build, verify, close  │
├──────────────────────────────────────────────┤
│ Layer 3 — Method Services                    │
│ memory, evidence, tailoring, practices, review│
├──────────────────────────────────────────────┤
│ Layer 2 — Method Engine                      │
│ state, gates, transitions, validation        │
├──────────────────────────────────────────────┤
│ Layer 1 — Method Core                        │
│ invariants, hierarchy, templates, semantics  │
└──────────────────────────────────────────────┘
```

---

## 2. Components

### 2.1 Method Core

Responsibilities:

- normative rules,
- document hierarchy,
- phase definitions,
- state definitions,
- gate semantics,
- change classes,
- minimal templates,
- conflict and precedence rules.

Constraints:

- no dependency on a specific AI model,
- no dependency on a specific issue tracker,
- no runtime state,
- versioned as plain text and schemas.

### 2.2 Configuration and Templates

Responsibilities:

- project-specific profiles,
- enabled phases,
- required artifacts by change class,
- selected compliance profile and custom profiles,
- enabled and skippable phases,
- artifact requirements by change class and profile,
- gate overrides that only strengthen the selected baseline,
- stand-alone or combination operating mode,
- integration mapping contracts,
- permissions, budgets, retention, and provenance rules,
- templates including `project-brief.md`.

Primary artifacts:

```text
.ggsad/config.yaml
.ggsad/templates/
.ggsad/schemas/
```

### 2.3 Tailoring and Profile Resolver

Responsibilities:

- resolve the invariant core, compliance profile, project overrides, change class, and local strengthening;
- produce the effective workflow and artifact contract;
- reject silent weakening of a higher-precedence layer;
- support default profiles `lean`, `standard`, `governed`, and `regulated`;
- support custom profiles with explicit inheritance and deviations.

### 2.4 Integration Mapping Registry

Responsibilities:

- register companion methods, frameworks, tools, and agent platforms;
- map external artifacts and commands to GG-SAD phases and artifact roles;
- declare source-of-truth ownership and synchronization rules;
- preserve stand-alone operation when integrations are absent;
- prevent integrations from bypassing gates or approvals.

### 2.5 Practice Profile and Combination Recipe Registry

Responsibilities:

- register optional development, testing, architecture, security, discovery, and product practices;
- resolve enabled practices from the compliance profile, project scope, change class, risk, and local strengthening;
- define practice-specific artifacts, gates, checks, evidence, and compatibility constraints;
- provide Combination Recipes for validated groups of practices;
- keep practice profiles subordinate to the GG-SAD invariant core.

Initial planned profile packages include:

- Testing Strategy Profiles: Property-Based, Mutation, Risk-Based, and Exploratory Testing;
- Architecture Practice Profiles: Feature-Sliced Design, Service-Layer Architecture, and Event-Driven Architecture;
- Security Practice Profiles: Threat Modeling;
- Discovery and Product Practice Profiles: Design Thinking and Jobs to Be Done.

### 2.6 Pair Review Service

Responsibilities:

- resolve whether Pair Review is optional or required for the current change;
- validate distinct Requestor and Reviewer identities, including Human–Human combinations;
- register review cycles, scope, criteria, findings, severities, dispositions, and results;
- prevent unresolved blocking findings from passing applicable gates;
- preserve review evidence without allowing findings to override governing artifacts;
- keep agent review distinct from human approval and formal segregation of duties.

### 2.7 Memory Service

Responsibilities:

- store and retrieve Decisions, Learnings, Failures, Definitions, and External Sources;
- distinguish Decisions from ADRs and reject architecture decisions stored as ordinary memory records;
- preserve IDs, scope, provenance, status, timestamps, trust, and links;
- filter retrieval by project, change, phase, permissions, and compliance profile;
- support export, backup, retention, correction, supersession, and deletion policies.

The Memory Service must not become a hidden source of governing truth.

### 2.8 State Manager

Responsibilities:

- load and save `state.yaml`,
- validate schema,
- append history events,
- apply transition actions,
- prevent invalid transitions,
- maintain wait and failure metadata.

The State Manager must not interpret free-form requirements.

### 2.9 Gate Engine

Responsibilities:

- evaluate DoF, DoW, DoD, and DoR,
- execute automatic checks,
- collect review and approval results,
- return explainable criterion-level outcomes,
- prevent transitions when blocking criteria fail.

The Gate Engine must preserve the evaluation order:

```text
DoF → DoW → current DoD → next DoR
```

### 2.10 Document Validator

Responsibilities:

- verify required files and headings,
- validate IDs and references,
- detect unresolved placeholders,
- check artifact completeness by class,
- detect hierarchy conflicts where determinable,
- identify local gate weakening,
- validate requirement-to-evidence links.

### 2.11 Transition Engine

Responsibilities:

- map actions to legal state changes,
- request gate evaluation,
- update state atomically,
- create history entries,
- reject arbitrary state mutation.

### 2.12 Evidence Mapper

Responsibilities:

- map requirements to test or review evidence,
- record quality-gate outcomes,
- identify missing evidence,
- support final close evaluation.

Evidence should normally reference existing test results, reports, commits, or commands instead of duplicating their contents.

### 2.13 CLI

Responsibilities:

- provide human- and agent-friendly entry points,
- initialize projects,
- create changes,
- validate artifacts,
- evaluate gates,
- execute transitions,
- show status,
- close changes.

The CLI is the first supported user interface.

### 2.14 Agent Workflow Adapter

Responsibilities:

- translate phase commands into agent instructions,
- load only relevant context,
- enforce readable and writable scopes,
- call CLI or engine functions,
- present wait, failure, and gate results clearly.

The initial architecture should use one agent with multiple phase workflows.

### 2.15 Integration Adapters

Optional responsibilities:

- pull-request checks,
- issue linking,
- roadmap synchronization,
- release orchestration,
- IDE commands,
- MCP exposure.

Adapters must depend on the engine. The engine must not depend on adapters.

---

## 3. Dependency Rules

```text
Integrations → Agent Workflows → Method Services → Method Engine → Method Core
```

Allowed:

- CLI depends on Engine and Core.
- Agent adapters depend on CLI or Engine.
- Companion-method adapters depend on the Mapping Registry and Engine.
- Memory adapters depend on the Memory Service and permission model.
- CI adapters depend on Validator and Gate Engine.

Forbidden:

- Method Core depending on GitHub or an agent SDK.
- State Manager changing specifications.
- Agent adapter bypassing transition validation.
- Integration adapter weakening project gates or the selected compliance profile.
- Memory records overriding ADRs, the project brief, architecture, or approved specifications.

---

## 4. Main Execution Flow

```text
User or Agent
    │
    ▼
CLI / Workflow Adapter
    │
    ├── Load project brief and configuration
    ├── Resolve compliance profile and workflow
    ├── Load change state and relevant memory
    ├── Apply integration mappings
    ├── Validate documents
    ▼
Gate Engine
    │
    ├── Evaluate DoF
    ├── Evaluate DoW
    ├── Evaluate current DoD
    └── Evaluate next DoR
    ▼
Transition Engine
    │
    ├── Accept transition
    └── Reject transition with reasons
    ▼
State Manager
    │
    ├── Update state
    └── Append history
```

---

## 5. Data Model

Core entities:

### Project Profile

- compliance profile
- operating mode
- enabled phases
- artifact policy
- approval policy
- evidence and retention policy
- integration mappings
- enabled practice profiles and combination recipes
- Pair Review policy and participant rules

### Memory Record

- id
- type: decision, learning, failure, definition, external-source
- scope
- content or reference
- provenance
- trust and status
- created, updated, superseded timestamps
- related artifacts

### Integration Mapping

- integration and version
- owned capabilities
- GG-SAD phase and artifact mappings
- source-of-truth rules
- permissions
- state synchronization
- failure and rollback behavior

### Change

- id
- title
- class
- goal
- flow profile
- current phase
- current status

### Artifact

- type
- path
- required state
- approval state

### Gate

- id
- category: DoR, DoD, DoW, DoF
- phase
- criteria

### Criterion

- id
- statement
- severity
- check mode
- expected evidence
- result
- explanation

### Pair Review Cycle

- id
- required
- requestor participant ID and type
- reviewer participant ID and type
- scope and criteria
- status
- findings and dispositions
- result and evidence references

### Review Finding

- id
- review-cycle ID
- category
- severity
- affected artifact and reference
- summary and details
- required action
- status and disposition rationale

### History Event

- timestamp
- actor
- action
- previous state
- new state
- reason

---

## 6. Reliability Requirements

- State updates must be atomic.
- Invalid YAML or schema violations must block transitions.
- Gate results must be reproducible where checks are automatic.
- Every state change must create a history event.
- Failure records must preserve relevant evidence.
- Wait states must preserve a resumable safe state.
- Profile resolution must be deterministic and explainable.
- Stand-alone operation must remain available when all integrations are disabled.
- Memory retrieval must be reproducible for the same query, permissions, and snapshot where the backend supports it.
- Human approval requirements must remain distinguishable from agent reviews.

---

## 7. Security and Safety Requirements

- Agents receive least-privilege write access per phase.
- Secrets must not be stored in GG-SAD artifacts.
- Destructive operations require project-defined approval.
- Breaking changes require explicit approval where configured.
- Tool output included as evidence must be sanitized when necessary.
- Integrations must not bypass local gate policies.
- Memory must apply least-privilege access, provenance validation, retention, and redaction policies.
- Regulated profiles must support segregation of duties and audit-ready history.

---

## 8. Extensibility

Extension points:

- custom automatic checks,
- project-specific and compliance flow profiles,
- companion-method mapping adapters,
- memory storage and retrieval backends,
- domain-specific templates,
- additional evidence providers,
- issue-tracker adapters,
- CI adapters,
- agent adapters.

Extensions must declare:

- purpose,
- inputs,
- outputs,
- permissions,
- failure behavior,
- maintenance owner.

---

## 9. Architectural Decisions Recommended for ADRs

The reference implementation should create ADRs for:

1. YAML as the state and configuration format.
2. Markdown as the normative and project-document format.
3. Python as the initial engine language.
4. Separation of method core and integrations.
5. One agent with phase-specific workflows for the initial release.
6. Explicit state-machine transitions rather than arbitrary status edits.
7. Human approvals as non-agent-authorizable events.
8. Compliance profiles and deterministic tailoring resolution.
9. `project-brief.md` as a central project-wide document.
10. Stand-alone operation and companion-method mapping contracts.
11. Memory record taxonomy and separation of Decisions from ADRs.
12. Initial memory backend, indexing, provenance, retention, and export strategy.
