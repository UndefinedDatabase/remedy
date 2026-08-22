import { useCallback, useEffect, useRef, useState } from "react";
import type { RemedyActivityItem } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
import type { FocusableTask } from "../../api/feedFocus";
import { nodeIdForFeedRow } from "../../api/feedFocus";
import { FEED_SCROLL_START, nextFeedScroll, shouldFollowNewest, shouldShowNewRowsPill } from "../../api/feedScroll";
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

/** How many live rows the side panel keeps. DECISION F021 D10 raised this from
 *  5 to 40 deliberately: the feature file's binding CSS gives the feed a 52vh
 *  box, and a window that always fits inside its box can never scroll, which
 *  would leave feedScroll.ts's never-yank rule unreachable in the product. The
 *  ring still holds BRAIN_RECENT_LIMIT and the timeline is still the archive. */
const LIVE_ROWS_SHOWN = 40;

/** The live half of the card: rows projected from the SSE stream, NEWEST
 *  FIRST. Remedy deliberately does not merge these with the dashboard's REST
 *  activity list — two clocks in one list would order neither honestly — so
 *  live rows REPLACE that list as soon as the stream has produced any.
 *
 *  Because rows render newest FIRST, the newest edge is the TOP of the box, so
 *  `distanceFromNewest` is `scrollTop` (DECISION F021 D10). feedScroll.ts owns
 *  every decision about following and unseen counts; this component owns only
 *  the DOM reads that rule cannot make, which is what keeps the rule testable
 *  in a repository with no DOM. */
function LiveFeed({ recent, recentDropped, tasks, onSelectNode }: {
  recent: readonly FeedRow[];
  recentDropped: number;
  tasks: readonly FocusableTask[];
  onSelectNode: (nodeId: string | null) => void;
}) {
  const newestFirst = recent.slice(-LIVE_ROWS_SHOWN).reverse();
  const boxRef = useRef<HTMLDivElement | null>(null);
  const [scrollState, setScrollState] = useState(FEED_SCROLL_START);
  // What the reader has already been shown. A ref rather than state: it is read
  // and written inside the arrival effect and must never itself cause a render.
  const seenCountRef = useRef(recent.length);

  const readDistanceFromNewest = useCallback((): number => {
    return boxRef.current ? boxRef.current.scrollTop : 0;
  }, []);

  useEffect(() => {
    const arrived = Math.max(0, recent.length - seenCountRef.current);
    seenCountRef.current = recent.length;
    if (arrived === 0) {
      return;
    }
    const distance = readDistanceFromNewest();
    setScrollState(prev => nextFeedScroll(prev, arrived, distance));
    // NEVER YANK: only a reader already at the newest edge is moved. A reader
    // who scrolled up keeps their position and accumulates an unseen count.
    if (shouldFollowNewest(distance) && boxRef.current) {
      boxRef.current.scrollTop = 0;
    }
  }, [recent.length, readDistanceFromNewest]);

  // Returning to the edge clears the unseen count, through the same rule that
  // accumulated it: no row arrives here, so `arrived` is 0.
  const handleFeedScroll = useCallback(() => {
    setScrollState(prev => nextFeedScroll(prev, 0, readDistanceFromNewest()));
  }, [readDistanceFromNewest]);

  const jumpToLive = useCallback(() => {
    if (boxRef.current) {
      boxRef.current.scrollTop = 0;
    }
    setScrollState(FEED_SCROLL_START);
  }, []);

  return (
    <div className={styles.activityList} ref={boxRef} onScroll={handleFeedScroll}>
      {shouldShowNewRowsPill(scrollState) ? (
        <button type="button" className={styles.jumpToLivePill} onClick={jumpToLive}>
          Jump to live · {scrollState.unseenRows} new
        </button>
      ) : null}
      {recentDropped > 0 ? (
        <p className={styles.emptyState}>
          {recentDropped} earlier {recentDropped === 1 ? "event" : "events"} left this window — the timeline keeps them all.
        </p>
      ) : null}
      {newestFirst.map(row => {
        const nodeId = nodeIdForFeedRow(row, tasks);
        const body = (
          <>
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
          </>
        );
        // A row with no node renders as the article it always was. Only a row
        // that can really jump becomes a button, so the affordance never lies.
        return nodeId ? (
          <button key={row.seq} type="button" title="Show this task in the graph"
            className={`${styles.activityItem} ${styles.activityItemJump}`}
            onClick={() => onSelectNode(nodeId)}>
            {body}
          </button>
        ) : (
          <article key={row.seq} className={styles.activityItem}>{body}</article>
        );
      })}
    </div>
  );
}

export function ActivityFeedCard({ activity, recent, recentDropped, tasks, onSelectNode }: {
  activity: RemedyActivityItem[];
  recent?: readonly FeedRow[];
  recentDropped?: number;
  tasks?: readonly FocusableTask[];
  onSelectNode?: (nodeId: string | null) => void;
}) {
  const hasActivity = activity.length > 0;
  const live = recent ?? [];

  // The live path wins whenever the stream has produced a row. The dashboard
  // list below is the pre-stream fallback, not a second source of truth.
  if (live.length > 0) {
    return (
      <section className={styles.card}>
        <header className={styles.cardHeader}><h2>Activity</h2></header>
        <LiveFeed recent={live} recentDropped={recentDropped ?? 0}
          tasks={tasks ?? []} onSelectNode={onSelectNode ?? (() => {})} />
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
