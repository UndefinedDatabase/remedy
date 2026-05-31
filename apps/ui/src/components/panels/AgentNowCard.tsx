import CodeIcon from "@mui/icons-material/Code";
import type { RemedyDashboard } from "../../api/types";
import styles from "./RightLivePanel.module.css";

export function AgentNowCard({ dashboard }: { dashboard: RemedyDashboard }) {
  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>Agent is doing now</h2>
        <span className={styles.liveSmall}><span /> Live</span>
      </header>
      <div className={styles.agentNow}>
        <div className={styles.actorIcon}><CodeIcon fontSize="small" /></div>
        <div>
          <strong>{dashboard.live.latestActor} is working</strong>
          <p>{dashboard.live.activeTaskLabel}</p>
        </div>
        <time>Just now</time>
      </div>
    </section>
  );
}
