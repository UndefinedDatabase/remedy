// The scrubber machine, its keyboard and LIVE's catch-up (DECISION F024 D3).
// Every expected state is a literal derived by hand from the rules in
// scrubState.ts.
import { describe, expect, it } from "vitest";
import {
  CATCH_UP_MAX_STEPS,
  CATCH_UP_STEP_MS,
  catchUpPlan,
  initialScrubState,
  SCRUB_QUEUE_CAP,
  scrubKeyEvent,
  scrubOverflowed,
  scrubReduce,
} from "./scrubState";
import type { ScrubState } from "./scrubState";

const STOPS = [0, 1, 7];

describe("live mode", () => {
  it("starts live at the head and follows it", () => {
    const live = initialScrubState(10);
    expect(live).toEqual({ mode: "live", position: 10, head: 10, queued: 0 });
    expect(scrubReduce(live, { type: "ingest", head: 14 })).toEqual({ mode: "live", position: 14, head: 14, queued: 0 });
  });

  it("hands back the same object for a head it already has, a step past the head and LIVE", () => {
    const live = initialScrubState(10);
    expect(scrubReduce(live, { type: "ingest", head: 10 })).toBe(live);
    expect(scrubReduce(live, { type: "ingest", head: 3 })).toBe(live);
    expect(scrubReduce(live, { type: "step", delta: 1 })).toBe(live);
    expect(scrubReduce(live, { type: "step_phase", delta: 1, stops: STOPS })).toBe(live);
    expect(scrubReduce(live, { type: "go_live" })).toBe(live);
  });

  it("ignores every move while the ledger is empty", () => {
    const empty = initialScrubState(-1);
    expect(scrubReduce(empty, { type: "scrub_to", seq: 3 })).toBe(empty);
    expect(scrubReduce(empty, { type: "step", delta: -1 })).toBe(empty);
    expect(scrubReduce(empty, { type: "step_phase", delta: -1, stops: [] })).toBe(empty);
  });
});

describe("scrubbed mode", () => {
  it("scrubs to a seq clamped between before-the-first-event and the head", () => {
    const live = initialScrubState(7);
    expect(scrubReduce(live, { type: "scrub_to", seq: 3 })).toEqual({ mode: "scrubbed", position: 3, head: 7, queued: 0 });
    expect(scrubReduce(live, { type: "scrub_to", seq: 99 })).toEqual({ mode: "scrubbed", position: 7, head: 7, queued: 0 });
    expect(scrubReduce(live, { type: "scrub_to", seq: -9 })).toEqual({ mode: "scrubbed", position: -1, head: 7, queued: 0 });
  });

  it("steps one event either way and stops at both ends", () => {
    const back = scrubReduce(initialScrubState(7), { type: "step", delta: -1 });
    expect(back).toEqual({ mode: "scrubbed", position: 6, head: 7, queued: 0 });
    const atHead = scrubReduce(back, { type: "step", delta: 1 });
    expect(atHead).toEqual({ mode: "scrubbed", position: 7, head: 7, queued: 0 });
    expect(scrubReduce(atHead, { type: "step", delta: 1 })).toBe(atHead);
    const first: ScrubState = { mode: "scrubbed", position: -1, head: 7, queued: 0 };
    expect(scrubReduce(first, { type: "step", delta: -1 })).toBe(first);
  });

  it("steps between phase stops, then before the first event, then to the head", () => {
    let s = initialScrubState(7);
    const seen: number[] = [];
    for (let i = 0; i < 4; i += 1) {
      s = scrubReduce(s, { type: "step_phase", delta: -1, stops: STOPS });
      seen.push(s.position);
    }
    expect(seen).toEqual([1, 0, -1, -1]);
    for (let i = 0; i < 4; i += 1) {
      s = scrubReduce(s, { type: "step_phase", delta: 1, stops: STOPS });
      seen.push(s.position);
    }
    expect(seen).toEqual([1, 0, -1, -1, 0, 1, 7, 7]);
    expect(s.mode).toBe("scrubbed");
  });

  it("queues what arrives behind the view and keeps the position", () => {
    const scrubbed = scrubReduce(initialScrubState(7), { type: "scrub_to", seq: 2 });
    const grown = scrubReduce(scrubReduce(scrubbed, { type: "ingest", head: 12 }), { type: "ingest", head: 15 });
    expect(grown).toEqual({ mode: "scrubbed", position: 2, head: 15, queued: 8 });
    expect(scrubReduce(grown, { type: "go_live" })).toEqual({ mode: "live", position: 15, head: 15, queued: 0 });
  });

  it("overflows only past the queue cap", () => {
    const at = (queued: number): ScrubState => ({ mode: "scrubbed", position: 0, head: queued, queued });
    expect(SCRUB_QUEUE_CAP).toBe(5000);
    expect(scrubOverflowed(at(5000))).toBe(false);
    expect(scrubOverflowed(at(5001))).toBe(true);
  });
});

describe("the keyboard", () => {
  it("maps arrows to events, shifted arrows to phases, Home and End to the two ends", () => {
    expect(scrubKeyEvent("ArrowLeft", false, STOPS)).toEqual({ type: "step", delta: -1 });
    expect(scrubKeyEvent("ArrowRight", false, STOPS)).toEqual({ type: "step", delta: 1 });
    expect(scrubKeyEvent("ArrowLeft", true, STOPS)).toEqual({ type: "step_phase", delta: -1, stops: STOPS });
    expect(scrubKeyEvent("ArrowRight", true, STOPS)).toEqual({ type: "step_phase", delta: 1, stops: STOPS });
    expect(scrubKeyEvent("Home", false, STOPS)).toEqual({ type: "scrub_to", seq: -1 });
    expect(scrubKeyEvent("End", false, STOPS)).toEqual({ type: "go_live" });
    expect(scrubKeyEvent("ArrowUp", false, STOPS)).toBeNull();
    expect(scrubKeyEvent("a", true, STOPS)).toBeNull();
  });
});

describe("LIVE's catch-up", () => {
  it("replays a short gap one event per frame", () => {
    expect(catchUpPlan(10, 13, false)).toEqual([
      { atMs: 120, seq: 11 },
      { atMs: 240, seq: 12 },
      { atMs: 360, seq: 13 },
    ]);
  });

  it("fast-forwards a long gap in at most eight frames ending exactly at the head", () => {
    expect(CATCH_UP_STEP_MS).toBe(120);
    expect(CATCH_UP_MAX_STEPS).toBe(8);
    expect(catchUpPlan(0, 100, false)).toEqual([
      { atMs: 120, seq: 13 },
      { atMs: 240, seq: 25 },
      { atMs: 360, seq: 38 },
      { atMs: 480, seq: 50 },
      { atMs: 600, seq: 63 },
      { atMs: 720, seq: 75 },
      { atMs: 840, seq: 88 },
      { atMs: 960, seq: 100 },
    ]);
  });

  it("jumps under reduced motion and plans nothing when already there", () => {
    expect(catchUpPlan(0, 100, true)).toEqual([{ atMs: 0, seq: 100 }]);
    expect(catchUpPlan(5, 5, false)).toEqual([]);
    expect(catchUpPlan(-1, 0, false)).toEqual([{ atMs: 120, seq: 0 }]);
  });
});
