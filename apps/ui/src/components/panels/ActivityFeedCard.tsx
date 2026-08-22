import type { RemedyActivityItem } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
import { BuilderGlyph, ReviewerGlyph, PersonGlyph, GearGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

const iconByActor: Record<string, typeof BuilderGlyph> = {
  Builder: BuilderGlyph,
  Reviewer: ReviewerGlyph,
  User: PersonGlyph,
  System: GearGlyph,
};

function formatTokenEstimate(tokens: number): string {
  return tokens >= 1000 ? `${(tokens / 1000).toFixed(1)}k` : String(tokens);
}

/** How many live rows the side panel shows. The ring holds up to
 *  BRAIN_RECENT_LIMIT; this card is a glance and the timeline is the archive. */
const LIVE_ROWS_SHOWN = 5;

/** The live half of the card: rows projected from the SSE stream, NEWEST
 *  FIRST. Remedy deliberately does not merge these with the dashboard's REST
 *  activity list — two clocks in one list would order neither honestly — so
 *  live rows REPLACE that list as soon as the stream has produced any. */
function LiveFeed({ recent, recentDropped }: { recent: readonly FeedRow[]; recentDropped: number }) {
  const newestFirst = recent.slice(-LIVE_ROWS_SHOWN).reverse();

  return (
    <div className={styles.activityList}>
      {recentDropped > 0 ? (
        <p className={styles.emptyState}>
          {recentDropped} earlier {recentDropped === 1 ? "event" : "events"} left this window — the timeline keeps them all.
        </p>
      ) : null}
      {newestFirst.map(row => (
        <article key={row.seq} className={styles.activityItem}>
          <div className={styles.actorIcon}><GearGlyph style={{ width: 16, height: 16, color: "white" }} /></div>
          <div>
            <div className={styles.activityMeta}>
              <strong>{row.kind || "event"}</strong>
              {row.timestamp ? <span>{row.timestamp}</span> : null}
              <span className={styles.activityTag}>#{row.seq}</span>
              {row.outcome ? <span className={styles.activityTag}>{row.outcome}</span> : null}
            </div>
            <p>{row.line}</p>
          </div>
        </article>
      ))}
    </div>
  );
}

export function ActivityFeedCard({ activity, recent, recentDropped }: { activity: RemedyActivityItem[]; recent?: readonly FeedRow[]; recentDropped?: number }) {
  const hasActivity = activity.length > 0;
  const live = recent ?? [];

  // The live path wins whenever the stream has produced a row. The dashboard
  // list below is the pre-stream fallback, not a second source of truth.
  if (live.length > 0) {
    return (
      <section className={styles.card}>
        <header className={styles.cardHeader}><h2>Activity</h2></header>
        <LiveFeed recent={live} recentDropped={recentDropped ?? 0} />
      </section>
    );
  }

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}><h2>Activity</h2></header>
      <div className={styles.activityList}>
        {hasActivity ? activity.slice(0, 5).map(item => {
          const Icon = iconByActor[item.actor] || GearGlyph;
          return (
            <article key={item.id} className={styles.activityItem}>
              <div className={styles.actorIcon}><Icon style={{ width: 16, height: 16, color: "white" }} /></div>
              <div>
                <div className={styles.activityMeta}>
                  <strong>{item.actor}</strong>
                  <span>{item.timeLabel}</span>
                  {item.taskId ? <span className={styles.activityTag}>{item.taskId}</span> : null}
                  {item.tokenEstimate ? <span className={styles.activityTag}>~{formatTokenEstimate(item.tokenEstimate)} tok</span> : null}
                </div>
                <p>{item.message}</p>
              </div>
            </article>
          );
        }) : (
          <p className={styles.emptyState}>No activity yet. Events will appear here as the agent works.</p>
        )}
      </div>
    </section>
  );
}
