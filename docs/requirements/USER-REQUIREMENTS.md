# GG-SAD — What the method must do for you (user requirements)

**Status:** Draft, rewritten in plain words for the owner. Not normative. The specification (`docs/method/GG-SAD_normative_method_specification.md`, v2.0 draft) has no section called "user requirements", so these were derived from its rules. If this file and the specification disagree, the specification governs until the owner decides.

**How to read each item**
- **In one sentence:** what you get.
- **Example:** a short story. *Ada* is the owner (a human). *builder* is an AI agent that does the work.
- **What the method does:** the behaviour, step by step.
- **Missing or risky today:** things that are not covered, or that you must accept.
- **Spec:** where the rule is written.
- **Decision:** `proposed` (not yet discussed), or `keep` / `modify` / `remove` with your wording.

Words used: a **change** is one piece of work with its own folder. A **gate** is a rule that must hold for the change to go on or to finish. A **spec** is the written description of what the change must achieve.

---

## UR-01 A change starts from a written goal and an approved spec

**In one sentence:** no work starts without a stated goal, and nobody can quietly change the agreed spec afterwards.

**Example:** Ada wants a login page. She writes the goal (problem, "done when", what is *not* part of the work) and the spec, and approves the spec. Later builder edits `spec.md` to add a "remember me" feature. The next attempt to finish the change is stopped: the spec no longer matches what Ada approved. Ada must read it and approve again.

**What the method does:**
1. The change definition must hold a goal, a scope, requirements and gates.
2. A human approves the spec. The tool stores a fingerprint of the approved text.
3. If the text differs from the fingerprint, the change cannot start, resume or close until a human approves again.

**Missing or risky today:** before the very first approval, edits are not caught (nothing is agreed yet). "Done when" is only text; the tool does not check it.

**Spec:** 3.1, 3.2, 23.1, 23.7, 24.3. **Replaces:** UR-001, 002, 003.

**Decision:** keep (UR-001, 002, 003 all kept). Weak spot: add a general structural check at approval: your approval is refused while any "done when" sentence is not tied to a requirement that has at least one evidence command. (The tool cannot judge whether the command really proves the sentence; you review that when you approve.)

## UR-02 Higher-ranking documents win

**In one sentence:** when two project documents disagree, the stronger one wins, and a change may not override it behind your back.

**Example:** the architecture says "jobs are stored in a database table". A new spec says "jobs go into a message queue". The order of authority (constitution, accepted decisions, project brief, architecture, change spec, code, evidence) says the architecture wins. builder must not just do it the queue way.

**What the method does:** states the order of authority and forbids silent overrides. An agent that finds a conflict must stop and ask (see UR-17).

**Missing or risky today:** nothing in the tooling checks "silently". It is a rule for people and agents only.

**Spec:** 4, 13.1, 19.1. **Replaces:** UR-004.

**Decision:** keep the rule. When a requirement is set aside because it contradicts a higher-ranking document, the owner is told openly: "your requirement was not applied, because it needs an approved change in <higher-ranked document>". Weak spot: both guards. (1) The tool keeps a fingerprint of the higher documents; if one is edited during a change, the change stops until a human approves the edit. (2) Each spec carries a line "conflicts with higher documents: none / these", confirmed by a human at approval; the tool only checks that the line exists.

## UR-03 Rigor fits the risk (compliance profiles)

**In one sentence:** you choose how strict the project is, from a light prototype setup to a regulated one, but even the lightest setup keeps the basics.

**Example:** Ada runs a prototype and picks `lean`. She may approve her own work. A bank team picks `regulated`: approvals and evidence are stricter. Both still need a goal, a spec, gates, evidence and a traceable result.

**What the method does:** four named profiles (`lean`, `standard`, `governed`, `regulated`) and custom ones. Every profile keeps the "invariant core": goal, spec, gates, evidence, controlled waiting and failing, a recorded result.

**Missing or risky today:** the specification only gives each profile "minimum characteristics". It does not yet say exactly what `standard` does differently from `lean`.

**Spec:** 3.6, 3.7, 5.1, 5.2. **Replaces:** UR-005, 006.

**Decision:** keep (restart interview, confirmed). Weak spot: keep the four names, and for each one list only what it really changes in the rules that exist today. (UR-006, the unremovable basics, is kept.)

## UR-04 Rules can get stricter, never weaker

**In one sentence:** a project setting or a single change may add rules, but never remove or soften a rule that is stronger.

**Example:** the project says "a failing security scan always stops the work". A change author tries to list that scan as "soft, just a warning". The tool rejects the change definition and names the gate and how it was weakened.

**What the method does:** rules come in layers (core protections; profiles; project settings; the change definition; tool mappings). A lower layer may add rules. If it removes, edits or softens a rule of a higher layer, the definition is rejected, and nothing is written. The check runs when the change is created and again before the gates are approved.

**Missing or risky today:** the fifth layer (tool mappings) is described but adds nothing to a `core` change and is not built.

**Spec:** 5.3, 23.7. **Replaces:** UR-007.

**Decision:** keep. Weak spot: state plainly that four layers are active; the fifth (tool mappings) moves to the "future" section until a tool plug-in really exists.

## UR-05 The rules of a change are frozen once you approve them

**In one sentence:** after you approve the gates, the scope and the evidence commands, nobody can change them without you approving again.

**Example:** Ada approves a change where "tests must pass" is a hard rule. Later someone edits the file so that the test command always reports success. Every action that would change the state is refused with `gates-changed`, until Ada looks at the new version and approves it.

**What the method does:** the tool stores a fingerprint of the gate definitions at approval and compares it before every action. `cancel` still works so that a damaged change can always be ended. The re-approval is recorded as an amendment.

**Missing or risky today:** `supersede` (end a change and name its replacement) is currently blocked by such an edit, while `cancel` is not. You asked to fix this.

**Spec:** 3.3, 24.1. **Replaces:** UR-008.

**Decision:** keep, with one addition: named and approved deputies (GitHub users; fallback = the repository owner) may give the re-approval too, not only the owner. Weak spot: `supersede` works after a gate edit exactly like `cancel` (human only, reason recorded). Open point for UR-11: how a deputy list is kept and protected.

## UR-06 A change has a simple life, and a finished change stays finished

**In one sentence:** a change is *open*, *active*, *waiting* or *closed*, and a closed change ends as *done*, *failed* or *cancelled*, for good.

**Example:** Ada cancels a change. A week later she wants it back. She cannot reopen it. She creates a new change that says "follows" the old one. The old one stays as it was.

**What the method does:** fixed states, fixed actions, a table that says which action is legal from which state. Anything else is rejected.

**Missing or risky today:** even a tiny fix after closing needs a whole new change.

**Spec:** 21, 23.2, 23.4. **Replaces:** UR-009.

**Decision:** keep. Weak spot: add a light "follow-up" change that starts pre-filled from the closed one (same goal and scope).

## UR-07 "Done" needs a check that runs and passes

**In one sentence:** a change finishes as *done* only if every requirement has a command that was run and passed.

**Example:** the change says "users can reset a password" (R1). It has the command `run-tests --suite reset`. When builder asks to close, the tool runs the command. If it passes, the change can close. If R1 has no command at all, the change cannot close, and the report names R1. A screenshot or "I tested it" does not count.

**What the method does:** each requirement lists at least one evidence command with a table of exit codes. Closing runs them. A missing command, a failing command or a command that cannot run all keep the change from closing.

**Missing or risky today:** a documentation-only change still needs some command (for example a link check). Whether a human sign-off may replace a command is not allowed today.

**Spec:** 3.4, 15, 20, 24.9. **Replaces:** UR-010.

**Decision:** keep. Weak spot: (a) a requirement marked "cannot be machine-checked" may be closed by a human sign-off with a written reason; the record shows it as human-checked. (b) Ready-made standard checks exist for document changes (links, formatting); they support the human in verifying a documentation change before signing off, and do not replace the sign-off. Confirmed 2026-11-02.

## UR-08 "I could not check" is a pause, not a failure

**In one sentence:** if a check cannot run (a tool is missing, it takes too long), the change waits. It does not fail.

**Example:** the test runner is not installed on the build machine. The tool does not say "tests failed". It puts the change into *waiting*, says which program is missing, and does not use up any retry. After Ada installs the runner, she resumes the change.

**What the method does:** every gate gives one of three results: satisfied, not satisfied, or not evaluable. Not evaluable never counts as a failure.

**Missing or risky today:** nothing forces a deadline. A change could wait for a long time. An optional expiry date exists, but an overdue wait stays a wait.

**Spec:** 23.6, 24.2. **Replaces:** UR-011.

**Decision:** keep, with one addition: an approved list of required tools. A check that cannot run because an approved tool is missing is a wait. A check that cannot run for any other reason (tool not on the list) is a failure. Weak spot: overdue waits appear as a warning in every status report, naming the owner who must act; nothing happens automatically. Open point: the approved tool list is part of the frozen definitions (UR-05), so changing it needs approval.

## UR-09 Serious failures end the change, milder ones ask you

**In one sentence:** a *hard* failure closes the change as failed on its own. A *soft* failure stops it and asks a human what to do.

**Example:** builder changes a file outside the allowed folders. That is a hard failure: the next close attempt ends the change as failed and names the file. A flaky test that failed three times is a soft failure: the change waits, and Ada chooses either "close as failed" or "allow two more tries" (an override with a reason).

**What the method does:** each fail gate has a severity (`hard` or `soft`). Soft failures never end a change automatically. An override needs a human, a reason and a number of further attempts (at least 1).

**Missing or risky today:** the spec fixes no default number of tries on purpose. The change author decides which gates are hard or soft (and the freeze in UR-05 protects that choice).

**Spec:** 12, 24.7. **Replaces:** UR-012.

**Decision:** keep. Weak spot: both. The approval summary shows hard/soft clearly and marks checks the author set softer than the project default; and a default number of tries is set per level (value to be fixed in the spec; authors may only lower it).

## UR-10 Waiting and open questions are visible and block progress

**In one sentence:** when something is unclear, the work stops with a clear question, and nobody can proceed on a guess.

**Example:** builder is not sure whether old accounts need migrating. It records a question "Q1: migrate old accounts? yes / no" owned by Ada and the change waits on Q1. Ada cannot approve the spec while Q1 is open, and the change cannot close. Ada answers "yes". The question is recorded; then the change can be resumed.

**What the method does:** a wait states reason, what is missing, who must act, and when it can resume. Questions are part of the recorded state, not text in a document. Silence is never an answer.

**Missing or risky today:** an answer does not resume the change by itself. Someone must run `resume`.

**Spec:** 11, 23.5, 24.8. **Replaces:** UR-013, 014.

**Decision:** keep. Weak spot: depends on who answers. If the answerer is allowed to resume, answer and resume happen in one step (the answerer confirms "answer and resume"). If the answerer is not allowed to resume, the status report says "ready to resume" and names who can.

## UR-11 Some decisions are for humans only, and the claim "I am human" has a stated strength

**In one sentence:** an agent can never approve, sign off, cancel or override on its own, and every action records how well the identity was checked.

**Example:** `agent:builder` tries to approve a sign-off gate. It is rejected: the name does not start with `human:`. Ada, as `human:ada`, approves it. The record says "level A0, self-declared".

**What the method does:** approvals, sign-offs, overrides, answers to human-owned questions, `fail`, `cancel`, `supersede` and `adopt` need an identity that starts with `human:`. Level A0 (self-declared) is built into the core. Levels A1 and A2 (platform review, signature) exist in an optional Signing Extension. If a higher level is required and cannot be shown, the action is rejected.

**Missing or risky today:** at A0 anybody can type `human:` in front of a name, including an agent that uses a human's account. The core method cannot prevent this. Real protection needs the Signing Extension, and even that does not prove a human is present.

**Spec:** 5.4, 23.4, 24.3, Signing Extension. **Replaces:** UR-015, 016.

**Decision:** keep, with two additions: (1) a list of approved humans (owner plus named deputies); a `human:` name not on the list is rejected; only the owner can change the list (this also answers the UR-05 deputy-list question); (2) the real Git/GitHub account is recorded next to the typed `human:` name, so a mismatch is visible afterwards. The Signing Extension stays optional.

## UR-12 A change stays inside its declared scope

**In one sentence:** a change may only touch the files and folders it lists, and touching anything else ends it as failed.

**Example:** the scope is `lib/**`. builder also fixes a typo in `docs/guide.md`. At the next close the tool compares the working copy with the starting point and finds `docs/guide.md` outside the scope. The change is closed as failed, and the record names the file.

**What the method does:** records the starting revision, measures all changed paths (committed, staged, unstaged, new), and treats any path outside the allowed list as a hard failure. The change's own record files are exempt.

**Missing or risky today:** files hidden by a `.gitignore` that existed at the start are invisible, so a change can alter ignored files unnoticed. Other unfinished work in the same folder counts against the change, so the change needs a clean, separate working copy. For a solo developer this may feel strict.

**Spec:** 24.5. **Replaces:** UR-017.

**Decision:** keep as is. Accepted limits: ignored files stay invisible to the scope check, and the change needs a clean, separate working copy.

## UR-13 The history cannot be rewritten unnoticed

**In one sentence:** every action is recorded in an append-only chain, so edits by hand or deleted entries are detected.

**Example:** someone edits `state.json` to change a failed change to "done". The tool recomputes the chain, sees that a stored fingerprint no longer matches and refuses to act on that change.

**What the method does:** each history entry holds a fingerprint of itself and of the entry before it. An optional "anchor" stored outside the project remembers the latest entry, so that cutting off the last entries is also detected. If the project requires the strongest identity level (A2), the anchor is mandatory.

**Missing or risky today:** someone who can write both the history and the anchor can rewrite both. It protects against accidents and partial tampering only.

**Spec:** 23.1, 24.4. **Replaces:** UR-018.

**Decision:** keep, with one addition: the anchor stays optional, but the limit is stated plainly in the approval summary, and the status report says when no anchor is set, so the owner knows the protection is weak.

## UR-14 Old, known test failures do not block new work

**In one sentence:** you can list tests that were already failing, so only *new* failures count.

**Example:** the test suite has two old failures (`t1`, `t2`). The change adds a third (`t9`). The gate would normally fail on all three. With a baseline listing `t1` and `t2`, the gate fails only because of `t9`, and the record names `t9`.

**What the method does:** a baseline on a test gate; part of the frozen definitions, so adding a name later needs your approval.

**Missing or risky today:** each gate must say how failure names are read from the test output. A baseline has no expiry.

**Spec:** 24.6. **Replaces:** UR-019.

**Decision:** keep (optional feature stays in the core), with one addition: each baseline name carries a written reason and a review date; past the date the status report shows a warning naming the owner, and the change is not blocked.

## UR-15 Names and commands are safe by construction

**In one sentence:** change names cannot escape their folder, and check commands cannot hide extra commands.

**Example:** a change named `../x` is rejected. A check command written as `run-tests --label "a; rm -rf /"` runs `run-tests` with that text as one argument; the `; rm -rf /` is not executed because no shell is used.

**What the method does:** strict rules for change identifiers (no slashes, no reserved names, unique ignoring case). Commands are argument lists run directly. The interpreter (for example your Python) is named in the project settings through a placeholder `@interpreter`, never discovered by searching the project.

**Missing or risky today:** pipes and redirections do not work; you wrap them in a script. A change can alter code in ignored folders that a command then runs, and the scope check will not see it.

**Spec:** 4.3, 24.10. **Replaces:** UR-020, 024.

**Decision:** keep, with one addition: the guide gets a short ready-made example of a wrapper script for pipes and redirections. The ignored-folder gap stays an accepted limit (same as UR-12).

## UR-16 Independent review, with an end

**In one sentence:** when review is required, a second participant checks the work in one round plus at most one re-check, and you decide each finding.

**Example:** builder asks `reviewer` to review. The reviewer reports ten findings. Ada marks seven *fix*, two *defer*, one *reject*. builder applies the seven fixes. The reviewer re-checks only those seven. Nothing new may be raised about the old text. The cycle ends.

**What the method does:** a bounded cycle, a reviewer different from the author, findings with severity, your disposition for each, and the result kept as evidence. An open blocking finding stops completion until you disposition it. You may order more rounds by an explicit, recorded instruction.

**Missing or risky today:** the tool does not yet have a gate that checks "the required review is done". A `review` gate kind is explicitly invalid. A human sign-off gate is the workaround.

**Spec:** 3.10, 14, 20. **Replaces:** UR-021.

**Decision:** keep, with one addition: a `review` gate that passes only when the review report is attached and every blocking finding has the owner's decision (structural check, like UR-01). This reopens the spec rule that a `review` gate kind is invalid; confirm when the spec text is edited.

## UR-17 Agents follow a routine and stop at big decisions

**In one sentence:** an agent loads the context, works in scope, checks the gates in a fixed order, and returns anything big to you.

**Example:** builder finds that the spec conflicts with an accepted decision (ADR). It writes down the conflict, stops, returns the requirement to Ada, and waits. It does not "make it work" with a workaround.

**What the method does:** an eight-step routine, a list of prohibitions (do not invent goals or approvals, do not treat silence as consent, do not hide errors, do not leave the scope), and four allowed answers to a mismatch between code and spec (fix the code, change and re-approve the spec, record an accepted exception, or stop). Breaking changes need your approval.

**Missing or risky today:** most of this is conduct. Only some parts (scope, gates, human-only actions) are enforced by the tool.

**Spec:** 13, 19, 19.1. **Replaces:** UR-022, 023.

**Decision:** keep, with two additions: (1) the approval summary lists plainly which rules the tool enforces and which are conduct only; (2) at close, an "agent report" is added to the history: errors seen, decisions returned to the owner, exceptions recorded. Confirmed 2026-11-02: the agent report is required when an agent closes a change (the UC-03 exception) and optional when a human closes.

## UR-18 Works alone or together with other tools

**In one sentence:** the method does not depend on one agent, IDE or framework, and a tool you add cannot skip a gate.

**Example:** a team uses another planning framework. GG-SAD keeps the goal, gates, state and closure. The other framework may keep its own planning notes. A mapping states which side is authoritative for each fact.

**What the method does:** two operating modes (stand-alone and combination) and a list of what a mapping contract must contain.

**Missing or risky today:** combination mode is described but not built in the reference implementation, and adds no gates to a `core` change.

**Spec:** 1, 3.8, 17. **Replaces:** UR-025.

**Decision:** change: combination mode moves to "future" (same treatment as the tool-mapping layer in UR-04). The core only promises that it works alone and does not depend on one agent, IDE or framework. Plus: the tool refuses to start when the project settings ask for combination mode, and the spec and guide mark it "described, not built". Confirm the exact refusal wording when the spec text is edited.

## UR-19 Little documentation, concrete examples

**In one sentence:** the method asks for a few project documents with templates, says each fact once, and wants every behavioural rule to come with an example.

**Example:** the project has a constitution, a brief, an architecture, a roadmap and decisions (ADRs). A requirement "a rejected name creates nothing" comes with a case: given the name `../x`, when `new` is requested, then it is rejected and nothing is written.

**What the method does:** project documents with templates in `.ggsad/templates/`, one place per fact, and at least one example per behavioural requirement.

**Missing or risky today:** the specification itself carries a representative set of 109 examples, not one per rule (known and accepted). It is not stated which project documents are optional in `lean`.

**Spec:** 3.5, 3.9, 4.2, 16. **Replaces:** UR-026, 027.

**Decision:** keep, with two additions: (1) the profile table states in plain words which project documents are required and which are optional per profile; (2) the tool warns, without blocking, when a required document is missing at approval. Confirmed 2026-11-02: in `lean`, the project brief and the constitution are required; the others are optional. Required documents for the other profiles are still to be listed in the profile table. The 109-example limit stays accepted.

## UR-20 Optional project memory

**In one sentence:** a project may keep notes on decisions, lessons, failures, definitions and outside sources, but they never replace the governing documents.

**Example:** the team records "we tried library X and it failed under load". An agent can find it next time. A design decision still goes into an ADR, not into memory.

**What the method does:** names five record types and the rule "memory never replaces ADRs".

**Missing or risky today:** no reference implementation exists. It is optional.

**Spec:** 18. **Replaces:** UR-028.

**Decision:** keep (optional, stays in the core spec), with two additions: (1) when a note and an ADR disagree, the ADR wins and the note must be marked "outdated"; (2) each of the five record types gets a tiny template (date, title, one sentence, link to source). No tool is built.


## UR-21 Worked examples show how a project of each kind uses the method

**In one sentence:** the repository ships three small, complete example projects, so a newcomer can copy one and see every document and every step of a real change.

**Example:** Ada runs a solo side project. She opens `examples/solo-developer/`, sees the project documents she needs under `lean` (brief and constitution), one finished change from `change.yaml` to `closed`, and one change that is waiting. She copies the folder and changes the names.

**What the method does:** `examples/lean-startup/`, `examples/solo-developer/` and `examples/governed-enterprise/` each hold the required project documents of their compliance profile (Section 4.2), one change that ends as `done`, one that waits (with owner and resume condition), one that fails, and the role settings (Section 3.11: Requestor list, Reviewer, Approver, `team_mode`). Every example is labelled "example, not a real project", and uses the same file layout as a real project.

**Missing or risky today:** the three folders exist and are empty. Examples can drift away from the specification when the specification changes, and nothing checks them. Human Reviewers do not exist in version 1, so the examples show agent Reviewers only.

**Spec:** 4.2, 3.11, 23. **Replaces:** nothing (the legacy CHG-002 draft was discarded).

**Decision:** proposed. (Keep, change, or defer? Suggested changes: 1 = the examples are checked by the tool, so a wrong example fails the repository checks; 2 = as 1, plus one short "how to read this example" page per folder.)
