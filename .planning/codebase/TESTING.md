# Testing Patterns

**Analysis Date:** 2026-08-18

## Test Framework

**Test Runner:**
- Framework: **pytest** 9.1.1
- Config location: `pyproject.toml` [tool.pytest.ini_options]
- Config: strict-config, strict-markers, xfail_strict = true

**Assertion Library:**
- pytest's built-in assertions (no external library)
- Use `assert` statements directly

**Run Commands:**
```bash
pytest                              # Run all tests
pytest -v                           # Verbose output
pytest tests/unit/                  # Run unit tests only
pytest --cov=ggsad                  # Coverage report
pytest --cov-report=term-missing    # Show missing lines
pytest -k "test_name"               # Run matching tests
pytest --collect-only               # List all tests without running
```

**Coverage:**
- Tool: `pytest-cov` 7.1.0
- Minimum: 85% coverage target (`fail_under = 85`)
- Branch coverage: enabled
- Source: `ggsad` package only
- Report: terminal with missing lines highlighted

## Test File Organization

**Location:**
- Test files co-located with tests directory structure (not with source)
- `tests/unit/test_*.py` for unit tests
- `tests/integration/test_*.py` for integration tests
- `tests/acceptance/test_*.py` for CLI acceptance tests
- `tests/property/test_*.py` for property-based tests

**Naming Convention:**
- Pattern: `test_[module_name].py` mirrors source structure
- Example: `src/ggsad/models/state.py` → `tests/unit/test_models_state.py`
- Example: `src/ggsad/application/create_change.py` → `tests/unit/test_create_change.py`

**Test Function Naming:**
- Format: `test_[subject]_[behavior]()` or `test_[behavior]()`
- Examples:
  - `test_parses_valid_state_and_aliases_class_field()`
  - `test_e001_initialize_a_clean_repository()` (specification reference E-001)
  - `test_valid_change_ids_are_accepted()` (parametrized test)
  - `test_property_any_chg_prefixed_id_with_three_or_more_digits_is_valid()` (property test)

## Test Structure

**Module Organization:**
```
tests/
├── unit/                  # Pure function/class testing
├── integration/           # Component interaction testing
├── acceptance/            # CLI end-to-end testing
└── property/              # Property-based testing with Hypothesis
```

**Test File Header Pattern:**
```python
"""Unit tests for the typed ChangeState model."""

from __future__ import annotations

from typing import Any

from ggsad.models.state import ChangeState

_VALID: dict[str, Any] = {
    # Test data at module level
}

def test_parses_valid_state_and_aliases_class_field() -> None:
    # Test implementation
```

**Key Patterns:**
1. Module-level docstring explains test scope
2. Test data defined at module level (e.g., `_VALID`) for reuse
3. Test functions have no required parameters
4. No conftest.py (fixtures provided by pytest built-ins or module-level setup)
5. All test functions include return type annotation `-> None`

## Parametrized Testing

**Single Parameter Decoration:**
```python
@pytest.mark.parametrize("change_id", ["CHG-001", "CHG-002", "CHG-999999"])
def test_valid_change_ids_are_accepted(change_id: str) -> None:
    validate_change_id(change_id)  # must not raise
```

**Multiple Parameters:**
```python
@pytest.mark.parametrize(
    "change_id",
    [
        "CHG-1",      # comment explaining invalid case
        "CHG-01",
        "chg-001",
        # ...
    ],
)
def test_invalid_change_ids_are_rejected(change_id: str) -> None:
    with pytest.raises(InvalidChangeIdentifierError):
        validate_change_id(change_id)
```

**Section Organization:**
- Use section comments: `# --- change ID validation (T-040) -------------------------------------------------`
- Group related parametrized tests by section
- See `tests/unit/test_create_change.py` for examples

## Property-Based Testing

**Framework:** Hypothesis 6.165.0

**Basic Pattern:**
```python
from hypothesis import given
from hypothesis import strategies as st

@given(digits=st.integers(min_value=1, max_value=999999).map(str))
def test_property_any_chg_prefixed_id_with_three_or_more_digits_is_valid(digits: str) -> None:
    if len(digits) >= 3:
        validate_change_id(f"CHG-{digits}")  # must not raise
    else:
        with pytest.raises(InvalidChangeIdentifierError):
            validate_change_id(f"CHG-{digits}")
```

**Settings Control:**
```python
from hypothesis import settings

@given(phase=st.sampled_from(_PHASES), status=st.sampled_from(_STATUSES))
@settings(max_examples=len(_PHASES) * len(_STATUSES), deadline=None)
def test_transition_behavior_across_all_state_combinations(phase: str, status: str) -> None:
    # Test implementation
```

**Strategies Used:**
- `st.integers(min_value=N, max_value=N)` - integer ranges
- `.map(str)` - transform strategy results
- `st.sampled_from(collection)` - pick from fixed collection
- See `tests/property/test_transition_properties.py` for additional examples

**When to Use:**
- Format validation across all possible inputs
- State machine transitions across all valid combinations
- Invariant properties (e.g., "any rejection leaves file byte-identical")

## Mocking and Fixtures

**Pytest Fixtures (Built-In):**
- `tmp_path: Path` - temporary directory for file I/O testing
- `runner: CliRunner` - typer CLI testing (see acceptance tests)

**Module-Level Test Data:**
- Use `_VALID` pattern for shared test data (private by underscore convention)
- Prevents fixture coupling while allowing reuse

**State Modification Helpers:**
- Define helper functions (private with `_` prefix) for test-specific setup
- Example from `tests/property/test_transition_properties.py`:
  ```python
  def _set_source_state(state_path: Path, phase: str, status: str) -> None:
      """Overwrite a change's phase/status, keeping the file schema-valid."""
      # Implementation
  ```

**When NOT to Mock:**
- File system: use `tmp_path` fixture
- YAML/JSON parsing: use actual `load_yaml_file()` and validate result
- Domain logic: call functions directly rather than mocking

**What to Mock (If Needed):**
- External APIs (not present in this codebase)
- System calls (not present in this codebase)
- Note: This project avoids external dependencies (R-016 requirement)

## CLI Testing

**Framework:** `typer.testing.CliRunner`

**Pattern:**
```python
from typer.testing import CliRunner
from ggsad.cli import app

runner = CliRunner()

def test_e001_initialize_a_clean_repository(tmp_path: Path) -> None:
    """E-001: an empty writable target directory is initialized successfully."""
    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code == 0
    assert (tmp_path / ".ggsad" / "config.yaml").exists()
    assert "created:" in result.output
```

**Assertions:**
- `result.exit_code` - command exit code (0 = success)
- `result.output` - stdout/stderr combined
- File system side effects: check files exist/don't exist after command

**Testing Failures:**
```python
def test_e002_reject_unsafe_reinitialization(tmp_path: Path) -> None:
    """E-002: a target directory with existing modified file causes init to fail."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    modified_content = b"# My modified constitution\n\nDo not overwrite this.\n"
    (docs_dir / "constitution.md").write_bytes(modified_content)

    result = runner.invoke(app, ["init", str(tmp_path)])

    assert result.exit_code != 0
    assert "conflict" in result.output.lower()
    assert (docs_dir / "constitution.md").read_bytes() == modified_content
```

## Error Testing

**Testing Exceptions:**
```python
with pytest.raises(InvalidChangeIdentifierError):
    validate_change_id("invalid-id")
```

**Testing Error Messages (if needed):**
```python
with pytest.raises(InvalidChangeIdentifierError, match="must match 'CHG-'"):
    validate_change_id("invalid-id")
```

**Testing Multiple Conditions:**
- Create test data that triggers each error path
- Use parametrized tests for multiple error conditions
- See `test_invalid_change_ids_are_rejected()` in `tests/unit/test_create_change.py`

## Pydantic Model Testing

**Validation Testing:**
```python
def test_parses_valid_state_and_aliases_class_field() -> None:
    state = ChangeState.model_validate(_VALID)

    assert state.change.change_class == "M"
    assert state.flow.status == "draft"
    assert len(state.history) == 1
```

**Schema Flexibility Testing:**
```python
def test_gates_block_is_preserved_untyped_when_present() -> None:
    data = {**_VALID, "gates": {"current": {"definition": "DoD", "result": "pending"}}}

    state = ChangeState.model_validate(data)

    assert state.gates == {"current": {"definition": "DoD", "result": "pending"}}
```

## Integration Testing

**Scope:** Component-level testing verifying multiple modules work together

**Example from `tests/integration/test_standalone_operation.py`:**
- Full init → new → validate workflow
- Cross-module dependency verification
- File system I/O with validation

**Pattern:**
1. Set up initial state (create files, initialize project)
2. Execute workflow (run commands, call functions)
3. Verify outcomes (file existence, content, state changes)

**Cross-Cutting Concerns:**
- Import hygiene (verifying no forbidden SDK imports)
- Dependency declarations (checking pyproject.toml)
- Stand-alone operation (no external integrations)

## Acceptance Testing

**Scope:** End-to-end CLI testing against specification requirements

**Test Naming Convention:**
- Pattern: `test_eNNN_[description]()` where E-NNN is specification exemplar ID
- Example: `test_e001_initialize_a_clean_repository()`
- Example: `test_e002_reject_unsafe_reinitialization()`

**Docstring Pattern:**
```python
def test_e001_initialize_a_clean_repository(tmp_path: Path) -> None:
    """E-001: an empty writable target directory is initialized successfully,
    and the approved GG-SAD directories and baseline files are created."""
```

**Assertions:**
- Exit codes: `assert result.exit_code == 0` for success
- Output content: `assert "created:" in result.output`
- File system state: `assert (tmp_path / "file").exists()`
- Data integrity: `assert (docs_dir / "file").read_bytes() == original_content`

## Coverage Configuration

**Config Location:** `pyproject.toml` [tool.coverage.run] and [tool.coverage.report]

**Coverage Settings:**
- Branch coverage: enabled
- Source: `ggsad` package only
- Minimum: 85% fail_under

**Excluded from Coverage:**
```python
"if TYPE_CHECKING:"          # Type-checking-only imports
"if __name__ == .__main__.:" # Script entry points
"raise NotImplementedError"  # Stub implementations
```

**View Coverage Report:**
```bash
pytest --cov=ggsad --cov-report=html
# Opens htmlcov/index.html in browser
```

**Coverage Gaps:**
- Check `pytest --cov-report=term-missing` output
- Each function should have at least one happy-path test
- Complex logic should have both success and failure paths

## Testing Anti-Patterns to Avoid

**❌ Don't:**
- Use global test fixtures (no conftest.py at root)
- Mock functions from the same module (test actual behavior)
- Skip error handling tests (test rejection paths, not just success)
- Leave `print()` statements (use `assert` or `typer.echo()` in actual code)
- Test implementation details (test behavior and outcomes, not internal state)

**✓ Do:**
- Keep test data at module level (`_VALID` pattern)
- Test both success and failure paths
- Name tests descriptively with specification references
- Use parametrized tests for multiple similar cases
- Return `-> None` on test functions
- Include type hints on all test parameters

---

*Testing analysis: 2026-08-18*
