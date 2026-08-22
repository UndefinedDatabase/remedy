import { useEffect, useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import type { FeedRow } from "../../api/feedRow";
import { newestActionRow } from "../../api/actionClass";
import { recencyLevel } from "../../api/recency";
import { deriveAgentStatus } from "../../cockpitLogic";
import { SparkGlyph, TaskCurrentGlyph } from "../icons/RemedyGlyphs";
import styles from "./RightLivePanel.module.css";

/** How often the card re-reads the clock. The dot fades on its own between
 *  FRESH_WINDOW_MS and QUIET_WINDOW_MS with no new event to re-render it, so
 *  the card must ask the time again; one second is far finer than the
 *  five-second window the fade begins at and costs one state write per second. */
const RECENCY_TICK_MS = 1000;

/** The clock, bound HERE because this is the edge that has one. recency.ts
 *  stays a pure function of two numbers and never reads a clock itself, which
 *  is what lets the fade be tested without waiting for it. */
function useRecencyNowMs(): number {
  const [nowMs, setNowMs] = useState(() => Date.now());
  useEffect(() => {
    const timer = window.setInterval(() => { setNowMs(Date.now()); }, RECENCY_TICK_MS);
    return () => { window.clearInterval(timer); };
  }, []);
  return nowMs;
}

export function AgentNowCard({ dashboard, recent }: { dashboard: RemedyDashboard; recent?: readonly FeedRow[] }) {
  const { status: statusText, detail, isRunning } = deriveAgentStatus(dashboard);
  // The newest ACTION the stream has produced, which is what this card is FOR.
  // Bookkeeping is excluded on purpose (actionClass.ts): a card that narrated
  // the agent reading files would report motion where there was none.
  const liveAction = newestActionRow(recent ?? []);
  const nowMs = useRecencyNowMs();
  // Both instants subtracted here sit on ONE clock: `receivedAtMs` is the
  // arrival stamp the host took from this same `Date.now`, never the envelope's
  // server-clock string, which a server running behind would render as a dead
  // agent. Remedy deliberately does NOT feed the badge from this level yet: the
  // dot may say "acted 20s ago" while the job has ended, and a badge saying
  // "Live" beside the word "Idle" is the R-0652 defect. The badge keeps the
  // agent's own running flag until that trade-off is ruled on its own.
  const level = recencyLevel(liveAction ? liveAction.receivedAtMs : null, nowMs);

  return (
    <section className={styles.card}>
      <header className={styles.cardHeader}>
        <h2>Agent is doing now</h2>
        {isRunning && <span className={styles.liveSmall}><span /> Live</span>}
      </header>
      <div className={styles.agentNow}>
        <div className={styles.actorIcon}>
          {isRunning ? <TaskCurrentGlyph style={{ width: 16, height: 16, color: "white" }} /> : <SparkGlyph style={{ width: 16, height: 16, color: "white" }} />}
        </div>
        <div>
          <strong>{statusText}</strong>
          <p>{liveAction ? liveAction.line : detail}</p>
        </div>
        <span className={styles.activityDot} data-recency={level} aria-hidden="true" />
      </div>
    </section>
  );
}
