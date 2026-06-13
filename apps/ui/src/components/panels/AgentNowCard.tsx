import type { RemedyDashboard } from "../../api/types";
import { deriveAgentStatus } from "../../cockpitLogic";
import { SparkGlyph, TaskCurrentGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

export function AgentNowCard({ dashboard }: { dashboard: RemedyDashboard }) {
  const { status: statusText, detail, isRunning } = deriveAgentStatus(dashboard);

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>Agent is doing now</h2>
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
