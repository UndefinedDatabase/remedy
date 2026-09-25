import { describe, expect, it } from "vitest";
import { STATE_MARK_PATHS } from "./glyphPaths";
import type { StateMark } from "./glyphPaths";
import { NODE_STATE_TREATMENTS, nodeStateOrder } from "./nodeStates";
import {
  BINDING_MARK_TOKENS, BINDING_STATE_MARKS, CONFORMANCE_MIN_ALPHA, CONFORMANCE_SCALE, CONFORMANCE_TOLERANCE,
  PROBE_POINTS, conformanceProbes, judgeProbe, parseCssColour, pixelShows,
} from "./glyphConformance";
import type { ConformanceProbe } from "./glyphConformance";

describe("the binding spec the harness judges against", () => {
  it("names a mark list for every state, and the state table carries exactly those marks today", () => {
    expect(Object.keys(BINDING_STATE_MARKS)).toEqual(nodeStateOrder());
    for (const state of nodeStateOrder()) {
      expect(NODE_STATE_TREATMENTS[state].marks.map((m) => m.mark), state).toEqual(BINDING_STATE_MARKS[state]);
    }
  });

  it("colours each mark as the state table does today", () => {
    for (const t of Object.values(NODE_STATE_TREATMENTS)) {
      for (const m of t.marks) {
        expect([m.token, m.outlineToken], m.mark).toEqual([BINDING_MARK_TOKENS[m.mark].mark, BINDING_MARK_TOKENS[m.mark].outline]);
      }
    }
  });
});

describe("PROBE_POINTS", () => {
  const dist = (a: [number, number], b: [number, number]) => Math.hypot(a[0] - b[0], a[1] - b[1]);

  it("probes the status dot's centre and the middle of its outline band", () => {
    expect(STATE_MARK_PATHS.status_dot.fillPath).toBe("M23 4.5A3 3 0 1 1 17 4.5A3 3 0 1 1 23 4.5Z");
    expect(dist(PROBE_POINTS.status_dot.mark, [20, 4.5])).toBe(0);
    const d = dist(PROBE_POINTS.status_dot.outline as [number, number], [20, 4.5]);
    expect(d).toBeGreaterThan(3);
    expect(d).toBeLessThan(4.5);
  });

  it("probes a point on the strike's line and the middle of the outline band beside it", () => {
    expect(STATE_MARK_PATHS.strike.strokePath).toBe("M3 21L21 3");
    const [x, y] = PROBE_POINTS.strike.mark;
    expect(x + y).toBe(24);
    expect(x).toBeGreaterThan(3);
    expect(x).toBeLessThan(21);
    const [ox, oy] = PROBE_POINTS.strike.outline as [number, number];
    const off = Math.abs(ox + oy - 24) / Math.SQRT2;
    expect(off).toBeGreaterThan(0.75);
    expect(off).toBeLessThan(1.5);
  });

  it("probes the top of the ring", () => {
    expect(STATE_MARK_PATHS.ring.strokePath).toBe("M23 12A11 11 0 1 1 1 12A11 11 0 1 1 23 12Z");
    expect(dist(PROBE_POINTS.ring.mark, [12, 12])).toBe(11);
    expect(PROBE_POINTS.ring.outline).toBeNull();
  });

  it("probes the left pause bar's centre and a point on its outline band, outside the fill", () => {
    expect(STATE_MARK_PATHS.pause.fillPath).toBe("M17 1.5H19V7.5H17ZM21 1.5H23V7.5H21Z");
    const [x, y] = PROBE_POINTS.pause.mark;
    expect(x).toBeGreaterThanOrEqual(17);
    expect(x).toBeLessThanOrEqual(19);
    expect(y).toBeGreaterThanOrEqual(1.5);
    expect(y).toBeLessThanOrEqual(7.5);
    const [ox] = PROBE_POINTS.pause.outline as [number, number];
    expect(ox).toBeLessThan(17);
    expect(ox).toBeGreaterThan(17 - 1.5);
  });
});

describe("conformanceProbes", () => {
  const probes = conformanceProbes();
  const tally = (mark: StateMark, part: string, expectation: string) =>
    probes.filter((p) => p.mark === mark && p.part === part && p.expect === expectation).length;

  it("probes every mark the spec gives, with its outline, and the absence of the dot, the strike and the pause mark everywhere else", () => {
    // 8 kinds by 8 states (DECISION F025 D3 clause 3 adds `paused`). Present: the dot on 2
    // states, the strike on 1, the ring on 2 (planned, paused), the pause mark on 1 —
    // each dot, strike and pause mark also on its outline (the ring has none). Absent:
    // the dot on 6 states, the strike on 7, the pause mark on 7.
    expect(tally("status_dot", "mark", "present")).toBe(16);
    expect(tally("status_dot", "outline", "present")).toBe(16);
    expect(tally("status_dot", "mark", "absent")).toBe(48);
    expect(tally("strike", "mark", "present")).toBe(8);
    expect(tally("strike", "outline", "present")).toBe(8);
    expect(tally("strike", "mark", "absent")).toBe(56);
    expect(tally("ring", "mark", "present")).toBe(16);
    expect(tally("pause", "mark", "present")).toBe(8);
    expect(tally("pause", "outline", "present")).toBe(8);
    expect(tally("pause", "mark", "absent")).toBe(56);
    expect(probes).toHaveLength(240);
  });

  it("marks a paused task present, with the pause mark's own token", () => {
    const mark = probes.find((p) => p.kind === "task" && p.state === "paused" && p.mark === "pause" && p.part === "mark");
    expect(mark?.expect).toBe("present");
    expect(mark?.token).toBe("--remedy-orange-400");
  });

  it("never probes for a missing ring", () => {
    expect(probes.filter((p) => p.mark === "ring" && p.expect === "absent")).toEqual([]);
  });

  it("places a probe in device pixels on the cell the painter drew, at its state's size", () => {
    // The failed task: row 0, column 5 (open, planned, paused, in_progress, pass, FAIL, ...
    // — `paused` shifted every later state's column by one), centred at (132, 12),
    // radius 7, size factor 1, so its glyph box starts at (125, 5) at 14/24 of a unit
    // per box unit.
    const dot = probes.find((p) => p.kind === "task" && p.state === "fail" && p.mark === "status_dot" && p.part === "mark");
    expect(dot?.x).toBeCloseTo((125 + 20 * (14 / 24)) * CONFORMANCE_SCALE, 9);
    expect(dot?.y).toBeCloseTo((5 + 4.5 * (14 / 24)) * CONFORMANCE_SCALE, 9);
    // The planned task, column 1, at 90% of radius 7.
    const ring = probes.find((p) => p.kind === "task" && p.state === "planned" && p.mark === "ring");
    const r = 7 * 0.9;
    expect(ring?.x).toBeCloseTo((36 - r + 12 * ((2 * r) / 24)) * CONFORMANCE_SCALE, 9);
    expect(ring?.y).toBeCloseTo((12 - r + 1 * ((2 * r) / 24)) * CONFORMANCE_SCALE, 9);
  });
});

describe("parseCssColour", () => {
  it("reads hex and the rgb function notations, and nothing else", () => {
    expect(parseCssColour(" #EF6363 ")).toEqual({ r: 239, g: 99, b: 99, a: 255 });
    expect(parseCssColour("#fff")).toEqual({ r: 255, g: 255, b: 255, a: 255 });
    expect(parseCssColour("rgb(1, 2, 3)")).toEqual({ r: 1, g: 2, b: 3, a: 255 });
    expect(parseCssColour("rgba(255, 255, 255, 0.85)")).toEqual({ r: 255, g: 255, b: 255, a: 217 });
    expect(parseCssColour("var(--remedy-state-done)")).toBeNull();
  });
});

describe("pixelShows and judgeProbe", () => {
  const red = { r: 239, g: 99, b: 99, a: 255 };

  it("counts a painted pixel within the tolerance on every channel as the colour", () => {
    expect(pixelShows(red, red)).toBe(true);
    expect(pixelShows({ ...red, g: 99 + CONFORMANCE_TOLERANCE }, red)).toBe(true);
    expect(pixelShows({ ...red, g: 99 + CONFORMANCE_TOLERANCE + 1 }, red)).toBe(false);
    expect(pixelShows({ ...red, a: CONFORMANCE_MIN_ALPHA - 1 }, red)).toBe(false);
  });

  const probe = (expectation: "present" | "absent"): ConformanceProbe => ({
    kind: "task", state: "fail", mark: "status_dot", part: "mark", expect: expectation, token: "--remedy-state-blocked", x: 0, y: 0,
  });
  const palette = { "--remedy-state-blocked": "#ef6363" };

  it("passes a present probe that shows its colour and an absent probe that does not", () => {
    expect(judgeProbe(probe("present"), red, palette).ok).toBe(true);
    expect(judgeProbe(probe("present"), { r: 52, g: 194, b: 126, a: 255 }, palette).ok).toBe(false);
    expect(judgeProbe(probe("absent"), { r: 52, g: 194, b: 126, a: 255 }, palette).ok).toBe(true);
    expect(judgeProbe(probe("absent"), red, palette).ok).toBe(false);
  });

  it("fails a probe whose token does not resolve to a colour, and says why", () => {
    const verdict = judgeProbe(probe("present"), red, {});
    expect(verdict).toEqual({ ok: false, why: "--remedy-state-blocked does not resolve to a colour" });
  });
});
