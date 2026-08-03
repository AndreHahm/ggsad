# Implementation Plan: <Change ID> — <Change Title>

## Metadata

- Change ID: <CHG-NNN>
- Status: Draft | Approved | Superseded
- Phase: plan
- Requestor: <participant-id>
- Planner: <participant-id>
- Approver: <participant-id-or-pending>
- Created: <YYYY-MM-DD>
- Last Updated: <YYYY-MM-DD>
- Specification: `spec.md`
- State: `state.yaml`

## 1. Purpose

<Explain what this plan covers and how it implements the approved specification.>

This plan is subordinate to the approved specification, accepted ADRs, architecture, project
brief, and constitution.

## 2. Planning Preconditions

- [ ] Specification is approved where required.
- [ ] Relevant project documents and ADRs were reviewed.
- [ ] Blocking questions are resolved or explicitly accepted.
- [ ] Required dependencies and permissions are identified.
- [ ] Ready-to-Plan criteria are satisfied.

## 3. Technical Approach

<Describe the selected approach, major design choices, and why it satisfies the specification.>

## 4. Alternatives Considered

### Option 1 — <Name>

- Summary:
- Advantages:
- Disadvantages:
- Reason Not Selected:

### Option 2 — <Name>

- Summary:
- Advantages:
- Disadvantages:
- Reason Not Selected:

## 5. Affected Components and Artifacts

| Component or Artifact | Planned Change | Requirement | Owner |
|---|---|---|---|
| <path-or-component> | <change> | R-001 | <owner> |

## 6. Architecture Impact

- Impact: None | Minor | Material
- ADR Required: Yes | No | Unknown
- Architecture Document Update Required: Yes | No
- Dependency Direction Changes: <description-or-none>
- Boundary Changes: <description-or-none>
- Related ADRs: <references>

<Describe the architectural impact.>

## 7. Data and State Impact

- Data Model Changes:
- State Model Changes:
- Configuration Changes:
- Schema Changes:
- Persistence Changes:
- Retention or Migration Impact:

## 8. Interface and Compatibility Impact

- CLI:
- API:
- Events:
- File Formats:
- Public Interfaces:
- Backward Compatibility:
- Deprecation:
- Versioning:

## 9. Security, Privacy, and Compliance Impact

- Threats:
- Trust Boundaries:
- Permissions:
- Secrets:
- Data Classification:
- Privacy:
- Compliance:
- Required Review or Approval:

## 10. Operational Impact

- Deployment:
- Packaging:
- Monitoring:
- Logging:
- Metrics:
- Alerting:
- Support:
- Backup and Recovery:
- Rollback:

## 11. Test and Verification Strategy

| Requirement / Example | Test Level | Test or Check | Evidence |
|---|---|---|---|
| R-001 / E-001 | unit | <test> | <evidence reference> |

### Required Test Types

- Unit:
- Integration:
- Acceptance:
- Regression:
- Property-Based:
- Security:
- Performance:
- Compatibility:
- Manual Review:

## 12. Evidence Strategy

<Describe where results will be recorded and which existing reports will be referenced rather than
duplicated.>

Expected evidence:

- <evidence item>
- <evidence item>

## 13. Pair Review Plan

- Required: Yes | No | Conditional
- Requestor: <participant-id>
- Reviewer: <distinct-participant-id-or-pending>
- Review Scope:
- Review Criteria:
- Stable Review Target:
- Blocking-Finding Rule:
- Re-verification Required: Yes | No | Conditional

## 14. Migration and Rollback

### Migration

<Describe migration steps or state `Not required`.>

### Rollback

<Describe rollback, withdrawal, or safe-state preservation.>

### Irreversible Actions

- <action or None>

## 15. Dependencies and Permissions

| Dependency or Permission | Owner | Required Before | Failure Behavior |
|---|---|---|---|
| <dependency> | <owner> | <step-or-phase> | wait | fail |

## 16. Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation | Detection |
|---|---|---|---|---|
| <risk> | low | medium | high | low | medium | high | <mitigation> | <signal> |

## 17. Implementation Sequence

1. <vertical implementation step>
2. <test or validation step>
3. <documentation or evidence step>

Each step SHOULD produce a reviewable and recoverable state.

## 18. Task Decomposition

Tasks are maintained in `tasks.md` only when decomposition provides execution value.

- Task Artifact Required: Yes | No
- Rationale: <rationale>

## 19. Wait and Fail Handling

### Expected Wait Conditions

| Condition | Owner / Source | Safe State | Resume Condition | Next Action |
|---|---|---|---|---|
| <condition> | <owner> | <state> | <condition> | <action> |

### Expected Fail Conditions

| Trigger | Required Response | Preservation Action | Final Status |
|---|---|---|---|
| <trigger> | <response> | <action> | FAILED_<CATEGORY> |

## 20. Delivery and Commit Strategy

- Branch or Worktree:
- Commit Boundaries:
- Generated Files:
- Review Target:
- Merge or Release Policy:

## 21. Plan Validation

Before approval, confirm:

- [ ] Every planned change maps to a requirement or approved technical necessity.
- [ ] No accepted ADR is contradicted.
- [ ] No excluded scope was introduced.
- [ ] Verification and evidence work are included.
- [ ] Migration, rollback, wait, and fail behavior are clear.
- [ ] Required approvals and Pair Review are identified.
- [ ] The implementation sequence is safe and reviewable.

## 22. Decisions and References

| Decision | Type | Reference |
|---|---|---|
| <decision> | ADR | scoped decision | specification | <path> |

## 23. Approval

- Approval Required: Yes | No
- Approver:
- Status: Pending | Approved | Rejected | Not Required
- Evidence:

## 24. Plan History

| Date | Actor | Status | Summary |
|---|---|---|---|
| <YYYY-MM-DD> | <actor> | Draft | Initial plan |
