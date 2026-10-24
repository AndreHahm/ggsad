# Phase 2: Normative Drafting - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-10-24
**Phase:** 2-Normative Drafting
**Areas discussed:** Form of the diff, core/full vs profiles, Plan split and order, Ripple scope

---

## Form of the diff

| Option | Description | Selected |
|--------|-------------|----------|
| Edit spec on branch | Edit the spec directly on the milestone branch; diff is the file versus origin/main | ✓ |
| Separate patch file | Draft a patch under .planning; edit the spec after approval | |
| Both | Edit on branch and freeze a patch file at phase end | |

**User's choice:** Edit spec on branch.

| Option | Description | Selected |
|--------|-------------|----------|
| Blob ids + SHA-256 | Record base and result blob ids and SHA-256 at phase end | ✓ |
| Commit range | Name the commit range (rewritten by a rebase merge) | |
| Frozen patch file | Patch file with SHA-256 | |

**User's choice:** Blob ids + SHA-256.

| Option | Description | Selected |
|--------|-------------|----------|
| One commit per requirement | SPEC-01..18 each in its own commit | ✓ |
| One commit per theme | A handful of larger commits | |
| One commit total | Single draft commit | |

**User's choice:** One commit per requirement.

---

## core/full vs profiles

| Option | Description | Selected |
|--------|-------------|----------|
| Separate axes | Method profile and compliance profile, both resolved in 5.3 | ✓ |
| Replace compliance profiles | core/full become the only default profiles | |
| One flat list | Add core and full beside the four in 5.1 | |

**User's choice:** Separate axes.

| Option | Description | Selected |
|--------|-------------|----------|
| Qualified terms | "method profile" and "compliance profile" | ✓ |
| Rename core/full | Needs a new owner decision | |

**User's choice:** Qualified terms.

| Option | Description | Selected |
|--------|-------------|----------|
| Inside layer 2 | Selected profile = method + compliance profile; six layers kept | ✓ |
| New seventh layer | Contradicts SPEC-16 and O-10 counts | |

**User's choice:** Inside layer 2.

| Option | Description | Selected |
|--------|-------------|----------|
| Supersede with new change | Profile fixed at creation; switch via supersede | ✓ |
| In-place, one direction | core to full in place; full to core by supersede | |
| In-place, both ways | Explicit operation with state mapping | |

**User's choice:** Supersede with new change.

---

## Plan split and order

| Option | Description | Selected |
|--------|-------------|----------|
| Five theme plans | Vocabulary; gates and results; trust and integrity; state and versioning; full revision and resolution | ✓ |
| By spec section order | Follow the document top to bottom | |
| One plan per requirement | 18 plans | |

**User's choice:** Five theme plans.

| Option | Description | Selected |
|--------|-------------|----------|
| Lean script | Read-only mechanical checks of the diff | ✓ |
| No script | Plan greps and Phase 4 review only | |

**User's choice:** Lean script.

| Option | Description | Selected |
|--------|-------------|----------|
| Draft + flag for Phase 3 | Most conservative reading, listed in a Drafting choices list | ✓ |
| Stop and ask | Checkpoint per ambiguity | |
| Record as open question | Leave as an open question in the text | |

**User's choice:** Draft + flag for Phase 3.

---

## Ripple scope

| Option | Description | Selected |
|--------|-------------|----------|
| Spec text only | Spec examples/templates only; other files go on a hand-off list | ✓ |
| Spec + examples/templates | Also convert specs/examples and .ggsad/templates | |
| Everything incl. schema | Also change state.schema.json | |

**User's choice:** Spec text only.

| Option | Description | Selected |
|--------|-------------|----------|
| Propose 2.0 | Breaking change to the contract (recommended) | |
| Propose 1.4 | Treat as a minor revision | ✓ |
| Leave to Phase 3 | Do not change the header | |

**User's choice:** Propose 1.4 (not the recommended option).

| Option | Description | Selected |
|--------|-------------|----------|
| Inline Given/When/Then | Under each rule, with an id | ✓ |
| Appendix of examples | One appendix with ids | |

**User's choice:** Inline Given/When/Then.

---

## Claude's Discretion

Order of requirement commits inside a plan, exact checks of the lean script, numbering and placement of new subsections and example ids, and exact rule wording within the decisions.

## Deferred Ideas

Conversion of specs/examples, .ggsad/templates, state.schema.json and the archived CHG-001 state; an in-place core/full switch.
