# Roles in GG-SAD, version 1

Status: decided by the owner in the discussion of 2026-11-02, for approval. Not yet in the specification.

Characters: **Ada** is the owner of the project. **Bo** is a teammate. **builder** is the agent that does the work. **devin** and **codex** are agents that review.

## The idea in one paragraph

In version 1, agents do the work and the review. Humans decide. builder (an agent) builds. devin (a different agent from a different vendor) checks it. Ada and her teammates approve, decide on findings, and answer questions. A review that a human performs is declined by gg-sad, and so is any work action by an agent that is not on the list in the settings.

## The nine roles

| # | Role | Is | Named in | If not named (fallback) |
|---|---|---|---|---|
| 1 | Requestor | agent | the settings (a list) | none: an agent not on the list is declined |
| 2a | Reviewer | agent from a different vendor than the Requestor | the settings | see 2b |
| 2b | Reviewer, fallback | agent from a third vendor | the settings | none |
| 3a | Approver | human | the change | 3b |
| 3b | Approver, fallback | human | n/a | the Change owner |
| 4a | Decision owner | human | the review (one per review) | 4b |
| 4b | Decision owner, fallback | human | n/a | the Approver |
| 5 | Owner | human | the hosting service, or the local Git identity; confirmed once and saved in the settings | none |
| 6 | Deputies | humans | the deputy list in the settings | none |
| 7a | Change owner | human | the change | 7b |
| 7b | Change owner, fallback | human | n/a | the Author |
| 8a | Author | human | the change | 8b |
| 8b | Author, fallback | human | n/a | the human who first approves the spec, then the Owner |
| 9a | Question or wait owner | human | the question or wait | 9b |
| 9b | Question or wait owner, fallback | human | n/a | the Author for questions about `spec.md`; otherwise the Change owner |

## Role by role

### 1 Requestor (agent, from the settings)

**Story.** The settings list `agent:builder` as the Requestor. builder creates the change, does the work, asks for the review and asks to close. Another agent, `agent:helper`, tries to start the change. gg-sad declines it: helper is not on the list.

**What changes.** There is no human Requestor in version 1. The old lean rule that a human who requested the work may approve it ends: Ada approves as Approver. Ada can still write the spec, as Author.

### 2 Reviewer (agent, different vendor) and its fallback

**Story.** The settings name `agent:devin` as Reviewer and `agent:codex` as fallback. builder (Anthropic) is the Requestor. devin (Cognition) reviews. If devin cannot report, gg-sad moves to codex by itself and records it in the history.

**What changes.**
- The Reviewer must come from a different vendor than the Requestor. The settings record vendor and model of each agent. The fallback must differ from both.
- A review action performed under a `human:` name is declined. This is the rule that a human must not run the independent reviewer.
- The switch to the fallback is automatic, and the status report shows that it happened.

### 3 Approver (human, per change)

**Story.** Change C-7 names Ada as Approver. Ada approves its spec, its gates, its sign-offs, its overrides, the re-approval of edited gates, the review result, and edits to higher documents. Bo, a deputy, cannot approve C-7 unless Ada is recorded as unavailable.

**Fallback.** A change that names no Approver, or names someone who is not an approved human, uses the Change owner. The status report warns when the fallback is used, so a typo cannot silently change who approves.

**One human in several roles.** A new setting `team_mode: solo | team` (default `team`) decides.

| Profile | team | solo |
|---|---|---|
| lean | same human may be Author and Approver | allowed |
| standard | not allowed | allowed |
| governed | not allowed | allowed |
| regulated | never | never |

### 4 Decision owner (human, per review)

**Story.** A review reports ten findings. The review scope names Ada as Decision owner. She marks each finding `fix`, `defer` or `reject`. If the scope names nobody, the Approver decides.

**What changes.** One Decision owner per review, with no override per finding. The same human may be Author, Approver and Decision owner, subject to the table above. The review record states it.

### 5 Owner (human)

**Story.** Ada runs `git init` locally. At `init`, gg-sad proposes her Git identity as Owner. She confirms once, and it is saved in the settings with her account. Later the repository moves to an organisation and the service shows another owner. The settings win, and the status report warns about the difference.

**What the Owner does.** Keeps the list of approved humans and the deputy list, uses `repair`, and changes the Owner in the settings (an approval by the current Owner).

### 6 Deputies (humans, from the settings list)

**Story.** Ada is on holiday. Bo is on the deputy list. Ada recorded before leaving that she is unavailable. Bo may give the re-approval of gates and stand in for Ada as Approver or Change owner.

**What a Deputy never does.** `repair`, changing the lists, or changing the Owner.

**Empty list.** An empty deputy list is valid, except under `regulated`, which needs at least one Deputy.

### 7 Change owner (human, per change)

**Story.** Change C-10 names Bo as Change owner. builder asks a question and names no owner, so it goes to Bo. Bo can cancel, supersede or fail his own change. Approvals stay with the Approver. When Bo leaves in week three, the Owner or Bo hands the change to someone else; the history records the handover and the reason.

**Fallback.** The Author.

### 8 Author (human, named in the change)

**Story.** builder drafts `spec.md`. Ada reads it and is named in the change as Author. She answers questions about the text of the spec. If the change names no Author, the human who first approves the spec becomes the Author, and the Owner is the last fallback.

### 9 Question or wait owner (human)

**Story.** builder asks "Q2: three or five retries?" and names no owner. The question is about `spec.md`, so the Author answers. A wait that gg-sad creates itself (a soft failure, a missing tool) goes to the Change owner. If the owner is away, the Change owner or the Owner hands the question to another approved human, with a reason. Naming an agent as owner is declined.

## Consequences in the specification

These parts of the specification change when this file is approved:

- 3.10 Pair Review: the Reviewer must be an agent; the Human–Human, Agent–Human and Human–Agent combinations leave the normative text.
- 5.4 and 5.1: lean self-approval by the Requestor is replaced by the table in role 3.
- 14.2 and 14.3: roles, vendor rule, automatic fallback, one Decision owner per review.
- 23.1: the change definition names Approver, Decision owner (in the review scope), Change owner and Author; `team_mode` and the role lists are settings.
- 24.3: the list of approved humans carries the roles Owner and Deputy; a review action under a `human:` name is declined with its own issue code.
- 23.8: warnings when a fallback is used, when `team_mode` is `solo`, when no Deputy exists.
- New examples for the declined human reviewer, the automatic fallback Reviewer, and the Approver fallback.

## Future setup (not in version 1)

The roles will later be able to be played by:

- human Requestors and human Reviewers,
- agentic Approvers, Decision owners, Deputies, Change owners, Authors, and Question or wait owners.

The specification will describe this in its "future" section and will not build it.

## Points the owner may want to confirm

1. Three vendors are needed for the Requestor, Reviewer and fallback Reviewer. A project with fewer vendors cannot use the fallback.
2. The fallback Approver applies also when the named Approver is not an approved human; the warning is the safeguard.
3. The Decision owner is one per review. A finding cannot name a different one.
