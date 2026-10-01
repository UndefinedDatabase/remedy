// T5_F292 T002 — the rules of the plan view's edit controls (DECISION F292 D3).
import { describe, expect, it } from "vitest";
import {
  PLAN_TOKEN_BANDS,
  changedPlanTaskFields,
  planCriterionProblem,
  planCriterionRemoveBlocked,
  planDeleteQuestion,
  planEditBlockedReason,
  planMergeBlocked,
  planMergeIds,
  planMergeSummary,
  planMove,
  planSplitBlocked,
  planSplitDefaultParts,
  planSplitPartition,
  planSplitSummary,
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

describe("the criteria rules (DECISION F292 D4)", () => {
  it("an empty criterion cannot be sent", () => {
    expect(planCriterionProblem("   ")).toBe("Write the criterion.");
    expect(planCriterionProblem(" reads a file ")).toBeNull();
  });
  it("a task keeps at least one criterion", () => {
    expect(planCriterionRemoveBlocked(task("T1"))).toBe("A task keeps at least one criterion.");
    expect(planCriterionRemoveBlocked(task("T1", [], { acceptance: ["a", "b"] }))).toBeNull();
  });
});

describe("planMove (DECISION F292 D4)", () => {
  const free = plan({ tasks: [task("A"), task("B"), task("C")] });

  it("swaps a task with its neighbour and answers the whole order", () => {
    expect(planMove(free, "B", -1)).toEqual({ order: ["B", "A", "C"] });
    expect(planMove(free, "B", 1)).toEqual({ order: ["A", "C", "B"] });
  });
  it("says a task at an end is already there", () => {
    expect(planMove(free, "A", -1)).toEqual({ blocked: "A is already first." });
    expect(planMove(free, "C", 1)).toEqual({ blocked: "C is already last." });
  });
  it("never moves a task before one it waits for", () => {
    expect(planMove(plan(), "T2", -1)).toEqual({ blocked: "T2 waits for T1, so it cannot come before it." });
  });
  it("never moves a task after one that waits for it", () => {
    expect(planMove(plan(), "T2", 1)).toEqual({ blocked: "T3 waits for T2, so T2 cannot come after it." });
  });
  it("moves past a neighbour that is not tied to it", () => {
    const p = plan({ tasks: [task("T1"), task("X"), task("T2", ["T1"])] });
    expect(planMove(p, "X", 1)).toEqual({ order: ["T1", "T2", "X"] });
    expect(planMove(p, "T2", -1)).toEqual({ order: ["T1", "T2", "X"] });
  });
  it("says an unknown task is already first or last rather than moving anything", () => {
    expect(planMove(free, "Z", -1)).toEqual({ blocked: "Z is already first." });
  });
});

describe("the merge rules (DECISION F292 D5)", () => {
  const four = plan({ tasks: [task("T1"), task("T2", ["T1"]), task("T3", ["T2", "T1"]), task("T4", ["T3"], { acceptance: ["a", "b"] })] });

  it("needs a second task", () => {
    expect(planMergeBlocked(plan({ tasks: [task("T1")] }))).toBe("There is no other task to merge with.");
    expect(planMergeBlocked(four)).toBeNull();
  });
  it("names the merged tasks in plan order, whatever order they were chosen in", () => {
    expect(planMergeIds(four, "T3", ["T4", "T1"])).toEqual(["T1", "T3", "T4"]);
    expect(planMergeIds(four, "T2", [])).toEqual(["T2"]);
  });
  it("asks for a second task before it says anything", () => {
    expect(planMergeSummary(four, ["T2"])).toEqual({ problem: "Choose at least one task to merge with." });
  });
  it("says the tasks become the first, with every criterion, and who will wait for it instead", () => {
    expect(planMergeSummary(four, ["T3", "T4"])).toEqual({ text: "T3 and T4 become one task, T3, with all 3 of their criteria." });
    expect(planMergeSummary(four, ["T1", "T3"])).toEqual(
      { text: "T1 and T3 become one task, T1, with all 2 of their criteria. T4 will wait for T1 instead." });
  });
  it("leaves out a task that already waits for the first", () => {
    expect(planMergeSummary(four, ["T2", "T3"])).toEqual(
      { text: "T2 and T3 become one task, T2, with all 2 of their criteria. T4 will wait for T2 instead." });
  });
});

describe("the split rules (DECISION F292 D5)", () => {
  const p = plan({ tasks: [task("T1"), task("T2", ["T1"], { acceptance: ["a", "b", "c"] }), task("T3", ["T2"])] });

  it("needs two criteria", () => {
    expect(planSplitBlocked(task("T1"))).toBe("A task with one criterion cannot be split.");
    expect(planSplitBlocked(p.tasks[1])).toBeNull();
  });
  it("starts with the last criterion in a second part", () => {
    expect(planSplitDefaultParts(p.tasks[1])).toEqual([1, 1, 2]);
  });
  it("gives one group per part that holds a criterion, in part order", () => {
    expect(planSplitPartition([1, 1, 2])).toEqual([[0, 1], [2]]);
    expect(planSplitPartition([3, 1, 3])).toEqual([[1], [0, 2]]);
    expect(planSplitPartition([2, 2, 2])).toEqual([[0, 1, 2]]);
  });
  it("asks for two parts before it says anything", () => {
    expect(planSplitSummary(p, p.tasks[1], [[0, 1, 2]])).toEqual({ problem: "Put the criteria into at least two parts." });
  });
  it("says how many tasks run one after the other, and who will wait for the last part", () => {
    expect(planSplitSummary(p, p.tasks[1], [[0, 1], [2]])).toEqual(
      { text: "T2 becomes 2 tasks run one after the other, each with its part of the criteria. T3 will wait for the last part." });
    expect(planSplitSummary(p, p.tasks[2], [[0], [1], [2]])).toEqual(
      { text: "T3 becomes 3 tasks run one after the other, each with its part of the criteria." });
  });
});
