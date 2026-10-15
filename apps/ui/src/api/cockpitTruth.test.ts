// amend1015: the cockpit's tiles and task rows read the server's truth, one way.
import { describe, expect, it } from "vitest";
import { costMetricsOf, tokensMetricOf } from "./cockpitTruth";

const ledger = (over: Record<string, unknown> = {}) => ({
  roles: [
    { role: "builder", harness_invocations: 2, tokens_in: 1200, tokens_out: 300 },
    { role: "reviewer", harness_invocations: 2, tokens_in: null, tokens_out: null },
  ],
  harness_invocations: 4, model_turns: null, tokens_in: 1200, tokens_out: 300,
  line: "builder: 2 harness invocations, 1.2k in / 300 out", ...over,
});

describe("tokensMetricOf (amend1015 P1.5)", () => {
  it("shows the ledger's tokens in plus out", () => {
    const m = tokensMetricOf({ known: false, ledger: ledger() });
    expect(m.value).toBe(1500);
    expect(m.unknown).toBe(false);
    expect(m.tooltip).toEqual({ builder: 1500 });
    expect(m.estimated).toBe(false);
  });

  it("falls back to the harness invocations when no call reported tokens", () => {
    const m = tokensMetricOf({ known: false, ledger: ledger({ tokens_in: null, tokens_out: null }) });
    expect(m.value).toBe(4);
    expect(m.suffix).toBe(" invocations");
    expect(m.unknown).toBe(false);
  });

  it("is an honest em dash only when the run made no call", () => {
    const m = tokensMetricOf({ known: false, ledger: ledger({ harness_invocations: 0, tokens_in: null, tokens_out: null, roles: [] }) });
    expect(m.value).toBe("—");
    expect(m.unknown).toBe(true);
  });

  it("keeps the event estimate for a job the ledger never saw", () => {
    const m = tokensMetricOf({ known: true, total_tokens: 900, by_role: { memory: 900 } });
    expect(m.value).toBe(900);
    expect(m.tooltip).toEqual({ memory: 900 });
  });
});

describe("costMetricsOf (amend1015 P5.1)", () => {
  it("has no cost tile unless the project asked for dollars", () => {
    expect(costMetricsOf({ show_cost_usd: false })).toEqual([]);
    expect(costMetricsOf(undefined)).toEqual([]);
  });

  it("keeps the cost tile when the project asked for dollars", () => {
    expect(costMetricsOf({ show_cost_usd: true })).toEqual([{ key: "cost", label: "Cost", value: "—", unknown: true }]);
  });
});
