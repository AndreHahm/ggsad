"""Safe YAML loading and dumping for governed GG-SAD artifacts.

Uses a safe-only loader (no arbitrary Python object construction, per
ADR-0003) and wraps parse failures with file-scoped, actionable context
(R-015). A missing file raises the standard `FileNotFoundError` rather than
being wrapped here -- artifact existence is a repository/document-level
concern (R-008), not a YAML-parsing concern.
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

_yaml = YAML(typ="safe")
_yaml.default_flow_style = False


class YamlLoadError(Exception):
    """Raised when a governed YAML file exists but is not safely parseable."""

    def __init__(
        self,
        path: Path,
        message: str,
        line: int | None = None,
        column: int | None = None,
    ) -> None:
        self.path = path
        self.message = message
        self.line = line
        self.column = column
        location = f" at line {line}, column {column}" if line is not None else ""
        super().__init__(f"{path}: invalid YAML{location}: {message}")


def load_yaml_text(text: str, *, source: Path | str = "<string>") -> Any:  # noqa: ANN401
    """Safely parse YAML from an in-memory string.

    Raises:
        YamlLoadError: if `text` is not valid, safely-parseable YAML.
    """
    try:
        return _yaml.load(text)
    except YAMLError as exc:
        problem_mark = getattr(exc, "problem_mark", None)
        line = problem_mark.line + 1 if problem_mark is not None else None
        column = problem_mark.column + 1 if problem_mark is not None else None
        raise YamlLoadError(path=Path(source), message=str(exc), line=line, column=column) from exc


def load_yaml_file(path: Path) -> Any:  # noqa: ANN401
    """Safely load and parse a YAML file.

    Raises:
        FileNotFoundError: if `path` does not exist.
        YamlLoadError: if the file exists but is not valid, safely-parseable YAML.
    """
    text = path.read_text(encoding="utf-8")
    return load_yaml_text(text, source=path)


def dump_yaml_bytes(data: Any) -> bytes:  # noqa: ANN401 -- dumping arbitrary already-validated data
    """Serialize `data` to UTF-8 YAML bytes, block-style, via the safe dumper."""
    buffer = StringIO()
    _yaml.dump(data, buffer)
    return buffer.getvalue().encode("utf-8")
