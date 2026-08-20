# Phase 5 Context — Quality-Tool Ownership Boundaries

## Status

Design approved by the repository owner on 2026-08-20. This artifact defines the boundary for
Phase 5 planning and execution.

## Goal

Make product quality-tool ownership explicit, remove installer-owned GSD runtime files from Python
product analysis, and standardize the retained active documentation on locked dependency sync and
strict `ty` checking without adding unnecessary automation.

## Selected Approach

Use a hybrid tool-native ownership boundary:

- Ruff keeps repository-root commands and configuration-backed exclusions.
- `ty` receives an explicit owned-path allowlist on the command line.
- pytest discovery and coverage remain configuration-backed.
- Retained active documentation uses one canonical baseline.
- Deterministic verification scans enforce this phase; no wrapper or permanent policy test is
  added.

This approach uses the strongest scoping mechanism exposed by each pinned tool while keeping
automation minimal.

Rejected approaches:

- A wrapper command, because it adds another maintained abstraction without improving the current
  tool guarantees.
- Exclusion-only scoping for every tool, because `ty` would depend on an expanding denylist and
  could silently absorb newly installed tooling.
- Explicit-path Ruff commands, because the owner selected Ruff's existing configuration-backed
  boundary.

## Ownership Boundary

Owned Python scope is:

- `src/` — product implementation;
- `tests/` — owned test code and fixtures;
- a future repository-owned `scripts/` directory, if one is introduced.

Installer-managed `.claude/` content, including GSD Core, hooks, agents, skills, and scripts, is
development tooling rather than Python product source. Its diagnostics must not be hidden through
rule suppression or exit-zero behavior; it is outside the product quality boundary by ownership.

Other excluded non-product surfaces remain outside Ruff's configured scope. Phase 5 must remove
`scripts` from Ruff's `extend-exclude` list so a future owned scripts directory is not excluded by
default. `.claude` remains explicitly excluded.

## Tool-Specific Scope

### Ruff

Keep configuration-backed scope and repository-root invocations:

```text
uv run ruff format --check .
uv run ruff check .
```

The existing `extend-exclude` list remains, except that `scripts` is removed. Phase 5 does not
switch Ruff to explicit command-line paths.

### ty

Use the explicit owned-path command:

```text
uv run ty check src tests
```

The pinned `ty` CLI exposes path arguments and exclusions but no configuration-backed include
allowlist. Explicit paths prevent repository-root discovery from entering `.claude/`. The existing
strict-mode equivalent remains:

```toml
[tool.ty.rules]
all = "error"
```

No `mypy`, `pyright`, diagnostic suppression, warning downgrade, or exit-zero fallback is added.

If a repository-owned Python `scripts/` directory is introduced later, the canonical command must
become `uv run ty check src tests scripts` in the same change.

### pytest and coverage

Keep pytest discovery rooted at `tests/` and coverage focused on the existing `ggsad` product
package. No placeholder scripts directory or nonexistent coverage source is created.

If owned Python scripts are introduced later, that change must add them to the configured coverage
source and test them through `tests/`.

## Canonical Baseline

Retained active documentation must use exactly this baseline:

```text
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check src tests
uv run pytest
uv build
```

Phase 5 updates:

- `AGENTS.md`;
- `README.md`;
- `specs/examples/class-m/evidence.md`.

The Class M example is illustrative rather than repository governance, but it must not teach the
obsolete bare sync or repository-wide type-check commands. Archived documents remain unchanged.
`CLAUDE.md` already delegates to `AGENTS.md` and requires no duplicate command block.

## Minimal-Automation Boundary

Phase 5 adds neither a quality wrapper nor a permanent policy-regression test. Compliance is
demonstrated through repeatable verification commands recorded in the phase evidence. The active
agent instructions remain the maintained source for the repository baseline.

## Scope Boundaries

Phase 5 may change only:

- quality-tool configuration in `pyproject.toml`;
- `AGENTS.md`;
- `README.md`;
- `specs/examples/class-m/evidence.md`;
- Phase 5 `.planning/` artifacts.

Phase 5 must not change:

- the English normative specification;
- product implementation under `src/ggsad/`;
- tests or product behavior;
- installer-owned `.claude/` files;
- archived historical material;
- schemas, templates, profiles, or mappings under `.ggsad/`.

## Verification Contract

Completion evidence must prove:

1. Ruff's configuration still excludes `.claude` and no longer excludes `scripts`.
2. `uv run ty check src tests` passes under `all = "error"`.
3. Retained active documents contain `uv sync --locked`, not bare `uv sync`.
4. Retained active documents use `ty`, not `mypy` or `pyright`, as the type-check baseline.
5. No retained active command uses bare `uv run ty check` without `src tests`.
6. `AGENTS.md`, README, and the active Class M example agree on the canonical baseline.
7. The English normative specification, product source, tests, `.ggsad/`, `.claude/`, and archive
   remain unchanged.
8. Ruff formatting and linting, strict scoped `ty`, pytest, packaging, and GSD consistency are run.

A plain `uv build` certificate failure, if it recurs, must be recorded as an environment failure.
A subsequent successful `uv build --native-tls` may demonstrate package correctness but does not
erase the plain-command result.

## Completion Boundary

Phase 5 closes only after TOOL-01 through TOOL-04 have explicit evidence and the quality-tool
boundary passes its verification contract. Phase 6 does not start automatically.
