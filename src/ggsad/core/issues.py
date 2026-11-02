"""Issues and reports of the `core` profile (Section 22.2: stable codes plus messages)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Issue:
    """One finding: a stable code, a human-readable message, and the location it concerns."""

    code: str
    message: str
    path: str = ""


@dataclass(frozen=True)
class Report:
    """The result of a validation: errors reject the operation, warnings never do."""

    issues: tuple[Issue, ...] = ()
    warnings: tuple[Issue, ...] = ()

    @property
    def ok(self) -> bool:
        """True when nothing rejects the operation."""
        return not self.issues

    @property
    def codes(self) -> tuple[str, ...]:
        """The codes of the errors, in order, which makes assertions short."""
        return tuple(issue.code for issue in self.issues)


@dataclass
class ReportBuilder:
    """Collects issues and warnings while a validation runs."""

    _issues: list[Issue] = field(default_factory=list)
    _warnings: list[Issue] = field(default_factory=list)

    def error(self, code: str, message: str, path: str = "") -> None:
        """Record an error."""
        self._issues.append(Issue(code, message, path))

    def warn(self, code: str, message: str, path: str = "") -> None:
        """Record a warning."""
        self._warnings.append(Issue(code, message, path))

    def build(self) -> Report:
        """Freeze the collected findings."""
        return Report(tuple(self._issues), tuple(self._warnings))
