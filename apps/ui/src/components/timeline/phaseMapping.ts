// The phase timeline's own reading of the event ledger: which phase of the job
// the ledger has reached at a prefix, where each phase began, and which events
// earn a sub-glyph on the track. Everything here is a pure function of the rows
// it is given (DECISION F024 D1): no React, no DOM, no Date, no wall clock, so the
// scrubber can ask the same question of any prefix events[0..s] and get the same
// answer the live bar gave when the ledger ended there.
//
// Deliberate absences, measured at `1bb3a35d`: the ledger `events-since` serves
// carries none of the roadmap's Part E names and no plan-approval event, a
// `job run` writes no event when a job completes, and the tests a round runs
// write no event of their own. So the table below maps the MEASURED writers
// only, a phase the ledger skipped is reported with a zero span rather than
// invented, and Finalized is derived from the reducer's own task states instead
// of from a marker that does not exist.
import { humanizeStreamEvent } from "../../api/humanize";
import { REVIEW_OUTCOME_STATE_TABLE } from "../graph/brainOntology";
import type { BrainEventRow, BrainTaskSeed } from "../graph/brainOntology";
import { reduceBrainEvent, seedBrainModel } from "../graph/brainReducer";

/** The six stops of the bar, in order (ux_spec.md §12). */
export type TimelinePhase = "job" | "planning" | "build" | "test" | "review" | "finalized";

export const TIMELINE_PHASES: readonly TimelinePhase[] = [
  "job",
  "planning",
  "build",
  "test",
  "review",
  "finalized",
];

/** The phase mapping table: a ledger kind to the phase it marks as begun. The
 *  Job phase begins at the ledger's first row whatever its kind, and Finalized
 *  has no row of its own, so neither appears here. A kind absent from this table
 *  marks no phase. */
export const PHASE_MARKER_TABLE: Readonly<Record<string, TimelinePhase>> = {
  planning_started: "planning",
  planning_completed: "planning",
  planning_failed: "planning",
  task_run_started: "build",
  builder_started: "build",
  builder_completed: "build",
  test_run_requested: "test",
  test_run_started: "test",
  test_run_completed: "test",
  test_run_blocked: "test",
  test_run_timed_out: "test",
  verification_passed: "test",
  verification_failed: "test",
  task_round_completed: "review",
};

/** The events that earn a sub-glyph on the track (T5_F024.md Design). */
export type SubGlyphKind = "decision" | "failure" | "heal" | "stop";

/** The sub-glyph table for the kinds whose glyph the kind alone decides. A
 *  review round is decided by its verdict instead, in `subGlyphKindOf`. */
export const SUB_GLYPH_TABLE: Readonly<Record<string, SubGlyphKind>> = {
  task_needs_decision: "decision",
  task_decision_answered: "decision",
  task_run_failed: "failure",
  verification_failed: "failure",
  planning_failed: "failure",
  test_run_timed_out: "failure",
  cycle_healed: "heal",
  job_stopped: "stop",
};

/** One stop of the bar as a prefix reads it. `endSeq` is the seq at which the
 *  next reached phase began, or null for the phase the prefix ends in; a phase
 *  the ledger skipped has `startSeq === endSeq`, which the bar draws as a
 *  compact tick. */
export interface PhaseSpan {
  phase: TimelinePhase;
  startSeq: number;
  endSeq: number | null;
}

/** What a prefix says about the job's phases. `spans` holds every reached phase
 *  in bar order and nothing for a phase not reached; `lastSeq` is the prefix's
 *  last row, or null for an empty ledger. */
export interface PhaseReading {
  current: TimelinePhase;
  spans: readonly PhaseSpan[];
  lastSeq: number | null;
}

/** One mark on the track: the row's seq, its glyph, the raw kind and task it
 *  came from, and the humanized line its hover shows. */
export interface SubGlyph {
  seq: number;
  glyph: SubGlyphKind;
  kind: string;
  taskId: string;
  line: string;
}

function has(table: Readonly<Record<string, unknown>>, key: string): boolean {
  // hasOwnProperty, never a bare lookup: a kind named `toString` would
  // otherwise resolve against Object.prototype.
  return Object.prototype.hasOwnProperty.call(table, key);
}

/** The rows in seq order with a repeated seq kept once, the first one winning
 *  — the same normalisation `rebuildBrainModel` applies. */
export function orderedLedger(rows: readonly BrainEventRow[]): BrainEventRow[] {
  const bySeq = new Map<number, BrainEventRow>();
  for (const row of rows) {
    if (!bySeq.has(row.seq)) bySeq.set(row.seq, row);
  }
  return [...bySeq.values()].sort((a, b) => a.seq - b.seq);
}

/** The timeline's seed: the task list with every status reset to `pending`.
 *  The dashboard's list carries TODAY's statuses, and a scrubbed prefix seeded
 *  with them would show the end of the job at its start. */
export function timelineSeedOf(tasks: readonly BrainTaskSeed[]): BrainTaskSeed[] {
  return tasks.map((task) => ({ ...task, status: "pending" }));
}

/** The phase a row marks as begun, or null. A review round marks Review only
 *  when it carries a reviewer's verdict: `no_review` and an empty outcome mean
 *  no reviewer ran, which is also why the reducer births no review run for them. */
export function markerPhaseOf(row: BrainEventRow): TimelinePhase | null {
  if (!has(PHASE_MARKER_TABLE, row.kind)) return null;
  if (row.kind === "task_round_completed" && !has(REVIEW_OUTCOME_STATE_TABLE, row.outcome)) return null;
  return PHASE_MARKER_TABLE[row.kind];
}

const REVIEW_FAILED = new Set(["fail", "needs_repair"]);

/** The phases of the prefix `rows` ends at. A phase begins at the first row
 *  that marks it or any later phase, so the bar only ever moves forward and a
 *  skipped phase begins where the phase after it did. Finalized begins at the
 *  row after which every task in the reducer's model has passed, and is
 *  reached only while that still holds at the prefix's last row. */
export function readPhases(
  jobId: string,
  tasks: readonly BrainTaskSeed[],
  rows: readonly BrainEventRow[],
): PhaseReading {
  const ordered = orderedLedger(rows);
  if (ordered.length === 0) return { current: "job", spans: [], lastSeq: null };

  const reviewIndex = TIMELINE_PHASES.indexOf("review");
  const starts: (number | null)[] = TIMELINE_PHASES.map(() => null);
  starts[0] = ordered[0].seq;
  let reached = 0;
  let passSince: number | null = null;
  let model = seedBrainModel(jobId, timelineSeedOf(tasks));

  for (const row of ordered) {
    model = reduceBrainEvent(model, row);
    const marked = markerPhaseOf(row);
    const index = marked === null ? -1 : TIMELINE_PHASES.indexOf(marked);
    for (let p = reached + 1; p <= index; p += 1) starts[p] = row.seq;
    if (index > reached) reached = index;
    const allPassed = model.nodes[0].state === "pass";
    if (!allPassed) passSince = null;
    else if (passSince === null) passSince = row.seq;
  }

  if (passSince !== null) {
    const finalizedAt = Math.max(passSince, starts[reached] as number);
    for (let p = reached + 1; p <= reviewIndex + 1; p += 1) starts[p] = finalizedAt;
    reached = reviewIndex + 1;
  }

  const spans: PhaseSpan[] = [];
  for (let p = 0; p <= reached; p += 1) {
    spans.push({
      phase: TIMELINE_PHASES[p],
      startSeq: starts[p] as number,
      endSeq: p < reached ? (starts[p + 1] as number) : null,
    });
  }
  return { current: TIMELINE_PHASES[reached], spans, lastSeq: ordered[ordered.length - 1].seq };
}

/** The sub-glyphs of a prefix, in seq order. A review round that failed or
 *  asked for repair is a failure; the next round of the SAME task that passes
 *  is a heal. Every other kind is decided by SUB_GLYPH_TABLE alone. */
export function extractSubGlyphs(rows: readonly BrainEventRow[]): SubGlyph[] {
  const failedReview = new Set<string>();
  const glyphs: SubGlyph[] = [];
  for (const row of orderedLedger(rows)) {
    const glyph = subGlyphKindOf(row, failedReview);
    if (glyph === null) continue;
    glyphs.push({
      seq: row.seq,
      glyph,
      kind: row.kind,
      taskId: row.taskId,
      line: humanizeStreamEvent(row.kind).line,
    });
  }
  return glyphs;
}

function subGlyphKindOf(row: BrainEventRow, failedReview: Set<string>): SubGlyphKind | null {
  if (row.kind === "task_round_completed") {
    if (REVIEW_FAILED.has(row.outcome)) {
      failedReview.add(row.taskId);
      return "failure";
    }
    if (row.outcome === "pass" && failedReview.has(row.taskId)) {
      failedReview.delete(row.taskId);
      return "heal";
    }
    return null;
  }
  return has(SUB_GLYPH_TABLE, row.kind) ? SUB_GLYPH_TABLE[row.kind] : null;
}
