import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import type { ForceGraph2DInstance } from "react-force-graph-2d";
import { seededRng } from "./buildForceBrainModel";
import { carryBrainPositions, selectionTaskIdOf } from "./brainView";
import { scheduleBrainBirths } from "./brainMotion";
import type { NodeKind } from "./brainOntology";
import type { BrainLayoutData, BrainLayoutLink, BrainLayoutNode } from "./forceBrainTypes";
import { useGraphSize } from "./useGraphSize";
import { paintBrainNodeInMotion } from "./renderers/paintNode";
import type { NodeMotion } from "./renderers/paintNode";
import { pulseScaleAt } from "./renderers/nodeStates";
import {
  STATE_TRANSITION_MS, brainNeedsAnimationFrames, layoutHasPulse, scheduleStateTransitions, transitionFrameAt,
} from "./renderers/stateMotion";
import type { StateTransition } from "./renderers/stateMotion";
import { usePageVisible } from "./usePageVisible";
import { readDocumentPalette } from "./renderers/palette";
import type { BrainPalette } from "./renderers/palette";
import { isZoomRunKind } from "./semanticZoom";
import type { ZoomEvent, ZoomState } from "./semanticZoom";
import { wheelZoomEvent } from "./zoomWheel";
import { ZOOM_CAMERA_MS, ZOOM_DIM_ALPHA, ZOOM_HOME_CAMERA, zoomCamera } from "./zoomView";
import type { ZoomEmphasis } from "./zoomView";
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

type NodePainter = (
  node: BrainLayoutNode, ctx: CanvasRenderingContext2D, globalScale: number, paint: BrainNodePaint, palette: BrainPalette,
  motion: NodeMotion,
) => void;

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

/** Every non-core node, drawn from its kind's glyph and its state's
 *  treatment in the resolved palette, with its pulse and any state change in
 *  flight (renderers/paintNode.ts; DECISIONS F020 D2 and D4).
 *  `buildBrainLayout` already resolved the node's radius per kind (graph_spec
 *  §4); the zoom decides whether a run shows its glyph. */
function paintGlyphNode(
  node: BrainLayoutNode, ctx: CanvasRenderingContext2D, globalScale: number, paint: BrainNodePaint, palette: BrainPalette,
  motion: NodeMotion,
): void {
  paintBrainNodeInMotion(ctx, node, { palette, zoom: globalScale, alpha: paint.alpha, scale: paint.scale }, motion);
}

// One painter per NodeKind: the core keeps its own, and every other kind is
// drawn from the glyph and state modules (T5_F020.md T002, which replaces
// F019's placeholder slots here).
const NODE_PAINTERS: Record<NodeKind, NodePainter> = {
  job_core: paintCoreNode,
  task: paintGlyphNode,
  builder_run: paintGlyphNode,
  review_run: paintGlyphNode,
  repair_run: paintGlyphNode,
  test_run: paintGlyphNode,
  synapse: paintGlyphNode,
  artifact: paintGlyphNode,
  cluster: paintGlyphNode,
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

export function ForceBrainGraph({ layout, selectedId, onSelectNode, zoom, emphasis, onZoomEvent }: {
  layout: BrainLayoutData;
  selectedId: string | null;
  onSelectNode: (nodeId: string | null) => void;
  zoom: ZoomState;
  emphasis: ZoomEmphasis;
  onZoomEvent: (event: ZoomEvent) => void;
}) {
  const { containerRef, size } = useGraphSize();
  const pageVisible = usePageVisible();
  // Every token the node painter reads, resolved once per mount: a 2D
  // canvas cannot read var() (tokens_rules.md, the palette bridge).
  const resolvedPalette = useMemo(() => readDocumentPalette(), []);
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

  // State changes: what changed state since the last layout, recorded the
  // same way as births, so the painter can crossfade and ripple it
  // (graph_spec §12; DECISION F020 D4).
  const transitionsPreviousLayoutRef = useRef<BrainLayoutData | null>(null);
  const transitionRecordsRef = useRef<Map<string, StateTransition>>(new Map());
  const [transitionsInFlight, setTransitionsInFlight] = useState(false);

  useLayoutEffect(() => {
    const now = performance.now();
    scheduleStateTransitions(transitionsPreviousLayoutRef.current, layout, now, reducedMotion)
      .forEach((t) => transitionRecordsRef.current.set(t.id, t));
    transitionsPreviousLayoutRef.current = layout;
    transitionRecordsRef.current.forEach((t, id) => {
      if (now >= t.startMs + t.durationMs) transitionRecordsRef.current.delete(id);
    });
    if (transitionRecordsRef.current.size === 0) { setTransitionsInFlight(false); return; }
    setTransitionsInFlight(true);
    const timer = setTimeout(() => setTransitionsInFlight(false), STATE_TRANSITION_MS + 50);
    return () => clearTimeout(timer);
  }, [layout]);

  const pulsing = useMemo(() => layoutHasPulse(layout), [layout]);
  const animating = brainNeedsAnimationFrames({ pageVisible, reducedMotion, birthsInFlight, transitionsInFlight, pulsing });

  const motionOf = useCallback((n: BrainLayoutNode): NodeMotion => {
    const now = performance.now();
    const record = transitionRecordsRef.current.get(n.id);
    return {
      fromState: record ? record.from : null,
      transition: record ? transitionFrameAt(record, now) : null,
      pulseScale: pulseScaleAt(n.state, now, reducedMotion),
    };
  }, []);

  const birthProgressOf = useCallback((id: string): BirthProgress | null => {
    const record = birthRecordsRef.current.get(id);
    if (!record) return null;
    const p = clamp((performance.now() - record.start) / record.durationMs, 0, 1);
    return { p, fade: record.fade };
  }, []);

  const handleNodeCanvasObject = useCallback((node: object, ctx: CanvasRenderingContext2D, globalScale: number) => {
    const n = node as BrainLayoutNode;
    const birth = paintOf(birthProgressOf(n.id));
    // graph_spec §10: outside the focused branch, everything dims to 25%.
    const dim = emphasis.dimmed.has(n.id) ? ZOOM_DIM_ALPHA : 1;
    const paint = { alpha: birth.alpha * dim, scale: birth.scale };
    NODE_PAINTERS[n.kind](n, ctx, globalScale, paint, resolvedPalette.palette, motionOf(n));

    if (n.id === selectedId || n.id === emphasis.ringId) {
      ctx.save();
      ctx.strokeStyle = "#2f6fff";
      ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.arc(n.x, n.y, n.radius + 5, 0, Math.PI * 2); ctx.stroke();
      ctx.restore();
    }

    // graph_spec §10, L1: the focused task's label is on at any camera factor.
    if (n.kind === "task" && n.label && (globalScale > 1.4 || emphasis.labelled.has(n.id))) {
      ctx.save();
      ctx.globalAlpha = dim;
      ctx.fillStyle = "#3a4f7e";
      ctx.font = `500 ${11 / globalScale}px -apple-system, sans-serif`;
      ctx.textAlign = "center"; ctx.textBaseline = "top";
      ctx.fillText(n.label, n.x, n.y + n.radius + 4);
      ctx.restore();
    }
  }, [selectedId, birthProgressOf, resolvedPalette, motionOf, emphasis]);

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
    const alpha = (progress ? progress.p : 1) * (emphasis.dimmed.has(target.id) ? ZOOM_DIM_ALPHA : 1);

    const sx = source.x, sy = source.y;
    const tx = target.x, ty = target.y;
    const mx = (sx + tx) / 2, my = (sy + ty) / 2;
    const dx = tx - sx, dy = ty - sy;
    const len = Math.sqrt(dx * dx + dy * dy) || 1;
    const curvature = curvatureFor(l.id);
    const cx = mx + (-dy / len) * curvature * 80;
    const cy = my + (dx / len) * curvature * 80;

    ctx.save();
    // graph_spec §10, L0: a branch with a run in flight glows, in the token
    // that paints an in-progress node (DECISION F023 D2).
    const glow = resolvedPalette.palette["--remedy-state-current"];
    if (emphasis.glowing.has(l.id) && glow) {
      ctx.globalAlpha = alpha * 0.3;
      ctx.strokeStyle = glow;
      ctx.lineWidth = l.width + 6;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(sx, sy);
      ctx.quadraticCurveTo(cx, cy, tx, ty);
      ctx.stroke();
    }
    ctx.globalAlpha = alpha;
    ctx.strokeStyle = "rgba(190, 212, 248, 0.8)";
    ctx.lineWidth = l.width;
    ctx.beginPath();
    ctx.moveTo(sx, sy);
    ctx.quadraticCurveTo(cx, cy, tx, ty);
    ctx.stroke();
    ctx.restore();
  }, [birthProgressOf, emphasis, resolvedPalette]);

  // graph_spec §10: a click is the same transition the wheel and the
  // breadcrumbs make; the shell's selection still opens the task's popover.
  const handleNodeClick = useCallback((node: object) => {
    const n = node as BrainLayoutNode;
    onZoomEvent({ type: "click", nodeId: n.id });
    // A run opens its own L2 detail, not its task's popover (DECISION F023 D4).
    if (isZoomRunKind(n.kind)) return;
    const id = selectionTaskIdOf(n);
    if (id !== null) onSelectNode(id);
  }, [onSelectNode, onZoomEvent]);

  // The wheel adapter reads the camera factor on every zoom frame; a camera
  // move this component makes itself is not a wheel and is ignored until it
  // lands (zoomWheel.ts holds the hysteresis, DECISION F023 D1).
  const hoveredIdRef = useRef<string | null>(null);
  const lastZoomRef = useRef(ZOOM_HOME_CAMERA);
  const cameraLockUntilRef = useRef(0);
  const handleNodeHover = useCallback((node: object | null) => {
    hoveredIdRef.current = node ? (node as BrainLayoutNode).id : null;
  }, []);
  const handleZoom = useCallback(({ k }: { k: number }) => {
    const previous = lastZoomRef.current;
    lastZoomRef.current = k;
    if (performance.now() < cameraLockUntilRef.current) return;
    const event = wheelZoomEvent(previous, k, hoveredIdRef.current);
    if (event) onZoomEvent(event);
  }, [onZoomEvent]);

  // The camera follows the level: L0 fits the organism, L1 centres the task,
  // L2 and L3 centre the run (zoomView.ts).
  const layoutRef = useRef(layout);
  useLayoutEffect(() => {
    layoutRef.current = { nodes: graphData.nodes, links: layout.links };
  }, [graphData, layout]);
  useEffect(() => {
    const fg = graphRef.current;
    const camera = zoomCamera(layoutRef.current, zoom);
    if (!fg || !camera) return;
    const ms = reducedMotion ? 0 : ZOOM_CAMERA_MS;
    cameraLockUntilRef.current = performance.now() + ms + 100;
    fg.centerAt(camera.x, camera.y, ms);
    fg.zoom(camera.k, ms);
  }, [zoom]);

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
      cameraLockUntilRef.current = performance.now() + (reducedMotion ? 0 : 600) + 100;
      fg.zoom(1.0, reducedMotion ? 0 : 600);
      fg.centerAt(0, 0, reducedMotion ? 0 : 600);
    }, reducedMotion ? 100 : 800);
    return () => clearTimeout(timer);
  }, []);

  return (
    // graph_spec §14: the canvas is not the accessible surface — the task
    // checklist, the popover and the stage's Simple view are.
    <div
      ref={containerRef}
      className={styles.container}
      data-ui="force-brain-graph"
      // A token the stylesheet does not declare paints nothing; its name
      // is left here for a test or a reviewer to find, never guessed.
      data-palette-missing={resolvedPalette.missing.length ? resolvedPalette.missing.join(" ") : undefined}
      aria-hidden="true"
    >
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
          autoPauseRedraw={!animating}
          enableNodeDrag
          enableZoomInteraction
          enablePanInteraction
          minZoom={0.3}
          maxZoom={4}
          onNodeClick={handleNodeClick}
          onNodeHover={handleNodeHover}
          onZoom={handleZoom}
          onBackgroundClick={() => onSelectNode(null)}
          nodeCanvasObject={handleNodeCanvasObject}
          nodeCanvasObjectMode={() => "replace"}
          nodePointerAreaPaint={brainPointerAreaPaint}
          linkCanvasObject={handleLinkCanvasObject}
          linkCanvasObjectMode={() => "replace"}
          // A particle keeps the canvas drawing whatever autoPauseRedraw says, so
          // it flows only on an active edge, with motion, on a visible page.
          linkDirectionalParticles={(l) => ((l as BrainLayoutLink).active && !reducedMotion && pageVisible ? 1 : 0)}
          linkDirectionalParticleWidth={2}
          onEngineStop={() => { /* simulation settled */ }}
        />
      )}
    </div>
  );
}
