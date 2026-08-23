import { describe, it, expect } from "vitest";
import { budgetTickFiguresOf } from "./budgetTick";
import type { BrainStreamFrame } from "./brainStream";

/** One frame as the transport delivers it: `event` is the whole envelope. */
function frameOf(event: unknown): BrainStreamFrame {
  return { seq: 7, event };
}

describe("budgetTickFiguresOf", () => {
  it("a tick frame yields its figures, by reference and untouched", () => {
    const budget = { spent_usd: 1.5, limit_usd: 4, basis: { cost: "actual" } };
    const figures = budgetTickFiguresOf(frameOf({
      seq: 7, event: "budget.tick", timestamp: "", outcome: "", task_id: "", budget,
    }));
    expect(figures).toBe(budget);
  });

  it("a non-tick frame yields null even when it carries a budget key", () => {
    // The kind is what licenses the payload; a stray key on another kind is not
    // a tick and must not be read as the latest one.
    expect(budgetTickFiguresOf(frameOf({
      seq: 7, event: "task.completed", budget: { spent_usd: 9 },
    }))).toBeNull();
  });

  it("a tick frame with no budget key yields null", () => {
    expect(budgetTickFiguresOf(frameOf({ seq: 7, event: "budget.tick" }))).toBeNull();
  });

  it("a tick frame whose budget is not an object yields null", () => {
    for (const budget of [null, "1.50", 3, [1, 2], true]) {
      expect(budgetTickFiguresOf(frameOf({ seq: 7, event: "budget.tick", budget }))).toBeNull();
    }
  });

  it("an envelope that is a string, null, an array or absent yields null", () => {
    // Parsed JSON from a server this client does not control: every one of
    // these shapes must answer null rather than throw.
    for (const event of ["budget.tick", null, [{ event: "budget.tick" }], undefined, 42]) {
      expect(() => budgetTickFiguresOf(frameOf(event))).not.toThrow();
      expect(budgetTickFiguresOf(frameOf(event))).toBeNull();
    }
  });

  it("an empty budget object is still a tick and is returned", () => {
    // Emptiness is `costMetric.ts`'s decision to make, not this reader's.
    const budget = {};
    expect(budgetTickFiguresOf(frameOf({ seq: 7, event: "budget.tick", budget }))).toBe(budget);
  });
});
