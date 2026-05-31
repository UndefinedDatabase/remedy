import type { NodeProps } from "@xyflow/react";
import CheckIcon from "@mui/icons-material/Check";
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked";
import { CodeOrbIcon } from "../icons/CodeOrbIcon";
import styles from "./GraphNodes.module.css";

function stateClass(state: string | undefined) {
  if (state === "done") return styles.done;
  if (state === "current") return styles.current;
  if (state === "suggested") return styles.suggested;
  if (state === "blocked") return styles.blocked;
  return styles.pending;
}

export function RootNode({ selected }: NodeProps) {
  return (
    <div className={`${styles.rootNode} ${selected ? styles.selected : ""}`}>
      <CodeOrbIcon className={styles.codeOrb} />
      <div className={styles.rootPulse} aria-hidden="true" />
    </div>
  );
}

export function WorkNode({ data, selected }: NodeProps) {
  const state = String(data.state || "pending");
  return (
    <div className={`${styles.workNode} ${stateClass(state)} ${selected ? styles.selected : ""}`}>
      <span className={styles.statusIcon}>{state === "done" ? <CheckIcon fontSize="inherit" /> : <RadioButtonUncheckedIcon fontSize="inherit" />}</span>
      <span className={styles.workLabel}>{String(data.label || "Work item")}</span>
    </div>
  );
}

export function TinyNode({ data, selected }: NodeProps) {
  return <div className={`${styles.tinyNode} ${stateClass(String(data.state || "pending"))} ${selected ? styles.selected : ""}`} title={String(data.label || "")} />;
}
