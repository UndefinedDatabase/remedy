# Plan

## Goal
Step 3 + 3.5: First Orchestration Skeleton + Planning Semantics Hardening.

## Current Step
Step 3.5 — COMPLETE. Pushing and updating PR #4.

## Completed
- [x] RunState.PLANNED added
- [x] Artifact.task_id=None convention documented (docstring + architecture.md)
- [x] PlanJobResult dataclass (job, changed)
- [x] plan_job returns PlanJobResult; state goes PENDING -> PLANNED
- [x] CLI uses PlanJobResult.changed
- [x] Tests updated + new tests for PLANNED, changed, task_id=None
- [x] README + architecture.md updated

## Next Steps
Step 4: TBD (task execution or provider scaffolding)
