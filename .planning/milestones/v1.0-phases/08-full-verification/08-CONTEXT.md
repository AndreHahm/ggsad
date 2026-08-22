# Phase 8 Context — Full Verification

## Status

Design approved by the repository owner on 2026-08-21. This artifact defines the boundary for
Phase 8 planning and execution.

## Goal

Run the milestone's complete repository verification baseline clean, preserve reproducible GSD
evidence for every required command, reconcile factual inconsistencies in active planning metadata,
and establish whether Milestone 1 is ready to close without changing product or method behavior.

## Selected Approach

Use one deterministic verification plan with three ordered parts:

1. reconcile only active planning metadata that contradicts completed milestone work;
2. run the exact VERIFY-01 command sequence from a clean worktree and capture its results;
3. record requirement-level and GSD milestone verification evidence before closing Phase 8.

Phase 8 is an evidence-and-closure phase. It does not reopen Phases 1–7, broaden their scope, or
create another implementation-remediation cycle without a newly evidenced blocking failure.

## Verification Baseline

VERIFY-01 uses exactly this command sequence:

```text
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run ty check src tests
uv run pytest
uv build
```

Each command must be run from the repository root in the Phase 8 worktree. Evidence must record the
command, exit status, material output, and relevant result counts. Required summaries include the
pytest test count and coverage result and the names of successfully produced distribution artifacts.

Before running the sequence, set `UV_NATIVE_TLS=1` for the Phase 8 verification process and record
that environment precondition in the evidence. The six command strings above remain authoritative
and unchanged; native TLS is configured before the run rather than added later as a retry flag.

`TLS-INTERCEPTION-ROOT-CAUSE.md` establishes why this is required on the current Windows machine:
Norton Antivirus actively re-signs PyPI certificates with a local root trusted by the Windows
certificate store, while uv's default bundled roots do not trust that issuer. Native TLS continues
certificate verification using the machine's configured trust policy; it does not disable TLS
validation or alter repository dependencies. The same condition was previously observed in
`.planning/milestones/PR-3-REBASE-SHA-RECONCILIATION.md`.

The evidence must retain the earlier default-backend `UnknownIssuer` diagnostic and distinguish it
from the authoritative run under `UV_NATIVE_TLS=1`. Do not run `uv sync --locked --native-tls` as a
post-failure fallback. A required-command failure after the environment precondition is applied
blocks closure until it is fixed in scope or explicitly returned to planning for disposition.

## Quality-Tool Boundary

The canonical strict type-check command is:

```text
uv run ty check src tests
```

Bare `uv run ty check` is not part of VERIFY-01. Its known diagnostics in installer-owned
`.claude/scripts/` are outside the product quality-tool ownership boundary established in Phase 5.
Phase 8 may mention this distinction so readers do not confuse the two commands, but it must not
suppress, fix, exclude, or otherwise change those installer-owned diagnostics.

## Evidence Contract

Phase 8 must create canonical GSD verification evidence under
`.planning/phases/08-full-verification/`. The evidence must:

- identify the verified revision and worktree state;
- record `UV_NATIVE_TLS=1` as the verification environment precondition and cite the root-cause
  analysis;
- cover VERIFY-01 and VERIFY-02 explicitly;
- record every required baseline command and its result;
- record GSD consistency and health results separately from the product baseline;
- distinguish errors from non-blocking warnings and state their disposition;
- confirm that the English normative specification, product source, tests, product configuration,
  `.ggsad/`, and installer-owned `.claude/` files were not changed by Phase 8;
- avoid creating GG-SAD `evidence.md` or advancing GG-SAD change state;
- support the final milestone audit without making the Phase 8 artifact depend on the SHA of the
  commit that contains that same artifact.

Raw terminal output may be summarized where it is repetitive, but the recorded evidence must remain
sufficient to reproduce each check and verify its result. Failed attempts and successful reruns must
not be collapsed into a misleading single success.

## Planning-Metadata Reconciliation

Phase 8 may correct active `.planning/` metadata only when current files contradict already recorded
completion evidence. The known candidates are:

- `.planning/REQUIREMENTS.md` traceability rows that still label completed NORM, AUDIT, or GAP
  requirement groups as pending;
- `.planning/STATE.md` continuity or blocker text that still describes initialization or an earlier
  phase as current;
- `.planning/ROADMAP.md` Phase 7 details that say `Plans: TBD` while the Progress table says Phase 7
  completed `1/1` plans;
- the mismatch between ROADMAP's Phase 6/7 `1/1` plan claims and `.planning/STATE.md`'s seven total
  plans, which account only for the formal plans completed in Phases 1–5;
- the absent Phase 7 directory and resulting GSD `6 → 8` numbering-gap warning, considered together
  with the retroactive Phase 6/7 evidence rather than repaired as an isolated filesystem warning;
- Phase 8 plan, summary, verification, state, roadmap, and requirement status fields required by
  normal GSD phase completion.

Corrections must preserve historical phase artifacts and must not reinterpret approved decisions,
requirements, or prior review outcomes. Discovery of a substantive contradiction is reported as a
finding rather than silently rewritten under the label of metadata cleanup.

## GSD Validation

Phase 8 planning and closure must run the supported pinned-GSD validations, including consistency
and health. The pre-Phase-8 warnings that Phase 7 or Phase 8 lacks an on-disk directory must be
re-evaluated after the Phase 8 directory exists. Any remaining warning must be recorded with its
cause and closure impact; warnings are not silently ignored.

## Scope Boundaries

Phase 8 may change only:

- Phase 8 artifacts under `.planning/phases/08-full-verification/`;
- factual status and continuity fields in active `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`,
  and `.planning/STATE.md` needed for verified Phase 8 or milestone closure;
- canonical GSD milestone verification or audit artifacts created by the supported workflow.

Phase 8 must not change:

- `docs/method/GG-SAD_normative_method_specification.md`;
- product implementation under `src/ggsad/`;
- tests or fixtures;
- `pyproject.toml`, `uv.lock`, or other product quality-tool configuration;
- `.ggsad/` schemas, templates, mappings, profiles, or examples;
- installer-owned `.claude/` files;
- archived historical material;
- product behavior or the approved meanings of requirements.

If a required baseline command exposes a defect that cannot be resolved within these boundaries,
Phase 8 stops and records the blocker. It does not expand its own authority to fix the defect.

## Completion Boundary

Phase 8 closes only when:

1. all six required VERIFY-01 commands pass exactly as specified;
2. VERIFY-01 and VERIFY-02 have explicit GSD evidence;
3. planning metadata accurately reflects Phases 1–8 and all completed v1 requirements;
4. GSD validation results and any residual warnings are recorded and dispositioned;
5. the Phase 8 diff remains within the documentation-only scope above; and
6. the repository owner explicitly authorizes milestone closure after reviewing the verification
   result.

Milestone 1 does not close automatically when the command baseline passes.
