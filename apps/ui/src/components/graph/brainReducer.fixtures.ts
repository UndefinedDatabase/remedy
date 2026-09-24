// Fixture streams and their expected models, HAND-DERIVED from DECISION F019 D1's
// Table 1 / Table 2 rather than computed by the reducer — a golden that were
// computed by the code under test could never catch that code being wrong.
// Every model constant below is a literal object; brainReducer.test.ts diffs
// the reducer's actual output against these with `toEqual`.
import type { BrainStreamFrame } from "../../api/brainStream";
import type { BrainEventRow, BrainModel, BrainTaskSeed, NodeState } from "./brainOntology";

/** One event row, as the design's own test helper is named: seq and kind are
 *  required, taskId and outcome default to "" the way most ignored/global
 *  frames actually carry them. */
export function row(seq: number, kind: string, taskId = "", outcome = ""): BrainEventRow {
  return { seq, kind, outcome, taskId };
}

// --- Golden A: one task, happy path -----------------------------------------

export const GOLDEN_A_JOB_ID = "job-a";

export const GOLDEN_A_TASKS: readonly BrainTaskSeed[] = [
  { id: "t1", status: "pending", rank: 0 },
];

export const GOLDEN_A_ROWS: readonly BrainEventRow[] = [
  row(1, "task_run_started", "t1"),
  row(2, "task_round_completed", "t1", "pass"),
  row(3, "verification_passed", "t1", "pass"),
  row(4, "task_run_completed", "t1", "pass"),
];

/** The same four rows, as `packages/orchestration/ui_server.py`'s safe
 *  envelope actually shapes them, for the feedRowOf interop test. */
export const GOLDEN_A_FRAMES: readonly BrainStreamFrame[] = [
  { seq: 1, event: { seq: 1, event: "task_run_started", timestamp: "", outcome: "", task_id: "t1" } },
  { seq: 2, event: { seq: 2, event: "task_round_completed", timestamp: "", outcome: "pass", task_id: "t1" } },
  { seq: 3, event: { seq: 3, event: "verification_passed", timestamp: "", outcome: "pass", task_id: "t1" } },
  { seq: 4, event: { seq: 4, event: "task_run_completed", timestamp: "", outcome: "pass", task_id: "t1" } },
];

export const GOLDEN_A_MODEL: BrainModel = {
  jobId: GOLDEN_A_JOB_ID,
  lastSeq: 4,
  nodes: [
    { id: "job:job-a", kind: "job_core", state: "pass", seq: 0, meta: {} },
    { id: "task:t1", kind: "task", state: "pass", parentId: "job:job-a", seq: 0, meta: { rank: 0, status: "pending" } },
    { id: "run:t1:1", kind: "builder_run", state: "pass", parentId: "task:t1", seq: 1, meta: { outcome: "pass" } },
    { id: "run:t1:2", kind: "review_run", state: "pass", parentId: "task:t1", seq: 2, meta: { outcome: "pass" } },
    { id: "run:t1:3", kind: "test_run", state: "pass", parentId: "task:t1", seq: 3, meta: { outcome: "pass" } },
  ],
  links: [
    { id: "job:job-a->task:t1", source: "job:job-a", target: "task:t1" },
    { id: "task:t1->run:t1:1", source: "task:t1", target: "run:t1:1" },
    { id: "task:t1->run:t1:2", source: "task:t1", target: "run:t1:2" },
    { id: "task:t1->run:t1:3", source: "task:t1", target: "run:t1:3" },
  ],
  ignored: {},
};

// --- Golden B: repair and resume --------------------------------------------

export const GOLDEN_B_JOB_ID = "job-b";

export const GOLDEN_B_TASKS: readonly BrainTaskSeed[] = [
  { id: "t1", status: "pending", rank: 0 },
  { id: "t2", status: "pending", rank: 1 },
];

// t1: started, round fail, round needs_repair, job_stopped (interrupts the
// open builder_run), started again, round pass, completed.
// t2: started, then needs a decision (its builder_run stays open — DECISION F019 D1
// does not have task_needs_decision touch any run).
export const GOLDEN_B_ROWS: readonly BrainEventRow[] = [
  row(1, "task_run_started", "t1"),
  row(2, "task_round_completed", "t1", "fail"),
  row(3, "task_round_completed", "t1", "needs_repair"),
  row(4, "job_stopped", "", "stopped"),
  row(5, "task_run_started", "t1"),
  row(6, "task_round_completed", "t1", "pass"),
  row(7, "task_run_completed", "t1", "pass"),
  row(8, "task_run_started", "t2"),
  row(9, "task_needs_decision", "t2"),
];

export const GOLDEN_B_MODEL: BrainModel = {
  jobId: GOLDEN_B_JOB_ID,
  lastSeq: 9,
  nodes: [
    { id: "job:job-b", kind: "job_core", state: "in_progress", seq: 0, meta: {} },
    { id: "task:t1", kind: "task", state: "pass", parentId: "job:job-b", seq: 0, meta: { rank: 0, status: "pending" } },
    { id: "task:t2", kind: "task", state: "blocked", parentId: "job:job-b", seq: 0, meta: { rank: 1, status: "pending" } },
    { id: "run:t1:1", kind: "builder_run", state: "blocked", parentId: "task:t1", seq: 1, meta: {} },
    { id: "run:t1:2", kind: "review_run", state: "fail", parentId: "task:t1", seq: 2, meta: { outcome: "fail" } },
    { id: "run:t1:3", kind: "review_run", state: "fail", parentId: "task:t1", seq: 3, meta: { outcome: "needs_repair" } },
    { id: "run:t1:5", kind: "builder_run", state: "pass", parentId: "task:t1", seq: 5, meta: { outcome: "pass" } },
    { id: "run:t1:6", kind: "review_run", state: "pass", parentId: "task:t1", seq: 6, meta: { outcome: "pass" } },
    { id: "run:t2:8", kind: "builder_run", state: "in_progress", parentId: "task:t2", seq: 8, meta: {} },
  ],
  links: [
    { id: "job:job-b->task:t1", source: "job:job-b", target: "task:t1" },
    { id: "job:job-b->task:t2", source: "job:job-b", target: "task:t2" },
    { id: "task:t1->run:t1:1", source: "task:t1", target: "run:t1:1" },
    { id: "task:t1->run:t1:2", source: "task:t1", target: "run:t1:2" },
    { id: "task:t1->run:t1:3", source: "task:t1", target: "run:t1:3" },
    { id: "task:t1->run:t1:5", source: "task:t1", target: "run:t1:5" },
    { id: "task:t1->run:t1:6", source: "task:t1", target: "run:t1:6" },
    { id: "task:t2->run:t2:8", source: "task:t2", target: "run:t2:8" },
  ],
  ignored: {},
};

// --- Golden C: unseeded task and unknown kinds ------------------------------

export const GOLDEN_C_JOB_ID = "job-c";

export const GOLDEN_C_TASKS: readonly BrainTaskSeed[] = [];

export const GOLDEN_C_ROWS: readonly BrainEventRow[] = [
  row(1, "task_run_started", "tX"),
  row(2, "budget.tick"),
  row(3, "steering_message_consumed"),
  row(4, "made_up_kind_xyz"),
  row(5, "builder_started", "tX"),
];

export const GOLDEN_C_MODEL: BrainModel = {
  jobId: GOLDEN_C_JOB_ID,
  lastSeq: 5,
  nodes: [
    { id: "job:job-c", kind: "job_core", state: "in_progress", seq: 0, meta: {} },
    { id: "task:tX", kind: "task", state: "in_progress", parentId: "job:job-c", seq: 1, meta: { rank: 0 } },
    { id: "run:tX:1", kind: "builder_run", state: "in_progress", parentId: "task:tX", seq: 1, meta: {} },
  ],
  links: [
    { id: "job:job-c->task:tX", source: "job:job-c", target: "task:tX" },
    { id: "task:tX->run:tX:1", source: "task:tX", target: "run:tX:1" },
  ],
  // builder_started is absent here on purpose (DECISION F019 D1: NOT counted).
  ignored: { "budget.tick": 1, steering_message_consumed: 1, made_up_kind_xyz: 1 },
};

// --- Cluster fixture: 11 finished runs + 1 in_progress ----------------------
// threshold=8: keep the 1 in_progress run + the 7 most-recent FINISHED runs
// (seq 5,7,8,9,10,11,12); the 4 oldest finished runs (seq 1-4: pass, fail,
// pass, pass) collapse into one cluster node, count 4 / pass 3 / fail 1.

export const CLUSTER_INPUT_MODEL: BrainModel = {
  jobId: "job-cluster",
  lastSeq: 12,
  nodes: [
    { id: "job:job-cluster", kind: "job_core", state: "in_progress", seq: 0, meta: {} },
    { id: "task:t1", kind: "task", state: "in_progress", parentId: "job:job-cluster", seq: 0, meta: { rank: 0, status: "running" } },
    { id: "run:t1:1", kind: "builder_run", state: "pass", parentId: "task:t1", seq: 1, meta: { outcome: "pass" } },
    { id: "run:t1:2", kind: "builder_run", state: "fail", parentId: "task:t1", seq: 2, meta: { outcome: "fail" } },
    { id: "run:t1:3", kind: "review_run", state: "pass", parentId: "task:t1", seq: 3, meta: { outcome: "pass" } },
    { id: "run:t1:4", kind: "test_run", state: "pass", parentId: "task:t1", seq: 4, meta: { outcome: "pass" } },
    { id: "run:t1:5", kind: "review_run", state: "pass", parentId: "task:t1", seq: 5, meta: { outcome: "pass" } },
    { id: "run:t1:6", kind: "builder_run", state: "in_progress", parentId: "task:t1", seq: 6, meta: {} },
    { id: "run:t1:7", kind: "test_run", state: "pass", parentId: "task:t1", seq: 7, meta: { outcome: "pass" } },
    { id: "run:t1:8", kind: "builder_run", state: "pass", parentId: "task:t1", seq: 8, meta: { outcome: "pass" } },
    { id: "run:t1:9", kind: "review_run", state: "pass", parentId: "task:t1", seq: 9, meta: { outcome: "pass" } },
    { id: "run:t1:10", kind: "test_run", state: "pass", parentId: "task:t1", seq: 10, meta: { outcome: "pass" } },
    { id: "run:t1:11", kind: "builder_run", state: "pass", parentId: "task:t1", seq: 11, meta: { outcome: "pass" } },
    { id: "run:t1:12", kind: "review_run", state: "pass", parentId: "task:t1", seq: 12, meta: { outcome: "pass" } },
  ],
  links: [
    { id: "job:job-cluster->task:t1", source: "job:job-cluster", target: "task:t1" },
    { id: "task:t1->run:t1:1", source: "task:t1", target: "run:t1:1" },
    { id: "task:t1->run:t1:2", source: "task:t1", target: "run:t1:2" },
    { id: "task:t1->run:t1:3", source: "task:t1", target: "run:t1:3" },
    { id: "task:t1->run:t1:4", source: "task:t1", target: "run:t1:4" },
    { id: "task:t1->run:t1:5", source: "task:t1", target: "run:t1:5" },
    { id: "task:t1->run:t1:6", source: "task:t1", target: "run:t1:6" },
    { id: "task:t1->run:t1:7", source: "task:t1", target: "run:t1:7" },
    { id: "task:t1->run:t1:8", source: "task:t1", target: "run:t1:8" },
    { id: "task:t1->run:t1:9", source: "task:t1", target: "run:t1:9" },
    { id: "task:t1->run:t1:10", source: "task:t1", target: "run:t1:10" },
    { id: "task:t1->run:t1:11", source: "task:t1", target: "run:t1:11" },
    { id: "task:t1->run:t1:12", source: "task:t1", target: "run:t1:12" },
  ],
  ignored: {},
};

export const CLUSTER_EXPECTED_MODEL: BrainModel = {
  jobId: "job-cluster",
  lastSeq: 12,
  nodes: [
    { id: "job:job-cluster", kind: "job_core", state: "in_progress", seq: 0, meta: {} },
    { id: "task:t1", kind: "task", state: "in_progress", parentId: "job:job-cluster", seq: 0, meta: { rank: 0, status: "running" } },
    { id: "run:t1:5", kind: "review_run", state: "pass", parentId: "task:t1", seq: 5, meta: { outcome: "pass" } },
    { id: "run:t1:6", kind: "builder_run", state: "in_progress", parentId: "task:t1", seq: 6, meta: {} },
    { id: "run:t1:7", kind: "test_run", state: "pass", parentId: "task:t1", seq: 7, meta: { outcome: "pass" } },
    { id: "run:t1:8", kind: "builder_run", state: "pass", parentId: "task:t1", seq: 8, meta: { outcome: "pass" } },
    { id: "run:t1:9", kind: "review_run", state: "pass", parentId: "task:t1", seq: 9, meta: { outcome: "pass" } },
    { id: "run:t1:10", kind: "test_run", state: "pass", parentId: "task:t1", seq: 10, meta: { outcome: "pass" } },
    { id: "run:t1:11", kind: "builder_run", state: "pass", parentId: "task:t1", seq: 11, meta: { outcome: "pass" } },
    { id: "run:t1:12", kind: "review_run", state: "pass", parentId: "task:t1", seq: 12, meta: { outcome: "pass" } },
    { id: "cluster:t1", kind: "cluster", state: "fail", parentId: "task:t1", seq: 4, meta: { count: 4, pass: 3, fail: 1 } },
  ],
  links: [
    { id: "job:job-cluster->task:t1", source: "job:job-cluster", target: "task:t1" },
    { id: "task:t1->run:t1:5", source: "task:t1", target: "run:t1:5" },
    { id: "task:t1->run:t1:6", source: "task:t1", target: "run:t1:6" },
    { id: "task:t1->run:t1:7", source: "task:t1", target: "run:t1:7" },
    { id: "task:t1->run:t1:8", source: "task:t1", target: "run:t1:8" },
    { id: "task:t1->run:t1:9", source: "task:t1", target: "run:t1:9" },
    { id: "task:t1->run:t1:10", source: "task:t1", target: "run:t1:10" },
    { id: "task:t1->run:t1:11", source: "task:t1", target: "run:t1:11" },
    { id: "task:t1->run:t1:12", source: "task:t1", target: "run:t1:12" },
    { id: "task:t1->cluster:t1", source: "task:t1", target: "cluster:t1" },
  ],
  ignored: {},
};

// --- Table 1: every listed seed status, plus one unknown --------------------

export const SEED_STATUS_CASES: readonly (readonly [string, NodeState])[] = [
  ["pending", "planned"],
  ["planned", "planned"],
  ["running", "in_progress"],
  ["active", "in_progress"],
  ["passed", "pass"],
  ["completed", "pass"],
  ["applied_to_job_workspace", "pass"],
  ["failed", "fail"],
  ["blocked", "blocked"],
  ["totally_unheard_of_status", "planned"],
];
