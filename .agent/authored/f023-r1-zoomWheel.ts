// Owns the wheel adapter of semantic zoom: it turns two successive camera zoom
// factors into the machine's `zoom_in` / `zoom_out` events (semanticZoom.ts).
// The HYSTERESIS lives here and nowhere else (T5_F023 Design): an event fires
// only when the zoom CROSSES a threshold, zoom-in above 1.6 over a node and
// zoom-out below 0.8, so every factor between the two is a dead band in which
// the level never flickers (graph_spec.md §10, DECISION F023 D1).
import type { ZoomEvent } from "./semanticZoom";

/** graph_spec §10: the wheel enters task focus above this factor, on a node. */
export const ZOOM_IN_ABOVE = 1.6;

/** graph_spec §10: the wheel walks back to the organism below this factor. */
export const ZOOM_OUT_BELOW = 0.8;

/** Which threshold, if any, the zoom crossed from `previous` to `next`. */
export function wheelCrossing(previous: number, next: number): "in" | "out" | null {
  if (previous <= ZOOM_IN_ABOVE && next > ZOOM_IN_ABOVE) return "in";
  if (previous >= ZOOM_OUT_BELOW && next < ZOOM_OUT_BELOW) return "out";
  return null;
}

/** The machine event one wheel step produces, or null. A zoom-in needs a node
 *  under the pointer: zooming into empty space focuses nothing. */
export function wheelZoomEvent(previous: number, next: number, nodeIdUnderPointer: string | null): ZoomEvent | null {
  const crossing = wheelCrossing(previous, next);
  if (crossing === "out") return { type: "zoom_out" };
  if (crossing === "in" && nodeIdUnderPointer !== null) return { type: "zoom_in", nodeId: nodeIdUnderPointer };
  return null;
}
