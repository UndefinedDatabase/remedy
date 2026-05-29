"""
Continue-from-node v0 — create a linked child job from a Brain node.

Every Brain node can become a safe origin for a new job. This is the
foundation for the user "joining in" from the Brain.

No auto-execution, no permission escalation, no LLM call, no file mutation.

Public API::

    continue_from_node(parent_job, graph, node_id, prompt, *, task_type=None) -> ContinueResult
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

from packages.core.models import Artifact, ArtifactKind, Job, RunState, Task
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.run_log import RunLogWriter
from packages.orchestration.storage import save_job
from packages.orchestration.project_brain import ProjectBrainGraph


@dataclass(frozen=True)
class ContinueResult:
    """Result of a continue-from-node operation."""

    parent_job_id: str
    child_job_id: str
    origin_node_id: str
    origin_node_type: str
    inherited_project: bool
    inherited_repo: bool


def continue_from_node(
    parent_job: Job,
    graph: ProjectBrainGraph,
    node_id: str,
    prompt: str,
    *,
    task_type: str | None = None,
) -> ContinueResult:
    """Create a linked child job from a Brain node.

    Validates parent job and node existence. Creates a new job with
    provenance metadata linking back to the parent and origin node.

    No auto-execution, no permission escalation, no LLM call.
    """
    # Validate node exists in graph
    node = next((n for n in graph.nodes if n.id == node_id), None)
    if node is None:
        safe_id = node_id[:64] if node_id else "(empty)"
        raise ValueError(f"node not found in parent brain graph: {safe_id!r}")

    # Determine inherited metadata
    parent_project_id = parent_job.metadata.get("project_id")
    parent_repo = parent_job.metadata.get("target_repo")

    # Build child job
    child_id = uuid4()
    child_meta: dict[str, Any] = {
        "parent_job_id": str(parent_job.id),
        "origin_node_id": node_id,
        "origin_node_type": node.type,
        "origin_node_label": node.label[:80],
        "origin_reason": f"Continued from {node.type} node in job {str(parent_job.id)[:8]}",
    }
    if parent_project_id:
        child_meta["project_id"] = parent_project_id
    if parent_repo:
        child_meta["target_repo"] = parent_repo

    # Create task if task_type provided
    tasks: list[Task] = []
    if task_type:
        task_id = uuid4()
        tasks.append(Task(
            id=task_id,
            description=prompt[:200] if len(prompt) > 200 else prompt,
            status=RunState.PENDING,
            inputs={"task_type": task_type},
            output_artifact_ids=[],
        ))

    child_job = Job(
        id=child_id,
        name=prompt[:100] if len(prompt) > 100 else prompt,
        user_prompt=prompt,
        state=RunState.PLANNED if tasks else RunState.PENDING,
        tasks=tasks,
        artifacts=[],
        metadata=child_meta,
    )

    save_job(child_job)

    # Link child to project if inherited
    if parent_project_id:
        try:
            from packages.orchestration.project_registry import (
                ProjectNotFoundError,
                attach_job,
                load_project,
                save_project,
            )
            project = load_project(UUID(parent_project_id))
            attach_job(project, str(child_id))
            save_project(project)
        except (ValueError, FileNotFoundError, OSError, ProjectNotFoundError) as exc:
            import sys
            print(
                f"WARNING: could not link child job to project "
                f"{parent_project_id[:8]}: {exc}",
                file=sys.stderr,
            )

    # Emit run-log event on parent job
    parent_log = RunLogWriter(job_id=parent_job.id)
    parent_log.log(
        "continued_from_node",
        outcome="spawned_child",
        parent_job_id=str(parent_job.id),
        child_job_id=str(child_id),
        origin_node_id=node_id,
        origin_node_type=node.type,
        inherited_project=bool(parent_project_id),
        inherited_repo=bool(parent_repo),
    )

    # Emit run-log event on child job
    child_log = RunLogWriter(job_id=child_id)
    child_log.log(
        "continued_from_node",
        outcome="created",
        parent_job_id=str(parent_job.id),
        child_job_id=str(child_id),
        origin_node_id=node_id,
        origin_node_type=node.type,
        inherited_project=bool(parent_project_id),
        inherited_repo=bool(parent_repo),
    )

    return ContinueResult(
        parent_job_id=str(parent_job.id),
        child_job_id=str(child_id),
        origin_node_id=node_id,
        origin_node_type=node.type,
        inherited_project=bool(parent_project_id),
        inherited_repo=bool(parent_repo),
    )


def export_continue_result_json(result: ContinueResult) -> dict[str, Any]:
    """JSON-serialisable export."""
    return {
        "version": 1,
        "parent_job_id": result.parent_job_id,
        "child_job_id": result.child_job_id,
        "origin_node_id": result.origin_node_id,
        "origin_node_type": result.origin_node_type,
        "inherited_project": result.inherited_project,
        "inherited_repo": result.inherited_repo,
    }
