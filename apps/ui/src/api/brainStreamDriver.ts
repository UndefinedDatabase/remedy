// Transport orchestration for the brain stream, as a pure reducer.
// The rules in brainStream.ts say what a client HOLDS; these say what it
// should DO next — reconnect, wait, refetch a snapshot, or fall back to
// polling. Effects are returned as DATA rather than performed, so the whole
// reconnect and fallback story is testable under the node-environment vitest
// that cannot render the React hook which will interpret them.
import {
  brainBackoffDelayMs, degradeBrainStream, failBrainStream, openBrainStream,
  receiveBrainFrame, repairBrainGap, resumeEventId,
} from "./brainStream";
import type { BrainStreamFrame, BrainStreamState } from "./brainStream";

/** How often the fallback transport re-reads the events tail. */
export const BRAIN_POLL_INTERVAL_MS = 3000;

/** What the transport tells the driver. `unsupported` is the fallback trigger:
 *  no EventSource in this environment, or the stream failed to construct.
 *
 *  A frame carries `receivedAtMs`: the instant the HOST saw it, read from the
 *  clock R22 injected. T5_F021's activity dot subtracts two numbers, and the
 *  envelope's own `timestamp` is a server-clock string ui_server.py passes
 *  through unparsed and empty where the run log has none — so a server running
 *  behind would read as a dead agent. Stamping on arrival keeps both operands
 *  on ONE clock. The driver only CARRIES the value; the ring consumes it. */
export type BrainStreamEvent =
  | { kind: "opened" }
  | { kind: "frame"; frame: BrainStreamFrame; receivedAtMs: number }
  | { kind: "closed" }
  | { kind: "unsupported" }
  | { kind: "snapshot"; seq: number }
  | { kind: "timer" };

/** What the driver asks its host to do. The host performs these; the driver
 *  never touches a socket, a timer or the network itself. */
export type BrainStreamEffect =
  | { kind: "connect"; lastEventId: string | null }
  | { kind: "wait"; ms: number }
  | { kind: "snapshot" }
  | { kind: "poll"; ms: number };

export interface BrainStreamStep {
  state: BrainStreamState;
  effects: BrainStreamEffect[];
}

/** True once the fallback has engaged: `delayed` is sticky for this session,
 *  because a transport that could not be constructed will not spontaneously
 *  become constructible, and a badge that flickered back to `live` would be
 *  claiming a stream the client does not have. */
function isPolling(state: BrainStreamState): boolean {
  return state.status === "delayed";
}

/** Resume where the fallback left off, on the same rule as the stream: the
 *  two transports share one consumer contract and one resume position. */
function resumeEffect(state: BrainStreamState): BrainStreamEffect {
  return isPolling(state)
    ? { kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }
    : { kind: "connect", lastEventId: resumeEventId(state) };
}

/** Advance the client by one transport event, returning the next state and
 *  the effects the host must perform. A gap ALWAYS asks for a snapshot before
 *  anything else: replaying from a position the client never held is how a
 *  hole becomes permanent. */
export function stepBrainStream(
  state: BrainStreamState,
  event: BrainStreamEvent,
): BrainStreamStep {
  switch (event.kind) {
    case "opened":
      return { state: openBrainStream(state), effects: [] };

    case "frame": {
      const next = receiveBrainFrame(state, event.frame, event.receivedAtMs);
      const gapOpened = next.gapDetected && !state.gapDetected;
      return { state: next, effects: gapOpened ? [{ kind: "snapshot" }] : [] };
    }

    case "snapshot": {
      const healed = repairBrainGap(state, event.seq);
      return { state: healed, effects: [resumeEffect(healed)] };
    }

    case "closed": {
      if (isPolling(state)) return { state, effects: [{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }] };
      const next = failBrainStream(state);
      return { state: next, effects: [{ kind: "wait", ms: brainBackoffDelayMs(next.attempt) }] };
    }

    case "unsupported": {
      const next = degradeBrainStream(state);
      return { state: next, effects: [{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }] };
    }

    case "timer":
      return { state, effects: [resumeEffect(state)] };
  }
}
