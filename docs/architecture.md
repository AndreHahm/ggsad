# GG-SAD Reference Implementation Architecture

## Metadata

- Project: GG-SAD Reference Implementation
- Status: Initial Baseline
- Architecture Version: 0.1
- Method Baseline: GG-SAD 1.2
- Last Updated: 2026-08-02

## 1. Architectural Goal

The reference implementation separates the stable GG-SAD method from automation, agent
workflows, and external integrations.

This separation prevents tool-specific behavior from becoming part of the method itself and
preserves both stand-alone and combination operation.

```text
┌──────────────────────────────────────────────┐
│ Layer 5 — Integrations and Companion Methods │
│ GSD, OpenSpec, Spec Kit, BMAD, IDE, CI, MCP  │
├──────────────────────────────────────────────┤
│ Layer 4 — Agent Workflows                    │
│ intake, specify, plan, build, verify, close  │
├──────────────────────────────────────────────┤
│ Layer 3 — Method Services                    │
│ profiles, evidence, review, memory, mappings │
├──────────────────────────────────────────────┤
│ Layer 2 — Method Engine                      │
│ state, gates, transitions, validation        │
├──────────────────────────────────────────────┤
│ Layer 1 — Method Core                        │
│ invariants, hierarchy, templates, semantics  │
└──────────────────────────────────────────────┘
```

## 2. Architectural Principles

1. **Method before automation.** Automation implements GG-SAD; it does not redefine it.
2. **Tool independence.** The core does not depend on a specific agent, IDE, issue tracker,
   repository host, or CI platform.
3. **Explicit transitions.** State changes occur through validated actions, never arbitrary
   status mutation.
4. **Evidence over assertion.** Completion requires traceable evidence.
5. **One fact, one home.** Derived artifacts reference governing facts rather than duplicating
   them.
6. **Risk-based scaling.** Profiles change workflow depth without removing the invariant core.
7. **Least privilege.** Agents and integrations receive only the access required by the active
   phase.
8. **Vertical slices.** Each implementation increment produces a usable, verifiable capability.
9. **Optional integrations.** Removing all companion mappings leaves a functional stand-alone
   workflow.
10. **Portable state.** Normative documents, configuration, state, and evidence remain
    human-readable and Git-portable.

## 3. System Context

The GG-SAD repository contains:

- normative and explanatory method documentation;
- project configuration, schemas, profiles, mappings, and templates;
- a Python CLI and rule engine;
- tests and executable examples;
- optional agent, CI, repository-hosting, and companion-method adapters.

Primary actors are:

| Actor | Responsibility |
|---|---|
| Project owner | Owns scope, policy, approvals, and releases |
| Requestor | Creates or changes governed work products |
| Reviewer | Independently reviews, verifies, tests, or validates |
| Approver | Provides approvals that policy reserves for a human or designated authority |
| CLI user | Initializes projects and executes validated GG-SAD actions |
| Coding agent | Performs phase-scoped work under project policy |
| CI system | Runs non-authoritative validation and gate checks |
| Companion method | Supplies subordinate planning, execution, or context engineering |

## 4. Repository Structure

```text
.
├── .ggsad/
│   ├── config.yaml
│   ├── mappings/
│   ├── profiles/
│   ├── schemas/
│   └── templates/
├── docs/
│   ├── adr/
│   ├── architecture.md
│   ├── constitution.md
│   ├── definitions/
│   ├── project-brief.md
│   └── roadmap.md
├── specs/
├── src/
│   └── ggsad/
├── tests/
├── AGENTS.md
├── CLAUDE.md
└── pyproject.toml
```

## 5. Components

### 5.1 Method Core

Responsibilities:

- invariant principles;
- normative terminology;
- document hierarchy;
- phases and statuses;
- change classes;
- gate semantics;
- conflict and precedence rules;
- minimum artifact contracts.

Constraints:

- no runtime state;
- no dependency on integrations;
- versioned as Markdown, YAML, and schemas.

### 5.2 Configuration and Templates

Primary artifacts:

```text
.ggsad/config.yaml
.ggsad/profiles/
.ggsad/mappings/
.ggsad/schemas/
.ggsad/templates/
```

Responsibilities:

- project operating mode;
- active compliance profile;
- enabled and skippable phases;
- artifact policy by profile and change class;
- approval and Pair Review policy;
- evidence, retention, permissions, and budget policy;
- integration mappings;
- project and change templates.

### 5.3 Profile Resolver

Responsibilities:

- resolve the effective workflow in this order:

```text
Invariant Core
→ Compliance Profile
→ Project Overrides
→ Change Class
→ Local Strengthening
→ Integration Mapping
```

- reject silent weakening of a higher-precedence layer;
- return explainable resolution results;
- support `lean`, `standard`, `governed`, `regulated`, and validated custom profiles.

### 5.4 Integration Mapping Registry

Responsibilities:

- register companion methods and tools;
- define owned capabilities and GG-SAD mappings;
- identify the authoritative source for each mapped fact;
- constrain permissions and state synchronization;
- define conflict, failure, rollback, and uninstall behavior.

The initial companion is **GSD**. GSD owns subordinate execution planning and context
engineering. GG-SAD retains governance, state, gates, evidence requirements, precedence, and
closure.

### 5.5 State Manager

Responsibilities:

- load and save `state.yaml`;
- validate state against the active schema;
- preserve phase and status as separate fields;
- append immutable history events;
- store wait and failure metadata;
- perform atomic writes.

The State Manager does not interpret requirements or silently modify governed documents.

### 5.6 Transition Engine

Supported actions initially include:

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

Responsibilities:

- verify that an action is legal from the current state;
- request gate evaluation when required;
- reject invalid transitions with criterion-level explanations;
- update state atomically;
- append history.

### 5.7 Gate Engine

Responsibilities:

- evaluate gates in the mandatory order:

```text
Definition of Fail
→ Definition of Wait
→ Current Definition of Done
→ Next Definition of Ready
```

- support automatic, review, and approval criteria;
- distinguish `fail`, `wait`, `pass`, `not_applicable`, and `not_evaluated`;
- prevent unresolved blocking findings from passing an applicable gate;
- keep human approval distinct from agent review.

### 5.8 Document Validator

Responsibilities:

- validate required files and headings;
- detect unresolved placeholders;
- validate identifiers and references;
- validate artifact requirements by profile and change class;
- detect local gate weakening;
- check requirement-to-example-to-evidence links;
- report determinable hierarchy conflicts.

### 5.9 Evidence Mapper

Responsibilities:

- connect goals, requirements, acceptance examples, tests, reports, reviews, and approvals;
- identify missing evidence;
- record deviations and limitations;
- support close evaluation without duplicating raw reports.

### 5.10 Pair Review Service

Responsibilities:

- determine whether Pair Review is optional or required;
- validate distinct Requestor and Reviewer identities;
- support Human–Human, Human–Agent, Agent–Human, Agent–Agent, and external review services;
- manage review cycles, findings, severity, disposition, and re-verification;
- block applicable gates for unresolved blocking findings;
- prevent review findings from overriding governing artifacts.

### 5.11 Memory Service

The Memory Service is deferred beyond the initial bootstrap.

Planned record types:

- Decision;
- Learning;
- Failure;
- Definition;
- External Source.

Memory remains subordinate to governing documents and may not replace ADRs.

### 5.12 CLI

The CLI is the first supported user interface.

Initial command direction:

```text
ggsad init
ggsad new
ggsad status
ggsad validate
ggsad transition
```

Later commands may include:

```text
ggsad profile
ggsad map
ggsad evaluate
ggsad wait
ggsad resume
ggsad fail
ggsad close
ggsad memory
```

### 5.13 Agent Workflow Adapter

Responsibilities:

- load phase-relevant context;
- translate phase commands into constrained agent instructions;
- enforce readable and writable scopes;
- invoke CLI or engine functions;
- present wait, failure, and gate outcomes clearly.

The initial release uses one implementation agent with phase-specific workflows rather than a
multi-agent swarm.

### 5.14 Integration Adapters

Optional adapters may support:

- GitHub and GitLab checks;
- issue and pull-request linking;
- IDE commands;
- release tooling;
- MCP exposure;
- companion-method synchronization.

Adapters depend on the engine. The engine must not depend on adapters.

## 6. Dependency Rules

```text
Integrations
    ↓
Agent Workflows
    ↓
Method Services
    ↓
Method Engine
    ↓
Method Core
```

Allowed dependencies:

- CLI → Engine and Core;
- Agent adapters → CLI or Engine;
- Companion mappings → Mapping Registry and Engine;
- CI adapters → Validator and Gate Engine;
- Memory adapters → Memory Service.

Forbidden dependencies and behavior:

- Method Core → GitHub, GSD, Claude Code, or another external platform;
- State Manager → specification mutation;
- Agent adapter → direct state bypass;
- Integration → gate weakening;
- Memory record → governing-document override;
- Reviewer → silent mutation of the Requestor's reviewed work product.

## 7. Main Execution Flow

```text
User or Agent
    │
    ▼
CLI / Workflow Adapter
    │
    ├── Load governing documents
    ├── Resolve profile and change class
    ├── Load state and relevant mappings
    ├── Validate artifacts
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
    ├── Update state atomically
    └── Append history event
```

## 8. Core Data Model

### Project Profile

- compliance profile;
- operating mode;
- enabled phases;
- artifact policy;
- approval and review policy;
- evidence and retention policy;
- integration mappings;
- enabled practices and recipes.

### Change

- stable ID;
- title;
- class;
- goal;
- flow profile;
- current phase;
- current status.

### Artifact

- artifact type;
- path;
- required state;
- approval state.

### Gate and Criterion

- stable ID;
- category;
- phase;
- statement;
- severity;
- check mode;
- expected evidence;
- result;
- explanation.

### Wait Record

- reason;
- waiting owner or source;
- resume condition;
- safe state;
- resume phase;
- next action.

### Failure Record

- trigger;
- category;
- required response;
- permitted preservation actions;
- final status;
- evidence references.

### Pair Review Cycle

- stable review ID;
- Requestor and Reviewer identities;
- scope and criteria;
- findings and dispositions;
- open blocking finding count;
- final result and evidence.

### History Event

- timestamp;
- actor;
- action;
- previous state;
- new state;
- reason.

## 9. Reliability Requirements

- State updates must be atomic.
- Invalid YAML or schema violations block transitions.
- Automatic checks must be reproducible.
- Every state change creates a history event.
- Wait states preserve a safe resumable state.
- Failures preserve relevant evidence.
- Profile resolution is deterministic and explainable.
- Stand-alone operation remains available without integrations.
- Human approvals remain distinguishable from agent reviews.
- Validation failures identify exact artifacts and criteria.

## 10. Security and Safety Requirements

- Agents receive least-privilege access per phase.
- Secrets must not be stored in GG-SAD artifacts.
- Destructive operations require explicit authorization.
- Breaking changes require explicit approval.
- Evidence output must be sanitized where necessary.
- Integrations must not bypass project policy.
- Release and publication credentials remain outside GG-SAD artifacts.
- Regulated profiles must support segregation of duties and audit-ready history.

## 11. Technology Baseline

- Python 3.12 or newer;
- `uv` for dependency and environment management;
- Typer for the CLI;
- Pydantic for internal models;
- `ruamel.yaml` for YAML processing;
- JSON Schema for portable structural validation;
- pytest and Hypothesis for tests;
- Ruff for formatting and linting;
- mypy for strict type checking;
- GitHub Actions as the first optional CI example.

## 12. Architectural Decisions Requiring ADRs

Initial ADR candidates:

1. Markdown as the normative document format.
2. YAML as the configuration and state format.
3. Python as the initial engine language.
4. Separation of Method Core and integrations.
5. Explicit transition actions instead of arbitrary status edits.
6. One agent with phase-specific workflows for the initial release.
7. Human approvals as non-agent-authorizable events.
8. Deterministic compliance-profile resolution.
9. `project-brief.md` as a central project document.
10. GSD as the initial execution companion.
11. Deferred database, web UI, MCP server, and semantic memory.
12. File-based project memory before optional indexed backends.

## 13. Known Limitations

- The initial implementation is not a complete workflow platform.
- Semantic conflict detection is limited to determinable structural rules.
- Human approvals require external identity and authority controls.
- GSD integration is initially contractual and procedural rather than deeply synchronized.
- Memory, web UI, MCP, and broad repository-host integrations are deferred.
- Compliance profiles provide workflow controls but do not guarantee legal or regulatory
  compliance.
