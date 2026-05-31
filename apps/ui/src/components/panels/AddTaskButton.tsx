import AddIcon from "@mui/icons-material/Add";
import styles from "./RightLivePanel.module.css";

export function AddTaskButton() {
  return (
    <button type="button" className={styles.addTask} title="Task creation from UI is not enabled yet. Use CLI or approve reviewer suggestions." onClick={() => undefined}>
      <AddIcon fontSize="small" />Add Task
    </button>
  );
}
