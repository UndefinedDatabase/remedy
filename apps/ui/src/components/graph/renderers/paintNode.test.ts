import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";
import type { NodeKind, NodeState } from "../brainOntology";
import { GLYPHS, GLYPH_MIN_ZOOM_RUN, STATE_MARK_PATHS } from "./glyphPaths";
import { NODE_STATE_TREATMENTS } from "./nodeStates";
import {
  CLUSTER_COUNT_SIZE, GLYPH_STROKE_WIDTH, HALO_SPREAD, RIPPLE_WIDTH, SPHERE_KINDS, paintBrainNode, paintBrainNodeInMotion,
} from "./paintNode";
import type { NodeMotion } from "./paintNode";
import type { PaintableNode } from "./paintNode";
import { brainPaletteTokens } from "./palette";
import type { BrainPalette } from "./palette";

/** A Path2D stand-in that remembers the string it was built from, so a drawn
 *  path can be traced back to the glyph or mark it came from. */
class RecordingPath2D {
  constructor(readonly d: string) {}
}

/** One recorded canvas operation with the paint state in force when it ran. */
interface Op {
  op: string;
  d?: string;
  radius?: number;
  text?: string;
  at?: [number, number];
  font?: string;
  fillStyle: unknown;
  strokeStyle: unknown;
  lineWidth: number;
  globalAlpha: number;
}

/** A 2D context that records every drawing call and the colours, alpha and
 *  width in force at that moment; save/restore keep a real state stack. */
class RecordingContext {
  ops: Op[] = [];
  fillStyle: unknown = "";
  strokeStyle: unknown = "";
  lineWidth = 1;
  globalAlpha = 1;
  lineCap = "butt";
  lineJoin = "miter";
  font = "";
  textAlign = "start";
  textBaseline = "alphabetic";
  private stack: [unknown, unknown, number, number][] = [];
  private lastArc = 0;

  private record(op: string, extra: Partial<Op> = {}): void {
    this.ops.push({
      op, fillStyle: this.fillStyle, strokeStyle: this.strokeStyle,
      lineWidth: this.lineWidth, globalAlpha: this.globalAlpha, ...extra,
    });
  }

  save(): void { this.stack.push([this.fillStyle, this.strokeStyle, this.lineWidth, this.globalAlpha]); }
  restore(): void {
    const top = this.stack.pop();
    if (top) [this.fillStyle, this.strokeStyle, this.lineWidth, this.globalAlpha] = top;
  }
  beginPath(): void {}
  translate(): void {}
  scale(): void {}
  arc(_x: number, _y: number, r: number): void { this.lastArc = r; }
  createRadialGradient(): { stops: [number, string][]; addColorStop: (o: number, c: string) => void } {
    const gradient = { stops: [] as [number, string][], addColorStop(o: number, c: string) { gradient.stops.push([o, c]); } };
    return gradient;
  }
  fill(path?: RecordingPath2D): void {
    this.record("fill", path ? { d: path.d } : { radius: this.lastArc });
  }
  stroke(path?: RecordingPath2D): void {
    this.record("stroke", path ? { d: path.d } : { radius: this.lastArc });
  }
  fillText(text: string, x: number, y: number): void {
    this.record("text", { text, at: [x, y], font: `${this.font}|${this.textAlign}|${this.textBaseline}` });
  }
}

/** Each token resolves to its own name behind a marker, so every colour the
 *  painter sets can be traced back to the token it came from. */
const PALETTE: BrainPalette = Object.fromEntries(brainPaletteTokens().map((t) => [t, `c(${t})`]));
const c = (token: string) => `c(${token})`;

function paint(
  kind: NodeKind, state: NodeState, zoom = 1, extra: { alpha?: number; scale?: number; label?: string; radius?: number } = {},
): Op[] {
  const ctx = new RecordingContext();
  const node: PaintableNode = { kind, state, x: 10, y: 20, radius: extra.radius ?? 4.5, label: extra.label };
  paintBrainNode(ctx as unknown as CanvasRenderingContext2D, node, {
    palette: PALETTE, zoom, alpha: extra.alpha ?? 1, scale: extra.scale ?? 1,
  });
  return ctx.ops;
}

const pathOps = (ops: Op[], d: string) => ops.filter((o) => o.d === d);

beforeAll(() => {
  vi.stubGlobal("Path2D", RecordingPath2D);
});
afterAll(() => {
  vi.unstubAllGlobals();
});

describe("paintBrainNode — colours", () => {
  it("sets no colour that is not a resolved palette token", () => {
    const allowed = new Set(Object.values(PALETTE));
    for (const kind of Object.keys(GLYPHS).filter((k) => k !== "job_core") as NodeKind[]) {
      for (const state of Object.keys(NODE_STATE_TREATMENTS) as NodeState[]) {
        for (const op of paint(kind, state, 2)) {
          const colour = op.op === "stroke" ? op.strokeStyle : op.fillStyle;
          const colours = typeof colour === "string" ? [colour]
            : (colour as { stops: [number, string][] }).stops.map((s) => s[1]);
          for (const value of colours) expect(allowed.has(value), `${kind}/${state}: ${value}`).toBe(true);
        }
      }
    }
  });

  it("glosses a sphere from the highlight into the state's fill", () => {
    const sphere = paint("task", "pass").find((o) => o.op === "fill" && o.radius === 4.5);
    expect((sphere?.fillStyle as { stops: [number, string][] }).stops).toEqual([
      [0, c("--remedy-graph-node-ring")], [0.35, c("--remedy-state-done")], [1, c("--remedy-state-done")],
    ]);
  });
});

describe("paintBrainNode — halo, size and birth", () => {
  it("draws a halo past the edge at the state's halo alpha", () => {
    const halo = paint("builder_run", "in_progress").find((o) => o.op === "fill" && o.radius === 4.5 + HALO_SPREAD);
    expect(halo?.fillStyle).toBe(c("--remedy-state-current"));
    expect(halo?.globalAlpha).toBeCloseTo(0.4, 10);
  });

  it("draws a planned node at 90% of its radius with no halo", () => {
    const fills = paint("task", "planned").filter((o) => o.op === "fill" && o.radius !== undefined);
    expect(fills.map((o) => o.radius)).toEqual([4.5 * 0.9]);
  });

  it("scales the radius and the alpha by the birth in flight", () => {
    const ops = paint("task", "pass", 1, { alpha: 0.5, scale: 0.5 });
    const sphere = ops.filter((o) => o.op === "fill" && o.radius !== undefined).pop();
    expect(sphere?.radius).toBe(2.25);
    expect(sphere?.globalAlpha).toBe(0.5);
  });
});

describe("paintBrainNode — glyphs", () => {
  it("draws a run's glyph only from the L1 zoom, in the state's ink", () => {
    for (const kind of ["builder_run", "review_run", "repair_run", "test_run"] as NodeKind[]) {
      const d = GLYPHS[kind].strokePath;
      expect(pathOps(paint(kind, "pass", GLYPH_MIN_ZOOM_RUN - 0.01), d), kind).toEqual([]);
      const drawn = pathOps(paint(kind, "pass", GLYPH_MIN_ZOOM_RUN), d);
      expect(drawn.map((o) => [o.op, o.strokeStyle, o.lineWidth]), kind)
        .toEqual([["stroke", c("--remedy-graph-node-ring"), GLYPH_STROKE_WIDTH]]);
    }
  });

  it("inks a planned run's glyph in the ring colour, so it shows on the white sphere", () => {
    const drawn = pathOps(paint("test_run", "planned", GLYPH_MIN_ZOOM_RUN), GLYPHS.test_run.strokePath);
    expect(drawn.map((o) => o.strokeStyle)).toEqual([c("--remedy-state-planned-ring")]);
  });

  it("fills a planned artifact white and lines it in the ring colour", () => {
    const ops = paint("artifact", "planned");
    expect(pathOps(ops, GLYPHS.artifact.fillPath).map((o) => o.fillStyle)).toEqual([c("--remedy-state-planned")]);
    expect(pathOps(ops, GLYPHS.artifact.strokePath).map((o) => o.strokeStyle)).toEqual([c("--remedy-state-planned-ring")]);
  });

  it("draws a sphere for exactly the task and run kinds", () => {
    expect([...SPHERE_KINDS].sort()).toEqual(["builder_run", "repair_run", "review_run", "task", "test_run"]);
  });

  it("draws the artifact, synapse and cluster from their glyph in the state's colour, with no sphere", () => {
    for (const kind of ["artifact", "synapse", "cluster"] as NodeKind[]) {
      const ops = paint(kind, "in_progress", 0.5);
      expect(ops.some((o) => o.radius !== undefined), kind).toBe(false);
      const glyph = GLYPHS[kind];
      for (const d of [glyph.fillPath, glyph.strokePath].filter(Boolean)) {
        const drawn = pathOps(ops, d);
        expect(drawn.length, `${kind}:${d}`).toBe(1);
        const colour = drawn[0].op === "fill" ? drawn[0].fillStyle : drawn[0].strokeStyle;
        expect(colour, kind).toBe(c("--remedy-state-current"));
      }
    }
  });
});

describe("paintBrainNode — state is never colour alone", () => {
  it("puts an outlined status dot on a failed and on a blocked node", () => {
    for (const state of ["fail", "blocked"] as NodeState[]) {
      const dot = pathOps(paint("test_run", state), STATE_MARK_PATHS.status_dot.fillPath);
      expect(dot.map((o) => [o.op, o.op === "fill" ? o.fillStyle : o.strokeStyle]), state).toEqual([
        ["stroke", c("--remedy-graph-node-ring")],
        ["fill", c("--remedy-state-blocked")],
      ]);
    }
  });

  it("strikes a vetoed node in its grey over a wider outline", () => {
    const strike = pathOps(paint("task", "vetoed"), STATE_MARK_PATHS.strike.strokePath);
    expect(strike.map((o) => [o.strokeStyle, o.lineWidth])).toEqual([
      [c("--remedy-graph-node-ring"), GLYPH_STROKE_WIDTH * 2],
      [c("--remedy-state-vetoed"), GLYPH_STROKE_WIDTH],
    ]);
  });

  it("rings a planned node in the planned ring colour", () => {
    const ring = pathOps(paint("task", "planned"), STATE_MARK_PATHS.ring.strokePath);
    expect(ring.map((o) => o.strokeStyle)).toEqual([c("--remedy-state-planned-ring")]);
  });

  it("draws no mark on a state that carries none", () => {
    const markPaths = Object.values(STATE_MARK_PATHS).flatMap((g) => [g.fillPath, g.strokePath]).filter(Boolean);
    for (const state of ["open", "in_progress", "pass"] as NodeState[]) {
      const ops = paint("task", state);
      expect(ops.filter((o) => o.d !== undefined && markPaths.includes(o.d)), state).toEqual([]);
    }
  });
});

describe("paintBrainNode — the cluster's count", () => {
  it("writes a cluster's count at its centre, in the state's line colour and the resolved font", () => {
    const text = paint("cluster", "planned", 1, { label: "+5", radius: 9 }).filter((o) => o.op === "text");
    expect(text.map((o) => [o.text, o.at, o.fillStyle, o.font])).toEqual([
      ["+5", [10, 20], c("--remedy-state-planned-ring"),
        `600 ${9 * 0.9 * CLUSTER_COUNT_SIZE}px ${c("--remedy-font-ui")}|center|middle`],
    ]);
  });

  it("writes nothing for a cluster with no count, or for a label on any other kind", () => {
    expect(paint("cluster", "pass", 1, { label: "" }).filter((o) => o.op === "text")).toEqual([]);
    expect(paint("task", "pass", 1, { label: "Fix the flaky test" }).filter((o) => o.op === "text")).toEqual([]);
  });
});

describe("paintBrainNodeInMotion", () => {
  function paintMoving(state: NodeState, motion: NodeMotion): Op[] {
    const ctx = new RecordingContext();
    paintBrainNodeInMotion(ctx as unknown as CanvasRenderingContext2D, { kind: "task", state, x: 10, y: 20, radius: 4.5 }, {
      palette: PALETTE, zoom: 1, alpha: 1, scale: 1,
    }, motion);
    return ctx.ops;
  }
  const spheres = (ops: Op[]) => ops.filter((o) => o.op === "fill" && typeof o.fillStyle === "object");
  const stopOf = (o: Op) => (o.fillStyle as { stops: [number, string][] }).stops[1][1];

  it("paints a node at rest once, at its pulse multiplier", () => {
    const ops = paintMoving("in_progress", { fromState: null, transition: null, pulseScale: 1.08 });
    expect(spheres(ops).map((o) => [o.radius, o.globalAlpha])).toEqual([[4.5 * 1.08, 1]]);
  });

  it("crossfades the old state out under the new one while a change runs", () => {
    const ops = paintMoving("pass", {
      fromState: "in_progress", transition: { fromAlpha: 0.25, toAlpha: 0.75, ripple: null, done: false }, pulseScale: 1,
    });
    expect(spheres(ops).map((o) => [stopOf(o), o.globalAlpha])).toEqual([
      [c("--remedy-state-current"), 0.25],
      [c("--remedy-state-done"), 0.75],
    ]);
  });

  it("rings the node in the highlight as the ripple leaves its edge", () => {
    const ops = paintMoving("pass", {
      fromState: "in_progress", transition: { fromAlpha: 0.5, toAlpha: 0.5, ripple: { spread: 7, alpha: 0.5 }, done: false },
      pulseScale: 1,
    });
    const ring = ops.filter((o) => o.op === "stroke" && o.radius === 4.5 + 7);
    expect(ring.map((o) => [o.strokeStyle, o.lineWidth, o.globalAlpha])).toEqual([[c("--remedy-graph-node-ring"), RIPPLE_WIDTH, 0.5]]);
  });

  it("paints a finished change once, in its new state", () => {
    const ops = paintMoving("pass", {
      fromState: "in_progress", transition: { fromAlpha: 0, toAlpha: 1, ripple: null, done: true }, pulseScale: 1,
    });
    expect(spheres(ops).map(stopOf)).toEqual([c("--remedy-state-done")]);
  });
});
