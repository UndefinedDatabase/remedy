"""
UI View Model — ELK directional layout + semantic zoom for the PixiJS brain canvas.

Transforms the raw ProjectBrainGraph into a view-model with:
- ELK layered layout (direction: RIGHT)
- 7 semantic zoom levels (Origin → Full Graph)
- Ranked node positions (job → task → artifact → patch → approval → proof → system)
- Explainable edge kinds with user-facing meanings
- Cluster grouping for dense nodes

Layout engine: elk-layered (deterministic, direction: RIGHT).
No ring layout. No random placement. Same graph = same positions.

Zoom levels (0-6):
  0 — Origin:       just the job node
  1 — Intent Path:  job + current task (max 3)
  2 — Work Path:    task, patch, approval/apply (max 8)
  3 — Proof Path:   proof, verification, test, revert (max 12)
  4 — Attention:    decisions, blockers, failed tests (max 18)
  5 — System:       memory, worker, context, events as clusters
  6 — Full Graph:   all nodes (explicit toggle only)

Public API::

    build_brain_view_model(job, events) -> dict
    build_node_detail(job, events, node_id) -> dict
    build_task_progress(job, events) -> dict
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Rank assignment — determines horizontal position in ELK layout
# ---------------------------------------------------------------------------

_RANK_MAP: dict[str, int] = {
    "job": 0,
    "task": 1,
    "artifact": 2,
    "patch_intent": 3,
    "approval_decision": 4,
    "patch_apply": 5,
    "patch_apply_proof": 6,
    "test_run": 6,
    "verification": 6,
    "permission_blocker": 4,
    "decision_queue": 4,
    "run_event": 3,
    "agent_loop": 5,
    "context_budget": 5,
    "context_coverage": 5,
    "constitution": 1,
    "project_placeholder": 1,
    "memory_placeholder": 7,
    "mcp_placeholder": 7,
}

# ---------------------------------------------------------------------------
# Zoom level assignment — when each node type becomes visible
# ---------------------------------------------------------------------------

_ZOOM_MAP: dict[str, int] = {
    "job": 0,
    "task": 1,
    "artifact": 2,
    "patch_intent": 2,
    "approval_decision": 2,
    "patch_apply": 3,
    "patch_apply_proof": 3,
    "test_run": 3,
    "verification": 3,
    "permission_blocker": 4,
    "decision_queue": 4,
    "run_event": 4,
    "agent_loop": 5,
    "context_budget": 5,
    "context_coverage": 5,
    "constitution": 5,
    "project_placeholder": 5,
    "memory_placeholder": 6,
    "mcp_placeholder": 6,
}

# Label visibility — when text appears (always >= zoom visibility)
_LABEL_ZOOM: dict[str, int] = {
    "job": 1,
    "task": 2,
    "artifact": 3,
    "patch_intent": 3,
    "approval_decision": 3,
    "test_run": 3,
}

# Zoom level names
_ZOOM_NAMES = [
    "Origin",
    "Intent Path",
    "Work Path",
    "Proof Path",
    "Attention",
    "System Clusters",
    "Full Graph",
]

# Max visible nodes per zoom level
_MAX_NODES_PER_ZOOM = [1, 3, 8, 12, 18, 30, 999]

# ---------------------------------------------------------------------------
# Zone / cluster assignment
# ---------------------------------------------------------------------------

_ZONE_MAP: dict[str, str] = {
    "job": "origin",
    "task": "lifecycle",
    "artifact": "lifecycle",
    "patch_intent": "patches",
    "approval_decision": "patches",
    "patch_apply": "patches",
    "patch_apply_proof": "proofs",
    "test_run": "testing",
    "verification": "testing",
    "permission_blocker": "attention",
    "decision_queue": "attention",
    "run_event": "events",
    "agent_loop": "system",
    "context_budget": "system",
    "context_coverage": "system",
    "constitution": "system",
    "project_placeholder": "system",
    "memory_placeholder": "future",
    "mcp_placeholder": "future",
}

# ---------------------------------------------------------------------------
# Edge kind mapping — raw edge type → user-facing kind + meaning
# ---------------------------------------------------------------------------

_EDGE_KIND_MAP: dict[str, tuple[str, str]] = {
    "has_task": ("creates", "Job created this task"),
    "created_artifact": ("creates", "Task produced this artifact"),
    "emitted_event": ("caused", "Job emitted this event"),
    "produced_patch_intent": ("leads_to", "Artifact produced patch proposal"),
    "decided_by": ("requires_approval", "Patch requires approval decision"),
    "applied_by": ("applied_by", "Patch applied by this operation"),
    "verified_by": ("verified_by", "Task verified by this check"),
    "blocked_by": ("blocked_by", "Task blocked by this issue"),
    "inspected_by": ("informed_by", "Agent loop inspected this job"),
    "governed_by": ("belongs_to", "Job governed by constitution"),
    "future_memory_layer": ("remembers", "Future memory connection"),
    "future_mcp_layer": ("follows", "Future MCP connection"),
    "has_context_snapshot": ("informed_by", "Job has context snapshot"),
    "belongs_to_project": ("belongs_to", "Job belongs to project"),
    "has_test_run": ("verified_by", "Job has test run"),
    "verified_after_apply": ("proved_by", "Test verified after apply"),
    "approved_by": ("approved_by", "Patch approved by decision"),
    "has_decision_queue": ("leads_to", "Job has pending decisions"),
    "has_context_budget": ("informed_by", "Job has context budget"),
    "allowed_apply": ("approved_by", "Approval allowed this apply"),
    "recorded_proof": ("proved_by", "Apply recorded proof"),
    "proof_verified_by": ("verified_by", "Proof verified by test"),
    "informed_memory": ("remembers", "Proof informed memory"),
    "summarizes": ("informed_by", "Context summarizes job"),
    "continued_as": ("leads_to", "Origin continued as child"),
}


# ---------------------------------------------------------------------------
# Human-readable node labels — Step 105
# ---------------------------------------------------------------------------

_HUMAN_NODE_LABELS: dict[str, tuple[str, str]] = {
    "job": ("Goal", "The goal you asked Remedy to achieve"),
    "task": ("Task", "A step toward achieving the goal"),
    "artifact": ("Output", "Content produced by a task"),
    "patch_intent": ("Proposed change", "A code change proposal for review"),
    "approval_decision": ("Approval", "A human approval or rejection"),
    "patch_apply": ("Applied change", "A code change that was applied"),
    "patch_apply_proof": ("Proof", "Evidence that a change was applied correctly"),
    "test_run": ("Test result", "Result of running automated tests"),
    "verification": ("Verification", "Automated quality check result"),
    "permission_blocker": ("Needs permission", "Action blocked until permission is granted"),
    "decision_queue": ("Needs decision", "Something requires your attention"),
    "run_event": ("Event", "A logged event in the workflow"),
    "agent_loop": ("Agent cycle", "One cycle of the automation loop"),
    "context_budget": ("Context budget", "Token budget for this job"),
    "context_coverage": ("Context coverage", "How much context is available"),
    "constitution": ("Project rules", "Rules extracted from your project"),
    "project_placeholder": ("Project", "Project configuration"),
    "memory_placeholder": ("Memory", "Learned facts (future)"),
    "mcp_placeholder": ("Tool", "External tool integration (future)"),
}

# Zoom policy object — returned in view model for frontend contract
_ZOOM_POLICY = {
    "direction": "zoom_in_reveals_more",
    "zoom_out_reduces_complexity": True,
    "labels_follow_screen_space": True,
    "full_graph_requires_explicit_toggle": True,
}


def _importance(node_type: str, status: str | None, risk: str | None) -> float:
    """Compute 0-1 importance score for a node."""
    base = {
        "job": 1.0, "task": 0.8, "artifact": 0.6,
        "patch_intent": 0.5, "approval_decision": 0.5,
        "test_run": 0.7, "permission_blocker": 0.9,
        "decision_queue": 0.6, "verification": 0.4,
        "patch_apply": 0.4, "patch_apply_proof": 0.3,
    }.get(node_type, 0.2)
    if risk in ("high", "critical"):
        base = min(1.0, base + 0.2)
    if status in ("failed", "blocked"):
        base = min(1.0, base + 0.15)
    return round(base, 2)


def _is_primary_chain_node(node_type: str) -> bool:
    """Is this node on the primary workflow chain?"""
    return node_type in (
        "job", "task", "artifact", "patch_intent",
        "approval_decision", "patch_apply", "patch_apply_proof",
        "test_run", "verification",
    )


def _is_attention_node(node_type: str, status: str | None, risk: str | None) -> bool:
    """Does this node require user attention?"""
    if node_type in ("permission_blocker", "decision_queue"):
        return True
    if status in ("failed", "blocked"):
        return True
    if risk in ("high", "critical"):
        return True
    return False


def _short_label(label: str) -> str:
    """Truncate label for compact display."""
    if len(label) <= 24:
        return label
    return label[:22] + "..."


# ---------------------------------------------------------------------------
# ELK layout computation (server-side, deterministic)
# ---------------------------------------------------------------------------

def _compute_elk_positions(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, dict[str, float]]:
    """Compute deterministic ELK-layered positions.

    Uses rank-based placement since we can't run elkjs on the server.
    Same input graph always produces same positions.
    Direction: RIGHT (job at left, proof/test at right).
    """
    # Group nodes by rank
    rank_groups: dict[int, list[dict[str, Any]]] = {}
    for n in nodes:
        rank = n["rank"]
        rank_groups.setdefault(rank, []).append(n)

    # Sort nodes within each rank by type then id for determinism
    for rank in rank_groups:
        rank_groups[rank].sort(key=lambda n: (n["type"], n["id"]))

    positions: dict[str, dict[str, float]] = {}
    x_spacing = 220.0
    y_spacing = 80.0

    for rank, group in sorted(rank_groups.items()):
        x = rank * x_spacing
        total = len(group)
        y_start = -(total - 1) * y_spacing / 2
        for i, n in enumerate(group):
            positions[n["id"]] = {
                "x": round(x, 1),
                "y": round(y_start + i * y_spacing, 1),
            }

    return positions


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_brain_view_model(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the semantic zoom view-model with ELK directional layout."""
    from packages.orchestration.project_brain import build_project_brain

    graph = build_project_brain(job, events)
    focus_job_id = str(job.id)

    # Build node list with rank/zone/zoom assignments
    raw_nodes = []
    for node in graph.nodes:
        ntype = node.type
        rank = _RANK_MAP.get(ntype, 7)
        zoom = _ZOOM_MAP.get(ntype, 6)
        label_zoom = _LABEL_ZOOM.get(ntype, zoom + 1)

        # Only the focus job is origin; child/continuation jobs are demoted
        is_origin = (ntype == "job" and node.id == focus_job_id)
        if ntype == "job" and node.id != focus_job_id:
            zoom = max(zoom, 5)  # push child jobs to System level
            label_zoom = max(label_zoom, 5)

        raw_nodes.append({
            "id": node.id,
            "type": ntype,
            "kind": _HUMAN_NODE_LABELS.get(ntype, (ntype.replace("_", " "), ""))[0],
            "user_title": _HUMAN_NODE_LABELS.get(ntype, (ntype.replace("_", " "), ""))[0],
            "user_kind": _HUMAN_NODE_LABELS.get(ntype, (ntype.replace("_", " "), ""))[1],
            "label_short": _short_label(node.label),
            "label_full": node.label,
            "layer": zoom,
            "rank": rank,
            "zone": _ZONE_MAP.get(ntype, "other"),
            "importance": _importance(ntype, node.status, node.risk),
            "status": node.status,
            "risk": node.risk,
            "cluster_id": _ZONE_MAP.get(ntype, "other"),
            "visible_from_zoom": zoom,
            "show_label_from_zoom": min(label_zoom, 6),
            "is_origin": is_origin,
            "is_primary_chain": _is_primary_chain_node(ntype),
            "is_attention": _is_attention_node(ntype, node.status, node.risk),
        })

    # Compute ELK-style positions
    positions = _compute_elk_positions(raw_nodes, [])
    for n in raw_nodes:
        pos = positions.get(n["id"], {"x": 0.0, "y": 0.0})
        n["x"] = pos["x"]
        n["y"] = pos["y"]
        n["width"] = 28
        n["height"] = 28

    # Enforce max visible nodes per zoom level
    # Sort by importance descending, then assign visibility
    sorted_by_importance = sorted(raw_nodes, key=lambda n: -n["importance"])
    for level in range(7):
        max_at_level = _MAX_NODES_PER_ZOOM[level]
        visible_at_level = [n for n in sorted_by_importance if n["visible_from_zoom"] <= level]
        if len(visible_at_level) > max_at_level:
            # Push excess nodes to next zoom level
            for excess in visible_at_level[max_at_level:]:
                if excess["visible_from_zoom"] == level:
                    excess["visible_from_zoom"] = min(level + 1, 6)

    # Build edge list with user-facing kinds
    node_map = {n["id"]: n for n in raw_nodes}
    edge_list = []
    for edge in graph.edges:
        kind_info = _EDGE_KIND_MAP.get(edge.type, ("follows", "Connected"))
        kind, meaning = kind_info
        src = node_map.get(edge.source)
        tgt = node_map.get(edge.target)
        src_zoom = src["visible_from_zoom"] if src else 6
        tgt_zoom = tgt["visible_from_zoom"] if tgt else 6
        is_primary = (
            src is not None and tgt is not None
            and src.get("is_primary_chain") and tgt.get("is_primary_chain")
        )
        edge_list.append({
            "source": edge.source,
            "target": edge.target,
            "kind": kind,
            "label": meaning,
            "meaning": meaning,
            "visible_from_zoom": max(src_zoom, tgt_zoom),
            "is_primary_chain": is_primary,
            "strength": 1.0 if is_primary else 0.5,
            "direction": "forward",
        })

    # Build clusters
    cluster_map: dict[str, list[str]] = {}
    for n in raw_nodes:
        cluster_map.setdefault(n["cluster_id"], []).append(n["id"])

    clusters = [
        {"id": cid, "node_ids": nids, "count": len(nids)}
        for cid, nids in sorted(cluster_map.items())
    ]

    # Zoom level info
    zoom_levels = []
    for level in range(7):
        visible = [n for n in raw_nodes if n["visible_from_zoom"] <= level]
        zoom_levels.append({
            "level": level,
            "name": _ZOOM_NAMES[level],
            "max_nodes": _MAX_NODES_PER_ZOOM[level],
            "visible_count": len(visible),
        })

    # visible_counts_by_zoom — monotonic non-decreasing (Step 102 contract)
    visible_counts_by_zoom = [zl["visible_count"] for zl in zoom_levels]

    # visible_node_ids_by_zoom — Step 113: subset monotonicity proof
    visible_node_ids_by_zoom: list[list[str]] = []
    for level in range(7):
        ids = sorted(n["id"] for n in raw_nodes if n["visible_from_zoom"] <= level)
        visible_node_ids_by_zoom.append(ids)

    # label_counts_by_zoom — how many labels visible at each level
    label_counts_by_zoom: list[int] = []
    for level in range(7):
        count = sum(1 for n in raw_nodes if n["show_label_from_zoom"] <= level)
        label_counts_by_zoom.append(count)

    # Edge flow_role enrichment — Step 114
    for n in raw_nodes:
        ntype = n["type"]
        nstatus = n.get("status")
        if ntype == "job":
            n["flow_role"] = "origin" if n["is_origin"] else "continuation"
        elif ntype == "task":
            if nstatus == "completed":
                n["flow_role"] = "task_completed"
            elif nstatus in ("running", "active"):
                n["flow_role"] = "task_active"
            else:
                n["flow_role"] = "task_future"
        elif ntype in ("artifact",):
            n["flow_role"] = "artifact"
        elif ntype in ("patch_intent",):
            n["flow_role"] = "change"
        elif ntype in ("approval_decision",):
            n["flow_role"] = "approval"
        elif ntype in ("patch_apply",):
            n["flow_role"] = "apply"
        elif ntype in ("patch_apply_proof",):
            n["flow_role"] = "proof"
        elif ntype in ("test_run", "verification"):
            n["flow_role"] = "test"
        elif ntype in ("decision_queue",):
            n["flow_role"] = "decision"
        elif ntype in ("memory_placeholder",):
            n["flow_role"] = "memory"
        elif ntype in ("permission_blocker",):
            n["flow_role"] = "decision"
        else:
            n["flow_role"] = "system"
        # lane = rank for simplicity
        n["lane"] = n["rank"]

    # Edge enrichment — Step 114
    for e in edge_list:
        src = node_map.get(e["source"])
        tgt = node_map.get(e["target"])
        e["source_rank"] = src["rank"] if src else 0
        e["target_rank"] = tgt["rank"] if tgt else 0
        e["primary_path"] = e["is_primary_chain"]

    return {
        "version": 4,
        "job_id": str(job.id),
        "layout_engine": "elk-layered",
        "direction": "RIGHT",
        "origin": str(job.id),
        "total_nodes": len(raw_nodes),
        "total_edges": len(edge_list),
        "default_zoom_level": 0,
        "max_initial_nodes": 1,
        "advanced_full_graph_available": True,
        "full_graph_requires_explicit_toggle": True,
        "zoom_policy": _ZOOM_POLICY,
        "visible_counts_by_zoom": visible_counts_by_zoom,
        "visible_node_ids_by_zoom": visible_node_ids_by_zoom,
        "label_counts_by_zoom": label_counts_by_zoom,
        "layers": [
            {"level": i, "name": _ZOOM_NAMES[i], "node_count": zoom_levels[i]["visible_count"]}
            for i in range(7)
        ],
        "zoom_levels": zoom_levels,
        "nodes": raw_nodes,
        "edges": edge_list,
        "clusters": clusters,
    }


def build_node_detail(job: Any, events: list[dict[str, Any]], node_id: str) -> dict[str, Any]:
    """Build compact node detail for the floating card."""
    from packages.orchestration.brain_detail import (
        build_brain_node_detail,
        export_brain_node_detail_json,
    )
    from packages.orchestration.project_brain import build_project_brain

    graph = build_project_brain(job, events)

    target = None
    for node in graph.nodes:
        if node.id == node_id:
            target = node
            break

    if target is None:
        return {"error": "node not found", "node_id": node_id}

    try:
        detail = build_brain_node_detail(job, graph, node_id, events)
        detail_json = export_brain_node_detail_json(detail)
    except (ValueError, KeyError):
        detail_json = {}

    # Plain-language status
    status_text = ""
    if target.status:
        status_map = {
            "active": "Currently running",
            "completed": "Completed successfully",
            "failed": "Failed — needs attention",
            "blocked": "Blocked — waiting for action",
            "pending": "Waiting to start",
        }
        status_text = status_map.get(target.status, target.status)

    result: dict[str, Any] = {
        "version": 2,
        "job_id": str(job.id),
        "node_id": node_id,
        "title": target.label,
        "status": target.status or "",
        "status_text": status_text,
        "why_this_matters": detail_json.get("meaning", ""),
        "evidence_summary": detail_json.get("evidence", [])[:3],
        "next_safe_action": "",
        "copy_command": "",
        "advanced": {
            "node_type": target.type,
            "node_id": node_id,
            "risk": target.risk,
            "zone": _ZONE_MAP.get(target.type, "other"),
            "rank": _RANK_MAP.get(target.type, 7),
            "importance": _importance(target.type, target.status, target.risk),
        },
    }
    actions = detail_json.get("next_actions", [])
    if actions:
        result["next_safe_action"] = str(actions[0])
    commands = detail_json.get("commands", [])
    if commands:
        result["copy_command"] = str(commands[0])
    return result


def build_task_progress(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build task progress ribbon data — Step 104."""
    from packages.core.models import RunState

    tasks = []
    for i, task in enumerate(job.tasks):
        status_val = task.status
        if hasattr(status_val, "value"):
            status_val = status_val.value

        # Determine verified status from events
        verified = False
        for e in events:
            if e.get("event") == "task_run_completed" and e.get("task_id") == str(task.id):
                verified = True
                break

        # Determine source — check metadata (legacy) or inputs dict
        source = "planner"
        meta = getattr(task, "metadata", None) or getattr(task, "inputs", None) or {}
        if isinstance(meta, dict):
            source = meta.get("source", "planner")

        # Status mapping
        if status_val == "completed":
            ribbon_status = "completed"
        elif status_val == "running":
            ribbon_status = "active"
        elif status_val == "pending":
            ribbon_status = "pending"
        elif status_val == "failed":
            ribbon_status = "active"  # show as needs attention
        else:
            ribbon_status = "future"

        # Reviewer-suggested tasks
        if source == "reviewer" and status_val == "pending":
            ribbon_status = "reviewer-suggested"

        # Proof/test status from events
        proof_status = "none"
        test_status = "none"
        for e in events:
            eid = e.get("task_id") or e.get("metadata", {}).get("task_id", "")
            if eid == str(task.id):
                if e.get("event") == "proof_collected":
                    proof_status = "collected"
                elif e.get("event") == "test_run_completed":
                    exit_code = e.get("metadata", {}).get("exit_code")
                    test_status = "pass" if exit_code == 0 else "fail"

        is_current = ribbon_status == "active"
        is_future = ribbon_status in ("future", "pending")
        is_reviewer = source == "reviewer"

        task_entry = {
            "id": str(task.id),
            "title": _short_label(task.task_type if hasattr(task, "task_type") else str(task.id)[:8]),
            "status": ribbon_status,
            "verified": verified,
            "source": source,
            "accepted": ribbon_status != "reviewer-suggested",
            "rank": i + 1,
            "related_node_id": str(task.id),
            "short_reason": "",
            "proof_status": proof_status,
            "test_status": test_status,
            "is_current": is_current,
            "is_future": is_future,
            "is_reviewer_suggested": is_reviewer,
        }
        tasks.append(task_entry)

    return {
        "version": 1,
        "job_id": str(job.id),
        "tasks": tasks,
    }


def build_next_action(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build next-action suggestion grounded in actual job state."""
    from packages.core.models import RunState

    state = job.state.value if hasattr(job.state, "value") else str(job.state)
    job_id = str(job.id)

    # Scan for pending approvals
    has_pending_approval = False
    for art in job.artifacts:
        meta = art.metadata or {}
        for intent in meta.get("patch_intent_explanations", []):
            if intent.get("approval_state") == "pending":
                has_pending_approval = True
                break

    # Scan for failed tests
    has_failed_test = False
    for e in reversed(events):
        if e.get("event") == "test_run_completed":
            if e.get("metadata", {}).get("exit_code") != 0:
                has_failed_test = True
            break

    # Scan for blockers
    has_blocker = any(
        e.get("event") == "stop_reason_recorded" and e.get("outcome") != "resolved"
        for e in events
    )

    # Scan for reviewer suggestions
    has_reviewer_suggestion = any(
        (getattr(t, "metadata", None) or getattr(t, "inputs", None) or {}).get("source") == "reviewer"
        and (t.status.value if hasattr(t.status, "value") else str(t.status)) == "pending"
        for t in job.tasks
    )

    # Determine primary action
    primary: dict[str, Any]
    if has_blocker:
        primary = {
            "label": "Resolve blocker",
            "command": f"remedy blocker list {job_id} --json",
            "risk": "low",
            "requires_human": True,
        }
    elif has_pending_approval:
        primary = {
            "label": "Review pending patch",
            "command": f"remedy patch list {job_id} --json",
            "risk": "medium",
            "requires_human": True,
        }
    elif has_reviewer_suggestion:
        primary = {
            "label": "Review suggested tasks",
            "command": f"remedy review list {job_id} --json",
            "risk": "low",
            "requires_human": True,
        }
    elif has_failed_test:
        primary = {
            "label": "Inspect test failure",
            "command": f"remedy test list {job_id} --json",
            "risk": "low",
            "requires_human": True,
        }
    elif state in ("active", "running"):
        primary = {
            "label": "Open UI to monitor progress",
            "command": f"remedy ui {job_id}",
            "risk": "low",
            "requires_human": False,
        }
    elif state == "completed":
        primary = {
            "label": "No action needed",
            "command": "",
            "risk": "low",
            "requires_human": False,
        }
    else:
        primary = {
            "label": "Open UI",
            "command": f"remedy ui {job_id}",
            "risk": "low",
            "requires_human": False,
        }

    # Secondary actions
    secondary = []
    if state != "completed":
        secondary.append({
            "label": "Open UI",
            "command": f"remedy ui {job_id}",
            "risk": "low",
            "requires_human": False,
        })
    secondary.append({
        "label": "Free VRAM",
        "command": "remedy worker unload --all",
        "risk": "low",
        "requires_human": False,
    })

    return {
        "version": 1,
        "job_id": job_id,
        "stage": state,
        "primary_action": primary,
        "secondary_actions": secondary,
    }


# ---------------------------------------------------------------------------
# Step 164 — Human Story ViewModel
# ---------------------------------------------------------------------------


def build_story(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build human-facing story model — Step 164.

    Returns headline, plain status, progress, journey items.
    No debug words (rank, importance, node_type, zone, etc.).
    """
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.ui_copy import (
        human_label,
        human_state,
        human_subtitle,
        is_default_visible,
        journey_kind,
    )

    graph = build_project_brain(job, events)
    state = job.state.value if hasattr(job.state, "value") else str(job.state)

    # Progress counts
    completed = 0
    active = 0
    pending = 0
    blocked = 0
    needs_review = 0
    for node in graph.nodes:
        if not is_default_visible(node.type):
            continue
        s = node.status or ""
        if s in ("completed", "passed", "approved"):
            completed += 1
        elif s in ("running", "active"):
            active += 1
        elif s in ("blocked", "failed"):
            blocked += 1
        elif s in ("needs_decision", "needs_approval"):
            needs_review += 1
        elif s == "pending":
            pending += 1

    # Headline
    job_name = job.name if len(job.name) <= 60 else job.name[:57] + "..."
    headline = f"{job_name}"
    plain_status = human_state(state)

    # Primary next action
    next_action_data = build_next_action(job, events)
    primary_next_action = next_action_data.get("primary_action", {})

    # Journey items — only default-visible nodes, ranked left-to-right
    journey: list[dict[str, Any]] = []
    for node in graph.nodes:
        if not is_default_visible(node.type):
            continue
        s = node.status or ""
        if s in ("completed", "passed", "approved"):
            j_state = "done"
        elif s in ("running", "active"):
            j_state = "current"
        elif s in ("blocked", "failed"):
            j_state = "blocked"
        elif s in ("needs_decision", "needs_approval"):
            j_state = "current"
        else:
            j_state = "pending"

        title = human_label(node.type)
        # Use node label if it's not just the type name
        label = node.label[:60] if node.label else title
        if label == node.type or label == node.id:
            label = title

        journey.append({
            "id": node.id,
            "kind": journey_kind(node.type),
            "title": title,
            "subtitle": label if label != title else human_subtitle(node.type),
            "state": j_state,
            "node_id": node.id,
            "visible_from_zoom": _ZOOM_MAP.get(node.type, 6),
        })

    # Sort journey by rank
    rank_order = {
        "goal": 0, "task": 1, "change": 2, "approval": 3,
        "apply": 4, "test": 5, "proof": 6, "review": 7,
        "memory": 8, "decision": 9,
    }
    journey.sort(key=lambda j: (rank_order.get(j["kind"], 99), j["id"]))

    return {
        "version": 1,
        "job_id": str(job.id),
        "headline": headline,
        "plain_status": plain_status,
        "primary_next_action": primary_next_action,
        "progress": {
            "completed": completed,
            "active": active,
            "pending": pending,
            "blocked": blocked,
            "needs_review": needs_review,
        },
        "journey": journey,
    }


# ---------------------------------------------------------------------------
# Step 165 — Human-Only Node Detail
# ---------------------------------------------------------------------------


def build_human_node_detail(
    job: Any, events: list[dict[str, Any]], node_id: str,
) -> dict[str, Any]:
    """Build human-only node detail — Step 165.

    No rank, importance, node_type, zone, present/missing signals,
    metadata, connected_to, edge_type in default output.
    Advanced available separately via debug-detail.
    """
    from packages.orchestration.brain_detail import (
        build_brain_node_detail,
        export_brain_node_detail_json,
    )
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.ui_copy import human_label, human_state, human_subtitle

    graph = build_project_brain(job, events)
    target = None
    for node in graph.nodes:
        if node.id == node_id:
            target = node
            break
    if target is None:
        return {"error": "node not found", "node_id": node_id}

    try:
        detail = build_brain_node_detail(job, graph, node_id, events)
        detail_json = export_brain_node_detail_json(detail)
    except (ValueError, KeyError):
        detail_json = {}

    title = human_label(target.type)
    label = target.label[:60] if target.label else title
    if label != title and label != target.type:
        title = label

    # What happened timeline
    what_happened: list[str] = []
    for item in detail_json.get("why_it_exists", []):
        what_happened.append(str(item))

    # Evidence (safe summaries only)
    evidence: list[str] = []
    for item in detail_json.get("evidence", []):
        s = str(item)
        # Strip internal key-value pairs that expose debug info
        if ":" in s and s.split(":")[0].strip() in (
            "status", "kind", "owner", "passed", "outcome",
        ):
            evidence.append(s)

    # Next action
    next_action: dict[str, Any] = {}
    actions = detail_json.get("next_actions", [])
    if actions:
        next_action = {
            "label": str(actions[0]),
            "command": str(actions[0]) if "remedy" in str(actions[0]) else "",
        }

    return {
        "version": 3,
        "job_id": str(job.id),
        "node_id": node_id,
        "title": title,
        "state": human_state(target.status),
        "summary": detail_json.get("explanation", human_subtitle(target.type)),
        "why_it_matters": human_subtitle(target.type),
        "what_happened": what_happened[:5],
        "evidence": evidence[:5],
        "next_action": next_action,
        "advanced_available": True,
    }


# ---------------------------------------------------------------------------
# Step 167 — Diagnostics Layers
# ---------------------------------------------------------------------------


def build_layers() -> dict[str, Any]:
    """Return layer definitions — Step 167."""
    from packages.orchestration.ui_copy import LAYERS
    return {
        "version": 1,
        "layers": LAYERS,
    }


def build_diagnostics_nodes(
    job: Any, events: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return diagnostics-only nodes — Step 167."""
    from packages.orchestration.project_brain import build_project_brain
    from packages.orchestration.ui_copy import human_label, is_diagnostics_only

    graph = build_project_brain(job, events)
    diag_nodes = []
    for node in graph.nodes:
        if is_diagnostics_only(node.type):
            diag_nodes.append({
                "id": node.id,
                "title": human_label(node.type),
                "type": node.type,
                "status": node.status or "",
            })
    return {
        "version": 1,
        "job_id": str(job.id),
        "layer": "diagnostics",
        "nodes": diag_nodes,
    }


# ---------------------------------------------------------------------------
# Step 168 — Task Ribbon Checklist
# ---------------------------------------------------------------------------


def build_checklist(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build task ribbon checklist — Step 168.

    Human-readable labels, no bare UUIDs, proper states.
    """
    from packages.orchestration.ui_copy import human_label, human_state, journey_kind

    items: list[dict[str, Any]] = []

    # Goal item
    job_name = job.name if len(job.name) <= 60 else job.name[:57] + "..."
    state_val = job.state.value if hasattr(job.state, "value") else str(job.state)
    items.append({
        "id": str(job.id),
        "label": job_name,
        "state": "done" if state_val == "completed" else "current",
        "kind": "goal",
        "checked": state_val == "completed",
        "muted": False,
        "node_id": str(job.id),
        "next_action": {},
    })

    # Task items
    for task in job.tasks:
        t_status = task.status.value if hasattr(task.status, "value") else str(task.status)
        desc = task.description if len(task.description) <= 50 else task.description[:47] + "..."

        if t_status == "completed":
            cl_state = "done"
            checked = True
        elif t_status in ("running", "active"):
            cl_state = "current"
            checked = False
        elif t_status in ("blocked", "failed"):
            cl_state = "blocked"
            checked = False
        else:
            cl_state = "pending"
            checked = False

        # Reviewer-suggested?
        source = (getattr(task, "inputs", None) or {}).get("source", "planner")
        if source == "reviewer" and t_status == "pending":
            cl_state = "suggested"

        items.append({
            "id": str(task.id),
            "label": desc if desc and desc != str(task.id) else human_label("task"),
            "state": cl_state,
            "kind": "task",
            "checked": checked,
            "muted": cl_state in ("pending", "suggested"),
            "node_id": str(task.id),
            "next_action": {},
        })

    # Patch intents / approvals from events
    for e in events:
        etype = e.get("event", "")
        if etype == "structured_patch_intent_created":
            items.append({
                "id": f"change-{len(items)}",
                "label": "Proposed change",
                "state": "done",
                "kind": "change",
                "checked": True,
                "muted": False,
                "node_id": "",
                "next_action": {},
            })
        elif etype == "source_patch_applied":
            items.append({
                "id": f"apply-{len(items)}",
                "label": "Applied change",
                "state": "done",
                "kind": "apply",
                "checked": True,
                "muted": False,
                "node_id": "",
                "next_action": {},
            })
        elif etype == "test_run_completed":
            meta = e.get("metadata", {})
            passed = meta.get("exit_code") == 0 or meta.get("passed")
            items.append({
                "id": f"test-{len(items)}",
                "label": "Tests passed" if passed else "Tests failed",
                "state": "done" if passed else "blocked",
                "kind": "test",
                "checked": bool(passed),
                "muted": False,
                "node_id": "",
                "next_action": {},
            })
        elif etype == "proof_collected":
            items.append({
                "id": f"proof-{len(items)}",
                "label": "Proof collected",
                "state": "done",
                "kind": "proof",
                "checked": True,
                "muted": False,
                "node_id": "",
                "next_action": {},
            })

    # Memory candidates from job metadata
    candidates = (job.metadata or {}).get("memory_candidates", [])
    for c in candidates:
        items.append({
            "id": c.get("id", f"mem-{len(items)}"),
            "label": f"Memory: {c.get('safe_summary', 'candidate')[:40]}",
            "state": "current" if c.get("status") == "pending" else "done",
            "kind": "memory",
            "checked": c.get("status") in ("approved", "rejected"),
            "muted": c.get("status") != "pending",
            "node_id": "",
            "next_action": {
                "label": "Review candidate",
                "command": f"remedy memory candidates {str(job.id)[:8]}",
            } if c.get("status") == "pending" else {},
        })

    # Reviewer recommendations
    recs = (job.metadata or {}).get("reviewer_recommendations", [])
    for r in recs:
        items.append({
            "id": r.get("id", f"review-{len(items)}"),
            "label": f"Review: {r.get('safe_summary', 'suggestion')[:40]}",
            "state": "suggested" if r.get("status") == "pending" else "done",
            "kind": "review",
            "checked": r.get("status") in ("accepted", "rejected"),
            "muted": r.get("status") != "pending",
            "node_id": "",
            "next_action": {},
        })

    return {
        "version": 1,
        "job_id": str(job.id),
        "items": items,
    }
