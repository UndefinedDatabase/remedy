import { describe, it, expect } from "vitest";
import {
  decisionClarificationFieldKey,
  collectDecisionClarificationAnswers,
} from "./decisionClarificationForm";
import { buildDecisionCardModel } from "./decisionCard";

/** A pending approval carrying the named questions, built through the real
 *  projection so the test cannot drift from the model the card renders. */
function approvalWith(decisionId: string, questionIds: string[]) {
  return buildDecisionCardModel({
    id: decisionId,
    status: "open",
    payload: {
      clarifications: questionIds.map(id => ({
        id,
        question: `question ${id}`,
        default_answer: `default ${id}`,
        impact: "medium",
      })),
    },
  });
}

describe("decisionClarificationFieldKey", () => {
  it("pairs the decision's position, the decision's id and the question's id", () => {
    expect(decisionClarificationFieldKey(2, "d-7", "q-risk")).toBe("2-d-7-q-risk");
  });

  it("gives two cards that share one id different keys for the same question", () => {
    // The inbox is a projection of a queue and can carry a duplicate id. A key
    // built from the id alone would collide here, and one card's field would
    // then hold the other card's answer.
    const first = decisionClarificationFieldKey(0, "d-1", "q-1");
    const second = decisionClarificationFieldKey(1, "d-1", "q-1");
    expect(first).not.toBe(second);
  });
});

describe("collectDecisionClarificationAnswers", () => {
  it("keys the map by the question id and never by the field key", () => {
    // The server compares the key against the plan's own question ids, so a map
    // keyed by the field key would be refused whole.
    const decision = approvalWith("d-1", ["q-1"]);
    const values = { [decisionClarificationFieldKey(0, "d-1", "q-1")]: "yes, proceed" };
    expect(collectDecisionClarificationAnswers(values, 0, decision)).toEqual({
      "q-1": "yes, proceed",
    });
  });

  it("collects the empty string for a field the operator never touched", () => {
    const decision = approvalWith("d-1", ["q-1", "q-2"]);
    const values = { [decisionClarificationFieldKey(0, "d-1", "q-1")]: "typed" };
    expect(collectDecisionClarificationAnswers(values, 0, decision)).toEqual({
      "q-1": "typed",
      "q-2": "",
    });
  });

  it("collects an empty object for a decision that carries no clarification", () => {
    // Every card but a pending flight-plan approval is this case, and it is the
    // normal one: the empty map is what becomes an absent `answers` key.
    const decision = buildDecisionCardModel({ id: "d-1", status: "open" });
    expect(decision.clarifications).toEqual([]);
    expect(collectDecisionClarificationAnswers({}, 0, decision)).toEqual({});
  });

  it("does not let a value stored under another decision's field key leak in", () => {
    // The store is flat and holds every card's fields at once. A collector that
    // iterated the store rather than this decision's questions would post the
    // other card's text under this card's question.
    const decision = approvalWith("d-1", ["q-1"]);
    const values = {
      [decisionClarificationFieldKey(1, "d-2", "q-1")]: "another card's text",
    };
    expect(collectDecisionClarificationAnswers(values, 0, decision)).toEqual({ "q-1": "" });
  });

  it("carries a value with surrounding whitespace untrimmed", () => {
    // Trimming has ONE owner, `clarificationAnswersArg` in `./decisionAnswer.ts`.
    // A second trim here would be a second owner of one rule.
    const decision = approvalWith("d-1", ["q-1"]);
    const values = { [decisionClarificationFieldKey(0, "d-1", "q-1")]: "  spaced  " };
    expect(collectDecisionClarificationAnswers(values, 0, decision)).toEqual({
      "q-1": "  spaced  ",
    });
  });
});
