# Independent review brief: core-only restructure of the normative specification

## Your role

You are the independent Reviewer. The Requestor is Claude Code (Anthropic). State in your report which product, vendor and model you are, and whether you share a session, prompt, notes or model with Claude Code.

This is the review round of a bounded Pair Review cycle (Section 14.3 of the specification): one review round and at most one re-check. Report every finding now. The re-check will cover only the findings the repository owner marks `fix`. Do not edit any file of the repository except your report.

## What is under review

- Base: commit `bd51cfd` (`git show bd51cfd:docs/method/GG-SAD_normative_method_specification.md`, version 1.4, 4,951 lines).
- Reviewed: commit `ef811ad`, files in `docs/method/`:
  - `GG-SAD_normative_method_specification.md` (version 2.0 draft, `core` only, 1,483 lines)
  - `GG-SAD_implementation_contract.md` (former Sections 22 and 25)
  - `GG-SAD_signing_extension.md` (assurance levels A1 and A2)
  - `GG-SAD_full_profile_deferred.md` (the `full` profile; not normative, verbatim from 1.4 apart from a header)
- Also changed: `AGENTS.md`, `CLAUDE.md` (GSD no longer required).

Use `git diff bd51cfd ef811ad -- docs/method AGENTS.md CLAUDE.md` and read the files at `ef811ad`. Do not read `.planning/`, `archive/`, or `specs/`.

## Decisions of the repository owner (the standard to judge against)

- D1. Remove the `full` method profile from the normative text. Keep it, unchanged in substance, in the deferred document.
- D2. Bound Pair Review: one review round, at most one re-check, the owner dispositions each finding as fix, defer or reject; the owner may overrule by explicit instruction (Section 14.3).
- D3. Split the specification: implementation contract (old Sections 22 and 25), signing extension (A1 and A2 of old Section 24.3), deferred `full`. The main text keeps a short Section 24.3 (A0, fail-closed, human-only actions). Section numbers stay stable.
- D4. Reduce the acceptance examples and renumber them in order. The result is not strictly one per rule; this is known and accepted.
- D5. The main specification is about 1,500 lines.
- D6. Development is by plain commits; GSD is no longer required (`AGENTS.md`, `CLAUDE.md`).

## Intended removals (do not report these as weakening)

The `full` profile and its rules; the `full` form of `spec.md`, `plan.md`, `tasks.md`, `evidence.md`; size classes, phases, Definition of Ready; the project-wide-definition exception (full only); resolution layer 4 (change class), so five layers instead of six; the `WAIT_*` categories (the wait kinds of Section 23.5 replace them); the templates of `project-brief.md`, `architecture.md`, `roadmap.md` (pointers to `.ggsad/templates/` replace them); about 260 acceptance examples (D4).

## What to evaluate

Judge the difference, reading unchanged text only as far as needed.

- C1 Contradiction and ambiguity: statements that cannot hold together; a term used in two senses; a rule whose outcome cannot be determined.
- C2 Orphaned `full` content: wording in the five normative-text files that still assumes phases, size classes, Definition of Ready, `full` change specifications, inline records, or a six-layer resolution.
- C3 Weakening: a protection, MUST/SHOULD rule or prohibition of 1.4 that applies to `core` and is removed, relaxed or made conditional without being listed under intended removals. Pay special attention to Section 24 and the new Section 24.3.
- C4 References: wrong or dangling section numbers, example numbers (`AE-nnn`), or cross-document references; a reference to a moved section that does not name the document.
- C5 Examples: an example that does not follow from its rule, or covers another case than its title names; a rule whose section now has no example at all and is hard to test.
- C6 Testability and bypass: rules that cannot be tested from outside, or that a hostile participant could satisfy in letter while defeating their purpose, especially in the bounded review rule and the split of Section 24.3.
- C7 Consistency of the split: statements that appear in two documents, or documents that disagree (main text, implementation contract, signing extension).
- C8 Self-containment: references to development artifacts, tool names that are not part of the method (examples of agents in Section 14.2 are allowed), or local paths.

## Severity

- BLOCKING: must be fixed or dispositioned by the owner before the text is final (contradiction, bypassable or weakened protection, wrong normative reference).
- MAJOR: an implementer could plausibly act on it incorrectly.
- MINOR: wording, structure or reference defect that cannot change what a conforming participant does.
- INFO: observation, not a defect.

## Output

Write one file, `docs/reviews/2026-10-31-core-only-review-report.md`, and nothing else. Layout:

```
REPORT BEGIN
IDENTITY: <product, vendor, model; shared session/prompt/notes/model with Claude Code: yes or no>
COMMIT: <output of git rev-parse HEAD>
FINDINGS: <none, or the number>
FINDING R-001
SEVERITY: <BLOCKING|MAJOR|MINOR|INFO>
REFERENCE: <file and section or line, one to four lines>
SUMMARY: <one line, at most 200 characters>
DETAIL: <the defect, and the smallest change that would resolve it>
...
CHECKS: <one line each for C1 to C8: what you did and found>
LIMITS: <what you did not verify; tools used; files opened outside the listed ones>
VERDICT: <NO BLOCKING FINDINGS | BLOCKING FINDINGS PRESENT>
REPORT END
```

Number findings R-001, R-002, ... in order of severity, most severe first. Report each defect once. Do not report style preferences or the known limits listed above.
