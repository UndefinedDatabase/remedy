// Effect interpretation for the brain stream: the loop that PERFORMS what
// brainStreamDriver decides, by turning its effects into calls on an INJECTED
// host. That is what lets the whole connect, backoff, snapshot and poll cycle
// run under the node-environment vitest — no EventSource, no timer, no React.
import { initialBrainStreamState } from "./brainStream";
import type { BrainStreamStatus } from "./brainStream";
import type { BudgetTickFigures } from "./costMetric";
import type { FeedRow } from "./feedRow";
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
  /** The bounded ring `receiveBrainFrame` maintains, oldest first. Compared by
   *  REFERENCE below, so it is the same array until a frame is accepted. */
  recent: readonly FeedRow[];
  /** Rows dropped past the bound. Above zero, the feed says so rather than
   *  quietly showing a window (DECISION F021 D5). */
  recentDropped: number;
  /** The latest budget tick's figures, null before the first tick. Compared by
   *  REFERENCE below, which is why `receiveBrainFrame` carries the previous
   *  value forward rather than copying it (DECISION F022 D6). The type is
   *  NAMED and never an inline object literal: `test_brain_stream_ring.py`
   *  slices this interface at its first closing brace. */
  budget: BudgetTickFigures | null;
}

export interface BrainStreamRunner {
  start(): void;
  dispatch(event: BrainStreamEvent): void;
  stop(): void;
  view(): BrainStreamView;
  /** Hear about every visible change. The returned function unsubscribes. */
  subscribe(listener: () => void): () => void;
}

/** The runner IS a store: `subscribe` plus a `view` whose object identity only
 *  changes when something visible does are exactly the pair React's
 *  `useSyncExternalStore` requires, so the hook holds no state of its own. */
export function createBrainStreamRunner(host: BrainStreamHost): BrainStreamRunner {
  let state = initialBrainStreamState();
  let settled = false;
  let stopped = false;
  let cancelPending: (() => void) | null = null;
  const listeners = new Set<() => void>();
  // Seeded FROM `state`, never from a fresh `[]`. `publish` compares the ring
  // by reference, and an empty literal here is a DIFFERENT array from the
  // equally empty one the initial state holds, so the first timer — which
  // changes nothing a reader can see — would announce a change nobody made.
  let cachedView: BrainStreamView = {
    status: null,
    lastSeq: null,
    gapDetected: false,
    recent: state.recent,
    recentDropped: state.recentDropped,
    budget: state.budget,
  };

  /** The SAME object until something a reader can see changes. React's
   *  `useSyncExternalStore` compares snapshots with `Object.is` and re-renders
   *  forever if a store hands back a fresh object every call, so this identity
   *  is a contract of the seam rather than an optimisation. */
  function view(): BrainStreamView {
    return cachedView;
  }

  /** Recompute what a reader would see; publish and announce it only if it
   *  actually moved, so a timer that changes nothing wakes nobody. */
  function publish(): void {
    const next: BrainStreamView = {
      status: settled ? state.status : null,
      lastSeq: state.lastSeq,
      gapDetected: state.gapDetected,
      recent: state.recent,
      recentDropped: state.recentDropped,
      budget: state.budget,
    };
    if (next.status === cachedView.status
      && next.lastSeq === cachedView.lastSeq
      && next.gapDetected === cachedView.gapDetected
      && next.recent === cachedView.recent
      && next.recentDropped === cachedView.recentDropped
      && next.budget === cachedView.budget) return;
    cachedView = next;
    for (const listener of listeners) listener();
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
    publish();
    for (const effect of step.effects) perform(effect);
  }

  return {
    start(): void {
      stopped = false;
      dispatch({ kind: "timer" });
    },
    dispatch,
    stop(): void {
      stopped = true;
      if (cancelPending !== null) cancelPending();
      cancelPending = null;
    },
    view,
    subscribe(listener: () => void): () => void {
      listeners.add(listener);
      return () => { listeners.delete(listener); };
    },
  };
}
