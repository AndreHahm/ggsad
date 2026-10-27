# Fix register, round 3: what changed in the specification and why

This register lists the three changes made to the specification to fix the three BLOCKING findings of the second independent review that the owner dispositioned fix. Each change implements the way the owner chose, which is recorded in the entry together with the options that were offered. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.

## The three changes

| Change | Title | Findings | Kind | Status | Sections | Examples |
|---|---|---|---|---|---|---|
| FG-10 | How the guard check treats an equivalent to the history anchor | RR-B-001 | owner decision | drafted | 22.4 | AE-306 |
| FG-11 | How the scope check treats ignore settings | RR-X-001 | owner decision | drafted | 24.5, 24.10 | AE-307 |
| FG-12 | When the fail action is allowed in the full profile | RR-X-002 | owner decision | drafted | 8.3, 24.7 | AE-308 |

## Change details

### FG-10 — How the guard check treats an equivalent to the history anchor

- What changed: The guard check now passes a history that has an anchor or an equivalent mechanism, as the history rules already allow. It reports a missing anchor only when the history has neither.
- Why: The guard asked for an anchor in so many words, so a change that correctly used an equivalent mechanism would have failed it.
- Options: Accept an equivalent | Anchor only, said openly
- Owner decision: Accept an equivalent
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: "where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor."
- After: "where the applicable configuration requires approvals at the level A2 (Section 24.3), it has an anchor or an equivalent mechanism (Section 24.4)."
- Notes: Section 22.4 only: the first verification, the sentence that names the stable issue codes, and the See sentence. The name of the issue code `anchor-missing` is kept, so that reports stay stable; the sentence now says that it is reported when the history has neither an anchor nor an equivalent mechanism. The example AE-306 is placed after AE-305 and cited in the See sentence of Section 22.4. Stale statements found by the sweep:
  - Section 24.4, the sentence that requires an anchor or an equivalent mechanism and the description of an equivalent mechanism: stays true, because it is the rule the guard now follows.
  - the example AE-142 (an equivalent mechanism meets the requirement for an anchor): stays true; AE-306 shows the same for the guard.
  - the `new` row and the `adopt` rows of Section 23.4 and Section 8.3: stay true; this fix does not speak of `adopt`.
  - the examples AE-303 to AE-305 and the other four verifications of Section 22.4: stay true.

### FG-11 — How the scope check treats ignore settings

- What changed: The scope check now counts only ignore files that lie inside the repository. They are ordinary files, so creating or changing one is a changed path that needs an allowed path, and ignore settings kept elsewhere are not applied.
- Why: Ignore settings kept outside the measured files could hide any out-of-scope work, because changing them left no changed path to count.
- Options: Repository files only | Detect any change | Measure every file | Say it openly
- Owner decision: Repository files only
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: "A file that version control is told to ignore is invisible to the measurement."
- After: "Only ignore files inside the repository count. An ignore file is an ordinary file of the working tree, such as a `.gitignore` file, so that creating or changing one is a changed path, and it is a scope violation when no pattern of the allowed path list matches it."
- Notes: Section 24.5: the sentence on the files that version control does not track (it now says that no ignore file inside the repository tells it to ignore them) and the paragraph on ignored files (extended with the rule on ignore files inside the repository and the sentence on ignore settings kept elsewhere, and the See sentence). Section 24.10: one phrase of the last paragraph. The example AE-307 is placed after AE-150 and cited in the paragraph on ignored files of Section 24.5. The examples AE-150 and AE-162 are corrected: each now says that the ignore file is inside the repository and in place at the base revision, because an ignore file that the change itself creates is a changed path. Point for the owner to confirm in the approval: the option says that ignore settings kept elsewhere are not applied; the exclude file in the metadata directory of version control is not an ordinary file of the working tree and cannot appear as a changed path, so the text counts it among the settings kept elsewhere, which follows from the reason that the option gives. Stale statements found by the sweep:
  - Section 24.5, the paragraph on the changed paths: updated.
  - Section 24.5, the paragraph on ignored files: updated.
  - Section 24.10, the last paragraph: updated; the rest of it stays true.
  - the examples AE-150 and AE-162: updated.
  - the example AE-149 (an untracked file that is not ignored): stays true.
  - the example AE-152 and the paragraph on isolation in Section 24.5: stay true.
  - the sentences on the temporary file and the lock object in Sections 24.5 and 25.1: stay true; they speak of the writer of the state document and not of ignore files.

### FG-12 — When the fail action is allowed in the full profile

- What changed: In the full profile, the fail action is now allowed only while a soft failure waits for a human. With only a hard failure active it is refused, and the change keeps its state.
- Why: One table said that fail is allowed whenever a failure condition is active, while the section on hard and soft failure said it is for a soft failure only.
- Options: Soft failures only | Any active failure
- Owner decision: Soft failures only
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: "A DoF condition is active."
- After: "A soft failure awaits disposition: the status is `waiting` with a wait state of the category `WAIT_DECISION` for a DoF condition of the severity `soft` that is active (Section 24.7)."
- Notes: Section 8.3: the Precondition cell of the `fail` row of the transition table, the rejected cell of the `fail` row of the table of results, and the last See sentence. Section 24.7: the paragraph on hard failure now names `fail` as a second exception next to `start` (otherwise its words, that an action which finds a hard failure closes the change as failed, would read as applying to a refused `fail`), and the See sentence of the `fail` sentence cites AE-308; the `fail` sentence itself is not edited. The example AE-243 is corrected: it said that `fail` is allowed whenever a Definition of Fail condition is active, and now shows a soft failure that waits. The example AE-308 is placed after AE-243 and cited in the last See sentence of Section 8.3 and in the See sentence of Section 24.7. The profile `core` is not edited: its `fail` row already restricts the action to a wait record of kind `fail-gate`. Stale statements found by the sweep:
  - the transition table of Section 8.3, the `fail` row: updated; the cells Legal From and Gate Order stay true.
  - the table of results of Section 8.3, the `fail` row: updated.
  - Section 8.4, the sentence that a soft fail condition waits for a human who closes the change with `fail`: stays true.
  - Section 24.7, the sentence `fail` is valid only while a soft failure awaits disposition: stays true.
  - Section 24.2, the paragraph on the actions that never answer blocked (`fail` is rejected with `gate-not-evaluable`): stays true.
  - the `fail` row of Section 23.4 and the examples AE-98 to AE-101: stay true.

## Normative lines removed or reworded

- A hard failure ends the change as failed without any human a :: the paragraph now names `fail` as a second exception, as the owner chose that `fail` is refused when only a hard failure is active

## Findings whose quoted sentence an edit touched

None.

## Findings not touched

- RR-A-001 (MAJOR): open information; no edit
- RR-A-002 (MAJOR): open information; no edit
- RR-A-003 (MINOR): open information; no edit
- RR-B-002 (MAJOR): open information; no edit
- RR-B-003 (MAJOR): open information; no edit
- RR-X-003 (MAJOR): open information; no edit
- RR-X-004 (MINOR): open information; no edit
- RR-X-005 (MINOR): open information; no edit
- RR-X-006 (MINOR): open information; no edit

## Header

The header of the specification (the Version line and the Revision line) is unchanged by this round.
