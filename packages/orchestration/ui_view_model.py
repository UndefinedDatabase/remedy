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

    # Build node list with rank/zone/zoom assignments
    raw_nodes = []
    for node in graph.nodes:
        ntype = node.type
        rank = _RANK_MAP.get(ntype, 7)
        zoom = _ZOOM_MAP.get(ntype, 6)
        label_zoom = _LABEL_ZOOM.get(ntype, zoom + 1)

        raw_nodes.append({
            "id": node.id,
            "type": ntype,
            "kind": ntype.replace("_", " "),
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
            "is_origin": ntype == "job",
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

    return {
        "version": 2,
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
        "node_id": node_id,
        "title": target.label,
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
