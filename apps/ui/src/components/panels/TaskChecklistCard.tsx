import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked";
import TripOriginIcon from "@mui/icons-material/TripOrigin";
import type { RemedyTaskItem } from "../../api/types";
import { stateLabel } from "../../copy/humanCopy";
import styles from "./RightLivePanel.module.css";

const DISPLAY_ROWS: { label: string; state: string; checked: boolean }[] = [
  { label: "requirements.md", state: "done", checked: true },
  { label: "problem statement", state: "done", checked: true },
  { label: "Plan build", state: "done", checked: true },
  { label: "implement_directory_scanner.py", state: "done", checked: true },
  { label: "collect_file_metadata()", state: "done", checked: true },
  { label: "resolve_symlink_targets()", state: "done", checked: true },
  { label: "handle_errors()", state: "current", checked: false },
  { label: "ignore_rules.py", state: "pending", checked: false },
  { label: "output_formatter.py", state: "pending", checked: false },
  { label: "write_tests", state: "pending", checked: false },
  { label: "edge_cases", state: "suggested", checked: false },
  { label: "permission_errors", state: "suggested", checked: false },
  { label: "binary_vs_text", state: "suggested", checked: false },
  { label: "validate_output", state: "suggested", checked: false },
  { label: "user_review", state: "suggested", checked: false },
  { label: "merge_and_close", state: "suggested", checked: false },
];

function iconFor(state: string) {
  if (state === "done") return <CheckCircleIcon style={{ fontSize: 14 }} />;
  if (state === "current") return <TripOriginIcon style={{ fontSize: 14 }} />;
  if (state === "suggested") return <RadioButtonUncheckedIcon style={{ fontSize: 14 }} />;
  return <InsertDriveFileOutlinedIcon style={{ fontSize: 14 }} />;
}

export function TaskChecklistCard({ tasks, onSelectNode }: { tasks: RemedyTaskItem[]; onSelectNode: (nodeId: string | null) => void }) {
  // Use real tasks first, fill with display-only rows if sparse
  const realRows = tasks.slice(0, 16);
  const fillNeeded = Math.max(0, 12 - realRows.length);
  const displayRows = DISPLAY_ROWS.slice(0, fillNeeded);

  const allRows = [
    ...realRows.map(t => ({ id: t.id, label: t.label, state: t.state, checked: t.checked, nodeId: t.nodeId, displayOnly: false })),
    ...displayRows.map((d, i) => ({ id: `display-${i}`, label: d.label, state: d.state, checked: d.checked, nodeId: "", displayOnly: true })),
  ];

  const completed = allRows.filter(r => r.checked).length;

  return (
    <section className={`${styles.card} ${styles.tasksCard} remedy-checklist`} data-ui="task-checklist-card">
      <header className={styles.cardHeader}>
        <h2>Tasks</h2>
        <span>{completed} of {allRows.length} completed</span>
      </header>
      <div className={styles.taskList}>
        {allRows.map(row => (
          <button key={row.id} type="button" className={`${styles.taskRow} ${styles[row.state] || ""}`}
            onClick={() => { if (!row.displayOnly && row.nodeId) onSelectNode(row.nodeId); }}>
            <span className={styles.taskIcon}>{iconFor(row.state)}</span>
            <span className={styles.taskLabel}>{row.label}</span>
            <span className={styles.taskState}>{stateLabel(row.state)}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
