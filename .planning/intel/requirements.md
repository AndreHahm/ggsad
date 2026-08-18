# Requirements

## No PRD-classified sources in this ingest set

No document in `CLASSIFICATIONS_DIR` was classified `type: PRD`. Per the extraction rule
("PRDs → requirements.md"), this file has no requirement entries.

`specs/CHG-001-reference-repository-bootstrap/spec.md` contains PRD-shaped content (Goal,
Success Signals, Non-Goals, Requirements R-001 through R-020, Acceptance Examples E-001 through
E-015, Constraints, Verification Plan) but was manifest-classified `type: DOC`. The classifier's
note states this override was applied because `CLAUDE.md` instructs that legacy files under
`specs/CHG-*` are not active development governance, even though the content itself reads as a
legacy GG-SAD change specification with ADR/PRD-like structure.

This document's requirement content (R-001 "Initialize a GG-SAD Project" through R-020 "Remain
Within the Approved Bootstrap Scope", and their acceptance examples E-001–E-015) is catalogued in
`context.md` under "CHG-001 — Reference Repository Bootstrap (legacy change spec)" for
downstream reference. It describes a historical GG-SAD-engine CLI bootstrap (`ggsad init/new/
validate/transition`) that the project roadmap (`docs/roadmap.md`) records as already
implemented and evidenced (R0 and R2 marked "Complete" / "Delivered" as of 2026-08-04), subject
to the "retain-versus-rewrite" audit rule in the governing SPEC (see `constraints.md`): prior
GG-SAD completion evidence is historical context, not proof of current conformance.

No competing-acceptance-variant conflict exists because no second PRD-classified source with
overlapping scope exists in this ingest set.
