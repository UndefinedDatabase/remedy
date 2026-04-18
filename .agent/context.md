# Context

## Active Branch
`feature/step3-orchestration-skeleton`

## PR
https://github.com/UndefinedDatabase/remedy/pull/4

## Scope
Step 3: First Orchestration Skeleton — minimal deterministic job-planning flow.

## Constraints
- No LLM calls
- No async
- No providers
- No Docker or MemPalace
- No retries or worker routing
- No new external dependencies

## Assumptions
- plan_job() mutates Job in place (Pydantic v2 models are mutable)
- Idempotency: if job.tasks or job.artifacts exist, return unchanged
- planning result is fully serializable via existing models
- plan-job CLI command loads, plans, and saves in one step

## Branch Scope Decision
Step 3 is a new branch: orchestration logic (plan_job, job_runner) has
a different purpose, scope, and merge intent from Step 2/2.5 (packaging + CLI).
PR #3 was merged before creating this branch.
