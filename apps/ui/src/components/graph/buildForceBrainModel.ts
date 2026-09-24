import type {
  BrainLayoutData, BrainLayoutLink, BrainLayoutNode,
} from "./forceBrainTypes";
import { clusterBrainModel } from "./brainReducer";
import type { BrainModel, BrainNode, NodeKind } from "./brainOntology";

export function seededRng(seed: string) {
  let h = 0;
  for (let i = 0; i < seed.length; i++) { h = ((h << 5) - h + seed.charCodeAt(i)) | 0; }
  let s = h >>> 0;
  return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}

// --- the graph module's single data-to-graph builder ------------------------
// This file is the single data-to-force-graph builder
// (docs/ui/design_reference/graph_tech_recommendation.md). buildBrainLayout
// below lays out the reducer's real model one to one — no decor, no invented
// node (graph_spec §8 truth; DECISION F019 D1). The decorative dashboard
// builder this file used to also carry (organic branches, ambient particles
// fanned out from the polled dashboard) was removed by DECISION F019 D4.

/** Core sphere radius, graph_spec §4 ("core: r 26 sphere"). */
export const BRAIN_CORE_RADIUS = 26;
/** Task node radius, graph_spec §4 ("task: r 7 (major)"). */
export const BRAIN_TASK_RADIUS = 7;
/** Run node radius, graph_spec §4 ("run: r 4.5"). */
export const BRAIN_RUN_RADIUS = 4.5;
/** Cluster node radius, graph_spec §4 ("cluster: r 9 + count") — bigger than a
 *  run so a collapsed history still reads as "more than one thing". */
export const BRAIN_CLUSTER_RADIUS = 9;
/** Distance from the core to the task ring, graph_spec §6 ("core-task
 *  120-170"); this design fixes one value inside that band. */
export const BRAIN_TASK_RING_RADIUS = 150;
/** Distance from a task to its run/cluster children, graph_spec §6
 *  ("task-run 34"). */
export const BRAIN_RUN_DISTANCE = 34;
/** The golden angle in radians, π·(3−√5): spaces tasks stably around the core
 *  regardless of how many exist, graph_spec §6 ("Seeded initial angles =
 *  golden-angle around the core so layouts are stable per job"). */
export const BRAIN_GOLDEN_ANGLE = Math.PI * (3 - Math.sqrt(5));
/** Angular step between a task's fanned-out children, graph_spec §6. */
export const BRAIN_RUN_FAN_STEP = 0.35;
/** Core→task link width — trunk thickness decays with depth (graph_spec §6,
 *  "core→task 2.2 → run 1.4"). */
export const BRAIN_CORE_LINK_WIDTH = 2.2;
/** Task→child link width, the next step of the same decay. */
export const BRAIN_RUN_LINK_WIDTH = 1.4;

/** Every non-core, non-task node buildBrainLayout treats as a task's depth-2
 *  child: the run kinds and the cluster node clusterBrainModel may leave
 *  behind (graph_spec §3 hierarchy). */
function isLayoutChildKind(kind: NodeKind): boolean {
  return kind !== "job_core" && kind !== "task";
}

/** A task's label is its seed title when one was given, else its bare id
 *  with the `task:` prefix stripped; a cluster's is its count, and every
 *  other node carries no label. */
function taskLabelOf(task: BrainNode): string {
  const title = task.meta.title;
  if (typeof title === "string" && title.length > 0) return title;
  return task.id.slice("task:".length);
}

/** A cluster's label is the count of runs it stands for, as `+n` (graph_spec
 *  §10: 'cluster chip "+n"'); a cluster that carries no count gets none. */
function clusterLabelOf(cluster: BrainNode): string {
  const count = cluster.meta.count;
  return typeof count === "number" && count > 0 ? `+${count}` : "";
}

/** Task ordering for golden-angle assignment (graph_spec §6: "Seeded initial
 *  angles = golden-angle around the core"): by seed rank (a rank-less task
 *  sorts last), then id. This is the order angles are HANDED OUT in, not the
 *  output node order — §8 truth keeps that as the clustered model's own
 *  order, which this function never touches. */
function orderTasksForAngle(tasks: readonly BrainNode[]): BrainNode[] {
  return [...tasks].sort((a, b) => {
    const rankA = typeof a.meta.rank === "number" ? a.meta.rank : Number.POSITIVE_INFINITY;
    const rankB = typeof b.meta.rank === "number" ? b.meta.rank : Number.POSITIVE_INFINITY;
    if (rankA !== rankB) return rankA - rankB;
    return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
  });
}

/** Child ordering for the fan (graph_spec §3: "run (1:n per task,
 *  chronological fan)"): by seq then id — the order the symmetric offset
 *  (k − (n − 1) / 2) is indexed by. */
function orderChildrenForFan(children: readonly BrainNode[]): BrainNode[] {
  return [...children].sort((a, b) => a.seq - b.seq || (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
}

/** A link is "active" — particles flow on it — when its own target run is
 *  in_progress, or its target task has any in_progress child (graph_spec §7:
 *  "particles on (one white particle per active run edge)"; §8: "particles
 *  flow only while a run is actually active per data"). */
function isLinkActive(nodes: readonly BrainNode[], target: BrainNode | undefined): boolean {
  if (!target) return false;
  if (target.state === "in_progress") return true;
  if (target.kind !== "task") return false;
  return nodes.some((n) => n.parentId === target.id && n.state === "in_progress");
}

/** Positions `clusterBrainModel(model)`'s nodes and links with no decor and
 *  no invented node (DECISION F019 D1; graph_spec §4 sizes, §6 layout, §8
 *  truth). Deterministic and total — no random draws, no Date — and the
 *  input model is never mutated. */
export function buildBrainLayout(model: BrainModel): BrainLayoutData {
  const clustered = clusterBrainModel(model);
  const rng = seededRng(clustered.jobId || "default");
  const seedAngle = rng() * 2 * Math.PI;

  const tasks = clustered.nodes.filter((n) => n.kind === "task");
  const taskAngle = new Map<string, number>();
  orderTasksForAngle(tasks).forEach((task, i) => {
    taskAngle.set(task.id, seedAngle + i * BRAIN_GOLDEN_ANGLE);
  });
  const taskPosition = new Map<string, { x: number; y: number }>();
  taskAngle.forEach((angle, id) => {
    taskPosition.set(id, {
      x: Math.cos(angle) * BRAIN_TASK_RING_RADIUS,
      y: Math.sin(angle) * BRAIN_TASK_RING_RADIUS,
    });
  });

  const childrenByTask = new Map<string, BrainNode[]>();
  for (const n of clustered.nodes) {
    if (!isLayoutChildKind(n.kind) || !n.parentId) continue;
    const list = childrenByTask.get(n.parentId) ?? [];
    list.push(n);
    childrenByTask.set(n.parentId, list);
  }
  const childPosition = new Map<string, { x: number; y: number }>();
  childrenByTask.forEach((children, taskId) => {
    const anchorAngle = taskAngle.get(taskId);
    const anchor = taskPosition.get(taskId);
    if (anchorAngle === undefined || !anchor) return;
    const ordered = orderChildrenForFan(children);
    const n = ordered.length;
    ordered.forEach((child, k) => {
      const angle = anchorAngle + (k - (n - 1) / 2) * BRAIN_RUN_FAN_STEP;
      childPosition.set(child.id, {
        x: anchor.x + Math.cos(angle) * BRAIN_RUN_DISTANCE,
        y: anchor.y + Math.sin(angle) * BRAIN_RUN_DISTANCE,
      });
    });
  });

  const nodes: BrainLayoutNode[] = clustered.nodes.map((n) => {
    if (n.kind === "job_core") {
      return {
        id: n.id, kind: n.kind, state: n.state, seq: n.seq,
        depth: 0, radius: BRAIN_CORE_RADIUS, x: 0, y: 0, fx: 0, fy: 0, label: "",
      };
    }
    if (n.kind === "task") {
      const p = taskPosition.get(n.id) ?? { x: 0, y: 0 };
      return {
        id: n.id, kind: n.kind, state: n.state, parentId: n.parentId, seq: n.seq,
        depth: 1, radius: BRAIN_TASK_RADIUS, x: p.x, y: p.y, label: taskLabelOf(n),
      };
    }
    const p = childPosition.get(n.id) ?? { x: 0, y: 0 };
    const radius = n.kind === "cluster" ? BRAIN_CLUSTER_RADIUS : BRAIN_RUN_RADIUS;
    return {
      id: n.id, kind: n.kind, state: n.state, parentId: n.parentId, seq: n.seq,
      depth: 2, radius, x: p.x, y: p.y, label: n.kind === "cluster" ? clusterLabelOf(n) : "",
    };
  });

  const byId = new Map(clustered.nodes.map((n) => [n.id, n]));
  const links: BrainLayoutLink[] = clustered.links.map((l) => {
    const target = byId.get(l.target);
    const isTaskLink = target?.kind === "task";
    return {
      id: l.id, source: l.source, target: l.target,
      depth: isTaskLink ? 1 : 2,
      width: isTaskLink ? BRAIN_CORE_LINK_WIDTH : BRAIN_RUN_LINK_WIDTH,
      active: isLinkActive(clustered.nodes, target),
    };
  });

  return { nodes, links };
}
