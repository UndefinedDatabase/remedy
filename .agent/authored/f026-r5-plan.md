# Plan — F026 Task edit at runtime

Branch: feature/f026-task-edit-runtime, cut from `main` at `90555849`, the
merge commit of pull request 280 (F025 Pause/resume).

## Goal

Course correction without restarting the world: a waiting, paused or
failed task of an approved plan is edited, gains a new spec version with
the prior one archived, and its next run provably carries the edit in
its prompt trace (`docs/roadmap/features/T5_F026.md`).

## Current Step

ROUND 5, the closure sequence's first half: book round 4, resolve
R-1060, register and repair R-1061 and R-1062, write the Built State,
consolidate the checklist, generate and run the closure's self-use
item, and run the feature's one full suite.

## Next Steps

1. The closure's second half: book round 5, register what the self-use
   run's defects ask for, repair what the suite requires, build the
   evidence bundle and the review package.
2. The closing round: rotate the ledger, accept F026 in STATUS with its
   README pins and the self-use item's `consumed_by`, open the pull
   request.

## Risks

The one full suite must run on the tree that ships. Open findings: 6 —
R-1008, R-1055, R-1057 and R-1058, owned by F285, and R-1061 and
R-1062, owned by F026.
