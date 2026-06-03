import type { RemedyDashboard } from "../../api/types";
import { SparkGlyph, TaskCurrentGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

export function AgentNowCard({ dashboard }: { dashboard: RemedyDashboard }) {
  const isRunning = dashboard.live.running;
  const isWaiting = dashboard.workerStatus?.lifecycle_state === "waiting_for_approval";
  const isBlocked = dashboard.workerStatus?.lifecycle_state === "blocked";

  let statusText = "Idle";
  let detail = "No active work.";

  if (isRunning) {
    statusText = "Working";
    detail = dashboard.live.activeTaskLabel || "Processing a task.";
  } else if (isWaiting) {
    statusText = "Needs your decision";
    detail = "A patch is waiting for approval.";
  } else if (isBlocked) {
    const reason = dashboard.workerStatus?.why_it_stopped?.replace(/_/g, " ") || "";
    statusText = "Blocked";
    detail = reason || "Cannot continue.";
  }

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>Agent</h2>
        {isRunning && <span className={styles.liveSmall}><span /> Live</span>}
      </header>
      <div className={styles.agentNow}>
        <div className={styles.actorIcon}>
          {isRunning ? <TaskCurrentGlyph style={{ width: 16, height: 16, color: "white" }} /> : <SparkGlyph style={{ width: 16, height: 16, color: "white" }} />}
        </div>
        <div>
          <strong>{statusText}</strong>
          <p>{detail}</p>
        </div>
      </div>
    </section>
  );
}
