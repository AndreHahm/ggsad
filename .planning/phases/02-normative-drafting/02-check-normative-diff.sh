#!/usr/bin/env bash
# Read-only quick check of the proposed normative specification diff.
#
# Usage: 02-check-normative-diff.sh [options]
#   --file PATH         specification to check (default: the specification path below; relative
#                       paths are taken from the repository root)
#   --ref GITREF        read the committed blob GITREF:PATH instead of the working tree
#   --base REF          base ref of the diff (default origin/main); must name a commit
#   --base-blob ID      blob id the specification has at the base (default da29d6f3...)
#   --paths-from FILE   read the changed-path list from FILE (NUL-delimited) instead of from git;
#                       a test hook for the scope checks
#   --section N[.M]     print the numbered heading N[.M] and its body, then exit 0 (exit 2 if the
#                       heading is absent); the body ends at the next heading of the same or a
#                       higher level
#   -h, --help          print this text
#
# Checks: B1 base blob, E1-E3 encoding, S1 S2 scope, N1 normative terms, X1 self-containment,
# R5 section map and structure, R6 base headings kept, R8 qualified "profile" (warning only).
#
# Output: one line per check, "PASS ID message" or "FAIL ID message"; "WARN ID message" lines are
# not counted; then "RESULT: PASS" or "RESULT: FAIL N". Exit 0 on pass, 1 on any failed check,
# 2 on a usage error, an unreadable input, or a failing git listing.
# Nothing is written outside a temporary directory that is removed on exit.

# The awk programs are single-quoted on purpose: their $ and fields must not be expanded.
# shellcheck disable=SC2016
set -u
export LC_ALL=C
export GIT_OPTIONAL_LOCKS=0
cd "$(git rev-parse --show-toplevel)" || { echo "not inside a git repository" >&2; exit 2; }

SPEC="docs/method/GG-SAD_normative_method_specification.md"
DEFAULT_BASE_BLOB="da29d6f3bdef2e88fdd85a762939017d7d7034fa"

FILE="$SPEC"
REF=""
BASE="origin/main"
BASE_BLOB="$DEFAULT_BASE_BLOB"
PATHS_FROM=""
SECTION=""

usage() {
  awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0" >&2
  exit 2
}

need_value() {
  if [ "$#" -lt 2 ] || [ -z "$2" ]; then
    echo "option $1 needs a value" >&2
    exit 2
  fi
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --file) need_value "$@"; FILE="$2"; shift 2 ;;
    --ref) need_value "$@"; REF="$2"; shift 2 ;;
    --base) need_value "$@"; BASE="$2"; shift 2 ;;
    --base-blob) need_value "$@"; BASE_BLOB="$2"; shift 2 ;;
    --paths-from) need_value "$@"; PATHS_FROM="$2"; shift 2 ;;
    --section) need_value "$@"; SECTION="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
done

[[ "$BASE_BLOB" =~ ^[0-9a-f]{40}$ ]] || { echo "--base-blob must be a 40-digit lowercase hexadecimal blob id" >&2; exit 2; }
if [ -n "$SECTION" ]; then
  [[ "$SECTION" =~ ^[0-9]+(\.[0-9]+)*$ ]] || { echo "--section needs a number such as 5 or 5.6" >&2; exit 2; }
fi
git rev-parse --verify --quiet "$BASE^{commit}" > /dev/null || { echo "--base $BASE is not a commit" >&2; exit 2; }
if [ -n "$PATHS_FROM" ]; then
  [ -f "$PATHS_FROM" ] && [ -r "$PATHS_FROM" ] || { echo "cannot read --paths-from $PATHS_FROM" >&2; exit 2; }
fi

TMP=$(mktemp -d) || { echo "cannot create a temporary directory" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT
REC="$TMP/spec"

if [ -n "$REF" ]; then
  git cat-file blob "$REF:$FILE" > "$REC" 2> /dev/null || { echo "cannot read $REF:$FILE" >&2; exit 2; }
else
  [ -f "$FILE" ] && [ -r "$FILE" ] || { echo "cannot read $FILE" >&2; exit 2; }
  cp "$FILE" "$REC" || { echo "cannot read $FILE" >&2; exit 2; }
fi

# --section: print one heading with its body (fences are respected) and stop.
if [ -n "$SECTION" ]; then
  awk -v want="$SECTION" '
    {
      isfence = ($0 ~ /^```/)
      if (!infence && !isfence && $0 ~ /^#+ /) {
        match($0, /^#+/); lvl = RLENGTH
        t = $0; sub(/^#+ +/, "", t); split(t, w, " "); num = w[1]; sub(/\.$/, "", num)
        if (on && lvl <= wl) { on = 0; done = 1 }
        if (!on && !done && num == want) { on = 1; wl = lvl; found = 1 }
      }
      if (on) print
      if (isfence) infence = !infence
    }
    END { exit found ? 0 : 2 }
  ' "$REC"
  rc=$?
  [ "$rc" -ne 2 ] || echo "section $SECTION not found" >&2
  exit "$rc"
fi

# The base text, from the recorded blob: used by R6 and to find the added lines.
git cat-file blob "$BASE_BLOB" > "$TMP/base" 2> /dev/null || { echo "cannot read base blob $BASE_BLOB" >&2; exit 2; }

# Added lines as "number:text" (lines of the checked text that the base does not have).
diff --new-line-format='%dn:%L' --old-line-format='' --unchanged-line-format='' "$TMP/base" "$REC" > "$TMP/added.txt"
[ "$?" -le 1 ] || { echo "cannot compare with the base text" >&2; exit 2; }

FAILS=0
pass() { echo "PASS $1 $2"; }
fail() { echo "FAIL $1 $2"; FAILS=$((FAILS + 1)); }
warn() { echo "WARN $1 $2"; }

# B1: the base blob on the base ref is still the one this phase was drafted against.
base_now=$(git rev-parse --verify --quiet "$BASE:$SPEC" 2> /dev/null) || base_now=""
if [ "$base_now" = "$BASE_BLOB" ]; then
  pass B1 "the specification on $BASE is still blob $BASE_BLOB"
else
  fail B1 "the specification on $BASE is [${base_now:-absent}], expected $BASE_BLOB; the base moved, record the diff identity again"
fi

# E1: no byte order mark; valid UTF-8.
bom=$(head -c3 "$REC" | od -An -tx1 | tr -d ' \n')
if [ "$bom" = efbbbf ]; then
  fail E1 "file starts with a UTF-8 byte order mark"
elif ! iconv -f UTF-8 -t UTF-8 "$REC" > /dev/null 2>&1; then
  fail E1 "file is not valid UTF-8"
else
  pass E1 "valid UTF-8 without BOM"
fi

# E2: LF only; exactly one final LF and no trailing blank line.
if [ "$(tr -cd '\r' < "$REC" | wc -c)" -gt 0 ]; then
  fail E2 "CR byte found (first at line $(tr '\r' '\001' < "$REC" | grep -n -m1 -a $'\001' | cut -d: -f1)); LF only is allowed"
elif [ ! -s "$REC" ]; then
  fail E2 "file is empty"
elif [ "$(tail -c1 "$REC" | od -An -tx1 | tr -d ' \n')" != 0a ]; then
  fail E2 "file does not end with a line feed"
elif ! tail -n1 "$REC" | grep -q '[^[:space:]]'; then
  fail E2 "file ends with a blank line"
else
  pass E2 "LF line endings, one final LF"
fi

# E3: no tab; trailing whitespace only as exactly two spaces after text.
e3=$(awk '
  index($0, "\t") { print "tab at line " NR; exit }
  $0 ~ /[ ]+$/ && $0 !~ /[^ ]  $/ { print "trailing whitespace other than two spaces after text at line " NR; exit }
' "$REC")
if [ -n "$e3" ]; then fail E3 "$e3"; else pass E3 "no tab; trailing whitespace only as two spaces after text"; fi

# S1, S2: every changed path since the base (committed, staged, unstaged, untracked), read
# NUL-delimited. A failing git listing is a usage-level error, never a pass.
if [ -n "$PATHS_FROM" ]; then
  cp "$PATHS_FROM" "$TMP/paths.raw" || { echo "cannot read --paths-from $PATHS_FROM" >&2; exit 2; }
else
  : > "$TMP/paths.raw"
  {
    git diff -z --name-only --no-renames "$BASE...HEAD" >> "$TMP/paths.raw" 2> /dev/null \
      && git diff -z --name-only --no-renames >> "$TMP/paths.raw" 2> /dev/null \
      && git diff -z --name-only --no-renames --cached >> "$TMP/paths.raw" 2> /dev/null \
      && git ls-files -z --others --exclude-standard >> "$TMP/paths.raw" 2> /dev/null
  } || { echo "cannot list the changed paths: a git command failed" >&2; exit 2; }
fi
sort -z -u "$TMP/paths.raw" > "$TMP/paths.txt" || { echo "cannot sort the changed paths" >&2; exit 2; }
s1=""
s2=""
while IFS= read -r -d '' p || [ -n "$p" ]; do
  [ -n "$p" ] || continue
  shown=${p//$'\n'/\\n}
  case "$p" in
    src/*) [ -n "$s1" ] || s1="$shown" ;;
    "$SPEC"|.planning/*) ;;
    *) [ -n "$s2" ] || s2="$shown" ;;
  esac
done < "$TMP/paths.txt"
if [ -n "$s1" ]; then fail S1 "path under src/ changed since $BASE: $s1"; else pass S1 "nothing under src/ changed since $BASE"; fi
if [ -n "$s2" ]; then
  fail S2 "path outside the specification and .planning/ changed since $BASE: $s2"
else
  pass S2 "changed paths since $BASE are the specification and .planning/ only"
fi

# N1: normative terms in added lines. FAIL on SHALL, REQUIRED, RECOMMENDED and malformed forms;
# WARN on lowercase must, should, shall.
awk '
  function snip(s) { return substr(s, 1, 70) }
  {
    p = index($0, ":"); ln = substr($0, 1, p - 1); t = substr($0, p + 1)
    if (t ~ /(^|[^A-Za-z])(SHALL|REQUIRED|RECOMMENDED)([^A-Za-z]|$)/ && !bad)
      { bad = "line " ln ": SHALL, REQUIRED and RECOMMENDED are not normative terms here: " snip(t) }
    else if (t ~ /(^|[^A-Za-z])(MUST|SHOULD) not([^A-Za-z]|$)/ && !bad)
      { bad = "line " ln ": malformed negation, write MUST NOT or SHOULD NOT: " snip(t) }
    else if (t ~ /(^|[^A-Za-z])NOT (MUST|SHOULD|MAY)([^A-Za-z]|$)/ && !bad)
      { bad = "line " ln ": malformed negation, NOT before the term: " snip(t) }
    else if (t ~ /(^|[^A-Za-z])MAY NOT([^A-Za-z]|$)/ && !bad)
      { bad = "line " ln ": MAY NOT is not a normative term: " snip(t) }
    if (t ~ /(^|[^A-Za-z])(must|should|shall)([^A-Za-z]|$)/) warns[++nw] = "line " ln ": lowercase modal: " snip(t)
  }
  END {
    if (bad != "") print "FAIL N1 " bad
    else print "PASS N1 added lines use only MUST, MUST NOT, SHOULD, SHOULD NOT and MAY"
    for (i = 1; i <= nw; i++) print "WARN N1 " warns[i]
  }
' "$TMP/added.txt" > "$TMP/n1.out" || { echo "internal error in N1" >&2; exit 2; }
while IFS= read -r line; do
  echo "$line"
  case "$line" in FAIL*) FAILS=$((FAILS + 1)) ;; esac
done < "$TMP/n1.out"

# X1: self-containment of the whole text (the base is clean): no development identifiers,
# hash-like tokens, addresses, paths or prototype names. WARN on the word "prototype".
x1=""
grep -o -E '[0-9A-Za-z_]+' "$REC" | grep -E '^[0-9A-Fa-f]{7,40}$' | grep '[0-9]' > "$TMP/hex.txt" || true
x1hex=$(head -n1 "$TMP/hex.txt")
if [ -n "$x1hex" ]; then x1="hash-like token [$x1hex]"; fi
if [ -z "$x1" ]; then
  while IFS='|' read -r label re; do
    hit=$(grep -n -E -e "$re" "$REC" | head -n1)
    if [ -n "$hit" ]; then x1="$label at line ${hit%%:*}"; break; fi
  done <<'PATTERNS'
decision or finding identifier|(^|[^A-Za-z0-9])(P|A|O)-[0-9]+
requirement or change identifier|(^|[^A-Za-z0-9])(DEC|SPEC|APPR|REVIEW|ENG|TRUST|INTEG|WORK|VERIFY|DEFER|CHG)-[0-9]+
web address|https?://
drive-letter or home-directory path|(^|[^A-Za-z0-9])[A-Za-z]:[\\/]|/Users/|/home/|~/
development directory|docs/decisions|\.planning/|\.gsd
prototype or planning name|gscore|ggsad-core-proto|MAPPING|MILESTONE-PROPOSAL|BACKLOG
PATTERNS
fi
if [ -n "$x1" ]; then fail X1 "$x1"; else pass X1 "no development identifier, hash-like token, address, path or prototype name"; fi
grep -n -i -E -e 'prototype' "$REC" | cut -c1-80 | while IFS= read -r hit; do
  warn X1 "the word prototype at line ${hit%%:*}"
done > "$TMP/x1warn.out"
cat "$TMP/x1warn.out"

# R5: the section map of 1.1 equals the numbered top-level headings; fences are balanced; every
# table keeps one column count.
awk '
  function fail(msg) { if (bad == "") bad = msg }
  /^```/ { fences++; infence = !infence; intable = 0; next }
  infence { next }
  /^## [0-9]+\. / { heads[substr($0, 4)]++; nh++ }
  /^\| [0-9]+\. / {
    s = substr($0, 3); i = index(s, " | ")
    if (i == 0) fail("line " NR ": malformed map row")
    else { rows[substr(s, 1, i - 1)]++; nr++ }
  }
  /^\|/ {
    t = $0; c = gsub(/\|/, "", t)
    if (!intable) { intable = 1; cols = c; tstart = NR }
    else if (c != cols) fail("line " NR ": table starting at line " tstart " has rows with different column counts")
    next
  }
  { intable = 0 }
  END {
    if (fences % 2 != 0) fail("an odd number of code fences (" fences ")")
    for (h in heads) {
      if (heads[h] > 1) fail("heading [" h "] occurs more than once")
      if (!(h in rows)) fail("heading [" h "] has no row in the section map")
    }
    for (r in rows) {
      if (rows[r] > 1) fail("map row [" r "] occurs more than once")
      if (!(r in heads)) fail("map row [" r "] has no matching heading")
    }
    if (bad != "") print "FAIL R5 " bad
    else print "PASS R5 the section map matches the " nh " numbered headings; fences balanced; table column counts constant"
  }
' "$REC" > "$TMP/r5.out" || { echo "internal error in R5" >&2; exit 2; }
while IFS= read -r line; do
  echo "$line"
  case "$line" in FAIL*) FAILS=$((FAILS + 1)) ;; esac
done < "$TMP/r5.out"

# R6: every heading line of the base is still present, unchanged and in order.
grep -E '^#{1,6} ' "$TMP/base" > "$TMP/base-headings.txt" || true
grep -E '^#{1,6} ' "$REC" > "$TMP/headings.txt" || true
r6=$(awk '
  NR == FNR { b[++n] = $0; next }
  i < n && $0 == b[i + 1] { i++ }
  END { if (i < n) print "base heading [" b[i + 1] "] is missing, retitled, renumbered or out of order" }
' "$TMP/base-headings.txt" "$TMP/headings.txt")
if [ -n "$r6" ]; then fail R6 "$r6"; else pass R6 "every base heading is present, unchanged and in order"; fi

# R8: warning only. Added lines with the word profile that is not qualified as a method profile,
# a compliance profile, or a named profile.
awk '
  {
    p = index($0, ":"); ln = substr($0, 1, p - 1); t = substr($0, p + 1)
    low = tolower(t); off = 0; rest = low
    while ((q = index(rest, "profile")) > 0) {
      pre = substr(low, 1, off + q - 1)
      ok = (pre ~ /(^|[^a-z])(method|compliance|custom|default|selected|active) $/ \
        || pre ~ /`(core|full|lean|standard|governed|regulated)` $/ \
        || pre ~ /_$/)
      if (!ok) { print "WARN R8 line " ln ": profile without a qualifier: " substr(t, 1, 70); break }
      off += q + 6; rest = substr(low, off + 1)
    }
  }
' "$TMP/added.txt" > "$TMP/r8.out" || { echo "internal error in R8" >&2; exit 2; }
if [ -s "$TMP/r8.out" ]; then cat "$TMP/r8.out"; else pass R8 "every added use of profile is qualified"; fi

if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL $FAILS"
exit 1
