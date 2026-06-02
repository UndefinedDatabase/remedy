import { describe, it, expect } from "vitest";
import { normalizeDashboardPayload, normalizeApiFailure, normalizeLiveState, normalizePipeline } from "./remedyApi";

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
