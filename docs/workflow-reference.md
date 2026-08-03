# Standard Product, Development, and Open Source Workflow

**Document:** `WORKFLOW.md`  
**Language:** English  
**Method baseline:** GG-SAD v1.2  
**Scope:** Integrated product lifecycle, software development lifecycle, and open source software lifecycle

---

## 1. Purpose

This document defines a practical end-to-end workflow from initial ideation to release, operation, evolution, and retirement.

It combines:

- the **standard product lifecycle** for discovering, validating, delivering, operating, and evolving a product;
- the **GG-SAD development lifecycle** for specification-anchored and gate-controlled implementation;
- the **open source software lifecycle** for governance, licensing, community participation, contribution management, public releases, maintenance, and project sustainability.

The workflow is intended as a standard reference. Projects MAY tailor phases, artifacts, approvals, evidence depth, and automation according to their active compliance profile. GG-SAD gates and invariants MUST NOT be bypassed.

---

## 2. Integrated Lifecycle Overview

```text
IDEATION
  ↓
DISCOVERY
  ↓
OPPORTUNITY VALIDATION
  ↓
PRODUCT STRATEGY
  ↓
PRODUCT DEFINITION
  ↓
OSS FOUNDATION
  ↓
INTAKE
  ↓
EXPLORE / DECIDE (when needed)
  ↓
SPECIFY
  ↓
PLAN
  ↓
DESIGN & ARCHITECTURE
  ↓
BUILD
  ↓
VERIFY
  ↓
RELEASE READINESS
  ↓
RELEASE & PUBLICATION
  ↓
ADOPTION & ENABLEMENT
  ↓
OPERATE & SUPPORT
  ↓
MEASURE & LEARN
  ↓
MAINTAIN & EVOLVE
  ↓
DEPRECATE / RETIRE / ARCHIVE
```

The phases do not always form a strict one-way sequence. Learning, incidents, market changes, community feedback, architectural discoveries, or security findings MAY return the workflow to an earlier phase.

---

## 3. Lifecycle Principles

- Every initiative or change MUST have a clear **goal**, expected benefit, accountable owner, and defined scope.
- The approved **specification** is the anchor for planning, implementation, verification, and acceptance.
- Existing project rules, accepted architecture decisions, and applicable policies take precedence over implementation convenience.
- Phase transitions MUST be controlled through:
  - **Definition of Ready (DoR):** May the next phase begin?
  - **Definition of Done (DoD):** Has the current phase completed successfully?
  - **Definition of Wait (DoW):** Must work pause in a safe and controlled state?
  - **Definition of Fail (DoF):** Must the workflow terminate unsuccessfully?
- Gate evaluation order MUST be:
  1. DoF
  2. DoW
  3. Current-phase DoD
  4. Next-phase DoR
- Exploration MUST NOT silently transition into production implementation.
- Product, engineering, operational, security, legal, compliance, and community concerns SHOULD be considered early rather than deferred to release.
- OSS work MUST define governance, licensing, contribution rules, security reporting, and maintainer responsibilities before broad public participation is invited.
- Evidence depth, approval requirements, documentation, and automation SHOULD be tailored to the project context and compliance profile.
- Behavioral requirements MUST use concrete acceptance examples or a justified alternative verifiable acceptance condition.
- Pair Review MAY be enabled or required according to the compliance profile, project scope, change class, risk, affected artifact, and project policy.
- When Pair Review is used, Requestor and Reviewer MUST be distinct participants. Human–Human, Human–Agent, Agent–Human, Agent–Agent, and external review-service combinations are permitted.
- Pair Review findings MUST return to the Requestor; the Reviewer MUST NOT silently modify the governed work product during the review cycle.


---

# 4. Product Discovery and Definition

## Phase 1 — Ideation

**Purpose:** Generate and capture potentially valuable product, technical, operational, or community ideas.

**Key criteria and characteristics:**

- Describe the idea, observed problem, or opportunity in plain language.
- Identify the potential users, stakeholders, maintainers, or affected communities.
- State the expected value, benefit, or improvement.
- Record the origin of the idea and relevant context.
- Capture early assumptions without presenting them as facts.
- Identify whether the idea is:
  - a new product;
  - a product capability;
  - a technical improvement;
  - an operational improvement;
  - an OSS initiative;
  - an experiment or research question.
- Avoid detailed solution design before the problem is understood.
- Reject, merge, defer, or promote ideas transparently.

**Typical outputs:**

- Idea statement
- Initial problem hypothesis
- Initial target audience
- Assumptions and unknowns
- Preliminary value hypothesis

**Exit criteria:**

- The idea is understandable enough to justify discovery work.
- A sponsor, owner, or decision-maker is identified.
- No immediate constitutional, ethical, legal, or strategic conflict is visible.

---

## Phase 2 — Discovery

**Purpose:** Understand the problem space, users, alternatives, constraints, and current system context.

**Key criteria and characteristics:**

- Research user needs, workflows, pain points, and desired outcomes.
- Analyze existing products, competitors, standards, libraries, and internal capabilities.
- Review relevant project documents, architecture, accepted decisions, roadmap, and known limitations.
- Identify legal, privacy, security, accessibility, compliance, and operational constraints.
- Determine whether the problem is real, recurring, material, and sufficiently understood.
- Separate verified facts from assumptions and opinions.
- Record external sources and their provenance.
- Identify affected user groups and potential unintended consequences.
- For brownfield work, document the relevant current state and dependencies.
- For OSS initiatives, inspect ecosystem expectations, competing projects, community gaps, and likely contributor profiles.

**Typical outputs:**

- Discovery notes
- User or stakeholder findings
- Current-state analysis
- Ecosystem and alternative analysis
- Constraint inventory
- Evidence-backed problem statement

**Exit criteria:**

- The problem and its context are sufficiently understood.
- Important assumptions are visible and testable.
- Major constraints and affected areas are known.
- The team can formulate a concrete opportunity hypothesis.

---

## Phase 3 — Opportunity Validation

**Purpose:** Determine whether the opportunity is desirable, viable, feasible, and responsible enough to pursue.

**Key criteria and characteristics:**

- Validate that the target problem matters to intended users or stakeholders.
- Estimate potential impact, reach, urgency, and strategic relevance.
- Test major assumptions through interviews, prototypes, experiments, data, or technical spikes.
- Assess technical feasibility and major architecture implications.
- Assess business, funding, staffing, operational, and maintenance viability.
- Evaluate security, privacy, legal, licensing, compliance, and reputational risks.
- Define measurable success signals and invalidation criteria.
- Compare the opportunity against alternatives, including doing nothing.
- For OSS products, validate whether an open source model serves the product and community goals.
- Identify the likely sustainability model, such as internal sponsorship, services, donations, dual licensing, or commercial extensions.

**Typical outputs:**

- Validated problem statement
- Opportunity assessment
- Experiment or prototype evidence
- Risk summary
- Initial success metrics
- Go, revise, wait, or stop decision

**Exit criteria:**

- Evidence supports continued investment.
- Critical feasibility questions have acceptable answers.
- The opportunity has a named owner and decision.
- Success and failure signals are defined.

---

## Phase 4 — Product Strategy

**Purpose:** Define why the product or initiative should exist and how it will create sustainable value.

**Key criteria and characteristics:**

- Define the product vision and intended long-term outcome.
- Identify primary users, customers, operators, contributors, and beneficiaries.
- Define the value proposition and strategic differentiators.
- Establish product principles and non-negotiable constraints.
- Select an appropriate product maturity target, such as prototype, MVP, production service, platform, or public OSS project.
- Define high-level success metrics and guardrail metrics.
- Establish build, buy, integrate, partner, or reuse decisions where applicable.
- Clarify ownership, funding, staffing, and operating assumptions.
- Define the intended open source role:
  - fully open source product;
  - open core;
  - source-available component;
  - internal product using OSS dependencies;
  - community-led project.
- Ensure the strategy is consistent with the constitution and accepted architecture decisions.

**Typical outputs:**

- Product vision
- Value proposition
- Strategic goals and non-goals
- Product principles
- Success and guardrail metrics
- Initial lifecycle and sustainability model

**Exit criteria:**

- Strategic intent and target users are clear.
- Product value and differentiation are understandable.
- Ownership and investment boundaries are accepted.
- The strategy provides enough direction for product definition.

---

## Phase 5 — Product Definition

**Purpose:** Translate strategy into a bounded product concept and durable project context.

**Key criteria and characteristics:**

- Define target users, core use cases, product boundaries, and expected outcomes.
- Describe the product type, lifecycle context, maturity level, and delivery model.
- Identify the initial scope, explicit non-goals, and future possibilities.
- Define key capabilities without prematurely decomposing them into implementation tasks.
- Record major dependencies, integrations, assumptions, and constraints.
- Establish product-level quality expectations.
- Define availability, support, security, privacy, compliance, and accessibility expectations.
- Identify product risks and unresolved decisions.
- Define the initial roadmap using concise horizons such as **Now**, **Next**, **Later**, and **Open**.
- Select the active GG-SAD compliance profile and tailoring rules.
- Ensure architecture decisions remain in ADRs rather than in the project brief.

**Typical outputs:**

- `docs/project-brief.md`
- `docs/roadmap.md`
- Updated `docs/constitution.md`, when required
- Initial product metrics
- Product-level acceptance boundaries
- Open questions and decision owners

**Exit criteria:**

- The durable project context is documented.
- Initial scope and non-goals are accepted.
- Product-level constraints and quality expectations are known.
- The project is ready to establish its OSS and delivery foundations.

---

# 5. Open Source Foundation

## Phase 6 — OSS Foundation and Governance

**Purpose:** Establish the legal, governance, repository, contribution, and community foundations required for responsible open source development.

**Key criteria and characteristics:**

- Decide whether and when the project will be publicly released.
- Select and document an appropriate license.
- Verify license compatibility for dependencies, assets, documentation, and contributed code.
- Define ownership of trademarks, branding, domains, and package names.
- Establish project governance and decision rights.
- Define maintainer roles, responsibilities, nomination, and removal processes.
- Define which decisions require maintainer consensus, a designated owner, or escalation.
- Publish a code of conduct and enforcement process.
- Define contribution requirements and review expectations.
- Define contributor licensing or developer certificate requirements when needed.
- Establish a security vulnerability reporting and disclosure process.
- Establish issue, discussion, support, and feature-request channels.
- Define versioning, compatibility, deprecation, and release policies.
- Establish repository structure, branch protections, required checks, and access controls.
- Define documentation standards and minimum public project metadata.
- Clarify the project sustainability and funding model.

**Typical outputs:**

- `LICENSE`
- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- Governance or maintainer policy
- Support policy
- Versioning and release policy
- Repository and access-control configuration

**Exit criteria:**

- Legal and licensing decisions are approved.
- Governance and maintainer responsibilities are explicit.
- Contribution and security-reporting processes exist.
- The repository can safely accept internal or public collaboration.

---

# 6. GG-SAD Development Workflow

## Phase 7 — Intake

**Purpose:** Convert an approved product need, defect, request, maintenance item, or community proposal into a traceable change candidate.

**Key criteria and characteristics:**

- Identify the requestor, sponsor, product owner, or decision owner.
- Describe the goal or problem and expected benefit.
- Classify the work, for example feature, defect, security fix, maintenance, documentation, operational change, or experiment.
- Determine the expected change size and lifecycle impact.
- Identify affected product areas, repositories, components, users, APIs, data, and operations.
- Check alignment with the project brief, constitution, roadmap, and accepted ADRs.
- Detect duplicates, overlaps, conflicts, dependencies, and prerequisite decisions.
- Identify whether the change originated internally or through an OSS issue, discussion, or pull request.
- Select the applicable workflow profile and required phases.
- Assign an accountable owner and initial priority.

**Typical outputs:**

- Intake record or issue
- Initial change classification
- Owner and decision-maker
- Initial scope and affected areas
- Selected workflow profile

**Ready-to-Spec criteria:**

- The goal or problem is described.
- The expected benefit is understandable.
- The requestor or decision owner is identified.
- Known constraints are available.
- Affected system areas are roughly known.
- No obvious conflict with the constitution exists.

---

## Phase 8 — Explore and Decide

**Purpose:** Reduce uncertainty when the problem, solution space, feasibility, or decision is not yet sufficiently clear for specification.

**Key criteria and characteristics:**

- Use this phase only when focused exploration is necessary.
- Define the question, uncertainty, or decision to resolve.
- Time-box prototypes, research, spikes, benchmarks, or experiments.
- Prevent experimental code from silently becoming production code.
- Record assumptions, observations, evidence, and limitations.
- Compare viable options and their trade-offs.
- Identify architecture decisions requiring an ADR.
- Consult product, security, operations, legal, compliance, or maintainers as needed.
- For OSS work, consider ecosystem conventions and community impact.
- End with an explicit decision: proceed, revise, defer, wait, or stop.

**Typical outputs:**

- Exploration note
- Prototype or spike
- Option analysis
- Decision record or ADR proposal
- Updated constraints and risks

**Exit criteria:**

- The defined uncertainty has been reduced sufficiently.
- Production work has not begun without approval.
- A decision and rationale are documented.
- The change can proceed to specification, wait safely, or close.

---

## Phase 9 — Specify

**Purpose:** Define the desired target state, boundaries, requirements, and verifiable acceptance conditions.

**Key criteria and characteristics:**

- Define the goal, expected benefit, and success signals.
- Describe the relevant current state.
- Define scope and explicit non-goals.
- Write clear, unambiguous, and verifiable requirements.
- Add at least one concrete acceptance example for every behavioral requirement, or document a justified alternative verifiable acceptance condition.
- Include normal, negative, failure, and boundary examples according to risk.
- Link examples to requirement IDs and planned verification evidence.
- Identify affected users, interfaces, data, components, and operational behavior.
- Document product, technical, security, privacy, legal, licensing, compliance, and accessibility constraints.
- Define compatibility and migration expectations.
- Mark potential breaking changes explicitly.
- Review applicable architecture documentation and ADRs.
- Resolve contradictions or return conflicting requirements to the requestor.
- Identify open questions and their owners.
- For OSS-facing changes, define user, contributor, maintainer, documentation, and ecosystem impact.

**Typical outputs:**

- `spec.md`
- Acceptance conditions or examples
- Updated issue or change record
- Decision or ADR references
- Initial evidence requirements

**Spec-Done criteria:**

- Goal, benefit, and success signals are described.
- Scope and non-goals are defined.
- Requirements are unambiguous and verifiable.
- Acceptance examples or acceptance conditions exist.
- Constraints are documented.
- Open questions are closed or explicitly accepted.
- ADR conflicts are resolved or returned to the requestor.
- The specification is approved.

---

## Phase 10 — Plan

**Purpose:** Define a safe, feasible, and reviewable technical delivery approach.

**Key criteria and characteristics:**

- Describe the technical approach and implementation sequence.
- Identify affected components, repositories, modules, APIs, schemas, data flows, and infrastructure.
- Assess architecture, security, privacy, compliance, accessibility, performance, and operational impacts.
- Determine whether new or changed ADRs are required.
- Define the test and verification strategy.
- Define migration, rollout, feature-flag, compatibility, and rollback needs.
- Identify dependencies, prerequisites, external services, tools, and permissions.
- Assess delivery and operational risks.
- Define documentation, release-note, and user-communication needs.
- Decompose implementation into manageable tasks when useful.
- Avoid turning the task list into the primary source of truth.
- For OSS changes, identify contributor coordination, maintainer review, downstream compatibility, and public communication needs.

**Typical outputs:**

- `plan.md`
- `tasks.md`, when useful
- Risk and dependency summary
- Test strategy
- Migration and rollback approach
- ADR proposals or references

**Plan-Done criteria:**

- The technical approach is described.
- Affected components are identified.
- Architecture, data, API, and operational impacts are assessed.
- The test strategy is defined.
- Migration and rollback needs are clarified.
- Risks and decisions are documented.
- Implementation is decomposed appropriately.

---

## Phase 11 — Design and Architecture

**Purpose:** Refine the solution structure and user experience before or during implementation where material design work is required.

**Key criteria and characteristics:**

- Apply this phase explicitly for changes with significant architecture, interaction, data, API, security, or operational design impact.
- Define system boundaries, responsibilities, interfaces, and dependency direction.
- Define user flows, interaction states, failure behavior, and accessibility needs.
- Define API contracts, events, schemas, persistence, and migration design.
- Define security boundaries, trust assumptions, permissions, and threat mitigations.
- Define observability, supportability, capacity, reliability, and recovery behavior.
- Evaluate build-versus-reuse choices and external dependency risks.
- Record durable architecture decisions in ADRs.
- Keep `docs/architecture.md` aligned with the current structural state.
- Review public API stability and extension points for OSS consumers and contributors.
- Ensure the design remains consistent with the approved specification.

**Typical outputs:**

- Updated `docs/architecture.md`
- ADRs
- UX or interaction design
- API or data contracts
- Threat model or security design
- Operational design

**Exit criteria:**

- Material design decisions are explicit and reviewed.
- Blocking architecture decisions are resolved.
- Interfaces and responsibilities are sufficiently clear for implementation.
- The design satisfies the approved specification and project rules.

---

## Phase 12 — Build

**Purpose:** Implement the approved specification and plan without introducing uncontrolled scope.

**Key criteria and characteristics:**

- Implement only approved requirements and explicitly accepted adjustments.
- Follow architecture principles, coding standards, repository rules, and ADRs.
- Add or update automated tests alongside implementation.
- Maintain small, reviewable, and traceable changes.
- Use secure dependency and secret-management practices.
- Update relevant code, configuration, schemas, infrastructure, documentation, and examples.
- Run local formatting, linting, type checking, tests, and analysis.
- Document deviations from the specification or plan.
- Stop and re-plan when material assumptions prove incorrect.
- Preserve a safe working state when entering a wait condition.
- For OSS development, follow contribution, sign-off, authorship, attribution, and review rules.
- Avoid merging contributor changes without required maintainer review and automated checks.

**Typical outputs:**

- Implementation changes
- Automated tests
- Updated documentation
- Migration scripts
- Configuration changes
- Pull request or equivalent review unit

**Build-Done criteria:**

- All approved changes are implemented.
- No unintended scope has been introduced.
- Tests have been added or updated.
- Local quality gates have succeeded.
- Required documentation is updated.
- Deviations from the specification are explained and approved.

---

## Phase 13 — Verify

**Purpose:** Demonstrate with evidence that the implementation satisfies the specification and applicable quality expectations.

**Key criteria and characteristics:**

- Verify every acceptance condition.
- Run required unit, integration, system, end-to-end, regression, and compatibility tests.
- Test negative, failure, recovery, permission, and boundary cases.
- Validate security, privacy, licensing, compliance, accessibility, performance, and reliability requirements as applicable.
- Review implementation against the specification, plan, architecture, and ADRs.
- Confirm migrations, rollback procedures, and operational readiness.
- Validate documentation, examples, upgrade instructions, and public API behavior.
- Capture reproducible evidence rather than relying on unsupported statements.
- Triage defects and distinguish release blockers from accepted limitations.
- For OSS changes, verify clean-room buildability, contributor setup, supported platforms, package metadata, and downstream compatibility where relevant.
- Resolve whether Pair Review is required from the effective profile, project scope, change class, risk, and policy.
- When Pair Review is used, identify distinct Requestor and Reviewer participants; Human–Human and mixed human/agent combinations are valid.
- Record review scope, criteria, findings, dispositions, and final result.
- Return findings to the Requestor and prevent unresolved blocking findings from passing the applicable gate.
- Do not treat Pair Review as a substitute for required human approval.

**Typical outputs:**

- `evidence.md`
- Test and analysis results
- Pair Review record or inline review evidence, when applicable
- Review findings
- Security or compliance evidence
- Accepted limitations
- Release candidate

**Verify-Done criteria:**

- All acceptance conditions have been verified.
- Required automated tests have succeeded.
- Relevant negative and failure cases have been checked.
- Regression tests have succeeded.
- Evidence is complete.
- Remaining limitations are documented.

---

# 7. Release and Publication

## Phase 14 — Release Readiness

**Purpose:** Confirm that the change or product increment can be deployed or published safely.

**Key criteria and characteristics:**

- Confirm that build and verification gates have passed.
- Confirm that security and quality gates are satisfied.
- Review unresolved defects, risks, deviations, and limitations.
- Confirm migration, rollout, rollback, backup, and recovery procedures.
- Confirm operational ownership, support readiness, monitoring, and alerting.
- Prepare version changes, changelog entries, release notes, and upgrade guidance.
- Validate artifact integrity, provenance, signatures, checksums, and software bill of materials when required.
- Confirm legal, license, attribution, export, privacy, and compliance requirements.
- Obtain required product, engineering, security, operational, legal, or maintainer approvals.
- Define release timing, channels, audiences, and communication.
- For OSS releases, confirm package registry access, repository permissions, branch/tag protections, and maintainer availability.

**Typical outputs:**

- Release checklist
- Release candidate approval
- Release notes and changelog
- Migration and rollback instructions
- Communication plan
- Signed approvals

**Ready-to-Release criteria:**

- Build and required tests have succeeded.
- Security and quality gates are satisfied.
- Migration and rollback are clarified.
- Known limitations are documented.
- Required approvals are available.

---

## Phase 15 — Release and Publication

**Purpose:** Deploy, publish, announce, and validate the approved product increment or OSS version.

**Key criteria and characteristics:**

- Create the approved version and immutable release tag.
- Build and publish reproducible release artifacts.
- Deploy through the approved environments or distribution channels.
- Publish packages, containers, binaries, source archives, documentation, and checksums as applicable.
- Publish release notes, changelog, migration guidance, and known limitations.
- Announce the release to intended users, customers, contributors, and maintainers.
- Run post-deployment or post-publication smoke tests.
- Monitor critical health, security, error, adoption, and operational signals.
- Verify that rollback or withdrawal remains possible.
- Record release evidence and approvals.
- Update roadmap, status, supported-version information, and documentation.
- For OSS projects, ensure the public release page, package metadata, license files, source references, and contribution links are correct.

**Typical outputs:**

- Deployed or published release
- Release tag and artifacts
- Release notes and changelog
- Deployment or publication evidence
- Updated documentation and roadmap

**Release-Done criteria:**

- Deployment or publication has succeeded.
- Smoke tests have succeeded.
- Version and release notes are documented.
- Monitoring shows no critical problems.
- Rollback is possible or explicitly not required.
- Roadmap and status are updated.

---

## Phase 16 — Adoption and Enablement

**Purpose:** Help users, operators, integrators, and contributors adopt the released product successfully.

**Key criteria and characteristics:**

- Publish onboarding, installation, configuration, migration, and troubleshooting guidance.
- Provide examples, tutorials, reference documentation, and known limitations.
- Communicate compatibility, support windows, and upgrade expectations.
- Enable support, success, operations, sales, advocacy, or community teams as applicable.
- Track onboarding friction and early adoption failures.
- Establish feedback and support channels.
- For OSS projects, label suitable first issues and contribution opportunities.
- Provide a reproducible development setup for contributors.
- Welcome and guide new users and contributors without promising unsupported service levels.
- Correct misleading documentation or examples quickly.

**Typical outputs:**

- User and contributor onboarding material
- Tutorials and examples
- Migration guides
- FAQ and troubleshooting documentation
- Community announcements
- Initial adoption feedback

**Exit criteria:**

- Intended users can install, access, or use the release.
- Operators and maintainers understand their responsibilities.
- Support and feedback channels are active.
- Critical adoption blockers have owners.

---

# 8. Operation, Community, and Evolution

## Phase 17 — Operate and Support

**Purpose:** Keep the product reliable, secure, usable, and supportable in real-world operation.

**Key criteria and characteristics:**

- Monitor availability, correctness, performance, capacity, security, cost, and user-impact signals.
- Respond to incidents, defects, vulnerability reports, and operational degradation.
- Maintain backups, recovery procedures, runbooks, and escalation paths.
- Triage support requests and distinguish defects, documentation gaps, feature requests, and misuse.
- Maintain supported-version and environment information.
- Patch critical issues using an appropriately shortened but still gated workflow.
- Keep dependencies, toolchains, build systems, and release infrastructure healthy.
- Track technical debt and recurring operational problems.
- For OSS projects, manage issues, discussions, pull requests, moderation, and security reports.
- Apply published service, support, disclosure, and community policies consistently.
- Protect maintainers from unsustainable response expectations and abusive behavior.

**Typical outputs:**

- Operational dashboards and alerts
- Incident and problem records
- Support and issue triage
- Security advisories and patches
- Maintenance releases
- Updated runbooks and known issues

**Exit criteria:**

- This is normally a continuous lifecycle phase.
- Individual incidents or maintenance changes close when their own GG-SAD gates are satisfied.

---

## Phase 18 — Measure and Learn

**Purpose:** Evaluate actual outcomes and feed evidence back into product, engineering, operations, and community decisions.

**Key criteria and characteristics:**

- Compare actual results with defined success and guardrail metrics.
- Measure adoption, activation, retention, reliability, performance, quality, cost, and user satisfaction as relevant.
- Analyze incidents, defects, support patterns, failed assumptions, and unexpected usage.
- Gather structured feedback from users, customers, operators, contributors, and maintainers.
- Distinguish signals from anecdotes and avoid vanity metrics.
- Record durable learnings, failures, definitions, and external sources in the project memory when available.
- Review whether product strategy, roadmap, architecture, policies, or documentation need revision.
- Assess community health, contributor experience, maintainer capacity, review latency, and issue backlog quality.
- Identify experiments, improvements, risks, and deprecation candidates.
- Feed validated findings into ideation, intake, roadmap, or strategy review.

**Typical outputs:**

- Outcome and metric review
- User and community feedback synthesis
- Incident and failure learnings
- Updated assumptions
- Improvement proposals
- Roadmap and strategy changes

**Exit criteria:**

- Meaningful findings are documented.
- Decisions and follow-up actions have owners.
- Evidence has been routed to the appropriate lifecycle phase.

---

## Phase 19 — Maintain and Evolve

**Purpose:** Sustain product value while adapting to user needs, ecosystem changes, technology changes, and accumulated learning.

**Key criteria and characteristics:**

- Prioritize defects, security work, dependencies, technical debt, usability improvements, and new capabilities.
- Balance innovation with reliability, compatibility, and maintenance capacity.
- Revisit architecture when constraints or scale materially change.
- Modernize components through explicit specifications and migration plans.
- Maintain compatibility policies and communicate breaking changes early.
- Review support windows and release branches.
- Keep documentation, examples, governance, and contribution processes current.
- Remove obsolete complexity and unsupported integrations deliberately.
- Review project sustainability, maintainer workload, funding, and bus factor.
- Grow trusted maintainers and delegate responsibilities safely.
- Use the GG-SAD intake-to-release workflow for each material change.
- Reassess product-market fit, product strategy, and OSS positioning periodically.

**Typical outputs:**

- Updated roadmap
- Maintenance and feature releases
- Architecture evolution
- Dependency and platform updates
- Governance improvements
- New contributor and maintainer capabilities

**Exit criteria:**

- This is normally a continuous phase.
- A transition to deprecation or retirement begins when continued operation no longer creates sufficient value or cannot be sustained responsibly.

---

# 9. Deprecation, Retirement, and Archive

## Phase 20 — Deprecate

**Purpose:** Announce and manage the controlled reduction or removal of support for a feature, API, version, integration, or product.

**Key criteria and characteristics:**

- Define the deprecated scope and rationale.
- Identify affected users, integrations, contributors, and downstream projects.
- Provide a migration path or explain why none exists.
- Publish timelines, support boundaries, and replacement options.
- Mark deprecated interfaces in code, documentation, schemas, and tooling.
- Avoid abrupt removal unless required by an urgent security, legal, or operational risk.
- Track adoption of replacement paths and unresolved blockers.
- Coordinate deprecation across packages, services, documentation, and release channels.
- For OSS projects, communicate through release notes, repository notices, discussions, and ecosystem channels.

**Typical outputs:**

- Deprecation notice
- Migration guide
- Support timeline
- Updated compatibility policy
- Removal plan

**Exit criteria:**

- Stakeholders have received reasonable notice.
- Migration or replacement guidance exists.
- Removal conditions and target dates are explicit.

---

## Phase 21 — Retire

**Purpose:** End active delivery, operation, or support in a controlled and reversible manner where required.

**Key criteria and characteristics:**

- Confirm the retirement decision, owner, rationale, and effective date.
- Validate contractual, legal, regulatory, privacy, retention, and security obligations.
- Notify users, customers, contributors, maintainers, and downstream dependents.
- Complete data export, migration, deletion, retention, or handover activities.
- Disable services, credentials, automation, integrations, and release pipelines safely.
- Preserve required source, artifacts, documentation, evidence, and decision history.
- Resolve ownership of domains, package names, signing keys, infrastructure, and funds.
- Decide whether the OSS project will be transferred, forked, community-maintained, made read-only, or archived.
- Publish final support and security statements.
- Confirm that no critical operational or security exposure remains.

**Typical outputs:**

- Retirement plan and approval
- User and community communication
- Data and infrastructure closure evidence
- Ownership transfer records, when applicable
- Final release or final advisory

**Exit criteria:**

- Active operation and support have ended as approved.
- Obligations and residual risks are addressed.
- Required records and artifacts are preserved.
- The project is ready for archival.

---

## Phase 22 — Archive

**Purpose:** Preserve the final project state and clearly communicate that active maintenance has ended.

**Key criteria and characteristics:**

- Mark repositories, websites, packages, and documentation as archived or unmaintained.
- Make the maintenance status visible in the README and project metadata.
- Disable or restrict issue submission, pull requests, automation, secrets, and deployment credentials as appropriate.
- Preserve source code, releases, documentation, licenses, notices, decisions, and security history.
- Retain records according to legal, compliance, contractual, and organizational policies.
- Document whether forks, successors, or alternative projects exist.
- Avoid implying ongoing support or security maintenance.
- Protect archived distribution channels from takeover or malicious replacement.
- Record final lessons and project outcomes.

**Typical outputs:**

- Archived repository or storage location
- Final maintenance-status notice
- Preserved release and decision history
- Successor or alternative references
- Final lifecycle report

**Exit criteria:**

- The archived state is durable, secure, and unambiguous.
- No active operational dependency remains without an owner.
- Users and contributors can identify the final status and available alternatives.

---

# 10. Cross-Cutting GG-SAD Practices

## Example-Driven Specification

- Every behavioral requirement has at least one concrete example or justified alternative acceptance condition.
- Example notation is flexible and tool-independent.
- Examples reference requirements and are mapped to verification evidence.
- Risk determines the required depth of normal, negative, failure, and boundary examples.

## Pair Review

- Pair Review is optional by default and may become mandatory through compliance, scope, class, risk, artifact type, or project policy.
- The Requestor creates or changes the work product.
- The Reviewer independently reviews, verifies, tests, or validates it and returns findings.
- Requestor and Reviewer are distinct participants.
- Human–Human, Human–Agent, Agent–Human, Agent–Agent, and external review-service combinations are supported.
- Reviewers do not silently modify governed work products during the review cycle.
- Blocking findings must be resolved, withdrawn, verified, or formally dispositioned before the applicable gate may pass.
- Pair Review does not replace required human approval.

# 11. Cross-Cutting OSS Activities

The following activities span multiple phases rather than occurring only once.

## Community Management

- Maintain clear and respectful communication channels.
- Enforce the code of conduct consistently.
- Welcome contributors and set realistic expectations.
- Moderate discussions, issues, and reviews.
- Recognize contributions fairly.
- Avoid maintainer overload and hidden support obligations.

## Contribution Management

- Provide reproducible setup and contribution instructions.
- Triage issues and proposals consistently.
- Label scope, priority, status, and contribution suitability.
- Require appropriate tests, documentation, and sign-off.
- Review contributions for specification, architecture, security, quality, licensing, and maintainability.
- Explain rejection, deferral, or requested changes respectfully.

## Security Management

- Provide a private vulnerability reporting channel.
- Define disclosure, embargo, remediation, and advisory procedures.
- Maintain supported-version information.
- Protect signing keys, release credentials, automation tokens, and maintainer accounts.
- Review dependencies and supply-chain risks.
- Publish advisories and patched releases responsibly.

## License and Compliance Management

- Maintain license files, copyright notices, and attribution.
- Track third-party dependencies and assets.
- Check inbound and outbound license compatibility.
- Preserve required source, notices, and offer obligations.
- Review export, privacy, accessibility, and regulatory requirements where applicable.

## Governance and Sustainability

- Keep decision rights and maintainer roles current.
- Document conflict-resolution and escalation paths.
- Review funding, infrastructure, ownership, and continuity risks.
- Develop new maintainers and reduce concentration of critical knowledge.
- Reassess project scope when capacity is insufficient.
- Prefer transparent deprecation over silent abandonment.

---

# 12. Standard Phase-Gate Questions

At the end of every phase, answer the following questions in order:

## Definition of Fail

- Has a constitutional, legal, security, licensing, compliance, or ADR violation occurred?
- Is the target state no longer achievable within approved constraints?
- Has an unapproved breaking change or unacceptable risk been introduced?
- Is the current implementation or migration state unrecoverable?

## Definition of Wait

- Is a required product, architecture, legal, security, operational, or maintainer decision missing?
- Is required information, access, dependency, approval, or external input unavailable?
- Can work pause in a documented and safe state?
- Are the resume condition, owner, and next action explicit?

## Definition of Done

- Are all required outputs complete and reviewed?
- Has the phase achieved its stated goal?
- Is evidence sufficient for the active compliance profile?
- Are deviations, risks, and remaining limitations documented and accepted?

## Definition of Ready

- Is the next phase necessary and enabled by the selected workflow?
- Are its inputs, owners, decisions, dependencies, and permissions available?
- Are relevant requirements, architecture constraints, and acceptance criteria clear?
- Is there no active DoF or DoW condition?

---

# 13. Tailoring Guidance

## Lightweight / Pre-PMF MVP

- Combine discovery, validation, and product definition where appropriate.
- Keep the project brief, specification, and acceptance conditions concise.
- Allow plan, tasks, and evidence to remain inside `spec.md` for small changes.
- Use rapid experiments, but keep exploration separate from production implementation.
- Require minimum security, licensing, rollback, and release evidence.
- Pair Review is optional unless risk, project policy, or a specific control requires it.
- Human–Human or mixed participant reviews may be used without requiring a separate review document.

## Standard Product Development

- Use the complete specification, planning, build, verification, and release flow for normal changes.
- Require practical peer review and documented quality gates.
- Maintain product metrics, roadmap, architecture, and release evidence.
- Operate a defined issue, contribution, and support workflow for OSS projects.
- Resolve Pair Review pragmatically from change size, risk, and project scope.
- Require distinct Requestor and Reviewer identities when Pair Review is activated.

## Governed / High-Impact Delivery

- Require stronger traceability, explicit approvals, independent review, and retained evidence.
- Add formal security, privacy, compliance, architecture, operational, and legal reviews.
- Apply controlled release, migration, rollback, provenance, and audit requirements.
- Restrict agent and maintainer permissions by phase and responsibility.
- Require Pair Review for selected high-impact or compliance-relevant changes.
- Permit Human–Human, Human–Agent, Agent–Human, and Agent–Agent combinations, while preserving any separate human approval requirement.

---

# 14. Common Shortened Flows

## Product Experiment

```text
IDEATION → DISCOVERY → OPPORTUNITY VALIDATION → EXPLORE → DECIDE → CLOSED
```

## Small Patch

```text
INTAKE → SPECIFY → BUILD → VERIFY → CLOSED
```

## Standard Product Change

```text
INTAKE → SPECIFY → PLAN → BUILD → VERIFY → CLOSED
```

## Release-Relevant Change

```text
INTAKE → SPECIFY → PLAN → DESIGN & ARCHITECTURE → BUILD → VERIFY → RELEASE READINESS → RELEASE → CLOSED
```

## OSS Contribution

```text
ISSUE / PROPOSAL → INTAKE → SPECIFY → PLAN (when needed) → BUILD → MAINTAINER REVIEW → VERIFY → MERGE → RELEASE
```

## Critical Security Patch

```text
PRIVATE INTAKE → SPECIFY → PLAN → BUILD → VERIFY → SECURITY APPROVAL → COORDINATED RELEASE → ADVISORY → MONITOR
```

## Deprecation and Retirement

```text
MEASURE & LEARN → DEPRECATE → MIGRATE USERS → RETIRE → ARCHIVE
```

---

# 15. Minimum Lifecycle Artifacts

## Project-Level

- `docs/constitution.md`
- `docs/project-brief.md`
- `docs/architecture.md`
- `docs/roadmap.md`
- Relevant ADRs
- Active compliance and workflow configuration

## Change-Level

- `spec.md`
- `plan.md`, when needed
- `tasks.md`, when useful
- `evidence.md`, when separate evidence is required
- Decision, wait, failure, and approval records as applicable
- Pair Review record in `evidence.md`, when required
- `review.md`, only when review complexity, retention, or compliance requires a separate artifact

## OSS-Level

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- Governance and maintainer policy
- Support and compatibility policy
- Changelog and release notes

---

# 16. Completion Definition

A product or change is not complete merely because code has been merged.

Completion requires that:

- the intended outcome has been specified and verified;
- relevant product, engineering, architecture, security, operational, legal, compliance, and OSS obligations have been satisfied;
- release or publication has succeeded when required;
- users, operators, maintainers, and contributors have the documentation they need;
- evidence and decisions are preserved;
- no active DoF or DoW condition remains;
- ownership for operation, learning, maintenance, evolution, or retirement is explicit.

