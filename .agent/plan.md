# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person or a program can read
one job's or run's lines in order on the command line and on the public API; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D7).

## Current Step
Round 10 on `feature/f203-structured-logging`, session 2, the closing round: book round 9's PASS,
the Built State, the ledger rotation, the STATUS flip with the README sync and the self-use entry
`SU-061`'s `consumed_by`, the handback, the push and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1, then the Open PR Gate merges F203's pull request; the next
   feature's first commit books round 10's verdict; Rule A5 names the next feature.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; F203 owns no open finding.
