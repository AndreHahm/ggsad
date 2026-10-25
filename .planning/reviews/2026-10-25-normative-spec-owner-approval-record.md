# Owner approval record: proposed normative method specification

- Owner approval: approved
- Owner reply date: 2026-10-25

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
| Packet file | `.planning/reviews/2026-10-25-normative-spec-owner-approval-packet.md` |
| Packet blob | `abb2a05dcf6e9a225da32922b6d3fccfbcb288e5` |
| Packet SHA-256 | `455321e7af76bb73b91ad2e95fb51b5d192aff14255818da43d1e27ef8e410de` |
| Reply given by | AndreHahm |
| Owner reply | Given by the repository owner through the interactive question tool and relayed by the orchestrating session |
| Check results | Pending-stage run before the reply: `RESULT: PASS`; final diff check: `RESULT: PASS` |

## Questions and answers

### Q01 — OQ-8

- Question: OQ-8: Restore a `review` gate kind with an action that records a review result (reviewer, reviewed revision, result)? Drafted reading: The kind is dropped; a review is a `sign-off` or a `check` gate (DC-111). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q02 — OQ-9

- Question: OQ-9: May a `core` change use combination mode, so that layer 6 applies to it? Drafted reading: No; layer 6 gives a `core` change no gate and combination mode is specified for `full` (DC-134). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q03 — OQ-10

- Question: OQ-10: May a change name a compliance profile that is stricter than the active one of the project? Drafted reading: No; the compliance profile of a change equals the one of the project (DC-135). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q04 — OQ-11

- Question: OQ-11: May an agent self-approve under `lean`? Drafted reading: No; self-approval means the requesting human (DC-136). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q05 — OQ-12

- Question: OQ-12: Should the decisions of 5.4 have an assurance floor above A0? Drafted reading: No floor; the level that 24.3 requires applies, A0 when none is stated (DC-137). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q06 — OQ-13

- Question: OQ-13: Should the assurance-relevant configuration be protected beyond the recorded required level (hashed into the gate definitions or kept outside the working tree)? Drafted reading: No; the ratchet covers the approval kinds and the residual is stated in 24.3 (DC-130). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q07 — OQ-14

- Question: OQ-14: May a question stay open through the phases before the Definition of Done of the specify phase? Drafted reading: The question stays open; `complete` answers `blocked` and the Definition of Done is not satisfied (DC-138). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q08 — OQ-15

- Question: OQ-15: Should an approved opt-out replace the required allowed path list of a `full` change? Drafted reading: No opt-out; the list is required for Ready-to-Build (DC-139). Do you accept the drafted reading?
- Answer: Accept drafted reading

### Q09 — Exempt set

- Question: Section 24.1 stops every state-changing operation while a change's gate definitions differ from the approved ones, except cancel, supersede, and the re-approval of the gate definitions; the roadmap wording is every operation except cancellation. Do you accept this exempt set?
- Answer: Accept exempt set

### Q10 — Header and heading

- Question: The header of the text reads Version 1.4 with a Revision line dated 2026-10-25, and Section 24 is titled "Protections Shared by Both Profiles". Do you keep the version number and the heading as drafted?
- Answer: Keep both

### Q11 — Drafting choices

- Question: The register lists 141 drafting choices, DC-01 to DC-141. Do you accept all of them as drafted? A choice you overrule is a requested change; if you overrule any, a follow-up asks for the ids.
- Answer: Accept all 141

### Q12 — Recorded findings and flagged items

- Question: Four review findings (IN-02, IN-08, IN-11, IN-14) are recorded without a text change, and seven edge items (F1 to F7) are flagged without text. Do you accept them as recorded? A change you request is a requested change.
- Answer: Accept as recorded

### Q13 — Approval

- Question: Do you approve the exact text identified by result blob ed758c46d5ac901359ab2c0df8e437ef89fed0f1 and SHA-256 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3, 4649 lines, together with the answers you gave to the earlier questions, or do you request changes? An answer that differs from a drafted reading is a requested change, not an approval.
- Answer: Approve exact text

### Q14 — Reply given by

- Question: Under which name or handle should this reply be recorded for the repository owner?
- Answer: AndreHahm

### Q15 — Reply date

- Question: Which date is your reply date? Give it as YYYY-MM-DD.
- Answer: 2026-10-25

## Requested changes

None.

## What follows

The owner approved the exact text identified above. The text is pinned for the independent review of a later phase, which a reviewer that is not the Requestor performs; this record does not start it. Any later edit of the reviewed file voids this approval and needs a new packet and a new record.

This record is evidence only. It does not change the reviewed file.
