# Plan — F026 Task edit at runtime

Branch: feature/f026-task-edit-runtime, cut from `main` at `90555849`, the
merge commit of pull request 280 (F025 Pause/resume).

## Goal

Course correction without restarting the world: a waiting, paused or
failed task of an approved plan is edited, gains a new spec version with
the prior one archived, and its next run provably carries the edit in
its prompt trace (`docs/roadmap/features/T5_F026.md`).

## Current Step

ROUND 3: book round 2 and resolve R-1059, record DECISION F026 D3,
reword `job.edit-task`'s help text, and land T003's first half — the
dashboard's `task_specs` section, the version chip on the node and in
the popover, and the popover's Versions list.

## Next Steps

1. T003's second half: the edit affordance on eligible nodes only,
   sent through the write door, and the end-to-end — fail, edit through
   the door, relaunch, the new trace carrying the edit, the fan visible.
2. The closure sequence.

## Risks

A chip must not read as a state; it is text in the state's own line
colour and never a mark. Open findings: 4 — R-1008, R-1055, R-1057 and
R-1058, all owned by F285.
