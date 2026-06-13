import { describe, it, expect } from "vitest";
import { normalizeApiFailure, normalizeDashboardPayload } from "./api/remedyApi";
import { deriveAgentStatus, liveIsActive, selectChecklistRows } from "./cockpitLogic";
import type { RemedyDashboard, RemedyTaskItem } from "./api/types";

function baseDashboard(overrides: Partial<RemedyDashboard> = {}): RemedyDashboard {
  const failure = normalizeApiFailure("job-1", []);
  return { ...failure, apiHealth: { degraded: false, failedEndpoints: [] }, ...overrides };
}

function task(partial: Partial<RemedyTaskItem>): RemedyTaskItem {
  return {
    id: partial.id || "t", label: partial.label || "Task", state: partial.state || "pending",
    kind: "task", checked: partial.checked ?? false, muted: false, nodeId: partial.nodeId || "t",
    ...partial,
  };
}

// ---------------------------------------------------------------------------
// LIVE pill — only when running
// ---------------------------------------------------------------------------

describe("liveIsActive", () => {
  it("is false when not running", () => {
    expect(liveIsActive(baseDashboard({ live: { ...baseDashboard().live, running: false } }))).toBe(false);
  });
  it("is true only when running === true", () => {
    expect(liveIsActive(baseDashboard({ live: { ...baseDashboard().live, running: true } }))).toBe(true);
  });
  it("idle dashboard from API failure is not live", () => {
    expect(liveIsActive(normalizeApiFailure("job-1", ["dashboard"]))).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// AgentNow status — no work claimed without evidence
// ---------------------------------------------------------------------------

describe("deriveAgentStatus", () => {
  it("Idle when nothing running", () => {
    const s = deriveAgentStatus(baseDashboard());
    expect(s.status).toBe("Idle");
    expect(s.isRunning).toBe(false);
  });

  it("Needs your decision when waiting for approval", () => {
    const d = baseDashboard({
      workerStatus: { worker_available: true, worker_id: "w", lifecycle_state: "waiting_for_approval", current_job_id: "", queue_count: 0, heartbeat_at: "", stale: false, why_it_stopped: "", next_command: "", redaction: "" },
    });
    expect(deriveAgentStatus(d).status).toBe("Needs your decision");
  });

  it("Blocked surfaces the stop reason", () => {
    const d = baseDashboard({
      workerStatus: { worker_available: true, worker_id: "w", lifecycle_state: "blocked", current_job_id: "", queue_count: 0, heartbeat_at: "", stale: false, why_it_stopped: "budget_exhausted", next_command: "", redaction: "" },
    });
    const s = deriveAgentStatus(d);
    expect(s.status).toBe("Blocked");
    expect(s.detail).toBe("budget exhausted");
  });

  it("Working only when running", () => {
    const d = baseDashboard({ live: { ...baseDashboard().live, running: true, activeTaskLabel: "Fixing auth" } });
    const s = deriveAgentStatus(d);
    expect(s.status).toBe("Working");
    expect(s.isRunning).toBe(true);
  });
});

// ---------------------------------------------------------------------------
// Task checklist — exactly the real rows
// ---------------------------------------------------------------------------

describe("selectChecklistRows", () => {
  it("renders exactly as many rows as real tasks", () => {
    const tasks = [task({ id: "a", checked: true }), task({ id: "b" }), task({ id: "c" })];
    const { rows, completed } = selectChecklistRows(tasks);
    expect(rows).toHaveLength(3);
    expect(completed).toBe(1);
  });

  it("empty tasks -> zero rows, never padded", () => {
    const { rows, completed } = selectChecklistRows([]);
    expect(rows).toHaveLength(0);
    expect(completed).toBe(0);
  });

  it("caps very long task lists", () => {
    const tasks = Array.from({ length: 30 }, (_, i) => task({ id: `t${i}` }));
    expect(selectChecklistRows(tasks).rows).toHaveLength(16);
  });
});

// ---------------------------------------------------------------------------
// Token metric — em dash at 0/unknown (cross-check via normalizer)
// ---------------------------------------------------------------------------

describe("token metric honesty", () => {
  it("shows em dash when token usage is unknown", () => {
    const dash = normalizeDashboardPayload("job-1", { tasks: [], metrics: {} });
    const tok = dash.metrics.find(m => m.key === "tokens");
    expect(tok!.value).toBe("—");
    expect(tok!.unknown).toBe(true);
  });
});
