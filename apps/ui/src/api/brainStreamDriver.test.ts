import { describe, it, expect } from "vitest";
import { initialBrainStreamState, openBrainStream, resumeEventId } from "./brainStream";
import { BRAIN_POLL_INTERVAL_MS, stepBrainStream } from "./brainStreamDriver";
import type { BrainStreamEvent } from "./brainStreamDriver";
import type { BrainStreamState } from "./brainStream";

/** Run a script of transport events, collecting every effect in order. */
function runScript(state: BrainStreamState, events: BrainStreamEvent[]) {
  const effects = [];
  let current = state;
  for (const event of events) {
    const step = stepBrainStream(current, event);
    current = step.state;
    effects.push(...step.effects);
  }
  return { state: current, effects };
}

/** The last effect a script produced. `Array.prototype.at` is newer than this
 *  project's TypeScript lib target, so the index is spelled out. */
function lastOf<T>(items: T[]): T {
  return items[items.length - 1];
}

function frame(seq: number): BrainStreamEvent {
  return { kind: "frame", frame: { seq, event: { seq } }, receivedAtMs: 0 };
}

describe("a clean stream", () => {
  it("opening asks for nothing and reports live", () => {
    const step = stepBrainStream(initialBrainStreamState(), { kind: "opened" });
    expect(step.effects).toEqual([]);
    expect(step.state.status).toBe("live");
  });
  it("contiguous frames ask for nothing", () => {
    const r = runScript(initialBrainStreamState(),
      [{ kind: "opened" }, frame(0), frame(1), frame(2)]);
    expect(r.effects).toEqual([]);
    expect(r.state.lastSeq).toBe(2);
    expect(r.state.status).toBe("live");
  });
});

describe("a dropped connection", () => {
  it("waits the backoff and then reconnects from the frame it holds", () => {
    const r = runScript(initialBrainStreamState(),
      [{ kind: "opened" }, frame(0), frame(1), { kind: "closed" }]);
    expect(r.effects).toEqual([{ kind: "wait", ms: 250 }]);
    expect(r.state.status).toBe("reconnecting");
    const resumed = stepBrainStream(r.state, { kind: "timer" });
    expect(resumed.effects).toEqual([{ kind: "connect", lastEventId: "1" }]);
  });
  it("repeated drops lengthen the wait", () => {
    const r = runScript(initialBrainStreamState(),
      [{ kind: "closed" }, { kind: "closed" }, { kind: "closed" }]);
    expect(r.effects.map((e) => ("ms" in e ? e.ms : null))).toEqual([250, 500, 1000]);
  });
  it("a successful open resets the wait to the floor", () => {
    const dropped = runScript(initialBrainStreamState(), [{ kind: "closed" }, { kind: "closed" }]);
    const reopened = stepBrainStream(dropped.state, { kind: "opened" });
    const again = stepBrainStream(reopened.state, { kind: "closed" });
    expect(again.effects).toEqual([{ kind: "wait", ms: 250 }]);
  });
  it("a client that holds nothing reconnects with no header", () => {
    const r = runScript(initialBrainStreamState(), [{ kind: "closed" }, { kind: "timer" }]);
    expect(lastOf(r.effects)).toEqual({ kind: "connect", lastEventId: null });
  });
});

describe("a gap in the sequence", () => {
  it("asks for a snapshot exactly once, not once per later frame", () => {
    const r = runScript(openBrainStream(initialBrainStreamState()),
      [frame(0), frame(4), frame(5), frame(6)]);
    expect(r.effects).toEqual([{ kind: "snapshot" }]);
  });
  it("the snapshot heals the hole and resumes from the snapshot position", () => {
    const gapped = runScript(openBrainStream(initialBrainStreamState()), [frame(0), frame(4)]);
    const healed = stepBrainStream(gapped.state, { kind: "snapshot", seq: 9 });
    expect(healed.state.gapDetected).toBe(false);
    expect(healed.effects).toEqual([{ kind: "connect", lastEventId: "9" }]);
    expect(resumeEventId(healed.state)).toBe("9");
  });
  it("a contiguous run never asks for a snapshot", () => {
    const r = runScript(openBrainStream(initialBrainStreamState()), [frame(0), frame(1), frame(2)]);
    expect(r.effects).toEqual([]);
  });
});

describe("the polling fallback", () => {
  it("engages on an unsupported transport and labels itself delayed", () => {
    const step = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    expect(step.state.status).toBe("delayed");
    expect(step.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
  });
  it("keeps polling rather than reconnecting once it has engaged", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const ticked = stepBrainStream(fallen.state, { kind: "timer" });
    expect(ticked.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
  });
  it("never claims live again on frames it polls", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const r = runScript(fallen.state, [frame(0), frame(1)]);
    expect(r.state.status).toBe("delayed");
    expect(r.state.lastSeq).toBe(1);
  });
  it("a poll that drops keeps polling and does not start a backoff", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const dropped = stepBrainStream(fallen.state, { kind: "closed" });
    expect(dropped.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
    expect(dropped.state.attempt).toBe(0);
  });
  it("a gap over the fallback still asks for a snapshot and resumes by polling", () => {
    const fallen = stepBrainStream(initialBrainStreamState(), { kind: "unsupported" });
    const r = runScript(fallen.state, [frame(0), frame(4)]);
    expect(lastOf(r.effects)).toEqual({ kind: "snapshot" });
    const healed = stepBrainStream(r.state, { kind: "snapshot", seq: 4 });
    expect(healed.effects).toEqual([{ kind: "poll", ms: BRAIN_POLL_INTERVAL_MS }]);
  });
});
