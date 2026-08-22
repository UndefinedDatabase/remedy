// Pure, framework-free client state for the SSE brain stream.
// Extracted from the React hook for the same reason cockpitLogic.ts was
// extracted from the panels: the node-environment vitest cannot render React,
// so the reconnect, gap and status rules live here where they can be tested.
import { feedRowOf } from "./feedRow";
import type { FeedRow } from "./feedRow";

// One-directional at RUNTIME though feedRow.ts names this module back: it takes
// `BrainStreamFrame` with `import type`, which TypeScript erases, so the emitted
// graph is brainStream -> feedRow -> humanize and terminates.

/** What the cockpit badge shows: a live stream, a retrying one, or polling. */
export type BrainStreamStatus = "live" | "reconnecting" | "delayed";

/** One frame as the server sends it: the ledger position IS the event id. */
export interface BrainStreamFrame {
  seq: number;
  event: unknown;
}

/** How many projected rows the ring holds. Nothing upstream supplies a bound —
 *  `packages/orchestration/ui_server.py` caps concurrent streams per job at
 *  SSE_MAX_STREAMS_PER_JOB and caps the event COUNT nowhere — so the client
 *  picks one: far past the handful a card shows, far short of a memory
 *  concern (DECISION F021 D5). */
export const BRAIN_RECENT_LIMIT = 500;

export interface BrainStreamState {
  status: BrainStreamStatus;
  /** The last seq the client actually HOLDS; null before the first frame. */
  lastSeq: number | null;
  /** A seq discontinuity was seen and no snapshot has repaired it yet. */
  gapDetected: boolean;
  /** Consecutive failed connection attempts; reset by a successful open. */
  attempt: number;
  /** The bounded ring of projected feed rows, OLDEST FIRST and at most
   *  BRAIN_RECENT_LIMIT of them. This is the feed's only data path. */
  recent: readonly FeedRow[];
  /** How many rows the ring has DROPPED past its bound. The drop is never
   *  silent: above zero the feed says so and points at the timeline. */
  recentDropped: number;
}

/** A client that holds nothing yet, and does not pretend to be live. */
export function initialBrainStreamState(): BrainStreamState {
  return {
    status: "reconnecting", lastSeq: null, gapDetected: false, attempt: 0,
    recent: [], recentDropped: 0,
  };
}

/** The `Last-Event-ID` value: the last frame HELD, never the next one wanted.
 *  The server adds the one — `resolve_sse_start` returns `int(text) + 1` — so
 *  a client sending its next-wanted seq would skip an event on every
 *  reconnect. Null means "send no header", which resumes from the cursor. */
export function resumeEventId(state: BrainStreamState): string | null {
  return state.lastSeq === null ? null : String(state.lastSeq);
}

/** An open connection is the only thing that makes the badge say live. */
export function openBrainStream(state: BrainStreamState): BrainStreamState {
  return { ...state, status: "live", attempt: 0 };
}

/** A dropped connection counts an attempt; the badge stops claiming live. */
export function failBrainStream(state: BrainStreamState): BrainStreamState {
  return { ...state, status: "reconnecting", attempt: state.attempt + 1 };
}

/** The fallback transport is honest about being slower than the stream. */
export function degradeBrainStream(state: BrainStreamState): BrainStreamState {
  return { ...state, status: "delayed" };
}

/** Applying a frame advances the held position and reports a discontinuity.
 *  A gap is `seq !== lastSeq + 1` — the disconnect hammer forbids both the
 *  duplicate and the hole, and the client must SEE the hole to ask for a
 *  snapshot. The first frame of a fresh client can carry any seq, because a
 *  resume from a cursor starts mid-ledger, so it never reports a gap. A frame
 *  at or behind the held position is a replay and is dropped. The projected
 *  feed row is appended HERE, behind that same early return — the only
 *  placement a reconnect replay cannot duplicate, since the runner's dispatch
 *  and the driver's reducer both see a frame before the guard has ruled on it
 *  (DECISION F021 D5). Dropping a replay returns the IDENTICAL state object,
 *  ring included, which is what lets a reader compare the ring by reference. */
export function receiveBrainFrame(
  state: BrainStreamState,
  frame: BrainStreamFrame,
  receivedAtMs: number,
): BrainStreamState {
  if (state.lastSeq !== null && frame.seq <= state.lastSeq) return state;
  const isGap = state.lastSeq !== null && frame.seq !== state.lastSeq + 1;
  const appended = [...state.recent, feedRowOf(frame, receivedAtMs)];
  const overflow = Math.max(0, appended.length - BRAIN_RECENT_LIMIT);
  return {
    ...state,
    status: state.status === "delayed" ? "delayed" : "live",
    lastSeq: frame.seq,
    gapDetected: state.gapDetected || isGap,
    attempt: 0,
    recent: overflow === 0 ? appended : appended.slice(overflow),
    recentDropped: state.recentDropped + overflow,
  };
}

/** A snapshot refetch is what repairs a gap: the held position jumps to the
 *  snapshot's own seq and the discontinuity is cleared. */
export function repairBrainGap(
  state: BrainStreamState,
  snapshotSeq: number,
): BrainStreamState {
  return { ...state, lastSeq: snapshotSeq, gapDetected: false };
}

/** Backoff floor and ceiling, named so the schedule and its tests cannot drift. */
export const BRAIN_BACKOFF_BASE_MS = 250;
export const BRAIN_BACKOFF_CAP_MS = 8000;

/** Reconnect backoff: doubling from the base, capped so a long outage still
 *  retries about every eight seconds rather than drifting into minutes. */
export function brainBackoffDelayMs(attempt: number): number {
  if (attempt <= 0) return 0;
  return Math.min(BRAIN_BACKOFF_BASE_MS * 2 ** (attempt - 1), BRAIN_BACKOFF_CAP_MS);
}
