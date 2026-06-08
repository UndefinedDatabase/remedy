import styles from "./RightLivePanel.module.css";

function PlusGlyph({ style }: { style?: React.CSSProperties }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" style={{ width: 16, height: 16, ...style }}>
      <path d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" />
    </svg>
  );
}

export function AddTaskButton() {
  return (
    <button type="button" className={styles.addTask} title="Task creation from UI is not enabled yet." onClick={() => undefined}>
      <PlusGlyph />Add Task
    </button>
  );
}
