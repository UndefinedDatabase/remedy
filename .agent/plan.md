# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1, D4, D5, D7 and D8).

## Current Step
Session 2, round 7: book round 6 (FAIL, the reviewer's selection), register R-1132 and R-1133,
record DECISION F200 D8 with the feature file's addendum, repair R-1132 by registering
`REMEDY_SERVE_DIRECT`, and land the systemd unit, the container entrypoint, their tests and the
built-state page `docs/system/serve-daemon-v1.md`. The open-findings count is 7 (`R-1117`,
`R-1125`, `R-1127`, `R-1128`, `R-1129`, `R-1133`, owned by F290, and `R-1132`, owned by F200).

## Next Steps
1. The amend0930b-slow-cap hardening stage: an acceptance audit by a fresh worker, then repairs.
2. The closure sequence.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
- Outside Linux a live process id alone marks a run as adopted (DECISION F200 D7).
- No test yet shows a STOP file stopping a run the supervisor started; the audit must answer it.
