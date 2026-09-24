import { describe, expect, it } from "vitest";
import { dashboardBrainSeeds } from "./brainView";
import { rebuildBrainModel, reduceBrainEvent, seedBrainModel } from "./brainReducer";
import { buildBrainLayout } from "./buildForceBrainModel";
import { BRAIN_DEMO_FRAMES, BRAIN_DEMO_JOB_ID, BRAIN_DEMO_TASKS, brainDemoRows } from "./brainDemoRecording";
import type { BrainEventRow, BrainModel } from "./brainOntology";

// The golden below is HAND-DERIVED from DECISION F019 D1's Tables 1 and 2,
// the same way brainReducer.fixtures.ts's goldens are — never printed from
// the reducer, or a bug in the reducer could never show up here. Task A is
// "a7a8f67f1b9a4814" (rank 0), task B is "1965fb3f26b64fe7" (rank 1); both
// seed as "pending" -> "planned" (Table 1). The recorded frames: task A gets
// a builder run at seq 0 (run:...4814:0), a needs_repair review at seq 1
// (fail, Table 2), a pass review at seq 2, then task_run_completed(pass) at
// seq 3 closes the builder run to pass and the task to pass. Task B repeats
// the same shape at seq 4-7 (its builder run keyed by seq 4). Both tasks end
// "pass", so the core (which is never stored, only derived) ends "pass" too.
const DEMO_GOLDEN_MODEL: BrainModel = {
  jobId: BRAIN_DEMO_JOB_ID,
  lastSeq: 7,
  nodes: [
    { id: "job:9f932a4f6afc4ded", kind: "job_core", state: "pass", seq: 0, meta: {} },
    {
      id: "task:a7a8f67f1b9a4814", kind: "task", state: "pass", parentId: "job:9f932a4f6afc4ded", seq: 0,
      meta: { rank: 0, title: "Deliver src/main.py", status: "pending" },
    },
    {
      id: "task:1965fb3f26b64fe7", kind: "task", state: "pass", parentId: "job:9f932a4f6afc4ded", seq: 0,
      meta: { rank: 1, title: "Deliver README.md", status: "pending" },
    },
    {
      id: "run:a7a8f67f1b9a4814:0", kind: "builder_run", state: "pass",
      parentId: "task:a7a8f67f1b9a4814", seq: 0, meta: { outcome: "pass" },
    },
    {
      id: "run:a7a8f67f1b9a4814:1", kind: "review_run", state: "fail",
      parentId: "task:a7a8f67f1b9a4814", seq: 1, meta: { outcome: "needs_repair" },
    },
    {
      id: "run:a7a8f67f1b9a4814:2", kind: "review_run", state: "pass",
      parentId: "task:a7a8f67f1b9a4814", seq: 2, meta: { outcome: "pass" },
    },
    {
      id: "run:1965fb3f26b64fe7:4", kind: "builder_run", state: "pass",
      parentId: "task:1965fb3f26b64fe7", seq: 4, meta: { outcome: "pass" },
    },
    {
      id: "run:1965fb3f26b64fe7:5", kind: "review_run", state: "fail",
      parentId: "task:1965fb3f26b64fe7", seq: 5, meta: { outcome: "needs_repair" },
    },
    {
      id: "run:1965fb3f26b64fe7:6", kind: "review_run", state: "pass",
      parentId: "task:1965fb3f26b64fe7", seq: 6, meta: { outcome: "pass" },
    },
  ],
  links: [
    { id: "job:9f932a4f6afc4ded->task:a7a8f67f1b9a4814", source: "job:9f932a4f6afc4ded", target: "task:a7a8f67f1b9a4814" },
    { id: "job:9f932a4f6afc4ded->task:1965fb3f26b64fe7", source: "job:9f932a4f6afc4ded", target: "task:1965fb3f26b64fe7" },
    { id: "task:a7a8f67f1b9a4814->run:a7a8f67f1b9a4814:0", source: "task:a7a8f67f1b9a4814", target: "run:a7a8f67f1b9a4814:0" },
    { id: "task:a7a8f67f1b9a4814->run:a7a8f67f1b9a4814:1", source: "task:a7a8f67f1b9a4814", target: "run:a7a8f67f1b9a4814:1" },
    { id: "task:a7a8f67f1b9a4814->run:a7a8f67f1b9a4814:2", source: "task:a7a8f67f1b9a4814", target: "run:a7a8f67f1b9a4814:2" },
    { id: "task:1965fb3f26b64fe7->run:1965fb3f26b64fe7:4", source: "task:1965fb3f26b64fe7", target: "run:1965fb3f26b64fe7:4" },
    { id: "task:1965fb3f26b64fe7->run:1965fb3f26b64fe7:5", source: "task:1965fb3f26b64fe7", target: "run:1965fb3f26b64fe7:5" },
    { id: "task:1965fb3f26b64fe7->run:1965fb3f26b64fe7:6", source: "task:1965fb3f26b64fe7", target: "run:1965fb3f26b64fe7:6" },
  ],
  ignored: {},
};

/** Fold a row stream through the live-reduce path, the way a stream client
 *  actually consumes frames one at a time (brainReducer.test.ts's own helper). */
function fold(seed: BrainModel, rows: readonly BrainEventRow[]): BrainModel {
  return rows.reduce((model, r) => reduceBrainEvent(model, r), seed);
}

describe("the F019 D1(10) demo recording", () => {
  it("the snapshot path matches the hand-derived golden", () => {
    const result = rebuildBrainModel(BRAIN_DEMO_JOB_ID, dashboardBrainSeeds(BRAIN_DEMO_TASKS), brainDemoRows());
    expect(result).toEqual(DEMO_GOLDEN_MODEL);
  });

  it("the live path (fold, one frame at a time) matches it too", () => {
    const seeded = seedBrainModel(BRAIN_DEMO_JOB_ID, dashboardBrainSeeds(BRAIN_DEMO_TASKS));
    const result = fold(seeded, brainDemoRows());
    expect(result).toEqual(DEMO_GOLDEN_MODEL);
  });

  it("double delivery is harmless: folding the rows twice gives the identical object", () => {
    const seeded = seedBrainModel(BRAIN_DEMO_JOB_ID, dashboardBrainSeeds(BRAIN_DEMO_TASKS));
    const rows = brainDemoRows();
    const once = fold(seeded, rows);
    const twice = fold(once, rows);
    expect(twice).toBe(once);
  });

  it("the recording renders: one layout node/link per model node/link, finite positions", () => {
    const layout = buildBrainLayout(DEMO_GOLDEN_MODEL);
    expect(layout.nodes.map((n) => n.id)).toEqual(DEMO_GOLDEN_MODEL.nodes.map((n) => n.id));
    expect(layout.links).toHaveLength(DEMO_GOLDEN_MODEL.links.length);
    for (const n of layout.nodes) {
      expect(Number.isFinite(n.x)).toBe(true);
      expect(Number.isFinite(n.y)).toBe(true);
    }
  });

  it("is self-consistent: the frames' task ids equal the tasks' ids, and every task has a clickable nodeId", () => {
    const frameTaskIds = new Set(
      BRAIN_DEMO_FRAMES.map((f) => (f.event as { task_id: string }).task_id),
    );
    const taskIds = new Set(BRAIN_DEMO_TASKS.map((t) => t.id));
    expect(frameTaskIds).toEqual(taskIds);
    for (const t of BRAIN_DEMO_TASKS) {
      expect(typeof t.nodeId).toBe("string");
      expect(t.nodeId.length).toBeGreaterThan(0);
    }
  });
});
