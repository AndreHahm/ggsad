# Plan Conformance Review — 05-01-PLAN.md

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer
- Requestor: Codex
- Reviewed artifact: `.planning/phases/05-quality-tool-ownership-boundaries/05-01-PLAN.md`
- Reviewed against: `.planning/phases/05-quality-tool-ownership-boundaries/05-CONTEXT.md`,
  `.planning/phases/05-quality-tool-ownership-boundaries/05-CONTEXT-REVIEW.md`, and roadmap
  requirements TOOL-01 through TOOL-04
- Review date: 2026-08-20
- Action: Plan-conformance check before Phase 5 execution
- Result: Conforms; one minor-to-moderate finding (automated verify block narrower than its own
  action prose); no blocking issues
- Scope: Plan-document review, verified empirically by running the plan's exact prescribed commands
  against the live repository rather than reading them for plausibility only. No repository files
  were modified as part of this review.

## Method

Ran every regex and drift-probe command the plan specifies directly against the current repository
state:

- Task 1's pre-change capture command (`rg` for `.claude`/`scripts` in Ruff's `extend-exclude`).
- Task 2's two drift probes (bare `uv sync`, bare `uv run ty check`) against all three target files.
- Simulated the post-edit text through the same negative-lookahead pattern to confirm it correctly
  reports zero matches once the fix is applied, not just that it plausibly should.
- Counted occurrences of `uv run ty check` in each target file to rule out a second instance being
  missed by a single-replace instruction.
- Verified the Task 3 revision anchor (`c2268a3`) is a real commit and is exactly the commit that
  recorded `05-CONTEXT-REVIEW.md` — the correct Phase 5 starting point.

## What checked out

- **Requirement mapping**: TOOL-01 (explicit scope) → Task 1. TOOL-02 (exclude installer-owned
  files) → Task 1 (`.claude` retained in `extend-exclude`, verified unchanged). TOOL-03 (`uv sync
  --locked` sole baseline) → Task 2. TOOL-04 (`ty` sole documented type-checker, closing the
  CONCERNS.md tooling-drift entry) → Task 2's `mypy|pyright` scan. All four have a concrete,
  verifiable implementation path.
- **Task 1's exact `rg` commands** correctly match the current `pyproject.toml`: both `.claude`
  (line 69) and `scripts` (line 77) are found by the combined pre-check pattern; the two
  post-edit-simulation patterns (`.claude` present / `scripts` absent) behave exactly as the
  acceptance criteria expect.
- **Task 2's drift probes** correctly and exactly identify the three obsolete references that exist
  right now — `specs/examples/class-m/evidence.md:52` (bare `uv sync`), and `AGENTS.md:30`,
  `README.md:93`, `evidence.md:55` (bare `uv run ty check`) — no more, no fewer. I independently
  confirmed each target file has exactly one `uv run ty check` occurrence, so a single substitution
  per file is sufficient and no second instance will be missed.
- **The PCRE2 negative-lookahead logic is sound**, not just plausible: I built the "already fixed"
  text by hand and ran it through the identical pattern, confirming it correctly reports zero matches
  (`rg` exit 1) once `uv sync --locked` / `uv run ty check src tests` are in place.
- **Scope boundaries and protected-file list** match `05-CONTEXT.md` exactly; `CLAUDE.md` is
  correctly left untouched (already delegates, no duplicate command block, consistent with what I
  verified in the context review).
- The Task 3 revision anchor `c2268a3` is real and correct.

## Finding

### PLR5-01 — Task 3's automated `<verify>` block is narrower than its own `<action>` prose requires (minor-to-moderate)

Two concrete gaps between what Task 3's action text mandates and what its `<verify>` shortcut
actually runs:

1. The action requires: "If plain `uv build` fails with the confirmed `UnknownIssuer` environment
   condition, record the failure verbatim and run `uv build --native-tls`." I confirmed in the
   context review that plain `uv build` *does* currently fail this way in this environment — not a
   hypothetical edge case, a live, reproducing condition. The `<verify>` block skips straight to
   `uv build --native-tls`, so an executor who runs only the automated shortcut would never capture
   the honest failure record the action explicitly requires.
2. The action requires re-running "the configuration assertions and retained-document drift scans
   from Tasks 1 and 2," but the `<verify>` block only re-runs the quality-tool chain
   (`ruff`/`ty`/`pytest`/`build`), not the four `rg` drift-scan commands from Tasks 1–2.

Neither is a content defect — a careful executor reading the full task will still do the right
thing — but the automated shortcut silently drops two steps the prose explicitly mandates, which is
exactly the class of drift that causes problems on a rushed or partially-automated re-run.

**Recommendation:** add the plain-`uv build` attempt (with its expected/honest failure recorded) and
the four Task 1/2 drift-scan commands to Task 3's `<verify>` block so the automated check matches
what the action text requires.

## Disposition

Open. PLR5-01 is a verification-robustness gap, not a content defect. Does not block execution, but
should be resolved before or during Task 3 so the automated check captures everything the action
prose already correctly requires.
