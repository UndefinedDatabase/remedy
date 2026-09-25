// The performance fixture the stage-1 and stage-6 frame budgets are measured
// on (DECISION F019 D6; docs/ui/design_reference/acceptance_criteria.md §5:
// "60fps p95 at 200 nodes (Stage-1+) and 500 nodes (Stage-6 gate) on the perf
// fixture trace"). The stage-1 frame-rate trace that docs/roadmap/features/
// T5_F044.md's T003 builds measures this fixture, as the line DECISION
// F019 D6 adds to that file says.
//
// Built through the REAL path (`seedBrainModel` + `reduceBrainEvent` over
// generated rows), the same reducer the live graph runs — never a hand-built
// `BrainModel` literal, so a reducer bug shows up here too.
import { reduceBrainEvent, seedBrainModel } from "./brainReducer";
import type { BrainEventRow, BrainModel, BrainTaskSeed } from "./brainOntology";

/** Stage-1 node target (acceptance_criteria.md §5, "60fps p95 at 200 nodes
 *  (Stage-1+)"). */
export const BRAIN_PERF_STAGE1_NODES = 200;
/** Stage-6 node target (acceptance_criteria.md §5, "...and 500 nodes
 *  (Stage-6 gate)"). */
export const BRAIN_PERF_STAGE6_NODES = 500;

/** Rounds every "normal" task runs (builder round -> review round, repeated).
 *  Chosen at 3 so a normal task's child count (2*3+1 = 7, or 2*3-1 = 5 for a
 *  task left open — see the arithmetic below) always stays UNDER
 *  clusterBrainModel's default 8-run threshold: clustering never fires in
 *  this fixture, so `buildBrainLayout(...).nodes.length` is exactly
 *  1 (core) + tasks + their (uncollapsed) children, nothing more to "mind". */
const ROUNDS_PER_TASK = 3;

interface StageConfig {
  /** Tasks that run ROUNDS_PER_TASK real builder/review rounds. */
  readonly normalCount: number;
  /** Tasks that are seeded but never started (zero rows) — see the
   *  arithmetic below for why a handful of these are required. */
  readonly bareCount: number;
}

// --- the arithmetic (why a target node count needs BOTH a task count and a
// handful of "bare" tasks, not task count alone) ---------------------------
//
// Every node buildBrainLayout draws is: 1 job_core, one node per seeded task,
// plus that task's run/review/verification children (clusterBrainModel only
// ever COLLAPSES excess children into a single cluster node, never adds one
// — and per the ROUNDS_PER_TASK comment above it never even fires here).
//
// A "normal" task's own child count is always ODD:
//   not left open:  2*ROUNDS_PER_TASK + 1 = 7   (a builder_run + review_run
//                                                 pair per round, +1 test_run
//                                                 from verification_passed)
//   left open:      2*ROUNDS_PER_TASK - 1 = 5   (the last round's review_run
//                                                 is skipped, its builder_run
//                                                 stays in_progress — this is
//                                                 the "every fifth task's
//                                                 last builder run is left in
//                                                 progress" active link)
// A task node (1, always present via the seed) plus an odd child count is
// always EVEN — true for ANY roundsPerTask or leaveOpen choice, since the
// child count's parity never depends on either. So N normal tasks always
// contribute an EVEN total; add the 1 job_core node (always present, itself
// odd) and core + N normal tasks is always ODD, structurally, no matter what
// N or ROUNDS_PER_TASK is — an even target like 200 or 500 can NEVER be hit
// by normal tasks alone.
//
// The fix is a handful of "bare" tasks: seeded (so each still gets a task
// node) but given ZERO rows, so each contributes EXACTLY 1 node — the only
// way to add an ODD contribution and flip the grand total's parity to EVEN.
// A bare task reads as "planned but not yet started", an ordinary job shape,
// not a synthetic trick.
//
//   total(N, L, B) = 1                                    (job_core)
//                  + N                                    (normal task nodes)
//                  + [ (N - L) * 7 + L * 5 ]               (their children)
//                  + B                                     (bare task nodes)
//                  = 1 + 8N - 2L + B
//
// leaveOpen is "every fifth task" (t % 5 === 0 among the N normal tasks,
// 0-indexed), so L = floor((N - 1) / 5) + 1:
//   N=26 -> L=6  (t=0,5,10,15,20,25): 1 + 8*26 - 2*6  = 197, + B=3 -> 200
//   N=65 -> L=13 (t=0,5,...,60):      1 + 8*65 - 2*13 = 495, + B=5 -> 500
const STAGE_CONFIG: Readonly<Record<number, StageConfig>> = {
  [BRAIN_PERF_STAGE1_NODES]: { normalCount: 26, bareCount: 3 },
  [BRAIN_PERF_STAGE6_NODES]: { normalCount: 65, bareCount: 5 },
};

function row(seq: number, kind: string, taskId = "", outcome = ""): BrainEventRow {
  return { seq, kind, outcome, taskId };
}

/** Generates the seeds (every task, normal and bare) and the rows (normal
 *  tasks only) for one stage config. `seq` starts at 0, not 1: the fixture's
 *  own test pins `model.lastSeq === rows.length - 1`, which only holds when
 *  the first row's seq is 0 (the same convention `events-since` cursor 0
 *  uses for "nothing read yet"). */
function buildRowsAndSeeds(
  normalCount: number,
  bareCount: number,
  roundsPerTask: number,
): { seeds: BrainTaskSeed[]; rows: BrainEventRow[] } {
  const total = normalCount + bareCount;
  const seeds: BrainTaskSeed[] = [];
  for (let t = 0; t < total; t++) {
    seeds.push({ id: `t${t}`, status: "pending", rank: t });
  }

  const rows: BrainEventRow[] = [];
  let seq = 0;
  for (let t = 0; t < normalCount; t++) {
    const taskId = `t${t}`;
    const leaveOpen = t % 5 === 0;
    for (let r = 0; r < roundsPerTask; r++) {
      const isLast = r === roundsPerTask - 1;
      rows.push(row(seq++, "task_run_started", taskId));
      if (isLast && leaveOpen) continue;
      const outcome = r % 3 === 1 ? "fail" : "pass";
      rows.push(row(seq++, "task_round_completed", taskId, outcome));
    }
    if (!leaveOpen) {
      rows.push(row(seq++, "verification_passed", taskId, "pass"));
      rows.push(row(seq++, "task_run_completed", taskId, "pass"));
    }
  }
  // Bare tasks (t in [normalCount, total)) are seeded above but never get a
  // row: still "pending", the parity fix the module header explains.
  return { seeds, rows };
}

/** Builds a deterministic `BrainModel` through the real reducer path such
 *  that `buildBrainLayout(brainPerfModel(n)).nodes.length === n` EXACTLY, for
 *  `n` in { BRAIN_PERF_STAGE1_NODES, BRAIN_PERF_STAGE6_NODES }. Pure and
 *  total for those two targets; throws for any other value rather than
 *  silently returning an off-target model a CI budget stage could
 *  misinterpret. */
export function brainPerfModel(nodeTarget: number): BrainModel {
  const { seeds, rows } = brainPerfLedger(nodeTarget);
  let model = seedBrainModel(`perf-${nodeTarget}`, seeds);
  for (const r of rows) model = reduceBrainEvent(model, r);
  return model;
}

/** The seeds and the ledger `brainPerfModel` folds, for a reader that needs
 *  the events rather than their end state: the phase timeline's scrub budget
 *  replays this ledger at every position (DECISION F024 D5). Throws for an
 *  unsupported target exactly as `brainPerfModel` does. */
export function brainPerfLedger(nodeTarget: number): { seeds: BrainTaskSeed[]; rows: BrainEventRow[] } {
  const config = STAGE_CONFIG[nodeTarget];
  if (!config) {
    throw new Error(
      `brainPerfModel: no fixture config for node target ${nodeTarget} ` +
        `(only ${BRAIN_PERF_STAGE1_NODES} and ${BRAIN_PERF_STAGE6_NODES} are supported)`,
    );
  }
  return buildRowsAndSeeds(config.normalCount, config.bareCount, ROUNDS_PER_TASK);
}
