// Paints one brain-graph node on a 2D canvas from the two sources of truth:
// its kind's geometry from glyphPaths.ts and its state's treatment from
// nodeStates.ts, in the colours the palette bridge resolved. It holds no
// colour, no shape and no state rule of its own (graph_spec.md §5,
// assets_spec.md §4, DECISION F020 D2). The job core keeps its own painter in
// ForceBrainGraph.tsx.
import type { NodeKind, NodeState } from "../brainOntology";
import { GLYPHS, STATE_MARK_PATHS, glyphDrawnAt, glyphPath2D, glyphTransform } from "./glyphPaths";
import type { GlyphPath2D } from "./glyphPaths";
import { NODE_STATE_TREATMENTS } from "./nodeStates";
import type { RemedyToken, StateMarkPaint } from "./nodeStates";
import { BRAIN_HIGHLIGHT_TOKEN, BRAIN_LABEL_FONT_TOKEN } from "./palette";
import type { BrainPalette } from "./palette";

/** Glyph stroke width in the 24-unit box, the value of `--remedy-icon-stroke`
 *  (assets_spec.md §4: "stroke --remedy-icon-stroke×scale, round caps"). */
export const GLYPH_STROKE_WIDTH = 1.5;

/** How far the soft halo reaches past the node's edge, in world units (the
 *  value F019's painter drew). */
export const HALO_SPREAD = 2.5;

/** The kinds drawn as a glossy state sphere with their glyph on top, in the
 *  state's ink; every other kind's glyph IS its body, filled in the state's
 *  colour and lined in the state's line colour. */
export const SPHERE_KINDS: ReadonlySet<NodeKind> = new Set<NodeKind>([
  "task", "builder_run", "review_run", "repair_run", "test_run",
]);

/** The fields of a positioned node this painter reads. `label` is written
 *  inside a cluster as its count (graph_spec §4: "cluster: r 9 + count") and
 *  is not painted for any other kind here. */
export interface PaintableNode {
  kind: NodeKind;
  state: NodeState;
  x: number;
  y: number;
  radius: number;
  label?: string;
}

/** A cluster's count is written at this share of the node's radius. */
export const CLUSTER_COUNT_SIZE = 0.75;

/** What the frame contributes: the resolved palette, the canvas zoom, and a
 *  birth's alpha and scale (1 and 1 at rest). */
export interface NodePaintFrame {
  palette: BrainPalette;
  zoom: number;
  alpha: number;
  scale: number;
}

function tokenValue(palette: BrainPalette, token: RemedyToken): string {
  return palette[token] ?? "";
}

/** Run `draw` with the canvas mapped onto the node's 24-unit glyph box. */
function inGlyphBox(ctx: CanvasRenderingContext2D, node: PaintableNode, radius: number, draw: () => void): void {
  const t = glyphTransform(node.x, node.y, radius);
  ctx.save();
  ctx.translate(t.offsetX, t.offsetY);
  ctx.scale(t.scale, t.scale);
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  draw();
  ctx.restore();
}

/** Fill then stroke a glyph's two paths in the colours given; a null colour
 *  or an empty path leaves that half undrawn. */
function drawPaths(ctx: CanvasRenderingContext2D, paths: GlyphPath2D, fill: string | null, stroke: string | null): void {
  if (fill !== null && paths.fill) {
    ctx.fillStyle = fill;
    ctx.fill(paths.fill);
  }
  if (stroke !== null && paths.stroke) {
    ctx.strokeStyle = stroke;
    ctx.lineWidth = GLYPH_STROKE_WIDTH;
    ctx.stroke(paths.stroke);
  }
}

/** One state mark: where it names an outline, the mark's own shape is first
 *  stroked twice as wide in that colour, so it stands off the node beneath. */
function drawMark(ctx: CanvasRenderingContext2D, mark: StateMarkPaint, node: PaintableNode, radius: number, palette: BrainPalette): void {
  const paths = glyphPath2D(STATE_MARK_PATHS[mark.mark]);
  const colour = tokenValue(palette, mark.token);
  inGlyphBox(ctx, node, radius, () => {
    const shape = paths.stroke ?? paths.fill;
    if (mark.outlineToken && shape) {
      ctx.strokeStyle = tokenValue(palette, mark.outlineToken);
      ctx.lineWidth = GLYPH_STROKE_WIDTH * 2;
      ctx.stroke(shape);
    }
    drawPaths(ctx, paths, colour, colour);
  });
}

/** Paint one non-core node: halo, body, glyph where the zoom allows it, then
 *  the state's marks, so state never rests on colour alone. */
export function paintBrainNode(ctx: CanvasRenderingContext2D, node: PaintableNode, frame: NodePaintFrame): void {
  const treatment = NODE_STATE_TREATMENTS[node.state];
  const radius = node.radius * treatment.sizeFactor * frame.scale;
  const fill = tokenValue(frame.palette, treatment.fillToken);
  const highlight = tokenValue(frame.palette, BRAIN_HIGHLIGHT_TOKEN);
  const ink = tokenValue(frame.palette, treatment.inkToken);
  const line = tokenValue(frame.palette, treatment.lineToken);
  const glyph = GLYPHS[node.kind];
  const paths = glyphPath2D(glyph);
  ctx.save();
  ctx.globalAlpha = frame.alpha;
  if (SPHERE_KINDS.has(node.kind)) {
    if (treatment.halo) {
      ctx.globalAlpha = frame.alpha * treatment.halo.alpha;
      ctx.fillStyle = tokenValue(frame.palette, treatment.halo.token);
      ctx.beginPath();
      ctx.arc(node.x, node.y, radius + HALO_SPREAD, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = frame.alpha;
    }
    const gradient = ctx.createRadialGradient(node.x - radius * 0.4, node.y - radius * 0.5, radius * 0.2, node.x, node.y, radius);
    gradient.addColorStop(0, highlight);
    gradient.addColorStop(0.35, fill);
    gradient.addColorStop(1, fill);
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
    ctx.fill();
    if (paths.stroke && glyphDrawnAt(node.kind, frame.zoom)) {
      inGlyphBox(ctx, node, radius, () => drawPaths(ctx, paths, null, ink));
    }
  } else {
    inGlyphBox(ctx, node, radius, () => drawPaths(ctx, paths, fill, line));
  }
  if (node.kind === "cluster" && node.label) {
    ctx.fillStyle = line;
    ctx.font = `600 ${radius * CLUSTER_COUNT_SIZE}px ${tokenValue(frame.palette, BRAIN_LABEL_FONT_TOKEN)}`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(node.label, node.x, node.y);
  }
  for (const mark of treatment.marks) drawMark(ctx, mark, node, radius, frame.palette);
  ctx.restore();
}
