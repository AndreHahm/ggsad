# CHG-001 — Reference Repository Bootstrap

## Metadata

- Change ID: CHG-001
- Slug: reference-repository-bootstrap
- Title: Reference Repository Bootstrap
- Class: M
- Phase: specify
- Status: ready
- Flow Profile: standard
- Compliance Profile: standard
- Requestor: human:project-owner
- Decision Owner: human:project-owner
- Intended Implementation Requestor: agent:claude-code
- Reviewer: agent:codex
- Approver: human:project-owner
- Created: 2026-08-02
- Last Updated: 2026-08-02
- Related Roadmap Item: R0 — Repository Bootstrap
- Parent Initiative: None

## Goal

### Desired Outcome

Create the first coherent GG-SAD reference-implementation repository baseline so that a user can:

1. initialize a GG-SAD project;
2. create a Class M change;
3. validate the project's core configuration and governed artifacts;
4. perform one controlled state transition from `draft` to `ready`;
5. receive clear, actionable errors when validation or transition conditions are not satisfied.

The result must demonstrate the smallest useful vertical slice of GG-SAD automation while
preserving stand-alone operation and the authority boundaries between GG-SAD and GSD.

### Problem Being Solved

The GG-SAD method baseline, project documents, templates, schemas, and implementation direction
exist, but the repository does not yet provide an executable reference workflow.

Without a coherent bootstrap:

- users must assemble the repository structure manually;
- configuration and state files cannot be validated consistently;
- change creation is not standardized;
- state transitions can be edited or interpreted inconsistently;
- companion tools may duplicate or override authoritative GG-SAD artifacts;
- completion claims cannot be tied to a tested initial workflow.

### Success Signals

- A clean repository can be initialized into the approved GG-SAD structure.
- A valid Class M change can be created with the required artifacts.
- Invalid configuration, mappings, state, and required artifact structures are rejected.
- A valid `draft → ready` transition succeeds through an explicit transition action.
- Invalid transitions fail without mutating governed files.
- Validation and transition failures identify the affected file and reason.
- The workflow operates without an active companion integration.
- A GSD mapping contract can be validated when GSD is enabled.
- Unit and acceptance tests demonstrate the required behavior.
- The repository passes the approved formatting, linting, typing, test, and build checks.

### Non-Goals

CHG-001 does not include:

- a complete DoR, DoD, DoW, and DoF gate engine;
- automatic evidence evaluation;
- CI integration;
- project-memory implementation;
- MCP server or MCP tools;
- web UI or dashboard;
- issue-tracker synchronization;
- autonomous multi-agent orchestration;
- automatic subagent delegation;
- release automation;
- automatic merge or publication;
- broad companion mappings beyond the documented GSD contract;
- a database-backed state store;
- a semantic index or vector store;
- stable 1.0 compatibility guarantees.

## Context

GG-SAD is the governing method for the repository. It owns goals, specifications, document
precedence, workflow state, gate semantics, evidence requirements, Pair Review policy, approvals,
and closure.

GSD Core is the initial subordinate execution and context-engineering companion. Files under
`.planning/` are derived execution aids and are not authoritative for GG-SAD scope, architecture,
state, approvals, or closure.

The initial repository uses:

- Python 3.12 or newer;
- `uv` for environments, dependency locking, and builds;
- Typer for the CLI;
- Pydantic v2 for internal models;
- `ruamel.yaml` for safe YAML loading and round-trip writing;
- JSON Schema Draft 2020-12 for portable structural validation;
- pytest and Hypothesis for tests;
- Ruff for formatting and linting;
- `ty` (Astral) for static typing, in strict mode.

The initial architectural decisions are documented in ADR-0001 through ADR-0008. They are
currently proposed and require human disposition before Ready-to-Build can pass unless the
decision owner explicitly records them as non-blocking drafts for this change.

## Scope

### Included

- Python package skeleton under `src/ggsad/`.
- CLI entry point named `ggsad`.
- Project configuration model and validation.
- Integration mapping model and validation.
- Change-state model and validation.
- Approved JSON Schemas:
  - `.ggsad/schemas/config.schema.json`;
  - `.ggsad/schemas/mappings.schema.json`;
  - `.ggsad/schemas/state.schema.json`.
- Repository templates under `.ggsad/templates/`.
- Default compliance-profile assets required for initialization.
- GSD companion mapping under `.ggsad/mappings/gsd.yaml`.
- `ggsad init`.
- `ggsad new`.
- `ggsad validate`.
- `ggsad transition` with the initial controlled `draft → ready` path.
- Human-readable and machine-actionable error output.
- Atomic state update behavior.
- Transition history append behavior.
- Stand-alone operation with no active integration.
- One complete Class M example.
- Unit, integration, acceptance, and selected property-based tests.
- Packaging and CLI help verification.
- Evidence capture for CHG-001.
- Required Pair Review of the completed implementation.

### Excluded

- Full profile inheritance and effective-workflow resolution beyond what is necessary to validate
  the configured standard profile.
- Complete criterion parsing and automatic gate execution.
- General-purpose workflow DSL.
- Arbitrary custom state transitions.
- Network services.
- Hosted services.
- Authentication or authorization systems.
- Persistent database.
- Full release workflow.
- Public package publication.
- Automatic GSD installation or modification.
- Mutation of GSD `.planning/` artifacts by the GG-SAD core.

## Stakeholders and Participants

| Role | Participant | Responsibility |
|---|---|---|
| Decision Owner | human:project-owner | Approves scope, ADR disposition, specification, and plan |
| Specification Requestor | human:project-owner | Defines the governed change |
| Implementation Requestor | agent:claude-code | Implements the approved change |
| Reviewer | agent:codex | Independently reviews implementation, tests, schemas, and evidence |
| Approver | human:project-owner | Provides required human approvals |
| Companion | tool:gsd-core | Provides subordinate execution and context support |

## Requirements

### R-001 — Initialize a GG-SAD Project

The CLI MUST provide an `init` command that creates the approved initial GG-SAD repository assets
in a target directory.

The command MUST:

- create only approved directories and files;
- use the repository templates and schemas;
- avoid overwriting existing files by default;
- produce a clear result summary;
- leave the target in a valid or safely rejected state.

- Priority: Must
- Verification Method: acceptance tests and filesystem inspection

### R-002 — Handle Repeated Initialization Safely

When initialization targets an already initialized or partially populated project, the CLI MUST
either:

- complete an explicitly safe idempotent operation; or
- reject the operation without overwriting governed or unrelated files.

The selected behavior MUST be consistent and tested.

- Priority: Must
- Verification Method: acceptance tests and unchanged-file checks

### R-003 — Create a Class M Change

The CLI MUST provide a `new` command that creates a Class M change under
`specs/<change-id>-<slug>/`.

The created change MUST contain:

- `state.yaml`;
- `spec.md`;
- `plan.md`;
- `tasks.md`;
- `evidence.md`.

The generated files MUST use the approved templates and include the change ID, slug, title, class,
initial phase, and initial status.

- Priority: Must
- Verification Method: acceptance tests and schema validation

### R-004 — Validate Change Identifiers

The CLI MUST reject malformed change IDs and unsafe slugs.

At minimum:

- change IDs MUST match `CHG-<three-or-more-digits>`;
- slugs MUST use lowercase alphanumeric segments separated by single hyphens;
- generated paths MUST remain inside the intended repository.

- Priority: Must
- Verification Method: parameterized and property-based tests

### R-005 — Validate Project Configuration

The validator MUST parse and validate `.ggsad/config.yaml` against
`.ggsad/schemas/config.schema.json`.

It MUST reject:

- invalid YAML;
- missing required fields;
- unsupported operating modes;
- invalid compliance-profile identifiers;
- invalid integration declarations;
- stand-alone configuration with active integrations;
- combination configuration without at least one integration.

- Priority: Must
- Verification Method: unit and acceptance tests

### R-006 — Validate Integration Mappings

The validator MUST parse and validate mapping files referenced by project configuration against
`.ggsad/schemas/mappings.schema.json`.

It MUST verify that:

- the mapping file exists;
- required ownership and permission fields are present;
- uninstall preserves GG-SAD artifacts;
- invalid paths and unsupported values are rejected;
- GSD cannot approve, directly transition, or close GG-SAD work.

- Priority: Must
- Verification Method: unit and acceptance tests

### R-007 — Validate Change State

The validator MUST parse and validate each governed `state.yaml` against
`.ggsad/schemas/state.schema.json`.

It MUST reject:

- invalid YAML;
- schema violations;
- invalid phase or status values;
- malformed change metadata;
- missing mandatory artifacts;
- incomplete wait metadata when status is `waiting`;
- incomplete failure metadata when status is `failed`.

- Priority: Must
- Verification Method: unit, acceptance, and property-based tests

### R-008 — Validate Required Change Artifacts

For a Class M change, validation MUST confirm the existence of the required state, specification,
plan, and evidence artifacts defined by the active project contract.

The validator MUST identify each missing artifact explicitly.

`tasks.md` is included in CHG-001's generated Class M baseline and MUST be validated for this
initial implementation.

- Priority: Must
- Verification Method: acceptance tests

### R-009 — Detect Unresolved Template Placeholders

Validation MUST reject governed artifacts containing unresolved template placeholders that would
make the artifact incomplete or ambiguous.

The initial implementation MUST detect at least the approved placeholder forms used by the
repository templates.

- Priority: Must
- Verification Method: unit and acceptance tests

### R-010 — Support an Explicit Draft-to-Ready Transition

The CLI MUST provide an explicit transition action that can move a valid change from:

```text
phase: specify
status: draft
```

to:

```text
phase: specify
status: ready
```

The action MUST NOT be implemented as an unrestricted status editor.

- Priority: Must
- Verification Method: acceptance tests

### R-011 — Enforce Transition Preconditions

The `draft → ready` transition MUST succeed only when:

- the project configuration is valid;
- referenced mappings are valid;
- the change state is valid;
- required Class M artifacts exist;
- the specification has no unresolved placeholders;
- the plan exists and has no unresolved placeholders;
- no active wait or failure condition is recorded;
- the current state is exactly the supported source state.

The transition does not constitute specification approval. Human approval remains an external
governed prerequisite when required by project policy.

- Priority: Must
- Verification Method: acceptance tests

### R-012 — Preserve Files on Rejected Operations

A failed validation, initialization, change creation, or transition MUST NOT leave partial or
unexpected mutations to governed files.

For transitions, the original `state.yaml` content MUST remain unchanged when the transition is
rejected.

- Priority: Must
- Verification Method: before-and-after content comparison

### R-013 — Update State Atomically

A successful transition MUST write `state.yaml` atomically or through an equivalent mechanism that
does not expose a partially written governed state.

- Priority: Must
- Verification Method: unit tests of the writer and acceptance tests

### R-014 — Append Transition History

A successful transition MUST append a history event containing at least:

- timestamp;
- actor;
- action;
- previous phase and status;
- new phase and status;
- reason or transition identifier.

- Priority: Must
- Verification Method: acceptance tests and schema validation

### R-015 — Produce Actionable Errors

CLI failures MUST:

- use a non-zero exit code;
- identify the failing command or validation area;
- identify the affected file where applicable;
- state the reason;
- avoid stack traces in normal user-facing validation failures;
- avoid exposing secrets or sensitive content.

- Priority: Must
- Verification Method: CLI acceptance tests

### R-016 — Preserve Stand-Alone Operation

The core initialization, change creation, validation, and transition workflow MUST operate when no
companion integration is enabled.

The core Python modules MUST NOT require GSD, Claude Code, GitHub, an IDE, CI, or an issue tracker.

- Priority: Must
- Verification Method: acceptance tests with stand-alone configuration and import tests

### R-017 — Keep GSD Subordinate

When the GSD mapping is enabled:

- `.planning/` MUST remain non-authoritative;
- GSD MUST NOT be granted direct state-transition, approval, or closure authority;
- validation MUST reject a mapping that violates those constraints;
- removing the GSD mapping MUST not remove GG-SAD artifacts.

- Priority: Must
- Verification Method: mapping validation tests

### R-018 — Provide a Complete Class M Example

The repository MUST include one complete, valid Class M example that passes the initial validator
and demonstrates the intended artifact relationship.

The example MUST NOT be treated as active project state.

- Priority: Must
- Verification Method: acceptance test

### R-019 — Provide Baseline Quality and Packaging

The repository MUST support the approved baseline commands:

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
uv build
uv run ggsad --help
```

- Priority: Must
- Verification Method: command execution and recorded evidence

### R-020 — Remain Within the Approved Bootstrap Scope

The implementation MUST NOT add the deferred capabilities listed in this specification.

Useful discoveries outside scope MUST be recorded as roadmap candidates or future change
proposals, not implemented opportunistically.

- Priority: Must
- Verification Method: implementation and Pair Review inspection

## Acceptance Examples

### E-001 — Initialize a Clean Repository

- Covers: R-001

Given an empty writable target directory
When the user runs `ggsad init <target>`
Then the approved GG-SAD directories and baseline files are created
And the command exits successfully
And the resulting project passes the initial project validation

### E-002 — Reject Unsafe Reinitialization

- Covers: R-002, R-012

Given a target directory containing an existing modified `docs/constitution.md`
When the user runs `ggsad init <target>` without an explicit overwrite capability
Then the command fails with an actionable conflict message
And the existing file remains byte-for-byte unchanged
And no unrelated file is removed

### E-003 — Create a Valid Class M Change

- Covers: R-003, R-004

Given a valid initialized project
When the user runs a command equivalent to
`ggsad new --class M CHG-002 example-change`
Then `specs/CHG-002-example-change/` is created
And it contains `state.yaml`, `spec.md`, `plan.md`, `tasks.md`, and `evidence.md`
And `state.yaml` identifies Class M, phase `specify`, and status `draft`
And all generated paths remain inside the repository

### E-004 — Reject an Invalid Change Identifier

- Covers: R-004, R-012, R-015

Given a valid initialized project
When the user attempts to create change ID `change/../../002`
Then the command fails with a non-zero exit code
And the message identifies the invalid identifier
And no files are created outside or inside the intended change directory

### E-005 — Reject Invalid Project YAML

- Covers: R-005, R-015

Given `.ggsad/config.yaml` contains invalid YAML
When the user runs `ggsad validate`
Then validation fails
And the output identifies `.ggsad/config.yaml`
And the output reports a YAML parsing error without a normal-operation stack trace

### E-006 — Reject an Unknown Compliance Profile

- Covers: R-005

Given `.ggsad/config.yaml` selects an unknown profile with no corresponding approved custom
profile
When the user runs `ggsad validate`
Then validation fails
And the output identifies the unsupported profile

### E-007 — Reject an Invalid GSD Mapping

- Covers: R-006, R-017

Given `.ggsad/mappings/gsd.yaml` sets `may_approve: true`
When the user runs `ggsad validate`
Then validation fails
And the output explains that the companion may not approve GG-SAD work

### E-008 — Reject Missing Class M Artifacts

- Covers: R-007, R-008

Given a Class M change whose `plan.md` is missing
When the user runs `ggsad validate`
Then validation fails
And the output identifies the change and missing `plan.md`

### E-009 — Reject Unresolved Placeholders

- Covers: R-009, R-011

Given a Class M `spec.md` still contains an unresolved approved template placeholder
When the user requests the `draft → ready` transition
Then the transition is rejected
And `state.yaml` remains unchanged
And the output identifies the unresolved placeholder and file

### E-010 — Perform the Valid Draft-to-Ready Transition

- Covers: R-010, R-011, R-013, R-014

Given a valid project and Class M change in phase `specify`, status `draft`
And all transition preconditions are satisfied
When the user runs a command equivalent to `ggsad transition CHG-002 ready`
Then `state.yaml` is updated atomically
And the status becomes `ready`
And the phase remains `specify`
And a transition history event is appended
And the command exits successfully

### E-011 — Reject an Unsupported Transition

- Covers: R-010, R-011, R-012

Given a change in phase `specify`, status `ready`
When the user requests another transition to `ready`
Then the transition is rejected
And the original state file remains unchanged
And the output states that the source state is unsupported

### E-012 — Operate Without GSD

- Covers: R-016

Given an initialized stand-alone project with no active integrations
When the user creates, validates, and transitions a valid Class M change
Then all supported operations succeed
And no GSD, Claude Code, `.planning/`, repository-host, IDE, or network dependency is required

### E-013 — Validate the Complete Example

- Covers: R-018

Given the repository's Class M example
When the validator evaluates it
Then the example passes all initial structural and schema checks
And it is clearly marked as an example rather than active project state

### E-014 — Pass the Baseline Quality Commands

- Covers: R-019

Given the completed CHG-001 implementation
When the approved quality and packaging commands are executed
Then every required command exits successfully
And the results are referenced in `evidence.md`

### E-015 — Exclude Deferred Capabilities

- Covers: R-020

Given the completed CHG-001 review target
When the independent Reviewer inspects dependencies, modules, commands, and generated artifacts
Then no memory backend, MCP server, web UI, issue synchronization, release automation, or
multi-agent orchestrator is present

## Constraints

### Project and Constitutional Constraints

- GG-SAD remains the governing method.
- Evidence is required for completion claims.
- Gate evaluation order remains DoF → DoW → DoD → DoR.
- No agent may self-issue human approval.
- No lower-precedence artifact may override an accepted ADR or governing project document.
- Secrets and sensitive data must not be committed or emitted in normal error output.
- Destructive repository operations require explicit authorization.

### Architecture and ADR Constraints

CHG-001 is governed by the disposition of:

- ADR-0001 — Use Python for the Reference Engine;
- ADR-0002 — Use Markdown for Governing Documents;
- ADR-0003 — Use YAML for Configuration and State;
- ADR-0004 — Separate the Method Core from Integrations;
- ADR-0005 — Use Explicit State Transition Actions;
- ADR-0006 — Use GSD as the Initial Execution Companion;
- ADR-0007 — Use One Agent with Phase-Specific Workflows Initially;
- ADR-0008 — Defer Memory, MCP, Web UI, and Multi-Agent Orchestration.

Disposition (2026-08-02, human:project-owner): ADR-0001 through ADR-0008 are recorded as
non-blocking drafts for CHG-001. Their individual `Status: Proposed` is unchanged by this
disposition and they are not thereby formally accepted as durable architecture; this disposition
only removes them as a Ready-to-Build blocker for this change. Implementation MUST still stop if
a conflict with the content of any of these ADRs is discovered.

Implementation MUST stop if an accepted ADR conflicts with this specification.

### Technology Constraints

- Python 3.12 or newer.
- `uv` for dependency, environment, lock, and build management.
- Typer for the CLI.
- Pydantic v2 for internal validated models.
- `ruamel.yaml` for safe YAML processing and round-trip writes.
- JSON Schema Draft 2020-12 for external schemas.
- pytest for tests.
- Hypothesis where property-based testing adds value.
- Ruff for formatting and linting.
- `ty` in strict mode (`pyproject.toml` `[tool.ty.rules] all = "error"`).
- No unapproved runtime dependency.

### Security, Privacy, and Compliance Constraints

- Use safe YAML loading.
- Prevent path traversal.
- Do not follow unsafe generated paths outside the repository.
- Do not expose secrets in errors or evidence.
- Do not execute external commands as part of structural validation.
- Use least-privilege filesystem behavior.
- No network access is required for supported core operations.

### Compatibility and Migration Constraints

- The project is pre-alpha; interfaces may evolve through governed changes.
- Schema versions must be explicit.
- Invalid or unsupported schema versions must fail clearly.
- No migration framework is required in CHG-001.
- Existing user files must not be overwritten silently.

### Resource and Budget Constraints

- Core commands should be suitable for local developer use.
- Validation should complete without network access.
- The implementation should avoid unnecessary full-repository scans.
- Repeated failures must not cause unbounded retry loops.

## Affected Areas

- Components:
  - CLI;
  - configuration loader;
  - YAML loader/writer;
  - schema validator;
  - document validator;
  - state model;
  - transition engine;
  - template service;
  - mapping validator.
- Interfaces:
  - `ggsad init`;
  - `ggsad new`;
  - `ggsad validate`;
  - `ggsad transition`;
  - `ggsad --help`.
- Data:
  - `.ggsad/config.yaml`;
  - `.ggsad/mappings/*.yaml`;
  - `specs/*/state.yaml`.
- Configuration:
  - compliance profile;
  - operating mode;
  - integration mapping references.
- Documentation:
  - templates;
  - example change;
  - README and usage guidance where required.
- Operations:
  - local CLI execution only.
- External Integrations:
  - optional GSD mapping validation only.

## Risks

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| Bootstrap scope expands into a workflow platform | high | medium | Enforce R-020 and ADR-0008 | Requestor |
| CLI contract is over-designed before pilots | medium | medium | Implement only required commands and paths | Requestor |
| State corruption on failed transition | high | low | Atomic writer and unchanged-file tests | Requestor |
| YAML ambiguity or unsafe parsing | high | low | Safe loader, schema validation, quoted values | Requestor |
| GSD becomes a second source of truth | high | medium | Validate mapping and precedence | Decision Owner |
| Placeholder detection produces false positives | medium | medium | Restrict detection to approved placeholder forms | Requestor |
| Proposed ADRs block implementation | high | high | Human disposition before Ready-to-Build | Decision Owner |
| Reviewer independence is not established | high | medium | Assign distinct Reviewer before Verify | Decision Owner |
| Schema and internal model drift | medium | medium | Contract tests and shared fixtures | Requestor |

## Dependencies and Prerequisites

| Dependency | Type | Owner | Required Condition | Status |
|---|---|---|---|---|
| Project constitution | approval | human:project-owner | Active or explicitly approved baseline | pending verification |
| ADR-0001 through ADR-0008 | decision | human:project-owner | Accepted or explicitly non-blocking for CHG-001 | recorded — non-blocking drafts for CHG-001 (2026-08-02) |
| Project brief | artifact | human:project-owner | Active and consistent | available |
| Architecture | artifact | human:project-owner | Initial boundaries defined | available |
| `.ggsad/config.yaml` | artifact | human:project-owner | Valid against schema | validated 2026-08-02 (Draft 2020-12, jsonschema) |
| GSD mapping | artifact | human:project-owner | Valid against schema | validated 2026-08-02 against `.ggsad/schemas/mappings.schema.json` |
| `state.yaml` | artifact | human:project-owner | Valid and in specify/draft | validated 2026-08-02; phase/status remains specify/draft |
| Specification approval | approval | human:project-owner | Approved before build | approved 2026-08-02 |
| Plan approval | approval | human:project-owner | Approved if required | approved 2026-08-02 |
| Pair Reviewer | participant | human:project-owner | Codex assigned as distinct Reviewer | resolved |

## Breaking-Change Assessment

- Breaking Change: No
- Affected Consumers: None; initial pre-alpha implementation
- Migration Required: No
- Approval Required: No separate breaking-change approval
- Reference: CHG-001 scope and ADR-0008

## Flow Gates

### Additional Ready Conditions

Ready-to-Build additionally requires:

- the eight initial ADRs are accepted or explicitly recorded as non-blocking drafts;
- this specification is approved;
- the implementation plan is approved or explicitly accepted as sufficient;
- `.ggsad/config.yaml`, the GSD mapping, and `state.yaml` validate;
- GSD-generated artifacts, if present, have been reviewed for scope and authority conflicts;
- the implementation Requestor identity is recorded;
- the distinct Pair Reviewer is assigned as `agent:codex`;
- the working tree is safe and understood.

### Additional Done Conditions

Build-Done additionally requires:

- all Must requirements R-001 through R-020 are implemented;
- all applicable acceptance examples are covered;
- no deferred capability has been introduced;
- all baseline quality commands pass;
- generated and failed operations preserve user files as specified.

Verify-Done additionally requires:

- all acceptance examples pass or have approved equivalent evidence;
- Pair Review is complete;
- no blocking finding remains open;
- deviations and limitations are documented;
- evidence maps requirements to tests and results.

### Additional Wait Conditions

Enter `waiting` when:

- required human approval is missing;
- an ADR remains blocking or conflicts with the specification;
- a material CLI or schema contract decision is unresolved;
- a distinct Pair Reviewer cannot be assigned before verification;
- GSD artifacts conflict with GG-SAD authority and cannot be corrected mechanically;
- a required project artifact is missing or invalid but recoverable.

### Additional Fail Conditions

Fail the flow when:

- the constitution or an accepted ADR is knowingly violated;
- governed state is corrupted and cannot be restored safely;
- implementation introduces an unauthorized breaking change;
- implementation proceeds materially outside CHG-001 scope after detection;
- evidence or approval is fabricated;
- a deferred capability is deliberately implemented despite an explicit stop decision.

## Verification Plan

| Requirement / Example | Verification Method | Expected Evidence | Owner |
|---|---|---|---|
| R-001 / E-001 | CLI acceptance test | test reference and command result | Requestor |
| R-002 / E-002 | filesystem comparison | unchanged-file assertion | Requestor |
| R-003 / E-003 | CLI acceptance test | generated tree and schema result | Requestor |
| R-004 / E-004 | parameterized and property tests | invalid-ID test report | Requestor |
| R-005 / E-005, E-006 | validator tests | config validation report | Requestor |
| R-006 / E-007 | mapping tests | mapping validation report | Requestor |
| R-007, R-008 / E-008 | state and artifact tests | validation report | Requestor |
| R-009 / E-009 | placeholder tests | rejection and unchanged state | Requestor |
| R-010–R-014 / E-010, E-011 | transition tests | state diff and history evidence | Requestor |
| R-015 | CLI error tests | exit code and captured output | Requestor |
| R-016 / E-012 | stand-alone acceptance test | successful isolated workflow | Requestor |
| R-017 / E-007, E-012 | mapping and architecture tests | permission and import results | Requestor |
| R-018 / E-013 | example validation | example validation result | Requestor |
| R-019 / E-014 | quality commands | command evidence | Requestor |
| R-020 / E-015 | Pair Review | review record | Reviewer |

## Pair Review

- Required: Yes
- Activation Basis: architecture, state-transition behavior, schemas, and project policy
- Requestor: agent:claude-code
- Reviewer: agent:codex
- Proposed Review ID: PR-001
- Review Scope:
  - repository structure;
  - `pyproject.toml`;
  - schemas;
  - configuration and mapping contracts;
  - CLI commands;
  - filesystem safety;
  - state-transition behavior;
  - test coverage;
  - scope compliance;
  - evidence.
- Separate `review.md`: Conditional
- Separate Human Approval: Yes for ADR and final project decisions
- Blocking Finding Rule: Unresolved blocking findings prevent Verify-Done and closure.
- Independence Rule: `agent:codex` must operate as a participant distinct from `agent:claude-code`; a Claude subagent or second Claude session does not satisfy this assignment.

## Approval

- Specification Approval Required: Yes
- Approver: human:project-owner
- Approval Status: Approved
- Approval Evidence: Recorded 2026-08-02 — human:project-owner: "Updated spec.md and plan.md are approved by me."

## Open Questions

| ID | Question | Owner | Blocking | Resolution Condition |
|---|---|---|---|---|
| Q-001 | Are ADR-0001 through ADR-0008 accepted, or explicitly non-blocking drafts for CHG-001? | human:project-owner | Resolved (2026-08-02) | Recorded: non-blocking drafts for CHG-001. See Change History and Dependencies and Prerequisites. |
| Q-003 | Is the initial user-facing CLI syntax in this specification approved, or may implementation choose equivalent syntax while preserving behavior? | human:project-owner | Resolved (2026-08-02) | Resolved via plan approval: the reference CLI syntax is `plan.md` §4.2; exact Typer parameter ordering may be refined without changing the behavioral contract. |
| Q-004 | Should repeated `ggsad init` be strictly rejected or safely idempotent for unchanged generated files? | human:project-owner | Resolved (2026-08-02) | Resolved via plan approval: conservative idempotency per `plan.md` §4.1 — unchanged generated files are left as-is, differing files conflict and block further writes, no overwrite flag in CHG-001. |
| Q-005 | Are Class M `tasks.md` files mandatory for CHG-001-generated changes or only for this bootstrap example? | human:project-owner | Resolved (2026-08-02) | Resolved via plan approval: per `plan.md` §4.3, all five artifacts (`state.yaml`, `spec.md`, `plan.md`, `tasks.md`, `evidence.md`) are mandatory for CHG-001-generated Class M changes; a later profile-resolver change may make `tasks.md` conditional. |

## Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Architecture: `docs/architecture.md`
- Roadmap: `docs/roadmap.md`
- ADRs: `docs/adr/ADR-0001-*.md` through `ADR-0008-*.md`
- Plan: `plan.md`
- Tasks: `tasks.md`
- Evidence: `evidence.md`
- State: `state.yaml`
- GSD Mapping: `.ggsad/mappings/gsd.yaml`
- Companion Execution Context: `.planning/` when present

## Change History

| Date | Actor | Status | Summary |
|---|---|---|---|
| 2026-08-02 | human:project-owner | Draft | Initial CHG-001 specification |
| 2026-08-02 | human:project-owner | Draft | Q-001 resolved: ADR-0001 through ADR-0008 recorded as non-blocking drafts for CHG-001 |
| 2026-08-02 | human:project-owner | Draft | Reviewer assigned: `agent:codex` as distinct Pair Reviewer |
| 2026-08-02 | human:project-owner | Draft | Q-003, Q-004, Q-005 resolved via plan approval (see Open Questions) |
| 2026-08-02 | human:project-owner | Approved | Specification approved |
| 2026-08-03 | agent:claude-code | Ready | `ggsad transition CHG-001 ready` succeeded via the engine built in Slice 6, once `evidence.md` (Slice 7) satisfied the last R-011 precondition. See `evidence.md` §6.5 and §15. |
| 2026-08-03 | human:project-owner | Ready | PRF-003 disposition: `ty` (Astral), configured in strict mode via `pyproject.toml` `[tool.ty.rules] all = "error"`, formally adopted in place of `mypy` — resolves the discrepancy DEV-002 flagged and Codex's Pair Review escalated into a blocking finding. `docs/constitution.md` amended to version 0.2 in the same decision (§11 baseline command); `docs/project-brief.md` and `docs/architecture.md` updated to match. See `evidence.md` §9 and §11. |
