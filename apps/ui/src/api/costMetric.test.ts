import { describe, it, expect } from "vitest";
import { costMetricOf, formatTokenCount, formatUsd } from "./costMetric";

// The guard case at the bottom reads `costMetric.ts` off disk. There is no
// `@types/node` in this workspace, so the node built-ins arrive through a
// dynamic import whose specifier is a variable — the shape `tsc` types as
// `any` and vitest still resolves at run time.
const FS_MODULE = "node:fs";
const URL_MODULE = "node:url";
type FsModule = { readFileSync: (path: string, encoding: string) => string };
type UrlModule = { fileURLToPath: (url: URL) => string };

async function costMetricSource(): Promise<string> {
  const fs = (await import(FS_MODULE)) as FsModule;
  const url = (await import(URL_MODULE)) as UrlModule;
  return fs.readFileSync(url.fileURLToPath(new URL("./costMetric.ts", import.meta.url)), "utf8");
}

/** Block and line comments removed, so the guard reads the CODE and not the
 *  prose about it: a token a comment merely mentions is not a token the code
 *  uses. */
function withoutComments(source: string): string {
  return source.replace(/\/\*[\s\S]*?\*\//g, " ").replace(/\/\/.*/g, " ");
}

describe("U1 both limits configured", () => {
  const view = costMetricOf({
    spent_usd: 1.5, limit_usd: 2, spent_tokens: 1200, limit_tokens: 4000,
    basis: { cost: "actual", tokens: "actual" }, unmeasured_calls: 0,
  });

  it("shows usd and divides by the usd limit", () => {
    expect(view.unit).toBe("usd");
    expect(view.display).toBe("$1.50");
    expect(view.fill).toBe(0.75);
    expect(view.level).toBe("normal");
    expect(view.limitless).toBe(false);
  });

  it("enumerates BOTH limits with their own fills, usd line first", () => {
    // The token line is the discriminator: without it this case would also pass
    // for a module that dropped the enumeration and kept only the shown unit.
    expect(view.tooltip[0]).toBe("Cost $1.50 of $2.00 (75%)");
    expect(view.tooltip).toContain("Tokens 1.2k of 4.0k (30%)");
    expect(view.tooltip.indexOf("Tokens 1.2k of 4.0k (30%)")).toBeGreaterThan(0);
  });
});

describe("U2 only a token limit", () => {
  function tokenView(spentTokens: number) {
    return costMetricOf({ spent_tokens: spentTokens, limit_tokens: 1000, spent_usd: 9.5 });
  }

  it("takes the unit and the denominator from the token limit", () => {
    // `spent_usd` is present and has no limit, so a module that preferred the
    // usd FIGURE rather than the usd PAIR would show the wrong unit here.
    expect(tokenView(849).unit).toBe("tokens");
    expect(tokenView(849).display).toBe("849");
    expect(tokenView(849).fill).toBe(0.849);
  });

  it("pins all three levels and both boundaries", () => {
    expect(tokenView(849).level).toBe("normal");
    expect(tokenView(850).level).toBe("warn");
    expect(tokenView(850).fill).toBe(0.85);
    expect(tokenView(1000).level).toBe("exceeded");
    expect(tokenView(1000).fill).toBe(1);
    expect(tokenView(2500).level).toBe("exceeded");
  });
});

describe("U3 limitless, in both its shapes", () => {
  const noLimitAtAll = costMetricOf({ spent_usd: 4.25 });
  const wrongUnitLimit = costMetricOf({ spent_usd: 4.25, limit_tokens: 5000 });

  it("spend with no limit renders the spent-only variant", () => {
    for (const view of [noLimitAtAll, wrongUnitLimit]) {
      expect(view.fill).toBeNull();
      expect(view.level).toBeNull();
      expect(view.limitless).toBe(true);
      expect(view.display).toBe("$4.25");
    }
  });

  it("never borrows the other unit's limit as a denominator", () => {
    // Asserted over the SERIALISED view rather than the fields alone: the
    // criterion is that no fake denominator is RENDERED, and a stray tooltip
    // line is a rendered denominator.
    const serialised = JSON.stringify(wrongUnitLimit);
    expect(serialised).not.toContain("5000");
    expect(serialised).not.toContain("5.0k");
    expect(serialised).not.toContain(" of ");
    expect(serialised).not.toContain("%");
    expect(JSON.stringify(noLimitAtAll)).not.toContain(" of ");
  });
});

describe("U4 the basis drives the marker, per shown unit", () => {
  function usdView(basis: unknown) {
    return costMetricOf({ spent_usd: 1, limit_usd: 4, basis });
  }

  it("only an actual basis of the shown unit clears the marker", () => {
    expect(usdView({ cost: "actual" }).estimated).toBe(false);
    expect(usdView({ cost: "lower_bound" }).estimated).toBe(true);
    expect(usdView({ cost: "absent" }).estimated).toBe(true);
    expect(usdView(undefined).estimated).toBe(true);
    expect(costMetricOf({ spent_usd: 1, limit_usd: 4 }).estimated).toBe(true);
  });

  it("a tokens view reads the TOKENS basis and ignores the cost basis", () => {
    // The discriminator: a module reading `basis.cost` unconditionally passes
    // every other case in this describe and fails exactly this one.
    const tokens = costMetricOf({
      spent_tokens: 100, limit_tokens: 1000,
      basis: { tokens: "actual", cost: "lower_bound" },
    });
    expect(tokens.unit).toBe("tokens");
    expect(tokens.estimated).toBe(false);
    expect(usdView({ tokens: "actual", cost: "lower_bound" }).estimated).toBe(true);
  });
});

describe("U5 unmeasured calls reach the tooltip", () => {
  function callsTooltip(unmeasured: unknown) {
    return costMetricOf({ spent_usd: 1, limit_usd: 4, unmeasured_calls: unmeasured }).tooltip;
  }

  it("states a zero and pins singular against plural", () => {
    expect(callsTooltip(0)).toContain("No unmeasured calls");
    expect(callsTooltip(1)).toContain("1 unmeasured call");
    expect(callsTooltip(1)).not.toContain("1 unmeasured calls");
    expect(callsTooltip(3)).toContain("3 unmeasured calls");
  });

  it("an absent count adds no line", () => {
    expect(callsTooltip(undefined).join("|")).not.toContain("unmeasured");
  });
});

describe("U6 malformed input is not an error", () => {
  const broken: unknown[] = [
    null, undefined, "a string", [], 7, {},
    { spent_usd: -1, limit_usd: 4 },
    { spent_usd: Number.NaN, limit_usd: 4 },
    { spent_usd: 1, limit_usd: 0 },
    { spent_usd: 1, limit_usd: 4, basis: "actual" },
  ];

  it("every shape yields a view and throws nothing", () => {
    for (const input of broken) {
      expect(() => costMetricOf(input)).not.toThrow();
      const view = costMetricOf(input);
      expect(typeof view.display).toBe("string");
      expect(Array.isArray(view.tooltip)).toBe(true);
      expect(["usd", "tokens"]).toContain(view.unit);
    }
  });

  it("a limit of zero is limitless rather than a division by zero", () => {
    const view = costMetricOf({ spent_usd: 1, limit_usd: 0 });
    expect(view.fill).toBeNull();
    expect(view.level).toBeNull();
    expect(view.limitless).toBe(true);
    expect(JSON.stringify(view)).not.toContain("Infinity");
  });

  it("a non-object basis marks the figure estimated", () => {
    expect(costMetricOf({ spent_usd: 1, limit_usd: 4, basis: "actual" }).estimated).toBe(true);
  });

  it("a NEGATIVE spend with a usable limit is limitless, not a negative fill", () => {
    // Finding R-0671: `usableFigure` already rejects a negative and the module
    // was correct; the missing thing was the proof. A spend read as absent
    // leaves no pair to divide, so the limitless variant is the answer rather
    // than a bar drawn backwards.
    const view = costMetricOf({ spent_usd: -1, limit_usd: 4 });
    expect(view.fill).toBeNull();
    expect(view.level).toBeNull();
    expect(view.limitless).toBe(true);
    expect(view.display).toBe("—");
  });
});

describe("U7 no price arithmetic in the frontend", () => {
  const PERMITTED_NUMBERS = new Set([0, 1, 100, 0.85, 2, 1000, 1000000]);
  const FORBIDDEN_TOKENS = ["price", "rate", "tariff", "perToken", "per_token"];

  it("the comment stripper actually removes something", async () => {
    const source = await costMetricSource();
    const code = withoutComments(source);
    expect(source.length).toBeGreaterThan(0);
    expect(code.length).toBeLessThan(source.length);
    // The module's own prose names two forbidden tokens on purpose, so a guard
    // reading the unstripped source would go red on the next assertion.
    expect(source.toLowerCase()).toContain("price");
    expect(source.toLowerCase()).toContain("rate");
  });

  it("the code names no price, rate or tariff", async () => {
    const code = withoutComments(await costMetricSource()).toLowerCase();
    for (const token of FORBIDDEN_TOKENS) {
      expect(code).not.toContain(token.toLowerCase());
    }
  });

  it("every numeric literal is one DECISION F022 D4 clause 5 permits", async () => {
    const code = withoutComments(await costMetricSource());
    const literals = code.match(/(?<![A-Za-z_$.\d])\d+(?:\.\d+)?/g) ?? [];
    expect(literals.length).toBeGreaterThan(0);
    for (const literal of literals) {
      expect(PERMITTED_NUMBERS.has(Number(literal))).toBe(true);
    }
  });
});

describe("the formatters this module exports", () => {
  it("formats dollars to two decimals and tokens on the 1k/1M rule", () => {
    expect(formatUsd(1.5)).toBe("$1.50");
    expect(formatTokenCount(999)).toBe("999");
    expect(formatTokenCount(1200)).toBe("1.2k");
    expect(formatTokenCount(2500000)).toBe("2.5M");
  });
});

describe("GO the fixture tick stream against a hand-written golden table", () => {
  // GO1 The stream in ARRIVAL order: one job walked from its first tick to over
  // its limit — normal, then warn, then exceeded — with the cost basis flipping
  // from `lower_bound` to `actual` mid-stream, then a limitless job's tick.
  // These are envelope payloads verbatim, snake_case and optional throughout,
  // and not view models.
  const BUDGET_TICK_STREAM: unknown[] = [
    {
      spent_usd: 1, limit_usd: 4, spent_tokens: 2000, limit_tokens: 8000,
      unmeasured_calls: 3, basis: { cost: "lower_bound", tokens: "actual" },
    },
    {
      spent_usd: 3.4, limit_usd: 4, spent_tokens: 6800, limit_tokens: 8000,
      unmeasured_calls: 1, basis: { cost: "lower_bound", tokens: "actual" },
    },
    {
      spent_usd: 4.6, limit_usd: 4, spent_tokens: 9200, limit_tokens: 8000,
      unmeasured_calls: 0, basis: { cost: "actual", tokens: "actual" },
    },
    { spent_usd: 0.75, basis: { cost: "lower_bound" } },
  ];

  // GO2 One golden per tick, each the WHOLE view. Written out by hand from
  // DECISION F022 D4's clauses; a table printed from the module would agree
  // with whatever the module does and would pin nothing.
  const COST_VIEW_GOLDENS = [
    {
      display: "$1.00", unit: "usd", estimated: true, fill: 0.25,
      level: "normal", limitless: false,
      tooltip: [
        "Cost $1.00 of $4.00 (25%)",
        "Tokens 2.0k of 8.0k (25%)",
        "Figures are an estimate",
        "3 unmeasured calls",
      ],
    },
    {
      display: "$3.40", unit: "usd", estimated: true, fill: 0.85,
      level: "warn", limitless: false,
      tooltip: [
        "Cost $3.40 of $4.00 (85%)",
        "Tokens 6.8k of 8.0k (85%)",
        "Figures are an estimate",
        "1 unmeasured call",
      ],
    },
    {
      display: "$4.60", unit: "usd", estimated: false, fill: 1.15,
      level: "exceeded", limitless: false,
      tooltip: [
        "Cost $4.60 of $4.00 (115%)",
        "Tokens 9.2k of 8.0k (115%)",
        "Figures are actual",
        "No unmeasured calls",
      ],
    },
    {
      display: "$0.75", unit: "usd", estimated: true, fill: null,
      level: null, limitless: true,
      tooltip: [
        "Spent $0.75, with no limit to measure it against",
        "Figures are an estimate",
      ],
    },
  ];

  it("carries exactly one golden per tick", () => {
    expect(COST_VIEW_GOLDENS).toHaveLength(BUDGET_TICK_STREAM.length);
  });

  BUDGET_TICK_STREAM.forEach((payload, index) => {
    const golden = COST_VIEW_GOLDENS[index];
    it(`tick ${index} renders ${golden.display} at level ${golden.level ?? "none"}`, () => {
      expect(costMetricOf(payload)).toEqual(golden);
    });
  });

  // GO3 The table is asserted over ITSELF, so a later edit cannot quietly drop a
  // state and leave a green suite behind. Each failure names what is missing.
  it("the table still covers every level and both bases", () => {
    const levels: (string | null)[] = COST_VIEW_GOLDENS.map(g => g.level);
    for (const level of ["normal", "warn", "exceeded"]) {
      expect(levels, `the golden table carries no ${level} level`).toContain(level);
    }
    expect(levels, "the golden table carries no null level, so the limitless variant is unpinned").toContain(null);
    const bases: boolean[] = COST_VIEW_GOLDENS.map(g => g.estimated);
    expect(bases, "the golden table carries no estimated figure").toContain(true);
    expect(bases, "the golden table carries no actual figure").toContain(false);
  });
});
