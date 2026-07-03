# UI Target Direction

> **Status: DEPRECATED** — Superseded by `docs/roadmap/ROADMAP.md` Teil H +
> `docs/ui/design_reference/ux_design.png`.

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
| Brain graph | `minmax(0, 1fr)` — largest area, shrinks before timeline |
| Bottom timeline | `clamp(136px, 15vh, 166px)` — process rail with phases + events |

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

### Phase Header (Row 1)
- Six phases: Job, Planning, Build, Test, Review, Finalized
- Each phase shows its REAL phase icon (briefcase, calendar, code, checklist, person, flag)
- **Phase icons ALWAYS stay visible** — never replaced with checkmarks
- Done/current/pending are VISUAL CLASSES on the icon shell, not icon replacements
- Current phase has blue gradient circle with glow
- Done phases keep their icon, with blue border
- Pending phases are faint/transparent

### Progress Rail (Row 2)
- Thin connecting line with blue gradient fill
- Phase markers on the rail show status:
  - Done markers: filled blue circle with small checkmark
  - Current marker: larger, blue with glow
  - Pending markers: empty, faint border

### Event Rail (Row 3 — conditional)
- Only shows when REAL timeline events exist from the event ledger
- No fake events from tasks
- Dashed line with bordered dots
- Blue dot = LLM action, green border = test, purple border = review
- Pending events have dashed borders

### Legend (Row 4 — conditional)
- Only shows when event rail is visible
- Three entries: LLM Action, Test, Review

### Timeline Must Support Loops
- Build/Test/Review may repeat multiple times
- Timeline events show cycle numbers
- Finalized means ALL gates passed (no pending tasks, no blocked tasks, no open approvals)

## Style

- Premium white/blue glass
- `backdrop-filter: blur()`
- Soft shadows, not heavy
- Subtle borders `rgba(61,98,164,.12)`
- No saturated neon
- No debug rails
- Reduced motion respected
- **No `overflow: hidden` on timeline** — clips glow effects

## What Not To Do

- Do not make the right panel wider than the graph
- Do not add a fifth row to the main grid
- Do not put ProjectSummaryCard in the main grid
- Do not show fake data
- Do not add mutation buttons
- Do not show raw content (source, model output, prompts, diffs, secrets)
- Do not replace phase icons with checkmarks in the header
- Do not create fake timeline events from planned tasks
- Do not mark Finalized unless all gates pass

## Manual QA Checklist

Before shipping UI changes, check:

- [ ] Graph dominates the center
- [ ] Right panel is compact (not wider than ~360px)
- [ ] Bottom timeline is visible and not clipped
- [ ] Phase icons show as briefcase/calendar/code/checklist/person/flag
- [ ] Done phases KEEP their real phase icons (not replaced with checkmarks)
- [ ] Current phase has strong blue visual
- [ ] Event rail ABSENT when no real events
- [ ] Event rail shows only real backend events (not task-derived)
- [ ] Exactly five top metrics
- [ ] No debug walls or oversized cards
- [ ] Commands are copy-only
- [ ] UI stays read-only
- [ ] Unknown data shown as unknown, not fake
- [ ] No raw content visible

## Screenshot Self-Check (Step 562)

Before claiming visual QA pass, answer:

1. Do phase icons show as Koffer/Kalender/Code/Test/Review/Flag? (expected: yes)
2. Are they centered like target? (expected: yes, grid-centered with label beside)
3. Is Build/current visually strong? (expected: blue gradient circle with glow)
4. Are done phases still real phase icons? (expected: yes, NOT checkmarks)
5. Is event row absent when no real events? (expected: yes)
6. Is timeline not clipped? (expected: yes, overflow: visible)
7. Does it look closer to target than previous screenshot? (expected: yes)
