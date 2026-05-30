"""
UI View Model — semantic zoom layering for the PixiJS brain canvas.

Transforms the raw ProjectBrainGraph into a view-model with zoom layers,
visibility thresholds, positions, and importance scores.

Zoom levels (0-5):
  0 — Origin:        just the job node
  1 — Core lifecycle: tasks, artifacts
  2 — Attention:      blockers, decisions, approvals, test runs
  3 — Evidence:       patch intents, proofs, verifications
  4 — System map:     context budget, constitution, agent loops
  5 — Full graph:     all nodes including placeholders

Public API::

    build_brain_view_model(job, events) -> dict
    build_node_detail(job, events, node_id) -> dict
"""

from __future__ import annotations

import hashlib
import math
from typing import Any

# Node type → zoom layer assignment
_LAYER_MAP: dict[str, int] = {
    "job": 0,
    "task": 1,
    "artifact": 1,
    "patch_intent": 2,
    "approval_decision": 2,
    "test_run": 2,
    "permission_blocker": 2,
    "decision_queue": 2,
    "verification": 3,
    "patch_apply": 3,
    "patch_apply_proof": 3,
    "run_event": 3,
    "context_budget": 4,
    "context_coverage": 4,
    "constitution": 4,
    "agent_loop": 4,
    "project_placeholder": 4,
    "memory_placeholder": 5,
    "mcp_placeholder": 5,
}

# Layer labels for the UI
_LAYER_NAMES = [
    "Origin",
    "Core Lifecycle",
    "Attention",
    "Evidence",
    "System Map",
    "Full Graph",
]

# When to show labels (zoom level at which text appears)
_LABEL_ZOOM: dict[str, int] = {
    "job": 0,
    "task": 2,
    "artifact": 2,
    "patch_intent": 3,
    "approval_decision": 3,
    "test_run": 3,
}


def _importance(node_type: str, status: str | None, risk: str | None) -> float:
    """Compute 0-1 importance score for a node."""
    base = {
        "job": 1.0,
        "task": 0.8,
        "artifact": 0.6,
        "patch_intent": 0.5,
        "approval_decision": 0.5,
        "test_run": 0.7,
        "permission_blocker": 0.9,
        "decision_queue": 0.6,
        "verification": 0.4,
        "patch_apply": 0.4,
        "patch_apply_proof": 0.3,
    }.get(node_type, 0.2)
    if risk in ("high", "critical"):
        base = min(1.0, base + 0.2)
    if status in ("failed", "blocked"):
        base = min(1.0, base + 0.15)
    return round(base, 2)


def _deterministic_position(node_id: str, node_type: str, layer: int, index: int, total_in_layer: int) -> dict[str, float]:
    """Generate deterministic x/y position based on layer ring layout."""
    if layer == 0:
        return {"x": 0.0, "y": 0.0}
    # Ring layout — each layer gets a ring at increasing radius
    radius = 120.0 + layer * 100.0
    # Use hash for stable angle offset
    h = int(hashlib.md5(node_id.encode()).hexdigest()[:8], 16)
    angle_offset = (h % 1000) / 1000.0 * 0.3
    if total_in_layer > 0:
        angle = (2 * math.pi * index / total_in_layer) + angle_offset
    else:
        angle = 0.0
    return {
        "x": round(radius * math.cos(angle), 1),
        "y": round(radius * math.sin(angle), 1),
    }


def _cluster_id(node_type: str) -> str:
    """Assign cluster grouping."""
    clusters = {
        "job": "origin",
        "task": "lifecycle",
        "artifact": "lifecycle",
        "patch_intent": "patches",
        "approval_decision": "patches",
        "patch_apply": "patches",
        "patch_apply_proof": "patches",
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
    }
    return clusters.get(node_type, "other")


def build_brain_view_model(job: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the semantic zoom view-model for the PixiJS brain canvas."""
    from packages.orchestration.project_brain import (
        build_project_brain,
        export_project_brain_json,
    )

    graph = build_project_brain(job, events)

    # Group nodes by layer for position calculation
    layer_groups: dict[int, list[Any]] = {}
    for node in graph.nodes:
        layer = _LAYER_MAP.get(node.type, 5)
        layer_groups.setdefault(layer, []).append(node)

    nodes = []
    for node in graph.nodes:
        layer = _LAYER_MAP.get(node.type, 5)
        group = layer_groups.get(layer, [])
        idx = next(i for i, n in enumerate(group) if n.id == node.id)
        pos = _deterministic_position(node.id, node.type, layer, idx, len(group))
        imp = _importance(node.type, node.status, node.risk)
        label_zoom = _LABEL_ZOOM.get(node.type, layer + 1)

        nodes.append({
            "id": node.id,
            "type": node.type,
            "label": node.label,
            "status": node.status,
            "risk": node.risk,
            "layer": layer,
            "visible_from_zoom": layer,
            "show_label_from_zoom": min(label_zoom, 5),
            "importance": imp,
            "cluster_id": _cluster_id(node.type),
            "position": pos,
        })

    edges = []
    for edge in graph.edges:
        # Edge visible when both endpoints visible
        src_layer = 5
        tgt_layer = 5
        for n in nodes:
            if n["id"] == edge.source:
                src_layer = n["layer"]
            if n["id"] == edge.target:
                tgt_layer = n["layer"]
        edges.append({
            "source": edge.source,
            "target": edge.target,
            "type": edge.type,
            "visible_from_zoom": max(src_layer, tgt_layer),
        })

    return {
        "version": 1,
        "job_id": str(job.id),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "layers": [
            {"level": i, "name": _LAYER_NAMES[i], "node_count": len(layer_groups.get(i, []))}
            for i in range(6)
        ],
        "nodes": nodes,
        "edges": edges,
    }


def build_node_detail(job: Any, events: list[dict[str, Any]], node_id: str) -> dict[str, Any]:
    """Build compact node detail for the floating card."""
    from packages.orchestration.brain_detail import (
        build_brain_node_detail,
        export_brain_node_detail_json,
    )
    from packages.orchestration.project_brain import build_project_brain

    graph = build_project_brain(job, events)

    # Find node in graph
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

    # Build compact card data
    return {
        "version": 1,
        "node_id": node_id,
        "type": target.type,
        "label": target.label,
        "status": target.status,
        "risk": target.risk,
        "layer": _LAYER_MAP.get(target.type, 5),
        "importance": _importance(target.type, target.status, target.risk),
        "cluster": _cluster_id(target.type),
        "meaning": detail_json.get("meaning", ""),
        "why_it_exists": detail_json.get("why_it_exists", ""),
        "evidence": detail_json.get("evidence", []),
        "next_actions": detail_json.get("next_actions", []),
        "commands": detail_json.get("commands", []),
        "advanced": {
            k: v for k, v in detail_json.items()
            if k not in ("meaning", "why_it_exists", "evidence", "next_actions", "commands",
                         "title", "id", "type", "status", "risk")
        },
    }
