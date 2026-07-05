# H — Staged Implementation Plan (for coding agents)

Global rules for every stage: tokens only (no literals); screenshot fidelity
over personal taste (deviations → deviations.md); do not touch `packages/**`
except additive read fields; keep `humanCopy.ts` wording discipline; every
stage ends with the visual acceptance ritual from J.

## Stage 1 — Static faithful layout & tokens
Goal: the frame matches the screenshot with live-but-static data.
Touch: `apps/ui/src/styles/tokens.css` (adopt canonical tokens), `globals.css`,
rail/metrics/command/panels/timeline `*.module.css`, `LeftBrandRail.tsx`
(JobHeader slot), `TaskChecklistCard.tsx` (tiles+count), `ActivityFeedCard.tsx`
(discs+ChatInput disabled), `CommandBar.tsx` (pill+buttons),
`GraphFilterChips.tsx` (dock style), `PhaseTimeline.tsx` (legend row). New:
`panels/ChatInput.tsx`, stylelint token gate. Tests: vitest snapshots per
card; stylelint CI; region-geometry test against the pixel-lock table.
Accept: side-by-side ≤ minor deltas per J checklist (graph excluded).
Risks: token value churn — settle via review, then freeze. Must not change:
api types, server, graph logic.

## Stage 2 — Real data wiring & basic graph
Goal: ForceBrain renderer mounted with correct entities/states; no premium FX.
Touch: `BrainGraphStage.tsx` (mount swap + fallback prop),
`ForceBrainGraph.tsx` → `renderers/ForceBrainRenderer.tsx`, new
`renderers/palette.ts` + `renderers/glyphPaths.ts`, `buildForceBrainModel.ts`
(runs/synapses from promptTrace, tests). Tests: builder unit (extended), truth
property (real ids only), fallback path renders. Accept: correct counts vs
chips/metrics; stable seeded layout across reloads. Must not change: popover
resolution logic.

## Stage 3 — Live event-driven graph
Goal: births/completions animate from data changes (polling differ).
Touch: model differ in `buildForceBrainModel.ts`, renderer birth/ripple
queue, `AgentNowCard` crossfade. Tests: differ unit (snapshot pairs → event
list), stagger rule (≤3 concurrent), reduced-motion path. Accept: a replayed
fixture session shows calm sequential growth; no layout explosions (frozen
sim + local reheat). Risks: polling jitter — debounce 2 ticks.

## Stage 4 — Semantic zoom & detail
Goal: L0–L2 + scrubber preview. Touch: new `graph/useSemanticZoom.ts`
(mine legacy thresholds), renderer dim/fan logic, `DetailPopover` anchoring,
`PhaseTimeline` scrubber (replay = re-render model at seq prefix; REPLAY pill).
Tests: zoom transition matrix, scrub property (state(s) == fold(events ≤ s)
over the differ), popover a11y (focus trap). Must not change: URL/router
assumptions (none exist — keep it that way).

## Stage 5 — Premium animation & polish
Goal: the organism feeling. Touch: renderer only — curved beaded edges, glow
sprites, particles, starfield/vignette layer, core breath, tip decor;
`motion_spec` timings. Tests: golden matrix (states × zoom × motion-off),
particle budget assertion. Accept: the J §2 human checklist passes on the
rest-state comparison. Risks: fps — measure after each effect; degrade order
per graph_spec §13.

## Stage 6 — Performance, a11y, fidelity hardening
Goal: gates locked. Touch: perf fixtures (200/500 nodes) + CI frame-time
budget, list-view toggle (DOM parity surface), aria-live wiring, axe pass on
the shell, golden-screenshot CI with tolerance, archive `graph/legacy/` +
stale root pack (banner → docs/archive), remove-MUI decision PR (separate).
Accept: all J budgets green; “do not pass if” list clean.
