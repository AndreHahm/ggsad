"""Shared conservative-idempotent manifest writer (R-002, R-012).

Both `ggsad init` (Slice 3) and `ggsad new` (Slice 4) follow the same
all-or-nothing shape: preflight every path in a manifest before writing
anything, and only write if no conflicts were found. That logic lives here
once rather than being duplicated per command.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PreflightResult:
    """Classification of every manifest path against the current filesystem."""

    to_create: tuple[Path, ...]
    unchanged: tuple[Path, ...]
    conflicts: tuple[Path, ...]

    @property
    def has_conflicts(self) -> bool:
        return bool(self.conflicts)


def preflight(manifest: dict[Path, bytes]) -> PreflightResult:
    """Classify each manifest path without writing anything."""
    to_create: list[Path] = []
    unchanged: list[Path] = []
    conflicts: list[Path] = []

    for path, content in manifest.items():
        if not path.exists():
            to_create.append(path)
        elif path.read_bytes() == content:
            unchanged.append(path)
        else:
            conflicts.append(path)

    return PreflightResult(
        to_create=tuple(to_create),
        unchanged=tuple(unchanged),
        conflicts=tuple(conflicts),
    )


@dataclass(frozen=True, slots=True)
class WriteResult:
    """Outcome of a `write_manifest` call."""

    created: tuple[Path, ...]
    unchanged: tuple[Path, ...]
    conflicts: tuple[Path, ...]

    @property
    def ok(self) -> bool:
        return not self.conflicts


def write_manifest(manifest: dict[Path, bytes]) -> WriteResult:
    """Preflight `manifest` and write it if -- and only if -- there are no conflicts."""
    plan = preflight(manifest)

    if plan.has_conflicts:
        return WriteResult(created=(), unchanged=plan.unchanged, conflicts=plan.conflicts)

    for path in plan.to_create:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(manifest[path])

    return WriteResult(created=plan.to_create, unchanged=plan.unchanged, conflicts=())
