"""Known-failure baselines (Section 24.6).

The rule that finds failure identifiers is the `extract` member of a check gate: a pattern with one
capture group that is applied to every line of the chosen stream. The identifiers form a set.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Final

from ggsad.core.gate_model import NOT_EVALUABLE, NOT_SATISFIED, SATISFIED, Outcome

if TYPE_CHECKING:
    from collections.abc import Collection

    from ggsad.core.gate_model import ExtractRule, RunOutcome

STREAMS: Final = ("stdout", "stderr", "both")
MAX_LINE: Final = 10_000
NAMED_NEW: Final = 3


def compile_rule(pattern: str) -> re.Pattern[str] | None:
    """The compiled pattern, or None when it is not a regular expression with one capture group."""
    try:
        compiled = re.compile(pattern)
    except re.error:
        return None
    return compiled if compiled.groups == 1 else None


def extract_failures(rule: ExtractRule, run: RunOutcome) -> set[str] | None:
    """The failure identifiers in the output, or None when the output cannot be read."""
    compiled = compile_rule(rule.pattern)
    if compiled is None or rule.stream not in STREAMS:
        return None
    text = {
        "stdout": run.stdout,
        "stderr": run.stderr,
        "both": run.stdout + "\n" + run.stderr,
    }[rule.stream]
    found: set[str] = set()
    for line in text.splitlines():
        match = compiled.search(line[:MAX_LINE])
        if match and match.group(1):
            found.add(match.group(1))
    return found


def compare(baseline: Collection[str], rule: ExtractRule | None, run: RunOutcome) -> Outcome:
    """Compare the failures of a run that ended `not_satisfied` with the baseline."""
    failures = extract_failures(rule, run) if rule is not None else None
    if not failures:
        return Outcome(
            NOT_EVALUABLE,
            "no failure identifier can be extracted, so the failures cannot be compared",
        )
    new = sorted(failures - set(baseline))
    unused = len(set(baseline) - failures)
    if not new and run.truncated:
        return Outcome(
            NOT_EVALUABLE, "the output was cut, so failures after the cut cannot be compared"
        )
    if not new:
        return Outcome(
            SATISFIED, f"every failure is on the baseline; {unused} baseline entries did not fail"
        )
    named = ", ".join(new[:NAMED_NEW])
    return Outcome(
        NOT_SATISFIED, f"{len(new)} new failures: {named}; {unused} baseline entries did not fail"
    )
