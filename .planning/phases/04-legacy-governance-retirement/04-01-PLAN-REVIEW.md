# Plan Conformance Review — 04-01-PLAN.md

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer
- Requestor: Codex
- Reviewed artifact: `.planning/phases/04-legacy-governance-retirement/04-01-PLAN.md`
- Reviewed against: `.planning/phases/04-legacy-governance-retirement/04-CONTEXT.md` (revision
  `6ee1f2f`, which already incorporates both `04-CONTEXT-REVIEW.md` findings CR-01 and CR-02),
  `.planning/phases/04-legacy-governance-retirement/04-CONTEXT-REVIEW.md`, and roadmap requirements
  RETIRE-01 through RETIRE-05
- Review date: 2026-08-20
- Action: Plan-conformance check before Phase 4 execution
- Result: Conforms well; one concrete, moderate finding (an incomplete automated safety net for
  stale-reference detection); everything else verified accurate, including an empirical schema/model
  validation of the plan's literal fixture content
- Scope: Plan-document review, cross-checked against actual repository state (README.md content by
  section, the target test file, the state JSON Schema, and a repo-wide search for archived-path
  references outside excluded locations). No repository files were modified as part of this review.

## Method

Confirmed `04-CONTEXT.md` was updated (commit `6ee1f2f`, "incorporate phase 4 context review") to
directly incorporate both findings from `04-CONTEXT-REVIEW.md` before this plan was written — CR-01
(README sections needing replacement, and where the replacement should point) and CR-02 (module
docstring in scope for the test-fixture decoupling) are both now explicit in the context. Verified
each plan task against the corrected context and against RETIRE-01–05. Read the actual `README.md`
by section (mapped every previously-flagged line number to its enclosing `##`/`###` heading) to
determine which sections are genuine repo-governance claims requiring rewrite versus legitimate
product documentation describing GG-SAD's own operating modes — the plan's task text needs to draw
this distinction correctly for its "preserve" vs. "replace" instructions to be safe. Extracted the
plan's literal fixture YAML and validated it against the actual `.ggsad/schemas/state.schema.json`
and `ChangeState` Pydantic model in a throwaway script — it passes both with zero issues. Ran a
repo-wide search for every archived path pattern outside `.planning/`, `docs/superpowers/`, and
`archive/` to confirm no other active file needs touching beyond what the plan already scopes.

## What checked out

- **Requirement mapping**: RETIRE-01 (classify all 29) → Task 2. RETIRE-02 (architecture disposition)
  → Task 2's manifest note ("both architectures were retired without a replacement"). RETIRE-03
  (roadmap disposition, preserving `docs/roadmap.md`'s delivery-status content) → Task 2's manifest
  note plus byte-identical archival. RETIRE-04 (no longer active governance) → Tasks 2–4 jointly.
  RETIRE-05 (CHG-* not conformance proof) → Task 1 (test decoupling) + Task 2 (manifest note) + Task 4.
  All five requirements have a concrete, traceable implementation path in the plan.
- **Arithmetic**: "eight individual root-level legacy docs" (constitution, project-brief, both
  architecture files, both roadmaps, implementation guide, workflow reference) + 8 ADRs + 4
  definitions + 2 guides + 1 DE spec + 5 CHG-001 files = 28, plus the already-absent startup file =
  29. Matches the context's inventory count exactly.
- **CR-01 resolution**: Task 3's action text is more precise than the corrected context itself —
  it explicitly names every section requiring replacement (GSD Integration → Repository Authority
  and Development Method; Document Hierarchy → short authority-pointer section; Repository Structure
  tree; Project Status and Initial Scope → Current Development Status; Development Workflow and
  Contributing), and explicitly instructs pointing the new authority section at `AGENTS.md` and
  `.planning/`. I independently read every README section by heading (Core Model, Key Capabilities,
  Operating Modes, Templates) that my original CR-01 finding's grep hits touched, and confirmed those
  are legitimate product documentation about GG-SAD's own operating modes — correctly left in the
  "preserve" list, not the "replace" list. The plan draws this line correctly.
- **CR-02 resolution**: Task 1's action explicitly includes "Rewrite the module docstring to say the
  module validates the repository's active configuration, mapping, and representative state fixture;
  it must not name CHG-001," and the acceptance criteria's prohibited-text scan ("no `CHG-001`,
  `chg_001`, `Slice`, or `specs/CHG-001` text") would catch the docstring specifically since it's part
  of the same module.
- **Fixture validity, empirically verified**: I copied the plan's literal fixture YAML into a
  throwaway file and ran it through the actual `load_schema`/`validate_against_schema` and
  `ChangeState.model_validate` calls this repository uses. Zero schema issues; model parses with
  `change.id="CHG-900"`, `flow.phase="specify"`, `flow.status="ready"` exactly as the acceptance
  criteria require. The `pair_review.requestor: null` / `reviewer: null` values are valid — the
  schema's `pairReviewParticipant` type explicitly allows `["object", "null"]`.
- **TDD sequencing**: Task 1 correctly runs the renamed test before creating the fixture and expects
  a missing-file failure, then creates the fixture — genuine red-then-green, not just cosmetic `tdd`
  framing.
- **Windows/shell-path awareness**: Task 2's explicit instruction to use "native PowerShell
  `Move-Item -LiteralPath` or `git mv` end-to-end; do not enumerate paths in one shell and move them
  through another" reflects real awareness of this environment's git-bash/PowerShell path-translation
  issues (I hit exactly this class of problem myself earlier in this session testing the fixture).
- **Scope boundary**: a repo-wide search for every archived-path pattern outside `.planning/`,
  `docs/superpowers/`, and `archive/` turned up only expected, already-scoped hits: installer-owned
  `.claude/` content (explicitly excluded), `.ggsad/`/`src/ggsad/` product templates and mappings that
  describe the *product's* document model for consumer projects (explicitly protected and correctly
  distinct from this repo's own governance), the normative specification's own Section 4.2 (same
  product-model distinction), a product example fixture, and product-behavior tests for `ggsad init`.
  Nothing outside the plan's declared `files_modified` needs touching.
- Task 4's revision anchor `6ee1f2f` is a real commit ("incorporate phase 4 context review").

## Finding

### PLR4-01 — No fully automated check that active files don't reference any archived path (moderate)

Task 3's automated verify command is a targeted `rg` pattern:

```
docs/constitution\.md|docs/project-brief\.md|docs/architecture(?:-reference)?\.md|docs/(?:implementation-)?roadmap\.md|specs/CHG-001|GSD artifacts.*subordinate|GSD does not own|@opengsd/gsd-core@latest
```

It does not include `docs/adr`, `docs/definitions`, `docs/guides`, `docs/workflow-reference`,
`docs/implementation-guide`, or the DE-spec filename. Of these, `docs/adr` is a live gap right now:
the current `README.md` references `docs/adr/ADR-0006-...` (line 138, inside the section Task 3
names "GSD Integration") and `docs/adr/` generically (line 147, inside "Document Hierarchy") — both
locations Task 3's action text correctly targets for replacement, but neither would be automatically
re-checked by Task 3's own verify command if the rewrite missed one of them.

Task 4's action then says to "scan active files... no active repository-governance instruction may
point to an archived path," which is the right requirement — but Task 4's `<verify>` block is only
the general baseline (`uv sync --locked && ruff format/check && pytest && uv build`); there is no
automated command anywhere in the plan that actually performs this scan. RETIRE-04's core promise
("no longer read as active development governance by any agent instruction file") currently depends
on unaided manual review rather than a repeatable command.

I ran a repo-wide search for every archived-path pattern (excluding `.planning/`,
`docs/superpowers/`, and `archive/`) myself and confirmed `README.md` is the only in-scope file that
still needs it — so the actual risk surface is small — but the plan itself has no command that would
catch a regression here on a future re-run.

**Recommendation:** either extend Task 3's `rg` pattern to include `docs/adr`, `docs/definitions`,
`docs/guides`, `docs/workflow-reference`, `docs/implementation-guide`, and the DE-spec filename, or
add one explicit automated command to Task 4 — something like
`rg -l -E 'docs/constitution|docs/project-brief|docs/architecture|docs/(implementation-)?roadmap|docs/adr|docs/definitions|docs/guides|docs/workflow-reference|docs/implementation-guide|GG-SAD_normative_method_specification_DE|specs/CHG-001' -- . ':!archive' ':!.planning' ':!.claude' ':!docs/superpowers' ':!.ggsad' ':!src/ggsad' ':!specs/examples' ':!tests'`
(scoped to exclude the confirmed-legitimate product/installer hits) — so RETIRE-04's verification is
a deterministic, re-runnable check rather than a one-time manual scan.

## Disposition

Open. PLR4-01 is a verification-robustness gap, not a content defect — the plan's instructions are
correct, only its automated safety net is incomplete. Does not block execution, but should be
resolved before or during Task 4 so RETIRE-04 has a repeatable check rather than relying on manual
diligence alone.
