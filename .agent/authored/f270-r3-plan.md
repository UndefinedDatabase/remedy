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

Round 3: book round 2's FAIL with R-0975 and R-0976, repair both, land
DECISION F270 D3 and build the `job apply` half of T004 —
`--commit "<message>"`, `--commit-auto`, `--push` and the registered
key `apply.push_after_mission`.

## Next Steps

1. The `do` half of T004: `do` passes the whole flag family through,
   pushes once at the end of a mission, and honours
   `apply.push_after_mission`; its not-yet-available refusals go.
2. The closure sequence: Built State, the one full-suite run, self-use,
   evidence and review package, STATUS and the pull request.
