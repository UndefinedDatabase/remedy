// T5_F292 T002 — the rules of the plan view's edit controls (DECISION F292 D3).
import { describe, expect, it } from "vitest";
import {
  PLAN_TOKEN_BANDS,
  changedPlanTaskFields,
  planDeleteQuestion,
  planEditBlockedReason,
  planTaskDraftOf,
  planTaskDraftProblem,
} from "./planEditView";
import type { RemedyPlan, RemedyPlanTask } from "./types";

function task(id: string, dependsOn: string[] = [], overrides: Partial<RemedyPlanTask> = {}): RemedyPlanTask {
  return {
    id, title: `Build ${id}`, goal: `goal of ${id}`, dependsOn, estTokensBand: "S", filesHint: [],
    acceptance: [`${id} works`], jobTaskId: `e-${id}`, status: "pending", specVersion: 1, ...overrides,
  };
}

function plan(overrides: Partial<RemedyPlan> = {}): RemedyPlan {
  return {
    available: true, version: 2, approval: "pending", editable: true, notEditableBecause: "",
    tasks: [task("T1"), task("T2", ["T1"]), task("T3", ["T2", "T1"])], error: "", ...overrides,
  };
}

const IDLE = { sending: false, awaitingVersion: null };

describe("planEditBlockedReason", () => {
  it("is null while the plan is open and nothing is in flight", () => {
    expect(planEditBlockedReason(plan(), IDLE)).toBeNull();
  });
  it("gives the window sentence for a closed plan", () => {
    expect(planEditBlockedReason(plan({ editable: false, notEditableBecause: "the job is running" }), IDLE))
      .toBe("Not open for editing: the job is running.");
  });
  it("is never null when there is no plan", () => {
    expect(planEditBlockedReason(plan({ available: false, editable: false, tasks: [] }), IDLE)).toBe("Not open for editing.");
  });
  it("waits while an edit is in flight", () => {
    expect(planEditBlockedReason(plan(), { sending: true, awaitingVersion: null })).toBe("An edit is being saved.");
  });
  it("waits until the version an accepted edit landed as has arrived, and no longer", () => {
    expect(planEditBlockedReason(plan({ version: 2 }), { sending: false, awaitingVersion: 3 }))
      .toBe("Waiting for version 3 of the plan to arrive.");
    expect(planEditBlockedReason(plan({ version: 3 }), { sending: false, awaitingVersion: 3 })).toBeNull();
    expect(planEditBlockedReason(plan({ version: 4 }), { sending: false, awaitingVersion: 3 })).toBeNull();
  });
});

describe("the task edit form's rules", () => {
  it("the sizes are the planner's four bands in order", () => {
    expect(PLAN_TOKEN_BANDS).toEqual(["S", "M", "L", "XL"]);
  });
  it("a draft starts from the task as shown", () => {
    expect(planTaskDraftOf(task("T1", [], { estTokensBand: "L" }))).toEqual({ title: "Build T1", goal: "goal of T1", band: "L" });
  });
  it.each([
    [{ title: "  ", goal: "g", band: "S" }, "Give the task a title."],
    [{ title: "t", goal: "", band: "S" }, "Give the task a goal."],
    [{ title: "t", goal: "g", band: "" }, "Choose a size."],
    [{ title: "t", goal: "g", band: "XXL" }, "Choose a size."],
    [{ title: "t", goal: "g", band: "XL" }, null],
  ])("the draft %j reads %j", (draft, problem) => {
    expect(planTaskDraftProblem(draft)).toBe(problem);
  });
  it("sends only what changed, trimmed", () => {
    const t = task("T1");
    expect(changedPlanTaskFields(t, { title: " Build T1 ", goal: "goal of T1", band: "S" })).toEqual({});
    expect(changedPlanTaskFields(t, { title: " Parse ", goal: "goal of T1", band: "S" })).toEqual({ title: "Parse" });
    expect(changedPlanTaskFields(t, { title: "Build T1", goal: "read it ", band: "M" }))
      .toEqual({ goal: "read it", est_tokens_band: "M" });
  });
});

describe("planDeleteQuestion", () => {
  it("says no task waits for a task nothing depends on", () => {
    const p = plan();
    expect(planDeleteQuestion(p, p.tasks[2])).toBe("Delete T3? No task waits for it.");
  });
  it("names the tasks that wait for it and what they will wait for instead", () => {
    const p = plan();
    expect(planDeleteQuestion(p, p.tasks[1])).toBe("Delete T2? T3 waits for it and will wait for T1 instead.");
  });
  it("says the wait is dropped when the task waited for nothing", () => {
    const p = plan();
    expect(planDeleteQuestion(p, p.tasks[0])).toBe("Delete T1? T2 and T3 wait for it; that wait will be dropped.");
  });
  it("joins three names with commas and a final and", () => {
    const p = plan({ tasks: [task("T1", ["T0"]), task("A", ["T1"]), task("B", ["T1"]), task("C", ["T1"])] });
    expect(planDeleteQuestion(p, p.tasks[0])).toBe("Delete T1? A, B and C wait for it and will wait for T0 instead.");
  });
});
