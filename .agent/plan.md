# Plan — Steps 435-449

## Goal
Background worker v1: job lifecycle, local queue, worker lock/lease, run-once/bounded, pause/cancel, dashboard.

## Current Step
All steps complete.

## Steps
- [x] Step 435: Clean handoff truth
- [x] Step 436: Job lifecycle model (11 states, valid transitions)
- [x] Step 437: Local job queue (enqueue, list, get_next, file-based)
- [x] Step 438: Worker lock/lease (claim, release, stale detection)
- [x] Step 439: Worker run once (one-shot, fixture/ollama/none providers)
- [x] Step 440: Bounded worker loop (max_jobs, max_seconds, idle_timeout)
- [x] Step 441: Heartbeat and worker status (file-based, safe export)
- [x] Step 442: Pause and cancel (CLI: job pause, job cancel, resume_queued)
- [x] Step 443: Approval-aware worker stop (waiting_for_approval state)
- [x] Step 444: Test resource safety (single job, no parallel tests, timeout)
- [x] Step 445: Stale recovery (lease expiry, reclaim by new worker)
- [x] Step 446: CLI commands (worker.run, worker.status, job.enqueue, job.pause, job.cancel)
- [x] Step 447: Dashboard worker field (read-only, safe metadata)
- [x] Step 448: Worker docs (docs/worker.md, plain language)
- [x] Step 449: Baseline (4127 passed, 8 skipped)
