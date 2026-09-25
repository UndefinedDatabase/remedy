// The live end-to-end of the scrubber (T5_F024.md T003, DECISION F024 D5): a REAL
// fake-provider job's ledger, paged the way the UI pages it, run through the same
// modules the bar and the stage use. `tests/ui_server/test_timeline_scrub_live.py`
// plans and runs the job, pages its frames and hands them in through a scratch
// vitest config's `define`; in the ordinary unit run nothing is handed in and this
// file skips, because there is no job to scrub.
import { describe, expect, it } from "vitest";
import type { BrainStreamFrame } from "../../api/brainStream";
import { feedRowOf } from "../../api/feedRow";
import type { BrainTaskSeed } from "../graph/brainOntology";
import { rebuildBrainModel } from "../graph/brainReducer";
import { extractSubGlyphs, readPhases, timelineSeedOf } from "./phaseMapping";
import { createScrubMemo } from "./scrubSnapshots";
import { initialScrubState, scrubKeyEvent, scrubReduce } from "./scrubState";
import { buildTimelineIndex, indexHead, phasesAt, phaseStops } from "./timelineIndex";
import { buildTimelineView, fractionOfSeq, seqAtFraction } from "./timelineView";

declare const __REMEDY_SCRUB_LIVE__: string | undefined;

interface LivePayload {
  jobId: string;
  tasks: BrainTaskSeed[];
  frames: Record<string, unknown>[];
}

const payload: LivePayload | null =
  typeof __REMEDY_SCRUB_LIVE__ === "string" ? (JSON.parse(__REMEDY_SCRUB_LIVE__) as LivePayload) : null;

// `skipIf` still COLLECTS the block, so its body must not fail on an empty payload.
describe.skipIf(payload === null)("a live fake job, scrubbed", () => {
  const { jobId, tasks, frames } = payload ?? { jobId: "", tasks: [], frames: [] };
  const rows = frames.map((envelope) => feedRowOf({ seq: envelope.seq, event: envelope } as BrainStreamFrame, 0));
  const index = buildTimelineIndex(jobId, tasks, rows);
  const head = indexHead(index) ?? -1;

  it("holds a ledger that runs from seq 0 without a hole", () => {
    expect(rows.length).toBeGreaterThan(0);
    expect(rows.map((r) => r.seq)).toEqual(rows.map((_, i) => i));
  });

  it("draws, at every position, exactly the reducer state of that prefix", () => {
    const memo = createScrubMemo(jobId, tasks, { every: 3, cap: 2 });
    memo.append(rows);
    for (let s = -1; s <= head; s += 1) {
      expect(memo.stateAt(s)).toEqual(rebuildBrainModel(jobId, timelineSeedOf(tasks), rows.filter((r) => r.seq <= s)));
    }
  });

  it("reads every prefix's phases as the plain fold does, and ends Finalized", () => {
    for (let s = -1; s <= head; s += 1) {
      expect(phasesAt(index, s)).toEqual(readPhases(jobId, tasks, rows.filter((r) => r.seq <= s)));
    }
    const whole = phasesAt(index, head);
    expect(whole.current).toBe("finalized");
    expect(whole.spans.find((span) => span.phase === "build")?.startSeq).toBe(0);
  });

  it("puts every sub-glyph on the track and every position on it and back", () => {
    const whole = phasesAt(index, head);
    const glyphs = extractSubGlyphs(rows);
    const view = buildTimelineView({ whole, at: whole, glyphs, position: head, elapsed: null });
    expect(view.glyphs.length).toBe(glyphs.length);
    for (let s = -1; s <= head; s += 1) expect(seqAtFraction(whole, fractionOfSeq(whole, s))).toBe(s);
  });

  it("walks back to before the first event by keyboard and returns to LIVE with End", () => {
    const stops = phaseStops(index);
    let state = initialScrubState(head);
    for (let i = 0; i <= head; i += 1) state = scrubReduce(state, scrubKeyEvent("ArrowLeft", false, stops)!);
    expect(state).toEqual({ mode: "scrubbed", position: -1, head, queued: 0 });
    state = scrubReduce(state, scrubKeyEvent("End", false, stops)!);
    expect(state).toEqual(initialScrubState(head));
  });
});
