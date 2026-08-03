"""Packaged GG-SAD method assets: schemas, templates, and mappings.

These are self-contained copies bundled with the ``ggsad`` package so that
``ggsad init`` can materialize a new project without depending on this
repository's own top-level ``.ggsad/`` directory.
"""

from __future__ import annotations

from importlib import resources
from importlib.resources.abc import Traversable


def resource_root() -> Traversable:
    """Return the traversable root of the packaged resources directory."""
    return resources.files(__package__)
