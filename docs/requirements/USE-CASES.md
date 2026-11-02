# GG-SAD — Use cases as stories

**Status:** Draft, rewritten in plain words for the owner. Not normative. Derived from the transition table (Section 23.4), the evaluation order (Section 23.6) and the protections (Section 24) of `docs/method/GG-SAD_normative_method_specification.md` (v2.0 draft). The related requirements are in `USER-REQUIREMENTS.md` (UR-xx).

**How to read each item**
- **Story:** who does what, in order. *Ada* is the owner (a human), *builder* is an AI agent, *reviewer* is a second participant.
- **What you see:** what the tool answers.
- **Missing or risky today:** gaps and things you must accept.
- **Decision:** `proposed` (not yet discussed), or `keep` / `modify` / `remove`.

Action names in `code font` are the commands of the method: `new`, `approve`, `start`, `close`, `wait`, `resume`, `ask`, `answer`, `fail`, `cancel`, `supersede`, `adopt`.

---

## UC-01 Set up a project

**Story:**
1. Ada decides how strict the project is and writes the profile (`lean`, `standard`, `governed`, `regulated`) into `.ggsad/config.yaml`.
2. She records the same profile, the method (`core`) and the working mode in `docs/project-brief.md`.
3. She creates the constitution, the architecture and the roadmap from the templates.

**What you see:** from now on, every new change must use that profile. A change with another profile is rejected.

**Missing or risky today:** the spec does not say whether there is a command that does the setup, or whether it is all by hand. It does not say which of the documents `lean` really needs.

**Spec:** 4.2, 5.1, 5.6, 16. **Needs:** UR-03, UR-19.

**Decision:** keep, with two additions: (1) an `init` command: the owner names the profile once; the tool creates the config, the brief and the template documents the profile requires (lean list per UR-19) and never overwrites existing files; (2) the tool checks that the profile in the config and in the brief match and reports a mismatch.

## UC-02 Plan a change: create, approve, start

**Story:**
1. Ada (or builder) writes `change.yaml` (goal, allowed folders, requirements with check commands, extra gates) and `spec.md`, and runs `new`.
2. The tool checks the name, the profile and the gates. A bad name such as `../x`, a missing severity, or a removed base gate is rejected, and nothing is written.
3. If there are open questions, Ada answers them first.
4. Ada runs `approve` for the spec and the gates. The tool stores fingerprints.
5. Someone runs `start`. The tool records the starting revision of the code.

**What you see:** the change is *open* after `new`, still *open* after `approve`, and *active* after `start`. `start` is refused if the gates are not approved, a fail or wait rule is already active, or the starting revision cannot be recorded.

**Missing or risky today:** the working copy must equal the starting revision, apart from the change's own files. The method does not prepare that isolation for you. It is open whether a human or an agent may run `new` (the spec allows both).

**Spec:** 23.1, 23.3, 23.4, 24.1, 24.5. **Needs:** UR-01, UR-04, UR-05, UR-12, UR-15.

**Decision:** keep, with two additions: (1) `start` refuses when the working copy is not clean, or lists the unrelated files and lets the owner name them as "known before start"; (2) agents may run `new`, but nothing runs until a human approves. Confirmed 2026-11-02: `start` simply refuses on an unclean working copy; there is no "known before start" list.

## UC-03 Do the work and finish as done

**Story:**
1. builder works inside the allowed folders.
2. builder runs `close`.
3. The tool checks, in order: hard failures; things it could not check; soft failures; wait rules; then the done gates, including the check command of every requirement.
4. Everything is in order.

**What you see:** the change is *closed* with the outcome *done*, and the results of the checks are in the history.

**Missing or risky today:** nothing says that a human must press the final `close`. An agent can close its own change when all gates pass.

**Spec:** 19, 20, 23.6, 24.9. **Needs:** UR-07, UR-17.

**Decision:** keep, with one addition: closing as `done` needs a human, unless the change was approved with "agent may close" written in its frozen definition. Closing as `failed` stays automatic.

## UC-04 The work leaves its scope and fails by itself

**Story:**
1. The allowed folders are `lib/**`.
2. builder changes `lib/net/client.py` (fine) and also `docs/guide.md` (outside).
3. builder runs `close`.

**What you see:** the tool answers *success*, but the change is *closed* with the outcome *failed*. The record names `docs/guide.md`. No human action was needed.

**Missing or risky today:** the failure is decided only when somebody runs an action, not at the moment of the edit. A file hidden by an ignore file is not seen.

**Spec:** 12, 24.5, 24.7. **Needs:** UR-09, UR-12.

**Decision:** keep, with two additions: (1) a read-only `check-scope` command that shows at any time whether the change has left its scope and changes nothing; (2) `status` and `close` show the same early warning without failing the change yet (the failure is still decided at `close`). The ignored-file gap stays accepted (UR-12).

## UC-05 A test keeps failing: soft failure and your decision

**Story:**
1. The change has a soft rule "the retry limit of `tests-pass` is 3".
2. `tests-pass` fails three times. At the next `close` the tool puts the change into *waiting* (kind `fail-gate`).
3. Ada looks at the history and chooses:
   - `fail` with a reason: the change is *closed*, outcome *failed*; or
   - an `override` approval with a reason and, say, two more tries: the change continues for exactly two more `close` attempts, and on the third it waits again.

**What you see:** the wait record says who must act and what resumes it ("a human recorded an override of ...").

**Missing or risky today:** there is no default for the number of tries. An override loses its effect if the gates are re-approved with changes.

**Spec:** 23.5, 24.2, 24.7. **Needs:** UR-09, UR-11.

**Decision:** keep, with one addition: the default number of tries from UR-09 applies; and when a re-approval would cancel an override, the tool says so before approving and shows how many tries are left.

## UC-06 Something cannot be checked

**Story:**
1. builder runs `close`. The test program is not installed.
2. The tool does not report a failure. It puts the change into *waiting* (kind `external`), names the gate and the missing program, and does not use up a retry.
3. Ada installs the program. builder runs `resume`.

**What you see:** the change is *active* again, and the earlier "cannot check" record stays in the history.

**Missing or risky today:** nobody is told that the cause is gone. There is no maximum waiting time.

**Spec:** 23.5, 23.6, 24.2. **Needs:** UR-08.

**Decision:** keep, with two additions: (1) the status report re-tests the missing program and shows "the cause may be gone, ready to resume" when it exists (nothing resumes by itself); (2) `resume` itself checks that the program exists and refuses with a clear message if it still does not. The overdue warning from UR-08 stays.

## UC-07 An agent has a question, or the work must pause

**Story:**
1. builder is unsure: "Q1: migrate old accounts? yes / no". It runs `ask`.
2. builder runs `wait` and names Q1. The change is *waiting* (kind `question`).
3. Ada runs `answer` with "yes". The question is recorded as answered.
4. builder (or Ada) runs `resume`.

**What you see:** while Q1 is open, `approve` for the spec is rejected (`open-questions`) and `close` is blocked. For a pause that is not a question (for example an outside team must act), `wait` is used with a reason, an owner and a resume condition, and the owner says when it holds.

**Missing or risky today:** the answer does not resume the change by itself. A manual wait is resumed on the owner's word alone.

**Spec:** 11, 23.4, 23.5, 24.8. **Needs:** UR-10.

**Decision:** keep, with the answer-and-resume step from UR-10, plus one addition: resuming a manual wait stays on the owner's word, but the resume must carry a one-sentence note ("what happened") that goes into the history; no note, no resume.

## UC-08 Someone edits the gates or the spec after approval

**Story A, gates:**
1. Ada approved the gates. Someone then changes a hard rule to soft in `change.yaml`.
2. Every action that would change the state is rejected with `gates-changed`. Only `cancel` and a new approval still work.
3. Ada reads the difference and approves again. The re-approval is recorded as an amendment.

**Story B, spec:**
1. The spec was approved. builder edits `spec.md`.
2. The stale-approval rule is active. `close`, `resume` and `start` are held.
3. Ada approves the spec again.

**Missing or risky today:** an override lapses when the gates are re-approved. Story B does not apply before the first approval. `supersede` is blocked in story A today (see UR-05).

**Spec:** 24.1, 23.7, 24.3. **Needs:** UR-01, UR-05.

**Decision:** keep, with two additions: (1) the approval summary shows what changed since the last approval, and shows "first approval" when there is none; (2) the amendment record keeps a short before/after of the changed gates and spec lines. `supersede` after a gate edit is already decided in UR-05; the override warning is decided in UC-05.

## UC-09 End a change early, or continue later

**Story:**
1. Ada runs `cancel`: the change is *closed* with the outcome *cancelled*. If a hard failure is active, or a soft failure waits for a decision, the outcome is *failed* instead.
2. If another change replaces this one, Ada runs `supersede` and names the replacement.
3. Later work is a new change with `follows` set to the closed change. The old change is never touched.

**What you see:** a closed change never changes again. `follows` must name a change that is already closed.

**Missing or risky today:** small fixes need a whole new change. `cancel` and `supersede` behave differently when the gates were edited (see UR-05).

**Spec:** 23.1, 23.2, 23.4, 24.7. **Needs:** UR-06, UR-11.

**Decision:** keep, with the UR-06 follow-up change and the UR-05 `supersede` fix, plus two additions: (1) `supersede` needs the replacement change to exist already, so a superseded change never points to nothing; (2) status shows the "reason for cancel" and the "follow-ups" of a closed change, so the owner can find what replaced it.

## UC-10 The history looks tampered with

**Story:**
1. Someone edits `state.json` by hand, or deletes the last entries.
2. The next action recomputes the chain (and compares it with the anchor, if there is one).
3. The tool refuses to act and says what it found: edited, truncated or rewritten.
4. For a history without an anchor that is otherwise in order, Ada runs `adopt` at the required level. The tool then keeps an anchor at the latest entry.

**What you see:** no action is accepted on a damaged history. `adopt` itself is rejected if the history is not consistent or if an anchor exists.

**Missing or risky today:** the spec says how to detect damage, not how to repair it. `adopt` cannot show whether entries were lost before it. Someone who can write both history and anchor can fool every check.

**Spec:** 23.1, 24.4. **Needs:** UR-13.

**Decision:** keep, with one addition: a `repair` path for the owner only. The tool shows exactly which entries are missing or wrong; the owner confirms in writing; the history continues with a "repaired" entry that records what was lost; the old damaged file is kept next to it. Confirmed 2026-11-02: `repair` is also allowed when an anchor exists, with the owner's written reason; the old anchor is kept in the "repaired" entry and a new anchor is set.

## UC-11 A human signs off a gate

**Story:**
1. The change has a gate `legal-ok` of the kind sign-off.
2. builder tries to approve it and is rejected (the name does not start with `human:`).
3. Ada, as `human:ada`, approves the gate. The tool records her identity, the level of the claim and the fingerprint of the gate definitions.

**What you see:** the gate is satisfied at the required level or higher, otherwise rejected. A project or a gate can demand a stronger level (A1, A2) in the Signing Extension.

**Missing or risky today:** at level A0 anyone can write `human:ada`. A later gate change makes the sign-off no longer match.

**Spec:** 23.3, 24.3, Signing Extension. **Needs:** UR-11.

**Decision:** keep, with the UR-11 additions (approved-human list, real account recorded), plus: when a gate edit makes a sign-off stale, the status report says so plainly (who signed, when, that the gate changed since), the change cannot close until the owner signs again, and the tool adds an open question for the owner asking for the new sign-off.

## UC-12 Independent review

**Story:**
1. Ada decides that a review is required and names builder as the Requestor and reviewer as the Reviewer. Scope and criteria are written down, and the work product is fixed to one revision.
2. reviewer reports all findings.
3. Ada marks each one *fix*, *defer* or *reject*, with a reason.
4. builder applies the fixes.
5. reviewer re-checks only the fixes and reports each as *verified* or *open*. No new findings about old text are accepted.
6. Ada dispositions what stays open as *accepted* or *deferred*. The cycle is over.

**What you see:** the result is kept as evidence in the history or in `review.md`. An open blocking finding blocks completion until Ada dispositions it.

**Missing or risky today:** no gate can check "the required review is complete". A sign-off gate is the workaround. A `review` gate is invalid.

**Spec:** 3.10, 14, 20. **Needs:** UR-16.

**Decision:** keep, with the `review` gate from UR-16, plus: the result is always kept in one place, `review.md` in the change folder, and the history records its fingerprint. `review.md` has a fixed layout (finding ID, severity, owner's decision, reason, verified or open) so the gate can check it.

## UC-13 An agent finds a conflict with an accepted decision

**Story:**
1. builder finds that requirement R2 ("jobs go into a queue") conflicts with an accepted ADR ("jobs live in a database table").
2. builder writes the conflict into the requirement or spec, stops work, returns R2 to Ada and asks for a decision.
3. Ada decides. The decision is recorded and referenced. If the ADR should change, that happens in its own approved change.

**What you see:** the agent does nothing further on R2 until Ada decides.

**Missing or risky today:** nothing in the tool records this as a state; today it is a rule of conduct. A question and a wait (UC-07) can be used to make it visible.

**Spec:** 13.1, 5.4, 19.1. **Needs:** UR-02, UR-17.

**Decision:** keep, with two additions: (1) a `conflict` command that opens a question for the owner, puts the change into waiting, and names the two documents that disagree (built on the same `ask` and `wait` as UC-07); (2) `close` is refused while a conflict question is open (the same block as any open question). An agent that never runs `conflict` is still only a conduct problem (UR-17).

## UC-14 Where do we stand? (status report)

**Story:**
1. Ada or builder runs `check`, `review` or `guard`.
2. The tool reports the state, the gate results and any problem. It writes nothing and records no failure.

**What you see:** if the gate definitions differ from the approved ones, the report says so and says that the gates are not enforced.

**Missing or risky today:** these report operations are defined in the Implementation Contract, not in the core text. `guard` is the natural home for the tool check asked for in UR-02.

**Spec:** 23.4, 24.1, Implementation Contract 22.4. **Needs:** UR-02, UR-17.

**Decision:** keep, with two additions: (1) one plain description of the status report moves into the core spec, with one list of everything it must show: state, gate results, warnings (overdue waits, no anchor, stale sign-off, scope warning, ready to resume, expired baseline, missing required document) and who must act; `guard` keeps the UR-02 tool check; (2) the report starts with a one-line summary for the owner: "needs you / waiting on others / all fine".

## UC-15 Accept known test failures

**Story:**
1. The test suite already has the failures `t1` and `t2`.
2. Ada adds a baseline `[t1, t2]` to the gate `tests-pass` and approves the gates.
3. At `close` the tests report `t1`, `t2` and `t9`.

**What you see:** the gate is *not satisfied* because of `t9`, and the record says there is one new failure and names `t9`. If only `t1` and `t2` fail, the gate is satisfied.

**Missing or risky today:** the gate must say how to read failure names from the output. If none can be read, the result is "cannot check". There is no expiry for baseline entries.

**Spec:** 24.6. **Needs:** UR-14.

**Decision:** keep, same as UR-14 (baseline stays; each name has a written reason and a review date; past the date the status report warns and names the owner).

## UC-16 Use GG-SAD together with another tool

**Story:**
1. A team already uses another framework for planning.
2. An integrator writes a mapping: what the tool owns, what GG-SAD owns, who is authoritative for each fact, what each side may read and write, how state is synchronised, and how to roll back.
3. The tool does planning and execution; GG-SAD keeps goals, gates, state and closure.

**What you see:** the tool cannot skip a gate or weaken the profile. On conflict, GG-SAD's document order decides.

**Missing or risky today:** specified, but not built in the reference implementation. A mapping adds no gates to a `core` change.

**Spec:** 3.8, 17. **Needs:** UR-18.

**Decision:** change: moves to "future", same as UR-18 (the tool refuses to start in combination mode; the spec and guide mark it "described, not built").
