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

Round 1: claim F270, book F269 round 13's verdict, register R-0974, land
DECISION F270 D1 and build T001 — the per-task commit on
`remedy/job-<job id>`.

## Next Steps

1. T002 and T003 together: `job apply --approve --commit-with-history`
   merges the job branch with `--no-ff`, refusing on a dirty operator
   tree, on a conflict and on a staging target.
2. T004: `--commit "<message>"`, `--commit-auto`, `--push` and the
   config key `apply.push_after_mission`, with `do` passing them through.
3. The closure sequence: Built State, the one full-suite run, self-use,
   evidence and review package, STATUS and the pull request.
