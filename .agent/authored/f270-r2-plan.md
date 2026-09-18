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

Round 2: book round 1's verdict, land DECISION F270 D2 and build T002
with T003 — `job apply --approve --commit-with-history` merges
`remedy/job-<job id>` with `--no-ff` under the operator's identity, and
refuses a dirty tree, a conflict, a staging target, a detached checkout
and a branch that is not the reviewed work, changing nothing.

## Next Steps

1. T004: `--commit "<message>"`, `--commit-auto`, `--push` and the
   config key `apply.push_after_mission`, with `do` passing the whole
   flag family through.
2. The closure sequence: Built State, the one full-suite run, self-use,
   evidence and review package, STATUS and the pull request.
