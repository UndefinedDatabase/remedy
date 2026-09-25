// The index behind the bar's fast path is held to the plain fold: at EVERY
// position of fuzzed ledgers, `phasesAt` equals `readPhases` over the prefix
// (DECISION F024 D3). The ledgers come from a seeded generator, so a red run
// replays exactly.
import { describe, expect, it } from "vitest";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import { GOLDEN_B_JOB_ID, GOLDEN_B_ROWS, GOLDEN_B_TASKS } from "../graph/brainReducer.fixtures";
import type { BrainEventRow, BrainTaskSeed } from "../graph/brainOntology";
import { readPhases } from "./phaseMapping";
import { buildTimelineIndex, indexHead, phasesAt, phaseStops } from "./timelineIndex";

const TASKS: readonly BrainTaskSeed[] = [
  { id: "t1", status: "completed", rank: 0 },
  { id: "t2", status: "pending", rank: 1 },
];

function generator(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

// Weighted toward the kinds that move phases and task states, so fuzzed
// ledgers reach Finalized, lose it and reach it again.
const KINDS: readonly [string, string][] = [
  ["planning_started", ""],
  ["planning_completed", "changed"],
  ["task_run_started", ""],
  ["task_run_started", ""],
  ["task_round_completed", "pass"],
  ["task_round_completed", "needs_repair"],
  ["task_round_completed", "no_review"],
  ["verification_passed", "pass"],
  ["test_run_started", ""],
  ["task_run_completed", "pass"],
  ["task_run_completed", "pass"],
  ["task_run_completed", "pass"],
  ["task_run_failed", "fail"],
  ["job_stopped", "stopped"],
  ["budget.tick", ""],
];

function fuzzLedger(seed: number, size: number): BrainEventRow[] {
  const next = generator(seed);
  const rows: BrainEventRow[] = [];
  let seq = 0;
  for (let i = 0; i < size; i += 1) {
    const [kind, outcome] = KINDS[Math.floor(next() * KINDS.length)];
    rows.push({ seq, kind, outcome, taskId: next() < 0.5 ? "t1" : "t2" });
    seq += next() < 0.1 ? 2 : 1;
  }
  return rows.reverse();
}

describe("the index equals the plain fold at every position", () => {
  it("over fuzzed ledgers, from before the first row to past the last", () => {
    let finalized = 0;
    for (let ledger = 1; ledger <= 16; ledger += 1) {
      const rows = fuzzLedger(ledger, 40 + ledger * 5);
      const index = buildTimelineIndex("job-x", TASKS, rows);
      const head = indexHead(index) as number;
      for (let s = -1; s <= head + 1; s += 1) {
        const expected = readPhases("job-x", TASKS, rows.filter((r) => r.seq <= s));
        expect(phasesAt(index, s)).toEqual(expected);
        if (expected.current === "finalized") finalized += 1;
      }
    }
    expect(finalized).toBeGreaterThan(0);
  });

  it("over the demo recording", () => {
    const tasks: BrainTaskSeed[] = [
      { id: "a7a8f67f1b9a4814", status: "pending", rank: 0 },
      { id: "1965fb3f26b64fe7", status: "pending", rank: 1 },
    ];
    const index = buildTimelineIndex(BRAIN_DEMO_JOB_ID, tasks, brainDemoRows());
    for (let s = -1; s <= 8; s += 1) {
      expect(phasesAt(index, s)).toEqual(
        readPhases(BRAIN_DEMO_JOB_ID, tasks, brainDemoRows().filter((r) => r.seq <= s)),
      );
    }
    expect(indexHead(index)).toBe(7);
    expect(phaseStops(index)).toEqual([0, 1, 7]);
  });
});

describe("the index's own arrays", () => {
  it("golden B: the high-water phase per row and each marked phase's start", () => {
    expect(buildTimelineIndex(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, GOLDEN_B_ROWS)).toEqual({
      seqs: [1, 2, 3, 4, 5, 6, 7, 8, 9],
      reached: [2, 4, 4, 4, 4, 4, 4, 4, 4],
      passSince: [null, null, null, null, null, null, null, null, null],
      starts: [1, 1, 1, 2, 2],
    });
  });

  it("an empty ledger reaches nothing and has no stops", () => {
    const index = buildTimelineIndex("job-e", TASKS, []);
    expect(indexHead(index)).toBeNull();
    expect(phasesAt(index, 5)).toEqual({ current: "job", spans: [], lastSeq: null });
    expect(phaseStops(index)).toEqual([]);
  });
});
