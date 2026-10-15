import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import type { BrainStreamStatus } from "../../api/brainStream";
import type { FeedRow } from "../../api/feedRow";
import { jobFinishedOf } from "../../api/cockpitTruth";
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

export function RightLivePanel({ dashboard, serverToken, onSelectNode, streamStatus, replay, recent, recentDropped, onOpenPlan, onOpenLessons, onOpenTour, onOpenStory, onOpenResults, onOpenMissions, onOpenTerms, focusedTaskId, systemOpen, onToggleSystem }: { dashboard: RemedyDashboard; serverToken: string; onSelectNode: (nodeId: string | null) => void; streamStatus?: BrainStreamStatus | null; replay?: boolean; recent?: readonly FeedRow[]; recentDropped?: number; onOpenPlan?: () => void; onOpenLessons?: () => void; onOpenTour?: () => void; onOpenStory?: () => void; onOpenResults?: () => void; onOpenMissions?: () => void; onOpenTerms?: () => void; focusedTaskId?: string; systemOpen?: boolean; onToggleSystem?: () => void }) {
  // amend1015 P4.1: the shell owns the system details when it hands them over (the rail opens
  // them too); a panel rendered alone keeps its own.
  const [ownAdvanced, setOwnAdvanced] = useState(false);
  const showAdvanced = systemOpen ?? ownAdvanced;
  const toggleAdvanced = onToggleSystem ?? (() => setOwnAdvanced(!ownAdvanced));

  return (
    <aside className={styles.panel} data-ui="right-live-panel">
      <LiveStatusPill live={liveIsActive(dashboard)} stage={dashboard.live.stage} streamStatus={streamStatus} replay={replay} />
      <AgentNowCard dashboard={dashboard} recent={recent} />
      <PauseControl target={{ jobId: dashboard.jobId, serverToken }} scope="job" action={jobPauseAction(dashboard)} />
      <NeedsAttentionCard dashboard={dashboard} />
      {/* The inbox addresses the job the DASHBOARD names, the same value the
          stream is opened against (DECISION F008 D3), never one re-read from
          the URL beside it. */}
      <DecisionInboxCard decisions={orderDecisionInbox(dashboard.decisionInbox)} tasks={dashboard.tasks} jobId={dashboard.jobId} serverToken={serverToken} onSelectNode={onSelectNode} />
      <ActivityFeedCard activity={dashboard.activity} recent={recent} recentDropped={recentDropped} tasks={dashboard.tasks} onSelectNode={onSelectNode} jobId={dashboard.jobId} serverToken={serverToken} stage={dashboard.live.stage} focusedTaskId={focusedTaskId} />
      <TaskChecklistCard tasks={dashboard.tasks} jobId={dashboard.jobId} serverToken={serverToken} onSelectNode={onSelectNode} finished={jobFinishedOf(dashboard.live.stage)} />
      {/* amend1015 P4.3: the eight buttons below are the only way to reach eight working panels,
          so they sit in one labelled group of legible chips rather than as faint loose text. */}
      <nav className={styles.moreGroup} aria-label="More panels" data-ui="more-panels">
      <span className={styles.moreLabel}>More</span>
      {/* The plan view's entry point (T5_F292 T001, DECISION F292 D2), first of the quiet buttons
          below the tasks card it reads beside; the shell owns whether the view is open. */}
      {onOpenPlan && (<button type="button" className={styles.advancedToggle} data-ui="plan-button" onClick={onOpenPlan}>Plan</button>)}
      {/* The learning overlay's entry point (T5_F265 T002, DECISION F265 D3), in the quiet style
          of the toggle below; the shell owns whether the overlay is open. */}
      {onOpenLessons && (
        <button type="button" className={styles.advancedToggle} onClick={onOpenLessons}>
          Lessons
        </button>
      )}
      {/* The guided tour's entry point (F036 T003, DECISION F036 D6), beside Lessons in the
          same quiet style; the shell owns whether the tour is open. */}
      {onOpenTour && (<button type="button" className={styles.advancedToggle} onClick={onOpenTour}>Tour</button>)}
      {/* The in-app story's entry point (F039 T002, DECISION F039 D6), beside Tour in the same
          quiet style; the shell owns whether the story is open. */}
      {onOpenStory && (<button type="button" className={styles.advancedToggle} onClick={onOpenStory}>Story</button>)}
      {/* The results panel's entry point (F041 T003, DECISION F041 D5), beside Story in the
          same quiet style; the shell owns whether the panel is open. */}
      {onOpenResults && (<button type="button" className={styles.advancedToggle} onClick={onOpenResults}>Results</button>)}
      {/* The missions panel's entry point (F305 T002, DECISION F305 D1), beside Results in the
          same quiet style; the shell owns whether the panel is open. */}
      {onOpenMissions && (<button type="button" className={styles.advancedToggle} data-ui="missions-button" onClick={onOpenMissions}>Missions</button>)}
      {/* The '?' panel's entry point (F043 T003, DECISION F043 D3), beside Results in the same
          quiet style; the shell owns whether the panel is open. */}
      {onOpenTerms && (<button type="button" className={styles.advancedToggle} data-ui="terms-button" onClick={onOpenTerms} aria-keyshortcuts="?">Terms</button>)}
      <button
        type="button"
        className={styles.advancedToggle}
        onClick={toggleAdvanced}
        aria-expanded={showAdvanced}
      >
        {showAdvanced ? "Hide system details" : "System details"}
      </button>
      </nav>
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
