# Independent review, round 6: proposed normative method specification

- Independent review: reported
- Owner dispositions: recorded in the review disposition record
- Blocking findings: 3

## The text reviewed

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `2acdd0b38174b6fd8e8e3df9952063c74071c22a` |
| Reviewed SHA-256 | `177bc9836133127936c19af9c4f60d076c327bd1743b67e1a875c89c5afb669e` |
| Line count | `4924` |
| Diffstat | `1 file changed, 3552 insertions(+), 50 deletions(-)` |
| Commits touching the file | `62` |
| Owner approval record | `.planning/reviews/2026-10-29-normative-spec-fix-round-6-approval-record.md` |
| Owner approval record blob | `90671e59cd1ad84e5cec3c4ae71d255b57b8370e` |
| Run set | `cbdd859d17f7` |
| Consent question | `May I send the test run and the four review passes RH-A, RH-B, RH-C and RH-X (run set cbdd859d17f7, model swe-2-medium) to Devin now? Sending cannot be undone, and no run is repeated without asking you again.` |
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
| RH-A | The header and sections 1 to 8 |
| RH-B | Sections 9 to 22 |
| RH-C | Section 23 |
| RH-X | The whole text, read across sections |

The passes RH-D and RH-E of the brief's table were not run. Their scopes (Section 24 up to the end of 24.5; Sections 24.6 to 24.10 and section 25) were read only by the cross-check pass RH-X.

## Reports

Each report is quoted whole, line by line: a quote mark and a space are added at the start of each line, and an empty line becomes a quote mark alone. The only change made to a report is mechanical: line endings are converted to LF and each tab to four spaces.

### RH-A — The header and sections 1 to 8

> REPORT BEGIN RH-A
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the SWE-2 Medium model; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md 177bc9836133127936c19af9c4f60d076c327bd1743b67e1a875c89c5afb669e
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RH-A, the header and sections 1 to 8 of SPEC.md, from the first line up to but not including the heading of section 9
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5
> FINDINGS: 2
> FINDING RH-A-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 8.5; lines 1119-1119; quote "Evaluation MUST stop as soon as a gate determines the requested action's outcome."
> SUMMARY: The flat MUST to stop as soon as one gate decides conflicts with the group-whole evaluation that Section 24.2 prescribes and that 8.5 itself cites.
> REASONING: Section 24.2 states that gates are evaluated by group and that a group is evaluated whole even when an earlier gate of the same group already decides, and the same subsection of 8.5 announces that Section 24.2 refines this order and describes the group rule. A reader of 8.5 alone still finds an unqualified MUST that is contradicted by the cited refinement. The declared refinement relationship makes the intended behaviour recoverable, so conforming behaviour does not change, but the sentence is misleading as worded.
> DISPOSITION REQUIRED: clarify; reword the sentence so that evaluation stops after the first deciding gate group, or state explicitly that Section 24.2 replaces this stopping rule.
> FINDING RH-A-002
> SEVERITY: INFO
> REFERENCE: file SPEC; section 5.3; lines 396-396; quote "or when the project configuration raises a required assurance level"
> SUMMARY: The sentence presents the project configuration raising an assurance level as a lower layer strengthening a higher layer, although the configuration is layer 3 itself.
> REASONING: The definition of strengthening is framed as an act of a lower layer on a higher layer, but the project configuration is one of the layers (layer 3), so the example does not fit the lower-to-higher direction the sentence sets up; the next paragraph separately explains that a configured higher level neutralizes a lower statement. The intent is clear from context, so this is an observation rather than a defect.
> DISPOSITION REQUIRED: owner may clarify which layers the configuration strengthens relative to, or leave the text unchanged.
> CHECKS PERFORMED:
> C1: I read the full pass range, compared each rule internally and against Sections 11.1, 22.2, 23.3, 23.7, 24.1 to 24.3, 24.7, and 25.1 that it cites, and found no contradiction besides the wording tension reported as RH-A-001; terms are used in one sense and outcomes are determinable.
> C2: I traced each owner decision to the range: O-1 is implemented by Section 5.6 defining the two method profiles, O-4 by state.json in Section 4.3 and the JSON example in Section 8.1, O-6 by the reopen row marked full only and Section 8.4, O-8 by the specified-but-not-implemented marking in Section 5.6, O-9 by the references to the shared protections of Section 24, and O-10 by the four implemented layers in Section 5.3; no decision is contradicted in this range.
> C3: I traced the requirements: SPEC-01 via Section 3.3 and the supersede gates-changed rule, SPEC-03 via the blocked column of the Section 8.3 tables, SPEC-04 via Sections 3.10 and 5.4, SPEC-06 via the Class S scope content in Section 6.1, SPEC-08 via the fail row and Section 8.4, SPEC-12 via the Section 5.6 applicability table, SPEC-14 and SPEC-15 via the profile markings and state.json, SPEC-16 via Section 5.3, and SPEC-17 via the reopen rows; none is contradicted in this range.
> C4: I checked the new gate-weakening check, the identifier rules, the exception of Section 4.2, and the transition-table rejection and blocked behaviour for testability and bypass; failure behaviour is specified for each action and no rule in the range is satisfiable in letter while defeating its purpose.
> C5: I checked every acceptance example in the range, AE-01 to AE-08, AE-121 to AE-124, AE-217, AE-218 to AE-248, AE-271 to AE-298 in part, AE-308, AE-310, AE-321, and AE-323 references, against the rule each names; each follows from its rule and covers the named case.
> C6: I searched the range for citations of development artifacts, decision or requirement identifiers, prototype names, tool names outside the method, and local paths; the text names only its own sections, files of the method, and acceptance examples, and none was found.
> C7: I compared every BASE paragraph in the range with SPEC: the changes add protections or restate them; the not-satisfied outcomes that BASE rejected are now recorded as blocked, which implements owner decision O-5, and no MUST, SHOULD, or prohibition of BASE is removed, relaxed, or made conditional without being said.
> C8: I verified the section numbers cited from the range, including Sections 11.1, 16.1, 16.4, 16.5, 22.2, 23.1 to 23.7, 24.1 to 24.9, and 25.1, and the terms core, full, blocked, not_evaluable, and the wait categories; all resolve to defined targets and no term is used before its definition without a pointer.
> LIMITS: I verified the hash of each of the four input files and read only files inside the working directory; no file outside it was opened. I used the Read and Grep tools and single plain commands sha256sum, wc, grep, and sed. Consultation of Sections 9 to 25 was limited to the passages needed to judge the range; the unchanged text of the range was compared line by line against BASE.md.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RH-A

### RH-B — Sections 9 to 22

> REPORT BEGIN RH-B
> IDENTITY: Devin, Cognition, SWE-2 Medium; I share no session, prompt, notes or model with Claude Code.
> INPUT SPEC.md 177bc9836133127936c19af9c4f60d076c327bd1743b67e1a875c89c5afb669e
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RH-B, sections 9 to 22 of SPEC.md (from heading 9 up to, not including, heading 23)
> COVERAGE: 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4
> FINDINGS: 3
> FINDING RH-B-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 12.2; lines 1527-1533; quote "required documentation"
> REFERENCE: file SPEC; section 12.2; lines 1537-1556; quote "### F-01 — Unauthorized Breaking Change"
> SUMMARY: The fail-rule template F-01 omits the mandatory element "required documentation" that the same section lists as MUST content.
> REASONING: Section 12.2 states that every fail rule MUST include trigger, required response, permitted preservation actions, final status, and required documentation, and the diff adds that every fail rule also states its severity. The template was edited in this change (a Severity block was added) yet still shows no field that carries the required documentation. A participant copying the template verbatim produces a non-conforming fail rule, and AE-269 confirms that a valid rule states "the required documentation", so the example does not follow from its rule. The omission already existed in BASE.md, but the change modifies this very template and leaves the defect in place.
> DISPOSITION REQUIRED: fix. Add a Required documentation element to the F-01 template, or clarify which part of the template carries that mandatory content.
> FINDING RH-B-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 22.1; lines 2301-2301; quote "as the read-only actions `check`, `review`, and `guard` (Section 22.4) do"
> SUMMARY: The reference "(Section 22.4)" is attached to three actions, but only `guard` is defined there; `check` and `review` are defined in Section 23.4.
> REASONING: Section 22.1 lists the reporting operations and cites Section 22.4 after naming all three read-only actions. Section 22.4 defines only `guard`; the read-only actions `check` and `review` are defined for `core` in Section 23.4 and are not described in Section 22.4 at all. A reader following the reference does not find two of the three named actions. The wording does not change any obligation, so the severity is MINOR.
> DISPOSITION REQUIRED: fix. Adjust the reference so it names Section 22.4 for `guard` and Section 23.4 for `check` and `review`, or define the read-only actions once and cite that location.
> FINDING RH-B-003
> SEVERITY: INFO
> REFERENCE: file SPEC; section 12; lines 1499-1503; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition"
> REFERENCE: file SPEC; section 12.1; lines 1519-1519; quote "A retry limit is a soft fail condition (Section 24.7)."
> SUMMARY: The rule that a retry limit is a soft fail condition is restated three times across Section 12 and 12.1.
> REASONING: Lines 1499 to 1503 explain twice that a retry limit is soft and pauses rather than terminates, and line 1519 states the same rule a third time. The repetition is consistent, not contradictory, and cannot change conformance; it is an observation about redundancy in newly added text.
> DISPOSITION REQUIRED: none; optionally consolidate the three statements into one.
> CHECKS PERFORMED:
> C1: I compared the changed sentences of sections 9 to 22 for statements that cannot hold together and for terms used in two senses. I found no contradiction; the soft/hard distinction in section 12 is explicitly carved out of the terminate obligation, and the three retry-limit restatements agree (finding RH-B-003).
> C2: I traced O-1 through O-11 into the range. Sections 9 and 10 are marked as the `full` profile (O-1, O-8); the wait template moved to JSON consistent with state format (O-4); `blocked` is a fourth normative result with `rejected`/`error` never changed (O-5, implemented in 22.2); the guard action is verify-only and never runs change commands (O-11, implemented in 22.4); integration mappings are named layer 6 and add no gate to a `core` change (O-10). No decision is contradicted and none lacks in-range text it would require.
> C3: I traced each requirement's in-range content. SPEC-03 is implemented in 22.2 and 22.3; SPEC-08 in section 12 and 12.1 (soft retry limits, hard scope violation); SPEC-09 in 9.4, 9.5, 10.4, 11.3 and 20; SPEC-10 in 15, 16.1 and 20; SPEC-12 partially (the `full` markings on 9, 10 and the `core` carve-outs in 19, 20 and 21; profile movement is specified outside the range); SPEC-14 via the acceptance examples AE-260 to AE-270 and AE-311 to AE-319; SPEC-15 via the JSON wait template. No requirement is contradicted and none is missing in-range content.
> C4: I checked testability and bypass. The blocked-result accounting, the guard's five verifications, and the wait-state field list are externally testable through the contract envelope and history. I found no protection a hostile participant could satisfy in letter while defeating its purpose within this range.
> C5: I checked each acceptance example in range (AE-111 to AE-116, AE-204 to AE-211 citations, AE-260 to AE-270, AE-287, AE-303 to AE-306, AE-311 to AE-319) against its rule. All follow from their rules; AE-115's `done` status in the build phase is legal under Section 8.2. One defect: the F-01 template example omits the mandatory required-documentation element (finding RH-B-001).
> C6: I checked for development-artifact citations. Sections 17 and 14.2 name external methods and products as explicit non-normative examples, as in BASE; no prototype identifier, decision identifier, requirement identifier, or local path appears in the changed text of this range.
> C7: I compared each protection of BASE sections 9 to 22 against SPEC. Ready-to-Plan and Spec-Done were strengthened from "answered or explicitly accepted" to all questions answered; the retry limit moved from hard to soft fail categories, which is an explicit, stated reclassification, not a silent removal; the result envelope gained a result without losing one. No protection was silently weakened.
> C8: I checked section references (5.3, 5.4, 5.6, 7, 8, 8.3, 23.2, 23.4, 23.6, 23.7, 24.1 to 24.10, 25.1, 25.3) and AE references in range; all named headings exist and the cited AEs are defined. One wrong-reference defect is finding RH-B-002.
> LIMITS: I used only the Read, Grep and Glob tools and the single commands `sha256sum` and `wc` on the four input files. I opened no file outside the working directory. Statements in sections outside 9 to 22 (for example the per-action blocked rules of Section 23.4 and the canonical form of Section 25) were consulted only to judge the in-range text, not reviewed in their own right. Whether the F-01 template omission predates this diff is noted in the finding; it is reported because the diff modifies that template.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RH-B

### RH-C — Section 23

> REPORT BEGIN RH-C
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the SWE-2 Medium model; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 177bc9836133127936c19af9c4f60d076c327bd1743b67e1a875c89c5afb669e
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RH-C, section 23 of SPEC.md, from the heading 23 up to but not including heading 24 (lines 2441-3178)
> COVERAGE: 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7
> FINDINGS: 4
> FINDING RH-C-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 23.4; lines 2656-2656; quote "The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active."
> REFERENCE: file SPEC; section 23.5; lines 3032-3032; quote "`fail-gate`: the evaluation of Section 23.6 found a soft fail condition (Section 24.7);"
> REFERENCE: file SPEC; section 24.7; lines 4130-4133; quote "The wait ends by a human disposition"
> SUMMARY: cancel and supersede close a change waiting on a soft fail as cancelled, contradicting the rule that the wait ends only by fail or override
> REASONING: Section 24.7 states that a soft failure pauses the change and that the wait ends by a human disposition which is one of exactly two: the `fail` action closing the change as failed, or a recorded override. Section 23.5 defines a wait record of kind `fail-gate` for that pause, and Section 23.4 makes `cancel` and `supersede` legal from every state except `closed`, explicitly stating that an active wait does not prevent them, and gives the outcome `cancelled` unless a hard fail condition is active. A change paused on a soft fail can therefore be closed as `cancelled` by `cancel` or `supersede` without either of the two permitted dispositions, so the wait does not end in one of the two ways the text enumerates, and a failure is recorded as a cancellation. The requirement SPEC-08 likewise names only close-as-failed and override as dispositions.
> DISPOSITION REQUIRED: Fix or owner decision: either state that `cancel` and `supersede` on a change that awaits the disposition of a soft fail condition close it as `failed`, or explicitly permit a cancellation outcome and reconcile it with Section 24.7 and SPEC-08.
> FINDING RH-C-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 23.3; lines 2576-2576; quote "`retry_limit`: a mapping with the members `gate` and `limit`, for a fail gate only."
> REFERENCE: file SPEC; section 23.3; lines 2579-2579; quote "or that names a predicate which is not listed for the kind of the gate MUST be rejected"
> SUMMARY: A wait gate whose condition holds `retry_limit` violates the fail-gate-only rule, yet no clause requires its rejection
> REASONING: Section 23.3 gives a fail gate and a wait gate a condition holding exactly one of `command`, `retry_limit`, and `predicate`, and declares `retry_limit` to be for a fail gate only. The rejection rule that follows covers a condition that holds none of the members, two or more of them, another member, or a predicate not listed for the kind of the gate. A wait gate whose condition holds only `retry_limit` matches none of those cases: `retry_limit` is one of the three named members, not another member. Whether such a definition is accepted or rejected cannot be determined from the text, and an implementation that accepts it creates a wait gate that pauses the change when a retry limit is reached, a behavior no rule defines.
> DISPOSITION REQUIRED: Fix: add a rejection clause for a wait gate whose condition holds `retry_limit`, or state how such a condition is evaluated.
> FINDING RH-C-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.4; lines 2674-2674; quote "(issue code `start-blocked`)"
> SUMMARY: The parenthetical leaves unclear whether the issue code `start-blocked` covers every rejected `start` or only gate-decided ones
> REASONING: The `rejected` column for `start` reads "The state is not `open`, or a precondition is not met, including a fail gate, a wait gate, or a gate that cannot be evaluated that would decide against the start (issue code `start-blocked`)." The parenthetical can be read as attaching the code to all rejections of `start` or only to the gate cases. Sections 24.2 and 24.7 assign `start-blocked` to the gate cases, and AE-26 records a rejection for unapproved gates without naming a code, so an implementer may report different issue codes for the same rejection.
> DISPOSITION REQUIRED: Clarify which `start` rejections carry the stable issue code `start-blocked`.
> FINDING RH-C-004
> SEVERITY: INFO
> REFERENCE: file SPEC; section 23.4; lines 2658-2658; quote "the anchor is created from the history as it is"
> SUMMARY: `adopt` is legal from any state, including `closed`, although a closed change is declared final and adoption cannot detect entries lost earlier
> REASONING: The transition table lists `adopt` as legal from any state, so it applies to a `closed` change even though Section 23.2 declares a closed change final. `adopt` changes neither state nor outcome, so no contradiction arises, but an anchor created for a closed change certifies the history only as found; Section 24.4 itself notes that adoption cannot show whether entries were lost before it. The owner may wish to confirm this is intended for closed changes.
> DISPOSITION REQUIRED: Owner awareness; optionally restrict `adopt` to non-closed states or state explicitly that adoption of a closed change is permitted.
> CHECKS PERFORMED:
> C1: Read all of section 23 and cross-checked the transition table, the rejected/blocked table, the wait-record rules and the evaluation order for consistency; found the retry-limit-on-wait-gate gap (RH-C-002) and the `start-blocked` ambiguity (RH-C-003), and the soft-fail wait versus cancel contradiction (RH-C-001).
> C2: Traced the owner decisions that touch this range: O-1 and O-8 (core specified as the built profile, four states) hold; O-5 holds (per-action rejected/blocked table present); O-6 and SPEC-17 hold (`reopen` absent from `core`, stated and exemplified by AE-48); O-10 holds (Section 23.7 and 5.3 give core four layers). No decision is contradicted or missing text in this range.
> C3: Traced the requirements that touch this range: SPEC-03 (blocked versus rejected per action) is satisfied; SPEC-09 (approval and closure blocked while a question is unanswered) is satisfied via the `approve` precondition and the `unanswered-question` base gate; SPEC-12 (core four-state model specified) is satisfied; SPEC-08 is engaged by the soft-fail wait, and finding RH-C-001 records the residual conflict.
> C4: Checked that each rule is testable and looked for bypass paths: gate validity, state transitions and outcomes are externally observable; the soft-fail pause can be ended by cancellation rather than by a disposition (RH-C-001); the retry_limit condition on a wait gate is unspecified (RH-C-002); no other bypass found in this range.
> C5: Checked every acceptance example in the range against its rule; the examples follow from the rules they cite. AE-271 names Section 12.2 in its Covers line, which is defensible because the example demonstrates the 12.2 content exemption of a core fail gate, so it is not reported.
> C6: Searched the range for development artifacts, prototype identifiers, decision or requirement identifiers, foreign tool names and local paths; none found. `specs/<change-id>/` is part of the method itself.
> C7: BASE.md ends at section 22.3, so the whole range is new text and nothing in it removes or relaxes a protection of BASE.md; the exemptions the text grants to `core` (Sections 11.2, 12.2 items) are stated openly and restated in Section 5.6.
> C8: Verified the headings cited from this range (Sections 3.1, 3.7, 3.9, 4.1, 4.3, 5.1, 5.3, 5.6, 6, 7, 9, 10, 11.1, 11.2, 12.2, 14.5, 22.3, 22.4, 23.x, 24.1, 24.2, 24.3, 24.4, 24.5, 24.7, 24.8, 24.9, 25.1, 25.3) exist and match what the citations claim; no wrong section number found. Terms used (states, outcomes, wait record kinds, base gates, results) are defined before or at use.
> LIMITS: Judgment of the transition table and evaluation order required consulting Sections 5.3, 5.6, 11.1, 11.2, 12.2, 22.3, 22.4, 24.2, 24.4, 24.7 and 25.1 outside the pass range, which were read only as context. Whether the cancellation of a soft-fail wait is intended behavior could not be determined from the text and is left to the owner. Tools used: Read, Grep, Glob-equivalent listing, sha256sum, grep, wc, head, sed, awk. No file outside the working directory was opened.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RH-C

### RH-X — The whole text, read across sections

> REPORT BEGIN RH-X
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the SWE-2 Medium model; shared session, prompt, notes or model with Claude Code: no.
> INPUT SPEC.md 177bc9836133127936c19af9c4f60d076c327bd1743b67e1a875c89c5afb669e
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RH-X, the whole text read across sections, from the header to the end of SPEC.md
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 24, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 3
> FINDING RH-X-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 25.1; lines 4552-4552; quote "The first entry of a `full` change is `new`"
> REFERENCE: file SPEC; section 25.3; lines 4828-4828; quote "The first entry of the new state document is a `migrate` entry with `n` 1"
> SUMMARY: Sections 25.1 and 25.3 contradict each other on the first history entry of a `full` change migrated from a YAML state document.
> REASONING: Section 25.1 states without qualification that the first entry of a `full` change is `new`. Section 25.3 states that a state document written earlier as `state.yaml` is migrated to `state.json` and that the first entry of that new document is a `migrate` entry with `n` 1. The only state document an earlier version of this method wrote is that of the then-only model, which is now `full`, so a migrated `full` change has a first entry that is `migrate`, not `new`. The two normative statements cannot both hold for the same change, and the closed-set rule of Section 25.1 does not resolve which governs.
> DISPOSITION REQUIRED: Fix. Qualify the Section 25.1 statement so that it applies to a change created by the `new` action, or explicitly carve out the migrated document of Section 25.3.
> FINDING RH-X-002
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 24.5; lines 3922-3922; quote "A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement"
> REFERENCE: file SPEC; section 24.5; lines 3954-3954; quote "in place at the base revision, tells version control to ignore"
> SUMMARY: The scope rule does not fix which revision of an ignore file applies, so an in-scope edit of an ignore file can hide out-of-scope work.
> REASONING: The normative rule is written in the present tense and does not state whether the ignore files that hide paths are those in place at the base revision or those present at measurement time. Only the acceptance example AE-150 mentions an ignore file in place at the base revision. Under the literal reading, a change whose allowed path list includes an ignore file inside the repository, for example `.gitignore` at the root, may edit that file so that it ignores further paths and then alter those paths without any scope violation, because ignored files are invisible to the measurement. That satisfies the letter of the scope protection while defeating its purpose of bounding what the change touches. The stated consequence in Section 24.10 covers only code that gate commands run, not the general case of hiding arbitrary files.
> DISPOSITION REQUIRED: Fix or owner decision. State in the rule which revision of the ignore files the measurement applies, for example only ignore files in place at the base revision, or state that a change may not alter an ignore file inside the repository to widen invisibility.
> FINDING RH-X-003
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 23.4; lines 2673-2673; quote "the gate definitions differ from the approved ones and the target is not the gate definitions"
> REFERENCE: file SPEC; section 24.1; lines 3336-3336; quote "the approval of the gate definitions that replaces the approved hash"
> SUMMARY: Whether an `approve` with target `all` is exempt from the frozen-gate comparison while the gate definitions differ cannot be determined.
> REASONING: Section 23.4 defines the target `all` as approving the specification and the gate definitions together, and its result table rejects an approval while the gate definitions differ when the target is not the gate definitions. Section 24.1 exempts the approval of the gate definitions that replaces the approved hash from the comparison. It is undecidable whether `all` counts as that exempt approval, because it contains the gate re-approval but also the specification approval, which is not exempt. One implementation may reject `all` and require a separate `gates` approval, another may accept it; both readings are defensible and produce different outcomes.
> DISPOSITION REQUIRED: Clarify. State whether the exemption of Section 24.1 covers the target `all`, for example by naming the exempt targets.
> CHECKS PERFORMED:
> C1: I read the full diff between BASE.md and SPEC.md and read the whole of SPEC.md across sections; I found the contradiction of finding RH-X-001, the unspecified reading of finding RH-X-002, and the ambiguity of finding RH-X-003; no term used in two senses was confirmed elsewhere.
> C2: I traced each owner decision O-1 to O-11: O-1 two profiles in Section 5.6, O-2 reversed non-goals implemented through Sections 5.3, 5.6, 22.4 and 23, O-3 normative levels and statement with optional verifiers in Section 24.3, O-4 JSON state with canonical form in Sections 4.3 and 25.1, O-5 the fourth result `blocked` and per-action tables in Sections 22.2, 8.3 and 23.4, O-6 `reopen` full-only in Sections 8.3 and 23.4, O-7 schema versions and explicit migration in Section 25.3, O-8 specified-but-not-implemented marking in Section 5.6, O-9 shared protections in Section 24, O-10 four of six layers in Section 5.3, O-11 verify-only guard in Section 22.4; all are implemented and none is contradicted.
> C3: I traced SPEC-01 to SPEC-18 to Sections 24.1 to 24.10, 22.2, 5.3, 5.6, 8.3, 23.1 to 23.7, and 25.1 to 25.3; each has normative text; SPEC-13 concerns files outside the provided inputs and could not be judged; SPEC-16 marks the feature as specified with the stated unproven limitation.
> C4: I examined testability and bypass across the protections; the anchor limits, the A0 to A2 limits, the ratcheted required level, and the interpreter opt-in disclose their weaknesses; I found the ignore-file bypass of finding RH-X-002 and no other bypass I could confirm.
> C5: I checked the acceptance examples of the changed text against their rules, including AE-111 to AE-124, AE-157, AE-214, AE-234 to AE-259, AE-274 to AE-323; each follows from its rule except insofar as findings RH-X-001 and RH-X-002 make the underlying rules unclear.
> C6: I searched the whole text for development artifacts, decision or requirement identifiers, tool names outside the method, and local paths; none found; the identifiers `AE-nnn`, `.ggsad/config.yaml`, and `state.yaml` in the migration rule are part of the method.
> C7: I compared every changed or removed line of BASE.md; the removal of the silent-weakening wording is a strengthening, the retry-limit change is disclosed in Section 12, the `reopen` restriction to `full` is decided by O-6, and the `blocked` result is decided by O-5; I found no undisclosed weakening.
> C8: I verified section numbers and cross-references across distant sections, the six layers of Section 5.3, the wait categories of Section 11.1, and every `See AE-nnn` pointer against the 323 defined examples; all resolve correctly.
> LIMITS: The two literal hash values stated in AE-183 and AE-184 could not be recomputed because no command may create a file or use a pipe; SPEC-13 about files under a source directory could not be verified because only the four input files were provided. I used the Read tool, the Grep tool, and the single commands ls, sha256sum, diff, wc, and grep as the brief allows; I opened no file outside the working directory other than the report file itself.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RH-X

## Findings

| Finding | Severity | Reference | Summary | Disposition |
|---|---|---|---|---|
| RH-A-001 | MINOR | file SPEC; section 8.5; lines 1119-1119; quote "Evaluation MUST stop as soon as a gate determines the requested action's outcome." | The flat MUST to stop as soon as one gate decides conflicts with the group-whole evaluation that Section 24.2 prescribes and that 8.5 itself cites. |  |
| RH-A-002 | INFO | file SPEC; section 5.3; lines 396-396; quote "or when the project configuration raises a required assurance level" | The sentence presents the project configuration raising an assurance level as a lower layer strengthening a higher layer, although the configuration is layer 3 itself. |  |
| RH-B-001 | MAJOR | file SPEC; section 12.2; lines 1527-1533; quote "required documentation" | The fail-rule template F-01 omits the mandatory element "required documentation" that the same section lists as MUST content. |  |
| RH-B-002 | MINOR | file SPEC; section 22.1; lines 2301-2301; quote "as the read-only actions `check`, `review`, and `guard` (Section 22.4) do" | The reference "(Section 22.4)" is attached to three actions, but only `guard` is defined there; `check` and `review` are defined in Section 23.4. |  |
| RH-B-003 | INFO | file SPEC; section 12; lines 1499-1503; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition" | The rule that a retry limit is a soft fail condition is restated three times across Section 12 and 12.1. |  |
| RH-C-001 | BLOCKING | file SPEC; section 23.4; lines 2656-2656; quote "The state `closed` with the outcome `cancelled`, or the outcome `failed` when a hard fail condition is active." | cancel and supersede close a change waiting on a soft fail as cancelled, contradicting the rule that the wait ends only by fail or override | fix |
| RH-C-002 | MAJOR | file SPEC; section 23.3; lines 2576-2576; quote "`retry_limit`: a mapping with the members `gate` and `limit`, for a fail gate only." | A wait gate whose condition holds `retry_limit` violates the fail-gate-only rule, yet no clause requires its rejection |  |
| RH-C-003 | MINOR | file SPEC; section 23.4; lines 2674-2674; quote "(issue code `start-blocked`)" | The parenthetical leaves unclear whether the issue code `start-blocked` covers every rejected `start` or only gate-decided ones |  |
| RH-C-004 | INFO | file SPEC; section 23.4; lines 2658-2658; quote "the anchor is created from the history as it is" | `adopt` is legal from any state, including `closed`, although a closed change is declared final and adoption cannot detect entries lost earlier |  |
| RH-X-001 | BLOCKING | file SPEC; section 25.1; lines 4552-4552; quote "The first entry of a `full` change is `new`" | Sections 25.1 and 25.3 contradict each other on the first history entry of a `full` change migrated from a YAML state document. | fix |
| RH-X-002 | BLOCKING | file SPEC; section 24.5; lines 3922-3922; quote "A file that an ignore file inside the repository tells version control to ignore is invisible to the measurement" | The scope rule does not fix which revision of an ignore file applies, so an in-scope edit of an ignore file can hide out-of-scope work. | fix |
| RH-X-003 | MAJOR | file SPEC; section 23.4; lines 2673-2673; quote "the gate definitions differ from the approved ones and the target is not the gate definitions" | Whether an `approve` with target `all` is exempt from the frozen-gate comparison while the gate definitions differ cannot be determined. |  |

## Requestor notes

- The Requestor checked the format of each report and whether each reference resolves in the pinned text; it did not assess whether any finding is correct.
- Independence rests on the reviewer's different product, vendor and model, on separate sessions that share no context with the Requestor, and on the reviewer's own statement of identity in each report; the repository cannot show more.
- A finding's severity is the reviewer's; only the repository owner dispositions a finding.

This note is evidence only. It does not change the reviewed file.
