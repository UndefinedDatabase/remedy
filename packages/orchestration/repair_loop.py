"""
Repair Loop v0 — structured failure → fix task → optional fixture patch intent.

No real provider. No automatic apply. No test execution.
Stops before any risky action.

Public API::

    start_repair_loop_v0(job_id, failure_artifact_id, ...) -> RepairLoopResult
    export_repair_loop_json(result) -> dict
    summarize_repair_loop(result) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

from packages.orchestration.do_run import (
    DoRunNextAction,
    validate_next_safe_action_command,
)


# ---------------------------------------------------------------------------
# Result model (Step 946)
# ---------------------------------------------------------------------------


@dataclass
class RepairLoopResult:
    """Result of a repair loop v0 run."""

    version: int = 1
    job_id: str = ""
    failure_artifact_id: str = ""
    fix_task_id: str = ""
    repair_artifact_id: str = ""
    repair_patch_intent_id: str = ""
    stop_reason: str = ""
    stop_detail: str = ""
    next_safe_action: DoRunNextAction | None = None
    proof_status: str = "incomplete"
    phases: list[dict[str, str]] = field(default_factory=list)
    error: str = ""
    generated_at: str = ""


# ---------------------------------------------------------------------------
# Orchestrator (Step 946)
# ---------------------------------------------------------------------------


def start_repair_loop_v0(
    job_id: str,
    failure_artifact_id: str,
    *,
    create_patch_intent: bool = False,
) -> RepairLoopResult:
    """Run repair loop v0 — creates fix task, optionally fixture patch intent.

    No real provider. No apply. No test execution. Stops before risky action.
    """
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import load_job, save_job
    from packages.orchestration.test_failure_artifact import (
        TestFailureArtifact,
        create_fix_task_from_failure,
        emit_failure_events,
    )
    from packages.orchestration.timeline import append_run_event

    result = RepairLoopResult(
        job_id=job_id,
        failure_artifact_id=failure_artifact_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    data_dir = resolve_data_root()

    # --- Phase: load ---
    try:
        job = load_job(job_id)
    except Exception:
        result.stop_reason = "job_not_found"
        result.stop_detail = f"Job {job_id[:8]} not found"
        result.error = result.stop_detail
        result.phases.append({"phase": "load", "status": "failed", "safe_summary": result.stop_detail})
        return result

    result.phases.append({"phase": "load", "status": "completed", "safe_summary": f"Job {job_id[:8]} loaded"})

    # --- Contract enforcement (Step 1071: central contract) ---
    from packages.orchestration.run_contract import (
        ensure_contract,
        evaluate_run_action,
        load_usage,
        save_usage,
    )

    repair_contract = ensure_contract(job)
    save_job(job)  # persist contract if newly created

    fix_decision = evaluate_run_action(repair_contract, "create_fix_task")
    if not fix_decision.allowed:
        result.stop_reason = "contract_blocked"
        result.stop_detail = fix_decision.reason
        result.phases.append({"phase": "contract", "status": "blocked", "safe_summary": fix_decision.reason})
        return result

    if create_patch_intent:
        pi_decision = evaluate_run_action(repair_contract, "create_patch_intent")
        if not pi_decision.allowed:
            result.stop_reason = "contract_blocked"
            result.stop_detail = pi_decision.reason
            result.phases.append({"phase": "contract", "status": "blocked", "safe_summary": pi_decision.reason})
            return result

    result.phases.append({"phase": "contract", "status": "completed", "safe_summary": "Contract checks passed"})

    # --- Phase: validate failure artifact ---
    failure_art = None
    failure_meta = None
    for art in job.artifacts:
        if str(art.id) == failure_artifact_id and art.metadata.get("test_failure"):
            failure_art = art
            failure_meta = art.metadata
            break

    if not failure_art or not failure_meta:
        result.stop_reason = "failure_artifact_not_found"
        result.stop_detail = f"Failure artifact {failure_artifact_id[:8]} not found in job"
        result.error = result.stop_detail
        result.phases.append({"phase": "validate", "status": "failed", "safe_summary": result.stop_detail})
        return result

    result.phases.append({"phase": "validate", "status": "completed",
                          "safe_summary": f"Failure artifact validated: {failure_meta.get('failure_kind', 'unknown')}"})

    # Reconstruct minimal TestFailureArtifact from metadata
    failure = TestFailureArtifact(
        artifact_id=failure_artifact_id,
        job_id=job_id,
        task_id=failure_meta.get("related_task_id", ""),
        related_intent_id=failure_meta.get("related_intent_id", ""),
        related_apply_id=failure_meta.get("related_apply_id", ""),
        related_test_run_id=failure_meta.get("related_test_run_id", ""),
        failing_phase=failure_meta.get("failing_phase", "test"),
        command_safe=failure_meta.get("command_safe", ""),
        exit_code=failure_meta.get("exit_code"),
        safe_summary=failure_meta.get("safe_summary", ""),
        output_ref=failure_meta.get("output_ref", ""),
        failure_kind=failure_meta.get("failure_kind", "unknown"),
    )

    # --- Phase: create fix task ---
    # Check if fix task already exists for this failure
    existing_fix = None
    for task in job.tasks:
        if task.inputs.get("failure_artifact_id") == failure_artifact_id:
            existing_fix = task
            break

    if existing_fix:
        fix_task = existing_fix
        result.phases.append({"phase": "fix_task", "status": "completed",
                              "safe_summary": f"Fix task already exists: {str(fix_task.id)[:8]}"})
    else:
        fix_task = create_fix_task_from_failure(job, failure)
        result.phases.append({"phase": "fix_task", "status": "completed",
                              "safe_summary": f"Fix task created: {str(fix_task.id)[:8]}"})

    result.fix_task_id = str(fix_task.id)

    # --- Phase: optional fixture patch intent ---
    if create_patch_intent:
        from packages.core.models import Artifact, ArtifactKind
        from packages.orchestration.approval_queue import make_intent_id

        repair_art = Artifact(
            name=f"fixture-repair-{failure.artifact_id[:8]}",
            content=f"Fixture repair proposal for: {failure.safe_summary[:100]}",
            kind=ArtifactKind.BUILDER_PROPOSAL,
            task_id=fix_task.id,
            metadata={
                "fixture": True,
                "repair": True,
                "failure_artifact_id": failure_artifact_id,
                "safe_summary": f"Fixture repair for {failure.failure_kind}",
                "patch_intent_explanations": [
                    {
                        "file": "docs/REPAIR.md",
                        "action": "create",
                        "risk": "low",
                        "reason": f"Fixture repair proposal for {failure.failure_kind}",
                        "summary": f"Fixture repair for: {failure.safe_summary[:100]}",
                    },
                ],
                "patch_intent_approvals": {},
            },
        )
        job.artifacts.append(repair_art)
        save_job(job)

        intent_id = make_intent_id(repair_art.id, 0)
        result.repair_artifact_id = str(repair_art.id)
        result.repair_patch_intent_id = intent_id

        result.phases.append({"phase": "repair_intent", "status": "completed",
                              "safe_summary": f"Repair patch intent {intent_id} created"})
    else:
        result.phases.append({"phase": "repair_intent", "status": "skipped",
                              "safe_summary": "No patch intent requested"})

    # --- Phase: emit events (idempotent — skip if already emitted for this failure) ---
    from packages.orchestration.timeline import load_run_events
    existing_events = load_run_events(data_dir, UUID(job_id))
    already_emitted = any(
        e.get("event") == "test_failure_artifact_created"
        and e.get("artifact_id") == failure_artifact_id
        for e in existing_events
    )
    if not already_emitted:
        emit_failure_events(data_dir, UUID(job_id), failure, fix_task_id=str(fix_task.id))

    append_run_event(data_dir, UUID(job_id), event="repair_loop_stopped", metadata={
        "job_id": job_id,
        "fix_task_id": str(fix_task.id),
        "failure_artifact_id": failure_artifact_id,
        "stop_reason": "awaiting_approval" if create_patch_intent else "fix_task_created",
    })

    result.phases.append({"phase": "events", "status": "completed", "safe_summary": "Events emitted"})

    # Step 1077: Record usage
    usage = load_usage(job)
    usage.loops_used += 1
    save_usage(job, usage)

    append_run_event(data_dir, UUID(job_id), event="contract_decision", metadata={
        "action": "repair_loop_complete",
        "loops_used": usage.loops_used,
        "contract_id": repair_contract.contract_id,
    })

    save_job(job)

    # --- Stop ---
    if create_patch_intent and result.repair_patch_intent_id:
        from packages.orchestration.approval_queue import get_patch_intent
        reloaded = load_job(job_id)
        verified_intent = get_patch_intent(reloaded, result.repair_patch_intent_id)
        if verified_intent is not None:
            result.stop_reason = "approval_required"
            result.stop_detail = "Repair patch intent awaiting approval"
            result.next_safe_action = DoRunNextAction(
                label="Approve repair patch",
                command=f"remedy patch approve {job_id} {result.repair_patch_intent_id}",
                reason="Review and approve the repair patch intent.",
            )
        else:
            result.stop_reason = "intent_not_verified"
            result.stop_detail = "Repair intent created but not verifiable — skipping next_safe_action"
            result.repair_patch_intent_id = ""
            result.next_safe_action = DoRunNextAction(
                label="Show job",
                command=f"remedy job show {job_id} --json",
                reason="Review the fix task and failure artifact.",
            )
    else:
        result.stop_reason = "fix_task_created"
        result.stop_detail = "Fix task created from failure evidence"
        result.next_safe_action = DoRunNextAction(
            label="Show job",
            command=f"remedy job show {job_id} --json",
            reason="Review the fix task and failure artifact.",
        )

    result.phases.append({"phase": "stop", "status": "stopped",
                          "safe_summary": f"Stopped: {result.stop_reason}"})

    return result


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------


def export_repair_loop_json(result: RepairLoopResult) -> dict[str, Any]:
    """Export RepairLoopResult as safe JSON dict."""
    out: dict[str, Any] = {
        "version": result.version,
        "job_id": result.job_id,
        "failure_artifact_id": result.failure_artifact_id,
        "fix_task_id": result.fix_task_id,
        "repair_artifact_id": result.repair_artifact_id,
        "repair_patch_intent_id": result.repair_patch_intent_id,
        "stop_reason": result.stop_reason,
        "stop_detail": result.stop_detail,
        "proof_status": result.proof_status,
        "phases": result.phases,
        "generated_at": result.generated_at,
        "next_safe_action": None,
    }
    if result.next_safe_action:
        out["next_safe_action"] = {
            "label": result.next_safe_action.label,
            "command": result.next_safe_action.command,
            "reason": result.next_safe_action.reason,
        }
    if result.error:
        out["error"] = result.error
    return out


def summarize_repair_loop(result: RepairLoopResult) -> str:
    """Human-readable repair loop summary."""
    lines = [
        f"Repair Loop: {result.job_id[:8]}",
        f"Failure: {result.failure_artifact_id[:8] if result.failure_artifact_id else 'none'}",
    ]
    if result.fix_task_id:
        lines.append(f"Fix task: {result.fix_task_id[:8]}")

    lines.append("")
    lines.append("Phases:")
    for p in result.phases:
        lines.append(f"  [{p.get('status', '?')}] {p.get('phase', '?')}: {p.get('safe_summary', '')}")

    lines.append(f"\nStop: {result.stop_reason}")
    if result.stop_detail:
        lines.append(f"  {result.stop_detail}")

    if result.next_safe_action:
        lines.append(f"\nNext: {result.next_safe_action.label}")
        lines.append(f"  $ {result.next_safe_action.command}")

    return "\n".join(lines)
