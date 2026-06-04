import type { RemedyDashboard, RemedyGraphNode } from "../../api/types";
import { TaskDoneGlyph, TaskCurrentGlyph, TaskPlannedGlyph } from "../icons/RemedyGlyphs";
import styles from "./DetailPopover.module.css";

const STATE_LABELS: Record<string, string> = {
  done: "Completed",
  current: "In progress",
  planned: "Planned",
  blocked: "Blocked",
  pending: "Planned",
  suggested: "Suggested",
};

function StateIcon({ state }: { state: string }) {
  if (state === "done") return <TaskDoneGlyph style={{ width: 14, height: 14, color: "var(--remedy-green, #4cc681)" }} />;
  if (state === "current") return <TaskCurrentGlyph style={{ width: 14, height: 14, color: "var(--remedy-blue, #4c83ff)" }} />;
  if (state === "blocked") return <TaskPlannedGlyph style={{ width: 14, height: 14, color: "#e06050" }} />;
  return <TaskPlannedGlyph style={{ width: 14, height: 14, color: "var(--remedy-ink-soft, #6f82a8)" }} />;
}

function TestBadge({ status }: { status?: string }) {
  if (!status || status === "none") return null;
  const pass = status === "pass";
  return (
    <span className={pass ? styles.badgePass : styles.badgeFail}>
      {pass ? "Tests pass" : "Tests fail"}
    </span>
  );
}

function formatTime(iso?: string): string | null {
  if (!iso) return null;
  try {
    const d = new Date(iso);
    return d.toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  } catch { return null; }
}

export function DetailPopover({ dashboard, selectedNode, onClose }: { dashboard: RemedyDashboard; selectedNode: RemedyGraphNode; onClose: () => void }) {
  const task = dashboard.tasks.find(i => i.nodeId === selectedNode.nodeId);
  const title = task?.label || selectedNode.label || "Task";
  const state = task?.state || selectedNode.state;
  const stateLabel = STATE_LABELS[state] || state;

  const outcomeSummary = task?.outcomeSummary;
  const changedFiles = task?.changedFilesSafe;
  const changedCount = task?.changedFilesCount;
  const testStatus = task?.testStatus;
  const blockedReason = task?.blockedReason;
  const completedAt = formatTime(task?.completedAt);

  const isDone = state === "done";
  const isBlocked = state === "blocked";
  const isCurrent = state === "current";

  return (
    <aside className={`${styles.popover} remedy-detail-compact`} aria-label="Task details" data-ui="detail-popover">
      <button className={styles.close} type="button" aria-label="Close" onClick={onClose}>&times;</button>
      <h2 className={styles.title}>{title}</h2>

      <div className={styles.statusRow}>
        <StateIcon state={state} />
        <span className={styles.statusLabel}>{stateLabel}</span>
        {completedAt && <span className={styles.timeLabel}>{completedAt}</span>}
        <TestBadge status={testStatus} />
      </div>

      {/* Outcome */}
      <section className={styles.section}>
        <h3>Outcome</h3>
        <p>{outcomeSummary || (
          isDone ? "Completed successfully."
          : isCurrent ? "Work is in progress."
          : isBlocked ? "Blocked — needs attention."
          : "Not started yet."
        )}</p>
      </section>

      {/* Blocked reason */}
      {isBlocked && blockedReason && (
        <section className={styles.section}>
          <h3>Blocker</h3>
          <p className={styles.blockerText}>{blockedReason}</p>
        </section>
      )}

      {/* Produced / Changed */}
      {changedFiles && changedFiles.length > 0 ? (
        <section className={styles.section}>
          <h3>Changed files</h3>
          <ul className={styles.fileList}>
            {changedFiles.map(f => <li key={f}>{f}</li>)}
          </ul>
        </section>
      ) : changedCount != null && changedCount > 0 ? (
        <section className={styles.section}>
          <h3>Changed</h3>
          <p className={styles.detail}>{changedCount} file{changedCount !== 1 ? "s" : ""} modified</p>
        </section>
      ) : null}

      {/* Checked */}
      <section className={styles.section}>
        <h3>Checked</h3>
        <p>{testStatus === "pass" ? "Tests passing"
          : testStatus === "fail" ? "Tests failing — needs repair"
          : task?.checked ? "Verified"
          : "Not yet checked"}</p>
      </section>

      {/* Action */}
      <section className={styles.section}>
        <h3>Action needed</h3>
        <p>{isBlocked
          ? "Review blocker above."
          : isDone
          ? "No action needed."
          : isCurrent
          ? "Agent is working on this."
          : "Waiting to start."
        }</p>
      </section>
    </aside>
  );
}
