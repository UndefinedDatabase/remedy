// T5_F039.md T002, DECISION F039 D6 — the story's own pacing words and its
// golden walkthrough, composed once from the pure rules three sibling
// modules already own: storyAutoplay's `autoplayStep` decides where and
// when the next move lands, storyNarration's `chapterAt` and `cardAt`
// answer where the scrub sits, and storyView's whole `StoryView` carries
// the chapters, cards, seqs and pacing this module reads. Remedy
// deliberately invents no narration here either: every word this module
// prints is a chapter's own title or copied straight from `storyNarration`.
import { autoplayStep } from "./storyAutoplay";
import { cardAt, chapterAt, type NarrationBeat, type NarrationCard } from "./storyNarration";
import type { StoryView } from "./storyView";

/** What the story says while the job is still recording, so a person reading
 *  it mid-run is never told the record is the whole run (DECISION F039 D6 (2)). */
export const STORY_RUNNING_LINE =
  "This job is still running, so its story ends where the record ends now.";

/** The scrub position in words: no chapter at all when the view holds none,
 *  before the first chapter's own start, past every chapter `chapterAt` can
 *  place it in, or the chapter and title `chapterAt` finds there. */
export function storyPositionLabel(view: StoryView, position: number): string {
  if (view.chapters.length === 0) return "No event is recorded yet.";
  if (position < view.chapters[0].startSeq) return "Before the first event";
  const at = chapterAt(view.chapters, position);
  if (at === -1) return "After the last event";
  const chapter = view.chapters[at];
  return `Chapter ${at + 1} of ${view.chapters.length}: ${chapter.title}`;
}

/** Where Play starts: before the first event while the scrub is LIVE, when
 *  the view holds no seq at all, or once `position` has already reached the
 *  ledger's own last seq; otherwise exactly where the scrub already stands,
 *  so resuming mid-story never jumps the reader back. */
export function storyPlayStart(view: StoryView, position: number, live: boolean): number {
  if (live || view.seqs.length === 0) return -1;
  const lastSeq = view.seqs[view.seqs.length - 1];
  if (position >= lastSeq) return -1;
  return position;
}

/** A card's beats the scrub has reached: `[]` for no card, else the beats at
 *  or before `position`, in the card's own order — never the beats a
 *  position has not drawn on the graph yet. */
export function storyBeatsAt(card: NarrationCard | null, position: number): readonly NarrationBeat[] {
  if (card === null) return [];
  return card.beats.filter((beat) => beat.seq <= position);
}

/** One move of the golden walkthrough: the position it lands on, how long it
 *  waited to get there, that position's words, the card reached there (its
 *  first seq, or null), and how many of that card's beats the position has
 *  reached. */
export interface StoryFrame {
  position: number;
  delayMs: number;
  label: string;
  cardFirstSeq: number | null;
  beats: number;
}

/** The whole autoplay walk, from position -1 until `autoplayStep` answers
 *  null: the golden walkthrough every `storyPlayer.test.ts` literal is
 *  hand-derived against. */
export function storyWalk(view: StoryView, reducedMotion: boolean): StoryFrame[] {
  const frames: StoryFrame[] = [];
  let position = -1;
  for (;;) {
    const step = autoplayStep(view.chapters, view.seqs, position, view.pacing, reducedMotion);
    if (step === null) return frames;
    position = step.position;
    const card = cardAt(view.chapters, view.cards, position);
    frames.push({
      position,
      delayMs: step.delayMs,
      label: storyPositionLabel(view, position),
      cardFirstSeq: card === null ? null : card.firstSeq,
      beats: storyBeatsAt(card, position).length,
    });
  }
}
