"""
UI App Shell — single-page HTML shell for the Remedy localhost UI.

Produces a self-contained HTML page with embedded CSS/JS that fetches
job data from the localhost API endpoints.  No external assets, CDN,
npm, or build step.

Visual direction: bright / white / ice / soft teal.
Calm entry UX — dashboard first, graph behind "Explore Brain" button.

Public API::

    build_app_shell(job_id, token) -> str
"""

from __future__ import annotations


def build_app_shell(job_id: str, token: str) -> str:
    """Return the full HTML app shell with embedded CSS and JS."""
    return _APP_HTML.replace("__JOB_ID__", job_id).replace("__TOKEN__", token)


# ---------------------------------------------------------------------------
# App Shell HTML — calm entry, light theme, progressive brain explorer
# ---------------------------------------------------------------------------

_APP_HTML = r"""<!DOCTYPE html>
<html lang="en" class="remedy-light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Remedy UI</title>
<style>
/* ── CSS Variables — Light/Ice/Teal ────────────────────────────────── */
:root {
  --remedy-bg: #f4f7fa;
  --remedy-surface: #ffffff;
  --remedy-surface-strong: #e8eef4;
  --remedy-text: #1a2332;
  --remedy-text-muted: #5a6a7a;
  --remedy-teal: #0a9396;
  --remedy-cyan: #94d2bd;
  --remedy-line: #d4dce6;
  --remedy-proof: #2d8a5e;
  --remedy-risk: #d45050;
  --remedy-warning: #c4820a;
  --remedy-memory: #7a68b8;
  --remedy-radius: 12px;
  --remedy-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --remedy-shadow-lg: 0 4px 16px rgba(0,0,0,0.08);
  --remedy-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --remedy-mono: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
}

/* ── Dark mode (optional, toggle) ──────────────────────────────────── */
.remedy-dark {
  --remedy-bg: #0e1420;
  --remedy-surface: #1a2332;
  --remedy-surface-strong: #243040;
  --remedy-text: #e0e8f0;
  --remedy-text-muted: #8898a8;
  --remedy-teal: #38c8c8;
  --remedy-cyan: #5ad4b4;
  --remedy-line: #2a3848;
  --remedy-proof: #38c878;
  --remedy-risk: #e05252;
  --remedy-warning: #e8a838;
  --remedy-memory: #9898e8;
  --remedy-shadow: 0 1px 3px rgba(0,0,0,0.3);
  --remedy-shadow-lg: 0 4px 16px rgba(0,0,0,0.4);
}

/* ── Reset & Base ──────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--remedy-font);
  background: var(--remedy-bg);
  color: var(--remedy-text);
  line-height: 1.6;
  min-height: 100vh;
}

/* ── Mist background ───────────────────────────────────────────────── */
.remedy-mist {
  position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(ellipse at 30% 20%, rgba(10,147,150,0.04) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 80%, rgba(148,210,189,0.03) 0%, transparent 50%);
}

/* ── Layout ────────────────────────────────────────────────────────── */
.remedy-app { max-width: 960px; margin: 0 auto; padding: 32px 24px; }
.remedy-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 32px; padding-bottom: 16px;
  border-bottom: 1px solid var(--remedy-line);
}
.remedy-logo { font-size: 20px; font-weight: 600; color: var(--remedy-teal); }
.remedy-job-id { font-family: var(--remedy-mono); font-size: 13px; color: var(--remedy-text-muted); }
.remedy-state-badge {
  display: inline-block; padding: 4px 12px; border-radius: 16px;
  font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
}
.state-completed { background: rgba(45,138,94,0.1); color: var(--remedy-proof); }
.state-running { background: rgba(10,147,150,0.1); color: var(--remedy-teal); }
.state-blocked { background: rgba(212,80,80,0.1); color: var(--remedy-risk); }
.state-pending { background: rgba(90,106,122,0.1); color: var(--remedy-text-muted); }

/* ── Cards ─────────────────────────────────────────────────────────── */
.remedy-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
.remedy-card {
  background: var(--remedy-surface); border-radius: var(--remedy-radius);
  padding: 20px; box-shadow: var(--remedy-shadow);
  border: 1px solid var(--remedy-line);
}
.remedy-card-hero {
  grid-column: 1 / -1;
  background: var(--remedy-surface);
  border-left: 4px solid var(--remedy-teal);
}
.remedy-card h3 {
  font-size: 12px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.8px; color: var(--remedy-text-muted); margin-bottom: 8px;
}
.remedy-card .value { font-size: 24px; font-weight: 600; }
.remedy-card .detail { font-size: 13px; color: var(--remedy-text-muted); margin-top: 4px; }

/* ── Lifecycle ─────────────────────────────────────────────────────── */
.remedy-lifecycle {
  display: flex; gap: 4px; flex-wrap: wrap; margin-top: 8px;
}
.lifecycle-step {
  display: flex; align-items: center; gap: 4px;
  padding: 4px 10px; border-radius: 8px; font-size: 12px;
  background: var(--remedy-surface-strong); color: var(--remedy-text-muted);
}
.lifecycle-step.active { background: rgba(10,147,150,0.1); color: var(--remedy-teal); font-weight: 600; }
.lifecycle-arrow { color: var(--remedy-line); font-size: 10px; }

/* ── Next Action ───────────────────────────────────────────────────── */
.remedy-next-action {
  background: var(--remedy-surface); border-radius: var(--remedy-radius);
  padding: 20px; box-shadow: var(--remedy-shadow); border: 1px solid var(--remedy-line);
  margin-bottom: 24px;
}
.remedy-next-action h3 {
  font-size: 12px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.8px; color: var(--remedy-text-muted); margin-bottom: 12px;
}
.action-primary {
  display: flex; align-items: center; gap: 12px;
}
.action-cmd {
  font-family: var(--remedy-mono); font-size: 13px; padding: 8px 16px;
  background: var(--remedy-surface-strong); border-radius: 8px;
  border: 1px solid var(--remedy-line); flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.action-copy {
  padding: 6px 14px; border-radius: 8px; border: 1px solid var(--remedy-teal);
  background: transparent; color: var(--remedy-teal); cursor: pointer;
  font-size: 12px; font-weight: 600; white-space: nowrap;
}
.action-copy:hover { background: rgba(10,147,150,0.08); }
.action-copy:focus-visible { outline: 2px solid var(--remedy-teal); outline-offset: 2px; }

/* ── Explore Brain Button ──────────────────────────────────────────── */
.remedy-explore-btn {
  display: block; width: 100%; padding: 14px; border-radius: var(--remedy-radius);
  border: 2px solid var(--remedy-teal); background: transparent;
  color: var(--remedy-teal); font-size: 15px; font-weight: 600;
  cursor: pointer; text-align: center; margin-bottom: 24px;
  transition: background 0.15s, color 0.15s;
}
.remedy-explore-btn:hover { background: var(--remedy-teal); color: #fff; }
.remedy-explore-btn:focus-visible { outline: 2px solid var(--remedy-teal); outline-offset: 2px; }

/* ── Tabs ──────────────────────────────────────────────────────────── */
.remedy-tabs {
  display: none; border-bottom: 1px solid var(--remedy-line);
  margin-bottom: 16px; gap: 0;
}
.remedy-tabs.visible { display: flex; }
.remedy-tab {
  padding: 8px 16px; border: none; background: none;
  font-size: 13px; font-weight: 500; color: var(--remedy-text-muted);
  cursor: pointer; border-bottom: 2px solid transparent;
}
.remedy-tab:hover { color: var(--remedy-text); }
.remedy-tab.active { color: var(--remedy-teal); border-bottom-color: var(--remedy-teal); }
.remedy-tab:focus-visible { outline: 2px solid var(--remedy-teal); outline-offset: -2px; }

/* ── Brain Explorer ────────────────────────────────────────────────── */
.remedy-brain-explorer { display: none; }
.remedy-brain-explorer.visible { display: block; }

.remedy-graph-container {
  position: relative; background: var(--remedy-surface);
  border-radius: var(--remedy-radius); border: 1px solid var(--remedy-line);
  box-shadow: var(--remedy-shadow); overflow: hidden;
  height: 500px;
}
.remedy-graph-canvas {
  width: 100%; height: 100%;
}
.remedy-graph-status {
  position: absolute; top: 12px; right: 12px; font-size: 11px;
  color: var(--remedy-text-muted); background: var(--remedy-surface);
  padding: 4px 10px; border-radius: 6px; border: 1px solid var(--remedy-line);
}

/* Node rendering */
.graph-node {
  cursor: pointer; transition: opacity 0.15s;
}
.graph-node circle { stroke: var(--remedy-line); stroke-width: 1.5; }
.graph-node.primary circle { r: 8; fill: var(--remedy-teal); }
.graph-node.cluster circle { r: 12; fill: var(--remedy-surface-strong); stroke: var(--remedy-teal); stroke-width: 2; }
.graph-node.secondary { opacity: 0; }
.graph-node.secondary.expanded { opacity: 1; }
.graph-node text {
  font-size: 10px; fill: var(--remedy-text-muted); text-anchor: middle;
  pointer-events: none; display: none;
}
.graph-node.primary text, .graph-node.selected text, .graph-node.cluster text { display: block; }
.graph-edge { stroke: var(--remedy-line); stroke-width: 1; opacity: 0.4; }
.graph-edge.proof-edge { stroke: var(--remedy-proof); stroke-width: 1.5; opacity: 0.6; }
.graph-edge.blocked-edge { stroke: var(--remedy-risk); stroke-dasharray: 4 2; }
.graph-node.selected circle { stroke: var(--remedy-teal); stroke-width: 3; filter: drop-shadow(0 0 6px rgba(10,147,150,0.3)); }

/* Detail panel */
.remedy-detail-panel {
  display: none; background: var(--remedy-surface);
  border-radius: var(--remedy-radius); border: 1px solid var(--remedy-line);
  box-shadow: var(--remedy-shadow); padding: 20px; margin-top: 16px;
}
.remedy-detail-panel.visible { display: block; }
.detail-title { font-size: 16px; font-weight: 600; margin-bottom: 8px; }
.detail-why { font-size: 13px; color: var(--remedy-text-muted); margin-bottom: 12px; }
.detail-section { margin-bottom: 12px; }
.detail-section h4 {
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 0.6px; color: var(--remedy-text-muted); margin-bottom: 4px;
}
.detail-section p { font-size: 13px; }
.detail-advanced { display: none; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--remedy-line); }
.detail-advanced.visible { display: block; }
.detail-advanced-toggle {
  font-size: 11px; color: var(--remedy-text-muted); background: none;
  border: none; cursor: pointer; text-decoration: underline;
}

/* Advanced filters drawer */
.remedy-filters-drawer { display: none; margin-bottom: 16px; }
.remedy-filters-drawer.visible { display: block; }
.filters-toggle {
  font-size: 12px; color: var(--remedy-text-muted); background: none;
  border: 1px solid var(--remedy-line); border-radius: 6px;
  padding: 4px 12px; cursor: pointer; margin-bottom: 8px;
}

/* ── Loading / Error ───────────────────────────────────────────────── */
.remedy-loading { text-align: center; padding: 48px; color: var(--remedy-text-muted); }
.remedy-error { text-align: center; padding: 48px; color: var(--remedy-risk); }

/* ── Reduced Motion ────────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; animation: none !important; }
}

/* ── Narrow Layout ─────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .remedy-cards { grid-template-columns: 1fr; }
  .remedy-app { padding: 16px 12px; }
  .remedy-header { flex-direction: column; align-items: flex-start; gap: 8px; }
}

/* ── Theme toggle ──────────────────────────────────────────────────── */
.theme-toggle {
  background: none; border: 1px solid var(--remedy-line); border-radius: 6px;
  padding: 4px 10px; font-size: 12px; cursor: pointer; color: var(--remedy-text-muted);
}
</style>
</head>
<body>
<div class="remedy-mist"></div>
<div class="remedy-app" id="app">
  <div class="remedy-loading" id="loading">Loading job data...</div>
</div>

<script>
(function() {
  "use strict";
  var JOB_ID = "__JOB_ID__";
  var TOKEN = "__TOKEN__";
  var API = "/api/jobs/" + JOB_ID + "/";

  // ── Helpers ──────────────────────────────────────────────────────────
  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }
  function $(id) { return document.getElementById(id); }

  function fetchJSON(endpoint, cb) {
    var url = API + endpoint + "?token=" + TOKEN;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onload = function() {
      if (xhr.status === 200) { cb(null, JSON.parse(xhr.responseText)); }
      else { cb("HTTP " + xhr.status); }
    };
    xhr.onerror = function() { cb("network error"); };
    xhr.send();
  }

  function copyText(text) {
    if (navigator.clipboard) { navigator.clipboard.writeText(text).catch(function(){}); }
  }

  // ── State mapping ────────────────────────────────────────────────────
  var stateLabels = {
    pending: "Pending", running: "Running", completed: "Verified",
    blocked: "Blocked", failed: "Needs Attention", cancelled: "Cancelled"
  };
  var stateClasses = {
    pending: "state-pending", running: "state-running", completed: "state-completed",
    blocked: "state-blocked", failed: "state-blocked", cancelled: "state-pending"
  };

  // ── Dashboard render ─────────────────────────────────────────────────
  function renderDashboard(d) {
    var state = d.state || "pending";
    var stateLabel = stateLabels[state] || state;
    var stateCls = stateClasses[state] || "state-pending";

    // Lifecycle pills
    var lcHTML = "";
    if (d.lifecycle && d.lifecycle.length) {
      lcHTML = '<div class="remedy-lifecycle">';
      for (var i = 0; i < d.lifecycle.length; i++) {
        if (i > 0) lcHTML += '<span class="lifecycle-arrow">&rarr;</span>';
        lcHTML += '<span class="lifecycle-step active">' + esc(d.lifecycle[i].step) +
          ' <small>(' + d.lifecycle[i].count + ')</small></span>';
      }
      lcHTML += '</div>';
    }

    // Proven
    var provenHTML = '<span class="value">0</span><div class="detail">No proofs yet</div>';
    if (d.proof_count > 0) {
      provenHTML = '<span class="value">' + d.proof_count + ' proof' + (d.proof_count > 1 ? 's' : '') + '</span>';
      if (d.latest_proof) provenHTML += '<div class="detail">Latest: ' + esc(d.latest_proof.hash) + '</div>';
      if (d.test_count > 0) provenHTML += '<div class="detail">' + d.test_count + ' test run' + (d.test_count > 1 ? 's' : '') + '</div>';
    }

    // Attention
    var attnCount = (d.pending_approvals || 0) + (d.blocker_count || 0) + (d.decision_count || 0);
    var attnHTML = '<span class="value">' + attnCount + '</span>';
    if (attnCount > 0) {
      var parts = [];
      if (d.pending_approvals) parts.push(d.pending_approvals + " approval" + (d.pending_approvals > 1 ? "s" : ""));
      if (d.blocker_count) parts.push(d.blocker_count + " blocker" + (d.blocker_count > 1 ? "s" : ""));
      if (d.decision_count) parts.push(d.decision_count + " decision" + (d.decision_count > 1 ? "s" : ""));
      attnHTML += '<div class="detail">' + esc(parts.join(", ")) + '</div>';
    } else {
      attnHTML += '<div class="detail">Nothing needs you right now</div>';
    }

    // Next action
    var nextHTML = '';
    if (d.next_action) {
      nextHTML = '<div class="remedy-next-action" id="next-action"><h3>Next safe action</h3>' +
        '<div class="action-primary"><span class="action-cmd" id="next-cmd">' + esc(d.next_action) + '</span>' +
        '<button class="action-copy" onclick="copyCmd()">Copy</button></div></div>';
    }

    // Token cost
    var tokenHTML = '<span class="value">' + esc(d.token_mode || "compact") + '</span>' +
      '<div class="detail">Context mode</div>';

    var html = '<header class="remedy-header">' +
      '<div><span class="remedy-logo">Remedy</span> ' +
      '<span class="remedy-job-id">' + esc(JOB_ID.slice(0, 8)) + '</span></div>' +
      '<div><span class="remedy-state-badge ' + stateCls + '">' + esc(stateLabel) + '</span>' +
      ' <button class="theme-toggle" onclick="toggleTheme()">&#9789;</button></div>' +
      '</header>';

    // Hero card
    html += '<div class="remedy-cards">' +
      '<div class="remedy-card remedy-card-hero" id="what-happened"><h3>What happened</h3>' +
      '<span class="value">' + (d.task_count || 0) + ' task' + ((d.task_count||0) !== 1 ? 's' : '') +
      ', ' + (d.apply_count || 0) + ' applied</span>' + lcHTML + '</div>';

    // Compact cards
    html += '<div class="remedy-card" id="proven"><h3>What is proven</h3>' + provenHTML + '</div>';
    html += '<div class="remedy-card" id="needs-attention"><h3>Needs your attention</h3>' + attnHTML + '</div>';
    html += '<div class="remedy-card" id="token-cost"><h3>Token cost</h3>' + tokenHTML + '</div>';

    // Guidance card
    if (d.guidance && d.guidance.length) {
      html += '<div class="remedy-card" id="guidance-summary"><h3>Guidance</h3>' +
        '<span class="value">' + d.guidance.length + ' suggestion' + (d.guidance.length > 1 ? 's' : '') + '</span>' +
        '<div class="detail">' + esc(d.guidance[0].title) + '</div></div>';
    }

    html += '</div>'; // close cards

    // Next action
    html += nextHTML;

    // Explore Brain button
    html += '<button class="remedy-explore-btn" id="explore-brain" onclick="exploreBrain()">Explore project brain</button>';

    // Tab bar (hidden until explore)
    html += '<div class="remedy-tabs" id="brain-tabs">' +
      '<button class="remedy-tab active" data-mode="proof-path" onclick="setMode(\'proof-path\')">Proof Path</button>' +
      '<button class="remedy-tab" data-mode="attention" onclick="setMode(\'attention\')">Attention</button>' +
      '<button class="remedy-tab" data-mode="system-map" onclick="setMode(\'system-map\')">System Map</button>' +
      '<button class="remedy-tab" data-mode="full-graph" onclick="setMode(\'full-graph\')">Full Graph</button>' +
      '</div>';

    // Filters drawer
    html += '<div class="remedy-filters-drawer" id="filters-drawer">' +
      '<button class="filters-toggle" onclick="toggleFilters()">Advanced filters</button>' +
      '</div>';

    // Brain explorer region
    html += '<div class="remedy-brain-explorer" id="brain-explorer">' +
      '<div class="remedy-graph-container"><svg class="remedy-graph-canvas" id="graph-svg"></svg>' +
      '<div class="remedy-graph-status" id="graph-status">Loading...</div></div></div>';

    // Detail panel
    html += '<div class="remedy-detail-panel" id="detail-panel">' +
      '<div class="detail-title" id="detail-title"></div>' +
      '<div class="detail-why" id="detail-why"></div>' +
      '<div class="detail-section" id="detail-evidence"><h4>Evidence</h4><p id="detail-evidence-text"></p></div>' +
      '<div class="detail-section" id="detail-actions"><h4>Related commands</h4><p id="detail-actions-text"></p></div>' +
      '<button class="detail-advanced-toggle" onclick="toggleAdvanced()">Show advanced metadata</button>' +
      '<div class="detail-advanced" id="detail-advanced"><pre id="detail-meta"></pre></div></div>';

    return html;
  }

  // ── Theme toggle ─────────────────────────────────────────────────────
  window.toggleTheme = function() {
    var el = document.documentElement;
    el.classList.toggle("remedy-dark");
    el.classList.toggle("remedy-light");
  };

  // ── Copy command ─────────────────────────────────────────────────────
  window.copyCmd = function() {
    var el = $("next-cmd");
    if (el) copyText(el.textContent);
  };

  // ── Brain Explorer ───────────────────────────────────────────────────
  var brainData = null;
  var currentMode = "proof-path";
  var selectedNode = null;

  window.exploreBrain = function() {
    $("brain-tabs").classList.add("visible");
    $("brain-explorer").classList.add("visible");
    if (!brainData) {
      $("graph-status").textContent = "Loading brain...";
      fetchJSON("brain", function(err, data) {
        if (err) { $("graph-status").textContent = "Failed to load brain"; return; }
        brainData = data;
        renderGraph();
      });
    }
  };

  // ── Graph mode tabs ──────────────────────────────────────────────────
  window.setMode = function(mode) {
    currentMode = mode;
    var tabs = document.querySelectorAll(".remedy-tab");
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].classList.toggle("active", tabs[i].getAttribute("data-mode") === mode);
    }
    if (brainData) renderGraph();
  };

  window.toggleAdvanced = function() {
    var el = $("detail-advanced");
    if (el) el.classList.toggle("visible");
  };

  window.toggleFilters = function() {
    var el = $("filters-drawer");
    if (el) el.classList.toggle("visible");
  };

  // ── Graph Renderer ───────────────────────────────────────────────────
  var PROOF_CHAIN_TYPES = ["job","task","patch_intent","approval","patch_apply","proof","test_run","decision","memory"];
  var ATTENTION_TYPES = ["stop_reason","permission_blocker","decision","test_run","git_status","context_budget","blocker"];
  var MAX_PRIMARY = 16;

  function classifyNodes(nodes) {
    var result = [];
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      var isPrimary = false;
      if (currentMode === "proof-path") {
        isPrimary = PROOF_CHAIN_TYPES.indexOf(n.type) >= 0;
      } else if (currentMode === "attention") {
        isPrimary = ATTENTION_TYPES.indexOf(n.type) >= 0 || n.type === "job";
      } else if (currentMode === "system-map") {
        isPrimary = true; // all visible but clustered
      } else {
        isPrimary = true; // full-graph
      }
      result.push({ node: n, primary: isPrimary });
    }
    return result;
  }

  function clusterNodes(classified) {
    // Cluster non-primary nodes by type; expand clusters if toggled
    var primary = [], clusters = {};
    for (var i = 0; i < classified.length; i++) {
      var n = classified[i].node;
      if (classified[i].primary || expandedClusters[n.type]) {
        primary.push(n);
      } else {
        var t = n.type;
        if (!clusters[t]) clusters[t] = [];
        clusters[t].push(n);
      }
    }
    // Cap primary nodes (only in non-full modes without explicit expansion)
    if (currentMode !== "full-graph" && primary.length > MAX_PRIMARY) {
      var overflow = primary.splice(MAX_PRIMARY);
      for (var j = 0; j < overflow.length; j++) {
        var ot = overflow[j].type;
        if (!expandedClusters[ot]) {
          if (!clusters[ot]) clusters[ot] = [];
          clusters[ot].push(overflow[j]);
        }
      }
    }
    return { primary: primary, clusters: clusters };
  }

  function renderGraph() {
    if (!brainData || !brainData.graph) return;
    var svg = $("graph-svg");
    var rect = svg.getBoundingClientRect();
    var W = rect.width || 900, H = rect.height || 500;
    var cx = W / 2, cy = H / 2;

    var nodes = brainData.graph.nodes || [];
    var edges = brainData.graph.edges || [];

    var classified = classifyNodes(nodes);
    var grouped = clusterNodes(classified);

    // Position primary nodes in a circle
    var positions = {};
    var primary = grouped.primary;
    for (var i = 0; i < primary.length; i++) {
      var angle = (2 * Math.PI * i) / Math.max(primary.length, 1) - Math.PI / 2;
      var r = Math.min(W, H) * 0.35;
      positions[primary[i].id] = {
        x: cx + r * Math.cos(angle),
        y: cy + r * Math.sin(angle)
      };
    }

    // Position clusters around edge
    var clusterKeys = Object.keys(grouped.clusters);
    var clusterPositions = {};
    for (var ci = 0; ci < clusterKeys.length; ci++) {
      var ca = (2 * Math.PI * ci) / Math.max(clusterKeys.length, 1);
      var cr = Math.min(W, H) * 0.42;
      clusterPositions[clusterKeys[ci]] = {
        x: cx + cr * Math.cos(ca),
        y: cy + cr * Math.sin(ca),
        count: grouped.clusters[clusterKeys[ci]].length
      };
    }

    // Build SVG
    var svgHTML = '';

    // Edges
    for (var ei = 0; ei < edges.length; ei++) {
      var e = edges[ei];
      var p1 = positions[e.source], p2 = positions[e.target];
      if (p1 && p2) {
        var ecls = "graph-edge";
        if (e.type === "proved_by" || e.type === "tested_by") ecls += " proof-edge";
        if (e.type === "blocked_by") ecls += " blocked-edge";
        svgHTML += '<line class="' + ecls + '" x1="' + p1.x + '" y1="' + p1.y +
          '" x2="' + p2.x + '" y2="' + p2.y + '"/>';
      }
    }

    // Primary nodes
    for (var ni = 0; ni < primary.length; ni++) {
      var n = primary[ni];
      var p = positions[n.id];
      var label = (n.label || n.type || "").substring(0, 20);
      svgHTML += '<g class="graph-node primary" data-id="' + esc(n.id) + '" onclick="selectNode(\'' + esc(n.id) + '\')">' +
        '<circle cx="' + p.x + '" cy="' + p.y + '" r="8" fill="' +
        (n.type === "job" ? "var(--remedy-teal)" : "var(--remedy-cyan)") + '"/>' +
        '<text x="' + p.x + '" y="' + (p.y - 14) + '">' + esc(label) + '</text></g>';
    }

    // Cluster nodes
    for (var ki = 0; ki < clusterKeys.length; ki++) {
      var k = clusterKeys[ki];
      var cp = clusterPositions[k];
      svgHTML += '<g class="graph-node cluster" data-type="' + esc(k) + '" onclick="expandCluster(\'' + esc(k) + '\')">' +
        '<circle cx="' + cp.x + '" cy="' + cp.y + '" r="12" fill="var(--remedy-surface-strong)" stroke="var(--remedy-teal)"/>' +
        '<text x="' + cp.x + '" y="' + (cp.y + 4) + '" style="display:block;font-size:10px;text-anchor:middle">' +
        cp.count + '</text>' +
        '<text x="' + cp.x + '" y="' + (cp.y - 18) + '" style="display:block">' + esc(k) + '</text></g>';
    }

    svg.innerHTML = svgHTML;
    var statusText = currentMode + " \u00b7 " + primary.length + " nodes";
    if (clusterKeys.length) statusText += " \u00b7 " + clusterKeys.length + " clusters";
    $("graph-status").textContent = statusText;
  }

  // ── Node selection ───────────────────────────────────────────────────
  window.selectNode = function(nodeId) {
    selectedNode = nodeId;
    var panel = $("detail-panel");
    panel.classList.add("visible");

    // Find node
    var node = null;
    var nodes = (brainData && brainData.graph && brainData.graph.nodes) || [];
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].id === nodeId) { node = nodes[i]; break; }
    }
    if (!node) { panel.classList.remove("visible"); return; }

    var detail = (brainData.details && brainData.details[nodeId]) || {};
    $("detail-title").textContent = detail.title || node.label || node.type;
    $("detail-why").textContent = detail.why || "Part of the project brain graph.";
    $("detail-evidence-text").textContent = detail.evidence || "See node metadata.";
    $("detail-actions-text").textContent = detail.commands || "remedy brain node " + JOB_ID.slice(0, 8) + " " + nodeId;

    // Advanced metadata (hidden by default)
    $("detail-advanced").classList.remove("visible");
    var meta = node.metadata || {};
    $("detail-meta").textContent = JSON.stringify(meta, null, 2);

    // Highlight in SVG
    var allNodes = document.querySelectorAll(".graph-node");
    for (var j = 0; j < allNodes.length; j++) {
      allNodes[j].classList.remove("selected");
      if (allNodes[j].getAttribute("data-id") === nodeId) {
        allNodes[j].classList.add("selected");
      }
    }
  };

  var expandedClusters = {};
  window.expandCluster = function(nodeType) {
    expandedClusters[nodeType] = !expandedClusters[nodeType];
    if (brainData) renderGraph();
  };

  // ── Init ─────────────────────────────────────────────────────────────
  fetchJSON("dashboard", function(err, data) {
    if (err) {
      $("app").innerHTML = '<div class="remedy-error">Failed to load job data (' + esc(err) + ')</div>';
      return;
    }
    $("app").innerHTML = renderDashboard(data);
  });

})();
</script>
</body>
</html>"""
