import { describe, expect, it } from "vitest";
import { BRAIN_CLUSTER_RADIUS, BRAIN_RUN_RADIUS, BRAIN_TASK_RADIUS } from "../buildForceBrainModel";
import { glyphDrawnAt, glyphKinds } from "./glyphPaths";
import { nodeStateOrder } from "./nodeStates";
import {
  MATRIX_CELL, MATRIX_CLUSTER_LABEL, MATRIX_ZOOM, glyphMatrixCells, glyphMatrixSize, paintGlyphMatrix,
} from "./glyphMatrix";
import type { NodePaintFrame, PaintableNode } from "./paintNode";
import type { BrainPalette } from "./palette";

const KINDS = glyphKinds().filter((k) => k !== "job_core");
const STATES = nodeStateOrder();

describe("glyphMatrixCells", () => {
  it("holds every non-core kind in every state exactly once", () => {
    const pairs = glyphMatrixCells().map((c) => `${c.node.kind}/${c.node.state}`);
    expect(pairs).toHaveLength(KINDS.length * STATES.length);
    expect(new Set(pairs).size).toBe(pairs.length);
    for (const kind of KINDS) for (const state of STATES) expect(pairs).toContain(`${kind}/${state}`);
  });

  it("puts kinds on rows in the glyph module's order and states on columns in the state module's", () => {
    for (const cell of glyphMatrixCells()) {
      expect(KINDS[cell.row]).toBe(cell.node.kind);
      expect(STATES[cell.col]).toBe(cell.node.state);
    }
  });

  it("centres each cell on its grid slot at the layout's own radius for the kind", () => {
    const radius = { task: BRAIN_TASK_RADIUS, cluster: BRAIN_CLUSTER_RADIUS } as Record<string, number>;
    for (const cell of glyphMatrixCells()) {
      expect(cell.node.x).toBe(MATRIX_CELL / 2 + cell.col * MATRIX_CELL);
      expect(cell.node.y).toBe(MATRIX_CELL / 2 + cell.row * MATRIX_CELL);
      expect(cell.node.radius, cell.node.kind).toBe(radius[cell.node.kind] ?? BRAIN_RUN_RADIUS);
    }
  });

  it("keeps every cell, halo and all, inside its own slot", () => {
    const largest = Math.max(...glyphMatrixCells().map((c) => c.node.radius));
    expect(2 * (largest + 2.5)).toBeLessThanOrEqual(MATRIX_CELL);
  });

  it("gives every cluster cell its count and no other cell a label", () => {
    for (const cell of glyphMatrixCells()) {
      expect(cell.node.label, `${cell.node.kind}/${cell.node.state}`)
        .toBe(cell.node.kind === "cluster" ? MATRIX_CLUSTER_LABEL : "");
    }
  });
});

describe("glyphMatrixSize", () => {
  it("is the columns and rows of the grid in cells", () => {
    expect(glyphMatrixSize()).toEqual({ width: STATES.length * MATRIX_CELL, height: KINDS.length * MATRIX_CELL });
  });
});

describe("paintGlyphMatrix", () => {
  it("paints at a zoom where every run kind shows its glyph", () => {
    for (const kind of KINDS) expect(glyphDrawnAt(kind, MATRIX_ZOOM), kind).toBe(true);
  });

  it("paints every cell once, at rest, at the L1 zoom, with the palette it was given", () => {
    const palette: BrainPalette = { "--remedy-state-done": "x" };
    const painted: [PaintableNode, NodePaintFrame][] = [];
    paintGlyphMatrix({} as CanvasRenderingContext2D, palette, (_ctx, node, frame) => { painted.push([node, frame]); });
    expect(painted.map(([n]) => n)).toEqual(glyphMatrixCells().map((c) => c.node));
    for (const [, frame] of painted) expect(frame).toEqual({ palette, zoom: MATRIX_ZOOM, alpha: 1, scale: 1 });
  });
});
