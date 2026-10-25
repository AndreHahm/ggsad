---
phase: 03-owner-approval
plan: 01
subsystem: governance-gate
tags: [owner-approval, check-script, evidence-packet, pinned-text, normative-specification]
status: complete

requires: ["02-08"]
provides:
  - "Read-only check script .planning/phases/03-owner-approval/03-check-owner-approval.sh with stages pending and recorded and a record skeleton printer"
  - "Pending owner approval packet .planning/reviews/2026-10-25-normative-spec-owner-approval-packet.md: pin table, twelve section headings, fifteen owner questions"
affects: [03-02 packet content, 03-03 owner checkpoint and record, milestone v1.1 Phase 4]

actuals:
  tokens: 11000
  tasks: 3
  commits: 3

tech-stack:
  added: []
  patterns:
    - "Approval pinned to the text by base blob, result blob, SHA-256, line count, diffstat and commit count; the checker compares the pins with the working file, the index and HEAD"
    - "Packet and record as two files tied by the packet blob and SHA-256; the packet may differ from the pinned form in its one status line only"
    - "Outcome rule is mechanical: approved needs every accepting answer and Q13 Approve exact text; anything else is a requested change"

key-files:
  created:
    - .planning/phases/03-owner-approval/03-check-owner-approval.sh
    - .planning/reviews/2026-10-25-normative-spec-owner-approval-packet.md
  modified: []

key-decisions:
  - "A-1 (flagged assumption for APPR-01, still unresolved until the owner answers): the diff the owner approves is the whole of the specification as identified by content (base blob to result blob), not a commit range; a changed answer or an overruled drafting choice is a requested change and yields the outcome changes requested. The checks enforce it; plan 02 states it to the owner."

patterns-established:
  - "The record is created only by --print-record-skeleton; every owner field holds the fill marker, which A1 and X1 reject, so an unfilled or hand-built record cannot pass."

requirements-completed: []  # APPR-01 stays open: it is satisfied only by a recorded owner approval (plan 03).

duration: "about 30 minutes"
completed: 2026-10-25
---

# Phase 3 Plan 01: Approval Gate Machinery Summary

A single read-only bash script now enforces the owner approval of the proposed normative specification (pins, scope, pending status, the fifteen-question contract, and in stage recorded the verbatim questions, answers and the two-outcome rule), and the packet exists as a pending skeleton pinned to the exact text; no owner field has been filled.

## Accomplishments

- Tracer (task 1): the pin table of the packet (base blob `da29d6f3bdef2e88fdd85a762939017d7d7034fa`, result blob `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`, SHA-256, 4649 lines, diffstat, 36 commits, register blob) is compared live with the specification file, the index entry, HEAD, the base ref, the register and the diff identity note; the status line must read `Owner approval: pending`. Checks E1, E2, P0, B1, R1, H1, C1, K1, I1, S1, T1.
- Packet structure (task 2): the twelve H2 headings in fixed order and the fifteen question blocks Q01 to Q15, built from the register (Question and Reading cells of OQ-8 to OQ-15, the 141 DC rows), the specification (Version 1.4, Revision date 2026-10-25, title of section 24) and the pin table, not typed. Checks H2, N1, X1.
- Recorded stage (task 3): P2 (packet unchanged except its status line, pinned by blob and SHA-256), A1 (record complete, valid reply date not before the Revision date, no fill marker), A2 (pins equal the packet's), A3 (questions character for character, every answer non-empty and not `unanswered`, Reply given by and the date equal the answers of Q14 and Q15), A4 (outcome rule). `--print-record-skeleton` prints the only record layout (15 question blocks, 22 fill markers).
- The script writes nothing outside its own temporary directory (removed by a trap), changes no git state, and is clean under `bash -n` and `shellcheck`.

## Task Commits

1. Task 1 (tracer): `f35fd09` docs(03-01): add the owner approval check script and packet skeleton (tracer)
2. Task 2: `6e50dc7` docs(03-01): add the packet structure and the owner question contract
3. Task 3: `ce58bb9` docs(03-01): add the recorded stage and the record skeleton to the owner approval check script
4. Summary: `docs(03-01): summary` (this file)

## Verification

- `bash 03-check-owner-approval.sh --stage pending`: PASS for E1, E2, P0, B1, R1, H1, C1, K1, I1, S1, T1, H2, N1, X1; `RESULT: PASS`, exit 0 (36 commits since origin/main touch the specification; register blob `66344ffb26d26ce84b3c9a318eb8e7cb2db6146a`).
- `bash -n` and `shellcheck` exit 0; no CR byte; `git ls-files --eol` shows `i/lf w/lf`.
- Packet counts: 15 lines `### Qnn — `, 13 `- Accepting answer: `, 2 `- Answer form: `, 12 `## `, one `- Owner approval: pending`.
- `--print-record-skeleton`: 15 `### Q` blocks, 22 `@@FILL@@`, one `| Packet blob | ` row, exit 0.
- Tracer seeds (copies of the inputs built outside the repository and removed afterwards): the specification with one byte appended as `--spec` gives `FAIL R1` and `FAIL H1`, exit 1; the status line set to `approved` gives `FAIL T1`; one digit of Result blob changed gives `FAIL R1` (and `FAIL I1`); Commits touching the file set to 35 gives `FAIL C1`; one digit of Register blob changed gives `FAIL K1`.
- Structure seeds: heading of the Header and heading section removed gives `FAIL H2`; the same heading doubled gives `FAIL H2`; Q03 without the register's Reading cell gives `FAIL N1`; Q13 without the SHA-256 gives `FAIL N1`; a header of 29 characters gives `FAIL N1`; equal answer labels give `FAIL N1`; a missing `Accepting answer` field gives `FAIL N1`; a changed Version in a specification copy gives `FAIL R1`, `FAIL H1` and `FAIL N1`; a line with a home-directory path gives `FAIL X1`; an extra 40-digit hexadecimal token gives `FAIL X1`; a web address gives `FAIL X1`. Unchanged copies of the register and specification as `--register` and `--spec` give `RESULT: PASS`.
- Recorded-stage fixtures (a record produced by `--print-record-skeleton` on a copy of the packet and filled with the accepting answers, a placeholder handle and a date after the Revision date; a second copy of the packet with the recorded status line): the good fixture ends `RESULT: PASS` with `--stage recorded`. Each seeded defect fails with the named id and exit 1: recorded packet left pending (T1); one word added to the recorded packet (P2); Q03 answered `Choose alternative` with outcome approved (A4); outcome changes requested with `None.` (A4); outcome approved with Q13 `Request changes` (A4); reply date earlier than the Revision date and reply date 2026-02-30 (A1); one character of a question changed (A3); an empty answer and an answer `unanswered` (A3, and A4); Reply given by differing from Q14 (A3); one digit of two pin values changed (A2, and X1); the fill marker left in place (A1, X1, and A4); a home-directory path (X1). Extra cases also behave as intended: a valid changes requested record passes; changes requested with every answer accepting fails A4; changes requested without a bullet fails A4; an outcome `approved with remarks`, an empty Reply given by row and a second reply date line fail A1; a record heading that differs from the packet fails A3; a web address fails X1.
- `bash 03-check-owner-approval.sh --stage recorded` on the real, pending packet with no record exits 2 and writes no file.
- `git hash-object docs/method/GG-SAD_normative_method_specification.md` prints `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`; `git diff --name-only origin/main...HEAD -- src .ggsad specs tests docs AGENTS.md CLAUDE.md` prints only the specification path (unchanged content). Each task commit lists exactly the files of its task.
- Precondition of task 1 held: clean tree, specification blob and SHA-256 as pinned, base blob as pinned, `02-check-normative-diff.sh --final` ends `RESULT: PASS`.

## Deviations from Plan

### Process

**1. [Tracer feedback gate] No human-verify checkpoint returned after the tracer**
- **Found during:** Task 1
- **Issue:** In an interactive run the tracer rule is to stop with a human-verify checkpoint after committing the tracer. The orchestrator assigned the whole plan for sequential execution through the summary, and the tracer's `<verify>` is fully automated.
- **Action:** The tracer's verification was run end-to-end after its commit and with the seeded failures (all fail for the right reason) before any expansion task, which is the autonomous form of the gate. No checkpoint was returned.

### Auto-added (Rule 2, correctness of the gate)

**2. Stricter P0, S1 and T1 than the plan text.** P0 also requires that Reviewed file and Register file equal the repository paths and that every value is exactly one backticked token. S1 rejects any changed path other than the specification and `.planning/`, which includes AGENTS.md and CLAUDE.md (the plan wording was ambiguous about them). T1 also rejects a reply-date line or a Reply given by row in the packet in both stages, so the reply cannot sit in the packet.

**3. K1 reads the register path from the packet.** The HEAD lookup uses the packet's Register file pin and the blob comes from the `--register` file, so a test copy of the register does not break the HEAD comparison.

**4. Raw-byte hashing.** Blobs are computed with `git hash-object --no-filters` so that they match the SHA-256 of the same bytes even though this machine has `core.autocrlf=true`.

**5. N1 also checks heading topics and the Q11 label.** Each block heading must read `### Qnn — topic` with the stated topic, and the Q11 accepting answer must read `Accept all 141`.

**6. A1 and the skeleton.** A1 also requires the Packet file row to equal the repository packet path, the three record headings in order, and a non-empty What follows section. Option `-h` exits 0 (usage to standard output); an unknown option exits 2.

### Ambiguity resolved toward the stricter reading

**7. Outcome changes requested.** The plan's truth for HC-4 says a requested change is "at least one differing answer or a stated change"; the task 3 action says Q13 or another answer must differ and the section must list a bullet. A4 follows the action text, so a stated change without a differing answer fails. An owner who wants a change while accepting the readings answers Q12 or Q13 with the other label, which is a differing answer.

**8. Question text of Q10.** The title of section 24 is written between double quotes in the question.

## Known Stubs

Intentional, resolved by plan 03-02 (not by this plan): the sections `What you are asked to decide`, `Review map: SPEC-01 to SPEC-18`, `Owner questions OQ-8 to OQ-15`, `Exempt set of Section 24.1`, `Header and heading`, `Drafting choices DC-01 to DC-141`, `Dispositions of the review findings`, `Recorded findings and flagged items`, `Unproven items (informational, for Phase 4)` and `Hand-off list (informational, for the engine phases)` of the packet have headings and no body text, so the packet cannot yet be put to the owner. Plan 03-02 writes them and extends the script; any change of the register or the specification before then voids the pins.

## Unverified

- The script cannot prove who answered. It proves that a record is complete, consistent with the packet's questions and the outcome rule, and tied to the pinned text. The channel of the reply (the interactive question tool, relayed by the orchestrator) has to be recorded in the record by plan 03-03.
- B1 compares with the local `origin/main` ref; it was not refreshed against the remote.
- The limits of the interactive question tool (header and label lengths) are checked against the plan's values (12 and 30 characters), not against the tool itself.
- Nothing in this plan states or implies that owner approval or any independent review has taken place; APPR-01 is open.

## Threat Flags

None. The script is read-only, writes only to its own temporary directory, and runs no git command that writes.

## Self-Check: PASSED

- Files exist: the check script, the packet, and this summary.
- Commits exist: `f35fd09`, `6e50dc7`, `ce58bb9`.
- `--stage pending` ends `RESULT: PASS`; the specification blob equals `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`; no owner field is filled in any committed file.
