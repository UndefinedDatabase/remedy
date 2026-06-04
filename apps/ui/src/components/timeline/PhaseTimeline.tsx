import type { RemedyPhase, RemedyTaskItem } from "../../api/types";
import { PhaseGlyph, TaskDoneGlyph } from "../icons/RemedyGlyphs";
import styles from "./PhaseTimeline.module.css";

const CANONICAL_PHASES = ["job", "planning", "build", "test", "review", "finalized"];
const PHASE_LABELS: Record<string, string> = {
  job: "Job", planning: "Planning", build: "Build",
  test: "Test", review: "Review", finalized: "Finalized",
};

const KIND_TYPE: Record<string, "action" | "test" | "review"> = {
  goal: "action", task: "action", apply: "action", change: "action", memory: "action",
  test: "test",
  review: "review", approval: "review", proof: "review",
};

/* ── Journey dot components (used in journey row + legend) ── */

function LlmDot({ className }: { className?: string }) {
  return <span className={`${styles.jDot} ${styles.jAction} ${className || ""}`} />;
}

function TestDot({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 12 12" className={`${styles.jIcon} ${styles.jTest} ${className || ""}`}>
      <circle cx="6" cy="6" r="5" fill="none" stroke="currentColor" strokeWidth=".8" opacity=".4" />
      <polyline points="3.5 6.2 5.2 8 8.5 4.2" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function ReviewDot({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 12 12" className={`${styles.jIcon} ${styles.jReview} ${className || ""}`}>
      <circle cx="6" cy="4" r="2" fill="none" stroke="currentColor" strokeWidth=".9" />
      <path d="M2.2 11c0-2.2 1.7-3.6 3.8-3.6s3.8 1.4 3.8 3.6" fill="none" stroke="currentColor" strokeWidth=".9" />
    </svg>
  );
}

const DOT_COMPONENT = { action: LlmDot, test: TestDot, review: ReviewDot } as const;

export function PhaseTimeline({ phases, tasks }: { phases: RemedyPhase[]; tasks?: RemedyTaskItem[] }) {
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
    ? ((currentIdx + 0.5) / canonicalPhases.length) * 100
    : doneCount === canonicalPhases.length ? 100 : 0;

  const journeyItems = (tasks || []).map(t => ({
    id: t.id,
    type: KIND_TYPE[t.kind] || ("action" as const),
    done: t.state === "done",
    pending: t.state === "pending" || t.state === "suggested",
  }));

  return (
    <section className={styles.timeline} aria-label="Project timeline" data-ui="phase-timeline">

      {/* ── Row 1: Phase icons + labels side by side ── */}
      <div className={styles.phaseBar}>
        {canonicalPhases.map(phase => (
          <article key={phase.id} className={`${styles.phase} ${styles[phase.state]}`}>
            <div className={styles.marker}>
              {phase.state === "done"
                ? <TaskDoneGlyph className={styles.markerIcon} />
                : <PhaseGlyph phase={phase.id} className={styles.markerIcon} />
              }
            </div>
            <span className={styles.label}>{phase.label}</span>
          </article>
        ))}
      </div>

      {/* ── Row 2: Progress track with dots at each phase ── */}
      <div className={styles.progressTrack}>
        <div className={styles.progressBg} />
        <div className={styles.progressFill} style={{ width: `${progressPct}%` }} />
        {canonicalPhases.map((phase, i) => {
          const left = ((i + 0.5) / canonicalPhases.length) * 100;
          const active = phase.state === "done" || phase.state === "current";
          return (
            <span
              key={`dot-${phase.id}`}
              className={`${styles.trackDot} ${active ? styles.trackDotActive : ""}`}
              style={{ left: `${left}%` }}
            />
          );
        })}
      </div>

      {/* ── Row 3: Journey timeline — DASHED line, dots with BORDERS, full width ── */}
      <div className={styles.journeyBar}>
        <div className={styles.journeyLine} />
        <div className={styles.journeyItems}>
          {journeyItems.map(item => {
            const Comp = DOT_COMPONENT[item.type];
            return (
              <span
                key={item.id}
                className={`${styles.journeyItem} ${item.pending ? styles.journeyPending : ""} ${item.done ? styles.journeyDone : ""}`}
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
