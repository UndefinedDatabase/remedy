// T5_F039.md T001, DECISION F039 D1 — a story's chapters are the phase bar's own
// reading of a job's event ledger, each phase's key events clustered by how
// closely they land together and a dense phase split into parts by the limit
// below. Remedy deliberately writes no chapter prose of its own beyond the
// title table: every sentence a chapter shows is either that table's title or
// a key event's own humanize-catalog line.
import type { BrainEventRow, BrainTaskSeed } from "../graph/brainOntology";
import {
  extractSubGlyphs,
  readPhases,
  TIMELINE_PHASES,
} from "../timeline/phaseMapping";
import type { SubGlyph, TimelinePhase } from "../timeline/phaseMapping";

// The most key events one chapter holds before it splits into parts.
export const STORY_CHAPTER_KEY_EVENT_LIMIT = 6;
// The largest seq gap between two consecutive key events that still keeps
// them in the same cluster; a wider gap starts a new one.
export const STORY_CLUSTER_SEQ_GAP = 2;

// One title per phase, in TIMELINE_PHASES order. A title names the phase and
// never its outcome: The finish is reached only where every task passed, so a
// failing run is never titled as a good one.
export const STORY_CHAPTER_TITLES: Readonly<Record<TimelinePhase, string>> = {
  job: "The start",
  planning: "The plan",
  build: "The build",
  test: "The tests",
  review: "The review",
  finalized: "The finish",
};

/** A run of a chapter's key events close enough together, in seq order, to
 *  read as one beat of the story: no two consecutive events in it are more
 *  than STORY_CLUSTER_SEQ_GAP seqs apart. */
export interface StoryCluster {
  firstSeq: number;
  lastSeq: number;
  events: readonly SubGlyph[];
}

/** One chapter, or one part of a chapter split by STORY_CHAPTER_KEY_EVENT_LIMIT.
 *  `endSeq` is exclusive: the chapter covers `[startSeq, endSeq)`. */
export interface StoryChapter {
  phase: TimelinePhase;
  part: number;
  parts: number;
  title: string;
  startSeq: number;
  endSeq: number;
  clusters: readonly StoryCluster[];
}

/** The title a chapter's part shows: the table's title alone when the phase
 *  has only one part, else the title with its part count. */
export function storyChapterTitle(phase: TimelinePhase, part: number, parts: number): string {
  const title = STORY_CHAPTER_TITLES[phase];
  return parts === 1 ? title : `${title}, part ${part} of ${parts}`;
}

/** Groups key events, already in seq order, into clusters: a new cluster
 *  starts wherever an event's seq exceeds the previous event's seq by more
 *  than STORY_CLUSTER_SEQ_GAP. `[]` for no event. */
export function clusterKeyEvents(events: readonly SubGlyph[]): StoryCluster[] {
  const clusters: StoryCluster[] = [];
  let current: SubGlyph[] = [];
  for (const event of events) {
    const previous = current[current.length - 1];
    if (previous !== undefined && event.seq - previous.seq > STORY_CLUSTER_SEQ_GAP) {
      clusters.push({ firstSeq: current[0].seq, lastSeq: previous.seq, events: current });
      current = [];
    }
    current.push(event);
  }
  if (current.length > 0) {
    clusters.push({ firstSeq: current[0].seq, lastSeq: current[current.length - 1].seq, events: current });
  }
  return clusters;
}

/** The story's chapters: the phase bar's own reading of the WHOLE ledger,
 *  each phase in TIMELINE_PHASES order that has a span becoming one chapter
 *  (split into parts when it holds more than STORY_CHAPTER_KEY_EVENT_LIMIT key
 *  events), in phase order and part order. `[]` for an empty ledger. */
export function buildStoryChapters(
  jobId: string,
  tasks: readonly BrainTaskSeed[],
  rows: readonly BrainEventRow[],
): StoryChapter[] {
  const reading = readPhases(jobId, tasks, rows);
  if (reading.lastSeq === null) return [];
  const lastSeq = reading.lastSeq;
  const keyEvents = extractSubGlyphs(rows);
  const spanByPhase = new Map(reading.spans.map((span) => [span.phase, span] as const));
  const chapters: StoryChapter[] = [];

  for (const phase of TIMELINE_PHASES) {
    const span = spanByPhase.get(phase);
    if (span === undefined) continue;
    const start = span.startSeq;
    const end = span.endSeq === null ? lastSeq + 1 : span.endSeq;
    if (start >= end) continue;
    const phaseEvents = keyEvents.filter((event) => event.seq >= start && event.seq < end);
    const parts = Math.max(1, Math.ceil(phaseEvents.length / STORY_CHAPTER_KEY_EVENT_LIMIT));

    for (let part = 1; part <= parts; part += 1) {
      const partStartIndex = (part - 1) * STORY_CHAPTER_KEY_EVENT_LIMIT;
      const partEvents = phaseEvents.slice(partStartIndex, partStartIndex + STORY_CHAPTER_KEY_EVENT_LIMIT);
      const startSeq = part === 1 ? start : partEvents[0].seq;
      const endSeq = part === parts ? end : phaseEvents[partStartIndex + STORY_CHAPTER_KEY_EVENT_LIMIT].seq;
      chapters.push({
        phase,
        part,
        parts,
        title: storyChapterTitle(phase, part, parts),
        startSeq,
        endSeq,
        clusters: clusterKeyEvents(partEvents),
      });
    }
  }

  return chapters;
}
