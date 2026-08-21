// Pure, framework-free client state for the SSE brain stream.
// Extracted from the React hook for the same reason cockpitLogic.ts was
// extracted from the panels: the node-environment vitest cannot render React,
// so the reconnect, gap and status rules live here where they can be tested.

/** What the cockpit badge shows: a live stream, a retrying one, or polling. */
export type BrainStreamStatus = "live" | "reconnecting" | "delayed";

/** One frame as the server sends it: the ledger position IS the event id. */
export interface BrainStreamFrame {
  seq: number;
  event: unknown;
}

export interface BrainStreamState {
  status: BrainStreamStatus;
  /** The last seq the client actually HOLDS; null before the first frame. */
  lastSeq: number | null;
  /** A seq discontinuity was seen and no snapshot has repaired it yet. */
  gapDetected: boolean;
  /** Consecutive failed connection attempts; reset by a successful open. */
  attempt: number;
}

/** A client that holds nothing yet, and does not pretend to be live. */
export function initialBrainStreamState(): BrainStreamState {
  return { status: "reconnecting", lastSeq: null, gapDetected: false, attempt: 0 };
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
 *  at or behind the held position is a replay and is dropped. */
export function receiveBrainFrame(
  state: BrainStreamState,
  frame: BrainStreamFrame,
): BrainStreamState {
  if (state.lastSeq !== null && frame.seq <= state.lastSeq) return state;
  const isGap = state.lastSeq !== null && frame.seq !== state.lastSeq + 1;
  return {
    ...state,
    status: state.status === "delayed" ? "delayed" : "live",
    lastSeq: frame.seq,
    gapDetected: state.gapDetected || isGap,
    attempt: 0,
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
