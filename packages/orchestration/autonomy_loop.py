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

    # Emit token_policy_applied once at loop start
    _emit_token_policy_applied(job, events)

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


def _emit_token_policy_applied(job: Job, events: list[dict[str, Any]]) -> None:
    """Emit token_policy_applied run-log event once at loop start."""
    try:
        from packages.orchestration.run_log import RunLogWriter
        from packages.orchestration.token_policy import build_default_token_policy
        from packages.orchestration.worker_recommend import recommend_worker

        tp = build_default_token_policy(job)
        rec = recommend_worker(job, events)
        log = RunLogWriter(job_id=job.id)
        log.log(
            "token_policy_applied",
            outcome="applied",
            mode=rec.token_mode,
            max_context_tokens=tp.budget.get("expensive_tokens", 100_000),
            estimated_context_tokens=rec.estimated_context_tokens,
            local_first=True,
            remote_model_requires_approval=rec.requires_approval,
            selected_worker=rec.recommended_worker,
        )
    except (ImportError, OSError):
        pass  # Non-critical — don't block loop


def _decide(
    job: Job,
    events: list[dict[str, Any]],
    autonomy_level: int,
    readiness_level: int,
    active_blockers: list,
    cycle_num: int,
) -> tuple[str, str, str, str]:
    """Return (decision, reason, next_action, blocked_by).

    Level semantics match autonomy_readiness.LEVELS:
      0 observe           — read-only inspection
      1 propose           — can generate plans/artifacts
      2 approved_apply    — can apply approved patches
      3 test_execution    — can run discovered test commands
      4 bounded_loop      — can run agent loop with max_cycles
      5 revert_capable    — can revert applied patches
      6 external_tools    — blocked (future)
      7 provider_autonomy — blocked (future)
    """
    from packages.orchestration.autonomy_readiness import LEVELS as _LEVELS  # noqa: F811

    # Level 0: observe only
    if autonomy_level == 0:
        return ("complete", "observe-only mode (level 0: observe)", "none", "")

    # Check if job is already complete
    if job.state == RunState.COMPLETED:
        return ("complete", "job already completed", "none", "")

    # Active blockers block progress
    if active_blockers:
        blocker_codes = ", ".join(b.reason_code for b in active_blockers[:3])
        return ("blocked", f"active blockers: {blocker_codes}",
                active_blockers[0].next_actions[0] if active_blockers[0].next_actions else "resolve blockers",
                blocker_codes)

    # Refuse if requested level exceeds readiness
    if autonomy_level > readiness_level:
        level_name = _LEVELS[min(autonomy_level, 7)]["name"] if autonomy_level <= 7 else "unknown"
        return ("blocked", f"readiness insufficient for level {autonomy_level} ({level_name})",
                "improve readiness signals", "readiness_insufficient")

    # Level 1: propose — can generate plans/artifacts
    if autonomy_level == 1:
        pending = [t for t in (job.tasks or []) if t.status == RunState.PENDING]
        if pending:
            return ("needs_approval", "pending tasks require approval (level 1: propose)",
                    "remedy job run-next <job_id>", "")
        return ("complete", "no pending tasks", "none", "")

    # Level 2: approved_apply — can apply approved patches
    if autonomy_level == 2:
        has_approved = any(
            e.get("event") == "patch_intent_approved"
            for e in events
        )
        if has_approved:
            return ("apply_approved", "approved intents ready for apply (level 2: approved_apply)",
                    "remedy patch apply <job_id> <intent_id>", "")
        pending = [t for t in (job.tasks or []) if t.status == RunState.PENDING]
        if pending:
            return ("needs_approval", "generated writes require approval before apply (level 2: approved_apply)",
                    "remedy patch approve <job_id> <intent_id>", "")
        return ("complete", "no pending tasks", "none", "")

    # Level 3: test_execution — can run discovered test commands
    if autonomy_level == 3:
        perms = (job.metadata or {}).get("permissions", {})
        if perms.get("repo_test_run") == "allow":
            return ("run_tests", "test execution allowed (level 3: test_execution)",
                    "remedy test run <job_id>", "")
        return ("blocked", "repo_test_run permission not granted (level 3: test_execution)",
                "remedy job permit <job_id> repo_test_run allow", "missing_permission")

    # Level 4: bounded_loop — can run agent loop with max_cycles
    if autonomy_level == 4:
        pending = [t for t in (job.tasks or []) if t.status == RunState.PENDING]
        if not pending:
            return ("complete", "no pending tasks (level 4: bounded_loop)", "none", "")
        return ("run_task", "bounded loop cycle (level 4: bounded_loop)",
                "remedy job run-next <job_id>", "")

    # Level 5: revert_capable — can revert applied patches
    if autonomy_level == 5:
        has_snapshot = any(e.get("event") == "snapshot_created" for e in events)
        if not has_snapshot:
            return ("blocked", "no snapshot for revert (level 5: revert_capable)",
                    "create snapshot before revert", "missing_snapshot")
        return ("complete", "revert capability confirmed (level 5: revert_capable)", "none", "")

    # Levels 6-7: blocked (future only)
    level_name = _LEVELS[min(autonomy_level, 7)]["name"] if autonomy_level <= 7 else "unknown"
    return ("blocked", f"level {autonomy_level} ({level_name}) not yet supported",
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
        lines.append("  Stop reasons:")
        for sr in result.stop_reasons:
            lines.append(f"    - {sr}")
    return "\n".join(lines)
