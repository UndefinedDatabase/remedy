import type { RemedyDashboard } from "../../api/types";
import type {
  BrainLayoutData, BrainLayoutLink, BrainLayoutNode, BrainNodeKind, BrainNodeState,
  ForceBrainGraphData, ForceBrainLink, ForceBrainNode,
} from "./forceBrainTypes";
import { clusterBrainModel } from "./brainReducer";
import type { BrainModel, BrainNode, NodeKind } from "./brainOntology";

type SizeClass = "small" | "medium" | "large";
type FilterMode = "all" | "open" | "planned" | "done";

function seededRng(seed: string) {
  let h = 0;
  for (let i = 0; i < seed.length; i++) { h = ((h << 5) - h + seed.charCodeAt(i)) | 0; }
  let s = h >>> 0;
  return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
}

const BRANCH_COLORS: string[] = ["#4c83ff", "#4cc681", "#a78bfa", "#67e8f9", "#91b8ff", "#5eead4"];

function particleCount(size: SizeClass): number {
  if (size === "small") return 4;
  if (size === "medium") return 8;
  return 14;
}

export function buildForceBrainModel(
  dashboard: RemedyDashboard,
  size: SizeClass = "medium",
  filter: FilterMode = "all",
): ForceBrainGraphData {
  const rng = seededRng(dashboard.jobId || "default");
  const nodes: ForceBrainNode[] = [];
  const links: ForceBrainLink[] = [];

  const root: ForceBrainNode = {
    id: "root", nodeId: dashboard.jobId, kind: "root", state: "current",
    label: "Project", sourceKind: "layout_only", depth: 0, value: 18, fx: 0, fy: 0,
    clickable: false, visibleLabel: false, alpha: 1, color: "#3478ff",
  };
  nodes.push(root);

  const realNodes = dashboard.graph.nodes.slice(0, 60);
  const branchCount = Math.max(3, Math.min(6, Math.ceil(realNodes.length / 4)));
  const baseLen = size === "small" ? 90 : size === "medium" ? 130 : 170;

  // Build organic branches radiating from root
  for (let b = 0; b < branchCount; b++) {
    const baseAngle = (b / branchCount) * Math.PI * 2 - Math.PI / 2 + (rng() - 0.5) * 0.4;
    const color = BRANCH_COLORS[b % BRANCH_COLORS.length];
    const armLen = baseLen + (rng() * 40 - 20);
    const segCount = 2 + Math.floor(rng() * 2);
    let prevId = "root";
    let cx = 0, cy = 0;

    for (let s = 0; s < segCount; s++) {
      const angle = baseAngle + (rng() - 0.5) * 0.6;
      const dist = armLen / segCount * (0.8 + rng() * 0.4);
      cx += Math.cos(angle) * dist;
      cy += Math.sin(angle) * dist;

      const branchId = `branch-${b}-${s}`;
      const branchNode: ForceBrainNode = {
        id: branchId, kind: "cluster", state: "planned", label: "",
        sourceKind: "layout_only", depth: 1, value: 4,
        fx: cx, fy: cy,
        clickable: false, visibleLabel: false, alpha: 0.3, color,
      };
      nodes.push(branchNode);
      links.push({
        source: prevId, target: branchId,
        strength: 0.6, curvature: 0.05 + rng() * 0.1, alpha: 0.25, width: 1.2 - s * 0.3,
      });
      prevId = branchId;
    }
  }

  // Distribute real nodes along branches
  const branchIds = nodes.filter(n => n.kind === "cluster").map(n => n.id);
  realNodes.forEach((gn, idx) => {
    const state: BrainNodeState = gn.state === "done" ? "done" : gn.state === "current" ? "current" : gn.state === "blocked" ? "blocked" : gn.state === "suggested" ? "suggested" : "planned";
    const kind: BrainNodeKind = gn.kind === "root" ? "task" : (gn.kind as BrainNodeKind) || "task";
    const branchTarget = branchIds[idx % branchIds.length];
    const anchor = nodes.find(n => n.id === branchTarget)!;
    const angle = rng() * Math.PI * 2;
    const dist = 15 + rng() * 35;

    const node: ForceBrainNode = {
      id: gn.id || `real-${idx}`, nodeId: gn.nodeId, kind, state, label: gn.label,
      sourceKind: "real_brain", clusterId: branchTarget, depth: 2, value: 5,
      x: (anchor.fx ?? 0) + Math.cos(angle) * dist,
      y: (anchor.fy ?? 0) + Math.sin(angle) * dist,
      clickable: true, visibleLabel: idx < 6, alpha: 0.85,
      color: anchor.color,
    };
    nodes.push(node);
    links.push({
      source: branchTarget, target: node.id, clusterId: branchTarget,
      strength: 0.4, curvature: 0.03 + rng() * 0.08, alpha: 0.2, width: 0.6,
    });
  });

  // Ambient particles — sparse, along branches.
  // Hard cap: total decorative (layout_only) nodes must never exceed 90; they
  // are purely visual, never interactive, never counted in any UI total.
  const LAYOUT_ONLY_CAP = 90;
  const pCount = particleCount(size);
  branchIds.forEach((bid) => {
    const anchor = nodes.find(n => n.id === bid)!;
    for (let p = 0; p < pCount; p++) {
      if (nodes.filter(n => n.sourceKind === "layout_only").length >= LAYOUT_ONLY_CAP) break;
      const angle = rng() * Math.PI * 2;
      const dist = 10 + rng() * 50;
      const pid = `${bid}-p${p}`;
      nodes.push({
        id: pid, kind: "particle", state: "planned", label: "",
        sourceKind: "layout_only", depth: 3, value: 1.5,
        x: (anchor.fx ?? 0) + Math.cos(angle) * dist,
        y: (anchor.fy ?? 0) + Math.sin(angle) * dist,
        clickable: false, visibleLabel: false,
        alpha: 0.12 + rng() * 0.2, color: anchor.color,
      });
      links.push({
        source: bid, target: pid, strength: 0.15,
        curvature: rng() * 0.15, alpha: 0.08, width: 0.3,
      });
    }
  });

  // Apply filter
  if (filter !== "all") {
    const allowedStates: BrainNodeState[] =
      filter === "done" ? ["done"] :
      filter === "open" ? ["current", "blocked"] :
      ["planned", "suggested"];
    nodes.forEach(n => {
      if (n.kind === "root" || n.kind === "cluster") return;
      if (!allowedStates.includes(n.state)) { n.alpha = 0.04; }
    });
    links.forEach(l => {
      const targetNode = typeof l.target === "string" ? nodes.find(n => n.id === l.target) : l.target;
      if (targetNode && (targetNode as ForceBrainNode).alpha < 0.1) { l.alpha = 0.02; }
    });
  }

  return { nodes, links };
}

// --- buildBrainLayout: positions the reducer's real model -------------------
// WHY this is a second, separate builder rather than a mode of the one above:
// buildForceBrainModel paints the polled-dashboard demo graph (decorative
// branches, ambient particles); this one lays out the reducer's real model
// 1:1, no decor, no invented node (graph_spec §8 truth; DECISION F019 D1).
// Its one caller is the brain renderer; the dashboard builder above paints
// the older decorative graph and is replaced when the renderer mounts.

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
 *  with the `task:` prefix stripped; every other node paints no label, so
 *  only a task node ever calls this. */
function taskLabelOf(task: BrainNode): string {
  const title = task.meta.title;
  if (typeof title === "string" && title.length > 0) return title;
  return task.id.slice("task:".length);
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
      depth: 2, radius, x: p.x, y: p.y, label: "",
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
