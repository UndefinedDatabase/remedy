# Plan — F026 Task edit at runtime

Branch: feature/f026-task-edit-runtime, cut from `main` at `90555849`, the
merge commit of pull request 280 (F025 Pause/resume).

## Goal

Course correction without restarting the world: a waiting, paused or
failed task of an approved plan is edited, gains a new spec version with
the prior one archived, and its next run provably carries the edit in
its prompt trace (`docs/roadmap/features/T5_F026.md`).

## Current Step

ROUND 1: claim F026, re-head the live review record, book F025's round
11, record DECISION F026 D1, and land T001 —
`packages/orchestration/task_edit_runtime.py`, the state gate, the
versioned in-place apply, the spec archive, the approval seal and the
failed-to-pending reset, with the task's `spec_version` field and its
unit tests.

## Next Steps

1. T002: `job.edit-task` in the catalog, the CLI and the write door with
   its audit, and the trace-proof test on a fake run — a failed task
   edited, relaunched, its trace carrying the new spec and no remnant of
   the old one.
2. T003: the version chip, the popover's version list, the edit
   affordance on eligible nodes only, and the end-to-end.
3. The closure sequence.

## Risks

An edit must never be lost to a running job's save; it is refused while
the job runs. Open findings: 4 — R-1008, R-1055, R-1057 and R-1058, all
owned by F285.
