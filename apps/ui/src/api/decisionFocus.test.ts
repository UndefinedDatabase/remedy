import { describe, it, expect } from "vitest";
import { nodeIdForDecisionCard } from "./decisionFocus";
import { buildDecisionCardModel } from "./decisionCard";

const TASKS = [
  { id: "T-1", nodeId: "node-T-1" },
  { id: "T-2", nodeId: "node-T-2" },
];

describe("nodeIdForDecisionCard", () => {
  it("resolves a decision to the node of the task it is about", () => {
    const model = buildDecisionCardModel({ id: "d-1", payload: { task_id: "T-2" } });
    expect(nodeIdForDecisionCard(model, TASKS)).toBe("node-T-2");
  });

  it("returns null when the linkage names a task the dashboard lacks", () => {
    // The inbox and the dashboard are two reads of one job and can disagree for
    // a moment. A stale id must not jump to the wrong node.
    const model = buildDecisionCardModel({ id: "d-1", payload: { task_id: "T-9" } });
    expect(nodeIdForDecisionCard(model, TASKS)).toBeNull();
  });

  it("returns null for a decision that carries no task linkage at all", () => {
    // A job-level question is the normal case here, not an error.
    const model = buildDecisionCardModel({ id: "d-1" });
    expect(model.taskId).toBe("");
    expect(nodeIdForDecisionCard(model, TASKS)).toBeNull();
  });

  it("returns null against an empty task list rather than throwing", () => {
    const model = buildDecisionCardModel({ id: "d-1", payload: { task_id: "T-1" } });
    expect(nodeIdForDecisionCard(model, [])).toBeNull();
  });

  it("reads the task id rather than the decision's own id", () => {
    // The two DIFFER here on purpose and only the task id names a task: a
    // resolver keyed on the decision's `id` would answer "node-T-2", and one
    // that returned the task id itself would answer "T-1" rather than a node.
    const model = buildDecisionCardModel({ id: "T-2", payload: { task_id: "T-1" } });
    expect(model.id).toBe("T-2");
    expect(model.taskId).toBe("T-1");
    expect(nodeIdForDecisionCard(model, TASKS)).toBe("node-T-1");
  });

  it("answers the task's nodeId and never the task id it matched on", () => {
    // `remedyApi.ts` falls back to the task id only when `related_node_id` is
    // absent, so the two are equal today and are not the same field. A resolver
    // returning the id it matched on would pass every case where they agree.
    const renamed = [{ id: "T-1", nodeId: "some-other-node" }];
    const model = buildDecisionCardModel({ id: "d-1", payload: { task_id: "T-1" } });
    expect(nodeIdForDecisionCard(model, renamed)).toBe("some-other-node");
  });

  it("does not resolve through inherited object properties", () => {
    // `task_id` reaches this rule from a payload the client does not control,
    // so a name like `constructor` must miss rather than match something on the
    // prototype. `find` compares values, which is why this holds.
    const model = buildDecisionCardModel({ id: "d-1", payload: { task_id: "constructor" } });
    expect(nodeIdForDecisionCard(model, TASKS)).toBeNull();
  });
});
