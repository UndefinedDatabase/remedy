import { describe, it, expect } from "vitest";
import {
  DECISION_RESOLVE_COMMAND_ID,
  buildDecisionResolveCommand,
  isUsableCommandNonce,
  jobCommandsPath,
} from "./decisionAnswer";
import { buildDecisionCardModel } from "./decisionCard";
import type { DecisionInboxEntry } from "./decisionCard";

/** A nonce the server's character class accepts, used wherever a test is about
 *  something other than the nonce. */
const GOOD_NONCE = "ui-a1b2c3d4";

/** Every model here is built through `buildDecisionCardModel` rather than by
 *  hand, so these tests pin the SEAM between the endpoint's payload and the
 *  command body — not a literal someone typed twice. */
function modelFrom(entry: DecisionInboxEntry) {
  return buildDecisionCardModel(entry);
}

/** The open card the accepted-body tests answer. */
function openCardEntry(): DecisionInboxEntry {
  return {
    id: "d-1",
    type: "task_decision",
    status: "open",
    safe_summary: "Two migrations claim the same table",
    payload: { options: ["keep first", "keep second"] },
  };
}

describe("DECISION_RESOLVE_COMMAND_ID", () => {
  it("is the literal command id the server routes a decision answer by", () => {
    expect(DECISION_RESOLVE_COMMAND_ID).toBe("decision.resolve");
  });
});

describe("jobCommandsPath", () => {
  it("builds the commands path with one leading slash, no host and no query", () => {
    expect(jobCommandsPath("job-42")).toBe("/api/jobs/job-42/commands");
  });
});

describe("isUsableCommandNonce", () => {
  it("accepts a plain id of letters, digits and a hyphen", () => {
    expect(isUsableCommandNonce("ui7-nonce_1")).toBe(true);
  });

  it("refuses the empty string, which carries no id at all", () => {
    expect(isUsableCommandNonce("")).toBe(false);
  });

  it("refuses a 65-character value, one past the server's ceiling", () => {
    const oneTooLong = "a".repeat(65);
    expect(oneTooLong).toHaveLength(65);
    expect(isUsableCommandNonce(oneTooLong)).toBe(false);
    expect(isUsableCommandNonce("a".repeat(64))).toBe(true);
  });

  it("refuses a value opening with a hyphen, which the first class forbids", () => {
    expect(isUsableCommandNonce("-leading")).toBe(false);
  });

  it("refuses a value carrying a path separator, because the nonce becomes a filename", () => {
    expect(isUsableCommandNonce("nonce/../escape")).toBe(false);
  });

  it("answers a non-string candidate rather than throwing on it", () => {
    expect(isUsableCommandNonce(undefined)).toBe(false);
    expect(isUsableCommandNonce(null)).toBe(false);
    expect(isUsableCommandNonce(7)).toBe(false);
  });
});

describe("buildDecisionResolveCommand", () => {
  it("builds the exact body the commands endpoint accepts, key spelling for key spelling", () => {
    const body = buildDecisionResolveCommand(modelFrom(openCardEntry()), "keep first", GOOD_NONCE);
    expect(body).toEqual({
      command: "decision.resolve",
      client_nonce: GOOD_NONCE,
      args: { decision_id: "d-1", answer: "keep first" },
    });
  });

  it("names exactly the three top-level keys and the two arg keys, and no others", () => {
    const body = buildDecisionResolveCommand(modelFrom(openCardEntry()), "keep first", GOOD_NONCE);
    expect(body).not.toBeNull();
    expect(Object.keys(body!).sort()).toEqual(["args", "client_nonce", "command"]);
    expect(Object.keys(body!.args).sort()).toEqual(["answer", "decision_id"]);
  });

  it("sends NO source key, so the record takes the server's human default", () => {
    const body = buildDecisionResolveCommand(modelFrom(openCardEntry()), "keep first", GOOD_NONCE);
    expect(body).not.toBeNull();
    expect(Object.keys(body!)).not.toContain("source");
    expect(Object.keys(body!.args)).not.toContain("source");
  });

  it("carries the answer the operator chose from the card's own affordances", () => {
    const model = modelFrom(openCardEntry());
    const chosen = model.answers[1];
    const body = buildDecisionResolveCommand(model, chosen.value, GOOD_NONCE);
    expect(body?.args.answer).toBe("keep second");
  });

  it("refuses a model with no id, because no record could match it", () => {
    const model = modelFrom({ status: "open", safe_summary: "A half-written card" });
    expect(model.id).toBe("");
    expect(buildDecisionResolveCommand(model, "keep first", GOOD_NONCE)).toBeNull();
  });

  it("refuses an empty answer, because the decision would resolve with nothing", () => {
    expect(buildDecisionResolveCommand(modelFrom(openCardEntry()), "", GOOD_NONCE)).toBeNull();
  });

  it("refuses a whitespace-only answer, which the server accepts and writes ONCE", () => {
    const model = modelFrom(openCardEntry());
    expect(buildDecisionResolveCommand(model, "   ", GOOD_NONCE)).toBeNull();
    expect(buildDecisionResolveCommand(model, "\t", GOOD_NONCE)).toBeNull();
    expect(buildDecisionResolveCommand(model, "\n \r\n", GOOD_NONCE)).toBeNull();
  });

  it("trims the answer it sends, so the write-once record carries no stray space", () => {
    const body = buildDecisionResolveCommand(modelFrom(openCardEntry()), "  keep first\n", GOOD_NONCE);
    expect(body?.args.answer).toBe("keep first");
  });

  it("trims only the edges, leaving the operator's own inner spacing alone", () => {
    const body = buildDecisionResolveCommand(modelFrom(openCardEntry()), " keep  the first one ", GOOD_NONCE);
    expect(body?.args.answer).toBe("keep  the first one");
  });

  it("refuses a nonce outside the class the server enforces", () => {
    expect(buildDecisionResolveCommand(modelFrom(openCardEntry()), "keep first", "-bad/nonce")).toBeNull();
  });

  it("refuses a decision that is NOT open, which the server answers 409", () => {
    const resolved = modelFrom({ ...openCardEntry(), status: "resolved" });
    expect(resolved.isOpen).toBe(false);
    expect(buildDecisionResolveCommand(resolved, "keep first", GOOD_NONCE)).toBeNull();
  });

  it("reads isOpen rather than an open-SOUNDING status string", () => {
    const reopened = modelFrom({ ...openCardEntry(), status: "reopened" });
    expect(reopened.status).toBe("reopened");
    expect(buildDecisionResolveCommand(reopened, "keep first", GOOD_NONCE)).toBeNull();
  });
});

describe("buildDecisionResolveCommand clarification answers", () => {
  /** The pending flight-plan approval this form exists for, with the two words
   *  the write door accepts and one open question riding the same card. */
  function pendingPlanEntry(): DecisionInboxEntry {
    return {
      id: "fp:approval",
      type: "flight_plan_approval",
      status: "open",
      safe_summary: "Flight plan awaiting approval (1 open question).",
      payload: {
        options: ["approve", "reject"],
        clarifications: [{ id: "q1", question: "Which store?", default_answer: "postgres" }],
      },
      answerable_by_decision_resolve: true,
    };
  }

  it("sends NO answers key at all when the caller passes no fourth argument", () => {
    const body = buildDecisionResolveCommand(modelFrom(pendingPlanEntry()), "approve", GOOD_NONCE);
    expect(body).not.toBeNull();
    expect(Object.keys(body!.args).sort()).toEqual(["answer", "decision_id"]);
    expect(Object.keys(body!.args)).not.toContain("answers");
    expect(body!.args.answers).toBeUndefined();
  });

  it("builds the byte-identical body a caller written before this form built", () => {
    // The property the whole round rests on: adding an optional fourth argument
    // may not move a single key of the body every existing call site already
    // produces, because those call sites pass nothing.
    const model = modelFrom(pendingPlanEntry());
    const before = buildDecisionResolveCommand(model, "approve", GOOD_NONCE);
    expect(JSON.stringify(before)).toBe(
      JSON.stringify({
        command: "decision.resolve",
        client_nonce: GOOD_NONCE,
        args: { decision_id: "fp:approval", answer: "approve" },
      }),
    );
  });

  it("carries a map that survives filtering under the server's own args key", () => {
    const body = buildDecisionResolveCommand(
      modelFrom(pendingPlanEntry()),
      "approve",
      GOOD_NONCE,
      { q1: "sqlite" },
    );
    expect(body).not.toBeNull();
    expect(Object.keys(body!.args).sort()).toEqual(["answer", "answers", "decision_id"]);
    expect(body!.args.answers).toEqual({ q1: "sqlite" });
    expect(body!.args.decision_id).toBe("fp:approval");
    expect(body!.args.answer).toBe("approve");
  });

  it("keys the answers by the question id the card model carried out", () => {
    const model = modelFrom(pendingPlanEntry());
    expect(model.clarifications.map((question) => question.id)).toEqual(["q1"]);
    const body = buildDecisionResolveCommand(model, "approve", GOOD_NONCE, {
      [model.clarifications[0].id]: "sqlite",
    });
    expect(body?.args.answers).toEqual({ q1: "sqlite" });
  });

  it("OMITS the key rather than sending it empty for an all-blank map", () => {
    // Absent already MEANS the default per question, so a form the operator
    // never touched must post exactly what passing nothing posts.
    const body = buildDecisionResolveCommand(modelFrom(pendingPlanEntry()), "approve", GOOD_NONCE, {
      q1: "   ",
      q2: "\n\t",
      q3: "",
    });
    expect(body).not.toBeNull();
    expect(Object.keys(body!.args)).not.toContain("answers");
    expect(body!.args.answers).toBeUndefined();
  });

  it("OMITS the key for an empty map, which chose nothing at all", () => {
    const body = buildDecisionResolveCommand(modelFrom(pendingPlanEntry()), "approve", GOOD_NONCE, {});
    expect(Object.keys(body!.args)).not.toContain("answers");
  });

  it("drops only the blank entries, keeping the ones the operator did fill", () => {
    const body = buildDecisionResolveCommand(modelFrom(pendingPlanEntry()), "approve", GOOD_NONCE, {
      q1: "sqlite",
      q2: "  ",
      q3: "behind a flag",
    });
    expect(body?.args.answers).toEqual({ q1: "sqlite", q3: "behind a flag" });
  });

  it("trims the values it sends, for the reason it already trims the answer", () => {
    const body = buildDecisionResolveCommand(modelFrom(pendingPlanEntry()), "approve", GOOD_NONCE, {
      q1: "  sqlite\n",
    });
    expect(body?.args.answers).toEqual({ q1: "sqlite" });
  });

  it("trims only the edges, leaving the operator's own inner spacing alone", () => {
    const body = buildDecisionResolveCommand(modelFrom(pendingPlanEntry()), "approve", GOOD_NONCE, {
      q1: " the  primary store ",
    });
    expect(body?.args.answers).toEqual({ q1: "the  primary store" });
  });

  it("refuses the whole body for a reason above, answers or no answers", () => {
    const resolved = modelFrom({ ...pendingPlanEntry(), status: "resolved" });
    expect(buildDecisionResolveCommand(resolved, "approve", GOOD_NONCE, { q1: "sqlite" })).toBeNull();
    expect(
      buildDecisionResolveCommand(modelFrom(pendingPlanEntry()), "  ", GOOD_NONCE, { q1: "sqlite" }),
    ).toBeNull();
  });
});
