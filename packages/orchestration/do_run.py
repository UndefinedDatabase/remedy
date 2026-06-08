"""
remedy do v1 — cohesive phased flow.

Runs a goal-driven sequence: init -> plan -> context -> build ->
patch_intent -> approval_required -> stop.

Fixture only in v1: no real LLM, no Ollama.
Stops before apply by default.
No raw content in output.

Public API::

    run_do(goal, repo_path, ...) -> DoRunResult
    export_do_run_json(result) -> dict
    summarize_do_run(result) -> str
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4


# ---------------------------------------------------------------------------
# Phase model (Step 906)
# ---------------------------------------------------------------------------

DO_PHASES = (
    "init", "plan", "context", "build",
    "patch_intent", "approval_required",
    "apply", "test", "proof", "stop",
)


@dataclass(frozen=True)
class DoRunPhase:
    """One phase in the do run."""

    phase: str
    status: str  # completed, skipped, blocked, stopped
    safe_summary: str
    event_id: str = ""
    next_safe_action: str = ""


@dataclass(frozen=True)
class DoRunStopReason:
    """Why the run stopped."""

    reason: str  # approval_required, context_blocked, build_complete, max_loops, error
    detail: str = ""


@dataclass(frozen=True)
class DoRunNextAction:
    """What the user should do next."""

    label: str
    command: str
    reason: str


# ---------------------------------------------------------------------------
# Result contract (Step 907)
# ---------------------------------------------------------------------------


@dataclass
class DoRunResult:
    """Full result of a remedy do run."""

    version: int = 1
    job_id: str = ""
    task_id: str = ""
    artifact_ids: list[str] = field(default_factory=list)
    patch_intent_id: str = ""
    proof_status: str = ""
    phases: list[DoRunPhase] = field(default_factory=list)
    stop_reason: DoRunStopReason = field(default_factory=lambda: DoRunStopReason(reason="unknown"))
    next_safe_action: DoRunNextAction | None = None
    autonomy_level: int = 2
    repo_path_safe: str = ""
    context_summary: str = ""
    generated_at: str = ""
    error: str = ""


# ---------------------------------------------------------------------------
# Run contract (Step 917)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DoRunContract:
    """Constraints for a do run."""

    autonomy_level: int = 2
    stop_before_apply: bool = True
    max_loops: int = 1


# ---------------------------------------------------------------------------
# Flow execution (Steps 909-915)
# ---------------------------------------------------------------------------


def run_do(
    goal: str,
    repo_path: str,
    *,
    autonomy_level: int = 2,
    max_loops: int = 1,
    stop_before_apply: bool = True,
) -> DoRunResult:
    """Run remedy do v1 — fixture only, phased, safe.

    Args:
        goal: User prompt / goal.
        repo_path: Path to target repo.
        autonomy_level: 0-7, capped at 3 for v1.
        max_loops: Max loops (1 for v1).
        stop_before_apply: Stop before apply (default True).
    """
    from packages.core.models import Artifact, ArtifactKind, Job, Task
    from packages.orchestration.data_paths import resolve_data_root
    from packages.orchestration.storage import save_job
    from packages.orchestration.timeline import append_run_event

    contract = DoRunContract(
        autonomy_level=min(autonomy_level, 3),
        stop_before_apply=stop_before_apply,
        max_loops=max_loops,
    )

    data_dir = resolve_data_root()
    result = DoRunResult(
        autonomy_level=contract.autonomy_level,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )

    # --- Phase: init (Step 909) ---
    repo = Path(repo_path).resolve()
    repo_exists = repo.is_dir()
    result.repo_path_safe = repo.name if repo_exists else ""

    job = Job(name=goal[:80], user_prompt=goal[:500])
    if repo_exists:
        art = Artifact(
            name="repo-ref", content="",
            kind=ArtifactKind.UNKNOWN,
            metadata={"repo_path": str(repo)},
        )
        job.artifacts = [art]
    save_job(job)
    result.job_id = str(job.id)

    _do_emit(data_dir, job.id, "do_run_initialized", {
        "goal_safe": goal[:200],
        "autonomy_level": contract.autonomy_level,
        "repo_exists": repo_exists,
    })

    result.phases.append(DoRunPhase(
        phase="init", status="completed",
        safe_summary=f"Job {str(job.id)[:8]} created",
    ))

    # --- Phase: plan (Step 910) ---
    task = Task(description=f"Implement: {goal[:200]}")
    job.tasks = [task]
    save_job(job)
    result.task_id = str(task.id)

    _do_emit(data_dir, job.id, "do_run_planned", {
        "task_id": str(task.id),
        "task_count": 1,
    })

    result.phases.append(DoRunPhase(
        phase="plan", status="completed",
        safe_summary="1 task created (fixture planner)",
    ))

    # --- Phase: context (Step 911) ---
    context_phase = _run_context_phase(job, repo, data_dir, result)
    result.phases.append(context_phase)
    if context_phase.status == "blocked":
        result.stop_reason = DoRunStopReason(
            reason="context_blocked",
            detail="Context inspection shows blocked readiness",
        )
        result.next_safe_action = DoRunNextAction(
            label="Inspect context",
            command=f"remedy context inspect {result.job_id} {result.task_id} --json",
            reason="Context is blocked. Inspect to see what files are missing.",
        )
        result.phases.append(DoRunPhase(
            phase="stop", status="stopped",
            safe_summary="Stopped: context blocked",
        ))
        _do_emit(data_dir, job.id, "do_run_stopped", {
            "reason": "context_blocked",
        })
        return result

    # --- Phase: build (Step 912) ---
    if contract.autonomy_level < 2:
        result.phases.append(DoRunPhase(
            phase="build", status="skipped",
            safe_summary="Skipped: autonomy level < 2",
        ))
        result.stop_reason = DoRunStopReason(
            reason="autonomy_too_low", detail="Build requires autonomy >= 2",
        )
        result.next_safe_action = DoRunNextAction(
            label="Run with higher autonomy",
            command=f"remedy do run \"{goal[:80]}\" --repo {repo_path} --autonomy-level 2 --json",
            reason="Increase autonomy to enable builder.",
        )
        result.phases.append(DoRunPhase(
            phase="stop", status="stopped",
            safe_summary="Stopped: autonomy too low for build",
        ))
        _do_emit(data_dir, job.id, "do_run_stopped", {"reason": "autonomy_too_low"})
        return result

    build_artifact = _run_build_phase(job, goal, repo, data_dir)
    result.artifact_ids.append(str(build_artifact.id))

    _do_emit(data_dir, job.id, "do_run_built", {
        "artifact_id": str(build_artifact.id),
    })

    result.phases.append(DoRunPhase(
        phase="build", status="completed",
        safe_summary="Fixture builder created safe artifact",
    ))

    # --- Phase: patch_intent (Step 913) ---
    intent_id = _run_patch_intent_phase(job, build_artifact, data_dir)
    if intent_id:
        result.patch_intent_id = intent_id
        _do_emit(data_dir, job.id, "do_run_patch_intent_created", {
            "intent_id": intent_id,
        })
        result.phases.append(DoRunPhase(
            phase="patch_intent", status="completed",
            safe_summary="Patch intent created, awaiting approval",
        ))
    else:
        result.phases.append(DoRunPhase(
            phase="patch_intent", status="skipped",
            safe_summary="No patch intent produced",
        ))

    # --- Phase: approval_required (Step 914) ---
    if intent_id and contract.stop_before_apply:
        result.stop_reason = DoRunStopReason(
            reason="approval_required",
            detail="Patch intent needs approval before apply",
        )
        result.next_safe_action = DoRunNextAction(
            label="Approve patch",
            command=f"remedy patch approve {result.job_id} {intent_id}",
            reason="Review and approve the patch intent to proceed.",
        )
        result.phases.append(DoRunPhase(
            phase="approval_required", status="stopped",
            safe_summary="Stopped: approval required before apply",
        ))
    elif not intent_id:
        result.stop_reason = DoRunStopReason(
            reason="build_complete_no_patch_intent",
            detail="Builder completed but no patch intent produced",
        )
        result.next_safe_action = DoRunNextAction(
            label="Show job",
            command=f"remedy job show {result.job_id} --json",
            reason="Inspect job artifacts for build output.",
        )

    # --- Phase: proof (Step 915) ---
    proof_phase = _run_proof_phase(job, data_dir, result)
    result.phases.append(proof_phase)

    # --- Phase: stop ---
    result.phases.append(DoRunPhase(
        phase="stop", status="stopped",
        safe_summary=f"Stopped: {result.stop_reason.reason}",
    ))
    _do_emit(data_dir, job.id, "do_run_stopped", {
        "reason": result.stop_reason.reason,
    })

    save_job(job)
    return result


# ---------------------------------------------------------------------------
# Phase helpers
# ---------------------------------------------------------------------------


def _run_context_phase(
    job: Any, repo: Path, data_dir: Path, result: DoRunResult,
) -> DoRunPhase:
    """Step 911: Context inspection phase."""
    try:
        from packages.orchestration.context_inspector import (
            inspect_context,
            summarize_context_inspection,
            READINESS_BLOCKED,
        )
        from packages.orchestration.timeline import load_run_events

        events = load_run_events(data_dir, job.id)
        inspection = inspect_context(
            job, events,
            task_id=result.task_id or None,
            repo_root=repo if repo.is_dir() else None,
        )

        result.context_summary = (
            f"{inspection.readiness.status}: "
            f"{inspection.budget.file_count} files, "
            f"~{inspection.budget.estimated_total_tokens} tokens"
        )

        _do_emit(data_dir, job.id, "do_run_context_inspected", {
            "readiness": inspection.readiness.status,
            "file_count": inspection.budget.file_count,
            "estimated_tokens": inspection.budget.estimated_total_tokens,
        })

        if inspection.readiness.status == READINESS_BLOCKED:
            return DoRunPhase(
                phase="context", status="blocked",
                safe_summary="Context blocked: " + ", ".join(inspection.readiness.blockers),
            )

        return DoRunPhase(
            phase="context", status="completed",
            safe_summary=result.context_summary,
        )

    except Exception as exc:
        return DoRunPhase(
            phase="context", status="skipped",
            safe_summary=f"Context inspection skipped: {type(exc).__name__}",
        )


def _run_build_phase(job: Any, goal: str, repo: Path, data_dir: Path) -> Any:
    """Step 912: Fixture builder creates safe artifact."""
    from packages.core.models import Artifact, ArtifactKind

    safe_summary = f"Fixture analysis of: {goal[:100]}"
    artifact = Artifact(
        name="fixture-build-output",
        content=safe_summary,
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=job.tasks[0].id if job.tasks else None,
        metadata={"fixture": True, "safe_summary": safe_summary},
    )
    job.artifacts.append(artifact)

    from packages.orchestration.storage import save_job
    save_job(job)
    return artifact


def _run_patch_intent_phase(job: Any, artifact: Any, data_dir: Path) -> str:
    """Step 913: Create patch intent from build artifact."""
    from packages.orchestration.approval_queue import make_intent_id

    intent_id = make_intent_id(artifact.id, 0)

    # Record intent on artifact metadata
    artifact.metadata["patch_intent_explanations"] = [
        {
            "file": "docs/CHANGES.md",
            "action": "create",
            "risk": "low",
            "summary": "Safe documentation change",
        }
    ]
    artifact.metadata["patch_intent_approvals"] = {}

    from packages.orchestration.storage import save_job
    save_job(job)
    return intent_id


def _run_proof_phase(job: Any, data_dir: Path, result: DoRunResult) -> DoRunPhase:
    """Step 915: Build proof chain (incomplete before apply)."""
    try:
        from packages.orchestration.proof_chain import (
            build_proof_chain,
            derive_next_safe_action,
        )
        from packages.orchestration.timeline import load_run_events

        events = load_run_events(data_dir, job.id)
        chain = build_proof_chain(job, events)
        result.proof_status = chain.summary_status

        nsa = derive_next_safe_action(job, events)
        if nsa and result.next_safe_action is None:
            result.next_safe_action = DoRunNextAction(
                label=nsa.label,
                command=nsa.command,
                reason=nsa.reason,
            )

        return DoRunPhase(
            phase="proof", status="completed",
            safe_summary=f"Proof: {chain.summary_status}",
        )
    except Exception:
        result.proof_status = "incomplete"
        return DoRunPhase(
            phase="proof", status="completed",
            safe_summary="Proof: incomplete (no changes applied yet)",
        )


# ---------------------------------------------------------------------------
# Export / summary
# ---------------------------------------------------------------------------


def export_do_run_json(result: DoRunResult) -> dict[str, Any]:
    """Export DoRunResult as safe JSON dict."""
    out: dict[str, Any] = {
        "version": result.version,
        "job_id": result.job_id,
        "task_id": result.task_id,
        "artifact_ids": result.artifact_ids,
        "patch_intent_id": result.patch_intent_id,
        "proof_status": result.proof_status,
        "phases": [
            {
                "phase": p.phase,
                "status": p.status,
                "safe_summary": p.safe_summary,
            }
            for p in result.phases
        ],
        "stop_reason": {
            "reason": result.stop_reason.reason,
            "detail": result.stop_reason.detail,
        },
        "next_safe_action": None,
        "autonomy_level": result.autonomy_level,
        "repo_path_safe": result.repo_path_safe,
        "context_summary": result.context_summary,
        "generated_at": result.generated_at,
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


def summarize_do_run(result: DoRunResult) -> str:
    """Human-readable do run summary."""
    lines: list[str] = []
    lines.append(f"remedy do: {result.job_id[:8]}")
    lines.append(f"Autonomy: {result.autonomy_level}")
    if result.repo_path_safe:
        lines.append(f"Repo: {result.repo_path_safe}")

    lines.append("")
    lines.append("Phases:")
    for p in result.phases:
        lines.append(f"  [{p.status}] {p.phase}: {p.safe_summary}")

    if result.context_summary:
        lines.append(f"\nContext: {result.context_summary}")

    lines.append(f"\nStop: {result.stop_reason.reason}")
    if result.stop_reason.detail:
        lines.append(f"  {result.stop_reason.detail}")

    if result.next_safe_action:
        lines.append(f"\nNext: {result.next_safe_action.label}")
        lines.append(f"  $ {result.next_safe_action.command}")

    if result.proof_status:
        lines.append(f"\nProof: {result.proof_status}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Event helper
# ---------------------------------------------------------------------------


def _do_emit(data_dir: Path, job_id: UUID, event: str, metadata: dict[str, Any]) -> None:
    from packages.orchestration.timeline import append_run_event
    append_run_event(data_dir, job_id, event=event, metadata=metadata)
