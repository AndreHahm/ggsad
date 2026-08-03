# Definition of Done

## Purpose

The Definition of Done (DoD) determines whether the current phase has completed successfully.

Completion requires evidence. A statement that work is finished is not sufficient.

A satisfied DoD does not override an active Definition of Fail or Definition of Wait condition.

## General Done Criteria

Unless strengthened by profile or local specification, a phase is done when:

- its stated goal has been achieved;
- required outputs are complete;
- applicable criteria have verifiable evidence;
- required review and approvals are recorded;
- no unexplained deviation remains;
- known limitations and risks are documented;
- governed artifacts are internally consistent;
- the current state is safe and reproducible;
- the next phase can evaluate its Definition of Ready.

## Intake Done

Intake is done when:

- the request is understandable;
- the goal or problem and expected benefit are recorded;
- Requestor and decision owner are identified;
- change type, expected class, and affected areas are classified;
- duplicates, conflicts, dependencies, and prerequisite decisions are identified;
- the appropriate workflow and initial priority are selected;
- the change can proceed, wait, stop, or enter exploration explicitly.

## Explore and Decide Done

Exploration is done when:

- the defined uncertainty has been reduced sufficiently;
- observations, assumptions, evidence, and limitations are recorded;
- viable options and trade-offs are documented;
- architecture decisions requiring ADRs are identified;
- production work has not started without approval;
- an explicit proceed, revise, wait, defer, or stop decision exists.

## Specification Done

Specification is done when:

- goal, benefit, and success signals are described;
- relevant context is documented;
- scope and non-goals are explicit;
- requirements are unambiguous and verifiable;
- every behavioral requirement has at least one concrete acceptance example or a justified
  alternative condition;
- risk-appropriate negative, failure, and boundary behavior is covered;
- constraints and compatibility expectations are documented;
- open questions are closed or explicitly accepted;
- ADR conflicts are resolved or returned to the Requestor;
- required approval is recorded.

## Plan Done

Planning is done when:

- the technical approach is described;
- affected components and artifact paths are identified;
- architecture, data, API, security, operational, and compatibility impacts are assessed;
- test and verification strategy is defined;
- migration, rollout, rollback, and preservation needs are clarified;
- dependencies, permissions, and prerequisites are known;
- risks and decisions are documented;
- implementation is decomposed appropriately;
- execution tasks remain subordinate to the approved specification.

## Design and Architecture Done

Design is done when:

- material boundaries, responsibilities, interfaces, and dependency directions are explicit;
- relevant data, API, event, persistence, migration, security, operational, and user-flow
  behavior is described;
- durable architecture decisions are recorded in accepted ADRs;
- `docs/architecture.md` reflects the approved current structural direction where applicable;
- critical design risks and trade-offs have been reviewed;
- the design remains consistent with the approved specification and constitution.

## Build Done

Build is done when:

- all approved behavior is implemented;
- no unintended scope was introduced;
- architecture and ADR constraints are respected;
- tests were added or updated;
- required formatting, linting, typing, tests, and build checks succeed;
- documentation and examples are updated;
- migrations and configuration changes are included where approved;
- deviations from specification or plan are explained and approved;
- the implementation is stable enough for verification and review.

## Verify Done

Verification is done when:

- every acceptance condition is verified;
- required automated tests succeed;
- risk-relevant negative, failure, recovery, permission, and boundary cases are checked;
- required regression and compatibility tests succeed;
- applicable security, accessibility, performance, reliability, and packaging checks succeed;
- requirement-to-example-to-evidence links are complete;
- deviations and remaining limitations are documented;
- evidence is reproducible or references durable reports;
- no required check is falsely reported as passed.

## Pair Review Done

Pair Review is done when:

- Requestor and distinct Reviewer identities are recorded;
- review scope and criteria are complete;
- findings have stable identifiers, severities, statuses, and dispositions;
- findings were returned to the Requestor;
- required corrections are complete;
- blocking findings are resolved and verified, withdrawn, or formally dispositioned;
- the final review result is preserved as evidence;
- required human approval remains separately recorded.

## Release Readiness Done

Release readiness is done when:

- verification and review gates pass;
- unresolved defects, deviations, risks, and limitations are reviewed;
- version, changelog, release notes, and migration guidance are prepared;
- artifact integrity and provenance checks are complete where required;
- rollout, rollback, backup, and recovery are ready;
- operational ownership, monitoring, and support are ready;
- required approvals are recorded.

## Release Done

Release is done when:

- approved artifacts are built and published or deployed;
- version and immutable release reference are recorded;
- smoke tests succeed;
- monitoring shows no critical problem;
- release notes and known limitations are published;
- rollback or withdrawal remains possible or is explicitly not required;
- release evidence is recorded;
- roadmap, supported-version information, and status are updated.

## Closure Done

A change is closed only when:

- no DoF condition is active;
- no DoW condition is active;
- all applicable phase DoD criteria are satisfied;
- required evidence is complete;
- required Pair Review is complete;
- blocking findings are resolved or formally dispositioned;
- specification, implementation, tests, and documentation are consistent;
- relevant project documents and references are updated;
- final status and history are recorded traceably.

## Quality Baseline

For Python implementation changes, the baseline is:

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv build
```

Additional checks apply according to the changed artifact and risk.

Local DoD criteria may strengthen these rules but MUST NOT silently weaken them.
