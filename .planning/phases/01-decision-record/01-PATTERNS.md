# Phase 1: Decision Record - Pattern Map

**Mapped:** 2026-10-24
**Files analyzed:** 1 (new, documentation only)
**Analogs found:** 2 partial / 1 (no ADR/decision-record analog exists in the repo)

## File Classification

| New File | Role | Data Flow | Closest Analog | Match Quality |
|----------|------|-----------|----------------|---------------|
| `docs/decisions/2026-10-23-executable-core-decisions.md` (name is planner's choice) | governance document (decision record, 11 ADR entries) | static reference, cited by id (O-n) from requirements and later specs | `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md` (status block, numbered owner decisions); `.planning/reviews/2026-10-24-reviewer-rule-amendment.md` (self-contained evidence note, field table) | role-match (partial, two analogs) |

## Pattern Assignments

### `docs/decisions/<date>-<slug>.md` (governance document, reference)

**Analog 1:** `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`

**Title and status block** (lines 1-21): H1 title, `## Status and authority`, then a plain bullet list of `- Key: value` lines. No YAML front matter. Wrapped at about 100 columns with continuation lines indented two spaces.
```markdown
# Normative Baseline Clarification and GSD Transition Design

## Status and authority

- Status: Approved
- Date: 2026-08-18
- Requestor: Codex
- Decision owner: repository owner
- Independent reviewer: Claude Code
...
- Final approval record: The repository owner explicitly approved reviewed design revision
  `c3b0a30` in the Codex review session on 2026-08-18 after ...
```
Then a one-paragraph statement of what the document does and does not do (lines 20-21: "This document designs the transition. It does not itself amend ..."). Copy this for the record's scope sentence (does not draft normative text, change `src/ggsad/`, or alter requirements).

**Numbered owner decisions** (lines 23-39):
```markdown
## Owner-confirmed governing decisions

The repository owner confirmed these decisions during the clarification sequence. ...

1. `docs/method/GG-SAD_normative_method_specification.md` is the leading document.
2. ...
```
Section headings are `##`, subsections `###`, sentence-case headings, no heading numbering in the doc title. Decision text is plain statements.

**Analog 2:** `.planning/reviews/2026-10-24-reviewer-rule-amendment.md` (self-contained, tracked evidence note)

**Metadata table** (lines 3-11): `| Field | Value |` / `|---|---|`, values in backticks for ids/paths, an explicit Verdict row. Use the same two-column table for per-entry or record-level metadata (decision date 2026-10-23, confirmation date, source `ggsad-core-proto` commit `058d6c0`, status).
```markdown
| Field | Value |
|---|---|
| Owner approval | Given by the repository owner for the exact diff before review (...) |
| Verdict | ACCEPT. No findings. |
```
**Quoted source** (lines 13-15): intro sentence "The reviewer's final report, unedited:" followed by `>` blockquote. Use for verbatim owner wording from the proposal (D-07).
**Closing disclaimer** (line 49): "This note is evidence only. It does not change the reviewed files." Mirror with "This record does not change the normative specification" style closer.
**Notes section** (lines 43-47): `## Requestor notes` bullet list. A "Requestor notes" section is the place for "rationale not recorded" caveats and owner-review remarks.

### Suggested ADR entry layout (planner's discretion, derived from conventions above)
No existing ADR in the repo. Keep to the repo's idioms: `### O-4: <title>` under `## Decisions`, then bold or bullet labels (`- Status:`, `- Context:`, `- Options considered:`, `- Chosen:`, `- Rationale:`, `- Consequences:`) in the same `- Key: value` style as the status block, or a per-entry `| Field | Value |` table. Use the literal strings from CONTEXT: status "Proposed wording" (D-09), "rationale not recorded" (D-07), "Superseded by" (D-11).

## Shared Patterns / Conventions for a New Governance Document

- **Language:** English throughout (the German specification was removed; D-08 self-contained).
- **File naming:** `YYYY-MM-DD-kebab-case-slug.md`, matching `docs/superpowers/specs/2026-08-18-normative-baseline-and-gsd-transition-design.md`, `docs/superpowers/plans/2026-08-18-gsd-bootstrap-transition.md`, `.planning/reviews/2026-10-24-reviewer-rule-amendment.md`. Companion files use a `-findings` suffix. Exceptions (`.planning/milestones/PR-3-REBASE-SHA-RECONCILIATION.md`, `v1.0-*`) are uppercase milestone records, not a pattern to follow.
- **Front matter:** none in any docs/spec/review file. Use H1 + status bullets or a table.
- **Dates:** ISO `YYYY-MM-DD` everywhere.
- **Tables vs lists:** tables for metadata/field-value (reviews note, PR-3 reconciliation record); bullet lists for status/authority; numbered lists for ordered decisions; `>` blockquote for verbatim quotes. Ids, paths, commit hashes in backticks.
- **Commit-hash rule:** do not cite hashes of this repository (rebase merges rewrite them; see `.planning/milestones/PR-3-REBASE-SHA-RECONCILIATION.md` lines 1-8, which records that exact problem). The prototype's `058d6c0` is acceptable.
- **Line endings and encoding:** `.gitattributes` sets `* text=auto eol=lf`; `git ls-files --eol` shows `i/lf w/lf` for README.md. Commit LF, UTF-8, no BOM. (A working-tree grep may show CRLF on some Windows checkouts; the index is LF.) Hard-wrap at about 100 columns in specs; the review note uses long unwrapped lines, so either is accepted.
- **How prior decisions are cited:** by stable ids (O-n, DEC-01, SPEC-nn, F-01 for findings) and by repo-relative backticked paths. `.planning/REQUIREMENTS.md` already cites O-1..O-11 (for example SPEC-12 cites O-1, SPEC-15 cites O-4) and line 3 states "owner decisions O-1 to O-11 were made 2026-10-23".
- **Commits:** small conventional `docs:` commits; status flip to "Decided (owner-confirmed <date>)" is a separate follow-up commit (D-09).

## Indexing / Linking Points for a New `docs/decisions/` Directory (observation only, no change proposed)

- There is no `docs/README.md` or docs index.
- `README.md` lines 55-68 contain a "Repository layout" fenced `text` tree listing `docs/method/` only (with the spec file); `docs/superpowers/` is not listed either, so a new `docs/decisions/` would not be listed unless the tree is edited.
- `README.md` lines 36-45 ("Repository Authority and Development Method") link the spec, `AGENTS.md` and `.planning/`; no decision-record link.
- `AGENTS.md` references only `docs/method/...`; no docs index.
- `.planning/PROJECT.md` Key Decisions table and `.planning/ROADMAP.md`/`REQUIREMENTS.md` (DEC-01) reference the record by concept, not path, so they will need no path updates unless the owner wants it.

## No Analog Found

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| ADR-style entry layout (context/options/chosen/rationale/consequences/status) | decision record | reference | No ADR or `docs/decisions/` exists in the repo; the entry layout must be composed from the status-block and field-table idioms above. |

## Metadata

**Analog search scope:** `docs/`, `docs/superpowers/{specs,plans}`, `.planning/{reviews,milestones}`, `README.md`, `AGENTS.md`, `.gitattributes`
**Files scanned:** about 12
**Pattern extraction date:** 2026-10-24
