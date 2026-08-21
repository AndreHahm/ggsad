# Independent Review — PR #3 Rebase SHA Reconciliation

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer, read-only (no edits, commits, pushes, or GitHub comments
  made as part of this review, per the review prompt's explicit constraint)
- Requestor: Codex (and/or the repository owner)
- Reviewed artifact: the complete uncommitted documentation diff on branch
  `chore/pr-3-rebase-sha-reconciliation` against `origin/main`, together with
  `.planning/milestones/PR-3-REBASE-SHA-RECONCILIATION.md`
- Reviewed against: rebased `main` tip `2a10641fd4af11b1f93929957d5d8442aa9198e3`
- Worktree: `C:\Dev\Repos\ggsad-worktrees\pr-3-sha-reconciliation`
- Review date: 2026-08-21
- Action: Independent verification of a mechanical stale-SHA reconciliation following PR #3's
  rebase merge
- Result: **Findings.** Two issues, neither touching the mapping's correctness — see below.
- Scope: Full diff review plus independent recomputation, not reliance on the reconciliation
  record's own assertions. No repository files were modified as part of this review.

## Method

Recomputed everything independently rather than trusting the record:

- Located the fork point (`git merge-base origin/bootstrap-gsd-transition origin/main` =
  `5d79f2fa2fec354c72170fc7781ccc4225c42ddf`) and confirmed 69 commits unique to each side.
- Computed `git patch-id --stable` for all 69 old (pre-rebase) and all 69 new (rebased) commits
  independently; compared patch-id sets for exact equality, checked for duplicates, and verified
  subject-line agreement on every matched pair.
- Cross-checked all 34 rows of the reconciliation table against this independently computed
  mapping — exact match, zero mismatches.
- Verified the table's completeness claim by extracting every SHA-like token (both 40-char and
  short 7-char forms) actually removed by the diff, resolving each to its full old hash, and
  confirming the resulting set is exactly the 34 rows in the table (no more, no fewer).
- Traced all 103 individual removed-SHA diff lines to their paired added-SHA replacement and
  confirmed each substitution used the specific, correctly-mapped new value — not merely "some
  valid new SHA."
- Grepped the entire tracked working tree for all 69 old hashes (both lengths) outside the
  reconciliation record itself.
- Located and individually verified every embedded `git diff`/`git show`/`git log` command across
  the modified evidence files, including the one two-sided range (`03-FOLLOW-UP-REVIEW.md`) — the
  highest-risk case for a partially-applied substitution.
- Ran `uv run ty check src tests` and bare `uv run ty check` in the worktree to confirm the
  record's baseline-condition claim (31 pre-existing diagnostics in `.claude/scripts/`) still
  holds and is correctly not attributed to this diff.
- Confirmed documentation-only scope via `git diff --name-only HEAD` against `docs/method/`,
  `src/`, `tests/`, `pyproject.toml`, `.ggsad/`, and `.claude/`.

## Findings

### F-01 — `01-BASELINE.txt` retains a pre-rebase SHA outside the reconciliation record (major)

**File:** `.planning/phases/01-normative-clarification/01-BASELINE.txt`, line 1

Contains the raw pre-rebase SHA `54f203668179d424395a237398ef06278ab0f5cd`, untouched by this
diff — a direct violation of the "no pre-rebase SHA outside the reconciliation record" requirement.
Not a missing-mapping problem: row 29 of the reconciliation table already correctly maps this exact
hash to `eaefb212a82e8d2e870d00bda052bc810949392e`; the file was simply never touched by the
mechanical replacement pass. Confirmed via full-tree grep that this is the only other file affected
— no systemic pattern beyond this single miss.

This file's documented purpose is "a durable pre-edit commit anchor," and
`01-VERIFICATION.md`'s Required Artifacts table checks that it "contains one resolvable
40-character commit SHA." That check currently passes only because `origin/bootstrap-gsd-transition`
still exists; once that ref is deleted (normal post-merge cleanup), the SHA becomes unreachable and
the artifact's own resolvability requirement silently breaks.

**Correction:** replace the file's content with `eaefb212a82e8d2e870d00bda052bc810949392e`.

### F-02 — Stale branch attribution alongside two correctly-rebased SHAs (moderate, two locations)

**Files:**
- `.planning/phases/01-normative-clarification/01-PAIR-REVIEW-FINDINGS.md`, line 11
- `.planning/phases/03-independent-review/03-PAIR-REVIEW-FINDINGS.md`, line 13

Both lines read `..., branch \`bootstrap-gsd-transition\`` immediately after a rebased SHA
(`c6d1209fdf9e8acedae1cca03a788a729933cb20` and `1a90ee74152be5ae82ed0fedde9a1db16826a470`
respectively). Verified with `git merge-base --is-ancestor` that neither SHA is reachable from
`origin/bootstrap-gsd-transition` — both exist only on `main`. The diff correctly swapped the hash
values but left an adjacent, independently-checkable claim (which branch the commit belongs to) now
false.

This directly bears on whether a central mapping table alone is sufficient for provenance: it is
not, wherever surrounding prose makes its own identity claim beyond citing the hash.

**Correction:** drop the trailing branch clause in both locations (the reconciliation record
already covers pre-rebase provenance centrally), or replace it with an accurate qualifier, e.g.
"now on `main` after PR #3's rebase — see the reconciliation record for the pre-rebase identity."

## Checklist confirmation

1. **Mapping validity — Confirmed.** All 69 patch-id pairs verified independently; all 34 table
   rows match independent computation exactly; zero subject-line mismatches.
2. **Stale-SHA cleanup — Rejected (partially).** 103 individual substitutions across the diff all
   resolved correctly; F-01 is a real, uncorrected leftover outside the diff's scope.
3. **Documentation-only scope — Confirmed.** No changes outside `.planning/` and
   `docs/superpowers/`; `docs/method/`, `src/`, `tests/`, `pyproject.toml`, `.ggsad/`, `.claude/`
   all unchanged. The 31 pre-existing `ty check` (bare) diagnostics reproduce exactly as described
   and are correctly not attributed to this diff.
4. **Provenance semantics — Rejected as currently written.** The mapping table itself is complete
   and correct, but F-02 shows it is not sufficient on its own wherever an evidence file's prose
   makes an independent claim about the commit's identity.

## Disposition

Open. F-01 should be corrected before this reconciliation is treated as complete — it directly
violates the "no pre-rebase SHA outside the reconciliation record" requirement and risks becoming
permanently unresolvable once the old branch is deleted. F-02 should be corrected for the evidence
records to remain unambiguous, though it does not affect the correctness of the mapping itself.

## Follow-up verification

- Verification date: 2026-08-21
- F-01: **Resolved.** `.planning/phases/01-normative-clarification/01-BASELINE.txt` now contains
  `eaefb212a82e8d2e870d00bda052bc810949392e`. Independently confirmed this is a resolvable commit
  and an ancestor of `origin/main` (`git merge-base --is-ancestor` succeeded).
- F-02: **Resolved.** Both `01-PAIR-REVIEW-FINDINGS.md` and `03-PAIR-REVIEW-FINDINGS.md` no longer
  attribute their rebased SHA to `branch \`bootstrap-gsd-transition\``; both now read "(rebased
  equivalent; original reviewed identity is recorded in
  `.planning/milestones/PR-3-REBASE-SHA-RECONCILIATION.md`)". Independently confirmed each rebased
  SHA is the correct patch-id-equivalent of its stated original identity via the reconciliation
  table, and that the referenced original identity is in fact present there.
  `PR-3-REBASE-SHA-RECONCILIATION.md` now explicitly documents that pre-rebase identities may
  appear in these two milestone records when a finding quotes one, which correctly accounts for the
  original identities quoted in this review document's own F-01/F-02 write-ups.
- Full-tree re-scan: searched all 983 tracked files (raw bytes, not text-decoded, so no file type
  was skipped) for all 69 pre-rebase SHAs, both 40-char and 7-char short forms. Zero hits outside
  `PR-3-REBASE-SHA-RECONCILIATION.md` and this review document.
- Scope: re-confirmed documentation-only — `docs/method/`, `src/`, `tests/`, `pyproject.toml`,
  `.ggsad/`, and `.claude/` remain untouched; no file outside `.planning/` or `docs/superpowers/`
  appears in the diff.
- New findings: **None.** Diffed the current working tree against the originally-reviewed diff,
  excluding the three files the corrections touched (`01-BASELINE.txt`,
  `01-PAIR-REVIEW-FINDINGS.md`, `03-PAIR-REVIEW-FINDINGS.md`) — every other file's diff content is
  byte-identical to what was originally reviewed.

**Final verdict: Verified**

**Disposition: Closed**
