// What the phase bar shows, computed rather than drawn (T5_F024.md T003,
// DECISION F024 D3): six equal segments, one per phase as the binding
// `.phase{flex:1}` lays them out; each segment's seq range read from the WHOLE
// ledger, so the ruler holds still while the handle moves; each segment's state
// read from the prefix at the handle, so what the bar says at a position is what
// that prefix says; sub-glyphs placed at their seq inside their segment; and the
// position readout. No React, no DOM, no clock.
import { TIMELINE_PHASES } from "./phaseMapping";
import type { PhaseReading, SubGlyph, SubGlyphKind, TimelinePhase } from "./phaseMapping";

export const PHASE_LABELS: Readonly<Record<TimelinePhase, string>> = {
  job: "Job",
  planning: "Planning",
  build: "Build",
  test: "Test",
  review: "Review",
  finalized: "Finalized",
};

export type SegmentState = "done" | "current" | "future";

/** One phase's segment. `compact` marks a phase the whole ledger passed through
 *  with a zero span, drawn as a tick; `fill` is how much of the segment lies at
 *  or before the handle, from 0 to 1. */
export interface SegmentView {
  phase: TimelinePhase;
  label: string;
  state: SegmentState;
  compact: boolean;
  fill: number;
}

/** One sub-glyph on the track: its segment, its offset inside it from 0 to 1,
 *  and whether the handle has reached it. */
export interface GlyphView {
  seq: number;
  glyph: SubGlyphKind;
  line: string;
  segment: number;
  offset: number;
  reached: boolean;
}

export interface TimelineView {
  segments: SegmentView[];
  glyphs: GlyphView[];
  readout: string;
}

// The seq range [from, to) each phase covers in the whole ledger, or null for a
// phase it never reached. The phase the ledger ends in runs to one past its head.
function rangesOf(whole: PhaseReading): ([number, number] | null)[] {
  return TIMELINE_PHASES.map((phase) => {
    const span = whole.spans.find((s) => s.phase === phase);
    if (!span) return null;
    const end = span.endSeq ?? (whole.lastSeq as number) + 1;
    return [span.startSeq, end];
  });
}

/** The bar at `position` over a ledger whose whole reading is `whole` and whose
 *  prefix reading at the handle is `at`. */
export function buildTimelineView(args: {
  whole: PhaseReading;
  at: PhaseReading;
  glyphs: readonly SubGlyph[];
  position: number;
  elapsed: string | null;
}): TimelineView {
  const { whole, at, position } = args;
  const ranges = rangesOf(whole);
  const current = at.lastSeq === null ? -1 : TIMELINE_PHASES.indexOf(at.current);

  const segments = TIMELINE_PHASES.map((phase, p): SegmentView => {
    const range = ranges[p];
    const compact = range !== null && range[0] === range[1];
    const state: SegmentState = current < 0 || p > current ? "future" : p < current ? "done" : "current";
    let fill = state === "done" ? 1 : 0;
    if (state === "current") {
      fill = range === null || compact ? 1 : Math.max(0, Math.min(1, (position + 1 - range[0]) / (range[1] - range[0])));
    }
    return { phase, label: PHASE_LABELS[phase], state, compact, fill };
  });

  const glyphs: GlyphView[] = [];
  for (const g of args.glyphs) {
    const p = ranges.findIndex((r) => r !== null && r[0] < r[1] && g.seq >= r[0] && g.seq < r[1]);
    if (p < 0) continue;
    const [from, to] = ranges[p] as [number, number];
    glyphs.push({
      seq: g.seq,
      glyph: g.glyph,
      line: g.line,
      segment: p,
      offset: (g.seq - from) / (to - from),
      reached: g.seq <= position,
    });
  }

  const head = whole.lastSeq;
  let readout = "No events yet";
  if (head !== null) {
    readout = position < 0 ? "Before the first event" : `Event ${position} of ${head}`;
    if (position >= 0 && args.elapsed !== null) readout += ` · ${args.elapsed}`;
  }
  return { segments, glyphs, readout };
}

// An ISO timestamp as milliseconds, or null. Parsing a value the ledger carries
// is not reading a clock: the same string always gives the same number.
function parseStamp(stamp: string): number | null {
  if (stamp === "") return null;
  const ms = Date.parse(stamp);
  return Number.isFinite(ms) ? ms : null;
}

/** The time between two ledger timestamps as the readout shows it — "+12s",
 *  "+3m 05s", "+1h 02m" — or null when either is missing or unreadable. */
export function elapsedLabel(firstStamp: string, stamp: string): string | null {
  const start = parseStamp(firstStamp);
  const at = parseStamp(stamp);
  if (start === null || at === null || at < start) return null;
  const seconds = Math.floor((at - start) / 1000);
  const pad = (n: number) => String(n).padStart(2, "0");
  if (seconds < 60) return `+${seconds}s`;
  if (seconds < 3600) return `+${Math.floor(seconds / 60)}m ${pad(seconds % 60)}s`;
  return `+${Math.floor(seconds / 3600)}h ${pad(Math.floor(seconds / 60) % 60)}m`;
}
