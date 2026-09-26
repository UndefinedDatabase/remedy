import { describe, expect, it } from "vitest";
import type { RemedyTaskItem } from "../../api/types";
import { reduceBrainEvent, seedBrainModel } from "./brainReducer";
import { row } from "./brainReducer.fixtures";
import { buildBrainLayout } from "./buildForceBrainModel";
import type { BrainLayoutData } from "./forceBrainTypes";
import {
  BRAIN_FILTER_STATES, DASHBOARD_STATE_STATUS, brainTaskCount, carryBrainPositions,
  dashboardBrainSeeds, filterBrainLayout, selectedBrainNodeId, selectionTaskIdOf, shellSelectionIdOf,
} from "./brainView";

function task(id: string, state: RemedyTaskItem["state"], label = id): RemedyTaskItem {
  return { id, label, state, kind: "task", checked: false, muted: false, nodeId: `node-${id}` };
}

/** A small real layout — one task per filter bucket, built the same way the
 *  stage builds one (seed → replay → position), never hand-typed positions. */
function sampleLayout(): BrainLayoutData {
  const tasks = [
    task("prog", "pending"),
    task("blocked", "blocked"),
    task("planned", "pending"),
    task("done", "pending"),
  ];
  let model = seedBrainModel("job-f", dashboardBrainSeeds(tasks));
  model = reduceBrainEvent(model, row(1, "task_run_started", "prog"));
  model = reduceBrainEvent(model, row(2, "task_run_started", "done"));
  model = reduceBrainEvent(model, row(3, "task_round_completed", "done", "pass"));
  model = reduceBrainEvent(model, row(4, "task_run_completed", "done", "pass"));
  return buildBrainLayout(model);
}

describe("DASHBOARD_STATE_STATUS", () => {
  it("maps all five dashboard state words onto the seed's status vocabulary; suggested seeds a task the reducer draws planned", () => {
    const tasks = [
      task("done1", "done"),
      task("cur1", "current"),
      task("pend1", "pending"),
      task("block1", "blocked"),
      task("sugg1", "suggested"),
    ];
    const seeds = dashboardBrainSeeds(tasks);
    expect(seeds.map((s) => s.status)).toEqual(["completed", "running", "pending", "blocked", "suggested"]);

    const model = seedBrainModel("job-x", seeds);
    const byId = new Map(model.nodes.map((n) => [n.id, n]));
    expect(byId.get("task:done1")?.state).toBe("pass");
    expect(byId.get("task:cur1")?.state).toBe("in_progress");
    expect(byId.get("task:pend1")?.state).toBe("planned");
    expect(byId.get("task:block1")?.state).toBe("blocked");
    expect(byId.get("task:sugg1")?.state).toBe("planned");
    expect(byId.get("task:sugg1")?.meta.status).toBe("suggested");
    expect(DASHBOARD_STATE_STATUS.suggested).toBe("suggested");
  });
});

describe("dashboardBrainSeeds", () => {
  it("rank is the list index and title is the task's label, in list order", () => {
    const tasks = [task("a", "pending", "Alpha"), task("b", "pending", "Beta"), task("c", "pending", "Gamma")];
    const seeds = dashboardBrainSeeds(tasks);
    expect(seeds.map((s) => s.rank)).toEqual([0, 1, 2]);
    expect(seeds.map((s) => s.title)).toEqual(["Alpha", "Beta", "Gamma"]);
    expect(seeds.map((s) => s.id)).toEqual(["a", "b", "c"]);
  });

  it("seeds a task named in pausedTaskIds as paused, whatever its dashboard status word (DECISION F025 D3 clause 2)", () => {
    const tasks = [task("a", "current", "Alpha"), task("b", "pending", "Beta"), task("c", "done", "Gamma")];
    const seeds = dashboardBrainSeeds(tasks, ["b"]);
    expect(seeds.map((s) => s.status)).toEqual(["running", "paused", "completed"]);
    const model = seedBrainModel("job-paused-seed", seeds);
    expect(model.nodes.find((n) => n.id === "task:b")?.state).toBe("paused");
  });

  it("with no second argument, seeds exactly as before — no call site is disturbed", () => {
    const tasks = [task("a", "pending", "Alpha")];
    expect(dashboardBrainSeeds(tasks)).toEqual(dashboardBrainSeeds(tasks, []));
  });

  // DECISION F026 D3 clause 2: `specVersions` puts a seed's `specVersion` key
  // ONLY when the map carries that task at all.
  it("puts specVersion on a seed only when the map carries that task", () => {
    const tasks = [task("a", "pending", "Alpha"), task("b", "pending", "Beta")];
    const seeds = dashboardBrainSeeds(tasks, [], [], { a: 2 });
    expect(seeds.find((s) => s.id === "a")?.specVersion).toBe(2);
    expect(seeds.find((s) => s.id === "b")).not.toHaveProperty("specVersion");
  });

  it("with no fourth argument, no seed carries a specVersion", () => {
    const tasks = [task("a", "pending", "Alpha")];
    const seeds = dashboardBrainSeeds(tasks, []);
    expect(seeds[0]).not.toHaveProperty("specVersion");
  });

  it("seeds a task named in vetoedTaskIds as vetoed, whatever its dashboard status word (DECISION F027 D7 (2))", () => {
    const tasks = [task("a", "current", "Alpha"), task("b", "pending", "Beta"), task("c", "done", "Gamma")];
    const seeds = dashboardBrainSeeds(tasks, [], ["b"]);
    expect(seeds.map((s) => s.status)).toEqual(["running", "vetoed", "completed"]);
    const model = seedBrainModel("job-vetoed-seed", seeds);
    expect(model.nodes.find((n) => n.id === "task:b")?.state).toBe("vetoed");
  });

  it("vetoed wins over paused when a task is named in both (DECISION F027 D7 (2))", () => {
    const tasks = [task("a", "pending", "Alpha")];
    const seeds = dashboardBrainSeeds(tasks, ["a"], ["a"]);
    expect(seeds[0].status).toBe("vetoed");
  });

  it("with no third argument, no task seeds vetoed", () => {
    const tasks = [task("a", "pending", "Alpha")];
    expect(dashboardBrainSeeds(tasks, [])).toEqual(dashboardBrainSeeds(tasks, [], []));
  });
});

describe("filterBrainLayout", () => {
  it('"all" returns the SAME object', () => {
    const layout = sampleLayout();
    expect(filterBrainLayout(layout, "all")).toBe(layout);
  });

  it("open keeps in_progress/blocked/fail tasks and drops planned/pass ones", () => {
    const layout = sampleLayout();
    const visible = filterBrainLayout(layout, "open");
    const taskIds = visible.nodes.filter((n) => n.kind === "task").map((n) => n.id).sort();
    expect(taskIds).toEqual(["task:blocked", "task:prog"]);
    expect(BRAIN_FILTER_STATES.open).toEqual(["in_progress", "blocked", "fail"]);
  });

  it("groups paused with planned (DECISION F025 D3 clause 2)", () => {
    expect(BRAIN_FILTER_STATES.planned).toEqual(["planned", "paused"]);
  });

  it("groups vetoed with done (DECISION F027 D7 (2))", () => {
    expect(BRAIN_FILTER_STATES.done).toEqual(["pass", "vetoed"]);
  });

  it("a run follows its task in and out", () => {
    const layout = sampleLayout();
    const visibleOpen = filterBrainLayout(layout, "open");
    expect(visibleOpen.nodes.some((n) => n.parentId === "task:prog")).toBe(true);
    const visibleDone = filterBrainLayout(layout, "done");
    expect(visibleDone.nodes.some((n) => n.parentId === "task:prog")).toBe(false);
  });

  it("a link is dropped when either end is dropped", () => {
    const layout = sampleLayout();
    const visibleDone = filterBrainLayout(layout, "done");
    const keptIds = new Set(visibleDone.nodes.map((n) => n.id));
    for (const l of visibleDone.links) {
      expect(keptIds.has(l.source)).toBe(true);
      expect(keptIds.has(l.target)).toBe(true);
    }
    expect(visibleDone.links.some((l) => l.target === "task:prog")).toBe(false);
  });

  it("the core always stays", () => {
    const layout = sampleLayout();
    for (const f of ["open", "planned", "done"] as const) {
      expect(filterBrainLayout(layout, f).nodes.some((n) => n.depth === 0)).toBe(true);
    }
  });

  it("input layout is never mutated", () => {
    const layout = sampleLayout();
    const before = JSON.parse(JSON.stringify(layout));
    filterBrainLayout(layout, "open");
    expect(layout).toEqual(before);
  });
});

describe("brainTaskCount", () => {
  it("counts only kind === task nodes", () => {
    const layout = sampleLayout();
    expect(brainTaskCount(layout)).toBe(4);
    expect(brainTaskCount(filterBrainLayout(layout, "planned"))).toBe(1);
  });
});

describe("selectedBrainNodeId", () => {
  const tasks = [task("a", "pending"), task("b", "pending")];

  it("resolves by task id", () => {
    expect(selectedBrainNodeId(tasks, "a")).toBe("task:a");
  });

  it("resolves by nodeId", () => {
    expect(selectedBrainNodeId(tasks, "node-b")).toBe("task:b");
  });

  it("returns null for null", () => {
    expect(selectedBrainNodeId(tasks, null)).toBeNull();
  });

  it("returns null for an unknown id", () => {
    expect(selectedBrainNodeId(tasks, "nope")).toBeNull();
  });
});

describe("selectionTaskIdOf", () => {
  it("a task node resolves to its own id", () => {
    expect(selectionTaskIdOf({ id: "task:t1", kind: "task", parentId: "job:j1" })).toBe("t1");
  });

  it("a run node resolves to its parent task via parentId", () => {
    expect(selectionTaskIdOf({ id: "run:t1:3", kind: "builder_run", parentId: "task:t1" })).toBe("t1");
  });

  it("a cluster node resolves to its parent task via parentId", () => {
    expect(selectionTaskIdOf({ id: "cluster:t1", kind: "cluster", parentId: "task:t1" })).toBe("t1");
  });

  it("the core resolves to null", () => {
    expect(selectionTaskIdOf({ id: "job:j1", kind: "job_core" })).toBeNull();
  });
});

describe("shellSelectionIdOf", () => {
  const tasks = [task("a", "pending"), task("b", "pending")];

  it("maps a task id to that task's nodeId", () => {
    expect(shellSelectionIdOf(tasks, "a")).toBe("node-a");
  });

  it("falls back to the given id for an unknown task", () => {
    expect(shellSelectionIdOf(tasks, "nope")).toBe("nope");
  });

  it("returns null for null", () => {
    expect(shellSelectionIdOf(tasks, null)).toBeNull();
  });
});

describe("carryBrainPositions", () => {
  it("keeps a survivor's x/y from previous", () => {
    const next = sampleLayout().nodes;
    const previous = next.map((n) => ({ id: n.id, x: n.x + 999, y: n.y + 999 }));
    const result = carryBrainPositions(previous, next);
    result.forEach((n) => {
      const p = previous.find((pp) => pp.id === n.id);
      expect(n.x).toBe(p?.x);
      expect(n.y).toBe(p?.y);
    });
  });

  it("gives a newcomer its own layout x/y when absent from previous", () => {
    const next = sampleLayout().nodes;
    const result = carryBrainPositions([], next);
    expect(result.map((n) => n.x)).toEqual(next.map((n) => n.x));
    expect(result.map((n) => n.y)).toEqual(next.map((n) => n.y));
  });

  it("never copies fx/fy from previous", () => {
    const next = sampleLayout().nodes;
    const previous = next.map((n) => ({ id: n.id, x: 1, y: 1, fx: 555, fy: 555 }));
    const result = carryBrainPositions(previous, next);
    const core = result.find((n) => n.depth === 0);
    expect(core?.fx).toBe(0);
    expect(core?.fy).toBe(0);
  });

  it("returns new objects and does not mutate either input", () => {
    const next = sampleLayout().nodes;
    const nextSnapshot = next.map((n) => ({ ...n }));
    const previous = next.map((n) => ({ id: n.id, x: n.x, y: n.y }));
    const previousSnapshot = previous.map((n) => ({ ...n }));
    const result = carryBrainPositions(previous, next);
    expect(result).not.toBe(next);
    result.forEach((n, i) => expect(n).not.toBe(next[i]));
    expect(next).toEqual(nextSnapshot);
    expect(previous).toEqual(previousSnapshot);
  });

  it("null previous yields plain copies", () => {
    const next = sampleLayout().nodes;
    const result = carryBrainPositions(null, next);
    expect(result).toEqual(next);
    result.forEach((n, i) => expect(n).not.toBe(next[i]));
  });
});
