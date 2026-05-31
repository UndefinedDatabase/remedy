export type RemedyState = "done" | "current" | "pending" | "blocked" | "suggested";
export type RemedyTaskKind = "goal" | "task" | "approval" | "apply" | "test" | "review" | "memory" | "proof" | "change";
export type RemedyMetricKey = "open" | "planned" | "done" | "progress";

export interface RemedyMetric { key: RemedyMetricKey; label: string; value: number; suffix?: string; }
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
export interface RemedyDashboard { jobId: string; title: string; description: string; conceptLabel: string; metrics: RemedyMetric[]; phases: RemedyPhase[]; tasks: RemedyTaskItem[]; activity: RemedyActivityItem[]; graph: { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[]; }; nextAction: RemedyNextAction; live: RemedyLiveState; apiHealth: RemedyApiHealth; }
