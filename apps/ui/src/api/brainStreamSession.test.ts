import { describe, it, expect } from "vitest";
import { createBrainStreamSession } from "./brainStreamSession";
import type { BrainStreamMessage, BrainStreamSource } from "./brainStreamHost";
import type { BrainStreamFrame } from "./brainStream";

/** A hand-driven EventSource, as in brainStreamHost.test.ts: its listeners fire
 *  when the TEST says so, never when a socket does. */
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

/** The scheduler RECORDS instead of firing: the runner re-arms a poll from
 *  inside the resume it just ran, so a fake that resumed synchronously would
 *  recurse forever rather than test anything. */
function harness(options: { absent?: boolean; tail?: BrainStreamFrame[] } = {}) {
  const sources: FakeSource[] = [];
  const opens: (string | null)[] = [];
  const tails: (number | null)[] = [];
  const waits: { ms: number; resume: () => void }[] = [];
  const session = createBrainStreamSession({
    openSource(lastEventId: string | null): BrainStreamSource | null {
      opens.push(lastEventId);
      if (options.absent === true) return null;
      const source = new FakeSource();
      sources.push(source);
      return source;
    },
    readSnapshotSeq(): Promise<number | null> { return Promise.resolve(null); },
    readTail(afterSeq: number | null): Promise<BrainStreamFrame[]> {
      tails.push(afterSeq);
      return Promise.resolve(options.tail ?? []);
    },
    schedule(ms: number, resume: () => void): () => void {
      waits.push({ ms, resume });
      return () => {};
    },
    now(): number {
      return 2000;
    },
  });
  return { sources, opens, tails, waits, session };
}

function payload(seq: number): string {
  return JSON.stringify({ seq, event: "task_started" });
}

describe("a composed brain stream session", () => {
  it("connects on start and reports no status until the transport answers", () => {
    const h = harness();
    expect(h.opens).toEqual([]);
    h.session.start();
    expect(h.opens).toEqual([null]);
    expect(h.session.view().status).toBeNull();
  });

  it("shows live once the source opens", () => {
    const h = harness();
    h.session.start();
    h.sources[0].emit("open");
    expect(h.session.view().status).toBe("live");
  });

  it("carries a frame's position into the view and wakes its subscribers", () => {
    const h = harness();
    let woken = 0;
    h.session.subscribe(() => { woken += 1; });
    h.session.start();
    h.sources[0].emit("message", { data: payload(4) });
    expect(h.session.view().lastSeq).toBe(4);
    expect(woken).toBe(1);
  });

  it("closes the socket when the caller closes the session", () => {
    const h = harness();
    h.session.start();
    h.sources[0].emit("open");
    h.session.close();
    expect(h.sources[0].closes).toBe(1);
  });

  it("performs nothing more once it is closed", () => {
    const h = harness();
    h.session.start();
    h.sources[0].emit("error");
    expect(h.waits).toHaveLength(1);
    h.session.close();
    h.waits[0].resume();
    expect(h.opens).toEqual([null]);
  });

  it("falls back to delayed polling where the environment has no EventSource", async () => {
    const h = harness({ absent: true });
    h.session.start();
    expect(h.session.view().status).toBe("delayed");
    expect(h.waits[0].ms).toBe(3000);
    h.waits[0].resume();
    await Promise.resolve();
    expect(h.tails).toEqual([null]);
  });
});
