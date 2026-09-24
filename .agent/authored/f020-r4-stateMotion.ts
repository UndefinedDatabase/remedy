// How a node's state CHANGE moves: a colour crossfade from the old state's
// treatment to the new one, and a completion ripple when a node reaches
// `pass` (graph_spec.md §12, motion_spec.md "completion ripple"). Pure and
// total, like brainMotion.ts beside it: no DOM, no clock of its own — every
// function takes the time it is asked about. Reduced motion schedules nothing,
// so a change is simply drawn in its new state (graph_spec §12: "ripple =
// none; ALL state remains readable statically").
import type { NodeState } from "../brainOntology";
import type { BrainLayoutData } from "../forceBrainTypes";
import { NODE_STATE_TREATMENTS } from "./nodeStates";

/** State crossfade and completion ripple length (motion_spec.md: "completion
 *  ripple | 300ms | ease-out"; graph_spec §12: "300ms white ring ripple
 *  r→r+14 fade; state color crossfade"). */
export const STATE_TRANSITION_MS = 300;

/** How far past the node's edge the ripple ring travels (graph_spec §12). */
export const COMPLETION_RIPPLE_SPREAD = 14;

/** One node's state change: when it started, how long it runs, and whether it
 *  ends in a completion ripple. */
export interface StateTransition {
  id: string;
  from: NodeState;
  to: NodeState;
  startMs: number;
  durationMs: number;
  ripple: boolean;
}

/** Every node whose state differs between two layouts, in the next layout's
 *  node order. A first paint (`previous === null`), a node born in `next` and
 *  the job core (which keeps its own painter, not the state language) change
 *  nothing here; a birth has its own motion in brainMotion.ts. */
export function scheduleStateTransitions(
  previous: BrainLayoutData | null,
  next: BrainLayoutData,
  nowMs: number,
  reducedMotion: boolean,
): StateTransition[] {
  if (previous === null || reducedMotion) return [];
  const before = new Map(previous.nodes.map((n) => [n.id, n.state]));
  return next.nodes
    .filter((n) => n.kind !== "job_core" && before.has(n.id) && before.get(n.id) !== n.state)
    .map((n) => ({
      id: n.id,
      from: before.get(n.id) as NodeState,
      to: n.state,
      startMs: nowMs,
      durationMs: STATE_TRANSITION_MS,
      ripple: n.state === "pass",
    }));
}

/** What a transition contributes to one frame: the old state's weight, the
 *  new state's weight, and the ripple ring's spread and alpha, or null. */
export interface TransitionFrame {
  fromAlpha: number;
  toAlpha: number;
  ripple: { spread: number; alpha: number } | null;
  done: boolean;
}

function easeOut(p: number): number {
  return 1 - Math.pow(1 - p, 3);
}

/** A transition `nowMs` into its run: a linear crossfade, and a ripple that
 *  eases out to COMPLETION_RIPPLE_SPREAD while it fades. */
export function transitionFrameAt(transition: StateTransition, nowMs: number): TransitionFrame {
  const raw = transition.durationMs > 0 ? (nowMs - transition.startMs) / transition.durationMs : 1;
  const p = Math.min(1, Math.max(0, raw));
  const ripple = transition.ripple && p < 1
    ? { spread: COMPLETION_RIPPLE_SPREAD * easeOut(p), alpha: 1 - p }
    : null;
  return { fromAlpha: 1 - p, toAlpha: p, ripple, done: p >= 1 };
}

/** Whether any node in the layout pulses (graph_spec §12: in-progress nodes). */
export function layoutHasPulse(layout: BrainLayoutData): boolean {
  return layout.nodes.some((n) => n.kind !== "job_core" && NODE_STATE_TREATMENTS[n.state].pulse);
}

/** What decides whether the canvas must keep drawing frames. */
export interface BrainAnimationNeeds {
  pageVisible: boolean;
  reducedMotion: boolean;
  birthsInFlight: boolean;
  transitionsInFlight: boolean;
  pulsing: boolean;
}

/** Whether the canvas must redraw on every frame. A hidden page never does,
 *  so a background tab spins no CPU (motion_spec.md: "pulses pause when tab
 *  hidden"); a birth or a transition in flight always does while visible;
 *  and a pulse does only when motion is not reduced. */
export function brainNeedsAnimationFrames(needs: BrainAnimationNeeds): boolean {
  if (!needs.pageVisible) return false;
  if (needs.birthsInFlight || needs.transitionsInFlight) return true;
  return needs.pulsing && !needs.reducedMotion;
}
