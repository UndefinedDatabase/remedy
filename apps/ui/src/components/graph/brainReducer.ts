// The brain graph's own state machine. This module owns EXISTENCE and STATE
// — which nodes exist, which edges connect them, what state each is in — and
// nothing about how any of it is drawn: the lifecycle feature that renders
// this graph owns the visual language (color, layout, animation). No React,
// no DOM, no Date, no Math.random: every function here is pure and total.
//
// Deliberate absences (DECISION F019 D1, docs/ui/design_reference/graph_spec.md §8):
// none of the roadmap's Part E event names (`run.started`, `plan.task_created`,
// ...) is emitted by the server, so Table 2 below dispatches on the MEASURED
// writers only. No event-schema change is made or assumed — the event schema
// is on the feature's do-not-touch list. No plan-approval event exists, so
// the task ring this reducer draws is born from the dashboard SEED, never
// from a stream frame of its own.
import {
  REVIEW_OUTCOME_STATE_TABLE,
  SEED_STATUS_STATE_TABLE,
} from "./brainOntology";
import type {
  BrainEventRow,
  BrainLink,
  BrainModel,
  BrainNode,
  BrainTaskSeed,
  NodeKind,
  NodeState,
} from "./brainOntology";

// --- id scheme (DECISION F019 D1 "Node ids") --------------------------------

function coreNodeId(jobId: string): string {
  return `job:${jobId}`;
}
function taskNodeId(taskId: string): string {
  return `task:${taskId}`;
}
function runNodeId(taskId: string, seq: number): string {
  return `run:${taskId}:${seq}`;
}
function clusterNodeId(taskId: string): string {
  return `cluster:${taskId}`;
}
function linkFor(parentId: string, childId: string): BrainLink {
  return { id: `${parentId}->${childId}`, source: parentId, target: childId };
}

// The kinds `runNodeId`, core derivation, open-run search and clustering all
// treat as one family: any node of these kinds is "a run" (DECISION F019 D1).
const RUN_KINDS: readonly NodeKind[] = ["builder_run", "review_run", "repair_run", "test_run"];
function isRunKind(kind: NodeKind): boolean {
  return RUN_KINDS.includes(kind);
}

// --- core-state derivation ---------------------------------------------------

/** Core state is never stored from a frame, only derived from the nodes that
 *  exist right now: an active run always wins, a failed or blocked task beats
 *  a merely-incomplete one, and "pass" requires every task to agree. */
function deriveCoreState(nodes: readonly BrainNode[]): NodeState {
  const tasks = nodes.filter((n) => n.kind === "task");
  const runs = nodes.filter((n) => isRunKind(n.kind));
  if (runs.some((r) => r.state === "in_progress")) return "in_progress";
  if (tasks.some((t) => t.state === "fail" || t.state === "blocked")) return "fail";
  if (tasks.length > 0 && tasks.every((t) => t.state === "pass")) return "pass";
  return "planned";
}

/** Re-stamps the core node with its derived state, returning the SAME model
 *  object when nothing changed — the identity a replayed row's early return
 *  depends on. */
function withDerivedCore(model: BrainModel): BrainModel {
  const derived = deriveCoreState(model.nodes);
  const core = model.nodes[0];
  if (core.state === derived) return model;
  const nextCore: BrainNode = { ...core, state: derived };
  return { ...model, nodes: [nextCore, ...model.nodes.slice(1)] };
}

// --- shared node surgery ------------------------------------------------------

function birthTask(
  nodes: readonly BrainNode[],
  links: readonly BrainLink[],
  taskId: string,
  seq: number,
): { nodes: BrainNode[]; links: BrainLink[] } {
  const id = taskNodeId(taskId);
  if (nodes.some((n) => n.id === id)) return { nodes: [...nodes], links: [...links] };
  const coreId = nodes[0].id;
  const highestRank = nodes.reduce(
    (max, n) => (n.kind === "task" ? Math.max(max, n.meta.rank as number) : max),
    -1,
  );
  const born: BrainNode = {
    id, kind: "task", state: "planned", parentId: coreId, seq, meta: { rank: highestRank + 1 },
  };
  return { nodes: [...nodes, born], links: [...links, linkFor(coreId, id)] };
}

/** "an open run" (DECISION F019 D1): the task's most recent run-kind child still in
 *  state in_progress, of any run kind. Only a builder_run is ever born in
 *  this state, but the search stays generic because that is how the design
 *  itself defines the term. */
function openRunOfKind(nodes: readonly BrainNode[], taskId: string, kind: NodeKind): BrainNode | undefined {
  const parent = taskNodeId(taskId);
  return nodes
    .filter((n) => n.kind === kind && n.parentId === parent && n.state === "in_progress")
    .reduce<BrainNode | undefined>((latest, n) => (!latest || n.seq > latest.seq ? n : latest), undefined);
}

function hasOpenRun(nodes: readonly BrainNode[], taskId: string): boolean {
  const parent = taskNodeId(taskId);
  return nodes.some((n) => isRunKind(n.kind) && n.parentId === parent && n.state === "in_progress");
}

function closeOpenRuns(nodes: readonly BrainNode[], taskId: string): BrainNode[] {
  const parent = taskNodeId(taskId);
  return nodes.map((n) =>
    isRunKind(n.kind) && n.parentId === parent && n.state === "in_progress"
      ? { ...n, state: "blocked" as NodeState }
      : n,
  );
}

function setTaskState(nodes: readonly BrainNode[], taskId: string, state: NodeState): BrainNode[] {
  const id = taskNodeId(taskId);
  return nodes.map((n) => (n.id === id ? { ...n, state } : n));
}

function ignoreRow(model: BrainModel, row: BrainEventRow): BrainModel {
  const count = (model.ignored[row.kind] ?? 0) + 1;
  return { ...model, ignored: { ...model.ignored, [row.kind]: count } };
}

// --- Table 2 (DECISION F019 D1): frame kind -> effect ------------------------

function onTaskRunStarted(model: BrainModel, row: BrainEventRow): BrainModel {
  const born = birthTask(model.nodes, model.links, row.taskId, row.seq);
  const closed = closeOpenRuns(born.nodes, row.taskId);
  const runId = runNodeId(row.taskId, row.seq);
  const withRun: BrainNode[] = [
    ...closed,
    { id: runId, kind: "builder_run", state: "in_progress", parentId: taskNodeId(row.taskId), seq: row.seq, meta: {} },
  ];
  const nodes = setTaskState(withRun, row.taskId, "in_progress");
  const links = [...born.links, linkFor(taskNodeId(row.taskId), runId)];
  return { ...model, nodes, links };
}

function onTaskRoundCompleted(model: BrainModel, row: BrainEventRow): BrainModel {
  const born = birthTask(model.nodes, model.links, row.taskId, row.seq);
  const runId = runNodeId(row.taskId, row.seq);
  const state = REVIEW_OUTCOME_STATE_TABLE[row.outcome] ?? "planned";
  const nodes: BrainNode[] = [
    ...born.nodes,
    { id: runId, kind: "review_run", state, parentId: taskNodeId(row.taskId), seq: row.seq, meta: { outcome: row.outcome } },
  ];
  const links = [...born.links, linkFor(taskNodeId(row.taskId), runId)];
  return { ...model, nodes, links };
}

function onVerification(model: BrainModel, row: BrainEventRow, state: "pass" | "fail"): BrainModel {
  const born = birthTask(model.nodes, model.links, row.taskId, row.seq);
  const runId = runNodeId(row.taskId, row.seq);
  const nodes: BrainNode[] = [
    ...born.nodes,
    { id: runId, kind: "test_run", state, parentId: taskNodeId(row.taskId), seq: row.seq, meta: { outcome: row.outcome } },
  ];
  const links = [...born.links, linkFor(taskNodeId(row.taskId), runId)];
  return { ...model, nodes, links };
}

function onTaskRunClosed(model: BrainModel, row: BrainEventRow, state: "pass" | "fail"): BrainModel {
  const born = birthTask(model.nodes, model.links, row.taskId, row.seq);
  const open = openRunOfKind(born.nodes, row.taskId, "builder_run");
  const withRun = open
    ? born.nodes.map((n) => (n.id === open.id ? { ...n, state, meta: { ...n.meta, outcome: row.outcome } } : n))
    : born.nodes;
  const nodes = setTaskState(withRun, row.taskId, state);
  return { ...model, nodes, links: born.links };
}

function onTaskRunNoop(model: BrainModel, row: BrainEventRow): BrainModel {
  // No "birth task" here (DECISION F019 D1): a noop that names a task nobody has
  // seen yet leaves no trace, because nothing actually happened.
  const open = openRunOfKind(model.nodes, row.taskId, "builder_run");
  if (!open) return { ...model };
  const nodes = model.nodes.map((n) =>
    n.id === open.id ? { ...n, state: "pass" as NodeState, meta: { ...n.meta, outcome: row.outcome } } : n,
  );
  return { ...model, nodes };
}

function onTaskNeedsDecision(model: BrainModel, row: BrainEventRow): BrainModel {
  const born = birthTask(model.nodes, model.links, row.taskId, row.seq);
  const nodes = setTaskState(born.nodes, row.taskId, "blocked");
  return { ...model, nodes, links: born.links };
}

function onTaskDecisionAnswered(model: BrainModel, row: BrainEventRow): BrainModel {
  // No "birth task" here either: answering a decision presumes the question
  // (and the task that asked it) already exists.
  const nodes = setTaskState(model.nodes, row.taskId, hasOpenRun(model.nodes, row.taskId) ? "in_progress" : "planned");
  return { ...model, nodes };
}

function onJobStopped(model: BrainModel): BrainModel {
  const nodes = model.nodes.map((n) => {
    if (isRunKind(n.kind) && n.state === "in_progress") return { ...n, state: "blocked" as NodeState };
    if (n.kind === "task" && n.state === "in_progress") return { ...n, state: "planned" as NodeState };
    return n;
  });
  return { ...model, nodes };
}

function applyBrainEvent(model: BrainModel, row: BrainEventRow): BrainModel {
  switch (row.kind) {
    case "task_run_started":
      return row.taskId === "" ? ignoreRow(model, row) : onTaskRunStarted(model, row);
    case "task_round_completed":
      if (row.taskId === "") return ignoreRow(model, row);
      if (row.outcome === "no_review" || row.outcome === "") return ignoreRow(model, row);
      return onTaskRoundCompleted(model, row);
    case "verification_passed":
      return row.taskId === "" ? ignoreRow(model, row) : onVerification(model, row, "pass");
    case "verification_failed":
      return row.taskId === "" ? ignoreRow(model, row) : onVerification(model, row, "fail");
    case "task_run_completed":
      return row.taskId === "" ? ignoreRow(model, row) : onTaskRunClosed(model, row, "pass");
    case "task_run_failed":
      return row.taskId === "" ? ignoreRow(model, row) : onTaskRunClosed(model, row, "fail");
    case "task_run_noop":
      return row.taskId === "" ? ignoreRow(model, row) : onTaskRunNoop(model, row);
    case "task_needs_decision":
      return row.taskId === "" ? ignoreRow(model, row) : onTaskNeedsDecision(model, row);
    case "task_decision_answered":
      return row.taskId === "" ? ignoreRow(model, row) : onTaskDecisionAnswered(model, row);
    case "job_stopped":
      return onJobStopped(model);
    case "builder_started":
    case "builder_completed":
      // Measured writer, deliberately silent: the builder_run node is born
      // by task_run_started, not by either of these (DECISION F019 D1), and unlike
      // an unhandled kind these are NOT counted in `ignored`.
      return model;
    default:
      return ignoreRow(model, row);
  }
}

// --- public surface ------------------------------------------------------

/** A job with no seed and no stream yet: the core exists, nothing else does. */
export function emptyBrainModel(jobId: string): BrainModel {
  const core: BrainNode = { id: coreNodeId(jobId), kind: "job_core", state: "planned", seq: 0, meta: {} };
  return { jobId, lastSeq: null, nodes: [core], links: [], ignored: {} };
}

/** The dashboard's own task list turned into the graph's starting shape —
 *  before this a client has a job id and nothing to draw. Seeded nodes carry
 *  seq 0 and are ordered by rank then id, matching job.tasks order. */
export function seedBrainModel(jobId: string, tasks: readonly BrainTaskSeed[]): BrainModel {
  const core: BrainNode = { id: coreNodeId(jobId), kind: "job_core", state: "planned", seq: 0, meta: {} };
  const ordered = [...tasks].sort((a, b) => a.rank - b.rank || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
  const nodes: BrainNode[] = [core];
  const links: BrainLink[] = [];
  for (const seed of ordered) {
    const id = taskNodeId(seed.id);
    const meta: Record<string, unknown> = { rank: seed.rank };
    if (seed.title !== undefined) meta.title = seed.title;
    meta.status = seed.status;
    const state = SEED_STATUS_STATE_TABLE[seed.status] ?? "planned";
    nodes.push({ id, kind: "task", state, parentId: core.id, seq: 0, meta });
    links.push(linkFor(core.id, id));
  }
  return withDerivedCore({ jobId, lastSeq: null, nodes, links, ignored: {} });
}

/** One frame folded into the graph, or a no-op if the ledger already has it.
 *  PURE and IDEMPOTENT PER SEQ: a row at or behind `lastSeq` returns the SAME
 *  object — the guard a live client and a reconnect replay can share. */
export function reduceBrainEvent(model: BrainModel, row: BrainEventRow): BrainModel {
  if (model.lastSeq !== null && row.seq <= model.lastSeq) return model;
  const next = applyBrainEvent(model, row);
  return withDerivedCore({ ...next, lastSeq: row.seq });
}

/** The snapshot path: seed fresh, then replay the ledger in seq order with
 *  duplicate seqs dropped (first wins) — REPLACES live state rather than
 *  merging into it, which is what makes a gap ghost-free (graph_spec §8). */
export function rebuildBrainModel(
  jobId: string,
  tasks: readonly BrainTaskSeed[],
  rows: readonly BrainEventRow[],
): BrainModel {
  const bySeq = new Map<number, BrainEventRow>();
  for (const row of rows) {
    if (!bySeq.has(row.seq)) bySeq.set(row.seq, row);
  }
  const ordered = [...bySeq.values()].sort((a, b) => a.seq - b.seq);
  return ordered.reduce((model, row) => reduceBrainEvent(model, row), seedBrainModel(jobId, tasks));
}

/** A pure VIEW over a model: the model itself keeps every run, this collapses
 *  the excess into one summary node per task so a long-lived task does not
 *  grow the graph without bound (graph_spec §10). Every in_progress run is
 *  always kept; the rest of the budget goes to the most recent finished runs
 *  by seq. A model with no task over `threshold` is returned UNCHANGED (===). */
export function clusterBrainModel(model: BrainModel, threshold = 8): BrainModel {
  const taskNodes = model.nodes.filter((n) => n.kind === "task");
  const clustered = new Map<string, { dropIds: Set<string>; clusterNode: BrainNode }>();

  for (const task of taskNodes) {
    const runs = model.nodes.filter((n) => isRunKind(n.kind) && n.parentId === task.id);
    if (runs.length <= threshold) continue;
    const open = runs.filter((n) => n.state === "in_progress");
    const finished = runs.filter((n) => n.state !== "in_progress");
    const keepCount = Math.max(0, threshold - open.length);
    const keptFinishedIds = new Set(
      [...finished].sort((a, b) => b.seq - a.seq).slice(0, keepCount).map((n) => n.id),
    );
    const dropped = finished.filter((n) => !keptFinishedIds.has(n.id));
    if (dropped.length === 0) continue;
    const pass = dropped.filter((n) => n.state === "pass").length;
    const fail = dropped.filter((n) => n.state === "fail").length;
    const maxSeq = dropped.reduce((m, n) => Math.max(m, n.seq), 0);
    const state: NodeState = fail > 0 ? "fail" : pass === dropped.length ? "pass" : "blocked";
    const taskId = task.id.slice("task:".length);
    clustered.set(task.id, {
      dropIds: new Set(dropped.map((n) => n.id)),
      clusterNode: {
        id: clusterNodeId(taskId), kind: "cluster", state, parentId: task.id, seq: maxSeq,
        meta: { count: dropped.length, pass, fail },
      },
    });
  }

  if (clustered.size === 0) return model;

  const dropIds = new Set<string>();
  clustered.forEach((c) => c.dropIds.forEach((id) => dropIds.add(id)));

  const nodes: BrainNode[] = model.nodes.filter((n) => !dropIds.has(n.id));
  clustered.forEach((c, taskId) => {
    let lastIdx = -1;
    nodes.forEach((n, idx) => {
      if (n.parentId === taskId) lastIdx = idx;
    });
    nodes.splice(lastIdx + 1, 0, c.clusterNode);
  });

  const links: BrainLink[] = [];
  for (const n of nodes) {
    if (n.kind === "job_core") continue;
    if (n.kind === "cluster") {
      links.push(linkFor(n.parentId as string, n.id));
      continue;
    }
    const original = model.links.find((l) => l.target === n.id);
    if (original) links.push(original);
  }

  return withDerivedCore({ ...model, nodes, links });
}
