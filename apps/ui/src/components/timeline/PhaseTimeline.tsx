import type { RemedyPhase } from "../../api/types";
import { PhaseGlyph, TaskDoneGlyph } from "../icons/RemedyGlyphs";
import styles from "./PhaseTimeline.module.css";

const CANONICAL_PHASES = ["job", "planning", "build", "test", "review", "finalized"];
const PHASE_LABELS: Record<string, string> = {
  job: "Job", planning: "Planning", build: "Build",
  test: "Test", review: "Review", finalized: "Finalized",
};

export function PhaseTimeline({ phases }: { phases: RemedyPhase[] }) {
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

  return (
    <section className={styles.timeline} aria-label="Project timeline" data-ui="phase-timeline">
      <div className={styles.track}>
        <div className={styles.trackBg} />
        <div className={styles.trackProgress} style={{ width: `${progressPct}%` }} />
      </div>
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
      </div>
    </section>
  );
}
