#!/usr/bin/env bash
# Read-only check of the Executable Core decision record.
#
# Usage: 01-check-decision-record.sh [options]
#   --file PATH       record to check (default: the record path below; relative paths are taken
#                     from the repository root)
#   --ref GITREF      read the committed blob GITREF:PATH instead of the working tree
#   --entries LIST    comma-separated entry ids expected in file order (default 1,2,...,11)
#   --stage STAGE     proposed (default) or confirmed
#   --date YYYY-MM-DD confirmation date, required for --stage confirmed
#   --print-chosen N  print the Chosen text of entry N as one line and exit 0 (exit 2 if the
#                     entry or its Chosen field is missing)
#
# Output: one line per check, "PASS ID message" or "FAIL ID message", then "RESULT: PASS" or
# "RESULT: FAIL N". Exit 0 on pass, 1 on any failed check, 2 on a usage error or an unreadable file.
# Nothing is written outside a temporary directory that is removed on exit.

set -u
export LC_ALL=C
cd "$(git rev-parse --show-toplevel)" || { echo "not inside a git repository" >&2; exit 2; }

REC_PATH="docs/decisions/2026-10-23-executable-core-decisions.md"
DECISION_DATE="2026-10-23"
DEPARTURE="The proposal recommended keeping YAML; the owner chose JSON instead."

FILE="$REC_PATH"
REF=""
ENTRIES="1,2,3,4,5,6,7,8,9,10,11"
STAGE="proposed"
DATE=""
PRINT_CHOSEN=""

usage() {
  sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//' >&2
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
    --entries) need_value "$@"; ENTRIES="$2"; shift 2 ;;
    --stage) need_value "$@"; STAGE="$2"; shift 2 ;;
    --date) need_value "$@"; DATE="$2"; shift 2 ;;
    --print-chosen) need_value "$@"; PRINT_CHOSEN="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
done

[[ "$ENTRIES" =~ ^[0-9]+(,[0-9]+)*$ ]] || { echo "--entries must be a comma-separated list of numbers" >&2; exit 2; }
[ "$STAGE" = proposed ] || [ "$STAGE" = confirmed ] || { echo "--stage must be proposed or confirmed" >&2; exit 2; }
if [ -n "$PRINT_CHOSEN" ]; then
  [[ "$PRINT_CHOSEN" =~ ^[0-9]+$ ]] || { echo "--print-chosen needs an entry number" >&2; exit 2; }
fi

DATEBAD=""
if [ "$STAGE" = confirmed ]; then
  [ -n "$DATE" ] || { echo "--stage confirmed needs --date YYYY-MM-DD" >&2; exit 2; }
  if ! [[ "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || [ "$(date -u -d "$DATE" +%F 2>/dev/null)" != "$DATE" ]; then
    DATEBAD="--date $DATE is not a valid ISO date"
  elif [[ "$DATE" < "$DECISION_DATE" ]]; then
    DATEBAD="--date $DATE is earlier than the decision date $DECISION_DATE"
  fi
fi

TMP=$(mktemp -d) || { echo "cannot create a temporary directory" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT
REC="$TMP/record"

if [ -n "$REF" ]; then
  git cat-file blob "$REF:$FILE" > "$REC" 2>/dev/null || { echo "cannot read $REF:$FILE" >&2; exit 2; }
else
  [ -f "$FILE" ] && [ -r "$FILE" ] || { echo "cannot read $FILE" >&2; exit 2; }
  cp "$FILE" "$REC" || { echo "cannot read $FILE" >&2; exit 2; }
fi

if [ -n "$PRINT_CHOSEN" ]; then
  awk -v want="$PRINT_CHOSEN" '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^### O-[0-9]+: / {
      s = $0; sub(/^### O-/, "", s); sub(/:.*/, "", s)
      cur = (!done && s + 0 == want + 0); inch = 0
      next
    }
    /^###/ { cur = 0; inch = 0; next }
    cur && /^- Chosen:( |$)/ {
      found = 1; inch = 1
      s = $0; sub(/^- Chosen:/, "", s); text = trim(s)
      next
    }
    cur && inch && /^  / {
      t = trim($0); if (t != "") text = (text == "" ? t : text " " t)
      next
    }
    cur && inch { inch = 0; done = 1 }
    END { if (!found) exit 2; print text }
  ' "$REC"
  exit $?
fi

FAILS=0
pass() { echo "PASS $1 $2"; }
fail() { echo "FAIL $1 $2"; FAILS=$((FAILS + 1)); }

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

# H1, F1, F2, D1, S1: structure of the entries.
AWK_ENTRIES='
function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
function fail(id, msg) { if (!(id in fmsg)) fmsg[id] = msg }
function lbl(n, name,   k) {
  for (k = 1; k <= nlab[n]; k++) if (lab[n, k] == name) return k
  return 0
}
BEGIN { explen = split(entries, expid, ",") }
/^## / {
  if ($0 == "## Decisions") { decfound++; indec = 1 }
  else if (indec) fail("H1", "line " NR ": a section follows ## Decisions, which must be the last section")
  cur = 0
  next
}
{
  if ($0 ~ /^- Owner confirmation:/) { ocnt++; ovalue = $0 }
  if (substr($0, 1, 3) == "###") {
    if (!indec) fail("H1", "line " NR ": heading starting with ### before the ## Decisions heading")
    if ($0 !~ /^### O-[0-9]+: ./) {
      fail("H1", "line " NR ": malformed entry heading, expected ### O-n: title")
      cur = 0
    } else {
      nent++
      s = $0; sub(/^### O-/, "", s); sub(/:.*/, "", s)
      eid[nent] = s; nlab[nent] = 0; cur = nent
    }
    next
  }
  if (!cur) next
  if ($0 ~ /^[ \t]*$/) next
  if ($0 ~ /^- /) {
    s = substr($0, 3); p = index(s, ":")
    name = (p > 0) ? substr(s, 1, p - 1) : ""
    rest = (p > 0) ? substr(s, p + 1) : ""
    if (name !~ /^[A-Za-z][A-Za-z ]*$/ || (rest != "" && substr(rest, 1, 1) != " ")) {
      fail("F1", "O-" eid[cur] ": line " NR ": malformed field bullet, expected - Label: text")
      next
    }
    k = ++nlab[cur]; lab[cur, k] = name; txt[cur, k] = trim(rest)
    next
  }
  if ($0 ~ /^  /) {
    if (nlab[cur] == 0) { fail("F1", "O-" eid[cur] ": line " NR ": text before the first field bullet"); next }
    t = trim($0); k = nlab[cur]
    if (t != "") txt[cur, k] = (txt[cur, k] == "" ? t : txt[cur, k] " " t)
    next
  }
  fail("F1", "O-" eid[cur] ": line " NR ": text at column 0 outside a field bullet")
}
END {
  # H1: heading ids, in the expected numeric order, none missing, none repeated.
  if (decfound == 0) fail("H1", "missing the ## Decisions heading")
  else if (decfound > 1) fail("H1", "the ## Decisions heading occurs more than once")
  m = (nent > explen) ? nent : explen
  for (i = 1; i <= m; i++) {
    if (i > nent) { fail("H1", "entry O-" expid[i] " is missing at position " i); break }
    if (i > explen) { fail("H1", "unexpected entry O-" eid[i] " at position " i); break }
    if (eid[i] != expid[i]) { fail("H1", "position " i ": found O-" eid[i] ", expected O-" expid[i]); break }
  }
  # F1: field labels, each once, in order.
  for (n = 1; n <= nent; n++) {
    id = eid[n]
    base = "Status|Decision date|Context|Options considered|Chosen|Rationale|Consequences"
    if (id + 0 == 4) base = "Status|Decision date|Context|Options considered|Chosen|Departs from the proposal|Rationale|Consequences"
    ne = split(base, ex, "|")
    delete a; na = 0
    for (k = 1; k <= nlab[n]; k++) {
      if (k == 3 && lab[n, k] == "Supersedes") continue
      a[++na] = lab[n, k]
    }
    mm = (na > ne) ? na : ne
    for (j = 1; j <= mm; j++) {
      if (j > na) { fail("F1", "O-" id ": missing field " ex[j]); break }
      if (j > ne) { fail("F1", "O-" id ": unexpected field " a[j]); break }
      if (a[j] != ex[j]) { fail("F1", "O-" id ": found field " a[j] " where " ex[j] " is expected (each field once, in order)"); break }
    }
  }
  # F2: no empty field.
  for (n = 1; n <= nent; n++)
    for (k = 1; k <= nlab[n]; k++)
      if (txt[n, k] == "")
        fail("F2", "O-" eid[n] " " lab[n, k] ": empty" (lab[n, k] == "Rationale" ? " (write rationale not recorded)" : ""))
  # D1: the O-4 departure sentence.
  d1note = "O-4 is not among the expected entries"
  for (n = 1; n <= nent; n++) {
    if (eid[n] + 0 != 4) continue
    d1note = "O-4 opens its departure field with the required sentence"
    k = lbl(n, "Departs from the proposal")
    if (!k) { fail("D1", "O-4: the Departs from the proposal field is missing"); break }
    t = txt[n, k]
    if (index(t, dep) != 1) fail("D1", "O-4 Departs from the proposal: must start with: " dep)
    else if (length(t) <= length(dep)) fail("D1", "O-4 Departs from the proposal: no YAML case follows the departure sentence")
  }
  # S1: status vocabulary by stage and the confirmation line.
  for (n = 1; n <= nent; n++) {
    k = lbl(n, "Status"); st = k ? txt[n, k] : ""
    if (st ~ /^Superseded by O-[0-9]+$/) continue
    if (stage == "proposed") {
      if (st != "Proposed wording") fail("S1", "O-" eid[n] " Status: found [" st "], stage proposed allows Proposed wording or Superseded by O-n")
    } else if (datebad != "") fail("S1", datebad)
    else if (st != "Decided (owner-confirmed " date ")") fail("S1", "O-" eid[n] " Status: found [" st "], expected Decided (owner-confirmed " date ")")
  }
  want = (stage == "proposed") ? "- Owner confirmation: pending" : "- Owner confirmation: " date
  if (ocnt != 1) fail("S1", "the - Owner confirmation: line occurs " ocnt + 0 " times, expected once")
  else if (ovalue != want) fail("S1", "header line is [" ovalue "], expected [" want "]")

  okm["H1"] = "entry headings are exactly " entries " in order"
  okm["F1"] = "every entry carries its fields once, in order"
  okm["F2"] = "no field is empty"
  okm["D1"] = d1note
  okm["S1"] = (stage == "proposed") ? "every Status is Proposed wording or superseded; header says pending" : "every Status is Decided (owner-confirmed " date "); header carries the date"
  split("H1 F1 F2 D1 S1", order, " ")
  for (i = 1; i <= 5; i++) {
    c = order[i]
    if (c in fmsg) print "FAIL " c " " fmsg[c]
    else print "PASS " c " " okm[c]
  }
}
'
awk -v entries="$ENTRIES" -v stage="$STAGE" -v date="$DATE" -v datebad="$DATEBAD" -v dep="$DEPARTURE" \
  "$AWK_ENTRIES" "$REC" > "$TMP/entries.out" || { echo "internal error while parsing the record" >&2; exit 2; }
while IFS= read -r line; do
  echo "$line"
  case "$line" in FAIL*) FAILS=$((FAILS + 1)) ;; esac
done < "$TMP/entries.out"

if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS"
  exit 0
fi
echo "RESULT: FAIL $FAILS"
exit 1
