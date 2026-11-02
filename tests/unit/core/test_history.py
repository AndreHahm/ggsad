"""Entries, the hash chain, and the anchor: AE-043 to AE-045, AE-075, AE-079, AE-083."""

from __future__ import annotations

from typing import Any

import pytest

from ggsad.core.canonical import ZERO_HASH, DomainError
from ggsad.core.history import (
    Anchor,
    Entry,
    EntryInvalidError,
    check_anchor,
    entry_hash,
    make_entry,
    validate_body,
    verify_chain,
    verify_history,
)


def body(action: Any = "ask", **override: Any) -> dict[str, Any]:
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


def chain(count: int) -> list[Entry]:
    entries: list[Entry] = []
    previous = ZERO_HASH
    for n in range(1, count + 1):
        entry = make_entry(n, previous, body(note=f"entry {n}"))
        entries.append(entry)
        previous = entry.hash
    return entries


def codes(issues: list[Any]) -> list[str]:
    return [issue.code for issue in issues]


# --- body validation (AE-075, AE-079, AE-083) ---


def test_a_valid_body_has_no_issue() -> None:
    assert validate_body(body()) == []


def test_ae_079_every_body_field_is_present_and_one_that_does_not_apply_is_null() -> None:
    entry = make_entry(1, ZERO_HASH, body())

    assert set(entry.body) == {
        "action", "actor", "account", "assurance", "at", "result", "gate_results",
        "gate_detail", "files", "note", "after",
    }  # fmt: skip
    for name in ("gate_results", "gate_detail", "files", "note", "account"):
        assert entry.body[name] is None


def test_a_missing_field_is_reported_and_so_is_an_unknown_one() -> None:
    data = body()
    del data["note"]
    data["surprise"] = 1

    assert codes(validate_body(data)) == ["entry-field-missing", "entry-field-unknown"]


def test_ae_083_the_action_is_a_name_from_a_closed_set() -> None:
    for name in ("new", "approve", "ask", "answer", "adopt", "repair", "migrate_"):
        issues = validate_body(body(name, **_extras(name)))
        assert (name == "migrate_") == ("entry-action-unknown" in codes(issues))

    assert "entry-action-unknown" in codes(validate_body(body("rewind")))
    for odd in (None, ["new"], 5):
        assert "entry-action-unknown" in codes(validate_body(body(action=odd)))


def _extras(name: str) -> dict[str, Any]:
    return {"repair": {"repaired": {}}}.get(name, {})


def test_ae_075_not_applicable_is_a_value_of_gate_results_and_a_wrong_case_is_not() -> None:
    good = body(
        "start",
        gate_results={"no-secrets": "not_satisfied", "docs-built": "not_applicable"},
        gate_detail={"no-secrets": "found a key"},
    )
    bad = body("start", gate_results={"no-secrets": "Not_satisfied"})

    assert validate_body(good) == []
    assert codes(validate_body(bad)) == ["entry-field-invalid"]


@pytest.mark.parametrize(
    "override",
    [
        {"gate_results": ["satisfied"]},
        {"gate_results": {"g": 1}},
        {"gate_results": None, "gate_detail": {"g": "x"}},
        {"gate_results": {"g": "satisfied"}, "gate_detail": {"other": "x"}},
        {"gate_results": {"g": "satisfied"}, "gate_detail": {"g": 5}},
        {"gate_results": {"g": "satisfied"}, "gate_detail": "text"},
        {"files": {"a.md": "sha256:ABC"}},
        {"files": ["a.md"]},
        {"actor": ""},
        {"account": ""},
        {"assurance": "A3"},
        {"assurance": ["A0"]},
        {"at": "2026-11-02 10:00:00"},
        {"at": "2026-13-02T10:00:00Z"},
        {"at": 5},
        {"result": "rejected"},
        {"result": "error"},
        {"note": 3},
        {"after": "open"},
    ],
)
def test_invalid_values_are_reported(override: dict[str, Any]) -> None:
    assert "entry-field-invalid" in codes(validate_body(body(**override)))


def test_valid_optional_values_are_accepted() -> None:
    valid = body(
        account="ada-h",
        note="a note",
        files={"docs/a.md": "sha256:" + "a" * 64},
        gate_results={"g": "satisfied"},
        gate_detail={"g": "ok"},
    )

    assert validate_body(valid) == []


def test_actions_add_only_their_own_fields() -> None:
    close_with_report = body("close", agent_report={"errors": []})
    repair = body("repair", repaired={"lost": 3})
    migrate = body("migrate", source_version="0.9", target_version="1.0", source_hash=ZERO_HASH)

    assert validate_body(close_with_report) == []
    assert validate_body(repair) == []
    assert validate_body(migrate) == []
    assert "entry-field-unknown" in codes(validate_body(body("ask", agent_report={})))
    assert "entry-field-missing" in codes(validate_body(body("repair")))
    assert "entry-field-missing" in codes(validate_body(body("migrate")))


def test_make_entry_refuses_an_invalid_body_and_a_body_outside_the_domain() -> None:
    with pytest.raises(EntryInvalidError):
        make_entry(1, ZERO_HASH, body(result="rejected"))
    with pytest.raises(DomainError):
        make_entry(1, ZERO_HASH, body(after={"x": 1.5}))


# --- the chain ---


def test_a_chain_of_entries_is_consistent() -> None:
    assert verify_chain(chain(4)) == []
    assert verify_history(chain(1), None).ok


def test_the_first_entry_follows_the_zero_hash() -> None:
    assert chain(2)[0].prev == ZERO_HASH
    assert chain(2)[1].prev == chain(2)[0].hash


def test_a_history_without_an_entry_is_not_consistent() -> None:
    assert codes(verify_chain([])) == ["history-inconsistent"]


def tampered(entries: list[Entry], index: int, **changes: Any) -> list[Entry]:
    entry = entries[index]
    values = {"n": entry.n, "prev": entry.prev, "body": entry.body, "hash": entry.hash}
    values.update(changes)
    return [*entries[:index], Entry(**values), *entries[index + 1 :]]


def test_an_edited_body_breaks_the_chain() -> None:
    entries = tampered(chain(3), 1, body=body(note="edited"))

    issues = verify_chain(entries)

    assert codes(issues) == ["history-inconsistent"]
    assert "entry 2 does not match its hash" in issues[0].message


def test_a_removed_middle_entry_breaks_the_chain() -> None:
    entries = chain(4)
    del entries[1]

    assert "history-inconsistent" in codes(verify_chain(entries))


@pytest.mark.parametrize("field", ["n", "prev"])
def test_a_wrong_position_or_previous_hash_breaks_the_chain(field: str) -> None:
    value: Any = 9 if field == "n" else ZERO_HASH

    assert codes(verify_chain(tampered(chain(3), 2, **{field: value}))) == ["history-inconsistent"]


def test_an_entry_with_a_value_outside_the_domain_is_inconsistent_not_a_crash() -> None:
    entry = chain(1)[0]
    broken = Entry(1, entry.prev, {**entry.body, "after": {"x": 1.5}}, entry.hash)

    assert "outside the domain" in verify_chain([broken])[0].message


def test_a_history_consistent_in_a_rewritten_layout_is_still_consistent() -> None:
    entries = chain(3)
    again = [Entry(e.n, e.prev, dict(reversed(list(e.body.items()))), e.hash) for e in entries]

    assert verify_chain(again) == []


# --- the anchor (AE-043, AE-044, AE-045) ---


def test_a_history_that_agrees_with_its_anchor_passes_and_may_be_longer() -> None:
    entries = chain(5)

    assert check_anchor(entries, Anchor(5, entries[4].hash)) == []
    assert check_anchor(entries, Anchor(3, entries[2].hash)) == []


def test_a_history_with_fewer_entries_than_the_anchor_is_truncated() -> None:
    entries = chain(5)

    issues = check_anchor(entries[:3], Anchor(5, entries[4].hash))

    assert codes(issues) == ["history-truncated"]
    assert "truncated" in issues[0].message


def test_ae_043_a_rewritten_entry_is_detected_through_the_anchor() -> None:
    original = chain(5)
    anchor = Anchor(5, original[4].hash)
    # Entry 5 is edited and the hashes are computed again, so the chain stays consistent.
    forged_body = body(note="forged")
    forged = Entry(5, original[3].hash, forged_body, entry_hash(original[3].hash, forged_body))
    history = [*original[:4], forged]

    assert verify_chain(history) == []
    report = verify_history(history, anchor)
    assert report.codes == ("history-rewritten",)
    assert "rewritten" in report.issues[0].message


def test_ae_044_a_history_without_an_anchor_is_refused_where_one_is_required() -> None:
    entries = chain(3)

    assert verify_history(entries, None, require_anchor=True).codes == ("anchor-missing",)
    assert verify_history(entries, None).ok
    assert verify_history(entries, Anchor(3, entries[2].hash), require_anchor=True).ok


def test_an_inconsistent_chain_is_reported_before_the_anchor_is_looked_at() -> None:
    entries = tampered(chain(3), 1, body=body(note="edited"))

    report = verify_history(entries, Anchor(3, entries[2].hash), require_anchor=True)

    assert report.codes == ("history-inconsistent",)
