import styles from "./RightLivePanel.module.css";

export function LiveStatusPill({ live }: { live: boolean }) {
  return <div className={styles.livePill}><span className={live ? styles.liveDot : styles.idleDot} />{live ? "LIVE" : "IDLE"}</div>;
}
