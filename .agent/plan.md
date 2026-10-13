# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person or a program can read
one job's or run's lines in order on the command line and on the public API; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D7).

## Current Step
Round 8 on `feature/f203-structured-logging`, session 2, the closure's evidence round: commit
round 7's handback, book round 7's PASS and R-1274's resolution, then the staging reclaim, the
evidence job on the accepted head and the review package.

## Next Steps
1. The closing round: the Built State, the ledger rotation, the self-use entry SU-061's
   consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; F203 owns no open finding.
