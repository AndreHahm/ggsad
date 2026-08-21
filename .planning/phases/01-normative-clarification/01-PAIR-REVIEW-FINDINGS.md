# Independent Pair Review Findings — Phase 1 Normative Clarification Diff

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer (Pair Review, per the governing design's Section 5 requirement
  that normative amendments receive owner approval and independent Claude Code review)
- Requestor: agent executing Phase 1 (`01-normative-clarification`)
- Reviewed artifact: `docs/method/GG-SAD_normative_method_specification.md`
- Reviewed revision: diff from baseline `eaefb212a82e8d2e870d00bda052bc810949392e` to
  `c6d1209fdf9e8acedae1cca03a788a729933cb20` (rebased equivalent; original reviewed identity is
  recorded in `.planning/milestones/PR-3-REBASE-SHA-RECONCILIATION.md`)
- Review date: 2026-08-19
- Action: Independent review of the Phase 1 normative-clarification diff, gating Phase 2 start
- Result: Not clear to approve as written — 4 blocking/major findings, 4 recommended findings
- Scope: Diff review only, scoped to exactly
  `git diff eaefb212a82e8d2e870d00bda052bc810949392e..HEAD -- docs/method/GG-SAD_normative_method_specification.md`.
  No repository files were modified as part of this review (Pair Review rule: a Reviewer must not
  silently edit the Requestor's governed work product).

## Method

Read the exact diff, then read the complete current file (not only the changed hunks) to check
cross-references and numbering consistency across parts of the document the diff did not touch.
Checked each of the design's seven "Normative specification correction scope" items
(`docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`) against what
the diff actually implements. Grepped the full file for `Section \d` and `Sections \d` cross-
references to verify none point to stale (pre-renumbering) section numbers.

## Findings

### SF-01 — Transition Table has no action that produces `ready` from `draft` (blocking)

`draft` is a canonical status (Section 8.1) and is stated to be "legal at any non-closed phase"
(Section 8.2). None of the eight actions in the Section 8.3 Transition Table produce status `ready`
from status `draft` within the same phase — `start` requires status already `ready` as its
precondition. This is exactly the transition the retained implementation already performs and
records (`CHG-001`'s own `draft-to-ready` history event; the real `ggsad transition CHANGE_ID ready`
command), and it is exactly the kind of operation the new Minimal Automation Contract (Section 22.1)
requires implementations to execute "under the Section 8 Transition Table." As written, that
already-shipped, real operation has no row in the table.

**Recommendation:** add a transition row (e.g. `ready`) with legal-from "A non-closed phase with
status `draft`," precondition "the current phase's DoR is satisfied," and resulting status `ready`
in the same phase.

### SF-02 — `fail`/`cancel`/`supersede` are legal from "Any phase/status," contradicting the closed-phase terminality rule (blocking)

Section 8.4 states: "Once a change is in the `closed` phase, no further phase advancement is legal
except through `reopen`." But the `fail`, `cancel`, and `supersede` rows in Section 8.3 list "Any
phase/status" — not "Any non-closed phase/status," which is what the `wait` row correctly uses — as
their legal starting point. Taken literally, this permits any of these three actions to be triggered
against an already-`closed`/`done` change, silently overwriting its recorded terminal outcome (e.g.,
turning a `closed`/`done` change into `closed`/`cancelled`) without going through `reopen` first.
This undermines the mutation-safety and terminal-state guarantees the design's item 3 asked this
table to establish.

**Recommendation:** restrict the "Legal From" column for `fail`, `cancel`, and `supersede` to "Any
non-closed phase/status," matching the `wait` row's pattern, so reaching these outcomes from an
already-closed change requires `reopen` first.

### SF-03 — No canonical phase list; Section 7's diagram still uses uppercase, inconsistent with the lowercase phase tokens this diff introduces throughout Section 8 (blocking, against a named success criterion)

The design's second success criterion is: "The normative state model has one canonical phase
vocabulary, status vocabulary, and transition contract." Section 8.1 delivers a clean, canonical,
lowercase fenced list for statuses. There is no equivalent for phases: Section 7 (untouched by this
diff) still only has an uppercase arrow diagram (`INTAKE`, `SPECIFY`, ..., `CLOSED`). Meanwhile,
every new sentence this diff adds in Section 8 uses lowercase backticked phase tokens (e.g.
`` `closed` `` at Sections 8.1, 8.2, 8.3, 8.4, 20, and 22.2), matching the real `state.yaml`
convention (`flow.phase: specify`) but visually and normatively conflicting with Section 7's still-
uppercase `CLOSED`. This diff is the vehicle meant to fix exactly this kind of ambiguity, and it
left the phase side of it untouched.

**Recommendation:** add a "Canonical Phases" fenced list to Section 7, lowercase, matching Section
8.1's treatment of statuses, and reconcile or retire the uppercase arrow diagram.

### SF-04 — Design item 1's "another development method may be used" clause was not added (major)

The design's "1. Establish authority and applicability" explicitly requires: "It will explicitly
permit a GG-SAD implementation to be developed using another method. Such a development method must
not redefine GG-SAD product semantics." This statement does not appear anywhere in the document
(checked the full file, not only the diff). The only related text is the pre-existing "combination
mode" paragraph (Section 1), which describes a GG-SAD-governed *project* borrowing planning or
execution tooling — not GG-SAD's own reference implementation being developed under a different
governing method. This is precisely the scenario this repository is living through right now (GSD as
sole development method, GG-SAD as the governed product), and the specification still doesn't say
it's permitted.

**Recommendation:** add the missing sentence(s) to Section 1 or 1.1, consistent with the design's
exact wording.

## Recommended (non-blocking)

### SF-05 — Design item 4's first requirement was not implemented

"Make tailoring deterministic" asked for two things: (a) who may omit a phase, how the omission is
recorded, and what evidence replaces it; and (b) non-delegable human approval. Only (b) was added
(new Section 5.4). (a) remains unaddressed anywhere in the document.

### SF-06 — Category Map (Section 1.1) uses 3 labels where the design specified 4

The design asked the specification to separate "method semantics," "project governance," "reference-
implementation requirements," and "optional integration guidance" as four distinct things. The
Section 1.1 table only ever assigns "Method Semantics," "Reference-Implementation Requirements,"
"Optional Integration Guidance," or "Authority & Applicability" — project-governance sections
(Document Hierarchy, Workflow and Compliance Tailoring) are folded into "Method Semantics" with no
distinct label. This may be an intentional, defensible simplification, but it is not documented as a
choice anywhere.

### SF-07 — No version bump or changelog entry for this amendment

The document still reads "**Version:** 1.2" (line 3) with no history or changelog section anywhere,
despite this being a substantial rewrite of the state model, Pair Review evidence rules, and a new
normative section (22). A version bump and a brief amendment note would improve traceability,
consistent with Section 3.4 (Evidence over Assertion).

### SF-08 — "Gate Order" is identical across all eight Transition Table rows

The Gate Order column ("DoF → DoW → current-phase DoD → next-phase DoR") is copy-pasted unchanged
across all eight actions, including `cancel`/`supersede`, where "next-phase DoR" evaluation is not
obviously meaningful. This is consistent with Section 8.5's blanket evaluation-priority rule, so not
incorrect, but a one-line note that inapplicable gates in the cascade are vacuously skipped would
remove ambiguity.

## What checked out cleanly

- Section renumbering (design item 7): complete and correct. Every `Section \d` and `Sections \d`
  cross-reference in the full document — not only the diff — resolves to the correct current
  section after renumbering.
- Minimal Automation Contract (Section 22): implements all of design item 6's bullets accurately.
- Pair Review evidence fields (Section 14.5): matches design item 5's eight-field list exactly.
- Canonical artifact model changes (Section 4.3): matches design item 2 precisely, including the
  mandatory-information vs. mandatory-file distinction and `state.yaml`'s conditional status.
- Vendor-name genericization in Section 14.2 examples is a positive, appropriately-scoped
  improvement aligned with the document's existing vendor-independence principle (Section 3.8).

## Disposition

Open. SF-01 through SF-04 should be dispositioned by the Requestor and repository owner before this
diff is treated as ready to merge into the normative specification; each is a concrete, on-point gap
against either the Transition Table's own internal consistency or a named design item/success
criterion. SF-05 through SF-08 are recommended improvements that may be folded into this amendment
or explicitly deferred with a stated reason.
