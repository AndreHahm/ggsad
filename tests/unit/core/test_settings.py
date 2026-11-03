"""The project settings file (schema 1.0, layout with a `roles` block)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ggsad.core.settings import build_context, gates_for, read_settings

GOOD: dict[str, Any] = {
    "schema_version": "1.0",
    "project": {"id": "my-project", "compliance_profile": "standard", "team_mode": "team"},
    "roles": {
        "owner": "human:ada",
        "approved_humans": [
            {"identity": "human:ada", "account": "ada-gh"},
            {"identity": "human:bo", "account": "bo-gh"},
        ],
        "deputies": ["human:bo"],
        "unavailable_approvers": [],
        "requestors": [{"identity": "agent:builder", "vendor": "vendor-a", "model": "model-x"}],
    },
    "defaults": {"retry_limit": 3, "fail_severity": "hard"},
    "minimum_levels": {"spec_approval": "A0", "gate_approval": "A1"},
}


def changed(path: list[str], value: object) -> dict[str, Any]:
    data = deepcopy(GOOD)
    target = data
    for key in path[:-1]:
        target = target[key]
    if value is ...:
        del target[path[-1]]
    else:
        target[path[-1]] = value
    return data


def test_a_good_file_is_read() -> None:
    settings, report = read_settings(GOOD)
    assert report.ok and settings is not None
    assert settings.owner == "human:ada" and settings.team_mode == "team"
    assert settings.approved_identities == {"human:ada", "human:bo"}
    assert settings.requestors[0].identity == "agent:builder"
    assert settings.minimum_levels == {"spec_approval": "A0", "gate_approval": "A1"}


def test_defaults_apply_when_sections_are_short() -> None:
    minimal = {
        "schema_version": "1.0",
        "project": {"id": "p", "compliance_profile": "lean"},
        "roles": {"owner": "human:ada"},
    }
    settings, report = read_settings(minimal)
    assert report.ok and settings is not None
    assert settings.team_mode == "team" and settings.retry_limit == 3
    assert settings.approved_humans is None and settings.approved_identities is None


@pytest.mark.parametrize(
    ("path", "value", "code"),
    [
        (["schema_version"], "0.1", "schema-version-unsupported"),
        (["schema_version"], ..., "schema-version-unsupported"),
        (["project", "compliance_profile"], "strict", "field-value-invalid"),
        (["project", "team_mode"], "pair", "field-value-invalid"),
        (["project", "id"], "", "field-missing"),
        (["roles", "owner"], "ada", "identity-invalid"),
        (["roles", "owner"], "human:", "identity-invalid"),
        (["roles", "approved_humans"], "all", "field-type-invalid"),
        (["roles", "approved_humans"], [{"identity": "human:ada"}], "field-missing"),
        (["roles", "deputies"], ["agent:x"], "identity-invalid"),
        (["roles", "deputies"], "human:bo", "field-type-invalid"),
        (["roles", "deputies"], ["human:eve"], "human-not-approved"),
        (["roles", "requestors"], [{"identity": "human:ada"}], "identity-invalid"),
        (["roles", "requestors"], [{"identity": "agent:x", "color": "red"}], "field-unknown"),
        (["roles", "extra"], 1, "field-unknown"),
        (["defaults", "retry_limit"], 4, "retry-limit-invalid"),
        (["defaults", "retry_limit"], -1, "retry-limit-invalid"),
        (["defaults", "retry_limit"], True, "retry-limit-invalid"),
        (["defaults", "fail_severity"], "medium", "field-value-invalid"),
        (["minimum_levels", "spec_approval"], "a1", "field-value-invalid"),
        (["minimum_levels", "magic"], "A0", "field-unknown"),
        (["extra"], 1, "field-unknown"),
        (["roles"], "x", "field-type-invalid"),
    ],
)
def test_invalid_files_are_refused(path: list[str], value: object, code: str) -> None:
    settings, report = read_settings(changed(path, value))
    assert settings is None and code in report.codes


def test_the_owner_must_be_approved_when_a_list_is_set() -> None:
    data = changed(["roles", "owner"], "human:zed")
    assert "owner-not-approved" in read_settings(data)[1].codes


def test_the_profile_regulated_needs_a_deputy() -> None:
    data = changed(["project", "compliance_profile"], "regulated")
    data["roles"]["deputies"] = []
    assert "deputy-required" in read_settings(data)[1].codes


def test_a_file_that_is_not_a_mapping_is_refused() -> None:
    assert read_settings(["x"])[0] is None
    assert read_settings(None)[1].codes == ("field-type-invalid",)


def test_build_context_takes_roles_from_the_change_definition() -> None:
    settings, _ = read_settings(GOOD)
    assert settings is not None
    definition = {"owner": "human:bo", "author": "human:ada", "agent_may_close": True}
    context = build_context(settings, definition, (), "C-1")
    assert (context.change_owner, context.approver, context.author) == (
        "human:bo",
        "human:bo",
        "human:ada",
    )
    assert context.owner == "human:ada" and context.agent_may_close
    assert context.requestors == {"agent:builder"} and context.deputies == {"human:bo"}
    assert context.minimum_levels["gate_approval"] == "A1"


@given(
    st.recursive(
        st.none() | st.booleans() | st.integers() | st.text(),
        lambda c: st.lists(c) | st.dictionaries(st.text(), c),
        max_leaves=10,
    )
)
def test_read_settings_never_raises(value: object) -> None:
    settings, report = read_settings(value)
    assert (settings is None) == (not report.ok)


def test_build_context_falls_back_to_the_change_owner_for_an_unapproved_approver() -> None:
    settings, _ = read_settings(GOOD)
    assert settings is not None
    away = build_context(settings, {"owner": "human:bo", "approver": "human:eve"}, (), "C-1")
    assert away.approver == "human:bo"
    named = build_context(settings, {"owner": "human:bo", "approver": "human:ada"}, (), "C-1")
    assert named.approver == "human:ada"


def test_the_interpreter_key_is_read_and_must_be_a_program_name() -> None:
    data = changed(["interpreter"], "rt-stable")
    settings, report = read_settings(data)
    assert report.ok and settings is not None and settings.interpreter == "rt-stable"
    plain, _ = read_settings(GOOD)
    assert plain is not None and plain.interpreter is None
    for bad in ("", 3, ["x"]):
        assert "field-type-invalid" in read_settings(changed(["interpreter"], bad))[1].codes


def test_gates_for_adds_the_requirements_and_the_default_retry_limit() -> None:
    settings, _ = read_settings(changed(["defaults", "retry_limit"], 2))
    assert settings is not None
    exit_map = {"satisfied": [0], "not_satisfied": [1]}
    gate = {"id": "t", "kind": "check", "command": ["x"], "exit_map": exit_map}
    evidence = {"command": ["y"], "exit_map": exit_map}
    definition = {
        "gates": {"fail": [], "wait": [], "done": [gate]},
        "requirements": [{"id": "R1", "evidence": [evidence]}],
    }
    by_id = {g.id: g for g in gates_for(settings, definition)}
    assert by_id["t#retry-limit"].limit == 2
    assert [r.id for r in by_id["incomplete-evidence"].requirements] == ["R1"]
