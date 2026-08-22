import { describe, it, expect } from "vitest";
import { createBrainStreamHost } from "./brainStreamHost";
import type { BrainStreamMessage, BrainStreamSource } from "./brainStreamHost";
import type { BrainStreamFrame } from "./brainStream";
import type { BrainStreamEvent } from "./brainStreamDriver";

/** A hand-driven EventSource: its listeners fire when the TEST says so, never
 *  when a socket does, which is what lets this suite run with no DOM. */
class FakeSource implements BrainStreamSource {
  listeners = new Map<string, ((event: BrainStreamMessage) => void)[]>();
  closes = 0;

  addEventListener(type: string, listener: (event: BrainStreamMessage) => void): void {
    const bucket = this.listeners.get(type) ?? [];
    bucket.push(listener);
    this.listeners.set(type, bucket);
  }

  close(): void { this.closes += 1; }

  emit(type: string, event: BrainStreamMessage = {}): void {
    for (const listener of this.listeners.get(type) ?? []) listener(event);
  }
}

interface Harness {
  events: BrainStreamEvent[];
  sources: FakeSource[];
  opens: (string | null)[];
  tails: (number | null)[];
  waits: number[];
  host: ReturnType<typeof createBrainStreamHost>;
}

/** `absent` gives an environment with no EventSource at all. */
function harness(options: { absent?: boolean; snapshot?: number | null; tail?: BrainStreamFrame[] } = {}): Harness {
  const events: BrainStreamEvent[] = [];
  const sources: FakeSource[] = [];
  const opens: (string | null)[] = [];
  const tails: (number | null)[] = [];
  const waits: number[] = [];
  const host = createBrainStreamHost((event) => { events.push(event); }, {
    openSource(lastEventId: string | null): BrainStreamSource | null {
      opens.push(lastEventId);
      if (options.absent === true) return null;
      const source = new FakeSource();
      sources.push(source);
      return source;
    },
    readSnapshotSeq(): Promise<number | null> {
      return options.snapshot === undefined
        ? Promise.reject(new Error("no snapshot"))
        : Promise.resolve(options.snapshot);
    },
    readTail(afterSeq: number | null): Promise<BrainStreamFrame[]> {
      tails.push(afterSeq);
      return options.tail === undefined
        ? Promise.reject(new Error("no tail"))
        : Promise.resolve(options.tail);
    },
    schedule(ms: number, resume: () => void): () => void {
      waits.push(ms);
      resume();
      return () => { events.push({ kind: "timer" }); };
    },
    now(): number {
      return 1000;
    },
  });
  return { events, sources, opens, tails, waits, host };
}

/** Let the adapter's own `then` callbacks run before the assertions do. */
async function settle(): Promise<void> {
  await Promise.resolve();
  await Promise.resolve();
}

function payload(seq: number): string {
  return JSON.stringify({ seq, event: "task_started", timestamp: "", outcome: "" });
}

describe("an open stream", () => {
  it("carries the resume position to the source and reports the open", () => {
    const h = harness();
    h.host.connect("7");
    expect(h.opens).toEqual(["7"]);
    h.sources[0].emit("open");
    expect(h.events).toEqual([{ kind: "opened" }]);
  });
  it("surfaces a frame with the position the payload carries", () => {
    const h = harness();
    h.host.connect(null);
    h.sources[0].emit("message", { data: payload(4) });
    expect(h.events).toEqual([
      { kind: "frame", frame: { seq: 4, event: JSON.parse(payload(4)) }, receivedAtMs: 1000 },
    ]);
  });
  it("drops a malformed frame instead of dispatching a broken one", () => {
    const h = harness();
    h.host.connect(null);
    h.sources[0].emit("message", { data: "{not json" });
    h.sources[0].emit("message", { data: JSON.stringify({ event: "no seq" }) });
    h.sources[0].emit("message", {});
    expect(h.events).toEqual([]);
  });
  it("reports a closed transport and lets its socket go", () => {
    const h = harness();
    h.host.connect(null);
    h.sources[0].emit("error");
    expect(h.events).toEqual([{ kind: "closed" }]);
    expect(h.sources[0].closes).toBe(1);
  });
});

describe("an environment without EventSource", () => {
  it("reports unsupported rather than pretending to connect", () => {
    const h = harness({ absent: true });
    h.host.connect(null);
    expect(h.events).toEqual([{ kind: "unsupported" }]);
  });
});

describe("reconnecting", () => {
  it("closes the previous socket before opening the next", () => {
    const h = harness();
    h.host.connect(null);
    h.host.connect("3");
    expect(h.sources[0].closes).toBe(1);
    expect(h.sources[1].closes).toBe(0);
    expect(h.opens).toEqual([null, "3"]);
  });
});

describe("the snapshot read", () => {
  it("carries the repaired position and moves the polling cursor with it", async () => {
    const h = harness({ snapshot: 12, tail: [] });
    h.host.requestSnapshot();
    await settle();
    expect(h.events).toEqual([{ kind: "snapshot", seq: 12 }]);
    h.host.pollOnce();
    await settle();
    expect(h.tails).toEqual([12]);
  });
  it("reports a closed transport when the read fails or holds no position", async () => {
    const failed = harness();
    failed.host.requestSnapshot();
    const empty = harness({ snapshot: null });
    empty.host.requestSnapshot();
    await settle();
    expect(failed.events).toEqual([{ kind: "closed" }]);
    expect(empty.events).toEqual([{ kind: "closed" }]);
  });
});

describe("the polling fallback", () => {
  it("asks from the position the stream reached and surfaces each frame in order", async () => {
    const h = harness({ tail: [{ seq: 6, event: null }, { seq: 7, event: null }] });
    h.host.connect(null);
    h.sources[0].emit("message", { data: payload(5) });
    h.host.pollOnce();
    await settle();
    expect(h.tails).toEqual([5]);
    expect(h.events.slice(1)).toEqual([
      { kind: "frame", frame: { seq: 6, event: null }, receivedAtMs: 1000 },
      { kind: "frame", frame: { seq: 7, event: null }, receivedAtMs: 1000 },
    ]);
  });
  it("reports a closed transport when the tail read fails", async () => {
    const h = harness();
    h.host.pollOnce();
    await settle();
    expect(h.events).toEqual([{ kind: "closed" }]);
    expect(h.tails).toEqual([null]);
  });
});

describe("closing the host", () => {
  it("closes the open socket once, however often it is asked", () => {
    const h = harness();
    h.host.connect(null);
    h.host.close();
    h.host.close();
    expect(h.sources[0].closes).toBe(1);
  });
});

describe("scheduling", () => {
  it("runs through the injected scheduler rather than a timer of its own", () => {
    const h = harness();
    const cancel = h.host.schedule(250, () => { h.events.push({ kind: "opened" }); });
    expect(h.waits).toEqual([250]);
    expect(h.events).toEqual([{ kind: "opened" }]);
    cancel();
    expect(h.events).toEqual([{ kind: "opened" }, { kind: "timer" }]);
  });
});
