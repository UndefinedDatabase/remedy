// T5_F039.md T002, DECISION F039 D4 — this module owns no timer: it only
// answers which scrub position autoplay moves to next and how long to wait
// before it lands there. Remedy deliberately paces a story by its events and
// its chapters, never by the events' own timestamps: a build that took hours
// and a build that took seconds both play at the same pace, one ledger event
// at a time, with one chapter pause more before every chapter's first event.
import type { StoryChapter } from "./storyChapters";
import { chapterAt } from "./storyNarration";

// The graph births one event before autoplay steps to the next (--remedy-dur-birth).
export const STORY_STEP_MS = 420;
// The time a chapter's title holds before its first event lands (--remedy-dur-pulse).
export const STORY_CHAPTER_PAUSE_MS = 1600;

// The clamp a pacing payload's fields are held to; outside it, the default wins.
export const STORY_PACING_MIN_MS = 50;
export const STORY_PACING_MAX_MS = 10000;

/** How long autoplay waits between two ledger events, and how much longer it
 *  waits before a new chapter's first event (DECISION F039 D4 (2)). */
export interface StoryPacing {
  stepMs: number;
  chapterPauseMs: number;
}

/** The pacing autoplay uses absent a payload: one node birth per step, one
 *  pulse before a chapter's opening. */
export const STORY_PACING_DEFAULT: StoryPacing = {
  stepMs: STORY_STEP_MS,
  chapterPauseMs: STORY_CHAPTER_PAUSE_MS,
};

/** One move autoplay makes: the scrub position it lands on, and the delay
 *  before it gets there. */
export interface AutoplayStep {
  position: number;
  delayMs: number;
}

function isPlainObject(raw: unknown): raw is Record<string, unknown> {
  return typeof raw === "object" && raw !== null && !Array.isArray(raw);
}

function clampedField(raw: Record<string, unknown>, key: string, fallback: number): number {
  const value = raw[key];
  if (
    typeof value === "number" &&
    Number.isInteger(value) &&
    value >= STORY_PACING_MIN_MS &&
    value <= STORY_PACING_MAX_MS
  ) {
    return value;
  }
  return fallback;
}

/** The pacing a payload sets: `step_ms` and `chapter_pause_ms` read from
 *  `raw` when it is a plain object, each kept only when it is a whole number
 *  from `STORY_PACING_MIN_MS` to `STORY_PACING_MAX_MS` inclusive, else its
 *  default (DECISION F039 D4 (5)). Never throws. */
export function storyPacingOf(raw: unknown): StoryPacing {
  if (!isPlainObject(raw)) return STORY_PACING_DEFAULT;
  return {
    stepMs: clampedField(raw, "step_ms", STORY_STEP_MS),
    chapterPauseMs: clampedField(raw, "chapter_pause_ms", STORY_CHAPTER_PAUSE_MS),
  };
}

/** The next scrub position autoplay moves to from `position`, and how long it
 *  waits before landing there. Without reduced motion, the next ledger seq
 *  greater than `position`, after one step plus one chapter pause when that
 *  seq opens a different chapter than `position` sits in. Under reduced
 *  motion, the next chapter's own start, after one chapter pause, or — past
 *  the last chapter — the ledger's own last seq; `null` once there is no seq
 *  left to reach (DECISION F039 D4 (3), (4)). */
export function autoplayStep(
  chapters: readonly StoryChapter[],
  seqs: readonly number[],
  position: number,
  pacing: StoryPacing,
  reducedMotion: boolean,
): AutoplayStep | null {
  const here = chapterAt(chapters, position);

  if (reducedMotion) {
    const nextChapter = chapters.slice(here + 1).find((chapter) => chapter.startSeq > position);
    if (nextChapter !== undefined) {
      return { position: nextChapter.startSeq, delayMs: pacing.chapterPauseMs };
    }
    const lastSeq = seqs[seqs.length - 1];
    if (lastSeq !== undefined && lastSeq > position) {
      return { position: lastSeq, delayMs: pacing.chapterPauseMs };
    }
    return null;
  }

  const next = seqs.find((seq) => seq > position);
  if (next === undefined) return null;
  const entersNewChapter = chapterAt(chapters, next) !== here;
  return {
    position: next,
    delayMs: pacing.stepMs + (entersNewChapter ? pacing.chapterPauseMs : 0),
  };
}

/** The whole autoplay walk's length in milliseconds, from position `-1` until
 *  `autoplayStep` answers null. */
export function autoplayTotalMs(
  chapters: readonly StoryChapter[],
  seqs: readonly number[],
  pacing: StoryPacing,
  reducedMotion: boolean,
): number {
  let total = 0;
  let position = -1;
  for (;;) {
    const step = autoplayStep(chapters, seqs, position, pacing, reducedMotion);
    if (step === null) return total;
    total += step.delayMs;
    position = step.position;
  }
}
