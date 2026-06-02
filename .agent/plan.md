# Plan — Steps 335-342

## Goal
Operator Cockpit v2: pipeline visibility, stop-reason UX, read-only decision queue.

## Current Step
All steps complete. Ready for commit + push.

## Steps
- [x] Step 335: Preflight — repo clean, no tracked artifacts, docs exist, tests green
- [x] Step 336: Pipeline status contract in dashboard v4 (additive `pipeline` object with 30+ fields)
- [x] Step 337: Pipeline timeline component (PipelineTimeline with step states)
- [x] Step 338: Stop reason card + next safe command (StopReasonCard with copy-to-clipboard)
- [x] Step 339: Read-only decision queue (approval visibility via pipeline.approval_status/intent_id)
- [x] Step 340: Repair loop visibility (repair_loop object in pipeline + repair step in timeline)
- [x] Step 341: Memory and source context operator visibility (ContextCard + pipeline.source_context/memory)
- [x] Step 342: Baseline 3895 passed, 7 skipped. Vitest 31. TypeScript clean. Build OK.
