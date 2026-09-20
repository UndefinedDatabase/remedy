# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 4 books round 3's verdict, resolves R-1002 with the reading the built
command gives on the operator's own root, and builds T003 under DECISION
F276 D5: `release_staging_workspace`, the hook that calls it under the
worktree path's own condition, the `.gitignore`-aware copy filter and the
16 MiB size backstop.

## Next Steps

1. T004 — `min_free_disk_bytes` on `JobBudgets` behind an injectable probe,
   a `free_disk` limit in `budget_guard.evaluate_budget`, checked at job
   start and every safe point, exhaustion taking the STOPPED path with
   post-mortem reason `disk_exhausted`, and a `doctor` disk section.
2. The closure sequence part one: the Built State paragraph, the integrity
   check, the integration gate's one full suite run with its transcript
   committed, and the evidence job with a fresh review package.
3. The closure sequence part two: the STATUS flip with the README counters
   and the pull request into `main`, which the next session's Open PR Gate
   merges.
