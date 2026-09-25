// The ONE geometry source for every brain-graph glyph. Each glyph is stored
// once, as SVG path data in a 24×24 box; the canvas builds its Path2D from
// those same strings and the legend renders them as SVG, so the graph and its
// legend cannot drift apart (graph_spec.md §5, assets_spec.md §4, T5_F020.md).
//
// Precedence, quoted verbatim from docs/ui/design_reference/assets_spec.md §4:
// "This is the codified form of `graph_spec.md` §5; on conflict, graph_spec §5
// + this table win over any feature-file prose."
//
// Paths use absolute M, L, H, V, A and Z commands only, so a test can read
// every coordinate without a path library. Colour is never decided here:
// nodeStates.ts owns state, and state is painted from `--remedy-state-*`.
import type { NodeKind } from "../brainOntology";

/** The side of the square box every glyph path is drawn in. */
export const GLYPH_BOX = 24;

/** The zoom at which run kinds show their glyph: graph_spec §5 draws run
 *  glyphs "at zoom ≥ L1", and §10 enters L1 at a zoom above 1.6. Below it a
 *  run is a plain state-coloured sphere, so its state still reads at distance. */
export const GLYPH_MIN_ZOOM_RUN = 1.6;

/** The drawn extent of a glyph inside the 24×24 box. */
export interface GlyphBounds {
  minX: number;
  minY: number;
  maxX: number;
  maxY: number;
}

/** One glyph: a text name for the list view and tooltips (assets_spec §4,
 *  accessibility fallback), the path that is stroked, the path that is
 *  filled, the extent both cover, and the lowest zoom it is drawn at. An
 *  empty path means that half is not drawn. */
export interface GlyphGeometry {
  name: string;
  strokePath: string;
  fillPath: string;
  bounds: GlyphBounds;
  minZoom: number;
}

/** One glyph per node kind, in legend order. Shapes per assets_spec §4. */
export const GLYPHS: Readonly<Record<NodeKind, GlyphGeometry>> = {
  job_core: {
    name: "Job",
    strokePath: "M9 8.5L5.5 12L9 15.5M15 8.5L18.5 12L15 15.5M13 7L11 17",
    fillPath: "M23 12A11 11 0 1 1 1 12A11 11 0 1 1 23 12Z",
    bounds: { minX: 1, minY: 1, maxX: 23, maxY: 23 },
    minZoom: 0,
  },
  task: {
    name: "Task",
    strokePath: "",
    fillPath: "M22 12A10 10 0 1 1 2 12A10 10 0 1 1 22 12Z",
    bounds: { minX: 2, minY: 2, maxX: 22, maxY: 22 },
    minZoom: 0,
  },
  builder_run: {
    name: "Builder run",
    strokePath: "M8 7L4 12L8 17M16 7L20 12L16 17M13.5 5L10.5 19",
    fillPath: "",
    bounds: { minX: 4, minY: 5, maxX: 20, maxY: 19 },
    minZoom: GLYPH_MIN_ZOOM_RUN,
  },
  review_run: {
    name: "Review run",
    strokePath: "M15.5 8A3.5 3.5 0 1 1 8.5 8A3.5 3.5 0 1 1 15.5 8ZM5 20A7 7 0 0 1 19 20",
    fillPath: "",
    bounds: { minX: 5, minY: 4.5, maxX: 19, maxY: 20 },
    minZoom: GLYPH_MIN_ZOOM_RUN,
  },
  repair_run: {
    name: "Repair run",
    strokePath: "M10 9.5L7.5 12L10 14.5M14 9.5L16.5 12L14 14.5M12 2A10 10 0 1 1 2 12M0 14L2 12L4 14",
    fillPath: "",
    bounds: { minX: 0, minY: 2, maxX: 22, maxY: 22 },
    minZoom: GLYPH_MIN_ZOOM_RUN,
  },
  test_run: {
    name: "Test run",
    strokePath: "M10 3V9L4.5 19.5L5.5 21H18.5L19.5 19.5L14 9V3M8.5 3H15.5M7 15H17",
    fillPath: "",
    bounds: { minX: 4.5, minY: 3, maxX: 19.5, maxY: 21 },
    minZoom: GLYPH_MIN_ZOOM_RUN,
  },
  synapse: {
    name: "Prompt or tool call",
    strokePath: "",
    fillPath: "M16 12A4 4 0 1 1 8 12A4 4 0 1 1 16 12Z",
    bounds: { minX: 8, minY: 8, maxX: 16, maxY: 16 },
    minZoom: 0,
  },
  artifact: {
    name: "Artifact",
    strokePath: "M6 3H14L19 8V21H6ZM14 3V8H19",
    fillPath: "M14 3L19 8H14Z",
    bounds: { minX: 6, minY: 3, maxX: 19, maxY: 21 },
    minZoom: 0,
  },
  cluster: {
    name: "Collapsed runs",
    strokePath: "M21 12A9 9 0 1 1 3 12A9 9 0 1 1 21 12Z",
    fillPath: "",
    bounds: { minX: 3, minY: 3, maxX: 21, maxY: 21 },
    minZoom: 0,
  },
};

/** The marks a state adds on top of a glyph (nodeStates.ts decides which
 *  state carries which): a small status dot at the top right, a 45° strike
 *  slash, a crisp outer ring, and (DECISION F025 D3 clause 3) `pause`'s two
 *  upright bars in that same status-dot corner. Same box, same rules as
 *  GLYPHS. */
export type StateMark = "status_dot" | "strike" | "ring" | "pause";

export const STATE_MARK_PATHS: Readonly<Record<StateMark, GlyphGeometry>> = {
  status_dot: {
    name: "Status dot",
    strokePath: "",
    fillPath: "M23 4.5A3 3 0 1 1 17 4.5A3 3 0 1 1 23 4.5Z",
    bounds: { minX: 17, minY: 1.5, maxX: 23, maxY: 7.5 },
    minZoom: 0,
  },
  strike: {
    name: "Strike",
    strokePath: "M3 21L21 3",
    fillPath: "",
    bounds: { minX: 3, minY: 3, maxX: 21, maxY: 21 },
    minZoom: 0,
  },
  ring: {
    name: "Ring",
    strokePath: "M23 12A11 11 0 1 1 1 12A11 11 0 1 1 23 12Z",
    fillPath: "",
    bounds: { minX: 1, minY: 1, maxX: 23, maxY: 23 },
    minZoom: 0,
  },
  // Two upright bars in the status dot's own box (U5): a fill path of two
  // rectangles, x 17-19 and 21-23, with a visible 2-unit gap between them,
  // both spanning the full y 1.5-7.5 — the box's own bounds, unchanged.
  pause: {
    name: "Pause",
    strokePath: "",
    fillPath: "M17 1.5H19V7.5H17ZM21 1.5H23V7.5H21Z",
    bounds: { minX: 17, minY: 1.5, maxX: 23, maxY: 7.5 },
    minZoom: 0,
  },
};

/** Every node kind that has a glyph, in legend order — read from GLYPHS
 *  itself, so a kind removed there leaves every consumer of this list. */
export function glyphKinds(): NodeKind[] {
  return Object.keys(GLYPHS) as NodeKind[];
}

/** Whether a kind's glyph is drawn at this zoom; below its minimum the node
 *  is drawn as a plain state-coloured sphere (graph_spec §5, §10). */
export function glyphDrawnAt(kind: NodeKind, zoom: number): boolean {
  return zoom >= GLYPHS[kind].minZoom;
}

/** Where a glyph's 24×24 box lands on the canvas for a node of `radius`
 *  centred at (x, y): the box is scaled to the node's diameter and centred
 *  on it, so `ctx.translate(offsetX, offsetY); ctx.scale(scale, scale)`
 *  draws the glyph over the node. */
export function glyphTransform(x: number, y: number, radius: number): { scale: number; offsetX: number; offsetY: number } {
  const scale = (2 * radius) / GLYPH_BOX;
  const half = (GLYPH_BOX / 2) * scale;
  return { scale, offsetX: x - half, offsetY: y - half };
}

/** The canvas form of one glyph: Path2D objects built from the SAME strings
 *  the legend renders, or null where that half is empty. */
export interface GlyphPath2D {
  stroke: Path2D | null;
  fill: Path2D | null;
}

const path2dCache = new Map<GlyphGeometry, GlyphPath2D>();

/** The Path2D pair for a glyph or a state mark, built once per geometry and
 *  reused on every frame after that. */
export function glyphPath2D(geometry: GlyphGeometry): GlyphPath2D {
  const cached = path2dCache.get(geometry);
  if (cached) return cached;
  const built: GlyphPath2D = {
    stroke: geometry.strokePath ? new Path2D(geometry.strokePath) : null,
    fill: geometry.fillPath ? new Path2D(geometry.fillPath) : null,
  };
  path2dCache.set(geometry, built);
  return built;
}
