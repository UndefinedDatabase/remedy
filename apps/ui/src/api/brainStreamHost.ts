// The real environment behind BrainStreamHost: an EventSource for the stream,
// two api reads for the snapshot and the polling tail, and a scheduler for the
// backoff. Every one of them is INJECTED, so this adapter — the last piece
// between the driver and a browser — runs under the node-environment vitest
// with no DOM, no socket and no network.
import type { BrainStreamFrame } from "./brainStream";
import type { BrainStreamEvent } from "./brainStreamDriver";
import type { BrainStreamHost } from "./brainStreamRunner";

/** What a source hands a listener. Only `data` is read: the ledger position
 *  travels INSIDE the payload (`_safe_event_summary` in ui_server.py writes
 *  `seq` into it), so this client never depends on `lastEventId` surviving a
 *  proxy. */
export interface BrainStreamMessage {
  data?: string;
}

/** The only part of EventSource this client uses. Structural on purpose: the
 *  browser's EventSource satisfies it as-is, and a test fake is a dozen lines
 *  with no DOM behind them. */
export interface BrainStreamSource {
  addEventListener(type: string, listener: (event: BrainStreamMessage) => void): void;
  close(): void;
}

/** Everything the adapter needs from the world, named so a test can hand it
 *  four functions and a browser can hand it four different ones. */
export interface BrainStreamHostDeps {
  /** Open a stream at the resume position, or return null where this
   *  environment has no EventSource — that null IS the `unsupported` the
   *  polling fallback engages on. */
  openSource(lastEventId: string | null): BrainStreamSource | null;
  /** The current snapshot's ledger position, or null when it has none yet. */
  readSnapshotSeq(): Promise<number | null>;
  /** The frames STRICTLY AFTER the held position; null asks from the start.
   *  The caller passes what the client HOLDS, never the next seq it wants —
   *  the cursor arithmetic belongs to whoever builds the request. */
  readTail(afterSeq: number | null): Promise<BrainStreamFrame[]>;
  /** setTimeout in a browser, a hand-fired fake in a test. */
  schedule(ms: number, resume: () => void): () => void;
  /** The client's own clock. Injected like every other capability here, so a
   *  test hands it a counter and a browser hands it Date.now, and no module in
   *  this chain has to reach for a global to learn what time it is. */
  now(): number;
}

/** The adapter OWNS its socket, so `close` sits on the returned object rather
 *  than on BrainStreamHost: the runner never opens a stream and must not be
 *  taught to close one. A React hook closes it when the component unmounts. */
export function createBrainStreamHost(
  dispatch: (event: BrainStreamEvent) => void,
  deps: BrainStreamHostDeps,
): BrainStreamHost & { close(): void } {
  let source: BrainStreamSource | null = null;
  let held: number | null = null;

  /** Every frame the client is told about moves the polling cursor too, so the
   *  fallback resumes where the stream stopped instead of replaying it. */
  function tell(frame: BrainStreamFrame): void {
    held = frame.seq;
    dispatch({ kind: "frame", frame, receivedAtMs: deps.now() });
  }

  /** Closing is idempotent and always forgets the socket first: an `error`
   *  arriving out of a close must not close a stream opened after it. */
  function drop(): void {
    const spent = source;
    source = null;
    if (spent !== null) spent.close();
  }

  /** A malformed frame is DROPPED, never dispatched: the seq discontinuity it
   *  leaves is what asks for a snapshot, while a parse error says nothing
   *  about whether the transport is alive. */
  function receive(message: BrainStreamMessage): void {
    if (typeof message.data !== "string") return;
    let payload: unknown;
    try {
      payload = JSON.parse(message.data);
    } catch {
      return;
    }
    if (payload === null || typeof payload !== "object") return;
    const seq = (payload as { seq?: unknown }).seq;
    if (typeof seq !== "number") return;
    tell({ seq, event: payload });
  }

  return {
    connect(lastEventId: string | null): void {
      drop();
      let opened: BrainStreamSource | null = null;
      try {
        opened = deps.openSource(lastEventId);
      } catch {
        opened = null;
      }
      if (opened === null) {
        dispatch({ kind: "unsupported" });
        return;
      }
      source = opened;
      opened.addEventListener("open", () => { dispatch({ kind: "opened" }); });
      opened.addEventListener("message", receive);
      opened.addEventListener("error", () => { drop(); dispatch({ kind: "closed" }); });
    },
    requestSnapshot(): void {
      deps.readSnapshotSeq().then(
        (seq) => {
          if (seq === null) { dispatch({ kind: "closed" }); return; }
          held = seq;
          dispatch({ kind: "snapshot", seq });
        },
        () => { dispatch({ kind: "closed" }); },
      );
    },
    pollOnce(): void {
      deps.readTail(held).then(
        (frames) => { for (const frame of frames) tell(frame); },
        () => { dispatch({ kind: "closed" }); },
      );
    },
    schedule(ms: number, resume: () => void): () => void {
      return deps.schedule(ms, resume);
    },
    close(): void {
      drop();
    },
  };
}
