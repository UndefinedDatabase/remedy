# UI Target Direction

## Layout

The Remedy dashboard has three columns:

1. **Left brand rail** — narrow, logo and navigation
2. **Center main area** — four rows: metrics, command bar, brain graph, phase timeline
3. **Right operator panel** — compact stack of status cards

The brain graph dominates the center. Everything else is compact.

## Proportions

| Area | Target size |
|------|-------------|
| Left rail | `clamp(220px, 16vw, 292px)` |
| Right panel | `clamp(280px, 22vw, 360px)` |
| Top metrics | `clamp(56px, 7vh, 72px)` |
| Command bar | `clamp(40px, 5vh, 50px)` |
| Brain graph | `minmax(300px, 1fr)` — largest area |
| Bottom timeline | `clamp(80px, 11vh, 110px)` — slim rail |

## Right Operator Panel

Stack order:
1. Live status pill
2. Agent is doing now
3. Project status (compact)
4. Pipeline / why it stopped
5. Activity feed
6. Task checklist

Rules:
- Cards share compact spacing (`10px` gap)
- Card padding around `10px 12px`
- No heavy nested glass cards inside the panel
- Labels `10px`, body text `11px`
- No debug walls
- No oversized cards

## Bottom Phase Timeline

- Slim horizontal glass rail
- Six phases: Job, Planning, Build, Test, Review, Finalized
- Current phase has blue glow ring
- Done phases filled/checked
- Future phases faint grey
- Thin connecting line (`1-2px`)
- Compact height, no bulky card feel

## Style

- Premium white/blue glass
- `backdrop-filter: blur()`
- Soft shadows, not heavy
- Subtle borders `rgba(61,98,164,.12)`
- No saturated neon
- No debug rails
- Reduced motion respected

## What Not To Do

- Do not make the right panel wider than the graph
- Do not add a fifth row to the main grid
- Do not put ProjectSummaryCard in the main grid
- Do not show fake data
- Do not add mutation buttons
- Do not show raw content (source, model output, prompts, diffs, secrets)

## Manual QA Checklist

Before shipping UI changes, check:

- [ ] Graph dominates the center
- [ ] Right panel is compact (not wider than ~360px)
- [ ] Project Brain feels like a small status card
- [ ] Bottom timeline is slim (under ~110px)
- [ ] Exactly five top metrics
- [ ] No debug walls or oversized cards
- [ ] Commands are copy-only
- [ ] UI stays read-only
- [ ] Unknown data shown as unknown, not fake
- [ ] No raw content visible
