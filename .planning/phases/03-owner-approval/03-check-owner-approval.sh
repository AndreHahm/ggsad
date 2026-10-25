#!/usr/bin/env bash
# Read-only check of the owner approval packet and, in stage recorded, of the owner approval record.
#
# Usage: 03-check-owner-approval.sh [options]
#   --stage STAGE     pending (default) or recorded. Pending checks the packet before the owner is
#                     asked; recorded checks the packet after the reply and the record of the reply
#   --packet PATH     the owner approval packet (default: the packet path of the repository; relative
#                     paths are taken from the repository root)
#   --record PATH     the owner approval record, read in stage recorded (default: the record path of
#                     the repository)
#   --register PATH   the drafting choices register whose blob the packet pins (default: the register
#                     of the drafting phase)
#   --spec PATH       the specification file to hash (default: the specification path of the
#                     repository); a test hook, the index and HEAD checks always read the real path
#   --base REF        base ref of the diff (default origin/main); must name a commit
#   -h, --help        print this text and exit 0
#
# Checks on the packet: E1 no byte order mark and valid UTF-8, E2 LF only and no tab, P0 the pin
# table, B1 the base blob, R1 the specification equals the result blob in the working file, the index
# and HEAD, H1 SHA-256, line count and diffstat, C1 the count of commits that touch the specification,
# K1 the register blob in the file and in HEAD, I1 the diff identity note agrees with the pins, S1
# every changed path since the base is the specification or under .planning/, T1 the status line, H2
# the twelve H2 headings in order, N1 the question blocks Q01 to Q15 (fields, labels, and the register,
# specification and pin facts that Q01 to Q13 must contain), X1 self-containment: no local path, address,
# link, scratch or transcript reference, unfinished marker or foreign hash-like token.
#
# Output: one line per check, "PASS ID message" or "FAIL ID message"; "WARN ID message" lines are not
# counted; then "RESULT: PASS" or "RESULT: FAIL N". Exit 0 on pass, 1 on any failed check, 2 on a
# usage error or an unreadable input.
# Nothing is written outside a temporary directory that is removed on exit.

set -u
export LC_ALL=C
export GIT_OPTIONAL_LOCKS=0
cd "$(git rev-parse --show-toplevel)" || { echo "not inside a git repository" >&2; exit 2; }

SPEC="docs/method/GG-SAD_normative_method_specification.md"
REG=".planning/phases/02-normative-drafting/02-DRAFTING-CHOICES.md"
PKT_DEFAULT=".planning/reviews/2026-10-25-normative-spec-owner-approval-packet.md"
REC_DEFAULT=".planning/reviews/2026-10-25-normative-spec-owner-approval-record.md"

STAGE="pending"
PACKET="$PKT_DEFAULT"
RECORD="$REC_DEFAULT"
REGISTER="$REG"
SPECFILE="$SPEC"
BASE="origin/main"

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
    --packet) need_value "$@"; PACKET="$2"; shift 2 ;;
    --record) need_value "$@"; RECORD="$2"; shift 2 ;;
    --register) need_value "$@"; REGISTER="$2"; shift 2 ;;
    --spec) need_value "$@"; SPECFILE="$2"; shift 2 ;;
    --base) need_value "$@"; BASE="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[ "$STAGE" = pending ] || [ "$STAGE" = recorded ] || { echo "--stage must be pending or recorded" >&2; exit 2; }
git rev-parse --verify --quiet "$BASE^{commit}" > /dev/null || { echo "--base $BASE is not a commit" >&2; exit 2; }
if [ "$STAGE" = recorded ]; then
  echo "--stage recorded (record $RECORD) is not available yet" >&2
  exit 2
fi

TMP=$(mktemp -d) || { echo "cannot create a temporary directory" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT
PK="$TMP/packet"
SP="$TMP/spec"
RG="$TMP/register"

readable() {
  if [ -f "$2" ] && [ -r "$2" ] && cp "$2" "$1" 2> /dev/null; then
    return 0
  fi
  echo "cannot read $2" >&2
  exit 2
}
readable "$PK" "$PACKET"
readable "$SP" "$SPECFILE"
readable "$RG" "$REGISTER"

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

PIN_LABELS=("Reviewed file" "Base blob" "Result blob" "Reviewed SHA-256" "Line count" "Diffstat" "Commits touching the file" "Register file" "Register blob")

parse_pins "$PK" "The text under approval" "$TMP/pkt.pins"
P_REVF=$(pin_tok "$TMP/pkt.pins" "Reviewed file")
P_BASE=$(pin_tok "$TMP/pkt.pins" "Base blob")
P_RES=$(pin_tok "$TMP/pkt.pins" "Result blob")
P_SHA=$(pin_tok "$TMP/pkt.pins" "Reviewed SHA-256")
P_LINES=$(pin_tok "$TMP/pkt.pins" "Line count")
P_DIFF=$(pin_tok "$TMP/pkt.pins" "Diffstat")
P_COMM=$(pin_tok "$TMP/pkt.pins" "Commits touching the file")
P_REGF=$(pin_tok "$TMP/pkt.pins" "Register file")
P_REGB=$(pin_tok "$TMP/pkt.pins" "Register blob")

# E1, E2: encoding of the packet.
msg=$(enc1 "$PK")
if [ -n "$msg" ]; then fail E1 "packet: $msg"; else pass E1 "packet is valid UTF-8 without BOM"; fi
msg=$(enc2 "$PK")
if [ -n "$msg" ]; then fail E2 "packet: $msg"; else pass E2 "packet has LF line endings, one final LF, no tab"; fi

# P0: the pin table has each of the nine labels once, with well-formed values.
p0=""
for l in "${PIN_LABELS[@]}"; do
  n=$(pin_count "$TMP/pkt.pins" "$l")
  if [ "$n" -ne 1 ]; then p0="the pin table has $n rows labelled [$l], expected one"; break; fi
done
if [ -z "$p0" ]; then
  extra=$(awk -F'\t' 'BEGIN { split("Reviewed file|Base blob|Result blob|Reviewed SHA-256|Line count|Diffstat|Commits touching the file|Register file|Register blob", a, "|"); for (i in a) ok[a[i]] = 1 } !($1 in ok) { print $1; exit }' "$TMP/pkt.pins")
  [ -z "$extra" ] || p0="the pin table has an unexpected row [$extra]"
fi
if [ -z "$p0" ]; then
  while IFS=$'\t' read -r label raw tok; do
    if [ "$raw" != "\`$tok\`" ]; then p0="the value of [$label] is not one backticked token"; break; fi
  done < "$TMP/pkt.pins"
fi
if [ -z "$p0" ]; then
  [ "$P_REVF" = "$SPEC" ] || p0="Reviewed file is [$P_REVF], expected $SPEC"
  [ -n "$p0" ] || [ "$P_REGF" = "$REG" ] || p0="Register file is [$P_REGF], expected $REG"
  [ -n "$p0" ] || [[ "$P_BASE" =~ ^[0-9a-f]{40}$ ]] || p0="Base blob [$P_BASE] is not 40 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$P_RES" =~ ^[0-9a-f]{40}$ ]] || p0="Result blob [$P_RES] is not 40 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$P_REGB" =~ ^[0-9a-f]{40}$ ]] || p0="Register blob [$P_REGB] is not 40 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$P_SHA" =~ ^[0-9a-f]{64}$ ]] || p0="Reviewed SHA-256 [$P_SHA] is not 64 lowercase hexadecimal digits"
  [ -n "$p0" ] || [[ "$P_LINES" =~ ^[0-9]+$ ]] || p0="Line count [$P_LINES] is not an integer"
  [ -n "$p0" ] || [[ "$P_COMM" =~ ^[0-9]+$ ]] || p0="Commits touching the file [$P_COMM] is not an integer"
  [ -n "$p0" ] || [[ "$P_DIFF" =~ ^[0-9]+\ files?\ changed(,\ [0-9]+\ insertions?\(\+\))?(,\ [0-9]+\ deletions?\(-\))?$ ]] || p0="Diffstat [$P_DIFF] does not have the form of git shortstat"
fi
if [ -n "$p0" ]; then fail P0 "$p0"; else pass P0 "the pin table has the nine rows once, each one backticked well-formed value"; fi

# B1: the specification on the base ref is still the base blob of the packet.
base_now=$(git rev-parse --verify --quiet "$BASE:$SPEC" 2> /dev/null) || base_now=""
if [ -n "$P_BASE" ] && [ "$base_now" = "$P_BASE" ]; then
  pass B1 "the specification on $BASE is still blob $P_BASE"
else
  fail B1 "the specification on $BASE is [${base_now:-absent}], the packet pins [$P_BASE]; the base moved, record the diff identity again"
fi

# R1: the specification equals the result blob in the file, the index and HEAD.
r_file=$(git hash-object --no-filters "$SP")
r_index=$(git ls-files -s -- "$SPEC" 2> /dev/null | awk 'NR == 1 { print $2 }')
r_head=$(git rev-parse --verify --quiet "HEAD:$SPEC" 2> /dev/null) || r_head=""
r1=""
[ "$r_file" = "$P_RES" ] || r1="the specification file has blob $r_file, the packet pins $P_RES (the file differs from the pinned text)"
[ -n "$r1" ] || [ "$r_index" = "$P_RES" ] || r1="the index holds [${r_index:-absent}] for the specification, the packet pins $P_RES (the index differs from the pinned text)"
[ -n "$r1" ] || [ "$r_head" = "$P_RES" ] || r1="HEAD holds [${r_head:-absent}] for the specification, the packet pins $P_RES (HEAD differs from the pinned text)"
if [ -n "$r1" ]; then fail R1 "$r1"; else pass R1 "the specification file, the index and HEAD all hold blob $P_RES"; fi

# H1: SHA-256, line count and diffstat of the specification equal the packet's.
calc_sha=$(sha256sum < "$SP" | cut -d ' ' -f1)
calc_lines=$(wc -l < "$SP" | tr -d ' ')
calc_diff=""
if [[ "$P_BASE" =~ ^[0-9a-f]{40}$ ]] && git cat-file blob "$P_BASE" > "$TMP/base" 2> /dev/null; then
  calc_diff=$(git diff --no-index --shortstat -- "$TMP/base" "$SP" | sed 's/^ *//')
fi
h1=""
[ "$calc_sha" = "$P_SHA" ] || h1="SHA-256 of the specification is $calc_sha, the packet pins [$P_SHA]"
[ -n "$h1" ] || [ "$calc_lines" = "$P_LINES" ] || h1="the specification has $calc_lines lines, the packet pins [$P_LINES]"
[ -n "$h1" ] || [ "$calc_diff" = "$P_DIFF" ] || h1="the diffstat of the specification is [$calc_diff], the packet pins [$P_DIFF]"
if [ -n "$h1" ]; then fail H1 "$h1"; else pass H1 "SHA-256, line count and diffstat of the specification equal the packet's"; fi

# C1: the count of commits since the base that touch the specification equals the packet's.
comm_now=$(git rev-list --count "$BASE..HEAD" -- "$SPEC" 2> /dev/null) || comm_now=""
if [ "$comm_now" = "$P_COMM" ]; then
  pass C1 "$comm_now commits since $BASE touch the specification"
else
  fail C1 "[${comm_now:-unknown}] commits since $BASE touch the specification, the packet pins [$P_COMM]"
fi

# K1: the register equals the register blob in the file and in HEAD.
k_file=$(git hash-object --no-filters "$RG")
k_head=$(git rev-parse --verify --quiet "HEAD:$P_REGF" 2> /dev/null) || k_head=""
k1=""
[ "$k_file" = "$P_REGB" ] || k1="the register file has blob $k_file, the packet pins [$P_REGB]"
[ -n "$k1" ] || [ "$k_head" = "$P_REGB" ] || k1="HEAD holds [${k_head:-absent}] for the register, the packet pins [$P_REGB]"
if [ -n "$k1" ]; then fail K1 "$k1"; else pass K1 "the register file and HEAD both hold blob $P_REGB"; fi

# I1: exactly one diff identity note, and it agrees with the pins.
shopt -s nullglob
idn=(.planning/reviews/*-normative-spec-diff-identity.md)
shopt -u nullglob
i1=""
if [ "${#idn[@]}" -ne 1 ]; then
  i1="found ${#idn[@]} diff identity notes, expected exactly one"
else
  for v in "$P_BASE" "$P_RES" "$P_SHA"; do
    if ! grep -q -F "\`$v\`" "${idn[0]}"; then i1="the diff identity note does not hold \`$v\`"; break; fi
  done
  if [ -z "$i1" ]; then
    idn_lines=$(awk -F'|' '$2 ~ /^ *Line count *$/ { v = $3; gsub(/[ `]/, "", v); print v; exit }' "${idn[0]}")
    [ "$idn_lines" = "$P_LINES" ] || i1="the diff identity note gives [$idn_lines] lines, the packet pins [$P_LINES]"
  fi
fi
if [ -n "$i1" ]; then fail I1 "$i1"; else pass I1 "the diff identity note holds the base blob, the result blob, the SHA-256 and the line count of the packet"; fi

# S1: every changed path since the base (committed, staged, unstaged, untracked), read NUL-delimited, is
# the specification or under .planning/. A failing git listing is a usage-level error, never a pass.
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

# T1: the status line of the packet.
t1=""
want_status="- Owner approval: pending"
[ "$STAGE" = pending ] || want_status="- Owner approval: recorded in the owner approval record"
n_status=$(grep -c '^- Owner approval:' "$PK")
if [ "$n_status" -ne 1 ]; then
  t1="$n_status lines start with [- Owner approval:], expected one"
elif ! grep -q -x -F -e "$want_status" "$PK"; then
  t1="the status line is [$(grep '^- Owner approval:' "$PK")], expected [$want_status]"
elif [ "$(grep -c '^- Owner reply date:' "$PK")" -ne 0 ]; then
  t1="the packet holds a reply date line; the reply belongs in the record only"
elif [ "$(grep -c '^| Reply given by |' "$PK")" -ne 0 ]; then
  t1="the packet holds a Reply given by row; the reply belongs in the record only"
fi
if [ -n "$t1" ]; then fail T1 "$t1"; else pass T1 "the status line is exactly [$want_status]; no reply date, no reply row"; fi

# H2: the twelve H2 headings of the packet, each once, in this order (fenced lines do not count).
awk '/^```/ { fence = !fence; next } !fence && /^## / { print }' "$PK" > "$TMP/h2.act"
cat > "$TMP/h2.exp" << 'HEADINGS'
## What you are asked to decide
## The text under approval
## Questions put to the owner
## Review map: SPEC-01 to SPEC-18
## Owner questions OQ-8 to OQ-15
## Exempt set of Section 24.1
## Header and heading
## Drafting choices DC-01 to DC-141
## Dispositions of the review findings
## Recorded findings and flagged items
## Unproven items (informational, for Phase 4)
## Hand-off list (informational, for the engine phases)
HEADINGS
h2=""
while IFS= read -r want; do
  n=$(grep -c -x -F -e "$want" "$TMP/h2.act")
  if [ "$n" -ne 1 ]; then h2="the heading [$want] occurs $n times, expected once"; break; fi
done < "$TMP/h2.exp"
if [ -z "$h2" ] && ! cmp -s "$TMP/h2.exp" "$TMP/h2.act"; then
  h2="the H2 headings are not exactly the twelve in the stated order (first difference: $(diff "$TMP/h2.exp" "$TMP/h2.act" | grep -m1 '^[<>]'))"
fi
if [ -n "$h2" ]; then fail H2 "$h2"; else pass H2 "the twelve H2 headings occur once each, in order"; fi

# qparse FILE SECTION OUT: write one line "kind US id US label US text" (US is the unit separator) for
# every line of the H2 section SECTION that follows an H3 "### Qnn — " question heading. Kind is HEAD for
# a heading, FIELD for a bullet "- Label: text", TEXT for any other line that is not blank.
US=$'\037'
qparse() {
  awk -v sect="$2" -v us="$US" '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^```/ { fence = !fence; next }
    !fence && /^## / { on = ($0 == "## " sect); cur = ""; next }
    !on || fence { next }
    /^### / {
      if (match($0, /^### Q[0-9][0-9] — /)) { cur = substr($0, 5, 3); print "HEAD" us cur us "" us $0 }
      else { cur = ""; print "HEAD" us "??" us "" us $0 }
      seen = 1; next
    }
    !seen || /^[ \t]*$/ { next }
    /^- [A-Za-z][A-Za-z ]*:( |$)/ {
      p = index($0, ":"); print "FIELD" us cur us substr($0, 3, p - 3) us trim(substr($0, p + 1)); next
    }
    { print "TEXT" us cur us "" us $0 }
  ' "$1" > "$3"
}

# qload TSV ORDER HEAD LABELS FIELDS COUNT ERROR: load the output of qparse into arrays and an error text.
# The arrays are associative and reached through name references, which shellcheck does not follow.
# shellcheck disable=SC2004,SC2034
qload() {
  local kind id label text cur="" first
  local -n q_ord=$2 q_head=$3 q_labs=$4 q_fld=$5 q_cnt=$6 q_err=$7
  q_ord=(); q_head=(); q_labs=(); q_fld=(); q_cnt=(); q_err=""
  while IFS="$US" read -r kind id label text; do
    case "$kind" in
      HEAD)
        if [ "$id" = "??" ]; then
          [ -n "$q_err" ] || q_err="malformed question heading [$text]"
          cur=""
        else
          q_cnt[$id]=$(( ${q_cnt[$id]:-0} + 1 ))
          if [ "${q_cnt[$id]}" -eq 1 ]; then q_ord+=("$id"); q_head[$id]=$text; q_labs[$id]=""; fi
          cur=$id
        fi ;;
      FIELD)
        if [ -n "$cur" ]; then
          q_labs[$cur]+="$label|"
          first="${q_fld["$cur|$label"]+set}"
          [ -n "$first" ] || q_fld["$cur|$label"]=$text
        fi ;;
      TEXT) [ -n "$q_err" ] || q_err="unexpected text in ${id:-the section}: [$text]" ;;
    esac
  done < "$1"
}

QIDS=(Q01 Q02 Q03 Q04 Q05 Q06 Q07 Q08 Q09 Q10 Q11 Q12 Q13 Q14 Q15)
QTOPICS=("OQ-8" "OQ-9" "OQ-10" "OQ-11" "OQ-12" "OQ-13" "OQ-14" "OQ-15" "Exempt set" "Header and heading" "Drafting choices" "Recorded findings and flagged items" "Approval" "Reply given by" "Reply date")
QSTAMP=" — "

declare -A PQ_HEAD=() PQ_LABS=() PQ_FLD=() PQ_CNT=()
PQ_ORD=()
PQ_ERR=""
qparse "$PK" "Questions put to the owner" "$TMP/pq.tsv"
qload "$TMP/pq.tsv" PQ_ORD PQ_HEAD PQ_LABS PQ_FLD PQ_CNT PQ_ERR

# The register: Question and Reading cells of OQ-8 to OQ-15, and the number of DC rows.
declare -A REG_Q=() REG_R=()
while IFS="$US" read -r k q r; do
  REG_Q[$k]=$q
  REG_R[$k]=$r
done < <(awk -v us="$US" '
  function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
  /^## / { on = ($0 == "## Owner questions OQ-8 to OQ-15"); next }
  on && /^\| OQ-[0-9]+ \|/ { n = split($0, c, "|"); print trim(c[2]) us trim(c[3]) us trim(c[5]) }
' "$RG")
REG_DC=$(grep -c '^| DC-[0-9][0-9]* |' "$RG")

# Facts of the specification that Q10 names: the Version, the date of the Revision line and the title of section 24.
S_VER=$(head -n 10 "$SP" | sed -n 's/^\*\*Version:\*\* *//p' | head -n1)
S_REVD=$(head -n 10 "$SP" | sed -n 's/^\*\*Revision:\*\* *\([0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\).*/\1/p' | head -n1)
S_TITLE=$(sed -n 's/^## 24\. *//p' "$SP" | head -n1)

# N1: the question blocks Q01 to Q15 and what each of them must contain.
n1=""
if [ -n "$PQ_ERR" ]; then
  n1=$PQ_ERR
elif [ "${PQ_ORD[*]}" != "${QIDS[*]}" ]; then
  n1="the question blocks are [${PQ_ORD[*]}], expected exactly [${QIDS[*]}] once each, in order"
else
  for i in "${!QIDS[@]}"; do
    id=${QIDS[$i]}
    if [ "${PQ_CNT[$id]}" -ne 1 ]; then n1="$id occurs ${PQ_CNT[$id]} times, expected once"; break; fi
    if [ "${PQ_HEAD[$id]}" != "### $id${QSTAMP}${QTOPICS[$i]}" ]; then n1="$id: the heading is [${PQ_HEAD[$id]}], expected [### $id${QSTAMP}${QTOPICS[$i]}]"; break; fi
    if [ "$i" -le 12 ]; then want_labs="Header|Question|Accepting answer|Other answer|"; else want_labs="Header|Question|Answer form|"; fi
    if [ "${PQ_LABS[$id]}" != "$want_labs" ]; then n1="$id: the fields are [${PQ_LABS[$id]}], expected [$want_labs] once each, in order"; break; fi
    hdr=${PQ_FLD["$id|Header"]}
    qt=${PQ_FLD["$id|Question"]}
    if [ -z "$hdr" ] || [ -z "$qt" ]; then n1="$id: the Header or the Question is empty"; break; fi
    if [ "${#hdr}" -gt 12 ]; then n1="$id: Header [$hdr] has ${#hdr} characters, at most 12 are allowed"; break; fi
    if [ "$i" -le 12 ]; then
      acc=${PQ_FLD["$id|Accepting answer"]}
      oth=${PQ_FLD["$id|Other answer"]}
      if [ -z "$acc" ] || [ -z "$oth" ] || [ "$acc" = "$oth" ]; then n1="$id: the two answer labels must be non-empty and differ"; break; fi
      if [ "${#acc}" -gt 30 ] || [ "${#oth}" -gt 30 ]; then n1="$id: an answer label has more than 30 characters"; break; fi
    elif [ -z "${PQ_FLD["$id|Answer form"]}" ]; then
      n1="$id: the Answer form is empty"; break
    fi
    if [ "$i" -le 7 ]; then
      k=${QTOPICS[$i]}
      if [ -z "${REG_Q[$k]:-}" ] || [ -z "${REG_R[$k]:-}" ]; then n1="$id: the register has no Question and Reading cells for $k"; break; fi
      [[ "$qt" == *"${REG_Q[$k]}"* ]] || { n1="$id: the question does not contain the register's Question cell of $k"; break; }
      [[ "$qt" == *"${REG_R[$k]}"* ]] || { n1="$id: the question does not contain the register's Reading cell of $k"; break; }
    fi
    case "$id" in
      Q10)
        if [ -z "$S_VER" ] || [ -z "$S_REVD" ] || [ -z "$S_TITLE" ]; then n1="Q10: the specification has no Version, Revision date or section 24 title to compare with"; break; fi
        for v in "$S_VER" "$S_REVD" "$S_TITLE"; do
          [[ "$qt" == *"$v"* ]] || { n1="Q10: the question does not contain [$v] from the specification"; break 2; }
        done ;;
      Q11)
        [[ "$qt" == *"$REG_DC"* ]] || { n1="Q11: the question does not contain the count $REG_DC of the register's DC rows"; break; }
        [ "$acc" = "Accept all $REG_DC" ] || { n1="Q11: the accepting answer is [$acc], expected [Accept all $REG_DC]"; break; } ;;
      Q13)
        for v in "$P_RES" "$P_SHA" "$P_LINES"; do
          [[ "$qt" == *"$v"* ]] || { n1="Q13: the question does not contain the pin [$v]"; break 2; }
        done ;;
    esac
  done
fi
if [ -n "$n1" ]; then fail N1 "$n1"; else pass N1 "Q01 to Q15 are complete and agree with the register, the specification and the pins"; fi

# X1: self-containment of the packet (and, in stage recorded, of the record).
hex_allowed=" $P_BASE $P_RES $P_REGB $P_SHA "
x1=""
x1_files=("$PK")
x1_names=("packet")
for idx in "${!x1_files[@]}"; do
  f=${x1_files[$idx]}
  nm=${x1_names[$idx]}
  while IFS='|' read -r label re; do
    hit=$(grep -n -E -e "$re" "$f" | head -n1)
    if [ -n "$hit" ]; then x1="$nm: $label at line ${hit%%:*}"; break 2; fi
  done << 'PATTERNS'
drive-letter or home-directory path|(^|[^A-Za-z0-9])[A-Za-z]:[\\/]|/Users/|/home/|~/
web address|https?://
markdown link|\]\(
temporary directory|/tmp/
scratch, local-data or transcript reference|[Ss][Cc][Rr][Aa][Tt][Cc][Hh][Pp][Aa][Dd]|[Aa][Pp][Pp][Dd][Aa][Tt][Aa]|[Tt][Rr][Aa][Nn][Ss][Cc][Rr][Ii][Pp][Tt]
unfinished-text marker|(^|[^A-Za-z0-9])(TODO|FIXME|TBD|XXX)([^A-Za-z0-9]|$)|@@FILL@@
PATTERNS
  while IFS= read -r tok; do
    case "$hex_allowed" in
      *" $tok "*) ;;
      *) x1="$nm: hash-like token [$tok] that is not a pin of the packet"; break 2 ;;
    esac
  done < <(grep -o -E '[0-9A-Za-z_]+' "$f" | grep -E '^[0-9A-Fa-f]{7,}$' | grep '[0-9]' | sort -u)
done
if [ -n "$x1" ]; then fail X1 "$x1"; else pass X1 "no local path, address, link, scratch reference, unfinished marker or foreign hash-like token"; fi

if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL $FAILS"
exit 1
