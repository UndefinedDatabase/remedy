import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import type { ForceGraph2DInstance } from "react-force-graph-2d";
import { seededRng } from "./buildForceBrainModel";
import { carryBrainPositions, selectionTaskIdOf } from "./brainView";
import { scheduleBrainBirths } from "./brainMotion";
import type { NodeKind, NodeState } from "./brainOntology";
import type { BrainLayoutData, BrainLayoutLink, BrainLayoutNode } from "./forceBrainTypes";
import { useGraphSize } from "./useGraphSize";
import styles from "./ForceBrainGraph.module.css";

const reducedMotion = typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

function clamp(value: number, lo: number, hi: number): number {
  return Math.min(hi, Math.max(lo, value));
}

// Cubic ease-out — APPROXIMATES --remedy-ease-soft (cubic-bezier(0.22, 1,
// 0.36, 1), motion_spec.md); this is not that bezier, just a cheap stand-in
// with the same "fast start, soft landing" shape for a canvas scale-in.
function easeOutApprox(p: number): number {
  return 1 - Math.pow(1 - p, 3);
}

// Status palette — mirrors tokens.css status palette (single source of truth
// for the real colour values; this file is on the raw-colour carve-out list,
// tests/ui_contracts/test_raw_colour_ratchet.py, because a 2D canvas context
// never resolves var()). Keys are the ontology's real NodeState values.
const STATE_FILL: Record<NodeState, string> = {
  open: "#a78bfa",
  planned: "#ffffff",
  in_progress: "#4c83ff",
  pass: "#34c27e",
  fail: "#ef6363",
  blocked: "#ef6363",
  // Reserved for the future struck-slash treatment (graph_spec §7); this
  // reducer never assigns `vetoed` yet, so the value is a placeholder grey.
  vetoed: "#9aa9c5",
};
const STATE_RING: Record<NodeState, string> = {
  open: "rgba(167,139,250,.4)",
  planned: "#9db9ee",
  in_progress: "rgba(76,131,255,.4)",
  pass: "rgba(52,194,126,.35)",
  fail: "rgba(239,99,99,.4)",
  blocked: "rgba(239,99,99,.4)",
  vetoed: "rgba(154,169,197,.4)",
};

/** How far into its birth a node is right now: `p` (0..1, clamped), and
 *  whether this birth is a plain fade (reduced motion) rather than a scale-in
 *  spring. `null` when the node carries no in-flight birth (paints at rest). */
interface BirthProgress {
  p: number;
  fade: boolean;
}

/** What a birth contributes to one paint call — a fade multiplies alpha by
 *  `p`, a spring scales the radius by an eased `p`; a node with no birth in
 *  flight paints with both at 1 (at rest). */
interface BrainNodePaint {
  alpha: number;
  scale: number;
}

function paintOf(progress: BirthProgress | null): BrainNodePaint {
  if (!progress) return { alpha: 1, scale: 1 };
  return progress.fade ? { alpha: progress.p, scale: 1 } : { alpha: 1, scale: easeOutApprox(progress.p) };
}

type NodePainter = (node: BrainLayoutNode, ctx: CanvasRenderingContext2D, globalScale: number, paint: BrainNodePaint) => void;

/** The core: existing halo (r64 radial gradient) + core sphere (r26 gradient)
 *  + white ring + `</>` glyph — geometry unchanged from the previous painter. */
function paintCoreNode(node: BrainLayoutNode, ctx: CanvasRenderingContext2D, _globalScale: number, paint: BrainNodePaint): void {
  const { x, y } = node;
  ctx.save();
  ctx.globalAlpha = paint.alpha;
  const halo = ctx.createRadialGradient(x, y, 6, x, y, 64);
  halo.addColorStop(0, "rgba(76,131,255,0.55)");
  halo.addColorStop(0.5, "rgba(76,131,255,0.18)");
  halo.addColorStop(1, "rgba(76,131,255,0)");
  ctx.fillStyle = halo;
  ctx.beginPath(); ctx.arc(x, y, 64, 0, Math.PI * 2); ctx.fill();
  const core = ctx.createRadialGradient(x - 6, y - 8, 4, x, y, 26);
  core.addColorStop(0, "#7ea6ff");
  core.addColorStop(1, "#2f6fff");
  ctx.fillStyle = core;
  ctx.beginPath(); ctx.arc(x, y, 26, 0, Math.PI * 2); ctx.fill();
  ctx.strokeStyle = "rgba(255,255,255,0.85)"; ctx.lineWidth = 2; ctx.stroke();
  ctx.fillStyle = "#ffffff";
  ctx.font = "600 15px ui-monospace, Menlo, monospace";
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillText("</>", x, y + 1);
  ctx.restore();
}

/** Every non-core node: a glossy sphere (radial gradient white-highlight →
 *  state fill) with a soft outer ring, at the node's OWN `radius` —
 *  `buildBrainLayout` already resolved that to 7 for a task, 4.5 for a run
 *  kind/synapse/artifact, 9 for a cluster (graph_spec §4), so one painter
 *  covers all of them; the glyph-per-kind lifecycle feature swaps entries in
 *  `NODE_PAINTERS` later without touching this function's shape. */
function paintSphereNode(node: BrainLayoutNode, ctx: CanvasRenderingContext2D, _globalScale: number, paint: BrainNodePaint): void {
  const { x, y } = node;
  const r = node.radius * paint.scale;
  const fill = STATE_FILL[node.state];
  const ring = STATE_RING[node.state];
  ctx.save();
  ctx.globalAlpha = paint.alpha;
  ctx.fillStyle = ring;
  ctx.beginPath(); ctx.arc(x, y, r + 2.5, 0, Math.PI * 2); ctx.fill();
  const gradient = ctx.createRadialGradient(x - r * 0.4, y - r * 0.5, r * 0.2, x, y, r);
  gradient.addColorStop(0, "rgba(255,255,255,0.9)");
  gradient.addColorStop(0.35, fill);
  gradient.addColorStop(1, fill);
  ctx.fillStyle = gradient;
  ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
  if (node.state === "planned") { ctx.strokeStyle = STATE_RING.planned; ctx.lineWidth = 1.2; ctx.stroke(); }
  ctx.restore();
}

// The glyph slots the lifecycle feature fills later (one entry per NodeKind
// so a future round can give a run kind its own Path2D glyph without
// touching the paint call sites).
const NODE_PAINTERS: Record<NodeKind, NodePainter> = {
  job_core: paintCoreNode,
  task: paintSphereNode,
  builder_run: paintSphereNode,
  review_run: paintSphereNode,
  repair_run: paintSphereNode,
  test_run: paintSphereNode,
  synapse: paintSphereNode,
  artifact: paintSphereNode,
  cluster: paintSphereNode,
};

function brainPointerAreaPaint(node: object, color: string, ctx: CanvasRenderingContext2D) {
  const n = node as BrainLayoutNode;
  const r = Math.max(n.radius + 4, 10);
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI * 2); ctx.fill();
}

// Per-edge jitter control point seeded by the edge's own id (graph_spec §6):
// deterministic, so the same job always bends the same link the same way.
function curvatureFor(linkId: string): number {
  return 0.05 + seededRng(linkId)() * 0.1;
}

interface D3ForceStrength { strength: (fn: (node: object) => number) => unknown; }
interface D3ForceDistance { distance: (fn: (link: object) => number) => unknown; }

export function ForceBrainGraph({ layout, selectedId, onSelectNode }: {
  layout: BrainLayoutData;
  selectedId: string | null;
  onSelectNode: (nodeId: string | null) => void;
}) {
  const { containerRef, size } = useGraphSize();
  const graphRef = useRef<ForceGraph2DInstance>(null);

  // The nodes of the graphData LAST PASSED TO THE GRAPH (not the previous
  // layout's own nodes): react-force-graph mutates these objects' x/y in
  // place as the simulation runs, so this ref is the one source that always
  // holds a survivor's latest simulated position, not its seeded one.
  const previousNodesRef = useRef<readonly { id: string; x?: number; y?: number }[] | null>(null);
  const graphData = useMemo(() => ({
    nodes: carryBrainPositions(previousNodesRef.current, layout.nodes),
    links: layout.links.map((l) => ({ ...l })), // fresh objects: the library rewrites source/target into node refs in place
  }), [layout]);
  useEffect(() => {
    previousNodesRef.current = graphData.nodes;
  }, [graphData]);

  // Births: what changed since the last layout, recorded as absolute
  // wall-clock windows the painter reads every frame (graph_spec §11-§12).
  const birthsPreviousLayoutRef = useRef<BrainLayoutData | null>(null);
  const birthRecordsRef = useRef<Map<string, { start: number; durationMs: number; fade: boolean }>>(new Map());
  const [birthsInFlight, setBirthsInFlight] = useState(false);
  const pauseTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // useLayoutEffect, not useEffect: the record must exist before the
  // canvas's next paint, or a newborn's first frame paints at full size.
  useLayoutEffect(() => {
    const births = scheduleBrainBirths(birthsPreviousLayoutRef.current, layout, reducedMotion);
    birthsPreviousLayoutRef.current = layout;
    const now = performance.now();
    births.forEach((b) => {
      birthRecordsRef.current.set(b.id, { start: now + b.delayMs, durationMs: b.durationMs, fade: b.fade });
    });
    // Drop records that already finished so the map cannot grow across a
    // long session — a birth is a moment, not permanent state.
    birthRecordsRef.current.forEach((record, id) => {
      if (now > record.start + record.durationMs) birthRecordsRef.current.delete(id);
    });
    const pendingEndsFromNow = [...birthRecordsRef.current.values()].map((r) => r.start + r.durationMs - now);
    if (pauseTimerRef.current) { clearTimeout(pauseTimerRef.current); pauseTimerRef.current = null; }
    if (pendingEndsFromNow.length === 0) { setBirthsInFlight(false); return; }
    setBirthsInFlight(true);
    const waitMs = Math.max(...pendingEndsFromNow) + 50;
    pauseTimerRef.current = setTimeout(() => {
      setBirthsInFlight(false);
      pauseTimerRef.current = null;
    }, waitMs);
    return () => {
      if (pauseTimerRef.current) { clearTimeout(pauseTimerRef.current); pauseTimerRef.current = null; }
    };
  }, [layout]);

  const birthProgressOf = useCallback((id: string): BirthProgress | null => {
    const record = birthRecordsRef.current.get(id);
    if (!record) return null;
    const p = clamp((performance.now() - record.start) / record.durationMs, 0, 1);
    return { p, fade: record.fade };
  }, []);

  const handleNodeCanvasObject = useCallback((node: object, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const n = node as BrainLayoutNode;
    const paint = paintOf(birthProgressOf(n.id));
    NODE_PAINTERS[n.kind](n, ctx, globalScale, paint);

    if (n.id === selectedId) {
      ctx.save();
      ctx.strokeStyle = "#2f6fff";
      ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.arc(n.x, n.y, n.radius + 5, 0, Math.PI * 2); ctx.stroke();
      ctx.restore();
    }

    if (n.kind === "task" && n.label && globalScale > 1.4) {
      ctx.save();
      ctx.fillStyle = "#3a4f7e";
      ctx.font = `500 ${11 / globalScale}px -apple-system, sans-serif`;
      ctx.textAlign = "center"; ctx.textBaseline = "top";
      ctx.fillText(n.label, n.x, n.y + n.radius + 4);
      ctx.restore();
    }
  }, [selectedId, birthProgressOf]);

  const handleLinkCanvasObject = useCallback((link: object, ctx: CanvasRenderingContext2D) => {
    // force-graph rewrites source/target from ids into node refs in place
    // once the simulation has them — this cast reflects BOTH shapes, since
    // BrainLayoutLink itself only declares the pre-rewrite string ids.
    const l = link as Omit<BrainLayoutLink, "source" | "target"> & {
      source: BrainLayoutNode | string;
      target: BrainLayoutNode | string;
    };
    const source = typeof l.source === "string" ? null : l.source;
    const target = typeof l.target === "string" ? null : l.target;
    if (!source || !target) return;
    const progress = birthProgressOf(target.id);
    const alpha = progress ? progress.p : 1;

    const sx = source.x, sy = source.y;
    const tx = target.x, ty = target.y;
    const mx = (sx + tx) / 2, my = (sy + ty) / 2;
    const dx = tx - sx, dy = ty - sy;
    const len = Math.sqrt(dx * dx + dy * dy) || 1;
    const curvature = curvatureFor(l.id);
    const cx = mx + (-dy / len) * curvature * 80;
    const cy = my + (dx / len) * curvature * 80;

    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = "rgba(190, 212, 248, 0.8)";
    ctx.lineWidth = l.width;
    ctx.beginPath();
    ctx.moveTo(sx, sy);
    ctx.quadraticCurveTo(cx, cy, tx, ty);
    ctx.stroke();
    ctx.restore();
  }, [birthProgressOf]);

  const handleNodeClick = useCallback((node: object) => {
    const id = selectionTaskIdOf(node as BrainLayoutNode);
    if (id !== null) onSelectNode(id);
  }, [onSelectNode]);

  // Configure the EXISTING d3 forces (getter, then call its own setter) —
  // replacing them with a plain object, as the old decorative renderer did,
  // leaves d3 nothing it can call (graph_spec §6).
  useEffect(() => {
    const fg = graphRef.current;
    if (!fg) return;
    try {
      const charge = fg.d3Force("charge") as D3ForceStrength | undefined;
      if (charge && typeof charge.strength === "function") {
        charge.strength((n: object) => ((n as BrainLayoutNode).depth <= 1 ? -60 : -12));
      }
      const link = fg.d3Force("link") as D3ForceDistance | undefined;
      if (link && typeof link.distance === "function") {
        link.distance((l: object) => ((l as BrainLayoutLink).depth === 1 ? 150 : 34));
      }
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
    // graph_spec §14: the canvas is not the accessible surface — the task
    // checklist, the popover and the stage's Simple view are.
    <div ref={containerRef} className={styles.container} data-ui="force-brain-graph" aria-hidden="true">
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
          autoPauseRedraw={!birthsInFlight}
          enableNodeDrag
          enableZoomInteraction
          enablePanInteraction
          minZoom={0.3}
          maxZoom={4}
          onNodeClick={handleNodeClick}
          onBackgroundClick={() => onSelectNode(null)}
          nodeCanvasObject={handleNodeCanvasObject}
          nodeCanvasObjectMode={() => "replace"}
          nodePointerAreaPaint={brainPointerAreaPaint}
          linkCanvasObject={handleLinkCanvasObject}
          linkCanvasObjectMode={() => "replace"}
          linkDirectionalParticles={(l) => ((l as BrainLayoutLink).active && !reducedMotion ? 1 : 0)}
          linkDirectionalParticleWidth={2}
          onEngineStop={() => { /* simulation settled */ }}
        />
      )}
    </div>
  );
}
