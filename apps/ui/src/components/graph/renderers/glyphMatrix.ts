// The kind-by-state matrix fixture: every non-core node kind in every node
// state, laid out as a story grid and painted by the SAME painter the live
// canvas uses, for visual review and for the conformance assertions that read
// its pixels (T5_F020.md, Design, "Conformance fixture"). Rows follow the
// glyph module's kind order and columns the state module's order, so a kind
// or a state added there joins the matrix with no edit here.
import type { NodeKind, NodeState } from "../brainOntology";
import { BRAIN_CLUSTER_RADIUS, BRAIN_RUN_RADIUS, BRAIN_TASK_RADIUS } from "../buildForceBrainModel";
import { GLYPH_MIN_ZOOM_RUN, glyphKinds } from "./glyphPaths";
import { nodeStateOrder } from "./nodeStates";
import { paintBrainNode } from "./paintNode";
import type { NodePaintFrame, PaintableNode } from "./paintNode";
import type { BrainPalette } from "./palette";

/** The distance between two cell centres, in world units. */
export const MATRIX_CELL = 24;

/** The zoom the matrix is painted at: L1, so every run shows its glyph. */
export const MATRIX_ZOOM = GLYPH_MIN_ZOOM_RUN;

/** The count a cluster cell carries, so the count text is in the fixture. */
export const MATRIX_CLUSTER_LABEL = "+3";

/** One cell: the node painted there and its grid position. */
export interface MatrixCell {
  row: number;
  col: number;
  node: PaintableNode;
}

/** A kind's radius at zoom 1, as the layout gives it (graph_spec §4). */
function radiusOf(kind: NodeKind): number {
  if (kind === "task") return BRAIN_TASK_RADIUS;
  if (kind === "cluster") return BRAIN_CLUSTER_RADIUS;
  return BRAIN_RUN_RADIUS;
}

/** Every non-core kind in every state, one cell each, centred on a grid of
 *  MATRIX_CELL starting half a cell in from the origin. The core has its own
 *  painter and one state that matters, so it is not a row. */
export function glyphMatrixCells(): MatrixCell[] {
  const kinds = glyphKinds().filter((k) => k !== "job_core");
  const states: NodeState[] = nodeStateOrder();
  return kinds.flatMap((kind, row) => states.map((state, col) => ({
    row,
    col,
    node: {
      kind,
      state,
      x: MATRIX_CELL / 2 + col * MATRIX_CELL,
      y: MATRIX_CELL / 2 + row * MATRIX_CELL,
      radius: radiusOf(kind),
      label: kind === "cluster" ? MATRIX_CLUSTER_LABEL : "",
    },
  })));
}

/** The grid's size in world units: columns by rows of MATRIX_CELL. */
export function glyphMatrixSize(): { width: number; height: number } {
  const cells = glyphMatrixCells();
  const cols = Math.max(...cells.map((c) => c.col)) + 1;
  const rows = Math.max(...cells.map((c) => c.row)) + 1;
  return { width: cols * MATRIX_CELL, height: rows * MATRIX_CELL };
}

/** Paint the whole matrix at rest, through `paint` — the live painter unless
 *  a test hands in a recorder. */
export function paintGlyphMatrix(
  ctx: CanvasRenderingContext2D,
  palette: BrainPalette,
  paint: (ctx: CanvasRenderingContext2D, node: PaintableNode, frame: NodePaintFrame) => void = paintBrainNode,
): void {
  for (const cell of glyphMatrixCells()) {
    paint(ctx, cell.node, { palette, zoom: MATRIX_ZOOM, alpha: 1, scale: 1 });
  }
}
