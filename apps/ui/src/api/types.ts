export type RemedyState = "done" | "current" | "pending" | "blocked" | "suggested";
export type RemedyTaskKind = "goal" | "task" | "approval" | "apply" | "test" | "review" | "memory" | "proof" | "change";
export type RemedyMetricKey = "open" | "planned" | "done" | "progress" | "tokens";

export interface RemedyMetric { key: RemedyMetricKey; label: string; value: number; suffix?: string; tooltip?: Record<string, number>; }
export interface RemedyNextAction { label: string; command: string; risk: "low" | "medium" | "high"; requiresHuman: boolean; }
export interface RemedyJourneyItem { id: string; kind: RemedyTaskKind; title: string; subtitle: string; state: RemedyState; nodeId: string; visibleFromZoom: number; }
export interface RemedyTaskItem { id: string; label: string; state: RemedyState; kind: RemedyTaskKind; checked: boolean; muted: boolean; nodeId: string; nextAction?: RemedyNextAction; }
export interface RemedyActivityItem { id: string; actor: "Builder" | "Reviewer" | "User" | "System"; message: string; timeLabel: string; kind: "build" | "review" | "user" | "system" | "test"; }
export interface RemedyGraphNode { id: string; label: string; kind: RemedyTaskKind | "root" | "tiny"; state: RemedyState; nodeId: string; group?: "open" | "planned" | "done" | "review" | "memory"; visibleFromZoom: number; showLabelFromZoom: number; }
export interface RemedyGraphEdge { id: string; source: string; target: string; meaning: string; state: RemedyState; }
export interface RemedyPhase { id: "job" | "planning" | "build" | "test" | "review" | "finalized"; label: string; state: RemedyState; icon: string; }
export interface RemedyLiveState { running: boolean; stage: string; activeTaskLabel: string; latestMessage: string; latestActor: RemedyActivityItem["actor"]; }
export interface RemedyStory { version: number; jobId: string; headline: string; plainStatus: string; description: string; primaryNextAction: RemedyNextAction; progress: { completed: number; active: number; pending: number; blocked: number; needsReview: number; }; journey: RemedyJourneyItem[]; }
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

export interface RemedyDashboard { jobId: string; title: string; description: string; conceptLabel: string; metrics: RemedyMetric[]; phases: RemedyPhase[]; tasks: RemedyTaskItem[]; activity: RemedyActivityItem[]; graph: { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[]; }; nextAction: RemedyNextAction; live: RemedyLiveState; apiHealth: RemedyApiHealth; pipeline: RemedyPipeline | null; resume: RemedyResume | null; projectSummary: RemedyProjectSummary | null; }
