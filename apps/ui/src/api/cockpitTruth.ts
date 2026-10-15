// amend1015: how the cockpit's tiles and task rows read the server's truth, in ONE place.
// Before it, the TOKENS tile read only event estimates (so a run the terminal measured
// showed "—"), and a task row was drawn done but counted not done. `remedyApi.ts` calls
// these and decides nothing about them itself.
import type { RemedyMetric } from "./types";

const EM_DASH = "—" as const;

function numberOf(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) && value >= 0 ? value : null;
}

/** The TOKENS tile (amend1015 P1.5): the ledger's tokens in plus out — the reading `remedy do`
 *  prints — else its harness invocations, else the older event estimate, else an em dash.
 *  A run that made at least one call never reads "—". */
export function tokensMetricOf(tokenUsage: any): RemedyMetric {
  const tu = tokenUsage || {};
  const ledger = tu.ledger || {};
  const tokensIn = numberOf(ledger.tokens_in);
  const tokensOut = numberOf(ledger.tokens_out);
  const base = { key: "tokens", label: "Tokens" } as const;
  if (tokensIn !== null || tokensOut !== null) {
    const tooltip: Record<string, number> = {};
    for (const role of Array.isArray(ledger.roles) ? ledger.roles : []) {
      const sum = (numberOf(role?.tokens_in) ?? 0) + (numberOf(role?.tokens_out) ?? 0);
      if (sum > 0) tooltip[String(role.role || "other")] = sum;
    }
    return { ...base, value: (tokensIn ?? 0) + (tokensOut ?? 0), tooltip, unknown: false };
  }
  const invocations = numberOf(ledger.harness_invocations) ?? 0;
  if (invocations > 0) return { ...base, value: invocations, suffix: " invocations", unknown: false };
  const estimate = tu.known ? numberOf(tu.total_tokens) ?? 0 : 0;
  if (estimate > 0) {
    const byRole = tu.by_role && Object.keys(tu.by_role).length > 0 ? tu.by_role : undefined;
    return { ...base, value: estimate, tooltip: byRole, unknown: false };
  }
  return { ...base, value: EM_DASH, unknown: true };
}

/** The COST tile (amend1015 P5.1, DECISION amend1015 D8): present only when the project set
 *  `show_cost_usd = true` under `[cockpit]` in `.remedy/config.toml`. It is `unknown` at load
 *  because no budget tick has arrived yet — the honest em dash, never a fake zero;
 *  `metricsWithCostTicker` fills it from the live stream (DECISION F022 D6). */
export function costMetricsOf(tokenUsage: any): RemedyMetric[] {
  return tokenUsage?.show_cost_usd === true ? [{ key: "cost", label: "Cost", value: EM_DASH, unknown: true }] : [];
}
