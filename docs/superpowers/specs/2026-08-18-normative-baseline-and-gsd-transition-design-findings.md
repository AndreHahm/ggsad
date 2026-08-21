# Independent Review Findings — Normative Baseline and GSD Transition Design

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer (as assigned by the reviewed document)
- Requestor: Codex
- Reviewed artifact: `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`
- Reviewed artifact revision: `800a004e7c8d7a565c34deab1b3aa61f9b1b6492` (2026-08-18T11:03:15+02:00)
- Review date: 2026-08-18
- Action: Review of design document prior to owner approval (transition sequence step 1)
- Result: Not ready for owner sign-off as written; no blocking defect in the design's diagnosis or approach
- Scope: Design-document review only. No implementation, no normative amendment, and no repository
  files were modified as part of this review (Pair Review rule: a Reviewer must not silently edit the
  Requestor's governed work product).

## Method

Findings were derived by reading the design document and cross-checking its claims against actual
repository state: `git status`/`git diff`, `AGENTS.md`, `CLAUDE.md`, `CLAUDE_CODE_PROJECT_START.md`,
`specs/CHG-001-reference-repository-bootstrap/state.yaml`, root directory listing, and
`.claude/gsd-core/VERSION`.

## Findings

### F-01 — Uncommitted diff is unrelated noise, not part of the amendment (non-blocking, housekeeping)

`git diff` shows a stray blank-line insertion at line 2 of
`docs/method/GG-SAD_normative_method_specification.md` with no semantic content. The design's own
transition sequence places "prepare the normative amendment" at step 3, not yet reached. This edit
should be reverted or explained before further work proceeds.

### F-02 — `CLAUDE.md` and `CLAUDE_CODE_PROJECT_START.md` are not named among artifacts to retire/rewrite (blocking for approval)

The "Existing repository treatment" section lists "root development constitution and agent rules
that impose GG-SAD workflow" for retirement/rewrite, but does not name two root files that impose
the same GG-SAD-as-development-governance model:

- `CLAUDE_CODE_PROJECT_START.md` — duplicates `AGENTS.md`'s hierarchy and Requestor-role text.
- `CLAUDE.md` — governs the reviewing/implementing agent directly (Requestor role, DoF/DoW/DoD/DoR
  reporting format, `CHG-001`-scoped "Initial Change Constraint" section).

This is the most consequential gap: if the transition proceeds without updating `CLAUDE.md`, the
implementing agent remains bound to instructions describing a governance model the transition is
meant to end (e.g., "act as Requestor," "map outcomes to `specs/<change-id>/evidence.md`").

### F-03 — Bootstrap authorization claim has no evidence trail (blocking for approval)

Line 10 asserts owner authorization for skipping a GG-SAD change as settled fact, while the
document's own status line reads "Draft for owner review" and step 1 of its sequence is "Approve
this design." Per `CLAUDE.md`'s Human Approval Boundaries, scope-governance changes require
explicit human approval, and material deviations must not be treated as accepted on an agent's
say-so. This claim should be confirmed directly with the repository owner rather than accepted from
the draft as written.

### F-04 — "Decisions" section reads as already settled despite being pre-approval (non-blocking, clarity)

Items such as "GSD Core is the sole development method" are phrased as accepted fact ahead of the
step-1 approval gate. Consider relabeling as "Proposed decisions" until owner sign-off closes.

### F-05 — Sequencing vs. actual repo state: GSD Core is already installed, not yet "onboarded" (non-blocking, needs reconciliation)

`.claude/gsd-core/VERSION` is `1.9.1` and the GSD command/agent set is already present in the tree,
but no `.planning/` directory exists yet, so it has not been used for real planning. Transition
sequence step 6 ("Pin and cleanly onboard current stable GSD Core") is written as future work but
the install already happened via a prior commit. The design should state whether "clean onboarding"
means treating the existing 1.9.1 install as the pinned version or reinstalling.

### F-06 — CHG-001's own state.yaml corroborates the design's diagnosis (informational, supports the design)

`specs/CHG-001-reference-repository-bootstrap/state.yaml` shows `flow.phase: specify` even after
Build and Verify-Done work completed (Pair Review verified, 0 open blocking findings, per the
2026-08-04 history entries). The phase field never advanced past `specify` across six implementation
slices and a full review cycle — a present-day, concrete instance of the ambiguous state narrative
the design's Section 3 sets out to fix. This strengthens rather than weakens the case for the
redesign.

### F-07 — Quality baseline in the design omits `uv sync` (non-blocking, low priority)

`AGENTS.md`'s baseline begins with `uv sync`; the design's "Quality and verification" block starts
at `ruff format --check`. Likely an omission of the environment-prep step rather than an intended
scope change.

## Disposition

Open. Awaiting Requestor (Codex) and/or repository-owner disposition on F-02 and F-03 before this
design can be considered ready for step-1 approval. F-01, F-04, F-05, and F-07 are non-blocking and
may be resolved alongside or folded into the eventual normative amendment/onboarding work. F-06 is
informational and requires no action.
