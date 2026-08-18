# Decisions

## No ADR-classified sources in this ingest set

No document in `CLASSIFICATIONS_DIR` was classified `type: ADR`. Per the extraction rule
("ADRs → decisions.md"), this file has no decision entries, because extraction target is
governed by the classifier's assigned `type`, not by a document's internal structure.

Eight legacy documents under `docs/adr/` (`ADR-0001` through `ADR-0008`) have ADR-shaped
content (Metadata, Decision Drivers, Considered Options, Decision, Consequences) but were
manifest-classified `type: DOC`, each with an explicit classifier note that the manifest
override was honored and that, independent of the override, every one of these documents
carries `Status: Proposed` (not `Accepted`) and therefore would not have been `locked` even
under a native ADR classification.

These eight documents are catalogued as candidate/historical architecture material in
`context.md` under "Legacy GG-SAD Architecture Decision Records (ADR-0001–0008)". Their
content (e.g., "use Python for the reference engine," "use Markdown for governing documents,"
"use YAML for configuration and state," "separate Method Core from integrations," "use explicit
state transition actions," "use GSD as initial execution companion," "use one agent with
phase-specific workflows," "defer memory/MCP/web UI/orchestration") remains available for a
downstream consumer (e.g. `gsd-roadmapper`) to consider as candidate technical direction for the
GG-SAD reference-implementation product, subject to the audit-before-retention rule stated in
`docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md` (see
`constraints.md`).

No LOCKED-vs-LOCKED conflict exists because no locked decision exists in this ingest set.
