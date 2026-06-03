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

export function DetailPopover({ dashboard, selectedNode, onClose }: { dashboard: RemedyDashboard; selectedNode: RemedyGraphNode; onClose: () => void }) {
  const task = dashboard.tasks.find(i => i.nodeId === selectedNode.nodeId);
  const title = task?.label || selectedNode.label || "Task";
  const state = task?.state || selectedNode.state;
  const stateLabel = STATE_LABELS[state] || state;

  return (
    <aside className={`${styles.popover} remedy-detail-compact`} aria-label="Task details" data-ui="detail-popover">
      <button className={styles.close} type="button" aria-label="Close" onClick={onClose}>×</button>
      <h2 className={styles.title}>{title}</h2>

      <div className={styles.statusRow}>
        <StateIcon state={state} />
        <span className={styles.statusLabel}>{stateLabel}</span>
      </div>

      <section className={styles.section}>
        <h3>Outcome</h3>
        <p>{state === "done"
          ? "This task was completed successfully."
          : state === "current"
          ? "Work is in progress on this task."
          : state === "blocked"
          ? "This task is blocked and needs attention."
          : "This task has not started yet."
        }</p>
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
