import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";
import {
  GLYPH_BOX, GLYPH_MIN_ZOOM_RUN, GLYPHS, STATE_MARK_PATHS,
  glyphDrawnAt, glyphKinds, glyphPath2D, glyphTransform,
} from "./glyphPaths";
import type { GlyphBounds, GlyphGeometry } from "./glyphPaths";

/** Every NodeKind brainOntology.ts declares, in the legend order the module
 *  must keep. Written out here so a kind dropped from GLYPHS fails a test. */
const ALL_KINDS = [
  "job_core", "task", "builder_run", "review_run", "repair_run",
  "test_run", "synapse", "artifact", "cluster",
];
const RUN_KINDS = ["builder_run", "review_run", "repair_run", "test_run"];

/** The SVG goldens: the exact strings the legend will render and the canvas
 *  will build its Path2D from. A geometry change must change this table. */
const GOLDEN: Record<string, [string, string]> = {
  job_core: ["M9 8.5L5.5 12L9 15.5M15 8.5L18.5 12L15 15.5M13 7L11 17", "M23 12A11 11 0 1 1 1 12A11 11 0 1 1 23 12Z"],
  task: ["", "M22 12A10 10 0 1 1 2 12A10 10 0 1 1 22 12Z"],
  builder_run: ["M8 7L4 12L8 17M16 7L20 12L16 17M13.5 5L10.5 19", ""],
  review_run: ["M15.5 8A3.5 3.5 0 1 1 8.5 8A3.5 3.5 0 1 1 15.5 8ZM5 20A7 7 0 0 1 19 20", ""],
  repair_run: ["M10 9.5L7.5 12L10 14.5M14 9.5L16.5 12L14 14.5M12 2A10 10 0 1 1 2 12M0 14L2 12L4 14", ""],
  test_run: ["M10 3V9L4.5 19.5L5.5 21H18.5L19.5 19.5L14 9V3M8.5 3H15.5M7 15H17", ""],
  synapse: ["", "M16 12A4 4 0 1 1 8 12A4 4 0 1 1 16 12Z"],
  artifact: ["M6 3H14L19 8V21H6ZM14 3V8H19", "M14 3L19 8H14Z"],
  cluster: ["M21 12A9 9 0 1 1 3 12A9 9 0 1 1 21 12Z", ""],
};

type Point = [number, number];

/** The points that fix a circular arc's extent: its end point, plus every
 *  axis-aligned extreme of its circle that the swept angle passes through
 *  (the SVG endpoint-to-centre conversion, rx == ry, no rotation). */
function arcExtremes(x1: number, y1: number, r: number, large: number, sweep: number, x2: number, y2: number): Point[] {
  const dx = (x1 - x2) / 2;
  const dy = (y1 - y2) / 2;
  const d2 = dx * dx + dy * dy;
  const radius = Math.max(r, Math.sqrt(d2));
  let coef = Math.sqrt(Math.max(0, (radius * radius - d2) / d2));
  if (large === sweep) coef = -coef;
  const cx = coef * dy + (x1 + x2) / 2;
  const cy = -coef * dx + (y1 + y2) / 2;
  const a1 = Math.atan2(y1 - cy, x1 - cx);
  let delta = Math.atan2(y2 - cy, x2 - cx) - a1;
  if (sweep && delta < 0) delta += 2 * Math.PI;
  if (!sweep && delta > 0) delta -= 2 * Math.PI;
  const points: Point[] = [[x2, y2]];
  for (let k = -4; k <= 8; k += 1) {
    const angle = (k * Math.PI) / 2;
    const t = delta ? (angle - a1) / delta : 2;
    if (t >= 0 && t <= 1) points.push([cx + radius * Math.cos(angle), cy + radius * Math.sin(angle)]);
  }
  return points;
}

/** Every point a path's outline can reach, for the M L H V A Z subset. */
function pathPoints(d: string): Point[] {
  const tokens = d.match(/[MLHVAZ]|-?\d*\.?\d+/g) ?? [];
  const points: Point[] = [];
  let x = 0, y = 0, startX = 0, startY = 0, cmd = "";
  let i = 0;
  const take = (n: number) => tokens.slice(i, (i += n)).map(Number);
  while (i < tokens.length) {
    if (/[MLHVAZ]/.test(tokens[i])) cmd = tokens[i++];
    if (cmd === "Z") { x = startX; y = startY; continue; }
    if (cmd === "M" || cmd === "L") {
      [x, y] = take(2);
      if (cmd === "M") { startX = x; startY = y; cmd = "L"; }
      points.push([x, y]);
    } else if (cmd === "H") {
      [x] = take(1); points.push([x, y]);
    } else if (cmd === "V") {
      [y] = take(1); points.push([x, y]);
    } else if (cmd === "A") {
      const [r, , , large, sweep, nx, ny] = take(7);
      points.push(...arcExtremes(x, y, r, large, sweep, nx, ny));
      x = nx; y = ny;
    }
  }
  return points;
}

function measuredBounds(g: GlyphGeometry): GlyphBounds {
  const points = [...pathPoints(g.strokePath), ...pathPoints(g.fillPath)];
  const round = (v: number) => Math.round(v * 1e6) / 1e6;
  return {
    minX: round(Math.min(...points.map((p) => p[0]))),
    minY: round(Math.min(...points.map((p) => p[1]))),
    maxX: round(Math.max(...points.map((p) => p[0]))),
    maxY: round(Math.max(...points.map((p) => p[1]))),
  };
}

const ALL_GEOMETRY: [string, GlyphGeometry][] = [
  ...Object.entries(GLYPHS), ...Object.entries(STATE_MARK_PATHS),
];

describe("GLYPHS", () => {
  it("holds one glyph per node kind, in legend order", () => {
    expect(glyphKinds()).toEqual(ALL_KINDS);
  });

  it("matches the SVG goldens exactly", () => {
    for (const kind of ALL_KINDS) {
      const glyph = GLYPHS[kind as keyof typeof GLYPHS];
      expect([glyph.strokePath, glyph.fillPath], kind).toEqual(GOLDEN[kind]);
    }
  });

  it("gives every glyph a text name, and no two glyphs the same name", () => {
    const names = Object.values(GLYPHS).map((g) => g.name);
    expect(names.every((n) => n.trim().length > 0)).toBe(true);
    expect(new Set(names).size).toBe(names.length);
  });

  it("draws no two kinds with the same geometry", () => {
    const shapes = Object.values(GLYPHS).map((g) => `${g.strokePath}|${g.fillPath}`);
    expect(new Set(shapes).size).toBe(shapes.length);
  });

  it("gives every run kind a stroked glyph of its own, drawn from the L1 zoom up", () => {
    for (const kind of RUN_KINDS) {
      const glyph = GLYPHS[kind as keyof typeof GLYPHS];
      expect(glyph.strokePath.length, kind).toBeGreaterThan(0);
      expect(glyph.minZoom, kind).toBe(GLYPH_MIN_ZOOM_RUN);
    }
  });
});

describe("path strings", () => {
  it("use only absolute M, L, H, V, A and Z commands and begin with M", () => {
    for (const [key, g] of ALL_GEOMETRY) {
      for (const d of [g.strokePath, g.fillPath].filter(Boolean)) {
        expect(d.startsWith("M"), key).toBe(true);
        expect(d.replace(/[MLHVAZ]|-?\d*\.?\d+|\s/g, ""), key).toBe("");
      }
    }
  });

  it("draw every glyph and mark something, inside the 24-unit box", () => {
    for (const [key, g] of ALL_GEOMETRY) {
      expect((g.strokePath + g.fillPath).length, key).toBeGreaterThan(0);
      const b = measuredBounds(g);
      expect(b.minX >= 0 && b.minY >= 0 && b.maxX <= GLYPH_BOX && b.maxY <= GLYPH_BOX, key).toBe(true);
    }
  });

  it("declare bounds equal to the extent their paths really reach", () => {
    for (const [key, g] of ALL_GEOMETRY) {
      expect(measuredBounds(g), key).toEqual(g.bounds);
    }
  });
});

describe("STATE_MARK_PATHS", () => {
  it("places the status dot in the top-right quarter of the box", () => {
    const b = STATE_MARK_PATHS.status_dot.bounds;
    expect(b.minX).toBeGreaterThanOrEqual(GLYPH_BOX / 2);
    expect(b.maxY).toBeLessThanOrEqual(GLYPH_BOX / 2);
  });

  it("draws the strike as one 45° slash from bottom left to top right", () => {
    expect(STATE_MARK_PATHS.strike.strokePath).toBe("M3 21L21 3");
  });
});

describe("glyphDrawnAt", () => {
  it("hides run glyphs below the L1 zoom and shows them from it", () => {
    for (const kind of RUN_KINDS) {
      expect(glyphDrawnAt(kind as keyof typeof GLYPHS, 1.59), kind).toBe(false);
      expect(glyphDrawnAt(kind as keyof typeof GLYPHS, GLYPH_MIN_ZOOM_RUN), kind).toBe(true);
    }
  });

  it("always draws the core, the task, the synapse, the artifact and the cluster", () => {
    for (const kind of ["job_core", "task", "synapse", "artifact", "cluster"] as const) {
      expect(glyphDrawnAt(kind, 0.3), kind).toBe(true);
    }
  });
});

describe("glyphTransform", () => {
  it("maps the 24-unit box onto the node's diameter, centred on the node", () => {
    expect(glyphTransform(0, 0, 12)).toEqual({ scale: 1, offsetX: -12, offsetY: -12 });
    expect(glyphTransform(100, 50, 4.5)).toEqual({ scale: 0.375, offsetX: 95.5, offsetY: 45.5 });
  });
});

describe("glyphPath2D", () => {
  const built: string[] = [];
  class RecordingPath2D {
    readonly d: string;
    constructor(d: string) {
      this.d = d;
      built.push(d);
    }
  }

  beforeAll(() => {
    vi.stubGlobal("Path2D", RecordingPath2D);
  });
  afterAll(() => {
    vi.unstubAllGlobals();
  });

  it("builds the canvas paths from the same strings the legend renders", () => {
    const artifact = glyphPath2D(GLYPHS.artifact);
    expect((artifact.stroke as unknown as RecordingPath2D).d).toBe(GLYPHS.artifact.strokePath);
    expect((artifact.fill as unknown as RecordingPath2D).d).toBe(GLYPHS.artifact.fillPath);
  });

  it("returns null for the half a glyph does not draw", () => {
    expect(glyphPath2D(GLYPHS.task).stroke).toBeNull();
    expect(glyphPath2D(GLYPHS.builder_run).fill).toBeNull();
  });

  it("builds each glyph's paths once and hands back the same objects after", () => {
    const first = glyphPath2D(GLYPHS.review_run);
    const count = built.length;
    const second = glyphPath2D(GLYPHS.review_run);
    expect(second).toBe(first);
    expect(built.length).toBe(count);
  });
});
