import type {
  RemedyPhase,
  RemedyTimelineEvent,
  RemedyTimelinePhase,
  RemedyState,
} from "../../api/types";
import { PhaseGlyph, TaskDoneGlyph } from "../icons/RemedyGlyphs";
import styles from "./PhaseTimeline.module.css";

const CANONICAL_PHASES: RemedyTimelinePhase[] = [
  "job",
  "planning",
  "build",
  "test",
  "review",
  "finalized",
];

const PHASE_LABELS: Record<RemedyTimelinePhase, string> = {
  job: "Job",
  planning: "Planning",
  build: "Build",
  test: "Test",
  review: "Review",
  finalized: "Finalized",
};

function phasePosition(index: number) {
  return `${(index / (CANONICAL_PHASES.length - 1)) * 100}%`;
}

function stateClass(state: RemedyState) {
  if (state === "done") return styles.isDone;
  if (state === "current") return styles.isCurrent;
  if (state === "blocked") return styles.isBlocked;
  return styles.isPending;
}

function eventClass(event: RemedyTimelineEvent) {
  return [
    styles.eventDot,
    event.kind === "llm_action" ? styles.eventLlm : "",
    event.kind === "test" ? styles.eventTest : "",
    event.kind === "review" ? styles.eventReview : "",
    event.state === "current" ? styles.eventCurrent : "",
    event.state === "pending" || event.state === "suggested" ? styles.eventPending : "",
    event.state === "blocked" ? styles.eventBlocked : "",
  ].filter(Boolean).join(" ");
}

export function PhaseTimeline({
  phases,
  timelineEvents = [],
}: {
  phases: RemedyPhase[];
  timelineEvents?: RemedyTimelineEvent[];
}) {
  const phaseMap = Object.fromEntries(phases.map((phase) => [phase.id, phase]));

  const canonical = CANONICAL_PHASES.map((id) => {
    const real = phaseMap[id];
    return {
      id,
      label: real?.label || PHASE_LABELS[id],
      state: real?.state || ("pending" as RemedyState),
    };
  });

  const currentIndex = canonical.findIndex((phase) => phase.state === "current");
  const lastDoneIndex = canonical.reduce(
    (latest, phase, index) => (phase.state === "done" ? index : latest),
    -1,
  );
  const activeIndex = currentIndex >= 0 ? currentIndex : Math.max(0, lastDoneIndex);
  const progressPct = canonical.length > 1
    ? (activeIndex / (canonical.length - 1)) * 100
    : 0;

  const hasEvents = timelineEvents.length > 0;

  return (
    <section className={styles.timeline} aria-label="Project process timeline" data-ui="phase-timeline">
      <div className={styles.phaseHeader}>
        {canonical.map((phase) => (
          <div
            key={`phase-${phase.id}`}
            className={[styles.phaseItem, stateClass(phase.state)].join(" ")}
            data-phase={phase.id}
            data-state={phase.state}
          >
            <span className={styles.phaseIconShell}>
              <PhaseGlyph phase={phase.id} className={styles.phaseIcon} />
            </span>
            <span className={styles.phaseLabel}>{phase.label}</span>
          </div>
        ))}
      </div>

      <div className={styles.rail} aria-hidden="true">
        <span className={styles.railBase} />
        <span className={styles.railFill} style={{ width: `${progressPct}%` }} />
        {canonical.map((phase, index) => (
          <span
            key={`marker-${phase.id}`}
            className={[styles.phaseMarker, stateClass(phase.state)].join(" ")}
            style={{ left: phasePosition(index) }}
          >
            {phase.state === "done" && <TaskDoneGlyph className={styles.markerCheck} />}
          </span>
        ))}
      </div>

      {hasEvents && (
        <div className={styles.eventRail} aria-label="Real work events">
          <span className={styles.eventRailLine} />
          {timelineEvents.map((event, index) => {
            const left = timelineEvents.length === 1
              ? "0%"
              : `${(index / Math.max(timelineEvents.length - 1, 1)) * 100}%`;

            return (
              <span
                key={event.id}
                className={styles.eventItem}
                style={{ left }}
                title={event.title}
                aria-label={`${event.title}, ${event.kind.replace("_", " ")}`}
              >
                <span className={eventClass(event)} />
              </span>
            );
          })}
        </div>
      )}

      {hasEvents && (
        <div className={styles.legend} aria-label="Timeline legend">
          <span className={styles.legendItem}>
            <span className={[styles.eventDot, styles.eventLlm].join(" ")} />
            <span>LLM Action</span>
          </span>
          <span className={styles.legendItem}>
            <span className={[styles.eventDot, styles.eventTest].join(" ")} />
            <span>Test</span>
          </span>
          <span className={styles.legendItem}>
            <span className={[styles.eventDot, styles.eventReview].join(" ")} />
            <span>Review</span>
          </span>
        </div>
      )}
    </section>
  );
}
