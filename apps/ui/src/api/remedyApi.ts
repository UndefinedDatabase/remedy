import { humanLabel, isDiagnosticsOnly, scrubUiText } from "../copy/humanCopy";
import type { PipelineStep, PipelineStepState, RemedyActivityItem, RemedyContinuationSummary, RemedyDashboard, RemedyGraphEdge, RemedyGraphNode, RemedyJourneyItem, RemedyMetric, RemedyNextAction, RemedyPhase, RemedyPipeline, RemedyPromptKind, RemedyPromptRole, RemedyPromptTraceItem, RemedyPromptTraceSummary, RemedySnapshotSummary, RemedyState, RemedyTaskItem, RemedyTimelineEvent, RemedyTimelineEventKind, RemedyTimelinePhase } from "./types";

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
      outcomeSummary: t.outcome_summary || undefined,
      changedFilesCount: typeof t.changed_files_count === "number" ? t.changed_files_count : undefined,
      changedFilesSafe: Array.isArray(t.changed_files_safe) ? t.changed_files_safe : undefined,
      testStatus: t.test_status || undefined,
      proofStatus: t.proof_status || undefined,
      applyStatus: t.apply_status || undefined,
      blockedReason: t.blocked_reason || undefined,
      completedAt: t.completed_at || undefined,
    };
  });

  // Metrics from dashboard
  const dm = dashboard.metrics || {};
  const tu = dashboard.token_usage || {};
  const tokenTotal = tu.known ? (tu.total_tokens ?? 0) : 0;
  const tokenKnown = Boolean(tu.known) && tokenTotal > 0;
  const tokenTooltip = tu.by_role && Object.keys(tu.by_role).length > 0 ? tu.by_role : undefined;
  const metrics: RemedyMetric[] = [
    { key: "open", label: "Open", value: dm.open ?? 0 },
    { key: "planned", label: "Planned", value: dm.planned ?? 0 },
    { key: "done", label: "Done", value: dm.done ?? 0 },
    { key: "progress", label: "Progress", value: dm.progress_percent ?? 0, suffix: "%" },
    metricTests(dm.tests),
    metricProof(dm.proof),
    { key: "tokens", label: "Tokens", value: tokenKnown ? tokenTotal : "—", tooltip: tokenTooltip, unknown: !tokenKnown },
    // The eighth tile. It is `unknown` at load because no budget tick has
    // arrived yet, which is the honest em dash ux_spec.md §10 requires for a
    // value that is not yet derivable — never a fake zero. `metricsWithCostTicker`
    // fills it from the live stream in the shell (DECISION F022 D6).
    { key: "cost", label: "Cost", value: "—", unknown: true },
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
    const promptKind = String(a.prompt_kind ?? a.promptKind ?? "");
    // A re-review prompt is a follow-up review pass; surface it distinctly.
    const label = promptKind === "re-review" ? "Re-review requested" : meta.label;
    const taskId = String(a.task_id ?? a.taskId ?? "");
    const tokenEstimate = a.token_estimate ?? a.tokenEstimate;
    return {
      id: a.id || `event-${idx}`,
      actor: meta.actor,
      message: scrubUiText(label || a.summary, ""),
      timeLabel: a.time ? formatEventTime(a.time) : "",
      kind: meta.kind,
      taskId: taskId || undefined,
      tokenEstimate: typeof tokenEstimate === "number" ? tokenEstimate : undefined,
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
    // The ledger's last budget tick, carried OPAQUELY: this mapper reads no
    // figure out of it and decides nothing about it, which is what keeps
    // `costMetric.ts` the single client-side arithmetic home. An absent section
    // stays absent as `null` — never an empty object, never a zero.
    budgetFinal: dashboard.budget_final ?? null,
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
    pipeline: normalizePipeline(dashboard.pipeline),
    resume: dashboard.resume ?? null,
    projectSummary: dashboard.project_summary ?? null,
    workerStatus: dashboard.worker ?? null,
    timelineEvents: normalizeTimelineEvents(dashboard.timeline_events),
    snapshot: normalizeSnapshotSummary(dashboard.snapshot),
    continuation: normalizeContinuationSummary(dashboard.continuation),
    promptTrace: normalizePromptTrace(dashboard.prompt_trace),
  };
}

// ---------------------------------------------------------------------------
// Cockpit metric + summary helpers (Step 1182)
// ---------------------------------------------------------------------------

/** Tests metric: value = passed runs, dot = latest outcome. Always derivable. */
function metricTests(raw: any): RemedyMetric {
  const t = raw || {};
  const state = (["pass", "fail", "none"].includes(t.latest_state) ? t.latest_state : "none") as RemedyMetric["state"];
  return { key: "tests", label: "Tests", value: typeof t.passed === "number" ? t.passed : 0, state };
}

/** Proof metric: value = verified, suffix = /total. "—" when not derivable. */
function metricProof(raw: any): RemedyMetric {
  const p = raw || {};
  const unknown = p.state === "unknown" || typeof p.verified !== "number" || typeof p.total_changes !== "number";
  if (unknown) return { key: "proof", label: "Proof", value: "—", unknown: true };
  return { key: "proof", label: "Proof", value: p.verified, suffix: `/${p.total_changes}` };
}

/** Snapshot summary: pass through with explicit unknown markers, never faked. */
function normalizeSnapshotSummary(raw: any): RemedySnapshotSummary | null {
  if (!raw || typeof raw !== "object") return null;
  const num = (v: any): number | "unknown" => (typeof v === "number" ? v : "unknown");
  return {
    applyRecords: num(raw.apply_records),
    verified: num(raw.verified),
    reverted: num(raw.reverted),
    driftDetected: typeof raw.drift_detected === "boolean" ? raw.drift_detected : "unknown",
    source: String(raw.source || "unavailable"),
  };
}

/** Continuation summary: pass through with explicit unknown markers. */
function normalizeContinuationSummary(raw: any): RemedyContinuationSummary | null {
  if (!raw || typeof raw !== "object") return null;
  return {
    available: typeof raw.available === "boolean" ? raw.available : "unknown",
    lastResult: String(raw.last_result || "none"),
    lastStopReason: String(raw.last_stop_reason || "none"),
  };
}

// ---------------------------------------------------------------------------
// Prompt trace normalization
// ---------------------------------------------------------------------------

const VALID_PROMPT_ROLES: RemedyPromptRole[] = ["builder", "reviewer", "system"];
const VALID_PROMPT_KINDS: RemedyPromptKind[] = ["initial", "review", "repair", "re-review", "unknown"];

function normalizePromptRole(raw: unknown): RemedyPromptRole {
  const s = String(raw ?? "").toLowerCase();
  return VALID_PROMPT_ROLES.includes(s as RemedyPromptRole) ? (s as RemedyPromptRole) : "system";
}

function normalizePromptKind(raw: unknown): RemedyPromptKind {
  const s = String(raw ?? "").toLowerCase();
  return VALID_PROMPT_KINDS.includes(s as RemedyPromptKind) ? (s as RemedyPromptKind) : "unknown";
}

function asNum(raw: unknown): number {
  return typeof raw === "number" && Number.isFinite(raw) ? raw : 0;
}

function asStrArray(raw: unknown): string[] {
  return Array.isArray(raw) ? raw.map((x) => String(x)) : [];
}

/** Map one prompt-trace item, accepting snake_case or camelCase keys. */
function normalizePromptTraceItem(raw: any, idx: number): RemedyPromptTraceItem {
  const item: RemedyPromptTraceItem = {
    id: String(raw.id ?? `prompt-${idx}`),
    taskId: String(raw.taskId ?? raw.task_id ?? ""),
    runId: String(raw.runId ?? raw.run_id ?? ""),
    round: asNum(raw.round),
    role: normalizePromptRole(raw.role),
    promptKind: normalizePromptKind(raw.promptKind ?? raw.prompt_kind),
    provider: String(raw.provider ?? ""),
    providerKind: String(raw.providerKind ?? raw.provider_kind ?? ""),
    promptSha256: String(raw.promptSha256 ?? raw.prompt_sha256 ?? ""),
    promptChars: asNum(raw.promptChars ?? raw.prompt_chars),
    promptTokensEstimated: asNum(raw.promptTokensEstimated ?? raw.prompt_tokens_estimated),
    contextCategories: asStrArray(raw.contextCategories ?? raw.context_categories),
    changedFilesSafe: asStrArray(raw.changedFilesSafe ?? raw.changed_files_safe),
    safeDiffFiles: asStrArray(raw.safeDiffFiles ?? raw.safe_diff_files),
    evidenceRef: String(raw.evidenceRef ?? raw.evidence_ref ?? ""),
    redactedPreview: String(raw.redactedPreview ?? raw.redacted_preview ?? ""),
    redactedPreviewTruncated: Boolean(raw.redactedPreviewTruncated ?? raw.redacted_preview_truncated ?? false),
  };
  const findingIds = raw.findingIds ?? raw.finding_ids;
  if (Array.isArray(findingIds) && findingIds.length) {
    item.findingIds = findingIds.map((x: unknown) => String(x));
  }
  return item;
}

/** Normalize the dashboard prompt-trace section; null when absent entirely. */
export function normalizePromptTrace(raw: any): RemedyPromptTraceSummary | null {
  if (!raw || typeof raw !== "object") return null;
  const items = Array.isArray(raw.items) ? raw.items.map(normalizePromptTraceItem) : [];
  const summary: RemedyPromptTraceSummary = {
    totalPrompts: asNum(raw.totalPrompts ?? raw.total_prompts),
    builderPrompts: asNum(raw.builderPrompts ?? raw.builder_prompts),
    reviewerPrompts: asNum(raw.reviewerPrompts ?? raw.reviewer_prompts),
    repairPrompts: asNum(raw.repairPrompts ?? raw.repair_prompts),
    totalPromptTokensEstimated: asNum(raw.totalPromptTokensEstimated ?? raw.total_prompt_tokens_estimated),
    items,
    source: String(raw.source ?? "absent"),
  };
  const missingReason = raw.missingReason ?? raw.missing_reason;
  if (missingReason) summary.missingReason = String(missingReason);
  return summary;
}

/** Normalize API failure into degraded RemedyDashboard. */
export function normalizeApiFailure(jobId: string, failedEndpoints: string[]): RemedyDashboard {
  return {
    jobId,
    title: "Mission Control",
    description: "",
    conceptLabel: "",
    // Remedy deliberately does NOT give the degraded path a `cost` tile, and
    // this is where a reader would search for it: a dashboard whose endpoints
    // failed has no stream figures either, so a cost tile here would be a
    // promise this path cannot keep. `metricsWithCostTicker` returns an array
    // with no cost entry unchanged and by reference, which is what makes the
    // absence safe rather than merely tolerated.
    metrics: [
      { key: "open", label: "Open", value: 0 },
      { key: "planned", label: "Planned", value: 0 },
      { key: "done", label: "Done", value: 0 },
      { key: "progress", label: "Progress", value: 0, suffix: "%" },
    ],
    // No endpoint answered, so there is no ledger figure either.
    budgetFinal: null,
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
    pipeline: null,
    resume: null,
    projectSummary: null,
    workerStatus: null,
    snapshot: null,
    continuation: null,
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

// ---------------------------------------------------------------------------
// Timeline event normalization
// ---------------------------------------------------------------------------

const VALID_TIMELINE_PHASES: RemedyTimelinePhase[] = ["job", "planning", "build", "test", "review", "finalized"];
const VALID_TIMELINE_KINDS: RemedyTimelineEventKind[] = ["llm_action", "test", "review"];

function normalizeTimelinePhase(raw: unknown): RemedyTimelinePhase {
  const s = String(raw || "").toLowerCase();
  return VALID_TIMELINE_PHASES.includes(s as RemedyTimelinePhase) ? (s as RemedyTimelinePhase) : "build";
}

function normalizeTimelineEventKind(raw: unknown): RemedyTimelineEventKind {
  const s = String(raw || "").toLowerCase();
  return VALID_TIMELINE_KINDS.includes(s as RemedyTimelineEventKind) ? (s as RemedyTimelineEventKind) : "llm_action";
}

function normalizeTimelineEvents(raw: any): RemedyTimelineEvent[] {
  if (!Array.isArray(raw)) return [];
  return raw.map((e: any, idx: number) => ({
    id: scrubUiText(e.id || `te-${idx}`, `te-${idx}`),
    phase: normalizeTimelinePhase(e.phase),
    kind: normalizeTimelineEventKind(e.kind),
    title: scrubUiText(e.title || e.label || "Timeline event", "Timeline event"),
    state: e.state ? normalizeState(e.state) : (e.done ? "done" as const : "pending" as const),
    cycle: typeof e.cycle === "number" ? e.cycle : undefined,
    timeLabel: (e.time_label || e.timeLabel) ? scrubUiText(e.time_label || e.timeLabel, "") : undefined,
  }));
}

// ---------------------------------------------------------------------------
// Pipeline normalization
// ---------------------------------------------------------------------------

function pipelineStepState(done: boolean | null, blocked: boolean, failed: boolean, skipped: boolean): PipelineStepState {
  if (failed) return "failed";
  if (blocked) return "blocked";
  if (skipped) return "skipped";
  if (done === true) return "done";
  if (done === false) return "waiting";
  return "unknown";
}

function buildPipelineSteps(p: any): PipelineStep[] {
  const steps: PipelineStep[] = [];
  const hasProvider = p.provider !== null;
  const hasContext = p.source_context?.injected === true;
  const hasMemory = p.memory?.used === true;
  const hasPatch = p.structured_patch_attempted === true;
  const parsed = p.parse_success === true;
  const parseFailed = p.parse_success === false;
  const hasIntent = p.intent_status !== "none" && p.intent_status !== "";
  const approved = p.approval_status === "approved";
  const applied = p.source_apply_status === "applied";
  const tested = p.tests_status !== "none";
  const testPassed = p.tests_passed === true;
  const repairUsed = p.repair_loop?.used === true;

  steps.push({ id: "provider", label: hasProvider ? `Provider: ${p.provider}` : "No provider", state: hasProvider ? "done" : "skipped" });
  steps.push({ id: "context", label: "Source context", state: pipelineStepState(hasContext, false, false, !hasProvider), detail: hasContext ? `${p.source_context.file_count ?? 0} files, ~${p.source_context.estimated_tokens ?? 0} tokens` : undefined });
  steps.push({ id: "memory", label: "Memory", state: pipelineStepState(hasMemory, false, false, !hasMemory), detail: hasMemory ? `${p.memory.item_count} items` : undefined });
  steps.push({ id: "patch", label: "Structured patch", state: pipelineStepState(hasPatch && parsed, false, parseFailed, !hasPatch), detail: parseFailed ? p.parse_error_kind || "Parse failed" : undefined });
  steps.push({ id: "intent", label: "Patch intent", state: pipelineStepState(hasIntent, p.approval_required && !approved, false, !hasIntent) });
  steps.push({ id: "approval", label: "Approval", state: pipelineStepState(approved, p.approval_required && !approved, false, !p.approval_required && !approved), detail: p.approval_required && !approved ? "Human approval required" : undefined });
  steps.push({ id: "apply", label: "Apply", state: pipelineStepState(applied, false, p.source_apply_status === "failed", !applied && !approved) });
  steps.push({ id: "test", label: "Test", state: pipelineStepState(testPassed, false, tested && !testPassed, !tested), detail: tested && !testPassed ? "Tests failed" : undefined });
  if (repairUsed) {
    steps.push({ id: "repair", label: "Repair loop", state: pipelineStepState(testPassed, false, !testPassed, false), detail: `Cycle ${p.repair_loop.cycle_count}/${p.repair_loop.max_cycles}` });
  }
  return steps;
}

export function normalizePipeline(raw: any): RemedyPipeline | null {
  if (!raw || typeof raw !== "object") return null;
  return {
    version: raw.version ?? 1,
    provider: raw.provider ?? null,
    provider_mode: raw.provider_mode ?? "none",
    source_context: raw.source_context ?? { injected: false },
    memory: raw.memory ?? { used: false, item_count: 0, truncated: false, context_hash: "" },
    structured_patch_attempted: Boolean(raw.structured_patch_attempted),
    parse_success: raw.parse_success ?? null,
    parse_error_kind: raw.parse_error_kind ?? "",
    intent_id: raw.intent_id ?? "",
    intent_status: raw.intent_status ?? "none",
    approval_required: Boolean(raw.approval_required),
    approval_status: raw.approval_status ?? "none",
    source_apply_status: raw.source_apply_status ?? "none",
    tests_status: raw.tests_status ?? "none",
    tests_passed: raw.tests_passed ?? null,
    repair_loop: raw.repair_loop ?? { used: false, cycle_count: 0, max_cycles: 0 },
    stop_reason: raw.stop_reason ?? "",
    stop_reason_label: raw.stop_reason_label ?? "",
    next_command: raw.next_command ?? "",
    stale: Boolean(raw.stale),
    source: raw.source ?? "unknown",
    steps: buildPipelineSteps(raw),
  };
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
  builder_prompt_created: { actor: "Builder", kind: "build", label: "Builder prompt sent" },
  reviewer_prompt_created: { actor: "Reviewer", kind: "review", label: "Reviewer prompt sent" },
  repair_prompt_created: { actor: "Builder", kind: "build", label: "Repair prompt sent" },
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
