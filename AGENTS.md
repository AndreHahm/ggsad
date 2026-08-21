# Agent Instructions

## Product authority

`docs/method/GG-SAD_normative_method_specification.md` is the leading source for GG-SAD method
semantics and reference-implementation behavior. Development artifacts must not redefine it.

## Development method

This repository uses pinned GSD Core 1.10.0 as its sole development method. Read and follow the
active `.planning/` project, requirements, roadmap, state, context, plans, and verification
artifacts. Do not create or advance GG-SAD change state to govern repository development.

## Approval and review

Changes to the English normative specification require explicit repository-owner approval and
independent review by Claude Code. A fresh context or subagent of the Requestor is not independent.

## Engineering baseline

Use Python with explicit type annotations, uv, Typer, Pydantic v2, ruamel.yaml, JSON Schema,
pytest, Hypothesis where valuable, Ruff, and ty strict checking. Preserve unrelated changes,
avoid destructive Git operations, do not commit secrets, and report checks that were not run.

Run the applicable baseline before completion:

`uv sync --locked`
`uv run ruff format --check .`
`uv run ruff check .`
`uv run ty check src tests`
`uv run pytest`
`uv build`

Installer-owned GSD files are development tooling, not Python product source. Product quality-tool
scope must be defined explicitly rather than weakened to hide product diagnostics.
