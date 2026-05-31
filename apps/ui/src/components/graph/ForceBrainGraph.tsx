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

function renderBrainNode(node: object, ctx: CanvasRenderingContext2D, globalScale: number) {
  const n = node as ForceBrainNode;
  const x = n.x ?? 0;
  const y = n.y ?? 0;
  ctx.save();
  ctx.globalAlpha = n.alpha;

  if (n.kind === "root") {
    // Large glowing blue orb
    const grad = ctx.createRadialGradient(x, y, 0, x, y, 22);
    grad.addColorStop(0, "#ffffff");
    grad.addColorStop(0.3, "#6da0ff");
    grad.addColorStop(1, "#3478ff");
    ctx.shadowBlur = 44;
    ctx.shadowColor = "#4c83ff";
    ctx.beginPath();
    ctx.arc(x, y, 18, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();
    // Code icon — two chevrons
    ctx.shadowBlur = 0;
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(x - 6, y - 5); ctx.lineTo(x - 10, y); ctx.lineTo(x - 6, y + 5);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x + 6, y - 5); ctx.lineTo(x + 10, y); ctx.lineTo(x + 6, y + 5);
    ctx.stroke();
  } else if (n.kind === "cluster") {
    // Glowing ring
    ctx.shadowBlur = 28;
    ctx.shadowColor = n.color;
    ctx.beginPath();
    ctx.arc(x, y, 10, 0, Math.PI * 2);
    ctx.strokeStyle = n.color;
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.shadowBlur = 0;
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fillStyle = n.color;
    ctx.fill();
  } else if (n.kind === "particle") {
    // Tiny dot
    const r = 1.2 + n.value * 0.3;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = n.color;
    ctx.fill();
  } else {
    // Semantic node — white core + colored stroke + glow
    const r = 4 + n.value * 0.5;
    ctx.shadowBlur = 16;
    ctx.shadowColor = n.color;
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
    ctx.strokeStyle = n.color;
    ctx.lineWidth = 1.5;
    ctx.stroke();
  }

  // Label only for root or selected semantic nodes at reasonable zoom
  if (n.visibleLabel && n.label && globalScale > 1.2) {
    ctx.shadowBlur = 0;
    ctx.globalAlpha = 0.9;
    ctx.font = `${Math.max(10, 11 / globalScale)}px Inter, system-ui, sans-serif`;
    ctx.fillStyle = "#1a3a6e";
    ctx.textAlign = "center";
    ctx.fillText(n.label, x, y + (n.kind === "root" ? 28 : 14));
  }

  ctx.restore();
}

function renderBrainLink(link: object, ctx: CanvasRenderingContext2D, _globalScale: number) {
  const l = link as ForceBrainLink;
  const source = l.source as ForceBrainNode;
  const target = l.target as ForceBrainNode;
  if (!source?.x || !target?.x) return;
  const sx = source.x, sy = source.y ?? 0;
  const tx = target.x, ty = target.y ?? 0;

  ctx.save();
  ctx.globalAlpha = l.alpha;
  ctx.strokeStyle = source.color || "#91b8ff";
  ctx.lineWidth = l.width;
  ctx.shadowBlur = 6;
  ctx.shadowColor = source.color || "#4c83ff";

  // Quadratic bezier curve
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
          linkCanvasObject={renderBrainLink}
          linkCanvasObjectMode={() => "replace"}
          onEngineStop={() => { /* simulation settled */ }}
        />
      )}
    </div>
  );
}
