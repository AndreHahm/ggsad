# Project Roadmap

## Metadata

- Project: <project-name>
- Status: Draft | Active | Superseded
- Last Updated: <YYYY-MM-DD>
- Owner: <name-or-role>
- Planning Horizon: <period-or-open-ended>

## Purpose

<Describe what this roadmap communicates and what it intentionally does not manage.>

This roadmap describes intended development direction. It is not a sprint backlog, epic hierarchy,
or substitute for governed change specifications.

## Roadmap Principles

- <principle>
- <principle>
- <principle>

## Now

### <Roadmap Item ID> — <Title>

- Status: Proposed | Ready | Active | Waiting | Done | Cancelled | Superseded
- Goal: <desired outcome>
- Rationale: <why now>
- Scope: <high-level boundary>
- Non-Goals: <excluded outcomes>
- Dependencies: <dependency or None>
- Risks: <key risk or None>
- Expected Evidence: <evidence>
- Related Changes: `<change-id-or-TBD>`
- Target Condition: <condition rather than unsupported date>
- Owner: <name-or-role>

**Exit Criteria**

- <criterion>
- <criterion>

## Next

### <Roadmap Item ID> — <Title>

- Status: Proposed
- Goal: <desired outcome>
- Dependency: <dependency>
- Admission Condition: <condition required before promotion to Now>
- Related Changes: <change-id-or-TBD>
- Owner: <name-or-role>

## Later

### <Roadmap Item ID> — <Title>

- Goal: <desired outcome>
- Why Deferred: <reason>
- Admission Signal: <evidence or condition>
- Owner: <name-or-role-or-TBD>

## Open

### <Open Topic ID> — <Decision or Question>

- Question: <open question>
- Why It Matters: <impact>
- Required Evidence: <evidence>
- Decision Owner: <name-or-role>
- Due Condition: <condition>
- Related ADR or Change: <reference-or-none>

## Deferred by Default

The following capabilities are not approved implementation scope unless a dedicated governed
change admits them:

- <capability>
- <capability>
- <capability>

## Completed

### <Roadmap Item ID> — <Title>

- Completed: <YYYY-MM-DD>
- Outcome: <verified result>
- Evidence: <reference>
- Related Changes: <change-id>
- Follow-Up: <reference-or-none>

## Dependencies

```text
<optional dependency diagram>
```

| Item | Depends On | Dependency Type | Resolution Condition |
|---|---|---|---|
| <item> | <item> | hard | soft | <condition> |

## Risks Across the Roadmap

| Risk | Affected Items | Impact | Mitigation | Owner |
|---|---|---|---|---|
| <risk> | <items> | low | medium | high | <mitigation> | <owner> |

## Roadmap Change Rules

- Promotion between horizons SHOULD be evidence-based.
- Roadmap entries MUST NOT silently create approved implementation scope.
- Architecture decisions MUST use ADRs.
- Material scope changes MUST use governed change specifications.
- Completed items MUST reference evidence.
- Obsolete items MUST be cancelled or superseded rather than silently removed.

## Roadmap History

| Date | Actor | Related Change | Summary |
|---|---|---|---|
| <YYYY-MM-DD> | <actor> | <change-id-or-none> | <summary> |
