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
#   --final             the phase gate: R1, R2, R3 and R7 become failures, C1 runs for SPEC-01 to
#                       SPEC-12 and SPEC-14 to SPEC-18, and R4, F1, W1, D1 and A1 run
#   --register FILE     the register that D1 reads (default: the register of this phase; relative
#                       paths are taken from the repository root); with --final
#   --version V         the method version R4 expects in the header (default 1.4); with --final
#   -h, --help          print this text
#
# Checks: B1 base blob, E1-E3 encoding, S1 S2 scope, N1 normative terms, X1 self-containment,
# R2 acceptance example structure and citations (warning only), R3 unfinished-text markers
# (warning only), R1 section references and heading numbers (warning only), R5 section map and
# structure, R6 base headings kept, R7 the old state file name and reopen per profile (warning only),
# R8 qualified "profile" (warning only). With --ids, C1: every listed id is named in the
# subject of a commit since the base that touches the specification (SPEC-13 is covered by S1 and
# S2 and needs no commit), and every such commit starts "docs(02-NN): SPEC-nn" and names only
# known ids; the two header subjects (the header commit of plan 05 and the header commit of plan
# 08) are accepted and count toward no id.
# With --final: R4 header version and revision line, F1 an acceptance example for each of the 41
# full rule units and a realization row for each of the 11 protections, W1 no status wording in the
# specification or in the notes of the phase, D1 every finding of the review (CR-01 to CR-03, WR-01
# to WR-27, IN-01 to IN-14) has exactly one row under the heading "Dispositions of the review
# findings" of the register, whose first two cells are the id and one of FIXED, FIXED-CONSERVATIVE,
# DEFERRED-TO-OWNER, RECORDED (no CR or WR row is RECORDED, and no other id has a row), and A1 the
# identity facts of the text (printed, not judged).
#
# Two checks fail in every mode: R9 the acceptance example ids (lines "**AE-nn — ") are exactly AE-1
# to AE-N with no gap and no repeat (N is printed), and J1 every json code fence parses (python3 with
# -I, else python, else node; with none of them a "WARN J1" line is printed and not counted).
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
FINAL=0
VERSION="1.4"
HEADER_SUBJECT="docs(02-05): header Version 1.4 and revision line (D-12)"
HEADER_SUBJECT2="docs(02-08): header revision line after the review fixes (D-12)"
REGISTER=".planning/phases/02-normative-drafting/02-DRAFTING-CHOICES.md"

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
    --final) FINAL=1; shift ;;
    --register) need_value "$@"; REGISTER="$2"; shift 2 ;;
    --version) need_value "$@"; VERSION="$2"; shift 2 ;;
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
[[ "$VERSION" =~ ^[0-9]+\.[0-9]+$ ]] || { echo "--version needs two integers joined by a dot, such as 1.4" >&2; exit 2; }
if [ "$FINAL" -eq 1 ]; then
  IDS="SPEC-01,SPEC-02,SPEC-03,SPEC-04,SPEC-05,SPEC-06,SPEC-07,SPEC-08,SPEC-09,SPEC-10,SPEC-11,SPEC-12,SPEC-14,SPEC-15,SPEC-16,SPEC-17,SPEC-18"
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
# warn_or_fail FILE: print the WARN lines of FILE. With --final each line is printed as FAIL and the
# check counts as one failure.
warn_or_fail() {
  if [ "$FINAL" -eq 1 ]; then
    sed 's/^WARN /FAIL /' "$1"
    FAILS=$((FAILS + 1))
  else
    cat "$1"
  fi
}

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
  warn_or_fail "$TMP/r2.warn"
else
  pass R2 "every acceptance example block has Covers, Given, When and Then, is cited and has a unique id ($(sed -n 's/^NOTE //p' "$TMP/r2.out") blocks); every subsection of sections 23 to 25 cites an example"
fi

# R9 (fails in every mode): the ids of the lines "**AE-nn — " outside code fences are exactly AE-1
# to AE-N, with no gap and no repeat.
awk '
  /^```/ { infence = !infence; next }
  infence { next }
  /^\*\*AE-[0-9]+ — / {
    id = $1; sub(/^\*\*AE-/, "", id); id += 0
    if (id in seen) { if (rep == "") rep = id; next }
    seen[id] = 1; n++; if (id > max) max = id
  }
  END {
    if (rep != "") print "FAIL R9 AE-" rep " is defined more than once"
    else {
      for (k = 1; k <= max; k++) if (!(k in seen)) { print "FAIL R9 AE-" k " is missing (the ids stop at AE-" max ", " n " blocks)"; exit }
      if (n == 0) print "FAIL R9 no acceptance example block found"
      else print "PASS R9 the ids AE-1 to AE-" max " are defined exactly once, no gap (N = " max ")"
    }
  }
' "$REC" > "$TMP/r9.out" || { echo "internal error in R9" >&2; exit 2; }
while IFS= read -r line; do
  echo "$line"
  case "$line" in FAIL*) FAILS=$((FAILS + 1)) ;; esac
done < "$TMP/r9.out"

# J1 (fails in every mode): each code fence with the info string json parses. The parser is python3
# (with -I), else python, else node; with none of them the check prints a warning and does not count.
awk -v dir="$TMP" '
  /^```/ {
    if (!infence) { infence = 1; isjson = ($0 ~ /^```json[ ]*$/); if (isjson) { nj++; out = dir "/j1-" nj ".json"; startline[nj] = NR; printf "" > out } }
    else { if (isjson) close(out); infence = 0; isjson = 0 }
    next
  }
  infence && isjson { print >> out }
  END { for (k = 1; k <= nj; k++) print k "\t" startline[k] > (dir "/j1.index"); if (nj == 0) printf "" > (dir "/j1.index") }
' "$REC" || { echo "internal error in J1" >&2; exit 2; }
j1py=""
for cand in python3 python; do
  if command -v "$cand" > /dev/null 2>&1 && "$cand" -I -c 'import json' > /dev/null 2>&1; then j1py="$cand"; break; fi
done
j1node=""
if [ -z "$j1py" ] && command -v node > /dev/null 2>&1; then j1node=node; fi
if [ -z "$j1py" ] && [ -z "$j1node" ]; then
  warn J1 "no JSON parser, blocks not parsed"
else
  j1bad=""
  j1n=0
  while IFS="$(printf '\t')" read -r k ln; do
    [ -n "$k" ] || continue
    j1n=$((j1n + 1))
    if [ -n "$j1py" ]; then
      "$j1py" -I -c 'import json,sys; json.load(open(sys.argv[1], encoding="utf-8"))' "$TMP/j1-$k.json" > /dev/null 2>&1 || { j1bad="the json block at line $ln does not parse"; break; }
    else
      node -e 'JSON.parse(require("fs").readFileSync(process.argv[1], "utf8"))' "$TMP/j1-$k.json" > /dev/null 2>&1 || { j1bad="the json block at line $ln does not parse"; break; }
    fi
  done < "$TMP/j1.index"
  if [ -n "$j1bad" ]; then fail J1 "$j1bad"; else pass J1 "$j1n json block(s) parse"; fi
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
if [ -s "$TMP/r3.out" ]; then warn_or_fail "$TMP/r3.out"; else pass R3 "no unfinished-text marker outside code fences"; fi

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

# R1: warning only. Every "Section N", "Sections N and M" and "Section N.M" reference (a list
# continues after a comma, "and", "or" or "to") resolves to a numbered heading outside code fences;
# heading numbers are unique; top-level numbers are contiguous from 1; subsection numbers are
# contiguous from 1 within each section.
awk '
  /^```/ { infence = !infence; next }
  infence { next }
  /^## [0-9]+\. / {
    n = $2; sub(/\.$/, "", n)
    if (n in have) print "WARN R1 line " NR ": heading number " n " occurs more than once"
    have[n] = 1; tops[n + 0] = 1; if (n + 0 > maxtop) maxtop = n + 0
    next
  }
  /^### [0-9]+\.[0-9]+ / {
    n = $2
    if (n in have) print "WARN R1 line " NR ": heading number " n " occurs more than once"
    have[n] = 1; split(n, w, "."); subs[w[1] + 0, w[2] + 0] = 1
    if (w[2] + 0 > maxsub[w[1] + 0]) maxsub[w[1] + 0] = w[2] + 0
    next
  }
  {
    t = $0
    while (match(t, /Sections? [0-9]+(\.[0-9]+)*/)) {
      ref = substr(t, RSTART, RLENGTH); sub(/^Sections? /, "", ref)
      nr++; rl[nr] = ref; rn[nr] = NR
      rest = substr(t, RSTART + RLENGTH)
      while (match(rest, /^(, and |, | and | or | to )[0-9]+(\.[0-9]+)*/)) {
        piece = substr(rest, RSTART, RLENGTH); sub(/^(, and |, | and | or | to )/, "", piece)
        nr++; rl[nr] = piece; rn[nr] = NR
        rest = substr(rest, RLENGTH + 1)
      }
      t = rest
    }
  }
  END {
    for (i = 1; i <= nr; i++) if (!(rl[i] in have)) print "WARN R1 line " rn[i] ": Section " rl[i] " does not resolve to a numbered heading"
    for (k = 1; k <= maxtop; k++) if (!(k in tops)) print "WARN R1 top-level numbers are not contiguous from 1: " k " is missing"
    for (k = 1; k <= maxtop; k++) for (m = 1; m <= maxsub[k]; m++) if (!((k, m) in subs)) print "WARN R1 subsection numbers are not contiguous: " k "." m " is missing"
  }
' "$REC" > "$TMP/r1.out" || { echo "internal error in R1" >&2; exit 2; }
if [ -s "$TMP/r1.out" ]; then warn_or_fail "$TMP/r1.out"; else pass R1 "every section reference resolves to a numbered heading; heading numbers are unique and contiguous"; fi

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
if [ -s "$TMP/r7.out" ]; then warn_or_fail "$TMP/r7.out"; else pass R7 "no old state file name outside Section 25.3; every reopen in Section 8 names the full profile"; fi

# C1 (only with --ids): the commits since the base that touch the specification. Each subject starts
# "docs(02-NN): SPEC-nn" and names only known ids (SPEC-01 to SPEC-18), except the two header
# subjects, which name none and count toward none. Each listed id is named by some subject.
# SPEC-13 is covered by S1 and S2 and needs no commit. Commits before the base never count.
if [ -n "$IDS" ]; then
  git log --format=%s "$BASE..HEAD" -- "$SPEC" > "$TMP/subjects.txt" 2> /dev/null \
    || { echo "cannot list the commits since $BASE" >&2; exit 2; }
  : > "$TMP/named.txt"
  c1=""
  prefix_re='^docs\(02-[0-9]{2}\): SPEC-[0-9]{2}'
  while IFS= read -r subj || [ -n "$subj" ]; do
    [ "$subj" = "$HEADER_SUBJECT" ] && continue
    [ "$subj" = "$HEADER_SUBJECT2" ] && continue
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

if [ "$FINAL" -eq 1 ]; then
  # R4: the header carries the method version and a revision line: an ISO date, an em dash and one
  # sentence that ends in a period. Only the first ten lines are read.
  head -n 10 "$REC" > "$TMP/header.txt"
  r4=""
  if [ "$(grep -c -x -F -e "**Version:** $VERSION" "$TMP/header.txt")" -ne 1 ]; then
    r4="the header has no single line **Version:** $VERSION"
  elif [ "$(grep -c -E -e '^\*\*Revision:\*\* [0-9]{4}-[0-9]{2}-[0-9]{2} — .+\.$' "$TMP/header.txt")" -ne 1 ]; then
    r4="the header has no single Revision line of the form: ISO date, em dash, one sentence ending in a period"
  fi
  if [ -n "$r4" ]; then fail R4 "$r4"; else pass R4 "header has **Version:** $VERSION and a Revision line with an ISO date, an em dash and a closing period"; fi

  # F1: an acceptance example for each of the 41 full rule units (the Covers lines below, each
  # outside code fences) and a realization row for each of the 11 protections. The unit of Section
  # 8.4 already has the example of reopen, so it needs two. Section 8.3 has one example per action.
  : > "$TMP/f1.units"
  for u in "Section 4.1" "Section 5.5" "Section 6.1" "Section 6.2" "Section 6.3" \
    "Section 7.1 (Patch Flow)" "Section 7.1 (Standard Flow)" "Section 7.1 (Release Flow)" \
    "Section 7.1 (Exploration Flow)" "Section 8.2" "Section 8.4" "Section 8.5" \
    "Section 11.2" "Section 12.2"; do
    printf '%s\n' "$u" >> "$TMP/f1.units"
  done
  for a in start complete wait resume fail cancel supersede reopen; do
    printf 'Section 8.3 (`%s`)\n' "$a" >> "$TMP/f1.units"
  done
  for k in 1 2 3 4 5 6 7 8; do
    printf 'Sections 9.%s and 10.%s\n' "$k" "$k" >> "$TMP/f1.units"
  done
  for k in 1 2 3 4 5 6 7 8 9 10; do
    printf 'Section 24.%s (full)\n' "$k" >> "$TMP/f1.units"
  done
  printf 'Section 22.2 (full)\n' >> "$TMP/f1.units"
  awk '
    /^```/ { infence = !infence; next }
    infence { next }
    /^- Covers: / { t = $0; sub(/^- Covers: /, "", t); seen[t]++ }
    END { for (t in seen) print seen[t] "\t" t }
  ' "$REC" > "$TMP/f1.seen"
  f1=""
  nunits=0
  while IFS= read -r u || [ -n "$u" ]; do
    nunits=$((nunits + 1))
    need=1
    [ "$u" = "Section 8.4" ] && need=2
    have=$(awk -F '\t' -v u="$u" '$2 == u { print $1 }' "$TMP/f1.seen")
    if [ "${have:-0}" -lt "$need" ]; then
      [ -n "$f1" ] || f1="no acceptance example with the line [- Covers: $u] (needs $need)"
    fi
  done < "$TMP/f1.units"
  awk -v cap='**Realization of the Protections in the Two Method Profiles**' '
    /^```/ { infence = !infence; next }
    infence { next }
    $0 == cap { capn++; st = 1; next }
    st == 1 { if ($0 == "") next; st = ($0 ~ /^\|/) ? 2 : 0 }
    st == 2 {
      if ($0 ~ /^\|/) {
        rows++
        if (rows > 2) {
          n = split($0, c, "|"); s = c[3]; gsub(/^ +| +$/, "", s); sec[s]++; data++
        }
      } else st = 0
    }
    END {
      bad = ""
      if (capn != 1) bad = "the caption occurs " capn + 0 " times, expected once"
      for (k = 1; bad == "" && k <= 10; k++) if (sec["24." k] != 1) bad = "no single realization row for Section 24." k
      if (bad == "" && sec["22.2"] != 1) bad = "no single realization row for the result blocked (Section 22.2)"
      if (bad == "" && data != 11) bad = "the realization table has " data + 0 " data rows, expected 11"
      if (bad != "") print "FAIL " bad; else print "PASS"
    }
  ' "$REC" > "$TMP/f1.table"
  if [ -z "$f1" ] && [ "$(cut -c1-4 "$TMP/f1.table")" != PASS ]; then f1="$(sed 's/^FAIL //' "$TMP/f1.table")"; fi
  if [ -n "$f1" ]; then fail F1 "$f1"; else pass F1 "all $nunits full rule units have an acceptance example (41 units expected) and all 11 protections a realization row"; fi

  # W1: no status wording in the specification or in the notes of this phase, and no owner reply
  # row in the identity note.
  w1=""
  : > "$TMP/w1.files"
  for f in .planning/phases/02-normative-drafting/02-DRAFTING-CHOICES.md .planning/reviews/*-normative-spec-diff-identity.md; do
    [ -f "$f" ] && printf '%s\n' "$f" >> "$TMP/w1.files"
  done
  if grep -q -i -F -e 'owner-confirmed' -e 'Decided (' "$REC"; then w1="the specification holds status wording"; fi
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if grep -q -i -F -e 'owner-confirmed' -e 'Decided (' "$f"; then
      [ -n "$w1" ] || w1="status wording in $f"
    fi
    case "$f" in
      *-normative-spec-diff-identity.md)
        if grep -q -i -E -e '^\| *Owner reply' "$f"; then [ -n "$w1" ] || w1="an Owner reply row in $f"; fi ;;
    esac
  done < "$TMP/w1.files"
  if [ -n "$w1" ]; then fail W1 "$w1"; else pass W1 "no status wording in the specification or in the $(wc -l < "$TMP/w1.files" | tr -d ' ') note(s) of the phase; no owner reply row"; fi

  # D1: every finding of the review has exactly one disposition row in the register, under the
  # heading "Dispositions of the review findings". A row is read by its first two cells.
  d1=""
  if [ ! -f "$REGISTER" ] || [ ! -r "$REGISTER" ]; then
    d1="cannot read the register $REGISTER"
  else
    d1=$(awk '
      function trim(s) { gsub(/^ +| +$/, "", s); return s }
      BEGIN {
        n = split("CR-01 CR-02 CR-03", a, " "); for (i = 1; i <= n; i++) { want[a[i]] = 1; ord[++no] = a[i] }
        for (k = 1; k <= 27; k++) { id = sprintf("WR-%02d", k); want[id] = 1; ord[++no] = id }
        for (k = 1; k <= 14; k++) { id = sprintf("IN-%02d", k); want[id] = 1; ord[++no] = id }
        okv["FIXED"] = 1; okv["FIXED-CONSERVATIVE"] = 1; okv["DEFERRED-TO-OWNER"] = 1; okv["RECORDED"] = 1
      }
      /^```/ { infence = !infence; next }
      infence { next }
      /^## / { insec = ($0 == "## Dispositions of the review findings"); if (insec) found++; next }
      insec && /^\|/ {
        m = split($0, c, "|")
        id = trim(c[2]); val = trim(c[3])
        if (id !~ /^[A-Za-z]+-[0-9]+$/) next
        rows[id]++
        if (rows[id] == 1) value[id] = val
        if (!(id in want) && other == "") other = id
      }
      END {
        if (found != 1) { print "the heading Dispositions of the review findings occurs " found + 0 " times, expected once"; exit }
        if (other != "") { print "the row for " other " is not a finding of the review"; exit }
        for (i = 1; i <= no; i++) {
          id = ord[i]
          if (rows[id] == 0) { print "no disposition row for " id; exit }
          if (rows[id] > 1) { print "more than one disposition row for " id; exit }
          if (!(value[id] in okv)) { print "the disposition of " id " is [" value[id] "], not FIXED, FIXED-CONSERVATIVE, DEFERRED-TO-OWNER or RECORDED"; exit }
          if (value[id] == "RECORDED" && id !~ /^IN-/) { print id " is RECORDED; only an IN finding may be"; exit }
        }
      }
    ' "$REGISTER")
  fi
  if [ -n "$d1" ]; then fail D1 "$d1"; else pass D1 "all 44 findings have exactly one disposition row; no CR or WR finding is RECORDED"; fi

  # A1: facts only, printed for the diff identity record of the phase. No verdict.
  echo "A1 base blob: ${base_now:-absent}"
  if [ -n "$REF" ]; then
    echo "A1 result blob: $(git rev-parse --verify --quiet "$REF:$FILE" 2> /dev/null || echo absent)"
  else
    echo "A1 result blob (working file): $(git hash-object "$REC")"
    echo "A1 result blob (HEAD): $(git rev-parse --verify --quiet "HEAD:$FILE" 2> /dev/null || echo absent)"
  fi
  echo "A1 SHA-256: $(sha256sum < "$REC" | cut -d ' ' -f1)"
  echo "A1 line count: $(wc -l < "$REC" | tr -d ' ')"
  echo "A1 diffstat: $(git diff --no-index --shortstat -- "$TMP/base" "$REC" | sed 's/^ *//')"
  echo "A1 commits touching the specification since $BASE: $(git log --format=%h "$BASE..HEAD" -- "$SPEC" 2> /dev/null | wc -l | tr -d ' ')"
  git log --format='A1 commit %h %s' "$BASE..HEAD" -- "$SPEC" 2> /dev/null
fi

if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL $FAILS"
exit 1
