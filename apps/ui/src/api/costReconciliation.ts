// The single home for the TERMINAL half of the COST tile: which figure the bar
// shows once the job has stopped, and what the client is allowed to say about a
// difference between the figure it RECEIVED over the stream and the figure the
// ledger HOLDS. DECISION F022 D8 rules every clause below — the trigger, the
// figure shown, the labelled delta and the absent side — and this module
// decides nothing D8 does not rule.
//
// Remedy deliberately does not compute a difference, and deliberately does not
// read a figure field such as `spent_usd` at all: both sides are the same
// producer's counters, so a gap means frames were missed in transport rather
// than money drifting, and a magnitude would be a second arithmetic home for
// money (DECISION F022 D7's closing clause). The note NAMES two displays that
// `costMetricOf` already produced and subtracts nothing.
// `costReconciliation.test.ts` guards both absences over this file's source.
//
// This is not `costTicker.ts`. That module's contract is the LIVE tick while a
// job runs; the terminal rules live here so a reader searching for them finds
// one file rather than a second responsibility bolted onto the first.
import { costMetricOf } from "./costMetric";
import type { BudgetTickFigures, CostMetricView } from "./costMetric";
import type { RemedyMetric } from "./types";

/** The metrics bar's own key for the cost tile. */
const COST_KEY = "cost";

/** The already-composed note, or `undefined` when there is nothing to say.
 *
 *  DECISION F022 D8 clause 3: the comparison is between the two DISPLAY
 *  strings, never the raw payloads, because a difference below the display
 *  precision would render as a label naming two identical figures. Clause 4:
 *  an absent received side is absent, so no label is composed at all. */
function ledgerFinalNote(
  ledger: CostMetricView,
  received: CostMetricView | null,
): string | undefined {
  if (received === null) return undefined;
  if (received.display === ledger.display) return undefined;
  return `final (ledger): ${ledger.display} — live estimate was ${received.display}`;
}

/** The bar's metrics with the cost tile reconciled against the ledger.
 *
 *  Returns the array BY REFERENCE whenever there is nothing to say — the job is
 *  still running, no ledger figure exists, or the array carries no cost tile —
 *  so React sees no new identity, exactly as `metricsWithCostTicker` does for
 *  the live tick. Only the cost entry is ever replaced.
 *
 *  Every render decision on the returned tile is `costMetricOf`'s: the unit,
 *  the denominator, the estimate marker, the fill, the band and the tooltip are
 *  all DECISION F022 D4's rules, applied here to the LEDGER's payload. */
export function metricsWithCostReconciliation(
  metrics: readonly RemedyMetric[],
  ledger: BudgetTickFigures | null,
  received: BudgetTickFigures | null,
  running: boolean,
): RemedyMetric[] {
  // Clause 1: terminal AND a ledger figure. While the job runs, the ledger's
  // last tick and the client's last tick are the same event, so calling one
  // "final" would claim a finality the run has not earned.
  if (running) return metrics as RemedyMetric[];
  if (ledger === null) return metrics as RemedyMetric[];
  if (!metrics.some((metric) => metric.key === COST_KEY)) return metrics as RemedyMetric[];

  // Clause 2: the figure shown is the LEDGER's, rendered through the one module
  // that owns the unit, the denominator, the marker and the thresholds.
  const finalView = costMetricOf(ledger);
  const receivedView = received === null ? null : costMetricOf(received);
  const costFinalNote = ledgerFinalNote(finalView, receivedView);
  return metrics.map((metric) => (
    metric.key === COST_KEY
      ? { ...metric, cost: finalView, unknown: false, costFinalNote }
      : metric
  ));
}
