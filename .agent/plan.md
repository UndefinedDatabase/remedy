# Plan

## Goal
Step 3: First Orchestration Skeleton — introduce a minimal, deterministic, local job-planning flow.

## Current Step
In progress on feature/step3-orchestration-skeleton (new branch from main after PR #3 merged).

## Next Steps
1. packages/orchestration/job_runner.py — plan_job()
2. CLI: plan-job command
3. tests/test_runner.py — plan_job tests
4. README.md — Step 3 docs
5. Push, create PR

## Decisions
- plan_job is synchronous, local, deterministic — no LLM
- Idempotency: return unchanged if job.tasks or job.artifacts exist
- State: RUNNING during planning, PENDING after (tasks ready to execute)
- 3 fixed tasks + 1 planning artifact
