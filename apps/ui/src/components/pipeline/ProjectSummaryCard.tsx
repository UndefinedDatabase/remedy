import type { RemedyProjectSummary } from "../../api/types";
import styles from "./Pipeline.module.css";

export function ProjectSummaryCard({ summary }: { summary: RemedyProjectSummary | null }) {
  if (!summary) return null;

  return (
    <section className={styles.projectCard} data-testid="project-summary-card">
      <header className={styles.panelHeader}><h2>Project</h2></header>
      <div className={styles.projectGrid}>
        <span className={styles.projectLabel}>Jobs</span>
        <span>{summary.job_count}</span>

        {summary.active_job_count > 0 && (
          <>
            <span className={styles.projectLabel}>Active</span>
            <span>{summary.active_job_count}</span>
          </>
        )}

        {summary.blocked_job_count > 0 && (
          <>
            <span className={styles.projectLabel}>Blocked</span>
            <span className={styles.projectBlocked}>{summary.blocked_job_count}</span>
          </>
        )}

        {summary.repeated_pattern_count > 0 && (
          <>
            <span className={styles.projectLabel}>Patterns</span>
            <span>{summary.repeated_pattern_count} repeated</span>
          </>
        )}

        <span className={styles.projectLabel}>Model check</span>
        <span>{summary.model_quality_confidence}</span>
      </div>

      {summary.current_focus && (
        <div className={styles.projectFocus}>{summary.current_focus}</div>
      )}

      {summary.top_blocker && (
        <div className={styles.projectBlocker}>Blocker: {summary.top_blocker}</div>
      )}

      {summary.suggested_next_step && (
        <div className={styles.projectNext}>{summary.suggested_next_step}</div>
      )}

      {summary.next_command && (
        <code
          className={styles.commandCode}
          onClick={() => navigator.clipboard?.writeText(summary.next_command)}
          title="Click to copy"
        >
          {summary.next_command}
        </code>
      )}
    </section>
  );
}
