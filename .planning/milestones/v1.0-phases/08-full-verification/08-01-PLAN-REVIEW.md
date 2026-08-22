# Plan Conformance Review — 08-01-PLAN.md

## Review record

- Reviewer: Claude Code
- Reviewer role: Independent reviewer
- Requestor: Codex
- Reviewed artifact: `.planning/phases/08-full-verification/08-01-PLAN.md`
- Reviewed against: `.planning/phases/08-full-verification/08-CONTEXT.md`,
  `.planning/phases/08-full-verification/08-CONTEXT-REVIEW.md` (findings PCR-01, PCR-02), and actual
  repository state
- Worktree: `C:\Dev\Repos\ggsad-worktrees\phase-8-full-verification`, branch
  `gsd/phase-8-full-verification`, HEAD `0824da144a8366a758f05d016f03c98c43d46ed3`
- Review date: 2026-08-21
- Action: Plan-conformance check before Phase 8 execution
- Result: Conforms; resolves both prior findings correctly (one more thoroughly than requested); one
  moderate, empirically-grounded finding about the verify mechanism for a legitimate failure path
- Scope: Plan-document review, cross-checked against actual repository state and verified by
  re-running the exact command the plan's Task 2 depends on. No repository files were modified as
  part of this review; execution had not started (no `08-VERIFICATION.md` or other Task 1–4 output
  existed at review time).

## Method

Read `08-01-PLAN.md` in full and cross-checked each task against PCR-01 and PCR-02's exact text.
Independently verified the underlying facts rather than trusting the plan's restated claims: checked
`REQUIREMENTS.md`'s actual NORM-01–08 checkbox-vs-traceability-table state (not just AUDIT/GAP, which
is all PCR-01 explicitly named), confirmed no pre-existing `.planning/phases/07-gap-remediation/`
directory conflicts with Task 1, confirmed the Task 3 revision anchor matches `HEAD` exactly, and
re-ran `uv sync --locked` in this worktree to check whether the condition PCR-02 described is still
live for Task 2's fail-fast logic to actually encounter.

## What checked out

- **PCR-01 (Phase 6/7 metadata contradiction) — resolved, and extended beyond what was asked.**
  Task 1 creates `07-gap-remediation/07-RETROACTIVE-CLOSURE.md` honestly stating Phase 7 had zero
  formal plans (no pre-existing directory conflict, confirmed). It changes ROADMAP.md's Phase 6/7
  plan markers to "0 formal plans" and the Progress table from `1/1` to `0/0` — resolving both the
  internal TBD-vs-Complete contradiction and the plan-count mismatch against `STATE.md`'s
  `total_plans: 7` in one move (0+0 additional plans correctly reconciles with 7 = Phases 1–5 only).
  For `REQUIREMENTS.md`, the plan fixes traceability status for **NORM, AUDIT, and GAP** — broader
  than PCR-01's literal scope (AUDIT/GAP only). Independently verified NORM-01–08 has the identical
  checkbox-`[x]`-vs-traceability-table-"Pending" mismatch PCR-01 only checked for AUDIT/GAP. This is
  a legitimate, accurate extension, not fabricated scope.
- **PCR-02 (foreseeable VERIFY-01 blocker) — resolved via an explicit policy decision.** Task 2
  records the known pre-existing TLS diagnostic separately from the authoritative run, matching
  PCR-02's recommendation exactly. It makes an explicit, strict choice on the ambiguity PCR-02
  raised: on `uv sync --locked` `UnknownIssuer`, stop immediately, do not retry with `--native-tls`,
  return control to the owner. This is a legitimate, defensible disposition, consistent with
  `08-CONTEXT.md`'s own "plain commands are authoritative" policy.
- Task 3's revision anchor (`0824da144a8366a758f05d016f03c98c43d46ed3`) matches `HEAD` exactly.
- Task 4's owner-authorization checkpoint correctly separates plan approval from milestone-closure
  approval, doesn't infer approval from silence, and shows the exact proposed tag before creating it.

## Finding

### PLR8-01 — Task 2's automated verify has no branch for its own documented failure path (moderate, empirically live)

Re-ran `uv sync --locked` in this worktree: it still fails with the same `UnknownIssuer` condition
PCR-02 documented. Given Task 2's fail-fast design, this plan will very likely stop at its first
command when executed here — not a hypothetical edge case.

Task 2's `<done>` tag explicitly allows for this outcome: "The exact VERIFY-01 baseline passes with
complete, honest evidence, **or Phase 8 stops with a precise blocker record**." But its automated
`<verify>` PowerShell script only checks that all six commands have a `PASS` row in the evidence
table — it has no branch that validates the alternative, equally-legitimate outcome (a
correctly-recorded blocker with the failure captured verbatim and no later commands attempted). If
Task 2 behaves exactly as designed and stops early, the automated verify will fail with no way to
distinguish "the task did the right thing and hit a real environmental blocker" from "the task
executed incorrectly."

**Recommendation:** add a second branch to Task 2's verify (or a short explicit note in the task)
that checks for a well-formed blocker record — the failing command's exact output, a `VERIFY-01
blocked` marker, and confirmation no later required command ran — when fewer than six `PASS` rows are
present, so the legitimate stop-early path has its own positive confirmation rather than only the
absence of a false one.

## Follow-up verification (2026-08-22)

`08-01-PLAN.md` was updated after this review to apply the approved TLS policy change. Re-read Task
2 in full and tested its updated automated verify script directly — not just read it — against
synthetic evidence files representing both the full-pass and blocked-at-first-command outcomes.

- **PLR8-01: Attempted, but the fix introduces a new blocking defect — see PLR8-02.** Task 2's
  action now specifies an exact, positively-checkable blocker-record structure (`VERIFY-01 status:
  BLOCKED`, `Failed command:`, `Failure classification:`, `Later required commands run: No`, a
  `BLOCKED`-result table row, and a `### Failure output:` section), and the verify script was
  extended with logic to validate it — precisely the shape PLR8-01 asked for. The *logic*, traced by
  hand, is correct: it accepts a full six-`PASS` evidence file, accepts a well-formed blocker record
  at any of the six command positions (verified the specific case most likely to occur here — a
  block at command index 0 — makes `passCount -eq $failedIndex` true as required), and correctly
  rejects a record with rows present for commands after the failure. But the script as written
  cannot run at all — see PLR8-02.

### PLR8-02 — Task 2's automated verify script has a PowerShell string-termination bug and cannot execute (blocking)

**File:** `.planning/phases/08-full-verification/08-01-PLAN.md`, Task 2's `<automated>` verify
element.

The script's blocker-record check includes:

```text
-and $evidence -match "(?s)### Failure output:\s*`?$escapedFailed`?.*?```text\s+\S.*?```"
```

This is inside a double-quoted PowerShell string. Backtick is PowerShell's escape character in
double-quoted strings, so a literal backtick must be doubled (`` `` ``) to appear once in the
output. The embedded markdown fence markers (`` ```text `` and the closing `` ``` ``) are each three
raw backticks, not doubled — the trailing triple-backtick immediately before the closing `"` escapes
that quote instead of terminating the string, leaving the string literal unterminated for the parser.

Verified this exactly, not just diagnosed it: extracted the literal, unmodified verify script from
the plan file (only the hardcoded evidence-file path was substituted, to point at synthetic test
files) and ran it as `.ps1` files. **Both the full-pass evidence case and the well-formed
blocked-at-`uv sync --locked` evidence case fail identically** with a PowerShell `ParserError` —
"The string has no terminating character" — before any of the script's conditional logic executes.
Isolated the defect to confirm it's exactly this one fragment: the single-backtick patterns used
elsewhere in the same script (e.g. `` `?$escaped`? ``, used three times for the PASS-row and
later-rows checks) parse and match correctly on their own; only the triple-backtick fence line is
broken.

**Impact:** as written, Task 2's automated verify fails unconditionally, for every possible outcome
of the six commands — including the simple "all six passed cleanly" case that worked correctly in
the pre-TLS-policy revision of this plan. This is a regression, not merely an unfulfilled addition:
the previous revision's verify script (checked in the prior review) had no blocker-path branch but
did correctly validate the full-pass case; this revision attempts to add the blocker-path branch and
in doing so breaks both paths.

**Recommendation:** double every literal backtick intended to appear in the matched text (six
backticks per three-backtick fence marker) so the string terminates correctly, or restructure the
check to avoid embedding literal backticks inside a double-quoted string entirely — for example by
building the pattern from concatenated single-quoted literal segments joined with `+` around the
interpolated `$escapedFailed` variable, or by using a single-quoted string with `-f` formatting
instead of direct interpolation. Whichever approach is chosen, re-run the corrected script against
both a full-pass and a blocked-at-each-of-the-six-positions synthetic evidence file before relying on
it, the same way this verification did.

**Final verdict: Findings**

**Disposition: Open — blocking.** PLR8-02 must be fixed before Task 2 executes. As written, Task 2
cannot produce a passing verify result under any circumstance, including the legitimate full-pass
outcome, which defeats the task's own purpose regardless of what the six commands actually do.

## Follow-up verification (2026-08-22, second pass)

Independently re-reviewed PLR8-02 against the current `08-01-PLAN.md`, without editing the reviewed
artifact. Task 2's `<automated>` verify element (line 195) no longer contains any literal backtick
characters: the blocker-record checks now use `.NET` regex hex escapes (`\x60` for a single backtick,
`\x60{3}` for a triple-backtick fence) inside the double-quoted PowerShell strings, instead of raw
backticks. Confirmed this with a direct search of the exact verify line for backtick characters
(count: 0).

Extracted the exact, unmodified verify script text from `08-01-PLAN.md` Task 2 (only the hardcoded
evidence-file path was left untouched — no substitution was needed, since the test evidence files
were placed at that same relative path under separate temporary working roots) and ran it as `.ps1`
files under both Windows PowerShell 5.1 (`powershell.exe`) and PowerShell 7 (`pwsh`) against nine
synthetic evidence files:

- All six commands `PASS`: exit `0` under both shells, no errors — the previously-broken full-pass
  path now parses and passes correctly.
- A well-formed `BLOCKED` record at each of the six command positions (index 0 through index 5,
  including the boundary case of the record's own final required command, index 5, which exercises
  the `$required[($failedIndex + 1)..($required.Count - 1)]` later-rows range at its edge): exit `0`
  at every position under both shells, no errors.
- A malformed `BLOCKED` record that otherwise conforms to the required structure but also contains a
  command-results row for a command after the failed one (index 2, following a block at index 1):
  exit `1` under both shells, with the script's own `Write-Error 'Evidence is neither six clean PASS
  rows nor a complete fail-fast blocker record'` — a clean application-level rejection, not a parser
  failure.

No `ParserError` occurred in any of the eighteen runs (nine evidence cases × two shells). No other
defect was found in the script's logic during this pass.

**PLR8-02: Resolved.** The PowerShell string-termination bug is fixed; the verify script parses and
executes correctly for the full-pass outcome, the blocked outcome at every command position, and
correctly rejects a blocker record contaminated with a later-command row.

**PLR8-01: Confirmed still resolved.** The blocked-path branch this finding originally asked for is
present, well-formed, and empirically validated at all six possible failure positions, not just the
single position traced by hand in the prior review pass.

No new defects found.

**Final verdict: Verified.**

**Disposition: Closed.**
