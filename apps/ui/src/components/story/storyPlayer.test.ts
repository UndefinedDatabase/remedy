// Goldens for the story's pacing words and its golden walkthrough (T5_F039.md
// T002, DECISION F039 D6). Every expected reading below is a literal,
// HAND-DERIVED from the rules in storyPlayer.ts, storyAutoplay.ts and
// storyNarration.ts over the demo recording's own view — never computed by
// the code under test.
import { describe, expect, it } from "vitest";
import { brainDemoRows, BRAIN_DEMO_JOB_ID } from "../graph/brainDemoRecording";
import type { BrainTaskSeed } from "../graph/brainOntology";
import {
  STORY_RUNNING_LINE,
  storyPlayStart,
  storyPositionLabel,
  storyWalk,
} from "./storyPlayer";
import { buildStoryView } from "./storyView";

const DEMO_TASKS: readonly BrainTaskSeed[] = [
  { id: "fe1b5b487fda490f", status: "pending", rank: 0 },
  { id: "4b3ddac9dba846af", status: "pending", rank: 1 },
];

const DEMO_VIEW = buildStoryView(BRAIN_DEMO_JOB_ID, DEMO_TASKS, brainDemoRows(), null, null);
const EMPTY_VIEW = buildStoryView("job-empty", [], [], null, null);

describe("storyWalk on the demo recording", () => {
  it("walks the ten positions with the golden waits, labels, cards and beat counts", () => {
    expect(storyWalk(DEMO_VIEW, false)).toEqual([
      { position: 0, delayMs: 2020, label: "Chapter 1 of 3: The build", cardFirstSeq: null, beats: 0 },
      { position: 1, delayMs: 2020, label: "Chapter 2 of 3: The review", cardFirstSeq: 1, beats: 1 },
      { position: 2, delayMs: 420, label: "Chapter 2 of 3: The review", cardFirstSeq: 1, beats: 1 },
      { position: 3, delayMs: 420, label: "Chapter 2 of 3: The review", cardFirstSeq: 1, beats: 2 },
      { position: 4, delayMs: 420, label: "Chapter 2 of 3: The review", cardFirstSeq: 1, beats: 2 },
      { position: 5, delayMs: 420, label: "Chapter 2 of 3: The review", cardFirstSeq: 1, beats: 2 },
      { position: 6, delayMs: 420, label: "Chapter 2 of 3: The review", cardFirstSeq: 6, beats: 1 },
      { position: 7, delayMs: 420, label: "Chapter 2 of 3: The review", cardFirstSeq: 6, beats: 1 },
      { position: 8, delayMs: 420, label: "Chapter 2 of 3: The review", cardFirstSeq: 6, beats: 2 },
      { position: 9, delayMs: 2020, label: "Chapter 3 of 3: The finish", cardFirstSeq: null, beats: 0 },
    ]);
  });

  it("walks three positions under reduced motion, one chapter pause each", () => {
    expect(storyWalk(DEMO_VIEW, true)).toEqual([
      { position: 0, delayMs: 1600, label: "Chapter 1 of 3: The build", cardFirstSeq: null, beats: 0 },
      { position: 1, delayMs: 1600, label: "Chapter 2 of 3: The review", cardFirstSeq: 1, beats: 1 },
      { position: 9, delayMs: 1600, label: "Chapter 3 of 3: The finish", cardFirstSeq: null, beats: 0 },
    ]);
  });

  it("answers no frames at all for an empty ledger", () => {
    expect(storyWalk(EMPTY_VIEW, false)).toEqual([]);
  });
});

describe("storyPositionLabel", () => {
  it.each([
    [-1, "Before the first event"],
    [0, "Chapter 1 of 3: The build"],
    [1, "Chapter 2 of 3: The review"],
    [8, "Chapter 2 of 3: The review"],
    [9, "Chapter 3 of 3: The finish"],
    [10, "After the last event"],
  ])("labels position %i as %s", (position, label) => {
    expect(storyPositionLabel(DEMO_VIEW, position)).toBe(label);
  });

  it("says no event is recorded yet for an empty ledger, at any position", () => {
    expect(storyPositionLabel(EMPTY_VIEW, 0)).toBe("No event is recorded yet.");
  });
});

describe("STORY_RUNNING_LINE", () => {
  it("names the running line verbatim", () => {
    expect(STORY_RUNNING_LINE).toBe(
      "This job is still running, so its story ends where the record ends now.",
    );
  });
});

describe("storyPlayStart", () => {
  it("starts at -1 when the scrub is LIVE, regardless of its position", () => {
    expect(storyPlayStart(DEMO_VIEW, 4, true)).toBe(-1);
  });

  it("starts at -1 once the position has reached the ledger's own last seq", () => {
    expect(storyPlayStart(DEMO_VIEW, 9, false)).toBe(-1);
  });

  it("starts exactly where the scrub already stands, mid-story", () => {
    expect(storyPlayStart(DEMO_VIEW, 4, false)).toBe(4);
  });

  it("starts at -1, unchanged, when the scrub already stands before the first event", () => {
    expect(storyPlayStart(DEMO_VIEW, -1, false)).toBe(-1);
  });

  it("starts at -1 for an empty view even when not live", () => {
    expect(storyPlayStart(EMPTY_VIEW, 0, false)).toBe(-1);
  });
});
