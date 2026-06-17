# Plan — Steps 2586-2615: Mission Run Loop + Morning Report v0

## Goal
Bounded mission run loop + clear morning report. Not full overnight autonomy.

## Steps
- [x] Step 2586: Mainline gate (PR #85 merged, clean working tree)
- [x] Step 2587: Core path audit
- [x] Step 2588: Terminology note in docs (mission-run-loop-morning-report-v0.md)
- [x] Step 2589: Bounded loop behavior (10 stop conditions, _WAITING_STATUSES)
- [x] Step 2590: run_mission_loop() function
- [x] Step 2591: MissionRunLoopResult model
- [x] Step 2592: MissionMorningReport model
- [x] Step 2593: build_mission_morning_report()
- [x] Step 2594: CLI dogfood run-loop
- [x] Step 2595: CLI dogfood morning-report
- [x] Step 2596: Alias assessment (skipped — no alias infra, documented)
- [x] Step 2597: Fix stale CLI examples (--adapter → --adapter-id)
- [x] Step 2598: Core readiness summary (_build_core_readiness)
- [x] Step 2599: Loop checkpoint safety (step_dogfood_run records checkpoints)
- [x] Step 2600: Self-repair in report (_build_self_repair_summary)
- [x] Step 2601: Builder/execution visibility (_build_builder_execution_summary)
- [x] Step 2602-2607: Tests (8 loop + 8 report = 16 new)
- [x] Step 2608: Catalog + contract entries
- [x] Step 2609: Review bundle (stop_reason, next_safe_action, morning_report_available)
- [x] Step 2610: Docs (mission-run-loop-morning-report-v0.md)
- [x] Step 2611: Architecture guard scan (no shell=True, no provider, no auto-apply)
- [x] Step 2612-2613: Targeted (538) + full suite (6800 passed)
- [ ] Step 2614: Final handoff

## Hard rules
No auto-apply/approve/PR/git; no provider SDK; no shell=True; no secret storage;
no raw leaks; no fake mission satisfaction; no fixed-duration profiles.
