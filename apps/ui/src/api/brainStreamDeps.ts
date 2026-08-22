// The real BrainStreamHostDeps: the SSE endpoint T001 built and the
// events-since transport T002 shares with it, turned into the four functions
// createBrainStreamHost asks for. Every piece of the world it needs arrives as
// an injected BrainStreamEnv rather than as a global, so all of it runs under
// the node-environment vitest with no DOM, no socket and no network. Remedy
// deliberately does not build that env from globalThis here: binding the real
// EventSource, fetch and timer belongs with the cockpit wiring that has them.
import type { BrainStreamFrame } from "./brainStream";
import type { BrainStreamHostDeps, BrainStreamSource } from "./brainStreamHost";

/** The events-since envelope, as `_build_events_since_json` in ui_server.py
 *  writes it. Only the two fields this client reads are named: `cursor` is the
 *  ledger's LENGTH as a string, and `events` carries one `_safe_event_summary`
 *  per ledger position. */
interface EventsSincePayload {
  cursor?: unknown;
  events?: unknown;
}

/** Everything the factory needs from the world, so a test hands it three
 *  functions and the cockpit hands it three different ones. */
export interface BrainStreamEnv {
  /** null in an environment with no EventSource — that null is what
   *  `createBrainStreamHost` turns into the `unsupported` its polling fallback
   *  engages on. */
  makeSource: ((url: string) => BrainStreamSource) | null;
  /** GET the path and parse its JSON body; rejects on a non-2xx status. */
  fetchJson(path: string): Promise<unknown>;
  /** setTimeout in a browser, a hand-fired fake in a test. The returned
   *  function cancels the pending resume. */
  setTimer(ms: number, resume: () => void): () => void;
  /** The client's own clock, carried beside the transport whose frames it will
   *  stamp. Injected for the same reason the timer is: real time is the one
   *  dependency a headless test cannot wait for. */
  now(): number;
}

/** The cursor arithmetic, in the ONE place that builds requests. The client
 *  holds a seq; the endpoint's `cursor` names the position to start AT; so a
 *  holder of S asks for S+1. `resolve_sse_start` adds that same one for the
 *  Last-Event-ID header, which is what makes a resume replay nothing and skip
 *  nothing whichever way the client resumes. */
export function cursorAfter(heldSeq: number | null): number {
  return heldSeq === null ? 0 : heldSeq + 1;
}

/** Turn the envelope's `cursor` — the ledger's LENGTH — into the position of
 *  its last event, which is what a resuming client HOLDS. An empty ledger has
 *  no position, and that null is what tells the driver to keep waiting rather
 *  than resume from a frame that was never sent. */
export function snapshotSeqOf(payload: unknown): number | null {
  if (payload === null || typeof payload !== "object") return null;
  const cursor = (payload as EventsSincePayload).cursor;
  const length = typeof cursor === "string" ? Number(cursor) : cursor;
  if (typeof length !== "number" || !Number.isFinite(length) || length <= 0) return null;
  return length - 1;
}

/** The frames of one events-since response, in ledger order. An entry with no
 *  numeric `seq` is DROPPED rather than renumbered: a client that invented a
 *  position would resume from a frame the server never sent. */
export function framesOf(payload: unknown): BrainStreamFrame[] {
  if (payload === null || typeof payload !== "object") return [];
  const events = (payload as EventsSincePayload).events;
  if (!Array.isArray(events)) return [];
  const frames: BrainStreamFrame[] = [];
  for (const entry of events) {
    if (entry === null || typeof entry !== "object") continue;
    const seq = (entry as { seq?: unknown }).seq;
    if (typeof seq !== "number") continue;
    frames.push({ seq, event: entry });
  }
  return frames;
}

/** Build the four functions `createBrainStreamHost` needs, for ONE job.
 *
 *  The two paths are the two transports of one envelope:
 *  `/api/jobs/<id>/events/stream` streams it, and `/api/jobs/<id>/events-since`
 *  answers the snapshot and the polling tail out of the same ledger. */
export function createBrainStreamHostDeps(jobId: string, env: BrainStreamEnv): BrainStreamHostDeps {
  const job = encodeURIComponent(jobId);
  const since = (cursor: number): string => `/api/jobs/${job}/events-since?cursor=${cursor}`;
  return {
    openSource(lastEventId: string | null): BrainStreamSource | null {
      const make = env.makeSource;
      if (make === null) return null;
      const held = lastEventId === null ? Number.NaN : Number(lastEventId);
      const from = Number.isFinite(held) ? cursorAfter(held) : 0;
      return make(`/api/jobs/${job}/events/stream?cursor=${from}`);
    },
    readSnapshotSeq(): Promise<number | null> {
      return env.fetchJson(since(0)).then(snapshotSeqOf);
    },
    readTail(afterSeq: number | null): Promise<BrainStreamFrame[]> {
      return env.fetchJson(since(cursorAfter(afterSeq))).then(framesOf);
    },
    schedule(ms: number, resume: () => void): () => void {
      return env.setTimer(ms, resume);
    },
    now(): number {
      return env.now();
    },
  };
}

/** The globals the browser environment is built from, taken as an argument
 *  rather than read off `globalThis`, so a test can present an environment
 *  WITHOUT EventSource without depending on which runtime is running it. */
export interface BrainStreamGlobals {
  EventSource?: new (url: string) => BrainStreamSource;
  fetch(path: string, init?: { method: "GET"; credentials: "same-origin" }): Promise<{
    ok: boolean;
    status: number;
    json(): Promise<unknown>;
  }>;
  setTimeout(resume: () => void, ms: number): unknown;
  clearTimeout(handle: unknown): void;
  /** Taken as an injected global like the others rather than called directly,
   *  so a test can present a clock it controls without touching real time.
   *  `window.Date` satisfies this structurally, which is what keeps
   *  RemedyShell.tsx's `browserBrainStreamEnv(window)` compiling unchanged. */
  Date: { now(): number };
}

/** Bind the injected environment to real globals. A runtime with no
 *  EventSource yields `makeSource: null`, which is exactly the `unsupported`
 *  the polling fallback engages on — the client degrades to DELAYED instead of
 *  claiming a liveness it does not have. */
export function browserBrainStreamEnv(globals: BrainStreamGlobals): BrainStreamEnv {
  const Source = globals.EventSource;
  return {
    makeSource: Source === undefined ? null : (url: string): BrainStreamSource => new Source(url),
    fetchJson(path: string): Promise<unknown> {
      return globals
        .fetch(path, { method: "GET", credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw new Error(`Request failed ${response.status}: ${path}`);
          return response.json();
        });
    },
    setTimer(ms: number, resume: () => void): () => void {
      const handle = globals.setTimeout(resume, ms);
      return (): void => { globals.clearTimeout(handle); };
    },
    now(): number {
      return globals.Date.now();
    },
  };
}
