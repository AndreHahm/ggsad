# Coding Conventions

**Analysis Date:** 2026-08-18

## Naming Patterns

**Files:**
- Module files use `snake_case.py`
- Package directories use `snake_case`
- Examples: `create_change.py`, `schema_validator.py`, `test_models_state.py`

**Functions and Methods:**
- Use `snake_case` for function names
- Use `snake_case` for method names
- Examples: `validate_change_id()`, `build_change_manifest()`, `resolve_change_directory()`

**Classes:**
- Use `PascalCase` for class names
- Use `PascalCase` for exception classes
- Examples: `ChangeState`, `FlowState`, `ChangeCreationError`, `InvalidChangeIdentifierError`

**Constants:**
- Use `UPPERCASE_SNAKE_CASE` for module-level constants
- Use `frozenset()` for immutable collections (see `KNOWN_BUILTIN_PROFILES` in `src/ggsad/validators/compliance_profile.py`)
- Examples: `CHANGE_ID_PATTERN`, `SLUG_PATTERN`, `SUPPORTED_CHANGE_CLASS = "M"`

**Test Functions:**
- Format: `test_[what_it_tests]()` (no arguments required beyond module-level data)
- Examples: `test_parses_valid_state_and_aliases_class_field()`, `test_e001_initialize_a_clean_repository()`
- Specification references in test names when applicable: `test_e001_*`, `test_no_source_module_imports_a_forbidden_integration_sdk()`

**Private Functions:**
- Prefix with single underscore: `_echo_manifest_result()`, `_imported_module_names()`, `_set_source_state()`
- Used for internal helpers and test-level fixtures

## Code Style

**Formatting:**
- Line length: 100 characters (configured in `pyproject.toml` under `[tool.ruff]`)
- String quotes: double quotes (`"string"` not `'string'`)
- Use `docstring-code-format = true` to format code blocks within docstrings

**Linting:**
- Tool: **Ruff** 0.16.1+ (see `pyproject.toml` [tool.ruff.lint])
- Enabled rules: A, ANN, ARG, B, C4, DTZ, E, F, I, N, PERF, PIE, PL, PTH, RUF, S, SIM, T20, TRY, UP
- Ignored rules: S101 (assert use in production code)
- Test-specific ignores: ANN, ARG, PLR2004, S (in `tests/**/*.py`)
- Type checking: **ty** 0.0.65 in strict mode (all rules = "error") targeting Python 3.13

**Import Organization:**
1. `from __future__ import annotations` (always first)
2. Standard library imports
3. Third-party imports (grouped by category)
4. Local imports (from `ggsad.*`)

Path aliases configured in ruff: `src`, `tests`

**Line Suppression:**
- Use `# noqa: RULE` with explanation comments
- Example: `# noqa: ANN401 -- parsed YAML/JSON is dynamically typed until schema-checked`
- Never skip hooks or disable signing (security/governance requirement)

## Type Annotations

**All Parameters and Returns:**
- Every function parameter MUST have a type annotation
- Every function MUST have a return type annotation (including `-> None`)
- Use Python 3.10+ union syntax: `str | None` not `Optional[str]`

**Type Annotation Tools:**
- `Annotated` from `typing` for CLI arguments with metadata (see `src/ggsad/cli.py`)
- `Field(alias=...)` from Pydantic for schema field mapping (see `src/ggsad/models/state.py`)
- `ConfigDict` from Pydantic for model configuration (frozen=True, extra="allow")

**Dynamic Types:**
- When receiving parsed YAML/JSON before validation, use `Any` with justification
- Example: `data: Any,  # noqa: ANN401 -- parsed YAML/JSON is dynamically typed until schema-checked`

## Import Organization

**File Header Pattern:**
```python
"""Module docstring."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import typer
from pydantic import BaseModel

from ggsad.models.state import ChangeState
from ggsad.validators.schema_validator import load_schema
```

**Circular Import Prevention:**
- Use `from __future__ import annotations` to defer type annotation evaluation
- Avoid importing at module level; use function-level imports if needed
- Group imports: stdlib → third-party → local

## Docstrings

**Module Level:**
- First line: one-sentence summary of module purpose
- Can include specification references (e.g., "Class M change creation (R-003, R-004, R-008, R-012)")
- Multi-paragraph description of implementation details when helpful
- Example from `src/ggsad/application/create_change.py` (lines 1-17)

**Function/Method Level:**
- Google-style format with one-sentence summary
- Sections: Summary, Args (if not using Annotated), Returns, Raises (if applicable)
- Keep summaries concise; detailed explanation in body if needed
- Example from `src/ggsad/cli.py` lines 47-53:
  ```python
  """Echo a WriteResult's created/unchanged/conflict paths consistently.

  Shared by `init` and `new`: both write a manifest with the same
  conservative-idempotent contract (R-002, R-012), so they report it the
  same way rather than drifting into two slightly different formats.
  """
  ```

**Class Level:**
- Describe purpose and configuration
- If using Pydantic, reference schema files
- Example from `src/ggsad/models/state.py` (lines 1-8)

## Error Handling

**Exception Hierarchy:**
- Create domain-specific base exception classes
- Inherit from built-in exceptions or domain bases (not Exception directly)
- Example hierarchy in `src/ggsad/application/create_change.py`:
  ```python
  class ChangeCreationError(ValueError):
      """Base for `ggsad new` rejections (R-004 validation, R-012 containment/conflict)."""

  class InvalidChangeIdentifierError(ChangeCreationError):
      """Raised when a change ID, slug, or class fails R-004 validation."""

  class ChangeAlreadyExistsError(ChangeCreationError):
      """Raised when the target change directory already exists."""
  ```

**Exception Docstrings:**
- Explain when and why the exception is raised
- Reference applicable specification rules

**Error Messages:**
- Include context: what failed, expected format, concrete examples
- Use f-strings with `!r` for repr formatting
- Example from `src/ggsad/application/create_change.py` line 77-80:
  ```python
  msg = (
      f"Invalid change ID {change_id!r}: must match 'CHG-' followed by "
      "three or more digits, e.g. 'CHG-002'."
  )
  raise InvalidChangeIdentifierError(msg)
  ```

**Validation Functions:**
- Raise specific exceptions with actionable messages
- Don't return success/failure; raise if invalid
- Use defense-in-depth comments explaining why checks seem redundant

## Logging

**Framework:** Console output via `typer.echo()` (not `print()`)

**Patterns:**
- CLI commands use `typer.echo()` for user-facing output
- No application-level logging library (logs via domain exceptions and validation results)
- Return domain objects containing validation issues/results for structured output
- Example from `src/ggsad/cli.py` lines 54-66

## Comments

**When to Comment:**
- Explain *why*, not *what* (code should be clear on *what*)
- Decision points: explain rationale or reference specification
- Defensive checks: note they're redundant and why
- Complex algorithms: break into logical steps

**Style:**
- Section comments use `# --- section name ---` format (see `tests/unit/test_create_change.py`)
- Reference specification IDs: `(R-003, R-004)`, `(T-040)`, `(E-001)`
- Use comments strategically; well-named functions don't need comments

**Specification References:**
- Use `(R-NNN)` for requirement references
- Use `(T-NNN)` for test case references
- Use `(E-NNN)` for exemplar/example references
- Use `(ADR-NNN)` for architecture decision records

## Function Design

**Size:**
- Keep functions focused on a single responsibility
- Most functions fit within 50 lines; complex validation/processing may be longer
- Break logic into multiple functions rather than deep nesting

**Parameters:**
- Use keyword-only parameters for optional/configuration arguments: `def func(*, option: str) -> None:`
- Use `Annotated` for CLI-level parameters with typer metadata
- Avoid positional parameters after keyword-only marker

**Return Values:**
- Return domain objects, not primitive types when possible
- Return collections of objects for multiple results: `list[ValidationIssue]`
- Use `-> None` explicitly for functions with side effects only
- Examples: `ChangeState`, `ValidationIssue`, `list[str]`

**Side Effects:**
- Functions that write files document this in docstring and naming
- Example: `write_manifest()`, `dump_change_state()`

## Module Design

**Exports:**
- Define `__all__` to control public API
- Include only stable, intended exports
- Example from `src/ggsad/__init__.py`: `__all__ = ["__version__"]`

**Constants:**
- Define at module level for cross-function reuse
- Use `frozenset()` for immutable constant collections
- Use compiled regex patterns at module level: `CHANGE_ID_PATTERN = re.compile(r"^CHG-\d{3,}$")`

**Barrel Files (Packages):**
- Package `__init__.py` files export key types and functions
- Example: `src/ggsad/models/__init__.py` exports all model classes

## Pydantic Models

**Configuration:**
- All models use `model_config = ConfigDict(...)` for consistency
- Standard settings:
  - `frozen=True` for immutable data models
  - `extra="allow"` to preserve unknown fields (schema evolution safety)
  - `populate_by_name=True` to support both field names and aliases

**Aliases:**
- Use `Field(alias="class")` when schema field name conflicts with Python keywords
- Populate by name allows both `change_class` (Python) and `class` (schema) to work

**Validation:**
- Use Pydantic's `.model_validate()` for parsing data
- Use `.model_dump(mode="json")` when serializing to JSON

---

*Convention analysis: 2026-08-18*
