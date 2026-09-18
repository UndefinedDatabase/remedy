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

Closed at round 7. Round 8 repairs pull request 258's hosted CI under
AGENTS.md amendment amend0820-gate-autonomy: it books round 7's verdict,
registers R-0979 — `test_delayed_readiness` starts its clock after the
server it times was launched — and moves that clock before `start()`.

## Next Steps

1. The Open PR Gate merges pull request 258 once its hosted CI passes;
   the next feature is then claimed under Rule A5, and its first commit
   books round 8's verdict and R-0979's resolution.
