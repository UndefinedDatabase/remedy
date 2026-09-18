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

Round 4: book round 3's verdict with the resolutions of R-0975 and
R-0976, register R-0977 for F273, land DECISION F270 D4 with its
operator question, and build the `do` half of T004 — `do` takes the
whole flag family, chains its jobs under a commit flag, pushes once per
mission, honours `apply.push_after_mission`, and a push waits only for
a red blocking criterion.

## Next Steps

1. The closure sequence: Built State, the one full-suite run, self-use,
   evidence and review package, STATUS and the pull request.
