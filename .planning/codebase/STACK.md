# Technology Stack

**Analysis Date:** 2026-08-18

## Languages

**Primary:**
- Python 3.13 - Entire codebase from `src/ggsad/` through tests; reference implementation of GG-SAD method specification

## Runtime

**Environment:**
- Python 3.13.14 (specified in `.python-version`)
- Requires Python >= 3.13 (per `pyproject.toml`)
- Support planned for Python 3.12 and 3.14 (classifiers in `pyproject.toml`)

**Package Manager:**
- `uv` (modern Python package installer; no venv activation required in lock file mode)
- Lockfile: `uv.lock` (present, pinned at `version = 1, revision = 3`)

## Frameworks

**Core:**
- Typer 0.27.0 - CLI framework for GG-SAD command entry point (`src/ggsad/cli.py`); provides `ggsad init|new|validate|transition` commands
- Pydantic 2.13.4 - Data validation and typed models (`src/ggsad/models/`); frozen immutable models for config and state

**Testing:**
- pytest 9.1.1 - Test runner; configured in `pyproject.toml` with strict markers and config
- pytest-cov 7.1.0 - Coverage reporting; 85% minimum coverage required (`tool.coverage.report.fail_under`)
- hypothesis 6.165.0 - Property-based testing; used in `tests/property/`

**Build/Dev:**
- Hatchling 1.27+ - Build backend (`build-system` in `pyproject.toml`); wheel configuration in `tool.hatch.build.targets.wheel`
- Ruff 0.16.1 - Linter and formatter; target Python 3.13 with 100-character line length
- Bandit 1.9.4 - Security linting; configured to skip B101 (assert) in tests
- pre-commit 4.6.1 - Git hook framework; configuration in `.pre-commit-config.yaml`
- build 1.5.0 - Package building backend tool

**Type Checking:**
- ty 0.0.65 - Type checker with strict mode; all 123 rules promoted to error status in `tool.ty.rules`

## Key Dependencies

**Critical:**
- `jsonschema` 4.26.0 - JSON Schema (Draft 2020-12) validation for `.ggsad/schemas/*.schema.json`; used in `src/ggsad/validators/schema_validator.py`
- `pydantic` 2.13.4 - Typed models: `ProjectConfig`, `ChangeState`, validation issue models; frozen immutability enforced
- `ruamel-yaml` 0.19.1 - YAML parsing with preservation of structure; used in `src/ggsad/validators/yaml_loader.py`
- `typer` 0.27.0 - CLI framework; powers all commands in `src/ggsad/cli.py`

**Infrastructure:**
- `colorama` 0.4.6 - Cross-platform colored terminal output (conditional on Windows)
- `packaging` - Version parsing and comparison utilities
- `filelock` - File locking for safe concurrent access

**Testing (Transitive):**
- `attrs` 26.1.0 - Attribute class definition
- `pluggy` 1.6.0 - Plugin system for pytest
- `iniconfig` - INI file parsing
- `coverage` 7.15.2 - Code coverage measurement engine

## Configuration

**Environment:**
- No environment variables required for core operation (no `.env` file in repository)
- All configuration file-based through `.ggsad/config.yaml`
- Project root discovery automatic (current directory by default; `--target` option to override)

**Build:**
- `pyproject.toml` - Single source of truth for metadata, dependencies, and tool config
- `uv.lock` - Reproducible builds; pinned versions for all dependencies
- `.python-version` - Python version specification (3.13.14)
- Ruff config in `pyproject.toml`: target-version=py313, line-length=100, extensive linting rules
- pytest config: strict-config, strict-markers, 85% coverage threshold
- ty (type checker) config: all rules as errors

## Platform Requirements

**Development:**
- Python 3.13+ (3.12 and 3.14 listed as supported classifiers)
- Git (for pre-commit hooks and repository operations)
- No OS-specific requirements; cross-platform (classifiers indicate `Operating System :: OS Independent`)

**Production:**
- Python 3.13+ runtime
- CLI-based execution (no server/daemon mode)
- File-system access for `.ggsad/`, `specs/`, and `docs/` directories
- No database, external services, or cloud dependencies

---

*Stack analysis: 2026-08-18*
