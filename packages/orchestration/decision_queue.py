"""
Human Decision Queue v1 — one safe surface for everything needing human attention.

Derives decisions from existing records: patch intents, stop reasons,
readiness, memory cards, repo status, worker recommendation, test runs.
Not a second source of truth — a read-only aggregation.

Public API::

    HumanDecision — frozen dataclass
    list_decisions(job, events) -> list[HumanDecision]
    get_decision(job, events, decision_id) -> HumanDecision | None
    explain_decisions(job, events) -> str
    export_decision_json(d) -> dict
    build_decision_summary(decisions) -> dict  (brain node metadata)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job


@dataclass(frozen=True)
class HumanDecision:
    """A single item requiring human attention."""

    id: str
    type: str  # patch_approval, stop_reason, test_failure, repo_dirty, ...
    status: str  # open, resolved
    severity: str  # info, warning, blocker
    source: str
    related_node_id: str
    related_intent_id: str
    related_file: str
    safe_summary: str
    next_actions: tuple[str, ...]
    created_at: str
    resolved_at: str | None


DECISION_TYPES = frozenset({
    "patch_approval", "stop_reason", "test_failure", "repo_dirty",
    "token_budget", "worker_approval", "memory_review", "revert_missing",
})


def list_decisions(
    job: Job,
    events: list[dict[str, Any]],
) -> list[HumanDecision]:
    """Derive all pending human decisions from existing state."""
    decisions: list[HumanDecision] = []
    job_id = str(job.id)

    # 1. Pending patch approvals
    try:
        from packages.orchestration.approval_queue import APPROVAL_PENDING, list_patch_intents
        intents = list_patch_intents(job)
        for pi in intents:
            if pi.get("state") == APPROVAL_PENDING:
                decisions.append(HumanDecision(
                    id=f"pa:{pi['intent_id']}",
                    type="patch_approval",
                    status="open",
                    severity="blocker",
                    source="approval_queue",
                    related_node_id=f"pi:{pi['intent_id']}",
                    related_intent_id=pi["intent_id"],
                    related_file=pi.get("target_path", ""),
                    safe_summary=f"Patch intent for {pi.get('target_path', '?')} awaits approval.",
                    next_actions=(
                        f"remedy patch approve {job_id[:8]} {pi['intent_id']}",
                        f"remedy patch reject {job_id[:8]} {pi['intent_id']}",
                    ),
                    created_at=pi.get("created_at", ""),
                    resolved_at=None,
                ))
    except (ImportError, ValueError, OSError):
        pass

    # 2. Stop reasons / blockers
    try:
        from packages.orchestration.stop_reasons import derive_stop_reasons
        stops = derive_stop_reasons(job, events)
        for sr in stops:
            if sr.status == "active":
                decisions.append(HumanDecision(
                    id=f"sr:{sr.id}",
                    type="stop_reason",
                    status="open",
                    severity=sr.severity,
                    source=sr.source,
                    related_node_id=sr.related_node_id,
                    related_intent_id=sr.related_intent_id,
                    related_file=sr.related_file,
                    safe_summary=sr.safe_summary,
                    next_actions=sr.next_actions,
                    created_at=sr.created_at,
                    resolved_at=None,
                ))
    except (ImportError, ValueError, OSError):
        pass

    # 3. Test failures
    test_fails = [e for e in events
                  if e.get("event") == "test_run_completed"
                  and e.get("metadata", {}).get("status") == "failed"]
    for tf in test_fails[-3:]:
        meta = tf.get("metadata", {})
        cmd = str(meta.get("command", "?"))
        decisions.append(HumanDecision(
            id=f"tf:{meta.get('test_run_id', 'unknown')[:8]}",
            type="test_failure",
            status="open",
            severity="blocker",
            source="test_run",
            related_node_id="",
            related_intent_id="",
            related_file="",
            safe_summary=f"Test '{cmd}' failed.",
            next_actions=("Review test output.", f"remedy test run {job_id[:8]}"),
            created_at=str(tf.get("timestamp", "")),
            resolved_at=None,
        ))

    # 4. Dirty repo
    git_reads = [e for e in events if e.get("event") == "git_status_read"]
    if git_reads:
        last = git_reads[-1].get("metadata", {})
        if last.get("dirty"):
            decisions.append(HumanDecision(
                id="dirty_repo",
                type="repo_dirty",
                status="open",
                severity="warning",
                source="git_status",
                related_node_id="",
                related_intent_id="",
                related_file="",
                safe_summary="Target repository has uncommitted changes.",
                next_actions=("Commit or stash changes in target repo.",),
                created_at=str(git_reads[-1].get("timestamp", "")),
                resolved_at=None,
            ))

    # 5. Budget exhaustion
    budget_error = str(
        job.metadata.get("budget_stop_reason", "")
        or job.metadata.get("error", "")
        or getattr(job, "error", "")
        or ""
    )
    if "budget_exhausted" in budget_error:
        decisions.append(HumanDecision(
            id="budget_exhausted",
            type="token_budget",
            status="open",
            severity="blocker",
            source="budget_guard",
            related_node_id="",
            related_intent_id="",
            related_file="",
            safe_summary=f"Job stopped: {budget_error[:200]}",
            next_actions=(
                "Increase budget limits and re-run.",
                f"remedy job budget {job_id[:8]}",
            ),
            created_at="",
            resolved_at=None,
        ))

    # 6. Stale/needs_review memory cards
    try:
        from packages.memory.local_gateway import list_memory
        entries = list_memory()
        stale = [e for e in entries if e.validity in ("stale", "needs_review")]
        for me in stale[:5]:
            decisions.append(HumanDecision(
                id=f"mem:{me.key}",
                type="memory_review",
                status="open",
                severity="info",
                source="memory",
                related_node_id="",
                related_intent_id="",
                related_file="",
                safe_summary=f"Memory '{me.key}' is {me.validity}.",
                next_actions=(f"remedy memory card-show {me.key}",),
                created_at="",
                resolved_at=None,
            ))
    except (ImportError, ValueError, OSError):
        pass

    return decisions


def get_decision(
    job: Job,
    events: list[dict[str, Any]],
    decision_id: str,
) -> HumanDecision | None:
    """Find a specific decision by ID."""
    for d in list_decisions(job, events):
        if d.id == decision_id:
            return d
    return None


def explain_decisions(job: Job, events: list[dict[str, Any]]) -> str:
    """Human-readable explanation of all pending decisions."""
    decisions = list_decisions(job, events)
    if not decisions:
        return f"No pending decisions for job {str(job.id)[:8]}."

    lines = [f"Human Decision Queue for {str(job.id)[:8]} ({len(decisions)} items)"]
    by_sev = {"blocker": 0, "warning": 0, "info": 0}
    for d in decisions:
        by_sev[d.severity] = by_sev.get(d.severity, 0) + 1
        status_mark = "[open]" if d.status == "open" else "[resolved]"
        lines.append(f"  {d.type} {status_mark} ({d.severity}): {d.safe_summary}")
        for a in d.next_actions[:2]:
            lines.append(f"    -> {a}")

    lines.append(f"\nSummary: {by_sev.get('blocker', 0)} blockers, "
                 f"{by_sev.get('warning', 0)} warnings, {by_sev.get('info', 0)} info")
    return "\n".join(lines)


def export_decision_json(d: HumanDecision) -> dict[str, Any]:
    """Export as safe JSON dict."""
    return {
        "id": d.id,
        "type": d.type,
        "status": d.status,
        "severity": d.severity,
        "source": d.source,
        "related_node_id": d.related_node_id,
        "related_intent_id": d.related_intent_id,
        "related_file": d.related_file,
        "safe_summary": d.safe_summary,
        "next_actions": list(d.next_actions),
        "created_at": d.created_at,
        "resolved_at": d.resolved_at,
    }


def build_decision_summary(decisions: list[HumanDecision]) -> dict[str, Any]:
    """Build safe metadata for brain node."""
    open_decisions = [d for d in decisions if d.status == "open"]
    by_sev = {"blocker": 0, "warning": 0, "info": 0}
    for d in open_decisions:
        by_sev[d.severity] = by_sev.get(d.severity, 0) + 1
    total_next = sum(len(d.next_actions) for d in open_decisions)
    return {
        "open_count": len(open_decisions),
        "high_count": by_sev.get("blocker", 0),
        "medium_count": by_sev.get("warning", 0),
        "low_count": by_sev.get("info", 0),
        "next_action_count": total_next,
    }
