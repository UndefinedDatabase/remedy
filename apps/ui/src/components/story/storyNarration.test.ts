// Goldens for the story's narration cards (T5_F039.md T002, DECISION F039 D3).
// Every expected reading below is a literal, HAND-DERIVED from the rules in
// storyNarration.ts, storyChapters.ts and phaseMapping.ts — never computed by
// the code under test.
import { describe, expect, it } from "vitest";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import { GOLDEN_B_JOB_ID, GOLDEN_B_ROWS, GOLDEN_B_TASKS, row } from "../graph/brainReducer.fixtures";
import type { BrainTaskSeed } from "../graph/brainOntology";
import type { OwnershipEntry, OwnershipView } from "../../api/ownership";
import { buildStoryChapters } from "./storyChapters";
import {
  buildNarrationCards,
  cardAt,
  chapterAt,
  storyCostLine,
  STORY_ACTOR_ACTIONS,
  STORY_VERDICT_LINES,
} from "./storyNarration";
import type { NarrationCard, StoryTick } from "./storyNarration";

const T1: readonly BrainTaskSeed[] = [{ id: "t1", status: "pending", rank: 0 }];

const T1T2: readonly BrainTaskSeed[] = [
  { id: "t1", status: "pending", rank: 0 },
  { id: "t2", status: "pending", rank: 1 },
];

const DEMO_TASKS: readonly BrainTaskSeed[] = [
  { id: "fe1b5b487fda490f", status: "pending", rank: 0 },
  { id: "4b3ddac9dba846af", status: "pending", rank: 1 },
];

const REVIEW_LINE = "A review round of a task finished.";

function ownerEntry(action: string, taskId: string, sentence: string): OwnershipEntry {
  return {
    recordRef: "r1",
    ts: "2026-09-28T00:00:00Z",
    actor: { kind: "operator", door: "cockpit", recordedAs: "operator", tokenNumber: 1, autoApproved: false },
    action,
    taskId,
    text: "",
    consequence: { kind: "none", taskIds: [], ref: "" },
    sentence,
  };
}

function ownershipView(entries: readonly OwnershipEntry[], error = ""): OwnershipView {
  return { schema: "remedy.ownership.v1", jobId: "job-b", entries: [...entries], error };
}

describe("the two tables", () => {
  it("STORY_VERDICT_LINES names all four outcomes REVIEW_OUTCOME_STATE_TABLE knows", () => {
    expect(STORY_VERDICT_LINES).toEqual({
      pass: "Verdict: pass",
      fail: "Verdict: fail",
      needs_repair: "Verdict: needs repair",
      blocked: "Verdict: blocked",
    });
  });

  it("STORY_ACTOR_ACTIONS joins the two key-event kinds to their ownership actions", () => {
    expect(STORY_ACTOR_ACTIONS).toEqual({
      job_stopped: "job_stopped",
      task_decision_answered: "decision_answered",
    });
  });
});

describe("storyCostLine", () => {
  const ticks: readonly StoryTick[] = [
    { seq: 1, figures: { spent_usd: 0.1, basis: { cost: "actual" } } },
    { seq: 5, figures: { spent_usd: 0.25 } },
    { seq: 7, figures: {} },
    { seq: 8, figures: { spent_tokens: 1500, basis: { tokens: "actual" } } },
  ];

  it.each([
    [0, null],
    [1, "Cost so far: $0.10"],
    [6, "Cost so far: ~$0.25"],
    [7, null],
    [9, "Cost so far: 1.5k tokens"],
  ])("at seq %i reads %s", (seq, expected) => {
    expect(storyCostLine(ticks, seq)).toBe(expected);
  });

  it("is null for no tick at all", () => {
    expect(storyCostLine([], 5)).toBeNull();
  });
});

describe("buildNarrationCards on the demo recording", () => {
  it("chapter 1 (the review) holds two cards, each a needs_repair beat and a pass beat, no actor and no cost", () => {
    const chapters = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows());
    const cards = buildNarrationCards(chapters, brainDemoRows(), [], null);
    expect(cards).toEqual([
      {
        chapter: 1,
        firstSeq: 1,
        lastSeq: 3,
        beats: [
          {
            seq: 1, glyph: "failure", taskId: "fe1b5b487fda490f", line: REVIEW_LINE,
            verdict: "Verdict: needs repair", actor: null,
          },
          {
            seq: 3, glyph: "heal", taskId: "fe1b5b487fda490f", line: REVIEW_LINE,
            verdict: "Verdict: pass", actor: null,
          },
        ],
        cost: null,
      },
      {
        chapter: 1,
        firstSeq: 6,
        lastSeq: 8,
        beats: [
          {
            seq: 6, glyph: "failure", taskId: "4b3ddac9dba846af", line: REVIEW_LINE,
            verdict: "Verdict: needs repair", actor: null,
          },
          {
            seq: 8, glyph: "heal", taskId: "4b3ddac9dba846af", line: REVIEW_LINE,
            verdict: "Verdict: pass", actor: null,
          },
        ],
        cost: null,
      },
    ] satisfies NarrationCard[]);
  });
});

describe("buildNarrationCards on GOLDEN_B_ROWS: a stop mid-run, a heal, then a decision", () => {
  it("names the stop's actor, marks each review round's verdict, and reads the cost at each cluster's last seq", () => {
    const chapters = buildStoryChapters(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, GOLDEN_B_ROWS);
    const ticks: readonly StoryTick[] = [
      { seq: 5, figures: { spent_usd: 0.25 } },
      { seq: 8, figures: { spent_usd: 0.5, basis: { cost: "actual" } } },
    ];
    const ownership = ownershipView([ownerEntry("job_stopped", "", "The operator stopped the job.")]);
    const cards = buildNarrationCards(chapters, GOLDEN_B_ROWS, ticks, ownership);
    expect(cards).toEqual([
      {
        chapter: 1,
        firstSeq: 2,
        lastSeq: 6,
        beats: [
          { seq: 2, glyph: "failure", taskId: "t1", line: REVIEW_LINE, verdict: "Verdict: fail", actor: null },
          { seq: 3, glyph: "failure", taskId: "t1", line: REVIEW_LINE, verdict: "Verdict: needs repair", actor: null },
          {
            seq: 4, glyph: "stop", taskId: "", line: "The job stopped.",
            verdict: null, actor: "The operator stopped the job.",
          },
          { seq: 6, glyph: "heal", taskId: "t1", line: REVIEW_LINE, verdict: "Verdict: pass", actor: null },
        ],
        cost: "Cost so far: ~$0.25",
      },
      {
        chapter: 1,
        firstSeq: 9,
        lastSeq: 9,
        beats: [
          {
            seq: 9, glyph: "decision", taskId: "t2", line: "task_needs_decision event",
            verdict: null, actor: null,
          },
        ],
        cost: "Cost so far: $0.50",
      },
    ] satisfies NarrationCard[]);
  });
});

describe("the stop's actor: only a single readable match names anyone", () => {
  const chapters = buildStoryChapters(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, GOLDEN_B_ROWS);

  function stopActor(ownership: OwnershipView | null): string | null {
    const cards = buildNarrationCards(chapters, GOLDEN_B_ROWS, [], ownership);
    return cards[0].beats[2].actor;
  }

  it("names nobody for a null view", () => {
    expect(stopActor(null)).toBeNull();
  });

  it("names nobody for an unreadable view", () => {
    expect(stopActor(ownershipView([ownerEntry("job_stopped", "", "x")], "server unreachable"))).toBeNull();
  });

  it("names nobody for two job_stopped entries", () => {
    expect(stopActor(ownershipView([
      ownerEntry("job_stopped", "", "a"),
      ownerEntry("job_stopped", "", "b"),
    ]))).toBeNull();
  });

  it("names nobody for only a job_paused entry", () => {
    expect(stopActor(ownershipView([ownerEntry("job_paused", "", "c")]))).toBeNull();
  });
});

describe("a card's cost reads its cluster's own lastSeq, never one past it", () => {
  it("a tick exactly one seq after the cluster's last key event is not the one its cost reads", () => {
    const rows = [
      row(1, "task_run_started", "t1"),
      row(2, "task_round_completed", "t1", "fail"),
    ];
    const chapters = buildStoryChapters("job-cost-edge", T1, rows);
    const ticks: readonly StoryTick[] = [
      { seq: 2, figures: { spent_usd: 1, basis: { cost: "actual" } } },
      { seq: 3, figures: { spent_usd: 2, basis: { cost: "actual" } } },
    ];
    const cards = buildNarrationCards(chapters, rows, ticks, null);
    const card = cards.find((c) => c.lastSeq === 2);
    expect(card?.cost).toBe("Cost so far: $1.00");
  });
});

describe("a decision's actor is scoped to the event's own task", () => {
  const rows = [
    row(1, "task_run_started", "t1"),
    row(2, "task_decision_answered", "t1"),
    row(3, "task_run_started", "t2"),
    row(4, "task_decision_answered", "t2"),
  ];
  const chapters = buildStoryChapters("job-decisions", T1T2, rows);

  it("each task's decision names its own entry's sentence, never the other task's", () => {
    const ownership = ownershipView([
      ownerEntry("decision_answered", "t1", "Someone answered t1's decision."),
      ownerEntry("decision_answered", "t2", "Someone answered t2's decision."),
    ]);
    const beats = buildNarrationCards(chapters, rows, [], ownership).flatMap((card) => card.beats);
    expect(beats.find((b) => b.taskId === "t1")?.actor).toBe("Someone answered t1's decision.");
    expect(beats.find((b) => b.taskId === "t2")?.actor).toBe("Someone answered t2's decision.");
  });

  it("names nobody when only another task's entry exists", () => {
    const ownership = ownershipView([
      ownerEntry("decision_answered", "t2", "Someone answered t2's decision."),
    ]);
    const beats = buildNarrationCards(chapters, rows, [], ownership).flatMap((card) => card.beats);
    expect(beats.find((b) => b.taskId === "t1")?.actor).toBeNull();
  });
});

describe("buildNarrationCards on phaseMapping.test.ts's planned-job case", () => {
  it("both failure beats carry no verdict, though their rows' outcome is fail", () => {
    const rows = [
      row(0, "planning_started"),
      row(1, "planning_completed", "", "changed"),
      row(2, "task_run_started", "t1"),
      row(3, "verification_failed", "t1", "fail"),
      row(4, "task_run_failed", "t1", "fail"),
    ];
    const chapters = buildStoryChapters("job-p", T1, rows);
    const cards = buildNarrationCards(chapters, rows, [], null);
    expect(cards).toHaveLength(1);
    expect(cards[0].beats.map((b) => [b.seq, b.verdict])).toEqual([
      [3, null],
      [4, null],
    ]);
  });
});

describe("chapterAt and cardAt over the demo recording", () => {
  const chapters = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows());
  const cards = buildNarrationCards(chapters, brainDemoRows(), [], null);

  it.each([
    [-1, -1, null],
    [0, 0, null],
    [1, 1, 1],
    [2, 1, 1],
    [5, 1, 1],
    [6, 1, 6],
    [8, 1, 6],
    [9, 2, null],
    [10, -1, null],
  ])("position %i reads chapter %i and a card starting at %s", (position, chapter, firstSeq) => {
    expect(chapterAt(chapters, position)).toBe(chapter);
    const card = cardAt(chapters, cards, position);
    expect(card === null ? null : card.firstSeq).toBe(firstSeq);
  });
});
