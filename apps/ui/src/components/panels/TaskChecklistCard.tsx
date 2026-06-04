import type { RemedyTaskItem } from "../../api/types";
import { TaskDoneGlyph, TaskCurrentGlyph, TaskPlannedGlyph } from "../icons/RemedyGlyphs";
import { stateLabel } from "../../copy/humanCopy";
import styles from "./RightLivePanel.module.css";

function iconFor(state: string) {
  if (state === "done") return <TaskDoneGlyph style={{ width: 14, height: 14, color: "var(--remedy-green, #4cc681)" }} />;
  if (state === "current") return <TaskCurrentGlyph style={{ width: 14, height: 14, color: "var(--remedy-blue, #4c83ff)" }} />;
  return <TaskPlannedGlyph style={{ width: 14, height: 14, color: "var(--remedy-ink-soft, #6f82a8)" }} />;
}

function outcomeHint(task: RemedyTaskItem): string | null {
  if (task.outcomeSummary) return task.outcomeSummary;
  if (task.testStatus === "fail") return "Tests failing";
  return null;
}

export function TaskChecklistCard({ tasks, onSelectNode }: { tasks: RemedyTaskItem[]; onSelectNode: (nodeId: string | null) => void }) {
  const realRows = tasks.slice(0, 16);
  const completed = realRows.filter(r => r.checked).length;

  if (realRows.length === 0) {
    return (
      <section className={`${styles.card} ${styles.tasksCard} remedy-checklist`} data-ui="task-checklist-card">
        <header className={styles.cardHeader}>
          <h2>Tasks</h2>
          <span>No tasks yet</span>
        </header>
        <div className={styles.taskList}>
          <p className={styles.emptyState}>Waiting for the agent to create tasks. Run a job to see real progress here.</p>
        </div>
      </section>
    );
  }

  return (
    <section className={`${styles.card} ${styles.tasksCard} remedy-checklist`} data-ui="task-checklist-card">
      <header className={styles.cardHeader}>
        <h2>Tasks</h2>
        <span>{completed} of {realRows.length} completed</span>
      </header>
      <div className={styles.taskList}>
        {realRows.map(row => {
          const hint = outcomeHint(row);
          return (
            <button key={row.id} type="button" className={`${styles.taskRow} ${styles[row.state] || ""}`}
              onClick={() => { if (row.nodeId) onSelectNode(row.nodeId); }}>
              <span className={styles.taskIcon}>{iconFor(row.state)}</span>
              <span className={styles.taskLabel}>
                {row.label}
                {hint && <span className={styles.taskHint}>{hint}</span>}
              </span>
              <span className={styles.taskState}>{stateLabel(row.state)}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}
