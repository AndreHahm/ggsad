#!/usr/bin/env bash
# Read-only check of the independent review machinery: the pins of the owner-approved text in the review
# note, their tie to the owner approval record, the Phase 3 recorded check and the live specification, and
# the scope, status, encoding and self-containment of the note.
#
# Usage: 04-check-independent-review.sh [options]
#   --stage STAGE     pins (default): the checks listed below. Later stages are added by later plans
#   --note PATH       the review note (default: the note path of the repository; relative paths are taken
#                     from the repository root)
#   --approval-record PATH
#                     the owner approval record (default: the record path of the repository)
#   --approval-packet PATH
#                     the owner approval packet, passed to the Phase 3 check (default: the packet path of
#                     the repository)
#   --spec PATH       the specification file to hash (default: the specification path of the repository);
#                     a test hook, the index and HEAD checks always read the real path
#   --base REF        base ref of the diff (default origin/main); must name a commit
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
NOTE="$NOTE_DEFAULT"
APPROVAL="$ARC_DEFAULT"
PACKET="$APK_DEFAULT"
SPECFILE="$SPEC"
BASE="origin/main"
BRIEFFILE="$BRIEF_DEFAULT"

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
    --note) need_value "$@"; NOTE="$2"; shift 2 ;;
    --approval-record) need_value "$@"; APPROVAL="$2"; shift 2 ;;
    --approval-packet) need_value "$@"; PACKET="$2"; shift 2 ;;
    --spec) need_value "$@"; SPECFILE="$2"; shift 2 ;;
    --base) need_value "$@"; BASE="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[ "$STAGE" = pins ] || { echo "--stage must be pins" >&2; exit 2; }
git rev-parse --verify --quiet "$BASE^{commit}" > /dev/null || { echo "--base $BASE is not a commit" >&2; exit 2; }

TMP=$(mktemp -d) || { echo "cannot create a temporary directory" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT
NT="$TMP/note"
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
input_hashes() {
  local n
  for n in SPEC.md BASE.md DECISIONS.md REQUIREMENTS.md; do
    printf '%s %s\n' "$n" "$(snapshot_input "$n" | sha256sum | cut -d ' ' -f1)"
  done
}

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
      if [ "$(pin_tok "$TMP/note.pins" "$l")" != pending ]; then p0="the row [$l] does not read pending in stage $STAGE"; break; fi
    done
  fi
fi
if [ -n "$p0" ]; then fail P0 "$p0"; else pass P0 "the pin table has the twelve rows once, each one backticked well-formed value, the consent rows pending"; fi

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

# T1: the three status lines and the two placeholder sections.
t1=""
for lab in "Independent review" "Owner dispositions" "Blocking findings"; do
  n=$(grep -c "^- $lab:" "$NT")
  if [ "$n" -ne 1 ]; then t1="$n lines start with [- $lab:], expected one"; break; fi
  if ! grep -q -x -F -e "- $lab: pending" "$NT"; then t1="the status line is [$(grep "^- $lab:" "$NT")], expected [- $lab: pending] in stage $STAGE"; break; fi
done
if [ -z "$t1" ]; then
  got=$(h2_lines "Reports" "$NT" | grep -v '^[[:space:]]*$')
  [ "$got" = "No report has been captured yet." ] || t1="the section Reports does not hold exactly its placeholder sentence"
fi
if [ -z "$t1" ]; then
  got=$(h2_lines "Findings" "$NT" | grep -v '^[[:space:]]*$')
  [ "$got" = "No findings table has been derived yet." ] || t1="the section Findings does not hold exactly its placeholder sentence"
fi
if [ -n "$t1" ]; then fail T1 "$t1"; else pass T1 "the three status lines read pending; Reports and Findings hold only their placeholder sentences"; fi

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
if [ -n "$n1" ]; then fail N1 "$n1"; else pass N1 "the Independence section has the six labelled bullets in order with the fixed Requestor and Reviewer lines"; fi

# X1: self-containment of the note, in real mode (the real input hashes and the real input files).
msg=$(x1_scan "$NT" "$TMP/real.hashes" "$TMP/real")
if [ -n "$msg" ]; then fail X1 "note: $msg"; else pass X1 "no local path, address, link, scratch reference, unfinished marker or foreign hash-like token"; fi

if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL $FAILS"
exit 1
