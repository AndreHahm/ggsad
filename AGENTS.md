# Agent Instructions

## Product authority

`docs/method/GG-SAD_normative_method_specification.md` is the leading source for GG-SAD method
semantics and reference-implementation behavior. Development artifacts must not redefine it.

## Development method

This repository is developed with plain, small, reviewable commits on short-lived branches. No
plan, summary, review brief, or state file is required for a change. Do not create or advance
GG-SAD change state to govern repository development.

## Approval and review

Changes to the English normative specification require explicit repository-owner approval and
independent review by a reviewer that is not the Requestor. A fresh context or subagent of the Requestor is not independent.
The review is bounded as Section 14.3 of the specification states: one review round and at most one
re-check. The owner dispositions each finding as fix, defer, or reject.

## Engineering baseline

Use Python with explicit type annotations, uv, argparse, ruamel.yaml, pytest, Hypothesis where
valuable, Ruff, and ty strict checking. Preserve unrelated changes,
avoid destructive Git operations, do not commit secrets, and report checks that were not run.

Run the applicable baseline before completion:

`uv sync --locked`
`uv run ruff format --check .`
`uv run ruff check .`
`uv run ty check src tests`
`uv run pytest`
`uv build`

Product quality-tool scope must be defined explicitly rather than weakened to hide product
diagnostics.
