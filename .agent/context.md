# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 470-484: Dashboard product rebuild — complete.

## Completed
- Font: --remedy-font-display/ui, no external fonts, antialiased
- Icons: RemedyGlyphs.tsx with 8 custom SVG components (no MUI in primary)
- Graph: BrainGraphCanvas — deterministic SVG from dashboard.tasks, no force sim, no fake dots
- Right panel: user-first (NeedsAttention + Activity + Tasks primary), Worker/Pipeline/Project in collapsed advanced
- Timeline: 6 canonical phases with progress track, custom PhaseGlyph, no fake dots
- Filter: "Needs work" instead of "Open"
- CLI: not in primary UX, only in collapsed advanced details
- Build: 327KB (down from ~500KB+), no react-force-graph-2d in primary

## Resource-Safety Rules (permanent)
- Never run pytest in background
- Always use scripts/remedy_pytest.sh for pytest execution

## Constraints
- UI remains read-only
- No external fonts
- No fake graph nodes
- No raw content in UI

## Dashboard Readiness
Significantly closer to target. Not pixel-perfect — needs manual QA and iteration.
Graph is deterministic and real. Right panel is user-facing. Timeline has progress.

## Recommended Next Block
Steps 485-494 — Real Ollama Trial Round
