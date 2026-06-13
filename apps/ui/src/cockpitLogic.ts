// Pure, CSS-free cockpit decision logic.
// Extracted from the panel components so it can be unit-tested under the
// node-environment vitest (which cannot import CSS modules / render React).
import type { RemedyDashboard, RemedyTaskItem } from "./api/types";

/** The LIVE pill is active ONLY when the backend reports a running job. */
export function liveIsActive(dashboard: RemedyDashboard): boolean {
  return dashboard.live.running === true;
}

export interface AgentStatus {
  status: string;
  detail: string;
  isRunning: boolean;
}

/** Truthful "Agent is doing now" status — never claims work without evidence. */
export function deriveAgentStatus(dashboard: RemedyDashboard): AgentStatus {
  const isRunning = dashboard.live.running === true;
  const lifecycle = dashboard.workerStatus?.lifecycle_state;

  if (isRunning) {
    return {
      status: "Working",
      detail: dashboard.live.activeTaskLabel || "Processing a task.",
      isRunning: true,
    };
  }
  if (lifecycle === "waiting_for_approval") {
    return { status: "Needs your decision", detail: "A patch is waiting for approval.", isRunning: false };
  }
  if (lifecycle === "blocked") {
    const reason = dashboard.workerStatus?.why_it_stopped?.replace(/_/g, " ") || "";
    return { status: "Blocked", detail: reason || "Cannot continue.", isRunning: false };
  }
  return { status: "Idle", detail: "No active work.", isRunning: false };
}

export interface ChecklistRows {
  rows: RemedyTaskItem[];
  completed: number;
  total: number;
}

/** Render rows are capped, but completed/total reflect ALL real tasks — the
 *  "x of y completed" count is never truncated by the render cap. */
export function selectChecklistRows(tasks: RemedyTaskItem[], cap = 16): ChecklistRows {
  const rows = tasks.slice(0, cap);
  return {
    rows,
    completed: tasks.filter(t => t.checked).length,
    total: tasks.length,
  };
}
