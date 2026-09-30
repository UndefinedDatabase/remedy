// T5_F044 T001, DECISION F044 D3 — whether the palette can offer a command right now. The rule
// is FIRST REASON WINS, in DECISION F044 D3 (2)'s own order: no write token, then a form entry
// the palette cannot yet ask the arguments of, then an ended job, then the command's own state —
// a pause only while the job's action is to pause, a resume only while it is parked or a pause is
// on its way, and the decision's answer only while a decision is open. Every other listed command
// (every "send" and "surface" entry besides `job.pause`, `job.unpause` and `decision.resolve`) is
// available whenever the first three checks pass, because their own refusal is the door's alone.
import type { PauseAction } from "./pauseView";
import { jobPauseAction } from "./pauseView";
import { steeringIsOpen } from "./steeringSend";
import type { RemedyDashboard } from "./types";
import type { PaletteCommand } from "./paletteCommands";
import { PALETTE_COMMANDS } from "./paletteCommands";

export const PALETTE_NO_TOKEN_REASON = "This page has no write token, so it cannot send commands.";
export const PALETTE_ENDED_REASON = "This job has ended, so it takes no more commands.";
export const PALETTE_FORM_REASON = "The palette cannot ask for this command's arguments yet.";
export const PALETTE_NOT_RUNNING_REASON = "The job is not running, so there is nothing to pause.";
export const PALETTE_ALREADY_PAUSED_REASON = "The job is already paused.";
export const PALETTE_PAUSE_PENDING_REASON = "A pause is already on its way.";
export const PALETTE_NOT_PAUSED_REASON = "The job is not paused.";
export const PALETTE_NO_DECISION_REASON = "No decision is waiting for an answer.";

/** What the palette needs to know about the job to judge every command's own state. */
export interface PaletteCommandFacts {
  readonly hasToken: boolean;
  readonly ended: boolean;
  readonly pauseAction: PauseAction | null;
  readonly openDecisions: number;
}

/** The facts of one dashboard, read once and shared across every command's own check. */
export function paletteCommandFactsOf(dashboard: RemedyDashboard, serverToken: string): PaletteCommandFacts {
  return {
    hasToken: serverToken !== "",
    ended: !steeringIsOpen(dashboard.live.stage),
    pauseAction: jobPauseAction(dashboard),
    openDecisions: dashboard.decisionInbox.length,
  };
}

/** THE FIRST-REASON-WINS RULE (DECISION F044 D3 (2)). "" means the command is available. */
export function paletteCommandReason(entry: PaletteCommand, facts: PaletteCommandFacts): string {
  if (!facts.hasToken) return PALETTE_NO_TOKEN_REASON;
  if (entry.flow === "form") return PALETTE_FORM_REASON;
  if (facts.ended) return PALETTE_ENDED_REASON;
  if (entry.command === "job.pause") {
    if (facts.pauseAction === "pause") return "";
    if (facts.pauseAction === "resume") return PALETTE_ALREADY_PAUSED_REASON;
    if (facts.pauseAction === "take_back") return PALETTE_PAUSE_PENDING_REASON;
    return PALETTE_NOT_RUNNING_REASON;
  }
  if (entry.command === "job.unpause") {
    return facts.pauseAction === "resume" || facts.pauseAction === "take_back" ? "" : PALETTE_NOT_PAUSED_REASON;
  }
  if (entry.command === "decision.resolve") {
    return facts.openDecisions > 0 ? "" : PALETTE_NO_DECISION_REASON;
  }
  return "";
}

/** Every refused command's reason, by command id — the shape `paletteSheet.ts`'s rows read an
 *  OWN key of, never an enumerable one it might inherit. */
export function paletteCommandReasons(facts: PaletteCommandFacts): Readonly<Record<string, string>> {
  const reasons: Record<string, string> = {};
  for (const entry of PALETTE_COMMANDS) {
    const reason = paletteCommandReason(entry, facts);
    if (reason !== "") reasons[entry.command] = reason;
  }
  return reasons;
}
