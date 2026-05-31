import AssignmentOutlinedIcon from "@mui/icons-material/AssignmentOutlined";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import TimelineIcon from "@mui/icons-material/Timeline";
import type { RemedyMetric } from "../../api/types";
import styles from "./TopMetricsBar.module.css";

const iconByKey = { open: AssignmentOutlinedIcon, planned: CalendarMonthOutlinedIcon, done: CheckCircleOutlineIcon, progress: TimelineIcon };

export function TopMetricsBar({ metrics }: { metrics: RemedyMetric[] }) {
  return (
    <section className={`${styles.bar} remedy-glass-card`} aria-label="Project metrics" data-ui="top-metrics-bar">
      {metrics.map(m => {
        const Icon = iconByKey[m.key];
        return (
          <article key={m.key} className={styles.metric}>
            <div className={styles.iconBox}><Icon fontSize="small" /></div>
            <div>
              <div className={styles.label}>{m.label}</div>
              <div className={styles.value}>{m.value}{m.suffix}</div>
              {m.key === "progress" && <div className={styles.progressTrack}><span style={{ width: `${Math.max(0, Math.min(m.value, 100))}%` }} /></div>}
            </div>
          </article>
        );
      })}
    </section>
  );
}
