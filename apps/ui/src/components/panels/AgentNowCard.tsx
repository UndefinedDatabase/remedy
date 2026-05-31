import CodeIcon from "@mui/icons-material/Code";
import PauseCircleOutlineIcon from "@mui/icons-material/PauseCircleOutline";
import type { RemedyDashboard } from "../../api/types";
import styles from "./RightLivePanel.module.css";

export function AgentNowCard({ dashboard }: { dashboard: RemedyDashboard }) {
  const isIdle = !dashboard.live.running;
  const Icon = isIdle ? PauseCircleOutlineIcon : CodeIcon;
  const statusText = isIdle ? "Agent is idle" : "Agent is doing now";
  const taskLabel = isIdle
    ? "No active work. Run a command to start."
    : dashboard.live.activeTaskLabel;

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>{statusText}</h2>
        {!isIdle && <span className={styles.liveSmall}><span /> Live</span>}
      </header>
      <div className={styles.agentNow}>
        <div className={styles.actorIcon}><Icon fontSize="small" /></div>
        <div>
          <strong>{isIdle ? "Idle" : `${dashboard.live.latestActor} is working`}</strong>
          <p>{taskLabel}</p>
        </div>
        {!isIdle && <time>Just now</time>}
      </div>
    </section>
  );
}
