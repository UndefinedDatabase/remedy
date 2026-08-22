import { describe, it, expect } from "vitest";
import { browserBrainStreamEnv, createBrainStreamHostDeps, cursorAfter, framesOf, snapshotSeqOf } from "./brainStreamDeps";
import type { BrainStreamEnv, BrainStreamGlobals } from "./brainStreamDeps";
import type { BrainStreamMessage, BrainStreamSource } from "./brainStreamHost";

/** A source that records nothing but its own construction: these tests are
 *  about the URL the factory builds, never about what a socket does with it. */
class FakeSource implements BrainStreamSource {
  addEventListener(_type: string, _listener: (event: BrainStreamMessage) => void): void {}
  close(): void {}
}

interface Recorder {
  urls: string[];
  paths: string[];
  timers: number[];
  env: BrainStreamEnv;
}

/** `absent` gives an environment with no EventSource; `payload` is what the
 *  one injected reader answers every request with. */
function recorder(options: { absent?: boolean; payload?: unknown } = {}): Recorder {
  const urls: string[] = [];
  const paths: string[] = [];
  const timers: number[] = [];
  return {
    urls,
    paths,
    timers,
    env: {
      makeSource: options.absent === true
        ? null
        : (url: string): BrainStreamSource => { urls.push(url); return new FakeSource(); },
      fetchJson(path: string): Promise<unknown> {
        paths.push(path);
        return Promise.resolve(options.payload);
      },
      setTimer(ms: number, _resume: () => void): () => void {
        timers.push(ms);
        return (): void => { timers.push(-ms); };
      },
      now(): number {
        return 4242;
      },
    },
  };
}

describe("the cursor arithmetic", () => {
  it("asks for the position after the one it holds", () => {
    expect(cursorAfter(7)).toBe(8);
    expect(cursorAfter(0)).toBe(1);
  });

  it("asks from the start when it holds nothing", () => {
    expect(cursorAfter(null)).toBe(0);
  });
});

describe("reading the events-since envelope", () => {
  it("reads the last position out of the ledger length the server sends as a string", () => {
    expect(snapshotSeqOf({ cursor: "3" })).toBe(2);
  });

  it("has no position for an empty ledger, a missing cursor or a non-object", () => {
    expect(snapshotSeqOf({ cursor: "0" })).toBeNull();
    expect(snapshotSeqOf({})).toBeNull();
    expect(snapshotSeqOf(null)).toBeNull();
    expect(snapshotSeqOf({ cursor: "not a number" })).toBeNull();
  });

  it("carries the whole summary as the frame's event, keyed by the ledger's own seq", () => {
    const frames = framesOf({ events: [{ seq: 4, event: "test_run_completed" }] });
    expect(frames).toEqual([{ seq: 4, event: { seq: 4, event: "test_run_completed" } }]);
  });

  it("drops an entry with no numeric seq rather than renumbering it", () => {
    expect(framesOf({ events: [{ event: "no seq" }, { seq: 2 }] })).toEqual([{ seq: 2, event: { seq: 2 } }]);
    expect(framesOf({ events: "not an array" })).toEqual([]);
  });
});

describe("the host deps over the real endpoints", () => {
  it("opens the stream one position after the frame it holds", () => {
    const r = recorder();
    createBrainStreamHostDeps("job-1", r.env).openSource("7");
    expect(r.urls).toEqual(["/api/jobs/job-1/events/stream?cursor=8"]);
  });

  it("opens the stream from the start when it holds nothing, and escapes the job id", () => {
    const r = recorder();
    createBrainStreamHostDeps("a/b", r.env).openSource(null);
    expect(r.urls).toEqual(["/api/jobs/a%2Fb/events/stream?cursor=0"]);
  });

  it("reports no source at all where the environment has no EventSource", () => {
    const r = recorder({ absent: true });
    expect(createBrainStreamHostDeps("job-1", r.env).openSource(null)).toBeNull();
    expect(r.urls).toEqual([]);
  });

  it("reads the snapshot position from the whole ledger", async () => {
    const r = recorder({ payload: { cursor: "5" } });
    await expect(createBrainStreamHostDeps("job-1", r.env).readSnapshotSeq()).resolves.toBe(4);
    expect(r.paths).toEqual(["/api/jobs/job-1/events-since?cursor=0"]);
  });

  it("polls the tail strictly after the position it holds", async () => {
    const r = recorder({ payload: { events: [{ seq: 9 }] } });
    const deps = createBrainStreamHostDeps("job-1", r.env);
    await expect(deps.readTail(8)).resolves.toEqual([{ seq: 9, event: { seq: 9 } }]);
    await deps.readTail(null);
    expect(r.paths).toEqual([
      "/api/jobs/job-1/events-since?cursor=9",
      "/api/jobs/job-1/events-since?cursor=0",
    ]);
  });

  it("hands the backoff straight to the environment's timer", () => {
    const r = recorder();
    const cancel = createBrainStreamHostDeps("job-1", r.env).schedule(250, () => {});
    cancel();
    expect(r.timers).toEqual([250, -250]);
  });

  it("reads the clock through the environment rather than a real one", () => {
    const r = recorder();
    expect(createBrainStreamHostDeps("job-1", r.env).now()).toBe(4242);
  });
});

describe("the browser environment", () => {
  interface Globals extends BrainStreamGlobals { cleared: unknown[]; }

  function globals(options: { source?: boolean; ok?: boolean } = {}): Globals {
    const cleared: unknown[] = [];
    const base = {
      cleared,
      fetch(_path: string): Promise<{ ok: boolean; status: number; json(): Promise<unknown> }> {
        return Promise.resolve({
          ok: options.ok !== false,
          status: options.ok === false ? 503 : 200,
          json: (): Promise<unknown> => Promise.resolve({ cursor: "2" }),
        });
      },
      setTimeout(resume: () => void, _ms: number): unknown { resume(); return "handle"; },
      clearTimeout(handle: unknown): void { cleared.push(handle); },
      Date: { now: (): number => 777 },
    };
    return options.source === true ? { ...base, EventSource: FakeSource } : base;
  }

  it("has no source where the runtime lacks EventSource, and one where it has it", () => {
    expect(browserBrainStreamEnv(globals()).makeSource).toBeNull();
    const make = browserBrainStreamEnv(globals({ source: true })).makeSource;
    expect(make).not.toBeNull();
    expect(make?.("/api/jobs/job-1/events/stream?cursor=0")).toBeInstanceOf(FakeSource);
  });

  it("parses a successful body and refuses a failed status", async () => {
    await expect(browserBrainStreamEnv(globals()).fetchJson("/p")).resolves.toEqual({ cursor: "2" });
    await expect(browserBrainStreamEnv(globals({ ok: false })).fetchJson("/p")).rejects.toThrow("503");
  });

  it("cancels a scheduled resume through the global it was given", () => {
    const g = globals();
    let resumed = 0;
    browserBrainStreamEnv(g).setTimer(10, () => { resumed += 1; })();
    expect(resumed).toBe(1);
    expect(g.cleared).toEqual(["handle"]);
  });

  it("reads the clock off the injected global, never a real one", () => {
    expect(browserBrainStreamEnv(globals()).now()).toBe(777);
  });
});
