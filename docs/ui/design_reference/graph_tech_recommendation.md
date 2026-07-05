# G — Graph Technical Recommendation (independent, codebase-grounded)

## Situation (verified)
Three implementations exist. **Mounted today:** `BrainGraphCanvas.tsx` — SVG,
deterministic radial fan, honest but visually far from the reference (straight
edges, no glow/particles/zoom, 80-task cap). **Built but unmounted:**
`ForceBrainGraph.tsx` — react-force-graph-2d (dependency already present) with
custom canvas painting: gradient core+halo, glossy state spheres, decorative
`layout_only` dots with hit-test exclusion, custom link painting; model builder
`buildForceBrainModel.ts` is unit-tested. **Legacy:** SVG `RemedyBrainFlow` +
`organicLayout.ts`/`semanticZoom.ts` — superseded, but its organic-layout and
zoom-threshold ideas are worth mining. Data arrives by polling (no SSE yet).

## Options evaluated against the screenshot
| Criterion | A) SVG (current mounted) | B) fg-2d + custom paint | C) bespoke Canvas2D | D) PixiJS v8 (WebGL/WebGPU) |
|---|---|---|---|---|
| Glow/bloom filaments | weak (SVG filters slow >100 nodes) | **good** (sprite gradients) | good | **best** (shader bloom) |
| Particles | poor | **native** (`linkDirectionalParticles`) + custom | manual | best |
| Organic curved edges | manual paths, ok | **custom linkCanvasObject — full control** | full control | full control |
| Semantic zoom | manual | zoom API + `onZoom` hooks exist | manual | manual |
| React 19 fit | native DOM | thin wrapper (already typed in repo) | ref-managed | ref-managed, heavier |
| Maintainability here | high but dead-end visually | **high — 869 LoC path already in repo, tested builder** | medium (own engine) | medium-low (new stack) |
| Perf @200 | fine | **fine** | fine | fine |
| Perf @500 | risky (DOM nodes) | fine with sprite glow + frozen sim | fine | fine |
| Perf @2000 | no | borderline (CPU canvas) | borderline | **yes, 60fps** |
| Migration risk now | — | **lowest** | medium | highest |
| A11y fallback | DOM "free" but misleading | canvas + list pairing (spec §14) | same | same |

## Recommendation
**Stage 1–5 (production v1): Option B — react-force-graph-2d with full custom
node+link painting**, evolving the existing unmounted `ForceBrainGraph.tsx`
into `renderers/ForceBrainRenderer.tsx`, mounted by `BrainGraphStage`. Reasons:
it is already a dependency, already typed (`types/react-force-graph-2d.d.ts`),
already half-built and unit-tested; d3-force is the right layout engine for
the radial organic look; the two visual gaps (glow, curved beaded edges) are
paint-layer work, not framework work — solved by sprite-gradient glow and
custom quadratic link painting (graph_spec §6, §13). The generic force-graph
look is avoided precisely because BOTH nodeCanvasObject and linkCanvasObject
are fully custom — the library contributes simulation, zoom/pan and hit
testing only.

**Premium/final stage (only if measured): Option D — PixiJS v8 renderer behind
the same model + a RendererPort interface.** Trigger is a FAILED measurement:
if the Stage-6 gate (60fps @500 nodes, and the later 2000-node ambition for
org views) cannot be met by B, port the painter to Pixi (WebGPU with WebGL
fallback), keeping `buildForceBrainModel`, the palette bridge, glyph paths and
the zoom state machine unchanged. This mirrors the staged decision already
recorded in `docs/roadmap/features/T1_F019.md` — the codebase and the roadmap
agree; do not jump to WebGL on hype.

**Keep:** `buildForceBrainModel.ts` (+test) as the single data→graph builder;
the `layout_only` truth pattern; `BrainGraphCanvas.tsx` demoted to explicit
fallback ("simple view" + no-WebGL path) until Stage 6, then archive with
`graph/legacy/`. **Replace later:** legacy folder (after mining
`semanticZoom.ts` thresholds), MUI dependency (unrelated cleanup).

## Risks
- Canvas glow perf: mitigated by sprite pre-render (graph_spec §13) — measure
  in Stage 1 with a 500-node fixture before building more.
- fg-2d API drift: version pinned (1.29.1) + the repo's own .d.ts; renderer
  isolated behind RendererPort so a swap stays a leaf change.
- Polling jitter causing layout jumps: freeze simulation, diff snapshots,
  reheat locally around changed nodes only.
- Screenshot fidelity is judged at L0 rest state — build the Stage-1 fidelity
  fixture from the SAME task distribution as the reference (≈36 tasks) so
  comparisons are meaningful.

## Test strategy
Unit: model builder (exists — extend for runs/synapses + differ), palette
bridge, zoom state machine (transition matrix). Visual: golden screenshots of
seeded fixture states (rest, active, failed, filtered, reduced-motion) with
per-region SSIM + human checklist (see J). Perf: scripted fixture at
200/500 nodes asserting frame-time p95 in a headless trace. Truth: property
test — rendered real-node ids == view-model ids; decor never hit-testable.
