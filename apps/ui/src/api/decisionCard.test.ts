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

/** The two outcome fields an answer carries when its card has NO triple. Spread
 *  into the expectations below so an evidence-free card still asserts the exact
 *  shape T003a added rather than quietly ignoring the new fields. */
const NO_OUTCOME = { expectedOutcome: "", downside: "" };

/** The sentence the model shows for a card whose `evidence_status` is anything
 *  but `present`, including a card that sends no status at all. Asserted as a
 *  value rather than pattern-matched, so a reword of it is a visible change. */
const NOTE_WITHOUT_RECEIPTS = "Recorded before receipts were required.";

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
      { kind: "option", label: "retry", value: "retry", posts: false, ...NO_OUTCOME },
      { kind: "option", label: "skip", value: "skip", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("offers the next actions as commands when the payload names no options", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      next_actions: ["remedy resume", "remedy abort"],
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "command", label: "remedy resume", value: "remedy resume", posts: false, ...NO_OUTCOME },
      { kind: "command", label: "remedy abort", value: "remedy abort", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("falls back to a single free-text answer when the card names neither", () => {
    expect(decisionAnswers({ type: "task_decision" })).toEqual([
      { kind: "free_text", label: "Answer", value: "", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("falls through an options key that is present but empty", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      payload: { options: [] },
      next_actions: ["remedy resume"],
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "command", label: "remedy resume", value: "remedy resume", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("falls through a missing payload without throwing", () => {
    expect(() => decisionAnswers({ type: "task_decision" })).not.toThrow();
    expect(decisionAnswers({ type: "task_decision", payload: null })).toEqual([
      { kind: "free_text", label: "Answer", value: "", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("renders a non-string option rather than dropping the question", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      payload: { options: [7, true] },
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "option", label: "7", value: "7", posts: false, ...NO_OUTCOME },
      { kind: "option", label: "true", value: "true", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("renders a NOVEL decision type generically, from its payload alone", () => {
    const card: DecisionInboxEntry = {
      type: NOVEL_TYPE,
      safe_summary: "Realign the warp core before the next burn",
      payload: { options: ["realign now", "defer one cycle"] },
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "option", label: "realign now", value: "realign now", posts: false, ...NO_OUTCOME },
      { kind: "option", label: "defer one cycle", value: "defer one cycle", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("stamps posts TRUE on EVERY answer when the endpoint says the door can answer", () => {
    const card: DecisionInboxEntry = {
      type: "task_decision",
      payload: { options: ["keep first", "keep second"] },
      answerable_by_decision_resolve: true,
    };
    const answers = decisionAnswers(card);
    expect(answers).toHaveLength(2);
    expect(answers.map((answer) => answer.posts)).toEqual([true, true]);
  });

  it("stamps posts FALSE on EVERY answer when the endpoint says the door would refuse", () => {
    const card: DecisionInboxEntry = {
      type: NOVEL_TYPE,
      next_actions: ["remedy resume", "remedy abort"],
      answerable_by_decision_resolve: false,
    };
    const answers = decisionAnswers(card);
    expect(answers).toHaveLength(2);
    expect(answers.map((answer) => answer.posts)).toEqual([false, false]);
  });

  it("stamps posts FALSE when the key is ABSENT, so an older server posts nothing", () => {
    // The reading is strict `=== true`. A server older than R43 sends no such
    // key at all, and `undefined` must not be read as permission to post.
    const card: DecisionInboxEntry = { type: "task_decision" };
    expect(card.answerable_by_decision_resolve).toBeUndefined();
    expect(decisionAnswers(card).map((answer) => answer.posts)).toEqual([false]);
  });

  it("stamps posts FALSE on the free-text fallback too, which has no payload to read", () => {
    const answers = decisionAnswers({ type: NOVEL_TYPE, answerable_by_decision_resolve: false });
    expect(answers).toEqual([
      { kind: "free_text", label: "Answer", value: "", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("gives two cards that differ ONLY in type identical answers", () => {
    const payload = { options: ["approve", "reject"] };
    const known: DecisionInboxEntry = { type: "task_decision", payload };
    const novel: DecisionInboxEntry = { type: NOVEL_TYPE, payload };
    expect(decisionAnswers(novel)).toEqual(decisionAnswers(known));
    expect(decisionAnswers(novel)).toHaveLength(2);
  });

  it("offers approve and reject as POSTABLE answers for a pending flight plan", () => {
    // The endpoint's own shape for a PENDING `fp:approval` card once DECISION
    // F031 D24 landed: `payload.options` carries the two words the write door
    // accepts by strict equality, and the server has already decided the door
    // would take them. No DOM harness reaches the inbox component, so this is
    // the only evidence available that the browser half of the approval works.
    const card: DecisionInboxEntry = {
      type: "flight_plan_approval",
      payload: { options: ["approve", "reject"] },
      answerable_by_decision_resolve: true,
    };
    expect(decisionAnswers(card)).toEqual([
      { kind: "option", label: "approve", value: "approve", posts: true, ...NO_OUTCOME },
      { kind: "option", label: "reject", value: "reject", posts: true, ...NO_OUTCOME },
    ]);
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
      payload: { options: ["keep first", "keep second"], task_id: "T-7" },
      age_seconds: 7320,
      blocked_count: 3,
    };
    expect(buildDecisionCardModel(card)).toEqual({
      id: "d-1",
      taskId: "T-7",
      type: "task_decision",
      status: "open",
      severity: "blocker",
      title: "Two migrations claim the same table",
      ageLabel: "2h",
      ageSeconds: 7320,
      blockedLabel: "blocks 3 tasks",
      blockedCount: 3,
      isOpen: true,
      answerableByDecisionResolve: false,
      answers: [
        { kind: "option", label: "keep first", value: "keep first", posts: false, ...NO_OUTCOME },
        { kind: "option", label: "keep second", value: "keep second", posts: false, ...NO_OUTCOME },
      ],
      clarifications: [],
      evidenceRefs: [],
      evidenceNote: NOTE_WITHOUT_RECEIPTS,
    });
  });

  it("projects the task the decision is about from the payload's own key", () => {
    const card: DecisionInboxEntry = {
      id: "d-2",
      payload: { task_id: "T-4" },
    };
    expect(buildDecisionCardModel(card).taskId).toBe("T-4");
  });

  it("gives the empty task id for a card carrying no payload at all", () => {
    expect(buildDecisionCardModel({ id: "d-3" }).taskId).toBe("");
  });

  it("gives the empty task id for a payload that is not an object", () => {
    expect(buildDecisionCardModel({ id: "d-4", payload: "T-4" }).taskId).toBe("");
    expect(buildDecisionCardModel({ id: "d-5", payload: null }).taskId).toBe("");
  });

  it("gives the empty task id for a non-string task_id rather than a number", () => {
    // A producer sending 7 would otherwise put a number where every consumer
    // expects a string; the resolver must see an id it can compare.
    expect(buildDecisionCardModel({ id: "d-6", payload: { task_id: 7 } }).taskId).toBe("");
  });

  it("projects the endpoint's answerability key under its camel-case name", () => {
    const model = buildDecisionCardModel({ id: "d-7", answerable_by_decision_resolve: true });
    expect(model.answerableByDecisionResolve).toBe(true);
    expect(model.answers.every((answer) => answer.posts)).toBe(true);
  });

  it("reads an ABSENT answerability key as false rather than as unknown", () => {
    const model = buildDecisionCardModel({ id: "d-8" });
    expect(model.answerableByDecisionResolve).toBe(false);
    expect(model.answers.every((answer) => answer.posts)).toBe(false);
  });

  it("does not treat a resolved decision as open", () => {
    expect(buildDecisionCardModel({ status: "resolved" }).isOpen).toBe(false);
  });

  it("renders a card with every optional field absent without throwing", () => {
    expect(() => buildDecisionCardModel({})).not.toThrow();
    expect(buildDecisionCardModel({})).toEqual({
      id: "",
      taskId: "",
      type: "",
      status: "",
      severity: "",
      title: "",
      ageLabel: "unknown age",
      ageSeconds: null,
      blockedLabel: "blocks nothing",
      blockedCount: 0,
      isOpen: false,
      answerableByDecisionResolve: false,
      answers: [{ kind: "free_text", label: "Answer", value: "", posts: false, ...NO_OUTCOME }],
      clarifications: [],
      evidenceRefs: [],
      evidenceNote: NOTE_WITHOUT_RECEIPTS,
    });
  });
});

describe("buildDecisionCardModel clarifications", () => {
  /** The endpoint's OWN shape for a pending `fp:approval` card carrying open
   *  questions: `decision_queue.py` writes `open_clarification_questions`'
   *  records straight into `payload.clarifications`, and every one of them has
   *  exactly the four snake-case keys asserted here. */
  function pendingPlanEntry(): DecisionInboxEntry {
    return {
      id: "fp:approval",
      type: "flight_plan_approval",
      status: "open",
      severity: "blocker",
      safe_summary: "Flight plan awaiting approval (2 open questions).",
      payload: {
        options: ["approve", "reject"],
        clarifications: [
          {
            id: "q1",
            question: "Which database backs the export?",
            default_answer: "postgres",
            impact: "Chooses the migration path",
          },
          {
            id: "q2",
            question: "Ship behind a flag?",
            default_answer: "yes",
            impact: "Decides the rollout",
          },
        ],
      },
      answerable_by_decision_resolve: true,
    };
  }

  it("projects every open question into the model's own camel case", () => {
    expect(buildDecisionCardModel(pendingPlanEntry()).clarifications).toEqual([
      {
        id: "q1",
        question: "Which database backs the export?",
        defaultAnswer: "postgres",
        impact: "Chooses the migration path",
      },
      {
        id: "q2",
        question: "Ship behind a flag?",
        defaultAnswer: "yes",
        impact: "Decides the rollout",
      },
    ]);
  });

  it("preserves the order the plan asked its questions in", () => {
    const ids = buildDecisionCardModel(pendingPlanEntry()).clarifications.map((q) => q.id);
    expect(ids).toEqual(["q1", "q2"]);
  });

  it("gives no clarifications for a card carrying no payload at all", () => {
    expect(buildDecisionCardModel({ id: "d-9" }).clarifications).toEqual([]);
  });

  it("gives no clarifications for a null payload", () => {
    expect(buildDecisionCardModel({ id: "d-10", payload: null }).clarifications).toEqual([]);
  });

  it("gives no clarifications for a payload that is not an object", () => {
    expect(buildDecisionCardModel({ id: "d-11", payload: "q1" }).clarifications).toEqual([]);
    expect(buildDecisionCardModel({ id: "d-12", payload: 7 }).clarifications).toEqual([]);
  });

  it("gives no clarifications when the key is present but not an array", () => {
    const card: DecisionInboxEntry = { id: "d-13", payload: { clarifications: "q1" } };
    expect(() => buildDecisionCardModel(card)).not.toThrow();
    expect(buildDecisionCardModel(card).clarifications).toEqual([]);
  });

  it("drops a non-object entry rather than throwing on it", () => {
    const card: DecisionInboxEntry = {
      id: "d-14",
      payload: { clarifications: [7, null, "q1", { id: "q2", question: "Real?" }] },
    };
    expect(buildDecisionCardModel(card).clarifications).toEqual([
      { id: "q2", question: "Real?", defaultAnswer: "", impact: "" },
    ]);
  });

  it("falls back to the empty string for a non-string field rather than raising", () => {
    const card: DecisionInboxEntry = {
      id: "d-15",
      payload: { clarifications: [{ id: "q1", question: 7, default_answer: null, impact: true }] },
    };
    expect(buildDecisionCardModel(card).clarifications).toEqual([
      { id: "q1", question: "", defaultAnswer: "", impact: "" },
    ]);
  });

  it("DROPS an entry whose id is blank after trimming, keeping the answerable ones", () => {
    // An id the write door cannot know refuses the WHOLE post, so a field the
    // operator can fill but never submit would cost them every other answer.
    const card: DecisionInboxEntry = {
      id: "d-16",
      payload: {
        clarifications: [
          { id: "", question: "No id at all" },
          { id: "   ", question: "Whitespace only" },
          { id: "q3", question: "Answerable" },
        ],
      },
    };
    expect(buildDecisionCardModel(card).clarifications).toEqual([
      { id: "q3", question: "Answerable", defaultAnswer: "", impact: "" },
    ]);
  });

  it("makes no payload throw, clarifications included", () => {
    expect(() => buildDecisionCardModel({ payload: { clarifications: [[], {}, 0] } })).not.toThrow();
    expect(buildDecisionCardModel({ payload: { clarifications: [[], {}, 0] } }).clarifications)
      .toEqual([]);
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

/** THE EVIDENCE TRIPLE (T5_F032 T003a). Every entry below is written in the
 *  endpoint's OWN spellings, exactly as `export_decision_json` in
 *  `packages/orchestration/decision_queue.py` emits them: a ref is
 *  `{kind, target, label}`, an outcome is `{option, expected_outcome, downside}`,
 *  and an optionless decision keys its single outcome with the EMPTY STRING. */

/** The shape a producer with real options emits: one outcome per option, keyed
 *  by the option's own text. */
function twoKeyedOutcomesEntry(): DecisionInboxEntry {
  return {
    id: "d-a",
    type: "task_decision",
    payload: { options: ["retry", "skip"] },
    evidence_refs: [{ kind: "test_run", target: "tr-9", label: "Test result for the export job" }],
    outcomes: [
      {
        option: "retry",
        expected_outcome: "The export job runs again",
        downside: "Costs another ten minutes",
      },
      {
        option: "skip",
        expected_outcome: "The pipeline moves on",
        downside: "The export stays stale",
      },
    ],
    evidence_status: "present",
  };
}

/** The shape five of the eight producers emit: no options, so ONE outcome keyed
 *  with the empty string, which must reach every affordance the card offers. */
function unkeyedOutcomeEntry(): DecisionInboxEntry {
  return {
    id: "d-b",
    type: "budget_decision",
    next_actions: ["remedy resume", "remedy abort"],
    evidence_refs: [],
    outcomes: [
      {
        option: "",
        expected_outcome: "The run continues under the raised budget",
        downside: "Spends more than planned",
      },
    ],
    evidence_status: "present",
  };
}

/** A card from before F032 required receipts: no triple keys at all. */
function noTripleEntry(): DecisionInboxEntry {
  return { id: "d-c", type: "task_decision", payload: { options: ["approve", "reject"] } };
}

/** A ref that points at nothing beside one that points somewhere real. */
function blankTargetRefEntry(): DecisionInboxEntry {
  return {
    id: "d-d",
    type: "task_decision",
    payload: { options: ["approve"] },
    evidence_refs: [
      { kind: "stop_record", target: "   ", label: "Stop record that points at nothing" },
      { kind: "escalation", target: "td:1", label: "Escalation raised by the worker" },
    ],
    outcomes: [],
    evidence_status: "recorded_before_evidence_requirements",
  };
}

describe("decisionAnswers carries each option's own outcome", () => {
  it("gives each answer ITS option's expected outcome and downside", () => {
    expect(decisionAnswers(twoKeyedOutcomesEntry())).toEqual([
      {
        kind: "option",
        label: "retry",
        value: "retry",
        posts: false,
        expectedOutcome: "The export job runs again",
        downside: "Costs another ten minutes",
      },
      {
        kind: "option",
        label: "skip",
        value: "skip",
        posts: false,
        expectedOutcome: "The pipeline moves on",
        downside: "The export stays stale",
      },
    ]);
  });

  it("never pairs one option's expectation with another's downside", () => {
    // The two halves travel together, so a mismatch here is the failure the
    // model's own `DecisionOutcomeText` exists to make impossible.
    const answers = decisionAnswers(twoKeyedOutcomesEntry());
    expect(answers.map((a) => [a.value, a.expectedOutcome, a.downside])).toEqual([
      ["retry", "The export job runs again", "Costs another ten minutes"],
      ["skip", "The pipeline moves on", "The export stays stale"],
    ]);
  });

  it("applies ONE unkeyed outcome to EVERY next-action answer of the card", () => {
    const answers = decisionAnswers(unkeyedOutcomeEntry());
    expect(answers).toHaveLength(2);
    expect(answers.map((a) => a.kind)).toEqual(["command", "command"]);
    expect(answers.map((a) => a.expectedOutcome)).toEqual([
      "The run continues under the raised budget",
      "The run continues under the raised budget",
    ]);
    expect(answers.map((a) => a.downside)).toEqual([
      "Spends more than planned",
      "Spends more than planned",
    ]);
  });

  it("reaches the free-text fallback with the unkeyed outcome too", () => {
    // The fallback's `value` IS the empty string, so it matches by the same key
    // every other answer uses rather than through a special case.
    const answers = decisionAnswers({
      id: "d-e",
      type: NOVEL_TYPE,
      outcomes: [{ option: "", expected_outcome: "The run resumes", downside: "Costs time" }],
    });
    expect(answers).toEqual([
      {
        kind: "free_text",
        label: "Answer",
        value: "",
        posts: false,
        expectedOutcome: "The run resumes",
        downside: "Costs time",
      },
    ]);
  });

  it("gives every answer two EMPTY STRINGS for a card carrying no triple", () => {
    const answers = decisionAnswers(noTripleEntry());
    expect(answers).toHaveLength(2);
    expect(answers.map((a) => a.expectedOutcome)).toEqual(["", ""]);
    expect(answers.map((a) => a.downside)).toEqual(["", ""]);
  });

  it("leaves both fields EMPTY when no outcome key matches any option", () => {
    // Keys that match nothing must not fall back to the first outcome: showing
    // the wrong expectation is worse than showing none.
    const answers = decisionAnswers({
      id: "d-f",
      type: "task_decision",
      payload: { options: ["approve", "reject"] },
      outcomes: [
        { option: "retry", expected_outcome: "Runs again", downside: "Costs time" },
        { option: "skip", expected_outcome: "Moves on", downside: "Stays stale" },
      ],
    });
    expect(answers.map((a) => [a.expectedOutcome, a.downside])).toEqual([
      ["", ""],
      ["", ""],
    ]);
  });

  it("still refuses to branch on the decision's TYPE, outcomes included", () => {
    // The same measurement the suite already makes for `posts`: two cards that
    // differ ONLY in type must answer identically, triple and all.
    const shared = {
      payload: { options: ["retry", "skip"] },
      outcomes: [
        { option: "retry", expected_outcome: "Runs again", downside: "Costs time" },
        { option: "skip", expected_outcome: "Moves on", downside: "Stays stale" },
      ],
      evidence_status: "present",
    };
    const known: DecisionInboxEntry = { type: "task_decision", ...shared };
    const novel: DecisionInboxEntry = { type: NOVEL_TYPE, ...shared };
    expect(decisionAnswers(novel)).toEqual(decisionAnswers(known));
    expect(decisionAnswers(novel)[0].expectedOutcome).toBe("Runs again");
  });
});

describe("buildDecisionCardModel evidence refs", () => {
  it("projects a ref's kind, target and scrubbed label", () => {
    expect(buildDecisionCardModel(twoKeyedOutcomesEntry()).evidenceRefs).toEqual([
      { kind: "test_run", target: "tr-9", label: "Test result for the export job" },
    ]);
  });

  it("DROPS a ref whose target is blank after trimming, keeping the followable one", () => {
    // A chip that points at nothing cannot be followed, and the deep link the
    // next round adds would have nothing to open.
    expect(buildDecisionCardModel(blankTargetRefEntry()).evidenceRefs).toEqual([
      { kind: "escalation", target: "td:1", label: "Escalation raised by the worker" },
    ]);
  });

  it("shows the fallback for a label that is a bare hex id, and NOT the id itself", () => {
    // §17 of the UX spec forbids the default UI to show a raw id, and
    // `scrubUiText` already rejects one. Losing the receipt entirely would be
    // worse than showing a generic word, so the ref survives with the fallback.
    const rawId = "a3f9c2e1b4d7";
    const model = buildDecisionCardModel({
      id: "d-g",
      evidence_refs: [{ kind: "test_run", target: "tr-1", label: rawId }],
    });
    expect(model.evidenceRefs).toHaveLength(1);
    expect(model.evidenceRefs[0].label).toBe("Receipt");
    expect(model.evidenceRefs[0].label).not.toBe(rawId);
    expect(model.evidenceRefs[0].label).not.toContain(rawId);
    // The target is still CARRIED for the next round's link, just never shown.
    expect(model.evidenceRefs[0].target).toBe("tr-1");
  });

  it("gives no refs for a card carrying no triple at all", () => {
    expect(buildDecisionCardModel(noTripleEntry()).evidenceRefs).toEqual([]);
  });

  it("gives no refs for an evidence_refs that is not an array", () => {
    expect(buildDecisionCardModel({ id: "d-h", evidence_refs: "tr-1" }).evidenceRefs).toEqual([]);
    expect(buildDecisionCardModel({ id: "d-i", evidence_refs: null }).evidenceRefs).toEqual([]);
  });

  it("skips a non-object ref entry rather than throwing on it", () => {
    const model = buildDecisionCardModel({
      id: "d-j",
      evidence_refs: [7, null, "tr-1", { kind: "test_run", target: "tr-2", label: "A test" }],
    });
    expect(model.evidenceRefs).toEqual([{ kind: "test_run", target: "tr-2", label: "A test" }]);
  });

  it("falls back on a non-string ref field rather than raising", () => {
    const model = buildDecisionCardModel({
      id: "d-k",
      evidence_refs: [{ kind: 7, target: "tr-3", label: null }],
    });
    expect(model.evidenceRefs).toEqual([{ kind: "", target: "tr-3", label: "Receipt" }]);
  });
});

describe("buildDecisionCardModel evidence note", () => {
  it("says NOTHING when the card really carries its receipts", () => {
    expect(buildDecisionCardModel(twoKeyedOutcomesEntry()).evidenceNote).toBe("");
  });

  it("says so in words for a record written before the requirement", () => {
    const model = buildDecisionCardModel({
      id: "d-l",
      evidence_status: "recorded_before_evidence_requirements",
    });
    expect(model.evidenceNote).toBe(NOTE_WITHOUT_RECEIPTS);
  });

  it("says the same for a card sending no status key at all", () => {
    expect(buildDecisionCardModel({ id: "d-m" }).evidenceNote).toBe(NOTE_WITHOUT_RECEIPTS);
  });

  it("never puts a raw status constant in the text a renderer shows", () => {
    // The status IS the present/missing signal §17 forbids, so neither constant
    // may appear in the note and the raw string must not reach the model.
    const legacy = buildDecisionCardModel({
      id: "d-n",
      evidence_status: "recorded_before_evidence_requirements",
    });
    expect(legacy.evidenceNote).not.toContain("recorded_before_evidence_requirements");
    expect(legacy.evidenceNote).not.toContain("present");
    expect(Object.values(legacy)).not.toContain("recorded_before_evidence_requirements");
  });
});

describe("buildDecisionCardModel stays total with a malformed triple", () => {
  it("returns a model rather than throwing on a non-array evidence_refs", () => {
    expect(() => buildDecisionCardModel({ id: "d-o", evidence_refs: 7 })).not.toThrow();
    expect(buildDecisionCardModel({ id: "d-o", evidence_refs: 7 }).id).toBe("d-o");
  });

  it("returns a model rather than throwing on a non-array outcomes", () => {
    const card: DecisionInboxEntry = { id: "d-p", outcomes: "retry" };
    expect(() => buildDecisionCardModel(card)).not.toThrow();
    expect(buildDecisionCardModel(card).answers.map((a) => a.expectedOutcome)).toEqual([""]);
  });

  it("returns a model rather than throwing on a non-object ref entry", () => {
    const card: DecisionInboxEntry = { id: "d-q", evidence_refs: [[], {}, 0, null] };
    expect(() => buildDecisionCardModel(card)).not.toThrow();
    expect(buildDecisionCardModel(card).evidenceRefs).toEqual([]);
  });

  it("returns a model rather than throwing on a null payload beside a triple", () => {
    const card: DecisionInboxEntry = {
      id: "d-r",
      payload: null,
      evidence_refs: null,
      outcomes: null,
      evidence_status: null,
    };
    expect(() => buildDecisionCardModel(card)).not.toThrow();
    expect(buildDecisionCardModel(card).evidenceRefs).toEqual([]);
    expect(buildDecisionCardModel(card).evidenceNote).toBe(NOTE_WITHOUT_RECEIPTS);
    expect(buildDecisionCardModel(card).answers).toEqual([
      { kind: "free_text", label: "Answer", value: "", posts: false, ...NO_OUTCOME },
    ]);
  });

  it("returns a model rather than throwing on a non-object outcome entry", () => {
    const card: DecisionInboxEntry = {
      id: "d-s",
      payload: { options: ["retry"] },
      outcomes: [7, null, "retry", { option: "retry", expected_outcome: "Runs", downside: "Slow" }],
    };
    expect(() => buildDecisionCardModel(card)).not.toThrow();
    expect(buildDecisionCardModel(card).answers[0].expectedOutcome).toBe("Runs");
  });
});

describe("the T003a read-back the block's G6 orders", () => {
  /** The four cards G6 names, reported as the tuples it asks for. These are
   *  ASSERTED here rather than only printed, so the reported read-back is a
   *  measurement the suite re-runs rather than a transcript anyone must trust. */
  function readBack(entry: DecisionInboxEntry) {
    const model = buildDecisionCardModel(entry);
    return {
      answers: model.answers.map((a) => [a.kind, a.value, a.expectedOutcome, a.downside]),
      evidenceRefs: model.evidenceRefs.map((r) => [r.kind, r.target, r.label]),
      evidenceNote: model.evidenceNote,
    };
  }

  it("reports a two-option card with two keyed outcomes", () => {
    expect(readBack(twoKeyedOutcomesEntry())).toEqual({
      answers: [
        ["option", "retry", "The export job runs again", "Costs another ten minutes"],
        ["option", "skip", "The pipeline moves on", "The export stays stale"],
      ],
      evidenceRefs: [["test_run", "tr-9", "Test result for the export job"]],
      evidenceNote: "",
    });
  });

  it("reports a card with one unkeyed outcome and two next actions", () => {
    expect(readBack(unkeyedOutcomeEntry())).toEqual({
      answers: [
        [
          "command",
          "remedy resume",
          "The run continues under the raised budget",
          "Spends more than planned",
        ],
        [
          "command",
          "remedy abort",
          "The run continues under the raised budget",
          "Spends more than planned",
        ],
      ],
      evidenceRefs: [],
      evidenceNote: "",
    });
  });

  it("reports a card with no triple at all", () => {
    expect(readBack(noTripleEntry())).toEqual({
      answers: [
        ["option", "approve", "", ""],
        ["option", "reject", "", ""],
      ],
      evidenceRefs: [],
      evidenceNote: NOTE_WITHOUT_RECEIPTS,
    });
  });

  it("reports a card carrying a blank-target ref beside a valid one", () => {
    expect(readBack(blankTargetRefEntry())).toEqual({
      answers: [["option", "approve", "", ""]],
      evidenceRefs: [["escalation", "td:1", "Escalation raised by the worker"]],
      evidenceNote: NOTE_WITHOUT_RECEIPTS,
    });
  });
});
