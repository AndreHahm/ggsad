# GG-SAD

**Goal-Gated Spec-Anchored Development**

GG-SAD is a lightweight, tool-independent development method and Python reference implementation
for goal-oriented, specification-driven software delivery. Every governed change begins with an
explicit goal, is anchored in an approved specification, and advances only after its applicable
readiness, completion, waiting, and failure conditions have been evaluated.

> **Status:** Pre-alpha. The method baseline exists; the CLI and automation remain under active
> development.

## Why GG-SAD?

AI-assisted development can lose control when goals, requirements, permissions, state, approvals,
and evidence are scattered across chat sessions and tool-specific plans. GG-SAD provides a small
governing layer that makes the intended outcome, authoritative specification, current state,
transition gates, required evidence, review identity, and approval explicit.

GG-SAD deliberately avoids mandatory sprints, epics, story points, large role systems, and
unnecessary document proliferation.

## Core Model

- **Goal:** the desired outcome, success signals, scope, and non-goals.
- **Specification anchor:** the approved definition of what a change must achieve.
- **Goal gates:** Definition of Fail, Wait, Done, and Ready, evaluated in that order.
- **Evidence:** verifiable tests, analyses, reviews, approvals, reports, commits, or release records.

Key capabilities include Class S, M, and L changes; explicit phases and statuses; controlled state
transitions; example-driven specifications; traceability; risk- and compliance-based tailoring;
`lean`, `standard`, `governed`, and `regulated` profiles; independent Pair Review; portable
Markdown, YAML, and JSON Schema artifacts; stand-alone use; and optional companion mappings.

## Repository Authority and Development Method

The [English normative specification](docs/method/GG-SAD_normative_method_specification.md) is the
leading source for GG-SAD method semantics and reference-implementation behavior. This README is
an orientation and usage guide, not a second specification.

[AGENTS.md](AGENTS.md) contains current repository instructions. This repository uses pinned GSD
Core 1.10.0 as its sole development method; [`.planning/`](.planning/) contains the active project,
requirements, roadmap, state, phase contexts, plans, and verification artifacts. Tool-specific
instructions are in [CLAUDE.md](CLAUDE.md).

## Current Development Status

The reference implementation is pre-alpha. Consult the [active roadmap](.planning/ROADMAP.md) for
completed work, the current phase, and planned development. Status summaries here intentionally do
not duplicate that development record.

## Repository Structure

```text
.
├── .ggsad/                         # Product configuration, schemas, profiles, mappings, templates
├── .planning/                      # Active GSD Core 1.10.0 development state
├── archive/legacy-ggsad-governance/ # Non-authoritative historical material
├── docs/method/
│   └── GG-SAD_normative_method_specification.md
├── src/ggsad/                      # Python reference implementation
├── tests/                          # Automated tests and fixtures
├── AGENTS.md
├── CLAUDE.md
└── pyproject.toml
```

## Requirements and Quick Start

Development requires Python 3.13 or newer, `uv`, and Git. Node.js and npm are needed only for
maintaining the pinned GSD development tooling.

```bash
git clone <repository-url>
cd ggsad
uv sync --locked
uv run ggsad --help
```

Useful commands include:

```bash
uv run ggsad init <project-id>
uv run ggsad change create <change-id> --title "Change title" --class M
uv run ggsad validate
```

Run the engineering baseline with:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src tests
uv run pytest
uv build
```

## Configuration, Schemas, and Templates

The primary project configuration is `.ggsad/config.yaml`. JSON Schema Draft 2020-12 schemas are
stored at:

```text
.ggsad/schemas/config.schema.json
.ggsad/schemas/mappings.schema.json
.ggsad/schemas/state.schema.json
```

The bundled GSD mapping contract is `.ggsad/mappings/gsd.yaml`. Reusable project and change
templates are under `.ggsad/templates/`, including specification, plan, tasks, evidence, gate,
configuration, mapping, and state artifacts. Generated artifacts require review before approval.

## Pair Review

Pair Review separates creation from independent evaluation: the Requestor creates or changes a
governed work product, while a distinct Reviewer evaluates it. Human and agent combinations are
supported. Pair Review becomes mandatory when required by the effective profile, scope, risk,
artifact, change class, or project policy; it does not replace required human approval.

## Development and Contributing

Before making repository changes, read [AGENTS.md](AGENTS.md), any applicable tool instructions,
and the active [GSD planning artifacts](.planning/). Follow the current phase context and approved
plan, preserve unrelated changes, add appropriate tests and evidence, and obtain the required
reviews and approvals.

Public contribution policy is not yet finalized. A dedicated `CONTRIBUTING.md` will be added before
broad community participation is invited.

## Historical Material

The [legacy governance archive manifest](archive/legacy-ggsad-governance/MANIFEST.md) explains the
retired documents and their dispositions. Archive contents are historical and non-authoritative.

## Security

Do not report security vulnerabilities through public issues. Until a dedicated security policy
and private reporting channel are published, contact the maintainer through the repository owner's
private contact mechanism. Never include credentials, tokens, personal data, or sensitive system
output in issues, artifacts, evidence, or review records.

## Compatibility and Stability

Until version 1.0, CLI commands, schemas, migrations, configuration fields, and mappings may change.
No compatibility guarantee should be inferred unless explicitly documented. Interface and schema
changes must still be governed, documented, and migration-aware.

## License

The repository license is defined by [LICENSE](LICENSE). Third-party components, tools, generated
files, and incorporated materials may use separate licenses; see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Disclaimer

GG-SAD provides development-process controls and implementation guidance. It does not certify
legal, regulatory, security, safety, or industry compliance. Each project remains responsible for
selecting, implementing, validating, and auditing controls appropriate to its context.
