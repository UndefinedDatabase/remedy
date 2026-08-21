import type { BrainStreamStatus } from "../../api/brainStream";
import styles from "./RightLivePanel.module.css";

/** The cockpit's one honest word about its own freshness, and why the
 *  TRANSPORT's status outranks the dashboard's: a client on the polling
 *  fallback is NOT live however active the job is, and saying so plainly is
 *  this feature's acceptance condition (T5_F008 — the fallback "labels itself
 *  visibly ('delayed') instead of pretending to be live"). That is also why
 *  the dashboard arm is LAST: it is the fallback, not the rule.
 *
 *  `streamStatus` is optional because no caller holds one yet — `useBrainStream`
 *  reaches the cockpit at R30, through RightLivePanel. */
export function LiveStatusPill({ live, streamStatus }: { live: boolean; streamStatus?: BrainStreamStatus | null }) {
  if (streamStatus === "delayed") {
    return <div className={styles.livePill} data-state="delayed"><span className={styles.delayedDot} />DELAYED</div>;
  }
  if (streamStatus === "reconnecting") {
    return <div className={styles.livePill} data-state="reconnecting"><span className={styles.reconnectingDot} />RECONNECTING</div>;
  }
  return <div className={styles.livePill} data-state={live ? "live" : "idle"}><span className={live ? styles.liveDot : styles.idleDot} />{live ? "LIVE" : "IDLE"}</div>;
}
