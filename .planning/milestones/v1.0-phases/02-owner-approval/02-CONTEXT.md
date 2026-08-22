# Phase 2: Owner Approval — Correction Context

**Gathered:** 2026-08-19
**Status:** Ready for planning

## Phase Boundary

Apply only the corrections dispositioned from Claude Code's review of the Phase 1 normative diff,
rerun the Phase 1 verification contract against the original baseline, and stop for repository-owner
approval of the new exact diff. Do not begin Phase 3 independent re-review in this phase.

## Authoritative Inputs

- `.planning/phases/01-normative-clarification/01-PAIR-REVIEW-FINDINGS.md`
- `.planning/phases/01-normative-clarification/01-BASELINE.txt`
- `docs/method/GG-SAD_normative_method_specification.md`
- Owner dispositions recorded in the 2026-08-19 discussion

## Approved Dispositions

### SF-01 — Accepted with modified remedy

Represent `draft` to `ready` within the existing `complete` action instead of adding a ninth
action. The `complete` row will define both the current-phase DoR case (`draft` to `ready`) and the
current-phase DoD case (`active` to `done`, followed by next-phase readiness where applicable).

### SF-02 — Accepted

Restrict `fail`, `cancel`, and `supersede` to non-closed phase/status combinations. A closed change
must be reopened before a different terminal outcome can be applied.

### SF-03 — Accepted

Define lowercase canonical phase identifiers in Section 7: `intake`, `explore`, `decide`,
`specify`, `plan`, `build`, `verify`, `release`, `closed`. Render phase-flow diagrams using those
identifiers. Do not add `design`; its schema discrepancy remains for the later conformance audit.

### SF-04 — Accepted

State that a GG-SAD implementation may be developed using another development method, but that
method must not redefine GG-SAD product semantics.

### SF-05 — Accepted

Define who may authorize a phase omission, how it is recorded, what replacement evidence is
required, and that omission cannot remove invariant obligations or bypass the next phase's DoR.

### SF-06 — Accepted

Retain `Authority & Applicability`, add `Project Governance` as a fifth category, and classify
Sections 4 and 5 as Project Governance. Preserve all other category assignments.

### SF-07 — Accepted

Bump the English normative specification to version 1.3 and add a dated, concise revision note.
Do not update the German sibling or legacy baseline references in this correction; those remain in
the later retirement/classification scope.

### SF-08 — Accepted

Clarify that gate order expresses precedence, inapplicable gates are skipped and recorded as
`not_applicable` when evidence is recorded, and evaluation stops when a gate determines the action's
outcome.

## Fixed Constraints

- The English normative specification remains the only product file modified.
- No implementation, tests, schemas, German specification, or legacy governance file is changed.
- The eight-action vocabulary remains unchanged.
- Corrections remain provisional until the repository owner approves the new exact diff.
- The corrected owner-approved revision must receive independent Claude Code re-review in Phase 3.
