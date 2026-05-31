import CloseIcon from "@mui/icons-material/Close";
import type { RemedyDashboard, RemedyGraphNode } from "../../api/types";
import styles from "./DetailPopover.module.css";

export function DetailPopover({ dashboard, selectedNode, onClose }: { dashboard: RemedyDashboard; selectedNode: RemedyGraphNode; onClose: () => void }) {
  const task = dashboard.tasks.find(i => i.nodeId === selectedNode.nodeId);
  const title = task?.label || selectedNode.label || "Project item";
  const state = task?.state || selectedNode.state;
  const next = task?.nextAction || dashboard.nextAction;
  return (
    <aside className={`${styles.popover} remedy-detail-compact`} aria-label="Selected item details" data-ui="detail-popover">
      <button className={styles.close} type="button" aria-label="Close details" onClick={onClose}><CloseIcon fontSize="small" /></button>
      <h2>{title}</h2>
      <div className={styles.state}>{state}</div>
      <section>
        <h3>Why it matters</h3>
        <p>This item is part of the verified path from goal to completed work.</p>
      </section>
      <section>
        <h3>Evidence</h3>
        <ul><li>{task?.checked ? "Completed and checked." : "Waiting for the next safe step."}</li></ul>
      </section>
      <section>
        <h3>Next safe action</h3>
        <code>{next.command}</code>
      </section>
      <button type="button" className={styles.advanced}>Diagnostics</button>
    </aside>
  );
}
