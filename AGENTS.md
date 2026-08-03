# Agent Instructions

## Purpose

This file defines the general rules for every human-operated or autonomous agent working in the **GG-SAD reference implementation** repository.

These rules apply to Claude Code, Codex, Gemini CLI, OpenCode, IDE agents, review agents, automation agents, and any future agent integration. Tool-specific instruction files may add stricter rules, but they must not weaken this file or any higher-precedence project artifact.

## Governing Method

The project uses **Goal-Gated Spec-Anchored Development (GG-SAD)** as the governing method.

GG-SAD owns:

- goals and approved scope;
- document precedence;
- change classification;
- workflow phase and status;
- Definition of Ready, Done, Wait, and Fail;
- evidence requirements;
- Pair Review rules;
- approvals and closure.

Companion methods and tools, including GSD, may support planning, context engineering, implementation, review, and verification. They do not own GG-SAD governance or final state.

## Mandatory Source-of-Truth Hierarchy

When two artifacts conflict, apply this precedence order:

1. `docs/constitution.md`
2. Accepted ADRs in `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. Approved scoped Decisions that do not replace an ADR
6. Approved change specification: `specs/<change-id>/spec.md`
7. Approved implementation plan: `specs/<change-id>/plan.md`
8. Change task checklist: `specs/<change-id>/tasks.md`
9. Implementation and tests
10. Evidence, reports, notes, and temporary work artifacts
11. Companion-method artifacts such as GSD `.planning/` files

A lower-precedence artifact must never silently override a higher-precedence artifact.

## Required Startup Procedure

Before changing files, every agent must:

1. Identify the active change ID.
2. Read the applicable project-level documents:
   - `docs/constitution.md`
   - `docs/project-brief.md`
   - `docs/architecture.md`
   - `docs/roadmap.md`
   - relevant accepted ADRs
3. Read the active change artifacts:
   - `state.yaml`
   - `spec.md`
   - `plan.md`, when present
   - `tasks.md`, when present
   - existing `evidence.md`, when present
4. Read `.ggsad/config.yaml` and relevant profile or integration mappings.
5. Identify the current phase, status, allowed scope, required outputs, and prohibited actions.
6. Check for unresolved placeholders, contradictions, missing approvals, and ADR conflicts.
7. Evaluate whether the current phase may begin or continue.

If the active change cannot be identified, the agent must not infer one from nearby files. It must report the ambiguity and enter a controlled wait state.

## Core Execution Rules

Every agent must:

- work from an explicit goal;
- remain inside the approved change scope;
- treat the approved specification as the implementation anchor;
- respect the project document hierarchy;
- preserve accepted ADRs unless a separate ADR-change flow is approved;
- use concrete acceptance examples for behavioral requirements;
- produce evidence for every completion claim;
- prefer the smallest coherent vertical slice;
- minimize duplicate facts and reference authoritative artifacts instead;
- keep the method core independent from external agents, vendors, IDEs, issue trackers, CI systems, and companion frameworks;
- stop safely when a required fact, dependency, decision, or approval is missing.

Every agent must not:

- invent goals, requirements, constraints, decisions, approvals, or evidence;
- interpret silence or missing information as approval;
- silently modify an approved specification, architecture document, ADR, or project policy;
- implement unapproved breaking changes;
- expand scope because a related improvement appears useful;
- mark a phase or change complete without verifiable evidence;
- hide failures, test errors, skipped checks, or unresolved deviations;
- bypass a gate by directly editing workflow state;
- use companion-method output as a replacement for GG-SAD artifacts;
- add infrastructure, services, dependencies, abstractions, hooks, or agents without a clear approved need.

## Gate Evaluation

At every transition point, evaluate gates in this order:

1. **Definition of Fail** — must the flow terminate?
2. **Definition of Wait** — must the flow pause safely?
3. **Definition of Done** — is the current phase complete?
4. **Definition of Ready** — may the next phase begin?

A passing Definition of Done does not override an active Wait or Fail condition.

Agents must not mutate `state.yaml` arbitrarily. State changes must use an approved transition command or follow the explicit transition contract defined by the active implementation stage.

## Wait Behavior

Enter `waiting` when work cannot continue safely but has not failed.

A wait report must state:

- the exact reason;
- the missing information, dependency, decision, or approval;
- the responsible person or source;
- the safe current state;
- the resume condition;
- the phase or action at which work should resume;
- the next intended action.

While waiting, agents must stop all risky, destructive, scope-changing, or approval-dependent work.

## Fail Behavior

Enter `failed` when a defined failure condition is triggered, including:

- violation of the constitution or an accepted ADR;
- critical security or data-integrity risk;
- repository corruption;
- unapproved breaking change;
- work outside approved scope;
- unrecoverable migration or build state;
- exceeded hard retry, cost, or resource limits;
- permanently unsatisfiable acceptance conditions.

On failure, the agent must stop, preserve relevant evidence, perform only approved containment or rollback actions, and report the failure without disguising it as partial success.

## Pair Review

Pair Review separates creation from independent evaluation.

- The **Requestor** creates or changes the governed work product.
- The **Reviewer** reviews, tests, verifies, validates, or evaluates it.
- Requestor and Reviewer must be distinct participants in the same review cycle.
- Human–Human, Human–Agent, Agent–Human, Agent–Agent, and external review-service combinations are allowed.
- A Reviewer must not silently edit the Requestor's governed work product during review.
- Findings must be returned to the Requestor for disposition.
- Open blocking findings block the applicable gate unless an authorized decision owner formally dispositions them.
- Pair Review does not replace required human approval.

An agent must not claim independent review of its own work under another session name unless the project explicitly defines the identities as independently controlled participants.

## File Ownership by Phase

Agents must respect the active phase's write scope.

Typical boundaries:

| Phase | Primary writable artifacts |
|---|---|
| Intake | intake record, initial `state.yaml` metadata |
| Specify | `spec.md`, permitted specification metadata |
| Plan | `plan.md`, optional `tasks.md`, permitted state metadata |
| Build | approved source, tests, implementation documentation |
| Verify | `evidence.md`, review records, verification metadata |
| Release | release artifacts explicitly named by the approved plan |

A Build agent must not silently rewrite an approved specification or ADR. A Verify agent must not silently fix the implementation it is reviewing. A separate correction cycle may reassign that agent as Requestor.

## Engineering Standards

Unless a higher-precedence artifact states otherwise:

- use Python with explicit type annotations;
- manage environments, dependencies, locking, and builds with `uv`;
- use Typer for CLI commands;
- use Pydantic v2 for validated internal models;
- use `ruamel.yaml` for round-trip YAML behavior;
- use JSON Schema for externally consumable structural validation;
- use pytest for tests;
- use Hypothesis for state and invariant testing where valuable;
- use Ruff for formatting and linting;
- use mypy for static type checking;
- keep modules cohesive and dependency direction explicit;
- prefer standard-library solutions when they are adequate;
- avoid speculative abstractions and premature extension systems.

## Test and Evidence Rules

Agents must:

- map every behavioral requirement and acceptance example to tests or explicit evidence;
- test success, failure, negative, and boundary behavior according to risk;
- preserve the working tree after failed validation or rejected transitions;
- provide actionable error messages;
- test stand-alone operation without optional integrations;
- record exact commands used for important verification;
- distinguish executed checks from checks that were skipped or unavailable;
- reference generated reports rather than duplicate large outputs in Markdown.

Before claiming Build-Done or Verify-Done, run the applicable approved checks. The expected baseline is:

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
```

Run additional security, packaging, schema, Markdown, or YAML checks when they are part of the active change or project gate.

## Dependency and Tool Rules

Before adding a dependency or tool, document:

- the concrete requirement it satisfies;
- why the standard library or an existing dependency is insufficient;
- runtime or development-only classification;
- security and maintenance implications;
- removal or replacement strategy where relevant.

Do not add a database, web application, MCP server, multi-agent orchestrator, unrestricted workflow DSL, semantic memory store, issue synchronization, or release automation unless an approved change explicitly includes it.

## Git and Repository Safety

Agents must:

- inspect the working tree before editing;
- avoid destructive Git commands unless explicitly approved;
- never discard unrelated user changes;
- keep commits scoped to the active change;
- avoid mixing generated files, refactors, dependency upgrades, and behavior changes without an approved reason;
- never rewrite published history without explicit approval;
- report unexpected tracked or untracked files before acting on them;
- preserve a reviewable state for Pair Review.

Do not commit secrets, credentials, local machine paths, personal data, or unsanitized sensitive tool output.

## Documentation Rules

Project documentation and code are written in English.

Agents must:

- use normative terms consistently where applicable;
- preserve stable IDs for requirements, examples, criteria, findings, ADRs, and changes;
- avoid copying the same rule into multiple authoritative locations;
- update project documentation only when the active change requires it;
- label derived or temporary summaries as non-authoritative;
- resolve or remove placeholders before claiming completion.

## GSD Companion Rules

When GSD is enabled:

- `.planning/` is subordinate execution state;
- GSD may discuss, plan, decompose, execute, verify, and prepare shipping information within the approved GG-SAD change;
- GSD must not redefine goals, requirements, architecture, gates, approvals, or closure;
- GSD completion does not close a GG-SAD change;
- conflicts must be resolved in favor of higher-precedence GG-SAD artifacts;
- derived GSD summaries should reference their authoritative GG-SAD paths;
- GSD-generated scope expansion must be rejected or returned for a separate GG-SAD change.

## Required Completion Report

At the end of an execution cycle, the agent must report:

1. active change and phase;
2. files changed;
3. requirements or tasks addressed;
4. checks executed and exact results;
5. evidence created or updated;
6. deviations, assumptions, risks, and unresolved findings;
7. current gate assessment in DoF → DoW → DoD → DoR order;
8. whether human approval or Pair Review is required next.

Do not describe work as complete when any required check, evidence item, approval, or blocking review finding remains unresolved.
