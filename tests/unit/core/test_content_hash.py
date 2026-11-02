"""The content hash (Implementation Contract 25.2): AE-087 to AE-092."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ggsad.core.canonical import DomainError, hash_bytes, hash_value
from ggsad.core.content_hash import (
    file_content_hash,
    files_content_hash,
    gate_binding_hash,
    is_text,
    normalize_line_endings,
    path_content_hash,
    yaml_content_hash,
    yaml_value,
)

if TYPE_CHECKING:
    from pathlib import Path


def test_ae_087_text_with_different_line_endings_has_one_content_hash() -> None:
    crlf = b"one\r\ntwo\r\n"
    lf = b"one\ntwo\n"
    cr = b"one\rtwo\r"

    assert file_content_hash(crlf) == file_content_hash(lf) == file_content_hash(cr)
    assert file_content_hash(lf) == hash_bytes(lf)


def test_a_lone_carriage_return_becomes_a_line_feed_and_nothing_else_changes() -> None:
    assert normalize_line_endings(b"a\r\r\nb\n\rc") == b"a\n\nb\n\nc"


def test_ae_088_the_kind_of_a_file_is_decided_by_its_bytes() -> None:
    text = "café\r\nline\r\n".encode()
    with_zero = b"a\r\n\x00\r\n"
    invalid = b"a\r\n\xff\xfe\r\n"

    for crlf in (text,):
        assert file_content_hash(crlf) == file_content_hash(crlf.replace(b"\r\n", b"\n"))
    for crlf in (with_zero, invalid):
        assert file_content_hash(crlf) != file_content_hash(crlf.replace(b"\r\n", b"\n"))
        assert file_content_hash(crlf) == hash_bytes(crlf)


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        (b"", True),
        (b"plain", True),
        ("é\U0001f600".encode(), True),
        (b"a\x00b", False),
        (b"\xc0\xaf", False),  # overlong encoding
        (b"\xed\xa0\x80", False),  # a surrogate code point
        (b"\xf4\x90\x80\x80", False),  # above U+10FFFF
        (b"\xff", False),
    ],
)
def test_a_file_is_text_exactly_when_it_is_valid_utf8_without_a_zero_byte(
    data: bytes, expected: bool
) -> None:
    assert is_text(data) is expected


def test_the_content_hash_of_a_file_on_disk(tmp_path: Path) -> None:
    path = tmp_path / "a.txt"
    path.write_bytes(b"x\r\ny\r\n")

    assert path_content_hash(path) == file_content_hash(b"x\ny\n")


BASE = """\
gates:
  done:
    - id: lint
    - id: tests
  limit: 3
"""


def test_ae_089_layout_comments_key_order_and_quoting_do_not_change_the_hash() -> None:
    varied = """\
# a comment
gates:
    limit: 3   # trailing comment
    done:
        - id: "lint"
        - {id: tests}
"""
    reordered = BASE.replace("- id: lint\n    - id: tests", "- id: tests\n    - id: lint")

    assert yaml_content_hash(varied) == yaml_content_hash(BASE)
    assert yaml_content_hash(reordered) != yaml_content_hash(BASE)


def test_ae_090_a_float_is_outside_the_domain_and_a_quoted_number_is_not() -> None:
    with pytest.raises(DomainError, match="floating-point"):
        yaml_content_hash("limit: 1.5\n")

    assert yaml_content_hash("limit: '1.5'\n") == hash_value({"limit": "1.5"})


def test_ae_091_the_order_of_the_files_has_no_effect_on_the_hash_of_a_set() -> None:
    a = file_content_hash(b"a")
    b = file_content_hash(b"b")

    first = files_content_hash({"lib/a.py": a, "docs/b.md": b})
    second = files_content_hash({"docs/b.md": b, "lib/a.py": a})

    assert first == second == hash_value({"docs/b.md": b, "lib/a.py": a})


def test_ae_092_the_identifier_of_the_gate_is_part_of_the_hash_of_a_sign_off() -> None:
    definitions = yaml_content_hash(BASE)

    assert gate_binding_hash(definitions, "review-ok") != gate_binding_hash(
        definitions, "release-ok"
    )
    assert gate_binding_hash(definitions, "review-ok") == hash_value(
        {"definitions": definitions, "gate": "review-ok"}
    )


# --- the YAML 1.2 core schema and the domain ---


def test_scalars_follow_the_core_schema() -> None:
    value = yaml_value(
        "a: null\nb: true\nc: False\nd: 12\ne: 0x1F\nf: 0o17\ng: -3\nh: +4\ni: '007'\nj: 007\n"
    )

    assert value == {
        "a": None, "b": True, "c": False, "d": 12, "e": 31, "f": 15, "g": -3, "h": 4,
        "i": "007", "j": 7,
    }  # fmt: skip


def test_a_date_is_a_plain_string_because_the_core_schema_has_no_timestamps() -> None:
    assert yaml_value("review_by: 2026-12-01\nat: 2026-12-01T10:00:00Z\n") == {
        "review_by": "2026-12-01",
        "at": "2026-12-01T10:00:00Z",
    }


def test_an_alias_is_replaced_by_the_value_it_refers_to() -> None:
    assert yaml_value("a: &x [1, 2]\nb: *x\n") == {"a": [1, 2], "b": [1, 2]}


def test_an_empty_document_is_null() -> None:
    assert yaml_value("") is None


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("a: 1\na: 2\n", "repeats the key"),
        ("1: a\n", "key must be a string"),
        ("? [a]\n: b\n", "key must be a string"),
        ("a: .inf\n", "floating-point"),
        ("a: .nan\n", "floating-point"),
        ("a: !!binary aGk=\n", "not in the domain"),
        ("a: [unclosed\n", "not valid YAML"),
        ("a: 1\n---\nb: 2\n", "not valid YAML"),
        ("a: 9007199254740993\n", "exceed"),
    ],
)
def test_a_value_outside_the_domain_has_no_content_hash(text: str, reason: str) -> None:
    with pytest.raises(DomainError, match=reason):
        yaml_content_hash(text)
