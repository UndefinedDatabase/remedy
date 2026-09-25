import { describe, expect, it } from "vitest";
import { feedRowOf } from "../../api/feedRow";
import {
  clusterBrainModel, emptyBrainModel, rebuildBrainModel, reduceBrainEvent, seedBrainModel,
} from "./brainReducer";
import {
  CLUSTER_EXPECTED_MODEL, CLUSTER_INPUT_MODEL, GOLDEN_A_FRAMES, GOLDEN_A_JOB_ID, GOLDEN_A_MODEL,
  GOLDEN_A_ROWS, GOLDEN_A_TASKS, GOLDEN_B_JOB_ID, GOLDEN_B_MODEL, GOLDEN_B_ROWS, GOLDEN_B_TASKS,
  GOLDEN_C_JOB_ID, GOLDEN_C_MODEL, GOLDEN_C_ROWS, GOLDEN_C_TASKS, SEED_STATUS_CASES, row,
} from "./brainReducer.fixtures";
import type { BrainEventRow, BrainModel } from "./brainOntology";

/** Fold a row stream through the live-reduce path, the way a stream client
 *  actually consumes frames one at a time. */
function fold(seed: BrainModel, rows: readonly BrainEventRow[]): BrainModel {
  return rows.reduce((model, r) => reduceBrainEvent(model, r), seed);
}

describe("Golden A: one task, happy path", () => {
  it("matches the hand-derived model exactly", () => {
    const seeded = seedBrainModel(GOLDEN_A_JOB_ID, GOLDEN_A_TASKS);
    expect(fold(seeded, GOLDEN_A_ROWS)).toEqual(GOLDEN_A_MODEL);
  });
});

describe("Golden B: repair and resume", () => {
  it("matches the hand-derived model, including the blocked interrupted run", () => {
    const seeded = seedBrainModel(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS);
    const result = fold(seeded, GOLDEN_B_ROWS);
    expect(result).toEqual(GOLDEN_B_MODEL);
    // Run ids are pinned to the SEQ that birthed them, not a birth-order
    // counter: seq 4 (job_stopped) births nothing, so t1's run ids are
    // 1, 2, 3, 5, 6 — never 1..5 — which is what keeps an id stable across
    // a gap (DECISION F019 D1).
    const t1RunIds = result.nodes.filter((n) => n.parentId === "task:t1").map((n) => n.id);
    expect(t1RunIds).toEqual(["run:t1:1", "run:t1:2", "run:t1:3", "run:t1:5", "run:t1:6"]);
    // job_stopped left the interrupted first attempt blocked, not deleted.
    const interrupted = result.nodes.find((n) => n.id === "run:t1:1");
    expect(interrupted?.state).toBe("blocked");
  });
});

describe("Golden C: unseeded task and unknown kinds", () => {
  it("matches the hand-derived model, including ignored counts", () => {
    const seeded = seedBrainModel(GOLDEN_C_JOB_ID, GOLDEN_C_TASKS);
    const result = fold(seeded, GOLDEN_C_ROWS);
    expect(result).toEqual(GOLDEN_C_MODEL);
    expect(result.ignored).not.toHaveProperty("builder_started");
  });
});

describe("Idempotence", () => {
  const goldens = [
    { name: "A", jobId: GOLDEN_A_JOB_ID, tasks: GOLDEN_A_TASKS, rows: GOLDEN_A_ROWS, model: GOLDEN_A_MODEL },
    { name: "B", jobId: GOLDEN_B_JOB_ID, tasks: GOLDEN_B_TASKS, rows: GOLDEN_B_ROWS, model: GOLDEN_B_MODEL },
    { name: "C", jobId: GOLDEN_C_JOB_ID, tasks: GOLDEN_C_TASKS, rows: GOLDEN_C_ROWS, model: GOLDEN_C_MODEL },
  ];

  for (const g of goldens) {
    it(`golden ${g.name}: each row delivered twice in a row still yields the golden`, () => {
      const doubled = g.rows.flatMap((r) => [r, r]);
      const seeded = seedBrainModel(g.jobId, g.tasks);
      expect(fold(seeded, doubled)).toEqual(g.model);
    });

    it(`golden ${g.name}: the whole stream delivered twice still yields the golden`, () => {
      const twice = [...g.rows, ...g.rows];
      const seeded = seedBrainModel(g.jobId, g.tasks);
      expect(fold(seeded, twice)).toEqual(g.model);
    });

    it(`golden ${g.name}: replaying an already-seen row returns the IDENTICAL object`, () => {
      const seeded = seedBrainModel(g.jobId, g.tasks);
      const applied = fold(seeded, g.rows);
      const replayedLast = reduceBrainEvent(applied, g.rows[g.rows.length - 1]);
      expect(replayedLast).toBe(applied);
      const replayedFirst = reduceBrainEvent(applied, g.rows[0]);
      expect(replayedFirst).toBe(applied);
    });
  }
});

/** A tiny deterministic shuffle (no Math.random): a fixed-seed LCG walks a
 *  Fisher-Yates pass, so the same seed always produces the same permutation. */
function seededShuffle<T>(items: readonly T[], seed: number): T[] {
  const arr = [...items];
  let s = seed;
  for (let i = arr.length - 1; i > 0; i--) {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    const j = s % (i + 1);
    const tmp = arr[i];
    arr[i] = arr[j];
    arr[j] = tmp;
  }
  return arr;
}

describe("Hostile orderings through the snapshot path", () => {
  it("a fixed-seed shuffle of golden B's rows, plus duplicates, still rebuilds golden B exactly", () => {
    const shuffled = seededShuffle(GOLDEN_B_ROWS, 42);
    const withDuplicates = [...shuffled, GOLDEN_B_ROWS[0], GOLDEN_B_ROWS[4], GOLDEN_B_ROWS[8]];
    const rebuilt = rebuildBrainModel(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, withDuplicates);
    expect(rebuilt).toEqual(GOLDEN_B_MODEL);
  });

  it("a second, differently-seeded shuffle also rebuilds golden B exactly", () => {
    const shuffled = seededShuffle(GOLDEN_B_ROWS, 12345);
    const rebuilt = rebuildBrainModel(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, shuffled);
    expect(rebuilt).toEqual(GOLDEN_B_MODEL);
  });
});

describe("Ghost hunt", () => {
  it("a snapshot rebuild over the FULL rows replaces a gapped live model with no leftover ghosts", () => {
    // Drop rows at two positions (indices 2 and 5): the needs_repair round
    // and the resumed round_completed(pass).
    const gapped = GOLDEN_B_ROWS.filter((_, idx) => idx !== 2 && idx !== 5);
    const seeded = seedBrainModel(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS);
    const live = fold(seeded, gapped);

    const rebuilt = rebuildBrainModel(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, GOLDEN_B_ROWS);
    expect(rebuilt).toEqual(GOLDEN_B_MODEL);

    // Every node in the gapped live model is not just an id golden B also
    // has: it is the SAME entity — same kind, same parent. An id that
    // collided across two DIFFERENT births (a stale counter reused after a
    // dropped row) would pass an id-only check while still being a ghost:
    // the right id wearing the wrong kind.
    const goldenById = new Map(GOLDEN_B_MODEL.nodes.map((n) => [n.id, n]));
    for (const liveNode of live.nodes) {
      const goldenNode = goldenById.get(liveNode.id);
      expect(goldenNode, `live node ${liveNode.id} has no counterpart in golden B`).toBeDefined();
      expect(goldenNode?.kind).toBe(liveNode.kind);
      expect(goldenNode?.parentId).toBe(liveNode.parentId);
    }
  });
});

describe("feedRowOf interop", () => {
  it("frames shaped as the server writes them feed the reducer into golden A", () => {
    const seeded = seedBrainModel(GOLDEN_A_JOB_ID, GOLDEN_A_TASKS);
    const rowsFromFrames = GOLDEN_A_FRAMES.map((frame) => {
      const feedRow = feedRowOf(frame, 0);
      return row(feedRow.seq, feedRow.kind, feedRow.taskId, feedRow.outcome);
    });
    expect(fold(seeded, rowsFromFrames)).toEqual(GOLDEN_A_MODEL);
  });
});

describe("clusterBrainModel", () => {
  it("11 finished runs + 1 in_progress collapse to the in_progress run, the 7 most recent, and one cluster node", () => {
    expect(clusterBrainModel(CLUSTER_INPUT_MODEL)).toEqual(CLUSTER_EXPECTED_MODEL);
  });

  it("a model with no task over the threshold is returned UNCHANGED (===)", () => {
    const seeded = seedBrainModel(GOLDEN_A_JOB_ID, GOLDEN_A_TASKS);
    const model = fold(seeded, GOLDEN_A_ROWS);
    expect(clusterBrainModel(model)).toBe(model);
  });
});

describe("Seed status table (Table 1)", () => {
  it.each(SEED_STATUS_CASES)("status %s maps to node state %s", (status, expected) => {
    const seeded = seedBrainModel("job-status", [{ id: "t1", status, rank: 0 }]);
    const task = seeded.nodes.find((n) => n.id === "task:t1");
    expect(task?.state).toBe(expected);
    expect(task?.meta.status).toBe(status);
  });
});

describe("task_run_started interrupts a still-open previous run", () => {
  it("a second start while the first builder_run is still in_progress blocks the first and opens a second", () => {
    const seeded = seedBrainModel("job-y", [{ id: "t1", status: "pending", rank: 0 }]);
    const afterFirst = reduceBrainEvent(seeded, row(1, "task_run_started", "t1"));
    expect(afterFirst.nodes.find((n) => n.id === "run:t1:1")?.state).toBe("in_progress");
    const afterSecond = reduceBrainEvent(afterFirst, row(2, "task_run_started", "t1"));
    expect(afterSecond.nodes.find((n) => n.id === "run:t1:1")?.state).toBe("blocked");
    expect(afterSecond.nodes.find((n) => n.id === "run:t1:2")?.state).toBe("in_progress");
  });
});

describe("rebuildBrainModel dedup and order", () => {
  it("keeps the FIRST row when two different rows share a seq", () => {
    const rebuilt = rebuildBrainModel("job-z", [], [
      row(1, "task_run_started", "t1"),
      row(1, "task_run_started", "t2"),
    ]);
    const ids = rebuilt.nodes.map((n) => n.id);
    expect(ids).toContain("task:t1");
    expect(ids).not.toContain("task:t2");
  });
});

describe("job_stopped blocks every in_progress run directly", () => {
  it("an in_progress run is blocked by job_stopped even with no further stream activity", () => {
    const seeded = seedBrainModel("job-w", [{ id: "t1", status: "pending", rank: 0 }]);
    const started = reduceBrainEvent(seeded, row(1, "task_run_started", "t1"));
    const stopped = reduceBrainEvent(started, row(2, "job_stopped", "", "stopped"));
    expect(stopped.nodes.find((n) => n.id === "run:t1:1")?.state).toBe("blocked");
    expect(stopped.nodes.find((n) => n.id === "task:t1")?.state).toBe("planned");
  });
});

describe("F025 pause/resume events (DECISION F025 D3 clause 2)", () => {
  it("task_paused births an unseen task paused, and is not counted in ignored", () => {
    const seeded = seedBrainModel("job-p", []);
    const paused = reduceBrainEvent(seeded, row(1, "task_paused", "t1"));
    expect(paused.nodes.find((n) => n.id === "task:t1")?.state).toBe("paused");
    expect(paused.ignored).not.toHaveProperty("task_paused");
  });

  it("task_paused never overwrites a task that already passed", () => {
    const seeded = seedBrainModel("job-p", [{ id: "t1", status: "pending", rank: 0 }]);
    const passed = fold(seeded, [
      row(1, "task_run_started", "t1"),
      row(2, "task_run_completed", "t1", "pass"),
    ]);
    const paused = reduceBrainEvent(passed, row(3, "task_paused", "t1"));
    expect(paused.nodes.find((n) => n.id === "task:t1")?.state).toBe("pass");
  });

  it("task_resumed returns a paused task to planned, and is not counted in ignored", () => {
    const seeded = seedBrainModel("job-p", [{ id: "t1", status: "pending", rank: 0 }]);
    const paused = reduceBrainEvent(seeded, row(1, "task_paused", "t1"));
    const resumed = reduceBrainEvent(paused, row(2, "task_resumed", "t1"));
    expect(resumed.nodes.find((n) => n.id === "task:t1")?.state).toBe("planned");
    expect(resumed.ignored).not.toHaveProperty("task_resumed");
  });

  it("task_resumed on a task that is not paused changes nothing", () => {
    const seeded = seedBrainModel("job-p", [{ id: "t1", status: "pending", rank: 0 }]);
    const resumed = reduceBrainEvent(seeded, row(1, "task_resumed", "t1"));
    expect(resumed.nodes.find((n) => n.id === "task:t1")?.state).toBe("planned");
  });

  it("job_paused returns an in-progress task to planned and its open run to paused, and is not counted in ignored", () => {
    const seeded = seedBrainModel("job-p", [{ id: "t1", status: "pending", rank: 0 }]);
    const started = reduceBrainEvent(seeded, row(1, "task_run_started", "t1"));
    const paused = reduceBrainEvent(started, row(2, "job_paused"));
    expect(paused.nodes.find((n) => n.id === "run:t1:1")?.state).toBe("paused");
    expect(paused.nodes.find((n) => n.id === "task:t1")?.state).toBe("planned");
    expect(paused.ignored).not.toHaveProperty("job_paused");
  });

  it("job_resumed changes no node, and is not counted in ignored", () => {
    const seeded = seedBrainModel("job-p", [{ id: "t1", status: "pending", rank: 0 }]);
    const started = reduceBrainEvent(seeded, row(1, "task_run_started", "t1"));
    const resumed = reduceBrainEvent(started, row(2, "job_resumed"));
    expect(resumed.nodes).toBe(started.nodes);
    expect(resumed.links).toBe(started.links);
    expect(resumed.ignored).not.toHaveProperty("job_resumed");
  });

  it("replaying an already-seen task_paused row returns the IDENTICAL object", () => {
    const seeded = seedBrainModel("job-p", [{ id: "t1", status: "pending", rank: 0 }]);
    const paused = reduceBrainEvent(seeded, row(1, "task_paused", "t1"));
    const replayed = reduceBrainEvent(paused, row(1, "task_paused", "t1"));
    expect(replayed).toBe(paused);
  });
});

describe("Core derivation", () => {
  it("planned when there are no tasks", () => {
    expect(emptyBrainModel("job-x").nodes[0].state).toBe("planned");
  });

  it("planned when every seeded task is planned and nothing has run", () => {
    const seeded = seedBrainModel("job-x", [{ id: "t1", status: "pending", rank: 0 }]);
    expect(seeded.nodes[0].state).toBe("planned");
  });

  it("in_progress when any run is in_progress", () => {
    const seeded = seedBrainModel("job-x", [{ id: "t1", status: "pending", rank: 0 }]);
    const started = reduceBrainEvent(seeded, row(1, "task_run_started", "t1"));
    expect(started.nodes[0].state).toBe("in_progress");
  });

  it("fail when a task is fail or blocked, and no run is in_progress", () => {
    const seeded = seedBrainModel("job-x", [{ id: "t1", status: "pending", rank: 0 }]);
    const failed = fold(seeded, [
      row(1, "task_run_started", "t1"),
      row(2, "task_run_failed", "t1", "boom"),
    ]);
    expect(failed.nodes[0].state).toBe("fail");
  });

  it("pass only when there is at least one task and every task is pass", () => {
    const seeded = seedBrainModel("job-x", [
      { id: "t1", status: "pending", rank: 0 },
      { id: "t2", status: "pending", rank: 1 },
    ]);
    const onePassed = fold(seeded, [
      row(1, "task_run_started", "t1"),
      row(2, "task_run_completed", "t1", "pass"),
    ]);
    // t2 is still planned, so the core is not pass yet.
    expect(onePassed.nodes[0].state).toBe("planned");
    const bothPassed = fold(onePassed, [
      row(3, "task_run_started", "t2"),
      row(4, "task_run_completed", "t2", "pass"),
    ]);
    expect(bothPassed.nodes[0].state).toBe("pass");
  });
});
