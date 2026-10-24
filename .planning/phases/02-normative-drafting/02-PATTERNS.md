# Phase 2: Normative Drafting - Pattern Map

**Mapped:** 2026-10-24
**Files analyzed:** 4 (1 modified spec, 1 new script, SUMMARY files, 1 packet note)
**Analogs found:** 4 / 4

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `docs/method/GG-SAD_normative_method_specification.md` | normative document | static reference | its own sections (mapped in 02-RESEARCH.md impact map) | exact (self) |
| `.planning/phases/02-normative-drafting/02-check-normative-diff.sh` | utility (read-only check script) | batch / transform (file + git in, PASS/FAIL lines out) | `.planning/phases/01-decision-record/01-check-decision-record.sh` | exact |
| `.planning/phases/02-normative-drafting/02-NN-SUMMARY.md` | evidence note | static record | `.planning/phases/01-decision-record/01-01-SUMMARY.md` (also 01-02, 01-03) | exact |
| `.planning/reviews/<date>-normative-spec-owner-approval.md` (Phase 3 packet, name is planner's choice) | evidence note / approval packet | static record | `.planning/reviews/2026-10-24-decision-record-owner-confirmation.md` | exact |

## Pattern Assignments

### `02-check-normative-diff.sh` (utility, batch)

**Analog:** `.planning/phases/01-decision-record/01-check-decision-record.sh` (364 lines). Copy the skeleton; replace the awk entry parser and X/G checks with the B1, E1-E3, S1, S2, C1, N1, X1, R1-R8, A1 checks from 02-RESEARCH.md (Validation Architecture).

**Header and contract** (lines 1-23): comment block with `Usage:` and one line per option; `Output:` line; exit codes; read-only guarantee. `usage()` re-prints lines 2-20 of itself.
```bash
#!/usr/bin/env bash
# Read-only check of ...
# Output: one line per check, "PASS ID message" or "FAIL ID message", then "RESULT: PASS" or
# "RESULT: FAIL N". Exit 0 on pass, 1 on any failed check, 2 on a usage error or an unreadable file.
# Nothing is written outside a temporary directory that is removed on exit.
set -u
export LC_ALL=C
cd "$(git rev-parse --show-toplevel)" || { echo "not inside a git repository" >&2; exit 2; }
```

**Constants then defaults then option parsing** (lines 25-61): upper-case constants for path and fixed text, then defaults, `usage()`, `need_value()`, a `while/case` loop. Add `--base REF` (default `origin/main`), `--base-blob ID` (default `da29d6f3bdef2e88fdd85a762939017d7d7034fa`), `--final`, `--version 1.4`; keep `--file` and `--ref`.
```bash
need_value() {
  if [ "$#" -lt 2 ] || [ -z "$2" ]; then echo "option $1 needs a value" >&2; exit 2; fi
}
while [ "$#" -gt 0 ]; do
  case "$1" in
    --file) need_value "$@"; FILE="$2"; shift 2 ;;
    --ref) need_value "$@"; REF="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
done
```
`--final` is a flag without a value: use `--final) FINAL=1; shift ;;` (no `need_value`).

**Ref validation** (lines 69-71) for `--base`:
```bash
git rev-parse --verify --quiet "$SCOPE_BASE^{commit}" > /dev/null || { echo "--scope-base $SCOPE_BASE is not a commit" >&2; exit 2; }
```

**Temp dir and reading the target** (lines 83-92): `mktemp -d`, `trap ... EXIT`, copy working-tree file or `git cat-file blob "$REF:$FILE"` to `$TMP/record`; unreadable gives exit 2. All checks then read `$REC`, never the original.

**Result helpers and check style** (lines 118-143): `pass ID msg` / `fail ID msg` increment `FAILS`; one `# ID: description` comment per check.
```bash
FAILS=0
pass() { echo "PASS $1 $2"; }
fail() { echo "FAIL $1 $2"; FAILS=$((FAILS + 1)); }
```

**Encoding checks, reusable verbatim for E1/E2** (lines 122-143): BOM via `head -c3 | od -An -tx1`, `iconv -f UTF-8 -t UTF-8`, CR count via `tr -cd '\r'`, final LF via `tail -c1`, trailing blank line via `tail -n1 | grep -q '[^[:space:]]'`. Add E3 (tab, trailing whitespace other than exactly two spaces) in the same shape.

**Awk-in-variable pattern** (lines 145-148, 267-272): program in a single-quoted `AWK_...='...'` with `# shellcheck disable=SC2016`; values passed with `awk -v name="$VAR"`; awk prints `PASS/FAIL ID msg` lines to `$TMP/*.out`; the shell loop echoes them and counts `FAIL*`. First-failure-only per check: `function fail(id,msg){ if (!(id in fmsg)) fmsg[id]=msg }`. Use for R1, R2, R5, R6.

**Scope check over all change sources** (lines 322-356, adapt for S1/S2): union of committed, unstaged, staged and untracked paths, then a `case` on each path.
```bash
{ git diff --name-only "$SCOPE_BASE...HEAD"; git diff --name-only
  git diff --name-only --cached; git ls-files --others --exclude-standard
} 2> /dev/null | sort -u > "$TMP/paths.txt"
```
Phase 2 `case`: allow only `docs/method/GG-SAD_normative_method_specification.md` and `.planning/*`; `src/*` fails S1.

**Pattern table via here-doc with `label|regex`** (lines 294-303, adapt for X1): `while IFS='|' read -r label re; do hit=$(grep -n -E -e "$re" "$REC" | head -n1) ...`. Hash-like token scan (lines 276-278) is reusable for the "hex of 7-40 chars containing a digit" rule; here the allowed set is empty.

**Footer** (lines 358-363): `RESULT: PASS` exit 0, else `RESULT: FAIL $FAILS` exit 1.

**Differences to plan for:** WARN lines (N1 lowercase modals, R7, R8, X1 "prototype") have no analog; print `WARN ID msg` without counting. A1 prints facts (blob, SHA-256 via `sha256sum`, line count, diffstat) and has no PASS/FAIL. C1 and R-checks that need the full text run only under `--final`.

---

### `02-NN-SUMMARY.md` (evidence note)

**Analog:** `.planning/phases/01-decision-record/01-01-SUMMARY.md`

**Front matter** (lines 1-31): YAML keys `phase, plan, subsystem, tags, status, requires, provides, affects, actuals {tokens, tasks, commits}, tech-stack {added, patterns}, key-files {created, modified}, key-decisions, patterns-established, requirements-completed, duration, completed`. Requirement ticks are left to the orchestrator at phase close, with a trailing comment: `requirements-completed: []  # SPEC-xx stays open: ...`.

**Body headings in order:** `# Phase N Plan NN: Title Summary`, one-sentence outcome, `## Accomplishments`, `## Task Commits` (numbered, `hash` subject, owner gate noted), `## Verification` (exact command lines and `RESULT` outcomes; negative runs that failed as intended; `git status --short` identical before and after script runs), `## Deviations from Plan` ("None - plan executed as written." or itemised), `## Known Stubs`, `## Unverified` (what only the Phase 4 reviewer or owner can judge), `## Self-Check: PASSED` (files and commit hashes exist on the branch).

**Constraint:** keep notes self-contained (memory: no links to transcripts or failed runs); name commands and results, not session artefacts.

---

### Owner-approval packet note for Phase 3 (evidence note)

**Analog:** `.planning/reviews/2026-10-24-decision-record-owner-confirmation.md`

**Layout:**
1. `# Owner confirmation: <subject>`
2. Field table `| Field | Value |` with rows: Reviewed file, Reviewed blob (git object id), Reviewed SHA-256, Check results (`RESULT: PASS` and the check ids), Owner reply (question text quoted, answer quoted, "requested no changes" statement), Confirmed on. Fill the first four from the A1 output (`git hash-object`, `sha256sum`).
3. One paragraph explaining why blob id and SHA-256 survive rebase and rebase-merge.
4. `## For the owner to look at`: "How to review" line with the file path and a `git diff origin/main...HEAD -- <file>` command.
5. Subsections per item needing owner attention: gaps ("rationale not recorded" analog: unresolved Drafting choices DC-nn), candidate material found elsewhere "not adopted", departures from earlier wording quoted in full as `>` blockquotes, then a bullet list of every decision restated for comparison (`- O-n: ...`; here the `full` realizations and DC items).
6. Closing line: `This note is evidence only. It does not change the reviewed file.`

**Shared with the sibling note** `.planning/reviews/2026-10-24-reviewer-rule-amendment.md`: same self-contained, plain-language, ~100-column wrap convention.

---

### `docs/method/GG-SAD_normative_method_specification.md` (modified)

Analogs are the spec's own sections, already mapped in 02-RESEARCH.md. Additions only:
- Commit-per-SPEC convention: subjects must name SPEC ids (checked by C1). Phase 1 used `docs(01-01): <what>`; use `docs(02-NN): SPEC-xx <what>`.
- Run the script before every spec commit (`bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh`); Phase 1 did this per task and recorded negative runs.
- Wrap and tone: 100 columns for planning notes; the spec's own line style governs inside the spec (E3 allows trailing whitespace only as exactly two spaces).

## Shared Patterns

### Read-only script discipline
**Source:** `01-check-decision-record.sh` lines 19-23, 83-84. **Apply to:** the check script. Temp dir with trap, no writes elsewhere, `set -u`, `LC_ALL=C`, exit 2 for usage and unreadable input.

### PASS/FAIL line format
**Source:** same, lines 119-120, 358-363. **Apply to:** all checks: `PASS ID message`, `FAIL ID message`, final `RESULT:` line.

### Verification evidence
**Source:** `01-01-SUMMARY.md` "Verification". **Apply to:** every SUMMARY: positive run, negative runs, unchanged `git status`.

## No Analog Found

| File | Role | Reason |
|---|---|---|
| WARN-level output and A1 fact printing in the script | utility | Phase 1 script has only PASS/FAIL; design the `WARN ID` line format as a compatible extension (not counted in `FAILS`) |
| C1 commit-subject coverage (`git log BASE..HEAD -- FILE`) | utility | Phase 1 had no per-commit rule; use `git log --format=%s` against the spec path |

## Metadata

**Analog search scope:** `.planning/phases/01-decision-record/`, `.planning/reviews/`
**Files scanned:** 6
**Pattern extraction date:** 2026-10-24
