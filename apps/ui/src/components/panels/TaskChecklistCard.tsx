import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked";
import TripOriginIcon from "@mui/icons-material/TripOrigin";
import type { RemedyTaskItem } from "../../api/types";
import { stateLabel } from "../../copy/humanCopy";
import styles from "./RightLivePanel.module.css";

function iconFor(task: RemedyTaskItem) {
  if (task.state === "done") return <CheckCircleIcon fontSize="small" />;
  if (task.state === "current") return <TripOriginIcon fontSize="small" />;
  if (task.state === "suggested") return <RadioButtonUncheckedIcon fontSize="small" />;
  return <InsertDriveFileOutlinedIcon fontSize="small" />;
}

export function TaskChecklistCard({ tasks, onSelectNode }: { tasks: RemedyTaskItem[]; onSelectNode: (nodeId: string) => void }) {
  const completed = tasks.filter(t => t.checked).length;
  return (
    <section className={`${styles.card} remedy-checklist`} data-ui="task-checklist">
      <header className={styles.cardHeader}>
        <h2>Tasks</h2>
        <span>{completed} of {tasks.length} completed</span>
      </header>
      <div className={styles.taskList}>
        {tasks.slice(0, 16).map(task => (
          <button key={task.id} type="button" className={`${styles.taskRow} ${styles[task.state]}`} onClick={() => onSelectNode(task.nodeId)}>
            <span className={styles.taskIcon}>{iconFor(task)}</span>
            <span className={styles.taskLabel}>{task.label}</span>
            <span className={styles.taskState}>{stateLabel(task.state)}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
