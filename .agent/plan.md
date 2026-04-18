# Plan

## Goal
Step 3.5: Planning Semantics Hardening — clarify planned/unplanned job states,
orchestration-owned artifacts, and explicit plan_job result shape.

## Current Step
In progress on feature/step3-orchestration-skeleton (PR #4 open).
Step 3.5 is in-scope: same feature boundary as Step 3.

## Next Steps
1. packages/core/models.py — add PLANNED to RunState
2. packages/core/models.py — clarify Artifact.task_id=None convention in docstring
3. packages/orchestration/job_runner.py — PlanJobResult dataclass + PLANNED state
4. apps/cli/main.py — use PlanJobResult.changed
5. tests/test_runner.py — update for new API, add PLANNED + changed tests
6. docs/architecture.md — document orchestration-owned artifact convention
7. README.md — update planned state description
8. Push, update PR

## Decisions
- PlanJobResult is a dataclass (not Pydantic) — it's a return type, not a domain model
- PLANNED state: planning complete, tasks ready to execute (distinct from PENDING)
- task_id=None convention documented in Artifact docstring + architecture.md
