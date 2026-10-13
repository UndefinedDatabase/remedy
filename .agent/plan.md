# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person or a program can read
one job's or run's lines in order on the command line and on the public API; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D5).

## Current Step
Round 6 on `feature/f203-structured-logging`, session 1, the closure's first round: book round
5's PASS, the consolidation pass, the closure's self-use item `SU-061` run to its approval gate
and never applied, and the feature's one full suite with its CPU cost.

## Next Steps
1. The closure's evidence round: the staging reclaim, the evidence job and the review package.
2. The closing round: the Built State, the ledger rotation, the STATUS flip and the pull request.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- A red full suite opens repair rounds under amend0917-throughput rule 2.
