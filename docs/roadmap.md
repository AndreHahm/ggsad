# GG-SAD Implementation Roadmap

## Metadata

- Project: GG-SAD Reference Implementation
- Status: Active
- Method Baseline: GG-SAD 1.2
- Last Updated: 2026-08-04

## Roadmap Principles

- Deliver the smallest coherent method first.
- Validate manually before automating.
- Add components only when repeated usage proves their value.
- Keep the Method Core independent from tools and agents.
- Preserve stand-alone and combination operation.
- Tailor workflow depth without weakening the invariant core.
- Prefer vertical slices that produce usable results.
- Treat Example-Driven Specification as a baseline.
- Resolve Pair Review from profile, scope, class, risk, and policy.
- Keep project memory subordinate to governing documents and provenance.
- Avoid mandatory multi-agent orchestration, web UI, MCP, and issue synchronization until
  demonstrated demand exists.

## Now

### R0 — Repository Bootstrap

**Goal:** Establish a coherent repository that humans and agents can use safely.

Deliverables:

- `pyproject.toml`;
- project-level governing documents;
- DoR, DoD, DoW, and DoF definitions;
- `.ggsad/` configuration, profiles, schemas, mappings, and templates;
- Python package and CLI skeleton;
- test structure;
- GSD local project integration;
- initial ADR set;
- `CHG-001-reference-repository-bootstrap`.

Exit criteria:

- repository installs with `uv sync`;
- baseline validation commands execute;
- GG-SAD and GSD ownership rules are explicit;
- Claude Code can start from approved instructions;
- no production capability is claimed without evidence.

**Status (2026-08-04):** Complete. `CHG-001-reference-repository-bootstrap` reached Build-Done and
Verify-Done — all five exit criteria above are evidenced in `specs/CHG-001-reference-repository-
bootstrap/evidence.md`. Pair Review (`agent:codex`, distinct from the implementing agent) completed
two real passes with zero open blocking findings. See `evidence.md` §14–15 for the full gate record.

### R1 — Reference Repository and Manual Flow

**Goal:** Make GG-SAD usable without a CLI or external platform dependency.

Deliverables:

- default profiles: lean, standard, governed, regulated;
- project and change templates;
- sample `state.yaml`;
- examples for Class S, M, and L;
- lean startup, solo developer, and governed examples;
- Example-Driven Specification examples;
- Pair Review examples, including Human–Human and mixed participants;
- manual wait and fail examples.

Exit criteria:

- a user can copy the repository structure;
- a complete flow can be executed manually;
- stand-alone operation works;
- GSD remains optional and subordinate;
- examples demonstrate distinct wait and fail outcomes.

**Status (2026-08-04):** Partially delivered by `CHG-001-reference-repository-bootstrap`, which was
scoped to Class M only (R-018/R-020; see `spec.md`'s Constraints and excluded-capability list).
Delivered: a complete Class M example (`specs/examples/class-m/`, honestly `evidence.md` "Not Run"
throughout, per the constitution's rule against asserting unexecuted checks); stand-alone operation
verified (R-016, E-012); GSD demonstrated as optional and subordinate (R-006/R-017). The four
built-in profile *names* (lean/standard/governed/regulated) are recognized and validated for
identity (E-006), but `.ggsad/profiles/` has no actual profile-content files yet — full profile
*resolution* is R4's job, not R0/R1's. Not yet delivered, remaining as future roadmap work: Class S
and L examples; a Human–Human or mixed-participant Pair Review example (CHG-001's own Pair Review
was Agent–Agent, `agent:claude-code`/`agent:codex`); dedicated manual wait and fail demonstration
examples (distinct from the incidental wait/fail behavior exercised during CHG-001's own build).

### R2 — Initial Vertical CLI Slice

**Goal:** Initialize and validate a project and create a controlled first change.

Initial commands:

```text
ggsad init
ggsad new
ggsad status
ggsad validate
ggsad transition
```

Initial controlled transition:

```text
draft → ready
```

Exit criteria:

- invalid configuration and state are rejected;
- required artifacts are created by class and profile;
- transition history is recorded;
- errors identify exact files and criteria;
- unit and acceptance tests pass.

**Status (2026-08-04):** Delivered by `CHG-001-reference-repository-bootstrap`, with one deliberate
scope narrowing: `ggsad status` from the original command list above was never part of CHG-001's
actually-approved scope (`spec.md`'s requirements are R-001 through R-020, and `CLAUDE.md`'s
Initial Change Constraint names exactly `init`/`new`/`validate`/`transition`) — this was a
pre-existing gap between this roadmap entry and the approved spec, not something dropped during
implementation. All five exit criteria above are met for the four commands actually built (150
tests, 98.58% coverage; see `evidence.md` §5–8). `ggsad status` remains a candidate for a future
change if/when needed.

## Next

### R3 — State and Transition Engine

Deliverables:

- Pydantic state models;
- YAML loader and atomic writer;
- explicit transition actions;
- history events;
- wait, resume, fail, cancel, supersede, and reopen behavior;
- property-based transition tests.

Exit criteria:

- invalid transitions are rejected;
- wait and fail remain distinguishable;
- safe state and resume metadata are preserved;
- every accepted transition creates history.

### R4 — Profile Resolver and Mapping Registry

Deliverables:

- deterministic profile resolution;
- invariant-core validation;
- custom-profile inheritance;
- effective-workflow report;
- mapping schema and registry;
- validated GSD mapping;
- stand-alone mapping;
- project-brief integration fields.

Exit criteria:

- all default profiles preserve invariants;
- lean mode avoids unnecessary artifacts;
- governed and regulated modes strengthen controls;
- mapping conflicts produce explainable outcomes;
- deleting mappings preserves stand-alone operation.

### R5 — Document Validator

Deliverables:

- required-file and heading validation;
- unresolved-placeholder detection;
- identifier and reference validation;
- artifact-policy validation;
- gate-weakening detection;
- initial hierarchy-conflict checks;
- machine-readable reports.

Exit criteria:

- structural errors are actionable;
- local weakening is blocked;
- validation can run locally and in CI;
- unsupported semantic claims are not presented as certain.

### R6 — Gate Engine

Deliverables:

- criterion model;
- automatic, review, and approval checks;
- mandatory DoF → DoW → DoD → DoR order;
- criterion-level reports;
- wait and failure record generation;
- close prerequisites.

Exit criteria:

- automatic checks are reproducible;
- human approvals cannot be self-issued by agents;
- failed criteria block transitions;
- not-applicable criteria require explainable resolution.

### R7 — Evidence and Traceability

Deliverables:

- requirement parser;
- acceptance-example parser;
- evidence reference model;
- requirement-to-example-to-evidence validation;
- quality-gate evidence;
- deviation and limitation records;
- final close evaluation.

Exit criteria:

- missing required evidence blocks closure;
- external reports are referenced rather than duplicated;
- traceability is explainable;
- deviations remain explicit.

### R8 — Pair Review Engine

Deliverables:

- review requirement resolution;
- participant identity model;
- review cycles and findings;
- severity and disposition rules;
- blocking-finding integration;
- conditional inline evidence and `review.md`.

Exit criteria:

- distinct Requestor and Reviewer identities are validated;
- Human–Human and mixed combinations work;
- unresolved blocking findings block gates;
- Pair Review remains separate from human approval.

## Later

### R9 — Agent Workflows

- phase-specific commands for intake, specify, plan, build, verify, review, close, status, and
  resume;
- least-privilege permission profiles;
- context-loading contracts;
- actionable wait and fail outputs;
- one-agent initial execution model.

### R10 — CI Integration

- stable exit codes;
- JSON validation reports;
- GitHub Actions example;
- GitLab CI example;
- pull-request and release validation profiles.

### R11 — Companion Methods and Practice Profiles

- documented mappings for OpenSpec, Spec Kit, BMAD, Hermes, and Kiro;
- testing practice profiles;
- architecture practice profiles;
- Threat Modeling;
- Design Thinking and Jobs to Be Done;
- validated combination recipes.

### R12 — Optional Repository and IDE Integrations

Candidates:

- GitHub Issues and Pull Requests;
- GitLab Issues and Merge Requests;
- Linear;
- Jira;
- VS Code;
- JetBrains;
- release tooling;
- MCP server;
- dashboard or web UI.

Admission requires demonstrated repeated need, clear ownership, permissions, failure behavior, and
acceptable maintenance cost.

### R13 — GG-SAD Project Memory

Deliverables:

- backend-neutral memory API;
- Decision, Learning, Failure, Definition, and External Source records;
- ADR-versus-Decision validation;
- provenance, trust, status, scope, retention, and redaction;
- file-based initial backend;
- export and migration;
- permission-aware retrieval.

Exit criteria:

- architecture decisions cannot bypass ADRs;
- every record has stable identity and provenance;
- governing documents override memory;
- storage remains portable and replaceable.

### R14 — Stable 1.0 Reference Implementation

Readiness requires:

- method stability across at least two minor releases;
- real pilot projects;
- versioned schemas;
- migration guidance;
- reviewed security and permission boundaries;
- proven stand-alone and combination modes;
- validated compliance profiles;
- stable Example-Driven Specification and Pair Review semantics.

Done requires:

- Class S, M, and L support;
- all four gate types operational;
- reliable wait/fail distinction;
- evidence-controlled closure;
- optional functional CI;
- phase-scoped agent workflows;
- complete documentation and examples;
- upgrade and rollback guidance;
- portable governed memory;
- no mandatory vendor, platform, or agent dependency.

## Open

### Dual-Track Development

Open questions:

- parallel Discovery and Delivery state;
- handover gates;
- ownership;
- evidence synchronization;
- prevention of unvalidated discovery assumptions entering delivery.

### Delivery Models

Trunk-Based Development, GitFlow, and Continuous Delivery remain open until decisions cover:

- branching compatibility;
- merge and release gates;
- feature-flag expectations;
- release evidence;
- rollback semantics;
- repository and CI coupling.

### Approval Identity

A portable method for recording and validating human approval identity remains open.

### Semantic Validation

The boundary between deterministic structural validation and model-assisted semantic review
requires explicit trust, reproducibility, and evidence rules.

## Deferred by Default

- mandatory multi-agent orchestration;
- automatic subagent delegation;
- hooks for every phase;
- centralized database-backed state;
- mandatory semantic memory;
- web application;
- mandatory issue synchronization;
- unrestricted workflow DSL;
- sprint and epic management;
- autonomous architecture approval;
- analytics platform.
