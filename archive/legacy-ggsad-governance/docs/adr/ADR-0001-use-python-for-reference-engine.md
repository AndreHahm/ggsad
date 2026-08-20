# ADR-0001: Use Python for the Reference Engine

## Metadata

- Status: Proposed
- Date: 2026-08-02
- Decision Owners: Project Maintainer
- Requestor: human:project-owner
- Reviewer: pending
- Approver: pending
- Related Change: CHG-001
- Supersedes: None
- Superseded By: None

## Context

GG-SAD requires an initial reference engine and CLI for repository initialization, validation,
profile resolution, state handling, controlled transitions, evidence mapping, and later gate
evaluation.

The implementation must remain portable, readable, testable, suitable for agent-assisted
development, and independent from a particular IDE, repository host, or cloud platform. The
project already defines a CLI-first strategy and a small vertical implementation slice.

This is a durable implementation-platform decision and therefore belongs in an ADR.

## Decision Drivers

- Mature ecosystem for CLI, validation, schemas, and testing
- Strong support for readable, maintainable reference implementations
- Broad availability across developer and CI environments
- Compatibility with Typer, Pydantic, JSON Schema, YAML, pytest, and Hypothesis
- Good fit for human and agent contributors
- Low operational overhead for the initial implementation

## Considered Options

### Option 1 — Python

Use Python 3.12 or newer for the initial engine and CLI.

**Advantages**

- Strong validation and CLI ecosystem
- Excellent testing support
- Fast implementation and iteration
- Readable reference implementation
- Broad contributor accessibility

**Disadvantages**

- Runtime dependency on Python
- Packaging and environment behavior vary across platforms
- Lower raw performance than compiled alternatives

### Option 2 — .NET / C#

Use .NET and C# for the engine and CLI.

**Advantages**

- Strong typing and tooling
- Good cross-platform CLI support
- Mature enterprise ecosystem

**Disadvantages**

- Higher bootstrap weight for a lightweight reference implementation
- Less direct alignment with the selected Python tooling stack
- Potentially narrower contributor familiarity in agentic OSS tooling

### Option 3 — Rust

Use Rust for the engine and CLI.

**Advantages**

- Strong correctness and performance
- Single-binary distribution
- Excellent control over state and concurrency

**Disadvantages**

- Higher implementation complexity
- Slower initial delivery
- Greater contributor and agent burden for a pre-alpha reference implementation

## Decision

> The project will use Python 3.12 or newer for the initial GG-SAD reference engine and CLI.

Python is an implementation choice, not a normative dependency of the GG-SAD method itself.

## Consequences

### Positive

- Rapid delivery of the first vertical slice
- Direct use of Typer, Pydantic, ruamel.yaml, JSON Schema, pytest, and Hypothesis
- Accessible codebase for humans and coding agents
- Straightforward local and CI execution

### Negative

- Python must be installed in development and execution environments
- Packaging and interpreter compatibility require explicit support policy
- A future single-binary distribution may require additional tooling

### Neutral or Operational

- Supported Python versions must be documented and tested
- `uv` will manage environments, locking, and builds

## Constraints and Guardrails

- The Method Core must remain language-independent.
- Python-specific behavior must not redefine normative GG-SAD semantics.
- Runtime dependencies require explicit justification.
- Public interfaces and schemas must remain portable.

## Implementation Notes

- Configure the package in `pyproject.toml`.
- Use a `src/ggsad/` layout.
- Expose the CLI through `ggsad = "ggsad.cli:app"`.
- Test supported Python versions in CI when CI is introduced.

## Verification

The decision is considered implemented when:

- the project installs with `uv sync`;
- the `ggsad` CLI entry point runs;
- unit and acceptance tests run on the supported Python baseline;
- no normative method artifact depends on Python-specific semantics.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Python version drift | medium | Define and test supported versions |
| Dependency growth | medium | Apply dependency admission rules |
| Packaging inconsistency | medium | Use `uv`, lockfiles, and build verification |
| Method becomes Python-coupled | high | Keep schemas and normative assets language-neutral |

## Rollback or Reversal

A future ADR may introduce another implementation language or a second compatible engine. Any
replacement must preserve schemas, state semantics, CLI contracts where stable, and migration
guidance.

## Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Architecture: `docs/architecture.md`
- Roadmap: `docs/roadmap.md`
- Related Change: `specs/CHG-001-reference-repository-bootstrap/`

## Decision History

| Date | Status | Actor | Summary |
|---|---|---|---|
| 2026-08-02 | Proposed | human:project-owner | Initial proposal |
