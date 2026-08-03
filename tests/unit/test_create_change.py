"""Unit tests for Class M change creation (R-003, R-004, R-008, R-012)."""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ggsad.application.create_change import (
    ChangeAlreadyExistsError,
    InvalidChangeIdentifierError,
    build_change_manifest,
    resolve_change_directory,
    validate_change_id,
    validate_slug,
)
from ggsad.models.state import ChangeState
from ggsad.validators.schema_validator import load_schema, validate_against_schema
from ggsad.validators.yaml_loader import load_yaml_text

REPO_ROOT = Path(__file__).resolve().parents[2]


# --- change ID validation (T-040) -------------------------------------------------


@pytest.mark.parametrize("change_id", ["CHG-001", "CHG-002", "CHG-999999"])
def test_valid_change_ids_are_accepted(change_id: str) -> None:
    validate_change_id(change_id)  # must not raise


@pytest.mark.parametrize(
    "change_id",
    [
        "CHG-1",  # fewer than 3 digits
        "CHG-01",  # fewer than 3 digits
        "chg-001",  # wrong case
        "CHG001",  # missing hyphen
        "CHG-abc",  # non-digit suffix
        "change/../../002",  # E-004: path-traversal attempt
        "",
        "CHG-001/../escape",
    ],
)
def test_invalid_change_ids_are_rejected(change_id: str) -> None:
    with pytest.raises(InvalidChangeIdentifierError):
        validate_change_id(change_id)


@given(digits=st.integers(min_value=1, max_value=999999).map(str))
def test_property_any_chg_prefixed_id_with_three_or_more_digits_is_valid(digits: str) -> None:
    if len(digits) >= 3:
        validate_change_id(f"CHG-{digits}")  # must not raise
    else:
        with pytest.raises(InvalidChangeIdentifierError):
            validate_change_id(f"CHG-{digits}")


# --- slug validation (T-041) -------------------------------------------------------


@pytest.mark.parametrize("slug", ["example-change", "a", "a1-b2-c3", "example"])
def test_valid_slugs_are_accepted(slug: str) -> None:
    validate_slug(slug)  # must not raise


@pytest.mark.parametrize(
    "slug",
    [
        "Example-Change",  # uppercase
        "example_change",  # underscore
        "example--change",  # double hyphen
        "-example",  # leading hyphen
        "example-",  # trailing hyphen
        "../../etc/passwd",  # traversal attempt
        "",
    ],
)
def test_invalid_slugs_are_rejected(slug: str) -> None:
    with pytest.raises(InvalidChangeIdentifierError):
        validate_slug(slug)


# --- path containment (T-041) ------------------------------------------------------


def test_resolve_change_directory_stays_under_specs(tmp_path: Path) -> None:
    change_dir = resolve_change_directory(tmp_path, "CHG-002", "example-change")

    assert change_dir == (tmp_path / "specs" / "CHG-002-example-change").resolve()
    assert change_dir.parent == (tmp_path / "specs").resolve()


# --- manifest building (T-042) ------------------------------------------------------


def test_manifest_contains_five_required_artifacts(tmp_path: Path) -> None:
    manifest = build_change_manifest(
        tmp_path, change_id="CHG-002", slug="example-change", title="Example Change"
    )

    change_dir = tmp_path / "specs" / "CHG-002-example-change"
    expected = {
        change_dir / "state.yaml",
        change_dir / "spec.md",
        change_dir / "plan.md",
        change_dir / "tasks.md",
        change_dir / "evidence.md",
    }

    assert set(manifest) == expected


def test_generated_state_yaml_is_schema_valid_and_identifies_the_change(tmp_path: Path) -> None:
    manifest = build_change_manifest(
        tmp_path, change_id="CHG-002", slug="example-change", title="Example Change"
    )
    change_dir = tmp_path / "specs" / "CHG-002-example-change"
    content = manifest[change_dir / "state.yaml"].decode("utf-8")

    data = load_yaml_text(content)
    schema = load_schema(REPO_ROOT / ".ggsad" / "schemas" / "state.schema.json")
    assert validate_against_schema(data=data, schema=schema, file_label="state.yaml") == []

    state = ChangeState.model_validate(data)
    assert state.change.id == "CHG-002"
    assert state.change.slug == "example-change"
    assert state.change.change_class == "M"
    assert state.flow.phase == "specify"
    assert state.flow.status == "draft"
    assert len(state.history) == 1
    assert state.history[0].event == "change-created"


def test_unsupported_change_class_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(InvalidChangeIdentifierError, match="Class M"):
        build_change_manifest(
            tmp_path,
            change_id="CHG-002",
            slug="example-change",
            title="Example",
            change_class="L",
        )


def test_build_change_manifest_rejects_invalid_id_before_touching_filesystem(
    tmp_path: Path,
) -> None:
    with pytest.raises(InvalidChangeIdentifierError):
        build_change_manifest(
            tmp_path, change_id="change/../../002", slug="example", title="Example"
        )

    assert not (tmp_path / "specs").exists()


def test_build_change_manifest_rejects_existing_change_directory(tmp_path: Path) -> None:
    change_dir = tmp_path / "specs" / "CHG-002-example-change"
    change_dir.mkdir(parents=True)

    with pytest.raises(ChangeAlreadyExistsError, match="already exists"):
        build_change_manifest(tmp_path, change_id="CHG-002", slug="example-change", title="Example")
