# Independent review, round 2: proposed normative method specification

- Independent review: reported
- Owner dispositions: recorded in the review disposition record
- Blocking findings: 3

## The text reviewed

| Field | Value |
|---|---|
| Reviewed file | `docs/method/GG-SAD_normative_method_specification.md` |
| Base blob | `da29d6f3bdef2e88fdd85a762939017d7d7034fa` |
| Result blob | `93f8278f1b0427444016cdbfa4b0e4ff9d16d369` |
| Reviewed SHA-256 | `6c0e86dd39e74242566755db6702972d893a83cc4827d9fc7e4805f89db85d91` |
| Line count | `4770` |
| Diffstat | `1 file changed, 3393 insertions(+), 45 deletions(-)` |
| Commits touching the file | `46` |
| Owner approval record | `.planning/reviews/2026-10-26-normative-spec-fix-round-approval-record.md` |
| Owner approval record blob | `456f0aa23ac63021e9958a4c6ccd91dab0680d3c` |
| Run set | `22ea024ce244` |
| Consent question | `May I send the test run and the three review passes (run set 22ea024ce244, model swe-2-medium) to Devin now? Sending cannot be undone, and no run is repeated without asking you again.` |
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
| RR-A | The header and sections 1 to 8 |
| RR-B | Sections 9 to 22 |
| RR-X | The whole text, read across sections |

The passes RR-C, RR-D and RR-E of the brief's table were not run. Their scopes (Section 23; Section 24 up to the end of 24.5; Sections 24.6 to 24.10 and section 25) were read only by the cross-check pass RR-X.

## Reports

Each report is quoted whole, line by line: a quote mark and a space are added at the start of each line, and an empty line becomes a quote mark alone. The only change made to a report is mechanical: line endings are converted to LF and each tab to four spaces.

### RR-A — The header and sections 1 to 8

> REPORT BEGIN RR-A
> IDENTITY: Devin, Cognition, model SWE-2 Medium; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 6c0e86dd39e74242566755db6702972d893a83cc4827d9fc7e4805f89db85d91
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RR-A, from the header of SPEC.md up to but not including the heading of section 9
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5
> FINDINGS: 3
> FINDING RR-A-001
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case."
> SUMMARY: The reserved-name check rejects only exact reserved names, not the reserved base-name-plus-extension forms that the same file systems also reserve.
> REASONING: The identifier rules exist so that a change identifier can safely name the directory specs/<change-id>/ on common file systems, which is why the Windows device names are listed and why case folding and a trailing dot are handled. On Windows a name such as nul.txt or com1.yaml is just as reserved as nul or com1, because the reservation applies to the base name before any extension. The identifier nul.txt satisfies the stated pattern, does not end with a dot, is not literally equal to nul, and is not equal to any other listed name after folding, so a conforming implementation accepts it and then cannot create the directory, or behaves platform-dependently. The acceptance example AE-288 does not cover this form, so the gap is not disambiguated elsewhere. An implementer acting on the text would accept identifiers the rule exists to exclude.
> DISPOSITION REQUIRED: Fix or clarify: either forbid a reserved base name before any extension dot, or state explicitly that extension forms are permitted and why.
> FINDING RR-A-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 4.3; lines 307-307; quote "enforced mechanically only for a change that has a state document"
> SUMMARY: The history-based protections of Sections 24.1 to 24.5, 24.7 and 24.8 are mechanically enforced only when a state document exists, which is optional for a `full` change.
> REASONING: The preceding sentence makes state.json mandatory only when the project uses persistent machine-readable workflow state, and otherwise permits the same information inline. The cited sentence then limits mechanical enforcement of frozen gate definitions, the not-evaluable handling, assurance and approval records, history consistency, scope checking, failure handling and open questions to changes that have a state document. A `full` change that records state inline therefore falls outside the only enforcement path the text describes, and a participant could satisfy the letter of the layout rule while escaping the mechanical checks that give the protections their teeth. The norms of Section 24 still apply in principle, but the text does not say how they are to be enforced, or verified from outside, for a change without a state document. An implementer could plausibly read this as making those checks optional. The risk is softened but not removed by the fact that `full` is not yet implemented.
> DISPOSITION REQUIRED: Clarify whether the Section 24 rules remain binding and how they are enforced or verified when no state document exists, or require a state document wherever those protections apply.
> FINDING RR-A-003
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 8.3; lines 887-887; quote "Rejection Behavior"
> SUMMARY: The transition table column named Rejection Behavior also describes blocked results, waits and closures, so its heading does not match its content.
> REASONING: The last column of the transition table is headed Rejection Behavior, yet for `complete` and `resume` it describes recording the evaluation and answering `blocked`, for `wait` it describes closing the change as failed with the answer `success`, and for `complete` it describes a soft fail or a not-evaluable gate putting the change in a wait. A second table then distinguishes `rejected` from `blocked` answers precisely, so the normative outcome is recoverable, but the column heading itself is misleading and could cause a reader to treat a recorded blocked evaluation as a rejection that writes nothing. This is a wording defect that does not change conforming behavior once the second table is read.
> DISPOSITION REQUIRED: Fix: retitle the column, for example to outcome and rejection behavior, or split the non-rejection outcomes into their own column.
> CHECKS PERFORMED:
> C1: I read the whole range and cross-checked the transition table, the rejected-versus-blocked table, section 8.4, section 8.5 and section 5.3 for statements that cannot hold together; found no contradiction, only the column-label mismatch reported as RR-A-003.
> C2: I traced the decisions that land in this range: O-1 two profiles in section 5.6, O-4 JSON state in 4.3 and 8.1, O-6 reopen kept for `full` only in 8.3 and 8.4, O-8 `full` marked specified but not implemented in 5.6, O-9 shared protections referenced in 3.7, 4.2 and 5.3, O-10 four implemented layers in 5.3; all as decided and none contradicted in this range.
> C3: I checked the requirements reachable in this range: SPEC-12 profile applicability and movement in 5.6, SPEC-14 marking and per-rule acceptance examples in sections 4 to 8, SPEC-15 state.json in 4.3 and 8.1, SPEC-16 six layers and core implementing four in 5.3, SPEC-17 reopen per profile in 8.3; all satisfied here; the identifiers SPEC-01, SPEC-02, SPEC-03 and SPEC-05 are referenced forward to sections 22 and 24 outside this range.
> C4: I looked for untestable rules and bypass paths; the identifier rules are concrete and testable except for the reserved-extension gap in RR-A-001, and the conditional mechanical enforcement of the history rules is reported as RR-A-002; failure and rejection behavior is otherwise specified per action.
> C5: I compared each acceptance example in the range (AE-01 to AE-08, AE-121 to AE-124, AE-217, AE-218 to AE-228, AE-229 to AE-248, AE-288, AE-290 to AE-298) with its stated rule; all follow from and cover the case they name; AE-288 does not cover the extension form noted in RR-A-001.
> C6: I checked the range for development artifacts, prototype identifiers, decision or requirement identifiers, foreign tool names and local paths; only method artifacts such as AE examples and project files like .ggsad/config.yaml appear; nothing improper found.
> C7: I compared every changed paragraph with BASE.md; the changes are additions and tightenings, for example silently weaken became weaken and new mandatory checks were added; no protection, MUST, SHOULD or prohibition of BASE.md was removed or relaxed in this range.
> C8: I verified the in-range cross-references: sections 16.1, 16.4, 16.5, 22.1, 22.2, 23.1 to 23.7, 24.1 to 24.9 and 25.1 exist with the expected subjects, and terms such as method profile, compliance profile and the gate result names are defined before or at first use.
> LIMITS: Sections 9 to 25 were consulted only to resolve references, not reviewed; sections 24.x and 25.x cited for enforcement details were not evaluated themselves. Tools used: Read, Grep, and single allowed commands ls, wc, diff and sha256sum. No file outside the working directory was opened.
> VERDICT: NO BLOCKING FINDINGS
> REPORT END RR-A

### RR-B — Sections 9 to 22

> REPORT BEGIN RR-B
> IDENTITY: Devin, an interactive command line agent by Cognition, powered by the SWE-2 Medium model; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 6c0e86dd39e74242566755db6702972d893a83cc4827d9fc7e4805f89db85d91
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RR-B, sections 9 to 22 of SPEC.md, from the heading "## 9. Definition of Ready" up to but not including "## 23. The `core` Profile"
> COVERAGE: 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4
> FINDINGS: 3
> FINDING RR-B-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 22.4; lines 2291-2291; quote "it has an anchor"
> SUMMARY: The guard action requires a history anchor where Section 24.4 and SPEC-05 permit an anchor or an equivalent mechanism, so a conforming change fails the guard.
> REASONING: Verification 1 of `guard` requires that a history "has an anchor" where the configuration requires A2 approvals, and failure yields the issue code `anchor-missing`. Section 24.4 states that such a history MUST have "an anchor or an equivalent mechanism", and requirement SPEC-05 likewise requires "an external anchor, or an equivalent". A change that correctly uses an equivalent mechanism is conforming yet is rejected by `guard`, so the two normative statements cannot both hold for every conforming change.
> DISPOSITION REQUIRED: Fix, for example by wording verification 1 to require an anchor or an equivalent mechanism, or an owner decision that `guard` enforces anchors only.
> FINDING RR-B-002
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 22.1; lines 2197-2197; quote "as the read-only actions `check`, `review`, and `guard` (Section 22.4) do"
> SUMMARY: The contract mandates reporting on a change via `check`, `review`, and `guard`, but `check` and `review` are defined only for the `core` profile, leaving `full` without them.
> REASONING: Section 22.1 lists reporting on a change among the operations an automation contract MUST support, realised by the read-only actions `check`, `review`, and `guard`. Section 22.4 defines `guard` for both method profiles, but `check` and `review` are defined only in Section 23.4 inside the `core` profile, and Section 8.3 defines no report actions for `full`. Whether and how a `full` change is reported on beyond `guard` is therefore undetermined, and an implementer could plausibly diverge.
> DISPOSITION REQUIRED: Clarify whether `check` and `review` apply to `full` changes (and define them there), or scope the contract operation to `core` and state that `guard` alone reports on `full` changes.
> FINDING RR-B-003
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 11.2; lines 1442-1442; quote "it holds a phase identifier of Section 7"
> SUMMARY: A resume phase is not part of the mandatory wait content, yet `resume` requires a recorded or explicitly required resume phase, so a wait recorded without one may be unresumable.
> REASONING: Section 11.2 lists six mandatory fields for a wait state and describes `resume_at` only as the field naming the resume phase; nothing states that a wait state MUST record one. Section 8.3 makes `resume` legal only when "the recorded or explicitly required resume phase is non-closed" and moves the change to that phase. For a wait recorded with the six mandatory fields but no `resume_at`, in a project that does not explicitly require one, no rule states a default resume phase, so whether the change can ever resume, and to which phase, cannot be determined from the text.
> DISPOSITION REQUIRED: Fix by stating a default resume phase (for example the phase in which the change waited) or by making the resume phase mandatory wait content; alternatively an owner decision.
> CHECKS PERFORMED:
> C1: Read all of sections 9 to 22 and cross-checked statements against sections 5.6, 7, 8.3, 23.4, 23.6, 23.7, 24.2, 24.4, 24.8 and 25.1; found the guard-versus-equivalent-anchor conflict (RR-B-001) and the undefined resume-phase outcome (RR-B-003); no other statements that cannot hold together were found.
> C2: Traced the decisions that touch this range: O-1 and O-8 are honoured by the profile markings in sections 9, 10, 19 and 21; O-5 is implemented by the four-result envelope and per-action rejected/blocked tables in 22.2 and 8.3; O-6 is preserved (`reopen` stays `full`-only); O-7 by the `migrate` operation in 22.1; O-9 by the pointers from 9.x, 10.x, 11, 12, 15, 16, 19 and 20 to the shared protections; O-11 by the verify-only `guard` of 22.4; no decision is contradicted except through RR-B-001, which limits an O-11/SPEC-05 mechanism.
> C3: Verified requirements visible in this range: SPEC-03 is satisfied by 22.2; SPEC-08 by 12.1 and the 24.7 pointers; SPEC-09 by 9.4, 9.5, 10.4, 20 and the 24.8 references; SPEC-10 by 10.7, 15 and 16.1; SPEC-14's acceptance-example coverage is largely met in this range (AE-260 to AE-270, AE-111 to AE-116, AE-287, AE-303 to AE-305); SPEC-16 is preserved in 17; SPEC-18 by 22.1 and 22.2; no requirement is contradicted within this range.
> C4: Checked that rules in range are testable and not trivially bypassable: `guard` runs no commands and proves the record only; the `blocked` envelope records evaluations so attempts stay countable; `full` rules degrade safely when no state document exists (AE-305); failure behaviour is specified per action; found no bypass except the report-action gap noted as RR-B-002.
> C5: Verified each named example in range against its rule: AE-260 to AE-270, AE-111 to AE-116 and AE-287, AE-303 to AE-305 all follow from the rules they cite; no example contradicts its rule or names another case.
> C6: Searched the range for development artifacts, prototype identifiers, decision or requirement ids, tool names that are not part of the method, and local paths; only the pre-existing illustrative product names of 14.2 and the pre-existing method and tool examples of 17 appear, both marked non-normative and unchanged from BASE.
> C7: Diffed sections 9 to 22 against BASE.md: the stricter treatment of open questions, the reclassification of retry limits as soft failures, the added allowed-path, evidence-command and severity fields, and the added completion conditions are stated additions or tightenings, not silent removals; no BASE protection was found removed, relaxed or made conditional without saying so.
> C8: Checked cross-references used in range (5.4, 5.6, 7, 8, 8.3, 10.7, 11, 16.1, 22.1, 22.4, 23.2, 23.4, 23.6, 23.7, 24.1 to 24.10, 25.1, 25.3); all resolve and match their targets; the `resume_at` value `plan` is a legal phase identifier of Section 7; no wrong section or example number found in range.
> LIMITS: Findings were judged with read-only access to the four input files only; AE identifiers cited but defined outside sections 9 to 22 were checked by searching for their definitions inside SPEC.md and were all present. Files were hashed with sha256sum and compared with the expected values, which matched. Sections consulted outside the pass range (4.3, 5.3 to 5.6, 6, 7, 8, 23, 24, 25) were read only as far as needed to judge the changed text; whether every `full` rule outside this range has an acceptance example was not exhaustively verified. No file outside the working directory was opened. Tools used: ls, grep, sha256sum, and file reading.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RR-B

### RR-X — The whole text, read across sections

> REPORT BEGIN RR-X
> IDENTITY: Devin, Cognition, model SWE-2 Medium; shared session, prompt, notes or model with Claude Code: no
> INPUT SPEC.md 6c0e86dd39e74242566755db6702972d893a83cc4827d9fc7e4805f89db85d91
> INPUT BASE.md 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3
> INPUT DECISIONS.md 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b
> INPUT REQUIREMENTS.md 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7
> SCOPE: RR-X, the whole text read across sections, from header to end
> COVERAGE: 1, 1.1, 2, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 4, 4.1, 4.2, 4.3, 5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6, 6.1, 6.2, 6.3, 7, 7.1, 8, 8.1, 8.2, 8.3, 8.4, 8.5, 9, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 10, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 11, 11.1, 11.2, 11.3, 12, 12.1, 12.2, 13, 13.1, 13.2, 13.3, 14, 14.1, 14.2, 14.3, 14.4, 14.5, 15, 16, 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17, 18, 19, 19.1, 20, 21, 22, 22.1, 22.2, 22.3, 22.4, 23, 23.1, 23.2, 23.3, 23.4, 23.5, 23.6, 23.7, 24, 24.1, 24.2, 24.3, 24.4, 24.5, 24.6, 24.7, 24.8, 24.9, 24.10, 25, 25.1, 25.2, 25.3
> FINDINGS: 6
> FINDING RR-X-001
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 24.5; lines 3776-3776; quote "A file that version control is told to ignore is invisible to the measurement."
> REFERENCE: file SPEC; section 24.5; lines 3768-3768; quote "the files that version control does not track and has not been told to ignore"
> SUMMARY: The scope check is bypassable: ignore rules can be changed in places the measurement never sees, hiding arbitrary out-of-scope work.
> REASONING: The measurement counts paths whose content differs from the base revision and untracked files not told to be ignored. A change that alters ignore configuration in a location outside the measured tree (for example the exclude file inside the version-control metadata directory, or a user-level excludes file) can turn any path into an ignored path without producing any changed path that the measurement would count. Subsequent work under those paths then leaves no scope violation. The specification acknowledges that ignored locations are invisible (Section 24.5 and the trust note in Section 24.10) but addresses only code that gate commands run; it nowhere protects the ignore configuration itself or requires it to be within the measured paths. The hard-failure protection of Section 24.5, which SPEC-06 requires, can therefore be satisfied in letter while defeated in purpose.
> DISPOSITION REQUIRED: Fix or owner decision. The scope rule needs to state which ignore sources count and how alterations of ignore configuration are detected or excluded, or explicitly accept the bypass as a documented limit.
> FINDING RR-X-002
> SEVERITY: BLOCKING
> REFERENCE: file SPEC; section 8.3; lines 893-893; quote "A DoF condition is active."
> REFERENCE: file SPEC; section 24.7; lines 3981-3981; quote "The `fail` action is valid only while a soft failure awaits disposition."
> SUMMARY: In `full`, the `fail` row of Section 8.3 makes `fail` legal whenever any DoF condition is active, while Section 24.7 makes it valid only for a soft failure awaiting disposition.
> REASONING: For a `full` change with an active fail condition of severity `hard` and no soft failure awaiting disposition, Section 8.3 admits `fail` from any non-closed phase/status and the evaluation then closes the change as failed and answers `success`. Section 24.7 states the action is valid only while a soft failure awaits disposition, which reads as requiring rejection. The two normative statements give different results for the same request, so the outcome cannot be determined from the text. In `core` no conflict arises because the `fail` row of Section 23.4 already restricts the action to a wait record of kind `fail-gate`.
> DISPOSITION REQUIRED: Fix: align the `fail` precondition of Section 8.3 with Section 24.7, or state explicitly that a `fail` request under an active hard DoF is admitted and closes the change.
> FINDING RR-X-003
> SEVERITY: MAJOR
> REFERENCE: file SPEC; section 11.2; lines 1421-1421; quote "outstanding information or decision"
> REFERENCE: file SPEC; section 5.6; lines 578-578; quote "the safe current state and the next action of a wait state in 11.2"
> REFERENCE: file SPEC; section 23.5; lines 2911-2911; quote "A `core` wait record has no safe current state and no next action."
> SUMMARY: Section 11.2 requires every wait state to name the outstanding information or decision, but the `core` wait record of Section 23.5 has no such item and AE-50 validates a record without it.
> REASONING: The applicability table of Section 5.6 applies Section 11.2 to both method profiles and carves out only the safe current state and the next action for `core`. The item `outstanding information or decision` therefore remains mandatory for a `core` wait state, yet the field list of Section 23.5 (kind, reason, owner, resume_when, expires, question) contains nothing that carries it, and example AE-50 accepts a wait record consisting of reason, owner, and resume condition alone. An implementer cannot tell whether a `core` wait record must carry the outstanding information or whether `reason` and `question` are meant to cover it.
> DISPOSITION REQUIRED: Clarify: either exempt the item in Section 5.6 or Section 23.5, or state which field of the `core` wait record carries the outstanding information or decision.
> FINDING RR-X-004
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 24.3; lines 3494-3494; quote "The signers file is kept outside the repository of the project, so that a participant who can change the repository cannot add a key for itself."
> SUMMARY: The placement of the A2 signers file outside the repository is stated declaratively, not as a normative requirement.
> REASONING: Section 24.3 marks the levels and the statement as normative but leaves verifiers optional. The sentence about the signers file is worded as a fact of the level definition rather than a MUST or SHOULD, so an implementation that keeps the signers file inside the repository violates no normative rule while losing the stated guarantee. This is a wording gap rather than a contradiction, since the paragraph can also be read as defining what counts as an A2 signers file.
> DISPOSITION REQUIRED: Clarify whether the location is part of the A2 definition or a normative requirement on the project.
> FINDING RR-X-005
> SEVERITY: MINOR
> REFERENCE: file SPEC; section 23.4; lines 2537-2537; quote "and `replaced_by` names a different change that exists"
> SUMMARY: The `core` `supersede` action accepts `replaced_by` naming any existing different change, including one that is already `closed`.
> REASONING: In `full`, supersession requires a later change authorized to replace this change's goal. In `core`, the precondition requires only existence and difference, so a change can be recorded as replaced by a change that has already ended, leaving no live successor. Nothing else breaks, because `replaced_by` is only a recorded reference, but the intent of a replacement is not expressed.
> DISPOSITION REQUIRED: Clarify whether `replaced_by` must name a change that is not `closed`, or confirm that a closed replacement is intended.
> FINDING RR-X-006
> SEVERITY: MINOR
> REFERENCE: file BASE; section 8.3; lines 514-514; quote "wait when the new corrective scope's DoW determines a pause"
> REFERENCE: file SPEC; section 8.3; lines 909-909; quote "a Definition of Wait condition of the new corrective scope is active"
> SUMMARY: The `full` `reopen` action no longer waits when the corrective scope's DoW is active; it is rejected instead, a contract change the text does not flag.
> REASONING: BASE.md allowed `reopen` to pause under an active DoW of the new corrective scope. SPEC.md lists that case under the rejected results (and AE-296 confirms rejection). The new text is internally consistent and arguably stricter, but the change of observable behavior is not announced in the Revision line or elsewhere. A participant built on the earlier text would observe a different result for the same request.
> DISPOSITION REQUIRED: Clarify or owner confirm: state whether the removal of the wait outcome of `reopen` is intended.
> CHECKS PERFORMED:
> C1: Read the whole text and compared interacting rules across sections (evaluation order in 8.5, 23.6 and 24.2; blocked and rejected tables in 8.3 and 23.4 against 22.2; wait-state content in 11.2 against 23.5; fail validity in 8.3 against 24.7). Found the contradiction of finding RR-X-002 and the underdetermination of finding RR-X-003; the remaining cross-section rules were consistent.
> C2: Traced each decision O-1 to O-11 to its implementing text: profiles and marked full in 5.6, six-layer resolution with four core layers in 5.3, normative levels and statement with optional verifiers in 24.3, JSON state in 4.3 and 25.1, fourth result and per-action tables in 22.2, 8.3 and 23.4, reopen per profile in 8.3 and 23.4, schema versions and explicit migration in 25.3, invariants of both profiles in 24, and the verify-only guard in 22.4. No decision contradicted; none missing.
> C3: Traced SPEC-01 to SPEC-18 to normative text: frozen gates in 24.1, three-valued results in 24.2, blocked result in 22.2, assurance levels and the agent-with-credentials statement in 24.3, consistency versus completeness and the anchor in 24.4, scope and isolation in 24.5, baselines in 24.6, hard and soft failure in 24.7, open questions in 24.8, executable evidence in 24.9, the opt-in interpreter and the ignored-location note in 24.10, profiles and their applicability and moving by supersede in 5.6, revised marked full with acceptance examples, JSON state with canonical form in 25.1, layered resolution in 5.3, reopen per profile, and schema versions in 25.3. SPEC-13 concerns the drafting process and is not verifiable from the text. Found one gap in the scope protection, reported as finding RR-X-001.
> C4: Looked for untestable rules and letter-versus-purpose bypasses. Found the ignore-configuration bypass of the scope check (finding RR-X-001) and the non-normative wording of the signers-file location (finding RR-X-004). The self-declared human prefix at A0 is an explicitly stated limit of Section 24.3, as SPEC-04 requires.
> C5: Checked each acceptance example against its rule, including the full-profile examples AE-249 to AE-305 and the edge examples AE-277, AE-280, AE-288 to AE-305. All examined examples follow from their rules; none names a case it does not cover.
> C6: Searched the text for development artifacts, prototype identifiers, decision and requirement identifiers, tool names that are not part of the method, and local paths. Found none; vendor and product names in Section 14.2 and tool names in Section 17 are marked as illustrative examples and were already present in BASE.md.
> C7: Compared BASE.md and SPEC.md for removed or relaxed protections. BASE protections were kept or strengthened (for example the lower-layer rule of 5.3 lost only the word silently and became stricter). The retry-limit category moved from hard to soft by design of the new fail model. One behavioral change without announcement is reported as finding RR-X-006.
> C8: Checked cross-references and section numbers cited in changed text (Sections 4.3, 5.3, 5.6, 8.3, 11.1, 11.2, 12.2, 16.1, 16.4, 16.5, 22.2, 22.4, 23.1 to 23.7, 24.1 to 24.10, 25.1 to 25.3) and term usage; all resolve to existing headings and terms are defined before or at use.
> LIMITS: The whole pass used only the Read, Grep, Glob and file-writing tools plus the permitted commands sha256sum and wc; no file outside the working directory was opened. The literal hash value stated in example AE-183 could not be recomputed, because the permitted commands give no way to hash a string without creating a file or using a pipe; the empty-object hash of AE-184 matches the well-known SHA-256 of that text. SPEC-13 (no file under the implementation tree modified during drafting) cannot be verified from the reviewed text and is reported as such. Examples whose quoted identifiers were checked were verified by search.
> VERDICT: BLOCKING FINDINGS PRESENT
> REPORT END RR-X

## Findings

| Finding | Severity | Reference | Summary | Disposition |
|---|---|---|---|---|
| RR-A-001 | MAJOR | file SPEC; section 4.3; lines 303-303; quote "It MUST NOT be `con`, `prn`, `aux`, `nul`, `com1` to `com9`, or `lpt1` to `lpt9`, compared after the ASCII upper case letters are folded to lower case." | The reserved-name check rejects only exact reserved names, not the reserved base-name-plus-extension forms that the same file systems also reserve. |  |
| RR-A-002 | MAJOR | file SPEC; section 4.3; lines 307-307; quote "enforced mechanically only for a change that has a state document" | The history-based protections of Sections 24.1 to 24.5, 24.7 and 24.8 are mechanically enforced only when a state document exists, which is optional for a `full` change. |  |
| RR-A-003 | MINOR | file SPEC; section 8.3; lines 887-887; quote "Rejection Behavior" | The transition table column named Rejection Behavior also describes blocked results, waits and closures, so its heading does not match its content. |  |
| RR-B-001 | BLOCKING | file SPEC; section 22.4; lines 2291-2291; quote "it has an anchor" | The guard action requires a history anchor where Section 24.4 and SPEC-05 permit an anchor or an equivalent mechanism, so a conforming change fails the guard. | fix |
| RR-B-002 | MAJOR | file SPEC; section 22.1; lines 2197-2197; quote "as the read-only actions `check`, `review`, and `guard` (Section 22.4) do" | The contract mandates reporting on a change via `check`, `review`, and `guard`, but `check` and `review` are defined only for the `core` profile, leaving `full` without them. |  |
| RR-B-003 | MAJOR | file SPEC; section 11.2; lines 1442-1442; quote "it holds a phase identifier of Section 7" | A resume phase is not part of the mandatory wait content, yet `resume` requires a recorded or explicitly required resume phase, so a wait recorded without one may be unresumable. |  |
| RR-X-001 | BLOCKING | file SPEC; section 24.5; lines 3776-3776; quote "A file that version control is told to ignore is invisible to the measurement." | The scope check is bypassable: ignore rules can be changed in places the measurement never sees, hiding arbitrary out-of-scope work. | fix |
| RR-X-002 | BLOCKING | file SPEC; section 8.3; lines 893-893; quote "A DoF condition is active." | In `full`, the `fail` row of Section 8.3 makes `fail` legal whenever any DoF condition is active, while Section 24.7 makes it valid only for a soft failure awaiting disposition. | fix |
| RR-X-003 | MAJOR | file SPEC; section 11.2; lines 1421-1421; quote "outstanding information or decision" | Section 11.2 requires every wait state to name the outstanding information or decision, but the `core` wait record of Section 23.5 has no such item and AE-50 validates a record without it. |  |
| RR-X-004 | MINOR | file SPEC; section 24.3; lines 3494-3494; quote "The signers file is kept outside the repository of the project, so that a participant who can change the repository cannot add a key for itself." | The placement of the A2 signers file outside the repository is stated declaratively, not as a normative requirement. |  |
| RR-X-005 | MINOR | file SPEC; section 23.4; lines 2537-2537; quote "and `replaced_by` names a different change that exists" | The `core` `supersede` action accepts `replaced_by` naming any existing different change, including one that is already `closed`. |  |
| RR-X-006 | MINOR | file BASE; section 8.3; lines 514-514; quote "wait when the new corrective scope's DoW determines a pause" | The `full` `reopen` action no longer waits when the corrective scope's DoW is active; it is rejected instead, a contract change the text does not flag. |  |


## Requestor notes

- The Requestor checked the format of each report and whether each reference resolves in the pinned text; it did not assess whether any finding is correct.
- Independence rests on the reviewer's different product, vendor and model, on separate sessions that share no context with the Requestor, and on the reviewer's own statement of identity in each report; the repository cannot show more.
- A finding's severity is the reviewer's; only the repository owner dispositions a finding.

This note is evidence only. It does not change the reviewed file.
