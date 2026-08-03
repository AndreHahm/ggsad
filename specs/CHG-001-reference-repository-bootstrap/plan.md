# Implementation Plan: CHG-001 — Reference Repository Bootstrap

## Metadata

- Change ID: CHG-001
- Status: Approved
- Phase: plan
- Requestor: human:project-owner
- Intended Implementation Requestor: agent:claude-code
- Planner: assistant:draft
- Reviewer: agent:codex
- Approver: human:project-owner
- Created: 2026-08-02
- Last Updated: 2026-08-02
- Specification: `spec.md`
- State: `state.yaml`

## 1. Purpose

This plan defines the smallest coherent technical implementation of CHG-001.

It is subordinate to:

1. `docs/constitution.md`;
2. accepted ADRs;
3. `docs/project-brief.md`;
4. `docs/architecture.md`;
5. the approved CHG-001 `spec.md`.

No implementation may begin until the specification's Ready-to-Build conditions are satisfied.

## 2. Planning Preconditions

- [x] CHG-001 goal and initial scope are defined.
- [x] Initial project documents and templates exist.
- [x] Initial schemas have been drafted.
- [x] Initial ADR proposals exist.
- [x] ADR-0001 through ADR-0008 are accepted or explicitly non-blocking (recorded 2026-08-02).
- [x] CHG-001 specification is approved (2026-08-02).
- [x] Open questions Q-003 through Q-005 are resolved (2026-08-02, via this plan's approval).
- [x] `.ggsad/config.yaml` validates against `config.schema.json` (verified 2026-08-02).
- [x] `.ggsad/mappings/gsd.yaml` validates against `mappings.schema.json` (verified 2026-08-02; schema file renamed from `mapping.schema.json` to match its own `$id` and all referencing documents).
- [x] CHG-001 `state.yaml` validates against `state.schema.json` (verified 2026-08-02, after adding the missing `wait.category`/`wait.safe_state`/`wait.next_action` keys).
- [x] GSD artifacts, if present, are reviewed for authority and scope conflicts (`.planning/` does not yet exist; vacuously satisfied).
- [x] The implementation Requestor is confirmed (`agent:claude-code`, per `spec.md` metadata).
- [x] The distinct Pair Reviewer is assigned as `agent:codex`.
- [x] The working tree is safe and understood (verified 2026-08-02: no commits yet, only untracked files, no conflicts).

Current result: all listed Planning Preconditions are now satisfied. See the Approval section
(§25) and the human-facing report for the final Ready-to-Build call — the state-engine
`draft → ready` transition for CHG-001 itself is a separate, not-yet-exercised action (see below).

## 3. Technical Approach

Implement one vertical CLI slice with clear internal boundaries:

```text
CLI
  ↓
Application Services
  ├── Project Initializer
  ├── Change Creator
  ├── Repository Validator
  └── Transition Service
        ↓
Method Engine
  ├── Models
  ├── Schema Validation
  ├── Document Validation
  ├── Transition Rules
  └── Atomic State Writer
        ↓
Method Assets
  ├── Schemas
  ├── Templates
  ├── Profiles
  └── Mappings
```

The first implementation will:

- keep schemas and templates as packaged repository assets;
- load YAML safely;
- validate YAML instances against JSON Schema;
- use Pydantic models where internal typed behavior is needed;
- expose Typer commands;
- make state writes atomic;
- treat GSD only as a validated optional mapping;
- avoid a generic plugin system, complete gate engine, database, server, or orchestrator.

The implementation should favor explicit small services over a broad framework.

## 4. Resolved Planning Choices

These choices are proposed by this plan and require approval with the plan.

### 4.1 Repeated Initialization

Use conservative idempotency:

- directories may already exist;
- a generated file that already exists with identical content is left unchanged;
- a generated file that exists with different content causes a conflict;
- no overwrite flag is included in CHG-001;
- the command reports created, unchanged, and conflicting paths;
- any conflict prevents further writes unless the operation can be preflighted completely.

This avoids both unsafe overwrite and needless rejection of an unchanged initialized project.

### 4.2 Initial CLI Shape

Use:

```text
ggsad init [TARGET]
ggsad new CHANGE_ID SLUG --class M [--title TEXT] [--target TARGET]
ggsad validate [TARGET] [--change CHANGE_ID] [--format text|json]
ggsad transition CHANGE_ID ready [--actor PARTICIPANT_ID] [--target TARGET]
ggsad --help
```

The exact Typer parameter ordering may be refined without changing the behavioral contract.

Only transition target `ready` from `specify/draft` is supported in CHG-001.

### 4.3 Class M Artifact Contract

For CHG-001, generated Class M changes contain:

- `state.yaml`;
- `spec.md`;
- `plan.md`;
- `tasks.md`;
- `evidence.md`.

All five are validated as required for the initial bootstrap contract.

A later profile-resolver change may make `tasks.md` conditional.

### 4.4 Placeholder Detection

Detect placeholders only in approved forms used by packaged templates:

- `<placeholder>`;
- `<placeholder-or-value>`;
- `<YYYY-MM-DD>`;
- other angle-bracket tokens matching the repository's placeholder convention.

Ignore angle-bracket syntax inside fenced code blocks where it represents examples rather than
unresolved document content, unless the template explicitly marks it as required.

The implementation should centralize this rule so it can evolve later.

## 5. Alternatives Considered

### Option 1 — One Vertical CLI Slice

Implement initialization, creation, validation, and one transition with narrow services.

**Advantages**

- Directly satisfies CHG-001.
- Produces a usable milestone.
- Keeps components testable.
- Avoids premature extension architecture.

**Disadvantages**

- Some later engine capabilities remain intentionally incomplete.
- Initial contracts may require later migration.

**Selected:** Yes.

### Option 2 — Build the Complete Gate Engine First

Implement all DoF, DoW, DoD, and DoR criteria before exposing commands.

**Advantages**

- More complete method semantics.
- Fewer temporary transition rules.

**Disadvantages**

- Excessive CHG-001 scope.
- Delays user-visible value.
- Requires unresolved approval and criterion models.

**Selected:** No.

### Option 3 — Implement a Generic Plugin and Integration Framework

Create a common runtime for GSD and future companions immediately.

**Advantages**

- Broad extensibility.

**Disadvantages**

- Premature abstraction.
- High maintenance cost.
- Conflicts with ADR-0004 and ADR-0008 intent.

**Selected:** No.

### Option 4 — Use Direct YAML Editing Without Internal Models

Operate directly on dictionaries.

**Advantages**

- Less code.

**Disadvantages**

- Weak internal invariants.
- Harder typing and testing.
- Higher transition-risk.

**Selected:** No.

## 6. Proposed Package Structure

```text
src/ggsad/
├── __init__.py
├── cli.py
├── errors.py
├── constants.py
├── application/
│   ├── __init__.py
│   ├── initialize_project.py
│   ├── create_change.py
│   ├── validate_repository.py
│   └── transition_change.py
├── models/
│   ├── __init__.py
│   ├── config.py
│   ├── mapping.py
│   ├── state.py
│   └── validation.py
├── engine/
│   ├── __init__.py
│   ├── transitions.py
│   └── state_writer.py
├── validators/
│   ├── __init__.py
│   ├── yaml_loader.py
│   ├── schema_validator.py
│   ├── document_validator.py
│   ├── path_validator.py
│   └── repository_validator.py
├── templates/
│   ├── __init__.py
│   ├── asset_loader.py
│   └── renderer.py
└── resources/
    ├── schemas/
    ├── templates/
    ├── profiles/
    └── mappings/
```

The exact structure may be simplified if a module would contain no meaningful responsibility.
Empty abstraction layers must not be created merely to match this diagram.

## 7. Affected Components and Artifacts

| Component or Artifact | Planned Change | Requirements |
|---|---|---|
| `pyproject.toml` | Confirm package metadata, dependencies, CLI entry point, tools | R-019 |
| `src/ggsad/cli.py` | Add Typer application and commands | R-001, R-003, R-005, R-010, R-015 |
| Models | Add typed config, mapping, state, and result models | R-005–R-007, R-014 |
| YAML loader | Safe parsing with clear source locations | R-005–R-007, R-015 |
| Schema validator | Draft 2020-12 validation | R-005–R-007 |
| Document validator | Required files and placeholders | R-008, R-009 |
| Project initializer | Preflight and conservative idempotency | R-001, R-002, R-012 |
| Change creator | Validate ID/slug and render Class M artifacts | R-003, R-004 |
| Transition service | Validate and execute draft-to-ready | R-010–R-014 |
| Atomic state writer | Safe temporary write and replace | R-012, R-013 |
| `.ggsad/schemas/` | Install approved schemas | R-005–R-007 |
| `.ggsad/templates/` | Install approved templates | R-001, R-003 |
| `.ggsad/mappings/gsd.yaml` | Provide valid companion mapping | R-006, R-017 |
| `specs/examples/class-m/` | Add complete valid example | R-018 |
| Tests | Add full behavioral coverage | R-001–R-020 |
| `evidence.md` | Record verification and review evidence | R-019, R-020 |

## 8. Architecture Impact

- Impact: Material initial implementation, within approved bootstrap architecture
- ADR Required: Yes; ADR-0001 through ADR-0008
- Architecture Document Update Required: Conditional after implementation confirms actual modules
- Dependency Direction:

```text
CLI → Application → Engine / Validators / Templates → Models / Method Assets
```

Forbidden directions:

- Method models or validators importing Claude Code, GSD, GitHub, IDE, or CI SDKs;
- transition service mutating specifications;
- GSD mapping code approving or closing GG-SAD work;
- templates becoming a second normative source outside the approved asset location.

## 9. Data and State Impact

### Configuration

`.ggsad/config.yaml` is loaded as YAML and validated against the approved schema.

### Mapping

Each referenced mapping is loaded and validated. Ownership and permission semantics remain explicit.

### State

`state.yaml` remains the machine-readable workflow state and contains:

- change metadata;
- flow phase and status;
- goal summary;
- artifact references;
- gate summary where present;
- Pair Review metadata;
- wait and failure metadata;
- history.

### Atomic Write Strategy

For a state transition:

1. read the original bytes;
2. parse and validate;
3. construct the new typed state;
4. serialize to a temporary file in the same directory;
5. flush and, where practical, synchronize;
6. validate the temporary file;
7. replace the original atomically;
8. remove temporary data on failure.

No original state write occurs before all transition checks pass.

## 10. Interface and Compatibility Impact

### CLI

The initial CLI is experimental.

User-facing errors should include:

- error category;
- affected file or change;
- concise reason;
- remediation hint where determinable.

Optional JSON output for validation may be implemented only if it remains small and does not delay
the core text interface.

### File Formats

Schemas define the external structural contract.

Unknown schema versions fail clearly in CHG-001. Migration is deferred.

### Backward Compatibility

No prior stable CLI or schema exists. The change is non-breaking by project policy.

## 11. Security, Privacy, and Compliance Impact

### Threats

- path traversal through target, change ID, slug, or artifact paths;
- unsafe YAML construction;
- partial or destructive writes;
- unintended overwrite of user files;
- secret disclosure through exception output;
- companion mappings granting excessive authority.

### Mitigations

- resolve and verify paths remain under the repository root;
- use safe YAML loading;
- avoid object construction features;
- preflight initialization and creation;
- use atomic state writes;
- sanitize user-facing errors;
- validate mapping permissions;
- require no network access or subprocess execution for core validation.

### Required Review

Pair Review must include filesystem safety, path validation, YAML loading, atomic writing, and
companion authority boundaries.

## 12. Operational Impact

- Deployment: None
- Packaging: Python wheel and source distribution build
- Monitoring: None
- Logging: concise CLI output; no persistent telemetry
- Metrics: None
- Alerting: None
- Support: README and actionable CLI help
- Backup and Recovery: user repository and Git
- Rollback: revert the CHG-001 commit or restore affected generated files from Git
- Network Dependency: None for core commands

## 13. Test and Verification Strategy

### Unit Tests

Cover:

- change ID and slug validation;
- safe path resolution;
- YAML parse errors;
- JSON Schema errors;
- Pydantic model validation;
- placeholder detection;
- initialization preflight;
- template rendering;
- transition rule evaluation;
- history-event creation;
- atomic writer failure cleanup;
- error rendering.

### Integration Tests

Cover:

- packaged resource loading;
- project initialization in a temporary directory;
- Class M creation;
- repository validation;
- mapping validation;
- state serialization and reload;
- stand-alone configuration.

### Acceptance Tests

Implement E-001 through E-015 as CLI-oriented tests using Typer's test runner and temporary
directories.

### Property-Based Tests

Use Hypothesis where useful for:

- invalid and valid change identifiers;
- slug safety;
- path containment;
- transition source-state combinations;
- rejected operations preserving original bytes.

Do not create a full state-machine framework in CHG-001.

## 14. Evidence Strategy

Record in `evidence.md`:

- requirement and example coverage;
- exact quality commands;
- test report references;
- packaging result;
- CLI help result;
- stand-alone workflow result;
- mapping validation result;
- Pair Review cycle and findings;
- deviations and known limitations;
- final gate evaluation.

Large raw outputs should be stored as test reports or command logs and referenced, not duplicated.

## 15. Pair Review Plan

- Required: Yes
- Proposed Review ID: PR-CHG-001-01
- Requestor: agent:claude-code
- Reviewer: agent:codex
- Approver: human:project-owner
- Stable Review Target: reviewed commit or explicitly identified worktree snapshot
- Scope:
  - specification compliance;
  - module boundaries;
  - schemas and fixtures;
  - CLI behavior;
  - path and overwrite safety;
  - YAML security;
  - atomic state updates;
  - invalid transition preservation;
  - stand-alone operation;
  - GSD authority boundaries;
  - deferred-scope exclusion;
  - tests and evidence.
- Blocking-Finding Rule: unresolved blocking or critical findings prevent Verify-Done.
- Re-verification Required: Yes for resolved blocking findings.

The Reviewer must not silently edit the Requestor's work product during the review cycle.

## 16. Migration and Rollback

### Migration

Not required. CHG-001 creates the first pre-alpha contract.

### Rollback

- Revert the implementation commit or change set.
- Remove only files proven to have been generated by CHG-001.
- Preserve user-authored files.
- Restore `state.yaml` from Git or the last valid copy if a defect is discovered.
- Do not run destructive repository cleanup automatically.

### Irreversible Actions

None are approved.

## 17. Dependencies and Permissions

| Dependency or Permission | Owner | Required Before | Failure Behavior |
|---|---|---|---|
| ADR disposition | human:project-owner | Build | wait |
| Specification approval | human:project-owner | Build | wait |
| Plan approval | human:project-owner | Build when required | wait |
| Python and uv | environment owner | Build and verify | wait |
| Project write access | repository owner | Build | wait |
| Pair Reviewer (`agent:codex`) | human:project-owner | Verify | resolved |
| Release credentials | Not applicable | Not applicable | excluded |

## 18. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation | Detection |
|---|---|---|---|---|
| Partial initialization | high | low | Full preflight before writes | acceptance test |
| Partial state write | high | low | atomic replacement | writer tests |
| Path traversal | critical | low | containment validation | property tests |
| YAML unsafe load | critical | low | safe loader only | security review |
| Inconsistent schema and model | high | medium | shared fixtures and contract tests | test suite |
| Overly broad architecture | medium | medium | delete empty abstractions | Pair Review |
| CLI syntax becomes accidental stable API | medium | medium | label pre-alpha, document behavior | docs review |
| GSD authority leak | high | medium | mapping constraints and tests | mapping tests |
| Proposed ADRs remain unresolved | high | high | wait before build | gate check |

## 19. Implementation Sequence

### Slice 1 — Package and Resource Baseline

1. Confirm `pyproject.toml`.
2. Create minimal package and CLI help.
3. Package schemas, templates, profiles, and mappings.
4. Add resource-loading tests.
5. Run formatting, linting, typing, tests, and build.

**Reviewable outcome:** `ggsad --help` works and packaged assets are available.

### Slice 2 — Safe YAML and Schema Validation

1. Implement safe YAML loader.
2. Implement JSON Schema loader and validator.
3. Add normalized validation issue model.
4. Validate config, mappings, and state.
5. Add invalid YAML and schema tests.

**Reviewable outcome:** governed YAML can be validated with actionable errors.

### Slice 3 — Repository Initialization

1. Define the approved generated asset manifest.
2. Implement complete preflight.
3. Implement conservative idempotency.
4. Render and write files safely.
5. Add initialization acceptance tests.

**Reviewable outcome:** a clean project can be initialized safely.

### Slice 4 — Class M Change Creation

1. Implement ID and slug validation.
2. Resolve safe change path.
3. Render five required artifacts.
4. Validate generated state and documents.
5. Add valid and invalid creation tests.

**Reviewable outcome:** a valid Class M change can be created.

### Slice 5 — Repository and Document Validation

1. Compose config, mapping, state, artifact, and placeholder checks.
2. Add repository-level result aggregation.
3. Add text output and non-zero exit codes.
4. Add stand-alone validation tests.
5. Validate the complete Class M example.

**Reviewable outcome:** `ggsad validate` produces actionable repository results.

### Slice 6 — Controlled Draft-to-Ready Transition

1. Implement explicit supported transition rule.
2. Evaluate all CHG-001 transition preconditions.
3. Build history event.
4. Implement atomic state replacement.
5. Add valid and invalid transition tests.
6. Confirm rejected operations preserve original bytes.

**Reviewable outcome:** one controlled state transition works safely.

### Slice 7 — Final Verification and Review Preparation

1. Run all baseline quality commands.
2. Build package.
3. Run CLI help and complete acceptance workflow.
4. Update `evidence.md`.
5. Prepare stable review target.
6. Conduct Pair Review.
7. Resolve and re-verify findings.
8. Evaluate Verify-Done and closure readiness.

## 20. Task Decomposition

The repository includes a separate `tasks.md` for CHG-001 because the change spans multiple vertical slices,
safety-sensitive filesystem behavior, schemas, CLI commands, tests, and independent review.

Tasks must map to the implementation sequence and specification requirements.

## 21. Wait and Fail Handling

### Expected Wait Conditions

| Condition | Owner / Source | Safe State | Resume Condition | Next Action |
|---|---|---|---|---|
| ADRs not dispositioned | human:project-owner | no production implementation | ADR decision recorded | re-evaluate Ready-to-Build |
| Specification not approved | human:project-owner | documents only | approval recorded | begin Slice 1 |
| CLI or artifact contract unresolved | human:project-owner | no affected implementation | decision recorded in spec/plan | update plan |
| GSD conflict | GSD artifact / decision owner | GG-SAD files unchanged | conflict corrected | resume planning |
| Codex Reviewer unavailable at review time | human:project-owner | stable review target | Codex available or replacement distinct Reviewer approved | start review |

### Expected Fail Conditions

| Trigger | Required Response | Preservation Action | Final Status |
|---|---|---|---|
| Irrecoverable governed-state corruption | stop writes and report | preserve files and evidence | FAILED_REPOSITORY_CORRUPTION |
| Unauthorized destructive overwrite | stop operation | preserve before/after evidence | FAILED_POLICY_VIOLATION |
| Deliberate out-of-scope platform implementation | stop affected work | isolate changes | FAILED_SCOPE_VIOLATION |
| Fabricated approval or evidence | stop verification and closure | preserve audit trail | FAILED_INTEGRITY |
| Critical path traversal or unsafe deserialization shipped in review target | stop and isolate | preserve finding evidence | FAILED_SECURITY |

## 22. Delivery and Commit Strategy

- Branch or Worktree: project-defined feature branch or GSD worktree
- Commit Boundaries:
  - package/resource baseline;
  - validation;
  - initialization;
  - change creation;
  - transition;
  - tests and documentation where not naturally colocated.
- Generated Files: only approved assets and test fixtures
- Review Target: one stable commit series or squashed review commit, according to repository policy
- Merge or Release Policy: no automatic merge or release under CHG-001
- GSD `/gsd-ship`: PR preparation only after GG-SAD Verify-Done prerequisites

## 23. Plan Validation

Before approval, confirm:

- [x] Every planned capability maps to CHG-001 requirements.
- [x] Deferred capabilities remain excluded.
- [x] Verification and evidence work are included.
- [x] Migration and rollback behavior are defined.
- [x] Wait and fail handling are explicit.
- [x] Pair Review is required and scoped.
- [x] ADR dispositions are recorded.
- [x] Specification open questions are resolved.
- [x] The user-facing CLI and artifact contract are approved.
- [x] The distinct Reviewer is assigned as `agent:codex`.

## 24. Decisions and References

| Decision | Type | Reference |
|---|---|---|
| Python reference engine | ADR | `docs/adr/ADR-0001-use-python-for-reference-engine.md` |
| Markdown governing documents | ADR | `docs/adr/ADR-0002-use-markdown-for-governing-documents.md` |
| YAML configuration and state | ADR | `docs/adr/ADR-0003-use-yaml-for-configuration-and-state.md` |
| Layered core and integrations | ADR | `docs/adr/ADR-0004-separate-method-core-from-integrations.md` |
| Explicit transition actions | ADR | `docs/adr/ADR-0005-use-explicit-state-transition-actions.md` |
| GSD execution companion | ADR | `docs/adr/ADR-0006-use-gsd-as-initial-execution-companion.md` |
| One agent with phase workflows | ADR | `docs/adr/ADR-0007-use-one-agent-with-phase-workflows.md` |
| Deferred platform capabilities | ADR | `docs/adr/ADR-0008-defer-memory-mcp-web-ui-and-orchestration.md` |
| Conservative idempotent initialization | Plan proposal | Section 4.1 |
| Initial CLI shape | Plan proposal | Section 4.2 |
| Five Class M artifacts | Plan proposal | Section 4.3 |
| Placeholder syntax | Plan proposal | Section 4.4 |

## 25. Approval

- Approval Required: Yes
- Approver: human:project-owner
- Status: Approved
- Evidence: Recorded 2026-08-02 — human:project-owner: "Updated spec.md and plan.md are approved by me."

## 26. Plan History

| Date | Actor | Status | Summary |
|---|---|---|---|
| 2026-08-02 | assistant:draft | Draft | Initial CHG-001 implementation plan |
| 2026-08-02 | human:project-owner | Draft | ADR-0001 through ADR-0008 recorded as non-blocking drafts for CHG-001 |
| 2026-08-02 | human:project-owner | Draft | Reviewer assigned: `agent:codex`; `tasks.md` created |
| 2026-08-02 | human:project-owner | Approved | Plan approved; Q-003, Q-004, Q-005 thereby resolved |
