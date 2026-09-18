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

Round 5, the closure sequence's integration gate: book round 4's
verdict, append the feature file's Built State, and run the full suite
once, committing its transcript.

## Next Steps

1. Repair whatever the closure suite lists, under the shrinking rule of
   operator amendment amend0917-throughput (2).
2. Closure round A: the self-use item, the integrity check, the evidence
   job and the review package.
3. Closure round B: the verdict bookings, the ledger rotation, STATUS,
   README and the pull request.
