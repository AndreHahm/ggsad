# Project Brief

## Metadata

- Project ID: <id>
- Project Name: <name>
- Status: draft | active | waiting | closed | superseded
- Owner: <name-or-role>
- Last Updated: <ISO-8601 date>

## Problem and Opportunity

<Describe the problem, need, or opportunity.>

## Target Users and Stakeholders

| User or Stakeholder | Need or Interest | Decision Role |
|---|---|---|
| <name-or-group> | <need> | owner | approver | contributor | informed |

## Desired Outcomes and Success Signals

- <verifiable outcome or signal>

## Project Type and Lifecycle Context

- Project Type: greenfield | brownfield | migration | modernization | re-engineering | mixed
- Repository Type: single-repository | multi-repository | monorepo
- Delivery Context: prototype | pre-PMF | product | platform | enterprise | regulated

## Scope

### Included

- <included capability or boundary>

### Excluded / Non-Goals

- <excluded capability or outcome>

## Constraints

- Time:
- Budget:
- Technology:
- Delivery:
- Security:
- Data Privacy:
- Operations:

## Compliance Profile

- Active Profile: lean | standard | governed | regulated | <custom>
- Profile Rationale: <why this profile fits>
- Required External Controls: <standard, regulation, contract, or None>

## GG-SAD Operating Mode

- Mode: stand-alone | combination

## Integrated Methods, Frameworks, Tools, and Agents

| Integration | Version | Purpose | GG-SAD Mapping | Source of Truth |
|---|---|---|---|---|
| <name> | <version> | <capability> | <mapping path> | GG-SAD | integration |

## Enabled Practices and Combination Recipes

| Practice or Recipe | Status | Scope | Required By | Configuration / Reference |
|---|---|---|---|---|
| Example-Driven Specification | enabled | all behavioral requirements | GG-SAD core | `.ggsad/config.yaml` |
| Pair Review | enabled | <phases-or-change-types> | compliance | project scope | risk | `.ggsad/config.yaml` |

## Pair Review Policy

- Default Requirement: optional | required
- Activation Basis: compliance profile | project scope | change class | risk | artifact type | custom
- Allowed Participant Types: human | agent | external-review-service
- Human–Human Allowed: yes
- Distinct Requestor and Reviewer Required: yes
- Separate Human Approval Required: yes | no | conditional
- Separate `review.md`: optional | conditional | mandatory
- Blocking Finding Resolution Rule: <rule>

## Product and Delivery Assumptions

- <assumption with validation or expiry condition>

## Key Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| <risk> | low | medium | high | <mitigation> | <owner> |

## Open Decisions

- <decision required, owner, and due condition>

## Related Governing Artifacts

- Constitution: `docs/constitution.md`
- Architecture: `docs/architecture.md`
- Roadmap: `docs/roadmap.md`
- ADRs: `docs/adr/`
- GG-SAD Configuration: `.ggsad/config.yaml`
