# Implementation Checklist: CHG-001 — Reference Repository Bootstrap

## Metadata

- Change ID: CHG-001
- Status: Active
- Phase: build
- Owner: agent:claude-code
- Reviewer: agent:codex
- Decision Owner: human:project-owner
- Last Updated: 2026-08-03
- Specification: `spec.md`
- Plan: `plan.md`
- State: `state.yaml`
- Evidence: `evidence.md`
- Review ID: PR-001

## Usage Rules

- This checklist is an execution aid, not the source of truth for requirements or architecture.
- Every task MUST map to the approved specification or implementation plan.
- Tasks MUST NOT expand CHG-001 scope.
- Claude Code acts as the implementation Requestor.
- Codex acts as the distinct Pair Reviewer.
- Codex MUST return findings to Claude Code and MUST NOT silently modify the reviewed work product.
- A task may be marked complete only when its stated verification has succeeded.
- Blocked tasks MUST be represented through the applicable GG-SAD wait or fail behavior.
- GSD `.planning/` tasks remain subordinate to this checklist and the approved GG-SAD plan.

## Status Legend

- `[ ]` Not started
- `[-]` In progress
- `[x]` Complete
- `[!]` Waiting or blocked
- `[~]` Superseded or not applicable with recorded rationale

## 1. Governance and Readiness

- [x] **T-001 — Record ADR disposition**
  - Maps To: CHG-001 Ready-to-Build
  - Artifacts: `docs/adr/ADR-0001-*.md` through `ADR-0008-*.md`
  - Owner: human:project-owner
  - Verification: Every ADR is accepted, rejected, or explicitly recorded as non-blocking.
  - Evidence: Recorded 2026-08-02 in `spec.md` (Q-001, Dependencies and Prerequisites, Constraints)
    and `plan.md` (§2, §23); ADRs' individual `Status: Proposed` unchanged — this is a
    CHG-001-scoped non-blocking disposition, not ADR acceptance.

- [x] **T-002 — Approve CHG-001 specification**
  - Maps To: Specification approval
  - Artifact: `spec.md`
  - Owner: human:project-owner
  - Verification: Approval status and evidence are recorded.
  - Evidence: `spec.md` § Approval — Approval Status: Approved (2026-08-02)

- [x] **T-003 — Resolve specification open questions**
  - Maps To: Q-001, Q-003, Q-004, Q-005
  - Owner: human:project-owner
  - Verification: No blocking question remains open.
  - Evidence: `spec.md` § Open Questions — all four rows marked Resolved (2026-08-02)

- [x] **T-004 — Approve or explicitly accept implementation plan**
  - Maps To: Ready-to-Build
  - Artifact: `plan.md`
  - Owner: human:project-owner
  - Verification: Plan approval status is recorded.
  - Evidence: `plan.md` §25 — Status: Approved (2026-08-02)

- [x] **T-005 — Assign distinct Pair Reviewer**
  - Maps To: Pair Review policy
  - Requestor: agent:claude-code
  - Reviewer: agent:codex
  - Verification: Requestor and Reviewer identities differ.
  - Evidence: `spec.md`, `plan.md`, and this checklist

- [x] **T-006 — Validate baseline governed artifacts**
  - Maps To: Ready-to-Build
  - Artifacts:
    - `.ggsad/config.yaml`
    - `.ggsad/mappings/gsd.yaml`
    - `.ggsad/schemas/config.schema.json`
    - `.ggsad/schemas/mappings.schema.json`
    - `.ggsad/schemas/state.schema.json`
    - `state.yaml`
  - Verification: All artifacts validate with no blocking error.
  - Evidence: Verified 2026-08-02 with an ad hoc `jsonschema` Draft 2020-12 check (not production
    code) over all three YAML/schema pairs. `.ggsad/schemas/mapping.schema.json` was renamed to
    `mappings.schema.json` to match its own `$id` and all referencing documents. CHG-001
    `state.yaml`'s `wait` block was missing the schema-required `category`/`safe_state`/
    `next_action` keys; added as `null` (status is `draft`, not `waiting`, so no wait metadata was
    actually needed). All three now validate. Formal `evidence.md` capture deferred to Slice 7 per
    plan.md §14.

- [x] **T-007 — Inspect repository and GSD state**
  - Maps To: AGENTS.md and CLAUDE.md startup rules
  - Commands:
    ```bash
    git status --short --branch
    git diff --stat
    git diff --cached --stat
    ```
  - Verification: Unexpected files, conflicts, and scope violations are resolved or reported.
  - Evidence: Verified 2026-08-02 — no commits yet on `main`, all files untracked, no diffs to
    reconcile. No unexpected state found.

## 2. Slice 1 — Package and Resource Baseline

- [x] **T-010 — Confirm Python project configuration**
  - Maps To: R-019
  - Files: `pyproject.toml`
  - Verification:
    ```bash
    uv sync
    uv build
    ```
  - Evidence: `uv sync` resolved/audited 44 packages; `uv build` produced `ggsad-0.1.0.tar.gz`
    and `ggsad-0.1.0-py3-none-any.whl` (2026-08-02). Also added `[tool.ruff] extend-exclude` for
    `.claude`, `.codex`, `.ggsad`, `.github`, `.idea`, `.qodo`, `docs`, `examples`, `scripts`,
    `specs` — `ruff format --check .` was reformatting Python fences inside GSD's own bundled
    markdown docs, outside CHG-001 scope. Full `evidence.md` capture deferred to Slice 7.

- [x] **T-011 — Create the minimal package and CLI entry point**
  - Maps To: R-001, R-003, R-005, R-010, R-015
  - Files:
    - `src/ggsad/__init__.py`
    - `src/ggsad/cli.py`
  - Expected Result: `ggsad --help` executes successfully.
  - Verification:
    ```bash
    uv run ggsad --help
    ```
  - Evidence: exit code 0, usage banner printed; `ggsad --version` also verified (exit 0,
    prints `ggsad 0.1.0`). No subcommands implemented yet (init/new/validate/transition land in
    Slices 3-6 per plan.md's Implementation Sequence).

- [x] **T-012 — Package schemas, templates, profiles, and mappings**
  - Maps To: R-001, R-003, R-005, R-006, R-007
  - Files: `src/ggsad/resources/` or approved equivalent
  - Verification: Resource-loading tests pass.
  - Constraint: Do not create an unused generic plugin framework.
  - Evidence: `src/ggsad/resources/{schemas,templates,mappings}/` populated from `.ggsad/`;
    confirmed present in the built wheel via `zipfile -l`. Default compliance-profile assets
    (`.ggsad/profiles/` is currently empty — only `.gitkeep`) are deferred to Slice 3, where
    `ggsad init` first needs to decide their content; nothing exists yet to package. The empty
    placeholder module directories (`adapters/`, `engine/`, `mappings/`, `models/`, `profiles/`,
    `templates/`, `validators/` under `src/ggsad/`) were removed — they held only `.gitkeep`, and
    `plan.md` §6 explicitly warns against empty abstraction layers; they'll be recreated in the
    slice that first needs them.

- [x] **T-013 — Add resource-loading tests**
  - Maps To: R-001, R-003
  - Files: `tests/unit/`, `tests/integration/`
  - Verification:
    ```bash
    uv run pytest <resource-test-paths>
    ```
  - Evidence: `tests/unit/test_version.py`, `tests/unit/test_cli.py`,
    `tests/integration/test_resource_loading.py` added. Full suite: 7 passed, 100% coverage on
    `src/ggsad` (threshold 85%). `ruff format --check .`, `ruff check .`, and `ty check` all pass
    with 0 issues. `bandit -r src/ggsad`: no issues identified. Slice 1's reviewable outcome
    ("`ggsad --help` works and packaged assets are available") is met.

## 3. Slice 2 — Safe YAML and Schema Validation

- [x] **T-020 — Implement safe YAML loading**
  - Maps To: R-005, R-006, R-007, R-015
  - Files: `src/ggsad/validators/yaml_loader.py` or approved equivalent
  - Requirements:
    - safe loading only;
    - clear file context;
    - no arbitrary object construction.
  - Verification: invalid-YAML and safety tests pass.
  - Evidence: `YAML(typ="safe")` (ruamel) rejects `!!python/object/apply:...` tags;
    `YamlLoadError` carries path/line/column. `tests/unit/test_yaml_loader.py` (6 tests,
    including an unsafe-tag rejection test).

- [x] **T-021 — Implement JSON Schema validation**
  - Maps To: R-005, R-006, R-007
  - Files: `src/ggsad/validators/schema_validator.py`
  - Verification: valid and invalid fixtures produce deterministic results.
  - Evidence: Draft 2020-12 validation via `jsonschema`, returns all violations (not just the
    first) as normalized `ValidationIssue`s. `tests/unit/test_schema_validator.py` (4 tests).

- [x] **T-022 — Implement typed configuration, mapping, and state models**
  - Maps To: R-005, R-006, R-007, R-014
  - Files: `src/ggsad/models/`
  - Verification:
    ```bash
    uv run mypy
    uv run pytest <model-test-paths>
    ```
  - Evidence: `ProjectConfig`, `IntegrationMapping`, `ChangeState` (Pydantic v2, frozen). Ran
    `uv run ty check` instead of `uv run mypy` — `mypy` is referenced by the constitution and
    spec's baseline commands, but `pyproject.toml`'s dev dependencies only install `ty`; flagged
    to the Requestor, not resolved here (a docs-vs-tooling decision, not a Slice 2 task).
    `history` on `ChangeState` is fully typed (`list[HistoryEvent]`) for the Slice 6 transition
    engine's use. `tests/unit/test_models_{config,mapping,state}.py` (6 tests).

- [x] **T-023 — Add normalized validation issues**
  - Maps To: R-015
  - Required Fields:
    - category;
    - file;
    - path or field;
    - concise reason;
    - remediation hint where determinable.
  - Verification: CLI error-output tests pass.
  - Evidence: `ValidationIssue` (frozen Pydantic model) in `src/ggsad/models/validation.py`,
    with all five fields and a `__str__` used by every validator in this slice.
    `tests/unit/test_validation_issue.py` (3 tests). CLI wiring (actual command output) lands in
    Slice 5 when `ggsad validate` exists — this task covers the model, not the command.

- [x] **T-024 — Test config, mapping, and state validation**
  - Maps To: E-005, E-007 (see note on E-006/E-008 below)
  - Verification: all referenced acceptance tests pass.
  - Evidence: `tests/integration/test_governed_artifact_validation.py` — E-005 (invalid YAML
    rejected with file+location) and E-007 (`may_approve: true` structurally schema-valid but
    rejected by `mapping_authority.py` as a business-rule violation) both pass. The same file
    also validates this repository's own `.ggsad/config.yaml`, `.ggsad/mappings/gsd.yaml`, and
    CHG-001's `state.yaml` end-to-end (load → schema → typed model), replacing the ad hoc script
    used to verify them earlier in this change.
  - **Scoping correction:** E-006 (unknown compliance profile) and E-008 (missing Class M
    artifact file) are **not** achievable by per-file schema/YAML validation alone — a JSON
    Schema cannot know which profile files or which sibling artifact files exist on disk. Both
    require the repository-level, filesystem-aware checks that `plan.md`'s own Slice 5 already
    scopes ("Compose config, mapping, state, artifact, and placeholder checks"). Moved to
    Slice 5's T-050/T-052 rather than force-fit here. R-005 through R-008 remain fully in scope;
    only their *sequencing* across slices is corrected — this is a `tasks.md` tracking fix
    (execution aid), not a change to `spec.md`/`plan.md`.

## 4. Slice 3 — Repository Initialization

- [x] **T-030 — Define the generated asset manifest**
  - Maps To: R-001
  - Verification: Manifest contains only approved CHG-001 assets.
  - Constraint: Exclude CI, memory, MCP, web UI, and orchestration assets.
  - Evidence: `build_asset_manifest()` in `src/ggsad/application/initialize_project.py`. 18
    entries: `.ggsad/config.yaml` (rendered, schema-valid defaults, `operating_mode: stand-alone`
    — no automatic GSD install, per spec.md's excluded-scope list), 3 packaged schemas, 10
    packaged templates, and the 4 project-level docs with a clean 1:1 template mapping
    (constitution, project-brief, architecture, roadmap). Deliberately excludes `docs/adr/`
    (per-decision, not templated) and `docs/definitions/` (4 documents from 1 generic template,
    no CHG-001 command to disambiguate) — see the T-024 scoping note above for the same reasoning
    pattern.

- [x] **T-031 — Implement initialization preflight**
  - Maps To: R-001, R-002, R-012
  - Required Behavior:
    - identify files to create;
    - classify identical existing files as unchanged;
    - classify differing existing files as conflicts;
    - perform no writes when conflicts exist.
  - Verification: preflight unit tests pass.
  - Evidence: `preflight()` classifies every manifest path before any write. Confirmed via test
    that a conflict on `docs/constitution.md` blocks writes to *every other* manifest path too
    (not just the conflicting one) — R-012's "no partial mutation" read literally.

- [x] **T-032 — Implement conservative idempotent initialization**
  - Maps To: R-001, R-002
  - Verification: E-001 and E-002 pass.
  - Constraint: No overwrite flag in CHG-001.
  - Evidence: `initialize_project()`. No `--overwrite`/`--force` flag exists on `ggsad init`.
    Verified end-to-end (not just in tests): ran `ggsad init` against a real temp directory
    (18 files created), re-ran it (all 18 reported `unchanged`, nothing rewritten).

- [x] **T-033 — Add initialization acceptance tests**
  - Maps To: E-001, E-002
  - Verification:
    ```bash
    uv run pytest <initialization-acceptance-tests>
    ```
  - Evidence: `tests/acceptance/test_init_acceptance.py` — E-001 (clean init succeeds, all
    approved files present) and E-002 (modified `docs/constitution.md` → exit non-zero,
    actionable conflict message, that file byte-for-byte unchanged, an unrelated sentinel file
    untouched, and no `.ggsad/` written at all) both pass via `CliRunner`. 50 tests total,
    99.5% coverage (remaining gap is a defensive branch for a resource-subdirectory case that
    can't occur with the current packaged resources — not worth a contrived fixture). ruff/ty/
    bandit/build all pass.

## 5. Slice 4 — Class M Change Creation

- [x] **T-040 — Implement change-ID validation**
  - Maps To: R-004
  - Accepted Form: `CHG-<three-or-more-digits>`
  - Verification: parameterized and property-based tests pass.
  - Evidence: `validate_change_id()` in `src/ggsad/application/create_change.py`, pattern
    `^CHG-\d{3,}$`. Parameterized tests (valid/invalid cases including the E-004 traversal
    string) plus a Hypothesis property test over arbitrary digit counts.

- [x] **T-041 — Implement slug validation and path containment**
  - Maps To: R-004, R-012
  - Verification:
    - unsafe slugs are rejected;
    - generated paths remain under `specs/`;
    - E-004 passes.
  - Evidence: `validate_slug()` (pattern `^[a-z0-9]+(?:-[a-z0-9]+)*$`) and
    `resolve_change_directory()`, which verifies the resolved path's parent is exactly
    `specs/` (defense in depth — the regexes already exclude `/` and `..`, so this checks
    containment rather than assuming it). E-004 passes.

- [x] **T-042 — Render the five required Class M artifacts**
  - Maps To: R-003, R-008
  - Generated Files:
    - `state.yaml`
    - `spec.md`
    - `plan.md`
    - `tasks.md`
    - `evidence.md`
  - Verification: generated artifacts exist and state validates.
  - Evidence: `build_change_manifest()`. `state.yaml` is constructed through the typed
    `ChangeState` model (Slice 2), not hand-formatted — correct by construction against
    `state.schema.json`. Found and fixed a real serialization bug during this work: naive
    `model_dump()` renders unset-optional fields as `null` even where the schema types them
    `array`-only (`failure.evidence`, `history[].action`, `goal.success_signals`, etc.), which
    fails validation; a `_dump_change_state()` helper now uses `exclude_none=True` and
    selectively restores the handful of fields the schema requires present-as-null (`wait.*`,
    `failure.reason`/`category`, `pair_review.requestor`/`reviewer`). spec/plan/tasks/evidence
    copied verbatim from their templates, same pattern as `docs/` in Slice 3.

- [x] **T-043 — Add Class M creation acceptance tests**
  - Maps To: E-003, E-004
  - Verification:
    ```bash
    uv run pytest <change-creation-acceptance-tests>
    ```
  - Evidence: `tests/acceptance/test_new_acceptance.py` — E-003 and E-004 both pass. Also found
    and fixed a real, non-hypothetical bug while writing these tests: two `new` calls within the
    same wall-clock second render byte-identical `state.yaml` (second-precision timestamp), which
    made my first conflict-detection design non-deterministic (passed or failed depending on
    timing). Fixed by checking the change directory's existence explicitly
    (`ChangeAlreadyExistsError`) rather than relying on byte comparison for this case — verified
    deterministic across repeated runs, and end-to-end against a real temp directory (create,
    reject re-creation, reject an E-004-style invalid ID). 83 tests, 98.45% coverage; ruff/ty/
    bandit/build all pass.

## 6. Slice 5 — Repository and Document Validation

- [x] **T-050 — Implement required-artifact validation**
  - Maps To: R-008
  - Verification: Every missing Class M artifact is reported explicitly.
  - Note (moved here from Slice 2 T-024, 2026-08-03): also covers E-008 (missing Class M
    artifact file) — requires filesystem-aware checks a per-file schema/YAML validator can't do.
  - Evidence: `validators/artifact_presence.py`. E-008 passes: a missing `plan.md` is reported
    with the change directory and the exact file name.

- [x] **T-051 — Implement approved placeholder detection**
  - Maps To: R-009
  - Constraint: Detect only repository-approved placeholder forms.
  - Verification: E-009 passes without false positives in approved code examples.
  - Evidence: `validators/placeholder_detector.py`. Found and fixed a real false-positive bug
    while validating this repo's own `spec.md`/`plan.md` against the new detector: it only
    stripped triple-backtick fenced blocks, not inline single-backtick code spans, so prose
    like `` `specs/<change-id>-<slug>/` `` (illustrating a path pattern) was flagged. Confirmed
    against the packaged templates that every genuine placeholder is bare, never
    backtick-wrapped, then fixed the detector to also strip inline spans — re-validating this
    repo's own CHG-001 artifacts now correctly finds only the genuine gap (missing
    `evidence.md`, expected until Slice 7), zero false positives. Scoped to `spec.md`/`plan.md`
    only (mirroring R-011's exact wording), not the whole change directory or `docs/` — a
    freshly `init`ed project's docs are expected to still contain placeholders. E-009 itself
    (transition rejection) is exercised in Slice 6, which reuses this same detector.

- [x] **T-052 — Implement repository-level validation aggregation**
  - Maps To: R-005–R-009, R-015
  - Expected Result: `ggsad validate` reports all relevant blocking issues coherently.
  - Note (moved here from Slice 2 T-024, 2026-08-03): also covers E-006 (unknown compliance
    profile) — requires checking the configured profile against the registered profile set,
    which is repository-level context, not per-file schema validation.
  - Evidence: `application/validate_repository.py` composes config (schema + `validators/
    compliance_profile.py`), declared mappings (schema + authority), and per-change (artifacts +
    state schema + placeholders) checks into one flat, ordered `list[ValidationIssue]`. Wired
    into `ggsad validate [TARGET] [--change ID] [--format text|json]`. `--format json` dumps
    structured issues (spec.md's "machine-actionable error output," not left as a nice-to-have).
    `--change` scopes to one change without scanning `specs/examples/`.

- [x] **T-053 — Implement stand-alone validation**
  - Maps To: R-016
  - Verification: No GSD, Claude Code, GitHub, IDE, network, or CI dependency is imported or required.
  - Evidence: `tests/integration/test_standalone_operation.py` — AST-scans every `src/ggsad/*.py`
    file for forbidden imports, checks `pyproject.toml`'s actual dependency lists (not the whole
    file — it legitimately mentions `.claude`/`.github` as `ruff` `extend-exclude` paths, which a
    naive substring test initially flagged as a false positive), and runs a real `init` →
    `validate` → `new` workflow with `operating_mode: stand-alone` and zero integrations.

- [x] **T-054 — Validate the complete Class M example**
  - Maps To: R-018, E-013
  - Files: `specs/examples/class-m/`
  - Verification: example passes and is marked non-active.
  - Evidence: Authored a genuinely complete, non-placeholder Class M example (`CHG-000`, "Add a
    `--quiet` flag to `ggsad validate`") — all 5 artifacts filled in, not template boilerplate.
    `evidence.md` honestly reports every gate as "Not Run"/"Not Applicable" per the constitution's
    rule against reporting unexecuted checks as passed. `validate_change()` on this directory
    returns zero issues. Marked non-active per R-018: lives under `specs/examples/`, one level
    deeper than real changes, so `discover_change_directories()` never picks it up, and
    `--change CHG-000` finds no match — verified both in the test and manually.

## 7. Slice 6 — Controlled Draft-to-Ready Transition

- [x] **T-060 — Implement the explicit transition rule**
  - Maps To: R-010, R-011
  - Supported Source: `specify/draft`
  - Supported Target: `specify/ready`
  - Constraint: No general status editor.
  - Evidence: `engine/transitions.py`. `ggsad transition CHANGE_ID TARGET_STATUS` rejects any
    `TARGET_STATUS` other than `ready` at the CLI layer, before any engine logic runs — not an
    unrestricted editor.

- [x] **T-061 — Implement transition precondition evaluation**
  - Maps To: R-011
  - Checks:
    - valid config;
    - valid referenced mappings;
    - valid state;
    - required artifacts;
    - no unresolved placeholders;
    - no active wait;
    - no active failure;
    - exact source state.
  - Evidence: `evaluate_transition_preconditions()` reuses Slice 5's `validate_project_config()` +
    `validate_change()` for the first five checks (they're the same checks R-005 through R-009
    already implement — R-011 restates them, doesn't add new logic), then adds the two
    transition-specific checks (no active wait/failure; exact source state).

- [x] **T-062 — Implement transition-history creation**
  - Maps To: R-014
  - Required Fields:
    - timestamp;
    - actor;
    - action;
    - previous phase and status;
    - new phase and status;
    - reason or transition identifier.
  - Evidence: all seven fields present in every appended `HistoryEvent` (`action: "complete"`,
    `event: "draft-to-ready"`). Verified in `test_e010_valid_transition_succeeds_and_appends_history`.

- [x] **T-063 — Implement atomic state writing**
  - Maps To: R-012, R-013
  - Verification:
    - temporary write in same directory;
    - temporary state validates;
    - atomic replace;
    - temporary cleanup on failure.
  - Evidence: `engine/state_writer.py` implements plan.md §9's exact sequence (temp file in the
    same directory, fsync, re-validate against the schema *before* replacing, `Path.replace`,
    cleanup on any exception). Directly tested: valid content replaces cleanly with no temp file
    left behind; invalid content raises `StateWriteError` *and* leaves the original untouched
    *and* cleans up the temp file.

- [x] **T-064 — Add valid-transition acceptance test**
  - Maps To: E-010
  - Verification: state becomes ready and history is appended.
  - Evidence: `tests/acceptance/test_transition_acceptance.py::test_e010_valid_transition_succeeds`.

- [x] **T-065 — Add rejected-transition preservation tests**
  - Maps To: E-009, E-011
  - Verification: original state bytes remain unchanged.
  - Evidence: E-009 (unresolved placeholder) and E-011 (already-ready change) both pass, both
    assert byte-for-byte state.yaml preservation on rejection.

- [x] **T-066 — Add focused property tests**
  - Maps To: R-004, R-012, R-013
  - Scope:
    - ID and slug safety;
    - path containment;
    - supported and unsupported source states;
    - failed-operation byte preservation.
  - Evidence: ID/slug/containment properties already covered by Slice 4's
    `tests/unit/test_create_change.py` Hypothesis tests (not duplicated). New:
    `tests/property/test_transition_properties.py` exhaustively covers all 80 schema-valid
    `(phase, status)` combinations (10 phases x 8 statuses) — confirms only `specify/draft`
    transitions, and every one of the other 79 combinations preserves `state.yaml` bytes exactly
    on rejection.

## 8. Slice 7 — Quality, Evidence, and Review

- [x] **T-070 — Run baseline quality commands**
  - Maps To: R-019, E-014
  - Commands:
    ```bash
    uv sync
    uv run ruff format --check .
    uv run ruff check .
    uv run mypy
    uv run pytest
    uv build
    uv run ggsad --help
    ```
  - Evidence: `evidence.md` §5. All pass. Ran `ty check` instead of `mypy` (DEV-002 in
    `evidence.md` §11 — `pyproject.toml` only installs `ty`); 142 tests, 98.56% coverage.

- [x] **T-071 — Verify the complete stand-alone workflow**
  - Maps To: R-016, E-012
  - Flow:
    - initialize;
    - create Class M change;
    - validate;
    - transition draft to ready.
  - Evidence: `evidence.md` §6.4. Ran the full sequence manually against a fresh temp directory
    this session (not just the automated test suite) — init, new, validate (correctly fails on
    unfilled templates), fill in, validate (OK), transition (succeeds), validate (OK).

- [x] **T-072 — Verify GSD mapping authority boundaries**
  - Maps To: R-006, R-017, E-007
  - Verification:
    - GSD may not approve;
    - GSD may not transition directly;
    - GSD may not close;
    - `.planning/` remains non-authoritative.
  - Evidence: `evidence.md` §6.2. Checked directly against the real `.ggsad/mappings/gsd.yaml`
    (not just synthetic fixtures): no authority issues on the real file; a mutated copy with
    `may_approve: true` is correctly caught. `.planning/` doesn't exist in this repo (GSD isn't
    installed as an active companion here), so "non-authoritative" holds vacuously; the mapping
    contract's `authoritative: false` markings on every `.planning/*` entry are schema-enforced.

- [x] **T-073 — Verify excluded capabilities are absent**
  - Maps To: R-020, E-015
  - Check:
    - no project memory backend;
    - no MCP server;
    - no web UI;
    - no issue synchronization;
    - no release automation;
    - no multi-agent orchestrator.
  - Evidence: `evidence.md` §6.3. Source-tree listing (22 files) + keyword audit across
    `src/ggsad/**/*.py`: no matches except one incidental "orchestrat" in a docstring about
    ordinary function composition, not multi-agent orchestration. `memory.enabled: false` in the
    generated default config.
  - Note: "Codex review" listed here as an evidence source is **not yet available** — see T-076.
    This task's static-audit portion is complete; the review portion is pending.

- [x] **T-074 — Complete CHG-001 evidence**
  - Maps To: all requirements
  - File: `evidence.md`
  - Verification:
    - requirement coverage complete;
    - example coverage complete;
    - commands recorded;
    - deviations and limitations explicit.
  - Evidence: `evidence.md` written — R-001 through R-020 and E-001 through E-015 all mapped to
    concrete test evidence (§3/§4); quality gates recorded with exact results (§5); two real
    deviations documented (§11); known limitations stated honestly, including that Pair Review
    has not occurred (§12). Not asserted as fully "Verify-Done" — §14 explicitly reports DoW
    triggered (Pair Review pending), not a false pass.

- [x] **T-075 — Prepare stable Pair Review target**
  - Requestor: agent:claude-code
  - Reviewer: agent:codex
  - Required Inputs:
    - stable commit or identified worktree;
    - `spec.md`;
    - `plan.md`;
    - `tasks.md`;
    - relevant ADRs;
    - implementation;
    - tests;
    - `evidence.md`.
  - Constraint: Requestor does not mutate the target while review is active unless a correction cycle starts.
  - Evidence: `human:project-owner` authorized committing 2026-08-03. Two commits on `main`:
    `b5d5995` (governance/GSD-tooling baseline) and `63e725a` (CHG-001 implementation — the
    review target). Working tree confirmed clean after both commits (`git status --short` empty).

- [-] **T-076 — Conduct Codex Pair Review**
  - Review ID: PR-001
  - Reviewer: agent:codex
  - Scope:
    - specification compliance;
    - architecture boundaries;
    - schemas;
    - CLI behavior;
    - path and overwrite safety;
    - YAML security;
    - atomic state update;
    - test sufficiency;
    - stand-alone operation;
    - GSD subordination;
    - excluded-scope compliance.
  - Output: stable findings with severity, status, artifact reference, and required action.
  - Status: In progress — `human:project-owner` authorized using the newly-installed Codex CLI
    (verified ready and authenticated) as the distinct reviewer.
    actually gets invoked as a genuinely distinct reviewer (external Codex CLI access,
    `human:project-owner` acting as reviewer, or an explicit recorded waiver). I cannot review my
    own work and call it Pair Review — the constitution is explicit that "a second pass, subagent,
    or new context of the same participant is not automatically an independent review."

- [!] **T-077 — Resolve Reviewer findings**
  - Requestor: agent:claude-code
  - Verification: Findings are accepted, rejected with rationale, resolved, or formally dispositioned.
  - Constraint: Open blocking findings prevent Verify-Done.
  - Status: Blocked on T-076.

- [!] **T-078 — Re-verify resolved blocking findings**
  - Reviewer: agent:codex
  - Evidence: finding status becomes `verified` or approved equivalent.
  - Status: Blocked on T-076/T-077.

- [x] **T-079 — Evaluate final GG-SAD gates**
  - Order:
    1. DoF
    2. DoW
    3. Verify-Done
    4. Ready-to-Close
  - Evidence: `evidence.md` §14. DoF: not triggered. DoW: **triggered** — Pair Review required
    and not conducted. Current (Build-Done): satisfied. Next (Verify-Done): not satisfied, blocked
    on Pair Review. Reported honestly as `Waiting`, not asserted as complete.

## 9. Documentation Synchronization

- [x] **T-080 — Update README usage where implemented**
  - Constraint: Do not document unimplemented commands as available.
  - Evidence: Fully read `README.md` (not skimmed). No unimplemented CLI commands are falsely
    claimed as available — the "Key Capabilities" section describes the GG-SAD method in general
    (Class S/M/L, all four profile names), and the separate "Project Status and Initial Scope"
    section correctly scopes CHG-001 to Class M only, with an explicit "some commands may remain
    unavailable" disclaimer; this two-tier structure is consistent with how `project-brief.md`
    and `architecture.md` are written. Found and fixed a real, unrelated bug while verifying
    this: `README.md` referenced a `QUICK_START.md` file (in the repo-structure diagram and in
    a "For the complete... bootstrap, follow: QUICK_START.md" pointer) that does not exist
    anywhere in the repository. Removed both references rather than author a new document —
    the README's own inline "Quick Start" content already covers the minimal setup path, and
    inventing a new file was outside this task's scope.

- [~] **T-081 — Update architecture to actual implemented structure**
  - Required Only If: implementation differs materially from the approved architecture.
  - Approval: follow ADR or architecture-change rules.
  - Status: Not applicable. `docs/architecture.md`'s repository structure and layered-dependency
    description (§4, §6) are high-level and consistent with what was actually built; the
    specific module layout in `plan.md` §6 (itself already approved) is the appropriate level of
    detail for that, not `architecture.md`. No material deviation requiring an ADR or
    architecture-document change occurred.

- [ ] **T-082 — Update roadmap status**
  - Required When: CHG-001 reaches verified completion.
  - Evidence: roadmap reference to CHG-001 result.
  - Status: Not yet required — CHG-001 is Build-Done but not Verify-Done (T-079). Revisit once
    Pair Review completes.

- [~] **T-083 — Update third-party notices if GSD files are committed**
  - File: `THIRD_PARTY_NOTICES.md`
  - Verification: installed version and applicable notices are accurate.
  - Status: Not applicable yet — nothing is committed (see T-075), so "if GSD files are
    committed" hasn't occurred. `THIRD_PARTY_NOTICES.md` already exists in the working tree;
    revisit its GSD entry accuracy at commit time, whenever that decision is made.

## 10. Wait Register

| Task | Category | Reason | Waiting For | Safe State | Resume Condition |
|---|---|---|---|---|---|
| — | — | No open waits. T-075 resolved (commits `b5d5995`/`63e725a`, 2026-08-03); T-076 in progress via Codex CLI. | — | — | — |

## 11. Completion Summary

- Total Tasks: 43
- Completed at Creation: 1
- Governance and Ready-to-Build tasks completed 2026-08-02: T-001, T-002, T-003, T-004, T-005,
  T-006, T-007 (7 of 7).
- Slice 1 (T-010 through T-013) completed 2026-08-02: package skeleton, minimal CLI
  (`--help`/`--version`), packaged resources (schemas/templates/mapping), resource-loading tests.
- Slice 2 (T-020 through T-024) completed 2026-08-03: safe YAML loader, JSON Schema validator,
  typed `ProjectConfig`/`IntegrationMapping`/`ChangeState` models, normalized `ValidationIssue`,
  mapping-authority semantic check (R-006/R-017). E-006 and E-008 moved to Slice 5 (T-050/T-052)
  — they need repository-level filesystem context a per-file validator can't provide. 16 of 43
  tasks complete. 34 tests, 100% coverage; ruff/ty/bandit/build all clean.
- Slice 3 (T-030 through T-033) completed 2026-08-03: `ggsad init` — generated asset manifest
  (18 files: config.yaml, 3 schemas, 10 templates, 4 project-level docs), conservative-idempotent
  preflight/write, CLI wiring. E-001 and E-002 pass; verified end-to-end against a real temp
  directory in addition to the test suite. 20 of 43 tasks complete. 50 tests, 99.5% coverage;
  ruff/ty/bandit/build all clean.
- Slice 4 (T-040 through T-043) completed 2026-08-03: `ggsad new` — change-ID/slug validation,
  path containment, `state.yaml` built through the typed `ChangeState` model (found and fixed a
  real null-vs-schema-type serialization bug in the process), 4 templated artifacts. Refactored
  `init`'s and `new`'s shared preflight/write logic into `manifest_writer.py`. Found and fixed a
  real timing bug: `new`'s original re-creation-conflict detection relied on byte comparison,
  which was non-deterministic within the same wall-clock second — replaced with an explicit
  directory-existence check. E-003 and E-004 pass; verified end-to-end (create, reject
  re-creation, reject an invalid ID) and re-ran the suite 3x to confirm the timing fix holds.
  24 of 43 tasks complete. 83 tests, 98.45% coverage; ruff/ty/bandit/build all clean.
- Slice 5 (T-050 through T-054) completed 2026-08-03: `ggsad validate` — config/mapping/state/
  artifact/placeholder checks composed into one aggregator, `--format text|json`, `--change`
  filter. Found and fixed a real placeholder-detector false positive (inline code spans weren't
  stripped, flagging pattern-illustrating prose in this repo's own `spec.md`/`plan.md`) and a
  real stand-alone-check false positive (a naive substring test flagged `ruff`'s own
  `extend-exclude` paths as forbidden dependencies). Authored the required complete, non-
  placeholder Class M example (`specs/examples/class-m/`, R-018/E-013) with an honestly-reported
  `evidence.md` (every gate "Not Run," per the constitution's rule against asserting unexecuted
  checks as passed). Re-validated this repo's own governed artifacts end-to-end: the only
  finding is CHG-001's own missing `evidence.md`, correctly deferred to Slice 7. 29 of 43 tasks
  complete. 125 tests, 98.71% coverage; ruff/ty/bandit/build all clean.
- Slice 6 (T-060 through T-066) completed 2026-08-03: `ggsad transition CHANGE_ID ready` —
  precondition evaluation (reuses Slice 5's config/mapping/state/artifact/placeholder checks,
  adds source-state and active-wait/failure checks), typed history-event construction, atomic
  replace-after-revalidate writer (`engine/state_writer.py`, plan.md §9's exact sequence).
  Promoted the state-serialization helper from `create_change.py` (private, Slice 4) to
  `models/state.py` (public, `dump_change_state`) since the transition engine needed the exact
  same null-vs-schema-type handling — a second real consumer, not speculative reuse. E-009,
  E-010, E-011 pass; property test exhaustively covers all 80 schema-valid (phase, status)
  combinations. **Ran the real engine against CHG-001 itself** (`ggsad transition CHG-001
  ready`): correctly rejected — the one known gap, missing `evidence.md`, is the sole blocker.
  `state.yaml` confirmed untouched (still `draft`, still 12 history events) — did not fabricate
  an `evidence.md` to force it through; that's Slice 7's job with real content. 35 of 43 tasks
  complete. 142 tests, 98.56% coverage; ruff/ty/bandit/build all clean.
- Slice 7 (T-070 through T-074, T-079 through T-081) completed 2026-08-03: all baseline quality
  gates re-verified (142 tests, 98.56% coverage); E-007 and E-015 re-checked against the real
  `.ggsad/mappings/gsd.yaml` and source tree, not just fixtures; full E-012 stand-alone lifecycle
  run manually end-to-end; `evidence.md` written honestly (DoW correctly reported as triggered on
  Pair Review, not asserted as passed). Found and fixed a real, unrelated bug verifying `README.md`
  for T-080: a reference to a nonexistent `QUICK_START.md`. **`ggsad transition CHG-001 ready`
  was re-run once `evidence.md` existed and succeeded** — CHG-001's own `state.yaml` is now
  genuinely `specify/ready`, through its own governed engine, not a hand edit. Fixed one
  resulting stale test assertion (`test_chg_001_state_is_schema_and_model_valid` hardcoded
  `status == "draft"` from earlier slices) and synced `spec.md`/`tasks.md` Metadata Status fields
  to match. T-075 through T-078 (Pair Review) and T-082/T-083 correctly left blocked or not-yet-
  applicable, not fabricated as done — see the Wait Register above and `evidence.md` §15 for the
  two decisions this needs from `human:project-owner`. 38 of 43 tasks complete (the 5 remaining
  are all Pair Review or Pair-Review-gated). 142 tests, 98.56% coverage; ruff/ty/bandit/build all
  clean.
- Current Blocking Area: **T-075/T-076 (Pair Review) — genuinely blocked on two decisions from
  `human:project-owner`**, not something this agent can resolve alone: (1) whether/how to create
  a stable commit as the Pair Review target, since this agent doesn't commit without being asked;
  (2) how `agent:codex` actually gets invoked as a genuinely distinct reviewer. CHG-001 is
  Build-Done and its own `draft → ready` transition has succeeded, but Verify-Done remains
  blocked until Pair Review completes.
- Assigned Requestor: agent:claude-code
- Assigned Reviewer: agent:codex
- Next Permitted Action: `human:project-owner` decides T-075/T-076 (commit authorization and
  Pair Review mechanism). Until then, no further CHG-001 implementation work is pending — the
  remaining tasks are all downstream of that decision.
