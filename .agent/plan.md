# Plan — F026 Task edit at runtime

Branch: feature/f026-task-edit-runtime, cut from `main` at `90555849`, the
merge commit of pull request 280 (F025 Pause/resume).

## Goal

Course correction without restarting the world: a waiting, paused or
failed task of an approved plan is edited, gains a new spec version with
the prior one archived, and its next run provably carries the edit in
its prompt trace (`docs/roadmap/features/T5_F026.md`).

## Current Step

ROUND 4: book round 3, register R-1060, record DECISION F026 D4, repair
R-1060, and land T003's second half — the edit affordance in the detail
popover for eligible tasks only, its send module, and the end-to-end
through the CLI and the real door.

## Next Steps

1. The closure sequence: the Built State, the checklist consolidation,
   the self-use item and the feature's one full suite; then the
   evidence bundle and the review package; then the acceptance and the
   pull request.

## Risks

The edit must reach the door only through its send module, and only for
a task the dashboard marks editable. Open findings: 5 — R-1008, R-1055,
R-1057 and R-1058, owned by F285, and R-1060, owned by F026.
