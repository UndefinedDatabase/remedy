import { describe, it, expect } from "vitest";
import { nodeIdForFeedRow } from "./feedFocus";

const TASKS = [
  { id: "T-1", nodeId: "node-T-1" },
  { id: "T-2", nodeId: "node-T-2" },
];

describe("nodeIdForFeedRow", () => {
  it("resolves a row to the node of the task that owns it", () => {
    expect(nodeIdForFeedRow({ taskId: "T-2" }, TASKS)).toBe("node-T-2");
  });

  it("returns null for a row that carries no linkage", () => {
    // Heartbeats and job-level events are the normal case here, not an error.
    expect(nodeIdForFeedRow({ taskId: "" }, TASKS)).toBeNull();
  });

  it("returns null when the linkage names a task the dashboard lacks", () => {
    // The stream and the dashboard are two reads of one job and can disagree
    // for a moment. A stale id must not jump to the wrong node.
    expect(nodeIdForFeedRow({ taskId: "T-9" }, TASKS)).toBeNull();
  });

  it("returns null against an empty task list rather than throwing", () => {
    expect(nodeIdForFeedRow({ taskId: "T-1" }, [])).toBeNull();
  });

  it("does not resolve through inherited object properties", () => {
    // `taskId` reaches this rule from parsed JSON the client does not control,
    // so a name like `constructor` must miss rather than match something on
    // the prototype. `find` compares values, which is why this holds.
    expect(nodeIdForFeedRow({ taskId: "constructor" }, TASKS)).toBeNull();
  });

  it("reads the task's nodeId and never assumes it equals the task id", () => {
    // `remedyApi.ts` falls back to the task id only when `related_node_id` is
    // absent, so the two are equal today and are not the same field.
    const renamed = [{ id: "T-1", nodeId: "some-other-node" }];
    expect(nodeIdForFeedRow({ taskId: "T-1" }, renamed)).toBe("some-other-node");
  });
});
