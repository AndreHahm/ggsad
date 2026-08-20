---
phase: 04-legacy-governance-retirement
plan: 01
status: complete
requirements: [RETIRE-01, RETIRE-02, RETIRE-03, RETIRE-04, RETIRE-05]
completed: 2026-08-20
---

# Phase 4 Plan 01 Summary

The superseded GG-SAD repository-governance corpus is preserved in a non-authoritative historical
archive. Active repository guidance now points to the English normative specification and pinned
GSD Core 1.10.0 development state, and active state-validation tests no longer depend on historical
CHG-001 evidence.

## Work Completed

- Replaced the CHG-001 integration-test dependency with a dedicated current-schema fixture.
- Moved 28 inventoried historical files byte-identically beneath
  `archive/legacy-ggsad-governance/`.
- Added a 29-disposition manifest covering the 28 moves and the already-absent startup file.
- Retired both architecture candidates without replacement.
- Classified the delivery-status roadmap separately from the aspirational roadmap.
- Rewrote README for the current authority and development-method model.
- Removed the owner-approved unpinned installation instruction from `THIRD_PARTY_NOTICES.md`.

## Scope

The English normative specification, `src/ggsad/`, and `.ggsad/` are unchanged from Phase 4's
starting revision `677b6f0`. Test changes are limited to the representative fixture and its one
integration module. Historical moves are all detected at 100% similarity.

## Verification Result

RETIRE-01 through RETIRE-05 are satisfied. Ruff, pytest, the native-TLS package build, and GSD
consistency pass. `ty` retains 31 known diagnostics confined to installer-owned `.claude/scripts`;
Phase 5 owns the quality-tool boundary. See `04-VERIFICATION.md` for exact evidence.

## Next Boundary

Phase 5 has not started. Advancing it requires the roadmap's separate hard-gate decision.
