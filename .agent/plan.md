# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends `job stop`, `job pause`, `job unpause` and `job run` to it while it
runs, and it runs again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISIONs F200 D1, D4 and D5).

## Current Step
Session 1, round 5: book round 4 (PASS) and two prose slips, record DECISION F200 D5 with the
feature file's addendum, and land `remedy job run` in client mode: the launcher's `--json` and
import path, the socket's `args.json`, `serve_client.follow_run`, the seam in `_cmd_job_run`, the
exit-code guard's entry, and the run's both-modes tests. The open-findings count is 5 (`R-1117`,
`R-1125`, `R-1127`, `R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. The restart that runs registered jobs again, with its SIGKILL test.
2. The systemd unit, the container entrypoint and the built-state page.
3. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- Every command other than those four runs direct in both modes (DECISION F200 D4).
