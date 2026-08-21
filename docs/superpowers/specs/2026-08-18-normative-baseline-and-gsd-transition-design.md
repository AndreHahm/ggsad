# Normative Baseline Clarification and GSD Transition Design

## Status and authority

- Status: Approved
- Date: 2026-08-18
- Requestor: Codex
- Decision owner: repository owner
- Independent reviewer: Claude Code
- Bootstrap authorization status: Approved
- Bootstrap authorization evidence: The repository owner explicitly authorized this one-time
  transition in the Codex review session on 2026-08-18 without requiring another GG-SAD change,
  because the transition replaces GG-SAD development governance with GSD.
- Design approval status: Approved
- Final approval record: The repository owner explicitly approved reviewed design revision
  `c3b0a30` in the Codex review session on 2026-08-18 after disposition of F-01 through F-07, and
  subsequently approved sequencing the GSD update and onboarding before the normative amendment
  so all substantive implementation work uses the selected development method.

This document designs the transition. It does not itself amend the normative specification,
delete existing governance, install GSD, or change the Python implementation.

## Owner-confirmed governing decisions

The repository owner confirmed these decisions during the clarification sequence. Final design
approval governs how they are implemented; it does not reopen the selected direction.

1. `docs/method/GG-SAD_normative_method_specification.md` is the leading document.
2. The leading document has two explicit responsibilities:
   - define GG-SAD method semantics and conformance;
   - define requirements for a GG-SAD reference implementation, including why required artifacts
     and automation exist.
3. GSD Core is the sole development method for this minimal-automation prototype.
4. GG-SAD is the product being implemented; it does not govern development of this prototype.
5. The current Python implementation and tests are retained as a candidate baseline.
6. Existing GG-SAD development-governance artifacts are subordinate, disposable historical
   material and must not constrain the transition.
7. The German normative specification is removed until the English baseline stabilizes.
8. Normative amendments require explicit owner approval and independent review by Claude Code.

## Goal

Produce a coherent English normative baseline and develop its minimal-automation reference
prototype under one current GSD workflow, while preserving verified implementation value and
eliminating mixed or circular governance.

## Success criteria

- A reader can distinguish GG-SAD method semantics from reference-implementation requirements.
- The normative state model has one canonical phase vocabulary, status vocabulary, and transition
  contract.
- Manual stand-alone GG-SAD operation is possible without a package or plugin.
- The minimal automation contract is explicit enough for independent implementations to produce
  compatible observable behavior.
- Development planning, execution, verification, and shipping use GSD only.
- Root-level GG-SAD artifacts are either product assets, clearly labeled examples, or removed from
  development-governance use.
- The retained Python implementation is audited against the clarified contract instead of being
  trusted because of prior completion claims.
- Required checks pass within a scope that excludes installer-owned third-party tooling.
- Claude Code independently reviews the normative amendment and transition result.

## Normative specification correction scope

### 1. Establish authority and applicability

The specification will state that it is the leading GG-SAD semantic and product baseline. Its
project-document hierarchy governs artifacts inside a GG-SAD-managed project; that hierarchy does
not outrank the normative specification itself.

The specification will separate:

- method semantics and invariants;
- project governance when GG-SAD is selected as a development method;
- reference-implementation requirements;
- optional integrations and non-normative implementation guidance.

It will explicitly permit a GG-SAD implementation to be developed using another method. Such a
development method must not redefine GG-SAD product semantics.

### 2. Define the canonical artifact model

The change-artifact model will include `state.yaml` when persistent machine-readable workflow
state is used. It will distinguish mandatory information from mandatory files:

- goal, specification anchor, gate outcome, evidence, wait/fail behavior, and final status are
  invariant information;
- separate `plan.md`, `tasks.md`, `evidence.md`, and `review.md` files remain conditional;
- inline storage is permitted only when its authoritative location and required fields are clear.

### 3. Replace the ambiguous state narrative with a transition contract

The normative model will define:

- canonical phases;
- canonical statuses;
- whether `closed` is a phase or status;
- legal phase/status combinations;
- actions that move between combinations;
- gate evaluation for every action;
- waiting from draft, ready, active, or done where applicable;
- cancellation, supersession, reopening, and terminal behavior;
- mutation safety and required history evidence.

The contract will use a transition table with current phase/status, action, preconditions, gate
order, resulting phase/status, and rejection behavior.

### 4. Make tailoring deterministic

The specification will define how invariant rules, profiles, project configuration, change class,
local strengthening, and integration mappings combine. It will define who may omit a phase, how
the omission is recorded, and what evidence replaces that phase.

Self-approval under a lean profile will explicitly remain subordinate to non-delegable human
approval rules.

### 5. Define portable approval and Pair Review evidence

The minimum record will identify the participant, role, reviewed artifact revision, action,
timestamp, result, findings, and disposition. Independent review requires a distinct participant
identity and control boundary, not merely a fresh context.

### 6. Define the minimal automation contract

The prototype must provide technology-neutral behavior for:

- initializing a stand-alone GG-SAD project;
- creating a goal-bound change;
- validating governing configuration, artifacts, references, and state;
- evaluating and executing at least one controlled state transition;
- rejecting invalid operations without partial mutation;
- emitting actionable human-readable results and a stable machine-readable result;
- recording transition history and relevant evidence.

The normative contract will specify observable behavior and compatibility requirements, not
Python module structure or a vendor-specific agent interface.

### 7. Repair document quality

- Renumber Sections 6 through 13 and repair incoming references.
- Remove the German normative specification.
- Remove tool-local citations and unresolved references from any retained normative source.
- Clearly label examples and templates so intentional placeholders are not mistaken for unresolved
  normative content.

## Development-method transition

### GSD baseline

Use official GSD Core 1.10.0, the stable release selected during this design review. The repository
already contains an installer-managed GSD Core 1.9.1 installation under `.claude/`, but it has not
been onboarded because no `.planning/` directory exists. Use the official installer's supported
update path to replace 1.9.1 with pinned version 1.10.0, then verify the installed version and
generated manifest before onboarding the existing repository. Do not manually edit or delete
installer-owned GSD files unless the official update or uninstall procedure requires it.

Do not combine a GSD workflow with GG-SAD change state, gates, approvals, or closure for prototype
development.

GSD owns development discussion, requirements decomposition, roadmap, plans, execution state,
verification workflow, and shipping artifacts. The English GG-SAD specification remains the
leading product requirement source.

### Existing repository treatment

Retain initially:

- `src/ggsad/`;
- `tests/`;
- packaging and Python quality configuration;
- the English normative specification;
- product schemas, templates, and examples that are required by the clarified contract.

Retire, archive outside the active workflow, or rewrite:

- the German normative specification;
- the root development constitution and agent rules that impose GG-SAD workflow;
- `CLAUDE_CODE_PROJECT_START.md`, which is retired because it hardcodes CHG-001 and the former
  GG-SAD/GSD combination model;
- `CLAUDE.md`, which is replaced with concise instructions for GSD as the sole development method
  and the English normative specification as the leading product authority;
- `AGENTS.md`, which is rewritten consistently so general agents do not continue enforcing GG-SAD
  development governance;
- `specs/CHG-*` development state and evidence;
- roadmap, ADRs, architecture, and implementation plans whose conclusions assumed the prior
  GG-SAD/GSD combination model;
- the existing GSD Core 1.9.1 installation, updated through the official installer rather than
  manually rewritten, before clean onboarding with pinned version 1.10.0.

Root `.ggsad` assets require classification before removal. Product resources and fixtures must be
relocated or clearly labeled; development-governance state must be retired.

### Retain-versus-rewrite rule

Existing code is retained only when it conforms to the clarified product contract and passes
verification. Prior GG-SAD completion evidence is historical context, not proof of conformance.
Non-conforming behavior is corrected or removed through GSD plans. A full rewrite requires a
specific technical finding showing that repair is more costly or risky.

## Quality and verification

The implementation baseline is:

```text
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
uv build
```

Installer-owned GSD runtime files must not be treated as Python product source. Quality-tool scope
will explicitly include product code, tests, and owned scripts while excluding third-party
generated tooling.

Verification will include:

- requirement-to-test traceability for the minimal automation contract;
- success, negative, boundary, and no-partial-mutation behavior;
- stand-alone operation without GSD at product runtime;
- an audit of retained code against the clarified normative specification;
- a clean GSD development-state check;
- independent Claude Code review of the normative amendment and transition diff.

## Design review dispositions

Claude Code reviewed commit `800a004e7c8d7a565c34deab1b3aa61f9b1b6492`. The repository owner and
Requestor dispositioned its findings as follows on 2026-08-18:

| Finding | Disposition | Resulting action |
|---|---|---|
| F-01 | Accepted | Removed the unrelated owner-authored blank line from the normative file. |
| F-02 | Accepted as blocking | Named `CLAUDE_CODE_PROJECT_START.md`, `CLAUDE.md`, and `AGENTS.md` explicitly in the retirement or rewrite scope. |
| F-03 | Partially accepted | Confirmed the bootstrap exception was approved; separated its evidence from pending final design approval. |
| F-04 | Clarity concern accepted; proposed wording rejected | Labeled the direction as owner-confirmed while leaving implementation details subject to design approval. |
| F-05 | Accepted | Defined installer-managed update from GSD Core 1.9.1 to pinned 1.10.0 before repository onboarding. |
| F-06 | Accepted as informational | Carry the CHG-001 state mismatch into amendment rationale and planning evidence; no design correction required. |
| F-07 | Accepted | Added `uv sync --locked` to the verification baseline. |

## Transition sequence

1. Approve this design.
2. Create a bootstrap implementation plan limited to installing the selected GSD version,
   neutralizing conflicting development instructions, and onboarding the existing repository.
3. Update the installer-managed GSD Core 1.9.1 files to pinned version 1.10.0 and verify the
   installed version and manifest.
4. Replace or suspend conflicting `AGENTS.md`, `CLAUDE.md`, and
   `CLAUDE_CODE_PROJECT_START.md` instructions sufficiently for GSD-only development.
5. Onboard the existing repository with GSD to create `.planning/`.
6. Use GSD to plan and prepare the normative amendment without changing implementation behavior.
7. Obtain owner approval for the exact normative diff.
8. Obtain independent Claude Code review and resolve blocking findings.
9. Use GSD to retire or relocate remaining conflicting development-governance artifacts.
10. Configure quality tools to separate owned source from installer-owned tooling.
11. Audit the retained implementation against the clarified contract.
12. Implement only identified conformance gaps through GSD.
13. Run the complete verification baseline and record GSD verification results.

## Safety and rollback

- Preserve repository history; do not destructively erase prior commits.
- Make the normative amendment reviewable separately from governance cleanup and behavior changes.
- Do not delete an artifact until its retained product content has been classified.
- Pin the selected GSD version so an upstream update cannot silently change the active workflow.
- If onboarding fails, revert only the onboarding change and retain the reviewed normative baseline
  and Python implementation.

## Explicit non-goals

- Building profile resolution, a full gate engine, memory, MCP, a web UI, CI integration, or
  multi-agent orchestration as part of this transition.
- Preserving prior roadmap ordering or change closure claims.
- Using GG-SAD and GSD simultaneously as development methods.
- Rewriting passing implementation code solely to obtain a clean history.
