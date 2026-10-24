# Roadmap: GG-SAD

## Milestones

- ✅ **v1.0 Normative Clarification & Governance Transition** — Phases 1–8 (shipped 2026-08-22)
- 🚧 **v1.1 Executable Core** — Phases 1–8 (in progress; phase numbering restarted at 1)

## Phases

<details>
<summary>✅ v1.0 Normative Clarification & Governance Transition (Phases 1–8) — SHIPPED 2026-08-22</summary>

- [x] Phase 1: Normative Clarification (3/3 plans) — completed 2026-08-19
- [x] Phase 2: Owner Approval (1/1 plan) — completed 2026-08-19
- [x] Phase 3: Independent Review (1/1 plan) — completed 2026-08-20
- [x] Phase 4: Legacy Governance Retirement (1/1 plan) — completed 2026-08-20
- [x] Phase 5: Quality-Tool Ownership Boundaries (1/1 plan) — completed 2026-08-21
- [x] Phase 6: Implementation Conformance Audit (0 formal plans) — completed 2026-08-21
- [x] Phase 7: Gap Remediation (0 formal plans) — completed 2026-08-21
- [x] Phase 8: Full Verification (1/1 plan) — completed 2026-08-22

[Archived roadmap and phase details](milestones/v1.0-ROADMAP.md)

</details>

### 🚧 v1.1 Executable Core (In Progress)

**Milestone Goal:** Turn the reference implementation from one executable transition into an executable
core, where every gate result is either checked mechanically or attributed to a verified human, and the
engine, not the agent, decides what may happen next.

**Phase numbering restarts at 1 in each milestone** (`--reset-phase-numbers`). The eight phases below
are the **v1.1** Phases 1–8 and are a different set from the shipped, archived **v1.0** Phases 1–8
above (archive: `milestones/v1.0-ROADMAP.md`, `milestones/v1.0-phases/`). Outside this section, qualify
the number. For example, v1.0 Phase 2 and v1.1 Phase 3 are both an Owner Approval gate, and v1.0
Phase 3 and v1.1 Phase 4 are both an Independent Review gate, but each belongs to its own milestone's
change.

This milestone turns the GG-SAD reference implementation from one executable transition into an
executable core, on the evidence of a prototype and eleven owner decisions (O-1 to O-11). It first
records those decisions, then drafts a normative amendment that specifies two profiles (`core` and
`full`) and the protections the prototype exercised, gates that amendment behind two independent hard
checkpoints (explicit repository-owner approval, then an independent review by a reviewer that is not
the Requestor), and only then builds the `core` engine, its trust and integrity layer, and its
workflow surface in `src/ggsad/`. It closes with an audit of the implementation against the *approved*
specification, adversarial tests for each protection, and a clean full verification baseline captured
as evidence. The `full` profile is specified but deliberately not built; the engine refuses it. The
prototype is a design reference and test oracle, not conformance evidence for this repository.

**Structure mode:** Horizontal Layers — a sequential specification-then-implementation process with
hard approval gates, not iterative user-facing feature slices. Each phase is a layer the next phase
depends on. Implementation follows approved text, never the reverse.

**Execution settings (from config.json):** sequential, non-parallel execution
(`parallelization: false`); manual/interactive phase advancement with explicit confirmation at each
gate (`mode: interactive`, `auto_advance: false`); no autonomous execution.

**Hard gates:** v1.1 Phase 3 (Owner Approval) and v1.1 Phase 4 (Independent Review) MUST NOT be
bundled with any other phase's work and MUST NOT be skipped or merged. Phases 5 to 8 MUST NOT start
until Phase 4 passes. Independence in Phase 4 means a reviewer that is not the Requestor, and not a
fresh context or subagent of the Requestor.

**Notes:**

- *Suggestion, not an owner decision:* v1.0 completed Phases 6 and 7 without formal plans and had to
  ratify them retroactively (finding PROC-01 in
  `milestones/v1.0-phases/06-implementation-conformance-audit/06-RETROACTIVE-REVIEW.md`). Require a
  plan before work in every v1.1 phase, with no retroactive closure.

- *Decided:* the Phase 4 reviewer. Requestor is Claude Code; the independent reviewer is Devin CLI
  (`devin -p`), recorded in `PROJECT.md` Key Decisions.

**Phase checklist (v1.1):**

- [ ] **Phase 1: Decision Record** - Record the owner's eleven decisions (O-1 to O-11) in one document before any normative text is drafted
- [ ] **Phase 2: Normative Drafting** - Produce a proposed diff to the normative specification covering SPEC-01 to SPEC-18, with no change under `src/ggsad/`
- [ ] **Phase 3: Owner Approval** - Repository owner reviews and explicitly approves (or requests changes to) the exact Phase 2 diff — hard gate
- [ ] **Phase 4: Independent Review** - Independent review by a non-Requestor reviewer evaluates the owner-approved diff; blocking findings resolved — hard gate
- [ ] **Phase 5: State and Gate Engine** - Implement the `core` engine in `src/ggsad/`: state, gates, frozen approvals, scope, failure handling, questions, and profile resolution
- [ ] **Phase 6: Trust and Integrity** - Implement the verifier interface, a non-forgeable verifier, tamper-evident history with an optional anchor, text/binary hashing, and versioned migration
- [ ] **Phase 7: Workflow Surface** - Implement the CLI, isolated checkouts, the on-demand guard, baseline-aware gates and the verify-only CI check
- [ ] **Phase 8: Verification** - Audit the implementation against the approved specification, prove each protection with an adversarial test, and run the full baseline clean

#### Phase 1: Decision Record

**Goal**: Record the repository owner's decisions O-1 through O-11 (made 2026-10-23) in a single decision record in the repository, each stating the option chosen, before any normative text is drafted.
**Depends on**: Nothing (first phase)
**Requirements**: DEC-01
**Success Criteria** (what must be TRUE):

  1. A single decision record exists in the repository stating each of O-1 through O-11 with the option the owner chose (DEC-01)
  2. O-4 (state moves to JSON) is recorded as departing from the proposal's recommendation to keep YAML (DEC-01)
  3. The record exists before any normative text for this milestone is drafted (DEC-01)

**Plans**: 2/3 plans executed

Plans:
**Wave 1**

- [x] 01-01-PLAN.md — Write the decision record: tracer (frame, the O-4 entry with its explicit departure from the YAML recommendation, first checks), then the other ten entries in Proposed wording and the lean read-only check script, committed on a branch other than main

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-02-PLAN.md — Owner review packet and checkpoint on the committed text, then a separate follow-up commit setting each entry to Decided (owner-confirmed date)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 01-03-PLAN.md — Readiness check, owner authorizes the push, open the pull request to main (no merge, no push to main), owner rebase-merges, verify the confirmed record on origin/main before Phase 2 starts

#### Phase 2: Normative Drafting

**Goal**: Produce a proposed diff to `docs/method/GG-SAD_normative_method_specification.md` that specifies the protections the prototype exercised and the two profiles, as proposed text only. No file under `src/ggsad/` is touched in this phase.
**Depends on**: Phase 1
**Requirements**: SPEC-01, SPEC-02, SPEC-03, SPEC-04, SPEC-05, SPEC-06, SPEC-07, SPEC-08, SPEC-09, SPEC-10, SPEC-11, SPEC-12, SPEC-13, SPEC-14, SPEC-15, SPEC-16, SPEC-17, SPEC-18
**Success Criteria** (what must be TRUE):

  1. The diff fixes a change's gate definitions at approval so that a later edit blocks every operation except cancellation until re-approved, and defines three-valued gate results in which an unevaluable gate is never a failure and never counts toward a retry limit (SPEC-01, SPEC-02)
  2. The diff adds the normative fourth result `blocked` to section 22.2 and states that `rejected` means nothing was written and is never `changed` (SPEC-03)
  3. The diff defines assurance levels A0 to A2 and the signed-approval statement as normative, leaves verifiers optional, and states that an agent able to use a human's credentials can act as that human (SPEC-04)
  4. The diff distinguishes history consistency from completeness with an anchor requirement for high assurance, and defines scope, how it is measured, and isolation from unrelated uncommitted work (SPEC-05, SPEC-06)
  5. The diff defines recorded known-failure baselines and the hard/soft failure distinction with a bounded, recorded override (SPEC-07, SPEC-08)
  6. The diff records open questions as change state with structured answers that block specification approval and closure, defines evidence as executable and tied to a requirement, and makes the gate-command interpreter explicit and opt-in with its trust consequence stated (SPEC-09, SPEC-10, SPEC-11)
  7. The diff specifies both profiles, `core` and `full`, states which requirements apply to which and how a change moves between them, revises `full` to carry the protections as invariants, marks it specified-but-not-implemented, and gives each `full` rule an acceptance example (SPEC-12, SPEC-14)
  8. The diff specifies state as JSON (`state.json`) with a canonical hashing form, the six-layer profile resolution order with `core` implementing four layers, `reopen` for `full` only, and `schema_version` with explicit recorded migration (SPEC-15, SPEC-16, SPEC-17, SPEC-18)
  9. No file under `src/ggsad/` is modified as part of producing this diff (SPEC-13)

**Plans**: TBD

#### Phase 3: Owner Approval

**Goal**: The repository owner reviews the exact proposed normative diff from Phase 2 and records explicit approval, or specific requested changes, before independent review begins. This is a hard gate — it cannot complete without the owner's explicit recorded approval of the diff exactly as it will be merged, and it MUST NOT be bundled with any other phase's work.
**Depends on**: Phase 2
**Requirements**: APPR-01
**Success Criteria** (what must be TRUE):

  1. The repository owner has reviewed the exact diff produced in Phase 2, covering SPEC-01 through SPEC-18 (APPR-01)
  2. The owner has recorded explicit approval, or specific requested changes, before independent review begins (APPR-01)
  3. This phase does not close until an explicit recorded owner approval exists for the diff exactly as it will be merged (APPR-01)

**Plans**: TBD

#### Phase 4: Independent Review

**Goal**: An independent review by a reviewer that is not the Requestor — and not a fresh context or subagent of the Requestor — evaluates the owner-approved diff and returns findings with stable IDs, severity and exact references. For this milestone the Requestor is Claude Code and the reviewer is Devin CLI. All blocking findings are resolved or explicitly dispositioned by the owner before this phase closes. This is a hard gate — independence must be structurally real, and this phase MUST NOT be bundled with any other phase's work.
**Depends on**: Phase 3
**Requirements**: REVIEW-01, REVIEW-02
**Success Criteria** (what must be TRUE):

  1. An independent review by a reviewer that is not the Requestor — and not a fresh context or subagent of the Requestor — evaluates the owner-approved diff (REVIEW-01)
  2. Review findings carry stable IDs, severity and exact references (REVIEW-01)
  3. All blocking findings are resolved (fixed) or explicitly dispositioned by the owner before the diff is treated as final (REVIEW-02)

**Plans**: TBD

#### Phase 5: State and Gate Engine

**Goal**: Implement the `core` profile's engine in `src/ggsad/` against the approved specification: the state model and transitions, gate evaluation, frozen gates and content-hash approvals, scope and failure handling, open questions, the refusal of the `full` profile, and profile resolution over four layers.
**Depends on**: Phase 4 (hard gate: Phase 4 must have passed before any work here starts)
**Requirements**: ENG-01, ENG-02, ENG-03, ENG-04, ENG-05, ENG-06, ENG-07
**Success Criteria** (what must be TRUE):

  1. For the `core` profile, every transition of the approved table is implemented; a rejected attempt writes nothing, a blocked attempt is recorded, and no operation leaves state partially written (ENG-01)
  2. The gate evaluator follows the approved evaluation order and returns three-valued results (ENG-02)
  3. Frozen gates, content-hash approvals and their staleness are implemented (ENG-03)
  4. Scope evaluation and hard/soft failure behaviour, including bounded overrides, are implemented (ENG-04)
  5. Open questions, structured answers and the approval block are implemented (ENG-05)
  6. A change that selects the `full` profile is refused with a clear message naming it as specified-but-not-implemented, and is never run as `core` silently (ENG-06)
  7. Profile resolution for `core` is implemented over its four layers, including the check that a change's gates cannot weaken the profile's base gates; this is unproven by the prototype beyond that check (ENG-07)

**Plans**: TBD

#### Phase 6: Trust and Integrity

**Goal**: Implement the verification and integrity layer the approved specification defines: a verifier interface, a verifier an agent cannot forge without the human's credentials, tamper-evident history with an optional anchor, correct hashing of text and binary content, and versioned migration.
**Depends on**: Phase 5
**Requirements**: TRUST-01, TRUST-02, INTEG-01, INTEG-02, INTEG-03
**Success Criteria** (what must be TRUE):

  1. A verifier interface exists, and the self-declared verifier is the default and is reported at the lowest assurance level (TRUST-01)
  2. At least one verifier cannot be forged by an agent that lacks the human's credentials, and verification fails closed (TRUST-02)
  3. State history is tamper-evident, and an optional external anchor detects truncation (INTEG-01)
  4. Hashing is defined for text and binary content, with line-ending normalisation applied to text only (INTEG-02)
  5. An unknown `schema_version` is refused with a clear message, and migrating existing artifacts, including `state.yaml` to `state.json`, is an explicit recorded command (INTEG-03)

**Plans**: TBD

#### Phase 7: Workflow Surface

**Goal**: Implement the commands and integrations that let a person and an agent use the engine: initialisation, change creation, approval, transition, check and review; isolated checkouts; an on-demand guard; baseline-aware gates with an explicit project interpreter; and a verify-only CI check.
**Depends on**: Phase 6
**Requirements**: WORK-01, WORK-02, WORK-03, WORK-04
**Success Criteria** (what must be TRUE):

  1. `init`, change creation, approval, transition, check and review commands exist with the approved result envelope and exit codes (WORK-01)
  2. Changes can run in isolated checkouts, and an on-demand guard that enforces hard failures can run from a hook or CI (WORK-02)
  3. Baseline-aware verification gates and an explicit, opt-in project interpreter are available (WORK-03)
  4. A verify-only CI check confirms history integrity (and the anchor), that frozen gates match the approval, that approvals are current and at the required level, scope against the base, and that no hard failure is active, without executing the change's own commands with CI's privileges; this is unproven by the prototype (WORK-04)

**Plans**: TBD

#### Phase 8: Verification

**Goal**: Audit the implementation against the *approved* specification, not against prototype results; prove each protection with an adversarial test that fails when the protection is removed; and run the complete verification baseline clean, capturing its output as evidence.
**Depends on**: Phase 7
**Requirements**: VERIFY-01, VERIFY-02, VERIFY-03
**Success Criteria** (what must be TRUE):

  1. A written list of evidenced conformance gaps exists, each with an exact reference, or an explicit statement that none exist (VERIFY-01)
  2. Each protection has an adversarial test that fails when the protection is removed: editing the gates, forging an approval, replaying a signature, truncating history, leaving scope (VERIFY-02)
  3. `uv sync --locked`, `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check src tests`, `uv run pytest` and `uv build` all run clean (VERIFY-03)
  4. The full command output is recorded as evidence (VERIFY-03)

**Plans**: TBD

## Progress

**Execution Order:**
Phases execute strictly in order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Phases 3 and 4 are hard gates and are
never merged with adjacent phases; Phases 5 to 8 do not start until Phase 4 passes. Manual, interactive
advancement only — no autonomous or parallel execution. The v1.0 phases are all complete and are
recorded in the collapsed block above; this table tracks the v1.1 phases only.

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Decision Record | v1.1 | 2/3 | In Progress|  |
| 2. Normative Drafting | v1.1 | 0/TBD | Not started | - |
| 3. Owner Approval | v1.1 | 0/TBD | Not started | - |
| 4. Independent Review | v1.1 | 0/TBD | Not started | - |
| 5. State and Gate Engine | v1.1 | 0/TBD | Not started | - |
| 6. Trust and Integrity | v1.1 | 0/TBD | Not started | - |
| 7. Workflow Surface | v1.1 | 0/TBD | Not started | - |
| 8. Verification | v1.1 | 0/TBD | Not started | - |
