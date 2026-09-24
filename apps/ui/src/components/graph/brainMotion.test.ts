import { describe, expect, it } from "vitest";
import {
  BRAIN_BIRTH_MAX_CONCURRENT, BRAIN_BIRTH_MS, BRAIN_BIRTH_REDUCED_MS, BRAIN_BIRTH_STAGGER_MS,
  scheduleBrainBirths,
} from "./brainMotion";
import type { BrainLayoutData, BrainLayoutNode } from "./forceBrainTypes";

/** A minimal, valid BrainLayoutNode — only `id` varies across these tests;
 *  the rest of the shape is irrelevant to scheduleBrainBirths, which reads
 *  ids only. */
function node(id: string): BrainLayoutNode {
  return { id, kind: "task", state: "planned", seq: 0, depth: 1, radius: 7, x: 0, y: 0, label: "" };
}

function layout(ids: readonly string[]): BrainLayoutData {
  return { nodes: ids.map(node), links: [] };
}

describe("scheduleBrainBirths", () => {
  it("first paint (previous === null) renders at rest: no births", () => {
    expect(scheduleBrainBirths(null, layout(["a", "b", "c"]), false)).toEqual([]);
  });

  it("five new nodes stagger with at most 3 concurrent, delays hand-derived from the formula", () => {
    // delay_i = max(i * STAGGER, i >= MAX ? delay_{i-MAX} + duration : 0)
    // STAGGER = 90, MAX = 3, duration = BRAIN_BIRTH_MS = 420:
    //   i=0: max(0*90, 0)                    = max(0, 0)     = 0
    //   i=1: max(1*90, 0)                    = max(90, 0)    = 90
    //   i=2: max(2*90, 0)                    = max(180, 0)   = 180
    //   i=3: max(3*90, delay_0 + 420 = 0+420) = max(270, 420) = 420
    //   i=4: max(4*90, delay_1 + 420 = 90+420)= max(360, 510) = 510
    const births = scheduleBrainBirths(layout([]), layout(["a", "b", "c", "d", "e"]), false);
    expect(births.map((b) => b.delayMs)).toEqual([0, 90, 180, 420, 510]);
    expect(births.every((b) => b.durationMs === BRAIN_BIRTH_MS)).toBe(true);
    expect(births.every((b) => b.fade === false)).toBe(true);
  });

  it("the same five births under reduced motion use the reduced duration and its own delays", () => {
    // Same formula, duration = BRAIN_BIRTH_REDUCED_MS = 180:
    //   i=0: max(0, 0)                      = 0
    //   i=1: max(90, 0)                     = 90
    //   i=2: max(180, 0)                    = 180
    //   i=3: max(270, delay_0 + 180 = 0+180) = max(270, 180) = 270
    //   i=4: max(360, delay_1 + 180 = 90+180)= max(360, 270) = 360
    const births = scheduleBrainBirths(layout([]), layout(["a", "b", "c", "d", "e"]), true);
    expect(births.map((b) => b.delayMs)).toEqual([0, 90, 180, 270, 360]);
    expect(births.every((b) => b.durationMs === BRAIN_BIRTH_REDUCED_MS)).toBe(true);
    expect(births.every((b) => b.fade === true)).toBe(true);
  });

  it("an unchanged model births nothing", () => {
    const model = layout(["a", "b"]);
    expect(scheduleBrainBirths(model, model, false)).toEqual([]);
  });

  it("a removed node births nothing for it, and a survivor is never re-born", () => {
    const previous = layout(["a", "b", "c"]);
    const next = layout(["a", "c"]);
    expect(scheduleBrainBirths(previous, next, false)).toEqual([]);
  });

  it("births come in next's node order, not sorted or reversed", () => {
    const previous = layout(["a"]);
    const next = layout(["z", "a", "m"]);
    const births = scheduleBrainBirths(previous, next, false);
    expect(births.map((b) => b.id)).toEqual(["z", "m"]);
  });

  it("mixes new and surviving nodes: only the new ones birth, at their own position in next's order", () => {
    const previous = layout(["a", "b"]);
    const next = layout(["a", "c", "b", "d"]);
    const births = scheduleBrainBirths(previous, next, false);
    expect(births.map((b) => b.id)).toEqual(["c", "d"]);
    expect(births.map((b) => b.delayMs)).toEqual([0, 90]);
  });

  it("re-exports the constants graph_spec §11 and §12 name", () => {
    expect(BRAIN_BIRTH_STAGGER_MS).toBe(90);
    expect(BRAIN_BIRTH_MAX_CONCURRENT).toBe(3);
    expect(BRAIN_BIRTH_MS).toBe(420);
    expect(BRAIN_BIRTH_REDUCED_MS).toBe(180);
  });
});
