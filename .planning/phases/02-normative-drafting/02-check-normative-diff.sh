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
#   --ids LIST          comma-separated requirement ids (SPEC-01 to SPEC-18); also runs C1
#   -h, --help          print this text
#
# Checks: B1 base blob, E1-E3 encoding, S1 S2 scope, N1 normative terms, X1 self-containment,
# R2 acceptance example structure and citations (warning only), R3 unfinished-text markers
# (warning only), R5 section map and structure, R6 base headings kept, R7 the old state file name
# and reopen per profile (warning only), R8 qualified "profile" (warning only). With --ids, C1: every listed id is named in the
# subject of a commit since the base that touches the specification (SPEC-13 is covered by S1 and
# S2 and needs no commit), and every such commit starts "docs(02-NN): SPEC-nn" and names only
# known ids; the single header subject of the last plan is accepted and counts toward no id.
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
IDS=""
HEADER_SUBJECT="docs(02-05): header Version 1.4 and revision line (D-12)"

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
    --ids) need_value "$@"; IDS="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
done

[[ "$BASE_BLOB" =~ ^[0-9a-f]{40}$ ]] || { echo "--base-blob must be a 40-digit lowercase hexadecimal blob id" >&2; exit 2; }
if [ -n "$SECTION" ]; then
  [[ "$SECTION" =~ ^[0-9]+(\.[0-9]+)*$ ]] || { echo "--section needs a number such as 5 or 5.6" >&2; exit 2; }
fi
if [ -n "$IDS" ]; then
  [[ "$IDS" =~ ^SPEC-(0[1-9]|1[0-8])(,SPEC-(0[1-9]|1[0-8]))*$ ]] || { echo "--ids needs a comma-separated list of ids from SPEC-01 to SPEC-18" >&2; exit 2; }
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
        if (!on && !done && (num "") == (want "")) { on = 1; wl = lvl; found = 1 }
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

# R2: warning only. Acceptance example structure outside fences: ids unique; every block (from a
# line "**AE-nn" to the next block, heading or rule line) has a Covers line and a Given, a When
# and a Then line.
awk '
  function close_block() {
    if (id == "") return
    if (!cov) print "WARN R2 " id " has no Covers line"
    if (!giv) print "WARN R2 " id " has no Given line"
    if (!whn) print "WARN R2 " id " has no When line"
    if (!thn) print "WARN R2 " id " has no Then line"
    id = ""
  }
  /^```/ { close_block(); infence = !infence; next }
  infence { next }
  /^\*\*AE-[0-9]+ / {
    close_block()
    id = $1; sub(/^\*\*/, "", id)
    if (seen[id]++) print "WARN R2 " id " is defined more than once"
    cov = 0; giv = 0; whn = 0; thn = 0; nblocks++
    next
  }
  /^#+ / || /^---$/ { close_block(); next }
  id != "" {
    if ($0 ~ /^- Covers: /) cov = 1
    else if ($0 ~ /^Given /) giv = 1
    else if ($0 ~ /^When /) whn = 1
    else if ($0 ~ /^Then /) thn = 1
  }
  END { close_block(); if (nblocks == 0) print "NOTE none"; else print "NOTE " nblocks }
' "$REC" > "$TMP/r2.out" || { echo "internal error in R2" >&2; exit 2; }
# R2, citations (warning only): every defined example is cited by a line "See AE-nn", every cited
# example is defined, and every subsection N.M of sections 23 to 25 cites at least one example.
awk '
  /^```/ { infence = !infence; next }
  infence { next }
  /^#+ / {
    cur = ""
    if ($0 ~ /^### (23|24|25)\.[0-9]+ /) { cur = $2; subs[++ns] = cur }
    next
  }
  /^\*\*AE-[0-9]+ / {
    id = $1; sub(/^\*\*/, "", id)
    if (!(id in defd)) { defd[id] = 1; dlist[++nd] = id }
    next
  }
  /[Ss]ee AE-[0-9]+/ {
    t = $0
    while (match(t, /AE-[0-9]+/)) {
      id = substr(t, RSTART, RLENGTH); t = substr(t, RSTART + RLENGTH)
      if (!(id in citd)) { citd[id] = 1; clist[++nc] = id }
    }
    if (cur != "") hasc[cur] = 1
  }
  END {
    for (i = 1; i <= nd; i++) if (!(dlist[i] in citd)) print "WARN R2 " dlist[i] " is defined but no rule line cites it"
    for (i = 1; i <= nc; i++) if (!(clist[i] in defd)) print "WARN R2 " clist[i] " is cited but not defined"
    for (i = 1; i <= ns; i++) if (!(subs[i] in hasc)) print "WARN R2 section " subs[i] " cites no acceptance example"
  }
' "$REC" > "$TMP/r2c.out" || { echo "internal error in R2 citations" >&2; exit 2; }
cat "$TMP/r2.out" "$TMP/r2c.out" | grep '^WARN R2' > "$TMP/r2.warn" || true
if [ -s "$TMP/r2.warn" ]; then
  cat "$TMP/r2.warn"
else
  pass R2 "every acceptance example block has Covers, Given, When and Then, is cited and has a unique id ($(sed -n 's/^NOTE //p' "$TMP/r2.out") blocks); every subsection of sections 23 to 25 cites an example"
fi

# R3: warning only. Unfinished-text markers outside code fences: TODO, FIXME, TBD, XXX, the word
# placeholder, "to be defined" and the like, and runs of question marks.
awk '
  /^```/ { infence = !infence; next }
  infence { next }
  {
    low = tolower($0)
    if ($0 ~ /(^|[^A-Za-z])(TODO|FIXME|TBD|XXX)([^A-Za-z]|$)/ \
      || low ~ /placeholder/ \
      || low ~ /to be (defined|decided|determined|written|specified)/ \
      || $0 ~ /[?][?][?]/) {
      print "WARN R3 line " NR ": unfinished-text marker: " substr($0, 1, 70)
    }
  }
' "$REC" > "$TMP/r3.out" || { echo "internal error in R3" >&2; exit 2; }
if [ -s "$TMP/r3.out" ]; then cat "$TMP/r3.out"; else pass R3 "no unfinished-text marker outside code fences"; fi

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

# R7: warning only. (a) The old state file name outside Section 25.3 (its only permitted place is
# the migration rule there), reported separately for a tree line of Section 4.3. (b) A line of
# Section 8 that mentions reopen and is not in a unit that names full: the line itself, its paragraph,
# or a paragraph that is only a bold caption line directly before it.
awk '
  /^```/ { isfence = 1; infence = !infence } !/^```/ { isfence = 0 }
  {
    L[NR] = $0; F[NR] = infence || isfence
    if (!infence && !isfence && $0 ~ /^## [0-9]+\./) { s = $2; sub(/\.$/, "", s); top = s; sub2 = "" }
    else if (!infence && !isfence && $0 ~ /^### [0-9]+\.[0-9]+ /) sub2 = $2
    SEC[NR] = top; SUB[NR] = sub2
  }
  END {
    for (i = 1; i <= NR; i++) {
      if (index(L[i], "state.yaml") > 0 && SUB[i] != "25.3") {
        if (SUB[i] == "4.3" && F[i]) print "WARN R7 line " i ": state.yaml in a tree line of Section 4.3"
        else print "WARN R7 line " i ": state.yaml outside Section 25.3: " substr(L[i], 1, 60)
      }
    }
    for (i = 1; i <= NR; i++) {
      if (SEC[i] != "8" || F[i] || index(L[i], "reopen") == 0) continue
      ok = (index(L[i], "full") > 0)
      st = i; while (!ok && st > 1 && L[st - 1] != "") st--
      en = i; while (!ok && en < NR && L[en + 1] != "") en++
      for (j = st; !ok && j <= en; j++) if (index(L[j], "full") > 0) ok = 1
      if (!ok && st >= 3 && L[st - 1] == "") {
        q = st - 2; while (q > 1 && L[q - 1] != "") q--
        if (q == st - 2 && L[q] ~ /^[*][*]/ && index(L[q], "full") > 0) ok = 1
      }
      if (!ok) print "WARN R7 line " i ": reopen in Section 8 without naming full: " substr(L[i], 1, 60)
    }
  }
' "$REC" > "$TMP/r7.out" || { echo "internal error in R7" >&2; exit 2; }
if [ -s "$TMP/r7.out" ]; then cat "$TMP/r7.out"; else pass R7 "no old state file name outside Section 25.3; every reopen in Section 8 names the full profile"; fi

# C1 (only with --ids): the commits since the base that touch the specification. Each subject starts
# "docs(02-NN): SPEC-nn" and names only known ids (SPEC-01 to SPEC-18), except the one header
# subject, which names none and counts toward none. Each listed id is named by some subject.
# SPEC-13 is covered by S1 and S2 and needs no commit. Commits before the base never count.
if [ -n "$IDS" ]; then
  git log --format=%s "$BASE..HEAD" -- "$SPEC" > "$TMP/subjects.txt" 2> /dev/null \
    || { echo "cannot list the commits since $BASE" >&2; exit 2; }
  : > "$TMP/named.txt"
  c1=""
  prefix_re='^docs\(02-[0-9]{2}\): SPEC-[0-9]{2}'
  while IFS= read -r subj || [ -n "$subj" ]; do
    [ "$subj" = "$HEADER_SUBJECT" ] && continue
    if ! [[ "$subj" =~ $prefix_re ]]; then
      [ -n "$c1" ] || c1="a commit that touches the specification does not start with docs(02-NN): SPEC-nn: [$subj]"
      continue
    fi
    for tok in $(printf '%s\n' "$subj" | grep -o -E 'SPEC-[0-9]{2}'); do
      if [[ "$tok" =~ ^SPEC-(0[1-9]|1[0-8])$ ]]; then
        echo "$tok" >> "$TMP/named.txt"
      elif [ -z "$c1" ]; then
        c1="a commit subject names the unknown id $tok: [$subj]"
      fi
    done
  done < "$TMP/subjects.txt"
  IFS=',' read -r -a wanted <<< "$IDS"
  for id in "${wanted[@]}"; do
    [ "$id" = SPEC-13 ] && continue
    if ! grep -q -x -F "$id" "$TMP/named.txt"; then
      [ -n "$c1" ] || c1="no commit since $BASE that touches the specification names $id"
    fi
  done
  if [ -n "$c1" ]; then fail C1 "$c1"; else pass C1 "each listed id is named by a commit since $BASE, and every such commit names a known id"; fi
fi

if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL $FAILS"
exit 1
