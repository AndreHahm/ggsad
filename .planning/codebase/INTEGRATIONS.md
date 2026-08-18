# External Integrations

**Analysis Date:** 2026-08-18

## APIs & External Services

**None currently.**

The GG-SAD reference implementation does not depend on external APIs or cloud services. All functionality is self-contained within the codebase and operates entirely on the local filesystem.

## Data Storage

**Databases:**
- Not applicable. No relational or NoSQL database integration.

**File Storage:**
- Local filesystem only
- Configuration: `.ggsad/` directory structure (templates, schemas, mappings, profiles)
- Governed artifacts: `specs/` directory (change manifests, state files, specifications)
- Project documentation: `docs/` directory (constitution, brief, architecture, ADRs, definitions)
- Runtime state: YAML files written atomically by `src/ggsad/engine/state_writer.py`

**Caching:**
- No caching layer
- In-memory caching only during CLI invocation

## Authentication & Identity

**Auth Provider:**
- None. No external authentication service.
- Participant identity is self-declared via CLI `--actor` parameter (defaults to `"cli-user"`)
- Tracked in `state.yaml` history as `HistoryEvent.actor` field

**Access Control:**
- File system permissions (Unix-style read/write/execute)
- No role-based access control enforcement in code
- Delegated to project `docs/constitution.md` (governance layer above the tool)

## Monitoring & Observability

**Error Tracking:**
- None. No error tracking service integration.
- Errors raised as Python exceptions with descriptive messages
- Exit codes used for shell integration (0=success, 1=failure)

**Logs:**
- Console output via `typer.echo()`
- JSON output format available for machine parsing (`--format json` in validate command)
- No persistent logging; all output is transient to stdout/stderr

**Validation Output:**
- Structured `ValidationIssue` model with category, file, field, reason, remediation
- JSON serializable for downstream consumption

## CI/CD & Deployment

**Hosting:**
- Not applicable. GG-SAD is a CLI tool (not a service).
- Distributed as Python package via PyPI (implied by `project.scripts.ggsad` entry point in `pyproject.toml`)

**CI Pipeline:**
- Not present in repository (no GitHub Actions, GitLab CI, or similar workflows committed)
- Local pre-commit hooks available; configuration in `.pre-commit-config.yaml`

**Package Distribution:**
- Build backend: Hatchling (configured in `pyproject.toml`)
- Package name: `ggsad`
- Version: 0.1.0 (pre-alpha reference implementation)
- Entry point: `ggsad = "ggsad.cli:app"`

## Environment Configuration

**Required env vars:**
- None. All configuration is file-based.

**Secrets location:**
- Not applicable. No credentials, API keys, or secrets managed by the tool.
- Project governance rules may place sensitive declarations in `docs/constitution.md` (not read by tool code)

**Configuration files:**
- `.ggsad/config.yaml` - Master configuration (project, method, workflow, pair review policy)
- `.ggsad/schemas/` - JSON Schema documents (config, mappings, state schema)
- `.ggsad/templates/` - Markdown templates for artifacts (spec, plan, evidence, etc.)
- `.ggsad/mappings/` - Integration mappings (e.g., `gsd.yaml` for GSD companion integration)
- `.ggsad/profiles/` - Compliance profile definitions (lean, standard, governed, regulated)

## Webhooks & Callbacks

**Incoming:**
- None. GG-SAD is pull-based (runs on developer invocation).

**Outgoing:**
- None. No notifications, callbacks, or event webhooks.
- State transitions recorded locally in `specs/<change-id>/state.yaml` with full history

## Companion Integrations

**GSD (Goal-Gated Spec-Anchored Development):**
- ID: `gsd`
- Mode: `companion`
- Mapping: `.ggsad/mappings/gsd.yaml`
- Enabled: true
- Purpose: Maps GG-SAD governance artifacts to external GSD workflow tools/agents
- Does not expose external APIs; defines how GG-SAD state maps to external tool semantics
- Per `docs/method/GG-SAD_normative_method_specification.md` § 3.8, GG-SAD retains authority while companion method provides execution capabilities

**Extensibility:**
- Additional integrations can be declared in `.ggsad/config.yaml` under `integrations[]`
- Each integration requires:
  - `id`: Unique identifier
  - `mode`: `companion` or other mode
  - `mapping`: Path to mapping YAML
  - `enabled`: Boolean flag

---

*Integration audit: 2026-08-18*
