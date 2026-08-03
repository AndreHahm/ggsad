# System Architecture

## Metadata

- Project: <project-name>
- Status: Draft | Active | Superseded
- Architecture Version: <version>
- Last Updated: <YYYY-MM-DD>
- Owner: <name-or-role>
- Related Change: <change-id-or-none>

## 1. Purpose

<Describe the purpose and scope of this architecture document.>

This document describes the current structural state of the system. Durable architecture
decisions and their rationale belong in ADRs.

## 2. Architectural Goals

- <goal>
- <goal>
- <goal>

## 3. Architectural Principles

1. **<Principle>.** <Explanation>
2. **<Principle>.** <Explanation>
3. **<Principle>.** <Explanation>

## 4. System Context

<Describe the system, its users, external actors, and surrounding systems.>

```text
<system-context-diagram>
```

### 4.1 Actors

| Actor | Responsibility | Interaction |
|---|---|---|
| <actor> | <responsibility> | <interaction> |

### 4.2 External Systems

| System | Purpose | Interface | Authority / Source of Truth |
|---|---|---|---|
| <system> | <purpose> | <interface> | <authority> |

## 5. Scope and Boundaries

### Included

- <component or responsibility>

### Excluded

- <component or responsibility>

### Trust Boundaries

- <boundary and significance>

## 6. Architecture Overview

```text
<high-level-component-diagram>
```

<Explain the overall structure and primary dependency direction.>

## 7. Components and Responsibilities

### 7.1 <Component Name>

**Purpose**

<What this component does.>

**Responsibilities**

- <responsibility>
- <responsibility>

**Owned Data or Artifacts**

- <data or artifact>

**Interfaces**

- <interface>

**Dependencies**

- <dependency>

**Constraints**

- <constraint>

### 7.2 <Component Name>

<Repeat the component structure as needed.>

## 8. Module and Dependency Rules

```text
<dependency-direction>
```

### Allowed Dependencies

- <source> → <target>

### Forbidden Dependencies

- <source> → <target>

### Dependency Invariants

- <invariant>

## 9. Data Model

### 9.1 Core Entities

#### <Entity>

- <field>
- <field>
- <field>

### 9.2 Data Ownership

| Data | Owner | Storage | Retention | Classification |
|---|---|---|---|---|
| <data> | <component> | <location> | <policy> | <classification> |

## 10. Main Data and Control Flows

### 10.1 <Flow Name>

```text
<flow-diagram>
```

1. <step>
2. <step>
3. <step>

### 10.2 Failure and Recovery Flow

<Describe failure handling, rollback, retry, wait, and recovery behavior.>

## 11. Interfaces and Contracts

### 11.1 CLI or User Interfaces

| Interface | Purpose | Stability | Contract Reference |
|---|---|---|---|
| <interface> | <purpose> | experimental | stable | <reference> |

### 11.2 APIs, Events, or File Contracts

| Contract | Producer | Consumer | Versioning | Schema |
|---|---|---|---|---|
| <contract> | <producer> | <consumer> | <policy> | <path> |

## 12. Deployment and Operational Architecture

### 12.1 Deployment Topology

```text
<deployment-diagram>
```

### 12.2 Runtime Environments

| Environment | Purpose | Deployment Method | Data |
|---|---|---|---|
| <environment> | <purpose> | <method> | <data> |

### 12.3 Observability

- Logging:
- Metrics:
- Tracing:
- Audit History:
- Health Checks:

### 12.4 Backup, Recovery, and Rollback

- Backup:
- Recovery:
- Rollback:
- Recovery Objectives:

## 13. Security and Privacy Architecture

- Authentication:
- Authorization:
- Secrets:
- Trust Boundaries:
- Data Classification:
- Encryption:
- Auditability:
- Threat Model Reference:
- Privacy Constraints:

## 14. Reliability and Performance Requirements

- Availability:
- Consistency:
- Atomicity:
- Retry Behavior:
- Capacity:
- Latency:
- Resource Limits:
- Degraded Mode:

## 15. Integration Architecture

| Integration | Mode | Owned Capability | Permissions | Failure Behavior | Uninstall Behavior |
|---|---|---|---|---|---|
| <integration> | adapter | companion | <capability> | <permissions> | <behavior> | <behavior> |

## 16. Technology Baseline

| Area | Selected Technology | Rationale | ADR |
|---|---|---|---|
| Language | <technology> | <short rationale> | <ADR reference> |
| Configuration | <technology> | <short rationale> | <ADR reference> |
| Testing | <technology> | <short rationale> | <ADR reference> |

## 17. Architectural Constraints

- <constraint>
- <constraint>
- <constraint>

## 18. Known Limitations and Technical Debt

| Limitation | Impact | Current Mitigation | Planned Resolution |
|---|---|---|---|
| <limitation> | <impact> | <mitigation> | <resolution> |

## 19. Architectural Risks

| Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|
| <risk> | low | medium | high | low | medium | high | <mitigation> | <owner> |

## 20. Related ADRs

- `<ADR-path>` — <decision title>

## 21. Related Artifacts

- Constitution: `docs/constitution.md`
- Project Brief: `docs/project-brief.md`
- Roadmap: `docs/roadmap.md`
- Definitions: `docs/definitions/`
- Schemas: `<path>`
- Active Change: `<path-or-none>`

## 22. Architecture History

| Date | Version | Actor | Related Change | Summary |
|---|---|---|---|---|
| <YYYY-MM-DD> | <version> | <actor> | <change-id> | <summary> |
