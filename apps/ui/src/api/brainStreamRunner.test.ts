import { describe, it, expect } from "vitest";
import { createBrainStreamRunner } from "./brainStreamRunner";
import type { BrainStreamHost, BrainStreamRunner } from "./brainStreamRunner";
import type { BrainStreamEvent } from "./brainStreamDriver";

interface ArmedTimer { ms: number; resume: () => void; spent: boolean }

/** Records every call and holds its timers until fired by hand, so the
 *  reconnect and poll cadences are read as data instead of waited for. */
class RecordingHost implements BrainStreamHost {
  connects: (string | null)[] = [];
  snapshots = 0;
  polls = 0;
  timers: ArmedTimer[] = [];

  connect(lastEventId: string | null): void { this.connects.push(lastEventId); }
  requestSnapshot(): void { this.snapshots += 1; }
  pollOnce(): void { this.polls += 1; }
  schedule(ms: number, resume: () => void): () => void {
    const armed: ArmedTimer = { ms, resume, spent: false };
    this.timers.push(armed);
    return () => { armed.spent = true; };
  }

  /** Fire the newest live timer — the only one the runner treats as pending. */
  tick(): void {
    for (let i = this.timers.length - 1; i >= 0; i -= 1) {
      const armed = this.timers[i];
      if (!armed.spent) { armed.spent = true; armed.resume(); return; }
    }
    throw new Error("no live timer to fire");
  }

  live(): number { return this.timers.filter((t) => !t.spent).length; }
  waits(): number[] { return this.timers.map((t) => t.ms); }
}

function started(): { host: RecordingHost; runner: BrainStreamRunner } {
  const host = new RecordingHost();
  const runner = createBrainStreamRunner(host);
  runner.start();
  return { host, runner };
}

function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } } };
}

describe("a runner that has not connected", () => {
  it("reports no status at all rather than claiming a reconnect", () => {
    const host = new RecordingHost();
    const runner = createBrainStreamRunner(host);
    expect(runner.view().status).toBe(null);
    runner.start();
    expect(runner.view().status).toBe(null);
    expect(host.connects).toEqual([null]);
  });
  it("is not resolved by a stray timer, which is its own bookkeeping", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "timer" });
    expect(runner.view().status).toBe(null);
    expect(host.connects).toEqual([null, null]);
  });
  it("resolves the status on the first transport event", () => {
    const { runner } = started();
    runner.dispatch({ kind: "opened" });
    expect(runner.view().status).toBe("live");
  });
});

describe("a dropped connection", () => {
  it("arms the backoff and reconnects from the frame it holds", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "opened" });
    runner.dispatch(frame(7));
    runner.dispatch({ kind: "closed" });
    expect(host.waits()).toEqual([250]);
    expect(host.connects).toEqual([null]);
    host.tick();
    expect(host.connects).toEqual([null, "7"]);
  });
  it("lengthens the armed wait on every further drop", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "closed" });
    runner.dispatch({ kind: "closed" });
    runner.dispatch({ kind: "closed" });
    expect(host.waits()).toEqual([250, 500, 1000]);
  });
  it("keeps at most one timer live so the rate stays bounded", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "closed" });
    runner.dispatch({ kind: "closed" });
    expect(host.timers.length).toBe(2);
    expect(host.live()).toBe(1);
  });
});

describe("a gap in the sequence", () => {
  it("asks the host for a snapshot exactly once", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "opened" });
    runner.dispatch(frame(0));
    runner.dispatch(frame(4));
    runner.dispatch(frame(5));
    expect(host.snapshots).toBe(1);
  });
  it("reconnects from the healed position once the snapshot lands", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "opened" });
    runner.dispatch(frame(0));
    runner.dispatch(frame(4));
    runner.dispatch({ kind: "snapshot", seq: 9 });
    expect(host.connects).toEqual([null, "9"]);
    expect(runner.view().gapDetected).toBe(false);
    expect(runner.view().lastSeq).toBe(9);
  });
});

describe("the polling fallback", () => {
  it("engages on an unsupported transport and labels itself delayed", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "unsupported" });
    expect(runner.view().status).toBe("delayed");
    expect(host.waits()).toEqual([3000]);
  });
  it("reads the tail once per tick and re-arms the next one", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "unsupported" });
    host.tick();
    expect(host.polls).toBe(1);
    expect(host.live()).toBe(1);
    host.tick();
    expect(host.polls).toBe(2);
    expect(host.connects).toEqual([null]);
  });
});

describe("stopping the runner", () => {
  it("cancels the pending timer and ignores every later event", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "closed" });
    runner.stop();
    expect(host.live()).toBe(0);
    runner.dispatch({ kind: "opened" });
    expect(runner.view().status).toBe("reconnecting");
    expect(host.connects).toEqual([null]);
  });
});
