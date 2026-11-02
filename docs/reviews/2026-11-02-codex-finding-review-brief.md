# Independent review brief: fix of the Codex finding on "cannot start" gates

## Your role

You are the independent Reviewer. The Requestor is Claude Code (Anthropic). State in your report which product, vendor and model you are, and whether you share a session, prompt, notes or model with Claude Code.

This is a new, narrow Pair Review cycle that the repository owner approved explicitly (Section 14.3): one review round and at most one re-check. Report every finding now. Do not edit any file of the repository except your report.

## What is under review

- A finding of the automated GitHub reviewer Codex on pull request 11, on `docs/method/GG-SAD_normative_method_specification.md` Section 24.2: the rule "a command that cannot start is `not_satisfied`" also applies to fail gates and wait gates, which are active when their result is `satisfied`. A fail gate whose program is missing would then be inactive, and the change could start or close without the condition having been checked.
- The fix: Section 24.2 now says that a done gate and an evidence command whose command cannot start (for a reason other than a missing approved program) are `not_satisfied`, and that a fail gate or a wait gate whose command cannot start is `not_evaluable`, so the change waits. The example AE-327 was added.
- Changed text: the one hunk in Section 24.2 of the specification, in the working tree at the commit named in your session instruction (the diff is in the file named there). The base is commit `61b1f95`'s equivalent on this branch.

Do not read `.planning/`, `archive/`, or `specs/`.

## Owner decisions (do not report them as defects)

- A check that cannot run because an approved tool is missing is a wait; a check that cannot run for another reason is a failure (UR-08). The default for a project with no list `required_tools` is that no program is approved (review finding R-003 of the earlier cycle).
- The fix keeps these decisions for done gates and evidence commands.

## What to evaluate

- C1 Is the finding real, and does the fix resolve it without a new gap? Check every kind of gate: fail, wait, done `check`, done `sign-off`, evidence commands, retry-limit gates, the built-in predicate gates.
- C2 Contradictions inside Section 24.2 and with Sections 23.3, 23.6, 24.6, 24.9, 24.10: in particular the sentence that a `not_evaluable` result MUST NOT be recorded as `not_satisfied`, the retry-limit count (only `not_satisfied` results count), and the order of evaluation by group.
- C3 Does the fix weaken a protection, or can a hostile participant still defeat a fail or wait gate by making its program fail to start in a way that the text classifies as `not_satisfied`?
- C4 References and the new example AE-327: does it follow from the rule?
- C5 A retry limit counts `not_satisfied` results: does a done gate whose program cannot start now consume attempts? Is that intended by the owner decision above, and is it stated clearly?

## Severity

BLOCKING, MAJOR, MINOR, INFO as in the earlier briefs.

## Output

Write one file, `docs/reviews/2026-11-02-codex-finding-review-report.md`, and nothing else. Layout:

```
REPORT BEGIN
IDENTITY: <product, vendor, model; shared session/prompt/notes/model with Claude Code: yes or no>
COMMIT: <the commit hash given in your session instruction>
FINDING VERIFIED: <yes|no|partly> - <one line>
FIX RESOLVES IT: <yes|no|partly> - <one line>
FINDINGS: <none, or the number>
FINDING R-001
SEVERITY: <BLOCKING|MAJOR|MINOR|INFO>
REFERENCE: <file and section or line>
SUMMARY: <one line, at most 200 characters>
DETAIL: <the defect, and the smallest change that would resolve it>
...
LIMITS: <what you did not verify; tools used; files opened outside the listed ones>
VERDICT: <NO BLOCKING FINDINGS | BLOCKING FINDINGS PRESENT>
REPORT END
```
