// Owns what the semantic-zoom state MEANS on the canvas: which nodes dim,
// which carry a label and a focus ring, which branches glow, where the camera
// goes, and what each breadcrumb says. PURE: it reads the positioned layout
// and the machine's state (semanticZoom.ts) and returns plain data, so the
// render effects are goldened headless; ForceBrainGraph.tsx only paints them
// (graph_spec.md §10, DECISION F023 D2). No effect here mutates the model.
import type { BrainLayoutData, BrainLayoutNode } from "./forceBrainTypes";
import { GLYPHS } from "./renderers/glyphPaths";
import type { ZoomCrumb, ZoomState } from "./semanticZoom";

/** graph_spec §10, L1: "siblings dim to 25%". */
export const ZOOM_DIM_ALPHA = 0.25;

/** The camera factor a click lands L1 on: above the wheel's 1.6, so the
 *  camera and the level agree and a wheel-out must cross 0.8 to leave. */
export const ZOOM_TASK_CAMERA = 2;

/** The camera factor L2 and L3 centre their run at. */
export const ZOOM_RUN_CAMERA = 2.4;

/** The camera factor of L0, the fit the graph opens at. */
export const ZOOM_HOME_CAMERA = 1;

/** How long a camera move between levels takes: `--remedy-dur-slow`, the
 *  motion_spec.md row for "progress/layout" moves. Reduced motion jumps. */
export const ZOOM_CAMERA_MS = 350;

/** Everything the painter needs from the zoom state, per node and per link. */
export interface ZoomEmphasis {
  /** Nodes painted at ZOOM_DIM_ALPHA: every node outside the focused task's
   *  branch at L1 and deeper; none at L0. The core never dims. */
  dimmed: ReadonlySet<string>;
  /** Nodes whose label is drawn whatever the camera factor: the focused task. */
  labelled: ReadonlySet<string>;
  /** The node the focus ring is drawn around: the task at L1, the run at L2
   *  and L3, nothing at L0. */
  ringId: string | null;
  /** Links drawn with the branch glow: at L0 every active link, deeper only
   *  the active links of the focused branch. */
  glowing: ReadonlySet<string>;
}

/** The focused task's node id in this layout, or null: the focus itself at
 *  L1, the focused run's parent at L2 and L3 — and null whenever the layout
 *  does not hold that task, as when a filter chip hides it, so a hidden focus
 *  never dims the whole graph. */
export function focusTaskIdOf(layout: BrainLayoutData, state: ZoomState): string | null {
  if (state.level === 0 || state.focusId === null) return null;
  const taskId = state.level === 1 ? state.focusId : layout.nodes.find((n) => n.id === state.focusId)?.parentId;
  return taskId !== undefined && layout.nodes.some((n) => n.id === taskId) ? taskId : null;
}

/** The render effects of one zoom state over one layout. */
export function zoomEmphasis(layout: BrainLayoutData, state: ZoomState): ZoomEmphasis {
  const taskId = focusTaskIdOf(layout, state);
  const inBranch = (n: BrainLayoutNode) => n.depth === 0 || n.id === taskId || n.parentId === taskId;
  const dimmed = new Set<string>();
  if (taskId !== null) layout.nodes.forEach((n) => { if (!inBranch(n)) dimmed.add(n.id); });
  const glowing = new Set<string>();
  layout.links.forEach((l) => {
    if (!l.active) return;
    if (taskId === null || l.target === taskId || l.source === taskId) glowing.add(l.id);
  });
  return {
    dimmed,
    labelled: new Set(taskId === null ? [] : [taskId]),
    ringId: state.level === 0 ? null : state.focusId,
    glowing,
  };
}

/** Where the camera should sit for a state: centre and factor. Null when the
 *  focus has no position in this layout, in which case the camera stays. */
export function zoomCamera(
  layout: BrainLayoutData,
  state: ZoomState,
): { x: number; y: number; k: number } | null {
  if (state.level === 0 || state.focusId === null) return { x: 0, y: 0, k: ZOOM_HOME_CAMERA };
  const node = layout.nodes.find((n) => n.id === state.focusId);
  if (!node) return null;
  return { x: node.x, y: node.y, k: state.level === 1 ? ZOOM_TASK_CAMERA : ZOOM_RUN_CAMERA };
}

/** The words a breadcrumb shows: "Job", then the task's own label, then the
 *  run's kind as the legend names it (renderers/glyphPaths.ts). */
export function zoomCrumbLabel(crumb: ZoomCrumb, layout: BrainLayoutData): string {
  if (crumb.level === 0) return "Job";
  const node = layout.nodes.find((n) => n.id === crumb.nodeId);
  if (crumb.level === 1) return node?.label || "Task";
  return node ? GLYPHS[node.kind].name : "Run";
}

/** Whether an Escape keypress should walk the zoom back: not while the key
 *  goes to a text field, and not while a dialog is open, whose own Escape
 *  closes it first (GraphLegend.tsx). */
export function escapeWalksBack(
  target: { tagName?: string; isContentEditable?: boolean } | null,
  dialogOpen: boolean,
): boolean {
  if (dialogOpen) return false;
  if (!target) return true;
  if (target.isContentEditable) return false;
  const tag = (target.tagName ?? "").toUpperCase();
  return tag !== "INPUT" && tag !== "TEXTAREA" && tag !== "SELECT";
}
