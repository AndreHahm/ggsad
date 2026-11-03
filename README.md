# GG-SAD

**Goal-Gated Spec-Anchored Development**

GG-SAD is a lightweight, tool-independent development method and Python reference implementation
for goal-oriented, specification-driven software delivery. Every governed change begins with an
explicit goal, is anchored in an approved specification, and advances only after its applicable
readiness, completion, waiting, and failure conditions have been evaluated.

> **Status:** Pre-alpha. The `core` method profile is implemented by the `ggsad` command line;
> the specification and the implementation contract define its scope.

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
- **Goal gates:** fail, wait, and done gates, evaluated in a fixed order. Their definitions are
  frozen when a human approves them.
- **Evidence:** verifiable tests, reviews, approvals, and reports that the history records.

Key capabilities include controlled state transitions under one transition table; example-driven
specifications; a hash-chained history of every change with an optional anchor outside the working
tree; scope checks against Git; `lean`, `standard`, `governed`, and `regulated` profiles;
independent Pair Review; portable Markdown, YAML, and JSON artifacts; and stand-alone use. A
second model with phases and size classes is kept in
[GG-SAD_full_profile_deferred.md](docs/method/GG-SAD_full_profile_deferred.md); it is not part of
the `core` profile.

## Repository Authority and Development Method

The [English normative specification](docs/method/GG-SAD_normative_method_specification.md) is the
leading source for GG-SAD method semantics and reference-implementation behavior. This README is
an orientation and usage guide, not a second specification.

[AGENTS.md](AGENTS.md) contains current repository instructions. The repository is developed with
plain, small, reviewable commits on short-lived branches. GSD is no longer used, and
[`.planning/`](.planning/) is a historical record. Tool-specific instructions are in
[CLAUDE.md](CLAUDE.md). The [implementation contract](docs/method/GG-SAD_implementation_contract.md)
defines the operations, the result envelope, and the state document of the reference
implementation.

## Current Development Status

The reference implementation is pre-alpha. The package `src/ggsad/core/` implements the `core`
profile: the transition table, gate evaluation, the history and its anchor, scope checks, evidence,
the status report, and the command line. The operation `migrate` converts an old `state.yaml`
(schema 0.1) to `state.json`; the refusals for an unusable schema version are implemented too.

## Repository Structure

```text
.
├── .planning/                      # Historical development record (GSD is no longer used)
├── archive/legacy-ggsad-governance/ # Non-authoritative historical material
├── docs/method/                    # Specification, implementation contract, extensions
├── docs/requirements/              # User requirements and use cases
├── src/ggsad/core/                 # Python reference implementation of the core profile
├── tests/unit/core/                # Automated tests
├── AGENTS.md
├── CLAUDE.md
└── pyproject.toml
```

## Requirements and Quick Start

Development requires Python 3.13 or newer, `uv`, and Git.

```bash
git clone <repository-url>
cd ggsad
uv sync --locked
uv run ggsad --help
```

Useful commands include:

```bash
uv run ggsad init --profile lean --owner human:ada
uv run ggsad new example --actor agent:assistant
uv run ggsad check example
uv run ggsad doctor
```

Every command takes the change identifier, prints readable text, and prints the result envelope
with `--json`. The exit code is 0 for `success`, 1 for `rejected` or `blocked`, and 2 for `error`.

Run the engineering baseline with:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check src tests
uv run pytest
uv build
```

## Configuration and Templates

`ggsad init` creates the project files and never overwrites one that exists:

```text
.ggsad/config.yaml          # settings, schema version 1.0: profile, roles, defaults, levels
.ggsad/templates/           # templates for the brief, constitution, architecture, roadmap,
                            # change definition, specification, and review report
docs/project-brief.md       # states the compliance profile; must equal the configuration
docs/constitution.md        # and, from the profile `standard` on, architecture and roadmap
specs/example/              # an example change to try with `ggsad new example`
```

A change lives in `specs/<change-id>/`: `change.yaml`, `spec.md`, `state.json` (the history), and
`review.md` when a review is kept. The anchor of a history is a Git ref
(`refs/ggsad/anchors/<change-id>`) in the repository. `ggsad doctor` checks the project, the
tools, and every change, and names the command that fixes each problem. A change that still has
only an old `state.yaml` is refused until `ggsad migrate <change-id>` converts it; the old file stays.
Only clear statuses are taken over (draft, ready, done, cancelled, failed with a reason).

## Pair Review

Pair Review separates creation from independent evaluation: the Requestor creates or changes a
governed work product, while a distinct Reviewer evaluates it. Human and agent combinations are
supported. Pair Review becomes mandatory when required by the effective profile, scope, risk,
artifact, change class, or project policy; it does not replace required human approval.

## Development and Contributing

Before making repository changes, read [AGENTS.md](AGENTS.md) and any applicable tool
instructions. Preserve unrelated changes, add appropriate tests and evidence, and obtain the
required reviews and approvals.

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
