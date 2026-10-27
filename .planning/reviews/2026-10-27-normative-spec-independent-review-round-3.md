# Independent review, round 3: proposed normative method specification

- Independent review: reported
- Owner dispositions: recorded in the review disposition record
- Blocking findings: 3

## The text reviewed

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `a81d9c89651f326605db08708ea4c079809a2825` |
| Reviewed SHA-256 | `d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc` |
| Line count | `4794` |
| Diffstat | `1 file changed, 3419 insertions(+), 47 deletions(-)` |
| Commits touching the file | `49` |
| Owner approval record | `.planning/reviews/2026-10-27-normative-spec-fix-round-3-approval-record.md` |
| Owner approval record blob | `3bae1be694d7f38eee59c08e1926c95d095ed554` |
| Run set | `25ed0550004e` |
| Consent question | `May I send the test run and the six review passes RT-A, RT-B, RT-C, RT-D, RT-E and RT-X (run set 25ed0550004e, model swe-2-medium) to Devin now? Sending cannot be undone, and no run is repeated without asking you again.` |
| Consent answer | `Consent` |

## Independence

- Requestor: Claude Code
- Reviewer: Devin CLI, a different product from a different vendor than the Requestor
- Reviewer version: 3000.4.25
- Reviewer model: swe-2-medium
- Invocation: headless (devin -p), permission mode auto, a read-only minimal configuration, one separate session per pass; no session, context or notes are shared with the Requestor or between passes
- Requestor role: prepared the inputs, started the passes, quoted each report mechanically and checked its format; did not write, edit, filter, merge, summarise or re-rate any finding

## Charter

The reviewer was asked to judge the changed text against eight items:

- C1 Contradiction and ambiguity: statements that cannot all hold together, a term used in two senses, a rule whose outcome cannot be determined from the text.
- C2 Owner decisions: each decision O-1 to O-11 of DECISIONS.md is implemented as chosen and none is contradicted; a decision with no corresponding text.
- C3 Requirements: each requirement SPEC-01 to SPEC-18 of REQUIREMENTS.md is satisfied by normative text and none is contradicted; content a requirement asks for that is missing.
- C4 Testability and bypass: rules that cannot be tested from outside, rules a hostile participant or agent could satisfy in letter while defeating their purpose, failure behaviour left unspecified.
- C5 Acceptance examples: an example that does not follow from its rule, contradicts it, or covers another case than the one it names.
- C6 Self-containment: text that cites development artifacts, prototype identifiers, identifiers of decisions or requirements of a project, tool names that are not part of the method, or local paths.
- C7 Weakening: a protection, MUST or SHOULD rule or prohibition of BASE.md that SPEC.md removes, relaxes or makes conditional without saying so.
- C8 References and terms: a wrong section number, example number or cross-reference; a term used without or before its definition.

## Severity scale

- BLOCKING: the text must not be treated as final until the finding is fixed or the repository owner dispositions it.
- MAJOR: a defect that an implementer or participant could plausibly act on incorrectly but that is not BLOCKING.
- MINOR: a defect of wording, structure or reference that cannot change what a conforming participant does.
- INFO: an observation or question that is not a defect.

## Passes

| Pass | Scope |
|---|---|
| RT-A | The header and sections 1 to 8 |
| RT-B | Sections 9 to 22 |
| RT-C | Section 23 |
| RT-D | Section 24 up to the end of 24.5 |
| RT-E | Sections 24.6 to 24.10 and section 25 |
| RT-X | The whole text, read across sections |

## Reports

Each report is quoted whole, line by line: a quote mark and a space are added at the start of each line, and an empty line becomes a quote mark alone. The only change made to a report is mechanical: line endings are converted to LF and each tab to four spaces.

### RT-A — The header and sections 1 to 8

> REPORT BEGIN RT-A
> IDENTITY: Devin, Cognition, model SWE-2 Medium; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RT-A, from the header of SPEC.md up to but not including heading 9 (lines 1-1118)
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5
> FINDINGS: 4
> FINDING RT-A-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 8.4; lines 1065-1065; quote "The comparison of the gate definitions with the approved ones (Section 24.1) does not stop `cancel` or `supersede`."
> SUMMARY: Edited gate definitions block every operation except cancellation per SPEC-01, but the text also exempts `supersede`.
> REASONING: REQUIREMENTS.md SPEC-01 states that a later edit to the gate definitions "blocks every operation except cancellation until a human re-approves". Section 8.4 (line 1065) states the hash comparison "does not stop `cancel` or `supersede`", and the referenced Section 24.1 confirms three exempt operations: `cancel`, `supersede`, and the re-approval itself. Allowing `supersede` to proceed is a second termination path the requirement text does not name. The intent (a change can always be ended) is plausible, but the text as written goes beyond the requirement's literal scope and the owner should decide whether the requirement or the text is corrected.
> DISPOSITION REQUIRED: Owner decision: either adjust the normative text to exempt only cancellation, or amend/confirm the requirement so that `supersede` is an accepted additional exemption.
> FINDING RT-A-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."
> SUMMARY: Reserved-name check compares the whole identifier; names like `nul.txt` pass it yet remain reserved on Windows.
> REASONING: The rule exists so the identifier can safely name the directory `specs/<change-id>/`. On Windows, the reserved device names are matched on the base name before any extension: `nul`, `nul.txt`, and `con.anything` are all invalid or resolve to devices. The stated check rejects only an identifier that equals the reserved name exactly, so an identifier such as `nul.x` satisfies every stated rule (it matches the pattern, does not end with `.`, and is not equal to `nul`) but still cannot name a directory on a Windows file system. An implementer following the text literally would accept identifiers that later fail or behave dangerously on Windows.
> DISPOSITION REQUIRED: Fix: also reject an identifier whose portion before the first `.` is a reserved name, or state explicitly that the check covers whole names only and accept the residual Windows risk.
> FINDING RT-A-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 5.3; lines 392-392; quote "Layer 5 is the gates and the scope of the change definition (Section 23.1)."
> SUMMARY: Layer 5 is defined as "local strengthening in the change specification" but for `core` it is silently relocated to the change definition.
> REASONING: The numbered resolution list defines layer 5 as "local strengthening in the change specification". For a `core` change the paragraph substitutes "the gates and the scope of the change definition", which is a different document (`change.yaml`, not `spec.md`). Since a `core` change also keeps a `spec.md` (Section 4.3), it is undecidable from the text whether additional gates or strengthening stated in a `core` change's `spec.md` count as layer-5 contributions or are ignored. The intended reading (change definition only) is probable but not stated.
> DISPOSITION REQUIRED: Clarify whether a `core` change's `spec.md` may carry layer-5 strengthening, or state that layer 5 for `core` is exclusively the change definition.
> FINDING RT-A-004
> SEVERITY: INFO
> REFERENCE: file BASE; section 8.3; lines 514-514; quote "wait when the new corrective scope's DoW determines a pause"
> REFERENCE: file SPEC; section 8.3; lines 909-909; quote "the resume-phase DoR is not satisfied, or a Definition of Wait condition of the new corrective scope is active"
> SUMMARY: BASE let `reopen` pause on an active DoW of the new scope; SPEC rejects instead of waiting.
> REASONING: In BASE the `reopen` rejection behavior included waiting when the new corrective scope's DoW determined a pause. In SPEC, `reopen` never answers `blocked` and is rejected when a DoW condition of the new corrective scope is active (transition table row and AE-296). The behavior is internally consistent with the new rejected/blocked model and the change simply stays closed, so this is likely deliberate; it is recorded so the owner can confirm the removal of the wait path was intended.
> DISPOSITION REQUIRED: Owner confirmation that removing the DoW wait path for `reopen` is intended; no change needed if confirmed.
> CHECKS PERFORMED:
> C1: Read SPEC sections header through 8.5 in full and cross-checked the transition table against 8.4, 8.5, and the referenced 24.1, 24.2, 24.7; found no internal contradiction; found the layer-5 wording gap of RT-A-003.
> C2: Traced O-1 (two method profiles, Section 5.6), O-3/A3 (Section 5.4 assurance levels), O-4 (`state.json` in 4.3 and 8.1 JSON example), O-6 (`reopen` marked `full` only in 8.3/8.4), O-8 (Section 5.6 marks `full` specified-but-not-implemented), O-9/O-10 (six layers, `core` implements 1,2,3,5), and O-2/O-5 consequences visible in 8.3 (`blocked` results table); all implemented as chosen in this range.
> C3: Checked the in-range portions of SPEC-01, SPEC-12, SPEC-14, SPEC-15, SPEC-16, SPEC-17; all satisfied except the SPEC-01 exemption gap reported as RT-A-001.
> C4: Examined identifier rejection rules, gate-weakening rejection, non-delegable approvals, and not-evaluable handling for bypass; found the Windows reserved-name gap of RT-A-002.
> C5: Verified in-range acceptance examples AE-01 to AE-08, AE-121 to AE-124, AE-217 to AE-248, AE-288 to AE-308 against their rules; all follow from the stated rules.
> C6: Searched the range for prototype identifiers, tool names, local paths, and requirement or decision ids; none found (AE-nn are the specification's own acceptance-example identifiers).
> C7: Compared every changed sentence in sections 1-8 against BASE; the `silently` removal in 5.3 and the `fail`-action narrowing in 8.3 are consistent with the new hard/soft model of Section 24.7; the `reopen` DoW change is reported as RT-A-004; no unstated weakening found.
> C8: Checked section references made in the range (23.1, 23.3, 23.4, 23.7, 24.1, 24.2, 24.3, 24.5, 24.7, 22.2, 16.1, 16.4, 25.1, 11.1, 13, 12, 9, 10, 5.6); all resolve; terms (DoR, DoD, DoW, DoF, assurance level, blocked) are defined or referenced at or before use.
> LIMITS: Read-only review using Read, Grep, and single allowed shell commands (ls, wc, grep, sed, sha256sum). Sections 9-25 were consulted only to judge in-range text (24.1, 24.2, 24.7, 23.4, 23.7 spot checks). No file outside the working directory was opened. Whether `supersede` should be exempt under SPEC-01 is left to the owner.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RT-A

### RT-B — Sections 9 to 22

> REPORT BEGIN RT-B
> IDENTITY: Devin, Cognition, model SWE-2 Medium; I share no session, prompt, notes or model with Claude Code: no.
> INPUT SPEC.md d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RT-B, sections 9 to 22 of SPEC.md (from heading 9 up to, not including, heading 23)
> COVERAGE: 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4
> FINDINGS: 4
> FINDING RT-B-001
> SEVERITY: BLOCKING
> REFERENCE: file BASE; section 12.1; lines 785-785; quote "exceeding hard budget, cost, or retry limits"
> REFERENCE: file SPEC; section 12; lines 1485-1485; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition"
> SUMMARY: BASE made exceeding a retry limit a condition under which the flow MUST terminate; SPEC makes every retry limit soft, allowing a recorded override and further attempts.
> REASONING: BASE.md lists exceeding retry limits among the typical fail categories of a DoF whose rule is that the flow MUST terminate unsuccessfully. SPEC.md removes retry limits from that category and declares a retry limit to be a soft fail condition under Section 24.7, where a human may close the change or record an override granting further attempts. That is a relaxation of a protection of the old text: behaviour that previously had to end the change can now continue by human disposition. The change implements the hard/soft distinction a requirement asks for, but the requirement text does not itself order that retry limits lose their terminating character, so the weakening stands as a finding for the repository owner to disposition.
> DISPOSITION REQUIRED: Owner decision: confirm that retry limits may be soft under Section 24.7 and no longer terminate the flow, or restore a terminating path (for example allow a hard severity on retry rules).
> FINDING RT-B-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 12; lines 1485-1485; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition"
> REFERENCE: file SPEC; section 12.1; lines 1501-1501; quote "A retry limit is a soft fail condition (Section 24.7)."
> SUMMARY: The normative statement that a retry limit is a soft fail condition is made twice, once before and once inside Section 12.1.
> REASONING: The same rule is stated in the introduction of Section 12 and again verbatim inside Section 12.1. The duplication cannot change behaviour, but it creates two normative homes for one rule and invites divergence on a later edit.
> DISPOSITION REQUIRED: Fix: keep one statement of the rule.
> FINDING RT-B-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 12.1; lines 1505-1505; quote "The interpreter that runs the commands of gates is explicit and opt-in (Section 24.10)."
> SUMMARY: A sentence about the gate-command interpreter sits inside the typical-fail-categories section although it is not a fail category.
> REASONING: Section 12.1 enumerates kinds of fail conditions. The sentence about the interpreter of Section 24.10 is a general statement, not a fail category, and its placement inside this section can mislead a reader into reading it as a fail trigger. It is a structural defect only.
> DISPOSITION REQUIRED: Fix: move the sentence to a fitting place, for example near Section 24.10 references outside the category list.
> FINDING RT-B-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 20; lines 2152-2152; quote "a soft failure that awaits a human disposition is a fail gate of the severity `soft` (Section 23.6)"
> SUMMARY: The completion criteria equate a soft failure awaiting disposition with any fail gate of severity soft, omitting that the gate must have decided.
> REASONING: The paragraph maps `full` conditions to `core` counterparts. Read literally, a `core` change that merely declares a fail gate of severity `soft` would count as having a soft failure awaiting disposition, even when the gate never fired, which would block completion wrongly. The neighbouring sentences use deciding gates for the active cases, so the intended reading is clear in context but the sentence itself is imprecise.
> DISPOSITION REQUIRED: Clarify: state that only a soft-severity fail gate that has decided counts as awaiting a human disposition.
> CHECKS PERFORMED:
> C1: Read sections 9 to 22 for statements that cannot hold together, doubled senses of terms and undeterminable rules; found the duplicated retry-limit rule (finding 002) and the imprecise soft-failure mapping (finding 004).
> C2: Traced O-1 to O-11 against this range; O-5 (fourth result blocked) is implemented in 22.2, O-11 (verify-only CI) in 22.4, O-4 (JSON state) in the 11.2 template and layout references, O-7 in the migrate operation of 22.1 and the issue codes of 22.2; no contradiction found in this range.
> C3: Traced SPEC-01 to SPEC-18 against this range; SPEC-03, SPEC-08, SPEC-09, SPEC-10 and the envelope rules appear satisfied by the text examined; SPEC-02 is partly visible through 11.1 and 12.1 references to Section 24.2; no missing in-range content found.
> C4: Checked testability and bypass of the changed rules; the blocked/rejected envelope rules, the guard verifications and the wait/fail contents are externally testable; found the weakening of retry-limit termination (finding 001).
> C5: Checked the acceptance examples AE-260 to AE-270, AE-287, AE-303 to AE-306 and AE-111 to AE-116 against their rules; each follows from the rule it names and names the section it covers; no defect found.
> C6: Checked for development artifacts, prototype identifiers, project decision or requirement ids, foreign tool names and local paths in this range; the named agents and tools in 14.2 and 17 are marked non-normative examples and were present in BASE; no defect found.
> C7: Compared each in-range protection, MUST and SHOULD rule of BASE with SPEC; found the retry-limit relaxation (finding 001); the removals of "or explicitly accepted" for open questions implement the stricter open-question requirement and are stated openly.
> C8: Checked cross-references and term use in the range; references to Sections 5.6, 8.3, 23.4, 23.6, 24.1 to 24.10 and 25.1 resolve to existing headings; found the misplaced interpreter sentence (finding 003).
> LIMITS: Judgement of references into sections outside the range (8.3, 23.x, 24.x, 25.x) is based on their headings and the citing sentences only, not on a full read of those sections. Whether a retry limit may still be declared with severity hard under Section 24.7 was not verified. Tools used: Read, Grep, sha256sum, diff, ls, wc, grep headings. No file outside the working directory was opened.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RT-B

### RT-C — Section 23

> REPORT BEGIN RT-C
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the SWE-2 Medium model; I share no session, prompt, notes or model with Claude Code.
> INPUT SPEC.md d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RT-C, section 23 of SPEC.md, from the heading `## 23. The `core` Profile` up to but not including `## 24. Protections Shared by Both Profiles`.
> COVERAGE: 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7
> FINDINGS: 3
> FINDING RT-C-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 23.3; lines 2480-2480; quote "`retry_limit`: a mapping with the members `gate` and `limit`, for a fail gate only."
> REFERENCE: file SPEC; section 23.3; lines 2483-2483; quote "or that names a predicate which is not listed for the kind of the gate MUST be rejected"
> SUMMARY: A wait gate whose condition holds `retry_limit` is forbidden by implication but is not covered by the MUST-reject enumeration, leaving the outcome undetermined.
> REASONING: Section 23.3 states that a condition holds exactly one of `command`, `retry_limit`, and `predicate`, and that `retry_limit` is "for a fail gate only". The rejection sentence covers a condition that holds none of the listed members, two or more of them, another member, or an unlisted predicate. A wait gate whose condition holds `retry_limit` satisfies none of those four cases: it holds exactly one listed member and names no predicate. The text therefore does not determine whether such a change definition MUST be rejected or is merely invalid. An implementer could plausibly accept it.
> DISPOSITION REQUIRED: Clarify the rejection rule so that a `retry_limit` condition on a wait gate is explicitly rejected, for example by adding "or that holds `retry_limit` on a wait gate" to the enumeration.
> FINDING RT-C-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 23.3; lines 2480-2480; quote "The member `gate` is the identifier of a done gate of the kind `check`, and the member `limit` is the limit of Section 24.2."
> SUMMARY: No rule states that a `retry_limit` whose member `gate` names a nonexistent gate or a gate that is not a `check` done gate MUST be rejected.
> REASONING: The member `gate` is defined as the identifier of a done gate of the kind `check`, but the rejection enumeration in the same paragraph does not cover the case where `gate` names no such gate: a missing identifier, a wait or fail gate identifier, or a `sign-off` done gate identifier all hold exactly one listed member and no invalid predicate. Section 24.2 defines when a retry limit becomes active but the definitional constraint in 23.3 has no matching MUST-reject requirement, so the outcome for such definitions is not determined by the text.
> DISPOSITION REQUIRED: Extend the rejection rule to cover a `retry_limit` condition whose `gate` member does not identify a `check` done gate of the same change.
> FINDING RT-C-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.3; lines 2491-2491; quote "- Covers: Section 12.2"
> SUMMARY: Example AE-271, located in Section 23.3 and about `core` fail gates, declares "Covers: Section 12.2" rather than Section 23.3.
> REASONING: Every neighbouring example in Section 23.3 declares "Covers: Section 23.3". AE-271 concerns what a `core` fail gate is not required to state from Section 12.2, so the label may be intentional, but as written it attributes coverage to a section the example does not exemplify and breaks the uniform convention used elsewhere in the section. It cannot change conforming behaviour.
> DISPOSITION REQUIRED: Fix or clarify the Covers label of AE-271, for example "Covers: Sections 12.2 and 23.3" or "Covers: Section 23.3".
> CHECKS PERFORMED:
> C1: Read all of section 23 and cross-checked the state model, gate condition rules, action preconditions and evaluation order for internal consistency; found the two undetermined rejection cases reported as RT-C-001 and RT-C-002; no outright contradictions found.
> C2: Traced the owner decisions relevant to this range: O-1 (both profiles kept; `core` is the four-state model, section 23 implements it), O-5 (`blocked` handled per action in the rejected/blocked table), O-6 (no `reopen` in `core`, stated in 23.4), O-9 (shared protections referenced via Section 24), O-10 (four resolution layers; base gates protected in 23.7); none contradicted within this range.
> C3: Checked the requirements that touch this range: SPEC-02, SPEC-03, SPEC-08, SPEC-09, SPEC-12, SPEC-16, SPEC-17 are addressed by the text of section 23 and its pointers; nothing they ask for is missing within this range.
> C4: Assessed testability and bypass: actions are rejected from unlisted states, closed is final, follows cannot resurrect a change, base gates cannot be removed or redefined, gate evaluation order is fixed; the only externally visible failure left unspecified is the rejection of the malformed conditions in RT-C-001 and RT-C-002.
> C5: Verified each acceptance example AE-09 to AE-59 and AE-215 to AE-299 in this range against its stated rule; all follow from the text; the single coverage-label anomaly is reported as RT-C-003.
> C6: Searched the range for citations of development artifacts, prototype identifiers, decision or requirement identifiers, foreign tool names and local paths; none found.
> C7: Compared BASE.md structure: BASE.md ends at section 22 and contains no counterpart to section 23, so the range is wholly new text; no protection, MUST or SHOULD rule of BASE.md located in this range is removed, relaxed or made conditional.
> C8: Checked cross-references made in the range: Sections 3.1, 3.7, 3.9, 4.1, 4.3, 5.1, 5.3, 5.6, 6, 7, 9, 10, 11.1, 11.2, 12.2, 14.5, 22.3, 22.4, 23.1-23.7, 24.1-24.10 and 25.1, 25.3 all exist and the cited content matches; terms such as `not_evaluable`, `not_applicable` and wait kinds are used consistently with their definitions elsewhere.
> LIMITS: The pass was limited to section 23; other sections were read only as needed to judge references and consistency. BASE.md contains no corresponding section, so weakening was judged at the level of whole-section presence rather than line-level diff. Tools used: Read, Grep, and single allowed commands ls, grep, sha256sum, sed and awk for line lookup; no file outside the working directory was opened. DECISIONS.md and REQUIREMENTS.md were read in full.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RT-C

### RT-D — Section 24 up to the end of 24.5

> REPORT BEGIN RT-D
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the model SWE-2 Medium; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RT-D, Section 24 up to the end of 24.5 (SPEC.md lines 3057-3899); BASE.md ends at Section 22.3, so the entire pass range is added text with no counterpart in BASE.
> COVERAGE: 24, 24.1, 24.2, 24.3, 24.4, 24.5
> FINDINGS: 3
> FINDING RT-D-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 24.2; lines 3354-3354; quote "The actions `wait`, `fail`, and `reopen` are rejected with `changed` false, nothing is written"
> SUMMARY: The full-only rule rejecting wait, fail, and reopen with issue code gate-not-evaluable has no acceptance example, contrary to SPEC-14 and O-8.
> REASONING: In `core` the actions `wait`, `fail`, and `reopen` evaluate no gate (reopen does not exist, and the wait and fail actions of Section 23.4 check only their own preconditions), so the sentence is operative only in `full`. Its example pointer cites AE-298 and AE-299, which cover only `cancel` and `supersede`; no acceptance example anywhere in the text exercises `wait`, `fail`, or `reopen` being rejected with `gate-not-evaluable` when a gate applying to them cannot be evaluated. REQUIREMENTS.md SPEC-14 requires that each `full` rule has an acceptance example of the kind the `core` rules have, and the recorded consequences of decision O-8 name giving each rule an acceptance example as the mitigation for a specified-but-unbuilt `full`. The requirement and the mitigation are therefore not met for this rule.
> DISPOSITION REQUIRED: Add an acceptance example covering the rejection of `wait`, `fail`, and `reopen` with the issue code `gate-not-evaluable` in `full`, or have the repository owner disposition the gap.
> FINDING RT-D-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.4; lines 3660-3660; quote "For the first entry, `prev` is the prefix `sha256:` followed by 64 digits 0"
> SUMMARY: The phrase 64 digits 0 is awkward and can be misread; the intended 64 zero digits should be spelled out unambiguously.
> REASONING: The parallel definition of `hash` in the same paragraph says the 64 lowercase hexadecimal digits of the SHA-256 digest, which is unambiguous. 64 digits 0 relies on the reader parsing 0 as a literal digit repeated 64 times; a misreading as a value of 64 decimal digits is unlikely but possible, and the wording is inconsistent with the sibling definition.
> DISPOSITION REQUIRED: Reword, for example to the prefix sha256: followed by 64 zero digits.
> FINDING RT-D-003
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.4; lines 3684-3684; quote "It MUST be performed by a human at the level that Section 24.3 requires for `adopt`"
> SUMMARY: Where a project requires approvals at A2 but sets no minimum for adopt, an A0 self-declared human identity can adopt a history, which weakens the anchor guarantee.
> REASONING: Section 24.4 requires an anchor or equivalent where the configuration requires approvals at A2, and refuses every action until a human adopts an unanchored history. The level required for `adopt` is the configured minimum for that kind of action (Section 24.3); a configuration that sets A2 only for approvals leaves `adopt` at A0, and at A0 the `human:` prefix is self-declared, so any participant can adopt an arbitrary consistent history and create the anchor. The specification is internally consistent and Section 24.3 states that no level proves a human is present, but the anchor's protection is only as strong as the adopt minimum in this configuration.
> DISPOSITION REQUIRED: Owner decision or clarification: whether the level required for `adopt` should be tied to the assurance level that triggers the anchor requirement.
> CHECKS PERFORMED:
> C1: Read the whole pass range and cross-checked the ordering rules, the wait/fail definitions, the anchor rules, and the scope rules against Sections 8.3, 8.5, 9.6, 11.1, 16.1, 22.2, 22.4, 23.1-23.7, and 25.1; the statements hold together; the only wording-level ambiguity found is RT-D-002.
> C2: Traced O-1, O-3, O-4, O-5, O-8, and O-9 into the range: both profiles carry the protections as invariants, assurance levels and the signed-approval statement are normative with optional verifiers, `blocked` is the fourth envelope result, state.json naming is used, and `full` is marked specified but not implemented; one consequence of O-8 (an example per full rule) is not met for one rule, reported as RT-D-001.
> C3: Verified SPEC-01 (frozen gates, Section 24.1), SPEC-02 (three-valued results, Section 24.2), SPEC-03 (blocked, via Section 22.2), SPEC-04 (A0-A2 and the statement, Section 24.3), SPEC-05 (consistency versus completeness and the anchor, Section 24.4), and SPEC-06 (scope, base revision, hard failure, isolation, Section 24.5) are satisfied; SPEC-14 is not fully satisfied (RT-D-001).
> C4: Examined fail-closed verification, the human-only action list, the signature statement with the history position (replay protection), the anchor outside the working tree, and the scope measurement including untracked and ignore-file rules; the named exemptions state.json.tmp and state.json.lock are deliberate and acknowledged; RT-D-003 records a residual observation about the adopt level.
> C5: Read every acceptance example in the range (AE-60, AE-61 to AE-86, AE-125 to AE-157, AE-249 to AE-259, AE-277 to AE-308 as present) and checked each against its rule; all follow from the rules they cite; the gap is a missing example (RT-D-001), not a wrong one.
> C6: The range cites only internal section numbers, profile names, file names of the method, and stable identifiers such as wait categories and issue codes; no development artifact, prototype identifier, decision or requirement identifier, foreign tool name, or local path appears.
> C7: BASE.md contains no Sections 23 to 25; the pass range is entirely added text, so no protection, MUST, SHOULD, or prohibition of BASE.md is removed or relaxed within the range; unchanged text was consulted only to judge the new text.
> C8: Cross-references checked: Sections 4.3, 5.4, 5.6, 8.3, 8.5, 9.6, 11.1, 12.2, 16.1, 22.2, 22.4, 23.1, 23.3, 23.4, 23.5, 23.6, 23.7, 24.5-24.10, 25.1, 25.2 all exist and say what the range cites; every AE number cited in the range (including AE-169, AE-281, AE-282, AE-286, AE-294, AE-298-300, AE-307) exists; terms used (not_applicable, anchor, adopt, wait record kinds, WAIT_EXTERNAL_SYSTEM) are defined before or at use.
> LIMITS: Tools used: Read, Grep, and the permitted commands sha256sum, grep, wc. BASE.md ends at Section 22.3, so a textual diff of the pass range against BASE was not possible beyond confirming the range is entirely new. I did not verify example numbering completeness across the whole document or the parsing rules of Section 25 outside what the range cites. I read one tool-generated overflow file under the system temporary directory containing grep output; no other file outside the working directory was opened.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RT-D

### RT-E — Sections 24.6 to 24.10 and section 25

> REPORT BEGIN RT-E
> IDENTITY: Devin, Cognition, SWE-2 Medium; I share no session, prompt, notes or model with Claude Code.
> INPUT SPEC.md d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RT-E, sections 24.6 to 24.10 and section 25, from heading 24.6 to end of file
> COVERAGE: 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 3
> FINDING RT-E-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.3; lines 4690-4690; quote "A file that already has the target version, or a higher one, is not migrated, and the operation answers `rejected`"
> SUMMARY: The rejection of a no-op migration is given no stable issue code, while every sibling refusal in 25.3 names one.
> REASONING: Section 25.3 assigns stable issue codes to each refusal (`migration-required`, `schema-version-unsupported`, `schema-version-mismatch`), but the rejection for a file already at or above the target version has none, so an implementation cannot be checked for which refusal it made and callers cannot distinguish the case mechanically.
> DISPOSITION REQUIRED: Fix by assigning a stable issue code to this rejection, or the owner decides that none is needed.
> FINDING RT-E-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.3; lines 4690-4690; quote "It applies the steps of the chain one at a time in ascending order of version"
> SUMMARY: Whether `migrate` accepts a file at a supported version below the target, and what happens when no step chain exists, is not stated.
> REASONING: `migratable` is defined only for versions that are not supported, so a file at a supported but lower version passes the version check; the text then speaks of applying "the steps of the chain" without saying whether such a file may be migrated or what the result is when no chain of steps leads from its version to the target.
> DISPOSITION REQUIRED: Clarify whether a supported version below the target is a legal input to `migrate` and specify the outcome when no step chain exists.
> FINDING RT-E-003
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.10; lines 4351-4351; quote "is not part of the gate definitions and is not frozen (Section 24.1), so a change of the configuration changes which program runs without a difference of the gate definitions"
> SUMMARY: The configured interpreter can be substituted without triggering the frozen-gates check; detection rests on review of `gate_detail` alone.
> REASONING: By design the interpreter named in the project configuration is not frozen, so changing it alters which program runs every gate command while the approved gate definitions still match. The text is explicit about this and requires the record to name the program, and recommends a warning for in-repository interpreters, so this is a documented trade-off rather than a hidden gap; it is flagged because the tamper evidence is weaker than the human re-approval that a gate-definition change forces.
> DISPOSITION REQUIRED: None required; owner may note that interpreter changes rely on record review rather than re-approval.
> CHECKS PERFORMED:
> C1: Read 24.6-25.3 in full and cross-checked rules within each section and against 22.2, 8.5, 23.5-23.7 and the Section 24 preamble; found no contradiction, but two under-specified outcomes reported as RT-E-001 and RT-E-002.
> C2: Traced O-4 (state.json, human-owned YAML), O-7 (schema_version, explicit recorded migration) and O-9 (protections for both profiles) into 25.1, 25.3 and the per-profile wording of 24.6-24.9; all implemented as chosen and none contradicted in this range.
> C3: Verified SPEC-07 (baselines), SPEC-08 (hard/soft failure and bounded overrides), SPEC-09 (questions as state blocking approval and closure), SPEC-10 (executable evidence, no requirements means incomplete), SPEC-11 (opt-in interpreter and trust consequence), SPEC-15 (JSON state and canonical form) and SPEC-18 (schema versions, refusal, explicit migration); each is satisfied by normative text in range.
> C4: Checked failure behaviour: unreadable output yields `not_evaluable`, overrides require reason and integer N of at least 1, overrides lapse on amendment, atomic write and lock rules cover interruption and concurrent writers, hand-lowered schema versions are detected; the bypass-relevant interpreter case is reported as RT-E-003 and the unspecified refusal code as RT-E-001.
> C5: Checked examples AE-87 to AE-110, AE-158 to AE-170, AE-171 to AE-182, AE-183 to AE-214, AE-279, AE-281, AE-283 to AE-285, AE-301 and AE-302 against their rules, including set equality, code-point ordering, counts of new failures, empty baseline, attempt counting and version comparisons; all follow from the rules they name.
> C6: Found no development artifacts, prototype identifiers, decision or requirement ids, or foreign tool names; `@interpreter`, `state.json`, `state.yaml`, `.ggsad/config.yaml` and the AE identifiers are defined by the method itself.
> C7: BASE.md contains no sections 23 to 25, so there is no text in range whose protection could be weakened; cross-checked that added rules do not relax protections of BASE sections they cite (8.3-8.5, 11, 12.2, 16.1, 22.1-22.2).
> C8: Verified references in range to Sections 8.3-8.5, 10.7, 11.1-11.2, 12.2, 16.1 (including the Evidence Commands heading), 20, 22.1-22.2, 23.1-23.7 and 24.1-24.5; all exist and match their subjects; no term is used before its definition.
> LIMITS: Verified all four input hashes against BRIEF.md; all match. I could not verify the literal digest quoted in AE-183 because computing it would require writing a file, which the brief forbids; the empty-object digest in AE-184 matches the known SHA-256 of "{}". Sections outside the range (23.x, 24.1-24.5, 22.x, 8.x, 11, 16.1) were read only as far as needed to judge changed text. Tools used: Read, Grep, sha256sum, wc. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RT-E

### RT-X — The whole text, read across sections

> REPORT BEGIN RT-X
> IDENTITY: Devin, Cognition, SWE-2 Medium; I share no session, prompt, notes or model with Claude Code.
> INPUT SPEC.md d116adfe870932c5e977e8a10ecf184f521a7d149a56393538a5c1360bf8e2cc
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RT-X, the whole text from header to end, read across sections, tracing each owner decision O-1 to O-11 and each requirement SPEC-01 to SPEC-18, and checking for conflicts between distant sections.
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 24, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 6
> FINDING RT-X-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 11.2; lines 1426-1426; quote "Every wait state MUST include:"
> REFERENCE: file SPEC; section 24.2; lines 3345-3345; quote "whose resume condition is that the gate can be evaluated and whose next action after resumption is the evaluation of the gate again"
> REFERENCE: file SPEC; section 24.7; lines 4000-4000; quote "in `full`, with the status `waiting` and a wait state of the category `WAIT_DECISION` (Section 11.1), whose resume condition is that a human has recorded an override"
> SUMMARY: Wait states that a full evaluation creates define only resume condition and next action, not the six fields Section 11.2 mandates.
> REASONING: Section 11.2 makes reason, outstanding information or decision, responsible person or source, resume condition, safe current state, and next action mandatory for every wait state, and AE-268 enforces that for the wait action. But the wait states created by evaluation in full, namely the WAIT_EXTERNAL_SYSTEM wait of Section 24.2 rule 2 and the WAIT_DECISION wait of Section 24.7, are specified with only a resume condition and, for the former, a next action. The text never states what the reason, outstanding decision, owner, or safe current state of such a generated wait state is, so an implementer cannot produce a conforming record from the text alone. The core equivalent is fully specified in Section 23.5, which makes the gap in full visible.
> DISPOSITION REQUIRED: Fix or clarify: state how each mandatory field of Section 11.2 is filled for a wait state that an evaluation creates in full.
> FINDING RT-X-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 24.7; lines 3998-3998; quote "The failure is decided by `cancel`, by `supersede`, or by the first action that completes or resumes the change."
> REFERENCE: file SPEC; section 8.3; lines 891-891; quote "When DoF finds a fail condition of the severity `hard` active, close the change as failed in the same state mutation and answer `success`"
> REFERENCE: file SPEC; section 8.3; lines 987-989; quote "Then the change is in the `closed` phase with the status `failed`, the result is `success`, and no wait state is recorded"
> SUMMARY: Section 24.7 omits the full wait action from the list of actions that decide a known hard failure, contradicting the Section 8.3 wait row and AE-295.
> REASONING: The transition table row for wait in Section 8.3 and example AE-295 state that a wait request on a full change with an active hard fail condition closes the change as failed. Section 24.7 closes with an exhaustive sentence naming cancel, supersede, and the first action that completes or resumes the change as the actions that decide such a failure, and wait is not among them. An implementer reading Section 24.7 alone would not apply the Definition of Fail check to the wait action, and the two statements cannot both hold if the list is read as complete.
> DISPOSITION REQUIRED: Fix: amend the enumeration in Section 24.7 to include the full wait action, or reword it so it is not an exhaustive list.
> FINDING RT-X-003
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 24.4; lines 3684-3684; quote "The `adopt` action creates the anchor from the history as it is, at the position and the hash of its latest entry (Section 23.4)."
> REFERENCE: file SPEC; section 24.4; lines 3670-3670; quote "an implementation MUST NOT act on a change whose history has none until a human adopts the history"
> REFERENCE: file SPEC; section 24; lines 3066-3066; quote "The state file, or the inline record where no state file is persisted (Section 4.3)"
> SUMMARY: The adopt action and the anchor mechanism are undefined for a full change that keeps its record inline and has no hash-chained history.
> REASONING: Section 24.4 requires a history to have an anchor or an equivalent where the configuration requires approvals at A2, and defines adopt as creating the anchor from the position and hash of the latest entry. For a full change whose record is kept inline under Section 4.3, there is no state document and no entries with n, prev, and hash, so the position and hash that adopt must record do not exist. Section 4.3 and Section 25.1 say the history-reading rules are not enforced mechanically for such a change, and Section 22.4 lets guard report them as not enforced, but the normative obligation and the defined recovery path contradict each other: the spec both requires an anchor for acting and defines an adopt precondition whose mechanism cannot apply. The behaviour of adopt on an inline record is left unspecified.
> DISPOSITION REQUIRED: Clarify: either exempt an inline-recorded full change from the anchor requirement explicitly, or define what the anchor records and what adopt does when no entry chain exists.
> FINDING RT-X-004
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 24.1; lines 3212-3212; quote "Every state-changing operation MUST first compute the hash of the current gate definitions and compare it with the approved hash."
> REFERENCE: file SPEC; section 25.3; lines 4690-4690; quote "It is explicit and it is never carried out silently as a part of another operation."
> REFERENCE: file SPEC; section 25.3; lines 4784-4786; quote "When the change definition is migrated and then the `close` action is requested"
> SUMMARY: Whether the migrate operation is subject to the Section 24.1 gate-hash comparison is unspecified, and one reading produces a deadlock.
> REASONING: Section 24.1 names only cancel, supersede, and the re-approval as exempt from the comparison and applies it to every state-changing operation. Migrate appends an entry to the history of a change, so it plausibly counts as state-changing. If it does, a change definition that was edited after approval and that also holds a migratable schema version is stuck: approvals are refused under Section 25.3 with migration-required because the file version is unusable, while migrate is refused under Section 24.1 with gates-changed. If migrate is not state-changing, the text does not say so, and the same question arises for ask, answer, and adopt, which append entries without changing state. AE-213 assumes migrate runs while definitions then differ, which is consistent only under one reading.
> DISPOSITION REQUIRED: Clarify in Section 24.1 which operations the comparison covers, or state the order of the schema-version refusal and the gate-hash comparison for migrate.
> FINDING RT-X-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 4.1; lines 187-187; quote "This section specifies the `full` method profile (Section 5.6)."
> REFERENCE: file SPEC; section 5.6; lines 573-573; quote "A section that the table does not name as `full` only applies to both method profiles."
> SUMMARY: The full-only sentence is placed inside heading 4.1, not under the Section 4 heading as in Sections 6 to 10, leaving its scope ambiguous.
> REASONING: In Sections 6, 7, 8, 9, and 10 the same sentence appears directly under the top-level heading and correctly marks the whole section as full-only, matching the table in Section 5.6. In Section 4 the sentence appears after the 4.1 heading. Read as scoping 4.1 it matches the table, which names only 4.1 as full-only; read as scoping Section 4 it would wrongly exclude 4.2 and 4.3, which a core change needs for its directory layout and identifier syntax. The placement convention is inconsistent and the referent of this section is not unambiguous.
> DISPOSITION REQUIRED: Fix: move or reword the sentence so it clearly applies to Section 4.1 only.
> FINDING RT-X-006
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 22.2; lines 2227-2227; quote "`error`: the operation could not be carried out; nothing was written, and `changed` is `false`."
> REFERENCE: file SPEC; section 22.2; lines 2229-2229; quote "A `rejected` result with `changed` true and a `blocked` result with `changed` false are invalid."
> SUMMARY: Section 22.2 declares only two result and changed combinations invalid, leaving an error result with changed true unaddressed by that sentence.
> REASONING: The definition of the error result says nothing was written and changed is false, and AE-113 covers only the two named combinations. An envelope that answers error with changed true contradicts the definition of error but is not covered by the explicit invalidity rule, which names only rejected with changed true and blocked with changed false. An implementer validating envelopes could plausibly treat the omission as deliberate.
> DISPOSITION REQUIRED: Fix or clarify: either state that every result other than success implies changed false, or add the error combination to the invalidity rule.
> CHECKS PERFORMED:
> C1: Compared interacting rules across distant sections (8.3, 22.2, 23.4, 23.5, 23.6, 24.1 to 24.10, 25.1 to 25.3) for statements that cannot hold together; found the wait-state content gap, the hard-failure enumeration omission, the inline-record anchor gap, and the migrate and comparison ordering ambiguity (findings RT-X-001 to RT-X-004).
> C2: Traced each of O-1 to O-11 to the implementing text: O-1 and O-8 in Section 5.6, O-2 in Sections 5.3, 23 and 22.4, O-3 in 24.3, O-4 in 4.3, 8.1, 11.2, 25.1 and 25.3, O-5 in 22.2 and the per-action tables, O-6 in 8.3, 8.4 and 23.4, O-7 in 25.3, O-9 in Section 24, O-10 in 5.3 (layers 1, 2, 3, 5), O-11 in 22.4; none is contradicted or left without text.
> C3: Traced SPEC-01 to SPEC-18: SPEC-01 in 24.1, SPEC-02 in 24.2, SPEC-03 in 22.2 and the per-action tables, SPEC-04 in 24.3, SPEC-05 in 24.4, SPEC-06 in 24.5, SPEC-07 in 24.6, SPEC-08 in 24.7, SPEC-09 in 24.8, SPEC-10 in 24.9, SPEC-11 in 24.10, SPEC-12 in 5.6, SPEC-14 in 24 and the full acceptance examples, SPEC-15 in 25.1 and the JSON templates, SPEC-16 in 5.3, SPEC-17 in 8.3 and 23.4, SPEC-18 in 25.3; SPEC-13 concerns src files and cannot be checked from this text. No requirement is contradicted by the text.
> C4: Checked externally testable rules and hostile-participant bypasses: fail-closed verification in 24.3, no-shell commands in 24.10, ignored-location warning in 24.5 and 24.10, anchor limits in 24.4; the failure behaviour gaps found are reported as findings RT-X-001, RT-X-003 and RT-X-004.
> C5: Read the acceptance examples AE-01 through AE-308 that accompany changed rules and checked each against its named rule; the examples examined follow from their rules and cover the cases they name; no counterexample found.
> C6: Searched the whole text for development-artifact references, prototype identifiers, decision and requirement identifiers, tool names and local paths; only the migration of a legacy state.yaml file appears, which is part of the method, not a project artifact.
> C7: Diffed BASE.md against SPEC.md line by line: no MUST, SHOULD or prohibition of BASE.md was removed, relaxed or made conditional; the reopen rejection change is stricter, not weaker, and the blocked result was added per O-5.
> C8: Checked section numbers and cross-references cited by the changed text (5.3 layers, 8.3, 11.1, 11.2, 12.2, 16.1, 22.2, 22.4, 23.x, 24.x, 25.x) and terms used before definition; references resolve; identifier, gate result, severity, and result names are used consistently.
> LIMITS: SPEC-13 (no file under src slash ggsad modified) cannot be verified from the reviewed text, which contains no such files; the review is limited to the specification text. I could not exhaustively confirm that every single full rule has an acceptance example (SPEC-14); coverage was spot-checked across Sections 4 to 22 and 24. Consistency between table cells of the two transition tables was checked by reading, not by mechanical proof. Tools used: Read, Grep, and single allowed shell commands ls, wc, sha256sum, diff, grep. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RT-X

## Findings

| Finding | Severity | Reference | Summary | Disposition |
|---|---|---|---|---|
| RT-A-001 | BLOCKING | file SPEC; section 8.4; lines 1065-1065; quote "The comparison of the gate definitions with the approved ones (Section 24.1) does not stop `cancel` or `supersede`." | Edited gate definitions block every operation except cancellation per SPEC-01, but the text also exempts `supersede`. | fix |
| RT-A-002 | MAJOR | file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case." | Reserved-name check compares the whole identifier; names like `nul.txt` pass it yet remain reserved on Windows. |  |
| RT-A-003 | MINOR | file SPEC; section 5.3; lines 392-392; quote "Layer 5 is the gates and the scope of the change definition (Section 23.1)." | Layer 5 is defined as "local strengthening in the change specification" but for `core` it is silently relocated to the change definition. |  |
| RT-A-004 | INFO | file BASE; section 8.3; lines 514-514; quote "wait when the new corrective scope's DoW determines a pause" | BASE let `reopen` pause on an active DoW of the new scope; SPEC rejects instead of waiting. |  |
| RT-B-001 | BLOCKING | file BASE; section 12.1; lines 785-785; quote "exceeding hard budget, cost, or retry limits" | BASE made exceeding a retry limit a condition under which the flow MUST terminate; SPEC makes every retry limit soft, allowing a recorded override and further attempts. | fix |
| RT-B-002 | MINOR | file SPEC; section 12; lines 1485-1485; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition" | The normative statement that a retry limit is a soft fail condition is made twice, once before and once inside Section 12.1. |  |
| RT-B-003 | MINOR | file SPEC; section 12.1; lines 1505-1505; quote "The interpreter that runs the commands of gates is explicit and opt-in (Section 24.10)." | A sentence about the gate-command interpreter sits inside the typical-fail-categories section although it is not a fail category. |  |
| RT-B-004 | MINOR | file SPEC; section 20; lines 2152-2152; quote "a soft failure that awaits a human disposition is a fail gate of the severity `soft` (Section 23.6)" | The completion criteria equate a soft failure awaiting disposition with any fail gate of severity soft, omitting that the gate must have decided. |  |
| RT-C-001 | MAJOR | file SPEC; section 23.3; lines 2480-2480; quote "`retry_limit`: a mapping with the members `gate` and `limit`, for a fail gate only." | A wait gate whose condition holds `retry_limit` is forbidden by implication but is not covered by the MUST-reject enumeration, leaving the outcome undetermined. |  |
| RT-C-002 | MAJOR | file SPEC; section 23.3; lines 2480-2480; quote "The member `gate` is the identifier of a done gate of the kind `check`, and the member `limit` is the limit of Section 24.2." | No rule states that a `retry_limit` whose member `gate` names a nonexistent gate or a gate that is not a `check` done gate MUST be rejected. |  |
| RT-C-003 | MINOR | file SPEC; section 23.3; lines 2491-2491; quote "- Covers: Section 12.2" | Example AE-271, located in Section 23.3 and about `core` fail gates, declares "Covers: Section 12.2" rather than Section 23.3. |  |
| RT-D-001 | BLOCKING | file SPEC; section 24.2; lines 3354-3354; quote "The actions `wait`, `fail`, and `reopen` are rejected with `changed` false, nothing is written" | The full-only rule rejecting wait, fail, and reopen with issue code gate-not-evaluable has no acceptance example, contrary to SPEC-14 and O-8. | fix |
| RT-D-002 | MINOR | file SPEC; section 24.4; lines 3660-3660; quote "For the first entry, `prev` is the prefix `sha256:` followed by 64 digits 0" | The phrase 64 digits 0 is awkward and can be misread; the intended 64 zero digits should be spelled out unambiguously. |  |
| RT-D-003 | INFO | file SPEC; section 24.4; lines 3684-3684; quote "It MUST be performed by a human at the level that Section 24.3 requires for `adopt`" | Where a project requires approvals at A2 but sets no minimum for adopt, an A0 self-declared human identity can adopt a history, which weakens the anchor guarantee. |  |
| RT-E-001 | MINOR | file SPEC; section 25.3; lines 4690-4690; quote "A file that already has the target version, or a higher one, is not migrated, and the operation answers `rejected`" | The rejection of a no-op migration is given no stable issue code, while every sibling refusal in 25.3 names one. |  |
| RT-E-002 | MINOR | file SPEC; section 25.3; lines 4690-4690; quote "It applies the steps of the chain one at a time in ascending order of version" | Whether `migrate` accepts a file at a supported version below the target, and what happens when no step chain exists, is not stated. |  |
| RT-E-003 | INFO | file SPEC; section 24.10; lines 4351-4351; quote "is not part of the gate definitions and is not frozen (Section 24.1), so a change of the configuration changes which program runs without a difference of the gate definitions" | The configured interpreter can be substituted without triggering the frozen-gates check; detection rests on review of `gate_detail` alone. |  |
| RT-X-001 | MAJOR | file SPEC; section 11.2; lines 1426-1426; quote "Every wait state MUST include:" | Wait states that a full evaluation creates define only resume condition and next action, not the six fields Section 11.2 mandates. |  |
| RT-X-002 | MAJOR | file SPEC; section 24.7; lines 3998-3998; quote "The failure is decided by `cancel`, by `supersede`, or by the first action that completes or resumes the change." | Section 24.7 omits the full wait action from the list of actions that decide a known hard failure, contradicting the Section 8.3 wait row and AE-295. |  |
| RT-X-003 | MAJOR | file SPEC; section 24.4; lines 3684-3684; quote "The `adopt` action creates the anchor from the history as it is, at the position and the hash of its latest entry (Section 23.4)." | The adopt action and the anchor mechanism are undefined for a full change that keeps its record inline and has no hash-chained history. |  |
| RT-X-004 | MAJOR | file SPEC; section 24.1; lines 3212-3212; quote "Every state-changing operation MUST first compute the hash of the current gate definitions and compare it with the approved hash." | Whether the migrate operation is subject to the Section 24.1 gate-hash comparison is unspecified, and one reading produces a deadlock. |  |
| RT-X-005 | MINOR | file SPEC; section 4.1; lines 187-187; quote "This section specifies the `full` method profile (Section 5.6)." | The full-only sentence is placed inside heading 4.1, not under the Section 4 heading as in Sections 6 to 10, leaving its scope ambiguous. |  |
| RT-X-006 | MINOR | file SPEC; section 22.2; lines 2227-2227; quote "`error`: the operation could not be carried out; nothing was written, and `changed` is `false`." | Section 22.2 declares only two result and changed combinations invalid, leaving an error result with changed true unaddressed by that sentence. |  |
## Requestor notes

- The Requestor checked the format of each report and whether each reference resolves in the pinned text; it did not assess whether any finding is correct.
- Independence rests on the reviewer's different product, vendor and model, on separate sessions that share no context with the Requestor, and on the reviewer's own statement of identity in each report; the repository cannot show more.
- A finding's severity is the reviewer's; only the repository owner dispositions a finding.

This note is evidence only. It does not change the reviewed file.
