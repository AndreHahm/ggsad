# Independent Review Findings — Phase 4 Context (Legacy Governance Retirement)

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer
- Requestor: Codex
- Reviewed artifact: `.planning/phases/04-legacy-governance-retirement/04-CONTEXT.md`
- Review date: 2026-08-20
- Action: Review of the Phase 4 boundary/design context prior to planning
- Result: Directionally sound and factually accurate; 2 findings worth resolving before or during
  planning, neither blocking
- Scope: Document review, cross-checked against actual repository state (file existence, README.md
  content, the target test file, ADR-0006, `AGENTS.md`/`CLAUDE.md`, and `.planning/intel/context.md`
  as the authoritative legacy-artifact source list). No repository files were modified as part of
  this review.

## Method

Verified every file named in the Archive Inventory actually exists at its claimed path (all 28 do;
`CLAUDE_CODE_PROJECT_START.md` is confirmed already absent, matching the context's claim). Verified
the "29 inventoried dispositions" arithmetic (16 + 2 + 2 + 9 = 29 table rows, 28 to archive + 1
already-absent). Cross-checked the inventory against `.planning/intel/context.md` (the source RETIRE-01
points to) and found no artifact identified there missing from the Phase 4 inventory. Read the current
`README.md`, `ADR-0006`, and `AGENTS.md`/`CLAUDE.md` directly to confirm the problems the context
claims exist actually exist, rather than trusting the description. Read
`tests/integration/test_governed_artifact_validation.py` in full to verify the Test-Fixture
Decoupling section's description against the actual code.

## What checked out cleanly

- Every archive-inventory file exists; the "already absent" claim for `CLAUDE_CODE_PROJECT_START.md`
  is correct.
- The inventory is a complete superset of `.planning/intel/context.md`'s identified legacy artifacts
  — nothing from that source list is missing, and the additions beyond the roadmap's summary
  paragraph (guides, definitions, implementation guide, workflow reference) are legitimately sourced
  from `intel/context.md`, not scope creep.
- `AGENTS.md` and `CLAUDE.md` genuinely contain zero references to the retired governance model
  (grepped for constitution/ADR/architecture/roadmap/project-brief/subordinate — no matches),
  confirming the context's claim that these two files need only verification, not modification, and
  correctly excluding them from Phase 4's changeable-files list.
- `ADR-0006` genuinely contains the "reversed premise" the context flags: "Ability to remain
  subordinate to GG-SAD governance" and "GSD Core as the initial subordinate execution... companion"
  — exactly backwards from the current model. The instruction to archive it with the reversed premise
  explicitly identified is well-targeted.
- `tests/integration/test_governed_artifact_validation.py` reads
  `specs/CHG-001-reference-repository-bootstrap/state.yaml` at its active path in exactly the two
  tests named (`test_chg_001_state_is_schema_and_model_valid`,
  `test_prf005_state_schema_rejects_unsupported_schema_version`), and the first test's
  CHG-001-specific assertions (`change.id == "CHG-001"`, phase/status, a "Slices 1-6... Slice 7"
  history comment) match the context's implicit description of what needs generalizing.
- The rejected-approaches reasoning (no git-history-only deletion, no in-place historical banners, no
  merging/rewriting architecture or roadmap docs in this phase) is sound and appropriately scoped.
- The distinction between GG-SAD-as-product-semantics (paths inside the normative specification
  describing a GG-SAD-managed *consumer* project's document model) and this repository's own
  retired development governance is explicitly and correctly drawn — the same distinction my earlier
  design review raised, now correctly internalized.

## Findings

### CR-01 — The Active README Contract likely understates the actual scope of the README rewrite (moderate, informational)

Reading the current `README.md` directly shows the old constitution/ADR-hierarchy framing repeated
in at least four separate locations, not one: the overview ("evidence remain subordinate to it," ~L46),
the document-hierarchy list (`docs/constitution.md` → ADRs → `docs/project-brief.md` →
`docs/architecture.md`, ~L146–149), the repository-structure tree diagram (~L174–175, which also
still shows `docs/adr/`, `docs/definitions/`, and omits none of the files being archived), and a
compliance-framing section repeating "constitution" and "accepted ADRs" (~L367, L385, L393–395).
Separately, the entire "Project Status and Initial Scope" section (~L192–224) presents
`CHG-001-reference-repository-bootstrap` as "The first implementation change is..." — active,
current-tense — and ends with "See `docs/roadmap.md` for the implementation sequence," pointing
readers at the document being archived instead of `.planning/ROADMAP.md`.

The context's Active README Contract bullets are directionally correct but phrase this as reference
removal ("references... are removed," "claims... are removed"), which reads like isolated line edits.
In practice this requires replacing or substantially rewriting at least two whole sections (the
document-hierarchy explanation and the "Project Status and Initial Scope" section) and touching four
separate locations for the same recurring content. The contract also doesn't say what should replace
the removed document-hierarchy explanation — leaving a gap risks an incomplete rewrite that satisfies
"references removed" literally while leaving the reader without any explanation of current precedence
(where `AGENTS.md` already has one, and could simply be pointed to).

**Recommendation:** note explicitly in the README contract (or in whatever plan Phase 4 produces)
that the document-hierarchy section and the "Project Status and Initial Scope" section require
replacement rather than incremental editing, and that the replacement for the document-hierarchy
explanation should point to `AGENTS.md` / `.planning/` rather than leave the topic unaddressed.

### CR-02 — Test-Fixture Decoupling doesn't mention the module docstring, which also names CHG-001 (minor)

`tests/integration/test_governed_artifact_validation.py`'s module docstring (lines 1–8) describes the
file's origin as covering "CHG-001's own `state.yaml`" staying "schema-valid, model-parseable... as
the repository evolves." The context's Test-Fixture Decoupling section instructs updating "the two
tests and their names/comments" but doesn't mention this module-level docstring. Once the two tests
no longer read CHG-001's file, the docstring's specific claim becomes stale.

**Recommendation:** include the module docstring in the Test-Fixture Decoupling scope so it no longer
names CHG-001 as something the module currently validates.

## Disposition

Open. Neither finding blocks planning from proceeding — both are refinements to make Phase 4's
eventual plan and execution more complete on the first pass rather than requiring a follow-up
correction cycle, consistent with the pattern already seen in Phase 1–3 (findings caught before
planning cost less than findings caught after).
