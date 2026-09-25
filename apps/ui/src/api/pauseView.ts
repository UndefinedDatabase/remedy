// THE PAUSE VIEW (DECISION F025 D4): pure functions of a `RemedyDashboard`
// that decide what the pause banner, the NowCard and the pause/resume controls
// show. Nothing here reaches a clock, a socket or a nonce — every answer is a
// function of the dashboard alone, so every case is a value a test can build
// without a fetch, a timer or a DOM.
import type { RemedyDashboard, RemedyState } from "./types";

/** The two sources DECISION F025 D2's own `--source` default and the door's
 *  `COMMAND_EFFECT_SOURCE` produce — mirrored here as `PAUSE_OWNER_SOURCES` and
 *  pinned to both Python originals by
 *  `tests/ui_contracts/test_pause_controls_contract.py`, the same mirror rule
 *  `steeringSend.ts`'s constants follow. */
export const PAUSE_OWNER_SOURCES: readonly string[] = ["cli", "ui"];

/** The job is PARKED exactly when its pause record is non-empty — the shape
 *  `RemedyPause.record` normalizes to `{}` for every other state. */
function jobIsParked(dashboard: RemedyDashboard): boolean {
  return Object.keys(dashboard.pause.record).length > 0;
}

/** "By you": the record's own `source` is one this browser or the CLI wrote,
 *  never a third party or a value this browser cannot name. */
function pausedByYou(dashboard: RemedyDashboard): boolean {
  const source = dashboard.pause.record.source;
  return typeof source === "string" && PAUSE_OWNER_SOURCES.includes(source);
}

/** What the graph's chrome shows about the job's pause state, or `null` when
 *  there is nothing to say. FIRST MATCH WINS, in the order a control-root
 *  error, a parked job, a pending request, then paused tasks — an error hides
 *  every other reading because none of them can be trusted once the control
 *  root itself could not be read. */
export interface PauseBanner {
  badge: string;
  text: string;
  command: string;
  tone: "warn";
}

const PARKED_COMMAND_PREFIX = "remedy job run ";

export function pauseBanner(dashboard: RemedyDashboard): PauseBanner | null {
  const { pause } = dashboard;
  if (pause.error !== "") {
    return {
      badge: "PAUSE",
      text: `The pause state could not be read: ${pause.error}`,
      command: "",
      tone: "warn",
    };
  }
  if (jobIsParked(dashboard)) {
    return {
      badge: "PAUSED",
      text: pausedByYou(dashboard)
        ? "Paused by you. Nothing runs until you resume it."
        : "Paused. Nothing runs until it is resumed.",
      command: `${PARKED_COMMAND_PREFIX}${dashboard.jobId}`,
      tone: "warn",
    };
  }
  if (pause.requested) {
    return {
      badge: "PAUSING",
      text: "Pause requested. The job stops before its next step.",
      command: "",
      tone: "warn",
    };
  }
  const pausedCount = pause.pausedTaskIds.length;
  if (pausedCount > 0) {
    return {
      badge: "PAUSED",
      text: pausedCount === 1
        ? "1 task is paused by you. The rest of the job keeps going."
        : `${pausedCount} tasks are paused by you. The rest of the job keeps going.`,
      command: "",
      tone: "warn",
    };
  }
  return null;
}

/** What the NowCard shows in place of `deriveAgentStatus`'s status and detail,
 *  or `null` when the ordinary status still applies. A parked job always
 *  answers, whatever `live.running` reads: a parked job never runs. */
export interface NowCardPause {
  status: "Paused";
  detail: string;
}

export function nowCardPause(dashboard: RemedyDashboard): NowCardPause | null {
  if (jobIsParked(dashboard)) {
    return { status: "Paused", detail: pausedByYou(dashboard) ? "Paused by you" : "Paused" };
  }
  if (!dashboard.live.running && dashboard.pause.pausedTaskIds.length > 0) {
    return { status: "Paused", detail: "Paused by you" };
  }
  return null;
}

/** The one action a pause/resume control offers, or `null` for no control at
 *  all — `PauseControl.tsx` renders nothing for `null`. */
export type PauseAction = "pause" | "resume" | "take_back";

/** The job's own action: resume a parked job, take back a pending request, or
 *  pause a running one — in that order, because a parked job is never
 *  running and a pending request pre-empts the plain pause offer. */
export function jobPauseAction(dashboard: RemedyDashboard): PauseAction | null {
  if (jobIsParked(dashboard)) {
    return "resume";
  }
  if (dashboard.pause.requested) {
    return "take_back";
  }
  if (dashboard.live.running) {
    return "pause";
  }
  return null;
}

/** One task's own action: resume it while it is paused, else offer to pause it
 *  only while it is `pending` — a task that is already `current` or `blocked`
 *  has started (or been dispatched) and DECISION F025 D1 makes a task pause a
 *  mask over PENDING tasks only, so pausing it now would tell the operator
 *  something untrue (R-1053); `done` and `suggested` likewise offer nothing,
 *  a done task having nothing left to withhold and a suggested one not yet
 *  part of the plan. */
export function taskPauseAction(
  dashboard: RemedyDashboard,
  taskId: string,
  taskState: RemedyState,
): PauseAction | null {
  if (dashboard.pause.pausedTaskIds.includes(taskId)) {
    return "resume";
  }
  if (taskState === "pending") {
    return "pause";
  }
  return null;
}

/** Every action's label, by SCOPE: the job's own resume reads "Resume", a
 *  task's reads "Resume task", because the two controls sit far enough apart
 *  on the page that the shorter job label never needs to say which thing it
 *  resumes. */
export function pauseActionLabel(scope: "job" | "task", action: PauseAction): string {
  if (action === "take_back") {
    return "Take back pause";
  }
  if (action === "resume") {
    return scope === "job" ? "Resume" : "Resume task";
  }
  return scope === "job" ? "Pause job" : "Pause task";
}
