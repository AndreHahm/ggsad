---
phase: 04-independent-review
plan: 15
subsystem: independent-review-fix-round-4-approval
tags: [independent-review, owner-approval, normative-specification, check-script, round-4]
status: complete

requires: ["04-14"]
provides:
  - "Diff identity note updated in place with the pins of the text of fix round 4 (fca228479a34e228785f4c0b100da3c6745ada0a, 4812 lines) and a pointer to the approval record"
  - "Profile 4 of the approval stages and printers of the fix round check script"
  - "Approval packet of round 4, printed by the script, and the owner approval record of round 4 (outcome approved)"
affects: [04-16 (preparation of the independent review of the approved text), 04-17]

actuals:
  tokens: 60000
  tasks: 3
  commits: 7

tech-stack:
  added: []
  patterns: ["profile variables with round 2 as the default", "packet printed from the live text and the register, equal byte for byte", "record rebuilt from pins and printed questions"]

key-files:
  created:
    - .planning/reviews/2026-10-27-normative-spec-fix-round-4-approval-packet.md
    - .planning/reviews/2026-10-27-normative-spec-fix-round-4-approval-record.md
  modified:
    - .planning/reviews/2026-10-24-normative-spec-diff-identity.md
    - .planning/phases/04-independent-review/04-check-fix-round.sh

key-decisions:
  - "The owner approved the exact text of fix round 4 (fingerprint fca228479a34, 4812 lines), which makes the two choices of plan 04-14 (OD-4 Cancel only, OD-5 Soft, said openly) and the example AE-310 final as part of that text."

requirements-completed: []  # No plan ticks a requirement here. The tick of APPR-01 from the first round is not changed by any plan; the orchestrator alone decides at phase close.

duration: "not measured; the plan spanned an implementation session (task 1), an owner checkpoint run by the orchestrator and a continuation session (task 3)"
completed: 2026-10-28
---

# Phase 4 Plan 15: Approval of the Text of Fix Round 4 Summary

PHASE NOT COMPLETE. The repository owner approved the exact new text of the specification (blob `fca228479a34e228785f4c0b100da3c6745ada0a`, 4812 lines) and the approval is on record with the exact pins. The independent review of this text has not started; plan 04-16 asks the owner which parts it reads. Phase 4 stays open and no requirement is ticked by this plan.

## Outcome

Approved. Record: `.planning/reviews/2026-10-27-normative-spec-fix-round-4-approval-record.md`. Key lines of the record:

- `Owner approval: approved`
- `Owner reply date: 2026-10-28`
- `Reply given by`: AndreHahm
- `Owner reply`: given by the repository owner through the interactive question tool and relayed by the orchestrating session; the name and the date were picks from candidates that the owner explicitly asked to be offered.

## Owner answers (as relayed)

- Statement of channel as the orchestrator gave it: the answers were given by the repository owner through the interactive question tool in the orchestrating session.
- Q01 (Approval), as asked: "Do you approve the new text exactly as it now stands (fingerprint fca228479a34, 4812 lines), or do you want changes? (My recommendation: Approve exact text.)". Answer: `Approve exact text`. The recorded question is the printed one, without the appended sentence (see Deviations).
- Q02 (Changes): not asked, because the text was approved. Recorded as `None. (not asked, because the text was approved)`.
- Q03 (Name): the owner's replies to two free-text asks came back only as the option label `Type it under Other`, so the question was not sent a third time; on the owner's `Offer candidates` the candidates `AndreHahm` and `Do not record a reply` were offered. Answer: `AndreHahm`. A pick from candidates the owner asked for.
- Q04 (Date): same pattern. Candidates `2026-10-28` and `2026-10-27` were offered. Answer: `2026-10-28`. A pick from candidates the owner asked for.
- Before asking, the orchestrator explained the three changes in plain words (OD-4 Cancel only, OD-5 Soft, said openly, and the new example AE-310 with no decision asked), asked the owner to confirm the wording `the earlier text of this method` in the added sentence of Section 12 (the owner approved the text as it stands without asking for a change), and offered to show any change line by line (not requested).
- The two choices of plan 04-14 and the third change were kept: the owner requested no change.

## Accomplishments

- IDN: the diff identity note was updated in place with the pins of the final text (task 1), then pointed at the approval record of round 4 with the statement that the independent review of this text has not taken place (task 3).
- FIX: profile 4 of the stages `approval-pending` and `approval-recorded` and of the four printers; round 2 stays the default and profile 3 behaves as before.
- APK4: printed by the script from the live text and the register; its status line changed once, from pending to recorded in the owner approval record.
- ARC4: created from the printed skeleton and filled with the owner's answers; pins the text, the register and the packet.

## Task Commits

1. Task 1: `416c1b0` docs(04-15): record the diff identity of the text of fix round 4
2. Task 1: `f1b9c97` docs(04-15): add profile 4 of the approval stages and printers to the fix round check script (tracer)
3. Task 1: `f0373b6` docs(04-15): add the owner approval packet of fix round 4
4. Task 2: owner checkpoint run by the orchestrator, no commit
5. Task 3: `5c35a7d` docs(04-15): record the owner approval of fix round 4
6. Task 3: `7ce77f2` docs(04-15): mark the fix round 4 packet as recorded
7. Task 3: `61c7fe8` docs(04-15): point the diff identity note at the approval record of round 4
8. Task 3: this summary, committed as `docs(04-15): summary`.

## Verification

- `bash FIX --round 4 --stage approval-recorded` ends `RESULT: PASS` (AR1 to AR5), exit 0, before and after the packet and identity commits. `bash FIX --round 4 --stage approval-pending` ends `RESULT: PASS` after the record exists (AP2 and AP5 accept the recorded status line). `bash FIX --round 4 --stage edits --complete` and `bash CHK2 --final` end `RESULT: PASS`.
- Replays with the current scripts: `bash FIX --replay-round-3 --with-current-scripts` ends `PASS R3-8` and `RESULT: PASS`; `--replay-round-2` ends `PASS R2-8` and `RESULT: PASS`; `--replay-round-1` ends `PASS FR5` and `RESULT: PASS`.
- Seeded cases re-run by this executor against copies of the record (each exited 1 with the named id): Q01 answered `Maybe` printed `FAIL AR4`; the date 2026-10-26 printed `FAIL AR5`; the date 2026-02-30 printed `FAIL AR5`; one word of the Q04 question changed printed `FAIL AR3`. The other seeded cases of task 1 (AP1, AP2, AP4, AR1, AR2, the second AR4 case, the fixtures for both outcomes) were run by the executor of task 1 and were not repeated here.
- The blob of the specification is `fca228479a34e228785f4c0b100da3c6745ada0a`, equal to the Result blob of the record and unchanged by this plan; 52 commits touch it since `origin/main`.
- `git diff --name-only origin/main...HEAD` outside `.planning/` lists only the specification; nothing under `src`, `.ggsad`, `specs`, `tests`, `AGENTS.md` or `CLAUDE.md` differs. `grep -c '^- \[x\] \*\*REVIEW-0' .planning/REQUIREMENTS.md` prints 0.
- Python baseline: not run, because only .planning/ changed in this plan.

## Dispatch

Dispatch: sequential executors on the main working tree (workflow.use_worktrees is false)

## Deviations from Plan

**1. [Process] Recommendation printed in the owner question.** At the owner's standing request, the orchestrator included "(My recommendation: Approve exact text.)" in the text of Q01, and said it before asking. The recommendation was the orchestrator's judgment of process only (the mechanical checks pass), not a reading of the specification's meaning, and the owner chose. The labels and descriptions were printed exactly as the script prints them. The plan says that no option is recommended. The recorded question is the printed one, so check AR3 holds; this deviation is stated here so that the approval can be weighed accordingly.

**2. [Observation] Acceptance criterion on REQUIREMENTS.md.** The plan expects `git diff --name-only origin/main...HEAD -- .planning/REQUIREMENTS.md` to print nothing. It prints the file, because earlier phases changed it on this branch (the ticks of SPEC-12 and APPR-01 in commits `d806ee8` and `251ace4`). No commit of this plan touches it (`git diff --name-only 416c1b0~1 HEAD` lists four files, none of them the requirements file), and no REVIEW-0x item is ticked.

## Known Stubs

None.

## Unverified

- The owner's answers reached this executor through the orchestrator's message and cannot be independently checked from the repository. The record states the channel; the checks prove completeness, consistency and the tie to the pinned text, not who answered.
- The name and the date were picks from candidates that the orchestrator offered at the owner's request; the owner's own typed reply never reached the record.
- The checks prove structure and consistency, not that the text is right. The text has not been independently reviewed.
- Requirement honesty: APPR-01 was ticked for the first text. The tick is not changed by any plan; it rests, for this text, on the new record. The orchestrator alone decides at phase close whether it stands.

## Next step

`/gsd-execute-phase 4 --gaps-only` for plan 04-16: the owner decides which parts of the approved text the independent review reads and consents to the exact run. Nothing is sent before that.
