# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1 and D4).

## Current Step
Session 1, round 4: book round 3 (PASS), record DECISION F200 D4 with the feature file's addendum
and operator question Q4's update, and land the supervisor's runs:
`packages/orchestration/serve_runs.py`, the door's `_dispatch_extra_command` hook, and the socket
handler's `job.run`. The open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`,
`R-1129`, all owned by F290).

## Next Steps
1. `remedy job run` in client mode: hand the job to the supervisor and follow its output to the
   end, printing it and exiting as the run does.
2. The restart that runs registered jobs again, with its SIGKILL test.
3. The systemd unit, the container entrypoint and the built-state page.
4. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
