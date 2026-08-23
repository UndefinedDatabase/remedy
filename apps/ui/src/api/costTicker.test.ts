import { describe, it, expect } from "vitest";
import { metricsWithCostTicker } from "./costTicker";
import type { RemedyMetric } from "./types";

/** The bar's metrics as `normalizeDashboardPayload` builds them, trimmed to the
 *  two entries these cases need. */
function barMetrics(): RemedyMetric[] {
  return [
    { key: "tokens", label: "Tokens", value: "—", unknown: true },
    { key: "cost", label: "Cost", value: "—", unknown: true },
  ];
}

describe("metricsWithCostTicker", () => {
  it("fills the cost entry from the tick and clears its unknown flag", () => {
    const filled = metricsWithCostTicker(barMetrics(), {
      spent_usd: 3.4, limit_usd: 4, basis: { cost: "actual" },
    });
    const cost = filled.find((m) => m.key === "cost");
    expect(cost!.unknown).toBe(false);
    expect(cost!.cost!.display).toBe("$3.40");
    expect(cost!.cost!.level).toBe("warn");
    expect(cost!.cost!.estimated).toBe(false);
  });

  it("decides nothing itself — the view is whatever costMetricOf answered", () => {
    // A limitless payload: the unit, the marker and the missing band are all
    // costMetric.ts's rulings and this module must not second-guess any of them.
    const filled = metricsWithCostTicker(barMetrics(), { spent_tokens: 1500 });
    const cost = filled.find((m) => m.key === "cost");
    expect(cost!.cost!.limitless).toBe(true);
    expect(cost!.cost!.display).toBe("1.5k");
    expect(cost!.cost!.unit).toBe("tokens");
    expect(cost!.cost!.estimated).toBe(true);
  });

  it("a null tick returns the SAME array, so React sees no new identity", () => {
    const metrics = barMetrics();
    expect(metricsWithCostTicker(metrics, null)).toBe(metrics);
  });

  it("an array with no cost entry is returned by reference", () => {
    // The degraded dashboard: it could not load, so it has no stream figures
    // either and a tile there would be a promise it cannot keep.
    const degraded: RemedyMetric[] = [{ key: "open", label: "Open", value: 0 }];
    expect(metricsWithCostTicker(degraded, { spent_usd: 1 })).toBe(degraded);
  });

  it("no other entry is replaced, and none is mutated", () => {
    const metrics = barMetrics();
    const before = { ...metrics[0] };
    const filled = metricsWithCostTicker(metrics, { spent_usd: 1 });
    expect(filled).not.toBe(metrics);
    expect(filled[0]).toBe(metrics[0]);
    expect(metrics[0]).toEqual(before);
  });

  it("the input's own cost entry is left alone", () => {
    const metrics = barMetrics();
    metricsWithCostTicker(metrics, { spent_usd: 1 });
    expect(metrics[1].cost).toBeUndefined();
    expect(metrics[1].unknown).toBe(true);
  });
});
