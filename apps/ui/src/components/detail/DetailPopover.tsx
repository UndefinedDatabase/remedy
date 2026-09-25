import type { RemedyDashboard, RemedyGraphNode, RemedyTaskItem } from "../../api/types";
import { taskPauseAction } from "../../api/pauseView";
import { specVersionRows, taskEditAction, taskSpecOf, versionChipLabel } from "../../api/taskSpecView";
import { TaskDoneGlyph, TaskCurrentGlyph, TaskPlannedGlyph } from "../icons/RemedyGlyphs";
import { PromptTracePanel } from "../prompt/PromptTracePanel";
import { PauseControl } from "../panels/PauseControl";
import { TaskVersionList } from "./TaskVersionList";
import { TaskEditForm } from "./TaskEditForm";
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
// A task whose changes DISAGREE is a real state that hunk-level approval makes
// normal, so it gets a label of its own: rendering it as "Applied" or falling
// through to "Unknown" would both tell the operator something untrue.
function applyStatus(task?: RemedyTaskItem): string {
  if (task?.applyStatus === "applied") return "Applied";
  if (task?.applyStatus === "reverted") return "Reverted";
  if (task?.applyStatus === "not_applied") return "Not applied";
  if (task?.applyStatus === "partial") return "Partially applied";
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

// `onOpenDiff` is OPTIONAL because this popover predates the viewer by many
// features and is mounted from more than one place. A caller that passes no
// handler keeps exactly the popover it had, and the entry point below is simply
// absent — never a dead control that answers a click with nothing. `serverToken`
// (DECISION F025 D4) is OPTIONAL for the same reason: the pause/resume control
// it gates needs a credential this popover otherwise never carries.
export function DetailPopover({ dashboard, selectedNode, selectedPromptId, onClose, onOpenDiff, serverToken }: { dashboard: RemedyDashboard; selectedNode: RemedyGraphNode; selectedPromptId?: string | null; onClose: () => void; onOpenDiff?: (taskId: string) => void; serverToken?: string }) {
  const task = dashboard.tasks.find(i => i.nodeId === selectedNode.nodeId);
  // Prompt-trace items for the selected task (prompt item taskId === task id).
  const prompts = task
    ? (dashboard.promptTrace?.items ?? []).filter(p => p.taskId === task.id)
    : [];
  // DECISION F026 D3 clause 2 — the task's spec and version chain, read
  // through the pure view so the popover decides nothing about them itself.
  const spec = taskSpecOf(dashboard, task?.id ?? "");
  const chipLabel = versionChipLabel(spec);
  // DECISION F026 D4 clause 1 — the edit affordance's own eligibility,
  // computed once and gated on below; `task` is undefined for a node this
  // popover otherwise renders fine (a node never mapped to a task item), so
  // the read only runs once a task is known to exist.
  const editAction = task ? taskEditAction(dashboard, task.id) : null;
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
        {chipLabel && (
          <span className={styles.versionChip} title="Edited at runtime">{chipLabel}</span>
        )}
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

      {/* Prompt trace — compact, redacted-only evidence */}
      <PromptTracePanel prompts={prompts} selectedPromptId={selectedPromptId} />

      {/* DECISION F026 D3 clause 3 — the Versions list, one row per spec
          version, each opening the fields that changed. Renders nothing for
          a task never edited at runtime (`specVersionRows` returns `[]`). */}
      <TaskVersionList key={task?.id ?? ""} rows={specVersionRows(spec)} />

      {/* DECISION F026 D4 clauses 1 and 2 — the "Edit task" affordance,
          offered only for a waiting, paused or failed task of an approved
          plan (`taskEditAction`'s own reading), and only once this popover
          already holds the credential the send spends. */}
      {task && serverToken && editAction && (
        <TaskEditForm
          key={task.id}
          target={{ jobId: dashboard.jobId, serverToken }}
          jobId={dashboard.jobId}
          action={editAction}
        />
      )}

      {/* THE TASK'S PAUSE/RESUME CONTROL (DECISION F025 D4), gated on the
          credential `serverToken` carries — the popover renders nothing here
          when no caller passes one, the same absence `onOpenDiff` below
          practices. */}
      {task && serverToken && (
        <PauseControl
          key={task.id}
          target={{ jobId: dashboard.jobId, serverToken }}
          scope={task.id}
          action={taskPauseAction(dashboard, task.id, task.state)}
        />
      )}

      {/* THE DIFF VIEWER'S ENTRY POINT, at POPOVER LEVEL rather than inside the
          "Changed files" section. That placement is the repair of finding
          `R-0726` and not a preference: the section renders only when
          `changedFilesSafe` is a non-empty list, and
          `packages/orchestration/ui_server.py` builds that list from
          `patch_intent_applied` EVENTS, while the diff this button opens is a
          separate artifact under the job's evidence directory. The two genuinely
          diverge, so a task run that HAS a diff and no safe file list offered no
          way into the viewer at all — the feature's only door held shut by a
          condition about something else.
          `docs/ui/design_reference/component_spec.md:108` also lists the
          popover's buttons as a PEER of its sections rather than inside one, so
          this is where the design reference put it in the first place.
          A real button and not a div, for the reason the hunk head in
          `DiffView.tsx` is one: a div carries no keyboard affordance, and the
          explicit type stops it submitting a form it may one day sit in. It
          passes the TASK id — what the server's task-run route keys on — rather
          than the graph node id, and it wears no class because this round may not
          touch the stylesheet. */}
      {task && onOpenDiff && (
        <button type="button" onClick={() => onOpenDiff(task.id)}>
          Open diff
        </button>
      )}
    </aside>
  );
}
