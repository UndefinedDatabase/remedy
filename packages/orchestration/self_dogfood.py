"""
Self-Dogfood Readiness + Self-Improvement Planner v0 (Steps 1399-1428).

Lets Remedy inspect its OWN evidence — live review verdict, handoff state, missing
evidence, failed tests, repair/provider chains, roadmap position — and produce
structured SelfImprovementItems + a Plan + ProposedTasks that flow through the
EXISTING approval workflow.

This is a PLANNING RAIL, not autonomous self-modification. It never edits code,
applies patches, approves tasks, inserts Job.tasks directly, creates PRs, does git
operations, runs in the background, or calls a provider/network/subprocess. Inspect
and plan are read-only; propose is metadata-only (creates ProposedTasks). All text is
scrubbed; no raw source/diff/logs/secrets/tracebacks/absolute paths leave this module.

Public API::

    build_self_dogfood_inspection(job_id=None, data_dir=None, agent_dir=None) -> SelfDogfoodInspection
    build_self_improvement_plan(...) -> SelfImprovementPlan
    propose_self_improvement(job_id, item_ids=None, top=None, data_dir=None, agent_dir=None) -> SelfDogfoodResult
    build_self_dogfood_report(...) -> dict
    export_inspection_json / export_plan_json / export_result_json / render_report_markdown
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

# ---------------------------------------------------------------------------
# Vocabularies (Steps 1400/1401/1407)
# ---------------------------------------------------------------------------


class SourceStatus:
    AVAILABLE = "available"
    MISSING = "missing"
    MALFORMED = "malformed"
    STALE = "stale"


class ItemType:
    BUG = "bug"
    SAFETY_GAP = "safety_gap"
    EVIDENCE_GAP = "evidence_gap"
    TEST_GAP = "test_gap"
    DOCS_GAP = "docs_gap"
    UX_GAP = "ux_gap"
    ARCHITECTURE_GAP = "architecture_gap"
    ROADMAP_NEXT = "roadmap_next"
    CLEANUP = "cleanup"
    SECURITY_HARDENING = "security_hardening"


class Priority:
    BLOCKER = "blocker"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Confidence:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


_PRIORITY_ORDER = {Priority.BLOCKER: 0, Priority.HIGH: 1, Priority.MEDIUM: 2, Priority.LOW: 3}


# ---------------------------------------------------------------------------
# Models (Step 1400)
# ---------------------------------------------------------------------------


@dataclass
class SelfImprovementEvidence:
    source: str
    ref: str = ""
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source, "ref": self.ref, "summary": self.summary}


@dataclass
class SelfImprovementSource:
    name: str
    status: str
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "status": self.status, "summary": self.summary}


@dataclass
class SelfImprovementRisk:
    id: str
    severity: str
    summary: str
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "severity": self.severity, "summary": self.summary,
                "source": self.source}


@dataclass
class SelfImprovementAction:
    label: str
    command: str
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"label": self.label, "command": self.command, "reason": self.reason}


@dataclass
class SelfImprovementItem:
    item_id: str
    fingerprint: str
    item_type: str
    priority: str
    confidence: str
    title: str
    detail: str = ""
    source_type: str = ""
    evidence: list[SelfImprovementEvidence] = field(default_factory=list)
    next_action: SelfImprovementAction | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id, "fingerprint": self.fingerprint,
            "item_type": self.item_type, "priority": self.priority,
            "confidence": self.confidence, "title": self.title, "detail": self.detail,
            "source_type": self.source_type,
            "evidence": [e.to_dict() for e in self.evidence],
            "next_action": self.next_action.to_dict() if self.next_action else None,
        }


@dataclass
class SelfDogfoodInspection:
    job_id: str = ""
    repository_identity: str = ""
    generated_at: str = ""
    sources_checked: list[SelfImprovementSource] = field(default_factory=list)
    items: list[SelfImprovementItem] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    risks: list[SelfImprovementRisk] = field(default_factory=list)
    proposed_task_ids: list[str] = field(default_factory=list)
    next_safe_action: SelfImprovementAction | None = None
    evidence_status: str = "complete"
    safe_summary: str = ""


@dataclass
class SelfImprovementPlan:
    job_id: str = ""
    generated_at: str = ""
    groups: dict[str, list[str]] = field(default_factory=dict)   # item_type -> item_ids
    recommended: list[SelfImprovementItem] = field(default_factory=list)
    item_count: int = 0
    blockers: list[str] = field(default_factory=list)
    safe_summary: str = ""


@dataclass
class SelfDogfoodResult:
    job_id: str = ""
    proposed_task_ids: list[str] = field(default_factory=list)
    skipped_existing: list[str] = field(default_factory=list)
    stop_reason: str = "ok"
    next_safe_action: SelfImprovementAction | None = None
    evidence_status: str = "complete"
    safe_summary: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _scrub(text: str) -> str:
    from packages.orchestration.provider_trust import _scrub_public
    return _scrub_public(str(text))[:300]


def _fingerprint(item_type: str, key: str) -> str:
    return hashlib.sha256(f"{item_type}:{key}".encode()).hexdigest()[:12]


def _mk_item(item_type: str, priority: str, confidence: str, title: str, *,
             key: str, detail: str = "", source_type: str = "",
             evidence: list[SelfImprovementEvidence] | None = None,
             next_action: SelfImprovementAction | None = None) -> SelfImprovementItem:
    fp = _fingerprint(item_type, key)
    return SelfImprovementItem(
        item_id=fp, fingerprint=fp, item_type=item_type, priority=priority,
        confidence=confidence, title=_scrub(title), detail=_scrub(detail),
        source_type=source_type, evidence=evidence or [], next_action=next_action)


# ---------------------------------------------------------------------------
# Evidence source registry (Step 1401)
# ---------------------------------------------------------------------------


def _agent_dir() -> Path:
    return Path(os.environ.get("REMEDY_AGENT_DIR") or ".agent")


def _read_agent_file(name: str) -> tuple[str, str]:
    """Return (text, status). status: available|missing|malformed."""
    p = _agent_dir() / name
    if not p.exists():
        return "", SourceStatus.MISSING
    try:
        return p.read_text(encoding="utf-8", errors="replace"), SourceStatus.AVAILABLE
    except OSError:
        return "", SourceStatus.MALFORMED


# ---------------------------------------------------------------------------
# Live review parser reuse (Step 1402)
# ---------------------------------------------------------------------------


def _review_findings():
    """Reuse the safe live-review parser from the overnight executor."""
    from packages.orchestration.overnight_executor import parse_review_findings
    return parse_review_findings(_agent_dir() / "live_review.md")


# ---------------------------------------------------------------------------
# Detectors (Steps 1402-1406)
# ---------------------------------------------------------------------------


def _detect_review(items: list, blockers: list, risks: list) -> None:
    f = _review_findings()
    if f.source in ("unavailable", "malformed"):
        items.append(_mk_item(
            ItemType.EVIDENCE_GAP, Priority.MEDIUM, Confidence.HIGH,
            "Live review file missing or unreadable", key="live_review_missing",
            detail="No parseable .agent/live_review.md verdict.", source_type="live_review"))
        return
    if f.verdict in ("pending", "fail"):
        blockers.append("review_verdict_not_pass")
        risks.append(SelfImprovementRisk(
            id="review_verdict", severity=Priority.BLOCKER,
            summary=f"Live review verdict is {f.verdict}.", source="live_review"))
        items.append(_mk_item(
            ItemType.SAFETY_GAP, Priority.BLOCKER, Confidence.HIGH,
            f"Live review verdict is {f.verdict}", key=f"review_verdict_{f.verdict}",
            detail="Resolve the review before claiming merge-ready.", source_type="live_review"))
    if f.open_blocker_or_high > 0:
        blockers.append("open_blocker_or_high_findings")
        items.append(_mk_item(
            ItemType.SAFETY_GAP, Priority.BLOCKER, Confidence.HIGH,
            f"{f.open_blocker_or_high} open blocker/high review finding(s)",
            key="open_blocker_high", detail="Open blocker/high findings must be resolved.",
            source_type="live_review"))


def _detect_stale_handoff(items: list) -> None:
    plan_text, plan_status = _read_agent_file("plan.md")
    ctx_text, _ = _read_agent_file("context.md")
    lr_text, _ = _read_agent_file("live_review.md")
    if plan_status != SourceStatus.AVAILABLE:
        return
    current = ""
    m = re.search(r"^##\s*Current Step\s*\n(.+)$", plan_text, re.MULTILINE)
    if m:
        current = m.group(1).strip().lower()
    open_steps = len(re.findall(r"^- \[ \]", plan_text, re.MULTILINE))
    done_marked = "done" in current or "merge-ready" in current or "ready to merge" in current
    if done_marked and open_steps > 0:
        items.append(_mk_item(
            ItemType.CLEANUP, Priority.LOW, Confidence.MEDIUM,
            "Plan marked done but has open steps", key="plan_done_open_steps",
            detail=f"{open_steps} step(s) still unchecked while current step reads done.",
            source_type="plan"))
    # live_review claims merge-ready but no changed-files table / test count.
    low_lr = lr_text.lower()
    if "pass" in low_lr and "changed files" not in low_lr and "| file |" not in low_lr:
        items.append(_mk_item(
            ItemType.EVIDENCE_GAP, Priority.MEDIUM, Confidence.MEDIUM,
            "Handoff missing a changed-files table", key="missing_changed_files_table",
            detail="A PASS handoff should include a file | what changed | why table.",
            source_type="live_review"))
    if "pass" in low_lr and "passed" not in low_lr and "pytest" not in low_lr:
        items.append(_mk_item(
            ItemType.EVIDENCE_GAP, Priority.MEDIUM, Confidence.LOW,
            "Handoff missing a recorded test count", key="missing_test_count",
            detail="A PASS handoff should record the full pytest count.",
            source_type="live_review"))


def _detect_evidence_gaps(job: Any, items: list) -> None:
    if job is None:
        return
    job_id = str(job.id)
    # Failure artifact without a repair attempt; repair without pending intent.
    try:
        from packages.orchestration.repair_loop import load_repair_attempts
        attempts = list(load_repair_attempts(job).values())
        attempt_failures = {a.failure_artifact_id for a in attempts}
        failures = [a for a in job.artifacts if (a.metadata or {}).get("test_failure")
                    and not (a.metadata or {}).get("failure_resolved")]
        for fa in failures:
            if str(fa.id) not in attempt_failures:
                items.append(_mk_item(
                    ItemType.EVIDENCE_GAP, Priority.HIGH, Confidence.HIGH,
                    "Unresolved failure has no repair attempt", key=f"failure_no_repair_{fa.id}",
                    detail="A failure artifact exists with no repair proposal.",
                    source_type="repair_loop",
                    evidence=[SelfImprovementEvidence("failure_artifact", str(fa.id))],
                    next_action=SelfImprovementAction(
                        "Propose a repair", f"remedy repair propose {job_id} {fa.id} --json",
                        "Unresolved failure with no repair attempt.")))
        for a in attempts:
            if a.status == "approval_required" and not a.repair_intent_id:
                items.append(_mk_item(
                    ItemType.EVIDENCE_GAP, Priority.MEDIUM, Confidence.MEDIUM,
                    "Repair attempt without a pending intent", key=f"repair_no_intent_{a.attempt_id}",
                    detail="A repair attempt requires approval but has no patch intent.",
                    source_type="repair_loop"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass
    # Provider trust accepted but not materialized.
    try:
        from packages.orchestration.provider_trust import load_trust_reports
        for r in load_trust_reports(job).values():
            if r.get("trust_status") == "accepted" and not r.get("repair_intent_id"):
                items.append(_mk_item(
                    ItemType.EVIDENCE_GAP, Priority.MEDIUM, Confidence.MEDIUM,
                    "Accepted provider candidate not materialized",
                    key=f"trust_not_materialized_{r.get('report_id','')}",
                    detail="Accepted provider trust report produced no applyable intent.",
                    source_type="provider_trust"))
    except (ImportError, OSError, ValueError, KeyError, TypeError, AttributeError):
        pass


def _detect_roadmap(items: list) -> None:
    """Deterministic roadmap rules — cite the module file as evidence. Registry-only
    (module existence), no code scanning."""
    pkg = Path("packages/orchestration")

    def has(mod: str) -> bool:
        return (pkg / mod).exists()

    rules = [
        (has("provider_trust.py") and has("repair_request_builder.py"),
         "Provider Trust Verification v1", "provider_trust.py",
         "Trust gate + request builder exist; harden trust verification beyond regex."),
        (has("overnight_executor.py"),
         "Bounded Overnight Executor v1", "overnight_executor.py",
         "Single-cycle executor exists; consider a bounded multi-cycle v1 (still gated)."),
        (has("self_dogfood.py"),
         "Self-Dogfood Execution v0", "self_dogfood.py",
         "Self-dogfood planner exists; a guarded execution rail is the natural next step."),
        (has("ui_server.py"),
         "Operator Cockpit Mutations v0", "ui_server.py",
         "Read-only cockpit truth exists; consider gated cockpit mutations."),
        (has("provider_patch_material.py") and has("do_continue.py"),
         "Git Commit Gate v0", "do_continue.py",
         "Proof/test/snapshot/apply stable; a human-gated commit gate could follow."),
    ]
    for ok, title, ev, detail in rules:
        if ok:
            items.append(_mk_item(
                ItemType.ROADMAP_NEXT, Priority.LOW, Confidence.MEDIUM, title,
                key=f"roadmap_{title}", detail=detail, source_type="roadmap",
                evidence=[SelfImprovementEvidence("module", ev)]))


def _detect_quality_debt(items: list) -> None:
    """Registry-only quality checks (Step 1405). No arbitrary code scanning."""
    # Every -v0/-v1 doc referenced by another doc should exist (deterministic).
    docs = Path("docs")
    expected = ["self-dogfood-v0.md"]
    for d in expected:
        if docs.exists() and not (docs / d).exists():
            items.append(_mk_item(
                ItemType.DOCS_GAP, Priority.LOW, Confidence.MEDIUM,
                f"Missing documentation: {d}", key=f"docs_missing_{d}",
                detail="A public feature should have a docs page.", source_type="docs"))


# ---------------------------------------------------------------------------
# Inspection builder (Steps 1401-1407)
# ---------------------------------------------------------------------------


def _repository_identity() -> str:
    try:
        return Path.cwd().name
    except OSError:
        return "repository"


def build_self_dogfood_inspection(
    job_id: str | None = None, data_dir: Path | None = None, agent_dir: Path | None = None,
) -> SelfDogfoodInspection:
    """Inspect Remedy's own evidence and produce SelfImprovementItems. Read-only."""
    from packages.orchestration.data_paths import resolve_data_root

    if agent_dir is not None:
        os.environ["REMEDY_AGENT_DIR"] = str(agent_dir)
    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    insp = SelfDogfoodInspection(
        job_id=job_id or "", repository_identity=_repository_identity(), generated_at=_now())

    # Source registry.
    for name in ("live_review.md", "context.md", "plan.md"):
        _, status = _read_agent_file(name)
        insp.sources_checked.append(SelfImprovementSource(f".agent/{name}", status))

    job = None
    if job_id:
        try:
            from packages.orchestration.storage import JobNotFoundError, load_job
            job = load_job(UUID(job_id), ddir)
            insp.sources_checked.append(SelfImprovementSource("job", SourceStatus.AVAILABLE))
        except (ValueError, JobNotFoundError):
            insp.sources_checked.append(SelfImprovementSource("job", SourceStatus.MISSING))
            insp.evidence_status = "degraded"

    items: list[SelfImprovementItem] = []
    blockers: list[str] = []
    risks: list[SelfImprovementRisk] = []
    _detect_review(items, blockers, risks)
    _detect_stale_handoff(items)
    _detect_evidence_gaps(job, items)
    _detect_roadmap(items)
    _detect_quality_debt(items)

    # Dedupe by fingerprint.
    seen: set[str] = set()
    deduped: list[SelfImprovementItem] = []
    for it in items:
        if it.fingerprint in seen:
            continue
        seen.add(it.fingerprint)
        deduped.append(it)
    deduped.sort(key=lambda i: _PRIORITY_ORDER.get(i.priority, 9))

    insp.items = deduped
    insp.blockers = blockers
    insp.risks = risks
    top = deduped[0] if deduped else None
    if top is not None and top.next_action is not None:
        insp.next_safe_action = top.next_action
    elif job_id:
        insp.next_safe_action = SelfImprovementAction(
            "Plan self-improvement", f"remedy self plan --job-id {job_id} --json",
            "Review the self-improvement plan.")
    else:
        insp.next_safe_action = SelfImprovementAction(
            "Plan self-improvement", "remedy self plan --json", "Review the self-improvement plan.")
    insp.safe_summary = (
        f"Self-dogfood: {len(deduped)} item(s), {len(blockers)} blocker(s), "
        f"{len(risks)} risk(s).")
    return insp


# ---------------------------------------------------------------------------
# Plan builder (Step 1408)
# ---------------------------------------------------------------------------


def build_self_improvement_plan(
    job_id: str | None = None, data_dir: Path | None = None, agent_dir: Path | None = None,
) -> SelfImprovementPlan:
    insp = build_self_dogfood_inspection(job_id, data_dir, agent_dir)
    plan = SelfImprovementPlan(job_id=job_id or "", generated_at=_now(),
                               item_count=len(insp.items), blockers=insp.blockers)
    groups: dict[str, list[str]] = {}
    for it in insp.items:
        groups.setdefault(it.item_type, []).append(it.item_id)
    plan.groups = groups
    plan.recommended = insp.items[:3]
    plan.safe_summary = (
        f"Plan: {len(insp.items)} item(s) in {len(groups)} group(s); "
        f"top {len(plan.recommended)} recommended.")
    return plan


# ---------------------------------------------------------------------------
# Propose (Step 1411/1414) — metadata-only ProposedTasks via existing flow.
# ---------------------------------------------------------------------------

_SELF_DOGFOOD_PREFIX = "self_dogfood:"


def propose_self_improvement(
    job_id: str, item_ids: list[str] | None = None, top: int | None = None,
    data_dir: Path | None = None, agent_dir: Path | None = None,
) -> SelfDogfoodResult:
    """Create ProposedTask(s) from selected SelfImprovementItem(s). Metadata-only:
    enters the existing evaluate/approve/materialize flow. Never inserts Job.tasks,
    never approves, never executes. Idempotent by item fingerprint."""
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.proposed_tasks import (
        ProposedTask,
        ProposedTaskSource,
        add_proposed_task,
        load_proposed_tasks_safe,
    )
    from packages.orchestration.run_contract import (
        ContractAction,
        ensure_contract,
        evaluate_run_action,
    )
    from packages.orchestration.storage import JobNotFoundError, load_job

    ddir = Path(data_dir) if data_dir is not None else resolve_data_root()
    result = SelfDogfoodResult(job_id=job_id)

    try:
        load_job(UUID(job_id), ddir)
    except (ValueError, JobNotFoundError):
        result.stop_reason = "job_not_found"
        result.evidence_status = "unknown"
        result.safe_summary = "Job not found."
        result.next_safe_action = SelfImprovementAction("List jobs", "remedy job list --json", "")
        return result

    from packages.orchestration.storage import load_job as _lj
    job = _lj(UUID(job_id), ddir)
    contract = ensure_contract(job)
    if not evaluate_run_action(contract, ContractAction.SELF_PROPOSE_TASK).allowed:
        result.stop_reason = "contract_blocked"
        result.safe_summary = "Contract denies self-propose."
        result.next_safe_action = SelfImprovementAction(
            "Inspect contract", f"remedy contract inspect {job_id} --json", "")
        return result

    insp = build_self_dogfood_inspection(job_id, ddir, agent_dir)
    by_id = {it.item_id: it for it in insp.items}

    # Selection.
    selected: list[SelfImprovementItem]
    if item_ids:
        selected = [by_id[i] for i in item_ids if i in by_id]
    elif top is not None:
        selected = insp.items[:max(0, top)]
    else:
        high = [it for it in insp.items if it.priority in (Priority.BLOCKER, Priority.HIGH)]
        if len(high) > 1:
            result.stop_reason = "ambiguous_selection"
            result.safe_summary = (
                f"{len(high)} high-priority items — pass --item-id <id> or --top N.")
            result.next_safe_action = SelfImprovementAction(
                "Inspect items", f"remedy self inspect --job-id {job_id} --json", "")
            return result
        selected = high or insp.items[:1]

    if not selected:
        result.stop_reason = "no_items"
        result.safe_summary = "No self-improvement items to propose."
        result.next_safe_action = SelfImprovementAction(
            "Inspect", f"remedy self inspect --job-id {job_id} --json", "")
        return result

    existing, _ = load_proposed_tasks_safe(job_id, ddir)
    existing_recs = {t.origin_recommendation_id for t in existing}

    for it in selected:
        rec = _SELF_DOGFOOD_PREFIX + it.fingerprint
        if rec in existing_recs:
            result.skipped_existing.append(it.item_id)
            continue
        task = ProposedTask(
            title=it.title[:120], reason=f"self-dogfood {it.item_type}",
            description=it.detail[:500], source=ProposedTaskSource.ORCHESTRATOR,
            risk="low", priority=it.priority if it.priority in ("low", "medium", "high") else "medium",
            job_id=job_id, origin_recommendation_id=rec, task_type="self_dogfood",
        )
        add_proposed_task(job_id, task, ddir)
        result.proposed_task_ids.append(task.id)

    result.stop_reason = "ok"
    result.safe_summary = (
        f"Proposed {len(result.proposed_task_ids)} task(s); "
        f"skipped {len(result.skipped_existing)} existing.")
    if result.proposed_task_ids:
        result.next_safe_action = SelfImprovementAction(
            "Evaluate proposed tasks", f"remedy decision list {job_id} --json",
            "Self-proposed tasks await human evaluation/approval.")
    else:
        result.next_safe_action = SelfImprovementAction(
            "Inspect", f"remedy self inspect --job-id {job_id} --json", "")
    return result


# ---------------------------------------------------------------------------
# Report (Step 1419) + exports
# ---------------------------------------------------------------------------


def export_inspection_json(insp: SelfDogfoodInspection) -> dict[str, Any]:
    return {
        "version": 1, "job_id": insp.job_id, "repository_identity": insp.repository_identity,
        "generated_at": insp.generated_at,
        "sources_checked": [s.to_dict() for s in insp.sources_checked],
        "blockers": insp.blockers,
        "risks": [r.to_dict() for r in insp.risks],
        "item_count": len(insp.items),
        "items": [i.to_dict() for i in insp.items],
        "proposed_task_ids": insp.proposed_task_ids,
        "next_safe_action": insp.next_safe_action.to_dict() if insp.next_safe_action else None,
        "evidence_status": insp.evidence_status, "safe_summary": insp.safe_summary,
    }


def export_plan_json(plan: SelfImprovementPlan) -> dict[str, Any]:
    return {
        "version": 1, "job_id": plan.job_id, "generated_at": plan.generated_at,
        "item_count": plan.item_count, "groups": plan.groups, "blockers": plan.blockers,
        "recommended": [i.to_dict() for i in plan.recommended],
        "safe_summary": plan.safe_summary,
    }


def export_result_json(result: SelfDogfoodResult) -> dict[str, Any]:
    return {
        "version": 1, "job_id": result.job_id,
        "proposed_task_ids": result.proposed_task_ids,
        "skipped_existing": result.skipped_existing, "stop_reason": result.stop_reason,
        "next_safe_action": result.next_safe_action.to_dict() if result.next_safe_action else None,
        "evidence_status": result.evidence_status, "safe_summary": result.safe_summary,
    }


def build_self_dogfood_report(
    job_id: str | None = None, data_dir: Path | None = None, agent_dir: Path | None = None,
) -> dict[str, Any]:
    insp = build_self_dogfood_inspection(job_id, data_dir, agent_dir)
    return export_inspection_json(insp)


def render_report_markdown(data: dict[str, Any]) -> str:
    lines = [f"# Self-Dogfood Report — {data.get('repository_identity', '')}", ""]
    lines.append("## Summary")
    lines.append(data.get("safe_summary", ""))
    lines.append("")
    lines.append("## What Remedy thinks is wrong")
    for it in data.get("items", []):
        lines.append(f"- ({it['priority']}) [{it['item_type']}] {it['title']}")
    lines.append("")
    lines.append("## Why it thinks so (evidence)")
    for it in data.get("items", []):
        if it.get("detail"):
            lines.append(f"- {it['title']}: {it['detail']}")
    lines.append("")
    lines.append("## Evidence sources")
    for s in data.get("sources_checked", []):
        lines.append(f"- {s['name']}: {s['status']}")
    lines.append("")
    lines.append("## Suggested next tasks")
    for it in data.get("items", [])[:3]:
        na = it.get("next_action")
        if na:
            lines.append(f"- {it['title']} → `{na['command']}`")
        else:
            lines.append(f"- {it['title']}")
    lines.append("")
    lines.append("## Human decisions required")
    if data.get("blockers"):
        for b in data["blockers"]:
            lines.append(f"- {b}")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("## Not safe to automate yet")
    lines.append("- Self-apply, self-merge, and self-approval are NOT performed. "
                 "Self-proposed tasks require human evaluation/approval and the normal "
                 "materialize → do continue flow.")
    return "\n".join(lines)
