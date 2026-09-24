// Types and literal lookup tables the reducer counts on. This module owns
// NAMES ONLY: every mapping here is a table, never a branch, so a status or
// outcome word the platform adds later is a one-line edit here instead of a
// logic change in brainReducer.ts. The reducer owns existence and state; this
// file owns the vocabulary both the dashboard seed and the event stream speak.
// Design authority: docs/ui/design_reference/graph_spec.md §2 (ontology).

/** The shapes a brain-graph node can take. `repair_run`, `synapse` and
 *  `artifact` are named here for the lifecycle feature that will draw them;
 *  brainReducer.ts never births one of these three, because no Part E event
 *  name exists to birth them from and a `repair_*` frame carries no task id
 *  to attach a run to (measured, DECISION F019 D1). */
export type NodeKind =
  | "job_core"
  | "task"
  | "builder_run"
  | "review_run"
  | "repair_run"
  | "test_run"
  | "synapse"
  | "artifact"
  | "cluster";

/** The states a node can be drawn in. `open` and `vetoed` are named for the
 *  same forward reason as the unused NodeKind values above — this reducer
 *  never assigns them, a later feature will. */
export type NodeState = "open" | "planned" | "in_progress" | "pass" | "fail" | "blocked" | "vetoed";

/** One graph node. `seq` is the frame that birthed it, or 0 for a node the
 *  dashboard seed already knew about — the ordinal a client did not have to
 *  wait on a stream to learn. `meta` is a grab-bag by design: what it holds
 *  differs by kind (rank for a task, outcome for a run, a count for a
 *  cluster) and the reducer is the only reader that needs to know which. */
export interface BrainNode {
  id: string;
  kind: NodeKind;
  state: NodeState;
  parentId?: string;
  seq: number;
  meta: Record<string, unknown>;
}

/** One parent edge. `id` is derived from its two ends so two call sites
 *  building the same edge can never disagree about its identity. */
export interface BrainLink {
  id: string;
  source: string;
  target: string;
}

/** The reducer's own input shape. Declared so a `FeedRow` (apps/ui/src/api/
 *  feedRow.ts) is assignable to it STRUCTURALLY — `feedRowOf(frame, 0)`
 *  output feeds `reduceBrainEvent` with no adapter in between. */
export interface BrainEventRow {
  seq: number;
  kind: string;
  outcome: string;
  taskId: string;
}

/** One dashboard task as the seed step sees it, before any stream frame has
 *  said anything about it. `rank` is the task's index in job.tasks. */
export interface BrainTaskSeed {
  id: string;
  status: string;
  rank: number;
  title?: string;
}

/** The whole graph at one point in the ledger. `ignored` is a counted debug
 *  note, never rendered: a kind counted there is a frame this reducer chose
 *  not to map onto the graph, not a bug that swallowed it silently. */
export interface BrainModel {
  jobId: string;
  lastSeq: number | null;
  nodes: readonly BrainNode[];
  links: readonly BrainLink[];
  ignored: Readonly<Record<string, number>>;
}

/** Table 1 (DECISION F019 D1, graph_spec §2): the dashboard's own task-status
 *  words — drawn from both vocabularies the design cites, pingpong's and the
 *  CLI RunState's — mapped onto the node states this graph draws. A status
 *  missing from this table is not an error: the reducer falls back to
 *  `planned` and keeps the raw word in `meta.status` (Table 1's own "ANY
 *  other value" row), so this table only needs to list the WELL-KNOWN ones. */
export const SEED_STATUS_STATE_TABLE: Readonly<Record<string, NodeState>> = {
  pending: "planned",
  planned: "planned",
  running: "in_progress",
  active: "in_progress",
  passed: "pass",
  completed: "pass",
  applied_to_job_workspace: "pass",
  failed: "fail",
  blocked: "blocked",
};

/** The review-outcome half of Table 2 (DECISION F019 D1): `task_round_completed`'s
 *  outcome word decides the born review_run's state. `needs_repair` folds
 *  into `fail` — a round that needs repair did not pass — and any outcome
 *  this table has not seen (including a future reviewer verdict) falls back
 *  to `planned` rather than guessing pass or fail. */
export const REVIEW_OUTCOME_STATE_TABLE: Readonly<Record<string, NodeState>> = {
  pass: "pass",
  fail: "fail",
  needs_repair: "fail",
  blocked: "blocked",
};
