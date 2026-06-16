"""
Brain Node Detail v1 — read-only explanation layer for individual Project Brain nodes.

This is the CLI foundation for the future "click a brain sphere and inspect it" UX.
Given a node_id from a ProjectBrainGraph, it produces a rich, redacted detail view:
explanation, connections, evidence, affected files, and next-action hints.

IMPORTANT — Scope limitations (v1):
  Read-only only.  No repo mutation, no save_job, no patch apply, no permission
  mutation, no shell/subprocess/Git/Docker/network/MCP/Claude execution, no memory
  writes, no frontend implementation, no raw artifact content rendering.

Relationship to other views:
  Project Brain   — the full graph map (all nodes/edges for a job)
  Brain Node Detail — drill into one node (this module)
  Cockpit         — current decision/status overview
  Timeline        — chronological run-log history
  Trust Report    — full audit report

Redaction policy:
  The following are NEVER surfaced in any field, output string, or JSON export:
  - artifact.content
  - patch_intent diff preview
  - approval_reason raw text
  - event.message
  - metadata.command_output / metadata.output
  - raw LLM prompts

Public API::

    build_brain_node_detail(job, graph, node_id, events) -> BrainNodeDetail
    summarize_brain_node_detail(detail) -> str
    export_brain_node_detail_json(detail) -> dict[str, Any]
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from packages.core.models import Job
from packages.orchestration._symbols import (
    INFO as _INFO,
)
from packages.orchestration._symbols import (
    NEXT as _NEXT,
)

# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------
from packages.orchestration._symbols import (
    OK as _OK,
)
from packages.orchestration._symbols import (
    WARN as _WARN,
)
from packages.orchestration._symbols import (
    section,
)
from packages.orchestration.approval_queue import APPROVAL_PENDING, list_patch_intents
from packages.orchestration.project_brain import (
    NT_AGENT_LOOP,
    NT_APPROVAL,
    NT_ARTIFACT,
    NT_AUTONOMY_READINESS,
    NT_BLOCKER,
    NT_CHANGE_SET,
    NT_CONSTITUTION,
    NT_CONTEXT_BUDGET,
    NT_CONTEXT_COVERAGE,
    NT_CONTEXT_PACK,
    NT_DECISION_QUEUE,
    NT_EVENT_LEDGER,
    NT_GIT_STATUS,
    NT_JOB,
    NT_MCP,
    NT_MEMORY,
    NT_MEMORY_ENTRY,
    NT_PATCH_APPLY,
    NT_PATCH_APPLY_PROOF,
    NT_PATCH_INTENT,
    NT_PATCH_REVERT,
    NT_PROJECT_PLACEHOLDER,
    NT_RUN_CONTRACT,
    NT_RUN_EVENT,
    NT_STOP_REASON,
    NT_TASK,
    NT_TEST_RUN,
    NT_TOKEN_POLICY,
    NT_VERIFICATION,
    NT_WORKER_ADAPTER,
    ProjectBrainGraph,
)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BrainNodeDetail:
    """Immutable detail view for a single node in the Project Brain Graph."""

    job_id: str
    node_id: str
    node_type: str
    title: str
    status: str
    risk: str | None
    explanation: str
    why_it_exists: tuple[str, ...]
    connected_to: tuple[dict[str, str], ...]
    evidence: tuple[str, ...]
    affected_files: tuple[str, ...]
    next_actions: tuple[str, ...]
    redaction_notes: tuple[str, ...]


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def build_brain_node_detail(
    job: Job,
    graph: ProjectBrainGraph,
    node_id: str,
    events: list[dict[str, Any]],
) -> BrainNodeDetail:
    """Build a read-only detail view for a single node in the Project Brain Graph.

    Raises ValueError if node_id is not found in the graph.

    Deterministic — no LLM calls, no external processes, no repo access.
    Redaction: artifact content, diff previews, approval reasons, event messages,
    and raw command output are never included.
    """
    node = next((n for n in graph.nodes if n.id == node_id), None)
    if node is None:
        safe_id = node_id[:64] if node_id else "(empty)"
        raise ValueError(f"node not found in graph: {safe_id!r}")

    job_id_str = str(job.id)

    # ── Connections ─────────────────────────────────────────────────────────
    node_map = {n.id: n for n in graph.nodes}
    connected: list[dict[str, str]] = []
    for edge in graph.edges:
        if edge.source == node_id:
            other = node_map.get(edge.target)
            if other:
                connected.append({
                    "direction": "outgoing",
                    "edge_type": edge.type,
                    "node_id": other.id,
                    "node_type": other.type,
                    "node_label": other.label[:60],
                })
        elif edge.target == node_id:
            other = node_map.get(edge.source)
            if other:
                connected.append({
                    "direction": "incoming",
                    "edge_type": edge.type,
                    "node_id": other.id,
                    "node_type": other.type,
                    "node_label": other.label[:60],
                })

    # ── Node-type-specific detail via registry ────────────────────────────────
    handler_with_job = _DETAIL_REGISTRY_JOB.get(node.type)
    if handler_with_job is not None:
        return handler_with_job(job, node, job_id_str, connected)

    handler = _DETAIL_REGISTRY.get(node.type)
    if handler is not None:
        return handler(node, job_id_str, connected)

    # Fallback for unknown future node types
    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node_id,
        node_type=node.type,
        title=node.label[:80],
        status=node.status or "unknown",
        risk=node.risk,
        explanation=f"Node of type '{node.type}'. No detailed explanation available.",
        why_it_exists=("Unknown node type — no explanation registered.",),
        connected_to=tuple(connected),
        evidence=(),
        affected_files=(),
        next_actions=(),
        redaction_notes=("Raw content fields are not rendered.",),
    )


def summarize_brain_node_detail(detail: BrainNodeDetail) -> str:
    """Return a human-readable detail report for a single brain node.

    Read-only: never mutates detail, job, or any filesystem resource.
    Redaction: same policy as build_brain_node_detail.
    """
    parts: list[str] = []
    parts.append("Remedy Brain Node Detail")
    parts.append(f"Job:  {detail.job_id[:8]}")
    parts.append(f"Node: {detail.node_id}")
    parts.append(f"Type: {detail.node_type}")
    parts.append(f"Title: {detail.title}")
    parts.append(f"Status: {detail.status}")
    if detail.risk:
        parts.append(f"Risk: {detail.risk}")

    parts.append(section("Explanation"))
    parts.append(f"  {detail.explanation}")

    parts.append(section("Why it exists"))
    for line in detail.why_it_exists:
        parts.append(f"  {_INFO} {line}")

    if detail.evidence:
        parts.append(section("Evidence"))
        for item in detail.evidence:
            parts.append(f"  {_OK} {item}")

    if detail.affected_files:
        parts.append(section("Affected files"))
        for f in detail.affected_files:
            parts.append(f"  {_WARN} {f}")

    parts.append(section("Connections"))
    if detail.connected_to:
        for conn in detail.connected_to:
            arrow = f"--{conn['edge_type']}-->"
            direction = conn["direction"]
            parts.append(
                f"  [{direction}] {arrow} {conn['node_type']} {conn['node_id'][:20]}"
                f"  ({conn['node_label'][:40]})"
            )
    else:
        parts.append("  (no connections)")

    if detail.next_actions:
        parts.append(section("Next actions"))
        for action in detail.next_actions:
            parts.append(f"  {_NEXT} {action}")

    if detail.redaction_notes:
        parts.append(section("Redaction"))
        for note in detail.redaction_notes:
            parts.append(f"  {_INFO} {note}")

    return "\n".join(parts)


def export_brain_node_detail_json(detail: BrainNodeDetail) -> dict[str, Any]:
    """Export the node detail as a JSON-serialisable dict.

    Redaction: same policy as build_brain_node_detail — no raw content,
    no approval reasons, no event messages, no diff previews.
    """
    return {
        "job_id":          detail.job_id,
        "node_id":         detail.node_id,
        "node_type":       detail.node_type,
        "title":           detail.title,
        "status":          detail.status,
        "risk":            detail.risk,
        "explanation":     detail.explanation,
        "why_it_exists":   list(detail.why_it_exists),
        "connected_to":    list(detail.connected_to),
        "evidence":        list(detail.evidence),
        "affected_files":  list(detail.affected_files),
        "next_actions":    list(detail.next_actions),
        "redaction_notes": list(detail.redaction_notes),
    }


# ---------------------------------------------------------------------------
# Node-type detail builders
# ---------------------------------------------------------------------------


def _detail_job(
    job: Job,
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    from packages.core.models import RunState

    task_count = len(job.tasks)
    artifact_count = len(job.artifacts)
    pending = sum(1 for t in job.tasks if t.status == RunState.PENDING)
    name_trunc = job.name if len(job.name) <= 80 else job.name[:80] + "…"

    explanation = (
        f"Top-level job '{name_trunc}'. "
        f"State: {job.state.value}. "
        f"Contains {task_count} task(s) ({pending} pending) "
        f"and {artifact_count} artifact(s)."
    )

    evidence = [
        f"state: {job.state.value}",
        f"task_count: {task_count}",
        f"pending_tasks: {pending}",
        f"artifact_count: {artifact_count}",
    ]
    if job.user_prompt:
        # Truncate prompt to avoid leaking large text; show intent only.
        prompt_preview = job.user_prompt[:120]
        evidence.append(f"user_prompt (truncated): {prompt_preview}")

    next_actions: list[str] = []
    if pending:
        next_actions.append(f"remedy job run-next {job_id_str}")
    next_actions.append(f"remedy brain trust {job_id_str}")
    next_actions.append(f"remedy brain {job_id_str}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_JOB,
        title=name_trunc,
        status=node.status or job.state.value,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Root node for this orchestration job.",
            "All tasks, artifacts, events, and decisions are connected through this node.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=tuple(next_actions),
        redaction_notes=("Full user prompt is truncated to 120 characters.",),
    )


def _detail_task(
    job: Job,
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    task = next((t for t in job.tasks if str(t.id) == node.id), None)
    if task is None:
        return _fallback(node, job_id_str, connected, "Task not found in job model.")

    task_type = str(task.inputs.get("task_type", "unknown"))
    desc = task.description if len(task.description) <= 120 else task.description[:120] + "…"

    explanation = (
        f"Task of type '{task_type}'. Status: {task.status.value}. "
        f"Description: {desc}"
    )

    # Collect affected files from linked artifact metadata (repo_applied_files only).
    affected: list[str] = []
    for art in job.artifacts:
        if art.task_id == task.id:
            files = art.metadata.get("repo_applied_files", [])
            if isinstance(files, list):
                affected.extend(str(f) for f in files[:20])

    evidence = [
        f"status: {task.status.value}",
        f"task_type: {task_type}",
        f"linked_artifacts: {len(task.output_artifact_ids)}",
    ]

    next_actions: list[str] = []
    if task.status.value == "pending":
        next_actions.append(f"remedy job run-next {job_id_str}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_TASK,
        title=desc,
        status=node.status or task.status.value,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Planned by the orchestration layer to fulfil the job.",
            "Executes a builder and produces one or more artifacts.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=tuple(dict.fromkeys(affected)),
        next_actions=tuple(next_actions),
        redaction_notes=("Artifact content is not rendered.",),
    )


def _detail_artifact(
    job: Job,
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    artifact = next((a for a in job.artifacts if str(a.id) == node.id), None)
    if artifact is None:
        return _fallback(node, job_id_str, connected, "Artifact not found in job model.")

    kind = artifact.kind.value
    owner = f"task {str(artifact.task_id)[:8]}" if artifact.task_id else "orchestration (no task)"
    name_trunc = artifact.name if len(artifact.name) <= 80 else artifact.name[:80] + "…"
    explanation = (
        f"Artifact '{name_trunc}' of kind '{kind}'. "
        f"Created by {owner}. "
        f"Content is not rendered."
    )

    # Affected files: repo_applied_files only, never content.
    affected: list[str] = []
    files = artifact.metadata.get("repo_applied_files", [])
    if isinstance(files, list):
        affected.extend(str(f) for f in files[:20])

    evidence = [
        f"kind: {kind}",
        f"owner: {owner}",
    ]
    pi_count = len(artifact.metadata.get("patch_intent_explanations", []))
    if pi_count:
        evidence.append(f"patch_intent_count: {pi_count}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_ARTIFACT,
        title=name_trunc,
        status="available",
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Produced by a builder or orchestration step.",
            "Carries structured output that may be applied to a repository.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=tuple(affected),
        next_actions=(),
        redaction_notes=(
            "Artifact content is not rendered.",
            "Diff preview is not rendered.",
        ),
    )


def _detail_patch_intent(
    job: Job,
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    # node_id is "pi:<intent_id>"
    intent_id = node.id[3:] if node.id.startswith("pi:") else node.id
    intents = list_patch_intents(job)
    intent = next((i for i in intents if i["intent_id"] == intent_id), None)

    if intent is None:
        return _fallback(node, job_id_str, connected, f"Patch intent '{intent_id}' not found.")

    target_path = intent["target_path"]
    action = intent["action"]
    risk = intent["risk"]
    state = intent["state"]

    explanation = (
        f"Proposes to {action} file '{target_path}'. "
        f"Risk: {risk}. "
        f"Approval state: {state}. "
        f"No diff preview is rendered."
    )

    evidence = [
        f"target_path: {target_path}",
        f"action: {action}",
        f"risk: {risk}",
        f"state: {state}",
    ]

    next_actions: list[str] = []
    if state == APPROVAL_PENDING:
        next_actions.append(
            f"remedy patch approve {job_id_str} {intent_id}"
        )
        next_actions.append(
            f"remedy patch reject {job_id_str} {intent_id}"
        )
    next_actions.append(f"remedy patch show {job_id_str} {intent_id}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_PATCH_INTENT,
        title=f"patch intent: {action} {target_path}",
        status=state,
        risk=risk,
        explanation=explanation,
        why_it_exists=(
            "Derived from a builder artifact to propose a specific file change.",
            "Requires human approval before any file can be written.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(target_path,) if target_path else (),
        next_actions=tuple(next_actions),
        redaction_notes=(
            "Diff preview is not rendered.",
            "Full derivation reason is not rendered.",
        ),
    )


def _detail_approval(
    job: Job,
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    # node_id is "approval:<intent_id>"
    intent_id = node.id[9:] if node.id.startswith("approval:") else node.id
    intents = list_patch_intents(job)
    intent = next((i for i in intents if i["intent_id"] == intent_id), None)

    if intent is None:
        return _fallback(node, job_id_str, connected, f"Approval for '{intent_id}' not found.")

    state = intent["state"]
    decided_at = intent.get("decided_at") or "unknown"
    decided_by = intent.get("decided_by") or "unknown"

    explanation = (
        f"Decision '{state}' recorded for patch intent '{intent_id}'. "
        f"Decided at: {decided_at}. "
        f"Decided by: {decided_by}. "
        f"Approval reason is not rendered."
    )

    evidence = [
        f"state: {state}",
        f"intent_id: {intent_id}",
        f"decided_at: {decided_at}",
        f"decided_by: {decided_by}",
    ]

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_APPROVAL,
        title=f"{state} decision for {intent_id}",
        status=state,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Records the human approval or rejection of a patch intent.",
            "Required before any patch can be applied to the repository.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=(),
        redaction_notes=("Approval reason text is not rendered.",),
    )


def _detail_verification(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    status = node.status or "unknown"
    task_id_short = (node.ref_id or "")[:8] or "unknown"

    explanation = (
        f"Verification result for task {task_id_short}: {status}. "
        f"Recorded when the task runner evaluated the builder output."
    )

    evidence = [f"status: {status}"]
    if node.ref_id:
        evidence.append(f"task_id: {node.ref_id[:36]}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_VERIFICATION,
        title=node.label[:80],
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Created when a task completes verification successfully.",
            "Confirms the builder output passed all acceptance criteria.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=(),
        redaction_notes=("Verification check output details are not rendered.",),
    )


def _detail_blocker(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    capability = str(node.metadata.get("capability", "unknown"))
    status = node.status or "blocked"

    explanation = (
        f"A permission_denied event was recorded for capability '{capability}'. "
        f"The task could not proceed until this permission is granted."
    )

    next_actions = [
        f"remedy job permit {job_id_str} {capability} allow",
        f"remedy job permissions {job_id_str}",
    ]

    evidence = [
        f"capability: {capability}",
        f"status: {status}",
    ]
    if node.ref_id:
        evidence.append(f"task_id: {node.ref_id[:36]}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_BLOCKER,
        title=node.label[:80],
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Created when a task_run_failed event with outcome=permission_denied was recorded.",
            "Signals that a capability must be explicitly granted before work can continue.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=tuple(next_actions),
        redaction_notes=("Event message is not rendered.",),
    )


def _detail_run_event(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    event_type = str(node.metadata.get("event_type", node.label))
    status = node.status or "recorded"

    explanation = (
        f"Lifecycle event '{event_type}'. "
        f"Outcome: {status}. "
        f"Raw event message and command output are not rendered."
    )

    evidence = [
        f"event_type: {event_type}",
        f"outcome: {status}",
    ]

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_RUN_EVENT,
        title=node.label[:80],
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Promoted from the run log to signal a notable lifecycle milestone.",
            "Provides traceability for key orchestration events.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=(f"remedy timeline {job_id_str}",),
        redaction_notes=(
            "Event message is not rendered.",
            "Raw command output is not rendered.",
        ),
    )


def _detail_agent_loop(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    stage    = str(node.metadata.get("stage", "unknown"))
    decision = str(node.metadata.get("decision", "unknown"))
    cycle    = node.metadata.get("cycle", 0)
    status   = node.status or decision

    explanation = (
        f"Agent loop inspection snapshot. "
        f"Stage: {stage}. Decision: {decision}. Cycle: {cycle}."
    )

    evidence = [
        f"stage: {stage}",
        f"decision: {decision}",
        f"cycle: {cycle}",
    ]

    next_actions = [f"remedy agent-loop {job_id_str}"]

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_AGENT_LOOP,
        title=node.label[:80],
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Created when remedy agent-loop was run against this job.",
            "Records the orchestration decision at a point in time.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=tuple(next_actions),
        redaction_notes=(),
    )


def _detail_constitution(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    source_count = node.metadata.get("source_count", "unknown")
    has_tests    = node.metadata.get("has_test_commands", False)
    status       = node.status or "loaded"

    explanation = (
        f"Project Constitution with {source_count} source file(s). "
        f"Has test commands: {has_tests}. "
        f"Advisory only — commands are hints, not enforced instructions."
    )

    evidence = [
        f"source_count: {source_count}",
        f"has_test_commands: {has_tests}",
        f"status: {status}",
    ]

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_CONSTITUTION,
        title="Project Constitution",
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Loaded from the attached repository's config files.",
            "Governs how Remedy interprets test commands and build instructions for this repo.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=(f"remedy constitution {job_id_str}",),
        redaction_notes=("Full source file contents are not rendered.",),
    )


def _detail_memory_entry(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    key = meta.get("key", "unknown")
    tags = meta.get("tags", [])
    source_type = meta.get("source_type", "unknown")
    created_at = meta.get("created_at", "unknown")
    approved = meta.get("approved", False)

    evidence = [
        f"key: {key}",
        f"source: {source_type}",
        f"approved: {approved}",
        f"created: {created_at}",
    ]
    if tags:
        evidence.append(f"tags: {', '.join(tags)}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_MEMORY_ENTRY,
        title=f"Memory: {key}",
        status="active" if approved else "informational",
        risk=None,
        explanation=(
            f"Local memory entry (key={key}). "
            "Approved entries are visible to the agent loop and context coverage."
        ),
        why_it_exists=(
            "Stored via 'remedy memory store' CLI command.",
            "Approved entries contribute to the project_memory context signal.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=(
            f"remedy memory recall --keyword {key} --json",
        ),
        redaction_notes=(
            "Memory value is not shown in brain detail — only key, tags, and metadata.",
        ),
    )


def _detail_memory_placeholder(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_MEMORY,
        title="MemPalace (future)",
        status="informational",
        risk=None,
        explanation=(
            "Reserved node for the Step 24+ semantic memory layer (MemPalace). "
            "Not yet implemented. This placeholder marks the integration point."
        ),
        why_it_exists=(
            "Always present to signal the future memory extension point.",
            "Will be replaced by live MemPalace memory nodes in a future step.",
        ),
        connected_to=tuple(connected),
        evidence=("status: informational — not yet active",),
        affected_files=(),
        next_actions=("Not yet available — Step 24+ only.",),
        redaction_notes=(),
    )


def _detail_mcp_placeholder(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_MCP,
        title="MCP Quarantine (future)",
        status="informational",
        risk=None,
        explanation=(
            "Reserved node for the Step 24+ MCP Quarantine tool layer. "
            "Not yet implemented. This placeholder marks the integration point."
        ),
        why_it_exists=(
            "Always present to signal the future MCP integration point.",
            "Will be replaced by live MCP tool nodes in a future step.",
        ),
        connected_to=tuple(connected),
        evidence=("status: informational — not yet active",),
        affected_files=(),
        next_actions=("Not yet available — Step 24+ only.",),
        redaction_notes=(),
    )


def _detail_context_coverage(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    score = node.metadata.get("score", 0)
    present = node.metadata.get("present_signal_count", 0)
    missing = node.metadata.get("missing_signal_count", 0)
    status = node.status or "unknown"

    explanation = (
        f"Context Coverage ({score}%) is a deterministic health signal "
        f"showing how much structured context Remedy currently has for this job. "
        f"It is not model confidence and not a guarantee of correctness. "
        f"{present} signal(s) present, {missing} missing."
    )

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_CONTEXT_COVERAGE,
        title=node.label[:80],
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Shows what structured context is available for this job.",
            "A low score means Remedy has limited context — not that it will fail.",
            "Project Memory (MemPalace) and MCP context are future signal sources.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"score: {score}%",
            f"present signals: {present}",
            f"missing signals: {missing}",
            f"scope: {node.metadata.get('scope', 'job')}",
        ),
        affected_files=(),
        next_actions=(
            f"remedy context {job_id_str[:8]}",
            f"remedy brain {job_id_str[:8]}",
            f"remedy brain trust {job_id_str[:8]}",
        ),
        redaction_notes=(
            "Does not include raw prompt, file content, artifact content, "
            "event messages, approval reasons, or diff text.",
        ),
    )


def _detail_patch_apply(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    status       = node.status or "unknown"
    target_path  = str(node.metadata.get("target_path", ""))
    action       = str(node.metadata.get("action", ""))
    bytes_written = int(node.metadata.get("bytes_written", 0))
    line_count   = int(node.metadata.get("line_count", 0))
    intent_id    = node.ref_id or node.id[6:]  # strip "apply:" prefix

    explanation = (
        f"Patch intent '{intent_id}' was applied to '{target_path}' "
        f"(action: {action}, outcome: {status}). "
        f"{bytes_written} byte(s) written, {line_count} line(s). "
        f"No patch content or diff text is rendered."
    )

    before_sha = str(node.metadata.get("before_sha256", ""))
    after_sha  = str(node.metadata.get("after_sha256", ""))
    bytes_delta = int(node.metadata.get("bytes_delta", 0))
    line_delta  = int(node.metadata.get("line_delta", 0))

    evidence = [
        f"intent_id: {intent_id}",
        f"target_path: {target_path}",
        f"action: {action}",
        f"outcome: {status}",
        f"bytes_written: {bytes_written}",
        f"line_count: {line_count}",
    ]
    if after_sha:
        evidence.append(f"before_sha256: {before_sha[:16] + '…' if before_sha else '(none)'}")
        evidence.append(f"after_sha256: {after_sha[:16]}…")
        evidence.append(f"bytes_delta: {bytes_delta:+d}")
        evidence.append(f"line_delta: {line_delta:+d}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_PATCH_APPLY,
        title=f"patch apply: {action} {target_path}",
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Records the successful application of an approved patch intent.",
            "Created when remedy patch apply was run.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(target_path,) if target_path else (),
        next_actions=(),
        redaction_notes=(
            "Patch content is not rendered.",
            "Diff text is not rendered.",
        ),
    )


def _detail_test_run(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    status          = node.status or "unknown"
    test_run_id     = str(node.metadata.get("test_run_id", node.ref_id or ""))
    command         = str(node.metadata.get("command", ""))
    exit_code       = node.metadata.get("exit_code")
    duration_ms     = int(node.metadata.get("duration_ms", 0))
    output_lines    = int(node.metadata.get("output_line_count", 0))
    output_bytes    = int(node.metadata.get("output_bytes", 0))
    cmd_source_type = str(node.metadata.get("command_source_type", ""))
    cmd_source_path = str(node.metadata.get("command_source_path", ""))
    cmd_purpose     = str(node.metadata.get("command_purpose", ""))
    cmd_confidence  = str(node.metadata.get("command_confidence", ""))

    outcome_sym = (
        "passed — all tests green"  if status == "passed"
        else "failed — one or more tests failed" if status == "failed"
        else "timed out" if status == "timeout"
        else "blocked — could not run"
    )

    src_str = (
        f" (discovered from {cmd_source_type}:{cmd_source_path}, "
        f"confidence={cmd_confidence})"
        if cmd_source_type else ""
    )
    explanation = (
        f"Local test run '{test_run_id}' using command '{command}'{src_str}. "
        f"Outcome: {outcome_sym}. "
        f"Exit code: {exit_code if exit_code is not None else 'n/a'}. "
        f"Duration: {duration_ms}ms. "
        f"Output file ({output_bytes} bytes, {output_lines} lines) is stored locally "
        f"but raw stdout/stderr are not rendered here."
    )

    evidence = [
        f"test_run_id: {test_run_id}",
        f"command: {command}",
        f"status: {status}",
        f"exit_code: {exit_code if exit_code is not None else 'n/a'}",
        f"duration_ms: {duration_ms}",
        f"output_bytes: {output_bytes}",
        f"output_line_count: {output_lines}",
        f"command_source_type: {cmd_source_type}",
        f"command_source_path: {cmd_source_path}",
        f"command_purpose: {cmd_purpose}",
        f"command_confidence: {cmd_confidence}",
    ]

    next_actions: list[str] = []
    if status == "failed":
        next_actions.append(
            "Check the test run output file in the workspace/test_runs/ directory."
        )
    if status in ("blocked", "timeout"):
        next_actions.append(
            "Verify that the test command is installed and the repo is accessible."
        )

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_TEST_RUN,
        title=f"test run: {status} ({command})",
        status=status,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Created when remedy test run was executed.",
            "Records the outcome of a permission-gated test run against the attached repo.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=tuple(next_actions),
        redaction_notes=(
            "Raw stdout/stderr are not rendered.",
            "Output file path is not included — use the workspace/test_runs/ directory.",
        ),
    )


def _detail_run_contract(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    autonomy = node.metadata.get("autonomy_level", 1)
    allowed = node.metadata.get("allowed_action_count", 0)
    denied = node.metadata.get("denied_action_count", 0)
    max_loops = node.metadata.get("max_loops", 10)
    scope = str(node.metadata.get("scope", "job"))

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_RUN_CONTRACT,
        title="Run Contract (execution boundary)",
        status=node.status or "active",
        risk=None,
        explanation=(
            f"Execution boundary contract for this job. "
            f"Autonomy level: {autonomy}. Scope: {scope}. "
            f"{allowed} allowed actions, {denied} denied actions, max {max_loops} loops. "
            "This is a boundary definition, not a capability promise."
        ),
        why_it_exists=(
            "Every job has an execution boundary that governs what the run can do.",
            "The run contract is the last line of defense before any action is taken.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"autonomy_level: {autonomy}",
            f"allowed_action_count: {allowed}",
            f"denied_action_count: {denied}",
            f"max_loops: {max_loops}",
            f"scope: {scope}",
        ),
        affected_files=(),
        next_actions=(
            "Inspect with `remedy policy contract <job_id>` for full contract details.",
        ),
        redaction_notes=("No sensitive data in run contract.",),
    )


def _detail_token_policy(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    scope = str(node.metadata.get("scope", "job"))
    zero_count = node.metadata.get("zero_token_step_count", 0)
    local_count = node.metadata.get("local_first_step_count", 0)
    expensive_count = node.metadata.get("expensive_step_count", 0)

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_TOKEN_POLICY,
        title="Token Policy (routing budget)",
        status=node.status or "active",
        risk=None,
        explanation=(
            f"Token routing policy for this job. Scope: {scope}. "
            f"{zero_count} zero-token steps, {local_count} local-first steps, "
            f"{expensive_count} expensive steps. "
            "Defines forbidden context and compaction rules."
        ),
        why_it_exists=(
            "Token economy ensures efficient resource usage.",
            "Zero-token steps avoid unnecessary LLM calls for deterministic operations.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"scope: {scope}",
            f"zero_token_step_count: {zero_count}",
            f"local_first_step_count: {local_count}",
            f"expensive_step_count: {expensive_count}",
        ),
        affected_files=(),
        next_actions=(
            "Inspect with `remedy policy token <job_id>` for full policy details.",
        ),
        redaction_notes=("No sensitive data in token policy.",),
    )


def _detail_worker_adapter(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    provider_id = str(node.metadata.get("provider_id", "unknown"))
    exec_mode = str(node.metadata.get("execution_mode", "unknown"))
    role_count = node.metadata.get("supported_role_count", 0)

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_WORKER_ADAPTER,
        title=f"Worker: {node.label}",
        status=node.status or "future",
        risk=None,
        explanation=(
            f"Worker adapter spec for provider '{provider_id}'. "
            f"Execution mode: {exec_mode}. {role_count} supported roles. "
            "This is a provider-neutral specification — no connection or secrets."
        ),
        why_it_exists=(
            "Worker adapters describe available providers without binding to them.",
            "Provider-neutral specs enable future multi-provider orchestration.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"provider_id: {provider_id}",
            f"execution_mode: {exec_mode}",
            f"supported_role_count: {role_count}",
        ),
        affected_files=(),
        next_actions=(
            "Inspect with `remedy workers` for all provider specs.",
        ),
        redaction_notes=("No secrets or API keys in worker specs.",),
    )


def _detail_autonomy_readiness(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    level = node.metadata.get("highest_eligible_level", 0)
    missing = node.metadata.get("missing_count", 0)
    blockers = node.metadata.get("blocker_count", 0)

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_AUTONOMY_READINESS,
        title=f"Autonomy Readiness: Level {level}",
        status=node.status or "active",
        risk=None,
        explanation=(
            f"Autonomy readiness assessment. Highest eligible level: {level}. "
            f"{missing} missing signals, {blockers} blockers. "
            "This is factual infrastructure readiness, not model confidence."
        ),
        why_it_exists=(
            "Quantifies what autonomy level the job can safely support.",
            "Guides execution decisions and surfaces missing prerequisites.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"highest_eligible_level: {level}",
            f"missing_count: {missing}",
            f"blocker_count: {blockers}",
        ),
        affected_files=(),
        next_actions=(
            f"Inspect with `remedy readiness job {job_id_str[:8]}`.",
        ),
        redaction_notes=("No sensitive data in readiness assessment.",),
    )


def _detail_context_pack(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    tokens = node.metadata.get("estimated_tokens", 0)
    budget = node.metadata.get("budget", 0)
    truncated = node.metadata.get("truncated", False)

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_CONTEXT_PACK,
        title="Context Pack",
        status=node.status or "active",
        risk=None,
        explanation=(
            f"Context pack: ~{tokens} tokens (budget={budget}). "
            f"Truncated: {truncated}. "
            "Deterministic compact context for future provider calls."
        ),
        why_it_exists=(
            "Reduces token usage by preparing compact structured context.",
            "No LLM calls, no network, no raw content included.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"estimated_tokens: {tokens}",
            f"budget: {budget}",
            f"truncated: {truncated}",
        ),
        affected_files=(),
        next_actions=(
            f"Build with `remedy context pack {job_id_str[:8]}`.",
        ),
        redaction_notes=("No raw content in context pack metadata.",),
    )


def _detail_patch_apply_proof(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    intent_id = str(meta.get("intent_id", node.ref_id or ""))
    target_path = str(meta.get("target_path", ""))
    action = str(meta.get("action", ""))
    outcome = str(meta.get("outcome", ""))
    before_sha = str(meta.get("before_sha256", ""))
    after_sha = str(meta.get("after_sha256", ""))
    bytes_delta = int(meta.get("bytes_delta", 0))
    line_delta = int(meta.get("line_delta", 0))
    applied_at = str(meta.get("applied_at", ""))

    explanation = (
        f"Cryptographic proof that patch intent '{intent_id}' was applied to "
        f"'{target_path}' (action: {action}, outcome: {outcome}). "
        f"SHA256 changed from {before_sha[:16]}… to {after_sha[:16]}…. "
        f"Bytes delta: {bytes_delta:+d}, line delta: {line_delta:+d}. "
        f"Applied at: {applied_at}."
    )

    evidence = [
        f"intent_id: {intent_id}",
        f"target_path: {target_path}",
        f"action: {action}",
        f"outcome: {outcome}",
        f"before_sha256: {before_sha[:16]}…" if before_sha else "before_sha256: (none)",
        f"after_sha256: {after_sha[:16]}…" if after_sha else "after_sha256: (none)",
        f"bytes_delta: {bytes_delta:+d}",
        f"line_delta: {line_delta:+d}",
        f"applied_at: {applied_at}",
    ]

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_PATCH_APPLY_PROOF,
        title=f"proof: {action} {target_path}",
        status=outcome or node.status or "recorded",
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Records the cryptographic proof (before/after SHA256) of a successful patch apply.",
            "Enables causal tracing from intent → approval → apply → proof → test.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(target_path,) if target_path else (),
        next_actions=(
            f"remedy file why {job_id_str[:8]} {target_path}" if target_path else "",
        ),
        redaction_notes=(
            "No file content or diff text is rendered.",
            "Only SHA256 hashes and byte/line deltas are shown.",
        ),
    )


def _detail_project_placeholder(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    project_id = str(meta.get("project_id", ""))
    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_PROJECT_PLACEHOLDER,
        title=f"Project: {project_id[:8]}" if project_id else "Project (unlinked)",
        status=node.status or "linked",
        risk=None,
        explanation=(
            f"Lightweight marker linking this job to project '{project_id[:8]}'."
        ),
        why_it_exists=(
            "Jobs can be linked to projects for cross-job aggregation.",
        ),
        connected_to=tuple(connected),
        evidence=(f"project_id: {project_id}",) if project_id else (),
        affected_files=(),
        next_actions=(),
        redaction_notes=(),
    )


def _detail_patch_revert(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    intent_id = str(meta.get("intent_id", node.ref_id or ""))
    target_path = str(meta.get("target_path", ""))
    outcome = str(meta.get("outcome", ""))
    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_PATCH_REVERT,
        title=f"Revert: {target_path}" if target_path else "Patch Revert",
        status=node.status or outcome or "reverted",
        risk=None,
        explanation=(
            f"Reverted patch intent '{intent_id}' on '{target_path}'. "
            f"Outcome: {outcome}."
        ),
        why_it_exists=(
            "A previously applied patch was reverted to restore original state.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"intent_id: {intent_id}",
            f"target_path: {target_path}",
            f"outcome: {outcome}",
        ),
        affected_files=(target_path,) if target_path else (),
        next_actions=(),
        redaction_notes=("No file content is rendered.",),
    )


def _detail_git_status(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    is_git = bool(meta.get("is_git_repo", False))
    branch = str(meta.get("branch", ""))
    sha = str(meta.get("head_sha", ""))
    dirty = bool(meta.get("dirty", True))
    changed = int(meta.get("changed_file_count", 0))
    status_hash = str(meta.get("status_hash", ""))

    status_str = "dirty" if dirty else ("clean" if is_git else "unavailable")
    explanation = (
        f"Read-only git status snapshot. "
        f"Branch: {branch} ({sha}). Working tree: {status_str}. "
        f"{changed} changed files. Hash: {status_hash}."
    )

    evidence = [
        f"is_git_repo: {is_git}",
        f"branch: {branch}",
        f"head_sha: {sha}",
        f"dirty: {dirty}",
        f"changed_file_count: {changed}",
        f"status_hash: {status_hash}",
    ]

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_GIT_STATUS,
        title=f"Git: {branch} ({sha})" if is_git else "Git: unavailable",
        status=status_str,
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Read-only snapshot of the attached repository's git state.",
            "No git write operations are performed.",
        ),
        connected_to=tuple(connected),
        evidence=tuple(evidence),
        affected_files=(),
        next_actions=(
            f"remedy repo status {job_id_str} --json",
        ),
        redaction_notes=("No file content or diff text is rendered.",),
    )


def _detail_change_set(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    intent_id = str(meta.get("intent_id", node.ref_id or ""))
    target_path = str(meta.get("target_path", ""))
    risk = str(meta.get("risk", ""))
    status = str(meta.get("status", ""))
    approval = str(meta.get("approval_state", ""))
    apply_outcome = str(meta.get("apply_outcome", ""))
    test_status = str(meta.get("test_status", ""))
    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_CHANGE_SET,
        title=f"Change: {target_path}" if target_path else "Change Set Entry",
        status=node.status or status,
        risk=risk or None,
        explanation=(
            f"Change set entry for '{target_path}'. "
            f"Approval: {approval}. Apply: {apply_outcome}. Test: {test_status}."
        ),
        why_it_exists=(
            "Tracks the full lifecycle of a single file change.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"intent_id: {intent_id}",
            f"target_path: {target_path}",
            f"risk: {risk}",
            f"approval: {approval}",
            f"apply: {apply_outcome}",
            f"test: {test_status}",
        ),
        affected_files=(target_path,) if target_path else (),
        next_actions=(),
        redaction_notes=("No diff content is rendered.",),
    )


def _detail_event_ledger(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    event_count = int(meta.get("event_count", 0))
    failed_count = int(meta.get("failed_count", 0))
    proof_count = int(meta.get("proof_count", 0))
    test_count = int(meta.get("test_count", 0))
    last_event_at = str(meta.get("last_event_at", ""))

    explanation = (
        f"Event ledger summary: {event_count} total events, "
        f"{failed_count} failed, {proof_count} proof, {test_count} test. "
        f"Last event: {last_event_at or 'none'}."
    )

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_EVENT_LEDGER,
        title=f"Event Ledger ({event_count} events)",
        status=node.status or "active",
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Aggregates run-log events into a summary for the brain graph.",
            "Individual events are not stored in the brain — only counts.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"event_count: {event_count}",
            f"failed_count: {failed_count}",
            f"proof_count: {proof_count}",
            f"test_count: {test_count}",
            f"last_event_at: {last_event_at}",
        ),
        affected_files=(),
        next_actions=(
            f"remedy event list {job_id_str[:8]} --json",
            f"remedy event timeline {job_id_str[:8]}",
        ),
        redaction_notes=("Individual event messages are not rendered.",),
    )


def _detail_stop_reason(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    reason_code = str(meta.get("reason_code", "unknown"))
    severity = str(meta.get("severity", "unknown"))
    status = str(meta.get("status", "open"))
    source = str(meta.get("source", ""))

    explanation = (
        f"Stop reason '{reason_code}' (severity: {severity}, status: {status}). "
        f"Source: {source or 'derived'}."
    )

    next_actions: list[str] = []
    if status == "open":
        next_actions.append(f"remedy blocker list {job_id_str[:8]}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_STOP_REASON,
        title=f"Stop: {reason_code}",
        status=status,
        risk=severity if severity in ("high", "critical") else None,
        explanation=explanation,
        why_it_exists=(
            "Derived from job state to explain why execution cannot proceed.",
            "Must be resolved before the autonomy loop can continue.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"reason_code: {reason_code}",
            f"severity: {severity}",
            f"status: {status}",
            f"source: {source}",
        ),
        affected_files=(),
        next_actions=tuple(next_actions),
        redaction_notes=("No raw content in stop reasons.",),
    )


def _detail_decision_queue(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    open_count = int(meta.get("open_count", 0))
    high_count = int(meta.get("high_count", 0))

    explanation = (
        f"{open_count} open decision(s), {high_count} high-priority. "
        "Derived from job state — patch approvals, stop reasons, test failures, etc."
    )

    next_actions: list[str] = []
    if open_count > 0:
        next_actions.append(f"remedy decision list {job_id_str[:8]}")

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_DECISION_QUEUE,
        title=f"Decisions: {open_count} open",
        status="active" if open_count > 0 else "idle",
        risk="high" if high_count > 0 else None,
        explanation=explanation,
        why_it_exists=(
            "Aggregates everything needing human attention into one surface.",
            "Derived read-only from existing records — not a second source of truth.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"open_count: {open_count}",
            f"high_count: {high_count}",
        ),
        affected_files=(),
        next_actions=tuple(next_actions),
        redaction_notes=("Summary counts only — no raw content.",),
    )


def _detail_context_budget(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
) -> BrainNodeDetail:
    meta = node.metadata or {}
    mode = str(meta.get("recommended_mode", "?"))
    budget = int(meta.get("budget", 0))
    tokens = int(meta.get("estimated_tokens", 0))
    savings = int(meta.get("token_savings", 0))

    explanation = (
        f"Recommended mode: {mode}, budget: {budget}, "
        f"estimated: {tokens} tokens, savings: {savings}."
    )

    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=NT_CONTEXT_BUDGET,
        title=f"Context: {mode}",
        status="ok",
        risk=None,
        explanation=explanation,
        why_it_exists=(
            "Deterministic context budget optimizer recommendation.",
            "Compares modes and picks best fit for the token budget.",
        ),
        connected_to=tuple(connected),
        evidence=(
            f"recommended_mode: {mode}",
            f"budget: {budget}",
            f"estimated_tokens: {tokens}",
            f"token_savings: {savings}",
        ),
        affected_files=(),
        next_actions=(
            f"remedy context explain {job_id_str[:8]}",
            f"remedy context optimize {job_id_str[:8]}",
        ),
        redaction_notes=("Counts and mode only — no raw content.",),
    )


# ---------------------------------------------------------------------------
# Detail handler registries — maps node type to handler function.
# Handlers needing the Job model use _DETAIL_REGISTRY_JOB.
# Handlers needing only node metadata use _DETAIL_REGISTRY.
# ---------------------------------------------------------------------------

_DETAIL_REGISTRY_JOB: dict[str, Any] = {
    NT_JOB: _detail_job,
    NT_TASK: _detail_task,
    NT_ARTIFACT: _detail_artifact,
    NT_PATCH_INTENT: _detail_patch_intent,
    NT_APPROVAL: _detail_approval,
}

_DETAIL_REGISTRY: dict[str, Any] = {
    NT_VERIFICATION: _detail_verification,
    NT_BLOCKER: _detail_blocker,
    NT_RUN_EVENT: _detail_run_event,
    NT_AGENT_LOOP: _detail_agent_loop,
    NT_CONSTITUTION: _detail_constitution,
    NT_MEMORY: _detail_memory_placeholder,
    NT_MEMORY_ENTRY: _detail_memory_entry,
    NT_MCP: _detail_mcp_placeholder,
    NT_CONTEXT_COVERAGE: _detail_context_coverage,
    NT_PATCH_APPLY: _detail_patch_apply,
    NT_TEST_RUN: _detail_test_run,
    NT_RUN_CONTRACT: _detail_run_contract,
    NT_TOKEN_POLICY: _detail_token_policy,
    NT_WORKER_ADAPTER: _detail_worker_adapter,
    NT_AUTONOMY_READINESS: _detail_autonomy_readiness,
    NT_CONTEXT_PACK: _detail_context_pack,
    NT_PATCH_APPLY_PROOF: _detail_patch_apply_proof,
    NT_PROJECT_PLACEHOLDER: _detail_project_placeholder,
    NT_PATCH_REVERT: _detail_patch_revert,
    NT_CHANGE_SET: _detail_change_set,
    NT_GIT_STATUS: _detail_git_status,
    NT_EVENT_LEDGER: _detail_event_ledger,
    NT_STOP_REASON: _detail_stop_reason,
    NT_DECISION_QUEUE: _detail_decision_queue,
    NT_CONTEXT_BUDGET: _detail_context_budget,
}


def _fallback(
    node: Any,
    job_id_str: str,
    connected: list[dict[str, str]],
    reason: str,
) -> BrainNodeDetail:
    return BrainNodeDetail(
        job_id=job_id_str,
        node_id=node.id,
        node_type=node.type,
        title=node.label[:80],
        status=node.status or "unknown",
        risk=node.risk,
        explanation=f"Detail could not be fully resolved: {reason}",
        why_it_exists=(),
        connected_to=tuple(connected),
        evidence=(),
        affected_files=(),
        next_actions=(),
        redaction_notes=("Raw content fields are not rendered.",),
    )
