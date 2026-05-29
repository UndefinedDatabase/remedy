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
    "mcp_placeholder": 4,
    "project_placeholder": 1,
    "patch_apply": 4,
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
        except Exception:
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
    return (
        _HTML
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
<title>Remedy Brain Viewer v0 — __JOB_SHORT_ID__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d1117;color:#c9d1d9;font-family:ui-monospace,SFMono-Regular,monospace;
     display:flex;flex-direction:column;height:100vh;overflow:hidden}
#hdr{background:#161b22;padding:9px 16px;display:flex;align-items:center;gap:10px;
     border-bottom:1px solid #21262d;flex-shrink:0}
#hdr h1{font-size:14px;font-weight:bold;color:#c9d1d9}
.badge{background:#1f2937;color:#7aa7e8;padding:2px 8px;border-radius:4px;
       font-size:11px;border:1px solid #2d3748}
.badge-warn{background:#2d1a08;color:#ffaa44;border-color:#4a2d10}
#render-badge[data-status="ready"]{background:#0a2a0a;color:#3fb950;border-color:#1a4a1a}
#render-badge[data-status="error"]{background:#2d1a08;color:#ffaa44;border-color:#4a2d10}
#render-badge[data-status="empty"]{background:#1a1a2d;color:#7aa7e8;border-color:#2d3a5a}
#render-badge[data-status="static-fallback"]{background:#1a1a2d;color:#8b949e;border-color:#2d3748}
#static-fallback{padding:12px 16px;background:#0d1117;border-bottom:1px solid #21262d;
  font-size:12px;overflow-y:auto;max-height:200px;flex-shrink:0}
.sf-sum{display:flex;gap:12px;margin-bottom:8px;flex-wrap:wrap}
.sf-sum span{color:#8b949e}.sf-sum b{color:#c9d1d9}
.sf-tbl{border-collapse:collapse;font-size:11px}
.sf-tbl th,.sf-tbl td{padding:2px 8px;text-align:left;border:1px solid #21262d}
.sf-tbl th{color:#484f58;font-weight:normal}
.sf-tbl td{color:#8b949e}
.sf-trunc{margin-top:4px;color:#484f58;font-size:10px;font-style:italic}
#main{display:flex;flex:1;overflow:hidden;min-height:0}
#gwrap{flex:1;position:relative;overflow:hidden}
svg#g{width:100%;height:100%;display:block}
#err-panel{display:none;position:absolute;top:10px;left:10px;right:10px;
  background:#1a0e08;color:#ffb347;border:1px solid #4a2d10;
  border-radius:6px;padding:10px 14px;font-size:12px;z-index:10}
#dp{width:330px;background:#161b22;border-left:1px solid #21262d;
    padding:12px;overflow-y:auto;font-size:12px;flex-shrink:0}
#dh{color:#484f58;padding:24px 0;text-align:center;font-size:13px}
.dt{font-size:14px;font-weight:bold;color:#7aa7e8;margin-bottom:8px;word-break:break-all}
.dr{margin:3px 0}.dl{color:#484f58}.dv{color:#c9d1d9}
.ds{margin:8px 0 3px;color:#7aa7e8;border-bottom:1px solid #21262d;
    padding-bottom:2px;font-size:10px;text-transform:uppercase;letter-spacing:.06em}
.di{margin:2px 0 2px 8px;color:#8b949e;word-break:break-all}
.drd{color:#6e4c2e;font-style:italic}
#leg{background:#161b22;padding:5px 16px;border-top:1px solid #21262d;
     display:flex;gap:14px;font-size:10px;flex-wrap:wrap;
     align-items:center;flex-shrink:0}
.li{display:flex;align-items:center;gap:4px}
.ld{width:11px;height:11px;border-radius:50%;border:1px solid #30363d}
#diag{background:#0d1117;padding:3px 16px;border-top:1px solid #21262d;
  font-size:10px;color:#484f58;display:flex;gap:14px;flex-wrap:wrap;
  align-items:center;flex-shrink:0}
#diag b{color:#30363d}
#diag span{color:#8b949e}
#ftr{background:#161b22;padding:3px 16px;font-size:10px;color:#30363d;
     border-top:1px solid #21262d;flex-shrink:0}
.el{stroke:#2d3748;stroke-width:1.5}
.nd{cursor:pointer}
.nd circle{stroke-width:2;transition:stroke .15s,stroke-width .15s}
.nd:hover circle,.nd.sel circle{stroke:#c9d1d9 !important;stroke-width:3}
.nd text{font-size:9px;fill:#8b949e;pointer-events:none;text-anchor:middle}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
.nd.run circle{animation:pulse 1.5s ease-in-out infinite}
</style>
</head>
<body data-render-status="static-fallback">
<div id="hdr">
  <h1>Remedy Brain Viewer</h1>
  <span class="badge badge-warn">read-only &middot; v0</span>
  <span class="badge">job __JOB_SHORT_ID__</span>
  <span class="badge">__GENERATED_AT__</span>
  <span class="badge" id="ctx-badge">Context: —%</span>
  <span class="badge" id="render-badge" data-status="static-fallback">● static</span>
</div>
<div id="static-fallback">
__STATIC_FALLBACK__
</div>
<div id="main">
  <div id="gwrap">
    <svg id="g"></svg>
    <div id="err-panel" style="display:none"><strong>Viewer error</strong> — <span id="err-msg"></span></div>
  </div>
  <div id="dp">
    <p id="dh">&larr; Click a node to inspect it</p>
    <div id="db" style="display:none"></div>
  </div>
</div>
<div id="leg">
  <strong style="color:#484f58">Legend:</strong>
  <div class="li"><div class="ld" style="background:#6e7681"></div>pending</div>
  <div class="li"><div class="ld" style="background:#4488ff"></div>running</div>
  <div class="li"><div class="ld" style="background:#d0d7de;border-color:#6e7681"></div>completed</div>
  <div class="li"><div class="ld" style="background:#cf4444"></div>blocked</div>
  <div class="li"><div class="ld" style="background:#d9a520"></div>needs approval</div>
  <div class="li"><div class="ld" style="background:#7c4fb0"></div>memory layer (future)</div>
  <div class="li"><div class="ld" style="background:#e06c1a"></div>mcp quarantine (future)</div>
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
<div id="ftr">Brain Viewer v0 &middot; read-only &middot; consumes remedy brain --json and remedy brain node --json &middot; foundation for React&nbsp;Flow / Three.js / AG-UI / A2UI</div>
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
