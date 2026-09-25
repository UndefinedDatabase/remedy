// Owns the semantic-zoom state machine: the level the graph is read at and the
// node it is focused on (T5_F023, graph_spec.md §10). PURE: no React, no DOM,
// no camera. The wheel adapter (zoomWheel.ts) turns camera zoom into this
// module's `zoom_in` / `zoom_out` events, and the hysteresis lives there, not
// here; a click, a breadcrumb and the Escape key speak to this module directly.
// Every transition is a function of (graph, state, event), so the whole matrix
// is goldened headless (DECISION F023 D1).
import type { BrainNode, NodeKind } from "./brainOntology";

/** L0 organism, L1 task focus, L2 run detail, L3 evidence (graph_spec §10). */
export type ZoomLevel = 0 | 1 | 2 | 3;

/** The tabs of the L3 evidence panel (T5_F023: diff | prompt trace | chat). */
export type EvidenceTab = "diff" | "prompt" | "chat";

/** Where the reader is. `focusId` is null at L0, a task node id at L1 and a run
 *  node id at L2 and L3. `tab` is non-null at L3 only: it is part of L3's
 *  address, because the L2 buttons land on different tabs of the same run. */
export interface ZoomState {
  level: ZoomLevel;
  focusId: string | null;
  tab: EvidenceTab | null;
}

/** L0, the default: the whole organism, nothing focused. */
export const ZOOM_HOME: ZoomState = { level: 0, focusId: null, tab: null };

/** Everything that can move the machine. `click` is a pointer click on a node,
 *  `zoom_in` / `zoom_out` are the wheel adapter's threshold crossings, `escape`
 *  is the Escape key, `crumb` is a breadcrumb jump to a shallower level,
 *  `open_evidence` is an L2 button or a tab switch, and `reconcile` re-checks
 *  the focus after the graph changed under it. */
export type ZoomEvent =
  | { type: "click"; nodeId: string }
  | { type: "zoom_in"; nodeId: string }
  | { type: "zoom_out" }
  | { type: "escape" }
  | { type: "crumb"; level: ZoomLevel }
  | { type: "open_evidence"; tab: EvidenceTab }
  | { type: "reconcile" };

/** One transition's result. A refused or empty transition returns the SAME
 *  state object it was given; `note` says why when the refusal is worth a debug
 *  line, and is null otherwise. */
export interface ZoomStep {
  state: ZoomState;
  note: string | null;
}

/** What the machine needs to know about a node: its kind and its parent. */
export interface ZoomGraphNode {
  kind: NodeKind;
  parentId?: string;
}

/** The nodes the machine validates focus against, by id. */
export type ZoomGraph = ReadonlyMap<string, ZoomGraphNode>;

/** Builds the lookup from one or more node lists. The caller passes the
 *  reducer's model, which keeps every run, and the clustered view's nodes, so a
 *  cluster can be clicked while a run a cluster hides can still hold the focus.
 *  A later list never overwrites an id an earlier list already gave. */
export function zoomGraphOf(
  ...lists: readonly (readonly Pick<BrainNode, "id" | "kind" | "parentId">[])[]
): ZoomGraph {
  const graph = new Map<string, ZoomGraphNode>();
  for (const list of lists) {
    for (const n of list) {
      if (!graph.has(n.id)) graph.set(n.id, { kind: n.kind, parentId: n.parentId });
    }
  }
  return graph;
}

const RUN_KINDS: readonly NodeKind[] = ["builder_run", "review_run", "repair_run", "test_run"];

/** True for the four run kinds, the only nodes L2 and L3 can focus. */
export function isZoomRunKind(kind: NodeKind): boolean {
  return RUN_KINDS.includes(kind);
}

function step(state: ZoomState, note: string | null = null): ZoomStep {
  return { state, note };
}

/** Moves to `next` unless it equals `state`, in which case `state` itself is
 *  returned, so an empty transition is recognisable by identity. */
function moveTo(state: ZoomState, next: ZoomState): ZoomStep {
  const same = state.level === next.level && state.focusId === next.focusId && state.tab === next.tab;
  return step(same ? state : next);
}

/** The task a node belongs to: a task is its own, anything else is its parent
 *  when that parent is a task in the graph; the core and orphans have none. */
function owningTaskId(graph: ZoomGraph, nodeId: string): string | null {
  const node = graph.get(nodeId);
  if (!node) return null;
  if (node.kind === "task") return nodeId;
  if (node.kind === "job_core" || node.parentId === undefined) return null;
  return graph.get(node.parentId)?.kind === "task" ? node.parentId : null;
}

/** The task id a run node id names under the reducer's id scheme,
 *  `run:<taskId>:<seq>` (DECISION F019 D1), read only when the run itself has
 *  left the graph and its parent can no longer be looked up. */
function taskIdOfRunNodeId(runNodeId: string): string | null {
  const match = /^run:(.+):\d+$/.exec(runNodeId);
  return match ? `task:${match[1]}` : null;
}

function taskFocus(taskId: string): ZoomState {
  return { level: 1, focusId: taskId, tab: null };
}

function missing(nodeId: string): string {
  return `focus target ${nodeId} is not in the graph`;
}

function onClick(graph: ZoomGraph, state: ZoomState, nodeId: string): ZoomStep {
  const node = graph.get(nodeId);
  if (!node) return step(state, missing(nodeId));
  if (node.kind === "job_core") return moveTo(state, ZOOM_HOME);
  if (isZoomRunKind(node.kind)) {
    if (owningTaskId(graph, nodeId) === null) return step(state, `run ${nodeId} has no task in the graph`);
    return moveTo(state, { level: 2, focusId: nodeId, tab: null });
  }
  const taskId = owningTaskId(graph, nodeId);
  if (taskId === null) return step(state, `${node.kind} ${nodeId} has no task in the graph`);
  return moveTo(state, taskFocus(taskId));
}

function onZoomIn(graph: ZoomGraph, state: ZoomState, nodeId: string): ZoomStep {
  if (state.level >= 2) return step(state, "the wheel does not leave run detail; Escape walks back");
  const node = graph.get(nodeId);
  if (!node) return step(state, missing(nodeId));
  if (node.kind === "job_core") return step(state);
  const taskId = owningTaskId(graph, nodeId);
  if (taskId === null) return step(state, `${node.kind} ${nodeId} has no task in the graph`);
  return moveTo(state, taskFocus(taskId));
}

function onEscape(graph: ZoomGraph, state: ZoomState): ZoomStep {
  if (state.level === 3) return moveTo(state, { level: 2, focusId: state.focusId, tab: null });
  if (state.level === 2) {
    const taskId = state.focusId === null ? null : owningTaskId(graph, state.focusId);
    return moveTo(state, taskId === null ? ZOOM_HOME : taskFocus(taskId));
  }
  return moveTo(state, ZOOM_HOME);
}

function onCrumb(graph: ZoomGraph, state: ZoomState, level: ZoomLevel): ZoomStep {
  if (level >= state.level) return step(state, level > state.level ? "a breadcrumb only walks back" : null);
  if (level === 0) return moveTo(state, ZOOM_HOME);
  if (level === 1) {
    const taskId = state.focusId === null ? null : owningTaskId(graph, state.focusId);
    return moveTo(state, taskId === null ? ZOOM_HOME : taskFocus(taskId));
  }
  return moveTo(state, { level: 2, focusId: state.focusId, tab: null });
}

function onOpenEvidence(state: ZoomState, tab: EvidenceTab): ZoomStep {
  if (state.level < 2) return step(state, "evidence opens from a run's detail");
  return moveTo(state, { level: 3, focusId: state.focusId, tab });
}

function onReconcile(graph: ZoomGraph, state: ZoomState): ZoomStep {
  if (state.focusId === null || graph.has(state.focusId)) return step(state);
  const gone = state.focusId;
  const taskId = state.level >= 2 ? taskIdOfRunNodeId(gone) : null;
  if (taskId !== null && graph.get(taskId)?.kind === "task") {
    return step(taskFocus(taskId), `focus ${gone} left the graph; walked up to its task`);
  }
  return step(ZOOM_HOME, `focus ${gone} left the graph; walked up to the job`);
}

/** The one transition function. Total over every (state, event) pair: an
 *  event that does not apply leaves the state as it was. */
export function zoomTransition(graph: ZoomGraph, state: ZoomState, event: ZoomEvent): ZoomStep {
  switch (event.type) {
    case "click":
      return onClick(graph, state, event.nodeId);
    case "zoom_in":
      return onZoomIn(graph, state, event.nodeId);
    case "zoom_out":
      return moveTo(state, ZOOM_HOME);
    case "escape":
      return onEscape(graph, state);
    case "crumb":
      return onCrumb(graph, state, event.level);
    case "open_evidence":
      return onOpenEvidence(state, event.tab);
    case "reconcile":
      return onReconcile(graph, state);
  }
}

/** One breadcrumb: the level it jumps to, the node that level is focused on
 *  (null for the job) and whether it is the level the reader is at. */
export interface ZoomCrumb {
  level: 0 | 1 | 2;
  nodeId: string | null;
  current: boolean;
}

/** The breadcrumb trail Job > Task > Run for a state. At L3 the trail still
 *  ends at the run and no crumb is current: the run crumb closes the panel. */
export function zoomBreadcrumbs(graph: ZoomGraph, state: ZoomState): ZoomCrumb[] {
  const crumbs: ZoomCrumb[] = [{ level: 0, nodeId: null, current: state.level === 0 }];
  if (state.level === 0 || state.focusId === null) return crumbs;
  const taskId = owningTaskId(graph, state.focusId);
  if (taskId !== null) crumbs.push({ level: 1, nodeId: taskId, current: state.level === 1 });
  if (state.level >= 2) crumbs.push({ level: 2, nodeId: state.focusId, current: state.level === 2 });
  return crumbs;
}
