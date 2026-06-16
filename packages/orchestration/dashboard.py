"""
Project Dashboard v1 — one excellent overview command.

Derives all data from existing services. No new persistence layer.
No raw content, no diff, no stdout/stderr, no approval reason.

Public API::

    build_job_dashboard(job, events) -> dict
    build_project_dashboard(project_id, jobs, all_events) -> dict
    summarize_job_dashboard(data) -> str
"""

from __future__ import annotations

from typing import Any

from packages.core.models import Job, RunState


def build_job_dashboard(
    job: Job,
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a complete job dashboard. All derived, no persistence."""
    from packages.orchestration.autonomy_readiness import assess_job_readiness
    from packages.orchestration.decision_queue import build_decision_summary, list_decisions
    from packages.orchestration.event_ledger import build_event_summary
    from packages.orchestration.worker_recommend import recommend_worker

    job_id = str(job.id)

    # Readiness
    report = assess_job_readiness(job, events)

    # Decisions
    decisions = list_decisions(job, events)
    decision_summary = build_decision_summary(decisions)

    # Latest change
    apply_proofs = [e for e in events if e.get("event") == "patch_apply_proof_recorded"]
    latest_change: dict[str, Any] = {}
    if apply_proofs:
        last = apply_proofs[-1].get("metadata", {})
        latest_change = {
            "target_path": last.get("target_path", ""),
            "action": last.get("action", ""),
            "outcome": last.get("outcome", ""),
        }

    # Test status
    test_runs = [e for e in events if e.get("event") == "test_run_completed"]
    test_status: dict[str, Any] = {"run_count": len(test_runs)}
    if test_runs:
        last_test = test_runs[-1].get("metadata", {})
        test_status["last_status"] = last_test.get("status", "unknown")
        test_status["last_command"] = last_test.get("command", "")

    # Git status
    git_reads = [e for e in events if e.get("event") == "git_status_read"]
    git_status: dict[str, Any] = {}
    if git_reads:
        gm = git_reads[-1].get("metadata", {})
        git_status = {
            "branch": gm.get("branch", ""),
            "dirty": gm.get("dirty", True),
            "changed_file_count": gm.get("changed_file_count", 0),
        }

    # Token/worker
    rec = recommend_worker(job, events)

    # Memory
    mem_count = 0
    stale_count = 0
    try:
        from packages.memory.local_gateway import list_memory
        entries = list_memory()
        mem_count = len([e for e in entries if e.approved and e.validity == "active"])
        stale_count = len([e for e in entries if e.validity in ("stale", "needs_review")])
    except (ImportError, ValueError, OSError):
        pass

    # Events
    event_summary = build_event_summary(events)

    # Next actions
    next_actions: list[str] = []
    if decision_summary["high_count"] > 0:
        next_actions.append(f"remedy decision list {job_id[:8]}")
    pending = [t for t in job.tasks if t.status == RunState.PENDING]
    if pending:
        next_actions.append(f"remedy job run-next {job_id[:8]}")
    next_actions.append(f"remedy brain graph {job_id[:8]}")

    return {
        "version": 1,
        "scope": "job",
        "job_id": job_id,
        "readiness": {
            "level": report.highest_eligible_level,
            "missing_count": len(report.next_actions),
        },
        "decisions": decision_summary,
        "latest_change": latest_change,
        "test_status": test_status,
        "git_status": git_status,
        "token_policy": {
            "token_mode": rec.token_mode,
        },
        "worker_recommendation": {
            "recommended_worker": rec.recommended_worker,
        },
        "memory": {
            "active_count": mem_count,
            "stale_count": stale_count,
        },
        "events": {
            "event_count": event_summary.event_count,
            "failed_count": event_summary.failed_count,
        },
        "next_actions": next_actions,
    }


def build_project_dashboard(
    project_id: str,
    jobs: list[Job],
    all_events: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    """Build a project-level dashboard."""
    from packages.orchestration.decision_queue import list_decisions

    total_decisions = 0
    readiness_levels: list[int] = []
    for j in jobs:
        jid = str(j.id)
        jevents = all_events.get(jid, [])
        decisions = list_decisions(j, jevents)
        total_decisions += len([d for d in decisions if d.status == "open"])
        try:
            from packages.orchestration.autonomy_readiness import assess_job_readiness
            r = assess_job_readiness(j, jevents)
            readiness_levels.append(r.highest_eligible_level)
        except (ImportError, ValueError, OSError):
            readiness_levels.append(0)

    # Memory
    mem_count = 0
    try:
        from packages.memory.local_gateway import list_memory
        entries = list_memory()
        mem_count = len([e for e in entries if e.approved and e.validity == "active"])
    except (ImportError, ValueError, OSError):
        pass

    return {
        "version": 1,
        "scope": "project",
        "project_id": project_id,
        "job_count": len(jobs),
        "readiness_summary": {
            "min_level": min(readiness_levels) if readiness_levels else 0,
            "max_level": max(readiness_levels) if readiness_levels else 0,
        },
        "open_decision_count": total_decisions,
        "memory": {
            "active_count": mem_count,
        },
        "next_actions": ["remedy decision list <job_id>"] if total_decisions else [],
    }


def summarize_job_dashboard(data: dict[str, Any]) -> str:
    """Human-readable dashboard text."""
    lines = [
        f"Remedy Dashboard: {data['job_id'][:8]}",
        f"  Readiness: Level {data['readiness']['level']}",
    ]
    dec = data.get("decisions", {})
    lines.append(f"  Decisions: {dec.get('open_count', 0)} open "
                 f"({dec.get('high_count', 0)} blockers)")

    lc = data.get("latest_change", {})
    if lc:
        lines.append(f"  Last change: {lc.get('target_path', 'none')} ({lc.get('outcome', '')})")

    ts = data.get("test_status", {})
    if ts.get("run_count", 0):
        lines.append(f"  Tests: {ts['run_count']} runs, last={ts.get('last_status', '?')}")

    gs = data.get("git_status", {})
    if gs:
        dirty = "dirty" if gs.get("dirty") else "clean"
        lines.append(f"  Git: {gs.get('branch', '?')} ({dirty})")

    wr = data.get("worker_recommendation", {})
    lines.append(f"  Worker: {wr.get('recommended_worker', '?')}")

    mem = data.get("memory", {})
    lines.append(f"  Memory: {mem.get('active_count', 0)} active, {mem.get('stale_count', 0)} stale")

    ev = data.get("events", {})
    lines.append(f"  Events: {ev.get('event_count', 0)} total, {ev.get('failed_count', 0)} failed")

    na = data.get("next_actions", [])
    if na:
        lines.append("  Next:")
        for a in na[:3]:
            lines.append(f"    -> {a}")

    return "\n".join(lines)
