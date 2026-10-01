# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends the door's commands and `job run` to it while it runs, and it runs
again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISION F200 D1).

## Current Step
Session 1, round 2: book round 1 (FAIL; R-1131, owned by F200, registered), record DECISION F200
D2, and land the supervisor: `packages/orchestration/serve_daemon.py`, the `effect_source`
attribute of the cockpit's handler, `remedy serve start`, `status` and `stop`, and their tests;
the import chain repairs R-1131 and is marked `Landed:`. The open-findings count is 6 (`R-1117`,
`R-1125`, `R-1127`, `R-1128`, `R-1129`, owned by F290; `R-1131`, owned by F200).

## Next Steps
1. Client detection, with `job.stop`, `job.pause` and `job.unpause` forwarded and one test module
   that runs them in both modes.
2. The door's other commands the command line shares, forwarded.
3. `job run` through the supervisor, with its run registry.
4. The restart that runs registered jobs again, with its SIGKILL test.
5. The systemd unit, the container entrypoint and the built-state page.
6. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- A command the door does not carry runs direct in both modes (DECISION F200 D1 (3)).
