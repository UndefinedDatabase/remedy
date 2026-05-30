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
  patch_apply_proof   — cryptographic proof of a successful file apply (Step 51)

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
  approved_by           — patch_intent → approval_decision (causal)
  allowed_apply         — approval_decision → patch_apply (causal)
  recorded_proof        — patch_apply → patch_apply_proof (causal)
  proof_verified_by     — patch_apply_proof → test_run (causal)
  informed_memory       — patch_apply_proof → memory (causal)
  summarizes            — context_pack → readiness or job (causal)
  continued_as          — origin_node → child_job_placeholder (Step 52)

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
from packages.orchestration.autonomy_readiness import assess_job_readiness
from packages.orchestration.context_coverage import derive_context_coverage
from packages.orchestration.run_contract import build_default_run_contract
from packages.orchestration.token_policy import build_default_token_policy
from packages.orchestration.worker_adapters import list_worker_specs
from packages.orchestration.change_set import derive_change_set
from packages.orchestration.data_paths import resolve_data_root
from packages.orchestration.timeline import load_run_events


# ---------------------------------------------------------------------------
# Symbols
# ---------------------------------------------------------------------------

from packages.orchestration._symbols import (
    OK as _OK,
    FAIL as _FAIL,
    WARN as _WARN,
    INFO as _INFO,
    NEXT as _NEXT,
    LINE as _LINE,
    section,
)


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
NT_PATCH_APPLY_PROOF   = "patch_apply_proof"
NT_PATCH_REVERT        = "patch_revert"
NT_CHANGE_SET          = "change_set"
NT_GIT_STATUS          = "git_status"

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
# Causal chain edges (Step 51)
ET_APPROVED_BY           = "approved_by"
ET_ALLOWED_APPLY         = "allowed_apply"
ET_RECORDED_PROOF        = "recorded_proof"
ET_PROOF_VERIFIED_BY     = "proof_verified_by"
ET_INFORMED_MEMORY       = "informed_memory"
ET_SUMMARIZES            = "summarizes"
ET_CONTINUED_AS          = "continued_as"
ET_REVERTED_BY           = "reverted_by"
ET_INCLUDES_INTENT       = "includes_intent"
ET_INCLUDES_APPLY        = "includes_apply"
ET_HAS_GIT_STATUS        = "has_git_status"

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
    NT_PATCH_APPLY_PROOF:   21,
    NT_GIT_STATUS:          22,
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
    "continued_from_node",
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
    degraded: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Graph accumulator — mutable workspace for section builders
# ---------------------------------------------------------------------------


class _Acc:
    """Mutable accumulator passed to each section builder."""

    __slots__ = ("job", "events", "constitution", "nodes", "edges",
                 "job_node_id", "degraded")

    def __init__(
        self,
        job: Job,
        events: list[dict[str, Any]],
        constitution: object | None,
    ) -> None:
        self.job = job
        self.events = events
        self.constitution = constitution
        self.nodes: list[BrainNode] = []
        self.edges: list[BrainEdge] = []
        self.job_node_id = str(job.id)
        self.degraded: list[str] = []

    def node_id_set(self) -> set[str]:
        """Build index of all node IDs for O(1) existence checks."""
        return {n.id for n in self.nodes}


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------


def _build_job_node(acc: _Acc) -> None:
    short_name = acc.job.name if len(acc.job.name) <= 50 else acc.job.name[:50] + "\u2026"
    acc.nodes.append(BrainNode(
        id=acc.job_node_id,
        type=NT_JOB,
        label=short_name,
        status=acc.job.state.value,
        ref_id=str(acc.job.id),
        metadata={"task_count": len(acc.job.tasks), "artifact_count": len(acc.job.artifacts)},
    ))


def _build_task_nodes(acc: _Acc) -> None:
    for task in acc.job.tasks:
        tid = str(task.id)
        desc = task.description
        label = desc if len(desc) <= 60 else desc[:60] + "\u2026"
        tt = str(task.inputs.get("task_type", "unknown"))
        acc.nodes.append(BrainNode(
            id=tid, type=NT_TASK, label=label,
            status=task.status.value, ref_id=tid,
            metadata={"task_type": tt},
        ))
        acc.edges.append(BrainEdge(source=acc.job_node_id, target=tid, type=ET_HAS_TASK))


def _build_artifact_nodes(acc: _Acc) -> None:
    for art in acc.job.artifacts:
        aid = str(art.id)
        name = art.name
        label = name if len(name) <= 60 else name[:60] + "\u2026"
        acc.nodes.append(BrainNode(
            id=aid, type=NT_ARTIFACT, label=label,
            status="available", ref_id=aid,
            metadata={"kind": art.kind.value},
        ))
        owner = str(art.task_id) if art.task_id is not None else acc.job_node_id
        acc.edges.append(BrainEdge(source=owner, target=aid, type=ET_CREATED))


def _build_patch_intent_nodes(acc: _Acc) -> None:
    intents = list_patch_intents(acc.job)
    for intent in intents:
        pi_id = intent["intent_id"]
        pi_nid = f"pi:{pi_id}"
        acc.nodes.append(BrainNode(
            id=pi_nid, type=NT_PATCH_INTENT,
            label=f"patch intent {pi_id}",
            status=intent["state"], risk=intent["risk"], ref_id=pi_id,
            metadata={"risk": intent["risk"], "state": intent["state"]},
        ))
        art_short = intent["artifact_id_short"]
        matching = next((a for a in acc.job.artifacts if a.id.hex[:8] == art_short), None)
        if matching:
            acc.edges.append(BrainEdge(source=str(matching.id), target=pi_nid, type=ET_PRODUCED_PI))
        if intent["state"] != APPROVAL_PENDING:
            adec_nid = f"approval:{pi_id}"
            acc.nodes.append(BrainNode(
                id=adec_nid, type=NT_APPROVAL,
                label=f"{intent['state']} {pi_id}",
                status=intent["state"], ref_id=pi_id,
                metadata={"state": intent["state"]},
            ))
            acc.edges.append(BrainEdge(source=pi_nid, target=adec_nid, type=ET_DECIDED))


def _build_apply_nodes(acc: _Acc) -> None:
    for art in acc.job.artifacts:
        records: dict = art.metadata.get("patch_intent_apply_records", {})
        for iid, rec in records.items():
            nid = f"apply:{iid}"
            acc.nodes.append(BrainNode(
                id=nid, type=NT_PATCH_APPLY,
                label=f"applied {iid}",
                status=rec.get("state", "unknown"), ref_id=iid,
                metadata={
                    "target_path": rec.get("target_path", ""),
                    "action": rec.get("action", ""),
                    "bytes_written": int(rec.get("bytes_written", 0)),
                    "line_count": int(rec.get("line_count", 0)),
                    **_extract_proof_fields(rec.get("proof", {})),
                },
            ))
            acc.edges.append(BrainEdge(source=f"pi:{iid}", target=nid, type=ET_APPLIED_BY))


def _build_test_run_nodes(acc: _Acc) -> None:
    apply_ids = [n.id for n in acc.nodes if n.type == NT_PATCH_APPLY]
    last_apply = apply_ids[-1] if apply_ids else None
    idx = 0
    for ev in acc.events:
        if ev.get("event") != "test_run_completed":
            continue
        meta = ev.get("metadata", {})
        tr_id = str(meta.get("test_run_id", f"tr{idx}"))
        command = str(meta.get("command", ""))
        status = str(meta.get("status", "unknown"))
        exit_code_raw = meta.get("exit_code")
        exit_code = int(exit_code_raw) if exit_code_raw is not None else -1
        node_status = "passed" if status == "passed" else "failed" if status == "failed" else "blocked"
        nid = f"test_run:{idx}"
        idx += 1
        acc.nodes.append(BrainNode(
            id=nid, type=NT_TEST_RUN,
            label=f"test run: {status} ({command})",
            status=node_status, ref_id=tr_id,
            metadata={
                "test_run_id": tr_id, "command": command,
                "status": status, "exit_code": exit_code,
                "duration_ms": int(meta.get("duration_ms", 0)),
                "output_line_count": int(meta.get("output_line_count", 0)),
                "output_bytes": int(meta.get("output_bytes", 0)),
                "command_source_type": str(meta.get("command_source_type", "")),
                "command_source_path": str(meta.get("command_source_path", "")),
                "command_purpose": str(meta.get("command_purpose", "")),
                "command_confidence": str(meta.get("command_confidence", "")),
            },
        ))
        acc.edges.append(BrainEdge(source=acc.job_node_id, target=nid, type=ET_HAS_TEST_RUN))
        if last_apply is not None:
            acc.edges.append(BrainEdge(source=nid, target=last_apply, type=ET_VERIFIED_AFTER_APPLY))


def _build_event_derived_nodes(acc: _Acc) -> None:
    ver_idx = blk_idx = al_idx = re_idx = 0
    for ev in acc.events:
        ev_type = ev.get("event", "")
        ev_task_id = ev.get("task_id")

        if ev_type == "task_run_completed" and ev_task_id:
            vid = f"verification:{ver_idx}"
            ver_idx += 1
            acc.nodes.append(BrainNode(
                id=vid, type=NT_VERIFICATION,
                label=f"verification passed (task {str(ev_task_id)[:8]})",
                status="passed", ref_id=str(ev_task_id),
                metadata={"task_id": str(ev_task_id)[:36]},
            ))
            acc.edges.append(BrainEdge(source=str(ev_task_id), target=vid, type=ET_VERIFIED))

        elif ev_type == "task_run_failed":
            outcome = ev.get("outcome") or ev.get("metadata", {}).get("outcome", "")
            if outcome == "permission_denied":
                cap = ev.get("capability") or ev.get("metadata", {}).get("capability", "unknown")
                bid = f"blocker:{blk_idx}"
                blk_idx += 1
                acc.nodes.append(BrainNode(
                    id=bid, type=NT_BLOCKER,
                    label=f"permission_denied:{cap}", status="blocked",
                    ref_id=str(ev_task_id) if ev_task_id else None,
                    metadata={"capability": str(cap)},
                ))
                if ev_task_id:
                    acc.edges.append(BrainEdge(source=str(ev_task_id), target=bid, type=ET_BLOCKED))

        elif ev_type == "agent_loop_inspected" or ev_type.startswith("agent_loop_"):
            meta = ev.get("metadata", {})
            aid = f"agent_loop:{al_idx}"
            al_idx += 1
            stage = str(meta.get("stage", ev.get("stage", "unknown")))
            decision = str(meta.get("decision", ev.get("decision", "unknown")))
            cycle = _safe_int(meta.get("cycle", ev.get("cycle")))
            outcome = str(ev.get("outcome", ""))
            acc.nodes.append(BrainNode(
                id=aid, type=NT_AGENT_LOOP,
                label=f"agent loop: {ev_type.replace('agent_loop_', '')}",
                status=outcome or decision, ref_id=str(acc.job.id),
                metadata={"stage": stage, "decision": decision, "cycle": cycle, "event_type": ev_type},
            ))
            acc.edges.append(BrainEdge(source=aid, target=acc.job_node_id, type=ET_INSPECTED))

        elif ev_type in _KEY_EVENTS:
            rid = f"run_event:{re_idx}"
            re_idx += 1
            outcome = ev.get("outcome", "recorded")
            acc.nodes.append(BrainNode(
                id=rid, type=NT_RUN_EVENT,
                label=ev_type.replace("_", " "),
                status=str(outcome) if outcome else "recorded",
                ref_id=str(acc.job.id), metadata={"event_type": ev_type},
            ))
            acc.edges.append(BrainEdge(source=acc.job_node_id, target=rid, type=ET_EMITTED))


def _build_constitution_node(acc: _Acc) -> None:
    has_event = any(e.get("event") == "project_constitution_loaded" for e in acc.events)
    if acc.constitution is None and not has_event:
        return
    con_meta: dict[str, str | int | bool] = {}
    con_label = "Project Constitution"
    con_status = "loaded"
    if acc.constitution is not None:
        try:
            sc = len(acc.constitution.source_files)
            ht = bool(acc.constitution.test_commands)
            con_meta = {"source_count": sc, "has_test_commands": ht}
            con_label = f"Project Constitution (sources={sc})"
        except AttributeError:
            pass
    else:
        con_status = "from_event"
    acc.nodes.append(BrainNode(
        id="constitution", type=NT_CONSTITUTION,
        label=con_label, status=con_status,
        ref_id=str(acc.job.id), metadata=con_meta,
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="constitution", type=ET_GOVERNED))


def _build_memory_nodes(acc: _Acc) -> None:
    # Placeholder (always present)
    acc.nodes.append(BrainNode(
        id="memory_placeholder", type=NT_MEMORY,
        label="MemPalace (future)", status="informational",
        metadata={"note": "reserved for Step 24+ memory layer"},
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="memory_placeholder", type=ET_FUTURE_MEMORY))

    # Real local memory entries
    try:
        from packages.memory.local_gateway import list_memory
        project_id = acc.job.metadata.get("project_id")
        entries = list_memory(
            project_id=project_id,
            job_id=str(acc.job.id) if not project_id else None,
        )
        if project_id:
            job_entries = list_memory(job_id=str(acc.job.id))
            seen = {me.id for me in entries}
            entries += [e for e in job_entries if e.id not in seen]
        for me in entries:
            if not me.approved:
                continue
            mnid = f"memory:{me.id}"
            acc.nodes.append(BrainNode(
                id=mnid, type=NT_MEMORY_ENTRY,
                label=f"memory: {me.key}", status=me.validity,
                metadata={
                    "key": me.key, "summary": me.summary,
                    "tags": me.tags,
                    "source_type": me.source_type,
                    "source_id": me.source_id or "",
                    "scope": me.scope,
                    "validity": me.validity,
                    "review_status": me.review_status,
                    "approved": me.approved,
                    "evidence_refs_count": len(me.evidence_refs),
                    "created_at": me.created_at,
                },
            ))
            acc.edges.append(BrainEdge(source=acc.job_node_id, target=mnid, type=ET_HAS_MEMORY))
    except (ImportError, FileNotFoundError, OSError):
        acc.degraded.append("memory")

    # MCP placeholder (always present)
    acc.nodes.append(BrainNode(
        id="mcp_placeholder", type=NT_MCP,
        label="MCP Quarantine (future)", status="informational",
        metadata={"note": "reserved for Step 24+ MCP layer"},
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="mcp_placeholder", type=ET_FUTURE_MCP))


def _build_context_coverage_node(acc: _Acc) -> None:
    cov = derive_context_coverage(acc.job, acc.events, constitution=acc.constitution)
    score = cov.score
    status = "low" if score < 50 else "partial" if score < 80 else "strong"
    acc.nodes.append(BrainNode(
        id="context_coverage", type=NT_CONTEXT_COVERAGE,
        label=f"Context Coverage ({score}%)", status=status,
        metadata={
            "score": score,
            "present_signal_count": sum(1 for s in cov.signals if s.present),
            "missing_signal_count": len(cov.missing_keys),
            "scope": "job",
        },
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="context_coverage", type=ET_HAS_CONTEXT_SNAPSHOT))


def _build_project_placeholder(acc: _Acc) -> None:
    raw = acc.job.metadata.get("project_id") if acc.job.metadata else None
    if not raw:
        return
    try:
        UUID(str(raw))
        pid = str(raw)
    except (ValueError, AttributeError):
        return
    nid = f"project:{pid}"
    acc.nodes.append(BrainNode(
        id=nid, type=NT_PROJECT_PLACEHOLDER,
        label=f"Project {pid[:8]}", status="linked",
        metadata={"project_id": pid},
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target=nid, type=ET_BELONGS_TO_PROJECT))


def _build_run_contract_node(acc: _Acc) -> None:
    rc = build_default_run_contract(acc.job)
    acc.nodes.append(BrainNode(
        id="run_contract", type=NT_RUN_CONTRACT,
        label="Run Contract (execution boundary)", status="active",
        metadata={
            "autonomy_level": rc.autonomy_level,
            "allowed_action_count": len(rc.allowed_actions),
            "denied_action_count": len(rc.denied_actions),
            "max_loops": rc.max_loops, "scope": rc.scope,
        },
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="run_contract", type=ET_HAS_RUN_CONTRACT))


def _build_token_policy_node(acc: _Acc) -> None:
    tp = build_default_token_policy(acc.job)
    acc.nodes.append(BrainNode(
        id="token_policy", type=NT_TOKEN_POLICY,
        label="Token Policy (routing budget)", status="active",
        metadata={
            "scope": tp.scope,
            "zero_token_step_count": len(tp.zero_token_steps),
            "local_first_step_count": len(tp.local_first_steps),
            "expensive_step_count": len(tp.expensive_model_steps),
        },
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="token_policy", type=ET_HAS_TOKEN_POLICY))


def _build_worker_adapter_nodes(acc: _Acc) -> None:
    for spec in list_worker_specs():
        nid = f"worker_adapter:{spec.provider_id}"
        acc.nodes.append(BrainNode(
            id=nid, type=NT_WORKER_ADAPTER,
            label=f"Worker: {spec.display_name}", status=spec.status,
            metadata={
                "provider_id": spec.provider_id,
                "execution_mode": spec.execution_mode,
                "supported_role_count": len(spec.supported_roles),
            },
        ))
        acc.edges.append(BrainEdge(source=acc.job_node_id, target=nid, type=ET_HAS_WORKER_ADAPTER))


def _build_readiness_node(acc: _Acc) -> None:
    try:
        evts = load_run_events(resolve_data_root(), acc.job.id)
        report = assess_job_readiness(acc.job, evts)
        sigs = report.signals
        acc.nodes.append(BrainNode(
            id="autonomy_readiness", type=NT_AUTONOMY_READINESS,
            label=f"Readiness: L{report.highest_eligible_level}", status="active",
            metadata={
                "highest_eligible_level": report.highest_eligible_level,
                "missing_count": sum(len(a.missing_signals) for a in report.levels),
                "blocker_count": sum(len(a.blockers) for a in report.levels),
                "scope": report.scope,
                "revert_capable": sigs.get("revert_snapshot", False),
                "test_capable": sigs.get("test_proof", False),
                "memory_present": sigs.get("approved_memory", False),
                "token_policy_applied": sigs.get("token_policy_applied", False),
            },
        ))
        acc.edges.append(BrainEdge(source=acc.job_node_id, target="autonomy_readiness", type=ET_HAS_READINESS))
    except (ImportError, FileNotFoundError, OSError):
        acc.degraded.append("readiness")


def _build_context_pack_node(acc: _Acc) -> None:
    cp_events = [e for e in acc.events if e.get("event") == "context_pack_created"]
    if not cp_events:
        return
    meta = cp_events[-1].get("metadata", {})
    acc.nodes.append(BrainNode(
        id="context_pack", type=NT_CONTEXT_PACK,
        label=f"Context Pack ({meta.get('mode', 'compact')})", status="active",
        metadata={
            "mode": str(meta.get("mode", "compact")),
            "budget": int(meta.get("budget", 0)),
            "estimated_tokens": int(meta.get("estimated_tokens", 0)),
            "truncated": bool(meta.get("truncated", False)),
            "section_count": int(meta.get("section_count", 0)),
        },
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="context_pack", type=ET_HAS_CONTEXT_PACK))


def _build_proof_nodes(acc: _Acc) -> None:
    proof_events = [e for e in acc.events if e.get("event") == "patch_apply_proof_recorded"]
    nids = acc.node_id_set()
    for idx, ev in enumerate(proof_events):
        meta = ev.get("metadata", {})
        iid = str(meta.get("intent_id", f"proof{idx}"))
        pnid = f"proof:{iid}"
        acc.nodes.append(BrainNode(
            id=pnid, type=NT_PATCH_APPLY_PROOF,
            label=f"proof: {meta.get('action', '')} {meta.get('target_path', '')}",
            status=str(meta.get("outcome", "recorded")), ref_id=iid,
            metadata={
                "intent_id": iid,
                "target_path": str(meta.get("target_path", "")),
                "action": str(meta.get("action", "")),
                "outcome": str(meta.get("outcome", "")),
                "before_sha256": str(meta.get("before_sha256", "")),
                "after_sha256": str(meta.get("after_sha256", "")),
                "before_bytes": int(meta.get("before_bytes", 0)),
                "after_bytes": int(meta.get("after_bytes", 0)),
                "bytes_delta": int(meta.get("bytes_delta", 0)),
                "before_line_count": int(meta.get("before_line_count", 0)),
                "after_line_count": int(meta.get("after_line_count", 0)),
                "line_delta": int(meta.get("line_delta", 0)),
                "applied_at": str(meta.get("applied_at", "")),
            },
        ))
        apply_nid = f"apply:{iid}"
        if apply_nid in nids:
            acc.edges.append(BrainEdge(source=apply_nid, target=pnid, type=ET_RECORDED_PROOF))


def _build_revert_nodes(acc: _Acc) -> None:
    nids = acc.node_id_set()
    for ev in acc.events:
        if ev.get("event") != "patch_intent_reverted":
            continue
        meta = ev.get("metadata", {})
        iid = str(meta.get("intent_id", ""))
        if not iid:
            continue
        rnid = f"revert:{iid}"
        acc.nodes.append(BrainNode(
            id=rnid, type=NT_PATCH_REVERT,
            label=f"revert: {meta.get('target_path', '')}",
            status=str(meta.get("outcome", "reverted")), ref_id=iid,
            metadata={
                "intent_id": iid,
                "target_path": str(meta.get("target_path", "")),
                "outcome": str(meta.get("outcome", "")),
                "existed_before": bool(meta.get("existed_before", False)),
                "bytes_written": int(meta.get("bytes_written", 0)),
                "line_count": int(meta.get("line_count", 0)),
                "before_sha256": str(meta.get("before_sha256", "")),
                "after_sha256": str(meta.get("after_sha256", "")),
            },
        ))
        apply_nid = f"apply:{iid}"
        if apply_nid in nids:
            acc.edges.append(BrainEdge(source=apply_nid, target=rnid, type=ET_REVERTED_BY))


def _build_change_set_nodes(acc: _Acc) -> None:
    try:
        entries = derive_change_set(acc.job, acc.events)
    except (ImportError, FileNotFoundError, OSError):
        acc.degraded.append("change_set")
        return
    nids = acc.node_id_set()
    for ce in entries:
        csnid = f"change_set:{ce.intent_id}"
        acc.nodes.append(BrainNode(
            id=csnid, type=NT_CHANGE_SET,
            label=f"change: {ce.target_path}", status=ce.status, ref_id=ce.intent_id,
            metadata={
                "intent_id": ce.intent_id, "target_path": ce.target_path,
                "risk": ce.risk, "status": ce.status,
                "approval_state": ce.approval.get("state", ""),
                "apply_outcome": ce.apply.get("outcome", ""),
                "test_status": ce.test.get("status", ""),
                "revert_outcome": ce.revert.get("outcome", ""),
            },
        ))
        pi_nid = f"pi:{ce.intent_id}"
        if pi_nid in nids:
            acc.edges.append(BrainEdge(source=csnid, target=pi_nid, type=ET_INCLUDES_INTENT))
        apply_nid = f"apply:{ce.intent_id}"
        if apply_nid in nids:
            acc.edges.append(BrainEdge(source=csnid, target=apply_nid, type=ET_INCLUDES_APPLY))


def _build_git_status_node(acc: _Acc) -> None:
    target_repo = acc.job.metadata.get("target_repo") if acc.job.metadata else None
    if not target_repo:
        return
    try:
        from packages.orchestration.git_status import read_git_status
        status = read_git_status(str(target_repo))
    except (ImportError, OSError):
        acc.degraded.append("git_status")
        return
    if not status.is_git_repo:
        return
    acc.nodes.append(BrainNode(
        id="git_status", type=NT_GIT_STATUS,
        label=f"Git: {status.current_branch} ({status.head_sha})",
        status="clean" if status.is_clean else "dirty",
        metadata={
            "current_branch": status.current_branch,
            "head_sha": status.head_sha,
            "is_clean": status.is_clean,
            "modified_count": len(status.modified_files),
            "untracked_count": len(status.untracked_files),
            "staged_count": len(status.staged_files),
            "has_upstream": status.has_upstream,
            "upstream_branch": status.upstream_branch,
            "ahead_count": status.ahead_count,
            "behind_count": status.behind_count,
        },
    ))
    acc.edges.append(BrainEdge(source=acc.job_node_id, target="git_status", type=ET_HAS_GIT_STATUS))


def _build_causal_edges(acc: _Acc) -> None:
    nids = acc.node_id_set()

    # patch_intent --approved_by--> approval_decision
    for n in acc.nodes:
        if n.type == NT_APPROVAL and n.ref_id:
            pi_nid = f"pi:{n.ref_id}"
            if pi_nid in nids:
                acc.edges.append(BrainEdge(source=pi_nid, target=n.id, type=ET_APPROVED_BY))

    # approval_decision --allowed_apply--> patch_apply
    for n in acc.nodes:
        if n.type == NT_PATCH_APPLY and n.ref_id:
            adec_nid = f"approval:{n.ref_id}"
            if adec_nid in nids:
                acc.edges.append(BrainEdge(source=adec_nid, target=n.id, type=ET_ALLOWED_APPLY))

    # proof --proof_verified_by--> test_run (chronological pairing)
    proof_ids = [n.id for n in acc.nodes if n.type == NT_PATCH_APPLY_PROOF]
    test_ids = [n.id for n in acc.nodes if n.type == NT_TEST_RUN]
    if proof_ids and test_ids:
        # Connect each proof to the next test_run after it by index
        ti = 0
        for pi in proof_ids:
            if ti < len(test_ids):
                acc.edges.append(BrainEdge(source=pi, target=test_ids[ti], type=ET_PROOF_VERIFIED_BY))
                ti += 1

    # proof --informed_memory--> memory (match by source_id when possible)
    memory_nodes = [n for n in acc.nodes if n.type == NT_MEMORY_ENTRY]
    if proof_ids and memory_nodes:
        # Build proof intent_id map
        proof_intent_map: dict[str, str] = {}
        for n in acc.nodes:
            if n.type == NT_PATCH_APPLY_PROOF and n.ref_id:
                proof_intent_map[n.ref_id] = n.id
        for mn in memory_nodes:
            src_id = mn.metadata.get("source_id", "")
            # Match source_id to proof intent_id
            matched_proof = proof_intent_map.get(src_id)
            if matched_proof:
                acc.edges.append(BrainEdge(source=matched_proof, target=mn.id, type=ET_INFORMED_MEMORY))
            elif proof_ids:
                # Fallback: last proof for unmatched memory
                acc.edges.append(BrainEdge(source=proof_ids[-1], target=mn.id, type=ET_INFORMED_MEMORY))

    # context_pack --summarizes--> readiness or job
    cp = next((n for n in acc.nodes if n.type == NT_CONTEXT_PACK), None)
    if cp:
        ar = next((n for n in acc.nodes if n.type == NT_AUTONOMY_READINESS), None)
        target = ar.id if ar else acc.job_node_id
        acc.edges.append(BrainEdge(source=cp.id, target=target, type=ET_SUMMARIZES))


def _build_continuation_edges(acc: _Acc) -> None:
    nids = acc.node_id_set()
    cont_events = [
        e for e in acc.events
        if e.get("event") == "continued_from_node" and e.get("outcome") == "spawned_child"
    ]
    for ev in cont_events:
        meta = ev.get("metadata", {})
        child_id = str(meta.get("child_job_id", ""))
        origin_nid = str(meta.get("origin_node_id", ""))
        if not child_id or not origin_nid:
            continue
        placeholder_id = f"child_job:{child_id[:8]}"
        acc.nodes.append(BrainNode(
            id=placeholder_id, type=NT_JOB,
            label=f"Child Job {child_id[:8]}", status="linked", ref_id=child_id,
            metadata={"parent_job_id": str(acc.job.id), "origin_node_id": origin_nid},
        ))
        if origin_nid in nids:
            acc.edges.append(BrainEdge(source=origin_nid, target=placeholder_id, type=ET_CONTINUED_AS))


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
    acc = _Acc(job, events, constitution)

    # Node builders (order matters for some — e.g. apply before test_run)
    _build_job_node(acc)
    _build_task_nodes(acc)
    _build_artifact_nodes(acc)
    _build_patch_intent_nodes(acc)
    _build_apply_nodes(acc)
    _build_test_run_nodes(acc)
    _build_event_derived_nodes(acc)
    _build_constitution_node(acc)
    _build_memory_nodes(acc)
    _build_context_coverage_node(acc)
    _build_project_placeholder(acc)
    _build_run_contract_node(acc)
    _build_token_policy_node(acc)
    _build_worker_adapter_nodes(acc)
    _build_readiness_node(acc)
    _build_context_pack_node(acc)
    _build_proof_nodes(acc)
    _build_revert_nodes(acc)
    _build_change_set_nodes(acc)
    _build_git_status_node(acc)

    # Edge builders (need full node set)
    _build_causal_edges(acc)
    _build_continuation_edges(acc)

    # Sort and freeze
    sorted_nodes = tuple(sorted(acc.nodes, key=lambda n: (_NODE_TYPE_ORDER.get(n.type, 99), n.id)))
    sorted_edges = tuple(sorted(acc.edges, key=lambda e: (e.source, e.target, e.type)))

    return ProjectBrainGraph(
        job_id=job.id, nodes=sorted_nodes, edges=sorted_edges,
        degraded=tuple(acc.degraded),
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
    parts.append(section("Node summary"))
    _all_types = [
        NT_JOB, NT_TASK, NT_ARTIFACT, NT_PATCH_INTENT, NT_APPROVAL,
        NT_VERIFICATION, NT_BLOCKER, NT_RUN_EVENT, NT_AGENT_LOOP,
        NT_CONSTITUTION, NT_CONTEXT_COVERAGE, NT_MEMORY, NT_MCP,
        NT_PROJECT_PLACEHOLDER, NT_PATCH_APPLY, NT_TEST_RUN,
        NT_RUN_CONTRACT, NT_TOKEN_POLICY, NT_WORKER_ADAPTER,
        NT_AUTONOMY_READINESS, NT_CONTEXT_PACK, NT_PATCH_APPLY_PROOF,
        NT_GIT_STATUS,
    ]
    for nt in _all_types:
        count = by_type.get(nt, 0)
        if count:
            parts.append(f"  {nt:<22}  {count}")

    # ── Node listing ───────────────────────────────────────────────────────
    parts.append(section("Graph nodes"))
    for node in graph.nodes:
        sym = _node_symbol(node.type)
        status_str = f" [{node.status}]" if node.status else ""
        risk_str   = f" risk={node.risk}" if node.risk else ""
        id_short   = node.id[:28]
        lbl        = node.label[:42]
        parts.append(f"  {sym} {node.type:<22} {id_short:<28} {lbl}{status_str}{risk_str}")

    # ── Edge listing ───────────────────────────────────────────────────────
    parts.append(section("Graph edges"))
    for edge in graph.edges:
        src = edge.source[:20]
        tgt = edge.target[:20]
        parts.append(f"  {src:<20}  --{edge.type}-->  {tgt}")

    # ── Visual status legend (Step 24+ mapping — no frontend exists yet) ──
    parts.append(section("Visual status legend (Step 24+)"))
    parts.append("  pending nodes: grey")
    parts.append("  running nodes: pulsing")
    parts.append("  completed nodes: white")
    parts.append("  blocked nodes: red")
    parts.append("  needs approval: amber")
    parts.append("  memory layer: violet")
    parts.append("  mcp quarantine: orange")

    # ── Future layers note ─────────────────────────────────────────────────
    parts.append(section("Future layers"))
    parts.append(f"  {_INFO} context_coverage      \u2014 deterministic context-health signal (Step 26)")
    parts.append(f"  {_INFO} memory_placeholder    \u2014 Step 24+ MemPalace / semantic memory")
    parts.append(f"  {_INFO} mcp_placeholder       \u2014 Step 24+ MCP Quarantine / tool layer")
    parts.append(f"  {_INFO} project_placeholder   \u2014 Project Registry v0 link (Step 28)")
    parts.append(f"  {_INFO} patch_apply           \u2014 approved patch application record (Step 30)")
    parts.append(f"  {_INFO} test_run              \u2014 permission-gated local test run result (Step 33)")
    parts.append(f"  {_INFO} React Flow / Three.js / AG-UI / A2UI mapping \u2014 Step 24+")

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
        "degraded": list(graph.degraded),
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
        NT_PATCH_APPLY_PROOF:   _OK,
    }.get(node_type, _INFO)
