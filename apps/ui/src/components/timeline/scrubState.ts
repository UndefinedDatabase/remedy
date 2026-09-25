// The scrubber as a pure machine (T5_F024.md T003, DECISION F024 D3): which seq
// the graph shows, whether that is the live head or a scrubbed position, and how
// many rows arrived behind a scrubbed view. The store keeps ingesting while the
// render is scrubbed; LIVE returns to the head by fast-forward under a duration
// cap, or — when more arrived than a catch-up should replay — by a labeled
// refetch. No React, no DOM, no clock: the hook that binds it owns the timers.

/** Rows that may arrive behind a scrubbed view before LIVE stops replaying them
 *  and refetches instead (T5_F024.md edge cases: truth over seamlessness). */
export const SCRUB_QUEUE_CAP = 5000;

/** One catch-up frame is held for `--remedy-dur-fast` (motion_spec.md). */
export const CATCH_UP_STEP_MS = 120;

/** A catch-up shows at most this many frames, so it never runs past
 *  CATCH_UP_STEP_MS × CATCH_UP_MAX_STEPS however far behind the view was. */
export const CATCH_UP_MAX_STEPS = 8;

export type ScrubMode = "live" | "scrubbed";

/** `position` is the seq whose prefix the graph shows, -1 before the first row;
 *  in live mode it is always the head. `head` is the last seq held, -1 while the
 *  ledger is empty. `queued` counts the rows that arrived while scrubbed. */
export interface ScrubState {
  mode: ScrubMode;
  position: number;
  head: number;
  queued: number;
}

export type ScrubEvent =
  | { type: "ingest"; head: number }
  | { type: "scrub_to"; seq: number }
  | { type: "step"; delta: 1 | -1 }
  | { type: "step_phase"; delta: 1 | -1; stops: readonly number[] }
  | { type: "go_live" };

export function initialScrubState(head: number): ScrubState {
  return { mode: "live", position: head, head, queued: 0 };
}

function scrubbedAt(state: ScrubState, seq: number): ScrubState {
  const position = Math.max(-1, Math.min(state.head, seq));
  if (state.mode === "scrubbed" && state.position === position) return state;
  return { ...state, mode: "scrubbed", position };
}

/** One event folded into the scrubber. An event that changes nothing hands back
 *  the SAME object, so a caller can compare by reference. */
export function scrubReduce(state: ScrubState, event: ScrubEvent): ScrubState {
  switch (event.type) {
    case "ingest": {
      if (event.head <= state.head) return state;
      if (state.mode === "live") return { ...state, position: event.head, head: event.head };
      return { ...state, head: event.head, queued: state.queued + (event.head - state.head) };
    }
    case "scrub_to":
      if (state.head < 0) return state;
      return scrubbedAt(state, event.seq);
    case "step":
      if (state.head < 0) return state;
      if (state.mode === "live" && event.delta > 0) return state;
      return scrubbedAt(state, state.position + event.delta);
    case "step_phase": {
      if (state.head < 0) return state;
      if (event.delta > 0) {
        const next = event.stops.find((s) => s > state.position);
        if (next === undefined) return state.mode === "live" ? state : scrubbedAt(state, state.head);
        return scrubbedAt(state, next);
      }
      const earlier = event.stops.filter((s) => s < state.position);
      return scrubbedAt(state, earlier.length > 0 ? earlier[earlier.length - 1] : -1);
    }
    case "go_live":
      if (state.mode === "live") return state;
      return initialScrubState(state.head);
  }
}

/** True when more rows arrived behind the scrubbed view than a catch-up should
 *  replay: LIVE then refetches the ledger and says so. */
export function scrubOverflowed(state: ScrubState): boolean {
  return state.queued > SCRUB_QUEUE_CAP;
}

/** The keyboard, as the slider pattern and T5_F024.md name it: arrows step one
 *  event, Shift+arrows step one phase, Home goes before the first event and End
 *  returns to LIVE. Any other key is not the scrubber's. */
export function scrubKeyEvent(key: string, shiftKey: boolean, stops: readonly number[]): ScrubEvent | null {
  if (key === "ArrowLeft" || key === "ArrowRight") {
    const delta = key === "ArrowLeft" ? -1 : 1;
    return shiftKey ? { type: "step_phase", delta, stops } : { type: "step", delta };
  }
  if (key === "Home") return { type: "scrub_to", seq: -1 };
  if (key === "End") return { type: "go_live" };
  return null;
}

/** One frame of a catch-up: the seq to show and when, from the moment LIVE was
 *  pressed. */
export interface CatchUpFrame {
  atMs: number;
  seq: number;
}

/** LIVE's fast-forward from `from` to `to`: at most CATCH_UP_MAX_STEPS frames,
 *  evenly spread, CATCH_UP_STEP_MS apart, the last exactly at `to`. Under
 *  reduced motion the view jumps (ux_spec.md §16: progress jumps). */
export function catchUpPlan(from: number, to: number, reducedMotion: boolean): CatchUpFrame[] {
  if (to <= from) return [];
  if (reducedMotion) return [{ atMs: 0, seq: to }];
  const steps = Math.min(to - from, CATCH_UP_MAX_STEPS);
  const frames: CatchUpFrame[] = [];
  for (let k = 1; k <= steps; k += 1) {
    frames.push({ atMs: k * CATCH_UP_STEP_MS, seq: from + Math.round(((to - from) * k) / steps) });
  }
  return frames;
}
