"""The state document and its safe writing (Contract 25.1, Section 24.4).

AE-078, AE-080, AE-081, AE-085, AE-086, and the anchor examples AE-043 to AE-045 end to end.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ggsad.core.anchor import FileAnchorStore, adopt_anchor, advance_anchor
from ggsad.core.canonical import ZERO_HASH
from ggsad.core.errors import StateError
from ggsad.core.history import Anchor, entry_hash
from ggsad.core.state_store import (
    LOCK_FILE,
    TEMPORARY_FILE,
    StateStore,
    _exclusive_lock,
    parse_state_document,
)


def body(action: str = "ask", **override: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "action": action,
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
    data.update(override)
    return data


def append_all(store: StateStore, count: int) -> None:
    for version in range(count):
        store.append(body(note=f"entry {version + 1}"), read_version=version)


def rewrite(path: Path, edit: Any) -> None:
    document = json.loads(path.read_text(encoding="utf-8"))
    edit(document)
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


# --- creating and appending ---


def test_the_first_append_creates_the_state_document(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "c-1")

    entry = store.append(body("new"), read_version=0)

    document = store.read()
    assert document is not None
    assert document.entries == (entry,)
    assert entry.n == 1
    assert entry.prev == ZERO_HASH
    assert document.schema_version == "1.0"
    store.verify(document)


def test_each_append_follows_the_hash_of_the_entry_before_it(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    append_all(store, 4)

    document = store.read()

    assert document is not None
    assert [e.n for e in document.entries] == [1, 2, 3, 4]
    assert all(
        b.prev == a.hash for a, b in zip(document.entries, document.entries[1:], strict=False)
    )


def test_a_change_without_a_state_document_reads_as_none(tmp_path: Path) -> None:
    assert StateStore(tmp_path).read() is None


def test_an_invalid_body_writes_nothing(tmp_path: Path) -> None:
    store = StateStore(tmp_path)

    with pytest.raises(ValueError, match="entry-field-invalid"):
        store.append(body(result="rejected"), read_version=0)

    assert not store.state_path.exists()


def test_a_body_outside_the_domain_writes_nothing(tmp_path: Path) -> None:
    store = StateStore(tmp_path)

    with pytest.raises(ValueError, match="float"):
        store.append(body(after={"x": 1.5}), read_version=0)

    assert not store.state_path.exists()


# --- AE-078: the layout of the file does not change a hash ---


def test_ae_078_the_layout_of_the_file_does_not_change_a_hash(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    append_all(store, 3)
    first = store.read()
    text = store.state_path.read_text(encoding="utf-8")
    compact = json.dumps(json.loads(text), separators=(",", ":"))
    store.state_path.write_text(compact, encoding="utf-8")

    second = store.read()

    assert first is not None
    assert second is not None
    assert [e.hash for e in first.entries] == [e.hash for e in second.entries]
    store.verify(second)


# --- AE-080 and AE-081: two writers ---


def test_ae_080_the_second_of_two_writers_with_the_same_version_fails_at_creation(
    tmp_path: Path,
) -> None:
    first, second = StateStore(tmp_path), StateStore(tmp_path)
    first.append(body("new"), read_version=0)

    with pytest.raises(StateError) as caught:
        second.append(body("new"), read_version=0)

    assert caught.value.code == "state-conflict"
    document = first.read()
    assert document is not None
    assert len(document.entries) == 1


def test_ae_081_a_leftover_lock_file_is_not_a_held_lock(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    append_all(store, 6)
    (tmp_path / LOCK_FILE).write_bytes(b"")  # left behind by a process that ended
    writer_one, writer_two = StateStore(tmp_path), StateStore(tmp_path)

    writer_one.append(body(note="question"), read_version=6)
    with pytest.raises(StateError) as caught:
        writer_two.append(body(note="other"), read_version=6)

    assert caught.value.code == "state-conflict"
    document = store.read()
    assert document is not None
    assert len(document.entries) == 7


def test_a_writer_that_cannot_take_the_lock_does_not_write(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    store.append(body("new"), read_version=0)

    with _exclusive_lock(tmp_path / LOCK_FILE), pytest.raises(StateError) as caught:
        store.append(body(note="blocked"), read_version=1)

    assert caught.value.code == "lock-unavailable"
    document = store.read()
    assert document is not None
    assert len(document.entries) == 1


# --- AE-085 and AE-086: an interrupted write ---


def test_ae_085_an_interrupted_creation_leaves_no_state_document(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = StateStore(tmp_path)

    def fail(self: Path, target: Any) -> None:
        raise OSError

    with monkeypatch.context() as patch:
        patch.setattr(Path, "replace", fail)
        with pytest.raises(StateError) as caught:
            store.append(body("new"), read_version=0)

    assert caught.value.code == "state-write-failed"
    assert (tmp_path / TEMPORARY_FILE).exists()
    assert store.read() is None
    store.append(body("new"), read_version=0)
    assert store.read() is not None


def test_ae_086_an_interrupted_write_leaves_the_previous_state_intact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    store = StateStore(tmp_path)
    append_all(store, 6)
    before = store.state_path.read_text(encoding="utf-8")

    def fail(self: Path, target: Any) -> None:
        raise OSError

    with monkeypatch.context() as patch:
        patch.setattr(Path, "replace", fail)
        with pytest.raises(StateError):
            store.append(body(note="seventh"), read_version=6)

    assert store.state_path.read_text(encoding="utf-8") == before
    document = store.read()
    assert document is not None
    assert len(document.entries) == 6
    store.verify(document)


# --- reading a damaged document ---


@pytest.mark.parametrize(
    "text",
    [
        "not json",
        "[]",
        '{"schema_version": "1.0"}',
        '{"schema_version": "1.0", "entries": [], "extra": 1}',
        '{"schema_version": "1.0", "entries": [], "entries": []}',
        '{"schema_version": "1.0", "entries": [{"n": 1}]}',
        '{"schema_version": "1.0", "entries": [{"n": "1", "prev": "p", "body": {}, "hash": "h"}]}',
        '{"schema_version": "1.0", "entries": [{"n": 1, "prev": 5, "body": {}, "hash": "h"}]}',
        '{"schema_version": "1.0", "entries": [{"n": 1.5, "prev": "p", "body": {}, "hash": "h"}]}',
        '{"schema_version": 1.0, "entries": []}',
        '{"schema_version": NaN, "entries": []}',
    ],
)
def test_a_document_that_is_not_valid_is_refused(text: str) -> None:
    with pytest.raises(StateError):
        parse_state_document(text)


def test_a_repeated_key_makes_the_document_invalid() -> None:
    with pytest.raises(StateError, match="repeated"):
        parse_state_document('{"schema_version": "1.0", "schema_version": "1.0", "entries": []}')


def test_an_unreadable_file_is_an_error_not_an_empty_change(tmp_path: Path) -> None:
    (tmp_path / "state.json").write_bytes(b"\xff\xfe\x00")

    with pytest.raises(StateError) as caught:
        StateStore(tmp_path).read()

    assert caught.value.code == "state-read-failed"


def test_an_unsupported_or_mismatching_schema_version_is_refused(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    append_all(store, 2)

    rewrite(store.state_path, lambda d: d.update(schema_version="0.1"))
    with pytest.raises(StateError) as unsupported:
        store.read()
    assert unsupported.value.code == "schema-version-unsupported"

    rewrite(store.state_path, lambda d: d.update(schema_version="1.0"))
    rewrite(
        store.state_path, lambda d: d["entries"][1]["body"]["after"].update(schema_version="0.9")
    )
    with pytest.raises(StateError) as mismatch:
        store.read()
    assert mismatch.value.code == "schema-version-mismatch"


def test_a_hand_edited_document_is_not_acted_on(tmp_path: Path) -> None:
    store = StateStore(tmp_path)
    append_all(store, 3)
    rewrite(store.state_path, lambda d: d["entries"][1]["body"].update(note="edited by hand"))

    with pytest.raises(StateError) as caught:
        store.append(body(note="next"), read_version=3)

    assert caught.value.code == "history-inconsistent"
    document = store.read()
    assert document is not None
    assert len(document.entries) == 3


# --- the anchor, end to end (AE-043 to AE-045) ---


def anchored(tmp_path: Path, **options: Any) -> tuple[StateStore, FileAnchorStore]:
    anchors = FileAnchorStore(tmp_path / "anchors")
    return StateStore(tmp_path / "c-1", anchors=anchors, **options), anchors


def test_the_anchor_is_created_with_the_first_entry_and_advances_with_each_append(
    tmp_path: Path,
) -> None:
    store, anchors = anchored(tmp_path)

    first = store.append(body("new"), read_version=0)
    assert anchors.read("c-1") == Anchor(1, first.hash)
    second = store.append(body(), read_version=1)
    assert anchors.read("c-1") == Anchor(2, second.hash)


def test_without_an_anchor_store_nothing_is_anchored(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "c-1")
    store.append(body("new"), read_version=0)

    assert not (tmp_path / "anchors").exists()


def test_ae_043_a_rewritten_history_is_detected_through_the_anchor(tmp_path: Path) -> None:
    store, _ = anchored(tmp_path)
    append_all(store, 3)
    document = store.read()
    assert document is not None

    # Rewrite the last entry and recompute its hash, so that the chain stays consistent.
    def forge(data: dict[str, Any]) -> None:
        last = data["entries"][2]
        last["body"]["note"] = "forged"
        last["hash"] = entry_hash(last["prev"], last["body"])

    rewrite(store.state_path, forge)

    with pytest.raises(StateError) as caught:
        store.append(body(), read_version=3)

    assert caught.value.code == "history-rewritten"


def test_a_truncated_history_is_detected_through_the_anchor(tmp_path: Path) -> None:
    store, _ = anchored(tmp_path)
    append_all(store, 4)
    rewrite(store.state_path, lambda d: d["entries"].pop())

    with pytest.raises(StateError) as caught:
        store.append(body(), read_version=3)

    assert caught.value.code == "history-truncated"


def test_ae_044_a_history_without_an_anchor_is_refused_until_a_human_adopts_it(
    tmp_path: Path,
) -> None:
    plain = StateStore(tmp_path / "c-1")
    append_all(plain, 3)
    anchors = FileAnchorStore(tmp_path / "anchors")
    strict = StateStore(tmp_path / "c-1", anchors=anchors, require_anchor=True)

    with pytest.raises(StateError) as refused:
        strict.append(body(), read_version=3)
    assert refused.value.code == "anchor-missing"

    document = strict.read()
    assert document is not None
    anchor = adopt_anchor(anchors, "c-1", document.entries)
    assert anchor == Anchor(3, document.entries[2].hash)

    strict.append(body(), read_version=3)
    after = strict.read()
    assert after is not None
    assert anchors.read("c-1") == Anchor(4, after.entries[3].hash)


def test_ae_045_the_adoption_of_an_inconsistent_history_is_rejected(tmp_path: Path) -> None:
    plain = StateStore(tmp_path / "c-1")
    append_all(plain, 3)
    rewrite(plain.state_path, lambda d: d["entries"][1]["body"].update(note="edited"))
    document = parse_state_document(plain.state_path.read_text(encoding="utf-8"))
    anchors = FileAnchorStore(tmp_path / "anchors")

    with pytest.raises(StateError) as caught:
        adopt_anchor(anchors, "c-1", document.entries)

    assert caught.value.code == "adopt-rejected"
    assert anchors.read("c-1") is None


def test_an_existing_anchor_cannot_be_adopted_over(tmp_path: Path) -> None:
    store, anchors = anchored(tmp_path)
    append_all(store, 2)
    document = store.read()
    assert document is not None

    with pytest.raises(StateError) as caught:
        adopt_anchor(anchors, "c-1", document.entries)

    assert caught.value.code == "adopt-rejected"


def test_an_anchor_is_never_replaced_by_one_from_another_history(tmp_path: Path) -> None:
    store, anchors = anchored(tmp_path)
    append_all(store, 2)
    other = StateStore(tmp_path / "other")
    other.append(body(note="different"), read_version=0)
    other.append(body(note="different 2"), read_version=1)
    other_document = other.read()
    assert other_document is not None

    with pytest.raises(StateError) as caught:
        advance_anchor(anchors, "c-1", other_document.entries)

    assert caught.value.code == "anchor-conflict"
    kept = anchors.read("c-1")
    assert kept is not None
    assert kept.position == 2


def test_a_damaged_anchor_file_is_an_error_not_no_anchor(tmp_path: Path) -> None:
    store, anchors = anchored(tmp_path)
    store.append(body("new"), read_version=0)
    path = tmp_path / "anchors" / "c-1.anchor.json"

    for content in ("garbage", "[]", '{"position": 0, "hash": "x"}', '{"position": 1}'):
        path.write_text(content, encoding="utf-8")
        with pytest.raises(StateError) as caught:
            anchors.read("c-1")
        assert caught.value.code == "anchor-invalid"


def test_an_anchor_is_kept_for_a_valid_change_identifier_only(tmp_path: Path) -> None:
    anchors = FileAnchorStore(tmp_path)

    with pytest.raises(StateError):
        anchors.read("../escape")
    with pytest.raises(StateError):
        anchors.write("a/b", Anchor(1, ZERO_HASH))


# --- anchor failures (Codex findings on PR 15) ---


def test_a_required_anchor_without_an_anchor_store_is_refused_before_anything_is_written(
    tmp_path: Path,
) -> None:
    with pytest.raises(StateError) as caught:
        StateStore(tmp_path / "c-1", require_anchor=True)

    assert caught.value.code == "anchor-required"
    assert not (tmp_path / "c-1").exists()


def test_an_unwritable_anchor_location_is_refused_before_the_state_document_is_written(
    tmp_path: Path,
) -> None:
    (tmp_path / "anchors").write_text("a regular file, not a directory", encoding="utf-8")
    store = StateStore(tmp_path / "c-1", anchors=FileAnchorStore(tmp_path / "anchors"))

    with pytest.raises(StateError) as created:
        store.append(body("new"), read_version=0)
    assert created.value.code == "anchor-write-failed"
    assert store.read() is None

    (tmp_path / "anchors").unlink()
    store.append(body("new"), read_version=0)
    (tmp_path / "anchors" / "c-1.anchor.json").unlink()
    (tmp_path / "anchors").rename(tmp_path / "anchors-moved")
    (tmp_path / "anchors").write_text("a regular file again", encoding="utf-8")
    with pytest.raises(StateError) as appended:
        store.append(body(), read_version=1)
    assert appended.value.code == "anchor-write-failed"
    document = store.read()
    assert document is not None
    assert len(document.entries) == 1


def failing_write(self: FileAnchorStore, change_id: str, anchor: Anchor) -> None:
    raise StateError("anchor-write-failed", "disk full")


def test_an_anchor_that_fails_after_the_write_reports_that_the_entry_was_recorded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    anchors = FileAnchorStore(tmp_path / "anchors")
    store = StateStore(tmp_path / "c-1", anchors=anchors)
    store.append(body("new"), read_version=0)

    with monkeypatch.context() as patch:
        patch.setattr(FileAnchorStore, "write", failing_write)
        with pytest.raises(StateError) as caught:
            store.append(body(), read_version=1)

    assert caught.value.code == "anchor-lagging"
    assert "entry 2 was recorded" in caught.value.message
    document = store.read()
    assert document is not None
    assert len(document.entries) == 2  # the error does not claim that nothing was written


def test_a_lagging_anchor_is_recovered_by_the_next_append(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    anchors = FileAnchorStore(tmp_path / "anchors")
    store = StateStore(tmp_path / "c-1", anchors=anchors)
    store.append(body("new"), read_version=0)
    with monkeypatch.context() as patch:
        patch.setattr(FileAnchorStore, "write", failing_write)
        with pytest.raises(StateError):
            store.append(body(), read_version=1)
    stale = store.read()
    assert stale is not None
    assert anchors.read("c-1") == Anchor(1, stale.entries[0].hash)

    store.verify(stale)  # a history longer than its anchor still agrees with it
    third = store.append(body(), read_version=2)

    assert anchors.read("c-1") == Anchor(3, third.hash)


def test_a_first_entry_whose_anchor_failed_is_recovered_by_adoption(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    anchors = FileAnchorStore(tmp_path / "anchors")
    store = StateStore(tmp_path / "c-1", anchors=anchors, require_anchor=True)
    with monkeypatch.context() as patch:
        patch.setattr(FileAnchorStore, "write", failing_write)
        with pytest.raises(StateError) as lagging:
            store.append(body("new"), read_version=0)
    assert lagging.value.code == "anchor-lagging"
    with pytest.raises(StateError) as refused:
        store.append(body(), read_version=1)
    assert refused.value.code == "anchor-missing"

    document = store.read()
    assert document is not None
    adopt_anchor(anchors, "c-1", document.entries)

    store.append(body(), read_version=1)
    assert anchors.read("c-1") is not None
