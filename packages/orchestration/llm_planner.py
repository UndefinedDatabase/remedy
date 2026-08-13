"""
LLM-backed job planning orchestration.

Provides plan_job_with_llm() which runs the planning step when a real
LLM planner provider is available.

The provider is injected as a callable — this module never imports provider
code. Orchestration owns all state transitions, transformation, and idempotency.
"""

from __future__ import annotations

from collections.abc import Callable

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.artifact_index import planning_artifact
from packages.orchestration.job_runner import PlanJobResult
from packages.orchestration.planner_models import PlannerOutput, ProposedTask
from packages.orchestration.prompt_segments import (
    ComposedPrompt,
    PromptSegmentRegistry,
    SegmentStabilityRank,
    compose_prompt_segments,
)


def _deduplicate_task_types(proposed_tasks: list[ProposedTask]) -> list[Task]:
    """Convert ProposedTask list to Task list with unique task_type values.

    If two proposed tasks share the same task_type, the second and subsequent
    occurrences are suffixed with _2, _3, etc. This prevents downstream
    consumers from confusing semantically different tasks that a planner
    accidentally gave the same type label.

    Example: [write_tests, write_tests] -> [write_tests, write_tests_2]
    """
    seen: dict[str, int] = {}
    tasks: list[Task] = []
    for t in proposed_tasks:
        tt = t.task_type
        if tt in seen:
            seen[tt] += 1
            tt = f"{t.task_type}_{seen[tt]}"
        else:
            seen[tt] = 1
        tasks.append(Task(description=t.description, inputs={"task_type": tt}))
    return tasks


def _recall_memory_for_planning(job: Job) -> tuple[str, dict]:
    """Recall approved memory for planner context injection.

    Returns (memory_section_text, metadata_dict).
    Empty string and metadata when no memory available.
    """
    try:
        from packages.memory.context_summary import (
            build_memory_context,
            format_memory_section,
        )
        project_id = job.metadata.get("project_id")
        ctx = build_memory_context(
            project_id=project_id,
            job_id=str(job.id) if not project_id else None,
            budget=500,
        )
        section = format_memory_section(ctx)
        meta = {
            "memory_item_count": ctx.item_count,
            "memory_estimated_tokens": ctx.estimated_tokens,
            "memory_truncated": ctx.truncated,
            "memory_scope": ctx.scope,
            "memory_context_hash": ctx.context_hash,
        }
        # Emit audit event
        from packages.memory.context_summary import emit_memory_recalled_event
        data_dir = job.metadata.get("data_dir")
        emit_memory_recalled_event(ctx, data_dir=data_dir, job_id=str(job.id), stage="planning")
        return section, meta
    except (ImportError, OSError, ValueError):
        return "", {}


# Named segments for the planner prompt, so a ledger row can say WHERE its
# tokens went. Ranks are the composition sort key, not a semantic label: TASK
# before STEERING is what reproduces the byte order already sent (DECISION D3).
def compose_planner_prompt(job_prompt: str, memory_section: str = "") -> ComposedPrompt:
    """Compose the planner prompt from registered segments, with its manifest.

    Byte identity with the pre-F115 concatenation is the whole contract: the
    join string is `PROMPT_SEGMENT_DELIMITER`, the same blank-line separator
    this module concatenated by hand, and an absent memory section registers NO
    segment rather than an empty one — so one segment composes to the bare job
    prompt, with no separator anywhere in it.
    """
    registry = PromptSegmentRegistry()
    registry.register("planner_job_prompt", SegmentStabilityRank.TASK, job_prompt)
    if memory_section:
        registry.register(
            "planner_memory_context", SegmentStabilityRank.STEERING, memory_section
        )
    return compose_prompt_segments(registry.registered_segments())


def plan_job_with_llm(
    job: Job,
    call_planner: Callable[[str], PlannerOutput],
    *,
    on_prompt_composed: Callable[[ComposedPrompt], None] | None = None,
) -> PlanJobResult:
    """Plan a job using an injected LLM planner callable.

    call_planner receives the job prompt string and must return a validated
    PlannerOutput. All errors from the provider propagate to the caller.

    Orchestration is responsible for:
      - idempotency (no-op if job already has tasks or artifacts)
      - state transitions: PENDING -> RUNNING -> PLANNED
      - transforming PlannerOutput into Job.tasks and a planning Artifact
      - deduplicating task_type values to avoid ambiguous downstream execution
      - NOT mutating the job through the provider
      - injecting approved project memory context when available
      - handing the composed prompt to ``on_prompt_composed``, when given,
        immediately before the provider call, so a caller can trace the
        segment manifest of the bytes it is about to send

    Caller must persist result.job after this call returns.

    Returns PlanJobResult(job, changed=False) if planning was skipped.
    """
    if job.tasks or job.artifacts:
        return PlanJobResult(job=job, changed=False)

    job.state = RunState.RUNNING

    # Recall approved memory (safe, bounded, no raw content)
    memory_section, memory_meta = _recall_memory_for_planning(job)

    # F115 D1/D3: compose instead of concatenating, so the caller's trace entry
    # carries a real segment manifest. The sent bytes are unchanged — the
    # composer joins with the same delimiter this concatenation used.
    composed = compose_planner_prompt(job.user_prompt or job.name, memory_section)
    prompt = composed.text
    if on_prompt_composed is not None:
        on_prompt_composed(composed)

    output: PlannerOutput = call_planner(prompt)

    job.tasks = _deduplicate_task_types(output.proposed_tasks)

    import hashlib as _hashlib
    _raw_prompt = job.user_prompt or job.name
    _prompt_hash = _hashlib.sha256(_raw_prompt.encode()).hexdigest()[:16]
    content_lines = [
        "LLM Planning Output",
        f"Job:    {job.id}",
        f"Prompt: [redacted] (hash={_prompt_hash}, len={len(_raw_prompt)})",
        "",
        f"Summary: {output.summary}",
        "",
        "Tasks:",
    ]
    for task in job.tasks:
        content_lines.append(f"  - {task.inputs['task_type']}: {task.description}")
    if output.acceptance_checks:
        content_lines.append("")
        content_lines.append("Acceptance Checks:")
        for c in output.acceptance_checks:
            content_lines.append(f"  - {c}")
    if output.notes:
        content_lines.append("")
        content_lines.append("Notes:")
        for n in output.notes:
            content_lines.append(f"  - {n}")

    # task_id=None: orchestration-owned artifact (see Artifact docstring).
    # Metadata uses consistent keys; provider/role/model/elapsed_ms/task_count
    # are added later by annotate_planning_result() after timing is known.
    job.artifacts = [
        Artifact(
            name="planning_output",
            content="\n".join(content_lines),
            mime_type="text/plain",
            task_id=None,
            kind=ArtifactKind.PLANNING,
            metadata={
                "summary": output.summary,
                "prompt_present": bool(_raw_prompt),
                "prompt_hash": _prompt_hash,
                "prompt_length": len(_raw_prompt),
                **memory_meta,
            },
        )
    ]

    job.state = RunState.PLANNED
    return PlanJobResult(job=job, changed=True)


def annotate_planning_result(
    result: PlanJobResult,
    *,
    provider: str,
    role: str,
    model: str,
    elapsed_ms: float,
) -> None:
    """Enrich the planning artifact metadata with provider/role/model/timing info.

    Locates the planning artifact via planning_artifact() — prefers explicit
    kind=PLANNING, falls back to legacy name+task_id convention for pre-Step-14
    artifacts.

    No-op if result.changed is False or no planning artifact is found.

    Designed to be called after plan_job_with_llm returns, before persisting.
    """
    if not result.changed:
        return
    artifact = planning_artifact(result.job.artifacts)
    if artifact is None:
        return
    artifact.metadata.update(
        {
            "provider": provider,
            "role": role,
            "model": model,
            "task_count": len(result.job.tasks),
            "elapsed_ms": round(elapsed_ms),
        }
    )
