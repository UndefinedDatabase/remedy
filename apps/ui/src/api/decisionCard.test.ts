import { describe, it, expect } from "vitest";
import {
  buildDecisionCardModel,
  countOpenDecisions,
  decisionAgeLabel,
  decisionAnswers,
  decisionBlockedLabel,
  decisionCardModels,
} from "./decisionCard";
import type { DecisionInboxEntry } from "./decisionCard";

/** A decision type this repository has never produced. It exists here to prove
 *  the renderer is generic; if a producer ever emits it, pick another. */
const NOVEL_TYPE = "warp_core_alignment";

describe("decisionAgeLabel", () => {
  it("reports an unreadable stamp as unknown rather than as zero", () => {
    expect(decisionAgeLabel(null)).toBe("unknown age");
  });

  it("reports a fresh question in seconds", () => {
    expect(decisionAgeLabel(0)).toBe("0s");
  });

  it("stays in seconds at the last whole second", () => {
    expect(decisionAgeLabel(59)).toBe("59s");
  });

  it("switches to minutes exactly at the minute boundary", () => {
    expect(decisionAgeLabel(60)).toBe("1m");
  });

  it("stays in minutes at the last whole minute", () => {
    expect(decisionAgeLabel(3599)).toBe("59m");
  });

  it("switches to hours exactly at the hour boundary", () => {
    expect(decisionAgeLabel(3600)).toBe("1h");
  });

  it("stays in hours at the last whole hour", () => {
    expect(decisionAgeLabel(86399)).toBe("23h");
  });

  it("switches to days exactly at the day boundary", () => {
    expect(decisionAgeLabel(86400)).toBe("1d");
  });

  it("truncates a multi-day age toward zero", () => {
    expect(decisionAgeLabel(86400 * 9 + 3600)).toBe("9d");
  });

  it("treats a negative age as zero rather than reporting it", () => {
    expect(decisionAgeLabel(-5)).toBe("0s");
  });
});

describe("decisionBlockedLabel", () => {
  it("says so plainly when nothing waits behind the decision", () => {
    expect(decisionBlockedLabel(0)).toBe("blocks nothing");
  });

  it("uses the singular for exactly one blocked task", () => {
    expect(decisionBlockedLabel(1)).toBe("blocks 1 task");
  });

  it("uses the plural above one", () => {
    expect(decisionBlockedLabel(4)).toBe("blocks 4 tasks");
  });
});

describe("decisionAnswers", () => {
  it("offers one option answer per payload option", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      payload: { options: ["retry", "skip"] },
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "option", label: "retry", value: "retry" },
      { kind: "option", label: "skip", value: "skip" },
    ]);
  });

  it("offers the next actions as commands when the payload names no options", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      next_actions: ["remedy resume", "remedy abort"],
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "command", label: "remedy resume", value: "remedy resume" },
      { kind: "command", label: "remedy abort", value: "remedy abort" },
    ]);
  });

  it("falls back to a single free-text answer when the card names neither", () => {
    expect(decisionAnswers({ type: "task_decision" })).toEqual([
      { kind: "free_text", label: "Answer", value: "" },
    ]);
  });

  it("falls through an options key that is present but empty", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      payload: { options: [] },
      next_actions: ["remedy resume"],
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "command", label: "remedy resume", value: "remedy resume" },
    ]);
  });

  it("falls through a missing payload without throwing", () => {
    expect(() => decisionAnswers({ type: "task_decision" })).not.toThrow();
    expect(decisionAnswers({ type: "task_decision", payload: null })).toEqual([
      { kind: "free_text", label: "Answer", value: "" },
    ]);
  });

  it("renders a non-string option rather than dropping the question", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      payload: { options: [7, true] },
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "option", label: "7", value: "7" },
      { kind: "option", label: "true", value: "true" },
    ]);
  });

  it("renders a NOVEL decision type generically, from its payload alone", () => {
    const card: DecisionInboxEntry = {
      type: NOVEL_TYPE,
      safe_summary: "Realign the warp core before the next burn",
      payload: { options: ["realign now", "defer one cycle"] },
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "option", label: "realign now", value: "realign now" },
      { kind: "option", label: "defer one cycle", value: "defer one cycle" },
    ]);
  });

  it("gives two cards that differ ONLY in type identical answers", () => {
    const payload = { options: ["approve", "reject"] };
    const known: DecisionInboxEntry = { type: "task_decision", payload };
    const novel: DecisionInboxEntry = { type: NOVEL_TYPE, payload };
    expect(decisionAnswers(novel)).toEqual(decisionAnswers(known));
    expect(decisionAnswers(novel)).toHaveLength(2);
  });
});

describe("buildDecisionCardModel", () => {
  it("flattens a full card into the fields a renderer projects", () => {
    const card: DecisionInboxEntry = {
      id: "d-1",
      type: "task_decision",
      status: "open",
      severity: "blocker",
      safe_summary: "Two migrations claim the same table",
      next_actions: ["remedy decision answer d-1"],
      payload: { options: ["keep first", "keep second"] },
      age_seconds: 7320,
      blocked_count: 3,
    };
    expect(buildDecisionCardModel(card)).toEqual({
      id: "d-1",
      type: "task_decision",
      status: "open",
      severity: "blocker",
      title: "Two migrations claim the same table",
      ageLabel: "2h",
      ageSeconds: 7320,
      blockedLabel: "blocks 3 tasks",
      blockedCount: 3,
      isOpen: true,
      answers: [
        { kind: "option", label: "keep first", value: "keep first" },
        { kind: "option", label: "keep second", value: "keep second" },
      ],
    });
  });

  it("does not treat a resolved decision as open", () => {
    expect(buildDecisionCardModel({ status: "resolved" }).isOpen).toBe(false);
  });

  it("renders a card with every optional field absent without throwing", () => {
    expect(() => buildDecisionCardModel({})).not.toThrow();
    expect(buildDecisionCardModel({})).toEqual({
      id: "",
      type: "",
      status: "",
      severity: "",
      title: "",
      ageLabel: "unknown age",
      ageSeconds: null,
      blockedLabel: "blocks nothing",
      blockedCount: 0,
      isOpen: false,
      answers: [{ kind: "free_text", label: "Answer", value: "" }],
    });
  });
});

describe("decisionCardModels", () => {
  it("preserves the order the endpoint sent", () => {
    const models = decisionCardModels({
      decisions: [
        { id: "first", age_seconds: 10, blocked_count: 9 },
        { id: "second", age_seconds: 90000, blocked_count: 0 },
        { id: "third", age_seconds: 120, blocked_count: 1 },
      ],
    });
    expect(models.map((m) => m.id)).toEqual(["first", "second", "third"]);
    expect(models.map((m) => m.ageLabel)).toEqual(["10s", "1d", "2m"]);
    expect(models.map((m) => m.blockedLabel)).toEqual([
      "blocks 9 tasks",
      "blocks nothing",
      "blocks 1 task",
    ]);
  });

  it("gives no cards for an inbox document carrying no decisions key", () => {
    expect(decisionCardModels({})).toEqual([]);
  });

  it("gives no cards when decisions is not an array", () => {
    expect(decisionCardModels({ decisions: "not an array" })).toEqual([]);
  });
});

describe("countOpenDecisions", () => {
  it("answers zero for an inbox with no cards at all", () => {
    expect(countOpenDecisions([])).toBe(0);
  });

  it("counts only the open cards of a mixed list", () => {
    const models = decisionCardModels({
      decisions: [
        { id: "a", status: "open" },
        { id: "b", status: "resolved" },
        { id: "c", status: "open" },
        { id: "d", status: "cancelled" },
      ],
    });
    expect(countOpenDecisions(models)).toBe(2);
  });

  it("answers zero when every card in the list is already resolved", () => {
    const models = decisionCardModels({
      decisions: [
        { id: "a", status: "resolved" },
        { id: "b", status: "resolved" },
      ],
    });
    expect(countOpenDecisions(models)).toBe(0);
  });

  it("reads isOpen rather than an open-SOUNDING status string", () => {
    // "reopened" is open-sounding and is NOT the endpoint's open status, so a
    // count that compared status text of its own would answer 1 here. The model
    // makes that comparison once, in buildDecisionCardModel, and this pins that
    // the count trusts it rather than repeating it.
    const model = buildDecisionCardModel({ id: "a", status: "reopened" });
    expect(model.isOpen).toBe(false);
    expect(countOpenDecisions([model])).toBe(0);
  });

  it("ignores the type filter's business entirely, counting across every type", () => {
    const models = decisionCardModels({
      decisions: [
        { id: "a", type: "task_decision", status: "open" },
        { id: "b", type: NOVEL_TYPE, status: "open" },
        { id: "c", type: NOVEL_TYPE, status: "resolved" },
      ],
    });
    expect(countOpenDecisions(models)).toBe(2);
  });
});
