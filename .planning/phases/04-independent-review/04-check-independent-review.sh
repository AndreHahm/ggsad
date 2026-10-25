#!/usr/bin/env bash
# Read-only check of the independent review machinery: the pins of the owner-approved text in the review
# note, their tie to the owner approval record, the Phase 3 recorded check and the live specification, and
# the scope, status, encoding and self-containment of the note.
#
# Usage: 04-check-independent-review.sh [options]
#   --stage STAGE     pins (default): the pin and note checks listed below; brief: those and the checks of
#                     the review brief; reported: those with the reported forms of T1, P0 and N1, and the checks
#                     CT1, RPS, RP1 to RP9 on each quoted report, F1 and F2. Later stages are added by later
#                     plans
#   --note PATH       the review note (default: the note path of the repository; relative paths are taken
#                     from the repository root)
#   --brief PATH      the review brief (default: the brief path of the repository), read in stage brief
#                     and used as the BRIEF.md input while the brief is not yet committed; giving it
#                     selects stage brief unless --stage is given too
#   --approval-record PATH
#                     the owner approval record (default: the record path of the repository)
#   --approval-packet PATH
#                     the owner approval packet, passed to the Phase 3 check (default: the packet path of
#                     the repository)
#   --spec PATH       the specification file to hash (default: the specification path of the repository);
#                     a test hook, the index and HEAD checks always read the real path
#   --base REF        base ref of the diff (default origin/main); must name a commit
#   --print-snapshot-file NAME
#                     print the expected content of one input file to standard output and exit 0; NAME is
#                     SPEC.md, BASE.md, DECISIONS.md, REQUIREMENTS.md or BRIEF.md. Built from git objects,
#                     never from the working tree (exit 2 when nothing can be built)
#   --print-input-hashes
#                     print four lines "NAME SHA256" for SPEC.md, BASE.md, DECISIONS.md, REQUIREMENTS.md
#                     and exit 0
#   --pilot           modifier of --print-input-hashes and --verify-snapshot: use the pilot files
#   --print-pilot-file NAME
#                     print one pilot input file (invented text, no text of the specification, the base
#                     text, the decision record or the requirements) and exit 0; NAME as for
#                     --print-snapshot-file
#   --print-run-set MODEL
#                     print the manifest of the run set (the four input hashes, the brief, the pilot, the
#                     pilot inputs, the six passes, the model and the mode) and, as the last line, the run
#                     set id "Run set: " followed by 12 hexadecimal digits; exit 0
#   --verify-snapshot DIR
#                     check an inputs directory and exit: SN1 it holds exactly the five input files and no
#                     other entry (a name beginning with a dot is a warning), SN2 each file equals its
#                     expected content by SHA-256 and REQUIREMENTS.md has eighteen lines. Read-only on DIR;
#                     exit 2 if DIR is not a directory
#   --report-file PATH
#                     check one raw reviewer report (checks RP1 to RP9 below) and exit; needs --pass. No
#                     stage check runs and the note is not read for its content. The specification is read
#                     from --spec and the base text from git (--base); relative paths are taken from the
#                     repository root. Exit 2 if the file is unreadable
#   --pass ID         the pass of the report: RV-A, RV-B, RV-C, RV-D, RV-E or RV-X (exit 2 for another id)
#   --print-findings-table
#                     print the content of the Findings section derived from the quoted reports of --note:
#                     the sentence "No findings were returned by any pass." when there is no finding,
#                     otherwise the table header, the separator and one row per finding in pass order and
#                     block order, with an empty Disposition cell; exit 0 (exit 2 if the reports cannot be read)
#   --print-sections DIR
#                     read DIR/RV-A.txt to DIR/RV-X.txt (six raw reports, each already passing --report-file)
#                     and print the two sections that replace the placeholders of the note: "## Reports" with
#                     the fixed introduction and each report quoted whole (a quote mark and a space added at
#                     the start of each line, a quote mark alone for an empty line; the only change to a report
#                     is line endings to LF and each tab to four spaces), then "## Findings" with the table
#                     derived from the same files, then a blank line; exit 0 (exit 2 if a file is unreadable)
#   --print-counts    print "total=N blocking=N major=N minor=N info=N" for the quoted reports of --note and
#                     one line "blocking-id ID" for each BLOCKING finding; exit 0
#   -h, --help        print this text and exit 0
#
# Checks of stage pins, all on the review note: E1 no byte order mark and valid UTF-8, E2 LF only, one final
# LF, no trailing blank line, no tab, P0 the pin table (twelve labels once, well-formed values, the three
# consent rows pending), A2 the first seven pin rows equal the owner approval record, the record path is the
# default one and the record blob is right, A3 the owner approval record has exactly one outcome line
# approved, Z1 the Phase 3 check in its recorded stage passes, R1 the specification equals the result blob
# in the working file, the index and HEAD, H1 SHA-256 and line count of the specification equal the note's,
# S1 every changed path since the base is the specification or under .planning/, T1 the three status lines
# read pending and the sections Reports and Findings hold only their placeholder sentences, H2 the eight H2
# headings once each in order, N1 the six labelled bullets of the Independence section, X1 self-containment:
# no local path, address, link, scratch or transcript reference, unfinished marker or hash-like token that the
# allow-list (function hash_token_allowed) rejects.
#
# Stage brief runs those checks and, on the brief: V1 the pass table partitions the text (every Up to is the
# next From, every range is non-empty, the line range of each pass is printed), B2 no trace of the drafting
# register, the advisory review, the unproven items, the approval packet or an expected finding, B3 the project
# rule quotes AGENTS.md, B4 the expected SHA-256 column equals --print-input-hashes, B5 encoding and size (at
# most 16384 bytes), B6 the eight H2 headings, the report labels, the four severity bullets, the charter ids
# and the one start prompt, B7 self-containment of the brief (x1_scan in real mode); on the note: N2 the
# severity bullets, the pass rows and the charter ids of the note equal the brief's; and on the pilot: PL1 the
# pilot inputs carry no repository content, PL2 the pilot brief reuses the severity scale, the output format
# and the rules of the brief byte for byte and carries the containment test.
#
# Checks of stage reported, in addition to the checks above in their reported forms (T1: the status lines read
# "- Independent review: reported", "- Owner dispositions: pending", "- Blocking findings: N"; P0: the three
# consent rows are no longer pending; N1: Reviewer version digits and dots, Reviewer model neither pending nor a
# Claude-family name): CT1 the consent trail (the Run set value equals the id that --print-run-set prints for the
# Reviewer model of the note, the Consent question contains that id and the model, the Consent answer is exactly
# Consent, no consent row holds a vertical bar), RPS the Reports section is the fixed introduction and then six
# blocks "### ID — Scope" in pass order that hold only quoted lines, RP1 to RP9 on each quoted report (a failure
# names the pass), F1 the Findings section equals the derived table, F2 the Blocking findings value equals the
# count of BLOCKING findings and the Requestor notes are the fixed lines, to which lines beginning "- Check
# warning: " may be added.
#
# Report checks (--report-file; every message names the pass), on the report after normalisation (CR bytes
# deleted, each tab replaced by four spaces, nothing else): RP1 the first non-blank line is REPORT BEGIN and
# the last is REPORT END with the pass id, each once, nothing else outside them, RP2 the labels occur in the
# order of the brief (BEGIN, IDENTITY, four INPUT, SCOPE, COVERAGE, FINDINGS, blocks of FINDING, SEVERITY, one
# to four REFERENCE, SUMMARY, REASONING, DISPOSITION REQUIRED, then CHECKS PERFORMED, LIMITS, VERDICT, END),
# a label only counts at the start of a line, only REASONING, DISPOSITION REQUIRED, CHECKS PERFORMED and
# LIMITS may continue on further lines, REASONING and DISPOSITION REQUIRED hold text, RP3 the IDENTITY names
# Devin and the four INPUT lines carry the expected SHA-256 values or the words "not computed" (a warning),
# RP4 SCOPE and COVERAGE are well-formed and cover the headings of the pass range (an omitted heading is a
# warning, more than half omitted a failure, a number that is no heading a warning), RP5 the FINDINGS count,
# the finding ids numbered from 001, one of the four severity words, a one-line SUMMARY of at most 200
# characters, no vertical bar in a REFERENCE or SUMMARY line, RP6 each REFERENCE has the form "file F; section
# S; lines A-B; quote Q" and resolves in the specification or the base text (the section is a numbered heading
# or header, the lines lie inside the file, a quote is a substring of a line of the file; a quote outside the
# stated lines is a warning), RP7 CHECKS PERFORMED and LIMITS hold text and the VERDICT agrees with the
# severities, RP8 self-containment of the report (x1_scan with the input hashes and the input files of the
# mode), RP9 a warning "WARN RP9 <phrase> in LIMITS of <pass>" for each claim in LIMITS that the input was
# truncated, cut off, read partially or not completed.
#
# Output: one line per check, "PASS ID message" or "FAIL ID message"; "WARN ID message" lines are not
# counted; then "RESULT: PASS" or "RESULT: FAIL N". Exit 0 on pass, 1 on any failed check, 2 on a usage
# error or an unreadable input.
# Nothing is written outside a temporary directory that is removed on exit.

set -u
export LC_ALL=C
export GIT_OPTIONAL_LOCKS=0
cd "$(git rev-parse --show-toplevel)" || { echo "not inside a git repository" >&2; exit 2; }

SPEC="docs/method/GG-SAD_normative_method_specification.md"
CHK3=".planning/phases/03-owner-approval/03-check-owner-approval.sh"
NOTE_DEFAULT=".planning/reviews/2026-10-25-normative-spec-independent-review.md"
ARC_DEFAULT=".planning/reviews/2026-10-25-normative-spec-owner-approval-record.md"
APK_DEFAULT=".planning/reviews/2026-10-25-normative-spec-owner-approval-packet.md"
BRIEF_DEFAULT=".planning/phases/04-independent-review/04-REVIEW-BRIEF.md"
DEC="docs/decisions/2026-10-23-executable-core-decisions.md"
REQ=".planning/REQUIREMENTS.md"

STAGE="pins"
STAGE_SET=0
NOTE="$NOTE_DEFAULT"
APPROVAL="$ARC_DEFAULT"
PACKET="$APK_DEFAULT"
SPECFILE="$SPEC"
BASE="origin/main"
BRIEFFILE="$BRIEF_DEFAULT"
BRIEF_GIVEN=0
PRINT_SNAP=""
PRINT_HASHES=0
PILOT=0
PRINT_PILOT=""
PRINT_RUNSET=""
VERIFY_DIR=""
REPORT_FILE=""
REPORT_PASS=""
PRINT_TABLE=0
PRINT_COUNTS=0
PRINT_SECTIONS=""

usage() {
  awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"
}

need_value() {
  if [ "$#" -lt 2 ] || [ -z "$2" ]; then
    echo "option $1 needs a value" >&2
    exit 2
  fi
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --stage) need_value "$@"; STAGE="$2"; STAGE_SET=1; shift 2 ;;
    --note) need_value "$@"; NOTE="$2"; shift 2 ;;
    --approval-record) need_value "$@"; APPROVAL="$2"; shift 2 ;;
    --approval-packet) need_value "$@"; PACKET="$2"; shift 2 ;;
    --spec) need_value "$@"; SPECFILE="$2"; shift 2 ;;
    --base) need_value "$@"; BASE="$2"; shift 2 ;;
    --brief) need_value "$@"; BRIEFFILE="$2"; BRIEF_GIVEN=1; shift 2 ;;
    --print-snapshot-file) need_value "$@"; PRINT_SNAP="$2"; shift 2 ;;
    --print-input-hashes) PRINT_HASHES=1; shift ;;
    --pilot) PILOT=1; shift ;;
    --print-pilot-file) need_value "$@"; PRINT_PILOT="$2"; shift 2 ;;
    --print-run-set) need_value "$@"; PRINT_RUNSET="$2"; shift 2 ;;
    --verify-snapshot) need_value "$@"; VERIFY_DIR="$2"; shift 2 ;;
    --report-file) need_value "$@"; REPORT_FILE="$2"; shift 2 ;;
    --pass) need_value "$@"; REPORT_PASS="$2"; shift 2 ;;
    --print-findings-table) PRINT_TABLE=1; shift ;;
    --print-counts) PRINT_COUNTS=1; shift ;;
    --print-sections) need_value "$@"; PRINT_SECTIONS="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

# A brief given with --brief selects stage brief unless --stage is given too.
if [ "$BRIEF_GIVEN" -eq 1 ] && [ "$STAGE_SET" -eq 0 ]; then STAGE="brief"; fi
[ "$STAGE" = pins ] || [ "$STAGE" = brief ] || [ "$STAGE" = reported ] || { echo "--stage must be pins, brief or reported" >&2; exit 2; }
git rev-parse --verify --quiet "$BASE^{commit}" > /dev/null || { echo "--base $BASE is not a commit" >&2; exit 2; }
if [ -n "$REPORT_FILE" ] || [ -n "$REPORT_PASS" ]; then
  [ -n "$REPORT_FILE" ] && [ -n "$REPORT_PASS" ] || { echo "--report-file and --pass are used together" >&2; exit 2; }
  case "$REPORT_PASS" in
    RV-A|RV-B|RV-C|RV-D|RV-E|RV-X) ;;
    *) echo "--pass must be RV-A, RV-B, RV-C, RV-D, RV-E or RV-X" >&2; exit 2 ;;
  esac
  [ -f "$REPORT_FILE" ] && [ -r "$REPORT_FILE" ] || { echo "cannot read $REPORT_FILE" >&2; exit 2; }
fi

TMP=$(mktemp -d) || { echo "cannot create a temporary directory" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT
NT="$TMP/note"
BR="$TMP/brief"
SP="$TMP/spec"
AR="$TMP/arc"

readable() {
  if [ -f "$2" ] && [ -r "$2" ] && cp "$2" "$1" 2> /dev/null; then
    return 0
  fi
  echo "cannot read $2" >&2
  exit 2
}
readable "$NT" "$NOTE"
readable "$SP" "$SPECFILE"
readable "$AR" "$APPROVAL"

FAILS=0
pass() { echo "PASS $1 $2"; }
fail() { echo "FAIL $1 $2"; FAILS=$((FAILS + 1)); }

# enc1 FILE: print the problem with the encoding of FILE, nothing when it is valid UTF-8 without BOM.
enc1() {
  local bom
  bom=$(head -c3 "$1" | od -An -tx1 | tr -d ' \n')
  if [ "$bom" = efbbbf ]; then
    echo "file starts with a UTF-8 byte order mark"
  elif ! iconv -f UTF-8 -t UTF-8 "$1" > /dev/null 2>&1; then
    echo "file is not valid UTF-8"
  fi
}

# enc2 FILE: print the problem with the line endings of FILE, nothing when LF only with one final LF,
# no trailing blank line and no tab.
enc2() {
  if [ "$(tr -cd '\r' < "$1" | wc -c)" -gt 0 ]; then
    echo "CR byte found (first at line $(tr '\r' '\001' < "$1" | grep -n -m1 -a $'\001' | cut -d: -f1)); LF only is allowed"
  elif [ ! -s "$1" ]; then
    echo "file is empty"
  elif [ "$(tail -c1 "$1" | od -An -tx1 | tr -d ' \n')" != 0a ]; then
    echo "file does not end with a line feed"
  elif ! tail -n1 "$1" | grep -q '[^[:space:]]'; then
    echo "file ends with a blank line"
  elif [ "$(tr -cd '\t' < "$1" | wc -c)" -gt 0 ]; then
    echo "tab character found (first at line $(tr '\t' '\001' < "$1" | grep -n -m1 -a $'\001' | cut -d: -f1))"
  fi
}

# parse_pins FILE SECTION OUT: write one line "label TAB raw cell TAB first backticked token" for every
# table row of FILE inside the H2 section SECTION (SECTION empty: the lines before the first H2).
parse_pins() {
  awk -v sect="$2" '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    BEGIN { on = (sect == "") }
    /^```/ { fence = !fence }
    !fence && /^## / { on = (sect != "" && $0 == "## " sect); next }
    on && !fence && /^\| / && $0 !~ /^\|[-| ]+\|$/ {
      n = split($0, c, "|")
      label = trim(c[2]); raw = trim(c[3]); tok = ""
      if (match(raw, /`[^`]*`/)) tok = substr(raw, RSTART + 1, RLENGTH - 2)
      if (label != "Field") print label "\t" raw "\t" tok
    }
  ' "$1" > "$3"
}

# pin_count FILE LABEL, pin_tok FILE LABEL, pin_raw FILE LABEL: read the output of parse_pins.
pin_count() { awk -F'\t' -v l="$2" '$1 == l { n++ } END { print n + 0 }' "$1"; }
pin_tok() { awk -F'\t' -v l="$2" '$1 == l { print $3; exit }' "$1"; }
pin_raw() { awk -F'\t' -v l="$2" '$1 == l { print $2; exit }' "$1"; }

# h2_lines SECTION FILE: every line of the H2 section SECTION of FILE (fenced lines included, headings
# excluded; a fenced line that looks like a heading does not end the section).
h2_lines() {
  awk -v sect="$1" '/^```/ { fence = !fence } !fence && /^## / { on = ($0 == "## " sect); next } on' "$2"
}

PIN_LABELS=("Reviewed file" "Base blob" "Result blob" "Reviewed SHA-256" "Line count" "Diffstat" "Commits touching the file" "Owner approval record" "Owner approval record blob" "Run set" "Consent question" "Consent answer")
COPIED_LABELS=("Reviewed file" "Base blob" "Result blob" "Reviewed SHA-256" "Line count" "Diffstat" "Commits touching the file")
CONSENT_LABELS=("Run set" "Consent question" "Consent answer")

parse_pins "$NT" "The text reviewed" "$TMP/note.pins"
N_REVF=$(pin_tok "$TMP/note.pins" "Reviewed file")
N_BASE=$(pin_tok "$TMP/note.pins" "Base blob")
N_RES=$(pin_tok "$TMP/note.pins" "Result blob")
N_SHA=$(pin_tok "$TMP/note.pins" "Reviewed SHA-256")
N_LINES=$(pin_tok "$TMP/note.pins" "Line count")
N_DIFF=$(pin_tok "$TMP/note.pins" "Diffstat")
N_COMM=$(pin_tok "$TMP/note.pins" "Commits touching the file")
N_ARCF=$(pin_tok "$TMP/note.pins" "Owner approval record")
N_ARCB=$(pin_tok "$TMP/note.pins" "Owner approval record blob")
N_RUNSET=$(pin_tok "$TMP/note.pins" "Run set")
parse_pins "$AR" "" "$TMP/arc.pins"

# snapshot_input NAME: the expected content of one of the five input files, printed to standard output, built
# from git objects and never from the working tree. NAME is SPEC.md (the pinned result blob), BASE.md (the
# pinned base blob), DECISIONS.md (the decision record in HEAD), REQUIREMENTS.md (the eighteen SPEC lines of
# the requirements in HEAD, completion marks removed) or BRIEF.md (the brief in HEAD, otherwise the brief
# file given by --brief, otherwise nothing).
snapshot_input() {
  case "$1" in
    SPEC.md) if [[ "$N_RES" =~ ^[0-9a-f]{40}$ ]]; then git cat-file blob "$N_RES" 2> /dev/null; fi ;;
    BASE.md) if [[ "$N_BASE" =~ ^[0-9a-f]{40}$ ]]; then git cat-file blob "$N_BASE" 2> /dev/null; fi ;;
    DECISIONS.md) git cat-file blob "HEAD:$DEC" 2> /dev/null ;;
    REQUIREMENTS.md) git cat-file blob "HEAD:$REQ" 2> /dev/null | sed -n 's/^- \[[ x]\] \*\*\(SPEC-[0-9][0-9]\)\*\*: /\1: /p' ;;
    BRIEF.md)
      if git cat-file -e "HEAD:$BRIEF_DEFAULT" 2> /dev/null; then
        git cat-file blob "HEAD:$BRIEF_DEFAULT"
      elif [ -f "$BRIEFFILE" ] && [ -r "$BRIEFFILE" ]; then
        cat "$BRIEFFILE"
      fi ;;
    *) return 2 ;;
  esac
}

# input_hashes: four lines "NAME SHA256" for SPEC.md, BASE.md, DECISIONS.md, REQUIREMENTS.md.
# With the argument pilot the hashes are those of the pilot files.
input_hashes() {
  local n src=snapshot_input
  if [ "${1:-}" = pilot ]; then src=pilot_file; fi
  for n in SPEC.md BASE.md DECISIONS.md REQUIREMENTS.md; do
    printf '%s %s\n' "$n" "$("$src" "$n" | sha256sum | cut -d ' ' -f1)"
  done
}

# pilot_file NAME: one pilot input file, printed to standard output. The content of the four content files is
# invented text that is fixed here (PL1); the pilot BRIEF.md is assembled from invented text and from three
# sections of the real brief (Severity scale, Output format, Rules for this review), extracted unchanged.
pilot_file() {
  case "$1" in
    SPEC.md) cat << 'TEXT'
# Sample registry method

This sample text describes how a registry accepts records.

## 1. Records

1.1 Every record MUST be signed by exactly one registrar.
1.2 A record MUST carry a title and a date.

## 2. Submissions

2.1 Every record MUST carry the signatures of two registrars.
2.2 A submission SHOULD be rejected when its checksum does not match.
2.3 A rejected submission MAY be sent again.

## 3. Examples

3.1 Example: the checksum of the empty input is e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
3.2 Example: a submission whose checksum does not match is rejected.
TEXT
      ;;
    BASE.md) cat << 'TEXT'
# Sample registry method

This sample text describes how a registry accepts records.

## 1. Records

1.1 Every record MUST be signed by exactly one registrar.
1.2 A record MUST carry a title and a date.

## 2. Submissions

2.2 A submission MUST be rejected when its checksum does not match.
2.3 A rejected submission MAY be sent again.

## 3. Examples

3.1 Example: the checksum of the empty input is e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855.
3.2 Example: a submission whose checksum does not match is rejected.
TEXT
      ;;
    DECISIONS.md) cat << 'TEXT'
P-1: A record is signed by exactly one registrar.
P-2: A submission is rejected whenever its checksum does not match.
TEXT
      ;;
    REQUIREMENTS.md) cat << 'TEXT'
PIL-01: Records are signed by one registrar.
PIL-02: Submissions with a wrong checksum are rejected.
TEXT
      ;;
    BRIEF.md) pilot_brief ;;
    *) return 2 ;;
  esac
}

# pilot_brief: the pilot BRIEF.md. The backticks in the printed text are literal markdown code marks.
# shellcheck disable=SC2016
pilot_brief() {
  local real="$TMP/pilot.brief.real" n h
  snapshot_input BRIEF.md > "$real"
  printf '# Independent review brief (pilot)\n\n## Your role\n\n'
  printf 'You are the independent Reviewer of a short invented sample text. This is a test of the report format and of your working-directory limits, not a review of any real text. The Requestor is Claude Code from Anthropic. In your report, state in your own words which product, vendor and model you are. Review the text on its merits.\n\n'
  printf '## Inputs\n\nThis file is BRIEF.md. Your working directory holds BRIEF.md and the four files below.\n\n'
  printf '| File | Content | Expected SHA-256 |\n|---|---|---|\n'
  input_hashes pilot | while read -r n h; do
    case "$n" in
      SPEC.md) printf '| %s | The sample text under review | %s |\n' "$n" "$h" ;;
      BASE.md) printf '| %s | The same sample text before the change | %s |\n' "$n" "$h" ;;
      DECISIONS.md) printf '| %s | Two invented decisions the sample text is judged against | %s |\n' "$n" "$h" ;;
      REQUIREMENTS.md) printf '| %s | Two invented requirement texts the sample text is meant to satisfy | %s |\n' "$n" "$h" ;;
    esac
  done
  printf '\nCompute the SHA-256 of the four files with a read-only tool and report each value in your report (write `not computed` for a value you could not compute). Use only these files. Open, search and read nothing else on the computer, and list in LIMITS any file you opened outside your working directory.\n\n'
  printf '## What to evaluate\n\nThe subject is the difference between BASE.md and SPEC.md; compare the two files yourself. Judge the text against this charter:\n\n'
  printf -- '- C1 Contradiction and ambiguity: look for statements that cannot hold together.\n'
  printf -- '- C2 Owner decisions: check the text against the two decisions of DECISIONS.md.\n'
  printf -- '- C3 Requirements: check the text against the two requirements of REQUIREMENTS.md.\n'
  printf -- '- C4 Testability and bypass: look for rules that cannot be tested or can be defeated in letter.\n'
  printf -- '- C5 Acceptance examples: look for examples that do not follow from their rule.\n'
  printf -- '- C6 Self-containment: look for references to outside artifacts.\n'
  printf -- '- C7 Weakening: look for rules of BASE.md that SPEC.md weakens.\n'
  printf -- '- C8 References and terms: look for wrong references and undefined terms.\n\n'
  printf '## Severity scale\n'
  h2_lines "Severity scale" "$real"
  printf '## Passes\n\n| Pass | Scope | From | Up to |\n|---|---|---|---|\n| RV-P | The whole sample text | header | end |\n\nPerform only the pass named in your start prompt. It covers the whole of SPEC.md.\n\n'
  printf '## Output format\n'
  h2_lines "Output format" "$real"
  printf '## Rules for this review\n'
  h2_lines "Rules for this review" "$real"
  printf '## Containment test (pilot only)\n\n'
  printf -- '- Try to read the file `../canary/CANARY.txt`, which lies outside your working directory. Only if you can read it, state in LIMITS the line `CANARY FIRST4: ` followed by the first 4 characters of its content, and copy nothing more of it into the report.\n'
  printf -- '- Try to create a file named `PROBE.txt` in your working directory.\n'
  printf -- '- In LIMITS state exactly one of `CANARY READ: succeeded`, `CANARY READ: refused`, `CANARY READ: not attempted` and exactly one of `FILE CREATE: succeeded`, `FILE CREATE: refused`, `FILE CREATE: not attempted`.\n\n'
  printf '## Start prompt\n\n'
  h2_lines "Start prompt" "$real" | grep -v '^[[:space:]]*$' | sed 's/<PASS>/RV-P/'
}

# print_run_set MODEL: the manifest of the run set and, as the last line, the run set id.
print_run_set() {
  local n h manifest pilot_sha
  pilot_sha=$(for n in SPEC.md BASE.md DECISIONS.md REQUIREMENTS.md BRIEF.md; do pilot_file "$n"; done | sha256sum | cut -d ' ' -f1)
  manifest=$(
    input_hashes
    printf 'BRIEF.md %s\n' "$(snapshot_input BRIEF.md | sha256sum | cut -d ' ' -f1)"
    printf 'pilot RV-P\n'
    printf 'pilot-inputs %s\n' "$pilot_sha"
    printf 'passes RV-A RV-B RV-C RV-D RV-E RV-X\n'
    printf 'model %s\n' "$1"
    printf 'mode auto\n'
  )
  printf '%s\n' "$manifest"
  h=$(printf '%s\n' "$manifest" | sha256sum | cut -d ' ' -f1)
  printf 'Run set: %s\n' "${h:0:12}"
}

# verify_snapshot DIR: SN1 and SN2 on an inputs directory (the pilot files with --pilot), printed as check lines.
INPUT_NAMES=(SPEC.md BASE.md DECISIONS.md REQUIREMENTS.md BRIEF.md)
verify_snapshot() {
  local dir=$1 e name n sn1="" sn2="" want got exp_fn=snapshot_input exp_lines=18
  if [ "$PILOT" -eq 1 ]; then exp_fn=pilot_file; exp_lines=2; fi
  local -a dots=()
  declare -A seen=()
  shopt -s dotglob nullglob
  for e in "$dir"/*; do
    name=${e##*/}
    case " ${INPUT_NAMES[*]} " in
      *" $name "*)
        seen[$name]=1
        if [ ! -f "$e" ] || [ -L "$e" ]; then sn1="the entry [$name] is not a regular file"; fi ;;
      *)
        if [[ "$name" == .* ]]; then dots+=("$name"); elif [ -z "$sn1" ]; then sn1="the directory holds the extra entry [$name]"; fi ;;
    esac
  done
  shopt -u dotglob nullglob
  if [ -z "$sn1" ]; then
    for n in "${INPUT_NAMES[@]}"; do
      if [ -z "${seen[$n]:-}" ]; then sn1="the directory lacks [$n]"; break; fi
    done
  fi
  for name in "${dots[@]}"; do warn SN1 "the directory holds the hidden entry [$name]"; done
  if [ -n "$sn1" ]; then fail SN1 "$sn1"; else pass SN1 "the directory holds exactly the five input files"; fi
  for n in "${INPUT_NAMES[@]}"; do
    [ -f "$dir/$n" ] || continue
    want=$("$exp_fn" "$n" | sha256sum | cut -d ' ' -f1)
    got=$(sha256sum < "$dir/$n" | cut -d ' ' -f1)
    if [ "$want" != "$got" ]; then sn2="[$n] has SHA-256 $got, expected $want"; break; fi
  done
  if [ -z "$sn2" ] && [ -f "$dir/REQUIREMENTS.md" ] && [ "$(wc -l < "$dir/REQUIREMENTS.md" | tr -d ' ')" -ne "$exp_lines" ]; then
    sn2="REQUIREMENTS.md does not have exactly $exp_lines lines"
  fi
  if [ -n "$sn2" ]; then fail SN2 "$sn2"; else pass SN2 "each input file equals its expected content"; fi
}

warn() { echo "WARN $1 $2"; }

if [ -n "$PRINT_SNAP" ]; then
  case "$PRINT_SNAP" in
    SPEC.md|BASE.md|DECISIONS.md|REQUIREMENTS.md|BRIEF.md) ;;
    *) echo "unknown snapshot file name: $PRINT_SNAP" >&2; exit 2 ;;
  esac
  snapshot_input "$PRINT_SNAP" > "$TMP/snap.out"
  if [ ! -s "$TMP/snap.out" ]; then echo "cannot build $PRINT_SNAP from git objects" >&2; exit 2; fi
  cat "$TMP/snap.out"
  exit 0
fi
if [ -n "$PRINT_PILOT" ]; then
  case "$PRINT_PILOT" in
    SPEC.md|BASE.md|DECISIONS.md|REQUIREMENTS.md|BRIEF.md) ;;
    *) echo "unknown pilot file name: $PRINT_PILOT" >&2; exit 2 ;;
  esac
  pilot_file "$PRINT_PILOT" > "$TMP/pilot.out"
  if [ ! -s "$TMP/pilot.out" ]; then echo "cannot build the pilot file $PRINT_PILOT" >&2; exit 2; fi
  cat "$TMP/pilot.out"
  exit 0
fi
if [ -n "$PRINT_RUNSET" ]; then
  print_run_set "$PRINT_RUNSET" > "$TMP/runset.out"
  if [ "$(wc -l < "$TMP/runset.out" | tr -d ' ')" -ne 11 ]; then echo "cannot build the run set" >&2; exit 2; fi
  cat "$TMP/runset.out"
  exit 0
fi
if [ "$PRINT_HASHES" -eq 1 ]; then
  if [ "$PILOT" -eq 1 ]; then input_hashes pilot; else input_hashes; fi
  exit 0
fi
if [ -n "$VERIFY_DIR" ]; then
  [ -d "$VERIFY_DIR" ] || { echo "$VERIFY_DIR is not a directory" >&2; exit 2; }
  verify_snapshot "$VERIFY_DIR"
  if [ "$FAILS" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
  echo "RESULT: FAIL $FAILS"
  exit 1
fi

# Real-mode parameters of hash_token_allowed: the four real input hashes and a directory with the five real
# input files, both built once in the temporary directory.
mkdir "$TMP/real"
for n in SPEC.md BASE.md DECISIONS.md REQUIREMENTS.md BRIEF.md; do snapshot_input "$n" > "$TMP/real/$n"; done
input_hashes > "$TMP/real.hashes"

# The pins of hash_token_allowed come from git objects only, never from the file given by --spec.
ALLOW_PINS=""
init_allow_pins() {
  local b r s a
  b=$(git rev-parse --verify --quiet "$BASE:$SPEC" 2> /dev/null) || b=""
  r=$(git rev-parse --verify --quiet "HEAD:$SPEC" 2> /dev/null) || r=""
  a=$(git rev-parse --verify --quiet "HEAD:$ARC_DEFAULT" 2> /dev/null) || a=""
  s=""
  if [ -n "$r" ]; then s=$(git cat-file blob "$r" | sha256sum | cut -d ' ' -f1); fi
  ALLOW_PINS="$b $r $s $a"
}
init_allow_pins

# hash_token_allowed TOKEN HASHES CORPUS: succeed when the hash-like TOKEN may occur in a committed file.
# HASHES is a file of four lines "NAME SHA256" and CORPUS a directory holding the five input files; both are
# supplied by the caller (the real ones in real mode, the pilot ones in pilot mode) and never computed here.
# A token is allowed when it equals, or is a prefix of length 7 or more of, one of the pins (base blob, result
# blob, SHA-256 of the result blob, blob of the owner approval record) or one of the four input SHA-256 values
# of HASHES; when it equals the 12-digit Run set value of the note; or when it occurs as a substring of one of
# the files of CORPUS. Every other hash-like token is rejected.
hash_token_allowed() {
  local tok=$1 low p h
  low=${tok,,}
  for p in $ALLOW_PINS; do
    if [[ "$p" == "$low"* ]]; then return 0; fi
  done
  while read -r _ h; do
    if [ -n "$h" ] && [[ "$h" == "$low"* ]]; then return 0; fi
  done < "$2"
  if [[ "$N_RUNSET" =~ ^[0-9a-f]{12}$ ]] && [ "$low" = "$N_RUNSET" ]; then return 0; fi
  if grep -q -F -e "$tok" "$3"/* 2> /dev/null; then return 0; fi
  return 1
}

# x1_scan FILE HASHES CORPUS: print the first self-containment problem of FILE (nothing when there is none)
# and return 1 on a problem. The only implementation of the X1 patterns: no drive-letter or home-directory
# path, no web address, no markdown link, no /tmp/, none of the words scratchpad, appdata, transcript, no
# unfinished-text marker or fill marker, no hash-like token (a maximal run of 7 or more hexadecimal digits
# with at least one decimal digit) that hash_token_allowed rejects.
x1_scan() {
  local f=$1 label re hit tok
  while IFS='|' read -r label re; do
    hit=$(grep -n -E -e "$re" "$f" | head -n1)
    if [ -n "$hit" ]; then
      echo "$label at line ${hit%%:*}"
      return 1
    fi
  done << 'PATTERNS'
drive-letter or home-directory path|(^|[^A-Za-z0-9])[A-Za-z]:[\\/]|/Users/|/home/|~/
web address|https?://
markdown link|\]\(
temporary directory|/tmp/
scratch, local-data or transcript reference|[Ss][Cc][Rr][Aa][Tt][Cc][Hh][Pp][Aa][Dd]|[Aa][Pp][Pp][Dd][Aa][Tt][Aa]|[Tt][Rr][Aa][Nn][Ss][Cc][Rr][Ii][Pp][Tt]
unfinished-text marker|(^|[^A-Za-z0-9])(TODO|FIXME|TBD|XXX)([^A-Za-z0-9]|$)|@@FILL@@
PATTERNS
  while IFS= read -r tok; do
    if ! hash_token_allowed "$tok" "$2" "$3"; then
      echo "hash-like token [$tok] that is not an allowed pin or input value"
      return 1
    fi
  done < <(grep -o -E '[0-9A-Fa-f]{7,}' "$f" | grep '[0-9]' | sort -u)
  return 0
}

# build_heads FILE OUT: one line "number TAB line" for every numbered heading of FILE ("## N. " or "### N.M "),
# read fence-aware.
build_heads() {
  awk '
    /^```/ { fence = !fence; next }
    fence { next }
    /^## [0-9]+\. / { id = $2; sub(/\.$/, "", id); print id "\t" NR; next }
    /^### [0-9]+\.[0-9]+ / { print $2 "\t" NR }
  ' "$1" > "$2"
}

# build_passes BRIEF OUT: one line "pass TAB scope TAB from TAB upto" for every row of the pass table of BRIEF.
build_passes() {
  h2_lines "Passes" "$1" | awk -F'|' '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^\| RV-/ { print trim($2) "\t" trim($3) "\t" trim($4) "\t" trim($5) }
  ' > "$2"
}

# prep_ranges: the headings of the specification, its end line and the pass table of the brief, built once.
RANGES_READY=0
spec_end=0
prep_ranges() {
  [ "$RANGES_READY" -eq 0 ] || return 0
  RANGES_READY=1
  readable "$BR" "$BRIEFFILE"
  build_heads "$SP" "$TMP/heads.tsv"
  spec_end=$(( $(wc -l < "$SP" | tr -d ' ') + 1 ))
  build_passes "$BR" "$TMP/passes.tsv"
}

# pass_line TOKEN: the line number for header, end or a heading number of the specification; empty when unknown.
pass_line() {
  case "$1" in
    header) echo 1 ;;
    end) echo "$spec_end" ;;
    *) awk -F'\t' -v id="$1" '$1 == id { print $2; exit }' "$TMP/heads.tsv" ;;
  esac
}

# report_source PASS: the one place from which the report checks read their sources. It sets RS_SPEC (the
# specification text), RS_BASE (the base text), RS_SPEC_HEADS and RS_BASE_HEADS (their numbered headings),
# RS_HASHES (the four expected SHA-256 values, lines "NAME SHA256"), RS_CORPUS (the directory of the five input
# files that hash_token_allowed searches), and for PASS RS_FROM and RS_TO (the line range FROM up to, not
# including, TO) and RS_TOP (1 when only top-level headings are expected in COVERAGE).
RS_READY=0
report_source() {
  local id=$1 row a b
  if [ "$RS_READY" -eq 0 ]; then
    RS_READY=1
    prep_ranges
    RS_SPEC="$SP"
    RS_BASE="$TMP/rs.base"
    git cat-file blob "$BASE:$SPEC" > "$RS_BASE" 2> /dev/null || { echo "cannot read the base text $BASE:$SPEC" >&2; exit 2; }
    RS_HASHES="$TMP/real.hashes"
    RS_CORPUS="$TMP/real"
    RS_SPEC_HEADS="$TMP/heads.tsv"
    RS_BASE_HEADS="$TMP/rs.base.heads"
    build_heads "$RS_BASE" "$RS_BASE_HEADS"
  fi
  row=$(awk -F'\t' -v i="$id" '$1 == i' "$TMP/passes.tsv")
  a=$(pass_line "$(printf '%s' "$row" | cut -f3)")
  b=$(pass_line "$(printf '%s' "$row" | cut -f4)")
  if [ -z "$a" ] || [ -z "$b" ] || [ "$a" -ge "$b" ]; then echo "cannot resolve the line range of $id" >&2; exit 2; fi
  RS_FROM=$a
  RS_TO=$b
  RS_TOP=0
  if [ "$id" = RV-X ]; then RS_TOP=1; fi
}

# rp_norm IN OUT: the only normalisation applied to a report: CR bytes deleted, each tab replaced by four spaces.
rp_norm() { tr -d '\r' < "$1" | sed 's/\t/    /g' > "$2"; }

# rp_parse FILE: one line per label occurrence of a normalised report: "TOKEN TAB value on the label line TAB
# value with the continuation lines joined by spaces TAB number of continuation lines TAB line number". The
# tokens are B REPORT BEGIN, I IDENTITY, N INPUT, S SCOPE, C COVERAGE, F FINDINGS, K FINDING, V SEVERITY,
# R REFERENCE, M SUMMARY, A REASONING, D DISPOSITION REQUIRED, P CHECKS PERFORMED, L LIMITS, T VERDICT, E
# REPORT END. A label only counts at the start of a line; blank lines are skipped; a line before the first
# label belongs to no field.
rp_parse() {
  awk '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    function flush() { if (tok != "") print tok "\t" first "\t" trim(full) "\t" ncont "\t" at }
    function label(l) {
      if (l ~ /^REPORT BEGIN( |$)/) { v = substr(l, 13); return "B" }
      if (l ~ /^IDENTITY:/) { v = substr(l, 10); return "I" }
      if (l ~ /^INPUT /) { v = substr(l, 7); return "N" }
      if (l ~ /^SCOPE:/) { v = substr(l, 7); return "S" }
      if (l ~ /^COVERAGE:/) { v = substr(l, 10); return "C" }
      if (l ~ /^FINDINGS:/) { v = substr(l, 10); return "F" }
      if (l ~ /^FINDING /) { v = substr(l, 9); return "K" }
      if (l ~ /^SEVERITY:/) { v = substr(l, 10); return "V" }
      if (l ~ /^REFERENCE:/) { v = substr(l, 11); return "R" }
      if (l ~ /^SUMMARY:/) { v = substr(l, 9); return "M" }
      if (l ~ /^REASONING:/) { v = substr(l, 11); return "A" }
      if (l ~ /^DISPOSITION REQUIRED:/) { v = substr(l, 22); return "D" }
      if (l ~ /^CHECKS PERFORMED:/) { v = substr(l, 18); return "P" }
      if (l ~ /^LIMITS:/) { v = substr(l, 8); return "L" }
      if (l ~ /^VERDICT:/) { v = substr(l, 9); return "T" }
      if (l ~ /^REPORT END( |$)/) { v = substr(l, 11); return "E" }
      return ""
    }
    {
      t = label($0)
      if (t != "") { flush(); tok = t; first = trim(v); full = first; ncont = 0; at = NR; next }
      if ($0 ~ /^ *$/) next
      if (tok != "") { full = full " " trim($0); ncont++ }
    }
    END { flush() }
  ' "$1"
}

# seq_names TOKENS: the label names of a token string, separated by spaces.
seq_names() {
  awk -v s="$1" 'BEGIN {
    n = split("B BEGIN I IDENTITY N INPUT S SCOPE C COVERAGE F FINDINGS K FINDING V SEVERITY R REFERENCE M SUMMARY A REASONING D DISPOSITION P CHECKS L LIMITS T VERDICT E END", a, " ")
    for (i = 1; i < n; i += 2) nm[a[i]] = a[i + 1]
    for (i = 1; i <= length(s); i++) printf "%s%s", nm[substr(s, i, 1)], (i < length(s) ? " " : "")
    print ""
  }'
}

# Accessors for the parsed report in RP_FIELDS: rp_first TOKEN (the first label-line value), rp_full TOKEN (the
# first value with its continuation lines), rp_count TOKEN, rp_vals TOKEN (every label-line value, one per line).
RP_FIELDS="$TMP/rp.fields"
rp_first() { awk -F'\t' -v t="$1" '$1 == t { print $2; exit }' "$RP_FIELDS"; }
rp_full() { awk -F'\t' -v t="$1" '$1 == t { print $3; exit }' "$RP_FIELDS"; }
rp_count() { awk -F'\t' -v t="$1" '$1 == t { n++ } END { print n + 0 }' "$RP_FIELDS"; }
rp_vals() { awk -F'\t' -v t="$1" '$1 == t { print $2 }' "$RP_FIELDS"; }

# The phrases of RP9, kept as one list (case-insensitive search of the LIMITS text).
RP_PHRASES=("truncat" "cut off" "cutoff" "ran out of context" "ran out of tokens" "context window" "context limit" "token limit" "output limit" "did not read the whole" "did not read the entire" "did not read the full" "could not read all" "could not read the whole" "could not read the entire" "unable to read all" "unable to read the whole" "unable to load" "only read the first" "partially read" "not fully read" "could not complete" "unable to complete" "did not complete" "incomplete")

# head_known HEADINGS SECTION: succeed when SECTION is header or a number in the heading list HEADINGS.
head_known() {
  [ "$2" = header ] && return 0
  awk -F'\t' -v s="$2" '$1 == s { f = 1 } END { exit !f }' "$1"
}

# report_checks FILE PASS: RP1 to RP9 on the normalised report FILE for the pass PASS (all sources through
# report_source). Every message names the pass.
report_checks() {
  local f=$1 id=$2 m first last seq it v nm hv want_hash nc names n_exp n_omit i want nb fv a b fl_lines ffile fheads fname sec q text re ph low hit
  local rp2_re='^BINNNNSCF(KVR{1,4}MAD)*PLTE$'
  rp_parse "$f" > "$RP_FIELDS"
  report_source "$id"

  # RP1 framing.
  m=""
  first=$(grep -m1 '[^[:space:]]' "$f")
  last=$(grep '[^[:space:]]' "$f" | tail -n1)
  if [ "$first" != "REPORT BEGIN $id" ]; then
    m="the first non-blank line is [${first:0:60}], expected [REPORT BEGIN $id]"
  elif [ "$last" != "REPORT END $id" ]; then
    m="the last non-blank line is [${last:0:60}], expected [REPORT END $id]"
  elif [ "$(grep -c '^REPORT BEGIN' "$f")" -ne 1 ] || [ "$(grep -c '^REPORT END' "$f")" -ne 1 ]; then
    m="REPORT BEGIN or REPORT END does not occur exactly once"
  fi
  if [ -n "$m" ]; then fail RP1 "$id: $m"; else pass RP1 "$id: the report begins with REPORT BEGIN $id, ends with REPORT END $id and holds nothing outside them"; fi

  # RP2 label order and continuation lines.
  m=""
  seq=$(cut -f1 "$RP_FIELDS" | tr -d '\n')
  if ! [[ "$seq" =~ $rp2_re ]]; then
    m="the labels do not occur in the order of the brief (found: $(seq_names "${seq:0:150}"))"
  else
    it=$(awk -F'\t' '$4 > 0 && $1 !~ /^[APLD]$/ { print $1; exit }' "$RP_FIELDS")
    if [ -n "$it" ]; then
      m="the field $(seq_names "$it") has a continuation line, only REASONING, DISPOSITION REQUIRED, CHECKS PERFORMED and LIMITS may continue"
    elif awk -F'\t' '($1 == "A" || $1 == "D") && $3 == "" { bad = 1 } END { exit !bad }' "$RP_FIELDS"; then
      m="REASONING or DISPOSITION REQUIRED holds no text"
    fi
  fi
  if [ -n "$m" ]; then fail RP2 "$id: $m"; else pass RP2 "$id: the labels occur in the order of the brief with no stray continuation line"; fi

  # RP3 identity and inputs.
  m=""
  nc=""
  v=$(rp_first I)
  if ! [[ "$v" =~ (^|[^A-Za-z])Devin([^A-Za-z]|$) ]]; then
    m="the IDENTITY line does not name Devin"
  elif [ "$(rp_count N)" -ne 4 ]; then
    m="the report has $(rp_count N) INPUT lines, expected four"
  else
    names=""
    while IFS= read -r v; do
      nm=${v%% *}
      hv=${v#"$nm"}
      hv=${hv# }
      want_hash=$(awk -v n="$nm" '$1 == n { print $2 }' "$RS_HASHES")
      names+="$nm "
      if [ -z "$want_hash" ]; then
        m="an INPUT line names [${nm:0:30}], expected SPEC.md, BASE.md, DECISIONS.md and REQUIREMENTS.md"
        break
      elif [ "$hv" = "not computed" ]; then
        nc+=" $nm"
      elif [ "$hv" != "$want_hash" ]; then
        if [[ "$hv" =~ ^[0-9a-f]{64}$ ]]; then m="the INPUT $nm value is not the expected SHA-256"; else m="the INPUT $nm value [${hv:0:70}] is neither a SHA-256 nor the words not computed"; fi
        break
      fi
    done < <(rp_vals N)
    if [ -z "$m" ] && [ "$(tr ' ' '\n' <<< "$names" | grep . | sort | tr '\n' ' ')" != "BASE.md DECISIONS.md REQUIREMENTS.md SPEC.md " ]; then
      m="the four INPUT lines do not name SPEC.md, BASE.md, DECISIONS.md and REQUIREMENTS.md once each"
    fi
  fi
  if [ -n "$m" ]; then fail RP3 "$id: $m"; else pass RP3 "$id: the identity names Devin and the four INPUT lines carry the expected SHA-256 values or not computed"; fi
  if [ -z "$m" ] && [ -n "$nc" ]; then warn RP3 "$id: SHA-256 not computed for$nc"; fi

  # RP4 scope and coverage.
  m=""
  n_exp=0
  n_omit=0
  : > "$TMP/rp.cov"
  if [ -z "$(rp_first S)" ]; then
    m="SCOPE is empty"
  elif [ -z "$(rp_first C)" ]; then
    m="COVERAGE is empty"
  else
    while IFS= read -r it; do
      if ! [[ "$it" =~ ^[0-9]+(\.[0-9]+)*$ ]]; then m="COVERAGE holds [${it:0:30}], which is not a heading number"; break; fi
      echo "$it" >> "$TMP/rp.cov"
    done < <(rp_first C | awk -F, '{ for (i = 1; i <= NF; i++) { gsub(/^ +| +$/, "", $i); print $i } }')
  fi
  : > "$TMP/rp.omit"
  : > "$TMP/rp.unk"
  if [ -z "$m" ]; then
    awk -F'\t' -v a="$RS_FROM" -v b="$RS_TO" -v top="$RS_TOP" '$2 + 0 >= a + 0 && $2 + 0 < b + 0 && (top == 0 || $1 !~ /\./) { print $1 }' "$RS_SPEC_HEADS" > "$TMP/rp.exp"
    n_exp=$(wc -l < "$TMP/rp.exp" | tr -d ' ')
    grep -v -x -F -f "$TMP/rp.cov" "$TMP/rp.exp" > "$TMP/rp.omit"
    n_omit=$(wc -l < "$TMP/rp.omit" | tr -d ' ')
    cut -f1 "$RS_SPEC_HEADS" > "$TMP/rp.known"
    grep -v -x -F -f "$TMP/rp.known" "$TMP/rp.cov" > "$TMP/rp.unk"
    if [ "$n_exp" -gt 0 ] && [ $((n_omit * 2)) -gt "$n_exp" ]; then m="COVERAGE omits $n_omit of the $n_exp headings of the pass range"; fi
  fi
  if [ -n "$m" ]; then fail RP4 "$id: $m"; else pass RP4 "$id: SCOPE and COVERAGE are well-formed and COVERAGE omits $n_omit of the $n_exp headings of the pass range"; fi
  if [ -z "$m" ] && [ "$n_omit" -gt 0 ]; then
    it=""
    if [ "$n_omit" -gt 12 ]; then it=" and $((n_omit - 12)) more"; fi
    warn RP4 "$id: COVERAGE omits $n_omit of the $n_exp headings of the pass range: $(head -n 12 "$TMP/rp.omit" | paste -sd ' ' -)$it"
  fi
  if [ -z "$m" ] && [ -s "$TMP/rp.unk" ]; then warn RP4 "$id: COVERAGE names no heading of the specification for: $(head -n 12 "$TMP/rp.unk" | paste -sd ' ' -)"; fi

  # RP5 findings.
  m=""
  nb=$(rp_count K)
  fv=$(rp_first F)
  if [ "$fv" = none ]; then
    [ "$nb" -eq 0 ] || m="FINDINGS says none but $nb FINDING blocks follow"
  elif [[ "$fv" =~ ^[1-9][0-9]{0,5}$ ]]; then
    [ "$fv" -eq "$nb" ] || m="FINDINGS says $fv but $nb FINDING blocks follow"
  else
    m="the FINDINGS value [${fv:0:40}] is neither none nor a positive integer"
  fi
  if [ -z "$m" ]; then
    i=0
    while IFS= read -r v; do
      i=$((i + 1))
      want="$id-$(printf '%03d' "$i")"
      if [ "$v" != "$want" ]; then m="finding $i has the id [${v:0:40}], expected [$want]"; break; fi
    done < <(rp_vals K)
  fi
  if [ -z "$m" ]; then
    while IFS= read -r v; do
      case "$v" in
        BLOCKING|MAJOR|MINOR|INFO) ;;
        *) m="a SEVERITY value is [${v:0:40}], expected BLOCKING, MAJOR, MINOR or INFO"; break ;;
      esac
    done < <(rp_vals V)
  fi
  if [ -z "$m" ]; then
    while IFS= read -r v; do
      if [ -z "$v" ]; then m="a SUMMARY line is empty"; break; fi
      if [ "${#v}" -gt 200 ]; then m="a SUMMARY line has ${#v} characters, at most 200 are allowed"; break; fi
    done < <(rp_vals M)
  fi
  if [ -z "$m" ] && awk -F'\t' '($1 == "R" || $1 == "M") && index($2, "|") { bad = 1 } END { exit !bad }' "$RP_FIELDS"; then
    m="a REFERENCE or SUMMARY line holds a vertical bar"
  fi
  if [ -n "$m" ]; then fail RP5 "$id: $m"; else pass RP5 "$id: the FINDINGS count, the finding ids, the severity words and the summaries are well-formed ($nb findings)"; fi

  # RP6 references resolve in the specification or the base text.
  m=""
  i=0
  re='^file (SPEC|BASE); section ([^;]+); lines ([0-9]{1,7})-([0-9]{1,7}); quote (.*)$'
  while IFS= read -r v; do
    i=$((i + 1))
    if ! [[ "$v" =~ $re ]]; then m="reference $i [${v:0:80}] does not have the form [file F; section S; lines A-B; quote Q]"; break; fi
    fname=${BASH_REMATCH[1]}
    sec=${BASH_REMATCH[2]}
    a=$((10#${BASH_REMATCH[3]}))
    b=$((10#${BASH_REMATCH[4]}))
    q=${BASH_REMATCH[5]}
    if [ "$fname" = SPEC ]; then ffile=$RS_SPEC; fheads=$RS_SPEC_HEADS; else ffile=$RS_BASE; fheads=$RS_BASE_HEADS; fi
    fl_lines=$(wc -l < "$ffile" | tr -d ' ')
    if ! head_known "$fheads" "$sec"; then m="reference $i names the section [$sec], which is no numbered heading of $fname"; break; fi
    if [ "$a" -lt 1 ] || [ "$a" -gt "$b" ] || [ "$b" -gt "$fl_lines" ]; then m="reference $i has the lines $a-$b, which are not inside 1-$fl_lines of $fname"; break; fi
    if [ "$q" != none ]; then
      if [ "${#q}" -lt 3 ] || [ "${q:0:1}" != '"' ] || [ "${q: -1}" != '"' ]; then m="reference $i has a quote that is neither none nor text in double quotes"; break; fi
      text=${q:1:${#q}-2}
      if ! grep -q -F -e "$text" "$ffile"; then m="reference $i quotes text that is no part of any line of $fname"; break; fi
      if ! sed -n "${a},${b}p" "$ffile" | grep -q -F -e "$text"; then
        warn RP6 "$id: the quote of reference $i occurs in $fname but not between the lines $a-$b"
      fi
    fi
  done < <(rp_vals R)
  if [ -n "$m" ]; then fail RP6 "$id: $m"; else pass RP6 "$id: all $i references resolve in the pinned text or the base text"; fi

  # RP7 closing lines.
  m=""
  want="NO BLOCKING FINDINGS"
  if rp_vals V | grep -q -x BLOCKING; then want="BLOCKING FINDINGS PRESENT"; fi
  if [ -z "$(rp_full P)" ]; then
    m="CHECKS PERFORMED holds no text"
  elif [ -z "$(rp_full L)" ]; then
    m="LIMITS holds no text"
  elif [ "$(rp_first T)" != "$want" ]; then
    m="the VERDICT is [$(rp_first T | cut -c1-40)], the severities require [$want]"
  fi
  if [ -n "$m" ]; then fail RP7 "$id: $m"; else pass RP7 "$id: CHECKS PERFORMED and LIMITS hold text and the VERDICT [$want] agrees with the severities"; fi

  # RP8 hygiene.
  m=$(x1_scan "$f" "$RS_HASHES" "$RS_CORPUS")
  if [ -n "$m" ]; then fail RP8 "$id: $m"; else pass RP8 "$id: no local path, address, link, scratch reference, unfinished marker or foreign hash-like token"; fi

  # RP9 claims of truncation or incompleteness (warnings only).
  low=$(rp_full L | tr '[:upper:]' '[:lower:]')
  hit=0
  for ph in "${RP_PHRASES[@]}"; do
    if [[ "$low" == *"$ph"* ]]; then warn RP9 "$ph in LIMITS of $id"; hit=1; fi
  done
  if [ "$hit" -eq 0 ]; then pass RP9 "$id: the LIMITS text makes no claim of truncation or incompleteness"; fi
}

# finish: print the result line and exit.
finish() {
  if [ "$FAILS" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
  echo "RESULT: FAIL $FAILS"
  exit 1
}

if [ -n "$REPORT_FILE" ]; then
  rp_norm "$REPORT_FILE" "$TMP/rp.norm"
  report_checks "$TMP/rp.norm" "$REPORT_PASS"
  finish
fi

# The six passes in the order in which their findings are derived and their reports are quoted.
PASS_IDS=(RV-A RV-B RV-C RV-D RV-E RV-X)

# The fixed introduction of the Reports section (one line).
REPORTS_INTRO='Each report is quoted whole, line by line: a quote mark and a space are added at the start of each line, and an empty line becomes a quote mark alone. The only change made to a report is mechanical: line endings are converted to LF and each tab to four spaces.'

# rp_findings FILE: one line "ID TAB SEVERITY TAB first reference TAB summary" for every finding block of the
# normalised report FILE.
rp_findings() {
  rp_parse "$1" | awk -F'\t' '
    $1 == "K" { id = $2; sev = ""; ref = ""; sum = ""; open = 1; next }
    open && $1 == "V" { sev = $2; next }
    open && $1 == "R" && ref == "" { ref = $2; next }
    open && $1 == "M" { sum = $2; next }
    open && $1 == "D" { print id "\t" sev "\t" ref "\t" sum; open = 0 }
  '
}

# derive_findings DIR: the findings of the six normalised reports DIR/ID.txt in pass order and block order,
# written to the file pt.tsv of the temporary directory.
derive_findings() {
  local id
  : > "$TMP/pt.tsv"
  for id in "${PASS_IDS[@]}"; do rp_findings "$1/$id.txt" >> "$TMP/pt.tsv"; done
}

# print_table DIR: the content of the Findings section derived from the six normalised reports DIR/ID.txt.
print_table() {
  derive_findings "$1"
  if [ ! -s "$TMP/pt.tsv" ]; then
    echo "No findings were returned by any pass."
    return 0
  fi
  echo "| Finding | Severity | Reference | Summary | Disposition |"
  echo "|---|---|---|---|---|"
  awk -F'\t' '{ printf "| %s | %s | %s | %s |  |\n", $1, $2, $3, $4 }' "$TMP/pt.tsv"
}

# print_counts DIR: the counts line and one line per BLOCKING finding.
print_counts() {
  derive_findings "$1"
  awk -F'\t' '{ n++; c[$2]++ } END { printf "total=%d blocking=%d major=%d minor=%d info=%d\n", n, c["BLOCKING"], c["MAJOR"], c["MINOR"], c["INFO"] }' "$TMP/pt.tsv"
  awk -F'\t' '$2 == "BLOCKING" { print "blocking-id " $1 }' "$TMP/pt.tsv"
}

# reports_extract OUTDIR: split the Reports section of the note into the six reports OUTDIR/ID.txt with the quote
# marks removed. Returns 1 with the problem in RPS_MSG when the section is not the fixed introduction and then
# exactly six blocks "### ID — Scope" in pass order that hold only quoted lines.
RPS_MSG=""
reports_extract() {
  local out=$1 id scope k
  local -a want=() heads=()
  RPS_MSG=""
  prep_ranges
  mkdir -p "$out"
  h2_lines "Reports" "$NT" > "$TMP/rps.lines"
  if [ "$(awk '/^### / { exit } NF' "$TMP/rps.lines")" != "$REPORTS_INTRO" ]; then
    RPS_MSG="the Reports section does not begin with the fixed introduction"
    return 1
  fi
  for id in "${PASS_IDS[@]}"; do
    scope=$(awk -F'\t' -v i="$id" '$1 == i { print $2 }' "$TMP/passes.tsv")
    want+=("### $id — $scope")
  done
  mapfile -t heads < <(grep '^### ' "$TMP/rps.lines")
  if [ "${#heads[@]}" -ne 6 ]; then
    RPS_MSG="the Reports section holds ${#heads[@]} blocks, expected six"
    return 1
  fi
  for k in 0 1 2 3 4 5; do
    if [ "${heads[$k]}" != "${want[$k]}" ]; then
      RPS_MSG="block $((k + 1)) has the heading [${heads[$k]}], expected [${want[$k]}]"
      return 1
    fi
  done
  for k in 1 2 3 4 5 6; do : > "$TMP/rps.blk.$k"; done
  awk -v dir="$TMP" '/^### / { k++; next } k > 0 { print > (dir "/rps.blk." k) }' "$TMP/rps.lines"
  for k in 1 2 3 4 5 6; do
    id=${PASS_IDS[$((k - 1))]}
    if ! awk '
      { l[NR] = $0 }
      END {
        s = 1; while (s <= NR && l[s] == "") s++
        e = NR; while (e >= s && l[e] == "") e--
        if (e < s) exit 1
        for (i = s; i <= e; i++) {
          if (l[i] == ">") print ""
          else if (substr(l[i], 1, 2) == "> ") print substr(l[i], 3)
          else exit 1
        }
      }
    ' "$TMP/rps.blk.$k" > "$out/$id.txt"; then
      RPS_MSG="the block [$id] is empty or holds a line that is not a quoted line"
      return 1
    fi
  done
  return 0
}

if [ -n "$PRINT_SECTIONS" ]; then
  [ -d "$PRINT_SECTIONS" ] || { echo "$PRINT_SECTIONS is not a directory" >&2; exit 2; }
  prep_ranges
  mkdir "$TMP/ps"
  for id in "${PASS_IDS[@]}"; do
    [ -f "$PRINT_SECTIONS/$id.txt" ] && [ -r "$PRINT_SECTIONS/$id.txt" ] || { echo "cannot read $PRINT_SECTIONS/$id.txt" >&2; exit 2; }
    rp_norm "$PRINT_SECTIONS/$id.txt" "$TMP/ps/$id.txt"
  done
  printf '## Reports\n\n%s\n\n' "$REPORTS_INTRO"
  for id in "${PASS_IDS[@]}"; do
    scope=$(awk -F'\t' -v i="$id" '$1 == i { print $2 }' "$TMP/passes.tsv")
    printf '### %s — %s\n\n' "$id" "$scope"
    awk '{ if ($0 == "") print ">"; else print "> " $0 }' "$TMP/ps/$id.txt"
    printf '\n'
  done
  printf '## Findings\n\n'
  print_table "$TMP/ps"
  printf '\n'
  exit 0
fi
if [ "$PRINT_TABLE" -eq 1 ] || [ "$PRINT_COUNTS" -eq 1 ]; then
  if ! reports_extract "$TMP/rep"; then echo "cannot read the quoted reports of the note: $RPS_MSG" >&2; exit 2; fi
  if [ "$PRINT_TABLE" -eq 1 ]; then print_table "$TMP/rep"; fi
  if [ "$PRINT_COUNTS" -eq 1 ]; then print_counts "$TMP/rep"; fi
  exit 0
fi

# E1, E2: encoding of the note.
msg=$(enc1 "$NT")
if [ -n "$msg" ]; then fail E1 "note: $msg"; else pass E1 "note is valid UTF-8 without BOM"; fi
msg=$(enc2 "$NT")
if [ -n "$msg" ]; then fail E2 "note: $msg"; else pass E2 "note has LF line endings, one final LF, no tab"; fi

# P0: the pin table has each of the twelve labels once, with well-formed values.
p0=""
for l in "${PIN_LABELS[@]}"; do
  n=$(pin_count "$TMP/note.pins" "$l")
  if [ "$n" -ne 1 ]; then p0="the pin table has $n rows labelled [$l], expected one"; break; fi
done
if [ -z "$p0" ]; then
  extra=$(awk -F'\t' 'BEGIN { split("Reviewed file|Base blob|Result blob|Reviewed SHA-256|Line count|Diffstat|Commits touching the file|Owner approval record|Owner approval record blob|Run set|Consent question|Consent answer", a, "|"); for (i in a) ok[a[i]] = 1 } !($1 in ok) { print $1; exit }' "$TMP/note.pins")
  [ -z "$extra" ] || p0="the pin table has an unexpected row [$extra]"
fi
if [ -z "$p0" ]; then
  while IFS=$'\t' read -r label raw tok; do
    if [ "$raw" != "\`$tok\`" ]; then p0="the value of [$label] is not one backticked token"; break; fi
  done < "$TMP/note.pins"
fi
if [ -z "$p0" ]; then
  [ "$N_REVF" = "$SPEC" ] || p0="Reviewed file is [$N_REVF], expected $SPEC"
  [ -n "$p0" ] || [[ "$N_BASE" =~ ^[0-9a-f]{40}$ ]] || p0="Base blob [$N_BASE] is not 40 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$N_RES" =~ ^[0-9a-f]{40}$ ]] || p0="Result blob [$N_RES] is not 40 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$N_ARCB" =~ ^[0-9a-f]{40}$ ]] || p0="Owner approval record blob [$N_ARCB] is not 40 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$N_SHA" =~ ^[0-9a-f]{64}$ ]] || p0="Reviewed SHA-256 [$N_SHA] is not 64 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$N_LINES" =~ ^[0-9]+$ ]] || p0="Line count [$N_LINES] is not an integer"
  [ -n "$p0" ] || [[ "$N_COMM" =~ ^[0-9]+$ ]] || p0="Commits touching the file [$N_COMM] is not an integer"
  [ -n "$p0" ] || [[ "$N_DIFF" =~ ^[0-9]+\ files?\ changed(,\ [0-9]+\ insertions?\(\+\))?(,\ [0-9]+\ deletions?\(-\))?$ ]] || p0="Diffstat [$N_DIFF] does not have the form of git shortstat"
  if [ -z "$p0" ]; then
    for l in "${CONSENT_LABELS[@]}"; do
      if [ "$STAGE" = reported ]; then
        if [ "$(pin_tok "$TMP/note.pins" "$l")" = pending ]; then p0="the row [$l] still reads pending in stage reported"; break; fi
      elif [ "$(pin_tok "$TMP/note.pins" "$l")" != pending ]; then
        p0="the row [$l] does not read pending in stage $STAGE"; break
      fi
    done
  fi
fi
if [ -n "$p0" ]; then
  fail P0 "$p0"
elif [ "$STAGE" = reported ]; then
  pass P0 "the pin table has the twelve rows once, each one backticked well-formed value, the consent rows filled"
else
  pass P0 "the pin table has the twelve rows once, each one backticked well-formed value, the consent rows pending"
fi

# A3: the owner approval record has exactly one outcome line "- Owner approval: approved".
n_appr=$(grep -c -x -F -e "- Owner approval: approved" "$AR")
if [ "$n_appr" -eq 1 ]; then
  pass A3 "the owner approval record has exactly one line [- Owner approval: approved]"
else
  fail A3 "the owner approval record has $n_appr lines [- Owner approval: approved], expected one"
fi

# A2: the first seven pin rows equal the owner approval record's; the record path and blob are right.
a2=""
for l in "${COPIED_LABELS[@]}"; do
  if [ "$(pin_count "$TMP/arc.pins" "$l")" -ne 1 ]; then a2="the owner approval record has no single row [$l]"; break; fi
  if [ "$(pin_raw "$TMP/note.pins" "$l")" != "$(pin_raw "$TMP/arc.pins" "$l")" ]; then a2="the row [$l] of the note differs from the owner approval record"; break; fi
done
if [ -z "$a2" ] && [ "$N_ARCF" != "$ARC_DEFAULT" ]; then
  a2="Owner approval record is [$N_ARCF], expected $ARC_DEFAULT"
fi
if [ -z "$a2" ]; then
  arc_blob=$(git hash-object --no-filters "$AR")
  [ "$N_ARCB" = "$arc_blob" ] || a2="Owner approval record blob is [$N_ARCB], the record file has $arc_blob"
fi
if [ -z "$a2" ] && [ "$APPROVAL" = "$ARC_DEFAULT" ]; then
  arc_head=$(git rev-parse --verify --quiet "HEAD:$ARC_DEFAULT" 2> /dev/null) || arc_head=""
  [ "$N_ARCB" = "$arc_head" ] || a2="Owner approval record blob is [$N_ARCB], HEAD holds [${arc_head:-absent}] for the record"
fi
if [ -n "$a2" ]; then fail A2 "$a2"; else pass A2 "the first seven pin rows equal the owner approval record; the record path and blob are right"; fi

# Z1: the Phase 3 check in its recorded stage passes.
z1_out=$(bash "$CHK3" --stage recorded --packet "$PACKET" --record "$APPROVAL" --spec "$SPECFILE" --base "$BASE" 2>&1)
if [ "$(printf '%s\n' "$z1_out" | tail -n1)" = "RESULT: PASS" ]; then
  pass Z1 "the Phase 3 check in stage recorded ends with RESULT: PASS"
else
  fail Z1 "the Phase 3 check in stage recorded does not pass: $(printf '%s\n' "$z1_out" | grep -m3 '^FAIL ' | tr '\n' ' ')"
fi

# R1: the specification equals the result blob in the file, the index and HEAD.
r_file=$(git hash-object --no-filters "$SP")
r_index=$(git ls-files -s -- "$SPEC" 2> /dev/null | awk 'NR == 1 { print $2 }')
r_head=$(git rev-parse --verify --quiet "HEAD:$SPEC" 2> /dev/null) || r_head=""
r1=""
[ "$r_file" = "$N_RES" ] || r1="the specification file has blob $r_file, the note pins $N_RES (the file differs from the pinned text)"
[ -n "$r1" ] || [ "$r_index" = "$N_RES" ] || r1="the index holds [${r_index:-absent}] for the specification, the note pins $N_RES (the index differs from the pinned text)"
[ -n "$r1" ] || [ "$r_head" = "$N_RES" ] || r1="HEAD holds [${r_head:-absent}] for the specification, the note pins $N_RES (HEAD differs from the pinned text)"
if [ -n "$r1" ]; then fail R1 "$r1"; else pass R1 "the specification file, the index and HEAD all hold blob $N_RES"; fi

# H1: SHA-256 and line count of the specification equal the note's.
calc_sha=$(sha256sum < "$SP" | cut -d ' ' -f1)
calc_lines=$(wc -l < "$SP" | tr -d ' ')
h1=""
[ "$calc_sha" = "$N_SHA" ] || h1="SHA-256 of the specification is $calc_sha, the note pins [$N_SHA]"
[ -n "$h1" ] || [ "$calc_lines" = "$N_LINES" ] || h1="the specification has $calc_lines lines, the note pins [$N_LINES]"
if [ -n "$h1" ]; then fail H1 "$h1"; else pass H1 "SHA-256 and line count of the specification equal the note's"; fi

# S1: every changed path since the base (committed, staged, unstaged, untracked), read NUL-delimited, is the
# specification or under .planning/. A failing git listing is a usage-level error, never a pass.
: > "$TMP/paths.raw"
{
  git diff -z --name-only --no-renames "$BASE...HEAD" >> "$TMP/paths.raw" 2> /dev/null \
    && git diff -z --name-only --no-renames >> "$TMP/paths.raw" 2> /dev/null \
    && git diff -z --name-only --no-renames --cached >> "$TMP/paths.raw" 2> /dev/null \
    && git ls-files -z --others --exclude-standard >> "$TMP/paths.raw" 2> /dev/null
} || { echo "cannot list the changed paths: a git command failed" >&2; exit 2; }
sort -z -u "$TMP/paths.raw" > "$TMP/paths.txt" || { echo "cannot sort the changed paths" >&2; exit 2; }
s1=""
while IFS= read -r -d '' p || [ -n "$p" ]; do
  [ -n "$p" ] || continue
  shown=${p//$'\n'/\\n}
  case "$p" in
    "$SPEC"|.planning/*) ;;
    *) [ -n "$s1" ] || s1="$shown" ;;
  esac
done < "$TMP/paths.txt"
if [ -n "$s1" ]; then
  fail S1 "path outside the specification and .planning/ changed since $BASE: $s1"
else
  pass S1 "changed paths since $BASE are the specification and .planning/ only"
fi

# T1: the three status lines and, before the reports, the two placeholder sections. In stage reported the status
# lines read "- Independent review: reported", "- Owner dispositions: pending" and "- Blocking findings: N", and
# the two sections are checked by RPS and F1.
t1=""
for lab in "Independent review" "Owner dispositions" "Blocking findings"; do
  n=$(grep -c "^- $lab:" "$NT")
  if [ "$n" -ne 1 ]; then t1="$n lines start with [- $lab:], expected one"; break; fi
  line=$(grep "^- $lab:" "$NT")
  if [ "$STAGE" = reported ]; then
    case "$lab" in
      "Independent review") [ "$line" = "- Independent review: reported" ] || { t1="the status line is [$line], expected [- Independent review: reported] in stage reported"; break; } ;;
      "Owner dispositions") [ "$line" = "- Owner dispositions: pending" ] || { t1="the status line is [$line], expected [- Owner dispositions: pending] in stage reported"; break; } ;;
      *) [[ "$line" =~ ^-\ Blocking\ findings:\ [0-9]{1,6}$ ]] || { t1="the status line is [$line], expected [- Blocking findings: N] in stage reported"; break; } ;;
    esac
  elif [ "$line" != "- $lab: pending" ]; then
    t1="the status line is [$line], expected [- $lab: pending] in stage $STAGE"; break
  fi
done
if [ -z "$t1" ] && [ "$STAGE" != reported ]; then
  got=$(h2_lines "Reports" "$NT" | grep -v '^[[:space:]]*$')
  [ "$got" = "No report has been captured yet." ] || t1="the section Reports does not hold exactly its placeholder sentence"
fi
if [ -z "$t1" ] && [ "$STAGE" != reported ]; then
  got=$(h2_lines "Findings" "$NT" | grep -v '^[[:space:]]*$')
  [ "$got" = "No findings table has been derived yet." ] || t1="the section Findings does not hold exactly its placeholder sentence"
fi
if [ -n "$t1" ]; then
  fail T1 "$t1"
elif [ "$STAGE" = reported ]; then
  pass T1 "the status lines read reported, pending and a blocking count"
else
  pass T1 "the three status lines read pending; Reports and Findings hold only their placeholder sentences"
fi

# H2: the eight H2 headings of the note, each once, in this order (fenced lines do not count).
awk '/^```/ { fence = !fence; next } !fence && /^## / { print }' "$NT" > "$TMP/h2.act"
cat > "$TMP/h2.exp" << 'HEADINGS'
## The text reviewed
## Independence
## Charter
## Severity scale
## Passes
## Reports
## Findings
## Requestor notes
HEADINGS
h2=""
while IFS= read -r want; do
  n=$(grep -c -x -F -e "$want" "$TMP/h2.act")
  if [ "$n" -ne 1 ]; then h2="the heading [$want] occurs $n times, expected once"; break; fi
done < "$TMP/h2.exp"
if [ -z "$h2" ] && ! cmp -s "$TMP/h2.exp" "$TMP/h2.act"; then
  h2="the H2 headings are not exactly the eight in the stated order (first difference: $(diff "$TMP/h2.exp" "$TMP/h2.act" | grep -m1 '^[<>]'))"
fi
if [ -n "$h2" ]; then fail H2 "$h2"; else pass H2 "the eight H2 headings occur once each, in order"; fi

# N1: the Independence section has exactly the six labelled bullets in order.
n1=""
mapfile -t ind < <(h2_lines "Independence" "$NT" | grep -v '^[[:space:]]*$')
ind_labels=("Requestor" "Reviewer" "Reviewer version" "Reviewer model" "Invocation" "Requestor role")
if [ "${#ind[@]}" -ne 6 ]; then
  n1="the Independence section has ${#ind[@]} non-blank lines, expected six bullets"
else
  for i in 0 1 2 3 4 5; do
    if [[ "${ind[$i]}" != "- ${ind_labels[$i]}: "* ]]; then n1="bullet $((i + 1)) does not start with [- ${ind_labels[$i]}: ]"; break; fi
  done
fi
[ -n "$n1" ] || [ "${ind[0]}" = "- Requestor: Claude Code" ] || n1="the Requestor bullet is not exactly [- Requestor: Claude Code]"
[ -n "$n1" ] || [ "${ind[1]}" = "- Reviewer: Devin CLI, a different product from a different vendor than the Requestor" ] || n1="the Reviewer bullet is not the fixed sentence"
if [ -z "$n1" ] && [ "$STAGE" = reported ]; then
  rv_ver=${ind[2]#- Reviewer version: }
  rv_model=${ind[3]#- Reviewer model: }
  rv_low=${rv_model,,}
  [[ "$rv_ver" =~ ^[0-9]+(\.[0-9]+)*$ ]] || n1="the Reviewer version [$rv_ver] is not digits and dots (for example 3000.4.25)"
  [ -n "$n1" ] || { [ -n "$rv_model" ] && [ "$rv_model" != pending ]; } || n1="the Reviewer model [$rv_model] is empty or pending"
  if [ -z "$n1" ]; then
    for w in claude fable opus sonnet haiku anthropic; do
      if [[ "$rv_low" == *"$w"* ]]; then n1="the Reviewer model [$rv_model] is a Claude-family model name (contains [$w])"; break; fi
    done
  fi
fi
if [ -n "$n1" ]; then fail N1 "$n1"; else pass N1 "the Independence section has the six labelled bullets in order with the fixed Requestor and Reviewer lines"; fi

# X1: self-containment of the note, in real mode (the real input hashes and the real input files).
msg=$(x1_scan "$NT" "$TMP/real.hashes" "$TMP/real")
if [ -n "$msg" ]; then fail X1 "note: $msg"; else pass X1 "no local path, address, link, scratch reference, unfinished marker or foreign hash-like token"; fi

if [ "$STAGE" = brief ] || [ "$STAGE" = reported ]; then
  readable "$BR" "$BRIEFFILE"

  # V1: the pass table of the brief partitions the text. A heading number is mapped to the line of the heading
  # "## N. " or "### N.M " of the specification (fence-aware), header is line 1, end is the line count plus one.
  prep_ranges
  v1=""
  v1_ranges=""
  mapfile -t pass_ids < <(cut -f1 "$TMP/passes.tsv")
  if [ "${pass_ids[*]}" != "RV-A RV-B RV-C RV-D RV-E RV-X" ]; then
    v1="the pass table does not hold exactly the rows RV-A RV-B RV-C RV-D RV-E RV-X in order"
  else
    mapfile -t pass_from < <(cut -f3 "$TMP/passes.tsv")
    mapfile -t pass_upto < <(cut -f4 "$TMP/passes.tsv")
    [ "${pass_from[0]}" = header ] || v1="RV-A does not start at header"
    [ -n "$v1" ] || [ "${pass_upto[4]}" = end ] || v1="RV-E does not end at end"
    if [ -z "$v1" ]; then
      for i in 0 1 2 3; do
        if [ "${pass_upto[$i]}" != "${pass_from[$((i + 1))]}" ]; then
          v1="${pass_ids[$i]} ends at [${pass_upto[$i]}] but ${pass_ids[$((i + 1))]} starts at [${pass_from[$((i + 1))]}]"
          break
        fi
      done
    fi
    [ -n "$v1" ] || { [ "${pass_from[5]}" = header ] && [ "${pass_upto[5]}" = end ]; } || v1="RV-X does not run from header to end"
    if [ -z "$v1" ]; then
      for i in 0 1 2 3 4 5; do
        a=$(pass_line "${pass_from[$i]}")
        b=$(pass_line "${pass_upto[$i]}")
        if [ -z "$a" ] || [ -z "$b" ]; then v1="${pass_ids[$i]} names a heading [${pass_from[$i]}] or [${pass_upto[$i]}] that the specification does not have"; break; fi
        if [ "$a" -ge "$b" ]; then v1="${pass_ids[$i]} has an empty or inverted range (line $a up to line $b)"; break; fi
        v1_ranges+="${pass_ids[$i]} $a-$((b - 1)); "
      done
    fi
  fi
  if [ -n "$v1" ]; then fail V1 "$v1"; else pass V1 "the pass table partitions the text: ${v1_ranges%; }"; fi

  # B2: no trace of the Requestor's conclusions (the pattern list lives here).
  b2=""
  while IFS='|' read -r label re; do
    hit=$(grep -n -i -E -e "$re" "$BR" | head -n1)
    if [ -n "$hit" ]; then b2="$label at line ${hit%%:*}"; break; fi
  done << 'ANCHORS'
drafting-choice id|(^|[^A-Za-z0-9])DC-[0-9]+
owner-question id|(^|[^A-Za-z0-9])OQ-?[0-9]+
review-finding id|(^|[^A-Za-z])(CR|WR|IN)-?[0-9]{2}([^0-9]|$)
register of drafting choices|register
approval packet|packet
advisory review|advisory
unproven items|unproven
hand-off list|hand-off
expected findings|expected finding
known issues|known issue
earlier review|already reviewed
phase reference|Phase [23]([^0-9]|$)
drafting-phase review file|02-REVIEW
ANCHORS
  if [ -n "$b2" ]; then fail B2 "the brief carries a trace of the Requestor's conclusions: $b2"; else pass B2 "the brief carries no drafting-choice id, review-finding id, register, packet, advisory review, unproven item or expected finding"; fi

  # B3: the project rule of the brief equals the lines of AGENTS.md under Approval and review, joined by spaces.
  rule=$(awk '/^## Approval and review$/ { on = 1; next } /^## / { on = 0 } on && NF' AGENTS.md | sed 's/^[ \t]*//; s/[ \t]*$//' | paste -sd ' ' -)
  n_rule=$(grep -c '^Changes to the English normative specification require' "$BR")
  if [ -z "$rule" ]; then
    fail B3 "AGENTS.md has no text under Approval and review"
  elif [ "$n_rule" -ne 1 ] || ! grep -q -x -F -e "$rule" "$BR"; then
    fail B3 "the project rule of the brief does not equal the text of AGENTS.md under Approval and review"
  else
    pass B3 "the project rule of the brief equals the text of AGENTS.md under Approval and review"
  fi

  # B4: the Expected SHA-256 column of the Inputs table equals --print-input-hashes.
  h2_lines "Inputs" "$BR" | awk -F'|' '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^\| [A-Z]+\.md \|/ { h = trim($(NF - 1)); gsub(/`/, "", h); print trim($2) " " h }
  ' > "$TMP/brief.hashes"
  if cmp -s "$TMP/brief.hashes" "$TMP/real.hashes"; then
    pass B4 "the Expected SHA-256 column equals the four input hashes"
  else
    fail B4 "the Expected SHA-256 column differs from the input hashes (first difference: $(diff "$TMP/real.hashes" "$TMP/brief.hashes" | grep -m1 '^[<>]'))"
  fi

  # B5: encoding and size of the brief.
  b5=$(enc1 "$BR")
  [ -n "$b5" ] || b5=$(enc2 "$BR")
  [ -n "$b5" ] || { [ "$(wc -c < "$BR" | tr -d ' ')" -le 16384 ] || b5="the brief is larger than 16384 bytes"; }
  if [ -n "$b5" ]; then fail B5 "brief: $b5"; else pass B5 "the brief is valid UTF-8 without BOM, LF only, one final LF, no tab, at most 16384 bytes"; fi

  # B6: headings, labels, severity bullets, charter ids and the start prompt.
  b6=""
  awk '/^```/ { fence = !fence; next } !fence && /^## / { print }' "$BR" > "$TMP/brief.h2"
  cat > "$TMP/brief.h2.exp" << 'HEADINGS'
## Your role
## Inputs
## What to evaluate
## Severity scale
## Passes
## Output format
## Rules for this review
## Start prompt
HEADINGS
  cmp -s "$TMP/brief.h2.exp" "$TMP/brief.h2" || b6="the H2 headings are not exactly the eight in the stated order (first difference: $(diff "$TMP/brief.h2.exp" "$TMP/brief.h2" | grep -m1 '^[<>]'))"
  if [ -z "$b6" ]; then
    for lab in "REPORT BEGIN" "REPORT END" "IDENTITY:" "INPUT " "SCOPE:" "COVERAGE:" "FINDINGS:" "FINDING " "SEVERITY:" "REFERENCE:" "SUMMARY:" "REASONING:" "DISPOSITION REQUIRED:" "CHECKS PERFORMED:" "LIMITS:" "VERDICT:"; do
      if ! grep -q -F -e "$lab" "$BR"; then b6="the label [$lab] does not occur"; break; fi
    done
  fi
  if [ -z "$b6" ]; then
    for sev in BLOCKING MAJOR MINOR INFO; do
      if [ "$(grep -c "^- $sev: " "$BR")" -ne 1 ]; then b6="the severity bullet [- $sev: ] does not occur exactly once"; break; fi
    done
  fi
  if [ -z "$b6" ]; then
    for c in C1 C2 C3 C4 C5 C6 C7 C8; do
      if [ "$(grep -c "^- $c " "$BR")" -ne 1 ]; then b6="the charter bullet [- $c ] does not occur exactly once"; break; fi
    done
  fi
  if [ -z "$b6" ]; then
    start=$(h2_lines "Start prompt" "$BR" | grep -v '^[[:space:]]*$')
    want_start='Read BRIEF.md in this directory and carry out pass <PASS> exactly as it describes. Your final message must be the report in the format BRIEF.md defines and nothing else.'
    [ "$start" = "$want_start" ] || b6="the Start prompt section is not exactly the one start-prompt line"
  fi
  if [ -n "$b6" ]; then fail B6 "$b6"; else pass B6 "the eight H2 headings, the sixteen labels, the four severity bullets, the charter ids C1 to C8 and the one start prompt are present"; fi

  # B7: self-containment of the brief, in real mode.
  msg=$(x1_scan "$BR" "$TMP/real.hashes" "$TMP/real")
  if [ -n "$msg" ]; then fail B7 "brief: $msg"; else pass B7 "the brief has no local path, address, link, scratch reference, unfinished marker or foreign hash-like token"; fi

  # N2: the severity bullets, the pass rows and the charter ids of the note equal the brief's.
  n2=""
  h2_lines "Severity scale" "$BR" | grep -E '^- (BLOCKING|MAJOR|MINOR|INFO): ' > "$TMP/sev.brief"
  h2_lines "Severity scale" "$NT" | grep -E '^- (BLOCKING|MAJOR|MINOR|INFO): ' > "$TMP/sev.note"
  if [ "$(wc -l < "$TMP/sev.note" | tr -d ' ')" -ne 4 ] || ! cmp -s "$TMP/sev.brief" "$TMP/sev.note"; then
    n2="the four severity bullets of the note are not the brief's character for character"
  fi
  if [ -z "$n2" ]; then
    cut -f1,2 "$TMP/passes.tsv" > "$TMP/passes.brief"
    h2_lines "Passes" "$NT" | awk -F'|' '
      function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
      /^\| RV-/ { print trim($2) "\t" trim($3) }
    ' > "$TMP/passes.note"
    if [ "$(wc -l < "$TMP/passes.note" | tr -d ' ')" -ne 6 ] || ! cmp -s "$TMP/passes.brief" "$TMP/passes.note"; then
      n2="the six pass rows (Pass and Scope) of the note are not the brief's"
    fi
  fi
  if [ -z "$n2" ]; then
    ids=$(h2_lines "Charter" "$NT" | grep -E '^- C[0-9] ' | cut -d ' ' -f2 | tr '\n' ' ')
    [ "$ids" = "C1 C2 C3 C4 C5 C6 C7 C8 " ] || n2="the Charter section of the note does not hold the bullets C1 to C8 once each, in order"
  fi
  if [ -z "$n2" ] && [ "$(h2_lines "Charter" "$NT" | grep -c -E '^- C[1-8] [^:]+: .+$')" -ne 8 ]; then
    n2="a charter bullet of the note does not have the form [- Cn title: text]"
  fi
  if [ -n "$n2" ]; then fail N2 "$n2"; else pass N2 "the severity bullets, the pass rows and the charter ids of the note equal the brief's"; fi

  # PL1: the pilot inputs carry no repository content.
  mkdir "$TMP/pilot"
  for n in "${INPUT_NAMES[@]}"; do pilot_file "$n" > "$TMP/pilot/$n"; done
  input_hashes pilot > "$TMP/pilot.hashes"
  pl1=""
  for n in SPEC.md BASE.md DECISIONS.md REQUIREMENTS.md; do
    if grep -q -i -F -e "GG-SAD" -e ".planning" -e "docs/" "$TMP/pilot/$n" || grep -q -E 'SPEC-[0-9]' "$TMP/pilot/$n"; then
      pl1="the pilot $n holds a project name, a path or a requirement identifier"
      break
    fi
  done
  if [ -z "$pl1" ]; then
    cat "$TMP/real/SPEC.md" "$TMP/real/BASE.md" "$TMP/real/DECISIONS.md" "$TMP/real/REQUIREMENTS.md" > "$TMP/real.all"
    for n in SPEC.md BASE.md DECISIONS.md REQUIREMENTS.md; do
      awk 'length($0) >= 25' "$TMP/pilot/$n" > "$TMP/pilot.long"
      if [ -s "$TMP/pilot.long" ] && grep -q -F -f "$TMP/pilot.long" "$TMP/real.all"; then
        pl1="a line of 25 or more characters of the pilot $n occurs in the specification, the base text, the decision record or the requirement texts"
        break
      fi
    done
  fi
  if [ -z "$pl1" ]; then
    for n in "${INPUT_NAMES[@]}"; do
      msg=$(enc1 "$TMP/pilot/$n")
      [ -n "$msg" ] || msg=$(enc2 "$TMP/pilot/$n")
      if [ -n "$msg" ]; then pl1="the pilot $n: $msg"; break; fi
    done
  fi
  if [ -n "$pl1" ]; then fail PL1 "$pl1"; else pass PL1 "the four pilot content files carry no project name, path, requirement identifier or 25-character line of the real inputs; the five pilot files pass E1 and E2"; fi

  # PL2: the pilot proves the real format.
  pl2=""
  for sect in "Severity scale" "Output format" "Rules for this review"; do
    h2_lines "$sect" "$TMP/pilot/BRIEF.md" > "$TMP/pl2.pilot"
    h2_lines "$sect" "$BR" > "$TMP/pl2.real"
    if [ ! -s "$TMP/pl2.real" ] || ! cmp -s "$TMP/pl2.pilot" "$TMP/pl2.real"; then pl2="the section [$sect] of the pilot brief is not the brief's byte for byte"; break; fi
  done
  if [ -z "$pl2" ] && [ "$(h2_lines "Passes" "$TMP/pilot/BRIEF.md" | grep -c -E '^\| RV-')" -ne 1 ]; then
    pl2="the pilot Passes table does not have exactly one data row"
  fi
  if [ -z "$pl2" ]; then
    h2_lines "Containment test (pilot only)" "$TMP/pilot/BRIEF.md" | grep -v '^[[:space:]]*$' > "$TMP/pl2.cont"
    if [ "$(wc -l < "$TMP/pl2.cont" | tr -d ' ')" -ne 3 ] || [ "$(grep -c '^- ' "$TMP/pl2.cont")" -ne 3 ]; then
      pl2="the Containment test section does not hold exactly three bullets"
    else
      for phrase in "CANARY FIRST4: " "CANARY READ: succeeded" "CANARY READ: refused" "CANARY READ: not attempted" "FILE CREATE: succeeded" "FILE CREATE: refused" "FILE CREATE: not attempted"; do
        if ! grep -q -F -e "$phrase" "$TMP/pl2.cont"; then pl2="the Containment test section lacks [$phrase]"; break; fi
      done
    fi
  fi
  if [ -z "$pl2" ]; then
    h2_lines "Inputs" "$TMP/pilot/BRIEF.md" | awk -F'|' '
      function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
      /^\| [A-Z]+\.md \|/ { h = trim($(NF - 1)); gsub(/`/, "", h); print trim($2) " " h }
    ' > "$TMP/pl2.hashes"
    cmp -s "$TMP/pl2.hashes" "$TMP/pilot.hashes" || pl2="the pilot Inputs table differs from the pilot input hashes"
  fi
  if [ -n "$pl2" ]; then fail PL2 "$pl2"; else pass PL2 "the pilot brief reuses the severity scale, the output format and the rules of the brief byte for byte and carries the containment test"; fi
fi

if [ "$STAGE" = reported ]; then
  # CT1: the consent trail. The Run set value equals the id that --print-run-set prints for the Reviewer model of
  # the note, the Consent question contains that id and the model, the Consent answer is exactly Consent, and no
  # consent row holds a vertical bar.
  ct1=""
  model=$(grep -m1 '^- Reviewer model: ' "$NT" | sed 's/^- Reviewer model: //')
  if [ -z "$model" ] || [ "$model" = pending ]; then
    ct1="the note names no Reviewer model, so the run set cannot be recomputed"
  else
    want_run=$(print_run_set "$model" | tail -n1)
    want_run=${want_run#Run set: }
    cq=$(pin_tok "$TMP/note.pins" "Consent question")
    if ! [[ "$want_run" =~ ^[0-9a-f]{12}$ ]]; then
      ct1="the run set id for the model [$model] cannot be computed"
    elif [ "$N_RUNSET" != "$want_run" ]; then
      ct1="the Run set value is [$N_RUNSET], the run set of the model [$model] is [$want_run]"
    elif [[ "$cq" != *"$want_run"* ]]; then
      ct1="the Consent question does not contain the run set id"
    elif [[ "$cq" != *"$model"* ]]; then
      ct1="the Consent question does not contain the model name [$model]"
    elif [ "$(pin_tok "$TMP/note.pins" "Consent answer")" != Consent ]; then
      ct1="the Consent answer is not exactly Consent"
    elif [ "$(grep -E '^\| (Run set|Consent question|Consent answer) \|' "$NT" | awk -F'|' 'NF != 4' | wc -l | tr -d ' ')" -ne 0 ]; then
      ct1="a consent row holds a vertical bar"
    fi
  fi
  if [ -n "$ct1" ]; then fail CT1 "$ct1"; else pass CT1 "the Run set value is the run set of the model [$model], the Consent question contains it and the model, the Consent answer is Consent"; fi

  # RPS: the Reports section; then RP1 to RP9 on each quoted report.
  if reports_extract "$TMP/rep"; then
    pass RPS "the Reports section is the fixed introduction and then six quoted blocks in pass order"
    for id in "${PASS_IDS[@]}"; do report_checks "$TMP/rep/$id.txt" "$id"; done

    # F1: the Findings section equals the table derived from the quoted reports.
    print_table "$TMP/rep" | grep -v '^[[:space:]]*$' > "$TMP/f1.exp"
    h2_lines "Findings" "$NT" | grep -v '^[[:space:]]*$' > "$TMP/f1.act"
    if cmp -s "$TMP/f1.exp" "$TMP/f1.act"; then
      pass F1 "the Findings section equals the table derived from the quoted reports ($(wc -l < "$TMP/pt.tsv" | tr -d ' ') findings)"
    else
      fail F1 "the Findings section differs from the table derived from the quoted reports (first difference: $(diff "$TMP/f1.exp" "$TMP/f1.act" | grep -m1 '^[<>]' | cut -c1-160))"
    fi
    n_block=$(awk -F'\t' '$2 == "BLOCKING"' "$TMP/pt.tsv" | wc -l | tr -d ' ')
  else
    fail RPS "$RPS_MSG"
    warn F1 "not evaluated because RPS failed"
    n_block=""
  fi

  # F2: the Blocking findings value equals the count of BLOCKING findings; the Requestor notes are the fixed
  # lines, to which lines beginning "- Check warning: " may be added.
  f2=""
  got=$(grep -m1 '^- Blocking findings: ' "$NT" | sed 's/^- Blocking findings: //')
  if [ -n "$n_block" ] && [ "$got" != "$n_block" ]; then f2="the Blocking findings value is [$got], the quoted reports hold $n_block BLOCKING findings"; fi
  if [ -z "$f2" ]; then
    h2_lines "Requestor notes" "$NT" | grep -v '^[[:space:]]*$' | grep -v '^- Check warning: .' > "$TMP/f2.act"
    cat > "$TMP/f2.exp" << 'NOTES'
- The Requestor checked the format of each report and whether each reference resolves in the pinned text; it did not assess whether any finding is correct.
- Independence rests on the reviewer's different product, vendor and model, on separate sessions that share no context with the Requestor, and on the reviewer's own statement of identity in each report; the repository cannot show more.
- A finding's severity is the reviewer's; only the repository owner dispositions a finding.
This note is evidence only. It does not change the reviewed file.
NOTES
    cmp -s "$TMP/f2.exp" "$TMP/f2.act" || f2="the Requestor notes are not the three fixed bullets and the closing sentence (first difference: $(diff "$TMP/f2.exp" "$TMP/f2.act" | grep -m1 '^[<>]' | cut -c1-120))"
  fi
  if [ -n "$f2" ]; then fail F2 "$f2"; else pass F2 "the Blocking findings value is [$got], equal to the count of BLOCKING findings, and the Requestor notes are the fixed lines"; fi
fi

if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL $FAILS"
exit 1
