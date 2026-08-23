// The seam that carries the live budget tick into the metrics bar. DECISION
// F022 D6 rules that the shell composes the bar's metrics through ONE pure
// function, so the wiring is testable under the node-environment vitest that
// cannot render React — the same reason `cockpitLogic.ts` and `brainStream.ts`
// were extracted from their components.
//
// Remedy deliberately decides nothing about the money here: the unit, the
// denominator, the estimate marker, the thresholds and the tooltip lines are
// all DECISION F022 D4's and they live in `costMetric.ts`. This module calls
// `costMetricOf` and composes an array.
import { costMetricOf } from "./costMetric";
import type { BudgetTickFigures } from "./costMetric";
import type { RemedyMetric } from "./types";

/** The metrics bar's own key for the cost tile. */
const COST_KEY = "cost";

/** The bar's metrics with the cost tile filled from the latest tick.
 *
 *  Returns a NEW array only when there is something new to say: a null tick,
 *  or a metrics array carrying no cost entry, is returned BY REFERENCE so
 *  React sees no new identity and the degraded dashboard stays untouched.
 *  Only the cost entry is ever replaced; no other entry is mutated or copied. */
export function metricsWithCostTicker(
  metrics: readonly RemedyMetric[],
  figures: BudgetTickFigures | null,
): RemedyMetric[] {
  if (figures === null) return metrics as RemedyMetric[];
  if (!metrics.some((metric) => metric.key === COST_KEY)) return metrics as RemedyMetric[];
  return metrics.map((metric) => (
    metric.key === COST_KEY
      ? { ...metric, cost: costMetricOf(figures), unknown: false }
      : metric
  ));
}
