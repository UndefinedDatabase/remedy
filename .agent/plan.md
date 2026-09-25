# Plan — F026 Task edit at runtime

Branch: feature/f026-task-edit-runtime, cut from `main` at `90555849`, the
merge commit of pull request 280 (F025 Pause/resume).

## Goal

Course correction without restarting the world: a waiting, paused or
failed task of an approved plan is edited, gains a new spec version with
the prior one archived, and its next run provably carries the edit in
its prompt trace (`docs/roadmap/features/T5_F026.md`).

## Current Step

ROUND 8, the closing round: book round 7, rotate the ledger, accept
F026 in STATUS with its README pins and the self-use item's
`consumed_by`, and open the pull request.

## Next Steps

1. The next feature's session merges this pull request at the Open PR
   Gate, then claims the first unchecked feature in STATUS.

## Risks

Open findings: 5 — R-1008, R-1055, R-1057, R-1058 and R-1064, all owned
by F285.
