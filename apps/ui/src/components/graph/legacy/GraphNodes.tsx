import type { NodeProps } from "@xyflow/react";
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

export function HotspotNode({ data, selected }: NodeProps) {
  const state = String(data.state || "pending");
  return (
    <div className={`${styles.hotspotNode} ${stateClass(state)} ${selected ? styles.selected : ""}`}>
      <span className={styles.nodeLabel}>{String(data.label || "")}</span>
    </div>
  );
}

// Keep WorkNode export for backward compat
export const WorkNode = HotspotNode;
export const TinyNode = HotspotNode;
