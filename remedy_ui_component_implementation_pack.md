# Remedy UI Full Rebuild — Component Implementation Pack

This file is meant to be copied to the coding agent together with the implementation prompt. It converts the reference screen into a concrete React 19 + TypeScript + MUI + CSS Modules + React Flow implementation.

The old UI is not to be polished. It should be removed from the default product path. The new default UI is a human-facing dashboard.

## Hard rule

Default UI must never show: `rank`, `importance`, `node_type`, `metadata`, `present signals`, `missing signals`, `context coverage`, `zone`, `edge_type`, `connected_to`, raw UUID labels, raw JSON, raw stdout/stderr, command output, diff preview, approval reason, tracebacks.

## Tech

Use React 19, TypeScript, MUI, `@mui/icons-material`, `@xyflow/react`, Vite, ESLint, CSS Modules. No CDN, no external fonts, no Tailwind for this screen, no old static viewer as primary UI.

## Target files

```txt
apps/ui/
  package.json
  tsconfig.json
  eslint.config.js
  index.html
  src/
    main.tsx
    RemedyApp.tsx
    api/types.ts
    api/remedyApi.ts
    copy/humanCopy.ts
    styles/tokens.css
    styles/globals.css
    components/shell/RemedyShell.tsx
    components/shell/RemedyShell.module.css
    components/shell/ReducedMotionProvider.tsx
    components/rail/LeftBrandRail.tsx
    components/rail/LeftBrandRail.module.css
    components/rail/RemedyLogo.tsx
    components/rail/RemedyLogo.module.css
    components/rail/SideIconDock.tsx
    components/rail/SideIconDock.module.css
    components/metrics/TopMetricsBar.tsx
    components/metrics/TopMetricsBar.module.css
    components/command/CommandBar.tsx
    components/command/CommandBar.module.css
    components/graph/BrainGraphStage.tsx
    components/graph/BrainGraphStage.module.css
    components/graph/RemedyBrainFlow.tsx
    components/graph/RemedyBrainFlow.module.css
    components/graph/GraphFilterChips.tsx
    components/graph/GraphFilterChips.module.css
    components/graph/GraphNodes.tsx
    components/graph/GraphNodes.module.css
    components/graph/SoftGlowEdge.tsx
    components/graph/organicLayout.ts
    components/graph/semanticZoom.ts
    components/panels/RightLivePanel.tsx
    components/panels/RightLivePanel.module.css
    components/panels/LiveStatusPill.tsx
    components/panels/AgentNowCard.tsx
    components/panels/ActivityFeedCard.tsx
    components/panels/TaskChecklistCard.tsx
    components/panels/AddTaskButton.tsx
    components/timeline/PhaseTimeline.tsx
    components/timeline/PhaseTimeline.module.css
    components/detail/DetailPopover.tsx
    components/detail/DetailPopover.module.css
    components/layers/LayerSwitcher.tsx
    components/layers/LayerSwitcher.module.css
    components/icons/NetworkLogoIcon.tsx
    components/icons/CodeOrbIcon.tsx
```

---

## 1. package.json

```json
{
  "name": "@remedy/ui",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite --host 127.0.0.1",
    "build": "vite build",
    "preview": "vite preview --host 127.0.0.1",
    "lint": "eslint src --ext .ts,.tsx",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@emotion/react": "^11.13.5",
    "@emotion/styled": "^11.13.5",
    "@mui/icons-material": "^6.4.0",
    "@mui/material": "^6.4.0",
    "@xyflow/react": "^12.4.4",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@eslint/js": "^9.18.0",
    "@types/react": "^19.0.7",
    "@types/react-dom": "^19.0.3",
    "@vitejs/plugin-react": "^4.3.4",
    "eslint": "^9.18.0",
    "eslint-plugin-react-hooks": "^5.1.0",
    "typescript": "^5.7.3",
    "vite": "^6.0.7",
    "vitest": "^2.1.8"
  }
}
```

---

## 2. index.html

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Remedy</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## 3. styles/tokens.css

```css
:root {
  --remedy-bg: #edf3fb;
  --remedy-bg-2: #f8fbff;
  --remedy-blue-950: #071b49;
  --remedy-blue-900: #122f6a;
  --remedy-blue-800: #173f8f;
  --remedy-blue-700: #2459d6;
  --remedy-blue-500: #4c83ff;
  --remedy-blue-300: #8fb3ff;
  --remedy-blue-100: #dce8ff;
  --remedy-cyan-400: #53d6df;
  --remedy-green-500: #4cc681;
  --remedy-purple-400: #a28cff;
  --remedy-orange-400: #f5a34e;
  --remedy-line: rgba(44, 82, 150, 0.16);
  --remedy-line-strong: rgba(44, 82, 150, 0.28);
  --remedy-card: rgba(255, 255, 255, 0.68);
  --remedy-card-strong: rgba(255, 255, 255, 0.86);
  --remedy-card-soft: rgba(255, 255, 255, 0.48);
  --remedy-text: #14254b;
  --remedy-muted: #6e7fa3;
  --remedy-faint: #9aa9c5;
  --remedy-radius-xl: 28px;
  --remedy-radius-lg: 22px;
  --remedy-radius-md: 16px;
  --remedy-shadow: 0 24px 70px rgba(55, 86, 138, 0.16);
  --remedy-shadow-soft: 0 14px 36px rgba(55, 86, 138, 0.12);
  --remedy-glow: 0 0 44px rgba(76, 131, 255, 0.38);
  --remedy-glow-strong: 0 0 90px rgba(76, 131, 255, 0.56);
  --remedy-left-width: 292px;
  --remedy-right-width: 404px;
  color-scheme: light;
}
```

---

## 4. styles/globals.css

```css
@import "./tokens.css";
@import "@xyflow/react/dist/style.css";

* { box-sizing: border-box; }
html, body, #root { width: 100%; height: 100%; margin: 0; }
body {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--remedy-text);
  background:
    radial-gradient(circle at 46% 34%, rgba(255,255,255,.9), transparent 24%),
    radial-gradient(circle at 58% 44%, rgba(124,170,255,.18), transparent 35%),
    linear-gradient(135deg, #f8fbff 0%, #edf3fb 45%, #e6eef8 100%);
  overflow: hidden;
}
button, input { font: inherit; }
button { cursor: pointer; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: .001ms !important; animation-duration: .001ms !important; animation-iteration-count: 1 !important; }
}
```

---

## 5. api/types.ts

```ts
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
export interface RemedyDashboard { jobId: string; title: string; description: string; conceptLabel: string; metrics: RemedyMetric[]; phases: RemedyPhase[]; tasks: RemedyTaskItem[]; activity: RemedyActivityItem[]; graph: { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[]; }; nextAction: RemedyNextAction; live: RemedyLiveState; }
```

---

## 6. copy/humanCopy.ts

```ts
const conceptLabels: Record<string, string> = {
  patch_intent: "Proposed change", patch_apply: "Applied change", patch_apply_proof: "Apply proof",
  test_run: "Test result", review_recommendation: "Review suggestion", memory_candidate: "Learning suggestion",
  decision_queue: "Needs decision", approval_decision: "Approval", artifact: "Generated work",
  task: "Task", job: "Project goal", proof: "Proof", change: "Changed file"
};
const diagnosticsOnly: Record<string, string> = { context_coverage: "Context check", token_policy: "Token budget", worker_adapter: "Worker", run_event: "Run event", event_ledger: "Event ledger" };
const forbidden = ["rank", "importance", "node_type", "metadata", "present signals", "missing signals", "context coverage", "zone", "edge_type", "connected_to", "raw_stdout", "raw_stderr", "command_output", "diff_preview", "approval_reason", "traceback"];

export function humanLabel(type: string, fallback = "Work item"): string {
  const normalized = String(type || "").toLowerCase();
  return conceptLabels[normalized] ?? diagnosticsOnly[normalized] ?? fallback;
}
export function isDiagnosticsOnly(type: string): boolean {
  return Object.prototype.hasOwnProperty.call(diagnosticsOnly, String(type || "").toLowerCase());
}
export function scrubUiText(value: unknown, fallback = "Work item"): string {
  const input = String(value ?? "").replace(/\s+/g, " ").trim();
  if (!input) return fallback;
  const lower = input.toLowerCase();
  if (forbidden.some((word) => lower.includes(word))) return fallback;
  if (/^[0-9a-f]{6,}(-[0-9a-f]+)*$/i.test(input)) return fallback;
  return input.length > 92 ? `${input.slice(0, 89)}…` : input;
}
export function stateLabel(state: string): string {
  if (state === "done") return "Done";
  if (state === "current") return "In Progress";
  if (state === "blocked") return "Blocked";
  if (state === "suggested") return "Suggested";
  return "Planned";
}
```

---

## 7. api/remedyApi.ts

```ts
import { humanLabel, isDiagnosticsOnly, scrubUiText } from "../copy/humanCopy";
import type { RemedyActivityItem, RemedyDashboard, RemedyGraphEdge, RemedyGraphNode, RemedyJourneyItem, RemedyMetric, RemedyNextAction, RemedyPhase, RemedyState, RemedyTaskItem } from "./types";

interface ApiClientOptions { jobId: string; token: string; baseUrl?: string; }
async function fetchJson<T>(path: string): Promise<T> { const r = await fetch(path, { method: "GET", credentials: "same-origin" }); if (!r.ok) throw new Error(`Request failed ${r.status}: ${path}`); return r.json() as Promise<T>; }
function normalizeState(value: unknown): RemedyState { const text = String(value || "").toLowerCase(); if (text.includes("done") || text.includes("pass") || text.includes("complete") || text.includes("applied")) return "done"; if (text.includes("block") || text.includes("fail")) return "blocked"; if (text.includes("current") || text.includes("active") || text.includes("running") || text.includes("progress")) return "current"; if (text.includes("suggest")) return "suggested"; return "pending"; }
function nextAction(label = "Review project state", command = "remedy dev status"): RemedyNextAction { return { label, command, risk: "low", requiresHuman: true }; }
function buildMetrics(tasks: RemedyTaskItem[]): RemedyMetric[] { const done = tasks.filter(t => t.state === "done").length; const open = tasks.filter(t => t.state === "current" || t.state === "blocked").length; const planned = tasks.filter(t => t.state === "pending" || t.state === "suggested").length; const progress = Math.round((done / Math.max(tasks.length, 1)) * 100); return [{ key: "open", label: "Open", value: open }, { key: "planned", label: "Planned", value: planned }, { key: "done", label: "Done", value: done }, { key: "progress", label: "Progress", value: progress, suffix: "%" }]; }
function buildPhases(tasks: RemedyTaskItem[]): RemedyPhase[] { const hasTests = tasks.some(t => t.kind === "test"); const hasReview = tasks.some(t => t.kind === "review" || t.state === "suggested"); const doneCount = tasks.filter(t => t.state === "done").length; const currentId = hasReview ? "review" : hasTests ? "test" : doneCount > 0 ? "build" : "planning"; return [{ id: "job", label: "Job", state: "done", icon: "briefcase" }, { id: "planning", label: "Planning", state: doneCount > 0 ? "done" : "current", icon: "calendar" }, { id: "build", label: "Build", state: currentId === "build" ? "current" : doneCount > 0 ? "done" : "pending", icon: "code" }, { id: "test", label: "Test", state: currentId === "test" ? "current" : hasTests ? "done" : "pending", icon: "check" }, { id: "review", label: "Review", state: currentId === "review" ? "current" : hasReview ? "done" : "pending", icon: "person" }, { id: "finalized", label: "Finalized", state: tasks.length > 0 && tasks.every(t => t.state === "done") ? "done" : "pending", icon: "flag" }]; }
function normalizeJourney(story: any, brain: any): RemedyJourneyItem[] { const src = story?.journey || []; if (Array.isArray(src) && src.length) return src.map((i: any, idx: number) => ({ id: String(i.id || `journey-${idx}`), kind: i.kind || "task", title: scrubUiText(i.title, humanLabel(i.kind || "task")), subtitle: scrubUiText(i.subtitle, ""), state: normalizeState(i.state), nodeId: String(i.node_id || i.nodeId || i.id || `journey-${idx}`), visibleFromZoom: Number(i.visible_from_zoom ?? i.visibleFromZoom ?? Math.min(idx, 3)) })); const nodes = Array.isArray(brain?.nodes) ? brain.nodes : []; const visible = nodes.filter((n: any) => !isDiagnosticsOnly(n.type || n.node_type)); const root = visible.find((n: any) => n.is_origin) || visible[0]; const journey: RemedyJourneyItem[] = []; if (root) journey.push({ id: "goal", kind: "goal", title: scrubUiText(root.title || root.label || brain?.job_title, "Project goal"), subtitle: "The main objective Remedy is working through.", state: "current", nodeId: String(root.id), visibleFromZoom: 0 }); visible.slice(0, 8).forEach((n: any, idx: number) => journey.push({ id: String(n.id || `node-${idx}`), kind: n.type === "test_run" ? "test" : n.type === "patch_apply" ? "apply" : n.type === "patch_intent" ? "change" : "task", title: scrubUiText(n.title || n.label || humanLabel(n.type || "task"), humanLabel(n.type || "task")), subtitle: scrubUiText(n.subtitle || n.summary || "", ""), state: normalizeState(n.status || n.state), nodeId: String(n.id || `node-${idx}`), visibleFromZoom: Math.min(idx + 1, 3) })); return journey; }
function normalizeTasks(progress: any, journey: RemedyJourneyItem[]): RemedyTaskItem[] { const src = progress?.items || progress?.checklist || progress?.tasks || []; const tasks = src.map((i: any, idx: number) => { const kind = (i.kind || i.type || "task") as RemedyTaskItem["kind"]; const state = normalizeState(i.state || i.status || (i.checked ? "done" : "pending")); return { id: scrubUiText(i.id || `task-${idx}`, `task-${idx}`), label: scrubUiText(i.label || i.title || i.short_reason || humanLabel(kind), humanLabel(kind)), state, kind, checked: Boolean(i.checked ?? i.verified ?? state === "done"), muted: Boolean(i.muted ?? state === "pending" || state === "suggested"), nodeId: String(i.node_id || i.related_node_id || i.nodeId || i.id || `task-${idx}`), nextAction: i.next_action ? { label: scrubUiText(i.next_action.label, "Review next action"), command: scrubUiText(i.next_action.command, "remedy dev status"), risk: i.next_action.risk || "low", requiresHuman: Boolean(i.next_action.requires_human ?? true) } : undefined }; }); if (tasks.length) return tasks; return journey.map(i => ({ id: i.id, label: i.title, state: i.state, kind: i.kind, checked: i.state === "done", muted: i.state === "pending" || i.state === "suggested", nodeId: i.nodeId, nextAction: nextAction() })); }
function normalizeGraph(journey: RemedyJourneyItem[], tasks: RemedyTaskItem[]): { nodes: RemedyGraphNode[]; edges: RemedyGraphEdge[] } { const nodes: RemedyGraphNode[] = []; journey.forEach((i, idx) => nodes.push({ id: i.nodeId, label: i.title, kind: idx === 0 ? "root" : i.kind, state: i.state, nodeId: i.nodeId, group: i.state === "done" ? "done" : i.state === "current" ? "open" : i.state === "suggested" ? "review" : "planned", visibleFromZoom: i.visibleFromZoom, showLabelFromZoom: idx <= 1 ? 0 : 2 })); tasks.slice(0, 80).forEach((t, idx) => { if (nodes.some(n => n.id === t.nodeId)) return; nodes.push({ id: t.nodeId, label: t.label, kind: t.kind, state: t.state, nodeId: t.nodeId, group: t.state === "done" ? "done" : t.state === "current" ? "open" : t.state === "suggested" ? "review" : "planned", visibleFromZoom: Math.min(2 + Math.floor(idx / 8), 4), showLabelFromZoom: idx < 8 ? 2 : 4 }); }); const edges: RemedyGraphEdge[] = []; for (let i = 0; i < journey.length - 1; i++) edges.push({ id: `edge-${journey[i].nodeId}-${journey[i + 1].nodeId}`, source: journey[i].nodeId, target: journey[i + 1].nodeId, meaning: "leads to", state: journey[i + 1].state }); return { nodes, edges }; }
function normalizeActivity(live: any, tasks: RemedyTaskItem[]): RemedyActivityItem[] { const active = tasks.find(t => t.state === "current"); return [{ id: "now", actor: "Builder", message: scrubUiText(live?.latestMessage || live?.latest_message || (active ? `Working on ${active.label}` : "Waiting for the next safe action."), "Project state updated."), timeLabel: "Just now", kind: "build" }, { id: "system", actor: "System", message: "Project state is ready for review.", timeLabel: "Now", kind: "system" }]; }
export async function loadRemedyDashboard(o: ApiClientOptions): Promise<RemedyDashboard> { const base = o.baseUrl || ""; const q = `token=${encodeURIComponent(o.token)}`; const [brain, progress, live, story] = await Promise.allSettled([fetchJson<any>(`${base}/api/jobs/${o.jobId}/brain-view-model?${q}`), fetchJson<any>(`${base}/api/jobs/${o.jobId}/task-progress?${q}`), fetchJson<any>(`${base}/api/jobs/${o.jobId}/live-state?${q}`), fetchJson<any>(`${base}/api/jobs/${o.jobId}/story?${q}`)]); const brainData = brain.status === "fulfilled" ? brain.value : {}; const progressData = progress.status === "fulfilled" ? progress.value : {}; const liveData = live.status === "fulfilled" ? live.value : {}; const storyData = story.status === "fulfilled" ? story.value : brainData?.story || {}; const journey = normalizeJourney(storyData, brainData); const tasks = normalizeTasks(progressData, journey); const graph = normalizeGraph(journey, tasks); return { jobId: o.jobId, title: scrubUiText(storyData?.headline || brainData?.title || brainData?.job_title, "Growing Brain Overview"), description: scrubUiText(storyData?.description || brainData?.description || "An AI agent working through a verified project plan.", "An AI agent working through a verified project plan."), conceptLabel: "Concept 01 of 10", metrics: buildMetrics(tasks), phases: buildPhases(tasks), tasks, activity: normalizeActivity(liveData, tasks), graph, nextAction: storyData?.primary_next_action ? { label: scrubUiText(storyData.primary_next_action.label, "Review project state"), command: scrubUiText(storyData.primary_next_action.command, "remedy dev status"), risk: storyData.primary_next_action.risk || "low", requiresHuman: Boolean(storyData.primary_next_action.requires_human ?? true) } : nextAction(), live: { running: Boolean(liveData?.running ?? true), stage: scrubUiText(liveData?.stage, "live"), activeTaskLabel: tasks.find(t => t.state === "current")?.label || "Waiting for next safe action", latestMessage: scrubUiText(liveData?.latest_message || liveData?.latestMessage, "Project state updated."), latestActor: "Builder" } }; }
```

---

## 8. main.tsx

```tsx
import React from "react";
import { createRoot } from "react-dom/client";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import RemedyApp from "./RemedyApp";
import "./styles/globals.css";

const theme = createTheme({
  palette: { mode: "light", primary: { main: "#4c83ff" }, text: { primary: "#14254b", secondary: "#6e7fa3" }, background: { default: "#edf3fb" } },
  shape: { borderRadius: 18 },
  typography: { fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' }
});

createRoot(document.getElementById("root")!).render(
  <React.StrictMode><ThemeProvider theme={theme}><RemedyApp /></ThemeProvider></React.StrictMode>
);
```

---

## 9. RemedyApp.tsx

```tsx
import { useEffect, useMemo, useState } from "react";
import { CircularProgress } from "@mui/material";
import { loadRemedyDashboard } from "./api/remedyApi";
import type { RemedyDashboard } from "./api/types";
import { RemedyShell } from "./components/shell/RemedyShell";
import { ReducedMotionProvider } from "./components/shell/ReducedMotionProvider";

function readUrlState() { const p = new URLSearchParams(window.location.search); return { jobId: p.get("job") || p.get("job_id") || "", token: p.get("token") || "" }; }
export default function RemedyApp() {
  const { jobId, token } = useMemo(readUrlState, []);
  const [dashboard, setDashboard] = useState<RemedyDashboard | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  useEffect(() => { let cancelled = false; async function load() { if (!jobId || !token) { setError("Missing job or token in the URL."); return; } try { const data = await loadRemedyDashboard({ jobId, token }); if (!cancelled) { setDashboard(data); setSelectedNodeId(data.graph.nodes[0]?.nodeId ?? null); } } catch (e) { if (!cancelled) setError(e instanceof Error ? e.message : "Could not load Remedy UI."); } } load(); const timer = window.setInterval(load, 5000); return () => { cancelled = true; window.clearInterval(timer); }; }, [jobId, token]);
  if (error) return <div style={{ display: "grid", placeItems: "center", height: "100%", color: "#14254b" }}>{error}</div>;
  if (!dashboard) return <div style={{ display: "grid", placeItems: "center", height: "100%" }}><CircularProgress /></div>;
  return <ReducedMotionProvider><RemedyShell dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={setSelectedNodeId} /></ReducedMotionProvider>;
}
```

---

## 10. shell/ReducedMotionProvider.tsx

```tsx
import { createContext, useContext, useEffect, useState } from "react";
const ReducedMotionContext = createContext(false);
export function ReducedMotionProvider({ children }: { children: React.ReactNode }) { const [reduced, setReduced] = useState(false); useEffect(() => { const media = window.matchMedia("(prefers-reduced-motion: reduce)"); const update = () => setReduced(media.matches); update(); media.addEventListener("change", update); return () => media.removeEventListener("change", update); }, []); return <ReducedMotionContext.Provider value={reduced}>{children}</ReducedMotionContext.Provider>; }
export function useReducedMotion() { return useContext(ReducedMotionContext); }
```

---

## 11. shell/RemedyShell.tsx

```tsx
import type { RemedyDashboard } from "../../api/types";
import { LeftBrandRail } from "../rail/LeftBrandRail";
import { TopMetricsBar } from "../metrics/TopMetricsBar";
import { CommandBar } from "../command/CommandBar";
import { BrainGraphStage } from "../graph/BrainGraphStage";
import { RightLivePanel } from "../panels/RightLivePanel";
import { PhaseTimeline } from "../timeline/PhaseTimeline";
import { DetailPopover } from "../detail/DetailPopover";
import { LayerSwitcher } from "../layers/LayerSwitcher";
import styles from "./RemedyShell.module.css";

export function RemedyShell({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string) => void }) {
  const selectedNode = dashboard.graph.nodes.find(n => n.nodeId === selectedNodeId || n.id === selectedNodeId) ?? dashboard.graph.nodes[0];
  return <div className={`${styles.shell} remedy-journey-shell`}><div className={styles.backgroundAura} aria-hidden="true" /><LeftBrandRail dashboard={dashboard} /><main className={styles.mainStage}><TopMetricsBar metrics={dashboard.metrics} /><CommandBar nextAction={dashboard.nextAction} /><BrainGraphStage dashboard={dashboard} selectedNodeId={selectedNode?.id ?? null} onSelectNode={onSelectNode} /><PhaseTimeline phases={dashboard.phases} /></main><RightLivePanel dashboard={dashboard} onSelectNode={onSelectNode} /><LayerSwitcher /><DetailPopover dashboard={dashboard} selectedNode={selectedNode} /></div>;
}
```

---

## 12. shell/RemedyShell.module.css

```css
.shell { width: 100vw; height: 100vh; position: relative; display: grid; grid-template-columns: var(--remedy-left-width) minmax(680px, 1fr) var(--remedy-right-width); gap: 26px; padding: 24px 26px; background: radial-gradient(circle at 52% 48%, rgba(255,255,255,.78), transparent 28%), radial-gradient(circle at 44% 58%, rgba(76,131,255,.12), transparent 38%), linear-gradient(135deg, #f8fbff 0%, #edf3fb 48%, #e5edf7 100%); overflow: hidden; }
.backgroundAura { position: absolute; inset: -20%; pointer-events: none; background: radial-gradient(circle at 50% 52%, rgba(111,156,255,.16), transparent 18%), radial-gradient(circle at 62% 32%, rgba(83,214,223,.08), transparent 20%); filter: blur(20px); }
.mainStage { position: relative; z-index: 1; display: grid; grid-template-rows: 102px 64px 1fr 154px; min-width: 0; gap: 18px; }
@media (max-width: 1180px) { .shell { grid-template-columns: 84px minmax(0, 1fr); } }
@media (max-width: 900px) { .shell { grid-template-columns: 1fr; padding: 16px; } .mainStage { grid-template-rows: auto auto 1fr auto; } }
```

---

## 13. icons/NetworkLogoIcon.tsx

```tsx
export function NetworkLogoIcon({ className }: { className?: string }) { const dots = [[16,10],[32,10],[10,24],[24,24],[38,24],[16,38],[32,38]]; return <svg className={className} viewBox="0 0 48 48" role="img" aria-label="Remedy network logo"><g fill="none" stroke="rgba(76,131,255,0.72)" strokeWidth="2"><path d="M16 10 L24 24 L32 10" /><path d="M10 24 L24 24 L38 24" /><path d="M16 38 L24 24 L32 38" /></g>{dots.map(([cx,cy], i) => <circle key={i} cx={cx} cy={cy} r="4.2" fill="#4c83ff" opacity={i === 3 ? 1 : .76} />)}</svg>; }
```

## 14. icons/CodeOrbIcon.tsx

```tsx
export function CodeOrbIcon({ className }: { className?: string }) { return <svg className={className} viewBox="0 0 72 72" role="img" aria-label="Code node"><defs><radialGradient id="codeOrbGradient" cx="50%" cy="50%" r="50%"><stop offset="0%" stopColor="#fff" /><stop offset="55%" stopColor="#6da0ff" /><stop offset="100%" stopColor="#2459d6" /></radialGradient></defs><circle cx="36" cy="36" r="31" fill="url(#codeOrbGradient)" /><circle cx="36" cy="36" r="31" fill="none" stroke="rgba(255,255,255,.8)" strokeWidth="2" /><path d="M29 27 L20 36 L29 45 M43 27 L52 36 L43 45 M39 24 L33 48" fill="none" stroke="white" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" /></svg>; }
```

---

## 15. rail/RemedyLogo.tsx + module.css

```tsx
import { NetworkLogoIcon } from "../icons/NetworkLogoIcon";
import styles from "./RemedyLogo.module.css";
export function RemedyLogo() { return <div className={styles.logo}><NetworkLogoIcon className={styles.mark} /><span className={styles.word}>REMEDY</span></div>; }
```

```css
.logo { display: flex; align-items: center; gap: 14px; }
.mark { width: 42px; height: 42px; filter: drop-shadow(0 8px 18px rgba(76,131,255,.22)); }
.word { color: var(--remedy-blue-900); font-weight: 700; font-size: 25px; letter-spacing: .42em; }
```

---

## 16. rail/LeftBrandRail.tsx + module.css

```tsx
import type { RemedyDashboard } from "../../api/types";
import { RemedyLogo } from "./RemedyLogo";
import { SideIconDock } from "./SideIconDock";
import styles from "./LeftBrandRail.module.css";
export function LeftBrandRail({ dashboard }: { dashboard: RemedyDashboard }) { return <aside className={styles.rail}><RemedyLogo /><section className={styles.intro}><div className={styles.concept}>{dashboard.conceptLabel}</div><h1>{dashboard.title}</h1><p>{dashboard.description}</p></section><SideIconDock /></aside>; }
```

```css
.rail { position: relative; z-index: 2; display: flex; flex-direction: column; gap: 56px; color: var(--remedy-blue-900); min-width: 0; }
.intro { max-width: 238px; }
.concept { color: var(--remedy-blue-700); opacity: .72; text-transform: uppercase; font-size: 14px; letter-spacing: .08em; margin-bottom: 16px; }
.intro h1 { margin: 0; color: var(--remedy-blue-900); font-size: 30px; line-height: 1.16; font-weight: 700; letter-spacing: -.04em; }
.intro p { color: var(--remedy-blue-900); margin: 24px 0 0; font-size: 16px; line-height: 1.58; max-width: 218px; }
@media (max-width: 1180px) { .intro { display: none; } }
```

---

## 17. rail/SideIconDock.tsx + module.css

```tsx
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import FolderOutlinedIcon from "@mui/icons-material/FolderOutlined";
import HistoryIcon from "@mui/icons-material/History";
import MenuBookOutlinedIcon from "@mui/icons-material/MenuBookOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import ShowChartIcon from "@mui/icons-material/ShowChart";
import styles from "./SideIconDock.module.css";
const items = [["Overview", AutoAwesomeIcon], ["Checks", CheckCircleOutlineIcon], ["Activity", ShowChartIcon], ["Files", FolderOutlinedIcon], ["History", HistoryIcon], ["Docs", MenuBookOutlinedIcon], ["Settings", SettingsOutlinedIcon]] as const;
export function SideIconDock() { return <nav className={styles.dock} aria-label="Remedy sections">{items.map(([label, Icon], i) => <button key={label} className={i === 0 ? styles.active : styles.button} aria-label={label}><Icon fontSize="small" /></button>)}</nav>; }
```

```css
.dock { width: 68px; padding: 18px 0; display: flex; flex-direction: column; gap: 16px; align-items: center; border-radius: 26px; background: rgba(255,255,255,.58); border: 1px solid rgba(91,126,188,.16); box-shadow: var(--remedy-shadow-soft); backdrop-filter: blur(18px); }
.button, .active { width: 42px; height: 42px; display: grid; place-items: center; border: 0; background: transparent; color: var(--remedy-blue-700); border-radius: 50%; transition: 160ms ease; }
.active { background: rgba(255,255,255,.9); box-shadow: inset 0 0 0 1px rgba(76,131,255,.2), 0 10px 24px rgba(76,131,255,.18); }
.button:hover { background: rgba(255,255,255,.56); }
```

---

## 18. metrics/TopMetricsBar.tsx + module.css

```tsx
import AssignmentOutlinedIcon from "@mui/icons-material/AssignmentOutlined";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";
import CheckCircleOutlineIcon from "@mui/icons-material/CheckCircleOutline";
import TimelineIcon from "@mui/icons-material/Timeline";
import type { RemedyMetric } from "../../api/types";
import styles from "./TopMetricsBar.module.css";
const iconByKey = { open: AssignmentOutlinedIcon, planned: CalendarMonthOutlinedIcon, done: CheckCircleOutlineIcon, progress: TimelineIcon };
export function TopMetricsBar({ metrics }: { metrics: RemedyMetric[] }) { return <section className={`${styles.bar} remedy-glass-card`} aria-label="Project metrics">{metrics.map(m => { const Icon = iconByKey[m.key]; return <article key={m.key} className={styles.metric}><div className={styles.iconBox}><Icon fontSize="small" /></div><div><div className={styles.label}>{m.label}</div><div className={styles.value}>{m.value}{m.suffix}</div>{m.key === "progress" && <div className={styles.progressTrack}><span style={{ width: `${Math.max(0, Math.min(m.value, 100))}%` }} /></div>}</div></article>; })}</section>; }
```

```css
.bar { height: 100%; display: grid; grid-template-columns: repeat(4, 1fr); align-items: center; border-radius: var(--remedy-radius-xl); background: rgba(255,255,255,.42); border: 1px solid rgba(78,111,172,.14); box-shadow: 0 20px 58px rgba(65,91,142,.1); backdrop-filter: blur(20px); overflow: hidden; }
.metric { min-width: 0; display: flex; align-items: center; gap: 18px; height: 58px; padding: 0 34px; border-right: 1px solid rgba(39,77,143,.12); }
.metric:last-child { border-right: 0; }
.iconBox { width: 42px; height: 42px; display: grid; place-items: center; color: var(--remedy-blue-700); border-radius: 12px; background: rgba(255,255,255,.68); box-shadow: inset 0 0 0 1px rgba(76,131,255,.22); }
.label { color: var(--remedy-blue-900); font-size: 13px; font-weight: 800; letter-spacing: .05em; text-transform: uppercase; }
.value { margin-top: 6px; font-size: 30px; line-height: 1; font-weight: 700; color: var(--remedy-blue-950); letter-spacing: -.04em; }
.progressTrack { margin-top: 10px; width: 108px; height: 4px; border-radius: 999px; background: rgba(76,131,255,.18); overflow: hidden; }
.progressTrack span { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, #3478ff, #8fb3ff); }
```

---

## 19. command/CommandBar.tsx + module.css

```tsx
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import type { RemedyNextAction } from "../../api/types";
import styles from "./CommandBar.module.css";
export function CommandBar({ nextAction }: { nextAction: RemedyNextAction }) { return <section className={styles.commandBar} aria-label="Command search"><div className={styles.spark}><AutoAwesomeIcon fontSize="small" /></div><input readOnly aria-label="Ask Remedy" value="" placeholder={`Ask your agent or jump to anything (e.g., &quot;${nextAction.label}&quot;)`} /><button type="button" aria-label="Copy suggested command" title={`Copy command: ${nextAction.command}`} onClick={() => navigator.clipboard?.writeText(nextAction.command)}><ArrowBackIcon /></button></section>; }
```

```css
.commandBar { display: grid; grid-template-columns: 44px 1fr 54px; align-items: center; height: 64px; border-radius: 24px; padding: 0 12px 0 20px; background: rgba(255,255,255,.48); border: 1px solid rgba(78,111,172,.14); box-shadow: 0 20px 52px rgba(65,91,142,.08); backdrop-filter: blur(20px); }
.spark { color: var(--remedy-blue-500); display: grid; place-items: center; }
.commandBar input { border: 0; outline: 0; background: transparent; color: var(--remedy-blue-900); font-size: 16px; }
.commandBar input::placeholder { color: rgba(18,47,106,.58); }
.commandBar button { width: 42px; height: 42px; border-radius: 50%; border: 1px solid rgba(36,89,214,.22); color: var(--remedy-blue-700); background: rgba(255,255,255,.72); }
```

---

## 20. graph/semanticZoom.ts

```ts
export function semanticZoomLevelFromViewportZoom(zoom: number): number {
  if (zoom < 0.36) return 0;
  if (zoom < 0.62) return 1;
  if (zoom < 0.92) return 2;
  if (zoom < 1.28) return 3;
  return 4;
}
```

---

## 21. graph/organicLayout.ts

```ts
import type { Edge, Node } from "@xyflow/react";
import type { RemedyDashboard, RemedyGraphNode } from "../../api/types";
function hash(input: string): number { let v = 2166136261; for (let i = 0; i < input.length; i++) { v ^= input.charCodeAt(i); v += (v << 1) + (v << 4) + (v << 7) + (v << 8) + (v << 24); } return Math.abs(v >>> 0); }
function seededOffset(id: string, scale: number): number { return ((hash(id) % 1000) / 1000 - .5) * scale; }
function stateToBranch(node: RemedyGraphNode, index: number): number { if (node.state === "done") return .34; if (node.state === "current") return -.1; if (node.state === "suggested") return .68; return index % 2 === 0 ? -.52 : .52; }
export function buildReactFlowGraph(dashboard: RemedyDashboard): { nodes: Node[]; edges: Edge[] } { const meaningful = dashboard.graph.nodes.slice(0, 120); const root = meaningful[0]; const nodes: Node[] = meaningful.map((node, i) => { if (i === 0) return { id: node.id, type: "root", position: { x: 0, y: 0 }, data: { ...node, zoomLabel: true }, draggable: false }; const branch = stateToBranch(node, i); const radius = 160 + Math.floor(i / 8) * 74 + seededOffset(node.id, 40); const angle = branch * Math.PI + seededOffset(node.id + "angle", .42); const x = Math.cos(angle) * radius + seededOffset(node.id + "x", 90); const y = Math.sin(angle) * radius * .62 + seededOffset(node.id + "y", 120); return { id: node.id, type: i < 22 ? "work" : "tiny", position: { x, y }, data: { ...node, index: i }, draggable: false }; }); const edges: Edge[] = []; dashboard.graph.edges.forEach(e => { if (nodes.some(n => n.id === e.source) && nodes.some(n => n.id === e.target)) edges.push({ id: e.id, source: e.source, target: e.target, type: "soft", data: { meaning: e.meaning, state: e.state } }); }); if (root?.id) nodes.slice(1, 80).forEach((n, i) => { if (edges.some(e => e.target === n.id)) return; const anchor = i < 12 ? root.id : nodes[Math.max(1, Math.floor(i / 2))]?.id || root.id; edges.push({ id: `organic-${anchor}-${n.id}`, source: anchor, target: n.id, type: "soft", data: { meaning: "branches to", state: n.data.state } }); }); return { nodes, edges }; }
```

---

## 22. graph/GraphNodes.tsx + module.css

```tsx
import type { NodeProps } from "@xyflow/react";
import CheckIcon from "@mui/icons-material/Check";
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked";
import { CodeOrbIcon } from "../icons/CodeOrbIcon";
import styles from "./GraphNodes.module.css";
function stateClass(state: string | undefined) { if (state === "done") return styles.done; if (state === "current") return styles.current; if (state === "suggested") return styles.suggested; if (state === "blocked") return styles.blocked; return styles.pending; }
export function RootNode({ selected }: NodeProps) { return <div className={`${styles.rootNode} ${selected ? styles.selected : ""}`}><CodeOrbIcon className={styles.codeOrb} /><div className={styles.rootPulse} aria-hidden="true" /></div>; }
export function WorkNode({ data, selected }: NodeProps) { const state = String(data.state || "pending"); return <div className={`${styles.workNode} ${stateClass(state)} ${selected ? styles.selected : ""}`}><span className={styles.statusIcon}>{state === "done" ? <CheckIcon fontSize="inherit" /> : <RadioButtonUncheckedIcon fontSize="inherit" />}</span><span className={styles.workLabel}>{String(data.label || "Work item")}</span></div>; }
export function TinyNode({ data, selected }: NodeProps) { return <div className={`${styles.tinyNode} ${stateClass(String(data.state || "pending"))} ${selected ? styles.selected : ""}`} title={String(data.label || "")} />; }
```

```css
.rootNode { position: relative; width: 86px; height: 86px; transform: translate(-43px, -43px); }
.codeOrb { position: relative; z-index: 2; width: 86px; height: 86px; filter: drop-shadow(0 0 32px rgba(76,131,255,.66)) drop-shadow(0 16px 34px rgba(36,89,214,.18)); }
.rootPulse { position: absolute; inset: -30px; border-radius: 50%; background: radial-gradient(circle, rgba(76,131,255,.28), transparent 68%); animation: remedyPulse 3.8s ease-in-out infinite; }
.workNode { min-width: 152px; max-width: 206px; min-height: 34px; display: flex; align-items: center; gap: 8px; padding: 7px 12px; border-radius: 999px; background: rgba(255,255,255,.76); border: 1px solid rgba(76,131,255,.2); color: var(--remedy-blue-900); box-shadow: 0 10px 26px rgba(65,91,142,.12); backdrop-filter: blur(12px); }
.workLabel { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 12px; font-weight: 700; }
.statusIcon { flex: 0 0 auto; width: 15px; height: 15px; display: grid; place-items: center; font-size: 13px; }
.tinyNode { width: 18px; height: 18px; border-radius: 50%; transform: translate(-9px, -9px); background: rgba(255,255,255,.9); border: 2px solid rgba(76,131,255,.48); box-shadow: 0 0 0 5px rgba(76,131,255,.08), 0 0 24px rgba(76,131,255,.2); }
.done { border-color: rgba(76,198,129,.58); }
.current { border-color: rgba(76,131,255,.95); box-shadow: 0 0 0 6px rgba(76,131,255,.12), 0 0 42px rgba(76,131,255,.3); }
.suggested { border-color: rgba(162,140,255,.58); }
.blocked { border-color: rgba(245,163,78,.68); }
.pending { border-color: rgba(143,179,255,.5); }
.selected { outline: 3px solid rgba(76,131,255,.26); outline-offset: 5px; }
@keyframes remedyPulse { 0%,100% { opacity: .45; transform: scale(.92); } 50% { opacity: .78; transform: scale(1.08); } }
```

---

## 23. graph/SoftGlowEdge.tsx

```tsx
import { BaseEdge, getBezierPath, type EdgeProps } from "@xyflow/react";
export function SoftGlowEdge(props: EdgeProps) { const [path] = getBezierPath(props); const state = String(props.data?.state || "pending"); const stroke = state === "done" ? "rgba(76,198,129,.34)" : state === "current" ? "rgba(76,131,255,.48)" : state === "suggested" ? "rgba(162,140,255,.28)" : "rgba(99,126,178,.18)"; return <><BaseEdge path={path} style={{ stroke: "rgba(76,131,255,.10)", strokeWidth: 8 }} /><BaseEdge path={path} style={{ stroke, strokeWidth: state === "current" ? 2.2 : 1.4 }} /></>; }
```

---

## 24. graph/RemedyBrainFlow.tsx + module.css

```tsx
import { useMemo } from "react";
import ReactFlow, { Background, type EdgeTypes, type NodeTypes, useEdgesState, useNodesState } from "@xyflow/react";
import type { RemedyDashboard } from "../../api/types";
import { useReducedMotion } from "../shell/ReducedMotionProvider";
import { buildReactFlowGraph } from "./organicLayout";
import { RootNode, TinyNode, WorkNode } from "./GraphNodes";
import { SoftGlowEdge } from "./SoftGlowEdge";
import styles from "./RemedyBrainFlow.module.css";
const nodeTypes: NodeTypes = { root: RootNode, work: WorkNode, tiny: TinyNode };
const edgeTypes: EdgeTypes = { soft: SoftGlowEdge };
export function RemedyBrainFlow({ dashboard, onSelectNode, filter }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string) => void; filter: "all" | "open" | "planned" | "done" }) { const reducedMotion = useReducedMotion(); const graph = useMemo(() => { const built = buildReactFlowGraph(dashboard); if (filter === "all") return built; const allowed = new Set(built.nodes.filter(n => { const s = n.data?.state; if (filter === "done") return s === "done"; if (filter === "open") return s === "current" || s === "blocked"; if (filter === "planned") return s === "pending" || s === "suggested"; return true; }).map(n => n.id)); const root = built.nodes[0]; if (root) allowed.add(root.id); return { nodes: built.nodes.filter(n => allowed.has(n.id)), edges: built.edges.filter(e => allowed.has(e.source) && allowed.has(e.target)) }; }, [dashboard, filter]); const [nodes, , onNodesChange] = useNodesState(graph.nodes); const [edges, , onEdgesChange] = useEdgesState(graph.edges); return <div className={`${styles.flowWrap} remedy-brain-canvas`}>{!reducedMotion && <div className={styles.particleVeil} aria-hidden="true" />}<ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes} fitView minZoom={.25} maxZoom={2.4} nodesDraggable={false} nodesConnectable={false} elementsSelectable panOnDrag zoomOnScroll proOptions={{ hideAttribution: true }} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onNodeClick={(_, node) => onSelectNode(String(node.data?.nodeId || node.id))} className={styles.reactFlow}><Background color="rgba(95,132,190,.12)" gap={32} size={1} /></ReactFlow><div className={styles.softCenterGlow} aria-hidden="true" /></div>; }
```

```css
.flowWrap { position: absolute; inset: 0; overflow: hidden; border-radius: 28px; }
.reactFlow { background: transparent; }
.reactFlow :global(.react-flow__node) { font-family: inherit; }
.reactFlow :global(.react-flow__handle) { display: none; }
.softCenterGlow { position: absolute; left: 50%; top: 52%; width: 640px; height: 360px; transform: translate(-50%, -50%); border-radius: 50%; pointer-events: none; background: radial-gradient(circle, rgba(255,255,255,.84), rgba(111,156,255,.14) 35%, transparent 70%); mix-blend-mode: screen; opacity: .72; }
.particleVeil { position: absolute; inset: 0; pointer-events: none; background-image: radial-gradient(circle, rgba(255,255,255,.86) 0 1px, transparent 1.8px), radial-gradient(circle, rgba(76,131,255,.26) 0 1px, transparent 1.8px); background-size: 88px 88px, 137px 137px; background-position: 0 0, 34px 52px; opacity: .55; animation: remedyDrift 24s linear infinite; }
@keyframes remedyDrift { from { transform: translate3d(0,0,0); } to { transform: translate3d(-60px,42px,0); } }
```

---

## 25. graph/GraphFilterChips.tsx + module.css

```tsx
import styles from "./GraphFilterChips.module.css";
const filters = [["all", "All"], ["open", "Open"], ["planned", "Planned"], ["done", "Done"]] as const;
export type GraphFilter = (typeof filters)[number][0];
export function GraphFilterChips({ value, onChange }: { value: GraphFilter; onChange: (value: GraphFilter) => void }) { return <div className={styles.chips} aria-label="Graph filters">{filters.map(([key, label]) => <button key={key} type="button" className={value === key ? styles.active : styles.chip} onClick={() => onChange(key)}>{key !== "all" && <span className={styles[key]} />}{label}</button>)}</div>; }
```

```css
.chips { position: absolute; left: 36px; bottom: 34px; z-index: 5; display: flex; align-items: center; gap: 16px; padding: 11px 14px; border-radius: 22px; background: rgba(255,255,255,.68); border: 1px solid rgba(78,111,172,.14); box-shadow: var(--remedy-shadow-soft); backdrop-filter: blur(18px); }
.chip, .active { min-width: 64px; height: 34px; border: 0; border-radius: 999px; padding: 0 16px; background: transparent; color: var(--remedy-blue-900); font-weight: 700; display: inline-flex; gap: 8px; align-items: center; justify-content: center; }
.active { color: white; background: linear-gradient(135deg, #3478ff, #5d8dff); box-shadow: 0 12px 26px rgba(76,131,255,.22); }
.open, .planned, .done { width: 10px; height: 10px; border-radius: 50%; }
.open { background: var(--remedy-purple-400); } .planned { background: var(--remedy-blue-500); } .done { background: var(--remedy-green-500); }
```

---

## 26. graph/BrainGraphStage.tsx + module.css

```tsx
import { useState } from "react";
import type { RemedyDashboard } from "../../api/types";
import { GraphFilterChips, type GraphFilter } from "./GraphFilterChips";
import { RemedyBrainFlow } from "./RemedyBrainFlow";
import styles from "./BrainGraphStage.module.css";
export function BrainGraphStage({ dashboard, selectedNodeId, onSelectNode }: { dashboard: RemedyDashboard; selectedNodeId: string | null; onSelectNode: (nodeId: string) => void }) { const [filter, setFilter] = useState<GraphFilter>("all"); return <section className={styles.stage} aria-label="Growing brain graph"><div className={styles.glassFog} aria-hidden="true" /><RemedyBrainFlow dashboard={dashboard} selectedNodeId={selectedNodeId} onSelectNode={onSelectNode} filter={filter} /><GraphFilterChips value={filter} onChange={setFilter} /></section>; }
```

```css
.stage { position: relative; min-height: 0; border-radius: 32px; overflow: hidden; background: radial-gradient(circle at 46% 50%, rgba(255,255,255,.94), transparent 18%), radial-gradient(circle at 46% 50%, rgba(76,131,255,.18), transparent 42%), linear-gradient(180deg, rgba(255,255,255,.16), rgba(255,255,255,.02)); }
.glassFog { position: absolute; inset: 0; pointer-events: none; background: linear-gradient(90deg, rgba(237,243,251,.82), transparent 18%, transparent 82%, rgba(237,243,251,.62)), linear-gradient(180deg, rgba(237,243,251,.48), transparent 32%, rgba(237,243,251,.34)); z-index: 2; mix-blend-mode: lighten; }
```

---

## 27. panels components + RightLivePanel.module.css

```tsx
// LiveStatusPill.tsx
import styles from "./RightLivePanel.module.css";
export function LiveStatusPill({ live }: { live: boolean }) { return <div className={styles.livePill}><span className={live ? styles.liveDot : styles.idleDot} />{live ? "LIVE" : "IDLE"}</div>; }
```

```tsx
// AgentNowCard.tsx
import CodeIcon from "@mui/icons-material/Code";
import type { RemedyDashboard } from "../../api/types";
import styles from "./RightLivePanel.module.css";
export function AgentNowCard({ dashboard }: { dashboard: RemedyDashboard }) { return <section className={styles.card}><header className={styles.cardHeader}><h2>Agent is doing now</h2><span className={styles.liveSmall}><span /> Live</span></header><div className={styles.agentNow}><div className={styles.actorIcon}><CodeIcon fontSize="small" /></div><div><strong>{dashboard.live.latestActor} is working</strong><p>{dashboard.live.activeTaskLabel}</p></div><time>Just now</time></div></section>; }
```

```tsx
// ActivityFeedCard.tsx
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import CodeIcon from "@mui/icons-material/Code";
import PersonOutlineIcon from "@mui/icons-material/PersonOutline";
import RateReviewOutlinedIcon from "@mui/icons-material/RateReviewOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import type { RemedyActivityItem } from "../../api/types";
import styles from "./RightLivePanel.module.css";
const iconByActor = { Builder: CodeIcon, Reviewer: RateReviewOutlinedIcon, User: PersonOutlineIcon, System: SettingsOutlinedIcon };
export function ActivityFeedCard({ activity }: { activity: RemedyActivityItem[] }) { return <section className={styles.card}><header className={styles.cardHeader}><h2>Chat / Activity</h2></header><div className={styles.activityList}>{activity.slice(0, 4).map(item => { const Icon = iconByActor[item.actor]; return <article key={item.id} className={styles.activityItem}><div className={styles.actorIcon}><Icon fontSize="small" /></div><div><div className={styles.activityMeta}><strong>{item.actor}</strong><span>{item.timeLabel}</span></div><p>{item.message}</p></div></article>; })}</div><div className={styles.askBar}><input readOnly placeholder="Ask something..." aria-label="Ask something" /><button type="button" aria-label="Send disabled" title="Chat input is not enabled yet"><ArrowForwardIcon fontSize="small" /></button></div></section>; }
```

```tsx
// TaskChecklistCard.tsx
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import InsertDriveFileOutlinedIcon from "@mui/icons-material/InsertDriveFileOutlined";
import RadioButtonUncheckedIcon from "@mui/icons-material/RadioButtonUnchecked";
import TripOriginIcon from "@mui/icons-material/TripOrigin";
import type { RemedyTaskItem } from "../../api/types";
import { stateLabel } from "../../copy/humanCopy";
import styles from "./RightLivePanel.module.css";
function iconFor(task: RemedyTaskItem) { if (task.state === "done") return <CheckCircleIcon fontSize="small" />; if (task.state === "current") return <TripOriginIcon fontSize="small" />; if (task.state === "suggested") return <RadioButtonUncheckedIcon fontSize="small" />; return <InsertDriveFileOutlinedIcon fontSize="small" />; }
export function TaskChecklistCard({ tasks, onSelectNode }: { tasks: RemedyTaskItem[]; onSelectNode: (nodeId: string) => void }) { const completed = tasks.filter(t => t.checked).length; return <section className={`${styles.card} remedy-checklist`}><header className={styles.cardHeader}><h2>Tasks</h2><span>{completed} of {tasks.length} completed</span></header><div className={styles.taskList}>{tasks.slice(0, 16).map(task => <button key={task.id} type="button" className={`${styles.taskRow} ${styles[task.state]}`} onClick={() => onSelectNode(task.nodeId)}><span className={styles.taskIcon}>{iconFor(task)}</span><span className={styles.taskLabel}>{task.label}</span><span className={styles.taskState}>{stateLabel(task.state)}</span></button>)}</div></section>; }
```

```tsx
// AddTaskButton.tsx
import AddIcon from "@mui/icons-material/Add";
import styles from "./RightLivePanel.module.css";
export function AddTaskButton() { return <button type="button" className={styles.addTask} title="Task creation from UI is not enabled yet. Use CLI or approve reviewer suggestions." onClick={() => undefined}><AddIcon fontSize="small" />Add Task</button>; }
```

```tsx
// RightLivePanel.tsx
import type { RemedyDashboard } from "../../api/types";
import { ActivityFeedCard } from "./ActivityFeedCard";
import { AddTaskButton } from "./AddTaskButton";
import { AgentNowCard } from "./AgentNowCard";
import { LiveStatusPill } from "./LiveStatusPill";
import { TaskChecklistCard } from "./TaskChecklistCard";
import styles from "./RightLivePanel.module.css";
export function RightLivePanel({ dashboard, onSelectNode }: { dashboard: RemedyDashboard; onSelectNode: (nodeId: string) => void }) { return <aside className={styles.panel}><LiveStatusPill live={dashboard.live.running} /><AgentNowCard dashboard={dashboard} /><ActivityFeedCard activity={dashboard.activity} /><TaskChecklistCard tasks={dashboard.tasks} onSelectNode={onSelectNode} /><AddTaskButton /></aside>; }
```

```css
.panel { position: relative; z-index: 3; display: flex; flex-direction: column; gap: 14px; min-width: 0; }
.livePill { align-self: flex-end; height: 48px; min-width: 110px; display: inline-flex; justify-content: center; align-items: center; gap: 10px; border-radius: 18px; background: rgba(255,255,255,.64); border: 1px solid rgba(78,111,172,.14); box-shadow: var(--remedy-shadow-soft); color: var(--remedy-blue-900); font-weight: 800; letter-spacing: .06em; }
.liveDot, .idleDot { width: 10px; height: 10px; border-radius: 50%; } .liveDot { background: var(--remedy-green-500); box-shadow: 0 0 0 6px rgba(76,198,129,.12); } .idleDot { background: var(--remedy-faint); }
.card { border-radius: 22px; background: rgba(255,255,255,.62); border: 1px solid rgba(78,111,172,.14); box-shadow: var(--remedy-shadow-soft); backdrop-filter: blur(20px); padding: 20px; }
.cardHeader { display: flex; justify-content: space-between; gap: 16px; align-items: center; margin-bottom: 16px; color: var(--remedy-blue-900); }
.cardHeader h2 { margin: 0; font-size: 14px; letter-spacing: .05em; font-weight: 900; text-transform: uppercase; }
.cardHeader span { color: var(--remedy-muted); font-size: 12px; font-weight: 700; }
.liveSmall { display: inline-flex; align-items: center; gap: 6px; } .liveSmall span { width: 7px; height: 7px; border-radius: 50%; background: var(--remedy-green-500); }
.agentNow, .activityItem { display: grid; grid-template-columns: 44px 1fr auto; align-items: center; gap: 12px; }
.agentNow strong, .activityMeta strong { color: var(--remedy-blue-900); font-size: 13px; }
.agentNow p, .activityItem p { margin: 3px 0 0; color: var(--remedy-blue-900); font-size: 12px; line-height: 1.35; } .agentNow time { color: var(--remedy-muted); font-size: 12px; }
.actorIcon { width: 38px; height: 38px; display: grid; place-items: center; border-radius: 50%; color: white; background: linear-gradient(135deg, #3478ff, #75a3ff); box-shadow: 0 12px 22px rgba(76,131,255,.22); }
.activityList { display: flex; flex-direction: column; gap: 16px; } .activityMeta { display: flex; gap: 10px; align-items: center; } .activityMeta span { color: var(--remedy-muted); font-size: 12px; }
.askBar { margin-top: 18px; display: grid; grid-template-columns: 1fr 38px; gap: 10px; } .askBar input { height: 38px; border: 1px solid rgba(78,111,172,.18); border-radius: 10px; padding: 0 12px; background: rgba(255,255,255,.72); color: var(--remedy-blue-900); } .askBar button, .addTask { border: 0; color: white; background: linear-gradient(135deg, #3478ff, #5d8dff); border-radius: 10px; }
.taskList { display: flex; flex-direction: column; gap: 7px; } .taskRow { height: 26px; display: grid; grid-template-columns: 22px 1fr auto; align-items: center; gap: 8px; border: 0; background: transparent; color: var(--remedy-blue-900); padding: 0; text-align: left; } .taskIcon { width: 18px; height: 18px; display: grid; place-items: center; } .taskLabel { overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 12px; font-weight: 700; } .taskState { color: var(--remedy-blue-700); font-size: 11px; font-weight: 800; }
.done .taskIcon { color: var(--remedy-green-500); } .current .taskIcon, .current .taskState { color: var(--remedy-blue-500); } .pending { opacity: .72; } .suggested { opacity: .64; color: var(--remedy-purple-400); }
.addTask { height: 42px; display: flex; align-items: center; justify-content: center; gap: 10px; font-weight: 800; background: rgba(255,255,255,.58); color: var(--remedy-blue-700); border: 1px solid rgba(78,111,172,.14); }
```

---

## 28. timeline/PhaseTimeline.tsx + module.css

```tsx
import AssignmentTurnedInOutlinedIcon from "@mui/icons-material/AssignmentTurnedInOutlined";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";
import CodeIcon from "@mui/icons-material/Code";
import FactCheckOutlinedIcon from "@mui/icons-material/FactCheckOutlined";
import FlagOutlinedIcon from "@mui/icons-material/FlagOutlined";
import RateReviewOutlinedIcon from "@mui/icons-material/RateReviewOutlined";
import type { RemedyPhase } from "../../api/types";
import styles from "./PhaseTimeline.module.css";
const icons = { job: AssignmentTurnedInOutlinedIcon, planning: CalendarMonthOutlinedIcon, build: CodeIcon, test: FactCheckOutlinedIcon, review: RateReviewOutlinedIcon, finalized: FlagOutlinedIcon };
export function PhaseTimeline({ phases }: { phases: RemedyPhase[] }) { return <section className={styles.timeline} aria-label="Project timeline"><div className={styles.mainLine} /><div className={styles.phaseRow}>{phases.map(phase => { const Icon = icons[phase.id]; return <article key={phase.id} className={`${styles.phase} ${styles[phase.state]}`}><div className={styles.phaseIcon}><Icon /></div><span>{phase.label}</span></article>; })}</div><div className={styles.microLine}>{Array.from({ length: 28 }, (_, i) => <span key={i} className={i % 5 === 0 ? styles.microStrong : ""} />)}</div><footer className={styles.legend}><span>LLM Action</span><span>Test</span><span>Review</span></footer></section>; }
```

```css
.timeline { position: relative; border-radius: 26px; padding: 26px 36px 22px; background: rgba(255,255,255,.5); border: 1px solid rgba(78,111,172,.14); box-shadow: var(--remedy-shadow-soft); backdrop-filter: blur(20px); }
.mainLine { position: absolute; left: 58px; right: 58px; top: 66px; height: 2px; background: rgba(39,77,143,.28); }
.phaseRow { position: relative; z-index: 1; display: grid; grid-template-columns: repeat(6, 1fr); align-items: start; }
.phase { display: grid; justify-items: center; gap: 10px; color: var(--remedy-blue-900); font-size: 14px; font-weight: 700; }
.phaseIcon { width: 42px; height: 42px; display: grid; place-items: center; border-radius: 50%; background: rgba(255,255,255,.8); color: var(--remedy-blue-700); border: 1px solid rgba(39,77,143,.24); }
.current .phaseIcon { color: white; background: linear-gradient(135deg, #3478ff, #6da0ff); box-shadow: 0 0 0 8px rgba(76,131,255,.12), 0 14px 28px rgba(76,131,255,.22); }
.done .phaseIcon { color: var(--remedy-green-500); } .pending { opacity: .68; }
.microLine { margin: 18px 74px 0; display: flex; justify-content: space-between; align-items: center; } .microLine span { width: 4px; height: 4px; border-radius: 50%; background: rgba(76,131,255,.32); } .microLine .microStrong { width: 8px; height: 8px; background: rgba(76,131,255,.7); }
.legend { margin-top: 18px; display: flex; justify-content: center; gap: 54px; color: var(--remedy-muted); font-size: 12px; font-weight: 700; }
```

---

## 29. detail/DetailPopover.tsx + module.css

```tsx
import CloseIcon from "@mui/icons-material/Close";
import type { RemedyDashboard, RemedyGraphNode } from "../../api/types";
import styles from "./DetailPopover.module.css";
export function DetailPopover({ dashboard, selectedNode }: { dashboard: RemedyDashboard; selectedNode?: RemedyGraphNode }) { if (!selectedNode) return null; const task = dashboard.tasks.find(i => i.nodeId === selectedNode.nodeId); const title = task?.label || selectedNode.label || "Project item"; const state = task?.state || selectedNode.state; const next = task?.nextAction || dashboard.nextAction; return <aside className={`${styles.popover} remedy-detail-compact`} aria-label="Selected item details"><button className={styles.close} type="button" aria-label="Close details"><CloseIcon fontSize="small" /></button><h2>{title}</h2><div className={styles.state}>{state}</div><section><h3>Why it matters</h3><p>This item is part of the verified path from goal to completed work.</p></section><section><h3>Evidence</h3><ul><li>{task?.checked ? "Completed and checked." : "Waiting for the next safe step."}</li></ul></section><section><h3>Next safe action</h3><code>{next.command}</code></section><button type="button" className={styles.advanced}>Diagnostics</button></aside>; }
```

```css
.popover { position: absolute; z-index: 6; right: calc(var(--remedy-right-width) + 54px); top: 90px; width: 340px; border-radius: 22px; padding: 22px; background: rgba(255,255,255,.78); border: 1px solid rgba(78,111,172,.14); box-shadow: var(--remedy-shadow); backdrop-filter: blur(22px); color: var(--remedy-text); }
.close { position: absolute; right: 14px; top: 14px; width: 28px; height: 28px; border: 0; border-radius: 9px; background: rgba(225,233,246,.72); color: var(--remedy-muted); }
.popover h2 { margin: 0 32px 5px 0; color: var(--remedy-text); font-size: 18px; font-weight: 800; }
.state { color: var(--remedy-muted); font-size: 12px; text-transform: uppercase; font-weight: 800; letter-spacing: .05em; margin-bottom: 18px; }
.popover h3 { margin: 16px 0 6px; font-size: 12px; text-transform: uppercase; color: var(--remedy-muted); letter-spacing: .06em; }
.popover p, .popover li { font-size: 13px; line-height: 1.45; } .popover ul { margin: 0; padding-left: 18px; }
.popover code { display: block; color: var(--remedy-blue-900); background: rgba(237,243,251,.72); border-radius: 10px; padding: 10px; font-size: 12px; white-space: pre-wrap; }
.advanced { margin-top: 16px; border: 0; background: transparent; color: var(--remedy-muted); font-size: 12px; }
```

---

## 30. layers/LayerSwitcher.tsx + module.css

```tsx
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import FactCheckOutlinedIcon from "@mui/icons-material/FactCheckOutlined";
import FolderOutlinedIcon from "@mui/icons-material/FolderOutlined";
import MemoryIcon from "@mui/icons-material/Memory";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import styles from "./LayerSwitcher.module.css";
const layers = [["Journey", AutoAwesomeIcon], ["Proof", FactCheckOutlinedIcon], ["Files", FolderOutlinedIcon], ["Memory", MemoryIcon], ["Diagnostics", SettingsOutlinedIcon]] as const;
export function LayerSwitcher() { return <nav className={`${styles.switcher} remedy-layer-switcher`} aria-label="View layers">{layers.map(([label, Icon], i) => <button key={label} type="button" className={i === 0 ? styles.active : styles.button} aria-label={label}><Icon fontSize="small" /></button>)}</nav>; }
```

```css
.switcher { position: absolute; z-index: 6; left: 32px; top: 328px; width: 62px; padding: 12px 0; display: flex; flex-direction: column; align-items: center; gap: 10px; border-radius: 24px; background: rgba(255,255,255,.52); border: 1px solid rgba(78,111,172,.14); box-shadow: var(--remedy-shadow-soft); backdrop-filter: blur(18px); }
.button, .active { width: 38px; height: 38px; display: grid; place-items: center; border: 0; border-radius: 50%; background: transparent; color: var(--remedy-blue-700); }
.active { color: white; background: linear-gradient(135deg, #3478ff, #6da0ff); box-shadow: 0 12px 22px rgba(76,131,255,.24); }
```

---

## Implementation acceptance checklist

After the agent implements this pack, `remedy ui <job_id>` should show:

```txt
Left: REMEDY logo, concept label, Growing Brain Overview, description, vertical icon dock
Top: Open / Planned / Done / Progress metrics in one rounded glass bar
Center: command pill + large glowing node graph with organic branches
Right: live badge, Agent is doing now, Chat / Activity, Tasks checklist, Add Task
Bottom: Job / Planning / Build / Test / Review / Finalized timeline
Detail: compact human explanation only
```

Smoke must fail if default UI or default API contains:

```txt
Context Coverage
present signals
missing signals
rank
importance
node_type
zone
edge_type
connected_to
raw JSON
metadata wall
debug rail
```

