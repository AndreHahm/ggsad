# Executable Core Decisions (O-1 to O-11)

## Status and authority

- Decision owner: repository owner
- Decisions made: 2026-10-23
- Owner confirmation: pending
- Requestor: Claude Code
- Applies to: the Executable Core milestone (v1.1)
- Source: The decided outcomes and the consequences are copied from `MILESTONE-PROPOSAL.md` in the
  prototype repository `ggsad-core-proto` at commit `058d6c0`; option wording that was still open
  at the time for O-1 to O-8 is copied from earlier drafts of the same file; nothing in this
  record depends on that repository being reachable.

This record states decisions. It does not draft normative text, change `src/ggsad/` or alter any
requirement.

## Using this record

- Binding: the decisions bind Phases 2 to 8 of the Executable Core milestone until superseded, and
  a deviation needs a new, dated owner decision entered here, not a silent change inside a phase.
- Changing: a decision changes only by appending an entry with the next free id (for example
  O-12) whose `- Supersedes: O-n` field names the old one; the old entry keeps its text and only
  its Status line changes, to `Superseded by O-12`; entries are never edited in place.
- Status values: exactly `Proposed wording`, `Decided (owner-confirmed YYYY-MM-DD)` and
  `Superseded by O-n`; an entry stays Proposed wording until the owner has reviewed the committed
  text, and only the owner's confirmation moves it to Decided.
- Rationale: the literal `rationale not recorded` marks a reason the owner did not state; the
  Requestor supplies no reasons and the owner may add one when reviewing.
- Ids: O-n ids are never renumbered; requirements and the roadmap cite them.

## Requestor notes

- Options for O-1 to O-8 come from earlier drafts of the proposal's decisions table; for O-9 to
  O-11 the proposal records no earlier options, so those entries say `alternatives not recorded`
  where that applies.
- The proposal records the owner's outcomes and rarely a reason, so entries reading `rationale not
  recorded` are open for the owner to complete during review.
- The proposal says it recommended keeping YAML but records no reasoning for that recommendation,
  and the O-4 sentences use only statements the proposal does record.
- This record cites no requirement ids and changes no requirement; the O-n citations in the
  requirements and the roadmap stay untouched.

## Decisions

### O-4: State format

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: The prototype hashes a canonical JSON state, while the examples in the specification are
  YAML; the question is which format state should use.
- Options considered: Two, from an earlier draft of the proposal: keep YAML and define a canonical
  form for hashing, or move state to JSON.
- Chosen: State moves to JSON in `state.json`, and human-owned definitions stay YAML.
- Departs from the proposal: The proposal recommended keeping YAML; the owner chose JSON instead.
  Keeping YAML needed only a defined canonical form for hashing. The proposal's own risk note says
  that with JSON humans lose easy reading and hand-editing of state.
- Rationale: rationale not recorded; the proposal states the owner's choice but no reason for it.
- Consequences: The state file name changes from `state.yaml` to `state.json` in the specification
  (sections 4.3, 8 and 22 and the templates), in the subject of `.ggsad/schemas/state.schema.json`,
  in `specs/examples/class-m/state.yaml` and in the archived CHG-001 state. Existing state files
  need the migration decided in O-7. State is engine-owned and not meant to be hand-edited, which
  the proposal gives as the reason readability weighs less. The proposal lists the risk that
  humans lose easy reading and hand-editing of state, with the mitigation that state is
  engine-owned, `check` and `review` are the human views, and the choice is revisited if people
  end up editing it.
