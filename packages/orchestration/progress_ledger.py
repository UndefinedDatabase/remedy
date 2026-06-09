"""
Progress Ledger v1 — structured checklist from plan, live review, and known risks.

Builds a unified view of what was done, what is open, what evidence proves it,
and what the latest review verdict is.

Public API::

    build_progress_ledger(plan_text=None, live_review_text=None, context_text=None,
                          job=None, events=None) -> ProgressLedger
    export_progress_ledger_json(ledger) -> dict
    summarize_progress_ledger(ledger) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ProgressStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    RESOLVED = "resolved"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    RISK = "risk"
    SKIPPED = "skipped"


class ProgressSource(str, Enum):
    PLAN_STEP = "plan_step"
    LIVE_REVIEW_FINDING = "live_review_finding"
    TEST_RESULT = "test_result"
    REPAIR_ARTIFACT = "repair_artifact"
    PROOF_GAP = "proof_gap"
    KNOWN_RISK = "known_risk"
    FEATURE_SUGGESTION = "feature_suggestion"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class ProgressEvidence:
    """One piece of evidence for a progress item."""

    ref: str = ""
    description: str = ""
    source_type: str = ""


@dataclass
class ProgressItem:
    """One item in the progress ledger."""

    item_id: str = ""
    title: str = ""
    status: ProgressStatus = ProgressStatus.PLANNED
    source_type: ProgressSource = ProgressSource.PLAN_STEP
    source_ref: str = ""
    severity: str = ""
    area: str = ""
    evidence_refs: list[ProgressEvidence] = field(default_factory=list)
    completed_at: str = ""
    owner_role: str = ""
    next_action: str = ""
    safe_summary: str = ""


@dataclass
class ProgressLedger:
    """Full progress ledger."""

    version: int = 1
    scope: str = ""
    verdict: str = ""
    items: list[ProgressItem] = field(default_factory=list)
    inconsistencies: list[str] = field(default_factory=list)

    @property
    def done_count(self) -> int:
        return sum(1 for i in self.items if i.status in (ProgressStatus.DONE, ProgressStatus.RESOLVED))

    @property
    def open_count(self) -> int:
        return sum(1 for i in self.items if i.status in (ProgressStatus.PLANNED, ProgressStatus.IN_PROGRESS))

    @property
    def blocked_count(self) -> int:
        return sum(1 for i in self.items if i.status == ProgressStatus.BLOCKED)

    @property
    def risk_count(self) -> int:
        return sum(1 for i in self.items if i.status == ProgressStatus.RISK)

    @property
    def skipped_count(self) -> int:
        return sum(1 for i in self.items if i.status == ProgressStatus.SKIPPED)


# ---------------------------------------------------------------------------
# Step 1012: Build ledger from plan.md
# ---------------------------------------------------------------------------

import re

_PLAN_ITEM_RE = re.compile(
    r"^-\s+\[(?P<check>[xX ])\]\s+(?:(?P<step>\d+):?\s*)?(?P<title>.+)$"
)

_SKIP_WORDS = frozenset({"skipped", "not run", "optional", "not implemented", "future work", "deferred"})


def build_progress_ledger_from_plan(plan_text: str) -> ProgressLedger:
    """Parse plan.md checklist into a ProgressLedger."""
    ledger = ProgressLedger()

    scope_match = re.search(r"^#\s+Plan\s*[—–-]\s*(.+)$", plan_text, re.MULTILINE)
    if scope_match:
        ledger.scope = scope_match.group(1).strip()

    for line in plan_text.splitlines():
        m = _PLAN_ITEM_RE.match(line.strip())
        if not m:
            continue

        checked = m.group("check").lower() == "x"
        step = m.group("step") or ""
        title = m.group("title").strip()

        title_lower = title.lower()
        is_skipped = any(w in title_lower for w in _SKIP_WORDS)

        if is_skipped:
            status = ProgressStatus.SKIPPED
        elif checked:
            status = ProgressStatus.DONE
        else:
            status = ProgressStatus.PLANNED

        item_id = f"plan-{step}" if step else f"plan-{len(ledger.items)}"

        item = ProgressItem(
            item_id=item_id,
            title=title,
            status=status,
            source_type=ProgressSource.PLAN_STEP,
            source_ref=f"step-{step}" if step else "",
            safe_summary=title[:200],
        )
        ledger.items.append(item)

    return ledger


# ---------------------------------------------------------------------------
# Step 1013: Merge live review findings
# ---------------------------------------------------------------------------

_FINDING_RE = re.compile(
    r"^###\s+(R-\d+):\s*(.+)$"
)

_STATUS_RE = re.compile(
    r"^\s*-\s+\*\*Status\*\*:\s*(.+)$"
)

_SEVERITY_RE = re.compile(
    r"^\s*-\s+\*\*Severity\*\*:\s*(.+)$"
)

_AREA_RE = re.compile(
    r"^\s*-\s+\*\*Area\*\*:\s*(.+)$"
)

_DONE_MARKER_RE = re.compile(
    r"Done:\s+(R-\d+)\s*[-–—]\s*(.+)"
)

_VERDICT_RE = re.compile(
    r"^##\s+Verdict\s*$", re.MULTILINE
)


def _parse_verdict(live_review_text: str) -> str:
    """Extract verdict line from live review."""
    lines = live_review_text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^##\s+Verdict", line):
            if i + 1 < len(lines):
                return lines[i + 1].strip()
    return ""


def merge_live_review_findings(ledger: ProgressLedger, live_review_text: str) -> None:
    """Merge live review findings into an existing ledger."""
    verdict = _parse_verdict(live_review_text)
    if verdict:
        ledger.verdict = verdict

    lines = live_review_text.splitlines()
    i = 0
    while i < len(lines):
        fm = _FINDING_RE.match(lines[i].strip())
        if not fm:
            i += 1
            continue

        finding_id = fm.group(1)
        finding_title = fm.group(2).strip()
        status_str = ""
        severity = ""
        area = ""
        done_summary = ""

        j = i + 1
        while j < len(lines) and not _FINDING_RE.match(lines[j].strip()):
            sm = _STATUS_RE.match(lines[j])
            if sm:
                status_str = sm.group(1).strip()
            sev = _SEVERITY_RE.match(lines[j])
            if sev:
                severity = sev.group(1).strip()
            ar = _AREA_RE.match(lines[j])
            if ar:
                area = ar.group(1).strip()
            dm = _DONE_MARKER_RE.search(lines[j])
            if dm and dm.group(1) == finding_id:
                done_summary = dm.group(2).strip()
            j += 1

        status_lower = status_str.lower()
        if "resolved" in status_lower:
            status = ProgressStatus.RESOLVED
        elif "open" in status_lower:
            sev_lower = severity.lower()
            if sev_lower in ("blocker", "high"):
                status = ProgressStatus.BLOCKED
            else:
                status = ProgressStatus.PLANNED
        elif "won't fix" in status_lower:
            status = ProgressStatus.SKIPPED
        else:
            status = ProgressStatus.PLANNED

        evidence = []
        if done_summary:
            evidence.append(ProgressEvidence(
                ref=finding_id,
                description=done_summary[:200],
                source_type="done_marker",
            ))

        item = ProgressItem(
            item_id=finding_id,
            title=finding_title[:200],
            status=status,
            source_type=ProgressSource.LIVE_REVIEW_FINDING,
            source_ref=finding_id,
            severity=severity,
            area=area,
            evidence_refs=evidence,
            safe_summary=finding_title[:200],
        )
        ledger.items.append(item)
        i = j

    # Consistency check: PASS verdict with open blocker/high
    if verdict:
        verdict_lower = verdict.lower()
        has_open_blocker = any(
            i.status == ProgressStatus.BLOCKED
            and i.source_type == ProgressSource.LIVE_REVIEW_FINDING
            for i in ledger.items
        )
        if "pass" in verdict_lower and "fail" not in verdict_lower and has_open_blocker:
            ledger.inconsistencies.append(
                "Verdict says PASS but open blocker/high findings exist"
            )


# ---------------------------------------------------------------------------
# Step 1014: Build ledger from known risks
# ---------------------------------------------------------------------------

_RISK_PATTERNS = [
    (re.compile(r"Pre-existing\s+Issue", re.IGNORECASE), "pre-existing"),
    (re.compile(r"Known\s+Risk", re.IGNORECASE), "known-risk"),
]


def merge_known_risks(ledger: ProgressLedger, context_text: str) -> None:
    """Merge known risks from context.md into ledger."""
    lines = context_text.splitlines()
    in_risk_section = False
    risk_idx = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("##"):
            in_risk_section = any(p.search(stripped) for p, _ in _RISK_PATTERNS)
            continue

        if in_risk_section and stripped.startswith("-"):
            risk_text = stripped.lstrip("- ").strip()
            if not risk_text:
                continue
            risk_idx += 1
            item = ProgressItem(
                item_id=f"risk-{risk_idx}",
                title=risk_text[:200],
                status=ProgressStatus.RISK,
                source_type=ProgressSource.KNOWN_RISK,
                source_ref="context.md",
                safe_summary=risk_text[:200],
            )
            ledger.items.append(item)

    # Also look for inline pre-existing issue markers
    for line in lines:
        stripped = line.strip()
        if "pre-existing" in stripped.lower() and "fails" in stripped.lower():
            already = any(
                i.source_type == ProgressSource.KNOWN_RISK and "pre-existing" in i.title.lower()
                for i in ledger.items
            )
            if not already:
                risk_text = stripped.lstrip("- ").strip()
                risk_idx += 1
                item = ProgressItem(
                    item_id=f"risk-{risk_idx}",
                    title=risk_text[:200],
                    status=ProgressStatus.RISK,
                    source_type=ProgressSource.KNOWN_RISK,
                    source_ref="context.md",
                    safe_summary=risk_text[:200],
                )
                ledger.items.append(item)


def merge_job_risks(ledger: ProgressLedger, job: Any, events: list[dict] | None = None) -> None:
    """Merge risks from job artifacts and events into ledger."""
    if job is None:
        return

    risk_idx = sum(1 for i in ledger.items if i.source_type == ProgressSource.KNOWN_RISK)

    for art in getattr(job, "artifacts", []):
        meta = getattr(art, "metadata", {}) or {}
        if meta.get("test_failure"):
            risk_idx += 1
            kind = meta.get("failure_kind", "test_failure")
            item = ProgressItem(
                item_id=f"risk-job-{risk_idx}",
                title=f"Test failure: {kind}"[:200],
                status=ProgressStatus.RISK,
                source_type=ProgressSource.REPAIR_ARTIFACT,
                source_ref=str(getattr(art, "id", ""))[:8],
                severity="High",
                safe_summary=f"Test failure artifact ({kind})"[:200],
            )
            ledger.items.append(item)

    if events:
        for ev in events:
            if ev.get("event") == "proof_gap_detected":
                risk_idx += 1
                gap = ev.get("gap_type", "unknown")
                item = ProgressItem(
                    item_id=f"risk-gap-{risk_idx}",
                    title=f"Proof gap: {gap}"[:200],
                    status=ProgressStatus.RISK,
                    source_type=ProgressSource.PROOF_GAP,
                    source_ref=ev.get("timestamp", ""),
                    safe_summary=f"Proof gap detected ({gap})"[:200],
                )
                ledger.items.append(item)


# ---------------------------------------------------------------------------
# Unified builder
# ---------------------------------------------------------------------------


def build_progress_ledger(
    *,
    plan_text: str | None = None,
    live_review_text: str | None = None,
    context_text: str | None = None,
    job: Any = None,
    events: list[dict] | None = None,
) -> ProgressLedger:
    """Build a unified progress ledger from available sources."""
    if plan_text:
        ledger = build_progress_ledger_from_plan(plan_text)
    else:
        ledger = ProgressLedger()

    if live_review_text:
        merge_live_review_findings(ledger, live_review_text)

    if context_text:
        merge_known_risks(ledger, context_text)

    if job:
        merge_job_risks(ledger, job, events)

    return ledger


# ---------------------------------------------------------------------------
# Step 1021: Auto-checkoff contract
# ---------------------------------------------------------------------------


def mark_progress_item_done(
    ledger: ProgressLedger, item_id: str, evidence_ref: str
) -> bool:
    """Mark a progress item done with evidence. Returns True if found."""
    for item in ledger.items:
        if item.item_id == item_id:
            item.status = ProgressStatus.DONE
            item.evidence_refs.append(ProgressEvidence(
                ref=evidence_ref,
                description=f"Marked done: {evidence_ref}"[:200],
                source_type="manual_checkoff",
            ))
            return True
    return False


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def export_progress_ledger_json(ledger: ProgressLedger) -> dict:
    """Export ledger as safe JSON dict."""
    return {
        "version": ledger.version,
        "scope": ledger.scope,
        "verdict": ledger.verdict,
        "done_count": ledger.done_count,
        "open_count": ledger.open_count,
        "blocked_count": ledger.blocked_count,
        "risk_count": ledger.risk_count,
        "skipped_count": ledger.skipped_count,
        "total_count": len(ledger.items),
        "inconsistencies": ledger.inconsistencies,
        "items": [
            {
                "item_id": i.item_id,
                "title": i.title,
                "status": i.status.value,
                "source_type": i.source_type.value,
                "source_ref": i.source_ref,
                "severity": i.severity,
                "area": i.area,
                "evidence_count": len(i.evidence_refs),
                "next_action": i.next_action,
                "safe_summary": i.safe_summary,
            }
            for i in ledger.items
        ],
    }


def summarize_progress_ledger(ledger: ProgressLedger) -> str:
    """Human-readable progress summary."""
    lines = ["Progress Ledger", "=" * 40]
    if ledger.scope:
        lines.append(f"Scope: {ledger.scope}")
    if ledger.verdict:
        lines.append(f"Verdict: {ledger.verdict}")
    lines.append("")
    lines.append(
        f"Done: {ledger.done_count}  Open: {ledger.open_count}  "
        f"Blocked: {ledger.blocked_count}  Risks: {ledger.risk_count}  "
        f"Skipped: {ledger.skipped_count}"
    )
    lines.append("")

    status_icons = {
        ProgressStatus.DONE: "[x]",
        ProgressStatus.RESOLVED: "[x]",
        ProgressStatus.PLANNED: "[ ]",
        ProgressStatus.IN_PROGRESS: "[~]",
        ProgressStatus.BLOCKED: "[!]",
        ProgressStatus.RISK: "[?]",
        ProgressStatus.SKIPPED: "[-]",
        ProgressStatus.DEFERRED: "[-]",
    }

    for item in ledger.items:
        icon = status_icons.get(item.status, "[ ]")
        sev = f" ({item.severity})" if item.severity else ""
        lines.append(f"  {icon} {item.item_id} — {item.title}{sev}")

    if ledger.inconsistencies:
        lines.append("")
        lines.append("Inconsistencies:")
        for inc in ledger.inconsistencies:
            lines.append(f"  ! {inc}")

    return "\n".join(lines)
