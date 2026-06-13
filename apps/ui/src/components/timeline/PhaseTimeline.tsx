import type {
  RemedyPhase,
  RemedyTimelineEvent,
  RemedyTimelinePhase,
  RemedyState,
} from "../../api/types";
import { CodeOrbGlyph, FlaskGlyph, PersonGlyph, TaskDoneGlyph } from "../icons/RemedyGlyphs";
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

const MAX_EVENT_CHIPS = 18;

function phasePercent(index: number): number {
  return (index / (CANONICAL_PHASES.length - 1)) * 100;
}

function stateClass(state: RemedyState) {
  if (state === "done") return styles.isDone;
  if (state === "current") return styles.isCurrent;
  if (state === "blocked") return styles.isBlocked;
  return styles.isPending;
}

function eventChipClass(event: RemedyTimelineEvent) {
  return [
    styles.eventChip,
    event.kind === "llm_action" ? styles.eventLlm : "",
    event.kind === "test" ? styles.eventTest : "",
    event.kind === "review" ? styles.eventReview : "",
    event.state === "current" ? styles.eventCurrent : "",
    event.state === "blocked" ? styles.eventBlocked : "",
  ].filter(Boolean).join(" ");
}

function EventGlyph({ kind }: { kind: RemedyTimelineEvent["kind"] }) {
  if (kind === "test") return <FlaskGlyph />;
  if (kind === "review") return <PersonGlyph />;
  return <CodeOrbGlyph />;
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

  // Keep the most recent MAX_EVENT_CHIPS events (oldest trimmed first), then
  // group by phase so chips cluster under their phase segment.
  const trimmed = timelineEvents.slice(-MAX_EVENT_CHIPS);
  const phaseIndex = Object.fromEntries(CANONICAL_PHASES.map((id, i) => [id, i]));
  const segmentWidth = 100 / (CANONICAL_PHASES.length - 1);
  const byPhase = new Map<string, RemedyTimelineEvent[]>();
  for (const e of trimmed) {
    const list = byPhase.get(e.phase) || [];
    list.push(e);
    byPhase.set(e.phase, list);
  }

  const positioned: { event: RemedyTimelineEvent; left: number }[] = [];
  for (const [phase, list] of byPhase) {
    const start = phasePercent(phaseIndex[phase] ?? 0);
    list.forEach((event, slot) => {
      const left = start + ((slot + 1) / (list.length + 1)) * segmentWidth;
      positioned.push({ event, left: Math.max(0, Math.min(left, 100)) });
    });
  }

  return (
    <section className={styles.timeline} aria-label="Project process timeline" data-ui="phase-timeline">
      <div className={styles.phaseHeader}>
        {canonical.map((phase, index) => (
          <div
            key={`phase-${phase.id}`}
            className={[styles.phaseItem, stateClass(phase.state)].join(" ")}
            style={{ left: `${phasePercent(index)}%` }}
            data-phase={phase.id}
            data-state={phase.state}
          >
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
            style={{ left: `${phasePercent(index)}%` }}
          >
            {phase.state === "done" && <TaskDoneGlyph className={styles.markerCheck} />}
          </span>
        ))}
      </div>

      <div className={styles.eventRail} aria-label="Real work event rail">
        {positioned.map(({ event, left }) => (
          <span
            key={event.id}
            className={styles.eventItem}
            style={{ left: `${left}%` }}
            title={event.title}
            aria-label={`${event.title}, ${event.kind.replace("_", " ")}`}
          >
            <span className={styles.eventTick} aria-hidden="true" />
            <span className={eventChipClass(event)} aria-hidden="true">
              <EventGlyph kind={event.kind} />
            </span>
          </span>
        ))}
      </div>

      <div className={styles.legend} aria-label="Timeline legend">
        <span className={styles.legendItem}>
          <span className={[styles.eventChip, styles.eventLlm].join(" ")}><CodeOrbGlyph /></span>
          <span>LLM Action</span>
        </span>
        <span className={styles.legendItem}>
          <span className={[styles.eventChip, styles.eventTest].join(" ")}><FlaskGlyph /></span>
          <span>Test</span>
        </span>
        <span className={styles.legendItem}>
          <span className={[styles.eventChip, styles.eventReview].join(" ")}><PersonGlyph /></span>
          <span>Review</span>
        </span>
      </div>
    </section>
  );
}
