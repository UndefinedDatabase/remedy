# Remedy UI Rebuild Specification

## 1. Visual Target Summary

The Remedy UI is a premium, bright white/pale blue glass dashboard that lets users instantly understand:
- What the job is
- What is open/planned/done
- What the agent is doing now
- Which tasks are completed/in progress/planned
- What the next action is

The design uses glass cards, soft shadows, large rounded corners, and a growing brain graph at center. No debug wording. No raw graph internals.

## 2. Component Tree

```
RemedyApp
  RemedyShell
    LeftBrandRail
      RemedyLogo
      ConceptIntro
      SideIconDock
    MainStage
      TopMetricsBar
      CommandBar
      BrainGraphStage
        GraphFilterChips
        RemedyBrainFlow
        SemanticZoomController
      PhaseTimeline
    RightLivePanel
      LiveStatusPill
      AgentNowCard
      ActivityFeedCard
      TaskChecklistCard
      AddTaskButton
    DetailPopover
    LayerSwitcher
    ReducedMotionProvider
```

## 3. Data Contracts

All components consume normalized `RemedyDashboard` data from `api/remedyApi.ts`. Raw API payloads are never passed directly. The adapter strips forbidden words, normalizes states, and maps internal concepts to human labels.

Key types: `RemedyDashboard`, `RemedyStory`, `RemedyJourneyItem`, `RemedyMetric`, `RemedyTaskItem`, `RemedyActivityItem`, `RemedyGraphNode`, `RemedyGraphEdge`, `RemedyPhase`, `RemedyNextAction`.

## 4. State Model

- Dashboard loaded from API, refreshed every 5s
- Selected node tracked as `selectedNodeId`
- Graph filter: all/open/planned/done (local state)
- Layer selection: journey/proof/files/memory/diagnostics (local state)
- Reduced motion: from OS media query

## 5. Accessibility Notes

- All interactive elements have aria-labels
- Reduced motion respected via `prefers-reduced-motion`
- Color is not sole indicator (icons + labels)
- Keyboard: Escape closes detail popover
- All text meets minimum contrast on light background

## 6. Semantic Zoom Rules

| Level | Viewport Zoom | Visible |
|-------|--------------|---------|
| 0 Overview | < 0.36 | Root + major branches only |
| 1 Phase | 0.36 - 0.62 | Root + phases + current task |
| 2 Work | 0.62 - 0.92 | Task/change/apply/test items |
| 3 Proof | 0.92 - 1.28 | Proof/review/memory candidates |
| 4 Diagnostics | > 1.28 | All visible (diagnostics only if layer enabled) |

Diagnostics nodes never appear just by zoom — require explicit diagnostics layer toggle.

## 7. CSS Module Architecture

Each component has a co-located `.module.css` file. All visual tokens live in `styles/tokens.css`. No global class collisions. No Tailwind. No external fonts or CDN.

Module files:
- `RemedyShell.module.css`
- `BrainGraphStage.module.css`
- `RightLivePanel.module.css`
- `PhaseTimeline.module.css`
- `TopMetricsBar.module.css`
- `CommandBar.module.css`
- `GraphNodes.module.css`
- `GraphFilterChips.module.css`
- `RemedyBrainFlow.module.css`
- `DetailPopover.module.css`
- `LayerSwitcher.module.css`
- `LeftBrandRail.module.css`
- `RemedyLogo.module.css`
- `SideIconDock.module.css`

## 8. Full Component Checklist

- [x] RemedyApp — entry point, data loading, error state
- [x] RemedyShell — 3-column grid layout
- [x] ReducedMotionProvider — context for animation preference
- [x] LeftBrandRail — logo, concept, description
- [x] RemedyLogo — network icon + wordmark
- [x] SideIconDock — 7 icon buttons
- [x] TopMetricsBar — 4 metric tiles
- [x] CommandBar — search pill, copy-only
- [x] BrainGraphStage — graph container with filter chips
- [x] RemedyBrainFlow — React Flow wrapper
- [x] GraphNodes (Root/Work/Tiny) — custom node renderers
- [x] SoftGlowEdge — custom edge renderer
- [x] GraphFilterChips — All/Open/Planned/Done
- [x] organicLayout — deterministic graph layout
- [x] semanticZoom — zoom level calculation
- [x] RightLivePanel — right column container
- [x] LiveStatusPill — live/idle indicator
- [x] AgentNowCard — current activity
- [x] ActivityFeedCard — chat/activity feed
- [x] TaskChecklistCard — task list with states
- [x] AddTaskButton — disabled placeholder
- [x] PhaseTimeline — 6-phase bottom bar
- [x] DetailPopover — selected node details
- [x] LayerSwitcher — view layer controls
- [x] NetworkLogoIcon — SVG logo
- [x] CodeOrbIcon — SVG code node

## 9. Forbidden Default UI Words

Default UI must NEVER show:
- rank
- importance
- node_type
- metadata
- present signals
- missing signals
- context coverage
- zone
- edge_type
- connected_to
- raw UUID labels
- raw JSON blobs
- raw stdout/stderr
- command_output
- diff_preview
- approval_reason
- traceback

## 10. CSS Tokens

```css
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
```
