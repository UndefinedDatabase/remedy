// The cost view is imported FROM `./costMetric` and never the other way round:
// that module declares its own input and output types precisely so this import
// direction stays acyclic.
import type { BudgetTickFigures, CostMetricView } from "./costMetric";

export type RemedyState = "done" | "current" | "pending" | "blocked" | "suggested";
export type RemedyTaskKind = "goal" | "task" | "approval" | "apply" | "test" | "review" | "memory" | "proof" | "change";
export type RemedyMetricKey = "open" | "planned" | "done" | "progress" | "tests" | "proof" | "tokens" | "cost";

export interface RemedyMetric {
  key: RemedyMetricKey;
  label: string;
  value: number | "—";
  suffix?: string;
  tooltip?: Record<string, number>;
  /** Latest test outcome — drives the status dot on the tests metric. */
  state?: "pass" | "fail" | "none";
  /** True when the value is not derivable (e.g. data root unavailable). */
  unknown?: boolean;
  /** Present only on the `cost` metric. `value`, `suffix` and `tooltip` cannot
   *  hold a limit, a basis or a threshold, so the whole cost reading arrives as
   *  one already-decided view — see DECISION F022 D4. */
  cost?: CostMetricView;
}

/** Safe aggregate snapshot / apply-record truth. "unknown" when data root is unavailable. */
export interface RemedySnapshotSummary {
  applyRecords: number | "unknown";
  verified: number | "unknown";
  reverted: number | "unknown";
  driftDetected: boolean | "unknown";
  source: string;
}

/** Safe continuation summary derived from do_continue events + approved intents. */
export interface RemedyContinuationSummary {
  available: boolean | "unknown";
  lastResult: string;
  lastStopReason: string;
}
export interface RemedyNextAction { label: string; command: string; risk: "low" | "medium" | "high"; requiresHuman: boolean; }
export interface RemedyJourneyItem { id: string; kind: RemedyTaskKind; title: string; subtitle: string; state: RemedyState; nodeId: string; visibleFromZoom: number; }
export interface RemedyTaskItem { id: string; label: string; state: RemedyState; kind: RemedyTaskKind; checked: boolean; muted: boolean; nodeId: string; nextAction?: RemedyNextAction; outcomeSummary?: string; changedFilesCount?: number; changedFilesSafe?: string[]; testStatus?: string; proofStatus?: string; applyStatus?: string; blockedReason?: string; completedAt?: string; }
export interface RemedyActivityItem { id: string; actor: "Builder" | "Reviewer" | "User" | "System"; message: string; timeLabel: string; kind: "build" | "review" | "user" | "system" | "test"; taskId?: string; tokenEstimate?: number; }

export type RemedyPromptRole = "builder" | "reviewer" | "system";
export type RemedyPromptKind = "initial" | "review" | "repair" | "re-review" | "unknown";

/** One captured prompt from a task-level prompt_trace.jsonl (already redacted). */
export interface RemedyPromptTraceItem {
  id: string;
  taskId: string;
  runId: string;
  round: number;
  role: RemedyPromptRole;
  promptKind: RemedyPromptKind;
  provider: string;
  providerKind: string;
  promptSha256: string;
  promptChars: number;
  promptTokensEstimated: number;
  contextCategories: string[];
  changedFilesSafe: string[];
  safeDiffFiles: string[];
  evidenceRef: string;
  redactedPreview: string;
  redactedPreviewTruncated: boolean;
  findingIds?: string[];
}

/** Aggregate prompt-trace section. "absent" source carries a missingReason. */
export interface RemedyPromptTraceSummary {
  totalPrompts: number;
  builderPrompts: number;
  reviewerPrompts: number;
  repairPrompts: number;
  totalPromptTokensEstimated: number;
  items: RemedyPromptTraceItem[];
  source: string;
  missingReason?: string;
}
export interface RemedyGraphNode { id: string; label: string; kind: RemedyTaskKind | "root" | "tiny"; state: RemedyState; nodeId: string; group?: "open" | "planned" | "done" | "review" | "memory"; visibleFromZoom: number; showLabelFromZoom: number; }
export interface RemedyGraphEdge { id: string; source: string; target: string; meaning: string; state: RemedyState; }
export interface RemedyPhase { id: "job" | "planning" | "build" | "test" | "review" | "finalized"; label: string; state: RemedyState; icon: string; }
export interface RemedyLiveState { running: boolean; stage: string; activeTaskLabel: string; latestMessage: string; latestActor: RemedyActivityItem["actor"]; }
export interface RemedyStory { version: number; jobId: string; headline: string; plainStatus: string; description: string; primaryNextAction: RemedyNextAction; progress: { completed: number; active: number; pending: number; blocked: number; needsReview: number; }; journey: RemedyJourneyItem[]; }
export type RemedyTimelinePhase = "job" | "planning" | "build" | "test" | "review" | "finalized";
export type RemedyTimelineEventKind = "llm_action" | "test" | "review";
export interface RemedyTimelineEvent {
  id: string;
  phase: RemedyTimelinePhase;
  kind: RemedyTimelineEventKind;
  title: string;
  state: RemedyState;
  cycle?: number;
  timeLabel?: string;
}
export type RemedyProposedTaskSource = "user" | "reviewer" | "orchestrator" | "model";
export type RemedyProposedTaskStatus = "proposed" | "evaluated" | "approved_for_build" | "rejected" | "deferred";
export interface RemedyProposedTask {
  id: string;
  title: string;
  reason: string;
  source: RemedyProposedTaskSource;
  risk: "low" | "medium" | "high";
  evaluationStatus: RemedyProposedTaskStatus;
  approvalRequired: boolean;
}
export interface RemedyApiHealth { degraded: boolean; failedEndpoints: string[]; }

export type PipelineStepState = "done" | "current" | "blocked" | "failed" | "skipped" | "unknown" | "waiting";

export interface PipelineSourceContext {
  injected: boolean;
  file_count?: number;
  test_file_count?: number;
  estimated_tokens?: number;
  truncated?: boolean;
  selection_hash?: string;
}

export interface PipelineMemory {
  used: boolean;
  item_count: number;
  truncated: boolean;
  context_hash: string;
}

export interface PipelineRepairLoop {
  used: boolean;
  cycle_count: number;
  max_cycles: number;
}

export interface PipelineStep {
  id: string;
  label: string;
  state: PipelineStepState;
  detail?: string;
}

export interface RemedyPipeline {
  version: number;
  provider: string | null;
  provider_mode: string;
  source_context: PipelineSourceContext;
  memory: PipelineMemory;
  structured_patch_attempted: boolean;
  parse_success: boolean | null;
  parse_error_kind: string;
  intent_id: string;
  intent_status: string;
  approval_required: boolean;
  approval_status: string;
  source_apply_status: string;
  tests_status: string;
  tests_passed: boolean | null;
  repair_loop: PipelineRepairLoop;
  stop_reason: string;
  stop_reason_label: string;
  next_command: string;
  stale: boolean;
  source: string;
  steps: PipelineStep[];
}

export interface RemedyResumeCheckpoint {
  id: string;
  kind: string;
  label: string;
  next_command: string;
}

export interface RemedyResume {
  replay_available: boolean;
  replay_degraded: boolean;
  latest_checkpoint: RemedyResumeCheckpoint | null;
  checkpoint_count: number;
  safe_checkpoint_count: number;
  can_resume: boolean;
  blocked_reason: string;
}

export interface RemedyProjectSummary {
  project_id: string;
  job_count: number;
  active_job_count: number;
  blocked_job_count: number;
  current_focus: string;
  top_blocker: string;
  repeated_pattern_count: number;
  model_quality_confidence: string;
  suggested_next_step: string;
  next_command: string;
  redaction: string;
}

export interface RemedyWorkerStatus {
  worker_available: boolean;
  worker_id: string;
  lifecycle_state: string;
  current_job_id: string;
  queue_count: number;
  heartbeat_at: string;
  stale: boolean;
  why_it_stopped: string;
  next_command: string;
  redaction: string;
}

/** `budgetFinal` is the LEDGER's own last budget tick, served as the dashboard's
 *  `budget_final` (DECISION F022 D7). It is carried as the arriving payload
 *  rather than as a decided view because `costReconciliation.ts` hands it to
 *  `costMetricOf` unread — see DECISION F022 D8 clause 2. `null` means the job
 *  emitted no tick at all, which stays absent rather than becoming a zero. */
export interface RemedyDashboard { jobId: string; title: string; description: string; conceptLabel: string; metrics: RemedyMetric[]; budgetFinal: BudgetTickFigures | null; phases: RemedyPhase[]; tasks: RemedyTaskItem[]; activity: RemedyActivityItem[]; graph: { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[]; }; nextAction: RemedyNextAction; live: RemedyLiveState; apiHealth: RemedyApiHealth; pipeline: RemedyPipeline | null; resume: RemedyResume | null; projectSummary: RemedyProjectSummary | null; workerStatus: RemedyWorkerStatus | null; timelineEvents?: RemedyTimelineEvent[]; snapshot: RemedySnapshotSummary | null; continuation: RemedyContinuationSummary | null; promptTrace?: RemedyPromptTraceSummary | null; }
