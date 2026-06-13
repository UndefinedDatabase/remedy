import type { RemedyDashboard, RemedyGraphNode, RemedyTaskItem } from "../../api/types";
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

const UNKNOWN = "Unknown";

function StateIcon({ state }: { state: string }) {
  if (state === "done") return <TaskDoneGlyph style={{ width: 14, height: 14, color: "var(--remedy-green, #4cc681)" }} />;
  if (state === "current") return <TaskCurrentGlyph style={{ width: 14, height: 14, color: "var(--remedy-blue, #4c83ff)" }} />;
  if (state === "blocked") return <TaskPlannedGlyph style={{ width: 14, height: 14, color: "#e06050" }} />;
  return <TaskPlannedGlyph style={{ width: 14, height: 14, color: "var(--remedy-ink-soft, #6f82a8)" }} />;
}

function formatTime(iso?: string): string | null {
  if (!iso) return null;
  try {
    const d = new Date(iso);
    return d.toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
  } catch { return null; }
}

// Per-task status fields. Every field falls back to "Unknown" when there is no
// evidence — never omitted, never invented. Apply/Proof come from authoritative
// backend truth (durable apply record + proof chain), not inferred from counts.
function applyStatus(task?: RemedyTaskItem): string {
  if (task?.applyStatus === "applied") return "Applied";
  if (task?.applyStatus === "reverted") return "Reverted";
  if (task?.applyStatus === "not_applied") return "Not applied";
  return UNKNOWN;
}
function testStatusLabel(task?: RemedyTaskItem): string {
  if (task?.testStatus === "pass") return "Passing";
  if (task?.testStatus === "fail") return "Failing";
  return UNKNOWN;
}
function proofStatusLabel(task?: RemedyTaskItem): string {
  if (task?.proofStatus === "verified") return "Verified";
  if (task?.proofStatus === "failed") return "Failed";
  return UNKNOWN;
}

function Field({ label, value }: { label: string; value: string }) {
  const unknown = value === UNKNOWN;
  return (
    <div className={styles.fieldRow}>
      <span className={styles.fieldKey}>{label}</span>
      <span className={unknown ? styles.fieldUnknown : styles.fieldVal}>{value}</span>
    </div>
  );
}

export function DetailPopover({ dashboard, selectedNode, onClose }: { dashboard: RemedyDashboard; selectedNode: RemedyGraphNode; onClose: () => void }) {
  const task = dashboard.tasks.find(i => i.nodeId === selectedNode.nodeId);
  const title = task?.label || selectedNode.label || "Task";
  const state = task?.state || selectedNode.state;
  const stateLabel = STATE_LABELS[state] || state;

  const outcomeSummary = task?.outcomeSummary;
  const changedFiles = task?.changedFilesSafe;
  const changedCount = task?.changedFilesCount;
  const blockedReason = task?.blockedReason;
  const completedAt = formatTime(task?.completedAt);

  const isDone = state === "done";
  const isBlocked = state === "blocked";
  const isCurrent = state === "current";

  const filesValue = changedCount != null
    ? `${changedCount} file${changedCount !== 1 ? "s" : ""}`
    : UNKNOWN;

  return (
    <aside className={`${styles.popover} remedy-detail-compact`} aria-label="Task details" data-ui="detail-popover">
      <button className={styles.close} type="button" aria-label="Close" onClick={onClose}>&times;</button>
      <h2 className={styles.title}>{title}</h2>

      <div className={styles.statusRow}>
        <StateIcon state={state} />
        <span className={styles.statusLabel}>{stateLabel}</span>
        {completedAt && <span className={styles.timeLabel}>{completedAt}</span>}
      </div>

      {/* Result (Ergebnis) */}
      <section className={styles.section}>
        <h3>Result</h3>
        <p>{outcomeSummary || (
          isDone ? "Completed, but no detailed outcome was recorded."
          : isCurrent ? "Work is in progress."
          : isBlocked ? "Blocked — needs attention."
          : "Not started yet."
        )}</p>
      </section>

      {/* Blocker */}
      {isBlocked && blockedReason && (
        <section className={styles.section}>
          <h3>Blocker</h3>
          <p className={styles.blockerText}>{blockedReason}</p>
        </section>
      )}

      {/* Changed files (safe names only) */}
      {changedFiles && changedFiles.length > 0 && (
        <section className={styles.section}>
          <h3>Changed files</h3>
          <ul className={styles.fileList}>
            {changedFiles.map(f => <li key={f}>{f}</li>)}
          </ul>
        </section>
      )}

      {/* Verification status — every field unknown-safe */}
      <section className={styles.section}>
        <h3>Verification</h3>
        <div className={styles.fields}>
          <Field label="Files changed" value={filesValue} />
          <Field label="Apply" value={applyStatus(task)} />
          <Field label="Test" value={testStatusLabel(task)} />
          <Field label="Proof" value={proofStatusLabel(task)} />
          <Field label="Snapshot" value={UNKNOWN} />
          <Field label="Reviewer" value={UNKNOWN} />
          <Field label="Artifacts" value={UNKNOWN} />
        </div>
      </section>
    </aside>
  );
}
