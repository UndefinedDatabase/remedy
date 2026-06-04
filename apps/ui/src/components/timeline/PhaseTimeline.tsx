import type { RemedyPhase, RemedyTaskItem, RemedyTimelineEvent, RemedyTimelineEventKind } from "../../api/types";
import { PhaseGlyph, TaskDoneGlyph } from "../icons/RemedyGlyphs";
import styles from "./PhaseTimeline.module.css";

const CANONICAL_PHASES = ["job", "planning", "build", "test", "review", "finalized"];
const PHASE_LABELS: Record<string, string> = {
  job: "Job", planning: "Planning", build: "Build",
  test: "Test", review: "Review", finalized: "Finalized",
};

const KIND_TYPE: Record<string, RemedyTimelineEventKind> = {
  goal: "llm_action", task: "llm_action", apply: "llm_action", change: "llm_action", memory: "llm_action",
  test: "test",
  review: "review", approval: "review", proof: "review",
};

function phasePosition(index: number): number {
  return (index / (CANONICAL_PHASES.length - 1)) * 100;
}

/* ── Event dot components ── */

function LlmDot({ className }: { className?: string }) {
  return <span className={`${styles.eventDot} ${styles.eventDotAction} ${className || ""}`} />;
}

function TestDot({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 12 12" className={`${styles.eventDotIcon} ${styles.eventDotTest} ${className || ""}`}>
      <circle cx="6" cy="6" r="5" fill="none" stroke="currentColor" strokeWidth=".8" opacity=".4" />
      <polyline points="3.5 6.2 5.2 8 8.5 4.2" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function ReviewDot({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 12 12" className={`${styles.eventDotIcon} ${styles.eventDotReview} ${className || ""}`}>
      <circle cx="6" cy="4" r="2" fill="none" stroke="currentColor" strokeWidth=".9" />
      <path d="M2.2 11c0-2.2 1.7-3.6 3.8-3.6s3.8 1.4 3.8 3.6" fill="none" stroke="currentColor" strokeWidth=".9" />
    </svg>
  );
}

const DOT_COMPONENT = { llm_action: LlmDot, test: TestDot, review: ReviewDot } as const;

/** Derive timeline events from tasks when backend doesn't provide them. */
function fallbackEventsFromTasks(tasks: RemedyTaskItem[]): RemedyTimelineEvent[] {
  return tasks.map((t, idx) => ({
    id: `fallback-${idx}`,
    kind: KIND_TYPE[t.kind] || "llm_action",
    phase: t.kind === "test" ? "test" : t.kind === "review" || t.kind === "approval" || t.kind === "proof" ? "review" : "build",
    done: t.state === "done",
    label: t.label,
  }));
}

export function PhaseTimeline({ phases, tasks, timelineEvents }: {
  phases: RemedyPhase[];
  tasks?: RemedyTaskItem[];
  timelineEvents?: RemedyTimelineEvent[];
}) {
  const phaseMap = Object.fromEntries(phases.map(p => [p.id, p]));

  const canonicalPhases = CANONICAL_PHASES.map(id => {
    const real = phaseMap[id];
    return {
      id,
      label: real?.label || PHASE_LABELS[id] || id,
      state: real?.state || "pending",
    };
  });

  const currentIdx = canonicalPhases.findIndex(p => p.state === "current");
  const doneCount = canonicalPhases.filter(p => p.state === "done").length;
  const progressPct = currentIdx >= 0
    ? phasePosition(currentIdx) + (phasePosition(1) - phasePosition(0)) * 0.5
    : doneCount === canonicalPhases.length ? 100 : phasePosition(Math.max(doneCount - 1, 0));

  const events = (timelineEvents && timelineEvents.length > 0)
    ? timelineEvents
    : fallbackEventsFromTasks(tasks || []);

  return (
    <section className={styles.timeline} aria-label="Project timeline" data-ui="phase-timeline">

      {/* ── Row 1: Phase header — icon + label side by side ── */}
      <div className={styles.phaseHeader}>
        {canonicalPhases.map(phase => (
          <div key={phase.id} className={`${styles.phaseSlot} ${styles[phase.state]}`}>
            <div className={styles.phaseIconShell}>
              {phase.state === "done"
                ? <TaskDoneGlyph className={styles.phaseIcon} />
                : <PhaseGlyph phase={phase.id} className={styles.phaseIcon} />
              }
            </div>
            <span className={styles.phaseLabel}>{phase.label}</span>
          </div>
        ))}
      </div>

      {/* ── Row 2: Rail with progress fill and phase markers ── */}
      <div className={styles.rail}>
        <div className={styles.railBase} />
        <div className={styles.railFill} style={{ width: `${progressPct}%` }} />
        {canonicalPhases.map((phase, i) => {
          const left = phasePosition(i);
          const active = phase.state === "done" || phase.state === "current";
          return (
            <span
              key={`marker-${phase.id}`}
              className={`${styles.phaseMarker} ${active ? styles.phaseMarkerActive : ""}`}
              style={{ left: `${left}%` }}
            />
          );
        })}
      </div>

      {/* ── Row 3: Event rail — dashed line, dots with borders ── */}
      <div className={styles.eventRail}>
        <div className={styles.eventLine} />
        <div className={styles.eventItems}>
          {events.map(ev => {
            const Comp = DOT_COMPONENT[ev.kind] || LlmDot;
            const pending = !ev.done;
            return (
              <span
                key={ev.id}
                className={`${styles.eventItem} ${pending ? styles.eventPending : ""} ${ev.done ? styles.eventDone : ""}`}
              >
                <Comp />
              </span>
            );
          })}
        </div>
      </div>

      {/* ── Row 4: Legend with proper icons ── */}
      <div className={styles.legend}>
        <span className={styles.legendEntry}>
          <LlmDot className={styles.legendIcon} />
          <span>LLM Action</span>
        </span>
        <span className={styles.legendEntry}>
          <TestDot className={styles.legendIcon} />
          <span>Test</span>
        </span>
        <span className={styles.legendEntry}>
          <ReviewDot className={styles.legendIcon} />
          <span>Review</span>
        </span>
      </div>
    </section>
  );
}
