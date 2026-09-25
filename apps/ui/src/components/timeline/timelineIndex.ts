// The bar's fast path: the phase reading of EVERY prefix of a ledger from one
// fold, so a scrubber dragged across thousands of events asks a lookup rather
// than a reduction (T5_F024.md T003, DECISION F024 D3). `phasesAt(index, s)` is
// held equal to `readPhases` over the rows at or below s — the plain fold in
// phaseMapping.ts, which stays the reference — by `timelineIndex.test.ts` at
// every position of fuzzed ledgers. No React, no DOM, no clock.
import type { BrainEventRow, BrainTaskSeed } from "../graph/brainOntology";
import { reduceBrainEvent, seedBrainModel } from "../graph/brainReducer";
import { markerPhaseOf, orderedLedger, TIMELINE_PHASES, timelineSeedOf } from "./phaseMapping";
import type { PhaseReading, PhaseSpan } from "./phaseMapping";

/** Per row of the ordered ledger: its seq, the furthest phase any row up to it
 *  marked, and the row after which every task has passed without a break, or
 *  null. `starts` holds where each marked phase began, Job to Review; a start
 *  is fixed the moment it is set, which is what makes it true of every prefix
 *  that reaches that phase. */
export interface TimelineIndex {
  seqs: readonly number[];
  reached: readonly number[];
  passSince: readonly (number | null)[];
  starts: readonly (number | null)[];
}

export function buildTimelineIndex(
  jobId: string,
  tasks: readonly BrainTaskSeed[],
  rows: readonly BrainEventRow[],
): TimelineIndex {
  const ordered = orderedLedger(rows);
  const starts: (number | null)[] = TIMELINE_PHASES.slice(0, -1).map(() => null);
  const seqs: number[] = [];
  const reached: number[] = [];
  const passSince: (number | null)[] = [];
  let high = 0;
  let since: number | null = null;
  let model = seedBrainModel(jobId, timelineSeedOf(tasks));
  for (const row of ordered) {
    if (seqs.length === 0) starts[0] = row.seq;
    model = reduceBrainEvent(model, row);
    const marked = markerPhaseOf(row);
    const index = marked === null ? -1 : TIMELINE_PHASES.indexOf(marked);
    for (let p = high + 1; p <= index; p += 1) starts[p] = row.seq;
    if (index > high) high = index;
    if (model.nodes[0].state !== "pass") since = null;
    else if (since === null) since = row.seq;
    seqs.push(row.seq);
    reached.push(high);
    passSince.push(since);
  }
  return { seqs, reached, passSince, starts };
}

/** The last seq the index holds, or null for an empty ledger. */
export function indexHead(index: TimelineIndex): number | null {
  return index.seqs.length > 0 ? index.seqs[index.seqs.length - 1] : null;
}

// The position of the last row whose seq is at or below `seq`, or -1.
function lastRowAtOrBelow(index: TimelineIndex, seq: number): number {
  let lo = 0;
  let hi = index.seqs.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (index.seqs[mid] <= seq) lo = mid + 1;
    else hi = mid;
  }
  return lo - 1;
}

/** The phases of the prefix that ends at `seq`: the rows at or below it. */
export function phasesAt(index: TimelineIndex, seq: number): PhaseReading {
  const at = lastRowAtOrBelow(index, seq);
  if (at < 0) return { current: "job", spans: [], lastSeq: null };
  let reached = index.reached[at];
  const starts: (number | null)[] = [...index.starts.slice(0, reached + 1), null];
  const since = index.passSince[at];
  if (since !== null) {
    const finalizedAt = Math.max(since, starts[reached] as number);
    for (let p = reached + 1; p < TIMELINE_PHASES.length; p += 1) starts[p] = finalizedAt;
    reached = TIMELINE_PHASES.length - 1;
  }
  const spans: PhaseSpan[] = [];
  for (let p = 0; p <= reached; p += 1) {
    spans.push({
      phase: TIMELINE_PHASES[p],
      startSeq: starts[p] as number,
      endSeq: p < reached ? (starts[p + 1] as number) : null,
    });
  }
  return { current: TIMELINE_PHASES[reached], spans, lastSeq: index.seqs[at] };
}

/** The distinct seqs at which a phase of the whole ledger begins, ascending:
 *  the stops Shift+Arrow steps between. */
export function phaseStops(index: TimelineIndex): number[] {
  const head = indexHead(index);
  if (head === null) return [];
  return [...new Set(phasesAt(index, head).spans.map((s) => s.startSeq))].sort((a, b) => a - b);
}
