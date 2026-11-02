"""The content hash of files, parsed definitions, and sets of files (Section 25.2).

An approval binds the content hash of what it approves. Text files are hashed after their line
endings are normalized; binary files byte for byte; a YAML definition by its parsed value, so
comments, layout, and key order have no effect.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from ruamel.yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode

from ggsad.core.canonical import DomainError, hash_bytes, hash_value

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

_TAG: Final = "tag:yaml.org,2002:"
# Tags that the YAML 1.2 core schema does not know. A plain scalar that ruamel resolves to one of
# them is an ordinary string under the core schema.
_STRING_LIKE: Final = frozenset({_TAG + "str", _TAG + "timestamp", _TAG + "merge", _TAG + "value"})


def normalize_line_endings(data: bytes) -> bytes:
    """Replace every CR LF, and every CR that is not followed by LF, with LF."""
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def is_text(data: bytes) -> bool:
    """A file is text exactly when its bytes are valid UTF-8 and hold no zero byte."""
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def file_content_hash(data: bytes) -> str:
    """The content hash of the bytes of a file."""
    return hash_bytes(normalize_line_endings(data) if is_text(data) else data)


def path_content_hash(path: Path) -> str:
    """The content hash of a file on disk."""
    return file_content_hash(path.read_bytes())


def files_content_hash(hashes: Mapping[str, str]) -> str:
    """The content hash of a set of files: the hash of the object from path to content hash."""
    return hash_value(dict(hashes))


def gate_binding_hash(definitions_hash: str, gate: str) -> str:
    """The content hash of the gate definitions together with a gate identifier (Section 24.3)."""
    return hash_value({"definitions": definitions_hash, "gate": gate})


def yaml_value(text: str) -> object:
    """Read YAML 1.2 with its core schema into the domain of Section 25.1.

    Raises DomainError for a value outside the domain: a float, a key that is not a string, a
    repeated key, or a scalar of a type that the domain does not hold.
    """
    try:
        node = YAML(typ="safe").compose(text)
    except YAMLError as error:
        raise DomainError("", f"not valid YAML: {error}") from error
    if node is None:
        return None
    return _convert(node, "", set())


def yaml_content_hash(text: str) -> str:
    """The content hash of a parsed YAML definition (Section 25.2)."""
    return hash_value(yaml_value(text))


def _convert(node: Node, path: str, active: set[int]) -> object:
    if id(node) in active:
        raise DomainError(path, "an alias must not refer to a node that contains it")
    if isinstance(node, ScalarNode):
        return _scalar(node, path)
    active = active | {id(node)}
    if isinstance(node, SequenceNode):
        return [_convert(item, f"{path}[{i}]", active) for i, item in enumerate(node.value)]
    if isinstance(node, MappingNode):
        return _mapping(node, path, active)
    raise DomainError(path, "unsupported YAML node")


def _mapping(node: MappingNode, path: str, active: set[int]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key_node, value_node in node.value:
        key = _convert(key_node, path, active)
        if not isinstance(key, str):
            raise DomainError(path, "a mapping key must be a string")
        if key in result:
            raise DomainError(path, f"the mapping repeats the key {key!r}")
        result[key] = _convert(value_node, f"{path}.{key}", active)
    return result


def _scalar(node: ScalarNode, path: str) -> object:
    tag = node.tag
    text = str(node.value)
    if tag in _STRING_LIKE:
        return text
    if tag == _TAG + "null":
        return None
    if tag == _TAG + "bool":
        return text.lower() == "true"
    if tag == _TAG + "int":
        return _integer(text, path)
    if tag == _TAG + "float":
        raise DomainError(path, "a floating-point number is not in the domain")
    raise DomainError(path, f"a scalar of the type {tag!r} is not in the domain")


def _integer(text: str, path: str) -> int:
    sign = -1 if text.startswith("-") else 1
    body = text.lstrip("+-").lower()
    try:
        if body.startswith("0x"):
            return sign * int(body[2:], 16)
        if body.startswith("0o"):
            return sign * int(body[2:], 8)
        return sign * int(body, 10)
    except ValueError as error:
        raise DomainError(path, f"{text!r} is not an integer") from error
