"""GG-SAD reference CLI entry point."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from ggsad import __version__
from ggsad.application.create_change import (
    SUPPORTED_CHANGE_CLASS,
    ChangeCreationError,
    build_change_manifest,
)
from ggsad.application.initialize_project import initialize_project
from ggsad.application.manifest_writer import WriteResult, write_manifest
from ggsad.application.validate_repository import validate_repository
from ggsad.engine.state_writer import StateWriteError
from ggsad.engine.transitions import SUPPORTED_TARGET_STATUS, perform_transition

app = typer.Typer(
    name="ggsad",
    help="Goal-Gated Spec-Anchored Development (GG-SAD) reference CLI.",
    no_args_is_help=False,
)


@app.callback(invoke_without_command=True)
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the ggsad version and exit.",
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Goal-Gated Spec-Anchored Development (GG-SAD) reference CLI."""
    if version:
        typer.echo(f"ggsad {__version__}")
        raise typer.Exit


def _echo_manifest_result(result: WriteResult, *, operation: str) -> None:
    """Echo a WriteResult's created/unchanged/conflict paths consistently.

    Shared by `init` and `new`: both write a manifest with the same
    conservative-idempotent contract (R-002, R-012), so they report it the
    same way rather than drifting into two slightly different formats.
    """
    if result.conflicts:
        typer.echo(f"{operation} failed: existing files conflict with generated content.")
        typer.echo("No files were written.")
        for path in result.conflicts:
            typer.echo(f"  conflict: {path}")
        for path in result.unchanged:
            typer.echo(f"  unchanged: {path}")
        return

    for path in result.created:
        typer.echo(f"created: {path}")
    for path in result.unchanged:
        typer.echo(f"unchanged: {path}")


@app.command("init")
def init_command(
    target: Annotated[
        Path,
        typer.Argument(help="Directory to initialize (created if it does not exist)."),
    ] = Path(),
) -> None:
    """Initialize a GG-SAD project structure in TARGET (default: current directory)."""
    result = initialize_project(target)
    _echo_manifest_result(result, operation="Initialization")

    if not result.ok:
        raise typer.Exit(code=1)

    typer.echo(f"GG-SAD project initialized at {target.resolve()}")


@app.command("new")
def new_command(
    change_id: Annotated[str, typer.Argument(help="Change ID, e.g. CHG-002.")],
    slug: Annotated[str, typer.Argument(help="Lowercase, hyphenated slug, e.g. example-change.")],
    change_class: Annotated[
        str,
        typer.Option("--class", help="Change class. CHG-001 only implements Class M."),
    ] = SUPPORTED_CHANGE_CLASS,
    title: Annotated[
        str | None,
        typer.Option("--title", help="Change title (defaults to a humanized slug)."),
    ] = None,
    target: Annotated[
        Path,
        typer.Option("--target", help="Project root containing (or to contain) specs/."),
    ] = Path(),
) -> None:
    """Create a new Class M change under TARGET/specs/CHANGE_ID-SLUG/.

    Unlike `init`, a second run against the same CHANGE_ID is expected to
    conflict rather than report "unchanged": `state.yaml` records a fresh
    creation timestamp on every render, and a change's `state.yaml` is
    expected to evolve after creation (transitions, approvals) -- silently
    treating a re-run as a no-op could clobber that progress.
    """
    resolved_title = title or slug.replace("-", " ").title()

    try:
        manifest = build_change_manifest(
            target,
            change_id=change_id,
            slug=slug,
            title=resolved_title,
            change_class=change_class,
        )
    except ChangeCreationError as exc:
        typer.echo(f"Change creation rejected: {exc}")
        raise typer.Exit(code=1) from exc

    result = write_manifest(manifest)
    _echo_manifest_result(result, operation="Change creation")

    if not result.ok:
        raise typer.Exit(code=1)

    typer.echo(f"Class {change_class} change {change_id} created at specs/{change_id}-{slug}/")


@app.command("validate")
def validate_command(
    target: Annotated[Path, typer.Argument(help="Project root to validate.")] = Path(),
    change: Annotated[
        str | None,
        typer.Option("--change", help="Validate only this change ID (e.g. CHG-002)."),
    ] = None,
    output_format: Annotated[
        str,
        typer.Option("--format", help="Output format: 'text' or 'json'."),
    ] = "text",
) -> None:
    """Validate governed GG-SAD artifacts under TARGET.

    Always checks `.ggsad/config.yaml` and its declared mappings. With no
    `--change`, also validates every change directory found under `specs/`
    (never `specs/examples/`, which is never active project state).
    """
    if output_format not in ("text", "json"):
        typer.echo(f"Invalid --format {output_format!r}: must be 'text' or 'json'.")
        raise typer.Exit(code=1)

    issues = validate_repository(target, change_id=change)

    if output_format == "json":
        typer.echo(json.dumps([issue.model_dump(mode="json") for issue in issues], indent=2))
    else:
        for issue in issues:
            typer.echo(str(issue))
        if issues:
            typer.echo(f"{len(issues)} validation issue(s) found.")
        else:
            typer.echo(f"OK: no validation issues found under {target.resolve()}")

    if issues:
        raise typer.Exit(code=1)


@app.command("transition")
def transition_command(
    change_id: Annotated[str, typer.Argument(help="Change ID to transition, e.g. CHG-002.")],
    target_status: Annotated[
        str, typer.Argument(help="Target status. CHG-001 only supports 'ready'.")
    ],
    actor: Annotated[
        str, typer.Option("--actor", help="Participant performing the transition.")
    ] = "cli-user",
    target: Annotated[
        Path, typer.Option("--target", help="Project root containing specs/.")
    ] = Path(),
) -> None:
    """Transition CHANGE_ID from specify/draft to specify/ready.

    The only transition CHG-001 implements -- not a general status editor
    (R-010). Every R-011 precondition must hold; a rejected transition never
    modifies `state.yaml` (R-012).
    """
    if target_status != SUPPORTED_TARGET_STATUS:
        typer.echo(
            f"Unsupported target status {target_status!r}: "
            f"CHG-001 only supports {SUPPORTED_TARGET_STATUS!r}."
        )
        raise typer.Exit(code=1)

    try:
        result = perform_transition(target, change_id, actor=actor)
    except StateWriteError as exc:
        typer.echo(f"Transition failed during write: {exc}")
        raise typer.Exit(code=1) from exc

    if result.rejected:
        typer.echo("Transition rejected:")
        for issue in result.issues:
            typer.echo(f"  {issue}")
        raise typer.Exit(code=1)

    typer.echo(f"{change_id}: specify/draft -> specify/{result.new_status}")
