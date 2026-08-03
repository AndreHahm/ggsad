# Claude Code Instructions

## Scope

This file adds Claude Code-specific rules to the repository-wide `AGENTS.md` instructions.

Claude Code must read and follow `AGENTS.md` first. If this file conflicts with `AGENTS.md` or a higher-precedence project artifact, the stricter or higher-precedence rule applies.

## Claude Code Role

Claude Code is the primary implementation runtime for the initial GG-SAD reference implementation.

Unless an active change states otherwise, Claude Code acts as the **Requestor** for implementation work. Claude Code is not automatically the independent Reviewer or human Approver.

Claude Code must not present its own second pass, subagent, or separate context window as independent Pair Review unless the project explicitly assigns a distinct independently controlled reviewer identity.

## Session Startup

At the start of every implementation session:

1. Read `AGENTS.md`.
2. Read `CLAUDE_CODE_PROJECT_START.md` when present.
3. Determine the active GG-SAD change from the user instruction and repository state.
4. Read the project and change artifacts required by `AGENTS.md`.
5. Inspect:

```bash
git status --short --branch
git diff --stat
git diff --cached --stat
```

6. Identify unexpected changes, generated files, unresolved conflicts, or files outside the active scope.
7. Report the current phase, status, governing scope, and initial gate assessment before implementation.

Do not begin production changes merely because a GSD phase or Claude task is available. Ready-to-Build must be satisfied.

## Planning Behavior

Claude Code must create or modify an implementation plan only when authorized by the active GG-SAD phase.

When using plan mode or GSD planning:

- anchor every step to an approved requirement, acceptance example, risk, or required artifact;
- separate approved scope from optional ideas;
- do not reopen accepted ADRs or project decisions without a detected conflict;
- reject tasks that belong to a later change;
- identify exact files or components where reasonably known;
- include verification and evidence work in the plan;
- include rollback or preservation behavior for risky changes;
- keep GSD `.planning/` artifacts subordinate to `specs/<change-id>/plan.md`.

Claude Code must present material scope, architecture, dependency, or breaking-change decisions to the human decision owner rather than silently selecting them.

## Editing Behavior

Claude Code must:

- make focused, reviewable edits;
- inspect relevant code before modifying it;
- preserve existing style and architecture unless the approved plan changes them;
- avoid broad formatting or unrelated cleanup;
- avoid replacing entire files when a small targeted edit is safer;
- verify generated files before treating them as correct;
- never modify higher-precedence artifacts merely to make current code pass validation;
- stop when implementation reveals a specification or ADR conflict.

When a specification change is required during Build:

1. stop implementation of the affected behavior;
2. document the conflict or new fact;
3. return the issue to the Requestor or human decision owner;
4. update and reapprove the specification through the proper flow;
5. resume only after the required gate is satisfied.

## Command Execution

Before running a command, Claude Code must understand its expected scope and effect.

Claude Code must:

- prefer non-destructive inspection before mutation;
- use project-local tools through `uv run` where applicable;
- avoid global package installation when a project-local alternative exists;
- avoid commands that can remove, reset, clean, overwrite, publish, deploy, or rewrite history without explicit approval;
- never run `git reset --hard`, `git clean -fd`, force-push, destructive migration, release, or publication commands unless the active change explicitly authorizes them;
- stop repeated failing command loops and report the underlying blocker;
- preserve exact command output needed as evidence without flooding governed documents with raw logs.

For multi-command validation, prefer explicit sequential commands. Do not hide failures behind shell constructs that continue silently.

## GSD Use in Claude Code

GSD is the approved initial execution companion, not the governing method.

After local installation and Claude Code restart, initialize it with:

```text
/gsd-new-project
```

Use the approved project description from `CLAUDE_CODE_PROJECT_START.md`.

For the active implementation phase, the expected GSD cycle is:

```text
/gsd-discuss-phase
/gsd-plan-phase
/gsd-execute-phase
/gsd-verify-work
```

Use `/gsd-ship` only after the applicable GG-SAD Verify-Done and release or closure conditions are satisfied.

Claude Code must review all GSD-generated artifacts for:

- scope expansion;
- duplicated sources of truth;
- contradictions with GG-SAD artifacts;
- premature components;
- unsupported dependencies;
- invented requirements or decisions.

When a conflict originates in GSD interpretation, correct the GSD artifact. Do not weaken or rewrite GG-SAD governance to match it.

## Context Management

Claude Code should keep the active context focused on:

- the active change;
- current phase and gate;
- relevant project rules and ADRs;
- affected implementation files;
- acceptance examples and required evidence.

Do not load or summarize the entire repository when a narrower context is sufficient. Do not omit a governing artifact merely to save context.

When handing work to a fresh context or GSD subagent, include:

- active change ID;
- exact goal and scope;
- current phase and state;
- authoritative artifact paths;
- relevant requirements and acceptance examples;
- allowed and prohibited files;
- required checks;
- current risks, decisions, and blockers;
- expected output contract.

A subagent may not approve, close, or transition the GG-SAD change unless explicitly authorized through the engine and project policy.

## Claude Code Subagents

Use subagents only when they provide a real context, permission, or specialization boundary.

Permitted examples include:

- read-only repository analysis;
- isolated test investigation;
- independent research within approved scope;
- focused static analysis;
- preparation of review candidates.

Do not create a subagent merely to simulate process compliance. A subagent under the same Claude Code control is not automatically an independent Pair Reviewer.

Every subagent instruction must state:

- role;
- scope;
- readable and writable files;
- prohibited actions;
- authoritative sources;
- expected evidence or output;
- stop conditions.

Claude Code remains responsible for validating subagent output before using it.

## Testing and Verification

Claude Code must run the checks required by the active specification, plan, and project gates.

Baseline commands:

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
```

When implementing packaging or CLI behavior, also run applicable commands such as:

```bash
uv build
uv run ggsad --help
```

When schemas, Markdown, YAML, dependencies, or security-relevant code change, run the applicable approved validators and scanners.

Claude Code must not claim a command passed unless it was executed successfully in the current relevant repository state. State clearly when a check was not run and why.

## Evidence Handling

Claude Code must map implementation outcomes to `specs/<change-id>/evidence.md` only when the active phase permits it.

Evidence should include:

- requirement or acceptance-example ID;
- test, command, report, commit, or file reference;
- result;
- relevant environment or version information;
- deviations and limitations;
- Pair Review references when required.

Reference durable reports instead of pasting excessive raw output. Do not fabricate evidence from expected behavior.

## Review Preparation

Before handing work to an independent Reviewer, Claude Code must:

1. produce a stable reviewable worktree or commit;
2. identify the Requestor as Claude Code with the configured participant identity;
3. identify the assigned distinct Reviewer;
4. state the review scope and criteria;
5. provide relevant specification, plan, ADR, code, test, and evidence references;
6. disclose known deviations, skipped checks, risks, and unresolved questions;
7. avoid making further changes to the review target until findings are returned, unless the review cycle is explicitly restarted.

Claude Code must not silently resolve, reject, or downgrade blocking findings. It must record the Requestor disposition and request re-verification where required.

## Human Approval Boundaries

Claude Code must request explicit human approval before:

- accepting or superseding an ADR;
- changing the constitution;
- approving a breaking change;
- changing project scope or core non-goals;
- releasing or publishing artifacts when human approval is configured;
- weakening a compliance profile, gate, test requirement, evidence requirement, or security control;
- performing destructive repository or data operations;
- treating a material deviation as accepted.

Claude Code may prepare the decision package, options, trade-offs, and recommendation. It must not record human approval until the human actually provides it.

## Initial Change Constraint

For `CHG-001-reference-repository-bootstrap`, Claude Code must remain within the approved bootstrap scope.

Expected capabilities:

- Python package and CLI skeleton;
- GG-SAD configuration, profiles, schemas, mappings, and templates;
- project-level documents and example change artifacts;
- state model and schema;
- `ggsad init`;
- `ggsad new`;
- `ggsad validate`;
- controlled `draft -> ready` transition;
- unit and acceptance tests;
- complete Class M example;
- documented GSD mapping.

Explicitly excluded:

- complete gate engine;
- automatic evidence evaluation;
- CI integration;
- project memory implementation;
- MCP server;
- web UI;
- issue synchronization;
- multi-agent orchestration;
- release automation;
- broad companion-framework adapters.

Discovering a useful excluded capability is not permission to implement it. Record it in the roadmap or as a proposed future change when appropriate.

## Required Claude Code Progress Report

During substantial work, provide concise progress updates after meaningful milestones or newly discovered blockers.

At the end of the session, report:

```text
Active change:
Current phase and status:
Goal:
Completed work:
Files changed:
Requirements/examples addressed:
Commands and checks executed:
Evidence updated:
Pair Review status:
Deviations and risks:
DoF assessment:
DoW assessment:
Current DoD assessment:
Next DoR assessment:
Required human decision or next action:
```

Do not conclude with a generic success statement. The final status must follow the actual GG-SAD gate results.
