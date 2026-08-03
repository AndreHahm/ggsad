# GG-SAD

**Goal-Gated Spec-Anchored Development**

GG-SAD is a lightweight, tool-independent development method and reference implementation for
goal-oriented, specification-driven software delivery.

Every governed change begins with an explicit goal, is anchored in an approved specification, and
moves through controlled phases only when the applicable readiness, completion, waiting, and
failure conditions have been evaluated.

> **Project status:** Pre-alpha reference implementation.
> The method baseline is defined; the CLI and automation components are under active development.

## Why GG-SAD?

AI-assisted software development often loses control when goals, requirements, architecture,
permissions, state, approvals, and completion evidence are distributed across chat sessions and
tool-specific planning files.

GG-SAD provides a small governing layer that answers:

- What outcome are we trying to achieve?
- Which specification is authoritative?
- May the next phase begin?
- Is the current phase complete?
- Must work pause safely?
- Must the flow terminate?
- Which evidence demonstrates that the result is correct?
- Who created the work, who reviewed it, and who approved it?

GG-SAD deliberately avoids mandatory sprints, epics, story points, large role systems, and
unnecessary document proliferation.

## Core Model

GG-SAD is built on four elements:

### Goal

Every change has an explicit desired outcome, success signals, scope, and non-goals.

### Specification Anchor

The approved specification defines what the change must achieve. Plans, implementation, tests, and
evidence remain subordinate to it.

### Goal Gates

Transitions are evaluated in this mandatory order:

1. **Definition of Fail (DoF)** — Must the flow terminate?
2. **Definition of Wait (DoW)** — Must the flow pause safely?
3. **Definition of Done (DoD)** — Is the current phase complete?
4. **Definition of Ready (DoR)** — May the next phase begin?

### Evidence

Completion is demonstrated through tests, analysis, review results, approvals, reports, commits,
release records, or other verifiable evidence. A status is not set solely by assertion.

## Key Capabilities

- Goal-bound Class S, M, and L changes
- Explicit phase and status model
- Controlled state-transition actions
- Definition of Ready, Done, Wait, and Fail
- Example-Driven Specification
- Requirement-to-example-to-evidence traceability
- Risk- and compliance-based workflow tailoring
- `lean`, `standard`, `governed`, and `regulated` profiles
- Optional or mandatory Pair Review
- Distinct Requestor and Reviewer identities
- Human–Human and mixed human/agent review combinations
- Stand-alone and combination operating modes
- Optional companion-method and tool mappings
- Portable Markdown, YAML, and JSON Schema artifacts
- CLI-first automation strategy

## Operating Modes

### Stand-Alone

GG-SAD supplies the governing workflow without requiring an external planning framework, coding
agent, IDE, issue tracker, repository host, or CI platform.

### Combination

GG-SAD retains authority over:

- goals and scope;
- specification;
- document precedence;
- workflow state;
- DoR, DoD, DoW, and DoF;
- evidence requirements;
- approvals;
- Pair Review policy;
- closure.

A companion method or tool may provide subordinate planning, context engineering, execution,
verification support, or automation.

## GSD Integration

This repository uses **GSD Core** as the initial execution and context-engineering companion.

GSD may support:

- discussion of implementation details;
- subordinate execution planning;
- context management;
- implementation;
- verification support;
- pull-request preparation.

GSD does not own or approve GG-SAD requirements, architecture, state, gates, evidence policy, or
closure.

The authoritative relationship is:

```text
GG-SAD                                GSD Core
-----------------------------------   ---------------------------------
Governing method                      Execution companion
Goal and approved scope               Context engineering
Specification and architecture        Discuss / Plan / Execute / Verify
State and transition authority        Derived execution state
DoR / DoD / DoW / DoF                 Verification support
Evidence requirements and closure     Shipping preparation
```

GSD artifacts under `.planning/` are derived execution aids. They must not override files under
`docs/`, `.ggsad/`, or `specs/`.

See:

- `docs/adr/ADR-0006-use-gsd-as-initial-execution-companion.md`
- `.ggsad/mappings/gsd.yaml`
- `THIRD_PARTY_NOTICES.md`

## Document Hierarchy

When artifacts conflict, the following precedence applies:

1. `docs/constitution.md`
2. accepted ADRs under `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. approved scoped Decisions that do not replace an ADR
6. approved change `spec.md`
7. approved change `plan.md`
8. change `tasks.md`
9. implementation and tests
10. evidence, reports, derived summaries, and temporary work artifacts
11. companion-method artifacts such as GSD `.planning/` files

A lower-precedence artifact must not silently override a higher-precedence artifact.

## Repository Structure

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
│   ├── definitions/
│   ├── architecture.md
│   ├── constitution.md
│   ├── project-brief.md
│   └── roadmap.md
├── specs/
│   └── <change-id>/
│       ├── state.yaml
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── evidence.md
├── src/
│   └── ggsad/
├── tests/
├── AGENTS.md
├── CLAUDE.md
├── THIRD_PARTY_NOTICES.md
└── pyproject.toml
```

## Project Status and Initial Scope

The first implementation change is:

```text
CHG-001-reference-repository-bootstrap
```

Its goal is to create a repository that can:

- initialize GG-SAD project assets;
- create a Class M change;
- validate configuration and core artifacts;
- perform a controlled `draft → ready` transition;
- provide actionable errors;
- demonstrate stand-alone operation;
- support a documented GSD companion mapping.

The following capabilities are intentionally deferred from the initial slice:

- complete gate engine;
- automatic evidence evaluation;
- CI integration;
- project memory implementation;
- MCP server;
- web UI;
- issue synchronization;
- multi-agent orchestration;
- release automation;
- broad companion-framework adapters.

See `docs/roadmap.md` for the implementation sequence.

## Requirements

Recommended development baseline:

- Python 3.12 or newer
- `uv`
- Git
- Node.js and npm only when installing GSD Core
- Claude Code when using the initial GSD integration

## Quick Start

A minimal Python setup is:

```bash
git clone <repository-url>
cd ggsad
uv sync
uv run ggsad --help
```

Run the baseline quality checks:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv build
```

Some commands may remain unavailable until their roadmap change has been implemented.

## Install GSD Core for Claude Code

From the repository root:

```bash
npx @opengsd/gsd-core@latest --claude --local
```

Restart Claude Code after installation.

Initialize the greenfield GSD execution context with:

```text
/gsd-new-project
```

Before accepting generated GSD artifacts:

- confirm that GG-SAD remains authoritative;
- reject scope outside the active GG-SAD change;
- remove duplicate canonical requirements;
- reject unsupported dependencies and premature components;
- keep `.planning/` classified as derived execution state;
- do not treat GSD shipping as GG-SAD closure.

The GSD installer and generated files are governed by GSD's own license. See
`THIRD_PARTY_NOTICES.md`.

## Development Workflow

Before changing files:

1. identify the active change;
2. read `AGENTS.md`;
3. read tool-specific instructions such as `CLAUDE.md`;
4. read the governing project documents and relevant accepted ADRs;
5. read the active change state, specification, plan, tasks, and evidence;
6. check the working tree;
7. evaluate whether the current phase may begin or continue.

Typical GG-SAD flow:

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

Shorter flows are permitted when the effective profile and change class allow them.

## Pair Review

Pair Review separates creation from independent evaluation:

- the **Requestor** creates or changes a governed work product;
- the **Reviewer** independently reviews, verifies, tests, validates, or evaluates it.

Requestor and Reviewer must be distinct participant identities for the same review cycle.

Supported combinations include:

- Human–Human
- Human–Agent
- Agent–Human
- Agent–Agent
- Human or Agent with an external review service

Pair Review is optional by default and becomes mandatory when required by profile, scope, change
class, risk, affected artifact, or project policy. It does not replace required human approval.

## Configuration and Schemas

Primary configuration:

```text
.ggsad/config.yaml
```

Primary schemas:

```text
.ggsad/schemas/config.schema.json
.ggsad/schemas/mappings.schema.json
.ggsad/schemas/state.schema.json
```

Primary mapping contract:

```text
.ggsad/mappings/gsd.yaml
```

The schemas use JSON Schema Draft 2020-12.

## Templates

Reusable templates are stored under `.ggsad/templates/`, including:

- constitution;
- architecture;
- roadmap;
- ADR;
- gate definition;
- specification;
- plan;
- tasks;
- evidence.

Generated project or change artifacts must be reviewed before being treated as approved.

## Contributing

The project is in an early bootstrap phase. Contributions should be:

- associated with an explicit GG-SAD change;
- limited to approved scope;
- consistent with the constitution and accepted ADRs;
- accompanied by appropriate tests and evidence;
- independently reviewed when required.

Before contributing, read:

- `AGENTS.md`
- `CLAUDE.md` when using Claude Code
- `docs/constitution.md`
- `docs/project-brief.md`
- `docs/architecture.md`
- relevant accepted ADRs
- the active change specification

A dedicated `CONTRIBUTING.md` will define the public contribution process before broad community
participation is invited.

## Security

Do not report security vulnerabilities through public issues.

Until a dedicated security policy and private reporting channel are published, contact the project
maintainer through the repository owner's private contact mechanism.

Do not include credentials, tokens, personal data, or sensitive system output in issues, changes,
evidence, or review records.

## Compatibility and Stability

The project is pre-alpha.

Until version 1.0:

- CLI commands may change;
- schemas may evolve;
- migrations may be required;
- configuration fields may change;
- integration mappings may be revised;
- no compatibility guarantee should be inferred unless explicitly documented.

Schema and interface changes must still be governed, documented, and migration-aware.

## License

The GG-SAD repository license is defined by the root `LICENSE` file.

Third-party components, tools, generated files, and incorporated materials may be governed by
separate licenses. See `THIRD_PARTY_NOTICES.md`.

## Disclaimer

GG-SAD provides development-process controls and implementation guidance. It does not itself
certify legal, regulatory, security, safety, or industry compliance.

Projects remain responsible for selecting, implementing, validating, and auditing controls
appropriate to their context.
