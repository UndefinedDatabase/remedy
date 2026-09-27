import { describe, expect, it } from "vitest";
import {
  INJECTED_TASK_ORIGIN,
  ORIGIN_CANVAS_CHIP_TEXT,
  ORIGIN_CHIP_TEXT,
  ORIGIN_CHIP_TITLE,
  injectDraftView,
  taskOriginChip,
} from "./injectView";

describe("taskOriginChip", () => {
  it("answers the words for a task whose origin is human_injected", () => {
    expect(taskOriginChip({ origin: INJECTED_TASK_ORIGIN })).toBe(ORIGIN_CHIP_TEXT);
    expect(taskOriginChip({ origin: "human_injected" })).toBe("Added by you");
  });

  it("is null for a task with no origin at all", () => {
    expect(taskOriginChip({})).toBeNull();
  });

  it("is null for a task whose origin is the empty string", () => {
    expect(taskOriginChip({ origin: "" })).toBeNull();
  });

  it("is null for a task with any other origin", () => {
    expect(taskOriginChip({ origin: "planner" })).toBeNull();
  });

  it("is null for a null or undefined task", () => {
    expect(taskOriginChip(null)).toBeNull();
    expect(taskOriginChip(undefined)).toBeNull();
  });

  it("the title names the one sentence both mounts share", () => {
    expect(ORIGIN_CHIP_TITLE).toBe("You added this task while the job was running.");
  });
});

describe("ORIGIN_CANVAS_CHIP_TEXT", () => {
  it("is the short word the canvas chip carries", () => {
    expect(ORIGIN_CANVAS_CHIP_TEXT).toBe("added");
  });
});

// DECISION F028 D7 (2) — `injectDraftView` over the wire body
// `task_injection.draft_task_injection` and `answer_injection_shortfall`
// actually answer.
describe("injectDraftView", () => {
  const draftedBody = {
    outcome: "drafted",
    job_id: "job-1",
    draft_id: "d1",
    confirm_token: "d1",
    task: {
      id: "INJ1",
      title: "Add rate limiting",
      goal: "Prevent abuse of the endpoint",
      acceptance: ["A test hits the endpoint 100 times and gets throttled"],
      est_tokens_band: "M",
      files_hint: ["packages/api/limits.py"],
    },
    placement: {
      basis: "frontier_default",
      rationale: "placed at the end of the plan with no dependency, because no planned task touches its files",
    },
    task_rationale: "This adds guardrails.",
    budget_check: {
      plan_band: "M",
      shortfall: false,
      arithmetic: "spent $1.00 + expected $0.50 = $1.50, under the $5.00 limit",
    },
    decision_seed: null,
    fence_conflicts: [{ path: "secrets/prod.env", rule: "deny", glob: "secrets/**" }],
    drafted_at: "2026-09-27T11:00:00+00:00",
    expires_at: "2026-09-27T11:15:00+00:00",
    planner_calls: 1,
    text: "add rate limiting",
    budget_extend_to_usd: null,
  };

  it("reads a drafted body into its sentences and lists", () => {
    expect(injectDraftView(draftedBody)).toEqual({
      kind: "drafted",
      draftId: "d1",
      confirmToken: "d1",
      title: "Add rate limiting",
      goal: "Prevent abuse of the endpoint",
      acceptance: ["A test hits the endpoint 100 times and gets throttled"],
      size: "Size: M.",
      placement: "Placed at the end of the plan with no dependency, because no planned task touches its files.",
      cost: "Cost check: spent $1.00 + expected $0.50 = $1.50, under the $5.00 limit.",
      fenceWarnings: ["secrets/prod.env is outside what this job may change."],
      expiresAt: "2026-09-27T11:15:00+00:00",
      question: "",
      options: [],
    });
  });

  const shortfallBody = {
    outcome: "shortfall",
    draft_id: "d2",
    confirm_token: null,
    task: { title: "Big task", goal: "Do a lot", acceptance: ["x"], est_tokens_band: "L" },
    placement: { basis: "stated", rationale: "placed after INJ1 because you named it" },
    task_rationale: "It is large.",
    budget_check: { arithmetic: "spent $4.00 + expected $2.00 = $6.00, over the $5.00 limit" },
    decision_seed: {
      question: "Adding this task would go over the job's cost limit. What should happen?",
      options: ["extend_budget", "shrink_task", "drop"],
      option_labels: {
        extend_budget: "Raise the job's cost limit to $6.00 and add the task.",
        shrink_task: "Draft the task again one size smaller, as size M, and check the cost again.",
        drop: "Drop this task and add nothing to the job.",
      },
    },
    fence_conflicts: [],
    expires_at: "2026-09-27T11:20:00+00:00",
  };

  it("reads a shortfall body's question and options in the seed's own order, with a null confirmToken", () => {
    expect(injectDraftView(shortfallBody)).toEqual({
      kind: "shortfall",
      draftId: "d2",
      confirmToken: null,
      title: "Big task",
      goal: "Do a lot",
      acceptance: ["x"],
      size: "Size: L.",
      placement: "Placed after INJ1 because you named it.",
      cost: "Cost check: spent $4.00 + expected $2.00 = $6.00, over the $5.00 limit.",
      fenceWarnings: [],
      expiresAt: "2026-09-27T11:20:00+00:00",
      question: "Adding this task would go over the job's cost limit. What should happen?",
      options: [
        { option: "extend_budget", label: "Raise the job's cost limit to $6.00 and add the task." },
        { option: "shrink_task", label: "Draft the task again one size smaller, as size M, and check the cost again." },
        { option: "drop", label: "Drop this task and add nothing to the job." },
      ],
    });
  });

  it("reads a derived draft (extra derived_from/answer keys) exactly as a fresh draft", () => {
    const derived = { ...draftedBody, draft_id: "d3", confirm_token: "d3", derived_from: "d2", answer: "extend_budget" };
    const view = injectDraftView(derived);
    expect(view?.kind).toBe("drafted");
    expect(view?.draftId).toBe("d3");
    expect(view?.confirmToken).toBe("d3");
  });

  it("is null for an outcome of confirmed", () => {
    expect(injectDraftView({ outcome: "confirmed", draft_id: "d1" })).toBeNull();
  });

  it("is null for null", () => {
    expect(injectDraftView(null)).toBeNull();
  });

  it("reads a body with every field missing as empty strings and empty lists, never an exception", () => {
    expect(injectDraftView({ outcome: "drafted" })).toEqual({
      kind: "drafted",
      draftId: "",
      confirmToken: "",
      title: "",
      goal: "",
      acceptance: [],
      size: "",
      placement: "",
      cost: "",
      fenceWarnings: [],
      expiresAt: "",
      question: "",
      options: [],
    });
  });
});
