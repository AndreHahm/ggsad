"""Atomic `state.yaml` replacement (R-012, R-013, plan.md Sec 9).

Strategy, exactly as plan.md Sec 9 specifies:

1. serialize the new state to a temporary file in the *same directory*
   (so the final replace stays on one filesystem);
2. flush and fsync it;
3. re-validate the temporary file's content against the schema before it
   becomes the real file -- a bug in the caller's state construction must
   never corrupt the governed file it's about to replace;
4. `os.replace` it onto the target path (atomic on both POSIX and Windows
   within the same directory/filesystem);
5. clean up the temporary file on any failure.

No write to the real path happens until every check above has passed.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from ggsad.models.validation import ValidationIssue
from ggsad.validators.schema_validator import load_schema, validate_against_schema
from ggsad.validators.yaml_loader import load_yaml_file


class StateWriteError(Exception):
    """Raised when a constructed state fails re-validation before replacement.

    Not expected to trigger in normal operation -- it's the last line of
    defense against a bug in the caller's state construction reaching the
    governed file.
    """


def _raise_on_revalidation_failure(issues: list[ValidationIssue], tmp_path: Path) -> None:
    if issues:
        reasons = "; ".join(issue.reason for issue in issues)
        msg = f"Serialized state at {tmp_path} failed re-validation: {reasons}"
        raise StateWriteError(msg)


def atomic_replace_state(state_path: Path, new_content: bytes, schema_path: Path) -> None:
    """Atomically replace `state_path` with `new_content`, after re-validating it."""
    fd, tmp_name = tempfile.mkstemp(dir=state_path.parent, prefix=".state.", suffix=".tmp")
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(new_content)
            handle.flush()
            os.fsync(handle.fileno())

        data = load_yaml_file(tmp_path)
        schema = load_schema(schema_path)
        issues = validate_against_schema(data=data, schema=schema, file_label=str(tmp_path))
        _raise_on_revalidation_failure(issues, tmp_path)

        tmp_path.replace(state_path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
