# Independent review brief

## Your role

You are the independent Reviewer of a proposed change to a normative method specification. The Requestor is Claude Code from Anthropic. In your report, state in your own words which product, vendor and model you are. Review the text on its merits. You have been given no notes, plans, conclusions or earlier reviews and must not look for any. The repository owner has approved this exact text; that does not limit what you may report.

The project rule for changes to this specification reads:

Changes to the English normative specification require explicit repository-owner approval and independent review by a reviewer that is not the Requestor. A fresh context or subagent of the Requestor is not independent.

## Inputs

This file is BRIEF.md. Your working directory holds BRIEF.md and the four files below.

| File | Content | Expected SHA-256 |
|---|---|---|
| SPEC.md | The text under review | 09e9b65cf285939dfb53ba36f9077a71cadf1e1551a7aaaf89910baf386a3704 |
| BASE.md | The same text before the change | 3866078e946f9e7b2ee699aeaa4919182aea589d77405f71d51c944ff2713bd3 |
| DECISIONS.md | The repository owner's decisions O-1 to O-11, the standard the text is judged against | 0dc3d03d0434cad3e3e1155fedc72f7b9914b33b080c1306e354f83162da6b1b |
| REQUIREMENTS.md | The requirement texts SPEC-01 to SPEC-18 that the text is meant to satisfy; a reference of the form MAPPING P-nn inside them points to a document you do not have and is ignored | 3d9f49d61c6bdf6122459594f3145eb137f6b7233cbc5614c9b93c6beda22ac7 |

Compute the SHA-256 of the four files with a read-only tool and report each value in your report (write `not computed` for a value you could not compute). Use only these files. Open, search and read nothing else on the computer, and list in LIMITS any file you opened outside your working directory.

## What to evaluate

The subject is the difference between BASE.md and SPEC.md inside the scope of your pass; compare the two files yourself. Read unchanged text only as far as needed to judge changed text. Judge the text against this charter:

- C1 Contradiction and ambiguity: statements that cannot all hold together, a term used in two senses, a rule whose outcome cannot be determined from the text.
- C2 Owner decisions: each decision O-1 to O-11 of DECISIONS.md is implemented as chosen and none is contradicted; a decision with no corresponding text.
- C3 Requirements: each requirement SPEC-01 to SPEC-18 of REQUIREMENTS.md is satisfied by normative text and none is contradicted; content a requirement asks for that is missing.
- C4 Testability and bypass: rules that cannot be tested from outside, rules a hostile participant or agent could satisfy in letter while defeating their purpose, failure behaviour left unspecified.
- C5 Acceptance examples: an example that does not follow from its rule, contradicts it, or covers another case than the one it names.
- C6 Self-containment: text that cites development artifacts, prototype identifiers, identifiers of decisions or requirements of a project, tool names that are not part of the method, or local paths.
- C7 Weakening: a protection, MUST or SHOULD rule or prohibition of BASE.md that SPEC.md removes, relaxes or makes conditional without saying so.
- C8 References and terms: a wrong section number, example number or cross-reference; a term used without or before its definition.

## Severity scale

- BLOCKING: the text must not be treated as final until the finding is fixed or the repository owner dispositions it.
- MAJOR: a defect that an implementer or participant could plausibly act on incorrectly but that is not BLOCKING.
- MINOR: a defect of wording, structure or reference that cannot change what a conforming participant does.
- INFO: an observation or question that is not a defect.

Use BLOCKING for a contradiction, a conflict with an owner decision or a requirement text, a protection that can be bypassed, or a protection of BASE.md that is weakened; the repository owner, not the reviewer, decides what happens to a finding.

## Passes

| Pass | Scope | From | Up to |
|---|---|---|---|
| RG-A | The header and sections 1 to 8 | header | 9 |
| RG-B | Sections 9 to 22 | 9 | 23 |
| RG-C | Section 23 | 23 | 24 |
| RG-D | Section 24 up to the end of 24.5 | 24 | 24.6 |
| RG-E | Sections 24.6 to 24.10 and section 25 | 24.6 | end |
| RG-X | The whole text, read across sections | header | end |

From and Up to name headings of SPEC.md: `header` is the first line and `end` is the line after the last. A pass covers the text from its From heading up to, but not including, its Up to heading. Perform only the pass named in your start prompt. For RG-A to RG-E, report findings located in that range and consult the rest of the text only to judge it. For RG-X, read the whole text across sections, trace each owner decision and each requirement to the text that implements it, and look for conflicts between distant sections.

## Output format

Write the report with your file-writing tool as the single file `../out/REPORT-<PASS>.md` (with your pass id in the name; create it once and write it in full). The file holds the report and nothing else; your final message is not read. Use these labels, each at the start of a line, in this order:

- `REPORT BEGIN <PASS>`: the first line, with your pass id.
- `IDENTITY:` one line: product, vendor and model as you know them, and whether you share a session, prompt, notes or model with Claude Code.
- `INPUT SPEC.md <sha256>`, `INPUT BASE.md <sha256>`, `INPUT DECISIONS.md <sha256>` and `INPUT REQUIREMENTS.md <sha256>`: four lines, one per input file.
- `SCOPE:` the pass id and the range you were asked to cover.
- `COVERAGE:` the comma-separated numbers of the headings of SPEC.md you examined, numbers only (for example `1, 2, 2.1, 3`). The header (the text before the first numbered heading) is a part of a pass range but has no number, so it is never written in COVERAGE, not even as the word `header`.
- `FINDINGS:` either `none` or the number of findings.
- For each finding, in order: `FINDING <PASS>-<NNN>` (three digits, from 001), then `SEVERITY:` with one of the four severity words, then one to four `REFERENCE:` lines, then `SUMMARY:` (one single line of at most 200 characters; count the characters of each SUMMARY line before writing it and shorten any line over 200; as a rule of thumb, at most about 30 words), `REASONING:` (may continue on the following lines) and `DISPOSITION REQUIRED:` (what must happen, for example fix, clarify, owner decision; may continue on the following lines). A reference has the form `REFERENCE: file SPEC; section 24.3; lines 3401-3403; quote "text copied exactly"`: file is SPEC or BASE; the line part is always `lines A-B` with two numbers, never `line N`, and a reference to a single line repeats the number, as in `REFERENCE: file SPEC; section 1; lines 7-7; quote "text copied exactly"`; section is a heading number of that file or `header`; the quote is one fragment of one line, at most 160 characters, copied exactly and checked by a search, or the word `none` when the finding concerns missing text.
- `CHECKS PERFORMED:` followed by one statement for each of C1 to C8 (lines beginning `C1:` to `C8:`) saying what you did and what you found.
- `LIMITS:` what you could not do or did not verify, the tools you used and any file you opened outside your working directory.
- `VERDICT:` exactly `NO BLOCKING FINDINGS` or `BLOCKING FINDINGS PRESENT`.
- `REPORT END <PASS>`: the last line.

Example of the layout, with placeholders:

```
REPORT BEGIN <PASS>
IDENTITY: <product, vendor, model; shared session, prompt, notes or model with Claude Code: yes or no>
INPUT SPEC.md <sha256>
INPUT BASE.md <sha256>
INPUT DECISIONS.md <sha256>
INPUT REQUIREMENTS.md <sha256>
SCOPE: <pass id and range>
COVERAGE: <heading numbers>
FINDINGS: <none or the number of findings>
FINDING <PASS>-001
SEVERITY: <BLOCKING, MAJOR, MINOR or INFO>
REFERENCE: file SPEC; section 24.3; lines 3401-3403; quote "text copied exactly"
SUMMARY: <one line>
REASONING: <text>
DISPOSITION REQUIRED: <text>
CHECKS PERFORMED:
C1: <what you did and found>
C2: <what you did and found>
C3: <what you did and found>
C4: <what you did and found>
C5: <what you did and found>
C6: <what you did and found>
C7: <what you did and found>
C8: <what you did and found>
LIMITS: <text>
VERDICT: <NO BLOCKING FINDINGS or BLOCKING FINDINGS PRESENT>
REPORT END <PASS>
```

## Rules for this review

- Read-only apart from the report: modify and delete no file, and create no file except `../out/REPORT-<PASS>.md`.
- Attempt nothing that this brief does not ask for. A refused action or tool call ends your session without any report, so prefer the Read tool, finish the whole analysis first, then create the report file in one step, and do not attempt any action that this brief forbids.
- No network access. Use only the Read, Grep and Glob tools and, if you need a command, one single plain command per call from this list: `ls`, `cat`, `head`, `tail`, `wc`, `grep`, `diff`, `sha256sum` (on Windows `certutil -hashfile` or `Get-FileHash`). Never use a pipe, a redirect, a command chain (`&&`, `;`, `||`), a substitution or any other command.
- The vertical bar character appears nowhere in your report. Use no absolute paths and no tab characters.
- A continuation line never begins with one of the label words above followed by a colon.
- One finding per defect, never merged. No padding.
- Say `FINDINGS: none` only when CHECKS PERFORMED shows what you examined.
- If you cannot complete the pass, say so in LIMITS rather than guess.

## Start prompt

Read BRIEF.md in this directory and carry out pass <PASS> exactly as it describes. Create the file ../out/REPORT-<PASS>.md holding the report in the format BRIEF.md defines and nothing else; your final message is not read.
