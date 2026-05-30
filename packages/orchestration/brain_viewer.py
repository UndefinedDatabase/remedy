"""
Brain Viewer (Legacy/Static) — static HTML snapshot export for the Project Brain Graph.

**Status: Legacy.** The primary interactive experience is now ``remedy ui start``
which serves the PixiJS-based semantic brain canvas at localhost.  This module
remains available as a static snapshot/export tool via ``remedy brain view``.

Generates a self-contained index.html (with embedded viewer data) under
REMEDY_DATA_DIR/viewers/<job_id>/.  The viewer consumes only the existing
--json machine contracts (export_project_brain_json and
export_brain_node_detail_json) and renders nodes/edges in a 2D visual.

Scope limitations:
  Read-only only.  No repo mutation, no patch apply, no permission mutation,
  no shell/subprocess/Git/Docker/network/MCP/Claude execution, no memory
  writes, no frontend framework.

Redaction policy:
  Same as brain_detail.py — no artifact content, diff previews, approval
  reasons, event messages, or raw command output in any generated file.

Public API::

    build_brain_viewer_data(job, graph, events) -> BrainViewerData
    export_brain_viewer_json(data) -> dict[str, Any]
    write_brain_viewer_files(data, out_dir: Path) -> Path
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from html import escape as _html_esc
from pathlib import Path
from typing import Any

from packages.core.models import Job
from packages.orchestration.brain_detail import (
    build_brain_node_detail,
    export_brain_node_detail_json,
)
from packages.orchestration.project_brain import (
    ProjectBrainGraph,
    export_project_brain_json,
)


# ---------------------------------------------------------------------------
# Semantic zone layout — maps node types to zones and radial layers
# ---------------------------------------------------------------------------

_ZONE_MAP: dict[str, str] = {
    "job": "intent",
    "task": "plan",
    "artifact": "artifact",
    "constitution": "policy",
    "context_coverage": "policy",
    "run_event": "event",
    "agent_loop": "event",
    "event_ledger": "event",
    "patch_intent": "artifact",
    "approval_decision": "approval",
    "patch_apply": "approval",
    "patch_apply_proof": "proof",
    "verification": "proof",
    "test_run": "proof",
    "permission_blocker": "decision",
    "stop_reason": "decision",
    "decision_queue": "decision",
    "memory_placeholder": "memory",
    "memory": "memory",
    "mcp_placeholder": "future",
    "project_placeholder": "intent",
    "autonomy_readiness": "policy",
    "context_pack": "policy",
    "context_budget": "policy",
    "run_contract": "policy",
    "token_policy": "policy",
    "worker_adapter": "policy",
    "git_status": "repo",
    "change_set": "repo",
    "patch_revert": "repo",
    "guidance_summary": "intent",
}

_LAYER_MAP: dict[str, int] = {
    "job": 0,
    "constitution": 1,
    "task": 1,
    "context_coverage": 1,
    "artifact": 2,
    "run_event": 2,
    "agent_loop": 2,
    "patch_intent": 3,
    "approval_decision": 3,
    "verification": 3,
    "permission_blocker": 3,
    "memory_placeholder": 4,
    "memory": 4,
    "mcp_placeholder": 4,
    "project_placeholder": 1,
    "patch_apply": 4,
    "autonomy_readiness": 1,
    "context_pack": 2,
    "event_ledger": 2,
    "stop_reason": 3,
    "decision_queue": 3,
    "context_budget": 2,
    "run_contract": 1,
    "token_policy": 1,
    "worker_adapter": 2,
    "git_status": 2,
    "change_set": 3,
    "patch_revert": 3,
    "patch_apply_proof": 4,
    "test_run": 4,
    "guidance_summary": 1,
}

# Zone angle offsets — each zone gets a sector of the circle
_ZONE_ANGLES: dict[str, float] = {
    "intent": 0.0,
    "plan": 0.4,
    "artifact": 0.8,
    "approval": 1.2,
    "proof": 1.6,
    "event": 2.0,
    "policy": 2.8,
    "decision": 3.6,
    "memory": 4.0,
    "repo": 4.8,
    "future": 5.4,
}

_LAYER_RADIUS = [0.0, 150.0, 290.0, 420.0, 530.0]
_CX = 500.0
_CY = 350.0


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BrainViewerData:
    """Immutable bundle of all data required to render a Brain Viewer page."""

    job_id: str
    generated_at: str
    graph: dict[str, Any]
    node_details: dict[str, dict[str, Any]]
    positions: dict[str, list[float]]
    detail_fallback_count: int = 0


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------


def build_brain_viewer_data(
    job: Job,
    graph: ProjectBrainGraph,
    events: list[dict[str, Any]],
) -> BrainViewerData:
    """Build read-only viewer data from job, graph, and run-log events.

    Deterministic — no LLM calls, no external processes, no repo access.
    Redaction: same policy as brain_detail — no raw content, no approval
    reasons, no diff previews, no event messages, no command output.
    """
    graph_dict = export_project_brain_json(graph)

    # Inject zone metadata into each node
    for node in graph_dict["nodes"]:
        node["zone"] = _ZONE_MAP.get(node["type"], "future")

    node_details: dict[str, dict[str, Any]] = {}
    detail_fallback_count = 0
    for node in graph.nodes:
        try:
            detail = build_brain_node_detail(job, graph, node.id, events)
            node_details[node.id] = export_brain_node_detail_json(detail)
        except (KeyError, ValueError, AttributeError, TypeError, RuntimeError, OSError):
            detail_fallback_count += 1
            node_details[node.id] = {
                "job_id": str(job.id),
                "node_id": node.id,
                "node_type": node.type,
                "title": node.label[:80],
                "status": node.status or "unknown",
                "risk": node.risk,
                "explanation": f"Detail unavailable for node '{node.type}'.",
                "why_it_exists": [],
                "connected_to": [],
                "evidence": [],
                "affected_files": [],
                "next_actions": [],
                "redaction_notes": ["Raw content fields are not rendered."],
            }

    positions = _compute_positions(graph_dict["nodes"])

    return BrainViewerData(
        job_id=str(job.id),
        generated_at=datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        graph=graph_dict,
        node_details=node_details,
        positions=positions,
        detail_fallback_count=detail_fallback_count,
    )


def export_brain_viewer_json(data: BrainViewerData) -> dict[str, Any]:
    """Export viewer data as a JSON-serialisable dict."""
    return {
        "version": 1,
        "job_id": data.job_id,
        "generated_at": data.generated_at,
        "graph": data.graph,
        "node_details": data.node_details,
        "positions": data.positions,
        "detail_fallback_count": data.detail_fallback_count,
    }


def write_brain_viewer_files(data: BrainViewerData, out_dir: Path) -> Path:
    """Write viewer_data.json and index.html under out_dir.

    Returns the path to index.html.  The caller is responsible for ensuring
    out_dir is under REMEDY_DATA_DIR and not inside the target repository.
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    viewer_dict = export_brain_viewer_json(data)

    (out_dir / "viewer_data.json").write_text(
        json.dumps(viewer_dict, sort_keys=True, indent=2),
        encoding="utf-8",
    )

    safe_json = json.dumps(viewer_dict, sort_keys=True).replace(
        "</script>", r"<\/script>"
    )
    static_fallback_html = _render_static_fallback(viewer_dict)
    html = _render_html(safe_json, data.job_id[:8], data.generated_at, static_fallback_html)
    index_path = out_dir / "index.html"
    index_path.write_text(html, encoding="utf-8")

    return index_path


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _compute_positions(nodes: list[dict[str, Any]]) -> dict[str, list[float]]:
    """Assign 2D positions using semantic zone + layered radial layout.

    Nodes in the same zone are grouped together in a sector.
    Returns {node_id: [x, y]} in a nominal 1000x700 coordinate space.
    """
    # Group by (layer, zone)
    by_zone_layer: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for node in nodes:
        zone = _ZONE_MAP.get(node["type"], "future")
        layer = _LAYER_MAP.get(node["type"], 3)
        by_zone_layer.setdefault((zone, layer), []).append(node)

    positions: dict[str, list[float]] = {}
    for (zone, layer_idx), layer_nodes in sorted(by_zone_layer.items()):
        r = (
            _LAYER_RADIUS[layer_idx]
            if layer_idx < len(_LAYER_RADIUS)
            else _LAYER_RADIUS[-1] + 80.0
        )
        base_angle = _ZONE_ANGLES.get(zone, 5.8)
        count = len(layer_nodes)
        spread = 0.35  # radians spread within zone
        for i, node in enumerate(layer_nodes):
            if r == 0.0:
                x, y = _CX, _CY
            elif count == 1:
                angle = base_angle - math.pi / 2.0
                x = round(_CX + r * math.cos(angle), 1)
                y = round(_CY + r * math.sin(angle), 1)
            else:
                offset = (i - (count - 1) / 2.0) * spread / max(count - 1, 1)
                angle = base_angle + offset - math.pi / 2.0
                x = round(_CX + r * math.cos(angle), 1)
                y = round(_CY + r * math.sin(angle), 1)
            positions[node["id"]] = [x, y]

    return positions


def _render_static_fallback(viewer_dict: dict) -> str:
    """Generate server-rendered HTML fallback — visible without JavaScript."""
    graph = viewer_dict.get("graph", {})
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    details = viewer_dict.get("node_details", {})
    fallback_count = viewer_dict.get("detail_fallback_count", 0)

    ctx_score = None
    for n in nodes:
        if n.get("type") == "context_coverage":
            meta = n.get("metadata") or {}
            if "score" in meta:
                ctx_score = meta["score"]
            break

    def _e(s: object) -> str:
        return _html_esc(str(s), quote=True)

    parts: list[str] = []
    parts.append('<div class="sf-sum">')
    parts.append(f'<span>nodes <b>{_e(len(nodes))}</b></span> ')
    parts.append(f'<span>edges <b>{_e(len(edges))}</b></span> ')
    parts.append(f'<span>details <b>{_e(len(details))}</b></span> ')
    parts.append(f'<span>fallbacks <b>{_e(fallback_count)}</b></span>')
    if ctx_score is not None:
        parts.append(f' <span>context <b>{_e(ctx_score)}%</b></span>')
    parts.append('</div>')
    if nodes:
        parts.append(
            '<table class="sf-tbl">'
            '<tr><th>type</th><th>label</th><th>status</th><th>risk</th></tr>'
        )
        for n in nodes[:50]:
            parts.append(
                f'<tr>'
                f'<td>{_e(n.get("type", ""))}</td>'
                f'<td>{_e(n.get("label", ""))}</td>'
                f'<td>{_e(n.get("status") or "")}</td>'
                f'<td>{_e(n.get("risk") or "")}</td>'
                f'</tr>'
            )
        parts.append('</table>')
        if len(nodes) > 50:
            parts.append(f'<p class="sf-trunc">showing 50 of {_e(len(nodes))} nodes</p>')
    return ''.join(parts)


def _render_html(
    viewer_json_str: str,
    job_short_id: str,
    generated_at: str,
    static_fallback_html: str,
) -> str:
    """Return self-contained HTML with JSON data island and server-rendered fallback."""
    from packages.orchestration.brain_viewer_theme import REMEDY_CSS

    return (
        _HTML
        .replace("__REMEDY_CSS__", REMEDY_CSS)
        .replace("__VIEWER_DATA_JSON__", viewer_json_str)
        .replace("__STATIC_FALLBACK__", static_fallback_html)
        .replace("__JOB_SHORT_ID__", job_short_id)
        .replace("__GENERATED_AT__", generated_at)
    )


# ---------------------------------------------------------------------------
# HTML template  (placeholders: __REMEDY_CSS__, __VIEWER_DATA_JSON__,
#                 __STATIC_FALLBACK__, __JOB_SHORT_ID__, __GENERATED_AT__)
# ---------------------------------------------------------------------------

_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Remedy Brain Viewer — __JOB_SHORT_ID__</title>
<style>
__REMEDY_CSS__
*{box-sizing:border-box;margin:0;padding:0}
body{display:flex;flex-direction:column;height:100vh;overflow:hidden}
#hdr{background:var(--remedy-bg-panel);padding:6px 16px;display:flex;align-items:center;gap:10px;
     border-bottom:1px solid var(--remedy-panel-border);flex-shrink:0;z-index:3}
#hdr h1{font-size:14px;font-weight:bold;color:var(--remedy-teal);font-family:var(--remedy-font-sans)}
.badge{background:rgba(56,200,200,0.08);color:var(--remedy-teal);padding:2px 8px;border-radius:4px;
       font-size:11px;border:1px solid var(--remedy-panel-border)}
.badge-warn{background:rgba(232,168,56,0.1);color:var(--remedy-warning);border-color:rgba(232,168,56,0.2)}
#render-badge[data-status="ready"]{background:rgba(56,200,136,0.1);color:var(--remedy-proof);border-color:rgba(56,200,136,0.2)}
#render-badge[data-status="error"]{background:rgba(224,82,82,0.1);color:var(--remedy-risk);border-color:rgba(224,82,82,0.2)}
#render-badge[data-status="empty"]{background:rgba(56,200,200,0.05);color:var(--remedy-fg-muted);border-color:var(--remedy-panel-border)}
#render-badge[data-status="static-fallback"]{background:rgba(58,74,90,0.3);color:var(--remedy-fg-muted);border-color:var(--remedy-muted)}
/* ── Search bar ── */
#search-bar{display:flex;gap:8px;padding:4px 16px;align-items:center;
  border-bottom:1px solid var(--remedy-panel-border);flex-shrink:0;z-index:3;
  background:var(--remedy-bg-panel)}
#search-input{background:rgba(56,200,200,0.04);border:1px solid var(--remedy-panel-border);
  color:var(--remedy-fg);font-family:var(--remedy-font);font-size:12px;padding:4px 10px;
  border-radius:4px;flex:1;max-width:300px;outline:none}
#search-input:focus{border-color:var(--remedy-teal);box-shadow:0 0 6px var(--remedy-glow)}
#search-input::placeholder{color:var(--remedy-fg-muted)}
.filter-btn{background:rgba(56,200,200,0.04);border:1px solid var(--remedy-panel-border);
  color:var(--remedy-fg-muted);font-size:10px;padding:3px 8px;border-radius:3px;cursor:pointer;
  font-family:var(--remedy-font);transition:all .15s}
.filter-btn:hover,.filter-btn.active{background:rgba(56,200,200,0.12);color:var(--remedy-teal);
  border-color:var(--remedy-teal)}
.filter-btn:focus-visible{outline:2px solid var(--remedy-teal);outline-offset:2px}
/* ── Info bar ── */
#info-bar{display:flex;gap:8px;padding:4px 16px;flex-wrap:wrap;font-size:11px;
  border-bottom:1px solid var(--remedy-panel-border);flex-shrink:0;z-index:2;
  background:var(--remedy-bg-panel)}
#info-bar .info-item{padding:3px 10px;border-radius:4px;
  background:rgba(56,200,200,0.04);border:1px solid var(--remedy-panel-border)}
/* ── Proof chain ── */
#proof-chain-panel{padding:0 16px;flex-shrink:0;z-index:1;
  border-bottom:1px solid var(--remedy-panel-border)}
/* ── Static fallback ── */
#static-fallback{padding:12px 16px;background:var(--remedy-bg);border-bottom:1px solid var(--remedy-panel-border);
  font-size:12px;overflow-y:auto;max-height:200px;flex-shrink:0;z-index:1}
.sf-sum{display:flex;gap:12px;margin-bottom:8px;flex-wrap:wrap}
.sf-sum span{color:var(--remedy-fg-muted)}.sf-sum b{color:var(--remedy-fg)}
.sf-tbl{border-collapse:collapse;font-size:11px}
.sf-tbl th,.sf-tbl td{padding:2px 8px;text-align:left;border:1px solid var(--remedy-panel-border)}
.sf-tbl th{color:var(--remedy-fg-muted);font-weight:normal}
.sf-tbl td{color:var(--remedy-fg-muted)}
.sf-trunc{margin-top:4px;color:var(--remedy-fg-muted);font-size:10px;font-style:italic}
/* ── Main layout ── */
#main{display:flex;flex:1;overflow:hidden;min-height:0;position:relative}
/* ── Left filter rail ── */
#filter-rail{width:180px;background:var(--remedy-bg-panel);border-right:1px solid var(--remedy-panel-border);
  overflow-y:auto;flex-shrink:0;padding:8px;font-size:11px;z-index:1}
#filter-rail .fr-section{margin-bottom:8px}
#filter-rail .fr-label{color:var(--remedy-fg-muted);font-size:9px;text-transform:uppercase;
  letter-spacing:.06em;margin-bottom:4px}
#filter-rail .fr-item{display:flex;align-items:center;gap:4px;padding:2px 4px;cursor:pointer;
  border-radius:3px;color:var(--remedy-fg-muted);transition:all .12s}
#filter-rail .fr-item:hover{background:rgba(56,200,200,0.06);color:var(--remedy-fg)}
#filter-rail .fr-item.active{color:var(--remedy-teal)}
#filter-rail .fr-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
/* ── Graph ── */
#gwrap{flex:1;position:relative;overflow:hidden}
svg#g{width:100%;height:100%;display:block}
/* ── Mist/depth layers ── */
.remedy-mist{position:absolute;inset:0;pointer-events:none;z-index:0;
  background:radial-gradient(ellipse at 50% 50%, transparent 40%, rgba(10,14,20,0.6) 100%)}
.remedy-scanlines{position:absolute;inset:0;pointer-events:none;z-index:0;opacity:0.03;
  background:repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(56,200,200,0.15) 2px, rgba(56,200,200,0.15) 3px)}
.remedy-grid{position:absolute;inset:0;pointer-events:none;z-index:0;opacity:0.04;
  background-size:40px 40px;
  background-image:linear-gradient(rgba(56,200,200,0.2) 1px, transparent 1px),
                   linear-gradient(90deg, rgba(56,200,200,0.2) 1px, transparent 1px)}
/* ── Error panel ── */
#err-panel{display:none;position:absolute;top:10px;left:10px;right:10px;
  background:rgba(224,82,82,0.1);color:var(--remedy-risk);border:1px solid rgba(224,82,82,0.3);
  border-radius:6px;padding:10px 14px;font-size:12px;z-index:10}
/* ── Side panels ── */
#side-panels{width:340px;display:flex;flex-direction:column;overflow-y:auto;
  border-left:1px solid var(--remedy-panel-border);flex-shrink:0;
  background:var(--remedy-bg-panel);z-index:1}
#dp{padding:12px;font-size:12px;flex:1;overflow-y:auto}
#dh{color:var(--remedy-fg-muted);padding:24px 0;text-align:center;font-size:13px}
.dt{font-size:14px;font-weight:bold;color:var(--remedy-teal);margin-bottom:8px;word-break:break-all}
.dr{margin:3px 0}.dl{color:var(--remedy-fg-muted)}.dv{color:var(--remedy-fg)}
.ds{margin:8px 0 3px;color:var(--remedy-teal);border-bottom:1px solid var(--remedy-panel-border);
    padding-bottom:2px;font-size:10px;text-transform:uppercase;letter-spacing:.06em}
.di{margin:2px 0 2px 8px;color:var(--remedy-fg-muted);word-break:break-all}
.drd{color:var(--remedy-muted);font-style:italic}
/* ── Next action rail ── */
#next-action-rail{padding:8px 12px;border-top:1px solid var(--remedy-panel-border)}
#next-action-rail .na-label{font-size:9px;text-transform:uppercase;letter-spacing:.06em;
  color:var(--remedy-fg-muted);margin-bottom:4px}
.na-card{background:rgba(56,200,200,0.04);border:1px solid var(--remedy-panel-border);
  border-radius:4px;padding:6px 8px;margin:3px 0;font-size:11px;cursor:default}
.na-card .na-title{color:var(--remedy-fg)}
.na-card .na-cmd{color:var(--remedy-teal);font-family:var(--remedy-font);font-size:10px;
  margin-top:2px;display:flex;align-items:center;gap:4px}
.copy-btn{background:none;border:1px solid var(--remedy-panel-border);color:var(--remedy-fg-muted);
  font-size:9px;padding:1px 6px;border-radius:3px;cursor:pointer;font-family:var(--remedy-font)}
.copy-btn:hover{color:var(--remedy-teal);border-color:var(--remedy-teal)}
.copy-btn:focus-visible{outline:2px solid var(--remedy-teal);outline-offset:1px}
/* ── Decision/Readiness side sections ── */
.remedy-decision-panel{border-left:2px solid var(--remedy-warning);padding-left:12px;margin:8px 0}
.remedy-readiness-panel{border-left:2px solid var(--remedy-teal);padding-left:12px;margin:8px 0}
/* ── Timeline ── */
#timeline-panel{padding:0 16px;flex-shrink:0;z-index:1;
  border-bottom:1px solid var(--remedy-panel-border)}
/* ── Guidance rail ── */
#guidance-rail{padding:4px 16px;flex-shrink:0;z-index:1;display:flex;gap:6px;flex-wrap:wrap;
  border-bottom:1px solid var(--remedy-panel-border);background:var(--remedy-bg-panel);font-size:11px}
.guide-card{background:rgba(56,200,200,0.04);border:1px solid var(--remedy-panel-border);
  border-radius:4px;padding:4px 8px;display:flex;align-items:center;gap:4px}
.guide-card.high{border-color:rgba(224,82,82,0.3);color:var(--remedy-risk)}
.guide-card.medium{border-color:rgba(232,168,56,0.3);color:var(--remedy-warning)}
.guide-card.info{color:var(--remedy-fg-muted)}
/* ── Legend ── */
#leg{background:var(--remedy-bg-panel);padding:4px 16px;border-top:1px solid var(--remedy-panel-border);
     display:flex;gap:14px;font-size:10px;flex-wrap:wrap;align-items:center;flex-shrink:0;z-index:2}
.li{display:flex;align-items:center;gap:4px}
.ld{width:11px;height:11px;border-radius:50%;border:1px solid var(--remedy-muted)}
/* ── Diag ── */
#diag{background:var(--remedy-bg);padding:3px 16px;border-top:1px solid var(--remedy-panel-border);
  font-size:10px;color:var(--remedy-fg-muted);display:flex;gap:14px;flex-wrap:wrap;
  align-items:center;flex-shrink:0;z-index:2}
#diag b{color:var(--remedy-muted)}
#diag span{color:var(--remedy-fg-muted)}
#ftr{background:var(--remedy-bg-panel);padding:3px 16px;font-size:10px;color:var(--remedy-muted);
     border-top:1px solid var(--remedy-panel-border);flex-shrink:0;z-index:2}
/* ── SVG styles ── */
.el{stroke:var(--remedy-line);stroke-width:1.5;transition:stroke .15s,opacity .15s}
.el.proof-edge{stroke:var(--remedy-proof);stroke-width:2;opacity:0.6}
.el.blocked-edge{stroke:var(--remedy-risk);stroke-dasharray:4 3}
.el.future-edge{stroke:var(--remedy-muted);opacity:0.3;stroke-dasharray:2 4}
.el.sel-edge{stroke:var(--remedy-teal);stroke-width:2.5;opacity:0.9}
.el.dim{opacity:0.08}
.nd{cursor:pointer;transition:transform .15s}
.nd circle{stroke-width:2;transition:stroke .15s,stroke-width .15s,filter .15s}
.nd:hover circle{stroke:var(--remedy-teal) !important;stroke-width:3;
  filter:drop-shadow(0 0 6px var(--remedy-glow))}
.nd.sel circle{stroke:var(--remedy-teal) !important;stroke-width:3;
  filter:drop-shadow(0 0 10px var(--remedy-teal))}
.nd.dim circle{opacity:0.15}
.nd.dim text{opacity:0.15}
.nd text{font-size:9px;fill:var(--remedy-fg-muted);pointer-events:none;text-anchor:middle}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.nd.run circle{animation:pulse 1.5s ease-in-out infinite}
@keyframes sel-pulse{0%,100%{filter:drop-shadow(0 0 8px var(--remedy-teal))}50%{filter:drop-shadow(0 0 14px var(--remedy-teal))}}
.nd.sel circle{animation:sel-pulse 2s ease-in-out infinite}
/* ── Zone labels ── */
.zone-label{font-size:10px;fill:var(--remedy-fg-muted);opacity:0.4;text-anchor:middle;
  font-family:var(--remedy-font-sans);text-transform:uppercase;letter-spacing:.08em;pointer-events:none}
/* ── Accessibility ── */
@media (prefers-reduced-motion: reduce) {
  .nd.run circle{animation:none}
  .nd.sel circle{animation:none;filter:drop-shadow(0 0 10px var(--remedy-teal))}
  .remedy-particle-field{animation:none !important}
  .remedy-scanlines{display:none}
}
[tabindex]:focus-visible,.filter-btn:focus-visible,#search-input:focus-visible{
  outline:2px solid var(--remedy-teal);outline-offset:2px}
</style>
</head>
<body class="remedy-shell" data-render-status="static-fallback">
<div class="remedy-orbit-bg"></div>
<div class="remedy-particle-field"></div>
<div id="hdr">
  <h1>Remedy Brain Viewer</h1>
  <span class="badge badge-warn">read-only</span>
  <span class="badge">job __JOB_SHORT_ID__</span>
  <span class="badge">__GENERATED_AT__</span>
  <span class="badge" id="ctx-badge">Context: —%</span>
  <span class="badge" id="render-badge" data-status="static-fallback">● static</span>
</div>
<div id="search-bar">
  <input id="search-input" type="text" placeholder="/ search nodes..." aria-label="Search nodes" tabindex="0">
  <button class="filter-btn" data-filter="blocker" tabindex="0">Blockers</button>
  <button class="filter-btn" data-filter="proof" tabindex="0">Proofs</button>
  <button class="filter-btn" data-filter="decision" tabindex="0">Decisions</button>
  <button class="filter-btn" data-filter="all" tabindex="0">Reset</button>
</div>
<div id="info-bar">
  <span class="info-item" id="info-readiness">Readiness: —</span>
  <span class="info-item" id="info-decisions">Decisions: —</span>
  <span class="info-item" id="info-worker">Worker: —</span>
  <span class="info-item" id="info-token-mode">Token: —</span>
  <span class="info-item" id="info-git">Git: —</span>
</div>
<div id="proof-chain-panel">
  <div class="remedy-proof-chain" id="proof-chain"></div>
</div>
<div id="static-fallback">
__STATIC_FALLBACK__
</div>
<div id="main">
  <div id="filter-rail">
    <div class="fr-section">
      <div class="fr-label">Zones</div>
      <div id="zone-filters"></div>
    </div>
    <div class="fr-section">
      <div class="fr-label">Status</div>
      <div id="status-filters"></div>
    </div>
    <div class="fr-section">
      <div class="fr-label">Risk</div>
      <div id="risk-filters"></div>
    </div>
  </div>
  <div id="gwrap">
    <div class="remedy-grid"></div>
    <div class="remedy-scanlines"></div>
    <div class="remedy-mist"></div>
    <svg id="g"></svg>
    <div id="err-panel" style="display:none"><strong>Viewer error</strong> — <span id="err-msg"></span></div>
  </div>
  <div id="side-panels">
    <div id="dp">
      <p id="dh">&larr; Click a node to inspect it</p>
      <div id="db" style="display:none"></div>
    </div>
    <div id="next-action-rail" style="display:none">
      <div class="na-label">Next Actions</div>
      <div id="na-cards"></div>
    </div>
    <div id="decision-section" class="remedy-decision-panel" style="display:none;padding:8px 12px">
      <div style="font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--remedy-fg-muted);margin-bottom:4px">Decisions</div>
      <div class="decision-count" id="decision-count">0</div>
      <div id="decision-list" style="font-size:11px;color:var(--remedy-fg-muted)"></div>
    </div>
    <div id="readiness-section" class="remedy-readiness-panel" style="display:none;padding:8px 12px">
      <div style="font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--remedy-fg-muted);margin-bottom:4px">Readiness</div>
      <div class="readiness-level" id="readiness-level">—</div>
      <div id="readiness-missing" style="font-size:11px;color:var(--remedy-fg-muted)"></div>
    </div>
  </div>
</div>
<div id="guidance-rail"></div>
<div id="timeline-panel">
  <div class="remedy-timeline" id="timeline"></div>
</div>
<div id="leg">
  <strong style="color:var(--remedy-fg-muted)">Legend:</strong>
  <div class="li"><div class="ld" style="background:var(--remedy-fg-muted)"></div>pending</div>
  <div class="li"><div class="ld" style="background:var(--remedy-cyan)"></div>running</div>
  <div class="li"><div class="ld" style="background:var(--remedy-teal)"></div>completed</div>
  <div class="li"><div class="ld" style="background:var(--remedy-risk)"></div>blocked</div>
  <div class="li"><div class="ld" style="background:var(--remedy-warning)"></div>needs approval</div>
  <div class="li"><div class="ld" style="background:var(--remedy-memory)"></div>memory</div>
  <div class="li"><div class="ld" style="background:var(--remedy-muted)"></div>future</div>
</div>
<div id="diag">
  <b>diag:</b>
  <span>nodes <span id="diag-nodes">?</span></span>
  <span>edges <span id="diag-edges">?</span></span>
  <span>details <span id="diag-details">?</span></span>
  <span>fallbacks <span id="diag-fallbacks">?</span></span>
  <span>selected <span id="diag-sel">none</span></span>
  <span>status <span id="diag-status">static-fallback</span></span>
</div>
<div id="ftr">Remedy Brain Viewer &middot; read-only &middot; static export &middot; no external assets</div>
<script id="viewer-data" type="application/json">__VIEWER_DATA_JSON__</script>
<script>
function _vErr(cat,msg){
  var safe=String(msg||'').replace(/[\\r\\n\\t]/g,' ').slice(0,120);
  document.body.setAttribute('data-render-status','error');
  var b=document.getElementById('render-badge');
  if(b){b.textContent='\\u25cf error';b.setAttribute('data-status','error');}
  var ds=document.getElementById('diag-status');
  if(ds)ds.textContent='error';
  var ep=document.getElementById('err-panel');
  if(ep){
    var em=document.getElementById('err-msg');
    if(em)em.textContent=String(cat)+': '+safe;
    ep.style.display='block';
  }
}
window.onerror=function(msg){console.error(msg);_vErr('uncaught',msg);return false;};
(function(){
'use strict';
function setRenderStatus(s){
  document.body.setAttribute('data-render-status',s);
  var b=document.getElementById('render-badge');
  if(b){b.textContent='\\u25cf '+s;b.setAttribute('data-status',s);}
  var ds=document.getElementById('diag-status');
  if(ds)ds.textContent=s;
  if(s==='ready'||s==='empty'){
    var sf=document.getElementById('static-fallback');
    if(sf)sf.style.display='none';
  }
}
try{
var _src=document.getElementById('viewer-data');
if(!_src)throw new Error('viewer-data island missing');
var VD=JSON.parse(_src.textContent);
var G=VD.graph,DET=VD.node_details,POS=VD.positions;
var selId=null;
var activeFilter=null;
var searchTerm='';
var JOB_ID=VD.job_id||'';

function col(n){
  var t=n.type,s=n.status||'';
  if(t==='memory_placeholder'||t==='memory')return'var(--remedy-memory)';
  if(t==='autonomy_readiness')return'var(--remedy-proof)';
  if(t==='context_pack'||t==='context_budget')return'var(--remedy-cyan)';
  if(t==='mcp_placeholder')return'var(--remedy-muted)';
  if(s==='blocked'||s==='failed'||s==='rejected')return'var(--remedy-risk)';
  if(s==='running')return'var(--remedy-cyan)';
  if(s==='completed'||s==='passed'||s==='loaded'||s==='approved')return'var(--remedy-teal)';
  if(t==='patch_intent'&&s==='pending')return'var(--remedy-warning)';
  if(s==='needs_decision'||s==='needs_approval')return'var(--remedy-warning)';
  if(s==='informational')return'var(--remedy-muted)';
  return'var(--remedy-fg-muted)';
}
function rad(n){
  if(n.type==='job')return 22;
  if(n.type==='task'||n.type==='artifact'||n.type==='patch_intent'||n.type==='approval_decision')return 15;
  return 11;
}
function esc(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
function edgeClass(e){
  var t=e.type||'';
  if(t.indexOf('proof')>=0||t.indexOf('verified')>=0)return'el proof-edge';
  if(t.indexOf('blocked')>=0)return'el blocked-edge';
  if(t.indexOf('future')>=0||t.indexOf('inert')>=0)return'el future-edge';
  return'el';
}
function nodeVisible(n){
  if(searchTerm){
    var q=searchTerm.toLowerCase();
    if((n.label||'').toLowerCase().indexOf(q)<0&&(n.type||'').toLowerCase().indexOf(q)<0&&(n.id||'').toLowerCase().indexOf(q)<0)return false;
  }
  if(!activeFilter||activeFilter==='all')return true;
  if(activeFilter==='blocker')return n.status==='blocked'||n.status==='failed'||n.type==='stop_reason'||n.type==='permission_blocker';
  if(activeFilter==='proof')return n.type==='test_run'||n.type==='verification'||n.type==='patch_apply_proof'||n.status==='passed';
  if(activeFilter==='decision')return n.type==='decision_queue'||n.type==='approval_decision'||n.status==='needs_decision'||n.status==='needs_approval';
  if(activeFilter.indexOf('zone:')==0){var z=activeFilter.slice(5);return(n.zone||'')==z;}
  if(activeFilter.indexOf('status:')==0){var st=activeFilter.slice(7);return(n.status||'')==st;}
  if(activeFilter.indexOf('risk:')==0)return!!n.risk;
  return true;
}
function scaledPos(W,H){
  var xs=Object.values(POS).map(function(p){return p[0];});
  var ys=Object.values(POS).map(function(p){return p[1];});
  if(!xs.length)return{};
  var minX=Math.min.apply(null,xs),maxX=Math.max.apply(null,xs);
  var minY=Math.min.apply(null,ys),maxY=Math.max.apply(null,ys);
  var pad=56,rX=maxX-minX||1,rY=maxY-minY||1;
  var sc=Math.min((W-pad*2)/rX,(H-pad*2)/rY);
  var ox=pad+(W-pad*2-rX*sc)/2,oy=pad+(H-pad*2-rY*sc)/2;
  var m={};
  for(var id in POS){
    m[id]=[(POS[id][0]-minX)*sc+ox,(POS[id][1]-minY)*sc+oy];
  }
  return m;
}
function render(){
  var wrap=document.getElementById('gwrap');
  var W=wrap.clientWidth||800,H=wrap.clientHeight||600;
  var svg=document.getElementById('g');
  svg.setAttribute('viewBox','0 0 '+W+' '+H);
  var pm=scaledPos(W,H);
  var visIds={};
  G.nodes.forEach(function(n){if(nodeVisible(n))visIds[n.id]=true;});
  var h='<g>';
  // Zone labels
  var zonePts={};
  G.nodes.forEach(function(n){
    var z=n.zone||'';var p=pm[n.id];if(!p||!z)return;
    if(!zonePts[z])zonePts[z]={sx:0,sy:0,c:0};
    zonePts[z].sx+=p[0];zonePts[z].sy+=p[1];zonePts[z].c++;
  });
  for(var zn in zonePts){
    var zp=zonePts[zn];
    h+='<text class="zone-label" x="'+(zp.sx/zp.c).toFixed(0)+'" y="'+((zp.sy/zp.c)-25).toFixed(0)+'">'+esc(zn)+'</text>';
  }
  // Edges
  G.edges.forEach(function(e){
    var s=pm[e.source],t=pm[e.target];
    if(!s||!t)return;
    var cls=edgeClass(e);
    var isSel=selId&&(e.source===selId||e.target===selId);
    if(isSel)cls+=' sel-edge';
    else if(selId||activeFilter)if(!visIds[e.source]&&!visIds[e.target])cls+=' dim';
    h+='<line class="'+cls+'" x1="'+s[0].toFixed(1)+'" y1="'+s[1].toFixed(1)+'" x2="'+t[0].toFixed(1)+'" y2="'+t[1].toFixed(1)+'"/>';
  });
  // Nodes
  G.nodes.forEach(function(n){
    var p=pm[n.id];if(!p)return;
    var x=p[0],y=p[1],r=rad(n),c=col(n);
    var vis=visIds[n.id];
    var cls='nd'+(n.status==='running'?' run':'')+(n.id===selId?' sel':'')+(vis?'':' dim');
    var lbl=n.label.length>15?n.label.slice(0,14)+'\\u2026':n.label;
    h+='<g class="'+cls+'" data-nid="'+esc(n.id)+'" tabindex="0" onclick="pick(this.dataset.nid)" onkeydown="if(event.key===\\'Enter\\')pick(this.dataset.nid)">';
    h+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+r+'" fill="'+c+'" stroke="var(--remedy-node-border)" stroke-width="2"/>';
    h+='<text x="'+x.toFixed(1)+'" y="'+(y+r+9).toFixed(1)+'">'+esc(lbl)+'</text>';
    h+='</g>';
  });
  h+='</g>';
  svg.innerHTML=h;
}
function buildCmdSuggestions(d){
  var cmds=[];
  var jid=JOB_ID.slice(0,8);
  cmds.push({label:'Inspect node',cmd:'remedy brain node '+jid+' '+d.node_id});
  if(d.node_type==='task'||d.node_type==='artifact')
    cmds.push({label:'View graph',cmd:'remedy brain graph '+jid+' --json'});
  if(d.affected_files&&d.affected_files.length)
    cmds.push({label:'File provenance',cmd:'remedy file why '+jid+' <path>'});
  if(d.node_type==='decision_queue'||d.node_type==='approval_decision')
    cmds.push({label:'Decisions',cmd:'remedy decision list '+jid});
  if(d.node_type==='stop_reason'||d.node_type==='permission_blocker')
    cmds.push({label:'Blockers',cmd:'remedy blocker list '+jid});
  if(d.node_type==='autonomy_readiness')
    cmds.push({label:'Readiness',cmd:'remedy readiness job '+jid});
  cmds.push({label:'Dashboard',cmd:'remedy dashboard job '+jid});
  cmds.push({label:'Guide',cmd:'remedy guide job '+jid});
  return cmds;
}
window.pick=function(nodeId){
  selId=nodeId;render();
  var diagSel=document.getElementById('diag-sel');
  if(diagSel)diagSel.textContent=nodeId||'none';
  document.getElementById('dh').style.display='none';
  var body=document.getElementById('db');
  body.style.display='block';
  var d=DET[nodeId];
  if(!d){body.innerHTML='<p style="color:var(--remedy-fg-muted)">No detail available.</p>';return;}
  var h='<div class="dt">'+esc(d.title)+'</div>';
  h+='<div class="dr"><span class="dl">type </span><span class="dv">'+esc(d.node_type)+'</span></div>';
  h+='<div class="dr"><span class="dl">status </span><span class="dv">'+esc(String(d.status))+'</span></div>';
  if(d.risk)h+='<div class="dr"><span class="dl">risk </span><span class="dv">'+esc(String(d.risk))+'</span></div>';
  h+='<div class="ds">Explanation</div><div class="di">'+esc(d.explanation)+'</div>';
  if(d.why_it_exists&&d.why_it_exists.length){
    h+='<div class="ds">Why it exists</div>';
    d.why_it_exists.forEach(function(w){h+='<div class="di">\\u25cb '+esc(w)+'</div>';});
  }
  if(d.evidence&&d.evidence.length){
    h+='<div class="ds">Evidence</div>';
    d.evidence.forEach(function(e){h+='<div class="di">\\u2713 '+esc(e)+'</div>';});
  }
  if(d.affected_files&&d.affected_files.length){
    h+='<div class="ds">Affected files</div>';
    d.affected_files.forEach(function(f){h+='<div class="di">! '+esc(f)+'</div>';});
  }
  if(d.next_actions&&d.next_actions.length){
    h+='<div class="ds">Next actions</div>';
    d.next_actions.forEach(function(a){h+='<div class="di">\\u2192 '+esc(a)+'</div>';});
  }
  if(d.connected_to&&d.connected_to.length){
    h+='<div class="ds">Connections ('+d.connected_to.length+')</div>';
    d.connected_to.slice(0,8).forEach(function(c){
      h+='<div class="di">['+esc(c.direction)+'] --'+esc(c.edge_type)+'--> '+esc(c.node_type)+' \\u00b7 '+esc(c.node_label.slice(0,28))+'</div>';
    });
  }
  if(d.redaction_notes&&d.redaction_notes.length){
    h+='<div class="ds drd">Redaction</div>';
    d.redaction_notes.forEach(function(r){h+='<div class="di drd">\\u25cb '+esc(r)+'</div>';});
  }
  body.innerHTML=h;
  // Next action rail
  var nar=document.getElementById('next-action-rail');
  var nac=document.getElementById('na-cards');
  if(nar&&nac){
    var cmds=buildCmdSuggestions(d);
    var ch='';
    cmds.forEach(function(c){
      ch+='<div class="na-card"><div class="na-title">'+esc(c.label)+'</div>';
      ch+='<div class="na-cmd"><code>'+esc(c.cmd)+'</code> ';
      ch+='<button class="copy-btn" onclick="navigator.clipboard&&navigator.clipboard.writeText(\\''+esc(c.cmd).replace(/'/g,"\\\\'")+'\\')" tabindex="0">copy</button>';
      ch+='</div></div>';
    });
    nac.innerHTML=ch;
    nar.style.display='block';
  }
};
// ── Search ──
var si=document.getElementById('search-input');
if(si){
  si.addEventListener('input',function(){searchTerm=si.value;render();});
}
// ── Filter buttons ──
document.querySelectorAll('.filter-btn[data-filter]').forEach(function(btn){
  btn.addEventListener('click',function(){
    var f=btn.getAttribute('data-filter');
    document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.remove('active');});
    if(f==='all'||activeFilter===f){activeFilter=null;}
    else{activeFilter=f;btn.classList.add('active');}
    render();
  });
});
// ── Keyboard ──
document.addEventListener('keydown',function(e){
  if(e.key==='/'){
    e.preventDefault();
    var si2=document.getElementById('search-input');
    if(si2)si2.focus();
  }
  if(e.key==='Escape'){
    selId=null;searchTerm='';activeFilter=null;
    var si3=document.getElementById('search-input');
    if(si3){si3.value='';si3.blur();}
    document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.remove('active');});
    document.getElementById('dh').style.display='';
    document.getElementById('db').style.display='none';
    var nar2=document.getElementById('next-action-rail');
    if(nar2)nar2.style.display='none';
    render();
  }
});
window.addEventListener('resize',render);
render();
// ── Diag ──
var dn=document.getElementById('diag-nodes');
var de=document.getElementById('diag-edges');
var dd=document.getElementById('diag-details');
var df=document.getElementById('diag-fallbacks');
if(dn)dn.textContent=G.nodes.length;
if(de)de.textContent=G.edges.length;
if(dd)dd.textContent=Object.keys(DET).length;
if(df)df.textContent=VD.detail_fallback_count||0;
// ── Context badge ──
(function(){
  var cc=G.nodes.find(function(n){return n.type==='context_coverage';});
  if(cc&&cc.metadata!=null){
    var el=document.getElementById('ctx-badge');
    if(el)el.textContent='Context: '+cc.metadata.score+'%';
  }
})();
// ── Filter rail ──
(function(){
  var zf=document.getElementById('zone-filters');
  var sf=document.getElementById('status-filters');
  var rf=document.getElementById('risk-filters');
  if(!zf)return;
  var zones={},statuses={},hasRisk=false;
  G.nodes.forEach(function(n){
    zones[n.zone||'other']=true;
    if(n.status)statuses[n.status]=true;
    if(n.risk)hasRisk=true;
  });
  var zh='';
  Object.keys(zones).sort().forEach(function(z){
    zh+='<div class="fr-item" data-filt="zone:'+esc(z)+'" tabindex="0"><div class="fr-dot" style="background:var(--remedy-teal)"></div>'+esc(z)+'</div>';
  });
  zf.innerHTML=zh;
  var sh='';
  Object.keys(statuses).sort().forEach(function(s){
    sh+='<div class="fr-item" data-filt="status:'+esc(s)+'" tabindex="0"><div class="fr-dot" style="background:var(--remedy-fg-muted)"></div>'+esc(s)+'</div>';
  });
  sf.innerHTML=sh;
  if(hasRisk){
    rf.innerHTML='<div class="fr-item" data-filt="risk:yes" tabindex="0"><div class="fr-dot" style="background:var(--remedy-risk)"></div>has risk</div>';
  }
  document.getElementById('filter-rail').addEventListener('click',function(ev){
    var item=ev.target.closest('.fr-item');
    if(!item)return;
    var f=item.getAttribute('data-filt');
    if(activeFilter===f){activeFilter=null;item.classList.remove('active');}
    else{
      document.querySelectorAll('.fr-item').forEach(function(i){i.classList.remove('active');});
      activeFilter=f;item.classList.add('active');
    }
    render();
  });
})();
// ── Info bar from graph nodes ──
(function(){
  var ar=G.nodes.find(function(n){return n.type==='autonomy_readiness';});
  if(ar){
    var m=ar.metadata||{};
    var el=document.getElementById('info-readiness');
    if(el)el.textContent='Readiness: '+(m.level!=null?m.level:'\\u2014');
    var rs=document.getElementById('readiness-section');
    if(rs){
      rs.style.display='block';
      var rl=document.getElementById('readiness-level');
      if(rl)rl.textContent=m.level!=null?String(m.level):'\\u2014';
      var rm=document.getElementById('readiness-missing');
      if(rm&&m.missing&&m.missing.length){
        rm.innerHTML=m.missing.map(function(s){return '<div>\\u2022 '+esc(s)+'</div>';}).join('');
      }
    }
  }
  var dq=G.nodes.find(function(n){return n.type==='decision_queue';});
  if(dq){
    var dm=dq.metadata||{};
    var el2=document.getElementById('info-decisions');
    if(el2)el2.textContent='Decisions: '+(dm.open_count!=null?dm.open_count:'\\u2014');
    var ds2=document.getElementById('decision-section');
    if(ds2&&dm.open_count>0){
      ds2.style.display='block';
      var dc=document.getElementById('decision-count');
      if(dc)dc.textContent=String(dm.open_count);
    }
  }
  var wa=G.nodes.find(function(n){return n.type==='worker_adapter';});
  if(wa){
    var wm=wa.metadata||{};
    var el3=document.getElementById('info-worker');
    if(el3)el3.textContent='Worker: '+(wm.worker||wm.recommended_worker||'\\u2014');
  }
  var tp=G.nodes.find(function(n){return n.type==='token_policy';});
  if(tp){
    var tm=tp.metadata||{};
    var el4=document.getElementById('info-token-mode');
    if(el4)el4.textContent='Token: '+(tm.mode||'\\u2014');
  }
  var gs=G.nodes.find(function(n){return n.type==='git_status';});
  if(gs){
    var gm=gs.metadata||{};
    var el5=document.getElementById('info-git');
    if(el5)el5.textContent='Git: '+(gm.branch||'\\u2014');
  }
})();
// ── Proof chain ──
(function(){
  var pc=document.getElementById('proof-chain');
  if(!pc)return;
  var verified=G.nodes.filter(function(n){return n.status==='completed'||n.status==='passed';});
  if(!verified.length){pc.innerHTML='<span style="color:var(--remedy-fg-muted);font-size:11px">No verified steps yet</span>';return;}
  var h='';
  verified.slice(0,12).forEach(function(n,i){
    if(i>0)h+='<span class="chain-arrow">\\u2192</span>';
    h+='<span class="chain-step">'+esc(n.label.length>18?n.label.slice(0,17)+'\\u2026':n.label)+'</span>';
  });
  if(verified.length>12)h+='<span class="chain-arrow">\\u2026 +'+(verified.length-12)+'</span>';
  pc.innerHTML=h;
})();
// ── Timeline ──
(function(){
  var tl=document.getElementById('timeline');
  if(!tl)return;
  var evts=G.nodes.filter(function(n){return n.type==='run_event'||n.type==='agent_loop';});
  if(!evts.length){tl.innerHTML='<span style="color:var(--remedy-fg-muted);font-size:10px">No events</span>';return;}
  var h='';
  evts.slice(0,15).forEach(function(n,i){
    if(i>0)h+='<span class="tl-dot"></span>';
    h+='<span class="tl-event">'+esc(n.label.length>20?n.label.slice(0,19)+'\\u2026':n.label)+'</span>';
  });
  if(evts.length>15)h+='<span class="tl-dot"></span><span class="tl-event">+'+(evts.length-15)+' more</span>';
  tl.innerHTML=h;
})();
// ── Guidance rail ──
(function(){
  var gr=document.getElementById('guidance-rail');
  if(!gr)return;
  var cards=[];
  var blocked=G.nodes.filter(function(n){return n.status==='blocked'||n.status==='failed';});
  if(blocked.length)cards.push({sev:'high',text:blocked.length+' blocker(s)'});
  var dq=G.nodes.find(function(n){return n.type==='decision_queue';});
  if(dq&&dq.metadata&&dq.metadata.open_count>0)cards.push({sev:'high',text:dq.metadata.open_count+' decision(s) pending'});
  var ar=G.nodes.find(function(n){return n.type==='autonomy_readiness';});
  if(ar&&ar.metadata)cards.push({sev:'info',text:'Readiness L'+ar.metadata.level});
  var tp2=G.nodes.find(function(n){return n.type==='token_policy';});
  if(tp2&&tp2.metadata)cards.push({sev:'info',text:'Token: '+(tp2.metadata.mode||'default')});
  if(!cards.length){gr.style.display='none';return;}
  var h='';
  cards.forEach(function(c){
    h+='<div class="guide-card '+c.sev+'">'+esc(c.text)+'</div>';
  });
  gr.innerHTML=h;
})();
setRenderStatus(G.nodes.length===0?'empty':'ready');
}catch(e){
  _vErr('render',e&&e.message?e.message:'unknown error');
}
})();
setTimeout(function(){
  var s=document.body.getAttribute('data-render-status');
  if(s==='static-fallback'||s==='loading'){_vErr('timeout','render did not complete');}
},2000);
</script>
</body>
</html>"""
