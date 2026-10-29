# Fix register, round 6: what changed in the specification and why

This register lists the changes made to the specification to fix the BLOCKING finding of the fifth independent review that the owner dispositioned fix, and the further findings that the owner dispositioned fix in the disposition addendum of round 5. For a change of the kind owner decision the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For a change of the kind repair the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.

## The changes

| Change | Title | Findings | Kind | Status | Sections | Examples |
|---|---|---|---|---|---|---|
| FG-23 | A reserved device name that is followed by an extension | RG-A-001, RG-X-004 | repair | drafted | 4.3 | AE-321 |
| FG-24 | Which change a supersede action may name as its replacement | RG-C-001 | owner decision | drafted | 23.4 | AE-322 |
| FG-25 | A specification file that nothing protects when its approval is never required | RG-X-001 | owner decision | drafted | 23.7 | AE-323 |

## Change details

### FG-23 — A reserved device name that is followed by an extension

- What changed: The rule on reserved device names now tests the part of the identifier before its first dot, so that `nul.txt` and `COM3.log` are rejected like `nul`. A new example shows both the rejected and the accepted identifiers.
- Why: The reviewer says the old test compared the whole identifier, and the owner dispositioned both findings fix.
- Options: none: no design choice was open, because the finding names the fix itself.
- Owner decision: none: no design choice was open, because the finding names the fix itself.
- Owner reason: none: no design choice was open, because the finding names the fix itself.
- Channel: none: no design choice was open, because the finding names the fix itself.
- Before: "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."
- After: "The part of the identifier before its first dot, which is the whole identifier when it holds no dot, MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."
- Notes: Section 4.3 only: one sentence of the paragraph on the identifier of a change is rewritten, the sentence See AE-321. is appended after See AE-288. at the end of that paragraph, and the example AE-321 is placed after AE-288. The list of reserved names is not widened and no other sentence of the paragraph is reworded. No design choice was open: the required action of RG-A-001 names the fix itself, and it also gives the reviewer's second wording, which forbids a dot after a reserved word. The two wordings reject the same identifiers (checked on `nul.txt`, `COM3.log`, `nul-1` and `console.txt`, and on `con.x`, `nul.tmp` and `a.nul`), and the first was drafted because the required action names it first. RG-X-004 is named in the Findings cell because the owner dispositioned it fix; the sentence that both findings quote is the sentence rewritten as the repair of RG-A-001 requires. The other reading that RG-X-004 names, to state that only bare names are prohibited, would leave `nul.txt` legal and contradict the fix recorded for RG-A-001, so it was not drafted. The sweep for stale statements (a search of the whole specification for each reserved name followed by a dot, for reserved and for device) found none:
  - Section 4.3, the example AE-288: stays true; its identifier `nul` is rejected under both the old and the new sentence.
  - Section 4.3, the sentences on the character pattern, the final dot, the uniqueness after the folding, the values of `follows` and `replaced_by` and the rejection of a definition: stay true and are not edited.
  - Section 16.1, the sentence that the Change ID follows the syntax of the identifier of a change: stays true.
  - Section 23.1 and Section 23.4, the sentences that the identifier follows the syntax of Section 4.3 and the rows of the `new` action: stay true.
  - the other uses of the words reserved and device concern other things and stay true.

### FG-24 — Which change a supersede action may name as its replacement

- What changed: A supersede action now refuses a replacement that is already closed. The condition of the action and the list of rejections say so, and a new example shows the refusal.
- Why: The reviewer says a change could be superseded into a dead end, and the owner dispositioned the finding fix and chose the way.
- Options: Not closed | Not closed, or done
- Owner decision: Not closed
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: "and `replaced_by` names a different change that exists."
- After: "and `replaced_by` names a different change that exists and is not `closed`."
- Notes: Section 23.4: the precondition of the `supersede` row of the transition table says that the replacement exists and is not closed, the `supersede` row of the table of results lists a closed replacement among the grounds for rejection, and the See list of the transition row gains AE-322. The example AE-322 is placed after AE-45, with the other examples of the `supersede` action in Section 23.4, and not after AE-309, which stands in Section 24.1. The paragraph on `follows` is not edited. The sweep for stale statements (a search for supersede, replaced_by, replacement and the words of the rule) found none:
  - Section 23.4, the sentence that the action `supersede` is performed by a human participant, and the sentence on the gate definitions that prevent it: stay true.
  - the examples AE-44, AE-78 and AE-309 name an existing change B without its state: they stay true because the change B of each is not closed, and they are not edited.
  - the example AE-45 and the examples AE-06 and AE-07: stay true; in AE-06 the replacement is a newly created change and in AE-07 the closed change is the one being superseded.
  - Section 8.3 and the example AE-245, and the phase and status model of the full profile: another profile, stay true.
  - Section 25.1, the member `replaced_by` of the state document: stays true.

### FG-25 — A specification file that nothing protects when its approval is never required

- What changed: The section on the base gates now says openly that the specification file is protected against later edits only after it was approved, and that before that only the change definition file is a machine-checkable anchor. A new example shows an edit that is not reported.
- Why: The reviewer says an edit of an unapproved specification file goes unnoticed, and the owner dispositioned the finding fix and chose the way.
- Options: Record its hash | Always approve it | Say it openly
- Owner decision: Say it openly
- Owner reason: none given
- Channel: Given by the repository owner through the interactive question tool and relayed by the orchestrating session.
- Before: none (new text)
- After: "before its first approval, an edit of `spec.md` is not reported as a difference from an approved version, and `change.yaml` is the only machine-checkable anchor of the change. See AE-323."
- Notes: Section 23.7 only: one new paragraph with one sentence is placed after the paragraph that ends with See AE-276., and the example AE-323 is placed after AE-276. The existing sentences of the section, including the sentence that a never-approved specification does not stop the start action, are not reworded. The sweep for stale statements (a search for never approved, stale, approved at least once and machine-checkable) found none:
  - Section 23.7, the bullet on the stale specification approval gate, which is active only after a first approval: stays true.
  - Section 23.7, the examples AE-57 and AE-276: stay true.
  - Section 23.4, the start row and the examples AE-25 and AE-26: stay true; the approval of the specification is still required only when the compliance profile or the project configuration requires it.
  - Section 24.3, the rule that an approval binds the exact content that is approved: stays true.
  - Section 5.3 and the example that rejects a redefinition of the base gate stale-spec-approval: stay true.

## Normative lines removed or reworded

- The identifier of a change, which is the `id` of a `core` ch :: the reserved-name sentence was rewritten so that the test applies to the part before the first dot, as the finding names

## Findings whose quoted sentence an edit touched

None.

## Findings not touched

- RG-A-002 (MINOR): open information; no edit
- RG-A-003 (MINOR): open information; no edit
- RG-A-004 (MINOR): open information; no edit
- RG-A-005 (MINOR): open information; no edit
- RG-A-006 (INFO): open information; no edit
- RG-B-001 (MINOR): open information; no edit
- RG-B-002 (MINOR): open information; no edit
- RG-B-003 (MINOR): open information; no edit
- RG-B-004 (INFO): open information; no edit
- RG-C-002 (MINOR): open information; no edit
- RG-D-001 (MINOR): open information; no edit
- RG-E-001 (MINOR): open information; no edit
- RG-E-002 (MINOR): open information; no edit
- RG-E-003 (INFO): open information; no edit
- RG-E-004 (INFO): open information; no edit
- RG-X-002 (MINOR): open information; no edit
- RG-X-003 (MINOR): open information; no edit
- RG-X-005 (MINOR): open information; no edit

## Header

The header of the specification (the Version line and the Revision line) is unchanged by this round.
