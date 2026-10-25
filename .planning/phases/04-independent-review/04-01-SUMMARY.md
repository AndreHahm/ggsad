---
phase: 04-independent-review
plan: 01
subsystem: independent-review-machinery
tags: [independent-review, check-script, review-brief, pilot-inputs, run-set]
status: complete

requires: ["03-03"]
provides:
  - "Read-only check script with stages pins and brief, the hash-token allow-list, snapshot verification, pilot inputs and the run-set id"
  - "Neutral review brief with the pass partition, charter C1 to C8, severity scale and output format"
  - "Review note skeleton with pins, three pending consent rows, status lines and independence facts"
affects: [04-02 report parser, 04-03 consent and runs, 04-04 owner dispositions]

actuals:
  tokens: 15400
  tasks: 4
  commits: 3

tech-stack:
  added: []
  patterns: ["checks built from git objects, never from the working tree", "one allow-list function for hash-like tokens, with the input hashes and the input files as parameters"]

key-files:
  created:
    - .planning/phases/04-independent-review/04-check-independent-review.sh
    - .planning/phases/04-independent-review/04-REVIEW-BRIEF.md
    - .planning/reviews/2026-10-25-normative-spec-independent-review.md
  modified: []

key-decisions:
  - "The owner decided to proceed with the residue left by the reviewer installation (two enabled MCP servers imported from another tool's configuration, three user skills) after four other servers were disabled for the review."

requirements-completed: []  # REVIEW-01 and REVIEW-02 are ticked by the orchestrator at phase close, not by this plan.

duration: "not measured; the plan spanned several orchestrated sessions including an owner checkpoint"
completed: 2026-10-25
---

# Phase 4 Plan 01: Review Machinery Summary

One read-only check script (stages pins and brief), a neutral review brief whose pass table is proven to partition the 4649-line specification, a review note skeleton tied to the owner approval record, synthetic pilot inputs and a run-set id were built and committed; nothing was sent to Devin or any other service.

## Accomplishments

- Check script: the pins in the note are checked against the owner approval record, the Phase 3 recorded check, and the live specification (working file, index and HEAD, SHA-256, line count); scope, status, encoding, structure and self-containment are enforced. Helpers `snapshot_input`, `hash_token_allowed` and `x1_scan` are defined once for every later stage and plan.
- Brief: five neutral inputs, a charter of eight items, a severity scale, six passes (five section passes plus one cross-cutting pass), a fixed report format and rules; checked for anchoring words (B2), the project rule (B3), expected hashes (B4), size and encoding (B5), structure (B6) and self-containment (B7).
- Snapshot of inputs: printable from git objects, verifiable by SHA-256 (SN1, SN2), with the requirement texts stripped of completion marks.
- Pilot inputs: invented text only, printed by the script, checked to carry no repository content (PL1) and to reuse the severity scale, output format and rules of the brief byte for byte (PL2); a decoy-read and file-creation test with fixed answer words.
- Run set: `--print-run-set MODEL` covers the four input hashes, the brief, the pilot, the pilot inputs, the six passes, the model and the mode; its 12-digit id changes when any of them changes.

## Task Commits

1. Task 1 (tracer): `9f011f3` docs(04-01): add the independent review check script core and note skeleton (tracer)
2. Task 2: `63f8400` docs(04-01): add the review brief, the brief stage and the snapshot check
3. Task 3: `5d55920` docs(04-01): add the pilot inputs and the run set to the review check script
4. Task 4: seeded fixtures and dry run found no defect, so there is no fix commit; this summary is committed as `docs(04-01): summary`.

## Verification

- `bash CHK --stage brief` (CHK is the check script): all 23 checks print PASS (E1, E2, P0, A3, A2, Z1, R1, H1, S1, T1, H2, N1, X1, V1, B2, B3, B4, B5, B6, B7, N2, PL1, PL2) and the last line is `RESULT: PASS`. The pass ranges printed by V1 are RV-A lines 1-1073, RV-B 1074-2247, RV-C 2248-2949, RV-D 2950-3772, RV-E 3773-4649, RV-X 1-4649.
- `shellcheck` on the script: exit 0.
- The specification blob is unchanged (`ed758c46d5ac901359ab2c0df8e437ef89fed0f1`); `git diff --name-only origin/main...HEAD` lists only the specification and paths under `.planning/`; no `REVIEW-0` requirement is ticked.
- Seeded runs, on copies of the files held outside the repository and removed afterwards. Each command form was run and each exited 1 with the named id (a run may print further FAIL lines that follow from the same edit):
  - Tracer checks: `--spec COPY` with one byte appended prints FAIL Z1, R1, H1; `--note COPY` with the first status line set to `reported` prints FAIL T1; with the Line count changed prints FAIL A2 and H1; `--approval-record COPY` with the outcome line `changes requested` prints FAIL A3 (and A2, Z1); `--note COPY` with a drive-letter path appended prints FAIL X1; with a foreign 40-digit hexadecimal token appended prints FAIL X1; with the Reports and Findings placeholders swapped prints FAIL T1; without the Consent answer row prints FAIL P0.
  - Brief stage, `--brief COPY`: RV-C Up to set to 25 prints FAIL V1; RV-B Up to set to 22 (a gap) prints FAIL V1; a sentence naming the register of drafting choices prints FAIL B2 (and PL2, because that section is reused by the pilot); one changed digit in an expected hash prints FAIL B4 (and B7); the project rule altered prints FAIL B3; padded beyond 16384 bytes prints FAIL B5 (and B6); the label `VERDICT:` removed prints FAIL B6 (and PL2); a foreign 40-digit token appended prints FAIL B7 (and B6). `--stage brief --note COPY` with one severity definition changed prints FAIL N2.
  - Snapshot: `--verify-snapshot DIR` with an extra file prints FAIL SN1; with one byte changed in BASE.md prints FAIL SN2; with a completion mark kept in REQUIREMENTS.md prints FAIL SN2; a directory built with `--print-snapshot-file` for the five names prints PASS SN1 and SN2.
  - Pilot and run set: a directory built with `--print-pilot-file` passes `--verify-snapshot DIR --pilot`; with one added file it prints FAIL SN1; a script copy whose pilot SPEC.md carries a 98-character line cut from the real specification prints FAIL PL1; a brief copy with one word changed in the Output format section prints FAIL PL2; a script copy whose pilot SPEC.md differs by one character prints a different `Run set:` line from the original, and the original prints the same line on a repeat run.
  - Hash-token allow-list (`--note COPY`, X1): an unedited example hash of the pinned text appended prints PASS X1; the same token with its last digit changed prints FAIL X1; a 12-digit prefix of the Result blob prints PASS X1; a 12-digit prefix of the SHA-256 of DECISIONS.md prints PASS X1; a 6-digit prefix of the Result blob prints PASS X1; a foreign 12-digit token prints FAIL X1; a drive-letter path prints FAIL X1; a pilot input hash in a real-mode scan prints FAIL X1.
- Dry run (local commands only; `devin -p` was not run and no repository text was sent):
  - `devin --version` printed version 3000.4.25.
  - `--verify-snapshot` passed on an inputs directory built with `--print-snapshot-file`, and on a pilot directory built with `--print-pilot-file` under `--pilot`.
  - A minimal read-only configuration (model swe-2-medium, an allow list of read tools and read-only commands, deny rules for every write and fetch pattern and for the repository by directory name) was built for the dry run; `devin --config ... auth status` printed `Logged in`, and the help call after the run's flags (`--permission-mode auto --model swe-2-medium --respect-workspace-trust false --help`) exited 0.
  - Listings of what the installation loads, read again immediately before this summary from a neutral directory under that minimal configuration: MCP servers: six are configured; four are disabled (GitKraken, the Notion server, codacy, the second Linear server) and two are enabled (pycharm, mcp-linear). Skills: three user skills are listed (my-skill, yes-flag-test-skill, declarative-repo-setup). Rules: one always-on rule (global_rules), which is empty. Plugins: none installed. The listings are the same with and without the minimal configuration.

## Deviations from Plan

**1. [Rule 3 - Blocking, syntax not determinable] Deny syntax for the repository path.** The plan asks for deny rules for the absolute repository path in the syntax the owner's configuration uses, taking it from the tool's help if not evident. The syntax for an absolute path could not be determined, while the owner's configuration already uses glob patterns. The repository deny rules for Read, Grep and Glob therefore use the glob form the owner's configuration already uses, computed at run time from the repository directory name and written only into the throwaway configuration. Whether that form denies reads of the absolute repository path is unproven. This adds to the A-1 and A-6 residue.

**2. [Plan checkpoint, W4 stop condition reached] Servers and skills loaded for the reviewer.** The listing showed six MCP servers and three user skills that would be loaded, which the plan treats as a stop condition for the owner. The owner decided to disable the MCP servers for the review. Four were disabled through the Devin command line (GitKraken, the Notion server, codacy, the second Linear server); the command line refused to disable the other two (pycharm and mcp-linear) because they are imported from another tool's configuration. The three skills cannot be disabled by the command line. The owner decided to proceed with the residue. The orchestrating session re-enables the four servers after the review; no executor edited a Devin configuration.

**3. [Observation] Listing context.** The final re-read of the listings was made from a neutral directory under the minimal configuration, not the inputs directory; no project-level rules, skills or servers exist in a directory of copies, so the listing is the user-level one.

No defect was found in the script, the brief or the note by the seeded runs, so no fix commit was made.

## Flagged assumptions

Carried verbatim from the plan; none is resolved by this plan.

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

None. The note carries intentional `pending` values (reviewer version and model, the consent rows, the three status lines, the Reports and Findings placeholders); plans 03 and 04 fill them.

## Unverified

- The script proves the pins, the neutrality of the brief and of the pilot inputs, and the integrity of the inputs; it does not prove that the reviewer is independent. Nothing has been sent to any service.
- Whether `--config` is honoured, including the deny rules for the repository path, is not proven by anything in this plan. The repository deny rules use a glob computed from the directory name (Deviation 1); whether that denies the absolute repository path is unproven.
- The pilot of plan 03 detects only a read that the reviewer reports or that leaks into the output; it does not prove the configuration is honoured.
- Whether standard output is the final message is first observed in the pilot of plan 03.
- Independence residue of A-1 and A-6: the repository cannot prevent the reviewer from reading outside its working directory if the tool ignores the configuration; it can only detect writes and rely on the reviewer's self-report of what it opened.
- Installation residue the owner decided to proceed with: two MCP servers (pycharm and mcp-linear), imported from another tool's configuration and enabled, and three user skills (my-skill, yes-flag-test-skill, declarative-repo-setup) would still be loaded by the reviewer; their effect on a review is not verified. The four other servers were disabled for the run and are to be re-enabled afterwards; the repository cannot show that they stay disabled during the runs.

## Self-Check: PASSED

- Files exist: the check script, the brief and the review note under `.planning/`.
- Commits `9f011f3`, `63f8400` and `5d55920` exist on gsd/v1.1-executable-core.
- `bash CHK --stage brief` ends with `RESULT: PASS`; `git status --short` was empty before this summary was written.
