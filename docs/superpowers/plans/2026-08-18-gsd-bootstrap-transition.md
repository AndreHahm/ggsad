# GSD Bootstrap Transition Implementation Plan

> **For agentic workers:** Execute this bootstrap plan sequentially. After Task 4, GSD Core 1.10.0
> is the sole development method and all further planning must be created and executed through GSD.

**Goal:** Replace the repository's mixed GG-SAD/GSD development governance with a verified,
pinned GSD Core 1.10.0 installation and an onboarded `.planning/` workspace, without changing the
GG-SAD normative specification or Python implementation.

**Architecture:** This is a narrow bootstrap boundary. The official installer owns `.claude/` GSD
runtime files; concise repository instructions establish the English normative specification as
product authority and GSD as development method; GSD onboarding then becomes the only source of
development plans and execution state.

**Tech Stack:** Git, Node.js/npm, official `@opengsd/gsd-core` installer, Markdown, Python/uv
verification commands.

**Spec:** `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`

## Global constraints

- Do not modify `docs/method/GG-SAD_normative_method_specification.md` during this bootstrap.
- Do not modify `src/ggsad/`, `tests/`, product schemas, templates, or examples.
- Do not manually edit installer-owned files listed by `.claude/gsd-file-manifest.json`.
- Preserve Git history and unrelated user changes.
- Pin GSD Core exactly to `1.10.0`; do not use `latest`.
- GSD is the sole development method after onboarding; GG-SAD remains the product being built.
- The English normative specification is the leading product authority.
- Normative amendments require repository-owner approval and independent Claude Code review.
- Stop if the installer reports an unresolved migration, destructive replacement, or manifest
  conflict involving a project-authored customization.

---

### Task 1: Capture the pre-transition baseline

**Files:**

- Read: `.claude/gsd-core/VERSION`
- Read: `.claude/gsd-file-manifest.json`
- Read: `.claude/gsd-install-state.json`
- Read: `AGENTS.md`
- Read: `CLAUDE.md`
- Read: `CLAUDE_CODE_PROJECT_START.md`
- Read: `pyproject.toml`
- Create: none
- Modify: none

**Interfaces:**

- Consumes: approved design commit on `bootstrap-gsd-transition`.
- Produces: recorded command output proving the pre-transition version, clean working tree, and
  baseline product-test result.

- [ ] **Step 1: Confirm the branch and exact working-tree scope**

Run:

```powershell
git branch --show-current
git status --short
git log -1 --oneline
```

Expected: branch is `bootstrap-gsd-transition`; status is clean; the latest commit contains the
approved design or this plan only.

- [ ] **Step 2: Confirm the installed GSD baseline**

Run:

```powershell
Get-Content -Raw .claude\gsd-core\VERSION
Get-Content -Raw .claude\gsd-install-state.json
```

Expected: version is `1.9.1`; install state parses as JSON and contains the existing installer
migrations.

- [ ] **Step 3: Capture the baseline product checks**

Run:

```powershell
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run pytest
```

Expected: dependency synchronization, formatting, lint, and all 150 current tests pass. Do not run
`ty check` as a green baseline assertion here: the known installer-owned `.claude/scripts` files
currently produce 31 diagnostics and Task 4 must record that as a future GSD work item rather than
silently weakening product checks.

- [ ] **Step 4: Stop on unexpected state**

If the branch, working tree, version, or product checks differ from the expected values, preserve
the output and stop before running the installer. Do not reset or discard unexpected files.

---

### Task 2: Update installer-owned GSD Core to 1.10.0

**Files:**

- Installer-managed update: `.claude/agents/`
- Installer-managed update: `.claude/commands/`
- Installer-managed update: `.claude/gsd-core/`
- Installer-managed update: `.claude/hooks/`
- Installer-managed update: `.claude/gsd-file-manifest.json`
- Installer-managed update: `.claude/gsd-install-state.json`
- Preserve: `.claude/analysis-kit.settings.json`
- Preserve: `.claude/git-kit.settings.json`
- Preserve: project-authored `.claude/skills/`

**Interfaces:**

- Consumes: clean Task 1 baseline and official npm package `@opengsd/gsd-core@1.10.0`.
- Produces: installer-managed GSD Core 1.10.0 files and an updated manifest/install state.

- [ ] **Step 1: Verify official npm package metadata**

Run:

```powershell
npm view @opengsd/gsd-core@1.10.0 name version repository.url dist.integrity
```

Expected: name is `@opengsd/gsd-core`; version is `1.10.0`; repository URL identifies
`open-gsd/gsd-core`; npm reports a non-empty integrity value. Stop before installation if any field
is absent or differs.

- [ ] **Step 2: Run the official pinned installer**

Run from the repository root:

```powershell
npx @opengsd/gsd-core@1.10.0 --claude --local
```

Expected: installer identifies the existing local installation, applies supported migrations, and
reports a successful Claude-local installation. If it asks before replacing a modified
installer-owned file, inspect the reported path and stop unless the manifest proves the file is
unmodified upstream content.

- [ ] **Step 3: Verify the installed version**

Run:

```powershell
Get-Content -Raw .claude\gsd-core\VERSION
```

Expected: exactly `1.10.0`, allowing only the file's trailing newline.

- [ ] **Step 4: Verify installer state and command surface**

Run:

```powershell
Get-Content -Raw .claude\gsd-file-manifest.json | ConvertFrom-Json | Out-Null
Get-Content -Raw .claude\gsd-install-state.json | ConvertFrom-Json | Out-Null
node .claude\gsd-core\bin\gsd-tools.cjs --help
```

Expected: both JSON documents parse; CLI exits successfully and lists `init`, `validate`, `state`,
`roadmap`, and `verify` commands.

- [ ] **Step 5: Review installer scope**

Run:

```powershell
git status --short
git diff --stat
git diff -- .claude/analysis-kit.settings.json .claude/git-kit.settings.json .claude/skills
```

Expected: installer-owned GSD files may change; project-owned settings and skills show no diff.
Stop if the installer changes product code, tests, normative documents, or project-owned skills.

- [ ] **Step 6: Commit the installer-managed update**

Run:

```powershell
git add -- .claude/agents .claude/commands .claude/gsd-core .claude/hooks .claude/gsd-file-manifest.json .claude/gsd-install-state.json .claude/settings.json .claude/package.json
git diff --cached --check
git commit -m "chore: pin GSD Core 1.10.0"
```

Expected: one commit containing only installer-managed GSD update output.

---

### Task 3: Replace conflicting development instructions

**Files:**

- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Delete: `CLAUDE_CODE_PROJECT_START.md`
- Test: repository text searches listed below

**Interfaces:**

- Consumes: approved transition design and installed GSD Core 1.10.0.
- Produces: concise cross-agent authority rules that do not create a second development workflow.

- [ ] **Step 1: Replace `AGENTS.md` with the bootstrap authority contract**

The replacement must contain exactly these policy sections and meanings:

```markdown
# Agent Instructions

## Product authority

`docs/method/GG-SAD_normative_method_specification.md` is the leading source for GG-SAD method
semantics and reference-implementation behavior. Development artifacts must not redefine it.

## Development method

This repository uses pinned GSD Core 1.10.0 as its sole development method. Read and follow the
active `.planning/` project, requirements, roadmap, state, context, plans, and verification
artifacts. Do not create or advance GG-SAD change state to govern repository development.

## Approval and review

Changes to the English normative specification require explicit repository-owner approval and
independent review by Claude Code. A fresh context or subagent of the Requestor is not independent.

## Engineering baseline

Use Python with explicit type annotations, uv, Typer, Pydantic v2, ruamel.yaml, JSON Schema,
pytest, Hypothesis where valuable, Ruff, and ty strict checking. Preserve unrelated changes,
avoid destructive Git operations, do not commit secrets, and report checks that were not run.

Run the applicable baseline before completion:

`uv sync --locked`
`uv run ruff format --check .`
`uv run ruff check .`
`uv run ty check`
`uv run pytest`
`uv build`

Installer-owned GSD files are development tooling, not Python product source. Product quality-tool
scope must be defined explicitly rather than weakened to hide product diagnostics.
```

- [ ] **Step 2: Replace `CLAUDE.md` with a Claude-specific pointer**

Use this content:

```markdown
# Claude Code Instructions

Follow `AGENTS.md` and the active GSD Core 1.10.0 workflow under `.planning/`.

For normative-specification work, act as Requestor only when assigned implementation work. When
assigned independent review, do not edit the reviewed artifact; return findings with stable IDs,
severity, exact references, and disposition requirements.

Do not treat legacy files under `specs/CHG-*`, prior GG-SAD evidence, or historical development
roadmaps as active development governance.
```

- [ ] **Step 3: Remove the obsolete startup prompt**

Run:

```powershell
git rm -- CLAUDE_CODE_PROJECT_START.md
```

Expected: only the obsolete CHG-001/GG-SAD-combination startup prompt is removed.

- [ ] **Step 4: Verify no active instruction still mandates GG-SAD development governance**

Run:

```powershell
rg -n "active change ID|DoF.*DoW.*DoD.*DoR|CHG-001|map.*evidence.md|GSD.*subordinate" AGENTS.md CLAUDE.md
```

Expected: no matches.

- [ ] **Step 5: Verify the authority statements are present**

Run:

```powershell
rg -n "leading source|sole development method|owner approval|independent review|GSD Core 1.10.0" AGENTS.md CLAUDE.md
```

Expected: matches identify the product authority, selected development method, and normative
approval boundary.

- [ ] **Step 6: Commit the instruction transition**

Run:

```powershell
git add -- AGENTS.md CLAUDE.md CLAUDE_CODE_PROJECT_START.md
git diff --cached --check
git commit -m "docs: switch development governance to GSD"
```

Expected: one commit modifying the two active instruction files and deleting the obsolete startup
prompt.

---

### Task 4: Onboard the retained repository into GSD

**Files:**

- Create through GSD: `.planning/PROJECT.md`
- Create through GSD: `.planning/REQUIREMENTS.md`
- Create through GSD: `.planning/ROADMAP.md`
- Create through GSD: `.planning/STATE.md`
- Create through GSD: `.planning/config.json`
- Create through GSD codebase mapping: `.planning/codebase/`
- Read as product authority: `docs/method/GG-SAD_normative_method_specification.md`
- Read as transition input: `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`

**Interfaces:**

- Consumes: GSD Core 1.10.0 and neutralized repository instructions.
- Produces: the sole active development context for all subsequent work.

- [ ] **Step 1: Start GSD existing-repository onboarding**

In Claude Code, run:

```text
/gsd-onboard
```

Provide this project statement when requested:

```text
Retain and audit the existing Python GG-SAD minimal-automation prototype. The English normative
specification is the leading product authority. GSD Core 1.10.0 is the sole development method.
The first milestone clarifies the normative specification without changing implementation
behavior, obtains repository-owner approval and independent Claude Code review, then audits the
retained implementation and changes only verified conformance gaps.
```

- [ ] **Step 2: Require codebase mapping before roadmap acceptance**

Ensure onboarding maps `src/ggsad/`, `tests/`, `pyproject.toml`, product resources, root `.ggsad`
assets, documentation, and legacy `specs/CHG-*` artifacts. Do not classify prior GG-SAD completion
claims as current requirements or verification evidence.

- [ ] **Step 3: Verify generated project authority and scope**

Run:

```powershell
rg -n "normative_method_specification.md|GSD Core 1.10.0|sole development method|retain|audit" .planning
rg -n "GSD.*subordinate|GG-SAD.*development method|CHG-001.*active" .planning
```

Expected: the first search matches project/requirements/roadmap content; the second search returns
no active-governance claims. Historical inventory references may mention CHG-001 only when clearly
labeled historical.

- [ ] **Step 4: Verify the first milestone sequence**

Inspect `.planning/ROADMAP.md` and require these ordered outcomes:

1. clarify the English normative specification;
2. obtain owner approval and independent Claude Code review;
3. classify and retire remaining legacy development governance;
4. correct quality-tool ownership boundaries;
5. audit retained implementation conformance;
6. implement only evidenced gaps;
7. run full verification.

Reject and regenerate the roadmap if it adds profile resolution, a full gate engine, memory, MCP,
web UI, CI integration, or multi-agent orchestration to this milestone.

- [ ] **Step 5: Run GSD health validation**

Run:

```powershell
node .claude\gsd-core\bin\gsd-tools.cjs validate health
```

Expected: status is `healthy`. If the exact 1.10.0 CLI requires the query form emitted by
`/gsd-health`, run `/gsd-health` and require the same `healthy` result; do not use repair mode until
the reported issue is understood.

- [ ] **Step 6: Confirm no product behavior changed**

Run:

```powershell
git diff main...HEAD -- src tests pyproject.toml uv.lock .ggsad specs/examples
uv run pytest
```

Expected: no product-code, test, dependency, lockfile, root product-resource, or example diff from
this bootstrap; all 150 current tests pass.

- [ ] **Step 7: Preserve a failed pre-commit onboarding for diagnosis**

If any check in Steps 3 through 6 fails, stop before committing. Preserve the uncommitted
`.planning/` files and command output for diagnosis. Do not reset, restore, clean, or delete them
automatically, and do not alter the completed GSD installer or instruction-transition commits.

- [ ] **Step 8: Commit GSD onboarding artifacts**

Run:

```powershell
git add -- .planning
git diff --cached --check
git commit -m "docs: onboard repository into GSD"
```

Expected: one commit containing only the generated and owner-accepted GSD development context.

---

### Task 5: Close the bootstrap and hand control to GSD

**Files:**

- Read: approved design and findings record
- Read: `.planning/PROJECT.md`
- Read: `.planning/REQUIREMENTS.md`
- Read: `.planning/ROADMAP.md`
- Read: `.planning/STATE.md`
- Modify through GSD only: `.planning/` status if onboarding workflow requires it

**Interfaces:**

- Consumes: completed Tasks 1 through 4.
- Produces: verified bootstrap state and a GSD-owned next action for normative clarification.

- [ ] **Step 1: Verify repository state**

Run:

```powershell
git status --short
git log --oneline -6
Get-Content -Raw .claude\gsd-core\VERSION
```

Expected: clean tree; separate commits for installer update, instruction transition, and GSD
onboarding; version `1.10.0`.

- [ ] **Step 2: Run the bootstrap verification set**

Run:

```powershell
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run pytest
uv build
```

Expected: all commands pass. Record `uv run ty check` separately as expected to remain blocked only
by installer-owned `.claude/scripts` diagnostics until GSD plans the ownership-scope correction.

- [ ] **Step 3: Roll back only a committed onboarding failure**

Perform this step only if Step 1 or Step 2 reveals a failure specifically caused by the committed
`.planning/` onboarding artifacts. Identify and verify the onboarding commit before reverting it:

```powershell
$onboardingCommit = git log -1 --format=%H -- .planning
git show --stat --oneline $onboardingCommit
git show --format=%s -s $onboardingCommit
```

Expected subject: `docs: onboard repository into GSD`. If the subject or changed paths do not
match the onboarding commit, stop and request direction. If they match, run:

```powershell
git revert --no-edit $onboardingCommit
```

Expected: a new revert commit removes only `.planning/` onboarding artifacts. Preserve the GSD
1.10.0 installer commit and instruction-transition commit, report the failure, and stop bootstrap
execution.

If Steps 1 and 2 pass, skip this rollback step.

- [ ] **Step 4: Identify the GSD next action**

In Claude Code, run:

```text
/gsd-progress --next
```

Expected: the next action discusses or plans the normative-clarification phase. It must not point
to a legacy GG-SAD change or CHG-001 closure action.

- [ ] **Step 5: Stop bootstrap execution**

Do not amend the normative specification from this bootstrap plan. Continue exclusively through
the GSD command and plan identified in Step 4.

---

## Independent plan-review dispositions

Claude Code reviewed commit `dd1aadd3c4f0fdc4a756c9574ba03020751887d7`. The repository owner and
Requestor dispositioned its findings on 2026-08-18:

| Finding | Disposition | Resulting action |
|---|---|---|
| PF-01 | Accepted | Expanded Task 4's protected-path diff to include `.ggsad` and `specs/examples`; corrected the review's step reference from Task 5 to Task 4. |
| PF-02 | Accepted with revised remedy | Added pre-commit preservation and post-commit targeted-revert procedures matching the actual onboarding commit boundary. |
| PF-03 | Accepted as informational | Added an npm package-name, version, repository, and integrity preflight before installation. |
