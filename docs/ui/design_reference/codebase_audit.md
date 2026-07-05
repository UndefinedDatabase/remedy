# B — Codebase Design Audit (grounded in the review bundle, 2026-07-04)

## Stack (verified)
- **Frontend:** React 19, TypeScript 5.7, Vite 6, CSS Modules; `vitest` unit
  tests. Dependencies include `react-force-graph-2d@1.29.1`, `d3-force@3`,
  and MUI (`@mui/material`, `@mui/icons-material`) — **CORRECTION (asset
  audit pass):** `@mui/icons-material` IS used in three secondary surfaces
  (`components/pipeline/StopReasonCard.tsx`, `components/pipeline/
  PipelineTimeline.tsx`, `components/layers/LayerSwitcher.tsx`); migration
  + removal plan: `assets_spec.md` §3. `@mui/material` itself remains a leftover from the superseded
  `remedy_ui_component_implementation_pack.md` (which mandated MUI +
  `@xyflow/react`; neither direction was followed — the pack is stale).
- **Backend for the UI:** `packages/orchestration/ui_server.py` (stdlib HTTP),
  polling endpoints `GET /api/jobs/{id}/dashboard` and
  `GET /api/jobs/{id}/brain-view-model` (`apps/ui/src/api/remedyApi.ts:578-596`).
  **No SSE yet** (roadmap F008 pending) — the UI polls.
- **Tests:** `apps/ui/src/**/**.test.ts` (vitest: `cockpitLogic`, `remedyApi`,
  `buildForceBrainModel`), plus Python `tests/ui_server/`, `tests/ui_contracts/`.
  **No Playwright/E2E in the UI app yet.**

## UI structure (verified paths)
`apps/ui/src/RemedyApp.tsx` → `components/shell/RemedyShell.tsx` composes:
- `rail/LeftBrandRail.tsx` (+ `RemedyLogo.tsx`, `SideIconDock.tsx`)
- `metrics/TopMetricsBar.tsx`
- `command/CommandBar.tsx` (jump-to over task labels already works)
- `graph/BrainGraphStage.tsx` → **active renderer: `BrainGraphCanvas.tsx` (SVG,
  deterministic radial layout, prompt satellites, filter-aware)** +
  `GraphFilterChips.tsx`
- `timeline/PhaseTimeline.tsx` (phases + event chips incl. test/review kinds)
- `panels/RightLivePanel.tsx` (LiveStatusPill, AgentNowCard, NeedsAttentionCard,
  ActivityFeedCard, TaskChecklistCard, "System details" toggle)
- `detail/DetailPopover.tsx`, `shell/DegradedBanner.tsx`,
  `shell/ReducedMotionProvider.tsx`, `layers/LayerSwitcher.tsx`
- Icons: `icons/RemedyGlyphs.tsx`, `icons/CodeOrbIcon.tsx`, `icons/NetworkLogoIcon.tsx`

Three graph generations coexist:
1. `graph/legacy/` — `RemedyBrainFlow.tsx` + `organicLayout.ts` +
   `semanticZoom.ts` + `SoftGlowEdge.tsx` + `ConstellationBackdrop.tsx` (SVG;
   superseded, kept as reference for organic layout + zoom ideas).
2. `graph/BrainGraphCanvas.tsx` — **currently mounted**; honest but visually
   plain (straight SVG edges, simple radial fan; caps at 80 tasks).
3. `graph/ForceBrainGraph.tsx` + `buildForceBrainModel.ts` +
   `forceBrainTypes.ts` — react-force-graph-2d with custom node painting
   (radial-gradient root glow, glossy state spheres, `layout_only` decorative
   dots excluded from hit-testing/counting) and custom link painting. **Built
   and unit-tested, not mounted by `BrainGraphStage`.**

## Styling system & tokens (verified)
- `apps/ui/src/styles/tokens.css` — `--remedy-*` namespace: ink/bg scales,
  blue 50–950 ramp, status palette (`--remedy-state-done #34c27e`,
  `-current #4c83ff`, `-open #a78bfa`, `-planned #ffffff` + ring `#9db9ee`,
  `-blocked #ef6363`), glass surfaces, radii (26/20/14/10), card/soft/glow
  shadows, rail widths (280/372). Comment marks the status palette as the
  "single source of truth" — good discipline, keep it.
- `apps/ui/src/styles/globals.css` — body background gradient (white bloom over
  `#ecf2fb`), `.remedy-glass-card` utility (blur 14px), reduced-motion global
  kill switch, thin scrollbars.
- **Gaps:** no spacing scale, no z-index layers, no motion duration/easing
  tokens, no graph-specific tokens (edge glow, particle, halo) — hardcoded
  rgba values live inside `ForceBrainGraph.tsx`/module CSS instead.

## Design docs already in the repo
- `docs/ui/design_reference/ux_design.png` — the law (this screenshot).
- `docs/ui/RICHTIG_PIXEL_LOCK_SPEC.md` — fixed 1678×926 frame + region table
  (left 0/0/292/926, stage 292/0/976/926, right 1286/24/350/832, metrics
  292/24/976/90). **Matches the screenshot 1:1 at ≈1.295× — keep as the layout
  contract.**
- `docs/ui/REMEDY_UI_REBUILD_SPEC.md` — component tree + copy rules; partially
  outdated (names `RemedyBrainFlow`/`SemanticZoomController` as the center).
- `remedy_ui_component_implementation_pack.md` (repo root) — **superseded**
  (mandates MUI + React Flow); its "hard rule" list of forbidden debug wording
  is still valuable → absorbed into `ux_spec.md` §Copy.
- Roadmap at audit time: `docs/roadmap/ROADMAP.md` (German v3.0, 150 features)
  — **superseded by the unified English roadmap shipped alongside this package**
  (same F-numbers; cockpit files are `T5_F0xx.md`); audit statements about
  feature files refer to the audited snapshot. +
  `docs/roadmap/features/T1_F008…T1_F044` cockpit files; `T1_F019` already
  fixes the staged renderer decision (fg-2d now, GPU later). CONVENTIONS.md
  carries the `--rm-*` token block (namespace conflict → see README K3).

## What already matches the screenshot
- Overall shell geometry and the glass language (region table, radii, shadows).
- Status color mapping incl. the Open=violet / Planned=white+ring / Done=green
  legend; state naming bridge (`suggested`=open, `pending`=planned) exists in
  code comments (`ForceBrainGraph.tsx:18-27`).
- Right panel composition (now-card, activity, tasks) and LIVE pill.
- Phase timeline with test/review event chips.
- Reduced-motion plumbing (`ReducedMotionProvider`, global CSS kill).
- Copy discipline (no debug wording) per the rebuild spec + humanCopy.ts.

## What does not match (the fidelity gap)
1. **Center graph**: active SVG renderer has straight edges, no glow bloom, no
   particles, no starfield depth, no organic branch curvature, no semantic zoom.
2. **Command bar**: present but not the screenshot's pill with sparkle icon +
   right return-arrow button (verify styling in Stage 1).
3. **Right panel chat**: activity feed exists; the screenshot's inline chat
   input ("Ask something…") and avatar discs need styling/slotting;
   NeedsAttentionCard has no screenshot slot (keep, collapsed styling).
4. **Filter chips**: exist; need the pill dock style (solid "All", dotted
   status dots) and positioning bottom-left of the stage.
5. **Timeline**: needs the sub-glyph legend row (`</>` LLM Action / flask Test
   / person Review) and scrubber affordance styling.
6. **Tokens**: missing spacing/z/motion/graph tokens (see D).

## Preserve / replace
- **Preserve:** shell + region contract, tokens.css namespace and status
  palette, RightLivePanel composition, PhaseTimeline logic, CommandBar jump
  logic, DetailPopover, ReducedMotionProvider, api/types.ts view-model,
  `buildForceBrainModel.ts` (+test) as the graph data builder, humanCopy.
- **Replace/refactor later:** `BrainGraphCanvas.tsx` as the mounted renderer
  (swap to the ForceBrainGraph path per G), `graph/legacy/**` (archive after
  Stage 5; mine `organicLayout.ts`/`semanticZoom.ts` first), MUI dependency
  (removal candidate — separate cleanup PR), stale
  `remedy_ui_component_implementation_pack.md` (move to `docs/archive/` with a
  DEPRECATED banner).
- **Do not touch:** `packages/**` server logic beyond additive read endpoints;
  `docs/roadmap/**` feature semantics (only the reference block insertions of
  Deliverable I); evidence/redaction paths feeding the dashboard.
