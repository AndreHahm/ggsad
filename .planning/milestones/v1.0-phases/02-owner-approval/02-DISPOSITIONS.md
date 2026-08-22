# Phase 1 Pair-Review Dispositions

Review source: `.planning/phases/01-normative-clarification/01-PAIR-REVIEW-FINDINGS.md`

Status: All findings are accepted, implemented, and approved as part of the exact corrected normative diff.

### SF-01 — Draft-to-ready transition

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Represent draft-to-ready within the existing `complete` action instead of adding a ninth action. A draft phase whose Definition of Ready passes becomes ready in the same phase; an active phase whose Definition of Done passes becomes done and advances as defined by the workflow.
- Affected sections: 8.3
- Implementation status: Applied in commit `02e2836`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

### SF-02 — Terminal transition sources

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Restrict `fail`, `cancel`, and `supersede` to non-closed changes.
- Affected sections: 8.3, 8.4
- Implementation status: Applied in commit `02e2836`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

### SF-03 — Canonical phase vocabulary

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Define the canonical lowercase phases as `intake`, `explore`, `decide`, `specify`, `plan`, `build`, `verify`, `release`, and `closed`; align diagrams and remove `design` as a phase token.
- Affected sections: 7.1–7.3
- Implementation status: Applied in commit `02e2836`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

### SF-04 — Method authority over the implementation

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Explicitly permit a GG-SAD implementation to be developed under another development method while prohibiting that method from redefining GG-SAD product semantics.
- Affected sections: 1.1
- Implementation status: Applied in commit `ad2c924`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

### SF-05 — Deterministic phase omission

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Require explicit workflow permission and authorized approval for phase omission, prohibit agent inference, define the omission record, require replacement evidence, preserve invariant-core obligations, and preserve the next phase's Definition of Ready.
- Affected sections: 5.5
- Implementation status: Applied in Section 5.5 by commit `710ac3b`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

### SF-06 — Project Governance category

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Add Project Governance as the fifth normative category and reclassify Sections 4 and 5 only.
- Affected sections: 1.1, 4, 5
- Implementation status: Applied in commit `ad2c924`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

### SF-07 — Normative version and revision metadata

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Bump the English specification from version 1.2 to 1.3 and add a concise dated revision note without changing German or legacy documents.
- Affected sections: document metadata
- Implementation status: Applied in commits `ad2c924` and `676ed76`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

### SF-08 — Gate evaluation precedence

- Disposition: Accepted
- Owner decision date: 2026-08-19
- Remedy: Define the gate order as precedence, stop evaluation when a gate determines the outcome, and record inapplicable gates as `not_applicable` when evidence supports that result.
- Affected sections: 8.5
- Implementation status: Applied in commit `02e2836`; approved in corrected revision `710ac3ba6b7702d208beaaa9c625da3e319ca25c`.

## Exact-Diff Approval

- Baseline revision: `eaefb212a82e8d2e870d00bda052bc810949392e`
- Corrected revision: `710ac3ba6b7702d208beaaa9c625da3e319ca25c`
- Owner approval: Approved
- Approval timestamp: `2026-08-19T07:46:59Z`
- Phase 3 independent re-review required: Yes
