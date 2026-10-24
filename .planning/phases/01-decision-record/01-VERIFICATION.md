---
phase: 01-decision-record
verified: 2026-10-24T18:00:00Z
status: passed
score: 15/15 must-haves verified
behavior_unverified: 0
overrides_applied: 1
re_verification: false
gaps: []
human_verification: []
overrides:
  - must_have: "Nothing is merged by the agent: only the owner's rebase merge lands the record"
    reason: "The owner instructed the agent in-session to merge pull request 9 and then accepted the deviation; the outcome the prohibition protects (rebase merge, no direct push to main, no protection bypass, content unchanged) holds"
    accepted_by: "repository owner, answering in the orchestrating session"
    accepted_at: "2026-10-24T16:58:20.384Z"
---

# Phase 1: Decision Record Verification Report

**Phase Goal:** Record the repository owner's decisions O-1 through O-11 (made 2026-10-23) in a single decision record in the repository, each stating the option chosen, before any normative text is drafted (O-4 recorded as departing from the proposal's YAML recommendation).
**Verified:** 2026-10-24
**Status:** passed (goal achieved on origin/main; the agent-run merge was accepted by the owner as an override; the owner also confirmed all eleven entries in-session)
**Re-verification:** No, initial verification

## Goal Achievement

All checks ran against `origin/main` (fetched, head `d3e81a5`) and the working tree, not against the SUMMARY files. The record's blob id is `c78cde2b7ad76f85149b8898e10eca80c7492340` on `origin/main`, on the local branch and in the working tree, so the three agree byte for byte.

### Observable Truths

| #  | Truth | Status | Evidence |
|----|-------|--------|----------|
| 1  | RM-1: a single decision record states each of O-1 to O-11 with the option the owner chose | VERIFIED | `docs/decisions/2026-10-23-executable-core-decisions.md` on origin/main holds eleven `### O-n:` headings in order, each with a one-sentence Chosen. I compared every Chosen sentence with the decided text in `MILESTONE-PROPOSAL.md` at 058d6c0 (read directly from the prototype repo): all eleven match the decided outcome with no widening or narrowing. O-6 is stated as the hybrid (stays in full, dropped from core), not as a lettered option. |
| 2  | RM-2: O-4 is recorded as departing from the proposal's recommendation to keep YAML | VERIFIED | `grep -c 'The proposal recommended keeping YAML; the owner chose JSON instead\.'` prints 1; it opens the `- Departs from the proposal:` field of O-4, followed by two sentences of the YAML case drawn from the proposal's option wording and its O-4 risk bullet. Script check D1 passes on origin/main. |
| 3  | RM-3: the record exists before any normative text for this milestone is drafted | VERIFIED | `git diff --name-only 627a82a origin/main -- docs/method src` is empty, so no normative or source file changed after the pre-milestone commit. The record is on origin/main (pull request 9, state MERGED 2026-10-24T16:51:19Z). No Phase 2 artifact exists in `.planning/phases/`. |
| 4  | D-04/D-06: every entry has Status, Decision date, Context, Options considered, Chosen, Rationale, Consequences in order; Chosen is one sentence | VERIFIED | Script F1 and F2 pass on origin/main. Reading the file confirms the layout in all eleven entries; O-3 and O-6 say `none listed in the proposal` where the proposal lists no consequence. |
| 5  | D-07: a rationale appears only where the proposal records one | VERIFIED | `grep -c '^- Rationale: rationale not recorded'` prints 10. O-6 alone states a reason (the decided text's own "it is phase-based"). Consequence remarks (for example the O-4 readability note) were not promoted into rationale. The O-2 candidate reason in PROJECT.md was offered to the owner in the evidence note and not adopted. |
| 6  | D-01/D-02/D-03: one tracked file in `docs/decisions/`, ids O-1..O-11 unrenumbered, no mapping table | VERIFIED | `git ls-tree --name-only origin/main docs/decisions/` lists one file. Script H1 confirms ids 1..11 in numeric order, each once. No table in the file. |
| 7  | D-08: self-contained; prototype named once with 058d6c0; no repo commit hash, path, link, prototype id or bare requirement id | VERIFIED | Script X1 and X2 pass on origin/main. I also grepped for debt markers (TBD, FIXME, XXX, TODO) in the record, script and evidence note: none. |
| 8  | D-09: Status Proposed wording at review, then a separate flip commit to `Decided (owner-confirmed 2026-10-24)`; header carries the confirmation date separately from 'Decisions made: 2026-10-23' | VERIFIED | `grep -c '^- Status: Decided (owner-confirmed 2026-10-24)$'` prints 11; header has `Decisions made: 2026-10-23` and `Owner confirmation: 2026-10-24`. History on origin/main: review packet, owner reply, flip (`git log --format=%s origin/main`). The last commit touching the record (`3bc7e8d`) has numstat 12/12 and touches only the record; its parent blob is `b4cc0844374dca8a5fe5ce70711937b1e6746bc3`, equal to the evidence note's Reviewed blob, and that blob hashes to the noted SHA-256 `2b26dd35...20e9`. |
| 9  | D-10/D-11: 'Using this record' states binding on Phases 2 to 8 and the append-only supersession rule | VERIFIED | Present in the file under `## Using this record` (Binding, Changing, Status values, Rationale, Ids bullets). |
| 10 | D-12: lines in REQUIREMENTS.md citing O-n were not edited | VERIFIED | Script G1 passes (`O-n citations in REQUIREMENTS.md untouched`); `.planning/REQUIREMENTS.md` is not among the 13 files of pull request 9. |
| 11 | Faithful restatement: Chosen sentences carry the decisive phrases; O-2 reversal scope, O-3 split, O-10 four layers, O-11 verify-only are exact | VERIFIED | Read against the proposal text at 058d6c0. One point to note: O-8/O-1/O-9 Consequences reuse the proposal's 'Two profiles' sentence, attributed as shared. No invented fact found. |
| 12 | Encoding: UTF-8 without BOM, LF only, one final LF, on tree and committed blob | VERIFIED | Script E1 and E2 pass with `--ref origin/main`. |
| 13 | Scope: the pull request changed only `docs/decisions/` and `.planning/` paths | VERIFIED | `gh pr view 9 --json files` lists 13 paths, all under `docs/decisions/` or `.planning/`. No change to `docs/method/`, `src/`, `AGENTS.md`, `CLAUDE.md`. Script G1 passes. |
| 14 | Delivery: reached main through a PR with a rebase merge, no merge commit, no push to main, content unchanged by the rebase | VERIFIED | `origin/main` history is linear with no merge commit. Blob on origin/main equals the blob confirmed on the branch. The rebase rewrote commit hashes (old hashes cited in the older summaries no longer resolve, as the orchestrator said); this is not a defect. |
| 15 | Plan prohibition: the agent merges nothing; only the owner's rebase merge lands the record (01-03) | VERIFIED as to outcome, flagged as to process | The record landed by rebase merge and nothing was pushed to main, but 01-03-SUMMARY.md records that the agent ran the merge on the owner's instruction. See Human Verification item 1 and the override suggestion below. Counted toward the score because the outcome the prohibition protects (a rebase merge, no direct push, no bypass) holds; the process question is routed to the owner. |

**Score:** 15/15 truths verified (0 present, behavior-unverified; 1 carries a flagged prohibition)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `docs/decisions/2026-10-23-executable-core-decisions.md` | Frame plus eleven entries, owner-confirmed | VERIFIED | 226 lines; substantive; blob `c78cde2b...7340` on origin/main. |
| `.planning/phases/01-decision-record/01-check-decision-record.sh` | Read-only check script, checks E1 E2 H1 F1 F2 D1 S1 X1 X2 G1 | VERIFIED | Runs; RESULT: PASS on origin/main with `--stage confirmed --date 2026-10-24 --scope-base origin/main`. Mutation spot checks behave correctly: deleting the O-5 heading gives `FAIL H1` and `FAIL F1`; running stage `proposed` on the confirmed record gives `FAIL S1`. |
| `.planning/reviews/2026-10-24-decision-record-owner-confirmation.md` | Evidence note with reviewed blob, SHA-256, owner reply, date | VERIFIED | Present on origin/main; blob and SHA-256 recomputed and match; owner reply and `2026-10-24` filled in. Closing disclaimer present. |
| `01-01-SUMMARY.md`, `01-02-SUMMARY.md` | Summaries | VERIFIED | On origin/main. |
| `01-03-SUMMARY.md` | Delivery summary | VERIFIED | Local branch only, by design (it reaches main via a later pull request). Its claims were checked against origin/main and hold. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| check script | the record | default `--file` path and `--ref` blob read | WIRED | Script run with `--ref origin/main` reads the blob and passes. |
| evidence note | the record | Reviewed blob equals the flip commit's parent blob | WIRED | `b4cc0844...6bc3` equals `git rev-parse <flip>~1:<record>`. |
| requirements/roadmap O-n citations | record ids | same ids O-1..O-11 | WIRED | REQUIREMENTS.md cites O-1 to O-11 (SPEC-03, 04, 12, 14 to 18, ENG-07, INTEG-03, WORK-04); every cited id exists in the record. No orphan checker built, as D-12 requires. |

### Data-Flow Trace (Level 4)

Not applicable: documentation phase, no rendered dynamic data.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Record on main passes the confirmed-stage check | `bash 01-check-decision-record.sh --ref origin/main --stage confirmed --date 2026-10-24 --scope-base origin/main` | all ten checks PASS, `RESULT: PASS` | PASS |
| Missing entry is caught | same, `--file` on a copy with the O-5 heading deleted | `FAIL H1`, `FAIL F1`, `RESULT: FAIL 2` | PASS |
| A Decided record cannot pass as proposed | `--stage proposed` on the current record | `FAIL S1` | PASS |
| Flip commit touches 12 lines | `git diff --numstat <flip>~1 <flip> -- <record>` | `12 12` | PASS |

### Probe Execution

Step 7c: the phase declares one probe, the check script, which was run above in the Behavioral Spot-Checks. No `scripts/*/tests/probe-*.sh` files exist for this phase.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| DEC-01 | 01-01, 01-02, 01-03 (all three list `requirements: [DEC-01]`) | O-1 to O-11 recorded in one decision record before any normative text, each stating the option chosen; O-4 departs from the YAML recommendation | SATISFIED | Truths 1 to 3 above. The only requirement mapped to Phase 1 in the REQUIREMENTS.md traceability table is DEC-01; no orphaned requirement. |

Note: `.planning/REQUIREMENTS.md` still shows DEC-01 as `[ ]` and `Pending`, and ROADMAP.md still shows Phase 1 unticked. The plans say the orchestrator ticks these at phase close, so this is expected, not a gap.

### Anti-Patterns Found

None. No TBD, FIXME, XXX, TODO or placeholder text in the record, script or evidence note; no stub entries (every field has substantive text); no repository commit hashes in tracked files.

### Human Verification Required

#### 1. Agent-run merge of pull request 9

**Test:** The owner confirms they told the agent to rebase-merge pull request 9, and decides whether to accept the deviation.
**Expected:** The owner accepts it. If accepted, add this to the frontmatter of this file:

```yaml
overrides:
  - must_have: "Nothing is merged by the agent: only the owner's rebase merge lands the record"
    reason: "Owner instructed the agent to rebase-merge pull request 9; outcome (rebase merge, no direct push to main, no protection bypass, content unchanged) holds"
    accepted_by: "<owner>"
    accepted_at: "<ISO timestamp>"
```

**Why human:** The plan 01-03 prohibition is `verification: test` and the repository gives no test for who merged; both the pull request author and the merger are the same account. An agent relaying that the owner said so is not consent.

#### 2. Owner spot-confirmation of the eleven decisions

**Test:** Glance at the eleven Chosen sentences and the O-4 departure text on origin/main.
**Expected:** They match the decisions made on 2026-10-23.
**Why human:** The reply is recorded in the evidence note, but the repository cannot prove who gave it, and only the owner can judge whether the proposal captured their decision.

### Gaps Summary

No gaps. The phase goal is achieved on origin/main: one record, eleven entries, each with the chosen option, O-4 explicitly departing from the YAML recommendation, owner-confirmed, delivered by rebase merge with identical content, and no normative text drafted before it. The status is human_needed solely because a plan-level prohibition (the agent merges nothing) was broken on an instruction the repository cannot attribute to the owner. This does not block Phase 2 on the evidence in the repository, but the flag should be resolved by the owner rather than absorbed.

---

_Verified: 2026-10-24_
_Verifier: Claude (gsd-verifier)_
