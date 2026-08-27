import { describe, it, expect } from "vitest";
import { buildDecisionCardModel } from "./decisionCard";
import type { DecisionCardModel } from "./decisionCard";
import { decisionUrgency, orderDecisionInbox } from "./decisionOrder";

/** A model built the way the endpoint's own payload builds one, so these tests
 *  order the objects the app really renders rather than hand-made lookalikes.
 *  `status` defaults to "open" because a closed card is the exception here. */
function card(
  id: string,
  ageSeconds: number | null,
  blockedCount: number,
  status = "open",
): DecisionCardModel {
  return buildDecisionCardModel({
    id,
    status,
    age_seconds: ageSeconds,
    blocked_count: blockedCount,
  });
}

describe("decisionUrgency", () => {
  it("is the blocked size plus one, times the age", () => {
    expect(decisionUrgency(card("d-1", 3600, 3))).toBe(14400);
  });

  it("scores a card that blocks nothing at its own age, not at zero", () => {
    expect(decisionUrgency(card("d-1", 42, 0))).toBe(42);
  });

  it("scores an unreadable age at zero rather than inventing one", () => {
    expect(decisionUrgency(card("d-1", null, 9))).toBe(0);
  });

  it("scores a negative age at zero, because clocks disagreeing is not urgency", () => {
    expect(decisionUrgency(card("d-1", -5, 2))).toBe(0);
  });

  it("scores a non-finite age at zero", () => {
    const model = { ...card("d-1", 10, 2), ageSeconds: Number.POSITIVE_INFINITY };
    expect(decisionUrgency(model)).toBe(0);
  });

  it("counts a non-finite blocked size as blocking nothing", () => {
    const model = { ...card("d-1", 10, 0), blockedCount: Number.NaN };
    expect(decisionUrgency(model)).toBe(10);
  });

  it("counts a negative blocked size as blocking nothing, exactly as its label reads", () => {
    const model = card("d-1", 10, -5);
    expect(model.blockedCount).toBe(-5);
    expect(model.blockedLabel).toBe("blocks nothing");
    expect(decisionUrgency(model)).toBe(10);
  });

  it("never throws, however broken the model it is handed", () => {
    const model = { ...card("", null, 0), ageSeconds: Number.NaN, blockedCount: Number.NaN };
    expect(() => decisionUrgency(model)).not.toThrow();
    expect(decisionUrgency(model)).toBe(0);
  });
});

describe("orderDecisionInbox", () => {
  it("gives a shuffled inbox exactly one order", () => {
    const hot = card("d-hot", 3600, 3); // (3 + 1) * 3600 = 14400
    const warm = card("d-warm", 7200, 0); // (0 + 1) * 7200 = 7200
    const mild = card("d-mild", 60, 5); // (5 + 1) * 60 = 360
    const unknown = card("d-unknown", null, 4); // unreadable stamp scores 0
    const closed = card("d-closed", 86400, 9, "resolved"); // urgent but answered
    const expected = ["d-hot", "d-warm", "d-mild", "d-unknown", "d-closed"];

    const first = orderDecisionInbox([unknown, closed, mild, hot, warm]);
    const second = orderDecisionInbox([warm, mild, closed, hot, unknown]);
    expect(first.map((m) => m.id)).toEqual(expected);
    expect(second.map((m) => m.id)).toEqual(expected);
  });

  it("reads open cards before closed ones whatever their urgency", () => {
    const closed = card("d-closed", 86400 * 30, 99, "resolved");
    const open = card("d-open", 1, 0);
    expect(orderDecisionInbox([closed, open]).map((m) => m.id)).toEqual(["d-open", "d-closed"]);
  });

  it("leaves age as the total order among cards that block nothing", () => {
    // Without the `+ 1` every one of these scores exactly 0 and the tie falls
    // to `id`, which is why the ids here run AGAINST the ages.
    const oldest = card("b-oldest", 500, 0);
    const middle = card("c-middle", 50, 0);
    const newest = card("a-newest", 5, 0);
    expect(orderDecisionInbox([newest, middle, oldest]).map((m) => m.id)).toEqual([
      "b-oldest",
      "c-middle",
      "a-newest",
    ]);
  });

  it("sorts an unreadable age last within its own group, not out of it", () => {
    const unknown = card("d-unknown", null, 100);
    const faint = card("d-faint", 1, 0);
    const closed = card("d-closed", 86400, 9, "resolved");
    expect(orderDecisionInbox([unknown, closed, faint]).map((m) => m.id)).toEqual([
      "d-faint",
      "d-unknown",
      "d-closed",
    ]);
  });

  it("breaks an exact urgency tie by id ascending", () => {
    const zeta = card("zeta", 100, 0); // (0 + 1) * 100 = 100
    const alpha = card("alpha", 10, 9); // (9 + 1) * 10 = 100
    expect(decisionUrgency(zeta)).toBe(decisionUrgency(alpha));
    expect(orderDecisionInbox([zeta, alpha]).map((m) => m.id)).toEqual(["alpha", "zeta"]);
  });

  it("returns a new array and leaves the one it was given untouched", () => {
    const input = [card("d-1", 10, 0), card("d-2", 900, 0), card("d-3", 100, 0)];
    const before = input.map((m) => m.id);
    const ordered = orderDecisionInbox(input);
    expect(ordered).not.toBe(input);
    expect(input.map((m) => m.id)).toEqual(before);
    expect(ordered.map((m) => m.id)).toEqual(["d-2", "d-3", "d-1"]);
  });

  it("orders an empty inbox into a new empty array", () => {
    const input: DecisionCardModel[] = [];
    const ordered = orderDecisionInbox(input);
    expect(ordered).toEqual([]);
    expect(ordered).not.toBe(input);
  });

  it("keeps two cards that are identical in every ordering key together", () => {
    const left = card("same", 10, 1);
    const right = card("same", 10, 1);
    expect(orderDecisionInbox([left, right])).toHaveLength(2);
  });
});
