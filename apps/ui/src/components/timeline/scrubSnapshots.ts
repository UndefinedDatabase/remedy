// The scrubber's memory of the ledger: the reducer state at any seq s, served as
// one memoized snapshot plus at most SNAPSHOT_EVERY reductions (T5_F024.md T002,
// DECISION F024 D2). The state it returns is BY CONSTRUCTION the state a fresh
// fold of the prefix gives — `rebuildBrainModel` over the timeline seed and every
// row at or below s — and `scrubSnapshots.test.ts` holds it to that at fuzzed
// positions. No React, no DOM, no Date: the memo owns a cache and nothing else.
import type { BrainEventRow, BrainModel, BrainTaskSeed } from "../graph/brainOntology";
import { reduceBrainEvent, seedBrainModel } from "../graph/brainReducer";
import { timelineSeedOf } from "./phaseMapping";

/** Snapshot spacing in seq, the binding spec's figure (T5_F024.md, ROADMAP F024). */
export const SNAPSHOT_EVERY = 200;

/** The most snapshots one memo keeps. Beyond it the snapshot farthest from the
 *  position being served is dropped, and rebuilt from the nearest lower one if a
 *  later position needs it: instant beats infinite. */
export const SNAPSHOT_CAP = 64;

export interface ScrubMemoOptions {
  every?: number;
  cap?: number;
}

/** What a memo holds right now: the seq boundary of every snapshot it keeps, in
 *  order, and how many rows it has reduced since it was made. */
export interface ScrubMemoStats {
  snapshots: number[];
  reductions: number;
}

export interface ScrubMemo {
  /** The last seq the memo holds, or null while its ledger is empty. */
  lastSeq(): number | null;
  /** Live ingestion. A row whose seq the memo already holds is dropped (the first
   *  one wins); a new row drops every snapshot that should have contained it,
   *  which at the head of the ledger is none and after a gap is every one above it. */
  append(rows: readonly BrainEventRow[]): void;
  /** The snapshot-refetch reset of gap recovery: the ledger is replaced and every
   *  snapshot dropped, to be rebuilt lazily. */
  reset(rows: readonly BrainEventRow[]): void;
  /** The reducer state after every row at or below `seq`. */
  stateAt(seq: number): BrainModel;
  stats(): ScrubMemoStats;
}

/** A memo over one job's ledger, seeded like the timeline: today's task list with
 *  every status reset to pending. A snapshot at boundary b is the state after
 *  every row whose seq is below b, for b a positive multiple of `every`. */
export function createScrubMemo(
  jobId: string,
  tasks: readonly BrainTaskSeed[],
  options: ScrubMemoOptions = {},
): ScrubMemo {
  const every = options.every ?? SNAPSHOT_EVERY;
  const cap = options.cap ?? SNAPSHOT_CAP;
  const seed = seedBrainModel(jobId, timelineSeedOf(tasks));
  let rows: BrainEventRow[] = [];
  const snapshots = new Map<number, BrainModel>();
  let reductions = 0;

  // The index of the first row whose seq is at least `seq`.
  function lowerBound(seq: number): number {
    let lo = 0;
    let hi = rows.length;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (rows[mid].seq < seq) lo = mid + 1;
      else hi = mid;
    }
    return lo;
  }

  // Fold every row with from <= seq < to onto `model`.
  function fold(model: BrainModel, from: number, to: number): BrainModel {
    let next = model;
    for (let i = lowerBound(from); i < rows.length && rows[i].seq < to; i += 1) {
      next = reduceBrainEvent(next, rows[i]);
      reductions += 1;
    }
    return next;
  }

  // Keep at most `cap` snapshots, dropping the farthest from `anchor` first and,
  // between two equally far, the lower one.
  function evict(anchor: number): void {
    while (snapshots.size > cap) {
      let victim = -1;
      let distance = -1;
      for (const boundary of [...snapshots.keys()].sort((a, b) => a - b)) {
        const d = Math.abs(boundary - anchor);
        if (d > distance) {
          victim = boundary;
          distance = d;
        }
      }
      snapshots.delete(victim);
    }
  }

  // The snapshot at `boundary`, built from the nearest lower one it can find.
  function snapshotAt(boundary: number, anchor: number): BrainModel {
    if (boundary <= 0) return seed;
    const kept = snapshots.get(boundary);
    if (kept) return kept;
    let base = boundary - every;
    while (base > 0 && !snapshots.has(base)) base -= every;
    let model = base > 0 ? (snapshots.get(base) as BrainModel) : seed;
    for (let b = Math.max(base, 0) + every; b <= boundary; b += every) {
      model = fold(model, b - every, b);
      snapshots.set(b, model);
      evict(anchor);
    }
    return model;
  }

  function add(incoming: readonly BrainEventRow[]): void {
    const held = new Set(rows.map((r) => r.seq));
    let lowest: number | null = null;
    const fresh: BrainEventRow[] = [];
    for (const row of incoming) {
      if (held.has(row.seq)) continue;
      held.add(row.seq);
      fresh.push(row);
      if (lowest === null || row.seq < lowest) lowest = row.seq;
    }
    if (lowest === null) return;
    rows = [...rows, ...fresh].sort((a, b) => a.seq - b.seq);
    for (const boundary of [...snapshots.keys()]) {
      if (boundary > lowest) snapshots.delete(boundary);
    }
  }

  return {
    lastSeq: () => (rows.length > 0 ? rows[rows.length - 1].seq : null),
    append: add,
    reset(next) {
      rows = [];
      snapshots.clear();
      add(next);
    },
    stateAt(seq) {
      const boundary = Math.floor((seq + 1) / every) * every;
      return fold(snapshotAt(boundary, seq), boundary, seq + 1);
    },
    stats: () => ({ snapshots: [...snapshots.keys()].sort((a, b) => a - b), reductions }),
  };
}
