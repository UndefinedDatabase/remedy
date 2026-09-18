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

Closed. Round 7 booked the closure verdict PASS_WITH_RISKS, rotated the
ledger and flipped STATUS; the pull request into `main` waits for the
Open PR Gate.

## Next Steps

1. The next session merges F270's pull request at the Open PR Gate, then
   claims the next feature under Rule A5.
