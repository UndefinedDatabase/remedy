// Owns the glue between the dashboard, the reducer's layout and the stage —
// pure: no React, no DOM. `BrainGraphStage.tsx` and `ForceBrainGraph.tsx` both
// need this glue and neither should have to re-derive it (DECISION F019 D3).
import type { RemedyState, RemedyTaskItem } from "../../api/types";
import type { BrainTaskSeed, NodeState } from "./brainOntology";
import type { BrainLayoutData, BrainLayoutNode } from "./forceBrainTypes";
import type { GraphFilter } from "./GraphFilterChips";

/** Table 1 bridge (DECISION F019 D1, graph_spec.md §2): the dashboard's own
 *  task-state words mapped onto the seed-status words `SEED_STATUS_STATE_TABLE`
 *  (brainOntology.ts) reads. `suggested` has no row in that table, so it falls
 *  back to `planned` with the raw word kept in the seeded node's `meta.status`
 *  — the reducer's own rule (a reducer never assigns `open`), not special-
 *  cased here. */
export const DASHBOARD_STATE_STATUS: Readonly<Record<RemedyState, string>> = {
  done: "completed",
  current: "running",
  pending: "pending",
  blocked: "blocked",
  suggested: "suggested",
};

/** One seed per dashboard task, in list order — `seedBrainModel`'s own input
 *  shape. `rank` is the task's index in the list (job.tasks order); `title`
 *  carries the dashboard's label through to the layout's task label.
 *  `pausedTaskIds` is the dashboard's own `pause.pausedTaskIds` (DECISION
 *  F025 D3 clause 2): a task named there seeds as `paused` regardless of its
 *  dashboard status word, so a page opened on a parked job draws it paused
 *  from the first paint — defaults to none, so every existing call site
 *  (none of which knows about a pause) keeps its exact prior seed.
 *  `specVersions` (DECISION F026 D3 clause 2) is the task-id-to-spec-version
 *  map `taskSpecView.ts`'s `taskSpecVersions` derives from the dashboard's
 *  `task_specs` section — defaults to none, so a caller that has not read it
 *  seeds no task with a version. A task's own id is put on the seed as
 *  `specVersion` ONLY when the map carries that task at all, never a
 *  fallback value. */
export function dashboardBrainSeeds(
  tasks: readonly RemedyTaskItem[],
  pausedTaskIds: readonly string[] = [],
  specVersions: Readonly<Record<string, number>> = {},
): BrainTaskSeed[] {
  const paused = new Set(pausedTaskIds);
  return tasks.map((t, index) => ({
    id: t.id,
    status: paused.has(t.id) ? "paused" : (DASHBOARD_STATE_STATUS[t.state] ?? t.state),
    rank: index,
    title: t.label,
    ...(Object.prototype.hasOwnProperty.call(specVersions, t.id) ? { specVersion: specVersions[t.id] } : {}),
  }));
}

/** The same open/planned/done split `BrainGraphCanvas` applies to the
 *  dashboard's words (open = current or blocked, planned = planned, done =
 *  done), restated in the ontology's own `NodeState` vocabulary so
 *  `filterBrainLayout` can read a layout node's state directly. `paused`
 *  groups with `planned` (DECISION F025 D3 clause 2): a paused node is not
 *  in progress and nothing has failed — it is waiting, exactly like a
 *  planned one, until the operator resumes it. */
export const BRAIN_FILTER_STATES: Readonly<Record<"open" | "planned" | "done", readonly NodeState[]>> = {
  open: ["in_progress", "blocked", "fail"],
  planned: ["planned", "paused"],
  done: ["pass"],
};

/** Filters a positioned layout down to one filter's nodes/links. `"all"`
 *  returns the SAME object (a caller's memo can skip the filtered branch
 *  entirely). Otherwise: the core (depth 0) always stays; a task (depth 1)
 *  stays when its state is in the filter's list; a depth-2 node stays when
 *  its `parentId` names a kept task, regardless of its own state; a link
 *  stays only when both its source and target stay. Node order is preserved.
 *  `layout` itself is never mutated. */
export function filterBrainLayout(layout: BrainLayoutData, filter: GraphFilter): BrainLayoutData {
  if (filter === "all") return layout;
  const allowedStates = BRAIN_FILTER_STATES[filter];
  const keptTaskIds = new Set(
    layout.nodes.filter((n) => n.depth === 1 && allowedStates.includes(n.state)).map((n) => n.id),
  );
  const keptIds = new Set<string>();
  const nodes = layout.nodes.filter((n) => {
    let keep: boolean;
    if (n.depth === 0) keep = true;
    else if (n.depth === 1) keep = keptTaskIds.has(n.id);
    else keep = n.parentId !== undefined && keptTaskIds.has(n.parentId);
    if (keep) keptIds.add(n.id);
    return keep;
  });
  const links = layout.links.filter((l) => keptIds.has(l.source) && keptIds.has(l.target));
  return { nodes, links };
}

/** The number of real `task` nodes a layout carries — used to decide whether
 *  the live canvas has anything to show (BrainGraphStage falls back to the
 *  simple view's own empty state otherwise). Decor is never counted
 *  (graph_spec §8 truth); this layout has none anyway. */
export function brainTaskCount(layout: BrainLayoutData): number {
  return layout.nodes.filter((n) => n.kind === "task").length;
}

/** The layout's own `task:`-prefixed node id for a shell selection id, or
 *  `null` when there is none. The shell's selection id is a bare task id when
 *  the old canvas set it and a dashboard `nodeId` when jump-to set it
 *  (RemedyShell.tsx `handleJump`), so both are tried against every task. */
export function selectedBrainNodeId(tasks: readonly RemedyTaskItem[], selectedNodeId: string | null): string | null {
  if (selectedNodeId === null) return null;
  const task = tasks.find((t) => t.id === selectedNodeId || t.nodeId === selectedNodeId);
  return task ? `task:${task.id}` : null;
}

/** The task id a click on this node should open — a task resolves to itself,
 *  any depth-2 kind (run/synapse/artifact/cluster) resolves to its parent
 *  task (a run or cluster click opens its owning task, since run detail is
 *  the zoom feature's L2), and the core resolves to nothing. */
export function selectionTaskIdOf(node: Pick<BrainLayoutNode, "id" | "kind" | "parentId">): string | null {
  if (node.kind === "job_core") return null;
  if (node.kind === "task") return node.id.slice("task:".length);
  return node.parentId ? node.parentId.slice("task:".length) : null;
}

/** The shell's own selection id for a `selectionTaskIdOf` result.
 *  `RemedyShell.tsx` resolves a click by `dashboard.graph.nodes.find(n =>
 *  n.nodeId === selectedNodeId || n.id === selectedNodeId)`, and
 *  `remedyApi.ts` builds each graph node's id from the task's `nodeId`
 *  (`related_node_id || id`) — so a live-view click must hand the shell the
 *  task's `nodeId`, not its bare id. Falls back to the given id itself when
 *  no task matches (a `null` click, or an id this dashboard has never seen,
 *  passes through unchanged). */
export function shellSelectionIdOf(tasks: readonly RemedyTaskItem[], taskId: string | null): string | null {
  if (taskId === null) return null;
  const task = tasks.find((t) => t.id === taskId);
  return task ? task.nodeId : taskId;
}

/** Builds a NEW node array for `next`: a node whose id also appears in
 *  `previous` with finite `x`/`y` takes that position instead of its freshly
 *  laid-out one, so a surviving node does not jump back to its seeded spot on
 *  every dashboard poll. `fx`/`fy` are always `next`'s own (the core stays
 *  pinned at the layout's origin) — `previous`'s `fx`/`fy`, if it even has
 *  any, are never read. Every returned node is a new object; neither input is
 *  mutated. `null` previous (first paint) yields plain copies of `next`. */
export function carryBrainPositions(
  previous: readonly { id: string; x?: number; y?: number }[] | null,
  next: readonly BrainLayoutNode[],
): BrainLayoutNode[] {
  const byId = new Map((previous ?? []).map((n) => [n.id, n]));
  return next.map((n) => {
    const prior = byId.get(n.id);
    if (prior && Number.isFinite(prior.x) && Number.isFinite(prior.y)) {
      return { ...n, x: prior.x as number, y: prior.y as number };
    }
    return { ...n };
  });
}
