import { describe, it, expect } from "vitest";
import { buildDecisionCardModel } from "./decisionCard";
import type { DecisionCardModel } from "./decisionCard";
import {
  DECISION_FILTER_ALL,
  decisionInboxView,
  decisionTypeChoices,
  filterDecisionsByType,
} from "./decisionFilter";

/** A model built the way the endpoint's own payload builds one, so these tests
 *  filter the objects the app really renders rather than hand-made lookalikes.
 *  `type` is left out where a card is meant to arrive untyped, which is exactly
 *  how `build_decision_inbox` sends a decision whose producer omitted it. */
function card(id: string, type?: string): DecisionCardModel {
  return buildDecisionCardModel({ id, type, status: "open" });
}

describe("decisionTypeChoices", () => {
  it("offers a decision type this repository has never produced, because the choices are DERIVED", () => {
    // THE EXTENSIBILITY PROPERTY, and the reason this module holds no hardcoded
    // type list and no switch over a decision type: a producer that starts
    // emitting a brand new kind of question gets a working chip the same day,
    // with no edit here. A reader who came looking for a per-type registry is
    // looking for something this module refuses to have.
    const choices = decisionTypeChoices([card("d-1", "quantum_handshake")]);
    expect(choices.map((choice) => choice.value)).toEqual([
      DECISION_FILTER_ALL,
      "quantum_handshake",
    ]);
    expect(choices[1].label).toBe("quantum_handshake");
  });

  it("puts the all choice first and counts every model on it", () => {
    const choices = decisionTypeChoices([card("d-1", "review"), card("d-2", "approval")]);
    expect(choices[0]).toEqual({ value: DECISION_FILTER_ALL, label: "All", count: 2 });
  });

  it("offers one choice per distinct type, sorted ascending", () => {
    const models = [
      card("d-1", "review"),
      card("d-2", "approval"),
      card("d-3", "review"),
      card("d-4", "escalation"),
    ];
    const choices = decisionTypeChoices(models);
    expect(choices.map((choice) => choice.value)).toEqual([
      DECISION_FILTER_ALL,
      "approval",
      "escalation",
      "review",
    ]);
    expect(new Set(choices.map((choice) => choice.value)).size).toBe(choices.length);
  });

  it("counts the models standing behind each choice", () => {
    const models = [card("d-1", "review"), card("d-2", "review"), card("d-3", "approval")];
    const counts = Object.fromEntries(
      decisionTypeChoices(models).map((choice) => [choice.value, choice.count]),
    );
    expect(counts).toEqual({ [DECISION_FILTER_ALL]: 3, approval: 1, review: 2 });
  });

  it("offers a chip for an untyped card, so no card is unreachable from the control", () => {
    const choices = decisionTypeChoices([card("d-1"), card("d-2", "review")]);
    expect(choices.map((choice) => choice.value)).toEqual([DECISION_FILTER_ALL, "", "review"]);
    expect(choices[1]).toEqual({ value: "", label: "Untyped", count: 1 });
  });

  it("offers the all choice alone, counting nothing, for an inbox with no models", () => {
    expect(decisionTypeChoices([])).toEqual([
      { value: DECISION_FILTER_ALL, label: "All", count: 0 },
    ]);
  });

  it("does not offer a second chip for a decision typed with the all sentinel itself", () => {
    const choices = decisionTypeChoices([card("d-1", DECISION_FILTER_ALL), card("d-2", "review")]);
    expect(choices.map((choice) => choice.value)).toEqual([DECISION_FILTER_ALL, "review"]);
    expect(choices[0].count).toBe(2);
  });
});

describe("filterDecisionsByType", () => {
  it("yields every model under the all value", () => {
    const models = [card("d-1", "review"), card("d-2"), card("d-3", "approval")];
    expect(filterDecisionsByType(models, DECISION_FILTER_ALL).map((m) => m.id)).toEqual([
      "d-1",
      "d-2",
      "d-3",
    ]);
  });

  it("yields only the models of the type it was given", () => {
    const models = [card("d-1", "review"), card("d-2", "approval"), card("d-3", "review")];
    expect(filterDecisionsByType(models, "review").map((m) => m.id)).toEqual(["d-1", "d-3"]);
  });

  it("yields the untyped models under the empty type", () => {
    const models = [card("d-1"), card("d-2", "review")];
    expect(filterDecisionsByType(models, "").map((m) => m.id)).toEqual(["d-1"]);
  });

  it("yields nothing for a type no model carries", () => {
    const models = [card("d-1", "review"), card("d-2", "approval")];
    expect(filterDecisionsByType(models, "quantum_handshake")).toEqual([]);
  });

  it("preserves the order it was given rather than imposing one of its own", () => {
    const models = [card("z", "review"), card("a", "review"), card("m", "review")];
    expect(filterDecisionsByType(models, "review").map((m) => m.id)).toEqual(["z", "a", "m"]);
  });

  it("returns a new array and neither mutates nor reorders the one it was given", () => {
    const models = [card("z", "review"), card("a", "approval"), card("m", "review")];
    const before = models.map((m) => m.id);
    const filtered = filterDecisionsByType(models, DECISION_FILTER_ALL);
    expect(filtered).not.toBe(models);
    expect(models.map((m) => m.id)).toEqual(before);
    filtered.reverse();
    expect(models.map((m) => m.id)).toEqual(before);
  });
});

describe("decisionInboxView", () => {
  it("reports no empty message while something is visible", () => {
    const view = decisionInboxView([card("d-1", "review")], DECISION_FILTER_ALL);
    expect(view.visible.map((m) => m.id)).toEqual(["d-1"]);
    expect(view.emptyMessage).toBeNull();
  });

  it("carries the same choices the control derives, whatever the filter", () => {
    const models = [card("d-1", "review"), card("d-2", "approval")];
    const view = decisionInboxView(models, "approval");
    expect(view.choices).toEqual(decisionTypeChoices(models));
    expect(view.visible.map((m) => m.id)).toEqual(["d-2"]);
  });

  it("says an empty inbox is empty, in one quiet line", () => {
    const view = decisionInboxView([], DECISION_FILTER_ALL);
    expect(view.visible).toEqual([]);
    expect(view.emptyMessage).toBe("No decisions are waiting.");
  });

  it("names the filtered type when the filter is what emptied the list", () => {
    const view = decisionInboxView([card("d-1", "review")], "approval");
    expect(view.visible).toEqual([]);
    expect(view.emptyMessage).toBe("No approval decisions are waiting.");
    expect(view.emptyMessage).not.toBe("No decisions are waiting.");
  });

  it("names an untyped filter in words rather than leaving a gap in the sentence", () => {
    const view = decisionInboxView([card("d-1", "review")], "");
    expect(view.emptyMessage).toBe("No untyped decisions are waiting.");
  });

  it("still offers the all choice when the filter emptied the list, so the operator can get back", () => {
    const view = decisionInboxView([card("d-1", "review")], "approval");
    expect(view.choices[0]).toEqual({ value: DECISION_FILTER_ALL, label: "All", count: 1 });
  });

  it("never throws, however broken the models it is handed", () => {
    const broken = [{ ...card("d-1", "review"), type: undefined as unknown as string }];
    expect(() => decisionInboxView(broken, DECISION_FILTER_ALL)).not.toThrow();
    expect(decisionTypeChoices(broken).map((choice) => choice.value)).toEqual([
      DECISION_FILTER_ALL,
      "",
    ]);
  });
});
