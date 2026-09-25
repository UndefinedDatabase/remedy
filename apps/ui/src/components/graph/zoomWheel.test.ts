import { describe, expect, it } from "vitest";
import { GOLDEN_B_MODEL } from "./brainReducer.fixtures";
import { GLYPH_MIN_ZOOM_RUN } from "./renderers/glyphPaths";
import { ZOOM_HOME, zoomGraphOf, zoomTransition, type ZoomState } from "./semanticZoom";
import { ZOOM_IN_ABOVE, ZOOM_OUT_BELOW, wheelCrossing, wheelZoomEvent } from "./zoomWheel";

describe("the thresholds", () => {
  it("are graph_spec §10's: in above 1.6, out below 0.8", () => {
    expect([ZOOM_IN_ABOVE, ZOOM_OUT_BELOW]).toEqual([1.6, 0.8]);
  });

  it("the wheel enters L1 at the very factor from which run glyphs are drawn", () => {
    expect(ZOOM_IN_ABOVE).toBe(GLYPH_MIN_ZOOM_RUN);
  });
});

describe("wheelCrossing — both sides of each boundary", () => {
  it.each([
    [1.0, 1.6, null, "reaching 1.6 is not above it"],
    [1.6, 1.6000001, "in", "just above 1.6 crosses"],
    [1.5, 2.0, "in", "a step across 1.6 crosses"],
    [1.61, 1.7, null, "already above 1.6 crosses nothing"],
    [1.7, 1.5, null, "falling back under 1.6 does not walk out"],
    [1.0, 0.8, null, "reaching 0.8 is not below it"],
    [0.8, 0.7999999, "out", "just below 0.8 crosses"],
    [1.2, 0.5, "out", "a step across 0.8 crosses"],
    [0.79, 0.7, null, "already below 0.8 crosses nothing"],
    [0.7, 0.9, null, "rising back over 0.8 does not zoom in"],
    [0.5, 2.0, "in", "one step over the whole dead band crosses in"],
    [2.0, 0.5, "out", "one step under the whole dead band crosses out"],
    [1.2, 1.2, null, "no movement"],
  ] as const)("%f → %f is %s (%s)", (previous, next, expected, _why) => {
    expect(wheelCrossing(previous, next)).toBe(expected);
  });
});

describe("wheelZoomEvent", () => {
  it("a crossing in needs a node under the pointer", () => {
    expect(wheelZoomEvent(1.0, 1.7, null)).toBeNull();
    expect(wheelZoomEvent(1.0, 1.7, "task:t1")).toEqual({ type: "zoom_in", nodeId: "task:t1" });
  });

  it("a crossing out needs none, and no crossing is no event", () => {
    expect(wheelZoomEvent(1.0, 0.7, null)).toEqual({ type: "zoom_out" });
    expect(wheelZoomEvent(1.0, 0.7, "task:t1")).toEqual({ type: "zoom_out" });
    expect(wheelZoomEvent(1.0, 1.2, "task:t1")).toBeNull();
  });
});

describe("hysteresis through the machine", () => {
  it("a zoom wobbling around either threshold never flickers the level", () => {
    const graph = zoomGraphOf(GOLDEN_B_MODEL.nodes);
    const trace = [1.0, 1.7, 1.5, 1.7, 1.59, 0.9, 0.79, 1.0, 0.81, 1.61];
    const levels: number[] = [];
    let state: ZoomState = ZOOM_HOME;
    for (let i = 1; i < trace.length; i += 1) {
      const event = wheelZoomEvent(trace[i - 1], trace[i], "task:t1");
      if (event) state = zoomTransition(graph, state, event).state;
      levels.push(state.level);
    }
    expect(levels).toEqual([1, 1, 1, 1, 1, 0, 0, 0, 1]);
  });
});
