# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends the door's commands and `job run` to it while it runs, and it runs
again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISION F200 D1).

## Current Step
Session 1, round 1: claim F200, re-head the ledger, book F292's round 14 (PASS), record DECISION
F200 D1 with the feature file's Amendment section and operator question Q4, and land
`packages/orchestration/serve_paths.py` with the durable data-root class `serve`. F200 owns no
open finding. The open-findings count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`,
all owned by F290).

## Next Steps
1. The supervisor: `remedy serve start`, `status` and `stop`, the socket answered by the
   cockpit's own handler with source `cli`, the owner-only token and the process id file.
2. Client detection, with `job.stop`, `job.pause` and `job.unpause` forwarded and one test module
   that runs them in both modes.
3. The door's other commands the command line shares, forwarded.
4. `job run` through the supervisor, with its run registry.
5. The restart that runs registered jobs again, with its SIGKILL test.
6. The systemd unit, the container entrypoint and the built-state page.
7. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- A command the door does not carry runs direct in both modes (DECISION F200 D1 (3)).
