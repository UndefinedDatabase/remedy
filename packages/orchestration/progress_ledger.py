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
