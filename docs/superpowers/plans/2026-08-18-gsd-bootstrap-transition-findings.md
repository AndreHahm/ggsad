# Independent Review Findings — GSD Bootstrap Transition Plan

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer (per the governing design's assignment)
- Requestor: Codex
- Reviewed artifact: `docs/superpowers/plans/2026-08-18-gsd-bootstrap-transition.md`
- Reviewed artifact revision: `dd1aadd3c4f0fdc4a756c9574ba03020751887d7` (2026-08-18T11:57:40+02:00)
- Governing design artifact: `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`
- Governing design revision: `4c5735b66fc6b3a54c5c066d28f9e5794bc69a1e` (2026-08-18T11:51:58+02:00,
  Status: Approved)
- Review date: 2026-08-18
- Action: Verification of the bootstrap plan against the approved, current-revision design
- Result: Plan conforms to the design on all major points; no blocking findings; three non-blocking
  gaps identified
- Scope: Plan-document review only. No implementation, no plan edits, and no repository files were
  modified as part of this review.

## Method

Read the plan in full and cross-checked it clause-by-clause against the design's *current* revision
(the design was revised and approved after my earlier review of commit `8377892`, including
disposition of findings F-01 through F-07 and a resequencing of the transition steps — see
`docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design-findings.md`).
Also verified specific factual claims in the plan against live repository state: `git status`,
`git log`, `.claude/gsd-core/VERSION`, `.claude/gsd-file-manifest.json`,
`.claude/gsd-install-state.json`, `.claude/package.json`, `.claude/settings.json`.

## Conformance summary

- Task ordering (capture baseline → install GSD 1.10.0 → neutralize `AGENTS.md`/`CLAUDE.md`/
  `CLAUDE_CODE_PROJECT_START.md` → onboard → close) matches the design's revised 13-step transition
  sequence exactly, including the resequencing that places GSD onboarding before the normative
  amendment.
- The GSD pin (`1.10.0`, upgrading the existing unonboarded `1.9.1` install rather than reinstalling)
  matches the design's "GSD baseline" section precisely. `.claude/gsd-core/VERSION` currently reads
  `1.9.1`, confirming the plan's stated starting state.
- The engineering-baseline command block in the plan's `AGENTS.md` replacement text
  (`uv sync --locked`, `ruff format --check`, `ruff check`, `ty check`, `pytest`, `uv build`) is
  identical, in the same order, to the design's "Quality and verification" section.
- Task 4 Step 4's seven required roadmap outcomes map one-to-one onto design transition-sequence
  steps 6 through 13.
- The design's non-goals list (no profile resolution, gate engine, memory, MCP, web UI, CI,
  multi-agent orchestration) is reproduced verbatim as a roadmap-rejection condition in Task 4 Step 4.
- Deleting `CLAUDE_CODE_PROJECT_START.md` and fully replacing `AGENTS.md`/`CLAUDE.md` directly
  implements the design's disposition of F-02 from the design-review findings.
- All files the plan reads or references as pre-existing (`.claude/gsd-file-manifest.json`,
  `.claude/gsd-install-state.json`, `.claude/package.json`, `.claude/settings.json`) exist in the
  repository as stated. The working tree is clean, confirming the earlier F-01 stray-diff finding
  against the design has already been resolved.

## Findings

### PF-01 — Task 5's product-code diff check omits `.ggsad/` and `specs/examples/` (non-blocking, completeness gap)

The plan's global constraints forbid modifying "product schemas, templates, or examples," and the
design's "Retain initially" list names these explicitly. Task 5 Step 2's verification only diffs
`src tests pyproject.toml uv.lock` against `main`. If the GSD installer or onboarding step touched
`.ggsad/schemas`, `.ggsad/templates`, or `specs/examples/`, this plan would not catch it.

**Recommendation:** extend the diff command to `git diff main...HEAD -- src tests pyproject.toml uv.lock .ggsad specs/examples`.

### PF-02 — No explicit rollback step for Task 4 (onboarding), unlike Task 1 (non-blocking, procedural gap)

The design's "Safety and rollback" section states: "If onboarding fails, revert only the onboarding
change and retain the reviewed normative baseline and Python implementation." Task 1 has an explicit
"Stop on unexpected state" step; Task 4 only has per-step "Expected:" conditions with no equivalent
instruction scoped to reverting *only* the onboarding commit. Since onboarding is committed
separately in Task 4 Step 7, a targeted `git revert` of that single commit is exactly what the
design calls for and should be stated explicitly rather than left to an implicit "stop" convention.

**Recommendation:** add a step to Task 4 (or a Task 4 "Step 8: Roll back on failure") instructing a
`git revert` of the Task 4 Step 7 onboarding commit only, preserving the Task 2 and Task 3 commits,
if any Task 4 verification step fails.

### PF-03 — `@opengsd/gsd-core` package identity is asserted, not verified against repo state (informational, shared with the design)

Neither `.claude/gsd-install-state.json` nor `.claude/package.json` records the installer's npm
package name, so this could not be independently confirmed from repository state alone. This is not
a plan-vs-design deviation — both documents assert the same package name — and Task 2 Step 1 will
surface a wrong package name immediately as an installer resolution failure. Noted for awareness
during execution, not as a defect.

## Disposition

Open. PF-01 and PF-02 are recommended fixes to the plan before execution begins; both are small,
additive changes that do not alter task ordering, scope, or the approved design. PF-03 requires no
plan change, only attention at Task 2 Step 1 execution time. No blocking findings were identified —
the plan may proceed to execution once PF-01/PF-02 are dispositioned by the Requestor.
