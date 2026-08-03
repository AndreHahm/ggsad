# Project Constitution

## Metadata

- Project: <project-name>
- Status: Draft | Active | Superseded
- Constitution Version: <version>
- Effective Date: <YYYY-MM-DD>
- Last Updated: <YYYY-MM-DD>
- Decision Owner: <name-or-role>
- Approved By: <name-or-role-or-pending>
- Related Change: <change-id-or-none>

## 1. Purpose

<Explain why this constitution exists and which project-wide behavior it governs.>

This constitution defines the non-negotiable rules for humans, agents, automation, integrations,
and companion methods operating in this repository.

## 2. Normative Language

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

- **MUST / MUST NOT** indicate mandatory requirements.
- **SHOULD / SHOULD NOT** indicate strong recommendations; deviations require documented
  justification.
- **MAY** indicates an optional capability or approach.

## 3. Order of Precedence

In case of conflict, apply the following order:

1. `docs/constitution.md`
2. accepted ADRs under `docs/adr/`
3. `docs/project-brief.md`
4. `docs/architecture.md`
5. approved scoped Decisions that do not replace an ADR
6. approved change specification `spec.md`
7. approved implementation plan `plan.md`
8. local task checklist `tasks.md`
9. implementation and tests
10. evidence, reports, derived summaries, and temporary work artifacts

A lower-precedence artifact MUST NOT silently override a higher-precedence artifact.

## 4. Project Principles

### 4.1 <Principle Name>

<Define the principle and its mandatory consequences.>

### 4.2 <Principle Name>

<Define the principle and its mandatory consequences.>

## 5. Goal and Scope Control

- Every material change MUST have an explicit goal.
- Scope and non-goals MUST be stated before implementation.
- <Add project-specific scope rules.>
- <Add prohibited scope behavior.>

## 6. Specification and Architecture Rules

- Approved specifications are binding change anchors.
- Existing accepted ADRs take precedence over new requirements and plans.
- Durable architecture decisions MUST use the ADR process.
- <Add project-specific architecture constraints.>
- <Add interface, data, deployment, or compatibility rules.>

## 7. Gate-Controlled Workflow

Every applicable transition MUST evaluate:

1. Definition of Fail;
2. Definition of Wait;
3. current-phase Definition of Done;
4. next-phase Definition of Ready.

State MUST change only through an approved transition process.

### 7.1 Definition of Ready Policy

<Define project-wide readiness expectations.>

### 7.2 Definition of Done Policy

<Define project-wide completion expectations.>

### 7.3 Definition of Wait Policy

<Define when work must pause safely.>

### 7.4 Definition of Fail Policy

<Define when work must terminate unsuccessfully.>

## 8. Evidence and Traceability

- Completion claims MUST be supported by verifiable evidence.
- Requirements and acceptance examples MUST be traceable to verification evidence.
- <Define required evidence types and retention.>
- <Define handling for deviations, limitations, and skipped checks.>

## 9. Pair Review and Approval

### 9.1 Pair Review Policy

- Default Requirement: Optional | Required
- Activation Basis: <profile, scope, class, risk, artifact type, or policy>
- Distinct Requestor and Reviewer Required: Yes
- Human–Human Allowed: Yes
- Separate Human Approval Required: Yes | No | Conditional

<Define blocking-finding behavior and review evidence requirements.>

### 9.2 Human Approval Boundaries

Explicit human approval is required for:

- <constitutional changes>
- <ADR acceptance or supersession>
- <breaking changes>
- <releases or publication>
- <destructive actions>
- <other project-specific decisions>

## 10. Engineering Quality

All production changes MUST:

- <quality requirement>
- <quality requirement>
- <quality requirement>

Baseline commands:

```bash
<format-command>
<lint-command>
<type-check-command>
<test-command>
<build-command>
```

## 11. Testing Rules

- <minimum test expectations>
- <negative and failure behavior expectations>
- <regression expectations>
- <test weakening or skipping policy>

## 12. Security and Safety

- Secrets MUST NOT be committed.
- Least privilege applies to humans, agents, automation, and integrations.
- Destructive operations require explicit authorization.
- <Add project-specific security constraints.>
- <Add privacy, data, or compliance constraints.>

## 13. Agent and Automation Rules

Agents MUST:

- <required behavior>
- <required behavior>

Agents MUST NOT:

- <prohibited behavior>
- <prohibited behavior>

## 14. Tool and Integration Independence

- <Define whether stand-alone operation is required.>
- <Define external integration authority and limits.>
- <Define conflict, failure, and uninstall behavior.>

## 15. Documentation Rules

- Project documentation language: <language>
- One fact SHOULD have one authoritative home.
- Generated summaries MUST be labeled as derived.
- <Add naming, structure, or update rules.>

## 16. Resource and Budget Constraints

- Time:
- Compute:
- Token or API Budget:
- Storage:
- Operational Cost:
- Retry Limits:
- Other:

## 17. Prohibited Actions and Dependencies

The following are prohibited unless explicitly approved:

- <action or dependency>
- <action or dependency>
- <action or dependency>

## 18. Breaking-Change Policy

<Define identification, assessment, approval, migration, communication, and failure behavior for
breaking changes.>

## 19. Release and Closure Rules

A change or release may close only when:

- <criterion>
- <criterion>
- <criterion>

## 20. Amendment Process

A constitution amendment requires:

1. a dedicated governed change;
2. documented rationale and impact;
3. review against accepted ADRs and method rules;
4. independent review where required;
5. explicit approval;
6. version and history updates.

## 21. Constitution History

| Date | Version | Status | Actor | Summary |
|---|---|---|---|---|
| <YYYY-MM-DD> | <version> | Draft | <actor> | Initial draft |
