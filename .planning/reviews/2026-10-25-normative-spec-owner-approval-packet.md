# Owner approval packet: proposed normative method specification

- Owner approval: recorded in the owner approval record

## What you are asked to decide

You are asked for one decision: approve the exact text of the proposed normative method specification that is identified under "The text under approval", or request changes. It is put to you as fifteen questions, Q01 to Q15, through the interactive question tool; they are listed under "Questions put to the owner". Your answers are recorded only in a separate owner approval record, never in this packet.

What counts as the diff you approve: the whole of the specification file, identified by its content, from the base blob on origin/main to the result blob. The pin table gives both blob ids and the SHA-256. It is not a commit range, because a rebase merge rewrites commits and a range would then no longer identify the text. The register of drafting choices that the pin table also names is the companion source for the drafting choices and is pinned too.

The two outcomes are `approved` and `changes requested`, and nothing else. An answer that differs from a drafted reading, an overruled drafting choice, and a change to the header, the exempt set or the heading are each a requested change, not an approval. Approval of the text with some readings overruled is not an available outcome.

Reading order for a review by exception:

1. The pins under "The text under approval".
2. "Owner questions OQ-8 to OQ-15": eight readings the text left open.
3. "Exempt set of Section 24.1".
4. "Header and heading".
5. Tier 1, the high-impact choices, under "Drafting choices DC-01 to DC-141".
6. Any requirement in the review map whose diff you want to see.
7. The rest on request.

When this packet was put to the owner, owner approval and independent review of this text had not taken place.

Independent review by a reviewer that is not the Requestor, the agent that drafted the text, follows an approval as a separate gate and is not part of this packet.

What follows each outcome:

- Approved: your reply is recorded in a separate record that pins this text. This phase closes only on that record. Any later edit of the specification voids the approval.
- Changes requested: this phase stays open. A gap-closure plan edits the specification for the requested changes, and the diff identity note is re-recorded with new pins. The packet is regenerated and you are asked again. The record of this round stays as history.

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

The blob id is the git object id of the file as committed, and the SHA-256 is the hash of the same content. Neither value changes when the branch is rebased or rebase-merged, because both are computed from the content of the file and not from commits; a commit hash or a commit range would not survive that.

How to review: run `git diff origin/main...HEAD -- docs/method/GG-SAD_normative_method_specification.md` for the whole diff, or use the commands in the review map to see the commits of one requirement at a time.

Any edit of the specification file voids these values, and a new packet would be needed. The register is pinned because the sections from "Drafting choices DC-01 to DC-141" to the hand-off list reproduce it.

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

Each row is one requirement of the milestone, SPEC-01 to SPEC-18. "What is approved" restates the requirement in plain language and adds no rule. "Sections" lists the numbered headings of the pinned text that implement it. "Acceptance examples" lists the worked cases of the text (AE-nn) that test it. "Drafting choices and questions" lists the drafting choices (DC-nn, reproduced under "Drafting choices DC-01 to DC-141") whose Block cell names the requirement, then the owner questions (OQ-8 to OQ-15, asked as Q01 to Q08) that touch them. "View the diff" gives the command, run from the repository root, that shows the commits of that requirement alone, found by the requirement id in the commit subject; SPEC-13 has no commit and its command prints nothing.

| Requirement | What is approved | Sections | Acceptance examples | Drafting choices and questions | View the diff |
|---|---|---|---|---|---|
| SPEC-01 | The gate definitions of a change are fixed when the change is approved. Any later edit to them blocks every state-changing operation until a human re-approves; the exempt set is wider than the requirement states, see Q09. | 16.1, 16.4, 24, 24.1, 24.9 | AE-75 to AE-86, AE-286 | DC-03, DC-42, DC-43, DC-44, DC-125 | `git log -p --reverse --grep='SPEC-01' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-02 | Gate results have three values: satisfied, not satisfied, and could not be evaluated. A gate that cannot be evaluated is never treated as a failure and never counts toward a retry limit. | 8.5, 23.3, 23.4, 23.6, 23.7, 24, 24.2, 24.7, 25.1 | AE-61 to AE-74, AE-280, AE-222, AE-223, AE-273, AE-279, AE-281 | DC-04, DC-23, DC-40, DC-41, DC-45, DC-46, DC-47, DC-48, DC-57, DC-58, DC-112, DC-118, DC-120, DC-121 | `git log -p --reverse --grep='SPEC-02' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-03 | The result envelope gains a fourth result, `blocked`: a recorded evaluation that did not close the change, always with `changed` true. `rejected` means nothing was written and is never `changed`. | 4.3, 8.3, 8.5, 11.2, 12.1, 12.2, 16.1, 16.4, 20, 22.1, 22.2, 22.3, 23.1, 23.2, 23.4, 23.6, 24.2, 24.7 | AE-111 to AE-120, AE-259, AE-102, AE-121, AE-122, AE-154, AE-268, AE-280, AE-287, AE-288 | DC-05, DC-24, DC-25, DC-54, DC-55, DC-56, DC-119, DC-120, DC-122, DC-132, DC-133 | `git log -p --reverse --grep='SPEC-03' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-04 | Assurance levels A0 to A2 and the signed-approval statement (operation, change, position in the history of the change, signer, exact content approved) are normative; verifiers such as an SSH signature or a platform review are optional. An agent able to use the credentials of a human can act as that human. | 4.3, 5.3, 5.4, 23.7, 24.3, 24.4, 24.5, 24.10, 25.1, 25.2 | AE-125 to AE-136, AE-289, AE-292, AE-293, AE-102, AE-154, AE-159, AE-161, AE-198, AE-221, AE-227, AE-276 | DC-11, DC-59, DC-60, DC-61, DC-62, DC-63, DC-64, DC-115, DC-130, DC-131, DC-136, DC-137, DC-140; questions OQ-11 (Q04), OQ-12 (Q05), OQ-13 (Q06) | `git log -p --reverse --grep='SPEC-04' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-05 | History consistency is distinguished from history completeness. Where a profile demands high assurance, an external anchor, or an equivalent, is required to detect truncation. | 23.4, 24.3, 24.4 | AE-137 to AE-146, AE-278 | DC-11, DC-65, DC-66, DC-67, DC-116 | `git log -p --reverse --grep='SPEC-05' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-06 | A change has a scope, measured against the commit the change started from; work outside it is a hard failure. A change runs isolated from unrelated uncommitted work. | 6.1, 9.6, 16.1, 24.5, 25.1 | AE-147 to AE-157, AE-253, AE-282, AE-294 | DC-21, DC-68, DC-69, DC-70, DC-71, DC-72, DC-73, DC-123, DC-139; questions OQ-15 (Q08) | `git log -p --reverse --grep='SPEC-06' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-07 | A verification gate can carry a recorded baseline of already-failing tests: it passes when every failure is on the baseline, fails and names any new failure, and is not evaluable when the failures cannot be read. | 24.2, 24.6 | AE-87 to AE-96, AE-254 | DC-23, DC-50 | `git log -p --reverse --grep='SPEC-07' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-08 | A hard failure closes the change as failed without human action. A soft failure pauses the change for a human disposition: close as failed, or a recorded override that grants a bounded number of further attempts and lapses when the gates are amended. | 12.2, 16.4, 20, 24.2, 24.7 | AE-97 to AE-110, AE-255, AE-279 | DC-19, DC-49, DC-51, DC-52, DC-53, DC-55, DC-118 | `git log -p --reverse --grep='SPEC-08' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-09 | Open questions are recorded as change state and can be answered by a choice among declared options. Specification approval and closure are blocked while any question is unanswered. | 9.4, 9.5, 10.4, 23.4, 23.5, 24.8 | AE-171 to AE-182, AE-256, AE-263, AE-275 | DC-08, DC-77, DC-78, DC-79, DC-114, DC-138; questions OQ-14 (Q07) | `git log -p --reverse --grep='SPEC-09' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-10 | Evidence is executable and tied to a requirement. A change with no requirements has no complete evidence. | 16.1, 16.4, 23.7, 24, 24.1, 24.9 | AE-163 to AE-170, AE-257, AE-286 | DC-18, DC-75, DC-76, DC-125 | `git log -p --reverse --grep='SPEC-10' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-11 | The interpreter that runs gate commands is explicit and opt-in. The text states the trust consequence: code in git-ignored locations is invisible to the scope check. | 24.3, 24.10, 25.1 | AE-158 to AE-162, AE-258, AE-289 | DC-74, DC-130; questions OQ-13 (Q06) | `git log -p --reverse --grep='SPEC-11' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-12 | Both method profiles are specified: `core`, the simplified four-state model, and `full`, the phases, readiness and done pairs, size classes and document hierarchy of the current specification. The text states which requirements apply to which and how a change moves between them. | 3.7, 4.1, 4.3, 5.1, 5.2, 5.6, 6, 7, 8, 9, 10, 11.2, 12.1, 14.1, 16.5, 19, 20, 21, 22.2, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 24, 24.2, 24.3, 24.5, 24.7, 24.8, 24.10, 25.2 | AE-01 to AE-08, AE-09 to AE-59, AE-291, AE-102, AE-129, AE-154, AE-161, AE-198, AE-222, AE-223, AE-268, AE-270, AE-271, AE-272, AE-273, AE-274, AE-275, AE-276, AE-277 | DC-02, DC-09, DC-22, DC-24, DC-26, DC-27, DC-28, DC-29, DC-30, DC-31, DC-32, DC-33, DC-34, DC-35, DC-36, DC-37, DC-38, DC-39, DC-57, DC-80, DC-108, DC-109, DC-110, DC-111, DC-112, DC-113, DC-114, DC-115, DC-117, DC-122, DC-131, DC-135; questions OQ-8 (Q01), OQ-10 (Q03) | `git log -p --reverse --grep='SPEC-12' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-13 | No file under `src/ggsad/` is modified while the normative text is drafted. | not applicable (no section; the diff under src/ is empty) | not applicable (no example; nothing is specified) | none | `git diff --stat origin/main...HEAD -- src` (prints nothing) |
| SPEC-14 | `full` carries the protections of SPEC-01 to SPEC-11 as invariants of both profiles, is marked specified but not implemented, and each `full` rule has an acceptance example of the kind the `core` rules have. | 4.1, 4.3, 6, 7, 8, 9, 10, 16.1, 16.4, 21, 24, 24.5, 24.9, 25.1 | AE-229 to AE-269, AE-286 | DC-06, DC-07, DC-10, DC-21, DC-22, DC-101, DC-102, DC-103, DC-104, DC-107, DC-125 | `git log -p --reverse --grep='SPEC-14' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-15 | State is a JSON document (`state.json`) with a defined canonical form for hashing. The examples and templates of the specification are updated accordingly. | 4.3, 16.1, 23.1, 23.2, 23.4, 24.2, 24.3, 24.5, 24.10, 25.1, 25.2 | AE-183 to AE-202, AE-102, AE-129, AE-154, AE-161, AE-281, AE-282, AE-283, AE-284, AE-285, AE-288 | DC-07, DC-14, DC-16, DC-80, DC-81, DC-82, DC-83, DC-84, DC-85, DC-86, DC-95, DC-121, DC-123, DC-124, DC-127, DC-128, DC-129, DC-131, DC-133 | `git log -p --reverse --grep='SPEC-15' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-16 | Profile resolution is the six-layer order of section 5.3, and a lower layer must not weaken a higher one. `core` implements four of the six layers. | 3.8, 4.2, 5.3, 5.4, 17, 23.4, 23.7 | AE-218 to AE-228, AE-290, AE-293 | DC-12, DC-13, DC-96, DC-97, DC-98, DC-99, DC-100, DC-105, DC-134, DC-140; questions OQ-9 (Q02) | `git log -p --reverse --grep='SPEC-16' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-17 | `reopen` is specified for `full` and absent from `core`, and the transition table states this per profile. | 8.3, 8.4, 23.4 | AE-48, AE-217, AE-246 | DC-02, DC-94 | `git log -p --reverse --grep='SPEC-17' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |
| SPEC-18 | Every artifact carries `schema_version`, an unknown version is refused, and migration is an explicit, recorded command. | 4.3, 22.1, 22.2, 24.3, 24.5, 24.10, 25.2, 25.3 | AE-203 to AE-214, AE-102, AE-129, AE-154, AE-161, AE-198 | DC-15, DC-25, DC-87, DC-88, DC-89, DC-90, DC-91, DC-92, DC-93, DC-126, DC-131 | `git log -p --reverse --grep='SPEC-18' origin/main..HEAD -- docs/method/GG-SAD_normative_method_specification.md` |

## Owner questions OQ-8 to OQ-15

Each of these eight questions is left open by a conservative reading in the text. The register holds the reasoning for each reading, under the drafting choice named in the question. A finding is a point raised by the advisory review of the text, and its row is in the table under "Dispositions of the review findings". You give your answers at Q01 to Q08; the slot under each question stays unanswered here.

### OQ-8 — Restore a review gate kind

- Finding: CR-01 (its row is under "Dispositions of the review findings")
- Question: Restore a `review` gate kind with an action that records a review result (reviewer, reviewed revision, result)?
- Drafted reading: The kind is dropped; a review is a `sign-off` or a `check` gate (DC-111).
- Alternative reading: Restore the `review` done-gate kind and add an action that records a review result (reviewer, reviewed revision, result).
- Text that changes under the alternative: Sections 23.3 and 23.4 (the gate kind and a new action row), 22.1 (a new operation) and 25.1 (a new field), as the register and the review finding say; AE-272 shows the drafted reading and would change; whether further examples change is not stated in the register.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

### OQ-9 — Combination mode for the core profile

- Finding: WR-18 (its row is under "Dispositions of the review findings")
- Question: May a `core` change use combination mode, so that layer 6 applies to it?
- Drafted reading: No; layer 6 gives a `core` change no gate and combination mode is specified for `full` (DC-134).
- Alternative reading: A `core` change may use combination mode, and layer 6 applies to it (the register states this alternative in DC-134).
- Text that changes under the alternative: Sections 5.3 and 17 and the examples AE-290 and AE-226 change; section 25.3 is unchanged in the draft, and whether it changes under the alternative is not stated in the register.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

### OQ-10 — A change profile stricter than the project's

- Finding: WR-19 (its row is under "Dispositions of the review findings")
- Question: May a change name a compliance profile that is stricter than the active one of the project?
- Drafted reading: No; the compliance profile of a change equals the one of the project (DC-135).
- Alternative reading: A change may name a compliance profile that is at least as strict as the active one of the project (the wording of the review finding, which DC-135 did not take).
- Text that changes under the alternative: Sections 5.6 and 23.1 (the rule that the compliance profile of a change equals the one of the project) and the example AE-291; the register states that a later change of the compliance profile of the project is not addressed; further reach is not stated in the register.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

### OQ-11 — Agent self-approval under lean

- Finding: WR-20 (its row is under "Dispositions of the review findings")
- Question: May an agent self-approve under `lean`?
- Drafted reading: No; self-approval means the requesting human (DC-136).
- Alternative reading: An agent may self-approve under `lean` outside the non-delegable set of 5.4.
- Text that changes under the alternative: The sentence that every approval needs a human would be restricted in 24.3 and in 23.4 to the approvals that 5.4 does not allow to be self-approved under `lean`, as the review finding says; sections 5.4 and 5.1 and the example AE-292 follow; the exact wording is not stated in the register.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

### OQ-12 — An assurance floor for the decisions of 5.4

- Finding: WR-21 (its row is under "Dispositions of the review findings")
- Question: Should the decisions of 5.4 have an assurance floor above A0?
- Drafted reading: No floor; the level that 24.3 requires applies, A0 when none is stated (DC-137).
- Alternative reading: The decisions of 5.4 get an assurance floor above A0.
- Text that changes under the alternative: Sections 5.4 and 24.3 and the example AE-293; which level the floor would be is for the owner to name, and the exact wording is not stated in the register.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

### OQ-13 — Protecting the assurance configuration

- Finding: WR-24 (its row is under "Dispositions of the review findings")
- Question: Should the assurance-relevant configuration be protected beyond the recorded required level (hashed into the gate definitions or kept outside the working tree)?
- Drafted reading: No; the ratchet covers the approval kinds and the residual is stated in 24.3 (DC-130).
- Alternative reading: The assurance-relevant configuration is protected beyond the recorded required level, by hashing it into the approved gate definitions or by keeping it outside the working tree.
- Text that changes under the alternative: Sections 24.3, 24.10 and 25.1 and the examples AE-289 and AE-159; the exact wording is not stated in the register. DC-130 states what the drafted reading leaves open: a participant that can change the configuration can still lower a minimum for a change whose history records no earlier approval of that kind, and for the kinds that record no required level.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

### OQ-14 — A question left open before the specify Definition of Done

- Finding: WR-25 (its row is under "Dispositions of the review findings")
- Question: May a question stay open through the phases before the Definition of Done of the specify phase?
- Drafted reading: The question stays open; `complete` answers `blocked` and the Definition of Done is not satisfied (DC-138).
- Alternative reading: Questions raised in the specify phase are excluded from the Definition of Wait condition until the Definition of Done of that phase (DC-138 states this alternative).
- Text that changes under the alternative: Sections 9.4, 24.8 and 8.5 and the example AE-263; the exact wording is not stated in the register.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

### OQ-15 — Opting out of the allowed path list

- Finding: WR-26 (its row is under "Dispositions of the review findings")
- Question: Should an approved opt-out replace the required allowed path list of a `full` change?
- Drafted reading: No opt-out; the list is required for Ready-to-Build (DC-139).
- Alternative reading: An approved opt-out replaces the required allowed path list for a `full` change that states its scope in words only (DC-139 states this alternative).
- Text that changes under the alternative: Sections 6.1, 9.6, 24.5 and 16.1 and the examples AE-294 and AE-253; the review finding says an unmeasurable scope in `full` would then be `not_applicable` for a change that opts out with an approved record; the form of that record is not stated in the register.
- Owner answer: unanswered (the answer is recorded only in the owner approval record)

## Exempt set of Section 24.1

Section 24.1 fixes the gate definitions of a change when the change is approved. While the gate definitions differ from the approved ones, every state-changing operation is stopped, except the operations quoted below, so that a change whose definitions were altered can still be ended or approved again. The text exempts three operations, which is wider than the success criterion of the roadmap, which says every operation except cancellation.

The text of Section 24.1 reads:

> Three operations are exempt from the comparison and MUST NOT be stopped by it: `cancel`, `supersede`, and the approval of the gate definitions that replaces the approved hash.

> The approval that replaces the approved hash is the re-approval; without the exemption, no change could leave this state.

The register explains the difference as follows:

The set of operations that the comparison of gate definitions does not stop is wider than the phrase "every operation except cancellation" in the success criterion: it holds `cancel`, `supersede` (which the move rule of 5.6 needs), and the re-approval of the gate definitions. The owner can overrule this (DC-03, DC-44).

The choices behind the exempt set are DC-03 and DC-44, in Tier 1 under "Drafting choices DC-01 to DC-141". You give your answer at Q09.

- Owner answer: unanswered (the answer is recorded only in the owner approval record)

## Header and heading

The header and the heading of Section 24 are quoted from the pinned text:

> **Version:** 1.4

> **Revision:** 2026-10-25 — Added the method profiles `core` and `full`, the protections that both method profiles share, JSON state with a canonical form, and schema versions with explicit migration, and aligned the gate model, the evaluation order, the approval rules, and the identifier rules.

> ## 24. Protections Shared by Both Profiles

> | 24. Protections Shared by Both Profiles | Method Semantics |

The register adds this note:

The header of the proposed text reads `Version: 1.4` and a Revision line dated 2026-10-25 (DC-106, DC-141). The number is a drafting value so that it can be changed in one line. Version 1.3 stays pinned in three places that this phase does not touch (see the hand-off list).

The choices behind the header are DC-20, DC-106 and DC-141; DC-106 and DC-141 are in Tier 1 and DC-20 is under the theme "Text-wide choices and the header", all under "Drafting choices DC-01 to DC-141". The version number is a drafting value and can be changed in one line. The check script of the drafting phase warns about the unqualified wording "Both Profiles" in the heading and in the section map row; this is a style heuristic and not a defect. You give your answer at Q10.

- Owner answer: unanswered (the answer is recorded only in the owner approval record)

## Drafting choices DC-01 to DC-141

A drafting choice is the reading the drafter took where the owner decisions left room. Each row has an id (DC-nn), the requirement block it belongs to (SPEC-nn; see the review map), the section of the text it concerns, and the reading taken. You can overrule any choice by its id at question Q11, and an overruled choice is a requested change. Each row below is the register row, character for character, and the register stays the home of the full list. The choices are ordered by impact first (Tier 1), then by theme.

### Tier 1: high-impact choices

Tier 1 is every drafting choice that an owner question, a disposition of a research question OQ-1 to OQ-7, the exempt set of Section 24.1, the version note of the header, or a review finding with the disposition FIXED-CONSERVATIVE cites; there are 24.

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-02 | SPEC-12, SPEC-17 | 23.4 | In `core`, `supersede` closes the change as `cancelled` with a required `replaced_by` that names a different existing change. |
| DC-03 | SPEC-01 | 24.1 | "Cancellation" includes `supersede`. The re-approval itself is exempt. A read-only report answers `rejected` with `changed` false and says that the gates are not enforced. |
| DC-07 | SPEC-15, SPEC-14 | 4.3, 25.1 | `core` keeps `state.json` always. `full` keeps the optional-state allowance of 4.3; the rules that read or write the history are enforced mechanically only for a change that has a state document, and an implementation does not report them as enforced for an inline record. |
| DC-11 | SPEC-04, SPEC-05 | 24.3, 24.4 | No assurance floor is assigned per compliance profile. "High assurance" means that the applicable configuration requires approvals at A2. |
| DC-12 | SPEC-16 | 23.7, 5.3 | The base gate set belongs to the method profile: for `core`, the scope violation gate (fail, hard), the unanswered question gate (wait), the stale specification approval gate (wait), and the incomplete evidence gate (done). Present on every change, not removable, not alterable by a lower layer. Identifiers added by DC-96. |
| DC-13 | SPEC-16 | 5.3, 4.2 | Weakening is absolute. The word "silently" is dropped from the rule. The exception of 4.2 is limited to the local specification of a `full` change (DC-98). |
| DC-17 | all | text | The specification cites no decision, requirement, prototype, or finding id; check X1 passes. The Revision line names no requirement id. |
| DC-44 | SPEC-01 | 24.1 | Every state-changing operation except `cancel`, `supersede`, and the approval that replaces the approved hash is rejected while the hashes differ (including `approve` of another target, `fail`, `adopt`, `ask`, `answer`). The re-approval is an amendment naming both hashes. |
| DC-96 | SPEC-16 | 5.3, 23.7 | The four base gates of `core` have the identifiers `scope-violation`, `unanswered-question`, `stale-spec-approval`, and `incomplete-evidence`. A change definition that redefines one of them or states that it does not apply is rejected at creation and again before the approval of the gate definitions; the stable issue code is `gate-weakened` when the listed gate differs in kind, condition, or severity or the gate is stated not to apply, and a listed gate that does not differ is rejected as a duplicate identifier (23.3). |
| DC-97 | SPEC-16 | 5.3 | Weakening is: remove a gate (state that it does not apply, or leave it out of a definition that replaces the gates of the higher layer), alter its condition (including kind and every declaration 24.1 fixes), lower its severity, lower the assurance level it requires. Strengthening is adding a gate with an identifier of its own or raising a level in the project configuration. A lower layer that states a lower assurance level than a higher layer requires does not lower it (the higher level is required, 24.3); the statement is accepted and has no effect, consistent with the example of 24.3 on the gate minimum. The result does not depend on the order of listing. Changed by DC-140. |
| DC-98 | SPEC-16 | 4.2, 5.3 | The approved exception of 4.2 exists only for the local specification of a `full` change that departs from a project-wide definition. A human approves it at the level 24.3 sets for the approval of gate definitions; it applies to that change only; it is recorded in the Deviations of the evidence (16.4); it never reaches the invariant core, the protections of section 24, or the base gates; a `core` change has none. It is a recorded human decision and not a weakening by a lower layer. The existing 4.2 sentence is not rewritten; a paragraph is added after it. For the owner to overrule (research OQ-2). |
| DC-104 | SPEC-14 | examples | The rule unit is as in the owner's granularity rule: 30 rule units (4.1, 5.5, 6.1 to 6.3, the four flows of 7.1, 8.2, the eight actions of 8.3, 8.4, 8.5, the eight pairs 9.k with 10.k, and the `full`-only parts of 11.2 and 12.2) plus the 11 realizations, 41 units. Each unit has one example block that shows a normal and a failure or boundary case. Unit 8.4 has two blocks, because the example of `reopen` already existed. The examples AE-218 to AE-228 belong to 5.3 and AE-229 to AE-269 to the 41 units. The pair examples sit after each Definition of Done and are cited from both 9.k and 10.k. |
| DC-106 | header | header | Version 1.4 (owner's number from the planning record; the packet states it so the owner can change it). The Revision line is dated 2026-10-24, the day of drafting, followed by an em dash and one sentence that names the amendment (method profiles, shared protections, JSON state, schema versions) and no id. Changed by DC-141. |
| DC-111 | SPEC-12 | 23.3 | The done-gate kind `review` is dropped, not realized. A review before closure is a `sign-off` gate or a `check` gate; the records of 14.5 are evidence that no gate evaluates; the read-only action `review` is unchanged. The other option (a `review-result` action with a recorded reviewer, revision and result) would add an operation to 22.1 and a field to 25.1 and is left to the owner (OQ-8). AE-272. |
| DC-112 | SPEC-12, SPEC-02 | 23.3, 23.7, 24.2 | A fail or wait gate has no kind and one `condition` with exactly one of the members `command` (plus `exit_map`, optional `time_limit`), `retry_limit` (a mapping with `gate`, a `check` done gate, and `limit`; fail gate only) or `predicate` (`scope-violation` on a fail gate; `unanswered-question`, `stale-spec-approval` on a wait gate). None, two, another member, or a predicate not listed for the kind is rejected at `new`; values are rejected at the approval of the gate definitions. A command condition is evaluated as a check command and carries no baseline (24.6). The base gates are fixed in 23.7 and are not subject to the kind and form rules. AE-273; AE-222 and AE-223 state their conditions in these forms. |
| DC-120 | SPEC-02, SPEC-03 | 24.2, 8.5, 23.6 | Evaluation stops by group: the groups are the fail, wait and done gates (`core`) and DoF, DoW, DoR, DoD, next DoR (`full`, order of 8.5); a group is evaluated whole; a gate of a later group is not evaluated (no command run, no result); the rules 1 to 5 rank the results of the gates that were evaluated. In `core` an active wait gate decides before an unevaluable done gate (`blocked`, no wait record), and an unevaluable wait gate gives an `external` wait. The other option (evaluate every gate first, then rank) would run commands of gates that cannot matter. AE-280. |
| DC-130 | SPEC-04, SPEC-11 | 24.3, 24.10, 25.1 | The record carries `required_level` for the approval kinds only (approval of the specification, approval and re-approval of gate definitions, sign-off, override); the ratchet applies to these kinds. The levels A0, A1, A2 and the statement are unchanged. The interpreter is not frozen; `gate_detail` names the program that the token stood for. A participant that can change the configuration can still lower a minimum for a change whose history records no earlier approval of that kind, and for the kinds that record no `required_level` (OQ-13). AE-289, AE-159. |
| DC-134 | SPEC-16 | 5.3, 17 | A `core` change does not use integration mappings: layer 6 gives it no gate, and its gates are the base gates of 23.7 and the gates of its change definition. The combination mode of 3.8 and 17 is specified for `full` and for combination use, and the reference implementation builds neither it nor `full`. Where layer 6 applies, it MUST NOT weaken a higher layer and no external workflow bypasses a gate (3.8). Section 17 points to 5.3. 25.3 is unchanged; it governs the migration of the integration mappings as a project-level artifact and gives a `core` change no gate. The six layers keep their numbers. The alternative (`core` supports combination mode and layer 6 applies to it) is left to the owner (OQ-9). AE-290. |
| DC-135 | SPEC-12 | 5.6, 23.1 | The compliance profile of a change MUST equal the active compliance profile of the project at the time the change is created, else the creation is rejected. The wording of the finding "or a stricter one" is not taken (OQ-10). A later change of the compliance profile of the project is not addressed. AE-291. |
| DC-136 | SPEC-04 | 5.4 | Self-approval under the `lean` compliance profile means that the human who requested the work may approve it; a participant that is not a human never approves (23.4 and 24.3 stay). The earlier sentence that the allowance "is unchanged" is replaced. Whether an agent may self-approve under `lean` is left to the owner (OQ-11). AE-292. |
| DC-137 | SPEC-04 | 5.4 | "A verified human" is replaced by a testable condition: a claim satisfies a decision of the non-delegable set only if its verified level is at least the level that 24.3 requires for the action that records the decision (A0 when no gate or configuration states a minimum). No assurance floor is assigned to the decisions of 5.4 (OQ-12). The A0 paragraph of 5.4 gets AE-293. |
| DC-138 | SPEC-09 | 9.4 | Ready-to-Spec is a statement about its criteria alone. While the recorded question is unanswered, `complete` answers `blocked` (24.8) and the Definition of Done of the specify phase is not satisfied. The alternative (exclude questions raised in the specify phase from the DoW condition) is not taken (OQ-14). AE-263. |
| DC-139 | SPEC-06 | 6.1, 9.6, 24.5 | The allowed path list is in the minimum content of Class S (6.1) and is a Ready-to-Build criterion (9.6). In `full` the scope is evaluated from the first approval of the gate definitions and the record shows `not_applicable` before; in `core` it is evaluated from the start. The alternative (an approved opt-out for changes that state a scope in words only) is not taken (OQ-15). Class M and Class L state no minimum content and are not changed. AE-294. |
| DC-141 | header | header | The Revision line is dated by `date +%F` on the day of the header commit (2026-10-25), followed by an em dash and one sentence that names the amendment (method profiles, shared protections, JSON state, schema versions) and the alignment of the gate model, the evaluation order, the approval rules and the identifier rules; it holds no id and no mention of a review. The header commit has the second id-less subject `docs(02-08): header revision line after the review fixes (D-12)`, and check C1 accepts both id-less subjects and counts neither toward an id. The version stays 1.4. |

### Theme: Method profiles and the core profile

Rule: the first requirement id in the Block cell is SPEC-12 or SPEC-17.

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-09 | SPEC-12 | 23.5 | The `core` wait record is its own (kind, reason, owner, resume condition, optional expiry, optional question), with no safe state and no next action. A table maps the four kinds to wait categories. |
| DC-22 | SPEC-12, SPEC-14 | 4.1, 6 to 10, 21 | The marker sentence "This section specifies the `full` method profile (Section 5.6)." heads 4.1, 6, 7, 8, 9, and 10, with a caption under the diagram of 21 and the statement in 5.6. |
| DC-26 | SPEC-12 | 5.6, 16.5 | The method profile is chosen per change at creation; project configuration MAY name a default; the project brief template gains `## Method Profile` with the values `core | full`. |
| DC-27 | SPEC-12 | 5.6 | Default applicability: both method profiles unless a section is listed as `full` only (4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 11.1, 16.1 to 16.4, the diagram of 21). Sections 23 to 25 state their own applicability. Changed by DC-108. |
| DC-28 | SPEC-12 | 5.6 | The mixed sections 11.2 and 12.2 apply to both method profiles except the safe current state and next action of a wait state (11.2) and the final status code of a fail rule (12.2), which are `full` only. Changed by DC-110. |
| DC-29 | SPEC-12 | 5.6 | Creation with no method profile and no project default is rejected; `core` and `full` are exact lowercase identifiers and any other value is rejected. |
| DC-30 | SPEC-12 | 5.6 | The reference implementation does not implement `full` and MUST reject the creation of a change that selects it; the marking does not weaken any `full` rule. |
| DC-31 | SPEC-12 | 23.1 | Directory `specs/<change-id>/` with `change.yaml`, `spec.md`, `state.json`; fields `id`, `method_profile`, `compliance_profile`, `author`, `owner`, `goal`, `scope.allow`, `requirements`, `gates`, optional `follows`. |
| DC-32 | SPEC-12 | 23.1 | `follows` MUST name an existing change that is `closed`; the field is a reference and never changes the named change. |
| DC-33 | SPEC-12 | 23.3 | Fail and wait gates are predicate gates; an active wait gate blocks start, resume, and close without creating a wait record; done gate kinds are `check`, `review`, `sign-off`; gate identifiers are unique including base gates. Changed by DC-111 and DC-112. |
| DC-34 | SPEC-12 | 23.4 | Transition table readings: `approve` and `answer` from every state except `closed`; `ask` from `open` and `active`; `fail` only from `waiting` with a `fail-gate` record; `adopt` from any state while the history has no anchor; read-only actions `check`, `review`, `guard`. Changed by DC-113 and DC-116. |
| DC-35 | SPEC-12 | 23.6 | Evaluation order: active hard fail, a gate that could not be evaluated, active soft fail, active wait gate, then for `close` only an unsatisfied done gate. Changed by DC-120. |
| DC-36 | SPEC-12 | 23.4 | An action from a state outside its Legal From cell is rejected; the choice between `rejected` and `blocked` for an unmet precondition is settled in 22.2 and the per-action tables. |
| DC-37 | SPEC-12 | 23.5 | Resume conditions by kind: `question` when answered; `fail-gate` when a human recorded an override; `external` when the gate can be evaluated again; `manual` when the owner of the wait states that the condition holds. An overdue wait stays a wait. |
| DC-38 | SPEC-12 | 3.7, 5.1, 5.2, 14.1 | Seven bare uses of "profile" became "compliance profile"; the four rows of the 5.1 table are byte-identical; "the `lean` profile" mentions and the heading of 5.3 are left as they are. |
| DC-39 | SPEC-12 | examples | Example ids are not in document order (AE-59 sits in 23.1). |
| DC-80 | SPEC-12, SPEC-15 | 4.3 | The `core` layout of 4.3 shows `change.yaml`, `spec.md`, `state.json`, and a conditional `review.md`; review files are measured by the scope check like any other non-record file. |
| DC-94 | SPEC-17 | 8.3, 8.4 | `reopen` is marked `full` only; in `core` a closed change is final; `follows` is a reference and a new change naming a change that is not closed is rejected. |
| DC-108 | SPEC-12 | 5.6 | 11.1 is removed from the `full`-only row and falls under "every other section", so it applies to both method profiles. AE-52 stays. |
| DC-109 | SPEC-12 | 19, 20 | The two sections stay in "both". Each gains a paragraph for a `core` change. For section 20 the fail, wait, soft failure, question, done criteria and evidence conditions are mapped to gates; the conditions about the requirement coverage table, Pair Review, document consistency and references are said to be met through the requirements and gates of the change, with no document of the `full` method profile required. This last mapping is the broadest reading. AE-270. |
| DC-110 | SPEC-12 | 5.6, 23.3 | `core` is exempt from the required response, the permitted preservation actions and the required documentation of 12.2; a `core` fail gate holds `id`, `severity`, `condition`; the response is fixed by 24.7. AE-271. |
| DC-113 | SPEC-12 | 23.4 | `ask` is legal from `open`, `active` and `waiting`; a question asked while waiting leaves the wait record unchanged and blocks `resume` through the unanswered question gate. AE-274. |
| DC-114 | SPEC-12, SPEC-09 | 23.4, 23.5, 24.8 | `wait` names an existing unanswered question and never creates one; the wait owner is the question's owner and another owner is rejected; reason and resume condition default to awaiting the answer; an answered or unknown question is rejected. AE-29 stays valid. AE-275. |
| DC-115 | SPEC-12, SPEC-04 | 23.7, 24.3 | The stale approval gate is active only if the specification was approved at least once and its hash differs from the last approved hash; a never-approved specification does not stop `start`. AE-276. |
| DC-117 | SPEC-12 | 23.5 | For a wait record made by evaluation, `owner` is the owner of the change, `resume_when` is `a human recorded an override of <id>` (`fail-gate`) or `gate <id> can be evaluated` (`external`), and `reason` names the gate and the cause. Who may `resume` such a record is not restated. AE-277. |

### Theme: Gates, results and failures

Rule: the first requirement id in the Block cell is SPEC-01, SPEC-02, SPEC-03, SPEC-07 or SPEC-08.

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-04 | SPEC-02 | 24.2 | `not_applicable` stays the marker for a gate that is not evaluated by design. `not_evaluable` is a separate result and is never recorded as `not_applicable`. |
| DC-05 | SPEC-03 | 22.2 | `blocked` means: valid operation, evaluation recorded, transition did not occur. Only `close` and `resume` (`core`) and `complete` and `resume` (`full`) answer it. |
| DC-19 | SPEC-08 | 24.7 | An override gives an integer N of at least 1; the text states no default; any other value is rejected. |
| DC-23 | SPEC-02, SPEC-07 | 24.2 | The check-command gate is defined in 24.2: command as an argument list, an exit map, an unmapped exit status is `not_evaluable`. |
| DC-24 | SPEC-03, SPEC-12 | 22.2, 23.2 | `core` records `state` and `outcome`; `full` records `phase` and `status`; the `state` field of the envelope is worded per method profile. |
| DC-25 | SPEC-03, SPEC-18 | 22.1 | Section 22.1 gains "record a human decision" and `migrate`, each inserted before the last list item so that no existing list line is rewritten. |
| DC-40 | SPEC-02 | 24.2 | Result names `satisfied`, `not_satisfied`, `not_evaluable` (exact lowercase); a done gate is met, and a fail or wait gate is active, when the result is `satisfied`. |
| DC-41 | SPEC-02 | 24 intro | Identifiers, path patterns, paths, and text values compare as sequences of Unicode code points without normalization; a rule MAY state otherwise. |
| DC-42 | SPEC-01 | 24.1 | The identity of the frozen definitions is the content hash of the parsed gate definitions; comments, layout, key order, and quoting do not change it; list order does. |
| DC-43 | SPEC-01 | 24.1 | The stable issue codes `gates-changed` and `start-blocked` are named in the text. |
| DC-45 | SPEC-02 | 24.2 | A check-command gate declares a command (argument list) and an exit map; there is no default map; a time limit and an extraction rule are optional. |
| DC-46 | SPEC-02 | 24.2 | Output never changes the result the exit map decides, except for the baseline comparison of 24.6; empty output never makes a gate `satisfied`. |
| DC-47 | SPEC-02 | 24.2 | A retry limit counts `not_satisfied` over the whole life of the change, never reset; reached when count is at least limit; a limit of 0 is reached at once; `not_evaluable` neither adds nor resets. |
| DC-48 | SPEC-02 | 24.2, 23.4 | `start` is rejected, creating no wait, when a gate cannot be evaluated or a fail or wait gate would decide; `resume` replaces the earlier wait record with a record of kind `external`; read-only actions create no wait. Changed by DC-118. |
| DC-49 | SPEC-08 | 24.7 | An action that closes the change as failed because of a hard failure answers `success`. |
| DC-50 | SPEC-07 | 24.6 | Baseline entries form a set; the record names up to three new failures in ascending code point order plus the count; an empty baseline is valid; a baseline on a gate that is not a check-command gate is invalid. |
| DC-51 | SPEC-08 | 24.7 | A retry limit is a soft fail condition; a retry limit that declares `hard` is invalid. Severity values are exact lowercase. |
| DC-52 | SPEC-08 | 24.7 | An override names the soft fail condition it covers; an attempt is an evaluation by `close` or `complete` made while the override is in force; the N-th attempt is allowed and the next evaluation pauses again. |
| DC-53 | SPEC-08 | 24.7 | In `full`, the wait caused by a soft failure is category `WAIT_DECISION` with the resume condition "a human has recorded an override"; `fail` is the other disposition. |
| DC-54 | SPEC-03 | 8.3, 23.4 | Per-action results: `resume` is rejected while the resume condition is not satisfied and blocked while a gate keeps the change waiting; `start` with an unmet gate is rejected in both profiles; `reopen` is never blocked; a `complete` that preserves the phase with status `done` answers `success`. |
| DC-55 | SPEC-08, SPEC-03 | 12.2, 16.4, 20 | The 12.2 template gains a `Severity` line, the 16.4 template a line for gates that could not be evaluated, and section 20 the condition "no soft failure awaits a human disposition". The 8.3 cell of `complete` no longer lists DoF among the causes of rejection. Changed by DC-119. |
| DC-56 | SPEC-03 | 8.3 | In `full`, `start` of a phase with an unevaluable gate follows the `core` reading (rejected, no wait); only `complete` and `resume` create the `external` wait. |
| DC-57 | SPEC-02, SPEC-12 | 24 intro | The term table defines the base revision in `core` as the revision recorded when `start` succeeds and in `full` as the revision recorded when the change starts; a `---` separator precedes the heading of section 24. |
| DC-58 | SPEC-02 | examples | Example ids AE-60 to AE-124 are consecutive but not in document order. |
| DC-118 | SPEC-08, SPEC-02 | 24.7, 24.2 | `start` never closes a change; with a hard fail gate active it is rejected (`changed` false, `start-blocked`) and the failure is decided by `cancel`, `supersede` or the first completing or resuming action. AE-279. |
| DC-119 | SPEC-03 | 8.3 | The precondition of `complete` is a legal source plus the requested evaluation of the DoR (from `draft`), the DoD (from `active`) or the next DoR (from `done`); the rejection cell and the result table reject only a source that is not legal; evaluation outcomes stay `blocked`. AE-121 and AE-122 stay. |
| DC-122 | SPEC-03, SPEC-12 | 12.1, 11.2, 24.7 | AE-102 states "a done gate that stays unsatisfied"; 12.1 lists only a hard budget or cost limit among the fail categories; the 11.2 template uses `owner`, adds `outstanding`, and sets `resume_at` to `plan`, with a sentence that lists the six fields. AE-268 names the fields. |
| DC-132 | SPEC-03 | 22.1, 22.3 | 22.1 and 22.3 name the transition table of the method profile; three bullets are added before the last (record a question, adopt a history, report on a change); the report bullet is worded as the read-only actions `check`, `review`, and `guard` without a section pointer. AE-287. |
| DC-133 | SPEC-03, SPEC-15 | 4.3, 23.1, 23.4, 16.1 | The identifier syntax is `[A-Za-z0-9][A-Za-z0-9._-]*` (whole identifier), no trailing `.`, no reserved device name (ASCII case-folded), unique after ASCII case folding, for `id`, Change ID, `follows` and `replaced_by`. Reserved names followed by an extension (such as `nul.txt`) and non-ASCII case folding are not addressed. AE-288. |

### Theme: Trust, scope, questions and evidence

Rule: the first requirement id in the Block cell is SPEC-04, SPEC-05, SPEC-06, SPEC-09, SPEC-10 or SPEC-11.

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-08 | SPEC-09 | 24.8, 9.5, 10.4 | Acceptance of an open question is an answer. The Open Questions section of 16.1 is a view; the recorded state governs. |
| DC-18 | SPEC-10 | 24.9 | An executable check bound to each requirement is required for complete evidence; the records of 15 supplement it. |
| DC-21 | SPEC-06, SPEC-14 | 24.5, 16.1 | A `full` change gets a machine-checkable allowed path list in the Scope of the change specification (DC-102). Scope is measured against "the revision the change started from". |
| DC-59 | SPEC-04 | 24.3 | Level names are the exact strings `A0`, `A1`, `A2`. A1 is a platform review of the checked-out revision; the specification names no platform. |
| DC-60 | SPEC-04 | 24.3 | The required level of an action is the higher of the gate minimum and the project configuration minimum for the kind of action; an unstated minimum is A0. |
| DC-61 | SPEC-04 | 24.3 | Human-only actions are every approval, sign-off, override, an answer to a question with a human owner, `cancel`, `supersede`, `fail`, `adopt` (`supersede` is added to the list the plan named, because 23.4 already requires a human). The identity of a human carries the prefix `human:`. |
| DC-62 | SPEC-04 | 24.3 | The statement is built by the implementation: a first line with a format identifier and version, then operation, change, version (history position), identity, and details sorted by name; values JSON-encoded; the signed bytes are the UTF-8 lines ended by line feeds. |
| DC-63 | SPEC-04 | 24.3 | An approval binds the content hash of the specification, of the gate definitions, or of the gate definitions plus the gate or fail condition identifier. The specification approval is stale while the current hash differs. Changed by DC-115. |
| DC-64 | SPEC-04 | 24.3 | An implementation that creates signatures SHOULD refuse an unprotected private key unless a human allows it; a participant who can write the signers file can list its own key (stated plainly). |
| DC-65 | SPEC-05 | 24.4 | An anchor or an equivalent is required only where the configuration requires approvals at A2; an equivalent is defined by properties; the anchor is kept outside the working tree and outside the history. Changed by DC-116. |
| DC-66 | SPEC-05 | 24.4 | `adopt` is rejected when the history is not consistent, in addition to the 23.4 precondition that no anchor exists, and needs a human at the level 24.3 requires. |
| DC-67 | SPEC-05 | 24.4 | Entry fields `n`, `prev`, `body`, `hash`; the first `prev` is `sha256:` plus 64 zero digits; the entry hash is over the canonical form of `prev` and `body`; a history without an entry is not consistent. |
| DC-68 | SPEC-06 | 24.5 | In `full` the allowed path list is a list of path patterns stated in the Scope of the change specification; a change that states none has a scope that cannot be measured (`not_evaluable`). Changed by DC-139. |
| DC-69 | SPEC-06 | 24.5 | Path patterns: relative to the repository root with `/`; no wildcard names one path; a trailing `/` names a tree; `*` stays inside one segment; a segment `**` matches any number of segments; an empty pattern, a leading `/`, or a segment `..` is invalid. Drafted conservatively; flagged as F1. |
| DC-70 | SPEC-06 | 24.5 | In `full` the base revision is recorded when the first phase of the change begins. |
| DC-71 | SPEC-06 | 24.5 | The exempt record files are the change definition, the specification, and the state document in `core`, and the specification and the state file or inline record in `full`; every other file in the change directory is measured. Changed by DC-123. |
| DC-72 | SPEC-06 | 24.5 | Before start the scope gate is recorded `not_applicable`; after start a scope that cannot be measured is `not_evaluable`, never `satisfied` and never a violation. Changed by DC-139. |
| DC-73 | SPEC-06 | 24.5 | A change MUST run isolated; an implementation SHOULD warn when it finds other uncommitted work at start and MUST NOT exclude such work from the measurement. |
| DC-74 | SPEC-11 | 24.10 | The designated token is the literal `@interpreter`; the interpreter is never discovered; with no configuration it is the implementation's own interpreter; a warning is advised when it lives inside the repository. |
| DC-75 | SPEC-10 | 24.9 | An evidence command is a check command of 24.2; closure is `close` in `core` and the evaluation of Verify-Done and the completion criteria in `full`. |
| DC-76 | SPEC-10 | 24.9, 24.1 | The requirement identifiers and the evidence commands are fixed with the gate definitions. Changed by DC-125. |
| DC-77 | SPEC-09 | 24.8 | A question id is `Q` plus a decimal number from 1 assigned by the implementation; structured options are pairwise distinct; an empty free-text answer is rejected; an answer does not resume a waiting change. |
| DC-78 | SPEC-09 | 24.8 | In `full` a question is recorded in the state file or inline record; an unanswered question makes a Definition of Wait condition active, so `complete` and `resume` answer `blocked`. |
| DC-79 | SPEC-09 | 24.8 | The issue code `open-questions` is named in the text. |
| DC-116 | SPEC-05 | 23.4, 24.4 | The entry of `new` creates the anchor at position 1 where one is kept or required; this is not a replacement. `adopt` serves a history with entries and no anchor. AE-278; AE-140 stays. |
| DC-125 | SPEC-10, SPEC-01, SPEC-14 | 24 intro, 16.1, 16.4, 24.9 | The fourth member of the parsed gate definitions of `full` is `requirements` with `id` and `evidence_commands`; the home of a command is a list item under `#### Evidence Commands` of the requirement; the hashed value of a command is the text of its item (marker removed, white-space runs collapsed). The form of the text is not fixed beyond "argument list, exit map, optional time limit", so two spellings of the same command are two values. AE-286. |

### Theme: State, hashing and schema versions

Rule: the first requirement id in the Block cell is SPEC-15 or SPEC-18.

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-14 | SPEC-15 | 25.1 | Canonical form restricted to strings, integers, booleans, null, arrays, and objects with string keys; keys in code point order; no whitespace; UTF-8 without BOM and final line feed; no ASCII escaping; `sha256:` prefix with 64 lowercase digits. No floating point. |
| DC-15 | SPEC-18 | 25.3 | An artifact is a machine-readable, schema-governed file (project configuration, integration mappings, change definition, state document). Markdown is out. A migration appends and never rewrites. |
| DC-16 | SPEC-15 | 25.2 | Text files normalize line endings, binary files are byte-exact; the classification rule is left to the implementation with a SHOULD default (valid UTF-8 and no zero byte). |
| DC-81 | SPEC-15 | 25.1 | All ten body fields are always present and a field that does not apply is `null`; `at` is a UTC string `YYYY-MM-DDThh:mm:ssZ`; `result` is `success` or `blocked`; a rejected or failed action writes no entry. Changed by DC-128 and DC-129. |
| DC-82 | SPEC-15 | 25.1 | The `after` record is the whole state and holds `schema_version`; the field is `base_revision`; in `full` it holds `phase` and `status` in place of `state` and `outcome`. Changed by DC-128. |
| DC-83 | SPEC-15 | 25.1 | Integers are decimal, without fraction or exponent, with a magnitude not above 2 to the power 53 minus 1; a string holds no surrogate code point; a value outside the domain ends with `error` and writes nothing. |
| DC-84 | SPEC-15 | 25.1 | The expected version is the number of entries read; the writer locks, compares under the lock, and on a difference answers `error` with `state-conflict`; atomic replacement through a temporary file in the same directory. Changed by DC-123 and DC-124. |
| DC-85 | SPEC-15 | 25.2 | A parsed YAML definition is read as YAML 1.2 with the core schema, aliases expanded; a float, a timestamp, a non-string key, a repeated key, or an integer above the bound has no content hash. Changed by DC-131. |
| DC-86 | SPEC-15 | 25.2 | The content hash of a file set is the hash of the canonical form of an object from path to file hash; the hash of gate definitions together with a gate identifier uses the members `definitions` and `gate`. |
| DC-87 | SPEC-18 | 25.3 | The version is a string of two integers joined by a dot, compared one integer at a time; a number is not a version. |
| DC-88 | SPEC-18 | 25.3 | Three stable issue codes: `migration-required`, `schema-version-unsupported`, `schema-version-mismatch`; every operation that uses the file is refused, read-only ones included; only `migrate` accepts a migratable version. |
| DC-89 | SPEC-18 | 25.3 | `migrate` applies steps in ascending order, one entry per step, all or nothing; it is a contract operation, legal from every state, and changes neither state nor outcome. |
| DC-90 | SPEC-18 | 25.3 | The migration entry adds `source_version`, `target_version`, and `source_hash`. |
| DC-91 | SPEC-18 | 25.3 | The document version must equal `after.schema_version` of the last entry; a difference makes the history not consistent and is refused with `schema-version-mismatch`. Changed by DC-126. |
| DC-92 | SPEC-18 | 25.3 | A project-level artifact is migrated inside a change that is not `closed`; a migration of a change definition that alters the parsed gate definitions needs a new human approval. |
| DC-93 | SPEC-18 | 25.3 | An old `state.yaml` is converted by `migrate` to `state.json` whose first entry is a `migrate` entry; the old file is not changed, deleted, or read afterwards; the hash chain restarts at that entry (an anchor makes the restart detectable). |
| DC-95 | SPEC-15 | 25.1 | The text carries two real SHA-256 test vectors (AE-183, AE-184); they are not development identifiers. |
| DC-121 | SPEC-15, SPEC-02 | 24.2, 25.1 | `gate_results` values are the three results in exact lowercase or the marker `not_applicable`; `gate_detail` is text for a gate that has a value in `gate_results`; the rejection rule of 24.2 applies to a record of a result. AE-61 stays. AE-281. |
| DC-123 | SPEC-15, SPEC-06 | 24.5, 25.1 | The scope exemption is two fixed names, `state.json.tmp` and `state.json.lock`, in the change directory, in both method profiles. Any other name, including `state.json.bak`, is measured. A leftover is never state, is ignored, and MAY be removed. Keeping the artifacts outside the working tree was not taken because it conflicts with the same-directory rename. AE-282. |
| DC-124 | SPEC-15 | 25.1 | The lock is a separate lock object held across compare and replace, taken also when no state document exists; it is a lock that the system releases when its holder ends, so a leftover file is not a held lock. It covers the creation and every operation that appends an entry. A reader does not take it. AE-283. |
| DC-126 | SPEC-18 | 25.3 | For a state document the comparison with the latest recorded version is made first; a lowered version that is migratable is still `schema-version-mismatch`. AE-211. |
| DC-127 | SPEC-15 | 4.3, 25.1 | The history-dependent list is extended (24.2 retry counts, 24.5 base revision, 24.7 overrides and attempts) and no inline-record fallback is defined; an inline-record `full` change does not get these rules enforced and the report must not claim them. AE-195. |
| DC-128 | SPEC-15 | 25.1, 23.2 | `reason` is in the `after` record of both method profiles (`status` for `full`); for a hard failure it is generated from the failing gates and their detail. AE-284. |
| DC-129 | SPEC-15 | 25.1 | `action` is the operation name from a closed set shared by both method profiles. AE-285. |
| DC-131 | SPEC-15, SPEC-04, SPEC-18, SPEC-12 | 4.3, 24.3, 24.5, 24.10, 25.2 | AE-154 states a state taken over from an older document; AE-161 is worded as a recommendation; ", a timestamp" is deleted from 25.2; 4.3 limits the conditional-files sentence to `full`; the statement clause names the history the action extends; AE-198 uses files that each hold the byte 00. |

### Theme: Resolution layers and the full revision

Rule: the first requirement id in the Block cell is SPEC-14 or SPEC-16.

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-06 | SPEC-14 | 24 intro | The frozen set of a `full` change is the change specification with its Flow Gates, its allowed path list, and the project-wide definitions in effect at the approval, identified by content hash (completed by DC-101). |
| DC-10 | SPEC-14 | examples | Examples for the rules of both profiles; ids unique and cited, consecutive, not necessarily in document order. Plan 05 adds one example per rule unit (DC-104). |
| DC-99 | SPEC-16 | 5.3, 3.8 | A `core` change implements layers 1, 2, 3, and 5. Layer 4 (change-class requirements, the size classes of 6) and layer 6 (integration mappings, 3.8 and 17) are not applicable to `core` and are specified for `full` and combination use. No seventh layer; layers are never renumbered. Changed by DC-134. |
| DC-100 | SPEC-16 | 5.3 | For a `full` change the no-weakening check compares the Flow Gates with the project-wide definitions of 4.2; an entry that removes or relaxes a condition is a weakening unless the approved exception covers it. |
| DC-101 | SPEC-14 | 24 intro | The definitions fixed in `full` are the Flow Gates, the allowed path list, and the project-wide definitions under `docs/definitions/` in effect at the approval. The parsed value is an object with `flow_gates` (lists `ready`, `done`, `wait`, `fail` of condition texts in written order; the text of a condition is the list item without its marker, white space runs replaced by one space; the marker `<optional>` is not a condition; a heading without items gives an empty list), `scope` (the allowed path list), and `definitions` (the content hash of the file set under `docs/definitions/`). A change of a project-wide definition after the approval makes the gate definitions differ from the approved ones. This completes the item that plan 04 handed over. Changed by DC-125. |
| DC-102 | SPEC-14 | 16.1 | The 16.1 template gains the heading `### Allowed Paths` with the line `- <path pattern>` in the Scope, and one paragraph says that this list is the allowed path list and that Included and Excluded describe the scope in words and are not measured. Changed by DC-139. |
| DC-103 | SPEC-14 | 24 intro | The realization table has 11 rows (24.1 to 24.10 and the result `blocked`) with the columns Protection, Section, In `core`, In `full`. The `full` cells are argued from the generic wording of the `full` flow (Flow Gates, DoR, DoD, DoW, DoF, wait categories, state file or inline record) and have no prototype evidence. |
| DC-105 | SPEC-16 | 23.4 | A stray comma before "An `answer`" in the paragraph after the 23.4 table (text of plan 02) became a full stop. This is the only edit of an existing line outside 5.3 in this plan; it changes no rule. |
| DC-107 | SPEC-14 | 24 intro | The 11 realization examples sit after the realization table in the section 24 intro, not at the end of each subsection 24.k, and are cited from one paragraph there. |
| DC-140 | SPEC-16, SPEC-04 | 5.3, 5.4 | IN-01: a lower statement of an assurance level is neutralized (accepted, no effect), not rejected; AE-221. IN-12: a weakening in a `full` change is rejected with the result `rejected`, `changed` false and the issue code `gate-weakened`; AE-227. IN-02: the A0 paragraph of 5.4 has AE-293; four other rules get no example in this phase and are recorded. IN-08, IN-11 and IN-14 are recorded and no text is changed for them (see "Recorded findings"). |

### Theme: Text-wide choices and the header

Rule: the Block cell reads all or header.

| ID | Block | Section | Reading taken |
|---|---|---|---|
| DC-01 | all | 1.1 | No renumbering. Sections 5.6, 23, 24, and 25 are added; map rows 23 and 24 are in the category Method Semantics and row 25 in Reference-Implementation Requirements. |
| DC-20 | header | header | Version and Revision are edited in the last commit that touches the text, with a subject that names no requirement id (see "Commit structure"). |

### Research questions OQ-1 to OQ-7 and how the draft answers them

These seven questions were open in the research that preceded the draft; each row is the register row that states how the draft answers it.

| ID | Question | Disposition in the draft |
|---|---|---|
| OQ-1 | Assurance floors and base gates per compliance profile | The draft assigns none (DC-11). Base gates belong to the method profile (DC-12, DC-96). The example of 24.3 shows that a compliance profile alone sets no minimum level. |
| OQ-2 | May an approved exception weaken a higher layer | The draft is absolute (DC-13, DC-97). The one exception left is the exception of 4.2, limited to the local specification of a `full` change (DC-98). |
| OQ-3 | Granularity of "each `full` rule has an acceptance example" | Settled by the owner's granularity rule: the rule unit; 41 units here (DC-104). |
| OQ-4 | `state.json` for `full` | Drafting choice DC-07: always for `core`; `full` keeps the optional-state allowance, with mechanical enforcement only where a state document exists. |
| OQ-5 | Cite the decision record in the text | The text cites none; check X1 passes (DC-17). |
| OQ-6 | `core` `supersede` | Closes as `cancelled` with `replaced_by` (DC-02). |
| OQ-7 | Items no requirement owns: exit codes and the text-versus-binary rule | Exit codes: no requirement owns them and none were added; handed to the engine phases with the list of stable issue codes. The text-versus-binary rule: 25.2 states the constraint (depends on the bytes only) and a SHOULD default; the concrete rule goes to the engine phases. |

Your answer at Q11 (all 141 drafting choices as drafted, or the ids you overrule):

- Owner answer: unanswered (the answer is recorded only in the owner approval record)

## Dispositions of the review findings

The advisory review of the proposed text found 3 critical findings (CR), 27 warnings (WR) and 14 information items (IN). Every finding has one row. FIXED means that the text was changed so that the finding no longer applies. FIXED-CONSERVATIVE means that the text was changed with the most conservative reading and that a question for the owner remains (OQ-8 to OQ-15). RECORDED means that no text was changed and the item is kept for the Phase 3 packet; no CR or WR finding is RECORDED. Counts: 30 FIXED, 10 FIXED-CONSERVATIVE, 0 DEFERRED-TO-OWNER, 4 RECORDED.

| Finding | Disposition | Where | Evidence | DC |
|---|---|---|---|---|
| CR-01 | FIXED-CONSERVATIVE | 23.3 | AE-272 | DC-111 |
| CR-02 | FIXED | 24.5, 25.1 | AE-282 | DC-123 |
| CR-03 | FIXED | 24 intro, 16.1, 16.4, 24.9 | AE-286 | DC-125 |
| WR-01 | FIXED | 24.7, 24.2, 23.4, 8.3 | AE-279 | DC-118 |
| WR-02 | FIXED | 8.3 | AE-121, AE-122 | DC-119 |
| WR-03 | FIXED | 5.6 | AE-52 | DC-108 |
| WR-04 | FIXED | 19, 20 | AE-270 | DC-109 |
| WR-05 | FIXED | 5.6, 23.3 | AE-271 | DC-110 |
| WR-06 | FIXED-CONSERVATIVE | 23.3, 23.7, 24.2 | AE-273, AE-222, AE-223 | DC-112 |
| WR-07 | FIXED-CONSERVATIVE | 24.2, 8.5, 23.6 | AE-280 | DC-120 |
| WR-08 | FIXED | 23.4 | AE-274 | DC-113 |
| WR-09 | FIXED | 23.4, 23.5, 24.8 | AE-275 | DC-114 |
| WR-10 | FIXED | 23.7, 24.3 | AE-276 | DC-115 |
| WR-11 | FIXED | 23.4, 24.4 | AE-278 | DC-116 |
| WR-12 | FIXED | 25.3 | AE-211 | DC-126 |
| WR-13 | FIXED | 24.2, 25.1 | AE-281 | DC-121 |
| WR-14 | FIXED | 25.1 | AE-283 | DC-124 |
| WR-15 | FIXED | 4.3, 25.1 | AE-195 | DC-127 |
| WR-16 | FIXED | 25.1, 23.2 | AE-284 | DC-128 |
| WR-17 | FIXED | 25.1 | AE-285 | DC-129 |
| WR-18 | FIXED-CONSERVATIVE | 5.3, 17 | AE-290, AE-226 | DC-134 |
| WR-19 | FIXED-CONSERVATIVE | 5.6, 23.1 | AE-291 | DC-135 |
| WR-20 | FIXED-CONSERVATIVE | 5.4 | AE-292 | DC-136 |
| WR-21 | FIXED-CONSERVATIVE | 5.4 | AE-293 | DC-137 |
| WR-22 | FIXED | 22.1, 22.3 | AE-287 | DC-132 |
| WR-23 | FIXED | 4.3, 23.1, 23.4, 16.1 | AE-288 | DC-133 |
| WR-24 | FIXED-CONSERVATIVE | 24.3, 24.10, 25.1 | AE-289, AE-159 | DC-130 |
| WR-25 | FIXED-CONSERVATIVE | 9.4 | AE-263 | DC-138 |
| WR-26 | FIXED-CONSERVATIVE | 6.1, 9.6, 24.5 | AE-294, AE-253 | DC-139 |
| WR-27 | FIXED | 25.2 | AE-198 | DC-131 |
| IN-01 | FIXED | 5.3 | AE-221 | DC-140 |
| IN-02 | RECORDED | 5.4, 25.1, 25.3, 23.5, 24.3 | AE-293 for the A0 paragraph; none for the four other sites | DC-140 |
| IN-03 | FIXED | 24.5, 24.7 | AE-154, AE-102 | DC-122, DC-131 |
| IN-04 | FIXED | 24.10 | AE-161 | DC-131 |
| IN-05 | FIXED | 25.2 | wording, no behavioral rule | DC-131 |
| IN-06 | FIXED | 12.1 | wording, no behavioral rule | DC-122 |
| IN-07 | FIXED | 4.3, 23.1 | wording, no behavioral rule | DC-131 |
| IN-08 | RECORDED | 4.2, 16.4, 5.3 | none; AE-227 is unchanged in this respect | DC-140 |
| IN-09 | FIXED | 11.2 | AE-268 | DC-122 |
| IN-10 | FIXED | 24.3 | AE-129 | DC-131 |
| IN-11 | RECORDED | 4.2, 23.1 | none | DC-140 |
| IN-12 | FIXED | 5.3 | AE-227 | DC-140 |
| IN-13 | FIXED | 23.5 | AE-277 | DC-117 |
| IN-14 | RECORDED | 24.9, 3.7, 5.2 | none | DC-140 |

## Recorded findings and flagged items

### Recorded findings

- IN-02: the A0 paragraph of 5.4 has an example (AE-293). Four rules still have no example of their own: the refusal of `migrate` for a file that already has the target version and the failing step that discards the earlier steps (25.3), the duplicate-key rule of the state document (25.1; AE-188 covers the layout only), the `expires` field and the overdue wait of 23.5, and the refusal of an unprotected key (24.3; AE-134 shows the risk only). The alternative acceptance condition that 3.9 allows was not written for them.
- IN-08: the exception of 4.2 is recorded in the Deviations of the evidence of the change (16.4), a conditional document that is normally written late, while the check of 5.3 runs when the change is created and again before the gate definitions are approved. An earlier home (a section of `spec.md` that is part of the hashed gate definitions) was not added.
- IN-11: 4.2 says that local specifications MUST NOT weaken the project-wide definitions and that a `core` change has no exception, but the text does not state whether the files under `docs/definitions/` bind a `core` change.
- IN-14: 24.9 requires an executable command for every requirement in both method profiles, while 3.7 and 5.2 let tailoring change the depth of evidence; the text does not say how a requirement that cannot be run (a visual or process requirement) is dispositioned.

### Flagged items F1 to F7

| Flag | Item | Requirement | Note |
|---|---|---|---|
| F1 | E18 encoding | 06 (scope) | Path case and normalization are platform dependent. The text compares paths as code point sequences without normalization and letter case matters (24, 24.5); on a file system that folds case or normalizes names, a changed path can match differently. The path pattern syntax (DC-69) is drafted, not exercised. |
| F2 | E36 precision | 12 (profiles) | The profile identifiers carry no quantity beyond counts, so no precision rule applies. |
| F3 | E42 adjacency | 14 (`full` revision) | Recorded as flagged in the accounting of plan 05; no rule or example was authored for it. |
| F4 | E44 ordering | 14 (`full` revision) | No defensible document criterion for an order of the rule units; the examples are not ordered by any criterion except the document order of their rules. |
| F5 | E45 | 15 | Unclassified probe item, flagged. |
| F6 | E46 | 16 | Unclassified probe item, flagged. |
| F7 | E47 | 17 | Unclassified probe item, flagged. |

No text, example or check was written for the flagged items.

Your answer at Q12 (the four recorded findings and the seven flagged items as recorded):

- Owner answer: unanswered (the answer is recorded only in the owner approval record)

## Unproven items (informational, for Phase 4)

Phase 4 examines these items; no answer is asked of you.

- SPEC-14, the `full` realizations: every row of the realization table and the 41 examples (DC-101, DC-103, DC-104). Specified, not implemented.
- SPEC-16, beyond the prototype's no-weakening check: the `full` side of the check (DC-100), the layer set of `core` (DC-99), and the exception of 4.2 (DC-98).
- SPEC-17: proved by absence only (a `core` change has no `reopen`).
- SPEC-18: decision-driven, no prototype evidence; the YAML-to-JSON conversion rule and the migration of a project-level artifact inside a change.
- The "or an equivalent" clause of the anchor rule in 24.4 (nothing exercised an equivalent mechanism).
- The A1 verifier of 24.3 (platform review is not tested directly and cannot serve a participant who works alone).
- The rule that a retry limit is a soft fail condition (reasoning).
- The path pattern syntax (F1 above).
- The condition forms of a `core` fail or wait gate (`command`, `retry_limit`, `predicate`) in 23.3 (DC-112).
- Evaluation by group with the early stop in 24.2, 8.5 and 23.6 (DC-120).
- The `requirements` member of the gate definitions of `full` and the heading `Evidence Commands` as the home of an evidence command (DC-125), and the hashed value of a command as text.
- The identifier syntax of 4.3 (DC-133), in particular reserved device names with an extension and non-ASCII case folding.
- Scope evaluation from the first approval of the gate definitions in `full` (DC-139).

## Hand-off list (informational, for the engine phases)

This phase changes none of these files or values.

- `specs/examples/class-m/state.yaml` (the example state; its `flow.profile` at line 10 is the compliance profile), `.ggsad/templates/*.template.md`, `.ggsad/schemas/state.schema.json`, and the archived CHG-001 state.
- The pinned method version "1.3" in `.ggsad/config.yaml` (line 10), `src/ggsad/application/initialize_project.py` (line 82), and `tests/unit/test_initialize_project.py` (line 61).
- The schema constants "0.1" in `.ggsad/schemas/config.schema.json` (line 20), `.ggsad/schemas/mappings.schema.json` (line 19), and `.ggsad/schemas/state.schema.json` (line 22). The text fixes the form of `schema_version` and the checks, not the version values; the version of the first JSON state document and the first migration step are engine choices.
- Exit codes (no requirement owns them): the mapping of the four results and of the stable issue codes (`gates-changed`, `start-blocked`, `open-questions`, `state-conflict`, `migration-required`, `schema-version-unsupported`, `schema-version-mismatch`, `gate-weakened`) to exit codes.
- The concrete text-versus-binary rule for content hashing (25.2 states the constraint and a SHOULD default only).
- Configuration keys that the text does not name: the minimum assurance levels, the interpreter, the platform account mapping, the signers file location, the anchor location, and the default method profile. Also the spelling of the statement format identifier, the signature scheme, and the storage of the anchor.
- The reference implementation refuses a change that selects `full`; the realizations in the table of the section 24 intro stay specified but not implemented.
- Names and fields that plans 06 to 08 added to the text: the in-progress file `state.json.tmp` and the lock object `state.json.lock` in the change directory (both exempt from the scope measurement); the fields `reason` and `required_level` of the state document; the closed set of `action` names; the condition forms `command`, `retry_limit` and `predicate` of a `core` fail or wait gate; the heading `Evidence Commands` of the change specification template and the members `requirements`, `evidence_commands` and `id` of the gate definitions of `full`; the identifier syntax of 4.3. The stable issue codes are unchanged by plans 06 to 08.

This packet is evidence only. It does not change the reviewed file.
