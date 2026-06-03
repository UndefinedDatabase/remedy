import type { RemedyDashboard } from "../../api/types";
import styles from "./RightLivePanel.module.css";

interface AttentionItem {
  title: string;
  description: string;
}

function deriveAttentionItem(dashboard: RemedyDashboard): AttentionItem | null {
  if (dashboard.workerStatus?.lifecycle_state === "waiting_for_approval") {
    return { title: "Needs your decision", description: "A patch is waiting for approval before it can be applied." };
  }
  if (dashboard.workerStatus?.lifecycle_state === "blocked") {
    const reason = dashboard.workerStatus.why_it_stopped?.replace(/_/g, " ") || "unknown reason";
    return { title: "Blocked", description: reason };
  }
  if (dashboard.workerStatus?.stale) {
    return { title: "Worker may have stopped", description: "No recent activity from the worker." };
  }
  const failedTasks = dashboard.tasks.filter(t => t.state === "blocked");
  if (failedTasks.length > 0) {
    return { title: "Task failed", description: `${failedTasks.length} task(s) need attention.` };
  }
  return null;
}

export function NeedsAttentionCard({ dashboard }: { dashboard: RemedyDashboard }) {
  const item = deriveAttentionItem(dashboard);
  if (!item) return null;

  return (
    <section className={styles.card} data-ui="needs-attention-card">
      <header className={styles.cardHeader}><h2>Needs attention</h2></header>
      <strong className={styles.attentionTitle}>{item.title}</strong>
      <p className={styles.attentionDesc}>{item.description}</p>
    </section>
  );
}
