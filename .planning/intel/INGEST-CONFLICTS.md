## Conflict Detection Report

### BLOCKERS (0)

None. Cycle detection was run across the `cross_refs` graph of all 31 classified documents in
this ingest set; no cycles were found (the two cyclic document groups identified in the prior run
— `specs/CHG-001-reference-repository-bootstrap/{plan,state,tasks,evidence}` and
`specs/examples/class-m/{spec,plan,state,tasks,evidence}` — were excluded from
`CLASSIFICATIONS_DIR` before this re-run and were not read). No `UNKNOWN`/low-confidence
classifications exist in this ingest set (all 31 are `high` confidence, typed `DOC` or `SPEC`).
No LOCKED-vs-LOCKED ADR contradiction exists because no document in this ingest set was
classified `type: ADR` (see `intel/decisions.md`).

### WARNINGS (2)

[WARNING] Two near-duplicate "reference architecture" documents with divergent detail
  Found: `docs/architecture.md` ("GG-SAD Reference Implementation Architecture," Status: Initial
  Baseline, Architecture Version 0.1, Method Baseline GG-SAD 1.2, dated 2026-08-02) and
  `docs/architecture-reference.md` ("GG-SAD Reference Architecture," no metadata block) both
  describe the same five-layer architecture, dependency rules, execution flow, and component
  responsibilities, with minor differences in detail depth, an "Architectural Decisions
  Recommended for ADRs" list that differs in ordering/count (13 vs. 12 items), and different
  Practice Profile organization. Neither document declares itself as superseding the other.
  Impact: A downstream consumer building `.planning/codebase/ARCHITECTURE.md` or roadmap content
  from this intel cannot mechanically pick one as authoritative without losing content unique to
  the other.
  → Both are catalogued verbatim-by-topic in `intel/context.md` ("GG-SAD Reference Implementation
  Architecture (two competing documents)"). Recommend the repository owner designate one as
  canonical (or explicitly merge them) in a future governed change; both are, in any case, already
  subordinated as historical/candidate material by the higher-precedence transition SPEC (see the
  auto-resolved entry below).

[WARNING] Two documents titled "GG-SAD Implementation Roadmap" with different structure and status content
  Found: `docs/implementation-roadmap.md` (Phase 0–10 structure, Suggested Release Milestones
  v0.1–v1.0, no live status entries) and `docs/roadmap.md` (`Now`/`Next`/`Later`/`Open` structure
  with R0–R14 items, `Status: Active`, Last Updated 2026-08-04, containing live delivery-status
  entries for R0/R1/R2 tied to `CHG-001-reference-repository-bootstrap`). Both are DOC-classified
  and neither cross-references the other as canonical or superseded.
  Impact: `docs/roadmap.md` is the only one of the two carrying evidenced project-status
  information (what CHG-001 actually delivered); a consumer that only reads
  `docs/implementation-roadmap.md` would miss this and could re-propose already-completed work
  as new scope.
  → Both are catalogued in `intel/context.md`. Recommend the repository owner confirm
  `docs/roadmap.md` as the status-bearing document and treat `docs/implementation-roadmap.md` as
  the original phase-planning reference (or consolidate) in a future governed change; both are
  also subordinated as historical material by the transition SPEC below.

### INFO (3)

[INFO] Auto-resolved: transition SPEC (precedence 1) and normative-method SPEC (precedence 0)
supersede the "GG-SAD governs this repository's own development" framing in 9 DOC-classified
sources
  Note: `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`
  (manifest precedence 1, `Status: Approved`) states as an owner-confirmed governing decision that
  "GSD Core is the sole development method for this minimal-automation prototype" and "GG-SAD is
  the product being implemented; it does not govern development of this prototype," and
  explicitly lists "roadmap, ADRs, architecture, and implementation plans whose conclusions
  assumed the prior GG-SAD/GSD combination model" for retirement, archival, or rewrite. This
  directly contradicts the active-development-governance framing found in: `docs/constitution.md`
  (§15 "GSD Companion Rules" — GSD as subordinate companion to GG-SAD), `docs/project-brief.md`
  ("GG-SAD Operating Mode: combination... GG-SAD is the governing method for this repository"),
  `docs/architecture.md` / `docs/architecture-reference.md` (GSD as Layer 5 integration
  subordinate to the GG-SAD Method Core), `docs/roadmap.md` and `docs/implementation-roadmap.md`
  (GG-SAD-governed roadmap phases for this repository), `docs/adr/ADR-0006-use-gsd-as-initial-
  execution-companion.md` (GSD subordinate to GG-SAD governance), and
  `specs/CHG-001-reference-repository-bootstrap/spec.md` (GG-SAD as "the governing method for the
  repository," GSD Core as subordinate companion). Per default precedence (`ADR > SPEC > PRD >
  DOC`) and the manifest's explicit precedence override, the SPEC wins: this ingest treats GSD
  Core 1.10.0 as the sole active development method for this repository, and the nine DOC sources
  above as historical/candidate product context only (not active development governance). This
  resolution is not ambiguous — it is stated explicitly and by name in the winning SPEC — so it is
  recorded here as auto-resolved rather than as a blocking or warning-level conflict. All nine
  sources remain fully catalogued in `intel/context.md` and `intel/decisions.md` /
  `intel/requirements.md` for downstream reference; none of their content was discarded.

[INFO] Auto-resolved: German normative method specification flagged for removal by the higher-precedence SPEC
  Note: `docs/method/GG-SAD_normative_method_specification_DE.md` (DOC-classified, no
  precedence override) is a full German translation of the leading normative specification.
  `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md` (SPEC,
  precedence 1) states as owner-confirmed governing decision #7: "The German normative
  specification is removed until the English baseline stabilizes." No conflicting instruction
  exists elsewhere in this ingest set. Recorded as auto-resolved; the German document's content is
  preserved for the record in `intel/context.md`.

[INFO] No ADR- or PRD-typed sources in this ingest set
  Note: All 31 classified documents in `CLASSIFICATIONS_DIR` are typed `DOC` (29) or `SPEC` (2).
  Eight legacy `docs/adr/ADR-000N-*.md` files have native ADR structure but were manifest-
  overridden to `DOC` (each carries `Status: Proposed`, never `Accepted`, so none would have been
  `locked` regardless of type). `specs/CHG-001-reference-repository-bootstrap/spec.md` has native
  PRD-like structure (20 requirements, 15 acceptance examples) but was manifest-overridden to
  `DOC` per `CLAUDE.md`'s instruction that legacy `specs/CHG-*` files are not active development
  governance. `intel/decisions.md` and `intel/requirements.md` are therefore empty of extracted
  entries by design, with pointers into `intel/context.md` for the underlying content.
