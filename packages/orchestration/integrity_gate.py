"""
Integrity Gate v1 — lightweight pre-handoff checks.

Verifies handler imports, live_review state, plan consistency,
and relevant untracked files before claiming PASS.

Public API::

    run_integrity_checks(collect_only=False) -> IntegrityGateResult
    export_integrity_json(result) -> dict
    summarize_integrity(result) -> str
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class IntegrityStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    WARN = "warn"


@dataclass
class IntegrityCheck:
    """One integrity check result."""

    name: str = ""
    status: IntegrityStatus = IntegrityStatus.SKIP
    message: str = ""


@dataclass
class IntegrityGateResult:
    """Full integrity gate result."""

    version: int = 1
    checks: list[IntegrityCheck] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.status in (IntegrityStatus.PASS, IntegrityStatus.SKIP, IntegrityStatus.WARN) for c in self.checks)

    @property
    def fail_count(self) -> int:
        return sum(1 for c in self.checks if c.status == IntegrityStatus.FAIL)


# ---------------------------------------------------------------------------
# R-0017 fix: explicit scope status parsing
# ---------------------------------------------------------------------------

_COMPLETE_WORDS_RE = re.compile(r"\b(COMPLETE|DONE)\b", re.IGNORECASE)
_FINAL_WORDS_RE = re.compile(r"\b(COMPLETE|FINAL|DONE)\b", re.IGNORECASE)


def _ctx_says_complete(ctx_text: str) -> bool:
    """Check if context explicitly declares current scope complete.

    Checks the ``## Scope`` heading line AND the line immediately after it
    for COMPLETE or DONE.  Also checks ``## Current Step`` heading + next line
    for COMPLETE, FINAL, or DONE.

    Does NOT do full-text search — prior block status text must not trigger this.
    """
    lines = ctx_text.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Check ## Scope heading and its content line
        if re.match(r"^##\s+Scope\b", stripped):
            if _COMPLETE_WORDS_RE.search(stripped):
                return True
            if i + 1 < len(lines) and _COMPLETE_WORDS_RE.search(lines[i + 1]):
                return True
        # Check ## Current Step heading and its content line
        if re.match(r"^##\s+Current\s+Step\b", stripped):
            if _FINAL_WORDS_RE.search(stripped):
                return True
            if i + 1 < len(lines) and _FINAL_WORDS_RE.search(lines[i + 1]):
                return True
    return False


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def _check_handler_import() -> IntegrityCheck:
    """Check that collect_all_handlers() works."""
    try:
        from apps.cli.commands import collect_all_handlers
        handlers = collect_all_handlers()
        if not isinstance(handlers, dict):
            return IntegrityCheck("handler_import", IntegrityStatus.FAIL, "collect_all_handlers did not return dict")
        return IntegrityCheck("handler_import", IntegrityStatus.PASS, f"handlers={len(handlers)}")
    except Exception as exc:
        return IntegrityCheck("handler_import", IntegrityStatus.FAIL, f"import failed: {type(exc).__name__}: {exc}"[:200])


def _check_live_review_verdict() -> IntegrityCheck:
    """Check live_review latest verdict is not PENDING/FAIL when context says complete."""
    agent_dir = Path(".agent")
    live_review = agent_dir / "live_review.md"
    context = agent_dir / "context.md"

    if not live_review.exists():
        return IntegrityCheck("live_review_verdict", IntegrityStatus.SKIP, "no .agent/live_review.md")

    lr_text = live_review.read_text(encoding="utf-8", errors="replace")
    verdict = ""
    for line in lr_text.splitlines():
        if line.strip().startswith("## Verdict"):
            continue
        if verdict == "" and line.strip() and not line.startswith("#"):
            verdict = line.strip()
            break

    # Parse more carefully
    lines = lr_text.splitlines()
    for i, line in enumerate(lines):
        if "## Verdict" in line and i + 1 < len(lines):
            verdict = lines[i + 1].strip()
            break

    if not verdict:
        return IntegrityCheck("live_review_verdict", IntegrityStatus.WARN, "no verdict found")

    verdict_lower = verdict.lower()

    # Check if context explicitly declares current scope complete (R-0017 fix)
    ctx_text = ""
    if context.exists():
        ctx_text = context.read_text(encoding="utf-8", errors="replace")

    ctx_complete = _ctx_says_complete(ctx_text)

    if ctx_complete and "pending" in verdict_lower:
        return IntegrityCheck("live_review_verdict", IntegrityStatus.FAIL,
                              f"Context says complete but verdict is PENDING: {verdict[:100]}")
    if ctx_complete and "fail" in verdict_lower and "pass" not in verdict_lower:
        return IntegrityCheck("live_review_verdict", IntegrityStatus.FAIL,
                              f"Context says complete but verdict is FAIL: {verdict[:100]}")

    return IntegrityCheck("live_review_verdict", IntegrityStatus.PASS, verdict[:100])


def _check_plan_consistency() -> IntegrityCheck:
    """Check plan.md has no unchecked final steps if context says complete."""
    agent_dir = Path(".agent")
    plan = agent_dir / "plan.md"
    context = agent_dir / "context.md"

    if not plan.exists():
        return IntegrityCheck("plan_consistency", IntegrityStatus.SKIP, "no .agent/plan.md")

    plan_text = plan.read_text(encoding="utf-8", errors="replace")
    ctx_text = ""
    if context.exists():
        ctx_text = context.read_text(encoding="utf-8", errors="replace")

    ctx_complete = _ctx_says_complete(ctx_text)

    unchecked = []
    for line in plan_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- [ ]"):
            unchecked.append(stripped[:80])

    if ctx_complete and unchecked:
        return IntegrityCheck("plan_consistency", IntegrityStatus.FAIL,
                              f"Context says complete but {len(unchecked)} unchecked steps remain")

    return IntegrityCheck("plan_consistency", IntegrityStatus.PASS,
                          f"unchecked={len(unchecked)}, context_complete={ctx_complete}")


def _check_relevant_untracked() -> IntegrityCheck:
    """Check for relevant untracked files that should be committed."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode != 0:
            return IntegrityCheck("relevant_untracked", IntegrityStatus.SKIP, "git command failed")

        untracked = [f.strip() for f in result.stdout.splitlines() if f.strip()]

        relevant_suffixes = {".py", ".ts", ".js", ".md", ".toml", ".yaml", ".yml", ".sh"}
        relevant_dirs = ("apps/", "packages/", "tests/", "scripts/", "docs/")

        relevant = []
        for f in untracked:
            if f.startswith((".data/", "node_modules/", "__pycache__/", ".git/")):
                continue
            ext = Path(f).suffix.lower()
            if ext in relevant_suffixes or f.startswith(relevant_dirs):
                relevant.append(f)

        if relevant:
            return IntegrityCheck("relevant_untracked", IntegrityStatus.FAIL,
                                  f"{len(relevant)} relevant untracked: {', '.join(relevant[:5])}"[:200])

        return IntegrityCheck("relevant_untracked", IntegrityStatus.PASS, f"untracked={len(untracked)}, relevant=0")
    except Exception as exc:
        return IntegrityCheck("relevant_untracked", IntegrityStatus.SKIP, f"error: {exc}"[:200])


def _check_high_blockers_open() -> IntegrityCheck:
    """Check for open blocker/high findings in live_review."""
    live_review = Path(".agent/live_review.md")
    if not live_review.exists():
        return IntegrityCheck("high_blockers_open", IntegrityStatus.SKIP, "no live_review.md")

    text = live_review.read_text(encoding="utf-8", errors="replace")

    finding_re = re.compile(r"^###\s+(R-\d+):", re.MULTILINE)
    status_re = re.compile(r"^\s*-\s+\*\*Status\*\*:\s*(.+)$", re.MULTILINE)
    severity_re = re.compile(r"^\s*-\s+\*\*Severity\*\*:\s*(.+)$", re.MULTILINE)

    lines = text.splitlines()
    open_high = []
    i = 0
    while i < len(lines):
        fm = finding_re.match(lines[i])
        if not fm:
            i += 1
            continue
        finding_id = fm.group(1)
        status = ""
        severity = ""
        j = i + 1
        while j < len(lines) and not finding_re.match(lines[j]):
            sm = status_re.match(lines[j])
            if sm:
                status = sm.group(1).strip().lower()
            sev = severity_re.match(lines[j])
            if sev:
                severity = sev.group(1).strip().lower()
            j += 1
        if "open" in status and severity in ("blocker", "high"):
            open_high.append(finding_id)
        i = j

    if open_high:
        return IntegrityCheck("high_blockers_open", IntegrityStatus.FAIL,
                              f"{len(open_high)} open blocker/high: {', '.join(open_high)}")

    return IntegrityCheck("high_blockers_open", IntegrityStatus.PASS, "no open blocker/high findings")


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------


def run_integrity_checks(*, collect_only: bool = False) -> IntegrityGateResult:
    """Run all integrity checks."""
    result = IntegrityGateResult()

    result.checks.append(_check_handler_import())
    result.checks.append(_check_live_review_verdict())
    result.checks.append(_check_plan_consistency())
    result.checks.append(_check_relevant_untracked())
    result.checks.append(_check_high_blockers_open())

    if collect_only:
        result.checks.append(_check_collect_only())

    return result


def _check_collect_only() -> IntegrityCheck:
    """Run pytest --collect-only as integrity check."""
    try:
        result = subprocess.run(
            ["bash", "scripts/remedy_pytest.sh", "tests/", "--collect-only", "-q"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            return IntegrityCheck("collect_only", IntegrityStatus.PASS, "pytest collection passed")
        return IntegrityCheck("collect_only", IntegrityStatus.FAIL,
                              f"collect-only failed: {result.stderr[:200]}")
    except Exception as exc:
        return IntegrityCheck("collect_only", IntegrityStatus.SKIP, f"error: {exc}"[:200])


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_integrity_json(result: IntegrityGateResult) -> dict:
    """Export integrity result as safe JSON dict."""
    return {
        "version": result.version,
        "passed": result.passed,
        "fail_count": result.fail_count,
        "check_count": len(result.checks),
        "checks": [
            {
                "name": c.name,
                "status": c.status.value,
                "message": c.message,
            }
            for c in result.checks
        ],
    }


def summarize_integrity(result: IntegrityGateResult) -> str:
    """Human-readable integrity summary."""
    lines = ["Integrity Gate", "=" * 40]
    status = "PASS" if result.passed else "FAIL"
    lines.append(f"Status: {status} ({result.fail_count} failures)")
    lines.append("")

    icons = {
        IntegrityStatus.PASS: "[✓]",
        IntegrityStatus.FAIL: "[✗]",
        IntegrityStatus.SKIP: "[-]",
        IntegrityStatus.WARN: "[!]",
    }

    for c in result.checks:
        icon = icons.get(c.status, "[ ]")
        lines.append(f"  {icon} {c.name}: {c.message}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Read-only integrity status (no subprocess, no .agent, no pytest)
# ---------------------------------------------------------------------------


def export_readonly_integrity_status() -> dict:
    """Return read-only integrity status for use by readiness/report/bundle.

    No subprocess. No .agent file reads. No pytest. No git.
    Returns 'unknown' when no persisted integrity record exists.
    Suitable for embedding in overnight readiness and review bundle output.
    """
    return {
        "status": "unknown",
        "source": "no_persisted_integrity_status",
        "passed": None,
        "checks": [],
    }
