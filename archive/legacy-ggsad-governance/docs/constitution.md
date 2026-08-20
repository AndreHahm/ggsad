# GG-SAD Project Constitution

## Metadata

- Project: GG-SAD Reference Implementation
- Status: Active
- Constitution Version: 0.2
- Method Baseline: GG-SAD 1.2
- Last Updated: 2026-08-03

## 1. Purpose

This constitution defines the non-negotiable rules for developing, reviewing, verifying,
releasing, and maintaining the GG-SAD reference implementation.

All humans, agents, automation, integrations, and companion methods operating in this repository
MUST follow this constitution.

## 2. Normative Language

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

- **MUST / MUST NOT** indicate mandatory requirements.
- **SHOULD / SHOULD NOT** indicate strong recommendations; deviations require documented
  justification.
- **MAY** indicates an optional capability or approach.

## 3. Order of Precedence

In case of conflict, the following order applies:

1. `docs/constitution.md`
2. accepted ADRs under `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. approved scoped Decisions that do not replace an ADR
6. approved change `spec.md`
7. approved change `plan.md`
8. change `tasks.md`
9. implementation and tests
10. evidence, generated summaries, GSD `.planning/` artifacts, notes, and temporary work

A lower-precedence artifact MUST NOT silently override a higher-precedence artifact.

## 4. Invariant GG-SAD Core

Every governed change MUST preserve:

- an explicit goal;
- a specification anchor appropriate to the change size;
- gate evaluation;
- evidence appropriate to the active profile;
- controlled wait behavior;
- controlled fail behavior;
- a traceable final status.

No profile, integration, shortcut, or agent instruction may remove these invariants.

## 5. Goal and Scope Control

- Every material change MUST have an explicit goal and success signals.
- Scope and non-goals MUST be stated before implementation.
- Agents MUST NOT invent requirements, approvals, constraints, or product goals.
- Work outside the approved scope MUST stop and return to the Requestor or decision owner.
- Exploration MUST NOT silently become production implementation.
- Opportunistic refactoring, broad formatting, and unrelated cleanup are prohibited unless
  explicitly included.

## 6. Specification and Architecture

- The approved specification is the binding change anchor.
- Behavioral requirements MUST include concrete acceptance examples or a justified alternative
  verifiable condition.
- Code, tests, plans, and evidence MUST remain consistent with the approved specification.
- Existing accepted ADRs take precedence over new requirements and plans.
- A discovered ADR conflict MUST stop affected planning or implementation.
- Durable architecture decisions MUST use the ADR process.
- Implementation convenience MUST NOT redefine architecture or project policy.

## 7. Gate-Controlled Flow

Every applicable transition MUST evaluate gates in this order:

1. Definition of Fail;
2. Definition of Wait;
3. current-phase Definition of Done;
4. next-phase Definition of Ready.

A satisfied Definition of Done does not override an active fail or wait condition.

State changes MUST occur through validated transition actions. Direct or arbitrary status mutation
is prohibited.

## 8. Evidence and Traceability

- A status MUST NOT be set solely by assertion.
- Evidence MUST be reproducible or reference a durable result.
- Requirements and acceptance examples MUST be traceable to verification evidence.
- Missing required evidence MUST block closure.
- Raw logs SHOULD be referenced rather than copied into governed documents.
- Evidence MUST NOT contain secrets or unnecessary sensitive data.
- Unexecuted checks MUST be reported as not run, never as passed.

## 9. Pair Review

- Pair Review is optional by default and may become mandatory through profile, scope, change
  class, risk, affected artifact, or local policy.
- Requestor and Reviewer MUST be distinct participant identities in the same review cycle.
- Human–Human, Human–Agent, Agent–Human, Agent–Agent, and approved external review-service
  combinations are permitted.
- The Reviewer MUST NOT silently modify the Requestor's governed work product during review.
- Findings MUST return to the Requestor for disposition.
- Unresolved blocking findings MUST block the applicable gate.
- Pair Review MUST NOT replace required human approval.
- A second pass, subagent, or new context of the same participant is not automatically an
  independent review.

## 10. Human Approval Boundaries

Explicit human approval is required for:

- constitutional changes;
- accepting, superseding, or materially changing an ADR;
- project-scope or core non-goal changes;
- breaking changes where approval is required;
- weakening a profile, gate, test, evidence, security, or review control;
- destructive repository, data, migration, publication, or release actions;
- treating a material deviation as accepted;
- stable releases until policy explicitly changes.

Agents may prepare options and recommendations but MUST NOT fabricate or self-issue human
approval.

## 11. Engineering Quality

All production changes MUST:

- use focused, reviewable edits;
- preserve the approved architecture and coding conventions;
- include or update tests appropriate to risk;
- pass required formatting, linting, typing, tests, and build checks;
- document justified deviations and limitations;
- avoid unnecessary dependencies and components;
- keep public interfaces explicit and versioned.

Baseline quality commands are:

```bash
uv sync
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
uv build
```

Additional security, schema, Markdown, YAML, compatibility, and packaging checks apply when
relevant.

## 12. Testing Rules

- Tests MUST verify approved behavior rather than implementation trivia.
- Negative, failure, recovery, permission, and boundary behavior MUST be covered according to
  risk.
- State transitions and profile resolution SHOULD use property-based tests.
- A failing test MUST NOT be deleted, skipped, or weakened merely to make a change pass.
- Test exclusions require a documented rationale and approval where material.
- Required regression tests MUST pass before closure.

## 13. Security and Repository Safety

- Secrets MUST NOT be committed or stored in governed artifacts.
- Least-privilege access applies to humans, agents, CI, and integrations.
- Destructive commands require explicit authorization.
- Agents MUST NOT run force-push, history rewriting, destructive reset, destructive clean,
  release, publication, or destructive migration commands without authorization.
- Dependencies MUST be pinned through the project lockfile and reviewed for necessity.
- Security findings with blocking severity MUST stop the applicable transition.
- Tool output used as evidence MUST be sanitized when necessary.

## 14. Tool and Integration Independence

- The Method Core MUST NOT depend on a specific agent, IDE, CI platform, issue tracker, or
  repository host.
- Integrations MUST be optional adapters.
- Removing an integration MUST preserve GG-SAD artifacts and stand-alone operation.
- External workflows MUST NOT bypass state, gate, approval, or closure rules.
- Integration conflicts MUST produce a controlled wait or fail outcome according to policy.

## 15. GSD Companion Rules

GSD is the initial execution companion.

When enabled:

- `.planning/` contains subordinate execution and context-engineering artifacts;
- GG-SAD owns goal, specification, state, gates, precedence, evidence requirements, approvals,
  and closure;
- GSD MUST NOT approve specifications or transitions;
- GSD MUST NOT silently modify project-wide governing documents;
- GSD output MUST be reviewed for scope expansion, duplicate truth, unsupported dependencies,
  premature components, and contradictions;
- conflicts are corrected in GSD artifacts or returned for decision, not resolved by weakening
  GG-SAD.

## 16. Documentation Rules

- English is the normative repository language.
- One fact SHOULD have one authoritative home.
- References are preferred to duplicated text.
- Placeholders MUST be resolved before an artifact is approved or completed.
- Generated or temporary summaries MUST be labeled non-authoritative.
- Documents MUST remain readable without proprietary tooling.
- Public documentation MUST not promise capabilities that are not implemented and verified.

## 17. Anti-Overhead Rules

1. No artifact without a clear consumer.
2. No new document when a section is sufficient.
3. No task checklist when execution is obvious.
4. No separate plan without relevant uncertainty, risk, or coordination need.
5. No duplicate evidence.
6. No new agent role without a genuine permission, context, or independence boundary.
7. No hook when explicit validation is sufficient.
8. No tool-specific dependency in the Method Core.
9. No local weakening of higher-precedence gates.
10. Every component and dependency must justify its workflow and maintenance cost.

## 18. Change and Release Discipline

- Changes SHOULD be delivered as vertical slices.
- Large initiatives MUST be decomposed into independently governed changes.
- Change classes S, M, and L determine artifact depth, not importance alone.
- A change may close only when no active DoF or DoW condition remains and all applicable DoD
  criteria and evidence requirements are satisfied.
- Releases require documented version, release notes, verification, known limitations, and
  rollback or an explicit statement that rollback is not required.
- Roadmap and governing documentation MUST be updated when the verified system state changes.

## 19. Amendment Process

A constitution amendment requires:

1. a dedicated governed change;
2. a documented reason and impact analysis;
3. review against existing ADRs and the normative GG-SAD baseline;
4. independent review;
5. explicit human approval;
6. version and history updates.

No implementation change may amend this constitution indirectly.
