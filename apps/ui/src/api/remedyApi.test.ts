import { describe, it, expect } from "vitest";
import { normalizeDashboardPayload, normalizeApiFailure, normalizeLiveState, normalizePipeline, diffEnvelopePath, loadDiffEnvelope } from "./remedyApi";
import type { DiffEnvelopeRequest } from "./remedyApi";

// ---------------------------------------------------------------------------
// Fixtures
// ---------------------------------------------------------------------------

function makeDashboardPayload(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    version: 3,
    job_id: "abc-123",
    generated_at: "2026-01-01T00:00:00Z",
    source: "server",
    live: { running: false, state: "idle", stale: true, confidence: "none" },
    metrics: { open: 0, planned: 2, done: 1, progress_percent: 33, source_counts: { tasks: 3, events: 5 } },
    tasks: [
      { id: "t1", title: "Parse the config file", status: "completed", verified: true, source: "real", related_node_id: "t1" },
      { id: "t2", title: "Write unit tests", status: "pending", verified: false, source: "real", related_node_id: "t2" },
    ],
    activity: [
      { id: "evt-1", time: "2026-01-01T00:00:00Z", actor: "Builder", event_kind: "task_created", summary: "Task created" },
    ],
    phases: [
      { id: "planning", title: "Planning", status: "done", rank: 0 },
      { id: "build", title: "Build", status: "current", rank: 1 },
    ],
    graph_summary: { node_count: 3, edge_count: 2, source: "project_brain", mode: "force_graph" },
    next_action: { kind: "guidance", label: "Review project state", requires_user: true },
    truth: { fallback_count: 0, synthetic_count: 0, demo_mode: false, missing_sources: [] },
    redaction: { policy: "safe_summaries_only", raw_content_exposed: false },
    job_name: "Test Job",
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// A. Dashboard success path
// ---------------------------------------------------------------------------

describe("normalizeDashboardPayload", () => {
  it("uses dashboard metrics", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    const progress = result.metrics.find(m => m.key === "progress");
    expect(progress?.value).toBe(33);
    const planned = result.metrics.find(m => m.key === "planned");
    expect(planned?.value).toBe(2);
  });

  it("uses dashboard tasks", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.tasks).toHaveLength(2);
    expect(result.tasks[0].label).toBe("Parse the config file");
  });

  it("uses dashboard live state", () => {
    const payload = makeDashboardPayload({ live: { running: true, state: "active" } });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.live.running).toBe(true);
  });

  it("uses dashboard phases", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.phases.length).toBeGreaterThanOrEqual(2);
    expect(result.phases[0].id).toBe("planning");
  });

  it("uses dashboard activity", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.activity.length).toBeGreaterThanOrEqual(1);
    expect(result.activity[0].actor).toBe("Builder");
  });

  it("apiHealth is not degraded on success", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.apiHealth.degraded).toBe(false);
    expect(result.apiHealth.failedEndpoints).toHaveLength(0);
  });
});

// ---------------------------------------------------------------------------
// B. Dashboard failure path
// ---------------------------------------------------------------------------

describe("normalizeApiFailure", () => {
  it("sets degraded to true", () => {
    const result = normalizeApiFailure("abc-123", ["dashboard"]);
    expect(result.apiHealth.degraded).toBe(true);
  });

  it("preserves failed endpoint names", () => {
    const result = normalizeApiFailure("abc-123", ["dashboard", "brain-view-model"]);
    expect(result.apiHealth.failedEndpoints).toContain("dashboard");
    expect(result.apiHealth.failedEndpoints).toContain("brain-view-model");
  });

  it("returns empty tasks", () => {
    const result = normalizeApiFailure("abc-123", ["dashboard"]);
    expect(result.tasks).toHaveLength(0);
  });

  it("returns not running", () => {
    const result = normalizeApiFailure("abc-123", ["dashboard"]);
    expect(result.live.running).toBe(false);
  });

  it("returns empty activity", () => {
    const result = normalizeApiFailure("abc-123", ["dashboard"]);
    expect(result.activity).toHaveLength(0);
  });
});

// ---------------------------------------------------------------------------
// C. Live state normalization
// ---------------------------------------------------------------------------

describe("normalizeLiveState", () => {
  it("missing live data = not running", () => {
    const result = normalizeLiveState(undefined);
    expect(result.running).toBe(false);
  });

  it("null live data = not running", () => {
    const result = normalizeLiveState(null);
    expect(result.running).toBe(false);
  });

  it("empty object = not running", () => {
    const result = normalizeLiveState({});
    expect(result.running).toBe(false);
    expect(result.stage).toBe("unknown");
  });

  it("running: true is preserved", () => {
    const result = normalizeLiveState({ running: true, stage: "active" });
    expect(result.running).toBe(true);
    expect(result.stage).toBe("active");
  });
});

// ---------------------------------------------------------------------------
// D. No fake tasks from fallback
// ---------------------------------------------------------------------------

describe("no fake fallback tasks", () => {
  it("empty tasks array stays empty", () => {
    const payload = makeDashboardPayload({ tasks: [] });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.tasks).toHaveLength(0);
  });

  it("no DISPLAY_ROWS or hardcoded task names", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    const fakeNames = ["Scaffold project", "Set up environment", "Configure linting"];
    for (const fakeName of fakeNames) {
      expect(result.tasks.some(t => t.label === fakeName)).toBe(false);
    }
  });
});

// ---------------------------------------------------------------------------
// E. Redaction
// ---------------------------------------------------------------------------

describe("redaction", () => {
  it("scrubs known forbidden field names from task labels", () => {
    const payload = makeDashboardPayload({
      tasks: [{ id: "t1", title: "raw_stdout from subprocess", status: "pending", source: "real", related_node_id: "t1" }],
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    // scrubUiText replaces forbidden content with fallback
    expect(result.tasks[0].label).not.toContain("raw_stdout");
  });

  it("scrubs UUID-only labels to fallback", () => {
    const payload = makeDashboardPayload({
      tasks: [{ id: "t1", title: "a1b2c3d4e5f6", status: "pending", source: "real", related_node_id: "t1" }],
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    // hex-only strings are replaced by scrubUiText
    expect(result.tasks[0].label).not.toBe("a1b2c3d4e5f6");
  });
});

// ---------------------------------------------------------------------------
// F. Empty dashboard (honest state)
// ---------------------------------------------------------------------------

describe("empty dashboard honesty", () => {
  it("empty dashboard shows no activity", () => {
    const payload = makeDashboardPayload({ activity: [], tasks: [] });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.activity).toHaveLength(0);
    expect(result.tasks).toHaveLength(0);
  });

  it("no fake progress on empty dashboard", () => {
    const payload = makeDashboardPayload({
      metrics: { open: 0, planned: 0, done: 0, progress_percent: 0 },
      tasks: [],
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    const progress = result.metrics.find(m => m.key === "progress");
    expect(progress?.value).toBe(0);
  });
});

// ---------------------------------------------------------------------------
// G. Pipeline normalization
// ---------------------------------------------------------------------------

describe("normalizePipeline", () => {
  it("returns null for missing pipeline", () => {
    expect(normalizePipeline(null)).toBeNull();
    expect(normalizePipeline(undefined)).toBeNull();
  });

  it("normalizes empty pipeline", () => {
    const p = normalizePipeline({ version: 1, provider: null, provider_mode: "none", stale: true });
    expect(p).not.toBeNull();
    expect(p!.provider).toBeNull();
    expect(p!.stale).toBe(true);
    expect(p!.steps.length).toBeGreaterThan(0);
  });

  it("normalizes fixture success pipeline", () => {
    const p = normalizePipeline({
      version: 1, provider: "fixture", provider_mode: "fixture",
      source_context: { injected: true, file_count: 3, estimated_tokens: 500 },
      memory: { used: false, item_count: 0, truncated: false, context_hash: "" },
      structured_patch_attempted: true, parse_success: true,
      intent_status: "approved", approval_required: false, approval_status: "approved",
      source_apply_status: "applied", tests_status: "pass", tests_passed: true,
      repair_loop: { used: false, cycle_count: 0, max_cycles: 0 },
      stop_reason: "", stop_reason_label: "", next_command: "",
      stale: false,
    });
    expect(p!.provider).toBe("fixture");
    expect(p!.tests_passed).toBe(true);
    const doneSteps = p!.steps.filter(s => s.state === "done");
    expect(doneSteps.length).toBeGreaterThanOrEqual(4);
  });

  it("normalizes approval required pipeline", () => {
    const p = normalizePipeline({
      version: 1, provider: "ollama", provider_mode: "ollama",
      source_context: { injected: true },
      memory: { used: true, item_count: 2, truncated: false, context_hash: "abc" },
      structured_patch_attempted: true, parse_success: true,
      intent_status: "created", approval_required: true, approval_status: "pending",
      source_apply_status: "none", tests_status: "none", tests_passed: null,
      repair_loop: { used: false, cycle_count: 0, max_cycles: 0 },
      stop_reason: "approval_required", stop_reason_label: "Human approval required",
      next_command: "remedy patch approve job-1 i-1",
      stale: false,
    });
    expect(p!.approval_required).toBe(true);
    expect(p!.stop_reason).toBe("approval_required");
    const approval = p!.steps.find(s => s.id === "approval");
    expect(approval?.state).toBe("blocked");
  });

  it("normalizes parse failure pipeline", () => {
    const p = normalizePipeline({
      version: 1, provider: "ollama",
      structured_patch_attempted: true, parse_success: false, parse_error_kind: "prose_only",
      stop_reason: "provider_output_prose_only",
      stop_reason_label: "Model returned prose, not a patch",
      stale: false,
    });
    expect(p!.parse_success).toBe(false);
    const patchStep = p!.steps.find(s => s.id === "patch");
    expect(patchStep?.state).toBe("failed");
  });

  it("normalizes repair loop pipeline", () => {
    const p = normalizePipeline({
      version: 1, provider: "ollama",
      structured_patch_attempted: true, parse_success: true,
      intent_status: "approved", approval_status: "approved",
      source_apply_status: "applied", tests_status: "fail", tests_passed: false,
      repair_loop: { used: true, cycle_count: 2, max_cycles: 3 },
      stop_reason: "test_failed_after_apply",
      stale: false,
    });
    const repairStep = p!.steps.find(s => s.id === "repair");
    expect(repairStep).toBeDefined();
    expect(repairStep!.detail).toContain("2/3");
  });

  it("does not include raw provider output", () => {
    const p = normalizePipeline({
      version: 1, provider: "ollama",
      stop_reason: "provider_output_prose_only",
      stale: false,
    });
    const str = JSON.stringify(p);
    expect(str).not.toContain("def ");
    expect(str).not.toContain("import ");
    expect(str).not.toContain("raw_");
  });
});

// ---------------------------------------------------------------------------
// H. Pipeline in dashboard
// ---------------------------------------------------------------------------

describe("pipeline in dashboard", () => {
  it("dashboard without pipeline returns null pipeline", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.pipeline).toBeNull();
  });

  it("dashboard with pipeline returns normalized pipeline", () => {
    const payload = makeDashboardPayload({
      pipeline: {
        version: 1, provider: "fixture", provider_mode: "fixture",
        source_context: { injected: true, file_count: 2 },
        memory: { used: false, item_count: 0, truncated: false, context_hash: "" },
        structured_patch_attempted: true, parse_success: true,
        intent_status: "approved", approval_status: "approved",
        source_apply_status: "applied", tests_status: "pass", tests_passed: true,
        repair_loop: { used: false, cycle_count: 0, max_cycles: 0 },
        stop_reason: "", stale: false,
      },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.pipeline).not.toBeNull();
    expect(result.pipeline!.provider).toBe("fixture");
    expect(result.pipeline!.steps.length).toBeGreaterThan(0);
  });

  it("failure dashboard has null pipeline", () => {
    const result = normalizeApiFailure("abc-123", ["dashboard"]);
    expect(result.pipeline).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// I. Token usage metric
// ---------------------------------------------------------------------------

describe("token usage metric", () => {
  it("cost is the last metric, order is open/planned/done/progress/tests/proof/tokens/cost", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.metrics).toHaveLength(8);
    expect(result.metrics.map(m => m.key)).toEqual([
      "open", "planned", "done", "progress", "tests", "proof", "tokens", "cost",
    ]);
  });

  it("cost loads unknown with an em dash, because no tick has arrived yet", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    const cost = result.metrics.find(m => m.key === "cost");
    expect(cost!.value).toBe("—");
    expect(cost!.unknown).toBe(true);
    expect(cost!.cost).toBeUndefined();
  });

  it("the degraded path carries no cost tile it could not honour", () => {
    const degraded = normalizeApiFailure("abc-123", ["dashboard"]);
    expect(degraded.metrics.map(m => m.key)).toEqual([
      "open", "planned", "done", "progress",
    ]);
  });

  it("unknown tokens shows em dash value", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    const tok = result.metrics.find(m => m.key === "tokens");
    expect(tok!.value).toBe("—");
    expect(tok!.unknown).toBe(true);
  });

  it("zero tokens shows em dash value", () => {
    const payload = makeDashboardPayload({ token_usage: { known: true, total_tokens: 0 } });
    const result = normalizeDashboardPayload("abc-123", payload);
    const tok = result.metrics.find(m => m.key === "tokens");
    expect(tok!.value).toBe("—");
    expect(tok!.unknown).toBe(true);
  });

  it("known tokens from token_usage", () => {
    const payload = makeDashboardPayload({
      token_usage: { known: true, total_tokens: 12500, estimated: true, by_role: { context: 8000, memory: 4500 } },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    const tok = result.metrics.find(m => m.key === "tokens");
    expect(tok!.value).toBe(12500);
    expect(tok!.suffix).toBeUndefined();
    expect(tok!.tooltip).toEqual({ context: 8000, memory: 4500 });
  });

  it("no raw prompt data in token metric", () => {
    const payload = makeDashboardPayload({
      token_usage: { known: true, total_tokens: 500, by_role: { planner: 500 } },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    const str = JSON.stringify(result.metrics);
    expect(str).not.toContain("raw_");
    expect(str).not.toContain("prompt");
  });
});

// ---------------------------------------------------------------------------
// J. Cockpit metrics: tests + proof
// ---------------------------------------------------------------------------

describe("tests + proof metrics", () => {
  it("tests metric maps passed count and latest_state dot", () => {
    const payload = makeDashboardPayload({
      metrics: { open: 0, planned: 0, done: 0, progress_percent: 0,
        tests: { runs: 4, passed: 3, failed: 1, latest_state: "fail" } },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    const tests = result.metrics.find(m => m.key === "tests");
    expect(tests!.value).toBe(3);
    expect(tests!.state).toBe("fail");
  });

  it("missing tests metric defaults to 0 / none", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    const tests = result.metrics.find(m => m.key === "tests");
    expect(tests!.value).toBe(0);
    expect(tests!.state).toBe("none");
  });

  it("proof metric maps verified/total", () => {
    const payload = makeDashboardPayload({
      metrics: { open: 0, planned: 0, done: 0, progress_percent: 0,
        proof: { total_changes: 4, verified: 3, state: "partial" } },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    const proof = result.metrics.find(m => m.key === "proof");
    expect(proof!.value).toBe(3);
    expect(proof!.suffix).toBe("/4");
    expect(proof!.unknown).toBeUndefined();
  });

  it("unknown proof shows em dash", () => {
    const payload = makeDashboardPayload({
      metrics: { open: 0, planned: 0, done: 0, progress_percent: 0,
        proof: { total_changes: "unknown", verified: "unknown", state: "unknown" } },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    const proof = result.metrics.find(m => m.key === "proof");
    expect(proof!.value).toBe("—");
    expect(proof!.unknown).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// K. Snapshot + continuation summaries
// ---------------------------------------------------------------------------

describe("snapshot + continuation summaries", () => {
  it("maps snapshot summary fields", () => {
    const payload = makeDashboardPayload({
      snapshot: { apply_records: 2, verified: 1, reverted: 0, drift_detected: false, source: "durable_apply_records" },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.snapshot).not.toBeNull();
    expect(result.snapshot!.applyRecords).toBe(2);
    expect(result.snapshot!.verified).toBe(1);
    expect(result.snapshot!.driftDetected).toBe(false);
    expect(result.snapshot!.source).toBe("durable_apply_records");
  });

  it("snapshot unknown values pass through as 'unknown'", () => {
    const payload = makeDashboardPayload({
      snapshot: { apply_records: "unknown", verified: "unknown", reverted: "unknown", drift_detected: "unknown", source: "unavailable" },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.snapshot!.applyRecords).toBe("unknown");
    expect(result.snapshot!.driftDetected).toBe("unknown");
  });

  it("maps continuation summary fields", () => {
    const payload = makeDashboardPayload({
      continuation: { available: true, last_result: "completed_verified", last_stop_reason: "completed_verified" },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.continuation!.available).toBe(true);
    expect(result.continuation!.lastResult).toBe("completed_verified");
  });

  it("continuation unknown available passes through", () => {
    const payload = makeDashboardPayload({
      continuation: { available: "unknown", last_result: "unknown", last_stop_reason: "unknown" },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.continuation!.available).toBe("unknown");
  });

  it("missing snapshot/continuation -> null", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.snapshot).toBeNull();
    expect(result.continuation).toBeNull();
  });

  it("failure dashboard has null snapshot + continuation", () => {
    const result = normalizeApiFailure("abc-123", ["dashboard"]);
    expect(result.snapshot).toBeNull();
    expect(result.continuation).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// The ledger's final budget figure (DECISION F022 D7 serves it, D8 renders it)
// ---------------------------------------------------------------------------

describe("budget_final transport", () => {
  it("maps the ledger figure through unchanged", () => {
    const payload = makeDashboardPayload({
      budget_final: { spent_usd: 4.2, limit_usd: 8, basis: { cost: "actual" }, unmeasured_calls: 0 },
    });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.budgetFinal).toEqual({
      spent_usd: 4.2, limit_usd: 8, basis: { cost: "actual" }, unmeasured_calls: 0,
    });
  });

  it("a null section stays null — the server says so for a job with no tick", () => {
    const payload = makeDashboardPayload({ budget_final: null });
    const result = normalizeDashboardPayload("abc-123", payload);
    expect(result.budgetFinal).toBeNull();
  });

  it("a payload with no budget_final key at all yields null, never an empty object", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.budgetFinal).toBeNull();
  });

  it("the failure dashboard carries no ledger figure", () => {
    expect(normalizeApiFailure("abc-123", ["dashboard"]).budgetFinal).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// The decision inbox: the /decisions document projected through
// `decisionCardModels` (T5_F031 T002a). Nothing is mocked and no fetch runs —
// that is precisely why the projection lives in normalizeDashboardPayload.
// ---------------------------------------------------------------------------

describe("decisionInbox projection", () => {
  it("projects every card of the document, in the endpoint's order", () => {
    const inbox = {
      decisions: [
        { id: "d1", type: "approval", status: "open", severity: "high", safe_summary: "Approve the config patch", age_seconds: 90, blocked_count: 2 },
        { id: "d2", type: "question", status: "answered", severity: "low", safe_summary: "Pick a module name", age_seconds: 5, blocked_count: 0 },
      ],
    };
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload(), undefined, inbox);
    expect(result.decisionInbox.map(c => c.id)).toEqual(["d1", "d2"]);
    expect(result.decisionInbox[0].title).toBe("Approve the config patch");
    expect(result.decisionInbox[0].ageLabel).toBe("1m");
    expect(result.decisionInbox[0].blockedLabel).toBe("blocks 2 tasks");
    expect(result.decisionInbox[0].isOpen).toBe(true);
    expect(result.decisionInbox[1].ageLabel).toBe("5s");
    expect(result.decisionInbox[1].blockedLabel).toBe("blocks nothing");
    expect(result.decisionInbox[1].isOpen).toBe(false);
  });

  it("an absent decisions document yields the empty inbox, never undefined", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload());
    expect(result.decisionInbox).toEqual([]);
  });

  it("a decisions value that is not an array yields the empty inbox", () => {
    const result = normalizeDashboardPayload("abc-123", makeDashboardPayload(), undefined, { decisions: "not-an-array" });
    expect(result.decisionInbox).toEqual([]);
  });

  it("the failure dashboard carries the empty inbox", () => {
    expect(normalizeApiFailure("abc-123", ["dashboard"]).decisionInbox).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// The diff envelope door (T5_F037 T003). No global is patched and no fetch is
// mocked: `loadDiffEnvelope` takes its fetcher as an argument, so a plain arrow
// function is the whole test double.
// ---------------------------------------------------------------------------

describe("the diff envelope door", () => {
  const request: DiffEnvelopeRequest = { jobId: "abc-123", token: "t0k" };

  it("addresses the job scope when the request names no task run", () => {
    expect(diffEnvelopePath(request)).toBe("/api/jobs/abc-123/diff?token=t0k");
  });

  it("addresses the task-run scope when the request names one", () => {
    expect(diffEnvelopePath({ ...request, taskId: "run-7" })).toBe(
      "/api/jobs/abc-123/task-runs/run-7/diff?token=t0k",
    );
  });

  it("percent-encodes the token and the task id, so neither can add a parameter or a segment", () => {
    const path = diffEnvelopePath({ jobId: "abc-123", token: "a&b=c", taskId: "run/7" });
    expect(path).toBe("/api/jobs/abc-123/task-runs/run%2F7/diff?token=a%26b%3Dc");
    expect(path).not.toContain("run/7");
    expect(path.split("&")).toHaveLength(1);
  });

  it("prefixes an explicit baseUrl and stays relative without one", () => {
    expect(diffEnvelopePath({ ...request, baseUrl: "http://127.0.0.1:8123" })).toBe(
      "http://127.0.0.1:8123/api/jobs/abc-123/diff?token=t0k",
    );
    expect(diffEnvelopePath(request).startsWith("/api/")).toBe(true);
  });

  it("reads null, empty and whitespace-only task ids as the job scope", () => {
    const jobScope = "/api/jobs/abc-123/diff?token=t0k";
    expect(diffEnvelopePath({ ...request, taskId: null })).toBe(jobScope);
    expect(diffEnvelopePath({ ...request, taskId: "" })).toBe(jobScope);
    expect(diffEnvelopePath({ ...request, taskId: "   " })).toBe(jobScope);
  });

  it("returns the parsed envelope and reads its own path exactly once", async () => {
    const seen: string[] = [];
    const envelope = await loadDiffEnvelope(request, async (path) => {
      seen.push(path);
      return { version: 1, scope: "job", available: true, files: [], task_run_ids: ["r1"] };
    });
    expect(seen).toEqual([diffEnvelopePath(request)]);
    expect(envelope.available).toBe(true);
    expect(envelope.version).toBe(1);
    expect(envelope.scope).toBe("job");
    expect(envelope.taskRunIds).toEqual(["r1"]);
  });

  it("degrades a rejected fetch to an unavailable envelope rather than throwing", async () => {
    const envelope = await loadDiffEnvelope(request, () => Promise.reject(new Error("403")));
    expect(envelope.available).toBe(false);
    expect(envelope.files).toEqual([]);
  });

  it("degrades a junk body to the same unavailable envelope", async () => {
    const fromString = await loadDiffEnvelope(request, async () => "not an envelope");
    expect(fromString.available).toBe(false);
    expect(fromString.files).toEqual([]);
    const fromArray = await loadDiffEnvelope(request, async () => [1, 2, 3]);
    expect(fromArray.available).toBe(false);
    expect(fromArray.files).toEqual([]);
  });
});
