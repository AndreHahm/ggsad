<!-- refreshed: 2026-08-18 -->
# Architecture

**Analysis Date:** 2026-08-18

## System Overview

GG-SAD (Goal-Gated Spec-Anchored Development) is a reference implementation of a governance-driven development workflow. The system accepts governance commands via CLI, processes them through layered application and validation logic, and maintains immutable state records for project changes.

```text
┌─────────────────────────────────────────────────────────────┐
│                    CLI Interface (Typer)                    │
│                    `src/ggsad/cli.py`                       │
│  init | new | validate | transition                         │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              Application Layer (Operations)                  │
│                `src/ggsad/application/`                     │
│  ┌─────────────────┬──────────────────┬────────────────┐   │
│  │   initialize    │  create_change   │    validate    │   │
│  │   _project      │                  │  _repository   │   │
│  └─────────────────┴──────────────────┴────────────────┘   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     manifest_writer (conservative idempotency)       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┴──────────────┐
        │                            │
┌───────▼──────────┐    ┌───────────▼──────────┐
│  Validators      │    │  Engine              │
│ (Stateless)      │    │  (State Operations)  │
├──────────────────┤    ├──────────────────────┤
│ • schema         │    │ • transitions        │
│ • mapping auth   │    │ • state_writer       │
│ • artifact       │    │   (atomic replace)   │
│ • placeholder    │    │                      │
│ • compliance     │    │                      │
│ • yaml_loader    │    │                      │
└────────┬─────────┘    └──────────┬───────────┘
         │                         │
         └────────────┬────────────┘
                      │
        ┌─────────────▼──────────────┐
        │    Models (Pydantic)       │
        │   `src/ggsad/models/`      │
        ├────────────────────────────┤
        │ • state.py                 │
        │ • config.py                │
        │ • mapping.py               │
        │ • validation.py            │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │    Resources               │
        │ (Packaged Assets)          │
        ├────────────────────────────┤
        │ • Templates (spec, plan)   │
        │ • Schemas (JSON)           │
        │ • Mappings (YAML)          │
        └────────────────────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   Filesystem I/O           │
        │ (YAML, JSON, atomic ops)   │
        └────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| CLI | Command dispatch, argument parsing, user I/O | `src/ggsad/cli.py` |
| initialize_project | Generate default project structure and config | `src/ggsad/application/initialize_project.py` |
| create_change | Build change manifests and initialize change state | `src/ggsad/application/create_change.py` |
| validate_repository | Compose and run all validation checks (R-005 through R-009) | `src/ggsad/application/validate_repository.py` |
| manifest_writer | Conservative-idempotent file write with preflight | `src/ggsad/application/manifest_writer.py` |
| transitions | Evaluate preconditions and perform state.yaml transitions | `src/ggsad/engine/transitions.py` |
| state_writer | Atomic state.yaml replacement with re-validation | `src/ggsad/engine/state_writer.py` |
| schema_validator | JSON Schema (Draft 2020-12) validation | `src/ggsad/validators/schema_validator.py` |
| compliance_profile | Validate compliance profile references | `src/ggsad/validators/compliance_profile.py` |
| mapping_authority | Validate mapping companion authority (R-017) | `src/ggsad/validators/mapping_authority.py` |
| artifact_presence | Verify required Class M artifacts exist | `src/ggsad/validators/artifact_presence.py` |
| placeholder_detector | Detect unresolved placeholders in spec/plan | `src/ggsad/validators/placeholder_detector.py` |
| yaml_loader | Load and dump YAML with error handling | `src/ggsad/validators/yaml_loader.py` |
| ChangeState (model) | Typed representation of change state document | `src/ggsad/models/state.py` |
| ProjectConfig (model) | Typed representation of project configuration | `src/ggsad/models/config.py` |
| ValidationIssue (model) | Normalized validation finding with category and remediation | `src/ggsad/models/validation.py` |
| resources | Access packaged method assets (templates, schemas) | `src/ggsad/resources/` |

## Pattern Overview

**Overall:** Layered command-driven validator pipeline with immutable state management

**Key Characteristics:**
- **Governance-First:** Every operation validates against schemas and compliance rules before any state change
- **Conservative Writes:** Preflight all changes, write atomically, or not at all (R-012, R-013)
- **Validation Composition:** Reusable validators compose into command-specific precondition checks
- **Pydantic Type Safety:** All data models use Pydantic for structural validation and type hints
- **Schema Authority:** JSON Schema (Draft 2020-12) is the canonical structural contract
- **YAML as Config/State:** YAML for all governed files; JSON for schemas only

## Layers

**CLI Layer:**
- Purpose: Parse commands, dispatch to application handlers, format output
- Location: `src/ggsad/cli.py`
- Contains: Typer command group with init, new, validate, transition subcommands
- Depends on: Application layer (initialize_project, create_change, validate_repository, transitions)
- Used by: End users via `ggsad` command

**Application Layer:**
- Purpose: High-level change and project operations; manifest building; validation aggregation
- Location: `src/ggsad/application/`
- Contains: Four modules handling initialization, change creation, validation, and file writes
- Depends on: Models, validators, engine, resources
- Used by: CLI layer and acceptance tests

**Validation Layer:**
- Purpose: Stateless validation of artifacts against schemas, rules, and governance constraints
- Location: `src/ggsad/validators/`
- Contains: Schema validation, YAML loading, compliance checking, artifact presence, placeholder detection, mapping authority
- Depends on: Models (for IssueCategory, ValidationIssue)
- Used by: Application layer (composed by validate_repository) and engine (precondition checks)

**Engine Layer:**
- Purpose: Low-level state management and atomic filesystem operations
- Location: `src/ggsad/engine/`
- Contains: Transition logic (R-010, R-011), atomic state.yaml replacement with re-validation (R-013)
- Depends on: Models, validators
- Used by: Application layer (transitions command) and tests

**Model Layer:**
- Purpose: Pydantic-based typed representations of governed data structures
- Location: `src/ggsad/models/`
- Contains: ChangeState, ProjectConfig, IntegrationMapping, ValidationIssue with normalized serialization
- Depends on: Pydantic
- Used by: All layers (application, engine, validators)

**Resources Layer:**
- Purpose: Provide packaged method assets as importable module resources
- Location: `src/ggsad/resources/`
- Contains: Subdirectories for templates (spec.template.md, plan.template.md, etc.), schemas (JSON), mappings (YAML)
- Depends on: importlib.resources
- Used by: initialize_project and create_change for asset materialization

## Data Flow

### Primary Request Path: `ggsad new`

1. CLI parses change ID, slug, class (`src/ggsad/cli.py:new_command`)
2. Call `build_change_manifest()` to construct change artifacts (`src/ggsad/application/create_change.py`)
   - Validate change ID and slug via regex (`src/ggsad/application/create_change.py:validate_change_id`, `validate_slug`)
   - Resolve `specs/<change-id>-<slug>/` with containment check
   - Load templates from packaged resources (`src/ggsad/resources/`)
   - Construct ChangeState model with initial state (`src/ggsad/models/state.py`)
   - Serialize state via `dump_change_state()` to normalized YAML
3. Call `write_manifest()` with all-or-nothing semantics (`src/ggsad/application/manifest_writer.py`)
   - Preflight all paths (create/unchanged/conflict)
   - Abort if any conflicts found
   - Write all files atomically (parents created as needed)
4. Report created/unchanged paths to user

### Secondary Flow: `ggsad transition`

1. CLI parses change ID and target status (`src/ggsad/cli.py:transition_command`)
2. Call `perform_transition()` to evaluate preconditions and perform draft→ready transition (`src/ggsad/engine/transitions.py`)
   - Locate change directory by ID pattern matching
   - Evaluate R-011 preconditions via `evaluate_transition_preconditions()`:
     - Project config validation (R-005)
     - Mapping validation (R-006, R-017)
     - Artifact presence (R-008)
     - State schema validity (R-007)
     - Placeholder detection (R-009)
     - No active wait/failure condition
     - Source state is exactly `specify/draft`
   - Load current ChangeState from `state.yaml`
   - Construct new ChangeState with updated flow status and history event
   - Serialize new state via `dump_change_state()`
3. Call `atomic_replace_state()` with re-validation before replacement (`src/ggsad/engine/state_writer.py`)
   - Write to temporary file in same directory
   - Flush and fsync
   - Re-validate temporary file against schema
   - Atomically replace real file via `os.replace()`
   - Clean up temporary file on any failure
4. Return transition result (ok/rejected with issues)

### Validation Flow: `ggsad validate`

1. CLI dispatches to `validate_repository()` (`src/ggsad/cli.py:validate_command`)
2. Aggregate all validation checks (`src/ggsad/application/validate_repository.py`)
   - Validate `.ggsad/config.yaml` schema (R-005)
   - Validate compliance profile exists (E-006)
   - For each declared integration mapping:
     - Validate schema (R-006)
     - Validate companion authority (R-017)
   - For each change directory under `specs/`:
     - Validate `state.yaml` schema (R-007)
     - Validate required Class M artifacts present (R-008)
     - Validate spec.md and plan.md for placeholders (R-009)
3. Return flat list of ValidationIssue objects
4. CLI formats as text or JSON and reports

**State Management:**
- Change state lives in `specs/<change-id>-<slug>/state.yaml` as mutable YAML file
- History is append-only within state.yaml (HistoryEvent objects in `history` list)
- No global state: each change is independent; no shared mutable data structures
- Transitions are atomic: either the state.yaml is replaced completely or not at all (R-013)

## Key Abstractions

**ChangeState (Models):**
- Purpose: Typed immutable view of a change's governance state
- Examples: `src/ggsad/models/state.py` contains ChangeState, ChangeIdentity, FlowState, GoalSummary, PairReviewState, WaitState, FailureState, HistoryEvent
- Pattern: Pydantic BaseModel with frozen=True, extra="allow", by_alias=True; `dump_change_state()` for schema-conformant serialization

**ValidationIssue (Models):**
- Purpose: Normalized validation finding with category, location, reason, and remediation hint
- Examples: SCHEMA_VIOLATION, MISSING_ARTIFACT, UNRESOLVED_PLACEHOLDER, MAPPING_AUTHORITY, UNSUPPORTED_TRANSITION
- Pattern: All validators return `list[ValidationIssue]` for consistent reporting (R-015)

**Manifest (Application):**
- Purpose: Path→bytes dict representing all files to be created/updated
- Examples: `build_change_manifest()` returns dict; `write_manifest()` processes it
- Pattern: Preflight every path, write all-or-nothing if no conflicts (R-002, R-012)

**Validator Composition (Application):**
- Purpose: Reuse individual validators in command-specific precondition chains
- Examples: `evaluate_transition_preconditions()` calls `validate_project_config()`, `validate_change()`, plus transition-specific checks
- Pattern: Validators return early on schema issues; semantic checks proceed only if schema is valid

## Entry Points

**`ggsad init [target]`:**
- Location: `src/ggsad/cli.py:init_command`
- Triggers: User runs `ggsad init` or `ggsad init <directory>`
- Responsibilities: Initialize project structure, generate `.ggsad/config.yaml`, materialize templates and schemas, create docs (constitution, project-brief, architecture, roadmap)

**`ggsad new CHG-<N> <slug> --goal <summary> [--class M] [--title <title>] [--target <dir>]`:**
- Location: `src/ggsad/cli.py:new_command`
- Triggers: User runs `ggsad new CHG-002 example-change --goal "Desired outcome"`
- Responsibilities: Validate change ID, slug, title, and required goal; build the change directory manifest; write spec/plan/tasks/evidence templates and goal-bound state.yaml

**`ggsad validate [target] [--change CHG-<N>] [--format text|json]`:**
- Location: `src/ggsad/cli.py:validate_command`
- Triggers: User runs `ggsad validate` or `ggsad validate --change CHG-002`
- Responsibilities: Run all applicable validation checks, report issues in text or JSON format

**`ggsad transition CHG-<N> ready [--actor <id>] [--target <dir>]`:**
- Location: `src/ggsad/cli.py:transition_command`
- Triggers: User runs `ggsad transition CHG-002 ready`
- Responsibilities: Evaluate R-011 preconditions, atomically transition state.yaml from specify/draft to specify/ready, record history event

## Architectural Constraints

- **Threading:** Single-threaded event loop. CLI commands are synchronous; no worker threads or async I/O.
- **Global state:** No module-level singletons or shared mutable state. All state is file-based (state.yaml) or function-local.
- **Circular imports:** None detected. Dependency graph is acyclic: CLI → Application → Validators/Engine/Models → Resources/Filesystem.
- **Atomicity:** State.yaml writes are atomic (temp + fsync + validate + replace). File manifests are all-or-nothing (preflight or abort).
- **Schema Authority:** JSON Schema (Draft 2020-12) is the single source of truth for file structure. Pydantic models are convenience wrappers, not the authority.
- **Extensibility Points:** Mappings (IntegrationDeclaration) allow integration with external systems. Compliance profiles allow rule tailoring. Templates support project customization.

## Anti-Patterns

### Partial State Mutations

**What happens:** Code that loads state.yaml, modifies it in memory, and writes it back without validating the result against the schema.

**Why it's wrong:** A bug in the modification logic can corrupt a governed file (state.yaml is the audit trail and must always be schema-valid per R-007).

**Do this instead:** Use `atomic_replace_state()` in `src/ggsad/engine/state_writer.py`. It serializes to a temp file, re-validates against the schema before replacement, and atomically replaces only if validation passes. This pattern is mandatory for any code that writes to state.yaml.

### Silent Validation Errors

**What happens:** Validators return empty lists instead of detailed issues; callers check `if not issues` without reporting the actual problem.

**Why it's wrong:** Users can't fix issues they don't understand. Validation output must be actionable per R-015.

**Do this instead:** All validators return `list[ValidationIssue]` with category, file, field, reason, and remediation hint. See `src/ggsad/models/validation.py:ValidationIssue`. CLI layer formats these consistently via `str(issue)` which includes all fields.

### Conflicting Manifest Writes

**What happens:** Code writes files one at a time, stopping on first error, leaving a partially-initialized project or change.

**Why it's wrong:** Partial writes violate R-012 (consistent observable behavior) and can leave the repository in an inconsistent state.

**Do this instead:** Use `build_*_manifest()` to construct a complete dict[Path, bytes], then pass to `write_manifest()` in `src/ggsad/application/manifest_writer.py`. This preflights all paths, writes all-or-nothing, and reports created/unchanged/conflicts consistently.

### Ignoring Path Traversal

**What happens:** Code accepts user-supplied change IDs or slugs without validating containment, allowing `../escape` patterns.

**Why it's wrong:** Attacker-controlled paths can write outside the intended directory (violates R-004, E-004).

**Do this instead:** Validate via regex first (`CHANGE_ID_PATTERN`, `SLUG_PATTERN` in `src/ggsad/application/create_change.py`), then verify containment explicitly via `resolve_change_directory()`. Both defenses are mandatory; don't rely on regex alone.

## Error Handling

**Strategy:** Fail fast with detailed, actionable errors. Validators collect all issues before returning; callers decide whether to abort or warn.

**Patterns:**
- CLI commands raise `typer.Exit(code=1)` with error message on validation failure
- Application layer returns `TransitionResult` or `WriteResult` with `ok` boolean and issues tuple
- Validators return `list[ValidationIssue]` for inspection (never raise)
- Schema violations are caught and wrapped in ValidationIssue, never bubble up as jsonschema exceptions
- Transition precondition failures are returned as issues, never written to state.yaml (R-012)
- Atomic writes throw `StateWriteError` if re-validation fails; this is a defensive last line, not expected in normal operation

## Cross-Cutting Concerns

**Logging:** None. This is a governed artifact system; all output is deterministic and traceable via state.yaml history. Debugging via test inspection (fixtures, property tests).

**Validation:** Centralized via `validate_repository()` which composes schema, compliance, artifact, authority, and placeholder checks. Transition-specific preconditions add no-wait/no-failure checks. All validation paths return `ValidationIssue` objects.

**Authentication:** Not implemented in CHG-001. The `actor` field in history events and state.yaml is documentary only (tracks who made transitions). Compliance profile and integration mappings support future auth integrations.

**Audit Trail:** Fully captured in state.yaml `history` list. Every transition appends a HistoryEvent with timestamp, actor, action, before/after state, reason, and evidence references. History is append-only within the mutable state.yaml.

---

*Architecture analysis: 2026-08-18*
