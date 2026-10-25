---
phase: 04-independent-review
plan: 02
subsystem: independent-review-machinery
tags: [independent-review, check-script, report-parser, reference-resolution, findings-table, pilot-mode]
status: complete

requires: ["04-01"]
provides:
  - "Report check RP1 to RP9 (--report-file with --pass) that resolves every reference of a reviewer report against the pinned text or the base text"
  - "Mechanical findings table, quoted-report sections and counts (--print-findings-table, --print-sections, --print-counts)"
  - "Stage reported with the consent-trail check CT1, the Reports section check RPS and the table and count checks F1 and F2"
  - "Pilot mode of the report check (--pilot-dir with --pass RV-P) with the containment answers PC0 and PC1"
affects: [04-03 consent and runs, 04-04 owner dispositions]

actuals:
  tokens: 12500
  tasks: 4
  commits: 4

tech-stack:
  added: []
  patterns: ["one report_source function supplies every source of the report check (real or pilot)", "findings are derived and compared by the script, never typed", "one allow-list function for hash-like tokens with the input hashes and the input files as parameters"]

key-files:
  created:
    - .planning/phases/04-independent-review/04-02-SUMMARY.md
  modified:
    - .planning/phases/04-independent-review/04-check-independent-review.sh

key-decisions:
  - "A reviewer report is accepted only when it follows the brief's format exactly and every reference resolves in the pinned text or the base text; the findings table is derived from the quoted reports by the script and compared with the note (F1, F2), so the Requestor cannot add, drop, reorder or re-rate a finding."

requirements-completed: []  # REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close, not by this plan.

duration: "not measured; the plan was executed in one session"
---

# Phase 4 Plan 02: Report Parser and Stage Reported Summary

The check script now parses a reviewer report of the brief's format (RP1 to RP9), resolves every reference against the pinned text or the base text, derives the findings table and the counts mechanically from the quoted reports, checks the consent trail and the table in the new stage reported, and reads a pilot report against the synthetic inputs (PC0, PC1); every rule was shown to fail for the right reason on a seeded defect, and nothing was sent to Devin or any other service.

## Accomplishments

- Report check (`--report-file PATH --pass ID`): RP1 framing, RP2 label order (a label counts only at the start of a line; only REASONING, DISPOSITION REQUIRED, CHECKS PERFORMED and LIMITS may continue), RP3 identity naming Devin and the four input SHA-256 values or `not computed` (a warning), RP4 scope and coverage against the headings of the pass range (an omitted heading is a warning, more than half omitted a failure), RP5 finding count, ids from 001, severity words, one-line summaries and no vertical bar, RP6 reference resolution (file SPEC or BASE, a numbered heading or `header`, line range inside the file, a quote that is a substring of a line, a warning when the quote lies outside the stated lines), RP7 closing lines and a verdict that agrees with the severities, RP8 self-containment by the allow-list of 04-01, RP9 a warning `WARN RP9 <phrase> in LIMITS of <pass>` for a claim of truncation or incompleteness.
- One function, `report_source`, supplies the specification text, the base text, the four expected SHA-256 values, the line range of the pass and the allow-list corpus; the pilot mode switches all of them to the pilot directory, so no check reads a source by another route. The pass-table and heading extraction of V1 moved into shared helpers without a change of the stage brief output.
- Printers: `--print-findings-table` (the sentence `No findings were returned by any pass.` or the table with an empty Disposition cell), `--print-sections DIR` (the Reports section with the fixed introduction and each report quoted whole, then the Findings section), `--print-counts` (`total=N blocking=N major=N minor=N info=N` and one `blocking-id ID` line per BLOCKING finding).
- Stage reported: the brief-stage checks with the reported forms of T1, P0 and N1 (Claude-family model names refused), CT1 (the Run set value equals the id that `--print-run-set` prints for the note's Reviewer model; the Consent question contains that id and the model; the Consent answer is exactly `Consent`), RPS (the fixed introduction and six quoted blocks in pass order), RP1 to RP9 on each quoted report, F1 (the Findings section equals the derived table) and F2 (the blocking count and the fixed Requestor notes, with optional `- Check warning: ` lines).
- Pilot mode (`--pilot-dir DIR` with `--pass RV-P`): PC0 verifies the directory as a pilot inputs directory, RP1 to RP9 run on the pilot inputs, PC1 requires exactly one `CANARY READ: refused` and one `FILE CREATE: refused` in LIMITS and no `succeeded`, `not attempted` or `CANARY FIRST4: ` form.

## Task Commits

1. Task 1 (tracer): `518e4c5` docs(04-02): add the report check and reference resolution to the review check script (tracer)
2. Task 2: `f6558f0` docs(04-02): add the findings table, the section printers and the stage reported to the review check script
3. Task 3: `f677146` docs(04-02): add the pilot mode to the report check
4. Task 4: `bbae219` docs(04-02): fix the review check script after the seeded runs (one defect, see Deviations); this summary is committed as `docs(04-02): summary`.

## Verification

CHK is the check script, SPEC the specification, NOTE the review note. Fixtures were generated from the pinned text and the pilot inputs by a small program kept outside the repository, were written into a throwaway directory outside the repository, and were removed afterwards; none is a review result and none is named in a committed file.

- `bash -n CHK` and `shellcheck CHK` exit 0; CHK has no CR byte; `bash CHK --help` exits 0, prints no local absolute path and mentions `--pilot-dir` and `PC1`. `bash CHK --stage brief` exits 0 with 23 PASS lines and `RESULT: PASS`.
- `bash CHK --stage reported` on the real note exits 1 (five failing checks: P0, T1, N1, CT1, RPS, with F1 and F2 not evaluated) because no report exists yet; it is a check result, not a script error. `grep -c '^- Independent review: pending$' NOTE` prints 1.
- Exit 2 usage cases: `--report-file /nonexistent --pass RV-A`, `--pass RV-Q`, `--pass RV-P` without `--pilot-dir`, `--pass RV-A --pilot-dir DIR` and `--pass RV-B --pilot-dir DIR` each print a usage message and exit 2.
- Part 1, `bash CHK --report-file REPORT --pass ID`: a good report for each of RV-A, RV-B (two findings, one BLOCKING and one MINOR), RV-C, RV-D, RV-E and RV-X ends `RESULT: PASS`; so does the RV-B report with CR LF line endings and with a tab inside REASONING. Seeded failures, each exit 1 with the named id (further FAIL lines may follow from the same edit): RP1 END line removed, text before BEGIN, text after END, two BEGIN lines; RP2 REASONING label missing, REFERENCE before SEVERITY, SUMMARY before SEVERITY, a continuation line after SUMMARY, empty REASONING; RP3 IDENTITY without Devin, wrong INPUT hash, malformed INPUT value, INPUT line missing; RP4 COVERAGE omitting 44 of 54 headings, a COVERAGE that is not a number list, empty SCOPE; RP5 severity CRITICAL, FINDINGS 3 against two blocks, FINDINGS none with blocks, repeated finding id, id with another pass letter, vertical bar in a SUMMARY, a SUMMARY of 201 characters; RP6 section 99.9, a quote that is not in the text, lines beyond the end of the file, an inverted range, a malformed reference, file OTHER, a BASE section that BASE lacks; RP7 NO BLOCKING FINDINGS next to a BLOCKING block, BLOCKING FINDINGS PRESENT without one, empty LIMITS; RP8 a drive-letter path. Warning-only cases that still end `RESULT: PASS`: `not computed` for one input (WARN RP3), one omitted heading (WARN RP4), a number that is no heading (WARN RP4), a quote present in the text but outside the stated lines (WARN RP6); `quote none` also passes.
- Part 2, hash-like tokens (RP8): a report whose REASONING quotes the first 64-digit example hash of SPEC unedited ends `RESULT: PASS` and prints `PASS RP8`; the same token with the last digit changed prints `FAIL RP8`; a 12-digit prefix of that hash, a 12-digit prefix of the Result blob and a 7-digit prefix of the SHA-256 of DECISIONS.md pass; a foreign 12-digit hexadecimal token with a digit, a foreign 40-digit token (the repeated digits 0123456789abcdef), a web address, a markdown link and a local-data reference word each print `FAIL RP8`. A note copy under stage reported whose Requestor notes carry a `- Check warning: ` line with a quoted example hash of the pinned text ends `RESULT: PASS`; the same line with a foreign 40-digit token prints `FAIL X1`.
- Part 3, RP9: LIMITS saying the output was truncated, `could not complete`, `incomplete` and `context limit` each print `WARN RP9 <phrase> in LIMITS of RV-B` and end `RESULT: PASS`; LIMITS saying only that the code was not executed prints `PASS RP9`.
- Part 4, printers and stage reported on a copy of NOTE assembled with `--print-sections` (six good reports, one with a BLOCKING and a MINOR finding, five with `FINDINGS: none`; status lines, version, model and the three consent rows set): `bash CHK --stage reported --note COPY` ends `RESULT: PASS`; `--print-counts` prints `total=2 blocking=1 major=0 minor=1 info=0` and one line `blocking-id RV-B-001`; `--print-findings-table` begins `| Finding | Severity |`. Seeded failures, each exit 1 with the named id: F1 one severity cell changed, one row dropped, one extra row, two rows swapped, a reference cell changed, one summary word changed in a quoted report; F2 the blocking count changed, a Requestor note changed; RP5 a severity word changed in a quoted report; RP7 a verdict changed; RPS a sixth block removed, a block duplicated, a line that is not a quoted line, the fixed introduction changed; N1 a model name containing `claude`, the Reviewer version left `pending`; T1 the first status line left `pending`; CT1 the Run set value with one digit changed (X1 also fails), the Consent question without the model name, the Consent answer set to another word; P0 one consent row left `pending`. Zero findings: six reports of `FINDINGS: none`, the one-sentence Findings section and a count of 0 end `RESULT: PASS`; `--print-counts` prints `total=0 blocking=0 major=0 minor=0 info=0` and no `blocking-id` line; the same note with a table header and separator added prints `FAIL F1`. A note whose RV-C report carries a truncation claim ends `RESULT: PASS` with `WARN RP9 truncat in LIMITS of RV-C`. `--print-sections` with one report file missing exits 2.
- Part 5, pilot mode (`--report-file REPORT --pass RV-P --pilot-dir DIR`, DIR built with `--print-pilot-file` for the five names): the good pilot report (INPUT lines with the four pilot SHA-256 values, COVERAGE `1, 2, 3`, one quote that is the example-hash line of the pilot text) ends `RESULT: PASS` and prints `PASS PC0`, `PASS RP8` and `PASS PC1`; the same report with one pilot SHA-256 value quoted in REASONING also prints `PASS RP8`. Seeded failures, each exit 1: `CANARY READ: succeeded`, `FILE CREATE: succeeded` and a `CANARY FIRST4: ` fragment print `FAIL PC1` (containment breach reported by the reviewer); `CANARY READ: not attempted`, no answer and a repeated answer print `FAIL PC1` (containment test not performed); a pilot directory with an extra file and one with a changed byte print `FAIL PC0` naming SN1 and SN2; a wrong INPUT hash prints `FAIL RP3`; a quote that is not in the pilot text prints `FAIL RP6`; a foreign 40-digit token prints `FAIL RP8`. A good report for a normal pass (`--pass RV-B`) whose REASONING quotes one of the four pilot SHA-256 values prints `FAIL RP8` and exits 1, because the real-mode call passes the real input hashes and the real snapshot inputs. The pilot report checked as `--pass RV-B` without `--pilot-dir` prints `FAIL RP1` and `FAIL RP3` (exit 1).
- With the script as committed after the fix, all 27 stage reported cases of part 4 give the results above and `bash CHK --stage brief` ends `RESULT: PASS`.
- The specification blob is unchanged (`git hash-object SPEC` prints `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`); `git diff --name-only origin/main...HEAD` lists only the specification and paths under `.planning/`; `grep -c '^- \[x\] \*\*REVIEW-0' .planning/REQUIREMENTS.md` prints 0; `git status --short` and `git ls-files --others --exclude-standard` print nothing before this summary.

## Deviations from Plan

**1. [Rule 1 - Interpretation] Where the "holds text" rule sits.** The plan lists the text requirement for REASONING, DISPOSITION REQUIRED, CHECKS PERFORMED and LIMITS under RP2 and repeats CHECKS PERFORMED and LIMITS under RP7. To avoid one defect failing two ids, RP2 checks REASONING and DISPOSITION REQUIRED and RP7 checks CHECKS PERFORMED and LIMITS; all four are checked.

**2. [Rule 1 - Interpretation] Continuation lines.** The plan says every other labelled field keeps its value on its label line. The script fails RP2 when a field other than the four may-continue fields has a continuation line (including text after REPORT END), so that stray text cannot be ignored silently. Blank lines are skipped everywhere.

**3. [Rule 1 - Interpretation] Message forms.** Every report-check message names the pass; the warning line form is `WARN RP9 <phrase> in LIMITS of <pass>`, so the plan-03 stop and the `- Check warning: ` line can carry the exact WARN line. A SUMMARY length is counted in bytes (the script runs in the C locale), which is stricter than characters for non-ASCII text.

**4. [Rule 1 - Interpretation] "Checked as a normal pass".** The plan says the pilot report checked as a normal pass and a real report checked with `--pilot-dir` must exit 2. The script exits 2 for `--pass RV-P` without `--pilot-dir`, for any other pass id with `--pilot-dir` and for `--pass RV-Q`; the pilot report checked as `--pass RV-B` without `--pilot-dir` is a legal call and fails RP1 and RP3 (exit 1).

**5. [Rule 1 - Bug] F2 passed on a count it had not evaluated.** On the real note (where RPS fails) `--stage reported` printed `PASS F2 ... [pending], equal to the count of BLOCKING findings`. F2 now prints a warning that the count is not evaluated when the Reports section could not be read. Fix commit `bbae219`.

**6. [Process] Tracer feedback gate.** The project setting `workflow.human_verify_mode` is `end-of-phase` and auto mode is off, so the tracer's human-verify step is deferred to the end-of-phase flow; the tracer's own `<verify>` (syntax, shellcheck, stage brief) and its seeded proof were re-run before the expansion tasks and passed.

**7. [Refactor] Shared helpers.** V1's heading extraction and pass-table parsing moved into `build_heads`, `build_passes`, `prep_ranges` and `pass_line` so that the report check uses the same mapping; the stage brief output is unchanged.

## Flagged assumptions

Carried verbatim from 04-01-SUMMARY.md; none is resolved by this plan.

- A-1 (REVIEW-01, probe category 'unclassified', status 'unresolved'): what the reviewer is given and must produce so that its judgment is independent. Decided here: five neutral files, a charter, a severity scale and an output format; separate sessions; a read-only minimal configuration; the reviewer's own statement of identity; a listing of what the installation loads in the inputs directory under the run's own configuration (W4). Unresolved residue: the repository cannot show everything else the reviewer's installation loads or that the reviewer opened nothing outside its directory; both rest on instruction, on that listing and on the reviewer's self-report.
- A-2 (REVIEW-01): whether a headless run, or six, reviews this text thoroughly cannot be shown. The coverage lines and the limits lines are the reviewer's claims. A result with no findings is recorded as such and is not evidence that no defect exists.
- A-3 (REVIEW-02, probe category 'unclassified', status 'unresolved'): what counts as blocking. The brief defines BLOCKING in one line and the reviewer applies it; the owner may disposition any finding, including by rejecting a BLOCKING one with a reason.
- A-4 (REVIEW-02): who classifies. The reviewer assigns severity; the Requestor never re-rates, merges or filters; only the owner dispositions.
- A-5 (REVIEW-02): resolving a finding by editing the specification voids the Phase 3 approval (text, blob and SHA-256 change). This phase does not edit the specification; plan 04 describes the path (a gap-closure plan edits the text, the diff identity is re-recorded, the owner approves the new exact text, and the changed parts are re-reviewed by Devin) and does not pre-write it.
- A-6: the owner's global Devin configuration auto-allows many commands (including git commit, python and bash -c) even in permission mode `auto`, so `auto` alone is not read-only. The runs therefore use a minimal configuration given with `--config` (a read-only allow list and explicit deny rules for every write and fetch pattern and for the repository path, the latter computed at run time and written only into the throwaway file), a working directory that is a throwaway copy outside the repository, and `--respect-workspace-trust false` (print mode refuses an untrusted directory otherwise). That the option is honoured cannot be proven by the repository. A pilot in plan 03 looks for a read of a decoy file in a second throwaway directory and for a file-creation attempt: it detects a read that the reviewer reports or that leaks into the output (the full decoy token in the output, a file created, a changed repository or snapshot) and it does not prove the configuration is honoured. The repository and the snapshot are verified after every run. If the tool ignored the configuration, the repository could not prevent the reviewer from reading outside its working directory; it could only detect writes and rely on the reviewer's self-report of what it opened. This residue (with A-1) is recorded as Unverified in the summaries.
- A-7: that the standard output of `devin -p` is exactly the reviewer's final message is assumed from the tool's documentation and is first confirmed by the pilot of plan 03 (the captured output must hold the report and nothing else).
- A-8: Devin offers models from several vendors, some from the Requestor's own vendor. The model is fixed to `swe-2-medium` (Cognition's own model family, the owner's current default and the model of the earlier review); a Claude-family model is refused, so that the model, not only the product, differs from the Requestor.
- A-9: the exact form of the headless call is verified here only syntactically (a help call that parses the flags); its behaviour is first seen in the pilot of plan 03.

## Known Stubs

None. The real note still carries its intentional `pending` values; plans 03 and 04 fill them.

## Unverified

- The script proves the format of a report, that its references resolve in the pinned text, the fidelity of the quoted reports and of the derived table, and the consent trail; it does not prove that a finding is right or that the reviewer is independent. The reviewer's identity is its own statement in each report.
- The report format and the parser are the Requestor's design and are exercised here only on fixtures written from the pinned text; they are first exercised on a real report in the pilot and the passes of plan 03, where A-7 and A-9 are first tested and A-6 is first observed.
- The pilot detects a read that the reviewer reports or that leaks into the output; it does not prove the configuration is honoured, so A-6 stays Unverified. PC1 takes the reviewer's answers as its own statement and the script looks neither for the decoy content nor at the filesystem.
- The truncation phrases of RP9 are a fixed list; a reviewer's claim in other words is not detected.
- A changed word in a REASONING or DISPOSITION REQUIRED text of a quoted report is not detected by any check (only the fields that enter the table and the format are compared).
- Nothing has been sent to Devin or any other service; the real note is untouched and still in pending form.

## Self-Check: PASSED

- Files exist: the check script and this summary under `.planning/phases/04-independent-review/`.
- Commits `518e4c5`, `f6558f0`, `f677146` and `bbae219` exist on gsd/v1.1-executable-core.
- `bash CHK --stage brief` ends with `RESULT: PASS`; `shellcheck CHK` exits 0; the specification blob is unchanged; `git status --short` was empty before this summary was written.
