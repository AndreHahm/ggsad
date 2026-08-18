# Synthesis Summary

Re-run of doc ingest synthesis after the repository owner excluded 9 cyclic historical/example
files (moved to `.planning/intel/excluded-cyclic-classifications/`, not read). This run consumed
all 31 remaining classification files in `.planning/intel/classifications/` from scratch and
overwrote every intel file.

## Docs Synthesized: 31

| Type | Count | Sources |
|---|---|---|
| SPEC | 2 | `docs/method/GG-SAD_normative_method_specification.md` (precedence 0), `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md` (precedence 1) |
| DOC | 29 | everything else (see `intel/context.md` for the full topic-keyed list) |
| ADR | 0 | none — 8 legacy `docs/adr/ADR-000N-*.md` files were manifest-overridden to `DOC` |
| PRD | 0 | none — `specs/CHG-001-reference-repository-bootstrap/spec.md` was manifest-overridden to `DOC` |
| UNKNOWN | 0 | none |

## Cycle Detection

Ran across the full `cross_refs` graph of all 31 documents. **No cycles found.** The two cyclic
groups from the prior run were excluded from `CLASSIFICATIONS_DIR` before this run and were not
traversed.

## Decisions Locked: 0

No document was classified `type: ADR`, so `intel/decisions.md` has no decision entries (by
extraction-target rule, not by omission). See `intel/decisions.md` for why, and
`intel/context.md` ("Legacy GG-SAD Architecture Decision Records (ADR-0001–0008)") for the
candidate ADR content that exists but was not extracted as a locked decision.

## Requirements Extracted: 0

No document was classified `type: PRD`, so `intel/requirements.md` has no requirement entries.
See `intel/requirements.md` for why, and `intel/context.md` ("CHG-001 — Reference Repository
Bootstrap (legacy change spec)") for the R-001–R-020 requirement content that exists but was not
extracted as REQ- entries.

## Constraints: 14 entries (2 SPEC sources)

`intel/constraints.md` — 8 entries from `docs/method/GG-SAD_normative_method_specification.md`
(document hierarchy, phase model/gate order, DoR/DoD/DoW/DoF summary, Pair Review model, evidence
model, agent execution algorithm, compliance profiles, combination contracts/memory model) and 6
entries from `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`
(development-method transition, existing-repository retain/retire treatment, quality/verification
baseline, normative-spec correction scope, transition sequence/non-goals). Type breakdown:
`protocol` × 13, `nfr` × 1.

## Context Topics: 13

`intel/context.md` — GSD bootstrap transition (plan + 2 review-findings docs); legacy ADR-0001–
0008; EN/DE human-readable guides; German normative spec (flagged for removal); two competing
architecture documents; project constitution; four project-wide gate definitions; implementation
guide + implementation roadmap; project brief; roadmap (status document); CHG-001 legacy change
spec; standard workflow reference; two empty example placeholder files.

## Conflicts: 0 blockers, 2 warnings, 3 auto-resolved (info)

- **0 BLOCKERS** — no cycles, no LOCKED-vs-LOCKED, no UNKNOWN/low-confidence docs.
- **2 WARNINGS** — two near-duplicate architecture documents (`docs/architecture.md` vs.
  `docs/architecture-reference.md`); two differently-structured documents both titled "GG-SAD
  Implementation Roadmap" (`docs/implementation-roadmap.md` vs. `docs/roadmap.md`, the latter
  carrying live delivery-status content the former lacks). Both require explicit owner disposition
  before being treated as fully reconciled, though neither blocks routing.
- **3 auto-resolved (INFO)** — the transition SPEC (precedence 1) and normative-method SPEC
  (precedence 0) supersede the "GG-SAD governs this repository's own development" framing found
  in 9 DOC-classified sources (constitution, project brief, both architecture docs, both roadmap
  docs, ADR-0006, CHG-001 spec); the German normative specification is flagged for removal per the
  transition SPEC; no ADR/PRD-typed sources exist in this ingest set (structural note, not a
  contradiction).

Full detail: `.planning/intel/INGEST-CONFLICTS.md`

## Entry Points for Downstream Consumers

- `.planning/intel/decisions.md` — empty by design; see note inside
- `.planning/intel/requirements.md` — empty by design; see note inside
- `.planning/intel/constraints.md` — 14 entries from the 2 SPEC sources
- `.planning/intel/context.md` — 13 topic entries from the 29 DOC sources
- `.planning/intel/INGEST-CONFLICTS.md` — full conflict report (0 blockers / 2 warnings / 3 info)
