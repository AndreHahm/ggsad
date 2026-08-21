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


def _result_envelope(  # noqa: PLR0913
    operation: str,
    result: str,
    *,
    changed: bool,
    issues: list[dict[str, str]] | None = None,
    state: dict[str, str] | None = None,
    data: dict[str, object] | None = None,
) -> dict[str, object]:
    """Build the shared observable result for every contract operation."""
    envelope: dict[str, object] = {
        "operation": operation,
        "result": result,
        "changed": changed,
    }
    if state is not None:
        envelope["state"] = state
    if issues is not None:
        envelope["issues"] = issues
    if data is not None:
        envelope["data"] = data
    return envelope


def _emit_envelope(envelope: dict[str, object]) -> None:
    typer.echo(f"Result: {json.dumps(envelope, sort_keys=True)}")


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
        _emit_envelope(
            _result_envelope(
                "initialize",
                "rejected",
                changed=False,
                issues=[
                    {"code": "path_conflict", "message": str(path)} for path in result.conflicts
                ],
            )
        )
        raise typer.Exit(code=1)

    typer.echo(f"GG-SAD project initialized at {target.resolve()}")
    _emit_envelope(
        _result_envelope(
            "initialize",
            "success",
            changed=bool(result.created),
            data={"message": f"GG-SAD project initialized at {target.resolve()}"},
        )
    )


@app.command("new")
def new_command(  # noqa: PLR0913, PLR0917
    change_id: Annotated[str, typer.Argument(help="Change ID, e.g. CHG-002.")],
    slug: Annotated[str, typer.Argument(help="Lowercase, hyphenated slug, e.g. example-change.")],
    goal: Annotated[
        str | None,
        typer.Option("--goal", help="Required goal summary that binds the new change."),
    ] = None,
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
            goal=goal or "",
            change_class=change_class,
        )
    except ChangeCreationError as exc:
        typer.echo(f"Change creation rejected: {exc}")
        _emit_envelope(
            _result_envelope(
                "create_change",
                "rejected",
                changed=False,
                issues=[{"code": "invalid_change", "message": str(exc)}],
            )
        )
        raise typer.Exit(code=1) from exc

    result = write_manifest(manifest)
    _echo_manifest_result(result, operation="Change creation")

    if not result.ok:
        _emit_envelope(
            _result_envelope(
                "create_change",
                "rejected",
                changed=False,
                issues=[
                    {"code": "path_conflict", "message": str(path)} for path in result.conflicts
                ],
            )
        )
        raise typer.Exit(code=1)

    message = f"Class {change_class} change {change_id} created at specs/{change_id}-{slug}/"
    typer.echo(message)
    _emit_envelope(
        _result_envelope(
            "create_change",
            "success",
            changed=True,
            state={"phase": "specify", "status": "draft"},
            data={"message": message},
        )
    )


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
        message = f"Invalid --format {output_format!r}: must be 'text' or 'json'."
        typer.echo(message)
        _emit_envelope(
            _result_envelope(
                "validate",
                "rejected",
                changed=False,
                issues=[{"code": "invalid_format", "message": message}],
            )
        )
        raise typer.Exit(code=1)

    issues = validate_repository(target, change_id=change)

    issue_data = [{"code": issue.category.value, "message": str(issue)} for issue in issues]
    envelope = _result_envelope(
        "validate",
        "rejected" if issues else "success",
        changed=False,
        issues=issue_data if issues else None,
        data={"message": f"{len(issues)} validation issue(s) found."}
        if issues
        else {"message": "Validation passed."},
    )
    if output_format == "json":
        typer.echo(json.dumps(envelope, indent=2))
    else:
        for issue in issues:
            typer.echo(str(issue))
        if issues:
            typer.echo(f"{len(issues)} validation issue(s) found.")
        else:
            typer.echo(f"OK: no validation issues found under {target.resolve()}")
        _emit_envelope(envelope)

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
        message = (
            f"Unsupported target status {target_status!r}: "
            f"CHG-001 only supports {SUPPORTED_TARGET_STATUS!r}."
        )
        typer.echo(message)
        _emit_envelope(
            _result_envelope(
                "transition",
                "rejected",
                changed=False,
                issues=[{"code": "unsupported_transition", "message": message}],
            )
        )
        raise typer.Exit(code=1)

    try:
        result = perform_transition(target, change_id, actor=actor)
    except StateWriteError as exc:
        typer.echo(f"Transition failed during write: {exc}")
        _emit_envelope(
            _result_envelope(
                "transition",
                "error",
                changed=False,
                issues=[{"code": "state_write_error", "message": str(exc)}],
            )
        )
        raise typer.Exit(code=1) from exc

    if result.rejected:
        typer.echo("Transition rejected:")
        for issue in result.issues:
            typer.echo(f"  {issue}")
        _emit_envelope(
            _result_envelope(
                "transition",
                "rejected",
                changed=False,
                issues=[
                    {"code": issue.category.value, "message": str(issue)} for issue in result.issues
                ],
            )
        )
        raise typer.Exit(code=1)

    typer.echo(f"{change_id}: specify/draft -> specify/{result.new_status}")
    _emit_envelope(
        _result_envelope(
            "transition",
            "success",
            changed=True,
            state={"phase": "specify", "status": str(result.new_status)},
        )
    )
