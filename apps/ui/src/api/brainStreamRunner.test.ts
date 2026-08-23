import { describe, it, expect } from "vitest";
import { createBrainStreamRunner } from "./brainStreamRunner";
import { BRAIN_RECENT_LIMIT } from "./brainStream";
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
  return { kind: "frame", frame: { seq, event: { seq } }, receivedAtMs: 0 };
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

/** The driver is the only author of a `connect`. A restart after the fallback
 *  engaged must therefore resume on the fallback's terms, not reopen a stream
 *  the client already learned it cannot have (finding R-0627). */
describe("restarting after the fallback engaged", () => {
  it("polls on the driver's authority instead of reopening a stream", () => {
    const { host, runner } = started();
    runner.dispatch({ kind: "unsupported" });
    runner.stop();
    runner.start();
    expect(host.connects).toEqual([null]);
    expect(host.waits()).toEqual([3000, 3000]);
    expect(runner.view().status).toBe("delayed");
  });
});

/** The seam R22's hook reads. `useSyncExternalStore` needs a subscribe and a
 *  snapshot whose identity is stable, so both are pinned here. */
describe("the runner as a store", () => {
  it("hands back the same view object until something visibly changes", () => {
    const { runner } = started();
    const first = runner.view();
    expect(runner.view()).toBe(first);
    runner.dispatch({ kind: "opened" });
    const second = runner.view();
    expect(second).not.toBe(first);
    expect(runner.view()).toBe(second);
  });
  it("tells every listener once per visible change", () => {
    const { runner } = started();
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.dispatch({ kind: "opened" });
    expect(calls).toBe(1);
    runner.dispatch(frame(3));
    expect(calls).toBe(2);
  });
  it("stays silent when an event changes nothing a reader can see", () => {
    const { runner } = started();
    runner.dispatch({ kind: "opened" });
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.dispatch({ kind: "timer" });
    expect(calls).toBe(0);
  });
  it("stops calling a listener once it unsubscribes", () => {
    const { runner } = started();
    let calls = 0;
    const unsubscribe = runner.subscribe(() => { calls += 1; });
    runner.dispatch({ kind: "opened" });
    unsubscribe();
    runner.dispatch(frame(3));
    expect(calls).toBe(1);
  });
});

describe("the view publishes the ring", () => {
  it("seeds the cached view from the state, so start alone announces nothing", () => {
    const host = new RecordingHost();
    const runner = createBrainStreamRunner(host);
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.start();
    expect(calls).toBe(0);
    expect(runner.view().recent).toEqual([]);
    expect(runner.view().recentDropped).toBe(0);
  });

  it("carries each accepted frame's projected row onto the view", () => {
    const { runner } = started();
    runner.dispatch(frame(4));
    runner.dispatch(frame(5));
    expect(runner.view().recent.map((r) => r.seq)).toEqual([4, 5]);
  });

  it("holds the ring's identity across a replay, so no re-render is asked for", () => {
    const { runner } = started();
    runner.dispatch(frame(4));
    const before = runner.view();
    runner.dispatch(frame(4));
    expect(runner.view()).toBe(before);
    expect(runner.view().recent).toBe(before.recent);
  });

  it("publishes the drop count once the bound is passed", () => {
    const { runner } = started();
    for (let seq = 1; seq <= BRAIN_RECENT_LIMIT + 3; seq += 1) {
      runner.dispatch(frame(seq));
    }
    expect(runner.view().recent.length).toBe(BRAIN_RECENT_LIMIT);
    expect(runner.view().recentDropped).toBe(3);
  });
});

/** DECISION F022 D6: the view carries the latest tick and compares it with
 *  `===`, which is the whole reason the state carries it forward by reference. */
describe("the view publishes the budget tick", () => {
  function tick(seq: number, budget: unknown): BrainStreamEvent {
    return { kind: "frame", frame: { seq, event: { seq, event: "budget.tick", budget } }, receivedAtMs: 0 };
  }

  it("seeds the cached view from the state, so start alone announces nothing", () => {
    const host = new RecordingHost();
    const runner = createBrainStreamRunner(host);
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.start();
    expect(calls).toBe(0);
    expect(runner.view().budget).toBeNull();
  });

  it("publishes a tick's figures once", () => {
    const { runner } = started();
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    const budget = { spent_usd: 2, limit_usd: 8 };
    runner.dispatch(tick(1, budget));
    expect(runner.view().budget).toBe(budget);
    expect(calls).toBe(1);
  });

  it("a tick that changes nothing else still publishes exactly once", () => {
    // Honest about its own reach: an accepted frame always moves `lastSeq` and
    // the ring too, so this case cannot single out the `budget` comparison. It
    // pins the count — one wake per tick, never two — and the replay case below
    // is what pins that an UNaccepted tick wakes nobody.
    const { runner } = started();
    runner.dispatch(tick(1, { spent_usd: 1 }));
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.dispatch(tick(2, { spent_usd: 2 }));
    expect(calls).toBe(1);
  });

  it("a replayed tick republishes nothing and keeps the view identity", () => {
    const { runner } = started();
    const budget = { spent_usd: 2 };
    runner.dispatch(tick(4, budget));
    const before = runner.view();
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.dispatch(tick(4, { spent_usd: 99 }));
    expect(runner.view()).toBe(before);
    expect(runner.view().budget).toBe(budget);
    expect(calls).toBe(0);
  });

  it("a non-tick frame that follows leaves the figures reference-identical", () => {
    const { runner } = started();
    const budget = { spent_usd: 2 };
    runner.dispatch(tick(1, budget));
    runner.dispatch(frame(2));
    expect(runner.view().budget).toBe(budget);
  });

  it("a timer that changes nothing publishes not at all", () => {
    const { runner } = started();
    runner.dispatch(tick(1, { spent_usd: 2 }));
    let calls = 0;
    runner.subscribe(() => { calls += 1; });
    runner.dispatch({ kind: "timer" });
    expect(calls).toBe(0);
  });
});
