# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1, D4, D5 and D7).

## Current Step
Session 2, round 6: book round 5 (PASS) and one prose slip, record DECISION F200 D7 with the
feature file's addendum, and land the restart: `RunLauncher.resume_registered` adopts, runs again
or records as lost every run the registry holds open, `run_supervisor` calls it before it serves,
and the SIGKILL kill test proves it. The open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`,
`R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. The systemd unit, the container entrypoint and the built-state page.
2. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
- Outside Linux a live process id alone marks a run as adopted (DECISION F200 D7).
