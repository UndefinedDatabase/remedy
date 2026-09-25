# Plan — F026 Task edit at runtime

Branch: feature/f026-task-edit-runtime, cut from `main` at `90555849`, the
merge commit of pull request 280 (F025 Pause/resume).

## Goal

Course correction without restarting the world: a waiting, paused or
failed task of an approved plan is edited, gains a new spec version with
the prior one archived, and its next run provably carries the edit in
its prompt trace (`docs/roadmap/features/T5_F026.md`).

## Current Step

ROUND 2: book round 1, register R-1059, record DECISION F026 D2, repair
R-1059, close round 1's unmet test obligation, and land T002 —
`job.edit-task` in the catalog, the CLI and the write door with its
audit, the spec version in `job plan-show`, and the trace proof on a
fake run.

## Next Steps

1. T003: the version chip, the popover's version list, the edit
   affordance on eligible nodes only, and the end-to-end.
2. The closure sequence.

## Risks

An edit must never be lost to a running job's save; it is refused while
the job runs. Open findings: 5 — R-1008, R-1055, R-1057 and R-1058, owned
by F285, and R-1059, owned by F026.
