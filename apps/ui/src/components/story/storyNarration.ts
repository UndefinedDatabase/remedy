// T5_F039.md T002, DECISION F039 D3 — a narration card is one cluster of a
// chapter's key events, each key event one beat carrying the humanize
// catalog's own line, the reviewer's own verdict word when the row is a
// review round, and the ownership ledger's own sentence when exactly one
// event and one entry agree; the card carries the cost so far and the sync a
// scrub position reads. Remedy deliberately invents no narration: every word
// a beat or a card shows is copied from a source that already wrote it.
import { costMetricOf, type BudgetTickFigures } from "../../api/costMetric";
import type { OwnershipEntry, OwnershipView } from "../../api/ownership";
import type { BrainEventRow } from "../graph/brainOntology";
import type { SubGlyph, SubGlyphKind } from "../timeline/phaseMapping";
import type { StoryChapter } from "./storyChapters";

/** hasOwnProperty, never a bare lookup: a key literally named `toString`
 *  would otherwise resolve against Object.prototype. */
function has(table: Readonly<Record<string, unknown>>, key: string): boolean {
  return Object.prototype.hasOwnProperty.call(table, key);
}

/** One line per outcome `REVIEW_OUTCOME_STATE_TABLE` (brainOntology.ts)
 *  knows, in that table's own order — pinned by
 *  `tests/ui_contracts/test_story_narration.py` so a new outcome the
 *  reviewer adds cannot go unheard here. */
export const STORY_VERDICT_LINES: Readonly<Record<string, string>> = {
  pass: "Verdict: pass",
  fail: "Verdict: fail",
  needs_repair: "Verdict: needs repair",
  blocked: "Verdict: blocked",
};

/** A key event's own kind to the ownership ledger's own action word, for the
 *  two kinds an entry ever names an actor for (DECISION F039 D3 clause 5). */
export const STORY_ACTOR_ACTIONS: Readonly<Record<string, string>> = {
  job_stopped: "job_stopped",
  task_decision_answered: "decision_answered",
};

/** One budget-tick reading at the seq it arrived. */
export interface StoryTick {
  seq: number;
  figures: BudgetTickFigures;
}

/** One key event, worded for the story. */
export interface NarrationBeat {
  seq: number;
  glyph: SubGlyphKind;
  taskId: string;
  line: string;
  verdict: string | null;
  actor: string | null;
}

/** One cluster of one chapter, worded. */
export interface NarrationCard {
  chapter: number;
  firstSeq: number;
  lastSeq: number;
  beats: readonly NarrationBeat[];
  cost: string | null;
}

// The one figure `costMetricOf` gives an empty payload, read once so
// `storyCostLine` never carries a second copy of the dash.
const NO_COST_DISPLAY = costMetricOf({}).display;

/** The cost so far at a scrub position: the display `costMetricOf` gives for
 *  the latest tick at or before `seq`, or null for no tick or a tick whose
 *  figure `costMetricOf` cannot show (DECISION F039 D3 clause 6). */
export function storyCostLine(ticks: readonly StoryTick[], seq: number): string | null {
  let latest: StoryTick | null = null;
  for (const tick of ticks) {
    if (tick.seq <= seq && (latest === null || tick.seq > latest.seq)) latest = tick;
  }
  if (latest === null) return null;
  const metric = costMetricOf(latest.figures);
  if (metric.display === NO_COST_DISPLAY) return null;
  return `Cost so far: ${metric.estimated ? "~" : ""}${metric.display}${metric.unit === "tokens" ? " tokens" : ""}`;
}

/** The verdict a beat shows: `STORY_VERDICT_LINES` for the outcome of the
 *  FIRST row holding the beat's seq, only when that row is a
 *  `task_round_completed` whose outcome the table knows; else null. */
function beatVerdict(seq: number, rows: readonly BrainEventRow[]): string | null {
  const source = rows.find((candidate) => candidate.seq === seq);
  if (source === undefined || source.kind !== "task_round_completed") return null;
  return has(STORY_VERDICT_LINES, source.outcome) ? STORY_VERDICT_LINES[source.outcome] : null;
}

/** The actor a beat names: the ownership ledger's own sentence, only when the
 *  view is readable, the event's kind maps to an ownership action, and the
 *  ledger and the view each hold EXACTLY ONE match for it — scoped to the
 *  event's own task for `decision_answered`, because an entry carries no seq
 *  to match by (DECISION F039 D3 clause 5). */
function beatActor(
  event: SubGlyph,
  allEvents: readonly SubGlyph[],
  ownership: OwnershipView | null,
): string | null {
  if (ownership === null || ownership.error !== "") return null;
  if (!has(STORY_ACTOR_ACTIONS, event.kind)) return null;
  const action = STORY_ACTOR_ACTIONS[event.kind];
  const scoped = action === "decision_answered";
  const matchingEvents = allEvents.filter((candidate) =>
    candidate.kind === event.kind && (!scoped || candidate.taskId === event.taskId));
  if (matchingEvents.length !== 1) return null;
  const matchingEntries: OwnershipEntry[] = ownership.entries.filter((entry) =>
    entry.action === action && (!scoped || entry.taskId === event.taskId));
  if (matchingEntries.length !== 1) return null;
  return matchingEntries[0].sentence;
}

function beatOf(
  event: SubGlyph,
  rows: readonly BrainEventRow[],
  allEvents: readonly SubGlyph[],
  ownership: OwnershipView | null,
): NarrationBeat {
  return {
    seq: event.seq,
    glyph: event.glyph,
    taskId: event.taskId,
    line: event.line,
    verdict: beatVerdict(event.seq, rows),
    actor: beatActor(event, allEvents, ownership),
  };
}

/** One narration card per cluster, chapter by chapter and cluster by cluster,
 *  in that order (DECISION F039 D3 clause 3). */
export function buildNarrationCards(
  chapters: readonly StoryChapter[],
  rows: readonly BrainEventRow[],
  ticks: readonly StoryTick[],
  ownership: OwnershipView | null,
): NarrationCard[] {
  const allEvents: SubGlyph[] = [];
  for (const chapter of chapters) {
    for (const cluster of chapter.clusters) {
      for (const event of cluster.events) allEvents.push(event);
    }
  }
  const cards: NarrationCard[] = [];
  chapters.forEach((chapter, chapterIndex) => {
    for (const cluster of chapter.clusters) {
      cards.push({
        chapter: chapterIndex,
        firstSeq: cluster.firstSeq,
        lastSeq: cluster.lastSeq,
        beats: cluster.events.map((event) => beatOf(event, rows, allEvents, ownership)),
        cost: storyCostLine(ticks, cluster.lastSeq),
      });
    }
  });
  return cards;
}

/** The index of the chapter whose `[startSeq, endSeq)` holds `position`, or
 *  -1 for a position no chapter reaches (DECISION F039 D3 clause 7). */
export function chapterAt(chapters: readonly StoryChapter[], position: number): number {
  return chapters.findIndex((chapter) => chapter.startSeq <= position && position < chapter.endSeq);
}

/** The LAST card of `chapterAt`'s chapter whose `firstSeq` the position has
 *  reached, or null before the chapter's first key event or outside every
 *  chapter (DECISION F039 D3 clause 7). */
export function cardAt(
  chapters: readonly StoryChapter[],
  cards: readonly NarrationCard[],
  position: number,
): NarrationCard | null {
  const chapter = chapterAt(chapters, position);
  if (chapter === -1) return null;
  let found: NarrationCard | null = null;
  for (const card of cards) {
    if (card.chapter === chapter && card.firstSeq <= position) found = card;
  }
  return found;
}
