"""
Remedy Visual System v1 — design tokens, CSS, status mapping.

Inspired by ice/teal forensic visual direction. No external assets,
no CDN, no fonts, no trademarked content. System fonts only.

Public API::

    DESIGN_TOKENS: dict[str, str]
    STATUS_CLASSES: dict[str, str]
    REMEDY_CSS: str
    get_status_class(status, node_type) -> str
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Design tokens — CSS custom properties
# ---------------------------------------------------------------------------

DESIGN_TOKENS: dict[str, str] = {
    "--remedy-bg": "#0a0e14",
    "--remedy-bg-panel": "rgba(14, 20, 30, 0.85)",
    "--remedy-fg": "#d0dae8",
    "--remedy-fg-muted": "#6b7d93",
    "--remedy-teal": "#38c8c8",
    "--remedy-cyan": "#5ce0d8",
    "--remedy-panel": "rgba(20, 30, 45, 0.75)",
    "--remedy-panel-border": "rgba(56, 200, 200, 0.15)",
    "--remedy-muted": "#3a4a5a",
    "--remedy-risk": "#e05252",
    "--remedy-warning": "#e8a838",
    "--remedy-proof": "#38c878",
    "--remedy-memory": "#7878d8",
    "--remedy-glow": "rgba(56, 200, 200, 0.12)",
    "--remedy-line": "rgba(56, 200, 200, 0.25)",
    "--remedy-node-border": "rgba(56, 200, 200, 0.3)",
    "--remedy-font": "ui-monospace, 'SF Mono', 'Cascadia Code', 'Consolas', monospace",
    "--remedy-font-sans": "system-ui, -apple-system, 'Segoe UI', sans-serif",
}

# ---------------------------------------------------------------------------
# Status classes — maps status/type to CSS class
# ---------------------------------------------------------------------------

STATUS_CLASSES: dict[str, str] = {
    "verified": "remedy-status-verified",
    "completed": "remedy-status-verified",
    "passed": "remedy-status-verified",
    "loaded": "remedy-status-verified",
    "approved": "remedy-status-verified",
    "ok": "remedy-status-verified",
    "idle": "remedy-status-verified",
    "needs_decision": "remedy-status-decision",
    "needs_approval": "remedy-status-decision",
    "pending": "remedy-status-decision",
    "open": "remedy-status-decision",
    "active": "remedy-status-decision",
    "blocked": "remedy-status-risk",
    "failed": "remedy-status-risk",
    "rejected": "remedy-status-risk",
    "running": "remedy-status-running",
    "memory": "remedy-status-memory",
    "future": "remedy-status-future",
    "inert": "remedy-status-future",
    "linked": "remedy-status-future",
    "informational": "remedy-status-muted",
}

# Node type to layer class
LAYER_CLASSES: dict[str, str] = {
    "job": "remedy-layer-core",
    "task": "remedy-layer-core",
    "artifact": "remedy-layer-core",
    "patch_intent": "remedy-layer-patch",
    "approval_decision": "remedy-layer-patch",
    "patch_apply": "remedy-layer-patch",
    "patch_apply_proof": "remedy-layer-proof",
    "test_run": "remedy-layer-proof",
    "verification": "remedy-layer-proof",
    "run_event": "remedy-layer-event",
    "agent_loop": "remedy-layer-event",
    "event_ledger": "remedy-layer-event",
    "stop_reason": "remedy-layer-risk",
    "permission_blocker": "remedy-layer-risk",
    "decision_queue": "remedy-layer-risk",
    "memory_placeholder": "remedy-layer-memory",
    "memory": "remedy-layer-memory",
    "constitution": "remedy-layer-policy",
    "run_contract": "remedy-layer-policy",
    "token_policy": "remedy-layer-policy",
    "context_coverage": "remedy-layer-context",
    "context_pack": "remedy-layer-context",
    "context_budget": "remedy-layer-context",
    "autonomy_readiness": "remedy-layer-readiness",
    "worker_adapter": "remedy-layer-worker",
    "git_status": "remedy-layer-repo",
    "change_set": "remedy-layer-repo",
    "patch_revert": "remedy-layer-repo",
    "project_placeholder": "remedy-layer-meta",
    "mcp_placeholder": "remedy-layer-future",
}


def get_status_class(status: str, node_type: str = "") -> str:
    """Return the CSS class for a node status."""
    if node_type in ("memory_placeholder", "memory"):
        return "remedy-status-memory"
    if node_type in ("mcp_placeholder",):
        return "remedy-status-future"
    return STATUS_CLASSES.get(status, "remedy-status-muted")


def get_layer_class(node_type: str) -> str:
    """Return the CSS class for a node's layer."""
    return LAYER_CLASSES.get(node_type, "remedy-layer-meta")


# ---------------------------------------------------------------------------
# Core CSS — all classes required by Steps 72-74
# ---------------------------------------------------------------------------

REMEDY_CSS = """\
:root {
  --remedy-bg: #0a0e14;
  --remedy-bg-panel: rgba(14, 20, 30, 0.85);
  --remedy-fg: #d0dae8;
  --remedy-fg-muted: #6b7d93;
  --remedy-teal: #38c8c8;
  --remedy-cyan: #5ce0d8;
  --remedy-panel: rgba(20, 30, 45, 0.75);
  --remedy-panel-border: rgba(56, 200, 200, 0.15);
  --remedy-muted: #3a4a5a;
  --remedy-risk: #e05252;
  --remedy-warning: #e8a838;
  --remedy-proof: #38c878;
  --remedy-memory: #7878d8;
  --remedy-glow: rgba(56, 200, 200, 0.12);
  --remedy-line: rgba(56, 200, 200, 0.25);
  --remedy-node-border: rgba(56, 200, 200, 0.3);
  --remedy-font: ui-monospace, 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  --remedy-font-sans: system-ui, -apple-system, 'Segoe UI', sans-serif;
}

/* ── Shell ─────────────────────────────────────────── */
.remedy-shell {
  background: var(--remedy-bg);
  color: var(--remedy-fg);
  font-family: var(--remedy-font);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* ── Background layers ─────────────────────────────── */
.remedy-orbit-bg {
  position: fixed;
  inset: 0;
  background: radial-gradient(ellipse at 30% 20%, rgba(56, 200, 200, 0.04) 0%, transparent 60%),
              radial-gradient(ellipse at 70% 80%, rgba(120, 120, 216, 0.03) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.remedy-particle-field {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image:
    radial-gradient(1px 1px at 10% 20%, rgba(56, 200, 200, 0.3), transparent),
    radial-gradient(1px 1px at 30% 60%, rgba(92, 224, 216, 0.2), transparent),
    radial-gradient(1px 1px at 50% 10%, rgba(56, 200, 200, 0.25), transparent),
    radial-gradient(1px 1px at 70% 40%, rgba(120, 120, 216, 0.2), transparent),
    radial-gradient(1px 1px at 90% 70%, rgba(56, 200, 200, 0.15), transparent),
    radial-gradient(1px 1px at 20% 90%, rgba(92, 224, 216, 0.2), transparent),
    radial-gradient(1px 1px at 60% 85%, rgba(56, 200, 200, 0.2), transparent),
    radial-gradient(1px 1px at 85% 15%, rgba(120, 120, 216, 0.15), transparent);
}

@keyframes remedy-particle-drift {
  0% { transform: translateY(0); }
  100% { transform: translateY(-20px); }
}
.remedy-particle-field {
  animation: remedy-particle-drift 30s linear infinite alternate;
}

/* ── Glass panels ──────────────────────────────────── */
.remedy-glass-panel {
  background: var(--remedy-panel);
  border: 1px solid var(--remedy-panel-border);
  border-radius: 8px;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  padding: 12px 16px;
  position: relative;
  z-index: 1;
}

.remedy-glass-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 8px;
  box-shadow: 0 0 20px var(--remedy-glow);
  pointer-events: none;
}

/* ── Proof chain ───────────────────────────────────── */
.remedy-proof-chain {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  font-size: 11px;
  overflow-x: auto;
}
.remedy-proof-chain .chain-step {
  padding: 4px 10px;
  border-radius: 4px;
  background: rgba(56, 200, 136, 0.1);
  border: 1px solid rgba(56, 200, 136, 0.2);
  color: var(--remedy-proof);
  white-space: nowrap;
}
.remedy-proof-chain .chain-arrow {
  color: var(--remedy-fg-muted);
  font-size: 10px;
}

/* ── Node cards ────────────────────────────────────── */
.remedy-node-card {
  background: var(--remedy-bg-panel);
  border: 1px solid var(--remedy-panel-border);
  border-radius: 6px;
  padding: 10px 14px;
  margin: 4px 0;
  font-size: 12px;
  transition: border-color 0.2s;
}
.remedy-node-card:hover {
  border-color: var(--remedy-teal);
}

.remedy-node-status {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}

/* ── Status colors ─────────────────────────────────── */
.remedy-status-verified { color: var(--remedy-teal); }
.remedy-status-verified .remedy-node-status { background: var(--remedy-teal); box-shadow: 0 0 6px var(--remedy-teal); }
.remedy-status-decision { color: var(--remedy-warning); }
.remedy-status-decision .remedy-node-status { background: var(--remedy-warning); box-shadow: 0 0 6px var(--remedy-warning); }
.remedy-status-risk { color: var(--remedy-risk); }
.remedy-status-risk .remedy-node-status { background: var(--remedy-risk); box-shadow: 0 0 6px var(--remedy-risk); }
.remedy-status-running { color: var(--remedy-cyan); }
.remedy-status-running .remedy-node-status { background: var(--remedy-cyan); animation: remedy-pulse 1.5s ease-in-out infinite; }
.remedy-status-memory { color: var(--remedy-memory); }
.remedy-status-memory .remedy-node-status { background: var(--remedy-memory); }
.remedy-status-future { color: var(--remedy-muted); }
.remedy-status-future .remedy-node-status { background: var(--remedy-muted); }
.remedy-status-muted { color: var(--remedy-fg-muted); }
.remedy-status-muted .remedy-node-status { background: var(--remedy-fg-muted); }

@keyframes remedy-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* ── Timeline ──────────────────────────────────────── */
.remedy-timeline {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 12px;
  overflow-x: auto;
  font-size: 10px;
}
.remedy-timeline .tl-event {
  padding: 3px 8px;
  border-radius: 3px;
  background: rgba(56, 200, 200, 0.06);
  border: 1px solid rgba(56, 200, 200, 0.12);
  color: var(--remedy-fg-muted);
  white-space: nowrap;
}
.remedy-timeline .tl-dot {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--remedy-muted);
}

/* ── Decision panel ────────────────────────────────── */
.remedy-decision-panel {
  border-left: 2px solid var(--remedy-warning);
  padding-left: 12px;
  margin: 8px 0;
}
.remedy-decision-panel .decision-count {
  font-size: 20px;
  font-weight: bold;
  color: var(--remedy-warning);
}

/* ── Readiness panel ───────────────────────────────── */
.remedy-readiness-panel {
  border-left: 2px solid var(--remedy-teal);
  padding-left: 12px;
  margin: 8px 0;
}
.remedy-readiness-panel .readiness-level {
  font-size: 20px;
  font-weight: bold;
  color: var(--remedy-teal);
}

/* ── Accessibility ─────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .remedy-particle-field {
    animation: none !important;
  }
  .remedy-status-running .remedy-node-status {
    animation: none !important;
  }
  @keyframes remedy-pulse {
    0%, 100% { opacity: 1; }
  }
}

/* ── Focus ─────────────────────────────────────────── */
.remedy-node-card:focus-visible,
[tabindex]:focus-visible {
  outline: 2px solid var(--remedy-teal);
  outline-offset: 2px;
}
"""
