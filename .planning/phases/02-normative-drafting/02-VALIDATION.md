---
phase: 02
slug: normative-drafting
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-10-24
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution. This is a documentation phase: the artifact is a diff to one Markdown specification, so validation is a read-only check script plus plan acceptance commands (see the Validation Architecture section of 02-RESEARCH.md).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | bash check script `.planning/phases/02-normative-drafting/02-check-normative-diff.sh` (built from plan 02-01 on; no Python test framework is involved) |
| **Config file** | none |
| **Quick run command** | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh` |
| **Full suite command** | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --final` (plan 02-05 only) |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** run the quick run command
- **After every plan wave:** run the quick run command with the ids drafted so far
- **Before `/gsd-verify-work`:** the `--final` run must pass
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | SPEC-12,SPEC-13 | T-02-01 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh \| tail -n1` | planned | ⬜ pending |
| 02-01-02 | 01 | 1 | SPEC-12,SPEC-13 | T-02-01 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh \| tail -n1` | planned | ⬜ pending |
| 02-01-03 | 01 | 1 | SPEC-12,SPEC-13 | T-02-01 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh \| tail -n1; git log --format=%s origin/main..HEAD -- docs/method/GG-SAD_normative_method` | planned | ⬜ pending |
| 02-02-01 | 02 | 2 | SPEC-02,SPEC-01,SPEC-07,SPEC-08,SPEC-03,SPEC-13 | T-02-02 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-02 \| tail -n1` | planned | ⬜ pending |
| 02-02-02 | 02 | 2 | SPEC-02,SPEC-01,SPEC-07,SPEC-08,SPEC-03,SPEC-13 | T-02-02 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-02,SPEC-01,SPEC-07 \| tail -n1` | planned | ⬜ pending |
| 02-02-03 | 02 | 2 | SPEC-02,SPEC-01,SPEC-07,SPEC-08,SPEC-03,SPEC-13 | T-02-02 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-02,SPEC-01,SPEC-07,SPEC-08,SPEC-03 \| tail -n1` | planned | ⬜ pending |
| 02-03-01 | 03 | 3 | SPEC-04,SPEC-05,SPEC-06,SPEC-11,SPEC-10,SPEC-09,SPEC-13 | T-02-03 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-04 \| tail -n1` | planned | ⬜ pending |
| 02-03-02 | 03 | 3 | SPEC-04,SPEC-05,SPEC-06,SPEC-11,SPEC-10,SPEC-09,SPEC-13 | T-02-03 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-04,SPEC-05,SPEC-06,SPEC-11 \| tail -n1` | planned | ⬜ pending |
| 02-03-03 | 03 | 3 | SPEC-04,SPEC-05,SPEC-06,SPEC-11,SPEC-10,SPEC-09,SPEC-13 | T-02-03 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-04,SPEC-05,SPEC-06,SPEC-11,SPEC-10,SPEC-09 \| tail -n1` | planned | ⬜ pending |
| 02-04-01 | 04 | 4 | SPEC-15,SPEC-18,SPEC-17,SPEC-13 | T-02-04 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-15 \| tail -n1` | planned | ⬜ pending |
| 02-04-02 | 04 | 4 | SPEC-15,SPEC-18,SPEC-17,SPEC-13 | T-02-04 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-15,SPEC-18 \| tail -n1` | planned | ⬜ pending |
| 02-04-03 | 04 | 4 | SPEC-15,SPEC-18,SPEC-17,SPEC-13 | T-02-04 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-15,SPEC-18,SPEC-17 \| tail -n1` | planned | ⬜ pending |
| 02-05-01 | 05 | 5 | SPEC-16,SPEC-14,SPEC-13 | T-02-05 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --ids SPEC-16 \| tail -n1` | planned | ⬜ pending |
| 02-05-02 | 05 | 5 | SPEC-16,SPEC-14,SPEC-13 | T-02-05 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --final \| grep -E '^(PASS F1\|FAIL)'` | planned | ⬜ pending |
| 02-05-03 | 05 | 5 | SPEC-16,SPEC-14,SPEC-13 | T-02-05 | read-only check script; no push, no out-of-scope paths | script | `bash .planning/phases/02-normative-drafting/02-check-normative-diff.sh --final \| tail -n1; git hash-object docs/method/GG-SAD_normative_method_specification.md` | planned | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `02-check-normative-diff.sh` — created in plan 02-01 task 1 (tracer) and extended in each later plan
- Existing infrastructure covers the rest (git, bash, grep, sha256sum).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Rule correctness of the drafted text, drafting choices, the `full` realizations | SPEC-01..SPEC-18 | A script cannot judge whether a rule says the right thing | Owner approval (Phase 3) and independent review (Phase 4) |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
