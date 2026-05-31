"""
UI App Shell (Legacy Fallback) — inline HTML shell for the Remedy localhost UI.

**Status: Legacy fallback.**  The primary UI is now the PixiJS-based semantic
brain canvas served from built assets in ``apps/ui/dist/``.  This module is
used only as a fallback when the built frontend is not available.

Produces a self-contained HTML page with embedded CSS/JS that fetches
job data from the localhost API endpoints.  No external assets, CDN,
npm, or build step.

Step 166: Journey graph layout (left-to-right forward journey).
Step 168: Task ribbon as real checklist.
Step 171: Visual polish v1 — calm premium default.

Public API::

    build_app_shell(job_id, token) -> str
"""

from __future__ import annotations


def build_app_shell(job_id: str, token: str) -> str:
    """Return the full HTML app shell with embedded CSS and JS."""
    return _APP_HTML.replace("__JOB_ID__", job_id).replace("__TOKEN__", token)


# ---------------------------------------------------------------------------
# App Shell HTML — Steps 166, 168, 171
# ---------------------------------------------------------------------------

_APP_HTML = r"""<!DOCTYPE html>
<html lang="en" class="remedy-light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remedy</title>
<style>
/* ── CSS Variables — Light/Calm Premium ──────────────────────────── */
:root {
  --remedy-bg: linear-gradient(135deg, #f8f9fc 0%, #eef1f6 100%);
  --remedy-bg-flat: #f4f7fa;
  --remedy-surface: #ffffff;
  --remedy-surface-hover: #fafbfd;
  --remedy-text: #1a2332;
  --remedy-text-muted: #6b7a8d;
  --remedy-text-faint: #9aa5b4;
  --remedy-teal: #0a9396;
  --remedy-cyan: #94d2bd;
  --remedy-line: #e2e8f0;
  --remedy-line-light: #edf2f7;
  --remedy-proof: #2d8a5e;
  --remedy-risk: #d45050;
  --remedy-warning: #c4820a;
  --remedy-memory: #7a68b8;
  --remedy-radius: 12px;
  --remedy-radius-sm: 8px;
  --remedy-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03);
  --remedy-shadow-node: 0 2px 8px rgba(0,0,0,0.06);
  --remedy-shadow-lg: 0 4px 16px rgba(0,0,0,0.06);
  --remedy-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --remedy-mono: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  --remedy-glow: rgba(10, 147, 150, 0.15);
  --remedy-node-done: #e8f5ee;
  --remedy-node-current: #e5f6f6;
  --remedy-node-blocked: #fce8e8;
  --remedy-node-pending: #f0f3f7;
}
.remedy-dark {
  --remedy-bg: linear-gradient(135deg, #0e1420 0%, #141e2e 100%);
  --remedy-bg-flat: #0e1420;
  --remedy-surface: #1a2332;
  --remedy-surface-hover: #1e2a3a;
  --remedy-text: #e0e8f0;
  --remedy-text-muted: #8898a8;
  --remedy-text-faint: #5a6a7a;
  --remedy-teal: #38c8c8;
  --remedy-cyan: #5ad4b4;
  --remedy-line: #2a3848;
  --remedy-line-light: #1e2e3e;
  --remedy-proof: #38c878;
  --remedy-risk: #e05252;
  --remedy-warning: #e8a838;
  --remedy-memory: #9898e8;
  --remedy-shadow: 0 1px 3px rgba(0,0,0,0.2);
  --remedy-shadow-node: 0 2px 8px rgba(0,0,0,0.2);
  --remedy-shadow-lg: 0 4px 16px rgba(0,0,0,0.3);
  --remedy-glow: rgba(56, 200, 200, 0.2);
  --remedy-node-done: rgba(56,200,120,0.08);
  --remedy-node-current: rgba(56,200,200,0.08);
  --remedy-node-blocked: rgba(224,82,82,0.08);
  --remedy-node-pending: rgba(200,210,220,0.05);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--remedy-font);
  background: var(--remedy-bg);
  color: var(--remedy-text);
  line-height: 1.6;
  min-height: 100vh;
}
/* ── Layout ──────────────────────────────────────────────────────── */
.remedy-journey-shell {
  display: grid;
  grid-template-columns: 260px 1fr;
  grid-template-rows: auto 1fr;
  min-height: 100vh;
}
/* ── Header ──────────────────────────────────────────────────────── */
.remedy-header {
  grid-column: 1 / -1;
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 24px;
  background: var(--remedy-surface);
  border-bottom: 1px solid var(--remedy-line);
}
.remedy-logo { font-size: 18px; font-weight: 700; color: var(--remedy-teal); letter-spacing: -0.3px; }
.remedy-headline { font-size: 14px; color: var(--remedy-text-muted); margin-left: 16px; flex: 1; }
.remedy-status-badge {
  display: inline-block; padding: 3px 10px; border-radius: 12px;
  font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.4px;
}
.status-done { background: rgba(45,138,94,0.08); color: var(--remedy-proof); }
.status-current { background: rgba(10,147,150,0.08); color: var(--remedy-teal); }
.status-blocked { background: rgba(212,80,80,0.08); color: var(--remedy-risk); }
.status-pending { background: rgba(107,122,141,0.08); color: var(--remedy-text-muted); }
/* ── Checklist (left ribbon) ─────────────────────────────────────── */
.remedy-checklist {
  padding: 16px;
  background: var(--remedy-surface);
  border-right: 1px solid var(--remedy-line);
  overflow-y: auto;
}
.checklist-title {
  font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px;
  color: var(--remedy-text-faint); margin-bottom: 12px;
}
.checklist-item {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 8px 10px; margin-bottom: 4px;
  border-radius: var(--remedy-radius-sm);
  cursor: pointer; transition: background 0.12s;
  font-size: 13px; line-height: 1.4;
}
.checklist-item:hover { background: var(--remedy-surface-hover); }
.checklist-item.item-current { background: var(--remedy-node-current); font-weight: 500; }
.checklist-item.item-blocked { color: var(--remedy-risk); }
.checklist-item.item-done { color: var(--remedy-text-muted); }
.checklist-item.item-suggested { color: var(--remedy-text-faint); font-style: italic; }
.checklist-item.item-muted { opacity: 0.5; }
.check-icon {
  width: 18px; height: 18px; border-radius: 50%;
  border: 2px solid var(--remedy-line);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; margin-top: 1px; font-size: 10px;
}
.check-icon.checked { background: var(--remedy-proof); border-color: var(--remedy-proof); color: #fff; }
.check-icon.current { border-color: var(--remedy-teal); }
.check-icon.blocked { border-color: var(--remedy-risk); }
.checklist-label { flex: 1; }
.checklist-kind {
  font-size: 9px; text-transform: uppercase; letter-spacing: 0.5px;
  color: var(--remedy-text-faint); margin-top: 2px;
}
/* ── Main content area ───────────────────────────────────────────── */
.remedy-main {
  display: flex; flex-direction: column; overflow: hidden;
  padding: 24px;
}
/* ── Progress bar ────────────────────────────────────────────────── */
.remedy-progress {
  display: flex; gap: 16px; margin-bottom: 24px;
}
.progress-stat {
  background: var(--remedy-surface);
  border: 1px solid var(--remedy-line);
  border-radius: var(--remedy-radius-sm);
  padding: 12px 16px;
  box-shadow: var(--remedy-shadow);
  min-width: 100px;
}
.progress-stat .stat-value { font-size: 20px; font-weight: 700; }
.progress-stat .stat-label { font-size: 11px; color: var(--remedy-text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
/* ── Journey graph ───────────────────────────────────────────────── */
.remedy-graph-area {
  flex: 1; min-height: 300px; position: relative;
  background: var(--remedy-surface);
  border: 1px solid var(--remedy-line);
  border-radius: var(--remedy-radius);
  box-shadow: var(--remedy-shadow);
  overflow: hidden;
}
.remedy-graph-area svg { width: 100%; height: 100%; display: block; }
/* Journey nodes */
.journey-node {
  cursor: pointer; transition: transform 0.12s;
}
.journey-node rect {
  rx: 8; ry: 8; stroke-width: 1.5;
  transition: stroke 0.12s, filter 0.12s;
}
.journey-node:hover rect {
  stroke: var(--remedy-teal); filter: drop-shadow(0 0 4px var(--remedy-glow));
}
.remedy-node-done rect { fill: var(--remedy-node-done); stroke: var(--remedy-proof); }
.remedy-node-current rect { fill: var(--remedy-node-current); stroke: var(--remedy-teal); stroke-width: 2; filter: drop-shadow(0 0 6px var(--remedy-glow)); }
.remedy-node-blocked rect { fill: var(--remedy-node-blocked); stroke: var(--remedy-risk); }
.remedy-node-pending rect { fill: var(--remedy-node-pending); stroke: var(--remedy-line); }
.journey-node text {
  font-size: 11px; fill: var(--remedy-text);
  text-anchor: middle; pointer-events: none;
}
.journey-node .node-subtitle {
  font-size: 9px; fill: var(--remedy-text-muted);
}
/* Journey edges */
.journey-edge { stroke: var(--remedy-line); stroke-width: 1.5; fill: none; }
.journey-edge.edge-done { stroke: var(--remedy-proof); opacity: 0.5; }
.journey-edge.edge-current { stroke: var(--remedy-teal); }
/* Selected */
.journey-node.selected rect { stroke: var(--remedy-teal); stroke-width: 2.5; }
/* ── Detail card (compact) ───────────────────────────────────────── */
.remedy-detail-compact {
  display: none;
  background: var(--remedy-surface);
  border: 1px solid var(--remedy-line);
  border-radius: var(--remedy-radius);
  box-shadow: var(--remedy-shadow-lg);
  padding: 20px; margin-top: 16px;
  max-width: 480px;
}
.remedy-detail-compact.visible { display: block; }
.detail-c-title { font-size: 16px; font-weight: 600; margin-bottom: 4px; }
.detail-c-state { font-size: 12px; color: var(--remedy-text-muted); margin-bottom: 12px; }
.detail-c-summary { font-size: 13px; line-height: 1.5; margin-bottom: 12px; }
.detail-c-section { margin-bottom: 10px; }
.detail-c-section h4 {
  font-size: 10px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.6px; color: var(--remedy-text-faint); margin-bottom: 4px;
}
.detail-c-section p { font-size: 12px; color: var(--remedy-text-muted); }
.detail-c-action {
  display: inline-block; padding: 6px 14px; border-radius: 6px;
  border: 1px solid var(--remedy-teal); color: var(--remedy-teal);
  font-size: 12px; font-family: var(--remedy-mono);
  background: transparent; cursor: pointer; margin-top: 8px;
}
.detail-c-action:hover { background: rgba(10,147,150,0.06); }
/* ── Layer switcher ──────────────────────────────────────────────── */
.remedy-layer-switcher {
  display: flex; gap: 4px; margin-bottom: 16px;
}
.layer-btn {
  padding: 4px 12px; border-radius: 6px;
  border: 1px solid var(--remedy-line);
  background: transparent; color: var(--remedy-text-muted);
  font-size: 11px; cursor: pointer;
  transition: all 0.12s;
}
.layer-btn:hover { border-color: var(--remedy-teal); color: var(--remedy-teal); }
.layer-btn.active { background: rgba(10,147,150,0.06); border-color: var(--remedy-teal); color: var(--remedy-teal); font-weight: 600; }
.layer-btn:focus-visible { outline: 2px solid var(--remedy-teal); outline-offset: 2px; }
/* ── Footer ──────────────────────────────────────────────────────── */
.remedy-footer {
  grid-column: 1 / -1;
  padding: 6px 24px; font-size: 10px; color: var(--remedy-text-faint);
  border-top: 1px solid var(--remedy-line); background: var(--remedy-surface);
}
/* ── Utilities ───────────────────────────────────────────────────── */
.theme-toggle {
  background: none; border: 1px solid var(--remedy-line); border-radius: 6px;
  padding: 3px 8px; font-size: 12px; cursor: pointer; color: var(--remedy-text-muted);
}
.remedy-loading { text-align: center; padding: 48px; color: var(--remedy-text-muted); }
.remedy-error { text-align: center; padding: 48px; color: var(--remedy-risk); }
/* ── Reduced Motion ──────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; animation: none !important; }
}
/* ── Narrow ──────────────────────────────────────────────────────── */
@media (max-width: 720px) {
  .remedy-journey-shell { grid-template-columns: 1fr; }
  .remedy-checklist { display: none; }
  .remedy-main { padding: 12px; }
}
</style>
</head>
<body>
<div class="remedy-journey-shell" id="shell">
  <div class="remedy-loading" id="loading">Loading...</div>
</div>
<script>
(function() {
  "use strict";
  var JOB_ID = "__JOB_ID__";
  var TOKEN = "__TOKEN__";
  var API = "/api/jobs/" + JOB_ID + "/";
  var selectedNode = null;
  var currentLayer = "journey";

  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  function $(id) { return document.getElementById(id); }
  function fetchJSON(endpoint, cb) {
    var url = API + endpoint + "?token=" + TOKEN;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onload = function() {
      if (xhr.status === 200) cb(null, JSON.parse(xhr.responseText));
      else cb("HTTP " + xhr.status);
    };
    xhr.onerror = function() { cb("network error"); };
    xhr.send();
  }

  // ── Build UI ──────────────────────────────────────────────────────
  function buildUI(story, checklist) {
    var shell = $("shell");
    var sLabel = story.plain_status || "Unknown";
    var sCls = "status-pending";
    if (sLabel === "Done" || sLabel === "Completed") sCls = "status-done";
    else if (sLabel === "In progress") sCls = "status-current";
    else if (sLabel === "Blocked" || sLabel === "Failed") sCls = "status-blocked";

    var html = '<header class="remedy-header">' +
      '<div><span class="remedy-logo">Remedy</span>' +
      '<span class="remedy-headline">' + esc(story.headline || "") + '</span></div>' +
      '<div><span class="remedy-status-badge ' + sCls + '">' + esc(sLabel) + '</span>' +
      ' <button class="theme-toggle" onclick="toggleTheme()">&#9789;</button></div></header>';

    // Checklist
    html += '<div class="remedy-checklist"><div class="checklist-title">Progress</div>';
    var items = (checklist && checklist.items) || [];
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      var iCls = "checklist-item";
      var cCls = "check-icon";
      var icon = "";
      if (it.checked) { cCls += " checked"; icon = "&#10003;"; iCls += " item-done"; }
      else if (it.state === "current") { cCls += " current"; iCls += " item-current"; }
      else if (it.state === "blocked") { cCls += " blocked"; iCls += " item-blocked"; }
      else if (it.state === "suggested") { iCls += " item-suggested"; }
      if (it.muted) iCls += " item-muted";
      html += '<div class="' + iCls + '" data-nid="' + esc(it.node_id || "") + '" onclick="pickNode(\'' + esc(it.node_id || "") + '\')">' +
        '<div class="' + cCls + '">' + icon + '</div>' +
        '<div><div class="checklist-label">' + esc(it.label) + '</div>' +
        '<div class="checklist-kind">' + esc(it.kind || "") + '</div></div></div>';
    }
    html += '</div>';

    // Main
    html += '<div class="remedy-main">';

    // Layer switcher
    html += '<div class="remedy-layer-switcher" id="layer-switcher">' +
      '<button class="layer-btn active" data-layer="journey" onclick="setLayer(\'journey\')">Journey</button>' +
      '<button class="layer-btn" data-layer="proof" onclick="setLayer(\'proof\')">Proof</button>' +
      '<button class="layer-btn" data-layer="review" onclick="setLayer(\'review\')">Review</button>' +
      '<button class="layer-btn" data-layer="diagnostics" onclick="setLayer(\'diagnostics\')">Diagnostics</button>' +
      '</div>';

    // Progress stats
    var p = story.progress || {};
    html += '<div class="remedy-progress">' +
      '<div class="progress-stat"><div class="stat-value">' + (p.completed || 0) + '</div><div class="stat-label">Done</div></div>' +
      '<div class="progress-stat"><div class="stat-value">' + (p.active || 0) + '</div><div class="stat-label">Active</div></div>' +
      '<div class="progress-stat"><div class="stat-value">' + (p.pending || 0) + '</div><div class="stat-label">Pending</div></div>' +
      '<div class="progress-stat"><div class="stat-value">' + (p.blocked || 0) + '</div><div class="stat-label">Blocked</div></div>';
    if (p.needs_review) html += '<div class="progress-stat"><div class="stat-value">' + p.needs_review + '</div><div class="stat-label">Review</div></div>';
    html += '</div>';

    // Graph area
    html += '<div class="remedy-graph-area" id="graph-area"><svg id="journey-svg"></svg></div>';

    // Detail card
    html += '<div class="remedy-detail-compact" id="detail-card">' +
      '<div class="detail-c-title" id="dc-title"></div>' +
      '<div class="detail-c-state" id="dc-state"></div>' +
      '<div class="detail-c-summary" id="dc-summary"></div>' +
      '<div class="detail-c-section" id="dc-why"><h4>Why it matters</h4><p id="dc-why-text"></p></div>' +
      '<div class="detail-c-section" id="dc-evidence"><h4>Evidence</h4><p id="dc-evidence-text"></p></div>' +
      '<button class="detail-c-action" id="dc-action" onclick="copyAction()" style="display:none"></button>' +
      '</div>';

    html += '</div>'; // main

    // Footer
    html += '<div class="remedy-footer">Remedy &middot; read-only &middot; localhost &middot; no external assets</div>';

    shell.innerHTML = html;

    // Render journey graph
    renderJourney(story.journey || []);
  }

  // ── Journey graph renderer (left-to-right) ─────────────────────────
  function renderJourney(journey) {
    var svg = $("journey-svg");
    if (!svg) return;
    var area = $("graph-area");
    var W = area.clientWidth || 800, H = area.clientHeight || 400;
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);

    if (!journey.length) {
      svg.innerHTML = '<text x="' + W/2 + '" y="' + H/2 + '" text-anchor="middle" fill="var(--remedy-text-faint)" font-size="14">No journey data</text>';
      return;
    }

    // Group by kind for left-to-right layout
    var kindOrder = ["goal","task","change","approval","apply","test","proof","review","memory","decision"];
    var groups = {};
    for (var i = 0; i < journey.length; i++) {
      var j = journey[i];
      var k = j.kind || "task";
      if (!groups[k]) groups[k] = [];
      groups[k].push(j);
    }

    // Position nodes
    var nodeW = 120, nodeH = 48, padX = 40, padY = 24;
    var positions = {};
    var colX = padX;
    var allNodes = [];

    for (var ki = 0; ki < kindOrder.length; ki++) {
      var kind = kindOrder[ki];
      var grp = groups[kind];
      if (!grp || !grp.length) continue;
      var colY = (H - grp.length * (nodeH + padY) + padY) / 2;
      for (var ni = 0; ni < grp.length; ni++) {
        var node = grp[ni];
        var x = colX;
        var y = Math.max(padY, colY + ni * (nodeH + padY));
        positions[node.id] = { x: x, y: y, node: node };
        allNodes.push({ x: x, y: y, node: node });
      }
      colX += nodeW + padX;
    }

    // Scale to fit
    var maxX = 0;
    for (var id in positions) {
      if (positions[id].x + nodeW > maxX) maxX = positions[id].x + nodeW;
    }
    var scale = 1;
    if (maxX + padX > W) {
      scale = (W - padX * 2) / (maxX - padX);
    }

    var svgHTML = '';

    // Edges (connect sequential nodes)
    for (var ai = 1; ai < allNodes.length; ai++) {
      var prev = allNodes[ai - 1];
      var curr = allNodes[ai];
      var x1 = (prev.x + nodeW) * scale;
      var y1 = (prev.y + nodeH / 2) * scale;
      var x2 = curr.x * scale;
      var y2 = (curr.y + nodeH / 2) * scale;
      var eCls = "journey-edge";
      if (prev.node.state === "done") eCls += " edge-done";
      else if (prev.node.state === "current") eCls += " edge-current";
      // Arrow marker
      svgHTML += '<line class="' + eCls + '" x1="' + x1 + '" y1="' + y1 +
        '" x2="' + x2 + '" y2="' + y2 + '" marker-end="url(#arrow)"/>';
    }

    // Arrow marker def
    svgHTML = '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">' +
      '<path d="M 0 0 L 10 5 L 0 10 z" fill="var(--remedy-line)"/></marker></defs>' + svgHTML;

    // Nodes
    for (var bi = 0; bi < allNodes.length; bi++) {
      var an = allNodes[bi];
      var nx = an.x * scale;
      var ny = an.y * scale;
      var nw = nodeW * scale;
      var nh = nodeH * scale;
      var nCls = "journey-node";
      if (an.node.state === "done") nCls += " remedy-node-done";
      else if (an.node.state === "current") nCls += " remedy-node-current";
      else if (an.node.state === "blocked") nCls += " remedy-node-blocked";
      else nCls += " remedy-node-pending";
      if (selectedNode === an.node.id) nCls += " selected";

      var title = (an.node.title || "").substring(0, 16);
      var subtitle = (an.node.subtitle || "").substring(0, 20);

      svgHTML += '<g class="' + nCls + '" onclick="pickNode(\'' + esc(an.node.id) + '\')" tabindex="0">' +
        '<rect x="' + nx + '" y="' + ny + '" width="' + nw + '" height="' + nh + '"/>' +
        '<text x="' + (nx + nw/2) + '" y="' + (ny + nh/2 - 4) + '">' + esc(title) + '</text>' +
        '<text class="node-subtitle" x="' + (nx + nw/2) + '" y="' + (ny + nh/2 + 10) + '">' + esc(subtitle) + '</text>' +
        '</g>';
    }

    svg.innerHTML = svgHTML;
  }

  // ── Node selection ─────────────────────────────────────────────────
  window.pickNode = function(nodeId) {
    if (!nodeId) return;
    selectedNode = nodeId;
    var card = $("detail-card");
    card.classList.add("visible");
    $("dc-title").textContent = "Loading...";
    $("dc-state").textContent = "";
    $("dc-summary").textContent = "";
    $("dc-why-text").textContent = "";
    $("dc-evidence-text").textContent = "";
    var actionBtn = $("dc-action");
    if (actionBtn) actionBtn.style.display = "none";

    fetchJSON("nodes/" + encodeURIComponent(nodeId) + "/human-detail", function(err, d) {
      if (err || !d || d.error) {
        $("dc-title").textContent = nodeId.substring(0, 20);
        $("dc-summary").textContent = "Detail unavailable.";
        return;
      }
      $("dc-title").textContent = d.title || "";
      $("dc-state").textContent = d.state || "";
      $("dc-summary").textContent = d.summary || "";
      $("dc-why-text").textContent = d.why_it_matters || "";
      var ev = (d.evidence || []).join("; ");
      $("dc-evidence-text").textContent = ev || "None";
      var na = d.next_action || {};
      if (na.command) {
        actionBtn.textContent = na.command;
        actionBtn.style.display = "inline-block";
        actionBtn._cmd = na.command;
      }
    });
  };

  window.copyAction = function() {
    var btn = $("dc-action");
    if (btn && btn._cmd && navigator.clipboard) {
      navigator.clipboard.writeText(btn._cmd).catch(function(){});
    }
  };

  // ── Layer switching ────────────────────────────────────────────────
  window.setLayer = function(layer) {
    currentLayer = layer;
    var btns = document.querySelectorAll(".layer-btn");
    for (var i = 0; i < btns.length; i++) {
      btns[i].classList.toggle("active", btns[i].getAttribute("data-layer") === layer);
    }
    // In this fallback shell, only journey is rendered; others show message
    if (layer !== "journey") {
      var svg = $("journey-svg");
      if (svg) {
        var area = $("graph-area");
        var W = area.clientWidth || 800, H = area.clientHeight || 400;
        svg.setAttribute("viewBox", "0 0 " + W + " " + H);
        svg.innerHTML = '<text x="' + W/2 + '" y="' + H/2 + '" text-anchor="middle" fill="var(--remedy-text-faint)" font-size="14">' +
          esc(layer.charAt(0).toUpperCase() + layer.slice(1)) + ' layer — available in full UI build</text>';
      }
    } else if (window._lastJourney) {
      renderJourney(window._lastJourney);
    }
  };

  // ── Theme ──────────────────────────────────────────────────────────
  window.toggleTheme = function() {
    document.documentElement.classList.toggle("remedy-dark");
    document.documentElement.classList.toggle("remedy-light");
  };

  // ── Init ───────────────────────────────────────────────────────────
  var loadedStory = null, loadedChecklist = null;
  var pending = 2;
  function tryRender() {
    pending--;
    if (pending <= 0 && loadedStory) {
      buildUI(loadedStory, loadedChecklist || { items: [] });
      window._lastJourney = loadedStory.journey || [];
    }
  }

  fetchJSON("story", function(err, data) {
    if (err) { $("shell").innerHTML = '<div class="remedy-error">Failed to load story (' + esc(err) + ')</div>'; return; }
    loadedStory = data;
    tryRender();
  });
  fetchJSON("checklist", function(err, data) {
    loadedChecklist = data;
    tryRender();
  });

  // Keyboard
  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") {
      selectedNode = null;
      var card = $("detail-card");
      if (card) card.classList.remove("visible");
    }
  });

})();
</script>
</body>
</html>"""
