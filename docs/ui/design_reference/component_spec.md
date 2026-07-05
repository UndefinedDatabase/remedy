# E — Component Breakdown

Format per component: purpose · structure · states · data · interaction ·
motion · a11y · **existing path** / recommended path · token deps.
"exists" paths are verified in the review bundle.

## AppShell (`RemedyShell`)
Frame-scaled grid per ux_spec §2. States: normal, degraded (banner), detail-open.
Data: `RemedyDashboard`. Exists: `apps/ui/src/components/shell/RemedyShell.tsx`
(+ `RemedyShell.module.css`). Keep composition; move region sizes onto
`--remedy-frame-*`/width tokens. A11y: landmark roles (aside/main), skip link.

## BrandSidebar (`LeftBrandRail`)
Purpose: identity + job context + nav. Structure: logo row (NetworkLogoIcon +
"REMEDY" 16/700 +0.14em), **JobHeader slot** (kicker=project, title=job,
description ≤3 lines, ink-soft), SideIconDock. Exists:
`components/rail/LeftBrandRail.tsx`. Change: rename concept copy to JobHeader
bindings (`dashboard.title`, project name, job description). A11y: h1 = job
title.

## VerticalNavigation (`SideIconDock`)
7 slots (overview, tasks, activity, files, history, docs, settings — final set
= existing dock order; do not invent routes). States: active/hover/focus/
disabled. Interaction: click routes/scrolls; tooltip on hover/focus. Exists:
`components/rail/SideIconDock.tsx`. Tokens: glow, blue-50, focus.

## MetricsBar (`TopMetricsBar`)
4 segments (OPEN, PLANNED, DONE, PROGRESS) per ux_spec §10. Data:
`dashboard.metrics` (keys open/planned/done/progress; keep tests/proof/tokens
for the advanced layer — LayerSwitcher — not in the hero bar). States: value,
"—" unknown, warn tint when blocked>0 (dot on OPEN). Exists:
`components/metrics/TopMetricsBar.tsx`. Motion: progress width `--remedy-dur-slow`.
A11y: each segment a labelled group; progress has role=progressbar.

## CommandBar
Per ux_spec §9. Data: task labels for jump; later command catalog (F044).
States: idle/focus/typing(dropdown)/disabled-send. Exists:
`components/command/CommandBar.tsx` (jump logic `handleJump` in RemedyShell —
keep). Add: sparkle disc, return-arrow button, dropdown sheet. A11y: combobox
pattern (aria-expanded, listbox, active-descendant).

## GrowingBrainGraph
The center organism — full spec in `graph_spec.md`; renderer decision in
`graph_tech_recommendation.md`. Exists (three generations, see audit):
mount point `components/graph/BrainGraphStage.tsx`. Recommended structure:
```
components/graph/
  BrainGraphStage.tsx        (mount + chips dock + empty tips)   [exists]
  buildForceBrainModel.ts    (data → nodes/links)                [exists+test]
  renderers/
    palette.ts               (token bridge, NEW)
    ForceBrainRenderer.tsx   (fg-2d custom paint, evolve from ForceBrainGraph.tsx)
```
`BrainGraphCanvas.tsx` (SVG) stays as the automatic no-WebGL/simple fallback
and the screen-reader-adjacent list source until Stage 6.

## BrainNode / BrainEdge / BrainCluster / BrainLegend
Painted, not DOM (see graph_spec §4–8, §11). BrainLegend: the filter-chip dock
doubles as the legend (screenshot shows no separate legend); a hover legend
tooltip on the dock explains states — same glyph paths as painted nodes
(export SVG from the shared path source).

## FilterChips (`GraphFilterChips`)
Values all/open/planned/done. Exists: `components/graph/GraphFilterChips.tsx`.
Style per ux_spec §13; state stays in BrainGraphStage. A11y: aria-pressed
buttons; filter changes announce via polite live region ("Showing done tasks").

## PhaseTimeline + TimelineScrubber
Exists: `components/timeline/PhaseTimeline.tsx` (phases + event chips with
test/review kinds). Add: glyph legend row, scrubber handle on current stop
(drag = replay preview; Stage 4 wires to event prefix). Data: phases + events
(existing), later seq cursor. A11y: slider role for scrubber (aria-valuenow =
seq), chips are buttons focusable in phase groups.

## AgentNowCard
Exists: `components/panels/AgentNowCard.tsx`. Bind: newest activity of kind
build/review with mono span for symbols; "LIVE" chip only in the panel header
(LiveStatusPill), not duplicated here. Motion: content crossfade
`--remedy-dur-base` on change; activity dot pulse.

## ActivityFeed (+ chat frame)
Exists: `components/panels/ActivityFeedCard.tsx`. Add: role discs (builder
`</>` blue, reviewer person violet, user initial disc, system dot), the
disabled "Ask something…" input + send button (ux_spec §11.3). Data:
`dashboard.activity` (actor/message/timeLabel/kind/taskId). Interaction: row
click → onSelectNode(task). Feed autoscroll pinned-to-bottom unless user
scrolled up (show "↓ new" pill then). A11y: feed is aria-live=polite (throttled
to 1 announcement / 5s), input has honest disabled description.

## SteeringInput / ChatInput
The input above, as its own small component so enabling later (roadmap F030
lineage) is a prop flip: `<ChatInput disabled reason=… onSend=…/>`. New file:
`components/panels/ChatInput.tsx`.

## TaskList (`TaskChecklistCard`) / TaskRow / AddTaskButton
Exists: `components/panels/TaskChecklistCard.tsx`. Add: header count
("24 of 36 completed" from tasks), state tiles + right status text per
ux_spec §11.4, AddTaskButton row (disabled until injection exists; honest
tooltip). TaskRow interaction: click selects node (exists), Enter/Space
keyboard, focus ring. Blocked rows: red dot + "Blocked" + reason tooltip
(`blockedReason` field exists).

## DetailPanel / EvidencePanel entry (`DetailPopover`)
Exists: `components/detail/DetailPopover.tsx` (task detail incl. prompt trace
highlight resolution in RemedyShell — keep resolution logic). Style: glass
sheet radius 20, right-anchored near node or right-panel edge; sections:
outcome summary, changed files (safe list), test/proof status, prompt trace
list (redactedPreview mono 12), buttons: "Open diff" (DiffViewer entry),
"Open app" (RuntimePreview entry). States: loading skeleton, empty ("No
evidence yet"), error "—". A11y: dialog role, focus trap, Esc closes
(exists per shell props).

## DiffViewer entry point
Not in this screenshot; entry = button in DetailPopover emitting
`onOpenDiff(taskId)` (no-op today; roadmap F037 lineage). Do NOT build the
viewer in this package's scope.

## RuntimePreview entry point
Same pattern: "Open app" button emitting `onOpenPreview()`; visible only when
`dashboard` exposes a runtime URL (not yet). Disabled otherwise with tooltip.

## Shared
LiveStatusPill (exists) — pulse dot; REPLAY variant (violet) for scrub state.
DegradedBanner (exists) — unchanged, canonical error surface.
NeedsAttentionCard (exists) — warn glass card, renders only when relevant.
LayerSwitcher (exists) — keep behind "System details"; not in hero layout.
