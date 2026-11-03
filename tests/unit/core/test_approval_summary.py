"""The approval summary and its confirmation (Section 24.1, AE-319)."""

from __future__ import annotations

import io
import json
from dataclasses import replace
from pathlib import Path
from typing import override

import pytest
from project_helpers import make_change, settle
from test_status import loaded_change

from ggsad.core.approval_summary import build_summary
from ggsad.core.cli import main
from ggsad.core.gate_model import Gate
from ggsad.core.state import Approval, State

AT = "2026-11-03T10:00:00Z"
OLD = "sha256:" + "0" * 64


class Terminal(io.StringIO):
    @override
    def isatty(self) -> bool:
        return True


def approve(root: Path, stdin: io.StringIO, *extra: str) -> int:
    argv = ["approve", "c-1", "all", "--actor", "human:ada", "--assurance", "A1", *extra]
    return main([*argv, "--root", str(root)], clock=lambda: AT, stdin=stdin)


def test_the_first_summary_lists_what_the_spec_asks_for(root: Path) -> None:
    settings, loaded = loaded_change(root)
    lines = build_summary(replace(loaded, state=State()), settings)
    text = "\n".join(lines)
    assert "first approval" in text
    assert "fail gate scope-violation: hard" in text
    assert "default retry limit: 3" in text
    assert "team_mode: team" in text and "anchor: set" in text
    assert "enforces: the scope" in text and "conduct only:" in text


def test_ae319_a_reapproval_says_first_that_an_override_lapses(root: Path) -> None:
    settings, loaded = loaded_change(root)
    state = State(
        state="active",
        approvals=(
            Approval("gates", "human:ada", "A1", "A0", OLD, definitions_hash=OLD),
            Approval("override", "human:ada", "A1", "A0", gate="flaky", attempts=2, used=1,
                     definitions_hash=OLD),
            Approval("gate", "human:ada", "A1", "A0", gate="legal", definitions_hash=OLD),
        ),
    )  # fmt: skip
    lines = build_summary(replace(loaded, state=state), settings)
    assert lines[0].startswith("the override of flaky lapses with 1 attempt(s) left")
    assert "the change would pause again" in lines[0]
    assert lines[1] == "the sign-off of legal becomes stale"
    assert "the gate definitions (approved" in "\n".join(lines)


def test_a_softer_fail_gate_is_flagged(root: Path) -> None:
    settings, loaded = loaded_change(root)
    gates = (Gate("flaky", "fail", "command", "soft"),)
    changed = replace(loaded, context=replace(loaded.context, gates=gates), state=State())
    assert "fail gate flaky: soft (softer than the default hard)" in build_summary(
        changed, settings
    )


def test_changed_documents_are_named(root: Path) -> None:
    settings, loaded = loaded_change(root)
    approval = Approval("spec", "human:ada", "A1", "A0", "sha256:" + "1" * 64,
                        documents=(("docs/constitution.md", OLD),))  # fmt: skip
    lines = build_summary(replace(loaded, state=State(approvals=(approval,))), settings)
    assert any("spec.md" in line and "docs/constitution.md" in line for line in lines)


def test_without_confirmation_nothing_is_recorded(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_change(root)
    settle(root)
    assert approve(root, io.StringIO("")) == 1
    captured = capsys.readouterr()
    assert "approval summary:" in captured.err and "approval-not-confirmed" in captured.out
    entries = json.loads((root / "specs/c-1/state.json").read_text(encoding="utf-8"))["entries"]
    assert len(entries) == 1


def test_an_interactive_yes_records_and_a_no_does_not(root: Path) -> None:
    make_change(root)
    settle(root)
    assert approve(root, Terminal("n\n")) == 1
    assert approve(root, Terminal("y\n")) == 0
    entries = json.loads((root / "specs/c-1/state.json").read_text(encoding="utf-8"))["entries"]
    assert len(entries) == 2


def test_yes_skips_the_question_but_still_shows_the_summary(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_change(root)
    settle(root)
    assert approve(root, io.StringIO(""), "--yes") == 0
    assert "approval summary:" in capsys.readouterr().err


def test_an_agent_is_rejected_without_a_summary(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_change(root)
    argv = ["approve", "c-1", "all", "--actor", "agent:builder", "--root", str(root)]
    assert main(argv, clock=lambda: AT, stdin=io.StringIO("")) == 1
    assert "approval summary:" not in capsys.readouterr().err
