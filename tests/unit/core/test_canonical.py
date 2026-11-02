"""The canonical form and the hash string (Implementation Contract 25.1): AE-074, 076, 077."""

from __future__ import annotations

import json

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ggsad.core.canonical import (
    MAX_INTEGER,
    ZERO_HASH,
    DomainError,
    canonical_bytes,
    canonical_text,
    hash_bytes,
    hash_value,
    is_hash_string,
)


def test_ae_074_the_canonical_form_sorts_keys_drops_whitespace_and_keeps_non_ascii() -> None:
    value = {"name": "café", "count": 2}

    assert canonical_text(value) == '{"count":2,"name":"café"}'
    assert canonical_bytes(value) == b'{"count":2,"name":"caf\xc3\xa9"}'
    assert (
        hash_value(value)
        == "sha256:29775eba68050199f13058db83b4c14ba4b6a6a26666d6373a3cc47481bf6471"
    )


def test_ae_076_keys_are_ordered_by_code_point_not_by_utf16_code_unit() -> None:
    emoji, tilde = chr(0x1F600), chr(0xFF5E)

    assert canonical_text({emoji: 1, tilde: 2}) == f'{{"{tilde}":2,"{emoji}":1}}'


@pytest.mark.parametrize(
    "value",
    [1.5, float("nan"), {"a": 1.0}, [2**53], {"a": b"bytes"}, {1: "x"}, ("tuple",), {"a": {3}}],
)
def test_ae_077_a_value_outside_the_domain_is_neither_written_nor_hashed(value: object) -> None:
    with pytest.raises(DomainError):
        canonical_bytes(value)
    with pytest.raises(DomainError):
        hash_value(value)


def test_the_error_names_where_the_value_is() -> None:
    with pytest.raises(DomainError) as caught:
        canonical_text({"a": [1, {"b": 1.5}]})

    assert caught.value.path == ".a[1].b"


def test_a_surrogate_code_point_is_outside_the_domain() -> None:
    with pytest.raises(DomainError):
        canonical_text("bad\ud800")


@pytest.mark.parametrize(
    ("value", "text"),
    [
        (None, "null"),
        (True, "true"),
        (False, "false"),
        (0, "0"),
        (-7, "-7"),
        (MAX_INTEGER, str(MAX_INTEGER)),
        (-MAX_INTEGER, str(-MAX_INTEGER)),
        ([], "[]"),
        ({}, "{}"),
        ('a"b\\c', '"a\\"b\\\\c"'),
        ("\b\t\n\f\r", '"\\b\\t\\n\\f\\r"'),
        ("\x00\x1f", '"\\u0000\\u001f"'),
        ("\x7f/", '"\x7f/"'),
        ([1, "a", None], '[1,"a",null]'),
    ],
)
def test_the_canonical_text_of_each_kind_of_value(value: object, text: str) -> None:
    assert canonical_text(value) == text


def test_booleans_are_not_integers() -> None:
    assert canonical_text([True, 1]) == "[true,1]"


def test_integers_beyond_two_to_the_53_minus_1_are_outside_the_domain() -> None:
    for value in (MAX_INTEGER + 1, -MAX_INTEGER - 1):
        with pytest.raises(DomainError):
            canonical_text(value)


def test_the_hash_string_is_sha256_in_lowercase() -> None:
    digest = hash_bytes(b"")

    assert digest == "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert is_hash_string(digest)
    assert not is_hash_string(digest.upper().replace("SHA256", "sha256"))
    assert not is_hash_string("sha256:abc")
    assert not is_hash_string(5)
    assert ZERO_HASH == "sha256:" + "0" * 64


_JSON = st.recursive(
    st.none() | st.booleans() | st.integers(-1000, 1000) | st.text(max_size=8),
    lambda inner: (
        st.lists(inner, max_size=4) | st.dictionaries(st.text(max_size=6), inner, max_size=4)
    ),
    max_leaves=12,
)


@given(value=_JSON)
def test_the_canonical_text_is_json_and_does_not_depend_on_key_order(value: object) -> None:
    text = canonical_text(value)

    assert json.loads(text) == value
    assert canonical_text(json.loads(json.dumps(value, sort_keys=False))) == text
    assert canonical_text(json.loads(json.dumps(value, indent=3))) == text
