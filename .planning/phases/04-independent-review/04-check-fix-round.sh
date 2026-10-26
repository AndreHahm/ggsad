#!/usr/bin/env bash
# Read-only check of the fix round that follows the independent review of the proposed normative method
# specification: the pins of the text of round 1, whether the live specification still equals them, the replay
# of the three round-1 checks at the commit that holds the round-1 text, and the record of the five owner
# decisions D-1 to D-5 with the printers of its questions and of its skeleton.
#
# Usage: 04-check-fix-round.sh [options]
#   --stage STAGE     state (default): ST1 and the fact line ST2; decisions: FD1 to FD8 on the decisions
#                     record. The stages edits, identity, approval-pending and approval-recorded are added to
#                     this script by later plans of the round; the list of stages is open
#   --approval-record PATH
#                     the owner approval record of round 1 (default: the record path of the repository;
#                     relative paths are taken from the repository root)
#   --disposition-record PATH
#                     the review disposition record of round 1 (default: the record path of the repository)
#   --decisions PATH  the record of the owner decisions, read in stage decisions (default: the record path of
#                     the repository)
#   --spec PATH       the specification file to hash (default: the specification path of the repository);
#                     a test hook that replaces the working file for the hash reads only, the index and HEAD
#                     reads always use the real path
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
# Output: one line per check, "PASS ID message" or "FAIL ID message"; "WARN ID message" lines and the
# "STATE:" lines are not counted; then "RESULT: PASS" or "RESULT: FAIL N". Exit 0 on pass, 1 on any failed
# check, 2 on a usage error or an unreadable input.
# Nothing is written outside a temporary directory that is removed on exit.

# The printf formats contain backticks on purpose: they are literal text of the printed records.
# shellcheck disable=SC2016

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
FDEC_DEFAULT=".planning/reviews/2026-10-26-normative-spec-fix-round-decisions.md"
FILL="@@FILL@@"

STAGE="state"
APPROVAL="$ARC_DEFAULT"
DISPO="$DREC_DEFAULT"
DECISIONS="$FDEC_DEFAULT"
SPECFILE="$SPEC"
BASE="origin/main"
REPLAY=0
CURRENT=0
PRINT_Q=0
PRINT_SKEL=0

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
    --base) need_value "$@"; BASE="$2"; shift 2 ;;
    --replay-round-1) REPLAY=1; shift ;;
    --with-current-scripts) CURRENT=1; shift ;;
    --print-decision-questions) PRINT_Q=1; shift ;;
    --print-decisions-skeleton) PRINT_SKEL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$STAGE" in
  state|decisions) ;;
  *) echo "--stage must be state or decisions" >&2; exit 2 ;;
esac
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
    if [ "$val" != "$(dec_findings "$id")" ]; then
      bad8="$bad8 $id(findings line differs from the printed one)"
    else
      for f in $(printf '%s\n' "$val" | grep -o -E 'RV-[A-Z]-[0-9]{3}'); do
        if ! printf '%s\n' "$fixids" | grep -q -x -F "$f"; then bad8="$bad8 $id($f is not a fix finding)"; fi
      done
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

if [ "$REPLAY" -eq 1 ]; then
  replay
  finish
fi

if [ "$STAGE" = state ]; then
  state_stage
  finish
fi

decisions_stage
finish
