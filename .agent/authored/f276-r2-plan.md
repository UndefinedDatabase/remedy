# Plan — F276 Data-root hygiene & disk budget

Branch: feature/f276-data-root-hygiene, cut from `main` at `43d14817`
(the merge commit of pull request 260, F273's closure).

## Goal

Every directory class under the data root has a named owner and a reclaim
rule, an operator reclaims scratch through one preview-first command, and a
job refuses to start below a disk floor
(`docs/roadmap/features/T2_F276.md`).

## Current Step

Round 2 books round 1's verdict and resolves R-1001, lands DECISION F276 D3
— `workspaces`, `runs` and `job_logs` are durable because live readers
depend on them — and builds T002: `remedy data reclaim`, dry run by default,
whose `--apply` removes only the paths its own preview named and refuses
everything else by name.

## Next Steps

1. T003 — the copy-mode lifecycle: `release_staging_workspace(job_id)` on the
   terminal-state hook, a `.gitignore`-aware copy filter and a per-file size
   ceiling, with the release call's removal as the red proof.
2. T004 — `min_free_disk_bytes` on `JobBudgets` behind an injectable probe,
   checked at job start and every safe point, exhaustion taking the STOPPED
   path with post-mortem reason `disk_exhausted`, and a `doctor` disk section.
3. The closure sequence: the Built State, the integration gate's one full
   suite run, the evidence job and review package, the STATUS flip and the
   pull request.
