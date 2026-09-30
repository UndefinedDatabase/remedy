// F044 T002 — the graph's keys (DECISION F044 D6): which node a key picks, or whether it walks back.
import { describe, expect, it } from "vitest";
import { zoomGraphOf } from "./semanticZoom";
import type { NodeKind } from "./brainOntology";
import type { ZoomState } from "./semanticZoom";
import { zoomKeyStep } from "./zoomKeys";

function node(id: string, kind: NodeKind, parentId?: string) {
  return { id, kind, parentId };
}

// Runs of task a sit on both sides of task b, so a sibling walk must follow the parent, not the
// order of the map alone.
const GRAPH = zoomGraphOf([
  node("core", "job_core"),
  node("task:a", "task", "core"),
  node("run:a:1", "builder_run", "task:a"),
  node("task:b", "task", "core"),
  node("run:a:2", "review_run", "task:a"),
  node("run:b:1", "builder_run", "task:b"),
  node("task:c", "task", "core"),
]);

const HOME: ZoomState = { level: 0, focusId: null, tab: null };
const at = (level: 0 | 1 | 2 | 3, focusId: string): ZoomState => ({ level, focusId, tab: level === 3 ? "diff" : null });

describe("zoomKeyStep, walking the siblings", () => {
  it("enters the tasks from the job at the first going forward and the last going back", () => {
    expect(zoomKeyStep(GRAPH, HOME, "next-sibling")).toEqual({ kind: "pick", nodeId: "task:a" });
    expect(zoomKeyStep(GRAPH, HOME, "previous-sibling")).toEqual({ kind: "pick", nodeId: "task:c" });
  });

  it("steps between tasks in the graph's order and wraps at either end", () => {
    expect(zoomKeyStep(GRAPH, at(1, "task:b"), "next-sibling")).toEqual({ kind: "pick", nodeId: "task:c" });
    expect(zoomKeyStep(GRAPH, at(1, "task:b"), "previous-sibling")).toEqual({ kind: "pick", nodeId: "task:a" });
    expect(zoomKeyStep(GRAPH, at(1, "task:c"), "next-sibling")).toEqual({ kind: "pick", nodeId: "task:a" });
    expect(zoomKeyStep(GRAPH, at(1, "task:a"), "previous-sibling")).toEqual({ kind: "pick", nodeId: "task:c" });
  });

  it("starts from the first task when the focus is not among the tasks", () => {
    expect(zoomKeyStep(GRAPH, at(1, "task:gone"), "next-sibling")).toEqual({ kind: "pick", nodeId: "task:a" });
  });

  it("steps between the runs of the focused run's own task, at a run and at its evidence", () => {
    expect(zoomKeyStep(GRAPH, at(2, "run:a:1"), "next-sibling")).toEqual({ kind: "pick", nodeId: "run:a:2" });
    expect(zoomKeyStep(GRAPH, at(2, "run:a:2"), "next-sibling")).toEqual({ kind: "pick", nodeId: "run:a:1" });
    expect(zoomKeyStep(GRAPH, at(3, "run:a:1"), "previous-sibling")).toEqual({ kind: "pick", nodeId: "run:a:2" });
    expect(zoomKeyStep(GRAPH, at(2, "run:b:1"), "next-sibling")).toEqual({ kind: "pick", nodeId: "run:b:1" });
  });

  it("picks nothing where there is nothing to walk", () => {
    expect(zoomKeyStep(zoomGraphOf([]), HOME, "next-sibling")).toBeNull();
    expect(zoomKeyStep(GRAPH, at(2, "run:gone:1"), "next-sibling")).toBeNull();
  });
});

describe("zoomKeyStep, zooming in and walking back", () => {
  it("zooms from a task into its first run, and nowhere else", () => {
    expect(zoomKeyStep(GRAPH, at(1, "task:a"), "zoom-in")).toEqual({ kind: "pick", nodeId: "run:a:1" });
    expect(zoomKeyStep(GRAPH, at(1, "task:c"), "zoom-in")).toBeNull();
    expect(zoomKeyStep(GRAPH, HOME, "zoom-in")).toBeNull();
    expect(zoomKeyStep(GRAPH, at(2, "run:a:1"), "zoom-in")).toBeNull();
  });

  it("walks back from every level", () => {
    for (const state of [HOME, at(1, "task:a"), at(2, "run:a:1"), at(3, "run:a:1")]) {
      expect(zoomKeyStep(GRAPH, state, "walk-back")).toEqual({ kind: "walk-back" });
    }
  });

  it("asks nothing of the zoom for the bar, the terms or the projects", () => {
    for (const action of ["open-bar", "open-terms", "go-projects"] as const) {
      expect(zoomKeyStep(GRAPH, at(1, "task:a"), action)).toBeNull();
    }
  });
});
