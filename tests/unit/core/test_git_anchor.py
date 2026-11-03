"""The Git-ref anchor store: it behaves like the file store (AE-043 to AE-045 use the protocol)."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from ggsad.core.anchor import AnchorStore, adopt_anchor, advance_anchor
from ggsad.core.canonical import ZERO_HASH
from ggsad.core.errors import StateError
from ggsad.core.git_anchor import GitAnchorStore
from ggsad.core.history import Anchor, make_entry

VALID_BODY = {
    "action": "ask",
    "actor": "human:ada",
    "account": None,
    "assurance": "A0",
    "at": "2026-11-02T10:00:00Z",
    "result": "success",
    "gate_results": None,
    "gate_detail": None,
    "files": None,
    "note": None,
    "after": {"state": "open", "schema_version": "1.0"},
}


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True, capture_output=True)
    return tmp_path


def entries(count: int) -> list:
    made = []
    previous = ZERO_HASH
    for number in range(1, count + 1):
        entry = make_entry(number, previous, VALID_BODY)
        made.append(entry)
        previous = entry.hash
    return made


def test_a_missing_anchor_reads_as_none(repo: Path) -> None:
    assert GitAnchorStore(repo).read("c-1") is None


def test_a_written_anchor_is_read_back(repo: Path) -> None:
    store = GitAnchorStore(repo)
    store.write("c-1", Anchor(2, "sha256:" + "a" * 64))
    assert store.read("c-1") == Anchor(2, "sha256:" + "a" * 64)


def test_the_store_satisfies_the_protocol(repo: Path) -> None:
    store: AnchorStore = GitAnchorStore(repo)
    chain = entries(3)
    adopt_anchor(store, "c-1", chain[:2])
    advance_anchor(store, "c-1", chain)
    assert store.read("c-1") == Anchor(3, chain[-1].hash)


def test_a_change_identifier_that_is_a_path_is_refused(repo: Path) -> None:
    with pytest.raises(StateError) as caught:
        GitAnchorStore(repo).read("../x")
    assert caught.value.code == "anchor-invalid"


def test_a_damaged_blob_is_an_error_not_no_anchor(repo: Path) -> None:
    blob = (
        subprocess.run(
            ["git", "hash-object", "-w", "--stdin"],
            cwd=repo,
            input=b"not json",
            check=True,
            capture_output=True,
        )
        .stdout.decode()
        .strip()
    )
    subprocess.run(
        ["git", "update-ref", "refs/ggsad/anchors/c-1", blob],
        cwd=repo,
        check=True,
        capture_output=True,
    )
    with pytest.raises(StateError) as caught:
        GitAnchorStore(repo).read("c-1")
    assert caught.value.code == "anchor-invalid"


def test_prepare_leaves_no_trace(repo: Path) -> None:
    GitAnchorStore(repo).prepare("c-1")
    refs = subprocess.run(["git", "for-each-ref"], cwd=repo, check=True, capture_output=True).stdout
    assert refs == b""


def test_prepare_fails_outside_a_repository(tmp_path: Path) -> None:
    with pytest.raises(StateError) as caught:
        GitAnchorStore(tmp_path / "missing").prepare("c-1")
    assert caught.value.code == "anchor-write-failed"
