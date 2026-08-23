// The single home for every render decision the COST metric makes. DECISION
// F022 D4 rules the semantics this file implements: one denominator chosen
// usd-first, an estimate marker read from the basis of the figure actually
// shown, two inclusive thresholds on the ratio, and no arithmetic beyond that
// ratio. A component that had to choose a unit, pick a denominator or compose a
// tooltip line would be a second home for those rules, so it does none of them.
//
// Remedy deliberately does not carry a price, a rate or a per_token tariff
// constant in the frontend: the backend is the single arithmetic home for
// money, and `costMetric.test.ts` guards that absence over this file's source.
//
// This module imports nothing from `./types` — `types.ts` imports FROM here.
// That direction is the one with no cycle, so the input and output types are
// declared below rather than borrowed.

/** The envelope's `budget` payload as it ARRIVES. Every field is optional
 *  because this is parsed JSON from a server the client does not control, and
 *  the field names are the wire's snake_case rather than the client's camel. */
export interface BudgetTickFigures {
  spent_tokens?: number;
  spent_usd?: number;
  limit_tokens?: number;
  limit_usd?: number;
  unmeasured_calls?: number;
  basis?: { cost?: string; tokens?: string };
}

/** Which figure the metric is showing. Chosen by which limit has a spend to
 *  divide, never mixed: a dollar spend over a token limit is a fabricated
 *  ratio wearing a real number's clothes. */
export type CostUnit = "usd" | "tokens";

/** The band the fill falls in. `level` is null exactly when `fill` is, so a
 *  limitless job has no band at all. */
export type CostLevel = "normal" | "warn" | "exceeded";

/** Everything one COST metric renders, decided here so the component decides
 *  nothing. `display` carries NO prefix — `estimated` is the flag the component
 *  turns into the `~` — and `tooltip` holds already-composed lines in the order
 *  they are shown. */
export interface CostMetricView {
  display: string;
  unit: CostUnit;
  estimated: boolean;
  fill: number | null;
  level: CostLevel | null;
  limitless: boolean;
  tooltip: string[];
}

/** DECISION F022 D4 clause 4: inclusive at both boundaries, so exactly 85 per
 *  cent warns and exactly 100 per cent is exceeded. A bar that waited for
 *  85.1 per cent would tell the truth late. */
const WARN_FILL = 0.85;
const EXCEEDED_FILL = 1;

/** The only basis string that means the figure is not an estimate. */
const ACTUAL_BASIS = "actual";

/** What `display` shows when the figure itself is missing. */
const NO_FIGURE = "—";

/** Read any value as an object. `null`, an array, a string, a number and
 *  `undefined` all read as the empty payload rather than throwing, because a
 *  total function is the whole point of this module. */
function objectOf(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

/** Read one figure as a usable non-negative finite number, or null. A string,
 *  a NaN, an infinity and a negative are treated as ABSENT rather than
 *  coerced: a fabricated number is worse than a missing one. */
function usableFigure(value: unknown): number | null {
  const usable = typeof value === "number" && Number.isFinite(value) && value >= 0;
  return usable ? (value as number) : null;
}

/** A limit is usable only when it is POSITIVE. A zero limit is the shape that
 *  would otherwise divide by zero and render an infinity as a fill, and
 *  DECISION F022 D4 clause 3 sends it to the limitless variant instead. */
function usableLimit(value: unknown): number | null {
  const figure = usableFigure(value);
  return figure !== null && figure > 0 ? figure : null;
}

/** The one division this client performs. Null whenever either side is
 *  unusable, which is how a missing limit becomes the limitless variant. */
function ratioOf(spent: number | null, limit: number | null): number | null {
  return spent === null || limit === null ? null : spent / limit;
}

/** Format a dollar figure. Two decimals always, so a ticking value does not
 *  change width while it climbs. */
export function formatUsd(value: number): string {
  return `$${value.toFixed(2)}`;
}

/** Format a token count on the metrics bar's own 1k/1M rule.
 *  `TopMetricsBar.tsx` carries a private copy of this rule; R8 is the round
 *  that makes the component use this one and deletes that copy. */
export function formatTokenCount(value: number): string {
  if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`;
  if (value >= 1000) return `${(value / 1000).toFixed(1)}k`;
  return String(value);
}

/** Format one figure in the unit shown, or the em dash when it is absent. */
function formatFigure(value: number | null, unit: CostUnit): string {
  if (value === null) return NO_FIGURE;
  return unit === "usd" ? formatUsd(value) : formatTokenCount(value);
}

/** With no usable pair there is still a figure to show, and it is whichever
 *  spend arrived — usd first, matching clause 1's preference. */
function fallbackUnit(spentUsd: number | null, spentTokens: number | null): CostUnit {
  if (spentUsd !== null) return "usd";
  return spentTokens !== null ? "tokens" : "usd";
}

/** DECISION F022 D4 clause 2: the marker reads the basis of the figure ACTUALLY
 *  SHOWN, and only the exact string "actual" clears it. Unknown provenance is
 *  not an actual, and the marker is cheap while a false claim of exactness is
 *  not. */
function isEstimated(basis: Record<string, unknown>, unit: CostUnit): boolean {
  const key = unit === "usd" ? "cost" : "tokens";
  return basis[key] !== ACTUAL_BASIS;
}

/** DECISION F022 D4 clause 4, as a total function of the ratio. */
function levelOf(fill: number): CostLevel {
  if (fill >= EXCEEDED_FILL) return "exceeded";
  if (fill >= WARN_FILL) return "warn";
  return "normal";
}

/** The ratio as a whole-number percentage — the second and last piece of
 *  arithmetic clause 5 permits. */
function percentOf(fill: number): string {
  return `${Math.round(fill * 100)}%`;
}

/** One tooltip line enumerating a unit's own spend, limit and fill. Empty when
 *  that unit has no usable pair, so the caller pushes nothing rather than
 *  naming a denominator that does not exist. */
function limitLine(label: string, spent: number | null, limit: number | null, unit: CostUnit): string {
  const fill = ratioOf(spent, limit);
  if (fill === null) return "";
  return `${label} ${formatFigure(spent, unit)} of ${formatFigure(limit, unit)} (${percentOf(fill)})`;
}

/** How many calls the figure could not measure, singular and plural. A zero is
 *  STATED rather than omitted: "no unmeasured calls" is the sentence that makes
 *  an actual basis believable. Absent stays absent. */
function unmeasuredLine(count: number | null): string {
  if (count === null) return "";
  if (count === 0) return "No unmeasured calls";
  return `${count} unmeasured call${count === 1 ? "" : "s"}`;
}

/** Says whether the figures are actual, in the vocabulary DECISION F022 D1
 *  clause four keeps off the wire. */
function basisLine(estimated: boolean): string {
  return estimated ? "Figures are an estimate" : "Figures are actual";
}

/** Turn one budget tick into every render decision the COST metric needs.
 *  Total: it accepts anything, throws nothing, and answers the limitless
 *  variant wherever the payload offers no usable spend-and-limit pair. */
export function costMetricOf(figures: unknown): CostMetricView {
  const payload = objectOf(figures);
  const spentUsd = usableFigure(payload["spent_usd"]);
  const spentTokens = usableFigure(payload["spent_tokens"]);
  const limitUsd = usableLimit(payload["limit_usd"]);
  const limitTokens = usableLimit(payload["limit_tokens"]);
  const basis = objectOf(payload["basis"]);

  // Clause 1: usd wins when it has a usable pair, tokens take it otherwise, and
  // the other unit's limit is NEVER borrowed as this unit's denominator.
  const usdFill = ratioOf(spentUsd, limitUsd);
  const tokenFill = ratioOf(spentTokens, limitTokens);
  const unit = usdFill !== null ? "usd" : tokenFill !== null ? "tokens" : fallbackUnit(spentUsd, spentTokens);
  const fill = usdFill !== null ? usdFill : tokenFill;

  const display = formatFigure(unit === "usd" ? spentUsd : spentTokens, unit);
  const estimated = isEstimated(basis, unit);
  const tooltip: string[] = [];
  if (fill === null) {
    tooltip.push(`Spent ${display}, with no limit to measure it against`);
  } else {
    const usdLine = limitLine("Cost", spentUsd, limitUsd, "usd");
    const tokenLine = limitLine("Tokens", spentTokens, limitTokens, "tokens");
    if (usdLine !== "") tooltip.push(usdLine);
    if (tokenLine !== "") tooltip.push(tokenLine);
  }
  tooltip.push(basisLine(estimated));
  const calls = unmeasuredLine(usableFigure(payload["unmeasured_calls"]));
  if (calls !== "") tooltip.push(calls);

  return {
    display,
    unit,
    estimated,
    fill,
    level: fill === null ? null : levelOf(fill),
    limitless: fill === null,
    tooltip,
  };
}
