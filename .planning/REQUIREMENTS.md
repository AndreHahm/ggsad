# Requirements: GG-SAD — Executable Core (Milestone v1.1)

**Defined:** 2026-10-24 (owner decisions O-1 to O-11 were made 2026-10-23)
**Input:** seed requirements derived from the prototype's milestone proposal; the prototype is context, not conformance evidence. IDs restart per milestone; a reference to the archive reads `v1.0 APPR-01`.
**Core Value:** A change can be driven from goal to closure by an agent and a human where every gate
result is either checked mechanically or attributed to a verified human, and the engine, not the
agent, decides what may happen next.

## v1 Requirements

Nine categories. The SPEC requirements are delivered as a proposed diff to the English normative
specification and are **hard-gated**: owner approval (APPR) and then independent review (REVIEW)
must pass before any engine work (ENG, TRUST, INTEG, WORK) begins, and those checkpoints MUST NOT be
bundled with other work. Implementation follows approved text, never the reverse.

### Decision Record (DEC)

- [ ] **DEC-01**: The owner's decisions O-1 through O-11 (made 2026-10-23) are recorded in one decision record in the repository before any normative text is drafted, each stating the option chosen and, for O-4 (JSON state), that it departs from the proposal's recommendation to keep YAML

### Normative Specification (SPEC)

Scope of the amendment is the set of protections the prototype exercised, plus the structural
decisions of O-1 to O-11. Changes are proposed text only (SPEC-13).

- [ ] **SPEC-01**: The proposed text states that a change's gate definitions are fixed when the change is approved, and that any later edit to them blocks every operation except cancellation until a human re-approves (MAPPING P-01)
- [ ] **SPEC-02**: The proposed text defines gate results as three-valued (satisfied, not satisfied, could not be evaluated); a gate that cannot be evaluated is never treated as a failure and never counts toward a retry limit (MAPPING P-02)
- [ ] **SPEC-03**: The proposed text adds a normative fourth result, `blocked`, to the result envelope (section 22.2): a recorded evaluation that did not close the change, always `changed: true`; `rejected` means nothing was written and is never `changed` (MAPPING P-03; O-5)
- [ ] **SPEC-04**: The proposed text defines assurance levels A0 to A2 and the signed-approval statement (operation, change, position in the change's history, signer, exact content approved) as normative, leaves verifiers (for example SSH signature, platform review) optional, and states that an agent able to use a human's credentials can act as that human (MAPPING P-04; O-3)
- [ ] **SPEC-05**: The proposed text distinguishes history consistency from history completeness and requires an external anchor, or an equivalent, to detect truncation where a profile demands high assurance (MAPPING P-05)
- [ ] **SPEC-06**: The proposed text defines a change's scope, how it is measured (against the commit the change started from), that work outside it is a hard failure, and that a change runs isolated from unrelated uncommitted work (MAPPING P-06)
- [ ] **SPEC-07**: The proposed text lets a verification gate carry a recorded baseline of already-failing tests: the gate passes when every failure is on the baseline, fails and names any new failure, and is not evaluable when the failures cannot be read (MAPPING P-07)
- [ ] **SPEC-08**: The proposed text distinguishes hard failure (the change closes as failed without human action) from soft failure (the change pauses for a human disposition: close as failed, or a recorded override that grants a bounded number of further attempts and lapses when the gates are amended) (MAPPING P-08)
- [ ] **SPEC-09**: The proposed text records open questions as change state, supports structured answers (a choice among declared options), and blocks specification approval and closure while any question is unanswered (MAPPING P-09)
- [ ] **SPEC-10**: The proposed text defines evidence as executable and tied to a requirement; a change with no requirements has no complete evidence (MAPPING P-10)
- [ ] **SPEC-11**: The proposed text makes the interpreter that runs gate commands explicit and opt-in, and states the trust consequence: code in git-ignored locations is invisible to the scope check (MAPPING P-12)
- [ ] **SPEC-12**: The proposed text specifies both profiles (O-1): `core` (the simplified four-state model) and `full` (the phases, DoR/DoD pairs, size classes and document hierarchy of the current specification), states which requirements apply to which, and how a change moves between them
- [ ] **SPEC-13**: No file under `src/ggsad/` is modified while the normative text is drafted
- [ ] **SPEC-14**: `full` is revised to carry the protections of SPEC-01 to SPEC-11 as invariants of both profiles (O-9), is marked specified-but-not-implemented (O-8), and each `full` rule has an acceptance example of the kind the `core` rules have
- [ ] **SPEC-15**: State is a JSON document (`state.json`) with a defined canonical form for hashing, and the specification's examples and templates are updated accordingly (O-4)
- [ ] **SPEC-16**: Profile resolution is specified as the six-layer order of section 5.3, with the rule that a lower layer must not weaken a higher one; `core` implements four of the six layers (O-2, O-10) — unproven by the prototype beyond a base-gate no-weakening check
- [ ] **SPEC-17**: `reopen` is specified for `full` and absent from `core`, and the transition table states this per profile (O-6)
- [ ] **SPEC-18**: Every artifact carries `schema_version`, an unknown version is refused, and migration is an explicit, recorded command (O-7)

### Owner Approval (APPR)

- [ ] **APPR-01**: The repository owner reviews the exact proposed normative diff (SPEC-01 through SPEC-18) and records explicit approval, or specific requested changes, before independent review begins

### Independent Review (REVIEW)

- [ ] **REVIEW-01**: An independent review by a reviewer that is not the Requestor — and not a fresh context or subagent of the Requestor — evaluates the owner-approved diff, with findings carrying stable IDs, severity and exact references
- [ ] **REVIEW-02**: Blocking findings are resolved, or explicitly dispositioned by the owner, before the diff is treated as final

### Core Engine (ENG)

- [ ] **ENG-01**: For the `core` profile, the state model and every transition of the approved table are implemented in `src/ggsad/`; a rejected attempt writes nothing, a blocked attempt is recorded, and no operation leaves state partially written
- [ ] **ENG-02**: The gate evaluator implements the approved evaluation order and the three-valued results
- [ ] **ENG-03**: Frozen gates, content-hash approvals and their staleness are implemented
- [ ] **ENG-04**: Scope evaluation and hard/soft failure behaviour, including bounded overrides, are implemented
- [ ] **ENG-05**: Open questions, structured answers and the approval block are implemented
- [ ] **ENG-06**: A change that selects the `full` profile is refused with a clear message naming it as specified-but-not-implemented; the engine never runs it as `core` silently
- [ ] **ENG-07**: Profile resolution for `core` is implemented over its four layers, including the check that a change's gates cannot weaken the profile's base gates (O-10) — unproven by the prototype beyond that check

### Trust and Integrity (TRUST, INTEG)

- [ ] **TRUST-01**: A verifier interface exists; the self-declared verifier is the default and is reported at the lowest assurance level
- [ ] **TRUST-02**: At least one verifier cannot be forged by an agent that lacks the human's credentials (the prototype's SSH signature is the reference design), and verification fails closed
- [ ] **INTEG-01**: State history is tamper-evident, and an optional external anchor detects truncation
- [ ] **INTEG-02**: Hashing is defined for text and for binary content, with line-ending normalisation applied to text only (the prototype normalises every file, a known weakness)
- [ ] **INTEG-03**: An unknown `schema_version` is refused with a clear message, and migrating existing artifacts — including `state.yaml` to `state.json` — is an explicit, recorded command (O-7)

### Workflow Surface (WORK)

- [ ] **WORK-01**: `init`, change creation, approval, transition, check and review commands exist with the approved result envelope and exit codes
- [ ] **WORK-02**: Changes can run in isolated checkouts, and an on-demand guard that enforces hard failures can run from a hook or CI
- [ ] **WORK-03**: Baseline-aware verification gates and an explicit, opt-in project interpreter are available
- [ ] **WORK-04**: A verify-only CI check confirms history integrity (and the anchor), that frozen gates match the approval, that approvals are current and at the required level, scope against the base, and that no hard failure is active; it does not execute the change's own commands with CI's privileges (O-11) — unproven by the prototype

### Verification (VERIFY)

- [ ] **VERIFY-01**: The implementation is audited against the approved specification, producing a written list of evidenced gaps, each with an exact reference, or an explicit statement that none exist
- [ ] **VERIFY-02**: Each protection has an adversarial test that fails when the protection is removed: editing the gates, forging an approval, replaying a signature, truncating history, leaving scope
- [ ] **VERIFY-03**: The complete verification baseline runs clean and its output is recorded as evidence: `uv sync --locked`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check src tests`, `uv run pytest`, `uv build`

## v2 Requirements (Deferred, Explicit Non-Goals for This Milestone)

Potential future milestone scope, not tracked further here:

### Deferred Capability

- **DEFER-01**: GG-SAD project memory (Decision/Learning/Failure/Definition/External Source records)
- **DEFER-02**: MCP integration
- **DEFER-03**: A web UI
- **DEFER-04**: Multi-agent orchestration
- **DEFER-05**: Implementing the `full` profile (specified in this milestone, built later — O-8)
- **DEFER-06**: Building change-class requirements and integration mappings as resolution layers, and combination mode (specified here, not built — O-10)

## Out of Scope

| Feature / Action | Reason |
|---|---|
| Building memory, MCP, a web UI, or multi-agent orchestration | Remain explicit non-goals (carried from v1.0) |
| Running the `full` profile in the engine | Specified but not built (O-8); ENG-06 refuses it |
| Copying prototype code into `src/ggsad/` | Stack, state format and CLI framework differ; the prototype is a design and test oracle |
| Treating prototype results, or prior GG-SAD/CHG-001 completion evidence, as proof of conformance | Historical context only; every requirement is re-verified here (carried from v1.0) |
| Modifying `src/ggsad/` while drafting normative text | SPEC-13, as NORM-08 did in v1.0 |
| Using GG-SAD and GSD simultaneously as development methods for this repository | GSD Core is the sole development method (carried from v1.0) |
| Preserving prior roadmap ordering or `specs/CHG-*` change-closure claims | Legacy docs are not active development governance (carried from v1.0) |
| Rewriting passing implementation code solely for a clean history | Explicit non-goal (carried from v1.0) |

## Traceability

Which phases cover which requirements. Phase numbers are this milestone's (v1.1) and restart at 1;
they are not the archived v1.0 phases of the same number.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DEC-01 | Phase 1 | Pending |
| SPEC-01 | Phase 2 | Pending |
| SPEC-02 | Phase 2 | Pending |
| SPEC-03 | Phase 2 | Pending |
| SPEC-04 | Phase 2 | Pending |
| SPEC-05 | Phase 2 | Pending |
| SPEC-06 | Phase 2 | Pending |
| SPEC-07 | Phase 2 | Pending |
| SPEC-08 | Phase 2 | Pending |
| SPEC-09 | Phase 2 | Pending |
| SPEC-10 | Phase 2 | Pending |
| SPEC-11 | Phase 2 | Pending |
| SPEC-12 | Phase 2 | Pending |
| SPEC-13 | Phase 2 | Pending |
| SPEC-14 | Phase 2 | Pending |
| SPEC-15 | Phase 2 | Pending |
| SPEC-16 | Phase 2 | Pending |
| SPEC-17 | Phase 2 | Pending |
| SPEC-18 | Phase 2 | Pending |
| APPR-01 | Phase 3 | Pending |
| REVIEW-01 | Phase 4 | Pending |
| REVIEW-02 | Phase 4 | Pending |
| ENG-01 | Phase 5 | Pending |
| ENG-02 | Phase 5 | Pending |
| ENG-03 | Phase 5 | Pending |
| ENG-04 | Phase 5 | Pending |
| ENG-05 | Phase 5 | Pending |
| ENG-06 | Phase 5 | Pending |
| ENG-07 | Phase 5 | Pending |
| TRUST-01 | Phase 6 | Pending |
| TRUST-02 | Phase 6 | Pending |
| INTEG-01 | Phase 6 | Pending |
| INTEG-02 | Phase 6 | Pending |
| INTEG-03 | Phase 6 | Pending |
| WORK-01 | Phase 7 | Pending |
| WORK-02 | Phase 7 | Pending |
| WORK-03 | Phase 7 | Pending |
| WORK-04 | Phase 7 | Pending |
| VERIFY-01 | Phase 8 | Pending |
| VERIFY-02 | Phase 8 | Pending |
| VERIFY-03 | Phase 8 | Pending |

**Coverage:**
- v1 requirements: 41 total
- Mapped to phases: 41
- Unmapped: 0 ✓

By phase: Phase 1 = 1 (DEC), Phase 2 = 18 (SPEC), Phase 3 = 1 (APPR), Phase 4 = 2 (REVIEW),
Phase 5 = 7 (ENG), Phase 6 = 5 (TRUST 2, INTEG 3), Phase 7 = 4 (WORK), Phase 8 = 3 (VERIFY).

---
*Requirements defined: 2026-10-24*
*Last updated: 2026-10-24 after roadmap creation (traceability filled in)*
