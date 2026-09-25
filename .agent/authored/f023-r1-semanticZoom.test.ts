import { describe, expect, it } from "vitest";
import { clusterBrainModel } from "./brainReducer";
import { CLUSTER_INPUT_MODEL, GOLDEN_B_MODEL } from "./brainReducer.fixtures";
import {
  ZOOM_HOME, zoomBreadcrumbs, zoomGraphOf, zoomTransition,
  type ZoomEvent, type ZoomGraph, type ZoomState,
} from "./semanticZoom";

// Every expected state and note below is HAND-DERIVED from graph_spec.md §10
// and DECISION F023 D1, never computed by the machine: a golden computed by
// the code under test could not catch that code being wrong. The graph is
// Golden B of the reducer's fixtures: job-b, tasks t1 and t2, t1's runs at
// seq 1, 2, 3, 5 and 6, and t2's open builder run at seq 8.
const GRAPH: ZoomGraph = zoomGraphOf(GOLDEN_B_MODEL.nodes);

const H: ZoomState = ZOOM_HOME;
const T1: ZoomState = { level: 1, focusId: "task:t1", tab: null };
const T2: ZoomState = { level: 1, focusId: "task:t2", tab: null };
const R2: ZoomState = { level: 2, focusId: "run:t1:2", tab: null };
const R8: ZoomState = { level: 2, focusId: "run:t2:8", tab: null };
const E2D: ZoomState = { level: 3, focusId: "run:t1:2", tab: "diff" };
const E2P: ZoomState = { level: 3, focusId: "run:t1:2", tab: "prompt" };

const MISSING_TASK = "focus target task:nope is not in the graph";
const MISSING_RUN = "focus target run:nope:1 is not in the graph";
const ONLY_BACK = "a breadcrumb only walks back";
const FROM_RUN = "evidence opens from a run's detail";
const WHEEL_STAYS = "the wheel does not leave run detail; Escape walks back";

const EVENTS: Record<string, ZoomEvent> = {
  "click core": { type: "click", nodeId: "job:job-b" },
  "click task t1": { type: "click", nodeId: "task:t1" },
  "click task t2": { type: "click", nodeId: "task:t2" },
  "click run t1:2": { type: "click", nodeId: "run:t1:2" },
  "click run t2:8": { type: "click", nodeId: "run:t2:8" },
  "click unknown": { type: "click", nodeId: "task:nope" },
  "wheel in on task t2": { type: "zoom_in", nodeId: "task:t2" },
  "wheel in on run t1:5": { type: "zoom_in", nodeId: "run:t1:5" },
  "wheel in on core": { type: "zoom_in", nodeId: "job:job-b" },
  "wheel in on unknown": { type: "zoom_in", nodeId: "run:nope:1" },
  "wheel out": { type: "zoom_out" },
  escape: { type: "escape" },
  "crumb job": { type: "crumb", level: 0 },
  "crumb task": { type: "crumb", level: 1 },
  "crumb run": { type: "crumb", level: 2 },
  "open diff": { type: "open_evidence", tab: "diff" },
  "open prompt": { type: "open_evidence", tab: "prompt" },
  reconcile: { type: "reconcile" },
};

// [start, event, expected state, expected note]; `same` marks a transition
// that must hand back the very state object it was given.
type Row = [string, ZoomState, keyof typeof EVENTS, ZoomState | "same", string | null];

const MATRIX: Row[] = [
  ["L0", H, "click core", "same", null],
  ["L0", H, "click task t1", T1, null],
  ["L0", H, "click task t2", T2, null],
  ["L0", H, "click run t1:2", R2, null],
  ["L0", H, "click run t2:8", R8, null],
  ["L0", H, "click unknown", "same", MISSING_TASK],
  ["L0", H, "wheel in on task t2", T2, null],
  ["L0", H, "wheel in on run t1:5", T1, null],
  ["L0", H, "wheel in on core", "same", null],
  ["L0", H, "wheel in on unknown", "same", MISSING_RUN],
  ["L0", H, "wheel out", "same", null],
  ["L0", H, "escape", "same", null],
  ["L0", H, "crumb job", "same", null],
  ["L0", H, "crumb task", "same", ONLY_BACK],
  ["L0", H, "crumb run", "same", ONLY_BACK],
  ["L0", H, "open diff", "same", FROM_RUN],
  ["L0", H, "open prompt", "same", FROM_RUN],
  ["L0", H, "reconcile", "same", null],

  ["L1", T1, "click core", H, null],
  ["L1", T1, "click task t1", "same", null],
  ["L1", T1, "click task t2", T2, null],
  ["L1", T1, "click run t1:2", R2, null],
  ["L1", T1, "click run t2:8", R8, null],
  ["L1", T1, "click unknown", "same", MISSING_TASK],
  ["L1", T1, "wheel in on task t2", T2, null],
  ["L1", T1, "wheel in on run t1:5", "same", null],
  ["L1", T1, "wheel in on core", "same", null],
  ["L1", T1, "wheel in on unknown", "same", MISSING_RUN],
  ["L1", T1, "wheel out", H, null],
  ["L1", T1, "escape", H, null],
  ["L1", T1, "crumb job", H, null],
  ["L1", T1, "crumb task", "same", null],
  ["L1", T1, "crumb run", "same", ONLY_BACK],
  ["L1", T1, "open diff", "same", FROM_RUN],
  ["L1", T1, "open prompt", "same", FROM_RUN],
  ["L1", T1, "reconcile", "same", null],

  ["L2", R2, "click core", H, null],
  ["L2", R2, "click task t1", T1, null],
  ["L2", R2, "click task t2", T2, null],
  ["L2", R2, "click run t1:2", "same", null],
  ["L2", R2, "click run t2:8", R8, null],
  ["L2", R2, "click unknown", "same", MISSING_TASK],
  ["L2", R2, "wheel in on task t2", "same", WHEEL_STAYS],
  ["L2", R2, "wheel in on run t1:5", "same", WHEEL_STAYS],
  ["L2", R2, "wheel in on core", "same", WHEEL_STAYS],
  ["L2", R2, "wheel in on unknown", "same", WHEEL_STAYS],
  ["L2", R2, "wheel out", H, null],
  ["L2", R2, "escape", T1, null],
  ["L2", R2, "crumb job", H, null],
  ["L2", R2, "crumb task", T1, null],
  ["L2", R2, "crumb run", "same", null],
  ["L2", R2, "open diff", E2D, null],
  ["L2", R2, "open prompt", E2P, null],
  ["L2", R2, "reconcile", "same", null],

  ["L3", E2D, "click core", H, null],
  ["L3", E2D, "click task t1", T1, null],
  ["L3", E2D, "click task t2", T2, null],
  ["L3", E2D, "click run t1:2", R2, null],
  ["L3", E2D, "click run t2:8", R8, null],
  ["L3", E2D, "click unknown", "same", MISSING_TASK],
  ["L3", E2D, "wheel in on task t2", "same", WHEEL_STAYS],
  ["L3", E2D, "wheel in on run t1:5", "same", WHEEL_STAYS],
  ["L3", E2D, "wheel in on core", "same", WHEEL_STAYS],
  ["L3", E2D, "wheel in on unknown", "same", WHEEL_STAYS],
  ["L3", E2D, "wheel out", H, null],
  ["L3", E2D, "escape", R2, null],
  ["L3", E2D, "crumb job", H, null],
  ["L3", E2D, "crumb task", T1, null],
  ["L3", E2D, "crumb run", R2, null],
  ["L3", E2D, "open diff", "same", null],
  ["L3", E2D, "open prompt", E2P, null],
  ["L3", E2D, "reconcile", "same", null],
];

describe("zoomTransition — the whole matrix, every start level by every event", () => {
  it("covers each of the four levels with every event exactly once", () => {
    for (const level of ["L0", "L1", "L2", "L3"]) {
      const names = MATRIX.filter((r) => r[0] === level).map((r) => r[2]);
      expect([...names].sort()).toEqual(Object.keys(EVENTS).sort());
    }
  });

  it.each(MATRIX)("%s + %s", (_level, start, eventName, expected, note) => {
    const result = zoomTransition(GRAPH, start, EVENTS[eventName]);
    if (expected === "same") expect(result.state).toBe(start);
    else expect(result.state).toEqual(expected);
    expect(result.note).toBe(note);
  });

  it("lands only on well-formed states: L0 unfocused, L1 on a task, L2 and L3 on a run, a tab at L3 alone", () => {
    for (const [, start, eventName] of MATRIX) {
      const { state } = zoomTransition(GRAPH, start, EVENTS[eventName]);
      const kind = state.focusId === null ? null : GRAPH.get(state.focusId)?.kind;
      if (state.level === 0) expect([state.focusId, state.tab]).toEqual([null, null]);
      if (state.level === 1) expect([kind, state.tab]).toEqual(["task", null]);
      if (state.level === 2) expect([kind === "builder_run" || kind === "review_run", state.tab]).toEqual([true, null]);
      if (state.level === 3) expect([kind === "builder_run" || kind === "review_run", state.tab === null]).toEqual([true, false]);
    }
  });
});

describe("Escape chains", () => {
  it("walks L3 → L2 → L1 → L0 one level per press and then stays put", () => {
    const seen: ZoomState[] = [];
    let state = E2D;
    for (let i = 0; i < 4; i += 1) {
      state = zoomTransition(GRAPH, state, { type: "escape" }).state;
      seen.push(state);
    }
    expect(seen).toEqual([R2, T1, H, H]);
    expect(seen[3]).toBe(seen[2]);
  });

  it("walks from an L2 focus on the other task back to that task, not to t1", () => {
    expect(zoomTransition(GRAPH, R8, { type: "escape" }).state).toEqual(T2);
  });
});

describe("zoomBreadcrumbs — Job > Task > Run", () => {
  it.each([
    ["L0", H, [{ level: 0, nodeId: null, current: true }]],
    ["L1", T1, [{ level: 0, nodeId: null, current: false }, { level: 1, nodeId: "task:t1", current: true }]],
    ["L2", R8, [
      { level: 0, nodeId: null, current: false },
      { level: 1, nodeId: "task:t2", current: false },
      { level: 2, nodeId: "run:t2:8", current: true },
    ]],
    ["L3", E2D, [
      { level: 0, nodeId: null, current: false },
      { level: 1, nodeId: "task:t1", current: false },
      { level: 2, nodeId: "run:t1:2", current: false },
    ]],
  ] as const)("%s", (_name, state, expected) => {
    expect(zoomBreadcrumbs(GRAPH, state)).toEqual(expected);
  });

  it("jumping to each crumb lands on the state that crumb names", () => {
    const crumbs = zoomBreadcrumbs(GRAPH, E2D);
    const landed = crumbs.map((c) => zoomTransition(GRAPH, E2D, { type: "crumb", level: c.level }).state);
    expect(landed).toEqual([H, T1, R2]);
  });
});

describe("clusters", () => {
  // CLUSTER_INPUT_MODEL: task t1 with twelve runs; its cluster view keeps
  // eight and folds seq 1 to 4 into `cluster:t1`.
  const CLUSTERED = zoomGraphOf(CLUSTER_INPUT_MODEL.nodes, clusterBrainModel(CLUSTER_INPUT_MODEL).nodes);

  it("the lookup holds every model node plus the view's cluster node", () => {
    expect(CLUSTERED.size).toBe(CLUSTER_INPUT_MODEL.nodes.length + 1);
    expect(CLUSTERED.get("cluster:t1")).toEqual({ kind: "cluster", parentId: "task:t1" });
  });

  it("a click on the '+N' cluster focuses its task at L1, where the cluster expands", () => {
    expect(zoomTransition(CLUSTERED, H, { type: "click", nodeId: "cluster:t1" }).state)
      .toEqual({ level: 1, focusId: "task:t1", tab: null });
  });

  it("a run the cluster hides can still hold the focus, so reconcile keeps it", () => {
    const hidden: ZoomState = { level: 2, focusId: "run:t1:1", tab: null };
    expect(zoomTransition(CLUSTERED, H, { type: "click", nodeId: "run:t1:1" }).state).toEqual(hidden);
    expect(zoomTransition(CLUSTERED, hidden, { type: "reconcile" }).state).toBe(hidden);
  });
});

describe("invalid focus is a no-op with a debug note", () => {
  it("an orphan run with no task in the graph cannot be focused", () => {
    const orphan = zoomGraphOf([{ id: "run:x:1", kind: "builder_run", parentId: "task:x" }]);
    const result = zoomTransition(orphan, H, { type: "click", nodeId: "run:x:1" });
    expect(result.state).toBe(H);
    expect(result.note).toBe("run run:x:1 has no task in the graph");
  });

  it("an artifact under a task focuses that task, one without a task is refused", () => {
    const graph = zoomGraphOf(GOLDEN_B_MODEL.nodes, [
      { id: "artifact:1", kind: "artifact", parentId: "task:t1" },
      { id: "artifact:2", kind: "artifact", parentId: "job:job-b" },
    ]);
    expect(zoomTransition(graph, H, { type: "click", nodeId: "artifact:1" }).state).toEqual(T1);
    const refused = zoomTransition(graph, H, { type: "click", nodeId: "artifact:2" });
    expect([refused.state, refused.note]).toEqual([H, "artifact artifact:2 has no task in the graph"]);
  });

  it("an earlier list wins when two lists give the same id", () => {
    const graph = zoomGraphOf([{ id: "task:t1", kind: "task", parentId: "job:j" }], [{ id: "task:t1", kind: "cluster" }]);
    expect(graph.get("task:t1")).toEqual({ kind: "task", parentId: "job:j" });
  });
});

describe("reconcile — the graph changed under the focus", () => {
  const withoutT2 = zoomGraphOf(GOLDEN_B_MODEL.nodes.filter((n) => n.id !== "task:t2" && n.id !== "run:t2:8"));
  const withoutRun2 = zoomGraphOf(GOLDEN_B_MODEL.nodes.filter((n) => n.id !== "run:t1:2"));

  it("a run that left while its task stayed walks up to the task (L2 and L3 alike)", () => {
    expect(zoomTransition(withoutRun2, R2, { type: "reconcile" }))
      .toEqual({ state: T1, note: "focus run:t1:2 left the graph; walked up to its task" });
    expect(zoomTransition(withoutRun2, E2D, { type: "reconcile" }))
      .toEqual({ state: T1, note: "focus run:t1:2 left the graph; walked up to its task" });
  });

  it("a run that left with its task walks up to the job", () => {
    expect(zoomTransition(withoutT2, R8, { type: "reconcile" }))
      .toEqual({ state: H, note: "focus run:t2:8 left the graph; walked up to the job" });
  });

  it("a focused task that left walks up to the job", () => {
    expect(zoomTransition(withoutT2, T2, { type: "reconcile" }))
      .toEqual({ state: H, note: "focus task:t2 left the graph; walked up to the job" });
  });

  it("a focus still in the graph is left alone", () => {
    expect(zoomTransition(withoutT2, T1, { type: "reconcile" }).state).toBe(T1);
  });
});
