import type { RemedyProjectSummary } from "../../api/types";
import styles from "./Pipeline.module.css";

export function ProjectSummaryCard({ summary }: { summary: RemedyProjectSummary | null }) {
  if (!summary) return null;

  return (
    <section className={styles.projectMiniCard} data-testid="project-summary-card">
      <header className={styles.projectHeader}><h2>Project</h2></header>
      <div className={styles.projectChips}>
        <span className={styles.projectChip}>{summary.job_count} jobs</span>
        {summary.active_job_count > 0 && (
          <span className={styles.projectChip}>{summary.active_job_count} active</span>
        )}
        {summary.blocked_job_count > 0 && (
          <span className={styles.projectChipWarning}>{summary.blocked_job_count} blocked</span>
        )}
        {summary.repeated_pattern_count > 0 && (
          <span className={styles.projectChip}>{summary.repeated_pattern_count} patterns</span>
        )}
        <span className={styles.projectChip}>model: {summary.model_quality_confidence}</span>
      </div>

      {summary.current_focus && (
        <div className={styles.projectFocus}>{summary.current_focus}</div>
      )}

      {summary.top_blocker && (
        <div className={styles.projectBlockerLine}>Blocker: {summary.top_blocker}</div>
      )}

      {summary.suggested_next_step && (
        <div className={styles.projectNextLine}>{summary.suggested_next_step}</div>
      )}

      {summary.next_command && (
        <button
          type="button"
          className={styles.projectCommandButton}
          onClick={() => navigator.clipboard?.writeText(summary.next_command)}
          aria-label={`Copy command: ${summary.next_command}`}
          title="Copy command"
        >
          {summary.next_command}
        </button>
      )}
    </section>
  );
}
