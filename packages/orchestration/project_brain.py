"""
Project Brain Graph v1 — read-only graph representation of a Remedy job.

Produces a structured node/edge graph suitable for future visual cockpit
rendering (React Flow, Three.js, AG-UI, A2UI).  This module is a read-only
contract and export layer only — no frontend, no rendering, no external
processes are called.

IMPORTANT — Scope limitations (v1):
  No external processes, no repo access, no frontend, no Three.js / AG-UI /
  React Flow integration.  The graph is a pure data contract for future Steps.
  Step 24+ will map these nodes to visual components.

Node types:
  job                 — top-level job
  task                — individual task within the job
  artifact            — output artifact produced by a task or orchestration
  patch_intent        — a proposed file patch derived from an artifact
  approval_decision   — a recorded approval or rejection for a patch intent
  verification        — a task_run_completed event (verification passed)
  permission_blocker  — a task_run_failed outcome=permission_denied event
  run_event           — a notable lifecycle event in the run log
  agent_loop          — an agent_loop_inspected event snapshot
  constitution        — the attached Project Constitution
  memory_placeholder  — reserved node for future MemPalace memory layer
  mcp_placeholder     — reserved node for future MCP Quarantine layer
  context_coverage    — deterministic context-health snapshot for the job
  project_placeholder — lightweight marker linking job to a RemyProject
  patch_apply         — an approved patch intent application record
  test_run            — a permission-gated local test run result (Step 33)

Edge types:
  has_task              — job → task
  created_artifact      — task (or job) → artifact
  emitted_event         — job → run_event
  produced_patch_intent — artifact → patch_intent
  decided_by            — patch_intent → approval_decision
  applied_by            — patch_intent → patch_apply
  verified_by           — task → verification
  blocked_by            — task → permission_blocker
  inspected_by          — agent_loop → job
  governed_by           — job → constitution
  future_memory_layer   — job → memory_placeholder
  future_mcp_layer      — job → mcp_placeholder
  has_context_snapshot  — job → context_coverage
  belongs_to_project    — job → project_placeholder
  has_test_run          — job → test_run
  verified_after_apply  — test_run → patch_apply (optional, when present)

Redaction policy:
  Artifact content, diff previews, approval reasons, event messages, and
  raw command output are NEVER included in any node label, metadata, or
  summary output.  Only counts, IDs, risk labels, and status values are
  surfaced.

Public API::

    build_project_brain(job, events, *, constitution=None) -> ProjectBrainGraph
    summarize_project_brain(graph) -> str
    export_project_brain_json(graph) -> dict[str, Any]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from packages.core.models import Job, RunState
from packages.orchestration.approval_queue import (
    APPROVAL_PENDING,
    list_patch_intents,
)
from packages.orchestration.context_coverage import derive_context_coverage


# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------

_OK   = "✓"
_FAIL = "✕"
_WARN = "!"
_INFO = "○"
_NEXT = "→"
_LINE = "─"


# ---------------------------------------------------------------------------
# Node / Edge type constants
# ---------------------------------------------------------------------------

NT_JOB          = "job"
NT_TASK         = "task"
NT_ARTIFACT     = "artifact"
NT_PATCH_INTENT = "patch_intent"
NT_APPROVAL     = "approval_decision"
NT_VERIFICATION = "verification"
NT_BLOCKER      = "permission_blocker"
NT_RUN_EVENT    = "run_event"
NT_AGENT_LOOP   = "agent_loop"
NT_CONSTITUTION      = "constitution"
NT_MEMORY            = "memory_placeholder"
NT_MEMORY_ENTRY      = "memory"
NT_MCP               = "mcp_placeholder"
NT_CONTEXT_COVERAGE  = "context_coverage"
NT_PROJECT_PLACEHOLDER = "project_placeholder"
NT_PATCH_APPLY         = "patch_apply"
NT_TEST_RUN            = "test_run"
NT_RUN_CONTRACT        = "run_contract"
NT_TOKEN_POLICY        = "token_policy"
NT_WORKER_ADAPTER      = "worker_adapter"
NT_AUTONOMY_READINESS  = "autonomy_readiness"
NT_CONTEXT_PACK        = "context_pack"

ET_HAS_TASK             = "has_task"
ET_CREATED              = "created_artifact"
ET_EMITTED              = "emitted_event"
ET_PRODUCED_PI          = "produced_patch_intent"
ET_DECIDED              = "decided_by"
ET_APPLIED_BY           = "applied_by"
ET_VERIFIED             = "verified_by"
ET_BLOCKED              = "blocked_by"
ET_INSPECTED            = "inspected_by"
ET_GOVERNED             = "governed_by"
ET_HAS_MEMORY           = "has_memory"
ET_FUTURE_MEMORY        = "future_memory_layer"
ET_FUTURE_MCP           = "future_mcp_layer"
ET_HAS_CONTEXT_SNAPSHOT  = "has_context_snapshot"
ET_BELONGS_TO_PROJECT    = "belongs_to_project"
ET_HAS_TEST_RUN          = "has_test_run"
ET_VERIFIED_AFTER_APPLY  = "verified_after_apply"
ET_HAS_RUN_CONTRACT      = "has_run_contract"
ET_HAS_TOKEN_POLICY      = "has_token_policy"
ET_HAS_WORKER_ADAPTER    = "has_worker_adapter"
ET_HAS_READINESS         = "has_readiness"
ET_HAS_CONTEXT_PACK      = "has_context_pack"

_NODE_TYPE_ORDER: dict[str, int] = {
    NT_JOB:              0,
    NT_TASK:             1,
    NT_ARTIFACT:         2,
    NT_PATCH_INTENT:     3,
    NT_APPROVAL:         4,
    NT_VERIFICATION:     5,
    NT_BLOCKER:          6,
    NT_RUN_EVENT:        7,
    NT_AGENT_LOOP:       8,
    NT_CONSTITUTION:     9,
    NT_CONTEXT_COVERAGE:    10,
    NT_MEMORY:              11,
    NT_MEMORY_ENTRY:        11,
    NT_MCP:                 12,
    NT_PROJECT_PLACEHOLDER: 13,
    NT_PATCH_APPLY:         14,
    NT_TEST_RUN:            15,
    NT_RUN_CONTRACT:        16,
    NT_TOKEN_POLICY:        17,
    NT_WORKER_ADAPTER:      18,
    NT_AUTONOMY_READINESS:  19,
    NT_CONTEXT_PACK:        20,
}

# Run-log events promoted to run_event nodes (not already covered by other types).
# project_constitution_loaded is intentionally excluded: it is represented by the
# dedicated constitution node (section 6 of build_project_brain) and must NOT also
# create a redundant run_event node.
_KEY_EVENTS: frozenset[str] = frozenset({
    "job_created",
    "builder_started",
    "builder_completed",
    "task_run_noop",
    "repo_application_completed",
    "patch_intent_failed",
})


# ---------------------------------------------------------------------------
# Immutable data models
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BrainNode:
    """A single node in the Project Brain Graph."""

    id: str
    type: str
    label: str
    status: str | None = None
    risk: str | None = None
    ref_id: str | None = None
    metadata: dict[str, str | int | bool] = field(default_factory=dict)


@dataclass(frozen=True)
class BrainEdge:
    """A directed edge in the Project Brain Graph."""

    source: str
    target: str
    type: str
    metadata: dict[str, str | int | bool] = field(default_factory=dict)


@dataclass(frozen=True)
class ProjectBrainGraph:
    """Immutable snapshot of the Project Brain Graph for a job."""

    job_id: UUID
    nodes: tuple[BrainNode, ...]
    edges: tuple[BrainEdge, ...]


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def build_project_brain(
    job: Job,
    events: list[dict[str, Any]],
    *,
    constitution: object | None = None,
) -> ProjectBrainGraph:
    """Build a read-only Project Brain Graph from job model and run-log events.

    Deterministic — no LLM calls, no external processes, no repo access.
    Redaction: no artifact content, diff previews, approval reasons,
    event messages, or command output are included.

    The memory_placeholder and mcp_placeholder nodes are ALWAYS present to
    signal the future extension points for MemPalace and MCP Quarantine.
    """
    nodes: list[BrainNode] = []
    edges: list[BrainEdge] = []
    job_node_id = str(job.id)

    # ── 1. Job node ─────────────────────────────────────────────────────────
    short_name = job.name if len(job.name) <= 50 else job.name[:50] + "…"
    nodes.append(BrainNode(
        id=job_node_id,
        type=NT_JOB,
        label=short_name,
        status=job.state.value,
        ref_id=str(job.id),
        metadata={"task_count": len(job.tasks), "artifact_count": len(job.artifacts)},
    ))

    # ── 2. Task nodes ────────────────────────────────────────────────────────
    for task in job.tasks:
        task_node_id = str(task.id)
        desc = task.description
        label = desc if len(desc) <= 60 else desc[:60] + "…"
        task_type = str(task.inputs.get("task_type", "unknown"))
        nodes.append(BrainNode(
            id=task_node_id,
            type=NT_TASK,
            label=label,
            status=task.status.value,
            ref_id=task_node_id,
            metadata={"task_type": task_type},
        ))
        edges.append(BrainEdge(
            source=job_node_id,
            target=task_node_id,
            type=ET_HAS_TASK,
        ))

    # ── 3. Artifact nodes ────────────────────────────────────────────────────
    for artifact in job.artifacts:
        art_node_id = str(artifact.id)
        art_name = artifact.name
        label = art_name if len(art_name) <= 60 else art_name[:60] + "…"
        nodes.append(BrainNode(
            id=art_node_id,
            type=NT_ARTIFACT,
            label=label,
            status="available",
            ref_id=art_node_id,
            metadata={"kind": artifact.kind.value},
        ))
        owner = str(artifact.task_id) if artifact.task_id is not None else job_node_id
        edges.append(BrainEdge(
            source=owner,
            target=art_node_id,
            type=ET_CREATED,
        ))

    # ── 4. Patch intent + approval decision nodes ────────────────────────────
    intents = list_patch_intents(job)
    for intent in intents:
        pi_id = intent["intent_id"]
        pi_node_id = f"pi:{pi_id}"
        nodes.append(BrainNode(
            id=pi_node_id,
            type=NT_PATCH_INTENT,
            label=f"patch intent {pi_id}",
            status=intent["state"],
            risk=intent["risk"],
            ref_id=pi_id,
            metadata={"risk": intent["risk"], "state": intent["state"]},
        ))
        # Edge: owning artifact → patch_intent
        art_short = intent["artifact_id_short"]
        matching_art = next(
            (a for a in job.artifacts if a.id.hex[:8] == art_short),
            None,
        )
        if matching_art:
            edges.append(BrainEdge(
                source=str(matching_art.id),
                target=pi_node_id,
                type=ET_PRODUCED_PI,
            ))

        # Approval decision node (only for decided intents)
        if intent["state"] != APPROVAL_PENDING:
            adec_node_id = f"approval:{pi_id}"
            nodes.append(BrainNode(
                id=adec_node_id,
                type=NT_APPROVAL,
                label=f"{intent['state']} {pi_id}",
                status=intent["state"],
                ref_id=pi_id,
                # approval_reason is NOT included — redacted
                metadata={"state": intent["state"]},
            ))
            edges.append(BrainEdge(
                source=pi_node_id,
                target=adec_node_id,
                type=ET_DECIDED,
            ))

    # ── 4.5. Patch apply record nodes ────────────────────────────────────────
    for artifact in job.artifacts:
        apply_records: dict = artifact.metadata.get("patch_intent_apply_records", {})
        for apply_intent_id, record in apply_records.items():
            apply_node_id = f"apply:{apply_intent_id}"
            apply_state   = record.get("state", "unknown")
            apply_action  = record.get("action", "")
            apply_path    = record.get("target_path", "")
            nodes.append(BrainNode(
                id=apply_node_id,
                type=NT_PATCH_APPLY,
                label=f"applied {apply_intent_id}",
                status=apply_state,
                ref_id=apply_intent_id,
                metadata={
                    "target_path":   apply_path,
                    "action":        apply_action,
                    "bytes_written": int(record.get("bytes_written", 0)),
                    "line_count":    int(record.get("line_count", 0)),
                    **_extract_proof_fields(record.get("proof", {})),
                },
            ))
            # Edge: patch_intent --applied_by--> patch_apply
            pi_node_id = f"pi:{apply_intent_id}"
            edges.append(BrainEdge(
                source=pi_node_id,
                target=apply_node_id,
                type=ET_APPLIED_BY,
            ))

    # ── 4.6. Test run nodes (from test_run_completed events) ─────────────────
    # Collect all patch_apply node IDs so we can optionally connect the latest
    # test_run to the most recent patch_apply.
    apply_node_ids: list[str] = [
        n.id for n in nodes if n.type == NT_PATCH_APPLY
    ]
    last_apply_node_id: str | None = apply_node_ids[-1] if apply_node_ids else None

    test_run_idx = 0
    for ev in events:
        if ev.get("event") != "test_run_completed":
            continue
        meta = ev.get("metadata", {})
        tr_id = str(meta.get("test_run_id", f"tr{test_run_idx}"))
        command = str(meta.get("command", ""))
        status = str(meta.get("status", "unknown"))
        exit_code_raw = meta.get("exit_code")
        exit_code = int(exit_code_raw) if exit_code_raw is not None else -1
        duration_ms = int(meta.get("duration_ms", 0))
        output_line_count = int(meta.get("output_line_count", 0))
        output_bytes = int(meta.get("output_bytes", 0))
        cmd_source_type = str(meta.get("command_source_type", ""))
        cmd_source_path = str(meta.get("command_source_path", ""))
        cmd_purpose = str(meta.get("command_purpose", ""))
        cmd_confidence = str(meta.get("command_confidence", ""))

        node_status = (
            "passed" if status == "passed"
            else "failed" if status == "failed"
            else "blocked"
        )
        tr_node_id = f"test_run:{test_run_idx}"
        test_run_idx += 1
        nodes.append(BrainNode(
            id=tr_node_id,
            type=NT_TEST_RUN,
            label=f"test run: {status} ({command})",
            status=node_status,
            ref_id=tr_id,
            metadata={
                "test_run_id":         tr_id,
                "command":             command,
                "status":              status,
                "exit_code":           exit_code,
                "duration_ms":         duration_ms,
                "output_line_count":   output_line_count,
                "output_bytes":        output_bytes,
                "command_source_type": cmd_source_type,
                "command_source_path": cmd_source_path,
                "command_purpose":     cmd_purpose,
                "command_confidence":  cmd_confidence,
            },
        ))
        edges.append(BrainEdge(
            source=job_node_id,
            target=tr_node_id,
            type=ET_HAS_TEST_RUN,
        ))
        # Optional: connect to the most recent patch_apply (deterministic).
        if last_apply_node_id is not None:
            edges.append(BrainEdge(
                source=tr_node_id,
                target=last_apply_node_id,
                type=ET_VERIFIED_AFTER_APPLY,
            ))

    # ── 5. Event-derived nodes ───────────────────────────────────────────────
    verification_idx = 0
    blocker_idx = 0
    agent_loop_idx = 0
    run_event_idx = 0

    for ev in events:
        ev_type = ev.get("event", "")
        ev_task_id = ev.get("task_id")

        if ev_type == "task_run_completed" and ev_task_id:
            ver_id = f"verification:{verification_idx}"
            verification_idx += 1
            nodes.append(BrainNode(
                id=ver_id,
                type=NT_VERIFICATION,
                label=f"verification passed (task {str(ev_task_id)[:8]})",
                status="passed",
                ref_id=str(ev_task_id),
                metadata={"task_id": str(ev_task_id)[:36]},
            ))
            edges.append(BrainEdge(
                source=str(ev_task_id),
                target=ver_id,
                type=ET_VERIFIED,
            ))

        elif ev_type == "task_run_failed":
            outcome = ev.get("outcome") or ev.get("metadata", {}).get("outcome", "")
            if outcome == "permission_denied":
                cap = ev.get("capability") or ev.get("metadata", {}).get("capability", "unknown")
                blk_id = f"blocker:{blocker_idx}"
                blocker_idx += 1
                nodes.append(BrainNode(
                    id=blk_id,
                    type=NT_BLOCKER,
                    label=f"permission_denied:{cap}",
                    status="blocked",
                    ref_id=str(ev_task_id) if ev_task_id else None,
                    metadata={"capability": str(cap)},
                ))
                if ev_task_id:
                    edges.append(BrainEdge(
                        source=str(ev_task_id),
                        target=blk_id,
                        type=ET_BLOCKED,
                    ))

        elif ev_type == "agent_loop_inspected":
            meta = ev.get("metadata", {})
            al_id = f"agent_loop:{agent_loop_idx}"
            agent_loop_idx += 1
            stage = str(meta.get("stage", ev.get("stage", "unknown")))
            decision = str(meta.get("decision", ev.get("decision", "unknown")))
            cycle = _safe_int(meta.get("cycle", ev.get("cycle")))
            nodes.append(BrainNode(
                id=al_id,
                type=NT_AGENT_LOOP,
                label=f"agent loop: {stage}/{decision}",
                status=decision,
                ref_id=str(job.id),
                metadata={"stage": stage, "decision": decision, "cycle": cycle},
            ))
            edges.append(BrainEdge(
                source=al_id,
                target=job_node_id,
                type=ET_INSPECTED,
            ))

        elif ev_type in _KEY_EVENTS:
            re_id = f"run_event:{run_event_idx}"
            run_event_idx += 1
            outcome = ev.get("outcome", "recorded")
            nodes.append(BrainNode(
                id=re_id,
                type=NT_RUN_EVENT,
                label=ev_type.replace("_", " "),
                status=str(outcome) if outcome else "recorded",
                ref_id=str(job.id),
                metadata={"event_type": ev_type},
            ))
            edges.append(BrainEdge(
                source=job_node_id,
                target=re_id,
                type=ET_EMITTED,
            ))

    # ── 6. Constitution node ─────────────────────────────────────────────────
    has_constitution_event = any(
        e.get("event") == "project_constitution_loaded" for e in events
    )
    if constitution is not None or has_constitution_event:
        con_meta: dict[str, str | int | bool] = {}
        con_label = "Project Constitution"
        con_status = "loaded"
        if constitution is not None:
            try:
                source_count = len(constitution.source_files)
                has_tests = bool(constitution.test_commands)
                con_meta = {"source_count": source_count, "has_test_commands": has_tests}
                con_label = f"Project Constitution (sources={source_count})"
            except AttributeError:
                pass
        else:
            con_status = "from_event"
        nodes.append(BrainNode(
            id="constitution",
            type=NT_CONSTITUTION,
            label=con_label,
            status=con_status,
            ref_id=str(job.id),
            metadata=con_meta,
        ))
        edges.append(BrainEdge(
            source=job_node_id,
            target="constitution",
            type=ET_GOVERNED,
        ))

    # ── 7. Memory + MCP placeholder nodes (always present) ──────────────────
    nodes.append(BrainNode(
        id="memory_placeholder",
        type=NT_MEMORY,
        label="MemPalace (future)",
        status="informational",
        metadata={"note": "reserved for Step 24+ memory layer"},
    ))
    edges.append(BrainEdge(
        source=job_node_id,
        target="memory_placeholder",
        type=ET_FUTURE_MEMORY,
    ))

    # ── 7b. Real local memory nodes (approved entries) ─────────────────────
    try:
        from packages.memory.local_gateway import list_memory
        project_id = job.metadata.get("project_id")
        mem_entries = list_memory(
            project_id=project_id,
            job_id=str(job.id) if not project_id else None,
        )
        for me in mem_entries:
            if not me.approved:
                continue
            mem_node_id = f"memory:{me.id}"
            nodes.append(BrainNode(
                id=mem_node_id,
                type=NT_MEMORY_ENTRY,
                label=f"memory: {me.key}",
                status="active",
                metadata={
                    "key": me.key,
                    "tags": me.tags,
                    "source_type": me.source_type,
                    "source_id": me.source_id or "",
                    "created_at": me.created_at,
                    "approved": me.approved,
                },
            ))
            edges.append(BrainEdge(
                source=job_node_id,
                target=mem_node_id,
                type=ET_HAS_MEMORY,
            ))
    except Exception:
        pass  # Memory not available — no nodes added.

    nodes.append(BrainNode(
        id="mcp_placeholder",
        type=NT_MCP,
        label="MCP Quarantine (future)",
        status="informational",
        metadata={"note": "reserved for Step 24+ MCP layer"},
    ))
    edges.append(BrainEdge(
        source=job_node_id,
        target="mcp_placeholder",
        type=ET_FUTURE_MCP,
    ))

    # ── 8. Context Coverage snapshot node (always present) ──────────────────
    cov = derive_context_coverage(job, events, constitution=constitution)
    cov_score = cov.score
    cov_status = (
        "low" if cov_score < 50
        else "partial" if cov_score < 80
        else "strong"
    )
    nodes.append(BrainNode(
        id="context_coverage",
        type=NT_CONTEXT_COVERAGE,
        label=f"Context Coverage ({cov_score}%)",
        status=cov_status,
        metadata={
            "score": cov_score,
            "present_signal_count": sum(1 for s in cov.signals if s.present),
            "missing_signal_count": len(cov.missing_keys),
            "scope": "job",
        },
    ))
    edges.append(BrainEdge(
        source=job_node_id,
        target="context_coverage",
        type=ET_HAS_CONTEXT_SNAPSHOT,
    ))

    # ── 9. Project placeholder node (present only when job is linked) ────────
    _raw_pid = job.metadata.get("project_id") if job.metadata else None
    project_id_str: str | None = None
    if _raw_pid:
        try:
            UUID(str(_raw_pid))
            project_id_str = str(_raw_pid)
        except (ValueError, AttributeError):
            pass  # malformed project_id — silently omit placeholder
    if project_id_str:
        proj_node_id = f"project:{project_id_str}"
        nodes.append(BrainNode(
            id=proj_node_id,
            type=NT_PROJECT_PLACEHOLDER,
            label=f"Project {str(project_id_str)[:8]}",
            status="linked",
            metadata={"project_id": str(project_id_str)},
        ))
        edges.append(BrainEdge(
            source=job_node_id,
            target=proj_node_id,
            type=ET_BELONGS_TO_PROJECT,
        ))

    # ── 10. Run Contract node (always present) ─────────────────────────────
    from packages.orchestration.run_contract import build_default_run_contract
    rc = build_default_run_contract(job)
    rc_node_id = "run_contract"
    nodes.append(BrainNode(
        id=rc_node_id,
        type=NT_RUN_CONTRACT,
        label="Run Contract (execution boundary)",
        status="active",
        metadata={
            "autonomy_level": rc.autonomy_level,
            "allowed_action_count": len(rc.allowed_actions),
            "denied_action_count": len(rc.denied_actions),
            "max_loops": rc.max_loops,
            "scope": rc.scope,
        },
    ))
    edges.append(BrainEdge(
        source=job_node_id,
        target=rc_node_id,
        type=ET_HAS_RUN_CONTRACT,
    ))

    # ── 11. Token Policy node (always present) ───────────────────────────
    from packages.orchestration.token_policy import build_default_token_policy
    tp = build_default_token_policy(job)
    tp_node_id = "token_policy"
    nodes.append(BrainNode(
        id=tp_node_id,
        type=NT_TOKEN_POLICY,
        label="Token Policy (routing budget)",
        status="active",
        metadata={
            "scope": tp.scope,
            "zero_token_step_count": len(tp.zero_token_steps),
            "local_first_step_count": len(tp.local_first_steps),
            "expensive_step_count": len(tp.expensive_model_steps),
        },
    ))
    edges.append(BrainEdge(
        source=job_node_id,
        target=tp_node_id,
        type=ET_HAS_TOKEN_POLICY,
    ))

    # ── 12. Worker Adapter nodes (one per known provider spec) ────────────
    from packages.orchestration.worker_adapters import list_worker_specs
    for idx, spec in enumerate(list_worker_specs()):
        wa_node_id = f"worker_adapter:{spec.provider_id}"
        nodes.append(BrainNode(
            id=wa_node_id,
            type=NT_WORKER_ADAPTER,
            label=f"Worker: {spec.display_name}",
            status=spec.status,
            metadata={
                "provider_id": spec.provider_id,
                "execution_mode": spec.execution_mode,
                "supported_role_count": len(spec.supported_roles),
            },
        ))
        edges.append(BrainEdge(
            source=job_node_id,
            target=wa_node_id,
            type=ET_HAS_WORKER_ADAPTER,
        ))

    # ── 13. Autonomy Readiness node ─────────────────────────────────────────
    try:
        from packages.orchestration.autonomy_readiness import assess_job_readiness
        from packages.orchestration.data_paths import resolve_data_root as _rdr
        from packages.orchestration.timeline import load_run_events as _lre
        _events = _lre(_rdr(), job.id)
        _report = assess_job_readiness(job, _events)
        ar_node_id = "autonomy_readiness"
        nodes.append(BrainNode(
            id=ar_node_id,
            type=NT_AUTONOMY_READINESS,
            label=f"Readiness: L{_report.highest_eligible_level}",
            status="active",
            metadata={
                "highest_eligible_level": _report.highest_eligible_level,
                "missing_count": sum(len(a.missing_signals) for a in _report.levels),
                "blocker_count": sum(len(a.blockers) for a in _report.levels),
                "scope": _report.scope,
            },
        ))
        edges.append(BrainEdge(
            source=job_node_id, target=ar_node_id,
            type=ET_HAS_READINESS,
        ))
    except Exception:
        pass

    # ── 14. Sort ─────────────────────────────────────────────────────────────
    sorted_nodes = tuple(
        sorted(nodes, key=lambda n: (_NODE_TYPE_ORDER.get(n.type, 99), n.id))
    )
    sorted_edges = tuple(
        sorted(edges, key=lambda e: (e.source, e.target, e.type))
    )

    return ProjectBrainGraph(
        job_id=job.id,
        nodes=sorted_nodes,
        edges=sorted_edges,
    )


def summarize_project_brain(graph: ProjectBrainGraph) -> str:
    """Return a human-readable Project Brain Graph report for a job.

    Read-only: never mutates graph, job, or any filesystem resource.
    Redaction: no artifact content, approval reasons, event messages,
    diff previews, or command output are included in the output.
    """
    short_id = str(graph.job_id)[:8]

    by_type: dict[str, int] = {}
    for node in graph.nodes:
        by_type[node.type] = by_type.get(node.type, 0) + 1

    parts: list[str] = []
    parts.append("Remedy Project Brain")
    parts.append(f"Job: {short_id}")
    parts.append(f"Nodes: {len(graph.nodes)}   Edges: {len(graph.edges)}")

    # ── Node type summary ──────────────────────────────────────────────────
    parts.append(_section("Node summary"))
    _all_types = [
        NT_JOB, NT_TASK, NT_ARTIFACT, NT_PATCH_INTENT, NT_APPROVAL,
        NT_VERIFICATION, NT_BLOCKER, NT_RUN_EVENT, NT_AGENT_LOOP,
        NT_CONSTITUTION, NT_CONTEXT_COVERAGE, NT_MEMORY, NT_MCP,
        NT_PROJECT_PLACEHOLDER, NT_PATCH_APPLY, NT_TEST_RUN,
        NT_RUN_CONTRACT, NT_TOKEN_POLICY, NT_WORKER_ADAPTER,
        NT_AUTONOMY_READINESS, NT_CONTEXT_PACK,
    ]
    for nt in _all_types:
        count = by_type.get(nt, 0)
        if count:
            parts.append(f"  {nt:<22}  {count}")

    # ── Node listing ───────────────────────────────────────────────────────
    parts.append(_section("Graph nodes"))
    for node in graph.nodes:
        sym = _node_symbol(node.type)
        status_str = f" [{node.status}]" if node.status else ""
        risk_str   = f" risk={node.risk}" if node.risk else ""
        id_short   = node.id[:28]
        lbl        = node.label[:42]
        parts.append(f"  {sym} {node.type:<22} {id_short:<28} {lbl}{status_str}{risk_str}")

    # ── Edge listing ───────────────────────────────────────────────────────
    parts.append(_section("Graph edges"))
    for edge in graph.edges:
        src = edge.source[:20]
        tgt = edge.target[:20]
        parts.append(f"  {src:<20}  --{edge.type}-->  {tgt}")

    # ── Visual status legend (Step 24+ mapping — no frontend exists yet) ──
    parts.append(_section("Visual status legend (Step 24+)"))
    parts.append("  pending nodes: grey")
    parts.append("  running nodes: pulsing")
    parts.append("  completed nodes: white")
    parts.append("  blocked nodes: red")
    parts.append("  needs approval: amber")
    parts.append("  memory layer: violet")
    parts.append("  mcp quarantine: orange")

    # ── Future layers note ─────────────────────────────────────────────────
    parts.append(_section("Future layers"))
    parts.append(f"  {_INFO} context_coverage      — deterministic context-health signal (Step 26)")
    parts.append(f"  {_INFO} memory_placeholder    — Step 24+ MemPalace / semantic memory")
    parts.append(f"  {_INFO} mcp_placeholder       — Step 24+ MCP Quarantine / tool layer")
    parts.append(f"  {_INFO} project_placeholder   — Project Registry v0 link (Step 28)")
    parts.append(f"  {_INFO} patch_apply           — approved patch application record (Step 30)")
    parts.append(f"  {_INFO} test_run              — permission-gated local test run result (Step 33)")
    parts.append(f"  {_INFO} React Flow / Three.js / AG-UI / A2UI mapping — Step 24+")

    return "\n".join(parts)


def export_project_brain_json(graph: ProjectBrainGraph) -> dict[str, Any]:
    """Export the graph as a JSON-serialisable dict.

    Schema::

        {
            "version": 1,
            "job_id":  "<uuid>",
            "nodes":   [{"id", "type", "label", "status", "risk", "ref_id", "metadata"}, ...],
            "edges":   [{"source", "target", "type", "metadata"}, ...],
        }

    Redaction: same policy as build_project_brain — no raw content, no
    approval reasons, no event messages, no diff previews.
    """
    return {
        "version": 1,
        "job_id": str(graph.job_id),
        "nodes": [
            {
                "id":       n.id,
                "type":     n.type,
                "label":    n.label,
                "status":   n.status,
                "risk":     n.risk,
                "ref_id":   n.ref_id,
                "metadata": n.metadata,
            }
            for n in graph.nodes
        ],
        "edges": [
            {
                "source":   e.source,
                "target":   e.target,
                "type":     e.type,
                "metadata": e.metadata,
            }
            for e in graph.edges
        ],
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _extract_proof_fields(proof: dict) -> dict:
    """Extract structural proof fields from an apply record's proof dict.

    Returns only safe scalar values; no raw file content.
    Returns an empty dict when proof is absent or empty.
    """
    if not proof:
        return {}
    return {
        "before_sha256":     str(proof.get("before_sha256", "")),
        "after_sha256":      str(proof.get("after_sha256", "")),
        "before_bytes":      int(proof.get("before_bytes", 0)),
        "after_bytes":       int(proof.get("after_bytes", 0)),
        "bytes_delta":       int(proof.get("bytes_delta", 0)),
        "before_line_count": int(proof.get("before_line_count", 0)),
        "after_line_count":  int(proof.get("after_line_count", 0)),
        "line_delta":        int(proof.get("line_delta", 0)),
    }


def _safe_int(val: object, default: int = 0) -> int:
    """Parse val as int; return default on None, missing, or non-numeric input."""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def _section(title: str) -> str:
    bar = _LINE * (50 - len(title) - 1)
    return f"\n{_LINE}{_LINE} {title} {bar}"


def _node_symbol(node_type: str) -> str:
    return {
        NT_JOB:          _OK,
        NT_TASK:         _INFO,
        NT_ARTIFACT:     _INFO,
        NT_PATCH_INTENT: _WARN,
        NT_APPROVAL:     _OK,
        NT_VERIFICATION: _OK,
        NT_BLOCKER:      _FAIL,
        NT_RUN_EVENT:    _INFO,
        NT_AGENT_LOOP:   _INFO,
        NT_CONSTITUTION:        _OK,
        NT_MEMORY:              _INFO,
        NT_MCP:                 _INFO,
        NT_PROJECT_PLACEHOLDER: _INFO,
        NT_PATCH_APPLY:         _OK,
        NT_TEST_RUN:            _INFO,
    }.get(node_type, _INFO)
