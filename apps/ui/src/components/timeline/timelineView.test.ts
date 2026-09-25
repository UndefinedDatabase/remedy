// The bar's view model (DECISION F024 D3): segment states from the prefix at
// the handle, segment ranges from the whole ledger, sub-glyph placement and the
// readout. Every expected view is a literal derived by hand.
import { describe, expect, it } from "vitest";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import type { BrainTaskSeed } from "../graph/brainOntology";
import { row } from "../graph/brainReducer.fixtures";
import { extractSubGlyphs, readPhases } from "./phaseMapping";
import { buildTimelineView, elapsedLabel, fractionOfSeq, PHASE_LABELS, seqAtFraction } from "./timelineView";

const DEMO_TASKS: readonly BrainTaskSeed[] = [
  { id: "a7a8f67f1b9a4814", status: "pending", rank: 0 },
  { id: "1965fb3f26b64fe7", status: "pending", rank: 1 },
];
const demo = (s: number) => readPhases(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows().filter((r) => r.seq <= s));
const DEMO_GLYPHS = extractSubGlyphs(brainDemoRows());
const REVIEW_LINE = "A review round of a task finished.";

describe("the bar over the demo recording", () => {
  it("at the head: every phase done, Finalized current and full", () => {
    const view = buildTimelineView({ whole: demo(7), at: demo(7), glyphs: DEMO_GLYPHS, position: 7, elapsed: "+1s" });
    expect(view.segments).toEqual([
      { phase: "job", label: "Job", state: "done", compact: true, fill: 1 },
      { phase: "planning", label: "Planning", state: "done", compact: true, fill: 1 },
      { phase: "build", label: "Build", state: "done", compact: false, fill: 1 },
      { phase: "test", label: "Test", state: "done", compact: true, fill: 1 },
      { phase: "review", label: "Review", state: "done", compact: false, fill: 1 },
      { phase: "finalized", label: "Finalized", state: "current", compact: false, fill: 1 },
    ]);
    expect(view.glyphs).toEqual([
      { seq: 1, glyph: "failure", line: REVIEW_LINE, segment: 4, offset: 0, reached: true },
      { seq: 2, glyph: "heal", line: REVIEW_LINE, segment: 4, offset: 1 / 6, reached: true },
      { seq: 5, glyph: "failure", line: REVIEW_LINE, segment: 4, offset: 4 / 6, reached: true },
      { seq: 6, glyph: "heal", line: REVIEW_LINE, segment: 4, offset: 5 / 6, reached: true },
    ]);
    expect(view.readout).toBe("Event 7 of 7 · +1s");
  });

  it("scrubbed to seq 3: Review half filled, Finalized ahead, later glyphs not reached", () => {
    const view = buildTimelineView({ whole: demo(7), at: demo(3), glyphs: DEMO_GLYPHS, position: 3, elapsed: null });
    expect(view.segments.map((s) => [s.state, s.fill])).toEqual([
      ["done", 1],
      ["done", 1],
      ["done", 1],
      ["done", 1],
      ["current", 0.5],
      ["future", 0],
    ]);
    expect(view.glyphs.map((g) => g.reached)).toEqual([true, true, false, false]);
    expect(view.readout).toBe("Event 3 of 7");
  });

  it("a glyph exactly at the handle counts as reached", () => {
    const view = buildTimelineView({ whole: demo(7), at: demo(2), glyphs: DEMO_GLYPHS, position: 2, elapsed: null });
    expect(view.glyphs.map((g) => g.reached)).toEqual([true, true, false, false]);
    expect(view.segments[4]).toEqual({ phase: "review", label: "Review", state: "current", compact: false, fill: 2 / 6 });
  });

  it("before the first event: nothing reached, nothing filled", () => {
    const view = buildTimelineView({ whole: demo(7), at: demo(-1), glyphs: DEMO_GLYPHS, position: -1, elapsed: "+0s" });
    expect(view.segments.every((s) => s.state === "future" && s.fill === 0)).toBe(true);
    expect(view.glyphs.every((g) => !g.reached)).toBe(true);
    expect(view.readout).toBe("Before the first event");
  });
});

describe("edges", () => {
  it("an empty ledger shows six future segments, no glyphs and says so", () => {
    const empty = readPhases("job-e", DEMO_TASKS, []);
    const view = buildTimelineView({ whole: empty, at: empty, glyphs: [], position: -1, elapsed: null });
    expect(view.segments.map((s) => [s.phase, s.state, s.compact, s.fill])).toEqual([
      ["job", "future", false, 0],
      ["planning", "future", false, 0],
      ["build", "future", false, 0],
      ["test", "future", false, 0],
      ["review", "future", false, 0],
      ["finalized", "future", false, 0],
    ]);
    expect(view.glyphs).toEqual([]);
    expect(view.readout).toBe("No events yet");
  });

  it("a Finalized the whole ledger later withdrew is still current where the handle is", () => {
    const t1: BrainTaskSeed[] = [{ id: "t1", status: "pending", rank: 0 }];
    const rows = [
      row(0, "task_run_started", "t1"),
      row(1, "task_round_completed", "t1", "pass"),
      row(2, "task_run_completed", "t1", "pass"),
      row(3, "task_run_started", "t1"),
    ];
    const whole = readPhases("job-w", t1, rows);
    const at = readPhases("job-w", t1, rows.slice(0, 3));
    const view = buildTimelineView({ whole, at, glyphs: [], position: 2, elapsed: null });
    expect(view.segments.map((s) => [s.state, s.fill])).toEqual([
      ["done", 1],
      ["done", 1],
      ["done", 1],
      ["done", 1],
      ["done", 1],
      ["current", 1],
    ]);
    expect(view.segments[4].compact).toBe(false);
  });

  it("names the six phases the way the bar does", () => {
    expect(PHASE_LABELS).toEqual({
      job: "Job", planning: "Planning", build: "Build", test: "Test", review: "Review", finalized: "Finalized",
    });
  });
});

describe("the track's geometry", () => {
  it("puts the handle at the end of its event's slot in its segment", () => {
    const whole = demo(7);
    expect(fractionOfSeq(whole, -1)).toBe(0);
    expect(fractionOfSeq(whole, 0)).toBe(3 / 6);
    expect(fractionOfSeq(whole, 1)).toBe((4 + 1 / 6) / 6);
    expect(fractionOfSeq(whole, 6)).toBe(5 / 6);
    expect(fractionOfSeq(whole, 7)).toBe(1);
    expect(fractionOfSeq(whole, 99)).toBe(1);
  });

  it("reads a point on the track back as the event it closes, every seq round-tripping", () => {
    const whole = demo(7);
    for (let s = -1; s <= 7; s += 1) expect(seqAtFraction(whole, fractionOfSeq(whole, s))).toBe(s);
    expect(seqAtFraction(whole, 0)).toBe(-1);
    expect(seqAtFraction(whole, 0.1)).toBe(0);
    expect(seqAtFraction(whole, 0.6)).toBe(1);
    expect(seqAtFraction(whole, 0.7)).toBe(2);
    expect(seqAtFraction(whole, 0.95)).toBe(7);
    expect(seqAtFraction(whole, 4)).toBe(7);
  });

  it("sends a point in a phase the ledger has not reached to the head", () => {
    const t1: BrainTaskSeed[] = [{ id: "t1", status: "pending", rank: 0 }];
    const whole = readPhases("job-u", t1, [row(0, "task_run_started", "t1"), row(1, "task_run_started", "t1")]);
    expect(seqAtFraction(whole, 0.99)).toBe(1);
    expect(fractionOfSeq(whole, 1)).toBe(3 / 6);
    const empty = readPhases("job-e", t1, []);
    expect(seqAtFraction(empty, 0.5)).toBe(-1);
    expect(fractionOfSeq(empty, 3)).toBe(0);
  });
});

describe("the readout's elapsed time", () => {
  it("measures from the first event's timestamp", () => {
    expect(elapsedLabel("2026-09-24T16:57:02.817154+00:00", "2026-09-24T16:57:03.864860+00:00")).toBe("+1s");
    expect(elapsedLabel("2026-09-24T16:57:02+00:00", "2026-09-24T17:00:07+00:00")).toBe("+3m 05s");
    expect(elapsedLabel("2026-09-24T16:57:02+00:00", "2026-09-24T17:59:30+00:00")).toBe("+1h 02m");
  });

  it("says nothing rather than guess", () => {
    expect(elapsedLabel("", "2026-09-24T16:57:03+00:00")).toBeNull();
    expect(elapsedLabel("2026-09-24T16:57:03+00:00", "not a time")).toBeNull();
    expect(elapsedLabel("2026-09-24T16:57:03+00:00", "2026-09-24T16:57:01+00:00")).toBeNull();
  });
});
