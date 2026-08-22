# Phase 1: Normative Clarification - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-08-18
**Phase:** 1-Normative Clarification
**Areas discussed:** Diff delivery mechanism, Section restructuring scope for NORM-01, Transition-table open question: is closed a phase or a status?, Minimal automation contract specificity (NORM-06)

---

## Diff delivery mechanism

| Option | Description | Selected |
|--------|-------------|----------|
| Direct edit in place | Phase 1 execution edits the live normative spec file directly; Phase 2 reviews the exact Git diff | ✓ |
| Separate proposal document first | A standalone proposal is drafted and reviewed before being applied to the real spec file | |

**User's choice:** Direct edit in place.
**Notes:** The normative specification is not edited during this discuss-phase session — only during later Phase 1 execution (plan/execute).

---

## Section restructuring scope for NORM-01

| Option | Description | Selected |
|--------|-------------|----------|
| (a) New top-level groupings | Introduce new top-level Part/Section groupings reorganizing existing content under the four categories | |
| (b) Keep order, add framing | Keep current section order/numbering; add explicit per-section category labeling or a mapping table | ✓ |

**User's choice:** Option (b).
**Notes:** Preserves current section order/numbering except for the required NORM-07 mechanical subsection-number repairs (Sections 6–13). Keeps the diff narrow and reviewable; composes with the NORM-07 numbering fix rather than compounding it.

---

## Transition-table open question: is closed a phase or a status?

| Option | Description | Selected |
|--------|-------------|----------|
| CLOSED as a status | CLOSED is a status value alongside draft/ready/active/waiting/done/... | |
| CLOSED as a terminal phase | CLOSED is a terminal phase; the change's terminal outcome (done/cancelled/superseded/failed) is carried as a separate status within that phase | ✓ |

**User's choice:** CLOSED is the terminal phase, not a status; approved the recommendation as presented.
**Notes:** Conflicting wording elsewhere in the normative spec is corrected during Phase 1 execution's direct edit, not during this discussion. The existing reference implementation's `state.schema.json` already encodes this shape (`flow.phase` enum includes `closed`; `flow.status` enum does not).

---

## Minimal automation contract specificity (NORM-06)

| Option | Description | Selected |
|--------|-------------|----------|
| Loose requirement | "Must emit structured output," no defined minimum field set | |
| Broad concrete envelope (initially proposed) | operation, result, goal_summary, specification_anchor, phase/status, gate_outcome, evidence, rejection_reason, timestamp — all required per operation | |
| Narrower concrete envelope | operation, result (success\|rejected\|error), changed, state, issues, optional data | ✓ |

**User's choice:** Narrower concrete envelope.
**Notes:** The repository owner explicitly narrowed the initially-proposed field set: `operation`; `result` (success/rejected/error); `changed` (whether persistent state changed); `state` (resulting phase/status when applicable); `issues` (stable codes + human-readable messages for rejection/errors); optional `data` for operation-specific output. Goal summary, specification anchor, gate outcome, evidence references, and timestamps may appear inside `data` when relevant but are not universally required — this clarifies compatible observable behavior without introducing unnecessary command-specific requirements into the base envelope.

---

## Claude's Discretion

None — every gray area was explicitly decided by the repository owner.

## Deferred Ideas

None mentioned during discussion.
