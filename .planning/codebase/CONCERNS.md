# Codebase Concerns

**Analysis Date:** 2026-08-18

## Tech Debt

**Type Checking Tool Migration (mypy → ty):**
- Issue: Deviation DEV-002 introduced during CHG-001 build when `pyproject.toml` dev dependencies specified only `ty`, not `mypy`. This mismatch between documented baseline commands (`constitution.md` and other governing documents) and actual installed tooling was escalated as blocking finding PRF-003 by Codex during Pair Review. While resolved via constitutional amendment (Version 0.1→0.2, 2026-08-03), the substitution represents a significant tooling change.
- Files: `docs/constitution.md` (§11), `pyproject.toml` ([tool.ty.environment], [tool.ty.rules]), `docs/project-brief.md`, `docs/architecture.md`, `docs/definitions/definition-of-done.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `specs/CHG-001-reference-repository-bootstrap/spec.md`
- Impact: Every document in the governing hierarchy was amended to reflect `ty` instead of `mypy`. Reverting or switching type checkers requires amending multiple authoritative documents and re-running independent review per the constitution's own amendment process (§19).
- Concern Level: Medium — resolved and independently re-verified by Codex, but represents a pattern of tooling drift in early-stage development
- Mitigation: Constitution amendment and independent re-verification completed (Codex Attempt 4). Monitor for similar unplanned tool substitutions.

**Path Traversal and Schema Validation Gaps (PRF-004, PRF-005):**
- Issue: Codex's independent Pair Review (Attempt 3) found two security/validation gaps in the schema and validator that the implementing agent and test suite had not caught:
  - PRF-004: `.ggsad/schemas/config.schema.json` and `mappings.schema.json` accepted Windows absolute paths (`C:\outside.yaml`), UNC paths (`\\server\share`), and backslash-traversal paths (`..\..\outside.yaml`) in the `relativePath` and `artifactPath` properties. The validator then resolved these relative-to-target paths using Python's `/` operator, which silently discards the left operand if the right side is absolute, allowing reads/writes outside the repository.
  - PRF-005: `schema_version` in all three schemas accepted arbitrary syntactically valid version strings (e.g., `"99.9"`) instead of enforcing only the currently supported `"0.1"`.
- Files: `.ggsad/schemas/config.schema.json`, `.ggsad/schemas/mappings.schema.json`, `.ggsad/schemas/state.schema.json`, `src/ggsad/resources/schemas/` (packaged copies), `src/ggsad/application/validate_repository.py` (containment check)
- Impact: PRF-004 was a real vulnerability allowing a malicious or erroneous `config.yaml` or `mappings.yaml` to reference files outside the project directory. PRF-005 could accept incompatible schema versions at runtime, causing silent failures or unexpected behavior when schemas evolve. Both are now fixed with regression tests (Codex Attempt 4 independently re-verified via adversarial probes).
- Concern Level: High (security-relevant) — resolved and re-verified, but indicates a gap in the agent's own threat modeling and schema design review.
- Mitigation: Fixes applied (regex tightening + explicit `is_relative_to()` containment check for PRF-004; `const: "0.1"` for PRF-005). Added 5 regression tests. Codex's adversarial probes (Attempt 4) re-confirmed all mitigations work. Pattern: independent Pair Review caught gaps the implementing agent's tests did not.

## Known Limitations and Scope Gaps

**Incomplete Phase Transition Engine (R3 in Roadmap):**
- Limitation: CHG-001 implements only the `specify/draft → specify/ready` transition (R-010). The full phase-transition engine (`intake`→`specify`→`plan`→`build`→`verify`→`release`→`closed` and all status states) is roadmap item R3, not part of CHG-001.
- Files: `src/ggsad/engine/transitions.py` (SUPPORTED_SOURCE_PHASE = "specify", SUPPORTED_SOURCE_STATUS = "draft", SUPPORTED_TARGET_STATUS = "ready")
- Impact: Users cannot automate transitions beyond draft→ready. The roadmap item R2 entry for `ggsad status` was never part of CHG-001's actually-approved scope (`spec.md` requirements R-001–R-020 and `CLAUDE.md`'s Initial Change Constraint name only `init`/`new`/`validate`/`transition`), creating a gap between the roadmap description and what was delivered.
- Status: Intentional — CHG-001's scope is deliberately limited to R0 (bootstrap) and one transition arc as a vertical slice for validation.
- Risk: Future changes must implement R3 (state and transition engine), R6 (gate engine), R7 (evidence and traceability), and R8 (Pair Review engine) before the full workflow is operational. Projects using only CHG-001's delivered capability are limited to manual workflow progress beyond draft→ready.

**No Profile Content Implementation (R4 in Roadmap):**
- Limitation: `.ggsad/config.yaml` recognizes the four built-in profile names (`lean`, `standard`, `governed`, `regulated`) and validates them (E-006), but `.ggsad/profiles/` contains no actual profile-content files. Profile resolution, inheritance, and effective-workflow reporting are R4 roadmap items.
- Files: `.ggsad/config.yaml`, `.ggsad/profiles/` (empty directory structure only), `src/ggsad/validators/compliance_profile.py` (validates profile name existence, not content)
- Impact: All projects must use the hardcoded `standard` profile behavior. Custom profiles, lean-mode cost reduction, and governed/regulated mode strengthening remain unimplemented.
- Status: Intentional — R4 is "Next" on the roadmap, not part of R0 (bootstrap) or R1 (reference examples).

**Limited Pair Review Coverage:**
- Limitation: CHG-001's own Pair Review (PR-001, `spec.md` §10, `spec.md` §15) is Agent–Agent (`agent:claude-code` Requestor, `agent:codex` Reviewer). No Human–Human or mixed-participant Pair Review is demonstrated in the reference repository.
- Files: `specs/CHG-001-reference-repository-bootstrap/evidence.md` (Section 9), `.ggsad/config.yaml` (pair_review policy), `docs/roadmap.md` (R1 partially delivered, noting absence of Human–Human example)
- Impact: Implementation and testing of Human–Human and mixed-participant Pair Review flows remain future work (R1 "remains as future roadmap work"). The validator enforces distinct Requestor/Reviewer identities (`src/ggsad/validators/mapping_authority.py`), but no end-to-end example demonstrates the workflow.
- Status: Documented as future work in roadmap (R1).

**Class S and L Examples Absent:**
- Limitation: Only a Class M example exists (`specs/examples/class-m/`). Class S (Patch) and Class L (Initiative) examples are R1 future work, not part of CHG-001's Class-M-only scope.
- Files: `specs/examples/` (only `class-m/` present)
- Impact: New projects cannot use real Class S or L templates or lifecycle examples. Unknown unknowns about Patch and Initiative workflows have not been surfaced.
- Status: Documented as future work in roadmap (R1).

**Manual Wait and Fail Demonstration Absent:**
- Limitation: CHG-001's own transition history records a `draft-to-ready` event but does not include dedicated manual examples demonstrating wait-state creation, resume, failure, or cancellation.
- Files: `specs/` (no dedicated wait/fail examples)
- Impact: Users cannot reference documented examples of how to use wait and fail states. These remain described in the normative spec but not shown working end-to-end in the repository.
- Status: Documented as future work in roadmap (R1, "distinct manual wait and fail demonstration examples").

**Single GSD Mapping Only:**
- Limitation: Only one integration mapping is implemented—the GSD companion mapping at `.ggsad/mappings/gsd.yaml`. The full mapping registry, stand-alone operation validation, and validation of the mapping contract remain R4 work.
- Files: `.ggsad/mappings/gsd.yaml`, `src/ggsad/validators/mapping_authority.py` (validates GSD mapping authority constraints), `src/ggsad/models/mapping.py`
- Impact: Stand-alone operation is tested (`evidence.md` E-012) but only with a single real mapping. Future companion methods (OpenSpec, Spec Kit, BMAD, Hermes, Kiro per the roadmap) have not been specified or integrated.
- Status: Intentional — R1 scope includes examples, R4 scope includes full registry and validation.

## Fragile Areas

**State Mutation Atomicity and File I/O:**
- Component: `src/ggsad/engine/state_writer.py` (`atomic_replace_state()`)
- Why Fragile: The atomic replace relies on writing to a same-directory temp file, syncing, revalidating, and then replacing the original. This sequence is correct but depends on filesystem guarantees and Python's file I/O behavior. If a mid-sequence exception occurs (disk full, permissions change, process killed), the original file and temp file may both exist in an inconsistent state.
- Safe Modification: Never modify `atomic_replace_state()` without adding explicit cleanup tests for exception paths (disk-full simulation, mid-sync termination, revalidation failure). Every rejection test already asserts the original file is byte-unchanged, but edge cases around partial writes and temp-file cleanup are worth stress-testing.
- Test Coverage: `tests/unit/test_state_writer.py` covers atomic replace, temp-file cleanup, invalid-content rejection, and original preservation. No explicit tests for disk-full or process-termination scenarios.

**Schema Version Locking to 0.1:**
- Component: `.ggsad/schemas/config.schema.json`, `mappings.schema.json`, `state.schema.json` (all constrain `schema_version: const: "0.1"`)
- Why Fragile: This fix (PRF-005) prevents forward-compatibility. If a future version of GG-SAD introduces `schema_version: "0.2"`, all existing YAML files must be manually migrated before they are readable by the new version. No migration tooling exists.
- Safe Modification: Before implementing schema_version 0.2 or higher, design and implement a migration command (e.g., `ggsad migrate --from 0.1 --to 0.2`). Document the migration path in the roadmap and constitution. Consider including backward-compatibility logic for at least one version cycle.
- Test Coverage: `tests/` includes regression tests for version rejection (schema_version 99.9 is rejected), but no migration or compatibility-window tests exist.

**Placeholder Detection Over Spec.md and Plan.md Only:**
- Component: `src/ggsad/validators/placeholder_detector.py`, invoked in `src/ggsad/application/validate_repository.py` (_PLACEHOLDER_CHECKED_ARTIFACTS = ("spec.md", "plan.md"))
- Why Fragile: The validator deliberately limits placeholder checks to exactly spec.md and plan.md to match R-011's wording ("no unresolved placeholders in the specification/plan"). However, new users might place placeholders in other artifacts (tasks.md, evidence.md, or supplementary docs) and expect validation to catch them. This narrow scope may lead to missed incomplete work.
- Safe Modification: If scope expansion is needed, update the requirement R-009 and R-011 to specify which files should be placeholder-checked, then add those files to _PLACEHOLDER_CHECKED_ARTIFACTS. Document the rationale for the chosen scope.
- Test Coverage: `tests/unit/test_placeholder_detector.py` and `tests/acceptance/test_validate_acceptance.py` both verify placeholder detection in spec.md/plan.md only. Good coverage for current scope, but no tests for "what if placeholder is in tasks.md?"

**Change ID Validation Regex:**
- Component: `src/ggsad/application/create_change.py` (validate_change_id pattern: `^CHG-\d{3,}-[a-z0-9]+(?:-[a-z0-9]+)*$`)
- Why Fragile: The regex enforces CHG-\d{3,}-slug. The three-digit minimum prevents CHG-1 or CHG-01 but allows CHG-9999 and beyond. If a project stores millions of changes, numeric overflow is theoretically possible, though Python integers are unbounded.
- Safe Modification: Document the intended ID space (e.g., "expect no more than 1 million changes" or "CHG ID is a stable project namespace, not a counter"). If ID collisions or overflow becomes a real concern, consider UUIDs or sequential IDs with rollover handling.
- Test Coverage: `tests/unit/test_create_change.py` includes parameterized tests for invalid IDs (missing prefix, wrong format, uppercase, special characters) and property-based tests covering various valid/invalid patterns. Numeric overflow not explicitly tested.

**Config/Mapping/State YAML Loading:**
- Component: `src/ggsad/validators/yaml_loader.py` (uses ruamel.yaml)
- Why Fragile: The loader intentionally uses `typ='rt'` (round-trip) mode to preserve comments and formatting, which is good for manual editing but slower and uses more memory than standard loading. If the repository scales to many hundreds of changes, YAML loading performance may degrade.
- Safe Modification: Monitor load times in integration tests. If performance becomes a bottleneck, consider selective preservation (comments on specific fields only, or dropping comment preservation for internal schema files).
- Test Coverage: `tests/unit/test_yaml_loader.py` tests safe loading, unsafe tag rejection, and error reporting. No performance or scalability tests.

## Performance Bottlenecks

**Validation on Every Transition:**
- Problem: `src/ggsad/engine/transitions.py::evaluate_transition_preconditions()` runs the full validation pipeline every time a transition is attempted. For projects with many integration mappings or large governance documents, this re-validates config, mappings, and state each time.
- Cause: Conservative correctness—the engine ensures every precondition is fresh before writing, preventing stale-state transitions. However, this means loading, parsing, and validating all YAML files on every `ggsad transition` call.
- Files: `src/ggsad/engine/transitions.py` (lines 82–109), called by `src/ggsad/cli.py::transition_command()`
- Improvement Path: (1) Add a `--skip-validation` flag for scripted workflows that know files are valid (with clear warnings). (2) Cache validation results per file + modification time (requires careful invalidation). (3) Implement R3 (state and transition engine) with smarter incremental validation. For now, this is acceptable for a reference implementation.

**Repository Initialization Over-Validates:**
- Problem: `src/ggsad/application/initialize_project.py::initialize_project()` writes 18 files but validates none of them after writing. `ggsad init` then returns to the CLI without confirming the generated files are valid.
- Cause: Intentional conservatism (R-012: leave in a valid or safely rejected state, but don't corrupt if schema changes later). The files use embedded resource templates proven valid at build time.
- Files: `src/ggsad/application/initialize_project.py` (manifest_writer.py)
- Improvement Path: Optional `--validate-after` flag to run `validate_project_config()` after init succeeds, providing extra confidence. Not critical for R0 but useful for complex deployments.

## Security Considerations

**YAML Deserialization (via ruamel.yaml):**
- Risk: YAML deserialization can execute arbitrary Python code if the YAML file contains object constructors. While the codebase uses `typ='rt'` and avoids `unsafe_load()`, a future change might enable unsafe loading.
- Files: `src/ggsad/validators/yaml_loader.py` (explicitly uses safe loading)
- Current Mitigation: `yaml_loader.py` uses `YAML(typ='rt', pure=True)` for safe, pure-Python loading. All governance YAML files (config.yaml, mappings.yaml, state.yaml) are validated against JSON Schemas after loading, providing a second barrier against unexpected structures.
- Recommendations: (1) Document the safe-loading choice in ADRs or architecture.md. (2) Add a Bandit check to the CI to flag any unsafe_load() calls. (3) Maintain a list of approved YAML features (no Python objects, anchors, aliases only in non-security contexts).

**File Path Traversal (now fixed, see PRF-004):**
- Risk: Resolved—see PRF-004 above. The `relativePath` and `artifactPath` schemas now reject absolute, UNC, and backslash-traversal paths. `src/ggsad/application/validate_repository.py::_validate_declared_mappings()` explicitly checks `is_relative_to(target)` as defense in depth.
- Status: Fixed and independently re-verified (Codex Attempt 4, PRF-004 verified).

**State File Permissions:**
- Risk: `.ggsad/state/CHG-*/state.yaml` files contain sensitive metadata (actor IDs, decision records, failure reasons). If a shared CI/CD environment runs `ggsad` commands, these files may be readable by unauthorized actors.
- Files: Any generated `specs/CHG-*/state.yaml`
- Current Mitigation: None explicit. Git permissions and CI/CD access controls are assumed.
- Recommendations: (1) Document that `specs/CHG-*/state.yaml` should be protected by CI/CD and Git access controls (e.g., no public clones). (2) Consider encrypting sensitive fields (actor IDs, private decision metadata) if the repository is shared. (3) Implement a redaction/audit-log feature as part of R10 (GG-SAD Project Memory).

## Test Coverage Gaps

**Transition Failures and Edge Cases:**
- Untested Behavior: The transition engine rejects transitions from states other than `specify/draft`, but no tests exercise transitions from `specify/ready` (should fail), `plan/draft` (should fail), or any non-`specify/draft` combination.
- Files: `tests/` (includes property test for 80 schema-valid phase/status combinations in `test_transition_properties.py`, but property test is skipped if the state is not exactly `specify/draft`, so failure paths are indirectly tested but not explicitly named)
- Risk: Boundary conditions around phase/status mismatches may have silent failures or incorrect error messages.
- Priority: Medium — property test provides coverage, but explicit failure tests for each invalid combination would improve clarity.

**Custom Profile Behavior:**
- Untested Behavior: Profiles are validated by name (E-006) but no tests exercise custom profile loading, inheritance, or effective-workflow resolution (these are R4 work).
- Files: `src/ggsad/validators/compliance_profile.py` (only validates standard/lean/governed/regulated names)
- Risk: When R4 is implemented, new bugs in profile resolution may not be caught by existing tests.
- Priority: Low — R4 will introduce its own tests.

**GSD Mapping Authority Constraints:**
- Untested Behavior: The GSD mapping authority validator (`src/ggsad/validators/mapping_authority.py`) checks that the GSD mapping does not grant `may_approve` or other forbidden authorities. The test uses a fixture with a mutated copy; the real `.ggsad/mappings/gsd.yaml` is not tested directly in CI.
- Files: `tests/integration/test_governed_artifact_validation.py` (test_e007), `evidence.md` (Section 6.2 confirms real mapping passes)
- Risk: If the real GSD mapping is manually edited and a forbidden authority is added, this will only be caught by a human reviewer or ad hoc manual validation.
- Priority: Low — evidence.md Section 6.2 manually re-verified the real mapping; consider adding a static CI check to validate the real mapping file, not just fixtures.

**Stand-Alone Operation with GSD Integration:**
- Untested Behavior: The test suite includes `test_standalone_operation.py` (E-012), which runs init→new→validate→transition with `operating_mode: stand-alone` and zero integrations. However, no tests combine stand-alone assertions with actual GSD integration enabled to verify GSD doesn't bypass GG-SAD gates.
- Files: `tests/integration/test_standalone_operation.py`, `.ggsad/mappings/gsd.yaml`, `.ggsad/config.yaml`
- Risk: Future changes to GSD integration might accidentally create a pathway to bypass GG-SAD validation if not explicitly tested for isolation.
- Priority: Medium — a test that runs with GSD enabled but validates that GSD cannot modify governed state files would strengthen confidence.

## Incomplete Implementations and Deferred Work

**Roadmap Alignment Issues:**

1. **R0 Status Overstated:** `docs/roadmap.md` (§Now, R0) claims "Complete" with all five exit criteria evidenced in `specs/CHG-001-reference-repository-bootstrap/evidence.md`. This is accurate. However, `docs/implementation-roadmap.md` (§Phase 1, exit criteria) refers to "no CLI or agent dependency is required," and CHG-001 relies on Pydantic/Typer/ruamel.yaml dependencies for the CLI to function. The distinction—between method-level independence and implementation-level dependencies—is subtle and correctly addressed in the context sections.

2. **R1 Partially Delivered But Marked Separate:** The roadmap separates R0 (bootstrap) from R1 (reference examples), and R1 is correctly marked "Partially delivered." However, the roadmap briefly implies R1 examples should come after R0, when in fact R1 examples (Class M example, stand-alone operation proof) are woven into CHG-001's evidence. This is not a bug but a point of confusion for readers expecting a clean separation.

3. **R2 "Delivered" But `ggsad status` Missing:** `docs/roadmap.md` (§Now, R2) claims all exit criteria are met, but explicitly notes that `ggsad status` "from the original command list above was never part of CHG-001's actually-approved scope" and "remains a candidate for a future change if/when needed." This is documented honestly in the roadmap but may confuse readers comparing the R2 description in `implementation-roadmap.md` to what is actually available.

4. **R3–R8 Unstarted:** The "Next" section of `docs/roadmap.md` lists R3–R8 but provides no implementation timelines or owners. For a project in active development, this is normal, but users expecting a timeline or implementation plan will find none.

**Deferred Capabilities Not Yet Triggered by Use:**

- **Project Memory (R13):** Explicitly deferred. The specification allows recording Decisions, Learnings, Failures, and External Sources, but no storage, retrieval, or CLI commands exist. If projects begin accumulating decision records, this capability will be needed sooner than planned.
- **Dual-Track Development (Open Topics):** Questions about parallel Discovery and Delivery state, handover gates, and evidence synchronization remain unresolved. If a project needs to track both exploratory work and production delivery, this gap will surface quickly.
- **Delivery Models (Open Topics):** Trunk-Based Development, GitFlow, and Continuous Delivery compatibility remain open. Projects using branching strategies or feature flags may need ad hoc workarounds.
- **Multi-Agent Orchestration (Deferred by Default):** Explicitly not included. If a project requires routing work to multiple specialized agents, this capability will need to be built or integrated.

## Integration and Dependency Risks

**Python Version Requirement:**
- Requirement: `pyproject.toml` requires Python >=3.13 (specified in `requires-python`).
- Risk: Python 3.13 is not widely deployed in all organizations yet. Projects using older Python versions (3.12, 3.11) cannot use the package without upgrading.
- Mitigation: The choice is intentional (ADR-0001 adopts Python for the reference engine) and well-documented. Consider backporting to 3.12 if adoption becomes a blocker. Currently acceptable for a reference implementation.

**Pydantic v2 Dependency:**
- Dependency: `pyproject.toml` requires `pydantic>=2.13.4`
- Risk: Pydantic v2 is a major version with breaking changes from v1. Projects using v1 or requiring both v1 and v2 for other packages may face dependency conflicts.
- Mitigation: Pydantic v2 is stable and actively maintained. The codebase uses no deprecated features. Keep this updated via dependabot or similar.

**ruamel.yaml for Round-Trip YAML:**
- Dependency: `pyproject.toml` requires `ruamel-yaml>=0.19.1`
- Risk: ruamel.yaml is less widely used than PyYAML. Maintenance and community support are smaller. If the package becomes unmaintained, migration to PyYAML (with comment-preservation loss) may be necessary.
- Mitigation: ruamel.yaml is actively maintained as of 2026. Keep vendored or pinned to prevent unexpected breaking changes.

**JSON Schema Draft 2020-12:**
- Choice: All schemas in `.ggsad/schemas/` use JSON Schema Draft 2020-12 (newest standard).
- Risk: Older validators or CI systems may not recognize 2020-12 features. Some tools (particularly in CI/CD) default to older drafts.
- Mitigation: Explicitly document in architecture.md and README.md which validator should be used. The `jsonschema>=4.26.0` package supports 2020-12.

## Recommendations

### Immediate (Next Phase)

1. **Clarify Roadmap Scope and Timing:** Add owners, timelines, and dependencies for R3–R8 roadmap items in `docs/roadmap.md`. Currently, it lists deliverables but not who will implement them or when.

2. **Profile Content Placeholder:** Even though R4 is deferred, create placeholder files (e.g., `.ggsad/profiles/standard.yaml`, etc.) so the profile structure is visible and future implementations have a clear location. This will reduce confusion for new users.

3. **Document Open Topics Resolution:** Dual-track development, delivery models, and approval identity remain open (§Open in roadmap). Explicitly assign these as design tasks in a future initiative (e.g., "Design and validate Trunk-Based Development support for GG-SAD"). Link them to roadmap items that depend on them (R3 phase transitions, R10 release workflow).

### Short-Term (1–2 Quarters)

1. **Add Class S and L Examples:** R1 explicitly calls for one example each for Class S and L. These are critical for validating the method across change sizes. Prioritize alongside any project that uses Patch or Initiative scopes.

2. **Implement R3 (State and Transition Engine):** The current limitation to `specify/draft → specify/ready` blocks real projects. R3 unlocks the full workflow. Estimate scope and assign ownership.

3. **Implement Human–Human Pair Review Example:** Current PR-001 is Agent–Agent. A Human–Human or mixed-participant Pair Review example is essential for teams. This is smaller than full R8 implementation and can be done in parallel.

4. **Schema Migration Tooling:** Before implementing `schema_version: "0.2"` or higher, design and implement a `ggsad migrate` command. Document the migration path in the constitution.

5. **Performance Monitoring:** Add optional timing logs to transition and validation to detect slowdowns as the repository scales. Set up alerts if a single `ggsad transition` call takes >5 seconds.

### Long-Term (Future Phases)

1. **Project Memory (R13):** Once multiple real projects have accumulated decision records, implement R13. Make it backend-neutral and subordinate to governing documents.

2. **Delivery Model Decision:** Resolve Trunk-Based Development, GitFlow, and Continuous Delivery compatibility (currently Open Topics). This blocks R10 (CI Integration) and R6 (Release workflow).

3. **Security Hardening:** After real-world use, revisit state-file permissions, YAML deserialization, and add secret management if sensitive data becomes common in change artifacts.

4. **IDE and CI Integrations (R12):** Once adoption is proven, evaluate GitHub Actions, GitLab CI, VS Code, and JetBrains integrations. Maintain strict rules: integrations are optional, cannot bypass gates, and do not modify method semantics.

---

*Concerns audit: 2026-08-18*
