# Plan — Steps 545-564

## Goal
Fix timeline visual failures from Steps 530-544. Encode orchestrator loop semantics. Remove fake events.

## Current Step
Complete — all steps done.

## Steps
- [x] Step 545: Handoff, acknowledge timeline failure, update context/plan/live_review
- [x] Step 546: Replace RemedyTimelineEvent type (state/title/cycle/timeLabel)
- [x] Step 547: Normalize timeline events safely (no fake events, returns [])
- [x] Step 548: Backend timeline events with state/title/cycle/time_label
- [x] Step 549: Finalized gate strict (checks pending/blocked tasks + approvals)
- [x] Step 550: Replace PhaseTimeline.tsx (PhaseGlyph always in header, TaskDoneGlyph only in rail)
- [x] Step 551: Replace PhaseTimeline.module.css (no overflow:hidden, state classes)
- [x] Step 552: Remove fallbackEventsFromTasks (event rail conditional on real events)
- [x] Step 553: Fix PhaseGlyph icons (strokeWidth=1.45 for visibility)
- [x] Step 554: Shell timeline height lock (clamp(136px, 15vh, 166px))
- [x] Step 555: Orchestrator loop contract doc (docs/orchestrator-loop.md)
- [x] Step 556: Proposed task evaluation model (RemedyProposedTask type)
- [x] Step 557: Timeline reflects loops (cycle-aware backend events)
- [x] Step 558: Task list separates proposed from planned (type contract only)
- [x] Step 559: Product tests (24 tests: icons, no fake events, CSS, types, backend, loop)
- [x] Step 560: Orchestrator loop tests (in test_timeline_guard.py)
- [x] Step 561: Visual QA checklist update (docs/ui-target.md)
- [x] Step 562: Screenshot self-check checklist (in docs/ui-target.md)
- [x] Step 563: Guarded tests — 4216 passed, 0 failed, Vitest 35, tsc clean, build 332KB
- [x] Step 564: Handoff report
