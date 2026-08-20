# Definition of Ready

## Purpose

The Definition of Ready (DoR) determines whether the next phase may begin.

A phase MUST NOT start merely because work is available or an agent can perform it. Its applicable
DoR criteria must be satisfied and no active Definition of Fail or Definition of Wait condition
may exist.

## Evaluation Position

Gate evaluation order is:

1. Definition of Fail;
2. Definition of Wait;
3. current-phase Definition of Done;
4. next-phase Definition of Ready.

## General Ready Criteria

Unless a profile or local specification strengthens them, the next phase is ready when:

- the goal and expected benefit are understandable;
- the active change and owner are identified;
- scope and non-goals are explicit;
- required governing artifacts have been read;
- required inputs, permissions, tools, and dependencies are available;
- blocking decisions and contradictions are resolved;
- applicable approval and review prerequisites are satisfied;
- required evidence expectations are defined;
- the current repository or working state is safe;
- no active DoF or DoW condition exists.

## Ready to Intake

Intake may begin when:

- a problem, opportunity, defect, request, or maintenance need is described;
- an initial Requestor or decision owner exists;
- the request is not obviously prohibited by the constitution;
- enough context exists to classify the work.

## Ready to Explore

Exploration may begin when:

- a specific uncertainty or decision question is defined;
- the exploration scope and time or resource boundary are explicit;
- production implementation is prohibited unless separately authorized;
- expected output and decision owner are identified.

## Ready to Specify

Specification may begin when:

- the goal or problem is described;
- expected benefit is understandable;
- the Requestor or decision owner is identified;
- known constraints are available;
- affected system areas are roughly known;
- no obvious constitutional conflict exists;
- any required exploration output is available.

## Ready to Plan

Planning may begin when:

- goal, success signals, scope, and non-goals are defined;
- requirements are understandable and verifiable;
- behavioral requirements include acceptance examples or justified alternatives;
- relevant architecture and accepted ADRs have been reviewed;
- open questions are resolved or explicitly accepted;
- no unresolved contradiction exists;
- specification approval required by policy is recorded.

## Ready to Design and Architecture

Design work may begin when:

- the approved specification identifies material architecture, interface, data, security,
  operational, or user-experience impact;
- design questions and decision owners are explicit;
- relevant existing architecture and ADRs have been reviewed;
- required stakeholders and reviewers are available;
- prohibited or non-goal solution directions are clear.

## Ready to Build

Implementation may begin when:

- the specification is approved;
- the technical approach is sufficiently clear;
- required design and ADR decisions are accepted;
- critical risks are assessed;
- dependencies, tools, permissions, and environments are available;
- test and verification criteria are defined;
- rollback or preservation behavior is defined where needed;
- no blocking decision, review finding, or approval is outstanding;
- the working tree and active scope are understood.

## Ready to Verify

Verification may begin when:

- the planned implementation is complete or sufficiently testable;
- relevant tests and fixtures exist;
- build and analysis tools are available;
- acceptance examples and required evidence are identified;
- known deviations are documented;
- the review target is stable when independent review is required.

## Ready to Review

Pair Review may begin when:

- Pair Review is required or explicitly selected;
- Requestor and distinct Reviewer identities are recorded;
- review scope and criteria are defined;
- a stable reviewable work product exists;
- governing specification, plan, architecture, tests, and existing evidence are available;
- known deviations, skipped checks, and limitations are disclosed.

## Ready to Release

Release may begin when:

- build and required tests have succeeded;
- applicable quality, security, compatibility, and compliance gates are satisfied;
- required Pair Review is complete;
- unresolved blocking findings do not remain;
- migration, rollout, rollback, and recovery are clarified;
- known limitations are documented;
- release notes and version information are prepared;
- required human approvals are recorded;
- release credentials and operational owners are available.

## Ready to Close

Closure may begin when:

- all required phases are complete;
- no DoF or DoW condition is active;
- requirement and acceptance-example coverage is evidenced;
- required Pair Review cycles are complete;
- blocking findings are resolved or formally dispositioned;
- specification, implementation, tests, and documentation are consistent;
- deviations and limitations are accepted where required;
- roadmap, architecture, ADR, and status updates are complete;
- final state and history can be recorded atomically.

## Class and Profile Tailoring

- Class S may use an inline specification when the active profile permits it.
- Class M normally requires a separate specification and may require plan and evidence artifacts.
- Class L must be decomposed where possible and requires stronger architecture, risk, review, and
  evidence readiness.
- `lean` may reduce optional artifacts.
- `standard` requires defined quality gates and recorded evidence.
- `governed` adds explicit review and approval readiness.
- `regulated` adds segregation of duties, retained evidence, and formal approval readiness.

Local DoR criteria may strengthen these rules but MUST NOT silently weaken them.
