import { useRef } from "react";
import type { PointerEvent } from "react";
import { CodeOrbGlyph, FlaskGlyph, PersonGlyph, TaskDoneGlyph, TaskPlannedGlyph } from "../icons/RemedyGlyphs";
import type { SubGlyphKind, TimelinePhase } from "./phaseMapping";
import type { SegmentState, GlyphView } from "./timelineView";
import { fractionOfSeq, seqAtFraction } from "./timelineView";
import type { TimelineScrub } from "./useTimelineScrub";
import styles from "./PhaseTimeline.module.css";

// The bar's six stops in order; phaseMapping.ts's TIMELINE_PHASES is the same
// list, which tests/ui_contracts/test_phase_mapping.py holds equal.
const CANONICAL_PHASES: readonly TimelinePhase[] = [
  "job",
  "planning",
  "build",
  "test",
  "review",
  "finalized",
];

// What begins each phase, on the label's hover (DECISION F024 D1).
const PHASE_HINTS: Record<TimelinePhase, string> = {
  job: "The job's first event",
  planning: "Planning started",
  build: "The first task run started",
  test: "The first test or verification ran",
  review: "The first review verdict arrived",
  finalized: "Every task has passed",
};

// The sub-glyphs' names, as the legend and a screen reader say them.
const GLYPH_NAMES: Record<SubGlyphKind, string> = {
  decision: "Decision",
  failure: "Failure",
  heal: "Heal",
  stop: "Stop",
};

const SEGMENT = 100 / CANONICAL_PHASES.length;

function stateClass(state: SegmentState) {
  if (state === "done") return styles.isDone;
  if (state === "current") return styles.isCurrent;
  return styles.isPending;
}

function chipClass(glyph: SubGlyphKind) {
  if (glyph === "failure") return [styles.eventChip, styles.eventBlocked].join(" ");
  if (glyph === "heal") return [styles.eventChip, styles.eventLlm].join(" ");
  if (glyph === "decision") return [styles.eventChip, styles.eventReview].join(" ");
  return [styles.eventChip, styles.eventStop].join(" ");
}

function GlyphIcon({ glyph }: { glyph: SubGlyphKind }) {
  if (glyph === "failure") return <FlaskGlyph />;
  if (glyph === "heal") return <CodeOrbGlyph />;
  if (glyph === "decision") return <PersonGlyph />;
  return <TaskPlannedGlyph />;
}

function glyphLeft(g: GlyphView): number {
  return (g.segment + g.offset) * SEGMENT;
}

export function PhaseTimeline({ scrub }: { scrub: TimelineScrub }) {
  const railRef = useRef<HTMLDivElement>(null);
  const { view, state, whole } = scrub;
  const live = state.mode === "live";

  // Drag or click on the track sets the position (T5_F024.md Design).
  const scrubFromPointer = (event: PointerEvent<HTMLDivElement>) => {
    const rail = railRef.current;
    if (!rail || state.head < 0) return;
    const rect = rail.getBoundingClientRect();
    if (rect.width <= 0) return;
    scrub.scrubTo(seqAtFraction(whole, (event.clientX - rect.left) / rect.width));
  };

  return (
    <section
      className={styles.timeline}
      aria-label="Project process timeline"
      data-ui="phase-timeline"
      data-mode={state.mode}
    >
      <div className={styles.phaseHeader}>
        {view.segments.map((phase) => (
          <div
            key={`phase-${phase.phase}`}
            className={[styles.phaseItem, stateClass(phase.state)].join(" ")}
            style={{ left: `${(CANONICAL_PHASES.indexOf(phase.phase) + 0.5) * SEGMENT}%` }}
            data-phase={phase.phase}
            data-state={phase.state}
            title={PHASE_HINTS[phase.phase]}
          >
            <span className={styles.phaseLabel}>{phase.label}</span>
          </div>
        ))}
      </div>

      <div
        ref={railRef}
        className={styles.rail}
        onPointerDown={(event) => {
          event.currentTarget.setPointerCapture(event.pointerId);
          scrubFromPointer(event);
        }}
        onPointerMove={(event) => {
          if (event.currentTarget.hasPointerCapture(event.pointerId)) scrubFromPointer(event);
        }}
      >
        <span className={styles.railBase} aria-hidden="true" />
        {view.segments.map((phase, index) => (
          <span
            key={`segment-${phase.phase}`}
            className={styles.phaseSegment}
            style={{ left: `calc(${index * SEGMENT}% + 3px)`, width: `calc(${SEGMENT}% - 6px)` }}
            aria-hidden="true"
          >
            <span className={styles.railFill} style={{ width: `${phase.fill * 100}%` }} />
          </span>
        ))}
        {view.segments.map((phase, index) => (
          <span
            key={`marker-${phase.phase}`}
            className={[styles.phaseMarker, stateClass(phase.state), phase.compact ? styles.isCompact : ""].join(" ")}
            style={{ left: `${(index + 0.5) * SEGMENT}%` }}
            aria-hidden="true"
          >
            {phase.state === "done" && !phase.compact && <TaskDoneGlyph className={styles.markerCheck} />}
          </span>
        ))}
        <div
          role="slider"
          tabIndex={0}
          className={styles.scrubHandle}
          style={{ left: `${fractionOfSeq(whole, state.position) * 100}%` }}
          aria-label="Timeline position"
          aria-valuemin={-1}
          aria-valuemax={Math.max(state.head, -1)}
          aria-valuenow={state.position}
          aria-valuetext={view.readout}
          onKeyDown={(event) => {
            if (scrub.onKey(event.key, event.shiftKey)) event.preventDefault();
          }}
        />
      </div>

      <div className={styles.eventRail} aria-label="Decisions, failures, heals and stops">
        {view.glyphs.map((g) => (
          <button
            type="button"
            key={`glyph-${g.seq}`}
            className={[styles.eventItem, g.reached ? "" : styles.isAhead].join(" ")}
            style={{ left: `${glyphLeft(g)}%` }}
            title={g.line}
            aria-label={`${GLYPH_NAMES[g.glyph]} at event ${g.seq}: ${g.line}`}
            onClick={() => scrub.scrubTo(g.seq)}
          >
            <span className={styles.eventTick} aria-hidden="true" />
            <span className={chipClass(g.glyph)} aria-hidden="true">
              <GlyphIcon glyph={g.glyph} />
            </span>
          </button>
        ))}
      </div>

      <div className={styles.legend} aria-label="Timeline legend">
        {(["decision", "failure", "heal", "stop"] as const).map((glyph) => (
          <span key={`legend-${glyph}`} className={styles.legendItem}>
            <span className={chipClass(glyph)}><GlyphIcon glyph={glyph} /></span>
            <span>{GLYPH_NAMES[glyph]}</span>
          </span>
        ))}
        <span className={styles.readout} aria-live="polite">{scrub.notice ?? view.readout}</span>
        <button
          type="button"
          className={styles.liveToggle}
          aria-pressed={live}
          disabled={live}
          onClick={scrub.goLive}
        >
          LIVE
        </button>
      </div>
    </section>
  );
}
