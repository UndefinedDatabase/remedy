import type { RemedyWorkerStatus } from "../../api/types";
import styles from "./Pipeline.module.css";

const STATE_LABELS: Record<string, string> = {
  idle: "Worker idle",
  running: "Working",
  waiting_for_approval: "Waiting for approval",
  blocked: "Blocked",
  completed: "Done",
  failed: "Failed",
  stale: "Stale worker",
  paused: "Paused",
};

export function WorkerStatusMini({ status }: { status: RemedyWorkerStatus | null }) {
  if (!status) return null;

  const label = STATE_LABELS[status.lifecycle_state] || status.lifecycle_state;

  return (
    <section className={styles.projectMiniCard} data-testid="worker-status-mini">
      <header className={styles.projectHeader}><h2>Worker</h2></header>
      <div className={styles.projectChips}>
        <span className={status.stale ? styles.projectChipWarning : styles.projectChip}>{label}</span>
        {status.queue_count > 0 && (
          <span className={styles.projectChip}>{status.queue_count} queued</span>
        )}
        {status.current_job_id && (
          <span className={styles.projectChip}>job {status.current_job_id.slice(0, 8)}</span>
        )}
      </div>

      {status.why_it_stopped && status.lifecycle_state !== "idle" && (
        <div className={styles.projectNextLine}>{status.why_it_stopped.replace(/_/g, " ")}</div>
      )}

      {status.next_command && (
        <button
          type="button"
          className={styles.projectCommandButton}
          onClick={() => navigator.clipboard?.writeText(status.next_command)}
          aria-label={`Copy command: ${status.next_command}`}
          title="Copy command"
        >
          {status.next_command}
        </button>
      )}
    </section>
  );
}
