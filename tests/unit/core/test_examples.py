"""The projects in `examples/` stay valid: each one passes `ggsad doctor` and `ggsad check`.

An example is copied to a temporary folder and made a Git repository again, because the record
files are all that `examples/` keeps. Regenerate the examples with `scripts/build_examples.py`.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from ggsad.core.cli import main

EXAMPLES = Path(__file__).resolve().parents[3] / "examples"
NAMES = ("lean-startup", "solo-developer", "governed-enterprise")


def _repository(name: str, target: Path) -> Path:
    shutil.copytree(EXAMPLES / name, target)
    for args in (
        ["init", "-q"],
        ["add", "-A"],
        ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "example"],
    ):
        subprocess.run(["git", *args], cwd=target, check=True, capture_output=True)  # nosec B603 B607
    return target


@pytest.mark.parametrize("name", NAMES)
def test_example_is_present(name: str) -> None:
    folders = sorted(path.name for path in (EXAMPLES / name / "specs").iterdir())
    assert len(folders) == 2


@pytest.mark.parametrize("name", NAMES)
def test_doctor_finds_no_problem_in_example(
    name: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _repository(name, tmp_path / name)
    code = main(["doctor", "--root", str(root)])
    output = capsys.readouterr().out
    assert code == 0, output
    assert "[problem]" not in output


@pytest.mark.parametrize("name", NAMES)
def test_check_reads_every_change_of_example(
    name: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _repository(name, tmp_path / name)
    for folder in sorted(path.name for path in (root / "specs").iterdir()):
        code = main(["check", folder, "--root", str(root)])
        output = capsys.readouterr().out
        assert code == 0, output
        assert "needs you" in output or "state: closed" in output
