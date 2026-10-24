# Phase 2: Normative Drafting - Context

**Gathered:** 2026-10-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce a proposed diff to `docs/method/GG-SAD_normative_method_specification.md` that specifies the protections the prototype exercised and the two method profiles (`core`, `full`), for SPEC-01 to SPEC-18. The output is proposed text only: nothing under `src/ggsad/` changes (SPEC-13), and the diff is not approved or reviewed in this phase (Phase 3 owner approval, Phase 4 independent review by Devin CLI; the Requestor is Claude Code).

The diff implements the eleven owner decisions O-1 to O-11 in `docs/decisions/2026-10-23-executable-core-decisions.md`, which bind this phase until superseded by a new dated owner decision.

</domain>

<decisions>
## Implementation Decisions

### Form of the diff
- **D-01:** The proposed text is written by editing `docs/method/GG-SAD_normative_method_specification.md` directly on the milestone branch (`gsd/v1.1-executable-core`). The diff is that file on the branch versus `origin/main`; no separate patch file is the artifact. `main` stays untouched until a pull request is merged. — **Reversibility:** reversible — a draft on a branch can be rewritten or reset before approval.
- **D-02:** The exact diff is identified for Phase 3 approval and Phase 4 review by git blob ids and SHA-256 recorded at the end of Phase 2 (the base blob on `origin/main` and the result blob), as Phase 1 did for the decision record. Commit hashes or ranges are not used as the identity, because a rebase merge rewrites them. Any later edit to the file invalidates the recorded values and requires recording new ones.
- **D-03:** Commits on the spec file are one per requirement (SPEC-01 to SPEC-18); closely related requirements may share a commit when separating them would leave an inconsistent text. Each commit subject names its requirement ids so a review finding maps to a commit.

### Method profiles versus compliance profiles
- **D-04:** The new method profiles `core` and `full` (O-1) and the existing compliance profiles of section 5.1 (`lean`, `standard`, `governed`, `regulated`) are separate axes. A project/change selects a method profile and a compliance profile; both are resolved in the section 5.3 order. The compliance profiles are kept unchanged. — **Reversibility:** costly — every later phase and the engine design cite this structure.
- **D-05:** The specification uses qualified terms, "method profile" for `core`/`full` and "compliance profile" for `lean` to `regulated`, wherever a bare "profile" would be ambiguous. The owner's O-1 wording ("profiles") is kept; no renaming (a rename would need a new dated owner decision in the record).
- **D-06:** In the six-layer resolution order of section 5.3 (SPEC-16, O-10), layer 2 "selected profile" means the pair method profile plus compliance profile, resolved together. The count stays six layers, and `core` implements layers 1, 2, 3 and 5 (invariant core, selected profile, project configuration, the change's own gates), exactly as O-10 decides. No seventh layer.
- **D-07:** A change's method profile is fixed when the change is created. To move between `core` and `full`, create a new change in the other profile and supersede the old one with the existing `supersede` action; no in-place switch and no mapping of the four `core` states onto the `full` phases is specified. — **Reversibility:** costly — an in-place switch could be added later only by a new dated owner decision plus a state mapping.

### Plan split, order and checks
- **D-08:** Phase 2 is planned as five theme plans, one wave each (all edit the same file, so they run in sequence): (1) profile vocabulary (SPEC-12); (2) gates and results (SPEC-01, 02, 03, 07, 08); (3) trust and integrity (SPEC-04, 05, 06, 09, 10, 11); (4) state and versioning (SPEC-15, 17, 18); (5) full-profile revision and resolution (SPEC-14, 16). SPEC-13 is a check in every plan, not a plan. SPEC-16, unproven by the prototype beyond a base-gate no-weakening check, is planned with its own acceptance examples in the last plan.
- **D-09:** Phase 2 includes a lean read-only check script, in the style of Phase 1's `01-check-decision-record.sh`. Its checks include: every SPEC id has a commit naming it; nothing under `src/ggsad/` changed; only `docs/method/` and `.planning/` are touched; normative-term and cross-reference sanity; LF endings and UTF-8 without BOM. The exact check list is the planner's choice.
- **D-10:** When the drafter meets an ambiguity that O-1 to O-11 do not settle, it drafts the most conservative reading, lists it in a per-plan "Drafting choices" list, and continues. Those lists are carried into the Phase 3 approval packet so the owner can overrule each choice at approval. The drafter does not stop execution for these and does not leave them as open questions in the normative text.

### Ripple scope
- **D-11:** Phase 2 touches only the specification text. Examples and templates written inside the specification are updated for `state.json` (SPEC-15). `specs/examples/class-m/state.yaml`, `.ggsad/templates/`, `.ggsad/schemas/state.schema.json` and the archived CHG-001 state are not changed in this phase, because the current implementation and tests validate them; they go on a hand-off list recorded for the engine phases (5 to 8).
- **D-12:** The specification's header is drafted as Version 1.4 with a new Revision line describing the change. The packet for Phase 3 states the number so the owner can change it at approval. — **Reversibility:** reversible — one header line.
- **D-13:** Acceptance examples for the `full` rules (SPEC-14) are written inline under each rule in Given/When/Then form, each with an id (for example AE-nn) that the rule cites, covering normal and failure/boundary behavior as section 3.9 requires, so rule, example and verification evidence stay traceable.

- **D-14:** For SPEC-14 the unit that needs an acceptance example is the rule unit (for example one transition-table row, one DoR/DoD pair, one size class), roughly 40 example sets, each covering normal and failure/boundary behavior; not every normative bullet and not one per section. Decided by the owner after the Phase 2 research found this the largest sizing risk.
- **D-15:** Research candidates that are judgment calls (research register DC-01 to DC-27 and open questions OQ-1, OQ-2, OQ-4, OQ-6, OQ-7) follow D-10: the drafter takes the most conservative reading and lists it for the Phase 3 packet. The specification does not cite the decision record or other development artifacts (OQ-5), keeping it self-contained.

### Claude's Discretion
- The order of requirement commits inside a plan, the exact checks of the lean script, the numbering and placement of new subsections and acceptance example ids, and the exact wording of rules, provided they follow D-01 to D-13, the section 2 normative terms and the Phase 1 record.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Decisions and requirements
- `docs/decisions/2026-10-23-executable-core-decisions.md` — owner decisions O-1 to O-11, binding on this phase (see "Using this record")
- `.planning/REQUIREMENTS.md` (SPEC-01 to SPEC-18) — the requirements this phase satisfies
- `.planning/ROADMAP.md` (Phase 2: Normative Drafting) — goal, dependency, success criteria 1 to 9
- `.planning/phases/01-decision-record/01-CONTEXT.md` — Phase 1 decisions (self-contained wording, no commit hashes of this repository, record binding until superseded)
- `.planning/PROJECT.md` — Current Milestone section and Key Decisions (reviewer-rule row)
- `AGENTS.md` and `CLAUDE.md` — owner approval of the exact diff and independent review for normative changes; GSD is the sole method

### The specification being amended
- `docs/method/GG-SAD_normative_method_specification.md` — section 2 (normative terms), 3.7 (invariant core), 3.9 (acceptance examples), 4.2/4.3 (state file), 5.1 to 5.3 (compliance profiles, tailoring, resolution), 8 (state model, transition table, reopen), 22 (automation contract, result envelope), header (Version 1.3)

### Source of the protections (outside this repository; copy facts into the spec, do not depend on them)
- `C:\Dev\Repos\ggsad-core-proto\MAPPING.md` (sections 1 to 6) — what the prototype exercised and contradicted (P-01 to P-12); the spec text must be self-contained and must not cite prototype-only ids
- `C:\Dev\Repos\ggsad-core-proto\MILESTONE-PROPOSAL.md` — decisions table and consequences list

### Hand-off list (recorded here, acted on in later phases)
- `specs/examples/class-m/state.yaml`, `.ggsad/templates/*.template.md`, `.ggsad/schemas/state.schema.json`, and the archived CHG-001 `state.yaml` — convert to `state.json` / the new schema when the engine is changed (not in Phase 2, D-11)
- Version "1.3" is pinned in `.ggsad/config.yaml` (line 10), `src/ggsad/application/initialize_project.py` (line 82) and `tests/unit/test_initialize_project.py` (line 61); the header change to 1.4 (D-12) leaves them stale until the engine phases update them (SPEC-13 forbids touching `src/ggsad/` in Phase 2)
- `.planning/phases/02-normative-drafting/02-RESEARCH.md` — spec impact map with per-requirement edit sites, conflicts T1-T20, Drafting-choice register DC-01 to DC-27 and the check-script design (read before planning)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `.planning/phases/01-decision-record/01-check-decision-record.sh`: model for the lean read-only check script (options, PASS/FAIL line format, `--ref`, scope checks).
- `.planning/reviews/2026-10-24-decision-record-owner-confirmation.md`: model for a packet that pins reviewed text by blob id and SHA-256.

### Established Patterns
- The earlier reviewer-rule amendment edited the specification on a branch and was approved and reviewed on an exact diff (Phase 3 and 4 repeat that for this milestone's diff).
- The specification already has a version/revision header, compliance profiles (section 5.1), a six-layer resolution order (section 5.3), eight statuses with `reopen` (section 8) and a three-valued result envelope (section 22.2).
- `src/ggsad/` currently implements `state.yaml`; it must stay untouched (SPEC-13).

### Integration Points
- Phase 3 (Owner Approval) consumes the blob ids, the per-plan "Drafting choices" lists and the diff; Phase 4 reviews the same blob; Phases 5 to 8 implement against the approved text and pick up the D-11 hand-off list.

</code_context>

<specifics>
## Specific Ideas

- The spec text must be self-contained: no prototype-only ids (P-nn), no commit hashes of this repository, no local paths.
- Version header: the owner chose Version 1.4 (the recommendation was 2.0); the packet states the number so it can be changed at approval.

</specifics>

<deferred>
## Deferred Ideas

- Conversion of `specs/examples/`, `.ggsad/templates/`, `.ggsad/schemas/state.schema.json` and the archived CHG-001 state to JSON — engine phases (hand-off list above).
- An in-place `core` to `full` switch with a state mapping — would need a new dated owner decision (D-07).

</deferred>

---

*Phase: 2-Normative Drafting*
*Context gathered: 2026-10-24*
