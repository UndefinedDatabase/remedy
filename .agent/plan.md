# Plan — Steps 530-544

## Goal
Rebuild timeline to match target screenshot. Cycle-aware events, correct icons, proper visual structure.

## Current Step
Complete — all steps done.

## Steps
- [x] Step 530: Context/plan update, acknowledge timeline failure
- [x] Step 531: Add RemedyTimelineEvent type + timelineEvents to RemedyDashboard
- [x] Step 532: Backend timeline_events in ui_server.py + 6 canonical phases
- [x] Step 533: PhaseTimeline.tsx rewrite (phaseHeader + rail + eventRail + legend)
- [x] Step 534: PhaseTimeline.module.css rewrite (rounded icon shell, dashed event line, bordered dots)
- [x] Step 535: Wire timelineEvents through shell + normalizer
- [x] Step 536: Timeline loop semantics (Build/Test/Review repeat via cycle-aware events)
- [x] Step 537: Shell height lock (clamp(128px, 14.5vh, 158px) + minmax(0, 1fr))
- [x] Step 538: Right panel alignment (no changes needed — already aligned)
- [x] Step 539: Fix PhaseGlyph icons (build=code, review=person, job=briefcase, test=flask)
- [x] Step 540: Timeline product tests (12 new tests in test_timeline_guard.py)
- [x] Step 541: Graph de-emphasis comment
- [x] Step 542: Task outcome panel — honest "no detailed outcome was recorded"
- [x] Step 543: Visual QA — TypeScript clean, build 332KB, Vitest 35, pytest 4204/0/8
- [x] Step 544: Guarded baseline — 4204 passed, 0 failed, 8 skipped
