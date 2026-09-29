// Goldens for the story's chapters (T5_F039.md T001, DECISION F039 D1). Every
// expected reading below is a literal, HAND-DERIVED from the rules in
// storyChapters.ts and the phase readings `phaseMapping.test.ts` pins, never
// computed by the code under test.
import { describe, expect, it } from "vitest";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import { GOLDEN_B_JOB_ID, GOLDEN_B_ROWS, GOLDEN_B_TASKS, row } from "../graph/brainReducer.fixtures";
import type { BrainTaskSeed } from "../graph/brainOntology";
import type { SubGlyph } from "../timeline/phaseMapping";
import {
  buildStoryChapters,
  clusterKeyEvents,
  storyChapterTitle,
  STORY_CHAPTER_KEY_EVENT_LIMIT,
  STORY_CHAPTER_TITLES,
  STORY_CLUSTER_SEQ_GAP,
} from "./storyChapters";
import type { StoryChapter } from "./storyChapters";

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

function assertTiles(chapters: readonly StoryChapter[], firstSeq: number, lastSeq: number): void {
  expect(chapters.length).toBeGreaterThan(0);
  expect(chapters[0].startSeq).toBe(firstSeq);
  for (let i = 1; i < chapters.length; i += 1) {
    expect(chapters[i].startSeq).toBe(chapters[i - 1].endSeq);
  }
  expect(chapters[chapters.length - 1].endSeq).toBe(lastSeq + 1);
}

describe("the title table and its constants", () => {
  it("bounds a chapter's key events at 6 and a cluster's seq gap at 2", () => {
    expect(STORY_CHAPTER_KEY_EVENT_LIMIT).toBe(6);
    expect(STORY_CLUSTER_SEQ_GAP).toBe(2);
  });

  it("names every phase, never its outcome", () => {
    expect(STORY_CHAPTER_TITLES).toEqual({
      job: "The start",
      planning: "The plan",
      build: "The build",
      test: "The tests",
      review: "The review",
      finalized: "The finish",
    });
  });
});

describe("storyChapterTitle", () => {
  it("is the table's title bare when the phase has one part", () => {
    expect(storyChapterTitle("planning", 1, 1)).toBe("The plan");
  });

  it("carries its part count when the phase split", () => {
    expect(storyChapterTitle("review", 2, 3)).toBe("The review, part 2 of 3");
  });
});

describe("clusterKeyEvents", () => {
  it("is empty for no event", () => {
    expect(clusterKeyEvents([])).toEqual([]);
  });

  it("starts a new cluster only when a gap exceeds STORY_CLUSTER_SEQ_GAP", () => {
    const e1: SubGlyph = { seq: 1, glyph: "failure", kind: "task_run_failed", taskId: "t1", line: "A task failed." };
    const e3: SubGlyph = { seq: 3, glyph: "failure", kind: "task_run_failed", taskId: "t1", line: "A task failed." };
    const e6: SubGlyph = { seq: 6, glyph: "failure", kind: "task_run_failed", taskId: "t1", line: "A task failed." };
    expect(clusterKeyEvents([e1, e3, e6])).toEqual([
      { firstSeq: 1, lastSeq: 3, events: [e1, e3] },
      { firstSeq: 6, lastSeq: 6, events: [e6] },
    ]);
  });
});

describe("buildStoryChapters on the pinned fixtures", () => {
  it("the demo recording: build with no cluster, review split into two clusters, then the finish", () => {
    const e1: SubGlyph = { seq: 1, glyph: "failure", kind: "task_round_completed", taskId: "fe1b5b487fda490f", line: REVIEW_LINE };
    const e3: SubGlyph = { seq: 3, glyph: "heal", kind: "task_round_completed", taskId: "fe1b5b487fda490f", line: REVIEW_LINE };
    const e6: SubGlyph = { seq: 6, glyph: "failure", kind: "task_round_completed", taskId: "4b3ddac9dba846af", line: REVIEW_LINE };
    const e8: SubGlyph = { seq: 8, glyph: "heal", kind: "task_round_completed", taskId: "4b3ddac9dba846af", line: REVIEW_LINE };
    const chapters = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows());
    expect(chapters).toEqual([
      { phase: "build", part: 1, parts: 1, title: "The build", startSeq: 0, endSeq: 1, clusters: [] },
      {
        phase: "review",
        part: 1,
        parts: 1,
        title: "The review",
        startSeq: 1,
        endSeq: 9,
        clusters: [
          { firstSeq: 1, lastSeq: 3, events: [e1, e3] },
          { firstSeq: 6, lastSeq: 8, events: [e6, e8] },
        ],
      },
      { phase: "finalized", part: 1, parts: 1, title: "The finish", startSeq: 9, endSeq: 10, clusters: [] },
    ] satisfies StoryChapter[]);
    assertTiles(chapters, 0, 9);
  });

  it("GOLDEN_B_ROWS: a stopped run that never finishes, build then a review of two clusters", () => {
    const g2: SubGlyph = { seq: 2, glyph: "failure", kind: "task_round_completed", taskId: "t1", line: REVIEW_LINE };
    const g3: SubGlyph = { seq: 3, glyph: "failure", kind: "task_round_completed", taskId: "t1", line: REVIEW_LINE };
    const g4: SubGlyph = { seq: 4, glyph: "stop", kind: "job_stopped", taskId: "", line: "The job stopped." };
    const g6: SubGlyph = { seq: 6, glyph: "heal", kind: "task_round_completed", taskId: "t1", line: REVIEW_LINE };
    const g9: SubGlyph = { seq: 9, glyph: "decision", kind: "task_needs_decision", taskId: "t2", line: "task_needs_decision event" };
    const chapters = buildStoryChapters(GOLDEN_B_JOB_ID, GOLDEN_B_TASKS, GOLDEN_B_ROWS);
    expect(chapters).toEqual([
      { phase: "build", part: 1, parts: 1, title: "The build", startSeq: 1, endSeq: 2, clusters: [] },
      {
        phase: "review",
        part: 1,
        parts: 1,
        title: "The review",
        startSeq: 2,
        endSeq: 10,
        clusters: [
          { firstSeq: 2, lastSeq: 6, events: [g2, g3, g4, g6] },
          { firstSeq: 9, lastSeq: 9, events: [g9] },
        ],
      },
    ] satisfies StoryChapter[]);
    assertTiles(chapters, 1, 9);
  });

  it("phaseMapping.test.ts's planned-job case: The plan, The build and The tests, the last holding one cluster", () => {
    const rows = [
      row(0, "planning_started"),
      row(1, "planning_completed", "", "changed"),
      row(2, "task_run_started", "t1"),
      row(3, "verification_failed", "t1", "fail"),
      row(4, "task_run_failed", "t1", "fail"),
    ];
    const v3: SubGlyph = { seq: 3, glyph: "failure", kind: "verification_failed", taskId: "t1", line: "Verification failed." };
    const f4: SubGlyph = { seq: 4, glyph: "failure", kind: "task_run_failed", taskId: "t1", line: "A task failed." };
    expect(buildStoryChapters("job-p", T1, rows)).toEqual([
      { phase: "planning", part: 1, parts: 1, title: "The plan", startSeq: 0, endSeq: 2, clusters: [] },
      { phase: "build", part: 1, parts: 1, title: "The build", startSeq: 2, endSeq: 3, clusters: [] },
      {
        phase: "test",
        part: 1,
        parts: 1,
        title: "The tests",
        startSeq: 3,
        endSeq: 5,
        clusters: [{ firstSeq: 3, lastSeq: 4, events: [v3, f4] }],
      },
    ] satisfies StoryChapter[]);
  });
});

describe("buildStoryChapters splits a dense phase and leaves a whole one alone", () => {
  it("a review of eight key events (seven needs_repair rounds and a pass) splits into parts of six and two, then finalizes", () => {
    const rows = [
      row(0, "task_run_started", "t1"),
      row(1, "task_round_completed", "t1", "needs_repair"),
      row(2, "task_round_completed", "t1", "needs_repair"),
      row(3, "task_round_completed", "t1", "needs_repair"),
      row(4, "task_round_completed", "t1", "needs_repair"),
      row(5, "task_round_completed", "t1", "needs_repair"),
      row(6, "task_round_completed", "t1", "needs_repair"),
      row(7, "task_round_completed", "t1", "needs_repair"),
      row(8, "task_round_completed", "t1", "pass"),
      row(9, "task_run_completed", "t1", "pass"),
      row(10, "task_run_started", "t2"),
      row(11, "task_run_completed", "t2", "pass"),
    ];
    const chapters = buildStoryChapters("job-split", T1T2, rows);
    expect(chapters.map((c) => [c.phase, c.part, c.parts, c.title, c.startSeq, c.endSeq])).toEqual([
      ["build", 1, 1, "The build", 0, 1],
      ["review", 1, 2, "The review, part 1 of 2", 1, 7],
      ["review", 2, 2, "The review, part 2 of 2", 7, 11],
      ["finalized", 1, 1, "The finish", 11, 12],
    ]);
    const [, reviewPart1, reviewPart2] = chapters;
    expect(reviewPart1.clusters).toEqual([
      { firstSeq: 1, lastSeq: 6, events: reviewPart1.clusters[0].events },
    ]);
    expect(reviewPart1.clusters[0].events.map((e) => e.seq)).toEqual([1, 2, 3, 4, 5, 6]);
    expect(reviewPart2.clusters).toEqual([
      { firstSeq: 7, lastSeq: 8, events: reviewPart2.clusters[0].events },
    ]);
    expect(reviewPart2.clusters[0].events.map((e) => [e.seq, e.glyph])).toEqual([
      [7, "failure"],
      [8, "heal"],
    ]);
  });

  it("a review of exactly six key events stays whole, with no part suffix", () => {
    const rows = [
      row(0, "task_run_started", "t1"),
      row(1, "task_round_completed", "t1", "needs_repair"),
      row(2, "task_round_completed", "t1", "needs_repair"),
      row(3, "task_round_completed", "t1", "needs_repair"),
      row(4, "task_round_completed", "t1", "needs_repair"),
      row(5, "task_round_completed", "t1", "needs_repair"),
      row(6, "task_round_completed", "t1", "pass"),
    ];
    const chapters = buildStoryChapters("job-whole", T1, rows);
    const review = chapters.find((c) => c.phase === "review");
    expect(review).toBeDefined();
    expect(review?.parts).toBe(1);
    expect(review?.title).toBe("The review");
    expect(review?.startSeq).toBe(1);
    expect(review?.endSeq).toBe(7);
    expect(review?.clusters).toHaveLength(1);
    expect(review?.clusters[0].events.map((e) => e.seq)).toEqual([1, 2, 3, 4, 5, 6]);
  });
});

describe("buildStoryChapters at the edges", () => {
  it("rows with no marker are honest: one Job-titled chapter", () => {
    expect(buildStoryChapters("job-s", T1, [row(0, ""), row(1, "")])).toEqual([
      { phase: "job", part: 1, parts: 1, title: "The start", startSeq: 0, endSeq: 2, clusters: [] },
    ] satisfies StoryChapter[]);
  });

  it("an empty ledger has no chapters", () => {
    expect(buildStoryChapters("job-e", T1, [])).toEqual([]);
  });

  it("builds the same chapters twice and leaves the rows array unchanged", () => {
    const rows = brainDemoRows();
    const before = rows.map((r) => ({ ...r }));
    const first = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, rows);
    const second = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, rows);
    expect(second).toEqual(first);
    expect(rows).toEqual(before);
  });
});
