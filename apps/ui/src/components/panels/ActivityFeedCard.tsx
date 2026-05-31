import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import CodeIcon from "@mui/icons-material/Code";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import RateReviewOutlinedIcon from "@mui/icons-material/RateReviewOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import type { RemedyActivityItem } from "../../api/types";
import styles from "./RightLivePanel.module.css";

const iconByActor = { Builder: CodeIcon, Reviewer: RateReviewOutlinedIcon, User: PersonOutlineIcon, System: SettingsOutlinedIcon };

export function ActivityFeedCard({ activity }: { activity: RemedyActivityItem[] }) {
  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}><h2>Chat / Activity</h2></header>
      <div className={styles.activityList}>
        {activity.slice(0, 4).map(item => {
          const Icon = iconByActor[item.actor];
          return (
            <article key={item.id} className={styles.activityItem}>
              <div className={styles.actorIcon}><Icon fontSize="small" /></div>
              <div>
                <div className={styles.activityMeta}><strong>{item.actor}</strong><span>{item.timeLabel}</span></div>
                <p>{item.message}</p>
              </div>
            </article>
          );
        })}
      </div>
      <div className={styles.askBar}>
        <input readOnly placeholder="Ask something..." aria-label="Ask something" />
        <button type="button" aria-label="Send disabled" title="Chat input is not enabled yet"><ArrowForwardIcon fontSize="small" /></button>
      </div>
    </section>
  );
}
