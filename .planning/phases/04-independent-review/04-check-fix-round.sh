#!/usr/bin/env bash
# Read-only check of the fix round that follows the independent review of the proposed normative method
# specification: the pins of the text of round 1, whether the live specification still equals them, the replay
# of the three round-1 checks at the commit that holds the round-1 text, the record of the five owner
# decisions D-1 to D-5 with the printers of its questions and of its skeleton, and the edits of the fix round
# with the register that lists them.
#
# Usage: 04-check-fix-round.sh [options]
#   --stage STAGE     state (default): ST1 and the fact line ST2; decisions: FD1 to FD8 on the decisions
#                     record; edits: FE1 to FE6 on the specification and the fix register. The stages
#                     identity, approval-pending and approval-recorded are added to this script by later plans
#                     of the round; the list of stages is open
#   --approval-record PATH
#                     the owner approval record of round 1 (default: the record path of the repository;
#                     relative paths are taken from the repository root)
#   --disposition-record PATH
#                     the review disposition record of round 1 (default: the record path of the repository)
#   --decisions PATH  the record of the owner decisions, read in stage decisions (default: the record path of
#                     the repository)
#   --spec PATH       the specification file to hash or to judge (default: the specification path of the
#                     repository); a test hook that replaces the working file for the hash reads and for the
#                     stage edits only, the index and HEAD reads always use the real path
#   --register PATH   the fix register, read in stage edits (default: the register path of the repository)
#   --complete        modifier of --stage edits: all nine groups must be drafted and the Findings cells of the
#                     register must cover exactly the eleven findings with the disposition fix
#   --base REF        base ref of the diff (default origin/main); must name a commit; in the replay the
#                     remote-tracking ref origin/main of the throwaway clone is set to this commit
#   --replay-round-1  run FR1 to FR4 instead of a stage (no other check runs): FR1 the newest commit reachable
#                     from HEAD at which the specification holds the round-1 blob is found (a commit that does
#                     not touch the specification counts) and holds the approval record and the disposition
#                     record; the commit is never printed. A throwaway clone of the repository is made outside
#                     the repository (a local clone, not a worktree), the commit is checked out detached in it
#                     and origin/main of the clone is aligned; there, with the scripts as they are at that
#                     commit, FR2 the drafting check with --final, FR3 the owner approval check in stage
#                     recorded, FR4 the review check in stage dispositioned each end RESULT: PASS. The clone is
#                     removed on exit; the repository and its refs are not changed
#   --with-current-scripts
#                     modifier of --replay-round-1: the working-tree versions of the three scripts are copied
#                     over the three paths in the clone and the three runs are repeated as FR5 (a later
#                     extension of a script still validates the round-1 evidence)
#   --print-decision-questions
#                     print the five decisions as the owner is asked them: a line with the id and the header,
#                     a line Findings:, the question on one line, one line per option "- label: description"
#                     (the label is the text before the first colon followed by a space), and a blank line
#                     between decisions; exit 0
#   --print-register-skeleton
#                     print the skeleton of the fix register (the only way the register is created): the nine
#                     groups with the status pending and the 14 findings that the owner did not disposition;
#                     exit 0 (exit 2 if the review note cannot be read)
#   --print-decisions-skeleton
#                     print the skeleton of the decisions record (the only way the record is created); every
#                     field that the owner completes holds the fill marker (@@FILL@@); exit 0 (exit 2 if the
#                     records of round 1 cannot be read)
#   -h, --help        print this text and exit 0
#
# Stage state: ST1 the approval record holds exactly one outcome line "- Owner approval: approved" and the pin
# rows Result blob (40 lowercase hexadecimal digits), Reviewed SHA-256 (64) and Line count (an integer), the
# disposition record holds the same three rows, and the values are equal. ST2 is a fact line and not a check:
# "STATE: ..." says whether the working file, the index and HEAD all hold the round-1 blob (all round-1 live
# checks apply) or not (the live checks that pin the round-1 text fail by design; use --replay-round-1).
#
# Stage decisions, on --decisions: FD1 valid UTF-8 without byte order mark, LF only with one final LF and no
# tab, no fill marker outside headings, no local path, web address, link, scratch or transcript word and no
# hash-like token except the round-1 result blob, the round-1 SHA-256 and the blob of the disposition record
# at HEAD; FD2 the structure (the H1, one line each of the two header lines, the four H2 headings in order,
# the seven H3 headings D-1 to D-5, Name and Date in order, the closing line last); FD3 the table of the text
# before the fix round equals the values of the two round-1 records and the blob of the disposition record at
# HEAD; FD4 the Question and Options bullets of each decision equal the printed ones character for character;
# FD5 each Answer is exactly one option label of its decision and each Owner reason is non-empty; FD6 the name
# is non-empty and equals the header line, the date is a valid calendar date (YYYY-MM-DD), equals the header
# line and is not earlier than the owner disposition date of the disposition record, and the two Answer lines
# of the reply details equal them; FD7 the What follows paragraph equals the printed one; FD8 the Findings
# line of each decision equals the printed one and names only findings with the disposition fix in the
# disposition record.
#
# Stage edits, on --spec and --register: the text of round 1 is read with git from the blob that the approval
# record names. A group counts as drafted when the Status cell of its row in the register reads drafted.
# FE1 for each drafted group the old statement is gone and the new facts are present in the places the group
# names, and its examples exist with their tags; FE2 the statements that stay true are unchanged (the sentence
# of Section 22.2 on the actions that can answer blocked, the last cell of every row of both tables of results,
# the realization row of the result blocked, the examples AE-259 and AE-287); FE3 minimality (the first eight
# lines, the quoted sentences of the 14 findings that were not dispositioned, the changed paths, every changed
# line inside a section that the register lists, no tab in an added line); FE4 every removed line that holds
# MUST, SHOULD or MAY is listed in the register with a reason; FE5 the register (layout, fields, quoted
# fragments, sections, examples, encoding, self-containment; with --complete all nine groups and the findings;
# the bullet Notes of an entry may be followed by nested bullets, one per result of the sweep for stale
# statements, and a bullet of the heading "Normative lines removed or reworded" has the form
# "- <first 60 characters of the removed line> :: <reason>", and one of the heading "Findings whose quoted
# sentence an edit touched" the form "- <finding id> :: <reason>");
# FE6 the Phase 2 check ends RESULT: PASS in --final mode on the specification under test.
#
# Output: one line per check, "PASS ID message" or "FAIL ID message"; "WARN ID message" lines and the
# "STATE:" lines are not counted; then "RESULT: PASS" or "RESULT: FAIL N". Exit 0 on pass, 1 on any failed
# check, 2 on a usage error or an unreadable input.
# Nothing is written outside a temporary directory that is removed on exit.

# The printf formats contain backticks on purpose: they are literal text of the printed records.
# The check functions of the groups are called by name; the fixed message texts hold backticks.
# shellcheck disable=SC2016,SC2329

set -u
export LC_ALL=C
export GIT_OPTIONAL_LOCKS=0
cd "$(git rev-parse --show-toplevel)" || { echo "not inside a git repository" >&2; exit 2; }
ROOT=$(pwd)

SPEC="docs/method/GG-SAD_normative_method_specification.md"
CHK=".planning/phases/04-independent-review/04-check-independent-review.sh"
CHK2=".planning/phases/02-normative-drafting/02-check-normative-diff.sh"
CHK3=".planning/phases/03-owner-approval/03-check-owner-approval.sh"
ARC_DEFAULT=".planning/reviews/2026-10-25-normative-spec-owner-approval-record.md"
DREC_DEFAULT=".planning/reviews/2026-10-25-normative-spec-review-disposition-record.md"
NOTE_DEFAULT=".planning/reviews/2026-10-25-normative-spec-independent-review.md"
FREG_DEFAULT=".planning/reviews/2026-10-26-normative-spec-fix-round-register.md"
FDEC_DEFAULT=".planning/reviews/2026-10-26-normative-spec-fix-round-decisions.md"
FILL="@@FILL@@"

STAGE="state"
APPROVAL="$ARC_DEFAULT"
DISPO="$DREC_DEFAULT"
DECISIONS="$FDEC_DEFAULT"
REGISTER="$FREG_DEFAULT"
SPECFILE="$SPEC"
BASE="origin/main"
REPLAY=0
CURRENT=0
PRINT_Q=0
PRINT_SKEL=0
PRINT_REG=0
COMPLETE=0

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
    --stage) need_value "$@"; STAGE="$2"; shift 2 ;;
    --approval-record) need_value "$@"; APPROVAL="$2"; shift 2 ;;
    --disposition-record) need_value "$@"; DISPO="$2"; shift 2 ;;
    --decisions) need_value "$@"; DECISIONS="$2"; shift 2 ;;
    --spec) need_value "$@"; SPECFILE="$2"; shift 2 ;;
    --register) need_value "$@"; REGISTER="$2"; shift 2 ;;
    --complete) COMPLETE=1; shift ;;
    --base) need_value "$@"; BASE="$2"; shift 2 ;;
    --replay-round-1) REPLAY=1; shift ;;
    --with-current-scripts) CURRENT=1; shift ;;
    --print-decision-questions) PRINT_Q=1; shift ;;
    --print-decisions-skeleton) PRINT_SKEL=1; shift ;;
    --print-register-skeleton) PRINT_REG=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$STAGE" in
  state|decisions|edits) ;;
  *) echo "--stage must be state, decisions or edits" >&2; exit 2 ;;
esac
[ "$COMPLETE" -eq 0 ] || { [ "$STAGE" = edits ] && [ "$REPLAY" -eq 0 ]; } || { echo "--complete is used with --stage edits only" >&2; exit 2; }
[ "$CURRENT" -eq 0 ] || [ "$REPLAY" -eq 1 ] || { echo "--with-current-scripts is used with --replay-round-1 only" >&2; exit 2; }

# decision_data: the fixed texts of the five decisions. One record per line, fields separated by a vertical
# bar: "D|id|header|findings" opens a decision, "Q|question" is its question, "O|label|description" is one
# option. No option is recommended; every description has the parts what happens, Gain and Cost.
decision_data() {
  cat << 'DATA'
D|D-1|Reopen pause|RV-A-001, RV-X-002
Q|Section 8.3 says that `reopen` (full profile) waits when the Definition of Wait of the new corrective scope determines a pause. The table of results in the same section says that `reopen` never answers `blocked`, and Section 22.2 lets only the actions that complete a change or a phase, and `resume`, answer `blocked`, so the result of a paused reopen is not determined. The first approval accepted the drafting choice that `reopen` is never blocked. What does a `reopen` answer when the Definition of Wait of its new scope determines a pause?
O|Rejected|nothing is written, `changed` is false and the change stays closed; the request is repeated when the condition is resolved. Gain: the smallest edit, consistent with the accepted drafting choice and with Section 22.2. Cost: the pause itself is not recorded and attempts cannot be counted.
O|Success, then waiting|the reopen takes effect and answers `success`, and the change returns to the resume phase with the status `waiting`. Gain: keeps the intent of the earlier wording of the row, Section 22.2 stays as it is, and the accepted drafting choice that `reopen` never answers `blocked` stays. Cost: a successful action can end in a wait, and the row of the transition table and the sentence after the table of results change.
O|Blocked|the evaluation is recorded, the change stays closed and the result is `blocked` with `changed` true. Gain: attempts become countable, as for `complete` and `resume`. Cost: the largest edit, because the row, the table of results, Section 22.2 and the realization row of the result `blocked` then name `reopen`, and it changes the accepted drafting choice.
D|D-2|Unevaluable gate|RV-A-003
Q|Section 24.2 settles `start` when a gate cannot be evaluated: `start` is rejected and no wait is created. For the other actions that evaluate gates and never answer `blocked` (in the full profile `wait`, `fail`, `cancel`, `supersede` and `reopen`; in the core profile `cancel` and `supersede`, which look for an active hard failure) the result is not stated: Section 24.2 says that the change waits, but a wait is a recorded change that these actions cannot answer under Section 22.2. What do these actions answer when a gate that applies to them cannot be evaluated?
O|Rejected|each of these actions is rejected with `changed` false, nothing is written and no wait is created, as for `start`. Gain: one rule for all of them, no new case of the result `blocked`, and Section 22.2 stays as it is. Cost: a `cancel` or `supersede` cannot proceed while a failure gate it must evaluate cannot be evaluated, and the failed evaluation is not recorded.
O|Cancel proceeds, others rejected|`cancel` and `supersede` take effect and the `not_evaluable` result is recorded, because a gate that cannot be evaluated is never a failure, while `wait`, `fail` and `reopen` are rejected with `changed` false, nothing written and no wait created. Gain: an authorized cancellation is never held up, and Section 22.2 stays as it is. Cost: a hard failure behind a gate that cannot be evaluated is not decided when the change is cancelled or superseded, two rules apply to these actions instead of one, and Section 8.4 and the `cancel` row of Section 23.4 get a clause.
O|Blocked|these actions answer `blocked`: the evaluation is recorded, the change waits as Section 24.2 says and the requested transition does not occur. Gain: the failed evaluation is recorded and attempts are countable, and rule 2 of Section 24.2 applies to every action alike. Cost: the largest edit, because Section 22.2, both tables of results and the realization row of the result `blocked` change, and a `cancel` can leave the change waiting instead of closing it.
D|D-3|Retry limit|RV-B-005
Q|The base text lists exceeding retry limits among the conditions that must terminate the flow. The specification makes a retry limit a soft fail condition: when it is reached the change pauses for a human, who closes it as failed or records a bounded override, and a retry limit that declares the severity hard is invalid. This was a drafting choice accepted in the first approval, and no owner decision speaks to it. Which severity may a retry limit have?
O|Soft, stated openly|a retry limit stays a soft fail condition as accepted; Section 12, where the obligation to terminate is limited, states that reaching a retry limit pauses the flow for a human disposition and that the flow ends as failed unless a human records an override. Gain: wording only, and the accepted drafting choice and the examples stay. Cost: the relaxation of the base text stays, and a reviewer may report it again for the owner's disposition.
O|Author's choice|a retry limit declares the severity hard or soft like any other fail condition; reaching a hard retry limit closes the change as failed, reaching a soft one pauses it. Gain: one rule for all fail conditions, and a project can choose termination without human action. Cost: the rule that a hard retry limit is invalid is removed, some examples change, and the accepted drafting choice changes.
O|Hard only|a retry limit is always a hard fail condition as in the base text; reaching it closes the change as failed without human action, no override applies to it, and a retry limit that declares soft is invalid. Gain: agrees with the base text, so there is no relaxation to state. Cost: it reverses the accepted drafting choice, a retry limit can no longer pause the flow for a human, and several examples change.
D|D-4|Text or binary|RV-E-001
Q|Section 25.2 hashes a text file after line-ending normalisation and a binary file byte for byte, but leaves the decision between text and binary to the implementation and only recommends (SHOULD) that a file is text when its bytes are valid UTF-8 and hold no zero byte. A content hash is therefore comparable only with one computed with the same decision. This was a drafting choice accepted in the first approval. How is the decision made?
O|One rule that must be followed|the recommended rule becomes a requirement (MUST): a file is text exactly when its bytes are valid UTF-8 and hold no zero byte, and binary otherwise. Gain: every conforming implementation computes the same hash for the same bytes, a hash computed by one implementation can be compared with one computed by another, and the edit is small. Cost: a binary format that happens to be valid UTF-8 without a zero byte is treated as text.
O|Recorded with the hash|the implementation keeps its own rule, but every stored content hash of a file is recorded with the kind that was applied (text or binary) and is verified with that kind. Gain: implementations keep their own classification, and a verification always uses the kind that was recorded. Cost: the larger edit, because the definition of the entry of the state document (Section 25.1), the approval and frozen gate records and the examples that show stored hashes change, and two implementations can record different kinds for the same bytes.
D|D-5|Verify-only CI|RV-X-003
Q|Owner decisions O-2 and O-11 bring continuous integration into scope as verify-only: CI checks history integrity and the anchor, that the frozen gates match the approval, that approvals are current and at the required level, and the scope against the base, and that no hard failure is active, and it does not execute the change's own commands with CI's privileges; CI proves the record, not the outcome. The specification names a read-only action `guard` in Sections 22.1 and 23.4 but never says what it checks, and has no other text for this decision. What should the specification carry?
O|Define guard as the verify-only action|a new subsection of Section 22 defines `guard`: read-only in both profiles, the five verifications of the decision, no execution of any command that the change or the project defines, `success` when all hold and `rejected` with issues otherwise, with acceptance examples; running `guard` in a pipeline is the CI integration, and an on-demand guard that enforces hard failures is met by the caller acting on the result. Gain: the decision has normative text, and the later workflow phase has specification text for its CI check. Cost: new normative text, issue codes and examples to be approved and reviewed, in which the Requestor's own drafting readings (listed for the owner at the approval) go beyond the decision.
O|Carry no CI text|the name `guard` is removed from Sections 22.1 and 23.4 and the specification states nothing about CI. Gain: the smallest edit, and no new normative text to approve or review. Cost: the decision has no normative text, which differs from decisions O-1 to O-10, and the later workflow phase has no specification text for its CI check.
DATA
}

NAME_Q='Under which name or handle should these decisions be recorded for the repository owner?'
DATE_Q='Which date are these decisions given? Give it as YYYY-MM-DD.'
H1_LINE='# Fix round decisions: proposed normative method specification'
FOLLOWS_TEXT='The decisions bind the drafting of plans 04-06 and 04-07; every other fix is drafted as a reading of the existing text that the owner sees in the approval packet and may change; the specification is edited only in those plans, and a new owner approval and a new independent review follow; this record is the record of these decisions only.'
CLOSING_LINE='This record is evidence only. It does not change the reviewed file.'
DEC_IDS=(D-1 D-2 D-3 D-4 D-5)

# print_questions: the five decisions as the owner is asked them.
print_questions() {
  local tag a b c first=1
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D) if [ "$first" -eq 0 ]; then printf '\n'; fi; first=0; printf '%s %s\nFindings: %s\n' "$a" "$b" "$c" ;;
      Q) printf '%s\n' "$a" ;;
      O) printf -- '- %s: %s\n' "$a" "$b" ;;
    esac
  done < <(decision_data)
}

# dec_header ID, dec_findings ID, dec_labels ID: parts of one decision.
dec_header() {
  local tag a b c
  while IFS='|' read -r tag a b c; do
    if [ "$tag" = D ] && [ "$a" = "$1" ]; then printf '%s\n' "$b"; return 0; fi
  done < <(decision_data)
}
dec_findings() {
  local tag a b c
  while IFS='|' read -r tag a b c; do
    if [ "$tag" = D ] && [ "$a" = "$1" ]; then printf '%s\n' "$c"; return 0; fi
  done < <(decision_data)
}
dec_labels() {
  local tag a b c cur=""
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D) cur=$a ;;
      O) if [ "$cur" = "$1" ]; then printf '%s\n' "$a"; fi ;;
    esac
  done < <(decision_data)
}

if [ "$PRINT_Q" -eq 1 ]; then
  print_questions
  exit 0
fi

TMP=$(mktemp -d) || { echo "cannot create a temporary directory" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT
AR="$TMP/arc"
DR="$TMP/dispo"
DC="$TMP/decisions"
SP="$TMP/spec"
NT="$TMP/note"
RG="$TMP/register"
T1="$TMP/text1"

readable() {
  if [ -f "$2" ] && [ -r "$2" ] && cp "$2" "$1" 2> /dev/null; then
    return 0
  fi
  echo "cannot read $2" >&2
  exit 2
}

git rev-parse --verify --quiet "$BASE^{commit}" > /dev/null || { echo "--base $BASE is not a commit" >&2; exit 2; }
readable "$AR" "$APPROVAL"
readable "$DR" "$DISPO"
if [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && [ "$STAGE" = decisions ]; then readable "$DC" "$DECISIONS"; fi
if [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && [ "$STAGE" = state ]; then readable "$SP" "$SPECFILE"; fi
if [ "$PRINT_REG" -eq 1 ] || { [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && [ "$STAGE" = edits ]; }; then readable "$NT" "$NOTE_DEFAULT"; fi
if [ "$PRINT_REG" -eq 0 ] && [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && [ "$STAGE" = edits ]; then
  readable "$SP" "$SPECFILE"
  readable "$RG" "$REGISTER"
fi

FAILS=0
pass() { echo "PASS $1 $2"; }
fail() { echo "FAIL $1 $2"; FAILS=$((FAILS + 1)); }

finish() {
  if [ "$FAILS" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
  echo "RESULT: FAIL $FAILS"
  exit 1
}

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

# parse_pins FILE OUT: write one line "label TAB raw cell TAB first backticked token" for every table row of
# FILE before its first H2 heading.
parse_pins() {
  awk '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^## / { exit }
    /^\| / && $0 !~ /^\|[-| ]+\|$/ {
      n = split($0, c, "|")
      label = trim(c[2]); raw = trim(c[3]); tok = ""
      if (match(raw, /`[^`]*`/)) tok = substr(raw, RSTART + 1, RLENGTH - 2)
      if (label != "Field") print label "\t" raw "\t" tok
    }
  ' "$1" > "$2"
}
pin_count() { awk -F'\t' -v l="$2" '$1 == l { n++ } END { print n + 0 }' "$1"; }
pin_tok() { awk -F'\t' -v l="$2" '$1 == l { print $3; exit }' "$1"; }
pin_raw() { awk -F'\t' -v l="$2" '$1 == l { print $2; exit }' "$1"; }

parse_pins "$AR" "$TMP/arc.pins"
parse_pins "$DR" "$TMP/dr.pins"
A_BLOB=$(pin_tok "$TMP/arc.pins" "Result blob")
A_SHA=$(pin_tok "$TMP/arc.pins" "Reviewed SHA-256")
A_LINES=$(pin_tok "$TMP/arc.pins" "Line count")
D_BLOB=$(pin_tok "$TMP/dr.pins" "Result blob")
D_SHA=$(pin_tok "$TMP/dr.pins" "Reviewed SHA-256")
D_LINES=$(pin_tok "$TMP/dr.pins" "Line count")

# drec_fix_ids: the finding ids with the disposition fix in the disposition record, one per line.
drec_fix_ids() {
  awk '/^### / { id = ($2 ~ /^RV-/) ? $2 : "" } /^- Disposition: fix$/ && id != "" { print id; id = "" }' "$DR"
}

# print_skeleton: the decisions record with the fill marker in every field the owner completes.
print_skeleton() {
  local drb tag a b c cur="" n_fix
  drb=$(git rev-parse --verify --quiet "HEAD:$DREC_DEFAULT") || { echo "cannot read the disposition record at HEAD" >&2; exit 2; }
  n_fix=$(drec_fix_ids | wc -l | tr -d ' ')
  printf '%s\n\n' "$H1_LINE"
  printf -- '- Decisions given by: %s\n- Owner decision date: %s\n\n' "$FILL" "$FILL"
  printf '## The text before the fix round\n\n| Field | Value |\n|---|---|\n'
  printf '| Reviewed file | %s |\n' "$(pin_raw "$TMP/arc.pins" "Reviewed file")"
  printf '| Round-1 result blob | %s |\n' "$(pin_raw "$TMP/arc.pins" "Result blob")"
  printf '| Round-1 reviewed SHA-256 | %s |\n' "$(pin_raw "$TMP/arc.pins" "Reviewed SHA-256")"
  printf '| Round-1 line count | %s |\n' "$(pin_raw "$TMP/arc.pins" "Line count")"
  printf '| Round-1 disposition record file | `%s` |\n' "$DREC_DEFAULT"
  printf '| Round-1 disposition record blob | `%s` |\n' "$drb"
  printf '| Findings dispositioned fix | `%s` |\n\n' "$n_fix"
  printf '## Decisions\n\n'
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D)
        if [ -n "$cur" ]; then printf -- '- Answer: %s\n- Owner reason: %s\n\n' "$FILL" "$FILL"; fi
        cur=$a
        printf '### %s — %s\n\n- Findings: %s\n' "$a" "$b" "$c" ;;
      Q) printf -- '- Question: %s\n- Options:\n' "$a" ;;
      O) printf '  - %s: %s\n' "$a" "$b" ;;
    esac
  done < <(decision_data)
  printf -- '- Answer: %s\n- Owner reason: %s\n\n' "$FILL" "$FILL"
  printf '## Reply details\n\n### Name\n\n- Question: %s\n- Answer: %s\n\n### Date\n\n- Question: %s\n- Answer: %s\n\n' "$NAME_Q" "$FILL" "$DATE_Q" "$FILL"
  printf '## What follows\n\n%s\n\n%s\n' "$FOLLOWS_TEXT" "$CLOSING_LINE"
}

# ---- the fix register: data and printer ------------------------------------------------------------------

REG_H1='# Fix register: what changed in the specification and why'
REG_INTRO='This register lists the nine changes made to the specification to fix the eleven findings of the first independent review. A change is a repair when the text had one consistent reading, and my choice when more than one reading was possible; for a choice the other readings are named, so that the owner can pick another one. A choice is a proposal: it becomes the decision of the owner only through the owner approval of the exact new text. The approval packet is printed from this register.'
REG_HEADER='The header of the specification (the Version line and the Revision line) is unchanged by this round.'

# fg_data: one line per group, "id|title|findings|kind".
fg_data() {
  cat << 'DATA'
FG-01|A pause request on a change that has already hit a hard failure|RV-A-002, RV-X-001|repair
FG-02|Re-opening a closed change when its new work would have to wait|RV-A-001, RV-X-002|my choice
FG-03|Starting a change when a check cannot be run|RV-C-001, RV-A-003|repair
FG-04|Cancelling or replacing a change when a check cannot be run|RV-A-003|my choice
FG-05|Which rule decides when a ready condition is not met|RV-D-001|repair
FG-06|Recording a question in the full profile|RV-B-001|repair
FG-07|What happens when a retry limit is reached|RV-B-005|my choice
FG-08|Deciding whether a file is text or binary before hashing it|RV-E-001|my choice
FG-09|The guard check for continuous integration|RV-X-003|my choice
DATA
}

# undisp: the findings of the review note without a disposition, one per line as "id TAB severity TAB quote".
undisp() {
  awk -F'|' '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    /^## / { on = ($0 == "## Findings"); next }
    on && /^\| RV-/ {
      if (trim($6) == "") {
        q = trim($4); sub(/^.*quote "/, "", q); sub(/"$/, "", q)
        print trim($2) "\t" trim($3) "\t" q
      }
    }
  ' "$NT"
}

# print_register_skeleton: the fix register with every field that is filled in later set to pending.
print_register_skeleton() {
  local g t f k id sev
  printf '%s\n\n%s\n\n' "$REG_H1" "$REG_INTRO"
  printf '## The nine changes\n\n| Change | Title | Findings | Kind | Status | Sections | Examples |\n|---|---|---|---|---|---|---|\n'
  while IFS='|' read -r g t f k; do
    printf '| %s | %s | %s | %s | pending | - | - |\n' "$g" "$t" "$f" "$k"
  done < <(fg_data)
  printf '\n## Change details\n\n'
  while IFS='|' read -r g t f k; do
    printf '### %s — %s\n\n- What changed: pending\n- Why: pending\n- My choice: pending\n- Before: pending\n- After: pending\n- Notes: pending\n\n' "$g" "$t"
  done < <(fg_data)
  printf '## Normative lines removed or reworded\n\nNone.\n\n## Findings whose quoted sentence an edit touched\n\nNone.\n\n## Findings not touched\n\n'
  while IFS=$'\t' read -r id sev _; do
    printf -- '- %s (%s): open information; no edit\n' "$id" "$sev"
  done < <(undisp)
  printf '\n## Header\n\n%s\n' "$REG_HEADER"
}

if [ "$PRINT_REG" -eq 1 ]; then
  print_register_skeleton
  exit 0
fi

if [ "$PRINT_SKEL" -eq 1 ]; then
  print_skeleton
  exit 0
fi

# ST1 and ST2: the pins of round 1 and the state of the specification.
state_stage() {
  local m="" n_out n_ok t
  n_out=$(grep -c '^- Owner approval: ' "$AR")
  n_ok=$(grep -c '^- Owner approval: approved$' "$AR")
  if [ "$n_out" -ne 1 ] || [ "$n_ok" -ne 1 ]; then
    m="the approval record does not hold exactly one outcome line [- Owner approval: approved]"
  fi
  for t in "Result blob" "Reviewed SHA-256" "Line count"; do
    if [ -n "$m" ]; then break; fi
    if [ "$(pin_count "$TMP/arc.pins" "$t")" -ne 1 ]; then m="the approval record does not hold the pin row [$t] exactly once"; fi
    if [ "$(pin_count "$TMP/dr.pins" "$t")" -ne 1 ]; then m="the disposition record does not hold the pin row [$t] exactly once"; fi
  done
  if [ -z "$m" ]; then
    if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then m="the result blob of the approval record is not 40 lowercase hexadecimal digits"
    elif ! [[ "$A_SHA" =~ ^[0-9a-f]{64}$ ]]; then m="the SHA-256 of the approval record is not 64 lowercase hexadecimal digits"
    elif ! [[ "$A_LINES" =~ ^[0-9]+$ ]]; then m="the line count of the approval record is not an integer"
    elif [ "$A_BLOB" != "$D_BLOB" ]; then m="the result blob of the disposition record differs from the approval record"
    elif [ "$A_SHA" != "$D_SHA" ]; then m="the SHA-256 of the disposition record differs from the approval record"
    elif [ "$A_LINES" != "$D_LINES" ]; then m="the line count of the disposition record differs from the approval record"
    fi
  fi
  if [ -n "$m" ]; then
    fail ST1 "$m"
    return 0
  fi
  pass ST1 "the approved round-1 text is pinned identically by the approval record and the disposition record (blob, SHA-256, $A_LINES lines)"
  local w i h
  w=$(git hash-object -- "$SPECFILE" 2> /dev/null) || w=""
  i=$(git rev-parse --verify --quiet ":$SPEC" 2> /dev/null) || i=""
  h=$(git rev-parse --verify --quiet "HEAD:$SPEC" 2> /dev/null) || h=""
  if [ "$w" = "$A_BLOB" ] && [ "$i" = "$A_BLOB" ] && [ "$h" = "$A_BLOB" ]; then
    echo "STATE: the specification equals the text of round 1 (all round-1 live checks apply)"
  else
    echo "STATE: the specification differs from the text of round 1 (the live checks that pin the round-1 text fail by design; use --replay-round-1)"
  fi
}

# find_round1_commit BLOB: print the newest commit reachable from HEAD at which the specification holds BLOB.
find_round1_commit() {
  git rev-list HEAD > "$TMP/revs" 2> /dev/null || return 1
  sed "s|\$|:$SPEC|" "$TMP/revs" | git cat-file --batch-check='%(objectname)' > "$TMP/objs" 2> /dev/null
  paste -d' ' "$TMP/revs" "$TMP/objs" | awk -v b="$1" '$2 == b { print $1; exit }'
}

# run_in_clone LABEL SCRIPT [ARGS]: run a script of the clone inside the clone; print its last line in $LAST and
# return 0 when it ended with RESULT: PASS and exit status 0.
run_in_clone() {
  local script=$1 rc
  shift
  (cd "$CL" && bash "$script" "$@") > "$TMP/run.out" 2>&1
  rc=$?
  LAST=$(tail -n1 "$TMP/run.out")
  [ "$rc" -eq 0 ] && [ "$LAST" = "RESULT: PASS" ]
}

# replay: FR1 to FR5.
replay() {
  local c om cm t
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then
    fail FR1 "the result blob of the approval record is not 40 lowercase hexadecimal digits"
    return 0
  fi
  c=$(find_round1_commit "$A_BLOB")
  if [ -z "$c" ]; then
    fail FR1 "no commit reachable from HEAD holds the specification with the round-1 blob"
    return 0
  fi
  if ! git cat-file -e "$c:$ARC_DEFAULT" 2> /dev/null || ! git cat-file -e "$c:$DREC_DEFAULT" 2> /dev/null; then
    fail FR1 "the commit that holds the round-1 text does not hold both round-1 records: the round-1 evidence is not in the history"
    return 0
  fi
  pass FR1 "found the newest commit reachable from HEAD that holds the round-1 text and both round-1 records"
  CL="$TMP/clone"
  if ! git clone --local --no-checkout --quiet -- "$ROOT" "$CL" > /dev/null 2>&1; then
    fail FR1 "the throwaway clone could not be made"
    return 0
  fi
  if ! git -C "$CL" checkout --quiet --detach "$c" > /dev/null 2>&1; then
    fail FR1 "the commit could not be checked out in the throwaway clone"
    return 0
  fi
  om=$(git rev-parse --verify --quiet "$BASE^{commit}")
  cm=$(git -C "$CL" rev-parse --verify --quiet "origin/main^{commit}" 2> /dev/null) || cm=""
  if [ "$cm" != "$om" ]; then
    git -C "$CL" update-ref refs/remotes/origin/main "$om" > /dev/null 2>&1
  fi
  if run_in_clone "$CHK2" --final; then pass FR2 "the drafting check with --final at the round-1 commit: $LAST"; else fail FR2 "the drafting check with --final at the round-1 commit: $LAST"; fi
  if run_in_clone "$CHK3" --stage recorded; then pass FR3 "the owner approval check in stage recorded at the round-1 commit: $LAST"; else fail FR3 "the owner approval check in stage recorded at the round-1 commit: $LAST"; fi
  if run_in_clone "$CHK" --stage dispositioned; then pass FR4 "the review check in stage dispositioned at the round-1 commit: $LAST"; else fail FR4 "the review check in stage dispositioned at the round-1 commit: $LAST"; fi
  if [ "$CURRENT" -eq 1 ]; then
    for t in "$CHK2" "$CHK3" "$CHK"; do
      if ! cp "$t" "$CL/$t" 2> /dev/null; then fail FR5 "the current version of a script could not be copied into the clone"; return 0; fi
    done
    local r2 r3 r4=""
    r2=PASS; r3=PASS; r4=PASS
    run_in_clone "$CHK2" --final || r2="FAIL ($LAST)"
    run_in_clone "$CHK3" --stage recorded || r3="FAIL ($LAST)"
    run_in_clone "$CHK" --stage dispositioned || r4="FAIL ($LAST)"
    if [ "$r2" = PASS ] && [ "$r3" = PASS ] && [ "$r4" = PASS ]; then
      pass FR5 "the current versions of the three scripts also end RESULT: PASS at the round-1 commit"
    else
      fail FR5 "the current versions of the three scripts at the round-1 commit: drafting check $r2, owner approval check $r3, review check $r4"
    fi
  fi
}

# ---- stage decisions -------------------------------------------------------------------------------------

# h2sec FILE NAME: the lines under the H2 heading NAME. h3blk FILE HEADING: the lines under the H3 line HEADING.
h2sec() { awk -v s="$2" '/^## / { on = ($0 == "## " s); next } on' "$1"; }
h3blk() { awk -v h="$2" '/^#+ / { on = ($0 == h); next } on' "$1"; }

# line_val PREFIX FILE: the value of the first line of FILE that begins with PREFIX (the text after the prefix,
# one leading space removed).
line_val() {
  awk -v p="$1" 'index($0, p) == 1 { v = substr($0, length(p) + 1); sub(/^ /, "", v); print v; exit }' "$2"
}

trim_ws() { printf '%s' "$1" | sed 's/^[ ]*//; s/[ ]*$//'; }

decisions_stage() {
  local id hd m lbl ok cnt val exp_q rec_q

  print_skeleton > "$TMP/exp"

  # FD1
  m=$(enc1 "$DC")
  if [ -z "$m" ]; then m=$(enc2 "$DC"); fi
  if [ -z "$m" ] && grep -v '^#' "$DC" | grep -q -F "$FILL"; then
    m="a fill marker is left in a field (line $(grep -n -F "$FILL" "$DC" | head -n1 | cut -d: -f1))"
  fi
  if [ -z "$m" ]; then
    m=$(fd1_scan "$DC")
  fi
  if [ -n "$m" ]; then fail FD1 "$m"; else pass FD1 "encoding, line endings, fill markers and self-containment are in order"; fi

  # FD2
  m=""
  if [ "$(head -n1 "$DC")" != "$H1_LINE" ]; then
    m="the first line is not the H1 [$H1_LINE]"
  elif [ "$(grep -c '^- Decisions given by:' "$DC")" -ne 1 ] || [ "$(grep -c '^- Owner decision date:' "$DC")" -ne 1 ]; then
    m="the lines [- Decisions given by:] and [- Owner decision date:] do not occur exactly once each"
  elif ! cmp -s <(grep '^## ' "$DC") <(grep '^## ' "$TMP/exp"); then
    m="the H2 headings are not the four expected ones in order"
  elif ! cmp -s <(grep '^### ' "$DC") <(grep '^### ' "$TMP/exp"); then
    m="the H3 headings are not D-1 to D-5, Name and Date, once each in order"
  elif [ "$(tail -n1 "$DC")" != "$CLOSING_LINE" ] || [ "$(grep -c -x -F "$CLOSING_LINE" "$DC")" -ne 1 ]; then
    m="the closing line is not the last line, once"
  fi
  if [ -n "$m" ]; then fail FD2 "$m"; else pass FD2 "H1, header lines, four H2 headings, seven H3 headings and the closing line are in order"; fi

  # FD3
  h2sec "$DC" "The text before the fix round" > "$TMP/t.rec"
  h2sec "$TMP/exp" "The text before the fix round" > "$TMP/t.exp"
  if cmp -s "$TMP/t.rec" "$TMP/t.exp"; then
    pass FD3 "the table of the text before the fix round equals the two round-1 records and the disposition record blob at HEAD"
  else
    m=$(diff "$TMP/t.exp" "$TMP/t.rec" | grep '^[<>] |' | head -n1 | cut -c1-60)
    fail FD3 "the table of the text before the fix round differs from the round-1 records (first difference: ${m:-no row})"
  fi

  # FD4, FD5, FD8 per decision
  local bad4="" bad5="" bad8="" fixids
  fixids=$(drec_fix_ids)
  for id in "${DEC_IDS[@]}"; do
    hd="### $id — $(dec_header "$id")"
    h3blk "$DC" "$hd" > "$TMP/b.rec"
    h3blk "$TMP/exp" "$hd" > "$TMP/b.exp"
    exp_q=$(awk '/^- Question: / || /^- Options:$/ || /^  - /' "$TMP/b.exp")
    rec_q=$(awk '/^- Question: / || /^- Options:$/ || /^  - /' "$TMP/b.rec")
    if [ "$exp_q" != "$rec_q" ]; then bad4="$bad4 $id"; fi

    # FD5
    cnt=$(grep -c '^- Answer:' "$TMP/b.rec")
    if [ "$cnt" -ne 1 ]; then
      bad5="$bad5 $id(answer line count $cnt)"
    else
      val=$(line_val "- Answer:" "$TMP/b.rec")
      ok=0
      while IFS= read -r lbl; do
        if [ "$val" = "$lbl" ]; then ok=1; fi
      done < <(dec_labels "$id")
      if [ "$ok" -eq 0 ]; then bad5="$bad5 $id(answer is not an option label)"; fi
    fi
    cnt=$(grep -c '^- Owner reason:' "$TMP/b.rec")
    if [ "$cnt" -ne 1 ]; then
      bad5="$bad5 $id(reason line count $cnt)"
    else
      val=$(line_val "- Owner reason:" "$TMP/b.rec")
      if [ -z "$(trim_ws "$val")" ] || [ "$val" != "$(trim_ws "$val")" ]; then bad5="$bad5 $id(owner reason empty or padded)"; fi
    fi

    # FD8
    val=$(line_val "- Findings:" "$TMP/b.rec")
    cnt=0
    for f in $(printf '%s\n' "$val" | grep -o -E 'RV-[A-Z]-[0-9]{3}'); do
      cnt=$((cnt + 1))
      if ! printf '%s\n' "$fixids" | grep -q -x -F "$f"; then bad8="$bad8 $id($f is not a finding with the disposition fix)"; fi
    done
    if [ "$cnt" -eq 0 ]; then
      bad8="$bad8 $id(names no finding)"
    elif [ "$val" != "$(dec_findings "$id")" ]; then
      bad8="$bad8 $id(findings line differs from the printed one)"
    fi
  done
  if [ -n "$bad4" ]; then fail FD4 "the Question or Options bullets differ from the printed ones in:$bad4"; else pass FD4 "the Question and Options bullets of all five decisions equal the printed ones"; fi
  if [ -n "$bad5" ]; then fail FD5 "answer or reason problems in:$bad5"; else pass FD5 "each Answer is one option label of its decision and each Owner reason is non-empty"; fi

  # FD6
  local nm dt dd nm_a dt_a drdate
  nm=$(line_val "- Decisions given by:" "$DC")
  dt=$(line_val "- Owner decision date:" "$DC")
  h3blk "$DC" "### Name" > "$TMP/n.rec"
  h3blk "$DC" "### Date" > "$TMP/d.rec"
  nm_a=$(line_val "- Answer:" "$TMP/n.rec")
  dt_a=$(line_val "- Answer:" "$TMP/d.rec")
  drdate=$(line_val "- Owner disposition date:" "$DR")
  m=""
  if [ -z "$(trim_ws "$nm")" ] || [ "$nm" != "$(trim_ws "$nm")" ]; then
    m="the name is empty or padded"
  elif [ "$nm_a" != "$nm" ] || [ "$(grep -c '^- Answer:' "$TMP/n.rec")" -ne 1 ]; then
    m="the name answer of the reply details differs from the header line"
  elif ! [[ "$dt" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || [ "$(date -u -d "$dt" +%F 2> /dev/null)" != "$dt" ]; then
    m="the date [$dt] is not a valid calendar date in the form YYYY-MM-DD"
  elif [ "$dt_a" != "$dt" ] || [ "$(grep -c '^- Answer:' "$TMP/d.rec")" -ne 1 ]; then
    m="the date answer of the reply details differs from the header line"
  elif ! [[ "$drdate" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    m="the owner disposition date of the disposition record is not a date"
  elif [[ "$dt" < "$drdate" ]]; then
    m="the date [$dt] is earlier than the owner disposition date of round 1 [$drdate]"
  elif [ "$(grep '^- Question:' "$TMP/n.rec")" != "- Question: $NAME_Q" ] || [ "$(grep '^- Question:' "$TMP/d.rec")" != "- Question: $DATE_Q" ]; then
    m="a question of the reply details differs from the printed one"
  fi
  if [ -n "$m" ]; then fail FD6 "$m"; else pass FD6 "name and date are complete, consistent and not earlier than the round-1 disposition date"; fi

  # FD7
  dd=$(h2sec "$DC" "What follows" | grep -v -x -F "$CLOSING_LINE" | grep -v '^$')
  if [ "$dd" = "$FOLLOWS_TEXT" ]; then pass FD7 "the What follows paragraph equals the printed one"; else fail FD7 "the What follows paragraph differs from the printed one"; fi

  if [ -n "$bad8" ]; then fail FD8 "finding problems in:$bad8"; else pass FD8 "the findings of every decision are findings with the disposition fix in the disposition record"; fi
}

# fd1_scan FILE: print the first self-containment problem of FILE, nothing when there is none.
fd1_scan() {
  local f=$1 label re hit tok
  while IFS='|' read -r label re; do
    hit=$(grep -n -E -e "$re" "$f" | head -n1)
    if [ -n "$hit" ]; then
      echo "$label at line ${hit%%:*}"
      return 0
    fi
  done << 'PATTERNS'
drive-letter or home-directory path|(^|[^A-Za-z0-9])[A-Za-z]:[\\/]|/Users/|/home/|~/
web address|https?://
markdown link|\]\(
temporary directory|/tmp/
scratch, local-data or transcript reference|[Ss][Cc][Rr][Aa][Tt][Cc][Hh][Pp][Aa][Dd]|[Aa][Pp][Pp][Dd][Aa][Tt][Aa]|[Tt][Rr][Aa][Nn][Ss][Cc][Rr][Ii][Pp][Tt]
unfinished-text marker|(^|[^A-Za-z0-9])(TODO|FIXME|TBD|XXX)([^A-Za-z0-9]|$)
PATTERNS
  local drb allowed
  drb=$(git rev-parse --verify --quiet "HEAD:$DREC_DEFAULT") || drb=""
  allowed=" $A_BLOB $A_SHA $drb "
  while IFS= read -r tok; do
    case "$allowed" in
      *" $tok "*) ;;
      *) echo "hash-like token [$tok] that is not one of the round-1 pins or the disposition record blob"; return 0 ;;
    esac
  done < <(grep -o -E '[0-9A-Fa-f]{7,}' "$f" | grep '[0-9]' | sort -u)
  return 0
}

# ---- stage edits -----------------------------------------------------------------------------------------

# rng FILE START END: the lines from the first line that begins with START up to, not including, the next line
# that begins with END.
rng() {
  awk -v s="$2" -v e="$3" '!on { if (index($0, s) == 1) { on = 1; print }; next } index($0, e) == 1 { exit } { print }' "$1"
}

# trow FILE START END ACTION PIPES: the first table row in the range whose first cell begins with the action
# name in backticks and that holds PIPES vertical bars (the transition tables and the tables of results differ
# in their column counts).
trow() {
  rng "$1" "$2" "$3" | awk -v a="| \`$4\` " -v n="$5" 'index($0, a) == 1 { t = $0; if (gsub(/\|/, "|", t) == n) { print; exit } }'
}

# exblock FILE ID: an acceptance example, from its title line to the line before the next example, heading or rule.
exblock() {
  awk -v h="**$2 — " 'on && /^(\*\*AE-|#|---$)/ { exit } index($0, h) == 1 { on = 1 } on' "$1"
}

# has TEXT FRAGMENT: the fragment is a substring of the text.
has() {
  [[ "$1" == *"$2"* ]]
}

# nchars TEXT: the number of characters (not bytes) of the text.
nchars() {
  printf '%s' "$1" | tr -d '\200-\277' | wc -c | tr -d ' '
}

# heads_of FILE: "line TAB number" for every numbered heading outside code fences.
heads_of() {
  awk '/^```/ { f = !f; next } !f && /^#+ [0-9]+(\.[0-9]+)*\.? / { n = $2; sub(/\.$/, "", n); print NR "\t" n }' "$1"
}

# reg_mask: the register with every field that is filled in later replaced by a marker.
reg_mask() {
  awk '
    /^## / { sec = $0; seen[sec] = 0; print; next }
    /^### / { print; next }
    sec == "## The nine changes" && /^\| FG-/ { split($0, c, "|"); printf "|%s|%s|%s|%s|@|@|@|\n", c[2], c[3], c[4], c[5]; next }
    sec == "## Change details" && /^- (What changed|Why|My choice|Before|After|Notes): / { l = $0; sub(/: .*$/, "", l); print l ": @"; next }
    sec == "## Change details" && /^  - / { next }
    sec == "## Normative lines removed or reworded" || sec == "## Findings whose quoted sentence an edit touched" {
      if ($0 != "" && !seen[sec]++) print "@"
      next
    }
    { print }
  '
}

PROB=""
bad() { if [ -z "$PROB" ]; then PROB=$1; fi; }

# ev GROUP LABEL: the value of a bullet of the entry of a group in the register.
ev() {
  awk -F'\t' -v g="$1" -v l="$2" '$1 == g && $2 == l { print substr($0, length($1) + length($2) + 3); exit }' "$TMP/reg.ent"
}

# F1 helpers: F1BAD collects the problems of FE1.
F1BAD=""
f1_note() { if [[ "; $F1BAD;" != *"; $1;"* ]]; then F1BAD="$F1BAD${F1BAD:+; }$1"; fi; }
# f1_gone GROUP NAME FUNCTION FRAGMENT: the fragment is in the place in the round-1 text and not in the new text.
f1_gone() {
  local old new
  old=$("$3" "$T1")
  new=$("$3" "$SP")
  if ! has "$old" "$4"; then
    f1_note "$1: internal: the old fragment [$4] is not in $2 of the round-1 text"
  elif has "$new" "$4"; then
    f1_note "$1: $2 still holds the old statement [$4]"
  fi
}
# f1_has GROUP NAME FUNCTION FRAGMENT: the fragment is in the place in the new text.
f1_has() {
  local new
  new=$("$3" "$SP")
  if [ -z "$new" ]; then
    f1_note "$1: $2 is not found"
  elif ! has "$new" "$4"; then
    f1_note "$1: $2 lacks [$4]"
  fi
}
# f1_same GROUP NAME FUNCTION: the place equals the place in the round-1 text.
f1_same() {
  local old new
  old=$("$3" "$T1")
  new=$("$3" "$SP")
  if [ -z "$old" ] || [ "$old" != "$new" ]; then f1_note "$1: $2 differs from the round-1 text"; fi
}
# f1_ex GROUP ID TAG WORDS...: the example exists with the tag and its Then line holds every word.
f1_ex() {
  local g=$1 id=$2 tag=$3 blk tl w
  shift 3
  blk=$(exblock "$SP" "$id")
  if [ -z "$blk" ]; then f1_note "$g: the example $id does not exist"; return 0; fi
  if ! printf '%s\n' "$blk" | grep -q -x -F -e "- Covers: $tag"; then f1_note "$g: $id lacks the tag [$tag]"; fi
  tl=$(printf '%s\n' "$blk" | grep '^Then ' | head -n1)
  for w in "$@"; do
    if ! has "$tl" "$w"; then f1_note "$g: the Then line of $id lacks [$w]"; fi
  done
}

# places of the checks FE1
p_wait8() { trow "$1" '### 8.3 ' '### 8.4 ' wait 7; }
p_waitres8() { trow "$1" '### 8.3 ' '### 8.4 ' wait 4; }

fe1_FG01() {
  f1_gone FG-01 "the wait row of the transition table of Section 8.3" p_wait8 "or DoF determines failure"
  f1_has FG-01 "the wait row of the transition table of Section 8.3" p_wait8 "Section 24.7"
  f1_has FG-01 "the wait row of the transition table of Section 8.3" p_wait8 "failed"
  f1_same FG-01 "the wait row of the table of results of Section 8.3" p_waitres8
  f1_ex FG-01 AE-295 'Section 8.3 (`wait`)' success failed
}

# para FILE START END KEY: the paragraph (the block of lines between blank lines) in the range that holds KEY.
para() {
  rng "$1" "$2" "$3" | awk -v k="$4" 'BEGIN { RS = "" } index($0, k) > 0 { print; exit }'
}
# f1_is GROUP NAME FUNCTION EXPECTED: the place equals the expected text.
f1_is() {
  local new
  new=$("$3" "$SP")
  if [ "$new" != "$4" ]; then f1_note "$1: $2 is [$new], expected [$4]"; fi
}
# f1_line GROUP NAME FUNCTION FRAGMENT...: one line of the place holds every fragment.
f1_line() {
  local g=$1 name=$2 fn=$3 l w ok
  shift 3
  while IFS= read -r l; do
    ok=1
    for w in "$@"; do
      if ! has "$l" "$w"; then ok=0; break; fi
    done
    if [ "$ok" -eq 1 ]; then return 0; fi
  done < <("$fn" "$SP")
  f1_note "$g: no line of $name holds all of [$*]"
}

# places of the checks FE1 (FG-02 to FG-06)
p_reopen8() { trow "$1" '### 8.3 ' '### 8.4 ' reopen 7; }
p_reopenres8() { trow "$1" '### 8.3 ' '### 8.4 ' reopen 4; }
p_reopenblk8() { p_reopenres8 "$1" | awk -F'|' '{ c = $(NF - 1); gsub(/^ +| +$/, "", c); print c }'; }
p_start8() { trow "$1" '### 8.3 ' '### 8.4 ' start 7; }
p_startres8() { trow "$1" '### 8.3 ' '### 8.4 ' start 4; }
p_start23() { trow "$1" '### 23.4 ' '### 23.5 ' start 5; }
p_cancel23() { trow "$1" '### 23.4 ' '### 23.5 ' cancel 5; }
p_para85() { para "$1" '### 8.5 ' '## 9. ' 'neither failed nor'; }
p_para84() { para "$1" '### 8.4 ' '### 8.5 ' 'DoF retains first priority'; }
p_lines83() { rng "$1" '### 8.3 ' '### 8.4 ' | grep -v '^|'; }
p_lines234() { rng "$1" '### 23.4 ' '### 23.5 ' | grep -v '^|'; }
p_after_hard242() {
  rng "$1" '### 24.2 ' '### 24.3 ' | awk 'BEGIN { RS = "" } f { print; exit } index($0, "A known hard failure therefore outranks") == 1 { f = 1 }'
}
p_rules242() {
  rng "$1" '### 24.2 ' '### 24.3 ' | awk 'index($0, "A known hard failure therefore outranks") == 1 { exit } index($0, "An action that evaluates gates decides from the results in this order") == 1 { on = 1 } on'
}
p_ask248() { para "$1" '### 24.8 ' '### 24.9 ' 'the `ask` action records a question without pausing the change'; }
p_realask() { awk 'index($0, "| Open questions as state |") == 1 { print; exit }' "$1"; }
p_realaskfull() { p_realask "$1" | awk -F'|' '{ print $(NF - 1) }'; }

fe1_FG02() {
  f1_gone FG-02 "the reopen row of the transition table of Section 8.3" p_reopen8 "wait when the new corrective scope's DoW determines a pause"
  f1_has FG-02 "the reopen row of the transition table of Section 8.3" p_reopen8 "DoW"
  f1_has FG-02 "the reopen row of the table of results of Section 8.3" p_reopenres8 "Definition of Wait"
  f1_is FG-02 "the blocked cell of the reopen row of the table of results of Section 8.3" p_reopenblk8 "Never."
  f1_ex FG-02 AE-296 'Section 8.3 (`reopen`)' rejected
}

fe1_FG03() {
  f1_gone FG-03 "the start row of the transition table of Section 23.4" p_start23 "finds no fail gate and no wait gate active"
  f1_has FG-03 "the start row of the transition table of Section 23.4" p_start23 "none of the steps 1 to 4"
  f1_has FG-03 "the start row of the transition table of Section 23.4" p_start23 "cannot be evaluated"
  f1_has FG-03 "the start row of the transition table of Section 8.3" p_start8 "cannot be evaluated"
  f1_has FG-03 "the start row of the table of results of Section 8.3" p_startres8 "cannot be evaluated"
  f1_has FG-03 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "start"
  f1_ex FG-03 AE-297 'Section 8.3 (`start`)' rejected
}

fe1_FG04() {
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "cancel"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "supersede"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "wait"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "fail"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "reopen"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "gate-not-evaluable"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "not_evaluable"
  f1_line FG-04 "the lines of Section 8.3 outside the tables" p_lines83 "Section 24.2" "cannot be evaluated"
  f1_line FG-04 "the lines of Section 23.4 outside the tables" p_lines234 "Section 24.2" "cannot be evaluated"
  f1_has FG-04 "the cancel row of the transition table of Section 23.4" p_cancel23 "cannot be evaluated"
  f1_has FG-04 "the paragraph of Section 8.4 on the priority of the Definition of Fail" p_para84 "cannot be evaluated"
  f1_has FG-04 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "start"
  f1_has FG-04 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "cancel"
  f1_has FG-04 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "Section 24.2"
  f1_ex FG-04 AE-298 'Section 8.3 (`cancel`)' cancelled
  f1_ex FG-04 AE-299 'Section 23.4 (`cancel`)' cancelled
}

fe1_FG05() {
  f1_has FG-05 "the rules of Section 24.2 and the paragraph that follows them" p_rules242 "Definition of Ready"
  f1_has FG-05 "the rules of Section 24.2 and the paragraph that follows them" p_rules242 "Section 8.3"
  f1_ex FG-05 AE-300 'Section 24.2 (full)' blocked
}

fe1_FG06() {
  f1_has FG-06 "the paragraph of Section 24.8 on the action ask" p_ask248 'the action `ask`'
  f1_has FG-06 "the paragraph of Section 24.8 on the action ask" p_ask248 "Section 25.1"
  f1_line FG-06 "the lines of Section 8.3 outside the tables" p_lines83 "approve" "ask" "answer" "adopt" "migrate" "Section 25.1"
  f1_gone FG-06 "the realization row Open questions as state" p_realask "The question is recorded in the state file"
  f1_has FG-06 "the full cell of the realization row Open questions as state" p_realaskfull "ask"
  f1_ex FG-06 AE-301 'Section 24.8 (full)' ask
}

# f1_nounless GROUP NAME FUNCTION: no line of the place that holds retry limit holds the word unless (either case).
f1_nounless() {
  if "$3" "$SP" | grep -F 'retry limit' | grep -q -i -w 'unless'; then f1_note "$1: a retry limit sentence of $2 holds the word unless"; fi
}

# places of the checks FE1 (FG-07 to FG-09)
p_open12() { rng "$1" '## 12. ' '### 12.1 '; }
p_new247() {
  rng "$1" '### 24.7 ' '### 24.8 ' | grep -v -x -F -f <(rng "$T1" '### 24.7 ' '### 24.8 ')
}
p_sec252() { rng "$1" '### 25.2 ' '### 25.3 '; }
p_sec224() { rng "$1" '### 22.4 ' '## 23. '; }
p_order22() { awk '/^### 22\.[0-9]+ / { printf "%s ", $2 }' "$1"; }
p_bullet221() { rng "$1" '### 22.1 ' '### 22.2 ' | grep -F '`guard`'; }
p_read234() { rng "$1" '### 23.4 ' '### 23.5 ' | grep -F 'are read-only'; }

fe1_FG07() {
  f1_has FG-07 "the opening of Section 12" p_open12 "retry limit"
  f1_has FG-07 "the opening of Section 12" p_open12 "soft"
  f1_has FG-07 "the opening of Section 12" p_open12 "Section 24.7"
  f1_line FG-07 "the opening of Section 12" p_open12 "retry limit" "closes the change as failed or records an override"
  f1_line FG-07 "the new lines of Section 24.7" p_new247 "retry limit" "human" "closes the change as failed or records an override"
  f1_nounless FG-07 "the opening of Section 12" p_open12
  f1_nounless FG-07 "the new lines of Section 24.7" p_new247
}

fe1_FG08() {
  f1_line FG-08 "Section 25.2" p_sec252 "MUST" "valid UTF-8" "zero byte"
  f1_gone FG-08 "Section 25.2" p_sec252 "an implementation SHOULD classify a file as text only when"
  f1_gone FG-08 "Section 25.2" p_sec252 "A content hash is therefore comparable only with a content hash that an implementation computed with the same decision"
  f1_ex FG-08 AE-302 'Section 25.2' text binary
}

fe1_FG09() {
  local w
  f1_is FG-09 "the order of the subsections of Section 22" p_order22 "22.1 22.2 22.3 22.4 "
  for w in 'guard' 'MUST NOT' 'Section 24.1' 'Section 24.3' 'Section 24.4' 'Section 24.5' 'Section 24.7' 'success' 'rejected' 'changed' \
    'history-inconsistent' 'anchor-missing' 'gates-changed' 'approval-stale' 'scope-violation' 'hard-failure-active'; do
    f1_has FG-09 "Section 22.4" p_sec224 "$w"
  done
  f1_has FG-09 "the reporting bullet of Section 22.1" p_bullet221 "Section 22.4"
  f1_has FG-09 "the sentence on the read-only actions in Section 23.4" p_read234 "Section 22.4"
  f1_ex FG-09 AE-303 'Section 22.4' success
  f1_ex FG-09 AE-304 'Section 22.4' rejected gates-changed
  f1_ex FG-09 AE-305 'Section 22.4' rejected
}

fe1() {
  local g n=0 fn
  F1BAD=""
  while IFS=$'\t' read -r g _ _ _ st _ _; do
    [ "$st" = drafted ] || continue
    n=$((n + 1))
    fn="fe1_${g//-/}"
    if declare -F "$fn" > /dev/null; then "$fn"; else f1_note "$g: no FE1 checks are defined for this group"; fi
  done < "$TMP/reg.rows"
  if [ -n "$F1BAD" ]; then fail FE1 "$F1BAD"; else pass FE1 "for each of the $n drafted groups the old statement is gone, the new facts are present and the examples exist with their tags"; fi
}

# sent22 FILE: the sentence of Section 22.2 that lists the actions which can answer blocked.
sent22() {
  rng "$1" '### 22.2 ' '### 22.3 ' | awk '{ i = index($0, "Only the actions that complete"); j = index($0, " Every other action answers"); if (i > 0 && j > i) { print substr($0, i, j - i); exit } }'
}
# lastcells FILE START END: the last cell of every row of the table of results in the range (rows of three columns).
lastcells() {
  rng "$1" "$2" "$3" | awk '{ t = $0; if (gsub(/\|/, "|", t) == 4 && $0 !~ /^\|[-|]+\|$/) { n = split($0, c, "|"); print c[n - 1] } }'
}
# realrow FILE: the realization row of the result blocked.
realrow() {
  awk 'index($0, "| The result `blocked` |") == 1 { print; exit }' "$1"
}

fe2() {
  local a b id
  PROB=""
  a=$(sent22 "$T1"); b=$(sent22 "$SP")
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "the sentence of Section 22.2 that lists the actions which can answer blocked is not the round-1 sentence"; fi
  a=$(lastcells "$T1" '### 8.3 ' '### 8.4 '); b=$(lastcells "$SP" '### 8.3 ' '### 8.4 ')
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "a blocked cell (the last cell) of the table of results of Section 8.3 differs from the round-1 text"; fi
  a=$(lastcells "$T1" '### 23.4 ' '### 23.5 '); b=$(lastcells "$SP" '### 23.4 ' '### 23.5 ')
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "a blocked cell (the last cell) of the table of results of Section 23.4 differs from the round-1 text"; fi
  a=$(realrow "$T1"); b=$(realrow "$SP")
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "the realization row of the result blocked differs from the round-1 text"; fi
  for id in AE-259 AE-287; do
    a=$(exblock "$T1" "$id"); b=$(exblock "$SP" "$id")
    if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "the example $id differs from the round-1 text"; fi
  done
  if [ -n "$PROB" ]; then fail FE2 "$PROB"; else pass FE2 "the sentence of Section 22.2, the blocked cells of both tables of results, the realization row of the result blocked and the examples AE-259 and AE-287 equal the round-1 text"; fi
}

# fe_diff: the difference round-1 text to new text as two files, $TMP/d.add ("line TAB text" of the new text) and
# $TMP/d.del ("position TAB text"; the position is the line of the new text at or before the removal).
fe_diff() {
  : > "$TMP/d.add"
  : > "$TMP/d.del"
  diff -U0 "$T1" "$SP" > "$TMP/spec.diff"
  [ "$?" -le 1 ] || { echo "cannot compare the specification with the round-1 text" >&2; exit 2; }
  awk -v add="$TMP/d.add" -v del="$TMP/d.del" '
    /^@@ / { h = $0; sub(/^@@ -[0-9,]+ \+/, "", h); split(h, p, /[ ,]/); c = p[1] + 0; nl = c; inh = 1; next }
    !inh { next }
    /^\+/ { print nl "\t" substr($0, 2) >> add; nl++; next }
    /^-/ { print c "\t" substr($0, 2) >> del }
  ' "$TMP/spec.diff"
}

# listed_sections: the section numbers of the Sections cells of the register, one per line.
listed_sections() {
  awk -F'\t' '$6 != "-" { n = split($6, a, ","); for (i = 1; i <= n; i++) { s = a[i]; gsub(/ /, "", s); if (s != "") print s } }' "$TMP/reg.rows"
}

fe3() {
  local id sev q ln
  PROB=""
  if ! cmp -s <(head -n8 "$T1") <(head -n8 "$SP"); then bad "the first eight lines of the specification (the header) differ from the round-1 text"; fi
  # the quoted sentences of the findings that were not dispositioned
  h2sec "$RG" "Findings whose quoted sentence an edit touched" | grep -o -E '^- RV-[A-Z]-[0-9]{3} :: .+' | cut -d' ' -f2 > "$TMP/touched.ids"
  undisp > "$TMP/undisp.tsv"
  if [ "$(wc -l < "$TMP/undisp.tsv" | tr -d ' ')" -ne 14 ]; then bad "the review note does not hold 14 findings without a disposition"; fi
  while IFS=$'\t' read -r id sev q; do
    if [ -n "$q" ] && ! grep -q -F -e "$q" "$SP" && ! grep -q -x -F -e "$id" "$TMP/touched.ids"; then
      bad "the quoted sentence of the undispositioned finding $id is no longer in the specification and the register lists no reason"
    fi
  done < "$TMP/undisp.tsv"
  # the changed paths
  { git diff --name-only --no-renames "$BASE...HEAD"; git diff --name-only --no-renames HEAD; git ls-files --others --exclude-standard; } 2> /dev/null | sort -u > "$TMP/paths.txt"
  while IFS= read -r ln; do
    [ -n "$ln" ] || continue
    case "$ln" in
      "$SPEC"|.planning/*) ;;
      *) bad "the path [$ln] changed since the base and is neither the specification nor under .planning/" ;;
    esac
  done < "$TMP/paths.txt"
  # a tab in an added line
  if awk -F'\t' 'NF > 2 { found = 1 } END { exit found ? 0 : 1 }' "$TMP/d.add"; then
    bad "an added line of the specification holds a tab"
  fi
  # every changed line lies inside a listed section
  heads_of "$SP" > "$TMP/heads.tsv"
  listed_sections > "$TMP/listed.txt"
  cat "$TMP/d.add" "$TMP/d.del" | awk -F'\t' '
    FILENAME == hf { hl[++nh] = $1; hn[nh] = $2; next }
    FILENAME == lf { ok[$1] = 1; next }
    $2 ~ /^[ ]*$/ { next }
    {
      n = $1 + 0; s = "0"
      for (i = nh; i >= 1; i--) if (hl[i] <= n) { s = hn[i]; break }
      if (!(s in ok)) { print "line " n " lies in section " s; exit }
    }
  ' hf="$TMP/heads.tsv" lf="$TMP/listed.txt" "$TMP/heads.tsv" "$TMP/listed.txt" - > "$TMP/fe3.sec"
  if [ -s "$TMP/fe3.sec" ]; then bad "a changed line is outside the sections listed in the register ($(head -n1 "$TMP/fe3.sec"))"; fi
  if [ -n "$PROB" ]; then fail FE3 "$PROB"; else pass FE3 "the header and the 14 undispositioned findings are untouched, only the specification and .planning/ changed, no added line holds a tab, and every changed line lies in a listed section"; fi
}

# csub TEXT N: the first N characters of the text.
csub() {
  printf '%s' "$1" | awk -v n="$2" '{ cnt = 0; for (i = 1; i <= length($0); i++) { b = substr($0, i, 1); if (b !~ /[\200-\277]/) { cnt++; if (cnt > n) { print substr($0, 1, i - 1); next } } } print $0 }'
}

fe4() {
  local txt key k
  PROB=""
  h2sec "$RG" "Normative lines removed or reworded" | grep -E '^- .* :: .+' > "$TMP/fe4.bullets"
  : > "$TMP/fe4.keys"
  while IFS=$'\t' read -r _ txt; do
    if printf '%s\n' "$txt" | grep -q -E '(^|[^A-Za-z])(MUST|SHOULD|MAY)([^A-Za-z]|$)'; then
      key=$(csub "$txt" 60)
      printf '%s\n' "$key" >> "$TMP/fe4.keys"
      if ! K="- $key :: " awk 'index($0, ENVIRON["K"]) == 1 { f = 1 } END { exit f ? 0 : 1 }' "$TMP/fe4.bullets"; then
        bad "a removed line with MUST, SHOULD or MAY has no register line with a reason: [$key]"
      fi
    fi
  done < "$TMP/d.del"
  while IFS= read -r k; do
    [ -n "$k" ] || continue
    key=${k#- }
    key=${key%% :: *}
    if ! grep -q -x -F -e "$key" "$TMP/fe4.keys"; then echo "WARN FE4 a register line matches no removed line: [$key]"; fi
  done < "$TMP/fe4.bullets"
  if [ -n "$PROB" ]; then fail FE4 "$PROB"; else pass FE4 "every removed line with MUST, SHOULD or MAY has a register line with a reason"; fi
}

fe5() {
  local g kind st secs exs v frag lab lim tok id n=0 top expect last
  local -a toks
  PROB=""
  # the layout and the encoding
  reg_mask < "$RG" > "$TMP/mask.rg"
  print_register_skeleton | reg_mask > "$TMP/mask.sk"
  if ! cmp -s "$TMP/mask.rg" "$TMP/mask.sk"; then
    bad "the layout differs from the printed skeleton (first difference: $(diff "$TMP/mask.sk" "$TMP/mask.rg" | grep '^[<>]' | head -n1 | cut -c1-80))"
  fi
  v=$(enc1 "$RG"); if [ -z "$v" ]; then v=$(enc2 "$RG"); fi
  if [ -n "$v" ]; then bad "$v"; fi
  if [ -z "$PROB" ]; then v=$(fd1_scan "$RG"); if [ -n "$v" ]; then bad "self-containment: $v"; fi; fi
  if [ "$(wc -l < "$TMP/reg.rows" | tr -d ' ')" -ne 9 ]; then bad "the table does not hold nine rows"; fi
  heads_of "$SP" | cut -f2 > "$TMP/headnums.txt"
  : > "$TMP/ids.all"
  while IFS=$'\t' read -r g _ _ kind st secs exs; do
    case "$st" in
      drafted) n=$((n + 1)) ;;
      pending) if [ "$COMPLETE" -eq 1 ]; then bad "$g is not drafted (--complete needs all nine)"; fi; continue ;;
      *) bad "$g: the Status cell is [$st], expected pending or drafted"; continue ;;
    esac
    if [ "$secs" = "-" ] || [ -z "$secs" ]; then bad "$g: the Sections cell is empty"; fi
    for lab in "What changed" "Why" "My choice" "Before" "After" "Notes"; do
      v=$(ev "$g" "$lab")
      if [ -z "$v" ] || [ "$v" = pending ] || has "$v" "$FILL"; then bad "$g: the bullet [$lab] is not filled"; fi
    done
    for lab in "What changed:300" "Why:200" "My choice:450"; do
      v=$(ev "$g" "${lab%:*}"); lim=${lab##*:}
      if [ "$(nchars "$v")" -gt "$lim" ]; then bad "$g: [${lab%:*}] is longer than $lim characters"; fi
      case "$v" in
        *"Section "*|*"AE-"*|*"|"*) bad "$g: [${lab%:*}] holds a section number, an example id or a vertical bar" ;;
      esac
    done
    v=$(ev "$g" "My choice")
    case "$kind" in
      repair) case "$v" in "none:"*) ;; *) bad "$g: a repair must give My choice as [none:] and the reason" ;; esac ;;
      "my choice")
        case "$v" in "none"*) bad "$g: a choice between readings must not give My choice as none" ;; esac
        if ! has "$v" "other"; then bad "$g: My choice does not name the other readings"; fi ;;
    esac
    if [ "$g" = FG-09 ]; then
      for tok in '(1)' '(2)' '(3)' '(4)'; do
        if ! has "$v" "$tok"; then bad "FG-09: My choice lacks the marker $tok of the numbered list of my own readings"; fi
      done
    fi
    for lab in Before After; do
      v=$(ev "$g" "$lab")
      if [ "$lab" = Before ] && [ "$v" = "none (new text)" ]; then continue; fi
      case "$v" in
        \"*\") ;;
        *) bad "$g: [$lab] is not one quoted fragment"; continue ;;
      esac
      frag=${v#\"}; frag=${frag%\"}
      if [ -z "$frag" ] || [ "$(nchars "$frag")" -gt 300 ]; then bad "$g: [$lab] is empty or longer than 300 characters"; continue; fi
      if [ "$lab" = Before ]; then
        grep -q -F -e "$frag" "$T1" || bad "$g: the Before fragment is not a part of a line of the round-1 text"
      else
        grep -q -F -e "$frag" "$SP" || bad "$g: the After fragment is not a part of a line of the new text"
      fi
    done
    IFS=',' read -r -a toks <<< "$secs"
    for tok in "${toks[@]}"; do
      tok=${tok// /}
      grep -q -x -F -e "$tok" "$TMP/headnums.txt" || bad "$g: the Sections cell names [$tok], which is no heading number of the specification"
    done
    if [ "$exs" != "-" ]; then
      IFS=',' read -r -a toks <<< "$exs"
      for tok in "${toks[@]}"; do
        id=${tok// /}
        printf '%s\n' "$id" >> "$TMP/ids.all"
        v=$(exblock "$SP" "$id")
        if [ -z "$v" ] || ! printf '%s\n' "$v" | grep -q '^- Covers: '; then bad "$g: the example $id does not exist with a Covers line"; fi
        if [ "$(grep -c -w -e "$id" "$SP")" -lt 2 ]; then bad "$g: the example $id is not cited"; fi
      done
    fi
  done < "$TMP/reg.rows"
  # the examples run on from AE-295 without a gap or a repeat, and the highest id of the specification ends the run
  sort -t- -k2 -n "$TMP/ids.all" > "$TMP/ids.sorted"
  expect=295
  last=294
  while IFS= read -r id; do
    [ -n "$id" ] || continue
    if [ "$id" != "AE-$expect" ]; then bad "the example ids of the register do not run on from AE-295 without a gap or a repeat (expected AE-$expect, found $id)"; break; fi
    last=$expect
    expect=$((expect + 1))
  done < "$TMP/ids.sorted"
  top=$(grep -o '^\*\*AE-[0-9]*' "$SP" | sed 's/\*\*AE-//' | sort -n | tail -n1)
  if [ "$top" != "$last" ]; then bad "the highest example id of the specification is AE-$top, but the register ends its run at AE-$last"; fi
  if [ "$COMPLETE" -eq 1 ]; then
    if [ "$n" -ne 9 ]; then bad "not all nine groups are drafted"; fi
    cut -f3 "$TMP/reg.rows" | grep -o -E 'RV-[A-Z]-[0-9]{3}' | sort -u > "$TMP/fnd.reg"
    drec_fix_ids | sort -u > "$TMP/fnd.fix"
    if ! cmp -s "$TMP/fnd.reg" "$TMP/fnd.fix"; then bad "the Findings cells of the register do not cover exactly the findings with the disposition fix"; fi
  fi
  if [ -n "$PROB" ]; then fail FE5 "$PROB"; else pass FE5 "the register is intact and its $n drafted entries are consistent with the text"; fi
}

fe6() {
  local args=(--final) out rc last
  if [ "$SPECFILE" != "$SPEC" ]; then args+=(--file "$SPECFILE"); fi
  out=$(bash "$CHK2" "${args[@]}" 2>&1)
  rc=$?
  last=$(printf '%s\n' "$out" | tail -n1)
  if [ "$rc" -eq 0 ] && [ "$last" = "RESULT: PASS" ]; then
    pass FE6 "the Phase 2 check with --final ends RESULT: PASS"
  else
    fail FE6 "the Phase 2 check with --final does not pass: $(printf '%s\n' "$out" | grep '^FAIL' | head -n3 | tr '\n' ';' | cut -c1-300)"
  fi
}

edits_stage() {
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then echo "the result blob of the approval record is not 40 lowercase hexadecimal digits" >&2; exit 2; fi
  git cat-file blob "$A_BLOB" > "$T1" 2> /dev/null || { echo "the round-1 text cannot be read from the repository" >&2; exit 2; }
  awk -v rows="$TMP/reg.rows" -v ent="$TMP/reg.ent" '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    /^## / { sec = $0; cur = ""; next }
    /^### FG-/ { cur = $2; next }
    sec == "## The nine changes" && /^\| FG-/ {
      split($0, c, "|")
      print trim(c[2]) "\t" trim(c[3]) "\t" trim(c[4]) "\t" trim(c[5]) "\t" trim(c[6]) "\t" trim(c[7]) "\t" trim(c[8]) >> rows
      next
    }
    sec == "## Change details" && cur != "" && /^- (What changed|Why|My choice|Before|After|Notes): / {
      l = $0; sub(/^- /, "", l); v = l; sub(/^[^:]*: /, "", v); sub(/:.*$/, "", l)
      print cur "\t" l "\t" v >> ent
    }
  ' "$RG"
  : >> "$TMP/reg.rows"
  : >> "$TMP/reg.ent"
  fe_diff
  fe1
  fe2
  fe3
  fe4
  fe5
  fe6
}

if [ "$REPLAY" -eq 1 ]; then
  replay
  finish
fi

if [ "$STAGE" = state ]; then
  state_stage
  finish
fi

if [ "$STAGE" = edits ]; then
  edits_stage
  finish
fi

decisions_stage
finish
