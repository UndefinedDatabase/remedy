# F — Growing Brain Graph Specification

The graph is the product's face. It must read as a **living neural organism**:
a glowing code core, soft luminous dendrites, small glossy nodes, quiet
particle life. Not a force-graph demo, not a hairball, not confetti.

## 1. What the graph represents
One job. The core is the job; branches are work lineage; every visible mark is
a REAL entity from the dashboard/brain view-model (server truth). Decorative
elements are explicitly non-semantic and non-interactive (see §8) — truth
discipline is a feature (`layout_only` pattern already exists and is correct).

## 2. Node ontology (aligned with `api/types.ts` + roadmap Part I)
Kinds: `job_core`, `task`, `builder_run`, `review_run`, `repair_run`,
`test_run`, `synapse` (tool/prompt call), `artifact`, `cluster` (+`decor`,
non-semantic). Current view-model supplies job/tasks/prompt-trace →
builder/review/repair runs come from prompt kinds (`initial|review|repair|
re-review`); test runs from task testStatus events; artifacts from
changedFilesSafe (Stage 2 keeps to what the API provides — no invented nodes).

States: `open` (suggested), `planned` (pending), `in_progress` (current),
`pass` (done), `fail/blocked`, `vetoed` (future; struck style reserved).

## 3. Hierarchy & parent/child rules
core → task (1:n) → run (1:n per task, chronological fan) → synapse (per run,
throttled/clustered) and artifact (docked to producing run). Children may not
outlive collapsed parents (cluster instead). Parent edge is mandatory; cross
edges only for mission lineage (future) — never decorative cross links between
real nodes.

## 4. Geometry & sizes (frame px; canvas world units 1:1 at zoom 1)
- core: r 26 sphere + halo r 64 (existing values — keep; screenshot ≈ r 24–28)
- task: r 7 (major) / 5.5 (minor value<8) — keep existing thresholds
- run: r 4.5; synapse: r 1.6–2.2; artifact: 7×9 doc glyph; cluster: r 9 + count
- decor dot: r 1.8 max, never larger than a synapse
- hit area: node r+4, min 10 (touch); decor & stars: NO hit area (enforced)

## 5. Colors, glow, glyphs
Fills from `--remedy-state-*`; glossy sphere = radial gradient white-highlight
→ state fill (existing painter — keep). Rings: soft state ring at 35–40%
alpha (existing STATE_RING — move to palette bridge). Core: `--remedy-graph-
core-hi→lo` gradient + `--remedy-graph-core-halo` radial halo + white `</>`
glyph (existing). Glyphs for run kinds at zoom ≥ L1: builder `</>`, review
head-and-shoulders, test flask, repair `</>`+ring — Path2D from ONE module
(`renderers/glyphPaths.ts`, evolve from `icons/RemedyGlyphs.tsx` so SVG legend
and canvas share geometry). No emoji, no fonts for glyphs except the core's
`</>` which may stay text (already monospace-painted) for crispness.

## 6. Organic branching (the look that beats generic force graphs)
- **Edges are curved filaments, not straight lines**: quadratic curves through
  a per-edge jitter control point (seeded by edge id — deterministic), plus
  1–2 painted "bead" micro-dots along active branch edges (screenshot shows
  beaded dendrites).
- Two-pass stroke: outer glow pass (`--remedy-graph-edge-glow`, width 3–5,
  50% alpha, only on branches with any non-planned descendant) + core filament
  (`--remedy-graph-edge-core`, width 1.2–1.6). Idle/planned branches: single
  pass `--remedy-graph-edge-idle` width 1.
- **Trunk thickness decays with depth** (core→task 2.2 → run 1.4 → synapse 1).
- Force layout tuning (d3-force): link distance grows with depth (core-task
  120–170, task-run 34, run-synapse 14), charge −60 tasks / −12 runs, radial
  force on tasks (radius by branch index) for the screenshot's radial spread;
  collision r+3. Seeded initial angles = golden-angle around the core so
  layouts are stable per job (seed = job id).
- Decorative frontier: each ACTIVE branch tip gets 2–4 `decor` dots fading
  outward (growth suggestion); planned branches get none. Total decor budget
  ≤ 120 dots (estimated) — it is garnish.

## 7. Behavior by state
- **Active branch** (any in_progress descendant): glow pass on, particles on
  (one white particle per active run edge, `--remedy-dur-particle` traversal,
  ≤ 24 concurrent — budget), tip decor animated at 0.6 alpha breathing.
- **Planned branch**: pale, thinner, no glow, nodes white+ring, 90% scale.
- **Done branch**: filament stays white but glow fades to 25% over 1.2s after
  completion; nodes green; no particles.
- **Failed/blocked**: node warn-red + small status dot; branch glow OFF and
  edge tinted `rgba(239,99,99,.35)` from failing node outward only (do not
  redden the whole organism).
- **Vetoed** (reserved): gray node with strike slash, downstream 40% alpha.
- **Core**: idle breath (halo 0.9→1.06 scale, 3.2s); "thinking" (any provider
  call active) = +15% halo alpha.

## 8. Truth rules
Every rendered REAL node maps 1:1 to a view-model entity with an id; counts in
chips/metrics NEVER include decor/stars (already enforced via `sourceKind ===
"layout_only"` — keep the pattern and the pointer-paint exclusion). No fake
progress motion: particles flow only while a run is actually active per data.

## 9. Depth layers (canvas paint order)
1. vignette (`--remedy-graph-vignette` radial, corners)
2. starfield: ~140 static speckles r 0.6–1.4, `--remedy-graph-star`, seeded,
   parallax 0.15× on pan (estimated count)
3. idle edges → 4. glow edges → 5. particles → 6. decor dots →
7. real nodes → 8. core → 9. labels (zoom-gated, ≥1.4 scale — existing rule)

## 10. Semantic zoom (L0–L3)
- **L0 organism** (default, fits-all): core + tasks + branch glow; runs
  collapsed into branch beads; cluster chip "+n" when a task has >8 children.
- **L1 task focus** (click task / zoom ≥1.6 on it): focused task's runs fan
  out; siblings dim to 25%; label on.
- **L2 run detail** (click run): DetailPopover anchored to node — verdict,
  tokens, duration, prompt kind; buttons diff/why (existing popover carries
  prompt-trace resolution — reuse).
- **L3 evidence**: popover "expand" → right-side evidence panel (Stage 4+;
  DetailPopover is the entry until then).
Transitions: wheel thresholds with hysteresis (in >1.6 on node, out <0.8),
click = same transitions, Esc walks back, breadcrumb chip top-left of stage.
State machine in `useSemanticZoom.ts` (adopt the legacy file's ideas; new
implementation lives beside the renderer, renderer-agnostic).

## 11. Event-to-graph mapping (Stage 3, polling now / SSE later)
plan task appears → task birth; run/prompt item appears → run birth + branch
activates; testStatus flips → test node state; task done → completion ripple;
blocked → fail treatment. With polling, diff consecutive snapshots to derive
birth/death events (model differ in `buildForceBrainModel` — extend, tested);
with SSE (F008 later) map envelope types directly. Ordering: births animate in
data order, max 3 concurrent staggered 90ms (calm rule).

## 12. Animation rules (see motion_spec.md for the system)
- **Birth**: node scales 0→1 with soft-out spring `--remedy-dur-birth`, parent
  edge draws in (line-dash reveal) simultaneously; glow pulse 600ms once.
- **Completion**: 300ms white ring ripple r→r+14 fade; state color crossfade.
- **Active pulse**: in_progress nodes ±8% scale, `--remedy-dur-pulse` loop.
- **Particles**: linear along the curved edge path, 2–3px, additive-ish alpha.
- **Reduced motion**: births = 180ms fade, no particles, no pulse (static 70%
  glow), ripple = none; ALL state remains readable statically.

## 13. Performance strategy
- Glow WITHOUT per-frame `shadowBlur`: pre-render radial-gradient sprites
  (offscreen canvas per state color + halo sizes) and `drawImage` them —
  shadowBlur on hundreds of nodes is the classic fps killer.
- Edge glow: single stroked pass with pre-multiplied alpha color (no filter).
- Starfield + vignette: painted once to an offscreen layer, blitted per frame.
- Freeze d3 simulation after settle (alphaMin), reheat only on data change.
- Budgets: 60fps @ 200 nodes (Stage-1 gate), 500 nodes (Stage 6 gate),
  degrade order above budget: particles → decor → glow pass → beads (never
  drop real nodes). 2000 nodes = explicitly the GPU-stage trigger (see G).

## 14. Accessibility fallback
Canvas is aria-hidden; a parallel structured list (existing TaskChecklistCard
+ a per-task run list in DetailPopover) is the accessible surface — document
this pairing in the component; stage toggle "List view" renders the same model
as DOM (Stage 6). Filter chips + list keep full keyboard operability;
announcements via polite live region.
