"""The `init` operation: set up a stand-alone GG-SAD project (Implementation Contract, 22.1).

`init` takes the compliance profile once. It creates the configuration, the brief, the documents
that the profile requires, the templates, and one example change. It never overwrites a file: a
file that exists is kept and listed as skipped. It reports a difference between the profile of the
configuration and the profile of the brief and then writes nothing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ggsad.core.issues import Issue
from ggsad.core.new_change import NewFields, definition_text, spec_text
from ggsad.core.operations import Envelope, failure
from ggsad.core.project import (
    ARCHITECTURE_PATH,
    BRIEF_PATH,
    CONFIG_PATH,
    CONSTITUTION_PATH,
    REQUIRED_DOCUMENTS,
    ROADMAP_PATH,
    brief_profile,
    read_yaml_file,
)
from ggsad.core.settings import PROFILES, TEAM_MODES
from ggsad.core.templates import (
    ARCHITECTURE_TEMPLATE,
    BRIEF_TEMPLATE,
    CONSTITUTION_TEMPLATE,
    EXAMPLE_DONE_WHEN,
    EXAMPLE_PROBLEM,
    REVIEW_TEMPLATE,
    ROADMAP_TEMPLATE,
    SPEC_TEMPLATE,
    config_text,
)
from ggsad.core.values import as_mapping

if TYPE_CHECKING:
    from pathlib import Path

TEMPLATES_DIRECTORY = ".ggsad/templates"
EXAMPLE_ID = "example"
DOCUMENT_TEXT = {
    BRIEF_PATH: BRIEF_TEMPLATE,
    CONSTITUTION_PATH: CONSTITUTION_TEMPLATE,
    ARCHITECTURE_PATH: ARCHITECTURE_TEMPLATE,
    ROADMAP_PATH: ROADMAP_TEMPLATE,
}


@dataclass(frozen=True)
class InitOptions:
    """What `init` needs to know once."""

    profile: str
    project_id: str
    owner: str
    requestors: tuple[str, ...] = ("agent:assistant",)
    team_mode: str = "team"


def _option_issues(options: InitOptions) -> list[Issue]:
    found: list[Issue] = []
    if options.profile not in PROFILES:
        found.append(Issue("profile-invalid", f"the profile is one of {', '.join(PROFILES)}"))
    if options.team_mode not in TEAM_MODES:
        found.append(Issue("team-mode-invalid", f"team_mode is one of {', '.join(TEAM_MODES)}"))
    if not options.project_id.strip():
        found.append(Issue("project-id-missing", "the project needs an identifier"))
    return found + _identity_issues(options)


def _identity_issues(options: InitOptions) -> list[Issue]:
    found: list[Issue] = []
    if not options.owner.startswith("human:") or options.owner == "human:":
        found.append(Issue("owner-invalid", "the Owner is written human:<name>"))
    found.extend(
        Issue("requestor-invalid", f"{name!r} is not written agent:<name>")
        for name in options.requestors
        if not name.startswith("agent:") or name == "agent:"
    )
    return found


def _existing_config_profile(root: Path) -> str | None:
    value, _ = read_yaml_file(root / CONFIG_PATH, "config")
    root_map = as_mapping(value) or {}
    profile = (as_mapping(root_map.get("project")) or {}).get("compliance_profile")
    return profile if isinstance(profile, str) else None


def _profile_issues(root: Path, options: InitOptions) -> list[Issue]:
    """A difference between the requested profile, the configuration, and the brief."""
    config, brief = _existing_config_profile(root), brief_profile(root)
    stated = {name: value for name, value in (("configuration", config), ("brief", brief)) if value}
    stated["request"] = options.profile
    if len(set(stated.values())) <= 1:
        return []
    text = ", ".join(f"the {name} says {value!r}" for name, value in stated.items())
    return [Issue("profile-mismatch", f"the profiles differ: {text}")]


def _document_text(path: str, profile: str, team_mode: str) -> str:
    text = DOCUMENT_TEXT[path]
    return text.format(profile=profile, team_mode=team_mode) if path == BRIEF_PATH else text


def _planned(options: InitOptions) -> dict[str, str]:
    """Every file `init` would create, by path."""
    owner, profile, mode = options.owner, options.profile, options.team_mode
    config = config_text(options.project_id, profile, mode, owner, options.requestors)
    files = {CONFIG_PATH: config}
    for path in REQUIRED_DOCUMENTS[profile]:
        files[path] = _document_text(path, profile, mode)
    for path in DOCUMENT_TEXT:
        name = path.rsplit("/", 1)[-1]
        files[f"{TEMPLATES_DIRECTORY}/{name}"] = _document_text(path, "<profile>", "<mode>")
    blank = NewFields("<problem>", ("<done-when sentence>",), owner, owner)
    files[f"{TEMPLATES_DIRECTORY}/change.yaml"] = definition_text("<change-id>", profile, blank)
    files[f"{TEMPLATES_DIRECTORY}/spec.md"] = SPEC_TEMPLATE
    files[f"{TEMPLATES_DIRECTORY}/review.md"] = REVIEW_TEMPLATE
    example = NewFields(EXAMPLE_PROBLEM, EXAMPLE_DONE_WHEN, owner, owner)
    files[f"specs/{EXAMPLE_ID}/change.yaml"] = definition_text(EXAMPLE_ID, profile, example)
    files[f"specs/{EXAMPLE_ID}/spec.md"] = spec_text(EXAMPLE_ID, example)
    return files


def _create(root: Path, files: dict[str, str]) -> tuple[list[str], list[str]]:
    """Write each missing file. Raises OSError after removing what this call created."""
    created: list[Path] = []
    skipped: list[str] = []
    try:
        for name, text in files.items():
            path = root / name
            if path.exists():
                skipped.append(name)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
            created.append(path)
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    return [p.relative_to(root).as_posix() for p in created], skipped


def init_project(root: Path, options: InitOptions) -> Envelope:
    """Set up the project in `root`. Nothing is written when the options or the profiles clash."""
    issues = _option_issues(options)
    if issues:
        return failure("init", tuple(issues))
    clash = _profile_issues(root, options)
    if clash:
        return failure("init", tuple(clash))
    try:
        created, skipped = _create(root, _planned(options))
    except OSError as error:
        return failure(
            "init", (Issue("state-write-failed", f"the files cannot be written: {error}"),)
        )
    data = {"created": created, "skipped": skipped, "profile": options.profile}
    return Envelope("init", "success", bool(created), data=data)
