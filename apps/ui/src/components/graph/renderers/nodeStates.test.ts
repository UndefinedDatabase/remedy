import { describe, expect, it } from "vitest";
import { STATE_MARK_PATHS } from "./glyphPaths";
import {
  NODE_PULSE_AMPLITUDE, NODE_PULSE_MS, NODE_STATE_TREATMENTS,
  nodeScaleAt, nodeStateOrder, nodeStateTokens,
} from "./nodeStates";

/** Every NodeState brainOntology.ts declares, in the legend order the module
 *  must keep. Written out here so a state dropped from the table fails. */
const ALL_STATES = ["open", "planned", "in_progress", "pass", "fail", "blocked", "vetoed"];

/** The fill token each state is painted with (T5_F020.md's binding spec, as
 *  token names; the Python guard checks the values those tokens carry). */
const FILL_TOKENS: Record<string, string> = {
  open: "--remedy-state-open",
  planned: "--remedy-state-planned",
  in_progress: "--remedy-state-current",
  pass: "--remedy-state-done",
  fail: "--remedy-state-blocked",
  blocked: "--remedy-state-blocked",
  vetoed: "--remedy-state-vetoed",
};

type State = keyof typeof NODE_STATE_TREATMENTS;
const treatment = (state: string) => NODE_STATE_TREATMENTS[state as State];
const marksOf = (state: string) => treatment(state).marks.map((m) => m.mark);

describe("NODE_STATE_TREATMENTS", () => {
  it("holds one treatment per node state, in legend order", () => {
    expect(nodeStateOrder()).toEqual(ALL_STATES);
  });

  it("paints each state with the fill token the spec fixes", () => {
    for (const state of ALL_STATES) {
      expect(treatment(state).fillToken, state).toBe(FILL_TOKENS[state]);
    }
  });

  it("names only design tokens, and lists each one once", () => {
    const tokens = nodeStateTokens();
    expect(tokens.every((t) => /^--remedy-[a-z0-9-]+$/.test(t))).toBe(true);
    expect(new Set(tokens).size).toBe(tokens.length);
    expect([...tokens].sort()).toEqual([
      "--remedy-graph-node-ring",
      "--remedy-state-blocked",
      "--remedy-state-current",
      "--remedy-state-done",
      "--remedy-state-open",
      "--remedy-state-planned",
      "--remedy-state-planned-ring",
      "--remedy-state-vetoed",
    ]);
  });

  it("gives every state a text name, and no two states the same name", () => {
    const names = ALL_STATES.map((s) => treatment(s).name);
    expect(names.every((n) => n.trim().length > 0)).toBe(true);
    expect(new Set(names).size).toBe(names.length);
  });

  it("uses only marks glyphPaths.ts draws", () => {
    for (const state of ALL_STATES) {
      for (const mark of marksOf(state)) expect(mark in STATE_MARK_PATHS, `${state}:${mark}`).toBe(true);
    }
  });
});

describe("glyph ink and body lines", () => {
  it("strokes a glyph on every state's sphere in a colour other than its fill", () => {
    for (const state of ALL_STATES) {
      expect(treatment(state).inkToken, state).not.toBe(treatment(state).fillToken);
    }
  });

  it("inks a planned node's glyph and lines in its ring colour, and every other state's glyph in white", () => {
    expect(treatment("planned").inkToken).toBe("--remedy-state-planned-ring");
    expect(treatment("planned").lineToken).toBe("--remedy-state-planned-ring");
    for (const state of ALL_STATES.filter((s) => s !== "planned")) {
      expect(treatment(state).inkToken, state).toBe("--remedy-graph-node-ring");
      expect(treatment(state).lineToken, state).toBe(FILL_TOKENS[state]);
    }
  });
});

describe("state is never colour alone", () => {
  it("marks a failed and a blocked node with the status dot", () => {
    expect(marksOf("fail")).toEqual(["status_dot"]);
    expect(marksOf("blocked")).toEqual(["status_dot"]);
  });

  it("marks a vetoed node with the strike and dims what hangs below it to 40%", () => {
    expect(marksOf("vetoed")).toEqual(["strike"]);
    expect(treatment("vetoed").downstreamAlpha).toBe(0.4);
  });

  it("draws a planned node at 90% size with its ring", () => {
    expect(treatment("planned").sizeFactor).toBe(0.9);
    expect(marksOf("planned")).toEqual(["ring"]);
  });

  it("outlines the status dot and the strike, so each stands off the node beneath it", () => {
    for (const state of ["fail", "blocked", "vetoed"]) {
      expect(treatment(state).marks[0].outlineToken, state).toBe("--remedy-graph-node-ring");
    }
  });

  it("draws only failed and blocked alike, as graph_spec §5's one blocked/failed row does", () => {
    const look = (s: string) => JSON.stringify({ ...treatment(s), name: "" });
    const pairs: string[] = [];
    ALL_STATES.forEach((a, i) => ALL_STATES.slice(i + 1).forEach((b) => {
      if (look(a) === look(b)) pairs.push(`${a}=${b}`);
    }));
    expect(pairs).toEqual(["fail=blocked"]);
  });
});

describe("branch glow and pulse", () => {
  it("pulses only the in-progress state", () => {
    expect(ALL_STATES.filter((s) => treatment(s).pulse)).toEqual(["in_progress"]);
  });

  it("asks full glow of an active branch, 25% of a done one, and none of the rest", () => {
    const glow = Object.fromEntries(ALL_STATES.map((s) => [s, treatment(s).branchGlowAlpha]));
    expect(glow).toEqual({ open: 0, planned: 0, in_progress: 1, pass: 0.25, fail: 0, blocked: 0, vetoed: 0 });
  });
});

describe("nodeScaleAt", () => {
  it("swings an in-progress node ±8% over one pulse period", () => {
    expect(NODE_PULSE_MS).toBe(1600);
    expect(NODE_PULSE_AMPLITUDE).toBe(0.08);
    expect(nodeScaleAt("in_progress", 0, false)).toBeCloseTo(1, 10);
    expect(nodeScaleAt("in_progress", NODE_PULSE_MS / 4, false)).toBeCloseTo(1.08, 10);
    expect(nodeScaleAt("in_progress", (3 * NODE_PULSE_MS) / 4, false)).toBeCloseTo(0.92, 10);
    expect(nodeScaleAt("in_progress", NODE_PULSE_MS, false)).toBeCloseTo(1, 10);
  });

  it("holds every node still under reduced motion", () => {
    expect(nodeScaleAt("in_progress", NODE_PULSE_MS / 4, true)).toBe(1);
  });

  it("draws a still state at its size factor whatever the time", () => {
    expect(nodeScaleAt("planned", NODE_PULSE_MS / 4, false)).toBe(0.9);
    expect(nodeScaleAt("pass", 123, false)).toBe(1);
  });
});
