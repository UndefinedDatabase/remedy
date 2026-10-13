# Plan — F203 Structured logging & correlation

## Goal
Remedy writes what it does to one operations log: a JSON line per record carrying the job, task
and run ids, owner-only under `<data root>/logs/`, rotated by size; a person or a program can read
one job's or run's lines in order on the command line and on the public API; and no `print`
remains in `packages/` unexcused (docs/roadmap/features/T12_F203.md; DECISIONs F203 D1 to D7).

## Current Step
Round 9 on `feature/f203-structured-logging`, session 2: book round 8's PASS, then the one full
suite once more on the tree that ships, because the operator's commit `3f06c01e9` moved the branch
after the recorded run (operator amendment amend0921-operator-feedback rule 1); its transcript
replaces `.agent/authored/f203-closure-suite.txt`.

## Next Steps
1. The closing round: the Built State, the ledger rotation, the self-use entry SU-061's
   consumed_by, the STATUS flip with the README sync, and the pull request, left unmerged.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306; F203 owns no open finding.
- A red suite stops the closure for a repair round under amendment amend0917-throughput rule 2.
