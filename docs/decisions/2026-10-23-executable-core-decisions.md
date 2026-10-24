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

### O-1: Fate of the heavy machinery

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: The specification defines eight phases, DoR/DoD pairs, size classes and a ten-rank
  hierarchy; the prototype ran four governed changes without any of them.
- Options considered: Three, from an earlier draft of the proposal: (a) keep as specified; (b)
  replace with the simplified core (four states, one gate list per change) as the new baseline;
  (c) keep both, as a full profile and a core profile.
- Chosen: Option (c) is chosen: both are kept as profiles, full (the specified phases, DoR/DoD
  pairs, size classes and hierarchy) and core (the simplified four-state model).
- Rationale: rationale not recorded
- Consequences: Full is revised and then refused by the engine until a later milestone; this is
  shared with O-8, O-9 and O-10. Resolution in core has four layers.

### O-2: Milestone 1 non-goals that are reversed

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: Milestone 1 (v1.0) listed profile resolution, a full gate engine, memory, MCP, a web UI,
  CI integration and multi-agent orchestration as out of scope; the question is which of these are
  reversed.
- Options considered: Two, as worded. An earlier draft proposed to bring a minimal gate engine in,
  allow only an on-demand guard from CI integration, and keep memory, MCP, a web UI and
  multi-agent orchestration out. The decided scope reverses everything except memory, MCP, a web
  UI and multi-agent orchestration.
- Chosen: Everything except memory, MCP, a web UI and multi-agent orchestration is reversed, so
  profile resolution, a gate engine (within the O-8 limit that core is built) and CI integration
  come back into scope.
- Rationale: rationale not recorded
- Consequences: The prototype has no evidence for profile resolution or for CI integration beyond
  its on-demand guard, so both are unproven; they need their own acceptance examples and are
  sequenced last within their phases. Memory, MCP, a web UI and multi-agent orchestration stay out,
  as in Milestone 1 (v1.0). The proposal required the project's Out of Scope list, which names
  profile resolution, a full gate engine and CI integration, to drop those lines at milestone
  start, with a reason and a pointer to O-2.

### O-3: Trust model

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: The question is whether assurance levels and signed approvals are normative or optional
  guidance.
- Options considered: Two, from the question itself: normative, or optional guidance. An earlier
  draft also proposed a split: levels and the statement format normative, and verifiers (SSH
  signature, platform review) optional.
- Chosen: Assurance levels and the signed-approval statement format are normative, and verifiers
  (SSH signature, platform review) are optional.
- Rationale: rationale not recorded
- Consequences: none listed in the proposal

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

### O-5: A fourth result, blocked

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: The question is whether the result envelope gains a fourth result named `blocked`.
- Options considered: Two, from an earlier draft of the proposal: make it normative, or state that
  blocked attempts are not recorded and give retry limits another mechanism.
- Chosen: `blocked` is a normative fourth result.
- Rationale: rationale not recorded
- Consequences: Section 22.2 of the specification lists four results, and the transition table
  must say, per action, which of `rejected` and `blocked` applies. The proposal treats the change
  of the prototype's recorded results from `rejected` to `blocked` as a migration (see O-7).

### O-6: Reopen

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: The specification requires `reopen`; the prototype replaced it with "follow with a new
  change".
- Options considered: Two, from an earlier draft of the proposal: keep `reopen`, or amend the
  specification. The decided outcome is neither a plain keep nor a plain amend; it is stated in
  Chosen.
- Chosen: `reopen` stays in full (it is phase-based) and is dropped from core, where a closed
  change is followed by a new one.
- Rationale: The decided text itself gives one reason, that `reopen` is phase-based; any further
  rationale is rationale not recorded.
- Consequences: none listed in the proposal

### O-7: Compatibility and schema versions

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: The schemas are pinned to `0.1` with no migration path.
- Options considered: One, from an earlier draft of the proposal: define `schema_version` handling
  and a migration rule before any format change; alternatives not recorded.
- Chosen: Every artifact carries `schema_version`, the engine refuses an unknown version, and
  migration is an explicit, recorded command, never silent.
- Rationale: rationale not recorded
- Consequences: The three schemas are pinned to `0.1` today with no path forward. The rename of
  the state file in O-4 and the prototype's own change of recorded results from `rejected` to
  `blocked` are both migrations that did not exist before.

### O-8: How much of the full profile this milestone builds

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: This question was created by O-1. Implementing the eight-phase model is the large piece
  that Milestone 1 (v1.0) left unbuilt.
- Options considered: One, from an earlier draft of the proposal, which marked it open: specify
  both profiles, implement core first, and mark full as specified but not implemented until a
  later milestone; alternatives not recorded.
- Chosen: Specify both profiles and build core only; full is specified but not built, and the
  specification marks it as such.
- Rationale: rationale not recorded
- Consequences: Full is revised and then refused by the engine until a later milestone; this is
  shared with O-1. The proposal's out-of-scope list says that full is specified but not built. The
  proposal lists the risk that a specified-but-unbuilt full hides contradictions in untested text:
  the independent review of the first normative diff of Milestone 1 (v1.0) found two blocking gaps
  in the transition table that executable checking would have caught. The mitigation it gives is
  to keep full small, mark it clearly, give each rule an acceptance example, and let the engine's
  refusal stop anything from running it.

### O-9: Whether the new protections apply to both profiles

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: The question is whether the new protections (frozen gates, tri-state results, trust
  levels, the scope gate and known-failure baselines) apply to both profiles.
- Options considered: alternatives not recorded; the question asks whether the protections apply
  to both profiles.
- Chosen: The protections are invariants of both profiles, so full inherits them and is revised to
  carry them.
- Rationale: rationale not recorded
- Consequences: Full is revised and then refused by the engine until a later milestone; this is
  shared with O-1.

### O-10: Resolution layers that core implements

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: Raised by O-2. Section 5.3 of the normative specification defines six resolution
  layers; the question is which of them core implements.
- Options considered: alternatives not recorded; the proposal splits the six layers into four that
  core implements and two (change-class requirements and integration mappings) that are specified
  but not built.
- Chosen: Of the six resolution layers, core implements four: the invariant core, the profile,
  project configuration and the change's own gates.
- Rationale: rationale not recorded
- Consequences: Change-class requirements and integration mappings are specified for full and
  combination use but not built. Resolution in core has four layers. Combination mode is specified
  but not built.

### O-11: What CI integration means

- Status: Proposed wording
- Decision date: 2026-10-23, by the repository owner
- Context: Raised by O-2. A change's check commands are code supplied by the pull request.
- Options considered: alternatives not recorded; the decided text excludes one approach, executing
  the change's own commands with CI's privileges.
- Chosen: CI integration is verify-only: CI checks history integrity (and the anchor), that the
  frozen gates match the approval, that approvals are current and at the required level, scope
  against the base, and that no hard fail is active, and it does not execute the change's own
  commands with CI's privileges.
- Rationale: rationale not recorded
- Consequences: CI proves the record, not the outcome. Because CI does not run the change's
  commands, it cannot confirm that the tests pass; it confirms that the recorded result is intact,
  approved and within scope. Actually running the tests stays a separate job the repository
  already has.
