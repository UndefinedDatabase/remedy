import { describe, expect, it } from "vitest";
import type { RemedyPromptTraceItem } from "../../api/types";
import { seedBrainModel } from "./brainReducer";
import { promptNodeId, withPromptNodes } from "./promptNodes";

function prompt(
  id: string,
  taskId: string,
  overrides: Partial<RemedyPromptTraceItem> = {},
): RemedyPromptTraceItem {
  return {
    id, taskId, runId: "run-1", round: 1, role: "builder", promptKind: "initial",
    provider: "p", providerKind: "k", promptSha256: "", promptChars: 0,
    promptTokensEstimated: 0, contextCategories: [], changedFilesSafe: [],
    safeDiffFiles: [], evidenceRef: "", redactedPreview: "", redactedPreviewTruncated: false,
    ...overrides,
  };
}

describe("promptNodeId", () => {
  it("answers prompt:<itemId>", () => {
    expect(promptNodeId("abc123")).toBe("prompt:abc123");
  });
});

describe("withPromptNodes", () => {
  it("births a synapse for an item whose task exists, with the id, kind, parent, seq, meta and link S1 names", () => {
    const model = seedBrainModel("job-1", [{ id: "t1", status: "running", rank: 0 }]);
    const item = prompt("p1", "t1", { round: 2, role: "reviewer", promptKind: "review", runId: "run-9" });
    const next = withPromptNodes(model, [item]);

    const synapse = next.nodes.find((n) => n.id === "prompt:p1");
    expect(synapse).toEqual({
      id: "prompt:p1",
      kind: "synapse",
      state: "in_progress", // task:t1 seeded "running" -> in_progress
      parentId: "task:t1",
      seq: 0,
      meta: { promptId: "p1", role: "reviewer", promptKind: "review", round: 2, attemptId: "run-9" },
    });

    const link = next.links.find((l) => l.id === "task:t1->prompt:p1");
    expect(link).toEqual({ id: "task:t1->prompt:p1", source: "task:t1", target: "prompt:p1" });
  });

  it("gives a synapse its own task node's state, for at least three different task states", () => {
    const model = seedBrainModel("job-2", [
      { id: "t-pass", status: "completed", rank: 0 },
      { id: "t-fail", status: "failed", rank: 1 },
      { id: "t-running", status: "running", rank: 2 },
    ]);
    const items = [
      prompt("p-pass", "t-pass"),
      prompt("p-fail", "t-fail"),
      prompt("p-running", "t-running"),
    ];
    const next = withPromptNodes(model, items);
    expect(next.nodes.find((n) => n.id === "prompt:p-pass")?.state).toBe("pass");
    expect(next.nodes.find((n) => n.id === "prompt:p-fail")?.state).toBe("fail");
    expect(next.nodes.find((n) => n.id === "prompt:p-running")?.state).toBe("in_progress");
  });

  it("skips an item whose task the model lacks", () => {
    const model = seedBrainModel("job-3", [{ id: "t1", status: "pending", rank: 0 }]);
    const next = withPromptNodes(model, [prompt("orphan", "no-such-task")]);
    expect(next.nodes.some((n) => n.id === "prompt:orphan")).toBe(false);
  });

  it("skips a repeated item the second time", () => {
    const model = seedBrainModel("job-4", [{ id: "t1", status: "pending", rank: 0 }]);
    const item = prompt("p1", "t1");
    const next = withPromptNodes(model, [item, item]);
    expect(next.nodes.filter((n) => n.id === "prompt:p1")).toHaveLength(1);
    expect(next.links.filter((l) => l.id === "task:t1->prompt:p1")).toHaveLength(1);
  });

  it("keeps item order", () => {
    const model = seedBrainModel("job-5", [
      { id: "t1", status: "pending", rank: 0 },
      { id: "t2", status: "pending", rank: 1 },
    ]);
    const items = [prompt("p-b", "t2"), prompt("p-a", "t1"), prompt("p-c", "t1")];
    const next = withPromptNodes(model, items);
    const bornIds = next.nodes.slice(model.nodes.length).map((n) => n.id);
    expect(bornIds).toEqual(["prompt:p-b", "prompt:p-a", "prompt:p-c"]);
  });

  it("answers the same object for no items", () => {
    const model = seedBrainModel("job-6", [{ id: "t1", status: "pending", rank: 0 }]);
    expect(withPromptNodes(model, [])).toBe(model);
  });

  it("answers the same object when every item is skipped", () => {
    const model = seedBrainModel("job-7", [{ id: "t1", status: "pending", rank: 0 }]);
    const item = prompt("p1", "t1");
    const onceBorn = withPromptNodes(model, [item]);
    // Every item on this second call either duplicates an already-born synapse
    // or names a task the model lacks -> nothing appends, so the SAME model
    // object (onceBorn) comes back.
    expect(withPromptNodes(onceBorn, [item, prompt("orphan", "no-such-task")])).toBe(onceBorn);
  });
});
