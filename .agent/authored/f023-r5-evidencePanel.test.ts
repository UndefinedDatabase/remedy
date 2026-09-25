import { describe, expect, it } from "vitest";
import type { RemedyPromptTraceItem } from "../../api/types";
import { EVIDENCE_CHAT_NOT_YET, EVIDENCE_TABS, evidencePromptsOf } from "./evidencePanel";

function prompt(id: string, taskId: string, round: number, role: RemedyPromptTraceItem["role"]): RemedyPromptTraceItem {
  return {
    id, taskId, runId: "r", round, role, promptKind: "review", provider: "p", providerKind: "k",
    promptSha256: "", promptChars: 0, promptTokensEstimated: 0, contextCategories: [], changedFilesSafe: [],
    safeDiffFiles: [], evidenceRef: "", redactedPreview: "", redactedPreviewTruncated: false,
  };
}

describe("the evidence panel's tabs", () => {
  it("are diff, prompt trace and chat, in T5_F023.md's order", () => {
    expect(EVIDENCE_TABS).toEqual([
      { tab: "diff", label: "Diff" },
      { tab: "prompt", label: "Prompt trace" },
      { tab: "chat", label: "Chat" },
    ]);
  });

  it("the chat tab says in plain words that it is not here yet and where steering is", () => {
    expect(EVIDENCE_CHAT_NOT_YET).toBe(
      "Talking about a single run arrives with its own feature. The job's steering box, in the right panel, already reaches the running job.",
    );
  });
});

describe("evidencePromptsOf", () => {
  const items = [
    prompt("t1-r2-reviewer", "t1", 2, "reviewer"),
    prompt("t2-r1-builder", "t2", 1, "builder"),
    prompt("t1-r1-reviewer", "t1", 1, "reviewer"),
    prompt("t1-r2-builder", "t1", 2, "builder"),
    prompt("t1-r1-builder", "t1", 1, "builder"),
    prompt("t1-r1-system", "t1", 1, "system"),
  ];

  it("keeps the task's own prompts in the order they were sent", () => {
    expect(evidencePromptsOf(items, "t1").map((p) => p.id)).toEqual([
      "t1-r1-builder", "t1-r1-reviewer", "t1-r1-system", "t1-r2-builder", "t1-r2-reviewer",
    ]);
  });

  it("is empty for a task that sent none, and never mutates its input", () => {
    const before = items.map((p) => p.id);
    expect(evidencePromptsOf(items, "t9")).toEqual([]);
    evidencePromptsOf(items, "t1");
    expect(items.map((p) => p.id)).toEqual(before);
  });
});
