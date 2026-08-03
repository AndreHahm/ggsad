# ADR-0002: Use Markdown for Governing Documents

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

GG-SAD depends on human-readable governing artifacts such as the constitution, project brief,
architecture, roadmap, ADRs, change specifications, plans, tasks, evidence, and review records.

These documents must remain portable, versionable, reviewable in Git, understandable without
proprietary tooling, and usable by humans and multiple coding agents.

## Decision Drivers

- Human readability
- Git-friendly review and history
- Broad tool and agent support
- Low authoring overhead
- Portability and long-term accessibility
- Compatibility with embedded structured examples and references

## Considered Options

### Option 1 — Markdown

Store governing documents as Markdown.

**Advantages**

- Human-readable as plain text
- Excellent Git diff behavior
- Broad editor and agent support
- Supports tables, code examples, links, and headings
- Easy static-site generation later

**Disadvantages**

- Weak structural guarantees without validators
- Multiple Markdown dialects exist
- Complex machine-readable data is awkward

### Option 2 — YAML or JSON Documents

Store governing documents primarily as structured data.

**Advantages**

- Stronger machine parsing
- Easier schema validation
- Consistent field access

**Disadvantages**

- Poorer long-form readability
- Awkward for rationale, trade-offs, and narrative specifications
- Higher editing friction for humans

### Option 3 — Database or Proprietary Document System

Store governing artifacts in a database or hosted documentation platform.

**Advantages**

- Advanced search and access controls
- Rich workflows and metadata

**Disadvantages**

- Platform dependency
- Reduced offline portability
- Harder Git-based review
- Conflicts with the initial low-overhead repository model

## Decision

> The project will use Markdown as the normative format for governing and change-level documents.

Structured machine state and configuration will use separate YAML or JSON Schema-backed
artifacts where appropriate.

## Consequences

### Positive

- Governing documents remain readable and portable
- Humans and agents can inspect the same authoritative source
- Git history provides transparent evolution
- Documentation can later feed static-site generation

### Negative

- Validators are needed for required sections, IDs, and references
- Semantic consistency cannot be guaranteed by syntax alone
- Formatting conventions must be documented

### Neutral or Operational

- Derived HTML or documentation sites are non-authoritative
- Markdown linting may be added as a development check

## Constraints and Guardrails

- One fact should have one authoritative home.
- Generated summaries must be labeled non-authoritative.
- Structured state must not be embedded in prose when a machine-readable artifact is required.
- Documents must remain understandable without rendering.

## Implementation Notes

- Store project-wide artifacts under `docs/`.
- Store change artifacts under `specs/<change-id>/`.
- Store the reusable ADR template under `.ggsad/templates/adr.md`.
- Add document validators incrementally.

## Verification

The decision is considered implemented when:

- all governing project documents are available as Markdown;
- ADRs and change artifacts use the approved templates;
- documentation is readable without a proprietary tool;
- derived output does not replace the Markdown source.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Structural drift | medium | Add heading and placeholder validation |
| Duplicate facts | high | Enforce source-of-truth references |
| Dialect inconsistency | low | Define repository Markdown conventions |
| Generated docs become authoritative | medium | Label generated artifacts as derived |

## Rollback or Reversal

A future ADR may introduce another normative format only with migration tooling, preserved Git
history, and equivalent human readability. Derived formats may be added without superseding this
decision.

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
