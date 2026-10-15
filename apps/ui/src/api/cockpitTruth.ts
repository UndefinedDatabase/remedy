// amend1015: how the cockpit's tiles and task rows read the server's truth, in ONE place.
// Before it, the TOKENS tile read only event estimates (so a run the terminal measured
// showed "—"), and a task row was drawn done but counted not done. `remedyApi.ts` calls
// these and decides nothing about them itself.
import type { RemedyMetric } from "./types";

const EM_DASH = "—" as const;

// Any value read as a plain object; anything else reads as the empty payload.
function objectOf(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value) ? (value as Record<string, unknown>) : {};
}

function numberOf(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) && value >= 0 ? value : null;
}

/** The TOKENS tile (amend1015 P1.5): the ledger's tokens in plus out — the reading `remedy do`
 *  prints — else its harness invocations, else the older event estimate, else an em dash.
 *  A run that made at least one call never reads "—". */
export function tokensMetricOf(tokenUsage: unknown): RemedyMetric {
  const tu = objectOf(tokenUsage);
  const ledger = objectOf(tu.ledger);
  const tokensIn = numberOf(ledger.tokens_in);
  const tokensOut = numberOf(ledger.tokens_out);
  const base = { key: "tokens", label: "Tokens" } as const;
  if (tokensIn !== null || tokensOut !== null) {
    const tooltip: Record<string, number> = {};
    for (const role of Array.isArray(ledger.roles) ? ledger.roles : []) {
      const r = objectOf(role);
      const sum = (numberOf(r.tokens_in) ?? 0) + (numberOf(r.tokens_out) ?? 0);
      if (sum > 0) tooltip[String(r.role || "other")] = sum;
    }
    return { ...base, value: (tokensIn ?? 0) + (tokensOut ?? 0), tooltip, unknown: false };
  }
  const invocations = numberOf(ledger.harness_invocations) ?? 0;
  if (invocations > 0) return { ...base, value: invocations, suffix: " invocations", unknown: false };
  const estimate = tu.known ? numberOf(tu.total_tokens) ?? 0 : 0;
  if (estimate > 0) {
    const roles = objectOf(tu.by_role) as Record<string, number>;
    const byRole = Object.keys(roles).length > 0 ? roles : undefined;
    return { ...base, value: estimate, tooltip: byRole, unknown: false };
  }
  return { ...base, value: EM_DASH, unknown: true };
}

/** The COST tile (amend1015 P5.1, DECISION amend1015 D8): present only when the project set
 *  `show_cost_usd = true` under `[cockpit]` in `.remedy/config.toml`. It is `unknown` at load
 *  because no budget tick has arrived yet — the honest em dash, never a fake zero;
 *  `metricsWithCostTicker` fills it from the live stream (DECISION F022 D6). */
export function costMetricsOf(tokenUsage: unknown): RemedyMetric[] {
  return objectOf(tokenUsage).show_cost_usd === true ? [{ key: "cost", label: "Cost", value: EM_DASH, unknown: true }] : [];
}

/** The job states that END a job (packages/core/models.py RunState, plus the dashboard's own
 *  `done`/`finalized`). A paused or blocked job is not finished: it waits for someone. */
const FINISHED_JOB_STAGES = new Set(["completed", "failed", "cancelled", "stopped", "done", "finalized"]);

/** True when the dashboard's `live.state` names a job that has ended (amend1015 P2.2). */
export function jobFinishedOf(stage: string | undefined | null): boolean {
  return FINISHED_JOB_STAGES.has(String(stage || "").toLowerCase());
}

/** A task row's check mark, the same fact the row's icon and the "x of y completed" count read
 *  (amend1015 P3.1). `verified ?? accepted ?? done` never reached the state when the server
 *  sent `verified: false`, so a row drawn done was counted not done. */
export function taskCheckedOf(raw: { verified?: unknown; accepted?: unknown }, state: string): boolean {
  return state === "done" || Boolean(raw.verified) || Boolean(raw.accepted);
}

/** What "+ Add Task" says on a job that has ended: the server would refuse the task with 409. */
export const ADD_TASK_FINISHED_HINT = "This job has already finished.";
