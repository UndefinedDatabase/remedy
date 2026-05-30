"""
Project Brain Aggregate v0 — read-only cross-job brain graph for a project.

Aggregates all job brain subgraphs under a single project root node,
with repo placeholder nodes and cross-job edges.

Public API::

    build_project_brain_aggregate(project, jobs, all_events) -> ProjectBrainAggregate
    export_project_brain_aggregate_json(agg) -> dict[str, Any]
    summarize_project_brain_aggregate(agg) -> str
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import PurePosixPath
from typing import Any
from uuid import UUID

from packages.core.models import Job
from packages.orchestration.project_brain import (
    BrainEdge,
    BrainNode,
    NT_JOB,
    NT_MEMORY_ENTRY,
    NT_PATCH_APPLY_PROOF,
    NT_TEST_RUN,
    ProjectBrainGraph,
    build_project_brain,
    export_project_brain_json,
)
from packages.orchestration.project_registry import RemyProject


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

NT_PROJECT = "project"
NT_REPO = "repo"

ET_CONTAINS_JOB = "contains_job"
ET_CONTAINS_REPO = "contains_repo"
ET_TARGETS_REPO = "targets_repo"
ET_CONTINUED_AS = "continued_as"


@dataclass(frozen=True)
class ProjectBrainAggregate:
    """Immutable aggregate brain graph for a project."""

    project_id: str
    project_name: str
    nodes: tuple[BrainNode, ...]
    edges: tuple[BrainEdge, ...]
    job_graphs: tuple[ProjectBrainGraph, ...]
    summary: dict[str, int]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_project_brain_aggregate(
    project: RemyProject,
    jobs: list[Job],
    all_events: dict[str, list[dict[str, Any]]],
    *,
    constitutions: dict[str, object | None] | None = None,
) -> ProjectBrainAggregate:
    """Build an aggregate brain graph across all jobs in a project.

    Args:
        project: The RemyProject.
        jobs: All Job objects linked to this project.
        all_events: Mapping from job_id (str) to run-log events for that job.
        constitutions: Optional mapping from job_id to constitution objects.

    Deterministic, read-only, no repo access, no LLM calls.
    """
    consts = constitutions or {}
    nodes: list[BrainNode] = []
    edges: list[BrainEdge] = []
    job_graphs: list[ProjectBrainGraph] = []

    pid = str(project.id)
    project_node_id = f"project:{pid}"

    # Project root node
    nodes.append(BrainNode(
        id=project_node_id,
        type=NT_PROJECT,
        label=project.name[:60],
        status="active",
        metadata={
            "project_id": pid,
            "job_count": len(jobs),
            "repo_count": len(project.repo_paths),
        },
    ))

    # Repo placeholder nodes
    repo_map: dict[str, str] = {}  # repo_path -> node_id
    for idx, rp in enumerate(project.repo_paths):
        # Use hash for stable ID, basename for label
        rp_hash = hashlib.sha256(rp.encode()).hexdigest()[:12]
        repo_node_id = f"repo:{rp_hash}"
        repo_map[rp] = repo_node_id
        basename = PurePosixPath(rp).name or f"repo-{idx}"
        nodes.append(BrainNode(
            id=repo_node_id,
            type=NT_REPO,
            label=f"Repo: {basename}",
            status="linked",
            metadata={
                "repo_basename": basename,
                "repo_index": idx,
                "linked_job_count": sum(
                    1 for j in jobs
                    if j.metadata.get("target_repo") == rp
                ),
            },
        ))
        edges.append(BrainEdge(
            source=project_node_id,
            target=repo_node_id,
            type=ET_CONTAINS_REPO,
        ))

    # Job subgraphs
    for job in jobs:
        jid = str(job.id)
        events = all_events.get(jid, [])
        constitution = consts.get(jid)

        graph = build_project_brain(job, events, constitution=constitution)
        job_graphs.append(graph)

        # Add all nodes from this job's graph (prefixed to avoid collisions)
        for n in graph.nodes:
            nodes.append(n)
        for e in graph.edges:
            edges.append(e)

        # Project --contains_job--> job
        edges.append(BrainEdge(
            source=project_node_id,
            target=jid,
            type=ET_CONTAINS_JOB,
        ))

        # Job --targets_repo--> repo
        target_repo = job.metadata.get("target_repo")
        if target_repo and target_repo in repo_map:
            edges.append(BrainEdge(
                source=jid,
                target=repo_map[target_repo],
                type=ET_TARGETS_REPO,
            ))

    # Continuation edges from run-log events
    job_id_set = {str(j.id) for j in jobs}
    for jid_str, events in all_events.items():
        for ev in events:
            if ev.get("event") == "continued_from_node" and ev.get("outcome") == "spawned_child":
                child_id = ev.get("metadata", {}).get("child_job_id", "")
                origin = ev.get("metadata", {}).get("origin_node_id", "")
                if child_id in job_id_set:
                    source = origin if origin else jid_str
                    edges.append(BrainEdge(
                        source=source,
                        target=child_id,
                        type=ET_CONTINUED_AS,
                    ))

    # Summary counts
    summary = {
        "job_count": len(jobs),
        "repo_count": len(project.repo_paths),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "memory_count": sum(1 for n in nodes if n.type == NT_MEMORY_ENTRY),
        "proof_count": sum(1 for n in nodes if n.type == NT_PATCH_APPLY_PROOF),
        "test_run_count": sum(1 for n in nodes if n.type == NT_TEST_RUN),
    }

    sorted_nodes = tuple(sorted(nodes, key=lambda n: n.id))
    sorted_edges = tuple(sorted(edges, key=lambda e: (e.source, e.target, e.type)))

    return ProjectBrainAggregate(
        project_id=pid,
        project_name=project.name,
        nodes=sorted_nodes,
        edges=sorted_edges,
        job_graphs=tuple(job_graphs),
        summary=summary,
    )


def export_project_brain_aggregate_json(
    agg: ProjectBrainAggregate,
) -> dict[str, Any]:
    """JSON-serialisable export."""
    return {
        "version": 1,
        "scope": "project",
        "project_id": agg.project_id,
        "project_name": agg.project_name,
        "graph": {
            "nodes": [
                {
                    "id": n.id,
                    "type": n.type,
                    "label": n.label,
                    "status": n.status,
                    "risk": n.risk,
                    "ref_id": n.ref_id,
                    "metadata": n.metadata,
                }
                for n in agg.nodes
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "type": e.type,
                    "metadata": e.metadata,
                }
                for e in agg.edges
            ],
        },
        "summary": agg.summary,
    }


def summarize_project_brain_aggregate(agg: ProjectBrainAggregate) -> str:
    """Human-readable summary."""
    parts: list[str] = []
    parts.append("Remedy Project Brain (Aggregate)")
    parts.append(f"Project: {agg.project_name} ({agg.project_id[:8]})")
    parts.append(f"Jobs: {agg.summary['job_count']}")
    parts.append(f"Repos: {agg.summary['repo_count']}")
    parts.append(f"Nodes: {agg.summary['node_count']}  Edges: {agg.summary['edge_count']}")
    parts.append(f"Memory entries: {agg.summary['memory_count']}")
    parts.append(f"Proofs: {agg.summary['proof_count']}")
    parts.append(f"Test runs: {agg.summary['test_run_count']}")

    # List job subgraphs
    parts.append("")
    for g in agg.job_graphs:
        parts.append(f"  Job {str(g.job_id)[:8]}: {len(g.nodes)} nodes, {len(g.edges)} edges")

    return "\n".join(parts)
