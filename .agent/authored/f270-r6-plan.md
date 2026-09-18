# Plan — F270 History apply: one commit per task, merge on demand

Branch: feature/f270-history-apply, cut from `main` at `b7f966c0` (the
merge commit of pull request 257, F269's closure).

## Goal

Every applied task lands as one commit on the job worktree branch, and
`job apply` gains the operator's flag family — `--commit-with-history`,
`--commit "<message>"`, `--commit-auto`, `--push` — that lands those
changes on the operator's branch only when the operator asks
(`docs/roadmap/features/T2_F270.md`).

## Current Step

Round 6, closure round A: book round 5's verdict and R-0978 for F273,
then the self-use item, the integrity check, the evidence job and the
review package at the accepted head.

## Next Steps

1. Closure round B: the verdict bookings, the ledger rotation, STATUS,
   README, the self-use item consumed, and the pull request.
