---
phase: 05-quality-tool-ownership-boundaries
verified: 2026-08-21
status: passed
score: 4/4 must-haves verified
behavior_unverified: 0
---

# Phase 5: Quality-Tool Ownership Boundaries Verification Report

**Phase Goal:** Explicitly scope product quality tools, exclude installer-owned GSD runtime files,
and standardize locked sync and strict `ty` across retained active documentation.

**Status:** passed

## Goal Achievement

| # | Truth | Status | Evidence |
|---|---|---|---|
| 1 | Ruff includes owned Python surfaces and excludes installer tooling. | VERIFIED | `.claude` remains in `extend-exclude`; `scripts` no longer does; root Ruff checks pass. |
| 2 | Strict `ty` checks only owned paths. | VERIFIED | `uv run ty check src tests` passes with zero diagnostics under `all = "error"`. |
| 3 | Active baselines use locked dependency sync. | VERIFIED | Drift scan finds no bare `uv sync`; all intended surfaces contain `uv sync --locked`. |
| 4 | Active baselines use the scoped `ty` command only. | VERIFIED | Drift and `mypy|pyright` scans return no matches; all intended surfaces contain `uv run ty check src tests`. |

**Score:** 4/4 truths verified

## Requirements Coverage

| Requirement | Status | Evidence |
|---|---|---|
| TOOL-01 | SATISFIED | Ruff, strict `ty`, pytest, and coverage have explicit owned-source boundaries. |
| TOOL-02 | SATISFIED | Installer-owned `.claude` remains excluded and protected from Phase 5 changes. |
| TOOL-03 | SATISFIED | Active command surfaces contain locked sync and no bare sync command. |
| TOOL-04 | SATISFIED | Scoped strict `ty` is the sole active type-check baseline; no `mypy` or `pyright` baseline exists. |

## Configuration and Drift Evidence

- `rg -n '^\s*"\.claude",$' pyproject.toml` — `.claude` present at line 69.
- `rg -n '^\s*"scripts",$' pyproject.toml` — no match (exit 1).
- `rg -n --pcre2 'uv sync(?! --locked)|uv run ty check(?! src tests)' AGENTS.md README.md specs/examples/class-m/evidence.md`
  — no match (exit 1).
- `rg -n 'mypy|pyright' AGENTS.md README.md specs/examples/class-m/evidence.md CLAUDE.md`
  — no match (exit 1).
- Positive scans confirm `uv sync --locked` and `uv run ty check src tests` in every intended
  active command surface.

## Scope Evidence

- `git diff --name-status c2268a3..HEAD` before closure evidence showed only the Phase 5 plan and
  review artifacts plus `pyproject.toml`, `AGENTS.md`, README, and the active Class M example.
- `git diff --exit-code c2268a3..HEAD -- docs/method/GG-SAD_normative_method_specification.md src/ggsad tests .ggsad .claude archive`
  — no differences.
- No wrapper, permanent policy test, placeholder scripts directory, dependency, rule suppression,
  warning downgrade, or exit-zero behavior was added.

## Engineering Baseline

- `uv sync --locked` — passed; 44 packages audited.
- `uv run ruff format --check .` — passed; 114 files already formatted.
- `uv run ruff check .` — passed.
- `uv run ty check src tests` — passed with zero diagnostics.
- `uv run pytest` — passed: 150 tests, 98.58% coverage.
- `uv build` — passed; source distribution and wheel built successfully.
- `node .claude/gsd-core/bin/gsd-tools.cjs validate consistency` — passed with three expected
  warnings for future Phase 6–8 directories not yet created.

After `pyproject.toml` changed, the first combined `uv run` attempt triggered an editable-package
refresh and failed before tool execution with `invalid peer certificate: UnknownIssuer`. A locked
`uv sync --locked --native-tls` rebuilt the editable package successfully; the unchanged canonical
commands then passed. The final required plain `uv build` also passed directly, so no build fallback
was needed.

## Review Finding Disposition

PLR5-01 was accepted and resolved in plan revision `0f45ab1`: Task 3's automated verification now
includes configuration assertions, documentation drift scans, and explicit handling of the plain
build result before any native-TLS fallback.

## Gaps Summary

No Phase 5 gaps remain. Phase 6 is unstarted.

---
*Verifier: Codex; implementation executed from the owner-approved and independently reviewed Phase 5 plan*
