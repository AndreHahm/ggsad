# Verification Evidence: CHG-001 — Reference Repository Bootstrap

## Metadata

- Change ID: CHG-001
- Phase: verify
- Status: Active
- Evidence Owner: agent:claude-code
- Requestor: agent:claude-code
- Reviewer: agent:codex (Pair Review not yet conducted — see Section 9)
- Created: 2026-08-03
- Last Updated: 2026-08-03
- Specification: `spec.md`
- Plan: `plan.md`
- State: `state.yaml`
- Review Record: Not yet created (Section 9)

## 1. Evidence Principles

- Evidence demonstrates completion; it does not replace the specification.
- Results MUST identify whether a check was executed, passed, failed, skipped, unavailable, or not
  applicable.
- Durable reports SHOULD be referenced rather than copied in full.
- Evidence MUST NOT contain secrets or unnecessary sensitive data.
- A status MUST NOT be based solely on assertion.

This document reports only what was actually executed during this session. Pair Review (Section
9) has not occurred and is reported as `Not Run`, not as passed or waived.

## 2. Verification Environment

| Item | Value |
|---|---|
| Repository Revision | Uncommitted working tree (no commits exist yet on `main`) |
| Branch / Worktree | `main`, all files untracked |
| Operating System | Windows 11 (win32) |
| Runtime | Python 3.13.14 |
| Toolchain | `uv`, `ruff` 0.16.1, `ty` 0.0.65, `pytest` 9.1.1, `pytest-cov` 7.1.0, `hypothesis` 6.165.0, `bandit` 1.9.4, `hatchling` |
| Configuration / Profile | `.ggsad/config.yaml`: `operating_mode: combination`, `compliance_profile: standard`, integration: `gsd` (companion) |
| Date and Time | 2026-08-03 (session-local; see individual command results below) |

## 3. Requirement Coverage

| Requirement | Acceptance Example / Condition | Verification Method | Evidence | Result |
|---|---|---|---|---|
| R-001 | E-001 | CLI acceptance test | `tests/acceptance/test_init_acceptance.py::test_e001_*` | Pass |
| R-002 | E-002 | CLI acceptance test + unit tests | `test_init_acceptance.py::test_e002_*`, `tests/unit/test_initialize_project.py` (idempotency) | Pass |
| R-003 | E-003 | CLI acceptance test | `tests/acceptance/test_new_acceptance.py::test_e003_*` | Pass |
| R-004 | E-004 | Parameterized + property tests | `tests/unit/test_create_change.py` (parameterized invalid IDs/slugs, Hypothesis property test) | Pass |
| R-005 | E-005, E-006 | Validator unit + acceptance tests | `tests/integration/test_governed_artifact_validation.py` (E-005), `tests/acceptance/test_validate_acceptance.py` (E-006), `tests/unit/test_validate_repository.py` | Pass |
| R-006 | E-007 | Validator unit + acceptance tests | `tests/integration/test_governed_artifact_validation.py::test_e007_*`, `tests/unit/test_mapping_authority.py` | Pass |
| R-007 | — | Schema + model tests | `tests/unit/test_models_state.py`, `tests/unit/test_validate_repository.py` (state schema checks) | Pass |
| R-008 | E-008 | Unit + acceptance tests | `tests/unit/test_artifact_presence.py`, `tests/acceptance/test_validate_acceptance.py::test_e008_*` | Pass |
| R-009 | E-009 | Unit + acceptance tests | `tests/unit/test_placeholder_detector.py`, `tests/acceptance/test_transition_acceptance.py::test_e009_*` | Pass |
| R-010 | E-010 | CLI acceptance test | `tests/acceptance/test_transition_acceptance.py::test_e010_*` | Pass |
| R-011 | E-009, E-011 | Unit + property tests | `tests/unit/test_transitions.py`, `tests/property/test_transition_properties.py` (all 80 schema-valid phase/status combinations) | Pass |
| R-012 | E-002, E-004, E-009, E-011 | Byte-preservation assertions throughout | Every rejection test above asserts unchanged bytes; property test covers this exhaustively for transitions | Pass |
| R-013 | — | Unit tests of the writer | `tests/unit/test_state_writer.py` (valid write, temp-file cleanup, invalid-content rejection + original preserved) | Pass |
| R-014 | — | Acceptance test | `test_transition_acceptance.py::test_e010_*` asserts all 7 required history fields | Pass |
| R-015 | — | Exit codes, no tracebacks, file identification, throughout | Every acceptance test asserts non-zero exit and file/reason presence in output; `ValidationIssue.__str__` tested in `tests/unit/test_validation_issue.py` | Pass |
| R-016 | E-012 | Stand-alone acceptance test + manual run | `tests/integration/test_standalone_operation.py`; manually ran the full init → new → validate → transition lifecycle stand-alone this session (Section 6.4) | Pass |
| R-017 | E-007, E-012 | Mapping + architecture tests | `test_mapping_authority.py`; no forbidden import in `src/ggsad/` (AST-scanned) | Pass |
| R-018 | E-013 | Example validation | `specs/examples/class-m/`; `tests/acceptance/test_validate_acceptance.py::test_e013_*` | Pass |
| R-019 | E-014 | Quality commands | Section 5 below | Pass |
| R-020 | E-015 | Static audit (this session) | Section 6.5 below | Pass |

## 4. Acceptance Example Coverage

| Example | Covers | Evidence | Result | Notes |
|---|---|---|---|---|
| E-001 | R-001 | `test_init_acceptance.py::test_e001_initialize_a_clean_repository` | Pass | |
| E-002 | R-002, R-012 | `test_init_acceptance.py::test_e002_reject_unsafe_reinitialization` | Pass | |
| E-003 | R-003, R-004 | `test_new_acceptance.py::test_e003_create_a_valid_class_m_change` | Pass | |
| E-004 | R-004, R-012, R-015 | `test_new_acceptance.py::test_e004_reject_an_invalid_change_identifier` | Pass | |
| E-005 | R-005, R-015 | `test_governed_artifact_validation.py::test_e005_*` | Pass | |
| E-006 | R-005 | `test_validate_acceptance.py::test_e006_unknown_compliance_profile_fails` | Pass | |
| E-007 | R-006, R-017 | `test_governed_artifact_validation.py::test_e007_*`, and this session's direct check against the real `.ggsad/mappings/gsd.yaml` (Section 6.2) | Pass | |
| E-008 | R-007, R-008 | `test_validate_acceptance.py::test_e008_missing_plan_is_identified_*` | Pass | |
| E-009 | R-009, R-011 | `test_transition_acceptance.py::test_e009_*` | Pass | |
| E-010 | R-010, R-011, R-013, R-014 | `test_transition_acceptance.py::test_e010_*` | Pass | |
| E-011 | R-010, R-011, R-012 | `test_transition_acceptance.py::test_e011_*` | Pass | |
| E-012 | R-016 | `test_standalone_operation.py`; manual full-lifecycle run (Section 6.4) | Pass | |
| E-013 | R-018 | `test_validate_acceptance.py::test_e013_*`; `specs/examples/class-m/` | Pass | |
| E-014 | R-019 | Section 5 (this document) | Pass | |
| E-015 | R-020 | Section 6.5 (this document) | Pass | |

## 5. Quality Gates

All commands run this session (2026-08-03), immediately before writing this file, against the
working tree in its current (uncommitted) state.

| Gate | Command | Result | Evidence | Notes |
|---|---|---|---|---|
| Environment / Dependency Sync | `uv sync` | Pass | "Resolved 44 packages... Audited 44 packages" | |
| Formatting | `uv run ruff format --check .` | Pass | "63 files already formatted" | |
| Linting | `uv run ruff check .` | Pass | "All checks passed!" | |
| Type Checking | `uv run ty check` | Pass | "All checks passed!" | Constitution/spec baseline commands say `mypy`; `pyproject.toml` only installs `ty`. Flagged to the Requestor in Slice 2, not resolved — a docs-vs-tooling decision outside this session's authority. |
| Unit + Integration + Acceptance + Property Tests | `uv run pytest` | Pass | 142 passed, 98.56% line coverage (threshold: 85%) | |
| Security | `uv run bandit -r src/ggsad` | Pass | "No issues identified" (1336 lines scanned) | |
| Build / Packaging | `uv build` | Pass | Built `ggsad-0.1.0.tar.gz` and `ggsad-0.1.0-py3-none-any.whl` | |
| CLI Help | `uv run ggsad --help` | Pass | Exit 0; lists `init`, `new`, `validate`, `transition` | |

## 6. Detailed Test Results

### 6.1 Full Test Suite

- Command:
  ```bash
  uv run pytest
  ```
- Result: Pass
- Exit Code: 0
- Report: 142 passed in 11.11s; coverage 98.56% (`src/ggsad/application/create_change.py` 94%,
  `initialize_project.py` 96%, `validate_repository.py` 99%, `cli.py` 96%, all other modules
  100%)
- Summary: All unit, integration, acceptance, and property tests pass.
- Limitations: The uncovered lines are documented, deliberate defensive branches — path-
  containment checks made unreachable by upstream regex validation, and `StateWriteError`'s
  "last line of defense" branch (a bug in state construction would need to occur for it to
  trigger) — not gaps in requirement coverage. Noted at each site in code comments.

### 6.2 GSD Mapping Authority Boundary (E-007) Against the Real Mapping File

- Command: ad hoc Python check against `.ggsad/mappings/gsd.yaml` (not `uv run pytest`, since this
  specifically re-verifies the *actual repository mapping*, not a synthetic fixture)
- Result: Pass
- Exit Code: not applicable (Python snippet, not a CLI command)
- Report: `validate_mapping_authority()` returns no issues against the real `gsd.yaml`; against a
  mutated copy with `may_approve: true`, structural schema validation still passes (the schema
  only types the field as boolean) but the authority check correctly reports one issue
  identifying `permissions/may_approve`.
- Summary: R-006/R-017 hold in practice, not just in unit test fixtures.

### 6.3 Excluded-Capability Audit (R-020, E-015)

- Command: source tree listing + keyword grep across `src/ggsad/**/*.py`
- Result: Pass
- Report: 22 source files, none named or referencing memory/MCP/web/orchestration capabilities.
  One incidental match for "orchestrat" in `application/__init__.py`'s docstring ("orchestrating
  CHG-001's CLI-visible operations") — ordinary software usage (the CLI layer composing function
  calls), not the excluded multi-agent orchestration sense (ADR-0008). `.ggsad/config.yaml`'s
  generated default is `memory.enabled: false`.
- Summary: no memory backend, MCP server, web UI, issue synchronization, release automation, or
  multi-agent orchestrator is present, confirming E-015.

### 6.4 Full Stand-Alone Lifecycle (E-012)

- Command: manual sequence against a fresh temp directory this session:
  ```bash
  ggsad init /tmp/ggsad-e012
  ggsad new CHG-002 example-change --target /tmp/ggsad-e012
  ggsad validate /tmp/ggsad-e012          # fails: unresolved placeholders (expected)
  # filled in spec.md and plan.md
  ggsad validate /tmp/ggsad-e012          # OK
  ggsad transition CHG-002 ready --actor human:e012-check --target /tmp/ggsad-e012
  ggsad validate /tmp/ggsad-e012          # OK
  ```
- Result: Pass
- Exit Codes: 0, 0, 1 (expected), 0, 0, 0
- Report: the complete init → new → validate → transition lifecycle succeeds stand-alone, with
  `operating_mode: stand-alone` and zero integrations declared, confirming R-016/E-012 beyond the
  automated test suite.

### 6.5 CHG-001's Own Draft-to-Ready Transition (Dogfooding)

- Command: `ggsad transition CHG-001 ready`
- Result: Rejected (correctly)
- Exit Code: 1
- Report: `[missing_artifact] ... evidence.md: Required Class M artifact 'evidence.md' is
  missing.` — the only finding. `state.yaml` confirmed byte-unchanged after the rejected
  attempt.
- Summary: this is not test-suite evidence; it's the real engine, run against this real change,
  in this real repository. It correctly identified that `evidence.md` (this very file) did not
  exist yet. It will be re-run after this file is written (Section 15).

## 7. Negative, Failure, Boundary, and Recovery Evidence

| Scenario | Requirement / Example | Evidence | Result |
|---|---|---|---|
| Reinitializing over a modified `docs/constitution.md` | R-002, R-012 / E-002 | `test_init_acceptance.py::test_e002_*` | Pass |
| Invalid change ID with path-traversal characters | R-004, R-012 / E-004 | `test_new_acceptance.py::test_e004_*` | Pass |
| Re-running `new` against an existing change | R-002 (analogous), R-012 | `test_cli.py::test_new_second_run_on_same_change_id_is_rejected_deterministically` | Pass |
| Invalid YAML in `config.yaml` | R-005 / E-005 | `test_governed_artifact_validation.py::test_e005_*` | Pass |
| Unknown compliance profile | R-005 / E-006 | `test_validate_acceptance.py::test_e006_*` | Pass |
| Mapping granting forbidden authority | R-006, R-017 / E-007 | `test_governed_artifact_validation.py::test_e007_*` | Pass |
| Missing required Class M artifact | R-008 / E-008 | `test_validate_acceptance.py::test_e008_*` | Pass |
| Unresolved placeholder blocks transition | R-009, R-011 / E-009 | `test_transition_acceptance.py::test_e009_*` | Pass |
| Transitioning an already-`ready` change | R-011 / E-011 | `test_transition_acceptance.py::test_e011_*` | Pass |
| Active wait/failure blocks transition | R-011 | `test_transitions.py::test_active_wait_blocks_transition`, `test_active_failure_blocks_transition` | Pass |
| Corrupted serialized state before write | R-013 | `test_state_writer.py::test_atomic_replace_state_rejects_invalid_content_*` | Pass |
| Every non-`specify/draft` source state (80 combinations) | R-011, R-012 | `tests/property/test_transition_properties.py` | Pass |

## 8. Traceability Summary

```text
Goal: create a repository that can initialize a GG-SAD project, create a
Class M change, validate its core artifacts, and perform a controlled
draft-to-ready transition.
|-- R-001..R-004 (init, new, ID/slug validation)
|   `-- E-001..E-004 -> Slices 3-4 tests -> Section 3/4 above
|-- R-005..R-009 (config/mapping/state/artifact/placeholder validation)
|   `-- E-005..E-009 -> Slice 2 + Slice 5 tests -> Section 3/4 above
|-- R-010..R-014 (controlled transition)
|   `-- E-010, E-011 -> Slice 6 tests + property test -> Section 3/4 above
|-- R-015 (actionable errors) -> throughout, ValidationIssue model
|-- R-016..R-018 (stand-alone, GSD subordination, complete example)
|   `-- E-012, E-013 -> Section 6.4, specs/examples/class-m/
`-- R-019..R-020 (quality/packaging, scope discipline)
    `-- E-014, E-015 -> Section 5, Section 6.3
```

## 9. Pair Review

- Required: Yes (per `spec.md`'s Pair Review section and `.ggsad/config.yaml`'s
  `pair_review.required_for` including architecture/state-engine/transition-engine/security-
  relevant work — this change touches all of those)
- Review ID: PR-CHG-001-01 (proposed in `spec.md`/`plan.md`, not yet opened)
- Requestor: agent:claude-code
- Reviewer: agent:codex (assigned in `spec.md`/`plan.md`/`state.yaml`, per `human:project-owner`'s
  instruction earlier in this session)
- Reviewer Type: Agent (external, distinct from the implementing agent)
- Review Scope: as defined in `plan.md` §15 — specification compliance, module boundaries,
  schemas, CLI behavior, path/overwrite safety, YAML security, atomic state updates, invalid-
  transition preservation, stand-alone operation, GSD authority boundaries, deferred-scope
  exclusion, tests and evidence
- Review Target: **not yet prepared.** No commits exist on `main` — the entire working tree is
  untracked. A stable review target (a commit or an explicitly identified worktree snapshot, per
  `plan.md` §15) requires either committing this work or another mechanism for pinning a
  reviewable state, and committing is outside what I do without being asked (see this session's
  operating constraints). **This is a decision point for `human:project-owner`, not something
  resolved in this document.**
- Result: **Not Run**
- Review Evidence: None

### Findings

None — the review has not started.

### Blocking-Finding Summary

- Open Blocking Findings: Not applicable (review not started)
- Resolution Evidence: Not applicable
- Re-verification Required: Not applicable
- Re-verification Result: Not applicable

## 10. Approval Evidence

| Approval | Required | Approver | Status | Evidence |
|---|---|---|---|---|
| Specification | Yes | human:project-owner | Approved | `spec.md` § Approval, recorded 2026-08-02 |
| Plan | Yes | human:project-owner | Approved | `plan.md` §25, recorded 2026-08-02 |
| ADR disposition (ADR-0001–0008) | Yes | human:project-owner | Recorded (non-blocking drafts for CHG-001) | `spec.md` Change History, `state.yaml` history |
| Architecture / ADR (formal acceptance) | Conditional | human:project-owner | Not Required for CHG-001 (drafts are non-blocking) | See ADR disposition above |
| Breaking Change | No | Not applicable | Not Required | `spec.md` Breaking-Change Assessment |
| Release | No | Not applicable | Not Required | CHG-001 does not include release |

## 11. Deviations

| ID | Specification or Plan Reference | Deviation | Impact | Status | Approval / Decision |
|---|---|---|---|---|---|
| DEV-001 | `spec.md` R-005–R-008 vs. `tasks.md` T-024 | E-006 and E-008 initially assigned to Slice 2 (T-024); moved to Slice 5 (T-050/T-052) once building them revealed both need repository-level filesystem context a per-file validator can't provide | None — R-005 through R-008 remain fully implemented; only sequencing across `tasks.md` slices changed | Resolved | `tasks.md` T-024 note, 2026-08-03; `tasks.md` is an execution aid, not `spec.md`/`plan.md`, so no separate approval was required |
| DEV-002 | Constitution / `spec.md` baseline commands say `uv run mypy` | `pyproject.toml`'s dev dependencies only install `ty`, not `mypy`; `ty` was used for every type-checking gate instead | None observed — `ty check` passes cleanly throughout | Open | Flagged to the Requestor (`human:project-owner`) in Slice 2; not resolved by this agent, since changing the documented baseline command is outside this session's authority |
| DEV-003 | `README.md` (not a `spec.md`/`plan.md` artifact — a pre-existing documentation bug found during T-080) | `README.md` referenced a `QUICK_START.md` file, in the repository-structure diagram and a "For the complete... bootstrap, follow" pointer, that does not exist anywhere in the repository | Broken documentation reference for anyone reading the README | Resolved | Both references removed 2026-08-03; the README's own inline Quick Start content already covers the minimal setup path, so no replacement file was authored (outside this task's scope) |

## 12. Known Limitations

- No commits exist on `main`; the entire implementation is in the working tree. A stable Pair
  Review target has not been prepared (Section 9).
- Pair Review (Section 9) has not occurred. Per the constitution, unresolved Pair Review blocks
  Verify-Done for architecture/state-engine/transition-engine/security-relevant work, which this
  change is.
- `mypy` vs. `ty` discrepancy between the documented baseline commands and the actual installed
  tooling (DEV-002) remains open.
- The `review_id` format mismatch flagged earlier this session (`spec.md`/`plan.md` use
  `PR-CHG-001-01`; `state.schema.json`'s `review_id` pattern is numeric-only,
  `^PR-\d{3,}$`) is still unresolved and will matter once Pair Review goes active — `state.yaml`
  currently omits `review_id` rather than picking a side.
- CHG-001's own `draft → ready` transition has not yet succeeded (Section 6.5) — this file's
  creation is the last missing precondition; see Section 15 for the next step.

## 13. Wait and Failure Evidence

### Wait Events

None recorded in `state.yaml`.

### Failure Events

None recorded in `state.yaml`.

## 14. Final Gate Evaluation

Evaluated in the mandatory order: DoF → DoW → current DoD → next DoR.

### Definition of Fail

- Triggered: No
- Criteria: constitution/repository corruption, unauthorized breaking change, unrecoverable state
  mutation, out-of-scope work that can't be isolated
- Evidence: none of these occurred; every rejected operation in this change (Sections 6, 7)
  preserved original files exactly
- Result: Not triggered

### Definition of Wait

- Triggered: **Yes** — Pair Review is required and has not been conducted; a stable review target
  has not been prepared; the reviewer-assignment mechanics (does `human:project-owner` have Codex
  CLI access, or another way to satisfy the distinct-reviewer requirement) are unconfirmed.
- Criteria: `spec.md` § Flow Gates § Additional Wait Conditions — "a distinct Pair Reviewer cannot
  be assigned before verification" is not quite this case (a reviewer *is* assigned: agent:codex)
  but the *mechanism* to actually invoke that review is not yet established
- Evidence: Section 9 above
- Result: **Waiting** — see Section 15 for the exact next action

### Current Definition of Done (Build-Done)

- Satisfied: Yes
- Criteria: `spec.md` § Flow Gates § Additional Done Conditions — all Must requirements R-001
  through R-020 implemented, all applicable acceptance examples covered, no deferred capability
  introduced, all baseline quality commands pass, generated/failed operations preserve user files
- Evidence: Sections 3–7 above
- Result: Build-Done is satisfied

### Next Definition of Ready (for `verify`/`release` phases)

- Satisfied: No
- Criteria: Verify-Done requires Pair Review complete with no open blocking finding (`spec.md` §
  Flow Gates § Additional Done Conditions, "Verify-Done")
- Evidence: Section 9
- Result: Not satisfied — blocked on Pair Review

## 15. Final Result

- Final Status: **Waiting** (build-complete, Verify-Done blocked on Pair Review — see DoW above)
- Recommended Transition: Once this file exists, re-run `ggsad transition CHG-001 ready` — with
  `evidence.md` now present, that specific precondition should now be satisfied. This document
  does not run that command itself, since committing to "the transition already happened" before
  it's actually attempted would be exactly the kind of assertion-based status the constitution
  prohibits.
- Transition Evidence: Not applicable yet — see Recommended Transition above
- Remaining Actions:
  1. Attempt `ggsad transition CHG-001 ready` now that `evidence.md` exists.
  2. `human:project-owner` decision needed: how to establish a stable Pair Review target (commit
     the work, or another mechanism) — this agent does not commit without being asked.
  3. `human:project-owner` decision needed: how to conduct Pair Review with a genuinely distinct
     `agent:codex` participant (external Codex CLI invocation, human-as-reviewer, or an explicit,
     recorded waiver).
  4. Resolve DEV-002 (`mypy` vs. `ty`) and the `review_id` pattern mismatch, at `human:project-
     owner`'s discretion.
- Evidence Owner Statement: All quality gates, acceptance examples, and requirements verifiable
  without external review are confirmed passing, with evidence gathered this session (not
  asserted from memory of earlier sessions). Pair Review has not occurred and is honestly reported
  as such. CHG-001 is Build-Done but not yet Verify-Done.

## 16. Evidence History

| Date | Actor | Revision | Summary |
|---|---|---|---|
| 2026-08-03 | agent:claude-code | 1 | Initial evidence record: Slices 1–6 quality gates, requirement/example coverage, stand-alone and GSD-authority re-verification, excluded-capability audit, and honest Pair Review status |
