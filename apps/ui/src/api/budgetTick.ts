// The one place a brain-stream frame is read as a budget tick. DECISION F022 D6
// rules that the latest tick's figures are held on the stream state, and this
// module is the reader that feeds that fold: it recognises the kind, hands the
// payload through untouched, and decides nothing about what the payload MEANS.
//
// Remedy deliberately does not perform arithmetic, choose a unit or compose a
// sentence here: `costMetric.ts` is the single home for every one of those
// decisions, and a second reader of the figure fields would be a second home.
// This module therefore never names a figure field at all.
import type { BrainStreamFrame } from "./brainStream";
import type { BudgetTickFigures } from "./costMetric";

// One-directional at RUNTIME: both imports are `import type`, which TypeScript
// erases, so the emitted graph does not name `brainStream.ts` back — the same
// shape `feedRow.ts` documents in its own header.

/** The envelope kind that carries figures, matching `BUDGET_TICK_EVENT` in
 *  `packages/orchestration/ui_server.py`. No other kind gains a `budget` key. */
const BUDGET_TICK_KIND = "budget.tick";

/** Read any value as an object. `null`, an array and every primitive read as
 *  the empty payload rather than throwing: the envelope is parsed JSON from a
 *  server this client does not control, so every field is CHECKED. */
function objectOf(value: unknown): Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

/** The latest tick's figures carried by one frame, or null when the frame is
 *  not a budget tick. The kind is `frame.event.event` — a frame's `event` field
 *  holds the whole safe ENVELOPE and the envelope's own `event` field is the
 *  kind string, which reads like a typo and is not one (the same trap
 *  `feedRow.ts` resolves). Total: it accepts anything and throws nothing. */
export function budgetTickFiguresOf(frame: BrainStreamFrame): BudgetTickFigures | null {
  const envelope = objectOf(frame.event);
  if (envelope["event"] !== BUDGET_TICK_KIND) return null;
  const budget = envelope["budget"];
  if (typeof budget !== "object" || budget === null || Array.isArray(budget)) return null;
  return budget as BudgetTickFigures;
}
