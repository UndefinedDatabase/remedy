import type { RemedyPhase, RemedyTaskItem } from "../../api/types";
import { PhaseGlyph, TaskDoneGlyph } from "../icons/RemedyGlyphs";
import styles from "./PhaseTimeline.module.css";

const CANONICAL_PHASES = ["job", "planning", "build", "test", "review", "finalized"];
const PHASE_LABELS: Record<string, string> = {
  job: "Job", planning: "Planning", build: "Build",
  test: "Test", review: "Review", finalized: "Finalized",
};

/* Map task kind to a dot color class for the journey row */
const KIND_DOT: Record<string, string> = {
  goal: "dotAction", task: "dotAction", apply: "dotAction", change: "dotAction",
  test: "dotTest",
  review: "dotReview", approval: "dotReview", proof: "dotReview",
  memory: "dotAction",
};

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
  const progressPct = currentIdx >= 0 ? ((currentIdx + 0.5) / canonicalPhases.length) * 100 : 0;

  /* Journey dots from tasks */
  const dots = (tasks || []).map(t => ({
    id: t.id,
    cls: KIND_DOT[t.kind] || "dotAction",
    state: t.state,
  }));

  return (
    <section className={styles.timeline} aria-label="Project timeline" data-ui="phase-timeline">
      {/* ── Phase row: markers on the track line ── */}
      <div className={styles.phaseRow}>
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
        {/* Track line behind markers */}
        <div className={styles.track} aria-hidden>
          <div className={styles.trackBg} />
          <div className={styles.trackProgress} style={{ width: `${progressPct}%` }} />
        </div>
      </div>

      {/* ── Journey dots row ── */}
      {dots.length > 0 && (
        <div className={styles.journeyRow} aria-label="Task progress dots">
          {dots.map(d => (
            <span
              key={d.id}
              className={`${styles.journeyDot} ${styles[d.cls]} ${d.state === "done" ? styles.dotDone : ""}`}
            />
          ))}
        </div>
      )}

      {/* ── Legend ── */}
      <div className={styles.legend}>
        <span className={styles.legendItem}>
          <span className={`${styles.legendDot} ${styles.dotAction}`} />LLM Action
        </span>
        <span className={styles.legendItem}>
          <span className={`${styles.legendDot} ${styles.dotTest}`} />Test
        </span>
        <span className={styles.legendItem}>
          <span className={`${styles.legendDot} ${styles.dotReview}`} />Review
        </span>
      </div>
    </section>
  );
}
