# Independent review: proposed normative method specification

- Independent review: reported
- Owner dispositions: recorded in the review disposition record
- Blocking findings: 6

## The text reviewed

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `ed758c46d5ac901359ab2c0df8e437ef89fed0f1` |
| Reviewed SHA-256 | `45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3` |
| Line count | `4649` |
| Diffstat | `1 file changed, 3268 insertions(+), 41 deletions(-)` |
| Commits touching the file | `36` |
| Owner approval record | `.planning/reviews/2026-10-25-normative-spec-owner-approval-record.md` |
| Owner approval record blob | `bf3420f84e04ababdf3e4588ecc150a7e1a9840f` |
| Run set | `a681b8fc5d9c` |
| Consent question | `Send the containment pilot and the six review passes (run set a681b8fc5d9c, model swe-2-medium, read-only configuration) to Devin now, knowing that sending is one-way and that no repeat of any run is covered by this consent?` |
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

- C1 Contradiction and ambiguity: whether any statements conflict, any term has two senses, or any rule leaves its outcome undetermined.
- C2 Owner decisions: whether each of the eleven owner decisions is implemented as chosen, none is contradicted, and none lacks corresponding text.
- C3 Requirements: whether each of the eighteen specification requirements is met by normative text, none is contradicted, and no requested content is missing.
- C4 Testability and bypass: whether rules can be tested from outside, whether a hostile participant could meet a rule in letter and defeat its purpose, and whether failure behaviour is specified.
- C5 Acceptance examples: whether each example follows from its rule and covers the case it names.
- C6 Self-containment: whether the text refers to development artifacts, prototype identifiers, project decision or requirement identifiers, tools outside the method, or local paths.
- C7 Weakening: whether any protection, MUST or SHOULD rule or prohibition of the base text is removed, relaxed or made conditional without saying so.
- C8 References and terms: whether section numbers, example numbers and cross-references are right and each term is defined before use.

## Severity scale

- BLOCKING: the text must not be treated as final until the finding is fixed or the repository owner dispositions it.
- MAJOR: a defect that an implementer or participant could plausibly act on incorrectly but that is not BLOCKING.
- MINOR: a defect of wording, structure or reference that cannot change what a conforming participant does.
- INFO: an observation or question that is not a defect.

## Passes

| Pass | Scope |
|---|---|
| RV-A | The header and sections 1 to 8 |
| RV-B | Sections 9 to 22 |
| RV-C | Section 23 |
| RV-D | Section 24 up to the end of 24.5 |
| RV-E | Sections 24.6 to 24.10 and section 25 |
| RV-X | The whole text, read across sections |

## Reports

Each report is quoted whole, line by line: a quote mark and a space are added at the start of each line, and an empty line becomes a quote mark alone. The only change made to a report is mechanical: line endings are converted to LF and each tab to four spaces.

### RV-A — The header and sections 1 to 8

> REPORT BEGIN RV-A
> IDENTITY: Devin, Cognition, SWE-2 Medium; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RV-A, header up to but not including section 9 (lines 1-1073)
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5
> FINDINGS: 4
> FINDING RV-A-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 8.3; lines 896-896; quote "wait when the new corrective scope's DoW determines a pause"
> REFERENCE: file SPEC; section 8.3; lines 909-909; quote "the corrective follow-up work is not authorized with a reason and a new goal-bound scope"
> SUMMARY: The reopen row allows a DoW pause, but the results table states reopen never answers blocked, leaving the pause result undetermined.
> REASONING: The transition-table row for reopen says the action waits when the new corrective scope's DoW determines a pause. A pause is a recorded evaluation and a state change, so it cannot be a rejection (nothing written, changed false) and cannot reasonably be success, since the reopen did not take effect. The only remaining result is blocked, yet the new rejected/blocked table at line 909 states reopen answers blocked never. The two normative statements cannot both hold, so the outcome of reopen under an active DoW condition cannot be determined from the text.
> DISPOSITION REQUIRED: Fix. Either permit reopen to answer blocked for a DoW pause, or state that a DoW pause is a rejection, and align the two tables.
> FINDING RV-A-002
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 8.3; lines 891-891; quote "when the precondition is not satisfied or DoF determines failure"
> REFERENCE: file SPEC; section 8.3; lines 911-911; quote "An action whose evaluation closes the change as failed answers"
> SUMMARY: The wait row rejects when DoF determines failure, but a DoF-determined failure must close the change and answer success, not a mutation-free rejection.
> REASONING: The wait row says the action is rejected without any partial mutation of persisted state when DoF determines failure. But DoF has first priority (Sections 8.4 and 8.5) and a hard fail condition closes the change as failed, which is a recorded state mutation, and the new sentence at line 911 states an action whose evaluation closes the change as failed answers success. A mutation-free rejection and a failure closure cannot both describe the same evaluation, so the outcome of wait under an active DoF condition is undetermined. This wording is inherited from BASE, but the newly added result model sharpens the conflict.
> DISPOSITION REQUIRED: Fix or owner decision. State whether wait under an active DoF condition closes the change as failed (answer success) or is refused, and align with Section 24.7.
> FINDING RV-A-003
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 8.3; lines 902-902; quote "an applicable gate does not allow the start"
> REFERENCE: file SPEC; section 8.5; lines 1060-1060; quote "the change waits, and a known hard failure is decided before it"
> SUMMARY: For start (and other actions that never answer blocked), the result of an applicable gate that cannot be evaluated is unspecified and conflicts with the rule that the change waits.
> REASONING: Section 8.5 and SPEC-02 require that a gate that cannot be evaluated is neither failed nor skipped and that the change waits. For start, fail, and reopen the rejected/blocked table lists blocked as never. A wait caused by a gate that cannot be evaluated is a recorded mutation, so it cannot be a rejection; the text does not say which result these actions answer in that case. An implementer cannot determine the outcome from the text, and different implementations could reject (dropping the evaluation) or close the change.
> DISPOSITION REQUIRED: Clarify. State per action how a gate that cannot be evaluated is answered when blocked is not available, or extend the blocked column accordingly.
> FINDING RV-A-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`"
> SUMMARY: The reserved-name check rejects bare device names but not extension forms such as nul.txt, which are also reserved on case-insensitive Windows file systems.
> REASONING: The rule reserves con, prn, aux, nul, com1-9 and lpt1-9 after case folding, so an identifier such as nul.txt is accepted by the syntax yet still names a reserved device on Windows file systems, where the reservation applies to the name before the extension. The stated purpose is that an identifier cannot escape or collide in the change directory; this corner defeats it on that platform.
> DISPOSITION REQUIRED: Clarify or fix. Either extend the reserved-name rule to cover the stem before a dot, or state that such identifiers are permitted.
> CHECKS PERFORMED:
> C1: Read sections header-8.5 in full and compared each changed statement with BASE. Found the reopen/DoW and wait/DoF outcome contradictions above and the unspecified not_evaluable handling for non-blocked actions; no other internal contradictions found.
> C2: Traced O-1, O-3, O-4, O-5, O-6, O-8, O-9 and O-10 into scope text: two method profiles (5.6), JSON state (4.3, 8.1), blocked result (8.3), reopen full-only (8.3, 8.4), full marked specified-but-not-implemented (5.6, line 571), four implemented layers for core (5.3, line 392). All consistent with the decisions; O-2, O-7 and O-11 are implemented outside this range and only referenced.
> C3: Checked SPEC-01 to SPEC-18 references within range: SPEC-02 (8.5 tri-state), SPEC-03 (8.3 result tables), SPEC-05/SPEC-06/SPEC-08 anchors (8.1, 6.1, 5.3), SPEC-12 (5.6), SPEC-14 (profile markers and acceptance examples per full rule), SPEC-15 (JSON state, JSON example), SPEC-16 (six layers, no weakening), SPEC-17 (reopen per profile). No requirement contradicted in range.
> C4: Examined gate-freezing hooks (3.3, 8.4 line 1020), identifier rejection (4.3), compliance-profile equality (5.6) and weakening checks (5.3 line 394) for bypass; the checks run at creation and again before gate approval, and cancel/supersede are exempt from the gate-definition comparison. No bypass found beyond the ambiguities reported.
> C5: Read every acceptance example in range (AE-01 to AE-08, AE-121 to AE-124, AE-217, AE-218 to AE-228, AE-229 to AE-248, AE-288, AE-290 to AE-293) against its rule; all follow from the named section. AE-229, AE-234, AE-235, AE-236 and AE-237 match their flow and precedence rules.
> C6: Searched for development-artifact and prototype references in range; sections 3.8, 5.3 and 5.6 cite only method-internal sections and AE identifiers, which are part of the specification. No external citations, tool names or local paths found.
> C7: Diffed BASE against SPEC line by line in range. The only relaxations are the new full-only exception for project-wide definitions (4.2), which BASE already admitted as an approved exception, and the change of silently weaken to weaken (5.3), which is a strengthening. No MUST or SHOULD protection of BASE was removed or made conditional.
> C8: Verified cross-references in range: Sections 13, 16.x, 22.2, 23.x, 24.x, 25.1 and the AE numbering are used consistently; the term method profile is defined in 5.6 before later uses, and compliance profile is used uniformly. No wrong section number found.
> LIMITS: Judged sections 9-25 only as needed to interpret in-range text. The not_evaluable outcome for non-blocked actions may be refined in Section 24.2, which is outside this pass. Tools used: Read, exec for sha256sum, wc and grep -n. No file outside the working directory was opened. The output directory was not listed before writing.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RV-A

### RV-B — Sections 9 to 22

> REPORT BEGIN RV-B
> IDENTITY: Devin, an interactive command line agent by Cognition, powered by the SWE-2 Medium model; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RV-B, sections 9 to 22 of SPEC.md (from heading 9 up to but not including heading 23)
> COVERAGE: 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3
> FINDINGS: 5
> FINDING RV-B-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 22.1; lines 2167-2167; quote "it appends an entry whose `action` is `ask` to the history of each change"
> SUMMARY: AE-287 records a question on a full change as an action named ask, but the Section 8.3 transition table for full defines no ask action.
> REASONING: AE-287 states that the record-a-question contract operation appends an entry whose `action` is `ask` to the history of each change, including the `full` change, and that the transitions of the `full` change are judged under the table of Section 8.3. The Section 8.3 transition table lists only `start`, `complete`, `wait`, `resume`, `fail`, `cancel`, `supersede`, and `reopen`; no `ask` action exists there, and the rejected/blocked table in 8.3 lists no case for it. Section 24.8 confirms the divergence: in `core` the `ask` action records a question, while in `full` a question is recorded in the state file or the inline record. An implementer cannot determine which action, if any, records a question for a `full` change, or whether `ask` is legal for it, so the texts cannot all hold together and the example does not follow from its rule.
> DISPOSITION REQUIRED: Fix or owner decision: either add an `ask` action for `full` to Section 8.3, or restate AE-287 and Section 24.8 so that the recording of a question on a `full` change is defined without an `ask` action.
> FINDING RV-B-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 11; lines 1362-1364; quote "DoW describes conditions under which the flow MUST pause in a controlled manner without being considered failed."
> REFERENCE: file SPEC; section 12; lines 1436-1436; quote "DoF describes conditions under which the flow MUST terminate unsuccessfully."
> SUMMARY: Sections 11 and 12 do not declare their method profile, unlike Sections 9 and 10, although a core change has no DoW or DoF.
> REASONING: Sections 9 and 10 each carry the sentence "This section specifies the `full` method profile (Section 5.6)." Sections 11 and 12 carry no such statement. Section 23.1 says a `core` change has "no Definition of Ready or Definition of Done per phase (Sections 9 and 10)" but is silent on Sections 11 and 12, and Section 20 maps a DoW condition to a wait gate and a DoF condition to a fail gate for `core`. A reader cannot tell from Sections 11 and 12 themselves whether their MUST rules bind a `core` change, a `full` change, or both; the examples AE-268 and AE-269 scope themselves to `full` without resolving the question. The defect is one of wording and cannot change what a conforming participant does once Section 20 and Section 23 are applied, so it is MINOR.
> DISPOSITION REQUIRED: Clarify: add a profile-applicability sentence to Sections 11 and 12 in the style of Sections 9 and 10.
> FINDING RV-B-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 12.2; lines 1462-1468; quote "permitted preservation actions"
> REFERENCE: file SPEC; section 12.2; lines 1490-1490; quote "`hard`"
> SUMMARY: The F-01 fail-rule template shows no fields for permitted preservation actions or required documentation, two of the five mandatory items.
> REASONING: Section 12.2 lists five mandatory items (trigger, required response, permitted preservation actions, final status, required documentation) and the text after the template adds severity as a sixth. The template itself names only Trigger, Required response, Final status, and Severity. Permitted preservation actions and required documentation appear only folded into the bullets of Required response, so a reader copying the template cannot see where the two mandatory items belong. The template was edited by this change (the Severity field was added), so the inconsistency is within the reviewed text, although the missing fields predate the change.
> DISPOSITION REQUIRED: Fix: extend the template so that every mandatory item has a visible place, or state that the Required response bullets carry the preservation actions and the documentation.
> FINDING RV-B-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 11.2; lines 1405-1405; quote "The field `resume_at` names the phase at which the change resumes, and it holds a phase identifier of Section 7."
> SUMMARY: The wait-state template and its explanation include the field resume_at, but the mandatory list and AE-268 omit it, so its optionality is undetermined.
> REASONING: The mandatory content list of Section 11.2 names six items and AE-268 tests exactly those six fields. The template and the explanatory sentence add a seventh field, `resume_at`, without stating whether a wait state without it is valid or rejected. The outcome of a `wait` request that omits `resume_at` cannot be determined from the text. This is a wording gap that pre-dates the change in part, but the template and the explanation were rewritten in this diff.
> DISPOSITION REQUIRED: Clarify: either add `resume_at` (or its absence rule) to the mandatory content, or state explicitly that it is optional and what happens when it is absent.
> FINDING RV-B-005
> SEVERITY: BLOCKING
> REFERENCE: file BASE; section 12.1; lines 785-785; quote "exceeding hard budget, cost, or retry limits"
> REFERENCE: file SPEC; section 12.1; lines 1454-1454; quote "A retry limit is a soft fail condition (Section 24.7)."
> SUMMARY: BASE listed exceeding retry limits among DoF conditions that MUST terminate the flow; SPEC downgrades a retry limit to a soft failure that only pauses it.
> REASONING: In BASE, Section 12 states that DoF describes conditions under which the flow MUST terminate unsuccessfully, and its typical categories include "exceeding hard budget, cost, or retry limits". SPEC splits that item: budget and cost stay in the list, but a retry limit is declared a soft fail condition, which under Section 12 and Section 24.7 pauses the flow for a human disposition instead of terminating it. The change is explicit and is consistent with the hard/soft model required by SPEC-08, so the weakening is not silent; nevertheless it relaxes a MUST-terminate protection of BASE, which the severity rule of this review classifies as BLOCKING for the owner to disposition.
> DISPOSITION REQUIRED: Owner decision: confirm that moving retry-limit exhaustion from a terminating fail condition to a soft fail condition is the intended weakening, or restore termination.
> CHECKS PERFORMED:
> C1: Read sections 9 to 22 in full and traced each cross-reference to Sections 5.3, 5.4, 5.6, 7, 8.3, 23, 24, and 25 that the changed text relies on. Found the `ask`-action contradiction of AE-287 with Section 8.3 (RV-B-001), the undeclared profile scope of Sections 11 and 12 (RV-B-002), and the undetermined optionality of `resume_at` (RV-B-004).
> C2: Verified in scope: O-1 and O-8 (sections 9, 10, 19, 20, 21 mark or describe `full` versus `core`), O-3 (human release approval and assurance-level claim in 10.8 and 14.2), O-4 (wait-state template moved to JSON in 11.2), O-5 (four results in 22.2, per-action rejected/blocked wording), O-7 (schema-version refusal codes in 22.2), O-9 (Sections 24 protections referenced throughout), O-10 (layer 6 statement in Section 17 matches Section 5.3). No decision contradicted except as recorded in RV-B-001.
> C3: Verified the in-scope parts of SPEC-03 (blocked result semantics match exactly), SPEC-04 (human claim at an assurance level, 14.2), SPEC-06 (allowed path list in 9.6, 10.6, 12.1, 16.1, 19), SPEC-07 (baseline note in 10.7 and 15), SPEC-08 (hard/soft split in 12), SPEC-09 (open questions in 9.4, 9.5, 10.4, 11.3, 20, 16.1), SPEC-10 (executable evidence in 10.7, 15, 16.1, 20), SPEC-12 (profile statements), SPEC-14 (full rules carry acceptance examples AE-260 to AE-270), SPEC-16 (integration mapping is layer 6 in Section 17), SPEC-18 (schema-version refusal in 22.2). No requirement contradicted in scope.
> C4: Checked the new envelope rules in 22.2 and 22.3 for bypass: `rejected`/`blocked` and `changed` combinations are pinned, non-success results require issues, only completion actions and `resume` answer `blocked`, and result names must be exact lowercase; the rules are testable from outside. No defect found beyond RV-B-001.
> C5: Read every acceptance example in scope (AE-260 to AE-270, AE-287, AE-111 to AE-116). Each follows from its rule except AE-287 (RV-B-001); AE-263 correctly shows Ready-to-Spec met with an unanswered question, matching the added sentence in 9.4.
> C6: The AE identifiers are the specification's own acceptance-example system, not project or prototype identifiers. Vendor names in 14.2 and 17 are marked illustrative and non-normative and pre-date the change. No new self-containment defect found.
> C7: Compared BASE and SPEC for the range. The only removed protection is the downgrade of retry-limit exhaustion (RV-B-005). The changes "answered or explicitly accepted" to "all open questions have been answered" in 9.5 and 10.4 are strengthenings consistent with SPEC-09, not weakenings.
> C8: Checked section references in scope: Sections 5.6, 7, 8.3, 11, 11.1, 22.1, 22.2, 23.2, 23.4, 23.6, 23.7, 24.1 to 24.10, 25.1, and 25.3 exist and say what the citing text claims, except that Section 8.3 contains no `ask` action (RV-B-001). The terms used in changed text (hard, soft, blocked, allowed path list, open question, method profile) are defined elsewhere in the document.
> LIMITS: I computed the four SHA-256 values with certutil-equivalent tooling (sha256sum) and used read-only file, search, and listing tools plus the permitted shell commands; no file outside the working directory was opened. Sections outside the pass range (notably 5, 8, 23, 24, 25) were read only as far as needed to judge the changed text; I did not verify the internal correctness of Section 23 or 24 beyond the points the in-scope text cites.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RV-B

### RV-C — Section 23

> REPORT BEGIN RV-C
> IDENTITY: Devin, an interactive command line agent by Cognition, powered by SWE-2 Medium; I share no session, prompt, notes or model with Claude Code.
> INPUT SPEC.md 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RV-C, section 23 of SPEC.md, from the heading `## 23. The `core` Profile` (line 2248) up to but not including `## 24.` (line 2950)
> COVERAGE: 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7
> FINDINGS: 3
> FINDING RV-C-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 23.4; lines 2448-2448; quote "and the evaluation of Section 23.6 finds no fail gate and no wait gate active"
> REFERENCE: file SPEC; section 23.4; lines 2473-2473; quote "including a fail gate, a wait gate, or a gate that cannot be evaluated that would decide against the start (issue code `start-blocked`)"
> SUMMARY: The `start` precondition names only active fail and wait gates, while the same table's rejected row also rejects when a gate cannot be evaluated.
> REASONING: The Precondition cell of the `start` row requires that the Section 23.6 evaluation find "no fail gate and no wait gate active". Read literally, a change whose gate condition cannot be evaluated (Section 23.6 step 2, which decides `waiting`) meets this precondition, so `start` could be read as permitted. The rejected-results row of the same table, and Section 23.6 itself ("The action `start` requires that none of the steps 1 to 4 would decide"), require rejection in that case. The two cells of one table admit two readings of the same case; an implementer reading only the precondition would start a change that the method intends to hold.
> DISPOSITION REQUIRED: Align the `start` precondition wording with Section 23.6, for example "the evaluation of Section 23.6 finds that none of the steps 1 to 4 decides".
> FINDING RV-C-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.3; lines 2394-2394; quote "- Covers: Section 12.2"
> SUMMARY: Example AE-271 sits in Section 23.3 and exercises the rule of Section 23.3, but its Covers tag cites Section 12.2, unlike the convention used by all other examples.
> REASONING: Every other acceptance example in Section 23 names the section whose rule it exercises. AE-271 validates a `core` fail gate that omits the items Section 12.2 makes mandatory; the rule that permits the omission is stated in Section 23.3 ("It states no required response, no permitted preservation actions, and no documentation"). Citing 12.2 as the covered section is defensible (the example justifies the exemption from 12.2) but breaks the document's own convention and may confuse traceability checks that map examples to the sections they cover.
> DISPOSITION REQUIRED: Change the Covers line to Section 23.3, or keep 12.2 if the owner confirms the convention is to name the relieved section; clarify.
> FINDING RV-C-003
> SEVERITY: INFO
> REFERENCE: file SPEC; section 23.4; lines 2452-2452; quote "Otherwise the change remains `waiting`, or becomes `closed` with the outcome `failed`, as Section 23.6 decides."
> SUMMARY: The `resume` row does not say that a soft fail found on resume replaces the wait record with one of kind `fail-gate`; Section 23.6 step 3 implies the replacement.
> REASONING: When `resume` is requested and the evaluation finds an active soft fail gate, Section 23.6 step 3 makes the change `waiting` with a wait record of kind `fail-gate`, which replaces the record (for example a `question` record) that caused the wait. The transition-table row says only "the change remains `waiting`" and is silent on the wait record. This is resolvable by reading Sections 23.5 and 23.6, so it is an observation rather than a defect.
> DISPOSITION REQUIRED: None required; optionally state in the `resume` row that the wait record is replaced as Section 23.6 decides.
> CHECKS PERFORMED:
> C1: Read all of Section 23 and cross-checked the transition table, the rejected/blocked table, and Section 23.6 against each other and against Sections 24.2 and 24.7 for consistency; found one internal ambiguity (RV-C-001), otherwise rules are mutually consistent.
> C2: Traced the owner decisions that touch this section: O-1 and O-8 (core profile specified, full marked elsewhere), O-4 (`state.json`, YAML definition), O-5 (fourth result `blocked` and per-action rejected/blocked table), O-6 (no `reopen` in core, `follows` instead), O-10 (four layers; base gates as layer 2 not weakenable). All are implemented as chosen in this range; none contradicted.
> C3: Checked the requirements that land in this range: SPEC-03 (blocked results per action, `rejected` never `changed`), SPEC-08 (hard close without human action, soft pause with bounded override), SPEC-09 (questions as state, structured answers, approval and close blocked), SPEC-17 (`reopen` absent from core). Satisfied; no contradiction found in this range.
> C4: Examined the transition table, evaluation order, base gates and wait records for untestable rules and bypasses (human-only actions listed, base gates non-removable and checked at creation and before approval, hand-edited state refused via Section 24.4); failure behaviour is specified, including a `start` that never closes a change.
> C5: Checked each acceptance example AE-09 to AE-59, AE-117 to AE-120, AE-215/216, AE-219/225 references, AE-271 to AE-277 against its stated rule; all follow from their rules. One Covers tag cites a different section than the rule exercised (RV-C-002).
> C6: Searched the range for development artifacts, prototype identifiers, decision or requirement ids, tool names and local paths; found none (only method artifact paths such as `specs/<change-id>/` and section references).
> C7: Section 23 is entirely new text; BASE.md ends at Section 22, so no protection, MUST or SHOULD rule of BASE.md exists in this range to be weakened. Nothing removed or relaxed.
> C8: Verified every cited section number in the range exists in SPEC.md (3.1, 3.7, 3.9, 4.1, 4.3, 5.1, 5.3, 5.6, 6, 7, 9, 10, 11.1, 11.2, 12.2, 14.5, 22.2/22.3, 23.x, 24.x, 25.1, 25.3); all resolve. Found the AE-271 Covers anomaly (RV-C-002) and the `start` precondition wording mismatch (RV-C-001).
> LIMITS: Verified text outside the range (Sections 5.3, 24.2, 24.7, 24.8, 24.9 headings) only as far as needed to judge the changed text in scope; requirements and decisions whose implementation lives outside Section 23 (for example SPEC-12 profile movement, SPEC-15 canonical form, SPEC-18 schema versions) were not fully traced. Tools used: Read, Grep, shell commands sha256sum, wc, grep, ls. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RV-C

### RV-D — Section 24 up to the end of 24.5

> REPORT BEGIN RV-D
> IDENTITY: Devin by Cognition, model SWE-2 Medium; I share no session, prompt, notes, or model with Claude Code.
> INPUT SPEC.md 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RV-D, Section 24 up to but not including Section 24.6 (SPEC.md lines 2950-3772)
> COVERAGE: 24, 24.1, 24.2, 24.3, 24.4, 24.5
> FINDINGS: 3
> FINDING RV-D-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 24.2; lines 3235-3235; quote "An action that evaluates gates decides from the results in this order, and the first rule that applies decides:"
> REFERENCE: file SPEC; section 24.2; lines 3245-3245; quote "the Definition of Ready of the current phase, the Definition of Done, and the Definition of Ready of the next phase"
> SUMMARY: Decision rules 1 to 5 rank only fail, wait, and done gates; how a not_satisfied Definition of Ready result in `full` is ranked is undefined.
> REASONING: In `full`, Section 24.2 prescribes five evaluation groups including the Definition of Ready of the current phase and of the next phase, so Ready conditions produce results that must be ranked by rules 1 to 5. Those rules name only a hard fail gate, a not_evaluable gate, a soft fail gate, a wait gate, and (for completing actions) a done gate. A Ready condition is none of these in the terms the section uses. If rules 1 to 5 are the complete decision procedure, a `complete` from `draft` whose current-phase DoR is not_satisfied matches no rule and the action would take effect, contradicting Section 8.3, which answers `blocked`. If rule 5 is read broadly so that a Ready condition counts as a done gate, then a not_satisfied next-phase DoR would make the change "not complete", contradicting Section 8.3, which prescribes `success` with the current phase preserved at status `done`, and AE-240. An implementer can plausibly choose either reading and act incorrectly.
> DISPOSITION REQUIRED: Clarify how Definition of Ready results map onto the decision rules, or state explicitly that Section 8.3 governs the outcomes of Ready conditions and that rules 1 to 5 apply to fail, wait, and done conditions only.
> FINDING RV-D-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24; lines 2993-2993; quote "See AE-249, AE-250, AE-251, AE-252, AE-253, AE-254, AE-255, AE-256, AE-257, AE-258, AE-259, AE-286."
> REFERENCE: file SPEC; section 24; lines 3035-3035; quote "AE-294 — Full: the scope is evaluated from the first approval of the gate definitions"
> SUMMARY: The example list after the realization table omits AE-294, which is placed in the same block and covers Section 24.5 (full).
> REASONING: The line "See AE-249 ... AE-259, AE-286" enumerates the acceptance examples that follow the realization table. AE-294 stands between AE-253 and AE-254 in that block and covers Section 24.5 (full), yet it is absent from the list. The list is therefore incomplete; a reader using it as an index would miss the example. The omission cannot change what a conforming participant does, so the severity is MINOR.
> DISPOSITION REQUIRED: Add AE-294 to the list (in the position matching its placement) or state that the list is not exhaustive.
> FINDING RV-D-003
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.2; lines 3247-3247; quote "The limit is a non-negative integer, and it is reached when the count is greater than or equal to the limit"
> SUMMARY: A retry limit of zero is permitted and is reached at a count of zero, so the fail condition it feeds is active before any failure is recorded.
> REASONING: The text admits every non-negative integer as a limit and defines reached as count greater than or equal to the limit. With a limit of zero the count, which starts at zero, already reaches it, so the fail condition is permanently active. This may be the intended semantics of a zero limit, but the specification neither says so nor gives an example; the observation is recorded so the owner can confirm the intent. It is not a defect as written.
> DISPOSITION REQUIRED: None required; confirm or rule out the always-active reading of a zero limit.
> CHECKS PERFORMED:
> C1: Read Sections 24 to 24.5 in full and traced every cross-reference to Sections 4.3, 5.4, 5.6, 8.3, 8.5, 9.6, 11.1, 12.2, 16.1, 22.2, 23.1 to 23.7, and 25.1 to 25.2 for consistency. Found the undetermined ranking of Definition of Ready results reported as RV-D-001; no other contradiction or undecidable rule found.
> C2: The decisions whose consequences touch this range are O-3 (assurance levels and signed-approval statement normative, verifiers optional: implemented in 24.3), O-9 (protections are invariants of both profiles: implemented by the opening of Section 24 and the realization table), and O-5 in part (the `blocked` row of the realization table matches Section 22.2). No decision is contradicted and none lacks corresponding text in this range.
> C3: SPEC-01 is satisfied by 24.1 (fixed at approval; edits block every operation except cancel, supersede, and re-approval); SPEC-02 by 24.2 (three-valued results, not_evaluable never a failure nor counted); SPEC-04 by 24.3 (A0 to A2, the statement fields operation, change, history position, signer, and content hash, optional verifiers, and the agent-with-credentials statement); SPEC-05 by 24.4 (consistency versus completeness and the anchor or equivalent where A2 is required); SPEC-06 by 24.5 (allowed path list, measurement against the base revision, hard failure, and isolation). No requirement text is contradicted and no asked content is missing.
> C4: Checked testability and bypass: the frozen-gate comparison covers re-approval and read-only operations; the fail-closed verification of 24.3 and the self-built statement prevent signature injection; the anchor rules, the non-replacement rule, and the limit that an actor who can write both history and anchor defeats them are all stated; the scope rule counts untracked files and exempts only the named record files. Found no bypass; noted the zero-limit edge as RV-D-003.
> C5: Checked each acceptance example in the range (AE-60, AE-75 to AE-86, AE-61 to AE-74, AE-125 to AE-136, AE-137 to AE-146, AE-147 to AE-157, AE-249 to AE-259, AE-278 to AE-286, AE-289, AE-294) against its rule and its Covers tag; all follow from their rules and name the case they cover.
> C6: Searched the range for development artifacts, decision and requirement identifiers, prototype names, tool names, and local paths; none found (version control, platform, and interpreter are named generically).
> C7: BASE.md ends at Section 22, so the whole reviewed range is new text; nothing in the range removes, relaxes, or makes conditional a protection of BASE.md.
> C8: Verified the referenced section numbers and terms used: Sections 22.2, 23.4, 23.6, 23.7, 24.1, 24.3, 24.4, 24.5, 24.7, 25.1, 25.2, 5.4, 5.6, 8.3, 8.5, 9.6, 10.7, 11.1, 12.2, 16.1, and 4.3 exist and say what the citing text claims; the term `not_applicable` is used before its marker discussion at line 3261 but the marker is introduced at line 3221. Found the AE-294 list omission reported as RV-D-002.
> LIMITS: The review used the Read tool, the Grep tool, and single sha256sum, wc, and grep commands; no file outside the working directory was opened and no other tool was used. Judgments about sections outside the range (for example 24.6 to 24.10 and 25.3) were made only by reading them as context, not by reviewing them. Whether the decision-rule gap of RV-D-001 is covered by later text was checked as far as the sections it cites; it was not fully re-derived against every section.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RV-D

### RV-E — Sections 24.6 to 24.10 and section 25

> REPORT BEGIN RV-E
> IDENTITY: Devin, an interactive command line agent from Cognition, powered by the SWE-2 Medium model; I share no session, prompt, notes or model with Claude Code: no.
> INPUT SPEC.md 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RV-E, sections 24.6 to 24.10 and section 25 of SPEC.md, from heading 24.6 to the end of the file.
> COVERAGE: 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 3
> FINDING RV-E-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 25.2; lines 4473-4473; quote "an implementation SHOULD classify a file as text only when its bytes are valid UTF-8 and hold no zero byte"
> SUMMARY: The text-versus-binary decision for content hashes is only a SHOULD, so two conforming implementations can hash the same file differently and break recorded approvals.
> REASONING: The content hash binds approvals (Section 24.3) and identifies frozen gate definitions (Section 24.1); a difference blocks every state-changing operation except cancel and supersede. Section 25.2 lets each implementation decide text versus binary from the bytes alone and only recommends the UTF-8/no-zero-byte rule. An implementation that hashes a valid UTF-8 file as binary produces a different content hash for a file with CRLF endings than one that normalizes line endings, so a hash recorded by one conforming implementation need not verify under another. The text admits that a hash is "comparable only with a content hash that an implementation computed with the same decision", but nothing requires the decision to be recorded or fixed, so a recorded hash cannot tell a verifier which rule produced it.
> DISPOSITION REQUIRED: Fix, or owner decision: either make the classification rule normative (MUST) or require the classification to be recorded with the hash so that approvals and frozen-gate comparisons stay verifiable across conforming implementations.
> FINDING RV-E-002
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 25.1; lines 4319-4319; quote "The writer names the version it read, which is the number of entries of the state document at that time"
> SUMMARY: The word "version" names an entry count in Section 25.1 and a schema version in Section 25.3, two senses of one term in adjacent sections.
> REASONING: Section 25.1 uses "version" for the number of entries a writer read before locking, while Section 25.3 uses "version" for the `schema_version` field of the same document, and Section 25.3 even speaks of "the latest recorded version" for the `after` record. A reader can resolve each use from context, but the reused term invites confusion between the optimistic-concurrency count and the schema version, especially since `state.json` carries both.
> DISPOSITION REQUIRED: Clarify wording, for example by calling the Section 25.1 value "the entry count read" or "read position", leaving "version" for the schema.
> FINDING RV-E-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.7; lines 3884-3884; quote "It lapses when its N attempts are used up and when the gate definitions are amended."
> SUMMARY: The override-lapse sentence joins its two triggers with "and", which can be misread as requiring both before the override lapses.
> REASONING: Read as a conjunction, the sentence would mean an override lapses only once its attempts are exhausted and the gate definitions are also amended; read as a list of triggers, it lapses on either. The examples AE-102 (attempts exhausted) and AE-103 (amendment alone) show the intended reading is either-trigger-lapses, so the normative sentence is looser than its examples.
> DISPOSITION REQUIRED: Fix: reword as "It lapses when its N attempts are used up, and it lapses when the gate definitions are amended" or "lapses as soon as either occurs".
> CHECKS PERFORMED:
> C1: I read Sections 24.6-24.10 and 25 in full and cross-checked statements against Sections 22.2, 23.4-23.7, 24.1-24.5, 8.3-8.5 and 11 that they invoke; I found no statement that cannot hold together with the rest, only the two-sense use of "version" reported as RV-E-002 and the ambiguous "and" reported as RV-E-003.
> C2: In scope, O-4 (state moves to `state.json`, canonical form for hashing, human-owned definitions stay YAML), O-5 (`blocked` recorded with `changed` true, e.g. AE-172, AE-182), and O-7 (every schema-governed artifact carries `schema_version`, unknown versions refused, migration explicit and recorded) are implemented in Sections 25.1-25.3 as chosen; no decision is contradicted and none lacks text in this range.
> C3: SPEC-07 is implemented in 24.6 (baseline satisfies when all failures are listed, names new failures, `not_evaluable` when unreadable); SPEC-08 in 24.7 (hard close without human action, soft wait with bounded override that lapses on amendment); SPEC-09 in 24.8 (questions as state, structured answers, approval and closure blocked); SPEC-10 in 24.9 (executable evidence bound to requirements, no requirements means no complete evidence); SPEC-11 in 24.10 (explicit opt-in `@interpreter` token, ignored-location caveat stated); SPEC-15 in 25.1-25.2; SPEC-18 in 25.3. Nothing a requirement asks for is missing in this range.
> C4: Rules are testable from outside; baselines are frozen with the gate hash so they cannot quietly hide a new failure, and failure behaviour (rejection at approval, `state-conflict`, `error` on failed atomic write) is specified. The only weakness found is the non-normative text/binary classification of Section 25.2, reported as RV-E-001.
> C5: I checked every example AE-87 to AE-110, AE-158 to AE-170, AE-171 to AE-182, AE-183 to AE-202, AE-203 to AE-214, AE-254, AE-277, AE-279 to AE-286 and AE-294 in or consulted for this range; each follows from its rule and names the case it covers.
> C6: The range cites no development artifacts, prototype identifiers, decision or requirement ids, tool names outside the method, or local paths; the `.ggsad/config.yaml` name is a method artifact defined by the specification itself.
> C7: BASE.md ends at Section 22.3, so all text in this range is new; I compared the range with BASE.md and found no protection, MUST, SHOULD or prohibition of BASE.md that this text removes, relaxes or makes conditional.
> C8: Cross-references I verified resolve correctly: Section 24 (code-point comparison, line 2963), Sections 22.1, 22.2, 23.1-23.7, 24.1-24.5, 8.3-8.5, 9.6, 10.7, 11.1-11.2, 12.2, 15, 16.1 (Open Questions and Evidence Commands headings exist at lines 1768 and 1721), and 20; example identifiers are unique and terms are used after definition.
> LIMITS: I did not recompute the literal digest values quoted in AE-183 and AE-184 because verifying them would require writing a file or piping data, which the brief forbids. I opened no file outside my working directory. Tools used: Read, Grep, and the single commands ls, wc, grep, sha256sum.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RV-E

### RV-X — The whole text, read across sections

> REPORT BEGIN RV-X
> IDENTITY: Devin, Cognition, model SWE-2 Medium; I share no session, prompt, notes, or model with Claude Code: no
> INPUT SPEC.md 45ba09d929758f9aa7d4640d93ef07a7f994c497eed2999aad9fceeb2ef34ca3
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RV-X, the whole text across sections, header to end; every owner decision and every requirement traced to its implementing text, and conflicts between distant sections sought.
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 24, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 7
> FINDING RV-X-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 8.3; lines 891-891; quote "Reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure"
> REFERENCE: file SPEC; section 24.7; lines 3871-3871; quote "the action MUST close the change as failed in the same state mutation"
> SUMMARY: The wait row of the Section 8.3 transition table rejects without mutation when DoF determines failure; Section 24.7 requires a close as failed that answers success.
> REASONING: The `wait` row, unchanged from BASE, instructs the implementation to reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure. Under the new Section 24.7, every action that evaluates gates and finds an active fail condition of the severity `hard` MUST close the change as failed in the same state mutation, and that action answers `success`. The gate order of the `wait` row is DoF then DoW, so `wait` does evaluate DoF. A `wait` request on a change with an active hard fail condition therefore has two contradictory prescribed outcomes: rejection with `changed` false and nothing written, or `success` with the change closed as failed and an entry appended. The outcome cannot be determined from the text. The same sentence pattern in BASE was harmless because no precise result envelope existed; Sections 22.2 and 24.7 now make the choice normative and contradictory.
> DISPOSITION REQUIRED: fix or owner decision. State for `wait` whether an active hard fail condition closes the change as failed with result `success` (Section 24.7) or whether the action is rejected, and align the row and the rejected/blocked table with the answer.
> FINDING RV-X-002
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 8.3; lines 896-896; quote "wait when the new corrective scope's DoW determines a pause"
> REFERENCE: file SPEC; section 8.3; lines 909-909; quote "or the resume-phase DoR is not satisfied"
> REFERENCE: file SPEC; section 22.2; lines 2182-2182; quote "Only the actions that complete a change or a phase and the action `resume` can answer `blocked`"
> SUMMARY: The reopen row prescribes a wait when the new scope's DoW pauses, but the results table says reopen answers blocked never, so the result of a paused reopen is undetermined.
> REASONING: The `reopen` row of the transition table states that the action waits when the new corrective scope's Definition of Wait determines a pause. Entering a wait changes the recorded state, which requires `changed` true, and under Section 22.2 only the actions that complete a change or a phase and `resume` can answer `blocked` with `changed` true. The adjacent Rejected and Blocked Results table assigns `reopen` exactly three `rejected` cases, none of them a DoW pause, and `blocked` never. A `reopen` whose new-scope DoW is active therefore has no valid result envelope: it cannot be `rejected` (a wait is a mutation), cannot be `blocked` (never listed), and cannot be `success` (no transition to a phase occurred). The text does not say whether the pause is rejected, turns the closed change `waiting`, or is impossible.
> DISPOSITION REQUIRED: fix or owner decision. Either add a `blocked` or a `rejected` case for a new-scope DoW pause on `reopen`, or state that an active DoW of the new scope makes the precondition fail, and update the table accordingly.
> FINDING RV-X-003
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 22.1; lines 2158-2158; quote "report on a change, as the read-only actions `check`, `review`, and `guard` do"
> REFERENCE: file SPEC; section 23.4; lines 2461-2461; quote "They are not rows of the table"
> SUMMARY: Decision O-11 (verify-only CI integration, also reversed into scope by O-2) has no corresponding text; `guard` is named but its checks are never specified.
> REASONING: DECISIONS.md O-2 reverses the Milestone 1 non-goal for CI integration, and O-11 decides what CI integration means: CI checks history integrity and the anchor, that the frozen gates match the approval, that approvals are current and at the required level, the scope against the base, and that no hard fail is active, and it does not execute the change's own commands with CI's privileges. No section of SPEC.md states any of this. The read-only actions `check`, `review`, and `guard` are named in Sections 22.1 and 23.4, but nowhere is it defined what each verifies or that the verification is verify-only and never executes the change's commands. An implementer has no normative text to build the decided CI behavior against, and a participant cannot tell whether CI proves the record or the outcome. Nothing contradicts the decision; the decision simply has no implementing text.
> DISPOSITION REQUIRED: owner decision or fix. Either add normative text for verify-only CI (for example defining `guard`) or record a decision that this specification does not carry the CI integration rules.
> FINDING RV-X-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 8.5; lines 1058-1058; quote "Evaluation MUST stop as soon as a gate determines the requested action's outcome"
> REFERENCE: file SPEC; section 8.5; lines 1060-1060; quote "the gates are evaluated by group, that a group is evaluated whole"
> SUMMARY: Section 8.5 keeps the per-gate stop rule and adds group-whole evaluation in the same paragraph; the two stopping rules differ in wording.
> REASONING: The unchanged sentence requires evaluation to stop as soon as a single gate determines the outcome, while the new sentence and Section 24.2 require a group to be evaluated whole and evaluation to stop only after the first group that decides. Section 24.2 declares itself a refinement, so behavior is arguably settled, but the two adjacent sentences in Section 8.5 state different stopping rules and a reader cannot tell from Section 8.5 alone which governs. The defect is wording only; the refined rule is reachable in Section 24.2.
> DISPOSITION REQUIRED: clarify. Amend the older sentence to refer to the group that decides, or state that it is superseded by the group rule of Section 24.2.
> FINDING RV-X-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.2; lines 3243-3243; quote "the wait record created by rule 2 replaces the earlier record, whose resume condition was met"
> SUMMARY: Section 24.2 says only that a rule-2 wait record replaces the earlier record on resume; whether a rule-3 soft-fail wait record replaces it is unstated.
> REASONING: On `resume` of a `core` `waiting` change, the text specifies that a wait record created by rule 2 (a gate that cannot be evaluated) replaces the earlier record. If the evaluation instead finds an active soft fail condition under rule 3, the change waits with a wait record of kind `fail-gate` under Sections 23.5 and 24.7, but the text does not say that this record replaces the earlier one. A reader can infer replacement because a `core` change has at most one wait record (Section 23.5), but the rule is not stated where it applies and an implementer could plausibly record or report it differently.
> DISPOSITION REQUIRED: clarify. State that a wait record created by any deciding rule replaces the earlier record on `resume`, or name the rules that do so.
> FINDING RV-X-006
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.2; lines 3247-3247; quote "The limit is a non-negative integer, and it is reached when the count is greater than or equal to the limit"
> SUMMARY: A retry limit of zero is a valid non-negative integer and makes the soft fail condition active before any attempt; the text does not address this edge.
> REASONING: Because the limit is reached when the count is greater than or equal to it, a limit of zero is reached with a count of zero, so the fail condition is active from the first evaluation. Nothing forbids or explains this value; it may be intended (zero further attempts granted), but it is worth noting because AE-70 rejects negative and non-integer limits while accepting zero without comment.
> DISPOSITION REQUIRED: none required; an owner may clarify whether a limit of zero is intended to be valid.
> FINDING RV-X-007
> SEVERITY: INFO
> REFERENCE: file SPEC; section 24.4; lines 3551-3551; quote "Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor"
> SUMMARY: The anchor requirement of SPEC-05 is keyed to a configuration that requires A2; no compliance profile can demand it, since profiles assign no minimum level.
> REASONING: SPEC-05 asks for an external anchor or equivalent where a profile demands high assurance. The text implements this as a MUST where the applicable configuration requires approvals at level A2, and Section 24.3 states that no minimum is assigned to a compliance profile, so a level is reached only through a gate or the project configuration. In substance the mapping is defensible, because an A2 requirement is the only operative form of a high-assurance demand in the text, but a reader looking for a profile-level trigger finds none.
> DISPOSITION REQUIRED: none required; an owner may confirm that the A2-configuration trigger is the intended reading of a profile demanding high assurance.
> CHECKS PERFORMED:
> C1: I compared the transition tables of Sections 8.3 and 23.4, the result rules of Section 22.2, the evaluation orders of 8.5, 23.6 and 24.2, and the failure rules of 24.7 against one another and against each action row; findings RV-X-001 and RV-X-002 are contradictions and RV-X-005 an ambiguity found this way; no other cross-section contradiction found.
> C2: I traced each decision O-1 to O-11: O-1 (two profiles, Section 5.6), O-3 (24.3 normative levels, optional verifiers), O-4 (state.json and canonical form, Section 25), O-5 (fourth result blocked, 22.2 and both per-action tables), O-6 (reopen full only, absent from 23.4), O-7 (schema_version, refusal, explicit migrate, 25.3), O-8 (full specified but not implemented, 5.6), O-9 (protections as invariants of both profiles, Section 24), O-10 (core implements layers 1, 2, 3, 5 of six, 5.3) are implemented as chosen; O-2 is implemented for profile resolution and the gate engine but its CI part has no text, and O-11 has no corresponding text: finding RV-X-003.
> C3: I traced SPEC-01 to SPEC-18: 01 (24.1), 02 (24.2), 03 (22.2), 04 (24.3 with AE-134), 05 (24.4 anchor or equivalent), 06 (24.5), 07 (24.6), 08 (24.7 with bounded override), 09 (24.8), 10 (24.9), 11 (24.10 with the ignored-location consequence), 12 (5.6 table and supersede move), 14 (protections carried into full with AE-249 to AE-259 examples), 15 (25.1 and converted examples), 16 (5.3 no-weakening, four of six layers), 17 (reopen per profile), 18 (25.3) are satisfied; SPEC-13 concerns files outside this review; no requirement contradicted.
> C4: I examined testability and bypass: frozen-gate comparison is mechanical and exempts only cancel, supersede and re-approval; retry counting is defined; the lock and atomic write are testable; acknowledged limits (actor writing history and anchor, agent holding credentials, ignored code) are stated honestly; findings RV-X-001, RV-X-002 and RV-X-005 are cases where failure behavior is not fully specified.
> C5: I read the acceptance examples against their rules; the new examples AE-218 to AE-294 and AE-01 to AE-59 follow from their rules and name their covered sections; I could not recompute the SHA-256 literals of AE-183 and AE-184, so their correctness is unverified.
> C6: I searched for development artifacts and project identifiers: no prototype names, requirement ids, decision ids, local paths or tool names outside the method's own vocabulary; `docs/definitions/`, `.ggsad/config.yaml` and `state.json.tmp` are artifacts of the method itself; the term reference implementation is a category of the document map.
> C7: I compared every changed line of BASE against SPEC via a full diff: the transition rows changed from reject to record-and-blocked per O-5; the reopen row gained the `full` only marker per O-6; state.yaml became state.json per O-4; open questions changed from answered or accepted to answered per the stated acceptance-is-an-answer rule; the hard-fail category entry for retry limits became a soft fail condition as Section 24.7 declares; no protection was removed or relaxed without being stated.
> C8: I checked cross references in the new text: Sections 22.2, 22.3, 23.x, 24.x, 25.x, 16.1, 16.4, 11.1, 11.2, 12.2, 9.6, 5.3, 5.6, 8.3 to 8.5 and the wait categories all resolve; the 294 AE identifiers are unique; terms such as base gates, check-command gate, blocked, and method profile are defined before or at their use; no wrong section number found.
> LIMITS: Unchanged prose of BASE-length sections was reviewed mainly through diff context and targeted reads for judging changed text, not line by line. I could not recompute the SHA-256 example values in AE-183 and AE-184 or any other cryptographic literal, because the permitted commands do not allow hashing a literal string. I did not verify that every `full` rule carries an acceptance example, only that the added AE-249 to AE-294 set covers each protection; SPEC-13 concerns repository files that are not inputs and could not be checked. Tools used: Read, Grep (file search), and the single commands ls, wc, grep, diff, and sha256sum. File opened outside the working directory: the overflow output file of the diff command, content.txt under the tool's devin.exe-overflows temporary directory.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RV-X

## Findings

| Finding | Severity | Reference | Summary | Disposition |
|---|---|---|---|---|
| RV-A-001 | BLOCKING | file SPEC; section 8.3; lines 896-896; quote "wait when the new corrective scope's DoW determines a pause" | The reopen row allows a DoW pause, but the results table states reopen never answers blocked, leaving the pause result undetermined. | fix |
| RV-A-002 | BLOCKING | file SPEC; section 8.3; lines 891-891; quote "when the precondition is not satisfied or DoF determines failure" | The wait row rejects when DoF determines failure, but a DoF-determined failure must close the change and answer success, not a mutation-free rejection. | fix |
| RV-A-003 | MAJOR | file SPEC; section 8.3; lines 902-902; quote "an applicable gate does not allow the start" | For start (and other actions that never answer blocked), the result of an applicable gate that cannot be evaluated is unspecified and conflicts with the rule that the change waits. | fix |
| RV-A-004 | MINOR | file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`" | The reserved-name check rejects bare device names but not extension forms such as nul.txt, which are also reserved on case-insensitive Windows file systems. |  |
| RV-B-001 | BLOCKING | file SPEC; section 22.1; lines 2167-2167; quote "it appends an entry whose `action` is `ask` to the history of each change" | AE-287 records a question on a full change as an action named ask, but the Section 8.3 transition table for full defines no ask action. | fix |
| RV-B-002 | MINOR | file SPEC; section 11; lines 1362-1364; quote "DoW describes conditions under which the flow MUST pause in a controlled manner without being considered failed." | Sections 11 and 12 do not declare their method profile, unlike Sections 9 and 10, although a core change has no DoW or DoF. |  |
| RV-B-003 | MINOR | file SPEC; section 12.2; lines 1462-1468; quote "permitted preservation actions" | The F-01 fail-rule template shows no fields for permitted preservation actions or required documentation, two of the five mandatory items. |  |
| RV-B-004 | MINOR | file SPEC; section 11.2; lines 1405-1405; quote "The field `resume_at` names the phase at which the change resumes, and it holds a phase identifier of Section 7." | The wait-state template and its explanation include the field resume_at, but the mandatory list and AE-268 omit it, so its optionality is undetermined. |  |
| RV-B-005 | BLOCKING | file BASE; section 12.1; lines 785-785; quote "exceeding hard budget, cost, or retry limits" | BASE listed exceeding retry limits among DoF conditions that MUST terminate the flow; SPEC downgrades a retry limit to a soft failure that only pauses it. | fix |
| RV-C-001 | MAJOR | file SPEC; section 23.4; lines 2448-2448; quote "and the evaluation of Section 23.6 finds no fail gate and no wait gate active" | The `start` precondition names only active fail and wait gates, while the same table's rejected row also rejects when a gate cannot be evaluated. | fix |
| RV-C-002 | MINOR | file SPEC; section 23.3; lines 2394-2394; quote "- Covers: Section 12.2" | Example AE-271 sits in Section 23.3 and exercises the rule of Section 23.3, but its Covers tag cites Section 12.2, unlike the convention used by all other examples. |  |
| RV-C-003 | INFO | file SPEC; section 23.4; lines 2452-2452; quote "Otherwise the change remains `waiting`, or becomes `closed` with the outcome `failed`, as Section 23.6 decides." | The `resume` row does not say that a soft fail found on resume replaces the wait record with one of kind `fail-gate`; Section 23.6 step 3 implies the replacement. |  |
| RV-D-001 | MAJOR | file SPEC; section 24.2; lines 3235-3235; quote "An action that evaluates gates decides from the results in this order, and the first rule that applies decides:" | Decision rules 1 to 5 rank only fail, wait, and done gates; how a not_satisfied Definition of Ready result in `full` is ranked is undefined. | fix |
| RV-D-002 | MINOR | file SPEC; section 24; lines 2993-2993; quote "See AE-249, AE-250, AE-251, AE-252, AE-253, AE-254, AE-255, AE-256, AE-257, AE-258, AE-259, AE-286." | The example list after the realization table omits AE-294, which is placed in the same block and covers Section 24.5 (full). |  |
| RV-D-003 | INFO | file SPEC; section 24.2; lines 3247-3247; quote "The limit is a non-negative integer, and it is reached when the count is greater than or equal to the limit" | A retry limit of zero is permitted and is reached at a count of zero, so the fail condition it feeds is active before any failure is recorded. |  |
| RV-E-001 | MAJOR | file SPEC; section 25.2; lines 4473-4473; quote "an implementation SHOULD classify a file as text only when its bytes are valid UTF-8 and hold no zero byte" | The text-versus-binary decision for content hashes is only a SHOULD, so two conforming implementations can hash the same file differently and break recorded approvals. | fix |
| RV-E-002 | MINOR | file SPEC; section 25.1; lines 4319-4319; quote "The writer names the version it read, which is the number of entries of the state document at that time" | The word "version" names an entry count in Section 25.1 and a schema version in Section 25.3, two senses of one term in adjacent sections. |  |
| RV-E-003 | MINOR | file SPEC; section 24.7; lines 3884-3884; quote "It lapses when its N attempts are used up and when the gate definitions are amended." | The override-lapse sentence joins its two triggers with "and", which can be misread as requiring both before the override lapses. |  |
| RV-X-001 | BLOCKING | file SPEC; section 8.3; lines 891-891; quote "Reject without any partial mutation of persisted state when the precondition is not satisfied or DoF determines failure" | The wait row of the Section 8.3 transition table rejects without mutation when DoF determines failure; Section 24.7 requires a close as failed that answers success. | fix |
| RV-X-002 | BLOCKING | file SPEC; section 8.3; lines 896-896; quote "wait when the new corrective scope's DoW determines a pause" | The reopen row prescribes a wait when the new scope's DoW pauses, but the results table says reopen answers blocked never, so the result of a paused reopen is undetermined. | fix |
| RV-X-003 | MAJOR | file SPEC; section 22.1; lines 2158-2158; quote "report on a change, as the read-only actions `check`, `review`, and `guard` do" | Decision O-11 (verify-only CI integration, also reversed into scope by O-2) has no corresponding text; `guard` is named but its checks are never specified. | fix |
| RV-X-004 | MINOR | file SPEC; section 8.5; lines 1058-1058; quote "Evaluation MUST stop as soon as a gate determines the requested action's outcome" | Section 8.5 keeps the per-gate stop rule and adds group-whole evaluation in the same paragraph; the two stopping rules differ in wording. |  |
| RV-X-005 | MINOR | file SPEC; section 24.2; lines 3243-3243; quote "the wait record created by rule 2 replaces the earlier record, whose resume condition was met" | Section 24.2 says only that a rule-2 wait record replaces the earlier record on resume; whether a rule-3 soft-fail wait record replaces it is unstated. |  |
| RV-X-006 | INFO | file SPEC; section 24.2; lines 3247-3247; quote "The limit is a non-negative integer, and it is reached when the count is greater than or equal to the limit" | A retry limit of zero is a valid non-negative integer and makes the soft fail condition active before any attempt; the text does not address this edge. |  |
| RV-X-007 | INFO | file SPEC; section 24.4; lines 3551-3551; quote "Where the applicable configuration requires approvals at the level A2 (Section 24.3), the history of a change MUST have an anchor" | The anchor requirement of SPEC-05 is keyed to a configuration that requires A2; no compliance profile can demand it, since profiles assign no minimum level. |  |

## Requestor notes

- The Requestor checked the format of each report and whether each reference resolves in the pinned text; it did not assess whether any finding is correct.
- Independence rests on the reviewer's different product, vendor and model, on separate sessions that share no context with the Requestor, and on the reviewer's own statement of identity in each report; the repository cannot show more.
- A finding's severity is the reviewer's; only the repository owner dispositions a finding.

This note is evidence only. It does not change the reviewed file.
