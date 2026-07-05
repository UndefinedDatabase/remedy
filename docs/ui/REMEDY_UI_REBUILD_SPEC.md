# Remedy UI Rebuild Specification (v2 · 2026-07-05)

> **DESIGN AUTHORITY:** `docs/ui/design_reference/` is the canonical design
> source (`ux_design.png` = visual law; `tokens.css` = token authority;
> `assets_spec.md` = asset authority; `graph_spec.md` = graph authority;
> `ux_spec.md`/`component_spec.md`/`motion_spec.md` = UX/component/motion
> authority; `acceptance_criteria.md` = visual QA authority). Where this file
> and the design reference disagree, **the design reference wins**. The v1
> inline token palette and the v1 five-level zoom table were removed for that
> reason; the old values are void.

## 1. Purpose of this file
The build-structure contract: component tree, data contracts, state model,
CSS-module layout. Visual values live in the design reference, not here.

## 2. Visual target summary
Premium bright glass cockpit around the Growing Brain graph: what the job is,
what is open/planned/done, what the agent is doing now, task states, the next
action. No debug wording, no raw graph internals (list: `ux_spec.md` §17).

## 3. Component tree (current canonical path)
```
RemedyApp
  RemedyShell
    LeftBrandRail
      RemedyLogo            (RemedyMark + wordmark — assets_spec §5)
      JobHeader             (kicker=project · title=job · description;
                             formerly "ConceptIntro" — README §K1)
      SideIconDock
    MainStage
      TopMetricsBar
      CommandBar
      BrainGraphStage
        GraphFilterChips
        renderers/ForceBrainRenderer   (fg-2d custom paint — graph_tech_recommendation.md)
        useSemanticZoom                (L0–L3 machine — graph_spec §10)
        BrainGraphCanvas               (simple/no-WebGL fallback until Stage 6)
      PhaseTimeline
    RightLivePanel
      LiveStatusPill
      AgentNowCard
      NeedsAttentionCard    (renders only when relevant)
      ActivityFeedCard
        ChatInput           (disabled until steering exists — ux_spec §11.3)
      TaskChecklistCard
      AddTaskButton         (disabled until injection exists)
    DetailPopover
    LayerSwitcher           (behind "System details")
    DegradedBanner
    ReducedMotionProvider
```
Superseded (do not build against): `RemedyBrainFlow`, `SemanticZoomController`,
`ConstellationBackdrop`, `SoftGlowEdge` (all `graph/legacy/`; mine
`organicLayout.ts`/`semanticZoom.ts` for ideas, then archive per Stage 6).
`NetworkLogoIcon` is deprecated (assets_spec §5). Any React-Flow wording in
older docs is historical — the renderer decision is fg-2d custom paint.

## 4. Data contracts
All components consume normalized `RemedyDashboard` from `api/remedyApi.ts`;
raw API payloads never pass through. The adapter strips forbidden words,
normalizes states (`suggested`→open, `pending`→planned, `current`→in-progress)
and maps internals to human labels (`humanCopy.ts`). Key types:
`RemedyDashboard`, `RemedyMetric`, `RemedyTaskItem`, `RemedyActivityItem`,
`RemedyGraphNode/Edge`, `RemedyPhase`, `RemedyNextAction`.

## 5. State model
Dashboard polled every 5 s (SSE arrives with roadmap F008); `selectedNodeId`;
graph filter all/open/planned/done (local); layer selection (local); reduced
motion from the OS media query (Provider + renderer both honor it).

## 6. Semantic zoom
Canonical model: `graph_spec.md` §10 (L0 organism · L1 task focus · L2 run
popover · L3 evidence panel; thresholds with hysteresis, clusters >8,
breadcrumbs, Esc). One preserved rule from v1, still binding: **diagnostics
content never appears through zoom alone — it requires the explicit
diagnostics layer toggle.**

## 7. CSS module architecture
Co-located `*.module.css` per component; all visual tokens come from
`styles/tokens.css`, which adopts `design_reference/tokens.css` (namespace
`--remedy-*`). No Tailwind. Fonts are self-hosted via npm per `assets_spec.md`
§1–§2 — no remote/CDN assets (that is the correct reading of v1's "no
external fonts": no *remote* fonts; bundled webfonts are required).
Module files: RemedyShell, BrainGraphStage, RightLivePanel, PhaseTimeline,
TopMetricsBar, CommandBar, GraphFilterChips, DetailPopover, LayerSwitcher,
LeftBrandRail, RemedyLogo, SideIconDock, ChatInput (+ renderer-internal
styles live in canvas code via the `renderers/palette.ts` token bridge).

## 8. Forbidden default UI words
Single source: `design_reference/ux_spec.md` §17 (rank, importance, node_type,
metadata, …, raw stdout/stderr, traceback). Enforced in `humanCopy.ts` and the
copy audit (`acceptance_criteria.md` §3/§7). Not duplicated here.

## 9. Tokens
See `design_reference/tokens.css` — the only palette. Layout widths mirror
the pixel-lock contract (`--remedy-left-width: 292px`,
`--remedy-right-width: 350px`, frame 1678×926).
