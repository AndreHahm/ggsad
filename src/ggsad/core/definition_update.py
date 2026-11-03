"""Updating one field of `change.yaml` in place (the `handover` action, Section 23.4).

The file is read and written with a round-trip parser, so comments and the layout stay. The write
goes to a temporary file that replaces the definition in one step. The owner is not part of the
frozen gate definitions (Section 24.1), so this edit never makes the gates look changed.
"""

from __future__ import annotations

import io
from collections.abc import MutableMapping
from typing import TYPE_CHECKING

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

if TYPE_CHECKING:
    from pathlib import Path


class DefinitionUpdateError(Exception):
    """The definition could not be updated."""


def set_owner(path: Path, owner: str) -> None:
    """Set the field `owner` of the change definition. Raises DefinitionUpdateError."""
    yaml = YAML(typ="rt")
    yaml.preserve_quotes = True
    try:
        data = yaml.load(path.read_text(encoding="utf-8"))
        if not isinstance(data, MutableMapping):
            raise DefinitionUpdateError(f"{path.name} is not a mapping")  # noqa: TRY003
        data["owner"] = DoubleQuotedScalarString(owner)
        buffer = io.StringIO()
        yaml.dump(data, buffer)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(buffer.getvalue(), encoding="utf-8", newline="\n")
        temporary.replace(path)
    except (OSError, UnicodeDecodeError, YAMLError) as error:
        raise DefinitionUpdateError(str(error)) from error
