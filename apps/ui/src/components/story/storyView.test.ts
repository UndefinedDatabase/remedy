// Goldens for the story's whole view (T5_F039.md T002, DECISION F039 D5). Every
// expected reading below is a literal, HAND-DERIVED from the rules in
// storyView.ts, storyChapters.ts, storyNarration.ts and storyAutoplay.ts —
// never computed by the code under test.
import { describe, expect, it } from "vitest";
import { feedRowOf } from "../../api/feedRow";
import type { BrainStreamFrame } from "../../api/brainStream";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import { row } from "../graph/brainReducer.fixtures";
import type { BrainEventRow, BrainTaskSeed } from "../graph/brainOntology";
import type { NarrationCard } from "./storyNarration";
import { buildStoryView, storyTicksOf } from "./storyView";

const DEMO_TASKS: readonly BrainTaskSeed[] = [
  { id: "fe1b5b487fda490f", status: "pending", rank: 0 },
  { id: "4b3ddac9dba846af", status: "pending", rank: 1 },
];

const REVIEW_LINE = "A review round of a task finished.";

// The review's two clusters, each a needs_repair beat and a pass beat, no
// ownership view and so no actor — the same literal storyNarration.test.ts
// hand-derives for buildNarrationCards on this recording.
const DEMO_CARDS_NO_COST: readonly NarrationCard[] = [
  {
    chapter: 1,
    firstSeq: 1,
    lastSeq: 3,
    beats: [
      { seq: 1, glyph: "failure", taskId: "fe1b5b487fda490f", line: REVIEW_LINE, verdict: "Verdict: needs repair", actor: null },
      { seq: 3, glyph: "heal", taskId: "fe1b5b487fda490f", line: REVIEW_LINE, verdict: "Verdict: pass", actor: null },
    ],
    cost: null,
  },
  {
    chapter: 1,
    firstSeq: 6,
    lastSeq: 8,
    beats: [
      { seq: 6, glyph: "failure", taskId: "4b3ddac9dba846af", line: REVIEW_LINE, verdict: "Verdict: needs repair", actor: null },
      { seq: 8, glyph: "heal", taskId: "4b3ddac9dba846af", line: REVIEW_LINE, verdict: "Verdict: pass", actor: null },
    ],
    cost: null,
  },
];

/** A row hand-made to carry a `budget` value `storyTicksOf` must reject on its
 *  own, bypassing `feedRowOf`'s own filtering entirely — the defence a row
 *  arriving some other way still needs. */
function rowWithRawBudget(seq: number, budget: unknown): BrainEventRow {
  const built: Record<string, unknown> = {
    seq, kind: "budget.tick", outcome: "", taskId: "", attemptId: "", planTaskIds: [], budget,
  };
  return built as unknown as BrainEventRow;
}

function tickFrame(seq: number, budget: unknown): BrainStreamFrame {
  return { seq, event: { seq, event: "budget.tick", budget } };
}

describe("storyTicksOf", () => {
  it("reads ticks from feed rows of budget.tick frames given out of seq order, in orderedLedger's order, skipping another kind and a string budget", () => {
    const rows = [
      feedRowOf(tickFrame(5, { spent_usd: 0.5 }), 0),
      feedRowOf({ seq: 1, event: { seq: 1, event: "task_run_started", budget: { spent_usd: 9 } } }, 0),
      feedRowOf(tickFrame(3, "not an object"), 0),
      feedRowOf(tickFrame(2, { spent_usd: 0.2 }), 0),
    ];
    expect(storyTicksOf(rows)).toEqual([
      { seq: 2, figures: { spent_usd: 0.2 } },
      { seq: 5, figures: { spent_usd: 0.5 } },
    ]);
  });

  it("yields no tick from hand-made rows whose budget is an array or a string", () => {
    const rows = [rowWithRawBudget(1, [1, 2]), rowWithRawBudget(2, "not an object")];
    expect(storyTicksOf(rows)).toEqual([]);
  });
});

describe("buildStoryView on the demo recording", () => {
  it("assembles the chapters' titles, the review's two cost-less cards, the full seq range and the decoded pacing", () => {
    const view = buildStoryView(
      BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows(), null, { step_ms: 300, chapter_pause_ms: 1 },
    );
    expect(view.chapters.map((chapter) => chapter.title)).toEqual(["The build", "The review", "The finish"]);
    expect(view.cards).toEqual(DEMO_CARDS_NO_COST);
    expect(view.seqs).toEqual([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]);
    // step_ms (300) is a whole number in [50, 10000] and is kept;
    // chapter_pause_ms (1) is below the floor and falls back to its default.
    expect(view.pacing).toEqual({ stepMs: 300, chapterPauseMs: 1600 });
  });

  it("gives both review cards the same cost so far when seq 2 becomes a budget tick", () => {
    const rows = brainDemoRows().map((demoRow) =>
      demoRow.seq === 2 ? feedRowOf(tickFrame(2, { spent_usd: 0.1, basis: { cost: "actual" } }), 0) : demoRow);
    const view = buildStoryView(BRAIN_DEMO_JOB_ID, DEMO_TASKS, rows, null, null);
    expect(view.cards.map((card) => card.cost)).toEqual(["Cost so far: $0.10", "Cost so far: $0.10"]);
  });
});

describe("buildStoryView's seqs", () => {
  it("are ascending and distinct even when rows arrive out of order with a repeated seq", () => {
    const rows: readonly BrainEventRow[] = [
      row(5, "task_run_started"),
      row(1, "task_run_started"),
      row(3, "task_run_started"),
      row(1, "task_run_completed"),
    ];
    const view = buildStoryView("job-x", [], rows, null, null);
    expect(view.seqs).toEqual([1, 3, 5]);
  });
});
