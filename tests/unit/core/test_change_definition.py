"""Change definition validation (Sections 5.3, 5.6, 23.1, 23.3, 24.1 to 24.9).

Tests are named after the acceptance example they exercise.
"""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from ggsad.core.change_definition import (
    ProjectContext,
    validate_for_gate_approval,
    validate_for_new,
)

if TYPE_CHECKING:
    from ggsad.core.issues import Report

CONTEXT = ProjectContext("standard", existing_ids=["Task-7"], closed_ids=["c-0"])
SENTENCE = "Users can reset a password"
EXIT_MAP = {"satisfied": [0], "not_satisfied": [1]}


def definition() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "id": "c-1",
        "method_profile": "core",
        "compliance_profile": "standard",
        "author": "human:ada",
        "owner": "human:ada",
        "approver": "human:bo",
        "goal": {"problem": "Resets are manual", "done_when": [SENTENCE], "non_goals": []},
        "scope": {"allow": ["lib/**"]},
        "requirements": [
            {
                "id": "R1",
                "text": "A user can reset a password",
                "examples": ["Given a user, when they reset, then a mail is sent"],
                "done_when": [SENTENCE],
                "evidence": [
                    {"command": ["run-tests", "--suite", "reset"], "exit_map": dict(EXIT_MAP)}
                ],
            }
        ],
        "gates": {"fail": [], "wait": [], "done": []},
    }


def new(data: object, context: ProjectContext = CONTEXT) -> Report:
    return validate_for_new(data, context)


def approval(data: object, context: ProjectContext = CONTEXT) -> Report:
    return validate_for_gate_approval(data, context)


def check_gate(gate_id: str = "tests-pass") -> dict[str, Any]:
    return {"id": gate_id, "kind": "check", "command": ["run-tests"], "exit_map": dict(EXIT_MAP)}


def test_a_valid_definition_is_accepted_at_creation_and_at_approval() -> None:
    assert new(definition()).ok
    assert approval(definition()).ok


def test_a_definition_that_is_not_a_mapping_is_rejected() -> None:
    assert new(["not", "a", "mapping"]).codes == ("definition-invalid",)


# --- identity, profiles, schema version (AE-001, AE-007, AE-008) ---


@pytest.mark.parametrize(
    ("identifier", "code"),
    [
        ("../x", "id-invalid"),
        ("a/b", "id-invalid"),
        ("task-7", "id-not-unique"),
        ("nul", "id-reserved"),
    ],
)
def test_ae_001_a_bad_identifier_rejects_the_definition(identifier: str, code: str) -> None:
    data = definition()
    data["id"] = identifier

    assert new(data).codes == (code,)


def test_ae_001_an_identifier_must_be_a_string() -> None:
    data = definition()
    data["id"] = 7

    assert new(data).codes == ("id-invalid",)


@pytest.mark.parametrize("value", ["full", "Core", " core", "core ", None])
def test_ae_007_only_the_exact_lowercase_core_is_a_method_profile(value: object) -> None:
    data = definition()
    data["method_profile"] = value

    assert "method-profile-invalid" in new(data).codes


def test_ae_008_the_compliance_profile_must_equal_the_projects() -> None:
    data = definition()
    data["compliance_profile"] = "lean"

    assert new(data).codes == ("compliance-profile-mismatch",)
    assert new(definition(), ProjectContext("lean")).codes == ("compliance-profile-mismatch",)


@pytest.mark.parametrize("version", ["0.1", "2.0", "1.00", "1", 1.0, None, "", "x.y"])
def test_an_unusable_schema_version_is_refused_and_nothing_else_is_reported(
    version: object,
) -> None:
    data = definition()
    data["schema_version"] = version

    assert new(data).codes == ("schema-version-unsupported",)


def test_required_fields_and_unknown_fields_are_reported() -> None:
    data = definition()
    del data["goal"]
    data["surprise"] = 1

    assert set(new(data).codes) == {"field-missing", "field-unknown"}


# --- roles (Section 3.11) ---


def test_author_and_owner_are_humans_and_approved_when_a_list_exists() -> None:
    data = definition()
    data["author"] = "agent:builder"
    assert new(data).codes == ("role-not-human",)

    unlisted = ProjectContext("standard", approved_humans=["human:bo"])
    assert new(definition(), unlisted).codes == ("human-not-approved", "human-not-approved")


def test_a_missing_or_unlisted_approver_falls_back_with_a_warning() -> None:
    data = definition()
    del data["approver"]
    report = new(data)
    assert report.ok
    assert [w.code for w in report.warnings] == ["approver-fallback"]

    unlisted = ProjectContext("standard", approved_humans=["human:ada"])
    report = new(definition(), unlisted)
    assert report.ok
    assert [w.code for w in report.warnings] == ["approver-fallback"]


def test_an_approver_that_is_not_a_human_is_rejected() -> None:
    data = definition()
    data["approver"] = "agent:x"

    assert new(data).codes == ("role-not-human",)


# --- follows ---


def test_follows_must_name_a_closed_change() -> None:
    closed = definition()
    closed["follows"] = "c-0"
    assert new(closed).ok

    for value in ("c-9", "../x", 3):
        data = definition()
        data["follows"] = value
        assert new(data).codes == ("follows-invalid",)


# --- goal ---


def test_goal_needs_problem_done_when_and_non_goals() -> None:
    data = definition()
    data["goal"] = {"problem": "", "done_when": [], "extra": 1}

    assert set(new(data).codes) == {"field-missing", "field-unknown", "field-type-invalid"}


def test_goal_must_be_a_mapping() -> None:
    data = definition()
    data["goal"] = "text"

    assert new(data).codes == ("field-type-invalid",)


# --- base gates (AE-002, AE-004, AE-005) ---


def test_ae_002_a_definition_that_removes_a_base_gate_is_rejected() -> None:
    data = definition()
    data["gates"]["not_applicable"] = ["incomplete-evidence"]

    report = new(data)

    assert report.codes == ("gate-weakened",)
    assert "incomplete-evidence" in report.issues[0].message
    assert "removed" in report.issues[0].message


def test_not_applicable_may_only_name_base_gates() -> None:
    data = definition()
    data["gates"]["not_applicable"] = ["lint"]

    assert new(data).codes == ("gate-unknown",)


def test_not_applicable_must_be_a_list_of_identifiers() -> None:
    data = definition()
    data["gates"]["not_applicable"] = "scope-violation"

    assert new(data).codes == ("field-type-invalid",)


def test_ae_004_a_strengthening_does_not_offset_a_later_weakening() -> None:
    data = definition()
    data["gates"]["done"] = [{"id": "review-ok", "kind": "sign-off"}]
    data["gates"]["fail"] = [
        {"id": "scope-violation", "severity": "soft", "condition": {"predicate": "scope-violation"}}
    ]

    report = new(data)

    assert report.codes == ("gate-weakened",)
    assert "severity lowered" in report.issues[0].message


def test_ae_005_the_weakening_is_checked_again_before_the_gates_are_approved() -> None:
    data = definition()
    assert new(data).ok
    data["gates"]["fail"] = [
        {"id": "scope-violation", "severity": "soft", "condition": {"predicate": "scope-violation"}}
    ]

    assert approval(data).codes == ("gate-weakened",)


def test_a_base_gate_listed_unchanged_is_a_duplicate_identifier() -> None:
    data = definition()
    data["gates"]["fail"] = [
        {"id": "scope-violation", "severity": "hard", "condition": {"predicate": "scope-violation"}}
    ]

    assert new(data).codes == ("gate-id-duplicate",)


@pytest.mark.parametrize(
    "gate",
    [
        {"id": "unanswered-question", "condition": {"predicate": "stale-spec-approval"}},
        {"id": "incomplete-evidence", "kind": "check", "command": ["x"]},
    ],
)
def test_a_base_gate_listed_in_a_different_form_is_weakened_whatever_its_condition(
    gate: dict[str, Any],
) -> None:
    data = definition()
    data["gates"]["wait" if "condition" in gate else "done"] = [gate]

    assert new(data).codes == ("gate-weakened",)


# --- gate lists (AE-016) ---


def test_ae_016_a_done_gate_of_an_unknown_kind_is_rejected() -> None:
    bad = definition()
    bad["gates"]["done"] = [{"id": "code-review", "kind": "peer"}]
    assert new(bad).codes == ("done-gate-kind-invalid",)

    good = definition()
    good["gates"]["done"] = [
        check_gate(),
        {"id": "legal-ok", "kind": "sign-off"},
        {"id": "code-review", "kind": "review"},
    ]
    assert new(good).ok


@pytest.mark.parametrize("kind", [None, ["check", "sign-off"], "Check", 3])
def test_a_done_gate_has_exactly_one_known_kind(kind: object) -> None:
    data = definition()
    data["gates"]["done"] = [{"id": "g", "kind": kind}]

    assert new(data).codes == ("done-gate-kind-invalid",)


def test_gate_identifiers_are_unique_across_the_three_lists() -> None:
    data = definition()
    data["gates"]["done"] = [check_gate("g")]
    data["gates"]["fail"] = [
        {"id": "g", "severity": "hard", "condition": {"command": ["x"], "exit_map": EXIT_MAP}}
    ]

    assert new(data).codes == ("gate-id-duplicate",)


def test_a_gate_is_a_mapping_with_an_id() -> None:
    data = definition()
    data["gates"]["done"] = ["text", {"kind": "review"}]

    assert new(data).codes == ("gate-invalid", "gate-invalid")


def test_the_gate_lists_are_required_lists() -> None:
    data = definition()
    del data["gates"]["wait"]
    data["gates"]["fail"] = "none"
    data["gates"]["extra"] = []

    assert set(new(data).codes) == {"field-missing", "field-type-invalid", "field-unknown"}


def test_gates_must_be_a_mapping() -> None:
    data = definition()
    data["gates"] = []

    assert new(data).codes == ("field-type-invalid",)


def test_unknown_members_of_a_gate_are_rejected() -> None:
    data = definition()
    data["gates"]["done"] = [{"id": "s", "kind": "sign-off", "color": "red"}]
    data["gates"]["wait"] = [
        {"id": "w", "severity": "soft", "condition": {"predicate": "unanswered-question"}}
    ]

    assert new(data).codes == ("gate-invalid", "gate-invalid")


# --- fail and wait conditions (Section 23.3) ---


def fail_gate(condition: object, severity: object = "hard") -> dict[str, Any]:
    return {"id": "f", "severity": severity, "condition": condition}


@pytest.mark.parametrize(
    "condition",
    [
        {},
        {"command": ["x"], "predicate": "scope-violation"},
        {"command": ["x"], "unknown": 1},
        {"predicate": "scope-violation", "exit_map": EXIT_MAP},
        {"predicate": "unanswered-question"},
        "scope-violation",
    ],
)
def test_a_condition_holds_exactly_one_valid_member(condition: object) -> None:
    data = definition()
    data["gates"]["fail"] = [fail_gate(condition)]

    assert new(data).codes == ("condition-invalid",)


def test_a_wait_gate_may_name_wait_predicates_but_not_a_retry_limit() -> None:
    ok = definition()
    ok["gates"]["wait"] = [{"id": "w", "condition": {"predicate": "stale-spec-approval"}}]
    assert new(ok).ok

    bad = definition()
    bad["gates"]["wait"] = [
        {"id": "w", "condition": {"retry_limit": {"gate": "t", "limit": 1}}},
        {"id": "p", "condition": {"predicate": "scope-violation"}},
    ]
    assert new(bad).codes == ("condition-invalid", "condition-invalid")


@pytest.mark.parametrize("severity", [None, "HARD", "medium", 1])
def test_a_fail_gate_needs_a_severity_in_exact_lowercase(severity: object) -> None:
    data = definition()
    data["gates"]["fail"] = [fail_gate({"predicate": "scope-violation"}, severity)]

    assert new(data).codes == ("severity-invalid",)


def test_a_command_condition_is_checked_at_approval() -> None:
    data = definition()
    data["gates"]["fail"] = [fail_gate({"command": ["leak-scan"]})]

    assert new(data).ok
    assert approval(data).codes == ("exit-map-invalid",)


# --- retry limits (Sections 24.2 and 24.7) ---


def retry_gate(target: str, limit: object, severity: str = "soft") -> dict[str, Any]:
    return {
        "id": "retry",
        "severity": severity,
        "condition": {"retry_limit": {"gate": target, "limit": limit}},
    }


def test_a_retry_limit_names_a_check_done_gate_of_the_same_change() -> None:
    ok = definition()
    ok["gates"]["done"] = [check_gate()]
    ok["gates"]["fail"] = [retry_gate("tests-pass", 2)]
    assert approval(ok).ok

    for target in ("missing", "legal-ok"):
        bad = definition()
        bad["gates"]["done"] = [check_gate(), {"id": "legal-ok", "kind": "sign-off"}]
        bad["gates"]["fail"] = [retry_gate(target, 2)]
        assert new(bad).codes == ("retry-limit-gate-invalid",)


def test_a_retry_limit_cannot_declare_the_severity_hard() -> None:
    data = definition()
    data["gates"]["done"] = [check_gate()]
    data["gates"]["fail"] = [retry_gate("tests-pass", 2, severity="hard")]

    assert new(data).codes == ("severity-invalid",)


@pytest.mark.parametrize("limit", [-1, 1.5, "3", None, True, 4])
def test_a_retry_limit_is_a_non_negative_integer_not_above_the_default(limit: object) -> None:
    data = definition()
    data["gates"]["done"] = [check_gate()]
    data["gates"]["fail"] = [retry_gate("tests-pass", limit)]

    assert new(data).ok
    assert approval(data).codes == ("retry-limit-invalid",)


def test_a_project_may_lower_the_default_retry_limit() -> None:
    data = definition()
    data["gates"]["done"] = [check_gate()]
    data["gates"]["fail"] = [retry_gate("tests-pass", 3)]

    assert approval(data, ProjectContext("standard", default_retry_limit=2)).codes == (
        "retry-limit-invalid",
    )


def test_a_retry_limit_holds_exactly_gate_and_limit() -> None:
    data = definition()
    data["gates"]["fail"] = [
        {"id": "r", "severity": "soft", "condition": {"retry_limit": {"gate": "t"}}},
        {"id": "s", "severity": "soft", "condition": {"retry_limit": {"gate": "", "limit": 1}}},
    ]

    assert set(new(data).codes) == {"condition-invalid", "retry-limit-gate-invalid"}


# --- commands, exit maps, time limits (Section 24.2) ---


def test_a_check_gate_needs_a_command_and_an_exit_map_at_approval() -> None:
    data = definition()
    data["gates"]["done"] = [{"id": "t", "kind": "check"}]

    assert new(data).ok
    assert approval(data).codes == ("command-missing",)

    data["gates"]["done"] = [{"id": "t", "kind": "check", "command": ["x"]}]
    assert approval(data).codes == ("exit-map-invalid",)


@pytest.mark.parametrize("command", [[], "run-tests", ["", "x"], [1]])
def test_a_command_is_a_non_empty_argument_list(command: object) -> None:
    data = definition()
    data["gates"]["done"] = [{"id": "t", "kind": "check", "command": command}]

    assert new(data).codes == ("command-invalid",)


@pytest.mark.parametrize(
    "exit_map",
    [
        "zero",
        {"satisfied": [0]},
        {"satisfied": [0], "not_satisfied": [0]},
        {"satisfied": [0], "not_satisfied": [-1]},
        {"satisfied": [0], "not_satisfied": [1], "weird": [2]},
        {"satisfied": [0], "not_satisfied": [1], "not_evaluable": [1]},
        {"satisfied": [0], "not_satisfied": ["x"]},
    ],
)
def test_an_exit_map_maps_each_status_at_most_once(exit_map: object) -> None:
    data = definition()
    data["gates"]["done"] = [{**check_gate(), "exit_map": exit_map}]

    assert "exit-map-invalid" in new(data).codes


def test_an_exit_map_may_map_not_evaluable_statuses() -> None:
    data = definition()
    data["gates"]["done"] = [
        {**check_gate(), "exit_map": {"satisfied": [0], "not_satisfied": [1], "not_evaluable": [2]}}
    ]

    assert approval(data).ok


@pytest.mark.parametrize("limit", [0, -5, "10", True])
def test_a_time_limit_is_a_positive_integer(limit: object) -> None:
    data = definition()
    data["gates"]["done"] = [{**check_gate(), "time_limit": limit}]

    assert new(data).codes == ("time-limit-invalid",)


def test_a_sign_off_minimum_level_is_a_known_level() -> None:
    ok = definition()
    ok["gates"]["done"] = [{"id": "s", "kind": "sign-off", "minimum_level": "A2"}]
    assert new(ok).ok

    bad = definition()
    bad["gates"]["done"] = [{"id": "s", "kind": "sign-off", "minimum_level": "A9"}]
    assert new(bad).codes == ("level-invalid",)


# --- baselines (Section 24.6) ---


def baseline_gate(baseline: object, kind: str = "check") -> dict[str, Any]:
    gate = check_gate() if kind == "check" else {"id": "g", "kind": kind}
    gate["baseline"] = baseline
    return gate


def test_a_baseline_entry_carries_a_reason_and_a_review_date() -> None:
    data = definition()
    entry = {"id": "t1", "reason": "flaky on CI", "review_by": "2026-12-01"}
    data["gates"]["done"] = [baseline_gate([entry])]
    assert approval(data).ok

    entry["review_by"] = date(2026, 12, 1)
    assert approval(data).ok


@pytest.mark.parametrize(
    "baseline",
    [
        "t1",
        ["t1"],
        [{"id": "t1", "reason": "r"}],
        [{"id": "t1", "reason": "", "review_by": "2026-12-01"}],
        [{"id": "t1", "reason": "r", "review_by": "soon"}],
        [{"id": "t1", "reason": "r", "review_by": 5}],
    ],
)
def test_an_invalid_baseline_is_rejected_at_approval(baseline: object) -> None:
    data = definition()
    data["gates"]["done"] = [baseline_gate(baseline)]

    assert new(data).ok
    assert "baseline-invalid" in approval(data).codes


def test_a_baseline_is_valid_only_on_a_check_gate() -> None:
    data = definition()
    entry = {"id": "t1", "reason": "r", "review_by": "2026-12-01"}
    data["gates"]["done"] = [baseline_gate([entry], kind="sign-off")]

    assert approval(data).codes == ("baseline-invalid",)


# --- scope (Section 24.5) ---


def test_the_scope_is_required_for_approval_and_holds_only_allow() -> None:
    data = definition()
    del data["scope"]
    assert new(data).ok
    assert approval(data).codes == ("scope-absent",)

    data["scope"] = {"allow": ["lib/**"], "deny": []}
    assert new(data).codes == ("field-type-invalid",)


@pytest.mark.parametrize("pattern", ["", "/etc", "a/../b", "..", 3])
def test_a_path_pattern_is_checked_at_approval(pattern: object) -> None:
    data = definition()
    data["scope"] = {"allow": [pattern]}

    assert new(data).ok
    assert approval(data).codes == ("scope-pattern-invalid",)


def test_an_empty_allowed_path_list_is_valid() -> None:
    data = definition()
    data["scope"] = {"allow": []}

    assert approval(data).ok


# --- gates absent (AE-037) ---


def test_ae_037_absent_gate_definitions_cannot_be_approved() -> None:
    data = definition()
    del data["gates"]

    assert new(data).ok
    assert approval(data).codes == ("gates-absent",)


# --- requirements and done_when coverage (AE-315, Sections 23.1 and 24.9) ---


def test_ae_315_a_done_when_sentence_without_evidence_refuses_the_approval() -> None:
    data = definition()
    data["goal"]["done_when"] = [SENTENCE, "Resets are logged"]

    assert new(data).ok
    report = approval(data)
    assert report.codes == ("done-when-uncovered",)
    assert "Resets are logged" in report.issues[0].message
    assert SENTENCE not in report.issues[0].message


def test_a_requirement_without_an_evidence_command_does_not_cover_its_sentence() -> None:
    data = definition()
    data["requirements"][0]["evidence"] = []

    assert approval(data).codes == ("done-when-uncovered",)


def test_a_human_check_covers_a_sentence_through_a_sign_off_gate() -> None:
    data = definition()
    data["requirements"][0]["evidence"] = []
    data["requirements"][0]["human_check"] = {"reason": "no command judges tone", "gate": "page-ok"}
    data["gates"]["done"] = [{"id": "page-ok", "kind": "sign-off"}]

    assert approval(data).ok


def test_a_human_check_must_name_a_sign_off_gate_at_approval() -> None:
    data = definition()
    data["requirements"][0]["human_check"] = {"reason": "r", "gate": "nope"}

    assert new(data).ok
    assert approval(data).codes == ("human-check-invalid",)


@pytest.mark.parametrize("check", ["text", {"reason": "r"}, {"reason": "", "gate": "g"}])
def test_a_human_check_holds_a_reason_and_a_gate(check: object) -> None:
    data = definition()
    data["requirements"][0]["human_check"] = check

    assert new(data).codes == ("human-check-invalid",)


def test_requirement_shape_errors_are_reported() -> None:
    data = definition()
    data["requirements"] = [
        "text",
        {"id": "R1", "text": "x", "color": 1},
        {"id": "R1", "text": "dup", "done_when": ["not a goal sentence"]},
        {"id": "", "text": "no id"},
        {"id": "R9", "text": "y", "done_when": "oops", "evidence": "oops"},
        {"id": "R8", "text": "z", "evidence": [{"nothing": 1}, "x"]},
    ]

    assert set(new(data).codes) == {
        "requirement-invalid",
        "requirement-id-duplicate",
        "done-when-unknown",
    }


def test_requirements_must_be_a_list() -> None:
    data = definition()
    data["requirements"] = {"id": "R1"}

    assert new(data).codes == ("field-type-invalid",)


def test_optional_fields_have_types() -> None:
    data = definition()
    data["required_tools"] = "scan"
    data["agent_may_close"] = "yes"

    assert new(data).codes == ("field-type-invalid", "field-type-invalid")

    good = definition()
    good["required_tools"] = ["scan", "lintx"]
    good["agent_may_close"] = True
    assert new(good).ok


def test_approval_ignores_the_changes_own_identifier_when_checking_uniqueness() -> None:
    context = ProjectContext("standard", existing_ids=["c-1", "C-2"])

    assert new(definition(), context).codes == ("id-not-unique",)
    assert approval(definition(), context).ok


def test_a_missing_field_is_reported_once_and_does_not_cascade() -> None:
    for name in ("id", "author", "requirements"):
        data = definition()
        del data[name]

        assert new(data).codes == ("field-missing",)


def test_goal_details_are_checked() -> None:
    data = definition()
    data["goal"] = {"problem": "p", "non_goals": "none"}

    assert set(new(data).codes) == {"field-missing", "field-type-invalid"}


# --- an explicit null is never "absent" (Codex finding on goal: null) ---


@pytest.mark.parametrize("field", ["goal", "requirements", "gates", "scope"])
def test_a_null_body_field_is_rejected_at_creation_and_at_approval(field: str) -> None:
    data = definition()
    data[field] = None

    assert not new(data).ok
    assert not approval(data).ok


def test_a_null_goal_cannot_skip_the_done_when_coverage_check() -> None:
    data = definition()
    data["goal"] = None

    assert new(data).codes == ("field-type-invalid",)
    assert "field-type-invalid" in approval(data).codes


@pytest.mark.parametrize(
    "mutate",
    [
        lambda d: d["gates"].__setitem__("not_applicable", None),
        lambda d: d["gates"].__setitem__("done", [{**check_gate(), "command": None}]),
        lambda d: d["gates"].__setitem__(
            "done", [{"id": "s", "kind": "sign-off", "minimum_level": None}]
        ),
        lambda d: d["requirements"][0].__setitem__("human_check", None),
        lambda d: d["requirements"][0].__setitem__("evidence", None),
        lambda d: d["requirements"][0].__setitem__("done_when", None),
    ],
)
def test_an_explicit_null_in_an_optional_member_is_rejected(mutate: Any) -> None:
    data = definition()
    mutate(data)

    assert not new(data).ok


# --- list and mapping values never crash a membership test (Codex finding) ---


@pytest.mark.parametrize("value", [[], {}, ["hard"], {"a": 1}, 3, None])
def test_an_unhashable_or_non_string_enum_value_is_an_issue_not_an_exception(
    value: object,
) -> None:
    data = definition()
    data["gates"]["fail"] = [fail_gate({"predicate": "scope-violation"}, value)]
    assert new(data).codes == ("severity-invalid",)

    data = definition()
    data["gates"]["fail"] = [fail_gate({"predicate": value})]
    assert new(data).codes == ("condition-invalid",)

    data = definition()
    data["gates"]["wait"] = [{"id": "w", "condition": {"predicate": value}}]
    assert new(data).codes == ("condition-invalid",)

    data = definition()
    data["gates"]["done"] = [{"id": "s", "kind": "sign-off", "minimum_level": value}]
    assert new(data).codes == ("level-invalid",)

    data = definition()
    data["gates"]["done"] = [{"id": "g", "kind": value}]
    assert new(data).codes == ("done-gate-kind-invalid",)


# --- no input makes a validator raise ---

_LEAF = (
    st.none()
    | st.booleans()
    | st.integers(-5, 5)
    | st.floats(allow_nan=False)
    | st.text(max_size=6)
)
_VALUES = st.recursive(
    _LEAF,
    lambda inner: (
        st.lists(inner, max_size=3) | st.dictionaries(st.text(max_size=5), inner, max_size=3)
    ),
    max_leaves=6,
)
_PATHS = [
    ("goal",),
    ("goal", "done_when"),
    ("scope",),
    ("scope", "allow"),
    ("requirements",),
    ("requirements", 0),
    ("requirements", 0, "evidence"),
    ("requirements", 0, "human_check"),
    ("gates",),
    ("gates", "fail"),
    ("gates", "wait"),
    ("gates", "done"),
    ("gates", "not_applicable"),
    ("follows",),
    ("approver",),
    ("required_tools",),
    ("agent_may_close",),
    ("id",),
    ("author",),
]


def replace_at(data: dict[str, Any], path: tuple[object, ...], value: object) -> None:
    target: Any = data
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


@given(path=st.sampled_from(_PATHS), value=_VALUES, gate=_VALUES)
def test_no_input_makes_a_validator_raise(
    path: tuple[object, ...], value: object, gate: object
) -> None:
    data = definition()
    data["gates"]["fail"] = [gate]
    data["gates"]["done"] = [gate]
    replace_at(data, path, value)

    assert isinstance(new(data).issues, tuple)
    assert isinstance(approval(data).issues, tuple)


def test_an_extraction_rule_is_a_pattern_with_one_capture_group_and_a_stream() -> None:
    data = definition()
    gate = check_gate()
    gate["extract"] = {"pattern": r"^FAILED (\S+)", "stream": "both"}
    data["gates"]["done"] = [gate]
    assert approval(data).ok
    gate["extract"] = {"pattern": r"^FAILED (\S+)"}
    assert approval(data).ok


@pytest.mark.parametrize(
    "rule",
    [
        "x",
        {},
        {"pattern": r"FAILED \S+"},
        {"pattern": r"(a)(b)"},
        {"pattern": "("},
        {"pattern": r"(\S+)", "stream": "none"},
        {"pattern": r"(\S+)", "color": "red"},
    ],
)
def test_an_invalid_extraction_rule_is_rejected_at_approval(rule: object) -> None:
    data = definition()
    gate = check_gate()
    gate["extract"] = rule
    data["gates"]["done"] = [gate]
    assert "extract-invalid" in approval(data).codes
