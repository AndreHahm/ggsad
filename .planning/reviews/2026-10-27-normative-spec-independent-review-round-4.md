# Independent review, round 4: proposed normative method specification

- Independent review: reported
- Owner dispositions: recorded in the review disposition record
- Blocking findings: 1

## The text reviewed

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `fca228479a34e228785f4c0b100da3c6745ada0a` |
| Reviewed SHA-256 | `5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1` |
| Line count | `4812` |
| Diffstat | `1 file changed, 3439 insertions(+), 49 deletions(-)` |
| Commits touching the file | `52` |
| Owner approval record | `.planning/reviews/2026-10-27-normative-spec-fix-round-4-approval-record.md` |
| Owner approval record blob | `8eaffe4aeb442c36d03acf5b3a73e6417e965d53` |
| Run set | `fb0cbd1f1eec` |
| Consent question | `May I send the test run and the six review passes RF-A, RF-B, RF-C, RF-D, RF-E and RF-X (run set fb0cbd1f1eec, model swe-2-medium) to Devin now? Sending cannot be undone, and no run is repeated without asking you again.` |
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
| RF-A | The header and sections 1 to 8 |
| RF-B | Sections 9 to 22 |
| RF-C | Section 23 |
| RF-D | Section 24 up to the end of 24.5 |
| RF-E | Sections 24.6 to 24.10 and section 25 |
| RF-X | The whole text, read across sections |

## Reports

Each report is quoted whole, line by line: a quote mark and a space are added at the start of each line, and an empty line becomes a quote mark alone. The only change made to a report is mechanical: line endings are converted to LF and each tab to four spaces.

### RF-A — The header and sections 1 to 8

> REPORT BEGIN RF-A
> IDENTITY: Devin, an interactive command line agent by Cognition, model SWE-2 Medium; I share no session, prompt, notes, or model with Claude Code: no.
> INPUT SPEC.md 5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RF-A, the header and sections 1 to 8 of SPEC.md, from the first line up to but not including the heading of section 9 (lines 1 to 1126)
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5
> FINDINGS: 6
> FINDING RF-A-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 4.3; lines 307-307; quote "enforced mechanically only for a change that has a state document"
> SUMMARY: The protections of Sections 24.1 to 24.8 are enforced mechanically only when a full change has a state document; a project without one loses all mechanical enforcement.
> REASONING: Section 4.3 makes state.json mandatory only when the project uses persistent machine-readable state, and states that the rules of Sections 24.1 to 24.5, 24.7, and 24.8 that read or write the history are enforced mechanically only for a change that has a state document. Those sections carry the new protections (frozen gates, tri-state results, assurance levels, history integrity, scope, severity, questions) that O-9 makes invariants of both profiles. In a full change where the same information is recorded inline in spec.md or evidence.md, an agent could edit gate definitions or history in letter-compliant ways that no mechanism detects; enforcement then rests entirely on humans. This is a protection that can be bypassed by a permitted configuration choice, so it is reported for the owner to disposition; it may be intended, but the text does not say that the protections still bind the change without mechanical enforcement, beyond the normative force of the rules themselves.
> DISPOSITION REQUIRED: Owner decision or fix: either state that the protections remain binding and how they are verified without a state document, or make a state document mandatory where the protections apply.
> FINDING RF-A-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`"
> SUMMARY: The reserved-name check misses device names followed by an extension (for example `con.x`), which the same file systems also reserve.
> REASONING: The identifier names the directory specs/<change-id>/. On file systems that reserve device names, the reservation also applies to the name followed by any extension, so `con.txt` or `com1.log` cannot name a directory there either, yet the rule accepts them. An implementation that follows the stated rule exactly accepts an identifier it then cannot use to create the change directory. The case-folding comparison is specified, but the extension form is not covered, and AE-288 exercises only the bare reserved names.
> DISPOSITION REQUIRED: Fix: extend the reserved-name rule to cover a reserved name followed by a dot and further characters, or state that such names are permitted.
> FINDING RF-A-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 5.6; lines 577-577; quote "4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 16.1 to 16.4, and the diagram of Section 21"
> SUMMARY: The applicability table names 8.1 to 8.5 as full only, leaving the unnumbered preamble of section 8 applicable to both profiles by the table's own rule.
> REASONING: The table states that a section it does not name as full only applies to both method profiles. It names "8.1 to 8.5" but not the body of section 8 itself, which contains the sentences "This section specifies the `full` method profile" and "Every phase has a status". The marking line resolves the intent, and a core change has no phases, so no conforming participant is likely to act differently; the defect is one of coverage wording in the table, consistent with how "6" and "7" are named whole while "8" is not.
> DISPOSITION REQUIRED: Fix: name section 8 whole in the table, or clarify that the preamble of a listed section shares its applicability.
> FINDING RF-A-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 8.3; lines 1019-1021; quote "an active Definition of Fail condition"
> SUMMARY: AE-244 does not state the severity of the active fail condition; the outcome `failed` follows only for severity `hard`.
> REASONING: The second change in AE-244 has "an active Definition of Fail condition" with no severity given, and the result is the closed phase with status `failed` because the Definition of Fail has first priority. Under Section 8.4 and Section 24.7, a fail condition of severity `soft` does not determine failure: it waits for a human disposition. The example as written covers only the hard case and could be read as any active fail condition turning a cancel into a failure. The rule it illustrates is correct; the example underspecifies its given state.
> DISPOSITION REQUIRED: Fix: add "of the severity `hard`" to the given state of the second change.
> FINDING RF-A-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 8.3; lines 904-904; quote "The change is closed, or no DoW condition is active"
> REFERENCE: file SPEC; section 8.3; lines 1037-1037; quote "each result is `rejected` with `changed` false and the issue code `gate-not-evaluable`"
> SUMMARY: The per-action table of rejected results omits the `gate-not-evaluable` rejection that AE-310 and Section 8.5 establish for wait, fail, and reopen.
> REASONING: AE-310 and Section 8.5 state that `wait`, `fail`, and `reopen` of the full profile answer `rejected` with issue code `gate-not-evaluable` when a gate that applies to them cannot be evaluated. The "Rejected and Blocked Results per Action" table lists rejected cases per action and, for these three actions, lists only the precondition failures; it does not list the not-evaluable case. A note after the table defers to Section 24.2 for those answers, so the omission does not change behavior, but the table reads as an enumeration and is incomplete for exactly the cases the note names.
> DISPOSITION REQUIRED: Fix or clarify: add the not-evaluable rejection to the affected rows, or state that the table does not enumerate the Section 24.2 cases.
> FINDING RF-A-006
> SEVERITY: INFO
> REFERENCE: file SPEC; section 5.3; lines 386-386; quote "The method profile (Section 5.6) and the compliance profile (Section 5.1) of a change are resolved together, and neither ranks above the other"
> SUMMARY: Layer 2 holds method profile and compliance profile with no ranking; the text does not say how a direct conflict between the two inside the layer resolves.
> REASONING: The weakening and strengthening rules are defined between layers. Within layer 2 both rule sets apply cumulatively in most readings, since a rule of either can only add obligations and "neither ranks above the other". The specification does not state what happens if a compliance-profile rule and a method-profile rule demand incompatible outcomes (for example different approval requirements phrased as permissions). In practice the higher-assurance or stronger reading presumably wins, but the outcome cannot be derived from the text alone.
> DISPOSITION REQUIRED: Clarify: state that within layer 2 both rule sets apply and any apparent conflict resolves to the stronger obligation, or define another rule.
> CHECKS PERFORMED:
> C1: Read the changed text of sections 1 to 8 for statements that cannot hold together and for terms used in two senses; found the underspecified intra-layer-2 conflict rule (RF-A-006) and no contradictions between the transition table, the rejected/blocked table, and Section 8.5 beyond the enumeration gap of RF-A-005.
> C2: Traced each owner decision that touches this range: O-1 (two profiles, Section 5.6), O-6 (reopen full only, marked in the 8.3 table and stated in 8.4), O-8 (full marked specified but not implemented, Section 5.6), O-9 (protections applied to both profiles, subject of RF-A-001), O-10 (core implements layers 1, 2, 3, 5, stated in 5.3 and AE-226), O-4 (state.json in 4.3 and the JSON metadata example of 8.1). No decision is contradicted in this range; O-2, O-3, O-5, O-7, O-11 are implemented mainly outside this range and were consulted only for judging.
> C3: Checked the requirement texts relevant here: SPEC-12 and SPEC-14 (profiles specified, full carries the protections and the specified-but-not-implemented marking), SPEC-16 (six-layer order and no-weakening rule, with core on four layers), SPEC-17 (reopen per profile in the transition table). All are present as normative text in this range; none is contradicted here. The mechanical-enforcement caveat is reported as RF-A-001.
> C4: Looked for untestable rules and bypasses: found the state-document enforcement caveat (RF-A-001) and the reserved-name gap that admits an identifier the file system cannot hold (RF-A-002); the identifier syntax, the weakening check at creation and before approval, and the per-action rejected/blocked cases are otherwise stated testably.
> C5: Checked every acceptance example in the range (AE-01 to AE-08, AE-121 to AE-124, AE-217 to AE-248, AE-288 to AE-298, AE-308, AE-310) against its named rule; all follow from their rules except AE-244, which underspecifies the severity that its outcome requires (RF-A-004).
> C6: Searched the range for development artifacts, prototype identifiers, decision or requirement ids, external tool names, and local paths; the range cites none — section and AE cross-references are internal to the method.
> C7: Compared BASE.md with SPEC.md in this range via a full diff; the rejected-to-blocked changes in the transition table and the reopen-waits-to-rejects change implement the new result model and are matched by the new per-action table; no MUST, SHOULD, or prohibition of BASE was removed or relaxed without the change being stated, aside from the enforcement caveat reported as RF-A-001, which is new text rather than removed text.
> C8: Checked section numbers and cross-references in the range (4.1, 4.2, 4.3, 5.1, 5.3, 5.6, 6.1, 7.1, 8.x, 16.1, 16.4, 16.5, 22.2, 23.1, 23.3, 23.4, 23.7, 24.1 to 24.9, 25.1); all cited sections exist and the terms used (method profile, compliance profile, blocked, changed, issue code, WAIT_DECISION, assurance levels A0 to A2, base gates) are defined or are defined in the cited later sections; the section-8 preamble gap of the applicability table is reported as RF-A-003.
> LIMITS: I computed all four SHA-256 values with sha256sum and they match the expected values in BRIEF.md. I used the Read tool, the Glob/Grep capability of the shell for heading line numbers, and the permitted commands ls, diff, and sha256sum, one plain command per call. The diff output exceeded the terminal buffer, so I also opened the output capture file that the shell tool wrote outside my working directory; no other file outside the working directory was opened. Sections 9 to 25 of SPEC.md were read only as far as their heading names and cited content needed to judge the changed text in scope; their own correctness is the subject of other passes.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RF-A

### RF-B — Sections 9 to 22

> REPORT BEGIN RF-B
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the SWE-2 Medium model; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md 5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RF-B; SPEC.md from the heading of section 9 up to, but not including, the heading of section 23 (sections 9 to 22).
> COVERAGE: 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4
> FINDINGS: 6
> FINDING RF-B-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 12; lines 1495-1495; quote "as the earlier text of this method did"
> SUMMARY: Normative sentence cites the earlier text of the method, a document outside this specification, which breaks self-containment.
> REASONING: The sentence states that reaching a retry limit "does not end it by itself, as the earlier text of this method did". The trailing clause depends on the wording of a previous version of the specification that a reader of this text does not have. Charter C6 covers text that cites development artifacts; a reference to the former wording of the method is such a citation. The normative effect (a retry limit pauses the flow for a human disposition) is still determinable, so the defect is of wording only.
> DISPOSITION REQUIRED: Fix. Remove the clause "as the earlier text of this method did"; the rule stands without it.
> FINDING RF-B-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 12.2; lines 1519-1521; quote "Every fail rule MUST include:"
> REFERENCE: file SPEC; section 12.2; lines 1550-1550; quote "Every fail rule also states its severity, `hard` or `soft` (Section 24.7)."
> SUMMARY: The mandatory-content list of a fail rule omits severity, which the following prose and the template require; whether a rule without severity is valid cannot be determined from the list.
> REASONING: Section 12.2 says "Every fail rule MUST include" and lists trigger, required response, permitted preservation actions, final status, and required documentation. Only after the template does the text add "Every fail rule also states its severity". AE-269 tests a rule without a final status but none without a severity. A reader checking conformance against the MUST list would find a severity-less rule conforming, while the prose suggests it is not. The outcome for such a rule is ambiguous (C1); the practical effect is small because a core fail gate without a severity is invalid under Section 23.3 and Section 24.7 fixes the response to an active condition.
> DISPOSITION REQUIRED: Fix. Add severity to the MUST-include list, or state explicitly in the list that severity is required in addition.
> FINDING RF-B-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 11.2; lines 1434-1441; quote "Every wait state MUST include:"
> REFERENCE: file SPEC; section 11.2; lines 1458-1458; quote "it holds a phase identifier of Section 7"
> REFERENCE: file SPEC; section 8.3; lines 892-892; quote "the recorded or explicitly required resume phase is non-closed"
> SUMMARY: The wait-state template carries resume_at and describes it, yet the mandatory list does not require it, while the resume action prefers a recorded resume phase.
> REASONING: Section 11.2 lists six mandatory items (reason, outstanding information or decision, responsible person or source, resume condition, safe current state, next action after resumption). The template additionally carries status and resume_at, and the prose assigns resume_at a phase identifier of Section 7, but no rule states whether resume_at is required. The resume action of Section 8.3 works on "the recorded or explicitly required resume phase"; a conforming wait state can therefore lack the recorded resume phase, leaving the outcome of resume dependent on the "explicitly required" fallback. The behavior is recoverable, so the defect is of wording and completeness rather than a trap (C1, C4).
> DISPOSITION REQUIRED: Clarify. State whether resume_at is mandatory for a full wait state, or state that its absence requires an explicitly required phase at resume.
> FINDING RF-B-004
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 5.6; lines 577-577; quote "16.1 to 16.4"
> REFERENCE: file SPEC; section 16.1; lines 1830-1830; quote "are the gate definitions of the change and are fixed when the change is approved (Section 24.1)"
> REFERENCE: file SPEC; section 16; lines 1727-1944; quote none
> SUMMARY: Sections 16.1 to 16.4 are full-only and contain normative rules, but no acceptance example covers them, while requirement SPEC-14 asks that each full rule have one.
> REASONING: The table of Section 5.6 marks "16.1 to 16.4" as `full` only. These sections carry rules an implementation can apply incorrectly or not at all, for example that the Flow Gates conditions together with the scope are the gate definitions fixed at approval (Section 16.1, line 1830), that requirement identifiers and evidence-command lists are fixed with the gate definitions (line 1836), and that a gate that could not be evaluated is listed by name and cause rather than Yes or No (Section 16.4, line 1946). Requirement SPEC-14 states that each `full` rule has an acceptance example of the kind the `core` rules have. No acceptance example in the text covers Section 16.1, 16.2, 16.3, or 16.4 (a search of all "Covers:" lines finds none naming Section 16). Whether a Minimum Template counts as a "rule" under SPEC-14 is the open point, which is why this is not raised as BLOCKING.
> DISPOSITION REQUIRED: Owner decision. Either add acceptance examples covering the rules of Sections 16.1 to 16.4, or record that template content is exempt from the per-rule example requirement.
> FINDING RF-B-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 12; lines 1493-1495; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition"
> REFERENCE: file SPEC; section 12; lines 1495-1495; quote "reaching one pauses the flow for a human disposition and does not end it by itself"
> REFERENCE: file SPEC; section 12.1; lines 1511-1511; quote "A retry limit is a soft fail condition (Section 24.7)."
> SUMMARY: The rule that a retry limit is a soft fail condition and does not terminate the flow is stated three times in Section 12.
> REASONING: The substance is stated at line 1493, restated at line 1495, and repeated at line 1511. Triple statement of one rule invites divergence on later edits and adds no normative content. This is a defect of wording and structure only (C1 by redundancy, no contradiction found among the three statements).
> DISPOSITION REQUIRED: Fix. State the rule once, for example at lines 1491-1493, and drop the repetitions at lines 1495 and 1511.
> FINDING RF-B-006
> SEVERITY: INFO
> REFERENCE: file SPEC; section 12.1; lines 1505-1505; quote "exceeding a hard budget or cost limit,"
> REFERENCE: file BASE; section 12.1; lines 785-785; quote "exceeding hard budget, cost, or retry limits,"
> SUMMARY: A retry limit moved from the hard fail categories to a soft failure; the change is disclosed in the text and matches the soft-failure design, so it is recorded as an observation, not a defect.
> REASONING: BASE listed "exceeding hard budget, cost, or retry limits" among the typical fail categories under a general obligation to terminate. SPEC removes retry limits from that list and declares a retry limit a soft fail condition that pauses the flow for a human disposition. Under charter C7 this would be a weakening, but the text discloses it explicitly (lines 1493-1495 name the earlier behavior) and the change is consistent with the soft-failure design of requirement SPEC-08, which grants a human the choice to close or to record a bounded override. No defect; noted so the owner is aware the protection changed in kind.
> DISPOSITION REQUIRED: None. Recorded for owner awareness only.
> CHECKS PERFORMED:
> C1: I read sections 9 to 22 in full and the diff of BASE against SPEC for this range; I checked the new sentences against each other and against Sections 5.6, 7, 8.3, 23.4, 23.6, 23.7, and 24.1 to 24.10 where they are referenced. Found the severity-list ambiguity (RF-B-002), the resume_at optionality gap (RF-B-003), and the triple-stated retry rule (RF-B-005); no outright contradiction located.
> C2: For this range, the decisions that bite are O-5 (blocked is a normative fourth result, implemented in 22.2 and per action in 8.3), O-11 (verify-only CI, implemented as the guard action of 22.4 with exactly the five verifications named), O-6 (reopen is marked full only in 8.3), and O-4 (the wait-state template moved to JSON, matching the state-document move). No decision in this range is contradicted or left without corresponding text.
> C3: SPEC-02, SPEC-03, SPEC-06, SPEC-07, SPEC-08, SPEC-09, and SPEC-10 are implemented or correctly referenced in this range; SPEC-14 is only partially met because the full-only rules of Sections 16.1 to 16.4 carry no acceptance example (RF-B-004).
> C4: Blocked is always recorded and changed true, so attempts stay countable; guard executes nothing and fails closed on a change without a state document, so it cannot be bypassed by running or by omission. The resume_at gap is the only failure behavior left partially unspecified (RF-B-003).
> C5: I checked every acceptance example in the range (AE-260 to AE-270, AE-287, AE-111 to AE-116, AE-303 to AE-306) against its named rule; each follows from and names the section it covers.
> C6: One self-containment breach found, the citation of the earlier text of the method in Section 12 (RF-B-001); no prototype identifiers, project artifact names, tool names, or local paths appear in the range.
> C7: I compared every changed line with BASE. The only protection change is the retry-limit move from a hard fail category to a soft failure, which the text discloses explicitly (RF-B-006); all other edits are additions or clarifications.
> C8: Section references (5.6, 7, 8.3, 22.2, 22.4, 23.2, 23.4, 23.6, 23.7, 24.1 to 24.10, 25.1, 25.3) and the See-AE pointers resolve correctly; every term used in changed text is defined in the document; the phase identifier plan used in the template exists in Section 7.
> LIMITS: I verified only the files listed in BRIEF.md and computed their SHA-256 with sha256sum; all hashes match the expected values. I used the Read, Grep, Glob-equivalent listing via ls, and the allowed commands ls, diff, wc, grep, sha256sum. Sections outside 9 to 22 (5.6, 7, 8, 23, 24, 25) were read only to judge the changed text in range, not reviewed in their own right. Tool-captured command output was written to files outside the working directory; I read those captures and opened no other file outside it. Whether Sections 16.1 to 16.4 count as rules under SPEC-14 is reported as an owner decision rather than resolved.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RF-B

### RF-C — Section 23

> REPORT BEGIN RF-C
> IDENTITY: Devin, an interactive command line agent by Cognition, model SWE-2 Medium; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RF-C, section 23 of SPEC.md, from the heading of section 23 up to but not including the heading of section 24
> COVERAGE: 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7
> FINDINGS: 2
> FINDING RF-C-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.6; lines 2984-2984; quote "the evaluation MUST stop as soon as a gate decides the requested action"
> REFERENCE: file SPEC; section 23.6; lines 2992-2992; quote "a group is evaluated whole, and that the evaluation stops after the first group that decides"
> SUMMARY: Section 23.6 first says evaluation MUST stop as soon as a gate decides, then says a group is evaluated whole, two stop rules that read differently
> REASONING: Read literally, "MUST stop as soon as a gate decides" directs the evaluator to halt at the first deciding gate, while the later sentence (and Section 24.2, which states every gate of a deciding group is evaluated even when an earlier gate of the same group already decides) directs it to finish the group. The outcome in state terms is the same, but which gates are evaluated and have results recorded differs between the two readings. The defect is wording only, since the group rule in the same paragraph and Section 24.2 supply the intended resolution.
> DISPOSITION REQUIRED: Fix: align the first sentence of Section 23.6 with the group rule, for example by stating that the evaluation stops once the results of a group decide the requested action.
> FINDING RF-C-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.3; lines 2490-2490; quote "the member `gate` is the identifier of a done gate of the kind `check`, and the member `limit` is the limit of Section 24.2"
> SUMMARY: A retry_limit fail gate must name a check done gate, but no rule requires the named gate to exist in the same change definition
> REASONING: Section 23.3 requires the member `gate` of a `retry_limit` condition to be the identifier of a done gate of the kind `check`, and the rejection rule of the same section covers missing members, extra members, and predicates not listed for the kind of the gate, but it does not state that the identifier must resolve to a done gate actually defined in the change. A change definition whose fail gate retries against an identifier that no done gate carries passes every stated validation, leaving a fail gate that can never become active, so a mistyped identifier silently disables the protection the gate was meant to provide.
> DISPOSITION REQUIRED: Fix or clarify: state that the identifier named by `gate` MUST be the identifier of a `check` done gate of the same change, and that a definition naming none is rejected.
> CHECKS PERFORMED:
> C1: Read the whole of section 23 and traced states, actions, preconditions, rejected and blocked results, and the evaluation order against each other; the transition table, the rejected and blocked table, and Section 23.6 are mutually consistent; one wording conflict between the stop rule and the group rule is reported as RF-C-001.
> C2: Checked the decisions that touch section 23: O-1 (core profile exists), O-4 (state.json is engine-owned), O-5 (blocked result is stated per action), O-6 (no reopen in core, closed is final), O-9 (protections of Section 24 apply), O-10 (four resolution layers, matching Section 5.3); all are implemented and none is contradicted in this range.
> C3: Checked the requirements implemented in this range: SPEC-03 (per-action rejected and blocked results), SPEC-08 (hard and soft failure paths), SPEC-09 (questions as state, structured answers, approval and closure blocked), SPEC-12 (four-state core model), SPEC-17 (reopen absent from core); all are satisfied; the cross-profile parts of SPEC-12 lie outside this range.
> C4: Checked that rules are testable and not bypassable: human-only actions are named, gate conditions and severities are validated at creation, base gates cannot be redefined or switched off, a hand-edited state document is detected, and unevaluable gates produce waits rather than failures; one residual gap around an unresolved retry_limit target is reported as RF-C-002.
> C5: Checked every acceptance example in the range (AE-09 to AE-58 and AE-215 to AE-299 located here) against its rule; each follows from the text, including the borderline cases AE-118 versus AE-274 (rejected versus blocked resume) and AE-299 (cancel proceeds on an unevaluable gate).
> C6: Searched the range for citations of development artifacts, decision or requirement identifiers, tool names and local paths; found none; artifact names used (change.yaml, spec.md, state.json, specs/<change-id>/) are part of the method itself.
> C7: Compared with BASE.md, which ends at section 22, so the range is entirely new text; where section 23 limits items of Sections 11.2 and 12.2 to the `full` profile it says so explicitly and the limitation follows owner decision O-1, so no unstated weakening was found in this range.
> C8: Verified the cross-references used in the range: Sections 3.1, 3.7, 3.9, 4.1, 4.3, 5.1, 5.3, 5.6, 6, 7, 9, 10, 11.1, 11.2, 12.2, 14.5, 22.2, 22.3, 22.4, 24.1 to 24.9 and 25.1 exist and match their use, and every cited example identifier (including AE-215, AE-216, AE-219, AE-225, AE-276, AE-277, AE-278, AE-284, AE-309) exists as an example in the text.
> LIMITS: The pass covers only section 23; Sections 24 and 25 and earlier sections were read only as far as needed to judge the text in range, so defects located entirely inside those sections are out of scope for this report. I did not execute any gate examples; consistency was judged by reading. Tools used: Read, Grep, Glob-equivalent listing, ls, wc and sha256sum. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RF-C

### RF-D — Section 24 up to the end of 24.5

> REPORT BEGIN RF-D
> IDENTITY: Devin, Cognition, model SWE-2 Medium; I share no session, prompt, notes or model with Claude Code.
> INPUT SPEC.md 5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RF-D, from heading 24 up to, but not including, heading 24.6 (lines 3067-3917 of SPEC.md)
> COVERAGE: 24, 24.1, 24.2, 24.3, 24.4, 24.5
> FINDINGS: 4
> FINDING RF-D-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 24.4; lines 3688-3688; quote "Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor or an equivalent mechanism"
> SUMMARY: The anchor requirement triggers only on a configured A2 minimum; a change whose gates alone require A2 gets no truncation detection.
> REASONING: Section 24.3 (line 3534) defines the required level of an action as the higher of the minimum the gate states and the minimum the project configuration sets. A change can therefore require A2 approvals purely through a gate minimum, with no A2 requirement in the applicable configuration. Section 24.4 then requires no anchor, so removal of the latest entries, including the entries that record the A2 approvals, is undetectable: a truncated history remains consistent. The protection SPEC-05 asks for, an anchor or equivalent where high assurance is demanded, is present only for the configuration trigger, so the same assurance demand expressed inside the change's own frozen gates bypasses it.
> DISPOSITION REQUIRED: Clarify or extend the trigger so that a high-assurance demand arising from a gate minimum also requires an anchor or equivalent, or have the owner confirm the narrower trigger.
> FINDING RF-D-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.5; lines 3798-3798; quote "a segment that is exactly `**` matches any number of path segments, including none"
> SUMMARY: Whether the pattern lib/** matches the path lib itself, when ** stands for zero segments, is not stated.
> REASONING: The rule says ** matches any number of path segments including none, but does not say whether the separator before the trailing ** may then also match nothing, so a conforming implementation cannot determine from the text whether the path lib matches lib/**. The same uncertainty applies to a pattern ending with a directory slash, which "names every path below that directory" without saying whether the directory path itself is named.
> DISPOSITION REQUIRED: Fix by adding a sentence that decides both cases, or clarify.
> FINDING RF-D-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.2; lines 3380-3380; quote "In `full`, it is a condition of a Flow Gates list (Section 16.1) that names a command."
> REFERENCE: file SPEC; section 24; lines 3124-3124; quote "a `full` change in the verify phase whose Definition of Done holds a check-command condition whose program does not exist"
> SUMMARY: In full, "check-command gate" is defined only for Flow Gates conditions, while AE-250 puts a check-command condition in the Definition of Done.
> REASONING: Line 3380 defines which full conditions are check-command gates and limits them to Flow Gates list items, but the introduction (line 3097) and AE-250 evaluate a Definition of Done check-command condition with exit-map semantics. The general first sentence of the paragraph ("a gate whose condition is the outcome of a command") can be read to cover it, but the profile-specific sentence then appears to exclude Definition conditions from the declared exit-map rules, leaving the applicable definition uncertain.
> DISPOSITION REQUIRED: Clarify whether the exit-map declaration and evaluation rules apply to command-bearing conditions of the Definitions of Ready, Done, Wait, and Fail in full.
> FINDING RF-D-004
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.5; lines 3804-3804; quote "exactly two further names in the change directory are exempt: the in-progress file `state.json.tmp` and the lock object `state.json.lock`"
> SUMMARY: The unconditional exemption lets any file named state.json.tmp or state.json.lock in the change directory escape scope measurement, not only a genuine leftover.
> REASONING: The exemption exists so that a file left behind by an interrupted write is never a scope violation, but it is not conditioned on the file being such a leftover. A participant can keep arbitrary content in the change directory under these exact names without a scope violation. The blast radius is small because the exemption is confined to the change directory and the real state document is protected by the history chain, so this is an observation rather than a defect that changes behavior.
> DISPOSITION REQUIRED: None required; the owner may accept the residual gap or bound the exemption.
> CHECKS PERFORMED:
> C1: Read sections 24 to 24.5 in full and cross-checked the rules, the result order of Section 24.2, the base gates of Section 23.7 and the transition table of Section 8.3; found no contradiction; one underdetermined pattern case (RF-D-002) and one definitional ambiguity (RF-D-003).
> C2: Traced O-1, O-3, O-5, O-8 and O-9 into the range: both profiles carry the protections as invariants, `blocked` is recorded with changed true, the signed-approval format is normative with optional verifiers, and full is marked specified but not implemented; no decision contradicted.
> C3: Checked SPEC-01, SPEC-02, SPEC-04, SPEC-05, SPEC-06 and SPEC-14 against the text; all are implemented, with one gap in the SPEC-05 anchor trigger reported as RF-D-001; SPEC-03 is satisfied in this range as far as the blocked usage shown is concerned.
> C4: Examined bypass paths: hash comparison precedes operations, cancel is exempt by design, gate-not-evaluable is never a failure, ignored-file and leftover-file exemptions were probed; found the narrow bypasses RF-D-001 and RF-D-004.
> C5: Verified the acceptance examples AE-60, AE-249 to AE-259, AE-286, AE-294, AE-300, AE-61 to AE-86, AE-125 to AE-136, AE-137 to AE-146, AE-278, AE-280 and AE-282, AE-307, AE-309, AE-310 references against their rules; they follow from the rules they cite.
> C6: Searched the range for development artifacts, prototype identifiers, decision or requirement identifiers of the project and local paths; found none; the AE-nn labels are part of the method's example convention of Section 3.9.
> C7: BASE.md contains no sections 23 to 25, so the whole range is new text; no protection, MUST, SHOULD or prohibition of BASE.md in this range was removed or relaxed.
> C8: Checked section references to 4.3, 5.1, 5.3, 5.4, 8.3, 8.5, 9.6, 11.1, 12.2, 16.1, 22.2, 23.1, 23.3, 23.4, 23.5, 23.6, 23.7, 24.1 to 24.10 and 25.1 to 25.2 and the heading names R<n> and Evidence Commands; all resolve to existing headings; terms human:, not_evaluable, not_applicable and the wait categories are used consistently with their definitions.
> LIMITS: BASE.md ends at Section 22.3, so comparison is one-sided new text; I read Sections 8.3, 9.6, 11.1, 22.2, 23.1 to 23.7 and 25 outside the range only to judge it. Tools used: Read, Grep, sha256sum, ls, wc, tail. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RF-D

### RF-E — Sections 24.6 to 24.10 and section 25

> REPORT BEGIN RF-E
> IDENTITY: Devin, an interactive command-line agent by Cognition, powered by the SWE-2 Medium model; I share no session, prompt, notes, or model with Claude Code: no
> INPUT SPEC.md 5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RF-E, sections 24.6 to 24.10 and section 25 of SPEC.md (from heading 24.6 up to the end of the file)
> COVERAGE: 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 4
> FINDING RF-E-001
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.7; lines 4014-4014; quote "A retry limit (Section 24.2) is a fail condition of the severity `soft`, and a retry limit that declares the severity `hard` is invalid and MUST be rejected."
> SUMMARY: Whether a retry limit that declares no severity, or declares `soft`, is valid is left implicit and can be misread against the missing-severity rejection rule.
> REASONING: The first rule of the section says a fail condition without a severity is invalid and MUST be rejected. The retry-limit sentence then defines a retry limit as a fail condition of the severity `soft` and invalidates only a declared `hard`. The intended reading, that a retry limit has the severity `soft` by definition and therefore is never "without a severity" and may also declare `soft`, is plausible but not stated; an implementer could instead apply the missing-severity rejection to an undeclared retry limit, or reject a declared `soft`. No acceptance example settles whether an undeclared or a `soft`-declared retry limit is accepted at approval.
> DISPOSITION REQUIRED: Clarify: state explicitly whether the severity field of a retry limit is optional, whether it defaults to `soft`, and whether declaring `soft` is valid.
> FINDING RF-E-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.7; lines 4031-4031; quote "It lapses when its N attempts are used up and when the gate definitions are amended."
> SUMMARY: "lapses when its N attempts are used up and when the gate definitions are amended" reads as a conjunction of two conditions rather than two independent lapse triggers.
> REASONING: The intended semantics, shown by AE-103 where an override with one attempt left lapses on amendment alone, is that either event lapses the override. The normative sentence joins the two events with "and", which a reader can parse as requiring both before the override lapses. The following sentence about a lapsed override does not resolve which reading is meant. An implementer applying the conjunctive reading would keep an override in force after amendment until the attempts are also used, contradicting AE-103.
> DISPOSITION REQUIRED: Fix wording: replace "and when" with "or when" (or "when either occurs"), matching AE-103.
> FINDING RF-E-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.3; lines 4708-4708; quote "It takes the file and optionally a target version, which is a supported version that is higher than the version of the file"
> SUMMARY: The result of a `migrate` request whose target version is unsupported, or is supported but unreachable by a chain of steps, is unspecified.
> REASONING: The paragraph constrains a valid target version and covers a target not given (highest supported) and a file already at or above the target (answered `rejected`). It does not state what happens when the caller gives a target that is not a supported version, or a supported target for which no step chain from the file's version exists. Failure behaviour is left unspecified: an implementation could reject, treat the request as error, or silently migrate to a different version. No acceptance example covers the case.
> DISPOSITION REQUIRED: Specify the result (presumably `rejected` with a stable issue code) for a target version that is unsupported, not higher than the file version in a defined way, or unreachable by the step chain.
> FINDING RF-E-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.9; lines 4344-4344; quote "an evidence command that is `satisfied` is bound to R1 and the action is requested again"
> SUMMARY: AE-168 does not state whether the gate definitions were approved, so it can be read as binding a new evidence command without the re-approval that Sections 24.1 and 24.9 require.
> REASONING: Section 24.9 fixes requirement identifiers and their evidence commands with the gate definitions, and AE-169 shows that changing an approved evidence command makes `close` answer `rejected` with `gates-changed` until a human re-approves. In AE-168 an evidence command is bound to R1 after the first `close` request and the second request is evaluated as complete, with no mention of re-approval. The example is consistent only if the gate definitions were never approved before; since it does not say so, it can be read as showing that an evidence command can be added and take effect without a new human approval, which would undercut the frozen-definitions rule it is meant to illustrate.
> DISPOSITION REQUIRED: Clarify the example: state that the gate definitions were not yet approved, or add the re-approval step before the second `close` request.
> CHECKS PERFORMED:
> C1: Read Sections 24.6 to 24.10 and 25 in full and checked internal consistency of the rules (baseline comparison, severity rules, override accounting, question fields, evidence completeness, interpreter token, canonical form, hashing, locking, schema versions, migration). Found two ambiguous wordings, reported as findings RF-E-001 and RF-E-002; no outright contradiction found.
> C2: Traced the owner decisions that touch this range: O-4 (state moves to `state.json`, definitions stay YAML: Section 25.1 and the `state.yaml` migration of Section 25.3), O-5 (`blocked` recorded with `changed` true: Sections 24.8, 25.1, consistent with 22.2), O-7 (every schema-governed file carries `schema_version`, unknown versions refused, migration explicit and recorded: Section 25.3), and O-9 (protections as invariants of both profiles: per-profile wording throughout). No decision is contradicted and none lacks corresponding text in the range.
> C3: Traced the requirements that land in this range: SPEC-07 (Section 24.6), SPEC-08 (Section 24.7), SPEC-09 (Section 24.8), SPEC-10 (Section 24.9), SPEC-11 (Section 24.10), SPEC-15 (Sections 25.1 and 25.2) and SPEC-18 (Section 25.3). Each is satisfied by normative text and none is contradicted; no required content is missing.
> C4: Looked for untestable rules, bypasses and unspecified failure behaviour. The rules in the range are testable through recorded results and issue codes. One case of unspecified failure behaviour found (invalid `migrate` target), reported as finding RF-E-003. The `state-conflict`, `schema-version-mismatch` and ignore-file exposure rules specify their failure modes.
> C5: Checked every acceptance example in the range (AE-87 to AE-110, AE-158 to AE-182, AE-183 to AE-214, AE-279, AE-281, AE-283 to AE-285, AE-301, AE-302) against its rule. Each follows from the rule it cites and covers the case it names, except AE-168 which omits a fact needed to see that it does not bypass frozen gate definitions, reported as finding RF-E-004.
> C6: Searched the range for citations of development artifacts, prototype identifiers, decision or requirement ids, tool names and local paths. None found; the text is self-contained.
> C7: The range is entirely new text (BASE.md ends at Section 22.3), so no protection, MUST, SHOULD or prohibition of BASE.md exists here to be weakened. Cross-read of the sections the range modifies by reference (8.3, 8.4, 11.1, 12.2, 22.1, 22.2, 23.4, 23.5, 23.7, 24.1, 24.2, 24.3) found no protection relaxed.
> C8: Verified cross-references made in the range: Sections 4.3, 5.6, 8.1, 8.3, 8.4, 10.7, 11, 11.1, 11.2, 12.2, 15, 16.1 (Evidence Commands heading), 20, 22.1, 22.2, 23.1 to 23.7 and 24.1 to 24.5 all exist and say what the citations claim; every cited AE identifier (including AE-279, AE-301, AE-302, AE-308) exists. Terms such as `check-command gate`, `exit map`, `wait record`, `approved hash`, `state-conflict` and `WAIT_DECISION` are used only after their definitions.
> LIMITS: I could not verify the SHA-256 digest value asserted inside acceptance example AE-183 against the canonical text it names, because computing it would have required a command outside the allowed list; the well-known empty-object digest of AE-184 is consistent with the canonical rules. I compared SPEC.md and BASE.md by structure and headings rather than a full line diff, since the pass range is entirely new. Tools used: Read, Grep, ls, grep, sha256sum, wc. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RF-E

### RF-X — The whole text, read across sections

> REPORT BEGIN RF-X
> IDENTITY: Devin, Cognition, powered by SWE-2 Medium; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 5c882bcc9ff7997ae379d5de4b15dc18646d6b69037b9458896abb49724283f1
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RF-X, the whole text from the header to the end, read across sections; each owner decision and each requirement traced to the text that implements it, and distant sections compared for conflicts
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 24, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 12
> FINDING RF-X-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 5.6; lines 577-577; quote "4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 16.1 to 16.4, and the diagram of Section 21"
> REFERENCE: file SPEC; section 16.1; lines 1836-1836; quote "The requirement identifiers and these lists are fixed with the gate definitions (Section 24.1), and a requirement without a list item has no evidence command."
> SUMMARY: Sections 16.1 to 16.4 are marked full-only yet contain normative rules and no acceptance example, which SPEC-14 requires for each full rule.
> REASONING: The Section 5.6 table assigns Sections 16.1 to 16.4 to `full` only. Those subsections carry normative rules: the Allowed Paths list holds machine-checkable patterns, the requirement identifiers and evidence command lists are fixed with the gate definitions, the Open Questions section is a view of recorded state, and the evidence record fields are prescribed. None of Sections 16.1 to 16.4 carries an acceptance example, and no AE elsewhere is marked as covering them. SPEC-14 requires that each `full` rule has an acceptance example of the kind the `core` rules have, and O-8's recorded mitigation requires the same. The required content is missing.
> DISPOSITION REQUIRED: Add an acceptance example covering the normative rules of Sections 16.1 to 16.4, or obtain an owner disposition narrowing SPEC-14.
> FINDING RF-X-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 13.1; lines 1570-1576; quote "When a requirement conflicts with an ADR, the agent MUST:"
> SUMMARY: Section 13 (ADR conflicts, specification drift, breaking changes) has MUST rules but no acceptance example anywhere in the section.
> REASONING: Sections 13.1 to 13.3 impose mandatory steps (document the conflict, stop work, return the requirement, request and reference a decision; the specification-drift dispositions; breaking-change approval). No acceptance example covers any of them. SPEC-14 asks for an example for each `full` rule; these rules govern `full` changes even though the section also applies to `core`, so the requirement plausibly reaches them.
> DISPOSITION REQUIRED: Add acceptance examples for Section 13 or clarify that SPEC-14 does not extend to sections applying to both method profiles.
> FINDING RF-X-003
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 14.3; lines 1628-1637; quote "A Pair Review cycle MUST:"
> SUMMARY: Sections 14.3 to 14.5 (review cycle, findings, review artifacts) contain MUST rules with no acceptance example.
> REASONING: The eight-step review cycle, the blocking-finding rule, and the mandatory eight-field Pair Review evidence record are normative rules that apply to `full` changes. No acceptance example covers Sections 14.3 to 14.5. Under SPEC-14 each `full` rule needs an example of the kind the `core` rules have.
> DISPOSITION REQUIRED: Add acceptance examples or clarify the reach of SPEC-14.
> FINDING RF-X-004
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 19.1; lines 2133-2142; quote "An AI agent MUST NOT:"
> SUMMARY: The agent prohibitions of Section 19.1 have no acceptance example.
> REASONING: Section 19.1 lists eight MUST NOT obligations binding agents on `full` changes; only the algorithm of Section 19 itself is illustrated by AE-270, which does not exercise the prohibitions. SPEC-14 asks for an example for each `full` rule.
> DISPOSITION REQUIRED: Add an acceptance example covering the prohibitions or clarify the reach of SPEC-14.
> FINDING RF-X-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 5.6; lines 573-573; quote "A section that the table does not name as `full` only applies to both method profiles."
> REFERENCE: file SPEC; section 11.3; lines 1474-1481; quote "An AI agent MUST:"
> SUMMARY: Several further normative rules in shared sections (11.3, 12.1, 15, 17, 18) have no acceptance example; the reach of SPEC-14 is ambiguous.
> REASONING: Sections 11.3, 12.1, 15, 17 and 18 apply to both method profiles under the Section 5.6 table and contain normative MUST and MUST NOT rules with no acceptance example. Whether SPEC-14's "each `full` rule" covers rules of sections shared by both profiles is not determinable from the text.
> DISPOSITION REQUIRED: Clarify whether SPEC-14 extends to rules of sections applying to both profiles, and add examples where it does.
> FINDING RF-X-006
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 25.3; lines 4694-4694; quote "A Markdown document, such as the specification of a change or the change specification of a `full` change, has no schema and no schema version."
> SUMMARY: Section 25.3 narrows schema_version to machine-readable files and excludes Markdown, while O-7 and SPEC-18 say every artifact carries schema_version.
> REASONING: O-7 states "Every artifact carries `schema_version`" and SPEC-18 repeats it. Section 25.3 limits the field to the project configuration, integration mappings, the change definition and the state document, and declares that a Markdown document has no schema and no schema version. Change specifications, plans and other governed artifacts are thereby outside the unknown-version refusal and the migration rule. An implementer could read the requirement more broadly than the text implements.
> DISPOSITION REQUIRED: Owner decision whether "every artifact" means every governed artifact or only schema-governed machine-readable files; align text or requirement.
> FINDING RF-X-007
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 24.4; lines 3688-3688; quote "Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor or an equivalent mechanism"
> REFERENCE: file SPEC; section 24.3; lines 3534-3534; quote "This specification assigns no minimum to a compliance profile (Section 5.1): a compliance profile reaches a level only through a gate or through the project configuration."
> SUMMARY: The anchor obligation is keyed to configuration requiring A2, not to a profile demanding high assurance as SPEC-05 states, and no compliance profile can demand it by itself.
> REASONING: SPEC-05 requires an external anchor or equivalent "where a profile demands high assurance". The text triggers the anchor only when the project configuration sets a minimum of A2. Since no minimum is assigned to any compliance profile, even `regulated` does not demand a level, so a profile that demands high assurance without explicit configuration never triggers the anchor. The mechanism exists but is wired to a different trigger than the requirement states.
> DISPOSITION REQUIRED: Tie the anchor obligation to the profile-demand the requirement describes, or obtain an owner disposition confirming configuration-keyed triggering.
> FINDING RF-X-008
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 22.4; lines 2313-2313; quote "This is decided from the results that the history records and from the measurement of the scope, and not by running a command."
> SUMMARY: The guard verification that no hard fail is active reads only recorded results, so a hard fail condition that became active after the last recorded evaluation is not detected.
> REASONING: O-11 decides that CI integration checks "that no hard fail is active". Verification 5 of `guard` is decided from the results the history records plus the live scope measurement, because `guard` runs no command. For a hard fail gate with a command condition, a failure that became active after the last recorded evaluation leaves no recorded result, so `guard` answers `success` while a hard fail is in fact active. The limitation is disclosed ("it proves the record, not the outcome"), but the check as specified does not establish what O-11 asks it to check.
> DISPOSITION REQUIRED: Owner decision whether record-based detection satisfies O-11, or state in the rule that the check covers recorded hard failures only.
> FINDING RF-X-009
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 16.1; lines 1830-1830; quote "The conditions listed under Flow Gates, together with the scope, are the gate definitions of the change and are fixed when the change is approved (Section 24.1)."
> REFERENCE: file SPEC; section 24; lines 3108-3108; quote "The member `definitions` is the content hash of the set of the files under `docs/definitions/` (Section 25.2)."
> SUMMARY: Section 16.1 defines the full gate definitions as Flow Gates plus scope, while Section 24 also includes requirements, evidence commands and the project-wide definitions hash.
> REASONING: For `full`, Section 16.1 states that the gate definitions are the Flow Gates together with the scope. Section 24.1 and the parsed-value definition in Section 24 additionally fix the requirements with their evidence commands and the content hash of the files under docs/definitions/. The two statements of what the gate definitions comprise differ; the narrower one could mislead an implementer of the hash comparison.
> DISPOSITION REQUIRED: Align Section 16.1 with the fuller definition in Section 24.
> FINDING RF-X-010
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.8; lines 4165-4165; quote "and the answer is recorded as a human decision (Section 22.1)"
> SUMMARY: A `full` answer is called a human decision although a question owned by an agent is answered by an agent.
> REASONING: Section 24.8 allows a question owner to be a non-human participant, and only an owner who is a human requires a human answer. The sentence recording the `full` answer "as a human decision" conflicts with an agent answering its own question, and the term does not match Section 22.1, which lists an answer among the recorded human decisions.
> DISPOSITION REQUIRED: Reword so the record of an answer does not presuppose a human answerer, or restrict question owners to humans.
> FINDING RF-X-011
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.1; lines 4552-4552; quote "Given a `core` project and a `full` project, and in each of them two writers that both read that no state document of the change `c-1` exists"
> SUMMARY: Example AE-191 speaks of a `core` project and a `full` project, but a method profile is a property of a change, not of a project.
> REASONING: Section 5.6 fixes the method profile per change and forbids treating it as a project property beyond an optional default. The AE wording projects the profile onto the project, which cannot change behaviour but makes the example read incorrectly.
> DISPOSITION REQUIRED: Rephrase the example to name the method profile of the change.
> FINDING RF-X-012
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 22.4; lines 2317-2317; quote "`approval-stale` for the third"
> SUMMARY: One issue code `approval-stale` covers two distinct third-verification failures: an approval that is not current and an approval below the required level.
> REASONING: Verification 3 checks both that every approval is current for the content it names and that it has the required level. A single code for both causes makes the report ambiguous about which failure occurred; this cannot change behaviour but reduces diagnosability.
> DISPOSITION REQUIRED: Assign distinct issue codes, or state that the one code covers both causes.
> CHECKS PERFORMED:
> C1: Read the whole text and compared distant sections (transition tables of 8.3 and 23.4 against 22.2, 24.2, 24.7; gate-definition content of 16.1 against 24; question handling across 9.4, 10.4, 23.4, 24.8). Found the term mismatch of finding RF-X-009 and the wording conflicts of findings RF-X-010 and RF-X-011; otherwise the sections reconcile.
> C2: Traced O-1 to O-11: two profiles (5.6, 23), reversed non-goals with memory/MCP/web UI/orchestration absent and combination specified-not-built (5.3, 17), normative levels and statement with optional verifiers (24.3), JSON state (4.3, 25.1), fourth result blocked (22.2, both tables), reopen full-only (8.3, 23.4, 8.4), schema_version and explicit migration (25.3), core-only build with full refused (5.6), protections as invariants of both profiles (24), four of six layers in core (5.3), verify-only CI (22.4). Gaps reported as findings RF-X-006, RF-X-007 and RF-X-008.
> C3: Traced SPEC-01 to SPEC-18 to normative text: frozen gates (24.1), three-valued results (24.2), blocked envelope (22.2), levels and human-credential limit (24.3), consistency/completeness and anchor (24.4), scope and isolation (24.5), baselines (24.6), hard and soft failure with override (24.7), open questions (24.8), executable evidence (24.9), opt-in interpreter with the git-ignored-code consequence (24.10), profiles and movement by supersede (5.6), revised full carrying the protections and marked unimplemented (5.6, 24), JSON state and canonical form (25.1), six-layer resolution with core at four (5.3), reopen per profile (8.3, 23.4). Gaps reported as findings RF-X-001 to RF-X-007. SPEC-13 concerns repository files outside the inputs and could not be verified.
> C4: Examined testability and bypass: hash-of-parsed-definitions freezing with cancel exempt and supersede blocked (24.1), fail-closed verification and the signers file outside the repository (24.3), anchor limits against an actor who can write both (24.4, disclosed), scope blindness to ignored code (24.5, 24.10, disclosed), unfrozen interpreter (24.10, disclosed), state-conflict locking (25.1). The self-declared human prefix at A0 is a disclosed limit. The record-only hard-failure check of guard is reported as finding RF-X-008.
> C5: Checked the acceptance examples named in the text against their rules; sampled AEs for gate weakening (AE-219 to AE-228), evaluation (AE-280, AE-295 to AE-310), scope (AE-147 to AE-157, AE-282, AE-307), baselines (AE-87 to AE-96), questions (AE-171 to AE-182), canonical form (AE-183 to AE-196) and migration (AE-203 to AE-214); all found to follow from their rules. Examples missing for the rules of findings RF-X-001 to RF-X-005.
> C6: Searched the text for development artifacts, prototype identifiers, decision and requirement ids and local paths; none found. Vendor product names appear only in the unchanged non-normative examples of Section 14.2.
> C7: Compared BASE to SPEC for removed or relaxed protections: retry limits reclassified from a DoF category to soft failures is declared in the text (Section 12) and required by SPEC-08; open questions tightened from "answered or explicitly accepted" to answered via a recorded answer (9.5, 10.4, 24.8); the fail action narrowed to soft-failure disposition with hard failures decided by evaluating actions or cancel (8.3, 24.7); the weakening rule strengthened from silently to any weakening (5.3). No undeclared weakening found.
> C8: Sampled cross-references (4.3 to 24.1-24.5/24.7/24.8 and 25.1; 8.3 to 22.2, 24.1, 24.2, 24.7; 22.1 to 22.4, 23.4, 24.4, 24.8, 25.3; 11.2 field mapping to 25.1; AE-coverage pointers). No wrong section or example number found.
> LIMITS: SPEC-13 (no file under src/ggsad/ modified) could not be verified from the inputs. Acceptance-example coverage was assessed section by section; AE identifiers were spot-checked rather than exhaustively resolved. Tools used: read, grep, wc and sha256sum on the four input files. No file outside the working directory was opened.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RF-X

## Findings

| Finding | Severity | Reference | Summary | Disposition |
|---|---|---|---|---|
| RF-A-001 | MAJOR | file SPEC; section 4.3; lines 307-307; quote "enforced mechanically only for a change that has a state document" | The protections of Sections 24.1 to 24.8 are enforced mechanically only when a full change has a state document; a project without one loses all mechanical enforcement. |  |
| RF-A-002 | MAJOR | file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`" | The reserved-name check misses device names followed by an extension (for example `con.x`), which the same file systems also reserve. |  |
| RF-A-003 | MINOR | file SPEC; section 5.6; lines 577-577; quote "4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 16.1 to 16.4, and the diagram of Section 21" | The applicability table names 8.1 to 8.5 as full only, leaving the unnumbered preamble of section 8 applicable to both profiles by the table's own rule. |  |
| RF-A-004 | MINOR | file SPEC; section 8.3; lines 1019-1021; quote "an active Definition of Fail condition" | AE-244 does not state the severity of the active fail condition; the outcome `failed` follows only for severity `hard`. |  |
| RF-A-005 | MINOR | file SPEC; section 8.3; lines 904-904; quote "The change is closed, or no DoW condition is active" | The per-action table of rejected results omits the `gate-not-evaluable` rejection that AE-310 and Section 8.5 establish for wait, fail, and reopen. |  |
| RF-A-006 | INFO | file SPEC; section 5.3; lines 386-386; quote "The method profile (Section 5.6) and the compliance profile (Section 5.1) of a change are resolved together, and neither ranks above the other" | Layer 2 holds method profile and compliance profile with no ranking; the text does not say how a direct conflict between the two inside the layer resolves. |  |
| RF-B-001 | MINOR | file SPEC; section 12; lines 1495-1495; quote "as the earlier text of this method did" | Normative sentence cites the earlier text of the method, a document outside this specification, which breaks self-containment. |  |
| RF-B-002 | MINOR | file SPEC; section 12.2; lines 1519-1521; quote "Every fail rule MUST include:" | The mandatory-content list of a fail rule omits severity, which the following prose and the template require; whether a rule without severity is valid cannot be determined from the list. |  |
| RF-B-003 | MINOR | file SPEC; section 11.2; lines 1434-1441; quote "Every wait state MUST include:" | The wait-state template carries resume_at and describes it, yet the mandatory list does not require it, while the resume action prefers a recorded resume phase. |  |
| RF-B-004 | MAJOR | file SPEC; section 5.6; lines 577-577; quote "16.1 to 16.4" | Sections 16.1 to 16.4 are full-only and contain normative rules, but no acceptance example covers them, while requirement SPEC-14 asks that each full rule have one. |  |
| RF-B-005 | MINOR | file SPEC; section 12; lines 1493-1495; quote "A retry limit is a soft fail condition, so that reaching it pauses the flow for a human disposition" | The rule that a retry limit is a soft fail condition and does not terminate the flow is stated three times in Section 12. |  |
| RF-B-006 | INFO | file SPEC; section 12.1; lines 1505-1505; quote "exceeding a hard budget or cost limit," | A retry limit moved from the hard fail categories to a soft failure; the change is disclosed in the text and matches the soft-failure design, so it is recorded as an observation, not a defect. |  |
| RF-C-001 | MINOR | file SPEC; section 23.6; lines 2984-2984; quote "the evaluation MUST stop as soon as a gate decides the requested action" | Section 23.6 first says evaluation MUST stop as soon as a gate decides, then says a group is evaluated whole, two stop rules that read differently |  |
| RF-C-002 | MINOR | file SPEC; section 23.3; lines 2490-2490; quote "the member `gate` is the identifier of a done gate of the kind `check`, and the member `limit` is the limit of Section 24.2" | A retry_limit fail gate must name a check done gate, but no rule requires the named gate to exist in the same change definition |  |
| RF-D-001 | MAJOR | file SPEC; section 24.4; lines 3688-3688; quote "Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor or an equivalent mechanism" | The anchor requirement triggers only on a configured A2 minimum; a change whose gates alone require A2 gets no truncation detection. |  |
| RF-D-002 | MINOR | file SPEC; section 24.5; lines 3798-3798; quote "a segment that is exactly `**` matches any number of path segments, including none" | Whether the pattern lib/** matches the path lib itself, when ** stands for zero segments, is not stated. |  |
| RF-D-003 | MINOR | file SPEC; section 24.2; lines 3380-3380; quote "In `full`, it is a condition of a Flow Gates list (Section 16.1) that names a command." | In full, "check-command gate" is defined only for Flow Gates conditions, while AE-250 puts a check-command condition in the Definition of Done. |  |
| RF-D-004 | INFO | file SPEC; section 24.5; lines 3804-3804; quote "exactly two further names in the change directory are exempt: the in-progress file `state.json.tmp` and the lock object `state.json.lock`" | The unconditional exemption lets any file named state.json.tmp or state.json.lock in the change directory escape scope measurement, not only a genuine leftover. |  |
| RF-E-001 | MINOR | file SPEC; section 24.7; lines 4014-4014; quote "A retry limit (Section 24.2) is a fail condition of the severity `soft`, and a retry limit that declares the severity `hard` is invalid and MUST be rejected." | Whether a retry limit that declares no severity, or declares `soft`, is valid is left implicit and can be misread against the missing-severity rejection rule. |  |
| RF-E-002 | MINOR | file SPEC; section 24.7; lines 4031-4031; quote "It lapses when its N attempts are used up and when the gate definitions are amended." | "lapses when its N attempts are used up and when the gate definitions are amended" reads as a conjunction of two conditions rather than two independent lapse triggers. |  |
| RF-E-003 | MINOR | file SPEC; section 25.3; lines 4708-4708; quote "It takes the file and optionally a target version, which is a supported version that is higher than the version of the file" | The result of a `migrate` request whose target version is unsupported, or is supported but unreachable by a chain of steps, is unspecified. |  |
| RF-E-004 | MINOR | file SPEC; section 24.9; lines 4344-4344; quote "an evidence command that is `satisfied` is bound to R1 and the action is requested again" | AE-168 does not state whether the gate definitions were approved, so it can be read as binding a new evidence command without the re-approval that Sections 24.1 and 24.9 require. |  |
| RF-X-001 | BLOCKING | file SPEC; section 5.6; lines 577-577; quote "4.1, 5.5, 6, 7, 8.1 to 8.5, 9, 10, 16.1 to 16.4, and the diagram of Section 21" | Sections 16.1 to 16.4 are marked full-only yet contain normative rules and no acceptance example, which SPEC-14 requires for each full rule. | fix |
| RF-X-002 | MAJOR | file SPEC; section 13.1; lines 1570-1576; quote "When a requirement conflicts with an ADR, the agent MUST:" | Section 13 (ADR conflicts, specification drift, breaking changes) has MUST rules but no acceptance example anywhere in the section. |  |
| RF-X-003 | MAJOR | file SPEC; section 14.3; lines 1628-1637; quote "A Pair Review cycle MUST:" | Sections 14.3 to 14.5 (review cycle, findings, review artifacts) contain MUST rules with no acceptance example. |  |
| RF-X-004 | MAJOR | file SPEC; section 19.1; lines 2133-2142; quote "An AI agent MUST NOT:" | The agent prohibitions of Section 19.1 have no acceptance example. |  |
| RF-X-005 | MINOR | file SPEC; section 5.6; lines 573-573; quote "A section that the table does not name as `full` only applies to both method profiles." | Several further normative rules in shared sections (11.3, 12.1, 15, 17, 18) have no acceptance example; the reach of SPEC-14 is ambiguous. |  |
| RF-X-006 | MAJOR | file SPEC; section 25.3; lines 4694-4694; quote "A Markdown document, such as the specification of a change or the change specification of a `full` change, has no schema and no schema version." | Section 25.3 narrows schema_version to machine-readable files and excludes Markdown, while O-7 and SPEC-18 say every artifact carries schema_version. |  |
| RF-X-007 | MAJOR | file SPEC; section 24.4; lines 3688-3688; quote "Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor or an equivalent mechanism" | The anchor obligation is keyed to configuration requiring A2, not to a profile demanding high assurance as SPEC-05 states, and no compliance profile can demand it by itself. |  |
| RF-X-008 | MAJOR | file SPEC; section 22.4; lines 2313-2313; quote "This is decided from the results that the history records and from the measurement of the scope, and not by running a command." | The guard verification that no hard fail is active reads only recorded results, so a hard fail condition that became active after the last recorded evaluation is not detected. |  |
| RF-X-009 | MINOR | file SPEC; section 16.1; lines 1830-1830; quote "The conditions listed under Flow Gates, together with the scope, are the gate definitions of the change and are fixed when the change is approved (Section 24.1)." | Section 16.1 defines the full gate definitions as Flow Gates plus scope, while Section 24 also includes requirements, evidence commands and the project-wide definitions hash. |  |
| RF-X-010 | MINOR | file SPEC; section 24.8; lines 4165-4165; quote "and the answer is recorded as a human decision (Section 22.1)" | A `full` answer is called a human decision although a question owned by an agent is answered by an agent. |  |
| RF-X-011 | MINOR | file SPEC; section 25.1; lines 4552-4552; quote "Given a `core` project and a `full` project, and in each of them two writers that both read that no state document of the change `c-1` exists" | Example AE-191 speaks of a `core` project and a `full` project, but a method profile is a property of a change, not of a project. |  |
| RF-X-012 | MINOR | file SPEC; section 22.4; lines 2317-2317; quote "`approval-stale` for the third" | One issue code `approval-stale` covers two distinct third-verification failures: an approval that is not current and an approval below the required level. |  |

## Requestor notes

- The Requestor checked the format of each report and whether each reference resolves in the pinned text; it did not assess whether any finding is correct.
- Independence rests on the reviewer's different product, vendor and model, on separate sessions that share no context with the Requestor, and on the reviewer's own statement of identity in each report; the repository cannot show more.
- A finding's severity is the reviewer's; only the repository owner dispositions a finding.

This note is evidence only. It does not change the reviewed file.
