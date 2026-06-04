import type { RemedyDashboard, RemedyGraphNode } from "../../api/types";
import { TaskDoneGlyph, TaskCurrentGlyph, TaskPlannedGlyph } from "../icons/RemedyGlyphs";
import styles from "./DetailPopover.module.css";

const STATE_LABELS: Record<string, string> = {
  done: "Completed",
  current: "In progress",
  planned: "Planned",
  blocked: "Blocked",
  pending: "Planned",
  suggested: "Suggested",
};

function StateIcon({ state }: { state: string }) {
  if (state === "done") return <TaskDoneGlyph style={{ width: 14, height: 14, color: "var(--remedy-green, #4cc681)" }} />;
  if (state === "current") return <TaskCurrentGlyph style={{ width: 14, height: 14, color: "var(--remedy-blue, #4c83ff)" }} />;
  return <TaskPlannedGlyph style={{ width: 14, height: 14, color: "var(--remedy-ink-soft, #6f82a8)" }} />;
}

function TestBadge({ status }: { status?: string }) {
  if (!status || status === "none") return null;
  const pass = status === "pass";
  return (
    <span className={pass ? styles.badgePass : styles.badgeFail}>
      {pass ? "Tests pass" : "Tests fail"}
    </span>
  );
}

export function DetailPopover({ dashboard, selectedNode, onClose }: { dashboard: RemedyDashboard; selectedNode: RemedyGraphNode; onClose: () => void }) {
  const task = dashboard.tasks.find(i => i.nodeId === selectedNode.nodeId);
  const title = task?.label || selectedNode.label || "Task";
  const state = task?.state || selectedNode.state;
  const stateLabel = STATE_LABELS[state] || state;

  const outcomeSummary = task?.outcomeSummary;
  const changedFiles = task?.changedFilesCount;
  const testStatus = task?.testStatus;

  return (
    <aside className={`${styles.popover} remedy-detail-compact`} aria-label="Task details" data-ui="detail-popover">
      <button className={styles.close} type="button" aria-label="Close" onClick={onClose}>&times;</button>
      <h2 className={styles.title}>{title}</h2>

      <div className={styles.statusRow}>
        <StateIcon state={state} />
        <span className={styles.statusLabel}>{stateLabel}</span>
        <TestBadge status={testStatus} />
      </div>

      <section className={styles.section}>
        <h3>Outcome</h3>
        <p>{outcomeSummary || (
          state === "done" ? "Completed successfully."
          : state === "current" ? "Work is in progress."
          : state === "blocked" ? "Blocked and needs attention."
          : "Not started yet."
        )}</p>
        {changedFiles != null && changedFiles > 0 && (
          <p className={styles.detail}>{changedFiles} file{changedFiles !== 1 ? "s" : ""} changed</p>
        )}
      </section>

      <section className={styles.section}>
        <h3>Checked</h3>
        <p>{task?.checked ? "Verified" : "Not yet checked"}</p>
      </section>

      <section className={styles.section}>
        <h3>Action needed</h3>
        <p>{state === "blocked"
          ? "Review what is blocking this task."
          : state === "done"
          ? "No action needed."
          : "Waiting for agent to continue."
        }</p>
      </section>
    </aside>
  );
}
