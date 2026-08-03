# ADR-0003: Use YAML for Configuration and State

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

GG-SAD needs machine-readable project configuration, compliance profiles, integration mappings,
change state, wait metadata, failure metadata, and transition history.

These artifacts must remain inspectable and editable by humans, portable across tools, and
validatable through stable schemas.

## Decision Drivers

- Human readability
- Git portability and reviewability
- Support for comments and concise nested structures
- Compatibility with JSON Schema and Python tooling
- Broad ecosystem support
- Suitability for agent inspection

## Considered Options

### Option 1 — YAML

Use YAML for project configuration, profiles, mappings, and change state.

**Advantages**

- Readable and concise
- Supports comments
- Broad tooling support
- Suitable for repository configuration
- Good fit with `ruamel.yaml` round-trip handling

**Disadvantages**

- YAML has parsing edge cases
- Implicit typing can surprise users
- Formatting preservation requires appropriate tooling

### Option 2 — JSON

Use JSON for all configuration and state.

**Advantages**

- Strict and widely supported
- Direct JSON Schema compatibility
- Fewer ambiguous parser behaviors

**Disadvantages**

- No comments
- More verbose for hand-edited files
- Less convenient for project configuration

### Option 3 — TOML

Use TOML for configuration and state.

**Advantages**

- Readable configuration syntax
- Strong ecosystem adoption
- Clear scalar behavior

**Disadvantages**

- Less natural for event history and deeply nested state
- JSON Schema integration is less direct
- Multiple formats would still be needed for external schemas

## Decision

> The project will use YAML for GG-SAD configuration, profiles, mappings, and change state.

JSON Schema will define portable structural contracts. YAML parsers must use safe loading and
explicit validation.

## Consequences

### Positive

- Configuration and state remain transparent
- Humans and agents can review workflow state directly
- Comments and ordered content can be preserved
- Schemas remain implementation-neutral

### Negative

- The project must defend against YAML ambiguity and unsafe parsing
- Atomic update and formatting preservation require care
- Schema validation is a separate step

### Neutral or Operational

- `ruamel.yaml` is the initial Python implementation library
- Schema versions must be explicit in YAML artifacts

## Constraints and Guardrails

- Use safe parsing only.
- Quote values that could be misinterpreted.
- Validate every governed YAML artifact before transition.
- State updates must be atomic.
- Invalid YAML or schema violations must block transitions.
- State files are not authoritative for requirements or architecture content.

## Implementation Notes

- Add `schema_version` to governed YAML files.
- Use JSON Schema for external validation.
- Use Pydantic models for internal validation where appropriate.
- Preserve transition history and wait/failure metadata.

## Verification

The decision is considered implemented when:

- `.ggsad/config.yaml` validates;
- profile and mapping YAML validate;
- Class M state files validate;
- invalid YAML and invalid schema instances are rejected safely;
- failed validation does not mutate governed state.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Implicit YAML typing | medium | Quote ambiguous values and validate types |
| Unsafe deserialization | high | Use safe loaders only |
| Partial state writes | high | Use atomic write-and-replace behavior |
| Formatting damage | low | Use round-trip YAML tooling |
| Schema drift | medium | Require explicit schema versions and migrations |

## Rollback or Reversal

A future ADR may adopt JSON or another format with migration tooling and backward-compatible
readers. Existing YAML artifacts must remain readable or migratable.

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
