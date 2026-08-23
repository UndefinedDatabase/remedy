import { describe, it, expect } from "vitest";
import { metricsWithCostReconciliation } from "./costReconciliation";
import type { RemedyMetric } from "./types";

// The guard case at the bottom reads `costReconciliation.ts` off disk. There is
// no `@types/node` in this workspace, so the node built-ins arrive through a
// dynamic import whose specifier is a variable — the same shape
// `costMetric.test.ts` already uses for its own source scan.
const FS_MODULE = "node:fs";
const URL_MODULE = "node:url";
type FsModule = { readFileSync: (path: string, encoding: string) => string };
type UrlModule = { fileURLToPath: (url: URL) => string };

async function reconciliationSource(): Promise<string> {
  const fs = (await import(FS_MODULE)) as FsModule;
  const url = (await import(URL_MODULE)) as UrlModule;
  return fs.readFileSync(url.fileURLToPath(new URL("./costReconciliation.ts", import.meta.url)), "utf8");
}

/** Block and line comments removed, so the guard reads the CODE and not the
 *  prose about it (finding R-0584). */
function withoutComments(source: string): string {
  return source.replace(/\/\*[\s\S]*?\*\//g, " ").replace(/\/\/.*/g, " ");
}

/** The wire's own names for the figures a cost reading is derived from.
 *  Whoever names one is doing the arithmetic. */
const FIGURE_FIELDS = ["spent_usd", "spent_tokens", "limit_usd", "limit_tokens"];

/** The bar's metrics as `normalizeDashboardPayload` builds them, trimmed to the
 *  two entries these cases need. */
function barMetrics(): RemedyMetric[] {
  return [
    { key: "tokens", label: "Tokens", value: "—", unknown: true },
    { key: "cost", label: "Cost", value: "—", unknown: true },
  ];
}

/** The ledger's own last tick. */
const LEDGER_TICK = { spent_usd: 4.2, limit_usd: 8, basis: { cost: "actual" } };

describe("metricsWithCostReconciliation — DECISION F022 D8 clause 1, the trigger", () => {
  it("a RUNNING job gets the SAME array, so nothing claims finality mid-run", () => {
    const metrics = barMetrics();
    expect(metricsWithCostReconciliation(metrics, LEDGER_TICK, null, true)).toBe(metrics);
  });

  it("a null ledger figure gets the SAME array, so the live tile stands", () => {
    const metrics = barMetrics();
    expect(metricsWithCostReconciliation(metrics, null, LEDGER_TICK, false)).toBe(metrics);
  });

  it("an array with no cost entry is returned by reference", () => {
    const degraded: RemedyMetric[] = [{ key: "open", label: "Open", value: 0 }];
    expect(metricsWithCostReconciliation(degraded, LEDGER_TICK, null, false)).toBe(degraded);
  });
});

describe("metricsWithCostReconciliation — clause 2, the figure shown is the ledger's", () => {
  it("the ledger's view replaces the live one at terminal", () => {
    const live = { spent_usd: 3.4, limit_usd: 8, basis: { cost: "estimated" } };
    const reconciled = metricsWithCostReconciliation(barMetrics(), LEDGER_TICK, live, false);
    const cost = reconciled.find((m) => m.key === "cost");
    expect(cost!.cost!.display).toBe("$4.20");
    expect(cost!.cost!.estimated).toBe(false);
    expect(cost!.cost!.fill).toBe(0.525);
    expect(cost!.cost!.level).toBe("normal");
    expect(cost!.unknown).toBe(false);
  });

  it("no other entry is replaced, and none is mutated", () => {
    const metrics = barMetrics();
    const before = { ...metrics[0] };
    const reconciled = metricsWithCostReconciliation(metrics, LEDGER_TICK, null, false);
    expect(reconciled).not.toBe(metrics);
    expect(reconciled[0]).toBe(metrics[0]);
    expect(metrics[0]).toEqual(before);
  });
});

describe("metricsWithCostReconciliation — clause 3, the delta is named not computed", () => {
  it("names BOTH displays when they differ", () => {
    const live = { spent_usd: 3.4, limit_usd: 8, basis: { cost: "estimated" } };
    const reconciled = metricsWithCostReconciliation(barMetrics(), LEDGER_TICK, live, false);
    const cost = reconciled.find((m) => m.key === "cost");
    expect(cost!.costFinalNote).toBe("final (ledger): $4.20 — live estimate was $3.40");
  });

  it("says NOTHING when the two displays are equal", () => {
    // The same figure arriving twice is not a delta, and a label naming two
    // identical figures contradicts itself on the reader's screen.
    const live = { spent_usd: 4.2, limit_usd: 8, basis: { cost: "estimated" } };
    const reconciled = metricsWithCostReconciliation(barMetrics(), LEDGER_TICK, live, false);
    const cost = reconciled.find((m) => m.key === "cost");
    expect(cost!.costFinalNote).toBeUndefined();
    expect(cost!.cost!.display).toBe("$4.20");
  });
});

describe("metricsWithCostReconciliation — clause 4, an absent side is absent", () => {
  it("no received figure renders the ledger view with NO note", () => {
    const reconciled = metricsWithCostReconciliation(barMetrics(), LEDGER_TICK, null, false);
    const cost = reconciled.find((m) => m.key === "cost");
    expect(cost!.cost!.display).toBe("$4.20");
    expect(cost!.costFinalNote).toBeUndefined();
  });
});

describe("the reconciliation names no figure field and does no arithmetic", () => {
  it("the comment stripper actually removes something", async () => {
    const source = await reconciliationSource();
    const code = withoutComments(source);
    expect(source.length).toBeGreaterThan(0);
    expect(code.length).toBeLessThan(source.length);
    // The module's own prose names a figure field on purpose, so a guard
    // reading the unstripped source would go red on the next assertion.
    expect(source).toContain("spent_usd");
  });

  it("the code names no figure field", async () => {
    const code = withoutComments(await reconciliationSource());
    for (const field of FIGURE_FIELDS) {
      expect(code).not.toContain(field);
    }
  });

  it("the field scan can actually see a field, so its green is not vacuous", async () => {
    const salted = withoutComments("const leak = payload.spent_usd;\n" + await reconciliationSource());
    expect(salted).toContain("spent_usd");
  });

  it("the code subtracts, divides and multiplies nothing", async () => {
    const code = withoutComments(await reconciliationSource())
      .replace(/"[^"]*"/g, '""')
      .replace(/'[^']*'/g, "''");
    for (const operator of [" - ", " / ", " * "]) {
      expect(code).not.toContain(operator);
    }
  });

  it("the operator scan can actually see an operator", async () => {
    const salted = withoutComments("const gap = ledger - received;\n" + await reconciliationSource());
    expect(salted).toContain(" - ");
  });
});
