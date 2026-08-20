# GG-SAD Implementation Roadmap

## Roadmap Principles

- Deliver the smallest coherent method first.
- Validate manually before automating.
- Add components only when repeated usage proves their value.
- Keep the method independent from specific tools and agents.
- Treat integrations and companion methods as optional adapters.
- Preserve equally valid stand-alone and combination operating modes.
- Tailor workflow depth to compliance needs without weakening the invariant core.
- Keep project memory subordinate to governing documents and explicit provenance.
- Prefer vertical slices that produce a usable result.
- Treat Example-Driven Specification as a method baseline.
- Resolve Pair Review from compliance, project scope, change class, risk, and project policy rather than requiring it universally.
- Support Human–Human and mixed human/agent review while preserving distinct participant identities.

---

## Phase 0 — Method Baseline

### Goal

Create a stable, reviewable baseline of GG-SAD.

### Deliverables

- normative method specification,
- human-readable guide,
- implementation guide,
- architecture document,
- roadmap,
- document hierarchy including `project-brief.md`,
- stand-alone and combination-mode rules,
- compliance-profile and workflow-tailoring model,
- state model,
- gate definitions,
- minimal templates,
- Example-Driven Specification rules and traceability,
- Pair Review definition, optionality rules, participant independence, findings lifecycle, and Human–Human support.

### Exit Criteria

- terminology is consistent,
- document precedence is explicit,
- DoR, DoD, DoW, and DoF are distinguishable,
- Class S, M, and L changes are defined,
- anti-overhead rules are accepted,
- invariant core and tailorable dimensions are explicit,
- default compliance profiles are defined,
- project brief purpose and precedence are agreed,
- Decisions are clearly distinguished from ADRs.

---

## Phase 1 — Reference Repository

### Goal

Create a manually usable GG-SAD reference repository.

### Deliverables

- `.ggsad/` structure,
- project-wide document templates including `project-brief.md`,
- default compliance profiles: lean, standard, governed, regulated,
- stand-alone and companion-method mapping examples,
- gate-definition templates,
- change templates,
- sample `state.yaml`,
- one example each for Class S, M, and L,
- a Pre-PMF startup MVP example using the lean profile,
- a solo-developer fast-iteration example,
- a governed or regulated enterprise example,
- contribution and usage instructions,
- Example-Driven specification examples,
- Pair Review examples for Human–Human, Human–Agent, Agent–Human, Agent–Agent, and external review services,
- conditional `review.md` template and inline evidence example.

### Exit Criteria

- a new project can copy the repository structure,
- a user can execute a complete flow manually,
- examples demonstrate wait and fail behavior,
- no CLI or agent dependency is required.

---

## Phase 2 — Pilot Validation

### Goal

Test GG-SAD against real work before building automation.

### Pilot Set

1. A small, low-risk patch.
2. A standard behavior change.
3. A high-risk or architecture-relevant change.
4. A Pre-PMF startup MVP using the lean profile.
5. A solo-developer fast-iteration flow.
6. A combination-mode pilot with one external framework or tool.
7. An optional Pair Review pilot for a low-risk change.
8. A required Pair Review pilot for a governed or regulated change.
9. A Human–Human Pair Review pilot and at least two mixed participant combinations.
10. A pilot using concrete acceptance examples with requirement-to-example-to-evidence traceability.

### Measurements

- documents actually used,
- sections repeatedly left empty,
- clarification cycles,
- wait events,
- fail events,
- gate ambiguity,
- duplicated evidence,
- time spent on method overhead,
- agent mistakes prevented by gates,
- profile-selection accuracy,
- profile-specific artifact and approval overhead,
- stand-alone versus combination-mode friction,
- mapping conflicts with external artifacts,
- memory candidates discovered during delivery.

### Exit Criteria

- at least three changes complete,
- unnecessary sections are removed or made optional,
- ambiguous gates are revised,
- mandatory artifacts are justified by observed use,
- lean mode remains materially faster than governed mode,
- all profiles preserve the invariant core,
- at least one combination-mode mapping is validated.

---

## Phase 3 — Validator and State Engine

### Goal

Automate structural checks and controlled transitions.

### Deliverables

- Python package skeleton,
- Pydantic models,
- JSON schemas for state, project brief, profiles, and mappings,
- compliance-profile resolver,
- integration-mapping registry,
- YAML loader and writer,
- state transition engine,
- document validator,
- gate-result model,
- history logging,
- unit tests,
- acceptance-example parser and traceability model,
- Pair Review cycle and finding schemas,
- distinct-participant validation.

### Initial Commands

```text
ggsad init
ggsad profile
ggsad map
ggsad new
ggsad status
ggsad validate
ggsad transition
```

### Exit Criteria

- invalid states are rejected,
- invalid transitions are rejected,
- state history is recorded,
- required artifacts are validated by class and compliance profile,
- profile inheritance and overrides are explainable,
- stand-alone mode has no integration dependency,
- invalid or incomplete mapping contracts are rejected,
- schema and structure errors are explainable.

---


## Phase 4 — Workflow Tailoring and Companion Methods

### Goal

Make GG-SAD practical from lean solo work to regulated enterprise delivery and usable both stand-alone and with other methods or tools.

### Deliverables

- invariant-core validator,
- default `lean`, `standard`, `governed`, and `regulated` profiles,
- custom-profile inheritance and validation,
- effective-workflow report,
- mapping-contract schema and registry,
- stand-alone adapter,
- initial combination guides and mappings for GSD, OpenSpec, Spec Kit, BMAD, Hermes, and Kiro,
- project-brief profile and integration sections,
- practice-profile schema and registry,
- Combination Recipe schema and validated reference recipes,
- compatibility and conflict rules for enabled practices,
- Testing Strategy Profiles for Property-Based, Mutation, Risk-Based, and Exploratory Testing,
- combined Architecture Practice Profiles package for Feature-Sliced Design, Service-Layer Architecture, and Event-Driven Architecture,
- Security Practice Profile for Threat Modeling,
- Discovery and Product Practice Profiles for Design Thinking and Jobs to Be Done,

### Commands

```text
ggsad profile list
ggsad profile show
ggsad profile resolve
ggsad profile validate
ggsad map add
ggsad map validate
ggsad map show
```

### Exit Criteria

- lean profile supports Pre-PMF MVP and solo fast-iteration use without unnecessary documents,
- regulated profile supports formal approvals, evidence retention, and segregation of duties,
- every profile preserves the invariant core,
- GG-SAD completes a full flow with no external framework,
- at least three companion mappings complete a full flow without bypassing GG-SAD gates.

## Phase 5 — Gate Engine

### Goal

Evaluate automatic, review, and approval criteria consistently.

### Deliverables

- criterion parser,
- automatic check interface,
- review result recording,
- approval result recording,
- DoF/DoW/DoD/DoR evaluation order,
- wait-state creation,
- failure-state creation,
- resume logic,
- gate reports,
- Pair Review requirement resolution,
- review-cycle state and finding lifecycle,
- distinct Requestor/Reviewer validation including Human–Human,
- blocking-finding gate integration,
- separation of agent review and human approval,

### Additional Commands

```text
ggsad evaluate
ggsad wait
ggsad resume
ggsad fail
ggsad close
```

### Exit Criteria

- wait and fail produce distinct state and output,
- automatic checks are reproducible,
- human approvals cannot be self-issued by agents,
- gate failures list criterion-level reasons.

---

## Phase 6 — Evidence and Traceability

### Goal

Connect goals and requirements to verifiable outcomes without duplicating reports.

### Deliverables

- requirement parser,
- evidence reference model,
- requirement-to-evidence validation,
- quality-gate evidence,
- deviation records,
- final close evaluation,
- requirement-to-acceptance-example-to-evidence mapping,
- Pair Review evidence and finding-disposition references,
- optional inline review evidence and conditional `review.md`,

### Exit Criteria

- every required requirement has evidence,
- missing evidence blocks close,
- deviations are explicit,
- external test reports can be referenced rather than copied.

---

## Phase 7 — Agent Workflows

### Goal

Enable controlled AI-agent execution through the existing engine.

### Deliverables

- `/ggsad.intake`,
- `/ggsad.specify`,
- `/ggsad.plan`,
- `/ggsad.build`,
- `/ggsad.verify`,
- `/ggsad.close`,
- `/ggsad.status`,
- `/ggsad.resume`,
- `/ggsad.review`,
- `/ggsad.findings`,
- Requestor and Reviewer permission profiles,
- review-only execution mode,
- support for Human–Human and human/agent/agent combinations,
- phase-specific permission profiles,
- context-loading rules,
- output contracts.

### Exit Criteria

- one agent can execute all phases using different commands,
- the agent cannot bypass gate checks,
- the agent cannot write outside phase permissions,
- specification changes during build require explicit workflow handling,
- wait and failure outputs are actionable.

---

## Phase 8 — CI Integration

### Goal

Provide repository checks without coupling GG-SAD to one hosting platform.

### Deliverables

- generic CLI exit codes,
- machine-readable validation reports,
- example GitHub Actions workflow,
- example GitLab CI workflow,
- pull-request validation profile,
- release validation profile.

### Exit Criteria

- CI can block invalid changes,
- CI output identifies the failed GG-SAD criteria,
- the core remains usable without CI,
- repository-platform adapters remain optional.

---

## Phase 9 — Optional Integrations

### Goal

Add integrations only where demand is demonstrated.

### Candidates

- GitHub Issues and Pull Requests,
- GitLab Issues and Merge Requests,
- Linear,
- Jira,
- VS Code commands,
- JetBrains integration,
- release tooling,
- MCP server,
- dashboard or web UI.

### Admission Criteria for an Integration

An integration should be accepted only when:

- a repeated manual workflow exists,
- the integration has a clear owner,
- permission boundaries are defined,
- failure behavior is defined,
- the integration does not alter method semantics,
- maintenance cost is justified.

---


## Phase 10 — GG-SAD Project Memory

### Goal

Provide durable, governed project memory without replacing the document hierarchy or ADR process.

### Deliverables

- memory record schema and API,
- record types for Decisions, Learnings, Failures, Definitions, and External Sources,
- explicit ADR-versus-Decision classifier and validation,
- provenance, trust, status, scope, and lifecycle metadata,
- CLI commands for add, search, show, supersede, correct, export, and delete,
- retrieval filters by project, change, phase, profile, and permissions,
- pluggable memory backend interface,
- initial local file or embedded backend,
- optional MCP exposure,
- backup, migration, retention, redaction, and audit policies,
- context-loading integration for agent workflows.

### Commands

```text
ggsad memory add
ggsad memory search
ggsad memory show
ggsad memory supersede
ggsad memory export
ggsad memory validate
```

### Exit Criteria

- architecture decisions cannot be stored as ordinary Decisions,
- every record has stable identity and provenance,
- memory retrieval respects permissions and compliance profiles,
- governing documents always override memory,
- failures and learnings can be reused across changes,
- external sources retain retrieval date and trust metadata,
- memory can be exported and migrated without lock-in.

## Open Topics

The following topics are intentionally unresolved and MUST NOT be treated as committed implementation scope until their method and state-model implications are decided:

### Dual-Track Development

Open questions include parallel Discovery and Delivery state, handover gates, ownership, evidence synchronization, and prevention of unvalidated discovery assumptions entering delivery.

### Delivery Models

Trunk-Based Development, GitFlow, and Continuous Delivery remain open topics. Required decisions include branching-model compatibility, merge and release gates, feature-flag expectations, release evidence, rollback semantics, and CI/repository coupling.

## Deferred by Default

The following components are intentionally deferred:

- multi-agent orchestration,
- automatic sub-agent delegation,
- workflow hooks for every phase,
- a mandatory centralized database-backed state or memory,
- web application,
- mandatory issue synchronization,
- an unrestricted custom workflow DSL that can bypass invariants,
- sprint and epic management,
- analytics platform,
- autonomous architecture approval.

---

## Suggested Release Milestones

### v0.1 — Method Baseline and Review Semantics

- documents including project brief,
- templates,
- stand-alone and combination semantics,
- compliance-profile model,
- manual examples,
- Example-Driven Specification baseline,
- Pair Review semantics and optionality.

### v0.2 — Validation, Tailoring, and Practice Core

- schemas,
- validator,
- state transitions,
- profile resolver,
- mapping-contract validation,
- practice-profile and Combination Recipe schemas,
- Pair Review identity and finding validation.

### v0.3 — Tailored Goal Gates

- DoR, DoD, DoW, DoF engine,
- wait and fail handling.

### v0.4 — Evidence, Review, and Compliance Profiles

- requirement traceability,
- close evaluation,
- example traceability,
- Pair Review evidence and blocking-finding handling.

### v0.5 — Agent Workflows

- phase commands,
- permissions,
- agent adapters.

### v0.6 — CI and Companion Profiles

- generic CI output,
- example hosting-platform workflows.

### v0.7 — Project Memory

- memory taxonomy and storage API,
- Decisions, Learnings, Failures, Definitions, and External Sources,
- provenance and retrieval controls,
- export and migration.

### v1.0 — Stable Reference Implementation

- proven on multiple real projects,
- versioned method specification,
- migration guidance,
- stable configuration and schema contracts,
- documented extension model.

---

## Definition of Ready for v1.0

- method baseline has been stable across at least two minor releases,
- at least three real projects have completed pilot changes,
- state and config schemas are versioned,
- breaking schema changes have a migration process,
- core commands are documented and tested,
- security and permission boundaries are reviewed,
- no mandatory dependency on a specific agent or platform exists,
- stand-alone and combination modes are proven,
- lean, standard, governed, and regulated profiles are validated,
- memory governance and ADR separation are reviewed,
- Example-Driven Specification and Pair Review semantics are stable,
- optional and required Pair Review profiles are validated,
- Human–Human and mixed participant combinations are proven.

## Definition of Done for v1.0

- Class S, M, and L changes are supported,
- all four gate types are operational,
- wait and fail are reliably differentiated,
- evidence completeness can block closure,
- CI integration is optional and functional,
- agent workflows respect phase permissions,
- documentation and examples are complete,
- upgrade and rollback guidance exists,
- `project-brief.md` is supported and validated,
- workflow tailoring is deterministic and explainable,
- Pre-PMF MVP and solo fast-iteration flows meet overhead targets,
- regulated profile produces audit-ready evidence,
- project memory is portable and subordinate to governing documents,
- concrete acceptance examples are traceable to requirements and evidence,
- Pair Review is deterministically optional or required by effective profile, scope, class, risk, and policy,
- Requestor and Reviewer independence is enforced, including Human–Human workflows.
