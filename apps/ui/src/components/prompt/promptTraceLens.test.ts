// Prompt-trace lens frontend tests — normalization + visible-graph integration.
// Steps 5451-5480, T004 — redaction-safe fixtures.
//
// Prompt bodies use a benign marker string instead of sensitive tokens, so the
// assertions never smuggle redaction-bait into the workspace diff.
import { describe, it, expect } from "vitest";
import { normalizePromptTrace, normalizeDashboardPayload } from "../../api/remedyApi";
import { buildDisplayModel } from "../graph/BrainGraphCanvas";

// Benign sentinel — would appear verbatim only if a raw prompt body leaked.
const markerString = "TOP_LEVEL_PROMPT_BODY_SHOULD_NOT_LEAK_INTO_DASHBOARD";

function rawItem(over: Record<string, unknown> = {}) {
  return {
    id: "T1-run1-r1-builder-0",
    task_id: "T1",
    run_id: "run1",
    round: 1,
    role: "builder",
    prompt_kind: "initial",
    provider: "fake",
    provider_kind: "synthetic_test",
    prompt_sha256: "feedface",
    prompt_chars: 80,
    prompt_tokens_estimated: 20,
    context_categories: ["goal"],
    changed_files_safe: ["docs/NOTES.md"],
    safe_diff_files: [],
    evidence_ref: "task_runs/T1/prompt_trace.jsonl",
    redacted_preview: `Builder body ${markerString} end.`,
    redacted_preview_truncated: false,
    ...over,
  };
}

function rawTrace(items: Record<string, unknown>[], over: Record<string, unknown> = {}) {
  return {
    total_prompts: items.length,
    builder_prompts: items.filter((i) => i.role === "builder").length,
    reviewer_prompts: items.filter((i) => i.role === "reviewer").length,
    repair_prompts: 0,
    total_prompt_tokens_estimated: 20 * items.length,
    items,
    source: "prompt_trace_jsonl",
    ...over,
  };
}

function dashboardWith(taskIds: string[], trace: unknown) {
  const tasks = taskIds.map((id) => ({
    id, title: `Task ${id}`, status: "completed", related_node_id: id,
  }));
  return normalizeDashboardPayload("job-1", { tasks, metrics: {}, prompt_trace: trace });
}

describe("normalizePromptTrace", () => {
  it("maps all fields from snake_case payload", () => {
    const summary = normalizePromptTrace(rawTrace([rawItem()]))!;
    expect(summary.source).toBe("prompt_trace_jsonl");
    expect(summary.totalPrompts).toBe(1);
    expect(summary.builderPrompts).toBe(1);
    const item = summary.items[0];
    expect(item.taskId).toBe("T1");
    expect(item.runId).toBe("run1");
    expect(item.role).toBe("builder");
    expect(item.promptKind).toBe("initial");
    expect(item.providerKind).toBe("synthetic_test");
    expect(item.promptTokensEstimated).toBe(20);
    expect(item.evidenceRef).toBe("task_runs/T1/prompt_trace.jsonl");
    expect(item.redactedPreview).toContain(markerString);
  });

  it("normalizes unknown role and kind to system/unknown", () => {
    const summary = normalizePromptTrace(rawTrace([
      rawItem({ role: "ghost", prompt_kind: "weird" }),
    ]))!;
    expect(summary.items[0].role).toBe("system");
    expect(summary.items[0].promptKind).toBe("unknown");
  });

  it("represents absent state explicitly", () => {
    const summary = normalizePromptTrace({
      source: "absent",
      missing_reason: "task_runs_missing",
      items: [],
      total_prompts: 0,
    })!;
    expect(summary.source).toBe("absent");
    expect(summary.missingReason).toBe("task_runs_missing");
    expect(summary.items).toHaveLength(0);
  });

  it("returns null when the section is entirely absent", () => {
    expect(normalizePromptTrace(null)).toBeNull();
    expect(normalizePromptTrace(undefined)).toBeNull();
  });
});

describe("buildDisplayModel visible-graph integration", () => {
  it("creates prompt nodes in the visible graph", () => {
    const dash = dashboardWith(["T1"], rawTrace([rawItem()]));
    const model = buildDisplayModel(dash);
    const promptNodes = model.nodes.filter((n) => n.kind === "prompt");
    expect(promptNodes).toHaveLength(1);
    expect(promptNodes[0].id).toBe("T1-run1-r1-builder-0");
  });

  it("does not inflate the task node count", () => {
    const dash = dashboardWith(["T1", "T2"], rawTrace([
      rawItem({ id: "p1", task_id: "T1" }),
      rawItem({ id: "p2", task_id: "T1" }),
      rawItem({ id: "p3", task_id: "T2" }),
    ]));
    const model = buildDisplayModel(dash);
    const taskNodes = model.nodes.filter((n) => n.kind === "task");
    expect(taskNodes).toHaveLength(2);
  });

  it("colors a prompt node by role", () => {
    const dash = dashboardWith(["T1"], rawTrace([
      rawItem({ id: "b", task_id: "T1", role: "builder", prompt_kind: "initial" }),
      rawItem({ id: "r", task_id: "T1", role: "reviewer", prompt_kind: "review" }),
    ]));
    const model = buildDisplayModel(dash);
    const builder = model.nodes.find((n) => n.id === "b");
    const reviewer = model.nodes.find((n) => n.id === "r");
    expect(builder?.color).toBe("#4c83ff");
    expect(reviewer?.color).toBe("#a78bfa");
  });

  it("surfaces a task's prompts via the prompt node taskId", () => {
    const dash = dashboardWith(["T1", "T2"], rawTrace([
      rawItem({ id: "p1", task_id: "T1" }),
      rawItem({ id: "p2", task_id: "T2" }),
    ]));
    const model = buildDisplayModel(dash);
    const forT1 = model.nodes.filter((n) => n.kind === "prompt" && n.taskId === "T1");
    expect(forT1).toHaveLength(1);
    expect(forT1[0].id).toBe("p1");
  });

  it("yields an empty prompt set for a task without a trace", () => {
    const dash = dashboardWith(["T1", "T2"], rawTrace([
      rawItem({ id: "p1", task_id: "T1" }),
    ]));
    const model = buildDisplayModel(dash);
    const forT2 = model.nodes.filter((n) => n.kind === "prompt" && n.taskId === "T2");
    expect(forT2).toHaveLength(0);
  });
});
