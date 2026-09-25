import type { BrainStreamStatus } from "../../api/brainStream";
import styles from "./RightLivePanel.module.css";

/** The cockpit's one honest word about its own freshness, and why the
 *  TRANSPORT's status outranks the dashboard's: a client on the polling
 *  fallback is NOT live however active the job is, and saying so plainly is
 *  this feature's acceptance condition (T5_F008 — the fallback "labels itself
 *  visibly ('delayed') instead of pretending to be live"). That is also why
 *  the dashboard arm is LAST: it is the fallback, not the rule.
 *
 *  `streamStatus` is optional because the pill outlived the rounds that had no
 *  transport to give it, not because nothing supplies one: at `a8965b2d`
 *  RemedyShell began passing a real status down the one chain that reaches
 *  this pill — RemedyShell to RightLivePanel to here — and at `88c55f5d` that
 *  was still the only chain either component had. */
export function LiveStatusPill({ live, streamStatus, replay }: { live: boolean; streamStatus?: BrainStreamStatus | null; replay?: boolean }) {
  // While the timeline is scrubbed the graph shows the past, so the pill says
  // REPLAY in the scrubber's violet before anything about the transport
  // (component_spec.md, LiveStatusPill; DECISION F024 D4).
  if (replay) {
    return <div className={styles.livePill} data-state="replay"><span className={styles.replayDot} />REPLAY</div>;
  }
  if (streamStatus === "delayed") {
    return <div className={styles.livePill} data-state="delayed"><span className={styles.delayedDot} />DELAYED</div>;
  }
  if (streamStatus === "reconnecting") {
    return <div className={styles.livePill} data-state="reconnecting"><span className={styles.reconnectingDot} />RECONNECTING</div>;
  }
  return <div className={styles.livePill} data-state={live ? "live" : "idle"}><span className={live ? styles.liveDot : styles.idleDot} />{live ? "LIVE" : "IDLE"}</div>;
}
