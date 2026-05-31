import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked";
import TripOriginIcon from "@mui/icons-material/TripOrigin";
import type { RemedyTaskItem } from "../../api/types";
import { stateLabel } from "../../copy/humanCopy";
import styles from "./RightLivePanel.module.css";

function iconFor(state: string) {
  if (state === "done") return <CheckCircleIcon style={{ fontSize: 14 }} />;
  if (state === "current") return <TripOriginIcon style={{ fontSize: 14 }} />;
  if (state === "suggested") return <RadioButtonUncheckedIcon style={{ fontSize: 14 }} />;
  return <InsertDriveFileOutlinedIcon style={{ fontSize: 14 }} />;
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
        {realRows.map(row => (
          <button key={row.id} type="button" className={`${styles.taskRow} ${styles[row.state] || ""}`}
            onClick={() => { if (row.nodeId) onSelectNode(row.nodeId); }}>
            <span className={styles.taskIcon}>{iconFor(row.state)}</span>
            <span className={styles.taskLabel}>{row.label}</span>
            <span className={styles.taskState}>{stateLabel(row.state)}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
