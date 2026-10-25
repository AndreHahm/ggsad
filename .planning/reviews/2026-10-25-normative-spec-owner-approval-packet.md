# Owner approval packet: proposed normative method specification

- Owner approval: pending

## What you are asked to decide

## The text under approval

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `ed758c46d5ac901359ab2c0df8e437ef89fed0f1` |
| Reviewed SHA-256 | `45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3` |
| Line count | `4649` |
| Diffstat | `1 file changed, 3268 insertions(+), 41 deletions(-)` |
| Commits touching the file | `36` |
| Register file | `.planning/phases/02-normative-drafting/02-DRAFTING-CHOICES.md` |
| Register blob | `66344ffb26d26ce84b3c9a318eb8e7cb2db6146a` |

## Questions put to the owner

The questions are put to the owner through the interactive question tool in groups of at most four, in the order Q01 to Q15. A question whose second answer needs specifics (Q11, Q12, Q13) is followed by one follow-up question, and the answer is recorded as the label, a colon and a space, and the follow-up text, verbatim. The answers are recorded only in the owner approval record and never in this packet.

### Q01 — OQ-8

- Header: OQ-8
- Question: OQ-8: Restore a `review` gate kind with an action that records a review result (reviewer, reviewed revision, result)? Drafted reading: The kind is dropped; a review is a `sign-off` or a `check` gate (DC-111). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q02 — OQ-9

- Header: OQ-9
- Question: OQ-9: May a `core` change use combination mode, so that layer 6 applies to it? Drafted reading: No; layer 6 gives a `core` change no gate and combination mode is specified for `full` (DC-134). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q03 — OQ-10

- Header: OQ-10
- Question: OQ-10: May a change name a compliance profile that is stricter than the active one of the project? Drafted reading: No; the compliance profile of a change equals the one of the project (DC-135). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q04 — OQ-11

- Header: OQ-11
- Question: OQ-11: May an agent self-approve under `lean`? Drafted reading: No; self-approval means the requesting human (DC-136). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q05 — OQ-12

- Header: OQ-12
- Question: OQ-12: Should the decisions of 5.4 have an assurance floor above A0? Drafted reading: No floor; the level that 24.3 requires applies, A0 when none is stated (DC-137). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q06 — OQ-13

- Header: OQ-13
- Question: OQ-13: Should the assurance-relevant configuration be protected beyond the recorded required level (hashed into the gate definitions or kept outside the working tree)? Drafted reading: No; the ratchet covers the approval kinds and the residual is stated in 24.3 (DC-130). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q07 — OQ-14

- Header: OQ-14
- Question: OQ-14: May a question stay open through the phases before the Definition of Done of the specify phase? Drafted reading: The question stays open; `complete` answers `blocked` and the Definition of Done is not satisfied (DC-138). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q08 — OQ-15

- Header: OQ-15
- Question: OQ-15: Should an approved opt-out replace the required allowed path list of a `full` change? Drafted reading: No opt-out; the list is required for Ready-to-Build (DC-139). Do you accept the drafted reading?
- Accepting answer: Accept drafted reading
- Other answer: Choose alternative

### Q09 — Exempt set

- Header: Exempt set
- Question: Section 24.1 stops every state-changing operation while a change's gate definitions differ from the approved ones, except cancel, supersede, and the re-approval of the gate definitions; the roadmap wording is every operation except cancellation. Do you accept this exempt set?
- Accepting answer: Accept exempt set
- Other answer: Change exempt set

### Q10 — Header and heading

- Header: Header
- Question: The header of the text reads Version 1.4 with a Revision line dated 2026-10-25, and Section 24 is titled "Protections Shared by Both Profiles". Do you keep the version number and the heading as drafted?
- Accepting answer: Keep both
- Other answer: Change one

### Q11 — Drafting choices

- Header: Choices
- Question: The register lists 141 drafting choices, DC-01 to DC-141. Do you accept all of them as drafted? A choice you overrule is a requested change; if you overrule any, a follow-up asks for the ids.
- Accepting answer: Accept all 141
- Other answer: Overrule some

### Q12 — Recorded findings and flagged items

- Header: Recorded
- Question: Four review findings (IN-02, IN-08, IN-11, IN-14) are recorded without a text change, and seven edge items (F1 to F7) are flagged without text. Do you accept them as recorded? A change you request is a requested change.
- Accepting answer: Accept as recorded
- Other answer: Request a change

### Q13 — Approval

- Header: Approval
- Question: Do you approve the exact text identified by result blob ed758c46d5ac901359ab2c0df8e437ef89fed0f1 and SHA-256 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3, 4649 lines, together with the answers you gave to the earlier questions, or do you request changes? An answer that differs from a drafted reading is a requested change, not an approval.
- Accepting answer: Approve exact text
- Other answer: Request changes

### Q14 — Reply given by

- Header: Reply by
- Question: Under which name or handle should this reply be recorded for the repository owner?
- Answer form: a name or handle typed by the owner; no option is recommended

### Q15 — Reply date

- Header: Reply date
- Question: Which date is your reply date? Give it as YYYY-MM-DD.
- Answer form: a calendar date typed by the owner; no option is recommended and the date is never taken from the clock

## Review map: SPEC-01 to SPEC-18

## Owner questions OQ-8 to OQ-15

## Exempt set of Section 24.1

## Header and heading

## Drafting choices DC-01 to DC-141

## Dispositions of the review findings

## Recorded findings and flagged items

## Unproven items (informational, for Phase 4)

## Hand-off list (informational, for the engine phases)

This packet is evidence only. It does not change the reviewed file.
