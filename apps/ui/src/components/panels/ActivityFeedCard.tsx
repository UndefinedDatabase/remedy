import type { RemedyActivityItem } from "../../api/types";
import { BuilderGlyph, ReviewerGlyph, PersonGlyph, GearGlyph, ArrowSendGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

const iconByActor: Record<string, typeof BuilderGlyph> = {
  Builder: BuilderGlyph,
  Reviewer: ReviewerGlyph,
  User: PersonGlyph,
  System: GearGlyph,
};

export function ActivityFeedCard({ activity }: { activity: RemedyActivityItem[] }) {
  const hasActivity = activity.length > 0;

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}><h2>Activity</h2></header>
      <div className={styles.activityList}>
        {hasActivity ? activity.slice(0, 4).map(item => {
          const Icon = iconByActor[item.actor] || GearGlyph;
          return (
            <article key={item.id} className={styles.activityItem}>
              <div className={styles.actorIcon}><Icon style={{ width: 16, height: 16, color: "white" }} /></div>
              <div>
                <div className={styles.activityMeta}><strong>{item.actor}</strong><span>{item.timeLabel}</span></div>
                <p>{item.message}</p>
              </div>
            </article>
          );
        }) : (
          <p className={styles.emptyState}>No activity yet. Events will appear here as the agent works.</p>
        )}
      </div>
      <div className={styles.askBar}>
        <input readOnly placeholder="Ask something..." aria-label="Ask something" />
        <button type="button" aria-label="Send disabled" title="Chat input is not enabled yet"><ArrowSendGlyph style={{ width: 16, height: 16 }} /></button>
      </div>
    </section>
  );
}
