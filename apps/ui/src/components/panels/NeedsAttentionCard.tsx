import type { RemedyDashboard } from "../../api/types";
import { CopyGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

interface AttentionItem {
  title: string;
  description: string;
}

function deriveAttentionItem(dashboard: RemedyDashboard): AttentionItem | null {
  const failedTasks = dashboard.tasks.filter(t => t.state === "blocked");
  if (failedTasks.length > 0) {
    return { title: "Task failed", description: `${failedTasks.length} task(s) need attention.` };
  }
  return null;
}

export function NeedsAttentionCard({ dashboard }: { dashboard: RemedyDashboard }) {
  const item = deriveAttentionItem(dashboard);
  if (!item) return null;

  const command = dashboard.nextAction.command;

  return (
    <section className={styles.card} data-ui="needs-attention-card">
      <header className={styles.cardHeader}><h2>Needs your decision</h2></header>
      <strong className={styles.attentionTitle}>{item.title}</strong>
      <p className={styles.attentionDesc}>{item.description}</p>
      <button
        type="button"
        className={styles.attentionAction}
        title={`Copy: ${command}`}
        onClick={() => navigator.clipboard?.writeText(command)}
      >
        <CopyGlyph style={{ width: 14, height: 14 }} />
        Copy next safe command
      </button>
    </section>
  );
}
