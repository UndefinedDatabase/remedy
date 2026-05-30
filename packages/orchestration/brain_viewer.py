"""
Brain Viewer v0 — local read-only static HTML viewer for the Project Brain Graph.

Generates a self-contained index.html (with embedded viewer data) under
REMEDY_DATA_DIR/viewers/<job_id>/.  The viewer consumes only the existing
--json machine contracts (export_project_brain_json and
export_brain_node_detail_json) and renders nodes/edges in a 2D visual.

IMPORTANT — Scope limitations (v0):
  Read-only only.  No repo mutation, no patch apply, no permission mutation,
  no shell/subprocess/Git/Docker/network/MCP/Claude execution, no memory
  writes, no frontend framework.  This is the foundation for future
  React Flow / Three.js / AG-UI / A2UI integration.

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
# Radial layout constants
# ---------------------------------------------------------------------------

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
    """Export viewer data as a JSON-serialisable dict.

    Schema::

        {
            "version": 1,
            "job_id": "<uuid>",
            "generated_at": "<iso>",
            "graph": { ... },                // export_project_brain_json output
            "node_details": { ... },         // node_id -> export_brain_node_detail_json output
            "positions": { ... },            // node_id -> [x, y]
            "detail_fallback_count": <int>,  // nodes that used fallback detail
        }

    Redaction: same policy as build_brain_viewer_data.
    """
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

    # Escape </script> to prevent tag break in both data island and execution script.
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
    """Assign 2D positions using a layered radial layout.

    Returns {node_id: [x, y]} in a nominal 1000x700 coordinate space.
    The JavaScript renderer scales these to fit the actual viewport.
    """
    by_layer: dict[int, list[dict[str, Any]]] = {}
    for node in nodes:
        layer = _LAYER_MAP.get(node["type"], 3)
        by_layer.setdefault(layer, []).append(node)

    positions: dict[str, list[float]] = {}
    for layer_idx, layer_nodes in sorted(by_layer.items()):
        r = (
            _LAYER_RADIUS[layer_idx]
            if layer_idx < len(_LAYER_RADIUS)
            else _LAYER_RADIUS[-1] + 80.0
        )
        count = len(layer_nodes)
        for i, node in enumerate(layer_nodes):
            if r == 0.0:
                x, y = _CX, _CY
            elif count == 1:
                angle = -math.pi / 2.0
                x = round(_CX + r * math.cos(angle), 1)
                y = round(_CY + r * math.sin(angle), 1)
            else:
                angle = (2.0 * math.pi * i / count) - math.pi / 2.0
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
        .replace("__VIEWER_DATA_JSON__", viewer_json_str)  # must precede __STATIC_FALLBACK__
        .replace("__STATIC_FALLBACK__", static_fallback_html)
        .replace("__JOB_SHORT_ID__", job_short_id)
        .replace("__GENERATED_AT__", generated_at)
    )


# ---------------------------------------------------------------------------
# HTML template  (placeholders: __VIEWER_DATA_JSON__, __STATIC_FALLBACK__,
#                              __JOB_SHORT_ID__, __GENERATED_AT__)
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
#hdr{background:var(--remedy-bg-panel);padding:9px 16px;display:flex;align-items:center;gap:10px;
     border-bottom:1px solid var(--remedy-panel-border);flex-shrink:0;z-index:2}
#hdr h1{font-size:14px;font-weight:bold;color:var(--remedy-teal);font-family:var(--remedy-font-sans)}
.badge{background:rgba(56,200,200,0.08);color:var(--remedy-teal);padding:2px 8px;border-radius:4px;
       font-size:11px;border:1px solid var(--remedy-panel-border)}
.badge-warn{background:rgba(232,168,56,0.1);color:var(--remedy-warning);border-color:rgba(232,168,56,0.2)}
#render-badge[data-status="ready"]{background:rgba(56,200,136,0.1);color:var(--remedy-proof);border-color:rgba(56,200,136,0.2)}
#render-badge[data-status="error"]{background:rgba(224,82,82,0.1);color:var(--remedy-risk);border-color:rgba(224,82,82,0.2)}
#render-badge[data-status="empty"]{background:rgba(56,200,200,0.05);color:var(--remedy-fg-muted);border-color:var(--remedy-panel-border)}
#render-badge[data-status="static-fallback"]{background:rgba(58,74,90,0.3);color:var(--remedy-fg-muted);border-color:var(--remedy-muted)}
#info-bar{display:flex;gap:8px;padding:6px 16px;flex-wrap:wrap;font-size:11px;
  border-bottom:1px solid var(--remedy-panel-border);flex-shrink:0;z-index:2;
  background:var(--remedy-bg-panel)}
#info-bar .info-item{padding:3px 10px;border-radius:4px;
  background:rgba(56,200,200,0.04);border:1px solid var(--remedy-panel-border)}
#static-fallback{padding:12px 16px;background:var(--remedy-bg);border-bottom:1px solid var(--remedy-panel-border);
  font-size:12px;overflow-y:auto;max-height:200px;flex-shrink:0;z-index:1}
.sf-sum{display:flex;gap:12px;margin-bottom:8px;flex-wrap:wrap}
.sf-sum span{color:var(--remedy-fg-muted)}.sf-sum b{color:var(--remedy-fg)}
.sf-tbl{border-collapse:collapse;font-size:11px}
.sf-tbl th,.sf-tbl td{padding:2px 8px;text-align:left;border:1px solid var(--remedy-panel-border)}
.sf-tbl th{color:var(--remedy-fg-muted);font-weight:normal}
.sf-tbl td{color:var(--remedy-fg-muted)}
.sf-trunc{margin-top:4px;color:var(--remedy-fg-muted);font-size:10px;font-style:italic}
#main{display:flex;flex:1;overflow:hidden;min-height:0;position:relative}
#gwrap{flex:1;position:relative;overflow:hidden}
svg#g{width:100%;height:100%;display:block}
#err-panel{display:none;position:absolute;top:10px;left:10px;right:10px;
  background:rgba(224,82,82,0.1);color:var(--remedy-risk);border:1px solid rgba(224,82,82,0.3);
  border-radius:6px;padding:10px 14px;font-size:12px;z-index:10}
#side-panels{width:340px;display:flex;flex-direction:column;overflow-y:auto;
  border-left:1px solid var(--remedy-panel-border);flex-shrink:0;
  background:var(--remedy-bg-panel)}
#dp{padding:12px;font-size:12px;flex:1;overflow-y:auto}
#dh{color:var(--remedy-fg-muted);padding:24px 0;text-align:center;font-size:13px}
.dt{font-size:14px;font-weight:bold;color:var(--remedy-teal);margin-bottom:8px;word-break:break-all}
.dr{margin:3px 0}.dl{color:var(--remedy-fg-muted)}.dv{color:var(--remedy-fg)}
.ds{margin:8px 0 3px;color:var(--remedy-teal);border-bottom:1px solid var(--remedy-panel-border);
    padding-bottom:2px;font-size:10px;text-transform:uppercase;letter-spacing:.06em}
.di{margin:2px 0 2px 8px;color:var(--remedy-fg-muted);word-break:break-all}
.drd{color:var(--remedy-muted);font-style:italic}
#proof-chain-panel{padding:0 16px;flex-shrink:0;z-index:1;
  border-bottom:1px solid var(--remedy-panel-border)}
#timeline-panel{padding:0 16px;flex-shrink:0;z-index:1;
  border-bottom:1px solid var(--remedy-panel-border)}
#leg{background:var(--remedy-bg-panel);padding:5px 16px;border-top:1px solid var(--remedy-panel-border);
     display:flex;gap:14px;font-size:10px;flex-wrap:wrap;
     align-items:center;flex-shrink:0;z-index:2}
.li{display:flex;align-items:center;gap:4px}
.ld{width:11px;height:11px;border-radius:50%;border:1px solid var(--remedy-muted)}
#diag{background:var(--remedy-bg);padding:3px 16px;border-top:1px solid var(--remedy-panel-border);
  font-size:10px;color:var(--remedy-fg-muted);display:flex;gap:14px;flex-wrap:wrap;
  align-items:center;flex-shrink:0;z-index:2}
#diag b{color:var(--remedy-muted)}
#diag span{color:var(--remedy-fg-muted)}
#ftr{background:var(--remedy-bg-panel);padding:3px 16px;font-size:10px;color:var(--remedy-muted);
     border-top:1px solid var(--remedy-panel-border);flex-shrink:0;z-index:2}
.el{stroke:var(--remedy-line);stroke-width:1.5}
.nd{cursor:pointer}
.nd circle{stroke-width:2;transition:stroke .15s,stroke-width .15s}
.nd:hover circle,.nd.sel circle{stroke:var(--remedy-teal) !important;stroke-width:3}
.nd text{font-size:9px;fill:var(--remedy-fg-muted);pointer-events:none;text-anchor:middle}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.nd.run circle{animation:pulse 1.5s ease-in-out infinite}
@media (prefers-reduced-motion: reduce) {
  .nd.run circle{animation:none}
  .remedy-particle-field{animation:none !important}
}
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
  <div id="gwrap">
    <svg id="g"></svg>
    <div id="err-panel" style="display:none"><strong>Viewer error</strong> — <span id="err-msg"></span></div>
  </div>
  <div id="side-panels">
    <div id="dp">
      <p id="dh">&larr; Click a node to inspect it</p>
      <div id="db" style="display:none"></div>
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
<div id="ftr">Remedy Brain Viewer &middot; read-only &middot; static export &middot; foundation for future 2D/3D viewer</div>
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
function col(n){
  var t=n.type,s=n.status||'';
  if(t==='memory_placeholder')return'#7c4fb0';
  if(t==='memory')return'#9b6fcf';
  if(t==='autonomy_readiness')return'#2ea043';
  if(t==='context_pack')return'#58a6ff';
  if(t==='mcp_placeholder')return'#e06c1a';
  if(s==='blocked')return'#cf4444';
  if(s==='running')return'#4488ff';
  if(s==='completed'||s==='passed'||s==='loaded')return'#d0d7de';
  if(t==='patch_intent'&&s==='pending')return'#d9a520';
  if(s==='approved')return'#3fb950';
  if(s==='rejected')return'#cf4444';
  if(s==='informational')return'#444c56';
  return'#6e7681';
}
function rad(n){
  if(n.type==='job')return 22;
  if(n.type==='task'||n.type==='artifact'||n.type==='patch_intent'||n.type==='approval_decision')return 15;
  return 11;
}
function esc(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
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
  var h='<g>';
  G.edges.forEach(function(e){
    var s=pm[e.source],t=pm[e.target];
    if(!s||!t)return;
    h+='<line class="el" x1="'+s[0].toFixed(1)+'" y1="'+s[1].toFixed(1)+'" x2="'+t[0].toFixed(1)+'" y2="'+t[1].toFixed(1)+'"/>';
  });
  G.nodes.forEach(function(n){
    var p=pm[n.id];if(!p)return;
    var x=p[0],y=p[1],r=rad(n),c=col(n);
    var cls='nd'+(n.status==='running'?' run':'')+(n.id===selId?' sel':'');
    var stk=n.id===selId?'#c9d1d9':'#30363d';
    var lbl=n.label.length>15?n.label.slice(0,14)+'\\u2026':n.label;
    h+='<g class="'+cls+'" data-nid="'+esc(n.id)+'" onclick="pick(this.dataset.nid)">';
    h+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+r+'" fill="'+c+'" stroke="'+stk+'" stroke-width="2"/>';
    h+='<text x="'+x.toFixed(1)+'" y="'+(y+r+9).toFixed(1)+'">'+esc(lbl)+'</text>';
    h+='</g>';
  });
  h+='</g>';
  svg.innerHTML=h;
}
window.pick=function(nodeId){
  selId=nodeId;render();
  var diagSel=document.getElementById('diag-sel');
  if(diagSel)diagSel.textContent=nodeId||'none';
  document.getElementById('dh').style.display='none';
  var body=document.getElementById('db');
  body.style.display='block';
  var d=DET[nodeId];
  if(!d){body.innerHTML='<p style="color:#484f58">No detail available.</p>';return;}
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
};
window.addEventListener('resize',render);
render();
var dn=document.getElementById('diag-nodes');
var de=document.getElementById('diag-edges');
var dd=document.getElementById('diag-details');
var df=document.getElementById('diag-fallbacks');
if(dn)dn.textContent=G.nodes.length;
if(de)de.textContent=G.edges.length;
if(dd)dd.textContent=Object.keys(DET).length;
if(df)df.textContent=VD.detail_fallback_count||0;
(function(){
  var cc=G.nodes.find(function(n){return n.type==='context_coverage';});
  if(cc&&cc.metadata!=null){
    var el=document.getElementById('ctx-badge');
    if(el)el.textContent='Context: '+cc.metadata.score+'%';
  }
})();
// ── Populate info-bar from graph nodes ──
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
// ── Populate proof chain from verified nodes ──
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
// ── Populate timeline from events in graph ──
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
