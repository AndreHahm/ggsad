# Phase 1: Normative Clarification - Context

**Gathered:** 2026-08-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce a proposed diff to `docs/method/GG-SAD_normative_method_specification.md` that
clarifies SPEC authority/applicability, the canonical artifact model, the state
transition-table contract, deterministic tailoring, portable Pair Review evidence fields,
a technology-neutral minimal automation contract, and document quality — all without
changing implementation behavior. No file under `src/ggsad/` is touched in this phase
(NORM-08). The diff itself is not applied to the spec file during this discussion — only
during later Phase 1 execution (plan/execute) — and it is not owner-approved or
independently reviewed until Phases 2 and 3.

</domain>

<decisions>
## Implementation Decisions

### Diff delivery mechanism
- **D-01:** Phase 1 execution edits `docs/method/GG-SAD_normative_method_specification.md` directly, in place. Phase 2 approval means the owner reviews the exact Git diff on the live file, not a separate proposal document. — **Reversibility:** reversible — nothing is built against this choice yet; switching to a staged-proposal-document approach later would only cost re-doing the Phase 1 execution step itself.

### Section restructuring scope for NORM-01
- **D-02:** Preserve the normative spec's current section order and numbering, except for the required NORM-07 mechanical subsection-number repairs (Sections 6–13). Satisfy NORM-01 through explicit category framing or a mapping table distinguishing: (1) the SPEC's own authority/applicability, (2) method semantics, (3) reference-implementation requirements, (4) optional integration guidance — rather than introducing new top-level Part/Section groupings. — **Reversibility:** reversible — a formatting/structure choice within the diff; can be redone before Phase 2 approval closes.

### Transition-table: is CLOSED a phase or a status?
- **D-03:** CLOSED is the terminal phase, not a status. A change in CLOSED carries a terminal outcome status such as `done`, `cancelled`, `superseded`, or `failed` — phase and status are orthogonal; CLOSED-phase changes are distinguished from each other by that outcome status, not by a separate "closed" status value. Conflicting wording elsewhere in the normative specification is corrected during Phase 1 execution's direct spec edit (per D-01) — not during this discussion. This decision aligns the clarified contract with the existing reference implementation, which already encodes this shape: `.ggsad/schemas/state.schema.json`'s `flow.phase` enum includes `closed`, while `flow.status` enum includes `done`/`failed`/`cancelled`/`superseded` but no `closed` value. — **Reversibility:** costly — Phase 2 owner approval and Phase 3 independent review lock in this transition-table shape; changing it after either gate closes requires re-approval and re-review, not just a doc edit.

### Minimal automation contract specificity (NORM-06)
- **D-04:** Define a concrete, technology-neutral minimal result envelope for automation-contract operations (init, create goal-bound change, validate, evaluate/execute one controlled transition) — not a loose "must emit structured output" requirement. Required fields:
  - `operation` — which contract operation ran
  - `result` — one of `success` | `rejected` | `error` (never partial)
  - `changed` — whether persistent state changed
  - `state` — resulting phase/status, when applicable (post-D-03: phase includes `closed`; status carries the terminal outcome)
  - `issues` — stable codes plus human-readable messages, for rejection/error cases
  - `data` — optional, operation-specific output

  Goal summary, specification anchor, gate outcome, evidence references, and timestamps
  are **not universally required** fields of the envelope — they may appear inside `data`
  when relevant to a specific operation, but are not mandated on every result. This is
  narrower than the field set first proposed during discussion (which had treated goal
  summary, spec anchor, gate outcome, evidence, and timestamp as always-required); the
  owner's approved version trades that broader traceability for a smaller universal
  surface, avoiding unnecessary command-specific requirements baked into the base
  envelope. — **Reversibility:** costly — Phase 6 (Implementation Conformance Audit) and
  Phase 7 (Gap Remediation) will scope their evidenced-gap and remediation work against
  this exact field set; changing it after Phase 2/3 approval requires re-approval,
  re-review, and replanning those phases' scope.

### Claude's Discretion
None — every gray area was explicitly decided by the repository owner; no area was left to Claude's judgment.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Governing transition documents
- `docs/method/GG-SAD_normative_method_specification.md` — the document this phase produces a diff against; precedence 0, leading product authority
- `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md` — approved transition design; precedence 1; Section 3 is the direct source of the CLOSED phase/status open question (D-03), Section 6 is the direct source of the minimal automation contract requirement (D-04)

### Derived project intel (from doc ingest)
- `.planning/intel/SYNTHESIS.md` — entry point summarizing the 31-document ingest synthesis
- `.planning/intel/context.md` — full catalogued legacy/historical document corpus (relevant to Phase 4, not this phase's edits, but explains why non-normative sources are not authoritative here)
- `.planning/intel/constraints.md` — extracted constraint entries from the two SPEC-typed sources

### Codebase context
- `.planning/codebase/CONCERNS.md` — known concerns catalogued for `src/ggsad/`
- `.planning/codebase/CONVENTIONS.md` — codebase conventions
- `.planning/codebase/STRUCTURE.md` — codebase structure

### Reference implementation schema (grounds D-03 and D-04)
- `.ggsad/schemas/state.schema.json` — current implemented `flow.phase`/`flow.status` enums (grounds D-03); the shape any Phase 6 audit of NORM-06 conformance will compare the clarified automation-contract envelope (D-04) against

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- None applicable — NORM-08 fixes this phase to a documentation-only diff; no `src/ggsad/` file is read for reuse or modified.

### Established Patterns
- `.ggsad/schemas/state.schema.json` already treats `phase` and `status` as orthogonal enums with `closed` only ever appearing in `phase` — the clarified normative transition-table contract (D-03) should describe, not contradict, this existing pattern.

### Integration Points
- None in this phase. `src/ggsad/` integration against the clarified contract is Phase 6's (Implementation Conformance Audit) responsibility, not Phase 1's.

</code_context>

<specifics>
## Specific Ideas

No specific implementation-detail requirements beyond the four decisions above — the repository owner's answers were precise and are captured verbatim in `<decisions>`.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 1-Normative Clarification*
*Context gathered: 2026-08-18*
