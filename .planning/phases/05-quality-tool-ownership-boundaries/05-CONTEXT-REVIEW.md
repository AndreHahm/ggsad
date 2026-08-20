# Independent Review Findings — Phase 5 Context (Quality-Tool Ownership Boundaries)

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer
- Requestor: Codex
- Reviewed artifact: `.planning/phases/05-quality-tool-ownership-boundaries/05-CONTEXT.md`
- Reviewed revision: commit `a138481` ("docs(gsd): define phase 5 quality-tool boundaries")
- Review date: 2026-08-20
- Action: Review of the Phase 5 boundary/design context prior to planning
- Result: **Approved.** Every checkable claim verified accurate by direct testing, not just
  reading. No findings.
- Scope: Document review, verified empirically against the live repository and toolchain — actually
  running the prescribed commands rather than trusting the description. No repository files were
  modified as part of this review (a `uv build` test produced a gitignored `dist/` artifact only;
  `git status` confirmed no tracked changes).

## Method

Ran every command the context prescribes or contrasts against, directly in this environment, rather
than reasoning about them abstractly:

- `uv run ty check src tests` — result recorded.
- `uv run ty check` (bare, for contrast) — result recorded.
- `uv run ruff check .` and `uv run ruff format --check .` — results recorded.
- `uv run ruff check scripts/` — sanity check that dropping `scripts` from `extend-exclude` is safe
  given the directory's current (empty) content.
- `uv build` (plain) and `uv build --native-tls` — to verify the certificate-failure caveat is a live
  condition in this environment, not stale history.

Grepped `AGENTS.md`, `README.md`, `specs/examples/class-m/evidence.md`, and `CLAUDE.md` for their
current baseline-command text to verify the context's claims about which documents contain obsolete
commands (bare `uv sync`, bare `uv run ty check`).

## Findings verified against live execution

| Claim in `05-CONTEXT.md` | Verification | Result |
|---|---|---|
| `uv run ty check src tests` passes under `all = "error"` | Ran it | **Passes, 0 diagnostics** |
| Bare `ty check` scans `.claude/scripts` and produces diagnostics | Ran it | **31 diagnostics, all in `.claude/scripts`** — matches the count referenced throughout Phases 1–3 evidence |
| Ruff's existing config-backed exclude already works; no command change needed | Ran `ruff check .` / `ruff format --check .` | **Both pass clean** |
| Dropping `scripts` from Ruff's `extend-exclude` is safe (directory is currently empty) | Ran `ruff check scripts/` | **Benign warning, exit 0, "All checks passed!"** |
| Plain `uv build` can hit a certificate failure; `--native-tls` is the fallback | Ran both | **Plain `uv build` failed with `invalid peer certificate: UnknownIssuer`; `uv build --native-tls` succeeded** — this is a live condition in this environment right now, not just historical |
| `AGENTS.md` line ~30 still has bare `uv run ty check` | Grep | **Confirmed** |
| `README.md` line ~93 still has bare `uv run ty check` | Grep | **Confirmed** |
| `specs/examples/class-m/evidence.md` still has bare `uv sync` and bare `uv run ty check` | Grep | **Confirmed** (lines 52, 55) |
| `CLAUDE.md` already delegates to `AGENTS.md`, no duplicate command block | Grep | **Confirmed, zero matches** |

## Scope-consistency check

`specs/examples/class-m/evidence.md` being in scope for Phase 5 is not new scope creep: Phase 4's
"Explicitly Retained Active Artifacts" section already named product examples as "retained for later
quality-boundary and conformance phases," correctly foreshadowing this.

## Architectural assessment

The hybrid approach — Ruff keeps its working, config-backed `extend-exclude`; `ty` gets an explicit
owned-path command because its CLI exposes no config-backed include option — matches the
recommendation I gave when Codex asked about applying the `ty` pattern to Ruff for consistency: don't
switch a mechanism that's empirically already working (Ruff) to match one that was adopted out of
necessity for a tool that lacks the same config option (`ty`). The one real, previously-latent defect
I identified in that discussion — `scripts` sitting in Ruff's `extend-exclude` despite the project's
own stated intent to include "owned scripts" in quality-tool scope — is explicitly fixed here.

## Disposition

Approved. No findings. Ready for Phase 5 plan authoring.
