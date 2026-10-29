# Independent review, round 5: proposed normative method specification

- Independent review: reported
- Owner dispositions: recorded in the review disposition record
- Blocking findings: 1

## The text reviewed

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `3c0f689e2464b3a9fc8fcce5c1fc7ef55e06bfd1` |
| Reviewed SHA-256 | `09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704` |
| Line count | `4898` |
| Diffstat | `1 file changed, 3529 insertions(+), 53 deletions(-)` |
| Commits touching the file | `59` |
| Owner approval record | `.planning/reviews/2026-10-28-normative-spec-fix-round-5-approval-record.md` |
| Owner approval record blob | `1dd1c6a9db034c7d77999fd2e3f903d5a891e0a6` |
| Run set | `196dfab7a957` |
| Consent question | `May I send the test run and the six review passes RG-A, RG-B, RG-C, RG-D, RG-E and RG-X (run set 196dfab7a957, model swe-2-medium) to Devin now? Sending cannot be undone, and no run is repeated without asking you again.` |
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
| RG-A | The header and sections 1 to 8 |
| RG-B | Sections 9 to 22 |
| RG-C | Section 23 |
| RG-D | Section 24 up to the end of 24.5 |
| RG-E | Sections 24.6 to 24.10 and section 25 |
| RG-X | The whole text, read across sections |

## Reports

Each report is quoted whole, line by line: a quote mark and a space are added at the start of each line, and an empty line becomes a quote mark alone. The only change made to a report is mechanical: line endings are converted to LF and each tab to four spaces.

### RG-A — The header and sections 1 to 8

> REPORT BEGIN RG-A
> IDENTITY: Devin, an interactive command line agent by Cognition, powered by SWE-2 Medium; I share no session, prompt, notes or model with Claude Code.
> INPUT SPEC.md 09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RG-A, the header and sections 1 to 8 of SPEC.md, from the header up to but not including the heading of section 9
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5
> FINDINGS: 6
> FINDING RG-A-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."
> SUMMARY: The reserved-name check compares the whole identifier, so `nul.txt` or `con.x` passes the rule yet is still a reserved device name on Windows.
> REASONING: On Windows the device names con, prn, aux, nul, com1 to com9 and lpt1 to lpt9 are reserved regardless of any extension: `nul.txt` cannot be created as a directory or file. The rule requires the whole identifier not to equal one of the reserved words and otherwise allows a dot and more characters through the pattern `[A-Za-z0-9][A-Za-z0-9._-]*` and the prohibition only on ending with `.`. An identifier such as `nul.txt` therefore satisfies the letter of the rule while defeating its stated purpose of naming a writable `specs/<change-id>/` directory, and AE-288 names only the bare reserved word case. This is a protection that can be bypassed in the sense of check C4.
> DISPOSITION REQUIRED: Fix the rule so the reserved-name test applies to the base name before the first dot (or forbids a dot after a reserved word), or the owner dispositions the finding.
> FINDING RG-A-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 4.3; lines 309-309; quote "A `core` change (Section 23.1) always has a state document, and it keeps its documents in this layout:"
> REFERENCE: file SPEC; section 4.3; lines 319-319; quote "`review.md` and other review files are conditional, they are not documents of the change"
> SUMMARY: The `core` layout lists `review.md` inside the documents a change keeps, while the next paragraph says `review.md` is conditional and not a document of the change.
> REASONING: The layout under "keeps its documents in this layout" shows four entries including `review.md`, which reads as though `review.md` belongs to the mandatory layout, yet the following text states it is conditional and not a document of the change. The two statements can be reconciled by reading the layout as a directory listing rather than a list of documents, but the wording invites a conforming reader to treat `review.md` as a required document.
> DISPOSITION REQUIRED: Clarify that the layout shows possible directory contents, or mark `review.md` as conditional in the layout.
> FINDING RG-A-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 8.3; lines 891-891; quote "Reject without any partial mutation of persisted state when the precondition is not satisfied. When DoF finds a fail condition of the severity `hard` active, close the change as failed"
> SUMMARY: For `wait`, the outcome is unspecified when a hard DoF condition is active but no DoW condition is active: the precondition fails yet the fail clause fires.
> REASONING: The `wait` row's precondition is "A DoW condition is active" and rejection applies "when the precondition is not satisfied", while the same cell directs that an active hard fail condition closes the change as failed. When a hard fail condition is active but no wait condition is, the text does not state whether the action is rejected or closes the change; the blocked-results table adds only that "no DoW condition is active" is a `rejected` case. An implementer cannot determine the outcome from this section alone; Section 24.7's evaluation order suggests DoF first, but the row does not say so.
> DISPOSITION REQUIRED: Clarify whether a `wait` request with an active hard fail condition and no active DoW condition is rejected or closes the change as failed.
> FINDING RG-A-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 8.3; lines 1019-1019; quote "and a second such change that also has an active Definition of Fail condition"
> SUMMARY: AE-244 does not give the severity of the active DoF condition, but only a hard condition determines failure under Section 24.7.
> REASONING: The example concludes that a change with an authorized cancellation and "an active Definition of Fail condition" ends `closed`/`failed` "because the Definition of Fail has first priority". Under the new severity model a soft fail condition does not determine failure; it pauses for a human disposition, and per Section 8.4 only a DoF that "determines that the change has failed" yields `failed` rather than `cancelled`. As written, the example's outcome follows only if the condition is `hard`, which is not stated; a reader applying it to a soft condition would reach the wrong result.
> DISPOSITION REQUIRED: State the severity `hard` in the Given clause of AE-244, or extend the example to cover the soft case.
> FINDING RG-A-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 7.1; lines 795-795; quote "and later a move of the change from the specify phase directly to the build phase is requested"
> SUMMARY: In AE-235 the second request is described as a move "from the specify phase" although the same change has just advanced to the plan phase.
> REASONING: The example first has `complete` advance the change from specify to plan, then describes a later move "of the change from the specify phase directly to the build phase". At that point the change is in plan, not specify, so the described source state cannot occur for the same change. The intended point (that skipping the plan phase is not permitted) is clear, but the example does not follow from its own sequence of events.
> DISPOSITION REQUIRED: Rephrase the second leg, for example as a separate change in the specify phase requesting a direct move to build.
> FINDING RG-A-006
> SEVERITY: INFO
> REFERENCE: file BASE; section 8.3; lines 514-514; quote "wait when the new corrective scope's DoW determines a pause"
> REFERENCE: file SPEC; section 8.3; lines 908-908; quote "or a Definition of Wait condition of the new corrective scope is active"
> SUMMARY: BASE let `reopen` wait on an active DoW of the new corrective scope; SPEC now rejects in that case, consistent with the new `blocked`/`rejected` contract but a real behavior change.
> REASONING: The BASE `reopen` rejection clause ended "wait when the new corrective scope's DoW determines a pause". SPEC removes the wait outcome and lists an active DoW of the new corrective scope under `rejected`, matching AE-296 and the general rule of Section 24.2 that `reopen` of the `full` profile is rejected when a gate cannot be evaluated or would wait. This appears deliberate and internally consistent, and is recorded here so the owner is aware of the behavior change for reopening changes whose corrective scope would have to wait.
> DISPOSITION REQUIRED: None; owner awareness only.
> CHECKS PERFORMED:
> C1: I compared all changed normative statements in sections 1 to 8 for internal consistency and found no outright contradiction; I found the unspecified `wait`/hard-DoF outcome of finding RG-A-003 and the layout wording tension of finding RG-A-002.
> C2: I traced decisions O-1 through O-11 to the text in range: method profiles and `full` specified-but-not-built (O-1, O-8, Section 5.6), four implemented layers for `core` (O-10, Section 5.3), JSON state (O-4, sections 4.3 and 8.1), `blocked` as a fourth result (O-5, Section 8.3), `reopen` marked `full` only (O-6, sections 8.3 and 8.4), protections referenced as shared invariants (O-9). No decision in range is contradicted or left without corresponding text.
> C3: In range, requirements touched are SPEC-01 (gate definitions fixed, referenced in 3.3 and enforced via `gates-changed`), SPEC-02 (three-valued results in 8.5), SPEC-03 (`blocked` per-action table in 8.3), SPEC-06 (scope referenced in 6.1 and 10.6), SPEC-12 (Section 5.6), SPEC-14 (full-only markings and acceptance examples for `full` rules), SPEC-15 (`state.json` and JSON examples), SPEC-16 (six-layer resolution with `core` on four layers), SPEC-17 (`reopen` `full` only). I found no in-range contradiction or missing content these requirements demand.
> C4: I looked for bypassable rules and found the reserved-name bypass of finding RG-A-001 and the precondition-ordering ambiguity of finding RG-A-003; other new rules (no-weakening check, identifier syntax, assurance neutralization) state their failure behaviour.
> C5: I checked every new acceptance example in range against its rule; findings RG-A-004 and RG-A-005 report the two examples whose stated outcome does not fully follow from or match their own narrative.
> C6: I searched the range for references to development artifacts, prototype identifiers, decision or requirement identifiers, tool names outside the method, and local paths, and found none; the AE-nnn identifiers are the specification's own acceptance-example numbering.
> C7: I compared BASE to SPEC for removed or relaxed protections: the `silently` dropped from "MUST NOT weaken" is compensated by the explicit strengthening rule in Section 5.3, the `reopen` wait-to-reject change is recorded as finding RG-A-006, the `fail` source was tightened, and I found no protection weakened without being said.
> C8: I checked new cross-references (Sections 16.1, 16.4, 16.5, 22.2, 23.1, 23.3, 23.4, 23.7, 24.1 to 24.9, 25.1) against the document's heading structure and the term `compliance profile` versus `method profile` and found no wrong number and no term used before its definition.
> LIMITS: I verified hashes with sha256sum and compared BASE and SPEC with diff plus targeted reads; I did not execute anything else and opened no file outside the working directory. Sections 9 to 25 were consulted only as needed to judge the in-range text (for example the definitions of `gates-changed` and the layer terms in Sections 23 to 25); the per-action coverage of `gates-changed` beyond `supersede` is stated globally in Section 24.1, which I read only to that extent.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RG-A

### RG-B — Sections 9 to 22

> REPORT BEGIN RG-B
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the SWE-2 Medium model; shared session, prompt, notes or model with Claude Code: no.
> INPUT SPEC.md 09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RG-B, SPEC.md sections 9 to 22, from the heading of section 9 up to but not including the heading of section 23.
> COVERAGE: 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4
> FINDINGS: 4
> FINDING RG-B-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 12; lines 1493-1495; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition"
> REFERENCE: file SPEC; section 12.1; lines 1511-1511; quote "A retry limit is a soft fail condition (Section 24.7)."
> SUMMARY: The rule that a retry limit is a soft fail condition is stated three times in Section 12 with near-identical wording, inviting drift.
> REASONING: Lines 1493 and 1495 of the Section 12 preamble say the same thing twice (that reaching a retry limit pauses the flow for a human disposition and does not end it by itself), and line 1511 in Section 12.1 repeats the rule a third time. The statements agree, so there is no contradiction, but triple restatement of one normative rule is redundant wording that a later edit could leave inconsistent.
> DISPOSITION REQUIRED: Fix by keeping one statement of the rule and a single cross-reference, or clarify why the repetition is intended.
> FINDING RG-B-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 11.2; lines 1458-1458; quote "The fields of the template are `reason`, `outstanding` (the outstanding information or decision), `owner` (the responsible person or source), `resume_when`, `safe_state`, and `next_action`."
> SUMMARY: Section 11.2 says the fields of the wait template are six, but the template above has eight fields, including status and resume_at.
> REASONING: The sentence enumerates exactly six names as "the fields of the template", while the template at lines 1446-1455 also contains `status` and `resume_at`. The following sentences do describe `resume_at` and `status`, so the information is recoverable, but the closed enumeration is factually incomplete and could mislead an implementer about which fields the record holds. A conforming participant is unlikely to act differently, hence MINOR.
> DISPOSITION REQUIRED: Clarify the wording, for example by listing all eight fields or by saying the six named fields are the wait-record fields within the entry.
> FINDING RG-B-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 10.1; lines 1256-1258; quote "the duplicate is dispositioned through the `cancel` action and does not satisfy the Definition of Done for forward advancement"
> SUMMARY: AE-260 uses the `cancel` action for a duplicate without establishing the authorized cancellation decision that Section 8.3 requires.
> REASONING: The transition table of Section 8.3 gives `cancel` the precondition that an authorized cancellation decision exists. The example's Given records only that the second request is a duplicate of an existing change; no authorized decision is stated. The conclusion still follows if one assumes the routing disposition implies the authorization, so the example does not contradict its rule, but it leaves a precondition implicit while other examples (for instance AE-316) spell out authorization explicitly.
> DISPOSITION REQUIRED: Clarify the example by stating the authorized cancellation decision in the Given, or state that the recorded duplicate disposition itself constitutes the authorization.
> FINDING RG-B-004
> SEVERITY: INFO
> REFERENCE: file BASE; section 12.1; lines 785-785; quote "- exceeding hard budget, cost, or retry limits,"
> REFERENCE: file SPEC; section 12.1; lines 1505-1505; quote "- exceeding a hard budget or cost limit,"
> SUMMARY: BASE listed exceeding retry limits among typical fail categories; SPEC moves retry limits to soft failures, disclosed in the text itself.
> REASONING: BASE Section 12.1 named retry limits in the same category list as hard budget and cost overruns, under a section whose obligation is to terminate unsuccessfully. SPEC removes retry limits from that list and expressly states, twice, that a retry limit is a soft fail condition that pauses the flow for a human disposition, consistent with the hard/soft model that Section 24.7 introduces and with the bounded override it defines. Because the change is disclosed and follows the new model rather than silently relaxing a MUST, this is recorded as an observation for the owner rather than a weakening defect.
> DISPOSITION REQUIRED: Owner awareness only; no change required unless the owner intended retry limits to remain potential hard failures.
> CHECKS PERFORMED:
> C1: I read sections 9 to 22 of SPEC in full and compared each changed statement with its neighbours and with the transition table of 8.3 and the envelope of 22.2; the results blocked, rejected, success and error, the actions that may answer blocked, and the phase identifiers used in the wait template are mutually consistent, and no contradiction or undeterminable rule was found.
> C2: Within this range, O-4 is implemented by the JSON wait template of 11.2 and the state.json wording, O-5 by the four-result envelope of 22.2, O-7 by the migration and schema-version operation of 22.1 and the refusal codes of 22.2, and O-11 by the verify-only guard action of 22.4; no decision is contradicted by this range.
> C3: SPEC-03 (the blocked result and the rejected and blocked invariants) is satisfied by 22.2 and 22.3, the in-range parts of SPEC-08 and SPEC-09 are reflected in 11.1, 12, 9.5, 10.4 and 20, and SPEC-12, SPEC-15, SPEC-17 and SPEC-18 are partially served here; none of the requirements is contradicted by this range.
> C4: The guard action of 22.4 is verifiable from outside through its result and stable issue codes, it forbids executing the change's own commands, and a missing state document degrades to a rejected result rather than silent acceptance; no untestable rule or letter-satisfying bypass was found in this range.
> C5: The new examples AE-260 to AE-270, AE-287, AE-311 to AE-319 and AE-303 to AE-306 follow from their stated rules; AE-260 leaves the cancel precondition implicit (finding RG-B-003) and AE-265 understates the hard-failure consequence while still naming it, which I judged acceptable.
> C6: No development artifacts, prototype identifiers, decision or requirement identifiers, or local paths appear in the changed text of this range; section 14.2 names products such as Claude Code, Codex and Devin, but that text is unchanged from BASE and explicitly marked non-normative.
> C7: BASE's rule that open questions may be answered or explicitly accepted was tightened to all answered; the retry-limit reclassification is the only relaxation and it is disclosed (finding RG-B-004); no other BASE protection in this range was removed or made conditional.
> C8: Cross-references to Sections 5.6, 7, 8.3, 16.1, 16.4, 22.2, 23.2, 23.4, 23.6, 23.7, 24.1 to 24.10 and 25.1 were checked against the headings and tables they name; all resolve correctly, and terms such as blocked, assurance level, allowed path list and soft failure are used consistently with their definitions.
> LIMITS: I used the Read, Grep and sha256sum tools only, on the four input files plus this brief; I opened no file outside the working directory except the system overflow copy of my own diff output. Text outside sections 9 to 22 (notably Sections 23 to 25 that this range cites) was read only as far as needed to judge changed text, so defects located wholly in those sections are out of scope for this pass.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RG-B

### RG-C — Section 23

> REPORT BEGIN RG-C
> IDENTITY: Devin CLI, Cognition, model SWE-2 Medium; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RG-C, Section 23 of SPEC.md (from heading 23 up to, not including, heading 24)
> COVERAGE: 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7
> FINDINGS: 2
> FINDING RG-C-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 23.4; lines 2649-2649; quote "`replaced_by` names a different change that exists"
> SUMMARY: The supersede precondition accepts a closed change as replaced_by, so a change can be superseded into a dead end.
> REASONING: The `supersede` action requires only that `replaced_by` names "a different change that exists", and the rejected-results row lists only a missing value, a self-reference, a nonexistent change, and differing gate definitions as grounds for rejection. Nothing requires the replacement change to be non-closed, or open to carrying the work forward. A participant could supersede change A by a change B that is already `closed` (with any outcome, including `failed` or `cancelled`), ending A as `cancelled` while its recorded replacement can never perform work, since a `closed` change is final (Section 23.2) and `core` has no `reopen`. By contrast `follows` carefully requires a `closed` target, showing the text knows how to constrain the state of a named change when the state matters. The omission defeats the evident purpose of `replaced_by` as a pointer to replacement work; whether an implementer must reject a closed replacement cannot be determined from the text.
> DISPOSITION REQUIRED: Clarify or fix: state whether `replaced_by` must name a change that is not `closed` (or define which states are legal), and adjust the precondition and the rejected-results row accordingly, or the owner may decide the wider reading is intended.
> FINDING RG-C-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.3; lines 2577-2579; quote "Covers: Section 12.2"
> SUMMARY: Acceptance example AE-271, placed in Section 23.3, declares "Covers: Section 12.2" although it exercises the rule stated in 23.3.
> REASONING: AE-271 tests that a `core` fail gate holding only an `id`, a `severity`, and a condition is valid. That rule is stated in Section 23.3 ("A `core` fail gate holds an `id`, a `severity`, and a condition") and the corresponding exemption from Section 12.2 is stated in the table of Section 5.6; Section 12.2 itself contains no `core` rule. Every other acceptance example in Section 23 names the 23.x subsection it illustrates. The mismatched Covers line is a wrong cross-reference that can mislead coverage tracing, though it cannot change conforming behavior.
> DISPOSITION REQUIRED: Fix: change the Covers line of AE-271 to Section 23.3 (or to Sections 5.6 and 23.3, matching the convention used elsewhere).
> CHECKS PERFORMED:
> C1: Read Section 23 in full and checked its rules against each other (states vs. transition table vs. evaluation order vs. wait records vs. base gates). The open/closed, waiting, and fail paths are mutually consistent; the only undeterminable outcome found is the closed-`replaced_by` case of RG-C-001.
> C2: Traced the decisions that touch Section 23: O-1 and O-8 (both profiles, core built) via Section 5.6 and the section header; O-4 (`state.json`, engine-owned) in 23.1 and the no-hand-edit rule; O-5 (`blocked` result) in the rejected/blocked table and its `changed` values, consistent with 22.2; O-6 (no `reopen` in core) at 23.4; O-9 (protections for both profiles) via the Section 24 references; O-10 (four-layer resolution, base gates not weakenable) at 23.7. No decision is contradicted.
> C3: Checked the requirement text that Section 23 must carry: SPEC-03 (rejected vs. blocked semantics) holds in the second 23.4 table and examples; SPEC-06 (scope hard failure) via the base gate of 23.7; SPEC-08 (hard vs. soft failure, override with bounded attempts) via 23.3, 23.4 (`fail`, `approve` target `override`), and 23.6; SPEC-09 (questions block approval and closure) via the `approve` precondition and the unanswered-question base gate; SPEC-10 (evidence gate) via the incomplete-evidence base gate; SPEC-12 and SPEC-17 (two profiles, no core `reopen`) hold. No in-scope requirement text is missing or contradicted.
> C4: Looked for untestable rules and bypasses: human-only actions are listed, `cancel` still yields `failed` under an active hard fail, a closed change is final, evaluation-created waits are fully specified, and the fail-gate wait kind gates the `fail` action. The one gap is that `replaced_by` need not name a live change (RG-C-001).
> C5: Checked each acceptance example in the range (AE-09 to AE-58, AE-215, AE-216, AE-271 to AE-320) against its rule; all follow from and match the rules they name; the only defect is the wrong Covers line of RG-C-002.
> C6: Section 23 cites only internal section numbers, field names, issue codes, and AE example identifiers, all part of the method's own apparatus; no development artifacts, prototype identifiers, decision or requirement ids, foreign tool names, or local paths appear.
> C7: BASE.md ends at Section 22 and contains no Section 23, so the whole section is new text; no BASE protection in scope was removed or relaxed. The exemptions from Sections 11.2 and 12.2 are stated openly in 23.2, 23.3, and 23.5.
> C8: Verified cross-references used in Section 23 against SPEC headings: 3.1, 3.7, 3.9, 4.1, 4.3, 5.1, 5.3, 5.6, 6, 7, 9, 10, 11.1, 11.2, 12.2, 14.5, 22.3, 22.4, 24.1 to 24.9, 25.1, and 25.3 all exist and carry the content cited. Terms (`base revision`, `wait record`, `predicate`, `sign-off`) are defined before or at use. One wrong Covers reference found (RG-C-002).
> LIMITS: Text outside Section 23 (notably Sections 24 and 25) was read only as far as needed to judge Section 23's references and is covered by other passes; I did not verify examples or rules located there beyond those references. Tools used: Read, Grep, Glob-equivalent listing, and single permitted commands `sha256sum`, `wc`, `grep`, `sed`. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RG-C

### RG-D — Section 24 up to the end of 24.5

> REPORT BEGIN RG-D
> IDENTITY: Devin CLI, Cognition, SWE-2 Medium; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md 09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RG-D, section 24 of SPEC.md up to but not including heading 24.6 (lines 3153-4003)
> COVERAGE: 24, 24.1, 24.2, 24.3, 24.4, 24.5
> FINDINGS: 1
> FINDING RG-D-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24; lines 3196-3196; quote "See AE-249, AE-250, AE-251, AE-252, AE-253, AE-254, AE-255, AE-256, AE-257, AE-258, AE-259, AE-286."
> REFERENCE: file SPEC; section 24; lines 3238-3238; quote "**AE-294 — Full: the scope is evaluated from the first approval of the gate definitions**"
> SUMMARY: Example AE-294 stands inside the section 24 example block but is missing from the See list that enumerates that block.
> REASONING: The See line at line 3196 enumerates the acceptance examples that follow it in the section 24 introduction (AE-249 to AE-259 and AE-286). AE-294 is placed physically inside that same block, between AE-253 and AE-254, yet is absent from the list. AE-294 is cited by Section 24.5 (line 3892), so the example is not orphaned, but the enumeration of the block is incomplete, which is a defect of reference and structure that cannot change conforming behavior.
> DISPOSITION REQUIRED: Fix by adding AE-294 to the See list at line 3196, or move the example next to the Section 24.5 text it covers.
> CHECKS PERFORMED:
> C1: I read all of sections 24, 24.1, 24.2, 24.3, 24.4 and 24.5 and traced their terms (results, wait kinds, wait categories, anchor, base revision, allowed path list, check-command gate, override, blocked) across sections 8.3, 8.4, 8.5, 9.6, 10.7, 11.1, 11.2, 22.1 to 22.4, 23.1 to 23.7, 24.6 to 24.10 and 25.1; I found no statement that cannot hold together with the rest; the group-evaluation short-circuit of 24.2 is internally consistent because the text states that an unevaluated gate cannot outrank an evaluated one.
> C2: I traced decisions O-3 (levels and signed-approval statement normative, verifiers optional: section 24.3), O-5 (result blocked: section 24 intro and the realization table), and O-9 (protections as invariants of both profiles: the realization table and the full acceptance examples AE-249 to AE-259, AE-286 and AE-294); each is implemented as chosen and none is contradicted in this range; O-1, O-2, O-4, O-6, O-7, O-8, O-10 and O-11 touch this range only through the profile realization table and are consistent with it.
> C3: In this range I verified SPEC-01 (section 24.1: frozen gate definitions, all operations blocked except cancel and re-approval), SPEC-02 (24.2: three results, not_evaluable never a failure and never counted), SPEC-04 (24.3: A0 to A2, normative statement with operation, change, history position, signer and approved content, optional verifiers, agent-as-human statement), SPEC-05 (24.4: consistency distinct from completeness, anchor or equivalent where A2 is required), and SPEC-06 (24.5: allowed path list measured against the base revision, violation a hard failure, isolation from unrelated uncommitted work); all are satisfied by normative text; SPEC-03, SPEC-07 to SPEC-18 concern sections outside this range and were consulted only where this range cites them.
> C4: I checked that the protections can be tested from outside and looked for letter-of-the-rule bypasses: fail-closed verification at A0, the exemption of only cancel and re-approval from the hash comparison, the anchor rules with their stated limit against an actor who can write both, the exemption of only named record files from scope, and the counting of user-level ignore settings as non-applied; I found no bypass and no unspecified failure behavior; a new ignore file inside the repository is itself a changed path, which closes the obvious scope-evasion route.
> C5: I checked each acceptance example in the range (AE-60, AE-75 to AE-86, AE-249 to AE-259, AE-61 to AE-74, AE-125 to AE-136, AE-137 to AE-146, AE-147 to AE-157, AE-249 block again for full, AE-280, AE-282, AE-289, AE-294, AE-298, AE-300, AE-303 to AE-310 where cited, AE-309, AE-310) against its rule; each follows from its rule and covers the case it names.
> C6: The range cites no development artifacts, prototype identifiers, decision or requirement identifiers, tool names outside the method, or local paths; AE-n identifiers are the specification's own acceptance-example convention; mentions of a .gitignore file occur only as examples of a generic ignore file.
> C7: Section 24 is entirely new text (BASE.md ends at section 22.3); I compared the range against BASE sections 8.3, 8.4, 8.5, 11.1, 11.2, 12.2 and 22.2 for removed or relaxed protections and found none weakened in this range; the added gates-changed rejection on supersede and the blocked result strengthen rather than relax the base rules.
> C8: I verified every cross-reference in the range: sections 4.3, 5.1, 5.4, 5.6, 8.3, 8.5, 9.6, 10.7, 11.1, 12.2, 16.1, 20, 22.1, 22.2, 22.4, 23.1 to 23.7, 24.5 to 24.10, 25.1, 25.2 and 25.3 exist and say what this range attributes to them; the only defect found is the missing AE-294 citation reported as finding RG-D-001; no term is used before its definition.
> LIMITS: I did not verify the SHA-256 test vectors inside examples (for instance the digest stated in AE-183) and did not execute any gate semantics; tools used were the Read, Grep and file-writing tools plus single sha256sum, wc, ls and grep commands allowed by the brief; I opened no file outside the working directory.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RG-D

### RG-E — Sections 24.6 to 24.10 and section 25

> REPORT BEGIN RG-E
> IDENTITY: Devin, Cognition, model SWE-2 Medium; shares no session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RG-E, sections 24.6 to 24.10 and section 25 of SPEC.md, from the heading of 24.6 up to the end of the file
> COVERAGE: 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 4
> FINDING RG-E-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.8; lines 4249-4249; quote "`answerer`: the participant that gave the answer."
> SUMMARY: The `answerer` field does not state that it is absent while the question is unanswered, unlike `answer`, leaving record shape ambiguous.
> REASONING: The field list defines `answer` as "absent while the question is unanswered" but gives no parallel rule for `answerer`. A record could plausibly be written with a present-but-null `answerer` or with the field omitted, and the text does not decide which is conforming. The effect is limited to the shape of stored state, not to behavior.
> DISPOSITION REQUIRED: Clarify that `answerer` is absent until an answer is recorded, matching the rule for `answer`.
> FINDING RG-E-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.3; lines 4794-4794; quote "It takes the file and optionally a target version, which is a supported version that is higher than the version of the file"
> SUMMARY: The rejection behavior for an explicit migrate target that is not a supported version higher than the file's version is unspecified.
> REASONING: The text defines the valid case for a target version and covers the case where the file already has the target or a higher version (rejected). It does not state what happens when a caller supplies a target that is unsupported, or supported but lower than the file's version. General rejection rules arguably cover it, but the failure behavior is not stated for this parameter.
> DISPOSITION REQUIRED: State that an invalid target version is rejected, or cite the general rejection rule that applies.
> FINDING RG-E-003
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.10; lines 4455-4455; quote "The interpreter that the project configuration names is not part of the gate definitions and is not frozen (Section 24.1)"
> SUMMARY: The interpreter behind `@interpreter` is explicitly unfrozen, so a project-configuration change alters what runs without triggering the frozen-gates protection.
> REASONING: Section 24.1 freezes gate definitions, but the configured interpreter is exempted by design, and the text discloses that what stands behind the token decides whether gates pass. The record naming the program that ran (via `gate_detail`) provides traceability. This is a deliberate, documented trust trade-off, not a hidden bypass, and it satisfies the SPEC-11 duty to make the interpreter explicit and opt-in.
> DISPOSITION REQUIRED: None required; the owner may wish to confirm the trade-off is acceptable.
> FINDING RG-E-004
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.6; lines 4014-4014; quote "when no failure identifier can be extracted, or when the output cannot be read, the result is `not_evaluable`"
> SUMMARY: A failing command whose output yields no extractable failure identifier is `not_evaluable`, so a genuinely new failure with unparseable output produces a wait, not a failure.
> REASONING: When the exit map yields `not_satisfied` but no failure identifier can be extracted, the result is `not_evaluable`. This is conservative (a wait, not silent satisfaction) and internally consistent with AE-89, but it means a real regression hidden by unparseable output pauses the change rather than failing it. Noted as an observation only.
> DISPOSITION REQUIRED: None required; behavior is consistent and safe-by-default.
> CHECKS PERFORMED:
> C1: Checked internal consistency of 24.6 to 24.10 and 25: baseline set semantics, hard/soft failure rules, question answer rules, evidence completeness, canonical form, hashing, locking, and schema-version rules are mutually consistent; the only ambiguity found is the `answerer` field absence (RG-E-001) and the unspecified invalid migrate target (RG-E-002).
> C2: Traced O-4 (state.json JSON with canonical form, implemented in 25.1), O-5 (`blocked` result, used in 24.7/24.8 and restricted in 25.1 entry `result`), and O-7 (schema_version plus explicit migrate, implemented in 25.3); all implemented as chosen and none contradicted in this range. O-1, O-2, O-3, O-6, O-8, O-9, O-10, O-11 have no contradicting text in this range; protections are stated for both profiles per O-9.
> C3: Verified SPEC-07 (baselines, 24.6), SPEC-08 (hard/soft failure with bounded override lapsing on amendment, 24.7), SPEC-09 (questions as state blocking approval and closure, 24.8), SPEC-10 (executable requirement-bound evidence, 24.9), SPEC-11 (opt-in interpreter and the stated git-ignored-code consequence, 24.10), SPEC-15 (state.json canonical form, 25.1), and SPEC-18 (schema_version refusal and explicit migrate, 25.3); all satisfied in this range. No required content missing.
> C4: Examined bypass potential: baselines are frozen with gate definitions (24.6, AE-96); overrides are bounded, reasoned, and lapse on amendment (24.7); acceptance by silence is excluded (24.8); evidence commands are frozen (24.9, AE-169); the interpreter and ignored-code gaps are disclosed consequences with recorded detail (24.10); lowered schema versions are detected by the latest-recorded-version check (25.3, AE-211); atomic writes and version-checked locking are specified (25.1). No unspecified failure behavior beyond RG-E-002.
> C5: Walked acceptance examples AE-87 to AE-110, AE-158 to AE-170, AE-171 to AE-182, AE-183 to AE-214, AE-279, AE-281, AE-283 to AE-285, AE-301, AE-302, AE-320 against their rules; all follow from the rules they name and cover the stated cases. The stated digest values in AE-183 and AE-184 could not be recomputed (see LIMITS).
> C6: Found no citations of development artifacts, prototype identifiers, decision or requirement identifiers, foreign tool names, or local machine paths in the range; file names used (state.json, state.json.tmp, state.json.lock, .ggsad/config.yaml) are method-defined artifacts.
> C7: BASE.md ends at section 22 and contains no counterpart to sections 24.6 to 24.10 or 25; all in-scope text is new, so no BASE protection, MUST, SHOULD, or prohibition in this range is removed, relaxed, or made conditional.
> C8: Verified cross-references from the range: code-point comparison points to the Section 24 preamble (line 3166) and Section 25.1 (line 4554); wait kinds `question`, `fail-gate`, `external` exist in Section 23.5; `migrate`, `ask`, `answer`, `approve`, `adopt` are defined in Sections 22.1 and 25.3; Sections 8.3, 8.4, 8.5, 10.7, 11.1, 11.2, 12.2, 16.1, 20, 22.2, 23.1 to 23.7, and 24.1 to 24.5 exist and support the citations. No wrong section or example numbers found in the range.
> LIMITS: SHA-256 values were computed with sha256sum for all four inputs and match the expected values in BRIEF.md. The literal digest values asserted in AE-183 and AE-184 were not recomputed, because the permitted commands cannot hash an arbitrary byte string without a pipe or redirect; they were judged structurally consistent instead. Sections outside 24.6 to 25 were read only as far as needed to judge changed text (preamble of 24, 24.1, 24.2, 23.3 to 23.5, 22.1, 22.2, 8.x, 12). No file outside the working directory was opened. Tools used: read, exec (sha256sum, ls, wc, grep), glob not needed.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RG-E

### RG-X — The whole text, read across sections

> REPORT BEGIN RG-X
> IDENTITY: Devin, an interactive command line agent by Cognition, powered by the SWE-2 Medium model; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md 09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RG-X, the whole text read across sections, from the header to the end of SPEC.md
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 24, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 5
> FINDING RG-X-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 23.7; lines 3110-3110; quote "which is active only if `spec.md` was approved at least once and its content hash differs from the content hash that was approved last"
> REFERENCE: file SPEC; section 23.4; lines 2641-2641; quote "the specification is approved when the compliance profile or the project configuration requires it"
> SUMMARY: A `core` change whose project never requires spec approval can have `spec.md` silently rewritten at any time; the stale gate never activates and nothing detects the drift.
> REASONING: The specification anchor is an invariant-core element (Section 3.7) and `spec.md` is the anchor of a `core` change (Section 23.1). Its integrity is protected only by the `stale-spec-approval` base gate, which by its own definition and AE-276 is active only after at least one approval. Approval of the specification is required only "when the compliance profile or the project configuration requires it" (Section 23.4). In a project that never requires the approval, a `core` change can start and close while `spec.md` is edited freely, with no record anywhere: the frozen set of Section 24.1 covers the gate lists, the scope, and the requirement evidence commands of `change.yaml`, not the text of `spec.md`. A participant can therefore satisfy every rule in letter while the stated specification anchor bears no relation to the approved intent. The scope check does not help because `spec.md` is an exempt record file (Section 24.5). The result differs from the `full` profile, where Spec-Done always requires "the specification is approved" (Section 10.4).
> DISPOSITION REQUIRED: Fix or clarify. Either bind the approved content hash of `spec.md` whenever the specification is anchored, require its approval for every `core` change, or state explicitly that in `core` the machine-checkable anchor is `change.yaml` and `spec.md` is unprotected prose.
> FINDING RG-X-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.3; lines 4780-4780; quote "Every machine-readable file that a schema governs carries the top-level field `schema_version`."
> SUMMARY: Requirement SPEC-18 and decision O-7 say every artifact carries `schema_version`; the text limits it to schema-governed machine-readable files.
> REASONING: SPEC-18 and O-7 are worded "every artifact". Section 25.3 covers only the project configuration, integration mappings, the change definition, and the state document, and explicitly gives Markdown documents no schema version. A human-readable artifact such as `spec.md`, `plan.md`, or `evidence.md` therefore carries no `schema_version` at all. This is probably the intended scope, but it is narrower than the literal decision and requirement text, so an implementer could argue either way. No normative conflict otherwise: unknown versions are refused, migration is explicit and recorded, and O-7 is otherwise implemented.
> DISPOSITION REQUIRED: Clarify, or have the owner disposition the requirement text: state that the obligation applies to schema-governed artifacts only, or extend `schema_version` to all artifacts.
> FINDING RG-X-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.4; lines 2641-2641; quote "the specification is approved when the compliance profile or the project configuration requires it"
> SUMMARY: The `start` precondition conditions spec approval on the compliance profile, but no section states how a compliance profile requires spec approval.
> REASONING: Section 24.3 says a compliance profile reaches a minimum assurance level only through a gate or the project configuration, and no compliance profile description in Section 5.1 mentions specification approval. There is therefore no defined mechanism by which "the compliance profile requires" the approval, making this precondition's outcome undeterminable for that disjunct. The project-configuration disjunct is defined elsewhere (required levels and approval requirements), so the practical gap is small.
> DISPOSITION REQUIRED: Clarify which clause of a compliance profile, if any, makes specification approval required, or drop the compliance profile from the precondition.
> FINDING RG-X-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."
> SUMMARY: The identifier rule bans reserved base names only; `con.x` or `nul.tmp` remain legal identifiers even though they are still unusable directory names on some file systems.
> REASONING: The rule exists so the identifier can safely name the directory `specs/<change-id>/`. On systems that reserve device names, the reservation also applies to names with an extension (for example `con.txt`), so the stated protection is incomplete for its own purpose. The pattern `[A-Za-z0-9][A-Za-z0-9._-]*` also permits `..` sequences and names like `a.` variants in the middle, though not a bare `..`, so it does not allow a path escape on its own. This is an edge case and cannot change what a conforming participant does on common systems.
> DISPOSITION REQUIRED: Fix: extend the reserved-name rule to cover the first dot-separated segment, or clarify that only bare reserved names are prohibited.
> FINDING RG-X-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.3; lines 4800-4800; quote "the `migrate` operation names a change that is not `closed`"
> SUMMARY: The migration rule borrows the `core` state name `closed` for both profiles; a `full` change is in the `closed` phase, which the sentence does not cover literally.
> REASONING: `closed` is defined as a state of `core` (Section 23.2) and a phase of `full` (Section 7), never a status. The sentence "a change that is not `closed`" is readable only by resolving the term differently per profile. It is unambiguous in intent but imprecise in the term it uses, and AE-212 illustrates only `core` states. No participant behavior changes.
> DISPOSITION REQUIRED: Fix wording, for example "a change that is not `closed` (in `full`: not in the `closed` phase)".
> CHECKS PERFORMED:
> C1: Read SPEC.md in full and BASE.md in full, ran diff of both, and traced statements that interact across distant sections: evaluation order (8.5, 23.6, 24.2), blocked vs rejected per action (8.3, 22.2, 23.4), hard and soft failure (12, 23.4, 24.7), wait records (11.2, 23.5), and the frozen-set definitions (24.1, Section 24 preamble). Found no outright contradiction; the nearest tension is reported as RG-X-001 and RG-X-003.
> C2: Traced each decision. O-1: both profiles specified (5.6, 23). O-2: resolution, gate engine, and CI re-entered; memory, MCP, web UI, orchestration absent. O-3: A0 to A2 and the statement format normative, verifiers optional (24.3). O-4: `state.json`, canonical form (25.1). O-5: `blocked` fourth result (22.2). O-6: `reopen` full-only, absent in core (8.3, 23.4). O-7/SPEC-18: schema_version, refusal, explicit migrate (25.3), with the scope caveat of RG-X-002. O-8: full marked specified but not implemented (5.6, AE-08). O-9: protections stated as invariants of both profiles (24 preamble, realization table). O-10: six layers kept, core implements four (5.3, AE-226). O-11: guard verify-only, five verifications, executes nothing (22.4).
> C3: Traced SPEC-01 (24.1), SPEC-02 (24.2), SPEC-03 (22.2), SPEC-04 (24.3), SPEC-05 (24.4), SPEC-06 (24.5), SPEC-07 (24.6), SPEC-08 (24.7), SPEC-09 (24.8), SPEC-10 (24.9), SPEC-11 (24.10), SPEC-12 (5.6), SPEC-13 (not verifiable from the inputs, noted in LIMITS), SPEC-14 (24 preamble and per-rule full examples), SPEC-15 (25.1), SPEC-16 (5.3), SPEC-17 (8.3, 23.4), SPEC-18 (25.3). All have implementing text; the literal wording gap of SPEC-18 is RG-X-002.
> C4: Looked for bypasses: gate redefinition (5.3 weakening check at creation and before approval), gate edits (24.1 hash), history edits (24.4 chain and anchor), spec edits (23.7 stale gate), scope bypass via ignored files (24.5, 24.10), identity spoofing (24.3 fail-closed). One residual hole is RG-X-001; the ignored-code consequence is disclosed normatively rather than closed, which matches SPEC-11.
> C5: Sampled acceptance examples against their rules across all sections (AE-226, AE-234 to AE-237, AE-248, AE-250, AE-253, AE-275, AE-280, AE-288, AE-294 to AE-310, AE-183, AE-208 to AE-214). Each sampled example follows from its rule and names the section it covers.
> C6: Searched for prototype identifiers, commit hashes, local paths, and tool names in normative text. Only method-internal terms (`state.json`, `change.yaml`, `specs/<change-id>/`, `.ggsad/config.yaml`) and the pre-existing non-normative tool names in Sections 14.2 and 17 were found; nothing cites development artifacts.
> C7: Compared every protection-bearing passage of BASE.md with SPEC.md. BASE's retry limit as a DoF category becomes a soft fail condition, matching SPEC-08; BASE's `reopen` DoW wait becomes a rejection, which is stricter, not weaker. No MUST, SHOULD, or prohibition of BASE was found relaxed or made conditional without being stated.
> C8: Checked cross-references sampled across sections: 8.3 to 24.2 and 22.2, 5.3 to 23.7 and 24.3, 9.4/9.5/10.4 to 24.8, 10.7 to 24.6 and 24.9, 11.2 and 23.5, 16.1 to 24.5 and 24.9, 22.4 to 24.1 to 24.7, 23.4 to 24.4 and 24.5, 25.1 to 24.2 and 24.4, 25.3 to 24.4. No wrong section number found. Terms are defined before or at first normative use (`blocked` in 8.3 points to 22.2).
> LIMITS: SPEC-13 (no file under `src/ggsad/` modified) cannot be verified: no repository files were provided beyond the four inputs, and the brief restricts reading to the working directory. I did not execute or validate any acceptance example mechanically; examples were checked by reading. AE numbering gaps were noted but not exhaustively audited as a sequence. Tools used: Read, sha256sum, wc, diff. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RG-X

## Findings

| Finding | Severity | Reference | Summary | Disposition |
|---|---|---|---|---|
| RG-A-001 | BLOCKING | file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case." | The reserved-name check compares the whole identifier, so `nul.txt` or `con.x` passes the rule yet is still a reserved device name on Windows. | fix |
| RG-A-002 | MINOR | file SPEC; section 4.3; lines 309-309; quote "A `core` change (Section 23.1) always has a state document, and it keeps its documents in this layout:" | The `core` layout lists `review.md` inside the documents a change keeps, while the next paragraph says `review.md` is conditional and not a document of the change. |  |
| RG-A-003 | MINOR | file SPEC; section 8.3; lines 891-891; quote "Reject without any partial mutation of persisted state when the precondition is not satisfied. When DoF finds a fail condition of the severity `hard` active, close the change as failed" | For `wait`, the outcome is unspecified when a hard DoF condition is active but no DoW condition is active: the precondition fails yet the fail clause fires. |  |
| RG-A-004 | MINOR | file SPEC; section 8.3; lines 1019-1019; quote "and a second such change that also has an active Definition of Fail condition" | AE-244 does not give the severity of the active DoF condition, but only a hard condition determines failure under Section 24.7. |  |
| RG-A-005 | MINOR | file SPEC; section 7.1; lines 795-795; quote "and later a move of the change from the specify phase directly to the build phase is requested" | In AE-235 the second request is described as a move "from the specify phase" although the same change has just advanced to the plan phase. |  |
| RG-A-006 | INFO | file BASE; section 8.3; lines 514-514; quote "wait when the new corrective scope's DoW determines a pause" | BASE let `reopen` wait on an active DoW of the new corrective scope; SPEC now rejects in that case, consistent with the new `blocked`/`rejected` contract but a real behavior change. |  |
| RG-B-001 | MINOR | file SPEC; section 12; lines 1493-1495; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition" | The rule that a retry limit is a soft fail condition is stated three times in Section 12 with near-identical wording, inviting drift. |  |
| RG-B-002 | MINOR | file SPEC; section 11.2; lines 1458-1458; quote "The fields of the template are `reason`, `outstanding` (the outstanding information or decision), `owner` (the responsible person or source), `resume_when`, `safe_state`, and `next_action`." | Section 11.2 says the fields of the wait template are six, but the template above has eight fields, including status and resume_at. |  |
| RG-B-003 | MINOR | file SPEC; section 10.1; lines 1256-1258; quote "the duplicate is dispositioned through the `cancel` action and does not satisfy the Definition of Done for forward advancement" | AE-260 uses the `cancel` action for a duplicate without establishing the authorized cancellation decision that Section 8.3 requires. |  |
| RG-B-004 | INFO | file BASE; section 12.1; lines 785-785; quote "- exceeding hard budget, cost, or retry limits," | BASE listed exceeding retry limits among typical fail categories; SPEC moves retry limits to soft failures, disclosed in the text itself. |  |
| RG-C-001 | MAJOR | file SPEC; section 23.4; lines 2649-2649; quote "`replaced_by` names a different change that exists" | The supersede precondition accepts a closed change as replaced_by, so a change can be superseded into a dead end. |  |
| RG-C-002 | MINOR | file SPEC; section 23.3; lines 2577-2579; quote "Covers: Section 12.2" | Acceptance example AE-271, placed in Section 23.3, declares "Covers: Section 12.2" although it exercises the rule stated in 23.3. |  |
| RG-D-001 | MINOR | file SPEC; section 24; lines 3196-3196; quote "See AE-249, AE-250, AE-251, AE-252, AE-253, AE-254, AE-255, AE-256, AE-257, AE-258, AE-259, AE-286." | Example AE-294 stands inside the section 24 example block but is missing from the See list that enumerates that block. |  |
| RG-E-001 | MINOR | file SPEC; section 24.8; lines 4249-4249; quote "`answerer`: the participant that gave the answer." | The `answerer` field does not state that it is absent while the question is unanswered, unlike `answer`, leaving record shape ambiguous. |  |
| RG-E-002 | MINOR | file SPEC; section 25.3; lines 4794-4794; quote "It takes the file and optionally a target version, which is a supported version that is higher than the version of the file" | The rejection behavior for an explicit migrate target that is not a supported version higher than the file's version is unspecified. |  |
| RG-E-003 | INFO | file SPEC; section 24.10; lines 4455-4455; quote "The interpreter that the project configuration names is not part of the gate definitions and is not frozen (Section 24.1)" | The interpreter behind `@interpreter` is explicitly unfrozen, so a project-configuration change alters what runs without triggering the frozen-gates protection. |  |
| RG-E-004 | INFO | file SPEC; section 24.6; lines 4014-4014; quote "when no failure identifier can be extracted, or when the output cannot be read, the result is `not_evaluable`" | A failing command whose output yields no extractable failure identifier is `not_evaluable`, so a genuinely new failure with unparseable output produces a wait, not a failure. |  |
| RG-X-001 | MAJOR | file SPEC; section 23.7; lines 3110-3110; quote "which is active only if `spec.md` was approved at least once and its content hash differs from the content hash that was approved last" | A `core` change whose project never requires spec approval can have `spec.md` silently rewritten at any time; the stale gate never activates and nothing detects the drift. |  |
| RG-X-002 | MINOR | file SPEC; section 25.3; lines 4780-4780; quote "Every machine-readable file that a schema governs carries the top-level field `schema_version`." | Requirement SPEC-18 and decision O-7 say every artifact carries `schema_version`; the text limits it to schema-governed machine-readable files. |  |
| RG-X-003 | MINOR | file SPEC; section 23.4; lines 2641-2641; quote "the specification is approved when the compliance profile or the project configuration requires it" | The `start` precondition conditions spec approval on the compliance profile, but no section states how a compliance profile requires spec approval. |  |
| RG-X-004 | MINOR | file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case." | The identifier rule bans reserved base names only; `con.x` or `nul.tmp` remain legal identifiers even though they are still unusable directory names on some file systems. |  |
| RG-X-005 | MINOR | file SPEC; section 25.3; lines 4800-4800; quote "the `migrate` operation names a change that is not `closed`" | The migration rule borrows the `core` state name `closed` for both profiles; a `full` change is in the `closed` phase, which the sentence does not cover literally. |  |

## Requestor notes

- The Requestor checked the format of each report and whether each reference resolves in the pinned text; it did not assess whether any finding is correct.
- Independence rests on the reviewer's different product, vendor and model, on separate sessions that share no context with the Requestor, and on the reviewer's own statement of identity in each report; the repository cannot show more.
- A finding's severity is the reviewer's; only the repository owner dispositions a finding.
- Check warning: WARN RP6 RG-A: the quote of reference 8 occurs in SPEC but not between the lines 908-908

This note is evidence only. It does not change the reviewed file.
