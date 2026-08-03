"""Unit tests for the safe YAML loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from ggsad.validators.yaml_loader import YamlLoadError, load_yaml_file, load_yaml_text


def test_load_yaml_text_parses_valid_yaml() -> None:
    data = load_yaml_text("a: 1\nb:\n  - x\n  - y\n")

    assert data == {"a": 1, "b": ["x", "y"]}


def test_load_yaml_text_rejects_malformed_yaml() -> None:
    with pytest.raises(YamlLoadError) as excinfo:
        load_yaml_text("a: [1, 2\nb: 3\n")

    assert excinfo.value.line is not None


def test_load_yaml_text_rejects_unsafe_python_object_tag() -> None:
    unsafe = "value: !!python/object/apply:builtins.print ['unsafe']\n"

    with pytest.raises(YamlLoadError):
        load_yaml_text(unsafe)


def test_load_yaml_file_reads_and_parses(tmp_path: Path) -> None:
    target = tmp_path / "config.yaml"
    target.write_text("key: value\n", encoding="utf-8")

    data = load_yaml_file(target)

    assert data == {"key": "value"}


def test_load_yaml_file_error_includes_path(tmp_path: Path) -> None:
    target = tmp_path / "broken.yaml"
    target.write_text("a: [1, 2\n", encoding="utf-8")

    with pytest.raises(YamlLoadError) as excinfo:
        load_yaml_file(target)

    assert excinfo.value.path == target
    assert str(target) in str(excinfo.value)


def test_load_yaml_file_missing_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_yaml_file(tmp_path / "does-not-exist.yaml")
