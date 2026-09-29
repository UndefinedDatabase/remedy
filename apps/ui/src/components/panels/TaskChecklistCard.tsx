import { useState } from "react";
import type { RemedyTaskItem } from "../../api/types";
import { selectChecklistRows } from "../../cockpitLogic";
import { ORIGIN_CHIP_TITLE, taskOriginChip } from "../../api/injectView";
import { TaskDoneGlyph, TaskPlannedGlyph } from "../icons/RemedyGlyphs";
import { AddTaskSheet } from "./AddTaskSheet";
import { Term } from "../term/Term";
import styles from "./RightLivePanel.module.css";

/** DECISION F028 D7 (1) — the row's own title, honest either way: disabled
 *  and why, or what pressing it does. */
const ADD_TASK_DISABLED_TITLE = "Adding a task needs the live page's server token.";
const ADD_TASK_ENABLED_TITLE = "Draft a new task for this job.";

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

// DECISION F043 D2 (1): the same conditions, in the same order, as stateText — so the
// explanation a row's state word opens always matches the word it explains.
function stateTerm(task: RemedyTaskItem): string {
  if (task.applyStatus === "partial") return "task.partially_applied";
  if (task.state === "done") return "task.done";
  if (task.state === "current") return "task.in_progress";
  if (task.state === "blocked") return "blocked.task";
  return "task.planned";
}

function outcomeHint(task: RemedyTaskItem): string | null {
  if (task.outcomeSummary) return task.outcomeSummary;
  if (task.testStatus === "fail") return "Tests failing";
  return null;
}

export function TaskChecklistCard({ tasks, jobId, serverToken, onSelectNode }: {
  tasks: RemedyTaskItem[];
  jobId: string;
  serverToken: string;
  onSelectNode: (nodeId: string | null) => void;
}) {
  const [sheetOpen, setSheetOpen] = useState(false);
  const { rows: realRows, completed, total } = selectChecklistRows(tasks);
  const addTaskDisabled = serverToken === "";

  if (realRows.length === 0) {
    return (
      <section className={`${styles.card} ${styles.tasksCard} remedy-checklist`} data-ui="task-checklist-card">
        <header className={styles.cardHeader}>
          <h2><Term term="panel.tasks">Tasks</Term></h2>
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
        <h2><Term term="panel.tasks">Tasks</Term></h2>
        <span>{completed} of {total} completed</span>
      </header>
      <div className={styles.taskList}>
        {realRows.map(row => {
          const hint = outcomeHint(row);
          const chip = taskOriginChip(row);
          return (
            <button key={row.id} type="button" className={`${styles.taskRow} ${styles[row.state] || ""}`}
              onClick={() => { if (row.nodeId) onSelectNode(row.nodeId); }}>
              <span className={styles.taskIcon}>{iconFor(row)}</span>
              <span className={styles.taskLabel}>
                {row.label}
                {hint && <span className={styles.taskHint}>{hint}</span>}
              </span>
              {chip && <span className={styles.originChip} title={ORIGIN_CHIP_TITLE}>{chip}</span>}
              <span className={styles.taskState}><Term term={stateTerm(row)} insideControl>{stateText(row)}</Term></span>
            </button>
          );
        })}
      </div>
      <button
        type="button"
        className={styles.addTaskRow}
        disabled={addTaskDisabled}
        title={addTaskDisabled ? ADD_TASK_DISABLED_TITLE : ADD_TASK_ENABLED_TITLE}
        onClick={() => setSheetOpen(true)}
      >
        + Add Task
      </button>
      {sheetOpen && (
        <AddTaskSheet target={{ jobId, serverToken }} tasks={tasks} onClose={() => setSheetOpen(false)} />
      )}
    </section>
  );
}
