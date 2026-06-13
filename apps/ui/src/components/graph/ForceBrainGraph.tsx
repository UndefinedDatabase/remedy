import { useCallback, useEffect, useMemo, useRef } from "react";
import ForceGraph2D from "react-force-graph-2d";
import type { ForceGraph2DInstance } from "react-force-graph-2d";
import type { RemedyDashboard } from "../../api/types";
import { buildForceBrainModel } from "./buildForceBrainModel";
import type { ForceBrainLink, ForceBrainNode } from "./forceBrainTypes";
import { useGraphSize } from "./useGraphSize";
import styles from "./ForceBrainGraph.module.css";

const reducedMotion = typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function sizeClass(w: number): "small" | "medium" | "large" {
  if (w < 900) return "small";
  if (w < 1400) return "medium";
  return "large";
}

// Status palette — mirrors tokens.css status palette (single source of truth).
// Keys are the real BrainNodeState values: planned == reference "pending",
// suggested == reference "open".
const STATE_FILL: Record<string, string> = {
  done: "#34c27e",
  current: "#4c83ff",
  planned: "#ffffff",
  suggested: "#a78bfa",
  blocked: "#ef6363",
  idle: "#ffffff",
};
const STATE_RING: Record<string, string> = {
  done: "rgba(52,194,126,.35)",
  current: "rgba(76,131,255,.4)",
  planned: "#9db9ee",
  suggested: "rgba(167,139,250,.4)",
  blocked: "rgba(239,99,99,.4)",
  idle: "#9db9ee",
};

function renderBrainNode(node: object, ctx: CanvasRenderingContext2D, globalScale: number) {
  const n = node as ForceBrainNode;
  const x = n.x ?? 0;
  const y = n.y ?? 0;

  if (n.kind === "root") {
    // Glow halo
    const halo = ctx.createRadialGradient(x, y, 6, x, y, 64);
    halo.addColorStop(0, "rgba(76,131,255,0.55)");
    halo.addColorStop(0.5, "rgba(76,131,255,0.18)");
    halo.addColorStop(1, "rgba(76,131,255,0)");
    ctx.fillStyle = halo;
    ctx.beginPath(); ctx.arc(x, y, 64, 0, Math.PI * 2); ctx.fill();
    // Core sphere with gradient
    const core = ctx.createRadialGradient(x - 6, y - 8, 4, x, y, 26);
    core.addColorStop(0, "#7ea6ff");
    core.addColorStop(1, "#2f6fff");
    ctx.fillStyle = core;
    ctx.beginPath(); ctx.arc(x, y, 26, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "rgba(255,255,255,0.85)"; ctx.lineWidth = 2; ctx.stroke();
    // </> glyph
    ctx.fillStyle = "#ffffff";
    ctx.font = `600 ${15}px ui-monospace, Menlo, monospace`;
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("</>", x, y + 1);
    return;
  }

  if (n.sourceKind === "layout_only") {
    // Decorative dots: tiny, pale, NEVER interactive, NEVER counted.
    ctx.fillStyle = "rgba(170, 196, 238, 0.55)";
    ctx.beginPath(); ctx.arc(x, y, 1.8, 0, Math.PI * 2); ctx.fill();
    return;
  }

  // Real entities (Task/Intent/Apply/Test/Proof/Finding)
  ctx.save();
  ctx.globalAlpha = n.alpha;
  const r = n.value >= 8 ? 7 : 5.5;
  const fill = STATE_FILL[n.state] ?? "#ffffff";
  const ring = STATE_RING[n.state] ?? "#9db9ee";
  // soft outer ring
  ctx.fillStyle = ring;
  ctx.beginPath(); ctx.arc(x, y, r + 2.5, 0, Math.PI * 2); ctx.fill();
  // glossy sphere
  const g = ctx.createRadialGradient(x - r * 0.4, y - r * 0.5, r * 0.2, x, y, r);
  g.addColorStop(0, "rgba(255,255,255,0.9)");
  g.addColorStop(0.35, fill);
  g.addColorStop(1, fill);
  ctx.fillStyle = g;
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
  if (n.state === "planned") { ctx.strokeStyle = "#9db9ee"; ctx.lineWidth = 1.2; ctx.stroke(); }

  if (n.visibleLabel && n.label && globalScale > 1.4) {
    ctx.fillStyle = "#3a4f7e";
    ctx.font = `500 ${11 / globalScale}px -apple-system, sans-serif`;
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    ctx.fillText(n.label, x, y + r + 4);
  }
  ctx.restore();
}

// Pointer hit-area: only real entities are hoverable/clickable; decorative
// layout_only dots paint no hit area, so they can never be selected or counted.
function pointerAreaPaint(node: object, color: string, ctx: CanvasRenderingContext2D) {
  const n = node as ForceBrainNode;
  if (n.sourceKind === "layout_only") return;
  const x = n.x ?? 0;
  const y = n.y ?? 0;
  const r = n.kind === "root" ? 26 : 8;
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
}

function renderBrainLink(link: object, ctx: CanvasRenderingContext2D, _globalScale: number) {
  const l = link as ForceBrainLink;
  const source = l.source as ForceBrainNode;
  const target = l.target as ForceBrainNode;
  if (!source?.x || !target?.x) return;
  const sx = source.x, sy = source.y ?? 0;
  const tx = target.x, ty = target.y ?? 0;

  const isReal = target.sourceKind === "real_brain" || source.sourceKind === "real_brain";

  ctx.save();
  ctx.globalAlpha = l.alpha;
  ctx.strokeStyle = "rgba(190, 212, 248, 0.8)";
  ctx.lineWidth = isReal ? 1.6 : 0.9;

  // Quadratic bezier curve (no glow, no directional particles → no flicker)
  const mx = (sx + tx) / 2;
  const my = (sy + ty) / 2;
  const dx = tx - sx;
  const dy = ty - sy;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  const cx = mx + (-dy / len) * l.curvature * 80;
  const cy = my + (dx / len) * l.curvature * 80;

  ctx.beginPath();
  ctx.moveTo(sx, sy);
  ctx.quadraticCurveTo(cx, cy, tx, ty);
  ctx.stroke();
  ctx.restore();
}

export function ForceBrainGraph({ dashboard, filter, onSelectNode }: {
  dashboard: RemedyDashboard;
  filter: "all" | "open" | "planned" | "done";
  onSelectNode: (nodeId: string | null) => void;
}) {
  const { containerRef, size } = useGraphSize();
  const graphRef = useRef<ForceGraph2DInstance>(null);

  const graphData = useMemo(
    () => buildForceBrainModel(dashboard, sizeClass(size.width), filter),
    [dashboard, size.width, filter],
  );

  const handleNodeClick = useCallback((node: object) => {
    const n = node as ForceBrainNode;
    if (n.clickable && n.nodeId) onSelectNode(n.nodeId);
  }, [onSelectNode]);

  // Configure forces after mount
  useEffect(() => {
    const fg = graphRef.current;
    if (!fg) return;
    try {
      fg.d3Force("charge", { strength: () => -30 } as object);
      fg.d3Force("link", { distance: (l: object) => {
        const link = l as ForceBrainLink;
        return link.width > 1 ? 120 : 50;
      }} as object);
    } catch { /* force config may not be available immediately */ }
  }, [graphData]);

  // Initial zoom fit
  useEffect(() => {
    const fg = graphRef.current;
    if (!fg) return;
    const timer = setTimeout(() => {
      fg.zoom(1.0, reducedMotion ? 0 : 600);
      fg.centerAt(0, 0, reducedMotion ? 0 : 600);
    }, reducedMotion ? 100 : 800);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div ref={containerRef} className={styles.container} data-ui="force-brain-graph">
      {size.width > 0 && (
        <ForceGraph2D
          ref={graphRef}
          graphData={graphData}
          width={size.width}
          height={size.height}
          backgroundColor="rgba(0,0,0,0)"
          nodeId="id"
          nodeRelSize={1}
          cooldownTicks={reducedMotion ? 20 : 80}
          d3AlphaDecay={0.045}
          d3VelocityDecay={0.28}
          enableNodeDrag
          enableZoomInteraction
          enablePanInteraction
          minZoom={0.3}
          maxZoom={4}
          onNodeClick={handleNodeClick}
          onBackgroundClick={() => onSelectNode(null)}
          nodeCanvasObject={renderBrainNode}
          nodeCanvasObjectMode={() => "replace"}
          nodePointerAreaPaint={pointerAreaPaint}
          linkCanvasObject={renderBrainLink}
          linkCanvasObjectMode={() => "replace"}
          linkDirectionalParticles={0}
          onEngineStop={() => { /* simulation settled */ }}
        />
      )}
    </div>
  );
}
