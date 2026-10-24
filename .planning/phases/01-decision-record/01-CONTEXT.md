# Phase 1: Decision Record - Context

**Gathered:** 2026-10-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Write the repository owner's decisions O-1 through O-11 (made 2026-10-23) into one decision record in this repository, each stating the option chosen, before any normative text for this milestone is drafted (DEC-01). O-4 must say it departs from the proposal's recommendation to keep YAML.

The phase delivers a document and nothing else. It does not draft normative text (Phase 2), change `src/ggsad/`, or alter the requirements.

</domain>

<decisions>
## Implementation Decisions

### Location and form
- **D-01:** The record lives under a new tracked directory `docs/decisions/`, outside `.planning/`, so it is durable, citable from the normative specification and not moved by milestone archival. The exact file name is the planner's choice, dated and descriptive (for example `2026-10-23-executable-core-decisions.md`).
- **D-02:** One file with eleven entries, not an index plus per-decision files (DEC-01 and the roadmap say "a single decision record").
- **D-03:** Entries keep the identifiers O-1 to O-11, the ids the requirements, roadmap and seeds already cite. No renumbering and no mapping table.

### Entry content
- **D-04:** Each entry is a full ADR: context (the question), options considered, the option chosen stated in one sentence, rationale, consequences, and status. Facts for options and consequences come from the prototype repo's `MILESTONE-PROPOSAL.md` decisions table and its consequences list.
- **D-05:** O-4 states plainly that the proposal recommended keeping YAML and the owner chose JSON instead, with the reasoning behind the YAML recommendation in one or two sentences so the departure is understood, not just flagged. Human-owned definitions stay YAML (recorded as part of O-4's choice).
- **D-06:** Each entry lists its consequences (taken from the proposal), so Phase 2 knows the knock-on effects.

### Provenance and wording
- **D-07:** Rationale contains only what the owner stated, quoted or closely paraphrased from what the proposal records. Where no reason was recorded the entry says "rationale not recorded"; the owner may add one during review. The Requestor does not invent the owner's reasons. This limits the "full ADR" shape: the rationale field may be thin for several entries, which is accepted.
- **D-08:** The record is self-contained. Each entry carries the question, options and facts it needs. The prototype repo (`ggsad-core-proto`, commit `058d6c0`) is named once as the source, and nothing depends on it being reachable.
- **D-09:** Entries start with status "Proposed wording". After the owner reviews the committed diff, a follow-up commit sets each to "Decided (owner-confirmed <date>)". The decisions were made on 2026-10-23; the record states that date and, separately, the confirmation date.

### Authority and change
- **D-10:** The record is binding on Phases 2 to 8 until superseded. A deviation requires a new, dated owner decision in the record, not a silent change inside a phase.
- **D-11:** A decision changes by appending a new entry with the next free id (for example O-12) stating "supersedes O-n"; the superseded entry keeps its text and gets a "Superseded by" status line. Entries are never edited in place.
- **D-12:** Later requirements that already cite O-n (SPEC-03, 04, 12, 14 to 18, ENG-07, INTEG-03, WORK-04 and others) keep their citations and are not edited; the record only has to use the same ids. No additional orphan check is added to this phase.

### Claude's Discretion
- File name within `docs/decisions/`, the exact heading layout of an entry, and how the status line is displayed.
- The wording of context and consequences, provided it stays faithful to the proposal.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### This repository
- `.planning/ROADMAP.md` (Phase 1: Decision Record) - goal, dependency and success criteria 1 to 3
- `.planning/REQUIREMENTS.md` (DEC-01) - the requirement this phase satisfies; other requirements cite O-n ids
- `.planning/PROJECT.md` - Current Milestone section and Key Decisions (including the reviewer-rule row)
- `AGENTS.md` - repository rules: GSD is the sole method; normative changes need owner approval of the exact diff and independent review by a reviewer that is not the Requestor
- `.planning/reviews/2026-10-24-reviewer-rule-amendment.md` - evidence of the earlier amendment; a model for a self-contained evidence note
- `docs/method/GG-SAD_normative_method_specification.md` - the specification the later phases amend (this phase does not touch it)

### Source of the decisions (outside this repository; copy facts into the record)
- `C:\Dev\Repos\ggsad-core-proto\MILESTONE-PROPOSAL.md` (commit `058d6c0`) - the decisions table O-1 to O-11 with questions, the owner's recorded choices and the consequences list
- `C:\Dev\Repos\ggsad-core-proto\MAPPING.md` - the evidence behind the proposals the decisions refer to (P-01 to P-12)
- `C:\Dev\Repos\ggsad-core-proto\seed\README.md` - how the seeds relate to the proposal

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`: the earlier governing design document; a style reference for a dated governance document in this repo.
- `.planning/reviews/2026-10-24-reviewer-rule-amendment.md`: tracked, self-contained evidence note (table plus quoted report).

### Established Patterns
- Governance documents are Markdown under `docs/`; `.planning/` holds GSD working state and is archived per milestone.
- Commits are small conventional `docs:` commits; `main` is protected, so changes go through a pull request with a rebase merge (merge commits are refused), which changes commit hashes: do not cite commit hashes of this repository inside the record.

### Integration Points
- No code. Phase 2 (Normative Drafting) consumes the record: SPEC-12 cites O-1, SPEC-15 cites O-4, SPEC-16 cites O-2 and O-10, and so on.

</code_context>

<specifics>
## Specific Ideas

- Do not cite commit hashes of this repository in the record (rebase merges rewrite them); the prototype's hash is acceptable because that repo is not rebased.
- The owner confirms the record by reviewing the exact committed diff; the status change is a separate commit, so the reviewed text stays identifiable.

</specifics>

<deferred>
## Deferred Ideas

- A repository check that every O-n is cited by at least one requirement or criterion and every cited O-n exists in the record (offered and declined for this phase). Could become a verification item in Phase 8.

</deferred>

---

*Phase: 1-Decision Record*
*Context gathered: 2026-10-24*
