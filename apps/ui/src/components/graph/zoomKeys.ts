// T5_F044 T002, DECISION F044 D6 — the graph's keys, read through the one keymap
// (api/keymap.ts): "j" and "k" walk the siblings one step, Enter zooms in, and Escape walks
// back, each becoming the SAME pick a pointer's click would make. PURE: the zoom machine
// (semanticZoom.ts) is not changed by this module; a pick is handed to the machine as a click.
// Siblings are read in the graph's own iteration order — the reducer's model order — never by
// screen position, which moves as the graph grows.
import { isZoomRunKind } from "./semanticZoom";
import type { ZoomGraph, ZoomState } from "./semanticZoom";
import type { KeymapAction } from "../../api/keymap";

/** A key's decision: pick a node (as a click would) or walk back (as Escape does). */
export type ZoomKeyStep =
  | { readonly kind: "pick"; readonly nodeId: string }
  | { readonly kind: "walk-back" };

/** The ids of one sibling group, in the graph's own iteration order: the run-kind nodes
 *  sharing the focused node's parent at level 2 or 3, or every task node otherwise. Null when
 *  the focus is at level 2 or 3 but is not itself in the graph, so its parent cannot be read. */
function siblingIds(graph: ZoomGraph, state: ZoomState): readonly string[] | null {
  if ((state.level === 2 || state.level === 3) && state.focusId !== null) {
    const focus = graph.get(state.focusId);
    if (!focus) return null;
    const ids: string[] = [];
    graph.forEach((node, id) => {
      if (isZoomRunKind(node.kind) && node.parentId === focus.parentId) ids.push(id);
    });
    return ids;
  }
  const ids: string[] = [];
  graph.forEach((node, id) => {
    if (node.kind === "task") ids.push(id);
  });
  return ids;
}

/** One step within a sibling group: wraps at either end, and enters at the first going forward
 *  or the last going back when the focus is not among them. Null for an empty group. */
function stepAmong(ids: readonly string[], focusId: string | null, forward: boolean): string | null {
  if (ids.length === 0) return null;
  const at = focusId === null ? -1 : ids.indexOf(focusId);
  if (at === -1) return forward ? ids[0] : ids[ids.length - 1];
  const next = forward ? (at + 1) % ids.length : (at - 1 + ids.length) % ids.length;
  return ids[next];
}

/** Enter picks the focused task's first run-kind node in the graph's order; null when it has
 *  none, and null at every level but 1. */
function firstRun(graph: ZoomGraph, state: ZoomState): string | null {
  if (state.level !== 1 || state.focusId === null) return null;
  let found: string | null = null;
  graph.forEach((node, id) => {
    if (found === null && isZoomRunKind(node.kind) && node.parentId === state.focusId) found = id;
  });
  return found;
}

/** The one decision every graph key defers to: what a keymap action means for the zoom, as the
 *  step the caller dispatches as a click or an escape. Every action but the four below is null. */
export function zoomKeyStep(graph: ZoomGraph, state: ZoomState, action: KeymapAction): ZoomKeyStep | null {
  if (action === "walk-back") return { kind: "walk-back" };
  if (action === "next-sibling" || action === "previous-sibling") {
    const ids = siblingIds(graph, state);
    if (ids === null) return null;
    const picked = stepAmong(ids, state.focusId, action === "next-sibling");
    return picked === null ? null : { kind: "pick", nodeId: picked };
  }
  if (action === "zoom-in") {
    const picked = firstRun(graph, state);
    return picked === null ? null : { kind: "pick", nodeId: picked };
  }
  return null;
}
