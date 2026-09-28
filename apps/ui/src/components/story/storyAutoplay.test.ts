// Goldens for the story's autoplay pacing (T5_F039.md T002, DECISION F039 D4).
// Every expected reading below is HAND-DERIVED from the rules in
// storyAutoplay.ts and the demo recording's own chapters, whose spans read
// build [0, 1), review [1, 9) and finalized [9, 10) — never computed by the
// code under test.
import { describe, expect, it } from "vitest";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import type { BrainTaskSeed } from "../graph/brainOntology";
import { buildStoryChapters } from "./storyChapters";
import {
  autoplayStep,
  autoplayTotalMs,
  storyPacingOf,
  STORY_CHAPTER_PAUSE_MS,
  STORY_PACING_DEFAULT,
  STORY_PACING_MAX_MS,
  STORY_PACING_MIN_MS,
  STORY_STEP_MS,
} from "./storyAutoplay";
import type { StoryPacing } from "./storyAutoplay";

const DEMO_TASKS: readonly BrainTaskSeed[] = [
  { id: "fe1b5b487fda490f", status: "pending", rank: 0 },
  { id: "4b3ddac9dba846af", status: "pending", rank: 1 },
];

describe("the four constants and the default pacing", () => {
  it("STORY_STEP_MS is 420", () => {
    expect(STORY_STEP_MS).toBe(420);
  });

  it("STORY_CHAPTER_PAUSE_MS is 1600", () => {
    expect(STORY_CHAPTER_PAUSE_MS).toBe(1600);
  });

  it("STORY_PACING_MIN_MS is 50", () => {
    expect(STORY_PACING_MIN_MS).toBe(50);
  });

  it("STORY_PACING_MAX_MS is 10000", () => {
    expect(STORY_PACING_MAX_MS).toBe(10000);
  });

  it("STORY_PACING_DEFAULT is the step and the chapter pause", () => {
    expect(STORY_PACING_DEFAULT).toEqual({ stepMs: 420, chapterPauseMs: 1600 });
  });
});

describe("storyPacingOf", () => {
  it("reads both fields from a plain object within the clamp", () => {
    expect(storyPacingOf({ step_ms: 200, chapter_pause_ms: 3000 })).toEqual({
      stepMs: 200,
      chapterPauseMs: 3000,
    });
  });

  it("keeps the clamp's own bounds, 50 and 10000", () => {
    expect(storyPacingOf({ step_ms: 50, chapter_pause_ms: 10000 })).toEqual({
      stepMs: 50,
      chapterPauseMs: 10000,
    });
  });

  it("falls back to default just outside the clamp, 49 and 10001", () => {
    expect(storyPacingOf({ step_ms: 49, chapter_pause_ms: 10001 })).toEqual(STORY_PACING_DEFAULT);
  });

  it("falls back to default for a fractional number and a numeric string", () => {
    expect(storyPacingOf({ step_ms: 200.5, chapter_pause_ms: "3000" })).toEqual(STORY_PACING_DEFAULT);
  });

  it.each([null, undefined, [], "x", 5])("falls back to default entirely for %p", (raw) => {
    expect(storyPacingOf(raw)).toEqual(STORY_PACING_DEFAULT);
  });
});

describe("autoplayStep and autoplayTotalMs over the demo recording", () => {
  const chapters = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows());
  const seqs = brainDemoRows().map((demoRow) => demoRow.seq);
  const pacing: StoryPacing = { stepMs: 100, chapterPauseMs: 1000 };

  it("walks from -1 to 9, pausing on every chapter's opening", () => {
    const steps: Array<[number, number]> = [];
    let position = -1;
    for (;;) {
      const step = autoplayStep(chapters, seqs, position, pacing, false);
      if (step === null) break;
      steps.push([step.position, step.delayMs]);
      position = step.position;
    }
    expect(steps).toEqual([
      [0, 1100],
      [1, 1100],
      [2, 100],
      [3, 100],
      [4, 100],
      [5, 100],
      [6, 100],
      [7, 100],
      [8, 100],
      [9, 1100],
    ]);
  });

  it.each([
    [-1, 0],
    [0, 1],
    [4, 9],
  ])("under reduced motion, position %i steps to %i after 1000", (start, expected) => {
    expect(autoplayStep(chapters, seqs, start, pacing, true)).toEqual({
      position: expected,
      delayMs: 1000,
    });
  });

  it("under reduced motion, the ledger's last seq has no next step", () => {
    expect(autoplayStep(chapters, seqs, 9, pacing, true)).toBeNull();
  });

  it("autoplayTotalMs with the default pacing is 9000", () => {
    expect(autoplayTotalMs(chapters, seqs, STORY_PACING_DEFAULT, false)).toBe(9000);
  });

  it("autoplayTotalMs with the default pacing, under reduced motion, is 4800", () => {
    expect(autoplayTotalMs(chapters, seqs, STORY_PACING_DEFAULT, true)).toBe(4800);
  });
});

describe("the demo recording's first four rows: an unfinished review", () => {
  const rows = brainDemoRows().slice(0, 4);
  const chapters = buildStoryChapters(BRAIN_DEMO_JOB_ID, DEMO_TASKS, rows);
  const seqs = rows.map((demoRow) => demoRow.seq);

  it("the walk ends at seq 3, without reduced motion", () => {
    expect(autoplayStep(chapters, seqs, 3, STORY_PACING_DEFAULT, false)).toBeNull();
    expect(autoplayTotalMs(chapters, seqs, STORY_PACING_DEFAULT, false)).toBe(4880);
  });

  it("the walk ends at seq 3, under reduced motion", () => {
    expect(autoplayStep(chapters, seqs, 3, STORY_PACING_DEFAULT, true)).toBeNull();
    expect(autoplayTotalMs(chapters, seqs, STORY_PACING_DEFAULT, true)).toBe(4800);
  });
});

describe("an empty ledger", () => {
  it("has no step and a total of 0", () => {
    expect(autoplayStep([], [], -1, STORY_PACING_DEFAULT, false)).toBeNull();
    expect(autoplayTotalMs([], [], STORY_PACING_DEFAULT, false)).toBe(0);
  });
});
