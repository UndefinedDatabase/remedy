// T5_F039.md T002, DECISION F039 D5 — a job's whole story, assembled once
// from the ledger rows, the task seeds, the ownership view and the browser's
// own pacing payload. This module decides nothing new about a row: it reads
// the ticks a budget event carries, then composes buildStoryChapters,
// buildNarrationCards, orderedLedger and storyPacingOf, the same four
// functions the chapters, the cards, the seqs and the pacing already own.
import type { BudgetTickFigures } from "../../api/costMetric";
import type { OwnershipView } from "../../api/ownership";
import type { BrainEventRow, BrainTaskSeed } from "../graph/brainOntology";
import { orderedLedger } from "../timeline/phaseMapping";
import { storyPacingOf, type StoryPacing } from "./storyAutoplay";
import { buildStoryChapters, type StoryChapter } from "./storyChapters";
import { buildNarrationCards, type NarrationCard, type StoryTick } from "./storyNarration";

/** A job's whole story: its chapters, the narration cards worded from them,
 *  the seqs autoplay steps over, and the decoded pacing (DECISION F039 D5). */
export interface StoryView {
  chapters: readonly StoryChapter[];
  cards: readonly NarrationCard[];
  seqs: readonly number[];
  pacing: StoryPacing;
}

/** `BrainEventRow` names no `budget` field of its own: `FeedRow`
 *  (apps/ui/src/api/feedRow.ts) carries it OPTIONALLY and is structurally
 *  assignable to the ontology's own input shape, the same way its header
 *  already describes. Read here the way `budgetTick.ts` reads an untrusted
 *  envelope: checked, never asserted. */
function budgetFieldOf(row: BrainEventRow): unknown {
  return (row as unknown as Record<string, unknown>)["budget"];
}

/** One tick per row of `orderedLedger(rows)` whose `budget` is a plain
 *  object — not null, not an array — in that order (DECISION F039 D5). */
export function storyTicksOf(rows: readonly BrainEventRow[]): StoryTick[] {
  const ticks: StoryTick[] = [];
  for (const row of orderedLedger(rows)) {
    const budget = budgetFieldOf(row);
    if (typeof budget === "object" && budget !== null && !Array.isArray(budget)) {
      ticks.push({ seq: row.seq, figures: budget as BudgetTickFigures });
    }
  }
  return ticks;
}

/** A job's whole story, assembled once from its ledger, its task seeds, its
 *  ownership view and the browser's own pacing payload (DECISION F039 D5). */
export function buildStoryView(
  jobId: string,
  tasks: readonly BrainTaskSeed[],
  rows: readonly BrainEventRow[],
  ownership: OwnershipView | null,
  pacing: unknown,
): StoryView {
  const chapters = buildStoryChapters(jobId, tasks, rows);
  return {
    chapters,
    cards: buildNarrationCards(chapters, rows, storyTicksOf(rows), ownership),
    seqs: orderedLedger(rows).map((row) => row.seq),
    pacing: storyPacingOf(pacing),
  };
}
