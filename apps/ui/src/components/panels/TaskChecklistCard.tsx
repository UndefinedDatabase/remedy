import type { RemedyTaskItem } from "../../api/types";
import { selectChecklistRows } from "../../cockpitLogic";
import { TaskDoneGlyph, TaskPlannedGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

// Finding R-0738: a task can be finished AND only partly applied, so apply state is
// read BEFORE the lifecycle state here — otherwise the row says "Done" about changes
// that only half landed. The blue filled check tile is the treatment
// docs/ui/design_reference/ux_spec.md section 11 item 4 binds for that case.
function iconFor(task: RemedyTaskItem) {
  if (task.applyStatus === "partial") return <span className={styles.checkPartial}><TaskDoneGlyph /></span>;
  if (task.state === "done") return <span className={styles.checkDone}><TaskDoneGlyph /></span>;
  if (task.state === "current") return <span className={styles.dotCurrent} />;
  return <TaskPlannedGlyph style={{ width: 16, height: 16, color: "var(--remedy-faint)" }} />;
}

function stateText(task: RemedyTaskItem): string {
  if (task.applyStatus === "partial") return "Partially applied";
  if (task.state === "done") return "Done";
  if (task.state === "current") return "In Progress";
  if (task.state === "blocked") return "Blocked";
  return "Planned";
}

function outcomeHint(task: RemedyTaskItem): string | null {
  if (task.outcomeSummary) return task.outcomeSummary;
  if (task.testStatus === "fail") return "Tests failing";
  return null;
}

export function TaskChecklistCard({ tasks, jobId, onSelectNode }: {
  tasks: RemedyTaskItem[];
  jobId: string;
  onSelectNode: (nodeId: string | null) => void;
}) {
  const { rows: realRows, completed, total } = selectChecklistRows(tasks);
  const proposeCommand = `remedy task propose --job ${jobId}`;

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
        <span>{completed} of {total} completed</span>
      </header>
      <div className={styles.taskList}>
        {realRows.map(row => {
          const hint = outcomeHint(row);
          return (
            <button key={row.id} type="button" className={`${styles.taskRow} ${styles[row.state] || ""}`}
              onClick={() => { if (row.nodeId) onSelectNode(row.nodeId); }}>
              <span className={styles.taskIcon}>{iconFor(row)}</span>
              <span className={styles.taskLabel}>
                {row.label}
                {hint && <span className={styles.taskHint}>{hint}</span>}
              </span>
              <span className={styles.taskState}>{stateText(row)}</span>
            </button>
          );
        })}
      </div>
      <button
        type="button"
        className={styles.proposeBtn}
        title={`Copy: ${proposeCommand}`}
        onClick={() => navigator.clipboard?.writeText(proposeCommand)}
      >
        + Propose task (copies CLI command)
      </button>
    </section>
  );
}
