import { humanLabel, isDiagnosticsOnly, scrubUiText } from "../copy/humanCopy";
import type { RemedyActivityItem, RemedyDashboard, RemedyGraphEdge, RemedyGraphNode, RemedyJourneyItem, RemedyMetric, RemedyNextAction, RemedyPhase, RemedyState, RemedyTaskItem } from "./types";

interface ApiClientOptions { jobId: string; token: string; baseUrl?: string; }

const FALLBACK_LABELS: Record<string, string> = {
  goal: "Project goal", task: "Current work", change: "Proposed change",
  apply: "Applied change", test: "Test result", proof: "Proof recorded",
  review: "Review suggestion", memory: "Learning note",
  decision: "Needs your decision", blocker: "Blocker",
};

function isWeakLabel(label: string): boolean {
  if (!label || label.length < 3) return true;
  if (/^[0-9a-f-]{8,}$/i.test(label)) return true;
  const weak = ["task", "output", "memory", "goal", "blocker"];
  return weak.includes(label.toLowerCase().trim());
}

function humanFallbackFor(kind: string, _index?: number): string {
  return FALLBACK_LABELS[kind] || FALLBACK_LABELS.task;
}

async function fetchJson<T>(path: string): Promise<T> {
  const r = await fetch(path, { method: "GET", credentials: "same-origin" });
  if (!r.ok) throw new Error(`Request failed ${r.status}: ${path}`);
  return r.json() as Promise<T>;
}

function normalizeState(value: unknown): RemedyState {
  const text = String(value || "").toLowerCase();
  if (text.includes("done") || text.includes("pass") || text.includes("complete") || text.includes("applied")) return "done";
  if (text.includes("block") || text.includes("fail")) return "blocked";
  if (text.includes("current") || text.includes("active") || text.includes("running") || text.includes("progress")) return "current";
  if (text.includes("suggest")) return "suggested";
  return "pending";
}

function nextAction(label = "Review project state", command = "remedy dev status"): RemedyNextAction {
  return { label, command, risk: "low", requiresHuman: true };
}

/* eslint-disable @typescript-eslint/no-explicit-any */

// ---------------------------------------------------------------------------
// Dashboard-first normalization (exported for testing)
// ---------------------------------------------------------------------------

/** Normalize a successful /dashboard payload into RemedyDashboard. */
export function normalizeDashboardPayload(
  jobId: string,
  dashboard: any,
  brainDetail?: any,
): RemedyDashboard {
  // Tasks from dashboard
  const tasks: RemedyTaskItem[] = (dashboard.tasks || []).map((t: any, idx: number) => {
    const state = normalizeState(t.status || t.state);
    const kind = (t.kind || "task") as RemedyTaskItem["kind"];
    const rawLabel = scrubUiText(t.title || t.description || humanLabel(kind), humanLabel(kind));
    const label = isWeakLabel(rawLabel) ? humanFallbackFor(kind, idx) : rawLabel;
    return {
      id: scrubUiText(t.id || `task-${idx}`, `task-${idx}`),
      label,
      state,
      kind,
      checked: Boolean(t.verified ?? t.accepted ?? state === "done"),
      muted: Boolean(state === "pending" || state === "suggested"),
      nodeId: String(t.related_node_id || t.id || `task-${idx}`),
      nextAction: undefined,
    };
  });

  // Metrics from dashboard
  const dm = dashboard.metrics || {};
  const metrics: RemedyMetric[] = [
    { key: "open", label: "Open", value: dm.open ?? 0 },
    { key: "planned", label: "Planned", value: dm.planned ?? 0 },
    { key: "done", label: "Done", value: dm.done ?? 0 },
    { key: "progress", label: "Progress", value: dm.progress_percent ?? 0, suffix: "%" },
  ];

  // Phases from dashboard
  const phases: RemedyPhase[] = (dashboard.phases || []).map((p: any) => ({
    id: p.id || "planning",
    label: p.title || p.label || p.id,
    state: normalizeState(p.status || p.state),
    icon: p.icon || "code",
  }));

  // Activity from dashboard
  const activity: RemedyActivityItem[] = (dashboard.activity || []).map((a: any, idx: number) => {
    const meta = EVENT_LABELS[a.event_kind] || { actor: (a.actor || "System") as any, kind: "system" as const, label: a.summary || a.event_kind || "" };
    return {
      id: a.id || `event-${idx}`,
      actor: meta.actor,
      message: scrubUiText(meta.label || a.summary, ""),
      timeLabel: a.time ? formatEventTime(a.time) : "",
      kind: meta.kind,
    };
  });

  // Live state from dashboard
  const live = dashboard.live || {};
  const running = Boolean(live.running ?? false);

  // Graph from brain-view-model detail (secondary) or dashboard graph_summary
  const graph = brainDetail
    ? normalizeGraphFromBrain(brainDetail, tasks)
    : buildMinimalGraph(tasks);

  // Next action from dashboard
  const na = dashboard.next_action;
  const nextAct: RemedyNextAction = na
    ? {
        label: scrubUiText(na.label, "Review project state"),
        command: scrubUiText(na.command || na.label, "remedy dev status"),
        risk: na.risk || "low",
        requiresHuman: Boolean(na.requires_user ?? true),
      }
    : nextAction();

  // Title/description
  const title = scrubUiText(dashboard.legacy?.job_name || brainDetail?.title || brainDetail?.job_title, "Growing Brain Overview");
  const description = scrubUiText(
    brainDetail?.description || "An AI agent working through a verified project plan.",
    "An AI agent working through a verified project plan.",
  );

  return {
    jobId,
    title,
    description,
    conceptLabel: "Concept 01 of 10",
    metrics,
    phases: phases.length > 0 ? phases : buildDefaultPhases(tasks),
    tasks,
    activity,
    graph,
    nextAction: nextAct,
    live: {
      running,
      stage: scrubUiText(live.state || live.stage, "unknown"),
      activeTaskLabel: tasks.find(t => t.state === "current")?.label || "Waiting for next safe action",
      latestMessage: scrubUiText(live.latest_message || "", ""),
      latestActor: "Builder",
    },
    apiHealth: { degraded: false, failedEndpoints: [] },
  };
}

/** Normalize API failure into degraded RemedyDashboard. */
export function normalizeApiFailure(jobId: string, failedEndpoints: string[]): RemedyDashboard {
  return {
    jobId,
    title: "Mission Control",
    description: "",
    conceptLabel: "",
    metrics: [
      { key: "open", label: "Open", value: 0 },
      { key: "planned", label: "Planned", value: 0 },
      { key: "done", label: "Done", value: 0 },
      { key: "progress", label: "Progress", value: 0, suffix: "%" },
    ],
    phases: [],
    tasks: [],
    activity: [],
    graph: { nodes: [], edges: [] },
    nextAction: nextAction(),
    live: {
      running: false,
      stage: "unknown",
      activeTaskLabel: "Waiting for next safe action",
      latestMessage: "",
      latestActor: "Builder",
    },
    apiHealth: { degraded: true, failedEndpoints },
  };
}

/** Normalize live-state data: missing = not running. */
export function normalizeLiveState(liveData: any): { running: boolean; stage: string } {
  return {
    running: Boolean(liveData?.running ?? false),
    stage: String(liveData?.stage || liveData?.state || "unknown"),
  };
}

// ---------------------------------------------------------------------------
// Graph helpers
// ---------------------------------------------------------------------------

function normalizeGraphFromBrain(brainDetail: any, tasks: RemedyTaskItem[]): { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[] } {
  // Use story + brain data to build journey, then graph
  const journey = normalizeJourney(brainDetail?.story || brainDetail, brainDetail);
  return normalizeGraph(journey, tasks);
}

function buildMinimalGraph(tasks: RemedyTaskItem[]): { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[] } {
  const nodes: RemedyGraphNode[] = tasks.slice(0, 20).map((t, idx) => ({
    id: t.nodeId, label: t.label, kind: t.kind, state: t.state, nodeId: t.nodeId,
    group: t.state === "done" ? "done" : t.state === "current" ? "open" : "planned",
    visibleFromZoom: Math.min(idx, 3), showLabelFromZoom: idx <= 1 ? 0 : 2,
  }));
  const edges: RemedyGraphEdge[] = [];
  for (let i = 0; i < nodes.length - 1; i++) {
    edges.push({
      id: `edge-${nodes[i].id}-${nodes[i + 1].id}`,
      source: nodes[i].id, target: nodes[i + 1].id,
      meaning: "leads to", state: nodes[i + 1].state,
    });
  }
  return { nodes, edges };
}

function buildDefaultPhases(tasks: RemedyTaskItem[]): RemedyPhase[] {
  const doneCount = tasks.filter(t => t.state === "done").length;
  return [
    { id: "job", label: "Job", state: "done", icon: "briefcase" },
    { id: "planning", label: "Planning", state: doneCount > 0 ? "done" : "current", icon: "calendar" },
    { id: "build", label: "Build", state: "pending", icon: "code" },
    { id: "test", label: "Test", state: "pending", icon: "check" },
    { id: "review", label: "Review", state: "pending", icon: "person" },
    { id: "finalized", label: "Finalized", state: "pending", icon: "flag" },
  ];
}

// ---------------------------------------------------------------------------
// Legacy helpers (used only for brain-view-model graph building)
// ---------------------------------------------------------------------------

function normalizeJourney(story: any, brain: any): RemedyJourneyItem[] {
  const src = story?.journey || [];
  if (Array.isArray(src) && src.length) {
    return src.map((i: any, idx: number) => ({
      id: String(i.id || `journey-${idx}`),
      kind: i.kind || "task",
      title: scrubUiText(i.title, humanLabel(i.kind || "task")),
      subtitle: scrubUiText(i.subtitle, ""),
      state: normalizeState(i.state),
      nodeId: String(i.node_id || i.nodeId || i.id || `journey-${idx}`),
      visibleFromZoom: Number(i.visible_from_zoom ?? i.visibleFromZoom ?? Math.min(idx, 3)),
    }));
  }
  const nodes = Array.isArray(brain?.nodes) ? brain.nodes : [];
  const visible = nodes.filter((n: any) => !isDiagnosticsOnly(n.type || n.node_type));
  const root = visible.find((n: any) => n.is_origin) || visible[0];
  const journey: RemedyJourneyItem[] = [];
  if (root) {
    journey.push({
      id: "goal", kind: "goal",
      title: scrubUiText(root.title || root.label || brain?.job_title, "Project goal"),
      subtitle: "The main objective Remedy is working through.",
      state: "current", nodeId: String(root.id), visibleFromZoom: 0,
    });
  }
  visible.slice(0, 8).forEach((n: any, idx: number) => journey.push({
    id: String(n.id || `node-${idx}`),
    kind: n.type === "test_run" ? "test" : n.type === "patch_apply" ? "apply" : n.type === "patch_intent" ? "change" : "task",
    title: scrubUiText(n.title || n.label || humanLabel(n.type || "task"), humanLabel(n.type || "task")),
    subtitle: scrubUiText(n.subtitle || n.summary || "", ""),
    state: normalizeState(n.status || n.state),
    nodeId: String(n.id || `node-${idx}`),
    visibleFromZoom: Math.min(idx + 1, 3),
  }));
  return journey;
}

function normalizeGraph(journey: RemedyJourneyItem[], tasks: RemedyTaskItem[]): { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[] } {
  const nodes: RemedyGraphNode[] = [];
  journey.forEach((i, idx) => nodes.push({
    id: i.nodeId, label: i.title, kind: idx === 0 ? "root" : i.kind, state: i.state, nodeId: i.nodeId,
    group: i.state === "done" ? "done" : i.state === "current" ? "open" : i.state === "suggested" ? "review" : "planned",
    visibleFromZoom: i.visibleFromZoom, showLabelFromZoom: idx <= 1 ? 0 : 2,
  }));
  tasks.slice(0, 80).forEach((t, idx) => {
    if (nodes.some(n => n.id === t.nodeId)) return;
    nodes.push({
      id: t.nodeId, label: t.label, kind: t.kind, state: t.state, nodeId: t.nodeId,
      group: t.state === "done" ? "done" : t.state === "current" ? "open" : t.state === "suggested" ? "review" : "planned",
      visibleFromZoom: Math.min(2 + Math.floor(idx / 8), 4), showLabelFromZoom: idx < 8 ? 2 : 4,
    });
  });
  const edges: RemedyGraphEdge[] = [];
  for (let i = 0; i < journey.length - 1; i++) {
    edges.push({
      id: `edge-${journey[i].nodeId}-${journey[i + 1].nodeId}`,
      source: journey[i].nodeId, target: journey[i + 1].nodeId,
      meaning: "leads to", state: journey[i + 1].state,
    });
  }
  return { nodes, edges };
}

const EVENT_LABELS: Record<string, { actor: RemedyActivityItem["actor"]; kind: RemedyActivityItem["kind"]; label: string }> = {
  task_created: { actor: "Builder", kind: "build", label: "Task created" },
  patch_intent_created: { actor: "Builder", kind: "build", label: "Change proposed" },
  patch_intent_approved: { actor: "User", kind: "user", label: "Change approved" },
  patch_intent_applied: { actor: "Builder", kind: "build", label: "Change applied" },
  test_run_completed: { actor: "Builder", kind: "test", label: "Tests run" },
  proof_collected: { actor: "Builder", kind: "build", label: "Proof collected" },
  review_recommendation: { actor: "Reviewer", kind: "review", label: "Review suggestion" },
  stop_reason_recorded: { actor: "System", kind: "system", label: "Stopped" },
};

function formatEventTime(ts: string): string {
  try {
    const d = new Date(ts);
    const now = Date.now();
    const diffMs = now - d.getTime();
    if (diffMs < 60_000) return "Just now";
    if (diffMs < 3_600_000) return `${Math.round(diffMs / 60_000)}m ago`;
    if (diffMs < 86_400_000) return `${Math.round(diffMs / 3_600_000)}h ago`;
    return d.toLocaleDateString();
  } catch { return ""; }
}
/* eslint-enable @typescript-eslint/no-explicit-any */

// ---------------------------------------------------------------------------
// Main loader: dashboard-first
// ---------------------------------------------------------------------------

export async function loadRemedyDashboard(o: ApiClientOptions): Promise<RemedyDashboard> {
  const base = o.baseUrl || "";
  const q = `token=${encodeURIComponent(o.token)}`;

  // Primary: fetch /dashboard
  let dashboardData: Record<string, unknown> | null = null;
  const failedEndpoints: string[] = [];

  try {
    dashboardData = await fetchJson<Record<string, unknown>>(`${base}/api/jobs/${o.jobId}/dashboard?${q}`);
  } catch {
    failedEndpoints.push("dashboard");
  }

  // If dashboard failed, return degraded state
  if (!dashboardData) {
    return normalizeApiFailure(o.jobId, failedEndpoints);
  }

  // Secondary: brain-view-model for graph rendering detail (optional)
  let brainData: Record<string, unknown> | undefined;
  try {
    brainData = await fetchJson<Record<string, unknown>>(`${base}/api/jobs/${o.jobId}/brain-view-model?${q}`);
  } catch {
    failedEndpoints.push("brain-view-model");
  }

  const result = normalizeDashboardPayload(o.jobId, dashboardData, brainData);

  // Propagate any secondary endpoint failures
  if (failedEndpoints.length > 0) {
    result.apiHealth = {
      degraded: failedEndpoints.includes("dashboard"),
      failedEndpoints,
    };
  }

  return result;
}
