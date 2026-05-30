"""
Limited Autonomy Loop v1 — contract-gated local autonomy.

No external tools, no provider execution beyond existing local path,
no MCP, no browser, no git writes. Each cycle returns a structured
decision. No auto-approval.

Public API::

    run_autonomy_loop(job, events, *, max_cycles, autonomy_level) -> LoopResult
    export_loop_result_json(result) -> dict
    summarize_loop_result(result) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job, RunState


@dataclass(frozen=True)
class CycleDecision:
    """One cycle's decision."""

    cycle: int
    decision: str
    reason: str
    next_action: str
    blocked_by: str
    token_mode: str
    selected_worker: str
    readiness_level: int


@dataclass(frozen=True)
class LoopResult:
    """Result of running the autonomy loop."""

    version: int
    job_id: str
    max_cycles: int
    autonomy_level: int
    cycles: tuple[CycleDecision, ...]
    final_decision: str
    stop_reasons: tuple[str, ...]


def run_autonomy_loop(
    job: Job,
    events: list[dict[str, Any]],
    *,
    max_cycles: int = 3,
    autonomy_level: int = 1,
) -> LoopResult:
    """Execute a limited autonomy loop. No auto-approval, no external providers."""
    from packages.orchestration.autonomy_readiness import assess_job_readiness
    from packages.orchestration.stop_reasons import derive_stop_reasons
    from packages.orchestration.worker_recommend import recommend_worker

    job_id = str(job.id)
    cycles: list[CycleDecision] = []
    stop_reason_summaries: list[str] = []

    for cycle_num in range(1, max_cycles + 1):
        # Assess readiness
        report = assess_job_readiness(job, events)
        readiness_level = report.highest_eligible_level

        # Get worker recommendation
        rec = recommend_worker(job, events)

        # Derive blockers
        blockers = derive_stop_reasons(job, events)
        active_blockers = [b for b in blockers if b.status == "active"]

        # Determine decision
        decision, reason, next_action, blocked_by = _decide(
            job, events, autonomy_level, readiness_level, active_blockers, cycle_num,
        )

        cycles.append(CycleDecision(
            cycle=cycle_num,
            decision=decision,
            reason=reason,
            next_action=next_action,
            blocked_by=blocked_by,
            token_mode=rec.token_mode,
            selected_worker=rec.recommended_worker,
            readiness_level=readiness_level,
        ))

        # Collect stop reasons
        for b in active_blockers:
            if b.safe_summary not in stop_reason_summaries:
                stop_reason_summaries.append(b.safe_summary)

        # Terminal decisions
        if decision in ("complete", "blocked", "stop_budget", "stop_no_progress"):
            break

    final = cycles[-1].decision if cycles else "blocked"

    return LoopResult(
        version=1,
        job_id=job_id,
        max_cycles=max_cycles,
        autonomy_level=autonomy_level,
        cycles=tuple(cycles),
        final_decision=final,
        stop_reasons=tuple(stop_reason_summaries),
    )


def _decide(
    job: Job,
    events: list[dict[str, Any]],
    autonomy_level: int,
    readiness_level: int,
    active_blockers: list,
    cycle_num: int,
) -> tuple[str, str, str, str]:
    """Return (decision, reason, next_action, blocked_by)."""

    # Level 0: observe only
    if autonomy_level == 0:
        return ("complete", "observe-only mode", "none", "")

    # Check if job is already complete
    if job.state == RunState.COMPLETED:
        return ("complete", "job already completed", "none", "")

    # Active blockers block progress
    if active_blockers:
        blocker_codes = ", ".join(b.reason_code for b in active_blockers[:3])
        return ("blocked", f"active blockers: {blocker_codes}",
                active_blockers[0].next_actions[0] if active_blockers[0].next_actions else "resolve blockers",
                blocker_codes)

    # Level 1: propose only
    if autonomy_level == 1:
        pending = [t for t in (job.tasks or []) if t.status == RunState.PENDING]
        if pending:
            return ("needs_approval", "pending tasks require approval",
                    "remedy job run-next <job_id>", "")
        return ("complete", "no pending tasks", "none", "")

    # Level 2: approve-required generated write
    if autonomy_level == 2:
        pending = [t for t in (job.tasks or []) if t.status == RunState.PENDING]
        if pending:
            return ("needs_approval", "generated writes require approval before apply",
                    "remedy patch approve <job_id> <intent_id>", "")
        return ("complete", "no pending tasks", "none", "")

    # Level 3: approved apply + proof
    if autonomy_level == 3:
        # Check for approved but unapplied intents
        has_approved = any(
            e.get("event") == "approval_decision"
            and e.get("outcome") == "approved"
            for e in events
        )
        if has_approved:
            return ("apply_approved", "approved intents ready for apply",
                    "remedy patch apply <job_id> <intent_id>", "")
        pending = [t for t in (job.tasks or []) if t.status == RunState.PENDING]
        if pending:
            return ("needs_approval", "tasks pending, no approved intents",
                    "approve pending intents", "")
        return ("complete", "all tasks resolved", "none", "")

    # Level 4: test execution
    if autonomy_level == 4:
        perms = (job.metadata or {}).get("permissions", {})
        if perms.get("repo_test_run"):
            return ("run_tests", "test execution allowed",
                    "remedy test run <job_id>", "")
        return ("blocked", "repo_test_run permission not granted",
                "grant repo_test_run permission", "missing_permission")

    # Level 5: revert capable
    if autonomy_level == 5:
        has_snapshot = any(e.get("event") == "snapshot_created" for e in events)
        if not has_snapshot:
            return ("blocked", "no snapshot for revert",
                    "create snapshot before revert", "missing_snapshot")
        return ("complete", "revert capability confirmed", "none", "")

    # Level 6: limited loop with cycle cap
    if autonomy_level == 6:
        pending = [t for t in (job.tasks or []) if t.status == RunState.PENDING]
        if not pending:
            return ("complete", "no pending tasks", "none", "")
        return ("run_task", "limited loop cycle",
                "remedy job run-next <job_id>", "")

    # Level 7+: future / blocked
    return ("blocked", "autonomy level not yet supported",
            "reduce autonomy level", "unsupported_level")


def export_loop_result_json(result: LoopResult) -> dict[str, Any]:
    """Export as safe JSON dict."""
    return {
        "version": result.version,
        "job_id": result.job_id,
        "max_cycles": result.max_cycles,
        "autonomy_level": result.autonomy_level,
        "cycles": [
            {
                "cycle": c.cycle,
                "decision": c.decision,
                "reason": c.reason,
                "next_action": c.next_action,
                "blocked_by": c.blocked_by,
                "token_mode": c.token_mode,
                "selected_worker": c.selected_worker,
                "readiness_level": c.readiness_level,
            }
            for c in result.cycles
        ],
        "final_decision": result.final_decision,
        "stop_reasons": list(result.stop_reasons),
    }


def summarize_loop_result(result: LoopResult) -> str:
    """Human-readable summary."""
    lines = [
        f"Autonomy Loop: {result.job_id[:8]}",
        f"  Level: {result.autonomy_level}  Max cycles: {result.max_cycles}",
        f"  Cycles run: {len(result.cycles)}",
        f"  Final: {result.final_decision}",
    ]
    for c in result.cycles:
        lines.append(f"  Cycle {c.cycle}: {c.decision} — {c.reason}")
    if result.stop_reasons:
        lines.append(f"  Stop reasons:")
        for sr in result.stop_reasons:
            lines.append(f"    - {sr}")
    return "\n".join(lines)
