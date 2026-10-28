# Fix register, round 5: what changed in the specification and why

This register lists the changes made to the specification to fix the BLOCKING finding of the fourth independent review that the owner dispositioned fix, and the related findings that the owner dispositioned fix in the disposition addendum of round 4. For a change of the kind owner decision the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For a change of the kind repair the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.

## The changes

| Change | Title | Findings | Kind | Status | Sections | Examples |
|---|---|---|---|---|---|---|
| FG-16 | Rules of the full-only templates that have no acceptance example | RF-X-001, RF-B-004 | owner decision | drafted | 16.1, 16.4 | AE-311, AE-312 |
| FG-17 | Rules on ADR conflicts, drift and breaking changes that have no acceptance example | RF-X-002 | owner decision | drafted | 13.1, 13.2, 13.3 | AE-313, AE-314, AE-315 |
| FG-18 | Rules on the review cycle and its artifacts that have no acceptance example | RF-X-003 | owner decision | drafted | 14.3, 14.4, 14.5 | AE-316, AE-317, AE-318 |
| FG-19 | Prohibitions on an AI agent that have no acceptance example | RF-X-004 | owner decision | drafted | 19.1 | AE-319 |
| FG-20 | How the evaluation of a core change stops | RF-C-001 | repair | drafted | 23.6 | - |
| FG-21 | A retry limit that names a check gate which does not exist | RF-C-002 | repair | drafted | 23.3 | AE-320 |
| FG-22 | A sentence that cites the earlier text of the method | RF-B-001 | repair | drafted | 12 | - |

## Change details

### FG-16 — Rules of the full-only templates that have no acceptance example

- What changed: Two new examples show the rules of the minimum templates: how a change specification states its gate conditions, allowed paths and evidence commands, and how the evidence lists a gate that could not be evaluated. The plan and tasks templates hold no rule sentence and got none.
- Why: The owner dispositioned the finding fix and chose to add examples for the rules of these templates, which had none.
- Options: Add examples | Say none needed
- Owner decision: Add examples
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: none (new text)
- After: "the other three lists are empty because the marker `<optional>` is not a condition, the allowed path list is `lib/**`"
- Notes: Sections 16.1 and 16.4 and the examples AE-311 and AE-312. The finding RF-B-004 shares this decision with RF-X-001. Sections 16.2 and 16.3 hold only a template and no rule sentence (no MUST, MUST NOT or SHOULD), so they got no example. Each example is cited by a See sentence appended to the paragraph on the allowed path list (16.1) and to the two paragraphs after the evidence template (16.4). The sweep for stale statements found none:
  - Section 16.1, the sentence that the Flow Gates conditions and the scope are the gate definitions of the change, and the sentence on the requirement identifiers and the evidence command lists: stay true and are not edited.
  - Section 16.1, the sentences on the Change ID, the Open Questions and the Included and Excluded lists: stay true.
  - Section 16.2 and Section 16.3: stay as they are; no example was added.
  - Section 16.4, the sentences on the final gate evaluation and on the Evidence column: stay true; only a See sentence was appended to each.
  - Section 5.6, the table row that marks Sections 16.1 to 16.4 as full only, and the sentence on the profiles of the sections: stay true; the new examples carry the prefix Full.
  - Section 24.1, the paragraph on the gate definitions of a full change and the examples AE-249 to AE-259: stay true.
  - Section 24.2, the paragraph on a gate that cannot be evaluated: stays true.
  - Section 24.9, the paragraph on evidence commands: stays true.

### FG-17 — Rules on ADR conflicts, drift and breaking changes that have no acceptance example

- What changed: Three new examples show the rules on a conflict with an accepted ADR, on a deviation of the implementation or the tests from the specification, and on breaking changes. Each rule now points to its example.
- Why: The owner dispositioned the finding fix and chose to add examples for these rules, which had none.
- Options: Add examples | Say none needed
- Owner decision: Add examples
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: none (new text)
- After: "stops planning or implementation, returns R2 to the requestor, and requests a decision"
- Notes: Sections 13.1, 13.2 and 13.3 and the examples AE-313, AE-314 and AE-315. Each example is cited by a See sentence: appended to the paragraph on changing an ADR (13.1), as a line after the list of actions (13.2) and appended to the paragraph on breaking changes (13.3). The example of Section 13.2 shows two of the four listed actions. The sweep for stale statements found none:
  - Section 13.1, the numbered duties on an ADR conflict and the sentence that accepted ADRs take precedence: stay true.
  - Section 13.2, the list of the four actions: stays true.
  - Section 12.1, the category of an unauthorized breaking change, and Section 12.2, the template F-01: stay true; the example AE-315 refers to the template.
  - Section 19.1, the prohibition on breaking changes without approval, and Section 19, the algorithm step on conflict, uncertainty or missing approval: stay true.
  - Section 20, the criteria for a completed change: stays true.
  - Section 5.6, the table of the profiles: stays true; Section 13 applies to both method profiles and the examples carry no prefix.

### FG-18 — Rules on the review cycle and its artifacts that have no acceptance example

- What changed: Three new examples show the rules on a review cycle that returns a blocking finding, on a blocking finding that blocks a gate until it is dispositioned, and on the evidence record of a review. Each rule now points to its example.
- Why: The owner dispositioned the finding fix and chose to add examples for these rules, which had none.
- Options: Add examples | Say none needed
- Owner decision: Add examples
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: none (new text)
- After: "the finding is returned to the Requestor, the disposition of the Requestor and the changes made are recorded"
- Notes: Sections 14.3, 14.4 and 14.5 and the examples AE-316, AE-317 and AE-318. Each example is cited by a See sentence: as a line after the list of the review cycle (14.3), appended to the paragraph on unresolved blocking findings (14.4) and appended to the paragraph on the eight fields of the evidence record (14.5). The sweep for stale statements found none:
  - Section 14.3, the numbered duties of a review cycle: stay true.
  - Section 14.4, the list of the fields of a finding and the recommended severities and statuses: stay true.
  - Section 14.5, the sentences on inline and separate evidence and on findings that are not requirements: stay true.
  - Section 14.2, the independence rule: stays true.
  - Section 20, the criterion that required Pair Review cycles are complete and blocking findings are resolved or formally dispositioned: stays true.
  - Sections 16.1 and 16.4, the Pair Review parts of the templates: stay true.
  - Section 5.6, the table of the profiles: stays true; Section 14 applies to both method profiles and the examples carry no prefix.

### FG-19 — Prohibitions on an AI agent that have no acceptance example

- What changed: One new example shows the prohibitions on an AI agent together: an agent that meets a gap does not invent, assume or speculate, does not hide an error, and does not work beyond the approved scope. The list now points to it.
- Why: The owner dispositioned the finding fix and chose to add an example for these prohibitions, which had none.
- Options: Add examples | Say none needed
- Owner decision: Add examples
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: none (new text)
- After: "does not read the missing answer as consent, does not silently modify the approved specification"
- Notes: Section 19.1 and the example AE-319. The example shows all eight prohibitions of the list and is cited by a See sentence on a line after the list. The sweep for stale statements found none:
  - Section 19.1, the eight prohibitions: stay true and are not edited.
  - Section 19, the algorithm steps (scope, wait on conflict or missing approval, final drift and evidence check) and the example AE-270: stay true.
  - Section 20, the criteria for a completed change: stays true.
  - Section 13.3, the rule on breaking changes: stays true.

### FG-20 — How the evaluation of a core change stops

- What changed: The first sentence of the evaluation order now says that the evaluation stops once the results of a group decide the requested action, which is what the later sentences on groups already said.
- Why: The reviewer says the two stop rules of the section read differently, and the owner dispositioned the finding fix.
- Options: none: no design choice was open, because the finding names the fix itself.
- Owner decision: none: no design choice was open, because the finding names the fix itself.
- Owner reason: none: no design choice was open, because the finding names the fix itself.
- Channel: none: no design choice was open, because the finding names the fix itself.
- Before: "and the evaluation MUST stop as soon as a gate decides the requested action:"
- After: "and the evaluation MUST stop once the results of a group decide the requested action (Section 24.2):"
- Notes: Section 23.6 only, the first sentence, and no example is added; the existing examples AE-53 to AE-55 already show the order. No design choice was open: the finding names the fix itself. The sweep for stale statements found none:
  - Section 23.6, the sentence after the list that the gates are evaluated by group, that a group is evaluated whole and that the evaluation stops after the first group that decides: stays true and is not edited.
  - Section 23.6, the numbered steps 1 to 5 and the examples AE-53 to AE-55: stay true.
  - Section 24.2, the paragraph on the evaluation by group: stays true; the first sentence now agrees with it.
  - Section 8.5, the sentence that the evaluation of a full change stops as soon as a gate determines the outcome: stays as it is; it belongs to the full profile, is not named by the finding and is not edited.

### FG-21 — A retry limit that names a check gate which does not exist

- What changed: The section on conditions now says that the identifier named by a retry limit must be the identifier of a check done gate of the same change, and that a definition naming none is rejected. A new example shows the rejection.
- Why: The reviewer says no rule required the named gate to exist in the same change, and the owner dispositioned the finding fix.
- Options: none: no design choice was open, because the finding names the fix itself.
- Owner decision: none: no design choice was open, because the finding names the fix itself.
- Owner reason: none: no design choice was open, because the finding names the fix itself.
- Channel: none: no design choice was open, because the finding names the fix itself.
- Before: none (new text)
- After: "The identifier named by `gate` MUST be the identifier of a done gate of the kind `check` of the same change, and a definition whose retry limit names none is rejected."
- Notes: Section 23.3 only: one sentence is added to the end of the bullet on the member `retry_limit`, and the example AE-320 is placed after the related example AE-273. The sentence that the finding quotes is not reworded. No design choice was open: the finding names the fix itself. The sweep for stale statements found none:
  - Section 23.3, the sentences on the member `gate` and the member `limit`, on the rejection of a condition with none, two or other members, and the example AE-273: stay true.
  - Section 24.2, the paragraph that defines a retry limit, the count of results of the named gate and the rejection of a retry limit that is not a non-negative integer when the gate definitions are approved: stays true.
  - Section 12 and Section 12.1, the sentences that a retry limit is a soft fail condition: stay true.
  - the examples AE-63, AE-64 and AE-70: stay true.

### FG-22 — A sentence that cites the earlier text of the method

- What changed: The clause that cited the earlier text of the method was removed from the sentence on a retry limit. The rest of the sentence is unchanged.
- Why: The reviewer says the clause cites a document outside the specification, and the owner dispositioned the finding fix.
- Options: none: no design choice was open, because the finding names the fix itself.
- Owner decision: none: no design choice was open, because the finding names the fix itself.
- Owner reason: none: no design choice was open, because the finding names the fix itself.
- Channel: none: no design choice was open, because the finding names the fix itself.
- Before: "does not end it by itself, as the earlier text of this method did."
- After: "does not end it by itself."
- Notes: Section 12 only: the clause at the end of the sentence is removed and nothing else is changed. No design choice was open: the finding names the fix itself. The sweep for stale statements found none:
  - Section 12, the sentence before it, that a retry limit is a soft fail condition so that reaching it pauses the flow for a human disposition: stays true.
  - Section 12, the part of the edited sentence before the clause, which states that reaching a retry limit pauses the flow for a human disposition and does not end it by itself: stays word for word.
  - Section 12.1, the sentence that a retry limit is a soft fail condition, and the list of the fail categories: stay true.
  - No other passage of the specification contains the words of the removed clause.

## Normative lines removed or reworded

- An existing ADR MUST only be changed or replaced through an  :: a See sentence was appended to cite the example, and no rule was reworded
- Breaking changes MUST be explicitly marked, assessed, and ap :: a See sentence was appended to cite the example, and no rule was reworded
- Unresolved blocking findings MUST block the applicable compl :: a See sentence was appended to cite the example, and no rule was reworded
- Regardless of whether it is stored inline in `evidence.md` o :: a See sentence was appended to cite the example, and no rule was reworded
- The Evidence column of the requirement coverage table points :: a See sentence was appended to cite the example, and no rule was reworded
- The gates of a `core` change MUST be evaluated in this order :: the stop rule was aligned with the group rule, as the finding names

## Findings whose quoted sentence an edit touched

None.

## Findings not touched

- RF-A-001 (MAJOR): open information; no edit
- RF-A-002 (MAJOR): open information; no edit
- RF-A-003 (MINOR): open information; no edit
- RF-A-004 (MINOR): open information; no edit
- RF-A-005 (MINOR): open information; no edit
- RF-A-006 (INFO): open information; no edit
- RF-B-002 (MINOR): open information; no edit
- RF-B-003 (MINOR): open information; no edit
- RF-B-005 (MINOR): open information; no edit
- RF-B-006 (INFO): open information; no edit
- RF-D-001 (MAJOR): open information; no edit
- RF-D-002 (MINOR): open information; no edit
- RF-D-003 (MINOR): open information; no edit
- RF-D-004 (INFO): open information; no edit
- RF-E-001 (MINOR): open information; no edit
- RF-E-002 (MINOR): open information; no edit
- RF-E-003 (MINOR): open information; no edit
- RF-E-004 (MINOR): open information; no edit
- RF-X-005 (MINOR): open information; no edit
- RF-X-006 (MAJOR): open information; no edit
- RF-X-007 (MAJOR): open information; no edit
- RF-X-008 (MAJOR): open information; no edit
- RF-X-009 (MINOR): open information; no edit
- RF-X-010 (MINOR): open information; no edit
- RF-X-011 (MINOR): open information; no edit
- RF-X-012 (MINOR): open information; no edit

## Header

The header of the specification (the Version line and the Revision line) is unchanged by this round.
