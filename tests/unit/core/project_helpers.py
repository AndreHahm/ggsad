"""Shared helpers for tests that run operations on a real temporary project."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from ggsad.core.engine_types import Actor, Request
from ggsad.core.new_change import NewFields, create_change
from ggsad.core.operations import Envelope

CONFIG = """\
schema_version: "1.0"
project: {id: demo, compliance_profile: lean}
roles:
  owner: "human:ada"
  approved_humans:
    - {identity: "human:ada", account: ada-gh}
  requestors:
    - {identity: "agent:builder"}
"""
SENTENCE = "Users can reset a password"
FIELDS = NewFields("Resets are manual", [SENTENCE], "human:ada", "human:ada")
AGENT = Actor("agent:builder")
ADA = Actor("human:ada", "A1", "ada-gh")
AT = "2026-11-03T10:00:00Z"
FULL = """\
schema_version: "1.0"
id: c-1
method_profile: core
compliance_profile: lean
author: "human:ada"
owner: "human:ada"
goal:
  problem: Resets are manual
  done_when: ["Users can reset a password"]
  non_goals: []
scope:
  allow: ["lib/**"]
requirements:
  - id: R1
    text: A user can reset a password
    examples: ["Given a user, when they reset, then a mail is sent"]
    done_when: ["Users can reset a password"]
    evidence:
      - command: [run-tests]
        exit_map: {satisfied: [0], not_satisfied: [1]}
gates: {fail: [], wait: [], done: []}
"""


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def write(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def req(action: str, actor: Actor = AGENT, **fields: Any) -> Request:
    return Request(action, actor, AT, **fields)


def make_change(root: Path) -> Envelope:
    return create_change(root, "c-1", req("new"), FIELDS)


def settle(root: Path) -> None:
    """Replace the template by a complete definition and commit it."""
    write(root, "specs/c-1/change.yaml", FULL)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "change")
