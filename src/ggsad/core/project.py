"""Reading the project from disk: settings, higher documents, and the checks on them.

Everything here reads and never writes. A file that is missing or bad becomes an `Issue`; nothing
raises for the content of a file (Sections 4.2, 5.1, 24.1, and 25.3).

Interpretations fixed here (listed in the pull request):
- the higher documents of the fingerprint are the constitution, every ADR, the project brief, and
  the architecture document; a missing one is left out of the fingerprint;
- the identity of the gate definitions is the content hash of the object that holds `gates`,
  `scope`, `required_tools`, `agent_may_close`, and the evidence commands of the requirements;
- the brief states its profile in a line `Compliance profile: <name>`.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

from ggsad.core.canonical import DomainError, hash_value
from ggsad.core.content_hash import path_content_hash, yaml_value
from ggsad.core.issues import Issue
from ggsad.core.settings import Settings, read_settings
from ggsad.core.values import as_list, as_mapping

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

CONFIG_PATH: Final = ".ggsad/config.yaml"
BRIEF_PATH: Final = "docs/project-brief.md"
CONSTITUTION_PATH: Final = "docs/constitution.md"
ARCHITECTURE_PATH: Final = "docs/architecture.md"
ROADMAP_PATH: Final = "docs/roadmap.md"
ADR_DIRECTORY: Final = "docs/adr"
HIGHER_DOCUMENTS: Final = (CONSTITUTION_PATH, BRIEF_PATH, ARCHITECTURE_PATH)
REQUIRED_DOCUMENTS: Final = {
    "lean": (BRIEF_PATH, CONSTITUTION_PATH),
    "standard": (BRIEF_PATH, CONSTITUTION_PATH, ARCHITECTURE_PATH, ROADMAP_PATH),
    "governed": (BRIEF_PATH, CONSTITUTION_PATH, ARCHITECTURE_PATH, ROADMAP_PATH),
    "regulated": (BRIEF_PATH, CONSTITUTION_PATH, ARCHITECTURE_PATH, ROADMAP_PATH),
}
FROZEN_FIELDS: Final = ("gates", "scope", "required_tools", "agent_may_close")
CONFLICT_LINE: Final = re.compile(r"^Conflicts with higher documents: \S.*$", re.MULTILINE)
PROFILE_LINE: Final = re.compile(r"^Compliance profile:[ \t]*(\S+)[ \t]*$", re.MULTILINE)


def read_yaml_file(path: Path, label: str) -> tuple[object | None, Issue | None]:
    """The parsed value of a YAML file, or an issue that says why it cannot be used."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, Issue(f"{label}-missing", f"{label} does not exist: {path.name}")
    except (OSError, UnicodeDecodeError) as error:
        return None, Issue(f"{label}-unreadable", f"{label} cannot be read: {error}")
    try:
        return yaml_value(text), None
    except DomainError as error:
        return None, Issue(f"{label}-invalid", f"{label} is not valid: {error}")


def load_settings(root: Path) -> tuple[Settings | None, tuple[Issue, ...]]:
    """The settings of the project, or the issues that stop every operation."""
    value, issue = read_yaml_file(root / CONFIG_PATH, "config")
    if issue is not None:
        return None, (issue,)
    settings, report = read_settings(value)
    return settings, report.issues


def definitions_hash(definition: Mapping[str, object]) -> str | None:
    """The identity of the frozen gate definitions, None when there are no gates (Section 24.1)."""
    if "gates" not in definition:
        return None
    frozen = {name: definition[name] for name in FROZEN_FIELDS if name in definition}
    frozen["evidence"] = _evidence_commands(definition.get("requirements"))
    return hash_value(frozen)


def _evidence_commands(requirements: object) -> dict[str, object]:
    found: dict[str, object] = {}
    for item in as_list(requirements) or []:
        requirement = as_mapping(item) or {}
        identifier = requirement.get("id")
        if isinstance(identifier, str):
            found[identifier] = requirement.get("evidence")
    return found


def document_fingerprint(root: Path) -> dict[str, str]:
    """The content hash of every higher document that exists, by path (Section 4.1)."""
    paths = [p for p in HIGHER_DOCUMENTS if (root / p).is_file()]
    adr = root / ADR_DIRECTORY
    if adr.is_dir():
        paths.extend(
            f"{ADR_DIRECTORY}/{item.name}" for item in sorted(adr.glob("*.md")) if item.is_file()
        )
    return {path: path_content_hash(root / path) for path in paths}


def missing_documents(root: Path, profile: str) -> list[str]:
    """The documents that the profile requires and the project does not have (Section 4.2)."""
    return [p for p in REQUIRED_DOCUMENTS.get(profile, ()) if not (root / p).is_file()]


def conflict_line_issues(spec_text: str | None) -> list[tuple[str, str]]:
    """Why `spec.md` cannot be approved: it must carry the conflict line (Section 4.1)."""
    if spec_text is None:
        return [("spec-missing", "spec.md does not exist")]
    if CONFLICT_LINE.search(spec_text) is None:
        message = "spec.md has no line 'Conflicts with higher documents: none' or a list"
        return [("conflict-line-missing", message)]
    return []


def brief_profile(root: Path) -> str | None:
    """The compliance profile that the project brief states, None when it states none."""
    try:
        text = (root / BRIEF_PATH).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    found = PROFILE_LINE.search(text)
    return found.group(1) if found else None


def profile_issue(root: Path, settings: Settings) -> Issue | None:
    """An issue when the brief and the configuration name different profiles (Section 5.1)."""
    stated = brief_profile(root)
    if stated is None or stated == settings.compliance_profile:
        return None
    message = (
        f"the configuration says {settings.compliance_profile!r} and the project brief says "
        f"{stated!r}"
    )
    return Issue("profile-mismatch", message)
