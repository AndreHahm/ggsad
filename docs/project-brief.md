# Project Brief

## Metadata

- Project ID: `ggsad`
- Project Name: GG-SAD Reference Implementation
- Status: active
- Owner: Project Maintainer
- Last Updated: 2026-08-02

## Problem and Opportunity

AI-assisted software development often fails because goals, specifications, architecture,
permissions, state, approvals, and completion evidence are spread across chat sessions and
tool-specific workflows.

Existing specification-driven and agentic-development frameworks provide valuable planning and
execution capabilities, but they differ in governance strength, artifact models, context
management, portability, and compliance support.

The opportunity is to provide a lightweight, tool-independent method and reference implementation
that controls when humans and agents may start, continue, wait, fail, verify, release, and close
work—without imposing mandatory sprints, epics, heavyweight ceremonies, or a large agent swarm.

## Target Users and Stakeholders

| User or Stakeholder | Need or Interest | Decision Role |
|---|---|---|
| Solo developers | Fast, low-overhead, agent-safe delivery | user, contributor |
| Software teams | Shared goals, specifications, gates, and evidence | user, contributor |
| Technical leads and architects | Architecture precedence and controlled change | approver, contributor |
| Platform and enablement teams | Reusable profiles, mappings, and automation | user, contributor |
| Regulated or high-impact teams | Traceability, independent review, retained evidence | user, approver |
| Coding-agent users | Clear scope, permissions, wait/fail behavior, and closure rules | user |
| Open-source maintainers | Portable repository governance and contribution controls | owner, approver |
| GG-SAD maintainers | Stable method semantics and sustainable implementation | owner, approver |

## Desired Outcomes and Success Signals

- A repository can initialize a usable GG-SAD structure without a mandatory external platform.
- Class S, M, and L changes can be represented and validated.
- Valid and invalid state transitions are distinguished with clear explanations.
- Definition of Ready, Done, Wait, and Fail are operational and evaluated in the correct order.
- Lean, standard, governed, and regulated profiles resolve deterministically.
- Requirements and acceptance examples can be traced to evidence.
- Pair Review can be omitted or required deterministically.
- Distinct Requestor and Reviewer identities are validated.
- GG-SAD operates stand-alone and with optional companion mappings.
- At least three real projects complete pilot changes before version 1.0.
- The method remains materially lighter than heavyweight role- and document-driven workflows.

## Project Type and Lifecycle Context

- Project Type: greenfield
- Repository Type: single-repository
- Delivery Context: open-source product and reference implementation
- Current Maturity: pre-alpha implementation
- Intended Maturity: stable, portable reference implementation

## Scope

### Included

- normative GG-SAD method assets;
- human-readable guides and templates;
- project and change artifact schemas;
- compliance-profile and workflow-tailoring resolution;
- state and transition management;
- document and reference validation;
- DoR, DoD, DoW, and DoF evaluation;
- evidence and traceability;
- Pair Review policy, cycles, findings, and gate integration;
- phase-specific agent workflows;
- optional CI and companion-method adapters;
- portable project memory after core workflow validation;
- examples for lean, standard, governed, and regulated contexts.

### Excluded / Non-Goals

- mandatory sprint, epic, story-point, or ceremony management;
- general-purpose project-management replacement;
- mandatory multi-agent orchestration;
- autonomous architecture approval;
- mandatory issue-tracker or repository-host synchronization;
- mandatory database, web application, MCP server, or semantic index;
- unrestricted workflow DSL capable of bypassing GG-SAD invariants;
- legal or regulatory compliance certification;
- replacing ADRs with a project memory;
- making GSD, OpenSpec, Spec Kit, BMAD, Claude Code, or another external tool normative.

## Constraints

- Time: Deliver in small vertical slices; avoid speculative platform work.
- Budget: Prefer open-source, local, and low-maintenance components.
- Technology: Python, Markdown, YAML, JSON Schema, and Git-portable artifacts.
- Delivery: CLI first; integrations remain optional.
- Security: Least privilege, no secrets in artifacts, explicit approval for destructive actions.
- Data Privacy: Minimize stored personal and sensitive data; sanitize evidence.
- Operations: Stand-alone operation must remain possible.
- Compatibility: Support Python 3.12 and newer during the initial implementation.
- Maintainability: Components and dependencies require a clear consumer and owner.

## Compliance Profile

- Active Profile: standard
- Profile Rationale: The repository requires defined quality gates, recorded evidence, practical
  independent review, and controlled releases without regulated-process overhead.
- Required External Controls: None at bootstrap.
- Future Validation: Governed and regulated example projects will test stronger profiles.

## GG-SAD Operating Mode

- Mode: combination

GG-SAD is the governing method for this repository. It owns goals, specification authority,
state, gates, precedence, approvals, evidence requirements, and closure.

## Integrated Methods, Frameworks, Tools, and Agents

| Integration | Version | Purpose | GG-SAD Mapping | Source of Truth |
|---|---|---|---|---|
| GSD Core | project-pinned current version | Execution planning and context engineering | `.ggsad/mappings/gsd.yaml` | GG-SAD for governance; GSD for subordinate execution artifacts |
| Claude Code | project-approved current version | Primary implementation runtime | `CLAUDE.md` | GG-SAD artifacts |
| Codex or Human Reviewer | project-assigned | Independent Pair Review | active change evidence or review record | GG-SAD review record |
| Git | current supported version | Version control and history | repository conventions | repository |
| GitHub Actions | optional | CI validation examples | future CI adapter | GG-SAD criteria and repository results |

## Enabled Practices and Combination Recipes

| Practice or Recipe | Status | Scope | Required By | Configuration / Reference |
|---|---|---|---|---|
| Example-Driven Specification | enabled | all behavioral requirements | GG-SAD core | normative method |
| Pair Review | conditional | architecture, engine, security, release, and higher-risk changes | profile, risk, project policy | `.ggsad/config.yaml` |
| GSD Execution Companion | enabled | planning and implementation context | project operating mode | `.ggsad/mappings/gsd.yaml` |
| Property-Based Testing | planned | state transitions and profile resolution | risk and component type | future practice profile |
| Threat Modeling | planned | security-relevant components | risk | future practice profile |

## Pair Review Policy

- Default Requirement: optional
- Activation Basis: compliance profile, project scope, change class, risk, artifact type, and
  local specification
- Required Initially For:
  - constitutional changes;
  - architecture and ADR changes;
  - state and transition engine changes;
  - gate engine changes;
  - profile-resolution changes;
  - security-relevant changes;
  - release candidates.
- Allowed Participant Types: human, agent, external-review-service
- Human–Human Allowed: yes
- Distinct Requestor and Reviewer Required: yes
- Separate Human Approval Required: conditional
- Separate `review.md`: conditional
- Blocking Finding Resolution Rule: Blocking findings must be resolved and verified, withdrawn,
  or formally dispositioned by an authorized decision owner before the applicable gate passes.

## Product and Delivery Assumptions

- Repository-based Markdown, YAML, and schemas provide sufficient transparency for the initial
  implementation.
- A CLI provides enough value before a web UI or IDE plugin.
- Manual pilots will reveal which workflow sections and automation are actually necessary.
- GSD can support implementation context without becoming a second source of governance truth.
- File-based state and later file-based memory can remain portable until usage proves the need for
  another backend.
- A single implementation agent with phase-specific workflows is safer and simpler than an
  initial agent swarm.

## Key Risks

| Risk | Impact | Mitigation | Owner |
|---|---|---|---|
| Method is over-automated before real pilots | high | Deliver manual repository and small vertical slices first | Maintainer |
| GG-SAD and GSD create duplicate sources of truth | high | Enforce mapping and precedence rules | Maintainer |
| Profiles silently weaken invariants | high | Deterministic resolver and invariant validation | Maintainer |
| Artifact volume creates excessive overhead | high | Apply anti-overhead rules and pilot measurements | Maintainer |
| Agents claim completion without evidence | high | Gate and evidence validation | Maintainer |
| Reviewer independence is simulated rather than real | medium | Validate participant identity and assignment | Maintainer |
| Tool coupling reduces portability | high | Keep adapters outside Method Core | Maintainer |
| Compliance claims exceed actual controls | high | State limitations and avoid certification claims | Maintainer |
| Schema or CLI contracts change too early | medium | Pre-1.0 versioning and migration policy | Maintainer |
| Maintainer capacity becomes a bottleneck | medium | Small scope, clear contribution rules, reusable checks | Maintainer |

## Open Decisions

- Final open-source license and copyright holder.
- Initial repository hosting organization and package publication namespace.
- Exact policy for supported Python versions after the bootstrap.
- Initial configuration and state schema versioning policy.
- Whether mypy remains the sole type checker or a later profile adds another checker.
- First stable mechanism for human approval identity.
- Timing and scope of project-memory implementation.
- Admission criteria for MCP and IDE integrations.
- Branching and delivery model; Trunk-Based Development, GitFlow, and Continuous Delivery remain
  open method topics.

## Related Governing Artifacts

- Constitution: `docs/constitution.md`
- Architecture: `docs/architecture.md`
- Roadmap: `docs/roadmap.md`
- Definitions: `docs/definitions/`
- ADRs: `docs/adr/`
- GG-SAD Configuration: `.ggsad/config.yaml`
- General Agent Rules: `AGENTS.md`
- Claude Code Rules: `CLAUDE.md`
