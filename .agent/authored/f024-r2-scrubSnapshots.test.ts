// T002's property test, T5_F024.md's "soul of the feature": at any fuzzed position
// the scrubbed state equals a FRESH reduction of that prefix, `rebuildBrainModel`
// over the timeline seed and every row at or below the position — plus the
// snapshot arithmetic, the memory cap and the invalidation rules of DECISION
// F024 D2. The ledgers are drawn from a seeded generator, so a red run replays.
import { describe, expect, it } from "vitest";
import { rebuildBrainModel, seedBrainModel } from "../graph/brainReducer";
import type { BrainEventRow, BrainTaskSeed } from "../graph/brainOntology";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import { timelineSeedOf } from "./phaseMapping";
import { createScrubMemo, SNAPSHOT_CAP, SNAPSHOT_EVERY } from "./scrubSnapshots";

const TASKS: readonly BrainTaskSeed[] = [
  { id: "t1", status: "completed", rank: 0 },
  { id: "t2", status: "running", rank: 1 },
  { id: "t3", status: "pending", rank: 2 },
];

// A small linear congruential generator: deterministic, so every fuzzed
// position below is the same on every run.
function generator(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

const KINDS: readonly [string, string][] = [
  ["task_run_started", ""],
  ["task_round_completed", "pass"],
  ["task_round_completed", "fail"],
  ["task_round_completed", "needs_repair"],
  ["task_round_completed", "no_review"],
  ["verification_passed", "pass"],
  ["verification_failed", "fail"],
  ["task_run_completed", "pass"],
  ["task_run_failed", "fail"],
  ["task_run_noop", "no_change"],
  ["task_needs_decision", ""],
  ["task_decision_answered", ""],
  ["job_stopped", "stopped"],
  ["budget.tick", ""],
  ["builder_started", ""],
  ["", ""],
];
const TASK_IDS = ["t1", "t2", "t3", "tX", ""];

/** A ledger of about `size` rows: seqs from 0 with gaps, some seqs repeated with
 *  a different row, and the whole list shuffled. */
function fuzzLedger(seed: number, size: number): BrainEventRow[] {
  const next = generator(seed);
  const pick = <T>(list: readonly T[]): T => list[Math.floor(next() * list.length)];
  const rows: BrainEventRow[] = [];
  let seq = 0;
  for (let i = 0; i < size; i += 1) {
    const [kind, outcome] = pick(KINDS);
    rows.push({ seq, kind, outcome, taskId: pick(TASK_IDS) });
    if (next() < 0.05) rows.push({ seq, kind: "job_stopped", outcome: "stopped", taskId: "" });
    seq += next() < 0.1 ? 2 + Math.floor(next() * 3) : 1;
  }
  for (let i = rows.length - 1; i > 0; i -= 1) {
    const j = Math.floor(next() * (i + 1));
    [rows[i], rows[j]] = [rows[j], rows[i]];
  }
  return rows;
}

function fresh(jobId: string, rows: readonly BrainEventRow[], seq: number) {
  return rebuildBrainModel(jobId, timelineSeedOf(TASKS), rows.filter((r) => r.seq <= seq));
}

function contiguous(count: number): BrainEventRow[] {
  return Array.from({ length: count }, (_, seq) => ({ seq, kind: "budget.tick", outcome: "", taskId: "" }));
}

describe("the prefix-equality property", () => {
  it("equals a fresh reduction at fuzzed positions, at the spec's spacing", () => {
    for (let ledger = 1; ledger <= 12; ledger += 1) {
      const rows = fuzzLedger(ledger, 150 + ledger * 60);
      const memo = createScrubMemo("job-f", TASKS);
      memo.append(rows);
      const last = memo.lastSeq() as number;
      const next = generator(ledger * 7919);
      const positions = [-1, 0, last, last + 5, ...Array.from({ length: 25 }, () => Math.floor(next() * (last + 1)))];
      for (const s of positions) {
        expect(memo.stateAt(s)).toEqual(fresh("job-f", rows, s));
      }
    }
  });

  it("holds under a tight spacing and cap, queried in random order", () => {
    for (let ledger = 20; ledger < 26; ledger += 1) {
      const rows = fuzzLedger(ledger, 120);
      const memo = createScrubMemo("job-t", TASKS, { every: 5, cap: 3 });
      memo.append(rows);
      const last = memo.lastSeq() as number;
      const next = generator(ledger);
      for (let q = 0; q < 40; q += 1) {
        const s = Math.floor(next() * (last + 2)) - 1;
        expect(memo.stateAt(s)).toEqual(fresh("job-t", rows, s));
        expect(memo.stats().snapshots.length).toBeLessThanOrEqual(3);
      }
    }
  });

  it("holds while the ledger grows live, one page at a time", () => {
    const rows = fuzzLedger(31, 400);
    const ordered = [...rows].sort((a, b) => a.seq - b.seq);
    const memo = createScrubMemo("job-l", TASKS, { every: 20 });
    for (let start = 0; start < ordered.length; start += 50) {
      memo.append(ordered.slice(start, start + 50));
      const head = memo.lastSeq() as number;
      expect(memo.stateAt(head)).toEqual(fresh("job-l", rows, head));
      expect(memo.stateAt(Math.floor(head / 2))).toEqual(fresh("job-l", rows, Math.floor(head / 2)));
    }
  });

  it("scrubs the demo recording to exactly its prefixes", () => {
    const tasks: BrainTaskSeed[] = [
      { id: "a7a8f67f1b9a4814", status: "pending", rank: 0 },
      { id: "1965fb3f26b64fe7", status: "pending", rank: 1 },
    ];
    const memo = createScrubMemo(BRAIN_DEMO_JOB_ID, tasks, { every: 3 });
    memo.append(brainDemoRows());
    for (let s = -1; s <= 7; s += 1) {
      expect(memo.stateAt(s)).toEqual(
        rebuildBrainModel(BRAIN_DEMO_JOB_ID, tasks, brainDemoRows().filter((r) => r.seq <= s)),
      );
    }
  });
});

describe("the snapshot arithmetic", () => {
  it("spaces snapshots 200 seq apart and keeps at most 64", () => {
    expect(SNAPSHOT_EVERY).toBe(200);
    expect(SNAPSHOT_CAP).toBe(64);
  });

  it("builds each boundary once and then serves any position with at most 199 reductions", () => {
    const memo = createScrubMemo("job-a", TASKS);
    memo.append(contiguous(1000));
    memo.stateAt(999);
    expect(memo.stats()).toEqual({ snapshots: [200, 400, 600, 800, 1000], reductions: 1000 });
    for (const [s, cost] of [[999, 0], [998, 199], [0, 1], [199, 0], [200, 1], [650, 51], [-1, 0]]) {
      const before = memo.stats().reductions;
      memo.stateAt(s);
      expect(memo.stats().reductions - before).toBe(cost);
    }
    expect(memo.stats().snapshots).toEqual([200, 400, 600, 800, 1000]);
  });

  it("drops the snapshots farthest from the position served, the lower one on a tie", () => {
    const memo = createScrubMemo("job-e", TASKS, { every: 10, cap: 2 });
    memo.append(contiguous(60));
    memo.stateAt(59);
    expect(memo.stats().snapshots).toEqual([50, 60]);
    memo.stateAt(35);
    expect(memo.stats().snapshots).toEqual([30, 50]);
    expect(memo.stats().reductions).toBe(60 + 30 + 6);
  });

  it("rebuilds a dropped snapshot from the nearest lower one it kept", () => {
    const memo = createScrubMemo("job-b", TASKS, { every: 10, cap: 2 });
    memo.append(contiguous(60));
    memo.stateAt(25);
    expect(memo.stats().snapshots).toEqual([10, 20]);
    const before = memo.stats().reductions;
    memo.stateAt(45);
    expect(memo.stats().snapshots).toEqual([30, 40]);
    expect(memo.stats().reductions - before).toBe(20 + 6);
  });
});

describe("ingestion and invalidation", () => {
  it("serves the timeline seed before the first row, never today's statuses", () => {
    const memo = createScrubMemo("job-s", TASKS);
    expect(memo.lastSeq()).toBeNull();
    expect(memo.stateAt(-1)).toEqual(seedBrainModel("job-s", timelineSeedOf(TASKS)));
    expect(memo.stateAt(-1).nodes.map((n) => n.state)).toEqual(["planned", "planned", "planned", "planned"]);
  });

  it("keeps the first row of a repeated seq, across appends", () => {
    const memo = createScrubMemo("job-d", TASKS);
    memo.append([{ seq: 0, kind: "task_run_started", outcome: "", taskId: "t1" }]);
    memo.append([{ seq: 0, kind: "job_stopped", outcome: "stopped", taskId: "" }]);
    expect(memo.stateAt(0)).toEqual(
      rebuildBrainModel("job-d", timelineSeedOf(TASKS), [{ seq: 0, kind: "task_run_started", outcome: "", taskId: "t1" }]),
    );
  });

  it("keeps every snapshot when the ledger grows at its head", () => {
    const memo = createScrubMemo("job-h", TASKS, { every: 10 });
    memo.append(contiguous(40));
    memo.stateAt(39);
    memo.append([{ seq: 40, kind: "task_run_started", outcome: "", taskId: "t2" }]);
    expect(memo.stats().snapshots).toEqual([10, 20, 30, 40]);
  });

  it("drops the snapshots above a gap-filling row and stays equal to a fresh fold", () => {
    const rows = contiguous(40).filter((r) => r.seq !== 17);
    const memo = createScrubMemo("job-g", TASKS, { every: 10 });
    memo.append(rows);
    memo.stateAt(39);
    const late = { seq: 17, kind: "task_run_started", outcome: "", taskId: "t3" };
    memo.append([late]);
    expect(memo.stats().snapshots).toEqual([10]);
    expect(memo.stateAt(39)).toEqual(fresh("job-g", [...rows, late], 39));
  });

  it("drops the snapshots a query beyond the head built once the head moves past them", () => {
    const memo = createScrubMemo("job-p", TASKS, { every: 10 });
    memo.append(contiguous(25));
    memo.stateAt(44);
    expect(memo.stats().snapshots).toEqual([10, 20, 30, 40]);
    const late = { seq: 25, kind: "task_run_started", outcome: "", taskId: "t1" };
    memo.append([late]);
    expect(memo.stats().snapshots).toEqual([10, 20]);
    expect(memo.stateAt(44)).toEqual(fresh("job-p", [...contiguous(25), late], 44));
  });

  it("forgets every snapshot on a snapshot-refetch reset and rebuilds lazily", () => {
    const memo = createScrubMemo("job-r", TASKS, { every: 10 });
    memo.append(contiguous(40));
    memo.stateAt(39);
    const refetched = fuzzLedger(41, 30);
    memo.reset(refetched);
    expect(memo.stats().snapshots).toEqual([]);
    const last = memo.lastSeq() as number;
    expect(memo.stateAt(last)).toEqual(fresh("job-r", refetched, last));
    memo.reset([]);
    expect(memo.stats().snapshots).toEqual([]);
    expect(memo.lastSeq()).toBeNull();
    expect(memo.stateAt(39)).toEqual(seedBrainModel("job-r", timelineSeedOf(TASKS)));
  });
});
