---
phase: 03-owner-approval
plan: 02
subsystem: governance-gate
tags: [owner-approval, evidence-packet, coverage-checks, review-map, normative-specification]
status: complete

requires: ["03-01"]
provides:
  - "Complete pending owner approval packet .planning/reviews/2026-10-25-normative-spec-owner-approval-packet.md: decision section, review map for SPEC-01 to SPEC-18, owner questions OQ-8 to OQ-15, exempt set, header, 141 drafting choices, 44 finding dispositions, recorded findings, flagged items, unproven items, hand-off items"
  - "Check script with the coverage and fidelity checks D1 D2 M1 M2 M3 O1 O2 L1 and the slot rule of T1 (22 checks in stage pending)"
affects: [03-03 owner checkpoint and record, milestone v1.1 Phase 4]

actuals:
  tokens: 22600
  tasks: 3
  commits: 4

tech-stack:
  added: []
  patterns:
    - "Register-copied sections are generated, not typed; D1 and D2 compare every register row and bullet with the packet, so a silent omission or rewording fails a check"
    - "Review map rows are checked live: every view command is parsed for its own requirement id and run against the history (M1); section numbers and acceptance examples are resolved in the pinned text (M3)"
    - "Alternatives to the eight conservative readings state only what the register and the review finding state; an unstated consequence reads 'not stated in the register'"

key-files:
  created:
    - .planning/phases/03-owner-approval/03-02-SUMMARY.md
  modified:
    - .planning/reviews/2026-10-25-normative-spec-owner-approval-packet.md
    - .planning/phases/03-owner-approval/03-check-owner-approval.sh

key-decisions:
  - "A-1 is now put in front of the owner (decision section): the diff that is approved is the whole specification file identified by content (base blob to result blob), not a commit range; a changed answer or an overruled drafting choice is a requested change. It stays an open assumption until the owner reads it."

patterns-established:
  - "Twelve identical unanswered slot lines (eight owner questions, exempt set, header, drafting choices, recorded findings); T1 rejects any other count, form or distribution in both stages"

requirements-completed: []  # APPR-01 stays open: it is satisfied only by a recorded owner approval (plan 03-03).

duration: "one session"
completed: 2026-10-25
---

# Phase 3 Plan 02: Owner Approval Packet Content Summary

The pending packet is complete and the script proves nothing of the register is missing or reworded; no owner field is filled and the packet claims neither an approval nor an independent review.

## Accomplishments

- Tracer (task 1): sections "Drafting choices", "Dispositions of the review findings", "Recorded findings and flagged items", "Unproven items" and "Hand-off list" were generated from the register in one scripted pass. The 24 Tier 1 choices were re-derived from the register and equal the plan's list exactly; the other 117 are in six themes (25, 29, 26, 25, 10, 2). Checks D1 (141 rows once, only in their section) and D2 (7 research dispositions, 44 finding rows and ids, 7 flagged rows plus header, 4 recorded findings, 13 unproven items, 8 hand-off items) pass.
- Decision section, description of the text and review map (task 2): the one decision, the diff that counts (A-1), the two outcomes, the reading order, the dated sentence that neither approval nor independent review had taken place, and what follows each outcome. The review map has 18 rows; sections, acceptance examples and drafting choices were derived from the register and the coverage table of the Phase 2 verification, the questions OQ-8 to OQ-15 are attached to the requirement that their drafting choice belongs to. Checks M1, M2, M3 pass.
- Owner questions, exempt set and header (task 3): OQ-8 to OQ-15 with the register's Question and Reading cells verbatim, the alternative, the affected text and an unanswered slot; the exempt set and the header quoted from the pinned text next to the register's own words, each with a slot; slots also at the end of the drafting choices (Q11) and the recorded findings (Q12). Checks O1, O2, L1 pass and T1 requires the twelve slots.
- `bash 03-check-owner-approval.sh --stage pending` runs 22 checks, all PASS.

## Task Commits

1. Task 1 (tracer): `eee27af` docs(03-02): add the register-copied sections of the owner approval packet (tracer)
2. Task 2: `8918374` docs(03-02): add the decision section, the text description and the review map
3. Task 3: `77e6ebd` docs(03-02): add the owner questions, the exempt set and the header section
4. Summary: `docs(03-02): summary` (this file)

## Verification

- Final run, stage pending, on the committed packet: PASS for E1 E2 P0 B1 R1 H1 C1 K1 I1 S1 T1 H2 N1 X1 D1 D2 M1 M2 M3 O1 O2 L1 (22 PASS lines), `RESULT: PASS`, exit 0. `bash -n` and `shellcheck` exit 0. D1 message: 141 rows; D2 counts 9 46 9 4 13 8 lines; M3: 94 distinct acceptance examples cited in the packet, all defined; C1: 36 commits.
- Counts: `^| DC-nn |` rows in packet and register 141 and 141; Tier 1 ids in ascending order equal the plan's list; 6 theme subsections; 44 finding rows; 7 flagged rows; 4 recorded findings; 18 review map rows; `--grep='SPEC-` once in 17 rows; `git diff --stat origin/main...HEAD -- src` once; the dated sentence once; 8 `### OQ-` headings; 12 slot lines and 12 `- Owner answer:` lines; 6 quoted lines; one `- Owner approval: pending`.
- Seeded failures (copies of the packet built outside the repository; none is part of the repository), each fails with the named check and exit 1: one DC row removed (D1); one DC row duplicated (D1); one character changed in a finding row (D2); one flagged row removed (D2); one unproven bullet removed (D2); one hand-off bullet removed (D2); one recorded finding removed (D2); one research disposition removed (D2); SPEC-07 row removed (M1, and M2 for the choices it no longer lists); SPEC-05 command in the SPEC-06 row (M1); a DC id removed from the fifth cell of SPEC-07 (M2); a Sections cell citing 99 (M3); AE-999 in an example cell (M3); `--base HEAD` makes the live view commands return no commit (M1, with B1 and C1); OQ-12 section removed (O1, O2, T1); Drafted reading of OQ-10 changed by one word (O2); a quoted line altered by one character (L1); a slot filled with an answer (T1, O1, O2); the status line set to approved (T1); one slot removed (T1, O1, O2).
- `git hash-object` of the specification prints `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`; of the register `66344ffb26d26ce84b3c9a318eb8e7cb2db6146a` (K1 passes); `git diff --name-only origin/main...HEAD -- src .ggsad specs tests AGENTS.md CLAUDE.md` prints nothing; `git status --short` is empty; no task commit deleted a file.
- `--print-record-skeleton` still prints 15 question blocks on the completed packet.

## Deviations from Plan

### Process

**1. [Tracer feedback gate] No human-verify checkpoint returned after the tracer**
- **Found during:** Task 1
- **Issue:** In an interactive run the tracer rule is to stop with a human-verify checkpoint. The orchestrator assigned the whole plan for sequential execution and the tracer's `<verify>` is fully automated.
- **Action:** The tracer was verified end-to-end (D1, D2, X1, plus the seeded failures) after its commit and before any expansion task, the autonomous form of the gate.

### Wording and form (no rule changed)

**2. Headings instead of section numbers in owner-facing prose.** The H2 headings of the packet are not numbered, so the reading order and cross references name the headings ("Owner questions OQ-8 to OQ-15", "Tier 1 under Drafting choices DC-01 to DC-141") instead of "section 5/6/7/8". Check messages still say "section 8" and "section 9" for the packet's eighth and ninth H2.

**3. Review map cells.** The register has no Evidence column on its drafting-choice rows; the acceptance examples are the coverage-table cell plus the AE ids of the Evidence cells of the findings whose drafting choice names the requirement (added only when not already inside a listed range). The words "and others" of the coverage table row of SPEC-14 were dropped (only AE-229 to AE-269 and AE-286 are listed). A Sections cell is the union of the coverage table and the register's Section cells, with ranges such as "6 to 10" expanded and non-section words dropped, so the SPEC-12 cell is long. SPEC-13 reads "not applicable" in the section and example cells and "none" in the drafting choice cell. The question cell reads "questions OQ-8 (Q01)" so the owner sees which question to answer.

**4. OQ-8 text.** AE-224 is not named: in the pinned text it now uses a `sign-off` gate, so the finding's reference to a `review` gate there no longer applies. Only AE-272, the register's evidence, is named.

**5. Quotes as separate blocks.** Each quoted line is its own blockquote (a blank line between), so the version, the revision line, the heading and the map row render separately. The slots at the end of the drafting choices (Q11) and of the recorded findings (Q12) have a one-line lead-in before the slot line.

### Auto-added (Rule 2, correctness of the gate)

**6. Stricter T1, M1 and M2 than the plan text.** T1 also checks that the slots sit in the right sections (8 in the owner questions, one each in the exempt set, the header, the drafting choices and the recorded findings). M1 also requires exactly one `--grep='SPEC-nn'` per command and 18 rows in total. M2 reports a requirement that the register names but the map does not list, in either direction. X1 needed no narrowing: no copied register row tripped it.

**7. Run time.** A full run takes about 30 seconds on this machine (process creation on Windows, 17 history queries in M1); no check was weakened for speed.

## Known Stubs

None. Every section of the packet has its content. The owner answer slots read `unanswered` by design; they are filled only in the owner approval record (plan 03-03).

## Unverified

- Whether the packet is understandable to the owner is for the owner to judge. The reading order and the review map are an attempt at review by exception, not a claim that the owner needs nothing else.
- The alternative readings and the affected text state only what the register and the review finding state; every consequence they do not state reads "not stated in the register". The judgement of what counts as stated is the drafter's and has not been independently checked.
- The Sections and Acceptance examples cells of the review map follow the register and the Phase 2 coverage table; a section or example that the register does not name for a requirement is absent, and the wording of the one-sentence restatements of the requirements is the drafter's.
- B1, C1 and M1 use the local `origin/main` ref and the local history; they were not refreshed against the remote.
- Nothing in this plan states or implies that owner approval or any independent review has taken place; APPR-01 is open and Phase 3 is not complete.

## Threat Flags

None. The script remains read-only and writes only to its own temporary directory; the packet adds no network, path or schema surface.

## Self-Check: PASSED

- Files exist: the packet, the check script and this summary.
- Commits exist: `eee27af`, `8918374`, `77e6ebd`.
- `--stage pending` ends `RESULT: PASS` with 22 PASS lines; the specification blob equals `ed758c46d5ac901359ab2c0df8e437ef89fed0f1`; no owner field is filled in any committed file.
