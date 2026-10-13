# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person or a program can read
one job's or run's lines in order on the command line and on the public API; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D6).

## Current Step
Round 7 on `feature/f203-structured-logging`, session 1, the closure's first repair round (of at
most three, amend0917-throughput rule 2): book round 6's PASS, the prose slip and R-1274, and
repair R-1274 by renaming `logging.json` to `logging.json_lines` (DECISION F203 D6). The closure
suite's bad set is that one node; the round must leave it green and add no bad node.

## Next Steps
1. The closure's evidence round: the staging reclaim, the evidence job and the review package.
2. The closing round: the Built State, the ledger rotation, the STATUS flip and the pull request.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; R-1274 by F203.
