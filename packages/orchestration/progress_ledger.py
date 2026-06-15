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
    RUN_CONTRACT_BLOCKER = "run_contract_blocker"


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
        # Snapshot integration (Step 1147): flag applies without verified snapshot
        for iid, rec in (meta.get("patch_intent_apply_records") or {}).items():
            if rec.get("state") == "applied" and not rec.get("snapshot_verified", False):
                risk_idx += 1
                item = ProgressItem(
                    item_id=f"risk-snap-{risk_idx}",
                    title=f"Apply without verified snapshot: {iid[:16]}"[:200],
                    status=ProgressStatus.RISK,
                    source_type=ProgressSource.PROOF_GAP,
                    source_ref=iid[:16],
                    severity="High",
                    safe_summary=f"Intent {iid[:16]} applied without snapshot_verified=True"[:200],
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
# Step 1059: Merge contract blockers
# ---------------------------------------------------------------------------


def extract_test_results_from_events(events: list[dict] | None) -> list[ProgressItem]:
    """Extract test run results from timeline events as ProgressItems."""
    if not events:
        return []
    items: list[ProgressItem] = []
    budget_exhausted_added = False
    for ev in events:
        ename = ev.get("event", "")
        meta = ev.get("metadata", ev)
        if ename in ("test_run_completed", "test_run_timed_out"):
            status_val = meta.get("status", "")
            run_id = meta.get("test_run_id", "")
            if status_val == "passed":
                items.append(ProgressItem(
                    item_id=f"test-pass-{run_id}",
                    title="Test run passed",
                    status=ProgressStatus.DONE,
                    source_type=ProgressSource.TEST_RESULT,
                    source_ref=run_id,
                    safe_summary=f"test_run_id={run_id} passed",
                ))
            elif status_val in ("failed", "timeout"):
                items.append(ProgressItem(
                    item_id=f"test-fail-{run_id}",
                    title=f"Test run {status_val}",
                    status=ProgressStatus.BLOCKED,
                    source_type=ProgressSource.TEST_RESULT,
                    severity="High",
                    source_ref=run_id,
                    safe_summary=f"test_run_id={run_id} {status_val} — check failure artifact",
                ))
        elif ename == "test_run_blocked" and not budget_exhausted_added:
            reason = meta.get("reason", "")
            if "budget" in reason or "max_test_runs" in reason or "exhausted" in reason:
                budget_exhausted_added = True
                items.append(ProgressItem(
                    item_id="test-budget-exhausted",
                    title="Test budget exhausted",
                    status=ProgressStatus.BLOCKED,
                    source_type=ProgressSource.RUN_CONTRACT_BLOCKER,
                    severity="High",
                    safe_summary="Test run budget exhausted — set max_test_runs higher",
                    next_action="remedy contract set <job_id> max_test_runs <n>",
                ))
    return items


def merge_test_results(ledger: ProgressLedger, events: list[dict] | None) -> None:
    """Merge test run items from events into the ledger."""
    items = extract_test_results_from_events(events)
    ledger.items.extend(items)


def extract_continuation_items_from_events(events: list[dict] | None) -> list[ProgressItem]:
    """Extract `remedy do --continue` progress items from events (Step 1176).

    Produces: continuation eligible, snapshot verified, apply completed, test
    passed/failed, proof verified, evidence incomplete. No automatic action.
    """
    if not events:
        return []
    items: list[ProgressItem] = []
    for ev in events:
        ename = ev.get("event", "")
        meta = ev.get("metadata", ev)
        if ename == "do_continue_started":
            items.append(ProgressItem(
                item_id="cont-eligible", title="Continuation eligible",
                status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
                source_ref=str(meta.get("intent_id", "")),
                safe_summary="Continuation cycle started for an approved intent.",
            ))
        elif ename == "do_continue_snapshot_verified":
            items.append(ProgressItem(
                item_id="cont-snapshot", title="Snapshot verified",
                status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
                source_ref=str(meta.get("snapshot_id", "")),
                safe_summary="Verified snapshot created before apply.",
            ))
        elif ename == "do_continue_applied":
            items.append(ProgressItem(
                item_id="cont-apply", title="Apply completed",
                status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
                source_ref=str(meta.get("apply_id", "")),
                safe_summary="Patch applied during continuation.",
            ))
        elif ename == "do_continue_test_completed":
            status_val = meta.get("status", "")
            if status_val == "passed":
                items.append(ProgressItem(
                    item_id="cont-test-pass", title="Continuation test passed",
                    status=ProgressStatus.DONE, source_type=ProgressSource.TEST_RESULT,
                    source_ref=str(meta.get("test_run_id", "")),
                    safe_summary="Linked test passed during continuation.",
                ))
            elif status_val in ("failed", "timeout"):
                items.append(ProgressItem(
                    item_id="cont-test-fail", title=f"Continuation test {status_val}",
                    status=ProgressStatus.BLOCKED, source_type=ProgressSource.TEST_RESULT,
                    severity="High", source_ref=str(meta.get("test_run_id", "")),
                    safe_summary="Continuation test failed — repair available.",
                    next_action="remedy repair start <job_id> <failure_artifact_id> --json",
                ))
        elif ename == "do_continue_proof_built":
            if meta.get("proof_status") == "verified":
                items.append(ProgressItem(
                    item_id="cont-proof", title="Proof verified",
                    status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
                    safe_summary="Change proof verified after continuation.",
                ))
        elif ename == "do_continue_stopped":
            reason = meta.get("stop_reason", "")
            if reason == "evidence_incomplete":
                items.append(ProgressItem(
                    item_id="cont-evidence-incomplete", title="Continuation evidence incomplete",
                    status=ProgressStatus.BLOCKED, source_type=ProgressSource.PROOF_GAP,
                    severity="High",
                    safe_summary="Apply may have succeeded but evidence degraded — manual review.",
                    next_action="remedy change proof <job_id> --json",
                ))
            elif reason == "snapshot_failed":
                items.append(ProgressItem(
                    item_id="cont-snapshot-failed", title="Continuation snapshot failed",
                    status=ProgressStatus.BLOCKED, source_type=ProgressSource.PROOF_GAP,
                    severity="High",
                    safe_summary="Snapshot could not be created/verified — investigate.",
                    next_action="remedy snapshot inspect <job_id> --json",
                ))
    return items


def merge_continuation_items(ledger: ProgressLedger, events: list[dict] | None) -> None:
    """Merge continuation progress items, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_continuation_items_from_events(events):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_repair_items_from_events(events: list[dict] | None) -> list[ProgressItem]:
    """Extract Repair Loop v1 progress items from events (Step 1206).

    Produces: repair needed, context ready, fix task created, repair patch intent
    pending approval, repair blocked, repair unavailable. De-duplicated by item_id
    on repeated reads. No automatic action.
    """
    if not events:
        return []
    items: list[ProgressItem] = []
    for ev in events:
        ename = ev.get("event", "")
        meta = ev.get("metadata", ev)
        if ename == "repair_attempt_requested":
            items.append(ProgressItem(
                item_id="repair-needed", title="Repair needed",
                status=ProgressStatus.IN_PROGRESS, source_type=ProgressSource.REPAIR_ARTIFACT,
                source_ref=str(meta.get("failure_artifact_id", "")),
                safe_summary="A repair was requested for a failing test.",
            ))
        elif ename == "repair_context_built":
            items.append(ProgressItem(
                item_id="repair-context", title="Repair context ready",
                status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
                source_ref=str(meta.get("failure_artifact_id", "")),
                safe_summary="Safe repair context built from the failure evidence.",
            ))
        elif ename == "repair_fix_task_created":
            items.append(ProgressItem(
                item_id="repair-fix-task", title="Fix task created",
                status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
                source_ref=str(meta.get("fix_task_id", "")),
                safe_summary="Fix task created from the failure evidence.",
            ))
        elif ename == "repair_approval_required":
            items.append(ProgressItem(
                item_id="repair-approval", title="Repair patch intent pending approval",
                status=ProgressStatus.BLOCKED, source_type=ProgressSource.REPAIR_ARTIFACT,
                severity="Medium", source_ref=str(meta.get("repair_intent_id", "")),
                safe_summary="A repair patch intent awaits approval. No apply yet.",
                next_action="remedy patch approve <job_id> <repair_intent_id>",
            ))
        elif ename == "repair_attempt_blocked":
            items.append(ProgressItem(
                item_id="repair-blocked", title="Repair blocked",
                status=ProgressStatus.BLOCKED, source_type=ProgressSource.REPAIR_ARTIFACT,
                severity="Medium", source_ref=str(meta.get("failure_artifact_id", "")),
                safe_summary="Repair could not proceed — review the blocker.",
                next_action="remedy repair status <job_id> --json",
            ))
        # Approved Repair Apply Cycle items (Step 1229).
        elif ename == "repair_apply_reconciled":
            rstatus = str(meta.get("status", ""))
            if rstatus == "tested_passed":
                items.append(ProgressItem(
                    item_id="repair-apply-tested-passed", title="Repair applied and tested (passed)",
                    status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
                    source_ref=str(meta.get("repair_attempt_id", "")),
                    safe_summary="Repair applied through do continue; linked test passed.",
                ))
            elif rstatus == "evidence_incomplete":
                items.append(ProgressItem(
                    item_id="repair-apply-evidence-incomplete", title="Repair evidence incomplete",
                    status=ProgressStatus.BLOCKED, source_type=ProgressSource.PROOF_GAP,
                    severity="High", source_ref=str(meta.get("repair_attempt_id", "")),
                    safe_summary="Repair applied but evidence degraded — inspect evidence.",
                    next_action="remedy change proof <job_id> --json",
                ))
            elif rstatus == "applied":
                items.append(ProgressItem(
                    item_id="repair-applied", title="Repair applied",
                    status=ProgressStatus.IN_PROGRESS, source_type=ProgressSource.REPAIR_ARTIFACT,
                    source_ref=str(meta.get("repair_attempt_id", "")),
                    safe_summary="Repair intent applied through do continue.",
                ))
        elif ename == "repair_tested_failed":
            items.append(ProgressItem(
                item_id="repair-apply-tested-failed", title="Repair applied but test failed",
                status=ProgressStatus.BLOCKED, source_type=ProgressSource.TEST_RESULT,
                severity="High", source_ref=str(meta.get("repair_attempt_id", "")),
                safe_summary="Repair applied; linked test failed — failure stays open, no auto-loop.",
                next_action="remedy repair status <job_id> --json",
            ))
        elif ename == "repair_failure_resolved":
            items.append(ProgressItem(
                item_id="repair-failure-resolved", title="Failure resolved by repair",
                status=ProgressStatus.RESOLVED, source_type=ProgressSource.REPAIR_ARTIFACT,
                source_ref=str(meta.get("failure_artifact_id", "")),
                safe_summary="Original failure resolved: snapshot + linked passing test + proof.",
            ))
    return items


def merge_repair_items(ledger: ProgressLedger, events: list[dict] | None) -> None:
    """Merge Repair Loop v1 progress items, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_repair_items_from_events(events):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_overnight_items(report: dict | None) -> list[ProgressItem]:
    """Extract Bounded Overnight Prep progress items from an overnight readiness
    report dict (Step 1259). Read-only; no duplicates. Empty when no report."""
    if not report:
        return []
    items: list[ProgressItem] = []
    blockers = report.get("blockers", []) or []
    ev = report.get("evidence_summary", {}) or {}
    budget = report.get("budget_summary", {}) or {}

    if report.get("can_run_unattended"):
        items.append(ProgressItem(
            item_id="overnight-ready", title="Overnight ready (policy-permitting)",
            status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
            safe_summary="Job assessed ready for a bounded unattended run."))
    elif blockers:
        items.append(ProgressItem(
            item_id="overnight-blocked", title="Overnight blocked",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Medium", safe_summary="Job not safe to run unattended.",
            next_action="remedy overnight readiness <job_id> --json"))

    if ev.get("pending_intents") or ev.get("pending_repair_intents"):
        items.append(ProgressItem(
            item_id="overnight-human-decision", title="Human decision required",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Medium", safe_summary="Approvals pending before any unattended run.",
            next_action="remedy overnight readiness <job_id> --json"))
    if ev.get("pending_repair_intents"):
        items.append(ProgressItem(
            item_id="overnight-repair-pending", title="Repair pending approval",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.REPAIR_ARTIFACT,
            severity="Medium", safe_summary="A repair patch intent awaits approval."))
    if budget.get("loops_exhausted") or budget.get("test_runs_exhausted"):
        items.append(ProgressItem(
            item_id="overnight-budget-exhausted", title="Budget exhausted",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.RUN_CONTRACT_BLOCKER,
            severity="Medium", safe_summary="A run-contract budget is exhausted.",
            next_action="remedy contract inspect <job_id> --json"))
    if ev.get("proof_status") == "verified":
        items.append(ProgressItem(
            item_id="overnight-proof-ready", title="Proof verified",
            status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
            safe_summary="Change proof is verified."))
    if "evidence_incomplete" in report.get("stop_reasons", []):
        items.append(ProgressItem(
            item_id="overnight-evidence-incomplete", title="Evidence incomplete",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.PROOF_GAP,
            severity="High", safe_summary="Evidence incomplete — inspect before any run.",
            next_action="remedy change proof <job_id> --json"))
    return items


def merge_overnight_items(ledger: ProgressLedger, report: dict | None) -> None:
    """Merge overnight prep items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_overnight_items(report):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_overnight_run_items(record: dict | None) -> list[ProgressItem]:
    """Extract Bounded Overnight Executor progress items from the latest run
    record (Step 1289). Read-only; fixed item_ids → no duplicates. Empty when no
    record. Reflects the executor's own truth (selected/executed/stopped)."""
    if not record:
        return []
    items: list[ProgressItem] = []
    selected = (record.get("selected_action") or {}).get("kind", "none")
    executed = (record.get("executed_action") or {}).get("kind", "none")
    stop = record.get("stop_reason", "")
    items.append(ProgressItem(
        item_id="overnight-run-requested", title="Overnight run requested",
        status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
        safe_summary=f"Mode {record.get('mode', 'report_only')}."))
    items.append(ProgressItem(
        item_id="overnight-run-action-selected", title="Overnight action selected",
        status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
        safe_summary=f"Selected: {selected}."))
    if executed and executed != "none":
        items.append(ProgressItem(
            item_id="overnight-run-action-executed", title="Overnight action executed",
            status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
            safe_summary=f"Executed: {executed} (stop={stop})."))
    if stop == "completed_verified":
        items.append(ProgressItem(
            item_id="overnight-run-completed-verified", title="Overnight completed (verified)",
            status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
            safe_summary="One bounded cycle completed and verified."))
    elif stop == "evidence_incomplete":
        items.append(ProgressItem(
            item_id="overnight-run-evidence-incomplete", title="Overnight evidence incomplete",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.PROOF_GAP,
            severity="High", safe_summary="Run stopped with incomplete evidence.",
            next_action="remedy change proof <job_id> --json"))
    elif stop in ("review_findings_open", "budget_exhausted", "medium_or_high_risk",
                  "human_approval_required", "contract_blocked", "permission_missing"):
        items.append(ProgressItem(
            item_id="overnight-run-blocked", title="Overnight run blocked",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Medium", safe_summary=f"Run blocked: {stop}.",
            next_action="remedy overnight readiness <job_id> --json"))
    else:
        items.append(ProgressItem(
            item_id="overnight-run-stopped", title="Overnight run stopped",
            status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
            safe_summary=f"Run stopped: {stop}."))
    return items


def merge_overnight_run_items(ledger: ProgressLedger, record: dict | None) -> None:
    """Merge overnight executor run items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_overnight_run_items(record):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_provider_trust_items(reports: dict | None) -> list[ProgressItem]:
    """Extract Provider Trust Gate progress items from persisted trust reports
    (Step 1322). Read-only; fixed item_ids → no duplicates. Safe summaries only."""
    if not reports:
        return []
    vals = list(reports.values())
    accepted = [r for r in vals if r.get("trust_status") == "accepted"]
    rejected = [r for r in vals if r.get("trust_status") == "rejected"]
    needs = [r for r in vals if r.get("trust_status") == "needs_human_review"]
    pending = [r for r in accepted if r.get("repair_intent_id")]
    items: list[ProgressItem] = []
    items.append(ProgressItem(
        item_id="provider-output-received", title="Provider output received",
        status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
        safe_summary=f"{len(vals)} provider trust report(s) on record."))
    if rejected:
        items.append(ProgressItem(
            item_id="provider-trust-rejected", title="Provider output rejected",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Medium", safe_summary=f"{len(rejected)} provider candidate(s) rejected by trust gate.",
            next_action="remedy provider trust-show <job_id> <report_id> --json"))
    if needs:
        items.append(ProgressItem(
            item_id="provider-trust-needs-review", title="Provider output needs review",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Medium", safe_summary=f"{len(needs)} provider candidate(s) need human review.",
            next_action="remedy provider trust-show <job_id> <report_id> --json"))
    if pending:
        items.append(ProgressItem(
            item_id="provider-repair-intent-pending", title="Provider repair intent pending approval",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.REPAIR_ARTIFACT,
            severity="Medium", safe_summary=f"{len(pending)} provider repair intent(s) pending approval.",
            next_action="remedy patch approve <job_id> <intent_id> --json"))
    elif accepted and not pending:
        items.append(ProgressItem(
            item_id="provider-repair-unavailable", title="Provider repair unavailable",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Low", safe_summary="Accepted provider candidate produced no pending intent."))
    return items


def merge_provider_trust_items(ledger: ProgressLedger, reports: dict | None) -> None:
    """Merge provider trust items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_provider_trust_items(reports):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_provider_material_items(materials: dict | None) -> list[ProgressItem]:
    """Extract Provider Patch Materialization progress items from persisted material
    manifests (Step 1348). Read-only; fixed item_ids → no duplicates."""
    if not materials:
        return []
    vals = list(materials.values())
    materialized = [m for m in vals if m.get("material_state") == "materialized"]
    failed = [m for m in vals if m.get("material_state") == "materialization_failed"]
    pending = [m for m in materialized if m.get("linked_intent_id")]
    items: list[ProgressItem] = []
    if materialized:
        items.append(ProgressItem(
            item_id="provider-patch-materialized", title="Provider patch materialized",
            status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
            safe_summary=f"{len(materialized)} provider patch(es) materialized into pending intents."))
    if pending:
        items.append(ProgressItem(
            item_id="provider-repair-intent-pending-approval", title="Provider repair intent pending approval",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.REPAIR_ARTIFACT,
            severity="Medium", safe_summary=f"{len(pending)} materialized provider repair intent(s) pending approval.",
            next_action="remedy patch approve <job_id> <intent_id> --json"))
    if failed:
        items.append(ProgressItem(
            item_id="provider-materialization-failed", title="Provider materialization failed",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Low", safe_summary=f"{len(failed)} provider candidate(s) failed materialization.",
            next_action="remedy provider material-show <job_id> <material_id> --json"))
    return items


def merge_provider_material_items(ledger: ProgressLedger, materials: dict | None) -> None:
    """Merge provider material items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_provider_material_items(materials):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_local_candidate_items(runs: list[dict] | None) -> list[ProgressItem]:
    """Extract Automated Local Candidate Generator v0 progress items (Step 1624) from persisted
    run manifests. Read-only; fixed item_ids → no duplicates. Generation never auto-applies."""
    if not runs:
        return []
    latest = runs[-1]
    items: list[ProgressItem] = [ProgressItem(
        item_id="local-candidate-run", title="Local candidate generation run",
        status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
        safe_summary=f"{len(runs)} local candidate generation run(s); latest={latest.get('status','')}.")]
    if any(r.get("status") == "unavailable" for r in runs):
        items.append(ProgressItem(
            item_id="local-candidate-unavailable", title="Local candidate generator unavailable",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK, severity="Low",
            safe_summary="Local candidate model unavailable on a run (deterministic flow unaffected).",
            next_action="remedy local-candidate status --json"))
    if any(r.get("status") == "trust_rejected" for r in runs):
        items.append(ProgressItem(
            item_id="local-candidate-trust-rejected", title="Local candidate trust rejected",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK, severity="Medium",
            safe_summary="A local candidate was rejected by the Trust Gate.",
            next_action="remedy local-candidate status --json"))
    if any(r.get("status") == "verification_rejected" for r in runs):
        items.append(ProgressItem(
            item_id="local-candidate-verification-rejected", title="Local candidate verification rejected",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK, severity="Medium",
            safe_summary="A local candidate was rejected by Verification.",
            next_action="remedy provider verification-show <job_id> <verification_id> --json"))
    if any(r.get("status") == "needs_review" for r in runs):
        items.append(ProgressItem(
            item_id="local-candidate-needs-review", title="Local candidate needs review",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK, severity="Medium",
            safe_summary="A local candidate needs human review after verification.",
            next_action="remedy provider verification-show <job_id> <verification_id> --json"))
    pending = [r for r in runs if r.get("status") == "intent_pending_approval" and r.get("intent_id")]
    if pending:
        items.append(ProgressItem(
            item_id="local-candidate-intent-pending", title="Local candidate intent pending approval",
            status=ProgressStatus.PLANNED, source_type=ProgressSource.REPAIR_ARTIFACT,
            safe_summary=f"{len(pending)} local-candidate repair intent(s) pending approval.",
            next_action="remedy patch approve <job_id> <intent_id> --json"))
    return items


def merge_local_candidate_items(ledger: ProgressLedger, runs: list[dict] | None) -> None:
    """Merge local candidate items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_local_candidate_items(runs):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_provider_verification_items(reports: dict | None) -> list[ProgressItem]:
    """Extract Provider Trust Verification v1 progress items (Step 1556) from persisted
    verification reports. Read-only; fixed item_ids → no duplicates."""
    if not reports:
        return []
    vals = list(reports.values())
    passed = [r for r in vals if r.get("decision") == "verification_passed"]
    needs = [r for r in vals if r.get("decision") == "needs_human_review"]
    rejected = [r for r in vals if r.get("decision") == "verification_rejected"]
    incomplete = [r for r in vals if r.get("decision") == "verification_incomplete"]
    loop = [r for r in vals if r.get("loop_risk") in ("medium", "high")]
    items: list[ProgressItem] = []
    items.append(ProgressItem(
        item_id="provider-verification-run", title="Provider verification run",
        status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
        safe_summary=f"{len(vals)} provider verification report(s) on record."))
    if passed:
        items.append(ProgressItem(
            item_id="provider-verification-passed", title="Provider verification passed",
            status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
            safe_summary=f"{len(passed)} candidate(s) passed verification (pending approval, not applied)."))
    if needs:
        items.append(ProgressItem(
            item_id="provider-verification-needs-review", title="Provider verification needs review",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK,
            severity="Medium", safe_summary=f"{len(needs)} candidate(s) need human review after verification.",
            next_action="remedy provider verification-show <job_id> <verification_id> --json"))
    if rejected:
        items.append(ProgressItem(
            item_id="provider-verification-rejected", title="Provider verification rejected",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK,
            severity="Medium", safe_summary=f"{len(rejected)} candidate(s) rejected by verification.",
            next_action="remedy provider verification-show <job_id> <verification_id> --json"))
    if incomplete:
        items.append(ProgressItem(
            item_id="provider-verification-incomplete", title="Provider verification incomplete",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Low", safe_summary=f"{len(incomplete)} verification(s) incomplete (no intent)."))
    if loop:
        items.append(ProgressItem(
            item_id="provider-verification-loop-risk", title="Provider verification loop risk",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK,
            severity="High", safe_summary=f"{len(loop)} verification(s) flagged loop risk (repeated candidate).",
            next_action="remedy provider verification-show <job_id> <verification_id> --json"))
    return items


def merge_provider_verification_items(ledger: ProgressLedger, reports: dict | None) -> None:
    """Merge provider verification items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_provider_verification_items(reports):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_builder_routing_items(traces: list[dict] | None) -> list[ProgressItem]:
    """Extract Expensive Builder Routing v0 progress items (Step 1592) from persisted routing
    traces. Read-only; fixed item_ids → no duplicates. Routing recommends only — no execution."""
    if not traces:
        return []
    latest = traces[-1]
    tier = latest.get("selected_tier", "")
    items: list[ProgressItem] = [ProgressItem(
        item_id="builder-routing-decision", title="Builder routing decision created",
        status=ProgressStatus.DONE, source_type=ProgressSource.FEATURE_SUGGESTION,
        safe_summary=f"{len(traces)} builder routing decision(s); latest tier={tier}.")]
    _tier_item = {
        "deterministic_only": ("builder-routing-deterministic", "Deterministic route selected",
                               ProgressStatus.DONE, ProgressSource.FEATURE_SUGGESTION, "", ""),
        "local_advisor": ("builder-routing-local-advisor", "Local advisor route selected",
                          ProgressStatus.DONE, ProgressSource.FEATURE_SUGGESTION, "", ""),
        "local_candidate_generator": ("builder-routing-local-candidate",
                                      "Local candidate route recommended", ProgressStatus.PLANNED,
                                      ProgressSource.FEATURE_SUGGESTION, "Low",
                                      "Local candidate generation recommended (not executed in v0)."),
        "external_candidate_generator": ("builder-routing-external-candidate",
                                         "External candidate route recommended", ProgressStatus.PLANNED,
                                         ProgressSource.FEATURE_SUGGESTION, "Medium",
                                         "External candidate generation recommended (not executed in v0)."),
        "human_review_required": ("builder-routing-human-review", "Builder routing needs human review",
                                  ProgressStatus.RISK, ProgressSource.KNOWN_RISK, "Medium",
                                  "Routing escalated to human review."),
        "no_safe_route": ("builder-routing-blocked", "Builder route blocked / no safe route",
                          ProgressStatus.BLOCKED, ProgressSource.KNOWN_RISK, "Low",
                          "No safe builder route; gather evidence or prepare a request package."),
    }.get(tier)
    if _tier_item:
        iid, title, status, src, sev, summ = _tier_item
        items.append(ProgressItem(
            item_id=iid, title=title, status=status, source_type=src, severity=sev,
            safe_summary=summ or f"Builder routing selected {tier}.",
            next_action=latest.get("next_safe_action", "")))
    return items


def merge_builder_routing_items(ledger: ProgressLedger, traces: list[dict] | None) -> None:
    """Merge builder routing items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_builder_routing_items(traces):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_repair_request_items(packages: dict | None, materials: dict | None) -> list[ProgressItem]:
    """Extract Repair Request Builder progress items (Step 1378). Read-only; fixed
    item_ids → no duplicates. A request package with no materialized candidate yet is
    an external candidate still pending import."""
    if not packages:
        return []
    pkgs = list(packages.values())
    materialized_failures = {m.get("failure_artifact_id") for m in (materials or {}).values()
                             if m.get("material_state") == "materialized"}
    pending = [p for p in pkgs if p.get("failure_artifact_id") not in materialized_failures]
    items: list[ProgressItem] = []
    items.append(ProgressItem(
        item_id="repair-request-prepared", title="Repair request prepared",
        status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
        safe_summary=f"{len(pkgs)} provider-agnostic repair request package(s) prepared."))
    if pending:
        items.append(ProgressItem(
            item_id="external-candidate-pending", title="External candidate pending",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Low", safe_summary=f"{len(pending)} request(s) awaiting an external candidate response.",
            next_action="remedy provider intake-repair <job_id> --failure-artifact-id <id> --input <file> --provider <label> --json"))
    if materialized_failures & {p.get("failure_artifact_id") for p in pkgs}:
        items.append(ProgressItem(
            item_id="external-candidate-imported", title="External candidate imported",
            status=ProgressStatus.DONE, source_type=ProgressSource.REPAIR_ARTIFACT,
            safe_summary="An external candidate was imported and materialized."))
    return items


def merge_repair_request_items(ledger: ProgressLedger, packages: dict | None,
                               materials: dict | None) -> None:
    """Merge repair request items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_repair_request_items(packages, materials):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_self_dogfood_items(proposed_tasks: list | None) -> list[ProgressItem]:
    """Extract Self-Dogfood progress items from durable self-dogfood ProposedTasks
    (Step 1415). Read-only; fixed item_ids → no duplicates."""
    if not proposed_tasks:
        return []
    sd = [t for t in proposed_tasks if getattr(t, "task_type", "") == "self_dogfood"]
    if not sd:
        return []

    def _st(t: Any) -> str:
        s = getattr(t, "status", "")
        return str(getattr(s, "value", s)).lower()

    proposed = [t for t in sd if _st(t) in ("proposed", "evaluated")]
    approved = [t for t in sd if "approved" in _st(t)]
    deferred = [t for t in sd if "deferred" in _st(t)]
    items: list[ProgressItem] = []
    items.append(ProgressItem(
        item_id="self-improvement-proposed", title="Self-improvement tasks proposed",
        status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
        safe_summary=f"{len(sd)} self-dogfood task(s) proposed."))
    if proposed:
        items.append(ProgressItem(
            item_id="self-improvement-pending-evaluation", title="Self-improvement awaiting evaluation",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK,
            severity="Low", safe_summary=f"{len(proposed)} self-dogfood task(s) await human evaluation.",
            next_action="remedy decision list <job_id> --json"))
    if approved:
        items.append(ProgressItem(
            item_id="self-improvement-approved", title="Self-improvement approved",
            status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
            safe_summary=f"{len(approved)} self-dogfood task(s) approved for build."))
    if deferred:
        items.append(ProgressItem(
            item_id="self-improvement-deferred", title="Self-improvement deferred",
            status=ProgressStatus.DEFERRED, source_type=ProgressSource.KNOWN_RISK,
            safe_summary=f"{len(deferred)} self-dogfood task(s) deferred."))
    return items


def merge_self_dogfood_items(ledger: ProgressLedger, proposed_tasks: list | None) -> None:
    """Merge self-dogfood items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_self_dogfood_items(proposed_tasks):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_self_execution_items(attempts: list | None) -> list[ProgressItem]:
    """Extract Self-Dogfood Execution progress items from attempts (Step 1442).
    Read-only; fixed item_ids → no duplicates. `attempts` are safe dicts."""
    if not attempts:
        return []
    states = [a.get("state", "") for a in attempts]
    items: list[ProgressItem] = []
    items.append(ProgressItem(
        item_id="self-execution-started", title="Self-improvement attempt started",
        status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
        safe_summary=f"{len(attempts)} self-improvement attempt(s)."))
    awaiting = sum(1 for s in states if s == "awaiting_external_candidate")
    pending = sum(1 for s in states if s == "intent_pending_approval")
    completed = sum(1 for s in states if s == "completed")
    blocked = sum(1 for s in states if s == "blocked")
    if awaiting:
        items.append(ProgressItem(
            item_id="self-execution-awaiting-candidate", title="Self attempt awaiting external candidate",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK, severity="Low",
            safe_summary=f"{awaiting} attempt(s) awaiting an external candidate.",
            next_action="remedy provider intake-repair <job_id> --input <file> --provider self_dogfood --json"))
    if pending:
        items.append(ProgressItem(
            item_id="self-execution-intent-pending", title="Self attempt intent pending approval",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.REPAIR_ARTIFACT, severity="Medium",
            safe_summary=f"{pending} self intent(s) pending approval.",
            next_action="remedy patch approve <job_id> <intent_id> --json"))
    if completed:
        items.append(ProgressItem(
            item_id="self-execution-completed", title="Self-improvement completed",
            status=ProgressStatus.DONE, source_type=ProgressSource.PROOF_GAP,
            safe_summary=f"{completed} self-improvement attempt(s) completed (proof verified)."))
    if blocked:
        items.append(ProgressItem(
            item_id="self-execution-blocked", title="Self-improvement attempt blocked",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK, severity="Low",
            safe_summary=f"{blocked} self-improvement attempt(s) blocked.",
            next_action="remedy self status --json"))
    return items


def merge_self_execution_items(ledger: ProgressLedger, attempts: list | None) -> None:
    """Merge self-execution items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_self_execution_items(attempts):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_orchestrator_items(latest_decision: dict | None) -> list[ProgressItem]:
    """Extract Orchestrator Brain progress items from the latest decision (Step 1481).
    Read-only; fixed item_ids → no duplicates."""
    if not latest_decision:
        return []
    stop = latest_decision.get("stop_reason", "")
    tier = (latest_decision.get("model_routing_plan") or {}).get("tier", "")
    loop = latest_decision.get("loop_guard_status", "")
    items: list[ProgressItem] = []
    items.append(ProgressItem(
        item_id="orchestrator-decision-created", title="Orchestrator decision created",
        status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
        safe_summary=f"Latest decision: {stop} (confidence {latest_decision.get('confidence','')})."))
    if stop == "human_review_required" or loop in ("block", "require_human_review"):
        items.append(ProgressItem(
            item_id="orchestrator-human-review", title="Orchestrator requires human review",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK, severity="Medium",
            safe_summary="Orchestrator routed the next step to human review.",
            next_action="remedy orchestrator report --json"))
    elif stop in ("no_safe_action", "evidence_incomplete"):
        items.append(ProgressItem(
            item_id="orchestrator-blocked", title="Orchestrator has no safe action",
            status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK, severity="Low",
            safe_summary=f"Orchestrator stop: {stop}.",
            next_action="remedy orchestrator inspect --json"))
    if tier == "local_advisor_preferred":
        items.append(ProgressItem(
            item_id="orchestrator-local-advisor", title="Local model advisor recommended",
            status=ProgressStatus.RISK, source_type=ProgressSource.FEATURE_SUGGESTION,
            safe_summary="A future local advisor could critique the plan (not built)."))
    elif tier == "external_builder_needed":
        items.append(ProgressItem(
            item_id="orchestrator-external-builder", title="External builder recommended",
            status=ProgressStatus.RISK, source_type=ProgressSource.FEATURE_SUGGESTION,
            safe_summary="Candidate generation is the bottleneck (output via Trust Gate only)."))
    return items


def merge_orchestrator_items(ledger: ProgressLedger, latest_decision: dict | None) -> None:
    """Merge orchestrator items into a ledger, de-duplicated by item_id."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_orchestrator_items(latest_decision):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_local_advisor_items(latest_decision: dict | None) -> list[ProgressItem]:
    """Extract Local Model Advisor progress items from the latest decision's advisor critique
    (Step 1517). Read-only; fixed item_ids → no duplicates. No raw prompt/response."""
    if not latest_decision:
        return []
    adv = latest_decision.get("advisor") or {}
    if not adv:
        return []
    status = adv.get("status", "")
    impact = adv.get("decision_impact", "")
    items: list[ProgressItem] = []
    if status in ("unavailable", "blocked"):
        items.append(ProgressItem(
            item_id="local-advisor-unavailable", title="Local advisor unavailable",
            status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK, severity="Low",
            safe_summary=f"Local advisor {status} ({adv.get('stop_reason','')}); "
                         "deterministic decision unchanged.",
            next_action="remedy local-advisor status --json"))
        return items
    if status in ("completed", "reused"):
        items.append(ProgressItem(
            item_id="local-advisor-run", title="Local advisor consulted",
            status=ProgressStatus.DONE, source_type=ProgressSource.KNOWN_RISK,
            safe_summary=f"Local advisor {status}; impact {impact}."))
        if adv.get("suggested_concerns"):
            items.append(ProgressItem(
                item_id="local-advisor-concern", title="Local advisor raised a concern",
                status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK, severity="Low",
                safe_summary=f"{len(adv['suggested_concerns'])} advisor concern(s) — advisory only.",
                next_action="remedy orchestrator report --json"))
        if impact == "confidence_adjusted":
            items.append(ProgressItem(
                item_id="local-advisor-confidence", title="Local advisor adjusted confidence",
                status=ProgressStatus.RISK, source_type=ProgressSource.KNOWN_RISK, severity="Low",
                safe_summary="Advisor lowered decision confidence; action unchanged."))
        elif impact == "human_review_required":
            items.append(ProgressItem(
                item_id="local-advisor-human-review", title="Local advisor escalated to human review",
                status=ProgressStatus.BLOCKED, source_type=ProgressSource.KNOWN_RISK, severity="Medium",
                safe_summary="Advisor flagged high risk on weak evidence — human review required.",
                next_action="remedy orchestrator report --json"))
    return items


def merge_local_advisor_items(ledger: ProgressLedger, latest_decision: dict | None) -> None:
    """Merge local advisor items into a ledger, de-duplicated by item_id (Step 1517)."""
    seen = {i.item_id for i in ledger.items}
    for item in extract_local_advisor_items(latest_decision):
        if item.item_id not in seen:
            ledger.items.append(item)
            seen.add(item.item_id)


def extract_contract_decisions_from_events(events: list[dict] | None) -> list[dict]:
    """Extract contract decision metadata from timeline events."""
    if not events:
        return []
    decisions: list[dict] = []
    for ev in events:
        if ev.get("event") == "contract_decision":
            meta = ev.get("metadata", ev)
            decisions.append(meta)
    return decisions


def merge_contract_blockers(
    ledger: ProgressLedger, contract_decisions: list[dict] | None = None,
) -> None:
    """Merge run contract blockers into ledger."""
    if not contract_decisions:
        return

    idx = 0
    for dec in contract_decisions:
        if dec.get("allowed"):
            continue
        idx += 1
        severity = "High" if dec.get("status") == "blocked" else "Medium"
        item = ProgressItem(
            item_id=f"contract-blocker-{idx}",
            title=f"Contract: {dec.get('reason', 'blocked')}"[:200],
            status=ProgressStatus.BLOCKED,
            source_type=ProgressSource.RUN_CONTRACT_BLOCKER,
            source_ref="run_contract",
            severity=severity,
            safe_summary=f"Contract {dec.get('status', 'blocked')}: {dec.get('reason', '')}"[:200],
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
    contract_decisions: list[dict] | None = None,
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

    # Auto-extract contract decisions from events if not explicitly provided
    effective_decisions = contract_decisions
    if not effective_decisions and events:
        effective_decisions = extract_contract_decisions_from_events(events)
    if effective_decisions:
        merge_contract_blockers(ledger, effective_decisions)

    # Auto-extract test results from events
    if events:
        merge_test_results(ledger, events)
        merge_continuation_items(ledger, events)
        merge_repair_items(ledger, events)

    # Overnight executor run items from the latest durable run record (Step 1289).
    if job is not None:
        try:
            from packages.orchestration.overnight_executor import latest_run_record
            merge_overnight_run_items(ledger, latest_run_record(str(job.id)))
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

    # Provider trust gate items from persisted trust reports (Step 1322).
    if job is not None:
        try:
            from packages.orchestration.provider_trust import load_trust_reports
            merge_provider_trust_items(ledger, load_trust_reports(job))
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

    # Provider patch materialization items from persisted materials (Step 1348).
    if job is not None:
        try:
            from packages.orchestration.provider_patch_material import load_materials
            merge_provider_material_items(ledger, load_materials(job))
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

    # Provider Trust Verification v1 items from persisted verification reports (Step 1556).
    if job is not None:
        try:
            from packages.orchestration.provider_trust_verification import load_verification_reports
            merge_provider_verification_items(ledger, load_verification_reports(job))
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

    # Repair request builder items from persisted request packages (Step 1378).
    if job is not None:
        try:
            from packages.orchestration.repair_request_builder import load_request_packages
            from packages.orchestration.provider_patch_material import load_materials as _lm
            merge_repair_request_items(ledger, load_request_packages(job), _lm(job))
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

    # Self-dogfood items from durable self-dogfood ProposedTasks (Step 1415).
    if job is not None:
        try:
            from packages.orchestration.proposed_tasks import load_proposed_tasks_safe
            pts, _degraded = load_proposed_tasks_safe(str(job.id))
            merge_self_dogfood_items(ledger, pts)
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

    # Self-dogfood execution attempts for this job (Step 1442).
    if job is not None:
        try:
            from packages.orchestration.self_dogfood_execution import list_attempts
            mine = [a for a in list_attempts() if a.get("job_id") == str(job.id)]
            merge_self_execution_items(ledger, mine)
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

    # Orchestrator brain latest decision (Step 1481).
    try:
        from packages.orchestration.orchestrator_brain import list_decisions
        scope = f"job:{job.id}" if job is not None else "repository"
        decisions = list_decisions(scope)
        latest = decisions[-1] if decisions else None
        merge_orchestrator_items(ledger, latest)
        # Local model advisor items from the latest decision's advisor critique (Step 1517).
        merge_local_advisor_items(ledger, latest)
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass

    # Expensive builder routing items from persisted routing traces (Step 1592).
    try:
        from packages.orchestration.builder_routing import load_builder_routing_traces
        scope = f"job:{job.id}" if job is not None else "repository"
        merge_builder_routing_items(ledger, load_builder_routing_traces(scope=scope))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass

    # Automated local candidate generation items from persisted run manifests (Step 1624).
    if job is not None:
        try:
            from packages.orchestration.local_candidate_generator import list_local_candidate_runs
            mine = [r for r in list_local_candidate_runs() if r.get("job_id") == str(job.id)]
            merge_local_candidate_items(ledger, mine)
        except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
            pass

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
