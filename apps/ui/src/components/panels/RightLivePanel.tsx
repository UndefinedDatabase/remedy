import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import type { BrainStreamStatus } from "../../api/brainStream";
import type { FeedRow } from "../../api/feedRow";
import { orderDecisionInbox } from "../../api/decisionOrder";
import { jobPauseAction } from "../../api/pauseView";
import { liveIsActive } from "../../cockpitLogic";
import { NeedsAttentionCard } from "./NeedsAttentionCard";
import { DecisionInboxCard } from "./DecisionInboxCard";
import { ActivityFeedCard } from "./ActivityFeedCard";
import { AgentNowCard } from "./AgentNowCard";
import { LiveStatusPill } from "./LiveStatusPill";
import { PauseControl } from "./PauseControl";
import { TaskChecklistCard } from "./TaskChecklistCard";
import styles from "./RightLivePanel.module.css";

export function RightLivePanel({ dashboard, serverToken, onSelectNode, streamStatus, replay, recent, recentDropped, onOpenLessons }: { dashboard: RemedyDashboard; serverToken: string; onSelectNode: (nodeId: string | null) => void; streamStatus?: BrainStreamStatus | null; replay?: boolean; recent?: readonly FeedRow[]; recentDropped?: number; onOpenLessons?: () => void }) {
  const [showAdvanced, setShowAdvanced] = useState(false);

  return (
    <aside className={styles.panel} data-ui="right-live-panel">
      <LiveStatusPill live={liveIsActive(dashboard)} streamStatus={streamStatus} replay={replay} />
      <AgentNowCard dashboard={dashboard} recent={recent} />
      <PauseControl target={{ jobId: dashboard.jobId, serverToken }} scope="job" action={jobPauseAction(dashboard)} />
      <NeedsAttentionCard dashboard={dashboard} />
      {/* The inbox addresses the job the DASHBOARD names, the same value the
          stream is opened against (DECISION F008 D3), never one re-read from
          the URL beside it. */}
      <DecisionInboxCard decisions={orderDecisionInbox(dashboard.decisionInbox)} tasks={dashboard.tasks} jobId={dashboard.jobId} serverToken={serverToken} onSelectNode={onSelectNode} />
      <ActivityFeedCard activity={dashboard.activity} recent={recent} recentDropped={recentDropped} tasks={dashboard.tasks} onSelectNode={onSelectNode} jobId={dashboard.jobId} serverToken={serverToken} stage={dashboard.live.stage} />
      <TaskChecklistCard tasks={dashboard.tasks} jobId={dashboard.jobId} onSelectNode={onSelectNode} />
      {/* The learning overlay's entry point (T5_F265 T002, DECISION F265 D3), in the quiet style
          of the toggle below; the shell owns whether the overlay is open. */}
      {onOpenLessons && (
        <button type="button" className={styles.advancedToggle} onClick={onOpenLessons}>
          Lessons
        </button>
      )}
      <button
        type="button"
        className={styles.advancedToggle}
        onClick={() => setShowAdvanced(!showAdvanced)}
        aria-expanded={showAdvanced}
      >
        {showAdvanced ? "Hide system details" : "System details"}
      </button>
      {showAdvanced && (
        <div className={styles.advancedSection} data-testid="advanced-details">
          {dashboard.pipeline && (
            <div className={styles.advancedItem}>
              <strong>Pipeline:</strong> {dashboard.pipeline.stop_reason || "running"}
            </div>
          )}
          {dashboard.projectSummary && (
            <div className={styles.advancedItem}>
              <strong>Project:</strong> {dashboard.projectSummary.job_count} jobs, {dashboard.projectSummary.current_focus || "idle"}
            </div>
          )}
        </div>
      )}
    </aside>
  );
}
