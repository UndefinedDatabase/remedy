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

function buildMetrics(tasks: RemedyTaskItem[]): RemedyMetric[] {
  const done = tasks.filter(t => t.state === "done").length;
  const open = tasks.filter(t => t.state === "current" || t.state === "blocked").length;
  const planned = tasks.filter(t => t.state === "pending" || t.state === "suggested").length;
  const progress = Math.round((done / Math.max(tasks.length, 1)) * 100);
  return [
    { key: "open", label: "Open", value: open },
    { key: "planned", label: "Planned", value: planned },
    { key: "done", label: "Done", value: done },
    { key: "progress", label: "Progress", value: progress, suffix: "%" },
  ];
}

function buildPhases(tasks: RemedyTaskItem[]): RemedyPhase[] {
  const hasTests = tasks.some(t => t.kind === "test");
  const hasReview = tasks.some(t => t.kind === "review" || t.state === "suggested");
  const doneCount = tasks.filter(t => t.state === "done").length;
  const currentId = hasReview ? "review" : hasTests ? "test" : doneCount > 0 ? "build" : "planning";
  return [
    { id: "job", label: "Job", state: "done", icon: "briefcase" },
    { id: "planning", label: "Planning", state: doneCount > 0 ? "done" : "current", icon: "calendar" },
    { id: "build", label: "Build", state: currentId === "build" ? "current" : doneCount > 0 ? "done" : "pending", icon: "code" },
    { id: "test", label: "Test", state: currentId === "test" ? "current" : hasTests ? "done" : "pending", icon: "check" },
    { id: "review", label: "Review", state: currentId === "review" ? "current" : hasReview ? "done" : "pending", icon: "person" },
    { id: "finalized", label: "Finalized", state: tasks.length > 0 && tasks.every(t => t.state === "done") ? "done" : "pending", icon: "flag" },
  ];
}

/* eslint-disable @typescript-eslint/no-explicit-any */
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

function normalizeTasks(progress: any, journey: RemedyJourneyItem[]): RemedyTaskItem[] {
  const src = progress?.items || progress?.checklist || progress?.tasks || [];
  const tasks = src.map((i: any, idx: number) => {
    const kind = (i.kind || i.type || "task") as RemedyTaskItem["kind"];
    const state = normalizeState(i.state || i.status || (i.checked ? "done" : "pending"));
    return {
      id: scrubUiText(i.id || `task-${idx}`, `task-${idx}`),
      label: (() => { const raw = scrubUiText(i.label || i.title || i.short_reason || humanLabel(kind), humanLabel(kind)); return isWeakLabel(raw) ? humanFallbackFor(kind, idx) : raw; })(),
      state, kind,
      checked: Boolean(i.checked ?? i.verified ?? state === "done"),
      muted: Boolean(i.muted ?? (state === "pending" || state === "suggested")),
      nodeId: String(i.node_id || i.related_node_id || i.nodeId || i.id || `task-${idx}`),
      nextAction: i.next_action ? {
        label: scrubUiText(i.next_action.label, "Review next action"),
        command: scrubUiText(i.next_action.command, "remedy dev status"),
        risk: i.next_action.risk || "low",
        requiresHuman: Boolean(i.next_action.requires_human ?? true),
      } : undefined,
    };
  });
  if (tasks.length) return tasks;
  return journey.map(i => ({
    id: i.id, label: i.title, state: i.state, kind: i.kind,
    checked: i.state === "done", muted: i.state === "pending" || i.state === "suggested",
    nodeId: i.nodeId, nextAction: nextAction(),
  }));
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

function normalizeActivity(live: any, tasks: RemedyTaskItem[], events?: any): RemedyActivityItem[] {
  // Derive from real event ledger if available
  const eventList = Array.isArray(events?.events) ? events.events : [];
  if (eventList.length > 0) {
    return eventList.slice(-4).reverse().map((e: any, idx: number) => {
      const meta = EVENT_LABELS[e.event] || { actor: "System" as const, kind: "system" as const, label: e.event };
      return {
        id: `event-${idx}`,
        actor: meta.actor,
        message: meta.label,
        timeLabel: e.timestamp ? formatEventTime(e.timestamp) : "",
        kind: meta.kind,
      };
    });
  }

  // Fallback: derive from live state
  const isIdle = !live?.running && !live?.latest_message && !live?.latestMessage;
  if (isIdle) return [];

  const items: RemedyActivityItem[] = [];
  const msg = live?.latestMessage || live?.latest_message;
  if (msg) {
    items.push({ id: "now", actor: "Builder", message: scrubUiText(msg, "Working."), timeLabel: "Just now", kind: "build" });
  } else {
    const active = tasks.find(t => t.state === "current");
    if (active) {
      items.push({ id: "now", actor: "Builder", message: `Working on ${active.label}`, timeLabel: "Just now", kind: "build" });
    }
  }
  return items;
}

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

export async function loadRemedyDashboard(o: ApiClientOptions): Promise<RemedyDashboard> {
  const base = o.baseUrl || "";
  const q = `token=${encodeURIComponent(o.token)}`;
  const [brain, progress, live, story, eventsSince] = await Promise.allSettled([
    fetchJson<Record<string, unknown>>(`${base}/api/jobs/${o.jobId}/brain-view-model?${q}`),
    fetchJson<Record<string, unknown>>(`${base}/api/jobs/${o.jobId}/task-progress?${q}`),
    fetchJson<Record<string, unknown>>(`${base}/api/jobs/${o.jobId}/live-state?${q}`),
    fetchJson<Record<string, unknown>>(`${base}/api/jobs/${o.jobId}/story?${q}`),
    fetchJson<Record<string, unknown>>(`${base}/api/jobs/${o.jobId}/events-since?cursor=0&${q}`),
  ]);
  const brainData: Record<string, unknown> = brain.status === "fulfilled" ? brain.value : {};
  const progressData: Record<string, unknown> = progress.status === "fulfilled" ? progress.value : {};
  const liveData: Record<string, unknown> = live.status === "fulfilled" ? live.value : {};
  const storyData: Record<string, unknown> = story.status === "fulfilled" ? story.value : (brainData?.story as Record<string, unknown>) || {};
  const eventsData: Record<string, unknown> = eventsSince.status === "fulfilled" ? eventsSince.value : {};
  const journey = normalizeJourney(storyData, brainData);
  const tasks = normalizeTasks(progressData, journey);
  const graph = normalizeGraph(journey, tasks);
  return {
    jobId: o.jobId,
    title: scrubUiText(storyData?.headline || brainData?.title || brainData?.job_title, "Growing Brain Overview"),
    description: scrubUiText(storyData?.description || brainData?.description || "An AI agent working through a verified project plan.", "An AI agent working through a verified project plan."),
    conceptLabel: "Concept 01 of 10",
    metrics: buildMetrics(tasks),
    phases: buildPhases(tasks),
    tasks,
    activity: normalizeActivity(liveData, tasks, eventsData),
    graph,
    nextAction: (storyData?.primary_next_action as Record<string, unknown>)
      ? {
          label: scrubUiText((storyData.primary_next_action as Record<string, unknown>).label, "Review project state"),
          command: scrubUiText((storyData.primary_next_action as Record<string, unknown>).command, "remedy dev status"),
          risk: ((storyData.primary_next_action as Record<string, unknown>).risk as RemedyDashboard["nextAction"]["risk"]) || "low",
          requiresHuman: Boolean((storyData.primary_next_action as Record<string, unknown>).requires_human ?? true),
        }
      : nextAction(),
    live: {
      running: Boolean(liveData?.running ?? true),
      stage: scrubUiText(liveData?.stage, "live"),
      activeTaskLabel: tasks.find(t => t.state === "current")?.label || "Waiting for next safe action",
      latestMessage: scrubUiText(liveData?.latest_message || liveData?.latestMessage, "Project state updated."),
      latestActor: "Builder",
    },
  };
}
