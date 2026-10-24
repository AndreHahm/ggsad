# Phase 1: Decision Record - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-10-24
**Phase:** 1-Decision Record
**Areas discussed:** Location and form, Entry content, Provenance and wording, Authority and change

---

## Location and form

| Option | Description | Selected |
|--------|-------------|----------|
| docs/decisions/ | New tracked directory outside .planning/; durable and citable | ✓ |
| docs/superpowers/specs/ | Beside the 2026-08 design document | |
| Phase directory | .planning/phases/01-decision-record/; archived at milestone end | |

**User's choice:** docs/decisions/. One file with 11 entries (alternative: index plus 11 files). Keep ids O-1..O-11 (alternative: new DEC-nn ids).

---

## Entry content

| Option | Description | Selected |
|--------|-------------|----------|
| Question, options, choice, consequences | Recommended | |
| Choice only | Minimum DEC-01 requires | |
| Full ADR | Context, options with pros and cons, choice, rationale, consequences, status | ✓ |

**User's choice:** Full ADR. O-4 departure stated plainly with the YAML reasoning. Consequences per entry: yes.
**Notes:** Interaction with the next area: rationale is limited to what the owner stated, so some fields may read "rationale not recorded".

---

## Provenance and wording

| Option | Description | Selected |
|--------|-------------|----------|
| Only what you stated | Quoted or closely paraphrased; "rationale not recorded" otherwise | ✓ |
| I draft, you correct | Requestor proposes rationale | |
| You supply it | Left blank for the owner | |

**User's choice:** Only what the owner stated. Self-contained record (alternative: link to the prototype repo). Owner reviews the diff, then a status line is set in a follow-up commit (alternative: final on commit).

---

## Authority and change

| Option | Description | Selected |
|--------|-------------|----------|
| Binding until superseded | Later phases implement it; deviation needs a new owner decision | ✓ |
| Informational | Context only | |

**User's choice:** Binding until superseded. Append, never edit (alternative: edit in place). Rely on existing O-n citations in requirements (alternative: add an orphan check).

---

## Claude's Discretion

File name, entry layout, status line display, wording of context and consequences.

## Deferred Ideas

An orphan check for O-n citations (possible Phase 8 verification item).
