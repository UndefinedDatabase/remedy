// Effect interpretation for the brain stream: the loop that PERFORMS what
// brainStreamDriver decides, by turning its effects into calls on an INJECTED
// host. That is what lets the whole connect, backoff, snapshot and poll cycle
// run under the node-environment vitest — no EventSource, no timer, no React.
import { initialBrainStreamState, resumeEventId } from "./brainStream";
import type { BrainStreamStatus } from "./brainStream";
import { stepBrainStream } from "./brainStreamDriver";
import type { BrainStreamEffect, BrainStreamEvent } from "./brainStreamDriver";

/** What the runner asks of its environment: an EventSource, setTimeout and two
 *  api reads in production, four recorders in a test. */
export interface BrainStreamHost {
  /** Open a stream from the resume position; frames arrive via `dispatch`. */
  connect(lastEventId: string | null): void;
  /** Refetch the state snapshot; its position arrives as a `snapshot` event. */
  requestSnapshot(): void;
  /** Read the events tail once, on the polling fallback's cadence. */
  pollOnce(): void;
  /** Run `resume` after `ms`. The returned function cancels that pending run. */
  schedule(ms: number, resume: () => void): () => void;
}

/** What a badge reads. `status` is NULL until the first transport event has
 *  resolved, because a client that has never connected has no honest status and
 *  the initial `reconnecting` would claim a history it does not have (finding
 *  R-0624). Null is not a fourth status: the union the feature file fixes is
 *  untouched and the runner simply declines to report before it knows. */
export interface BrainStreamView {
  status: BrainStreamStatus | null;
  lastSeq: number | null;
  gapDetected: boolean;
}

export interface BrainStreamRunner {
  start(): void;
  dispatch(event: BrainStreamEvent): void;
  stop(): void;
  view(): BrainStreamView;
}

/** Remedy deliberately gives this no change callback yet: nothing subscribes
 *  until R19's hook exists, and a listener with no reader is untestable. */
export function createBrainStreamRunner(host: BrainStreamHost): BrainStreamRunner {
  let state = initialBrainStreamState();
  let settled = false;
  let stopped = false;
  let cancelPending: (() => void) | null = null;

  function view(): BrainStreamView {
    return {
      status: settled ? state.status : null,
      lastSeq: state.lastSeq,
      gapDetected: state.gapDetected,
    };
  }

  /** At most one timer outstanding: a second wait armed over a pending one
   *  would double the reconnect rate the backoff exists to bound. */
  function arm(ms: number, resume: () => void): void {
    if (cancelPending !== null) cancelPending();
    cancelPending = host.schedule(ms, () => {
      cancelPending = null;
      if (!stopped) resume();
    });
  }

  function perform(effect: BrainStreamEffect): void {
    switch (effect.kind) {
      case "connect":
        host.connect(effect.lastEventId);
        return;
      case "snapshot":
        host.requestSnapshot();
        return;
      case "wait":
        arm(effect.ms, () => { dispatch({ kind: "timer" }); });
        return;
      case "poll":
        arm(effect.ms, () => { host.pollOnce(); dispatch({ kind: "timer" }); });
        return;
    }
  }

  /** A `timer` is the runner's own bookkeeping, so it never resolves the
   *  status: only an event the TRANSPORT produced says what to show. */
  function dispatch(event: BrainStreamEvent): void {
    if (stopped) return;
    const step = stepBrainStream(state, event);
    state = step.state;
    if (event.kind !== "timer") settled = true;
    for (const effect of step.effects) perform(effect);
  }

  return {
    start(): void {
      stopped = false;
      host.connect(resumeEventId(state));
    },
    dispatch,
    stop(): void {
      stopped = true;
      if (cancelPending !== null) cancelPending();
      cancelPending = null;
    },
    view,
  };
}
