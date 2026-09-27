import { describe, expect, it } from "vitest";
import { dashboardBrainSeeds } from "./brainView";
import { rebuildBrainModel, reduceBrainEvent, seedBrainModel } from "./brainReducer";
import { buildBrainLayout } from "./buildForceBrainModel";
import { BRAIN_DEMO_FRAMES, BRAIN_DEMO_JOB_ID, BRAIN_DEMO_TASKS, brainDemoRows } from "./brainDemoRecording";
import type { BrainEventRow, BrainModel } from "./brainOntology";

// The golden below is HAND-DERIVED from DECISION F019 D1's Tables 1/2 and
// F288 D3 (3)'s two new tables, the same way brainReducer.fixtures.ts's
// goldens are — never printed from the reducer, or a bug in the reducer
// could never show up here. Task A is "fe1b5b487fda490f" (rank 0), task B is
// "4b3ddac9dba846af" (rank 1); both seed as "pending" -> "planned" (Table 1).
// The recorded frames, re-captured for R-1075: task A gets a builder run at
// seq 0 (run:...490f:0, attempt "b1603f4616344102"), a needs_repair review
// at seq 1 (fail, Table 2), a repair at seq 2 (changed -> pass, F288 D3's
// repair table), a pass review at seq 3, then task_run_completed(pass) at
// seq 4 closes the builder run to pass and the task to pass — every run of
// task A's carries `meta.attemptId` since every one of its rows does. Task B
// repeats the same shape at seq 5-9 (its own attempt, its builder run keyed
// by seq 5). Both tasks end "pass", so the core (which is never stored, only
// derived) ends "pass" too.
const DEMO_GOLDEN_MODEL: BrainModel = {
  jobId: BRAIN_DEMO_JOB_ID,
  lastSeq: 9,
  nodes: [
    { id: "job:1fe464f842e74f55", kind: "job_core", state: "pass", seq: 0, meta: {} },
    {
      id: "task:fe1b5b487fda490f", kind: "task", state: "pass", parentId: "job:1fe464f842e74f55", seq: 0,
      meta: { rank: 0, title: "Deliver src/main.py", status: "pending" },
    },
    {
      id: "task:4b3ddac9dba846af", kind: "task", state: "pass", parentId: "job:1fe464f842e74f55", seq: 0,
      meta: { rank: 1, title: "Deliver README.md", status: "pending" },
    },
    {
      id: "run:fe1b5b487fda490f:0", kind: "builder_run", state: "pass",
      parentId: "task:fe1b5b487fda490f", seq: 0, meta: { attemptId: "b1603f4616344102", outcome: "pass" },
    },
    {
      id: "run:fe1b5b487fda490f:1", kind: "review_run", state: "fail",
      parentId: "task:fe1b5b487fda490f", seq: 1, meta: { outcome: "needs_repair", attemptId: "b1603f4616344102" },
    },
    {
      id: "run:fe1b5b487fda490f:2", kind: "repair_run", state: "pass",
      parentId: "task:fe1b5b487fda490f", seq: 2, meta: { outcome: "changed", attemptId: "b1603f4616344102" },
    },
    {
      id: "run:fe1b5b487fda490f:3", kind: "review_run", state: "pass",
      parentId: "task:fe1b5b487fda490f", seq: 3, meta: { outcome: "pass", attemptId: "b1603f4616344102" },
    },
    {
      id: "run:4b3ddac9dba846af:5", kind: "builder_run", state: "pass",
      parentId: "task:4b3ddac9dba846af", seq: 5, meta: { attemptId: "935e9371d7ce4fe5", outcome: "pass" },
    },
    {
      id: "run:4b3ddac9dba846af:6", kind: "review_run", state: "fail",
      parentId: "task:4b3ddac9dba846af", seq: 6, meta: { outcome: "needs_repair", attemptId: "935e9371d7ce4fe5" },
    },
    {
      id: "run:4b3ddac9dba846af:7", kind: "repair_run", state: "pass",
      parentId: "task:4b3ddac9dba846af", seq: 7, meta: { outcome: "changed", attemptId: "935e9371d7ce4fe5" },
    },
    {
      id: "run:4b3ddac9dba846af:8", kind: "review_run", state: "pass",
      parentId: "task:4b3ddac9dba846af", seq: 8, meta: { outcome: "pass", attemptId: "935e9371d7ce4fe5" },
    },
  ],
  links: [
    { id: "job:1fe464f842e74f55->task:fe1b5b487fda490f", source: "job:1fe464f842e74f55", target: "task:fe1b5b487fda490f" },
    { id: "job:1fe464f842e74f55->task:4b3ddac9dba846af", source: "job:1fe464f842e74f55", target: "task:4b3ddac9dba846af" },
    { id: "task:fe1b5b487fda490f->run:fe1b5b487fda490f:0", source: "task:fe1b5b487fda490f", target: "run:fe1b5b487fda490f:0" },
    { id: "task:fe1b5b487fda490f->run:fe1b5b487fda490f:1", source: "task:fe1b5b487fda490f", target: "run:fe1b5b487fda490f:1" },
    { id: "task:fe1b5b487fda490f->run:fe1b5b487fda490f:2", source: "task:fe1b5b487fda490f", target: "run:fe1b5b487fda490f:2" },
    { id: "task:fe1b5b487fda490f->run:fe1b5b487fda490f:3", source: "task:fe1b5b487fda490f", target: "run:fe1b5b487fda490f:3" },
    { id: "task:4b3ddac9dba846af->run:4b3ddac9dba846af:5", source: "task:4b3ddac9dba846af", target: "run:4b3ddac9dba846af:5" },
    { id: "task:4b3ddac9dba846af->run:4b3ddac9dba846af:6", source: "task:4b3ddac9dba846af", target: "run:4b3ddac9dba846af:6" },
    { id: "task:4b3ddac9dba846af->run:4b3ddac9dba846af:7", source: "task:4b3ddac9dba846af", target: "run:4b3ddac9dba846af:7" },
    { id: "task:4b3ddac9dba846af->run:4b3ddac9dba846af:8", source: "task:4b3ddac9dba846af", target: "run:4b3ddac9dba846af:8" },
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
