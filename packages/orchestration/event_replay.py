"""
Event Replay v1 — safe read model from run-log events.

Reconstructs job progress from safe metadata only.
No raw prompts, provider output, file content, diffs, or stdout/stderr.

Public API::

    replay_job(job_id, data_dir) -> JobReplayState
    find_checkpoints(replay) -> list[JobCheckpoint]
    resume_dry_run(job, checkpoint_id, data_dir) -> ResumeDryRun
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID


@dataclass
class ReplayStage:
    """One stage in the replay timeline."""
    id: str
    label: str
    reached: bool
    event_id: str = ""
    event_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class JobReplayState:
    """Safe read model reconstructed from events."""
    version: int = 1
    job_id: str = ""
    generated_at: str = ""
    event_count: int = 0
    last_event_id: str = ""
    last_event_at: str = ""
    current_stage: str = "unknown"
    stop_reason: str = ""
    provider: str = ""
    stages: list[ReplayStage] = field(default_factory=list)
    structured_patch: dict[str, Any] = field(default_factory=dict)
    approval: dict[str, Any] = field(default_factory=dict)
    source_apply: dict[str, Any] = field(default_factory=dict)
    tests: dict[str, Any] = field(default_factory=dict)
    repair: dict[str, Any] = field(default_factory=dict)
    memory: dict[str, Any] = field(default_factory=dict)
    source_context: dict[str, Any] = field(default_factory=dict)
    degraded: bool = False
    degraded_reason: str = ""
    redaction: str = "safe_metadata_only"


@dataclass
class JobCheckpoint:
    """A resume-safe boundary in the job timeline."""
    id: str
    job_id: str
    kind: str
    label: str
    status: str = "available"
    safe_to_resume: bool = False
    resume_mode: str = ""
    event_id: str = ""
    event_at: str = ""
    reason: str = ""
    blocked_reason: str = ""
    required_capabilities: list[str] = field(default_factory=list)
    required_approvals: list[str] = field(default_factory=list)
    related_intent_id: str = ""
    related_task_id: str = ""
    next_command: str = ""


@dataclass
class ResumeDryRun:
    """Result of a resume dry-run — preview without mutation."""
    job_id: str = ""
    checkpoint_id: str = ""
    checkpoint_kind: str = ""
    can_resume: bool = False
    would_run_stage: str = ""
    required_capabilities: list[str] = field(default_factory=list)
    required_approvals: list[str] = field(default_factory=list)
    blocked_reason: str = ""
    next_command: str = ""
    safety_summary: str = ""
    redaction: str = "safe_metadata_only"


_STAGE_ORDER = [
    "job_created", "planning_started", "planning_completed",
    "source_context_injected", "memory_context_attached",
    "builder_started", "structured_patch_attempted", "structured_patch_created",
    "approval_required", "approval_recorded",
    "source_patch_applied", "test_run_completed",
    "repair_cycle_started", "repair_cycle_completed",
    "proof_collected", "stopped",
]

_EVENT_TO_STAGE = {
    "autorun_started": "job_created",
    "source_context_injected": "source_context_injected",
    "project_memory_recalled": "memory_context_attached",
    "autorun_builder_completed": "builder_started",
    "builder_patch_parsed": "structured_patch_attempted",
    "structured_patch_intent_created": "structured_patch_created",
    "builder_bridge_intent_approved": "approval_recorded",
    "patch_intent_applied": "source_patch_applied",
    "test_run_completed": "test_run_completed",
    "builder_bridge_test_completed": "test_run_completed",
    "repair_loop_cycle_started": "repair_cycle_started",
    "repair_loop_succeeded": "repair_cycle_completed",
    "repair_loop_stopped": "stopped",
    "proof_collected": "proof_collected",
    "autorun_provider_error": "stopped",
}


def replay_job(job_id: str | UUID, data_dir: str | Path) -> JobReplayState:
    """Reconstruct job progress from event ledger. Safe metadata only."""
    from packages.orchestration.timeline import load_run_events

    data_path = Path(data_dir)
    jid = str(job_id)
    events = load_run_events(data_path, jid)

    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state = JobReplayState(job_id=jid, generated_at=now, event_count=len(events))

    if not events:
        state.degraded = True
        state.degraded_reason = "no_events"
        state.current_stage = "unknown"
        return state

    state.last_event_at = events[-1].get("timestamp", "")
    state.last_event_id = f"evt-{len(events)}"

    reached: set[str] = set()
    for e in events:
        ev = e.get("event", "")
        meta = e.get("metadata", {})
        stage = _EVENT_TO_STAGE.get(ev)
        if stage:
            reached.add(stage)

        if ev == "autorun_builder_completed":
            state.provider = meta.get("provider", "")
        if ev == "builder_patch_parsed":
            state.structured_patch = {
                "attempted": True,
                "parse_success": meta.get("parse_success", False),
                "error_kind": meta.get("error_kind", ""),
                "output_hash": meta.get("output_hash", "")[:16],
            }
        if ev == "builder_bridge_intent_approved":
            state.approval = {
                "status": "approved",
                "intent_id": meta.get("intent_id", ""),
            }
        if ev == "structured_patch_intent_created":
            if "status" not in state.approval:
                state.approval = {"status": "pending"}
        if ev == "patch_intent_applied":
            state.source_apply = {"status": "applied"}
        if ev in ("test_run_completed", "builder_bridge_test_completed"):
            passed = meta.get("passed", meta.get("exit_code") == 0)
            state.tests = {"status": "pass" if passed else "fail", "passed": passed}
        if ev == "repair_loop_cycle_started":
            state.repair = {
                "used": True,
                "cycle": meta.get("cycle", 0),
                "max_cycles": meta.get("max_cycles", 0),
            }
        if ev == "source_context_injected":
            state.source_context = {
                "injected": True,
                "file_count": meta.get("file_count", 0),
                "estimated_tokens": meta.get("estimated_tokens", 0),
            }
        if ev == "project_memory_recalled":
            state.memory = {
                "used": True,
                "item_count": meta.get("item_count", 0),
            }
        if ev == "autorun_provider_error":
            state.stop_reason = meta.get("stop_reason", "provider_unavailable")
        if ev == "repair_loop_stopped":
            state.stop_reason = meta.get("reason", "")
        if ev == "builder_patch_parsed" and not meta.get("parse_success"):
            state.stop_reason = meta.get("stop_reason", "") or meta.get("error_kind", "")

    # Build stages list
    for sid in _STAGE_ORDER:
        state.stages.append(ReplayStage(
            id=sid,
            label=sid.replace("_", " ").capitalize(),
            reached=sid in reached,
        ))

    # Determine current stage
    for sid in reversed(_STAGE_ORDER):
        if sid in reached:
            state.current_stage = sid
            break

    return state


def find_checkpoints(replay: JobReplayState) -> list[JobCheckpoint]:
    """Identify resume boundaries from replay state.

    Only marks safe_to_resume=True when:
    1. An actual resume implementation exists for this mode, AND
    2. Required data (intent, patch, permission, repo) is available.
    """
    checkpoints: list[JobCheckpoint] = []
    jid = replay.job_id

    reached_ids = {s.id for s in replay.stages if s.reached}

    # context_ready — inspectable but no builder resume path exists yet
    if "source_context_injected" in reached_ids:
        checkpoints.append(JobCheckpoint(
            id=f"{jid}-ctx", job_id=jid, kind="context_ready",
            label="Source context ready",
            status="inspectable",
            safe_to_resume=False, resume_mode="from_context",
            blocked_reason="resume_mode_not_implemented",
            next_command=f"remedy event replay {jid} --json",
        ))

    # patch_intent_created — needs approval first
    if "structured_patch_created" in reached_ids or replay.approval.get("status") == "pending":
        checkpoints.append(JobCheckpoint(
            id=f"{jid}-intent", job_id=jid, kind="patch_intent_created",
            label="Patch intent created",
            status="blocked",
            safe_to_resume=False,
            resume_mode="from_intent",
            blocked_reason="approval_pending",
            required_approvals=["patch_intent"],
            next_command=f"remedy patch show {jid} {replay.approval.get('intent_id', '<intent_id>')}",
        ))

    # approval_recorded — patch approved but StructuredPatch not persisted on job
    if replay.approval.get("status") == "approved":
        checkpoints.append(JobCheckpoint(
            id=f"{jid}-approved", job_id=jid, kind="approval_recorded",
            label="Patch approved",
            status="blocked",
            safe_to_resume=False,
            resume_mode="from_approval",
            blocked_reason="missing_patch_payload",
            required_capabilities=["repo_generated_write"],
            related_intent_id=replay.approval.get("intent_id", ""),
            next_command=f"remedy event replay {jid} --json",
        ))

    # source_apply_proven — patch already applied, can resume to tests
    if "source_patch_applied" in reached_ids:
        checkpoints.append(JobCheckpoint(
            id=f"{jid}-applied", job_id=jid, kind="source_apply_proven",
            label="Patch applied — resume to tests",
            status="available",
            safe_to_resume=True, resume_mode="from_apply",
            required_capabilities=["repo_test_run"],
            next_command=f"remedy job resume {jid} --checkpoint {jid}-applied --json",
        ))

    # tests_failed — repair resume not implemented in v1
    if replay.tests.get("status") == "fail":
        checkpoints.append(JobCheckpoint(
            id=f"{jid}-testfail", job_id=jid, kind="tests_failed",
            label="Tests failed",
            status="blocked",
            safe_to_resume=False, resume_mode="from_test_failure",
            blocked_reason="resume_mode_not_implemented",
            next_command=f"remedy job summary {jid} --json",
        ))

    # tests_passed — complete, nothing to resume
    if replay.tests.get("status") == "pass":
        checkpoints.append(JobCheckpoint(
            id=f"{jid}-pass", job_id=jid, kind="tests_passed",
            label="Tests passed",
            status="complete",
            safe_to_resume=False, resume_mode="complete",
            reason="Job completed successfully",
            next_command=f"remedy job summary {jid} --json",
        ))

    # stopped — not resumable
    if replay.stop_reason and replay.stop_reason not in ("", "test_failed_after_apply"):
        checkpoints.append(JobCheckpoint(
            id=f"{jid}-stopped", job_id=jid, kind="stopped",
            label=f"Stopped: {replay.stop_reason}",
            status="blocked",
            safe_to_resume=False,
            blocked_reason=replay.stop_reason,
        ))

    return checkpoints


def resume_dry_run(
    job: Any,
    checkpoint_id: str,
    data_dir: str | Path,
) -> ResumeDryRun:
    """Preview resume without mutation."""
    replay = replay_job(str(job.id), data_dir)
    checkpoints = find_checkpoints(replay)

    cp = next((c for c in checkpoints if c.id == checkpoint_id), None)
    if not cp:
        return ResumeDryRun(
            job_id=str(job.id), checkpoint_id=checkpoint_id,
            can_resume=False, blocked_reason="checkpoint_not_found",
            safety_summary="No matching checkpoint found in event history.",
        )

    if not cp.safe_to_resume:
        return ResumeDryRun(
            job_id=str(job.id), checkpoint_id=checkpoint_id,
            checkpoint_kind=cp.kind, can_resume=False,
            blocked_reason=cp.blocked_reason or "not_resumable",
            safety_summary=f"Checkpoint '{cp.kind}' is not safe to resume: {cp.blocked_reason}",
        )

    stage_map = {
        "from_approval": "source_apply",
        "from_apply": "test_run",
        "from_test_failure": "repair_loop",
        "from_context": "builder",
    }

    return ResumeDryRun(
        job_id=str(job.id), checkpoint_id=checkpoint_id,
        checkpoint_kind=cp.kind, can_resume=True,
        would_run_stage=stage_map.get(cp.resume_mode, "unknown"),
        required_capabilities=cp.required_capabilities,
        required_approvals=cp.required_approvals,
        next_command=cp.next_command,
        safety_summary=f"Would continue from '{cp.kind}' into {stage_map.get(cp.resume_mode, 'next stage')}.",
    )


def export_replay_json(replay: JobReplayState) -> dict[str, Any]:
    """Safe JSON export of replay state."""
    return {
        "version": replay.version,
        "job_id": replay.job_id,
        "generated_at": replay.generated_at,
        "event_count": replay.event_count,
        "last_event_id": replay.last_event_id,
        "last_event_at": replay.last_event_at,
        "current_stage": replay.current_stage,
        "stop_reason": replay.stop_reason,
        "provider": replay.provider,
        "stages": [
            {"id": s.id, "label": s.label, "reached": s.reached}
            for s in replay.stages
        ],
        "structured_patch": replay.structured_patch,
        "approval": replay.approval,
        "source_apply": replay.source_apply,
        "tests": replay.tests,
        "repair": replay.repair,
        "memory": replay.memory,
        "source_context": replay.source_context,
        "degraded": replay.degraded,
        "degraded_reason": replay.degraded_reason,
        "redaction": replay.redaction,
    }


def export_checkpoints_json(checkpoints: list[JobCheckpoint]) -> list[dict[str, Any]]:
    """Safe JSON export of checkpoints."""
    return [
        {
            "id": c.id,
            "job_id": c.job_id,
            "kind": c.kind,
            "label": c.label,
            "status": c.status,
            "safe_to_resume": c.safe_to_resume,
            "resume_mode": c.resume_mode,
            "blocked_reason": c.blocked_reason,
            "required_capabilities": c.required_capabilities,
            "required_approvals": c.required_approvals,
            "related_intent_id": c.related_intent_id,
            "next_command": c.next_command,
        }
        for c in checkpoints
    ]


def export_dry_run_json(dr: ResumeDryRun) -> dict[str, Any]:
    """Safe JSON export of dry-run result."""
    return {
        "job_id": dr.job_id,
        "checkpoint_id": dr.checkpoint_id,
        "checkpoint_kind": dr.checkpoint_kind,
        "can_resume": dr.can_resume,
        "would_run_stage": dr.would_run_stage,
        "required_capabilities": dr.required_capabilities,
        "required_approvals": dr.required_approvals,
        "blocked_reason": dr.blocked_reason,
        "next_command": dr.next_command,
        "safety_summary": dr.safety_summary,
        "redaction": dr.redaction,
    }
