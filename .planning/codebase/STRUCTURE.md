# Codebase Structure

**Analysis Date:** 2026-08-18

## Directory Layout

```
ggsad/
├── .ggsad/                    # Runtime config and packaged method assets
│   ├── config.yaml            # Project-level GG-SAD configuration
│   ├── mappings/
│   │   └── gsd.yaml           # Integration mapping example
│   ├── profiles/              # Compliance profile definitions
│   ├── schemas/               # Authoritative JSON Schemas (Draft 2020-12)
│   │   ├── config.schema.json
│   │   ├── state.schema.json
│   │   └── mappings.schema.json
│   └── templates/             # Project initialization templates
│       ├── constitution.template.md
│       ├── project-brief.template.md
│       ├── architecture.template.md
│       └── roadmap.template.md
├── .planning/
│   └── codebase/              # GSD codebase documentation (this file)
├── docs/
│   ├── method/
│   │   ├── GG-SAD_normative_method_specification.md  # Authority
│   │   └── GG-SAD_normative_method_specification_DE.md
│   ├── adr/                   # Architecture Decision Records
│   ├── definitions/           # DoR, DoD, DoW, DoF documents
│   ├── guides/                # User guides
│   ├── superpowers/           # Workflow examples
│   └── *.md                   # Project governance docs (constitution, brief, etc.)
├── examples/
│   ├── governed-enterprise/   # Example project: enterprise governance
│   ├── lean-startup/          # Example project: lightweight startup
│   └── solo-developer/        # Example project: solo developer
├── specs/
│   ├── CHG-001-reference-repository-bootstrap/  # Original bootstrap change
│   │   ├── state.yaml         # Change state (governed)
│   │   ├── spec.md            # Change specification
│   │   ├── plan.md            # Implementation plan
│   │   ├── tasks.md           # Task list
│   │   └── evidence.md        # Completion evidence
│   └── examples/              # Example change structures (never active project state)
│       ├── class-l/
│       ├── class-m/
│       └── class-s/
├── src/
│   └── ggsad/                 # Main Python package (entry point)
│       ├── __init__.py
│       ├── cli.py             # Typer CLI app: init, new, validate, transition
│       ├── application/       # High-level operations and manifests
│       │   ├── __init__.py
│       │   ├── initialize_project.py
│       │   ├── create_change.py
│       │   ├── validate_repository.py
│       │   └── manifest_writer.py
│       ├── engine/            # Low-level state management and atomic operations
│       │   ├── __init__.py
│       │   ├── transitions.py
│       │   └── state_writer.py
│       ├── models/            # Pydantic data models (typed governance structures)
│       │   ├── __init__.py
│       │   ├── state.py       # ChangeState, HistoryEvent, etc.
│       │   ├── config.py      # ProjectConfig, IntegrationDeclaration
│       │   ├── mapping.py     # IntegrationMapping
│       │   └── validation.py  # ValidationIssue, IssueCategory
│       ├── validators/        # Stateless validation functions
│       │   ├── __init__.py
│       │   ├── schema_validator.py      # JSON Schema validation (R-005, R-006, R-007)
│       │   ├── compliance_profile.py    # Compliance profile validation (E-006)
│       │   ├── mapping_authority.py     # Mapping companion authority (R-017)
│       │   ├── artifact_presence.py     # Required artifact checks (R-008)
│       │   ├── placeholder_detector.py  # Unresolved placeholder detection (R-009)
│       │   └── yaml_loader.py           # YAML parsing with error handling
│       └── resources/         # Packaged method assets (templates, schemas)
│           ├── __init__.py
│           ├── mappings/
│           ├── schemas/
│           └── templates/
├── tests/
│   ├── acceptance/            # End-to-end CLI behavior tests
│   │   ├── test_init_acceptance.py
│   │   ├── test_new_acceptance.py
│   │   ├── test_transition_acceptance.py
│   │   └── test_validate_acceptance.py
│   ├── integration/           # Integration tests (file I/O, schema loading)
│   │   ├── test_governed_artifact_validation.py
│   │   ├── test_resource_loading.py
│   │   └── test_standalone_operation.py
│   ├── property/              # Property-based tests (Hypothesis)
│   │   └── test_transition_properties.py
│   ├── unit/                  # Unit tests per module
│   │   ├── test_cli.py
│   │   ├── test_create_change.py
│   │   ├── test_initialize_project.py
│   │   ├── test_validate_repository.py
│   │   ├── test_transitions.py
│   │   ├── test_state_writer.py
│   │   ├── test_schema_validator.py
│   │   ├── test_compliance_profile.py
│   │   ├── test_mapping_authority.py
│   │   ├── test_artifact_presence.py
│   │   ├── test_placeholder_detector.py
│   │   ├── test_models_state.py
│   │   ├── test_models_config.py
│   │   ├── test_models_mapping.py
│   │   ├── test_validation_issue.py
│   │   ├── test_yaml_loader.py
│   │   └── test_version.py
│   └── fixtures/              # Shared test fixtures and helpers
├── pyproject.toml             # Python project config (dependencies, build)
├── README.md
├── LICENSE
├── CLAUDE.md                  # Claude Code instructions
├── AGENTS.md                  # GSD agent definitions
└── .github/workflows/         # CI/CD pipelines

```

## Directory Purposes

**`.ggsad/`:**
- Purpose: Runtime configuration and packaged method assets; materialized by `ggsad init`
- Contains: config.yaml, schemas (JSON), templates (Markdown), integration mappings (YAML)
- Key files: `config.yaml` (project config), `schemas/` (JSON Schema authority), `templates/` (initialization templates)

**`docs/`:**
- Purpose: Project governance documents and method documentation
- Contains: Normative specification, ADRs, definitions (DoR/DoD/DoW/DoF), guides, examples
- Key files: `docs/method/GG-SAD_normative_method_specification.md` (authoritative), `docs/adr/` (decision records), `docs/definitions/` (gate definitions)

**`specs/`:**
- Purpose: Active and example change directories; project change history
- Contains: Class M changes (CHG-NNN-slug), each with state.yaml and artifacts
- Key files: `specs/CHG-001-reference-repository-bootstrap/state.yaml` (change state), spec.md/plan.md/tasks.md/evidence.md (artifacts)
- Note: `specs/examples/` is never active project state; used for documentation only

**`src/ggsad/`:**
- Purpose: Main Python package; entry point for CLI and library use
- Contains: CLI app, application layer, engine, models, validators, resources
- Entry point: `ggsad.cli:app` (Typer application)

**`src/ggsad/cli.py`:**
- Purpose: Typer CLI command dispatcher
- Contains: Four commands (init, new, validate, transition) with argument parsing and output formatting
- Key functions: `main()` (callback), `init_command()`, `new_command()`, `validate_command()`, `transition_command()`

**`src/ggsad/application/`:**
- Purpose: High-level operations and manifest building
- Contains: Project initialization, change creation, repository validation, file write logic
- Key modules:
  - `initialize_project.py` - R-001, R-002: project structure init with conservative idempotency
  - `create_change.py` - R-003, R-004, R-008, R-012: change creation and validation
  - `validate_repository.py` - R-005 through R-009, R-015: validation composition
  - `manifest_writer.py` - R-002, R-012: preflight+write-all-or-nothing

**`src/ggsad/engine/`:**
- Purpose: Low-level state management and atomic filesystem operations
- Contains: State transitions, atomic state.yaml replacement
- Key modules:
  - `transitions.py` - R-010, R-011, R-012, R-013, R-014: draft→ready transition with precondition evaluation
  - `state_writer.py` - R-012, R-013: atomic state.yaml replacement (temp+fsync+validate+replace)

**`src/ggsad/models/`:**
- Purpose: Pydantic-based typed representations of all governed data structures
- Contains: ChangeState, ProjectConfig, IntegrationMapping, ValidationIssue
- Key modules:
  - `state.py` - ChangeState, ChangeIdentity, FlowState, HistoryEvent, etc.; `dump_change_state()` for schema-conformant serialization
  - `config.py` - ProjectConfig, ProjectSection, WorkflowSection, PairReviewPolicy
  - `validation.py` - ValidationIssue, IssueCategory (enum)

**`src/ggsad/validators/`:**
- Purpose: Stateless validation functions; reusable building blocks for precondition checks
- Contains: Schema validation, compliance checking, artifact presence, placeholder detection, mapping authority
- Key modules:
  - `schema_validator.py` - JSON Schema (Draft 2020-12) validation (R-005, R-006, R-007)
  - `compliance_profile.py` - Verify compliance profile exists (E-006)
  - `artifact_presence.py` - Check required Class M artifacts (R-008)
  - `placeholder_detector.py` - Detect `<...>` placeholders in spec.md/plan.md (R-009)
  - `mapping_authority.py` - Validate mapping companion authority (R-017)
  - `yaml_loader.py` - YAML parsing, error wrapping, dump

**`src/ggsad/resources/`:**
- Purpose: Packaged method assets (templates, schemas, mappings) bundled with the package
- Contains: Subdirectories for `mappings/`, `schemas/`, `templates/`
- Key functions: `resource_root()` - returns importlib.resources Traversable for asset access
- Usage: Used by `initialize_project.py` and `create_change.py` to materialize files without depending on repo-level `.ggsad/`

**`tests/`:**
- Purpose: Test suites covering all layers (acceptance, integration, property, unit)
- Contains: Acceptance tests (CLI behavior), integration tests (file I/O), property tests (Hypothesis), unit tests (per module)
- Key patterns:
  - Acceptance tests: Full CLI workflows (init → new → validate → transition)
  - Integration tests: Artifact loading, schema validation, standalone operation
  - Property tests: Transition state transitions (Hypothesis)
  - Unit tests: Per-module logic, error handling, validation rules

## Key File Locations

**Entry Points:**
- `src/ggsad/cli.py` - Typer app root; entry point is `ggsad.cli:app`
- `src/ggsad/cli.py:main()` - Callback for `--version` flag
- `src/ggsad/cli.py:init_command()` - `ggsad init` command
- `src/ggsad/cli.py:new_command()` - `ggsad new` command
- `src/ggsad/cli.py:validate_command()` - `ggsad validate` command
- `src/ggsad/cli.py:transition_command()` - `ggsad transition` command

**Configuration & Schema:**
- `.ggsad/config.yaml` - Project configuration (schema_version, project, method, workflow, pair_review, memory, integrations)
- `.ggsad/schemas/config.schema.json` - Config schema authority (R-005)
- `.ggsad/schemas/state.schema.json` - State schema authority (R-007)
- `.ggsad/schemas/mappings.schema.json` - Mappings schema authority (R-006)
- `src/ggsad/resources/schemas/` - Packaged schema copies

**Core Logic:**
- `src/ggsad/application/initialize_project.py:initialize_project()` - R-001 project init
- `src/ggsad/application/create_change.py:build_change_manifest()` - R-003, R-004 change creation
- `src/ggsad/application/validate_repository.py:validate_repository()` - R-005 through R-009 validation aggregation
- `src/ggsad/engine/transitions.py:perform_transition()` - R-010, R-011 transition logic
- `src/ggsad/engine/state_writer.py:atomic_replace_state()` - R-012, R-013 atomic writes

**Testing:**
- `tests/acceptance/` - Full workflow tests (init, new, validate, transition)
- `tests/integration/` - Schema loading, artifact validation, resource access
- `tests/property/` - Transition state machine properties (Hypothesis)
- `tests/unit/` - Per-module unit tests (validators, models, application)
- `tests/fixtures/` - Shared test utilities

## Naming Conventions

**Files:**
- Python modules: `snake_case.py` (e.g., `create_change.py`, `schema_validator.py`)
- Test files: `test_<module>.py` (e.g., `test_create_change.py`)
- Templates: `<name>.template.md` (e.g., `spec.template.md`, `constitution.template.md`)
- Schemas: `<artifact>.schema.json` (e.g., `state.schema.json`, `config.schema.json`)
- Generated files in change dirs: `<name>.md` (spec.md, plan.md, tasks.md, evidence.md)
- State files: `state.yaml`

**Directories:**
- Packages: `snake_case/` with `__init__.py` (e.g., `application/`, `validators/`)
- Change IDs: `CHG-<three-or-more-digits>-<slug>` (e.g., `CHG-001-reference-repository-bootstrap`)
- Change slugs: `lowercase-hyphenated` (e.g., `reference-repository-bootstrap`)
- Test categories: lowercase (acceptance, integration, property, unit, fixtures)

**Python Names:**
- Classes: `PascalCase` (e.g., `ChangeState`, `ValidationIssue`)
- Functions: `snake_case` (e.g., `build_change_manifest()`, `validate_change_id()`)
- Constants: `UPPER_CASE` (e.g., `CHANGE_ID_PATTERN`, `SUPPORTED_CHANGE_CLASS`)
- Private functions/methods: `_snake_case` (e.g., `_validate_source_state()`)
- Modules: `snake_case.py`

## Where to Add New Code

**New Feature (e.g., new transition type):**
- Primary code: `src/ggsad/engine/transitions.py` (add transition logic) or `src/ggsad/application/` (add high-level operation)
- Precondition checks: `src/ggsad/validators/` (add new validator if needed, or extend existing)
- Data models: `src/ggsad/models/state.py` or `config.py` (if new data structures needed)
- Schema: `.ggsad/schemas/state.schema.json` or `config.schema.json` (update schema authority)
- Tests: `tests/acceptance/` (end-to-end), `tests/unit/test_<new_module>.py` (logic)

**New Validator:**
- Implementation: `src/ggsad/validators/<name>.py` (e.g., `src/ggsad/validators/my_validator.py`)
- Pattern: Function returning `list[ValidationIssue]`; import ValidationIssue from `models/validation.py`
- Integration: Import and call in `src/ggsad/application/validate_repository.py` or `src/ggsad/engine/transitions.py`
- Tests: `tests/unit/test_<name>.py` with parametrized test cases for valid/invalid inputs

**New Command:**
- CLI: Add `@app.command()` function in `src/ggsad/cli.py`
- Implementation: Create new module in `src/ggsad/application/` (e.g., `my_operation.py`)
- Models: Use existing models from `src/ggsad/models/` or extend if needed
- Tests: `tests/acceptance/test_<command>_acceptance.py` for CLI behavior; unit tests for logic

**New Model/Data Structure:**
- Implementation: `src/ggsad/models/<name>.py` (e.g., `src/ggsad/models/new_structure.py`)
- Pattern: Pydantic BaseModel with frozen=True for immutability
- Schema: Add or update `<artifact>.schema.json` in `.ggsad/schemas/` and `src/ggsad/resources/schemas/`
- Tests: `tests/unit/test_models_<name>.py` with serialization/deserialization tests

**New Validator Rule (e.g., new compliance check):**
- Add to existing validator module: `src/ggsad/validators/compliance_profile.py` or create new
- Return ValidationIssue for any violation
- Compose into validation chain: Update `validate_repository()` or precondition evaluation
- Test: Add test cases to `tests/unit/test_<validator>.py`

**Tests:**
- Unit: `tests/unit/test_<module>.py` - test individual functions, error cases, edge cases
- Integration: `tests/integration/test_<feature>.py` - test interaction between modules, file I/O
- Acceptance: `tests/acceptance/test_<command>_acceptance.py` - test full CLI workflows
- Property: `tests/property/test_<feature>_properties.py` - use Hypothesis for property-based tests
- Fixtures: `tests/fixtures/` - shared utilities, factory functions, temp directories

## Special Directories

**`.ggsad/`:**
- Purpose: Runtime configuration and packaged method assets
- Generated: Partially — `config.yaml` is materialized by `ggsad init`; schemas/templates/mappings are packaged copies
- Committed: Yes — schemas and templates are versioned; config.yaml is part of project state

**`src/ggsad/resources/`:**
- Purpose: Bundled assets for `ggsad init` and `ggsad new` without repo dependency
- Generated: No — these are source files packaged with the distribution
- Committed: Yes — all templates, schemas, mappings are part of the package

**`specs/CHG-001-reference-repository-bootstrap/`:**
- Purpose: Original CHG-001 change; demonstrates Class M structure
- Generated: No — manually created during bootstrap; serves as reference
- Committed: Yes — part of project history

**`specs/examples/`:**
- Purpose: Example change structures for documentation
- Generated: No
- Committed: Yes
- Note: Never treated as active project state; `ggsad validate` excludes this directory

**`docs/adr/`:**
- Purpose: Architecture Decision Records (ADRs)
- Generated: No — authored per decision
- Committed: Yes — part of governance records

**`.planning/codebase/`:**
- Purpose: GSD codebase documentation (ARCHITECTURE.md, STRUCTURE.md, etc.)
- Generated: Yes — by `gsd-map-codebase` command
- Committed: Yes — provides context for future work

**`.github/workflows/`:**
- Purpose: CI/CD pipelines
- Generated: No — checked in
- Committed: Yes

---

*Structure analysis: 2026-08-18*
