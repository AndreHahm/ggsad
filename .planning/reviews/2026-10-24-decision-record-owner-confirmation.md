# Owner confirmation: decision record O-1 to O-11

| Field | Value |
|---|---|
| Reviewed file | `docs/decisions/2026-10-23-executable-core-decisions.md` |
| Reviewed blob | `b4cc0844374dca8a5fe5ce70711937b1e6746bc3` |
| Reviewed SHA-256 | `2b26dd3553d6daf5868335bdb3690773de398c76e9e9a4737c904fb7380520e9` |
| Check results | `RESULT: PASS` (ten checks E1, E2, H1, F1, F2, D1, S1, X1, X2, G1 pass in stage proposed) |
| Owner reply | Given through the interactive question tool. Question: "Do you confirm all eleven record entries exactly as committed (blob b4cc0844…, Proposed wording), including the O-4 departure text?" Answer: "Confirm all eleven". Question: "Which date is your confirmation date?" Answer: "2026-10-24". The owner requested no changes and added no rationale. |
| Confirmed on | `2026-10-24` |

The blob id is the git object id of the record as committed; the SHA-256 is that blob's content
hashed. Neither changes when the branch is rebased or rebase-merged, so both identify the text
the owner reviews. Every entry reads `Proposed wording` and the header reads
`Owner confirmation: pending`.

## For the owner to look at

How to review: open `docs/decisions/2026-10-23-executable-core-decisions.md`, or run
`git diff origin/main...HEAD -- docs/decisions/2026-10-23-executable-core-decisions.md`.

### Entries that read `rationale not recorded`

Ten entries state no reason: O-1, O-2, O-3, O-4, O-5, O-7, O-8, O-9, O-10 and O-11. You may supply a
reason for any of them in your reply; it is inserted in your own words and nothing else is adopted.
O-4 reads `rationale not recorded; the proposal states the owner's choice but no reason for it`.

O-6 is the one entry whose Rationale states a reason: the decided text itself says `reopen` is
phase-based; any further rationale is `rationale not recorded`.

### Candidate reasons found elsewhere in the repository (not adopted)

The Requestor has not adopted any of these. Say so in your reply if you want one used, in your own
words.

- O-2, from `.planning/PROJECT.md`, Key Decisions row "Profile resolution, a gate engine and CI
  integration removed from Out of Scope": "Owner decision O-2 in the next-milestone proposal: the
  v1.0 non-goals applied to the clarification-only milestone, and the next milestone needs them.
  Memory, MCP, a web UI and multi-agent orchestration stay out of scope."
- O-8, from `.planning/REQUIREMENTS.md`, Out of Scope table, row "Running the `full` profile in the
  engine": "Specified but not built (O-8); ENG-06 refuses it". This states what O-8 means, not why
  it was decided.
- No candidate reason was found for O-1, O-3, O-4, O-5, O-7, O-9, O-10 or O-11 in
  `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md` or `.planning/ROADMAP.md`.

### O-4: the departure from the proposal

Quoted in full from the record:

> Departs from the proposal: The proposal recommended keeping YAML; the owner chose JSON instead.
> Keeping YAML needed only a defined canonical form for hashing. The proposal's own risk note says
> that with JSON humans lose easy reading and hand-editing of state.

The proposal records no reasoning for its YAML recommendation. The two reasoning sentences (keeping
YAML needed only a defined canonical form for hashing; the risk note on readability and
hand-editing) use only the proposal's option wording and risk note. Correct them if they misstate
the case.

### O-6: neither plain keep nor plain amend

The specification requires `reopen`; the prototype replaced it with a new change. The decided
outcome is that `reopen` stays in full and is dropped from core, so it is neither keeping nor
amending the specification as a whole. Check that this matches your decision.

### The eleven Chosen sentences

Compare each with the decision you made on 2026-10-23.

- O-1: Option (c) is chosen: both are kept as profiles, full (the specified phases, DoR/DoD pairs, size classes and hierarchy) and core (the simplified four-state model).
- O-2: Everything except memory, MCP, a web UI and multi-agent orchestration is reversed, so profile resolution, a gate engine (within the O-8 limit that core is built) and CI integration come back into scope.
- O-3: Assurance levels and the signed-approval statement format are normative, and verifiers (SSH signature, platform review) are optional.
- O-4: State moves to JSON in `state.json`, and human-owned definitions stay YAML.
- O-5: `blocked` is a normative fourth result.
- O-6: `reopen` stays in full (it is phase-based) and is dropped from core, where a closed change is followed by a new one.
- O-7: Every artifact carries `schema_version`, the engine refuses an unknown version, and migration is an explicit, recorded command, never silent.
- O-8: Specify both profiles and build core only; full is specified but not built, and the specification marks it as such.
- O-9: The protections are invariants of both profiles, so full inherits them and is revised to carry them.
- O-10: Of the six resolution layers, core implements four: the invariant core, the profile, project configuration and the change's own gates.
- O-11: CI integration is verify-only: CI checks history integrity (and the anchor), that the frozen gates match the approval, that approvals are current and at the required level, scope against the base, and that no hard fail is active, and it does not execute the change's own commands with CI's privileges.

This note is evidence only. It does not change the reviewed file.
